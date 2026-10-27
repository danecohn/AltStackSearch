# Vigil Search: VigilTech branding applied on top of the exact pinned SearXNG image (AGPL-3.0-or-later).
# Every integration point fails closed: if upstream changes, the build stops instead of shipping a half-branded page.
from pathlib import Path
import os
import shutil

root = Path(os.environ.get('VIGILTECH_UPSTREAM_ROOT', '/usr/local/searxng/searx'))
assets = Path(__file__).resolve().parent
theme = root / 'static/themes/simple'
ICON = "{{ url_for('static', filename='vigiltech/product-icons/search/web/icon-192.png') }}"


def need(text, needle, what):
    if needle not in text:
        raise RuntimeError('SearXNG integration changed: ' + what)
    return text


# Page shell: title, VigilTech menu bar, footer credit, body class and design-system links.
base = root / 'templates/simple/base.html'
text = base.read_text()
text = text.replace('SearXNG — a privacy-respecting, open metasearch engine', 'Vigil Search — independent web metasearch')
need(text, '<main id=', 'main element')
text = text.replace(
    '<main id=',
    '<header class="vt-menubar"><a href="/" class="vt-brand"><img src="' + ICON + '" alt="">Vigil Search</a>'
    '<nav><a href="/office">Vigil Office</a><a href="/warehouse">Vigil Drive</a><a href="/mail">Vigil Mail</a>'
    '<a href="/calendar">Vigil Calendar</a><a href="/social">Vigil Social</a>'
    '<a id="search-account" href="/social#account">Your account</a></nav></header><main id=', 1)
need(text, "{{ _('Powered by') }} <a", 'footer credit')
text = text.replace("{{ _('Powered by') }} <a", "VigilTech · {{ _('Powered by') }} <a")
need(text, '<body class="', 'body class')
text = text.replace('<body class="', '<body class="vt ', 1)
links = (
    "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='vigiltech/css/vigilsans.css') }}\">"
    "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='vigiltech/css/goldengate.css') }}\">"
    "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='vigiltech-search.css') }}\">"
    "<script defer src=\"{{ url_for('static', filename='vigiltech.js') }}\"></script>"
    "<script defer src=\"{{ url_for('static', filename='altstack-account.js') }}\"></script>"
    "<meta name=\"theme-color\" content=\"#120a14\"><meta property=\"og:title\" content=\"Vigil Search\">"
    "<meta property=\"og:image\" content=\"{{ url_for('static', filename='vigiltech/logos/social/vigiltech-social-1200x630.png', _external=True) }}\">"
    "<link rel=\"apple-touch-icon\" href=\"{{ url_for('static', filename='vigiltech/product-icons/search/web/apple-touch-icon.png') }}\">"
    "<link rel=\"manifest\" href=\"{{ url_for('static', filename='vigiltech/product-icons/search/web/manifest.webmanifest') }}\">"
)
text = text.replace('</head>', links + '</head>', 1)
text = text.replace('<html ', '<html data-theme="dark" ', 1)
text = text.replace('img/favicon.svg', 'img/favicon.ico')
base.write_text(text)

# Home page heading.
p = root / 'templates/simple/index.html'
text = need(p.read_text(), '<h1>SearXNG</h1>', 'home heading')
p.write_text(text.replace(
    '<h1>SearXNG</h1>',
    '<img class="vt-search-mark" src="' + ICON + '" alt=""><h1>Vigil Search</h1>'
    '<p class="vt-search-note">Metasearch with no ads and no paid placements.</p>'))

# Results header: our icon and name instead of the upstream wordmark; name replaced elsewhere in the template.
p = root / 'templates/simple/search.html'
if p.exists():
    text = p.read_text().replace('SearXNG', 'Vigil Search')
    needle = "{% include 'simple/searxng-wordmark.min.svg' without context %}"
    need(text, needle, 'results header wordmark')
    text = text.replace(needle, '<img src="' + ICON + '" alt=""><span class="vt-wordmark">Vigil Search</span>')
    p.write_text(text)

# Static files: design system, theme override, appearance bridge, account bridge, product web icons.
shutil.copytree(assets / 'vigiltech', theme / 'vigiltech', dirs_exist_ok=True)
for name in ['vigiltech-search.css', 'vigiltech.js', 'altstack-account.js', 'altstack.css']:
    shutil.copy2(assets / name, theme / name)
shutil.copy2(assets / 'logo.svg', theme / 'img/altstack.svg')
shutil.copy2(assets / 'logo.svg', theme / 'img/favicon.svg')
logo = (assets / 'logo.png').read_bytes()
if not logo.startswith(b'\x89PNG\r\n\x1a\n'):
    raise RuntimeError('Vigil Search favicon is not a valid PNG export')
kit = assets / 'vigiltech/product-icons/search/web'
for source, target in [('favicon-32.png', 'favicon.png'), ('favicon.ico', 'favicon.ico'), ('apple-touch-icon.png', 'apple-touch-icon.png')]:
    shutil.copy2(kit / source, theme / 'img' / target)
(theme / 'img/searxng.png').write_bytes(logo)

# Any remaining upstream logo reference points at the VigilTech mark.
for template in (root / 'templates/simple').rglob('*.html'):
    text = template.read_text()
    for old in ['img/searxng.png', 'img/searxng.svg', 'img/searxng-wordmark.svg']:
        text = text.replace(old, 'img/altstack.svg')
    template.write_text(text)

# Modified resources must not keep upstream precompressed variants.
for path in (theme / 'img').glob('*'):
    if path.suffix in ['.gz', '.br'] and any(name in path.name for name in ['favicon', 'searxng', 'altstack', 'apple-touch']):
        path.unlink()
for path in theme.glob('*'):
    if path.suffix in ['.gz', '.br'] and path.name.split('.')[0] in ['altstack', 'altstack-account', 'vigiltech', 'vigiltech-search']:
        path.unlink()

# Discard explicitly marked sponsored results if an upstream engine returns any.
p = root / 'webapp.py'
text = p.read_text()
old = 'results = result_container.get_ordered_results()'
need(text, old, 'result container')
p.write_text(text.replace(old, "results = [r for r in result_container.get_ordered_results() if not any((r.as_dict() if hasattr(r, 'as_dict') else r).get(k) for k in ('is_ad', 'sponsored', 'advertisement'))]"))
