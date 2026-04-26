#!/usr/bin/env python3
"""Count promptfoo YAML cases without requiring third-party YAML packages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CASE_PATTERN = re.compile(r"^-\s+description:", re.MULTILINE)


def count_cases(path: Path) -> int:
    if path.is_file():
        return len(CASE_PATTERN.findall(path.read_text(encoding="utf-8")))

    return sum(count_cases(case_path) for case_path in sorted(path.glob("*.yaml")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Count promptfoo YAML test cases.")
    parser.add_argument("path", type=Path, help="YAML case file or directory")
    parser.add_argument("--min-cases", type=int, default=0)
    args = parser.parse_args()

    total = count_cases(args.path)
    print(f"total_cases: {total}")
    if total < args.min_cases:
        print(f"status: below minimum by {args.min_cases - total}")
        return 1

    print("status: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
