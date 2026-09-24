"""EML 03: replace one Add node with the K=19 EML-only tree."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.eml_series.visuals import (
    BLUE, GOLD, GREEN, INK, MUTED, PINK,
    EMLNode, ExpressionTree, OperatorChip, txt,
)


# Direct-search K=19 witness from the paper's supplementary verification.
E1 = ("EML", "x", "1")
E2 = ("EML", "1", E1)
E3 = ("EML", "1", E2)
E4 = ("EML", E3, "1")
E5 = ("EML", "1", E4)       # ln(e - x)
E6 = ("EML", "y", "1")     # exp(y)
E7 = ("EML", E5, E6)        # e - x - y
E8 = ("EML", E7, "1")       # exp(e - x - y)
ADD_TREE = ("EML", "1", E8) # x + y


class EMLAdditionGraph(Scene):
    DURATION = 66

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.stage = VGroup()
        self.add(
            txt("ONE PRIMITIVE  /  EML 03", 20, MUTED).move_to(UP * 7.25),
            txt("덧셈도 기본 연산자가 아니라면?", 35).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s: recap two unary functions represented by EML trees.
        self.text(
            "지금까지는 하나의 입력을 바꿨습니다",
            "지금까지 지수함수와 로그를\nEML의 연결 구조로 표현했습니다.",
            "x → exp(x)     ·     x → ln(x)",
        )
        exp_tree = ExpressionTree(("EML", "x", "1"), width=2.6).scale(.82)
        log_tree = ExpressionTree(
            ("EML", "1", ("EML", ("EML", "1", "x"), "1")),
            width=4.4, level_gap=1.0,
        ).scale(.56)
        exp_card = VGroup(exp_tree, txt("exp(x)", 26, BLUE).next_to(exp_tree, DOWN, buff=.35))
        log_card = VGroup(log_tree, txt("ln(x)", 26, PINK).next_to(log_tree, DOWN, buff=.35))
        unary = VGroup(exp_card, log_card).arrange(RIGHT, buff=1.0).move_to(UP * .2)
        self.play(FadeIn(unary), run_time=.9)
        self.play(Indicate(exp_card, color=BLUE, scale_factor=1.04),
                  Indicate(log_card, color=PINK, scale_factor=1.04), run_time=1.0)
        self.stage = unary
        self.to(6)

        # 6–12 s: one familiar binary node.
        self.text(
            "이번에는 두 입력을 결합합니다",
            "이번에는 가장 익숙한 이항 연산인\n덧셈을 없애보겠습니다.",
            "두 입력 x, y     →     하나의 출력 x + y",
        )
        add_graph = self.make_add_graph(scale=1.0).move_to([0, .35, 0])
        self.play(FadeOut(unary), FadeIn(add_graph), run_time=.8)
        self.play(Indicate(add_graph.node, color=GOLD, scale_factor=1.12), run_time=.9)
        self.stage = add_graph
        self.to(12)

        # 12–19 s: forbid Add and reveal the EML-only witness.
        self.text(
            "+ 노드는 사용할 수 없습니다",
            "보통 덧셈 노드 하나면 충분하지만,\n이번에는 같은 EML 노드만 반복해 연결합니다.",
            "1 Add node  →  9 EML nodes",
        )
        crossed = Cross(add_graph.node, stroke_color=PINK, stroke_width=5)
        self.play(Create(crossed), run_time=.55)
        self.add_tree = self.make_add_tree().move_to([0, .15, 0])
        self.add_tree.set_opacity(.12)
        self.play(FadeOut(VGroup(add_graph, crossed)), FadeIn(self.add_tree), run_time=.75)
        self.play(self.add_tree.edges.animate.set_opacity(.7),
                  self.add_tree.leaves.animate.set_opacity(.8),
                  self.add_tree.nodes.animate.set_opacity(1), run_time=1.0)
        self.node_count = txt("9 identical EML nodes", 25, GOLD).move_to([0, -3.65, 0])
        self.play(FadeIn(self.node_count), run_time=.45)
        self.stage = VGroup(self.add_tree, self.node_count)
        self.to(19)

        # 19–26 s: isolate the five-node x branch.
        self.text(
            "먼저 x의 경로",
            "입력 x는 다섯 개의 EML 노드를 지나며\n다음 계산에 필요한 형태로 바뀝니다.",
            "x  →  ln(e − x)",
        )
        self.play(FadeOut(self.node_count), run_time=.25)
        self.dim_tree(self.add_tree)
        x_leaf = self.find_leaf(self.add_tree, "x")
        x_edges = VGroup(*[self.add_tree.edges[i] for i in [0, 3, 5, 6, 9]])
        x_path = VGroup(x_leaf, x_edges, *self.add_tree.nodes[:5])
        self.play(x_path.animate.set_opacity(1), run_time=.6)
        self.play(LaggedStart(*[Indicate(n, color=BLUE, scale_factor=1.05)
                                for n in self.add_tree.nodes[:5]], lag_ratio=.13), run_time=1.65)
        self.x_badge = self.result_badge("L = ln(e − x)", BLUE).move_to([2.55, -2.65, 0])
        self.play(FadeIn(self.x_badge), run_time=.5)
        self.stage.add(self.x_badge)
        self.to(26)

        # 26–32 s: the y branch is shorter and meets x at E7.
        self.text(
            "y는 다른 경로를 지납니다",
            "입력 y는 한 개의 EML을 지나 eʸ가 되고,\n두 경로는 다음 EML에서 만납니다.",
            "y → eʸ     ·     EML(L, eʸ) = e − x − y",
        )
        y_leaf = self.find_leaf(self.add_tree, "y")
        y_edges = VGroup(self.add_tree.edges[10], self.add_tree.edges[13])
        y_path = VGroup(y_leaf, y_edges, self.add_tree.nodes[5])
        self.play(y_path.animate.set_opacity(1), run_time=.5)
        self.play(Indicate(y_path, color=PINK, scale_factor=1.07), run_time=.85)
        self.y_badge = self.result_badge("R = eʸ", PINK).move_to([2.65, -.95, 0])
        self.play(FadeIn(self.y_badge), run_time=.45)
        meet = self.add_tree.nodes[6]
        self.play(meet.animate.set_opacity(1),
                  Indicate(meet, color=GOLD, scale_factor=1.1), run_time=.9)
        self.stage.add(self.y_badge)
        self.to(32)

        # 32–42 s: evaluate the remaining three nodes with a readable side panel.
        self.text(
            "두 경로가 합쳐진 뒤",
            "안쪽부터 계산하면 지수와 로그가 생겼다가\n마지막 두 노드에서 다시 정리됩니다.",
            "leaf → root     ·     같은 tree, 같은 평가 순서",
        )
        self.play(FadeOut(VGroup(self.x_badge, self.y_badge)),
                  self.add_tree.animate.scale(.68).move_to([-2.45, .45, 0]), run_time=.75)
        rows = VGroup(
            self.formula_row("L = ln(e − x)", BLUE),
            self.formula_row("R = eʸ", PINK),
            self.formula_row("EML(L,R) = e − x − y", GOLD),
            self.formula_row("→ exp(e − x − y)", BLUE),
            self.formula_row("→ e − (e − x − y)", GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.35).move_to([1.55, .35, 0])
        for index, row in enumerate(rows):
            node = self.add_tree.nodes[min(6 + max(0, index - 2), 8)]
            self.play(FadeIn(row, shift=UP * .08),
                      Indicate(node, color=row[0].get_color(), scale_factor=1.08),
                      run_time=.55)
        self.eval_rows = rows
        self.stage.add(rows)
        self.to(42)

        # 42–48 s: collapse the evaluated tree to the familiar result.
        self.text(
            "마지막에 남는 출력",
            "복잡한 EML tree의 최종 결과는\n처음 덧셈과 같은 x+y입니다.",
            "EML-only tree(x, y) = x + y",
        )
        result = OperatorChip("x + y", GREEN, width=2.7, height=1.35).move_to([0, .45, 0])
        self.play(FadeOut(VGroup(self.add_tree, rows)), FadeIn(result), run_time=.8)
        self.play(Flash(result, color=GREEN, line_length=.28, flash_radius=1.35),
                  Indicate(result, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.stage = result
        self.to(48)

        # 48–55 s: compare two graphs with the same input-output relation.
        self.text(
            "같은 계산, 다른 표현",
            "왼쪽은 덧셈 노드 하나, 오른쪽은 EML-only tree입니다.\n두 graph의 입력과 출력 관계는 같습니다.",
            "1 Add node     ⇔     9 EML nodes",
        )
        left = self.make_add_graph(scale=.63).move_to([-2.35, .45, 0])
        right = self.make_add_tree().scale(.42).move_to([2.35, .55, 0])
        comparison = VGroup(
            left, right,
            txt("1 Add node", 23, BLUE).move_to([-2.35, -2.75, 0]),
            txt("9 EML nodes · depth 8", 23, GOLD).move_to([2.35, -2.75, 0]),
            txt("x + y", 27, GREEN).move_to([-2.35, -3.35, 0]),
            txt("x + y", 27, GREEN).move_to([2.35, -3.35, 0]),
        )
        self.play(FadeOut(result), FadeIn(comparison), run_time=.85)
        self.play(Indicate(VGroup(comparison[-2], comparison[-1]),
                           color=GREEN, scale_factor=1.08), run_time=.75)
        self.stage = comparison
        self.to(55)

        # 55–62 s: representation uniformity is not execution optimization.
        self.text(
            "표현 통일과 계산 최적화는 다릅니다",
            "연산자의 종류는 하나로 줄었지만, node 수와 depth는 늘었습니다.\n어떤 graph가 잘 실행되는지는 별도의 문제입니다.",
            "표현 가능한가?  →  node 수?  →  실행하기 좋은 graph?",
        )
        tradeoff = VGroup(
            self.metric_card("연산자 종류", "1", BLUE).move_to([-2.45, .55, 0]),
            txt("≠", 46, PINK).move_to([0, .55, 0]),
            self.metric_card("graph 비용", "9 nodes · depth 8", GOLD).move_to([2.45, .55, 0]),
            txt("실제 효율 = 연산량 + 의존성 + 메모리 이동", 24, MUTED).move_to([0, -1.25, 0]),
        )
        self.play(FadeOut(comparison), FadeIn(tradeoff), run_time=.8)
        self.play(Indicate(tradeoff[1], color=PINK, scale_factor=1.25), run_time=.7)
        self.stage = tradeoff
        self.to(62)

        # 62–66 s: multiplication may have a different, not necessarily larger, topology.
        self.text(
            "다음은 곱셈 graph",
            "그렇다면 곱셈은 같은 EML만으로\n어떤 연결 구조를 만들게 될까요?",
            "NEXT  ·  x × y와 graph complexity",
        )
        teaser = VGroup(
            OperatorChip("x × y", PINK, width=2.0, height=1.05).move_to([-2.5, .4, 0]),
            Arrow([-1.25, .4, 0], [.15, .4, 0], buff=.08,
                  color=GOLD, stroke_width=3, tip_length=.15),
            EMLNode(width=1.45, height=.72, compact=True).move_to([1.1, 1.35, 0]),
            EMLNode(width=1.45, height=.72, compact=True).move_to([2.1, .05, 0]),
            EMLNode(width=1.45, height=.72, compact=True).move_to([.25, -.8, 0]),
            txt("?", 42, GOLD).move_to([3.2, .4, 0]),
        )
        self.play(FadeOut(tradeoff), FadeIn(teaser), run_time=.75)
        self.stage = teaser
        self.to(66)

    def make_add_tree(self):
        tree = ExpressionTree(ADD_TREE, width=7.0, level_gap=.82).scale(.72)
        # Give the two variable leaves persistent branch colors.
        self.find_leaf(tree, "x").set_color(BLUE)
        self.find_leaf(tree, "y").set_color(PINK)
        return tree

    def find_leaf(self, tree, value):
        for leaf in tree.leaves:
            if leaf[1].text == str(value):
                return leaf
        raise ValueError(f"Leaf not found: {value}")

    def dim_tree(self, tree):
        tree.edges.set_opacity(.12)
        tree.nodes.set_opacity(.14)
        tree.leaves.set_opacity(.18)

    def leaf(self, value, color):
        return VGroup(
            Circle(radius=.35, stroke_color=color, stroke_width=2,
                   fill_color="#12233A", fill_opacity=.95),
            txt(value, 26, color),
        )

    def make_add_graph(self, scale=1.0):
        x_leaf = self.leaf("x", BLUE).move_to([-2.2, -.65, 0])
        y_leaf = self.leaf("y", PINK).move_to([2.2, -.65, 0])
        node = VGroup(
            Circle(radius=.62, stroke_color=GOLD, stroke_width=2.5,
                   fill_color=GOLD, fill_opacity=.08),
            txt("+", 42, GOLD),
        ).move_to([0, .45, 0])
        output = OperatorChip("x + y", GREEN, width=2.2, height=.9).move_to([0, 2.35, 0])
        graph = VGroup(
            Arrow(x_leaf.get_top(), node.get_bottom() + LEFT * .18, buff=.08,
                  color=BLUE, stroke_width=3, tip_length=.15),
            Arrow(y_leaf.get_top(), node.get_bottom() + RIGHT * .18, buff=.08,
                  color=PINK, stroke_width=3, tip_length=.15),
            Arrow(node.get_top(), output.get_bottom(), buff=.08,
                  color=GREEN, stroke_width=3, tip_length=.15),
            x_leaf, y_leaf, node, output,
        ).scale(scale)
        graph.node = node
        graph.output = output
        return graph

    def result_badge(self, text, color):
        label = txt(text, 20, color, 2.6)
        box = RoundedRectangle(width=max(1.65, label.width + .3), height=.52,
                               corner_radius=.1, stroke_color=color,
                               fill_color="#12233A", fill_opacity=.96,
                               stroke_width=1.4)
        return VGroup(box, label)

    def formula_row(self, text, color):
        dot = Dot(radius=.055, color=color)
        label = txt(text, 23, color, 3.85)
        return VGroup(dot, label).arrange(RIGHT, buff=.18)

    def metric_card(self, title, value, color):
        box = RoundedRectangle(width=3.3, height=2.15, corner_radius=.15,
                               stroke_color=color, fill_color=color,
                               fill_opacity=.07, stroke_width=1.7)
        return VGroup(
            box,
            txt(title, 23, color).move_to([0, .45, 0]),
            txt(value, 31, INK, 2.9).move_to([0, -.35, 0]),
        )

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
