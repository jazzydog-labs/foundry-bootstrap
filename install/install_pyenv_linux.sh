#!/bin/bash
set -euo pipefail

# Install pyenv on Linux using git checkout
if command -v pyenv &>/dev/null; then
    echo "✅ pyenv already installed"
    exit 0
fi

if ! command -v git &>/dev/null; then
    echo "❌ git not found. Please install git first."
    exit 1
fi

PYENV_ROOT="$HOME/.pyenv"

git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT"

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
