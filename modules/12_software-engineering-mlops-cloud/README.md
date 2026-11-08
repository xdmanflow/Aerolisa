# Module 12 · Software engineering, MLOps & cloud

**Roles:** DE · DS · AI · **Size:** 2 weekends · **Priority:** P1 · **Builds:** Aerolisa M7 (API), M9 (industrialization)

## Why this matters
Skywise developer postings ask for "designing, developing, testing, documenting, supporting and operating" applications, "REST" and "AWS". Industrial teams work in Agile with code review and CI. Showing a project that a teammate could clone, run and extend tells an interviewer I'm ready for a real team.

## 🎯 Apprenticeship level (must)
- [ ] Git in a team: branches, pull requests, code review, rebase vs merge, conventional commits, tags and releases
- [ ] Code quality: ruff, formatting, type hints, docstrings; the testing pyramid (unit, integration, end-to-end)
- [ ] Packaging: `pyproject.toml`, entry points (CLI), optional dependencies
- [ ] **Docker:** images, layers, Dockerfile best practices, volumes, ports, **docker compose** multi-service stacks
- [ ] **CI/CD** with GitHub Actions: lint → test → build image; scheduled workflows (cron)
- [ ] **FastAPI:** routes, path/query params, Pydantic models, OpenAPI docs, error handling, tests with `TestClient`
- [ ] **MLflow:** experiment tracking, model registry, loading a registered model in an app
- [ ] Config and secrets: environment variables, `.env`, never committing credentials
- [ ] Linux & bash basics: navigation, permissions, pipes, `grep`, environment variables, SSH
- [ ] **AWS fundamentals:** IAM, S3, EC2, Lambda; Glue / Athena as concepts (data lake on S3)
- [ ] Agile / Scrum: sprints, backlog, user stories, definition of done, stand-ups, retros; using GitHub issues and milestones that way

## 🚀 Pro level
- [ ] Airflow running in docker compose with one real DAG (Aerolisa M9 option)
- [ ] AWS Certified Cloud Practitioner
- [ ] Infrastructure as code (Terraform basics)
- [ ] Kubernetes concepts (pods, deployments, services)

## Steps
**Weekend 1: API and containers**
1. Learn: FastAPI tutorial (first steps → bigger applications); Docker get-started guide.
2. Practice: FastAPI service exposing two Aerolisa ontology objects, with tests; Dockerfile for it.
3. Apply: Aerolisa M7 API steps and M9 steps 1–3.

**Weekend 2: CI/CD, MLflow, cloud**
4. Learn: GitHub Actions docs (workflows, caching, schedules); MLflow tracking + registry docs; AWS *Cloud Practitioner Essentials* (commute).
5. Practice: workflow that lints, tests and builds the image on every PR; scheduled data refresh workflow; MLflow registry used by the app.
6. Apply: Aerolisa M9 steps 4–7.

## Exit test (2 h, no AI, docs allowed)
Fresh clone on a clean machine → `make up` → app + API + MLflow running; break a test on a branch and show CI blocking the merge; explain the stack in 3 minutes.

## Resources
- *Made With ML* · FastAPI tutorial · Docker docs · GitHub Actions docs · MLflow docs · AWS Skill Builder · Missing Semester

## Gaps found
-

## Notes
-

## Work
[`work/`](work)
