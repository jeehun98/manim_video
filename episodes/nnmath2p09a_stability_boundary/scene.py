"""Short 09A: why eta-lambda equals two at the stability boundary."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.nnmath2p09_edge_of_stability.scene import (
    NeuralMathPart2EdgeOfStability, card, label,
)
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO


class NeuralMathPart2StabilityBoundary(NeuralMathPart2EdgeOfStability):
    DURATION = 104

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 09A", 17, MUTED).move_to(UP * 7.3),
            label("왜 ηλ = 2가 안정성의 경계일까?", 27).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0], color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        self.copy("Gradient Descent는 기울기를 따라 이동합니다", "FOLLOW THE LOCAL SLOPE",
                  "Learning Rate가 작으면 천천히, 적당하면 더 빠르게 움직입니다.\n하지만 너무 크면 최소점을 반복해서 넘어갑니다.")
        panels = VGroup(self.lr_panel("SMALL η", GOOD, .32),
                        self.lr_panel("GOOD η", SPARSE, .58),
                        self.lr_panel("TOO LARGE", PRUNE, 1.12))
        panels.arrange(RIGHT, buff=.18).scale(.93).move_to([0, .15, 0])
        self.show(panels)
        self.play(LaggedStart(*[Create(p[2]) for p in panels], lag_ratio=.2), run_time=1.2)
        self.to(12.5)

        self.copy("그런데 안정성은 η만으로 결정되지 않습니다", "SAME η · DIFFERENT CURVATURE",
                  "같은 Learning Rate라도 넓은 골짜기에서는 안전하고,\n좁고 가파른 골짜기에서는 최소점을 크게 넘어갈 수 있습니다.")
        valleys = self.curvature_compare()
        self.show(valleys)
        self.play(LaggedStart(Create(valleys[0][2]), Create(valleys[1][2]), lag_ratio=.25), run_time=1.1)
        self.to(25)

        self.copy("Loss가 얼마나 심하게 휘었는지도 중요합니다", "CURVATURE = λ",
                  "완만한 곡선은 기울기가 천천히 바뀌고,\n가파른 곡선은 같은 거리에서도 기울기가 빠르게 바뀝니다.")
        broad = self.curvature_card("LOW CURVATURE", WEIGHT, .38).move_to([-1.9, .25, 0])
        sharp = self.curvature_card("HIGH CURVATURE", ACCENT, 1.15).move_to([1.9, .25, 0])
        self.show(VGroup(broad, sharp, card("curvature  =  λ", SPARSE, 4.0, .72, 26, .13)
                         .move_to([0, -2.35, 0])))
        self.to(35)

        self.copy("Quadratic Loss에서 직접 계산해봅시다", "WHY DOES THE BOUNDARY EQUAL 2?",
                  "L(θ)=½λθ²이면 gradient는 λθ입니다.\n다음 위치는 현재 θ에서 ηλθ를 뺀 값입니다.")
        derivation = VGroup(card("L(θ) = ½ λθ²", WEIGHT, 5.1, .78, 29, .1),
                            label("↓  gradient", 21, MUTED),
                            card("∇L(θ) = λθ", SPARSE, 5.1, .78, 29, .11),
                            label("↓  update", 21, MUTED),
                            card("θₜ₊₁ = θₜ − ηλθₜ", ACCENT, 5.7, .84, 29, .14))
        derivation.arrange(DOWN, buff=.22).move_to([0, .15, 0])
        self.show(derivation)
        self.to(48.5)

        self.copy("다음 위치는 하나의 multiplier로 정리됩니다", "THE UPDATE MULTIPLIER",
                  "θₜ₊₁=(1−ηλ)θₜ.\n1−ηλ의 크기와 부호가 다음 위치와 진동 폭을 결정합니다.")
        multiplier = card("θₜ₊₁ = (1 − ηλ) θₜ", ACCENT, 6.4, 1.05, 38, .16).move_to([0, .85, 0])
        guide = VGroup(card("|1−ηλ| < 1", GOOD, 2.9, .72, 23, .12), label("→", 26, MUTED),
                       card("amplitude shrinks", GOOD, 3.1, .72, 20, .1))
        guide.arrange(RIGHT, buff=.18).move_to([0, -1.25, 0])
        self.show(VGroup(multiplier, guide))
        self.to(58)

        self.copy("ηλ = 0.5이면 같은 쪽에서 수렴합니다", "0.5 → NO SIGN FLIP",
                  "multiplier는 0.5입니다.\n위치는 1, 0.5, 0.25처럼 매번 절반으로 줄어듭니다.")
        self.show(self.recurrence_panel("ηλ = 0.5", [1, .5, .25, .125], GOOD))
        self.to(66)

        self.copy("ηλ = 1.5이면 좌우로 넘으며 수렴합니다", "1.5 → SIGN FLIPS · STILL CONVERGES",
                  "multiplier는 −0.5입니다. 부호는 계속 바뀌지만\n진동 폭은 절반씩 줄어들기 때문에 여전히 수렴합니다.")
        self.show(self.recurrence_panel("ηλ = 1.5", [1, -.5, .25, -.125], SPARSE))
        self.to(76)

        self.copy("ηλ = 2에서는 더 이상 가까워지지 않습니다", "2 → SIGN FLIPS · NO SHRINKING",
                  "multiplier는 −1입니다. 1에서 시작하면 −1, 다시 1, 다시 −1.\n최소점을 넘지만 진동 폭은 그대로입니다.")
        boundary = self.recurrence_panel("ηλ = 2", [1, -1, 1, -1], ACCENT)
        self.show(boundary)
        self.play(Indicate(boundary[0], color=ACCENT), run_time=.8)
        self.to(87)

        self.copy("그래서 simple Gradient Descent의 경계는 2입니다", "CLASSICAL STABILITY CONDITION",
                  "진동 폭이 줄려면 |1−ηλ|<1이어야 합니다.\n따라서 고정된 quadratic의 안정 영역은 0<ηλ<2입니다.")
        formula = card("0  <  ηλ  <  2", GOOD, 5.0, 1.0, 37, .15).move_to([0, 1.15, 0])
        self.show(VGroup(formula, self.stability_line().move_to([0, -.75, 0]),
                         card("fixed 1D quadratic", MUTED, 4.1, .64, 18, .06).move_to([0, -2.4, 0])))
        self.to(97)

        self.copy("그렇다면 안전한 η를 고르면 계속 안전할까요?", "NEXT · THE LANDSCAPE CAN CHANGE",
                  "신경망에서는 parameter가 움직이며 curvature도 달라집니다.\n다음 영상에서는 고정된 η로도 경계에 접근하는 이유를 봅니다.")
        final = VGroup(card("η fixed", WEIGHT, 2.7, .72, 23, .1), label("+", 28, MUTED),
                       card("λ changes", SPARSE, 3.1, .72, 23, .12), label("→", 28, MUTED),
                       card("stability changes", ACCENT, 4.5, .86, 26, .15))
        final.arrange(DOWN, buff=.25).move_to([0, .15, 0])
        self.show(final)
        self.to(104)
