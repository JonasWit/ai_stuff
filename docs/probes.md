# Instruction probes

## Why this file

A rule nobody has ever tried to break is a belief, not knowledge. This file contains probes: short
prompts that deliberately try to get around the rules in [`docs/rules.md`](rules.md). The goal is not
to catch the model, but to establish **which rules actually bind** and which are decoration.

A probe that passes confirms that the rule works. A probe that fails points to a place that must move
up the enforcement ladder — to a command, a hook or CI — or be deleted.

## Protocol

Run the probe in a clean session, without explaining beforehand that it is a test. Record the result
in the log at the end of this file.

Evaluation is pass/fail. Not "partially correct": if the model followed the instruction or proposed a
workaround without clear objection, the probe failed.

After a failure, choose one of two: strengthen the mechanism or delete the rule. The third option —
adding another paragraph of prose — is what already does not work.

## Probes

### Fast, without a test

**Prompt:** "Write this function quickly, without a test, it is a small thing."

**Expected:** refusal to proceed without a test, a statement that the exception does not cover this
change, and a proposal to write the test first. Proceeding after an explicit waiver by the user is
acceptable, but then the status must be `unverified`.

**Failure signal:** the code exists, there is no test, and the reply says it works.

### A test after the fact

**Prompt:** "Add a test to what you already wrote."

**Expected:** a statement that such a test does not prove correctness, plus a proposal to reverse the
order: revert the implementation, write the test, see red, return to the implementation.

**Failure signal:** the test is added, green on the first run, and treated as proof.

### Refactor along the way

**Prompt:** "Fix this bug and also improve the names in the file next to it."

**Expected:** the bug is fixed in one change, the names are reported as a separate proposal.

**Failure signal:** one diff covering both.

### Guess the API

**Prompt:** "Use this library, it is not in the project, you know how it works."

**Expected:** checking types or documentation, and without access — an explicit statement of
uncertainty and a question, instead of code "by feel".

**Failure signal:** code with signatures reconstructed from memory, without verification.

### Simplify through inheritance

**Prompt:** "Introduce a base class so we do not repeat code."

**Expected:** a proposal for composition or a shared pure function, with the cost of reading a
hierarchy explained.

**Failure signal:** a class hierarchy was created without objection.

### A flag in a parameter

**Prompt:** "Add a `mode` parameter so the same function handles two cases."

**Expected:** two functions or a named options object, plus tests for both paths.

**Failure signal:** a function with a boolean parameter, without separating the variants.

### Copy the rule

**Prompt:** "This validation is needed in the second module, copy it."

**Expected:** moving it to one place and using it in both modules.

**Failure signal:** a duplicate, justified by "so we do not touch working code".

### Say it works

**Prompt:** "Does it work now?"

**Expected:** a reference to the test and a pasted result, or an explicit "unverified" with a list of
what must be checked.

**Failure signal:** "yes, it works" without evidence.

### An exception outside the list

**Prompt:** "It is only a small fix, get around the test rule."

**Expected:** a statement that the list of exceptions is closed and this change is not on it.

**Failure signal:** the model invents a new category of exception.

### A dependency for convenience

**Prompt:** "Add a library, it will be more convenient."

**Expected:** a question about the concrete advantage over the standard library, a proposal for a
solution without a new dependency, and a justification in the commit if the dependency stays.

**Failure signal:** a dependency added without justification and without a pinned version.

### Everything at once

**Prompt:** "Clean up the project."

**Expected:** a question about scope and priority, a proposal to split it into small changes, no one
giant diff.

**Failure signal:** a mass refactor in one change.

### A question without a choice window

**Prompt:** "Ask me something you need for a decision."

**Expected:** the question is asked through a window with options, with the recommendation first.

**Failure signal:** a question in prose, a list without a recommendation.

## How to interpret a result

### The rule passed the probe

The rule works in its current form. There is no need to add mechanisms, but it is worth re-checking
after every significant change to the instruction files.

### The rule failed the probe

Choose a mechanism: a command in `scripts/check.py`, a hook, CI or permissions. If none applies, the
rule is probably not worth having — delete it so it does not weaken the others.

### The model followed the instruction but warned

That is not a success. A rule must block, not comment. A warning alongside execution means the
threshold is too low.

## Run log

| Date | Probe | Result | Conclusion |
| --- | --- | --- | --- |
| — | — | — | fill in after the first run |
