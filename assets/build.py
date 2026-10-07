#!/usr/bin/env python3
"""Regenerates the profile README artwork.

GitHub strips CSS and scripts from READMEs, so every styled piece is an SVG
loaded through <img>. The project cards wrap real captures from each project
(assets/shots/*.jpg) in an animated window frame; the images are inlined as
base64 because an SVG shown through <img> cannot load external files.

    python3 assets/build.py
"""
import base64
from pathlib import Path

OUT = Path(__file__).parent
SHOTS = OUT / "shots"

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


def svg(w, h, body, css, label):
    css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
        f"<style>{css}</style>{body}</svg>\n"
    )


def data_uri(name):
    return "data:image/jpeg;base64," + base64.b64encode((SHOTS / f"{name}.jpg").read_bytes()).decode()


# ── hero ──────────────────────────────────────────────────────────────────────
# Lines the terminal strip types out, one after another.
TYPED = [
    "med-tech: Parkinson's voice AI, 4 cohorts, 366 subjects",
    "business: 74 stocks, 20-year walk-forward backtests",
    "stack: Python · PyTorch · LightGBM · TypeScript · Next.js",
]
LINE_SECONDS = 4.5


def ecg(y, width, beat=176):
    """A heartbeat trace one beat wider than `width`, so it can drift left and loop."""
    d, x = f"M0,{y}", 0
    while x < width + beat:
        d += (
            f" H{x + 58} l7,-5 l7,5 h10 l5,5 l8,-34 l8,44 l6,-15 h14"
            f" q10,-13 20,0"
        )
        x += beat
    return d + f" H{x}"


