#!/usr/bin/env -S bash -c 'exec "$(dirname "$0")/.tools/venv/bin/python" "$0" "$@"'
"""Concrete confirmation of the counterexamples reported by Halmos and Hevm.

For every FAIL in results/pertest.csv, the counterexample(s) are parsed from the
tool log, encoded as calldata and replayed with `forge test` against the same
concrete subject contract, calling the property function from the default
Foundry sender (the caller used by both symbolic tools). The replay outcome is
classified as:

  confirmed   the concrete run violates the property in the same way
              (assertion failure for prove_ tests and Halmos-style proveFail_
              tests; successful execution for Hevm proveFail_ tests)
  refuted     the concrete run satisfies the property
  other       the concrete run reverts for a different reason (manual review)

Writes results/confirmation.csv and the generated replay tests under
results/confirm/.
"""
import csv
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|[⠀-⣿] Parsing [^\n\[]*")
FOUNDRY_CALLER = "0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38"
TOOL_NAMES = {"halmos": "Halmos", "hevm": "Hevm"}


def abi_inputs(workdir, contract, sig):
    art = json.loads((workdir / "out" / f"{contract}.t.sol" / f"{contract}.json").read_text())
    for item in art["abi"]:
        if item.get("type") == "function":
            s = f"{item['name']}({','.join(i['type'] for i in item['inputs'])})"
            if s == sig:
                return item["inputs"]
    raise KeyError(sig)


def unwrap_hex(text):
    """Joins hexadecimal values that the terminal renderer wrapped over lines."""
    lines, out = text.split("\n"), []
    for line in lines:
        if out and re.search(r"0x[0-9a-fA-F]+$", out[-1].rstrip()) and re.fullmatch(r"\s*[0-9a-fA-F]+\s*", line):
            out[-1] = out[-1].rstrip() + line.strip()
        else:
            out.append(line)
    return "\n".join(out)


def halmos_cexs(log, inputs):
    """List of {param: value} parsed from Halmos counterexample blocks."""
    text = unwrap_hex(ANSI.sub("", log))
    out = []
    for block in re.split(r"Counterexample:", text)[1:]:
        vals = {}
        for m in re.finditer(r"\bp_(\w+?)_([a-z0-9\[\]]+)_[0-9a-f]+_\d+\s*=\s*(0x[0-9a-fA-F]+)", block):
            vals[m.group(1)] = m.group(3)
        if vals or not inputs:
            out.append(vals)
    return out


def hevm_cexs(log, inputs):
    """List of {param: value} parsed from Hevm 'calldata: f(a,b,...)' lines."""
    text = ANSI.sub("", log)
    out = []
    for m in re.finditer(r"calldata:\s+\w+\((.*)\)\s*$", text, re.M):
        args = split_args(m.group(1))
        if len(args) == len(inputs):
            out.append({i["name"]: a for i, a in zip(inputs, args)})
    return out


def split_args(s):
    args, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        args.append(cur.strip())
    return args


def sol_literal(typ, value):
    if value is None:
        value = "0"
    if typ == "address":
        v = int(value, 16) if str(value).startswith("0x") else int(value)
        return f"address(uint160({v}))"
    if typ == "bool":
        if str(value).lower() in ("true", "false"):
            return str(value).lower()
        return "true" if int(value, 16 if str(value).startswith("0x") else 10) else "false"
    if typ.startswith("uint") or typ.startswith("int"):
        v = int(value, 16) if str(value).startswith("0x") else int(value)
        return f"{typ}({v})" if typ.startswith("uint") else f"{typ}(int256({v}))"
    raise ValueError(f"unsupported type {typ}")


def replay_contract(subject_contract, tool, cases):
    fns = []
    for k, (sig, inputs, cex) in enumerate(cases):
        if any(i["type"].endswith("]") or i["type"] in ("bytes", "string") for i in inputs):
            fns.append(f"    function test_cex_{k}() public {{ console2.log(\"OUTCOME\", {k}, \"unsupported\"); }}")
            continue
        args = ", ".join(sol_literal(i["type"], cex.get(i["name"])) for i in inputs)
        enc = f'abi.encodeWithSignature("{sig}"{", " if args else ""}{args})'
        fns.append(f"""    function test_cex_{k}() public {{
        vm.prank({FOUNDRY_CALLER});
        (bool ok, bytes memory ret) = address(this).call({enc});
        if (ok) console2.log("OUTCOME", {k}, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", {k}, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", {k}, string.concat("revert:", vm.toString(ret)));
    }}""")
    return (f"""// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/{tool}/subjects/{subject_contract}.t.sol";

contract Confirm_{subject_contract} is {subject_contract} {{
    function _slice(bytes memory b) internal pure returns (bytes memory r) {{
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }}

""" + "\n\n".join(fns) + "\n}\n")


def classify(tool, sig, outcome):
    name = sig.split("(")[0]
    if outcome == "unsupported":
        return "other"
    if name.startswith("proveFail") and tool == "hevm":
        return "confirmed" if outcome == "success" else "refuted"
    if outcome == "panic:1":
        return "confirmed"
    if outcome == "success":
        return "refuted"
    return "other"


def main():
    rows = list(csv.DictReader(open(RES / "pertest.csv")))
    fails = [r for r in rows if r["verdict"] == "FAIL"]
    groups = {}
    for r in fails:
        groups.setdefault((r["tool"], r["subject"]), []).append(r)
    results = []
    (RES / "confirm").mkdir(exist_ok=True)
    for (tool, subject), rs in sorted(groups.items()):
        contract = f"{subject}_{TOOL_NAMES[tool]}"
        w = ROOT / "repro" / "work" / f"{subject}_{tool}"
        cases = []
        hevm_tags = {}
        for r in rs:
            inputs = abi_inputs(w, contract, r["test"])
            log = (ROOT / r["log"]).read_text(errors="replace")
            cexs = (halmos_cexs if tool == "halmos" else hevm_cexs)(log, inputs)
            if tool == "hevm":
                tags = re.findall(r"Counterexample:\s*\[([a-z ]+)\]", ANSI.sub("", log))
                hevm_tags[r["test"]] = "validated" if "validated" in tags else (tags[0] if tags else "")
            if not cexs:
                results.append({"tool": tool, "subject": subject, "test": r["test"], "cex": "",
                                "outcome": "no counterexample in log", "classification": "other"})
            for c in cexs:
                cases.append((r["test"], inputs, c))
        if not cases:
            continue
        src = replay_contract(contract, tool, cases)
        # separate project, so that the replay contract never reaches the symbolic runs
        cw = ROOT / "repro" / "work" / f"confirm_{subject}_{tool}"
        if cw.exists():
            shutil.rmtree(cw)
        shutil.copytree(w / "test", cw / "test")
        shutil.copy(w / "foundry.toml", cw / "foundry.toml")
        os.symlink(ROOT / "lib", cw / "lib")
        os.symlink(ROOT / "src", cw / "src")
        (cw / "test" / "confirm").mkdir(exist_ok=True)
        (cw / "test" / "confirm" / f"Confirm_{contract}.t.sol").write_text(src)
        (RES / "confirm" / f"Confirm_{contract}.t.sol").write_text(src)
        p = subprocess.run(["forge", "test", "--root", str(cw), "--match-contract", f"^Confirm_{contract}$",
                            "-vv"], capture_output=True, text=True)
        (RES / "confirm" / f"Confirm_{contract}.log").write_text(p.stdout + p.stderr)
        outcomes = {int(m.group(1)): m.group(2).strip()
                    for m in re.finditer(r"OUTCOME (\d+) (.+)", ANSI.sub("", p.stdout))}
        for k, (sig, _, cex) in enumerate(cases):
            out = outcomes.get(k, "not executed")
            cls = classify(tool, sig, out)
            if tool == "hevm":
                # Hevm treats msg.sender as symbolic and does not print the caller it
                # chose, so a replay from the Foundry sender is not always faithful.
                # Hevm replays every counterexample concretely itself and tags it as
                # [validated] or [not reproducible]; that tag is the confirmation used.
                tag = hevm_tags.get(sig, "")
                out = f"hevm:{tag}; foundry-replay:{out}"
                cls = "confirmed" if tag == "validated" else ("refuted" if tag == "not reproducible" else cls)
            results.append({"tool": tool, "subject": subject, "test": sig,
                            "cex": json.dumps(cex), "outcome": out, "classification": cls})
            print(f"{tool:6} {subject:20} {sig:70} {out[:60]:60} {cls}")
    with open(RES / "confirmation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tool", "subject", "test", "cex", "outcome", "classification"])
        w.writeheader()
        w.writerows(results)


if __name__ == "__main__":
    main()
