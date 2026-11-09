#!/usr/bin/env python3
"""Newsroom cards for the org profile, built from https://onetech.group/feed.

Writes profile/assets/news-{1..3}-{light,dark}.svg and rewrites the block between
<!-- NEWS:START --> and <!-- NEWS:END --> in profile/README.md.
Only links on onetech.group are accepted; all feed text is XML-escaped.
"""
import datetime as dt
import email.utils
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_org_svgs import BASE_CSS, OUT, ROOT, THEMES, font_css, svg  # noqa: E402

FEED = "https://onetech.group/feed"
README = ROOT / "profile" / "README.md"
START, END = "<!-- NEWS:START -->", "<!-- NEWS:END -->"
N = 3


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def fetch():
    req = urllib.request.Request(FEED, headers={"User-Agent": "otg-org-profile-builder"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    items = []
    for it in root.iter("item"):
        link = (it.findtext("link") or "").strip()
        host = urllib.parse.urlparse(link).hostname or ""
        if not (host == "onetech.group" or host.endswith(".onetech.group")):
            continue
        date = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
        items.append(dict(title=" ".join((it.findtext("title") or "").split()), link=link, date=date,
                          category=(it.findtext("category") or "News").strip()))
    items.sort(key=lambda x: x["date"], reverse=True)
    return items[:N]


def wrap(text, width, lines):
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = f"{cur} {w}".strip()
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = out[-1][: width - 1].rstrip() + "…"
    return out


def card(t, item):
    W, H = 380, 196
    css = font_css(mono_bold=False) + BASE_CSS
    g = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>']
    cat = item["category"].upper()[:22]
    cw = len(cat) * 10 * 0.612 + 22
    g.append(f'<rect x="20" y="20" width="{cw:.0f}" height="22" rx="11" fill="{t["primary_light"]}"/>'
             f'<circle cx="31" cy="31" r="2.5" fill="{t["link"]}"/>'
             f'<text class="mono" x="39" y="35" font-size="10" fill="{t["link"]}">{esc(cat)}</text>')
    g.append(f'<text class="mono" x="{W-20}" y="35" text-anchor="end" font-size="10.5" fill="{t["muted"]}">'
             f'{item["date"]:%d.%m.%Y}</text>')
    for k, line in enumerate(wrap(item["title"], 36, 3)):
        g.append(f'<text class="sans" x="20" y="{78 + k * 24}" font-size="17.5" font-weight="600" '
                 f'letter-spacing="-.2" fill="{t["text"]}">{esc(line)}</text>')
    g.append(f'<path d="M20,{H-44} H{W-20}" stroke="{t["border_light"]}"/>')
    g.append(f'<text class="mono" x="20" y="{H-20}" font-size="11" fill="{t["link"]}">Read on onetech.group →</text>')
    return svg(W, H, esc(f'{item["title"]} ({item["date"]:%d.%m.%Y})'), css, "".join(g))


def main():
    items = fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    blocks = []
    for i, item in enumerate(items, 1):
        for mode, t in THEMES.items():
            (OUT / f"news-{i}-{mode}.svg").write_text(card(t, item), encoding="utf-8")
        blocks.append(f'<a href="{esc(item["link"])}"><picture><source media="(prefers-color-scheme: dark)" '
                      f'srcset="./assets/news-{i}-dark.svg"><img alt="{esc(item["title"])}" '
                      f'src="./assets/news-{i}-light.svg" width="32%"></picture></a>')
    readme = README.read_text(encoding="utf-8")
    a, b = readme.index(START) + len(START), readme.index(END)
    new = readme[:a] + "\n<p>\n" + "\n".join(blocks) + "\n</p>\n" + readme[b:]
    README.write_text(new, encoding="utf-8")
    for it in items:
        print(f'{it["date"]:%Y-%m-%d}  {it["title"]}')


if __name__ == "__main__":
    main()
