# Copilot

> An AIP-style assistant: answers maintenance questions from public-domain documents **with citations**, answers fleet questions through **tools on the Aerolisa API**, and **proposes** actions that a human must confirm.

**Milestone:** M10 (+ AIP Logic twin on the Foundry edition)
**May import:** `aerolisa.core`, `aerolisa.api`, `aerolisa.planner`
**Learn:** Renaissance 13

## Why
Skywise-ecosystem roles now ask for GenAI integrated into analytics (RAG, prompt engineering, agentic workflows), and Palantir's AIP is built on the same idea: LLMs working on the ontology, with actions keeping a human in control. An ungrounded chatbot would hurt the project; a grounded, evaluated one helps it.

## Design
- **Corpus:** public-domain or licence-clean documents only, listed in [corpus_sources.md](corpus_sources.md)
- **Retrieval:** chunks with page references; embeddings + BM25 hybrid; re-ranking
- **Answers:** cite sources; say "not covered by my sources" when retrieval is weak
- **Tools (read-only):** `get_engine`, `get_aircraft`, `rank_inspections`, `explain_engine`
- **Proposals:** `propose_schedule_inspection` returns a draft; the user confirms in the app; only then does the API run the action
- **Logging:** every question, retrieved chunk, tool call and proposal
- **Data rule:** only public data and Aerolisa's simulated objects are ever sent to an external LLM API

## Steps
1. [ ] Corpus selected and listed with licences (M10 step 1)
2. [ ] Ingestion: PDF → text → chunks with page numbers (step 2)
3. [ ] Hybrid retrieval + re-ranking + cited answers + refusal rule (step 3)
4. [ ] 30-question evaluation set; `reports/copilot-eval.md` (step 4)
5. [ ] Two chunking strategies compared (step 5)
6. [ ] Read-only tools on the API (step 6)
7. [ ] Proposal + confirmation flow (step 7)
8. [ ] Copilot page in the app (step 8)
9. [ ] AIP Logic "explain engine risk" on Foundry (step 9)

## Definition of done
- [ ] Eval set answered with citations above my target score
- [ ] Cannot change any data without a human click
- [ ] Architecture diagram + demo segment
