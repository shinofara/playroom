# AGENTS.md

This file provides guidance for agentic coding agents operating in this repository.
The goal is to ensure consistent, safe, and predictable changes even as the codebase evolves.

---

## Repository Overview

- Repository name: `playroom`
- Current state: minimal scaffold
- Expectation: this repo may grow to include application code, tests, and tooling
- Agents should **inspect the repo first** before assuming language or framework

When the repo is sparse or ambiguous, prefer **conservative, generic choices** and ask the user for clarification if needed.

---

## Build, Lint, and Test Commands

Agents should always look for standard tooling files before running commands:

- JavaScript / TypeScript: `package.json`, `pnpm-lock.yaml`, `yarn.lock`
- Python: `pyproject.toml`, `setup.cfg`, `requirements.txt`
- Rust: `Cargo.toml`
- Go: `go.mod`
- Other languages: inspect root config files

### JavaScript / TypeScript (if applicable)

- Install dependencies:
  - `npm install`
  - or `pnpm install`
  - or `yarn install`

- Build:
  - `npm run build`

- Lint:
  - `npm run lint`

- Test (all):
  - `npm test`
  - or `npm run test`

- Test (single file):
  - Jest: `npx jest path/to/test.test.ts`
  - Vitest: `npx vitest path/to/test.test.ts`

- Test (single test name):
  - Jest: `npx jest -t "test name"`
  - Vitest: `npx vitest -t "test name"`

### Python (if applicable)

- Install dependencies:
  - `pip install -r requirements.txt`
  - or `poetry install`

- Lint:
  - `ruff check .`
  - or `flake8`

- Format:
  - `black .`

- Test (all):
  - `pytest`

- Test (single file):
  - `pytest tests/test_example.py`

- Test (single test):
  - `pytest tests/test_example.py::test_name`

### Rust (if applicable)

- Build:
  - `cargo build`

- Lint:
  - `cargo clippy`

- Format:
  - `cargo fmt`

- Test (all):
  - `cargo test`

- Test (single test):
  - `cargo test test_name`

### General Rules

- Do not install new tools without user approval
- Prefer running **targeted tests** over full suites during iteration
- If commands are unclear, ask before running

---

## Code Style Guidelines

These rules apply unless overridden by more specific tooling or configuration.

### General Principles

- Prefer clarity over cleverness
- Make the smallest reasonable change
- Avoid unrelated refactors
- Follow existing patterns in the codebase

### Imports

- Use absolute imports where supported
- Group imports in this order:
  1. Standard library
  2. Third-party libraries
  3. Internal modules

- Remove unused imports
- Keep import lists sorted and stable

### Formatting

- Use the project formatter if present (e.g. Prettier, Black, rustfmt)
- Do not introduce formatting-only diffs unless requested
- Keep lines reasonably short (~100 characters)

### Naming Conventions

- Variables and functions: `camelCase` or language-idiomatic
- Types and classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE` where idiomatic
- Files and directories: lowercase with hyphens or underscores

Names should be:

- Descriptive
- Unambiguous
- Consistent with nearby code

### Types

- Prefer explicit types at module boundaries
- Avoid `any` / dynamic types unless unavoidable
- Let inference work for local variables when clear

### Functions

- Keep functions small and focused
- Avoid deeply nested conditionals
- Prefer pure functions where practical

### Error Handling

- Do not swallow errors silently
- Use explicit error types where available
- Include actionable context in error messages

Bad:

- `catch (e) {}`

Good:

- Log or rethrow with context
- Return structured errors when appropriate

### Logging

- Avoid excessive logging
- Never log secrets or credentials
- Prefer structured logs if used

### Comments

- Comment *why*, not *what*
- Avoid redundant comments
- Keep comments up to date with code

---

## Tests

- Follow existing test structure and naming
- Tests should be deterministic
- One logical behavior per test
- Use clear, descriptive test names

When adding tests:

- Prefer unit tests over integration tests
- Avoid unnecessary mocks
- Keep setup minimal and explicit

---

## Git and Workflow Expectations

- Do not commit unless explicitly asked
- Commits should represent meaningful units of work
- Avoid amending commits unless requested

---

## Cursor / Copilot Rules

- No `.cursor/rules/` directory found
- No `.cursorrules` file found
- No `.github/copilot-instructions.md` found

If these files are added later, their instructions **must be followed** and should take precedence where applicable.

---

## HR / Recruitment Documents

このリポジトリには採用関連のドキュメントが含まれています。

### 募集要項（Job Descriptions）

- **保存場所**: `docs/hr/career/`
- **命名規則**: `YYYY-MM-<ポジション名>.md`
- **言語**: 日本語・英語（バイリンガル形式）

募集要項を作成・編集する際は、このディレクトリ内の既存ファイルを参考にしてください。

### 評価レビュー（Candidate Reviews）

- **保存場所**: `docs/hr/reviews/`
- **命名規則**: `YYYY-MM-DD_<候補者名>.md`

### 関連スキル

- `.opencode/skills/job-posting/`: 募集要項作成スキル
- `.opencode/skills/gemini-drive/`: レジュメ評価スキル

---

## When in Doubt

- Inspect existing code first
- Ask the user for clarification
- Choose the safest, least surprising option

This file should be updated as the repository grows.
