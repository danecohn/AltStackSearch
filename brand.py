from pathlib import Path
import shutil
root=Path('/usr/local/searxng/searx');assets=Path('/opt/altstack-search')
base=root/'templates/simple/base.html';text=base.read_text()
text=text.replace('SearXNG — a privacy-respecting, open metasearch engine','AltStack Search — independent web metasearch')
text=text.replace('</head>', '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'altstack.css\') }}"><script defer src="{{ url_for(\'static\', filename=\'altstack-account.js\') }}"></script></head>')
text=text.replace('<body class=', '<body class=',1).replace('<main id=', '<header class="altstack-menubar"><a href="/" class="altstack-brand"><img src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt="">AltStack Search</a><nav><a href="/office">Office</a><a href="/warehouse">Warehouse</a><a href="/social">Social</a><a id="search-account" href="/social#account">Your account</a></nav></header><main id=',1)
text=text.replace("{{ _('Powered by') }} <a", "AltStack LLC · {{ _('Powered by') }} <a")
base.write_text(text)
p=root/'templates/simple/index.html';p.write_text(p.read_text().replace('<h1>SearXNG</h1>','<img class="altstack-search-mark" src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt=""><h1>AltStack Search</h1><p class="altstack-search-note">The whole web. A different perspective.<br>No ads. No paid placements.</p>'))
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/altstack.svg')
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/favicon.svg')
for name in ['altstack.css','altstack-account.js']:shutil.copy2(assets/name,root/'static/themes/simple'/name)
# Remove the upstream logo in the results search header while preserving search controls.
p=root/'templates/simple/search.html'
if p.exists():p.write_text(p.read_text().replace('SearXNG','AltStack Search'))
# Discard explicitly marked sponsored results if an upstream engine returns any.
p=root/'webapp.py';text=p.read_text();old='results = result_container.get_ordered_results()'
if old not in text:raise RuntimeError('SearXNG result integration changed')
text=text.replace(old,"results = [r for r in result_container.get_ordered_results() if not any((r.as_dict() if hasattr(r, 'as_dict') else r).get(k) for k in ('is_ad', 'sponsored', 'advertisement'))]")
p.write_text(text)

# Modified sources/static assets must not retain upstream precompressed variants.
import base64,re
logo=base64.b64decode(re.search(r'data:image/png;base64,([^"]+)',(assets/'logo.svg').read_text()).group(1))
for name in ['favicon.png','searxng.png']: (root/'static/themes/simple/img'/name).write_bytes(logo)
for template in (root/'templates/simple').rglob('*.html'):
 text=template.read_text()
 for old in ['img/searxng.png','img/searxng.svg','img/searxng-wordmark.svg']:text=text.replace(old,'img/altstack.svg')
 template.write_text(text)
for path in (root/'static/themes/simple/img').glob('*'):
 if path.suffix in ['.gz','.br'] and any(name in path.name for name in ['favicon','searxng','altstack']):path.unlink()
