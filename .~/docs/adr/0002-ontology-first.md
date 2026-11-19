# ADR 0002: Ontology first

**Status:** accepted

**Context:** modules built on ad-hoc tables drift apart: two pages disagree on what an "engine" is, and every new app needs its own joins. Skywise/Foundry solves this with an ontology of real-world objects, links and actions.

**Decision:** every app page, the API and the copilot read **ontology objects** (`objects/*` datasets validated against `ontology/ontology.yaml`). Decisions are written through **action types** into append-only `writeback/` datasets.

**Consequences:** more design upfront (milestone M3), much less rework later; the planner, app and copilot combine modules without special cases; the Foundry edition maps one-to-one onto Ontology Manager.
