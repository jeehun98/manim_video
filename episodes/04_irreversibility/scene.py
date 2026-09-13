"""100-second portrait episode: different inputs, indistinguishable outputs.

No LaTeX or audio required. Render through scripts/render.py 04.
Irreversible here means not uniquely invertible from the output alone,
on the stated input domain, rather than thermodynamic irreversibility.
"""
import os
from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = "#091119"
INK, MUTED, ACCENT = "#EDF3F7", "#94A7B7", "#61E4CF"
COLORS = ["#FF8C9D", "#68D9F0", "#D3A5FF", "#F3CF75"]


def text(s, size=32, color=INK):
    if any(c in s for c in "₁₂₃"):
        for digit, sub in zip("123", "₁₂₃"):
            s = s.replace(sub, f"<sub>{digit}</sub>")
        obj = MarkupText(s, font="Arial", font_size=size, color=color)
    else:
        obj = Text(s, font="Arial", font_size=size, color=color)
    if obj.width > 7.5:
        obj.scale_to_fit_width(7.5)
    return obj


def mapping(values, output):
    inputs = VGroup(*[text(v, 44, COLORS[i % 4]) for i, v in enumerate(values)])
    for entry in inputs:
        if entry.width > 3.1:
            entry.scale_to_fit_width(3.1)
    inputs.arrange(DOWN, buff=.65).move_to([-2.5, 1, 0])
    result = text(output, 66, ACCENT).move_to([2.2, 1, 0])
    arrows = VGroup(*[Arrow(v.get_right()+RIGHT*.18, result.get_left()+LEFT*.18,
                           buff=.08, color=MUTED, stroke_width=3,
                           max_tip_length_to_length_ratio=.1) for v in inputs])
    return VGroup(inputs, arrows, result)


