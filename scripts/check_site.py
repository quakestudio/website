#!/usr/bin/env python3
"""Pre-deploy check for the QUAKE site. Standard library only.

Runs as the Cloudflare Pages build command, so a failing check stops the deploy
and the live site stays on the last good version. Run it locally before opening
a pull request:

    python3 scripts/check_site.py            # errors fail, draft markers are listed
    python3 scripts/check_site.py --strict   # also fail on draft markers (use before launch)
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://quake-studio.com"
SKIP_SEO = {"404.html"}

errors = []
warnings = []
todos = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._in = None
        self.meta = {}
        self.links = []          # (rel, hreflang, href)
        self.hrefs = []
        self.srcs = []
        self.ids = set()
        self.h1 = 0
        self.imgs = []
        self.jsonld = []
        self.todo = 0
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if "data-todo" in a:
            self.todo += 1
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in, self._buf = "title", []
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append((a.get("rel", ""), a.get("hreflang"), a.get("href", "")))
            if a.get("rel") in ("stylesheet", "icon", "apple-touch-icon"):
                self.srcs.append(a.get("href", ""))
        elif tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        elif tag in ("img", "script", "iframe", "source") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "jsonld", []

    def handle_endtag(self, tag):
        if self._in == "title" and tag == "title":
            self.title = "".join(self._buf).strip()
            self._in = None
        elif self._in == "jsonld" and tag == "script":
            self.jsonld.append("".join(self._buf))
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)


def url_for(path):
    rel = path.relative_to(SITE).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve(url_path):
    """Map a site URL path to a file in site/, or None."""
    p = unquote(url_path)
    candidates = [SITE / p.lstrip("/")]
    if p.endswith("/"):
        candidates = [SITE / p.lstrip("/") / "index.html"]
    else:
        candidates.append(SITE / (p.lstrip("/") + ".html"))
        candidates.append(SITE / p.lstrip("/") / "index.html")
    for c in candidates:
        if c.is_file():
            return c
    return None


def main():
    strict = "--strict" in sys.argv
    pages = {}
    for f in sorted(SITE.rglob("*.html")):
        parser = Page()
        parser.feed(f.read_text(encoding="utf-8"))
        pages[f] = parser

    wa_numbers, tel_numbers = set(), set()

    for f, pg in pages.items():
        name = f.relative_to(SITE).as_posix()
        url = url_for(f)

        if pg.todo:
            todos.append(f"{name}: {pg.todo} draft marker(s)")

        if pg.lang not in ("tr", "en"):
            errors.append(f"{name}: <html lang> must be tr or en, found {pg.lang!r}")
        if pg.lang == "en" and not url.startswith("/en/") and name not in SKIP_SEO:
            errors.append(f"{name}: English page outside /en/")
        if pg.lang == "tr" and url.startswith("/en/"):
            errors.append(f"{name}: Turkish page inside /en/")

        if not pg.title:
            errors.append(f"{name}: missing <title>")
        if pg.h1 != 1:
            errors.append(f"{name}: needs exactly one <h1>, found {pg.h1}")

        if name not in SKIP_SEO:
            desc = pg.meta.get("description", "")
            if not desc:
                errors.append(f"{name}: missing meta description")
            elif len(desc) > 175:
                warnings.append(f"{name}: meta description is {len(desc)} chars (aim for under 160)")
            if len(pg.title) > 65:
                warnings.append(f"{name}: title is {len(pg.title)} chars (aim for under 65)")
            canon = [h for r, _, h in pg.links if r == "canonical"]
            if canon != [DOMAIN + url]:
                errors.append(f"{name}: canonical should be {DOMAIN + url}, found {canon}")
            alts = {hl: h for r, hl, h in pg.links if r == "alternate" and hl}
            for hl in ("tr", "en", "x-default"):
                if hl not in alts:
                    errors.append(f"{name}: missing hreflang={hl}")
            if alts.get("tr") and alts.get("en"):
                tr_file = resolve(urlparse(alts["tr"]).path)
                en_file = resolve(urlparse(alts["en"]).path)
                if not tr_file:
                    errors.append(f"{name}: hreflang tr points to a missing page {alts['tr']}")
                if not en_file:
                    errors.append(f"{name}: hreflang en points to a missing page {alts['en']}")
                if DOMAIN + url not in (alts.get("tr"), alts.get("en")):
                    errors.append(f"{name}: hreflang links do not include the page itself")
            if pg.meta.get("og:url") and pg.meta["og:url"] != DOMAIN + url:
                errors.append(f"{name}: og:url should be {DOMAIN + url}")

        for block in pg.jsonld:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                errors.append(f"{name}: structured data (ld+json) is not valid JSON: {e}")

        for img in pg.imgs:
            if "alt" not in img:
                errors.append(f"{name}: <img src={img.get('src')!r}> has no alt text")
            if not (img.get("width") and img.get("height")):
                warnings.append(f"{name}: <img src={img.get('src')!r}> has no width/height (causes layout shift)")

        for ref in pg.hrefs + pg.srcs:
            u = urlparse(ref)
            if u.scheme in ("http", "https"):
                if u.netloc == "wa.me":
                    wa_numbers.add(u.path.strip("/"))
                if u.netloc in ("quake-studio.com", "www.quake-studio.com") and not resolve(u.path or "/"):
                    errors.append(f"{name}: link to missing page {ref}")
                continue
            if u.scheme == "tel":
                tel_numbers.add(u.path)
                continue
            if u.scheme in ("mailto",) or ref.startswith("data:"):
                continue
            if ref.startswith("#"):
                if ref[1:] and unquote(ref[1:]) not in pg.ids:
                    errors.append(f"{name}: anchor {ref} has no matching id on the page")
                continue
            if not ref.startswith("/"):
                errors.append(f"{name}: use root-relative links (starting with /), found {ref!r}")
                continue
            target = resolve(u.path)
            if not target:
                errors.append(f"{name}: link to missing file {ref}")
            elif u.fragment and target.suffix == ".html":
                if unquote(u.fragment) not in pages[target].ids:
                    errors.append(f"{name}: {ref} points to an anchor that does not exist")

    if len(wa_numbers) > 1:
        errors.append(f"WhatsApp links use different numbers: {sorted(wa_numbers)}")
    if len(tel_numbers) > 1:
        errors.append(f"Phone links use different numbers: {sorted(tel_numbers)}")

    # Every Turkish page needs an English twin and the other way round.
    urls = {url_for(f) for f, pg in pages.items() if f.name != "404.html"}
    for u in sorted(urls):
        twin = u[3:] if u.startswith("/en/") else "/en" + u
        twin = twin or "/"
        if twin not in urls:
            errors.append(f"{u}: missing language twin {twin}")

    # Sitemap must list every page.
    sm = SITE / "sitemap.xml"
    if sm.is_file():
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8")))
        for u in sorted(urls):
            if DOMAIN + u not in locs:
                errors.append(f"sitemap.xml: missing {DOMAIN + u}")
        for loc in sorted(locs):
            if not resolve(urlparse(loc).path):
                errors.append(f"sitemap.xml: lists a missing page {loc}")
    else:
        errors.append("site/sitemap.xml is missing")

    # Oversized images slow the site down on phones.
    for img in SITE.rglob("*"):
        if img.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".avif") and img.stat().st_size > 400_000:
            warnings.append(f"{img.relative_to(SITE)} is {img.stat().st_size // 1000} KB (keep photos under 400 KB)")

    for w in warnings:
        print(f"warning: {w}")
    if todos:
        print(f"{'error' if strict else 'note'}: draft markers still in the site (search for data-todo):")
        for t in todos:
            print(f"  {t}")
        if strict:
            errors.append("draft markers remain (run without --strict to allow them)")
    for e in errors:
        print(f"ERROR: {e}")

    print(f"\nChecked {len(pages)} pages: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
