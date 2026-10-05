"""Neural Network Mathematics Part 2, episode 06: Grokking."""
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
    obj = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    pts = [np.array(point, dtype=float) for point in points]
    if smooth:
        obj.set_points_smoothly(pts)
    else:
        obj.set_points_as_corners(pts)
    return obj


class NeuralMathPart2Grokking(Scene):
    DURATION = 126

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 06", 17, MUTED).move_to(UP * 7.3),
            label("훈련 정확도 100% 이후에도 모델은 무엇을 배울까?", 27).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        # 1 — The apparent finish line.
        self.copy(
            "훈련 데이터를 전부 맞혔습니다", "TRAIN ACCURACY = 100%",
            "모든 훈련 예제의 정답을 맞혔다면\n학습은 이미 끝난 것처럼 보입니다.",
        )
        examples = VGroup(*[
            card(f"sample {i + 1}   ✓", GOOD, 2.9, .7, 20, .12)
            for i in range(6)
        ]).arrange_in_grid(rows=3, cols=2, buff=.32).move_to([0, .35, 0])
        self.show(VGroup(examples,
                         card("100% correct", GOOD, 4.1, .8, 27, .16).move_to([0, -2.65, 0])))
        self.to(10.0)

        # 2 — The standard overfitting expectation.
        self.copy(
            "보통은 여기서 과적합을 걱정합니다", "KEEP TRAINING?",
            "이미 외웠는데 계속 학습하면\n새 데이터 성능은 더 나빠질 것 같습니다.",
        )
        stop = card("STOP", PRUNE, 2.2, 1.0, 31, .16).move_to([-2.15, .45, 0])
        continue_card = card("CONTINUE", SPARSE, 2.9, 1.0, 27, .14).move_to([2.15, .45, 0])
        down = VGroup(
            Arrow(continue_card.get_bottom(), [2.15, -1.25, 0], buff=.12,
                  color=PRUNE, stroke_width=4, tip_length=.18),
            label("test performance?", 21, PRUNE).move_to([2.15, -1.75, 0]),
        )
        self.show(VGroup(stop, continue_card, down,
                         card("Expected: overfitting ↑", PRUNE, 4.9, .76, 23, .13)
                         .move_to([0, -2.75, 0])))
        self.to(16.0)

        # 3 — The central delayed-generalization curve.
        self.copy(
            "그런데 훨씬 나중에 Test가 올라갑니다", "DELAYED GENERALIZATION",
            "Train은 일찍 100%가 되고 Test는 오래 낮습니다.\n그러다 뒤늦게 빠르게 상승합니다.",
        )
        chart = self.grokking_chart()
        self.show(chart)
        cursor = Dot([-2.25, .95, 0], radius=.11, color=ACCENT)
        path = route([[-2.25, .95, 0], [.75, .95, 0], [1.35, 1.4, 0], [2.35, 2.0, 0]],
                     ACCENT, 3, .25, True)
        self.add_stage(cursor)
        self.play(MoveAlongPath(cursor, path), run_time=1.35)
        self.to(22.5)

        # 4 — Name the phenomenon, but keep the wording careful.
        self.copy(
            "이 지연된 전환을 Grokking이라 부릅니다", "GROKKING",
            "특정한 학습 환경에서 오래된 memorization 뒤\ngeneralization이 급격히 좋아지는 현상입니다.",
        )
        memorization_card = card("Memorization", PRUNE, 2.8, .9, 25, .15).move_to([-2.3, .55, 0])
        generalization_card = card("Generalization", GOOD, 3.1, .9, 24, .15).move_to([2.3, .55, 0])
        timeline = VGroup(memorization_card, generalization_card,
                          label("long training", 20, MUTED).move_to([0, -.35, 0]))
        arrow = Arrow(memorization_card.get_right(), generalization_card.get_left(), buff=.12,
                      color=ACCENT, stroke_width=4, tip_length=.18)
        self.show(VGroup(timeline, arrow,
                         card("late behavioral transition", ACCENT, 5.3, .78, 23, .14)
                         .move_to([0, -2.6, 0])))
        self.to(29.5)

        # 5 — Modular arithmetic as the canonical toy task.
        self.copy(
            "대표적인 장난감 문제는 모듈러 연산입니다", "a + b  mod  p",
            "가능한 입력 조합 일부만 보여주고\n나머지는 Test로 남겨둡니다.",
        )
        a = self.number_token("5", WEIGHT).move_to([-2.8, .75, 0])
        b = self.number_token("4", SPARSE).move_to([-2.8, -.65, 0])
        gate = card("+  mod 7", ACCENT, 2.3, 1.35, 27, .15).move_to([0, .05, 0])
        result = self.number_token("2", GOOD).move_to([2.75, .05, 0])
        path_a = route([a.get_right(), [-1.25, .75, 0], gate.get_left()], WEIGHT, 3)
        path_b = route([b.get_right(), [-1.25, -.65, 0], gate.get_left()], SPARSE, 3)
        path_out = route([gate.get_right(), result.get_left()], GOOD, 3)
        self.show(VGroup(path_a, path_b, path_out, a, b, gate, result,
                         label("5 + 4 = 2  (mod 7)", 27, ACCENT).move_to([0, -2.65, 0])))
        moving_a, moving_b = a.copy(), b.copy()
        self.add_stage(moving_a, moving_b)
        self.play(MoveAlongPath(moving_a, path_a), MoveAlongPath(moving_b, path_b), run_time=.9)
        self.play(FadeOut(moving_a), FadeOut(moving_b), run_time=.15)
        self.to(37.0)

        # 6 — Memorized examples versus unseen combinations.
        self.copy(
            "처음에는 예제를 개별적으로 외울 수 있습니다", "TRAIN ✓  ·  UNSEEN ?",
            "훈련에 나온 조합은 전부 맞히지만\n처음 보는 조합에는 규칙을 적용하지 못합니다.",
        )
        train = self.example_panel("TRAIN · mod 7", (("1+2", "3"), ("5+4", "9→2"), ("3+6", "9→2")), GOOD)
        train.move_to([-2.05, .3, 0])
        test = self.example_panel("UNSEEN", (("2+6", "?"), ("4+4", "?"), ("6+6", "?")), PRUNE)
        test.move_to([2.05, .3, 0])
        self.show(VGroup(train, test,
                         card("memorized examples  ≠  learned rule", ACCENT, 6.5, .78, 22, .14)
                         .move_to([0, -2.8, 0])))
        self.to(44.0)

        # 7 — Training continues across a long plateau.
        self.copy(
            "정확도 100% 이후에도 Loss는 낮아집니다", "THOUSANDS OF MORE STEPS",
            "Train Accuracy가 100%이고 Loss가 계속 낮아지는 동안에도\noptimizer는 오랫동안 parameter를 바꿀 수 있습니다.",
        )
        start = card("Train fit", GOOD, 2.2, .82, 23, .14).move_to([-3.0, .45, 0])
        end = card("Test jump", ACCENT, 2.35, .82, 23, .14).move_to([3.0, .45, 0])
        long_line = Line(start.get_right(), end.get_left(), color=MUTED, stroke_width=4)
        ticks = VGroup(*[
            Line([x, .27, 0], [x, .63, 0], color=MUTED, stroke_opacity=.45)
            for x in np.linspace(-1.65, 1.65, 9)
        ])
        token = Dot(start.get_right(), radius=.12, color=ACCENT)
        self.show(VGroup(start, end, long_line, ticks,
                         label("long plateau", 23, MUTED).move_to([0, -1.0, 0]),
                         card("optimization continues", SPARSE, 4.7, .75, 22, .12)
                         .move_to([0, -2.65, 0])))
        self.add_stage(token)
        self.play(token.animate.move_to(end.get_left()), run_time=1.4, rate_func=linear)
        self.to(52.0)

        # 8 — Accuracy is not a stopping certificate.
        self.copy(
            "정확도 100%는 정지 조건이 아닙니다", "ACCURACY ≠ ZERO GRADIENT",
            "정확도는 argmax가 맞는지만 봅니다.\nLoss와 parameter update는 계속 달라질 수 있습니다.",
        )
        accuracy = card("Train Accuracy", WEIGHT, 3.05, .82, 22, .12).move_to([-2.15, .6, 0])
        value = card("100%", GOOD, 2.0, .82, 28, .16).move_to([-2.15, -.65, 0])
        gradient = card("∇θ L", PRUNE, 2.0, .82, 29, .14).move_to([2.15, .6, 0])
        nonzero = card("≠ 0", ACCENT, 2.0, .82, 29, .14).move_to([2.15, -.65, 0])
        self.show(VGroup(accuracy, value, gradient, nonzero,
                         label("same accuracy · different optimization state", 21, MUTED)
                         .move_to([0, -2.55, 0])))
        self.to(59.5)

        # 9 — Same classification, different confidence and loss.
        self.copy(
            "같은 정답이어도 Loss는 다릅니다", "P(y)=0.6  vs  P(y)=0.999",
            "둘 다 분류는 맞지만 정답 확률과 loss가 다릅니다.\n따라서 학습 신호가 남아 있습니다.",
        )
        left = self.confidence_panel("CORRECT", .6, WEIGHT, "higher loss").move_to([-2.05, .25, 0])
        right = self.confidence_panel("CORRECT", .999, GOOD, "lower loss").move_to([2.05, .25, 0])
        self.show(VGroup(left, right,
                         card("accuracy is already tied", ACCENT, 4.9, .75, 22, .13)
                         .move_to([0, -2.75, 0])))
        self.to(66.5)

        # 10 — Two ways to fit all training points.
        self.copy(
            "훈련점을 맞히는 방식은 하나가 아닙니다", "TWO SOLUTIONS · SAME TRAIN ACCURACY",
            "개별 예제를 외우는 것에 가까운 해와\n더 일반화되는 규칙적 해 모두 훈련점을 맞힐 수 있습니다.",
        )
        memorization = self.solution_panel("MEMORIZATION", PRUNE, jagged=True).move_to([-2.05, .25, 0])
        generalization = self.solution_panel("GENERALIZATION", GOOD, jagged=False).move_to([2.05, .25, 0])
        self.show(VGroup(memorization, generalization,
                         card("Train Accuracy = 100%  ·  both", ACCENT, 6.3, .82, 23, .16)
                         .move_to([0, -2.8, 0])))
        self.to(77.0)

        # 11 — Optimization may move between fitting solutions.
        self.copy(
            "정답을 찾은 뒤에도 표현 방식은 바뀔 수 있습니다", "SAME TRAIN FIT · DIFFERENT DYNAMICS",
            "같은 훈련 데이터를 만족한 채\nparameter와 내부 표현은 다른 방식으로 계속 바뀔 수 있습니다.",
        )
        mem = card("memorizing solution", PRUNE, 3.1, .92, 22, .14).move_to([-2.45, .5, 0])
        gen = card("generalizing solution", GOOD, 3.25, .92, 21, .14).move_to([2.45, .5, 0])
        curve = route([mem.get_right(), [-.8, 1.45, 0], [.4, -1.0, 0], gen.get_left()],
                      ACCENT, 4, .7, True)
        token = Dot(mem.get_right(), radius=.14, color=ACCENT)
        self.show(VGroup(mem, gen, curve,
                         label("Train Accuracy stays high", 23, GOOD).move_to([0, -2.15, 0])))
        self.add_stage(token)
        self.play(MoveAlongPath(token, curve), run_time=1.35)
        self.to(84.0)

        # 12 — Sudden behavior can hide gradual internal change.
        self.copy(
            "겉의 급변이 내부의 급변을 뜻하지는 않습니다", "BEHAVIOR  /  REPRESENTATION",
            "Test accuracy는 갑자기 뛰어도\n내부 구조는 훨씬 전부터 점진적으로 변할 수 있습니다.",
        )
        behavior = self.mini_timeline("TEST ACCURACY", abrupt=True, color=ACCENT).move_to([0, 1.35, 0])
        internal = self.mini_timeline("INTERNAL STRUCTURE", abrupt=False, color=SPARSE).move_to([0, -1.25, 0])
        self.show(VGroup(behavior, internal,
                         card("Sudden output  ≠  sudden learning", PRUNE, 5.8, .72, 22, .13)
                         .move_to([0, -3.0, 0])))
        self.to(92.0)

        # 13 — Competing solutions under optimization and regularization.
        self.copy(
            "두 종류의 해가 경쟁한다고 볼 수 있습니다", "OPTIMIZATION  +  REGULARIZATION",
            "일부 설정에서는 장기 dynamics와 weight decay가\n더 일반화되는 해를 선호할 수 있습니다.",
        )
        root = card("fits training data", WEIGHT, 3.8, .86, 24, .13).move_to([0, 1.85, 0])
        mem = card("memorizing", PRUNE, 2.7, .86, 23, .13).move_to([-2.0, -.45, 0])
        rule = card("rule-like", GOOD, 2.7, .86, 23, .13).move_to([2.0, -.45, 0])
        arrows = VGroup(
            Arrow(root.get_bottom(), mem.get_top(), buff=.12, color=PRUNE, tip_length=.16),
            Arrow(root.get_bottom(), rule.get_top(), buff=.12, color=GOOD, tip_length=.16),
        )
        self.show(VGroup(root, mem, rule, arrows,
                         label("possible interpretation · setting dependent", 20, MUTED)
                         .move_to([0, -2.55, 0])))
        self.to(100.0)

        # 14 — Connect to representable versus reachable.
        self.copy(
            "좋은 해의 존재와 도달 시점은 다릅니다", "REPRESENTABLE  ≠  REACHED YET",
            "일반화하는 해가 존재해도 optimizer가 곧바로 도달하진 않습니다.\n외운 것처럼 보이는 행동이 오래 나타날 수 있습니다.",
        )
        space = RoundedRectangle(width=6.9, height=3.6, corner_radius=.25,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.035)
        start = Dot([-2.5, -.65, 0], radius=.14, color=PRUNE)
        goal = Dot([2.5, .9, 0], radius=.17, color=GOOD)
        path = route([start.get_center(), [-1.2, 1.0, 0], [.3, -.7, 0], [1.35, .2, 0], goal.get_center()],
                     ACCENT, 4, .65, True)
        self.show(VGroup(space, path, start, goal,
                         label("memorization behavior", 19, PRUNE).next_to(start, DOWN, buff=.2),
                         label("generalizing behavior", 19, GOOD).next_to(goal, UP, buff=.2)))
        mover = start.copy()
        self.add_stage(mover)
        self.play(MoveAlongPath(mover, path), run_time=1.35)
        self.to(110.5)

        # 15 — Grokking is not a universal promise.
        self.copy(
            "오래 학습하면 언제나 이해할까요?", "NO UNIVERSAL GUARANTEE",
            "Grokking은 모든 모델의 필연이 아닙니다.\n데이터와 optimizer, regularization에 따라 달라집니다.",
        )
        claim = card("Train longer  =  discover true rule", PRUNE, 6.8, 1.0, 24, .14)
        claim_box = claim[0]
        cross = VGroup(
            Line(claim_box.get_corner(DL) + np.array([.18, .12, 0]),
                 claim_box.get_corner(UR) + np.array([-.18, -.12, 0]),
                 color=PRUNE, stroke_width=6),
            Line(claim_box.get_corner(UL) + np.array([.18, -.12, 0]),
                 claim_box.get_corner(DR) + np.array([-.18, .12, 0]),
                 color=PRUNE, stroke_width=6),
        )
        conditions = label("data · model · optimizer · regularization · training regime", 20, MUTED)
        conditions.move_to([0, -1.75, 0])
        self.show(VGroup(claim, cross, conditions,
                         card("observed in particular settings", ACCENT, 5.6, .72, 21, .12)
                         .move_to([0, -2.8, 0])))
        self.to(117.5)

        # 16 — Durable conclusion.
        self.copy(
            "정답을 맞힌 것과 학습이 끝난 것은 다릅니다", "AFTER 100% ACCURACY",
            "모델은 같은 훈련 답을 유지하면서도\n그 답을 구현하는 방식을 계속 바꿀 수 있습니다.",
        )
        top = card("All training answers correct", GOOD, 5.8, .92, 25, .15).move_to([0, 1.75, 0])
        middle = label("↓  learning dynamics continue  ↓", 25, ACCENT).move_to([0, .2, 0])
        bottom = card("A different way to implement the answer", SPARSE, 6.9, 1.0, 23, .15)
        bottom.move_to([0, -1.5, 0])
        self.show(VGroup(top, middle, bottom,
                         label("Accuracy saturation  ≠  learning completion", 24, PRUNE)
                         .move_to([0, -3.0, 0])))
        self.to(126.0)

    def number_token(self, value, color):
        circle = Circle(radius=.42, color=color, stroke_width=3,
                        fill_color=BG, fill_opacity=1)
        return VGroup(circle, label(value, 27, color).move_to(circle))

    def grokking_chart(self):
        x_axis = Arrow([-3.2, -1.8, 0], [3.25, -1.8, 0], buff=0,
                       color=MUTED, stroke_width=2.5, tip_length=.15)
        y_axis = Arrow([-3.2, -1.8, 0], [-3.2, 2.45, 0], buff=0,
                       color=MUTED, stroke_width=2.5, tip_length=.15)
        train = VGroup(
            CubicBezier([-3.05, -1.45, 0], [-2.9, -1.1, 0], [-2.55, 1.85, 0], [-2.1, 1.95, 0],
                        color=GOOD, stroke_width=5),
            Line([-2.1, 1.95, 0], [3.0, 1.95, 0], color=GOOD, stroke_width=5),
        )
        test = VGroup(
            CubicBezier([-3.05, -1.4, 0], [-2.45, -1.18, 0], [-.1, -1.1, 0], [.65, -1.05, 0],
                        color=PRUNE, stroke_width=5),
            CubicBezier([.65, -1.05, 0], [1.15, -1.02, 0], [1.35, 1.82, 0], [2.15, 1.9, 0],
                        color=PRUNE, stroke_width=5),
            Line([2.15, 1.9, 0], [3.0, 1.95, 0], color=PRUNE, stroke_width=5),
        )
        plateau = DashedLine([-2.05, -1.75, 0], [-2.05, 2.2, 0],
                             color=ACCENT, dash_length=.13, stroke_opacity=.55)
        return VGroup(x_axis, y_axis, train, test, plateau,
                      label("Train", 20, GOOD).move_to([2.7, 2.3, 0]),
                      label("Test", 20, PRUNE).move_to([2.65, 1.45, 0]),
                      label("training steps", 18, MUTED).move_to([1.9, -2.25, 0]),
                      label("accuracy", 18, MUTED).rotate(PI / 2).move_to([-3.65, .45, 0]))

    def example_panel(self, title, pairs, color):
        box = RoundedRectangle(width=3.55, height=4.25, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04, stroke_width=2.5)
        rows = VGroup(*[
            VGroup(card(inp, color, 1.35, .62, 18, .1), label("→", 21, MUTED),
                   card(out, color, 1.15, .62, 18, .1)).arrange(RIGHT, buff=.12)
            for inp, out in pairs
        ]).arrange(DOWN, buff=.35).move_to([0, -.1, 0])
        return VGroup(box, label(title, 23, color).move_to([0, 1.65, 0]), rows)

    def confidence_panel(self, title, value, color, subtitle):
        box = RoundedRectangle(width=3.55, height=4.15, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04, stroke_width=2.5)
        track = RoundedRectangle(width=2.75, height=.5, corner_radius=.12,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.16)
        fill = RoundedRectangle(width=max(.12, 2.47 * value), height=.3,
                                corner_radius=.08, stroke_width=0,
                                fill_color=color, fill_opacity=.9)
        fill.align_to(track, LEFT).shift(RIGHT * .14)
        meter = VGroup(track, fill).move_to([0, .25, 0])
        return VGroup(box, label(title, 22, color).move_to([0, 1.55, 0]), meter,
                      label(f"P(y) = {value}", 26, color).move_to([0, -.65, 0]),
                      label(subtitle, 20, MUTED).move_to([0, -1.5, 0]))

    def solution_panel(self, title, color, jagged):
        box = RoundedRectangle(width=3.55, height=4.3, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04, stroke_width=2.5)
        xs = np.linspace(-1.25, 1.25, 5)
        ys = .32 * xs
        dots = VGroup(*[Dot([x, y, 0], radius=.085, color=WEIGHT) for x, y in zip(xs, ys)])
        if jagged:
            points = []
            for i, (x, y) in enumerate(zip(xs, ys)):
                points.append([x, y, 0])
                if i < len(xs) - 1:
                    points.append([(x + xs[i + 1]) / 2,
                                   (y + ys[i + 1]) / 2 + (.5 if i % 2 else -.5), 0])
            curve = route(points, color, 4, 1, True)
        else:
            curve = Line([-1.4, -.45, 0], [1.4, .45, 0], color=color, stroke_width=4)
        graph = VGroup(curve, dots).move_to([0, -.1, 0])
        return VGroup(box, label(title, 20, color).move_to([0, 1.65, 0]), graph,
                      label("fits all train points", 18, GOOD).move_to([0, -1.55, 0]))

    def mini_timeline(self, title, abrupt, color):
        box = RoundedRectangle(width=6.8, height=1.8, corner_radius=.2,
                               color=color, fill_color=color, fill_opacity=.035, stroke_width=2)
        axis = Line([-2.65, -.35, 0], [2.75, -.35, 0], color=MUTED, stroke_width=2)
        if abrupt:
            curve = VGroup(
                Line([-2.55, -.15, 0], [.65, -.15, 0], color=color, stroke_width=4),
                CubicBezier([.65, -.15, 0], [1.0, -.14, 0], [1.05, .56, 0], [1.45, .58, 0],
                            color=color, stroke_width=4),
                Line([1.45, .58, 0], [2.55, .58, 0], color=color, stroke_width=4),
            )
        else:
            curve = CubicBezier([-2.55, -.1, 0], [-1.4, -.02, 0], [.75, .48, 0], [2.55, .58, 0],
                                color=color, stroke_width=4)
        return VGroup(box, label(title, 19, color).move_to([-2.2, .58, 0]), axis, curve)

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
            self.remove(self.stage)
        self.stage = new_stage
        self.add(self.stage)
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def add_stage(self, *objects):
        self.stage.add(*objects)

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
