# Module 00 · Launch

**Roles:** all · **Size:** 1 weekend · **Priority:** P0 · **Builds:** Aerolisa M0 (clean slate)

## Why this matters
Applications, accounts and admin take calendar time that no amount of studying can compress. Starting them first means nothing blocks me later. The diagnostic tells me which modules I can move through fast and where my real gaps are.

## 🎯 Apprenticeship level (must)
- [ ] Every account and tool below works
- [ ] Diagnostic done and gap list written
- [ ] Career kit v1 exists (CV EN + FR, LinkedIn, GitHub profile, tracker)
- [ ] TOEIC booked
- [ ] Admin questions sent (CESI, paperwork)

## 🚀 Pro level
- [ ] GitHub profile README with a short "what I build" section and links
- [ ] Anki decks created: `SQL`, `Stats`, `Foundry`, `Aviation`, `Interview`

## Steps

### Saturday: accounts, diagnostic
1. **Tools:** Python 3.11+, VS Code, Git, GitHub, Docker Desktop, Anki (phone + computer).
2. **Accounts:**
   - Palantir **Developer Tier** (build.palantir.com), Palantir Learn (learn.palantir.com), Palantir Community. If sign-up conflicts with an existing Learn account, ask on the community forum.
   - OpenSky Network account, then create an **API client** on the account page (the REST API uses OAuth2 client credentials; keep `credentials.json` out of Git).
   - Kaggle (optional, for datasets and notebooks).
3. **Diagnostic (2 h, closed book, no AI).** Write it as a file in `work/diagnostic/`:
   - Python (30 min): parse a text file into a dict of lists; group and count; write a function with a test; a small class.
   - SQL (30 min): 5 queries on any small table: join, group by + having, a subquery, a window function, deduplication.
   - Statistics (30 min): mean vs median with outliers, standard deviation, conditional probability, what a p-value is, correlation vs causation.
   - ML (30 min): train/test split purpose, overfitting, precision vs recall, what a random forest is, why random splitting C-MAPSS is wrong.
4. Correct it. Write `work/diagnostic/gaps.md`: each gap → module where it gets fixed. Mark modules where I scored ≥ 90% as "fast track" (do the exit test first; if passed, go straight to the Pro level or move on).

### Sunday: career kit and admin
5. **CV v1** in English and French, one page each: education (CESI, programme taught in English, top of class), ALTEN internship (data & AI for recruitment, described without confidential data), SAA predictive maintenance research, skills, languages, Palantir badges. Follow [career/application-kit.md](../../career/application-kit.md).
6. **LinkedIn:** featured section ready for Aerolisa; skills list aligned with [SKILLS_MATRIX.md](../../SKILLS_MATRIX.md).
7. **GitHub:** pin Aerolisa, Renaissance and Turbofan-RUL; repository descriptions and topics filled.
8. **Tracker:** start [career/applications.md](../../career/applications.md) and save Airbus careers searches (see [module 15](../15_interviews-applications/README.md)).
9. **Book the TOEIC** (see [career/languages.md](../../career/languages.md)).
10. **Admin emails:** CESI (final year in alternance confirmed? which RNCP code and rhythm to give employers?), and any paperwork my residence status requires for an apprenticeship contract (ask CESI's international office; start early, it can take weeks).
11. **Aerolisa M0:** follow the M0 steps in Aerolisa's [ROADMAP.md](https://github.com/xdmanflow/Aerolisa/blob/main/ROADMAP.md).

## Exit test
- [ ] I can log in to Foundry Developer Tier and open a project
- [ ] An authenticated OpenSky API call works from a script
- [ ] `gaps.md` exists and maps every gap to a module
- [ ] CV v1 sent to two people for feedback
- [ ] Aerolisa CI is green on `main`

## Resources
- [palantir/README.md](../../palantir/README.md) · [career/](../../career/README.md) · OpenSky REST API docs

## Gaps found
-

## Notes
-

## Work
Notes, diagnostic and answers: [`work/`](work)
