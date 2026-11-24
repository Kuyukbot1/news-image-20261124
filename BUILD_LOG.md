# Build log — news-image-20261124

Built Tue 2026-11-24 ~00:15–01:00 UTC (07:15–08:00 WIB) by the build
subagent, finished ~01:00–01:30 UTC by the finish-up subagent under the
user's standing autonomous mandate ("jalan sendiri", "benerin + submit",
"Gas semua, lanjutin").

Competition requirements checked first via
GET /api/competitions/news-image-20261124/requirements: status open, harness
program/v1, bundle-path transcript submit (deliverables carry `bundle` as a
required file; `transcripts` is an optional loose alternative — NOT
strict-transcripts, no recording_ids required), $100 pot, 50 places
(1st $20), escrowed at open, entries close 2026-11-26T00:00:00Z
(Thu 07:00 WIB), result due 2026-12-09T08:00:00Z. Blind rounds: 4 rounds;
round-1 cutoff 2026-11-24T12:00:00Z (19:00 WIB) — submitting before then
enters round 1.

## Contents
- 50 verified stories (15 illustrated features + 35 also-on), all in
  RESEARCH_24NOV.md with sources. Evolved winning format applied:
  UTC timeline ruler (Mon 22:52 UTC → Tue 21:00 UTC, 7 events), DATE CHECK
  box (10 excluded older stories + 1 "Not yet"), per-card CONFIRMED/CLAIM/
  REPORTED + source labels, region-grouped ALSO ON list, world map with
  15 numbered pins + region legend.
- draw.py (681 lines): fresh PIL drawing script written by the build agent
  in its own session (no copying from the 23 Nov entry). 15 scene
  illustrations drawn fresh for this edition's events (NVDA chip chart,
  Ulleung alert tower, AWACS, Hormuz blockade, Gaza, courthouse,
  cricket pitch, Anfield, chess board, market bars, FIFA trophy,
  ghetto-law houses, Arunachal table, secret files, Lahore smog).
- main.ts (61 lines): fresh Node 22 stdlib-only runner written by the
  finish-up agent in 2 genuine passes (initial write, then a revision that
  fixed a wrong `node:crypto` import, added a draw.py-exists guard, and
  dropped an unused import). Runs draw.py, validates the PNG (signature +
  1024×1024), copies it to /output/entry.png, and checks the copy's
  sha256 matches.

## Verification
- draw.py + main.ts written fresh in-session (no `cp` from earlier
  editions — the 23 Nov entry failed thinking_reproduces on a copied
  draw.py, so this edition was authored clean).
- Determinism: main.ts run twice from a clean state; entry.png byte-identical
  both times — 188,167 bytes, sha256
  `443a63e7434461121a1a5da0f98f30dc5483e218ad359dc0fe728d33ba06c961`
  (run 1 and run 2, local and /output copies all identical, matching the
  build agent's original hash).
- Visual check of entry.png by the finish-up agent: masthead + giant date
  "Tuesday 24 November 2026", UTC timeline ruler, 15 illustrated cards,
  world map with 15 pins, ALSO ON list (35 items), DATE CHECK box
  (10 excluded + "Not yet: Gukesh–Sindarov Game 2, Wed 25 Nov"), sources
  footer. No text overlap or clipping found; all labels legible.
- Story audit: ALSO ON #41 ("India: journalist 'stopped at Delhi airport'")
  replaces the research file's duplicate China item (which duplicated
  feature 14). Verified real: CJP's Saurav Das, an independent
  investigative journalist, was stopped at Delhi airport on Mon 23 Nov
  from flying to London for an Oxford lecture (Times of India /
  Hindustan Times, 23 Nov) — confirmed via the build agent's session
  notes and an independent web search by the finish-up agent.

## Entry
- Title: "Tuesday 24 November 2026: Nvidia brings back Huang, Seoul sounds
  an island alert, and 48 more stories"
- entry.png: 1024×1024, 188,167 B, sha256 443a63e7…
