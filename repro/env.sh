#!/usr/bin/env bash
# Prints the hardware/software environment of the experiment.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$ROOT/repro/versions.env"
TOOLS="$ROOT/repro/.tools/bin"
echo "date:        $(date -Iseconds)"
echo "host cpu:    $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs)"
echo "cores:       $(nproc)"
echo "memory:      $(free -h | awk '/Mem:/{print $2}')"
echo "os:          $(. /etc/os-release; echo "$PRETTY_NAME") / kernel $(uname -r)"
echo "forge:       $(forge --version | head -1)"
echo "solc:        $(grep -h '^solc' "$ROOT/foundry.toml" | cut -d'"' -f2)"
echo "halmos:      $("$TOOLS/halmos" --version 2>&1 | tail -1) (solver: ${HALMOS_SOLVER:-z3})"
echo "hevm:        $("$TOOLS/hevm" version 2>&1 | head -1)"
echo "z3:          $(z3 --version)"
echo "cvc5:        $(cvc5 --version 2>/dev/null | head -1)"
for d in openzeppelin-contracts solmate forge-std; do
    printf '%-12s %s %s\n' "$d:" "$(git -C "$ROOT/lib/$d" describe --tags --always 2>/dev/null)" "$(git -C "$ROOT/lib/$d" rev-parse HEAD)"
done
