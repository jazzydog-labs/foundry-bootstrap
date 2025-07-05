#!/bin/bash
set -euo pipefail

# Setup Python orchestrator tools (pipx, etc.)

echo "🔧 Setting up Python orchestrator tools..."

# Ensure Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python first."
    exit 1
fi

# Install pipx for Python CLI tools
if ! command -v pipx &> /dev/null; then
    echo "📦 Installing pipx..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    
    # Add pipx to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    echo "📝 Added pipx to PATH: $HOME/.local/bin"
else
    echo "✅ pipx already installed"
fi

# Ensure Python user bin directory is in PATH
PYTHON_USER_BIN="$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin"
if [[ -d "$PYTHON_USER_BIN" ]]; then
    export PATH="$PYTHON_USER_BIN:$PATH"
    echo "📝 Added Python user bin directory to PATH: $PYTHON_USER_BIN"
fi

# Install basic Python development tools
echo "📦 Installing basic Python development tools..."

# Install requirements for the orchestrator
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_FILE="$REPO_ROOT/requirements.txt"

if [[ -f "$REQUIREMENTS_FILE" ]]; then
    echo "📦 Installing Python requirements..."
    python3 -m pip install --user -r "$REQUIREMENTS_FILE"
else
    echo "📦 Installing basic Python tools..."
fi

echo "✅ Python orchestrator setup complete" 