"""Builds assets/terminal.svg: a terminal window that types out who you are, in Vigless colours.
Each line's width is pinned with textLength, so the typing lands on whole characters in any monospace font."""
from pathlib import Path
from xml.sax.saxutils import escape

W, CH, LH, X0, Y0 = 880, 9.0, 27, 26, 74
GREEN, GOLD, INK, WHITE, GREY = "#00C896", "#D4AF37", "#0A0A0A", "#EDEDED", "#9A9A9A"
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
TYPE = 0.075      # seconds per typed character
PROMPT = [("cam3ronport3r@thecore", GREEN), (":", WHITE), ("~", GOLD), ("$ ", WHITE)]
PLEN = sum(len(t) for t, _ in PROMPT)

# (kind, parts) where parts = [(text, colour, bold)]
LINES = [
    ("cmd", "whoami"),
    ("out", [("cameron", WHITE, True), (" · founder of ", GREY, False), ("vigless", GREEN, True),
             (" · i build bots and models that hunt for edges", GREY, False)]),
    ("cmd", "cat motto.txt"),
    ("out", [("process over ", WHITE, True), ("picks.", GREEN, True)]),
    ("cmd", "ls ~/bots"),
    ("out", [("vigless/", GREEN, True), ("   gamelines/", GREEN, True), ("   tiktok-autoposter/", GREEN, True),
             ("   whop-webhook/", GREEN, True), ("   thecore/", GREEN, True)]),
    ("cmd", "ls ~/models"),
    ("out", [("gamelines/", GOLD, True), ("   tennis/", GOLD, True), ("   longterm/", GOLD, True),
             ("   move-estimator/", GOLD, True)]),
    ("cursor", None),
]

H = Y0 + LH * (len(LINES) - 1) + 34
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
       f'aria-label="cam3ronport3r: founder of Vigless, building bots and models that hunt for edges. Process over picks.">',
       f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{INK}" stroke="#262626"/>',
       f'<path d="M0.5 34 V12.5 a12 12 0 0 1 12 -12 H{W-12.5} a12 12 0 0 1 12 12 V34 Z" fill="#151515"/>',
       f'<line x1="0" y1="34" x2="{W}" y2="34" stroke="#262626"/>',
       '<circle cx="22" cy="17.5" r="6" fill="#FF5F57"/><circle cx="42" cy="17.5" r="6" fill="#FEBC2E"/>'
       '<circle cx="62" cy="17.5" r="6" fill="#28C840"/>',
       f'<text x="{W/2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#7A7A7A">'
       f'cam3ronport3r@thecore: ~</text>']


def text(x, y, parts, n, extra=""):
    spans = "".join(f'<tspan fill="{c}"{" font-weight=\"700\"" if b else ""}>{escape(t)}</tspan>' for t, c, b in parts)
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="15" textLength="{n*CH:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" xml:space="preserve"{extra}>{spans}</text>')


t = 0.5
for i, (kind, body) in enumerate(LINES):
    y = Y0 + LH * i
    if kind in ("cmd", "cursor"):
        out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                   + text(X0, y, [(s, c, True) for s, c in PROMPT], PLEN) + '</g>')
        cx = X0 + PLEN * CH
        if kind == "cursor":
            out.append(f'<rect x="{cx+2:.1f}" y="{y-14}" width="9" height="18" fill="{GREEN}" opacity="0">'
                       f'<animate attributeName="opacity" values="1;0" dur="1.1s" begin="{t:.2f}s" '
                       f'repeatCount="indefinite" calcMode="discrete"/></rect>')
            break
        n = len(body)
        dur = max(n * TYPE, 0.2)
        steps = ";".join(f"{k*CH:.1f}" for k in range(n + 1))
        cid = f"c{i}"
        out.append(f'<clipPath id="{cid}"><rect x="{cx:.1f}" y="{y-18}" width="0" height="24">'
                   f'<animate attributeName="width" values="{steps}" dur="{dur:.2f}s" begin="{t+0.15:.2f}s" '
                   f'fill="freeze" calcMode="discrete"/></rect></clipPath>')
        out.append(text(cx, y, [(body, WHITE, False)], n, f' clip-path="url(#{cid})"'))
        t += 0.15 + dur + 0.35
    else:
        n = sum(len(s) for s, _, _ in body)
        out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                   + text(X0, y, body, n) + '</g>')
        t += 0.45
out.append("</svg>")
dest = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
dest.parent.mkdir(exist_ok=True)
dest.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size} bytes), animation ends at {t:.1f}s")
