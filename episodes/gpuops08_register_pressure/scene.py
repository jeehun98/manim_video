"""GPU operations 08: fusion limits through live values and register pressure."""
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


class GPURegisterPressure(Scene):
    DURATION = 90

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  08", 20, MUTED).move_to(UP * 7.3),
            label("왜 모든 연산을 하나로 합치지 않을까?", 30).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–7: recap removal of intermediate traffic.
        self.copy(
            "지금까지는 중간 메모리 왕복을 없앴습니다", "FUSION RECAP",
            "중간값을 Global Memory에 저장하지 않고\n같은 Kernel 안에서 다음 연산으로 이어갔습니다.",
        )
        ops = VGroup(*[
            mini(x, c, 1.25, .7, 22) for x, c in zip(
                ("A", "B", "C", "D"), (WEIGHT, GOOD, ACCENT, SPARSE))
        ]).arrange(RIGHT, buff=.55).move_to([0, 1.2, 0])
        links = VGroup(*[
            arrow(ops[i].get_right(), ops[i + 1].get_left(), GOOD, 2)
            for i in range(3)
        ])
        crossed = VGroup(*[
            VGroup(mini("STORE\nLOAD", PRUNE, 1.2, .72, 14),
                   Line(LEFT * .55, RIGHT * .55, color=PRUNE, stroke_width=4))
            for _ in range(3)
        ]).arrange(RIGHT, buff=.8).move_to([0, -1.35, 0])
        self.show(VGroup(ops, links, crossed))
        self.to(7)

        # 7–14: tempt the viewer with maximal fusion.
        self.copy(
            "그럼 전부 하나로 합치면 가장 빠를까요?", "MORE FUSION = MORE SPEED ?",
            "Operator 세 개, 다섯 개, 열 개까지\n가능한 연산을 모두 한 Kernel에 넣어봅시다.",
        )
        groups = VGroup()
        for count, color, y in ((3, GOOD, 2.25), (5, ACCENT, .25), (10, PRUNE, -1.85)):
            nodes = VGroup(*[
                mini(str(i + 1), color, .5, .5, 14) for i in range(count)
            ]).arrange(RIGHT, buff=.12)
            frame = SurroundingRectangle(nodes, color=color, buff=.22,
                                         corner_radius=.15)
            tag = label(f"{count} ops / 1 kernel", 19, color).next_to(frame, LEFT, buff=.3)
            groups.add(VGroup(nodes, frame, tag).move_to([.75, y, 0]))
        self.show(groups)
        self.play(Indicate(groups[-1], color=PRUNE, scale_factor=1.03), run_time=.6)
        self.to(14)

        # 14–22: values not materialized still have to live somewhere.
        self.copy(
            "저장하지 않은 값도 사라지지는 않습니다", "WHERE DOES THE VALUE LIVE?",
            "다음 계산에 필요한 중간값은 GPU 내부 어딘가에\n마지막 사용 시점까지 계속 남아 있어야 합니다.",
        )
        flow = self.horizontal_flow(
            ("make v₀", "op A", "op B", "last use"),
            (WEIGHT, GOOD, ACCENT, PRUNE),
            widths=(1.55, 1.35, 1.35, 1.65), height=.7,
        ).move_to([0, 1.6, 0])
        live = RoundedRectangle(width=6.15, height=.65, corner_radius=.12,
                                stroke_color=ACCENT, fill_color=ACCENT,
                                fill_opacity=.22, stroke_width=2)
        live.move_to([.25, -.25, 0])
        live_text = label("v₀ is LIVE", 23, ACCENT).move_to(live)
        question = label("not in Global Memory  ≠  gone", 23, PRUNE)
        question.move_to([0, -1.8, 0])
        self.show(VGroup(flow, live, live_text, question))
        self.to(22)

        # 22–30: thread registers fill with live values.
        self.copy(
            "살아 있는 값은 흔히 Register에 놓입니다", "THREAD REGISTER SET",
            "Thread가 동시에 유지해야 하는 값이 많아지면\n그 Thread에 필요한 Register 수도 늘어날 수 있습니다.",
        )
        thread = RoundedRectangle(width=6.7, height=4.6, corner_radius=.25,
                                  stroke_color=GOOD, stroke_width=3,
                                  fill_color=GOOD, fill_opacity=.025)
        thread.move_to([0, .35, 0])
        title = label("Thread", 25, GOOD).move_to([0, 2.85, 0])
        regs = VGroup(*[
            mini(f"R{i}\n[{v}]", c, 1.05, .85, 17)
            for i, (v, c) in enumerate(zip(
                ("a", "b", "c", "temp0", "temp1", "temp2", "v₀", "v₁"),
                (WEIGHT, WEIGHT, WEIGHT, ACCENT, ACCENT, ACCENT, PRUNE, PRUNE)))
        ]).arrange_in_grid(rows=2, cols=4, buff=(.35, .5)).move_to([0, .25, 0])
        self.show(VGroup(thread, title, regs))
        self.to(30)

        # 30–37: explain overlapping live ranges, not simply code length.
        self.copy(
            "핵심은 동시에 살아 있는 값의 수입니다", "OVERLAPPING LIVE RANGES",
            "값은 생성부터 마지막 사용까지 살아 있습니다.\n여러 lifetime이 겹치면 필요한 Register가 증가합니다.",
        )
        axis = Arrow([-3.3, -2.5, 0], [3.4, -2.5, 0], buff=0,
                     color=MUTED, stroke_width=2, tip_length=.14)
        time_tag = label("시간", 18, MUTED).next_to(axis, RIGHT, buff=.1)
        bars = VGroup()
        specs = ((-2.8, 2.6), (-2.1, 2.8), (-1.35, 2.5), (-.55, 2.3))
        colors = (GOOD, ACCENT, WEIGHT, PRUNE)
        for i, ((start, width), color) in enumerate(zip(specs, colors)):
            bar = Rectangle(width=width, height=.47, fill_color=color,
                            fill_opacity=.75, stroke_width=0)
            bar.move_to([start + width / 2, 2.0 - i * 1.0, 0])
            name = label(f"v{i}", 20, color).next_to(bar, LEFT, buff=.18)
            bars.add(VGroup(bar, name))
        overlap = DashedVMobject(Rectangle(width=1.25, height=4.2), num_dashes=18,
                                  color=INK).move_to([.15, .55, 0])
        tag = label("4 live values", 21, INK).move_to([.15, 3.05, 0])
        self.show(VGroup(axis, time_tag, bars, overlap, tag))
        self.to(37)

        # 37–45: name register pressure and mention spill risk.
        self.copy(
            "이 요구량이 커지는 것이 Register Pressure입니다", "REGISTER PRESSURE ↑",
            "Fusion으로 live value가 늘면 Register 요구량도 커질 수 있습니다.\n한계를 넘으면 일부 값이 spill될 가능성도 있습니다.",
        )
        before = VGroup(
            label("BEFORE", 20, GOOD),
            *[mini(f"R{i}", GOOD, .8, .58, 17) for i in range(4)],
        ).arrange(DOWN, buff=.25).move_to([-2.15, .4, 0])
        after_regs = VGroup(*[
            mini(f"R{i}", PRUNE, .8, .48, 15) for i in range(10)
        ]).arrange_in_grid(rows=5, cols=2, buff=(.2, .18))
        after = VGroup(label("FUSED", 20, PRUNE), after_regs)
        after.arrange(DOWN, buff=.3).move_to([1.5, .4, 0])
        pressure = Arrow([-.45, -.4, 0], [.55, -.4, 0], buff=0,
                         color=PRUNE, stroke_width=4, tip_length=.2)
        spill = mini("spill ?", ACCENT, 1.7, .65, 20).move_to([3.0, -2.45, 0])
        self.show(VGroup(before, after, pressure, spill))
        self.to(45)

        # 45–53: a finite register file is shared by resident work.
        self.copy(
            "한 SM의 Register File은 유한합니다", "FIXED RESOURCE PER SM",
            "SM에는 Register 자원의 총량이 정해져 있습니다.\n여러 Thread와 Warp가 이 자원을 나누어 사용합니다.",
        )
        sm = RoundedRectangle(width=7.0, height=5.1, corner_radius=.25,
                              stroke_color=SPARSE, stroke_width=3,
                              fill_color=SPARSE, fill_opacity=.025)
        sm.move_to([0, .2, 0])
        title = label("SM", 25, SPARSE).move_to([0, 3.05, 0])
        register_file = card("Register File  ·  fixed capacity", ACCENT,
                             5.8, .82, 24).move_to([0, 1.75, 0])
        warps = VGroup(*[
            card(f"Warp {i}", c, 5.2, .58, 19)
            for i, c in enumerate((GOOD, WEIGHT, ACCENT, PRUNE))
        ]).arrange(DOWN, buff=.27).move_to([0, -.65, 0])
        self.show(VGroup(sm, title, register_file, warps))
        self.to(53)

        # 53–61: more registers per thread can reduce resident warps.
        self.copy(
            "Thread당 요구량이 커지면 배치 수가 줄 수 있습니다", "RESIDENT WARPS MAY DECREASE",
            "같은 Register File에서 각 Thread가 더 많이 요구하면\n동시에 resident할 수 있는 Warp 수가 줄어들 수 있습니다.",
        )
        left = self.register_partition("LOW PRESSURE", 5, 1.0, GOOD)
        right = self.register_partition("HIGH PRESSURE", 3, 1.65, PRUNE)
        left.move_to([-2.0, .15, 0])
        right.move_to([2.0, .15, 0])
        divider = Line([0, 3.0, 0], [0, -2.8, 0], color=MUTED,
                       stroke_opacity=.3)
        self.show(VGroup(left, right, divider))
        self.to(61)

        # 61–69: fewer warps can reduce latency hiding opportunities.
        self.copy(
            "대신 실행할 Warp의 여유도 줄 수 있습니다", "LESS LATENCY-HIDING HEADROOM",
            "한 Warp가 메모리를 기다릴 때 준비된 Warp가 많으면 교체할 수 있습니다.\nresident Warp가 적으면 그 여유도 줄어들 수 있습니다.",
        )
        before = VGroup(
            mini("Warp A\nWAIT", PRUNE, 2.0, .85, 20),
            mini("Warp B\nRUN", GOOD, 2.0, .85, 20),
            mini("Warp C\nREADY", ACCENT, 2.0, .85, 18),
        ).arrange(DOWN, buff=.35).move_to([-2.0, .35, 0])
        after = VGroup(
            mini("Warp A\nWAIT", PRUNE, 2.0, .85, 20),
            mini("no spare\nwarp", MUTED, 2.0, .85, 18),
        ).arrange(DOWN, buff=.45).move_to([2.0, .35, 0])
        tags = VGroup(label("MORE RESIDENT", 18, GOOD).move_to([-2.0, 2.65, 0]),
                      label("FEWER RESIDENT", 18, PRUNE).move_to([2.0, 2.65, 0]))
        self.show(VGroup(before, after, tags,
                         arrow([-1.0, .35, 0], [1.0, .35, 0], PRUNE)))
        self.to(69)

        # 69–77: make the tradeoff explicit.
        self.copy(
            "Fusion에는 두 비용의 교환관계가 있습니다", "TRAFFIC ↓  ↔  PRESSURE ↑",
            "중간 Global Memory 왕복은 줄어듭니다.\n대신 Kernel 내부에서 유지할 상태는 커질 수 있습니다.",
        )
        beam = Line([-3.0, .25, 0], [3.0, .25, 0], color=INK, stroke_width=5)
        pivot = Polygon([-.35, -.1, 0], [.35, -.1, 0], [0, -1.0, 0],
                        color=MUTED, fill_color=MUTED, fill_opacity=.5)
        traffic = card("Global Memory\nTraffic ↓", GOOD, 2.65, 1.25, 23)
        traffic.move_to([-2.2, 1.05, 0])
        pressure = card("Register\nPressure ↑", PRUNE, 2.65, 1.25, 23)
        pressure.move_to([2.2, 1.05, 0])
        note = label("benefit", 20, GOOD).move_to([-2.2, 2.35, 0])
        cost = label("cost", 20, PRUNE).move_to([2.2, 2.35, 0])
        self.show(VGroup(beam, pivot, traffic, pressure, note, cost))
        self.to(77)

        # 77–84: performance can peak before maximal fusion.
        self.copy(
            "더 많은 Fusion이 항상 더 빠르지는 않습니다", "PERFORMANCE CAN PEAK",
            "처음에는 메모리 왕복 감소가 이깁니다. 하지만 어느 순간\n추가 자원 비용이 이득보다 커질 수 있습니다.",
        )
        x_axis = Arrow([-3.1, -2.25, 0], [3.35, -2.25, 0], buff=0,
                       color=MUTED, stroke_width=2, tip_length=.14)
        y_axis = Arrow([-3.1, -2.25, 0], [-3.1, 2.8, 0], buff=0,
                       color=MUTED, stroke_width=2, tip_length=.14)
        curve = VMobject(color=ACCENT, stroke_width=5)
        curve.set_points_smoothly([
            [-2.8, -1.55, 0], [-1.7, .25, 0], [-.45, 1.55, 0],
            [.55, 1.8, 0], [1.5, 1.45, 0], [2.65, .45, 0],
        ])
        peak = Dot([.4, 1.78, 0], color=GOOD, radius=.1)
        tag = label("best point", 20, GOOD).next_to(peak, UP, buff=.25)
        labels = VGroup(label("fusion amount →", 18, MUTED).move_to([1.65, -2.72, 0]),
                        label("speed", 18, MUTED).move_to([-3.45, 2.55, 0]))
        self.show(VGroup(x_axis, y_axis, curve, peak, tag, labels))
        self.to(84)

        # 84–90: preserve selected boundaries and hand off to compiler policy.
        self.copy(
            "모든 경계가 아니라 좋은 경계를 선택합니다", "COMPILER: HOW FAR TO FUSE?",
            "어떤 값을 유지하고 어디서 Kernel을 끊을지가 중요합니다.\n컴파일러는 이 Fusion 경계를 어떻게 결정할까요?",
        )
        graph = self.horizontal_flow(
            ("A", "B", "C", "D", "E"),
            (WEIGHT, GOOD, ACCENT, SPARSE, PRUNE),
            widths=(1.0, 1.0, 1.0, 1.0, 1.0), height=.65,
        ).move_to([0, 1.25, 0])
        left_fused = SurroundingRectangle(VGroup(graph[0][0], graph[0][1], graph[0][2]),
                                          color=GOOD, buff=.3, corner_radius=.18)
        boundary = DashedLine([1.0, 2.25, 0], [1.0, .15, 0], color=PRUNE,
                              dash_length=.14)
        question = card("Legality  +  Profitability", ACCENT, 5.3, .9, 26)
        question.move_to([0, -1.45, 0])
        self.show(VGroup(graph, left_fused, boundary, question))
        self.to(90)

    def register_partition(self, title, count, width, color):
        frame = RoundedRectangle(width=3.25, height=5.0, corner_radius=.2,
                                 stroke_color=color, stroke_width=2)
        bars = VGroup(*[
            Rectangle(width=width, height=.5, stroke_color=color,
                      fill_color=color, fill_opacity=.35)
            for _ in range(count)
        ]).arrange(DOWN, buff=.22)
        bars.move_to(frame)
        tag = label(title, 17, color).next_to(frame, UP, buff=.28)
        count_tag = label(f"{count} resident warps", 18, color).next_to(frame, DOWN, buff=.28)
        return VGroup(frame, bars, tag, count_tag)

    def horizontal_flow(self, names, colors, widths=None, height=.82):
        if widths is None:
            widths = tuple(1.7 for _ in names)
        nodes = VGroup(*[
            card(n, c, w, height, 21, .12)
            for n, c, w in zip(names, colors, widths)
        ])
        nodes.arrange(RIGHT, buff=.35)
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
