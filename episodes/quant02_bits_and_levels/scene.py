"""Quantization 02: bits determine the number and spacing of levels."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE,
    QuantizationLine, pill, txt,
)


class BitsAndLevels(Scene):
    DURATION = 56

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  02", 20, MUTED).move_to(UP * 7.25),
            txt("8bit와 4bit는 실제로 무엇이 다를까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — continue directly from episode 1's final frame.
        self.text(
            "표현 가능한 숫자를 몇 개나 남길까요?",
            "앞에서는 Quantization이 표현 가능한 값의 종류를\n줄이는 과정이라고 했습니다.",
            "bit 수     ↓     표현 가능한 값의 개수",
        )
        fine = self.level_line(17, 6.7, VALUE).move_to([0, 1.0, 0])
        coarse = self.level_line(5, 6.7, GRID).move_to([0, -.75, 0])
        previous = VGroup(
            fine, coarse,
            txt("촘촘한 격자", 22, VALUE).next_to(fine, UP, buff=.28),
            txt("거친 격자", 22, GRID).next_to(coarse, UP, buff=.28),
        )
        self.play(FadeIn(previous), run_time=.85)
        relation = VGroup(
            pill("bit 수", SNAP, 1.65),
            txt("↓", 30, MUTED),
            pill("값의 개수", GRID, 2.25),
        ).arrange(DOWN, buff=.18).move_to([0, .1, 0])
        self.play(previous.animate.set_opacity(.18), FadeIn(relation, scale=.92), run_time=.8)
        self.play(Indicate(relation[-1], color=SNAP, scale_factor=1.08), run_time=.7)
        opening = VGroup(previous, relation)
        self.keep_stage(opening)
        self.to(7)

        # 7–15 s — one bit produces exactly two code words and two levels.
        self.text(
            "1bit에는 두 가지 상태가 있습니다",
            "bit 하나는 0 또는 1이므로,\n두 개의 값을 서로 구분할 수 있습니다.",
            "2¹ = 2 values",
        )
        codes_1 = VGroup(self.bit_code("0", VALUE), self.bit_code("1", VALUE))
        codes_1.arrange(RIGHT, buff=1.35).move_to([0, 1.55, 0])
        line_1 = self.level_line(2, 5.5, VALUE).move_to([0, -.35, 0])
        arrows_1 = VGroup(*[
            Arrow(codes_1[i].get_bottom(), line_1[i + 1].get_center(), buff=.15,
                  color=VALUE, stroke_width=2.4, tip_length=.12)
            for i in range(2)
        ])
        one_bit = VGroup(codes_1, line_1, arrows_1)
        self.play(FadeOut(opening), FadeIn(codes_1), Create(line_1[0]), run_time=.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_1], lag_ratio=.2),
                  LaggedStart(*[FadeIn(line_1[i + 1], scale=1.7) for i in range(2)],
                              lag_ratio=.2), run_time=.9)
        self.keep_stage(one_bit)
        self.play(Indicate(line_1[1:], color=SNAP, scale_factor=1.18), run_time=.75)
        self.to(15)

        # 15–24 s — two and three bits: each extra bit doubles the grid.
        self.text(
            "bit가 하나 늘면 격자는 두 배가 됩니다",
            "2bit는 네 개, 3bit는 여덟 개의 조합을 만들고\n각 조합이 하나의 위치에 대응합니다.",
            "2² = 4          2³ = 8          매번 ×2",
        )
        row_2 = self.code_level_row(2, ["00", "01", "10", "11"], 4, 5.8, VALUE)
        row_2.move_to([0, 1.55, 0])
        row_3 = self.code_level_row(3, ["000", "001", "010", "011",
                                             "100", "101", "110", "111"],
                                    8, 5.8, GRID)
        row_3.move_to([0, -.9, 0])
        doubling = VGroup(
            txt("4 positions", 20, VALUE).move_to([3.05, 1.2, 0]),
            txt("8 positions", 20, GRID).move_to([3.05, -1.25, 0]),
            Arrow([3.05, .75, 0], [3.05, -.45, 0], color=SNAP,
                  stroke_width=2.5, tip_length=.12),
            txt("×2", 24, SNAP).move_to([3.4, .15, 0]),
        )
        growth = VGroup(row_2, row_3, doubling)
        self.play(FadeOut(one_bit), FadeIn(row_2), run_time=.75)
        self.play(TransformFromCopy(row_2[2], row_3[2]), FadeIn(row_3[:2]),
                  FadeIn(doubling), run_time=1.0)
        self.keep_stage(growth)
        self.play(LaggedStart(*[Indicate(dot, color=SNAP, scale_factor=1.45)
                                for dot in row_3[2][1:]], lag_ratio=.06), run_time=.9)
        self.to(24)

        # 24–33 s — general rule and the 8-bit / 4-bit counts.
        self.text(
            "가능한 조합의 수는 2ⁿ입니다",
            "그래서 8bit는 256개,\n4bit는 16개의 값을 표현할 수 있습니다.",
            "8bit: 2⁸ = 256          4bit: 2⁴ = 16",
        )
        formula = VGroup(
            txt("n bits", 27, MUTED),
            txt("→", 31, SNAP),
            txt("2ⁿ values", 44, SNAP),
        ).arrange(RIGHT, buff=.3).move_to([0, 2.0, 0])
        count_8 = self.count_card("8bit", "256 values", VALUE).move_to([-2.05, -.2, 0])
        count_4 = self.count_card("4bit", "16 values", GRID).move_to([2.05, -.2, 0])
        rule = VGroup(formula, count_8, count_4)
        self.play(FadeOut(growth), FadeIn(formula, shift=DOWN * .12), run_time=.65)
        self.play(FadeIn(count_8), FadeIn(count_4), run_time=.7)
        self.keep_stage(rule)
        self.play(Indicate(formula[-1], color=SNAP, scale_factor=1.1),
                  Indicate(count_8[1], color=VALUE, scale_factor=1.05), run_time=.8)
        self.to(33)

        # 33–44 s — same range, visibly different spacing, and 0.43 snapping.
        self.text(
            "같은 범위라면 값의 간격이 달라집니다",
            "0부터 1까지 같은 범위를 나눠도 8bit 격자는 촘촘하고,\n4bit 격자는 더 거칩니다.",
            "input 0.43     →     8bit: 0.431     ·     4bit: 0.400",
        )
        axis_8 = self.dense_axis(256, 6.7, VALUE).move_to([0, 1.35, 0])
        axis_4 = self.dense_axis(16, 6.7, GRID).move_to([0, -1.05, 0])
        labels = VGroup(
            txt("8bit · 256", 22, VALUE).next_to(axis_8, UP, buff=.35).align_to(axis_8, LEFT),
            txt("4bit · 16", 22, GRID).next_to(axis_4, UP, buff=.35).align_to(axis_4, LEFT),
            txt("0", 18, MUTED).next_to(axis_8, LEFT, buff=.1),
            txt("1", 18, MUTED).next_to(axis_8, RIGHT, buff=.1),
            txt("0", 18, MUTED).next_to(axis_4, LEFT, buff=.1),
            txt("1", 18, MUTED).next_to(axis_4, RIGHT, buff=.1),
        )
        input_8 = Dot(axis_8[0].point_from_proportion(.43) + UP * .48,
                      radius=.095, color=ERROR)
        input_4 = Dot(axis_4[0].point_from_proportion(.43) + UP * .48,
                      radius=.095, color=ERROR)
        input_labels = VGroup(
            txt("0.43", 18, ERROR).next_to(input_8, UP, buff=.08),
            txt("0.43", 18, ERROR).next_to(input_4, UP, buff=.08),
        )
        target_8 = Dot(axis_8[0].point_from_proportion(round(.43 * 255) / 255),
                       radius=.12, color=SNAP)
        target_4 = Dot(axis_4[0].point_from_proportion(round(.43 * 15) / 15),
                       radius=.12, color=SNAP)
        snap_arrows = VGroup(
            Arrow(input_8.get_center(), target_8.get_center(), buff=.05,
                  color=SNAP, stroke_width=2, tip_length=.09),
            Arrow(input_4.get_center(), target_4.get_center(), buff=.05,
                  color=SNAP, stroke_width=2, tip_length=.09),
        )
        comparison = VGroup(axis_8, axis_4, labels, input_8, input_4, input_labels,
                            target_8, target_4, snap_arrows)
        self.play(FadeOut(rule), FadeIn(axis_8), FadeIn(axis_4), FadeIn(labels), run_time=.9)
        self.play(FadeIn(input_8), FadeIn(input_4), FadeIn(input_labels), run_time=.4)
        self.play(GrowArrow(snap_arrows[0]), GrowArrow(snap_arrows[1]),
                  TransformFromCopy(input_8, target_8),
                  TransformFromCopy(input_4, target_4), run_time=1.0)
        self.keep_stage(comparison)
        self.play(Indicate(target_8, color=GOOD, scale_factor=1.7),
                  Indicate(target_4, color=ERROR, scale_factor=1.7), run_time=.8)
        self.to(44)

        # 44–50 s — name the spacing: resolution.
        self.text(
            "이 간격이 Quantization의 해상도입니다",
            "bit 수가 줄면 저장 공간은 줄지만,\n가까운 값들을 구분하는 능력도 함께 떨어집니다.",
            "작은 간격 = 높은 resolution     ·     큰 간격 = 낮은 resolution",
        )
        close = self.spacing_demo(.42, VALUE).move_to([-2.05, .35, 0])
        wide = self.spacing_demo(1.15, GRID).move_to([2.05, .35, 0])
        resolution = VGroup(
            close, wide,
            txt("촘촘함", 23, VALUE).move_to([-2.05, -1.15, 0]),
            txt("거침", 23, GRID).move_to([2.05, -1.15, 0]),
        )
        self.play(FadeOut(comparison), FadeIn(resolution), run_time=.75)
        self.keep_stage(resolution)
        self.play(Indicate(close[-1], color=VALUE, scale_factor=1.1),
                  Indicate(wide[-1], color=GRID, scale_factor=1.1), run_time=.75)
        self.to(50)

        # 50–56 s — keep 8 bits fixed and change only the represented range.
        self.text(
            "같은 8bit라도 간격은 달라질 수 있습니다",
            "256개 위치를 어떤 숫자 범위에 맞추느냐에 따라\n실제 값 사이의 간격은 완전히 달라집니다.",
            "NEXT  ·  실수 범위와 정수 격자를 연결하는 scale",
        )
        narrow = self.range_bar("0  ~  1", "같은 256개 · 촘촘함", VALUE, 4.0)
        narrow.move_to([0, 1.25, 0])
        wide_range = self.range_bar("−100  ~  100", "같은 256개 · 성김", GRID, 6.8)
        wide_range.move_to([0, -.85, 0])
        ranges = VGroup(narrow, wide_range)
        self.play(FadeOut(resolution), FadeIn(narrow), run_time=.55)
        self.play(TransformFromCopy(narrow[1], wide_range[1]), FadeIn(wide_range[0]),
                  FadeIn(wide_range[2]), run_time=.85)
        self.keep_stage(ranges)
        self.play(Indicate(wide_range[0], color=SNAP, scale_factor=1.06), run_time=.75)
        self.to(56)

    def level_line(self, count, width, color):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=MUTED, stroke_width=2.5)
        marks = VGroup(*[
            VGroup(Line(UP * .17, DOWN * .17, color=color, stroke_width=3),
                   Dot(radius=.055, color=color)).move_to(axis.point_from_proportion(i / (count - 1)))
            for i in range(count)
        ])
        return VGroup(axis, *marks)

    def dense_axis(self, count, width, color):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=MUTED, stroke_width=2.2)
        ticks = VGroup(*[
            Line(UP * (.14 if i % max(1, (count - 1) // 8) == 0 else .075),
                 DOWN * (.14 if i % max(1, (count - 1) // 8) == 0 else .075),
                 color=color, stroke_width=.9 if count > 32 else 2.0,
                 stroke_opacity=.72).move_to(axis.point_from_proportion(i / (count - 1)))
            for i in range(count)
        ])
        return VGroup(axis, ticks)

    def bit_code(self, code, color, width=.88):
        box = RoundedRectangle(width=width, height=.72, corner_radius=.13,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.09)
        return VGroup(box, txt(code, 28, color, width - .12))

    def code_level_row(self, bits, codes, count, width, color):
        visible_codes = VGroup(*[self.bit_code(code, color, .62 if bits == 3 else .8)
                                 for code in codes])
        visible_codes.arrange(RIGHT, buff=.08).scale(.75)
        line = self.level_line(count, width, color)
        line.next_to(visible_codes, DOWN, buff=.32)
        return VGroup(txt(f"{bits}bit", 22, color).next_to(visible_codes, LEFT, buff=.22),
                      visible_codes, line)

    def count_card(self, title, count, color):
        box = RoundedRectangle(width=3.25, height=2.0, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box, txt(title, 34, color).move_to(box.get_center() + UP * .4),
                      txt(count, 27, INK).move_to(box.get_center() + DOWN * .42))

    def spacing_demo(self, gap, color):
        marks = VGroup(*[
            VGroup(Line(UP * .32, DOWN * .32, color=color, stroke_width=3),
                   Dot(radius=.075, color=color)).move_to([(i - 2) * gap, 0, 0])
            for i in range(5)
        ])
        span = DoubleArrow(marks[2].get_center() + DOWN * .65,
                           marks[3].get_center() + DOWN * .65,
                           buff=.03, color=SNAP, stroke_width=2, tip_length=.09)
        label = txt("resolution", 20, SNAP).next_to(span, DOWN, buff=.14)
        return VGroup(marks, span, label)

    def range_bar(self, range_text, detail, color, width):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=color, stroke_width=4)
        ends = VGroup(Line(UP * .22, DOWN * .22, color=color, stroke_width=4),
                      Line(UP * .22, DOWN * .22, color=color, stroke_width=4))
        ends[0].move_to(axis.get_start())
        ends[1].move_to(axis.get_end())
        title = txt(range_text, 27, color).next_to(axis, UP, buff=.3)
        subtitle = txt(detail, 20, MUTED).next_to(axis, DOWN, buff=.28)
        return VGroup(title, VGroup(axis, ends), subtitle)

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
