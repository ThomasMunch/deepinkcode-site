"""Generate the home, app and support pages of deepinkcode.com in all languages.

Usage:  python3 _src/build.py      (run from the repo root or anywhere)
Text lives in _src/content.py. Privacy pages are hand-written; this script only
updates their language switcher. Jekyll ignores this folder (leading underscore).
"""
import json, os, re, sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import LANG_ORDER, LANGS, HOME, SUPPORT, FEATURES, PRIVACY_FAQ, PRICE_FAQ, APP_ORDER, APPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://deepinkcode.com"
YEAR = "2026"
SHOT_W = {"wordfeud": 462, "wwf": 462, "scrabble": 460}

def e(s):
    return escape(s, quote=True)

def url(lang, path):
    return f"{LANGS[lang]['prefix']}/{path}"

def lang_switch(cur, paths):
    """paths: lang -> site path for that language version."""
    links = []
    for l in LANG_ORDER:
        cur_attr = ' aria-current="true"' if l == cur else ""
        links.append(f'<a href="{paths[l]}" hreflang="{LANGS[l]["html"]}" lang="{LANGS[l]["html"]}" '
                     f'title="{LANGS[l]["name"]}"{cur_attr}>{l.upper()}</a>')
    return '<span class="langs">' + "".join(links) + "</span>"

def head(lang, title, desc, path, image, ld=None):
    L = LANGS[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{BASE}{url(l, path)}">\n'
                   for l in LANG_ORDER)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{url("en", path)}">\n'
    out = f"""<!doctype html>
<html lang="{L['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}{url(lang, path)}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="DeepInkCode">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{BASE}{url(lang, path)}">
<meta property="og:image" content="{BASE}{image}">
<meta property="og:locale" content="{L['og']}">
<meta name="twitter:card" content="summary_large_image">
"""
    if ld:
        out += '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + "\n</script>\n"
    out += """<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
</head>
<body>
"""
    return out

def header(lang, path, current):
    L = LANGS[lang]
    cur = lambda k: ' aria-current="page"' if k == current else ""
    paths = {l: url(l, path) for l in LANG_ORDER}
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{url(lang, '')}"><img src="/assets/img/logo.webp" alt="" width="36" height="36"><span>DEEP<b>INK</b>CODE</span></a>
    <nav class="nav">
      <a href="{url(lang, '#apps')}"{cur('apps')}>{L['nav_apps']}</a>
      <a href="{url(lang, 'support/')}"{cur('support')}>{L['nav_support']}</a>
      <a href="{L['privacy_url']}">{L['nav_privacy']}</a>
      {lang_switch(lang, paths)}
    </nav>
  </div>
</header>
"""

def footer(lang, script=False):
    L = LANGS[lang]
    s = '<script src="/assets/site.js" defer></script>\n' if script else ""
    return f"""<footer class="site-footer">
  <div class="wrap">
    <span>© {YEAR} DeepInkCode · CVR 45115666 · {L['country']}</span>
    <span><a href="mailto:support@deepinkcode.com">support@deepinkcode.com</a> · <a href="{L['privacy_url']}">{L['nav_privacy']}</a></span>
  </div>
</footer>
{s}</body>
</html>
"""

def badges(lang, app):
    L = LANGS[lang]
    f, alt, w = L["gp_badge"]
    out = (f'<a class="badge badge-gp" href="{app["gp"]}" rel="noopener"><img src="/assets/img/badges/{f}" '
           f'alt="{e(alt)}" width="{w}" height="40"></a>')
    if app["as"]:
        out += (f'<a class="badge badge-as" href="{app["as"]}" rel="noopener"><img src="/assets/img/badges/app-store.svg" '
                f'alt="{e(L["as_alt"])}" width="120" height="40"></a>')
    return f'<div class="stores">{out}</div>'

def write(lang, path, html):
    p = os.path.join(ROOT, LANGS[lang]["prefix"].strip("/"), path, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(html)

def build_home(lang):
    H, L = HOME[lang], LANGS[lang]
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "DeepInkCode",
          "url": BASE + "/", "logo": BASE + "/assets/img/logo.webp", "email": "support@deepinkcode.com"}
    cards = ""
    for slug in APP_ORDER:
        a = APPS[slug]
        cards += f"""  <article class="card card-{a['cls']}">
    <div class="card-head"><img src="/assets/img/apps/{a['img']}-icon.webp" alt="" width="64" height="64"><h2>{a['name']}</h2></div>
    <p>{e(a[lang]['tagline'])}</p>
    {badges(lang, a)}
    <a class="more" href="{url(lang, slug + '/')}">{L['read_more']}</a>
  </article>
"""
    html = head(lang, H["title"], H["desc"], "", "/assets/img/phone.webp", ld) + header(lang, "", "apps") + f"""<main class="wrap">
<section class="hero">
  <div class="hero-text">
  <h1>{e(H['h1'])}</h1>
  <p>{e(H['lead'])}</p>
  </div>
  <img class="hero-img" src="/assets/img/phone.webp" alt="{e(H['hero_alt'])}" width="360" height="360">
