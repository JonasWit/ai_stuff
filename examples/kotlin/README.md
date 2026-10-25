# Golden example: TimerEngine (Kotlin)

A model of a pure core in Kotlin, copied unchanged from the `workoutbase` project.

## What it shows

- **Immutable state** — `TimerState` and `TimerConfig` are `data class`es, and every operation returns
  a new state instead of changing the existing one.
- **Time as an argument** — `tick(state, deltaMillis)` does not read a clock, so tests do not need
  real time.
- **Closed variants** — `TimerPhase` and `TimerCue` are enums, and the `when` in the engine is
  exhaustive; a new variant is a compile error, not a silent gap.
- **Validation at the boundary** — `TimerConfig` checks ranges in `init`, so the core does not repeat
  the same conditions further down.
- **A result as a value** — `TimerTransition` returns a new state together with the list of cues to
  play; the core does not know that sound or vibration exist.
- **Tests as a specification** — test names are sentences about guaranteed behavior, one test
  corresponds to one rule, zero mocks.

## How to read it

Start with `TimerEngineTest.kt`, then `TimerEngine.kt`. The tests say what the timer must do; the
implementation shows how to build that without side effects.

## What this directory does not do

It is not built or run in this repository. There is no Kotlin toolchain here — the files are a
reference for reading and copying. To run them you need a Kotlin project with JUnit, such as
`workoutbase`.

## Origin and maintenance

The files come from the `workoutbase` application (package `com.wtk_apps.workoutbase.timer`). When the
rules in [`docs/rules.md`](../../docs/rules.md) change, check whether the example still illustrates
them; if it does not, fix the example in the same change.
