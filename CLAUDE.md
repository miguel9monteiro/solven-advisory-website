# Solven Advisory Website

Marketing site for Solven Advisory: a one-founder AI enablement and
implementation consultancy in Lisbon (founder: Miguel Monteiro), selling to
private equity, real estate, and venture firms. Core thesis: "augmentation
without cognitive atrophy". The analyst produces the work first; the model
enters as critic, red-teamer, and verifier, never as author. Offer: monthly
Claude enablement programmes (four-session arc), build work (agents on real
workflows), AI due diligence on targets, and token economics. Solven is a
member of the Anthropic Partner Network.

## Stack and deployment

- Plain HTML/CSS/JS. No framework, no build step, no webfonts.
- Deployed on Vercel from GitHub `miguel9monteiro/solven-advisory-website`;
  **pushing to `main` deploys to production immediately.**
- `vercel.json`: `cleanUrls` on, `trailingSlash` off, `/blog.html` redirect,
  security and asset-cache headers. Internal links are extensionless
  (`/about`, `/contact#book`); assets use absolute paths (`/assets/...`).
- `.vercelignore` keeps `legacy/` (old Astro site), `BRAND.md`,
  `articlesforblog/`, and `tools/` out of production. They were once publicly
  served; keep it that way.
- Canonical origin: `https://solvenadvisory.ai` (apex, no www, no trailing
  slash; the PT page is `/pt`). Every page carries canonical + OG + Twitter
  meta and shares `assets/og.png` (1200x630, generated from brand SVGs).

## Layout

- Pages: `index`, `programmes`, `approach`, `work`, `about`, `contact`,
  `privacy`, `404`, `blog/index` + three articles (`blog/<slug>.html`,
  July 2026, author Miguel Monteiro), and `ai-flix` (AI Flix, the Solven
  screening room: Netflix-style dark shelves of YouTube videos with real
  thumbnails; EN-only like the journal, "AI Flix · EN" in the PT nav).
  Cards open in the on-site Solven player (a dialog embedding YouTube's
  privacy-enhanced youtube-nocookie player); videos whose owners disable
  embedding are detected automatically and open on YouTube instead.
  **AI Flix is videos only and the owner curates it** — never add entries
  on your own initiative. `ai-flix.html` is GENERATED: to add a video the
  owner supplies a YouTube URL; append it to `VIDEOS` in
  `tools/build_ai_flix.py` (url + len required; title/src/note optional
  overrides) and run the tool, which fetches title, channel, and
  thumbnail from YouTube oEmbed and rebuilds the page and its JSON-LD.
  Bump the "updated" month in the tool's hero copy when the shelf
  changes.
- Portuguese mirror under `pt/`: `pt/index` plus full pt-PT versions of the
  five core pages. The pairs (keep in sync when EN copy changes):
  `/` ↔ `/pt`, `/programmes` ↔ `/pt/programas`, `/approach` ↔ `/pt/abordagem`,
  `/work` ↔ `/pt/trabalho`, `/about` ↔ `/pt/sobre`,
  `/contact` ↔ `/pt/contacto`. PT pages use the standard header with PT
  labels (Blog links to the EN journal as "Blog · EN") and the compact
  `.ptfooter`. The journal, privacy, and 404 are EN-only (their PT toggle
  goes to `/pt`).
- Shared: `solven.css` (design system + motion), `solven.js` (motion/interaction
  layer), `BRAND.md` (brand reference: palette, type, voice; not deployed).
- Discovery: `robots.txt` (deliberately liberal; all crawlers and AI bots
  explicitly welcomed), `sitemap.xml` (12 URLs, hreflang on the `/` and `/pt`
  pair only), `llms.txt` (hand-written index), `llms-full.txt` (**generated**:
  run `python3 tools/build_llms_full.py` after any copy change, never hand-edit),
  `site.webmanifest`.
- Structured data: ProfessionalService on `/`, Service + FAQPage on
  `/programmes`, Blog/BlogPosting on the journal, WebPage on `/pt`.

## Conversion stack

- Booking: Cal.com EU embedded inline on `/contact#calendar`
  (`cal.eu/miguelmonteirosolven`, loader from `app.cal.eu/embed/embed.js`);
  the "countersign" signature block links to it on-page. A "Book a call"
  `.nav-cta` button sits in every header; booking is the primary CTA in the
  hero and all closers.
