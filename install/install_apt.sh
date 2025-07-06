#!/bin/bash
set -euo pipefail

# Install packages using apt-get from config/packages.yaml

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$(dirname "$SCRIPT_DIR")/config/packages.yaml"

if ! command -v apt-get &>/dev/null; then
    echo "❌ apt-get not found. Cannot install packages"
    exit 1
fi

# Parse YAML to get package names and apt overrides
PACKAGES=()
current_name=""
while IFS= read -r line; do
    if [[ $line =~ ^[[:space:]]*-\ name: ]]; then
        # Start of a package entry
        if [[ -n "$current_name" ]]; then
            PACKAGES+=("$current_name")
        fi
        current_name="$(echo "$line" | cut -d: -f2 | xargs)"
    elif [[ $line =~ apt-override: ]]; then
        current_name="$(echo "$line" | cut -d: -f2 | xargs)"
    fi
done < "$CONFIG_FILE"
if [[ -n "$current_name" ]]; then
    PACKAGES+=("$current_name")
fi
PACKAGES_STR="${PACKAGES[*]}"

echo "📦 Installing apt packages: $PACKAGES_STR"
apt-get update
apt-get install -y $PACKAGES_STR

echo "✅ apt packages installed"
