#!/usr/bin/env -S bash -c 'exec "$(dirname "$0")/.tools/venv/bin/python" "$0" "$@"'
"""Runs Halmos and Hevm on the experimental subjects.

Each (subject, tool) pair is executed inside an isolated Foundry project under
repro/work/, containing only the property suite and the concrete subject, so
that each tool sees exactly one contract under test.

Two phases:
  pertest  every test case runs in its own process, with a per-test timeout and
           a memory cap; this gives the verdict, the time and the peak memory of
           each test case (one run).
  suite    the whole suite runs in a single process, as a developer would run it;
           repeated N times. Test cases whose process did not terminate in the
           pertest phase (timeout / out of memory / tool crash) are excluded and
           reported as censored; inconclusive verdicts that terminate are kept.

Usage:
  repro/run.py pertest  [--subjects S ...] [--tools T ...] [--timeout SEC]
  repro/run.py suite    [--subjects S ...] [--tools T ...] [--runs N]
"""
import argparse
import csv
import json
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "repro" / ".tools" / "bin"
WORK = ROOT / "repro" / "work"
RESULTS = ROOT / "results"
EXTRA_ARGS = {"halmos": [], "hevm": []}

STANDARDS = ["ERC20", "ERC721", "ERC1155", "ERC4626"]
IMPLS = ["OpenZeppelin", "Solmate"]
SUBJECTS = [f"{s}_{i}" for s in STANDARDS for i in IMPLS]
TOOL_NAMES = {"halmos": "Halmos", "hevm": "Hevm"}

MEMORY_MAX = os.environ.get("MEMORY_MAX", "10G")
for _line in (ROOT / "repro" / "versions.env").read_text().splitlines():
    if "=" in _line and not _line.startswith("#"):
        os.environ.setdefault(*_line.split("=", 1))
DEFAULT_TIMEOUT = {"ERC20": 1800, "ERC721": 1800, "ERC1155": 1800, "ERC4626": 600}


# --------------------------------------------------------------------------- setup

def workdir(subject, tool):
    std = subject.split("_")[0]
    w = WORK / f"{subject}_{tool}"
    if not (w / "out").exists():
        if w.exists():
            shutil.rmtree(w)
        (w / "test" / tool / "subjects").mkdir(parents=True)
        shutil.copy(ROOT / "foundry.toml", w / "foundry.toml")
        os.symlink(ROOT / "lib", w / "lib")
        os.symlink(ROOT / "src", w / "src")
        shutil.copy(ROOT / f"test/{tool}/{std}{tool}.t.sol", w / f"test/{tool}/{std}{tool}.t.sol")
        name = f"{subject}_{TOOL_NAMES[tool]}"
        shutil.copy(ROOT / f"test/{tool}/subjects/{name}.t.sol", w / f"test/{tool}/subjects/{name}.t.sol")
        subprocess.run(["forge", "build", "--ast", "--root", str(w)], check=True,
                       stdout=subprocess.DEVNULL)
    return w


def test_names(subject, tool):
    """Signatures of the symbolic tests of the concrete subject contract."""
    w = workdir(subject, tool)
    name = f"{subject}_{TOOL_NAMES[tool]}"
    art = json.loads((w / "out" / f"{name}.t.sol" / f"{name}.json").read_text())
    return sorted(sig for sig in art["methodIdentifiers"] if sig.startswith("prove"))


def fname(sig):
    return sig.split("(")[0]


# ------------------------------------------------------------------- measurement

