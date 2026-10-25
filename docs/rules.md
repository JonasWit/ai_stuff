# Rules for writing code with AI

## Overarching rules

- Test before code, without exceptions. The only exception: changes with no executable behavior
  — documentation, comments, commit messages, tool-enforced formatting.
- The red phase must be observed. A test that passed before the change proves nothing.
- A claim without a test is a hypothesis. "Works", "fixed", "done" require the name of the test
  that confirms it.
- A pure core: state as an argument, a new value instead of mutation, side effects in thin adapters.
- Variants as closed types with exhaustive matching, so a forgotten case is a compile error rather
  than a silent bug.
- One source of truth per rule and one name per concept.
- One file, one topic. Fixed section order: types, pure functions, adapters.
- Do not guess APIs. Types or documentation first, code second.
- One purpose per change: no refactors along the way, no leftover TODOs.
- Find the existing pattern in the repository first, then repeat it.
- Before calling a task done, run the project check command (here:
  `uv run python scripts/check.py`) and show the raw output.
- A rule that cannot be checked mechanically will be broken sooner or later.

## How to read this document

This document is the canonical source of knowledge about writing code so that collaboration with a
language model is predictable. It is not a collection of human "best practices". The rules are
chosen for one goal: **fewer mistakes made by AI and cheaper, safer later changes**.

The document is normative. If code and document disagree, the code is wrong — unless the change was
deliberately recorded here or in `docs/decisions.md`.

Every rule corresponds to a real failure mode of the model: losing context, inventing a nonexistent
API, skipping a case, fixing one of two copies of a rule, a change that looks local but touches five
files. A rule that addresses none of these has no place here.

## Language independence

The rules describe properties of code, not syntax. They translate into the idioms of the language
the project is written in, instead of importing solutions from a language where they happened to
work well.

- **Closed variants and exhaustive matching** — a sealed class with `when` (Kotlin), a discriminated
  union with `never` (TypeScript), an `enum` with `match` (Python, Rust), a `switch` with an
  unreachable `default`. In languages without sum types, the compiler's role falls to a test that
  iterates every variant.
- **A result as a value** — `Result`, `Either`, or an explicit error type in the signature when the
  language has no typed result. Exceptions stay at the boundary.
- **Port and adapter** — `interface`, `Protocol`, `trait`, a higher-order function: whatever the
  language offers as a contract.
- **Pure function** — no mutation and no I/O, regardless of whether the language enforces it.

The author's tooling preferences (Python and `uv` for helper scripts and tests) are a choice of
environment, not an architectural rule. A project with its own toolchain keeps it.

## Precedence

### Global instruction file

The user's global instruction file — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or the equivalent in your
harness — contains a distilled, universal version of these rules. It works in every project,
including those where this document does not exist.

### This document

It is the canonical source and may tighten global rules. It may not loosen them. The rule that
applies: **the more specific and more restrictive wins**.

### User instruction

An explicit user instruction may waive a rule from this document. The conditions are less flexible
than they look:

- the waiver must be explicit; it may not be inferred from hurry, context or a mental shortcut
- the agent names the rule it waives and the risk that comes with it
- the waiver is recorded in the reply and in the commit as
  `Rule waived: <rule> (<reason>)`
- waiving a test rule **does not waive the ban on claims**: code without a test has the status
  `unverified` and may not be described as working

A user instruction may not waive safety rules or introduce unlawful content. In that situation the
agent refuses and explains why.

## Measures for every pattern

### Context cost

How many tokens and how many files must be read to make one correct change. A pattern that requires
reading half the repository is bad — no matter how clean it looks.

### Change locality

How many places must be touched when one requirement changes. A good answer is one place. If a new
case requires edits in five files and remembering two invariants, the pattern is hostile to AI.

### Error detectability

Whether a mistake will fail the compiler or a test, or pass silently. We prefer solutions where a
forgotten case is a compile error, not behavior that "kind of works" until the first production run.

A pattern that is elegant to a human but requires holding global invariants spread across many files
is rejected here — even if it reads well in code review.

## Tests

### Test before code, without exceptions

A test exists before any code is generated. The order is fixed: failing test, then implementation,
then refactor. There is no "I will write it first and add tests later" — a test added after the fact
describes code that already exists, so it checks nothing.

### A closed list of exceptions

The exception applies only to changes that **have no executable behavior**:

- documentation content, including this file and `README.md`
- comments
- commit messages and change descriptions
- formatting and file layout enforced by a tool

The list is closed. "It is hard to write a test", "the change is obvious", "it is only a rename",
"it is only a small fix" are not exceptions — they are sentences a model says to get around the
rule. Renames and refactors have a test, because the test must already exist before the change; if
it does not, a characterization test for the current behavior comes first.

If an agent uses an exception, it must name the list item it relies on in its reply. Its own
criteria are not allowed.

### The red phase must be observed

A test that passed before the change proves nothing. The agent must see a red result before writing
the implementation. A test written against existing code passes regardless of whether the logic is
correct — and that is exactly why it gives a false sense of safety.

The test must also actually check the claim it is meant to prove. An assertion about something
other than the declared effect is not proof.

