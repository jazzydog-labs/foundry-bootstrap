#!/bin/bash
set -euo pipefail

# foundry-bootstrap: Entry point for bootstrapping the foundry ecosystem
# This script handles minimal bash bootstrapping before delegating to Python

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$SCRIPT_DIR/install"
ORCHESTRATE_DIR="$SCRIPT_DIR/orchestrate"

echo "🔧 foundry-bootstrap: Starting bootstrap process..."

# Install core dependencies via bash scripts
echo "📦 Installing core dependencies..."

# Install Homebrew if missing
if ! command -v brew &> /dev/null; then
    echo "🍺 Installing Homebrew..."
    bash "$INSTALL_DIR/install_brew.sh"
else
    echo "✅ Homebrew already installed"
fi

# Install pyenv if missing
if ! command -v pyenv &> /dev/null; then
    echo "🐍 Installing pyenv..."
    bash "$INSTALL_DIR/install_pyenv.sh"
else
    echo "✅ pyenv already installed"
fi

# Install Python 3.12 via pyenv
echo "🐍 Installing Python 3.12..."
bash "$INSTALL_DIR/install_python.sh"

# Setup Python orchestrator
echo "🔧 Setting up Python orchestrator..."
bash "$INSTALL_DIR/setup_python_orchestrator.sh"

# Hand off to Python orchestrator
echo "🚀 Delegating to Python orchestrator..."
cd "$ORCHESTRATE_DIR"
if python3 main.py; then
    echo "✅ Bootstrap complete!"
    
    # Run test script to verify installation
    echo "🧪 Running verification tests..."
    cd "$SCRIPT_DIR"
    if python3 test_setup.py; then
        echo "🎉 All tools verified successfully!"
    else
        echo "⚠️  Some tools may not be properly installed. Check the output above."
        exit 1
    fi
else
    echo "❌ Bootstrap failed. Check the output above."
    exit 1
fi 