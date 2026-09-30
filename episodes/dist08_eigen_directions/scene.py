"""Distribution mathematics 08: discover covariance eigenvectors by projection."""
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
    # Exact sample covariance [[2,1],[1,2]].
    return np.column_stack((np.sqrt(2) * base[:, 0],
                            base[:, 0] / np.sqrt(2) +
                            np.sqrt(1.5) * base[:, 1]))


POINTS = sample_points()
SIGMA = np.array([[2, 1], [1, 2]])
SCALE = 1.23


def projected_variance(degrees):
    v = np.array([np.cos(degrees * DEGREES), np.sin(degrees * DEGREES)])
    return float(v @ SIGMA @ v)


class CovarianceEigenDirections(Scene):
    DURATION = 42

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  08", 19, MUTED).move_to(UP * 7.3),
            txt("행렬 안에서 분포의 방향을 찾을 수 있을까?", 28).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–3.5: keep the coordinates visible until the projection transition.
        self.copy("점구름과 공분산 행렬", "Σ = [[2, 1], [1, 2]]")
        dots = self.cloud(scale=.72).shift(LEFT * 1.65)
        oval = self.oval(scale=.72).shift(LEFT * 1.65)
        axes = self.axes().scale(.63).shift(LEFT * 1.65)
        mat = self.matrix(("2", "1", "1", "2")).scale(.72).shift(RIGHT * 2.1)
        sigma = txt("Σ =", 32, ACCENT).move_to([.45, 0, 0])
        self.stage = VGroup(axes, dots, oval, mat, sigma)
        self.add(self.stage)
        self.to(3.5)

        # 3.5–7: morph the existing coordinates into the projection view.
        self.copy("방향 하나를 골라 투영", "점들을 단위방향 v 위로 내려놓습니다")
        proj = self.projection(0, connectors=True)
        self.play(Transform(axes, self.axes()), Transform(dots, self.cloud()),
                  FadeOut(oval), FadeOut(mat), FadeOut(sigma),
                  FadeIn(proj), run_time=.85)
        self.stage = VGroup(axes, dots, proj)
        self.to(7)

        # 7–10.5: rotate the viewing direction.
        self.copy("돌려보면 퍼짐이 바뀝니다", "방향마다 투영 분산이 다릅니다")
        spread = self.spread_meter(0)
        self.play(FadeIn(spread), run_time=.3)
        self.stage.add(spread)
        for angle in (22.5, 90, 135):
            self.play(Transform(proj, self.projection(angle)),
                      Transform(spread, self.spread_meter(angle)), run_time=.65)
        self.to(10.5)

        # 10.5–14.5: discover the maximum at +45 degrees.
        self.copy("가장 넓게 퍼지는 방향", "45° 방향에서 투영 분산이 최대")
        self.play(Transform(proj, self.projection(45)),
                  Transform(spread, self.spread_meter(45)), run_time=.85)
        major = Line([-2.65, -2.65, 0], [2.65, 2.65, 0],
                     color=ACCENT, stroke_width=3.5, stroke_opacity=.8)
        label = txt("v₁  /  maximum", 30, ACCENT).move_to([1.7, 3.1, 0])
        self.play(Create(major), FadeIn(label), run_time=.6)
        self.stage.add(major, label)
        self.to(14.5)

        # 14.5–18: quantify the projection from the matrix.
        self.copy("이 방향의 분산은 얼마일까?", "단위벡터 v의 투영 분산 = vᵀΣv")
        self.clear_stage()
        mat = self.matrix(("2", "1", "1", "2")).scale(.75).shift(UP * .75)
        formula = txt("Var(vᵀX) = vᵀΣv", 37, ACCENT).move_to([0, -1.7, 0])
        unit = txt("|v| = 1", 29, MUTED).move_to([0, -2.75, 0])
        self.show(VGroup(mat, formula, unit), FadeIn(mat),
                  FadeIn(formula), FadeIn(unit), run_time=.8)
        self.to(18)

        # 18–22.5: a polar direction scan finds 3 at 45 degrees.
        self.copy("모든 단위방향을 비교하면", "vᵀΣv = 2 + sin(2θ)")
        self.clear_stage()
        circle = Circle(radius=1.45, color=MUTED, stroke_width=2).move_to([-1.9, 0, 0])
        scan = self.scan_arrow(0)
        graph = self.variance_graph()
        marker = self.graph_marker(0)
        self.show(VGroup(circle, scan, graph, marker), FadeIn(circle),
                  GrowArrow(scan), FadeIn(graph), FadeIn(marker), run_time=.7)
        for angle in (20, 45):
            self.play(Transform(scan, self.scan_arrow(angle)),
                      Transform(marker, self.graph_marker(angle)), run_time=.65)
        winner = txt("max = 3  at  45°", 30, GOOD).move_to([0, -3.4, 0])
        self.play(FadeIn(winner), run_time=.35)
        self.stage.add(winner)
        self.to(22.5)

        # 22.5–26.5: applying Sigma preserves the maximum direction.
        self.copy("그 방향에 행렬을 적용하면", "Σv₁ = 3v₁  /  방향은 그대로")
        self.clear_stage()
        axes = self.axes()
        short = Arrow(ORIGIN, [1.08, 1.08, 0], buff=0,
                      color=WEIGHT, stroke_width=6)
        long = Arrow(ORIGIN, [3.24, 3.24, 0], buff=0,
                     color=ACCENT, stroke_width=6)
        line = DashedLine([-3, -3, 0], [3, 3, 0], color=ACCENT,
                          dash_length=.16, stroke_opacity=.45)
        formula = txt("Σv₁ = 3v₁", 37, ACCENT).move_to([0, -3.75, 0])
        self.show(VGroup(axes, line, short, formula), FadeIn(axes),
                  Create(line), GrowArrow(short), FadeIn(formula), run_time=.75)
        self.play(Transform(short, long), run_time=.7)
        self.to(26.5)

        # 26.5–30: name the maximum eigenpair.
        self.copy("발견한 방향의 이름", "v₁: 고유벡터     λ₁=3: 고유값")
        name = txt("Eigenvector  v₁", 33, WEIGHT).move_to([-1.7, 2.9, 0])
        value = txt("Eigenvalue  λ₁ = 3", 32, ACCENT).move_to([1.25, -2.6, 0])
        self.play(FadeIn(name), FadeIn(value), run_time=.65)
        self.stage.add(name, value)
        self.to(30)

        # 30–33.5: perpendicular minor eigenvector and variance 1.
        self.copy("수직인 또 하나의 방향", "v₂의 투영 분산은 1")
        self.clear_stage()
        cloud = self.cloud(scale=.87)
        oval = self.oval(scale=.87)
        major = Line([-3.0, -3.0, 0], [3.0, 3.0, 0],
                     color=ACCENT, stroke_width=3)
        minor = Line([-1.9, 1.9, 0], [1.9, -1.9, 0],
                     color=SPARSE, stroke_width=3)
        labels = VGroup(
            txt("v₁ : λ₁ = 3", 29, ACCENT).move_to([2.1, 3.05, 0]),
            txt("v₂ : λ₂ = 1", 29, SPARSE).move_to([-2.1, 3.05, 0]),
        )
        self.show(VGroup(cloud, oval, major, minor, labels),
                  FadeIn(cloud), Create(oval), Create(major), Create(minor),
                  FadeIn(labels), run_time=.85)
        self.to(33.5)

        # 33.5–37.5: reconstruct both axes from the matrix's two eigenpairs.
        self.copy("숫자 안에 들어 있던 두 주축", "고유벡터는 방향, 고유값은 그 방향의 분산")
        self.clear_stage()
        mat = self.matrix(("2", "1", "1", "2")).scale(.68).shift(LEFT * 2.0)
        arrow = Arrow([-.55, 0, 0], [.55, 0, 0], buff=0,
                      color=ACCENT, stroke_width=3)
        oval = self.oval(scale=.48).shift(RIGHT * 2.1)
        directions = VGroup(
            Line([.8, -1.3, 0], [3.4, 1.3, 0], color=ACCENT, stroke_width=3),
            Line([1.1, 1.0, 0], [3.1, -1.0, 0], color=SPARSE, stroke_width=3),
        )
        vals = txt("λ₁ = 3      λ₂ = 1", 27, INK).move_to([2.1, -2.2, 0])
        self.show(VGroup(mat, arrow, oval, directions, vals),
                  FadeIn(mat), GrowArrow(arrow), Create(oval),
                  Create(directions), FadeIn(vals), run_time=.85)
        self.to(37.5)

        # 37.5–42: rotate the axes; covariance becomes diagonal in this basis.
        self.copy("이 방향을 새 좌표축으로 삼으면?", "Σ → diag(3, 1)     다음: PCA")
        self.clear_stage()
        axes = self.axes()
        rotated = self.axes().rotate(45 * DEGREES)
        cloud = self.cloud(scale=.8)
        oval = self.oval(scale=.8)
        mat = self.matrix(("3", "0", "0", "1")).scale(.62).shift(DOWN * 3.5)
        question = txt("분포를 가장 잘 바라보는 방향은?", 31, INK)
        question.move_to([0, 4.1, 0])
        self.show(VGroup(axes, cloud, oval, mat, question),
                  FadeIn(axes), FadeIn(cloud), Create(oval),
                  FadeIn(mat), FadeIn(question), run_time=.75)
        self.play(Transform(axes, rotated), run_time=.85)
        self.to(42)

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

    def projection(self, degrees, connectors=False):
        v = np.array([np.cos(degrees * DEGREES), np.sin(degrees * DEGREES)])
        unit = np.array([v[0], v[1], 0])
        line = Line(-3.7 * unit, 3.7 * unit, color=ACCENT,
                    stroke_width=3, stroke_opacity=.85)
        arrow = Arrow(ORIGIN, 2.5 * unit, buff=0,
                      color=GOOD, stroke_width=5)
        dots = VGroup(*[
            Dot(SCALE * float(p @ v) * unit, radius=.075, color=GOOD)
            for p in POINTS
        ])
        guides = VGroup()
        if connectors:
            for p in POINTS[::6]:
                original = SCALE * np.array([p[0], p[1], 0])
                foot = SCALE * float(p @ v) * unit
                guides.add(DashedLine(original, foot, color=MUTED,
                                      stroke_opacity=.4, stroke_width=1.5))
        label = txt("v", 28, GOOD).move_to(2.8 * unit + .2 * UP)
        return VGroup(line, guides, dots, arrow, label)

    def spread_meter(self, degrees):
        variance = projected_variance(degrees)
        box = RoundedRectangle(width=5.4, height=.73, corner_radius=.14,
                               stroke_color=MUTED, stroke_width=1.3)
        bar = Rectangle(width=4.85 * variance / 3, height=.3,
                        fill_color=GOOD, fill_opacity=.85,
                        stroke_width=0).align_to(box, LEFT).shift(RIGHT * .27)
        label = txt(f"투영 분산  {variance:.2f}", 28, GOOD)
        label.next_to(box, UP, buff=.22)
        return VGroup(box, bar, label).move_to([0, -4.15, 0])

    def variance_graph(self):
        axes = Axes(x_range=[0, 180, 45], y_range=[1, 3.2, 1],
                    x_length=4.1, y_length=2.8, tips=False,
                    axis_config={"color": MUTED, "stroke_width": 2})
        axes.move_to([1.65, 0, 0])
        curve = axes.plot(lambda x: 2 + np.sin(2 * x * DEGREES),
                          x_range=[0, 180], color=GOOD,
                          use_smoothing=False)
        labels = VGroup(
            txt("θ", 24, INK).next_to(axes.x_axis, RIGHT, buff=.12),
            txt("vᵀΣv", 24, GOOD).next_to(axes.y_axis, UP, buff=.12),
        )
        return VGroup(axes, curve, labels)

    def graph_marker(self, degrees):
        axes = self.variance_graph()[0]
        return Dot(axes.c2p(degrees, projected_variance(degrees)),
                   radius=.12, color=ACCENT)

    def scan_arrow(self, degrees):
        t = degrees * DEGREES
        center = np.array([-1.9, 0, 0])
        return Arrow(center, center + 1.4 * np.array([np.cos(t), np.sin(t), 0]),
                     buff=0, color=ACCENT, stroke_width=5)

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