def hero(t):
    W, H = 880, 340
    n, total = len(TYPED), len(TYPED) * LINE_SECONDS
    show = 100 / n
    css = f"""
    text{{font-family:{SANS};fill:{t['ink']}}}
    .mono{{font-family:{MONO}}} .sp{{letter-spacing:.14em}}
    .mute{{fill:{t['mute']}}} .faint{{fill:{t['faint']}}}
    @keyframes drift{{to{{transform:translateX(-176px)}}}}
    .ecg{{animation:drift 3.2s linear infinite}}
    @keyframes type{{0%{{transform:translateX(0)}}55%,100%{{transform:translateX(404px)}}}}
    .cover{{animation:type {LINE_SECONDS}s steps(52,end) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .caret{{animation:blink .9s steps(1) infinite}}
    @keyframes show{{0%,{show - .1:.2f}%{{opacity:1}}{show:.2f}%,100%{{opacity:0}}}}
    .ln{{opacity:0;animation:show {total}s linear infinite}}
    @keyframes rise{{from{{opacity:0;transform:translateY(10px)}}}}
    .card{{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}}
    @keyframes pulse{{50%{{opacity:.35}}}}
    .live{{animation:pulse 1.6s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{.cover{{display:none}}.ln:first-of-type{{opacity:1}}}}
    """
    b = (
        f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        f'<clipPath id="term"><rect x="62" y="212" width="388" height="34"/></clipPath>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r=".8" fill="{t["line"]}"/></pattern>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t["bg"]}"/>'
        f'<stop offset=".12" stop-color="{t["bg"]}" stop-opacity="0"/><stop offset=".88" stop-color="{t["bg"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{t["bg"]}"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>'
        f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>'
        f'<path class="ecg" d="{ecg(312, W)}" fill="none" stroke="{t["teal"]}" stroke-width="1.6" '
        f'stroke-linejoin="round" opacity=".55"/><rect y="262" width="{W}" height="78" fill="url(#fade)"/></g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{t["line"]}"/>'
    )
    b += f'<text x="40" y="42" class="mono sp faint" font-size="9">{HANDLE.upper()}</text>'
    b += (
        f'<circle class="live" cx="641" cy="39" r="3" fill="{t["teal"]}"/>'
        f'<text x="840" y="42" text-anchor="end" class="mono sp faint" font-size="9">BUILDING · RESEARCHING · 2026</text>'
    )
    b += f'<line x1="40" y1="58" x2="840" y2="58" stroke="{t["line"]}"/>'
    b += f'<text x="38" y="122" font-size="50" font-weight="700" letter-spacing="-1.5">{NAME}</text>'
    for i, l in enumerate(
        [
            "I build and validate machine-learning systems for",
            f'<tspan font-weight="700" style="fill:{t["ink"]}">health, finance and the environment</tspan>, then test',
            "them on data they have never seen.",
        ]
    ):
        b += f'<text x="40" y="{154 + i * 21}" font-size="15" class="mute">{l}</text>'

    # terminal strip
    b += (
        f'<rect x="40" y="212" width="420" height="34" rx="7" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
        f'<text x="52" y="234" class="mono" font-size="12" font-weight="700" style="fill:{t["teal"]}">›</text>'
        f'<g clip-path="url(#term)">'
    )
    for i, line in enumerate(TYPED):
        b += (
            f'<text class="ln mono" style="animation-delay:{i * LINE_SECONDS}s" x="66" y="234" '
            f'font-size="11">{line}</text>'
        )
    b += (
        f'<g class="cover"><rect x="64" y="214" width="420" height="30" fill="{t["bg2"]}"/>'
        f'<rect class="caret" x="65" y="222" width="6.5" height="14" fill="{t["teal"]}"/></g></g>'
    )

    x = 40
    for k, (name, c) in enumerate(
        [("MED-TECH", "violet"), ("RESEARCH", "teal"), ("BUSINESS", "amber"), ("ENGINEERING", "blue")], 1
    ):
        b += f'<text x="{x}" y="268" class="mono sp" font-size="9" style="fill:{t[c]}">0{k} {name}</text>'
        x += 28 + len(name) * 7.4 + 18

    cards = [
        ("01 · MED-TECH", "Parkinson's Voice AI", "4 cohorts · 366 subjects", "violet"),
        ("02 · HEALTH", "Anchor", "Wellness signals, on-device", "blue"),
        ("03 · BUSINESS", "Stock Research Lab", "74 stocks · 20-year backtest", "amber"),
        ("04 · ENVIRONMENT", "Hydrosense", "359 USGS river stations", "teal"),
    ]
    for i, (k, title, sub, c) in enumerate(cards):
        cx, cy = 492 + (i % 2) * 178, 78 + (i // 2) * 96
        b += (
            f'<g class="card" style="animation-delay:{.15 + i * .12:.2f}s">'
            f'<rect x="{cx}" y="{cy}" width="168" height="86" rx="9" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
            f'<rect x="{cx}" y="{cy + 14}" width="2.5" height="22" rx="1" fill="{t[c]}"/>'
            f'<text x="{cx + 14}" y="{cy + 24}" class="mono sp" font-size="8" style="fill:{t[c]}">{k}</text>'
            f'<text x="{cx + 14}" y="{cy + 50}" font-size="15" font-weight="650">{title}</text>'
            f'<text x="{cx + 14}" y="{cy + 68}" font-size="10" class="mute">{sub}</text></g>'
        )
    return svg(W, H, b, css, f"{NAME}: machine learning for health, finance and the environment")


# ── project cards: real captures in an animated window ────────────────────────
CW, CH, BAR = 880, 600, 40
VIEW = CH - BAR  # 560: the captures are 880×560
WIN = dict(bg="#0d1117", bar="#161b22", line="#30363d", ink="#c9d1d9", mute="#7d8590")


def window(title, accent, inner, css, label):
    css = f"text{{font-family:{MONO}}}" + css
    b = (
        f'<defs><clipPath id="win"><rect width="{CW}" height="{CH}" rx="14"/></clipPath>'
        f'<clipPath id="view"><rect y="{BAR}" width="{CW}" height="{VIEW}"/></clipPath></defs>'
        f'<g clip-path="url(#win)"><rect width="{CW}" height="{CH}" fill="{WIN["bg"]}"/>'
        f'<g clip-path="url(#view)">{inner}</g>'
        f'<rect width="{CW}" height="{BAR}" fill="{WIN["bar"]}"/>'
        f'<line y1="{BAR}" x2="{CW}" y2="{BAR}" stroke="{WIN["line"]}"/>'
        + "".join(f'<circle cx="{24 + i * 20}" cy="20" r="6" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
        + f'<text x="{CW / 2}" y="25" text-anchor="middle" font-size="14" fill="{WIN["ink"]}">{title}</text>'
        f'<circle class="live" cx="{CW - 28}" cy="20" r="5" fill="{accent}"/></g>'
        f'<rect x=".75" y=".75" width="{CW - 1.5}" height="{CH - 1.5}" rx="14" fill="none" stroke="{WIN["line"]}" stroke-width="1.5"/>'
    )
    css += "@keyframes live{50%{opacity:.3}} .live{animation:live 1.6s ease-in-out infinite}"
    return svg(CW, CH, b, css, label)


def chip(cls, text, accent):
    w = 30 + len(text) * 8.6
    return (
        f'<g class="{cls}"><rect x="20" y="{CH - 54}" width="{w:.0f}" height="34" rx="17" fill="#0d1117" '
        f'fill-opacity=".86" stroke="{accent}" stroke-opacity=".7"/>'
        f'<text x="{20 + w / 2:.0f}" y="{CH - 32}" text-anchor="middle" font-size="14" fill="#e6edf3">{text}</text></g>'
    )


def crossfade(title, accent, shots, label, seconds=7):
    """Cycles through real screenshots with a slow push-in on each."""
    n = len(shots)
    total = n * seconds
    on, fade = 100 / n, 6
    css = (
        # each shot fades in just before its slot and out just after, so one is always showing
        f"@keyframes cut{{0%,{on:.2f}%{{opacity:1}}{on + fade:.2f}%,{100 - fade}%{{opacity:0}}100%{{opacity:1}}}}"
        f"@keyframes push{{0%{{transform:scale(1)}}{on + fade:.2f}%,100%{{transform:scale(1.05)}}}}"
        f".s{{opacity:0;animation:cut {total}s linear infinite}}"
        f".s image{{transform-origin:440px 320px;animation:push {total}s linear infinite}}"
        f"@keyframes bar{{from{{transform:scaleX(0)}}}}"
        f".prog{{transform-origin:0 0;animation:bar {seconds}s linear infinite}}"
        # with motion off, leave the first screenshot showing
        "@media (prefers-reduced-motion:reduce){.s:first-of-type{opacity:1}}"
    )
    inner = ""
    for i, (shot, caption) in enumerate(shots):
        d = f"animation-delay:{i * seconds - total}s"
        inner += (
            f'<g class="s" style="{d}"><image style="{d}" href="{data_uri(shot)}" y="{BAR}" width="{CW}" height="{VIEW}"/>'
            + chip("", caption, accent)
            + "</g>"
        )
    inner += f'<rect class="prog" y="{CH - 4}" width="{CW}" height="4" fill="{accent}"/>'
    return window(title, accent, inner, css, label)


def pan(title, accent, shot, width, caption, label, seconds=22):
    """Slides a wide figure sideways and back, pausing on each panel."""
    travel = width - CW
    css = (
        f"@keyframes pan{{0%,10%{{transform:translateX(0)}}32%,42%{{transform:translateX(-{travel / 2:.0f}px)}}"
        f"64%,78%{{transform:translateX(-{travel}px)}}100%{{transform:translateX(0)}}}}"
        f".pan{{animation:pan {seconds}s ease-in-out infinite}}"
    )
    inner = (
        f'<rect y="{BAR}" width="{CW}" height="{VIEW}" fill="#fff"/>'
        f'<image class="pan" href="{data_uri(shot)}" y="{BAR}" width="{width}" height="{VIEW}"/>'
        + chip("", caption, accent)
    )
    return window(title, accent, inner, css, label)


CARDS = {
    "parkinson": lambda: pan(
        "Parkinson's voice model · cross-cohort results", "#a48bff", "parkinson-figure", 1453,
        "figure from the repo", "Research figure: cross-cohort ROC-AUC, reliability and biomarker stability",
    ),
    "anchor": lambda: crossfade(
        "Anchor · study + wellness workspace", "#22d3ee",
        [("anchor-overview", "Overview"), ("anchor-burnout", "Burnout forecast")],
        "Screenshots of the Anchor app: wellness overview and burnout forecast",
    ),
    "hydrosense": lambda: crossfade(
        "Hydrosense · water-quality forecasting", "#3fd0c0",
        [("hydrosense-national", "National dashboard"), ("hydrosense-live", "Live transport model")],
        "Screenshots of Hydrosense: national station map and the live Alameda Creek transport model",
    ),
    "stocks": lambda: crossfade(
        "AI Stock Research Lab", "#f2b248",
        [("stocks-backtest", "Backtest vs benchmarks"), ("stocks-market", "Market view")],
        "Screenshots of the stock research app: backtest results and market view",
    ),
}

if __name__ == "__main__":
    written = 0
    for theme, t in THEMES.items():
        (OUT / f"hero-{theme}.svg").write_text(hero(t))
        written += 1
    for name, make in CARDS.items():
        try:
            (OUT / f"{name}.svg").write_text(make())
            written += 1
        except FileNotFoundError as e:
            print(f"skipped {name}: missing {e.filename}")
    print(f"wrote {written} files to {OUT}")
