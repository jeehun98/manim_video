"""Small scene-independent Manim objects."""

import numpy as np
from manim import Line, RoundedRectangle, UP, VGroup

from .theme import INK, PRUNE, WEIGHT, ZERO
from .typography import text


class Pill(VGroup):
    def __init__(self, label, color, width=2.5, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.18,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=color,
            fill_opacity=0.09,
        )
        self.label = text(label, 22, color, width - 0.22)
        self.add(self.box, self.label)


def pill(label, color, width=2.5):
    """Function-style compatibility constructor for :class:`Pill`."""

    return Pill(label, color, width)


class WeightMatrix(VGroup):
    """A compact matrix whose zero and non-zero entries are addressable."""

    def __init__(self, values, cell_size=0.92, **kwargs):
        super().__init__(**kwargs)
        self.values = values
        rows, cols = len(values), len(values[0])
        self.cells = VGroup()
        self.entries = VGroup()
        self.zeros = VGroup()
        self.nonzeros = VGroup()

        for row_index, row in enumerate(values):
            for column_index, value in enumerate(row):
                is_zero = abs(value) < 1e-9
                center = np.array(
                    [
                        (column_index - (cols - 1) / 2) * cell_size,
                        ((rows - 1) / 2 - row_index) * cell_size,
                        0,
                    ]
                )
                color = ZERO if is_zero else WEIGHT
                cell = RoundedRectangle(
                    width=cell_size * 0.86,
                    height=cell_size * 0.78,
                    corner_radius=0.09,
                    stroke_color=color,
                    stroke_width=1.25,
                    fill_color=color,
                    fill_opacity=0.08 if is_zero else 0.12,
                ).move_to(center)
                label = text(
                    "0" if is_zero else f"{value:g}",
                    22,
                    ZERO if is_zero else INK,
                    cell_size * 0.72,
                ).move_to(center)
                item = VGroup(cell, label)
                self.cells.add(cell)
                self.entries.add(item)
                (self.zeros if is_zero else self.nonzeros).add(item)

        self.add(self.entries)


def weight_connection(start, end, value):
    strength = min(1.0, 0.22 + abs(value))
    color = PRUNE if abs(value) < 0.05 else WEIGHT
    line = Line(
        start,
        end,
        color=color,
        stroke_width=1.5 + 4.0 * abs(value),
        stroke_opacity=strength,
    )
    label = text(f"{value:g}", 21, color).move_to(
        line.point_from_proportion(0.46) + UP * 0.19
    )
    return VGroup(line, label)

