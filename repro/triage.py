#!/usr/bin/env -S bash -c 'exec "$(dirname "$0")/.tools/venv/bin/python" "$0" "$@"'
"""Locates, for every confirmed counterexample, the call that led to the
assertion failure, using the Foundry execution trace of the concrete replay.

For each replay it reports the last external call made to the contract under
test before the assertion failed and whether that call reverted (and why) or
returned. This is the evidence used for the manual classification in
results/classification.csv.

Writes results/triage.csv.
"""
import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|[⠀-⣿] Parsing [^\n\[]*")
SUBJECT_PREFIX = ("OpenZeppelinERC", "SolmateERC")


def last_subject_call(trace):
    """Returns (call, outcome) of the last top-level call to the subject."""
    lines = trace.splitlines()
    best = None
    for i, line in enumerate(lines):
        m = re.match(r"^([\s│]*)[├└]─ \[\d+\] ((?:%s)\w*)::(\w+\(.*\))\s*$" % "|".join(SUBJECT_PREFIX), line)
        if not m:
            continue
        indent = len(m.group(1))
        outcome = "?"
        for nxt in lines[i + 1:]:
            r = re.match(r"^([\s│]*)└─ ← \[(\w+)\]\s*(.*)$", nxt)
            if r and len(r.group(1)) == indent + 4:
                outcome = f"{r.group(2)} {r.group(3)}".strip()
                break
        best = (f"{m.group(2)}::{m.group(3)}", outcome)
    return best or ("", "")


def main():
    rows = [r for r in csv.DictReader(open(RES / "confirmation.csv")) if r["classification"] == "confirmed"]
    seen = {}
    out = []
    for r in rows:
        key = (r["tool"], r["subject"], r["test"])
        if key in seen:
            continue
        seen[key] = True
        contract = f"{r['subject']}_{'Halmos' if r['tool'] == 'halmos' else 'Hevm'}"
        cw = ROOT / "repro" / "work" / f"confirm_{r['subject']}_{r['tool']}"
        src = (cw / "test" / "confirm" / f"Confirm_{contract}.t.sol").read_text()
        # index of the first replay of this test
        k = next(int(m.group(1)) for m in re.finditer(r"function test_cex_(\d+)\(\) public \{\s*(?:vm\.prank\([^)]*\);\s*)?"
                                                     r"\(bool ok, bytes memory ret\) = address\(this\)\.call\("
                                                     r"abi\.encodeWithSignature\(\"([^\"]+)\"", src)
                 if m.group(2) == r["test"])
        p = subprocess.run(["forge", "test", "--root", str(cw), "--match-test", f"test_cex_{k}\\(", "-vvvv"], capture_output=True, text=True)
        trace = ANSI.sub("", p.stdout)
        call, outcome = last_subject_call(trace)
        out.append({"tool": r["tool"], "subject": r["subject"], "test": r["test"],
                    "last_call": call, "last_call_outcome": outcome})
        print(f"{r['tool']:6} {r['subject']:20} {r['test'][:60]:60} {call[:70]:70} {outcome}")
    with open(RES / "triage.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
