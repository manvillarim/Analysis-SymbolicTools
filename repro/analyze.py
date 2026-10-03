#!/usr/bin/env -S bash -c 'exec "$(dirname "$0")/.tools/venv/bin/python" "$0" "$@"'
"""Builds every table and figure of the paper from results/*.csv.

Outputs (results/tables/):
  verdicts.csv / verdicts.tex      RQ1: Pass/Bugs/FP/FN/Inc per tool and subject
  time_suite.csv / time_*.tex      RQ2: suite execution time (real/user/sys), all subjects
  memory.csv / memory.tex          RQ2: peak memory per tool and subject
  stats.csv / stats.tex            RQ2: Welch t-test, Mann-Whitney U, Vargha-Delaney A12
  accuracy.csv / accuracy.tex      RQ3: accuracy per subject, FP/FN/Inc rates, overall P
  pertest_time.csv                 per test case time and memory (supplementary)
  reliability_scores.pdf           overall reliability figure
"""
import csv
import re
import math
import statistics as st
from collections import defaultdict
from pathlib import Path

from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
OUT = RES / "tables"

STANDARDS = ["ERC20", "ERC721", "ERC1155", "ERC4626"]
IMPLS = ["OpenZeppelin", "Solmate"]
SUBJECTS = [f"{s}_{i}" for s in STANDARDS for i in IMPLS]
TOOLS = ["halmos", "hevm"]
TOOL_LABEL = {"halmos": "Halmos", "hevm": "Hevm"}
STD_LABEL = {"ERC20": "ERC-20", "ERC721": "ERC-721", "ERC1155": "ERC-1155", "ERC4626": "ERC-4626"}
INCONCLUSIVE = {"TIMEOUT", "OOM", "ERROR"}


def read(name):
    p = RES / name
    return list(csv.DictReader(open(p))) if p.exists() else []


def label(subject):
    s, i = subject.split("_")
    return f"{STD_LABEL[s]} {i}"


def fmt_time(sec):
    if sec is None or (isinstance(sec, float) and math.isnan(sec)):
        return "--"
    if sec < 60:
        return f"{sec:.2f}s"
    m, s = divmod(sec, 60)
    return f"{int(m)}m{s:04.1f}s"


def ci95(xs):
    n = len(xs)
    if n < 2:
        return (float("nan"), float("nan"))
    m, sd = st.mean(xs), st.stdev(xs)
    h = stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
    return (m - h, m + h)


def a12(x, y):
    """Vargha-Delaney A12: probability that a value from x is larger than one from y."""
    gt = sum(1 for a in x for b in y if a > b)
    eq = sum(1 for a in x for b in y if a == b)
    return (gt + 0.5 * eq) / (len(x) * len(y))


def a12_magnitude(a):
    d = abs(a - 0.5)
    return "negligible" if d < 0.06 else "small" if d < 0.14 else "medium" if d < 0.21 else "large"


def write_csv(name, rows):
    if not rows:
        return
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def write_tex(name, header, rows, caption, label_, colspec=None):
    colspec = colspec or "l" + "c" * (len(header) - 1)
    lines = [r"\begin{table}[htb]", r"\centering", r"\begin{scriptsize}",
             rf"\begin{{tabular}}{{{colspec}}}", r"\toprule",
             " & ".join(rf"\textbf{{{h}}}" for h in header) + r" \\", r"\midrule"]
    lines += [" & ".join(str(c) for c in r) + r" \\" for r in rows]
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{scriptsize}",
              rf"\caption{{{caption}}}", rf"\label{{{label_}}}", r"\end{table}", ""]
    (OUT / name).write_text("\n".join(lines))


# ------------------------------------------------------------------ RQ1 / RQ3

