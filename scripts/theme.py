"""Shared look for every generated card. Change colours here, re-run, done.

Palette: sage on charcoal. One accent, tinted neutrals, no pure black/white.
"""
import os

USER = os.environ.get("GH_PROFILE_USER", "SubhamPro11")
HANDLE = "cryo"                      # shown in the fake terminal prompts

BG     = "#121413"                   # page charcoal
TILE   = "#181b19"                   # raised panel
FRAME  = "#2a2f2c"                   # hairlines
MUTED  = "#8a9490"
INK    = "#d8ddd3"
ACCENT = "#9bbf7a"                   # sage, the only accent

# empty -> most active: same hue, getting brighter
RAMP = ["#1b1f1c", "#2c3b2a", "#44603b", "#6f9654", "#9bbf7a"]

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# set STATIC=1 to render the finished frame (for previews); the real run animates
STATIC = bool(os.environ.get("STATIC"))
