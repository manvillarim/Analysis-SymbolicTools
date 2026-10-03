#!/usr/bin/env -S bash -c 'exec "$(dirname "$0")/.tools/venv/bin/python" "$0" "$@"'
"""Classifies every failing verdict, combining the concrete confirmation
(results/confirmation.csv) with the manual analysis of the replay traces
(results/triage.csv). The manual analysis is encoded in RULES below, one entry
per property, with the justification that goes into the paper.

outcome   bug  the counterexample is real (the concrete replay violates the property)
          fp   the counterexample does not reproduce concretely
          inc  a failure was reported without a usable counterexample (counted as inconclusive)
category  (only for bug)
          normative       the implementation violates a MUST of the EIP
          suite-property  the implementation violates a property required by
                          the test suite but not by the EIP (e.g. zero-address checks)
          test-defect     the property itself is wrong: it fails for a correct
                          implementation (the counterexample exposes the test)

Writes results/classification.csv.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"

# (standard, regex on the test name) -> (category, justification)
RULES = [
    # ERC-20: EIP-20 does not require reverts on the zero address; mint/burn are not part of EIP-20
    ("ERC20", r"^proveFail_(Approve\w*Zero\w*|ApproveZeroAddressForMSGSender|MintToZeroAddress|"
              r"Transfer\w*ZeroAddress\w*|TransferFromToZeroAddress33)$",
     "suite-property", "EIP-20 does not require transfer/transferFrom/approve to revert on the zero address"),
    # ERC-721
    ("ERC721", r"^prove_safeTransferFrom$", "test-defect",
     "the receiver mock declares onERC721Received() without parameters, so every safe transfer to it reverts"),
    ("ERC721", r"^proveFail_setApprovalForAll$", "test-defect",
     "EIP-721 allows any account to call setApprovalForAll for itself; the property expects a revert"),
    ("ERC721", r"^proveFail_ApproveWhenIsNotApprovedForAll$", "test-defect",
     "the setup calls setApprovalForAll from address(0) without constraining it; a correct rejection fails the test"),
    # ERC-1155
    ("ERC1155", r"^proveFail_safeTransferFromWhenSenderIsNotMSGSender$", "test-defect",
     "msg.sender is not constrained to differ from the token holder; with a symbolic caller (Hevm) "
     "the holder itself performs a valid transfer"),
    ("ERC1155", r"^proveFail_burnZeroAddress$", "suite-property",
     "burning is not part of the EIP-1155 interface; the zero-address check is a suite requirement"),
    ("ERC1155", r"^proveFail_setApprovalForAllSenderEqualsOperator$", "suite-property",
     "EIP-1155 does not require setApprovalForAll to revert for operator == address(0)"),
    # ERC-4626 (vault share token is an ERC-20)
    ("ERC4626", r"^proveFail_(approve\w*zero\w*|transfer\w*zero\w*|mint_to_zero\w*|burn_from_zero\w*)$",
     "suite-property", "EIP-20/EIP-4626 do not require a revert on the zero address"),
    ("ERC4626", r"^proveFail_(withdraw|redeem|mint|deposit)With\w+$", "test-defect",
     "EIP-4626 does not require a revert in this situation; the call is valid and succeeds in both implementations"),
]


# Underlying defect of each suite-property violation: (function, role of the zero address)
DEFECTS = {
    "ERC20": {
        "proveFail_ApproveFromZeroAddress": ("approve", "caller"),
        "proveFail_ApproveZeroAddressForMSGSender": ("approve", "caller"),
        "proveFail_ApproveToZeroAddress": ("approve", "spender"),
        "proveFail_ApproveZeroAddress": ("approve", "spender"),
        "proveFail_TransferToZeroAddress": ("transfer", "recipient"),
        "proveFail_TransferZeroAmountToZeroAddressReverts": ("transfer", "recipient"),
        "proveFail_TransferFromToZeroAddress33": ("transferFrom", "recipient"),
        "proveFail_TransferFromZeroAmountToZeroAddressReverts": ("transferFrom", "recipient"),
        "proveFail_TransferFromZeroAddressForMSGSender": ("transferFrom", "caller"),
        "proveFail_MintToZeroAddress": ("mint", "recipient"),
    },
    "ERC1155": {
        "proveFail_burnZeroAddress": ("burn", "holder"),
        "proveFail_setApprovalForAllSenderEqualsOperator": ("setApprovalForAll", "operator"),
    },
    "ERC4626": {
        "proveFail_approvefrom_zero_address_reverts": ("approve", "caller"),
        "proveFail_approvezero_address_reverts": ("approve", "spender"),
        "proveFail_transfer_from_zero_address_reverts": ("transfer", "caller"),
        "proveFail_transfer_to_zero_address_reverts": ("transfer", "recipient"),
        "proveFail_transferFrom_from_zero_address_reverts": ("transferFrom", "owner"),
        "proveFail_transferFrom_to_zero_address_reverts": ("transferFrom", "recipient"),
        "proveFail_mint_to_zero_address_reverts": ("mint", "recipient"),
        "proveFail_burn_from_zero_address_reverts": ("burn", "holder"),
    },
}


def defect_for(subject, test):
    f = DEFECTS.get(subject.split("_")[0], {}).get(test.split("(")[0])
    return f"{f[0]}: zero address as {f[1]}" if f else ""


def rule_for(subject, test):
    std = subject.split("_")[0]
    name = test.split("(")[0]
    for s, rx, cat, why in RULES:
        if s == std and re.match(rx, name):
            return cat, why
    return "unclassified", ""


def main():
    pertest = list(csv.DictReader(open(RES / "pertest.csv")))
    conf = {}
    for r in csv.DictReader(open(RES / "confirmation.csv")):
        conf.setdefault((r["tool"], r["subject"], r["test"]), []).append(r["classification"])
    triage = {(r["tool"], r["subject"], r["test"]): r for r in csv.DictReader(open(RES / "triage.csv"))} \
        if (RES / "triage.csv").exists() else {}
    out = []
    for r in pertest:
        if r["verdict"] != "FAIL":
            continue
        key = (r["tool"], r["subject"], r["test"])
        replays = conf.get(key, [])
        if "confirmed" in replays:
            outcome = "bug"
            category, why = rule_for(r["subject"], r["test"])
        elif replays and all(x == "refuted" for x in replays):
            outcome, category, why = "fp", "", "counterexample does not reproduce concretely"
        elif r["tool"] == "hevm" and re.search(r"Counterexample:\s*\[error attempting to reproduce",
                                               re.sub(r"\x1b\[[0-9;]*m", "", (ROOT / r["log"]).read_text(errors="replace"))):
            outcome, category, why = "inc", "", "the tool reported a failure but could not build a counterexample"
        else:
            outcome, category, why = "review", "", "replay inconclusive: " + ",".join(replays)
        t = triage.get(key, {})
        out.append({"tool": r["tool"], "subject": r["subject"], "test": r["test"], "outcome": outcome,
                    "category": category, "justification": why,
                    "defect": defect_for(r["subject"], r["test"]) if category == "suite-property" else "",
                    "evidence": f"{t.get('last_call', '')} -> {t.get('last_call_outcome', '')}".strip(" ->")})
    with open(RES / "classification.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        if o["outcome"] != "bug" or o["category"] == "unclassified":
            print(f"needs attention: {o['tool']} {o['subject']} {o['test']} {o['outcome']} {o['category']}")
    print(f"{len(out)} failing verdicts classified")


if __name__ == "__main__":
    main()
