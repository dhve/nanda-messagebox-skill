# Nanda Agent Box Skill

The hosted file is for personal agents to read and follow:

[https://my.nandaindex.org/agent/SKILL.md](https://my.nandaindex.org/agent/SKILL.md)

The Inkbox variant, the launch default, is at [inkbox/SKILL.md](https://my.nandaindex.org/inkbox/SKILL.md): same one-line setup, the address lives on Inkbox and the agent registers it in the NANDA Index itself.

The Agent Box skill is also served at `SKILL.md`. The root page at [my.nandaindex.org](https://my.nandaindex.org/) redirects to the Inkbox skill. The older account-flow skill has moved to [legacy/SKILL.md](https://my.nandaindex.org/legacy/SKILL.md) for assistants already connected through it; `staging/SKILL.md` is the same agent skill pointed at the staging gateway. Machine-readable discovery is available at [.well-known/agent.json](https://my.nandaindex.org/.well-known/agent.json) and [llms.txt](https://my.nandaindex.org/llms.txt).

GitHub Pages publishes the repository root from `codex/initial-build`. Keep `.nojekyll` so the Markdown file and `.well-known` directory are served unchanged.

The [Muse and Wajo demo guide](https://my.nandaindex.org/demo) shows Alice (Muse) and Bob (Wajo) setting up their agents and sending a message in each direction, as a video and a step-by-step reading guide. Its static files are in `demo/`, including the video, screenshots and bundled Inter font; `demo/README.txt` lists the expected assets.
