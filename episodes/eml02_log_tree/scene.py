"""EML 02: evaluate a repeated EML tree until only ln(x) remains."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.eml_series.visuals import (
    BLUE, GOLD, GREEN, INK, MUTED, PINK,
    EMLNode, ExpressionTree, OperatorChip, txt,
)


LOG_TREE = ("EML", "1", ("EML", ("EML", "1", "x"), "1"))


class EMLLogTree(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.stage = VGroup()
        self.add(
            txt("ONE PRIMITIVE  /  EML 02", 20, MUTED).move_to(UP * 7.25),
            txt("같은 연산자를 연결해서 로그 만들기", 35).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s: recap the depth-one expression from episode 1.
        self.text(
            "1편의 가장 얕은 tree",
            "앞에서는 EML의 두 번째 입력에 상수 1을 넣어\n지수함수를 표현했습니다.",
            "EML(x, 1) = eˣ",
        )
        exp_tree = ExpressionTree(("EML", "x", "1"), width=3.0).scale(1.05).move_to([-1.8, .35, 0])
        exp_arrow = Arrow([-.15, .35, 0], [1.25, .35, 0], buff=.08,
                          color=GOLD, stroke_width=4, tip_length=.18)
        exp_chip = OperatorChip("eˣ", GOLD, width=1.7, height=1.12).move_to([2.35, .35, 0])
        recap = VGroup(exp_tree, exp_arrow, exp_chip)
        self.play(FadeIn(exp_tree), Create(exp_arrow), FadeIn(exp_chip), run_time=1.0)
        self.play(Indicate(exp_chip, color=GOLD, scale_factor=1.08), run_time=.75)
        self.stage = recap
        self.to(6)

        # 6–12 s: pose log as the new target, without adding a log primitive.
        self.text(
            "이번 목표는 ln x",
            "이번에는 새로운 연산자를 추가하지 않고\n로그를 만들어보겠습니다.",
            "새 log node 없이     ·     EML만 사용",
        )
        log_chip = OperatorChip("ln x", PINK, width=2.0, height=1.15).move_to([-2.35, .55, 0])
        crossed = Cross(log_chip, stroke_color=PINK, stroke_width=5)
        compact_tree = ExpressionTree(LOG_TREE, width=5.8, level_gap=1.08).scale(.6).move_to([2.0, .2, 0])
        target = VGroup(log_chip, crossed,
                        Arrow([-.85, .55, 0], [.25, .55, 0], buff=.05,
                              color=GOLD, stroke_width=3, tip_length=.15),
                        compact_tree)
        self.play(FadeOut(recap), FadeIn(log_chip), Create(crossed),
                  GrowArrow(target[2]), FadeIn(compact_tree), run_time=1.0)
        self.stage = target
        self.play(LaggedStart(*[Indicate(n, color=GOLD, scale_factor=1.05)
                                for n in compact_tree.nodes], lag_ratio=.22), run_time=1.2)
        self.to(12)

        # 12–19 s: show that node outputs can become node inputs.
        self.text(
            "출력은 다시 입력이 됩니다",
            "EML의 입력에는 숫자뿐 아니라\n다른 EML의 결과도 넣을 수 있습니다.",
            "같은 node의 출력 → 다음 node의 입력",
        )
        self.tree = ExpressionTree(LOG_TREE, width=5.8, level_gap=1.22).scale(.88).move_to([0, .2, 0])
        self.tree.edges.set_opacity(.18)
        self.tree.nodes.set_opacity(.25)
        self.tree.leaves.set_opacity(.35)
        self.play(FadeOut(target), FadeIn(self.tree), run_time=.7)
        self.stage = self.tree
        self.play(self.tree.leaves.animate.set_opacity(1), run_time=.55)
        self.play(LaggedStart(*[AnimationGroup(Create(edge), edge.animate.set_opacity(1))
                                for edge in self.tree.edges], lag_ratio=.12),
                  self.tree.nodes.animate.set_opacity(1), run_time=1.8)
        self.to(19)

        # 19–26 s: evaluate the deepest node first.
        self.text(
            "가장 안쪽부터 계산합니다",
            "가장 안쪽 EML에 1과 x를 넣으면\n첫 번째 중간 결과가 만들어집니다.",
            "A = EML(1, x) = e − ln x",
        )
        inner, middle, root = self.tree.nodes
        self.badge_a = self.result_badge("A = e − ln x", BLUE).next_to(inner, LEFT, buff=.28)
        self.play(Indicate(VGroup(self.tree.leaves[1], self.tree.leaves[2], inner),
                           color=BLUE, scale_factor=1.06), run_time=1.1)
        self.play(FadeIn(self.badge_a, shift=UP * .12), run_time=.65)
        self.play(Flash(inner.output_anchor(), color=BLUE, flash_radius=.35,
                        line_length=.12), run_time=.7)
        self.stage.add(self.badge_a)
        self.to(26)

        # 26–33 s: feed A to the next identical EML node.
        self.text(
            "그 결과를 다음 노드로",
            "A를 다음 EML의 첫 번째 입력에 넣으면\n두 번째 중간 결과 B가 됩니다.",
            "B = EML(A, 1) = eᴬ = eᵉ / x",
        )
        self.badge_b = self.result_badge("B = eᵉ / x", PINK).next_to(middle, LEFT, buff=.25)
        path_to_middle = self.tree.edges[2]
        self.play(Indicate(self.badge_a, color=BLUE, scale_factor=1.05),
                  ShowPassingFlash(path_to_middle.copy().set_color(BLUE).set_stroke(width=7),
                                   time_width=.45), run_time=1.0)
        self.play(Indicate(VGroup(middle, self.tree.leaves[3]),
                           color=PINK, scale_factor=1.06), run_time=.85)
        self.play(FadeIn(self.badge_b, shift=UP * .1), run_time=.65)
        self.stage.add(self.badge_b)
        self.to(33)

        # 33–42 s: the root expression exposes the cancellation.
        self.text(
            "마지막 EML에서",
            "B를 마지막 노드의 두 번째 입력에 넣으면,\n지수와 로그로 만들어진 항들이 다시 펼쳐집니다.",
            "EML(1, B) = e − ln(eᵉ / x)",
        )
        self.play(Indicate(self.badge_b, color=PINK, scale_factor=1.06), run_time=.7)
        self.play(ShowPassingFlash(self.tree.edges[-1].copy().set_color(PINK).set_stroke(width=7),
                                   time_width=.45),
                  Indicate(root, color=GOLD, scale_factor=1.08), run_time=1.1)
        self.play(self.tree.animate.scale(.58).move_to([-2.55, .3, 0]),
                  FadeOut(VGroup(self.badge_a, self.badge_b)), run_time=.75)
        self.algebra = self.make_cancellation()
        self.play(FadeIn(self.algebra[0]), run_time=.6)
        self.play(TransformFromCopy(self.algebra[0], self.algebra[1]), run_time=.8)
        self.to(42)

        # 42–48 s: cancel equal e terms and leave ln(x).
        self.text(
            "같은 항이 서로 상쇄됩니다",
            "바깥의 e와 괄호 안의 e가 상쇄되고,\n마지막에는 ln x만 남습니다.",
            "e − (e − ln x) = ln x",
        )
        e_left, e_inner = self.algebra.cancel_terms
        strikes = VGroup(Cross(e_left, stroke_color=PINK, stroke_width=4),
                         Cross(e_inner, stroke_color=PINK, stroke_width=4))
        self.play(Indicate(VGroup(e_left, e_inner), color=GOLD, scale_factor=1.18), run_time=.8)
        self.play(Create(strikes), run_time=.65)
        self.play(FadeIn(self.algebra[2], shift=UP * .12), run_time=.7)
        self.stage.add(strikes, self.algebra)
        self.to(48)

        # 48–55 s: compare the ordinary symbol and the EML-only graph.
        self.text(
            "새로운 노드를 추가한 것이 아닙니다",
            "로그라는 새 primitive를 추가한 것이 아니라,\n같은 EML 노드의 연결 구조만 바꿨습니다.",
            "같은 primitive  +  다른 graph  →  다른 연산",
        )
        summary_tree = ExpressionTree(LOG_TREE, width=5.8, level_gap=1.05).scale(.55).move_to([-2.45, .15, 0])
        summary = VGroup(
            summary_tree,
            txt("+", 36, MUTED).move_to([-.35, .15, 0]),
            txt("연결 구조", 28, BLUE).move_to([1.0, .15, 0]),
            Arrow([2.0, .15, 0], [2.65, .15, 0], buff=.05,
                  color=GOLD, stroke_width=3, tip_length=.14),
            OperatorChip("ln x", PINK, width=1.5, height=.95).move_to([3.35, .15, 0]),
        )
        self.play(FadeOut(VGroup(self.tree, self.algebra, strikes)), FadeIn(summary), run_time=.85)
        self.stage = summary
        self.play(Indicate(summary[-1], color=PINK, scale_factor=1.08), run_time=.8)
        self.to(55)

        # 55–60 s: bridge from operations to generated constants.
        self.text(
            "다음은 숫자입니다",
            "그렇다면 연산뿐 아니라, 계산에 필요한 숫자들도\n이 구조 안에서 만들 수 있을까요?",
            "NEXT  ·  상수 1에서 다른 수 만들기",
        )
        constants = VGroup(
            self.leaf("1", GREEN).move_to([-3.0, .4, 0]),
            txt("→", 35, GOLD).move_to([-1.9, .4, 0]),
            OperatorChip("EML tree", GOLD, width=2.2, height=1.05).move_to([-.35, .4, 0]),
            txt("→", 35, GOLD).move_to([1.2, .4, 0]),
            VGroup(*[self.leaf(v, c).scale(.8) for v, c in [("e", BLUE), ("0", PINK), ("−1", GOLD)]])
                .arrange(RIGHT, buff=.35).move_to([2.7, .4, 0]),
        )
        self.play(FadeOut(summary), FadeIn(constants), run_time=.8)
        self.stage = constants
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.1) for c in constants[-1]],
                              lag_ratio=.25), run_time=1.0)
        self.to(60)

    def leaf(self, value, color):
        return VGroup(
            Circle(radius=.38, stroke_color=color, stroke_width=2,
                   fill_color="#12233A", fill_opacity=.95),
            txt(value, 27, color),
        )

    def result_badge(self, text, color):
        label = txt(text, 19, color, 2.4)
        box = RoundedRectangle(width=max(1.5, label.width + .28), height=.48,
                               corner_radius=.1, stroke_color=color,
                               fill_color="#12233A", fill_opacity=.96,
                               stroke_width=1.4)
        return VGroup(box, label)

    def token_row(self, tokens, colors, y):
        row = VGroup(*[txt(token, 31, color) for token, color in zip(tokens, colors)])
        row.arrange(RIGHT, buff=.16).move_to([1.65, y, 0])
        return row

    def make_cancellation(self):
        row1 = self.token_row(
            ["e", "−", "ln", "(", "eᵉ / x", ")"],
            [GOLD, INK, PINK, MUTED, BLUE, MUTED], 1.55,
        )
        row2 = self.token_row(
            ["e", "−", "(", "e", "−", "ln x", ")"],
            [GOLD, INK, MUTED, GOLD, INK, PINK, MUTED], .15,
        )
        row3 = VGroup(
            txt("=", 31, MUTED),
            OperatorChip("ln x", PINK, width=1.7, height=.85),
        ).arrange(RIGHT, buff=.3).move_to([1.65, -1.45, 0])
        group = VGroup(row1, row2, row3)
        group.cancel_terms = (row2[0], row2[3])
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
