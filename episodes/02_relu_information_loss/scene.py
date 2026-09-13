"""ReLU — Information Loss #1. 42-second silent portrait master."""
from math import erf, sqrt
import os
from manim import *

config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = "#091119"
INK, MUTED, ACCENT = "#EDF3F7", "#94A7B7", "#61E4CF"
PINK = "#FF8C9D"
COLORS = [PINK, "#68D9F0", "#D3A5FF", "#F3CF75"]
VALUES = [[1, 2, 3, 4], [-1, 2, -3, 4], [-1, -2, -3, 1]]


def txt(s, size=30, color=INK):
    return Text(s, font="Arial", font_size=size, color=color)


def column(values, x):
    entries = VGroup(*[txt(f"{v:g}".replace("-", "−"), 36, c)
                      for v, c in zip(values, COLORS)])
    entries.arrange(DOWN, buff=0.35).move_to([x, 1.2, 0])
    brackets = VGroup(*[VMobject().set_points_as_corners([
        [x+s*.52, 2.55, 0], [x+s*.72, 2.55, 0],
        [x+s*.72, -.15, 0], [x+s*.52, -.15, 0]
    ]).set_stroke(MUTED, 2) for s in [-1, 1]])
    return VGroup(brackets, entries)


def distribution(mu, y, scale=1):
    # Equal-width illustrative density bins; zero lies between bins.
    bars = VGroup()
    for x in np.arange(-3.9, 4, .2):
        h = 1.45*np.exp(-.5*((x-mu)/.9)**2)*scale
        bar = Rectangle(width=.14, height=max(.008, h), stroke_width=0,
                        fill_color=PINK if x < 0 else ACCENT, fill_opacity=.85)
        bar.move_to([x*.78, y+h/2, 0])
        bars.add(bar)
    base = Line([-3.3, y, 0], [3.3, y, 0], color=MUTED, stroke_width=1)
    zero = DashedLine([0, y-.15, 0], [0, y+1.7*scale, 0], color=INK, stroke_width=1.5)
    label = txt("0", 20, MUTED).move_to([0, y-.35, 0])
    return VGroup(base, zero, label, bars)


