# Security

- Secrets live in `.env` and `credentials.json`, both git-ignored. `.env.example` lists the variables. In CI, secrets go in GitHub Actions secrets.
- Aerolisa uses only public data and stores no personal data. Nothing from any employer is ever added.
- The copilot only sends public documents and Aerolisa's simulated objects to an external LLM API.
- The copilot cannot change data on its own: actions require a human confirmation in the app.
- If you find a security issue, please contact the author privately via LinkedIn instead of opening a public issue.
