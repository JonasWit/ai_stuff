# Agent Instructions

This repository is a knowledge base: how to write and maintain code so that AI agents make fewer
mistakes, and how to encode that knowledge in the instruction file of any harness (`AGENTS.md`,
`CLAUDE.md`, `GEMINI.md` and equivalents). It is not an application.

Read these before editing anything:

- `docs/rules.md` — canonical coding rules.
- `README.md` — the human-facing summary of preferred choices.
- `docs/instruction-files.md` — how to distribute those rules into instruction files.
- `docs/decisions.md` — decision log; every new pattern needs an entry here.
- `docs/probes.md` — probes that check whether the rules actually bind.

## Verification and tests

- Tests come first, always. The only exceptions are changes with no executable
  behavior: documentation content, comments, commit messages, tool-enforced formatting.
- Watch the test fail before implementing. A test that passed before the change
  proves nothing.
- No claim without a test. Otherwise state "unverified" and what is missing.
- Run `uv run python scripts/check.py` before committing and paste the raw output.
- Scripts and tests are Python, managed by `uv`. Tests use `pytest`. Do not add a
  second toolchain for tooling.
- Every commit message needs one trailer line: `Test: <name>` or
  `Unverified: <reason>`. The `commit-msg` hook rejects anything else.

## Writing rules

- Normative rules live in `docs/`. This file summarizes and links; it never copies
  full rule text, because duplication is a bug.
- Everything in this repository is English: documentation, instruction files,
  comments, commit messages and repository metadata.
- Rules are harness-independent. Tool-specific mechanics belong in
  `docs/instruction-files.md`, never in the canonical source.
- Do not number rule lists; headings carry the structure.
- Stay within the file size budget enforced by `scripts/check.py`.

## Working process

- Find an existing pattern and follow it. A new pattern means a new entry in
  `docs/decisions.md` in the same change.
- One change, one purpose. No drive-by refactors, no leftover TODOs.
- Ask questions through the structured question tool, never in plain prose.
- Report what you could not verify. Silence about uncertainty is a false claim.

## Structure

- `docs/` — the knowledge itself
- `scripts/` — tooling in Python, with pytest tests in `scripts/tests/`
- `AGENTS.md` — shared rules read by most harnesses
- `CLAUDE.md` — thin Claude Code adapter that imports `AGENTS.md`
- `.githooks/` — git hooks, enabled through `core.hooksPath`
- `.github/` — pull request template

## Precedence

The global instruction file provides defaults. The documents here refine and tighten
them. When they conflict, the more specific and more restrictive rule wins; this
repository may not loosen a global rule, for example by dropping the test-first
requirement.
