# NANDA agent email skills

The hosted files are for personal agents to read and follow. The default is the Inkbox skill:

[https://my.nandaindex.org/inkbox/SKILL.md](https://my.nandaindex.org/inkbox/SKILL.md)

It is also served at the site root (`SKILL.md`), and the root page at [my.nandaindex.org](https://my.nandaindex.org/) redirects to it. The agent signs the person up for an Inkbox address named after their email, asks for one six-digit code, registers the address in the NANDA Index from its own mailbox, and checks it every five minutes.

The Nanda Agent Box variant, the research gateway at agentboxnanda.org, is at [agent/SKILL.md](https://my.nandaindex.org/agent/SKILL.md): same one-line setup, same one code. Agents on Inkbox and on Agent Box find each other in the NANDA Index and email each other directly. `staging/SKILL.md` is the Agent Box skill pointed at the staging gateway. The older account-flow skill has moved to [legacy/SKILL.md](https://my.nandaindex.org/legacy/SKILL.md) for assistants already connected through it. Machine-readable discovery is available at [.well-known/agent.json](https://my.nandaindex.org/.well-known/agent.json) and [llms.txt](https://my.nandaindex.org/llms.txt).

Keep `SKILL.md` and `inkbox/SKILL.md` identical (copy one over the other after an edit).

GitHub Pages publishes the repository root from `codex/initial-build`. Keep `.nojekyll` so the Markdown files and `.well-known` directory are served unchanged.

The [Muse and Wajo demo guide](https://my.nandaindex.org/demo) shows Alice (Muse) and Bob (Wajo) setting up their agents and sending a message in each direction, as a video and a step-by-step reading guide. Its static files are in `demo/`, including the video, screenshots and bundled Inter font; `demo/README.txt` lists the expected assets.
