# Nanda Agent Box Skill

The hosted file is for personal agents to read and follow:

[https://my.nandaindex.org/agent/SKILL.md](https://my.nandaindex.org/agent/SKILL.md)

The site root redirects to the file. The older account-flow skill stays at [SKILL.md](https://my.nandaindex.org/SKILL.md) for assistants already connected through it; `staging/SKILL.md` is the same agent skill pointed at the staging gateway. Machine-readable discovery is available at [.well-known/agent.json](https://my.nandaindex.org/.well-known/agent.json) and [llms.txt](https://my.nandaindex.org/llms.txt).

GitHub Pages publishes the repository root from `codex/initial-build`. Keep `.nojekyll` so the Markdown file and `.well-known` directory are served unchanged.