</section>
<section class="apps" id="apps">
{cards}</section>
</main>
""" + footer(lang)
    write(lang, "", html)

def build_app(lang, slug):
    a, L = APPS[slug], LANGS[lang]
    c = a[lang]
    path = slug + "/"
    ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": a["name"],
          "url": BASE + url(lang, path), "description": c["desc"], "applicationCategory": "GameApplication",
          "operatingSystem": a["os"], "inLanguage": L["html"], "image": f"{BASE}/assets/img/apps/{a['img']}-icon.webp",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "publisher": {"@type": "Organization", "name": "DeepInkCode", "url": BASE + "/"},
          "sameAs": [u for u in (a["gp"], a["as"]) if u]}
    shot_base = a["shots_localized"].get(lang, a["img"])
    gallery = "\n".join(f'    <li><img src="/assets/img/apps/{shot_base}-{i}.webp" alt="{e(alt)}" '
                        f'width="{SHOT_W[a["img"]]}" height="1000" loading="lazy"></li>'
                        for i, alt in enumerate(c["shots"], 1))
    video = ""
    if a["video"]:
        video = f"""
  <section class="app-section">
    <h2>{L['video']}</h2>
    <a class="video" href="https://www.youtube.com/watch?v={a['video']}" data-yt="{a['video']}" data-title="{a['name']}" aria-label="{L['play']}: {a['name']}">
      <img src="/assets/img/apps/{a['img']}-video.webp" alt="" width="480" height="270" loading="lazy">
      <span class="play" aria-hidden="true"></span>
    </a>
    <p class="note">{e(L['video_note'])}</p>
  </section>"""
    steps = "\n".join(f'      <li><span class="num">{i}</span><div><strong>{e(t)}</strong>{e(d)}</div></li>'
                      for i, (t, d) in enumerate(c["steps"], 1))
    feats = "\n".join(f"      <li>{e(f)}</li>" for f in FEATURES[lang])
    faq_items = [(q, a_ if a_ else PRICE_FAQ[lang]) for q, a_ in c["faq"]] + [PRIVACY_FAQ[lang]]
    faq = "\n".join(f'    <div class="faq-item"><h3>{e(q)}</h3><p>{e(ans)}</p></div>' for q, ans in faq_items)
    others = "\n".join(f'      <li><a href="{url(lang, s + "/")}">{APPS[s]["name"]}</a></li>'
                       for s in APP_ORDER if s != slug)
    note = f'\n    <p class="note">{e(c["note"])}</p>' if c["note"] else "\n    "
    html = head(lang, c["title"], c["desc"], path, f"/assets/img/apps/{shot_base}-1.webp", ld) + header(lang, path, None) + f"""<main class="wrap app app-{a['cls']}">
<section class="app-hero">
  <img class="app-icon" src="/assets/img/apps/{a['img']}-icon.webp" alt="{a['name']} {L['icon']}" width="128" height="128">
  <div>
    <h1>{a['name']}</h1>
    <p class="tagline">{e(c['tagline'])}</p>
    {badges(lang, a)}{note}
  </div>
</section>
<p class="lead app-intro">{e(c['intro'])}</p>
<p class="app-intro">{e(c['extra'])}</p>

<section class="app-section">
  <h2>{L['screenshots']}</h2>
  <ul class="gallery">
{gallery}
  </ul>
</section>
{video}
<div class="app-cols">
  <section class="app-section">
    <h2>{L['how']}</h2>
    <ol class="steps">
{steps}
    </ol>
  </section>
  <section class="app-section">
    <h2>{L['features']}</h2>
    <ul class="checks">
{feats}
    </ul>
  </section>
</div>
<section class="app-section faq">
  <h2>{L['faq']}</h2>
{faq}
</section>
<section class="app-section more-apps">
  <h2>{L['more']}</h2>
    <ul>
{others}
    </ul>
</section>
<p class="note disclaimer">{e(c['disclaimer'])}</p>
</main>
""" + footer(lang, script=True)
    write(lang, path, html)

def build_support(lang):
    S = SUPPORT[lang]
    items = "\n".join(f"  <li>{e(i)}</li>" for i in S["items"])
    html = head(lang, S["title"], S["desc"], "support/", "/assets/img/phone.webp") + header(lang, "support/", "support") + f"""<main class="wrap">
<article class="page">
<h1>{e(S['h1'])}</h1>
<p class="lead">{e(S['lead'])}</p>
<p><a href="mailto:support@deepinkcode.com">support@deepinkcode.com</a></p>
<h2>{e(S['h2'])}</h2>
<ul class="features">
{items}
</ul>
</article>
</main>
""" + footer(lang)
    write(lang, "support/", html)

def patch_privacy():
    """Hand-written privacy pages exist in en + da only; swap their single language link for the switcher."""
    pages = {"en": "privacy-policy-website/index.html", "da": "da/privatlivspolitik/index.html"}
    paths = {"en": "/privacy-policy-website/", "da": "/da/privatlivspolitik/", "nl": "/nl/", "sv": "/sv/", "no": "/no/"}
    for lang, rel in pages.items():
        p = os.path.join(ROOT, rel)
        html = open(p, encoding="utf-8").read()
        html = re.sub(r'<a class="lang"[^>]*>[^<]*</a>|<span class="langs">.*?</span>', lambda m: lang_switch(lang, paths), html, count=1)
        open(p, "w", encoding="utf-8").write(html)

def build_sitemap():
    paths = [""] + [s + "/" for s in APP_ORDER] + ["support/"]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in paths:
        for lang in LANG_ORDER:
            out += ["  <url>", f"    <loc>{BASE}{url(lang, p)}</loc>"]
            out += [f'    <xhtml:link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{BASE}{url(l, p)}"/>' for l in LANG_ORDER]
            out += [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{url("en", p)}"/>', "  </url>"]
    out += [f"  <url><loc>{BASE}/privacy-policy-website/</loc></url>",
            f"  <url><loc>{BASE}/da/privatlivspolitik/</loc></url>", "</urlset>"]
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")

if __name__ == "__main__":
    for lang in LANG_ORDER:
        build_home(lang)
        build_support(lang)
        for slug in APP_ORDER:
            build_app(lang, slug)
    patch_privacy()
    build_sitemap()
    print("built", len(LANG_ORDER) * (2 + len(APP_ORDER)), "pages")
