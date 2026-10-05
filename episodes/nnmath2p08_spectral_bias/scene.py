"""Neural Network Mathematics Part 2, episode 08: Spectral Bias."""
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


class NeuralMathPart2SpectralBias(Scene):
    DURATION = 154

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 08", 17, MUTED).move_to(UP * 7.3),
            label("Spectral Bias · 신경망은 왜 낮은 주파수부터 학습할까?", 25).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        # 1 — Begin with one complicated answer, not two pre-labelled frequencies.
        self.copy(
            "신경망은 정답을 한 번에 만들어갈까요?", "ONE COMPLICATED TARGET",
            "학습이 진행되면 출력은 점점 정답에 가까워집니다.\n우리는 보통 정답 전체가 함께 다듬어진다고 생각합니다.",
        )
        target_box = RoundedRectangle(width=7.0, height=3.65, corner_radius=.22,
                                      color=ACCENT, fill_color=ACCENT,
                                      fill_opacity=.025, stroke_width=2)
        target_box.move_to([0, .65, 0])
        target = self.wave_curve(1, .3, ACCENT, [0, .65, 0], width=6.5)
        net = self.network_icon(7, WEIGHT).scale(.58).move_to([0, -2.25, 0])
        self.show(VGroup(target_box, target,
                         label("TARGET", 20, ACCENT).move_to([-3.0, 2.1, 0]), net,
                         label("random output  →  closer output  →  answer", 20, MUTED)
                         .move_to([0, -3.25, 0])))
        self.to(6.4)

        # 2 — Make the ordinary mental model explicit: the whole curve improves together.
        self.copy(
            "보통은 전체 모양이 조금씩 가까워진다고 생각합니다", "THE USUAL MENTAL MODEL",
            "랜덤한 출력이 조금 더 비슷해지고, 다시 더 비슷해져\n마침내 하나의 정답 곡선이 된다는 그림입니다.",
        )
        stages = VGroup()
        for i, (lo, hi, name, color) in enumerate([
            (0, 0, "STEP 0", MUTED), (.35, .05, "STEP 100", WEIGHT),
            (.72, .14, "STEP 500", SPARSE), (1, .3, "STEP 2000", ACCENT),
        ]):
            box = RoundedRectangle(width=6.7, height=1.05, corner_radius=.15,
                                   color=color, fill_color=color, fill_opacity=.025,
                                   stroke_width=1.5)
            curve = self.wave_curve(lo, hi, color, [.65, 0, 0], width=4.8)
            stages.add(VGroup(box, label(name, 18, color).move_to([-2.45, 0, 0]), curve))
        stages.arrange(DOWN, buff=.22).scale(.9).move_to([0, .0, 0])
        self.show(stages)
        self.play(LaggedStart(*[Indicate(row, color=row[1].get_color()) for row in stages],
                              lag_ratio=.18), run_time=1.2)
        self.to(10.1)

        # 3 — Animate that familiar view before revealing what it hides.
        self.copy(
            "겉으로 보면 하나의 곡선이 완성되는 과정입니다", "ONE OUTPUT · ONE LOSS",
            "하지만 이 모습만으로는 정답을 구성하는\n모든 구조가 같은 속도로 학습됐는지 알 수 없습니다.",
        )
        target = self.wave_curve(1, .3, ACCENT, [0, 1.2, 0], width=6.6)
        pred = self.wave_curve(0, 0, GOOD, [0, -1.25, 0], width=6.6)
        step = card("training step  0", ACCENT, 2.8, .6, 18, .11).move_to([0, -2.7, 0])
        self.show(VGroup(target, pred, step,
                         label("TARGET", 18, ACCENT).move_to([-3.0, 2.15, 0]),
                         label("PREDICTION", 18, GOOD).move_to([-2.75, -.25, 0])))
        broad = self.wave_curve(.88, 0, GOOD, [0, -1.25, 0], width=6.6)
        full = self.wave_curve(1, .29, GOOD, [0, -1.25, 0], width=6.6)
        step_mid = card("training step  500", ACCENT, 2.8, .6, 18, .11).move_to(step)
        step_end = card("training step  2000", ACCENT, 2.8, .6, 18, .11).move_to(step)
        self.play(ReplacementTransform(pred, broad), ReplacementTransform(step, step_mid), run_time=.75)
        self.play(ReplacementTransform(broad, full), ReplacementTransform(step_mid, step_end), run_time=.75)
        self.stage.add(full, step_end)
        self.to(15.4)

        # 4 — Physically pull the one target apart.
        self.copy(
            "하나의 정답을 뜯어보면 다른 모습이 보입니다", "DECOMPOSE THE SAME TARGET",
            "큰 물결, 조금 빠른 물결, 아주 빠른 물결.\n하나로 보이던 정답 안에 서로 다른 성분이 있습니다.",
        )
        composite = self.wave_curve(1, .3, ACCENT, [0, 1.65, 0], width=6.6)
        whole = card("ONE TARGET", ACCENT, 2.5, .66, 19, .12).move_to([0, 2.65, 0])
        self.show(VGroup(composite, whole))
        low = self.component_row("LOW", 1, 0, WEIGHT).scale(.82).move_to([0, .45, 0])
        high = self.component_row("HIGH", 0, .3, PRUNE, high_freq=5.5).scale(.82).move_to([0, -1.45, 0])
        plus = label("+", 34, MUTED).move_to([0, -.5, 0])
        self.play(FadeOut(whole),
                  ReplacementTransform(composite.copy(), low),
                  ReplacementTransform(composite, high), FadeIn(plus), run_time=1.25)
        self.stage = VGroup(low, high, plus)
        self.to(22.2)

        # 5 — Establish the Fourier viewpoint using the same target.
        self.copy(
            "하나의 함수를 여러 주파수의 합으로 봅니다", "FOURIER VIEW",
            "서로 다른 진동을 더해 하나의 복잡한 함수를 바라보는\nFourier 관점입니다.",
        )
        modes = VGroup(
            self.component_row("LOW", 1, 0, WEIGHT),
            self.component_row("MID", 0, .18, SPARSE, high_freq=2.8),
            self.component_row("HIGH", 0, .3, PRUNE, high_freq=5.5),
        ).arrange(DOWN, buff=.28).scale(.86).move_to([0, .15, 0])
        self.show(modes)
        self.play(LaggedStart(*[Indicate(mode, color=mode[1].get_color()) for mode in modes],
                              lag_ratio=.2), run_time=1.15)
        self.to(26.8)

        # 6 — Reveal unequal progress at one and the same training step.
        self.copy(
            "각 성분은 같은 속도로 학습되지 않을 수 있습니다", "SAME STEP · DIFFERENT PROGRESS",
            "정답 전체가 균일하게 만들어지는 대신\n어떤 성분은 빠르게, 다른 성분은 느리게 학습될 수 있습니다.",
        )
        bars = VGroup(self.error_bar("LOW", .9, WEIGHT),
                      self.error_bar("MID", .9, SPARSE),
                      self.error_bar("HIGH", .9, PRUNE)).arrange(DOWN, buff=.46).move_to([0, .25, 0])
        step = card("training step  500", ACCENT, 3.0, .62, 19, .11).move_to([0, -2.55, 0])
        self.show(VGroup(bars, step,
                         label("remaining error", 18, MUTED).move_to([0, 2.25, 0])))
        self.play(self.set_bar(bars[0], .12), self.set_bar(bars[1], .45),
                  self.set_bar(bars[2], .78), run_time=1.2)
        self.to(35.5)

        # 7 — Name the phenomenon only after the viewer has discovered it.
        self.copy(
            "신경망은 모든 구조를 동등하게 배우지 않습니다", "SPECTRAL BIAS",
            "낮은 주파수 성분을 높은 주파수 성분보다 먼저,\n또는 더 쉽게 배우는 경향을 Spectral Bias라 부릅니다.",
        )
        low = self.mode_token("LOW", WEIGHT, 1.0).scale(1.05).move_to([-2.15, .65, 0])
        high = self.mode_token("HIGH", PRUNE, 5.5).scale(1.05).move_to([2.15, .65, 0])
        self.show(VGroup(low, high,
                         card("NOT EQUALLY LEARNED", ACCENT, 5.3, .9, 27, .15)
                         .move_to([0, -1.5, 0])))
        self.to(42.7)

        # 8 — The loss does not contain an instruction about frequency order.
        self.copy(
            "하지만 Loss에는 학습 순서가 적혀 있지 않습니다", "NO ‘LOW FIRST’ IN THE OBJECTIVE",
            "모델이 받은 것은 입력과 정답, 그리고 오차를 줄이라는 조건뿐입니다.\n낮은 주파수를 먼저 배우라는 지시는 없습니다.",
        )
        data = VGroup(*[Dot([x, .55 * np.sin(x) + .14 * np.sin(5.5 * x), 0],
                            radius=.065, color=WEIGHT) for x in np.linspace(-3, 3, 17)])
        loss = card("Loss = prediction − target", ACCENT, 5.4, .9, 25, .14).move_to([0, -1.35, 0])
        forbidden = card("learn LOW first", PRUNE, 3.3, .72, 20, .09).move_to([0, -2.55, 0])
        cross = Line([-1.55, -2.82, 0], [1.55, -2.28, 0], color=PRUNE, stroke_width=5)
        self.show(VGroup(data, loss, forbidden, cross,
                         label("(x₁,y₁), (x₂,y₂), …", 22, MUTED).move_to([0, 1.7, 0])))
        self.to(50.5)

        # 9 — State the deeper surprise: optimization is not neutral in function space.
        self.copy(
            "학습은 함수 공간의 모든 방향을 같게 보지 않습니다", "LEARNING IS NOT NEUTRAL",
            "같은 함수 공간 안에서도 학습 dynamics는\n모든 방향을 똑같이 취급하지 않을 수 있습니다.",
        )
        center = Dot([0, -.2, 0], radius=.1, color=ACCENT)
        directions = VGroup(
            Arrow(center.get_center(), [-2.7, 1.7, 0], buff=.12, color=WEIGHT,
                  stroke_width=8, tip_length=.22),
            Arrow(center.get_center(), [0, 1.35, 0], buff=.12, color=SPARSE,
                  stroke_width=5, tip_length=.2),
            Arrow(center.get_center(), [2.1, .7, 0], buff=.12, color=PRUNE,
                  stroke_width=2.5, tip_length=.18),
        )
        self.show(VGroup(center, directions,
                         label("LOW", 19, WEIGHT).move_to([-2.8, 2.15, 0]),
                         label("MID", 19, SPARSE).move_to([0, 1.8, 0]),
                         label("HIGH", 19, PRUNE).move_to([2.25, 1.05, 0]),
                         card("different response strengths", ACCENT, 5.3, .78, 22, .13)
                         .move_to([0, -2.15, 0])))
        self.to(56.0)

        # 10 — Prevent the everyday explanation from becoming the endpoint.
        self.copy(
            "단순히 큰 모양이라서 쉬운 걸까요?", "OBSERVATION  ≠  EXPLANATION",
            "큰 구조가 먼저 보인다는 말만으로는\n왜 각 성분의 학습 속도가 달라지는지 설명하지 못합니다.",
        )
        observation = card("큰 모양이 먼저 나타남", WEIGHT, 5.1, .9, 25, .12).move_to([0, 1.1, 0])
        explanation = card("왜 속도가 다른가?", ACCENT, 5.1, .9, 27, .15).move_to([0, -1.1, 0])
        self.show(VGroup(observation, label("≠", 48, PRUNE).move_to([0, 0, 0]), explanation))
        self.to(61.4)

        # 11 — Set up the second reveal: the spectrum of the learning dynamics.
        self.copy(
            "그렇다면 왜 학습 속도가 다를까요?", "WHY DIFFERENT RATES?",
            "정답을 여러 주파수 방향으로 나눈 것처럼\n학습 dynamics 자체도 여러 방향으로 나누어 보겠습니다.",
        )
        question = label("정답의 spectrum을 넘어\n학습의 spectrum으로", 38, ACCENT, 6.5, BOLD)
        self.show(VGroup(question,
                         card("look at the learning operator", SPARSE, 5.3, .82, 23, .14)
                         .move_to([0, -2.0, 0])))
        self.to(70.0)

        # 12 — Decompose the learning operator into eigen-directions.
        self.copy(
            "학습 오차를 서로 다른 속도의 mode로 나눕니다", "LEARNING OPERATOR → EIGEN-DIRECTIONS",
            "특정한 kernel 관점에서는 학습 오차를 여러 고유방향,\n즉 서로 다른 속도로 줄어드는 mode로 분해할 수 있습니다.",
        )
        left_box = RoundedRectangle(width=3.55, height=4.65, corner_radius=.22,
                                    color=WEIGHT, fill_color=WEIGHT, fill_opacity=.025, stroke_width=2)
        left_box.move_to([-2.0, .15, 0])
        right_box = RoundedRectangle(width=3.55, height=4.65, corner_radius=.22,
                                     color=SPARSE, fill_color=SPARSE, fill_opacity=.025, stroke_width=2)
        right_box.move_to([2.0, .15, 0])
        fourier = VGroup(self.mode_token("Low", WEIGHT, 1.0),
                         self.mode_token("Mid", SPARSE, 2.7),
                         self.mode_token("High", PRUNE, 5.4))
        fourier.arrange(DOWN, buff=.25).scale(.72).move_to([-2.0, -.35, 0])
        eigenmodes = VGroup(card("q₁", WEIGHT, 1.45, .62, 21, .11),
                            card("q₂", SPARSE, 1.45, .62, 21, .11),
                            card("q₃", PRUNE, 1.45, .62, 21, .11))
        eigenmodes.arrange(DOWN, buff=.35).move_to([2.0, -.35, 0])
        self.show(VGroup(left_box, right_box,
                         label("정답을 분해", 22, WEIGHT).move_to([-2.0, 2.0, 0]),
                         label("Function → Fourier", 18, MUTED).move_to([-2.0, 1.45, 0]),
                         fourier,
                         label("학습을 분해", 22, SPARSE).move_to([2.0, 2.0, 0]),
                         label("Dynamics → Eigenmodes", 18, MUTED).move_to([2.0, 1.45, 0]),
                         eigenmodes,
                         label("두 번의 분해", 21, ACCENT).move_to([0, -2.75, 0])))
        self.play(Indicate(fourier, color=WEIGHT), Indicate(eigenmodes, color=SPARSE), run_time=.9)
        self.to(77.2)

        # 13 — Eigenvalues set the component-wise learning strength.
        self.copy(
            "각 방향에는 서로 다른 Eigenvalue가 대응합니다", "LARGE λ → FAST  ·  SMALL λ → SLOW",
            "큰 고유값 방향의 오차는 빠르게 줄고\n작은 고유값 방향의 오차는 천천히 줄어듭니다.",
        )
        time_label = card("t = 0", ACCENT, 1.6, .58, 19, .11).move_to([0, 2.15, 0])
        rows = VGroup(
            self.eigen_row("q₁", "λ₁ = 5", "FAST", WEIGHT, .95),
            self.eigen_row("q₂", "λ₂ = 1", "MEDIUM", SPARSE, .95),
            self.eigen_row("q₃", "λ₃ = 0.2", "SLOW", PRUNE, .95),
        ).arrange(DOWN, buff=.42).move_to([0, .0, 0])
        self.show(VGroup(time_label, rows))
        time_after = card("t = 1", ACCENT, 1.6, .58, 19, .11).move_to(time_label)
        self.play(ReplacementTransform(time_label, time_after),
                  self.set_eigen_strength(rows[0], .03),
                  self.set_eigen_strength(rows[1], .35),
                  self.set_eigen_strength(rows[2], .78), run_time=1.15)
        self.to(84.3)

        # 14 — The central equation now explains the rate difference.
        self.copy(
            "고유값이 성분별 오차 감소 속도를 정합니다", "ERROR DECAY ALONG EIGEN-DIRECTION i",
            "lambda i가 클수록 해당 방향의 오차 계수 c i가\n시간에 따라 더 빠르게 사라집니다.",
        )
        formula = card("cᵢ(t) ≈ cᵢ(0)e^(−λᵢt)", ACCENT, 6.4, 1.15, 34, .15).move_to([0, 1.65, 0])
        fast = self.decay_plot(1.15, WEIGHT, "large λ", [-1.9, -.55, 0])
        slow = self.decay_plot(.22, PRUNE, "small λ", [1.9, -.55, 0])
        self.show(VGroup(formula, fast, slow))
        self.play(Create(fast[2]), Create(slow[2]), run_time=1.1)
        self.to(89.9)

        # 15 — Link frequencies to eigenvalues carefully, not universally.
        self.copy(
            "왜 낮은 주파수가 먼저 나타날 수 있을까요?", "SETTING-DEPENDENT SPECTRAL STRUCTURE",
            "많은 설정에서 낮은 주파수 성분이 더 큰 고유값의 mode와 연결되어\n먼저 학습될 수 있지만, 보편적인 등식은 아닙니다.",
        )
        left_box = RoundedRectangle(width=3.35, height=4.75, corner_radius=.22,
                                    color=WEIGHT, fill_color=WEIGHT, fill_opacity=.025, stroke_width=2)
        left_box.move_to([-2.15, .2, 0])
        right_box = RoundedRectangle(width=3.35, height=4.75, corner_radius=.22,
                                     color=GOOD, fill_color=GOOD, fill_opacity=.025, stroke_width=2)
        right_box.move_to([2.15, .2, 0])
        modes = VGroup(self.mode_token("Low", WEIGHT, 1.0),
                       self.mode_token("Mid", SPARSE, 2.7),
                       self.mode_token("High", PRUNE, 5.4))
        modes.arrange(DOWN, buff=.35).scale(.7).move_to([-2.15, .05, 0])
        lambdas = VGroup(card("λ₁  large", WEIGHT, 2.05, .62, 19, .12),
                         card("λ₂  medium", SPARSE, 2.05, .62, 18, .12),
                         card("λ₃  small", PRUNE, 2.05, .62, 19, .12))
        lambdas.arrange(DOWN, buff=.48).move_to([2.15, .05, 0])
        links = VGroup(*[
            Arrow(modes[i].get_right(), lambdas[i].get_left(), buff=.13,
                  color=[WEIGHT, SPARSE, PRUNE][i], stroke_width=2.5, tip_length=.13)
            for i in range(3)
        ])
        caveat = card("setting-dependent · not a universal equality", ACCENT, 6.5, .68, 18, .12)
        caveat.move_to([0, -2.65, 0])
        self.show(VGroup(left_box, right_box,
                         label("FOURIER SPECTRUM", 19, WEIGHT).move_to([-2.15, 2.15, 0]),
                         label("LEARNING SPECTRUM", 19, GOOD).move_to([2.15, 2.15, 0]),
                         modes, lambdas, links, caveat))
        self.play(LaggedStart(*[ShowPassingFlash(link.copy().set_stroke(width=5), time_width=.7)
                                for link in links], lag_ratio=.18), run_time=1.1)
        self.to(100.5)

        # 16 — Expressivity stays the same while error-decay rates differ.
        self.copy(
            "늦게 배운다고 표현하지 못하는 것은 아닙니다", "BOTH REPRESENTABLE · DIFFERENT ERROR DECAY",
            "두 성분을 모두 표현할 수 있어도 학습 dynamics가\n각각의 오차를 줄이는 속도는 다를 수 있습니다.",
        )
        space = RoundedRectangle(width=7.15, height=4.75, corner_radius=.28,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.035, stroke_width=2)
        low_wave = self.wave_curve(.65, 0, WEIGHT, [-1.9, .8, 0], width=2.7)
        high_wave = self.wave_curve(0, .65, PRUNE, [1.9, .8, 0], width=2.7, high_freq=6.0)
        low_speed = self.mini_error("learning speed", .9, GOOD).move_to([-1.9, -1.25, 0])
        high_speed = self.mini_error("learning speed", .25, PRUNE).move_to([1.9, -1.25, 0])
        self.show(VGroup(space,
                         label("REPRESENTABLE FUNCTIONS", 21, MUTED).move_to([0, 2.15, 0]),
                         low_wave, high_wave,
                         card("Representable  ✓", GOOD, 2.6, .62, 18, .11).move_to([-1.9, -.25, 0]),
                         card("Representable  ✓", GOOD, 2.6, .62, 18, .11).move_to([1.9, -.25, 0]),
                         low_speed, high_speed,
                         label("FAST", 18, GOOD).move_to([-1.9, -2.0, 0]),
                         label("SLOW", 18, PRUNE).move_to([1.9, -2.0, 0])))
        self.to(112.4)

        # 17 — Central distinction and the broad-trend consequence.
        self.copy(
            "표현 가능성과 학습 가능성은 다릅니다", "EXPRESSIVITY  ≠  LEARNABILITY",
            "표현 가능한 답도 optimizer에게 똑같이 쉬운 것은 아닙니다.\n큰 구조가 먼저 나타나고 세부 굴곡은 나중에 맞춰질 수 있습니다.",
        )
        expressivity = card("EXPRESSIVITY", WEIGHT, 3.2, 1.0, 28, .15).move_to([-2.25, .75, 0])
        learnability = card("LEARNABILITY", GOOD, 3.45, 1.0, 27, .15).move_to([2.25, .75, 0])
        dots = self.noisy_points().scale(.72).move_to([0, -1.45, 0])
        trend = self.wave_curve(.58, 0, ACCENT, [0, -1.45, 0], width=4.7, low_freq=.75)
        self.show(VGroup(expressivity, label("≠", 54, PRUNE).move_to([0, .75, 0]),
                         learnability, dots, trend))
        self.to(121.8)

        # 18 — Frequency is not a synonym for signal quality.
        self.copy(
            "낮은 주파수가 항상 신호인 것은 아닙니다", "LOW ≠ SIGNAL  ·  HIGH ≠ NOISE",
            "날카로운 경계나 작은 문자처럼 중요한 정보가 높은 주파수에 있다면\n학습 dynamics 때문에 늦게 배워질 수도 있습니다.",
        )
        false_rule = card("Low = Signal    High = Noise", PRUNE, 6.2, .86, 23, .12).move_to([0, 2.0, 0])
        cross = VGroup(Line([-2.9, 1.55, 0], [2.9, 2.45, 0], color=PRUNE, stroke_width=5),
                       Line([-2.9, 2.45, 0], [2.9, 1.55, 0], color=PRUNE, stroke_width=5))
        blurred = self.cat_panel(False).move_to([-2.05, -.35, 0])
        sharp = self.cat_panel(True).move_to([2.05, -.35, 0])
        arrow = Arrow(blurred.get_right(), sharp.get_left(), buff=.18, color=ACCENT, tip_length=.16)
        self.show(VGroup(false_rule, cross, blurred, sharp, arrow,
                         label("low-pass only", 18, MUTED).move_to([-2.05, -2.45, 0]),
                         label("high frequency added", 18, GOOD).move_to([2.05, -2.45, 0])))
        self.to(132.2)

        # 19 — Fourier features change the spectral structure seen by the model.
        self.copy(
            "입력 표현을 바꿔 높은 주파수를 돕기도 합니다", "FOURIER FEATURES",
            "좌표 x를 여러 sine과 cosine 성분으로 변환해 제공하면\n고주파 구조를 더 쉽게 사용할 수 있습니다.",
        )
        x = card("x", WEIGHT, 1.0, .82, 28, .15).move_to([-3.35, .4, 0])
        features = VGroup(*[
            card(name, color, 1.6, .62, 17, .11)
            for name, color in zip(["sin ω₁x", "cos ω₁x", "sin ω₂x", "cos ω₂x"],
                                   [WEIGHT, GOOD, SPARSE, ACCENT])
        ]).arrange(DOWN, buff=.18).move_to([-.95, .4, 0])
        net = self.network_icon(7, SPARSE).scale(.62).move_to([1.55, .4, 0])
        out = self.wave_curve(0, .5, PRUNE, [3.2, .4, 0], width=1.0, high_freq=8.0)
        arrows = VGroup(Arrow(x.get_right(), features.get_left(), buff=.12, color=MUTED, tip_length=.13),
                       Arrow(features.get_right(), net.get_left(), buff=.12, color=MUTED, tip_length=.13),
                       Arrow(net.get_right(), [2.72, .4, 0], buff=.05, color=MUTED, tip_length=.13))
        self.show(VGroup(x, features, net, out, arrows,
                         label("change the representation · change what is easy", 20, ACCENT)
                         .move_to([0, -2.25, 0])))
        self.to(141.5)

        # 20 — Final message: the difference appears in the learning spectrum.
        self.copy(
            "표현 가능한 모든 답이 학습에서도 동등하지 않습니다", "THE LEARNING SPECTRUM",
            "신경망은 정답의 모든 구조를 같은 속도로 배우지 않을 수 있습니다.\n그 차이를 learning dynamics의 spectrum으로 볼 수 있습니다.",
        )
        low_column = VGroup(self.mode_token("LOW", WEIGHT, 1.0).scale(.88),
                            label("↓", 28, MUTED), card("λ large", GOOD, 2.0, .62, 20, .12),
                            label("↓", 28, MUTED), card("FAST", GOOD, 2.0, .62, 20, .12))
        low_column.arrange(DOWN, buff=.18).move_to([-2.1, .45, 0])
        high_column = VGroup(self.mode_token("HIGH", PRUNE, 5.4).scale(.88),
                             label("↓", 28, MUTED), card("λ small", PRUNE, 2.0, .62, 20, .12),
                             label("↓", 28, MUTED), card("SLOW", PRUNE, 2.0, .62, 20, .12))
        high_column.arrange(DOWN, buff=.18).move_to([2.1, .45, 0])
        conclusion = card("Representable  ≠  Equally Learnable", ACCENT, 6.7, .86, 24, .15)
        conclusion.move_to([0, -2.45, 0])
        self.show(VGroup(low_column, high_column, conclusion,
                         label("FUNCTION SPECTRUM  ↔  LEARNING SPECTRUM", 20, MUTED)
                         .move_to([0, 2.65, 0])))
        self.to(154)

    def mini_error(self, name, value, color):
        track = RoundedRectangle(width=2.45, height=.34, corner_radius=.08,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.45)
        fill = RoundedRectangle(width=max(.12, 2.2 * value), height=.2, corner_radius=.05,
                                stroke_width=0, fill_color=color, fill_opacity=.9)
        fill.align_to(track, LEFT).shift(RIGHT * .12)
        return VGroup(label(name, 16, color).move_to([-1.0, .45, 0]), track, fill)

    def set_mini_error(self, meter, value):
        old_fill = meter[2]
        track = meter[1]
        width = max(.12, 2.2 * value)
        new_fill = RoundedRectangle(width=width, height=.2, corner_radius=.05,
                                    stroke_width=0, fill_color=old_fill.get_fill_color(),
                                    fill_opacity=.9)
        new_fill.move_to([track.get_left()[0] + .12 + width / 2, track.get_y(), 0])
        return ReplacementTransform(old_fill, new_fill)

    def set_eigen_strength(self, row, strength):
        track = row[3][0]
        old_fill = row[3][1]
        width = max(.12, 1.35 * strength)
        new_fill = RoundedRectangle(width=width, height=.2, corner_radius=.05,
                                    stroke_width=0, fill_color=old_fill.get_fill_color(),
                                    fill_opacity=.9)
        new_fill.move_to([track.get_left()[0] + .1 + width / 2, track.get_y(), 0])
        return ReplacementTransform(old_fill, new_fill)

    def cat_panel(self, sharp):
        color = GOOD if sharp else MUTED
        opacity = 1 if sharp else .28
        box = RoundedRectangle(width=3.35, height=3.55, corner_radius=.18,
                               color=color, fill_color=color, fill_opacity=.025,
                               stroke_width=2, stroke_opacity=opacity)
        head = Circle(radius=.72, color=color, stroke_width=3 if sharp else 7,
                      stroke_opacity=opacity).move_to([0, .1, 0])
        left_ear = Polygon([-.58, .58, 0], [-.38, 1.15, 0], [-.12, .73, 0],
                           color=color, stroke_width=3, stroke_opacity=opacity)
        right_ear = Polygon([.58, .58, 0], [.38, 1.15, 0], [.12, .73, 0],
                            color=color, stroke_width=3, stroke_opacity=opacity)
        eyes = VGroup(Dot([-.25, .2, 0], radius=.055, color=color),
                      Dot([.25, .2, 0], radius=.055, color=color)).set_opacity(opacity)
        nose = Dot([0, -.05, 0], radius=.045, color=ACCENT).set_opacity(opacity)
        details = VGroup(
            Line([-.15, -.2, 0], [0, -.3, 0], color=color, stroke_width=2),
            Line([0, -.3, 0], [.15, -.2, 0], color=color, stroke_width=2),
            Line([-.18, -.08, 0], [-.82, -.02, 0], color=color, stroke_width=1.8),
            Line([-.18, -.18, 0], [-.82, -.3, 0], color=color, stroke_width=1.8),
            Line([.18, -.08, 0], [.82, -.02, 0], color=color, stroke_width=1.8),
            Line([.18, -.18, 0], [.82, -.3, 0], color=color, stroke_width=1.8),
            label("CAT", 17, color).move_to([0, -1.25, 0]),
        )
        details.set_opacity(1 if sharp else 0)
        return VGroup(box, head, left_ear, right_ear, eyes, nose, details)

    def mode_token(self, name, color, frequency):
        frame = RoundedRectangle(width=2.35, height=.78, corner_radius=.14,
                                 color=color, fill_color=color, fill_opacity=.035, stroke_width=1.8)
        xs = np.linspace(-.65, .65, 70)
        points = [np.array([.35 + x, .17 * np.sin(frequency * x * 2.2), 0]) for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=2.6, stroke_opacity=.9)
        curve.set_points_smoothly(points)
        return VGroup(frame, label(name, 19, color).move_to([-.72, 0, 0]), curve)

    def eigen_row(self, direction, eigenvalue, speed, color, strength):
        frame = RoundedRectangle(width=6.7, height=1.0, corner_radius=.16,
                                 color=color, fill_color=color, fill_opacity=.03, stroke_width=1.8)
        gauge_bg = RoundedRectangle(width=1.55, height=.32, corner_radius=.08,
                                    stroke_width=0, fill_color=ZERO, fill_opacity=.45)
        gauge_fill = RoundedRectangle(width=max(.12, 1.35 * strength), height=.2,
                                      corner_radius=.05, stroke_width=0,
                                      fill_color=color, fill_opacity=.9)
        gauge_fill.align_to(gauge_bg, LEFT).shift(RIGHT * .1)
        gauge = VGroup(gauge_bg, gauge_fill).move_to([1.05, 0, 0])
        return VGroup(frame,
                      label(direction, 19, color).move_to([-2.35, 0, 0]),
                      label(eigenvalue, 21, INK).move_to([-.65, 0, 0]), gauge,
                      label(speed, 18, color).move_to([2.45, 0, 0]))

    def decay_plot(self, eigenvalue, color, title, center):
        axes = VGroup(Line([-1.25, -.75, 0], [1.35, -.75, 0], color=MUTED, stroke_width=1.6),
                      Line([-1.25, -.75, 0], [-1.25, .95, 0], color=MUTED, stroke_width=1.6))
        ts = np.linspace(0, 1, 90)
        points = [np.array([-1.2 + 2.45 * t, -.7 + 1.45 * np.exp(-3.2 * eigenvalue * t), 0])
                  for t in ts]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.92)
        curve.set_points_smoothly(points)
        group = VGroup(axes, label(title, 20, color).move_to([0, 1.25, 0]), curve,
                       label("error", 16, MUTED).rotate(PI / 2).move_to([-1.55, .15, 0]),
                       label("time", 16, MUTED).move_to([.9, -1.05, 0]))
        group.move_to(center)
        return group

    def rate_panel(self, title, color, eigenvalue):
        box = RoundedRectangle(width=3.65, height=4.25, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035, stroke_width=2.2)
        check = card("Representable  ✓", GOOD, 2.75, .68, 19, .12).move_to([0, 1.15, 0])
        plot = self.decay_plot(eigenvalue, color,
                               "fast decay" if eigenvalue > .5 else "slow decay", [0, -.55, 0])
        plot.scale(.78)
        return VGroup(box, label(title, 21, color).move_to([0, 1.75, 0]), check, plot)

    def wave_curve(self, low, high, color, center, width=6.2, low_freq=1.0, high_freq=5.5):
        xs = np.linspace(-width / 2, width / 2, 220)
        points = [np.array([center[0] + x,
                            center[1] + .72 * low * np.sin(low_freq * x)
                            + .72 * high * np.sin(high_freq * x), 0]) for x in xs]
        curve = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=.92)
        curve.set_points_smoothly(points)
        return curve

    def plot_box(self, title, color, center):
        box = RoundedRectangle(width=3.55, height=3.6, corner_radius=.2,
                               color=color, fill_color=color, fill_opacity=.025, stroke_width=2)
        box.move_to(center)
        return VGroup(box, label(title, 19, color).move_to(np.array(center) + UP * 1.45))

    def wave_panel(self, title, low, high, color, high_freq=5.5):
        frame = self.plot_box(title, color, [0, 0, 0])
        curve = self.wave_curve(low, high, color, [0, 0, 0], width=3.0, high_freq=high_freq)
        return VGroup(frame, curve)

    def network_icon(self, hidden_count, color):
        left = VGroup(*[Dot([-1.0, y, 0], radius=.08, color=MUTED) for y in [-.65, 0, .65]])
        ys = np.linspace(-1.0, 1.0, hidden_count)
        hidden = VGroup(*[Dot([0, y, 0], radius=.055, color=color) for y in ys])
        right = VGroup(*[Dot([1.0, y, 0], radius=.08, color=GOOD) for y in [-.45, .45]])
        links = VGroup(*[
            Line(a.get_center(), b.get_center(), color=ZERO, stroke_width=.8, stroke_opacity=.35)
            for ga, gb in [(left, hidden), (hidden, right)] for a in ga for b in gb
        ])
        return VGroup(links, left, hidden, right)

    def target_prediction_frame(self, target, prediction):
        return VGroup(target, prediction,
                      label("TARGET", 19, ACCENT).move_to([-3.05, 2.25, 0]),
                      label("PREDICTION", 19, GOOD).move_to([-2.75, -.35, 0]),
                      Line([-3.4, -.05, 0], [3.4, -.05, 0], color=ZERO, stroke_width=1.4))

    def component_row(self, name, low, high, color, high_freq=5.5):
        frame = RoundedRectangle(width=6.8, height=1.35, corner_radius=.18,
                                 color=color, fill_color=color, fill_opacity=.025, stroke_width=1.8)
        curve = self.wave_curve(low, high, color, [.6, 0, 0], width=4.9, high_freq=high_freq)
        return VGroup(frame, label(name, 20, color).move_to([-2.55, 0, 0]), curve)

    def error_bar(self, name, value, color):
        frame = RoundedRectangle(width=6.4, height=1.05, corner_radius=.16,
                                 color=color, fill_color=color, fill_opacity=.025, stroke_width=1.8)
        track = RoundedRectangle(width=4.35, height=.38, corner_radius=.09,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.45)
        fill = RoundedRectangle(width=max(.15, 4.0 * value), height=.23, corner_radius=.06,
                                stroke_width=0, fill_color=color, fill_opacity=.9)
        fill.align_to(track, LEFT).shift(RIGHT * .17)
        gauge = VGroup(track, fill).move_to([.65, 0, 0])
        return VGroup(frame, label(name, 20, color).move_to([-2.25, 0, 0]), gauge)

    def set_bar(self, bar, value):
        old_fill = bar[2][1]
        track = bar[2][0]
        new_fill = RoundedRectangle(width=max(.15, 4.0 * value), height=.23, corner_radius=.06,
                                    stroke_width=0, fill_color=old_fill.get_fill_color(),
                                    fill_opacity=.9)
        new_fill.align_to(track, LEFT).shift(RIGHT * .17).move_to(
            [track.get_left()[0] + .17 + max(.15, 4.0 * value) / 2, track.get_y(), 0]
        )
        return ReplacementTransform(old_fill, new_fill)

    def learnability_panel(self, title, color, progress):
        box = RoundedRectangle(width=3.55, height=4.0, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035, stroke_width=2.3)
        check = card("Representable  ✓", GOOD, 2.75, .72, 20, .13).move_to([0, .75, 0])
        track = RoundedRectangle(width=2.8, height=.42, corner_radius=.1,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.45)
        fill = RoundedRectangle(width=2.5 * progress, height=.25, corner_radius=.07,
                                stroke_width=0, fill_color=color, fill_opacity=.92)
        fill.align_to(track, LEFT).shift(RIGHT * .15)
        gauge = VGroup(track, fill).move_to([0, -.55, 0])
        return VGroup(box, label(title, 22, color).move_to([0, 1.55, 0]), check, gauge,
                      label("training progress", 18, MUTED).move_to([0, -1.25, 0]))

    def noisy_points(self):
        xs = np.linspace(-3.1, 3.1, 17)
        noise = np.array([.15, -.18, .12, -.1, .2, -.16, .08, -.14, .18,
                          -.2, .1, -.08, .16, -.13, .2, -.15, .1])
        ys = .78 * np.sin(.75 * xs) + noise
        return VGroup(*[Dot([x, y + .2, 0], radius=.075, color=WEIGHT) for x, y in zip(xs, ys)])

    def path(self, points, color, width=3, smooth=False):
        path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=.7)
        points = [np.array(point, dtype=float) for point in points]
        if smooth:
            path.set_points_smoothly(points)
        else:
            path.set_points_as_corners(points)
        return path

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
