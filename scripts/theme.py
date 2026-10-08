"""Shared look for every generated card. Change colours here, re-run, done."""
import os

USER = os.environ.get("GH_PROFILE_USER", "SubhamPro11")
HANDLE = "cryo"                      # shown in the fake terminal prompts

BG      = "#0a0e14"                  # page navy
TILE    = "#0f151d"                  # raised panel
FRAME   = "#1f2a37"                  # hairlines
MUTED   = "#7d8a9c"
INK     = "#d6dde8"
LIME    = "#39FF14"                  # the one accent

# GitHub's own 0-4 contribution levels, mapped onto navy -> lime
RAMP = ["#111821", "#143d1a", "#1f7a21", "#2fc21a", "#39FF14"]

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# set STATIC=1 to render the finished frame (for previews); the real run animates
STATIC = bool(os.environ.get("STATIC"))
