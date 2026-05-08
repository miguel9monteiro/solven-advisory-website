import { defineConfig } from 'astro/config';

// TODO: set `site` once the domain is registered (e.g. 'https://solvenadvisory.com').
// Without it, og:image meta will use a relative URL — fine for dev, but social
// scrapers want absolute URLs in production.
export default defineConfig({
  trailingSlash: 'never',
  build: {
    inlineStylesheets: 'auto',
  },
});
