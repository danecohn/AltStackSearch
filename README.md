# Vigil Search (AltStackSearch)

<img src="vigiltech/product-icons/search/web/icon-192.png" alt="Vigil Search" width="96">

Vigil Search is VigilTech's distribution of [SearXNG](https://github.com/searxng/searxng), a metasearch engine. It has no advertising and no paid placements. A product of VigilTech, vigiltech.org. VigilTech was founded by Demetria Althea Cohn.

This distribution incorporates SearXNG and remains licensed under **AGPL-3.0-or-later**; the upstream `LICENSE` and the source-offer links in the footer are kept. The Dockerfile pins the exact official image digest, whose labels identify the corresponding SearXNG source revision; upstream source is at https://github.com/searxng/searxng. This repository contains all VigilTech modifications and build scripts. VigilTech-owned brand assets are GPL v3 and Vigil Sans is SIL OFL 1.1; relabelling the combined work GPL-only would be incorrect.

Search is served under `/search` through the platform's fixed private upstream proxy. Social bearer tokens and account cookies are not forwarded. IP addresses are used by SearXNG's abuse limiter; queries are not stored in account preferences. Infrastructure and upstream search providers can process network requests according to their own policies. No advertising or paid placements are inserted, and explicitly marked sponsored results are filtered.

`SEARXNG_SECRET`, `SEARXNG_BASE_URL`, and an authenticated `SEARXNG_VALKEY_URL` are required. Run the cache before Search. The source and upstream notices remain accessible in the footer.

## How the theme is applied

`brand.py` runs once while the image is built and patches the pinned SearXNG templates (it stops with an error if an integration point has changed):

- `vigiltech/` holds the VigilTech design system (Golden Gate tokens, Vigil Sans) and the Vigil Search web icon kit.
- `vigiltech-search.css` maps SearXNG's own classes onto the design system: Night and Dawn appearances, frosted header, pink primary buttons, explicit text and background colours in every state.
- `vigiltech.js` adds the Appearance menu (system, Dawn, Night, system font).
- `altstack-account.js` optionally syncs search preferences with a signed-in account. Queries are never saved.

## Static preview

`preview/` has static pages (search home, results, preferences) for checking the look without running SearXNG: run `python3 -m http.server` in this folder and open `/preview/index.html`. They are hand-written markup shaped like SearXNG's simple theme, not SearXNG output, and are left out of the image.

Icons: [VigilTech](https://github.com/danecohn/vigilicons), supplied `products/search` kit.
