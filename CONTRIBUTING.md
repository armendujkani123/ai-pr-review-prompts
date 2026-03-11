# Contributing

Thanks for contributing to AI PR Review Prompts.

## Development Setup

```bash
git clone https://github.com/armendujkani123/ai-pr-review-prompts.git
cd ai-pr-review-prompts
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

## Pull Request Guidelines

- Keep changes focused
- Add tests for behavior changes
- Update docs when flags, prompts, or examples change
- Explain user impact clearly in the pull request
