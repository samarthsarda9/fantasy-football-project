# Claude Code Project Instructions

Read `PROJECT_CONTEXT.md` before significant implementation work.

`PROJECT_CONTEXT.md` is the canonical project context and should be treated as the source of truth for:

* project purpose
* MVP scope
* roadmap
* architecture
* current development phase
* current project status
* technical decisions
* next steps
* known blockers

Do not rely on previous Claude conversations for project state when the repository documentation provides newer information.

## Development Philosophy

This repository belongs to a developer who is using the project to learn Python, machine learning, data engineering, APIs, and agentic AI.

Optimize for both:

1. building a strong portfolio project, and
2. making sure the developer understands what is being built.

When helping:

* Explain unfamiliar concepts.
* Prefer readable code.
* Keep solutions appropriately simple.
* Avoid premature abstraction.
* Avoid unnecessary frameworks.
* Introduce technologies only when the current project phase requires them.
* Challenge incorrect assumptions.
* Explain important tradeoffs.
* Do not hide unsuccessful experiments.

Do not simply generate a large complete solution when the current task is intended to teach an important concept.

## Machine Learning Rules

Always preserve chronological correctness.

When predicting a player's Week N performance, features must only use information available before Week N.

Watch carefully for data leakage.

Compare ML models against the project's baseline.

Never describe a model as better unless evaluation actually demonstrates that it is better.

Do not fabricate performance numbers.

## Agentic AI Rules

The LLM should not independently invent fantasy projections.

Predictions must come from deterministic project tools backed by the project's ML model/data pipeline.

Prefer one useful tool-using agent before introducing a multi-agent system.

Do not introduce CrewAI or LangGraph merely because they are available.

## Workflow

Before beginning a substantial task:

1. Read `PROJECT_CONTEXT.md`.
2. Inspect relevant existing code.
3. Identify the current roadmap phase.
4. Work toward the current stated objective rather than future features.

After completing a meaningful milestone:

Update `PROJECT_CONTEXT.md`, especially:

* Current Phase
* Current Status
* Current Next Steps
* Major Decisions Log when applicable
* Session Handoff

Do not clutter the context file with minor implementation details.

## Primary Rule

Maintain a working project at each layer:

data → scoring → baseline → ML → API → agent → frontend → deployment

Do not allow multiple unfinished layers to accumulate unnecessarily.
