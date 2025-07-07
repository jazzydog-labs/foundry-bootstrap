#!/bin/bash
set -euo pipefail

# Install pyenv on Linux with dependency handling and optional offline archive
if command -v pyenv &>/dev/null; then
    echo "✅ pyenv already installed"
    exit 0
fi

PYENV_ROOT="$HOME/.pyenv"

# Install build dependencies unless explicitly skipped
if command -v apt-get &>/dev/null && [[ -z "${PYENV_SKIP_DEPS:-}" ]]; then
    DEPS=(
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev
        libsqlite3-dev curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev
        libxmlsec1-dev libffi-dev liblzma-dev
    )
    apt-get update
    apt-get install -y "${DEPS[@]}"
fi

# Use local archive when provided, otherwise clone from GitHub
if [[ -n "${PYENV_ARCHIVE:-}" && -f "$PYENV_ARCHIVE" ]]; then
    mkdir -p "$PYENV_ROOT"
    tar -xzf "$PYENV_ARCHIVE" -C "$PYENV_ROOT" --strip-components=1
else
    if ! command -v git &>/dev/null; then
        echo "❌ git not found. Please install git first."
        exit 1
    fi
    git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT"
fi

export PYENV_ROOT="$PYENV_ROOT"
export PATH="$PYENV_ROOT/bin:$PATH"

if ! grep -q 'pyenv init' "$HOME/.bashrc" 2>/dev/null; then
    echo '# pyenv configuration' >> "$HOME/.bashrc"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$HOME/.bashrc"
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'eval "$(pyenv init --path)"' >> "$HOME/.bashrc"
    echo 'eval "$(pyenv init -)"' >> "$HOME/.bashrc"
fi

source "$HOME/.bashrc"

echo "✅ pyenv installed successfully"
