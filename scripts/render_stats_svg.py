#!/usr/bin/env python3
"""contributions.json -> stats.svg (tiles slide in, numbers count up, month bars grow)."""
import datetime, json, os
from theme import *

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "..", "data", "contributions.json")))
OUT = os.path.join(HERE, "..", "stats.svg")

W, H, PAD, BAR = 840, 880, 20, 30
COLS, ROWS, GAP, TILE_H = 2, 3, 16, 150
TILE_W = (W - PAD * 2 - GAP) / COLS
TILES_TOP = BAR + PAD
CHART_TOP = TILES_TOP + ROWS * TILE_H + (ROWS - 1) * GAP + GAP
FRAMES, COUNT_DUR, STAGGER = 14, 1.1, 0.14


def short(s):
    return datetime.date.fromisoformat(s).strftime("%b %d").replace(" 0", " ")


def span(s):
    return f'{short(s["start"])} to {short(s["end"])}' if s["length"] else "none right now"


cur, lng, best = data["current_streak"], data["longest_streak"], data["best_day"]
n_days = len(data["days"])
tiles = [
    ("current streak", cur["length"], " days", span(cur), ACCENT if cur["length"] else INK),
    ("longest streak", lng["length"], " days", span(lng), INK),
    ("contributions", data["total_contributions"], "", "in the last year", INK),
    ("active days", data["active_days"], f" / {n_days}", f'{data["active_days"]/n_days:.0%} of the year', INK),
    ("best day", best["count"], "", short(best["date"]), INK),
    ("avg / active day", data["avg_per_active_day"], "", "contributions", INK),
]

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">']
if not STATIC:
    p.append('<style>.t{opacity:0;animation:in .45s ease-out both}'
             '@keyframes in{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:none}}'
             '.b{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:g .6s ease-out both}'
             '@keyframes g{to{transform:scaleY(1)}}'
             '@media (prefers-reduced-motion:reduce){.t,.b{opacity:1!important;transform:none!important;animation:none!important}}</style>')
p.append(f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>')
p.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{FRAME}"/>')
p.append(f'<line x1="0" y1="{BAR}" x2="{W}" y2="{BAR}" stroke="{FRAME}"/>')
p.append(f'<text x="{PAD}" y="20" font-size="13" fill="{MUTED}">{HANDLE}@github:~$ <tspan fill="{ACCENT}">./stats.sh</tspan></text>')


def grp(delay):
    return "<g>" if STATIC else f'<g class="t" style="animation-delay:{delay:.2f}s">'


def num(v, like):
    return f"{v:,.1f}" if isinstance(like, float) else f"{int(round(v)):,}"


for i, (label, value, suffix, caption, accent) in enumerate(tiles):
    x = PAD + (i % COLS) * (TILE_W + GAP)
    y = TILES_TOP + (i // COLS) * (TILE_H + GAP)
    start = i * STAGGER
    p.append(grp(start))
    p.append(f'<rect x="{x:.1f}" y="{y}" width="{TILE_W:.1f}" height="{TILE_H}" rx="4" fill="{TILE}" stroke="{FRAME}"/>')
    p.append(f'<text x="{x+24:.1f}" y="{y+40}" fill="{MUTED}" font-size="22">$ {label}</text>')
    if STATIC:
        p.append(f'<text x="{x+24:.1f}" y="{y+100}" font-size="54" font-weight="700" fill="{accent}">{num(value,value)}'
                 f'<tspan font-size="24" font-weight="400" fill="{MUTED}">{suffix}</tspan></text>')
    else:
        t0 = start + 0.27
        for k in range(1, FRAMES + 1):   # pre-rendered frames: GitHub runs SMIL/CSS in <img> SVGs, never JS
            v = value * (1 - (1 - k / FRAMES) ** 3)
            on = t0 + COUNT_DUR * (k - 1) / FRAMES
            off = t0 + COUNT_DUR * k / FRAMES
            anim = f'<set attributeName="opacity" to="1" begin="{on:.3f}s"/>'
            if k < FRAMES:
                anim += f'<set attributeName="opacity" to="0" begin="{off:.3f}s"/>'
            p.append(f'<text x="{x+24:.1f}" y="{y+100}" opacity="0" font-size="54" font-weight="700" fill="{accent}">'
                     f'{num(v,value)}<tspan font-size="24" font-weight="400" fill="{MUTED}">{suffix}</tspan>{anim}</text>')
    p.append(f'<text x="{x+24:.1f}" y="{y+132}" fill="{MUTED}" font-size="20">{caption}</text></g>')

monthly = data["monthly"]
cw, ch = W - PAD * 2, H - PAD - CHART_TOP
bar_start = STAGGER * 6 + 0.4
p.append(grp(bar_start - 0.3))
p.append(f'<rect x="{PAD}" y="{CHART_TOP}" width="{cw}" height="{ch}" rx="4" fill="{TILE}" stroke="{FRAME}"/>')
p.append(f'<text x="{PAD+24}" y="{CHART_TOP+40}" fill="{MUTED}" font-size="22">$ contributions / month</text></g>')
top, bot = CHART_TOP + 78, CHART_TOP + ch - 44
l, r = PAD + 24, PAD + cw - 24
slot = (r - l) / len(monthly)
bw = slot * 0.6
peak = max(m["total"] for m in monthly) or 1
for i, m in enumerate(monthly):
    h = max(2, (bot - top) * m["total"] / peak)
    bx = l + i * slot + (slot - bw) / 2
    colr = ACCENT if m["total"] == peak else RAMP[3]
    cls = "" if STATIC else f' class="b" style="animation-delay:{bar_start+i*0.06:.2f}s"'
    p.append(f'<rect{cls} x="{bx:.1f}" y="{bot-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" fill="{colr}"/>')
    p.append(f'<text x="{bx+bw/2:.1f}" y="{bot+28}" fill="{MUTED}" font-size="15" text-anchor="middle">'
             f'{datetime.date.fromisoformat(m["month"]+"-01").strftime("%b")}</text>')
    if m["total"]:
        p.append(f'<text x="{bx+bw/2:.1f}" y="{bot-h-8:.1f}" fill="{INK}" font-size="15" text-anchor="middle">{m["total"]}</text>')
p.append("</svg>")
open(OUT, "w").write("".join(p))
print("wrote", os.path.basename(OUT))
