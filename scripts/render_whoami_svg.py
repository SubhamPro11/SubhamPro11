#!/usr/bin/env python3
"""Terminal-style 'whoami' card, same 840x880 canvas as stats.svg so they sit side by side.
Edit the LINES list below; every line is typed in once, then the cursor blinks."""
import html, os
from theme import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "whoami.svg")
W, H, PAD, BAR = 840, 880, 28, 30

GLYPHS = {
    "C": [" #### ", "#    #", "#     ", "#    #", " #### "],
    "R": ["##### ", "#    #", "##### ", "#   # ", "#    #"],
    "Y": ["#    #", " #  # ", "  ##  ", "  ##  ", "  ##  "],
    "O": [" #### ", "#    #", "#    #", "#    #", " #### "],
}
LOGO = ["  ".join(GLYPHS[ch][r] for ch in "CRYO") for r in range(5)]

# (kind, label, value)  kind: p = prompt, k = key/value, c = continuation, b = blank
LINES = [
    ("p", "whoami", ""),
    ("k", "name", "Subham Kumar (Cryo)"),
    ("k", "role", "AI & computer vision engineer"),
    ("c", "", "solo full-stack builder"),
    ("k", "study", "B.Tech CSE, Parul University '27"),
    ("k", "base", "India"),
    ("k", "stack", "Next.js, React, TypeScript, Python"),
    ("k", "infra", "Supabase, Cloudflare, Docker"),
    ("k", "ai", "Claude Code, Cursor, Codex, n8n, MCP"),
    ("k", "certs", "AWS Cloud Foundations"),
    ("c", "", "AWS Solutions Architecture"),
    ("b", "", ""),
    ("p", "ls ~/shipping", ""),
    ("k", "crawlers", "crawlers.dpdns.org"),
    ("k", "aurawalls", "aurawalls.qzz.io"),
    ("k", "airwaves", "playit.morbius.workers.dev"),
    ("k", "lockscreen", "github.com/SubhamPro11/lockscreengtf"),
    ("b", "", ""),
    ("p", "cat now.txt", ""),
    ("k", "focus", "Crawlers SEO + Core Web Vitals"),
]
FS, LH, LABEL_W = 20, 31, 140
logo_fs, logo_lh = 26, 26

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
     f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>',
     f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{FRAME}"/>',
     f'<line x1="0" y1="{BAR}" x2="{W}" y2="{BAR}" stroke="{FRAME}"/>',
     f'<text x="{PAD}" y="20" font-size="13" fill="{MUTED}">{HANDLE}@github:~$ <tspan fill="{LIME}">./whoami.sh</tspan></text>']

CELLW, CELLH = 15, 15
y0 = BAR + 30
for ri, row in enumerate(LOGO):
    for ci, ch in enumerate(row):
        if ch != " ":
            p.append(f'<rect x="{PAD + ci*CELLW}" y="{y0 + ri*CELLH}" width="{CELLW-2}" height="{CELLH-2}" fill="{LIME}"/>')
y = y0 + len(LOGO) * CELLH + 52
sep = y - 22
p.append(f'<line x1="{PAD}" y1="{sep}" x2="{W-PAD}" y2="{sep}" stroke="{FRAME}"/>')

n = 0
for kind, a, b in LINES:
    if kind == "b":
        y += LH // 2
        continue
    if kind == "p":
        body = f'<tspan fill="{LIME}">$</tspan> <tspan fill="{INK}">{html.escape(a)}</tspan>'
        svg = f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{MUTED}">{body}</text>'
        width = (len(a) + 2) * FS * 0.62
    else:
        key = f'<tspan fill="{MUTED}">{html.escape(a)}</tspan>' if a else ""
        svg = (f'<text x="{PAD}" y="{y}" font-size="{FS}">{key}</text>'
               f'<text x="{PAD+LABEL_W}" y="{y}" font-size="{FS}" fill="{INK}">{html.escape(b)}</text>')
        width = W
    if STATIC:
        p.append(svg)
    else:
        d = 0.35 + n * 0.16
        p.append(f'<clipPath id="l{n}"><rect x="{PAD-2}" y="{y-FS}" height="{LH}" width="0">'
                 f'<animate attributeName="width" from="0" to="{width:.0f}" begin="{d:.2f}s" dur="0.30s" fill="freeze"/></rect></clipPath>'
                 f'<g clip-path="url(#l{n})">{svg}</g>')
    n += 1
    y += LH

y += 6
p.append(f'<text x="{PAD}" y="{y}" font-size="{FS}" fill="{LIME}">$</text>')
p.append(f'<rect x="{PAD+FS*0.62*2}" y="{y-FS+3}" width="11" height="{FS}" fill="{LIME}">'
         + ('' if STATIC else '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.51;1" dur="1s" repeatCount="indefinite"/>')
         + '</rect>')
p.append("</svg>")
open(OUT, "w").write("".join(p))
print("wrote", os.path.basename(OUT), "last line y =", y)
