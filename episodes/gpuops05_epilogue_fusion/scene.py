"""GPU operations 05: elementwise dependencies enable GEMM epilogue fusion."""
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


def arrow(start, end, color=MUTED, width=2.7):
    return Arrow(start, end, buff=.06, color=color, stroke_width=width,
                 tip_length=.15)


def mini(value, color, width=1.35, height=.54, size=17):
    return card(value, color, width, height, size, .16)


def output_tile(rows=4, cols=4, highlight=(1, 2)):
    cells = VGroup()
    chosen = None
    for r in range(rows):
        for c in range(cols):
            active = (r, c) == highlight
            color = ACCENT if active else WEIGHT
            box = RoundedRectangle(
                width=.78, height=.66, corner_radius=.08,
                stroke_color=color, stroke_width=2 if active else 1.2,
                fill_color=color, fill_opacity=.2 if active else .06,
            )
            value = label(f"c{r}{c}", 17, color, .58)
            item = VGroup(box, value)
            cells.add(item)
            if active:
                chosen = item
    cells.arrange_in_grid(rows=rows, cols=cols, buff=(.13, .13))
    return cells, chosen


class GPUEpilogueFusion(Scene):
    DURATION = 112

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  05", 20, MUTED).move_to(UP * 7.3),
            label("행렬곱 뒤의 연산은 왜 합칠 수 있을까?", 30)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–11: introduce the expression, but do not start from memory traffic.
        self.copy(
            "한 줄의 수식 · 세 Operator", "Y = ReLU(XW + b)",
            "행렬곱 뒤에 Bias와 ReLU가 이어집니다.\n한 줄이지만 세 Operator로 나눠 볼 수 있습니다.",
        )
        formula = label("Y = ReLU(XW + b)", 44).move_to([0, 2.15, 0])
        ops = self.horizontal_flow(
            ("MatMul", "Bias", "ReLU"),
            (WEIGHT, ACCENT, GOOD),
            widths=(2.0, 1.65, 1.65),
        ).move_to([0, -.45, 0])
        self.show(VGroup(formula, ops))
        self.play(Indicate(formula, color=ACCENT, scale_factor=1.03), run_time=.7)
        self.to(11)

        # 11–20: zoom from the output tile to one representative element.
        self.copy(
            "GEMM이 만드는 출력의 일부", "화면에서는 cᵢⱼ 하나를 확대",
            "실제 Kernel은 출력 tile의 일부를 다룹니다.\n여기서는 dependency를 보기 위해 cᵢⱼ 하나를 확대합니다.",
        )
        gemm = card("GEMM", WEIGHT, 3.0, .9, 28).move_to([-2.4, 1.8, 0])
        tile, chosen = output_tile()
        tile.move_to([1.7, .55, 0])
        outline = SurroundingRectangle(tile, color=SPARSE, buff=.25,
                                       corner_radius=.18)
        zoom = card("cᵢⱼ", ACCENT, 2.25, 1.0, 33).move_to([-1.2, -2.35, 0])
        self.show(VGroup(gemm, tile, outline, zoom,
                         arrow(gemm.get_right(), outline.get_left(), WEIGHT),
                         arrow(chosen.get_bottom(), zoom.get_top(), ACCENT)))
        self.play(Indicate(chosen, color=ACCENT, scale_factor=1.12), run_time=.8)
        self.to(20)

        # 20–27: one output value is accumulated from FMAs.
        self.copy(
            "FMA가 누적되어 출력값이 됩니다", "aᵢₖ × bₖⱼ  +  accumulator",
            "곱셈과 덧셈이 반복됩니다.\nFMA의 누적 결과가 출력값 cᵢⱼ입니다.",
        )
        formula = label("cᵢⱼ = Σₖ Aᵢₖ Bₖⱼ", 37).move_to([0, 3.25, 0])
        fmas = VGroup(*[
            mini("FMA(aᵢ₀, b₀ⱼ)", WEIGHT, 3.15),
            mini("FMA(aᵢ₁, b₁ⱼ)", WEIGHT, 3.15),
            mini("FMA(aᵢ₂, b₂ⱼ)", WEIGHT, 3.15),
            mini("⋮", MUTED, 3.15),
        ]).arrange(DOWN, buff=.23).move_to([-1.75, .15, 0])
        accum = card("Accumulator", GOOD, 3.0, 1.05, 28).move_to([2.15, .15, 0])
        out = card("cᵢⱼ ready", ACCENT, 2.5, .82, 28).move_to([2.15, -2.3, 0])
        links = VGroup(*[
            arrow(x.get_right(), accum.get_left() + UP * (.34 - i * .22),
                  GOOD, 2.1)
            for i, x in enumerate(fmas)
        ], arrow(accum.get_bottom(), out.get_top(), GOOD))
        self.show(VGroup(formula, fmas, accum, out, links))
        self.play(Indicate(accum, color=GOOD, scale_factor=1.05), run_time=.7)
        self.to(27)

        # 27–38: avoid the false one-thread/one-register equivalence.
        self.copy(
            "실행 주체가 출력의 일부를 가지고 있습니다",
            "Thread / Warp  ·  accumulator fragments",
            "Thread 또는 Warp가 여러 출력 fragment를\naccumulator/register 상태로 보유할 수 있습니다.",
        )
        actor = card("Thread / Warp", SPARSE, 2.8, 1.0, 27).move_to([-2.65, .6, 0])
        fragments = VGroup(*[
            mini(x, c, 1.35, .68, 20) for x, c in
            zip(("cᵢⱼ", "cᵢⱼ₊₁", "cᵢ₊₁ⱼ", "…"),
                (ACCENT, WEIGHT, WEIGHT, MUTED))
        ]).arrange_in_grid(rows=2, cols=2, buff=(.35, .35)).move_to([1.55, .6, 0])
        bank = SurroundingRectangle(fragments, color=GOOD, buff=.4,
                                    corner_radius=.2)
        bank_tag = label("Accumulator / Register state", 20, GOOD)
        bank_tag.next_to(bank, UP, buff=.38)
        note = label("구현에 따라 fragment 배치는 달라짐", 19, MUTED)
        note.move_to([0, -2.35, 0])
        self.show(VGroup(actor, fragments, bank, bank_tag, note,
                         arrow(actor.get_right(), bank.get_left(), GOOD)))
        self.play(Indicate(fragments[0], color=ACCENT, scale_factor=1.08), run_time=.7)
        self.to(38)

        # 38–46: the value is still live; the store is only one possible next step.
        self.copy(
            "값은 아직 계산 주체의 손에 있습니다", "LIVE VALUE  ·  아직 STORE하지 않음",
            "cᵢⱼ는 아직 on-chip 상태로 살아 있습니다.\n지금 Global Memory에 저장할 필요는 없습니다.",
        )
        state = card("cᵢⱼ", ACCENT, 2.5, 1.0, 34).move_to([0, 2.35, 0])
        live = SurroundingRectangle(state, color=GOOD, buff=.42,
                                    corner_radius=.22)
        live_tag = label("LIVE", 22, GOOD).next_to(live, UP, buff=.28)
        store = card("STORE", PRUNE, 2.1, .75, 22).move_to([0, -1.0, 0])
        memory = card("Global Memory", SPARSE, 4.0, .9, 24).move_to([0, -2.9, 0])
        paused = DashedLine(state.get_bottom(), store.get_top(), color=PRUNE,
                            stroke_width=2.5, dash_length=.14)
        cross = VGroup(
            Line([-.55, -1.42, 0], [.55, -.58, 0], color=PRUNE, stroke_width=5),
            Line([-.55, -.58, 0], [.55, -1.42, 0], color=PRUNE, stroke_width=5),
        )
        self.show(VGroup(state, live, live_tag, store, memory, paused, cross,
                         arrow(store.get_bottom(), memory.get_top(), PRUNE)))
        self.to(46)

        # 46–54: bias depends on the current value and a directly indexed bias.
        self.copy(
            "Bias는 현재 값과 bⱼ만 필요", "다른 출력 원소 dependency 없음",
            "cᵢⱼ와 해당 열의 bⱼ만 있으면 됩니다.\n다른 출력 원소의 완성을 기다리지 않습니다.",
        )
        current = card("cᵢⱼ", ACCENT, 1.7, .8, 28).move_to([-2.5, 1.55, 0])
        bias = card("bⱼ", WEIGHT, 1.7, .8, 28).move_to([-2.5, -.25, 0])
        add = card("+", GOOD, 1.25, 1.05, 38).move_to([0, .65, 0])
        result = card("cᵢⱼ + bⱼ", GOOD, 2.75, .88, 27).move_to([2.45, .65, 0])
        others = VGroup(*[
            mini(x, ZERO, 1.2, .55, 18) for x in ("c₀₀", "c₀₁", "c₁₀")
        ]).arrange(RIGHT, buff=.28).move_to([0, -2.25, 0])
        self.show(VGroup(current, bias, add, result, others,
                         arrow(current.get_right(), add.get_left() + UP * .22, ACCENT),
                         arrow(bias.get_right(), add.get_left() + DOWN * .22, WEIGHT),
                         arrow(add.get_right(), result.get_left(), GOOD),
                         label("필요 없음", 19, MUTED).next_to(others, DOWN, buff=.35)))
        self.to(54)

        # 54–62: ReLU is a pure per-element decision.
        self.copy(
            "ReLU도 현재 값 하나만 봅니다", "yᵢⱼ = max(0, xᵢⱼ)",
            "현재 원소의 부호만 확인하면\nReLU 결과를 즉시 결정할 수 있습니다.",
        )
        value = card("xᵢⱼ", ACCENT, 1.8, .85, 29).move_to([-2.6, .65, 0])
        test = card("xᵢⱼ > 0 ?", WEIGHT, 2.35, .9, 27).move_to([0, .65, 0])
        result = card("max(0, xᵢⱼ)", GOOD, 2.7, .9, 27).move_to([2.65, .65, 0])
        single = VGroup(value, test, result,
                        arrow(value.get_right(), test.get_left(), WEIGHT),
                        arrow(test.get_right(), result.get_left(), GOOD))
        no_wait = label("다른 출력이 완성될 때까지 기다릴 필요 없음", 21, GOOD)
        no_wait.move_to([0, -1.65, 0])
        self.show(VGroup(single, no_wait))
        self.to(62)

        # 62–70: make the value lifetime the visual center.
        self.copy(
            "원소별 연산은 그대로 이어갈 수 있습니다", "KEEP THE VALUE LIVE",
            "같은 값을 놓지 않고 Bias와 ReLU에 전달합니다.\n원소별 dependency가 연속 실행을 가능하게 합니다.",
        )
        chain = self.horizontal_flow(
            ("cᵢⱼ", "+ bⱼ", "ReLU", "output"),
            (ACCENT, WEIGHT, GOOD, GOOD),
            widths=(1.35, 1.45, 1.55, 1.7), height=.74,
        ).move_to([0, .7, 0])
        frame = SurroundingRectangle(chain, color=GOOD, buff=.52,
                                     corner_radius=.24)
        tag = label("same live value", 22, GOOD).next_to(frame, UP, buff=.35)
        elementwise = card("ELEMENTWISE", SPARSE, 3.8, .8, 25).move_to([0, -2.15, 0])
        self.show(VGroup(chain, frame, tag, elementwise))
        self.play(Indicate(chain, color=GOOD, scale_factor=1.02), run_time=.8)
        self.to(70)

        # 70–79: only now show the consequence of separate kernels.
        self.copy(
            "값을 놓으면 다시 가져와야 합니다", "Fusion ×  ·  STORE / LOAD 반복",
            "Kernel을 나누면 중간값을 STORE하고\n다음 Kernel이 Global Memory에서 다시 LOAD합니다.",
        )
        names = ("cᵢⱼ", "STORE", "Global Memory", "LOAD",
                 "+ Bias", "STORE", "LOAD", "ReLU")
        colors = (ACCENT, PRUNE, SPARSE, WEIGHT, ACCENT, PRUNE, WEIGHT, GOOD)
        nodes = VGroup(*[
            mini(n, c, 3.1 if n == "Global Memory" else 2.25,
                 .52, 17)
            for n, c in zip(names, colors)
        ]).arrange(DOWN, buff=.17).move_to([0, -.05, 0])
        links = VGroup(*[
            arrow(nodes[i].get_bottom(), nodes[i + 1].get_top(),
                  colors[i + 1], 1.9)
            for i in range(len(nodes) - 1)
        ])
        self.show(VGroup(nodes, links))
        self.to(79)

        # 79–87: keeping the value live leaves one final store.
        self.copy(
            "값을 놓지 않고 끝까지 계산", "Fusion ○  ·  final STORE only",
            "현재 값에 Bias와 ReLU를 연속 적용합니다.\n모든 계산이 끝난 최종 결과만 저장합니다.",
        )
        chain = VGroup(
            card("cᵢⱼ", ACCENT, 2.4, .75, 27),
            card("+ bⱼ", WEIGHT, 2.4, .75, 27),
            card("ReLU", GOOD, 2.4, .75, 27),
            card("final STORE", PRUNE, 2.8, .75, 24),
        ).arrange(DOWN, buff=.55).move_to([0, .25, 0])
        links = VGroup(*[
            arrow(chain[i].get_bottom(), chain[i + 1].get_top(),
                  chain[i + 1][0].get_stroke_color())
            for i in range(3)
        ])
        memory = card("Global Memory", SPARSE, 3.8, .85, 23)
        memory.next_to(chain, DOWN, buff=.58)
        self.show(VGroup(chain, links, memory,
                         arrow(chain[-1].get_bottom(), memory.get_top(), PRUNE)))
        self.to(87)

        # 87–95: name the fused output stage.
        self.copy(
            "GEMM의 출력 단계에서 함께 처리", "EPILOGUE FUSION",
            "GEMM이 만든 fragment를 저장하기 전에\n후속 연산을 출력 단계에서 함께 처리합니다.",
        )
        accum = card("FMA accumulation", WEIGHT, 4.4, .85, 24).move_to([0, 2.65, 0])
        epilogue = self.horizontal_flow(
            ("fragment", "+ Bias", "ReLU"),
            (ACCENT, WEIGHT, GOOD),
            widths=(1.75, 1.6, 1.5), height=.7,
        ).move_to([0, .25, 0])
        ep_frame = SurroundingRectangle(epilogue, color=ACCENT, buff=.42,
                                        corner_radius=.2)
        ep_tag = label("EPILOGUE", 21, ACCENT).next_to(ep_frame, UP, buff=.25)
        store = card("final STORE", PRUNE, 3.0, .75, 22).move_to([0, -2.55, 0])
        kernel = SurroundingRectangle(VGroup(accum, ep_frame, ep_tag),
                                      color=SPARSE, buff=.35,
                                      corner_radius=.25)
        self.show(VGroup(accum, epilogue, ep_frame, ep_tag, store, kernel,
                         arrow(accum.get_bottom(), ep_frame.get_top(), GOOD),
                         arrow(ep_frame.get_bottom(), store.get_top(), PRUNE)))
        self.to(95)

        # 95–105: memory traffic reduction follows from extending lifetime.
        self.copy(
            "달라진 것은 중간값의 수명입니다",
            "keep live  →  no intermediate materialization",
            "수학적 연산은 그대로 남아 있습니다.\n값의 수명이 늘어나 중간 materialization이 사라집니다.",
        )
        left = VGroup(
            label("DROP & RELOAD", 20, PRUNE),
            mini("register", GOOD, 2.5),
            mini("STORE", PRUNE, 2.5),
            mini("memory", SPARSE, 2.5),
            mini("LOAD", WEIGHT, 2.5),
        ).arrange(DOWN, buff=.27).move_to([-2.1, .45, 0])
        right = VGroup(
            label("KEEP LIVE", 20, GOOD),
            mini("register", GOOD, 2.5),
            mini("+ Bias", WEIGHT, 2.5),
            mini("ReLU", GOOD, 2.5),
            mini("final STORE", PRUNE, 2.5),
        ).arrange(DOWN, buff=.27).move_to([2.1, .45, 0])
        divider = Line([0, 3.15, 0], [0, -3.15, 0], color=MUTED,
                       stroke_opacity=.3)
        result = label("Materialization 제거는 결과", 22, ACCENT)
        result.move_to([0, -3.35, 0])
        self.show(VGroup(left, right, divider, result))
        self.to(105)

        # 105–112: finish with the dependency question and a next-step hint.
        self.copy(
            "Fusion에서 먼저 물어볼 것", "현재 값만으로 다음 계산이 가능한가?",
            "원소별 연산은 한 값의 경로로 연결하기 쉽습니다.\n여러 출력의 관계가 필요하면 조건이 복잡해집니다.",
        )
        local = self.horizontal_flow(
            ("Add", "Scale", "ReLU", "Clamp"),
            (WEIGHT, ACCENT, GOOD, SPARSE),
            widths=(1.25, 1.4, 1.45, 1.55), height=.64,
        ).move_to([0, 2.25, 0])
        local_tag = label("one element · continuous path", 20, GOOD)
        local_tag.next_to(local, UP, buff=.42)
        values = VGroup(*[
            mini(x, WEIGHT, 1.0, .52, 17) for x in ("c₀₀", "c₀₁", "c₀₂", "c₀₃")
        ]).arrange(RIGHT, buff=.25).move_to([0, -.55, 0])
        multi = card("multi-output relation", SPARSE, 3.5, .82, 22)
        multi.move_to([0, -2.45, 0])
        fan = VGroup(*[
            arrow(v.get_bottom(), multi.get_top() + RIGHT * x, SPARSE, 1.8)
            for v, x in zip(values, (-.85, -.3, .3, .85))
        ])
        complex_note = label("여러 출력이 필요하면 조건이 복잡", 19, MUTED)
        complex_note.next_to(multi, DOWN, buff=.38)
        self.show(VGroup(local, local_tag, values, multi, fan, complex_note))
        self.to(112)

    def horizontal_flow(self, names, colors, widths=None, height=.82):
        if widths is None:
            widths = tuple(1.7 for _ in names)
        nodes = VGroup(*[
            card(n, c, w, height, 21, .12)
            for n, c, w in zip(names, colors, widths)
        ])
        nodes.arrange(RIGHT, buff=.46)
        links = VGroup(*[
            arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                  colors[i + 1], 2.2)
            for i in range(len(nodes) - 1)
        ])
        return VGroup(nodes, links)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.12)
        self.heading = label(heading, 30).move_to(UP * 5.12)
        self.note = label(note, 21, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2,
            fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note),
                  FadeIn(self.caption_box), FadeIn(self.caption), run_time=.25)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.22)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.5)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
