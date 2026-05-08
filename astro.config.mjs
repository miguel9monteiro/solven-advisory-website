import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.solvenadvisory.ai',
  trailingSlash: 'never',
  build: {
    inlineStylesheets: 'auto',
  },
});