### A claim without a test is a hypothesis

No statement about the behavior of code may be treated as proven unless a test supports it. This
applies to the agent's reply, the commit message, the change description and this document.

"Works", "fixed", "done", "safe", "does not affect anything else" are allowed only together with
the name of the test that confirms them. Without a test, the only allowed wording is an explicit
"unverified" together with what would have to be checked.

### Claim versus judgment

Not every statement is a claim about behavior. The distinction is necessary, because without it the
rule "no test means a hypothesis" cannot be satisfied and will be ignored entirely.

A behavioral claim — "the function returns X", "the change does not break Y", "it handles case Z" —
requires a test.

A judgment — "this split is clearer", "this name is better", "less code" — does not require a test,
but must be labeled as a judgment and may not be used as proof of correctness. A judgment is not an
argument in a dispute about behavior.

Numbers — timings, sizes, coverage, case counts — must come from an actual run. An estimate
presented as a fact is a claim without evidence.

### A test as a specification

One test corresponds to one rule. The test name is a sentence in domain language and states what
behavior is guaranteed. Reading the list of test names should be enough to reconstruct the
requirements without reading the implementation. That way a failing test tells the agent exactly
what stopped working, instead of forcing it to trace the code.

## Core style

### Pure functions

Functions are deterministic and free of side effects. The same arguments always produce the same
result. Reading the signature should be enough to say what the function does without reading its
body.

### State as an argument, a new value instead of mutation

A function that needs state receives it as an argument and returns a new value. It does not mutate
shared state. No mutation means no hidden call order — and hidden order is one of the most common
model mistakes when editing existing code.

### Side effects in thin adapters

I/O, network, filesystem, clock, randomness, environment variables — all of it lives in thin
wrappers at the edges of a module. The core logic does not know they exist. That is why core tests
need no mocks, and the model does not weave `fetch` into the middle of a calculation.

## Patterns that reduce model error

### Types at the boundaries

External data is validated once, on entry, and turned into a narrow type. Beyond that the core
trusts the type and does not repeat the checks. A model rarely makes mistakes in the middle when
there are no uncertain data shapes there — it makes them mainly at the boundary, where everything
is "some object".

### Closed sum types and exhaustive matching

Behavior variants are represented as a closed set of types, and handling requires exhaustive
matching. Adding a variant produces compile errors in every place that must be updated. This is the
most effective known technique for turning a silently skipped case into a loud error. When the
language has no sum types, a test that iterates every variant takes the compiler's role — otherwise
the rule does not work at all.

### Errors as values in the core

The core returns a result as a value whose type lists the possible failures. Exceptions stay at the
boundary, where they turn into a response or a log entry. The signature then shows every case that
must be remembered; an exception is invisible in the signature, so the model regularly skips it. In
languages without a typed result, an explicit error type in the signature or an equally explicit,
documented contract takes that role.

### Signatures without flags

No boolean parameters such as `send(x, true)` and no long positional parameter lists. A behavior
variant is a separate function or a named options object. A flag at the call site is unreadable to a
human and misleading to a model that does not see the function definition.

### Functional core, imperative shell

Logic is pure and testable without an environment. The whole environment — input, output,
configuration, time — lives in one thin place, usually at the bottom of the file. A model editing
logic then has no temptation to touch I/O, and one editing I/O does not need to understand the logic.

### A pipeline of small steps

A complex transformation is a sequence of small, pure functions with one input and one output. A new
step is inserted between two existing ones without rewriting the whole thing. One long procedural
function requires the model to understand everything on every change and invites accidental
modification of a neighboring fragment.

### Data instead of logic

When behavior is a matrix of cases, express it as data: a table, a mapping, a list of rules. A model
edits data far more reliably than an `if`/`else` chain. A chain of conditions grows uncontrollably,
and every new branch can change the behavior of a neighboring one.

### One source of truth per rule

Every business rule exists in exactly one place. Duplication is the main source of the "agent fixed
one copy" bug. If the same validation appears in two files, that is not a matter of taste — it is
guaranteed inconsistency on the next change.

### Names as search

Every concept has exactly one name across the repository. No synonyms such as `user`, `account`,
`client` for the same thing. No bags called `data`, `manager`, `utils`, `helper`, `handler`,
`process`. A name must make it possible to find every place with one search; the model works mostly
by searching, so names are its interface to the code.

### One file, one topic

A file corresponds to one topic and fits within a reasonable size budget, so it can be read in full.
The file name is the search path to the topic. A file that must be read in fragments is a file the
model will not understand.

### Fixed file skeleton

The order of sections is always the same: types, pure functions, adapters at the end. The model
knows where to add a new element and does not invent a new convention on every change.

### Mechanical conventions

Formatting, import order and layout are enforced by a tool, not by a document and not by good
intentions. The document explains only "why". A rule that cannot be checked mechanically will be
broken under context pressure.

### Comments about traps, not code

A comment does not describe what the code does — that is visible in the code. A comment says why
something is done in an unusual way, what must not be changed, and what trap lurks in that place.
Every module starts with a short header: why it exists, what it receives, what it guarantees. The
agent reads that header before editing and knows what it must not break.

