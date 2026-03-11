# AI PR Review Prompts

[![CI](https://github.com/armendujkani123/ai-pr-review-prompts/actions/workflows/ci.yml/badge.svg)](https://github.com/armendujkani123/ai-pr-review-prompts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

Open-source prompt packs and CLI tools for AI-assisted pull request review, change risk assessment, and code-review workflow standardization.

## Why This Project Exists

Many teams use AI during review, but the quality of results varies because prompts are inconsistent. This project packages structured review prompts so maintainers and contributors can get repeatable outputs for regressions, missing tests, rollout risks, and documentation gaps.

## Features

- Structured prompt templates for pull request review and code review
- Python CLI for generating reusable review prompts from a PR summary or diff notes
- Review modes for general quality, security, testing, and release risk
- Markdown and JSON output formats
- Examples, tests, CI, and open-source contributor documentation

## Repository Structure

```text
ai-pr-review-prompts/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── pr_review_cli.py
├── examples/
├── prompts/
├── pyproject.toml
└── tests/
```

## Installation

### Requirements

- Python 3.9 or newer

### Quick Start

```bash
git clone https://github.com/armendujkani123/ai-pr-review-prompts.git
cd ai-pr-review-prompts
python3 pr_review_cli.py --list-modes
```

### Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
```

## Usage

Generate a general review prompt:

```bash
python3 pr_review_cli.py \
  --title "Refactor payment retry logic" \
  --summary "Moves retry handling into a shared service and updates job scheduling"
```

Generate a security-focused review prompt:

```bash
python3 pr_review_cli.py \
  --title "Add JWT refresh endpoint" \
  --summary "Introduces token refresh flow and updates auth middleware" \
  --mode security
```

Load review context from a file:

```bash
python3 pr_review_cli.py --from-file examples/sample_pr_summary.txt --mode testing
```

Export JSON output for automation:

```bash
python3 pr_review_cli.py \
  --title "Change database migrations" \
  --summary "Backfills a new nullable column and updates ORM mappings" \
  --output-format json
```

## Available Review Modes

- `general`: broad review for correctness, clarity, maintainability, and regressions
- `security`: focus on auth, secrets, access control, and unsafe behavior
- `testing`: focus on missing tests, edge cases, and coverage gaps
- `release_risk`: focus on rollout impact, migration safety, and operational risk

## Quality Standards

- Tested with `unittest`
- GitHub Actions CI on push and pull request
- MIT licensed
- Contributor, conduct, and security documentation included

## Roadmap

- Add diff-aware prompt generation from changed file lists
- Add GitHub Actions examples for PR comment automation
- Add prompt packs for incident reviews and release sign-off
- Add optional severity tagging for findings

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup, testing, and pull request expectations.

## Security

See [SECURITY.md](./SECURITY.md) for vulnerability reporting guidance.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
