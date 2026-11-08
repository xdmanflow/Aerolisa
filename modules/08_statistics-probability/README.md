# Module 08 · Statistics & probability

**Roles:** DA · DS · **Size:** 2 weekends · **Priority:** P0 · **Builds:** Aerolisa M5 (utilization statistics), M6 (reliability and survival analysis)

## Why this matters
Data analyst and data scientist interviews always include statistics questions, and aviation reliability is applied statistics: failure rates, lifetimes, Weibull curves, censored data. Being able to say "this engine population is in wear-out, β > 1" is what makes a data scientist credible to maintenance engineers.

## 🎯 Apprenticeship level (must)
- [ ] Descriptive: mean, median, mode, variance, standard deviation, quantiles, IQR, outliers, skewness; histograms and boxplots
- [ ] Probability: events, conditional probability, independence, **Bayes' theorem**, base-rate fallacy (why most alerts can be false alarms)
- [ ] Random variables, expectation, variance, linearity of expectation
- [ ] Distributions and when they appear: Bernoulli/binomial (pass/fail), **Poisson** (failure counts), **exponential** (constant failure rate), **Weibull** (wear-out), normal, log-normal
- [ ] Law of large numbers and central limit theorem (intuition + simulation)
- [ ] Sampling, standard error, **confidence intervals**, bootstrap
- [ ] Hypothesis tests: t-test, chi-square, Mann–Whitney; p-values; type I/II errors; power; multiple testing
- [ ] A/B testing logic; correlation vs causation; Simpson's paradox
- [ ] Reliability: hazard rate, bathtub curve, MTBF / MTTR, reliability function R(t)
- [ ] Survival analysis: **censoring**, Kaplan–Meier curves, Weibull fit

## 🚀 Pro level
- [ ] Cox proportional hazards
- [ ] Bayesian updating with conjugate priors (beta-binomial for failure probabilities)
- [ ] Extreme value thinking for rare events

## Steps
**Weekend 1: core statistics**
1. Learn: *OpenIntro Statistics* chapters on summary statistics, probability, distributions, inference foundations; StatQuest on p-values and confidence intervals.
2. Practice: simulate the CLT and a bootstrap CI in NumPy; compute by hand, then in code, 10 classic interview questions (in `work/`).
3. Apply: Aerolisa M5, utilization statistics per airframe (cycles/day distribution, outliers, CI on mean daily cycles).

**Weekend 2: reliability**
4. Learn: lifelines docs (Kaplan–Meier, Weibull fitter); a reliability primer (bathtub curve, MTBF).
5. Practice: treat C-MAPSS training units as failure times and test units as censored; plot Kaplan–Meier; fit a Weibull; interpret β and η.
6. Apply: Aerolisa M6, reliability view of the simulated fleet.

## Exit test (60 min, no AI)
20 interview-style questions (probability puzzles, test choice, interpreting a p-value, Bayes with a base rate), plus: fit and interpret a Weibull on given lifetimes.

## Resources
- *OpenIntro Statistics* · *Think Stats* · StatQuest · lifelines docs

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
