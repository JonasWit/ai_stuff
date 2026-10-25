<div align="center">

# AI Rules

**Rules that make AI agents break less code — written so they can be enforced, not just declared.**

![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Docs: English](https://img.shields.io/badge/docs-English-red)
![Check: one command](https://img.shields.io/badge/check-one%20command-success)

</div>

A knowledge base about writing and maintaining code with AI agents. It is not an application and
not a framework: a set of rules, documents and scripts you copy into your own project.

The rules describe code, not tooling. The same set works in Claude Code, OpenCode, Codex, Cursor,
Copilot and Gemini CLI.

## Why this exists

A model does not break code because it is bad at coding. It breaks code because it works under
context pressure: it loses the thread, invents a nonexistent API, skips a variant, fixes one of
two copies of the same rule, makes a "local" change that touches five files. Every rule in this
repository targets one of those failure modes. A rule that targets none has no business here.

Starting assumption: **a rule that lives only in prose is a probability, not a guarantee.** That is
why every rule has a path down the enforcement ladder — from prose, through a checklist and a
single command, to a hook, CI and permissions.

The rules are language-agnostic. Types, contracts and error handling translate into the idioms of
the language the project is written in. The author's tooling preference (Python, `uv`, `pytest` for
helper scripts) is described separately and is not an architectural rule.

## Start in a minute

```sh
git clone https://github.com/JonasWit/AI-Rules.git
cd AI-Rules
uv run python scripts/check.py
```

The last command checks repository consistency: required files, dead links, forbidden markers,
file size budgets and project tests.

## Pick your path

| I want to… | Start with |
| --- | --- |
| learn the rules and the reasoning | [`docs/rules.md`](docs/rules.md) |
| adopt them in my project | [`AGENTS.md`](AGENTS.md), then [`docs/instruction-files.md`](docs/instruction-files.md) |
| see what good code looks like | [`examples/kotlin/`](examples/kotlin/README.md) |
| check whether a model actually follows them | [`docs/probes.md`](docs/probes.md) |
| see what is enforced mechanically | [`scripts/check.py`](scripts/check.py) |

## One rule set, every harness

The content of the rules is shared. Only the file a harness reads and the way it includes extra
content depend on the tool.

| Harness | File it reads |
| --- | --- |
| Claude Code | [`CLAUDE.md`](CLAUDE.md), which imports [`AGENTS.md`](AGENTS.md); newer versions read `AGENTS.md` directly |
| OpenCode | [`AGENTS.md`](AGENTS.md) |
| Codex | [`AGENTS.md`](AGENTS.md) |
| Cursor | [`AGENTS.md`](AGENTS.md) or `.cursor/rules/*.mdc` |
| GitHub Copilot | [`AGENTS.md`](AGENTS.md) or `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` |

Details, differences and portability traps: [`docs/instruction-files.md`](docs/instruction-files.md).

## What is inside

```
docs/            knowledge: rules, distribution to instruction files, decisions, probes
examples/kotlin/ golden example of a pure core (TimerEngine)
scripts/         one check command plus its pytest suite
AGENTS.md        shared rules for every harness
CLAUDE.md        thin Claude Code adapter: imports AGENTS.md
.githooks/       commit-msg hook that demands evidence in the commit
.github/         pull request template with the definition of done
```

## Preferred choices

### Non-negotiable

- **Test before code.** Always, except changes with no executable behavior.
- **A claim requires a test.** Label a judgment ("this is clearer") as a judgment, not as proof.
- **One change, one purpose.** No refactors along the way.

### Architecture

- **Functional core, thin I/O shell.** The logic does not know that a network, clock or file exists.
- **Dependencies point one way.** Adapters and UI know the core; the core never knows them.
- **Validate once at the boundary.** External data becomes a narrow type on entry and is trusted deeper.
- **Modules by domain, not by type.** `orders/`, not `services/` + `models/` + `controllers/`.
- **Variants as closed types with exhaustive matching.** A forgotten case is a compile error; in languages without sum types, an `enum` plus a test that iterates every variant.
- **Errors as values in the core.** `Result`/`Either`, or an explicit error type in the signature when the language has no typed result. Exceptions stay at the boundary.
- **Explicit state passed as an argument.** No globals, singletons or mutable modules.
- **Time, randomness, identifiers and the network are injected.** The core never reads them itself.
- **Configuration is loaded once, at startup.** Passed on as an explicit object.
- **Composition over inheritance.** Class hierarchies only where a framework requires them.
- **At most three layers.** Every extra layer costs context and invites mistakes.
- **No DI containers, behavior-changing decorators or metaprogramming.** Explicit calls.

### Code

- **A file around 300 lines, a function around 30.** This is a project convention, not a measurement; the file limit is enforced by [`scripts/check.py`](scripts/check.py).
- **One name per concept across the repository.** No synonyms; no `data`, `manager`, `utils`, `helper`.
- **No flags in parameters.** A variant is a separate function or a named options object.
- **Early exits, at most two levels of nesting.**
- **Data instead of logic.** A case matrix is a table or a mapping, not an `if`/`else` chain.
- **Immutable structures.** A function returns a new value; it does not mutate its input.
- **Deterministic ordering** in collections and output, so diffs stay readable.
- **A narrow module API.** A few public functions, the rest private.
- **A comment explains a trap, not the code.** Module header: why it exists, what it takes, what it guarantees.

### Tests

- **One test, one rule.** The test name is a sentence about guaranteed behavior.
- **The core is tested without mocks.** Mocks only at boundaries we defined ourselves.
- **Deterministic tests.** No real clock, network or randomness; inject them instead.
- **Property and snapshot tests** where there are too many cases to enumerate by hand.
- **Before changing old code**, write a characterization test for the current behavior.

### Dependencies and tooling

- **Standard library before a package.** A new dependency needs a justification.
- **Pinned versions, lockfile in the repository.**
- **One toolchain for tooling.** No second build system next to an existing one.
- **One check command** per project, regardless of language.
- **Formatting and lint in tool configuration**, not in documentation as a request.

### Author preference, not architecture

- **Helper scripts and their tests in Python**, environment and versions managed by `uv`, tests in `pytest`.
- This concerns tooling, not project code. A project with its own toolchain keeps it.

### What not to do

- **Do not build abstractions "for the future".** Introduce them when a second case appears.
- **Do not add a layer just to "separate responsibilities".** First check that the problem exists.
- **Do not extract shared code until there are two real uses.**
- **Do not rename or restructure in a commit that fixes a bug.**
- **Do not leave `TODO` behind.** Either it is done, or it is reported as not done.

## Golden example

[`examples/kotlin/`](examples/kotlin/README.md) — `TimerEngine` from the `WorkoutBase` project as a
model of a pure core: immutable state, time as an argument, exhaustive variant matching and tests
written as a specification.

```kotlin
@Test
fun tick_throughPrepare_movesToFirstWorkRound() { … }

fun tick(state: TimerState, deltaMillis: Long): TimerTransition
```

The core does not read a clock — it receives elapsed time as an argument and returns a new state
together with the list of cues to play. That is why the test needs neither real time nor Android.

## Documents

| File | The question it answers |
| --- | --- |
| [`docs/rules.md`](docs/rules.md) | Which rules to follow when writing code, and why they reduce the number of model mistakes |
| [`docs/instruction-files.md`](docs/instruction-files.md) | How to move this knowledge into the instruction file of any harness so it actually works |
| [`docs/decisions.md`](docs/decisions.md) | Decision log: problem, decision, rejected alternatives, consequences |
| [`docs/probes.md`](docs/probes.md) | Probes that try to break the rules, to establish which ones actually bind |
| [`AGENTS.md`](AGENTS.md) | The shared instruction file; [`CLAUDE.md`](CLAUDE.md) imports it for Claude Code |

## Enforcement

| Mechanism | What it blocks |
| --- | --- |
| [`scripts/check.py`](scripts/check.py) | Missing documents, dead links, forbidden markers, oversized files, failing project tests |
| `uv run pytest` | Regressions in the check script itself |
| `.githooks/commit-msg` | Commits without a `Test:` or `Unverified:` line |
| `.github/pull_request_template.md` | Pull requests that skip the definition of done |

Enable the hooks once per clone:

```sh
git config core.hooksPath .githooks
```

Run the check (including project tests, when `pyproject.toml` exists):

```sh
uv run python scripts/check.py
```

Run only the check script's tests:

```sh
uv run pytest
```

## Using this in a new project

- Copy [`AGENTS.md`](AGENTS.md) and those documents from `docs/` that fit the project. If your harness reads its own file, add an adapter that imports the shared content instead of copying it.
- Keep normative rules in one place and link to them; never copy the full text twice.
- Add stack-specific commands and tool configuration in the same change, so the rules become executable rather than aspirational.
- Write the golden example in the language of the first project, not before.
- Run the probes from [`docs/probes.md`](docs/probes.md) once the rules are in place.

## License

MIT — see [`LICENSE`](LICENSE). Unless stated otherwise in a subdirectory, the contents are
published under that license.
