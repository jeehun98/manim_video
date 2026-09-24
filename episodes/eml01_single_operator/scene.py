"""EML 01: reduce a calculator to one primitive, then recover exp."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.eml_series.visuals import (
    BLUE, GOLD, GREEN, INK, MUTED, PINK,
    EMLNode, ExpressionTree, OperatorChip, input_arrow, txt,
)


class EMLSingleOperator(Scene):
    DURATION = 50

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.stage = VGroup()
        self.add(
            txt("ONE PRIMITIVE  /  EML 01", 20, MUTED).move_to(UP * 7.25),
            txt("과학용 계산기의 연산자를 하나만 남긴다면?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–5 s: the familiar calculator vocabulary.
        self.text(
            "계산기는 많은 연산자를 사용합니다",
            "우리가 계산할 때는 덧셈, 곱셈, 로그, 지수함수처럼\n수많은 연산자를 사용합니다.",
            "각 기호가 서로 다른 계산 규칙",
        )
        symbols = ["+", "−", "×", "÷", "√x", "eˣ", "ln x", "sin x", "cos x"]
        colors = [BLUE, PINK, GOLD, GREEN, BLUE, GOLD, PINK, GREEN, BLUE]
        self.chips = VGroup(*[OperatorChip(s, c) for s, c in zip(symbols, colors)])
        self.chips.arrange_in_grid(rows=3, cols=3, buff=(.35, .45)).move_to(UP * .45)
        self.stage = self.chips
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .18) for c in self.chips],
                              lag_ratio=.08), run_time=1.4)
        self.play(LaggedStart(*[Indicate(c, color=colors[i], scale_factor=1.05)
                                for i, c in enumerate(self.chips)], lag_ratio=.08), run_time=1.6)
        self.to(5)

        # 5–11 s: many operator kinds imply many rules and dispatch paths.
        self.text(
            "종류가 늘면, 구분할 것도 늘어납니다",
            "연산 종류가 다양할수록 시스템은 각각의 규칙을 구현하고,\n어떤 계산 경로로 보낼지도 구분해야 합니다.",
            "연산 규칙 구현     ·     계산 경로 선택",
        )
        path_rows = VGroup()
        for i, (symbol, color) in enumerate(zip(["+", "×", "eˣ", "ln", "sin"],
                                                [BLUE, GOLD, GREEN, PINK, BLUE])):
            y = 2.5 - i * 1.15
            chip = OperatorChip(symbol, color, width=1.0, height=.62).move_to([-3.0, y, 0])
            route = Arrow([-2.35, y, 0], [-1.25, y, 0], buff=.05, color=color,
                          stroke_width=2.5, tip_length=.13)
            rule = RoundedRectangle(width=3.5, height=.7, corner_radius=.1,
                                    stroke_color=color, stroke_width=1.4,
                                    fill_color=color, fill_opacity=.05).move_to([.75, y, 0])
            label = txt(f"{symbol} 전용 규칙 · 경로", 21, color, 3.1).move_to(rule)
            path_rows.add(VGroup(chip, route, rule, label))
        self.play(FadeOut(self.chips), LaggedStart(*[FadeIn(r, shift=RIGHT * .15)
                                                     for r in path_rows], lag_ratio=.1), run_time=1.2)
        self.stage = path_rows
        self.play(LaggedStart(*[Indicate(r, scale_factor=1.02) for r in path_rows],
                              lag_ratio=.12), run_time=1.5)
        self.to(11)

        # 11–17 s: one primitive gives a uniform expression vocabulary.
        self.text(
            "primitive가 적다면",
            "더 적은 primitive로 같은 계산을 표현하면,\n표현 규칙과 연산 그래프를 통일할 수 있습니다.",
            "작은 연산 집합     ·     반복 가능한 graph node",
        )
        primitive = OperatorChip("primitive", GOLD, width=2.5, height=1.0).move_to([-2.15, .55, 0])
        p_nodes = VGroup(*[OperatorChip("P", GOLD, width=1.0, height=.62)
                           for _ in range(3)])
        p_nodes[0].move_to([2.0, 1.55, 0])
        p_nodes[1].move_to([1.25, -.1, 0])
        p_nodes[2].move_to([2.75, -.1, 0])
        p_edges = VGroup(
            Line(p_nodes[1].get_top(), p_nodes[0].get_bottom() + LEFT * .2,
                 color=BLUE, stroke_width=2),
            Line(p_nodes[2].get_top(), p_nodes[0].get_bottom() + RIGHT * .2,
                 color=PINK, stroke_width=2),
        )
        uniform = VGroup(
            primitive,
            Arrow([-.65, .55, 0], [.55, .55, 0], buff=.05, color=GOLD,
                  stroke_width=3, tip_length=.15),
            p_edges, p_nodes,
            txt("하나의 규칙", 23, GOLD).move_to([-2.15, -.45, 0]),
            txt("같은 node의 반복", 23, GOLD).move_to([2.0, -1.0, 0]),
        )
        self.play(FadeOut(path_rows), FadeIn(uniform), run_time=.75)
        self.stage = uniform
        self.play(LaggedStart(*[Indicate(n, color=GOLD, scale_factor=1.06)
                                for n in p_nodes], lag_ratio=.25), run_time=1.4)
        self.to(17)

        # 17–21 s: explicitly separate representation from execution speed.
        self.text(
            "하지만 서로 다른 문제입니다",
            "표현이 단순해지는 것과 실제 계산량이나\n실행 시간이 줄어드는 것은 같은 말이 아닙니다.",
            "표현 가능성  ≠  실제 실행 효율",
        )
        distinction = VGroup(
            OperatorChip("표현 구조", BLUE, width=2.55, height=1.05).move_to([-2.25, .55, 0]),
            txt("≠", 46, PINK).move_to([0, .55, 0]),
            OperatorChip("실행 효율", GREEN, width=2.55, height=1.05).move_to([2.25, .55, 0]),
            txt("연산량 · 메모리 이동 · 하드웨어", 24, MUTED).move_to([0, -1.0, 0]),
        )
        self.play(FadeOut(uniform), FadeIn(distinction), run_time=.7)
        self.stage = distinction
        self.play(Indicate(distinction[1], color=PINK, scale_factor=1.25), run_time=.7)
        self.to(21)

        # 21–27 s: the paper's constructive single-operator result.
        self.text(
            "그렇다면 어디까지 줄일 수 있을까?",
            "한 논문은 EML 하나와 상수 1만으로\n계산기의 기본 연산들을 표현할 수 있음을 보였습니다.",
            "one operator  +  constant 1",
        )
        self.eml = EMLNode().move_to([0, .7, 0])
        one = self.leaf("1", GREEN).move_to([0, -1.25, 0])
        orbit = VGroup(*[OperatorChip(s, c, width=1.05, height=.65)
                         for s, c in zip(["+", "×", "eˣ", "ln", "sin", "√x"],
                                         [BLUE, GOLD, GREEN, PINK, BLUE, GREEN])])
        for chip, point in zip(orbit, [[-3, 2.3, 0], [0, 3.0, 0], [3, 2.3, 0],
                                       [-3, -1.9, 0], [0, -2.8, 0], [3, -1.9, 0]]):
            chip.move_to(point).set_opacity(.32)
        claim = VGroup(self.eml, one, orbit,
                       Arrow(one.get_top(), self.eml.right_anchor(), buff=.08,
                             color=GREEN, stroke_width=2.5, tip_length=.14))
        self.play(FadeOut(distinction), FadeIn(claim), run_time=.75)
        self.stage = claim
        self.play(LaggedStart(*[chip.animate.set_opacity(.75) for chip in orbit],
                              lag_ratio=.1), run_time=1.2)
        self.play(Circumscribe(self.eml, color=GOLD, buff=.15), run_time=.8)
        self.to(27)

        # 27–33 s: open the node and show its two internal paths.
        self.text(
            "EML은 두 입력을 받습니다",
            "EML은 e의 x승에서 y의 로그를 빼는\n하나의 이항 연산자입니다.",
            "EML(x, y) = eˣ − ln y",
        )
        self.flow = self.make_flow("y")
        self.play(FadeOut(claim), FadeIn(self.flow), run_time=.65)
        self.stage = self.flow
        self.play(Indicate(self.flow.exp_path, color=BLUE, scale_factor=1.03), run_time=.75)
        self.play(Indicate(self.flow.log_path, color=PINK, scale_factor=1.03), run_time=.75)
        self.to(33)

        # 33–39 s: substitute the only distinguished constant.
        self.text(
            "두 번째 입력에 1을 넣으면",
            "두 번째 입력에 상수 1을 넣어보겠습니다.",
            "EML(x, 1) = eˣ − ln 1",
        )
        new_y = self.leaf("1", GREEN).move_to(self.flow.y_leaf)
        new_log = txt("ln 1", 31, GREEN).move_to(self.flow.log_value)
        self.play(Transform(self.flow.y_leaf, new_y),
                  Transform(self.flow.log_value, new_log), run_time=1.0)
        self.play(Indicate(VGroup(self.flow.y_leaf, self.flow.log_value),
                           color=GREEN, scale_factor=1.12), run_time=.9)
        self.to(39)

        # 39–44 s: ln(1) vanishes.
        self.text(
            "가장 얕은 EML tree",
            "ln 1은 0이므로, 이 한 개의 EML 노드는\n지수함수와 같은 계산을 표현합니다.",
            "EML(x, 1) = eˣ − 0 = eˣ",
        )
        zero = txt("0", 38, GREEN).move_to(self.flow.log_value)
        simplified = txt("eˣ", 46, GOLD).move_to(self.flow.result)
        self.play(Transform(self.flow.log_value, zero),
                  self.flow.log_arrow.animate.set_opacity(.25), run_time=.7)
        self.play(Transform(self.flow.result, simplified),
                  self.flow.minus.animate.set_opacity(.2), run_time=.9)
        self.to(44)

        # 44–50 s: recover exp, then reveal the real subject—uniform trees.
        self.text(
            "핵심은 함수 하나가 아닙니다",
            "같은 EML 노드를 반복해서 연결하면, 더 많은 연산을\n하나의 통일된 expression tree로 표현할 수 있습니다.",
            "하나의 primitive     →     더 깊은 연산 그래프",
        )
        tree = ExpressionTree(("EML", "x", "1"), width=3.0).scale(1.1).move_to([-1.8, .35, 0])
        arrow = Arrow([-.15, .35, 0], [1.25, .35, 0], buff=.08,
                      color=GOLD, stroke_width=4, tip_length=.18)
        exp_chip = OperatorChip("eˣ", GOLD, width=1.7, height=1.12).move_to([2.35, .35, 0])
        exp_chip.save_state()
        exp_chip.set_opacity(.16)
        reconstruction = VGroup(tree, arrow, exp_chip)
        self.play(FadeOut(self.flow), FadeIn(tree), Create(arrow), FadeIn(exp_chip), run_time=.8)
        self.stage = reconstruction
        self.play(
            Restore(exp_chip),
            Flash(exp_chip, color=GOLD, line_length=.25, flash_radius=1.1),
            run_time=1.0,
        )
        self.play(Indicate(exp_chip, color=GOLD, scale_factor=1.08), run_time=.65)
        log_tree = ExpressionTree(
            ("EML", "1", ("EML", ("EML", "1", "x"), "1")),
            width=5.8, level_gap=1.08,
        ).scale(.55).move_to([2.35, -.1, 0])
        deeper = VGroup(
            log_tree,
            txt("반복 연결", 23, PINK).move_to([2.35, -2.55, 0]),
            txt("…", 38, MUTED).move_to([.45, .2, 0]),
        )
        self.play(reconstruction.animate.scale(.72).move_to([-1.95, .15, 0]),
                  FadeIn(deeper), run_time=.8)
        self.stage = VGroup(reconstruction, deeper)
        self.to(50)

    def leaf(self, value, color):
        return VGroup(
            Circle(radius=.38, stroke_color=color, stroke_width=2,
                   fill_color="#12233A", fill_opacity=.95),
            txt(value, 28, color),
        )

    def make_flow(self, right_value):
        x_leaf = self.leaf("x", BLUE).move_to([-2.45, -1.8, 0])
        y_leaf = self.leaf(right_value, PINK).move_to([2.45, -1.8, 0])
        exp_box = OperatorChip("exp", BLUE, width=1.65).move_to([-2.45, .05, 0])
        log_box = OperatorChip("ln", PINK, width=1.65).move_to([2.45, .05, 0])
        exp_value = txt("eˣ", 36, BLUE).move_to([-1.35, 2.05, 0])
        log_value = txt(f"ln {right_value}", 34, PINK).move_to([1.35, 2.05, 0])
        minus = txt("−", 42, GOLD).move_to([0, 2.05, 0])
        result = txt("eˣ − ln y", 39, GOLD).move_to([0, 3.35, 0])
        x_arrow = input_arrow(x_leaf.get_top(), exp_box.get_bottom(), BLUE)
        y_arrow = input_arrow(y_leaf.get_top(), log_box.get_bottom(), PINK)
        exp_arrow = input_arrow(exp_box.get_top(), exp_value.get_bottom(), BLUE)
        log_arrow = input_arrow(log_box.get_top(), log_value.get_bottom(), PINK)
        merge = VGroup(
            Line(exp_value.get_top(), result.get_bottom() + LEFT * .45, color=BLUE, stroke_width=2),
            Line(log_value.get_top(), result.get_bottom() + RIGHT * .45, color=PINK, stroke_width=2),
        )
        group = VGroup(x_leaf, y_leaf, x_arrow, y_arrow, exp_box, log_box,
                       exp_arrow, log_arrow, exp_value, log_value, minus, merge, result)
        group.x_leaf, group.y_leaf = x_leaf, y_leaf
        group.exp_value, group.log_value = exp_value, log_value
        group.log_arrow, group.minus, group.result = log_arrow, minus, result
        group.exp_path = VGroup(x_leaf, x_arrow, exp_box, exp_arrow, exp_value)
        group.log_path = VGroup(y_leaf, y_arrow, log_box, log_arrow, log_value)
        return group

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 24, GOLD).move_to(DOWN * 4.72)
        self.sub = txt(sub, 27).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.35)

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(
                self.progress.animate.stretch_to_fit_width(width).move_to(
                    [-3.8 + width / 2, -7.35, 0]
                ),
                run_time=min(.28, remain),
            )
            self.wait(max(0, target - self.time))
