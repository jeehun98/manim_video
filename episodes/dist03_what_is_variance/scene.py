"""Distribution mathematics 03: variance as weighted squared distance."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, SPARSE, WEIGHT, txt


NARROW = {-1: .15, 0: .70, 1: .15}
WIDE = {-3: .25, -2: .15, 0: .20, 2: .15, 3: .25}
SAME_VAR_PEAK = {-2: .125, 0: .75, 2: .125}
SAME_VAR_SPLIT = {-1: .5, 1: .5}


class WhatIsVariance(Scene):
    DURATION = 49

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  03", 19, MUTED).move_to(UP * 7.3),
            txt("분산은 무엇을 측정하는가?", 33).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–5: exactly the two examples from the closing image of episode 02.
        self.copy("평균은 같아도 퍼진 정도는 다릅니다", "두 분포 모두 μ = 0")
        top = self.distribution(NARROW, 1.0, 2.1, WEIGHT,
                                labels=(-3, 0, 3))
        bottom = self.distribution(WIDE, -2.35, 5.8, SPARSE,
                                   labels=(-3, 0, 3))
        mean_line = DashedLine([0, -2.45, 0], [0, 3.05, 0],
                               color=ACCENT, dash_length=.13)
        names = VGroup(
            txt("A  좁게", 27, WEIGHT).move_to([-3.05, 2.55, 0]),
            txt("B  넓게", 27, SPARSE).move_to([-3.05, -.8, 0]),
        )
        self.show(VGroup(top, bottom, mean_line, names),
                  FadeIn(top), FadeIn(bottom), Create(mean_line),
                  FadeIn(names), run_time=1.05)
        self.to(5)

        # 5–9: connect the same center to the occupied positions.
        self.copy("차이는 평균에서의 거리", "좁은 A는 짧고, 넓은 B는 깁니다")
        distance_lines = VGroup(*[
            Line([0, .25, 0], [x * .7, .25, 0], color=WEIGHT,
                 stroke_width=2.5)
            for x in (-1, 1)
        ], *[
            Line([0, -3.12, 0], [x * .7, -3.12, 0], color=SPARSE,
                 stroke_width=2.5)
            for x in (-3, -2, 2, 3)
        ])
        self.play(LaggedStart(*[Create(line) for line in distance_lines],
                              lag_ratio=.1), run_time=.95)
        self.stage.add(distance_lines)
        self.to(9)

        # 9–14: signed deviations.
        self.copy("값에서 평균을 빼면", "편차 = x − μ")
        self.clear_stage()
        axis = self.simple_axis(-.75, (-2, 0, 2), .78)
        center = DashedLine([0, -.75, 0], [0, 1.1, 0],
                            color=ACCENT, dash_length=.13)
        dots = VGroup(Dot([-1.56, -.75, 0], radius=.17, color=WEIGHT),
                      Dot([1.56, -.75, 0], radius=.17, color=WEIGHT))
        arrows = VGroup(
            Arrow([0, -.15, 0], [-1.56, -.15, 0], buff=0, color=SPARSE),
            Arrow([0, -.15, 0], [1.56, -.15, 0], buff=0, color=GOOD),
        )
        labels = VGroup(
            txt("−2", 34, SPARSE).move_to([-1.58, .75, 0]),
            txt("+2", 34, GOOD).move_to([1.58, .75, 0]),
            txt("μ = 0", 29, ACCENT).move_to([0, -2.25, 0]),
        )
        self.show(VGroup(axis, center, dots, arrows, labels),
                  Create(axis), Create(center), FadeIn(dots),
                  GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  FadeIn(labels), run_time=1.1)
        self.to(14)

        # 14–18: a direct sum cancels.
        self.copy("그대로 더하면 서로 지워집니다", "−2 + 2 = 0")
        self.clear_stage()
        equation = VGroup(
            txt("−2", 51, SPARSE), txt("+", 45, MUTED),
            txt("2", 51, GOOD), txt("=", 45, MUTED),
            txt("0", 58, ACCENT),
        ).arrange(RIGHT, buff=.35).move_to([0, .65, 0])
        left_arrow = Arrow([-2.95, -1.4, 0], [-.25, -1.4, 0],
                           buff=0, color=SPARSE)
        right_arrow = Arrow([2.95, -1.4, 0], [.25, -1.4, 0],
                            buff=0, color=GOOD)
        self.show(VGroup(equation, left_arrow, right_arrow),
                  FadeIn(equation), GrowArrow(left_arrow),
                  GrowArrow(right_arrow), run_time=.9)
        self.play(FadeOut(left_arrow), FadeOut(right_arrow),
                  Indicate(equation[-1], color=ACCENT), run_time=.65)
        self.stage = VGroup(equation)
        self.to(18)

        # 18–23: the failure persists at a larger distance.
        self.copy("많이 퍼졌는데 합은 0?", "−10 + 10 = 0  ≠  퍼짐 0")
        self.clear_stage()
        axis = self.simple_axis(-.75, (-10, 0, 10), .28)
        dots = VGroup(Dot([-2.8, -.75, 0], radius=.17, color=SPARSE),
                      Dot([2.8, -.75, 0], radius=.17, color=GOOD))
        formula = txt("−10  +  10  =  0", 43, ACCENT).move_to([0, 1.25, 0])
        warning = txt("퍼짐이 0이라는 뜻은 아닙니다", 29, INK)
        warning.move_to([0, -2.45, 0])
        self.show(VGroup(axis, dots, formula, warning),
                  Create(axis), FadeIn(dots), FadeIn(formula),
                  FadeIn(warning), run_time=1.05)
        self.to(23)

        # 23–27: squared deviations avoid the cancellation; no uniqueness claim.
        self.copy("편차를 제곱하면", "양쪽 모두 양수가 되고, 먼 값이 더 커집니다")
        self.clear_stage()
        before = txt("x − μ", 44, MUTED).move_to([0, 2.25, 0])
        after = txt("(x − μ)²", 48, ACCENT).move_to(before)
        examples = VGroup(
            self.formula_card("(−2)² = 4", SPARSE),
            self.formula_card("(+2)² = 4", GOOD),
        ).arrange(RIGHT, buff=.35).move_to([0, -.2, 0])
        far = txt("|x − μ| ↑   →   (x − μ)² ↑", 29, MUTED)
        far.move_to([0, -2.35, 0])
        self.show(VGroup(before), FadeIn(before), run_time=.5)
        self.play(Transform(before, after), run_time=.7)
        self.play(FadeIn(examples), FadeIn(far), run_time=.75)
        self.stage = VGroup(before, examples, far)
        self.to(27)

        # 27–34: each squared distance is weighted by its probability.
        self.copy("분포 전체의 퍼짐을 재면", "제곱거리에 각 위치의 확률을 곱해 더합니다")
        self.clear_stage()
        chart = self.distribution(WIDE, -1.75, 6.2, SPARSE,
                                  labels=(-3, -2, 0, 2, 3))
        center = DashedLine([0, -1.75, 0], [0, .05, 0],
                            color=ACCENT, dash_length=.12)
        distances = VGroup(*[
            Line([0, -2.75, 0], [x * .7, -2.75, 0],
                 color=ACCENT, stroke_width=2, stroke_opacity=.6)
            for x in (-3, -2, 2, 3)
        ])
        formula = txt("Var(X) = Σₓ P(X=x)(x−μ)²", 31, ACCENT)
        formula.move_to([0, 2.75, 0])
        equivalent = txt("= E[(X−μ)²]", 34, GOOD).move_to([0, 1.95, 0])
        example = VGroup(
            txt("B:  2 × .25 × 3²  +  2 × .15 × 2²", 28, INK),
            txt("= 5.70", 31, GOOD),
        ).arrange(DOWN, buff=.17).move_to([0, -3.7, 0])
        self.show(VGroup(chart, center, distances, formula, equivalent, example),
                  FadeIn(chart), Create(center), FadeIn(distances),
                  FadeIn(formula), FadeIn(equivalent), FadeIn(example),
                  run_time=1.25)
        self.to(34)

        # 34–38: same mean; moving the outer mass increases variance.
        self.copy("같은 평균, 다른 분산", "A: 0.30   B: 5.70 → 9.20")
        self.clear_stage()
        top = self.distribution(NARROW, 1.0, 2.1, WEIGHT,
                                labels=(-4, 0, 4))
        bottom = self.distribution(WIDE, -2.35, 5.8, SPARSE,
                                   labels=(-4, 0, 4))
        center = DashedLine([0, -2.45, 0], [0, 3.05, 0],
                            color=ACCENT, dash_length=.13)
        va = txt("Var(A) = 0.30", 28, WEIGHT).move_to([2.45, 2.55, 0])
        vb = txt("Var(B) = 5.70", 28, SPARSE).move_to([2.45, -.8, 0])
        self.show(VGroup(top, bottom, center, va, vb),
                  FadeIn(top), FadeIn(bottom), Create(center),
                  FadeIn(va), FadeIn(vb), run_time=1)
        new_vb = txt("Var(B) = 9.20", 28, SPARSE).move_to(vb)
        self.play(bottom.bars[-3].animate.shift(LEFT * .7),
                  bottom.bars[3].animate.shift(RIGHT * .7),
                  Transform(vb, new_vb), run_time=1.25)
        self.to(38)

        # 38–43: two complementary summaries.
        self.copy("평균과 분산", "위치와 퍼짐을 각각 요약합니다")
        self.clear_stage()
        mean = self.summary_card("Mean", "어디에 있는가", ACCENT)
        variance = self.summary_card("Variance", "얼마나 퍼져 있는가", SPARSE)
        mean.move_to([0, 1.15, 0])
        variance.move_to([0, -1.15, 0])
        center = DashedLine([0, 2.55, 0], [0, 1.95, 0],
                            color=ACCENT, dash_length=.1)
        spread = DoubleArrow([-2.5, -2.35, 0], [2.5, -2.35, 0],
                             color=SPARSE, buff=0)
        self.show(VGroup(mean, variance, center, spread),
                  FadeIn(mean, shift=DOWN * .12),
                  FadeIn(variance, shift=UP * .12),
                  Create(center), GrowArrow(spread), run_time=1.05)
        self.to(43)

        # 43–49: equal mean and variance do not determine the shape.
        self.copy("평균과 분산까지 같다면?", "같은 μ와 σ²라도 분포 모양은 다를 수 있습니다")
        self.clear_stage()
        peak = self.distribution(SAME_VAR_PEAK, 1.0, 2.0, WEIGHT,
                                 labels=(-2, 0, 2))
        split = self.distribution(SAME_VAR_SPLIT, -2.25, 2.8, SPARSE,
                                  labels=(-2, 0, 2))
        labels = VGroup(
            txt("C  단봉형", 25, WEIGHT).move_to([-3.0, 2.45, 0]),
            txt("D  양봉형", 25, SPARSE).move_to([-3.0, -.8, 0]),
        )
        same = txt("μC = μD = 0     Var(C) = Var(D) = 1", 28, ACCENT)
        same.move_to([0, -3.35, 0])
        final = txt("같은 평균 + 같은 분산 = 같은 분포?", 29, INK)
        final.move_to([0, -4.45, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.24,
                                     corner_radius=.13)
        self.show(VGroup(peak, split, labels, same, final, frame),
                  FadeIn(peak), FadeIn(labels[0]), run_time=.75)
        self.play(FadeIn(split), FadeIn(labels[1]), FadeIn(same),
                  run_time=.85)
        self.play(FadeIn(final), Create(frame), run_time=.7)
        self.to(49)

    def distribution(self, probabilities, y, height_scale, color,
                     labels=(-3, 0, 3)):
        xscale = .7
        axis = Arrow([-3.55, y, 0], [3.55, y, 0], buff=0,
                     color=MUTED, stroke_width=2.8,
                     max_tip_length_to_length_ratio=.035)
        ticks = VGroup(*[
            Line([x * xscale, y - .1, 0], [x * xscale, y + .1, 0],
                 color=MUTED)
            for x in labels
        ])
        numbers = VGroup(*[
            txt(str(x), 23, INK).move_to([x * xscale, y - .38, 0])
            for x in labels
        ])
        bars = {}
        group = VGroup()
        for x, p in probabilities.items():
            h = p * height_scale
            bar = RoundedRectangle(width=.43, height=h, corner_radius=.045,
                                   stroke_color=color, stroke_width=1.1,
                                   fill_color=color, fill_opacity=.56)
            bar.move_to([x * xscale, y + h / 2, 0])
            bars[x] = bar
            group.add(bar)
        chart = VGroup(VGroup(axis, ticks, numbers), group)
        chart.bars = bars
        return chart

    def simple_axis(self, y, values, scale):
        axis = Arrow([-3.4, y, 0], [3.4, y, 0], buff=0,
                     color=MUTED, stroke_width=3)
        ticks = VGroup(*[
            Line([x * scale, y - .1, 0], [x * scale, y + .1, 0],
                 color=MUTED)
            for x in values
        ])
        labels = VGroup(*[
            txt(str(x), 25, INK).move_to([x * scale, y - .45, 0])
            for x in values
        ])
        return VGroup(axis, ticks, labels)

    def formula_card(self, value, color):
        box = RoundedRectangle(width=3.25, height=1.3, corner_radius=.18,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=color, fill_opacity=.09)
        return VGroup(box, txt(value, 31, color, 3.0))

    def summary_card(self, title, meaning, color):
        box = RoundedRectangle(width=6.35, height=1.55,
                               corner_radius=.2, stroke_color=color,
                               fill_color=color, fill_opacity=.08)
        label = txt(title, 29, color).move_to([0, .32, 0])
        sub = txt(meaning, 28, INK).move_to([0, -.36, 0])
        return VGroup(box, label, sub)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.15)
        self.head = txt(heading, 32, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 27, INK).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.27)

    def show(self, stage, *animations, run_time=.9):
        self.stage = stage
        self.play(*animations, run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.3)
        self.stage = VGroup()

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.28, remain))
            self.wait(max(0, target - self.time))
