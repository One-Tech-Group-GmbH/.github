#!/usr/bin/env python3
"""Animated SVGs for the One Tech Group GitHub organization profile.

Run:  python3 tools/build_org_svgs.py   -> writes profile/assets/*.svg (light + dark)
Copy is taken from onetech.group. Palette = OTG Design System tokens.
Fonts (Geist, Space Mono; SIL OFL) are embedded because <img>-rendered SVGs
cannot load external fonts.
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
OUT = ROOT / "profile" / "assets"

THEMES = {
    "light": dict(page="#f9f8f6", card="#ffffff", section="#f5f4f1", border="#e8e5e0",
                  border_light="#f0eeea", text="#1a1a1a", secondary="#5e5b56", muted="#6f6a64",
                  primary="#1d48c0", link="#1d48c0", primary_light="#f0f3fb", primary_subtle="#e4eafa",
                  success="#16a34a", error="#dc2626", idle="#d9d6d0", line="#bdb6ab"),
    "dark": dict(page="#161514", card="#1e1d1b", section="#252422", border="#333130",
                 border_light="#292826", text="#edebe8", secondary="#a8a49e", muted="#98938c",
                 primary="#4d6fd0", link="#7e97e3", primary_light="#1e2a44", primary_subtle="#243056",
                 success="#16a34a", error="#f87171", idle="#3d3a36", line="#55514c"),
}
MONO_ADV = 0.612


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def font_css(geist=True, mono=True, mono_bold=True):
    css = []
    if geist:
        css.append("@font-face{font-family:'Geist';font-weight:100 900;"
                   f"src:url(data:font/woff2;base64,{b64('geist-latin-variable.woff2')}) format('woff2');}}")
    if mono:
        css.append("@font-face{font-family:'Space Mono';font-weight:400;"
                   f"src:url(data:font/woff2;base64,{b64('space-mono-latin-400.woff2')}) format('woff2');}}")
    if mono_bold:
        css.append("@font-face{font-family:'Space Mono';font-weight:700;"
                   f"src:url(data:font/woff2;base64,{b64('space-mono-latin-700.woff2')}) format('woff2');}}")
    return "\n".join(css)


BASE_CSS = """
.sans{font-family:'Geist',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
.mono{font-family:'Space Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def svg(w, h, title, style, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'<style>{style}</style>{body}</svg>\n')


PRODUCTS = [
    ("01", "AdServer1", "Direct sales, booking and", "playout for your inventory.", ["BOOKING", "PLAYOUT"]),
    ("02", "SSP1", "Programmatic monetization", "with full yield control.", ["PG", "PMP", "RTB"]),
    ("03", "DMP1", "Audiences and data signals", "across every touchpoint.", ["AUDIENCES"]),
    ("04", "NMS1", "Operate and monitor your", "whole screen network.", ["MONITORING"]),
]
CHANNELS = ["DOOH", "OOH", "PRINT", "RADIO"]


# ---------------------------------------------------------------- header: the fanned hand
def header(t):
    W, H = 1200, 340
    px, py = 930, 352  # pivot of the hand (below the cards)
    angles = [-21, -7, 7, 21]
    fan = []
    for i, a in enumerate(angles):
        fan.append(f"@keyframes f{i}{{0%,8%{{transform:rotate(0deg)}}30%,78%{{transform:rotate({a}deg)}}96%,100%{{transform:rotate(0deg)}}}}"
                   f".c{i}{{transform-box:view-box;transform-origin:{px}px {py}px;animation:f{i} 9s cubic-bezier(.3,.7,.2,1) infinite}}")
    style = font_css() + BASE_CSS + "".join(fan) + f"""
@media (prefers-reduced-motion: reduce){{{''.join(f'.c{i}{{transform:rotate({a}deg)}}' for i, a in enumerate(angles))}}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion: no-preference){{.in{{opacity:0;animation:rise .7s ease-out forwards}}}}
.d1{{animation-delay:.1s}}.d2{{animation-delay:.3s}}.d3{{animation-delay:.5s}}.d4{{animation-delay:.7s}}
"""
    g = [f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
         f'<circle cx="2" cy="2" r="1.1" fill="{t["border"]}"/></pattern>'
         f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>',
         f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{t["page"]}"/>'
         f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".6"/>']
    # cards
    cw, ch = 156, 214
    for i, (num, name, _, _, _) in enumerate(PRODUCTS):
        x, y = px - cw / 2, py - 66 - ch
        front = i == len(PRODUCTS) - 1
        fill = t["primary"] if front else t["card"]
        ink = "#ffffff" if front else t["text"]
        sub = "#dbe3fb" if front else t["muted"]
        g.append(f'<g class="c{i}">')
        g.append(f'<rect x="{x+3}" y="{y+5}" width="{cw}" height="{ch}" rx="10" fill="#000" opacity=".06"/>')
        g.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{fill}" stroke="{t["primary"] if front else t["border"]}"/>')
        g.append(f'<text class="mono" x="{x+14}" y="{y+26}" font-size="11" letter-spacing="1.4" fill="{sub}">{num} /</text>')
        g.append(f'<text class="mono" x="{x+14}" y="{y+ch-20}" font-size="17" font-weight="700" fill="{ink}">{name}</text>')
        # tiny glyph per product
        gx, gy = x + 14, y + 52
        col = "#ffffff" if front else t["primary"]
        soft = "#ffffff" if front else t["idle"]
        if i == 0:  # calendar
            for r in range(4):
                for c in range(6):
                    on = (r * 6 + c) % 7 != 3
                    g.append(f'<rect x="{gx+c*21}" y="{gy+r*18}" width="16" height="13" rx="2" fill="{col if on else soft}" opacity="{1 if on else .5}"/>')
        elif i == 1:  # one screen sold three ways
            g.append(f'<rect x="{gx}" y="{gy}" width="126" height="44" rx="4" fill="none" stroke="{col}" stroke-width="1.5"/>')
            for k, (w, o) in enumerate([(52, 1), (42, .7), (32, .45)]):
                xx = gx + sum([52, 42, 32][:k])
                g.append(f'<rect x="{xx}" y="{gy+56}" width="{w-3}" height="10" rx="2" fill="{col}" opacity="{o}"/>')
        elif i == 2:  # ranked audiences
            for k, w in enumerate([120, 86, 54]):
                g.append(f'<rect x="{gx}" y="{gy+k*22}" width="{w}" height="12" rx="3" fill="{col}" opacity="{1 - k * .25}"/>')
        else:  # network tiles
            for r in range(4):
                for c in range(6):
                    off = (r, c) == (2, 4)
                    g.append(f'<rect x="{gx+c*21}" y="{gy+r*18}" width="16" height="13" rx="2" fill="{col}" opacity="{.35 if off else .9}"/>')
        g.append('</g>')
    # text block
    x0 = 64
    g.append(f'<text class="mono in d1" x="{x0}" y="112" font-size="13" letter-spacing="2.2" fill="{t["link"]}">THE AD INFRASTRUCTURE FOR PUBLISHERS</text>')
    g.append(f'<text class="sans in d2" x="{x0-3}" y="180" font-size="68" font-weight="640" letter-spacing="-2.4" fill="{t["text"]}">One Tech Group</text>')
    g.append(f'<text class="sans in d3" x="{x0}" y="226" font-size="25" fill="{t["secondary"]}">One to many, with one platform.</text>')
    cx = x0
    g.append('<g class="in d4">')
    for ch_ in CHANNELS:
        w = len(ch_) * 11 * MONO_ADV + 30
        g.append(f'<rect x="{cx}" y="252" width="{w:.0f}" height="26" rx="13" fill="{t["card"]}" stroke="{t["border"]}"/>'
                 f'<circle cx="{cx+13}" cy="265" r="2.5" fill="{t["link"]}"/>'
                 f'<text class="mono" x="{cx+21}" y="269" font-size="11" fill="{t["secondary"]}">{ch_}</text>')
        cx += w + 8
    g.append('</g></g>')
    g.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{t["border"]}"/>')
    return svg(W, H, "One Tech Group. The ad infrastructure for publishers. One to many, with one platform. DOOH, OOH, Print, Radio.",
               style, "".join(g))


# ---------------------------------------------------------------- product cards
def products(t):
    W, H = 1200, 330
    cw, gap = 282, 24
    style = font_css(mono_bold=True) + BASE_CSS + """
@keyframes book{0%,5%{opacity:0}12%,88%{opacity:1}100%{opacity:0}}
.slot{opacity:0;animation:book 7s ease-out infinite}
@keyframes blinkoff{0%,45%{opacity:1}50%,95%{opacity:.15}100%{opacity:1}}
.down{animation:blinkoff 2.4s steps(1) infinite}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media (prefers-reduced-motion: no-preference){.bar{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s cubic-bezier(.2,.7,.3,1) both}}
@media (prefers-reduced-motion: reduce){.slot{opacity:1}}
"""
    g = []
    for i, (num, name, l1, l2, tags) in enumerate(PRODUCTS):
        x = i * (cw + gap)
        g.append(f'<g transform="translate({x},1)">')
        g.append(f'<rect x=".5" y=".5" width="{cw-1}" height="{H-3}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>')
        g.append(f'<text class="mono" x="22" y="36" font-size="11" letter-spacing="1.6" fill="{t["muted"]}">{num} /</text>')
        g.append(f'<rect x="22" y="54" width="{cw-44}" height="120" rx="8" fill="{t["section"]}"/>')
        g.append(f'<g transform="translate(22,54)">{STAGES[i](t, cw - 44)}</g>')
        g.append(f'<text class="mono" x="22" y="218" font-size="21" font-weight="700" fill="{t["text"]}">{name}</text>')
        g.append(f'<text class="sans" x="22" y="250" font-size="14" fill="{t["secondary"]}">{l1}</text>')
        g.append(f'<text class="sans" x="22" y="270" font-size="14" fill="{t["secondary"]}">{l2}</text>')
        tx = 22
        for tag in tags:
            w = len(tag) * 10 * MONO_ADV + 16
            g.append(f'<rect x="{tx}" y="288" width="{w:.0f}" height="20" rx="4" fill="{t["primary_light"]}"/>'
                     f'<text class="mono" x="{tx+8}" y="302" font-size="10" fill="{t["link"]}">{tag}</text>')
            tx += w + 6
        g.append('</g>')
    return svg(W, H, "Four products, one platform: AdServer1 for direct sales, booking and playout; SSP1 for programmatic "
               "monetization with yield control; DMP1 for audiences and data signals; NMS1 to operate and monitor screen networks.",
               style, "".join(g))


def stage_adserver(t, w):
    out = [f'<text class="mono" x="14" y="18" font-size="10" fill="{t["muted"]}">booking calendar</text>']
    cols, rows, cw, ch = 7, 4, 26, 15
    x0, y0 = 14, 28
    k = 0
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (cw + 4), y0 + r * (ch + 4)
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="2.5" fill="{t["card"]}" stroke="{t["border"]}"/>')
            if (r * 7 + c) % 9 not in (4, 8):
                out.append(f'<rect class="slot" style="animation-delay:{k*0.09:.2f}s" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="2.5" fill="{t["primary"]}"/>')
                k += 1
    out.append(f'<text class="mono" x="{w-14}" y="112" text-anchor="end" font-size="10" fill="{t["link"]}">87% booked</text>')
    return "".join(out)


def stage_ssp(t, w):
    out = [f'<rect x="14" y="14" width="{w-28}" height="50" rx="5" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>',
           f'<text class="mono" x="{w/2}" y="44" text-anchor="middle" font-size="11" fill="{t["muted"]}">screen #0417</text>']
    segs = [("PG", .42, 1), ("PMP", .33, .72), ("RTB", .25, .48)]
    x = 14
    full = w - 28
    for k, (lab, f, o) in enumerate(segs):
        ww = full * f - 2
        out.append(f'<rect class="bar" style="animation-delay:{k*0.35:.2f}s" x="{x:.1f}" y="76" width="{ww:.1f}" height="14" rx="3" fill="{t["primary"]}" opacity="{o}"/>')
        out.append(f'<text class="mono" x="{x:.1f}" y="106" font-size="10" fill="{t["secondary"]}">{lab}</text>')
        x += ww + 2
    return "".join(out)


def stage_dmp(t, w):
    out = []
    rows = [("commuters", 1.0, "1.2M"), ("shoppers", .7, "840K"), ("families", .38, "460K")]
    for k, (lab, f, val) in enumerate(rows):
        y = 22 + k * 28
        out.append(f'<text class="mono" x="14" y="{y}" font-size="10" fill="{t["muted"]}">{lab}</text>')
        out.append(f'<rect x="14" y="{y+5}" width="{w-80}" height="9" rx="3" fill="{t["card"]}"/>')
        out.append(f'<rect class="bar" style="animation-delay:{k*0.25:.2f}s" x="14" y="{y+5}" width="{(w-80)*f:.1f}" height="9" rx="3" fill="{t["primary"]}" opacity="{1-k*.2}"/>')
        out.append(f'<text class="mono" x="{w-14}" y="{y+13}" text-anchor="end" font-size="10" fill="{t["secondary"]}">{val}</text>')
    out.append(f'<text class="mono" x="14" y="112" font-size="9.5" fill="{t["link"]}">privacy-first · no personal ids</text>')
    return "".join(out)


def stage_nms(t, w):
    out = []
    cols, rows = 10, 4
    s = 16
    x0 = (w - cols * (s + 4)) / 2 + 2
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (s + 4), 14 + r * (s + 4)
            down = (r, c) == (1, 6)
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{s}" height="{s}" rx="3" fill="{t["card"]}" stroke="{t["border"]}"/>')
            cls = 'class="down" ' if down else ""
            out.append(f'<circle {cls}cx="{x+s/2:.1f}" cy="{y+s/2}" r="3" fill="{t["error"] if down else t["success"]}"/>')
    out.append(f'<text class="mono" x="14" y="112" font-size="10" fill="{t["muted"]}">network status</text>')
    out.append(f'<text class="mono" x="{w-14}" y="112" text-anchor="end" font-size="10" fill="{t["link"]}">39/40 online</text>')
    return "".join(out)


STAGES = [stage_adserver, stage_ssp, stage_dmp, stage_nms]


# ---------------------------------------------------------------- channels -> one pipeline
def channels(t):
    W, H = 1200, 150
    style = font_css(mono_bold=True) + BASE_CSS + """
@keyframes dash{to{stroke-dashoffset:-24}}
.flow{stroke-dasharray:3 9;animation:dash 1.2s linear infinite}
"""
    g = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>',
         f'<text class="sans" x="32" y="66" font-size="24" font-weight="620" letter-spacing="-.5" fill="{t["text"]}">Every channel.</text>',
         f'<text class="sans" x="32" y="96" font-size="24" font-weight="620" letter-spacing="-.5" fill="{t["secondary"]}">One card index.</text>']
    tx, ty = 960, 75
    for i, ch_ in enumerate(CHANNELS):
        y = 30 + i * 30
        x = 420
        path = f"M{x+86},{y} C{x+220},{y} {tx-200},{ty} {tx-120},{ty}"
        g.append(f'<path d="{path}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
        g.append(f'<path class="flow" d="{path}" fill="none" stroke="{t["primary"]}" stroke-width="1.5" opacity=".5"/>')
        g.append(f'<circle r="3.5" fill="{t["primary"]}"><animateMotion dur="2.6s" begin="{i*0.65}s" repeatCount="indefinite" path="{path}"/></circle>')
        g.append(f'<rect x="{x}" y="{y-12}" width="86" height="24" rx="12" fill="{t["section"]}" stroke="{t["border"]}"/>'
                 f'<circle cx="{x+14}" cy="{y}" r="2.5" fill="{t["link"]}"/>'
                 f'<text class="mono" x="{x+24}" y="{y+4}" font-size="11" fill="{t["secondary"]}">{ch_}</text>')
    g.append(f'<rect x="{tx-120}" y="{ty-22}" width="330" height="44" rx="22" fill="{t["primary"]}"/>')
    g.append(f'<text class="mono" x="{tx+45}" y="{ty+5}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="1" '
             f'fill="#ffffff">ONE ORDER · ONE REPORT · ONE INVOICE</text>')
    return svg(W, H, "Every channel, one card index: DOOH, OOH, Print and Radio flow into one order, one report, one invoice.",
               style, "".join(g))


# ---------------------------------------------------------------- link buttons
def button(t, label, icon):
    fs = 14
    w = int(52 + len(label) * fs * 0.56)
    H = 40
    icons = {
        "web": (f'<circle cx="23" cy="20" r="8.5" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'
                f'<ellipse cx="23" cy="20" rx="3.6" ry="8.5" fill="none" stroke="{t["link"]}" stroke-width="1.2"/>'
                f'<line x1="14.5" y1="20" x2="31.5" y2="20" stroke="{t["link"]}" stroke-width="1.2"/>'),
        "careers": (f'<rect x="14" y="14" width="18" height="13" rx="2.5" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'
                    f'<path d="M19.5,14 V11.5 h7 V14" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'),
        "contact": (f'<rect x="14" y="13" width="18" height="14" rx="2.5" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'
                    f'<path d="M14.5,14 L23,21 L31.5,14" fill="none" stroke="{t["link"]}" stroke-width="1.5"/>'),
    }
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{H-1}" rx="8" fill="{t["card"]}" stroke="{t["border"]}"/>'
            + icons[icon] + f'<text class="sans" x="42" y="25" font-size="{fs}" font-weight="560" fill="{t["text"]}">{label}</text>')
    return svg(w, H, label, font_css(mono=False, mono_bold=False) + BASE_CSS, body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [("header", header), ("products", products), ("channels", channels)]
    for mode, t in THEMES.items():
        for name, fn in jobs:
            (OUT / f"{name}-{mode}.svg").write_text(fn(t), encoding="utf-8")
        for name, label, icon in [("web", "onetech.group", "web"), ("careers", "Careers", "careers"),
                                  ("contact", "Contact", "contact")]:
            (OUT / f"btn-{name}-{mode}.svg").write_text(button(t, label, icon), encoding="utf-8")
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