def measured_run(cmd, cwd, timeout, log_path):
    """Runs cmd under a memory cap; returns wall/user/sys/peak RSS and status."""
    full = ["systemd-run", "--user", "--scope", "--quiet",
            "-p", f"MemoryMax={MEMORY_MAX}", "-p", "MemorySwapMax=0"] + cmd
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    peak = 0
    with open(log_path, "w") as log:
        t0 = time.monotonic()
        env = dict(os.environ, COLUMNS="1000", TERM="dumb", NO_COLOR="1")  # unwrapped, plain logs
        proc = subprocess.Popen(full, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                                start_new_session=True, env=env)
        ps = psutil.Process(proc.pid)
        timed_out = False
        while proc.poll() is None:
            try:
                rss = ps.memory_info().rss + sum(c.memory_info().rss for c in ps.children(recursive=True))
                peak = max(peak, rss)
            except psutil.Error:
                pass
            if time.monotonic() - t0 > timeout:
                timed_out = True
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                break
            time.sleep(0.2)
        wall = time.monotonic() - t0
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    rc = proc.returncode
    if timed_out:
        status = "timeout"
    elif rc in (-9, 137):
        status = "oom"
    else:
        status = "exited"
    return {
        "wall_s": round(wall, 3),
        "user_s": round(after.ru_utime - before.ru_utime, 3),
        "sys_s": round(after.ru_stime - before.ru_stime, 3),
        "peak_rss_mb": round(peak / 2**20, 1),
        "returncode": rc,
        "status": status,
    }


def tool_cmd(tool, w, match=None, json_out=None):
    if tool == "halmos":
        cmd = [str(TOOLS / "halmos"), "--root", str(w)]
        cmd += ["--function", match if match else "prove"]
        if json_out:
            cmd += ["--json-output", str(json_out)]
        return cmd + EXTRA_ARGS["halmos"]
    cmd = [str(TOOLS / "hevm"), "test", "--root", str(w)]
    if match:
        cmd += ["--match", match]
    return cmd + EXTRA_ARGS["hevm"]


# ----------------------------------------------------------------------- parsing

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|[⠀-⣿] Parsing [^\n\[]*")


def parse_verdicts(tool, log_text):
    """Returns {test_signature: (verdict, reason)} from a tool log.

    verdict is PASS, FAIL (counterexample reported) or ERROR (no verdict: the
    tool gave up, explored the test only partially, or every path reverted).
    """
    text = ANSI.sub("", log_text)
    verdicts = {}
    if tool == "halmos":
        for m in re.finditer(r"\[(PASS|FAIL|ERROR|TIMEOUT)\]\s+(\w+\([^)]*\))", text):
            # long signatures may be wrapped over several lines by the terminal renderer
            v, sig = m.group(1), re.sub(r"\s+", "", m.group(2))
            if v in ("PASS", "FAIL"):
                verdicts[sig] = (v, "")
                continue
            if v == "TIMEOUT":
                reason = "solver-timeout"
            elif "all paths have been reverted" in re.sub(r"\s+", " ", text):
                reason = "all-paths-reverted"
            else:
                reason = "error"
            verdicts[sig] = ("ERROR", reason)
        return verdicts
    # hevm prints "[RUNNING] sig" followed by "[PASS] name" / "[FAIL] name" and warnings
    blocks = re.split(r"(?=^\[RUNNING\])", text, flags=re.M)
    for b in blocks:
        m = re.match(r"^\[RUNNING\]\s+(\w+\([^)]*\))", b)
        if not m:
            continue
        sig = m.group(1)
        r = re.search(r"^\s*\[(PASS|FAIL|ERROR)\]\s+%s\b" % re.escape(fname(sig)), b, re.M)
        if not r:
            continue
        v = r.group(1)
        partial = "only able to partially explore" in b
        if v == "FAIL" and not re.search(r"(?i)counterexample", b):
            reason = "all-branches-reverted" if "all branches reverted" in b else \
                     ("partial-exploration" if partial else "no-counterexample")
            verdicts[sig] = ("ERROR", reason)
        elif v == "ERROR":
            verdicts[sig] = ("ERROR", "error")
        else:
            verdicts[sig] = (v, "partial-exploration" if partial else "")
    return verdicts


def memory_cap_mb():
    v = MEMORY_MAX.strip().upper()
    return float(v[:-1]) * {"G": 1024, "M": 1}[v[-1]] if v[-1] in "GM" else float(v) / 2**20


def classify_run(test, verdicts, status, log_text="", peak_rss_mb=0.0):
    if "Internal Error" in log_text and test not in verdicts:
        # hevm aborts the whole process (and every test still running in it)
        return "ERROR", "tool-crash"
    if test in verdicts:
        return verdicts[test]
    if status == "timeout":
        return "TIMEOUT", "timeout"
    if status == "oom" or (float(peak_rss_mb or 0) >= 0.95 * memory_cap_mb()
                           and "executor has been shutdown" in log_text):
        # the solver processes were killed by the memory limit of the run
        return "OOM", "memory-limit"
    return "ERROR", "no-verdict"


def reparse():
    """Recomputes verdicts of results/pertest.csv from the stored logs."""
    path = RESULTS / "pertest.csv"
    new_fields = ["timestamp", "tool", "subject", "test", "verdict", "reason", "shared", "status", "wall_s",
                  "user_s", "sys_s", "peak_rss_mb", "returncode", "log"]
    old_fields = [f for f in new_fields if f != "reason"]
    raw = list(csv.reader(open(path)))[1:]
    # rows appended by a runner started before the "reason" column existed have one field less
    rows = [dict(zip(new_fields if len(x) == len(new_fields) else old_fields, x)) for x in raw]
    for r in rows:
        text = (ROOT / r["log"]).read_text(errors="replace")
        r["verdict"], r["reason"] = classify_run(r["test"], parse_verdicts(r["tool"], text), r["status"], text,
                                                 r.get("peak_rss_mb", 0))
        r.setdefault("shared", "1")
    fields = ["timestamp", "tool", "subject", "test", "verdict", "reason", "shared", "status", "wall_s",
              "user_s", "sys_s", "peak_rss_mb", "returncode", "log"]
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)  # atomic: a concurrent reader never sees a partial file


