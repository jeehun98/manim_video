"""Distribution mathematics 02: mode, median, mean, and spread."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, BG, GOOD, INK, MUTED, SPARSE, WEIGHT, txt


BASE = dict(zip(range(-4, 5), (.04, .07, .11, .18, .20, .18, .11, .07, .04)))
WITH_OUTLIER = {x: p * .92 for x, p in BASE.items()} | {8: .08}
SKEWED = dict(zip((*range(-4, 5), 8),
                  (.02, .03, .05, .08, .20, .18, .15, .10, .07, .12)))


class WhereIsCenter(Scene):
    DURATION = 70

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  02", 19, MUTED).move_to(UP * 7.3),
            txt("분포의 중심은 어디일까?", 33).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–7: pick up the question from episode 01.
        self.copy("분포를 숫자 하나로 대표한다면?", "어느 위치가 분포의 중심일까요?")
        chart = self.chart(BASE, lambda x: x * .67, -1.6)
        center_line = DashedLine([0, -1.58, 0], [0, 1.25, 0],
                                 color=ACCENT, dash_length=.12)
        question = txt("?", 50, ACCENT).move_to([0, 2.15, 0])
        self.show(VGroup(chart, center_line, question),
                  FadeIn(chart, shift=UP * .18), FadeIn(center_line),
                  FadeIn(question), run_time=1.15)
        self.to(7)

        # 7–13: mode.
        self.copy("가장 많이 모인 곳", "가장 높은 막대의 위치 = 최빈값")
        self.play(*[bar.animate.set_opacity(.19) for x, bar in chart.bars.items()
                   if x != 0], run_time=.65)
        mode_dot = Dot([0, .74, 0], radius=.14, color=ACCENT)
        mode_label = txt("Mode = 0", 38, ACCENT).move_to([0, 2.25, 0])
        self.play(FadeOut(question), FadeIn(mode_dot, scale=.6),
                  FadeIn(mode_label), run_time=.65)
        self.stage = VGroup(chart, center_line, mode_dot, mode_label)
        self.to(13)

        # 13–20: the median crosses 50% of cumulative mass. The center atom
        # means it is not literally 50% strictly to either side.
        self.copy("확률의 절반이 지나는 곳", "누적 확률이 50%를 넘는 위치 = 중앙값")
        self.clear_stage()
        chart = self.chart(BASE, lambda x: x * .67, -1.7)
        divider = DashedLine([0, -1.72, 0], [0, 1.15, 0],
                             color=SPARSE, dash_length=.12)
        left = txt("P(X < 0) = 40%", 25, MUTED).move_to([-2.05, 2.35, 0])
        right = txt("P(X ≤ 0) = 60%", 25, MUTED).move_to([2.05, 2.35, 0])
        median_label = txt("Median = 0", 36, SPARSE).move_to([0, -3.35, 0])
        self.show(VGroup(chart, divider, left, right, median_label),
                  FadeIn(chart), Create(divider), FadeIn(left), FadeIn(right),
                  FadeIn(median_label), run_time=1.05)
        self.to(20)

        # 20–28: a balance point and the discrete expectation formula.
        self.copy("질량이 균형을 이루는 곳", "값 × 그 값의 확률을 모두 더합니다")
        self.clear_stage()
        beam = Line([-3.15, -.45, 0], [3.15, -.45, 0],
                    color=MUTED, stroke_width=5)
        support = Triangle(stroke_color=ACCENT, fill_color=ACCENT,
                           fill_opacity=.25).scale(.32).rotate(PI)
        support.move_to([0, -.83, 0])
        masses = VGroup(*[
            Dot([x * .67, -.13, 0], radius=.1 + .55 * p, color=WEIGHT)
            for x, p in BASE.items()
        ])
        formula = txt("μ = E[X] = Σₓ x P(X = x)", 34, ACCENT)
        formula.move_to([0, 2.15, 0])
        equal = txt("왼쪽 질량의 모멘트 = 오른쪽 질량의 모멘트", 24, MUTED)
        equal.move_to([0, -2.05, 0])
        self.show(VGroup(beam, support, masses, formula, equal),
                  Create(beam), FadeIn(support),
                  LaggedStart(*[FadeIn(m) for m in masses], lag_ratio=.07),
                  FadeIn(formula), FadeIn(equal), run_time=1.3)
        self.play(Indicate(support, color=ACCENT, scale_factor=1.2), run_time=.8)
        self.to(28)

        # 28–33: all three coincide for the symmetric example.
        self.copy("대칭이면 세 중심이 겹칩니다", "이 분포에서는 모두 0입니다")
        self.clear_stage()
        chart = self.chart(BASE, lambda x: x * .67, -1.65)
        common = DashedLine([0, -1.65, 0], [0, 1.22, 0],
                            color=ACCENT, dash_length=.11)
        legend = VGroup(
            txt("Mode  0", 27, ACCENT),
            txt("Median  0", 27, SPARSE),
            txt("Mean  0", 27, GOOD),
        ).arrange(RIGHT, buff=.42).move_to([0, 2.7, 0])
        self.show(VGroup(chart, common, legend), FadeIn(chart),
                  Create(common), FadeIn(legend), run_time=1)
        self.to(33)

        # 33–39: add one distant, small probability mass; normalize old mass.
        self.copy("오른쪽 멀리 작은 질량을 추가", "기존 확률 × 0.92, 새로운 위치 8에 0.08")
        self.clear_stage()
        mapper = lambda x: -1.12 + x * .52
        chart = self.chart(WITH_OUTLIER, mapper, -1.65, labels=(-4, 0, 4, 8))
        old_bars = VGroup(*[chart.bars[x] for x in range(-4, 5)])
        outlier = chart.bars[8]
        tag = txt("8 : 8%", 29, ACCENT).move_to([mapper(8), .3, 0])
        self.play(FadeIn(chart[0]), FadeIn(old_bars), run_time=.75)
        self.play(FadeIn(outlier, shift=UP * .3), FadeIn(tag), run_time=.8)
        self.stage = VGroup(chart, tag)
        self.to(39)

        # 39–46: mode and median stay at zero; mean shifts by .08 × 8.
        self.copy("멀리 있는 값이 평균을 당깁니다", "Mode = 0   Median = 0   Mean = 0.64")
        self.play(FadeOut(tag), run_time=.25)
        zero = mapper(0)
        mean = mapper(.64)
        fixed = DashedLine([zero, -1.65, 0], [zero, 1.35, 0],
                           color=SPARSE, dash_length=.11)
        mean_line = DashedLine([zero, -1.65, 0], [zero, 1.35, 0],
                               color=GOOD, dash_length=.11)
        lever = Line([zero, -2.45, 0], [mapper(8), -2.45, 0],
                     color=ACCENT, stroke_width=3)
        formula = txt("Mean: 0 → 0.64  =  0.08 × 8", 31, GOOD)
        formula.move_to([0, 2.7, 0])
        self.play(Create(fixed), Create(mean_line), Create(lever),
                  FadeIn(formula), run_time=.9)
        self.play(mean_line.animate.shift(RIGHT * (mean - zero)),
                  run_time=1.1)
        self.stage = VGroup(chart, fixed, mean_line, lever, formula)
        self.to(46)

        # 46–54: an explicitly different skewed example separates all three.
        self.copy("모양을 더 바꾸면 세 중심이 갈라집니다", "높은 곳 0 · 절반 지점 1 · 균형점 1.67")
        self.clear_stage()
        chart = self.chart(SKEWED, mapper, -1.8, labels=(-4, 0, 1, 4, 8))
        markers = VGroup(*[
            DashedLine([mapper(x), -1.8, 0], [mapper(x), 1.0, 0],
                       color=color, dash_length=.1)
            for x, color in ((0, ACCENT), (1, SPARSE), (1.67, GOOD))
        ])
        legend = VGroup(
            txt("Mode = 0", 24, ACCENT),
            txt("Median = 1", 24, SPARSE),
            txt("Mean = 1.67", 24, GOOD),
        ).arrange(RIGHT, buff=.32).move_to([0, 2.65, 0])
        self.show(VGroup(chart, markers, legend), FadeIn(chart),
                  LaggedStart(*[Create(m) for m in markers], lag_ratio=.22),
                  FadeIn(legend), run_time=1.3)
        self.to(54)

        # 54–61: replace the vague 'middle' with a balance interpretation.
        self.copy("평균은 균형점", "멀리 있는 값은 거리만큼 더 큰 영향을 줍니다")
        self.clear_stage()
        vague = txt("Mean = 가운데", 38, MUTED).move_to([0, 1.8, 0])
        strike = Line(vague.get_left() + LEFT * .1, vague.get_right() + RIGHT * .1,
                      color=MUTED, stroke_width=3)
        precise = txt("Mean = 확률질량의 균형점", 35, ACCENT)
        precise.move_to([0, -.1, 0])
        box = SurroundingRectangle(precise, color=ACCENT, buff=.32,
                                   corner_radius=.15)
        formula = txt("μ = Σₓ x P(X = x)", 29, GOOD).move_to([0, -2.15, 0])
        self.show(VGroup(vague, strike, precise, box, formula),
                  FadeIn(vague), Create(strike), FadeIn(precise),
                  Create(box), FadeIn(formula), run_time=1.2)
        self.to(61)

        # 61–70: same mean, visibly different spread.
        self.copy("중심은 같아도 퍼짐은 다릅니다", "다음 질문: 분포는 얼마나 퍼져 있을까?")
        self.clear_stage()
        narrow = {-1: .15, 0: .70, 1: .15}
        wide = {-3: .25, -2: .15, 0: .20, 2: .15, 3: .25}
        top = self.chart(narrow, lambda x: x * .75, 1.0, labels=(-3, 0, 3),
                         height_scale=2.1)
        bottom = self.chart(wide, lambda x: x * .75, -2.35,
                            labels=(-3, 0, 3), height_scale=5.8)
        a = txt("A  좁게", 26, WEIGHT).move_to([-3.15, 2.55, 0])
        b = txt("B  넓게", 26, SPARSE).move_to([-3.15, -.8, 0])
        mean_line = DashedLine([0, -2.45, 0], [0, 3.12, 0],
                               color=ACCENT, dash_length=.13)
        same = txt("μA = μB = 0", 30, ACCENT).move_to([0, -3.65, 0])
        final = txt("분포는 얼마나 퍼져 있을까?", 33, INK)
        final.move_to([0, -4.55, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.26,
                                     corner_radius=.13)
        self.show(VGroup(top, bottom, a, b, mean_line, same, final, frame),
                  FadeIn(top), FadeIn(bottom), FadeIn(a), FadeIn(b),
                  Create(mean_line), FadeIn(same), run_time=1.1)
        self.play(FadeIn(final), Create(frame), run_time=.7)
        self.to(70)

    def chart(self, probabilities, mapper, y, labels=None, height_scale=11):
        axis = Arrow([-3.55, y, 0], [3.55, y, 0], buff=0,
                     color=MUTED, stroke_width=2.8,
                     max_tip_length_to_length_ratio=.035)
        if labels is None:
            labels = (-4, -2, 0, 2, 4)
        ticks = VGroup(*[
            Line([mapper(x), y - .11, 0], [mapper(x), y + .11, 0],
                 color=MUTED)
            for x in labels
        ])
        numbers = VGroup(*[
            txt(str(x), 24, INK).move_to([mapper(x), y - .4, 0])
            for x in labels
        ])
        bars = {}
        bar_group = VGroup()
        for x, p in probabilities.items():
            h = p * height_scale
            bar = RoundedRectangle(width=.43, height=h, corner_radius=.045,
                                   stroke_color=WEIGHT if x != 8 else ACCENT,
                                   stroke_width=1.1,
                                   fill_color=WEIGHT if x != 8 else ACCENT,
                                   fill_opacity=.55)
            bar.move_to([mapper(x), y + h / 2, 0])
            bars[x] = bar
            bar_group.add(bar)
        chart = VGroup(VGroup(axis, ticks, numbers), bar_group)
        chart.bars = bars
        return chart

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.16)
        self.head = txt(heading, 33, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 27, INK).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.28)

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
