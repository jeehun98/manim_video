"""GPU operations 07: fuse reduction and elementwise phases of Softmax."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=2.7, height=.85, size=25, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.15,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .18))


def mini(value, color, width=1.35, height=.54, size=17):
    return card(value, color, width, height, size, .16)


def arrow(start, end, color=MUTED, width=2.7):
    return Arrow(start, end, buff=.06, color=color, stroke_width=width,
                 tip_length=.15)


class GPUSoftmaxFusion(Scene):
    DURATION = 90

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  07", 20, MUTED).move_to(UP * 7.3),
            label("Softmax는 왜 하나의 Kernel이 될 수 있을까?", 29)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–7: introduce a real operator mixing both patterns.
        self.copy(
            "Reduction과 원소별 계산이 함께 등장합니다", "ONE OPERATOR · MANY PHASES",
            "앞에서는 여러 값을 작은 상태로 축약했습니다.\n이번에는 두 구조가 함께 있는 Softmax를 보겠습니다.",
        )
        values = VGroup(*[
            mini(v, WEIGHT, 1.0, .7, 22) for v in ("1", "3", "2", "5")
        ]).arrange(RIGHT, buff=.22).move_to([-1.35, .5, 0])
        softmax = card("Softmax", SPARSE, 2.5, 1.05, 29).move_to([2.45, .5, 0])
        self.show(VGroup(values, softmax,
                         arrow(values.get_right(), softmax.get_left(), SPARSE)))
        self.to(7)

        # 7–15: unfold stable Softmax into its logical phases.
        self.copy(
            "Softmax를 계산 단계로 펼쳐봅시다", "stable Softmax",
            "최댓값을 찾고 빼고, 지수를 계산합니다.\n그 합을 구한 뒤 각 값을 합으로 나눕니다.",
        )
        flow = self.horizontal_flow(
            ("MAX", "SUB", "EXP", "SUM", "DIV"),
            (ACCENT, GOOD, WEIGHT, SPARSE, PRUNE),
            widths=(1.25, 1.25, 1.25, 1.25, 1.25), height=.72,
        ).move_to([0, .65, 0])
        kinds = VGroup(*[
            label(x, 16, c) for x, c in zip(
                ("REDUCE", "ELEMENT", "ELEMENT", "REDUCE", "ELEMENT"),
                (ACCENT, GOOD, GOOD, SPARSE, PRUNE))
        ]).arrange(RIGHT, buff=.38).move_to([0, -1.0, 0])
        formula = label("yᵢ = exp(xᵢ − m) / ℓ", 30, INK).move_to([0, 2.65, 0])
        self.show(VGroup(formula, flow, kinds))
        self.to(15)

        # 15–23: separate kernels materialize each phase.
        self.copy(
            "단계를 끊으면 경계마다 메모리를 왕복합니다", "KERNEL BOUNDARY = DATA BOUNDARY",
            "각 단계를 별도 Kernel로 실행하면 결과를 저장하고,\n다음 Kernel이 Global Memory에서 다시 읽습니다.",
        )
        kernels = VGroup(*[
            mini(x, c, 1.3, .62, 17) for x, c in zip(
                ("MAX", "SUB", "EXP", "SUM", "DIV"),
                (ACCENT, GOOD, WEIGHT, SPARSE, PRUNE))
        ]).arrange(RIGHT, buff=.22).move_to([0, 2.3, 0])
        stores = VGroup(*[
            mini("STORE\nLOAD", MUTED, 1.12, .8, 14) for _ in range(4)
        ])
        for i, item in enumerate(stores):
            item.move_to((kernels[i].get_right() + kernels[i + 1].get_left()) / 2 + DOWN * 2.0)
        links = VGroup()
        for i in range(4):
            links.add(arrow(kernels[i].get_bottom(), stores[i].get_top(), PRUNE, 1.7))
            links.add(arrow(stores[i].get_top() + DOWN * .02,
                            kernels[i + 1].get_bottom(), MUTED, 1.7))
        memory = label("Global Memory", 24, PRUNE).move_to([0, -.9, 0])
        self.show(VGroup(kernels, stores, links, memory))
        self.to(23)

        # 23–30: max reduces all inputs to one state.
        self.copy(
            "첫 Reduction은 입력을 m 하나로 축약합니다", "m = maxᵢ xᵢ",
            "최댓값 계산이 남겨야 할 상태는 입력의 복사본이 아니라\n현재까지 가장 큰 값 m입니다.",
        )
        xs = VGroup(*[
            mini(f"x{i}", WEIGHT, 1.0, .58, 19) for i in range(4)
        ]).arrange(RIGHT, buff=.38).move_to([0, 2.2, 0])
        reduce = card("MAX reduction", ACCENT, 3.5, .9, 26).move_to([0, .25, 0])
        m = card("m = 5", GOOD, 2.2, .95, 31).move_to([0, -2.0, 0])
        fan = VGroup(*[
            arrow(x.get_bottom(), reduce.get_top() + RIGHT * p, ACCENT, 1.8)
            for x, p in zip(xs, (-.9, -.3, .3, .9))
        ])
        self.show(VGroup(xs, reduce, m, fan,
                         arrow(reduce.get_bottom(), m.get_top(), GOOD)))
        self.to(30)

        # 30–37: m unlocks independent elementwise work.
        self.copy(
            "m이 정해지면 다시 원소별 계산입니다", "zᵢ = exp(xᵢ − m)",
            "각 원소는 같은 m을 빼고 지수를 취합니다.\n이 단계에서는 다른 원소의 결과가 필요하지 않습니다.",
        )
        rows = VGroup()
        for i, value in enumerate(("1", "3", "2", "5")):
            row = self.horizontal_flow(
                (f"x{i}={value}", "− m", "exp", f"z{i}"),
                (WEIGHT, GOOD, ACCENT, SPARSE),
                widths=(1.35, 1.15, 1.15, 1.15), height=.54,
            )
            rows.add(row)
        rows.arrange(DOWN, buff=.35).move_to([0, .55, 0])
        mtag = card("shared m", GOOD, 2.2, .65, 21).move_to([0, 3.3, 0])
        self.show(VGroup(rows, mtag))
        self.to(37)

        # 37–44: exponentials enter another reduction.
        self.copy(
            "지수값은 다시 합으로 축약됩니다", "ℓ = Σᵢ zᵢ",
            "원소별로 만든 zᵢ는 두 번째 Reduction에 들어갑니다.\n이번에 남겨야 할 작은 상태는 합 ℓ입니다.",
        )
        zs = VGroup(*[
            mini(f"z{i}", WEIGHT, 1.05, .6, 20) for i in range(4)
        ]).arrange(RIGHT, buff=.38).move_to([0, 2.25, 0])
        total = card("SUM reduction", SPARSE, 3.5, .9, 26).move_to([0, .25, 0])
        ell = card("ℓ = Σ zᵢ", ACCENT, 2.5, .95, 29).move_to([0, -2.0, 0])
        fan = VGroup(*[
            arrow(z.get_bottom(), total.get_top() + RIGHT * p, SPARSE, 1.8)
            for z, p in zip(zs, (-.9, -.3, .3, .9))
        ])
        self.show(VGroup(zs, total, ell, fan,
                         arrow(total.get_bottom(), ell.get_top(), ACCENT)))
        self.to(44)

        # 44–51: small reduction states do not replace per-element data.
        self.copy(
            "상태는 작아졌지만 원소별 정보도 필요합니다", "m, ℓ  +  per-element data",
            "Reduction 상태 m과 ℓ는 작습니다. 하지만 최종 출력은\n각 원소마다 zᵢ를 ℓ로 나누어 만들어야 합니다.",
        )
        state = VGroup(card("m", GOOD, 1.4, .9, 32),
                       card("ℓ", ACCENT, 1.4, .9, 32)).arrange(RIGHT, buff=.5)
        state.move_to([0, 2.25, 0])
        data = VGroup(*[
            mini(f"z{i}", WEIGHT, 1.05, .58, 20) for i in range(4)
        ]).arrange(RIGHT, buff=.35).move_to([0, .2, 0])
        outputs = VGroup(*[
            mini(f"y{i}", PRUNE, 1.05, .58, 20) for i in range(4)
        ]).arrange(RIGHT, buff=.35).move_to([0, -2.0, 0])
        links = VGroup(*[
            arrow(data[i].get_bottom(), outputs[i].get_top(), PRUNE, 1.8)
            for i in range(4)
        ])
        self.show(VGroup(state, data, outputs, links,
                         label("yᵢ = zᵢ / ℓ", 23, ACCENT).move_to([0, -3.15, 0])))
        self.to(51)

        # 51–59: one kernel keeps useful data on chip.
        self.copy(
            "한 Kernel 안에서 필요한 데이터만 이어갑니다", "NO FULL TENSOR BETWEEN PHASES",
            "논리적 단계는 그대로지만 Kernel 경계를 없앨 수 있습니다.\n상태와 값을 GPU 내부에 두고 다음 계산을 이어갑니다.",
        )
        border = RoundedRectangle(width=7.1, height=5.6, corner_radius=.28,
                                  stroke_color=GOOD, stroke_width=3,
                                  fill_color=GOOD, fill_opacity=.025)
        border.move_to([0, .25, 0])
        tag = label("Softmax Kernel", 24, GOOD).move_to([0, 3.3, 0])
        flow = self.horizontal_flow(
            ("MAX", "x−m\nEXP", "SUM", "÷ ℓ"),
            (ACCENT, WEIGHT, SPARSE, PRUNE),
            widths=(1.35, 1.75, 1.35, 1.35), height=.86,
        ).move_to([0, .4, 0])
        states = VGroup(mini("m", GOOD, 1.0), mini("ℓ", ACCENT, 1.0))
        states.arrange(RIGHT, buff=.35).move_to([0, -1.55, 0])
        self.show(VGroup(border, tag, flow, states))
        self.to(59)

        # 59–67: illustrate threads, warp reduction, and shared state.
        self.copy(
            "Thread들은 상태를 만들고 다시 사용합니다", "THREADS  ↔  WARP REDUCTION",
            "여러 Thread가 원소를 처리하고 Warp reduction으로 m을 만듭니다.\n그 m을 공유해 다음 원소별 계산을 계속합니다.",
        )
        threads = VGroup(*[
            mini(f"T{i}", WEIGHT, .85, .52, 16) for i in range(8)
        ]).arrange(RIGHT, buff=.1).move_to([0, 2.45, 0])
        warp = card("warp MAX", ACCENT, 3.0, .8, 24).move_to([0, .7, 0])
        m = card("m shared", GOOD, 2.3, .75, 23).move_to([0, -1.0, 0])
        next_op = card("xᵢ − m  →  exp", WEIGHT, 4.2, .8, 24).move_to([0, -2.65, 0])
        self.show(VGroup(threads, warp, m, next_op,
                         arrow(threads.get_bottom(), warp.get_top(), ACCENT),
                         arrow(warp.get_bottom(), m.get_top(), GOOD),
                         arrow(m.get_bottom(), next_op.get_top(), WEIGHT)))
        self.to(67)

        # 67–75: compare the three fusion patterns.
        self.copy(
            "세 편의 Fusion 구조를 비교해봅시다", "VALUE  ·  STATE  ·  ALTERNATION",
            "Epilogue는 값 하나를 유지하고, Reduction은 값을 축약합니다.\nSoftmax는 두 패턴을 번갈아 사용합니다.",
        )
        rows = VGroup(
            self.pattern_row("EPILOGUE", "value → element → element", GOOD),
            self.pattern_row("REDUCTION", "values → partial state", SPARSE),
            self.pattern_row("SOFTMAX", "reduce ↔ element ↔ reduce", ACCENT),
        ).arrange(DOWN, buff=.55).move_to([0, .35, 0])
        self.show(rows)
        self.to(75)

        # 75–83: the decisive question is what must survive each phase.
        self.copy(
            "Fusion은 Operator 개수로 결정되지 않습니다", "WHAT MUST SURVIVE?",
            "중요한 것은 각 단계가 다음 단계에 무엇을 넘기는가입니다.\n값인지, 작은 상태인지, 다시 필요한 원소 데이터인지 봐야 합니다.",
        )
        phases = self.horizontal_flow(
            ("ELEMENT", "REDUCE", "ELEMENT", "REDUCE", "ELEMENT"),
            (GOOD, ACCENT, WEIGHT, SPARSE, PRUNE),
            widths=(1.35, 1.25, 1.35, 1.25, 1.35), height=.66,
        ).move_to([0, 1.45, 0])
        question = card("next phase에 필요한 데이터는?", ACCENT, 5.5, 1.0, 27)
        question.move_to([0, -1.25, 0])
        tags = label("live values  ·  m  ·  ℓ  ·  reread", 22, MUTED)
        tags.move_to([0, -2.55, 0])
        self.show(VGroup(phases, question, tags))
        self.to(83)

        # 83–90: state the caveat and bridge to online Softmax.
        self.copy(
            "모든 중간 데이터가 사라지는 것은 아닙니다", "KEEP  ·  COMPRESS  ·  REREAD",
            "구현은 값을 register나 shared memory에 유지하거나 입력을 다시 읽습니다.\n무엇을 남길지 정하는 것이 Softmax Fusion의 핵심입니다.",
        )
        choices = VGroup(
            card("KEEP\nvalues on-chip", GOOD, 2.15, 1.25, 21),
            card("COMPRESS\nto m, ℓ", ACCENT, 2.15, 1.25, 21),
            card("REREAD\ninput", SPARSE, 2.15, 1.25, 21),
        ).arrange(RIGHT, buff=.32).move_to([0, 1.45, 0])
        finish = card("same Softmax output", PRUNE, 4.4, .95, 28).move_to([0, -1.2, 0])
        bridge = label("입력을 순차적으로 보며 상태를 갱신한다면?", 22, MUTED)
        bridge.move_to([0, -2.7, 0])
        links = VGroup(*[
            arrow(c.get_bottom(), finish.get_top() + RIGHT * p, PRUNE, 1.8)
            for c, p in zip(choices, (-1.0, 0, 1.0))
        ])
        self.show(VGroup(choices, finish, bridge, links))
        self.to(90)

    def pattern_row(self, title, body, color):
        left = card(title, color, 2.15, .72, 20)
        right = card(body, color, 4.4, .72, 20)
        row = VGroup(left, right).arrange(RIGHT, buff=.45)
        return VGroup(row, arrow(left.get_right(), right.get_left(), color, 1.8))

    def horizontal_flow(self, names, colors, widths=None, height=.82):
        if widths is None:
            widths = tuple(1.7 for _ in names)
        nodes = VGroup(*[
            card(n, c, w, height, 21, .12)
            for n, c, w in zip(names, colors, widths)
        ])
        nodes.arrange(RIGHT, buff=.32)
        links = VGroup(*[
            arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                  colors[i + 1], 2.0)
            for i in range(len(nodes) - 1)
        ])
        return VGroup(nodes, links)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 21, ACCENT).move_to(DOWN * 4.45)
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
