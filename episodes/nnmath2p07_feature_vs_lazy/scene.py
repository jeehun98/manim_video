"""Neural Network Mathematics Part 2, episode 07: Feature vs Lazy Learning."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, BG, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.86, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .24))


def route(points, color=MUTED, width=3, opacity=.65, smooth=False):
    path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    points = [np.array(point, dtype=float) for point in points]
    if smooth:
        path.set_points_smoothly(points)
    else:
        path.set_points_as_corners(points)
    return path


class LearningBoard(VGroup):
    """Persistent two-lane comparison with common data and prediction."""

    def __init__(self):
        super().__init__()
        self.left_center = np.array([-2.05, .25, 0])
        self.right_center = np.array([2.05, .25, 0])
        left_box = RoundedRectangle(width=3.65, height=5.05, corner_radius=.24,
                                    color=SPARSE, fill_color=SPARSE,
                                    fill_opacity=.035, stroke_width=2.4)
        right_box = RoundedRectangle(width=3.65, height=5.05, corner_radius=.24,
                                     color=GOOD, fill_color=GOOD,
                                     fill_opacity=.035, stroke_width=2.4)
        left_box.move_to(self.left_center)
        right_box.move_to(self.right_center)
        self.left_title = label("A · FEATURE LEARNING", 19, SPARSE, 3.2).move_to([-2.05, 2.25, 0])
        self.right_title = label("B · LAZY LEARNING", 19, GOOD, 3.2).move_to([2.05, 2.25, 0])

        self.left_origin = np.array([-2.05, .35, 0])
        self.right_origin = np.array([2.05, .35, 0])
        offsets = [
            [-.95, .45, 0], [-.55, -.35, 0], [-.15, .72, 0], [.3, -.52, 0], [.75, .2, 0],
            [-.75, -.62, 0], [-.32, .12, 0], [.08, -.05, 0], [.48, .62, 0], [.9, -.28, 0],
        ]
        colors = [WEIGHT] * 5 + [PRUNE] * 5
        self.left_points = VGroup(*[
            Dot(self.left_origin + np.array(offset), radius=.075, color=color, fill_opacity=.72)
            for offset, color in zip(offsets, colors)
        ])
        self.right_points = VGroup(*[
            Dot(self.right_origin + np.array(offset), radius=.075, color=color, fill_opacity=.72)
            for offset, color in zip(offsets, colors)
        ])
        self.left_vectors = VGroup(
            Arrow(self.left_origin, self.left_origin + np.array([1.05, .2, 0]), buff=0,
                  color=WEIGHT, stroke_width=4, tip_length=.15),
            Arrow(self.left_origin, self.left_origin + np.array([-.35, 1.05, 0]), buff=0,
                  color=ACCENT, stroke_width=4, tip_length=.15),
            Arrow(self.left_origin, self.left_origin + np.array([-.8, -.65, 0]), buff=0,
                  color=PRUNE, stroke_width=4, tip_length=.15),
        )
        self.right_vectors = VGroup(
            Arrow(self.right_origin, self.right_origin + np.array([1.05, .2, 0]), buff=0,
                  color=WEIGHT, stroke_width=4, tip_length=.15),
            Arrow(self.right_origin, self.right_origin + np.array([-.35, 1.05, 0]), buff=0,
                  color=ACCENT, stroke_width=4, tip_length=.15),
            Arrow(self.right_origin, self.right_origin + np.array([-.8, -.65, 0]), buff=0,
                  color=PRUNE, stroke_width=4, tip_length=.15),
        )
        self.left_names = VGroup(*[
            label(f"v{i + 1}", 18, color).next_to(vec.get_end(), direction, buff=.08)
            for i, (vec, color, direction) in enumerate(zip(
                self.left_vectors, [WEIGHT, ACCENT, PRUNE], [RIGHT, UP, LEFT]
            ))
        ])
        self.right_names = VGroup(*[
            label(f"v{i + 1}", 18, color).next_to(vec.get_end(), direction, buff=.08)
            for i, (vec, color, direction) in enumerate(zip(
                self.right_vectors, [WEIGHT, ACCENT, PRUNE], [RIGHT, UP, LEFT]
            ))
        ])
        self.left_status = card("directions can move", SPARSE, 3.0, .68, 19, .1)
        self.left_status.move_to([-2.05, -1.6, 0])
        self.right_status = card("directions stay near init", GOOD, 3.2, .68, 18, .1)
        self.right_status.move_to([2.05, -1.6, 0])
        self.coefficients = VGroup(*[
            card(value, color, .78, .58, 17, .14).move_to([1.2 + i * .85, -2.35, 0])
            for i, (value, color) in enumerate(zip([".2", "−.1", ".3"], [WEIGHT, ACCENT, PRUNE]))
        ])
        self.coeff_label = label("combination weights", 17, MUTED, 2.7).move_to([2.05, -2.82, 0])
        self.left_marker = Dot(self.left_origin, radius=.11, color=SPARSE)
        self.right_marker = Dot(self.right_origin, radius=.11, color=GOOD)
        self.add(left_box, right_box, self.left_title, self.right_title,
                 self.left_points, self.right_points,
                 self.left_vectors, self.right_vectors, self.left_names, self.right_names,
                 self.left_status, self.right_status, self.coefficients, self.coeff_label,
                 self.left_marker, self.right_marker)


class NeuralMathPart2FeatureLazy(Scene):
    DURATION = 139

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 07", 17, MUTED).move_to(UP * 7.3),
            label("신경망은 학습하며 정말 새로운 Feature를 만들까?", 26).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        # 1 — Reverse the question raised by Grokking.
        self.copy(
            "성능이 변하면 내부 표현도 크게 변했을까요?", "BEHAVIOR  vs  REPRESENTATION",
            "앞에서는 같은 정답 뒤에도 내부가 변할 수 있었습니다.\n이번에는 반대 방향으로 질문해봅니다.",
        )
        graph = self.grokking_chart().scale(.68).move_to([0, .75, 0])
        question = card("학습됨  =  내부 표현이 바뀜?", SPARSE, 5.8, .86, 24, .14)
        question.move_to([0, -2.35, 0])
        self.show(VGroup(graph, question))
        self.play(graph.animate.scale(.82).shift(UP * .18).set_opacity(.58),
                  Indicate(question, color=PRUNE), run_time=.8)
        self.to(7.7)

        # 2 — The familiar feature-learning story.
        self.copy(
            "우리가 보통 떠올리는 학습의 모습", "TRAIN → NEW FEATURES → PREDICT",
            "고양이를 학습하면 귀와 털, 얼굴 형태처럼\n유용한 내부 Feature가 새로 만들어진다고 생각합니다.",
        )
        cloud = self.feature_cloud(np.array([0, .2, 0]), separated=False, scale=1.35)
        self.show(cloud)
        axes = VGroup(
            Arrow([0, .2, 0], [2.45, .55, 0], buff=0, color=WEIGHT, stroke_width=4, tip_length=.16),
            Arrow([0, .2, 0], [-.75, 2.45, 0], buff=0, color=ACCENT, stroke_width=4, tip_length=.16),
            Arrow([0, .2, 0], [-1.65, -1.5, 0], buff=0, color=PRUNE, stroke_width=4, tip_length=.16),
        )
        names = VGroup(label("귀", 20, WEIGHT).next_to(axes[0].get_end(), RIGHT),
                       label("털", 20, ACCENT).next_to(axes[1].get_end(), UP),
                       label("얼굴 형태", 20, PRUNE).next_to(axes[2].get_end(), LEFT))
        axes.set_opacity(0)
        names.set_opacity(0)
        self.stage.add(axes, names)
        self.play(axes.animate.set_opacity(1), names.animate.set_opacity(1), run_time=.5)
        separated = self.feature_cloud(np.array([0, .2, 0]), separated=True, scale=1.35)
        self.play(*[cloud[i].animate.move_to(separated[i]) for i in range(len(separated))], run_time=1.15)
        self.to(15.4)

        # 3 — Establish the persistent two-lane comparison.
        self.copy(
            "같은 데이터, 같은 목표, 다른 학습 방식", "TWO REGIMES",
            "두 모델은 같은 예측 문제를 풉니다.\n차이는 어떤 내부 객체가 움직이는가입니다.",
        )
        board = LearningBoard()
        self.show(board)
        self.to(19.3)
        self.play(Indicate(board.left_vectors, color=SPARSE),
                  Indicate(board.right_vectors, color=GOOD), run_time=.8)
        self.to(23.2)

        # 4 — Feature-learning lane: rotate the basis itself.
        self.copy(
            "Feature Learning은 방향 자체를 바꿉니다", "vᵢ⁽⁰⁾ → vᵢ⁽ᵀ⁾",
            "왼쪽에서는 Feature 방향이 회전하고 재구성됩니다.\n표현 공간 자체가 데이터에 맞춰 움직입니다.",
        )
        self.play(
            Rotate(board.left_vectors[0], angle=32 * DEGREES, about_point=board.left_origin),
            Rotate(board.left_vectors[1], angle=-38 * DEGREES, about_point=board.left_origin),
            Rotate(board.left_vectors[2], angle=24 * DEGREES, about_point=board.left_origin),
            *[point.animate.move_to(board.left_origin + np.array(offset))
              for point, offset in zip(board.left_points, self.separated_offsets())],
            FadeOut(board.left_names), run_time=1.4,
        )
        new_names = VGroup(*[
            label(f"v{i + 1}′", 18, color).next_to(vec.get_end(), direction, buff=.08)
            for i, (vec, color, direction) in enumerate(zip(
                board.left_vectors, [WEIGHT, ACCENT, PRUNE], [RIGHT, UP, LEFT]
            ))
        ])
        board.add(new_names)
        self.play(FadeIn(new_names), Indicate(board.left_status, color=SPARSE), run_time=.45)
        self.to(32.0)

        # 5 — Lazy lane: fixed tangent features, changing coefficients.
        self.copy(
            "Lazy Learning은 초기 방향 근처에 머뭅니다", "vᵢ⁽⁰⁾ ≈ vᵢ⁽ᵀ⁾",
            "오른쪽에서는 초기 Feature 구조를 크게 바꾸지 않고\n그 Feature를 조합하는 계수로 출력을 맞춥니다.",
        )
        targets = ["1.4", "−.8", "2.1"]
        for token, value, color in zip(list(board.coefficients), targets, [WEIGHT, ACCENT, PRUNE]):
            replacement = card(value, color, .78, .58, 17, .18).move_to(token)
            self.play(ReplacementTransform(token, replacement), run_time=.28)
            board.coefficients.add(replacement)
        self.play(Indicate(board.right_vectors, color=GOOD), run_time=.6)
        self.to(40.8)

        # 6 — Same destination, distinct internal motion.
        self.copy(
            "둘 다 같은 예측에 도달할 수 있습니다", "SAME OUTPUT · DIFFERENT MOTION",
            "한쪽은 Feature를 움직이고 다른 쪽은 기존 Feature의 조합을 바꿉니다.\n성능만 보면 이 차이는 보이지 않습니다.",
        )
        left_acc = card("Accuracy = 95%", ACCENT, 2.8, .7, 20, .14).move_to([-2.05, 3.15, 0])
        right_acc = card("Accuracy = 95%", ACCENT, 2.8, .7, 20, .14).move_to([2.05, 3.15, 0])
        conclusion = card("같은 성능  ≠  같은 학습", PRUNE, 4.8, .72, 23, .14).move_to([0, -3.55, 0])
        board.add(left_acc, right_acc, conclusion)
        self.play(FadeIn(VGroup(left_acc, right_acc)), run_time=.35)
        self.play(FadeIn(conclusion), Indicate(left_acc, color=ACCENT),
                  Indicate(right_acc, color=ACCENT), run_time=.6)
        self.to(48.5)

        # 7 — Zoom into the lazy lane and show a local tangent plane.
        self.copy(
            "초기점 주변에서는 모델을 선형화할 수 있습니다", "θ = θ₀ + Δθ",
            "parameter 변화가 적절한 의미에서 작고 근사가 유지되면\n학습 궤적은 초기점 주변의 접선으로 설명될 수 있습니다.",
        )
        origin = Dot([-1.7, .15, 0], radius=.16, color=WEIGHT)
        neighborhood = Circle(radius=1.28, color=WEIGHT, stroke_opacity=.45,
                              fill_color=WEIGHT, fill_opacity=.035).move_to(origin)
        plane = Polygon([-.45, -.55, 0], [2.45, -.05, 0], [1.65, 1.65, 0], [-1.15, 1.05, 0],
                        color=SPARSE, fill_color=SPARSE, fill_opacity=.08, stroke_opacity=.65)
        endpoint = Dot([-.7, .7, 0], radius=.14, color=ACCENT)
        delta = Arrow(origin.get_center(), endpoint.get_center(), buff=.18,
                      color=ACCENT, stroke_width=4, tip_length=.16)
        path = route([origin.get_center(), [-1.45, .6, 0], [-1.1, .35, 0], endpoint.get_center()],
                     ACCENT, 3, .7, True)
        self.show(VGroup(plane, neighborhood, path, origin, endpoint, delta,
                         label("θ₀", 22, WEIGHT).next_to(origin, DOWN),
                         label("θ₀ + Δθ", 22, ACCENT).next_to(endpoint, UP),
                         label("local tangent plane", 20, SPARSE).move_to([1.35, -1.15, 0])))
        mover = origin.copy()
        self.stage.add(mover)
        self.play(MoveAlongPath(mover, path), run_time=1.1)
        self.to(57.4)

        # 8 — One central equation, split into fixed and learned parts.
        self.copy(
            "Lazy Learning의 핵심 근사", "LOCAL LINEARIZATION",
            "초기 모델과 초기 gradient가 만든 방향은 거의 고정되고\n학습은 그 방향을 얼마나 사용할지 결정합니다.",
        )
        formula = card("f(x;θ₀+Δθ) ≈ f(x;θ₀) + ∇θf(x;θ₀)ᵀ Δθ",
                       ACCENT, 7.5, 1.05, 25, .12).move_to([0, .85, 0])
        fixed = card("∇θf(x;θ₀)   ·   Tangent features", GOOD, 4.8, .76, 21, .12)
        fixed.move_to([-1.15, -.85, 0])
        learned = card("Δθ   ·   learned combination", SPARSE, 4.3, .76, 21, .12)
        learned.move_to([1.25, -2.05, 0])
        self.show(VGroup(formula, fixed, learned))
        self.play(Indicate(fixed, color=GOOD), run_time=.55)
        self.play(Indicate(learned, color=SPARSE), run_time=.55)
        self.to(66.2)

        # 9 — The parameter gradient becomes a tangent feature vector.
        self.copy(
            "초기 Jacobian이 Tangent Feature처럼 작동합니다", "φ(x) = ∇θ f(x;θ₀)",
            "모델을 parameter에 대해 미분한 긴 vector를\n입력 x가 가진 tangent feature로 볼 수 있습니다.",
        )
        bars = self.vector_bars([.45, .9, .3, .72, .55, .18, .82, .38], WEIGHT)
        bars.move_to([0, .45, 0])
        self.show(VGroup(bars,
                         label("∇θ f(x;θ₀)", 27, WEIGHT).move_to([0, 2.2, 0]),
                         card("Tangent Feature  φ(x)", GOOD, 4.5, .82, 24, .14)
                         .move_to([0, -2.0, 0])))
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=.07),
                  run_time=1.0)
        self.to(73.9)

        # 10 — Fixed feature arrows, moving coefficient sliders, changing output.
        self.copy(
            "Feature는 고정하고 조합만 바꿀 수 있습니다", "FIXED FEATURES  /  CHANGING Δθ",
            "phi 방향은 그대로 둔 채 delta theta 계수만 바꿔도\n결과 함수는 계속 변할 수 있습니다.",
        )
        features = VGroup(*[
            Arrow([-2.7 + i * 2.7, 1.1, 0], [-2.15 + i * 2.7, 2.0, 0], buff=0,
                  color=color, stroke_width=4, tip_length=.15)
            for i, color in enumerate([WEIGHT, ACCENT, PRUNE])
        ])
        sliders = VGroup()
        slider_dots = VGroup()
        for i, color in enumerate([WEIGHT, ACCENT, PRUNE]):
            track = Line([-3.35 + i * 2.7, -.15, 0], [-1.55 + i * 2.7, -.15, 0],
                         color=ZERO, stroke_width=6)
            dot = Dot(track.point_from_proportion(.2 + .18 * i), radius=.11, color=color)
            sliders.add(track); slider_dots.add(dot)
        output = self.wave_curve(amplitude=.65, frequency=1.0, color=GOOD, center=[0, -2.0, 0])
        self.show(VGroup(features, sliders, slider_dots, output,
                         label("φ₁", 19, WEIGHT).next_to(features[0], UP),
                         label("φ₂", 19, ACCENT).next_to(features[1], UP),
                         label("φ₃", 19, PRUNE).next_to(features[2], UP)))
        self.play(*[dot.animate.move_to(track.point_from_proportion(value))
                    for dot, track, value in zip(slider_dots, sliders, [.82, .35, .7])],
                  output.animate.stretch(1.28, 1), run_time=1.2)
        self.to(82.7)

        # 11 — Turn two inputs into tangent vectors, then take their dot product.
        self.copy(
            "두 입력의 Tangent Feature를 비교합니다", "NEURAL TANGENT KERNEL",
            "입력마다 tangent feature vector를 만들고\n두 vector의 내적으로 입력 사이의 관계를 정의합니다.",
        )
        xa = card("xA", WEIGHT, 1.15, .72, 22, .14).move_to([-3.2, .8, 0])
        xb = card("xB", PRUNE, 1.15, .72, 22, .14).move_to([-3.2, -.8, 0])
        va = self.vector_bars([.75, .35, .9, .55], WEIGHT).scale(.65).move_to([-.6, .8, 0])
        vb = self.vector_bars([.65, .25, .82, .45], PRUNE).scale(.65).move_to([-.6, -.8, 0])
        links = VGroup(Arrow(xa.get_right(), va.get_left(), buff=.15, color=MUTED, tip_length=.13),
                       Arrow(xb.get_right(), vb.get_left(), buff=.15, color=MUTED, tip_length=.13))
        formula = card("K(x,x′) = φ(x)ᵀ φ(x′)", ACCENT, 5.0, .86, 25, .14).move_to([0, -2.45, 0])
        self.show(VGroup(xa, xb, va, vb, links, formula,
                         label("φ(xA)", 20, WEIGHT).move_to([2.5, .8, 0]),
                         label("φ(xB)", 20, PRUNE).move_to([2.5, -.8, 0])))
        self.play(Indicate(va, color=WEIGHT), Indicate(vb, color=PRUNE), run_time=.7)
        self.to(90.5)

        # 12 — Width grows while the kernel matrix settles.
        self.copy(
            "특정 무한 폭 극한에서는 NTK가 거의 고정됩니다", "WIDTH → ∞  ·  K₀ ≈ Kₜ",
            "hidden neuron 수를 늘리는 특정 scaling limit에서는\nkernel matrix가 학습 중 거의 변하지 않는 그림이 나타납니다.",
        )
        net = self.network_icon(4, WEIGHT).move_to([-2.35, .25, 0])
        k0 = self.kernel_grid("K₀", [[1, .7, .2], [.7, 1, .35], [.2, .35, 1]], WEIGHT)
        kt = self.kernel_grid("Kₜ", [[1, .69, .21], [.69, 1, .34], [.21, .34, 1]], GOOD)
        kernels = VGroup(k0, label("≈", 34, ACCENT), kt).arrange(RIGHT, buff=.22).scale(.72)
        kernels.move_to([1.65, .15, 0])
        self.show(VGroup(net, kernels,
                         label("width = 4", 20, MUTED).move_to([-2.35, -2.0, 0])))
        wider = self.network_icon(10, WEIGHT).move_to(net)
        self.play(ReplacementTransform(net, wider), run_time=.8)
        self.play(Indicate(kernels, color=GOOD), run_time=.65)
        self.to(99.3)

        # 13 — Explicitly scope the claim.
        self.copy(
            "하지만 넓다고 언제나 Lazy한 것은 아닙니다", "WIDTH ALONE IS NOT ENOUGH",
            "parameterization과 scaling, 학습률과 초기화 같은\n학습 조건이 함께 Lazy regime을 결정합니다.",
        )
        claim = VGroup(card("Wide Network", WEIGHT, 2.7, .8, 22, .13),
                       label("→", 30, MUTED),
                       card("Lazy Learning", GOOD, 2.8, .8, 22, .13)).arrange(RIGHT, buff=.25)
        claim.move_to([0, 1.65, 0])
        cross = VGroup(Line([-3.1, 1.15, 0], [3.1, 2.15, 0], color=PRUNE, stroke_width=5),
                       Line([-3.1, 2.15, 0], [3.1, 1.15, 0], color=PRUNE, stroke_width=5))
        conditions = VGroup(*[
            card(name, color, 2.7, .66, 18, .1)
            for name, color in zip(["Scaling", "Initialization", "Learning rate", "Parameterization"],
                                   [SPARSE, ACCENT, GOOD, PRUNE])
        ]).arrange_in_grid(rows=2, cols=2, buff=.35).move_to([0, -.75, 0])
        self.show(VGroup(claim, cross, conditions))
        self.to(107.0)

        # 14 — Output function moves; the representation cloud barely does.
        self.copy(
            "출력은 크게 변해도 표현은 거의 그대로일 수 있습니다", "OUTPUT Δ LARGE  /  REPRESENTATION Δ SMALL",
            "prediction은 정답 곡선에 가까워지지만\nrepresentation cloud는 초기 상태 근처에 머물 수 있습니다.",
        )
        initial_curve = self.wave_curve(.25, .7, PRUNE, [-2.05, .7, 0], width=3.2)
        target_curve = self.wave_curve(.75, 1.2, ACCENT, [-2.05, .7, 0], width=3.2)
        cloud_before = self.feature_cloud(np.array([2.05, .65, 0]), False, .85).set_opacity(.3)
        cloud_after = self.feature_cloud(np.array([2.1, .7, 0]), False, .85)
        self.show(VGroup(initial_curve, cloud_before, cloud_after,
                         label("Prediction", 21, ACCENT).move_to([-2.05, 2.15, 0]),
                         label("Representation", 21, GOOD).move_to([2.05, 2.15, 0]),
                         self.meter("large change", .9, ACCENT).scale(.52).move_to([-2.05, -1.55, 0]),
                         self.meter("small change", .15, GOOD).scale(.52).move_to([2.05, -1.55, 0])))
        self.play(ReplacementTransform(initial_curve, target_curve), run_time=1.0)
        self.stage.add(target_curve)
        self.to(114.7)

        # 15 — Accuracy alone fades; internal before/after checks remain.
        self.copy(
            "정확도만으로는 두 방식을 구분할 수 없습니다", "COMPARE BEFORE ↔ AFTER",
            "학습 전후의 Feature 방향과 Jacobian, kernel을\n직접 비교해야 무엇이 움직였는지 알 수 있습니다.",
        )
        accuracy = card("Accuracy = 95%", ACCENT, 3.5, .76, 23, .14).move_to([0, 2.15, 0])
        rows = VGroup(
            self.change_row("Feature arrows", "rotated?", SPARSE),
            self.change_row("Jacobian", "changed?", WEIGHT),
            self.change_row("Kernel K", "changed?", GOOD),
        ).arrange(DOWN, buff=.38).move_to([0, -.45, 0])
        self.show(VGroup(accuracy, rows))
        self.play(accuracy.animate.set_opacity(.18), run_time=.55)
        self.play(LaggedStart(*[Indicate(row, color=ACCENT) for row in rows], lag_ratio=.15),
                  run_time=.85)
        self.to(122.5)

        # 16 — The regimes are endpoints on a continuum.
        self.copy(
            "실제 모델은 두 극단 사이에 있을 수 있습니다", "A CONTINUUM, NOT A BINARY",
            "Feature Learning과 Lazy Learning은 유용한 두 극단입니다.\n실제 모델은 Feature와 조합을 함께 바꿀 수 있습니다.",
        )
        line = Line([-3.15, .3, 0], [3.15, .3, 0], color=MUTED, stroke_width=5)
        ticks = VGroup(*[Line([x, .08, 0], [x, .52, 0], color=MUTED, stroke_width=2)
                         for x in np.linspace(-3.15, 3.15, 9)])
        models = VGroup(*[
            Dot([x, .3, 0], radius=.13, color=color)
            for x, color in zip([-2.5, -1.15, .2, 1.45, 2.55],
                                [SPARSE, WEIGHT, ACCENT, GOOD, PRUNE])
        ])
        self.show(VGroup(line, ticks, models,
                         label("Feature Learning", 21, SPARSE).move_to([-2.45, 1.1, 0]),
                         label("Lazy Learning", 21, GOOD).move_to([2.45, 1.1, 0]),
                         card("different models · different regimes", ACCENT, 5.8, .76, 21, .13)
                         .move_to([0, -1.75, 0])))
        self.play(LaggedStart(*[Indicate(dot, color=dot.get_color()) for dot in models], lag_ratio=.1),
                  run_time=.8)
        self.to(129.1)

        # 17 — Separate prediction learning from feature learning.
        self.copy(
            "모델의 학습과 Feature Learning은 같은 말이 아닙니다", "PREDICTION LEARNING  ≠  FEATURE LEARNING",
            "성능이 좋아졌다는 사실만으로\n새로운 Feature가 생겼다고 결론 내릴 수 없습니다.",
        )
        prediction = card("Prediction Learning", GOOD, 5.1, .9, 25, .15).move_to([0, 1.5, 0])
        relation = label("=", 48, ACCENT).move_to([0, .1, 0])
        feature = card("Feature Learning", SPARSE, 5.1, .9, 25, .15).move_to([0, -1.3, 0])
        self.show(VGroup(prediction, relation, feature))
        not_equal = label("≠", 48, PRUNE).move_to(relation)
        self.play(FadeOut(relation), FadeIn(not_equal), run_time=.5)
        self.stage.add(not_equal)
        self.to(134.6)

        # 18 — Visual bridge to Spectral Bias.
        self.copy(
            "그렇다면 여러 패턴 중 무엇부터 배울까요?", "NEXT · SPECTRAL BIAS",
            "다음에는 완만한 패턴과 빠른 진동이 함께 있을 때\n신경망이 어떤 성분부터 따라가는지 살펴보겠습니다.",
        )
        target = self.composite_wave(ACCENT).move_to([0, .55, 0])
        learned = self.wave_curve(.9, .55, GOOD, [0, .55, 0], width=6.4)
        self.show(VGroup(target, learned,
                         label("target = slow wave + fast ripple", 20, ACCENT).move_to([0, 2.25, 0]),
                         label("model first follows the broad pattern", 21, GOOD).move_to([0, -1.85, 0])))
        self.play(Create(learned), run_time=.8)
        self.to(139.0)

    def grokking_chart(self):
        x_axis = Arrow([-3.0, -1.45, 0], [3.1, -1.45, 0], buff=0,
                       color=MUTED, stroke_width=2.3, tip_length=.14)
        y_axis = Arrow([-3.0, -1.45, 0], [-3.0, 2.1, 0], buff=0,
                       color=MUTED, stroke_width=2.3, tip_length=.14)
        train = VGroup(
            CubicBezier([-2.9, -1.2, 0], [-2.7, -.5, 0], [-2.45, 1.55, 0], [-2.0, 1.65, 0],
                        color=GOOD, stroke_width=5),
            Line([-2.0, 1.65, 0], [2.85, 1.65, 0], color=GOOD, stroke_width=5),
        )
        test = VGroup(
            Line([-2.9, -1.1, 0], [.45, -1.05, 0], color=PRUNE, stroke_width=5),
            CubicBezier([.45, -1.05, 0], [.9, -.9, 0], [1.2, 1.45, 0], [1.85, 1.6, 0],
                        color=PRUNE, stroke_width=5),
            Line([1.85, 1.6, 0], [2.85, 1.65, 0], color=PRUNE, stroke_width=5),
        )
        return VGroup(x_axis, y_axis, train, test,
                      label("Train Accuracy = 100%", 19, GOOD).move_to([1.3, 2.0, 0]),
                      label("Test", 19, PRUNE).move_to([2.5, 1.2, 0]))

    def separated_offsets(self):
        return [
            [-1.0, .75, 0], [-.65, .95, 0], [-.3, .62, 0], [.05, .9, 0], [.4, .58, 0],
            [-.35, -.72, 0], [0, -.95, 0], [.35, -.68, 0], [.7, -.92, 0], [1.0, -.62, 0],
        ]

    def feature_cloud(self, center, separated=False, scale=1.0):
        offsets = self.separated_offsets() if separated else [
            [-.95, .45, 0], [-.55, -.35, 0], [-.15, .72, 0], [.3, -.52, 0], [.75, .2, 0],
            [-.75, -.62, 0], [-.32, .12, 0], [.08, -.05, 0], [.48, .62, 0], [.9, -.28, 0],
        ]
        colors = [WEIGHT] * 5 + [PRUNE] * 5
        return VGroup(*[
            Dot(center + np.array(offset) * scale, radius=.085, color=color, fill_opacity=.8)
            for offset, color in zip(offsets, colors)
        ])

    def vector_bars(self, values, color):
        bars = VGroup()
        for i, value in enumerate(values):
            height = .35 + 1.55 * value
            bar = RoundedRectangle(width=.48, height=height, corner_radius=.08,
                                   stroke_color=color, stroke_width=1.5,
                                   fill_color=color, fill_opacity=.18 + .35 * value)
            bar.move_to([(i - (len(values) - 1) / 2) * .65, -1 + height / 2, 0])
            bars.add(bar)
        return bars

    def wave_curve(self, amplitude, frequency, color, center, width=6.0):
        xs = np.linspace(-width / 2, width / 2, 100)
        points = [np.array([center[0] + x, center[1] + amplitude * np.sin(frequency * x * 2), 0])
                  for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.9)
        curve.set_points_smoothly(points)
        return curve

    def composite_wave(self, color):
        xs = np.linspace(-3.2, 3.2, 180)
        points = [np.array([x, .8 * np.sin(1.1 * x) + .22 * np.sin(7.5 * x), 0]) for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.85)
        curve.set_points_smoothly(points)
        return curve

    def network_icon(self, hidden_count, color):
        left = VGroup(*[Dot([-1.0, y, 0], radius=.08, color=MUTED) for y in [-.65, 0, .65]])
        ys = np.linspace(-1.05, 1.05, hidden_count)
        hidden = VGroup(*[Dot([0, y, 0], radius=.055 if hidden_count > 6 else .08, color=color)
                          for y in ys])
        right = VGroup(*[Dot([1.0, y, 0], radius=.08, color=GOOD) for y in [-.45, .45]])
        links = VGroup(*[
            Line(a.get_center(), b.get_center(), color=ZERO, stroke_width=.8, stroke_opacity=.35)
            for group_a, group_b in [(left, hidden), (hidden, right)] for a in group_a for b in group_b
        ])
        return VGroup(links, left, hidden, right)

    def change_row(self, name, question, color):
        frame = RoundedRectangle(width=6.3, height=.9, corner_radius=.16,
                                 color=color, fill_color=color, fill_opacity=.04, stroke_width=2)
        before = VGroup(*[Line([-.15, 0, 0], [.15, h, 0], color=MUTED, stroke_width=3)
                          for h in [.25, .5, .75]]).arrange(RIGHT, buff=.12)
        after = before.copy().set_color(color)
        before.move_to([-.65, 0, 0]); after.move_to([.85, 0, 0])
        arrow = Arrow([-.15, 0, 0], [.35, 0, 0], buff=0, color=MUTED, tip_length=.1)
        return VGroup(frame, label(name, 19, color).move_to([-2.0, 0, 0]),
                      before, arrow, after, label(question, 17, MUTED).move_to([2.25, 0, 0]))

    def kernel_grid(self, title, values, color):
        cells = VGroup()
        for r, row in enumerate(values):
            for c, value in enumerate(row):
                opacity = .06 + .25 * float(value)
                box = Square(side_length=.68, stroke_color=color, stroke_width=1.5,
                             fill_color=color, fill_opacity=opacity)
                box.move_to([(c - 1) * .72, (1 - r) * .72, 0])
                cells.add(VGroup(box, label(f"{value:g}", 16, INK).move_to(box)))
        return VGroup(label(title, 20, color).move_to([0, 1.45, 0]), cells)

    def meter(self, title, value, color):
        frame = RoundedRectangle(width=6.3, height=1.35, corner_radius=.18,
                                 color=color, fill_color=color, fill_opacity=.035,
                                 stroke_width=2)
        track = RoundedRectangle(width=4.6, height=.4, corner_radius=.1,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.4)
        fill = RoundedRectangle(width=max(.14, 4.25 * value), height=.24, corner_radius=.07,
                                stroke_width=0, fill_color=color, fill_opacity=.95)
        fill.align_to(track, LEFT).shift(RIGHT * .18)
        gauge = VGroup(track, fill).move_to([.45, -.2, 0])
        return VGroup(frame, label(title, 19, color).move_to([-1.8, .32, 0]), gauge)

    def before_after_panel(self, title, color, rotate):
        box = RoundedRectangle(width=3.55, height=4.45, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035,
                               stroke_width=2.3)
        before_origin = np.array([-.75, .35, 0])
        after_origin = np.array([.75, .35, 0])
        before = Arrow(before_origin, before_origin + np.array([.35, 1.0, 0]), buff=0,
                       color=MUTED, stroke_width=3, tip_length=.13)
        after_delta = np.array([.85, .62, 0]) if rotate else np.array([.35, 1.0, 0])
        after = Arrow(after_origin, after_origin + after_delta, buff=0,
                      color=color, stroke_width=4, tip_length=.13)
        arrow = Arrow([-.25, .35, 0], [.25, .35, 0], buff=0,
                      color=MUTED, stroke_width=2, tip_length=.11)
        note = "angle changed" if rotate else "same direction"
        if not rotate:
            weight_before = label("× .2", 18, MUTED).move_to([-.75, -.65, 0])
            weight_after = label("× 1.4", 18, color).move_to([.75, -.65, 0])
            extra = VGroup(weight_before, weight_after)
        else:
            extra = VGroup()
        return VGroup(box, label(title, 18, color, 3.15).move_to([0, 1.65, 0]),
                      before, after, arrow, extra,
                      label(note, 19, color).move_to([0, -1.45, 0]))

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 28).move_to(UP * 5.12)
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
            self.remove(self.stage)
        self.stage = new_stage
        self.add(self.stage)
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        end_x = -3.8 + max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.put_start_and_end_on(
                np.array([-3.8, -7.36, 0]), np.array([end_x, -7.36, 0])),
                run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
