# CLAUDE.md — Solven Advisory Website

This file is the source of truth for building the Solven Advisory marketing site.
Read it before writing any code. When in doubt, prefer restraint.

## What we're building

A small marketing website for Solven Advisory — an AI strategy advisory for
private equity firms in Portugal. The site exists to (a) make Solven look
credible to a partner at Quest Capital opening it on their phone, and (b)
give them a way to get in touch. That's the job. Anything beyond that is scope creep.

## Stack

- **Astro** (zero-JS by default; this is intentional — do not add React, Vue, or any client framework)
- **Plain CSS** with custom properties from `design/tokens.css`
- **No CSS framework.** Not Tailwind, not Bootstrap, not Pico. The brand is
  restraint; the styling should be hand-written and small.
- **No JavaScript** unless absolutely necessary. If you reach for JS, ask first.
- Deployed to Vercel.

## Pages

- `/` — Home. Hero (wordmark, one sentence about what Solven does, contact link)
  above the fold, followed by the "Where we work" section: four service
  pillars in a 2×2 grid mapping to different buyers inside a PE firm
  (deal team, portfolio team, CFO, managing partner). Below-the-fold
  scroll is intentional; visitors who care will scroll. Don't add a
  third home section without a strong reason.
- `/about` — Two short paragraphs. Miguel Monteiro and his co-founder
  (currently in stealth — do not name the second founder anywhere on
  the site or in any structured data). Where the firm is based. No
  team grid, no headshots in v1.
- `/approach` — The "augmentation without cognitive atrophy" thesis, three short sections.
  This is the only page with substantive prose.
- `/contact` — Email address. That's it. No form in v1.

That's four pages. Do not add a blog, a news section, a case studies page, or a
careers page unless explicitly asked. Resist the urge to fill space.

## Voice (when writing copy)

- **Considered, not corporate.** Direct, not blunt.
- Complete sentences. No fragments for emphasis. No em-dashes used as drama.
- Never use: synergy, leverage (as a verb), value-add, robust, holistic, leading,
  cutting-edge, world-class, best-in-class, unlock, ecosystem, journey, delight.
- Never start a sentence with "We are passionate about" or "Our mission is."
- Specific over generic. "We've worked with PE firms in Lisbon, Porto, and Madrid"
  beats "We work with leading firms across Iberia."
- When in doubt, fewer words.

## Visual rules (read these twice)

- **The brand has three colours.** Charcoal, two sages, bone. That's it.
  No blues, no golds, no greys other than the ones in tokens.css.
- **Bone (#F4F2EB) is the page background.** Not white. White is reserved for form
  inputs and code blocks if absolutely needed.
- **The chevron is the only sage-coloured element on any given screen.**
  Don't make buttons sage. Don't make links sage. Don't put sage rules on bone
  panels for "visual interest." The chevron carries the colour; everything else
  is charcoal on bone.
- **Generous whitespace.** Default page padding is the equivalent of two H1 line-heights.
  When something looks too sparse, leave it.
- **Hairlines, not borders.** Dividers are 0.5px in `--rule-grey`. No 1px borders, no
  shadows, no rounded corners larger than 4px (and prefer 0px).
- **No animations on page load.** No fade-ins, no slide-ups, no parallax. The site
  should feel like a printed page that happens to be on the web.
- **No hover effects on body text.** Links can change colour on hover (charcoal → sage deep)
  and that's the only interaction.

## Typography

System fonts only — Georgia (serif) and Calibri (sans). See BRAND.md for the
hierarchy. Do not import Google Fonts. Do not use @font-face. The site renders
the same on every device or it doesn't ship.

For body copy on screen, set Calibri at 17px minimum (1.0625rem). The brand doc
says 11pt for print; web needs more.

## Logos

All five lockups are in `logos/`. Use them as `<img>` tags or inline SVG.
Never typeset "Solven" by hand in HTML — always use the SVG. The chevron is a
fixed vector path, not a Georgia letter, and Word/browsers render it differently.

- Header navigation: `03_solven_horizontal_lockup.svg`
- Hero: `01_solven_primary_lockup.svg`
- Footer: `02_solven_reversed_lockup.svg` (on a charcoal panel)
- Favicon: see `favicons/` directory

## Icons

If icons are needed, use only the curated set in `icons/`. These are from Lucide
(MIT licensed) and are pre-styled for the brand. Do not import lucide-react or
any other icon library — copy the SVG you need into the page directly.

## Things to never do

- Never use stock photography. Not headshots, not office shots, not abstract gradients.
- Never use AI-generated images. Especially not on a site for an AI advisory.
- Never add a chatbot, a popup, a cookie banner with custom styling, or a "subscribe"
  module. (Cookie banner only if legally required, and minimal.)
- Never add testimonials in v1.
- Never add a "trusted by" logo strip.
- Never use uppercase for body content. Uppercase is reserved for the ADVISORY
  designator and section labels (Calibri, tracked).
- Never centre body copy. Body text is left-aligned, ragged right.
- Never justify text.
- Never use a serif for buttons or UI labels. UI is Calibri; editorial is Georgia.

## File conventions

- Images go in `public/`
- Components in `src/components/`
- Layouts in `src/layouts/`
- Pages in `src/pages/`
- Global styles in `src/styles/global.css` — import `tokens.css` first, then your styles

## Acceptance criteria

A page is shippable when:

1. It loads in under 200ms on a cold cache.
2. Lighthouse scores 100/100/100/100.
3. The HTML is readable without CSS (semantic, ordered).
4. It works on a 320px-wide screen without horizontal scroll.
5. Nothing on the page is sage-coloured except the chevron.
6. There is no JavaScript in the bundle (check the network tab).

If a feature would break any of these, push back before building.
