"""Quantization 11 finale: what extreme quantization loses and leaves behind."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class BinaryTernaryNetworks(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  11  ·  PART I FINALE", 19, MUTED).move_to(UP * 7.25),
            txt("1비트까지 줄이면 무엇을 잃고, 무엇이 남을까?", 30).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — begin with the semantic question, not the bit count.
        self.text(
            "모든 연결의 정확한 크기가 정말 필요할까?",
            "일반 신경망의 weight는 feature를 얼마나 강하게, 어느 방향으로\n반영할지 하나의 실수에 함께 기록합니다.",
            "continuous weight  =  magnitude  +  direction",
        )
        features = VGroup(*[
            self.feature_row(name, weight, color)
            for name, weight, color in (
                ("FEATURE A", "0.17", VALUE),
                ("FEATURE B", "1.42", GOOD),
                ("FEATURE C", "−0.63", ERROR),
                ("FEATURE D", "0.04", GRID),
            )
        ]).arrange(DOWN, buff=.22, aligned_edge=LEFT).move_to([-1.05, .35, 0])
        neuron = self.node("Σ", SNAP).move_to([3.0, .35, 0])
        links = VGroup(*[
            Line(row.get_right(), neuron.get_left(), color=row[1].get_color(),
                 stroke_width=1.6 + 3.1 * strength)
            for row, strength in zip(features, (.12, 1.0, .44, .04))
        ])
        precise = VGroup(features, neuron, links)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * .08) for r in features],
                              lag_ratio=.07), FadeIn(neuron), run_time=.7)
        self.play(LaggedStart(*[Create(line) for line in links], lag_ratio=.07),
                  run_time=.55)
        self.keep_stage(precise)
        self.play(Indicate(features, color=SNAP, scale_factor=1.03), run_time=.65)
        self.to(7)

        # 7–14 s — extreme quantization discards magnitude and preserves choices.
        self.text(
            "극단적으로 줄이면 강도 정보부터 사라집니다",
            "Binary weight에는 −1과 +1만 남아 연결을 같은 방향으로 쓸지,\n반대 방향으로 쓸지만 선택합니다.",
            "w ∈ { −1, +1 }       magnitude ✕       direction ✓",
        )
        axis = Line([-3.15, .15, 0], [3.15, .15, 0], color=MUTED, stroke_width=2.3)
        minus = self.state_marker(axis.get_start(), "−1", ERROR)
        plus = self.state_marker(axis.get_end(), "+1", GOOD)
        props = (.08, .23, .36, .62, .76, .91)
        dots = VGroup(*[
            Dot(axis.point_from_proportion(p) + UP * (1.0 + .24 * (i % 2)),
                radius=.1, color=VALUE) for i, p in enumerate(props)
        ])
        ghosts = dots.copy().set_opacity(.18)
        targets = (axis.get_start(), axis.get_start(), axis.get_start(),
                   axis.get_end(), axis.get_end(), axis.get_end())
        arrows = VGroup(*[
            Arrow(dots[i].get_bottom(), targets[i] + UP * .13, buff=.04,
                  color=SNAP, stroke_width=1.7, tip_length=.075)
            for i in range(len(dots))
        ])
        meaning = VGroup(
            pill("−1 · REVERSE", ERROR, 2.05),
            pill("+1 · KEEP", GOOD, 1.8),
        ).arrange(RIGHT, buff=.55).move_to([0, -1.55, 0])
        binary = VGroup(axis, minus, plus, dots, ghosts, arrows, meaning)
        self.play(FadeOut(precise), Create(axis), FadeIn(minus), FadeIn(plus),
                  FadeIn(dots), run_time=.65)
        self.add(ghosts)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.05),
                  *[dots[i].animate.move_to(targets[i]) for i in range(len(dots))],
                  run_time=.85)
        self.play(FadeIn(meaning), run_time=.35)
        self.keep_stage(binary)
        self.to(14)

        # 14–22 s — activation-only compression versus a binary dot product.
        self.text(
            "Activation만 줄이는 것과 둘 다 줄이는 것은 다릅니다",
            "Activation만 binary면 다음 층에 전달되는 값이 단순해집니다.\nWeight까지 binary면 dot product의 곱셈 규칙 자체가 달라집니다.",
            "activation only  →  compressed signal       both binary  →  new dot product",
        )
        act_only = self.compare_mode(
            "ACTIVATION ONLY", "x ∈ {−1,+1}", "weight는 실수", VALUE)
        both = self.compare_mode(
            "WEIGHT + ACTIVATION", "w,x ∈ {−1,+1}", "곱셈도 bit 비교", SNAP)
        modes = VGroup(act_only, both).arrange(RIGHT, buff=.4).scale(.92)
        modes.move_to([0, .45, 0])
        transition = VGroup(
            pill("값 전달 단순화", VALUE, 2.25), txt("→", 28, MUTED),
            pill("핵심 연산 변화", SNAP, 2.25),
        ).arrange(RIGHT, buff=.28).move_to([0, -1.65, 0])
        mode_stage = VGroup(modes, transition)
        self.play(FadeOut(binary), FadeIn(modes), run_time=.7)
        self.play(FadeIn(transition, shift=UP * .08), run_time=.4)
        self.keep_stage(mode_stage)
        self.play(Indicate(both, color=SNAP, scale_factor=1.05), run_time=.65)
        self.to(22)

        # 22–32 s — XNOR asks whether two signs are equal.
        self.text(
            "둘 다 Binary면 곱셈은 같은 부호인지 묻습니다",
            "같은 부호의 곱은 +1, 다른 부호의 곱은 −1입니다.\n0과 1 bit로 바꾸면 이 판단을 XNOR 연산으로 표현할 수 있습니다.",
            "same sign  →  +1 / XNOR 1       different sign  →  −1 / XNOR 0",
        )
        truth = VGroup(
            self.truth_row("+1", "+1", "+1", "1", GOOD),
            self.truth_row("+1", "−1", "−1", "0", ERROR),
            self.truth_row("−1", "+1", "−1", "0", ERROR),
            self.truth_row("−1", "−1", "+1", "1", GOOD),
        ).arrange(DOWN, buff=.16).move_to([0, .45, 0])
        headers = VGroup(
            txt("w", 17, MUTED), txt("x", 17, MUTED), txt("w×x", 17, MUTED),
            txt("XNOR", 17, MUTED),
        )
        headers[0].move_to(truth[0][0].get_center() + UP * .62)
        headers[1].move_to(truth[0][2].get_center() + UP * .62)
        headers[2].move_to(truth[0][4].get_center() + UP * .62)
        headers[3].move_to(truth[0][6].get_center() + UP * .62)
        xnor_tag = pill("MULTIPLY  →  BITWISE XNOR", SNAP, 3.65).move_to([0, -1.85, 0])
        xnor = VGroup(truth, headers, xnor_tag)
        self.play(FadeOut(mode_stage), FadeIn(headers),
                  LaggedStart(*[FadeIn(r, shift=RIGHT * .06) for r in truth],
                              lag_ratio=.08), run_time=.8)
        self.play(FadeIn(xnor_tag), run_time=.35)
        self.keep_stage(xnor)
        self.play(Indicate(VGroup(*[row[6] for row in truth]), color=SNAP,
                           scale_factor=1.08), run_time=.7)
        self.to(32)

        # 32–41 s — the dot product becomes matches minus mismatches.
        self.text(
            "Dot Product는 같은 위치의 개수를 세는 문제가 됩니다",
            "네 위치 중 같은 부호가 2개, 다른 부호가 2개라면\n각 항의 합은 플러스 2 마이너스 2, 즉 0입니다.",
            "wᵀx  =  matches − mismatches  =  2 − 2  =  0",
        )
        w_row = self.bit_vector("w", ("+", "−", "+", "+"), SNAP)
        x_row = self.bit_vector("x", ("+", "+", "+", "−"), VALUE)
        labels = VGroup(*[
            pill(label, GOOD if label == "SAME" else ERROR, 1.05)
            for label in ("SAME", "DIFF", "SAME", "DIFF")
        ]).arrange(RIGHT, buff=.18)
        vectors = VGroup(w_row, x_row, labels).arrange(DOWN, buff=.36)
        vectors.move_to([0, .55, 0])
        matches = VGroup(
            pill("2 MATCHES", GOOD, 1.95), txt("−", 30, MUTED),
            pill("2 MISMATCHES", ERROR, 2.25), txt("= 0", 30, SNAP),
        ).arrange(RIGHT, buff=.25).scale(.9).move_to([0, -1.75, 0])
        count_stage = VGroup(vectors, matches)
        self.play(FadeOut(xnor), FadeIn(w_row), FadeIn(x_row), run_time=.55)
        self.play(LaggedStart(*[FadeIn(label, shift=UP * .06) for label in labels],
                              lag_ratio=.08), run_time=.55)
        self.play(FadeIn(matches), run_time=.4)
        self.keep_stage(count_stage)
        self.play(Indicate(matches, color=SNAP, scale_factor=1.05), run_time=.65)
        self.to(41)

        # 41–49 s — ternary weights are add, subtract, or ignore commands.
        self.text(
            "Ternary Weight는 연결을 세 가지 명령으로 바꿉니다",
            "+1이면 feature를 더하고, −1이면 빼고, 0이면 무시합니다.\n강도를 정밀하게 조절하는 대신 방향과 선택만 남깁니다.",
            "+1  →  ADD x          −1  →  SUBTRACT x          0  →  IGNORE",
        )
        commands = VGroup(
            self.command_card("+1", "ADD", "x", GOOD),
            self.command_card("−1", "SUBTRACT", "−x", ERROR),
            self.command_card("0", "IGNORE", "0", MUTED),
        ).arrange(RIGHT, buff=.3).scale(.92).move_to([0, .35, 0])
        code = VGroup(
            txt("neuron", 18, MUTED), txt("=", 23, MUTED),
            txt("x₁", 26, GOOD), txt("−", 25, MUTED), txt("x₂", 26, ERROR),
            txt("+", 25, MUTED), txt("0x₃", 26, MUTED),
            txt("+", 25, MUTED), txt("x₄", 26, GOOD),
        ).arrange(RIGHT, buff=.16).move_to([0, -1.65, 0])
        ternary = VGroup(commands, code)
        self.play(FadeOut(count_stage),
                  LaggedStart(*[FadeIn(c, shift=UP * .08) for c in commands],
                              lag_ratio=.1), run_time=.75)
        self.play(FadeIn(code), run_time=.4)
        self.keep_stage(ternary)
        self.play(Indicate(commands[2], color=MUTED, scale_factor=1.08), run_time=.65)
        self.to(49)

        # 49–56 s — visualize the semantic shift in connectivity.
        self.text(
            "정밀한 연결 강도가 관계의 방향과 선택으로 바뀝니다",
            "Binary는 반영과 반전을, Ternary는 여기에 무시를 더합니다.\n0 weight가 늘면 연결 기여가 사라져 sparsity도 생길 수 있습니다.",
            "magnitude-rich connections  →  direction / selection structure",
        )
        left = self.network_panel(
            "CONTINUOUS", (("A", "0.17"), ("B", "1.42"),
                           ("C", "−0.63"), ("D", "0.04")), VALUE)
        right = self.network_panel(
            "TERNARY", (("A", "0"), ("B", "+1"),
                        ("C", "−1"), ("D", "0")), SNAP)
        panels = VGroup(left, txt("→", 34, MUTED), right)
        panels.arrange(RIGHT, buff=.35).scale(.9).move_to([0, .45, 0])
        meaning = VGroup(
            pill("B · ADD", GOOD, 1.55),
            pill("C · SUBTRACT", ERROR, 2.05),
            pill("A,D · IGNORE", MUTED, 2.0),
        ).arrange(RIGHT, buff=.22).scale(.88).move_to([0, -1.75, 0])
        structure = VGroup(panels, meaning)
        self.play(FadeOut(ternary), FadeIn(panels), run_time=.7)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * .06) for m in meaning],
                              lag_ratio=.08), run_time=.45)
        self.keep_stage(structure)
        self.play(Indicate(right, color=SNAP, scale_factor=1.04), run_time=.65)
        self.to(56)

        # 56–60 s — close Part I on the real computational significance.
        self.text(
            "1비트 신경망은 계산의 종류를 바꾸려는 시도입니다",
            "잃는 것은 연결의 정밀한 magnitude이고, 남는 것은 방향·선택과\nbit 비교로 바꿀 수 있는 새로운 dot product 구조입니다.",
            "LOSE: precise magnitude       KEEP: direction / selection       GAIN: bit operations",
        )
        losses = self.final_card("잃는 것", "정밀한 강도", ERROR)
        remains = self.final_card("남는 것", "방향 · 선택", SNAP)
        gains = self.final_card("바뀌는 계산", "XNOR · COUNT", GOOD)
        finale = VGroup(losses, remains, gains).arrange(RIGHT, buff=.32).scale(.92)
        finale.move_to([0, .3, 0])
        caveat = pill("real speed depends on kernels and hardware", MUTED, 4.5)
        caveat.move_to([0, -1.65, 0])
        final_stage = VGroup(finale, caveat)
        self.play(FadeOut(structure),
                  LaggedStart(*[FadeIn(c, shift=UP * .08) for c in finale],
                              lag_ratio=.08), run_time=.7)
        self.play(FadeIn(caveat), run_time=.3)
        self.keep_stage(final_stage)
        self.to(60)

    def feature_row(self, name, weight, color):
        feature = pill(name, color, 1.65)
        value = pill(weight, color, 1.15)
        return VGroup(feature, value).arrange(RIGHT, buff=.22)

    def node(self, label, color):
        circle = Circle(radius=.46, stroke_color=color, stroke_width=2,
                        fill_color=color, fill_opacity=.1)
        return VGroup(circle, txt(label, 23, color).move_to(circle))

    def state_marker(self, point, label, color):
        tick = Line(point + UP * .35, point + DOWN * .35,
                    color=color, stroke_width=4)
        return VGroup(tick, Dot(point, radius=.12, color=color),
                      txt(label, 24, color).next_to(point, DOWN, buff=.48))

    def compare_mode(self, title, formula, result, color):
        box = RoundedRectangle(width=3.7, height=2.75, corner_radius=.22,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06)
        return VGroup(
            box,
            txt(title, 19, color).move_to(box.get_center() + UP * .85),
            txt(formula, 23, INK).move_to(box.get_center() + UP * .08),
            txt(result, 20, color).move_to(box.get_center() + DOWN * .78),
        )

    def truth_row(self, w, x, product, bit, color):
        return VGroup(
            pill(w, SNAP, .9), txt("×", 19, MUTED),
            pill(x, VALUE, .9), txt("=", 19, MUTED),
            pill(product, color, .9), txt("→", 19, MUTED),
            pill(bit, color, .85),
        ).arrange(RIGHT, buff=.24)

    def bit_vector(self, name, signs, color):
        cells = VGroup(*[pill(sign, color, 1.0) for sign in signs])
        cells.arrange(RIGHT, buff=.18)
        return VGroup(txt(name, 24, color), cells).arrange(RIGHT, buff=.35)

    def command_card(self, state, command, result, color):
        box = RoundedRectangle(width=2.4, height=2.45, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06)
        return VGroup(
            box,
            txt(state, 34, color).move_to(box.get_center() + UP * .7),
            txt(command, 19, INK).move_to(box),
            txt(result, 26, color).move_to(box.get_center() + DOWN * .72),
        )

    def network_panel(self, title, rows, color):
        box = RoundedRectangle(width=3.35, height=3.15, corner_radius=.22,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.05)
        entries = VGroup(*[
            VGroup(txt(name, 19, INK), txt(weight, 21,
                   MUTED if weight == "0" else color)).arrange(RIGHT, buff=.8)
            for name, weight in rows
        ]).arrange(DOWN, buff=.25, aligned_edge=LEFT)
        entries.move_to(box.get_center() + DOWN * .2)
        return VGroup(box,
                      txt(title, 21, color).move_to(box.get_center() + UP * 1.15),
                      entries)

    def final_card(self, title, content, color):
        box = RoundedRectangle(width=2.4, height=2.25, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        return VGroup(
            box,
            txt(title, 20, color).move_to(box.get_center() + UP * .55),
            txt(content, 22, INK, 2.1).move_to(box.get_center() + DOWN * .48),
        )

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 22, SNAP).move_to(DOWN * 4.72)
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
