[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Kuyukbot1/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Kuyukbot1/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# Tuesday 24 November 2026: Nvidia brings back Huang, Seoul sounds an island alert, and 48 more stories

Bounty: [news-image-20261124 — "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124)

One 1024×1024 front page summing up Tuesday 24 November 2026 in 50 sourced
stories: 15 illustrated feature cards, a UTC timeline ruler, a DATE CHECK box
of older news left out on purpose, a world map with 15 numbered pins, and a
region-grouped ALSO ON list. Every story was reported on 24 November 2026
(or first reported late on 23 November and carried as Tuesday news); disputed
claims are attributed, never stated as fact. Sources: AP, Reuters, AFP, BBC,
Al Jazeera, UN News, and the outlets named on each card.

## How it is built

- `draw.py` — Pillow script that draws the whole page deterministically
  (fixed content, no clock, no network, no randomness). Run `python3 draw.py`
  to regenerate `entry.png`.
- `main.ts` — Node 22 (stdlib only) entrypoint: runs `draw.py`, validates
  the PNG (signature, 1024×1024), and places a copy at `/output/entry.png`.
- `entry.png` — the submitted image, 1024×1024, byte-identical on every run
  (sha256 `443a63e7434461121a1a5da0f98f30dc5483e218ad359dc0fe728d33ba06c961`).
- `RESEARCH_24NOV.md` — the 50 verified stories with sources, the UTC
  timeline, and the DATE CHECK exclusions.
- `BUILD_LOG.md` — build steps, determinism proof, and verification results.
