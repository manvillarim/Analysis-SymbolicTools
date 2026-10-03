# Symbolic Testing of ERC Standard Smart Contracts

This repository contains the artifacts of the work *"An Empirical Evaluation of Symbolic Testing Tools for ERC Standard Smart Contracts"*, which compares the symbolic testing tools [Halmos](https://github.com/a16z/halmos) and [Hevm](https://github.com/argotorg/hevm) on the OpenZeppelin and Solmate implementations of ERC-20, ERC-721, ERC-1155 and ERC-4626.

---

## Authors

Manoel Felipe Araújo Villarim[0009-0005-6045-4519] - mfav@cin.ufpe.br

Alexandre Cabral Mota[0000-0003-4416-8123] - acm@cin.ufpe.br

Juliano Manabu Iyoda[0000-0001-7137-8287] - jmi@cin.ufpe.br

Márcio Lopes Cornélio[0000-0002-9801-4659] - mlc2@cin.ufpe.br

---

## Structure

```
.
├── lib/                          # Contracts under test and test library, fetched by repro/setup.sh
│   ├── openzeppelin-contracts/   #   OpenZeppelin Contracts, release v5.7.0
│   ├── solmate/                  #   Solmate, commit 89365b8
│   └── forge-std/                #   forge-std, release v1.17.0
├── src/mocks/
│   ├── Mocks.sol                 # Thin wrappers exposing the internal mint/burn of each subject;
│   │                             #   the token logic is the unmodified upstream code
│   └── Interfaces.sol            # Common external API of the subjects, used by the test suites
├── test/
│   ├── halmos/                   # Property suites for Halmos (try/catch style), one per standard,
│   │   │                         #   written as abstract contracts over the common interface
│   │   └── subjects/             #   One concrete test contract per implementation
│   └── hevm/                     # The same suites for Hevm (proveFail style)
│       └── subjects/
├── repro/                        # Reproduction package
│   ├── versions.env              #   Pinned versions of tools, solver and subjects
│   ├── setup.sh                  #   Installs Halmos and Hevm locally and fetches the subjects
│   ├── env.sh                    #   Records the hardware and software environment
│   ├── run.py                    #   Runs the tools (per test case and complete suite)
│   ├── confirm.py                #   Replays every counterexample concretely with forge
│   ├── triage.py                 #   Locates, in the replay trace, the call that violated the property
│   ├── classify.py               #   Classifies every confirmed violation, with its justification
│   ├── analyze.py                #   Builds every table and figure from the raw measurements
│   └── run_all.sh                #   Complete pipeline
├── results/                      # Raw measurements and generated tables (see "Results")
├── tables/                       # Helper scripts of a preliminary, manual analysis; not used by
│                                 #   the pipeline and not needed to reproduce the results
├── reliability_scores.pdf        # Reliability figure (copy of results/tables/reliability_scores.pdf)
└── foundry.toml                  # solc 0.8.30, EVM version cancun, optimizer disabled
```

---

## Subjects and Test Suites

The test suites are adapted from the property suites of [Lindy Labs](https://github.com/lindy-labs/solidity_properties). Each suite is written once and instantiated by one concrete test contract per implementation, so the same test bodies run against OpenZeppelin and Solmate.

| Standard | Test cases | Halmos contracts | Hevm contracts |
|----------|-----------:|------------------|----------------|
| ERC-20   | 65 | `ERC20_OpenZeppelin_Halmos`, `ERC20_Solmate_Halmos` | `ERC20_OpenZeppelin_Hevm`, `ERC20_Solmate_Hevm` |
| ERC-721  | 14 | `ERC721_OpenZeppelin_Halmos`, `ERC721_Solmate_Halmos` | `ERC721_OpenZeppelin_Hevm`, `ERC721_Solmate_Hevm` |
| ERC-1155 | 14 | `ERC1155_OpenZeppelin_Halmos`, `ERC1155_Solmate_Halmos` | `ERC1155_OpenZeppelin_Hevm`, `ERC1155_Solmate_Hevm` |
| ERC-4626 | 46 | `ERC4626_OpenZeppelin_Halmos`, `ERC4626_Solmate_Halmos` | `ERC4626_OpenZeppelin_Hevm`, `ERC4626_Solmate_Hevm` |

Halmos does not support the `proveFail` convention, so its suites wrap the operation that must revert in `try ... { assert(false); } catch { assert(true); }`; the Hevm suites call it directly in a `proveFail_` test. Two semantic differences between the tools remain and matter when the verdicts are compared:

- Halmos fixes `msg.sender` to the default Foundry sender, whereas Hevm treats it as a symbolic value.
- A Hevm `proveFail_` test passes as soon as every path reverts, including reverts raised by the set-up calls of the test.

---

## Requirements

1. Linux with a systemd user session. Every tool run is confined to a memory limit through `systemd-run --user --scope`, so that a run that exhausts memory is recorded instead of disturbing the machine.
2. [Foundry](https://getfoundry.sh/) — `forge` on the `PATH`. Developed against forge 1.7.1; `forge` downloads solc 0.8.30 itself.
3. [uv](https://docs.astral.sh/uv/) and Python ≥ 3.11 (developed with 3.14), used to install Halmos in an isolated environment.
4. `z3` on the `PATH`, used by Hevm. Developed against Z3 4.12.6.
5. `git` and `curl`.

`repro/setup.sh` installs **Halmos 0.3.3** (with SciPy and Matplotlib for the analysis) in `repro/.tools/venv` and downloads the static **Hevm 0.58.0** binary to `repro/.tools/bin`; nothing is installed globally. Neither `git submodule update` nor `forge install` is needed.

Both tools are run with **Z3**. Halmos uses Yices by default since version 0.3, so the pipeline passes `--solver z3` (set by `HALMOS_SOLVER` in `repro/versions.env`); Halmos with its default solver is measured separately as supplementary data.

The measurements were taken on an Intel Core i5-12450H (12 threads) with 16 GB of RAM running Fedora Linux 44. Every run is limited to 10 GB of memory (`MEMORY_MAX`). For comparable timings, close memory-intensive applications and keep the machine from suspending during the runs, e.g. by running the pipeline under `systemd-inhibit --what=sleep:idle:handle-lid-switch`.

---

## Reproduction

All commands are run from the **repository root**.

### 1. Install the tools and fetch the subjects

```bash
./repro/setup.sh
```

The script is idempotent. It checks out the pinned versions of `lib/openzeppelin-contracts`, `lib/solmate` and `lib/forge-std` and writes the environment to `results/environment.txt`.

### 2. Run the complete pipeline

```bash
./repro/run_all.sh
```

Every step is **resumable**: measurements already stored in `results/` are skipped, so an interrupted run continues where it stopped. The steps are:

| Step | Command | What it does | Time* |
|------|---------|--------------|------:|
| 1 | `repro/run.py pertest` | Runs every test case in its own process, recording verdict, real/user/sys time and peak memory of the process tree (tool and solvers). Limits: 30 min per test case (10 min for ERC-4626) and 10 GB | ~2 h |
| 2 | `repro/confirm.py`, `repro/triage.py`, `repro/classify.py` | Replays every counterexample concretely with `forge test`, locates the violating call in the trace and classifies each confirmed violation as *normative* (violates a MUST of the EIP), *suite property* (required by the suite but not by the EIP) or *test defect* (the property fails for a correct implementation) | ~10 min |
| 3 | `repro/run.py suite --runs 10` | Runs the complete suite of each subject in a single process, 10 times per tool, interleaving tools and subjects. Test cases that did not terminate in step 1 are excluded and reported as censored | ~14 h |
| 4 | `repro/run.py pertest --out results/sensitivity ...` | Repeats step 1 with larger exploration bounds: Halmos `--loop 4 --solver-timeout-assertion 600s`, Hevm `--max-iterations 20 --smt-timeout 600` | ~4 h |
| 5 | `repro/run.py ... --out results/halmos_yices` | Supplementary: Halmos with its default solver (Yices) | ~1 h |
| 6 | `repro/analyze.py` | Builds every table and figure | seconds |

\* On the machine described above; Hevm accounts for most of the time.

### 3. Run a single tool or subject

Each phase accepts `--tools` (`halmos`, `hevm`) and `--subjects` (`<Standard>_<Implementation>`, e.g. `ERC20_Solmate`):

```bash
./repro/run.py pertest --tools halmos --subjects ERC20_OpenZeppelin ERC20_Solmate
./repro/run.py suite   --tools hevm   --subjects ERC721_OpenZeppelin --runs 10
```

The tools can also be invoked directly on a subject. Each `(subject, tool)` pair gets its own Foundry project under `repro/work/`, created by `run.py` and containing only the suite and one concrete test contract, because the `--match` option of Hevm selects test functions but not contracts:

```bash
repro/.tools/bin/halmos --root repro/work/ERC20_Solmate_halmos --function prove --solver z3
repro/.tools/bin/hevm test --root repro/work/ERC20_Solmate_hevm
```

### 4. Regenerate the tables only

```bash
./repro/analyze.py
```

`analyze.py` reads only the CSV files in `results/`, so it reproduces every table and figure from the stored measurements without running any tool.

---

## Results

```
results/
├── environment.txt        # Hardware, OS and exact versions of tools, solver and subjects
├── pertest.csv            # One row per (tool, subject, test case): verdict, reason for an
│                          #   inconclusive verdict, real/user/sys time, peak memory, log path
├── suite.csv              # One row per execution of a complete suite (16 pairs x 10 runs)
├── confirmation.csv       # Concrete replay of every counterexample and its outcome
├── triage.csv             # Call that violated the property in each replay
├── classification.csv     # Category, justification and underlying defect of every confirmed violation
├── confirm/               # Generated replay tests and their forge output
├── logs/                  # Raw output of every tool run (evidence for every verdict)
├── sensitivity/           # Step 4, same layout as pertest.csv
├── halmos_yices/          # Step 5: Halmos with Yices, same layout as pertest.csv and suite.csv
└── tables/
    ├── paper_layout/      # The LaTeX tables exactly as they appear in the paper
    ├── paper/             # The same tables in a compact two-tool layout
    ├── *.csv              # The same data in CSV
    └── reliability_scores.pdf
```

A verdict is **PASS**, **FAIL** (a counterexample was reported) or **inconclusive**: the run timed out, exceeded the memory limit, crashed, explored the test only partially, reported that every path reverted, or reported a failure without a usable counterexample. The reason is recorded in the `reason` column of `pertest.csv`.

The tables in `results/tables/paper_layout/` are the ones of the paper:

| File | Content |
|------|---------|
| `test_results.tex` | Verdicts per tool and subject (Pass, confirmed violations, FP, FN, inconclusive) |
| `classification.tex` | Classification of the confirmed violations (normative, suite property, test defect) |
| `suite_violations.tex` | Defects of Solmate behind the suite-property violations, with the verdict of each tool |
| `time.tex` | Execution time of the complete suite (real, user, sys) |
| `memory.tex` | Peak memory of the complete suite |
| `accuracy.tex` | Accuracy per subject and overall reliability score |
| `stats.tex` | Welch's t-test, exact Mann-Whitney U test and Vargha-Delaney Â12 |
| `sensitivity.tex` | Effect of the exploration bounds on the inconclusive verdicts |

A false negative is counted when a test case passes on one tool while the other tool found a confirmed violation of a property of the contract (normative or suite property) in the same test case; divergences on defective test cases are not counted.
