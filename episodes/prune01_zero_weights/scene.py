"""Pruning 01: does setting a weight to zero remove the computation?"""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO,
    WeightMatrix, pill, txt, weight_connection,
)


class ZeroWeights(Scene):
    DURATION = 50
    DENSE = (
        (.82, .18, -.67, .41),
        (.03, -.91, .27, .06),
        (-.52, .74, -.01, -.83),
        (.12, -.38, .63, .02),
    )
    SPARSE_VALUES = (
        (.82, 0, -.67, .41),
        (0, -.91, .27, 0),
        (-.52, .74, 0, -.83),
        (0, -.38, .63, 0),
    )

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("PRUNING & SPARSITY  /  01", 20, MUTED).move_to(UP * 7.25),
            txt("Weight를 0으로 만들면 정말 빨라질까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s — begin with one neuron and five weighted connections.
        self.text(
            "이 연결들이 정말 전부 필요할까요?",
            "신경망의 연결에는 각각 Weight가 있습니다.",
            "하나의 출력에 모이는 5개의 연결",
        )
        inputs, output, connections, labels = self.network()
        network = VGroup(inputs, output, connections, labels)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * .12) for n in inputs],
                              lag_ratio=.1), run_time=.65)
        self.play(FadeIn(output, scale=.65), run_time=.35)
        self.play(LaggedStart(*[
            AnimationGroup(Create(c[0]), FadeIn(c[1], shift=RIGHT * .08),
                           lag_ratio=.28)
            for c in connections
        ], lag_ratio=.13), run_time=1.35)
        self.keep_stage(network)
        self.to(6)

        # 6–12 s — separate large weights from near-zero weights.
        self.text(
            "모든 Weight의 영향이 같지는 않습니다",
            "어떤 Weight는 큰 영향을 주지만,\n어떤 Weight는 거의 0에 가깝습니다.",
            "0.03   ·   −0.01",
        )
        self.play(*[
            connections[i].animate.set_opacity(.23)
            for i in (0, 2, 4)
        ], run_time=.45)
        self.play(
            Indicate(connections[1], color=PRUNE, scale_factor=1.1),
            Indicate(connections[3], color=PRUNE, scale_factor=1.1),
            run_time=.9,
        )
        small_tag = pill("거의 0", PRUNE, 2.0).move_to([0, -2.25, 0])
        self.play(FadeIn(small_tag, shift=UP * .12), run_time=.45)
        self.keep_stage(network, small_tag)
        self.to(12)

        # 12–21 s — make the small values exactly zero and remove their edges.
        self.text(
            "작은 Weight를 아예 0으로 만듭니다",
            "영향이 작은 연결을 제거하는 이 과정을\nPruning이라고 합니다.",
            "0.03 → 0        −0.01 → 0",
        )
        zero_a = txt("0", 23, PRUNE).move_to(connections[1][1])
        zero_b = txt("0", 23, PRUNE).move_to(connections[3][1])
        self.play(Transform(connections[1][1], zero_a),
                  Transform(connections[3][1], zero_b), run_time=.65)
        self.play(
            Uncreate(connections[1][0]), Uncreate(connections[3][0]),
            FadeOut(connections[1][1], scale=.7),
            FadeOut(connections[3][1], scale=.7),
            *[connections[i].animate.set_opacity(1) for i in (0, 2, 4)],
            run_time=.85,
        )
        prune_tag = pill("PRUNING", PRUNE, 2.35).move_to([0, -2.2, 0])
        self.play(ReplacementTransform(small_tag, prune_tag), run_time=.45)
        self.keep_stage(network, prune_tag)
        self.to(21)

        # 21–33 s — reveal the same idea as a dense-to-sparse matrix change.
        self.text(
            "행렬로 보면 변화가 더 선명합니다",
            "빽빽했던 Weight 행렬에서\n일부 값이 0으로 바뀝니다.",
            "DENSE                     SPARSE",
        )
        dense = WeightMatrix(self.DENSE, 1.03).move_to([0, .25, 0])
        dense_label = pill("DENSE", WEIGHT, 2.0).next_to(dense, UP, buff=.48)
        dense_stage = VGroup(dense, dense_label)
        self.play(FadeOut(network), FadeOut(prune_tag), FadeIn(dense_stage), run_time=.7)
        self.play(LaggedStart(*[
            Indicate(item, color=PRUNE, scale_factor=1.12)
            for i, item in enumerate(dense.entries) if i in (1, 4, 7, 10, 12, 15)
        ], lag_ratio=.08), run_time=.9)
        sparse = WeightMatrix(self.SPARSE_VALUES, 1.03).move_to(dense)
        sparse_label = pill("SPARSE", SPARSE, 2.15).move_to(dense_label)
        sparse_stage = VGroup(sparse, sparse_label)
        self.play(FadeTransform(dense_stage, sparse_stage), run_time=1.15)
        self.play(Indicate(sparse.zeros, color=SPARSE, scale_factor=1.03), run_time=.75)
        self.keep_stage(sparse_stage)
        self.to(33)

        # 33–39.5 s — focus on the arithmetic identity behind the intuition.
        self.text(
            "0인 Weight의 곱셈 결과는 항상 0입니다",
            "입력값이 무엇이든 결과는 달라지지 않습니다.",
            "x × 0 = 0",
        )
        equation = VGroup(
            txt("x", 62, WEIGHT), txt("×", 50, MUTED),
            txt("0", 62, PRUNE), txt("=", 50, MUTED), txt("0", 62, PRUNE),
        ).arrange(RIGHT, buff=.38).move_to([0, .35, 0])
        input_examples = VGroup(
            txt("2.1", 22, WEIGHT), txt("−0.7", 22, WEIGHT),
            txt("19", 22, WEIGHT), txt("…", 22, MUTED),
        ).arrange(RIGHT, buff=.55).move_to([0, 1.75, 0])
        brace = Brace(input_examples, DOWN, color=MUTED)
        arithmetic = VGroup(equation, input_examples, brace)
        self.play(FadeOut(sparse_stage), FadeIn(input_examples, shift=DOWN * .1),
                  GrowFromCenter(brace), run_time=.6)
        self.play(LaggedStart(*[FadeIn(x, scale=.7) for x in equation], lag_ratio=.11),
                  run_time=1.0)
        self.play(Flash(equation[-1], color=PRUNE, flash_radius=.55),
                  Indicate(equation[2], color=PRUNE, scale_factor=1.18),
                  Indicate(equation[4], color=PRUNE, scale_factor=1.18), run_time=.8)
        self.keep_stage(arithmetic)
        self.to(39.5)

        # 39.5–46 s — visually remove zero multiplications, but phrase it as a question.
        self.text(
            "그렇다면 이 계산은 건너뛸 수 있지 않을까요?",
            "0인 Weight가 많아질수록\n필요한 곱셈도 줄어드는 것처럼 보입니다.",
            "0 곱셈을 지우면  →  남은 계산만 실행?",
        )
        values = (.8, 0, -.7, 0, .6, 0, -.5, 0)
        chips = VGroup()
        for i, value in enumerate(values):
            color = ZERO if value == 0 else WEIGHT
            box = RoundedRectangle(width=.78, height=.72, corner_radius=.12,
                                   stroke_color=color, stroke_width=1.4,
                                   fill_color=color, fill_opacity=.08)
            label = txt("× 0" if value == 0 else f"× {value:g}", 19,
                        color, .65)
            chips.add(VGroup(box, label))
        chips.arrange_in_grid(2, 4, buff=(.22, .34)).move_to([0, .4, 0])
        skip_tag = pill("SKIP?", ACCENT, 1.9).move_to([0, -1.65, 0])
        self.play(FadeOut(arithmetic), LaggedStart(*[FadeIn(c) for c in chips],
                                                   lag_ratio=.06), run_time=.75)
        self.play(
            *[chips[i].animate.set_opacity(.12).scale(.9) for i in (1, 3, 5, 7)],
            *[chips[i].animate.set_color(GOOD) for i in (0, 2, 4, 6)],
            run_time=.8,
        )
        self.play(FadeIn(skip_tag, shift=UP * .12), run_time=.4)
        self.keep_stage(chips, skip_tag)
        self.to(46)

        # 46–50 s — finish on the tempting but unproven 10x speedup claim.
        self.text(
            "Weight의 90%를 지우면",
            "계산량은 크게 줄어듭니다.\n그렇다면 실행시간도 같게 줄어들까요?",
            "90% PRUNED       FLOPs ↓",
        )
        grid = VGroup()
        for i in range(100):
            alive = i in (2, 13, 25, 37, 41, 58, 64, 76, 89, 95)
            color = GOOD if alive else ZERO
            grid.add(Square(.25, stroke_width=.5, stroke_color=color,
                            fill_color=color, fill_opacity=.9 if alive else .13))
        grid.arrange_in_grid(10, 10, buff=.055).move_to([0, 1.05, 0])
        pruned = txt("90% PRUNED", 27, PRUNE).move_to([0, -1.0, 0])
        down = txt("↓", 36, ACCENT).move_to([0, -1.66, 0])
        question = txt("10× FASTER?", 42, ACCENT, weight=BOLD).move_to([0, -2.65, 0])
        self.play(FadeOut(chips), FadeOut(skip_tag), FadeIn(grid, scale=.95),
                  FadeIn(pruned), run_time=.8)
        self.play(FadeIn(down, shift=DOWN * .08),
                  FadeIn(question, shift=UP * .18), run_time=.7)
        self.play(Indicate(question, color=ACCENT, scale_factor=1.08), run_time=.7)
        self.keep_stage(grid, pruned, down, question)
        self.to(50)

    def network(self):
        ys = (2.0, 1.0, 0.0, -1.0, -2.0)
        values = (.82, .03, -.61, -.01, .74)
        inputs = VGroup(*[
            VGroup(Circle(.28, stroke_color=WEIGHT, stroke_width=2,
                          fill_color=WEIGHT, fill_opacity=.12),
                   txt(f"x{i + 1}", 19, WEIGHT)).move_to([-3.05, y, 0])
            for i, y in enumerate(ys)
        ])
        output = VGroup(
            Circle(.43, stroke_color=ACCENT, stroke_width=2.5,
                   fill_color=ACCENT, fill_opacity=.12),
            txt("y", 25, ACCENT),
        ).move_to([3.05, 0, 0])
        connections = VGroup(*[
            weight_connection(inputs[i].get_right(), output.get_left(), value)
            for i, value in enumerate(values)
        ])
        labels = VGroup(
            txt("inputs", 20, MUTED).move_to([-3.05, -2.75, 0]),
            txt("output", 20, MUTED).move_to([3.05, -.85, 0]),
        )
        return inputs, output, connections, labels

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 22, ACCENT).move_to(DOWN * 4.72)
        self.sub = txt(sub, 27).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.35)

    def keep_stage(self, *allowed):
        roots = (self.chrome, self.progress, self.head, self.note, self.sub, *allowed)
        keep = set()
        for root in roots:
            keep.update(root.get_family())
        for mob in list(self.mobjects):
            if mob not in keep:
                self.remove(mob)

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.35, 0]), run_time=min(.28, remain))
            self.wait(max(0, target - self.time))
