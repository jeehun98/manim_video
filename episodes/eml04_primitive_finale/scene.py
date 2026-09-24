"""EML 04 finale: meaning comes from a primitive and its topology."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.eml_series.visuals import (
    BLUE, GOLD, GREEN, INK, MUTED, PINK,
    EMLNode, ExpressionTree, OperatorChip, txt,
)


EXP_TREE = ("EML", "x", "1")
LOG_TREE = ("EML", "1", ("EML", ("EML", "1", "x"), "1"))
E1 = ("EML", "x", "1")
E2 = ("EML", "1", E1)
E3 = ("EML", "1", E2)
E4 = ("EML", E3, "1")
E5 = ("EML", "1", E4)
E6 = ("EML", "y", "1")
E7 = ("EML", E5, E6)
E8 = ("EML", E7, "1")
ADD_TREE = ("EML", "1", E8)


class EMLPrimitiveFinale(Scene):
    DURATION = 72
    POOL_SIZE = 12

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.stage = VGroup()
        self.add(
            txt("ONE PRIMITIVE  /  EML 04  ·  FINALE", 20, MUTED).move_to(UP * 7.25),
            txt("하나의 연산자로 계산한다는 것은 무엇일까?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s: recap the three constructions actually shown in the series.
        self.text(
            "서로 달라 보였던 계산들",
            "지금까지 지수함수, 로그, 덧셈처럼\n서로 달라 보이는 연산을 같은 EML로 표현했습니다.",
            "exp(x)     ·     ln(x)     ·     x + y",
        )
        familiar = VGroup(
            OperatorChip("exp", BLUE, width=1.55),
            OperatorChip("ln", PINK, width=1.55),
            OperatorChip("+", GOLD, width=1.55),
            OperatorChip("×", GREEN, width=1.55).set_opacity(.35),
        ).arrange_in_grid(rows=2, cols=2, buff=(.75, .65)).move_to([0, .35, 0])
        note = txt("×  ·  논문의 더 넓은 연산 세계", 21, MUTED).move_to([0, -1.75, 0])
        recap = VGroup(familiar, note)
        self.play(LaggedStart(*[FadeIn(chip, shift=UP * .15) for chip in familiar],
                              lag_ratio=.15), FadeIn(note), run_time=1.3)
        self.play(LaggedStart(*[Indicate(familiar[i], scale_factor=1.06)
                                for i in range(3)], lag_ratio=.2), run_time=1.1)
        self.stage = recap
        self.to(7)

        # 7–14 s: different surface vocabulary, one internal grammar.
        self.text(
            "겉은 달라도 내부 문법은 같습니다",
            "겉으로는 다른 계산이지만 내부 표현은\n모두 같은 종류의 노드로 바꿀 수 있습니다.",
            "many operators  →  EML + constant 1",
        )
        center_node = EMLNode(width=2.5, height=1.15).move_to([0, .7, 0])
        one = self.leaf("1", GREEN).move_to([0, -1.15, 0])
        arrow = Arrow(one.get_top(), center_node.right_anchor(), buff=.08,
                      color=GREEN, stroke_width=3, tip_length=.15)
        reduced = VGroup(center_node, one, arrow,
                         txt("표현 grammar", 24, GOLD).move_to([0, -2.05, 0]))
        transforms = [chip.animate.move_to(center_node).scale(.15).set_opacity(0)
                      for chip in familiar]
        self.play(FadeOut(note), LaggedStart(*transforms, lag_ratio=.1),
                  FadeIn(reduced), run_time=1.5)
        self.play(Circumscribe(center_node, color=GOLD, buff=.17), run_time=.8)
        self.stage = reduced
        self.to(14)

        # 14–20 s: establish an unchanged inventory of identical parts.
        self.text(
            "부품은 모두 동일합니다",
            "이제 똑같은 EML 블록 열두 개를 준비하고,\n연결 구조만 바꿔보겠습니다.",
            "same nodes     ·     topology changes",
        )
        self.pool = VGroup(*[EMLNode(width=1.2, height=.6, compact=True)
                             for _ in range(self.POOL_SIZE)])
        self.pool.arrange_in_grid(rows=3, cols=4, buff=(.35, .48)).move_to([0, .35, 0])
        self.play(FadeOut(reduced), LaggedStart(*[FadeIn(n, shift=UP * .1)
                                                  for n in self.pool], lag_ratio=.06),
                  run_time=1.2)
        self.play(LaggedStart(*[Indicate(n, color=GOLD, scale_factor=1.05)
                                for n in self.pool], lag_ratio=.06), run_time=1.25)
        self.stage = self.pool
        self.to(20)

        # 20–28 s: the same inventory forms exp with one active node.
        self.text(
            "첫 번째 연결 구조",
            "한 노드의 두 입력에 x와 1을 연결하면\n지수함수의 graph가 됩니다.",
            "EML(x, 1) = exp(x)",
        )
        exp_targets, exp_overlay = self.layout_targets(EXP_TREE, scale=1.0, center=[0, .65, 0])
        exp_result = OperatorChip("exp(x)", BLUE, width=2.1, height=.95).move_to([0, 2.85, 0])
        exp_out = Arrow([0, 1.32, 0], exp_result.get_bottom(), buff=.08,
                        color=BLUE, stroke_width=3, tip_length=.15)
        self.play(*[Transform(node, target) for node, target in zip(self.pool, exp_targets)],
                  run_time=1.25)
        self.play(FadeIn(exp_overlay), GrowArrow(exp_out), FadeIn(exp_result), run_time=.8)
        self.play(Indicate(exp_result, color=BLUE, scale_factor=1.07), run_time=.7)
        current_overlay = VGroup(exp_overlay, exp_out, exp_result)
        self.to(28)

        # 28–36 s: no parts are replaced; three are rewired into ln.
        self.text(
            "같은 부품, 다른 연결",
            "블록을 다시 풀어 세 노드로 연결하면,\n이번에는 로그의 graph가 됩니다.",
            "same EML blocks     →     ln(x)",
        )
        log_targets, log_overlay = self.layout_targets(LOG_TREE, scale=.8, center=[0, .25, 0])
        log_result = OperatorChip("ln(x)", PINK, width=2.0, height=.95).move_to([0, 3.0, 0])
        log_out = Arrow(log_overlay.root_point, log_result.get_bottom(), buff=.08,
                        color=PINK, stroke_width=3, tip_length=.15)
        self.play(FadeOut(current_overlay),
                  *[Transform(node, target) for node, target in zip(self.pool, log_targets)],
                  run_time=1.25)
        self.play(FadeIn(log_overlay), GrowArrow(log_out), FadeIn(log_result), run_time=.8)
        self.play(Indicate(log_result, color=PINK, scale_factor=1.07), run_time=.7)
        current_overlay = VGroup(log_overlay, log_out, log_result)
        self.to(36)

        # 36–45 s: nine of the same objects become the addition tree.
        self.text(
            "연결을 다시 바꾸면",
            "이번에는 아홉 노드가 두 입력을 합쳐\n덧셈과 같은 관계를 만듭니다.",
            "same EML blocks     →     x + y",
        )
        add_targets, add_overlay = self.layout_targets(ADD_TREE, scale=.64, center=[0, .35, 0])
        add_result = OperatorChip("x + y", GREEN, width=2.0, height=.9).move_to([0, 3.15, 0])
        add_out = Arrow(add_overlay.root_point, add_result.get_bottom(), buff=.08,
                        color=GREEN, stroke_width=3, tip_length=.15)
        self.play(FadeOut(current_overlay),
                  *[Transform(node, target) for node, target in zip(self.pool, add_targets)],
                  run_time=1.45)
        self.play(FadeIn(add_overlay), GrowArrow(add_out), FadeIn(add_result), run_time=.8)
        self.play(Indicate(add_result, color=GREEN, scale_factor=1.07), run_time=.7)
        current_overlay = VGroup(add_overlay, add_out, add_result)
        self.to(45)

        # 45–52 s: one evaluation rule can traverse every uniform tree.
        self.text(
            "하나의 공통된 평가 규칙",
            "tree의 모양은 달라도 각 노드는 언제나\n같은 EML 규칙으로 계산할 수 있습니다.",
            "left, right  →  exp(left) − ln(right)",
        )
        rule_rows = VGroup()
        for i, color in enumerate([BLUE, PINK, GOLD]):
            y = 1.75 - i * 1.45
            row = VGroup(
                self.leaf("L", BLUE).scale(.65).move_to([-3.1, y, 0]),
                self.leaf("R", PINK).scale(.65).move_to([-2.15, y, 0]),
                Arrow([-1.7, y, 0], [-.85, y, 0], buff=.05,
                      color=MUTED, stroke_width=2, tip_length=.12),
                EMLNode(width=1.4, height=.68, compact=True).move_to([0, y, 0]),
                Arrow([.8, y, 0], [1.55, y, 0], buff=.05,
                      color=color, stroke_width=2, tip_length=.12),
                txt("eᴸ − ln R", 25, color).move_to([2.65, y, 0]),
            )
            rule_rows.add(row)
        self.play(FadeOut(VGroup(self.pool, current_overlay)), FadeIn(rule_rows), run_time=.85)
        self.play(LaggedStart(*[Indicate(row[3], color=GOLD, scale_factor=1.07)
                                for row in rule_rows], lag_ratio=.25), run_time=1.2)
        self.stage = rule_rows
        self.to(52)

        # 52–59 s: a short structural comparison with NAND.
        self.text(
            "NAND가 던졌던 것과 닮은 질문",
            "NAND 하나가 여러 논리 연산을 구성하듯, EML은\n작은 primitive set의 표현력이 어디까지인지 묻습니다.",
            "universal primitive라는 구조적 아이디어",
        )
        nand = VGroup(
            OperatorChip("NAND", BLUE, width=2.1, height=1.0),
            txt("→", 34, MUTED),
            txt("NOT · AND · OR", 26, BLUE),
        ).arrange(RIGHT, buff=.4).move_to([0, 1.35, 0])
        eml = VGroup(
            OperatorChip("EML + 1", GOLD, width=2.1, height=1.0),
            txt("→", 34, MUTED),
            txt("exp · ln · + · …", 26, GOLD),
        ).arrange(RIGHT, buff=.4).move_to([0, -1.05, 0])
        comparison = VGroup(
            nand, eml,
            txt("디지털 논리", 21, MUTED).move_to([-2.85, 2.1, 0]),
            txt("elementary functions", 21, MUTED).move_to([-2.5, -.3, 0]),
        )
        self.play(FadeOut(rule_rows), FadeIn(comparison), run_time=.8)
        self.play(Indicate(nand[0], color=BLUE, scale_factor=1.06),
                  Indicate(eml[0], color=GOLD, scale_factor=1.06), run_time=1.0)
        self.stage = comparison
        self.to(59)

        # 59–65 s: power of expression and runtime efficiency remain separate.
        self.text(
            "표현력은 효율과 같은 말이 아닙니다",
            "물론 실제 컴퓨터에서 EML 하나만 쓰는 것이\n가장 효율적이라는 뜻은 아닙니다.",
            "Expressive power  ≠  execution efficiency",
        )
        caveat = VGroup(
            self.metric_card("표현 가능성", "무엇을 만들 수 있나?", BLUE).move_to([-2.35, .45, 0]),
            txt("≠", 47, PINK).move_to([0, .45, 0]),
            self.metric_card("실행 효율", "얼마나 잘 실행되나?", GREEN).move_to([2.35, .45, 0]),
            txt("node 수 · depth · 메모리 이동 · 하드웨어", 23, MUTED).move_to([0, -1.25, 0]),
        )
        self.play(FadeOut(comparison), FadeIn(caveat), run_time=.8)
        self.play(Indicate(caveat[1], color=PINK, scale_factor=1.25), run_time=.75)
        self.stage = caveat
        self.to(65)

        # 65–72 s: close on the real question—parts or composition?
        self.text(
            "복잡성은 어디에서 오는가?",
            "결국 계산을 결정하는 것은 가진 부품의 종류뿐 아니라,\n그 부품을 어떻게 조합하는가이기도 합니다.",
            "few kinds of parts     ·     many possible structures",
        )
        forest = self.make_forest()
        center = EMLNode(width=1.65, height=.8, compact=True).move_to([0, .35, 0])
        rings = VGroup(
            Circle(radius=1.35, color=GOLD, stroke_opacity=.25).move_to(center),
            Circle(radius=2.2, color=GOLD, stroke_opacity=.12).move_to(center),
        )
        finale = VGroup(forest, rings, center,
                        txt("하나의 primitive", 27, GOLD).move_to([0, -2.55, 0]),
                        txt("수많은 계산 graph", 30, INK).move_to([0, 3.15, 0]))
        self.play(FadeOut(caveat), FadeIn(forest), Create(rings), FadeIn(center), run_time=1.0)
        self.play(LaggedStart(*[Indicate(tree, scale_factor=1.03)
                                for tree in forest], lag_ratio=.2), run_time=1.1)
        self.play(FadeIn(finale[-2]), FadeIn(finale[-1]), run_time=.6)
        self.stage = finale
        self.to(72)

    def leaf(self, value, color):
        return VGroup(
            Circle(radius=.35, stroke_color=color, stroke_width=2,
                   fill_color="#12233A", fill_opacity=.95),
            txt(value, 25, color),
        )

    def inactive_targets(self, count):
        bank = VGroup(*[EMLNode(width=.78, height=.4, compact=True).set_opacity(.16)
                        for _ in range(count)])
        if count:
            bank.arrange_in_grid(rows=2, cols=6, buff=(.18, .2)).move_to([0, -3.25, 0])
        return list(bank)

    def layout_targets(self, expression, scale, center):
        skeleton = ExpressionTree(expression, width=6.6, level_gap=.86).scale(scale).move_to(center)
        active = [node.copy() for node in skeleton.nodes]
        inactive = self.inactive_targets(self.POOL_SIZE - len(active))
        targets = active + inactive
        overlay = VGroup(skeleton.edges.copy(), skeleton.leaves.copy())
        overlay.root_point = skeleton.root.output_anchor()
        return targets, overlay

    def metric_card(self, title, value, color):
        box = RoundedRectangle(width=3.35, height=2.05, corner_radius=.15,
                               stroke_color=color, fill_color=color,
                               fill_opacity=.07, stroke_width=1.7)
        return VGroup(
            box,
            txt(title, 24, color).move_to([0, .42, 0]),
            txt(value, 23, INK, 2.95).move_to([0, -.35, 0]),
        )

    def make_forest(self):
        exp = ExpressionTree(EXP_TREE, width=2.2).scale(.55).move_to([-2.65, .3, 0])
        log = ExpressionTree(LOG_TREE, width=4.0, level_gap=.9).scale(.38).move_to([2.55, 1.2, 0])
        add = ExpressionTree(ADD_TREE, width=6.2, level_gap=.75).scale(.3).move_to([2.25, -1.2, 0])
        for tree, color in [(exp, BLUE), (log, PINK), (add, GREEN)]:
            tree.set_stroke(opacity=.55)
            tree.nodes.set_color(GOLD)
            tree.leaves.set_color(color)
        return VGroup(exp, log, add)

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
