# AltStack Search

<!-- artemis-publisher:start -->
<img src="brand/artemis/artemis-wordmark.svg" alt="Artemis Softworks LLC" width="340">

**A product of Artemis Softworks LLC.** Founded by **Demetria Althea Cohn**.

Companion software for macOS, thoughtfully available for Windows and Linux. See the [Artemis identity and design system](brand/artemis/BRAND.md). Platform availability varies by product and release.
<!-- artemis-publisher:end -->


Artemis Softworks LLC distribution of SearXNG, licensed under AGPL-3.0-or-later. The Dockerfile pins the exact official image digest. Its upstream image labels identify the corresponding SearXNG source revision; upstream source is available at https://github.com/searxng/searxng. This directory contains all AltStack modifications and build scripts.

Search is served under `/search` through the platform's fixed private upstream proxy. Social bearer tokens and account cookies are not forwarded. IP addresses are used by SearXNG's abuse limiter; queries are not stored in AltStack account preferences. Infrastructure and upstream search providers can process network requests according to their own policies. AltStack inserts no advertising or paid placements and filters explicitly marked sponsored results.

`SEARXNG_SECRET`, `SEARXNG_BASE_URL`, and an authenticated `SEARXNG_VALKEY_URL` are required. Run the cache before Search. The source and upstream notices remain accessible in the footer.
