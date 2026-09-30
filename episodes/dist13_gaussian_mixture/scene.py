"""Distribution mathematics 13: discover a Gaussian mixture from two clusters."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


MU1 = np.array([-2.0, 1.0])
MU2 = np.array([2.0, -1.0])
SIGMA = np.array([[.36, -.11], [-.11, .22]])
PI1, PI2 = .4, .6
GLOBAL_MU = PI1 * MU1 + PI2 * MU2
GLOBAL_SIGMA = SIGMA + PI1 * PI2 * np.outer(MU1 - MU2, MU1 - MU2)
SCALE = .78


def sample_cloud():
    rng = np.random.default_rng(13)
    root = np.linalg.cholesky(SIGMA)
    a = rng.normal(size=(24, 2)) @ root.T + MU1
    b = rng.normal(size=(36, 2)) @ root.T + MU2
    return a, b


LEFT_POINTS, RIGHT_POINTS = sample_cloud()


class GaussianMixtureDiscovery(Scene):
    DURATION = 43

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("PART IV  /  DISTRIBUTION MATHEMATICS 13", 18, MUTED).move_to(UP * 7.3),
            txt("Gaussian Mixture Model | 하나로 부족하다면?", 27, INK, 7.7).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–2.7: start with the surprising data shape, not the model definition.
        self.copy("데이터가 두 덩어리라면?", "멀리 떨어진 두 군집")
        axes = self.axes()
        left, right = self.clouds()
        self.show(VGroup(axes, left, right), FadeIn(axes), FadeIn(left),
                  FadeIn(right), run_time=.85)
        self.to(2.7)

        # 2.7–6.1: one Gaussian must spread across the mostly empty middle.
        self.copy("하나로 설명해보면", "Single Gaussian")
        single = self.contour(GLOBAL_MU, GLOBAL_SIGMA, ACCENT, radius=1.8)
        self.play(Create(single), run_time=.7)
        self.stage.add(single)
        self.to(6.1)

        # 6.1–8.9: visibly mark the mismatch in the data gap.
        self.copy("가운데 빈 곳까지 채웁니다", "데이터는 적은데, 모델은 하나의 덩어리")
        gap = Circle(radius=.58, color=PRUNE, stroke_width=3,
                     fill_color=PRUNE, fill_opacity=.10).move_to(self.pos(GLOBAL_MU))
        marker = txt("데이터가 드문 곳", 25, PRUNE).move_to([0, -2.65, 0])
        self.play(FadeIn(gap), FadeIn(marker), run_time=.6)
        self.stage.add(gap, marker)
        self.to(8.9)

        # 8.9–12.1: allow each cluster to have its own simple explanation.
        self.copy("각 덩어리를 따로 설명하면", "Gaussian 1    +    Gaussian 2")
        self.play(FadeOut(single), FadeOut(gap), FadeOut(marker), run_time=.3)
        c1 = self.contour(MU1, SIGMA, GOOD, radius=1.9)
        c2 = self.contour(MU2, SIGMA, WEIGHT, radius=1.9)
        labels = VGroup(txt("p₁(x)", 28, GOOD).move_to([-2.65, 2.75, 0]),
                        txt("p₂(x)", 28, WEIGHT).move_to([2.65, -2.75, 0]))
        self.play(Create(c1), Create(c2), FadeIn(labels), run_time=.85)
        self.stage = VGroup(axes, left, right, c1, c2, labels)
        self.to(12.1)

        # 12.1–16.1: probability densities cannot simply be added.
        self.copy("그냥 더하면?", "∫p₁=1,  ∫p₂=1")
        self.clear_stage()
        cards = self.mass_cards("1", "1", "전체 확률 = 2", PRUNE)
        self.show(cards, FadeIn(cards), run_time=.8)
        self.to(16.1)

        # 16.1–19.8: mixture weights restore a normalized probability density.
        self.copy("사용 비율을 정합니다", "π₁=0.4,  π₂=0.6")
        weighted = self.mass_cards("0.4", "0.6", "0.4 + 0.6 = 1", GOOD)
        self.play(Transform(cards, weighted), run_time=.7)
        self.to(19.8)

        # 19.8–23.0: two weighted components form one two-peaked density.
        self.copy("두 분포가 하나가 됩니다", "p(x) = 0.4p₁(x) + 0.6p₂(x)")
        self.clear_stage()
        profile = self.density_profile()
        self.show(profile, FadeIn(profile), run_time=.9)
        self.to(23)

        # 23.0–25.8: name and generalize the construction.
        self.copy("Gaussian Mixture Model", "단순한 분포 여러 개로 복잡한 분포를")
        self.clear_stage()
        formula = txt("p(x) = Σₖ πₖ N(x | μₖ, Σₖ)", 38, ACCENT, 7.35)
        formula.move_to([0, 1.5, 0])
        condition = txt("πₖ ≥ 0     /     Σₖ πₖ = 1", 31, GOOD).move_to([0, .25, 0])
        name = txt("Gaussian Mixture Model  /  GMM", 30, INK, 7.3)
        name.move_to([0, -1.55, 0])
        line = Line([-2.9, -2.2, 0], [2.9, -2.2, 0], color=MUTED)
        idea = txt("단순한 여러 개 → 하나의 복잡한 현상", 28, INK, 7.3)
        idea.move_to([0, -3.15, 0])
        self.show(VGroup(formula, condition, name, line, idea),
                  FadeIn(formula), FadeIn(condition), FadeIn(name),
                  Create(line), FadeIn(idea), run_time=.9)
        self.to(25.8)

        # 25.8–29.0: compare the false central peak with the mixture's valley.
        self.copy("중요한 것은 모양의 차이", "하나의 넓은 봉우리  vs  두 개의 봉우리")
        self.clear_stage()
        compare = VGroup(self.small_profile(-2.0, False),
                         self.small_profile(2.0, True))
        self.show(compare, FadeIn(compare), run_time=.9)
        self.to(29)

        # 29.0–32.1: separate centers and covariance structures are possible.
        self.copy("영역마다 설명이 달라집니다", "각각의 중심 · 방향 · 크기 · 비율")
        self.clear_stage()
        left, right = self.clouds()
        axes = self.axes()
        c1 = self.contour(MU1, SIGMA, GOOD, radius=1.9)
        c2 = self.contour(MU2, SIGMA, WEIGHT, radius=1.9)
        badges = VGroup(txt("μ₁, Σ₁, π₁", 26, GOOD).move_to([-2.65, 2.85, 0]),
                        txt("μ₂, Σ₂, π₂", 26, WEIGHT).move_to([2.65, -2.85, 0]))
        self.show(VGroup(axes, left, right, c1, c2, badges),
                  FadeIn(axes), FadeIn(left), FadeIn(right),
                  Create(c1), Create(c2), FadeIn(badges), run_time=.9)
        self.to(32.1)

        # 32.1–35.9: an observation is ambiguous where the components overlap.
        self.copy("그렇다면 이 점은?", "두 Gaussian 중 어디에서 왔을까?")
        x = self.pos([0, 0])
        dot = Dot(x, radius=.13, color=ACCENT)
        rays = VGroup(DashedLine(x, self.pos(MU1), color=GOOD),
                      DashedLine(x, self.pos(MU2), color=WEIGHT))
        self.play(Create(rays), FadeIn(dot), run_time=.65)
        self.stage.add(rays, dot)
        self.to(35.9)

        # 35.9–38.1: replace a forced class label with a probability question.
        self.copy("꼭 하나만 골라야 할까?", "Hard assignment  →  soft assignment")
        hard = txt("x → 1  또는  x → 2", 31, PRUNE).move_to([0, -3.45, 0])
        soft = txt("P(z=1 | x)      P(z=2 | x)", 30, GOOD, 7.25)
        soft.move_to([0, -3.45, 0])
        self.play(FadeIn(hard), run_time=.3)
        self.play(Transform(hard, soft), run_time=.48)
        self.stage.add(hard)
        self.to(38.1)

        # 38.1–43.0: leave the responsibility computation to the next episode.
        self.copy("다음 질문: Responsibility", "한 점은 어느 Gaussian에 속할까?")
        end = txt("한 점의 소속을 확률로 표현할 수 있을까?", 30, INK, 7.2)
        end.move_to([0, -4.35, 0])
        frame = SurroundingRectangle(end, color=ACCENT, buff=.2, corner_radius=.12)
        self.play(FadeIn(end), Create(frame), run_time=.6)
        self.stage.add(end, frame)
        self.to(43)

    def pos(self, value):
        return np.array([SCALE * value[0], SCALE * value[1], 0])

    def axes(self):
        return VGroup(
            Arrow([-3.65, 0, 0], [3.65, 0, 0], buff=0,
                  color=MUTED, stroke_width=2),
            Arrow([0, -3.25, 0], [0, 3.25, 0], buff=0,
                  color=MUTED, stroke_width=2),
        )

    def clouds(self):
        left = VGroup(*[Dot(self.pos(p), radius=.062, color=GOOD)
                        for p in LEFT_POINTS])
        right = VGroup(*[Dot(self.pos(p), radius=.062, color=WEIGHT)
                         for p in RIGHT_POINTS])
        return left, right

    def contour(self, mean, covariance, color, radius=2):
        values, vectors = np.linalg.eigh(covariance)
        angle = np.arctan2(vectors[1, 1], vectors[0, 1])
        return Ellipse(width=2 * SCALE * radius * np.sqrt(values[1]),
                       height=2 * SCALE * radius * np.sqrt(values[0]),
                       color=color, stroke_width=2.6,
                       fill_color=color, fill_opacity=.045).rotate(angle).shift(self.pos(mean))

    def mass_cards(self, a, b, total, total_color):
        boxes = VGroup()
        for x, number, color in ((-1.9, a, GOOD), (1.9, b, WEIGHT)):
            box = RoundedRectangle(width=2.65, height=2.2, corner_radius=.16,
                                   stroke_color=color, stroke_width=2,
                                   fill_color=color, fill_opacity=.06).move_to([x, .8, 0])
            val = txt(number, 48, color).move_to([x, 1.1, 0])
            label = txt("확률질량", 26, INK).move_to([x, .2, 0])
            boxes.add(box, val, label)
        plus = txt("+", 44, INK).move_to([0, .8, 0])
        result = txt(total, 36, total_color).move_to([0, -2.2, 0])
        return VGroup(boxes, plus, result)

    def density_profile(self):
        baseline = Line([-3.5, -1.8, 0], [3.5, -1.8, 0], color=MUTED)
        left = self.profile_curve(-2.1, 2.5, GOOD, .4)
        right = self.profile_curve(2.1, 2.5, WEIGHT, .6)
        mixture = self.profile_curve(0, 2.5, ACCENT, 1, mixture=True)
        labels = VGroup(txt("0.4p₁", 26, GOOD).move_to([-2.35, 2.0, 0]),
                        txt("0.6p₂", 26, WEIGHT).move_to([2.35, 3.15, 0]),
                        txt("p = 0.4p₁ + 0.6p₂", 30, ACCENT).move_to([0, -3.1, 0]))
        return VGroup(baseline, left, right, mixture, labels)

    def profile_curve(self, center, height, color, weight, mixture=False, xshift=0):
        def y(t):
            a = .4 * np.exp(-.5 * ((t + 2.1) / .58) ** 2)
            b = .6 * np.exp(-.5 * ((t - 2.1) / .58) ** 2)
            if mixture:
                return a + b
            return weight * np.exp(-.5 * ((t - center) / .58) ** 2)
        return ParametricFunction(lambda t: np.array([t + xshift,
                                    -1.8 + height * y(t) / .6, 0]),
                                  t_range=[-3.5, 3.5, .035],
                                  color=color, stroke_width=4 if mixture else 2.3,
                                  stroke_opacity=1 if mixture else .75)

    def small_profile(self, x, mixture):
        baseline = Line([x-1.55, -1.5, 0], [x+1.55, -1.5, 0], color=MUTED)
        if mixture:
            curve = ParametricFunction(lambda t: np.array([
                x+t, -1.5+2.5*(.4*np.exp(-.5*((t+.85)/.31)**2)
                                +.6*np.exp(-.5*((t-.85)/.31)**2)), 0]),
                t_range=[-1.55, 1.55, .025], color=GOOD, stroke_width=3.4)
            name = "Gaussian Mixture"
        else:
            curve = ParametricFunction(lambda t: np.array([
                x+t, -1.5+1.5*np.exp(-.5*(t/.88)**2), 0]),
                t_range=[-1.55, 1.55, .025], color=PRUNE, stroke_width=3.4)
            name = "Single Gaussian"
        label = txt(name, 25, INK, 3.35).move_to([x, -2.3, 0])
        return VGroup(baseline, curve, label)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.14)
        self.head = txt(heading, 30, INK, 7.25).move_to([0, 4.95, 0])
        self.caption = txt(caption, 26, INK, 7.25).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.24)

    def show(self, stage, *animations, run_time=.9):
        self.stage = stage
        self.play(*animations, run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.26)
        self.stage = VGroup()

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.28, remain))
            tail = target - self.time
            if tail > .001:
                self.wait(tail)
