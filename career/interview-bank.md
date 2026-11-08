# Interview bank

Write every answer **myself, first, without AI**, in `modules/15_interviews-applications/work/answers/`. Then say it out loud. A question is "ready" when I can answer it in under 2 minutes without notes.

## Motivation & fit
1. Tell me about yourself.
2. Why Airbus? Why this team?
3. Why data / why Skywise / why Palantir Foundry?
4. What do you know about Skywise? Who uses it and for what?
5. Which of Airbus's values speaks to you, and when did you act on it?
6. Where do you see yourself after the apprenticeship?
7. Why should we pick you over another student?
8. What's the hardest thing you've learned on your own?

## Behavioural (answer with STAR, see [stories.md](stories.md))
9. A time you had to learn a tool very fast.
10. A project that failed or was cancelled. What did you do?
11. A disagreement with a colleague or stakeholder.
12. A time you delivered something a non-technical person used.
13. A time you found an error in data or in someone's numbers.
14. A time you had too much to do. How did you prioritise?
15. A time you showed initiative nobody asked for.

## Python
16. List vs tuple vs set vs dict: when each? Time complexity of lookups?
17. What does a decorator do? Write one that times a function.
18. Mutable default arguments: what's the bug?
19. Generators: what and why?
20. pandas: `merge` vs `join` vs `concat`; `apply` vs vectorized operations.
21. How do you test a function that transforms a DataFrame?
22. Live: group a list of records by key and count; deduplicate keeping the latest.

## SQL
23. `WHERE` vs `HAVING`.
24. `INNER` vs `LEFT` join; what happens to rows without a match; anti-join.
25. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`.
26. Find the second highest value per group.
27. Running total and 7-day moving average.
28. Detect consecutive days with the same status (gaps-and-islands).
29. Why did this join double my row count?
30. `UNION` vs `UNION ALL`. `COUNT(*)` vs `COUNT(col)`.
31. What's an index; when doesn't it help?

## Data engineering & modeling
32. ETL vs ELT; batch vs streaming.
33. Star schema; what's the grain of a fact table?
34. Slowly changing dimension type 2: how and why?
35. Why Parquet over CSV?
36. What makes a pipeline idempotent? Why does it matter?
37. How do you handle a late-arriving or corrected source file?
38. Which data-quality checks would you put on flight data?
39. Spark: transformation vs action; what is a shuffle; when to broadcast a join?
40. Spark: why are Python UDFs slow?
41. A pipeline produced half the usual rows overnight. Walk me through your investigation.

## Palantir Foundry
42. What is the Ontology, and how is it different from a set of tables?
43. Object type, link type, action type: define each with an aviation example.
44. Pipeline Builder vs Code Repositories: when do you pick which?
45. What is a dataset transaction? Snapshot vs append.
46. How do you find why a dataset is stale or broken? (lineage, build logs, health checks)
47. What is Workshop for? Describe an app you built.
48. What is a Function in Foundry, and where would you use TypeScript?
49. What is AIP Logic? How does an action keep a human in control?
50. What did you build on Foundry, and what was hard?

## Statistics
51. Mean vs median; when does it matter?
52. What is a p-value? What isn't it?
53. Type I vs type II error in the context of maintenance alerts.
54. Bayes: a test with 99% sensitivity on a rare failure. What's the chance an alert is real?
55. Confidence interval: interpret one correctly.
56. Correlation vs causation, with an aviation example.
57. What does a Weibull shape parameter β > 1 tell you?
58. What is censored data and why can't you just drop it?

## Machine learning
59. Bias vs variance; how do you spot overfitting?
60. Why is a random train/test split wrong on C-MAPSS?
61. Random forest vs gradient boosting.
62. Precision vs recall: which matters more for engine alerts, and why?
63. How do you pick a classification threshold?
64. What is data leakage? Give two examples.
65. How do you explain a prediction to a maintenance engineer?
66. How would you know a deployed model is degrading?

## Predictive maintenance & domain
67. Explain RUL. How did you label it, and why clip it?
68. What are the three ways to frame predictive maintenance as an ML problem?
69. Why give a RUL with an interval?
70. What's the business value of turning unscheduled removals into scheduled ones?
71. What's an AOG? An MEL? An ATA chapter?
72. What would change in Aerolisa with real airline data?

## GenAI
73. How does RAG work? Why not just fine-tune?
74. How do you evaluate a RAG system?
75. How do you stop a copilot from taking a wrong action?
76. What data must never be sent to an external LLM API in aerospace?

## Questions I ask them (pick 3)
- What does a typical week look like for the apprentice on this team?
- Does the team build on Skywise, or mainly consume Skywise products? Which Foundry tools do you use most?
- What would make this apprenticeship a success for you after one year?
- Who are the main users of what the team builds?
- What's the biggest data challenge the team has right now?
- How did previous apprentices continue after the apprenticeship?

## Video-interview checklist (score each answer 0–2)
- [ ] Answer starts with the point in the first sentence
- [ ] STAR structure for behavioural questions; a number or concrete result at the end
- [ ] 60–90 seconds
- [ ] Eye contact with the camera, good light, quiet room, neutral background
- [ ] No filler loops ("so, basically…")
- [ ] Ends cleanly, no trailing "yeah…"

**Pass: ≥ 80% of the maximum score across 5 answers.**
