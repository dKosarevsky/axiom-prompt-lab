#!/usr/bin/env python3
"""Create a compact Markdown summary from promptfoo JSON output."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


def prompt_label(output: dict[str, Any]) -> str:
    prompt = output.get("prompt")
    if isinstance(prompt, dict):
        return str(prompt.get("label") or prompt.get("id") or prompt.get("display") or "unknown")
    if prompt is not None:
        return str(prompt)
    return str(output.get("promptLabel") or output.get("promptId") or "unknown")


def category(output: dict[str, Any]) -> str:
    test_case = output.get("testCase") or output.get("test") or {}
    if isinstance(test_case, dict):
        metadata = test_case.get("metadata") or {}
        if isinstance(metadata, dict) and metadata.get("category"):
            return str(metadata["category"])
    return str(output.get("category") or "uncategorized")


def score(output: dict[str, Any]) -> float | None:
    value = output.get("score")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def outputs_from_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    results = payload.get("results", payload)
    outputs = results.get("outputs") if isinstance(results, dict) else None
    if isinstance(outputs, list):
        return [item for item in outputs if isinstance(item, dict)]
    return []


def average(values: list[float]) -> float | None:
    return mean(values) if values else None


def format_float(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def summarize(outputs: list[dict[str, Any]]) -> str:
    by_prompt: dict[str, list[float]] = defaultdict(list)
    by_category: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    by_metric: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    failures: list[dict[str, Any]] = []

    for output in outputs:
        label = prompt_label(output)
        item_score = score(output)
        if item_score is not None:
            by_prompt[label].append(item_score)
            by_category[category(output)][label].append(item_score)
        if output.get("success") is False:
            failures.append(output)

        named_scores = output.get("namedScores") or output.get("named_scores") or {}
        if isinstance(named_scores, dict):
            for metric, metric_score in named_scores.items():
                if isinstance(metric_score, (int, float)):
                    by_metric[str(metric)][label].append(float(metric_score))

    labels = sorted(by_prompt)
    baseline = next((label for label in labels if "baseline" in label.lower()), labels[0] if labels else "baseline")
    candidate = next(
        (label for label in labels if label != baseline and "compact" in label.lower()),
        next((label for label in labels if label != baseline), "candidate"),
    )

    lines = [
        "# Promptfoo Results Summary",
        "",
        f"Total outputs: {len(outputs)}",
        f"Baseline average ({baseline}): {format_float(average(by_prompt.get(baseline, [])))}",
        f"Candidate average ({candidate}): {format_float(average(by_prompt.get(candidate, [])))}",
        "",
        "## Delta By Category",
        "",
        "| Category | Baseline | Candidate | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]

    category_deltas: list[tuple[str, float]] = []
    for name in sorted(by_category):
        base = average(by_category[name].get(baseline, []))
        cand = average(by_category[name].get(candidate, []))
        delta = None if base is None or cand is None else cand - base
        if delta is not None:
            category_deltas.append((name, delta))
        lines.append(f"| {name} | {format_float(base)} | {format_float(cand)} | {format_float(delta)} |")

    lines.extend(["", "## Delta By Metric", "", "| Metric | Baseline | Candidate | Delta |", "| --- | ---: | ---: | ---: |"])
    metric_deltas: list[tuple[str, float]] = []
    for name in sorted(by_metric):
        base = average(by_metric[name].get(baseline, []))
        cand = average(by_metric[name].get(candidate, []))
        delta = None if base is None or cand is None else cand - base
        if delta is not None:
            metric_deltas.append((name, delta))
        lines.append(f"| {name} | {format_float(base)} | {format_float(cand)} | {format_float(delta)} |")

    wins = sorted(category_deltas + metric_deltas, key=lambda item: item[1], reverse=True)[:5]
    regressions = sorted(category_deltas + metric_deltas, key=lambda item: item[1])[:5]

    lines.extend(["", "## Biggest Wins", ""])
    lines.extend([f"- {name}: {delta:+.3f}" for name, delta in wins] or ["- n/a"])

    lines.extend(["", "## Biggest Regressions", ""])
    lines.extend([f"- {name}: {delta:+.3f}" for name, delta in regressions] or ["- n/a"])

    lines.extend(["", "## Failed Assertions", "", f"- Total failed outputs: {len(failures)}"])
    lines.extend(["", "## Human Review Candidates", ""])
    if failures:
        for output in failures[:10]:
            lines.append(f"- {prompt_label(output)} / {category(output)} / score {format_float(score(output))}")
    else:
        lines.append("- No failed outputs in JSON.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize promptfoo JSON results.")
    parser.add_argument("results_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.results_json.read_text(encoding="utf-8"))
    summary = summarize(outputs_from_results(payload))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(summary, encoding="utf-8")
    print(f"summary: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
