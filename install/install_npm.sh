#!/bin/bash
set -euo pipefail

# Install npm global packages

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first via Homebrew."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm first."
    exit 1
fi

echo "📦 Installing npm global packages..."

# Read packages from config file
CONFIG_FILE="$(dirname "$0")/../config/npm.yaml"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ npm config file not found: $CONFIG_FILE"
    exit 1
fi

# Extract package names from YAML (simple parsing)
PACKAGES=()
while IFS= read -r line; do
    # Skip comments and empty lines
    if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line// }" ]]; then
        continue
    fi
    # Extract package names (lines starting with -)
    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*([^[:space:]]+) ]]; then
        PACKAGE="${BASH_REMATCH[1]}"
        # Skip commented packages
        if [[ ! "$PACKAGE" =~ ^# ]]; then
            PACKAGES+=("$PACKAGE")
        fi
    fi
done < "$CONFIG_FILE"

# Install each package
for package in "${PACKAGES[@]}"; do
    echo "📦 Installing $package..."
    npm install -g "$package"
done

echo "✅ npm global packages installed successfully" 