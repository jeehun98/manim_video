"""Reusable visuals for the pruning and sparsity series."""
import os

from manim import *

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

config.pixel_width = int(os.environ.get("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.environ.get("VIDEO_HEIGHT", "1920"))
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = BG


def txt(text, size=28, color=INK, max_width=7.7, weight=NORMAL):
    obj = Text(str(text), font=FONT, font_size=size, color=color,
               weight=weight, line_spacing=1.18)
    if obj.width > max_width:
        obj.scale_to_fit_width(max_width)
    return obj


def pill(text, color, width=2.5):
    box = RoundedRectangle(width=width, height=.72, corner_radius=.18,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=color, fill_opacity=.09)
    return VGroup(box, txt(text, 22, color, width - .22))


class WeightMatrix(VGroup):
    """A compact matrix whose zero and non-zero entries can be addressed."""

    def __init__(self, values, cell_size=.92, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        rows, cols = len(values), len(values[0])
        self.cells = VGroup()
        self.entries = VGroup()
        self.zeros = VGroup()
        self.nonzeros = VGroup()
        for r, row in enumerate(values):
            for c, value in enumerate(row):
                is_zero = abs(value) < 1e-9
                center = np.array([
                    (c - (cols - 1) / 2) * cell_size,
                    ((rows - 1) / 2 - r) * cell_size,
                    0,
                ])
                cell = RoundedRectangle(
                    width=cell_size * .86, height=cell_size * .78,
                    corner_radius=.09, stroke_color=ZERO if is_zero else WEIGHT,
                    stroke_width=1.25, fill_color=ZERO if is_zero else WEIGHT,
                    fill_opacity=.08 if is_zero else .12,
                ).move_to(center)
                label = txt(
                    "0" if is_zero else f"{value:g}", 22,
                    ZERO if is_zero else INK, cell_size * .72,
                ).move_to(center)
                item = VGroup(cell, label)
                self.cells.add(cell)
                self.entries.add(item)
                (self.zeros if is_zero else self.nonzeros).add(item)
        self.add(self.entries)


def weight_connection(start, end, value):
    strength = min(1.0, .22 + abs(value))
    color = PRUNE if abs(value) < .05 else WEIGHT
    line = Line(start, end, color=color, stroke_width=1.5 + 4.0 * abs(value),
                stroke_opacity=strength)
    label = txt(f"{value:g}", 21, color).move_to(
        line.point_from_proportion(.46) + UP * .19
    )
    return VGroup(line, label)