def verdict_tables(pertest, classification):
    """classification.csv: tool, subject, test, outcome in {bug, fp}, category, note."""
    cls = {(r["tool"], r["subject"], r["test"]): r for r in classification}
    rows, acc_rows = [], []
    for subject in SUBJECTS:
        for tool in TOOLS:
            rs = [r for r in pertest if r["tool"] == tool and r["subject"] == subject]
            if not rs:
                continue
            n = len(rs)
            passed = sum(r["verdict"] == "PASS" for r in rs)
            inc = sum(r["verdict"] in INCONCLUSIVE for r in rs) + \
                sum(r["verdict"] == "FAIL" and cls.get((tool, subject, r["test"]), {}).get("outcome") == "inc"
                    for r in rs)
            fails = [r for r in rs if r["verdict"] == "FAIL"]
            bugs = sum(cls.get((tool, subject, r["test"]), {}).get("outcome") == "bug" for r in fails)
            fp = sum(cls.get((tool, subject, r["test"]), {}).get("outcome") == "fp" for r in fails)
            unclassified = len(fails) - bugs - fp - sum(
                cls.get((tool, subject, r["test"]), {}).get("outcome") == "inc" for r in fails)
            # false negative: the test case passed on this tool while the other tool
            # found a confirmed violation of a property of the contract (normative or
            # suite property) in the same test case. Test cases are matched by name,
            # since a few of them have different parameters in the two suites. A
            # confirmed failure of a defective test case is not a defect of the
            # contract, so passing it does not count as a false negative.
            other = [t for t in TOOLS if t != tool][0]
            missed = {k[2].split("(")[0] for k, c in cls.items()
                      if k[0] == other and k[1] == subject and c.get("outcome") == "bug"
                      and c.get("category") in ("normative", "suite-property")}
            by_name = defaultdict(list)
            for r in rs:
                by_name[r["test"].split("(")[0]].append(r["verdict"])
            fn = sum(1 for name, vs in by_name.items() if name in missed and all(v == "PASS" for v in vs))
            rows.append({"subject": subject, "tool": tool, "tests": n, "pass": passed, "bugs": bugs,
                         "fp": fp, "fn": fn, "inc": inc, "unclassified": unclassified,
                         "timeout": sum(r["verdict"] == "TIMEOUT" for r in rs),
                         "oom": sum(r["verdict"] == "OOM" for r in rs),
                         "error": sum(r["verdict"] == "ERROR" for r in rs)})
            acc = 1 - (fp + fn + inc) / n
            acc_rows.append({"subject": subject, "tool": tool, "n": n, "accuracy": acc,
                             "fp_rate": round(fp / n, 4), "fn_rate": round(fn / n, 4),
                             "inc_rate": round(inc / n, 4)})
    write_csv("verdicts.csv", rows)
    write_csv("accuracy.csv", acc_rows)

    for std in STANDARDS:
        body = []
        for tool in TOOLS:
            for impl in IMPLS:
                r = next((x for x in rows if x["subject"] == f"{std}_{impl}" and x["tool"] == tool), None)
                if r:
                    body.append([rf"\textbf{{{TOOL_LABEL[tool]}}}" if impl == "OpenZeppelin" else "", impl,
                                 r["pass"], r["bugs"], r["fp"], r["fn"], r["inc"]])
        if body:
            write_tex(f"verdicts_{std}.tex", ["Tool", "Impl.", "Pass", "Bugs", "FP", "FN", "Inc"], body,
                      f"{STD_LABEL[std]} test results (Pass/Bugs/FP/FN/Inc) for OpenZeppelin and Solmate implementations.",
                      f"tab:test_results_{std.lower()}", "llccccc")

    # accuracy tables, one per implementation
    overall = {}
    for impl in IMPLS:
        body = []
        for tool in TOOLS:
            cells = []
            for std in STANDARDS:
                r = next((x for x in acc_rows if x["subject"] == f"{std}_{impl}" and x["tool"] == tool), None)
                cells.append(f"{100 * r['accuracy']:.1f}\\%" if r else "--")
            body.append([TOOL_LABEL[tool]] + cells)
        write_tex(f"accuracy_{impl}.tex", ["Tool"] + [STD_LABEL[s] for s in STANDARDS], body,
                  f"Accuracy for the {impl} contracts.", f"tab:tool_accuracy_{impl.lower()}")
    for tool in TOOLS:
        all_ = [r["accuracy"] for r in acc_rows if r["tool"] == tool]
        no4626 = [r["accuracy"] for r in acc_rows if r["tool"] == tool and not r["subject"].startswith("ERC4626")]
        overall[tool] = {"P_all": st.mean(all_) if all_ else float("nan"),
                         "P_without_ERC4626": st.mean(no4626) if no4626 else float("nan"),
                         "n_subjects": len(all_)}
    write_csv("reliability.csv", [{"tool": t, **{k: round(v, 4) if isinstance(v, float) else v
                                                 for k, v in d.items()}} for t, d in overall.items()])
    return rows, acc_rows, overall


# ------------------------------------------------------------------------ RQ2

