# Module 13 · GenAI, LLMs, agents & AIP

**Roles:** AI · DS · **Size:** 3 weekends · **Priority:** P0 for AI roles, P1 otherwise · **Builds:** Aerolisa M10 (copilot), M4 AIP step

## Why this matters
Airbus opens AI apprenticeships ("LLMs for space engineering", "AI integration") and Skywise-ecosystem roles ask to "integrate GenAI/LLM capabilities (RAG, prompt engineering, agentic workflows) into analytics solutions". Palantir's AIP is exactly that: LLMs working on top of the ontology, with actions and human approval. A grounded, evaluated copilot on aviation data is a strong signal, and an ungrounded chatbot is a negative one.

## 🎯 Apprenticeship level (must)
- [ ] LLM basics: tokens, embeddings, transformer and attention (intuition: Q/K/V, softmax), context window, temperature and sampling
- [ ] Prompt engineering: system vs user instructions, few-shot, structured JSON output with schemas, decomposition, refusing when unsure
- [ ] Calling an LLM API from Python; cost and latency awareness
- [ ] **RAG:** document loading, chunking strategies, embeddings, vector stores (Chroma / FAISS), hybrid search (BM25 + vectors), re-ranking, **citations**
- [ ] **Evaluation:** a labelled question set; retrieval recall; answer correctness and groundedness; LLM-as-judge with its limits; regression testing prompts
- [ ] **Agents:** tool calling, the agent loop, tool design (narrow, typed, read-only first), guardrails, **human-in-the-loop** for any action that changes data
- [ ] Safety in industry: no sensitive or export-controlled data to external APIs; prompt injection basics; logging and auditability
- [ ] **AIP:** AIP Logic (LLM-backed functions on the ontology), AIP Agent Studio, AIP Evals; how actions keep a human in control

## 🚀 Pro level
- [ ] Fine-tuning vs RAG trade-offs; small open models run locally
- [ ] Multi-agent patterns; planning
- [ ] Semantic search with AIP (Palantir developer example)
- [ ] Speedrun: *Your First Agentic AIP Workflow*

## Steps
**Weekend 1: LLMs and prompting**
1. Learn: Hugging Face LLM course (first chapters); attention explained (3Blue1Brown); a provider's prompt engineering guide.
2. Practice: structured extraction of fields from 20 public maintenance texts into a Pydantic schema; measure accuracy against my own labels.
3. Apply: Aerolisa M10 steps 1–2 (corpus of public-domain FAA documents, licences listed).

**Weekend 2: RAG and evaluation**
4. Learn: a RAG course or guide (chunking, hybrid search, re-ranking); one article on RAG evaluation.
5. Practice: RAG with citations; 30-question evaluation set; compare 2 chunking strategies by retrieval recall.
6. Apply: Aerolisa M10 steps 3–5.

**Weekend 3: agents and AIP**
7. Learn: tool-calling docs of my LLM provider; Palantir Learn *Speedrun: Your First AIP Workflow*; AIP Logic docs.
8. Practice: agent with 3 read-only tools on the Aerolisa API + 1 "propose action" tool that needs human confirmation; the same "explain engine risk" logic in AIP Logic on the Foundry edition.
9. Apply: Aerolisa M10 steps 6–9.

## Exit test (90 min, no AI for the written part)
Explain on paper: chunking choices, why hybrid search, how to measure groundedness, how to stop an agent from taking a wrong action. Then run the eval set and defend the score.

## Resources
- Hugging Face LLM course · 3Blue1Brown (attention) · DeepLearning.AI short courses · Palantir AIP docs and speedruns

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
