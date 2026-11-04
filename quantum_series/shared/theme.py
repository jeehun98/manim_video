"""Quantum documentary palette and responsive layout; no animation decisions here."""
import os
from dataclasses import dataclass
import numpy as np
from manim import config, Text

BG = '#0B1020'
INK = '#EEF2FA'
MUTED = '#8D9BB6'
HEAT = '#FF9F43'
DATA = '#32C5FF'
OLD = '#A494C9'
GOLD = '#FFD166'
FONT = 'Malgun Gothic'

def p(x, y):
    return np.array([x, y, 0.])

def text(s, x=0, y=0, size=30, color=INK, width=None):
    obj = Text(s, font=FONT, font_size=size, color=color, line_spacing=.8)
    if width and obj.width > width:
        obj.scale_to_fit_width(width)
    return obj.move_to(p(x, y))

@dataclass(frozen=True)
class Layout:
    portrait: bool

    @property
    def heading_y(self): return 5.3 if self.portrait else 2.65
    @property
    def brand_y(self): return 7.12 if self.portrait else 3.85
    @property
    def caption_y(self): return -6.1 if self.portrait else -3.57
    @property
    def graph_center(self): return p(0, .15) if self.portrait else p(3.25, .05)
    @property
    def graph_width(self): return 6.8 if self.portrait else 7.65
    @property
    def context(self): return p(0, 3.3) if self.portrait else p(-4.6, .45)
    @property
    def body_width(self): return 7.6 if self.portrait else 14
    @property
    def column_x(self): return [-2.7, -.9, .9, 2.7] if self.portrait else [-4.2, -1.4, 1.4, 4.2]
    @property
    def comparison_x(self): return (-1.95, 1.95) if self.portrait else (-3.7, 3.7)

def configure():
    portrait = os.environ.get('QUANTUM_LAYOUT', 'shorts') == 'shorts'
    preview = os.environ.get('QUANTUM_PREVIEW') == '1'
    config.frame_width, config.frame_height = (9, 16) if portrait else (16, 9)
    config.pixel_width, config.pixel_height = ((360, 640) if portrait else (640, 360)) if preview else ((1080, 1920) if portrait else (1920, 1080))
    config.frame_rate = 30
    config.background_color = BG
    return Layout(portrait)