class ReLUInformationLoss(Scene):
    def until(self, seconds):
        if self.time > seconds + .05:
            raise ValueError(f"Timeline overrun: {self.time} > {seconds}")
        if seconds-self.time > .01:
            self.wait(seconds-self.time)

    def construct(self):
        series = txt("ACTIVATION FUNCTION SERIES / 02", 20, MUTED).move_to(UP*6.6)
        title = txt("Same rule.", 48).move_to(UP*5.45)
        formula = txt("f(x) = max(0, x)", 34, ACCENT).move_to(UP*4.45)
        self.play(FadeIn(series), FadeIn(title), FadeIn(formula), run_time=.6)
        vectors = VGroup(*[column(v, x) for v, x in zip(VALUES, [-2.65, 0, 2.65])])
        names = VGroup(*[txt(n, 30).move_to([x, 3.1, 0]) for n, x in zip("ABC", [-2.65, 0, 2.65])])
        caption = txt("Different inputs. Different effects.", 29).move_to(DOWN*2)
        self.play(LaggedStart(*[FadeIn(v, shift=UP*.15) for v in vectors], lag_ratio=.2), FadeIn(names), run_time=.9)
        self.wait(.6)
        for i in range(4):
            self.play(*[Transform(v[1][i], txt(str(max(0, vals[i])), 36, COLORS[i]).move_to(v[1][i]))
                        for v, vals in zip(vectors, VALUES)], run_time=.65)
        self.play(FadeIn(caption), run_time=.5)
        self.until(7)

        counts = VGroup()
        for v, vals in zip(vectors, VALUES):
            n = sum(x < 0 for x in vals)
            metric = VGroup(txt(f"{n} / 4 zeroed", 25, MUTED), txt(f"{n/4:.0%}", 45, ACCENT)).arrange(DOWN, buff=.2).move_to([v.get_center()[0], -1.55, 0])
            sources = VGroup(*[v[1][i] for i, x in enumerate(vals) if x < 0])
            if n:
                self.play(Indicate(sources), run_time=.35)
                self.play(TransformFromCopy(sources, metric), run_time=.45)
            else:
                self.play(FadeIn(metric), run_time=.8)
            counts.add(metric)
        definition = VGroup(txt("Zeroed Ratio", 36, ACCENT),
                            txt("negative entries / all entries", 27),
                            txt("A suppression indicator", 23, MUTED)).arrange(DOWN, buff=.28).move_to(DOWN*3.85)
        self.play(FadeOut(caption), FadeIn(definition), Transform(title, txt("Count the suppressed values", 37).move_to(title)), run_time=.6)
        self.until(14)

        charts = VGroup(*[distribution(mu, y) for mu, y in zip([1.3, 0, -1.3], [2, -.8, -3.6])])
        labels = VGroup(*[txt(s, 24, MUTED).move_to([0, y+1.95, 0]) for s, y in zip(
            ["Mostly positive → small fraction", "Balanced → roughly half", "Mostly negative → large fraction"], [2, -.8, -3.6])])
        self.play(FadeOut(counts), FadeOut(definition), FadeOut(names),
                  Transform(title, txt("From values to distributions", 36).move_to(title)),
                  *[ReplacementTransform(v, c) for v, c in zip(vectors, charts)], FadeIn(labels), run_time=.8)
        note = txt("Illustrative distributions", 22, MUTED).move_to(DOWN*5)
        self.play(FadeIn(note), run_time=.3)
        self.wait(.8)
        for chart in charts:
            negatives = list(chart[3])[:20]
            # Stack the negative bins at zero; this is discrete mass, not density.
            targets = []
            height = 0.0
            for b in negatives:
                mass_height = b.height * .10
                targets.append(b.animate.stretch_to_fit_width(.12).stretch_to_fit_height(mass_height).move_to([0, chart[0].get_y()+height+mass_height/2, 0]))
                height += mass_height
            self.play(*targets, run_time=.65)
        collapse = txt("Negative values collect at zero", 27, PINK).move_to(DOWN*5.8)
        self.play(FadeIn(collapse), run_time=.4)
        self.until(21)

        tracker = ValueTracker(0)
        large = always_redraw(lambda: distribution(tracker.get_value(), -.7, 1.7))
        probability = always_redraw(lambda: txt(f"P(X < 0) ≈ {0.5*(1+erf(-tracker.get_value()/(.9*sqrt(2)))):.2f}", 40, PINK).move_to(DOWN*2.3))
        explanation = VGroup(txt("Expected fraction suppressed", 28), txt("Symmetric example, centered at zero", 23, MUTED)).arrange(DOWN, buff=.3).move_to(DOWN*3.5)
        self.play(FadeOut(labels), FadeOut(collapse), ReplacementTransform(charts, large),
                  Transform(title, txt("The input predicts the fraction", 35).move_to(title)), FadeIn(probability), FadeIn(explanation), run_time=.8)
        self.wait(.7)
        self.play(tracker.animate.set_value(1.3), FadeOut(explanation[1]), run_time=1.5)
        self.wait(.4)
        self.play(tracker.animate.set_value(-1.3), run_time=1.5)
        self.until(28)

        self.play(FadeOut(large), FadeOut(probability), FadeOut(explanation), FadeOut(note),
                  Transform(title, txt("Is counting enough?", 43).move_to(title)), run_time=.6)
        cards = VGroup()
        for name, values, y in [("A", ["−0.01", "−0.02", "3", "4"], 2.1), ("B", ["−10", "−20", "3", "4"], -.5)]:
            row = VGroup(*[txt(v, 35, c) for v, c in zip(values, COLORS)]).arrange(RIGHT, buff=.45).move_to([0, y, 0])
            label = txt(name, 26, MUTED).next_to(row, LEFT, buff=.4)
            cards.add(VGroup(label, row))
        self.play(FadeIn(cards), run_time=.5)
        self.wait(.6)
        result = txt("[ 0, 0, 3, 4 ]", 37, ACCENT).move_to(DOWN*2.4)
        self.play(TransformFromCopy(cards[0][1], result), run_time=.7)
        self.play(Indicate(cards[1][1]), run_time=.3)
        ratio = txt("Both: 2 / 4 zeroed = 50%", 32).move_to(DOWN*3.5)
        self.play(FadeIn(ratio), run_time=.5)
        self.play(*[Indicate(VGroup(c[1][0], c[1][1]), color=PINK) for c in cards], run_time=.8)
        magnitude = txt("Same count. Different magnitudes.", 29, PINK).move_to(DOWN*4.7)
        self.play(FadeIn(magnitude), run_time=.4)
        self.until(36)

        self.play(Transform(title, txt("ReLU — Information Loss #1", 35).move_to(title)),
                  FadeOut(formula), FadeOut(ratio), FadeOut(magnitude), FadeOut(result),
                  cards.animate.scale(.85).shift(UP*.5), run_time=.6)
        question = VGroup(txt("Same zeroed ratio.", 32), txt("Same information loss?", 36, PINK)).arrange(DOWN, buff=.3).move_to(DOWN*2.4)
        next_ep = VGroup(txt("NEXT", 21, MUTED), txt("How much was removed?", 35, ACCENT)).arrange(DOWN, buff=.25).move_to(DOWN*4.4)
        self.play(FadeIn(question), run_time=.6)
        self.wait(.8)
        self.play(FadeIn(next_ep, shift=UP*.15), run_time=.5)
        self.until(42)
