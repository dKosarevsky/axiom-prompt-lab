#!/usr/bin/env python3
"""Count characters in a prompt Markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path


def extract_prompt_text(markdown: str) -> str:
    lines = markdown.splitlines(keepends=True)
    in_block = False
    prompt_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not in_block and stripped == "```text":
            in_block = True
            continue
        if in_block and stripped == "```":
            return "".join(prompt_lines)
        if in_block:
            prompt_lines.append(line)

    return markdown


def count_prompt_chars(path: Path) -> int:
    return len(extract_prompt_text(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count characters in the first fenced text prompt block."
    )
    parser.add_argument("path", type=Path, help="Markdown prompt file to inspect")
    parser.add_argument(
        "--limit",
        type=int,
        default=1500,
        help="Character limit to check against",
    )
    args = parser.parse_args()

    count = count_prompt_chars(args.path)
    over_by = count - args.limit

    print(f"file: {args.path}")
    print(f"characters: {count}")
    print(f"limit: {args.limit}")
    if over_by <= 0:
        print("status: ok")
        return 0

    print(f"status: over limit by {over_by}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