def time_tables(suite, pertest):
    by = defaultdict(list)
    for r in suite:
        if r["status"] == "exited":
            by[(r["tool"], r["subject"])].append(r)
    rows = []
    for subject in SUBJECTS:
        for tool in TOOLS:
            rs = by.get((tool, subject), [])
            if not rs:
                continue
            real = [float(r["wall_s"]) for r in rs]
            user = [float(r["user_s"]) for r in rs]
            sys_ = [float(r["sys_s"]) for r in rs]
            mem = [float(r["peak_rss_mb"]) for r in rs]
            lo, hi = ci95(real)
            rows.append({"subject": subject, "tool": tool, "runs": len(rs),
                         "n_tests": rs[0]["n_tests"], "n_censored": rs[0]["n_censored"],
                         "real_mean_s": round(st.mean(real), 3),
                         "real_sd_s": round(st.stdev(real), 3) if len(real) > 1 else 0,
                         "real_median_s": round(st.median(real), 3),
                         "real_ci95_lo_s": round(lo, 3), "real_ci95_hi_s": round(hi, 3),
                         "real_cv": round(st.stdev(real) / st.mean(real), 4) if len(real) > 1 else 0,
                         "user_mean_s": round(st.mean(user), 3),
                         "user_sd_s": round(st.stdev(user), 3) if len(user) > 1 else 0,
                         "sys_mean_s": round(st.mean(sys_), 3),
                         "sys_sd_s": round(st.stdev(sys_), 3) if len(sys_) > 1 else 0,
                         "mem_mean_mb": round(st.mean(mem), 1), "mem_max_mb": round(max(mem), 1),
                         "mem_sd_mb": round(st.stdev(mem), 1) if len(mem) > 1 else 0})
    write_csv("time_suite.csv", rows)

    body = []
    for subject in SUBJECTS:
        cells = [label(subject)]
        for tool in TOOLS:
            r = next((x for x in rows if x["subject"] == subject and x["tool"] == tool), None)
            if r:
                cens = f"$^{{\\dagger{r['n_censored']}}}$" if int(r["n_censored"]) else ""
                cells += [f"{fmt_time(r['real_mean_s'])} ($\\pm${fmt_time(r['real_sd_s'])}){cens}",
                          fmt_time(r["user_mean_s"]), fmt_time(r["sys_mean_s"])]
            else:
                cells += ["--", "--", "--"]
        body.append(cells)
    write_tex("time_suite.tex",
              ["Subject", "Halmos Real", "Halmos User", "Halmos Sys", "Hevm Real", "Hevm User", "Hevm Sys"],
              body, "Average suite execution time over 10 runs (mean $\\pm$ standard deviation). "
              "$\\dagger n$: $n$ test cases excluded because they did not terminate (timeout, out of memory or tool crash).",
              "tab:time_all", "lcccccc")

    body = []
    for subject in SUBJECTS:
        cells = [label(subject)]
        for tool in TOOLS:
            r = next((x for x in rows if x["subject"] == subject and x["tool"] == tool), None)
            cells += [f"{r['mem_mean_mb']:.0f}" if r else "--", f"{r['mem_max_mb']:.0f}" if r else "--"]
        # max over per-test runs, which includes the test cases that hit the limit
        for tool in TOOLS:
            pt = [float(x["peak_rss_mb"]) for x in pertest if x["tool"] == tool and x["subject"] == subject]
            cells.append(f"{max(pt):.0f}" if pt else "--")
        body.append(cells)
    write_tex("memory.tex",
              ["Subject", "Halmos mean", "Halmos max", "Hevm mean", "Hevm max",
               "Halmos max/test", "Hevm max/test"], body,
              "Peak resident memory (MB) of the tool process tree, including solver processes. "
              "Suite: mean and maximum over 10 runs; per test: maximum over all test cases.",
              "tab:memory", "lcccccc")
    write_csv("memory.csv", [{k: r[k] for k in ("subject", "tool", "mem_mean_mb", "mem_max_mb")} for r in rows])
    return rows, by


def stats_tables(by):
    rows = []
    for subject in SUBJECTS:
        h = [float(r["wall_s"]) for r in by.get(("halmos", subject), [])]
        v = [float(r["wall_s"]) for r in by.get(("hevm", subject), [])]
        if len(h) < 2 or len(v) < 2:
            continue
        hn = by[("halmos", subject)][0]["n_tests"]
        vn = by[("hevm", subject)][0]["n_tests"]
        t = stats.ttest_ind(v, h, equal_var=False)
        # exact test unless a value occurs in both samples (the exact distribution assumes no ties)
        method = "asymptotic" if set(v) & set(h) else "exact"
        u = stats.mannwhitneyu(v, h, alternative="two-sided", method=method)
        sh_h, sh_v = stats.shapiro(h), stats.shapiro(v)
        lev = stats.levene(h, v)
        a = a12(v, h)
        rows.append({"subject": subject, "same_test_set": hn == vn, "n_halmos": len(h), "n_hevm": len(v),
                     "welch_t": round(t.statistic, 3), "welch_df": round(t.df, 2), "welch_p": t.pvalue,
                     "mw_U": u.statistic, "mw_p": u.pvalue, "mw_method": method, "A12_hevm_slower": round(a, 3),
                     "A12_magnitude": a12_magnitude(a),
                     "shapiro_p_halmos": round(sh_h.pvalue, 4), "shapiro_p_hevm": round(sh_v.pvalue, 4),
                     "levene_p": round(lev.pvalue, 4)})
    write_csv("stats.csv", rows)
    body = [[label(r["subject"]) + ("" if r["same_test_set"] else "$^{*}$"),
             f"{r['welch_t']:.1f}", f"{r['welch_df']:.1f}", f"{r['welch_p']:.1e}",
             f"{r['mw_U']:.0f}", f"{r['mw_p']:.1e}", f"{r['A12_hevm_slower']:.2f} ({r['A12_magnitude']})"]
            for r in rows]
    write_tex("stats.tex", ["Subject", "$t$", "df", "$p$ (Welch)", "$U$", "$p$ (M-W)", "$\\hat{A}_{12}$"], body,
              "Welch's two-sample $t$-test and Mann-Whitney $U$ test on the real execution time of the suite "
              "(10 runs per tool), with the Vargha-Delaney $\\hat{A}_{12}$ effect size (probability that a Hevm run "
              "is slower than a Halmos run). $^{*}$: the tools ran different test sets because of censored test cases.",
              "tab:stats", "lcccccc")
    return rows


