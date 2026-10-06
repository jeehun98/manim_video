"""Shared palette and opt-in Manim render configuration."""

import os

from manim import config

BG = "#091119"
INK = "#EDF3F7"
MUTED = "#94A7B7"
WEIGHT = "#68D9F0"
PRUNE = "#FF8C9D"
SPARSE = "#AF9CF5"
ACCENT = "#F3CF75"
GOOD = "#61E4CF"
ZERO = "#31404D"
FONT = "Malgun Gothic"


def configure_vertical(width=None, height=None, frame_rate=30):
    """Apply the repository's standard 9:16 render settings explicitly."""

    config.pixel_width = int(width or os.environ.get("VIDEO_WIDTH", "1080"))
    config.pixel_height = int(height or os.environ.get("VIDEO_HEIGHT", "1920"))
    config.frame_width = 9
    config.frame_height = 16
    config.frame_rate = frame_rate
    config.background_color = BG

