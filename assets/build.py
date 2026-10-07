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
    "med-tech: SurgiVision, surgical video segmentation",
    "business: 74 stocks, 20-year walk-forward backtests",
    "stack: Python · PyTorch · LightGBM · TypeScript · Next.js",
]
LINE_SECONDS = 4.5
INTERESTS = [("Biology", "violet"), ("Business", "amber"), ("Technology", "blue"), ("Future of AI", "teal")]


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
    W, H = 880, 468
    PX, PY, PR = 150, 196, 82  # portrait centre and radius
    TX = 296  # left edge of the text column
    n, total = len(TYPED), len(TYPED) * LINE_SECONDS
    show = 100 / n
    css = f"""
    text{{font-family:{SANS};fill:{t['ink']}}}
    .mono{{font-family:{MONO}}} .sp{{letter-spacing:.14em}}
    .mute{{fill:{t['mute']}}} .faint{{fill:{t['faint']}}}
    @keyframes drift{{to{{transform:translateX(-176px)}}}}
    .ecg{{animation:drift 3.2s linear infinite}}
    @keyframes type{{0%{{transform:translateX(0)}}55%,100%{{transform:translateX(424px)}}}}
    .cover{{animation:type {LINE_SECONDS}s steps(54,end) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .caret{{animation:blink .9s steps(1) infinite}}
    @keyframes show{{0%,{show - .1:.2f}%{{opacity:1}}{show:.2f}%,100%{{opacity:0}}}}
    .ln{{opacity:0;animation:show {total}s linear infinite}}
    @keyframes pulse{{50%{{opacity:.35}}}}
    .live{{animation:pulse 1.6s ease-in-out infinite}}
    .o{{transform-origin:{PX}px {PY}px}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .cw{{animation:spin 14s linear infinite}}
    .ccw{{animation:spin 30s linear infinite reverse}}
    .orbit{{animation:spin 11s linear infinite}}
    @keyframes ping{{0%{{transform:scale(1);opacity:.55}}70%,100%{{transform:scale(1.42);opacity:0}}}}
    .ping{{animation:ping 3.6s ease-out infinite}}
    @keyframes glow{{50%{{opacity:.9;transform:scale(1.06)}}}}
    .glow{{opacity:.55;animation:glow 5s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{.cover{{display:none}}.ln:first-of-type{{opacity:1}}.ping{{opacity:0}}}}
    """
    b = (
        f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        f'<clipPath id="term"><rect x="{TX + 22}" y="272" width="412" height="34"/></clipPath>'
        f'<clipPath id="face"><circle cx="{PX}" cy="{PY}" r="{PR}"/></clipPath>'
        f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r=".8" fill="{t["line"]}"/></pattern>'
        f'<radialGradient id="halo"><stop offset=".55" stop-color="{t["teal"]}" stop-opacity=".32"/>'
        f'<stop offset="1" stop-color="{t["teal"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="arc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["teal"]}"/>'
        f'<stop offset=".5" stop-color="{t["blue"]}"/><stop offset="1" stop-color="{t["violet"]}"/></linearGradient>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t["bg"]}"/>'
        f'<stop offset=".12" stop-color="{t["bg"]}" stop-opacity="0"/><stop offset=".88" stop-color="{t["bg"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{t["bg"]}"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>'
        f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#dots)" opacity=".55"/>'
        f'<path class="ecg" d="{ecg(444, W)}" fill="none" stroke="{t["teal"]}" stroke-width="1.6" '
        f'stroke-linejoin="round" opacity=".5"/><rect y="396" width="{W}" height="72" fill="url(#fade)"/></g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{t["line"]}"/>'
    )
    b += f'<text x="40" y="42" class="mono sp faint" font-size="9">{HANDLE.upper()}</text>'
    b += (
        f'<circle class="live" cx="641" cy="39" r="3" fill="{t["teal"]}"/>'
        f'<text x="840" y="42" text-anchor="end" class="mono sp faint" font-size="9">BUILDING · RESEARCHING · 2026</text>'
    )
    b += f'<line x1="40" y1="58" x2="840" y2="58" stroke="{t["line"]}"/>'

    # portrait: halo, sonar ping, two counter-rotating rings and three orbiting dots
    b += (
        f'<circle class="o glow" cx="{PX}" cy="{PY}" r="{PR + 40}" fill="url(#halo)"/>'
        f'<circle class="o ping" cx="{PX}" cy="{PY}" r="{PR + 2}" fill="none" stroke="{t["teal"]}" stroke-width="1.5"/>'
        f'<circle class="o ping" style="animation-delay:-1.8s" cx="{PX}" cy="{PY}" r="{PR + 2}" fill="none" '
        f'stroke="{t["violet"]}" stroke-width="1.5"/>'
        f'<circle class="o ccw" cx="{PX}" cy="{PY}" r="{PR + 22}" fill="none" stroke="{t["faint"]}" stroke-width="1" '
        f'stroke-dasharray="2 9" stroke-linecap="round"/>'
        f'<image href="{data_uri("portrait")}" x="{PX - PR}" y="{PY - PR}" width="{PR * 2}" height="{PR * 2}" '
        f'clip-path="url(#face)" preserveAspectRatio="xMidYMid slice"/>'
        f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="{t["bg"]}" stroke-width="3"/>'
        f'<circle class="o cw" cx="{PX}" cy="{PY}" r="{PR + 8}" fill="none" stroke="url(#arc)" stroke-width="3" '
        f'stroke-dasharray="{(PR + 8) * 3.9:.0f} {(PR + 8) * 2.4:.0f}" stroke-linecap="round"/>'
    )
    for i, (c, r, dur) in enumerate([("violet", 5, 11), ("amber", 4, 17), ("blue", 3.5, 23)]):
        b += (
            f'<g class="o orbit" style="animation-duration:{dur}s;animation-delay:-{i * 4}s">'
            f'<circle cx="{PX}" cy="{PY - PR - 22}" r="{r}" fill="{t[c]}"/>'
            f'<circle cx="{PX}" cy="{PY - PR - 22}" r="{r + 4}" fill="{t[c]}" opacity=".22"/></g>'
        )

    b += f'<text x="{TX - 2}" y="124" font-size="48" font-weight="700" letter-spacing="-1.5">{NAME}</text>'
    b += f'<text x="{TX}" y="150" font-size="14" class="mute">Machine learning · research · product</text>'
    for i, l in enumerate(
        [
            "I build and validate machine-learning systems for "
            f'<tspan font-weight="700" style="fill:{t["ink"]}">health, finance</tspan>',
            f'<tspan font-weight="700" style="fill:{t["ink"]}">and the environment</tspan>, then test them on data they have never seen.',
        ]
    ):
        b += f'<text x="{TX}" y="{186 + i * 22}" font-size="15" class="mute">{l}</text>'

    # interests
    b += f'<text x="{TX}" y="251" class="mono sp faint" font-size="9">INTERESTED IN</text>'
    x = TX + 104
    for name, c in INTERESTS:
        w = 24 + len(name) * 6.6
        b += (
            f'<rect x="{x}" y="234" width="{w:.0f}" height="26" rx="13" fill="{t[c]}" fill-opacity=".12" '
            f'stroke="{t[c]}" stroke-opacity=".55"/>'
            f'<text x="{x + w / 2:.0f}" y="251.5" text-anchor="middle" font-size="12" font-weight="600" '
            f'style="fill:{t[c]}">{name}</text>'
        )
        x += w + 8

    # terminal strip
    b += (
        f'<rect x="{TX}" y="272" width="444" height="34" rx="7" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
        f'<text x="{TX + 12}" y="294" class="mono" font-size="12" font-weight="700" style="fill:{t["teal"]}">›</text>'
        f'<g clip-path="url(#term)">'
    )
    for i, line in enumerate(TYPED):
        b += (
            f'<text class="ln mono" style="animation-delay:{i * LINE_SECONDS}s" x="{TX + 26}" y="294" '
            f'font-size="11.5">{line}</text>'
        )
    b += (
        f'<g class="cover"><rect x="{TX + 24}" y="274" width="440" height="30" fill="{t["bg2"]}"/>'
        f'<rect class="caret" x="{TX + 25}" y="282" width="6.5" height="14" fill="{t["teal"]}"/></g></g>'
    )

    cards = [
        ("01 · MED-TECH", "Parkinson's Voice AI", "4 cohorts · 366 subjects", "violet"),
        ("02 · HEALTH", "Anchor", "Wellness signals, on-device", "blue"),
        ("03 · BUSINESS", "Stock Research Lab", "74 stocks · 20-year backtest", "amber"),
        ("04 · ENVIRONMENT", "Hydrosense", "359 USGS river stations", "teal"),
    ]
    for i, (k, title, sub, c) in enumerate(cards):
        cx, cy = 40 + i * 203, 330
        b += (
            '<g>'
            f'<rect x="{cx}" y="{cy}" width="191" height="72" rx="9" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
            f'<rect x="{cx}" y="{cy + 12}" width="2.5" height="20" rx="1" fill="{t[c]}"/>'
            f'<text x="{cx + 14}" y="{cy + 21}" class="mono sp" font-size="8" style="fill:{t[c]}">{k}</text>'
            f'<text x="{cx + 14}" y="{cy + 42}" font-size="14.5" font-weight="650">{title}</text>'
            f'<text x="{cx + 14}" y="{cy + 59}" font-size="10" class="mute">{sub}</text></g>'
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
    "surgivision": lambda: crossfade(
        "SurgiVision · surgical vision research", "#f87171",
        [("surgivision-pov", "Live segmentation on the demo clip"), ("surgivision-research", "Research workspace")],
        "Screenshots of SurgiVision: live segmentation of a synthetic laparoscopic clip, and the research workspace",
    ),
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
        [("stocks-overview", "Portfolio overview"), ("stocks-backtest", "Backtest results")],
        "Screenshots of the stock research app: portfolio overview and backtest results",
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