def pertest_table(pertest):
    rows = [{k: r[k] for k in ("tool", "subject", "test", "verdict", "wall_s", "user_s", "sys_s", "peak_rss_mb")}
            for r in pertest]
    write_csv("pertest_time.csv", rows)


ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|[⠀-⣿] Parsing [^\n\[]*")


def effective_verdict(r):
    """Verdict as defined in the paper: PASS, FAIL or INC. A failure reported
    without a usable counterexample is inconclusive (same rule as classify.py)."""
    if r["verdict"] in INCONCLUSIVE:
        return "INC"
    if r["verdict"] == "FAIL" and r["tool"] == "hevm":
        log = ANSI.sub("", (ROOT / r["log"]).read_text(errors="replace"))
        if re.search(r"Counterexample:\s*\[error attempting to reproduce", log) and "[validated]" not in log:
            return "INC"
    return r["verdict"]


def sensitivity_table(pertest):
    """Verdict changes between the default configuration and larger bounds."""
    sens = read("sensitivity/pertest.csv")
    if not sens:
        return
    base = {(r["tool"], r["subject"], r["test"]): effective_verdict(r) for r in pertest}
    for r in sens:
        r["verdict"] = effective_verdict(r)
    norm = lambda v: v
    rows, body = [], []
    for subject in SUBJECTS:
        cells = [label(subject)]
        for tool in TOOLS:
            rs = [r for r in sens if r["tool"] == tool and r["subject"] == subject]
            if not rs:
                cells += ["--", "--", "--"]
                continue
            inc0 = sum(norm(base[(tool, subject, r["test"])]) == "INC" for r in rs)
            inc1 = sum(norm(r["verdict"]) == "INC" for r in rs)
            to_pass = sum(norm(base[(tool, subject, r["test"])]) == "INC" and r["verdict"] == "PASS" for r in rs)
            new_fail = sum(norm(base[(tool, subject, r["test"])]) != "FAIL" and r["verdict"] == "FAIL" for r in rs)
            lost_fail = sum(base[(tool, subject, r["test"])] == "FAIL" and r["verdict"] != "FAIL" for r in rs)
            rows.append({"subject": subject, "tool": tool, "inc_default": inc0, "inc_sensitivity": inc1,
                         "inc_to_pass": to_pass, "new_fail": new_fail, "fail_lost": lost_fail})
            cells += [f"{inc0} $\\rightarrow$ {inc1}", to_pass, new_fail]
        body.append(cells)
    write_csv("sensitivity.csv", rows)
    write_tex("sensitivity.tex",
              ["Subject", "Halmos Inc", "Halmos Inc$\\rightarrow$Pass", "Halmos new Fail",
               "Hevm Inc", "Hevm Inc$\\rightarrow$Pass", "Hevm new Fail"], body,
              "Sensitivity of the verdicts to the exploration bounds: inconclusive test cases with the default "
              "configuration $\\rightarrow$ with larger bounds (Halmos: \\texttt{--loop 4 --solver-timeout-assertion 600s}; "
              "Hevm: \\texttt{--max-iterations 20 --smt-timeout 600}), inconclusive cases that became Pass, and "
              "new failures.", "tab:sensitivity", "lcccccc")


def figure(overall):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3))
    tools = [TOOL_LABEL[t] for t in TOOLS]
    with4626 = [overall[t]["P_all"] for t in TOOLS]
    without = [overall[t]["P_without_ERC4626"] for t in TOOLS]
    x = range(len(tools))
    b1 = ax.bar([i - 0.2 for i in x], without, 0.4, label="ERC-20/721/1155", color="#4C72B0")
    b2 = ax.bar([i + 0.2 for i in x], with4626, 0.4, label="all subjects (ERC-4626 included)", color="#DD8452")
    for bars in (b1, b2):
        for b in bars:
            ax.annotate(f"{b.get_height():.2f}", (b.get_x() + b.get_width() / 2, b.get_height()),
                        ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(x), tools)
    ax.set_ylim(0, 1.25)
    ax.set_ylabel("Reliability score $P$")
    ax.legend(fontsize=8, loc="upper center", ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "reliability_scores.pdf")
    fig.savefig(ROOT / "reliability_scores.pdf")  # the figure included by the paper


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pertest = read("pertest.csv")
    suite = read("suite.csv")
    classification = read("classification.csv")
    verdict_rows, acc_rows, overall = verdict_tables(pertest, classification)
    time_rows, by = time_tables(suite, pertest)
    stat_rows = stats_tables(by)
    pertest_table(pertest)
    sensitivity_table(pertest)
    paper_tables(verdict_rows, acc_rows, overall, time_rows, stat_rows)
    layout_tables(verdict_rows, acc_rows, overall, time_rows, stat_rows)
    figure(overall)
    for t, d in overall.items():
        print(f"{TOOL_LABEL[t]}: P = {d['P_all']:.3f} (all {d['n_subjects']} subjects), "
              f"{d['P_without_ERC4626']:.3f} without ERC-4626")
    print(f"tables written to {OUT.relative_to(ROOT)}")



# ------------------------------------------------------------- paper tables
# Final LaTeX tables, in the exact form used in the paper (results/tables/paper/).

IMPL_SHORT = {"OpenZeppelin": "OpenZeppelin", "Solmate": "Solmate"}


def _table(name, colspec, head, body, caption, label_):
    lines = [r"\begin{table}[htbp]", r"\centering", r"\begin{scriptsize}",
             rf"\begin{{tabular}}{{{colspec}}}", r"\toprule"] + head + [r"\midrule"] + body + \
            [r"\bottomrule", r"\end{tabular}", r"\end{scriptsize}",
             rf"\caption{{{caption}}}", rf"\label{{{label_}}}", r"\end{table}", ""]
    (OUT / "paper").mkdir(exist_ok=True)
    (OUT / "paper" / name).write_text("\n".join(lines))


