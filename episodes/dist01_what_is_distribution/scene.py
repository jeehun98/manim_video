"""Distribution mathematics 01: probability mass over possible values."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, BG, GOOD, INK, MUTED, SPARSE, WEIGHT, txt


class WhatIsDistribution(Scene):
    DURATION = 72
    VALUES = (1, 1, 2, 2, 2, 4)
    XS = {1: -2.7, 2: -.9, 3: .9, 4: 2.7}

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  01", 19, MUTED).move_to(UP * 7.3),
            txt("분포는 무엇을 나타내는가?", 33).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–6: individual observations.
        self.copy("여섯 개의 숫자", "하나씩 보면 각각의 값입니다")
        row = VGroup(*[txt(str(v), 54, WEIGHT) for v in self.VALUES])
        row.arrange(RIGHT, buff=.55).move_to([0, .2, 0])
        self.show(row, FadeIn(row, shift=UP * .2))
        self.to(6)

        # 6–14: place every observation at its value.
        self.copy("값의 공간에 놓으면", "같은 값은 같은 위치에 쌓입니다")
        axis = self.axis(-1.8)
        dots = self.dot_stacks(-1.8)
        self.play(Create(axis), run_time=.7)
        self.play(*[ReplacementTransform(row[i], dots[i]) for i in range(6)],
                  run_time=1.5)
        self.stage = VGroup(axis, dots)
        self.to(14)

        # 14–22: reorder data without touching the dot stack.
        self.copy("순서는 달라도", "아래의 모양은 그대로입니다")
        original = txt("[1, 1, 2, 2, 2, 4]", 38, INK).move_to([0, 2.55, 0])
        shuffled = txt("[2, 4, 1, 2, 1, 2]", 38, INK).move_to(original)
        self.play(FadeIn(original), run_time=.5)
        self.play(Transform(original, shuffled), run_time=.9)
        self.play(Indicate(dots, color=GOOD, scale_factor=1.04), run_time=.9)
        self.stage.add(original)
        self.to(22)

        # 22–34: counts become empirical probabilities.
        self.copy("개수에서 확률로", "관측된 비중 = 개수 / 전체 개수")
        bars = self.bars((2, 3, 0, 1), -1.8, scale=.86)
        counts = VGroup(*[
            txt(s, 32, ACCENT).move_to([self.XS[v], -1.5 + h * .86, 0])
            for v, h, s in ((1, 2, "2"), (2, 3, "3"), (4, 1, "1"))
        ])
        self.play(FadeOut(original), FadeOut(dots), FadeIn(bars), run_time=.8)
        self.play(FadeIn(counts), run_time=.45)
        total = txt("전체 개수 = 6", 31, MUTED).move_to([0, 3.05, 0])
        self.play(FadeIn(total), run_time=.5)
        fractions = VGroup(*[
            txt(s, 29, ACCENT).move_to(counts[i])
            for i, s in enumerate(("2/6", "3/6", "1/6"))
        ])
        self.play(Transform(counts, fractions), run_time=.7)
        decimals = VGroup(*[
            txt(s, 27, GOOD).move_to(counts[i])
            for i, s in enumerate(("0.33", "0.50", "0.17"))
        ])
        self.play(Transform(counts, decimals), run_time=.7)
        empirical = txt("관측값으로 만든 경험적 분포", 23, MUTED).move_to([0, -3.45, 0])
        self.play(FadeIn(empirical), run_time=.4)
        self.stage = VGroup(axis, bars, counts, total, empirical)
        self.to(34)

        # 34–44: one unit of mass split among the possible values.
        self.copy("전체 확률 = 1", "가능한 값들에 확률을 나누어 놓습니다")
        self.clear_stage()
        whole = RoundedRectangle(width=4.2, height=.75, corner_radius=.16,
                                 stroke_color=ACCENT, fill_color=ACCENT,
                                 fill_opacity=.32).move_to([0, 2.65, 0])
        whole_label = txt("1", 34, INK).move_to(whole)
        self.play(FadeIn(whole), FadeIn(whole_label), run_time=.65)
        pieces = VGroup(*[
            Rectangle(width=w, height=.72, stroke_width=1.5, stroke_color=c,
                      fill_color=c, fill_opacity=.48)
            for w, c in ((1.4, WEIGHT), (2.1, SPARSE), (.7, GOOD))
        ])
        pieces.arrange(RIGHT, buff=0).move_to(whole)
        self.play(FadeOut(whole_label), ReplacementTransform(whole, pieces), run_time=.8)
        destinations = [self.XS[v] for v in (1, 2, 4)]
        self.play(*[pieces[i].animate.move_to([destinations[i], .4, 0])
                    for i in range(3)], run_time=1.15)
        mass_labels = VGroup(*[
            txt(s, 31, INK).move_to([destinations[i], -.45, 0])
            for i, s in enumerate(("2/6", "3/6", "1/6"))
        ])
        self.play(FadeIn(mass_labels), run_time=.45)
        equation = txt("Σₓ P(X = x) = 1", 36, ACCENT).move_to([0, -2.35, 0])
        self.play(FadeIn(equation, shift=UP * .12), run_time=.55)
        self.stage = VGroup(pieces, mass_labels, equation)
        self.to(44)

        # 44–53: distributions can have different shapes.
        self.copy("이것이 분포", "확률이 어디에, 얼마나 놓여 있는가")
        self.clear_stage()
        label = txt("Distribution", 46, ACCENT).move_to([0, 2.8, 0])
        axis = self.axis(-2.25)
        bars = self.bars((2, 3, 0, 1), -2.25, scale=.85)
        self.play(FadeIn(label), Create(axis), FadeIn(bars), run_time=.8)
        for shape in ((4, 2, 1, .3), (3, .6, .6, 3), (1.6, 1.8, 1.5, 1.4)):
            new_bars = self.bars(shape, -2.25, scale=.85)
            self.play(Transform(bars, new_bars), run_time=1.1)
        self.stage = VGroup(label, axis, bars)
        self.to(53)

        # 53–62: samples from a hypothetical generating distribution.
        self.copy("분포에서 데이터로", "관측값은 분포에서 얻은 결과로 볼 수 있습니다")
        self.clear_stage()
        source = txt("Distribution", 41, ACCENT).move_to([0, 2.8, 0])
        arrow = Arrow([0, 2.12, 0], [0, .85, 0], color=MUTED, buff=0)
        data = VGroup(*[txt(s, 35, WEIGHT) for s in ("x₁", "x₂", "x₃", "x₄", "…")])
        data.arrange(RIGHT, buff=.45).move_to([0, -.05, 0])
        caveat = txt("6개 관측값만으로 원래 분포를 확정할 수는 없습니다", 23, MUTED)
        caveat.move_to([0, -2.25, 0])
        self.play(FadeIn(source), GrowArrow(arrow), run_time=.7)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .55) for d in data],
                              lag_ratio=.22), run_time=1.5)
        self.play(FadeIn(caveat), run_time=.45)
        self.stage = VGroup(source, arrow, data, caveat)
        self.to(62)

        # 62–72: three different shapes and the next question.
        self.copy("분포를 숫자 하나로 요약한다면?", "서로 다른 모양의 중심은 어디일까요?")
        self.clear_stage()
        graphs = VGroup(*[
            self.mini_distribution(i, weights)
            for i, weights in enumerate(((.05, .4, 1, .4, .05),
                                         (1, .55, .25, .1, .05),
                                         (.1, 1, .18, 1, .1)))
        ])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * .15) for g in graphs],
                              lag_ratio=.22), run_time=1.4)
        questions = VGroup(*[
            txt("?", 48, ACCENT).move_to([x, 1.45, 0])
            for x in (-2.55, 0, 2.55)
        ])
        self.play(FadeIn(questions), run_time=.6)
        final = txt("분포의 중심은 어디일까?", 38, INK).move_to([0, -3.05, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.35, corner_radius=.16)
        self.play(FadeIn(final), Create(frame), run_time=.8)
        self.stage = VGroup(graphs, questions, final, frame)
        self.to(72)

    def axis(self, y):
        line = Arrow([-3.65, y, 0], [3.75, y, 0], buff=0, color=MUTED,
                     stroke_width=3, max_tip_length_to_length_ratio=.035)
        ticks = VGroup(*[
            Line([x, y - .12, 0], [x, y + .12, 0], color=MUTED)
            for x in self.XS.values()
        ])
        labels = VGroup(*[
            txt(str(v), 29, INK).move_to([x, y - .48, 0])
            for v, x in self.XS.items()
        ])
        return VGroup(line, ticks, labels)

    def dot_stacks(self, y):
        seen = {1: 0, 2: 0, 3: 0, 4: 0}
        result = VGroup()
        for value in self.VALUES:
            j = seen[value]
            seen[value] += 1
            result.add(Dot([self.XS[value], y + .43 + j * .46, 0],
                           radius=.16, color=WEIGHT))
        return result

    def bars(self, heights, y, scale):
        result = VGroup()
        for value, height in enumerate(heights, 1):
            if height <= 0:
                result.add(Rectangle(width=.82, height=.001, stroke_opacity=0,
                                     fill_opacity=0).move_to([self.XS[value], y, 0]))
                continue
            h = height * scale
            result.add(RoundedRectangle(width=.82, height=h, corner_radius=.08,
                        stroke_color=WEIGHT if value != 2 else SPARSE,
                        fill_color=WEIGHT if value != 2 else SPARSE,
                        fill_opacity=.53).move_to([self.XS[value], y + h / 2, 0]))
        return result

    def mini_distribution(self, index, weights):
        center = -2.55 + index * 2.55
        baseline = -.85
        xs = np.linspace(center - 1.05, center + 1.05, len(weights))
        curve = VMobject(stroke_color=WEIGHT if index != 2 else SPARSE,
                         stroke_width=4)
        curve.set_points_smoothly([
            np.array([x, baseline + 2.1 * h, 0])
            for x, h in zip(xs, weights)
        ])
        axis = Line([center - 1.08, baseline, 0],
                    [center + 1.08, baseline, 0], color=MUTED)
        return VGroup(axis, curve)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.18)
        self.head = txt(heading, 34, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 27, INK).move_to([0, -5.75, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.3)

    def show(self, stage, animation):
        self.stage = stage
        self.play(animation, run_time=.85)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.35)
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