class Irreversibility(Scene):
    def until(self, end):
        if self.time > end + .05:
            raise ValueError(f"Section overrun: {self.time} > {end}")
        if end - self.time > .02:
            self.wait(end - self.time)

    def construct(self):
        series = text("COMPUTATION & INFORMATION / 04", 20, MUTED).move_to(UP*6.6)
        title = text("Nonlinearity", 46).move_to(UP*5.3)
        operation = text("Express more complex relationships", 29, ACCENT).move_to(UP*3.9)
        caption = text("Activation functions", 30, MUTED).move_to(DOWN*2.2)
        detail = text("", 24)
        axes = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=6,
                    y_length=4, tips=False, axis_config={"color": MUTED, "stroke_width": 2}).move_to(UP*.6)
        curve = axes.plot(lambda x: .7*x, color=COLORS[1])
        self.play(FadeIn(series), FadeIn(title), FadeIn(operation), Create(axes), Create(curve), FadeIn(caption), run_time=1)
        self.play(Transform(curve, axes.plot(lambda x: x**3/4, color=ACCENT)), run_time=2)
        self.until(8)

        graph = mapping(["x₁", "x₂", "x₃"], "y")
        self.play(ReplacementTransform(VGroup(axes, curve), graph),
                  Transform(title, text("Another property", 43).move_to(title)),
                  Transform(operation, text("Different inputs → same output", 31, ACCENT).move_to(operation)),
                  Transform(caption, text("Some differences cannot be recovered", 29).move_to(caption)), run_time=1)
        self.play(Transform(title, text("Irreversibility", 46).move_to(title)),
                  Transform(detail, text("Nonlinear ≠ irreversible", 26, MUTED).move_to(DOWN*3.5)), run_time=.7)
        self.until(17)

        self.play(Transform(graph, mapping(["−1", "−10", "−100"], "0")),
                  Transform(operation, text("ReLU", 38, ACCENT).move_to(operation)),
                  Transform(caption, text("Different negative values. One zero.", 30).move_to(caption)),
                  FadeOut(detail), run_time=.8)
        travellers = [graph[2].copy() for _ in graph[0]]
        self.play(*[TransformFromCopy(v, target) for v, target in zip(graph[0], travellers)], run_time=1.3)
        self.remove(*travellers)
        self.until(24)
        detail = text("y = 0 tells us only: x ≤ 0", 29, ACCENT).move_to(DOWN*3.5)
        self.play(Transform(caption, text("Which input produced this zero?", 31).move_to(caption)),
                  FadeIn(detail), Circumscribe(graph[2], color=ACCENT), run_time=.8)
        self.until(30)
        self.play(Transform(operation, text("Many-to-One", 36, ACCENT).move_to(operation)),
                  Transform(caption, text("Distinguishable before. Same after.", 30).move_to(caption)), run_time=.7)
        self.until(34)

        for name, values, output, erased, note, end in [
            ("Absolute value  |x|", ["−3", "+3"], "3", "Sign information disappears", "Input domain: real numbers", 41),
            ("Square  x²", ["−2", "+2"], "4", "Sign information disappears", "Magnitude is still recoverable: |x| = √y", 46),
        ]:
            self.play(Transform(graph, mapping(values, output)),
                      Transform(title, text("The same structure appears elsewhere", 31).move_to(title)),
                      Transform(operation, text(name, 35, ACCENT).move_to(operation)),
                      Transform(caption, text(erased, 31, COLORS[0]).move_to(caption)),
                      Transform(detail, text(note, 25, MUTED).move_to(detail)), run_time=.8)
            self.until(end)

        # Show an actual pooling window before revealing a second possible input.
        pool = VGroup(*[text(v, 43, ACCENT if i == 1 else COLORS[0]) for i,v in enumerate(["1","7","3","2"])])
        for i, v in enumerate(pool):
            v.move_to([(i-1.5)*1.5, 1.5, 0])
        boxes = VGroup(*[RoundedRectangle(width=1.25, height=1.2, corner_radius=.12,
                         stroke_color=MUTED, stroke_width=2).move_to(v) for v in pool])
        self.play(ReplacementTransform(graph, pool), FadeIn(boxes),
                  Transform(operation, text("Max Pooling", 36, ACCENT).move_to(operation)),
                  Transform(caption, text("Only the maximum remains", 31).move_to(caption)),
                  Transform(detail, text("Non-selected values are not recoverable", 25, MUTED).move_to(detail)), run_time=.8)
        self.play(*[FadeOut(pool[i]) for i in [0,2,3]], FadeOut(boxes),
                  pool[1].animate.move_to(UP).scale(1.5), run_time=1.1)
        self.until(51)
        graph = mapping(["[1, 7, 3, 2]", "[6, 7, 0, 4]"], "7")
        self.play(ReplacementTransform(pool[1], graph), run_time=.8)
        self.until(54)

        self.play(Transform(graph, mapping(["1.01", "1.02", "1.03"], "1.0")),
                  Transform(operation, text("Quantization", 36, ACCENT).move_to(operation)),
                  Transform(caption, text("Small differences disappear", 31, COLORS[0]).move_to(caption)),
                  Transform(detail, text("Example: round to the nearest 0.1", 25, MUTED).move_to(detail)), run_time=.8)
        self.until(61)
        self.play(Transform(graph, mapping(["x₁", "x₂", "x₃"], "y")),
                  Transform(title, text("Different operations. Different losses.", 32).move_to(title)),
                  Transform(operation, text("Fewer distinctions survive", 34, ACCENT).move_to(operation)),
                  Transform(caption, text("Some input states become indistinguishable", 27).move_to(caption)),
                  Transform(detail, text("This need not reduce the vector dimension", 25, MUTED).move_to(detail)), run_time=.8)
        self.until(66)

        # Output constraints are properties of these specific operations.
        # They are not a universal consequence of being non-injective.
        line = NumberLine(x_range=[-2, 4, 1], length=6.6, color=MUTED, include_numbers=False).move_to(UP*.7)
        zero = text("0", 29).next_to(line.n2p(0), DOWN, buff=.25)
        allowed = Arrow(line.n2p(0), line.n2p(4)+RIGHT*.2, buff=0, color=ACCENT, stroke_width=9)
        region = VGroup(line, zero, allowed)
        self.play(ReplacementTransform(graph, region),
                  Transform(title, text("More than information loss", 38).move_to(title)),
                  Transform(operation, text("ReLU / output constraint", 32, ACCENT).move_to(operation)),
                  Transform(caption, text("y ≥ 0", 54, ACCENT).move_to(caption)),
                  Transform(detail, text("Every ReLU output is non-negative", 27, MUTED).move_to(detail)), run_time=.9)
        samples = VGroup(*[Dot(line.n2p(v)+UP*.6, color=COLORS[0], radius=.1) for v in [-1.5,-.5,1.5,3]])
        self.play(FadeIn(samples), run_time=.4)
        self.play(*[d.animate.move_to(line.n2p(max(0,v))) .set_color(ACCENT) for d,v in zip(samples,[-1.5,-.5,1.5,3])], run_time=1.1)
        self.until(74)

        clamp_line = NumberLine(x_range=[-1,2,.5], length=6.6, color=MUTED, include_numbers=False).move_to(UP*.7)
        interval = Line(clamp_line.n2p(0), clamp_line.n2p(1), color=ACCENT, stroke_width=9)
        clamp = VGroup(clamp_line, interval, *[Dot(clamp_line.n2p(v), color=ACCENT) for v in [0,1]],
                       *[text(str(v),29).next_to(clamp_line.n2p(v),DOWN,buff=.25) for v in [0,1]])
        self.play(ReplacementTransform(region,clamp), FadeOut(samples),
                  Transform(operation,text("Clamp / chosen bounds",32,ACCENT).move_to(operation)),
                  Transform(caption,text("0 ≤ y ≤ 1",48,ACCENT).move_to(caption)),
                  Transform(detail,text("Example: clamp to [0, 1]",27,MUTED).move_to(detail)),run_time=.8)
        incoming=VGroup(*[Dot(clamp_line.n2p(v)+UP*.65,color=COLORS[0],radius=.11) for v in [-.8,.4,1.8]])
        self.play(FadeIn(incoming),run_time=.4)
        self.play(*[d.animate.move_to(clamp_line.n2p(np.clip(v,0,1))).set_color(ACCENT) for d,v in zip(incoming,[-.8,.4,1.8])],run_time=1)
        self.until(80)

        grid_line = NumberLine(x_range=[.8,1.2,.1],length=6.6,color=MUTED,include_numbers=False).move_to(UP*.7)
        grid=VGroup(grid_line,*[Dot(grid_line.n2p(v),color=ACCENT,radius=.12) for v in [.8,.9,1,1.1,1.2]],
                    *[text(f"{v:.1f}",25).next_to(grid_line.n2p(v),DOWN,buff=.25) for v in [.8,.9,1,1.1,1.2]])
        self.play(ReplacementTransform(clamp,grid),FadeOut(incoming),
                  Transform(operation,text("Quantization / discrete levels",31,ACCENT).move_to(operation)),
                  Transform(caption,text("Outputs lie on a grid",36,ACCENT).move_to(caption)),
                  Transform(detail,text("0.1-spaced levels • a local view",25,MUTED).move_to(detail)),run_time=.8)
        incoming=VGroup(*[Dot(grid_line.n2p(v)+UP*(.5+i*.3),color=COLORS[i],radius=.09) for i,v in enumerate([1.01,1.02,1.03])])
        self.play(FadeIn(incoming),run_time=.4)
        self.play(*[d.animate.move_to(grid_line.n2p(1)).set_color(ACCENT) for d in incoming],run_time=1.2)
        self.until(86)
        self.play(Transform(title,text("Discard differences. Know the output.",32).move_to(title)),
                  Transform(caption,text("The possible output becomes clearer",30,ACCENT).move_to(caption)),run_time=.7)
        self.until(91)

        final_graph=mapping(["x₁","x₂","x₃"],"y")
        self.play(ReplacementTransform(grid,final_graph),FadeOut(incoming),
                  Transform(title,text("More than information loss",38).move_to(title)),
                  Transform(operation,text("Many-to-One",36,ACCENT).move_to(operation)),
                  Transform(caption,text("Some distinctions are discarded",31,COLORS[0]).move_to(caption)),
                  Transform(detail,text("Output constraints remain knowable",30,ACCENT).move_to(detail)),run_time=.9)
        endnote=text("ReLU: y ≥ 0   •   Clamp: 0 ≤ y ≤ 1",25,MUTED).move_to(DOWN*4.8)
        self.play(FadeIn(endnote),run_time=.5)
        self.until(100)
