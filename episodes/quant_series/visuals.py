"""Reusable number-line visuals for the quantization series."""
from manim import *

BG = "#091119"
INK = "#EDF3F7"
MUTED = "#94A7B7"
VALUE = "#68D9F0"
GRID = "#AF9CF5"
SNAP = "#F3CF75"
ERROR = "#FF8C9D"
GOOD = "#61E4CF"
FONT = "Malgun Gothic"

config.pixel_width = int(__import__("os").environ.get("VIDEO_WIDTH", "1080"))
config.pixel_height = int(__import__("os").environ.get("VIDEO_HEIGHT", "1920"))
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


class QuantizationLine(VGroup):
    """A stable 0..1 number line with optional representable grid points."""

    def __init__(self, width=7.0, grid_values=(), show_labels=True, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2,
                         color=MUTED, stroke_width=3)
        self.add(self.axis)
        self.grid = VGroup()
        self.labels = VGroup()
        for value in grid_values:
            x = self.point(value)[0]
            tick = Line([x, -.22, 0], [x, .22, 0], color=GRID, stroke_width=5)
            marker = Dot([x, 0, 0], radius=.075, color=GRID)
            self.grid.add(VGroup(tick, marker))
            if show_labels:
                self.labels.add(txt(f"{value:.2f}" if value not in (0, 1) else f"{value:.1f}",
                                    20, GRID).move_to([x, -.55, 0]))
        self.add(self.grid, self.labels)

    def point(self, value, y=0):
        return np.array([-self.width / 2 + self.width * value, y, 0])


class ValueDot(VGroup):
    """A labeled value whose center is the data point used for snapping."""

    def __init__(self, value, line, color=VALUE, label_y=.55, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.dot = Dot(line.point(value), radius=.105, color=color)
        self.label = txt(f"{value:.2f}", 21, color).move_to(
            line.point(value) + UP * label_y
        )
        self.stem = Line(self.dot.get_center(), self.label.get_bottom(),
                         color=color, stroke_width=1.4, stroke_opacity=.45)
        self.add(self.stem, self.dot, self.label)


def value_dots(values, line, alternating=False):
    dots = VGroup()
    label_lanes = (.72, -.72, 1.25, -1.25, .72)
    for i, value in enumerate(values):
        height = .58 if not alternating else label_lanes[i % len(label_lanes)]
        dot = ValueDot(value, line, label_y=height)
        if height < 0:
            dot.label.move_to(line.point(value) + DOWN * .62)
            dot.stem.put_start_and_end_on(dot.dot.get_center(), dot.label.get_top())
        dots.add(dot)
    return dots


def pill(text, color, width=2.35):
    box = RoundedRectangle(width=width, height=.72, corner_radius=.18,
                           stroke_color=color, stroke_width=1.8,
                           fill_color=color, fill_opacity=.09)
    return VGroup(box, txt(text, 22, color, width - .2))


class MappedAxes(VGroup):
    """Aligned real/integer axes shared by the scale and zero-point episodes."""

    def __init__(self, real_range=(0.0, 1.0), int_range=(0, 255), width=6.7,
                 real_color=VALUE, int_color=GRID, dense_ticks=True, **kwargs):
        super().__init__(**kwargs)
        self.real_range = real_range
        self.int_range = int_range
        self.real_axis = Line(LEFT * width / 2, RIGHT * width / 2,
                              color=real_color, stroke_width=3).shift(UP)
        self.int_axis = Line(LEFT * width / 2, RIGHT * width / 2,
                             color=int_color, stroke_width=3).shift(DOWN)
        tick_count = int_range[1] - int_range[0] + 1 if dense_ticks else 17
        self.int_ticks = VGroup(*[
            Line(UP * (.12 if i in (0, tick_count - 1) else .065),
                 DOWN * (.12 if i in (0, tick_count - 1) else .065),
                 color=int_color, stroke_width=.8 if tick_count > 32 else 1.7,
                 stroke_opacity=.7).move_to(
                     self.int_axis.point_from_proportion(i / (tick_count - 1)))
            for i in range(tick_count)
        ])
        self.end_labels = VGroup(
            txt(f"{real_range[0]:g}", 19, real_color).next_to(self.real_axis, LEFT, buff=.1),
            txt(f"{real_range[1]:g}", 19, real_color).next_to(self.real_axis, RIGHT, buff=.1),
            txt(str(int_range[0]), 19, int_color).next_to(self.int_axis, LEFT, buff=.1),
            txt(str(int_range[1]), 19, int_color).next_to(self.int_axis, RIGHT, buff=.1),
        )
        self.connectors = VGroup(
            DashedLine(self.real_axis.get_start(), self.int_axis.get_start(),
                       color=MUTED, stroke_width=1.5, dash_length=.08),
            DashedLine(self.real_axis.get_end(), self.int_axis.get_end(),
                       color=MUTED, stroke_width=1.5, dash_length=.08),
        )
        self.axis_names = VGroup(
            txt("real x", 20, real_color).next_to(self.real_axis, UP, buff=.22),
            txt("integer q", 20, int_color).next_to(self.int_axis, DOWN, buff=.22),
        )
        self.add(self.real_axis, self.int_axis, self.int_ticks, self.end_labels,
                 self.connectors, self.axis_names)

    def real_point(self, value):
        lo, hi = self.real_range
        return self.real_axis.point_from_proportion((value - lo) / (hi - lo))

    def int_point(self, value):
        lo, hi = self.int_range
        return self.int_axis.point_from_proportion((value - lo) / (hi - lo))