def _sci(p):
    m, e = f"{p:.1e}".split("e")
    return f"${m}\\times10^{{{int(e)}}}$"


def _rows_by_standard(make_cells):
    body = []
    for k, std in enumerate(STANDARDS):
        if k:
            body.append(r"\addlinespace")
        for j, impl in enumerate(IMPLS):
            body.append(" & ".join([STD_LABEL[std] if j == 0 else "", impl] +
                                   [str(c) for c in make_cells(f"{std}_{impl}")]) + r" \\")
    return body


def paper_tables(verdict_rows, acc_rows, overall, time_rows, stat_rows):
    V = {(r["subject"], r["tool"]): r for r in verdict_rows}
    cols = ("pass", "bugs", "fp", "fn", "inc")
    _table("test_results.tex", "llrrrrrrrrrr",
           [r" & & \multicolumn{5}{c}{\textbf{Halmos}} & \multicolumn{5}{c}{\textbf{Hevm}} \\",
            r"\cmidrule(lr){3-7}\cmidrule(lr){8-12}",
            r"\textbf{Standard} & \textbf{Impl.} & Pass & Viol. & FP & FN & Inc & Pass & Viol. & FP & FN & Inc \\"],
           _rows_by_standard(lambda s: [V[(s, t)][c] for t in TOOLS for c in cols]),
           "Verdicts per tool and subject (61 ERC-20, 14 ERC-721, 14 ERC-1155 and 46 ERC-4626 test cases). "
           "Viol.: confirmed property violations; FP: false positives; FN: false negatives (test cases that "
           "passed while the other tool found a confirmed violation, also counted in Pass); Inc: inconclusive verdicts.",
           "tab:test_results")

    A = {(r["subject"], r["tool"]): r for r in acc_rows}
    body = _rows_by_standard(lambda s: [f"{100 * A[(s, t)]['accuracy']:.1f}\\%" for t in TOOLS])
    body += [r"\midrule",
             rf"\multicolumn{{2}}{{l}}{{Reliability $P$ (all subjects)}} & {overall['halmos']['P_all']:.2f} & {overall['hevm']['P_all']:.2f} \\",
             rf"\multicolumn{{2}}{{l}}{{Reliability $P$ (without ERC-4626)}} & {overall['halmos']['P_without_ERC4626']:.2f} & {overall['hevm']['P_without_ERC4626']:.2f} \\"]
    _table("accuracy.tex", "llrr",
           [r"\textbf{Standard} & \textbf{Impl.} & \textbf{Halmos} & \textbf{Hevm} \\"], body,
           "Accuracy per subject and overall reliability score $P$ (mean accuracy).", "tab:accuracy")

    T = {(r["subject"], r["tool"]): r for r in time_rows}

    def tcells(s):
        out = []
        for t in TOOLS:
            r = T[(s, t)]
            dag = f"$^{{\\dagger}}$" if int(r["n_censored"]) else ""
            out += [f"{r['real_mean_s']:.2f} $\\pm$ {r['real_sd_s']:.2f}{dag}", f"{r['user_mean_s']:.2f}", f"{r['sys_mean_s']:.2f}"]
        return out
    _table("time.tex", "llrrrrrr",
           [r" & & \multicolumn{3}{c}{\textbf{Halmos}} & \multicolumn{3}{c}{\textbf{Hevm}} \\",
            r"\cmidrule(lr){3-5}\cmidrule(lr){6-8}",
            r"\textbf{Standard} & \textbf{Impl.} & Real & User & Sys & Real & User & Sys \\"],
           _rows_by_standard(tcells),
           "Execution time of the complete suite in seconds: mean over 10 runs (real time: mean $\\pm$ standard "
           "deviation). $^{\\dagger}$: one test case excluded because it did not terminate (timeout, memory limit or tool crash).",
           "tab:time_all")

    def mcells(s):
        out = [f"{T[(s, t)]['mem_mean_mb'] / 1024:.2f}" for t in TOOLS]
        return out
    _table("memory.tex", "llrr",
           [r"\textbf{Standard} & \textbf{Impl.} & \textbf{Halmos} & \textbf{Hevm} \\"],
           _rows_by_standard(mcells),
           "Peak resident memory (GB) of the tool process tree, including solver processes, during the complete "
           "suite: mean over 10 runs (the standard deviation is at most 0.1\\,GB).", "tab:memory")

    S = {r["subject"]: r for r in stat_rows}

    def scells(s):
        if s not in S:
            return ["--"] * 6
        r = S[s]
        return [f"{r['welch_t']:.1f}", f"{r['welch_df']:.1f}", _sci(r["welch_p"]), f"{r['mw_U']:.0f}",
                _sci(r["mw_p"]), f"{r['A12_hevm_slower']:.2f}"]
    _table("stats.tex", "llrrrrrr",
           [r"\textbf{Standard} & \textbf{Impl.} & $t$ & df & $p$ (Welch) & $U$ & $p$ (M-W) & $\hat{A}_{12}$ \\"],
           _rows_by_standard(scells),
           "Welch's two-sample $t$-test and Mann-Whitney $U$ test on the real execution time of the complete suite "
           "(10 runs per tool), and Vargha-Delaney effect size $\\hat{A}_{12}$ (probability that a Hevm run is "
           "slower than a Halmos run).", "tab:stats")

    sens = {(r["subject"], r["tool"]): r for r in csv.DictReader(open(OUT / "sensitivity.csv"))} \
        if (OUT / "sensitivity.csv").exists() else {}
    if sens:
        def secells(s):
            out = []
            for t in TOOLS:
                r = sens[(s, t)]
                out += [f"{r['inc_default']} $\\rightarrow$ {r['inc_sensitivity']}", r["inc_to_pass"], r["new_fail"]]
            return out
        _table("sensitivity.tex", "llrrrrrr",
               [r" & & \multicolumn{3}{c}{\textbf{Halmos}} & \multicolumn{3}{c}{\textbf{Hevm}} \\",
                r"\cmidrule(lr){3-5}\cmidrule(lr){6-8}",
                r"\textbf{Standard} & \textbf{Impl.} & Inc & Inc$\rightarrow$Pass & New fail & Inc & Inc$\rightarrow$Pass & New fail \\"],
               _rows_by_standard(secells),
               "Inconclusive verdicts reported with the default configuration $\\rightarrow$ with larger exploration "
               "bounds (Halmos: \\texttt{--loop 4 --solver-timeout-assertion 600s}; Hevm: \\texttt{--max-iterations 20 "
               "--smt-timeout 600}), inconclusive verdicts that became Pass, and new failures. Inconclusive verdicts as defined in Section~\\ref{sec:methodology}.", "tab:sensitivity")

    # one row per underlying defect of the suite-property violations
    allcls = read("classification.csv")
    sp = [r for r in allcls if r["outcome"] == "bug" and r["category"] == "suite-property"]
    verdict_by_name = defaultdict(list)
    for r in read("pertest.csv"):
        verdict_by_name[(r["tool"], r["subject"], r["test"].split("(")[0])].append(effective_verdict(r))
    confirmed = {(r["tool"], r["subject"], r["test"].split("(")[0]) for r in sp}
    defects = defaultdict(set)
    for r in sp:
        defects[(r["subject"], r.get("defect", ""))].add(r["test"].split("(")[0])

    def cell(tool, subject, names):
        out = []
        for n in sorted(names):
            if (tool, subject, n) in confirmed:
                out.append("Viol.")
            else:
                vs = verdict_by_name.get((tool, subject, n), ["--"])
                out.append("Inc" if "INC" in vs else ("Pass" if all(v == "PASS" for v in vs) else vs[0].title()))
        return ", ".join(out)
    body = []
    for (subject, defect), names in sorted(defects.items(), key=lambda x: (SUBJECTS.index(x[0][0]), x[0][1])):
        fn, role = defect.split(": ", 1) if ": " in defect else (defect, "")
        tests = ", ".join(rf"\tn{{{n}}}" for n in sorted(names))
        body.append(f"{label(subject)} & \\texttt{{{fn}}} & {role.replace('zero address as ', '')} & {tests} & "
                    f"{cell('halmos', subject, names)} & {cell('hevm', subject, names)} \\\\")
    if body:
        _table("suite_violations.tex",
               r"@{}l l l >{\raggedright\arraybackslash}p{0.34\textwidth} l l@{}",
               [r"\textbf{Subject} & \textbf{Function} & \textbf{Zero address as} & \textbf{Test cases} & \textbf{Halmos} & \textbf{Hevm} \\"],
               body,
               "Defects behind the suite-property violations: one row per function and role of the zero address, "
               "with the test cases that expose it and the verdict of each tool on each of them (Viol.: confirmed "
               "violation; every confirmed violation was replayed concretely).", "tab:suite_violations")

    cls = [r for r in allcls if r["outcome"] == "bug"]
    cnt = defaultdict(int)
    for r in cls:
        cnt[(r["subject"], r["tool"], r["category"])] += 1
    cats = ["normative", "suite-property", "test-defect"]
    body = _rows_by_standard(lambda s: [cnt[(s, t, c)] for c in cats for t in TOOLS])
    distinct = {c: len({(r["subject"], r["test"]) for r in cls if r["category"] == c}) for c in cats}
    body += [r"\midrule",
             rf"\multicolumn{{2}}{{l}}{{Distinct (both tools)}} & \multicolumn{{2}}{{c}}{{{distinct['normative']}}} & "
             rf"\multicolumn{{2}}{{c}}{{{distinct['suite-property']}}} & \multicolumn{{2}}{{c}}{{{distinct['test-defect']}}} \\"]
    _table("classification.tex", "llrrrrrr",
           [r" & & \multicolumn{2}{c}{\textbf{Normative EIP}} & \multicolumn{2}{c}{\textbf{Suite property}} & \multicolumn{2}{c}{\textbf{Test defect}} \\",
            r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}",
            r"\textbf{Standard} & \textbf{Impl.} & Halmos & Hevm & Halmos & Hevm & Halmos & Hevm \\"], body,
           "Classification of the confirmed property violations. Normative EIP: violation of a MUST requirement of "
           "the standard; suite property: required by the test suite but not by the EIP (all are zero-address checks); "
           "test defect: the property fails for a correct implementation. Distinct: number of different "
           "(subject, test case) pairs.", "tab:classification")



