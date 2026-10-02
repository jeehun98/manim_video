"""GPU operations 09: ReLU is cheap; moving its data may not be."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=2.7, height=.85, size=25):
    box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.1)
    return VGroup(box, label(value, size, color, width - .18))


def arrow(start, end, color=MUTED):
    return Arrow(start, end, buff=.05, color=color, stroke_width=2.7,
                 tip_length=.14)


def row(values, color=WEIGHT, width=1.12, size=25):
    group = VGroup(*[card(str(v), color, width, .84, size) for v in values])
    group.arrange(RIGHT, buff=.18)
    return group


class GPUReLUMemoryFusion(Scene):
    DURATION = 87

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  09", 20, MUTED).move_to(UP * 7.3),
            label("ReLU는 GPU에서 어떻게 계산될까?", 31)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–8: define ReLU quickly, then move past its elementary math.
        self.copy("음수는 0, 양수는 그대로", "ReLU(x) = max(0, x)")
        formula = label("ReLU(x) = max(0, x)", 38, INK)
        formula.move_to([0, 3.15, 0])
        axes = VGroup(
            Line([-2.55, -.05, 0], [2.55, -.05, 0],
                 color=MUTED, stroke_width=2),
            Line([0, -1.25, 0], [0, 1.45, 0],
                 color=MUTED, stroke_width=2),
            Line([-2.35, -.05, 0], [0, -.05, 0],
                 color=PRUNE, stroke_width=5),
            Line([0, -.05, 0], [2.2, 1.35, 0],
                 color=GOOD, stroke_width=5),
        ).move_to([0, .58, 0])
        inp = row((-2, 1, -5, 3), WEIGHT).move_to([0, -1.85, 0])
        out = row((0, 1, 0, 3), GOOD).move_to([0, -3.0, 0])
        self.show(VGroup(formula, axes, inp, out))
        self.to(8)

        # 8–15: each output depends only on its corresponding input.
        self.copy("각 원소는 서로를 볼 필요가 없습니다", "yᵢ = max(0, xᵢ)")
        top = row(("x₀", "x₁", "x₂", "x₃"), WEIGHT, 1.35, 26)
        bottom = row(("y₀", "y₁", "y₂", "y₃"), GOOD, 1.35, 26)
        top.move_to([0, 1.6, 0]); bottom.move_to([0, -1.2, 0])
        links = VGroup(*[arrow(top[i].get_bottom(), bottom[i].get_top(), GOOD)
                         for i in range(4)])
        self.show(VGroup(top, bottom, links,
                         label("다른 x의 값은 필요 없음", 25, ACCENT)
                         .move_to([0, -2.9, 0])))
        self.to(15)

        # 15–25: threads can each handle one or more elements.
        self.copy("여러 Thread가 같은 연산을 적용", "원소별 독립 계산")
        threads = row(("T₀", "T₁", "T₂", "T₃"), ACCENT, 1.35, 25)
        inp = row((-2, 1, -5, 3), WEIGHT, 1.35, 26)
        out = row((0, 1, 0, 3), GOOD, 1.35, 26)
        threads.move_to([0, 2.45, 0]); inp.move_to([0, .4, 0])
        out.move_to([0, -1.65, 0])
        links = VGroup(*[arrow(threads[i].get_bottom(), inp[i].get_top(),
                               WEIGHT) for i in range(4)],
                       *[arrow(inp[i].get_bottom(), out[i].get_top(),
                               GOOD) for i in range(4)])
        self.show(VGroup(threads, inp, out, links,
                         label("한 Thread가 여러 원소를 맡을 수도 있음",
                               21, MUTED).move_to([0, -3.2, 0])))
        self.to(25)

        # 25–32: the arithmetic is tiny.
        self.copy("Thread 안의 계산은 작습니다", "값 하나를 0과 비교")
        thread = card("Thread", WEIGHT, 5.0, 2.7, 32)
        thread.move_to([0, .7, 0])
        math = label("y = max(0, x)", 38, GOOD)
        math.move_to([0, .1, 0])
        gauge_label = label("Compute", 23, MUTED).move_to([-2.3, -2.35, 0])
        gauge = Rectangle(width=3.1, height=.36, stroke_color=MUTED,
                          stroke_width=1.5).move_to([1.0, -2.35, 0])
        fill = Rectangle(width=.5, height=.31, stroke_width=0,
                         fill_color=GOOD, fill_opacity=.9)
        fill.move_to([-.3, -2.35, 0])
        self.show(VGroup(thread, math, gauge_label, gauge, fill))
        self.to(32)

        # 32–41: a separate kernel must read and write a tensor.
        self.copy("값은 먼저 읽고, 다시 저장합니다", "Read  →  ReLU  →  Write")
        memory = card("Global Memory", WEIGHT, 2.6, 1.65, 26)
        compute = card("SM Compute\nReLU", GOOD, 2.6, 1.65, 25)
        memory.move_to([-2.15, .6, 0]); compute.move_to([2.15, .6, 0])
        read = arrow(memory.get_top() + RIGHT * .45,
                     compute.get_top() + LEFT * .45, ACCENT)
        write = arrow(compute.get_bottom() + LEFT * .45,
                      memory.get_bottom() + RIGHT * .45, SPARSE)
        traffic = card("Read  →  ReLU  →  Write", ACCENT,
                       6.3, .9, 27).move_to([0, -2.55, 0])
        self.show(VGroup(memory, compute, read, write, traffic,
                         label("x", 22, ACCENT).move_to([0, 1.8, 0]),
                         label("y", 22, SPARSE).move_to([0, -.65, 0])))
        self.to(41)

        # 41–50: conceptual relative work, not measured performance.
        self.copy("큰 Tensor에서는 이동이 병목일 수 있습니다", "Memory-bound가 될 수 있음")
        bars = VGroup(
            label("Compute", 23, GOOD).move_to([-2.65, 1.6, 0]),
            Rectangle(width=.65, height=.55, fill_color=GOOD,
                      fill_opacity=.85, stroke_width=0).move_to([-.65, 1.6, 0]),
            label("Memory Traffic", 23, ACCENT)
            .move_to([-2.25, -.1, 0]),
            Rectangle(width=4.2, height=.55, fill_color=ACCENT,
                      fill_opacity=.85, stroke_width=0).move_to([1.15, -.1, 0]),
            label("개념도 · 측정값 아님", 21, MUTED)
            .move_to([0, -2.3, 0]),
            label("수많은 원소에 같은 Read / Write", 23, INK)
            .move_to([0, -3.0, 0]),
        )
        self.show(bars)
        self.to(50)

        # 50–60: separate MatMul and ReLU materialize Y.
        self.copy("MatMul 뒤에 별도 ReLU가 있다면", "중간 Y를 쓰고 다시 읽습니다")
        blocks = VGroup(
            card("MatMul", WEIGHT, 2.5, .75, 25),
            card("Write Y", PRUNE, 2.5, .75, 25),
            card("Global Memory", ACCENT, 3.6, .75, 24),
            card("Read Y", PRUNE, 2.5, .75, 25),
            card("ReLU", GOOD, 2.5, .75, 25),
        ).arrange(DOWN, buff=.35).move_to([0, 0, 0])
        links = VGroup(*[arrow(blocks[i].get_bottom(),
                               blocks[i+1].get_top()) for i in range(4)])
        self.show(VGroup(blocks, links,
                         label("중간 결과 Y의 Write → Read", 22, PRUNE)
                         .move_to([0, -3.2, 0])))
        self.to(60)

        # 60–69: keep the output fragment live and apply ReLU in the epilogue.
        self.copy("값이 아직 실행 중인 타일에 있다면", "ReLU 후 최종 결과만 저장")
        fragment = card("MatMul output fragment", WEIGHT,
                        5.6, .8, 22).move_to([0, 2.0, 0])
        relu = card("ReLU on fragment", GOOD,
                    5.6, .8, 22).move_to([0, .35, 0])
        live = SurroundingRectangle(VGroup(fragment, relu), color=SPARSE,
                                    buff=.3, corner_radius=.18)
        store = card("Write final Z", ACCENT, 4.1, .8, 25)
        store.move_to([0, -2.2, 0])
        self.show(VGroup(fragment, relu, live, store,
                         arrow(fragment.get_bottom(), relu.get_top(), GOOD),
                         arrow(relu.get_bottom(), store.get_top(), ACCENT),
                         label("on-chip  ·  구현이 지원할 때", 20, MUTED)
                         .move_to([0, -3.3, 0])))
        self.to(69)

        # 69–78: explicitly compare the memory movements.
        self.copy("Fusion은 중간 왕복을 피합니다", "최종 Write는 그대로 남습니다")
        sep = VGroup(
            label("SEPARATE", 23, PRUNE),
            card("MatMul", WEIGHT, 1.33, .68, 19),
            card("Write Y", PRUNE, 1.33, .68, 19),
            card("Read Y", PRUNE, 1.33, .68, 19),
            card("ReLU", GOOD, 1.33, .68, 19),
            card("Write Z", ACCENT, 1.33, .68, 19),
        )
        sep[1:].arrange(RIGHT, buff=.14).move_to([0, 1.5, 0])
        sep[0].move_to([0, 2.5, 0])
        fused = VGroup(
            label("FUSED", 23, GOOD),
            card("MatMul", WEIGHT, 2.0, .72, 22),
            card("ReLU", GOOD, 2.0, .72, 22),
            card("Write Z", ACCENT, 2.0, .72, 22),
        )
        fused[1:].arrange(RIGHT, buff=.35).move_to([0, -1.65, 0])
        fused[0].move_to([0, -.65, 0])
        removed = SurroundingRectangle(VGroup(sep[2], sep[3]),
                                       color=PRUNE, buff=.12,
                                       corner_radius=.1)
        self.show(VGroup(sep, fused, removed,
                         label("중간 Y의 materialization 제거 가능", 21, PRUNE)
                         .move_to([0, -3.0, 0])))
        self.to(78)

        # 78–87: same mathematics, different execution cost.
        self.copy("같은 수식, 다른 실행 비용", "어디서 읽고 어디에 저장하는가")
        formula = card("ReLU(x) = max(0, x)", GOOD,
                       6.1, 1.1, 32).move_to([0, 2.1, 0])
        math = label("수식은 그대로", 27, INK).move_to([0, .6, 0])
        cost = card("Data movement matters", ACCENT,
                    6.3, 1.0, 29).move_to([0, -1.55, 0])
        self.show(VGroup(formula, math, cost,
                         arrow(math.get_bottom(), cost.get_top(), ACCENT)))
        self.to(87)

    def copy(self, heading, note):
        old = VGroup(self.heading, self.note)
        if len(old):
            self.play(FadeOut(old), run_time=.15)
        self.heading = label(heading, 30).move_to(UP * 5.12)
        self.note = label(note, 22, ACCENT).move_to(DOWN * 4.8)
        self.play(FadeIn(self.heading), FadeIn(self.note), run_time=.32)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.3)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.65)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
