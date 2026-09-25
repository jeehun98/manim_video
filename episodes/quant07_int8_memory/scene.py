"""Quantization 07: why smaller values reduce storage and memory traffic."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class INT8Memory(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  07", 20, MUTED).move_to(UP * 7.25),
            txt("INT8은 컴퓨터에서 무엇을 줄일까?", 31).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — hook: the same logical value occupies very different space.
        self.text(
            "같은 숫자, 다른 크기",
            "32bit 대신 8bit로 표현하면 컴퓨터 안에서는\n무엇이 실제로 달라질까요?",
            "FP32  32 bits                         INT8  8 bits",
        )
        fp_bits = self.bit_strip(32, VALUE, 6.8, "FP32")
        int_bits = self.bit_strip(8, SNAP, 1.7, "INT8")
        strips = VGroup(fp_bits, int_bits).arrange(DOWN, buff=1.0,
                                                   aligned_edge=LEFT)
        strips.move_to([0, .2, 0])
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in fp_bits[0]],
                              lag_ratio=.015), FadeIn(fp_bits[1:]), run_time=.8)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in int_bits[0]],
                              lag_ratio=.05), FadeIn(int_bits[1:]), run_time=.55)
        self.keep_stage(strips)
        self.play(Indicate(int_bits, color=SNAP, scale_factor=1.05), run_time=.65)
        self.to(7)

        # 7–15 s — bytes and the exact raw-storage ratio.
        self.text(
            "값 하나의 저장 공간은 4분의 1",
            "FP32 하나는 4 bytes, INT8 하나는 1 byte입니다.\n같은 개수라면 원시 데이터 크기는 이론적으로 4분의 1입니다.",
            "32 bits = 4 bytes          8 bits = 1 byte",
        )
        fp_bytes = self.byte_row(4, VALUE, "FP32", "4 bytes")
        int_byte = self.byte_row(1, SNAP, "INT8", "1 byte")
        byte_compare = VGroup(fp_bytes, int_byte).arrange(DOWN, buff=.8,
                                                          aligned_edge=LEFT)
        byte_compare.move_to([0, .25, 0])
        quarter = pill("RAW STORAGE  × 1/4", GOOD, 3.15).move_to([0, -1.55, 0])
        byte_stage = VGroup(byte_compare, quarter)
        self.play(FadeOut(strips), FadeIn(byte_compare), run_time=.75)
        self.play(FadeIn(quarter, shift=UP * .12), run_time=.45)
        self.keep_stage(byte_stage)
        self.play(Indicate(quarter, color=GOOD, scale_factor=1.06), run_time=.65)
        self.to(15)

        # 15–24 s — the small difference accumulates across a tensor.
        self.text(
            "수십억 개의 weight에서는 차이가 누적됩니다",
            "같은 16개 값을 담아도 FP32 tensor는 네 배의 공간을 쓰고,\nINT8 tensor는 같은 값을 더 작은 영역에 담습니다.",
            "same 16 values     ·     FP32 64 B     ·     INT8 16 B",
        )
        fp_tensor = self.tensor_block(16, 4, VALUE, "FP32", "64 bytes")
        int_tensor = self.tensor_block(16, 1, SNAP, "INT8", "16 bytes")
        tensors = VGroup(fp_tensor, int_tensor).arrange(DOWN, buff=.85,
                                                        aligned_edge=LEFT)
        tensors.move_to([0, .15, 0])
        self.play(FadeOut(byte_stage), FadeIn(fp_tensor), run_time=.55)
        self.play(TransformFromCopy(fp_tensor[1], int_tensor[1]),
                  FadeIn(VGroup(int_tensor[0], int_tensor[2])), run_time=.85)
        self.keep_stage(tensors)
        self.play(Indicate(int_tensor, color=SNAP, scale_factor=1.04), run_time=.65)
        self.to(24)

        # 24–36 s — main visual: equal-size transfer carries 4x more values.
        self.text(
            "더 중요한 것은 메모리에서 가져오는 비용입니다",
            "GPU는 HBM에서 연산 장치로 데이터를 계속 옮깁니다.\n같은 16-byte 전송이라면 INT8은 네 배의 값을 담을 수 있습니다.",
            "same transfer size          4 FP32 values  vs  16 INT8 values",
        )
        hbm = self.hardware_box("HBM", "GPU MEMORY", VALUE).move_to([-2.75, .15, 0])
        compute = self.hardware_box("COMPUTE", "MATH UNITS", GRID).move_to([2.75, .15, 0])
        bus = VGroup(
            Line([-1.68, .45, 0], [1.68, .45, 0], color=MUTED, stroke_width=5),
            Triangle(color=MUTED, fill_color=MUTED, fill_opacity=1)
            .scale(.11).rotate(-PI / 2).move_to([1.66, .45, 0]),
        )
        fp_packet = self.packet(4, VALUE, "FP32", "16 B transfer").move_to([0, 1.45, 0])
        int_packet = self.packet(16, SNAP, "INT8", "16 B transfer").move_to([0, -.95, 0])
        memory_stage = VGroup(hbm, compute, bus, fp_packet, int_packet)
        self.play(FadeOut(tensors), FadeIn(hbm), FadeIn(compute), Create(bus[0]),
                  FadeIn(bus[1]), run_time=.75)
        self.play(FadeIn(fp_packet), run_time=.5)
        self.play(fp_packet.animate.shift(RIGHT * 1.15), run_time=.75,
                  rate_func=linear)
        self.play(fp_packet.animate.shift(LEFT * 1.15), FadeIn(int_packet), run_time=.5)
        self.play(int_packet.animate.shift(RIGHT * 1.15), run_time=.75,
                  rate_func=linear)
        self.keep_stage(memory_stage)
        self.play(Indicate(int_packet[0], color=SNAP, scale_factor=1.04), run_time=.7)
        self.to(36)

        # 36–44 s — fixed bandwidth becomes more values per second.
        self.text(
            "같은 bandwidth로 더 많은 값을 전달합니다",
            "초당 이동할 수 있는 byte 수가 같아도 datatype이 작으면\n같은 시간에 더 많은 숫자를 연산 장치에 공급할 수 있습니다.",
            "smaller datatype  →  more values per transfer  →  less traffic",
        )
        fp_lane = self.bandwidth_lane("FP32", 4, VALUE, "4 values")
        int_lane = self.bandwidth_lane("INT8", 16, SNAP, "16 values")
        lanes = VGroup(fp_lane, int_lane).arrange(DOWN, buff=.9,
                                                  aligned_edge=LEFT)
        lanes.move_to([0, .2, 0])
        ratio = pill("VALUES PER TRANSFER  × 4", GOOD, 3.65).move_to([0, -1.65, 0])
        bandwidth_stage = VGroup(lanes, ratio)
        self.play(FadeOut(memory_stage), FadeIn(lanes), run_time=.8)
        self.play(FadeIn(ratio, shift=UP * .1), run_time=.45)
        self.keep_stage(bandwidth_stage)
        self.play(Indicate(int_lane[1], color=SNAP, scale_factor=1.04), run_time=.65)
        self.to(44)

        # 44–51 s — memory-bound compute can spend less time waiting.
        self.text(
            "데이터를 기다리는 연산이라면 속도에도 영향을 줍니다",
            "계산보다 데이터 이동이 병목인 작업에서는 memory traffic이\n줄어드는 것만으로도 연산 장치의 대기 시간을 줄일 수 있습니다.",
            "memory-bound workload          waiting ↓          runtime ↓ possible",
        )
        fp_timeline = self.timeline("FP32", [(.9, ERROR), (.45, GRID), (.85, ERROR),
                                              (.45, GRID), (.85, ERROR)], 5.6)
        int_timeline = self.timeline("INT8", [(.28, ERROR), (.72, GRID), (.28, ERROR),
                                               (.72, GRID), (.28, ERROR), (.72, GRID)], 5.6)
        timelines = VGroup(fp_timeline, int_timeline).arrange(DOWN, buff=.85,
                                                              aligned_edge=LEFT)
        timelines.move_to([0, .2, 0])
        legend = VGroup(pill("WAIT", ERROR, 1.35), pill("COMPUTE", GRID, 1.65))
        legend.arrange(RIGHT, buff=.25).scale(.8).move_to([0, -1.65, 0])
        wait_stage = VGroup(timelines, legend)
        self.play(FadeOut(bandwidth_stage), FadeIn(timelines), FadeIn(legend),
                  run_time=.8)
        self.keep_stage(wait_stage)
        self.play(Indicate(int_timeline, color=GOOD, scale_factor=1.03), run_time=.65)
        self.to(51)

        # 51–56 s — explicit caveat: storage ratio is not a speed guarantee.
        self.text(
            "하지만 INT8이 항상 4배 빠른 것은 아닙니다",
            "실제 속도는 연산과 메모리 이동의 비율, 변환 비용,\n그리고 하드웨어의 INT8 지원에 따라 달라집니다.",
            "1/4 storage  ≠  guaranteed 4× speed",
        )
        claim = txt("INT8  =  ALWAYS  4× FASTER", 35, INK).move_to([0, .45, 0])
        cross = Cross(claim, stroke_color=ERROR, stroke_width=8)
        factors = VGroup(
            pill("memory / compute", VALUE, 2.5),
            pill("conversion cost", SNAP, 2.35),
            pill("hardware support", GRID, 2.55),
        ).arrange(DOWN, buff=.24).scale(.82).move_to([0, -1.05, 0])
        caveat = VGroup(claim, cross, factors)
        self.play(FadeOut(wait_stage), FadeIn(claim), Create(cross), run_time=.65)
        self.play(FadeIn(factors, shift=UP * .08), run_time=.45)
        self.keep_stage(caveat)
        self.to(56)

        # 56–60 s — next: compact operands can also change arithmetic throughput.
        self.text(
            "더 작은 숫자는 실제 계산도 빠르게 만들 수 있을까?",
            "다음에는 낮은 precision이 저장과 이동을 넘어\n곱셈 처리량에도 영향을 주는 이유를 살펴봅니다.",
            "NEXT  ·  Low-Precision Compute",
        )
        ops = VGroup(*[
            self.op_card("INT8 × INT8", str(i + 1)) for i in range(4)
        ]).arrange_in_grid(rows=2, cols=2, buff=(.35, .35)).move_to([0, .25, 0])
        feed = Arrow([0, -1.75, 0], [0, -1.05, 0], color=SNAP,
                     stroke_width=4, tip_length=.16)
        next_stage = VGroup(ops, feed)
        self.play(FadeOut(caveat), LaggedStart(*[FadeIn(o, scale=.9) for o in ops],
                                               lag_ratio=.1), run_time=.75)
        self.play(GrowArrow(feed), run_time=.35)
        self.keep_stage(next_stage)
        self.to(60)

    def bit_strip(self, count, color, width, label):
        gap = .018
        cell_w = (width - gap * (count - 1)) / count
        cells = VGroup(*[
            Rectangle(width=cell_w, height=.52, stroke_width=.6,
                      stroke_color=color, fill_color=color, fill_opacity=.85)
            for _ in range(count)
        ]).arrange(RIGHT, buff=gap)
        title = txt(label, 24, color).next_to(cells, LEFT, buff=.28)
        count_label = txt(f"{count} bits", 20, MUTED).next_to(cells, RIGHT, buff=.22)
        return VGroup(cells, title, count_label)

    def byte_row(self, count, color, name, size):
        cells = VGroup(*[
            RoundedRectangle(width=1.05, height=1.05, corner_radius=.12,
                             stroke_color=color, stroke_width=2,
                             fill_color=color, fill_opacity=.18)
            for _ in range(count)
        ]).arrange(RIGHT, buff=.12)
        for i, cell in enumerate(cells):
            cell.add(txt(f"B{i + 1}", 18, color).move_to(cell))
        cells.align_to(LEFT * 2.1, LEFT)
        return VGroup(txt(name, 23, color).next_to(cells, LEFT, buff=.3), cells,
                      txt(size, 21, INK).next_to(cells, RIGHT, buff=.25))

    def tensor_block(self, values, bytes_per_value, color, name, size):
        cell_w = .16 * bytes_per_value
        cells = VGroup(*[
            Rectangle(width=cell_w, height=.38, stroke_color=color,
                      stroke_width=1, fill_color=color, fill_opacity=.55)
            for _ in range(values)
        ]).arrange_in_grid(rows=2, cols=8, buff=(.04, .08))
        title = txt(name, 23, color).next_to(cells, LEFT, buff=.3)
        amount = txt(size, 21, INK).next_to(cells, RIGHT, buff=.25)
        return VGroup(title, cells, amount)

    def hardware_box(self, title, subtitle, color):
        box = RoundedRectangle(width=1.8, height=2.25, corner_radius=.2,
                               stroke_color=color, stroke_width=2.3,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box,
                      txt(title, 26, color).move_to(box.get_center() + UP * .25),
                      txt(subtitle, 15, MUTED).move_to(box.get_center() + DOWN * .28))

    def packet(self, count, color, name, transfer):
        cols = 8 if count > 8 else count
        rows = 2 if count > 8 else 1
        width = 3.15 / cols
        cells = VGroup(*[
            Rectangle(width=width, height=.38, stroke_color=color, stroke_width=1,
                      fill_color=color, fill_opacity=.8)
            for _ in range(count)
        ]).arrange_in_grid(rows=rows, cols=cols, buff=(.025, .025))
        frame = SurroundingRectangle(cells, color=INK, stroke_width=1.5, buff=.08)
        label = txt(f"{name} · {count} values", 18, color).next_to(frame, UP, buff=.1)
        size = txt(transfer, 15, MUTED).next_to(frame, DOWN, buff=.08)
        return VGroup(cells, frame, label, size)

    def bandwidth_lane(self, name, count, color, amount):
        frame = RoundedRectangle(width=6.1, height=.85, corner_radius=.14,
                                 stroke_color=MUTED, stroke_width=1.5)
        cell_w = 4.45 / count
        cells = VGroup(*[
            Rectangle(width=cell_w, height=.42, stroke_width=.5,
                      stroke_color=color, fill_color=color, fill_opacity=.8)
            for _ in range(count)
        ]).arrange(RIGHT, buff=.015).move_to(frame)
        return VGroup(txt(name, 21, color).next_to(frame, LEFT, buff=.22), cells,
                      frame, txt(amount, 18, INK).next_to(frame, RIGHT, buff=.2))

    def timeline(self, name, segments, total_width):
        total = sum(length for length, _ in segments)
        parts = VGroup(*[
            Rectangle(width=total_width * length / total, height=.65,
                      stroke_width=0, fill_color=color, fill_opacity=.82)
            for length, color in segments
        ]).arrange(RIGHT, buff=.035)
        return VGroup(txt(name, 22, INK).next_to(parts, LEFT, buff=.25), parts)

    def op_card(self, label, index):
        box = RoundedRectangle(width=2.75, height=1.25, corner_radius=.17,
                               stroke_color=SNAP, stroke_width=1.8,
                               fill_color=SNAP, fill_opacity=.08)
        return VGroup(box, txt(label, 22, SNAP).move_to(box),
                      txt(index, 14, MUTED).move_to(box.get_corner(UR) + DL * .16))

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
