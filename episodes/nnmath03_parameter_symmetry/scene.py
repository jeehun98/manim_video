"""Neural Network Mathematics 03: different parameters, identical functions."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def badge(value, color=WEIGHT, width=3, size=26):
    frame = RoundedRectangle(width=width, height=.9, corner_radius=.16,
                             stroke_color=color, stroke_width=2,
                             fill_color=color, fill_opacity=.12)
    return VGroup(frame, label(value, size, color, width - .25))


class NeuralMathParameterSymmetry(Scene):
    DURATION = 132

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        title = label("백만 개의 파라미터가 정말 백만 개의 역할을 할까?", 26)
        title.move_to(UP * 6.45)
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  03", 18, MUTED).move_to(UP * 7.3),
            title,
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:12 — A large network raises the question.
        self.copy("백만 개의 파라미터", "1,000,000 PARAMETERS",
                  "파라미터 백만 개는 정말 백만 개의\n독립적인 역할을 뜻할까요?")
        network = self.network()
        count = label("1,000,000 Parameters", 40, ACCENT).move_to([0, -2.25, 0])
        params = label("θ₁, θ₂, θ₃, …, θ₁,₀₀₀,₀₀₀", 25, WEIGHT).move_to([0, 2.7, 0])
        self.show(VGroup(network, count, params))
        self.to(12)

        # 00:12–00:22 — The two-weight toy model.
        self.copy("두 파라미터만 남겨봅시다", "w₁ = 2     ·     w₂ = 3",
                  "입력에 2를 곱하고 다시 3을 곱합니다.\n전체 함수는 f(x)=6x입니다.")
        chain = self.chain("× 2", "× 3", "2x", "6x")
        formula = badge("f(x) = 6x", GOOD, 4.0, 32).move_to([0, -2.2, 0])
        self.show(VGroup(chain, formula))
        self.to(22)

        # 00:22–00:36 — Both weights change; the graph stays fixed.
        self.copy("숫자는 모두 바뀌었는데", "(2, 3)  →  (1, 6)",
                  "이제 1과 6으로 바꿉니다.\n파라미터는 달라도 함수는 여전히 f(x)=6x입니다.")
        graph = self.function_graph().scale(.8).move_to([0, -1.2, 0])
        old = badge("(2, 3)", WEIGHT, 2.3).move_to([-1.65, 2.2, 0])
        new = badge("(1, 6)", ACCENT, 2.3).move_to([1.65, 2.2, 0])
        arrow = Arrow(old.get_right(), new.get_left(), buff=.12, color=MUTED,
                      stroke_width=3, tip_length=.16)
        self.show(VGroup(old, arrow, new, graph))
        self.to(36)

        # 00:36–00:48 — Distinct coordinates in parameter space.
        self.copy("파라미터 공간에서는 다른 점", "(w₁, w₂)  ∈  ℝ²",
                  "(2,3)과 (1,6)은 서로 다른 좌표입니다.\n두 점 사이에는 분명한 거리도 있습니다.")
        axes = self.axes_2d()
        a = self.xy(2, 3)
        b = self.xy(1, 6)
        points = VGroup(Dot(a, radius=.12, color=WEIGHT), Dot(b, radius=.12, color=ACCENT),
                        label("(2,3)", 21, WEIGHT).next_to(a, RIGHT, buff=.18),
                        label("(1,6)", 21, ACCENT).next_to(b, RIGHT, buff=.18),
                        DashedLine(a, b, color=MUTED, dash_length=.14))
        self.show(VGroup(axes, points))
        self.to(48)

        # 00:48–01:04 — The full positive branch of w1*w2=6.
        self.copy("같은 함수는 두 점에만 있지 않습니다", "w₁w₂ = 6",
                  "(1,6), (2,3), (3,2), (6,1).\n곱이 6인 한, 함수는 계속 f(x)=6x입니다.")
        axes = self.axes_2d()
        curve = self.hyperbola()
        samples = VGroup()
        for x, y in ((1, 6), (2, 3), (3, 2), (6, 1)):
            p = self.xy(x, y)
            samples.add(Dot(p, radius=.095, color=ACCENT),
                        label(f"({x},{y})", 17, ACCENT).next_to(p, UP, buff=.12))
        invariant = badge("f(x) = 6x", GOOD, 3.4, 27).move_to([1.95, -2.7, 0])
        self.show(VGroup(axes, curve, samples, invariant))
        moving = Dot(self.xy(1, 6), radius=.15, color=GOOD)
        self.add(moving)
        self.play(MoveAlongPath(moving, curve), run_time=2.3, rate_func=linear)
        self.remove(moving)
        self.to(64)

        # 01:04–01:20 — Name the symmetry once the example is established.
        self.copy("서로 다른 파라미터, 같은 함수", "PARAMETER SYMMETRY",
                  "θ와 θ′는 달라도 두 함수는 같을 수 있습니다.\n이런 중복 표현을 파라미터 대칭성이라 부릅니다.")
        pair = VGroup(badge("θ ≠ θ′", ACCENT, 3.0, 31),
                      label("but", 24, MUTED),
                      badge("fθ = fθ′", GOOD, 3.0, 31)).arrange(DOWN, buff=.32)
        pair.move_to([0, .75, 0])
        term = label("Parameter Symmetry", 37, SPARSE).move_to([0, -2.6, 0])
        self.show(VGroup(pair, term))
        self.to(80)

        # 01:20–01:33 — Return to a high-dimensional neural network.
        self.copy("다시 백만 차원으로", "θ ∈ ℝ¹,⁰⁰⁰,⁰⁰⁰",
                  "실제 신경망의 구조는 훨씬 복잡하지만\n서로 다른 위치가 반드시 다른 함수를 뜻하지는 않습니다.")
        rays = self.radial_axes(26)
        center = Dot(ORIGIN, radius=.18, color=ACCENT)
        formula = label("θ ∈ ℝ¹,⁰⁰⁰,⁰⁰⁰", 34, INK).move_to([0, 2.9, 0])
        self.show(VGroup(rays, center, formula))
        self.to(93)

        # 01:33–01:46 — Parameter count does not establish independent roles.
        self.copy("좌표의 수와 역할의 수", "COUNT  ≠  INDEPENDENT ROLES",
                  "백만 개의 파라미터는 백만 차원 좌표를 뜻합니다.\n그것만으로 백만 개의 독립 기능은 보장되지 않습니다.")
        left = badge("Parameter space", WEIGHT, 3.0, 22).move_to([-2.1, 2.3, 0])
        right = badge("Function", GOOD, 2.4, 24).move_to([2.2, -1.3, 0])
        sources = VGroup(*[Dot([-2.15, y, 0], radius=.09, color=WEIGHT)
                           for y in (1.0, .2, -.6, -1.4, -2.2)])
        links = VGroup(*[Arrow(dot.get_center(), right.get_left(), buff=.15,
                               color=SPARSE, stroke_width=2, stroke_opacity=.75,
                               tip_length=.12) for dot in sources])
        count = label("1,000,000 Parameters  ≟  Independent Roles?", 23, ACCENT)
        count.move_to([0, -3.2, 0])
        self.show(VGroup(left, right, sources, links, count))
        self.to(106)

        # 01:46–01:58 — Relate the result to the earlier two episodes.
        self.copy("앞의 두 영상과 연결하면", "d ≪ D     ·     SOLUTION SET     ·     SYMMETRY",
                  "작은 학습 자유도, 큰 해 집합, 같은 함수의 중복 표현.\n파라미터 수와 실질적 자유도는 같은 개념이 아닙니다.")
        cards = VGroup(badge("01  d ≪ D", WEIGHT, 5.5, 27),
                       badge("02  solution set", SPARSE, 5.5, 27),
                       badge("03  fθ = fθ′", GOOD, 5.5, 27)).arrange(DOWN, buff=.4)
        cards.move_to([0, .15, 0])
        self.show(cards)
        self.to(118)

        # 01:58–02:12 — Close on a question about model distance.
        self.copy("그렇다면 모델 사이의 거리는?", "‖θA − θB‖  vs  fθA = fθB",
                  "파라미터 공간에서 멀어도 함수는 같을 수 있습니다.\n두 신경망의 거리는 무엇으로 재야 할까요?")
        a, b = np.array([-3, 1.4, 0]), np.array([3, 1.4, 0])
        top = VGroup(Dot(a, radius=.13, color=WEIGHT), Dot(b, radius=.13, color=ACCENT),
                     label("θA", 24, WEIGHT).next_to(a, UP, buff=.2),
                     label("θB", 24, ACCENT).next_to(b, UP, buff=.2),
                     DoubleArrow(a + DOWN * .45, b + DOWN * .45, buff=0,
                                 color=MUTED, stroke_width=3, tip_length=.17),
                     label("‖θA − θB‖", 26, MUTED).move_to([0, .25, 0]))
        same = badge("fθA(x) = fθB(x)", GOOD, 5.4, 30).move_to([0, -1.55, 0])
        question = label("파라미터가 다르면, 정말 다른 모델일까?", 28, ACCENT)
        question.move_to([0, -3.0, 0])
        self.show(VGroup(top, same, question))
        self.to(132)

    def network(self):
        layers = ((-3.1, 3), (-1.55, 5), (0, 6), (1.55, 5), (3.1, 3))
        dots = [[Dot([x, (j - (n - 1) / 2) * .72, 0], radius=.065, color=WEIGHT)
                 for j in range(n)] for x, n in layers]
        links = VGroup(*[Line(p.get_center(), q.get_center(), color=WEIGHT,
                              stroke_width=1.1, stroke_opacity=.25)
                         for left, right in zip(dots[:-1], dots[1:])
                         for p in left for q in right])
        return VGroup(links, *[p for layer in dots for p in layer]).move_to([0, .2, 0])

    def chain(self, first, second, middle, output):
        positions = (-2.65, 0, 2.65)
        nodes = VGroup(*[badge(t, c, 1.35, 25).move_to([x, .25, 0])
                         for x, t, c in zip(positions, ("x", middle, output),
                                            (WEIGHT, SPARSE, GOOD))])
        arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                                buff=.08, color=MUTED, stroke_width=3, tip_length=.16)
                          for i in range(2)])
        tags = VGroup(label(first, 22, ACCENT).move_to([-1.35, 1.2, 0]),
                      label(second, 22, ACCENT).move_to([1.35, 1.2, 0]))
        return VGroup(nodes, arrows, tags)

    def function_graph(self):
        axes = Axes(x_range=[-1, 1, .5], y_range=[-6, 6, 3],
                    x_length=5.0, y_length=3.7, tips=False,
                    axis_config={"color": MUTED, "stroke_width": 2})
        graph = axes.plot(lambda x: 6 * x, x_range=[-.9, .9], color=GOOD, stroke_width=6)
        tag = label("y = 6x  (unchanged)", 22, GOOD).next_to(axes, DOWN, buff=.28)
        return VGroup(axes, graph, tag)

    def axes_2d(self):
        x = Arrow([-3.45, -2.2, 0], [3.4, -2.2, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.14)
        y = Arrow([-3.2, -2.45, 0], [-3.2, 2.8, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.14)
        return VGroup(x, y, label("w₁", 20, MUTED).move_to([3.45, -2.58, 0]),
                      label("w₂", 20, MUTED).move_to([-3.5, 2.75, 0]))

    def xy(self, x, y):
        return np.array([-3.15 + .95 * x, -2.17 + .74 * y, 0])

    def hyperbola(self):
        curve = VMobject(color=GOOD, stroke_width=5)
        curve.set_points_smoothly([self.xy(x, 6 / x) for x in np.linspace(.95, 6.35, 80)])
        return curve

    def radial_axes(self, count):
        rays = VGroup()
        for i in range(count):
            angle = TAU * i / count
            end = [3.1 * np.cos(angle), 2.1 * np.sin(angle), 0]
            rays.add(Line(ORIGIN, end, color=SPARSE, stroke_width=1.7,
                          stroke_opacity=.22 + .28 * (i % 4 == 0)))
        return rays

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
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
