#!/usr/bin/env bash
# Installs the pinned tool versions and fetches the contracts under test.
# Everything is installed inside repro/.tools, nothing global is touched.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$ROOT/repro/.tools"
source "$ROOT/repro/versions.env"

mkdir -p "$TOOLS/bin"

# --- Halmos (Python package, isolated venv) ---------------------------------
if [ ! -x "$TOOLS/venv/bin/halmos" ] || ! "$TOOLS/venv/bin/halmos" --version 2>/dev/null | grep -q "$HALMOS_VERSION"; then
    uv venv --python "$HALMOS_PYTHON" "$TOOLS/venv"
    uv pip install --python "$TOOLS/venv/bin/python" "halmos==$HALMOS_VERSION" scipy==1.18.1 matplotlib==3.11.2
fi
ln -sf "$TOOLS/venv/bin/halmos" "$TOOLS/bin/halmos"

# --- Hevm (static release binary) -------------------------------------------
if [ ! -x "$TOOLS/bin/hevm" ] || ! "$TOOLS/bin/hevm" version 2>/dev/null | grep -q "$HEVM_VERSION"; then
    curl -fsSL -o "$TOOLS/bin/hevm" \
        "https://github.com/argotorg/hevm/releases/download/release/$HEVM_VERSION/hevm-x86_64-linux"
    chmod +x "$TOOLS/bin/hevm"
fi

# --- Contracts under test and test library ----------------------------------
fetch() { # fetch <url> <dir> <ref>
    local url="$1" dir="$ROOT/lib/$2" ref="$3"
    if [ ! -d "$dir/.git" ] && [ ! -f "$dir/.git" ]; then
        rm -rf "$dir"
        git clone --quiet "$url" "$dir"
    fi
    git -C "$dir" fetch --quiet --force --tags origin
    git -C "$dir" checkout --quiet --force "$ref"
    git -C "$dir" clean --quiet -fdx
    git -C "$dir" submodule update --quiet --init --recursive 2>/dev/null || true
}
fetch https://github.com/OpenZeppelin/openzeppelin-contracts openzeppelin-contracts "$OZ_REF"
fetch https://github.com/transmissions11/solmate              solmate                "$SOLMATE_REF"
fetch https://github.com/foundry-rs/forge-std                 forge-std              "$FORGE_STD_REF"

# --- Record the environment --------------------------------------------------
"$ROOT/repro/env.sh" > "$ROOT/results/environment.txt"
cat "$ROOT/results/environment.txt"
