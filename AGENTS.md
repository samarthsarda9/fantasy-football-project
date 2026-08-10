# Codex Repository Instructions

Before performing significant work in this repository, read:

`PROJECT_CONTEXT.md`

Treat `PROJECT_CONTEXT.md` as the project's shared source of truth for:

* project goals
* architecture
* current phase
* roadmap
* technical constraints
* completed work
* next steps
* major decisions

## Working Style

This is both a learning project and a portfolio project.

The developer is learning Python, machine learning, and agentic AI while building the application.

Therefore:

* Prefer clear, simple implementations over clever ones.
* Explain unfamiliar concepts and important design choices.
* Do not add unnecessary abstractions or dependencies.
* Do not skip ahead to future roadmap phases unless explicitly requested.
* Do not automatically build an entire feature when a smaller learning step is more appropriate.
* Point out incorrect assumptions.
* Preserve proper temporal ML evaluation and guard against data leakage.
* Never fabricate model metrics or claim improvement without measured evidence.

## Before Coding

Determine:

1. What phase the project is currently in.
2. What already works.
3. What the immediate next objective is.

Inspect existing code before proposing architecture that may already exist.

## After Meaningful Work

Update the appropriate sections of `PROJECT_CONTEXT.md`, especially:

* Current Phase
* Current Status
* Current Next Steps
* Major Decisions Log, if a durable decision was made
* Session Handoff

Do not update it for trivial changes.

## Scope

The current MVP is intentionally narrow.

Do not introduce additional technologies, positions, data sources, agent frameworks, infrastructure, or features merely because they might eventually be useful.

Build one working layer before adding the next one.
