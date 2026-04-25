#!/usr/bin/env python3
"""Count characters in a prompt Markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_frontmatter(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return metadata
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    return {}


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


def parse_int_metadata(metadata: dict[str, str], key: str) -> int | None:
    value = metadata.get(key)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count characters in the first fenced text prompt block."
    )
    parser.add_argument("path", type=Path, help="Markdown prompt file to inspect")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Character limit to check against",
    )
    parser.add_argument(
        "--check-metadata",
        action="store_true",
        help="Verify frontmatter char_limit and measured_chars values",
    )
    parser.add_argument(
        "--compare-text",
        type=Path,
        help="Compare extracted prompt text to another text file",
    )
    args = parser.parse_args()

    markdown = args.path.read_text(encoding="utf-8")
    prompt_text = extract_prompt_text(markdown)
    metadata = parse_frontmatter(markdown)
    metadata_limit = parse_int_metadata(metadata, "char_limit")
    limit = args.limit if args.limit is not None else metadata_limit or 1500
    count = len(prompt_text)
    over_by = count - limit
    status = 0

    print(f"file: {args.path}")
    print(f"characters: {count}")
    print(f"limit: {limit}")
    if over_by <= 0:
        print("status: ok")
    else:
        print(f"status: over limit by {over_by}")
        status = 1

    if args.check_metadata:
        metadata_errors: list[str] = []
        measured_chars = parse_int_metadata(metadata, "measured_chars")
        if metadata_limit is not None and metadata_limit != limit:
            metadata_errors.append(f"metadata char_limit: {metadata_limit} != {limit}")
        if measured_chars is None:
            metadata_errors.append("metadata measured_chars: missing or invalid")
        elif measured_chars != count:
            metadata_errors.append(f"metadata measured_chars: {measured_chars} != {count}")

        if metadata_errors:
            for error in metadata_errors:
                print(error)
            status = 1
        else:
            print("metadata: ok")

    if args.compare_text:
        expected = args.compare_text.read_text(encoding="utf-8")
        if expected == prompt_text:
            print("compare_text: ok")
        else:
            print(f"compare_text: mismatch with {args.compare_text}")
            status = 1

    return status


if __name__ == "__main__":
    raise SystemExit(main())
