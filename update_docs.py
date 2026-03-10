#!/usr/bin/env python
"""Regenerate CONFIG_REFERENCE.md from ghostty defaults."""

import subprocess
import sys
from pathlib import Path

CONFIG_REF_MD = Path(__file__).parent / "CONFIG_REFERENCE.md"
SEPARATOR = "---\n"


def get_ghostty_docs() -> str:
    result = subprocess.run(
        ["ghostty", "+show-config", "--default", "--docs"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error running ghostty: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def transform(raw: str) -> str:
    """Transform ghostty +show-config --default --docs output to Markdown."""
    lines = raw.splitlines()
    output: list[str] = []
    in_code_block = False
    current_section: str | None = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Section heading comments: lines starting with "# ## "
        if line.startswith("# ## "):
            if in_code_block:
                output.append("```")
                output.append("")
                in_code_block = False
            heading = line[2:]  # strip "# "
            current_section = heading
            output.append("")
            output.append(heading)
            output.append("")
            i += 1
            continue

        # Regular doc comment lines
        if line.startswith("# "):
            if in_code_block:
                output.append("```")
                output.append("")
                in_code_block = False
            output.append(line[2:])  # strip "# " prefix
            i += 1
            continue

        # Blank comment line
        if line == "#":
            if in_code_block:
                output.append("```")
                output.append("")
                in_code_block = False
            output.append("")
            i += 1
            continue

        # Key = value lines (default values)
        if line and not line.startswith("#"):
            if in_code_block:
                output.append("```")
                output.append("")
                in_code_block = False
            output.append(f"Default: `{line}`")
            output.append("")
            i += 1
            continue

        # Empty lines
        if not line:
            if not in_code_block:
                output.append("")
            i += 1
            continue

        i += 1

    if in_code_block:
        output.append("```")
        output.append("")

    return "\n".join(output)


def main() -> None:
    raw = get_ghostty_docs()
    new_content = transform(raw)

    text = CONFIG_REF_MD.read_text()
    sep_index = text.find(SEPARATOR)
    if sep_index == -1:
        print(f"Could not find separator '{SEPARATOR.strip()}' in {CONFIG_REF_MD}", file=sys.stderr)
        sys.exit(1)

    header = text[: sep_index + len(SEPARATOR)]
    updated = header + "\n" + new_content.strip() + "\n"
    CONFIG_REF_MD.write_text(updated)
    print(f"Updated {CONFIG_REF_MD}")


if __name__ == "__main__":
    main()
