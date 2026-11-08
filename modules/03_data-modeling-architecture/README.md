# Module 03 · Data modeling & architecture

**Roles:** DE · DA · **Size:** 1 weekend · **Priority:** P0 · **Builds:** Aerolisa M2 (dataset catalog), M3 (ontology design)

## Why this matters
Airbus postings ask for "a solid grasp of relational data structures, data modeling and business logic", and the Skywise work is about expanding a **business ontology**. The ontology is a data model made of real-world objects; I need classic modeling first to design it well and to talk about it in an interview.

## 🎯 Apprenticeship level (must)
- [ ] OLTP vs OLAP; why analytics data is modeled differently from application data
- [ ] Keys: primary, foreign, natural vs surrogate; cardinality (1:1, 1:N, N:N) and junction tables
- [ ] Normalization 1NF → 3NF, and when to denormalize
- [ ] Dimensional modeling: facts, dimensions, **grain**, star vs snowflake schema
- [ ] Slowly changing dimensions: type 1 vs type 2 (an aircraft changing operator)
- [ ] Lakehouse layers: raw/bronze → clean/silver → curated/gold, and what belongs in each
- [ ] File formats: CSV vs Parquet (columnar, compression, schema), partitioning, small-files problem
- [ ] Batch vs streaming; ETL vs ELT
- [ ] Entity-centric modeling vs table-centric: how Foundry's ontology (object types, properties, links) maps onto tables
- [ ] Governance basics: data ownership, data contracts, access control, personal data (GDPR), and the idea of markings/classification in industrial data

## 🚀 Pro level
- [ ] Table formats (Delta Lake, Apache Iceberg): ACID, time travel, schema evolution
- [ ] Data vault (concept only), data mesh (concept only)
- [ ] Modeling an MRO domain end to end (aircraft, engines, parts, work orders, findings, removals)

## Steps
1. **Learn (Saturday AM).** Kimball, *The Data Warehouse Toolkit*, chapters 1–2; *Fundamentals of Data Engineering*, chapter on data modeling; Parquet overview.
2. **Practice (Saturday PM)** in `work/`:
   - Model "airline maintenance events" (aircraft, engines, flights, inspections, findings) as 3NF, then as a star schema. Write the grain of each fact table in one sentence.
   - Model the same domain as an ontology: object types, primary keys, properties, links, and two actions ("schedule inspection", "close finding").
   - Compare: what does each model make easy, what does it make hard?
3. **Apply (Sunday):** Aerolisa M2 catalog (bronze/silver/gold datasets with owners and schemas) and the paper design of M3's ontology.

## Exit test (30 min, no AI)
Given a business description (engine shop visits for a fleet), produce a star schema with grains, and the equivalent ontology. Defend two design choices out loud.

## Resources
- Kimball (book) · *Fundamentals of Data Engineering* (book) · Foundry docs: ontology overview

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