- Contact form posts to FormSubmit (`formsubmit.co/miguelmonteiro@solvenadvisory.ai`)
  with honeypot and `?sent=1` success state.
- Header also carries a `.nav-lang` language toggle: PT on English pages, EN
  on `/pt`.
- Analytics: Vercel Web Analytics snippet on every page (cookieless; the site
  promises "No cookies, no list", so never add cookie-based tracking).

## Writing rules

- **Em dashes are a big no. Never use an em dash (—) anywhere**: not in copy,
  titles, meta, JSON-LD, code comments, or generated files. Rewrite with a
  comma, colon, full stop, or restructure. En dashes and spaced hyphens as
  dashes are not acceptable substitutes. The middot (·) is the house separator
  for labels ("Lisbon · 2026", "Contact · Solven Advisory"). This extends to
  visual elements: a decorative hairline that reads as a dash was removed too.
- Voice (BRAND.md): considered, not corporate; complete sentences, no
  fragments for emphasis; specific over generic; fewer words when in doubt.
  Banned words: synergy, leverage (verb), value-add, robust, holistic,
  leading, cutting-edge, unlock, ecosystem, journey, delight.
- British spelling (programmes, analyse, organisation).
- Portuguese content is **European Portuguese**: formação (not capacitação),
  casas/sociedades de investimento (not firmas), equipas, vossos, «guillemets»,
  "marcar uma chamada". Finance anglicisms (private equity, term sheet, deck)
  are deliberate.

## Invariants

- The three FAQ answers shared between `programmes.html` and `contact.html`
  must stay word-for-word identical, and the FAQPage JSON-LD in
  `programmes.html` must exactly match the visible answer text.
- title = og:title = twitter:title, and description = og:description =
  twitter:description, per page.
- hreflang (en / pt-PT / x-default) lives only on paired pages, reciprocally
  on both sides of each EN ↔ PT pair (and in the sitemap); annotating
  unpaired pages (journal, privacy, 404) is invalid.
- The `.nav-lang` toggle always targets the page's own counterpart, never
  the other language's home (except on unpaired pages, where PT → `/pt`).
- The three shared FAQ answers exist in BOTH languages: EN on
  `programmes`/`contact`, PT on `pt/programas`/`pt/contacto`; each language
  pair must stay word-for-word identical internally.
- Exactly one h1 per page; no internal link may end in `.html`.
- Motion: content visible by default. Hidden states exist only behind
  JS-applied classes (`.pending`, `body.intro-armed`, `html.anim`) with timed
  rescue paths; `prefers-reduced-motion: reduce` is a hard stop for every
  effect. See the headers in `solven.js` and the cinematic sections of
  `solven.css` (view-transition continuity, blur focus-pull reveals, dark-band
  light drift, breathing chevrons, the self-drawing contract signature on
  contact, `data-stagger` cascades).
- Never pure black, no greens beyond the two brand sages, no third typeface,
  bone background not white (BRAND.md).

## Known issues and owner to-dos (verify before assuming fixed)

- **Apex misrouted**: `solvenadvisory.ai` 301s to
  `solven-advisory-website.vercel.app`; only `www` serves correctly. Fix is in
  Vercel domain settings (apex primary, www redirects to it). Canonicals
  already point at the apex.
- **Email deliverability**: MX is Microsoft 365 but SPF is GoDaddy-only
  (`include:secureserver.net -all`) and M365 DKIM is off; DMARC quarantines.
  Owner must fix DNS + M365 admin.
- FormSubmit needs a one-time activation click (first live form submission
  emails the owner a confirmation link).
- Vercel Web Analytics needs its dashboard toggle (until then the snippet
  404s harmlessly).
- Sitemap not yet submitted in Google Search Console (domain verification
  TXT already exists on solvenadvisory.ai).
- `solvenadvisory.com` belongs to an unrelated ERP advisory (name collision on
  branded search). `solvenadvisory.pt` and `solven.pt` were unregistered as of
  2026-07-28; owner intends to register.
- The contact signature says "Co-founder" while about says "the team"; whether
  Solven is one founder or two is unresolved. Do not "fix" without asking.
- The "Anthropic Partner Network · Phase 1" badge is plain text; it needs a
  verification link only the owner can supply.
