# Pattern decision log

## Why this file

The rule "a new pattern only with a record" with no place to record it ends with patterns appearing
in code and knowledge about them in nobody's head. This file is that place.

An entry is short and answers four questions: what was the problem, what was decided, what was
rejected, and what it entails. It is not an essay and not documentation — it is a trace of a decision.

## When to add an entry

- you introduce a pattern that does not exist in the repository yet
- you change an existing pattern
- you deliberately reject an alternative that will keep coming back in conversations
- you break a rule from `docs/rules.md` and have a reason for it

## Entry template

```markdown
### Decision name

**Status:** accepted | rejected | to revise

**Problem:** one sentence about what needed a decision.

**Decision:** what was decided, in the imperative.

**Rejected alternatives:** what was considered and why it was dropped.

**Consequences:** what this means for future changes, what must not be done.
```

## Decisions

### The repository as a knowledge base, not a project

**Status:** accepted

**Problem:** style and architecture rules for AI are scattered across conversations, notes and
configuration files of various tools. A place that is the source of truth is needed.

**Decision:** this repository stores knowledge about architecture and code style for working with
language models, plus instructions on how to move that knowledge into agent instruction files.
Project code goes elsewhere.

**Rejected alternatives:** keeping the rules only in a global instruction file — cannot be versioned
or justified; keeping them in notes outside the repository — no change history.

**Consequences:** the documents in `docs/` are canonical. The global instruction file is their
distilled version and may not contain contradicting content.

### Normative document separated from the summary

**Status:** accepted

**Problem:** full justifications are too long for startup context, and a short summary is not enough
to settle disputes.

**Decision:** `docs/rules.md` is the canonical source. The `AGENTS.md` file in the repository
contains a summary and a link, not a copy.

**Rejected alternatives:** one giant `AGENTS.md` — dilutes attention and drops out during context
compaction; links without a summary — the model has no reason to look inside.

**Consequences:** changing a rule requires checking both places. A duplicate of the full content is a
bug.

### A closed list of exceptions from test-before-code

**Status:** accepted

**Problem:** the rule "always a test" without a list of exceptions is ignored in practice, because
the model finds a justification for itself. A rule with an open list is equally easy to bypass.

**Decision:** the exceptions are listed exhaustively: documentation, comments, commit messages,
tool-enforced formatting. The agent must name the list item it relies on.

**Rejected alternatives:** "the agent's common sense" — unpredictable; no exceptions — the rule is
impossible to satisfy when changing a document itself.

**Consequences:** a new exception requires an entry in this log and a change to the document.
Expanding the list in conversation is not allowed.

### A decision log instead of a patterns catalog

**Status:** accepted

**Problem:** a patterns catalog describes what exists. It does not say why it exists or what was not
chosen, so dead patterns live forever and rejected ideas keep coming back.

**Decision:** patterns are recorded as decisions with a problem, alternatives and consequences, in
this file.

**Rejected alternatives:** a textbook-style patterns catalog — no decision history; no record at all
— knowledge disappears after the session.

**Consequences:** an entry without rejected alternatives is incomplete, because it does not protect
against a rejected idea returning.

### A golden example only with the first stack

**Status:** accepted — superseded by "Golden example from workoutbase"

**Problem:** a reference example is the most effective carrier of style, but one written in a guessed
language teaches the wrong thing.

**Decision:** the model module is written in the language of the first real project, together with
its tool configuration.

**Rejected alternatives:** an example in TypeScript or Python right away — risk that the stack will
be different; a pseudocode example — cannot be run, so it is not testable.

**Consequences:** until the first project, the rules are descriptive only, and their enforcement is
limited to `scripts/check.py`, the hook and the PR template.

### A check script without stack dependencies

**Status:** accepted

**Problem:** without a stack there is nothing to run, so "one command" might not exist for weeks — and
a rule without a command is prose.

**Decision:** `scripts/check.py` checks what is always checkable: required files, dead links in
documents, forbidden markers, file size budget. Once a stack appears, the same command runs its
tests.

