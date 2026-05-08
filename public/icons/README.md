# Icons

Curated Lucide icon set (MIT licensed, https://lucide.dev). Each icon uses
`stroke="currentColor"` so it inherits text colour — set the colour on the
parent element via CSS.

## How to use

Inline the SVG directly. Don't use an icon component library.

```html
<a href="mailto:hello@solvenadvisory.com" class="contact-link">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect width="20" height="16" x="2" y="4" rx="2"/>
    <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
  </svg>
  hello@solvenadvisory.com
</a>
```

## Available

- `arrow-right.svg` — primary directional arrow, navigation
- `arrow-up-right.svg` — external link indicator
- `close.svg` — modal/menu dismiss
- `linkedin.svg` — social link
- `mail.svg` — contact, email
- `map-pin.svg` — location (Lisbon)
- `menu.svg` — mobile nav toggle

## Adding more icons

If you need an icon not in this set, copy it from https://lucide.dev only.
Don't import lucide-react or any icon component library — keep the bundle empty.
Match the existing settings: `stroke-width="1.5"`, `stroke-linecap="round"`,
`stroke-linejoin="round"`, `aria-hidden="true"`.

Lucide's default stroke-width is 2; the brand uses 1.5 for a lighter feel
that matches the brand's typographic restraint.
