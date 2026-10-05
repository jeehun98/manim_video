"""Neural Network Mathematics Part 2, episode 09: Edge of Stability."""
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
    box = RoundedRectangle(width=width, height=height, corner_radius=.16,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=fill)
    return VGroup(box, label(value, size, color, width - .24))


class NeuralMathPart2EdgeOfStability(Scene):
    DURATION = 256

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 09", 17, MUTED).move_to(UP * 7.3),
            label("Edge of Stability · 왜 불안정해지기 직전까지 학습할까?", 25).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        # 1 — Ordinary gradient-descent intuition.
        self.copy("Gradient Descent는 기울기를 따라 이동합니다", "FOLLOW THE LOCAL SLOPE",
                  "작은 Learning Rate는 조금씩, 적당한 값은 더 빠르게 움직입니다.\n너무 크면 최소점을 반복해서 넘어가 수렴하지 못할 수 있습니다.")
        panels = VGroup(self.lr_panel("SMALL η", GOOD, .32),
                        self.lr_panel("GOOD η", SPARSE, .58),
                        self.lr_panel("TOO LARGE", PRUNE, 1.12))
        panels.arrange(RIGHT, buff=.18).scale(.93).move_to([0, .15, 0])
        self.show(panels)
        self.play(LaggedStart(*[Create(p[2]) for p in panels], lag_ratio=.2), run_time=1.2)
        self.to(16)

        # 2 — Same learning rate, different curvature.
        self.copy("안정성을 결정하는 것은 η뿐일까요?", "SAME STEP · DIFFERENT CURVATURE",
                  "같은 Learning Rate라도 넓은 골짜기에서는 안전하고,\n좁고 가파른 골짜기에서는 최소점을 크게 넘어갈 수 있습니다.")
        valleys = self.curvature_compare()
        self.show(valleys)
        self.play(LaggedStart(Create(valleys[0][2]), Create(valleys[1][2]), lag_ratio=.25), run_time=1.1)
        self.to(31)

        # 3 — Define curvature visually before using lambda.
        self.copy("Loss가 얼마나 심하게 휘었는지도 중요합니다", "THIS IS CURVATURE",
                  "완만한 곡선은 기울기가 천천히 바뀌고,\n가파른 곡선은 같은 거리에서도 기울기가 빠르게 바뀝니다.")
        broad = self.curvature_card("LOW CURVATURE", WEIGHT, .38).move_to([-1.9, .25, 0])
        sharp = self.curvature_card("HIGH CURVATURE", ACCENT, 1.15).move_to([1.9, .25, 0])
        self.show(VGroup(broad, sharp, card("curvature  =  λ", SPARSE, 4.0, .72, 26, .13)
                         .move_to([0, -2.35, 0])))
        self.to(43)

        # 4 — Derive the update multiplier instead of stating the answer.
        self.copy("가장 단순한 Quadratic에서 직접 계산해봅시다", "WHY DOES THE BOUNDARY EQUAL 2?",
                  "L(θ)=½λθ²이면 gradient는 λθ입니다.\n다음 위치는 현재 위치에서 ηλθ를 뺀 값입니다.")
        derivation = VGroup(
            card("L(θ) = ½ λθ²", WEIGHT, 5.1, .78, 29, .1),
            label("↓  gradient", 21, MUTED),
            card("∇L(θ) = λθ", SPARSE, 5.1, .78, 29, .11),
            label("↓  update", 21, MUTED),
            card("θₜ₊₁ = θₜ − ηλθₜ", ACCENT, 5.7, .84, 29, .14),
        ).arrange(DOWN, buff=.22).move_to([0, .15, 0])
        self.show(derivation)
        self.to(59)

        # 5 — The whole stability story is in the multiplier.
        self.copy("다음 위치는 하나의 multiplier로 정리됩니다", "THE UPDATE MULTIPLIER",
                  "θₜ₊₁=(1−ηλ)θₜ.\n1−ηλ의 크기와 부호가 다음 위치와 진동의 폭을 결정합니다.")
        multiplier = card("θₜ₊₁ = (1 − ηλ) θₜ", ACCENT, 6.4, 1.05, 38, .16).move_to([0, .85, 0])
        guide = VGroup(card("|1−ηλ| < 1", GOOD, 2.9, .72, 23, .12),
                       label("→", 26, MUTED), card("amplitude shrinks", GOOD, 3.1, .72, 20, .1))
        guide.arrange(RIGHT, buff=.18).move_to([0, -1.25, 0])
        self.show(VGroup(multiplier, guide))
        self.to(70)

        # 6 — eta lambda = 0.5.
        self.copy("ηλ = 0.5이면 매번 절반으로 줄어듭니다", "0.5 → NO SIGN FLIP · CONVERGES",
                  "multiplier는 0.5입니다. 위치는 1, 0.5, 0.25처럼\n같은 쪽에서 최소점으로 가까워집니다.")
        self.show(self.recurrence_panel("ηλ = 0.5", [1, .5, .25, .125], GOOD))
        self.to(80)

        # 7 — eta lambda = 1.5.
        self.copy("ηλ = 1.5이면 부호가 바뀌어도 수렴합니다", "1.5 → SIGN FLIPS · STILL CONVERGES",
                  "multiplier는 −0.5입니다. 최소점을 좌우로 넘지만\n이동 폭은 절반씩 줄어들기 때문에 여전히 수렴합니다.")
        self.show(self.recurrence_panel("ηλ = 1.5", [1, -.5, .25, -.125], SPARSE))
        self.to(92)

        # 8 — eta lambda = 2 makes the amplitude stop shrinking.
        self.copy("ηλ = 2에서는 더 이상 가까워지지 않습니다", "2 → SIGN FLIPS · NO SHRINKING",
                  "multiplier는 −1입니다. 1에서 시작하면 −1, 다시 1, 다시 −1.\n최소점을 넘지만 진동의 폭은 그대로입니다.")
        boundary = self.recurrence_panel("ηλ = 2", [1, -1, 1, -1], ACCENT)
        self.show(boundary)
        self.play(Indicate(boundary[0], color=ACCENT), run_time=.8)
        self.to(105)

        # 9 — Now the classical boundary is motivated.
        self.copy("그래서 단순한 Quadratic의 경계는 2입니다", "CLASSICAL STABILITY CONDITION",
                  "진동의 폭이 줄려면 |1−ηλ|<1이어야 합니다.\n따라서 simple Gradient Descent의 안정 영역은 0<ηλ<2입니다.")
        formula = card("0  <  ηλ  <  2", GOOD, 5.0, 1.0, 37, .15).move_to([0, 1.15, 0])
        self.show(VGroup(formula, self.stability_line().move_to([0, -.75, 0]),
                         card("fixed 1D quadratic", MUTED, 4.1, .64, 18, .06).move_to([0, -2.4, 0])))
        self.to(117)

        # 10 — Make the transition to neural networks explicit.
        self.copy("여기까지는 고정된 Loss 지형의 이야기입니다", "WHAT CHANGES IN A NEURAL NETWORK?",
                  "처음에 안전한 η를 골랐다면 계속 안전할 것 같지만,\n신경망에서는 parameter 자체가 학습 중 계속 이동합니다.")
        chain = VGroup(card("choose η", GOOD, 2.2, .78, 23, .12), label("→", 28, MUTED),
                       card("start stable", WEIGHT, 2.5, .78, 22, .1), label("→", 28, MUTED),
                       card("always stable?", ACCENT, 2.7, .78, 22, .13))
        chain.arrange(RIGHT, buff=.15).move_to([0, .4, 0])
        self.show(VGroup(chain, label("parameter θ keeps moving", 26, SPARSE).move_to([0, -1.45, 0])))
        self.to(128)

        # 11 — Move from broad to sharp local geometry.
        self.copy("모델이 경험하는 local curvature가 변합니다", "BROAD REGION → SHARP REGION",
                  "처음에는 완만한 영역에 있어도 학습하면서 더 좁은 영역으로 이동할 수 있습니다.\nη는 그대로지만 Hessian의 최대 고유값 λₘₐₓ가 커집니다.")
        landscape = self.landscape()
        self.show(landscape)
        self.play(MoveAlongPath(landscape[-1], landscape[-2]), run_time=1.25, rate_func=smooth)
        self.to(142)

        # 12 — Keep the concrete numerical example intact.
        self.copy("η = 0.01을 끝까지 고정해봅시다", "η IS NOT CHANGING",
                  "λₘₐₓ가 20, 100, 190으로 증가하면\nηλₘₐₓ는 0.2, 1.0, 1.9로 경계 2에 접근합니다.")
        numeric = self.numeric_example()
        self.show(numeric)
        self.play(LaggedStart(*[Indicate(row, color=[GOOD, SPARSE, ACCENT][i])
                                for i, row in enumerate(numeric[2:5])], lag_ratio=.25), run_time=1.4)
        self.to(160)

        # 13 — State the interpretation of the numbers.
        self.copy("Learning Rate를 키워서 경계에 간 것이 아닙니다", "FIXED η · CHANGING LANDSCAPE",
                  "한 번도 바뀌지 않은 η에, 모델이 새 위치에서 경험하는 λₘₐₓ가 곱해집니다.\n그래서 같은 step size의 안정성이 달라집니다.")
        eta = self.gauge("LEARNING RATE  η = 0.01", .42, ACCENT, "FIXED", [0, 1.7, 0])
        lam = self.gauge("SHARPNESS  λₘₐₓ", .91, SPARSE, "RISING", [0, .05, 0])
        product = self.product_gauge(.92).move_to([0, -2.0, 0])
        self.show(VGroup(eta, lam, product))
        self.to(171)

        # 14 — Track measured sharpness toward 2/eta.
        self.copy("실제 학습에서도 λₘₐₓ가 경계로 상승할 수 있습니다", "TRACK THE LARGEST HESSIAN EIGENVALUE",
                  "λₘₐₓ를 추적하면 값이 증가해 classical boundary인\n2/η 부근에 도달하는 현상이 관찰될 수 있습니다.")
        early = self.sharpness_graph(.38, False)
        near = self.sharpness_graph(.97, False)
        self.show(early)
        self.play(ReplacementTransform(early, near), run_time=1.2)
        self.stage = near
        self.to(184)

        # 15 — Fixed quadratic intuition predicts failure, but training persists.
        self.copy("고정 Quadratic의 직관이라면 곧 무너질 것 같습니다", "THE SURPRISE",
                  "하지만 신경망 학습은 바로 끝나지 않을 수 있습니다.\ncurvature가 경계 부근에서 움직이면서도 학습이 계속됩니다.")
        graph = self.sharpness_graph(.99, True)
        question = card("DIVERGE NOW?", PRUNE, 3.5, .72, 23, .11).move_to([0, -2.35, 0])
        self.show(VGroup(graph, question))
        answer = card("TRAINING CONTINUES", GOOD, 4.4, .72, 23, .13).move_to(question)
        self.play(ReplacementTransform(question, answer), run_time=.8)
        self.stage = VGroup(graph, answer)
        self.to(196)

        # 16 — Show the loss dynamics, not just sharpness.
        self.copy("Loss도 매 step 부드럽게 감소하지 않습니다", "OSCILLATION WITH LONG-TERM PROGRESS",
                  "일부 step에서는 Loss가 증가하고 진동할 수 있습니다.\n하지만 더 긴 시간에서 보면 학습은 계속 진행될 수 있습니다.")
        loss = self.loss_plot(True).move_to([0, .45, 0])
        self.show(loss)
        self.to(208)

        # 17 — Name the phenomenon after both observables are visible.
        self.copy("이 예상 밖의 dynamics가 Edge of Stability입니다", "NEAR THE CLASSICAL BOUNDARY",
                  "classical stability boundary 부근에서 curvature와 Loss가 진동해도\n학습이 이어질 수 있는 현상을 Edge of Stability라고 합니다.")
        summary = self.summary_panel()
        name = card("EDGE OF STABILITY", ACCENT, 5.7, .85, 29, .16).move_to([0, -2.55, 0])
        self.show(VGroup(summary, name))
        self.to(219)

        # 18 — Re-emphasize the causal sequence.
        self.copy("모델이 처음부터 경계에 있었던 것은 아닙니다", "PARAMETERS MOVE → CURVATURE CHANGES",
                  "parameter 이동이 local geometry를 바꾸고,\n그 결과 같은 Learning Rate의 안정성도 위치에 따라 달라집니다.")
        chain = self.geometry_chain()
        self.show(chain)
        self.play(LaggedStart(*[Indicate(item, color=[WEIGHT, SPARSE, ACCENT][i])
                                for i, item in enumerate(chain[::2])], lag_ratio=.2), run_time=1.1)
        self.to(230)

        # 19 — Separate the edge from divergence.
        self.copy("불안정할수록 좋다는 뜻은 아닙니다", "EDGE  ≠  UNLIMITED INSTABILITY",
                  "η가 지나치게 크거나 안정 범위를 크게 벗어나면 실제로 발산합니다.\n핵심은 고전적 경계 부근에서도 학습이 이어질 수 있다는 점입니다.")
        strip = self.region_strip()
        self.show(strip)
        self.play(Indicate(strip[1], color=ACCENT), run_time=.8)
        self.to(240)

        # 20 — Connect to the previous spectrum episode precisely.
        self.copy("이번에는 spectrum의 가장 큰 값에 주목합니다", "λᵢ: LEARNING SPEED · λₘₐₓ: STABILITY",
                  "가장 큰 eigenvalue는 curvature가 가장 높은 방향입니다.\n같은 η에서 안정성 문제가 가장 먼저 나타날 수 있는 방향이기도 합니다.")
        spectrum = self.spectrum(big=True).move_to([0, .65, 0])
        formula = card("η λₘₐₓ  ≈  2", ACCENT, 4.4, .86, 31, .15).move_to([0, -2.05, 0])
        self.show(VGroup(spectrum, formula))
        self.play(Indicate(spectrum[-1], color=ACCENT), run_time=.8)
        self.to(249)

        # 21 — Final statement.
        self.copy("좋은 학습이 항상 매끄러운 하강일 필요는 없습니다", "THE EDGE OF STABILITY",
                  "η가 그대로여도 curvature는 변할 수 있습니다.\n안정성과 불안정성의 경계에서 이어지는 dynamics가 Edge of Stability입니다.")
        final = VGroup(card("η fixed", WEIGHT, 3.0, .72, 24, .1), label("+", 29, MUTED),
                       card("λₘₐₓ ↑", SPARSE, 3.0, .72, 25, .12), label("→", 29, MUTED),
                       card("η λₘₐₓ ≈ 2", ACCENT, 4.2, .88, 31, .16), label("↓", 30, MUTED),
                       card("EDGE OF STABILITY", GOOD, 6.0, .92, 29, .15))
        final.arrange(DOWN, buff=.2).move_to([0, .2, 0])
        self.show(final)
        self.to(256)

    def curvature_compare(self):
        def panel(title, color, sharpness, ratio):
            frame = RoundedRectangle(width=3.55, height=4.45, corner_radius=.2,
                                     color=color, fill_color=color, fill_opacity=.025,
                                     stroke_width=2)
            xs = np.linspace(-1.45, 1.45, 100)
            points = [np.array([x, -1.0 + sharpness * x * x, 0]) for x in xs]
            bowl = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.9)
            bowl.set_points_smoothly(points)
            values = [1.25]
            for i in range(1, 6):
                values.append((-1) ** i * abs(values[-1]) * ratio)
            path_points = [np.array([x, -1.0 + sharpness * x * x, 0]) for x in values]
            path = VMobject(stroke_color=GOOD if ratio < .7 else PRUNE,
                            stroke_width=3.5, stroke_opacity=.95)
            path.set_points_as_corners(path_points)
            return VGroup(frame, bowl, path,
                          label(title, 20, color).move_to([0, 1.75, 0]),
                          card("same η", ACCENT, 1.7, .52, 16, .1).move_to([0, -1.7, 0]))
        broad = panel("BROAD VALLEY", WEIGHT, .42, .38)
        sharp = panel("SHARP VALLEY", ACCENT, 1.08, .94)
        return VGroup(broad, sharp).arrange(RIGHT, buff=.35).move_to([0, .15, 0])

    def curvature_card(self, title, color, sharpness):
        frame = RoundedRectangle(width=3.45, height=4.05, corner_radius=.2,
                                 color=color, fill_color=color, fill_opacity=.025,
                                 stroke_width=2)
        xs = np.linspace(-1.35, 1.35, 100)
        points = [np.array([x, -1.0 + sharpness * x * x, 0]) for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.93)
        curve.set_points_smoothly(points)
        left_tangent = Line([-.85, -.6, 0], [-.35, -.98, 0], color=MUTED, stroke_width=2)
        right_tangent = Line([.35, -.98, 0], [.85, -.6, 0], color=MUTED, stroke_width=2)
        return VGroup(frame, curve, left_tangent, right_tangent,
                      label(title, 19, color).move_to([0, 1.62, 0]))

    def recurrence_panel(self, title, values, color):
        heading = card(title, color, 3.4, .76, 28, .14).move_to([0, 2.3, 0])
        line = Line([-3.1, .35, 0], [3.1, .35, 0], color=MUTED, stroke_width=2)
        center = Line([0, .05, 0], [0, .65, 0], color=ACCENT, stroke_width=3)
        dots = VGroup()
        arrows = VGroup()
        scale = 2.35
        for i, value in enumerate(values):
            dots.add(VGroup(Dot([scale * value, .35, 0], radius=.115, color=color),
                            label(str(i), 15, color).move_to([scale * value, .83, 0])))
            if i:
                arrows.add(CurvedArrow([scale * values[i - 1], .18, 0],
                                       [scale * value, .18, 0], angle=.32,
                                       color=color, stroke_width=2.5, tip_length=.14))
        seq = "  →  ".join(f"{v:g}" for v in values)
        sequence = card(seq, color, 6.2, .78, 25, .1).move_to([0, -1.35, 0])
        verdict = card("amplitude shrinks" if abs(values[-1]) < .5 else "amplitude stays 1",
                       GOOD if abs(values[-1]) < .5 else ACCENT,
                       4.4, .66, 20, .11).move_to([0, -2.35, 0])
        return VGroup(heading, line, center, arrows, dots, sequence, verdict,
                      label("minimum", 16, ACCENT).move_to([0, -.15, 0]))

    def numeric_example(self):
        eta = card("η = 0.01  FIXED", ACCENT, 4.2, .78, 28, .14).move_to([0, 2.45, 0])
        header = VGroup(label("λₘₐₓ", 19, SPARSE).move_to([-2.05, 1.4, 0]),
                        label("×  η", 19, MUTED).move_to([0, 1.4, 0]),
                        label("ηλₘₐₓ", 19, GOOD).move_to([2.05, 1.4, 0]))
        rows = []
        for lam, product, color in [(20, .2, GOOD), (100, 1.0, SPARSE), (190, 1.9, ACCENT)]:
            row = VGroup(card(str(lam), color, 1.55, .7, 24, .1), label("× 0.01 =", 22, MUTED),
                         card(f"{product:g}", color, 1.55, .7, 25, .13))
            row.arrange(RIGHT, buff=.3)
            rows.append(row)
        rows_group = VGroup(*rows).arrange(DOWN, buff=.34).move_to([0, -.25, 0])
        boundary = VGroup(label("0", 17, MUTED), Line([0, 0, 0], [4.5, 0, 0], color=ZERO, stroke_width=8),
                          Line([4.5, -.25, 0], [4.5, .25, 0], color=ACCENT, stroke_width=4),
                          label("2", 20, ACCENT)).arrange(RIGHT, buff=.08).scale(.75).move_to([0, -2.45, 0])
        return VGroup(eta, header, *rows, boundary)

    def bowl(self, color, width=6.0, height=2.5):
        xs = np.linspace(-width / 2, width / 2, 100)
        points = [np.array([x, -1.15 + height * (x / (width / 2)) ** 2, 0]) for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.9)
        curve.set_points_smoothly(points)
        return curve

    def zigzag_path(self, ratio, color):
        xs = [-2.65]
        for i in range(1, 7):
            xs.append((-1) ** i * abs(xs[-1]) * ratio)
        points = [[x, -1.15 + 2.7 * (x / 3.15) ** 2, 0] for x in xs]
        path = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.95)
        path.set_points_as_corners([np.array(p) for p in points])
        return path

    def lr_panel(self, title, color, ratio):
        frame = RoundedRectangle(width=2.45, height=4.0, corner_radius=.18,
                                 color=color, fill_color=color, fill_opacity=.025, stroke_width=1.8)
        bowl = self.bowl(MUTED, 2.05, 1.2).scale(.88).move_to([0, -.2, 0])
        path = self.zigzag_path(ratio, color).scale(.31).move_to([0, -.2, 0])
        state = "CONVERGE" if ratio < 1 else "DIVERGE"
        return VGroup(frame, label(title, 17, color).move_to([0, 1.55, 0]), path,
                      bowl, label(state, 16, color).move_to([0, -1.55, 0]))

    def stability_line(self):
        line = Line([-3.2, 0, 0], [3.2, 0, 0], color=MUTED, stroke_width=4)
        boundary = Line([.65, -.32, 0], [.65, .32, 0], color=ACCENT, stroke_width=5)
        stable = Line([-3.0, 0, 0], [.58, 0, 0], color=GOOD, stroke_width=9)
        unstable = Line([.72, 0, 0], [3.0, 0, 0], color=PRUNE, stroke_width=9)
        return VGroup(line, stable, unstable, boundary,
                      label("0", 18, MUTED).move_to([-3.0, -.48, 0]),
                      label("2", 21, ACCENT).move_to([.65, -.5, 0]),
                      label("STABLE", 18, GOOD).move_to([-1.25, .55, 0]),
                      label("UNSTABLE", 18, PRUNE).move_to([1.9, .55, 0]),
                      label("ηλ", 19, INK).move_to([3.35, -.05, 0]))

    def sharpness_graph(self, fraction, oscillate=False):
        origin = np.array([-2.9, -1.55, 0])
        x_axis = Line(origin, origin + RIGHT * 5.9, color=MUTED, stroke_width=1.7)
        y_axis = Line(origin, origin + UP * 3.65, color=MUTED, stroke_width=1.7)
        boundary_y = origin[1] + 3.0
        boundary = DashedLine([origin[0], boundary_y, 0], [origin[0] + 5.9, boundary_y, 0],
                              color=ACCENT, dash_length=.12, stroke_width=2.5)
        ts = np.linspace(0, 1, 130)
        base = .35 + 2.62 * (1 - np.exp(-4.0 * ts)) * fraction
        if oscillate:
            base += .14 * np.sin(36 * ts) * np.clip((ts - .43) * 2.0, 0, 1)
        points = [np.array([origin[0] + 5.75 * t, origin[1] + y, 0]) for t, y in zip(ts, base)]
        curve = VMobject(stroke_color=SPARSE, stroke_width=4, stroke_opacity=.95)
        curve.set_points_smoothly(points)
        return VGroup(x_axis, y_axis, boundary, curve,
                      label("2/η", 20, ACCENT).move_to([3.35, boundary_y + .28, 0]),
                      label("λₘₐₓ", 19, SPARSE).move_to([-3.2, 2.15, 0]),
                      label("training step", 18, MUTED).move_to([1.7, -1.95, 0]))

    def spectrum(self, big=False):
        heights = [.45, .75, 1.05, 1.45, 2.15 if big else 1.7]
        bars = VGroup()
        for i, height in enumerate(heights):
            color = ACCENT if i == len(heights) - 1 else WEIGHT
            bar = RoundedRectangle(width=.62, height=height, corner_radius=.08,
                                   stroke_width=0, fill_color=color, fill_opacity=.88)
            bars.add(VGroup(bar, label("λₘₐₓ" if i == 4 else f"λ{i+1}", 15, color)
                            .next_to(bar, DOWN, buff=.13)))
        bars.arrange(RIGHT, buff=.42, aligned_edge=DOWN)
        return bars

    def landscape(self):
        broad = self.bowl(WEIGHT, 6.7, 1.2).move_to([-1.2, .35, 0])
        narrow = self.bowl(ACCENT, 2.0, 2.7).move_to([2.15, .35, 0])
        route = CubicBezier([-3.0, 1.55, 0], [-1.2, .2, 0], [.7, -.65, 0], [2.15, -1.03, 0])
        route.set_stroke(SPARSE, width=3, opacity=.7)
        point = Dot(route.get_start(), radius=.12, color=GOOD)
        return VGroup(broad, narrow,
                      label("broad", 18, WEIGHT).move_to([-2.15, 2.1, 0]),
                      label("sharp", 18, ACCENT).move_to([2.15, 2.1, 0]),
                      card("λₘₐₓ  ↑", ACCENT, 2.5, .7, 24, .13).move_to([0, -2.3, 0]),
                      route, point)

    def gauge(self, title, value, color, status, center):
        track = RoundedRectangle(width=5.5, height=.42, corner_radius=.1,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.48)
        width = max(.2, 5.15 * value)
        fill = RoundedRectangle(width=width, height=.25, corner_radius=.07,
                                stroke_width=0, fill_color=color, fill_opacity=.95)
        fill.move_to([track.get_left()[0] + .17 + width / 2, 0, 0])
        group = VGroup(label(title, 20, color).move_to([-1.72, .55, 0]),
                       card(status, color, 1.45, .52, 16, .1).move_to([2.05, .55, 0]),
                       track, fill)
        group.move_to(center)
        return group

    def product_gauge(self, value):
        track = RoundedRectangle(width=5.7, height=.48, corner_radius=.1,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.48)
        width = max(.2, 5.25 * value)
        fill = RoundedRectangle(width=width, height=.28, corner_radius=.07,
                                stroke_width=0, fill_color=GOOD, fill_opacity=.95)
        fill.move_to([track.get_left()[0] + .22 + width / 2, 0, 0])
        boundary = Line([2.45, -.34, 0], [2.45, .34, 0], color=ACCENT, stroke_width=5)
        return VGroup(label("η λₘₐₓ", 22, GOOD).move_to([-2.15, .62, 0]),
                      label("2", 21, ACCENT).move_to([2.45, .62, 0]), track, fill, boundary)

    def loss_plot(self, oscillatory):
        origin = np.array([-3.05, -1.45, 0])
        axes = VGroup(Line(origin, origin + RIGHT * 6.1, color=MUTED, stroke_width=1.7),
                      Line(origin, origin + UP * 3.65, color=MUTED, stroke_width=1.7))
        ts = np.linspace(0, 1, 180)
        if oscillatory:
            ys = 2.75 * np.exp(-2.0 * ts) + .36 * np.sin(42 * ts) * (1 - .25 * ts)
        else:
            ys = 2.85 * np.exp(-2.4 * ts)
        points = [np.array([origin[0] + 5.95 * t, origin[1] + .25 + y, 0]) for t, y in zip(ts, ys)]
        curve = VMobject(stroke_color=GOOD, stroke_width=4, stroke_opacity=.95)
        curve.set_points_smoothly(points)
        trend = DashedLine(points[0], points[-1], color=ACCENT, dash_length=.14,
                           stroke_width=2) if oscillatory else VGroup()
        return VGroup(axes, curve, trend,
                      label("Loss", 19, GOOD).move_to([-3.25, 2.35, 0]),
                      label("step", 18, MUTED).move_to([2.55, -1.82, 0]))

    def region_strip(self):
        stable = card("STABLE", GOOD, 2.25, 1.1, 23, .13)
        edge = card("EDGE", ACCENT, 2.25, 1.1, 27, .18)
        divergence = card("DIVERGENCE", PRUNE, 2.65, 1.1, 21, .13)
        strip = VGroup(stable, edge, divergence).arrange(RIGHT, buff=.12)
        pointer = Triangle(color=ACCENT, fill_color=ACCENT, fill_opacity=1).scale(.16).rotate(PI)
        pointer.next_to(edge, UP, buff=.25)
        return VGroup(stable, edge, divergence, pointer,
                      label("η λₘₐₓ  increases  →", 21, MUTED).next_to(strip, DOWN, buff=.65),
                      card("EDGE  ≠  UNLIMITED INSTABILITY", ACCENT, 6.4, .78, 22, .13)
                      .move_to([0, -2.45, 0]))

    def geometry_chain(self):
        first = card("PARAMETERS MOVE", WEIGHT, 5.0, .86, 24, .12)
        second = card("LOCAL CURVATURE CHANGES", SPARSE, 5.6, .86, 23, .12)
        third = card("STABILITY CHANGES", ACCENT, 5.0, .86, 24, .14)
        arrow1 = label("↓", 31, MUTED)
        arrow2 = label("↓", 31, MUTED)
        return VGroup(first, arrow1, second, arrow2, third).arrange(DOWN, buff=.28).move_to([0, .15, 0])

    def answer_panel(self, symbol, answer, color):
        box = RoundedRectangle(width=3.5, height=4.1, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035, stroke_width=2.2)
        return VGroup(box, label(symbol, 38, color).move_to([0, .9, 0]),
                      label("↓", 30, MUTED).move_to([0, .05, 0]),
                      label(answer, 23, INK, 3.0, BOLD).move_to([0, -.9, 0]))

    def summary_panel(self):
        sharpness = self.sharpness_graph(.98, True).scale(.48).move_to([0, 1.25, 0])
        loss = self.loss_plot(True).scale(.48).move_to([0, -1.35, 0])
        return VGroup(sharpness, loss,
                      card("higher curvature", SPARSE, 2.7, .58, 17, .1).move_to([-2.05, .1, 0]),
                      card("oscillatory Loss", GOOD, 2.7, .58, 17, .1).move_to([2.05, .1, 0]))

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 28).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(width=7.65, height=1.15, corner_radius=.14,
                                            stroke_color=ZERO, stroke_width=1.2,
                                            fill_color=ZERO, fill_opacity=.32)
        self.caption_box.move_to([0, -5.65, 0])
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