### Feedback loop in one command

Typecheck, tests and lint run with one command and finish within seconds. The agent then has
deterministic feedback and fixes its own mistake instead of guessing. A slow loop or several
commands is an invitation to "I will check it later".

### Property and snapshot tests

Properties ("for any input, X holds") and snapshots pin down behavior the model cannot analyze in
full. A snapshot additionally makes every output change visible in the diff, so an accidental
modification does not pass unnoticed.

### Pinned and minimal dependencies

Every dependency is a surface where the model can hallucinate an API, and a version whose behavior
can change. Versions are pinned, and a new dependency requires a justification. The standard library
beats a package when the difference is small.

### No guessing APIs

Before using an external API, the agent reads the type definitions available in the repository or
the documentation named by the project. It does not reconstruct signatures from memory. If an API
cannot be confirmed, the agent reports that instead of writing code "by feel".

### One purpose per change

One change implements one requirement. No refactor along the way, no renaming unrelated things, no
"while I was here I also fixed". A small diff is reviewable; a large diff hides bugs and makes it
impossible to attribute a regression to its cause.

## Anti-patterns

### Inheritance and class hierarchies

A hierarchy forces reading many files to understand one method and spreads responsibility across
layers. Prefer composition and functions; use inheritance only where the platform requires it.

### Metaprogramming and magic

Macros, dynamic dispatch, behavior-changing decorators, dependency injection containers,
configuration based on naming conventions — all of it is invisible when reading a single file. The
model cannot predict what will happen, so it cannot safely change the code.

### Layers for layers

Every additional layer of abstraction costs context and is one more place to confuse where the logic
belongs. Two, at most three layers. Names like `AbstractFactoryBuilderProxy` are a signal that the
project has slipped out of control.

### `utils` and `helpers` bags

A file without a domain name attracts everything that does not fit anywhere else and becomes
unsearchable. A function belongs in a topical module, or nowhere.

### Flags in parameters

A boolean parameter changes the behavior of a function in a way that is invisible at the call site.
A separate function, a separate path, a separate test.

### Deep nesting

More than two levels of nesting is a signal that early exits or a split into steps are missing. The
model gets lost in nested conditions and confuses the level it is currently at.

### Mutable global state and singletons

Hidden state makes functions nondeterministic and ties the result to call order. State is passed
explicitly.

### Scattered configuration

Behavior driven by an environment variable read in a deep layer cannot be traced. Configuration is
loaded once, at the boundary, and passed on as an argument.

### GoF patterns without payoff

A design pattern is used only when it genuinely reduces context cost, change locality or error
detectability. `Strategy` as a map of functions — yes. `Visitor` and elaborate factories — almost
never. The name of a pattern is not an argument.

## Agent working process

### Find the existing pattern first

Before writing code, the agent looks for how a similar problem was already solved in the repository
and repeats that pattern. Consistency with the local idiom matters more than whether a better
pattern exists elsewhere.

### A new pattern only with a record

If no existing pattern fits, the agent may introduce a new one — but in the same change it adds an
entry to `docs/decisions.md`. Otherwise the repository acquires new, conflicting conventions with
every session.

### Do not guess intent

When a requirement is ambiguous, the agent asks instead of choosing an interpretation. A wrong
assumption is cheaper to catch before the code than after it.

### Do not refactor along the way

A change has one purpose. Unrelated things, even clearly bad ones, are reported, not fixed in the
same diff.

### Leave no TODO

Code with a `TODO` is unfinished. Either the task is done, or it is explicitly reported as not done,
with the reason and consequences.

### Report uncertainty

The agent points out places it has not verified with a test and risks it cannot rule out. Silence
about uncertainty is a report of false certainty.

## Definition of done

A change is done when the test was written before the implementation, went through the red phase and
then the green one, the project check command passes, no claim in the change description is left
without a test reference, and dependencies have not grown without justification.

## Moving rules into tools

A rule that can be checked mechanically is moved into tool configuration. The document describes
"why", the tools enforce "what".

Current state:

- `scripts/check.py` — one command that checks what is checkable without a stack: the presence of
  required files, dead links in documentation, forbidden markers, the file size budget. When a stack
  appears, the same command runs its tests.
- Author preference, not an architectural rule: tooling scripts and tests are in Python, managed by
  `uv`, with tests in `pytest`. A project with its own toolchain keeps it.
- `.githooks/commit-msg` — a commit without a `Test:` or `Unverified: <reason>` line does not exist.
- PR template with the definition-of-done checklist.
- CI on PRs and a required status before merging to `main` — to be enabled together with the first
  stack.

To be enforced in configuration once a stack is chosen:

- strict typing mode, no implicit types, no `any`
- exhaustive variant matching as a compile error
- file size limit
- formatting and import order
- lint run together with tests in one command
- no warnings as a condition of a green loop

## Where to store this knowledge

This document describes **how to write code**. How to move these rules into instruction files for
agents is described in [`docs/instruction-files.md`](instruction-files.md). Decisions about patterns
and their justifications go to [`docs/decisions.md`](decisions.md). How to check whether the rules
actually bind the model is described in [`docs/probes.md`](probes.md).
