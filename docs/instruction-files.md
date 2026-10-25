# Storing knowledge in agent instruction files

## Why this document

This document describes how to move knowledge about architecture and code style into the files an
agent reads automatically. The substantive rules live in [`docs/rules.md`](rules.md); here we cover
only distribution: **what goes where, in what form, and what makes it checkable**.

The starting point is uncomfortable: an instruction file is not documentation. Nobody reads it for
pleasure. The model reads it in full, once, at the beginning of a session, and then works under
limited context. A document that requires careful reading is a document that will not work.

The assumptions about model attention in this document are provisional. There are no measurements
here — just practice and conclusions drawn from it. Every such assumption that can be checked with a
probe from [`docs/probes.md`](probes.md) is waiting to be checked, not believed. There is also no
length threshold: line count is a fact, not proof that rules stop working.

## Overarching principle

**An instruction is not documentation.** Documentation explains. An instruction commands and gives a
way to verify. A sentence that cannot be verified is ballast in an instruction — it takes up space
and lowers the weight of the remaining sentences.

Practical consequence: justification, examples and philosophy live in `docs/`. The instruction file
keeps only what must be in context from the first second.

## Three levels

### Global level

The user's instruction file in the harness configuration directory: `~/.claude/CLAUDE.md` (Claude
Code), `~/.config/opencode/AGENTS.md` (OpenCode), `~/.codex/AGENTS.md` (Codex),
`~/.gemini/GEMINI.md` (Gemini CLI). It enters the context in every project. A place for universal,
stack-independent rules: test discipline, core purity, working process, communication rules. Nothing
that concerns one project.

Selection criterion: only what applies in every project goes here. Every line costs in every session
and lowers the weight of the other rules, so a rule about one project is a mistake here. There is no
fixed length threshold — whether a file is too long is decided by whether the rules in its lower
sections still pass the probes, not by line count.

### Repository level