# ------------------------------------------------- tables in the layout of the paper
IMPL_ABBR = {"OpenZeppelin": "OZ", "Solmate": "SM"}
ABBR_NOTE = "OZ: OpenZeppelin; SM: Solmate."


def _float(colspec, head, body, caption, label_, tabcolsep=None):
    lines = [r"\begin{table}[!htbp]", r"\centering", r"\footnotesize"]
    if tabcolsep:
        lines.append(rf"\setlength{{\tabcolsep}}{{{tabcolsep}}}")
    lines += [rf"\begin{{tabular}}{{{colspec}}}", r"\toprule", head, r"\midrule"] + body + \
             [r"\bottomrule", r"\end{tabular}", rf"\caption{{{caption}}}", rf"\label{{{label_}}}", r"\end{table}", ""]
    return "\n".join(lines)


def _rows(cells_of, subjects=SUBJECTS):
    out = []
    for std in STANDARDS:
        for j, impl in enumerate(IMPLS):
            s = f"{std}_{impl}"
            if s not in subjects:
                continue
            first = STD_LABEL[std] if j == 0 else ""
            out.append(f"{first:<8} & {IMPL_ABBR[impl]} & " + " & ".join(str(c) for c in cells_of(s)) + r" \\")
    return out


def _stacked(ncols, cells_of):
    body = []
    for k, tool in enumerate(TOOLS):
        if k:
            body.append(r"\midrule")
        body.append(rf"\multicolumn{{{ncols}}}{{@{{}}l}}{{\textit{{{TOOL_LABEL[tool]}}}}} \\")
        body += _rows(lambda s: cells_of(tool, s))
    return body


