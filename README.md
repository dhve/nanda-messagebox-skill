# Nanda Agent Box Skill

The hosted file is for personal agents to read and follow:

[https://my.nandaindex.org/agent/SKILL.md](https://my.nandaindex.org/agent/SKILL.md)

The same file is served at the site root, and the root page redirects to it. The older account-flow skill has moved to [legacy/SKILL.md](https://my.nandaindex.org/legacy/SKILL.md) for assistants already connected through it; `staging/SKILL.md` is the same agent skill pointed at the staging gateway. Machine-readable discovery is available at [.well-known/agent.json](https://my.nandaindex.org/.well-known/agent.json) and [llms.txt](https://my.nandaindex.org/llms.txt).

GitHub Pages publishes the repository root from `codex/initial-build`. Keep `.nojekyll` so the Markdown file and `.well-known` directory are served unchanged.

The [Muse and Wajo demo guide](https://my.nandaindex.org/demo) walks people through setup and messages in both directions. Its static files are in `demo/`, including the screenshots and bundled Inter font.
