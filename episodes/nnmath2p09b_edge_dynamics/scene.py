"""Short 09B: fixed learning rate, changing curvature, and Edge of Stability."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.nnmath2p09_edge_of_stability.scene import (
    NeuralMathPart2EdgeOfStability, card, label,
)
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO


class NeuralMathPart2EdgeDynamics(NeuralMathPart2EdgeOfStability):
    DURATION = 122

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        title = VGroup(
            label("Edge of Stability", 23, ACCENT),
            label("고정된 Learning Rate,\n발산해야 할 것 같은데 왜 학습은 계속될까?", 21, INK, 7.5),
        ).arrange(DOWN, buff=.12).move_to(UP * 6.55)
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 09B", 16, MUTED).move_to(UP * 7.55),
            title,
            Line([-3.8, 5.75, 0], [3.8, 5.75, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0], color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        self.copy("Quadratic의 안정성은 ηλ가 함께 결정합니다", "RECAP · 0 < ηλ < 2",
                  "Learning Rate η가 고정되어 있어도 curvature λ가 달라지면\n같은 한 걸음의 안정성은 달라질 수 있습니다.")
        formula = card("0  <  ηλ  <  2", GOOD, 5.0, 1.0, 37, .15).move_to([0, 1.0, 0])
        pair = VGroup(card("η fixed", WEIGHT, 2.5, .68, 22, .1), label("×", 27, MUTED),
                      card("λ changes", SPARSE, 2.9, .68, 22, .12)).arrange(RIGHT, buff=.2).move_to([0, -1.0, 0])
        self.show(VGroup(formula, pair))
        self.to(11)

        self.copy("신경망은 학습하면서 다른 지형으로 이동합니다", "BROAD REGION → SHARP REGION",
                  "처음에는 완만한 영역에 있어도 더 좁고 높은 curvature로 이동할 수 있습니다.\nη는 그대로지만 Hessian의 최대 eigenvalue λₘₐₓ가 커집니다.")
        landscape = self.landscape()
        self.show(landscape)
        self.play(MoveAlongPath(landscape[-1], landscape[-2]), run_time=1.25, rate_func=smooth)
        self.to(24)

        self.copy("η = 0.01을 끝까지 고정해봅시다", "THE KEY NUMERICAL EXAMPLE",
                  "λₘₐₓ가 20, 100, 190으로 증가하면\nηλₘₐₓ는 0.2, 1.0, 1.9로 경계 2에 접근합니다.")
        numeric = self.numeric_example()
        self.show(numeric)
        self.play(LaggedStart(*[Indicate(row, color=[GOOD, SPARSE, ACCENT][i])
                                for i, row in enumerate(numeric[2:5])], lag_ratio=.25), run_time=1.4)
        self.to(34)

        self.copy("Learning Rate를 키워서 경계에 간 것이 아닙니다", "FIXED η · CHANGING LANDSCAPE",
                  "한 번도 바뀌지 않은 η에 새 위치의 λₘₐₓ가 곱해집니다.\n모델이 경험하는 curvature가 변하며 안정성이 달라진 것입니다.")
        eta = self.gauge("LEARNING RATE  η = 0.01", .42, ACCENT, "FIXED", [0, 1.7, 0])
        lam = self.gauge("SHARPNESS  λₘₐₓ", .91, SPARSE, "RISING", [0, .05, 0])
        product = self.product_gauge(.92).move_to([0, -2.0, 0])
        self.show(VGroup(eta, lam, product))
        self.to(44)

        self.copy("λₘₐₓ가 classical boundary로 상승할 수 있습니다", "TRACK THE LARGEST HESSIAN EIGENVALUE",
                  "실제 신경망에서 λₘₐₓ를 추적하면 값이 증가해\nsimple Gradient Descent의 2/η 부근에 도달할 수 있습니다.")
        early = self.sharpness_graph(.38, False)
        near = self.sharpness_graph(.97, False)
        self.show(early)
        self.play(ReplacementTransform(early, near), run_time=1.2)
        self.stage = near
        self.to(53)

        self.copy("고정 Quadratic의 직관이라면 곧 무너질 것 같습니다", "THE SURPRISE",
                  "하지만 신경망 학습은 바로 끝나지 않을 수 있습니다.\ncurvature가 경계 부근에서 움직이면서도 학습이 계속됩니다.")
        graph = self.sharpness_graph(.99, True)
        question = card("DIVERGE NOW?", PRUNE, 3.5, .72, 23, .11).move_to([0, -2.35, 0])
        self.show(VGroup(graph, question))
        answer = card("TRAINING CONTINUES", GOOD, 4.4, .72, 23, .13).move_to(question)
        self.play(ReplacementTransform(question, answer), run_time=.8)
        self.stage = VGroup(graph, answer)
        self.to(64)

        self.copy("Loss도 매 step 부드럽게 감소하지 않습니다", "OSCILLATION WITH LONG-TERM PROGRESS",
                  "일부 step에서는 Loss가 증가하고 진동할 수 있습니다.\n하지만 더 긴 시간에서 보면 학습은 계속 진행될 수 있습니다.")
        self.show(self.loss_plot(True).move_to([0, .45, 0]))
        self.to(73)

        self.copy("이 dynamics가 Edge of Stability입니다", "NEAR THE CLASSICAL BOUNDARY",
                  "classical boundary 부근에서 curvature와 Loss가 진동해도\n학습이 이어질 수 있는 현상을 Edge of Stability라고 합니다.")
        summary = self.summary_panel()
        name = card("EDGE OF STABILITY", ACCENT, 5.7, .85, 29, .16).move_to([0, -2.55, 0])
        self.show(VGroup(summary, name))
        self.to(81)

        self.copy("모델이 처음부터 경계에 있었던 것은 아닙니다", "PARAMETERS MOVE → CURVATURE CHANGES",
                  "parameter 이동이 local geometry를 바꿨습니다.\n그래서 같은 Learning Rate도 모든 위치에서 같은 안정성을 뜻하지 않습니다.")
        chain = self.geometry_chain()
        self.show(chain)
        self.play(LaggedStart(*[Indicate(item, color=[WEIGHT, SPARSE, ACCENT][i])
                                for i, item in enumerate(chain[::2])], lag_ratio=.2), run_time=1.1)
        self.to(91)

        self.copy("불안정할수록 좋다는 뜻은 아닙니다", "EDGE  ≠  UNLIMITED INSTABILITY",
                  "η가 지나치게 크거나 안정 범위를 크게 벗어나면 실제로 발산합니다.\n핵심은 고전적인 경계 부근에서도 학습이 이어질 수 있다는 점입니다.")
        strip = self.region_strip()
        self.show(strip)
        self.play(Indicate(strip[1], color=ACCENT), run_time=.8)
        self.to(102)

        self.copy("가장 큰 eigenvalue는 가장 날카로운 방향입니다", "λᵢ: LEARNING SPEED · λₘₐₓ: STABILITY",
                  "같은 η에서 가장 높은 curvature 방향은\n안정성 문제가 가장 먼저 나타날 수 있는 방향이기도 합니다.")
        spectrum = self.spectrum(big=True).move_to([0, .65, 0])
        formula = card("η λₘₐₓ  ≈  2", ACCENT, 4.4, .86, 31, .15).move_to([0, -2.05, 0])
        self.show(VGroup(spectrum, formula))
        self.play(Indicate(spectrum[-1], color=ACCENT), run_time=.8)
        self.to(110)

        self.copy("좋은 학습이 항상 매끄러운 하강일 필요는 없습니다", "THE EDGE OF STABILITY",
                  "η가 그대로여도 curvature는 변할 수 있습니다.\n안정성과 불안정성의 경계에서 학습이 이어질 수 있습니다.")
        final = VGroup(card("η fixed", WEIGHT, 3.0, .72, 24, .1), label("+", 29, MUTED),
                       card("λₘₐₓ ↑", SPARSE, 3.0, .72, 25, .12), label("→", 29, MUTED),
                       card("η λₘₐₓ ≈ 2", ACCENT, 4.2, .88, 31, .16), label("↓", 30, MUTED),
                       card("EDGE OF STABILITY", GOOD, 6.0, .92, 29, .15))
        final.arrange(DOWN, buff=.2).move_to([0, .2, 0])
        self.show(final)
        self.to(122)
