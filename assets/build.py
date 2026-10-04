#!/usr/bin/env python3
"""Regenerates the profile README artwork.

GitHub strips CSS and scripts from READMEs, so every styled piece is an SVG
loaded through <img>. Each one is emitted in a dark and a light variant and
the README picks between them with <picture>.

    python3 assets/build.py
"""
import math
from pathlib import Path

OUT = Path(__file__).parent

NAME = "Anshuman Kumar"
HANDLE = "a6nkay-source"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(
        bg="#0f1620", bg2="#151e2b", line="#243042", ink="#e8edf4", mute="#8b98a9", faint="#556275",
        teal="#3fd0c0", violet="#a48bff", amber="#f2b248", blue="#5aa9ff", pink="#ff5fa8",
    ),
    "light": dict(
        bg="#f6f4ee", bg2="#ffffff", line="#e2ddd0", ink="#1a1f29", mute="#5e6673", faint="#9aa0a8",
        teal="#0e8f84", violet="#6a4fd8", amber="#b27408", blue="#2670d6", pink="#d02a78",
    ),
}


def svg(w, h, body, t, label, extra_css=""):
    css = f"""
    text{{font-family:{SANS};fill:{t['ink']}}}
    .mono{{font-family:{MONO};letter-spacing:.14em}}
    .mute{{fill:{t['mute']}}} .faint{{fill:{t['faint']}}}
    @keyframes drift{{to{{transform:translateX(-120px)}}}}
    .drift{{animation:drift 9s linear infinite}}
    .drift.slow{{animation-duration:15s}}
    {extra_css}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{label}"><style>{css}</style>{body}</svg>\n'
    )


def wave(y, amp, width, period=120):
    """A sine-ish path one period wider than `width`, so it can drift left and loop."""
    d = f"M0,{y} Q{period / 4},{y - amp} {period / 2},{y}"
    x = period / 2
    while x < width + period:
        x += period / 2
        d += f" T{x},{y}"
    return d


def frame(w, h, t, rx=12):
    return (
        f'<defs><clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r=".8" fill="{t["line"]}"/></pattern></defs>'
        f'<rect width="{w}" height="{h}" rx="{rx}" fill="{t["bg"]}"/>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="{t["line"]}"/>'
    )


def tag(x, y, text, color, size=9):
    return f'<text x="{x}" y="{y}" class="mono" font-size="{size}" fill="{color}" style="fill:{color}">{text}</text>'


# ── hero ──────────────────────────────────────────────────────────────────────
def hero(t):
    W, H = 880, 300
    b = frame(W, H, t, 14)
    b += f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>'
    b += (
        f'<path class="drift slow" d="{wave(268, 9, W)}" fill="none" stroke="{t["teal"]}" stroke-width="1.5" opacity=".35"/>'
        f'<path class="drift" d="{wave(280, 6, W)}" fill="none" stroke="{t["blue"]}" stroke-width="1.5" opacity=".3"/></g>'
    )
    b += tag(40, 42, HANDLE.upper(), t["faint"])
    b += f'<text x="840" y="42" text-anchor="end" class="mono faint" font-size="9">SELECTED WORK · 2026</text>'
    b += f'<line x1="40" y1="58" x2="840" y2="58" stroke="{t["line"]}"/>'
    b += f'<text x="38" y="128" font-size="50" font-weight="700" letter-spacing="-1.5">{NAME}</text>'
    lines = [
        "I train models, then check whether they",
        f'<tspan font-weight="700">actually work</tspan> — on rivers, voices and',
        "markets. Sometimes I just make a game.",
    ]
    for i, l in enumerate(lines):
        b += f'<text x="40" y="{164 + i * 22}" font-size="15.5" class="mute">{l}</text>'
    x = 40
    for n, (name, c) in enumerate(
        [("WATER", "teal"), ("HEALTH", "violet"), ("MARKETS", "amber"), ("LEARNING", "blue"), ("GAMES", "pink")], 1
    ):
        b += tag(x, 248, f"0{n} {name}", t[c])
        x += 28 + len(name) * 7.4 + 18
    cards = [
        ("01 · RESEARCH", "Hydrosense", "Nitrate forecasts for US rivers", "teal"),
        ("02 · RESEARCH", "PD Voice Model", "Tested on unseen cohorts", "violet"),
        ("03 · WEB", "Stock Research Lab", "74 stocks, honest backtests", "amber"),
        ("04 · WEB", "Anchor", "A study space that checks in", "blue"),
    ]
    for i, (k, title, sub, c) in enumerate(cards):
        cx, cy = 492 + (i % 2) * 178, 78 + (i // 2) * 96
        b += (
            f'<rect x="{cx}" y="{cy}" width="168" height="86" rx="9" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
            f'<rect x="{cx}" y="{cy + 14}" width="2.5" height="22" rx="1" fill="{t[c]}"/>'
            + tag(cx + 14, cy + 24, k, t[c], 8)
            + f'<text x="{cx + 14}" y="{cy + 50}" font-size="15" font-weight="650">{title}</text>'
            f'<text x="{cx + 14}" y="{cy + 68}" font-size="10" class="mute">{sub}</text>'
        )
    return svg(W, H, b, t, f"{NAME}: selected work")


# ── project art (440×264) ─────────────────────────────────────────────────────
AW, AH = 440, 264


def art_hydrosense(t):
    c = t["teal"]
    b = frame(AW, AH, t) + tag(24, 32, "01 RESEARCH · WATER QUALITY", t["faint"])
    f = lambda x: 142 - 26 * math.sin(x / 38) - 9 * math.sin(x / 11 + 1)
    obs = " ".join(f"{x},{f(x):.1f}" for x in range(30, 251, 5))
    fc = [(x, f(x) - (x - 250) * 0.12) for x in range(250, 411, 5)]
    spread = lambda x: 4 + (x - 250) * 0.16
    band = " ".join(f"{x},{y - spread(x):.1f}" for x, y in fc) + " " + " ".join(
        f"{x},{y + spread(x):.1f}" for x, y in reversed(fc)
    )
    for gy in (80, 120, 160, 200):
        b += f'<line x1="30" y1="{gy}" x2="410" y2="{gy}" stroke="{t["line"]}" stroke-width=".7"/>'
    b += (
        f'<line x1="30" y1="86" x2="410" y2="86" stroke="{t["pink"]}" stroke-dasharray="3 4" opacity=".8"/>'
        f'<text x="410" y="78" text-anchor="end" font-size="9" style="fill:{t["pink"]}">nitrate limit</text>'
        f'<line x1="250" y1="62" x2="250" y2="206" stroke="{t["faint"]}" stroke-dasharray="2 3"/>'
        f'<text x="246" y="72" text-anchor="end" font-size="9" class="mute">observed</text>'
        f'<text x="255" y="72" font-size="9" style="fill:{c}">forecast</text>'
        f'<polygon points="{band}" fill="{c}" opacity=".16"/>'
        f'<polyline points="{obs}" fill="none" stroke="{t["ink"]}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in fc)}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="5 4"/>'
        f'<circle cx="250" cy="{f(250):.1f}" r="3.5" fill="{t["bg"]}" stroke="{c}" stroke-width="2"/>'
    )
    b += (
        f'<g clip-path="url(#clip)"><path class="drift" d="{wave(236, 6, AW)} V{AH} H0 Z" fill="{c}" opacity=".14"/>'
        f'<path class="drift slow" d="{wave(244, 5, AW)} V{AH} H0 Z" fill="{c}" opacity=".2"/></g>'
    )
    return svg(AW, AH, b, t, "Hydrosense: observed nitrate levels with a forecast and its uncertainty band")


def art_parkinson(t):
    c = t["violet"]
    css = (
        "@keyframes pulse{50%{transform:scaleY(.45)}}"
        ".bar{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}"
    )
    b = frame(AW, AH, t) + tag(24, 32, "02 RESEARCH · VOICE BIOMARKERS", t["faint"])
    for i in range(26):
        h = 14 + 52 * abs(math.sin(i * 0.55) * math.cos(i * 0.21 + 0.4))
        b += (
            f'<rect class="bar" style="animation-delay:{-i * 0.11:.2f}s" x="{30 + i * 7}" y="{138 - h / 2:.1f}" '
            f'width="3.6" height="{h:.1f}" rx="1.8" fill="{c}" opacity="{0.45 + 0.55 * (i % 3) / 2:.2f}"/>'
        )
    b += (
        f'<text x="30" y="204" font-size="10" class="mute">voice recording</text>'
        f'<text x="30" y="219" font-size="10" class="mute">→ shimmer, pitch, jitter</text>'
    )
    x0, y0, s = 262, 62, 148
    b += (
        f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
        f'<line x1="{x0}" y1="{y0 + s}" x2="{x0 + s}" y2="{y0}" stroke="{t["faint"]}" stroke-dasharray="3 4"/>'
        f'<path d="M{x0},{y0 + s} C{x0 + 4},{y0 + 62} {x0 + 44},{y0 + 14} {x0 + s},{y0} V{y0 + s} Z" fill="{c}" opacity=".14"/>'
        f'<path d="M{x0},{y0 + s} C{x0 + 4},{y0 + 62} {x0 + 44},{y0 + 14} {x0 + s},{y0}" fill="none" stroke="{c}" stroke-width="2.2"/>'
        f'<text x="{x0 + s - 10}" y="{y0 + s - 30}" text-anchor="end" font-size="22" font-weight="700">0.88</text>'
        f'<text x="{x0 + s - 10}" y="{y0 + s - 14}" text-anchor="end" font-size="9" class="mute">AUC · unseen cohort</text>'
        f'<text x="{x0}" y="{y0 + s + 16}" font-size="9" class="faint">ROC curve</text>'
    )
    return svg(AW, AH, b, t, "Parkinson's voice model: ROC curve with 0.88 AUC on an unseen cohort", css)


def art_stocks(t):
    b = frame(AW, AH, t) + tag(24, 32, "03 WEB · PORTFOLIO RESEARCH", t["faint"])
    rows = [("Hold every stock equally", 16.1, t["faint"]), ("AI portfolio", 14.5, t["amber"]), ("S&amp;P 500", 11.0, t["faint"])]
    for i, (name, v, col) in enumerate(rows):
        y, w = 74 + i * 46, v * 19.5
        b += (
            f'<text x="30" y="{y}" font-size="11" class="{"mute" if i != 1 else ""}" font-weight="{600 if i == 1 else 400}">{name}</text>'
            f'<rect x="30" y="{y + 8}" width="{w:.0f}" height="16" rx="3" fill="{col}"/>'
            f'<text x="{38 + w:.0f}" y="{y + 20}" font-size="12" font-weight="700">{v}%</text>'
        )
    b += (
        f'<line x1="30" y1="206" x2="410" y2="206" stroke="{t["line"]}"/>'
        f'<text x="30" y="225" font-size="10" class="mute">Return per year, 2006–2026, after costs.</text>'
        f'<text x="30" y="241" font-size="10" class="mute">The no-skill baseline won, and the app says so.</text>'
    )
    return svg(AW, AH, b, t, "Stock research lab backtest: equal-weight 16.1%, AI portfolio 14.5%, S&amp;P 500 11.0% per year")


def art_anchor(t):
    c = t["blue"]
    css = "@keyframes breathe{50%{opacity:.35}} .breathe{animation:breathe 3s ease-in-out infinite}"
    b = frame(AW, AH, t) + tag(24, 32, "04 WEB · STUDY WORKSPACE", t["faint"])
    b += (
        f'<rect x="30" y="50" width="380" height="188" rx="9" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
        f'<line x1="30" y1="72" x2="410" y2="72" stroke="{t["line"]}"/>'
        + "".join(f'<circle cx="{44 + i * 12}" cy="61" r="3" fill="{t["line"]}"/>' for i in range(3))
        + f'<line x1="112" y1="72" x2="112" y2="238" stroke="{t["line"]}"/>'
    )
    for i, w in enumerate([44, 36, 50, 30, 42, 34]):
        on = i == 0
        b += f'<rect x="44" y="{88 + i * 22}" width="{w}" height="6" rx="3" fill="{c if on else t["line"]}"/>'
    circ = 2 * math.pi * 34
    b += (
        f'<circle cx="176" cy="142" r="34" fill="none" stroke="{t["line"]}" stroke-width="7"/>'
        f'<circle cx="176" cy="142" r="34" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" '
        f'stroke-dasharray="{circ * 0.78:.1f} {circ:.1f}" transform="rotate(-90 176 142)"/>'
        f'<circle class="breathe" cx="176" cy="142" r="5" fill="{c}"/>'
        f'<text x="176" y="198" text-anchor="middle" font-size="9" class="mute">wellness</text>'
    )
    for i, lab in enumerate(["posture", "gaze", "typing rhythm"]):
        y = 96 + i * 30
        b += (
            f'<text x="240" y="{y}" font-size="9" class="mute">{lab}</text>'
            f'<rect x="240" y="{y + 6}" width="150" height="5" rx="2.5" fill="{t["line"]}"/>'
            f'<rect x="240" y="{y + 6}" width="{[112, 96, 128][i]}" height="5" rx="2.5" fill="{c}" opacity="{[1, .7, .85][i]}"/>'
        )
    b += (
        f'<rect x="226" y="196" width="172" height="28" rx="14" fill="{c}"/>'
        f'<circle cx="241" cy="210" r="4" fill="{t["bg2"]}"/>'
        f'<text x="252" y="213.5" font-size="10" font-weight="600" style="fill:{t["bg2"]}">Time for a 30s check-in?</text>'
    )
    return svg(AW, AH, b, t, "Anchor: a study dashboard with a wellness ring, live signals and a check-in prompt", css)


def art_neon(t):
    # A game screen: stays dark in both themes.
    cy, pk, yl = "#3df2ff", "#ff3fa4", "#ffe14d"
    css = (
        "@keyframes blink{50%{opacity:.25}} .coin{animation:blink 1.6s ease-in-out infinite}"
        "@keyframes hover{50%{transform:translateY(-5px)}} .player{animation:hover 1.8s ease-in-out infinite}"
    )
    hz = 150
    b = (
        f'<defs><clipPath id="clip"><rect width="{AW}" height="{AH}" rx="12"/></clipPath>'
        f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0620"/><stop offset="1" stop-color="#2a0f4a"/></linearGradient>'
        f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{yl}"/><stop offset="1" stop-color="{pk}"/></linearGradient>'
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        f'<g clip-path="url(#clip)"><rect width="{AW}" height="{AH}" fill="url(#sky)"/>'
        f'<circle cx="220" cy="{hz - 8}" r="52" fill="url(#sun)"/>'
        + "".join(f'<rect x="160" y="{hz - 40 + i * 9}" width="120" height="{1.5 + i * .6}" fill="#1c0a38"/>' for i in range(5))
        + f'<rect y="{hz}" width="{AW}" height="{AH - hz}" fill="#0b0620"/>'
    )
    for i in range(-9, 10):
        b += f'<line x1="{220 + i * 14}" y1="{hz}" x2="{220 + i * 90}" y2="{AH}" stroke="{pk}" stroke-width=".8" opacity=".55"/>'
    y, step = hz, 5.0
    while y < AH:
        b += f'<line x1="0" y1="{y:.1f}" x2="{AW}" y2="{y:.1f}" stroke="{pk}" stroke-width=".8" opacity=".55"/>'
        y += step
        step *= 1.38
    b += f'<line x1="0" y1="{hz}" x2="{AW}" y2="{hz}" stroke="{cy}" stroke-width="1.5" filter="url(#glow)"/>'
    for i, (x, yy) in enumerate([(150, 196), (196, 188), (242, 196)]):
        b += f'<circle class="coin" style="animation-delay:{-i * .4}s" cx="{x}" cy="{yy}" r="5" fill="{yl}" filter="url(#glow)"/>'
    b += (
        f'<rect class="player" x="88" y="198" width="22" height="22" rx="4" fill="none" stroke="{cy}" stroke-width="2.5" filter="url(#glow)"/>'
        f'<path d="M318,222 l14,-26 l14,26 z" fill="none" stroke="{pk}" stroke-width="2.5" stroke-linejoin="round" filter="url(#glow)"/>'
        f'<text x="220" y="76" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="5" '
        f'style="fill:{cy};font-family:{MONO}" filter="url(#glow)">NEON ESCAPE</text></g>'
        f'<text x="24" y="32" class="mono" font-size="9" style="fill:#9a86c9">05 GAME · PYTHON</text>'
        f'<text x="416" y="32" text-anchor="end" class="mono" font-size="9" style="fill:{yl}">LEVEL 1 / 3</text>'
    )
    return svg(AW, AH, b, t, "Neon Escape: a neon arcade scene with a player, coins and an enemy", css)


ART = {
    "hero": hero,
    "hydrosense": art_hydrosense,
    "parkinson": art_parkinson,
    "stocks": art_stocks,
    "anchor": art_anchor,
    "neon": art_neon,
}

if __name__ == "__main__":
    for name, fn in ART.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t))
    print(f"wrote {len(ART) * len(THEMES)} files to {OUT}")