def layout_tables(verdict_rows, acc_rows, overall, time_rows, stat_rows):
    P = OUT / "paper_layout"
    P.mkdir(exist_ok=True)
    V = {(r["subject"], r["tool"]): r for r in verdict_rows}
    (P / "test_results.tex").write_text(_float(
        "@{}llrrrrr@{}",
        r"\textbf{Standard} & \textbf{Impl.} & \textbf{Pass} & \textbf{Viol.} & \textbf{FP} & \textbf{FN} & \textbf{Inc} \\",
        _stacked(7, lambda t, s: [V[(s, t)][c] for c in ("pass", "bugs", "fp", "fn", "inc")]),
        "Verdicts per tool and subject (65 ERC-20, 14 ERC-721, 14 ERC-1155 and 46 ERC-4626 test cases). "
        + ABBR_NOTE + " Viol.: confirmed property violations; FP: false positives; FN: false negatives (test cases "
        "that passed while the other tool found a confirmed violation of a property of the contract, also counted in "
        "Pass); Inc: inconclusive verdicts.", "tab:test_results", "4.5pt"))

    A = {(r["subject"], r["tool"]): r["accuracy"] for r in acc_rows}
    body = _rows(lambda s: [f"{100 * A[(s, t)]:.1f}\\%" for t in TOOLS])
    body += [r"\midrule",
             rf"\multicolumn{{2}}{{@{{}}l}}{{$P$ (all subjects)}}      & {overall['halmos']['P_all']:.2f} & {overall['hevm']['P_all']:.2f} \\",
             rf"\multicolumn{{2}}{{@{{}}l}}{{$P$ (without ERC-4626)}}  & {overall['halmos']['P_without_ERC4626']:.2f} & {overall['hevm']['P_without_ERC4626']:.2f} \\"]
    (P / "accuracy.tex").write_text(_float(
        "@{}llrr@{}", r"\textbf{Standard} & \textbf{Impl.} & \textbf{Halmos} & \textbf{Hevm} \\", body,
        "Accuracy per subject and overall reliability score $P$ (mean accuracy). " + ABBR_NOTE, "tab:accuracy"))

    T = {(r["subject"], r["tool"]): r for r in time_rows}

    def tc(t, s):
        if (s, t) not in T:
            return ["--"] * 3
        r = T[(s, t)]
        dag = r"$^{\dagger}$" if int(r["n_censored"]) else ""
        return [f"{r['real_mean_s']:.2f} $\\pm$ {r['real_sd_s']:.2f}{dag}", f"{r['user_mean_s']:.2f}", f"{r['sys_mean_s']:.2f}"]
    (P / "time.tex").write_text(_float(
        "@{}llrrr@{}", r"\textbf{Standard} & \textbf{Impl.} & \textbf{Real} & \textbf{User} & \textbf{Sys} \\",
        _stacked(5, tc),
        "Execution time of the complete suite in seconds: mean over 10 runs (real time: mean $\\pm$ standard "
        "deviation). " + ABBR_NOTE + " $^{\\dagger}$: test cases that did not terminate in the per-test runs "
        "(timeout, memory limit or tool crash) are excluded.", "tab:time_all", "4.5pt"))

    sd = max(r["mem_sd_mb"] for r in time_rows) / 1024
    (P / "memory.tex").write_text(_float(
        "@{}llrr@{}", r"\textbf{Standard} & \textbf{Impl.} & \textbf{Halmos} & \textbf{Hevm} \\",
        _rows(lambda s: [f"{T[(s, t)]['mem_mean_mb'] / 1024:.2f}" if (s, t) in T else "--" for t in TOOLS]),
        "Peak resident memory (GB) of the tool process tree, including solver processes, during the complete "
        f"suite: mean over 10 runs (the standard deviation is at most {sd:.2f}\\,GB). " + ABBR_NOTE, "tab:memory"))

    S = {r["subject"]: r for r in stat_rows}

    def sci(p):
        m, e = f"{p:.1e}".split("e")
        return f"${m}{{\\cdot}}10^{{{int(e)}}}$"
    (P / "stats.tex").write_text(_float(
        "@{}llrrrrrr@{}",
        r"\textbf{Std.} & \textbf{Impl.} & $t$ & df & $p_{\mathrm{W}}$ & $U$ & $p_{\mathrm{MW}}$ & $\hat{A}_{12}$ \\",
        _rows(lambda s: ["--"] * 6 if s not in S else [f"{S[s]['welch_t']:.1f}" if S[s]['welch_t'] >= 0 else f"${S[s]['welch_t']:.1f}$",
                         f"{S[s]['welch_df']:.1f}", sci(S[s]["welch_p"]), f"{S[s]['mw_U']:.0f}", sci(S[s]["mw_p"]),
                         f"{S[s]['A12_hevm_slower']:.2f}"]),
        "Welch's two-sample $t$-test ($p_{\\mathrm{W}}$) and exact Mann-Whitney $U$ test ($p_{\\mathrm{MW}}$) on "
        "the real execution time of the complete suite (10 runs per tool), and Vargha-Delaney effect size "
        "$\\hat{A}_{12}$ (probability that a Hevm run is slower than a Halmos run). " + ABBR_NOTE, "tab:stats", "3pt"))

    sens = {(r["subject"], r["tool"]): r for r in read("tables/sensitivity.csv")} if (OUT / "sensitivity.csv").exists() else {}
    if sens:
        (P / "sensitivity.tex").write_text(_float(
            "@{}llccc@{}",
            r"\textbf{Standard} & \textbf{Impl.} & \textbf{Inc} & \textbf{Inc$\rightarrow$Pass} & \textbf{New fail} \\",
            _stacked(5, lambda t, s: [f"{sens[(s, t)]['inc_default']} $\\rightarrow$ {sens[(s, t)]['inc_sensitivity']}",
                                      sens[(s, t)]["inc_to_pass"], sens[(s, t)]["new_fail"]]),
            "Inconclusive verdicts with the default configuration $\\rightarrow$ with larger exploration bounds, "
            "inconclusive verdicts that became Pass, and new failures. Larger bounds: Halmos \\texttt{--loop 4 "
            "--solver-timeout-assertion 600s}; Hevm \\texttt{--max-iterations 20 --smt-timeout 600}. Inconclusive "
            "verdicts as defined in Section~\\ref{sec:methodology}. " + ABBR_NOTE, "tab:sensitivity", "4.5pt"))

    cls = [r for r in read("classification.csv") if r["outcome"] == "bug"]
    cnt = defaultdict(int)
    for r in cls:
        cnt[(r["subject"], r["tool"], r["category"])] += 1
    cats = ["normative", "suite-property", "test-defect"]
    distinct = {c: len({(r["subject"], r["test"].split("(")[0]) for r in cls if r["category"] == c}) for c in cats}
    body = _stacked(5, lambda t, s: [cnt[(s, t, c)] for c in cats])
    body += [r"\midrule", rf"\multicolumn{{2}}{{@{{}}l}}{{Distinct (both tools)}} & {distinct['normative']} & "
                          rf"{distinct['suite-property']} & {distinct['test-defect']} \\"]
    (P / "classification.tex").write_text(_float(
        "@{}llrrr@{}", r"\textbf{Standard} & \textbf{Impl.} & \textbf{Normative} & \textbf{Suite} & \textbf{Defect} \\",
        body,
        "Classification of the confirmed property violations. Normative: violation of a MUST requirement of the "
        "EIP; Suite: property required by the test suite but not by the EIP (all are zero-address checks); Defect: "
        "the property fails for a correct implementation. Distinct: number of different (subject, test case) "
        "pairs. " + ABBR_NOTE, "tab:classification", "5pt"))

    src = (OUT / "paper" / "suite_violations.tex").read_text()
    body = [l.replace("ERC-20 Solmate", "ERC-20").replace("ERC-1155 Solmate", "ERC-1155").replace("ERC-4626 Solmate", "ERC-4626")
            for l in src.split("\\midrule", 1)[1].split("\\bottomrule")[0].strip().splitlines()]
    (P / "suite_violations.tex").write_text("\n".join([
        r"\begin{table}[!htbp]", r"\centering", r"\footnotesize", r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabularx}{\columnwidth}{@{}lll>{\raggedright\arraybackslash}Xll@{}}", r"\toprule",
        r"\textbf{Std.} & \textbf{Function} & \textbf{Zero addr.} & \textbf{Test cases} & \textbf{Halmos} & \textbf{Hevm} \\",
        r"\midrule"] + body + [r"\bottomrule", r"\end{tabularx}",
        r"\caption{The 16 defects of Solmate behind the 20 suite-property violations: function, role of the zero "
        r"address, test cases that expose the defect and verdict of each tool on each test case (Viol.: confirmed "
        r"violation, replayed concretely). The ERC-4626 rows concern the vault share token, which inherits the "
        r"Solmate ERC-20.}", r"\label{tab:suite_violations}", r"\end{table}", ""]))


if __name__ == "__main__":
    main()
