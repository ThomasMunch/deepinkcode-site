# deepinkcode.com

Static website for DeepInkCode, hosted on GitHub Pages with the custom domain in `CNAME`.

Plain HTML/CSS. Each page is `<path>/index.html`. Languages: English (root), Danish (`da/`),
Dutch (`nl/`), Swedish (`sv/`) and Norwegian (`no/`).

The home, app and support pages in all languages are generated:

    python3 _src/build.py

Edit text in `_src/content.py`, run the script and commit the generated HTML. The script also
rewrites `sitemap.xml` and the language switcher on the privacy pages. Privacy pages
(`/privacy-policy-website/`, `/da/privatlivspolitik/`) are hand-written.

Important: `/privacy-policy-website/` and `/support/` are linked from the Google Play and App Store
listings. Do not rename them. Keep `googlec3da86efecdaaf4d.html` (Google Search Console verification).
