"""Reusable portrait visuals for EML nodes and expression trees."""
import os

import numpy as np
from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = "#0B1220"

INK = "#EDF2FA"
MUTED = "#93A5BF"
BLUE = "#66D9EF"
GOLD = "#F6CA78"
PINK = "#EF9DCA"
GREEN = "#8CE3BB"
NODE_FILL = "#12233A"
FONT = "Malgun Gothic"


def txt(text, size=28, color=INK, width=7.7):
    """Series text helper with a safe portrait-frame width."""
    mob = Text(str(text), font=FONT, font_size=size, color=color, line_spacing=1.2)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


class OperatorChip(VGroup):
    """A calculator operator tile used before and after reduction to EML."""

    def __init__(self, symbol, color=BLUE, width=1.35, height=.88, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=width, height=height, corner_radius=.14,
            stroke_color=color, stroke_width=1.7,
            fill_color=color, fill_opacity=.08,
        )
        self.symbol = txt(symbol, 29, color, width - .16)
        self.add(self.box, self.symbol)


class EMLNode(VGroup):
    """A two-input EML primitive with stable connection anchors.

    Children connect to ``left_anchor`` and ``right_anchor`` and the result
    leaves through ``output_anchor``.  The same object can therefore be used
    alone, in a flow diagram, or recursively inside an expression tree.
    """

    def __init__(self, width=2.35, height=1.12, compact=False, **kwargs):
        super().__init__(**kwargs)
        color = GOLD
        self.box = RoundedRectangle(
            width=width, height=height, corner_radius=.18,
            stroke_color=color, stroke_width=2.4,
            fill_color=NODE_FILL, fill_opacity=.96,
        )
        self.name = txt("EML", 29 if not compact else 21, color, width - .35)
        self.left_port = Dot(radius=.055, color=BLUE)
        self.right_port = Dot(radius=.055, color=PINK)
        self.out_port = Dot(radius=.055, color=GREEN)
        self.add(self.box, self.name, self.left_port, self.right_port, self.out_port)
        self._place_ports(self)

    def _place_ports(self, _):
        bottom = self.box.get_bottom()
        self.left_port.move_to(bottom + LEFT * self.box.width * .24)
        self.right_port.move_to(bottom + RIGHT * self.box.width * .24)
        self.out_port.move_to(self.box.get_top())

    def left_anchor(self):
        return self.left_port.get_center()

    def right_anchor(self):
        return self.right_port.get_center()

    def output_anchor(self):
        return self.out_port.get_center()


class ExpressionTree(VGroup):
    """Render nested ``("EML", left, right)`` tuples as a reusable tree."""

    def __init__(self, expression, width=6.8, level_gap=1.25, **kwargs):
        super().__init__(**kwargs)
        self.expression = expression
        leaves = self._leaf_count(expression)
        x_positions = np.linspace(-width / 2, width / 2, max(leaves, 2))
        self.nodes = VGroup()
        self.leaves = VGroup()
        self.edges = VGroup()
        self._cursor = 0
        self.root, _, depth = self._build_tree(expression, x_positions, 0, level_gap)
        self.add(self.edges, self.nodes, self.leaves)
        self.tree_depth = depth

    @classmethod
    def _leaf_count(cls, expr):
        if not isinstance(expr, tuple):
            return 1
        return cls._leaf_count(expr[1]) + cls._leaf_count(expr[2])

    def _build_tree(self, expr, xs, depth, gap):
        y = -depth * gap
        if not isinstance(expr, tuple):
            x = xs[self._cursor]
            self._cursor += 1
            leaf = VGroup(
                Circle(radius=.27, stroke_color=BLUE if str(expr) != "1" else GREEN,
                       fill_color=NODE_FILL, fill_opacity=.95, stroke_width=1.6),
                txt(expr, 21, BLUE if str(expr) != "1" else GREEN, .42),
            ).move_to([x, y, 0])
            self.leaves.add(leaf)
            return leaf, x, depth

        left, lx, ld = self._build_tree(expr[1], xs, depth + 1, gap)
        right, rx, rd = self._build_tree(expr[2], xs, depth + 1, gap)
        x = (lx + rx) / 2
        node = EMLNode(width=1.25, height=.62, compact=True).move_to([x, y, 0])
        self.nodes.add(node)
        self.edges.add(
            Line(left.get_top(), node.left_anchor(), color=BLUE, stroke_width=2),
            Line(right.get_top(), node.right_anchor(), color=PINK, stroke_width=2),
        )
        return node, x, max(ld, rd)


def input_arrow(start, end, color):
    return Arrow(start, end, buff=.08, color=color, stroke_width=3,
                 max_tip_length_to_length_ratio=.14)
