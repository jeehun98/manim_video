"""Distribution mathematics 04: two moments cannot determine a distribution."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


PEAK = {-2: .125, 0: .75, 2: .125}
SPLIT = {-1: .5, 1: .5}


class SameMomentsDifferentDistributions(Scene):
    DURATION = 43

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  04", 19, MUTED).move_to(UP * 7.3),
            txt("같은 평균과 분산이면 같은 분포일까?", 31).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: continue from episode 03's central-peak distribution.
        self.copy("분포 A", "μ = 0     σ² = 1")
        chart_a = self.chart(PEAK, -1.5, WEIGHT, height_scale=3.1)
        mean_line = DashedLine([0, -1.5, 0], [0, 1.22, 0],
                               color=ACCENT, dash_length=.12)
        stats = VGroup(
            self.stat_card("μ = 0", ACCENT),
            self.stat_card("σ² = 1", GOOD),
        ).arrange(RIGHT, buff=.4).move_to([0, 2.6, 0])
        self.show(VGroup(chart_a, mean_line, stats), FadeIn(chart_a),
                  Create(mean_line), FadeIn(stats), run_time=1.15)
        self.to(4)

        # 4–8.5: hide the shape, leaving only its two-number summary.
        self.copy("두 숫자만 남긴다면", "이 요약만으로 원래 모양을 복원할 수 있을까요?")
        self.play(FadeOut(chart_a), FadeOut(mean_line), run_time=.55)
        empty_axis = self.empty_axis(-1.5)
        question = txt("?", 56, MUTED).move_to([0, .15, 0])
        self.play(Create(empty_axis), FadeIn(question), run_time=.65)
        self.stage = VGroup(stats, empty_axis, question)
        self.to(8.5)

        # 8.5–12.5: another compatible, visibly different distribution.
        self.copy("다른 모양의 분포 B", "중앙은 비고 질량이 양쪽에 있습니다")
        chart_b = self.chart(SPLIT, -1.5, SPARSE, height_scale=3.1)
        self.play(FadeOut(question), FadeOut(empty_axis), FadeIn(chart_b),
                  run_time=.9)
        self.stage = VGroup(stats, chart_b)
        self.to(12.5)

        # 12.5–16.5: confirm that both probability balances are at zero.
        self.copy("평균은 둘 다 0", "좌우 질량이 같은 거리에서 균형을 이룹니다")
        self.clear_stage()
        top = self.chart(PEAK, 1.0, WEIGHT, height_scale=2.0)
        bottom = self.chart(SPLIT, -2.3, SPARSE, height_scale=2.8)
        line = DashedLine([0, -2.35, 0], [0, 3.0, 0],
                          color=ACCENT, dash_length=.13)
        labels = VGroup(
            txt("A", 30, WEIGHT).move_to([-3.1, 2.45, 0]),
            txt("B", 30, SPARSE).move_to([-3.1, -.9, 0]),
            txt("μA = μB = 0", 30, ACCENT).move_to([0, -3.5, 0]),
        )
        self.show(VGroup(top, bottom, line, labels), FadeIn(top),
                  FadeIn(bottom), Create(line), FadeIn(labels), run_time=1.1)
        self.to(16.5)

        # 16.5–20.5: tune B from ±1.5 to ±1, keeping total mass and mean.
        self.copy("퍼짐도 같게 맞출 수 있습니다", "B:  σ² = 2.25  →  1")
        self.clear_stage()
        start = {-1.5: .5, 1.5: .5}
        chart = self.chart(start, -1.45, SPARSE, height_scale=3.25)
        mean_line = DashedLine([0, -1.45, 0], [0, 1.25, 0],
                               color=ACCENT, dash_length=.13)
        value = txt("σ² = 2.25", 37, SPARSE).move_to([0, 2.25, 0])
        reference = txt("A의 분산 = 1", 27, GOOD).move_to([0, -3.15, 0])
        self.show(VGroup(chart, mean_line, value, reference),
                  FadeIn(chart), Create(mean_line), FadeIn(value),
                  FadeIn(reference), run_time=.95)
        fixed = txt("σ² = 1", 37, GOOD).move_to(value)
        self.play(chart.bars[-1.5].animate.shift(RIGHT * .38),
                  chart.bars[1.5].animate.shift(LEFT * .38),
                  Transform(value, fixed), run_time=1.15)
        self.to(20.5)

        # 20.5–25: same two statistics do not imply equal distributions.
        self.copy("숫자는 같지만 모양은 다릅니다", "μA = μB,   σ²A = σ²B,   PA ≠ PB")
        self.clear_stage()
        top = self.chart(PEAK, 1.0, WEIGHT, height_scale=2.0)
        bottom = self.chart(SPLIT, -2.25, SPARSE, height_scale=2.8)
        shared = txt("μ = 0     σ² = 1", 31, ACCENT).move_to([0, -3.55, 0])
        equality = txt("A = B", 39, INK).move_to([0, 3.0, 0])
        strike = Line(equality.get_left() + LEFT * .1,
                      equality.get_right() + RIGHT * .1,
                      color=PRUNE, stroke_width=4)
        different = txt("P_A ≠ P_B", 33, PRUNE).move_to(equality)
        tags = VGroup(
            txt("A", 29, WEIGHT).move_to([-3.1, 2.4, 0]),
            txt("B", 29, SPARSE).move_to([-3.1, -.8, 0]),
        )
        self.show(VGroup(top, bottom, shared, equality, strike, different, tags),
                  FadeIn(top), FadeIn(bottom), FadeIn(shared),
                  FadeIn(equality), FadeIn(tags), run_time=1.0)
        self.play(Create(strike), run_time=.45)
        self.play(FadeOut(equality), FadeOut(strike), FadeIn(different),
                  run_time=.5)
        self.to(25)

        # 25–28.5: a many-to-one compression into two numbers.
        self.copy("서로 다른 분포 → 같은 두 숫자", "(μ, σ²)는 분포의 압축된 요약입니다")
        self.clear_stage()
        inputs = VGroup(
            self.source_card("Distribution A", "중앙 봉우리", WEIGHT),
            self.source_card("Distribution B", "양쪽 봉우리", SPARSE),
        ).arrange(RIGHT, buff=.42).move_to([0, 1.65, 0])
        arrows = VGroup(*[
            Arrow(card.get_bottom(), [0, -.65, 0], buff=.14,
                  color=MUTED, stroke_width=2.5)
            for card in inputs
        ])
        summary = self.source_card("Summary", "μ = 0,  σ² = 1", ACCENT)
        summary.move_to([0, -1.65, 0])
        two_numbers = txt("두 숫자에 압축", 28, ACCENT).move_to([0, -3.25, 0])
        self.show(VGroup(inputs, arrows, summary, two_numbers),
                  FadeIn(inputs), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  FadeIn(summary), FadeIn(two_numbers), run_time=1.2)
        self.to(28.5)

        # 28.5–33: explicitly name shape information that can be lost.
        self.copy("요약하며 사라지는 정보", "봉우리·꼬리·비대칭성은 두 수치에 담기지 않습니다")
        self.clear_stage()
        details = VGroup(
            self.feature("봉우리 개수", WEIGHT),
            self.feature("꼬리 모양", SPARSE),
            self.feature("비대칭성", GOOD),
        ).arrange(DOWN, buff=.35).move_to([0, 1.45, 0])
        card = self.source_card("Summary", "μ,  σ²", ACCENT)
        card.move_to([0, -2.2, 0])
        self.show(VGroup(details, card), FadeIn(details), FadeIn(card),
                  run_time=.85)
        self.play(*[item.animate.set_opacity(.12) for item in details],
                  Indicate(card, color=ACCENT, scale_factor=1.08),
                  run_time=.9)
        self.to(33)

        # 33–37: statistics are cards extracted from a larger object.
        self.copy("통계량은 분포 자체가 아닙니다", "두 숫자는 중요한 단서입니다")
        self.clear_stage()
        distribution = self.source_card("Distribution", "확률이 놓인 전체 구조", WEIGHT)
        distribution.move_to([0, 2.2, 0])
        arrow = Arrow([0, 1.25, 0], [0, -.3, 0],
                      buff=0, color=MUTED)
        stats = VGroup(
            self.stat_card("μ", ACCENT),
            self.stat_card("σ²", GOOD),
        ).arrange(RIGHT, buff=.55).move_to([0, -1.35, 0])
        summary = txt("Summary  /  두 숫자로 압축", 27, MUTED)
        summary.move_to([0, -2.75, 0])
        self.show(VGroup(distribution, arrow, stats, summary),
                  FadeIn(distribution), GrowArrow(arrow),
                  FadeIn(stats), FadeIn(summary), run_time=1.1)
        self.to(37)

        # 37–43: move from one value x to a pair (x,y) and a diagonal cloud.
        self.copy("하나의 값에서 두 값으로", "다음 질문: 두 변수를 동시에 보면?")
        self.clear_stage()
        one_axis = self.empty_axis(-.65)
        one_label = txt("x", 32, WEIGHT).move_to([2.9, -.2, 0])
        self.play(Create(one_axis), FadeIn(one_label), run_time=.7)
        self.play(FadeOut(one_axis), FadeOut(one_label), run_time=.35)
        x_axis = Arrow([-2.6, -2.15, 0], [3.05, -2.15, 0], buff=0,
                       color=MUTED)
        y_axis = Arrow([-2.6, -2.15, 0], [-2.6, 2.65, 0], buff=0,
                       color=MUTED)
        axis_labels = VGroup(
            txt("x", 28, WEIGHT).move_to([3.2, -2.15, 0]),
            txt("y", 28, SPARSE).move_to([-2.6, 2.85, 0]),
            txt("(x, y)", 31, ACCENT).move_to([1.95, 2.55, 0]),
        )
        points = VGroup(*[
            Dot([x, y, 0], radius=.09, color=WEIGHT)
            for x, y in ((-2.1, -1.55), (-1.75, -1.25), (-1.4, -.95),
                         (-1.1, -.7), (-.8, -.45), (-.35, -.2),
                         (-.15, .35), (.25, .15), (.55, .6),
                         (.95, .8), (1.25, 1.1), (1.65, 1.45),
                         (2.05, 1.7))
        ])
        self.play(Create(x_axis), Create(y_axis), FadeIn(axis_labels),
                  run_time=.7)
        self.play(LaggedStart(*[FadeIn(dot, scale=.5) for dot in points],
                              lag_ratio=.06), run_time=1.0)
        final = txt("두 변수를 동시에 보면 무엇이 달라질까?", 30, INK)
        final.move_to([0, -4.35, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.25,
                                     corner_radius=.13)
        self.play(FadeIn(final), Create(frame), run_time=.65)
        self.stage = VGroup(x_axis, y_axis, axis_labels, points, final, frame)
        self.to(43)

    def chart(self, probabilities, y, color, height_scale=3.0):
        axis = self.empty_axis(y)
        bars = {}
        group = VGroup()
        for x, p in probabilities.items():
            h = p * height_scale
            bar = RoundedRectangle(width=.5, height=h, corner_radius=.055,
                                   stroke_color=color, stroke_width=1.3,
                                   fill_color=color, fill_opacity=.58)
            bar.move_to([x * .76, y + h / 2, 0])
            bars[x] = bar
            group.add(bar)
        chart = VGroup(axis, group)
        chart.bars = bars
        return chart

    def empty_axis(self, y):
        line = Arrow([-3.45, y, 0], [3.45, y, 0], buff=0,
                     color=MUTED, stroke_width=2.8,
                     max_tip_length_to_length_ratio=.035)
        ticks = VGroup(*[
            Line([x * .76, y - .1, 0], [x * .76, y + .1, 0], color=MUTED)
            for x in (-2, -1, 0, 1, 2)
        ])
        labels = VGroup(*[
            txt(str(x), 23, INK).move_to([x * .76, y - .4, 0])
            for x in (-2, 0, 2)
        ])
        return VGroup(line, ticks, labels)

    def stat_card(self, value, color):
        box = RoundedRectangle(width=2.75, height=1.05,
                               corner_radius=.17, stroke_color=color,
                               stroke_width=1.8, fill_color=color,
                               fill_opacity=.08)
        return VGroup(box, txt(value, 32, color))

    def source_card(self, title, detail, color):
        box = RoundedRectangle(width=3.25, height=1.5,
                               corner_radius=.18, stroke_color=color,
                               stroke_width=1.6, fill_color=color,
                               fill_opacity=.08)
        words = VGroup(
            txt(title, 25, color, 3.0).move_to([0, .35, 0]),
            txt(detail, 22, INK, 3.0).move_to([0, -.38, 0]),
        )
        return VGroup(box, words)

    def feature(self, value, color):
        box = RoundedRectangle(width=5.2, height=.75, corner_radius=.14,
                               stroke_color=color, stroke_width=1.3,
                               fill_color=color, fill_opacity=.07)
        return VGroup(box, txt(value, 27, color))

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.15)
        self.head = txt(heading, 31, INK).move_to([0, 4.95, 0])
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
