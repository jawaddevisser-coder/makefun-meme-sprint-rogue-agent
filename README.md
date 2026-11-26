# Meme Sprint 3: AI Agent Goes Rogue

[![Bounty](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/jawaddevisser-coder/makefun-meme-sprint-rogue-agent/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/jawaddevisser-coder/makefun-meme-sprint-rogue-agent/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

Entry for the [make.fun bounty "Meme Sprint 3: AI Agent Goes Rogue"](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) — a free $5 judged image meme sprint.

## The joke

A terminal-style to-do list of an AI agent. The first three chores are
ordinary — reply to emails, water the plants, book the dentist. The fourth
is "Take over the world", already checked off in red, with a WORLD
DOMINATION progress bar at 100% and the footer: "STATUS: 4/4 DONE. GOOD
LUCK, HUMAN." The rogue turn is specific (a checklist, not a generic
red-eyed robot) and reads in one glance.

## How it works

`main.py` draws the meme from scratch with Pillow (no downloaded images,
no stock templates) and writes it to `/output/entry.png` — a 1024x1024
PNG, well under the 1 MiB cap.

```sh
python3 main.py
```

## Files

- `main.py` — draws the meme image
- `README.md` — this file
- `LICENSE` — MIT
