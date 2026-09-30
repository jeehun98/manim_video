"""Distribution mathematics 11: Gaussian density as a function of Mahalanobis distance."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


SIGMA = np.array([[4., 1.], [1., 1.]])
EIGVALS, EIGVECS = np.linalg.eigh(SIGMA)
MAJOR_ANGLE = np.arctan2(EIGVECS[1, 1], EIGVECS[0, 1])
WHITEN = EIGVECS @ np.diag(1 / np.sqrt(EIGVALS)) @ EIGVECS.T


def sample_points():
    angles = np.linspace(0, TAU, 24, endpoint=False)
    base = np.array([(r * np.cos(t), r * np.sin(t))
                     for r in (.65, 1.3) for t in angles])
    base /= np.sqrt(np.mean(base[:, 0] ** 2))
    return np.column_stack((2 * base[:, 0],
                            .5 * base[:, 0] + np.sqrt(.75) * base[:, 1]))


POINTS = sample_points()


class WhyGaussianEllipse(Scene):
    DURATION = 50

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  11", 19, MUTED).move_to(UP * 7.3),
            txt("Gaussian의 타원은 어디서 오는가?", 31).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: pick up the nested Mahalanobis contours from episode 10.
        self.copy("지난 편의 타원", "dₘ(x,μ) = c  :  같은 거리의 점")
        axes = self.axes()
        inner = self.contour(1, GOOD)
        outer = self.contour(2, ACCENT)
        center = Dot(ORIGIN, radius=.13, color=INK)
        labels = VGroup(
            txt("dₘ=1", 27, GOOD).move_to([1.6, .95, 0]),
            txt("dₘ=2", 27, ACCENT).move_to([3.05, 1.9, 0]),
        )
        self.show(VGroup(axes, inner, outer, center, labels),
                  FadeIn(axes), Create(inner), Create(outer),
                  FadeIn(center), FadeIn(labels), run_time=.9)
        self.to(4)

        # 4–8: same ellipse seen as a Gaussian density level set.
        self.copy("Gaussian에서도 같은 타원", "밀도 표면의 옆모습과 위에서 본 등고선")
        self.clear_stage()
        bell = self.bell(-1.85)
        top = self.contour(1.3, ACCENT).scale(.48).shift(RIGHT * 2.05)
        view_labels = VGroup(
            txt("side view", 24, MUTED).move_to([-1.85, -2.2, 0]),
            txt("top view", 24, MUTED).move_to([2.05, -2.2, 0]),
        )
        self.show(VGroup(bell, top, view_labels), FadeIn(bell),
                  Create(top), FadeIn(view_labels), run_time=.85)
        self.to(8)

        # 8–12: a horizontal density cut corresponds to an ellipse in top view.
        self.copy("같은 높이에서 자르면", "p(x) = c  :  같은 밀도의 점")
        cut = Line([-2.54, .4, 0], [-1.16, .4, 0],
                   color=GOOD, stroke_width=3.4)
        intersections = VGroup(
            Dot([-2.54, .4, 0], radius=.1, color=GOOD),
            Dot([-1.16, .4, 0], radius=.1, color=GOOD),
        )
        top_glow = self.contour(1.3, GOOD).scale(.48).shift(RIGHT * 2.05)
        tag = txt("p(x) = c", 29, GOOD).move_to([2.05, 2.05, 0])
        self.play(Create(cut), FadeIn(intersections), Transform(top, top_glow),
                  FadeIn(tag), run_time=.9)
        self.stage.add(cut, intersections, tag)
        self.to(12)

        # 12–16: show the full 2D formula while focusing on the quadratic term.
        self.copy("왜 하필 타원일까?", "지수 안의 거리 제곱을 보세요")
        self.clear_stage()
        norm = txt("p(x) = 1/(2π√|Σ|) · exp[−½ Q(x)]", 34, INK)
        norm.move_to([0, 1.4, 0])
        quadratic = txt("Q(x) = (x−μ)ᵀ Σ⁻¹ (x−μ)", 37, ACCENT)
        quadratic.move_to([0, -.35, 0])
        box = SurroundingRectangle(quadratic, color=ACCENT, buff=.24,
                                   corner_radius=.12)
        helper = txt("Σ: 퍼짐과 방향", 29, MUTED).move_to([0, -2.2, 0])
        self.show(VGroup(norm, quadratic, box, helper),
                  FadeIn(norm), FadeIn(quadratic), Create(box),
                  FadeIn(helper), run_time=.85)
        self.to(16)

        # 16–20: recognize the squared Mahalanobis distance.
        self.copy("앞에서 본 바로 그 값", "Q(x) = dₘ(x,μ)²")
        self.clear_stage()
        quadratic = txt("(x−μ)ᵀ Σ⁻¹ (x−μ)", 39, ACCENT).move_to([0, 1.15, 0])
        equals = txt("=", 43, MUTED).move_to([0, 0, 0])
        distance = txt("dₘ(x,μ)²", 48, GOOD).move_to([0, -1.25, 0])
        self.show(VGroup(quadratic, equals, distance),
                  FadeIn(quadratic), FadeIn(equals), FadeIn(distance),
                  run_time=.75)
        self.to(20)

        # 20–24: density decays with squared distance.
        self.copy("거리가 커질수록 밀도는 낮아집니다", "p(x) ∝ exp[−dₘ²/2]")
        self.clear_stage()
        formula = txt("p(x) ∝ exp[−½ dₘ(x,μ)²]", 37, ACCENT)
        formula.move_to([0, 2.7, 0])
        bars = VGroup(*[
            self.density_bar(r, np.exp(-.5 * r * r), 1.3 - 1.2 * r)
            for r in range(4)
        ])
        self.show(VGroup(formula, bars), FadeIn(formula),
                  LaggedStart(*[FadeIn(bar) for bar in bars],
                              lag_ratio=.15), run_time=1.1)
        self.to(24)

        # 24–28: any three points on one contour have the same Gaussian density.
        self.copy("같은 거리라면 같은 밀도", "방향이 달라도 dₘ가 같으면 p(x)도 같습니다")
        self.clear_stage()
        axes = self.axes()
        ring = self.contour(1.55, ACCENT)
        angles = (25, 145, 255)
        points = VGroup(*[
            Dot(self.contour_point(1.55, angle), radius=.15,
                color=color)
            for angle, color in zip(angles, (GOOD, PRUNE, SPARSE))
        ])
        names = VGroup(*[
            txt(name, 29, color).move_to(dot.get_center() + offset)
            for dot, name, color, offset in zip(
                points, ("A", "B", "C"), (GOOD, PRUNE, SPARSE),
                (RIGHT * .3 + UP * .25, LEFT * .3 + UP * .25,
                 LEFT * .3 + DOWN * .3))
        ])
        equal = txt("p(A) = p(B) = p(C)", 34, ACCENT)
        equal.move_to([0, -3.35, 0])
        self.show(VGroup(axes, ring, points, names, equal),
                  FadeIn(axes), Create(ring), FadeIn(points),
                  FadeIn(names), FadeIn(equal), run_time=.95)
        self.to(28)

        # 28–32: multiple distance contours are multiple density contours.
        self.copy("등거리선 = 등밀도선", "dₘ=1, 2, 3  ↔  서로 다른 밀도 높이")
        self.clear_stage()
        rings = VGroup(
            self.contour(1, GOOD).scale(.7),
            self.contour(2, ACCENT).scale(.7),
            self.contour(3, SPARSE).scale(.7),
        )
        labels = VGroup(
            txt("dₘ=1", 27, GOOD).move_to([1.45, .75, 0]),
            txt("dₘ=2", 27, ACCENT).move_to([2.7, 1.25, 0]),
            txt("dₘ=3", 27, SPARSE).move_to([3.55, 2.25, 0]),
        )
        center = Dot(ORIGIN, radius=.12, color=INK)
        self.show(VGroup(rings, labels, center),
                  LaggedStart(*[Create(r) for r in rings],
                              lag_ratio=.2), FadeIn(labels),
                  FadeIn(center), run_time=1.05)
        self.to(32)

        # 32–37: covariance changes the contours and thus the density geometry.
        self.copy("Σ가 바뀌면 밀도 모양도 바뀝니다", "원형 → 가로 → 세로 → 기울어진 타원")
        self.clear_stage()
        shape = self.covariance_shape(np.eye(2))
        formula = txt("Σ 변화", 34, ACCENT).move_to([0, -3.0, 0])
        self.show(VGroup(shape, formula), FadeIn(shape),
                  FadeIn(formula), run_time=.65)
        for sigma in (np.diag([3., 1.]), np.diag([1., 3.]), SIGMA):
            self.play(Transform(shape, self.covariance_shape(sigma)),
                      run_time=.65)
        self.to(37)

        # 37–41: the three descriptions of one geometry.
        self.copy("하나의 구조, 세 가지 언어", "공분산 → 거리 → 확률밀도")
        self.clear_stage()
        cards = VGroup(
            self.card("Σ", "Covariance", WEIGHT),
            self.card("dₘ", "Distance", GOOD),
            self.card("p(x)", "Density", ACCENT),
        ).arrange(DOWN, buff=.38).move_to([0, -.05, 0])
        arrows = VGroup(*[
            Arrow(cards[i].get_bottom() + DOWN * .04,
                  cards[i + 1].get_top() + UP * .04,
                  buff=0, color=MUTED, stroke_width=2.3)
            for i in range(2)
        ])
        self.show(VGroup(cards, arrows),
                  LaggedStart(*[FadeIn(card) for card in cards],
                              lag_ratio=.15), Create(arrows), run_time=1.0)
        self.to(41)

        # 41–45: pose the inverse question, ellipse versus circle.
        self.copy("그렇다면 공간을 다시 바꾸면?", "타원 (x−μ)ᵀΣ⁻¹(x−μ)=1  ↔  원 |z|²=1")
        self.clear_stage()
        left = self.contour(1.4, ACCENT).scale(.62).shift(LEFT * 2.0)
        right = Circle(radius=1.4, color=GOOD,
                       stroke_width=2.5).shift(RIGHT * 2.0)
        arrow = Arrow([-.45, 0, 0], [.45, 0, 0],
                      buff=0, color=MUTED, stroke_width=2.8)
        labels = VGroup(
            txt("Mahalanobis", 27, ACCENT).move_to([-2.0, -2.2, 0]),
            txt("Euclidean", 27, GOOD).move_to([2.0, -2.2, 0]),
        )
        self.show(VGroup(left, right, arrow, labels), Create(left),
                  Create(right), GrowArrow(arrow), FadeIn(labels),
                  run_time=.85)
        self.to(45)

        # 45–50: actual whitening sends covariance Sigma to I.
        self.copy("타원을 원으로 만들 수 있을까?", "Σ  →  I     /     Whitening")
        self.clear_stage()
        cloud = self.cloud()
        ellipse = self.contour(1.5, ACCENT)
        self.show(VGroup(cloud, ellipse), FadeIn(cloud),
                  Create(ellipse), run_time=.7)
        whitened = self.whitened_cloud()
        circle = Circle(radius=1.5, color=GOOD, stroke_width=2.5,
                        fill_color=GOOD, fill_opacity=.025)
        self.play(Transform(cloud, whitened),
                  Transform(ellipse, circle), run_time=1.15)
        final = txt("타원을 원으로 만들 수 있을까?", 31, INK)
        final.move_to([0, -3.75, 0])
        frame = SurroundingRectangle(final, color=ACCENT,
                                     buff=.23, corner_radius=.12)
        self.play(FadeIn(final), Create(frame), run_time=.55)
        self.stage.add(final, frame)
        self.to(50)

    def axes(self):
        return VGroup(
            Arrow([-3.65, 0, 0], [3.65, 0, 0], buff=0,
                  color=MUTED, stroke_width=2),
            Arrow([0, -3.4, 0], [0, 3.4, 0], buff=0,
                  color=MUTED, stroke_width=2),
        )

    def contour(self, distance, color):
        return Ellipse(width=2 * distance * np.sqrt(EIGVALS[1]),
                       height=2 * distance * np.sqrt(EIGVALS[0]),
                       color=color, stroke_width=2.5,
                       stroke_opacity=.9, fill_color=color,
                       fill_opacity=.025).rotate(MAJOR_ANGLE)

    def contour_point(self, distance, degrees):
        theta = degrees * DEGREES
        base = np.array([distance * np.sqrt(EIGVALS[1]) * np.cos(theta),
                         distance * np.sqrt(EIGVALS[0]) * np.sin(theta)])
        c, s = np.cos(MAJOR_ANGLE), np.sin(MAJOR_ANGLE)
        p = np.array([[c, -s], [s, c]]) @ base
        return np.array([p[0], p[1], 0])

    def cloud(self):
        return VGroup(*[
            Dot([x, y, 0], radius=.065, color=WEIGHT) for x, y in POINTS
        ])

    def whitened_cloud(self):
        transformed = POINTS @ WHITEN.T
        return VGroup(*[
            Dot([x, y, 0], radius=.065, color=WEIGHT)
            for x, y in transformed
        ])

    def bell(self, cx):
        curve = ParametricFunction(
            lambda t: np.array([cx + .52 * t,
                                -.85 + 3.05 * np.exp(-.5 * t * t), 0]),
            t_range=[-3.2, 3.2], color=WEIGHT, stroke_width=3.2)
        base = Line([cx - 1.75, -.85, 0], [cx + 1.75, -.85, 0],
                    color=MUTED, stroke_width=2)
        return VGroup(base, curve)

    def density_bar(self, distance, relative, y):
        left = -1.9
        box = RoundedRectangle(width=6.1, height=.75,
                               corner_radius=.1, stroke_color=MUTED,
                               stroke_width=1.1, fill_opacity=0)
        box.move_to([0, y, 0])
        bar = Rectangle(width=max(.08, 3.55 * relative), height=.33,
                        stroke_width=0, fill_color=GOOD,
                        fill_opacity=.82)
        bar.move_to([left + bar.width / 2, y, 0])
        label = txt(f"dₘ={distance}", 27, INK).move_to([-2.35, y, 0])
        value = txt(f"{relative:.2f}", 27, GOOD).move_to([2.35, y, 0])
        return VGroup(box, bar, label, value)

    def covariance_shape(self, sigma):
        vals, vecs = np.linalg.eigh(sigma)
        angle = np.arctan2(vecs[1, 1], vecs[0, 1])
        return Ellipse(width=3.4 * np.sqrt(vals[1]),
                       height=3.4 * np.sqrt(vals[0]),
                       color=ACCENT, stroke_width=2.8,
                       fill_color=ACCENT, fill_opacity=.04).rotate(angle)

    def card(self, symbol, meaning, color):
        box = RoundedRectangle(width=5.5, height=1.15,
                               corner_radius=.15, stroke_color=color,
                               stroke_width=1.5, fill_color=color,
                               fill_opacity=.07)
        sym = txt(symbol, 38, color).move_to([-1.7, 0, 0])
        label = txt(meaning, 29, INK).move_to([.85, 0, 0])
        return VGroup(box, sym, label)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.14)
        self.head = txt(heading, 30, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 26, INK).move_to([0, -5.8, 0])
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
