#!/usr/bin/env python3
"""Generate structured AI prompts for pull request review workflows."""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

DEFAULT_MODE = "general"


def prompt_dir() -> Path:
    return Path(__file__).resolve().parent / "prompts"


def list_modes() -> list[str]:
    return sorted(path.stem for path in prompt_dir().glob("*.md"))


def load_mode(mode: str) -> str:
    prompt_path = prompt_dir() / f"{mode}.md"
    if not prompt_path.exists():
        available = ", ".join(list_modes()) or "none"
        raise ValueError(f"Unknown mode '{mode}'. Available modes: {available}.")
    return prompt_path.read_text(encoding="utf-8").strip()


def read_summary(title: str | None, summary: str | None, from_file: str | None) -> tuple[str, str]:
    if from_file and summary:
        raise ValueError("Use either --summary or --from-file, not both.")
    pr_title = title.strip() if title else "Untitled pull request"
    if from_file:
        pr_summary = Path(from_file).read_text(encoding="utf-8").strip()
    elif summary:
        pr_summary = summary.strip()
    else:
        pr_summary = input("Enter pull request summary: ").strip()
    return pr_title, pr_summary


def build_prompt_payload(
    *,
    title: str,
    summary: str,
    mode: str = DEFAULT_MODE,
    changed_files: str | None = None,
    context: str | None = None,
) -> dict[str, str]:
    pr_title = title.strip()
    pr_summary = summary.strip()
    file_context = changed_files.strip() if changed_files else "No changed file list provided."
    extra_context = context.strip() if context else "No additional review context provided."
    mode_guidance = load_mode(mode)

    return {
        "title": "AI Pull Request Review Prompt",
        "pull_request_title": pr_title,
        "summary": pr_summary,
        "changed_files": file_context,
        "context": extra_context,
        "requested_output": (
            "1. High-Risk Findings\n"
            "2. Behavioral Regression Risks\n"
            "3. Missing Tests or Validation\n"
            "4. Security or Reliability Concerns\n"
            "5. Documentation or Rollout Gaps\n"
            "6. Final Review Recommendation"
        ),
        "review_mode": mode,
        "mode_guidance": mode_guidance,
    }


def render_markdown(payload: dict[str, str]) -> str:
    return textwrap.dedent(
        f"""\
# {payload["title"]}

## Pull Request Title
{payload["pull_request_title"]}

## Summary
{payload["summary"]}

## Changed Files
{payload["changed_files"]}

## Additional Context
{payload["context"]}

## Requested Output
{payload["requested_output"]}

## Review Mode
{payload["review_mode"]}

## Mode Guidance
{payload["mode_guidance"]}
"""
    ).strip()


def render_output(payload: dict[str, str], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2)
    return render_markdown(payload)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate AI prompts for pull request review workflows."
    )
    parser.add_argument("--title", help="Pull request title.")
    parser.add_argument("--summary", help="Pull request summary or description.")
    parser.add_argument("--from-file", help="Read the PR summary from a file.")
    parser.add_argument(
        "--mode",
        default=DEFAULT_MODE,
        help="Review mode to use. Run --list-modes to inspect options.",
    )
    parser.add_argument(
        "--changed-files",
        help="Optional newline-delimited or comma-delimited changed file list.",
    )
    parser.add_argument(
        "--context",
        help="Optional deployment, architecture, or team review context.",
    )
    parser.add_argument(
        "--output-format",
        default="markdown",
        choices=("markdown", "json"),
        help="Format for the generated prompt.",
    )
    parser.add_argument("--output", help="Optional path to save the generated prompt.")
    parser.add_argument(
        "--list-modes",
        action="store_true",
        help="List available review modes and exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_modes:
        for name in list_modes():
            print(name)
        return 0

    try:
        title, summary = read_summary(args.title, args.summary, args.from_file)
        if not summary:
            raise ValueError("A pull request summary is required.")
        payload = build_prompt_payload(
            title=title,
            summary=summary,
            mode=args.mode,
            changed_files=args.changed_files,
            context=args.context,
        )
        rendered = render_output(payload, args.output_format)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Prompt written to {output_path}")
        return 0

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
