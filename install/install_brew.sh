#!/bin/bash
set -euo pipefail

# Install Homebrew if not already installed

if command -v brew &> /dev/null; then
    echo "✅ Homebrew already installed"
    exit 0
fi

echo "🍺 Installing Homebrew..."

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH for current session
if [[ -f /opt/homebrew/bin/brew ]]; then
    # Apple Silicon
    eval "$(/opt/homebrew/bin/brew shellenv)"
elif [[ -f /usr/local/bin/brew ]]; then
    # Intel
    eval "$(/usr/local/bin/brew shellenv)"
fi

echo "✅ Homebrew installed successfully" 