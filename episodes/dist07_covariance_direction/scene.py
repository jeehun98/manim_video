"""Distribution mathematics 07: covariance and the direction of joint spread."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


def standardized_base():
    """Paired centered coordinates with unit variances and zero covariance."""
    theta = np.linspace(0, TAU, 24, endpoint=False)
    points = np.array([(r * np.cos(t), r * np.sin(t))
                       for r in (.65, 1.30) for t in theta])
    return points / np.sqrt(np.mean(points[:, 0] ** 2))


BASE = standardized_base()


def cloud_coordinates(rho):
    """The same observations with Var(X)=Var(Y)=1 and Cov(X,Y)=rho."""
    return np.column_stack((BASE[:, 0],
                            rho * BASE[:, 0] + np.sqrt(1 - rho * rho) * BASE[:, 1]))


class CovarianceDirection(Scene):
    DURATION = 49

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  07", 19, MUTED).move_to(UP * 7.3),
            txt("공분산이 바뀌면 왜 분포가 기울어질까?", 29).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: circular cloud and its mean.
        self.copy("기울지 않은 점구름", "평균점 (μₓ, μᵧ)")
        axes = self.axes()
        dots = self.cloud(0)
        mean = Dot(ORIGIN, radius=.14, color=ACCENT)
        mean_label = txt("(μₓ, μᵧ)", 26, ACCENT).move_to([1.0, -.48, 0])
        self.show(VGroup(axes, dots, mean, mean_label), FadeIn(axes),
                  FadeIn(dots), FadeIn(mean), FadeIn(mean_label), run_time=1.0)
        self.to(4)

        # 4–8: fix both marginal variances throughout the transformations.
        self.copy("각자의 퍼짐은 고정", "Var(X) = 1     Var(Y) = 1")
        fixed = VGroup(
            self.badge("Var(X) = 1", WEIGHT, -1.65),
            self.badge("Var(Y) = 1", SPARSE, 1.65),
        )
        self.play(FadeIn(fixed), run_time=.55)
        self.stage.add(fixed)
        self.to(8)

        # 8–13: covariance rises as paired positions become concordant.
        self.copy("공분산만 양수로 바꾸면", "x가 클 때 y도 큰 짝이 늘어납니다")
        cov_label = txt("Cov(X,Y) = 0", 31, MUTED).move_to([0, 3.2, 0])
        self.play(FadeIn(cov_label), run_time=.25)
        for rho in (.2, .5, .8):
            next_label = txt(f"Cov(X,Y) = {rho:.1f}", 31, GOOD).move_to(cov_label)
            self.play(Transform(dots, self.cloud(rho)),
                      Transform(cov_label, next_label), run_time=.75)
        self.stage.add(cov_label)
        self.to(13)

        # 13–17: the concordant quadrants have positive products.
        self.copy("왜 오른쪽 위로 기울었을까?", "오른쪽 위와 왼쪽 아래: 편차의 곱이 +")
        upper = txt("(+)(+) = +", 29, GOOD).move_to([2.1, 2.45, 0])
        lower = txt("(−)(−) = +", 29, GOOD).move_to([-2.0, -2.45, 0])
        line = Line([-2.45, -2.45, 0], [2.45, 2.45, 0],
                    color=GOOD, stroke_width=3, stroke_opacity=.75)
        self.play(Create(line), FadeIn(upper), FadeIn(lower), run_time=.8)
        self.stage.add(line, upper, lower)
        self.to(17)

        # 17–22: compare covariance zero and stronger positive covariance.
        self.copy("같은 방향의 짝이 많아질수록", "Cov: 0  →  0.2  →  0.5  →  0.8")
        self.clear_stage()
        axes = self.axes()
        dots = self.cloud(0)
        outline = self.outline(0)
        fixed = VGroup(self.badge("Var(X) = 1", WEIGHT, -1.65),
                       self.badge("Var(Y) = 1", SPARSE, 1.65))
        cov_label = txt("Cov = 0", 33, MUTED).move_to([0, 3.2, 0])
        self.show(VGroup(axes, dots, outline, fixed, cov_label),
                  FadeIn(axes), FadeIn(dots), FadeIn(outline), FadeIn(fixed),
                  FadeIn(cov_label), run_time=.65)
        for rho in (.2, .5, .8):
            self.play(Transform(dots, self.cloud(rho)),
                      Transform(outline, self.outline(rho)),
                      Transform(cov_label, txt(f"Cov = {rho:.1f}", 33, GOOD).move_to(cov_label)),
                      run_time=.55)
        self.to(22)

        # 22–27: opposite-sign products reverse the tilt.
        self.copy("반대 방향의 짝이 많으면", "왼쪽 위·오른쪽 아래는 편차의 곱이 −")
        self.play(Transform(dots, self.cloud(-.8)),
                  Transform(outline, self.outline(-.8)),
                  Transform(cov_label, txt("Cov = −0.8", 33, PRUNE).move_to(cov_label)),
                  run_time=1.15)
        self.to(27)

        # 27–31: three geometric outcomes under identical marginal variances.
        self.copy("세 가지 함께 퍼지는 방향", "두 분산은 모두 1, 공분산만 다릅니다")
        self.clear_stage()
        panels = VGroup(
            self.panel(.8, -2.45, GOOD, "Cov > 0"),
            self.panel(0, 0, MUTED, "Cov = 0"),
            self.panel(-.8, 2.45, PRUNE, "Cov < 0"),
        )
        self.show(panels, FadeIn(panels), run_time=.75)
        self.to(31)

        # 31–35: isolate the three numbers represented by the cloud.
        self.copy("2차원 퍼짐을 적는 세 숫자", "Var(X), Var(Y), Cov(X,Y)")
        self.clear_stage()
        cards = VGroup(
            self.badge("Var(X)", WEIGHT, -2.35, y=.8, width=2.15),
            self.badge("Var(Y)", SPARSE, 0, y=.8, width=2.15),
            self.badge("Cov(X,Y)", GOOD, 2.35, y=.8, width=2.15),
        )
        small = self.cloud(.8, scale=.5).shift(DOWN * 1.4)
        self.show(VGroup(cards, small), FadeIn(cards), FadeIn(small), run_time=.8)
        self.to(35)

        # 35–40: diagonal variances and mirrored off-diagonal covariance.
        self.copy("하나의 배열로 묶으면", "대각선은 분산, 나머지 두 칸은 공분산")
        self.clear_stage()
        matrix = self.matrix(("?", "?", "?", "?"))
        self.show(matrix, FadeIn(matrix), run_time=.45)
        next_matrix = self.matrix(("Var(X)", "?", "?", "Var(Y)"))
        self.play(Transform(matrix, next_matrix), run_time=.65)
        full_matrix = self.matrix(("Var(X)", "Cov(X,Y)", "Cov(X,Y)", "Var(Y)"))
        self.play(Transform(matrix, full_matrix), run_time=.75)
        self.to(40)

        # 40–44: name the covariance matrix and retain the tilted cloud.
        self.copy("공분산 행렬 Σ", "각자의 퍼짐 + 함께 움직이는 방향")
        self.clear_stage()
        sigma = txt("Σ =", 46, ACCENT).move_to([-3.55, .7, 0])
        matrix = self.matrix(("Var(X)", "Cov(X,Y)", "Cov(X,Y)", "Var(Y)"))
        matrix.scale(.8).shift(RIGHT * .75 + UP * .7)
        cloud = self.cloud(.8, scale=.65).shift(DOWN * 2.0)
        oval = self.outline(.8, scale=.65).shift(DOWN * 2.0)
        self.show(VGroup(sigma, matrix, cloud, oval), FadeIn(sigma),
                  FadeIn(matrix), FadeIn(cloud), Create(oval), run_time=.8)
        self.to(44)

        # 44–49: ask whether the matrix reveals the major direction.
        self.copy("숫자만 보고 방향을 찾을 수 있을까?", "행렬 안에서 가장 길게 퍼진 방향은?")
        self.clear_stage()
        example = self.matrix(("1", "0.8", "0.8", "1"), compact=True)
        example.scale(.75).shift(LEFT * 1.5)
        symbol = txt("Σ =", 37, ACCENT).move_to([-3.5, 0, 0])
        oval = self.outline(.8, scale=.55).shift(RIGHT * 2.1)
        cloud = self.cloud(.8, scale=.55).shift(RIGHT * 2.1)
        connection = Arrow([.15, 0, 0], [.95, 0, 0], buff=0,
                           color=ACCENT, stroke_width=3)
        self.show(VGroup(symbol, example, connection, oval, cloud),
                  FadeIn(symbol), FadeIn(example), GrowArrow(connection),
                  FadeIn(oval), FadeIn(cloud), run_time=.75)
        major = Line([.8, -1.3, 0], [3.4, 1.3, 0], color=ACCENT,
                     stroke_width=4)
        question = txt("행렬 안에서 분포의 방향을 찾을 수 있을까?", 29, INK)
        question.move_to([0, -3.7, 0])
        box = SurroundingRectangle(question, color=ACCENT, buff=.22,
                                   corner_radius=.12)
        self.play(Create(major), FadeIn(question), Create(box), run_time=.7)
        self.stage.add(major, question, box)
        self.to(49)

    def axes(self):
        return VGroup(
            Arrow([-3.25, 0, 0], [3.25, 0, 0], buff=0,
                  color=MUTED, stroke_width=2.4),
            Arrow([0, -2.65, 0], [0, 2.65, 0], buff=0,
                  color=MUTED, stroke_width=2.4),
            txt("x", 25, WEIGHT).move_to([3.45, -.25, 0]),
            txt("y", 25, SPARSE).move_to([-.25, 2.83, 0]),
        )

    def cloud(self, rho, scale=1):
        return VGroup(*[
            Dot([scale * 1.5 * x, scale * 1.5 * y, 0],
                radius=.065 if scale == 1 else .055, color=WEIGHT)
            for x, y in cloud_coordinates(rho)
        ])

    def outline(self, rho, scale=1):
        # Eigenvalues 1±|rho|; equal marginal variances make the axes ±45°.
        major = 5.2 * np.sqrt(1 + abs(rho)) * scale
        minor = 5.2 * np.sqrt(1 - abs(rho)) * scale
        return Ellipse(width=major, height=minor, color=ACCENT,
                       stroke_width=2.4, stroke_opacity=.85,
                       fill_color=ACCENT, fill_opacity=.025).rotate(
                           45 * DEGREES if rho >= 0 else -45 * DEGREES)

    def badge(self, label, color, x, y=-3.6, width=3.0):
        box = RoundedRectangle(width=width, height=.8, corner_radius=.15,
                               stroke_color=color, stroke_width=1.5,
                               fill_color=color, fill_opacity=.075)
        box.move_to([x, y, 0])
        return VGroup(box, txt(label, 25, color, width - .2).move_to(box))

    def panel(self, rho, x, color, label):
        box = RoundedRectangle(width=2.27, height=3.0, corner_radius=.15,
                               stroke_color=color, stroke_width=1.3,
                               fill_color=color, fill_opacity=.025)
        box.move_to([x, -.1, 0])
        dots = self.cloud(rho, scale=.37).shift(RIGHT * x)
        outline = self.outline(rho, scale=.37).shift(RIGHT * x)
        sign = txt(label, 25, color, 2.2).move_to([x, -2.25, 0])
        return VGroup(box, outline, dots, sign)

    def matrix(self, values, compact=False):
        width = 3.75 if compact else 5.75
        x = (-.85, .85) if compact else (-1.5, 1.5)
        size = 29 if compact else 27
        entries = VGroup(*[
            txt(value, size, WEIGHT if i in (0, 3) else GOOD,
                1.65 if compact else 2.65).move_to([x[i % 2],
                                                     .66 if i < 2 else -.66, 0])
            for i, value in enumerate(values)
        ])
        left = VMobject().set_points_as_corners([
            [-width / 2 + .22, 1.35, 0], [-width / 2, 1.35, 0],
            [-width / 2, -1.35, 0], [-width / 2 + .22, -1.35, 0]
        ]).set_stroke(INK, width=2.6)
        right = VMobject().set_points_as_corners([
            [width / 2 - .22, 1.35, 0], [width / 2, 1.35, 0],
            [width / 2, -1.35, 0], [width / 2 - .22, -1.35, 0]
        ]).set_stroke(INK, width=2.6)
        return VGroup(left, right, entries)

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
