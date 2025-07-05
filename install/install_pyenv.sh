#!/bin/bash
set -euo pipefail

# Install pyenv if not already installed

if command -v pyenv &> /dev/null; then
    echo "✅ pyenv already installed"
    exit 0
fi

echo "🐍 Installing pyenv..."

# Install pyenv via Homebrew
brew install pyenv

# Add pyenv to shell configuration
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [[ -n "$SHELL_CONFIG" ]]; then
    # Add pyenv init to shell config if not already present
    if ! grep -q "pyenv init" "$SHELL_CONFIG" 2>/dev/null; then
        echo "" >> "$SHELL_CONFIG"
        echo "# pyenv configuration" >> "$SHELL_CONFIG"
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$SHELL_CONFIG"
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> "$SHELL_CONFIG"
        echo 'eval "$(pyenv init --path)"' >> "$SHELL_CONFIG"
        echo 'eval "$(pyenv init -)"' >> "$SHELL_CONFIG"
        echo "📝 Added pyenv configuration to $SHELL_CONFIG"
    fi
    
    # Source the config for current session
    source "$SHELL_CONFIG"
fi

echo "✅ pyenv installed successfully" 