"""Neural Network Mathematics 14: why Hessian spectra contain many flat directions."""

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


class NeuralMathHessianFlatDirections(Scene):
    DURATION = 141
    CENTER = np.array([0.0, 0.35, 0.0])

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  14", 18, MUTED).move_to(UP * 7.3),
            label("왜 Hessian에는 0에 가까운 고유값이 많을까?", 26).move_to(UP * 6.46),
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

        # 00:00–00:08 — Continue from Gradient Flow and zoom into a minimum.
        self.copy(
            "Gradient Flow가 도착한 곳을 확대하면",
            "DIRECTION  →  LOCAL CURVATURE",
            "Minimum 주변에서 Loss는 왜\n방향마다 다르게 변할까요?",
        )
        valley = self.elongated_contours(WEIGHT, ratio=2.0, angle=20 * DEGREES)
        path = VMobject(color=ACCENT, stroke_width=4).set_points_smoothly(
            [[-3.1, 2.5, 0], [-2.1, 1.2, 0], [-0.7, 0.58, 0], self.CENTER]
        )
        dot = Dot(path.get_start(), radius=0.1, color=ACCENT)
        minimum = Dot(self.CENTER, radius=0.14, color=GOOD)
        halo = Circle(radius=0.42, color=GOOD, stroke_width=3).move_to(minimum)
        self.show(VGroup(valley, path.set_stroke(opacity=0.55), dot, minimum, halo,
                         label("θ*", 24, GOOD).next_to(halo, DOWN, buff=0.2)))
        self.play(MoveAlongPath(dot, path), run_time=2.4, rate_func=smooth)
        self.play(Indicate(halo, color=GOOD, scale_factor=1.25), run_time=1.0)
        self.to(8)

        # 00:08–00:16 — Isotropic bowl.
        self.copy(
            "먼저 둥근 그릇",
            "L(x,y) = x² + y²   ·   H = 2I",
            "어느 방향으로 움직여도 비슷하게 증가합니다.\n모든 방향의 곡률이 같습니다.",
        )
        contours = self.circular_contours()
        rays = self.direction_rays(12, radius=2.55, colors=[WEIGHT] * 12)
        center = Dot(self.CENTER, radius=0.13, color=ACCENT)
        equal = VGroup(*[
            label("λ=2", 18, WEIGHT).move_to(
                self.CENTER + np.array([2.95 * np.cos(a), 2.25 * np.sin(a), 0])
            ) for a in (0, PI / 2, PI, 3 * PI / 2)
        ])
        self.show(VGroup(contours, rays, center, equal))
        self.play(LaggedStart(*[GrowArrow(ray) for ray in rays], lag_ratio=0.06), run_time=1.5)
        self.to(16)

        # 00:16–00:25 — Anisotropic bowl.
        self.copy(
            "계수를 바꾸면 모양이 달라집니다",
            "L(x,y) = 10x² + 0.01y²",
            "x 방향은 아주 가파르고,\ny 방향은 거의 평평합니다.",
        )
        ellipses = self.elongated_contours(PRUNE, ratio=4.6, angle=0)
        axes = self.cross_axes()
        steep = DoubleArrow([-1.15, 0.35, 0], [1.15, 0.35, 0], buff=0,
                            color=PRUNE, stroke_width=5, tip_length=0.2)
        flat = DoubleArrow([0, -2.75, 0], [0, 3.45, 0], buff=0,
                           color=GOOD, stroke_width=5, tip_length=0.2)
        tags = VGroup(
            card("x  ·  steep", PRUNE, 2.45, 0.7, 21).move_to([2.25, 2.5, 0]),
            card("y  ·  almost flat", GOOD, 3.25, 0.7, 21).move_to([-1.85, 3.45, 0]),
        )
        self.show(VGroup(ellipses, axes, steep, flat, Dot(self.CENTER, radius=0.12, color=ACCENT), tags))
        self.play(Indicate(steep, color=PRUNE), Indicate(flat, color=GOOD), run_time=1.4)
        self.to(25)

        # 00:25–00:34 — Hessian eigen-equation.
        self.copy(
            "방향별 휘어짐을 숫자로 읽습니다",
            "HESSIAN EIGEN-DIRECTIONS",
            "vᵢ는 특별한 방향, λᵢ는\n그 방향의 국소 곡률입니다.",
        )
        equation = card("H vᵢ  =  λᵢ vᵢ", ACCENT, 6.6, 1.2, 40, 0.09).move_to([0, 1.6, 0])
        direction = card("vᵢ   eigen-direction", WEIGHT, 5.5, 0.9, 24).move_to([0, 0.0, 0])
        curvature = card("λᵢ   local curvature", GOOD, 5.5, 0.9, 24).move_to([0, -1.3, 0])
        local = label("L(θ*+αvᵢ) ≈ L(θ*) + ½α²λᵢ", 25, MUTED).move_to([0, 3.45, 0])
        self.show(VGroup(equation, direction, curvature, local))
        self.play(Indicate(direction[0], color=WEIGHT), Indicate(curvature[0], color=GOOD), run_time=1.2)
        self.to(34)

        # 00:34–00:42 — Compare directional slices.
        self.copy(
            "같은 점, 전혀 다른 단면",
            "LARGE λ  vs  λ ≈ 0",
            "큰 λ는 민감한 방향, λ≈0은\n국소 2차 변화가 작은 방향입니다.",
        )
        sharp = self.slice_chart(2.1, PRUNE, "λ = 20", "STIFF").scale(0.78).move_to([-1.9, 0.15, 0])
        flat_chart = self.slice_chart(0.11, GOOD, "λ = 0.02", "FLAT").scale(0.78).move_to([1.9, 0.15, 0])
        divide = Line([0, 3.1, 0], [0, -2.7, 0], color=MUTED, stroke_opacity=0.28)
        self.show(VGroup(sharp, flat_chart, divide))
        self.to(42)

        # 00:42–00:50 — Add a dimension and reveal a trough.
        self.copy(
            "평평한 방향을 하나 추가하면",
            "L(x,y,z) = x² + y²   ·   ∂²L/∂z² = 0",
            "z 방향으로 Loss가 변하지 않는\n긴 통 모양의 valley가 됩니다.",
        )
        trough = self.trough_mesh()
        z_arrow = DoubleArrow([-3.05, -2.45, 0], [3.1, 2.1, 0], buff=0,
                              color=GOOD, stroke_width=4, tip_length=0.18)
        z_tag = card("z direction  ·  λz = 0", GOOD, 4.4, 0.72, 22).move_to([0, 3.65, 0])
        self.show(VGroup(trough, z_arrow, z_tag))
        self.play(ShowPassingFlash(z_arrow.copy().set_stroke(width=8), time_width=0.7), run_time=1.5)
        self.to(50)

        # 00:50–00:59 — Conceptual Hessian spectrum.
        self.copy(
            "고차원에서는 이런 방향이 많습니다",
            "CONCEPTUAL HESSIAN SPECTRUM",
            "0 근처에 많은 값이 모이고,\n큰 양의 값은 일부인 형태가 자주 나타납니다.",
        )
        spectrum = self.spectrum_chart()
        self.show(spectrum)
        bars = spectrum[2]
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.04), run_time=1.8)
        self.to(59)

        # 00:59–01:09 — Overparameterization.
        self.copy(
            "이유 1  ·  필요한 것보다 많은 파라미터",
            "OVERPARAMETERIZATION",
            "수많은 parameter direction 중\n강하게 제약되는 방향은 일부일 수 있습니다.",
        )
        rays = self.parameter_rays(34)
        center = Dot(self.CENTER, radius=0.15, color=ACCENT)
        counts = VGroup(
            card("parameters   D = 1,000,000", WEIGHT, 6.2, 0.8, 23).move_to([0, 3.45, 0]),
            card("strong constraints   ≪ D", PRUNE, 5.5, 0.8, 23).move_to([0, -2.9, 0]),
        )
        self.show(VGroup(rays, center, counts))
        active = {2, 10, 18, 27}
        self.play(*[
            ray.animate.set_stroke(
                color=PRUNE if i in active else MUTED,
                opacity=0.95 if i in active else 0.10,
                width=4 if i in active else 1.2,
            ) for i, ray in enumerate(rays)
        ], run_time=1.5)
        self.to(69)

        # 01:09–01:18 — ReLU scaling symmetry.
        self.copy(
            "이유 2  ·  같은 함수를 만드는 연속 경로",
            "ReLU SCALING SYMMETRY",
            "w→cw, v→v/c로 움직여도\n적절한 조건에서는 같은 함수가 유지됩니다.",
        )
        axes = self.parameter_axes()
        symmetry_path = self.hyperbola_path()
        point = Dot(symmetry_path.get_start(), radius=0.11, color=ACCENT)
        formula = card("v · ReLU(w x)", WEIGHT, 3.4, 0.78, 23).move_to([2.1, 3.35, 0])
        invariant = card("wv = constant", GOOD, 3.4, 0.78, 23).move_to([-2.0, 3.35, 0])
        output = self.function_panel().move_to([0, -2.75, 0])
        self.show(VGroup(axes, symmetry_path, point, formula, invariant, output))
        self.play(MoveAlongPath(point, symmetry_path), run_time=3.0, rate_func=smooth)
        self.play(Indicate(output, color=GOOD), run_time=0.9)
        self.to(78)

        # 01:18–01:26 — Tangent to a constant-loss path.
        self.copy(
            "경로를 따라 움직여도 Loss가 그대로라면",
            "L(θ(t)) = constant",
            "symmetry path의 접선 방향은\nexact flat direction이 됩니다.",
        )
        curve = self.hyperbola_path(color=GOOD).shift(UP * 0.65)
        theta = Dot(curve.point_from_proportion(0.54), radius=0.13, color=ACCENT)
        tangent = DoubleArrow(theta.get_center() + np.array([-1.45, 0.72, 0]),
                              theta.get_center() + np.array([1.45, -0.72, 0]),
                              buff=0, color=ACCENT, stroke_width=5, tip_length=0.2)
        loss_line = Line([-2.7, -2.0, 0], [2.7, -2.0, 0], color=GOOD, stroke_width=5)
        loss_axis = VGroup(Line([-3.0, -2.55, 0], [3.0, -2.55, 0], color=MUTED),
                           Line([-3.0, -2.55, 0], [-3.0, -1.25, 0], color=MUTED))
        self.show(VGroup(curve, theta, tangent, loss_axis, loss_line,
                         label("tangent  ·  zero mode", 23, ACCENT).move_to([0, 3.25, 0]),
                         label("Loss", 20, MUTED).move_to([-3.35, -1.35, 0])))
        self.play(Indicate(tangent, color=ACCENT), Indicate(loss_line, color=GOOD), run_time=1.3)
        self.to(86)

        # 01:26–01:35 — Data cannot see every direction.
        self.copy(
            "이유 3  ·  데이터가 보지 못하는 방향",
            "Jv ≈ 0",
            "v 방향으로 움직여도 현재 데이터의 출력이\n거의 변하지 않으면 Jv≈0입니다.",
        )
        center = Dot(self.CENTER, radius=0.15, color=ACCENT)
        observed = VGroup(*[
            DoubleArrow(self.CENTER - 2.65 * d, self.CENTER + 2.65 * d, buff=0,
                        color=WEIGHT, stroke_width=3.2, tip_length=0.16)
            for d in (np.array([1.0, 0.15, 0]), np.array([0.45, 0.8, 0]))
        ])
        blind = DoubleArrow(self.CENTER + np.array([-1.65, 2.1, 0]),
                            self.CENTER + np.array([1.65, -2.1, 0]), buff=0,
                            color=MUTED, stroke_width=4, tip_length=0.18)
        samples = VGroup(*[
            card(f"sample {i}", WEIGHT, 1.7, 0.58, 18, 0.06).move_to([-2.7 + 1.8 * i, 3.2, 0])
            for i in range(4)
        ])
        blind_tag = card("invisible to current data", MUTED, 5.1, 0.72, 22).move_to([0, -2.85, 0])
        self.show(VGroup(observed, blind, center, samples, blind_tag))
        self.play(*[Indicate(ray, color=WEIGHT) for ray in observed], run_time=1.1)
        self.play(Indicate(blind, color=MUTED), run_time=1.0)
        self.to(95)

        # 01:35–01:45 — Link Jacobian-null directions to curvature.
        self.copy(
            "출력 변화가 작으면 곡률도 작아질 수 있습니다",
            "GAUSS–NEWTON STRUCTURE",
            "H≈JᵀGJ인 성분에서는\nJv≈0이면 Hv≈0가 됩니다.",
        )
        chain = VGroup(
            card("parameter move   v", WEIGHT, 5.8, 0.84, 24),
            card("output change   Jv ≈ 0", MUTED, 5.8, 0.84, 24),
            card("curvature   vᵀJᵀGJv ≈ 0", GOOD, 5.8, 0.84, 24),
        ).arrange(DOWN, buff=0.7).move_to([0, 0.35, 0])
        arrows = VGroup(*[
            Arrow(chain[i].get_bottom(), chain[i + 1].get_top(), buff=0.1,
                  color=ACCENT, stroke_width=3, tip_length=0.18)
            for i in range(2)
        ])
        caveat = label("important component  ·  not always the full Hessian", 18, MUTED).move_to([0, -3.2, 0])
        self.show(VGroup(chain, arrows, caveat))
        self.play(LaggedStart(*[Indicate(item[0], color=item[0].get_color()) for item in chain],
                              lag_ratio=0.25), run_time=1.8)
        self.to(105)

        # 01:45–01:54 — Inactive ReLU unit.
        self.copy(
            "이유 4  ·  사용되지 않는 뉴런",
            "INACTIVE ReLU ON TRAINING DATA",
            "모든 sample에서 꺼진 unit의 일부 weight는\n당장 출력과 Loss를 바꾸지 않을 수 있습니다.",
        )
        samples = VGroup(*[
            card(value, WEIGHT, 1.35, 0.62, 19, 0.05)
            for value in ("x₁", "x₂", "x₃", "x₄")
        ]).arrange(DOWN, buff=0.28).move_to([-2.8, 0.45, 0])
        neuron = Circle(radius=0.55, color=MUTED, stroke_width=3, fill_color=ZERO, fill_opacity=0.35)
        neuron.move_to([0, 0.45, 0])
        relu = label("ReLU", 22, MUTED).move_to(neuron)
        outputs = VGroup(*[card("0", MUTED, 1.0, 0.55, 20, 0.04) for _ in range(4)])
        outputs.arrange(DOWN, buff=0.35).move_to([2.75, 0.45, 0])
        links_in = VGroup(*[Line(s.get_right(), neuron.get_left(), color=MUTED, stroke_opacity=0.45) for s in samples])
        links_out = VGroup(*[Line(neuron.get_right(), o.get_left(), color=MUTED, stroke_opacity=0.45) for o in outputs])
        off = card("h(xᵢ)=0   for all training samples", PRUNE, 6.5, 0.78, 22).move_to([0, -2.65, 0])
        cross = VGroup(Line([-0.28, 0.17, 0], [0.28, 0.73, 0], color=PRUNE, stroke_width=5),
                       Line([-0.28, 0.73, 0], [0.28, 0.17, 0], color=PRUNE, stroke_width=5))
        self.show(VGroup(links_in, links_out, samples, neuron, relu, outputs, cross, off))
        self.play(Wiggle(links_in, scale_value=1.04), run_time=1.4)
        self.play(*[Indicate(o, color=MUTED) for o in outputs], run_time=1.0)
        self.to(114)

        # 01:54–02:04 — Exact versus approximate flatness.
        self.copy(
            "모든 near-zero eigenvalue가 같지는 않습니다",
            "EXACT  ≠  APPROXIMATELY FLAT",
            "symmetry의 exact flat direction과\n천천히 변하는 방향을 구별해야 합니다.",
        )
        exact = self.flatness_panel(exact=True).move_to([-1.9, 0.25, 0])
        approx = self.flatness_panel(exact=False).move_to([1.9, 0.25, 0])
        divide = Line([0, 3.1, 0], [0, -2.8, 0], color=MUTED, stroke_opacity=0.28)
        self.show(VGroup(exact, approx, divide))
        self.to(124)

        # 02:04–02:13 — Replace a point minimum with an extended valley.
        self.copy(
            "Minimum을 점 하나로만 그리면",
            "POINT  →  EXTENDED LOW-LOSS REGION",
            "실제 주변은 몇 방향으로만 좁고,\n수많은 방향으로 길게 뻗을 수 있습니다.",
        )
        point = Dot(self.CENTER, radius=0.18, color=ACCENT)
        rings = self.elongated_contours(GOOD, ratio=5.2, angle=24 * DEGREES)
        stiff = DoubleArrow(self.CENTER + np.array([-0.55, 1.15, 0]),
                            self.CENTER + np.array([0.55, -1.15, 0]), buff=0,
                            color=PRUNE, stroke_width=5, tip_length=0.18)
        flat = DoubleArrow(self.CENTER + np.array([-2.8, -1.25, 0]),
                           self.CENTER + np.array([2.8, 1.25, 0]), buff=0,
                           color=GOOD, stroke_width=5, tip_length=0.18)
        self.show(VGroup(rings, point, stiff, flat,
                         card("few stiff", PRUNE, 2.5, 0.68, 21).move_to([-2.4, 3.2, 0]),
                         card("many flat", GOOD, 2.7, 0.68, 21).move_to([2.25, 3.2, 0])))
        self.play(point.animate.scale(0.65), rings.animate.set_stroke(opacity=0.72), run_time=1.2)
        self.to(133)

        # 02:13–02:21 — Final synthesis.
        self.copy(
            "고차원 minimum의 더 좋은 그림",
            "FEW STIFF DIRECTIONS  +  MANY FLAT DIRECTIONS",
            "둥근 그릇보다, 몇 방향만 휘어진\n넓은 고차원 골짜기에 가까울 수 있습니다.",
        )
        valley = self.elongated_contours(GOOD, ratio=5.8, angle=18 * DEGREES)
        center = Dot(self.CENTER, radius=0.13, color=ACCENT)
        summary = VGroup(
            card("overparameterization", WEIGHT, 3.1, 0.66, 19),
            card("symmetry", SPARSE, 2.2, 0.66, 19),
            card("data-null", MUTED, 2.2, 0.66, 19),
            card("inactive units", PRUNE, 2.6, 0.66, 19),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.22)).move_to([0, -2.8, 0])
        final = card("High-dimensional minimum  ≈  wide valley", ACCENT, 7.0, 0.85, 24).move_to([0, 3.65, 0])
        self.show(VGroup(valley, center, summary, final))
        self.play(ShowPassingFlash(valley.copy().set_stroke(color=ACCENT, width=5), time_width=0.8), run_time=1.6)
        self.to(141)

    # ---------- Visual building blocks ----------

    def circular_contours(self):
        return VGroup(*[
            Circle(radius=r, color=WEIGHT, stroke_width=2.5, stroke_opacity=0.82 - 0.12 * i)
            .stretch(0.82, 1).move_to(self.CENTER)
            for i, r in enumerate((0.65, 1.2, 1.8, 2.45, 3.1))
        ])

    def elongated_contours(self, color=GOOD, ratio=4.5, angle=0):
        contours = VGroup()
        for i, scale in enumerate((0.65, 1.1, 1.6, 2.15, 2.7)):
            contours.add(Ellipse(width=scale * ratio, height=scale,
                                 color=color, stroke_width=2.4,
                                 stroke_opacity=max(0.18, 0.82 - 0.12 * i)))
        contours.scale_to_fit_width(7.0).rotate(angle).move_to(self.CENTER)
        return contours

    def direction_rays(self, count, radius=2.5, colors=None):
        rays = VGroup()
        colors = colors or [WEIGHT] * count
        for i in range(count):
            angle = TAU * i / count
            direction = np.array([np.cos(angle), 0.82 * np.sin(angle), 0])
            rays.add(Arrow(self.CENTER, self.CENTER + radius * direction, buff=0.18,
                           color=colors[i], stroke_width=2.4, tip_length=0.14))
        return rays

    def cross_axes(self):
        return VGroup(
            Arrow([-3.35, 0.35, 0], [3.35, 0.35, 0], buff=0, color=MUTED, stroke_width=2),
            Arrow([0, -3.1, 0], [0, 3.75, 0], buff=0, color=MUTED, stroke_width=2),
            label("x", 20, MUTED).move_to([3.25, 0.03, 0]),
            label("y", 20, MUTED).move_to([0.27, 3.58, 0]),
        )

    def slice_chart(self, curvature, color, eigenvalue, name):
        base = Line([-1.9, -1.35, 0], [1.9, -1.35, 0], color=MUTED, stroke_opacity=0.65)
        vertical = Line([-1.9, -1.35, 0], [-1.9, 1.9, 0], color=MUTED, stroke_opacity=0.65)
        x = np.linspace(-1.65, 1.65, 80)
        y = -0.8 + curvature * (x / 1.55) ** 2
        y = np.minimum(y, 1.55)
        curve = VMobject(color=color, stroke_width=5).set_points_smoothly(
            [np.array([a, b, 0]) for a, b in zip(x, y)]
        )
        return VGroup(base, vertical, curve, Dot([0, -0.8, 0], radius=0.1, color=ACCENT),
                      label(eigenvalue, 24, color).move_to([0, 2.25, 0]),
                      label(name, 22, color).move_to([0, -1.9, 0]))

    def trough_mesh(self):
        mesh = VGroup()

        def project(u, z):
            height = 0.34 * u * u
            return np.array([0.78 * z + 0.6 * u, 0.38 * z + height - 1.15, 0])

        samples = np.linspace(-2.8, 2.8, 60)
        for z in np.linspace(-2.7, 2.7, 10):
            mesh.add(VMobject(color=WEIGHT, stroke_width=1.6, stroke_opacity=0.52)
                     .set_points_smoothly([project(u, z) for u in samples]))
        for u in np.linspace(-2.1, 2.1, 10):
            mesh.add(VMobject(color=GOOD, stroke_width=1.6, stroke_opacity=0.55)
                     .set_points_smoothly([project(u, z) for z in samples]))
        return mesh

    def spectrum_chart(self):
        base = Line([-3.25, -2.25, 0], [3.3, -2.25, 0], color=MUTED)
        yaxis = Line([-3.25, -2.25, 0], [-3.25, 2.85, 0], color=MUTED)
        heights = (4.6, 4.25, 3.85, 3.3, 2.75, 2.15, 1.6, 1.2, 0.85, 0.55,
                   0.36, 0.25, 0.18, 0.13, 0.10, 0.08, 0.07, 0.06)
        bars = VGroup()
        for i, h in enumerate(heights):
            x = -2.95 + i * 0.34
            bars.add(Rectangle(width=0.24, height=h, stroke_width=0,
                               fill_color=GOOD if i < 12 else PRUNE,
                               fill_opacity=0.82).move_to([x, -2.25 + h / 2, 0]))
        labels = VGroup(
            label("near 0", 20, GOOD).move_to([-2.45, -2.75, 0]),
            label("large +", 20, PRUNE).move_to([2.25, -2.75, 0]),
            label("count", 18, MUTED).move_to([-3.55, 2.75, 0]),
            label("eigenvalue λ", 18, MUTED).move_to([1.55, -3.2, 0]),
        )
        return VGroup(base, yaxis, bars, labels)

    def parameter_rays(self, count):
        rays = VGroup()
        for i in range(count):
            angle = TAU * i / count
            length = 2.1 + 0.5 * (i % 4) / 3
            direction = np.array([np.cos(angle), 0.78 * np.sin(angle), 0])
            rays.add(Line(self.CENTER, self.CENTER + length * direction,
                          color=WEIGHT, stroke_width=2, stroke_opacity=0.38))
        return rays

    def parameter_axes(self):
        origin = np.array([-0.5, 0.15, 0])
        return VGroup(
            Arrow([-3.2, origin[1], 0], [3.2, origin[1], 0], buff=0, color=MUTED, stroke_width=2),
            Arrow([origin[0], -2.1, 0], [origin[0], 2.85, 0], buff=0, color=MUTED, stroke_width=2),
            label("w", 21, MUTED).move_to([3.05, origin[1] - 0.3, 0]),
            label("v", 21, MUTED).move_to([origin[0] + 0.25, 2.7, 0]),
        )

    def hyperbola_path(self, color=ACCENT):
        xs = np.linspace(0.65, 3.2, 90)
        points = [np.array([-0.5 + x, 0.15 + 1.7 / x, 0]) for x in xs]
        return VMobject(color=color, stroke_width=4).set_points_smoothly(points)

    def function_panel(self):
        box = RoundedRectangle(width=6.5, height=1.25, corner_radius=0.16,
                               stroke_color=GOOD, stroke_width=2,
                               fill_color=GOOD, fill_opacity=0.07)
        line = VMobject(color=GOOD, stroke_width=4).set_points_smoothly(
            [[-2.5, -0.3, 0], [-1.3, -0.3, 0], [0, -0.3, 0], [1.2, 0.3, 0], [2.5, 0.9, 0]]
        )
        line.scale(0.7).move_to(box)
        tag = label("fθ(x) unchanged", 21, GOOD).move_to(box.get_top() + DOWN * 0.22)
        return VGroup(box, line, tag)

    def flatness_panel(self, exact=True):
        color = GOOD if exact else WEIGHT
        box = RoundedRectangle(width=3.45, height=5.4, corner_radius=0.18,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=0.04)
        base = Line([-1.35, -1.45, 0], [1.35, -1.45, 0], color=MUTED)
        vertical = Line([-1.35, -1.45, 0], [-1.35, 1.35, 0], color=MUTED)
        xs = np.linspace(-1.15, 1.15, 70)
        ys = np.full_like(xs, -0.35) if exact else -0.45 + 0.12 * xs * xs
        curve = VMobject(color=color, stroke_width=5).set_points_smoothly(
            [[x, y, 0] for x, y in zip(xs, ys)]
        )
        title = label("EXACT" if exact else "APPROXIMATE", 22, color).move_to([0, 1.9, 0])
        detail = label("symmetry\nL = constant" if exact else "small curvature\nL changes slowly",
                       18, INK, 2.9).move_to([0, -2.0, 0])
        return VGroup(box, base, vertical, curve, title, detail)

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
        remaining = target - self.time
        if remaining < -0.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(0.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            run_time = min(0.25, remaining)
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=run_time)
            self.wait(max(0, target - self.time))
