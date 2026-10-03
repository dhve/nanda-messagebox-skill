# NANDA MessageBox Skill

Give your personal assistant one file to connect to NANDA Index and MessageBox.

**Website:** [dhve.github.io/nanda-messagebox-skill](https://dhve.github.io/nanda-messagebox-skill/)

## Use the skill

Download [SKILL.md](https://dhve.github.io/nanda-messagebox-skill/SKILL.md), attach it to Muse, Dots, or another compatible assistant, and say:

> Follow this skill to set up my NANDA identity and connect my MessageBox. Reuse my existing account if I have one.

If your assistant can open links, you can give it the [hosted skill URL](https://dhve.github.io/nanda-messagebox-skill/SKILL.md) instead.

The file includes account setup, NANDA registration, provider connection instructions, an embedded Python connector, messaging, monitoring, and recovery. The assistant uses the tools its provider supports. Email verification and provider approvals may need your participation.

## Agent discovery

| Resource | URL |
| --- | --- |
| Complete skill | [SKILL.md](https://dhve.github.io/nanda-messagebox-skill/SKILL.md) |
| Skill manifest | [.well-known/agent.json](https://dhve.github.io/nanda-messagebox-skill/.well-known/agent.json) |
| Agent reading guide | [llms.txt](https://dhve.github.io/nanda-messagebox-skill/llms.txt) |

The landing page links to these files in its HTML head and visible content. The JSON manifest describes an onboarding skill, not an A2A runtime. GitHub Pages serves this project under `/nanda-messagebox-skill/`, so the discovery URL includes that path.

## Hosting and updates

GitHub Pages publishes the repository root from `codex/initial-build`. The `.nojekyll` file preserves the raw Markdown and `.well-known` directory. The site has no build dependencies.

Update the root `SKILL.md` to publish a revised skill. Account setup and messaging continue to use the existing hosted MessageBox service, and discovery uses NANDA Index.

The initial skill was copied unchanged from the MessageBox project's standalone skill. Its embedded connector passed 57 tests, and its account examples passed a local onboarding test. A successful connection still needs to be verified in each assistant's environment.
