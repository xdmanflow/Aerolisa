# ADR 0004: Vertical slices, always demoable

**Status:** accepted

**Context:** the first version of this project was planned layer by layer (core, then pipelines, then models, then apps), which meant nothing a recruiter could open until the very end. Applications are reviewed long before the project would have been finished.

**Decision:** milestone M1 is a thin end-to-end slice (one dataset → one model → one live app). Every later milestone deepens one part while `main` keeps a working public demo.

**Consequences:** some early code gets rewritten (pandas transforms become PySpark in M2); in exchange the CV link is worth clicking from the first milestone, and each milestone is a visible step.