**Rejected alternatives:** waiting for a stack — a rule without enforcement; a heavy Node-dependent
runner — contradicts dependency minimalism.

**Consequences:** the script has its own tests in `scripts/tests/`, run with `uv run pytest`. Every new
check requires a test.

### Python scripts and tests managed by uv

**Status:** accepted as an author preference

**Problem:** helper tools must run with one command on every machine, without manually installing an
interpreter and libraries. The first version was in PowerShell, which tied the tooling to Windows and
made testing harder.

**Decision:** helper scripts and their tests in this repository are in Python. The environment and
versions are managed by `uv`, tests are written in `pytest` and run with `uv run pytest`. Dependencies
are declared in `pyproject.toml`, versions are pinned in `uv.lock`. This is a tooling choice, not an
architectural rule.

**Rejected alternatives:** PowerShell — Windows only, no convenient test framework; Node — a second
toolchain next to Python; global `pip` — a nondeterministic environment that depends on what is
already installed.

**Consequences:** every new script has a test in `scripts/tests/`. Running it requires neither
activating an environment nor installing dependencies by hand. Architectural rules remain
language-independent; a project with its own toolchain keeps it.

### A human summary in the README

**Status:** accepted

**Problem:** a one-page summary of choices in a separate file required an extra click, and on entry to
the repository a human opens `README.md` anyway.

**Decision:** the summary of preferred choices lives in `README.md`. The documents in `docs/` contain
justifications, details and the decision log.

**Rejected alternatives:** a separate file in `docs/` — an extra step and a risk of divergence; no
summary — entry requires reading the whole document.

**Consequences:** `README.md` is the only place for the digest. Changing a rule requires checking
`README.md` and `docs/rules.md`.

### A golden example from WorkoutBase

**Status:** accepted — supersedes the earlier decision "A golden example only with the first stack"

**Problem:** descriptive rules do not show what their implementation looks like in real code, and the
first project's stack already exists: Kotlin in `WorkoutBase`.

**Decision:** `examples/kotlin/` contains `TimerEngine` and its tests copied from `WorkoutBase` without
changes, with a description of what they illustrate and what this directory does not contain.

**Rejected alternatives:** writing a new example from scratch — would duplicate existing, proven code;
keeping the example only in `WorkoutBase` — the knowledge would not be available outside that project.

**Consequences:** the example is a reference, not a built module. Changing the rules requires checking
whether the example still illustrates them.

### Rules independent of the harness

**Status:** accepted

**Problem:** the distribution document assumed OpenCode and Claude Code. The rules looked tied to a
tool, and every new harness required copying content instead of reusing it.

**Decision:** rule content is harness-independent. A harness is an adapter: a file name, a location
and an inclusion mechanism. The repository keeps one source (`AGENTS.md` plus `docs/`) and thin
adapters, such as `CLAUDE.md` importing `AGENTS.md`.

**Rejected alternatives:** a separate copy of the rules for every tool — divergence by design; support
only for `AGENTS.md` — Claude Code before v2.1.277 and several harnesses read their own file names;
a full adapter per tool in the repository — copies content that ages with the tool.

**Consequences:** a new harness means a row in the table in `docs/instruction-files.md` and, if
needed, an adapter. An adapter may not contain normative content. The canonical source may not
depend on a tool name.

### English as the repository language

**Status:** accepted

**Problem:** documentation was in Polish while instruction files, scripts and commit messages were in
English. Two languages in one repository produced a hybrid vocabulary and made the rules harder to
reuse outside one person's projects.

**Decision:** every document, instruction file, comment, commit message and repository metadata is in
English. Only the user's replies may use another language.

**Rejected alternatives:** keeping the docs in Polish and translating on demand — guarantees drift and
duplicated content; mixing languages per document — the model answers in a random language and edits
produce hybrid sentences.

**Consequences:** the document file names are English (`rules.md`, `instruction-files.md`,
`decisions.md`, `probes.md`), and `scripts/check.py` requires those names. A new document is created
in English from the start.
