# ADR 0006: Foundry-style transforms

**Status:** accepted

**Context:** the Foundry edition (M4) should reuse the local pipelines, and interviews for Skywise roles will probe Code Repositories transforms.

**Decision:** local transforms are declared like Foundry Python transforms: a decorator with named `Input` datasets and one `Output`, a pure function from DataFrames to a DataFrame, no I/O inside the function. `aerolisa.core` provides the decorator, a registry, and a build runner that orders transforms by topological sort.

**Consequences:** transforms are easy to unit test (pass DataFrames in, check the DataFrame out); porting to `transforms.api` is mostly changing imports and paths; lineage comes for free from the declared inputs and outputs.
