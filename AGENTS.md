# Agent Instructions

Repository-specific rules live in [`docs/zasady-ai.md`](docs/zasady-ai.md) (Polish).
Read it before writing code. In short:

- Tests come first, always: write a failing test, watch it fail, then implement.
  The only exceptions are changes with no executable behavior (documentation,
  comments, commit messages, tool-enforced formatting). "Hard to test" is not an
  exception.
- No claim counts as proven without a test. In replies and commit messages,
  "works", "fixed", "done" and "safe" must name the test that proves it.
  Otherwise the status is explicitly "unverified".
- Pure functions in the core; pass state in and return a new value; keep side
  effects in thin adapters at the edges.
- Model the domain with closed types and exhaustive matching, so a forgotten
  case is a compile error rather than a silent bug.
- Find an existing pattern in the repo and follow it; introduce a new one only
  if you document it in the same change.
- One change, one purpose. No drive-by refactors, no leftover TODOs.

## Precedence

The global `AGENTS.md` provides defaults. `docs/zasady-ai.md` refines and
tightens them for this repository. When they conflict, the more specific and
more restrictive rule wins; the repository document may not loosen a global
rule (for example, it may not remove the test-first requirement).