`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or another file the harness reads in the repository root. It
enters the context when working in that repository. A place for: directory structure, commands
(test, check, build), stack specifics, references to the knowledge documents, local tightening of
global rules.

Selection criterion: only what cannot be inferred from the code — structure, commands, local
tightening, links to the knowledge documents. When the file grows, the content moves to `docs/`, and
a link plus a summary stay in the file. There is no fixed length threshold: what measures it is the
effectiveness of the rules, not line count.

### Knowledge level

The `docs/` directory: `rules.md`, `decisions.md`, `probes.md`, this file. It is not loaded
automatically, so it **must be linked from the instruction file, in its first section**. Knowledge
without a link leading to it does not exist for the model.

Here you may be long, because here you arrive deliberately, on request.

### Skills layer

Procedures loaded on demand: "how to add a new pattern", "how to audit the rules". Advantage — they
do not consume context until needed. Disadvantage — they must be invoked, so they are unsuitable for
rules that must always apply. Critical rules stay in instruction files; skills are for activities,
not prohibitions.

## What goes where

| Content | Location | Why |
| --- | --- | --- |
| Test before code, no claims without evidence | global | applies in every project |
| Pure core, effects at the edges | global | stack-independent |
| Test/check/lint commands | repository | depend on the project |
| Directory structure and naming conventions | repository | local knowledge |
| Justifications and examples | `docs/` | too long for startup context |
| Decisions about patterns | `docs/decisions.md` | history, not instruction |
| Procedure for a rare activity | skill | loaded on demand |
| User preferences about communication | global | project-independent |

## A form that works

### Imperative and one rule per point

"Write the test before the code" works. "It should be considered whether, in a given case, it would
be reasonable to begin work by writing a test" does not. One rule per point, no multi-sentence
paragraphs.

### Most important first

The first dozen or so lines carry the most weight. If the context is truncated or summarized, what
survives must be the prohibitions, not the philosophy.

### Falsifiability

Every rule should answer the question "how will I know it was broken". A rule without such a
criterion is a wish.

### Fixed section order

The established order: verification and tests, project rules, working process, language and
communication. The model learns the layout and finds the right fragment faster. Changing the order
on every edit destroys that benefit.

### No adjectives without a criterion

"Clean code", "professional", "solid", "following best practices" — every model understands them
differently and none can be checked. Instead: a concrete condition and a way to verify it.

### One rule, one place

The same principle in a global file, a repository file and `docs/` is three versions that will
diverge over time. The rule: canonical source in `docs/`, summary in the instruction file, no copies
of the full text.

## What not to do

### Do not count on the model opening `docs/`

The file is not loaded automatically. Without a link at the top of the instruction file, the
knowledge in `docs/` is unavailable, even though it formally exists.

### Do not mix languages in instruction files

One language per file. Mixing makes the model answer in a random language, and edits produce hybrid
sentences. This repository uses English for every document, instruction file and commit message.

### Do not write rules you cannot check

A rule without a verification mechanism is decoration, and decoration teaches the model that rules
are not binding.

### Do not duplicate full content

A summary in the instruction file and the source in `docs/`. A copy of the full content in two
places is guaranteed contradiction.

### Do not mix tooling preferences with architecture

The choice of language for scripts, test framework or package manager is a preference, not an
architectural rule. It may be mentioned in an instruction file, but it must be labeled as such.
Otherwise a project inherits the idioms of one stack as universal law, and when the technology
changes, the rules lose meaning together with the tool.

Architecture describes properties: a pure core, one validation boundary, explicit variants. Language
only provides the way to write them down.

### Do not leave dead rules

A rule that has not been used or broken for months takes up context and dilutes the rest. An audit
also means deletion.

## Instruction files across harnesses

### Rules belong to the project, not the tool

What is shared is the content: verification requirements, architectural properties, working process,
prohibitions. The harness determines only transport: the file name, its location and the way extra
content is included. Changing tools should not change a single rule.

Practical consequence: keep one source of content and thin adapters. An adapter contains no rules —
it points to the source. A copy of the content in a second file is guaranteed divergence, not
support for a second tool.

### Where the instruction file goes

| Harness | Project file | Global file | Including shared content |
| --- | --- | --- | --- |
| Claude Code | `CLAUDE.md`; since v2.1.277 it also reads `AGENTS.md` | `~/.claude/CLAUDE.md` | `@AGENTS.md` inside `CLAUDE.md` |
| OpenCode | `AGENTS.md` (`CLAUDE.md` as fallback) | `~/.config/opencode/AGENTS.md` | the `instructions` field in `opencode.json` |
| Codex | `AGENTS.md` or `AGENTS.override.md` | `~/.codex/AGENTS.md` | directory hierarchy |
| Cursor | `AGENTS.md` or `.cursor/rules/*.mdc` | User Rules in settings | `AGENTS.md` in the repository root |
| GitHub Copilot | `AGENTS.md` or `.github/copilot-instructions.md` | personal instructions in the IDE | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` (the name is configurable) | `~/.gemini/GEMINI.md` | `@file.md` |

The table contains examples, not a closed list. A new harness can usually be connected without
changing the rules: check its documentation for the file it reads and whether it can include an
existing one.

Sources: [Claude Code](https://code.claude.com/docs/en/memory),
[OpenCode](https://opencode.ai/docs/rules/),
[Codex](https://developers.openai.com/codex/agent-configuration/agents-md),
[Cursor](https://cursor.com/docs/context/rules),
[Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions),
[Gemini CLI](https://geminicli.com/docs/cli/gemini-md/).

### What moves unchanged

- Verification requirements: test before code, an observed red phase, no claims without evidence.
- Code properties: a pure core, validation at the boundary, closed variants, errors as values.
- Process: one change, one purpose; a new pattern with a decision-log entry; asking instead of
  guessing.
- Project commands: test, check, lint — as long as the harness can run them.

### What is harness-specific

- File and configuration directory names.
- The inclusion syntax: `@file`, the `instructions` field, imports in `GEMINI.md`.
- The mechanism for permissions, hooks and sandboxes. The rule "the agent cannot perform this
  operation" has a different implementation in every tool; only the intent is shared.
- Built-in tool names and the way subagents are invoked.

These elements stay in the instruction file of the given harness or in its configuration. They do
not move into the canonical source, because the source must apply regardless of the tool.

### An adapter without duplication

When a harness reads its own file and the shared content lives in `AGENTS.md`, the adapter should be
empty of content:

- an import, if the harness supports it — for example a `CLAUDE.md` containing `@AGENTS.md`
- a symbolic link, if the team works only on systems that support them; on Windows this requires
  elevated privileges or Developer Mode
- one sentence, "read `AGENTS.md` before working", when nothing more is available — the weakest
  version, because it depends on the model's decision

In this repository [`CLAUDE.md`](../CLAUDE.md) is exactly such an adapter: it contains an import and
not a single rule.

### Shared traps, independent of the tool

- **One file per directory wins.** When a directory contains two independent instruction files, the
  harness picks one according to its own precedence. The other becomes dead. Hence an adapter, not a
  copy.
- **Load order differs between tools.** Do not assume that the global file is superior or that a
  file in a subdirectory overrides the root one; check the harness documentation.
- **A size limit truncates silently.** Codex has a default 32 KiB limit on combined files, and
  Claude Code recommends keeping instruction files under 200 lines. The most important rules go at
  the top.
- **Context compaction removes unused content first.** A short file with prohibitions at the start
  survives a long philosophy at the end.
- **A subagent does not inherit the conversation.** It inherits the instruction file if the harness
  decides so. Repeat the rules critical to the task in the subagent prompt.

### Verifying that the harness actually reads the rules

Do not assume — check. The method depends on the tool:

- Claude Code: `/context` or `/memory` lists the loaded memory files.
- Codex: `codex ... "List the instruction sources you loaded."`
- Gemini CLI: `/memory show`.

The shared principle: if you cannot point to evidence that the file was loaded, treat the rule as
inactive.

## The enforcement ladder

Each rung has more power. A rule should stand as low as possible, but not lower than its stakes
require.

- **Prose** — the model may skip it. Enough for preferences and judgments.
- **Checklist** — requires the agent to go point by point. Works until someone ticks without thinking.
- **Command** — one command gives raw output. The agent must show it.
- **Hook** — a commit without the required field does not exist. A workaround exists, but it is visible.
- **CI** — the result blocks the merge, regardless of the goodwill of the model or the human.
- **Required status and branch protection** — red does not get in, even through `--no-verify`.
- **Permissions** — the agent physically cannot perform the operation. The strongest, the most inconvenient.

A test rule belongs at least at the command rung. A rule about commits belongs in a hook. A rule
about merging — in CI and branch protection.

## Instruction file template

The skeleton below is a starting point for a new repository. The section order is part of the
contract.

```markdown
# Agent Instructions

Read docs/<rules>.md before writing code.

## Verification and tests

- Test before code, no exceptions except changes with no executable behavior.
- Watch the test fail before implementing.
- No claim without a test; otherwise mark it "unverified".
- Run `./scripts/check` and paste the raw output.

## Design rules

- Pure core, side effects in thin adapters.
- Closed types with exhaustive matching.
- One source of truth per rule, one name per concept.
- No inheritance, no metaprogramming, no DI containers.

## Working process

- Follow the existing pattern in this repository.
- Document a new pattern in the same change.
- Ask when the requirement is ambiguous.
- One change, one purpose.

## Structure and commands

- Test command: ...
- Check command: ...
- Source layout: ...

## Precedence

Global instructions provide defaults. This file tightens them. When they conflict, the more
specific and more restrictive rule wins; this file may not loosen a global rule.
```

## Validation checklist

Before treating an instruction file as ready, check:

- Do the first dozen lines contain the rules whose violation is the most expensive?
- Does every rule say how to recognize that it was broken?
- Does no rule require reading another file to understand it?
- Is every longer piece of content in `docs/`, with a link at the top of the instruction file?
- Is there no duplicate of the full content in two files?
- Do the commands given in the file actually exist and pass in a fresh clone?
- Does every line earn its place, that is, is violating it more expensive than keeping it in context?

## Maintenance

Changing a rule means changing the canonical source plus, if needed, the summary. A new pattern is
recorded in [`docs/decisions.md`](decisions.md). Rule effectiveness is checked with the probes from
[`docs/probes.md`](probes.md). A rule that fails a probe must move to a higher rung of the
enforcement ladder or be deleted.
