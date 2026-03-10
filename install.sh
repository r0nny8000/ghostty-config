#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_CONFIG="$SCRIPT_DIR/config"
GHOSTTY_DIR="$HOME/Library/Application Support/com.mitchellh.ghostty"
TARGET="$GHOSTTY_DIR/config"

mkdir -p "$GHOSTTY_DIR"

if [[ -L "$TARGET" ]]; then
    current_target="$(readlink "$TARGET")"
    if [[ "$current_target" == "$REPO_CONFIG" ]]; then
        echo "Already installed: $TARGET -> $REPO_CONFIG"
        exit 0
    else
        echo "Replacing existing symlink: $TARGET -> $current_target"
        rm "$TARGET"
    fi
elif [[ -e "$TARGET" ]]; then
    backup="${TARGET}.bak.$(date +%Y%m%d_%H%M%S)"
    echo "Backing up existing config to: $backup"
    mv "$TARGET" "$backup"
fi

ln -s "$REPO_CONFIG" "$TARGET"
echo "Installed: $TARGET -> $REPO_CONFIG"
