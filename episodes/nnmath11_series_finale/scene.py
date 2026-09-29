"""Neural Network Mathematics finale: parameter space to learned solution."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, size=25, height=.86):
    box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.10)
    return VGroup(box, label(value, size, color, width-.2))


class NeuralMathSeriesFinale(Scene):
    DURATION = 86

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  FINALE", 18, MUTED).move_to(UP*7.3),
            label("왜 신경망은 문제보다 훨씬 클까?", 28).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 1 — Return to the opening question.
        self.copy("처음의 질문", "PROBLEM  ≪  MODEL",
                  "작은 문제에 왜 거대한 신경망을 쓸까요?\n시리즈는 이 질문에서 시작했습니다.")
        problem = self.tiny_problem().move_to([-2.1, 0, 0])
        network = self.network().move_to([1.65, 0, 0])
        self.show(VGroup(problem, network,
                         label("Problem", 22, GOOD).move_to([-2.1, -2.2, 0]),
                         label("Model", 22, WEIGHT).move_to([1.65, -2.2, 0])))
        self.to(5)

        # 2 — Some answers are representable by smaller models.
        self.copy("작은 모델도 답을 담을 수 있다", "fsmall(x)  ≈  flarge(x)",
                  "어떤 답은 작은 모델로도 표현됩니다.\n남는 파라미터는 낭비일까요?")
        small = card("small model", GOOD, 3.05, 25).move_to([-1.85, 1.05, 0])
        large = card("large model", WEIGHT, 3.05, 25).move_to([1.85, 1.05, 0])
        left_curve = self.polyline([[-3.05, -.9, 0], [-2.4, -.3, 0], [-1.85, -.75, 0],
                                    [-1.2, .05, 0], [-.65, -.1, 0]], GOOD, 4)
        right_curve = self.polyline([[.65, -.9, 0], [1.3, -.3, 0], [1.85, -.75, 0],
                                     [2.5, .05, 0], [3.05, -.1, 0]], WEIGHT, 4)
        self.show(VGroup(small, large, left_curve, right_curve,
                         label("similar output", 22, ACCENT).move_to([0, -2.3, 0])))
        self.to(10)

        # 3 — Training starts without the answer.
        self.copy("하지만 정답을 모르고 시작합니다", "θ₀  →  ?",
                  "학습은 정답을 알고 시작하지 않습니다.\n모르는 답을 찾아야 합니다.")
        field = RoundedRectangle(width=6.9, height=4.7, corner_radius=.25,
                                 stroke_color=WEIGHT, fill_color=WEIGHT, fill_opacity=.035)
        start = Dot([-2.45, -1.35, 0], color=ACCENT, radius=.13)
        target = label("★", 55, GOOD).move_to([2.0, 1.25, 0])
        self.show(VGroup(field, start, target,
                         label("θ₀", 25, ACCENT).next_to(start, DOWN, buff=.22),
                         label("unknown solution", 21, MUTED).move_to([1.6, 1.95, 0])))
        self.to(15)

        # 4 — The central distinction.
        self.copy("답을 담는 일과 찾는 일", "REPRESENT  ≠  FIND",
                  "답을 담는 데 필요한 크기와\n찾는 데 유리한 공간은 다릅니다.")
        left = self.panel("REPRESENT", "completed answer", GOOD).move_to([-1.9, 0, 0])
        right = self.panel("FIND", "learning path", WEIGHT).move_to([1.9, 0, 0])
        self.show(VGroup(left, right, label("≠", 38, ACCENT)))
        self.to(20)

        # 5 — Solution structure can change in a larger space.
        self.copy("커진 공간, 달라지는 해", "MORE DIRECTIONS  ·  SOLUTION SET",
                  "공간이 커지면 해의 구조와\n접근 방향도 달라질 수 있습니다.")
        narrow = RoundedRectangle(width=2.25, height=3.7, corner_radius=.18,
                                  stroke_color=SPARSE, fill_color=SPARSE, fill_opacity=.06).move_to([-1.9, 0, 0])
        wide = RoundedRectangle(width=3.75, height=4.6, corner_radius=.18,
                                stroke_color=WEIGHT, fill_color=WEIGHT, fill_opacity=.04).move_to([1.4, 0, 0])
        one = Dot([-1.9, .35, 0], color=GOOD, radius=.12)
        solution = Ellipse(width=2.8, height=1.15, color=GOOD,
                           fill_color=GOOD, fill_opacity=.15).rotate(PI/6).move_to([1.4, .15, 0])
        points = VGroup(*[Dot([1.4+x, .15+.34*x, 0], color=GOOD, radius=.065)
                          for x in np.linspace(-1.1, 1.1, 7)])
        self.show(VGroup(narrow, wide, one, solution, points,
                         label("small", 19, SPARSE).move_to([-1.9, -2.45, 0]),
                         label("expanded", 19, WEIGHT).move_to([1.4, -2.45, 0])))
        self.to(25)

        # 6 — Parameter symmetry.
        self.copy("파라미터 하나가 역할 하나는 아닙니다", "θA ≠ θB     but     fθA = fθB",
                  "서로 다른 파라미터가\n같은 함수를 만들 수도 있습니다.")
        dots = VGroup(*[Dot([x, 1.15, 0], radius=.11, color=WEIGHT if i % 2 else SPARSE)
                        for i, x in enumerate(np.linspace(-2.6, 2.6, 6))])
        branches = VGroup(*[Line(dot.get_center(), [0, -.55, 0],
                                 color=MUTED, stroke_opacity=.55, stroke_width=2)
                            for dot in dots])
        function = card("same function  f", GOOD, 4.7, 29).move_to([0, -1.25, 0])
        self.show(VGroup(branches, dots, function))
        self.to(30)

        # 7 — Connectivity and curvature are two aspects of the loss geometry.
        self.copy("해와 그 주변도 한 모양이 아닙니다", "MODE CONNECTIVITY  ·  HESSIAN",
                  "좋은 해는 연결되기도 합니다.\n주변 손실 변화는 방향마다 다릅니다.")
        a = Dot([-2.55, -.95, 0], color=GOOD, radius=.12)
        b = Dot([2.35, -.95, 0], color=GOOD, radius=.12)
        path = self.smooth([[-2.55, -.95, 0], [-1.4, .65, 0], [0, 1.0, 0],
                            [1.4, .45, 0], [2.35, -.95, 0]], GOOD, 5)
        rays = VGroup(*[Arrow([0, 1.0, 0], [dx, 1.0+dy, 0], color=ACCENT,
                              stroke_width=2, buff=0, tip_length=.12)
                        for dx, dy in ((-.4, .8), (.45, .9), (.85, .15), (-.8, -.05))])
        self.show(VGroup(path, a, b, rays,
                         label("low-loss path", 22, GOOD).move_to([0, -2.15, 0])))
        self.to(35)

        # 8 — Flatness depends on parameter coordinates.
        self.copy("Loss 지형도 절대적인 지도는 아닙니다", "SAME FUNCTION  ·  DIFFERENT GEOMETRY",
                  "같은 함수도 좌표에 따라\n평평하거나 날카롭게 보일 수 있습니다.")
        sharp = self.bowl(.58, PRUNE, "sharp").move_to([-1.85, 0, 0])
        flat = self.bowl(1.3, GOOD, "flat").move_to([1.85, 0, 0])
        self.show(VGroup(sharp, flat,
                         label("reparameterize", 20, ACCENT).move_to([0, -2.5, 0])))
        self.to(40)

        # 9 — Non-monotonic example for model size versus error.
        self.copy("크기와 일반화도 단순하지 않습니다", "DOUBLE DESCENT  ·  POSSIBLE PATTERN",
                  "모델을 키워도 오차가 다시 내려가는\n경우가 있었습니다.")
        axes = VGroup(Line([-3, -2.1, 0], [3, -2.1, 0], color=MUTED),
                      Line([-3, -2.1, 0], [-3, 2.0, 0], color=MUTED))
        curve = self.smooth([[-2.85, 1.55, 0], [-1.95, -.8, 0], [-.95, -.25, 0],
                             [-.1, 1.65, 0], [.55, .7, 0], [1.3, -.65, 0],
                             [2.7, -1.15, 0]], ACCENT, 5)
        self.show(VGroup(axes, curve,
                         label("model size", 20, MUTED).move_to([2.25, -2.55, 0]),
                         label("test error", 20, MUTED).move_to([-2.3, 2.2, 0])))
        self.to(46)

        # 10 — Optimizer follows one actual trajectory.
        self.copy("학습은 한 경로를 따라갑니다", "θ₀  →  θ₁  →  ···  →  θ*",
                  "해가 많아도 학습은 초기점에서\n하나의 경로를 따라갑니다.")
        targets = VGroup(*[Dot([x, y, 0], radius=.075, color=GOOD)
                           for x, y in ((-2, 1.5), (-.5, 1.55), (1.45, 1.4),
                                        (-1.6, -.2), (1.6, -.95), (2.65, .65))])
        path = self.polyline([[-2.7, -1.85, 0], [-1.8, -1.35, 0], [-.8, -.9, 0],
                              [.25, .25, 0], [1.45, 1.4, 0]], WEIGHT, 5)
        self.show(VGroup(targets, path, Dot([-2.7, -1.85, 0], color=ACCENT),
                         label("one training run", 21, WEIGHT).move_to([0, -2.55, 0])))
        self.to(51)

        # 11 — Representable does not imply reachable.
        self.copy("표현 가능해도 닿지 못할 수 있습니다", "REPRESENTABLE  ≠  REACHABLE",
                  "표현할 수 있는 답에 학습으로는\n닿지 못할 수도 있습니다.")
        field = RoundedRectangle(width=6.9, height=4.7, corner_radius=.25,
                                 stroke_color=SPARSE, fill_color=SPARSE, fill_opacity=.035)
        good = label("★", 54, GOOD).move_to([2.25, 1.2, 0])
        bad = Dot([1.15, -1.15, 0], color=PRUNE, radius=.14)
        path = self.polyline([[-2.5, -1.2, 0], [-1.35, -.55, 0],
                              [-.15, -1.05, 0], [1.15, -1.15, 0]], PRUNE, 5)
        self.show(VGroup(field, good, path, bad,
                         label("exists", 20, GOOD).move_to([2.25, 2, 0]),
                         label("trained", 20, PRUNE).move_to([1.15, -1.85, 0])))
        self.to(57)

        # 12 — Implicit bias among equal-loss solutions.
        self.copy("학습 방식도 해를 고릅니다", "IMPLICIT BIAS",
                  "도달 가능한 해가 여럿이어도\n학습 규칙은 특정 해를 선호할 수 있습니다.")
        solutions = VGroup(*[Dot([x, 1.0, 0], color=c, radius=.12)
                             for x, c in zip((-2.45, -.8, .85, 2.4),
                                             (SPARSE, GOOD, WEIGHT, ACCENT))])
        guides = VGroup(*[Line([-2.7, -1.65, 0], d.get_center(),
                               color=MUTED, stroke_opacity=.28, stroke_width=2)
                           for d in solutions])
        chosen = self.polyline([[-2.7, -1.65, 0], [-1.9, -.55, 0],
                                [-.8, 1.0, 0]], GOOD, 5)
        self.show(VGroup(guides, chosen, solutions,
                         label("same Training Loss", 22, MUTED).move_to([0, 2.15, 0]),
                         label("selected", 21, GOOD).move_to([-.8, 1.6, 0])))
        self.to(63)

        # 13 — Evaluate function behavior, not merely the scalar training loss.
        self.copy("같은 Loss도 끝은 아닙니다", "LOSS  →  FUNCTION BEHAVIOR",
                  "같은 Loss만으로는 부족합니다.\n주변 변화와 실제 동작도 살펴야 합니다.")
        equal = card("L(A) = L(B)", WEIGHT, 4.4, 29).move_to([0, 1.65, 0])
        arrows = VGroup(Arrow([-1, 1.05, 0], [-1.8, -.05, 0], color=MUTED, buff=.15),
                        Arrow([1, 1.05, 0], [1.8, -.05, 0], color=MUTED, buff=.15))
        a = card("Δf small", GOOD, 3.1, 24).move_to([-1.85, -.65, 0])
        b = card("Δf large", PRUNE, 3.1, 24).move_to([1.85, -.65, 0])
        self.show(VGroup(equal, arrows, a, b,
                         label("which change matters?", 22, ACCENT).move_to([0, -2.15, 0])))
        self.to(68)

        # 14 — Find large, represent compactly, conditionally.
        self.copy("큰 공간에서 찾고, 작게 담는다", "LARGE TO FIND  ·  SMALL TO REPRESENT",
                  "어떤 경우에는 큰 공간에서 찾은 답을\n작은 모델에 담을 수 있습니다.")
        large = card("100M parameters", WEIGHT, 3.5, 25).move_to([-1.9, 1.0, 0])
        small = card("20M parameters", GOOD, 3.5, 25).move_to([1.9, 1.0, 0])
        arrow = Arrow(large.get_right(), small.get_left(), buff=.12,
                      color=ACCENT, stroke_width=3, tip_length=.17)
        function = card("f large(x) ≈ f small(x)", GOOD, 5.4, 25).move_to([0, -1.25, 0])
        self.show(VGroup(large, small, arrow, function))
        self.to(73)

        # 15 — Revisit the initial picture with paths inside its extra space.
        self.copy("처음 질문으로 돌아갑니다", "EXTRA SPACE  CAN AID THE SEARCH",
                  "여분의 공간은 답을 담는 데만이 아니라\n찾는 과정에도 쓰일 수 있습니다.")
        frame = RoundedRectangle(width=6.9, height=4.7, corner_radius=.25,
                                 stroke_color=WEIGHT, fill_color=WEIGHT, fill_opacity=.035)
        center = label("★", 54, GOOD).move_to([1.8, .65, 0])
        routes = VGroup(
            self.polyline([[-2.6, -1.6, 0], [-1.5, -.7, 0], [-.3, .35, 0], [1.8, .65, 0]], WEIGHT, 3),
            self.polyline([[-2.6, -1.6, 0], [-2.1, 1.55, 0], [-.2, 1.8, 0], [1.8, .65, 0]], SPARSE, 3),
            self.polyline([[-2.6, -1.6, 0], [-.65, -1.85, 0], [1.1, -1.1, 0], [1.8, .65, 0]], ACCENT, 3),
        )
        self.show(VGroup(frame, routes, center,
                         Dot([-2.6, -1.6, 0], color=PRUNE),
                         label("space for learning paths", 21, GOOD).move_to([0, -2.6, 0])))
        self.to(79)

        # 16 — End card, with the series' final, qualified perspective.
        self.copy("신경망의 수학", "FROM PARAMETER SPACE TO LEARNED SOLUTION",
                  "신경망은 답을 표현하면서\n그 답을 찾아가는 시스템이기도 합니다.")
        top = label("The space to learn", 33, WEIGHT).move_to([0, 1.4, 0])
        neq = label("≠", 43, ACCENT).move_to([0, .15, 0])
        bottom = label("The space to represent", 33, GOOD).move_to([0, -1.15, 0])
        signature = label("신경망의 수학", 28, MUTED).move_to([0, -2.65, 0])
        self.show(VGroup(top, neq, bottom, signature))
        self.to(86)

    def tiny_problem(self):
        box = RoundedRectangle(width=2.3, height=2.3, corner_radius=.2,
                               stroke_color=GOOD, fill_color=GOOD, fill_opacity=.04)
        path = self.polyline([[-.8, -.4, 0], [-.4, -.05, 0], [0, .25, 0],
                              [.4, .55, 0], [.8, .85, 0]], GOOD, 4)
        return VGroup(box, path)

    def network(self):
        nodes = VGroup()
        wires = VGroup()
        layers = [(-1.2, (-.9, 0, .9)), (-.35, (-1.35, -.45, .45, 1.35)),
                  (.5, (-1.35, -.45, .45, 1.35)), (1.35, (-.9, 0, .9))]
        for i, (x, ys) in enumerate(layers):
            for y in ys:
                nodes.add(Dot([x, y, 0], radius=.07, color=WEIGHT if i < 3 else GOOD))
        for (x1, ys1), (x2, ys2) in zip(layers[:-1], layers[1:]):
            for y1 in ys1:
                for y2 in ys2:
                    wires.add(Line([x1, y1, 0], [x2, y2, 0],
                                   color=WEIGHT, stroke_opacity=.28, stroke_width=1.5))
        return VGroup(wires, nodes)

    def panel(self, title, detail, color):
        frame = RoundedRectangle(width=3.4, height=4.3, corner_radius=.2,
                                 stroke_color=color, stroke_width=2,
                                 fill_color=color, fill_opacity=.06)
        title_mob = label(title, 25, color, 3.0).move_to([0, .95, 0])
        detail_mob = label(detail, 22, INK, 3.0).move_to([0, -.75, 0])
        return VGroup(frame, title_mob, detail_mob)

    def bowl(self, width, color, name):
        xmax = .65 if width < .7 else 1.3
        curve = self.smooth([[x, -.8+1.65*(x/width)**2, 0]
                             for x in np.linspace(-xmax, xmax, 61)], color, 5)
        base = Line([-1.4, -1.45, 0], [1.4, -1.45, 0], color=MUTED, stroke_opacity=.5)
        tag = label(name, 23, color).move_to([0, 2.0, 0])
        return VGroup(base, curve, Dot([0, -.8, 0], color=ACCENT, radius=.085), tag)

    def polyline(self, points, color, width):
        line = VMobject(color=color, stroke_width=width)
        line.set_points_as_corners(points)
        return line

    def smooth(self, points, color, width):
        line = VMobject(color=color, stroke_width=width)
        line.set_points_smoothly(points)
        return line

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP*5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN*4.45)
        self.caption_box = RoundedRectangle(width=7.65, height=1.15, corner_radius=.14,
                                            stroke_color=ZERO, stroke_width=1.2,
                                            fill_color=ZERO, fill_opacity=.32).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note), FadeIn(self.caption_box),
                  FadeIn(self.caption), run_time=.2)

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
