"""Distribution mathematics 10: the unit of distance can depend on a distribution."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


SIGMA = np.array([[4., 1.], [1., 1.]])
EIGVALS, EIGVECS = np.linalg.eigh(SIGMA)
MAJOR_ANGLE = np.arctan2(EIGVECS[1, 1], EIGVECS[0, 1])


def sample_points():
    angles = np.linspace(0, TAU, 24, endpoint=False)
    base = np.array([(r * np.cos(t), r * np.sin(t))
                     for r in (.65, 1.3) for t in angles])
    base /= np.sqrt(np.mean(base[:, 0] ** 2))
    return np.column_stack((2 * base[:, 0],
                            .5 * base[:, 0] + np.sqrt(.75) * base[:, 1]))


POINTS = sample_points()


class DistributionSetsDistance(Scene):
    DURATION = 50

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  10", 19, MUTED).move_to(UP * 7.3),
            txt("거리의 단위는 분포가 결정할 수 있다", 31).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: two observations at precisely the same Euclidean distance.
        self.copy("둘 다 평균에서 2만큼", "|A−μ| = |B−μ| = 2")
        axes = self.axes()
        circle = Circle(radius=2, color=MUTED, stroke_width=2,
                        stroke_opacity=.75)
        a = Dot([2, 0, 0], radius=.17, color=GOOD)
        b = Dot([0, 2, 0], radius=.17, color=PRUNE)
        mu = Dot(ORIGIN, radius=.12, color=ACCENT)
        rays = VGroup(
            Line(ORIGIN, [2, 0, 0], color=GOOD, stroke_width=4),
            Line(ORIGIN, [0, 2, 0], color=PRUNE, stroke_width=4),
        )
        labels = VGroup(
            txt("A", 36, GOOD).move_to([2.35, -.3, 0]),
            txt("B", 36, PRUNE).move_to([.32, 2.27, 0]),
            txt("μ", 29, ACCENT).move_to([-.32, -.35, 0]),
            txt("2", 31, GOOD).move_to([1.1, -.45, 0]),
            txt("2", 31, PRUNE).move_to([-.42, 1.1, 0]),
        )
        self.show(VGroup(axes, circle, rays, a, b, mu, labels),
                  FadeIn(axes), Create(circle), Create(rays),
                  FadeIn(a), FadeIn(b), FadeIn(mu), FadeIn(labels),
                  run_time=.9)
        self.to(4)

        # 4–8: reveal the data while retaining the Euclidean circle.
        self.copy("점구름이 나타나면", "같은 원 위의 두 점이 다르게 보입니다")
        cloud = self.cloud()
        self.play(FadeIn(cloud), run_time=1.15)
        self.stage.add(cloud)
        self.to(8)

        # 8–12: A lies in a common direction, B in a sparse one.
        self.copy("A는 익숙하고, B는 드뭅니다", "Typical  A                 Unusual  B")
        spot_a = Circle(radius=.5, color=GOOD, stroke_width=2.5,
                        stroke_opacity=.8).move_to(a)
        spot_b = Circle(radius=.5, color=PRUNE, stroke_width=2.5,
                        stroke_opacity=.8).move_to(b)
        typical = txt("Typical", 29, GOOD).move_to([2.65, 1.0, 0])
        unusual = txt("Unusual", 29, PRUNE).move_to([1.1, 2.7, 0])
        self.play(Create(spot_a), Create(spot_b),
                  FadeIn(typical), FadeIn(unusual), run_time=.75)
        self.stage.add(spot_a, spot_b, typical, unusual)
        self.to(12)

        # 12–16: different directional ruler marks, same coordinate displacement.
        self.copy("같은 2, 다른 눈금", "가로는 넓게 퍼지고 세로는 좁게 퍼집니다")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud()
        circle = Circle(radius=2, color=MUTED, stroke_width=1.8,
                        stroke_opacity=.6)
        points = self.two_points()
        ticks = VGroup(*[
            Line([x, -.14, 0], [x, .14, 0], color=GOOD, stroke_width=2.4)
            for x in (-2, 0, 2)
        ], *[
            Line([-.14, y, 0], [.14, y, 0], color=PRUNE, stroke_width=2.4)
            for y in (-2, -1, 0, 1, 2)
        ])
        spread = VGroup(
            txt("σₓ = 2", 30, GOOD).move_to([2.35, -1.0, 0]),
            txt("σᵧ = 1", 30, PRUNE).move_to([-1.1, 2.65, 0]),
        )
        self.show(VGroup(axes, cloud, circle, points, ticks, spread),
                  FadeIn(axes), FadeIn(cloud), Create(circle),
                  FadeIn(points), FadeIn(ticks), FadeIn(spread),
                  run_time=.8)
        self.to(16)

        # 16–20: equal displacement is not an equal change relative to spread.
        self.copy("좌표의 2는 같지만", "분포 안에서는 B의 변화가 더 큽니다")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud()
        points = self.two_points()
        wide = DoubleArrow([-3.25, -2.75, 0], [3.25, -2.75, 0],
                           buff=0, color=GOOD, stroke_width=3)
        narrow = DoubleArrow([-3.85, -1.35, 0], [-3.85, 1.35, 0],
                             buff=0, color=PRUNE, stroke_width=3)
        notes = VGroup(
            txt("넓은 방향", 28, GOOD).move_to([2.4, -3.2, 0]),
            txt("좁은 방향", 28, PRUNE).move_to([-2.35, 2.55, 0]),
        )
        self.show(VGroup(axes, cloud, points, wide, narrow, notes),
                  FadeIn(axes), FadeIn(cloud), FadeIn(points),
                  GrowArrow(wide), GrowArrow(narrow), FadeIn(notes),
                  run_time=.85)
        self.to(20)

        # 20–25: the main perspective shift, circle to distribution-aware ellipse.
        self.copy("자를 분포에 맞춰 바꾸면", "같은 거리의 선이 원에서 타원으로")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud()
        points = self.two_points()
        equal = Circle(radius=2, color=MUTED, stroke_width=2.3)
        self.show(VGroup(axes, cloud, points, equal), FadeIn(axes),
                  FadeIn(cloud), FadeIn(points), Create(equal), run_time=.65)
        ellipse = self.contour(1.7, ACCENT)
        self.play(Transform(equal, ellipse), run_time=1.25)
        a_in = txt("A: 안쪽", 29, GOOD).move_to([2.55, 1.15, 0])
        b_out = txt("B: 바깥", 29, PRUNE).move_to([1.2, 2.75, 0])
        self.play(FadeIn(a_in), FadeIn(b_out), run_time=.45)
        self.stage.add(a_in, b_out)
        self.to(25)

        # 25–29: covariance captures the directional scales.
        self.copy("방향과 퍼짐은 Σ 안에", "Σ = [[4, 1], [1, 1]]")
        self.clear_stage()
        mat = self.matrix(("4", "1", "1", "1"))
        sigma = txt("Σ =", 42, ACCENT).move_to([-3.1, 0, 0])
        cloud = self.cloud(scale=.49).shift(DOWN * 2.85)
        ellipse = self.contour(1.7, ACCENT).scale(.49).shift(DOWN * 2.85)
        self.show(VGroup(mat, sigma, cloud, ellipse), FadeIn(mat),
                  FadeIn(sigma), FadeIn(cloud), Create(ellipse),
                  run_time=.8)
        self.to(29)

        # 29–33: inverse covariance gives large spread small weight.
        self.copy("퍼짐을 반대로 보정합니다", "큰 퍼짐 → 작은 가중치   /   작은 퍼짐 → 큰 가중치")
        self.clear_stage()
        sigma = txt("Σ", 56, WEIGHT).move_to([-2.5, 1.2, 0])
        arrow = Arrow([-1.45, 1.2, 0], [1.45, 1.2, 0],
                      buff=0, color=ACCENT, stroke_width=3)
        inverse = txt("Σ⁻¹", 56, ACCENT).move_to([2.5, 1.2, 0])
        bars = VGroup(
            self.weight_card("많이 퍼짐", "작게", GOOD, -.55),
            self.weight_card("적게 퍼짐", "크게", PRUNE, -2.1),
        )
        self.show(VGroup(sigma, arrow, inverse, bars), FadeIn(sigma),
                  GrowArrow(arrow), FadeIn(inverse), FadeIn(bars),
                  run_time=.8)
        self.to(33)

        # 33–37: name the metric, after the ruler intuition has landed.
        self.copy("이 거리가 Mahalanobis distance", "차이 · 역공분산 · 차이")
        self.clear_stage()
        first = txt("x − μ", 39, WEIGHT).move_to([0, 1.85, 0])
        inverse = txt("Σ⁻¹", 43, ACCENT).move_to([0, .25, 0])
        formula = txt("dₘ(x,μ) = √[(x−μ)ᵀ Σ⁻¹ (x−μ)]", 31, INK)
        formula.move_to([0, -1.5, 0])
        name = txt("Mahalanobis Distance", 34, GOOD).move_to([0, -2.65, 0])
        self.show(VGroup(first, inverse, formula, name),
                  FadeIn(first), FadeIn(inverse), FadeIn(formula),
                  FadeIn(name), run_time=.9)
        self.to(37)

        # 37–41: exact distances for A=(2,0), B=(0,2).
        self.copy("처음 두 점을 다시 재면", "Euclidean: 둘 다 2   /   Mahalanobis: A < B")
        self.clear_stage()
        cards = VGroup(
            self.distance_card("A", "2", "1.15", GOOD),
            self.distance_card("B", "2", "2.31", PRUNE),
        ).arrange(DOWN, buff=.45).move_to([0, .2, 0])
        header = txt("직선거리       분포 기준 거리", 28, MUTED)
        header.move_to([.7, 2.65, 0])
        verdict = txt("같은 2  →  B가 더 멀다", 32, ACCENT)
        verdict.move_to([0, -2.75, 0])
        self.show(VGroup(cards, header, verdict), FadeIn(cards),
                  FadeIn(header), FadeIn(verdict), run_time=.85)
        self.to(41)

        # 41–45: constant Mahalanobis distances form nested ellipses.
        self.copy("등거리선도 달라집니다", "dₘ = 1     /     dₘ = 2")
        self.clear_stage()
        axes = self.axes()
        inner = self.contour(1, GOOD)
        outer = self.contour(2, ACCENT)
        center = Dot(ORIGIN, radius=.12, color=INK)
        labels = VGroup(
            txt("1", 29, GOOD).move_to([1.9, 1.0, 0]),
            txt("2", 29, ACCENT).move_to([3.4, 1.75, 0]),
        )
        self.show(VGroup(axes, inner, outer, center, labels),
                  FadeIn(axes), Create(inner), Create(outer),
                  FadeIn(center), FadeIn(labels), run_time=.85)
        self.to(45)

        # 45–50: circles versus ellipses, then Gaussian level sets.
        self.copy("원에서 타원으로", "왜 Gaussian의 등고선도 이런 모양일까?")
        self.clear_stage()
        left = Circle(radius=1.25, color=MUTED, stroke_width=2)
        left.move_to([-2.1, .55, 0])
        right = self.contour(1, ACCENT).scale(.62).shift(RIGHT * 2.1 + UP * .55)
        titles = VGroup(
            txt("Euclidean", 27, MUTED).move_to([-2.1, -1.45, 0]),
            txt("Mahalanobis", 27, ACCENT).move_to([2.1, -1.45, 0]),
        )
        self.show(VGroup(left, right, titles), Create(left),
                  Create(right), FadeIn(titles), run_time=.75)
        glow = self.contour(1, ACCENT).scale(.62).shift(RIGHT * 2.1 + UP * .55)
        glow.set_stroke(opacity=.25, width=8)
        question = txt("왜 Gaussian은 타원 모양일까?", 33, INK)
        question.move_to([0, -3.55, 0])
        box = SurroundingRectangle(question, color=ACCENT,
                                   buff=.25, corner_radius=.12)
        self.play(FadeIn(glow), FadeIn(question), Create(box), run_time=.7)
        self.stage.add(glow, question, box)
        self.to(50)

    def axes(self):
        return VGroup(
            Arrow([-3.65, 0, 0], [3.65, 0, 0], buff=0,
                  color=MUTED, stroke_width=2),
            Arrow([0, -3.4, 0], [0, 3.4, 0], buff=0,
                  color=MUTED, stroke_width=2),
        )

    def cloud(self, scale=1):
        return VGroup(*[
            Dot([scale * x, scale * y, 0], radius=.065,
                color=WEIGHT) for x, y in POINTS
        ])

    def contour(self, distance, color):
        return Ellipse(width=2 * distance * np.sqrt(EIGVALS[1]),
                       height=2 * distance * np.sqrt(EIGVALS[0]),
                       color=color, stroke_width=2.5,
                       stroke_opacity=.9, fill_color=color,
                       fill_opacity=.025).rotate(MAJOR_ANGLE)

    def two_points(self):
        return VGroup(
            Dot([2, 0, 0], radius=.16, color=GOOD),
            Dot([0, 2, 0], radius=.16, color=PRUNE),
            Dot(ORIGIN, radius=.11, color=ACCENT),
            txt("A", 31, GOOD).move_to([2.34, -.33, 0]),
            txt("B", 31, PRUNE).move_to([.32, 2.25, 0]),
        )

    def matrix(self, values):
        entries = VGroup(*[
            txt(value, 37, WEIGHT if i in (0, 3) else GOOD).move_to([
                -.8 if i % 2 == 0 else .8, .64 if i < 2 else -.64, 0])
            for i, value in enumerate(values)
        ])
        left = VMobject().set_points_as_corners([
            [-1.8, 1.35, 0], [-2, 1.35, 0], [-2, -1.35, 0],
            [-1.8, -1.35, 0]]).set_stroke(INK, width=2.5)
        right = VMobject().set_points_as_corners([
            [1.8, 1.35, 0], [2, 1.35, 0], [2, -1.35, 0],
            [1.8, -1.35, 0]]).set_stroke(INK, width=2.5)
        return VGroup(left, right, entries)

    def weight_card(self, spread, weight, color, y):
        box = RoundedRectangle(width=6.0, height=.95, corner_radius=.15,
                               stroke_color=color, stroke_width=1.4,
                               fill_color=color, fill_opacity=.07)
        box.move_to([0, y, 0])
        left = txt(spread, 29, color).move_to([-1.45, y, 0])
        arrow = txt("→", 29, MUTED).move_to([0, y, 0])
        right = txt(weight, 29, INK).move_to([1.5, y, 0])
        return VGroup(box, left, arrow, right)

    def distance_card(self, point, euclidean, mahalanobis, color):
        box = RoundedRectangle(width=6.1, height=1.25, corner_radius=.16,
                               stroke_color=color, stroke_width=1.5,
                               fill_color=color, fill_opacity=.07)
        return VGroup(box,
                      txt(point, 39, color).move_to([-2.35, 0, 0]),
                      txt(euclidean, 37, INK).move_to([-.25, 0, 0]),
                      txt(mahalanobis, 37, color).move_to([1.95, 0, 0]))

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
            self.wait(max(0, target - self.time))
