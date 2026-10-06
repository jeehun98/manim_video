"""Neural Network Mathematics 13: training as dynamics in parameter space."""

import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import (
    ACCENT,
    GOOD,
    INK,
    MUTED,
    PRUNE,
    SPARSE,
    WEIGHT,
    ZERO,
    configure_vertical,
    text,
)

configure_vertical()


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return text(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=0.82, size=23, fill=0.11):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - 0.22))


class NeuralMathGradientDynamics(Scene):
    DURATION = 147
    ORIGIN = np.array([0.0, 0.45, 0.0])
    XSCALE = 1.02
    YSCALE = 0.78
    QUADRATIC = np.array([[0.52, 0.30], [0.30, 1.18]])

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  13", 18, MUTED).move_to(UP * 7.3),
            label("신경망 학습을 동역학계로 보면 보이는 것", 27).move_to(UP * 6.46),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=0.35),
        )
        self.progress = Rectangle(
            width=0.01,
            height=0.035,
            fill_color=ACCENT,
            fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.chrome.set_z_index(100)
        self.progress.set_z_index(101)
        self.add(self.chrome, self.progress)
        self.add_foreground_mobjects(self.chrome, self.progress)

        # 00:00–00:06 — Familiar ball-on-a-surface picture.
        self.copy(
            "익숙한 공 하나의 그림",
            "L(θ)",
            "Gradient Descent는 흔히 공이 Loss 지형을\n아래로 굴러가는 모습으로 설명됩니다.",
        )
        surface = self.surface_mesh()
        start = np.array([-2.65, 1.65])
        path = self.surface_trajectory(start)
        ball = Dot(path.get_start(), radius=0.11, color=ACCENT)
        minimum = Dot(self.surface_point(np.zeros(2)), radius=0.07, color=GOOD)
        minimum_ring = Circle(radius=0.22, color=GOOD, stroke_width=2).move_to(minimum)
        self.show(VGroup(surface, path.set_stroke(opacity=0.35), ball, minimum, minimum_ring))
        self.play(MoveAlongPath(ball, path), run_time=2.8, rate_func=smooth)
        self.play(Indicate(minimum_ring, color=GOOD), run_time=0.8)
        self.to(6)

        # 00:06–00:16 — Change viewpoint and expose the local gradient.
        self.copy(
            "공 하나가 아니라 공간 전체를 봅니다",
            "θₜ₊₁ = θₜ − η∇L(θₜ)",
            "gradient는 가장 빠른 증가 방향이고,\nGradient Descent는 그 반대로 움직입니다.",
        )
        contours = self.quadratic_contours()
        theta = Dot(self.p2s(np.array([-2.05, 1.35])), radius=0.12, color=ACCENT)
        vector = self.arrow_at(self.single_grad, np.array([-2.05, 1.35]), ACCENT, 0.78)
        tag = label("−∇L(θ)", 23, ACCENT).next_to(vector, UP, buff=0.13)
        equation = card("θₜ₊₁ = θₜ − η∇L(θₜ)", ACCENT, 5.6, 0.8, 24, 0.12)
        equation.move_to([0, -2.95, 0])
        self.show(VGroup(contours, theta, vector, tag, equation))
        self.play(GrowArrow(vector), FadeIn(tag), run_time=1.2)
        self.to(16)

        # 00:16–00:26 — Fill the whole space with arrows.
        self.copy(
            "모든 위치에 화살표를 그립니다",
            "VECTOR FIELD   F(θ) = −∇L(θ)",
            "모든 위치에서 -∇L을 그리면\n공간 전체에 하나의 방향장이 생깁니다.",
        )
        field = self.vector_field(self.single_grad, color=WEIGHT)
        self.show(VGroup(self.plane_grid(), self.quadratic_contours(0.34), field))
        self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.018), run_time=2.2)
        self.to(26)

        # 00:26–00:32 — Several initial conditions trace trajectories.
        self.copy(
            "학습은 이 흐름을 따라갑니다",
            "CURRENT STATE  →  NEXT STATE  →  TRAJECTORY",
            "각 점은 현재 위치의 방향만 보고 움직입니다.\n그 작은 이동의 반복이 학습 경로가 됩니다.",
        )
        starts = [(-2.8, 2.4), (-2.9, -1.8), (-1.4, 2.65), (1.55, -2.5), (2.8, 1.8), (2.9, -0.9)]
        paths = VGroup(*[self.flow_path(self.single_grad, p, steps=125) for p in starts])
        dots = VGroup(*[Dot(path.get_start(), radius=0.085, color=c) for path, c in zip(
            paths, [WEIGHT, ACCENT, GOOD, SPARSE, PRUNE, INK]
        )])
        base = VGroup(self.quadratic_contours(0.26), self.vector_field(self.single_grad, color=MUTED, opacity=0.45))
        self.show(VGroup(base, paths.set_stroke(opacity=0.66), dots))
        self.play(*[MoveAlongPath(dot, path) for dot, path in zip(dots, paths)], run_time=3.2, rate_func=linear)
        self.to(32)

        # 00:32–00:44 — Discrete steps become gradient flow.
        self.copy(
            "step을 줄이면 부드러운 흐름이 됩니다",
            "GRADIENT DESCENT  →  GRADIENT FLOW",
            "유한한 step을 매우 작게 생각하면\nθ̇=-∇L(θ)인 연속적인 흐름으로 볼 수 있습니다.",
        )
        smooth_path = self.flow_path(self.single_grad, (-2.75, 2.05), steps=150)
        proportions = np.linspace(0, 1, 8)
        discrete = VGroup(*[
            Dot(smooth_path.point_from_proportion(float(t)), radius=0.09, color=ACCENT)
            for t in proportions
        ])
        step_arrows = VGroup(*[
            Arrow(discrete[i].get_center(), discrete[i + 1].get_center(), buff=0.08,
                  color=ACCENT, stroke_width=3, tip_length=0.14)
            for i in range(len(discrete) - 1)
        ])
        formula_a = card("θₜ₊₁ = θₜ − η∇L(θₜ)", ACCENT, 5.7, 0.72, 22, 0.10).move_to([0, -2.65, 0])
        group = VGroup(self.quadratic_contours(0.28), discrete, step_arrows, formula_a)
        self.show(group)
        dense = self.path_dots(smooth_path, 30, WEIGHT)
        formula_b = card("θ̇ = −∇L(θ)", WEIGHT, 4.2, 0.72, 24, 0.12).move_to(formula_a)
        self.play(ReplacementTransform(discrete, dense), FadeOut(step_arrows),
                  Transform(formula_a, formula_b), run_time=2.0)
        self.play(Create(smooth_path.set_color(WEIGHT)), run_time=1.3)
        self.stage.add(smooth_path)
        self.to(44)

        # 00:44–00:50 — Same destination, different paths.
        self.copy(
            "목적지는 같아도 경로는 다릅니다",
            "INITIAL CONDITION + VECTOR FIELD → TRAJECTORY",
            "출발점이 다르면 처음 만나는 gradient와\n그 다음 상태가 달라집니다.",
        )
        starts = [(-3.0, 2.2), (-2.65, -2.25), (0.2, 2.75), (2.8, 1.8), (2.6, -2.4)]
        paths = VGroup(*[self.flow_path(self.single_grad, p, steps=140) for p in starts])
        dots = VGroup(*[Dot(path.get_start(), radius=0.08, color=ACCENT) for path in paths])
        minimum = Dot(self.p2s(np.zeros(2)), radius=0.14, color=GOOD)
        self.show(VGroup(self.quadratic_contours(0.28), paths.set_stroke(color=WEIGHT, opacity=0.72), dots, minimum))
        self.play(*[MoveAlongPath(dot, path) for dot, path in zip(dots, paths)], run_time=2.7, rate_func=linear)
        self.to(50)

        # 00:50–00:57 — Basins split the parameter space.
        self.copy(
            "공간이 목적지별로 나뉩니다",
            "BASIN OF ATTRACTION",
            "같은 attractor로 흘러가는 초기조건의 영역을\nBasin of Attraction이라고 부릅니다.",
        )
        basin = self.basin_background()
        minima = VGroup(
            Dot(self.p2s(np.array([-1.5, 0])), radius=0.15, color=WEIGHT),
            Dot(self.p2s(np.array([1.5, 0])), radius=0.15, color=SPARSE),
        )
        starts = [(-3.0, 2.4), (-2.7, 0.3), (-2.3, -2.25), (-0.7, 2.55),
                  (0.65, -2.5), (1.5, 2.5), (2.6, -0.3), (3.0, 1.7)]
        paths = VGroup(*[self.flow_path(self.double_grad, p, steps=145, dt=0.024) for p in starts])
        dots = VGroup(*[
            Dot(path.get_start(), radius=0.075, color=WEIGHT if p[0] < 0 else SPARSE)
            for p, path in zip(starts, paths)
        ])
        labels = VGroup(
            label("Basin A", 25, WEIGHT).move_to([-2.1, 3.75, 0]),
            label("Basin B", 25, SPARSE).move_to([2.1, 3.75, 0]),
        )
        self.show(VGroup(basin, self.double_contours(), paths.set_stroke(opacity=0.55), dots, minima, labels))
        self.play(*[MoveAlongPath(dot, path) for dot, path in zip(dots, paths)], run_time=3.3, rate_func=linear)
        self.to(57)

        # 00:57–01:05 — Zoom attention to the boundary saddle.
        self.copy(
            "두 basin의 경계에 있는 점",
            "BASIN BOUNDARY  ·  SADDLE",
            "경계에는 한 방향과 다른 방향의 행동이\n전혀 다른 saddle point가 놓일 수 있습니다.",
        )
        boundary = DashedLine([0, -2.45, 0], [0, 3.65, 0], color=PRUNE, stroke_width=3)
        saddle = Dot(self.p2s(np.zeros(2)), radius=0.15, color=PRUNE)
        spotlight = Circle(radius=0.55, color=PRUNE, stroke_width=3).move_to(saddle)
        stage = VGroup(self.basin_background(), self.double_contours(), boundary, saddle, spotlight,
                       label("saddle", 25, PRUNE).next_to(spotlight, RIGHT, buff=0.2))
        self.show(stage)
        self.play(Indicate(spotlight, color=PRUNE, scale_factor=1.18), run_time=1.2)
        self.to(65)

        # 01:05–01:15 — Canonical saddle field.
        self.copy(
            "한 방향에서는 끌고, 다른 방향에서는 밉니다",
            "L(x,y) = x² − y²",
            "x축에서는 원점으로 접근하지만\ny축 방향에서는 원점에서 멀어집니다.",
        )
        saddle_surface = self.saddle_mesh()
        formula = card("L(x,y) = x² − y²", PRUNE, 4.8, 0.72, 24, 0.11).move_to([0, -2.85, 0])
        self.show(VGroup(saddle_surface, formula))
        saddle_field = self.vector_field(self.saddle_grad, color=PRUNE, xlim=2.8, ylim=2.7)
        axes = self.axis_cross()
        self.play(ReplacementTransform(saddle_surface, VGroup(axes, saddle_field)), run_time=1.8)
        # ReplacementTransform adds its target to the scene, but the target is not
        # automatically substituted inside self.stage. Track it explicitly so the
        # following self.show() fades the axes and yellow saddle field out as well.
        self.stage = VGroup(axes, saddle_field, formula)
        starts = [(-2.7, 0), (2.7, 0), (-1.9, 0.14), (1.9, -0.14), (0, 0.55), (0, -0.55)]
        paths = VGroup(*[self.flow_path(self.saddle_grad, p, steps=75, dt=0.026, stop_radius=None) for p in starts])
        dots = VGroup(*[Dot(path.get_start(), radius=0.075, color=ACCENT) for path in paths])
        self.add(paths.set_stroke(color=ACCENT, opacity=0.55), dots)
        self.stage.add(paths, dots)
        self.play(*[MoveAlongPath(dot, path) for dot, path in zip(dots, paths)], run_time=2.6, rate_func=linear)
        self.to(75)

        # 01:15–01:23 — Stable and unstable directions.
        self.copy(
            "Stable / Unstable Direction",
            "STABLE MANIFOLD = SPECIAL INITIAL CONDITIONS",
            "정확히 stable direction 위에 놓인 시작점은 saddle로 가지만,\n조금만 벗어나도 unstable direction으로 빠져나갑니다.",
        )
        stable = DoubleArrow([-3.25, 0.45, 0], [3.25, 0.45, 0], buff=0,
                             color=WEIGHT, stroke_width=5, tip_length=0.2)
        unstable = DoubleArrow([0, -2.5, 0], [0, 3.4, 0], buff=0,
                               color=PRUNE, stroke_width=5, tip_length=0.2)
        center = Dot(self.ORIGIN, radius=0.14, color=ACCENT)
        stable_tag = label("Stable Direction", 23, WEIGHT).move_to([0, 1.0, 0])
        unstable_tag = label("Unstable Direction", 23, PRUNE).rotate(PI / 2).move_to([0.48, 2.25, 0])
        manifold = DashedLine([-3.4, 0.45, 0], [3.4, 0.45, 0], color=GOOD, stroke_width=7)
        manifold.set_stroke(opacity=0.4)
        self.show(VGroup(self.axis_cross(), manifold, stable, unstable, center, stable_tag, unstable_tag))
        near_path = self.flow_path(self.saddle_grad, (-2.6, 0.10), steps=90, dt=0.025, stop_radius=None)
        near_dot = Dot(near_path.get_start(), radius=0.085, color=ACCENT)
        self.add(near_path.set_stroke(color=ACCENT, opacity=0.65), near_dot)
        self.stage.add(near_path, near_dot)
        self.play(MoveAlongPath(near_dot, near_path), run_time=2.2, rate_func=linear)
        self.to(83)

        # 01:23–01:32 — A stable minimum as an attractor.
        self.copy(
            "주변의 흐름을 받아들이는 상태",
            "ATTRACTOR",
            "주변에서 안정적인 local minimum은 Gradient Flow의\nattractor처럼 동작할 수 있습니다.",
        )
        starts = [(2.8, 2.2), (-2.7, 2.3), (-2.8, -2.1), (2.7, -2.3), (0.2, 2.8), (3.1, 0.2)]
        paths = VGroup(*[self.flow_path(self.single_grad, p, steps=135) for p in starts])
        dots = VGroup(*[Dot(path.get_start(), radius=0.075, color=WEIGHT) for path in paths])
        center = Dot(self.p2s(np.zeros(2)), radius=0.16, color=GOOD)
        halo = Circle(radius=0.42, color=GOOD, stroke_width=3).move_to(center)
        self.show(VGroup(self.quadratic_contours(0.30), paths.set_stroke(color=WEIGHT, opacity=0.6), dots,
                         center, halo, label("Attractor", 27, GOOD).next_to(halo, DOWN, buff=0.2)))
        self.play(*[MoveAlongPath(dot, path) for dot, path in zip(dots, paths)], run_time=2.7, rate_func=linear)
        self.to(92)

        # 01:32–01:40 — Gradient trajectory is not a shortest path.
        self.copy(
            "학습은 최단거리로 가지 않습니다",
            "LOCAL DIRECTION ≠ GLOBAL SHORTEST PATH",
            "목적지의 위치를 직접 아는 것이 아니라\n현재 위치의 gradient만 따르기 때문에 경로는 휘어집니다.",
        )
        start = np.array([-2.9, 2.5])
        end = self.p2s(np.zeros(2))
        path = self.flow_path(self.single_grad, start, steps=145)
        straight = DashedLine(self.p2s(start), end, color=MUTED, stroke_width=3)
        dot = Dot(path.get_start(), radius=0.09, color=ACCENT)
        self.show(VGroup(self.quadratic_contours(0.25), straight,
                         label("Shortest path", 21, MUTED).next_to(straight, LEFT, buff=0.12),
                         path.set_stroke(color=WEIGHT, width=5), dot,
                         label("Gradient trajectory", 22, WEIGHT).move_to([1.7, 2.8, 0])))
        self.play(MoveAlongPath(dot, path), run_time=2.8, rate_func=linear)
        self.to(100)

        # 01:40–01:48 — Step size changes the discrete dynamics.
        self.copy(
            "Step Size는 dynamics를 바꿉니다",
            "η ↑   STABLE → OSCILLATION → DIVERGENCE",
            "작은 step은 흐름을 따르지만, 너무 크면\nminimum을 지나쳐 진동하거나 발산할 수 있습니다.",
        )
        panels = VGroup(
            self.step_panel(0.35, "small η", GOOD),
            self.step_panel(1.35, "large η", ACCENT),
            self.step_panel(2.15, "too large", PRUNE),
        ).arrange(DOWN, buff=0.48).move_to([0, 0.55, 0])
        self.show(panels)
        self.play(LaggedStart(*[ShowIncreasingSubsets(panel[2]) for panel in panels], lag_ratio=0.25), run_time=2.5)
        self.to(108)

        # 01:48–01:59 — High-dimensional parameter space.
        self.copy(
            "실제 공간에는 축이 훨씬 많습니다",
            "θ₁, θ₂, θ₃, …, θₙ",
            "2D 그림은 수백만, 수십억 차원일 수 있는\n실제 dynamics의 작은 단면입니다.",
        )
        origin = np.array([0, 0.35, 0])
        directions = [RIGHT, UP, normalize(RIGHT + UP), normalize(LEFT + UP),
                      normalize(2 * RIGHT - UP), normalize(LEFT - 1.4 * UP)]
        axes = VGroup(*[
            Arrow(origin, origin + d * (2.1 + 0.18 * i), buff=0, color=c, stroke_width=3, tip_length=0.18)
            for i, (d, c) in enumerate(zip(directions, [WEIGHT, SPARSE, GOOD, ACCENT, PRUNE, MUTED]))
        ])
        tags = VGroup(*[
            label(f"θ{i + 1}" if i < 5 else "… θₙ", 22, axis.get_color()).next_to(axis.get_end(), axis.get_vector(), buff=0.08)
            for i, axis in enumerate(axes)
        ])
        core = Dot(origin, radius=0.12, color=INK)
        self.show(VGroup(axes, tags, core, card("millions to billions of dimensions", SPARSE, 6.5, 0.76, 22, 0.1).move_to([0, -2.7, 0])))
        self.play(LaggedStart(*[GrowArrow(axis) for axis in axes], lag_ratio=0.12), run_time=1.6)
        self.to(119)

        # 01:59–02:06 — SGD noise perturbs the smooth path.
        self.copy(
            "SGD에서는 경로가 조금씩 흔들립니다",
            "MINI-BATCH GRADIENT = FULL GRADIENT + NOISE",
            "실제 학습은 매끈한 흐름보다\nvector field 주변을 흔들리며 이동하는 경로에 가깝습니다.",
        )
        reference_path = self.flow_path(self.single_grad, (-2.9, 2.4), steps=120)
        noisy = self.noisy_path(reference_path)
        reference_path.set_stroke(color=MUTED, width=3, opacity=0.65)
        noisy.set_stroke(color=ACCENT, width=5)
        dot = Dot(noisy.get_start(), radius=0.09, color=ACCENT)
        self.show(VGroup(self.quadratic_contours(0.25), reference_path, noisy, dot,
                         label("Gradient Flow", 20, MUTED).move_to([-2.2, -2.6, 0]),
                         label("SGD", 22, ACCENT).move_to([2.2, -2.6, 0])))
        self.play(MoveAlongPath(dot, noisy), run_time=2.7, rate_func=linear)
        self.to(126)

        # 02:06–02:17 — Reconstruct the whole picture.
        self.copy(
            "하나의 그림 안에서 모두 연결됩니다",
            "INITIAL CONDITION → TRAJECTORY → BASIN / SADDLE / ATTRACTOR",
            "Loss Landscape가 vector field를 만들고,\n초기 상태가 그 위에서 하나의 trajectory를 만듭니다.",
        )
        overview = self.overview()
        self.show(overview)
        self.play(LaggedStart(*[Indicate(item, scale_factor=1.06) for item in overview[5]], lag_ratio=0.18), run_time=2.8)
        self.to(137)

        # 02:17–02:27 — Final message.
        self.copy(
            "학습은 파라미터 공간 위의 흐름입니다",
            "TRAINING = DYNAMICS IN PARAMETER SPACE",
            "초기 상태와 vector field가 경로를 만들고,\n그 경로들의 전체 구조가 학습 dynamics입니다.",
        )
        final_field = self.vector_field(self.single_grad, color=MUTED, opacity=0.4)
        statement = card("Training = Dynamics\nin Parameter Space", ACCENT, 6.5, 1.5, 31, 0.16)
        statement.move_to([0, 0.6, 0])
        korean = label("학습은 파라미터 공간 위의 흐름이다", 28, INK).move_to([0, -1.1, 0])
        self.show(VGroup(self.quadratic_contours(0.18), final_field, statement, korean))
        self.play(Indicate(statement, color=ACCENT, scale_factor=1.04), run_time=1.4)
        self.to(147)

    # ---------- Mathematical visuals ----------

    def p2s(self, point):
        p = np.asarray(point, dtype=float)
        return self.ORIGIN + np.array([p[0] * self.XSCALE, p[1] * self.YSCALE, 0])

    def single_grad(self, point):
        return self.QUADRATIC @ np.asarray(point, dtype=float)

    @staticmethod
    def double_grad(point):
        x, y = np.asarray(point, dtype=float)
        return np.array([4 * x * (x * x - 2.25), 1.3 * y])

    @staticmethod
    def saddle_grad(point):
        x, y = np.asarray(point, dtype=float)
        return np.array([2 * x, -2 * y])

    def plane_grid(self):
        grid = VGroup()
        for x in np.arange(-3, 3.1, 1):
            grid.add(Line(self.p2s((x, -3)), self.p2s((x, 3)), color=ZERO, stroke_width=1.2))
        for y in np.arange(-3, 3.1, 1):
            grid.add(Line(self.p2s((-3.4, y)), self.p2s((3.4, y)), color=ZERO, stroke_width=1.2))
        return grid

    def axis_cross(self):
        return VGroup(
            Arrow(self.p2s((-3.3, 0)), self.p2s((3.3, 0)), buff=0, color=MUTED, stroke_width=2),
            Arrow(self.p2s((0, -3.2)), self.p2s((0, 3.2)), buff=0, color=MUTED, stroke_width=2),
            label("x", 22, MUTED).move_to(self.p2s((3.25, -0.32))),
            label("y", 22, MUTED).move_to(self.p2s((0.28, 3.05))),
        )

    def quadratic_contours(self, opacity=0.48):
        values, vectors = np.linalg.eigh(self.QUADRATIC)
        angle = np.arctan2(vectors[1, 0], vectors[0, 0])
        contours = VGroup()
        for level, alpha in zip([0.35, 0.75, 1.25, 1.9, 2.7, 3.7], np.linspace(0.9, 0.25, 6)):
            radii = np.sqrt(2 * level / values)
            ellipse = Ellipse(
                width=2 * radii[0] * self.XSCALE,
                height=2 * radii[1] * self.YSCALE,
                color=WEIGHT,
                stroke_width=2,
                stroke_opacity=opacity * alpha,
            ).rotate(angle).move_to(self.ORIGIN)
            contours.add(ellipse)
        return contours

    def vector_field(self, grad, color=WEIGHT, opacity=0.8, xlim=3.0, ylim=2.7):
        arrows = VGroup()
        for x in np.linspace(-xlim, xlim, 7):
            for y in np.linspace(-ylim, ylim, 7):
                p = np.array([x, y])
                g = -np.asarray(grad(p), dtype=float)
                norm = np.linalg.norm(g)
                if norm < 1e-7:
                    continue
                direction = g / norm
                start = self.p2s(p) - np.array([direction[0] * self.XSCALE,
                                                 direction[1] * self.YSCALE, 0]) * 0.25
                end = self.p2s(p) + np.array([direction[0] * self.XSCALE,
                                               direction[1] * self.YSCALE, 0]) * 0.25
                arrows.add(Arrow(start, end, buff=0, color=color, stroke_width=2.1,
                                 stroke_opacity=opacity, tip_length=0.13))
        return arrows

    def arrow_at(self, grad, point, color=ACCENT, length=0.8):
        g = -np.asarray(grad(point), dtype=float)
        g /= max(np.linalg.norm(g), 1e-8)
        start = self.p2s(point)
        direction = np.array([g[0] * self.XSCALE, g[1] * self.YSCALE, 0])
        direction /= max(np.linalg.norm(direction), 1e-8)
        return Arrow(start, start + direction * length, buff=0.08, color=color,
                     stroke_width=5, tip_length=0.2)

    def flow_points(self, grad, start, steps=120, dt=0.045, stop_radius=0.035):
        point = np.asarray(start, dtype=float)
        points = [point.copy()]
        for _ in range(steps):
            vector = -np.asarray(grad(point), dtype=float)
            magnitude = np.linalg.norm(vector)
            if stop_radius is not None and magnitude < stop_radius:
                break
            # Cap only the numerical step; arrow lengths remain normalized separately.
            if magnitude * dt > 0.13:
                vector *= 0.13 / (magnitude * dt)
            point = point + dt * vector
            points.append(point.copy())
            if abs(point[0]) > 3.6 or abs(point[1]) > 3.5:
                break
        return points

    def flow_path(self, grad, start, steps=120, dt=0.045, stop_radius=0.035):
        points = [self.p2s(p) for p in self.flow_points(grad, start, steps, dt, stop_radius)]
        if len(points) < 2:
            points.append(points[0] + RIGHT * 0.001)
        return VMobject(color=WEIGHT, stroke_width=3).set_points_smoothly(points)

    def path_dots(self, path, count, color):
        return VGroup(*[
            Dot(path.point_from_proportion(float(t)), radius=0.045, color=color)
            for t in np.linspace(0, 1, count)
        ])

    def surface_value(self, point):
        p = np.asarray(point, dtype=float)
        return 0.5 * float(p @ self.QUADRATIC @ p)

    def surface_point(self, point):
        x, y = np.asarray(point, dtype=float)
        z = self.surface_value(point)
        return np.array([0.88 * x + 0.34 * y, 0.2 + 0.30 * y + 0.29 * z, 0])

    def surface_mesh(self):
        mesh = VGroup()
        samples = np.linspace(-3.0, 3.0, 45)
        for x in np.linspace(-3, 3, 11):
            points = [self.surface_point((x, y)) for y in samples]
            mesh.add(VMobject(color=WEIGHT, stroke_width=1.4, stroke_opacity=0.5).set_points_smoothly(points))
        for y in np.linspace(-3, 3, 11):
            points = [self.surface_point((x, y)) for x in samples]
            mesh.add(VMobject(color=SPARSE, stroke_width=1.4, stroke_opacity=0.42).set_points_smoothly(points))
        floor = label("Loss Surface", 22, MUTED).move_to([0, -2.7, 0])
        return VGroup(mesh, floor)

    def surface_trajectory(self, start):
        points = [self.surface_point(p) for p in self.flow_points(self.single_grad, start, 120, 0.045)]
        return VMobject(color=ACCENT, stroke_width=4).set_points_smoothly(points)

    def basin_background(self):
        left = Rectangle(width=3.5, height=5.55, stroke_width=0,
                         fill_color=WEIGHT, fill_opacity=0.075).move_to([-1.75, 0.55, 0])
        right = Rectangle(width=3.5, height=5.55, stroke_width=0,
                          fill_color=SPARSE, fill_opacity=0.075).move_to([1.75, 0.55, 0])
        return VGroup(left, right)

    def double_contours(self):
        contours = VGroup()
        for center, color in [((-1.5, 0), WEIGHT), ((1.5, 0), SPARSE)]:
            for width, height, opacity in [(0.8, 0.6, 0.75), (1.5, 1.0, 0.52), (2.25, 1.55, 0.28)]:
                contours.add(Ellipse(width=width * self.XSCALE, height=height * self.YSCALE,
                                     color=color, stroke_width=2, stroke_opacity=opacity).move_to(self.p2s(center)))
        contours.add(DashedLine(self.p2s((0, -3)), self.p2s((0, 3)), color=PRUNE,
                                stroke_width=2, stroke_opacity=0.45))
        return contours

    def saddle_mesh(self):
        mesh = VGroup()
        samples = np.linspace(-2.7, 2.7, 45)

        def project(x, y):
            z = 0.18 * (x * x - y * y)
            return np.array([0.96 * x + 0.28 * y, 0.55 + 0.27 * y + 0.52 * z, 0])

        for x in np.linspace(-2.5, 2.5, 10):
            mesh.add(VMobject(color=WEIGHT, stroke_width=1.5, stroke_opacity=0.58)
                     .set_points_smoothly([project(x, y) for y in samples]))
        for y in np.linspace(-2.5, 2.5, 10):
            mesh.add(VMobject(color=PRUNE, stroke_width=1.5, stroke_opacity=0.54)
                     .set_points_smoothly([project(x, y) for x in samples]))
        return mesh

    def step_panel(self, eta, title, color):
        box = RoundedRectangle(width=6.8, height=1.55, corner_radius=0.15,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=0.045)
        line = Line([-2.65, 0, 0], [2.65, 0, 0], color=MUTED, stroke_width=2)
        center = Dot(ORIGIN, radius=0.07, color=GOOD)
        x = 2.2
        values = [x]
        for _ in range(7):
            x = x - eta * x
            values.append(x)
        values = np.clip(values, -3.0, 3.0)
        dots = VGroup(*[Dot([v * 0.85, 0, 0], radius=0.065, color=color) for v in values])
        for dot, opacity in zip(dots, np.linspace(0.35, 1.0, len(dots))):
            dot.set_opacity(float(opacity))
        label_group = label(f"{title}   η={eta:g}", 19, color).move_to([0, 0.48, 0])
        group = VGroup(box, line, dots, center, label_group)
        return group

    def noisy_path(self, smooth_path):
        rng = np.random.default_rng(1313)
        points = []
        for i, t in enumerate(np.linspace(0, 1, 52)):
            point = smooth_path.point_from_proportion(float(t)).copy()
            envelope = np.sin(np.pi * t)
            point += np.array([rng.normal(0, 0.055), rng.normal(0, 0.09), 0]) * envelope
            points.append(point)
        return VMobject().set_points_smoothly(points)

    def overview(self):
        background = self.basin_background()
        contours = self.double_contours()
        field = self.vector_field(self.double_grad, color=MUTED, opacity=0.30)
        start = np.array([-2.85, 2.25])
        path = self.flow_path(self.double_grad, start, steps=140, dt=0.024)
        path.set_stroke(color=WEIGHT, width=4)
        labels = VGroup(
            label("Initial condition", 18, ACCENT).move_to(self.p2s(start) + UP * 0.35),
            label("Trajectory", 18, WEIGHT).move_to([-2.2, 1.3, 0]),
            label("Basin", 18, SPARSE).move_to([2.3, 3.55, 0]),
            label("Saddle", 18, PRUNE).move_to([0.5, 0.1, 0]),
            label("Attractor", 18, GOOD).move_to([-1.55, -0.25, 0]),
        )
        markers = VGroup(
            Dot(self.p2s(start), radius=0.09, color=ACCENT),
            path,
            Rectangle(width=3.35, height=5.3, stroke_color=SPARSE, stroke_opacity=0.25),
            Dot(self.p2s((0, 0)), radius=0.11, color=PRUNE),
            Dot(self.p2s((-1.5, 0)), radius=0.13, color=GOOD),
        )
        return VGroup(background, contours, field, path, markers, labels)

    # ---------- Shared scene chrome ----------

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.remove_foreground_mobjects(self.heading, self.note, self.caption_box, self.caption)
            self.play(FadeOut(old), run_time=0.1)
        self.heading = label(heading, 28).move_to(UP * 5.12)
        self.note = label(note, 18, ACCENT).move_to(DOWN * 4.42)
        self.caption_box = RoundedRectangle(
            width=7.65,
            height=1.15,
            corner_radius=0.14,
            stroke_color=ZERO,
            stroke_width=1.2,
            fill_color=ZERO,
            fill_opacity=0.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        for mob in (self.heading, self.note, self.caption_box, self.caption):
            mob.set_z_index(100)
        self.caption.set_z_index(101)
        self.play(FadeIn(self.heading), FadeIn(self.note), FadeIn(self.caption_box),
                  FadeIn(self.caption), run_time=0.2)
        self.add_foreground_mobjects(self.chrome, self.heading, self.note,
                                    self.caption_box, self.caption, self.progress)
        self.restore_layers()

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=0.18)
            # Animated objects can also be registered as top-level scene mobjects.
            # Remove the full family so no child survives after a stage transition.
            self.remove(*self.stage.get_family())
        self.stage = new_stage
        if len(self.stage):
            self.play(FadeIn(self.stage, shift=UP * 0.1), run_time=0.4)
        self.restore_layers()

    def restore_layers(self):
        self.chrome[0].set_opacity(1)
        self.chrome[1].set_opacity(1)
        self.chrome[2].set_stroke(opacity=0.35)
        self.heading.set_opacity(1)
        self.note.set_opacity(1)
        self.caption_box.set_opacity(1)
        self.caption.set_opacity(1)
        self.add(self.chrome, self.progress)
        self.bring_to_front(self.chrome, self.heading, self.note,
                            self.caption_box, self.caption, self.progress)

    def to(self, target):
        self.restore_layers()
        remaining = target - self.time
        if remaining < -0.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(0.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(0.25, remaining))
            self.wait(max(0, target - self.time))
