# Ghostty Terminal Configuration

This repository contains my personal [Ghostty](https://ghostty.org) terminal
configuration for macOS.

## Project Structure

- `config` — Ghostty configuration file (symlinked into
  `~/Library/Application Support/com.mitchellh.ghostty/config`)
- `install.sh` — Symlink installer script (idempotent, creates timestamped
  backups of existing configs)

## Active Configuration

Current settings in `config`:

```
shell-integration-features = no-cursor
font-family = "0xProto Nerd Font Mono"
font-size = 14
background = 323232
cursor-style = block
cursor-style-blink
```

## Updating the Config Reference

When Ghostty releases a new version with new or changed configuration options,
regenerate the Config Reference section by running:

```sh
python update_docs.py
```

This script runs `ghostty +show-config --default --docs`, applies the Markdown
transformation, and rewrites `CONFIG_REFERENCE.md`. Review the diff, then commit.

## Config Reference

The full config reference is in [`CONFIG_REFERENCE.md`](CONFIG_REFERENCE.md).
