"""Neural Network Mathematics 06: local stability versus coordinate dependence."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, size=25):
    box = RoundedRectangle(width=width, height=.82, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.11)
    return VGroup(box, label(value, size, color, width-.2))


class NeuralMathFlatnessGeneralization(Scene):
    DURATION = 97

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  06", 18, MUTED).move_to(UP*7.3),
            label("평평한 해가 정말 더 좋은 모델일까?", 28).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:07 — Two equally low solutions.
        self.copy("같은 Loss, 다른 모양", "SHARP  vs  FLAT",
                  "둘 다 낮은 Loss의 해입니다.\n어느 쪽이 더 좋은 해일까요?")
        sharp = self.bowl(.58, PRUNE, "Sharp").move_to([-2.0, .1, 0])
        flat = self.bowl(1.35, GOOD, "Flat").move_to([2.0, .1, 0])
        values = VGroup(label("Loss = 0.01", 21, PRUNE).move_to([-2.0, -2.65, 0]),
                        label("Loss = 0.01", 21, GOOD).move_to([2.0, -2.65, 0]))
        self.show(VGroup(sharp, flat, values))
        self.to(7)

        # 00:07–00:14 — Equal Euclidean perturbations show real local stability.
        self.copy("첫 주장: Flat은 안정적이다", "SAME ‖Δθ‖  ·  DIFFERENT ΔLOSS",
                  "같은 크기로 움직이면 Sharp의 Loss는 오르고\nFlat은 낮은 Loss를 유지합니다.")
        sharp = self.bowl(.58, PRUNE, "Sharp").move_to([-2.0, .1, 0])
        flat = self.bowl(1.35, GOOD, "Flat").move_to([2.0, .1, 0])
        s_point = Dot(sharp[3].get_center() + np.array([.42, 1.0, 0]),
                      radius=.085, color=ACCENT)
        f_point = Dot(flat[3].get_center() + np.array([.42, .18, 0]),
                      radius=.085, color=ACCENT)
        arrows = VGroup(Arrow(sharp[3].get_center(), s_point.get_center(), buff=.1,
                              color=ACCENT, tip_length=.15),
                        Arrow(flat[3].get_center(), f_point.get_center(), buff=.1,
                              color=ACCENT, tip_length=.15))
        self.show(VGroup(sharp, flat, s_point, f_point, arrows,
                         card("Flat  →  stable", GOOD, 3.3, 26).move_to([0, -2.8, 0])))
        self.to(14)

        # 00:14–00:22 — The tempting generalization claim remains a question.
        self.copy("일반화로 이어지는 매력적인 직관", "FLAT  ⇒  BETTER TEST PERFORMANCE  ?",
                  "주변에서도 잘 작동하면 새 데이터에도\n안정적일까요? 아직 가설입니다.")
        train = card("Training Data", WEIGHT, 3.2, 25).move_to([-1.9, 1.6, 0])
        test = card("Test Data  ?", ACCENT, 3.2, 25).move_to([1.9, 1.6, 0])
        arrow = Arrow(train.get_right(), test.get_left(), buff=.16,
                      color=MUTED, stroke_width=3, tip_length=.16)
        cloud = VGroup(*[Dot([x, y, 0], radius=.08, color=GOOD)
                         for x,y in ((-1.4,-.5),(-.8,-.1),(-.3,-.7),(.35,-.25),(.9,-.65),(1.5,-.2))])
        region = Ellipse(width=5.2, height=1.7, color=GOOD, fill_color=GOOD,
                         fill_opacity=.1).move_to([0, -.45, 0])
        question = label("Flat Minimum  →  Better Generalization?", 26, ACCENT)
        question.move_to([0, -2.55, 0])
        self.show(VGroup(train, test, arrow, region, cloud, question))
        self.to(22)

        # 00:22–00:28 — The reversal: identical functions.
        self.copy("반대편에서 온 질문", "SAME FUNCTION  ·  DIFFERENT SHAPE?",
                  "함수는 전혀 바꾸지 않고\n평평함만 바꿀 수 있을까요?")
        pair = VGroup(card("θ", WEIGHT, 2.1, 31),
                      label("≠", 32, MUTED),
                      card("θ′", SPARSE, 2.1, 31)).arrange(RIGHT, buff=.34)
        pair.move_to([0, 1.45, 0])
        same = card("fθ(x) = fθ′(x)", GOOD, 5.1, 32).move_to([0, -.35, 0])
        only_shape = label("Flatness can change?", 29, ACCENT).move_to([0, -2.1, 0])
        self.show(VGroup(pair, same, only_shape))
        self.to(28)

        # 00:28–00:36 — Parameter symmetry in a two-factor linear model.
        self.copy("Parameter Symmetry를 다시 보면", "(w₁,w₂)  →  (cw₁,w₂/c)",
                  "한 값을 c배하고 다른 값을 c로 나누면\n곱과 함수 f(x)=6x는 그대로입니다.")
        chain = VGroup(card("x", WEIGHT, 1.25, 28), label("× w₁", 23, ACCENT),
                       card("h", SPARSE, 1.25, 28), label("× w₂", 23, ACCENT),
                       card("y", GOOD, 1.25, 28)).arrange(RIGHT, buff=.18)
        chain.move_to([0, 1.55, 0])
        before = card("(2,3)", WEIGHT, 2.4, 28).move_to([-1.75, -.35, 0])
        after = card("(200,0.03)", SPARSE, 3.3, 25).move_to([1.8, -.35, 0])
        connector = Arrow(before.get_right(), after.get_left(), buff=.12,
                          color=ACCENT, tip_length=.17)
        invariant = card("f(x) = 6x", GOOD, 3.9, 31).move_to([0, -2.35, 0])
        self.show(VGroup(chain, before, after, connector, invariant))
        self.to(36)

        # 00:36–00:46 — The same 0.1 coordinate move has a different scale.
        self.copy("같은 0.1 이동의 의미는?", "DIFFERENT PARAMETER SCALES",
                  "두 좌표의 스케일은 크게 다릅니다.\n같은 0.1 이동은 같은 함수 변화가 아닙니다.")
        left = VGroup(card("(2,3)", WEIGHT, 2.8, 27),
                      label("w₂ + 0.1", 22, ACCENT),
                      card("Δ(w₁w₂) = 0.2", WEIGHT, 3.1, 21)).arrange(DOWN, buff=.38)
        right = VGroup(card("(200,0.03)", SPARSE, 3.2, 24),
                       label("w₂ + 0.1", 22, ACCENT),
                       card("Δ(w₁w₂) = 20", SPARSE, 3.1, 21)).arrange(DOWN, buff=.38)
        left.move_to([-1.95, .15, 0]); right.move_to([1.95, .15, 0])
        divider = Line([0, 2.25, 0], [0, -2.35, 0], color=MUTED, stroke_opacity=.3)
        self.show(VGroup(left, right, divider))
        self.to(46)

        # 00:46–00:56 — Exact curvature counterexample for the toy loss.
        self.copy("함수는 같은데 Sharpness가 바뀝니다", "L = (w₁w₂ − 6)²",
                  "같은 함수와 Loss 0이어도 최대 곡률은\n26에서 약 80,000으로 바뀝니다.")
        flat = self.bowl(1.18, GOOD, "flatter").scale(.82).move_to([-1.95, .6, 0])
        sharp = self.bowl(.42, PRUNE, "sharper").scale(.82).move_to([1.95, .6, 0])
        numbers = VGroup(card("λmax = 26", GOOD, 3.15, 24).move_to([-1.95, -1.95, 0]),
                         card("λmax ≈ 80,000", PRUNE, 3.45, 22).move_to([1.95, -1.95, 0]))
        same = label("same f(x)=6x  ·  same Loss=0", 22, ACCENT).move_to([0, -3.05, 0])
        self.show(VGroup(flat, sharp, numbers, same))
        self.to(56)

        # 00:56–01:06 — Equal visual weight for both true viewpoints.
        self.copy("두 관점이 정면으로 충돌합니다", "WHAT DOES FLATNESS MEASURE?",
                  "Flat은 정해진 좌표에서 안정적입니다.\n하지만 같은 함수도 좌표에 따라 다르게 보입니다.")
        left = self.argument_panel("Flatness", "Local Stability", GOOD).move_to([-1.95, .3, 0])
        right = self.argument_panel("Same Function", "Different Flatness", SPARSE).move_to([1.95, .3, 0])
        clash = label("VS", 37, ACCENT).move_to([0, .4, 0])
        self.show(VGroup(left, right, clash))
        self.to(66)

        # 01:06–01:13 — A coordinate grid changes shape while the terrain does not.
        self.copy("같은 지도, 다른 눈금", "COORDINATES CHANGE THE MEASURE",
                  "지형이 같아도 축 눈금이 바뀌면\n보이는 경사와 거리의 값은 달라집니다.")
        contour = VGroup(*[Ellipse(width=w, height=h, color=GOOD,
                                    stroke_opacity=.5, stroke_width=2)
                           for w,h in ((.9,.9),(1.6,1.6),(2.4,2.4))])
        first = contour.copy().scale(.85).move_to([-1.9, .2, 0])
        second = contour.copy().stretch(1.55, dim=0).stretch(.55, dim=1)
        second.scale(.85).move_to([1.9, .2, 0])
        axes = VGroup(label("equal scale", 22, WEIGHT).move_to([-1.9, -2.05, 0]),
                      label("rescaled axes", 22, SPARSE).move_to([1.9, -2.05, 0]))
        self.show(VGroup(first, second, axes))
        self.to(73)

        # 01:13–01:21 — Neither viewpoint gets dismissed.
        self.copy("처음 직관도 여전히 중요합니다", "DEFINE THE PERTURBATION FIRST",
                  "Flatness는 쓸모 있는 국소 정보입니다.\n좌표와 변화의 크기·방식을 먼저 정해야 합니다.")
        sharp = self.bowl(.58, PRUNE, "Sharp").scale(.8).move_to([-1.95, .25, 0])
        flat = self.bowl(1.35, GOOD, "Flat").scale(.8).move_to([1.95, .25, 0])
        question = card("Which coordinates?  Which Δθ?", ACCENT, 6.4, 25)
        question.move_to([0, -2.85, 0])
        self.show(VGroup(sharp, flat, question))
        self.to(81)

        # 01:21–01:28 — Make the user's metric choice explicit.
        self.copy("무엇을 측정하려는가?", "CHOOSE THE COMPARISON",
                  "실제 변화에 대한 안정성인가,\n표현 방식에 무관한 비교인가? 목적을 선택해야 합니다.")
        left = self.argument_panel("Local Robustness", "specified Δθ", GOOD)
        right = self.argument_panel("Invariant Comparison", "same function", SPARSE)
        left.move_to([-1.95, .3, 0]); right.move_to([1.95, .3, 0])
        selector = label("measurement choice", 25, ACCENT).move_to([0, -2.6, 0])
        self.show(VGroup(left, right, selector))
        self.to(88)

        # 01:28–01:37 — The next question: parameter versus functional geometry.
        self.copy("모델의 거리와 복잡도는 어디서 잴까?", "PARAMETER  vs  FUNCTIONAL GEOMETRY",
                  "좌표를 바꿔도 함수는 그대로입니다.\n무엇을 기준으로 모델을 비교해야 할까요?")
        left = card("Parameter Geometry", WEIGHT, 3.35, 23).move_to([-1.9, 2.1, 0])
        right = card("Functional Geometry", GOOD, 3.35, 23).move_to([1.9, 2.1, 0])
        stretched = Ellipse(width=2.9, height=.95, color=WEIGHT).move_to([-1.9, .15, 0])
        graph = self.function_graph().scale(.72).move_to([1.9, .05, 0])
        bridge = Arrow([-.15, .1, 0], [.35, .1, 0], color=ACCENT,
                       stroke_width=3, tip_length=.16)
        question = label("어떤 거리가 의미 있을까?", 30, ACCENT).move_to([0, -2.7, 0])
        self.show(VGroup(left, right, stretched, graph, bridge, question))
        self.to(97)

    def bowl(self, width, color, name):
        xmax = .65 if width < .7 else 1.3
        curve = VMobject(color=color, stroke_width=5)
        curve.set_points_smoothly([[x, -.65 + 1.8*(x/width)**2, 0]
                                   for x in np.linspace(-xmax, xmax, 61)])
        base = Line([-1.45, -1.35, 0], [1.45, -1.35, 0], color=MUTED, stroke_opacity=.5)
        dot = Dot([0, -.65, 0], radius=.1, color=ACCENT)
        tag = label(name, 25, color).move_to([0, 2.05, 0])
        return VGroup(base, curve, tag, dot)

    def argument_panel(self, title, detail, color):
        frame = RoundedRectangle(width=3.42, height=4.2, corner_radius=.2,
                                 stroke_color=color, stroke_width=2,
                                 fill_color=color, fill_opacity=.07)
        top = label(title, 26, color, 3.1).move_to([0, .8, 0])
        body = label(detail, 23, INK, 3.1).move_to([0, -.55, 0])
        return VGroup(frame, top, body)

    def function_graph(self):
        x = Line([-1.55, 0, 0], [1.55, 0, 0], color=MUTED)
        y = Line([0, -1.5, 0], [0, 1.5, 0], color=MUTED)
        line = Line([-1.25, -1.25, 0], [1.25, 1.25, 0], color=GOOD, stroke_width=5)
        return VGroup(x, y, line)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP*5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN*4.45)
        self.caption_box = RoundedRectangle(width=7.65, height=1.15,
                                             corner_radius=.14, stroke_color=ZERO,
                                             stroke_width=1.2, fill_color=ZERO,
                                             fill_opacity=.32).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note),
                  FadeIn(self.caption_box), FadeIn(self.caption), run_time=.2)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP*.12), run_time=.4)

    def to(self, target):
        remaining = target-self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target-self.time))
