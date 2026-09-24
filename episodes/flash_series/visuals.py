"""Portrait-safe visual components for the FlashAttention series."""
import os

from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = "#0B1220"

INK = "#EDF2FA"
MUTED = "#93A5BF"
Q_BLUE = "#66D9EF"
K_PINK = "#EF9DCA"
V_GREEN = "#8CE3BB"
S_GOLD = "#F6CA78"
P_VIOLET = "#B8A7FF"
O_CORAL = "#FF8FA3"
HBM_BLUE = "#4479B8"
NODE_FILL = "#12233A"
FONT = "Malgun Gothic"


def txt(text, size=28, color=INK, width=7.7):
    mob = Text(str(text), font=FONT, font_size=size, color=color, line_spacing=1.2)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


class MatrixGrid(VGroup):
    """Compact matrix whose entries can be addressed and highlighted."""

    def __init__(self, rows, cols, label, color, cell=.42, values=None, **kwargs):
        super().__init__(**kwargs)
        self.rows, self.cols = rows, cols
        self.cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                square = Square(
                    side_length=cell, stroke_color=color, stroke_width=1.1,
                    fill_color=color, fill_opacity=.07,
                )
                if values is None:
                    content = txt("·", 15, color, cell * .65)
                else:
                    content = txt(values[r][c], 13, color, cell * .72)
                entry = VGroup(square, content)
                entry.move_to([(c - (cols - 1) / 2) * cell,
                               ((rows - 1) / 2 - r) * cell, 0])
                self.cells.add(entry)
        self.name = txt(label, 22, color).next_to(self.cells, UP, buff=.16)
        self.add(self.cells, self.name)

    def row(self, index):
        start = index * self.cols
        return VGroup(*self.cells[start:start + self.cols])


class DataCard(VGroup):
    def __init__(self, name, subtitle, color, width=2.0, height=1.2, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(
            width=width, height=height, corner_radius=.16,
            stroke_color=color, stroke_width=1.8,
            fill_color=color, fill_opacity=.07,
        )
        title = txt(name, 27, color, width - .2).move_to(box.get_center() + UP * .2)
        sub = txt(subtitle, 17, MUTED, width - .2).move_to(box.get_center() + DOWN * .25)
        self.add(box, title, sub)


class MemoryBox(VGroup):
    def __init__(self, width=6.8, height=1.7, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(
            width=width, height=height, corner_radius=.16,
            stroke_color=HBM_BLUE, stroke_width=2,
            fill_color=HBM_BLUE, fill_opacity=.09,
        )
        label = txt("GPU HBM", 22, HBM_BLUE).move_to(
            box.get_corner(UL) + RIGHT * .85 + DOWN * .3
        )
        hint = txt("큰 용량  ·  연산 사이의 중간값", 17, MUTED).move_to(
            box.get_corner(UR) + LEFT * 2.15 + DOWN * .3
        )
        self.add(box, label, hint)
