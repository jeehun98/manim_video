"""Activation Function Series — ReLU. 38 seconds, portrait, no LaTeX needed.

Render: python scripts/render.py 01
Change VALUES, COLORS, activation(), and section budgets to adapt the lesson.
"""
from manim import *
import os

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = "#091119"

INK = "#EDF3F7"
MUTED = "#94A7B7"
ACCENT = "#61E4CF"
COLORS = ["#FF8C9D", "#68D9F0", "#D3A5FF", "#F3CF75", "#8DADFF"]
VALUES = [-2, 1, -0.5, 3, -4]
SECTION_SECONDS = [4, 10, 8, 9, 3, 4]


def activation(x):
    return max(0, x)


def text(s, size=30, color=INK):
    if "₁" in s or "₂" in s:
        parts = VGroup()
        for char in s:
            part = Text({"₁": "1", "₂": "2"}.get(char, char),
                        font="Arial", font_size=size * (0.62 if char in "₁₂" else 1), color=color)
            parts.add(part)
        parts.arrange(RIGHT, buff=0.018)
        for char, part in zip(s, parts):
            if char in "₁₂":
                part.shift(DOWN * size / 240)
        return parts
    return Text(s, font="Arial", font_size=size, color=color)


def number(x):
    return f"{x:g}".replace("-", "−")


def column(values, position):
    entries = VGroup(*[text(number(v), 35, c) for v, c in zip(values, COLORS)])
    entries.arrange(DOWN, buff=0.36).move_to(position)
    h = entries.height / 2 + 0.18
    brackets = VGroup(*[VMobject().set_points_as_corners([
        [s * 0.57, h, 0], [s * 0.76, h, 0],
        [s * 0.76, -h, 0], [s * 0.57, -h, 0]
    ]).set_stroke(MUTED, 2) for s in [-1, 1]]).shift(position)
    return VGroup(brackets, entries), entries


