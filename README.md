# Solven Advisory — Website Assets

This directory contains everything needed to build the Solven Advisory website.
Drop it into the root of an Astro project (or reorganise per your stack).

## Read first

- **`CLAUDE.md`** — Agent instructions. The voice, the visual rules, the things
  to never do. Read this before writing any code.
- **`BRAND.md`** — Brand reference, agent-readable. Colour codes, type spec,
  lockup usage.

## Directory map

```
solven_site/
├── CLAUDE.md              ← agent instructions for the build
├── BRAND.md               ← brand reference, machine-readable
├── README.md              ← you are here
│
├── design/
│   ├── tokens.css         ← CSS custom properties (the source of truth)
│   └── tokens.json        ← same values, JSON format
│
├── logos/
│   ├── 01_solven_primary_lockup.svg     ← default
│   ├── 02_solven_reversed_lockup.svg    ← dark backgrounds
│   ├── 03_solven_horizontal_lockup.svg  ← nav, signatures
│   ├── 04_solven_wordmark_only.svg      ← inline references
│   ├── 05_solven_favicon.svg            ← favicon source
│   └── outlined/                         ← [empty — for outlined exports]
│
├── favicons/
│   ├── favicon.ico              ← legacy browsers
│   ├── favicon-16.png           ← browser tab
│   ├── favicon-32.png           ← browser tab (retina)
│   ├── favicon-512.png          ← PWA / large icons
│   ├── apple-touch-icon.png     ← iOS home screen (180px)
│   ├── og-image.png             ← social sharing card (1200×630)
│   └── og-image.svg             ← OG card source
│
├── icons/
│   ├── README.md          ← how to use icons
│   ├── arrow-right.svg
│   ├── arrow-up-right.svg
│   ├── close.svg
│   ├── linkedin.svg
│   ├── mail.svg
│   ├── map-pin.svg
│   └── menu.svg
│
├── ornaments/
│   ├── chevron.svg              ← standalone mark
│   ├── hairline.svg             ← thin divider
│   └── section-divider.svg      ← divider with centred chevron
│
└── templates/
    ├── Base.astro         ← reference layout with SEO and brand integration
    └── index.astro        ← reference homepage
```

## Suggested project layout

When dropping these into an Astro project:

```
project-root/
├── CLAUDE.md              ← move from solven_site/
├── BRAND.md               ← move from solven_site/
├── public/
│   ├── favicon.ico        ← from solven_site/favicons/
│   ├── favicon-16.png
│   ├── favicon-32.png
│   ├── apple-touch-icon.png
│   ├── og-image.png
│   ├── design/
│   │   └── tokens.css     ← from solven_site/design/
│   ├── logos/             ← from solven_site/logos/
│   └── icons/             ← from solven_site/icons/
└── src/
    ├── layouts/
    │   └── Base.astro     ← from solven_site/templates/
    ├── pages/
    │   └── index.astro    ← from solven_site/templates/
    └── styles/
        └── global.css     ← write this one
```

## Quick-start commands

```bash
# Create Astro project
npm create astro@latest solven-site -- --template minimal --typescript strict

# Drop in assets
cp -r solven_site/* solven-site/

# Restructure as above, then
cd solven-site
npm install
npm run dev
```

## Brand fundamentals (the version you'll need most often)

- **Colours**: charcoal `#2A2A28`, sage deep `#6B8068`, sage `#8FA68A`, bone `#F4F2EB`
- **Type**: Georgia (serif) + Calibri (sans). System fonts. No webfonts.
- **The chevron is the only sage element on any screen.** Don't tint anything else.
- **Bone is the page background.** Never pure white.
- **No JavaScript** in the bundle. Astro renders to static HTML.
- **No animations on load.** No fade-ins, no parallax, no scroll effects.
