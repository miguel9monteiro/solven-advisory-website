# Solven Advisory Website

Static HTML site for Solven Advisory (AI enablement and implementation for
investment firms, Lisbon). No framework, no build step. Deployed on Vercel
with `cleanUrls` (internal links are extensionless). Brand reference lives in
`BRAND.md` (colours, type, voice); `legacy/` is an old version, ignore it.
`llms-full.txt` is generated from the pages; regenerate it after copy changes.

## Writing rules

- **Em dashes are a big no. Never use an em dash (—) anywhere on this site**:
  not in copy, headings, titles, meta descriptions, JSON-LD, code comments,
  or generated files (`llms.txt`, `llms-full.txt`). Rewrite the sentence with
  a comma, colon, full stop, or restructure it. En dashes and spaced hyphens
  used as dashes are not an acceptable substitute. The middot (·) is the
  house separator for labels ("Lisbon · 2026", "Session one · Foundations").
- Voice (from BRAND.md): considered, not corporate; complete sentences, no
  fragments for emphasis; specific over generic; fewer words when in doubt.
  Banned words: synergy, leverage (verb), value-add, robust, holistic,
  leading, cutting-edge, unlock, ecosystem, journey, delight.
- British spelling (programmes, analyse, organisation).

## Invariants

- Motion: content is visible by default. Hidden states exist only behind
  JS-applied classes (`.pending`, `body.intro-armed`, `html.anim`) with
  timed rescue paths, and `prefers-reduced-motion: reduce` is a hard stop
  for every effect. New motion must follow the same contract (see the
  headers in `solven.js` and the cinematic sections of `solven.css`).

- The three FAQ answers shared between `programmes.html` and `contact.html`
  must stay word-for-word identical, and the FAQPage JSON-LD in
  `programmes.html` must exactly match the visible answer text.
- Canonical origin is `https://solvenadvisory.ai` (apex, no trailing slash;
  the PT page is `/pt`). Every page carries canonical + OG + Twitter meta.
- Never use pure black, never use greens other than the two brand sages,
  never add a third typeface (see BRAND.md).
