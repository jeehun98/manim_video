"""Neural Network Mathematics 02: overparameterization and solution geometry."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=2.8, height=.9, size=24, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .2))


class NeuralMathOverparameterization(Scene):
    DURATION = 116

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  02", 18, MUTED).move_to(UP * 7.3),
            label("왜 더 큰 공간에서 답을 찾는 것이 쉬울까?", 29).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–8: continue directly from episode 01.
        self.copy(
            "필요한 자유도는 훨씬 작을 수 있었습니다", "d intrinsic  ≪  D",
            "전체 파라미터 수보다 훨씬 적은 자유도만으로도\n신경망은 학습될 수 있었습니다.",
        )
        outer = RoundedRectangle(width=7.0, height=5.0, corner_radius=.3,
                                 stroke_color=MUTED, stroke_width=2,
                                 fill_color=MUTED, fill_opacity=.02)
        plane = Polygon([-3.0, -1.0, 0], [1.65, -2.0, 0], [3.0, 1.2, 0], [-1.6, 2.2, 0],
                        color=SPARSE, fill_color=SPARSE, fill_opacity=.16)
        formula = label("θ ∈ ℝᴰ", 31, INK).move_to([0, 3.05, 0])
        small = label("trainable subspace  ℝᵈ", 21, SPARSE).move_to([0, -2.55, 0])
        self.show(VGroup(outer, plane, formula, small))
        self.to(8)

        # 8–16: reverse the apparent waste into the episode question.
        self.copy(
            "그렇다면 큰 공간은 낭비일까요?", "WASTE  OR  ADVANTAGE?",
            "거대한 공간은 단순한 낭비일까요?\n오히려 큰 공간 때문에 답을 찾기 쉬워지는 것은 아닐까요?",
        )
        left = card("D ≫ d", MUTED, 2.5, 1.15, 31).move_to([-2.0, .35, 0])
        right = card("easier search ?", ACCENT, 3.5, 1.15, 27, .16).move_to([1.75, .35, 0])
        arrow = Arrow(left.get_right(), right.get_left(), buff=.25,
                      color=ACCENT, stroke_width=4, tip_length=.2)
        question = VGroup(left, arrow, right)
        backdrop = self.radial_axes(18)
        self.show(VGroup(backdrop, question))
        self.to(16)

        # 16–24: an isolated optimum is a tiny target.
        self.copy(
            "답이 정확히 한 점이라면", "ISOLATED OPTIMUM  θ*",
            "좋은 모델이 정확히 한 점에만 존재한다면\n학습은 작은 목표를 정확히 찾아가는 문제입니다.",
        )
        axes = self.axes_2d()
        optimum = Dot([1.7, 1.2, 0], radius=.12, color=GOOD)
        halo = Circle(radius=.38, color=GOOD, stroke_opacity=.3).move_to(optimum)
        path = VMobject(color=ACCENT, stroke_width=4)
        path.set_points_smoothly([[-2.7, -1.4, 0], [-1.8, .5, 0], [-.5, -.25, 0],
                                  [.55, .9, 0], [1.7, 1.2, 0]])
        point = Dot(path.get_start(), radius=.11, color=ACCENT)
        tag = label("θ*", 24, GOOD).next_to(optimum, UP, buff=.2)
        self.show(VGroup(axes, path, point, optimum, halo, tag))
        self.play(MoveAlongPath(point, path), run_time=1.6, rate_func=smooth)
        self.to(24)

        # 24–32: enlarging the ambient box does not enlarge an isolated target.
        self.copy(
            "공간만 커지면 표적은 더 작아 보입니다", "BIGGER SPACE  ≠  BIGGER TARGET",
            "공간이 커진다고 이런 점을 찾는 일이\n저절로 쉬워지지는 않습니다.",
        )
        boxes = VGroup(*[
            Square(side_length=s, color=MUTED, stroke_opacity=.18 + .12 * i)
            for i, s in enumerate((1.4, 3.0, 5.2, 7.0))
        ])
        target = Dot(ORIGIN, radius=.11, color=GOOD)
        rings = VGroup(*[Circle(radius=r, color=GOOD, stroke_opacity=.18)
                         for r in (.3, .5)])
        scale_tag = label("ambient space ↑", 24, MUTED).move_to([0, -3.0, 0])
        self.show(VGroup(boxes, rings, target, scale_tag))
        self.play(*[box.animate.set_stroke(opacity=.08 + .08 * i)
                    for i, box in enumerate(boxes)], run_time=1.0)
        self.to(32)

        # 32–42: same functional condition, several parameter choices.
        self.copy(
            "같은 결과를 만드는 파라미터는 여러 개입니다", "w₁w₂ = 1",
            "w₁w₂=1이면 (1,1), (2,1/2), (4,1/4)는\n모두 같은 조건을 만족하는 답입니다.",
        )
        axes = self.axes_2d(x_name="w₁", y_name="w₂")
        curve = self.hyperbola_curve()
        samples = VGroup()
        for x, y, text_value in ((1, 1, "(1, 1)"), (2, .5, "(2, 1/2)"), (4, .25, "(4, 1/4)")):
            p = self.coord(x, y)
            dot = Dot(p, radius=.09, color=ACCENT)
            tag = label(text_value, 17, ACCENT).next_to(dot, UP, buff=.12)
            samples.add(VGroup(dot, tag))
        formula = card("w₁w₂ = 1", GOOD, 2.6, .75, 25, .12).move_to([1.95, 2.65, 0])
        self.show(VGroup(axes, curve, samples, formula))
        self.to(42)

        # 42–50: emphasize a continuous solution set, not a linear subspace.
        self.copy(
            "답은 고립된 점이 아닐 수 있습니다", "SOLUTION SET  /  MANIFOLD-LIKE",
            "답은 고립된 점이 아니라\n연속적인 해 집합으로 나타날 수 있습니다.",
        )
        dots = VGroup(*[Dot(self.coord(x, 1 / x), radius=.065, color=GOOD)
                        for x in np.linspace(.42, 4.7, 26)])
        curve = self.hyperbola_curve(color=GOOD, width=7)
        point = Dot(self.coord(1, 1), radius=.17, color=ACCENT)
        point_tag = label("one solution", 20, ACCENT).next_to(point, LEFT, buff=.25)
        set_tag = label("continuous family of solutions", 23, GOOD).move_to([0, -2.65, 0])
        self.show(VGroup(self.axes_2d(x_name="w₁", y_name="w₂"), curve,
                         dots, point, point_tag, set_tag))
        self.to(50)

        # 50–60: add a parameter axis but not another constraint.
        self.copy(
            "변수 하나를 더 추가해봅시다", "ℝ²  →  ℝ³",
            "추가된 자유도가 모두\n새로운 조건을 만드는 것은 아닙니다.",
        )
        curve2d = self.hyperbola_curve(color=GOOD, width=6).scale(.8).shift(LEFT * 1.65)
        z_axis = Arrow([1.35, -2.1, 0], [3.15, 1.8, 0], buff=0,
                       color=WEIGHT, stroke_width=2.5, tip_length=.16)
        copies = VGroup(*[
            curve2d.copy().shift(np.array([.18 * i, .38 * i, 0])).set_stroke(opacity=.18 + .1 * i)
            for i in range(7)
        ])
        ribbons = VGroup(*[
            Line(curve2d.point_from_proportion(t),
                 curve2d.point_from_proportion(t) + np.array([1.08, 2.28, 0]),
                 color=SPARSE, stroke_opacity=.35)
            for t in np.linspace(.06, .94, 9)
        ])
        labels = VGroup(
            label("solution curve", 20, GOOD).move_to([-1.8, -2.45, 0]),
            label("extra parameter direction", 19, WEIGHT).move_to([2.05, 2.5, 0]),
        )
        self.show(VGroup(copies, ribbons, z_axis, labels))
        self.to(60)

        # 60–68: surface and abstract high-dimensional solution freedom.
        self.copy(
            "여분의 방향이 해 집합을 확장할 수 있습니다", "ℝ³  →  ℝᴰ",
            "같은 답을 표현할 여분의 방향이 생기면\n해 집합은 더 높은 차원으로 확장될 수 있습니다.",
        )
        surface = self.solution_surface()
        dimensions = VGroup(
            card("D = 2", MUTED, 1.7, .65, 19),
            label("→", 25, MUTED),
            card("D = 3", SPARSE, 1.7, .65, 19, .12),
            label("→", 25, MUTED),
            card("D ≫ 3", ACCENT, 1.9, .65, 19, .12),
        ).arrange(RIGHT, buff=.18).move_to([0, -2.75, 0])
        self.show(VGroup(surface, dimensions))
        self.to(68)

        # 68–77: the apparent paradox.
        self.copy(
            "큰 공간의 역설", "SEARCH SPACE ↑   ·   SOLUTION SET ↑",
            "탐색할 공간은 커졌지만\n답이 존재할 수 있는 구조도 커졌습니다.",
        )
        left = VGroup(
            RoundedRectangle(width=3.0, height=4.5, corner_radius=.2,
                             color=MUTED, stroke_width=2),
            Dot([0, .2, 0], radius=.1, color=GOOD),
            label("small target", 20, MUTED).move_to([0, -2.7, 0]),
        ).move_to([-2.15, .25, 0])
        right_frame = RoundedRectangle(width=3.5, height=4.5, corner_radius=.2,
                                       color=SPARSE, stroke_width=2)
        band = Polygon([-1.5, -.6, 0], [1.15, -1.7, 0], [1.55, 1.0, 0], [-1.1, 1.85, 0],
                       color=GOOD, fill_color=GOOD, fill_opacity=.16).move_to([2.05, .25, 0])
        right = VGroup(right_frame.move_to([2.05, .25, 0]), band,
                       label("larger target set", 20, GOOD).move_to([2.05, -2.7, 0]))
        self.show(VGroup(left, right))
        self.to(77)

        # 77–87: multiple starting points can hit different parts of the set.
        self.copy(
            "과매개변수화는 도달할 길을 늘릴 수 있습니다", "OVERPARAMETERIZATION  ·  MORE WAYS TO ARRIVE",
            "여분의 차원은 여러 초기점이 서로 다른 위치의 해에\n도달할 수 있는 구조를 만들어줄 수 있습니다.",
        )
        surface = self.solution_surface(opacity=.2)
        paths = VGroup()
        starts = ((-3.0, -2.25), (-2.7, 2.5), (2.9, -2.2), (3.0, 2.25))
        ends = ((-.9, -.55), (-.55, 1.05), (.75, -.2), (1.0, .9))
        for (sx, sy), (ex, ey), color in zip(starts, ends, (WEIGHT, ACCENT, PRUNE, SPARSE)):
            path = VMobject(color=color, stroke_width=3.5)
            path.set_points_smoothly([[sx, sy, 0], [(sx + ex) * .45, sy * .35, 0], [ex, ey, 0]])
            paths.add(VGroup(path, Dot([sx, sy, 0], radius=.08, color=color),
                             Dot([ex, ey, 0], radius=.085, color=GOOD)))
        self.show(VGroup(surface, paths))
        self.to(87)

        # 87–97: state the idealized local dimension count.
        self.copy(
            "차원을 세면 직관이 더 선명해집니다", "LOCAL + IDEALIZED DIMENSION COUNT",
            "regular한 해 근처에 r개의 독립 제약이 있다면\ndim(S) ≈ D-r라는 차원 계수 직관을 얻습니다.",
        )
        ambient = card("parameter space", MUTED, 5.7, .8, 22).move_to([0, 2.35, 0])
        formula = card("dim(S)  ≈  D  −  r", ACCENT, 5.7, 1.15, 34, .16).move_to([0, .45, 0])
        conditions = VGroup(
            card("D variables", WEIGHT, 2.2, .7, 20),
            card("r independent constraints", PRUNE, 3.45, .7, 18),
        ).arrange(RIGHT, buff=.35).move_to([0, -1.15, 0])
        caveat = label("near a regular solution  ·  Jacobian rank r", 19, MUTED)
        caveat.move_to([0, -2.35, 0])
        self.show(VGroup(ambient, formula, conditions, caveat))
        self.to(97)

        # 97–106: line versus surface for one independent constraint.
        self.copy(
            "변수는 늘고 조건은 그대로라면", "D − r  INCREASES",
            "D=2, r=1이면 선처럼, D=3, r=1이면\n면처럼 답의 자유도가 남을 수 있습니다.",
        )
        left = self.dimension_example(2, 1, "dim(S) = 1", False).move_to([-2.05, .25, 0])
        right = self.dimension_example(3, 1, "dim(S) = 2", True).move_to([2.05, .25, 0])
        divider = Line([0, 2.8, 0], [0, -2.5, 0], color=MUTED, stroke_opacity=.3)
        self.show(VGroup(left, right, divider))
        self.to(106)

        # 106–116: overparameterization helps, but landscape geometry is next.
        self.copy(
            "하지만 해 집합의 크기만으로는 부족합니다", "L(θ)  ·  GEOMETRY MATTERS",
            "답이 넓다고 학습이 자동으로 쉽지는 않습니다.\n그 답으로 향하는 loss 지형도 중요합니다.",
        )
        terrain = self.loss_terrain()
        lambdas = card("λ₁ ≫ λ₂ ≈ 0", ACCENT, 3.6, .85, 29, .14).move_to([0, -2.2, 0])
        question = label("모든 방향은 정말 같은 역할을 할까?", 27, INK).move_to([0, 2.75, 0])
        self.show(VGroup(terrain, lambdas, question))
        self.to(116)

    def axes_2d(self, x_name="θ₁", y_name="θ₂"):
        x = Arrow([-3.25, -2.25, 0], [3.35, -2.25, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.14)
        y = Arrow([-3.0, -2.5, 0], [-3.0, 2.75, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.14)
        return VGroup(x, y, label(x_name, 19, MUTED).move_to([3.35, -2.58, 0]),
                      label(y_name, 19, MUTED).move_to([-3.35, 2.7, 0]))

    def coord(self, x, y):
        return np.array([-2.85 + 1.25 * x, -2.15 + 1.03 * y, 0])

    def hyperbola_curve(self, color=GOOD, width=5):
        curve = VMobject(color=color, stroke_width=width)
        points = [self.coord(x, 1 / x) for x in np.linspace(.38, 4.75, 65)]
        curve.set_points_smoothly(points)
        return curve

    def radial_axes(self, count):
        axes = VGroup()
        for i in range(count):
            angle = TAU * i / count
            length = 2.4 + .55 * (i % 3)
            end = [length * np.cos(angle), .72 * length * np.sin(angle), 0]
            axes.add(Line(ORIGIN, end, color=MUTED, stroke_width=1.2,
                          stroke_opacity=.22))
        return axes

    def solution_surface(self, opacity=.16):
        plane = Polygon([-2.8, -1.15, 0], [1.65, -2.1, 0], [2.85, 1.2, 0], [-1.6, 2.15, 0],
                        color=GOOD, fill_color=GOOD, fill_opacity=opacity,
                        stroke_width=3)
        grid = VGroup()
        for t in np.linspace(.12, .88, 5):
            a = interpolate(plane.get_vertices()[0], plane.get_vertices()[3], t)
            b = interpolate(plane.get_vertices()[1], plane.get_vertices()[2], t)
            grid.add(Line(a, b, color=GOOD, stroke_opacity=.25))
        for t in np.linspace(.12, .88, 5):
            a = interpolate(plane.get_vertices()[0], plane.get_vertices()[1], t)
            b = interpolate(plane.get_vertices()[3], plane.get_vertices()[2], t)
            grid.add(Line(a, b, color=GOOD, stroke_opacity=.25))
        return VGroup(plane, grid, label("solution surface", 22, GOOD).move_to([0, 2.7, 0]))

    def dimension_example(self, d, r, result, surface):
        frame = RoundedRectangle(width=3.35, height=4.8, corner_radius=.22,
                                 color=SPARSE if surface else WEIGHT, stroke_width=2)
        title = label(f"D = {d},  r = {r}", 23, INK).move_to([0, 1.85, 0])
        if surface:
            shape = Polygon([-1.2, -.65, 0], [.75, -1.15, 0], [1.2, .55, 0], [-.75, 1.0, 0],
                            color=GOOD, fill_color=GOOD, fill_opacity=.2)
        else:
            shape = Line([-1.15, -.85, 0], [1.15, .85, 0], color=GOOD, stroke_width=7)
        answer = label(result, 23, ACCENT).move_to([0, -1.85, 0])
        return VGroup(frame, title, shape, answer)

    def loss_terrain(self):
        curves = VGroup()
        for i, y in enumerate(np.linspace(-1.25, 1.25, 7)):
            curve = VMobject(color=WEIGHT if i != 3 else GOOD,
                             stroke_width=2.2 if i != 3 else 5)
            points = []
            for x in np.linspace(-2.8, 2.8, 25):
                height = .24 * (x ** 2) + .12 * np.sin(2.2 * x + i)
                points.append([x, y * .55 + height - .75, 0])
            curve.set_points_smoothly(points)
            curves.add(curve)
        steep = Arrow([-2.0, -.2, 0], [-.8, 1.45, 0], buff=0,
                      color=PRUNE, stroke_width=3, tip_length=.17)
        flat = Arrow([-.45, -.05, 0], [1.8, .05, 0], buff=0,
                     color=GOOD, stroke_width=3, tip_length=.17)
        tags = VGroup(label("steep", 20, PRUNE).next_to(steep, LEFT, buff=.15),
                      label("flat", 20, GOOD).next_to(flat, DOWN, buff=.15))
        return VGroup(curves, steep, flat, tags)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2,
            fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note),
                  FadeIn(self.caption_box), FadeIn(self.caption), run_time=.2)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
