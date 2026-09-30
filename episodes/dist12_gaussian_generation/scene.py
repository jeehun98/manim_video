"""Distribution mathematics 12: generate Gaussians from one standard Gaussian."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


DISPLAY = .72
ANGLE = 45 * DEGREES
ROTATE = np.array([[np.cos(ANGLE), -np.sin(ANGLE)],
                   [np.sin(ANGLE), np.cos(ANGLE)]])
STRETCH = np.diag([2., 1.])
TRANSFORM = ROTATE @ STRETCH
SHIFT = np.array([1., -.6])


def standard_points():
    rng = np.random.default_rng(12)
    points = rng.normal(size=(72, 2))
    points -= points.mean(axis=0)
    values, vectors = np.linalg.eigh(points.T @ points / len(points))
    return points @ vectors @ np.diag(1 / np.sqrt(values)) @ vectors.T


POINTS = standard_points()


class GaussianFromOneCircle(Scene):
    DURATION = 50

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  12", 19, MUTED).move_to(UP * 7.3),
            txt("모든 Gaussian은 하나의 원에서 만들 수 있을까?", 29).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: a centered Gaussian with identity covariance.
        self.copy("출발점은 원형 Gaussian 하나", "Z ~ N(0, I)    /    μ=0, Σ=I")
        axes = self.axes()
        cloud = self.cloud(np.eye(2))
        contour = self.contour(np.eye(2))
        mean = Dot(ORIGIN, radius=.13, color=ACCENT)
        self.show(VGroup(axes, cloud, contour, mean), FadeIn(axes),
                  FadeIn(cloud), Create(contour), FadeIn(mean),
                  run_time=.9)
        self.to(4)

        # 4–8: rotating a measuring direction changes no variance.
        self.copy("아직 특별한 방향이 없습니다", "단위방향 v마다 Var(vᵀZ)=1")
        ray = self.direction_arrow(0)
        badge = txt("Var(vᵀZ) = 1", 32, GOOD).move_to([0, -3.45, 0])
        self.play(GrowArrow(ray), FadeIn(badge), run_time=.55)
        self.stage.add(ray, badge)
        for angle in (35, 70, 120):
            self.play(Transform(ray, self.direction_arrow(angle)),
                      run_time=.38)
        self.to(8)

        # 8–12: stretch only the horizontal coordinate by two.
        self.copy("가로로 두 배 늘리면", "S = diag(2,1)")
        self.play(FadeOut(ray), FadeOut(badge),
                  Transform(cloud, self.cloud(STRETCH)),
                  Transform(contour, self.contour(STRETCH)),
                  run_time=1.1)
        self.stage = VGroup(axes, cloud, contour, mean)
        self.to(12)

        # 12–16: scaling a coordinate by two quadruples its variance.
        self.copy("퍼짐에 방향이 생깁니다", "Cov(SZ) = diag(4,1)")
        axes_marks = VGroup(
            Line([-3.3, 0, 0], [3.3, 0, 0], color=GOOD,
                 stroke_width=3.5, stroke_opacity=.7),
            Line([0, -1.85, 0], [0, 1.85, 0], color=SPARSE,
                 stroke_width=3.5, stroke_opacity=.7),
        )
        labels = VGroup(
            txt("Varₓ = 4", 29, GOOD).move_to([2.45, -1.1, 0]),
            txt("Varᵧ = 1", 29, SPARSE).move_to([-1.1, 2.25, 0]),
        )
        self.play(Create(axes_marks), FadeIn(labels), run_time=.75)
        self.stage.add(axes_marks, labels)
        self.to(16)

        # 16–20: rotate the entire transformed cloud.
        self.copy("이번에는 회전해보면", "R · SZ  →  기울어진 Gaussian")
        self.play(FadeOut(axes_marks), FadeOut(labels),
                  Transform(cloud, self.cloud(TRANSFORM)),
                  Transform(contour, self.contour(TRANSFORM)),
                  run_time=1.15)
        self.stage = VGroup(axes, cloud, contour, mean)
        self.to(20)

        # 20–24: combine stretch and rotation in one matrix A.
        self.copy("두 동작을 하나의 행렬로", "A = R · S    /    X₀ = AZ")
        self.clear_stage()
        sequence = VGroup(
            self.shape_card(np.eye(2), -2.65, WEIGHT, "Z"),
            self.shape_card(STRETCH, 0, GOOD, "SZ"),
            self.shape_card(TRANSFORM, 2.65, ACCENT, "AZ"),
        )
        arrows = VGroup(
            Arrow([-1.55, 0, 0], [-1.1, 0, 0], buff=0,
                  color=MUTED, stroke_width=2.5),
            Arrow([1.1, 0, 0], [1.55, 0, 0], buff=0,
                  color=MUTED, stroke_width=2.5),
        )
        self.show(VGroup(sequence, arrows), FadeIn(sequence),
                  GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  run_time=.85)
        self.to(24)

        # 24–28: transform identity covariance into AA^T.
        self.copy("공분산은 어떻게 바뀔까?", "Cov(AZ) = A I Aᵀ = AAᵀ")
        self.clear_stage()
        top = txt("Cov(Z) = I", 39, WEIGHT).move_to([0, 1.8, 0])
        map_arrow = Arrow([0, 1.1, 0], [0, .25, 0],
                          buff=0, color=ACCENT, stroke_width=3)
        middle = txt("X₀ = AZ", 41, GOOD).move_to([0, -.3, 0])
        result = txt("Cov(X₀) = A I Aᵀ = AAᵀ", 37, ACCENT)
        result.move_to([0, -1.9, 0])
        self.show(VGroup(top, map_arrow, middle, result),
                  FadeIn(top), GrowArrow(map_arrow), FadeIn(middle),
                  FadeIn(result), run_time=.85)
        self.to(28)

        # 28–32: choose A so AA^T is the desired covariance.
        self.copy("원하는 공분산도 만들 수 있습니다", "AAᵀ = Σ")
        self.clear_stage()
        source = self.contour(np.eye(2)).scale(.55).shift(LEFT * 2.25)
        target = self.contour(TRANSFORM).scale(.55).shift(RIGHT * 2.25)
        arrow = Arrow([-.85, 0, 0], [.85, 0, 0],
                      buff=0, color=ACCENT, stroke_width=3)
        a_label = txt("A", 37, ACCENT).move_to([0, .55, 0])
        labels = VGroup(
            txt("I", 34, WEIGHT).move_to([-2.25, -1.65, 0]),
            txt("Σ", 34, ACCENT).move_to([2.25, -1.65, 0]),
            txt("AAᵀ = Σ", 36, GOOD).move_to([0, -2.8, 0]),
        )
        self.show(VGroup(source, target, arrow, a_label, labels),
                  Create(source), GrowArrow(arrow), Create(target),
                  FadeIn(a_label), FadeIn(labels), run_time=.85)
        self.to(32)

        # 32–36: shift every transformed point by the desired mean.
        self.copy("위치도 바꾸려면", "X = AZ + μ")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud(TRANSFORM)
        contour = self.contour(TRANSFORM)
        mean = Dot(ORIGIN, radius=.13, color=ACCENT)
        self.show(VGroup(axes, cloud, contour, mean),
                  FadeIn(axes), FadeIn(cloud), Create(contour),
                  FadeIn(mean), run_time=.65)
        self.play(Transform(cloud, self.cloud(TRANSFORM, SHIFT)),
                  Transform(contour, self.contour(TRANSFORM, SHIFT)),
                  mean.animate.move_to(self.position(SHIFT)),
                  run_time=1.05)
        self.to(36)

        # 36–40: one generative equation summarizes the construction.
        self.copy("한 줄로 쓰면", "Z ~ N(0,I)  →  X ~ N(μ,Σ)")
        self.clear_stage()
        formula = txt("X = AZ + μ", 52, ACCENT).move_to([0, 1.8, 0])
        source = txt("Z ~ N(0, I)", 34, WEIGHT).move_to([0, .45, 0])
        arrow = Arrow([0, -.1, 0], [0, -.95, 0],
                      buff=0, color=MUTED, stroke_width=3)
        result = txt("X ~ N(μ, Σ)", 36, GOOD).move_to([0, -1.45, 0])
        condition = txt("AAᵀ = Σ", 30, MUTED).move_to([0, -2.6, 0])
        self.show(VGroup(formula, source, arrow, result, condition),
                  FadeIn(formula), FadeIn(source), GrowArrow(arrow),
                  FadeIn(result), FadeIn(condition), run_time=.85)
        self.to(40)

        # 40–44: one source branches into many visible Gaussian shapes.
        self.copy("서로 다른 Gaussian도 하나에서", "같은 Z, 서로 다른 A와 μ")
        self.clear_stage()
        source = Circle(radius=.66, color=WEIGHT, stroke_width=2.3,
                        fill_color=WEIGHT, fill_opacity=.025)
        source.move_to([0, 2.4, 0])
        center_text = txt("N(0,I)", 27, WEIGHT).move_to(source)
        panels = VGroup(
            self.mini_shape(-3.1, np.diag([2., .65]), 0, "가로"),
            self.mini_shape(-1.55, np.diag([.65, 2.]), 0, "세로"),
            self.mini_shape(0, TRANSFORM, 0, "대각선"),
            self.mini_shape(1.55, ROTATE @ np.diag([2.5, .35]), 0, "가는"),
            self.mini_shape(3.1, TRANSFORM, .4, "이동"),
        )
        branches = VGroup(*[
            Arrow([0, 1.7, 0], [x, .55, 0], buff=.08,
                  color=MUTED, stroke_width=1.8)
            for x in (-3.1, -1.55, 0, 1.55, 3.1)
        ])
        self.show(VGroup(source, center_text, branches, panels),
                  FadeIn(source), FadeIn(center_text),
                  Create(branches), FadeIn(panels), run_time=1.0)
        self.to(44)

        # 44–47: reverse the construction, briefly recalling whitening.
        self.copy("거꾸로 돌리면", "Ellipse → Circle    /    Whitening")
        self.clear_stage()
        cloud = self.cloud(TRANSFORM, SHIFT)
        contour = self.contour(TRANSFORM, SHIFT)
        arrow = txt("Σ  →  I", 34, GOOD).move_to([0, -3.3, 0])
        self.show(VGroup(cloud, contour, arrow), FadeIn(cloud),
                  Create(contour), FadeIn(arrow), run_time=.5)
        self.play(Transform(cloud, self.cloud(np.eye(2))),
                  Transform(contour, self.contour(np.eye(2))),
                  run_time=.85)
        self.to(47)

        # 47–50: the next question points beyond linear transformations.
        self.copy("Gaussian 밖으로도 확장할 수 있을까?", "단순한 분포를 변형해 더 복잡한 분포로")
        self.clear_stage()
        grid = self.grid(0)
        question = txt("분포 자체를 변환해서 만들 수 있을까?", 31, INK)
        question.move_to([0, -3.65, 0])
        frame = SurroundingRectangle(question, color=ACCENT,
                                     buff=.22, corner_radius=.12)
        self.show(VGroup(grid, question, frame), FadeIn(grid),
                  FadeIn(question), Create(frame), run_time=.55)
        self.play(Transform(grid, self.grid(.7)), run_time=.8)
        self.to(50)

    def position(self, point):
        return np.array([DISPLAY * point[0], DISPLAY * point[1], 0])

    def cloud(self, matrix, mean=None):
        if mean is None:
            mean = np.zeros(2)
        values = POINTS @ matrix.T + mean
        return VGroup(*[
            Dot(self.position(p), radius=.067, color=WEIGHT) for p in values
        ])

    def contour(self, matrix, mean=None, distance=2):
        if mean is None:
            mean = np.zeros(2)
        covariance = matrix @ matrix.T
        values, vectors = np.linalg.eigh(covariance)
        angle = np.arctan2(vectors[1, 1], vectors[0, 1])
        return Ellipse(width=2 * DISPLAY * distance * np.sqrt(values[1]),
                       height=2 * DISPLAY * distance * np.sqrt(values[0]),
                       color=ACCENT, stroke_width=2.3,
                       stroke_opacity=.85, fill_color=ACCENT,
                       fill_opacity=.025).rotate(angle).shift(self.position(mean))

    def axes(self):
        return VGroup(
            Arrow([-3.6, 0, 0], [3.6, 0, 0], buff=0,
                  color=MUTED, stroke_width=2),
            Arrow([0, -3.2, 0], [0, 3.2, 0], buff=0,
                  color=MUTED, stroke_width=2),
        )

    def direction_arrow(self, degrees):
        t = degrees * DEGREES
        return Arrow(ORIGIN, [1.8 * np.cos(t), 1.8 * np.sin(t), 0],
                     buff=0, color=GOOD, stroke_width=4)

    def shape_card(self, matrix, x, color, label):
        box = RoundedRectangle(width=2.1, height=3.1,
                               corner_radius=.15, stroke_color=color,
                               stroke_width=1.3, fill_color=color,
                               fill_opacity=.025).move_to([x, 0, 0])
        shape = self.contour(matrix).scale(.33).shift(RIGHT * x + UP * .2)
        name = txt(label, 30, color).move_to([x, -1.9, 0])
        return VGroup(box, shape, name)

    def mini_shape(self, x, matrix, offset, label):
        shape = self.contour(matrix).scale(.18)
        shape.move_to([x + offset, -.35, 0])
        text_label = txt(label, 23, INK, 1.3).move_to([x, -1.65, 0])
        return VGroup(shape, text_label)

    def grid(self, bend):
        lines = VGroup()
        for fixed in np.linspace(-2.2, 2.2, 6):
            lines.add(ParametricFunction(
                lambda t, f=fixed: np.array([
                    f + bend * .38 * np.sin(t * 1.4), t, 0]),
                t_range=[-2.2, 2.2], color=MUTED,
                stroke_width=1.6, stroke_opacity=.65))
            lines.add(ParametricFunction(
                lambda t, f=fixed: np.array([
                    t, f + bend * .38 * np.sin(t * 1.4), 0]),
                t_range=[-2.2, 2.2], color=MUTED,
                stroke_width=1.6, stroke_opacity=.65))
        return lines

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
