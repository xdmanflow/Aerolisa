# ADR 0003: Public data only, never committed

**Status:** accepted, amended Nov. 2026: the public NASA C-MAPSS FD001 files (5.6 MB) are committed for reproducibility of the SAA research; everything else stays out of Git.

**Context:** data licences and repository size.

**Decision:** only public sources; raw data downloaded at runtime; only small samples in Git. Samples of sources whose terms forbid redistribution (OpenSky, Eurocontrol, Airbus) are synthetic. Nothing from an employer, ever.

**Consequences:** reproducible pipelines, no licence issues, fast clones.
