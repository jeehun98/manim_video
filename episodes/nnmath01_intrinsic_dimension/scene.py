"""Neural Network Mathematics 01: random-subspace training and intrinsic dimension."""
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


def card(value, color=WEIGHT, width=2.8, height=.9, size=24, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .2))


class NeuralMathIntrinsicDimension(Scene):
    DURATION = 112

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  01", 18, MUTED).move_to(UP * 7.3),
            label("왜 모델은 필요 이상으로 큰 학습 공간에서 움직일까?", 28)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–8: begin with the scale mismatch, without teaching parameter space.
        self.copy(
            "백만 개의 파라미터, 백만 개의 방향", "θ ∈ ℝ¹,⁰⁰⁰,⁰⁰⁰",
            "파라미터가 백만 개인 신경망은\n백만 차원의 공간에서 학습됩니다.",
        )
        space = self.parameter_space()
        path = VMobject(color=ACCENT, stroke_width=4)
        path.set_points_smoothly([
            [-2.7, -1.7, 0], [-1.8, -.2, 0], [-.9, 1.1, 0],
            [.4, .65, 0], [1.25, 1.75, 0], [2.5, 1.2, 0],
        ])
        theta = Dot(path.get_start(), radius=.13, color=ACCENT)
        self.show(VGroup(space, path, theta))
        self.play(MoveAlongPath(theta, path), run_time=1.5, rate_func=smooth)
        self.to(8)

        # 8–16: most directions dim; pose the episode's question.
        self.copy(
            "정말 모든 방향이 필요할까요?", "1,000,000 DIRECTIONS  ?",
            "정말 이 백만 개의 방향이 모두 필요할까요?\n필요 이상으로 거대한 공간인 것은 아닐까요?",
        )
        axes = self.radial_axes(22)
        question = label("필요한 방향은 몇 개일까?", 34, ACCENT).move_to([0, -.3, 0])
        count = label("1,000,000", 54, INK).move_to([0, 1.2, 0])
        self.show(VGroup(axes, count, question))
        self.play(*[
            axis.animate.set_stroke(opacity=.08 if i % 5 else .65)
            for i, axis in enumerate(axes)
        ], run_time=1.3)
        self.to(16)

        # 16–26: insert a small random subspace into the full space.
        self.copy(
            "공간을 강제로 잘라본다면?", "RANDOM SUBSPACE",
            "무작위로 고른 작은 부분공간을 넣고\n모델이 그 밖으로 나가지 못하게 합니다.",
        )
        boundary = RoundedRectangle(
            width=7.0, height=5.0, corner_radius=.28,
            stroke_color=MUTED, stroke_width=2, fill_color=MUTED,
            fill_opacity=.025,
        ).move_to([0, .25, 0])
        plane = Polygon(
            [-3.0, -.9, 0], [1.65, -2.0, 0], [3.05, 1.25, 0], [-1.55, 2.3, 0],
            stroke_color=SPARSE, stroke_width=3,
            fill_color=SPARSE, fill_opacity=.18,
        )
        dots = VGroup(*[
            Dot([x, .22 * x + y, 0], radius=.055, color=SPARSE)
            for x, y in ((-2.2, -.1), (-1.4, .9), (-.6, -.7), (.2, .3),
                         (.8, -.5), (1.45, .6), (2.0, -.2))
        ])
        tags = VGroup(
            label("full space  ℝᴰ", 20, MUTED).move_to([0, 3.05, 0]),
            label("small space  ℝᵈ", 22, SPARSE).move_to([0, -2.55, 0]),
        )
        self.show(VGroup(boundary, plane, dots, tags))
        self.to(26)

        # 26–36: define the fixed projection and learned coordinates.
        self.copy(
            "학습 변수는 작은 좌표 φ뿐입니다", "θ = θ₀ + Pφ",
            "θ₀와 P는 고정하고 작은 좌표 φ만 학습합니다.\n실제 파라미터는 θ = θ₀ + Pφ로 정해집니다.",
        )
        formula = label("θ  =  θ₀  +  P φ", 48, INK).move_to([0, 1.55, 0])
        fixed = VGroup(
            card("θ₀  fixed", MUTED, 2.35, .82, 22),
            card("P  random + fixed", SPARSE, 2.95, .82, 20),
        ).arrange(RIGHT, buff=.35).move_to([0, .05, 0])
        learned = card("φ ∈ ℝᵈ   LEARNED", ACCENT, 4.1, 1.0, 25, .18)
        learned.move_to([0, -1.55, 0])
        brace = Brace(learned, DOWN, color=ACCENT)
        brace_text = label("d trainable coordinates", 20, ACCENT).next_to(brace, DOWN, buff=.18)
        self.show(VGroup(formula, fixed, learned, brace, brace_text))
        self.to(36)

        # 36–45: make the non-pruning distinction visually explicit.
        self.copy(
            "모델 크기는 그대로, 자유도만 줄입니다", "NOT PRUNING",
            "파라미터는 여전히 1,000,000개입니다.\n움직일 수 있는 자유도만 500개로 줄어듭니다.",
        )
        rows = VGroup(
            self.compare_row("PARAMETERS", "1,000,000", "1,000,000", GOOD),
            self.compare_row("DEGREES OF FREEDOM", "1,000,000", "500", ACCENT),
        ).arrange(DOWN, buff=.8).move_to([0, .4, 0])
        keep = label("same network representation", 20, GOOD).move_to([0, -2.35, 0])
        self.show(VGroup(rows, keep))
        self.to(45)

        # 45–55: make the naive failure intuition plausible.
        self.copy(
            "좋은 해를 놓치지 않을까요?", "INTUITION: TOO FEW DIRECTIONS",
            "좋은 해에 도달하기 어려워 보입니다.\n대부분의 방향을 처음부터 사용할 수 없으니까요.",
        )
        outer = RoundedRectangle(width=7.0, height=5.0, corner_radius=.3,
                                 stroke_color=MUTED, stroke_width=2)
        outer.move_to([0, .2, 0])
        plane = Polygon([-3, -1.2, 0], [2.4, -2, 0], [3, .1, 0], [-2.4, 1, 0],
                        color=SPARSE, fill_color=SPARSE, fill_opacity=.12)
        optimum = Dot([1.8, 1.75, 0], radius=.17, color=GOOD)
        ring = Circle(radius=.45, color=GOOD, stroke_opacity=.35).move_to(optimum)
        miss = label("good solution?", 21, GOOD).next_to(optimum, UP, buff=.25)
        track = DashedLine([-2.6, -.95, 0], [2.2, -1.63, 0], color=ACCENT)
        self.show(VGroup(outer, plane, optimum, ring, miss, track))
        self.to(55)

        # 55–65: show successful optimization constrained to the plane.
        self.copy(
            "그런데 작은 공간 안에서도 학습됩니다", "LOSS ↓   ·   PERFORMANCE ↑",
            "작은 공간 안에서도 loss는 내려가고\n모델은 기준 성능에 가까워질 수 있습니다.",
        )
        plane = Polygon([-3.1, -1.45, 0], [2.2, -2.1, 0], [3.1, .7, 0], [-2.2, 1.45, 0],
                        color=SPARSE, fill_color=SPARSE, fill_opacity=.13)
        path = VMobject(color=ACCENT, stroke_width=5)
        path.set_points_smoothly([
            [-2.4, -.9, 0], [-1.6, .3, 0], [-.6, -.2, 0],
            [.25, .65, 0], [1.1, .35, 0], [1.85, 1.0, 0],
        ])
        point = Dot(path.get_start(), radius=.13, color=ACCENT)
        loss = VGroup(
            label("LOSS", 18, MUTED),
            *[Rectangle(width=.28, height=h, fill_color=c, fill_opacity=.8, stroke_width=0)
              for h, c in ((1.8, PRUNE), (1.35, PRUNE), (.95, ACCENT), (.5, GOOD))]
        ).arrange(RIGHT, aligned_edge=DOWN, buff=.14).move_to([0, -2.65, 0])
        self.show(VGroup(plane, path, point, loss))
        self.play(MoveAlongPath(point, path), run_time=1.7, rate_func=smooth)
        self.to(65)

        # 65–76: sweep d while performance approaches the baseline.
        self.copy(
            "부분공간의 차원 d를 늘려봅니다", "10 → 50 → 100 → 500 → 1000",
            "d를 10, 50, 100, 500, 1000으로 늘리면\n어느 순간 원래 성능의 기준선에 도달합니다.",
        )
        graph = self.performance_graph()
        values = VGroup(*[
            card(str(v), ACCENT if v == 500 else MUTED, 1.15, .62, 18,
                 .18 if v == 500 else .06)
            for v in (10, 50, 100, 500, 1000)
        ]).arrange(RIGHT, buff=.18).move_to([0, -2.75, 0])
        self.show(VGroup(graph, values))
        self.to(76)

        # 76–86: name the operational measurement and its dependencies.
        self.copy(
            "여기서 Intrinsic Dimension을 측정합니다", "MINIMUM d TO REACH THE TARGET",
            "기준에 도달하는 최소 차원으로 Intrinsic Dimension을 측정합니다.\n이는 조건에 따라 달라지는 실험적 측정값입니다.",
        )
        target = card("target performance", GOOD, 5.2, .85, 24).move_to([0, 2.0, 0])
        down = Arrow([0, 1.45, 0], [0, .55, 0], buff=0, color=MUTED,
                     stroke_width=3, tip_length=.18)
        result = card("d*  =  smallest successful d", ACCENT, 6.2, 1.05, 27, .18)
        result.move_to([0, -.15, 0])
        deps = VGroup(*[
            card(v, c, 1.7, .62, 17, .07)
            for v, c in (("model", WEIGHT), ("data", SPARSE),
                         ("optimizer", PRUNE), ("criterion", GOOD))
        ]).arrange(RIGHT, buff=.15).move_to([0, -2.0, 0])
        self.show(VGroup(target, down, result, deps))
        self.to(86)

        # 86–96: random subspaces should miss an isolated solution.
        self.copy(
            "좋은 해가 한 점뿐이라면?", "RANDOM SLICES SHOULD MISS",
            "좋은 해가 특별한 한 점이라면 무작위 부분공간이\n그 근처를 지날 가능성은 매우 낮아야 합니다.",
        )
        solution = Dot([.55, .45, 0], radius=.16, color=GOOD)
        halo = Circle(radius=.42, color=GOOD, stroke_opacity=.3).move_to(solution)
        slices = VGroup(*[
            Polygon([-3.3, y - .45, 0], [3.3, y + .2, 0], [3.3, y + .65, 0],
                    [-3.3, y, 0], color=c, fill_color=c, fill_opacity=.08,
                    stroke_opacity=.65)
            for y, c in ((-2.0, SPARSE), (-.9, WEIGHT), (1.45, PRUNE))
        ])
        point_tag = label("isolated solution", 20, GOOD).next_to(solution, RIGHT, buff=.25)
        self.show(VGroup(slices, solution, halo, point_tag))
        self.to(96)

        # 96–104: transform the simplistic point into possible rich geometry.
        self.copy(
            "해의 기하는 한 점보다 풍부할 수 있습니다", "A CLUE, NOT A FLAT-PLANE CLAIM",
            "좋은 해의 기하는 한 점보다 풍부할 수 있고,\n필요한 자유도는 파라미터 수보다 작을 수 있습니다.",
        )
        dot = Dot([-2.6, .3, 0], radius=.14, color=GOOD)
        arrow1 = Arrow([-2.15, .3, 0], [-1.25, .3, 0], buff=0, color=MUTED,
                       stroke_width=2, tip_length=.15)
        curve = VMobject(color=GOOD, stroke_width=8)
        curve.set_points_smoothly([[-.9, -.2, 0], [-.3, .75, 0], [.45, -.4, 0], [1.1, .55, 0]])
        arrow2 = Arrow([1.45, .3, 0], [2.05, .3, 0], buff=0, color=MUTED,
                       stroke_width=2, tip_length=.15)
        region = Ellipse(width=1.5, height=2.2, color=ACCENT,
                         fill_color=GOOD, fill_opacity=.15).rotate(-.35).move_to([2.75, .3, 0])
        caveat = label("possible solution geometry", 21, ACCENT).move_to([0, -2.1, 0])
        self.show(VGroup(dot, arrow1, curve, arrow2, region, caveat))
        self.to(104)

        # 104–112: reverse the question and open the rest of the series.
        self.copy(
            "그러면 질문은 뒤집힙니다", "WHY SO MANY PARAMETERS?",
            "큰 공간은 복잡한 답을 표현하기 위해서만일까요?\n아니면 답을 찾기 쉽게 만들기 위해서일까요?",
        )
        question = label(
            "복잡한 답을 표현하기 위해서?\n\n답을 찾기 쉽게 만들기 위해서?",
            31, INK, 7.0,
        ).move_to([0, .75, 0])
        finale = card(
            "Large Parameter Space\n≠\nEqually Large Intrinsic Dimension",
            ACCENT, 7.1, 2.2, 25, .15,
        ).move_to([0, -2.0, 0])
        self.show(VGroup(question, finale))
        self.to(112)

    def parameter_space(self):
        cloud = VGroup()
        for i in range(48):
            angle = i * 2.39996
            radius = .48 * np.sqrt(i + 1)
            x = radius * np.cos(angle)
            y = .78 * radius * np.sin(angle) + .2
            cloud.add(Dot([x, y, 0], radius=.025 + .015 * (i % 3),
                          color=MUTED, fill_opacity=.16 + .06 * (i % 4)))
        axes = self.radial_axes(16)
        frame = Ellipse(width=7.1, height=5.1, color=MUTED,
                        stroke_opacity=.3).move_to([0, .2, 0])
        return VGroup(frame, cloud, axes)

    def radial_axes(self, count):
        axes = VGroup()
        for i in range(count):
            angle = TAU * i / count
            extent = 2.6 + .55 * (i % 3)
            end = np.array([extent * np.cos(angle), .72 * extent * np.sin(angle), 0])
            axes.add(Line(ORIGIN, end, color=MUTED, stroke_width=1.3,
                          stroke_opacity=.32))
        axes.move_to([0, .25, 0])
        return axes

    def compare_row(self, title, left_value, right_value, color):
        name = label(title, 17, MUTED).move_to([0, .72, 0])
        left = card(left_value, MUTED, 2.55, .85, 23).move_to([-1.9, 0, 0])
        right = card(right_value, color, 2.55, .85, 23, .16).move_to([1.9, 0, 0])
        arrow = Arrow(left.get_right(), right.get_left(), buff=.16,
                      color=color, stroke_width=3, tip_length=.17)
        body = VGroup(left, arrow, right)
        return VGroup(name, body).arrange(DOWN, buff=.22)

    def performance_graph(self):
        x_axis = Arrow([-3.15, -2.0, 0], [3.35, -2.0, 0], buff=0,
                       color=MUTED, stroke_width=2, tip_length=.14)
        y_axis = Arrow([-3.15, -2.0, 0], [-3.15, 2.75, 0], buff=0,
                       color=MUTED, stroke_width=2, tip_length=.14)
        baseline = DashedLine([-3.0, 1.75, 0], [3.0, 1.75, 0],
                              color=GOOD, dash_length=.16)
        curve = VMobject(color=ACCENT, stroke_width=5)
        points = [[-2.75, -1.55, 0], [-1.85, -1.15, 0], [-.95, -.1, 0],
                  [.15, 1.0, 0], [1.15, 1.62, 0], [2.7, 1.78, 0]]
        curve.set_points_smoothly(points)
        dots = VGroup(*[Dot(p, radius=.075, color=ACCENT) for p in points])
        target = label("original-performance criterion", 18, GOOD).move_to([.65, 2.1, 0])
        labels = VGroup(
            label("d →", 18, MUTED).move_to([3.2, -2.35, 0]),
            label("performance", 17, MUTED).move_to([-3.15, 3.03, 0]),
        )
        return VGroup(x_axis, y_axis, baseline, curve, dots, target, labels)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
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