def name_regex(tool, names):
    alt = "|".join(sorted(set(names)))
    return f"^({alt})\\(" if tool == "halmos" else f"^({alt})$"


# ------------------------------------------------------------------------ phases

def phase_pertest(subjects, tools, timeout_override, only=None):
    out_csv = RESULTS / "pertest.csv"
    fields = ["timestamp", "tool", "subject", "test", "verdict", "reason", "shared", "status", "wall_s",
              "user_s", "sys_s", "peak_rss_mb", "returncode", "log"]
    done = set()
    if out_csv.exists():
        with open(out_csv) as f:
            done = {(r["tool"], r["subject"], r["test"]) for r in csv.DictReader(f)}
    new = not out_csv.exists()
    with open(out_csv, "a", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        if new:
            wr.writeheader()
        for subject in subjects:
            std = subject.split("_")[0]
            timeout = timeout_override or DEFAULT_TIMEOUT[std]
            for tool in tools:
                w = workdir(subject, tool)
                logs = RESULTS / "logs" / "pertest" / f"{subject}_{tool}"
                logs.mkdir(parents=True, exist_ok=True)
                sigs = test_names(subject, tool)
                for name in sorted({fname(t) for t in sigs}):
                    if only and not re.search(only, name):
                        continue
                    group = [t for t in sigs if fname(t) == name]
                    if all((tool, subject, t) in done for t in group):
                        continue
                    log = logs / f"{name}.log"
                    m = measured_run(tool_cmd(tool, w, match=name_regex(tool, [name])), w, timeout, log)
                    text = log.read_text(errors="replace")
                    verdicts = parse_verdicts(tool, text)
                    for test in group:
                        verdict, reason = classify_run(test, verdicts, m["status"], text, m["peak_rss_mb"])
                        row = {"timestamp": datetime.now().isoformat(timespec="seconds"), "tool": tool,
                               "subject": subject, "test": test, "verdict": verdict, "reason": reason, "shared": len(group),
                               "log": str(log.relative_to(ROOT)), **m}
                        wr.writerow(row)
                        f.flush()
                        print(f"[pertest] {tool:6} {subject:20} {test:70} {verdict:8} {m['wall_s']:>9.2f}s "
                              f"{m['peak_rss_mb']:>8.0f}MB", flush=True)


def finished_tests(subject, tool):
    """Tests whose process terminated in the pertest phase (any verdict except
    timeout / out of memory / tool crash). Inconclusive verdicts (ERROR) are
    kept: they are part of the real cost of running the suite. A tool crash is
    excluded because it aborts every other test running in the same process."""
    rows = list(csv.DictReader(open(RESULTS / "pertest.csv")))
    return sorted(r["test"] for r in rows if r["tool"] == tool and r["subject"] == subject
                  and r["verdict"] not in ("TIMEOUT", "OOM") and r.get("reason") != "tool-crash")


def phase_suite(subjects, tools, runs):
    out_csv = RESULTS / "suite.csv"
    fields = ["timestamp", "tool", "subject", "run", "n_tests", "n_censored", "status",
              "wall_s", "user_s", "sys_s", "peak_rss_mb", "returncode", "log"]
    done = set()
    if out_csv.exists():
        with open(out_csv) as f:
            done = {(r["tool"], r["subject"], r["run"]) for r in csv.DictReader(f)}
    new = not out_csv.exists()
    # interleave tools and subjects across runs so that time-dependent noise
    # (thermal state, background load) does not favour one treatment
    plan = [(run, subject, tool) for run in range(1, runs + 1) for subject in subjects for tool in tools]
    with open(out_csv, "a", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        if new:
            wr.writeheader()
        for run, subject, tool in plan:
            if (tool, subject, str(run)) in done:
                continue
            w = workdir(subject, tool)
            all_tests = test_names(subject, tool)
            ok = finished_tests(subject, tool)
            if not ok:
                continue
            match = None
            if len(ok) < len(all_tests):
                bad = {fname(t) for t in all_tests if t not in ok}
                ok = [t for t in ok if fname(t) not in bad]
                match = name_regex(tool, [fname(t) for t in ok])
            logs = RESULTS / "logs" / "suite" / f"{subject}_{tool}"
            logs.mkdir(parents=True, exist_ok=True)
            log = logs / f"run{run:02d}.log"
            timeout = sum(float(r["wall_s"]) for r in csv.DictReader(open(RESULTS / "pertest.csv"))
                                          if r["tool"] == tool and r["subject"] == subject and r["test"] in ok) * 3 + 600
            m = measured_run(tool_cmd(tool, w, match=match), w, timeout, log)
            row = {"timestamp": datetime.now().isoformat(timespec="seconds"), "tool": tool,
                   "subject": subject, "run": run, "n_tests": len(ok),
                   "n_censored": len(all_tests) - len(ok), "log": str(log.relative_to(ROOT)), **m}
            wr.writerow(row)
            f.flush()
            print(f"[suite] run {run:2} {tool:6} {subject:20} {m['status']:8} {m['wall_s']:>9.2f}s "
                  f"{m['peak_rss_mb']:>8.0f}MB", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["pertest", "suite", "reparse"])
    ap.add_argument("--subjects", nargs="+", default=SUBJECTS)
    ap.add_argument("--tools", nargs="+", default=list(TOOL_NAMES))
    ap.add_argument("--timeout", type=int, default=None)
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--only", default=None, help="pertest: run only the test cases whose name matches this regex")
    ap.add_argument("--out", default="results", help="results directory (relative to the repository)")
    ap.add_argument("--halmos-args", default="", help="extra Halmos options, e.g. '--loop 4'")
    ap.add_argument("--hevm-args", default="", help="extra Hevm options, e.g. '--max-iterations 20'")
    a = ap.parse_args()
    global RESULTS
    RESULTS = ROOT / a.out
    EXTRA_ARGS["halmos"] = a.halmos_args.split()
    if "--solver" not in EXTRA_ARGS["halmos"]:
        # Halmos defaults to Yices since 0.3; the experiment uses Z3, the solver of Hevm
        EXTRA_ARGS["halmos"] = ["--solver", os.environ.get("HALMOS_SOLVER", "z3")] + EXTRA_ARGS["halmos"]
    EXTRA_ARGS["hevm"] = a.hevm_args.split()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "options.txt").write_text(f"halmos: {' '.join(EXTRA_ARGS['halmos'])}\nhevm: {' '.join(EXTRA_ARGS['hevm'])}\n")
    if a.phase == "reparse":
        reparse()
    elif a.phase == "pertest":
        phase_pertest(a.subjects, a.tools, a.timeout, a.only)
    else:
        phase_suite(a.subjects, a.tools, a.runs)


if __name__ == "__main__":
    main()
