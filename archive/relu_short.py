"""Render with: python -m manim render relu_short.py ReLUShort"""
from manim import *
import os

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = "#071018"

CYAN = "#6EF2E1"
WHITE = "#EAF7F6"
MUTED = "#7F9795"
RED = "#FF7A88"


def label(value, size=34, color=WHITE):
    return Text(value, font="Arial", font_size=size, color=color)


def neon(shape):
    """A restrained halo, kept behind the crisp outline."""
    return VGroup(
        shape.copy().set_stroke(CYAN, width=12, opacity=0.035),
        shape.copy().set_stroke(CYAN, width=7, opacity=0.10),
        shape,
    )


class ReLUShort(Scene):
    def construct(self):
        # All beats are multiples of 0.1 s: 300 frames / 30 fps = 10 s.
        eyebrow = label("ACTIVATION FUNCTION", 21, MUTED).move_to(UP * 5.7)
        title = label("ReLU", 76).move_to(UP * 4.8)
        subtitle = label("What happens to a negative value?", 23, MUTED)
        subtitle.move_to(UP * 3.9)
        self.play(FadeIn(eyebrow), FadeIn(title, shift=UP * 0.15),
                  FadeIn(subtitle), run_time=0.8)

        input_shape = RoundedRectangle(width=3.2, height=0.95,
            corner_radius=0.16, stroke_color=CYAN, stroke_width=2).move_to(UP * 2.5)
        input_node = neon(input_shape)
        input_text = label("x = −3").move_to(input_shape)
        self.play(Create(input_node), FadeIn(input_text), run_time=0.7)

        operator_shape = Circle(radius=0.65, stroke_color=CYAN, stroke_width=2)
        operator = neon(operator_shape)
        operator_text = label("ReLU", 29)
        line_in = Line(input_shape.get_bottom(), operator_shape.get_top(),
                       color=CYAN, stroke_width=2)
        self.play(Create(line_in), Create(operator), FadeIn(operator_text), run_time=0.7)

        particle = VGroup(Dot(radius=0.19, color=CYAN, fill_opacity=0.15,
                              stroke_opacity=0), Dot(radius=0.075, color=CYAN))
        particle.move_to(input_shape.get_bottom())
        self.add(particle)
        self.play(particle.animate.move_to(operator_shape.get_top()), run_time=0.8)
        self.play(FadeOut(particle), Indicate(operator, color=CYAN, scale_factor=1.08),
                  run_time=0.4)

        value = label("−3", 38, RED)
        zero = label("0", 38, CYAN)
        self.play(FadeOut(operator_text), FadeIn(value), run_time=0.3)
        self.play(Transform(value, zero), run_time=0.6)
        self.wait(0.3)
        self.play(FadeOut(value), FadeIn(operator_text), run_time=0.3)

        output_shape = RoundedRectangle(width=3.2, height=0.95,
            corner_radius=0.16, stroke_color=CYAN, stroke_width=2).move_to(DOWN * 2.5)
        output_node = neon(output_shape)
        output_text = label("y = 0", color=CYAN).move_to(output_shape)
        line_out = Line(operator_shape.get_bottom(), output_shape.get_top(),
                        color=CYAN, stroke_width=2)
        particle.move_to(operator_shape.get_bottom())
        self.add(particle)
        self.play(Create(line_out), particle.animate.move_to(output_shape.get_top()),
                  run_time=0.7)
        self.play(Create(output_node), FadeIn(output_text), FadeOut(particle), run_time=0.6)

        equation = label("ReLU(x) = max(0, x)", 34).move_to(DOWN * 4.5)
        equation_frame = neon(RoundedRectangle(width=6.7, height=1.05,
            corner_radius=0.16, stroke_color=CYAN, stroke_width=1.3).move_to(equation))
        self.play(Create(equation_frame), Write(equation), run_time=0.9)
        conclusion = label("Negative values are clipped to zero", 23, MUTED)
        conclusion.move_to(DOWN * 5.5)
        self.play(FadeIn(conclusion, shift=UP * 0.1), run_time=0.4)
        self.wait(2.5)
