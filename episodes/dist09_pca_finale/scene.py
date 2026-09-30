"""Distribution mathematics 09: from variance to covariance and PCA."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


def sample_points():
    angles = np.linspace(0, TAU, 24, endpoint=False)
    base = np.array([(r * np.cos(t), r * np.sin(t))
                     for r in (.65, 1.3) for t in angles])
    base /= np.sqrt(np.mean(base[:, 0] ** 2))
    return np.column_stack((np.sqrt(2) * base[:, 0],
                            base[:, 0] / np.sqrt(2) +
                            np.sqrt(1.5) * base[:, 1]))


POINTS = sample_points()
SCALE = 1.23


class WhyMatrixAndPCA(Scene):
    DURATION = 50

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  09", 19, MUTED).move_to(UP * 7.3),
            txt("왜 퍼짐은 행렬이 되고, PCA로 이어질까?", 29).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: one-dimensional spread needs one number.
        self.copy("1차원: 퍼짐은 숫자 하나", "Var(X) = σ²")
        line = Arrow([-3.25, -.15, 0], [3.25, -.15, 0], buff=0,
                     color=MUTED, stroke_width=2.7)
        dots = VGroup(*[
            Dot([x * .72, -.15 + .22 + j * .26, 0], radius=.09, color=WEIGHT)
            for x, count in zip((-3, -2, -1, 0, 1, 2, 3), (1, 2, 3, 4, 3, 2, 1))
            for j in range(count)
        ])
        mean = txt("μ", 35, ACCENT).move_to([0, -.75, 0])
        spread = DoubleArrow([-2.15, -1.5, 0], [2.15, -1.5, 0],
                             buff=0, color=GOOD, stroke_width=3)
        formula = txt("σ²", 54, GOOD).move_to([0, -2.55, 0])
        self.show(VGroup(line, dots, mean, spread, formula), FadeIn(line),
                  FadeIn(dots), FadeIn(mean), GrowArrow(spread),
                  FadeIn(formula), run_time=.85)
        self.to(4)

        # 4–8: in the plane, the same cloud has several directional spreads.
        self.copy("2차원: 보는 방향마다 다르게", "가로 · 세로 · 대각선의 퍼짐")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud(scale=.9)
        oval = self.oval(scale=.9)
        self.show(VGroup(axes, cloud, oval), FadeIn(axes), FadeIn(cloud),
                  Create(oval), run_time=.75)
        indicators = VGroup(
            Line([-2.4, 0, 0], [2.4, 0, 0], color=WEIGHT,
                 stroke_width=4, stroke_opacity=.7),
            Line([0, -2.4, 0], [0, 2.4, 0], color=SPARSE,
                 stroke_width=4, stroke_opacity=.7),
            Line([-2.65, -2.65, 0], [2.65, 2.65, 0], color=ACCENT,
                 stroke_width=4, stroke_opacity=.8),
        )
        self.play(LaggedStart(*[Create(i) for i in indicators],
                              lag_ratio=.2), run_time=1.2)
        self.stage.add(indicators)
        self.to(8)

        # 8–12: rotate a projection and show vT Sigma v changes.
        self.copy("퍼짐이 방향의 함수가 됩니다", "단위방향 v  →  투영 분산 vᵀΣv")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud()
        proj = self.projection(0)
        number = txt("vᵀΣv = 2.0", 31, GOOD).move_to([0, -4.05, 0])
        self.show(VGroup(axes, cloud, proj, number), FadeIn(axes),
                  FadeIn(cloud), FadeIn(proj), FadeIn(number), run_time=.6)
        for angle, val in ((45, "3.0"), (135, "1.0")):
            self.play(Transform(proj, self.projection(angle)),
                      Transform(number, txt(f"vᵀΣv = {val}", 31, GOOD)
                                .move_to(number)), run_time=.7)
        self.to(12)

        # 12–16: covariance matrix captures axial and joint spread.
        self.copy("그래서 퍼짐을 행렬에 담습니다", "대각선: 각자의 분산  /  양옆: 공분산")
        self.clear_stage()
        mat = self.matrix(("2", "1", "1", "2"))
        sigma = txt("Σ =", 42, ACCENT).move_to([-3.05, 0, 0])
        diag = VGroup(
            txt("Var(X)", 27, WEIGHT).move_to([-1.2, 2.5, 0]),
            txt("Var(Y)", 27, WEIGHT).move_to([1.2, -2.5, 0]),
        )
        off = txt("Cov(X,Y)", 29, GOOD).move_to([1.65, 2.5, 0])
        self.show(VGroup(mat, sigma, diag, off), FadeIn(mat),
                  FadeIn(sigma), FadeIn(diag), FadeIn(off), run_time=.85)
        self.to(16)

        # 16–20: recall the two principal axes discovered in episode 08.
        self.copy("행렬 속에서 찾은 두 주축", "v₁은 긴 방향  /  v₂는 짧은 방향")
        self.clear_stage()
        cloud = self.cloud(scale=.88)
        oval = self.oval(scale=.88)
        major = Line([-3, -3, 0], [3, 3, 0], color=ACCENT,
                     stroke_width=3.2)
        minor = Line([-1.95, 1.95, 0], [1.95, -1.95, 0],
                     color=SPARSE, stroke_width=3.2)
        labels = VGroup(
            txt("v₁   λ₁ = 3", 29, ACCENT).move_to([2.05, 3.15, 0]),
            txt("v₂   λ₂ = 1", 29, SPARSE).move_to([-2.05, 3.15, 0]),
        )
        self.show(VGroup(cloud, oval, major, minor, labels),
                  FadeIn(cloud), Create(oval), Create(major),
                  Create(minor), FadeIn(labels), run_time=.85)
        self.to(20)

        # 20–24: leave the point cloud fixed and rotate only the axes.
        self.copy("분포에 맞춰 좌표축을 돌리면", "(x, y)  →  (v₁, v₂)")
        self.clear_stage()
        axes = self.axes()
        cloud = self.cloud(scale=.85)
        oval = self.oval(scale=.85)
        self.show(VGroup(axes, cloud, oval), FadeIn(axes),
                  FadeIn(cloud), Create(oval), run_time=.7)
        rotated = self.axes().rotate(45 * DEGREES)
        rotated[0].set_color(ACCENT)
        rotated[1].set_color(SPARSE)
        self.play(Transform(axes, rotated), run_time=1.1)
        labels = VGroup(
            txt("v₁", 30, ACCENT).move_to([2.55, 2.8, 0]),
            txt("v₂", 30, SPARSE).move_to([-2.6, 2.8, 0]),
        )
        self.play(FadeIn(labels), run_time=.35)
        self.stage.add(labels)
        self.to(24)

        # 24–28: covariance is diagonal in the new coordinates.
        self.copy("새 좌표계에서는 기울기가 사라집니다", "새 공분산 행렬 = [[3, 0], [0, 1]]")
        self.clear_stage()
        before = self.matrix(("2", "1", "1", "2")).scale(.68).shift(UP * 1.55)
        arrow = Arrow([0, .15, 0], [0, -.7, 0], buff=0,
                      color=ACCENT, stroke_width=3)
        after = self.matrix(("3", "0", "0", "1")).scale(.68).shift(DOWN * 1.55)
        zeros = VGroup(
            Circle(radius=.25, color=GOOD, stroke_width=2.3).move_to(after[2][1]),
            Circle(radius=.25, color=GOOD, stroke_width=2.3).move_to(after[2][2]),
        )
        self.show(VGroup(before, arrow, after, zeros), FadeIn(before),
                  GrowArrow(arrow), FadeIn(after), Create(zeros),
                  run_time=.9)
        self.to(28)

        # 28–32: compare variances, not literal geometric axis lengths.
        self.copy("두 방향의 분산을 비교하면", "λ₁ = 3    >    λ₂ = 1")
        self.clear_stage()
        bars = VGroup(
            self.variance_bar("v₁", 3, ACCENT, 1.2),
            self.variance_bar("v₂", 1, SPARSE, -1.15),
        )
        self.show(bars, FadeIn(bars), run_time=.8)
        self.to(32)

        # 32–36: retain the major component and project to 1D.
        self.copy("작은 방향을 생략하면", "2D  →  1D    /    큰 분산 방향만 유지")
        self.clear_stage()
        cloud = self.cloud(scale=.75)
        axis = Line([-2.9, -2.9, 0], [2.9, 2.9, 0],
                    color=ACCENT, stroke_width=3)
        projected = self.projected_cloud(scale=.75)
        label = txt("z = v₁ᵀx", 31, GOOD).move_to([0, -3.65, 0])
        self.show(VGroup(cloud, axis, label), FadeIn(cloud),
                  Create(axis), FadeIn(label), run_time=.7)
        self.play(Transform(cloud, projected), run_time=1.1)
        self.to(36)

        # 36–40: name PCA after the need for it is visible.
        self.copy("주성분 분석, PCA", "큰 변동을 담는 방향부터 새 축으로 선택")
        self.clear_stage()
        cloud = self.cloud(scale=.72)
        oval = self.oval(scale=.72)
        axis = Line([-2.9, -2.9, 0], [2.9, 2.9, 0],
                    color=ACCENT, stroke_width=4)
        title = txt("PCA", 58, ACCENT).move_to([0, -3.6, 0])
        self.show(VGroup(cloud, oval, axis, title), FadeIn(cloud),
                  Create(oval), Create(axis), FadeIn(title),
                  run_time=.85)
        self.to(40)

        # 40–45: recap the entire second act as one chain.
        self.copy("2부의 한 줄 연결", "퍼짐 → 방향이 있는 퍼짐 → 고유방향 → PCA")
        self.clear_stage()
        items = VGroup(
            self.card("σ²", "1D 퍼짐", WEIGHT),
            self.card("Σ", "방향별 퍼짐", GOOD),
            self.card("v₁, v₂", "고유방향", SPARSE),
            self.card("PCA", "축을 다시 선택", ACCENT),
        ).arrange(DOWN, buff=.27).move_to([0, -.15, 0])
        arrows = VGroup(*[
            Arrow(items[i].get_bottom() + DOWN * .05,
                  items[i + 1].get_top() + UP * .05,
                  buff=0, color=MUTED, stroke_width=2.2)
            for i in range(3)
        ])
        self.show(VGroup(items, arrows),
                  LaggedStart(*[FadeIn(item) for item in items],
                              lag_ratio=.16), Create(arrows), run_time=1.2)
        self.to(45)

        # 45–50: equal Euclidean distance can mean different relative rarity.
        self.copy("다음 질문: 같은 거리일까?", "|a−μ| = |b−μ|   그런데 분포 안의 위치는 다릅니다")
        self.clear_stage()
        cloud = self.cloud(scale=.78)
        oval = self.oval(scale=.78)
        axes = self.axes()
        distance = DashedVMobject(Circle(radius=2.25, color=MUTED,
                                        stroke_width=1.8), num_dashes=40)
        a = Dot([2.25 / np.sqrt(2), 2.25 / np.sqrt(2), 0],
                radius=.16, color=GOOD)
        b = Dot([-2.25 / np.sqrt(2), 2.25 / np.sqrt(2), 0],
                radius=.16, color=PRUNE)
        labels = VGroup(
            txt("a: 안쪽", 27, GOOD).move_to([2.25, 2.4, 0]),
            txt("b: 바깥", 27, PRUNE).move_to([-2.25, 2.4, 0]),
        )
        self.show(VGroup(axes, cloud, oval, distance, a, b, labels),
                  FadeIn(axes), FadeIn(cloud), Create(oval),
                  Create(distance), FadeIn(a), FadeIn(b), FadeIn(labels),
                  run_time=.85)
        question = txt("같은 거리의 두 점은 정말 똑같이 가까울까?", 29, INK)
        question.move_to([0, -4.1, 0])
        frame = SurroundingRectangle(question, color=ACCENT, buff=.22,
                                     corner_radius=.12)
        self.play(FadeIn(question), Create(frame), run_time=.55)
        self.stage.add(question, frame)
        self.to(50)

    def projected_cloud(self, scale=.75):
        v = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
        return VGroup(*[
            Dot(SCALE * scale * float(p @ v) * np.array([v[0], v[1], 0]),
                radius=.06, color=GOOD) for p in POINTS
        ])

    def variance_bar(self, label, value, color, y):
        left = -2.2
        bar = Rectangle(width=1.22 * value, height=.58,
                        fill_color=color, fill_opacity=.75,
                        stroke_width=0).move_to([left + .61 * value, y, 0])
        baseline = Line([left, y - .39, 0], [2.4, y - .39, 0],
                        color=MUTED, stroke_width=1.4)
        text_label = txt(f"{label}    λ = {value}", 31, color)
        text_label.move_to([0, y + .72, 0])
        return VGroup(baseline, bar, text_label)

    def card(self, symbol, meaning, color):
        box = RoundedRectangle(width=5.6, height=1.15,
                               corner_radius=.16, stroke_color=color,
                               stroke_width=1.5, fill_color=color,
                               fill_opacity=.065)
        left = txt(symbol, 32, color, 1.6).move_to([-1.55, 0, 0])
        right = txt(meaning, 27, INK, 3.2).move_to([.8, 0, 0])
        return VGroup(box, left, right)

    def cloud(self, scale=1):
        return VGroup(*[Dot([SCALE * scale * x, SCALE * scale * y, 0],
                            radius=.06, color=WEIGHT) for x, y in POINTS])

    def oval(self, scale=1):
        return Ellipse(width=7.55 * scale, height=4.35 * scale,
                       color=ACCENT, stroke_width=2.1, stroke_opacity=.8,
                       fill_color=ACCENT, fill_opacity=.025).rotate(45 * DEGREES)

    def axes(self):
        return VGroup(
            Line([-3.5, 0, 0], [3.5, 0, 0], color=MUTED, stroke_width=2),
            Line([0, -3.5, 0], [0, 3.5, 0], color=MUTED, stroke_width=2),
        )

    def projection(self, degrees):
        angle = degrees * DEGREES
        v = np.array([np.cos(angle), np.sin(angle)])
        direction = np.array([v[0], v[1], 0])
        line = Line(-3.7 * direction, 3.7 * direction,
                    color=ACCENT, stroke_width=3)
        dots = VGroup(*[
            Dot(SCALE * float(p @ v) * direction, radius=.075,
                color=GOOD) for p in POINTS
        ])
        arrow = Arrow(ORIGIN, 2.5 * direction, buff=0,
                      color=GOOD, stroke_width=5)
        return VGroup(line, dots, arrow)

    def matrix(self, values):
        entries = VGroup(*[
            txt(value, 36, WEIGHT if i in (0, 3) else GOOD).move_to([
                -.78 if i % 2 == 0 else .78, .65 if i < 2 else -.65, 0])
            for i, value in enumerate(values)
        ])
        left = VMobject().set_points_as_corners([
            [-1.78, 1.35, 0], [-2, 1.35, 0], [-2, -1.35, 0],
            [-1.78, -1.35, 0]]).set_stroke(INK, width=2.5)
        right = VMobject().set_points_as_corners([
            [1.78, 1.35, 0], [2, 1.35, 0], [2, -1.35, 0],
            [1.78, -1.35, 0]]).set_stroke(INK, width=2.5)
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