class ReLUIntroduction(Scene):
    def finish_section(self, start, budget):
        remaining = budget - (self.time - start)
        if remaining < -0.02:
            raise ValueError(f"Section exceeds budget by {-remaining:.2f}s")
        if remaining > 0.02:
            self.wait(remaining)

    def construct(self):
        # 1 / 0–4 s: name and definition, then retain the formula as an anchor.
        start = self.time
        series = text("ACTIVATION FUNCTION SERIES", 20, MUTED).move_to(UP * 6.3)
        title = text("ReLU", 82).move_to(UP * 1.4)
        self.play(FadeIn(series), FadeIn(title, shift=UP * 0.15), run_time=0.6)
        self.wait(0.4)
        full_name = text("Rectified Linear Unit", 42).move_to(title)
        self.play(ReplacementTransform(title, full_name), run_time=0.9)
        formula = text("f(x) = max(0, x)", 39, ACCENT).move_to(DOWN * 0.1)
        self.play(Write(formula), run_time=0.8)
        self.finish_section(start, SECTION_SECONDS[0])

        # 2 / 4–14 s: each input visibly travels to and becomes its output.
        start = self.time
        heading = text("ReLU", 52).move_to(UP * 5.2)
        self.play(ReplacementTransform(full_name, heading),
                  formula.animate.scale(0.8).move_to(UP * 4.25), run_time=0.7)
        vin, ins = column(VALUES, LEFT * 2.1 + UP * 0.35)
        vout, outs = column([activation(v) for v in VALUES], RIGHT * 2.1 + UP * 0.35)
        input_name = text("x", 32).next_to(vin, UP, buff=0.35)
        output_name = text("ReLU(x)", 32).next_to(vout, UP, buff=0.35)
        arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, color=ACCENT).shift(UP * 0.35)
        each = text("One element at a time", 28, MUTED).move_to(DOWN * 3)
        self.play(FadeIn(vin), FadeIn(input_name), Create(arrow),
                  FadeIn(vout[0]), FadeIn(output_name), FadeIn(each), run_time=0.8)
        for source, target in zip(ins, outs):
            moving = source.copy()
            self.add(moving)
            self.play(Indicate(source, scale_factor=1.14),
                      ReplacementTransform(moving, target, path_arc=-0.2), run_time=0.8)
            self.wait(0.15)
        rule = VGroup(text("Negative → zero", 29),
                      text("Positive → unchanged", 29)).arrange(DOWN, buff=0.3).move_to(DOWN * 3.7)
        self.play(ReplacementTransform(each, rule), run_time=0.6)
        # Regroup the individually revealed entries for the next continuous move.
        self.remove(*outs)
        self.add(vout)
        vectors = VGroup(vin, vout, input_name, output_name, arrow)
        self.finish_section(start, SECTION_SECONDS[1])

        # 3 / 14–22 s: the exact same colored pairs become graph samples.
        start = self.time
        self.play(vectors.animate.scale(0.46).move_to(LEFT * 2.65 + UP * 0.4),
                  FadeOut(rule), run_time=0.8)
        axes = Axes(x_range=[-4.5, 3.5, 1], y_range=[-0.5, 3.5, 1],
                    x_length=4.65, y_length=3.7,
                    axis_config={"color": MUTED, "stroke_width": 1.6,
                                 "include_ticks": True, "tip_width": 0.12,
                                 "tip_height": 0.12}).move_to(RIGHT * 1.35 + UP * 0.1)
        axis_labels = VGroup(text("x", 22).next_to(axes.x_axis, RIGHT, buff=0.08),
                            text("f(x)", 22).next_to(axes.y_axis, UP, buff=0.1),
                            text("0", 18, MUTED).next_to(axes.c2p(0, 0), DOWN + RIGHT, buff=0.1))
        self.play(Create(axes), FadeIn(axis_labels), run_time=0.7)
        dots = VGroup()
        for i, value in enumerate(VALUES):
            dot = Dot(axes.c2p(value, activation(value)), radius=0.075, color=COLORS[i]).set_z_index(3)
            pair = text(f"({number(value)}, {number(activation(value))})", 30, COLORS[i]).move_to(UP * 2.9 + RIGHT * 1.3)
            self.play(TransformFromCopy(VGroup(ins[i], outs[i]), pair), run_time=0.3)
            self.play(TransformFromCopy(pair, dot), Indicate(outs[i]), run_time=0.4)
            self.play(FadeOut(pair), run_time=0.1)
            dots.add(dot)
        curve = VGroup(Line(axes.c2p(-4.5, 0), axes.c2p(0, 0), color=ACCENT, stroke_width=4),
                       Line(axes.c2p(0, 0), axes.c2p(3.3, 3.3), color=ACCENT, stroke_width=4))
        graph_rule = VGroup(text("x < 0   →   f(x) = 0", 28),
                            text("x ≥ 0   →   f(x) = x", 28)).arrange(DOWN, buff=0.3).move_to(DOWN * 3.1)
        self.play(LaggedStart(*[Create(segment) for segment in curve], lag_ratio=0.25),
                  FadeIn(graph_rule), run_time=1.0)
        self.play(Indicate(curve[0], scale_factor=1), Indicate(curve[1], scale_factor=1), run_time=0.6)
        graph = VGroup(axes, axis_labels, curve, dots)
        self.finish_section(start, SECTION_SECONDS[2])

        # 4 / 22–31 s: input heights converge onto the zero-output branch.
        start = self.time
        graph.save_state()
        expanded = Axes(x_range=[-4.5, 3.5, 1], y_range=[-4.5, 3.5, 1],
                        x_length=6.6, y_length=6.2,
                        axis_config={"color": MUTED, "stroke_width": 1.6,
                                     "tip_width": 0.12, "tip_height": 0.12}).move_to(DOWN * 0.1)
        expanded_labels = VGroup(
            text("x", 22).next_to(expanded.x_axis, RIGHT, buff=0.08),
            text("f(x)", 22).next_to(expanded.y_axis, UP, buff=0.1),
            text("0", 18, MUTED).next_to(expanded.c2p(0, 0), DOWN + RIGHT, buff=0.1))
        expanded_curve = VGroup(
            Line(expanded.c2p(-4.5, 0), expanded.c2p(0, 0), color=ACCENT, stroke_width=4),
            Line(expanded.c2p(0, 0), expanded.c2p(3.3, 3.3), color=ACCENT, stroke_width=4))
        self.play(FadeOut(vectors), FadeOut(graph_rule),
                  Transform(axes, expanded), Transform(axis_labels, expanded_labels),
                  Transform(curve, expanded_curve),
                  *[d.animate.move_to(expanded.c2p(v, activation(v)))
                    for d, v in zip(dots, VALUES)], run_time=0.8)
        # Use the target coordinate system to avoid interpolation rounding.
        point = expanded.c2p
        regions = VGroup(
            VGroup(text("x < 0", 24, MUTED), text("OFF", 32, COLORS[0])).arrange(DOWN, buff=0.12).move_to(LEFT * 2 + UP * 2.7),
            VGroup(text("x ≥ 0", 24, MUTED), text("PASS", 32, ACCENT)).arrange(DOWN, buff=0.12).move_to(RIGHT * 1.9 + UP * 2.7))
        reference = DashedLine(point(-4.3, -4.3), point(3.3, 3.3),
                               color=MUTED, stroke_width=1.3).set_opacity(0.3)
        ref_label = text("y = x", 20, MUTED).move_to(LEFT * 2.45 + DOWN * 3.45)
        self.play(FadeIn(regions), Create(reference), FadeIn(ref_label), run_time=0.5)
        negative_values = [-4, -2, -1, -0.5]
        negative_colors = [COLORS[4], COLORS[0], COLORS[2], COLORS[2]]
        moving = VGroup(*[Dot(point(v, v), radius=0.085, color=c).set_z_index(4)
                         for v, c in zip(negative_values, negative_colors)])
        trails = VGroup(*[DashedLine(point(v, v), point(v, 0), color=c,
                                    stroke_width=1.4).set_opacity(0.45)
                         for v, c in zip(negative_values, negative_colors)])
        negative_maps = VGroup(*[text(f"{number(v)} → 0", 25, c)
                               for v, c in zip(negative_values, negative_colors)]).arrange(RIGHT, buff=0.38).move_to(DOWN * 4.2)
        caption = text("Negative activations are suppressed.", 27).move_to(DOWN * 5.4)
        self.play(FadeIn(moving), FadeIn(caption), run_time=0.4)
        for i, value in enumerate(negative_values):
            self.play(Create(trails[i]),
                      Transform(moving[i], Dot(point(value, 0), radius=0.085,
                                color=negative_colors[i]).set_z_index(4)),
                      FadeIn(negative_maps[i]), run_time=0.65)
        self.play(Indicate(curve[0], scale_factor=1, color=COLORS[0]), run_time=0.4)
        half = Dot(point(0.5, 0.5), radius=0.075, color=COLORS[1]).set_z_index(4)
        positive_dots = [half, dots[1], dots[3]]
        positive_maps = VGroup(*[text(f"{number(v)} → {number(v)}", 25, c)
                               for v, c in zip([0.5, 1, 3], [COLORS[1], COLORS[1], COLORS[3]])]).arrange(RIGHT, buff=0.65).move_to(DOWN * 4.85)
        positive_caption = text("Positive activations pass through.", 27).move_to(caption)
        self.play(FadeIn(half), ReplacementTransform(caption, positive_caption), run_time=0.3)
        for dot, mapping in zip(positive_dots, positive_maps):
            # Pulse at the same coordinates: positive activations never move.
            self.play(Indicate(dot, scale_factor=1.6, color=dot.get_color()),
                      FadeIn(mapping), run_time=0.45)
        self.finish_section(start, SECTION_SECONDS[3])

        # 5 / 31–34 s: briefly name the property the motion just demonstrated.
        start = self.time
        key = text("ReLU introduces nonlinearity", 31, ACCENT).move_to(DOWN * 4.6)
        kink = Circle(radius=0.23, color=ACCENT, stroke_width=2).move_to(point(0, 0))
        self.play(FadeOut(negative_maps), FadeOut(positive_maps),
                  FadeOut(positive_caption), FadeOut(trails), FadeOut(ref_label),
                  FadeIn(key), Create(kink), run_time=0.5)
        self.play(Indicate(kink, scale_factor=1.5), run_time=0.6)
        self.finish_section(start, SECTION_SECONDS[4])

        # Closing / 34–38 s: reuse the original vector and graph side by side.
        start = self.time
        self.play(FadeOut(regions), FadeOut(reference), FadeOut(kink),
                  FadeOut(moving), FadeOut(half), FadeOut(key),
                  Restore(graph), FadeIn(vectors), run_time=0.7)
        summary = VGroup(text("Negative activations → suppressed", 27),
                         text("Positive activations → pass through", 27)).arrange(DOWN, buff=0.25).move_to(DOWN * 3.15)
        self.play(LaggedStart(*[TransformFromCopy(source, target.copy())
                    for source, target in zip(ins, outs)], lag_ratio=0.15),
                  FadeIn(summary), run_time=0.8)
        ending = VGroup(text("This simple rule gives the network", 25, MUTED),
                        text("nonlinear behavior.", 28, ACCENT)).arrange(DOWN, buff=0.18).move_to(DOWN * 4.7)
        self.play(FadeIn(ending), run_time=0.4)
        self.finish_section(start, SECTION_SECONDS[5])
