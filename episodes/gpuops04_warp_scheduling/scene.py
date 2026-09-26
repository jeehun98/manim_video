"""GPU operations 04: SIMT warps and hardware latency hiding."""
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
    return Arrow(start, end, buff=.06, color=color, stroke_width=2.7,
                 tip_length=.15)


def lane_grid(color=WEIGHT):
    cells = VGroup()
    for i in range(32):
        box = RoundedRectangle(width=.69, height=.5, corner_radius=.07,
                               stroke_color=color, stroke_width=1.25,
                               fill_color=color, fill_opacity=.11)
        cells.add(VGroup(box, label(str(i), 17, color, .5)))
    cells.arrange_in_grid(rows=4, cols=8, buff=(.11, .11))
    return cells


def bar(value, color, width=1.1, height=.45):
    box = RoundedRectangle(width=width, height=height, corner_radius=.07,
                           stroke_color=color, stroke_width=1,
                           fill_color=color, fill_opacity=.65)
    return VGroup(box, label(value, 16, INK, width - .1))


class GPUWarpScheduling(Scene):
    DURATION = 108

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  04", 20, MUTED).move_to(UP * 7.3),
            label("GPU는 코드를 어떤 순서로 실행할까?", 31)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–6: CUDA is written from a thread's point of view.
        self.copy("같은 Kernel, 다른 데이터", "Thread마다 자기 입력으로 실행")
        code = card("out[i] = a[i] * b[i] + c[i];", WEIGHT,
                    7.1, .9, 22).move_to([0, 2.1, 0])
        threads = VGroup(*[card(x, c, 1.25, .77, 20) for x, c in
                           zip(("T0", "T1", "T2", "...", "T31"),
                               (GOOD, GOOD, GOOD, MUTED, GOOD))])
        threads.arrange(RIGHT, buff=.28).move_to([0, -.65, 0])
        self.show(VGroup(code, threads,
                         arrow(code.get_bottom(), [0, .0, 0], ACCENT)))
        self.to(6)

        # 6–14: display all 32 lanes before naming the group.
        self.copy("Thread를 하나씩만 보지 않습니다", "연속된 32개 Thread")
        grid = lane_grid().move_to([0, -.15, 0])
        labels = VGroup(label("T0", 22, WEIGHT).next_to(grid, UP, buff=.36)
                        .align_to(grid, LEFT),
                        label("T31", 22, WEIGHT).next_to(grid, DOWN, buff=.36)
                        .align_to(grid, RIGHT))
        self.show(VGroup(grid, labels))
        self.to(14)

        # 14–23: group consecutive thread IDs into a warp.
        self.copy("32개 Thread가 하나의 Warp", "NVIDIA GPU  ·  WARP 0")
        grid = lane_grid(GOOD).move_to([0, -.3, 0])
        outline = SurroundingRectangle(grid, color=ACCENT,
                                       buff=.27, corner_radius=.2)
        tag = card("WARP 0", ACCENT, 2.7, .82, 26)
        tag.next_to(outline, UP, buff=.55)
        self.show(VGroup(grid, outline, tag,
                         label("32 active lanes in this example", 20, MUTED)
                         .next_to(outline, DOWN, buff=.52)))
        self.to(23)

        # 23–32: one common instruction, distinct data per active lane.
        self.copy("Warp에 공통 명령을 발행합니다", "활성 Thread는 각자 다른 값으로 계산")
        instruction = card("FMA instruction", GOOD, 4.25, .9, 28)
        instruction.move_to([0, 2.5, 0])
        grid = lane_grid(GOOD).move_to([0, -.45, 0])
        data = label("(a₀,b₀,c₀)     (a₁,b₁,c₁)       · · ·       (a₃₁,b₃₁,c₃₁)",
                     20, WEIGHT, 7.2).move_to([0, -2.8, 0])
        self.show(VGroup(instruction, grid, data,
                         arrow(instruction.get_bottom(), grid.get_top(), GOOD)))
        self.to(32)

        # 32–42: reconnect the FMA contraction from episode 1.
        self.copy("1화의 FMA를 실행 단위로 보면", "한 명령 · 여러 Thread의 데이터")
        source = card("a*b+c", WEIGHT, 2.9, .78, 28)
        source.move_to([-2.1, 2.45, 0])
        fma = card("FMA", GOOD, 2.5, .78, 28)
        fma.move_to([2.15, 2.45, 0])
        examples = VGroup(*[
            card("T0: a₀b₀+c₀", WEIGHT, 5.4, .68, 23),
            card("T1: a₁b₁+c₁", WEIGHT, 5.4, .68, 23),
            card("⋮", MUTED, 5.4, .5, 25),
            card("T31: a₃₁b₃₁+c₃₁", WEIGHT, 5.4, .68, 23),
        ]).arrange(DOWN, buff=.2).move_to([0, -.8, 0])
        self.show(VGroup(source, fma, examples,
                         arrow(source.get_right(), fma.get_left(), SPARSE),
                         arrow(fma.get_bottom(), examples.get_top(), GOOD)))
        self.to(42)

        # 42–51: a dependent FMA waits for a load from global memory.
        self.copy("Warp 0이 데이터를 기다립니다", "LOAD  →  data ready  →  FMA")
        flow = VGroup(
            card("LOAD", WEIGHT, 1.75, .78, 23),
            card("WAIT", PRUNE, 1.75, .78, 23),
            card("FMA", GOOD, 1.75, .78, 23),
            card("STORE", SPARSE, 1.75, .78, 23),
        ).arrange(RIGHT, buff=.26).move_to([0, 1.45, 0])
        memory = card("Global Memory", ACCENT, 4.5, 1.0, 26)
        memory.move_to([0, -1.8, 0])
        self.show(VGroup(flow, memory,
                         arrow(flow[0].get_bottom(),
                               memory.get_top() + LEFT * .7, ACCENT),
                         arrow(memory.get_top() + RIGHT * .7,
                               flow[2].get_bottom(), GOOD)))
        self.to(51)

        # 51–60: show other warps resident on the same SM.
        self.copy("SM 전체가 함께 기다릴 필요는 없습니다", "Warp 0 WAIT  ·  다른 Warp READY")
        warps = VGroup(*[
            card("Warp 0  ·  WAIT", PRUNE, 5.3, .76, 24),
            card("Warp 1  ·  READY", GOOD, 5.3, .76, 24),
            card("Warp 2  ·  READY", GOOD, 5.3, .76, 24),
            card("Warp 3  ·  READY", GOOD, 5.3, .76, 24),
        ]).arrange(DOWN, buff=.37).move_to([0, 0, 0])
        sm = SurroundingRectangle(warps, color=SPARSE, buff=.34,
                                  corner_radius=.2)
        self.show(VGroup(warps, sm, label("ONE SM", 21, SPARSE)
                         .next_to(sm, UP, buff=.42)))
        self.to(60)

        # 60–70: the hardware scheduler selects eligible warps.
        self.copy("하드웨어가 준비된 Warp를 선택", "Warp Scheduler  →  execution units")
        ready = VGroup(*[card(x, c, 1.6, .73, 22) for x, c in
                         zip(("W0 WAIT", "W1 READY", "W2 READY", "W3 READY"),
                             (PRUNE, GOOD, GOOD, GOOD))])
        ready.arrange(DOWN, buff=.35).move_to([-2.85, .0, 0])
        sched = card("Warp\nScheduler", SPARSE, 2.25, 1.3, 23)
        sched.move_to([.05, 0, 0])
        units = card("execution\nunits", ACCENT, 2.0, 1.3, 23)
        units.move_to([2.95, 0, 0])
        links = VGroup(*[arrow(ready[i].get_right(),
                               sched.get_left() + UP * (.28 * (2-i)), GOOD)
                         for i in (1, 2, 3)],
                       arrow(sched.get_right(), units.get_left(), ACCENT))
        self.show(VGroup(ready, sched, units, links))
        self.play(Indicate(ready[1], color=GOOD, scale_factor=1.04),
                  Indicate(ready[2], color=GOOD, scale_factor=1.04),
                  run_time=.8)
        self.to(70)

        # 70–79: multi-warp timeline; W0's LOAD remains pending.
        self.copy("Warp 0이 기다리는 동안", "다른 Warp 명령이 발행됩니다")
        axis = Line([-2.8, -2.85, 0], [3.35, -2.85, 0],
                    color=MUTED, stroke_width=2)
        row_y = (2.35, 1.2, .05, -1.1)
        names = VGroup(*[label(f"W{i}", 21, c).move_to([-3.38, y, 0])
                         for i, (y, c) in enumerate(zip(
                             row_y, (PRUNE, GOOD, WEIGHT, ACCENT)))])
        rows = VGroup(*[Line([-2.85, y-.38, 0], [3.3, y-.38, 0],
                             color=ZERO, stroke_width=1)
                        for y in row_y])
        blocks = VGroup(
            bar("LOAD", WEIGHT, .9).move_to([-2.2, row_y[0], 0]),
            bar("FMA", PRUNE, .9).move_to([2.65, row_y[0], 0]),
            bar("FMA", GOOD, .9).move_to([-.75, row_y[1], 0]),
            bar("ADD", WEIGHT, .9).move_to([1.25, row_y[1], 0]),
            bar("FMA", WEIGHT, .9).move_to([.1, row_y[2], 0]),
            bar("LOAD", ACCENT, .9).move_to([1.1, row_y[3], 0]),
        )
        pending = DashedLine([-1.68, row_y[0], 0],
                             [2.15, row_y[0], 0],
                             color=PRUNE, stroke_width=2,
                             dash_length=.12)
        self.show(VGroup(axis, rows, names, blocks, pending,
                         label("time →", 20, MUTED)
                         .move_to([2.7, -3.3, 0])))
        self.to(79)

        # 79–88: the latency exists, but useful instructions can cover it.
        self.copy("지연을 없애는 것은 아닙니다", "다른 작업으로 가리는 Latency Hiding")
        top = VGroup(
            label("Warp 0만 있으면", 24, PRUNE).move_to([-2.5, 2.65, 0]),
            bar("LOAD", WEIGHT, 1.1).move_to([-2.3, 1.65, 0]),
            bar("WAIT", PRUNE, 3.0).move_to([.1, 1.65, 0]),
            bar("FMA", GOOD, 1.1).move_to([2.7, 1.65, 0]),
        )
        bottom = VGroup(
            label("다른 Warp가 있으면", 24, GOOD).move_to([-2.4, -.45, 0]),
            bar("LOAD W0", WEIGHT, 1.1).move_to([-2.3, -1.55, 0]),
            bar("W1", GOOD, .9).move_to([-1.1, -1.55, 0]),
            bar("W2", SPARSE, .9).move_to([-.1, -1.55, 0]),
            bar("W3", ACCENT, .9).move_to([.9, -1.55, 0]),
            bar("W1", GOOD, .9).move_to([1.9, -1.55, 0]),
            bar("W0", WEIGHT, .9).move_to([2.9, -1.55, 0]),
        )
        self.show(VGroup(top, bottom,
                         label("W0의 memory latency는 남아 있음", 21, MUTED)
                         .move_to([0, -2.75, 0])))
        self.to(88)

        # 88–99: compile-time scheduling and runtime warp issue are different.
        self.copy("두 종류의 스케줄링", "Compiler  /  GPU hardware")
        left = VGroup(
            label("COMPILE TIME", 23, ACCENT),
            card("MUL A  →  ADD A", ACCENT, 3.4, .8, 21),
            card("MUL B는 독립", GOOD, 3.4, .8, 21),
            card("Instruction\nScheduling", SPARSE, 3.4, 1.0, 22),
        ).arrange(DOWN, buff=.38).move_to([-2.02, .2, 0])
        right = VGroup(
            label("RUNTIME", 23, WEIGHT),
            card("Warp 0  WAIT", PRUNE, 3.4, .8, 21),
            card("Warp 1, 2 READY", GOOD, 3.4, .8, 21),
            card("Warp\nScheduling", WEIGHT, 3.4, 1.0, 22),
        ).arrange(DOWN, buff=.38).move_to([2.02, .2, 0])
        self.show(VGroup(left, right,
                         Line([0, 3.1, 0], [0, -3.2, 0],
                              color=MUTED, stroke_opacity=.32)))
        self.to(99)

        # 99–108: a single ready warp exposes latency; tee up global memory.
        self.copy("다른 준비된 작업이 충분해야 합니다", "다음 질문: 왜 메모리는 오래 걸릴까?")
        single = card("1 ready Warp  →  WAIT 노출", PRUNE,
                      6.4, .9, 23).move_to([0, 2.3, 0])
        many = card("many ready Warps  →  지연 숨김", GOOD,
                    6.4, .9, 23).move_to([0, .75, 0])
        memory = card("Global Memory", ACCENT, 4.2, .95, 26)
        memory.move_to([0, -2.45, 0])
        self.show(VGroup(single, many, memory,
                         arrow([0, .15, 0], memory.get_top(), ACCENT)))
        self.to(108)

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
