"""40-second ReLU episode: beyond counts, absolute and relative change."""
import os
from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = "#091119"
INK, MUTED, ACCENT = "#EDF3F7", "#94A7B7", "#61E4CF"
COLORS = ["#FF8C9D", "#68D9F0", "#D3A5FF", "#F3CF75"]
VALUES = [[-.1, -.2, 3, 4], [-10, -20, 3, 4]]


def text(s, size=30, color=INK):
    return Text(s, font="Arial", font_size=size, color=color)


def column(values, x, y=1.5):
    entries = VGroup(*[text(f"{v:g}".replace("-", "−"), 34, c)
                      for v, c in zip(values, COLORS)]).arrange(DOWN, buff=.3).move_to([x, y, 0])
    brackets = VGroup(*[VMobject().set_points_as_corners([
        [x+s*.66, y+1.35, 0], [x+s*.82, y+1.35, 0],
        [x+s*.82, y-1.35, 0], [x+s*.66, y-1.35, 0]
    ]).set_stroke(MUTED, 2) for s in [-1, 1]])
    return VGroup(brackets, entries)


class ReLUChangeMagnitude(Scene):
    def until(self, end):
        if self.time > end+.05:
            raise ValueError(f"Section overrun: {self.time} > {end}")
        if end-self.time > .02:
            self.wait(end-self.time)

    def construct(self):
        series = text("ACTIVATION FUNCTION SERIES / 03", 20, MUTED).move_to(UP*6.6)
        title = text("Previously: count the changes", 34).move_to(UP*5.4)
        rule = text("ReLU: negative → zero", 29, ACCENT).move_to(UP*4.35)
        self.play(FadeIn(series), FadeIn(title), FadeIn(rule), run_time=.5)
        a = column(VALUES[0], -2.05)
        a_name = text("A", 30).move_to([-2.05, 3.85, 0])
        a_original = a.copy()
        self.play(FadeIn(a), FadeIn(a_name), run_time=.5)
        self.play(*[Transform(a[1][i], text("0", 34, COLORS[i]).move_to(a[1][i])) for i in [0, 1]], run_time=.7)
        ratio_a = VGroup(text("2 / 4 changed", 25, MUTED), text("50%", 48, ACCENT)).arrange(DOWN, buff=.2).move_to([-2.05, -1.15, 0])
        ratio_label = text("Zeroed Ratio", 29, MUTED).move_to(DOWN*2.6)
        self.play(TransformFromCopy(VGroup(a[1][0], a[1][1]), ratio_a), FadeIn(ratio_label), run_time=.6)
        self.until(3)

        b = column(VALUES[1], 2.05)
        b_original = b.copy()
        b_name = text("B", 30).move_to([2.05, 3.85, 0])
        self.play(FadeIn(b), FadeIn(b_name), run_time=.5)
        self.play(*[Transform(b[1][i], text("0", 34, COLORS[i]).move_to(b[1][i])) for i in [0, 1]], run_time=.7)
        ratio_b = ratio_a.copy().move_to([2.05, -1.15, 0])
        self.play(TransformFromCopy(VGroup(b[1][0], b[1][1]), ratio_b), run_time=.5)
        self.play(Indicate(ratio_a[1]), Indicate(ratio_b[1]), run_time=.5)
        self.play(Transform(a, a_original), Transform(b, b_original),
                  Transform(rule, text("But was the change the same?", 29, MUTED).move_to(rule)), run_time=.6)
        self.play(*[Indicate(VGroup(v[1][0], v[1][1])) for v in [a, b]], run_time=.6)
        self.until(7)

        # All eight bars use the same linear scale: 0.17 scene units per unit.
        bars, bar_labels, baselines = VGroup(), VGroup(), VGroup()
        for vals, center in zip(VALUES, [-2.05, 2.05]):
            group, labels = VGroup(), VGroup()
            for i, value in enumerate(vals):
                x = center+(i-1.5)*.65
                h = abs(value)*.17
                group.add(Rectangle(width=.4, height=h, stroke_width=0,
                                    fill_color=COLORS[i], fill_opacity=.9).move_to([x, .1+h/2, 0]))
                labels.add(text(f"{abs(value):g}", 22, COLORS[i]).move_to([x, -.2, 0]))
            bars.add(group); bar_labels.add(labels)
            baselines.add(Line([center-1.35, .1, 0], [center+1.35, .1, 0], color=MUTED, stroke_width=1))
        scale_note = text("Absolute values • same scale", 23, MUTED).move_to(DOWN*3.1)
        self.play(FadeOut(a[0]), FadeOut(b[0]), FadeOut(ratio_label),
                  *[ReplacementTransform(v[1][i], bars[j][i]) for j, v in enumerate([a, b]) for i in range(4)],
                  FadeIn(bar_labels), FadeIn(baselines), FadeIn(scale_note),
                  Transform(title, text("How much changed?", 44).move_to(title)), run_time=.9)
        self.wait(.5)
        ghosts = VGroup(*[bar.copy().set_fill(opacity=.08).set_stroke(bar.get_color(), 1, opacity=.4)
                          for group in bars for bar in list(group)[:2]])
        self.add(ghosts)
        self.play(*[bars[j][i].animate.stretch_to_fit_height(.001).move_to([bars[j][i].get_x(), .1, 0]).set_opacity(0)
                    for j in range(2) for i in range(2)],
                  Transform(rule, text("ReLU removes the negative entries", 28, ACCENT).move_to(rule)), run_time=1.2)
        contrast = VGroup(text("Same number changed.", 30), text("The size of what vanished differs.", 28, COLORS[0])).arrange(DOWN, buff=.3).move_to(DOWN*4.35)
        self.play(FadeIn(contrast), run_time=.5)
        self.until(11)

        # Reuse the retained bars as the output and ghosts as removed entries.
        outputs = VGroup(column([0, 0, 3, 4], -2.05), column([0, 0, 3, 4], 2.05))
        self.play(*[ReplacementTransform(bars[j], outputs[j]) for j in range(2)],
                  FadeOut(ghosts), FadeOut(bar_labels), FadeOut(baselines), FadeOut(scale_note),
                  FadeOut(ratio_a), FadeOut(ratio_b), FadeOut(contrast),
                  Transform(rule, text("input − output = removed part", 29, ACCENT).move_to(rule)), run_time=.7)
        inputs = VGroup(column(VALUES[0], -2.05), column(VALUES[1], 2.05))
        self.play(*[Transform(outputs[j], inputs[j]) for j in range(2)], run_time=.6)
        subtraction = text("− [ 0, 0, 3, 4 ]", 31, MUTED).move_to(DOWN*1)
        self.play(FadeIn(subtraction), run_time=.4)
        removed = VGroup(column([-.1, -.2, 0, 0], -2.05), column([-10, -20, 0, 0], 2.05))
        self.play(*[Transform(outputs[j][1][i], removed[j][1][i]) for j in range(2) for i in range(4)], run_time=.9)
        difference = text("Δx = x − ReLU(x)", 37, ACCENT).move_to(DOWN*2.5)
        self.play(FadeOut(subtraction), FadeIn(difference),
                  Transform(title, text("The removed part is a vector", 35).move_to(title)), run_time=.5)
        self.until(16)

        length_title = text("Size of the removed part", 35).move_to(title)
        norm = text("Change magnitude = ‖Δx‖", 32, ACCENT).move_to(difference)
        lengths = [np.linalg.norm([-.1, -.2]), np.linalg.norm([-10, -20])]
        indicators, numbers = VGroup(), VGroup()
        for center, length in zip([-2.05, 2.05], lengths):
            h = length*.14
            indicators.add(Rectangle(width=.6, height=h, stroke_width=0, fill_color=ACCENT, fill_opacity=.9).move_to([center, -.6+h/2, 0]))
            numbers.add(text(f"{length:.3f}", 36, ACCENT).move_to([center, -1.25, 0]))
        detail = text("Vector length (Euclidean) • same scale", 22, MUTED).move_to(DOWN*3.4)
        self.play(*[TransformFromCopy(outputs[j][1], indicators[j]) for j in range(2)],
                  *[FadeOut(o) for o in outputs], Transform(title, length_title),
                  FadeOut(rule), Transform(difference, norm), FadeIn(numbers), FadeIn(detail), run_time=.8)
        times = text("B removes 100× the magnitude", 30, COLORS[0]).move_to(DOWN*4.6)
        self.play(FadeIn(times), run_time=.5)
        self.until(20)

        # The ratio compares Euclidean lengths; it is not an additive decomposition.
        whole_lengths = [np.linalg.norm(v) for v in VALUES]
        ratios = [delta / whole for delta, whole in zip(lengths, whole_lengths)]
        comparison = VGroup()
        for center, delta, whole in zip([-2.05, 2.05], lengths, whole_lengths):
            pair = VGroup()
            for offset, value, color, label in [(-.72, whole, MUTED, "Input"), (.72, delta, ACCENT, "Change")]:
                h = value*.13
                bar = Rectangle(width=.55, height=h, stroke_width=0, fill_color=color, fill_opacity=.9).move_to([center+offset, -.5+h/2, 0])
                number = text(f"{value:.3f}", 24, color).next_to(bar, UP, buff=.15)
                name = text(label, 23, color).move_to([center+offset, -.9, 0])
                pair.add(VGroup(bar, number, name))
            comparison.add(pair)
        self.play(*[ReplacementTransform(indicators[j], comparison[j]) for j in range(2)], FadeOut(numbers), FadeOut(times),
                  FadeOut(difference), Transform(title, text("Compared with the whole input", 34).move_to(title)),
                  Transform(detail, text("Input size gives the change context", 26, MUTED).move_to(DOWN*2)), run_time=.7)
        fraction = VGroup(text("Relative change", 34, ACCENT), text("‖x − ReLU(x)‖ / ‖x‖", 34)).arrange(DOWN, buff=.25).move_to(DOWN*3.3)
        self.wait(.6)
        self.play(FadeIn(fraction), run_time=.5)
        self.wait(.5)
        normalized, calculations = VGroup(), VGroup()
        for center, ratio, delta, whole in zip([-2.05, 2.05], ratios, lengths, whole_lengths):
            outline = Rectangle(width=2.8, height=.55, stroke_color=MUTED, stroke_width=2).move_to([center, 1.7, 0])
            fill = Rectangle(width=2.8*ratio, height=.51, stroke_width=0, fill_color=ACCENT, fill_opacity=.95).move_to([center-1.4+1.4*ratio, 1.7, 0])
            label = text(f"≈ {ratio:.1%}", 46, ACCENT).move_to([center, .55, 0])
            normalized.add(VGroup(outline, fill, label))
            calculations.add(text(f"{delta:.3f} / {whole:.3f}", 26, MUTED).move_to([center, -.5, 0]))
        self.play(*[ReplacementTransform(comparison[j], normalized[j]) for j in range(2)], FadeIn(calculations),
                  Transform(detail, text("Each outline = its original input size", 24, MUTED).move_to(DOWN*1.7)), run_time=.8)
        relative_note = text("Same count. Very different relative change.", 26, COLORS[0]).move_to(DOWN*4.65)
        self.play(FadeIn(relative_note), run_time=.5)
        self.until(29)

        summary = VGroup()
        for center, ratio in zip([-2.05, 2.05], ratios):
            group = VGroup(text("Changed entries", 25, MUTED), text("50%", 42, MUTED),
                           text("Relative change", 25, ACCENT), text(f"≈ {ratio:.1%}", 48, ACCENT)).arrange(DOWN, buff=.3).move_to([center, 1.6, 0])
            summary.add(group)
        message = VGroup(text("Counting alone can miss the difference.", 28),
                         text("Size and proportion may matter more.", 29, COLORS[0])).arrange(DOWN, buff=.4).move_to(DOWN*1.5)
        self.play(*[ReplacementTransform(normalized[j], summary[j]) for j in range(2)], FadeOut(calculations), FadeOut(detail),
                  FadeOut(fraction), FadeOut(relative_note), FadeIn(message),
                  Transform(title, text("Beyond how many changed", 36).move_to(title)), run_time=.8)
        self.until(34)

        conclusion = VGroup(text("How many changed?", 29, MUTED),
                            text("How much, relative to the input?", 30, ACCENT)).arrange(DOWN, buff=.35).move_to(DOWN*1.15)
        question = VGroup(text("The measure shapes the interpretation.", 26),
                          text("Which change matters more?", 33, COLORS[0])).arrange(DOWN, buff=.4).move_to(DOWN*3.8)
        self.play(ReplacementTransform(message, conclusion), FadeIn(question),
                  Transform(title, text("Same ReLU. A different perspective.", 32).move_to(title)), run_time=.8)
        self.until(40)
