"""Quantization 04: zero point aligns real zero with an integer code."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE,
    MappedAxes, pill, txt,
)


class QuantizationZeroPoint(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  04", 20, MUTED).move_to(UP * 7.25),
            txt("실수의 0은 정수 격자의 어디에 놓여야 할까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — previous assumption: both origins are aligned.
        self.text(
            "지금까지는 두 축의 0이 같다고 가정했습니다",
            "Scale은 정수 한 칸의 실제 크기를 정했고,\n실수 0과 정수 0은 같은 시작점에 있었습니다.",
            "scale = 한 칸의 크기     ·     real 0 ↔ integer 0",
        )
        aligned = MappedAxes((0, 1), (0, 255), width=6.6).move_to([0, .15, 0])
        origin = VGroup(
            Dot(aligned.real_point(0), radius=.12, color=ERROR),
            Dot(aligned.int_point(0), radius=.12, color=ERROR),
            Line(aligned.real_point(0), aligned.int_point(0),
                 color=ERROR, stroke_width=2.5),
            txt("0 ↔ 0", 23, ERROR).move_to([-2.7, .15, 0]),
        )
        aligned_stage = VGroup(aligned, origin)
        self.play(FadeIn(aligned), FadeIn(origin), run_time=.9)
        self.play(Indicate(origin, color=SNAP, scale_factor=1.08), run_time=.75)
        self.keep_stage(aligned_stage)
        self.to(7)

        # 7–15 s — a range that crosses zero breaks the aligned-origin picture.
        self.text(
            "하지만 실제 범위는 항상 0에서 시작하지 않습니다",
            "−1부터 3까지의 실수를 0부터 255의 정수로 표현하면\n실수 0은 정수 0과 같은 위치에 있을 수 없습니다.",
            "real −1…3     ↔     integer 0…255",
        )
        shifted = MappedAxes((-1, 3), (0, 255), width=6.6).move_to([0, .15, 0])
        real_zero = shifted.real_point(0)
        question = VGroup(
            Dot(real_zero, radius=.12, color=ERROR),
            txt("real 0", 22, ERROR).next_to(real_zero, UP, buff=.2),
            DashedLine(real_zero + DOWN * .12,
                       shifted.int_axis.point_from_proportion(.25) + UP * .1,
                       color=ERROR, stroke_width=2, dash_length=.09),
            txt("?", 36, SNAP).next_to(
                shifted.int_axis.point_from_proportion(.25), DOWN, buff=.25),
        )
        problem = VGroup(shifted, question)
        self.play(FadeOut(aligned_stage), FadeIn(shifted), FadeIn(question), run_time=.9)
        self.keep_stage(problem)
        self.play(Indicate(question[-1], color=SNAP, scale_factor=1.35), run_time=.75)
        self.to(15)

        # 15–23 s — proportional alignment places real zero near q=64.
        self.text(
            "두 범위를 맞추면 실수 0은 q≈64에 놓입니다",
            "실수 0은 −1부터 3까지 범위의 4분의 1 지점이므로\n정수 공간에서도 약 4분의 1 지점에 대응됩니다.",
            "real 0     ↓     q ≈ 64",
        )
        q64 = shifted.int_point(64)
        mapping = VGroup(
            Dot(real_zero, radius=.13, color=ERROR),
            Dot(q64, radius=.15, color=SNAP),
            DashedLine(real_zero, q64, color=ERROR, stroke_width=2.5,
                       dash_length=.09),
            txt("real 0", 22, ERROR).next_to(real_zero, UP, buff=.2),
            txt("q ≈ 64", 25, SNAP).next_to(q64, DOWN, buff=.28),
            pill("¼ of the range", VALUE, 2.45).move_to([0, -2.3, 0]),
        )
        found = VGroup(shifted, mapping)
        self.play(FadeOut(question), FadeIn(mapping[:-1]), run_time=.65)
        self.play(FadeIn(mapping[-1], shift=UP * .1), run_time=.45)
        self.keep_stage(found)
        self.play(Flash(q64, color=SNAP, flash_radius=.42),
                  Indicate(mapping[4], color=SNAP, scale_factor=1.12), run_time=.8)
        self.to(23)

        # 23–30 s — define zero point as the integer code for real zero.
        self.text(
            "이 위치가 바로 zero point입니다",
            "Zero point는 실수값 0을 표현하는 정수 값입니다.\n이 예에서는 정수 64가 실수 0을 의미합니다.",
            "x = 0     ↔     z = 64",
        )
        integer_strip = self.integer_strip(0, 255, 6.6).move_to([0, .15, 0])
        zp_dot = Dot(integer_strip[0].point_from_proportion(64 / 255),
                     radius=.17, color=SNAP)
        zp_line = Line(UP * .48, DOWN * .48, color=ERROR,
                       stroke_width=3).move_to(zp_dot)
        zero_card = VGroup(
            pill("real x = 0", ERROR, 2.25),
            txt("↓", 30, MUTED),
            pill("zero point = 64", SNAP, 3.05),
        ).arrange(DOWN, buff=.17).move_to([0, 1.8, 0])
        definition = VGroup(integer_strip, zp_dot, zp_line, zero_card)
        self.play(FadeOut(found), FadeIn(integer_strip), FadeIn(zp_line),
                  FadeIn(zp_dot, scale=1.7), FadeIn(zero_card), run_time=.9)
        self.keep_stage(definition)
        self.play(Indicate(zero_card[-1], color=SNAP, scale_factor=1.08), run_time=.75)
        self.to(30)

        # 30–38 s — offset form of the dequantization equation.
        self.text(
            "먼저 zero point만큼 좌표를 이동합니다",
            "정수 q에서 zero point z를 뺀 뒤,\n그 차이에 scale s를 곱해 실제 값 x로 해석합니다.",
            "q − z = 0일 때     x = 0",
        )
        formula = VGroup(
            txt("x", 58, VALUE), txt("≈", 45, MUTED), txt("s", 58, GOOD),
            txt("(", 55, INK), txt("q", 58, GRID), txt("−", 45, MUTED),
            txt("z", 58, SNAP), txt(")", 55, INK),
        ).arrange(RIGHT, buff=.16).move_to([0, 1.1, 0])
        labels = VGroup(
            txt("실제 값", 19, VALUE).next_to(formula[0], DOWN, buff=.48),
            txt("scale", 19, GOOD).next_to(formula[2], DOWN, buff=.48),
            txt("정수 값", 19, GRID).next_to(formula[4], DOWN, buff=.48),
            txt("zero point", 19, SNAP).next_to(formula[6], DOWN, buff=.48),
        )
        focus = SurroundingRectangle(VGroup(formula[4], formula[5], formula[6]),
                                     color=SNAP, buff=.13, corner_radius=.1)
        equation = VGroup(formula, labels, focus)
        self.play(FadeOut(definition), LaggedStart(*[FadeIn(m) for m in formula],
                                                   lag_ratio=.06), run_time=.8)
        self.play(FadeIn(labels), Create(focus), run_time=.6)
        self.keep_stage(equation)
        self.play(Indicate(focus, color=SNAP, scale_factor=1.06), run_time=.75)
        self.to(38)

        # 38–46 s — slide the real ruler while the integer grid stays fixed.
        self.text(
            "범위가 움직이면 zero point도 움직입니다",
            "정수 격자는 그대로 두고 실수 범위를 −1…3에서\n−3…1로 옮기면 실수 0의 위치도 오른쪽으로 이동합니다.",
            "−1…3: z≈64          −3…1: z≈191",
        )
        ruler = self.sliding_ruler((-1, 0, 1, 2, 3), 6.4, VALUE).move_to([0, 1.15, 0])
        fixed_q = self.integer_strip(0, 255, 6.4).move_to([0, -1.0, 0])
        marker = Dot(fixed_q[0].point_from_proportion(64 / 255),
                     radius=.15, color=SNAP)
        marker_label = txt("z ≈ 64", 23, SNAP).next_to(marker, DOWN, buff=.28)
        move_stage = VGroup(ruler, fixed_q, marker, marker_label)
        self.play(FadeOut(equation), FadeIn(move_stage), run_time=.75)
        new_ruler = self.sliding_ruler((-3, -2, -1, 0, 1), 6.4, VALUE)
        new_ruler.move_to(ruler)
        new_marker = fixed_q[0].point_from_proportion(191 / 255)
        new_label = txt("z ≈ 191", 23, SNAP).next_to(new_marker, DOWN, buff=.28)
        self.play(Transform(ruler, new_ruler), marker.animate.move_to(new_marker),
                  Transform(marker_label, new_label), run_time=1.5, rate_func=smooth)
        self.keep_stage(move_stage)
        self.play(Indicate(VGroup(marker, marker_label), color=SNAP, scale_factor=1.1),
                  run_time=.75)
        self.to(46)

        # 46–53 s — symmetric ranges can align both zeros at q=0.
        self.text(
            "대칭 범위에서는 zero point를 0에 둘 수 있습니다",
            "실수 범위를 0을 중심으로 대칭적으로 잡고 signed 정수와\n대응시키면 두 축의 0을 중앙에서 맞출 수 있습니다.",
            "−1…1     ↔     −127…127          zero point = 0",
        )
        symmetric = self.symmetric_axes(6.6).move_to([0, .2, 0])
        zero_pair = VGroup(
            Dot(symmetric[0].get_center(), radius=.13, color=ERROR),
            Dot(symmetric[1].get_center(), radius=.15, color=SNAP),
            DashedLine(symmetric[0].get_center(), symmetric[1].get_center(),
                       color=ERROR, stroke_width=2.5, dash_length=.09),
            pill("zero point = 0", SNAP, 2.85).move_to([0, -2.25, 0]),
        )
        symmetric_stage = VGroup(symmetric, zero_pair)
        self.play(FadeOut(move_stage), FadeIn(symmetric), FadeIn(zero_pair), run_time=.9)
        self.keep_stage(symmetric_stage)
        self.play(Indicate(zero_pair[-1], color=SNAP, scale_factor=1.09), run_time=.75)
        self.to(53)

        # 53–60 s — once the grid is placed, snapping creates an error.
        self.text(
            "격자에 맞추는 순간 작은 차이가 남을 수 있습니다",
            "Scale과 zero point로 격자를 배치해도 실제 값을 가장 가까운\n위치로 옮기면 원래 값과 표현값 사이에 차이가 생깁니다.",
            "NEXT  ·  원래 값과 표현값의 차이, Quantization Error",
        )
        error_axis = NumberLine(x_range=[.38, .48, .02], length=6.0,
                                include_numbers=False, color=MUTED,
                                stroke_width=2.5).move_to([0, .25, 0])
        grid_ticks = VGroup(*[
            Line(UP * .24, DOWN * .24, color=GRID, stroke_width=3).move_to(error_axis.n2p(v))
            for v in (.38, .40, .42, .44, .46, .48)
        ])
        original = Dot(error_axis.n2p(.43), radius=.13, color=VALUE)
        represented = Dot(error_axis.n2p(.44), radius=.16, color=SNAP)
        original_label = txt("0.43", 23, VALUE).next_to(original, UP, buff=.28)
        represented_label = txt("0.44", 23, SNAP).next_to(represented, DOWN, buff=.28)
        error_span = DoubleArrow(original.get_center() + UP * .72,
                                 represented.get_center() + UP * .72,
                                 buff=.02, color=ERROR, stroke_width=2.5,
                                 tip_length=.08)
        error_label = txt("error", 23, ERROR).next_to(error_span, UP, buff=.12)
        error_stage = VGroup(error_axis, grid_ticks, original, represented,
                             original_label, represented_label, error_span, error_label)
        self.play(FadeOut(symmetric_stage), FadeIn(error_axis), FadeIn(grid_ticks),
                  FadeIn(original), FadeIn(original_label), run_time=.7)
        self.play(TransformFromCopy(original, represented), FadeIn(represented_label),
                  GrowArrow(error_span), FadeIn(error_label), run_time=.8)
        self.keep_stage(error_stage)
        self.play(Indicate(VGroup(error_span, error_label), color=ERROR,
                           scale_factor=1.16), run_time=.75)
        self.to(60)

    def integer_strip(self, lo, hi, width):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=GRID, stroke_width=3)
        ticks = VGroup(*[
            Line(UP * .07, DOWN * .07, color=GRID, stroke_width=.8,
                 stroke_opacity=.7).move_to(axis.point_from_proportion(i / 255))
            for i in range(256)
        ])
        labels = VGroup(txt(str(lo), 19, GRID).next_to(axis, LEFT, buff=.1),
                        txt(str(hi), 19, GRID).next_to(axis, RIGHT, buff=.1),
                        txt("integer q", 20, GRID).next_to(axis, DOWN, buff=.28))
        return VGroup(axis, ticks, labels)

    def sliding_ruler(self, values, width, color):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=color, stroke_width=3)
        marks = VGroup()
        for i, value in enumerate(values):
            point = axis.point_from_proportion(i / (len(values) - 1))
            marks.add(VGroup(
                Line(UP * .23, DOWN * .23, color=color, stroke_width=2.5).move_to(point),
                txt(str(value).replace("-", "−"), 21,
                    ERROR if value == 0 else color).next_to(point, UP, buff=.28),
            ))
        name = txt("real x ruler", 20, color).next_to(axis, DOWN, buff=.28)
        return VGroup(axis, marks, name)

    def symmetric_axes(self, width):
        real = NumberLine(x_range=[-1, 1, 1], length=width, include_numbers=False,
                          color=VALUE, stroke_width=3).shift(UP)
        integer = NumberLine(x_range=[-127, 127, 127], length=width,
                             include_numbers=False, color=GRID,
                             stroke_width=3).shift(DOWN)
        labels = VGroup(
            txt("−1", 20, VALUE).next_to(real, LEFT, buff=.1),
            txt("0", 20, ERROR).next_to(real.get_center(), UP, buff=.25),
            txt("1", 20, VALUE).next_to(real, RIGHT, buff=.1),
            txt("−127", 20, GRID).next_to(integer, LEFT, buff=.1),
            txt("0", 20, SNAP).next_to(integer.get_center(), DOWN, buff=.25),
            txt("127", 20, GRID).next_to(integer, RIGHT, buff=.1),
            txt("real x", 20, VALUE).next_to(real, UP, buff=.28),
            txt("integer q", 20, GRID).next_to(integer, DOWN, buff=.28),
        )
        return VGroup(real, integer, labels)

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
