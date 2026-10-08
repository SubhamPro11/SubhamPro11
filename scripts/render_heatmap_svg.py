#!/usr/bin/env python3
"""contributions.json -> contrib-heatmap.svg (boxes slide in once, then hold)."""
import datetime, json, os
from theme import *

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "..", "data", "contributions.json")))
OUT = os.path.join(HERE, "..", "contrib-heatmap.svg")

CELL, GAP = 12, 3
STEP = CELL + GAP
PAD, LEFT, TOPLBL, BAR = 22, 30, 20, 34

days = data["days"]
first = datetime.date.fromisoformat(days[0]["date"])
col, grid = [None] * ((first.weekday() + 1) % 7), []
for d in days:
    wd = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7
    while len(col) < wd:
        col.append(None)
    col.append(d)
    if len(col) == 7:
        grid.append(col); col = []
if col:
    grid.append(col + [None] * (7 - len(col)))

art_w, art_h = len(grid) * STEP, 7 * STEP
W = PAD * 2 + LEFT + art_w
foot = 92
H = BAR + TOPLBL + art_h + foot + PAD
gx0, gy0 = PAD + LEFT, BAR + TOPLBL

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
if not STATIC:
    p.append('<style>.c{opacity:0;animation:in .4s cubic-bezier(.2,.8,.2,1) both}'
             '@keyframes in{0%{opacity:0;transform:translateY(-6px)}100%{opacity:1;transform:none}}'
             '@media (prefers-reduced-motion:reduce){.c{opacity:1!important;animation:none!important}}</style>')
p.append(f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>')
p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{FRAME}"/>')
p.append(f'<line x1="0" y1="{BAR}" x2="{W}" y2="{BAR}" stroke="{FRAME}"/>')
p.append(f'<text x="{PAD}" y="21" font-size="13" fill="{MUTED}">{HANDLE}@github:~$ '
         f'<tspan fill="{ACCENT}">./contributions.sh</tspan></text>')

seen = set()
for ci, c in enumerate(grid):
    first_cell = next((x for x in c if x), None)
    if first_cell:
        dt = datetime.date.fromisoformat(first_cell["date"])
        if (dt.year, dt.month) not in seen and dt.day <= 7:
            seen.add((dt.year, dt.month))
            p.append(f'<text x="{gx0 + ci*STEP}" y="{BAR+14}" font-size="10" fill="{MUTED}">{dt.strftime("%b")}</text>')
for r, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
    p.append(f'<text x="{PAD}" y="{gy0 + r*STEP + 10}" font-size="9" fill="{MUTED}">{name}</text>')

for ci, c in enumerate(grid):
    for ri, d in enumerate(c):
        if not d:
            continue
        n = d["count"]
        delay = ci * 0.018 + ri * 0.045
        cls = "" if STATIC else f' class="c" style="animation-delay:{delay:.3f}s"'
        p.append(f'<rect{cls} x="{gx0+ci*STEP}" y="{gy0+ri*STEP}" width="{CELL}" height="{CELL}" rx="2" '
                 f'fill="{RAMP[min(d["level"],4)]}"><title>{d["date"]}: {n} contribution{"" if n==1 else "s"}</title></rect>')

# legend, bottom right of the grid
ly = gy0 + art_h + 8
lx = W - PAD - (len(RAMP) * STEP + 70)
p.append(f'<text x="{lx}" y="{ly+10}" font-size="10" fill="{MUTED}">less</text>')
for i, colr in enumerate(RAMP):
    p.append(f'<rect x="{lx+34+i*STEP}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{colr}"/>')
p.append(f'<text x="{lx+34+len(RAMP)*STEP+4}" y="{ly+10}" font-size="10" fill="{MUTED}">more</text>')

sy = ly + 28
p.append(f'<line x1="0" y1="{sy}" x2="{W}" y2="{sy}" stroke="{FRAME}"/>')
cs, ls, best = data["current_streak"]["length"], data["longest_streak"]["length"], data["best_day"]
y1, y2 = sy + 26, sy + 52
p.append(f'<text x="{PAD}" y="{y1}" font-size="13" fill="{MUTED}"><tspan fill="{ACCENT}" font-weight="700">'
         f'{data["total_contributions"]:,}</tspan> contributions in the last year</text>')
p.append(f'<text x="{W-PAD}" y="{y1}" font-size="12" fill="{MUTED}" text-anchor="end">'
         f'{data["range"]["start"]} to {data["range"]["end"]}</text>')
p.append(f'<text x="{PAD}" y="{y2}" font-size="13" fill="{MUTED}">current streak <tspan fill="{INK}" font-weight="700">{cs}d</tspan>'
         f' &#183; longest <tspan fill="{INK}" font-weight="700">{ls}d</tspan>'
         f' &#183; best day <tspan fill="{INK}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')
p.append("</svg>")
open(OUT, "w").write("".join(p))
print("wrote", os.path.basename(OUT), W, "x", H)
