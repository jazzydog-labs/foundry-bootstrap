#!/bin/bash
set -euo pipefail

# Install Python 3.12 via pyenv

PYTHON_VERSION="3.12.0"

echo "🐍 Installing Python $PYTHON_VERSION via pyenv..."

# Ensure pyenv is available
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv not found. Please install pyenv first."
    exit 1
fi

# Check if Python version is already installed
if pyenv versions | grep -q "$PYTHON_VERSION"; then
    echo "✅ Python $PYTHON_VERSION already installed"
else
    echo "📦 Installing Python $PYTHON_VERSION..."
    pyenv install "$PYTHON_VERSION"
fi

# Set as global Python version
echo "🌍 Setting Python $PYTHON_VERSION as global version..."
pyenv global "$PYTHON_VERSION"

# Verify installation
PYTHON_VERSION_OUTPUT=$(python3 --version 2>&1)
echo "✅ $PYTHON_VERSION_OUTPUT installed and set as global"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Upgrade pip to latest version
echo "📦 Upgrading pip to latest version..."
python3 -m pip install --upgrade pip

# Add Python user bin directory to PATH for current session
PYTHON_USER_BIN="$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin"
if [[ -d "$PYTHON_USER_BIN" ]]; then
    export PATH="$PYTHON_USER_BIN:$PATH"
    echo "📝 Added Python user bin directory to PATH: $PYTHON_USER_BIN"
fi

echo "✅ Python setup complete" 