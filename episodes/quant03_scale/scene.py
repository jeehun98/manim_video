"""Quantization 03: scale is the real-world size of one integer step."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE,
    MappedAxes, pill, txt,
)


class QuantizationScale(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  03", 20, MUTED).move_to(UP * 7.25),
            txt("정수 1칸은 실제 값으로 얼마를 의미할까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — resume episode 2: same 256 positions, different ranges.
        self.text(
            "같은 8bit라도 간격은 달라질 수 있습니다",
            "256개 위치를 어떤 실수 범위에 배치하느냐에 따라\n한 칸이 의미하는 실제 크기가 달라집니다.",
            "정수 한 칸의 실제 크기     =     scale",
        )
        ranges = VGroup(
            self.range_row("0  ~  1", "256 positions", VALUE, 4.0),
            self.range_row("−100  ~  100", "256 positions", GRID, 6.8),
        ).arrange(DOWN, buff=.9).move_to([0, .2, 0])
        self.play(FadeIn(ranges[0]), FadeIn(ranges[1]), run_time=.8)
        scale_pill = pill("SCALE", SNAP, 2.0).move_to([0, -2.15, 0])
        self.play(FadeIn(scale_pill, shift=UP * .12),
                  Indicate(ranges, color=SNAP, scale_factor=1.025), run_time=.8)
        opening = VGroup(ranges, scale_pill)
        self.keep_stage(opening)
        self.to(7)

        # 7–15 s — align a real axis with the 8-bit integer axis.
        self.text(
            "실수 범위를 256개 정수 위치에 대응시킵니다",
            "예를 들어 0부터 1까지의 실수 범위를\n0부터 255까지의 정수 위치에 맞춥니다.",
            "real 0…1     ↔     integer 0…255",
        )
        axes = MappedAxes((0, 1), (0, 255), width=6.6).move_to([0, .15, 0])
        mapping_label = pill("256 positions", GRID, 2.55).move_to([0, -2.25, 0])
        self.play(FadeOut(opening), Create(axes.real_axis), Create(axes.int_axis),
                  FadeIn(axes.end_labels), run_time=.7)
        self.play(FadeIn(axes.int_ticks), Create(axes.connectors),
                  FadeIn(axes.axis_names), FadeIn(mapping_label), run_time=.95)
        axes_stage = VGroup(axes, mapping_label)
        self.keep_stage(axes_stage)
        self.play(Indicate(axes.connectors, color=SNAP, scale_factor=1.04), run_time=.7)
        self.to(15)

        # 15–23 s — zoom into q=0,1,2,3 and name a single step.
        self.text(
            "정수 1칸마다 실제 값이 약 0.0039 증가합니다",
            "정수 값이 1 증가할 때 실제 값이 얼마나 증가하는지,\n그 한 칸의 크기가 바로 scale입니다.",
            "scale = 1 ÷ 255 ≈ 0.0039",
        )
        qs = (0, 1, 2, 3)
        xs = (0.0000, 1 / 255, 2 / 255, 3 / 255)
        columns = VGroup(*[
            VGroup(
                txt(f"x ≈ {x:.4f}", 21, VALUE),
                Arrow(DOWN * .05, DOWN * .62, buff=0, color=MUTED,
                      stroke_width=1.8, tip_length=.09),
                self.code_box(f"q = {q}", GRID),
            ).arrange(DOWN, buff=.17)
            for q, x in zip(qs, xs)
        ]).arrange(RIGHT, buff=.22).scale(.92).move_to([0, .35, 0])
        bracket = BraceBetweenPoints(columns[0][0].get_bottom() + DOWN * .15,
                                     columns[1][0].get_bottom() + DOWN * .15,
                                     direction=DOWN, color=SNAP)
        step_label = txt("scale", 23, SNAP).next_to(bracket, DOWN, buff=.12)
        zoom = VGroup(columns, bracket, step_label)
        self.play(FadeOut(axes_stage), LaggedStart(*[FadeIn(c, shift=UP * .1)
                                                    for c in columns], lag_ratio=.12),
                  run_time=.95)
        self.play(GrowFromCenter(bracket), FadeIn(step_label), run_time=.6)
        self.keep_stage(zoom)
        self.play(Indicate(VGroup(bracket, step_label), color=SNAP, scale_factor=1.12),
                  run_time=.75)
        self.to(23)

        # 23–31 s — introduce only the origin-aligned scale equation.
        self.text(
            "실제 값은 정수 값에 scale을 곱해 해석합니다",
            "두 축의 0이 일치하는 가장 단순한 경우에는\n정수 q에 scale s를 곱해 실제 값 x를 복원합니다.",
            "정수 한 칸이 실제 세계에서 얼마짜리인가?",
        )
        formula = VGroup(
            txt("x", 60, VALUE), txt("≈", 47, MUTED),
            txt("s", 60, SNAP), txt("·", 48, MUTED), txt("q", 60, GRID),
        ).arrange(RIGHT, buff=.24).move_to([0, 1.0, 0])
        under = VGroup(
            txt("실제 값", 21, VALUE).next_to(formula[0], DOWN, buff=.45),
            txt("scale", 21, SNAP).next_to(formula[2], DOWN, buff=.45),
            txt("정수 값", 21, GRID).next_to(formula[4], DOWN, buff=.45),
        )
        guides = VGroup(*[
            DashedLine(formula[i].get_bottom(), under[j].get_top(),
                       color=(VALUE, SNAP, GRID)[j], stroke_width=1.5, dash_length=.07)
            for j, i in enumerate((0, 2, 4))
        ])
        equation = VGroup(formula, under, guides)
        self.play(FadeOut(zoom), LaggedStart(*[FadeIn(m, shift=UP * .08)
                                              for m in formula], lag_ratio=.08), run_time=.75)
        self.play(FadeIn(under), Create(guides), run_time=.65)
        self.keep_stage(equation)
        self.play(Indicate(formula[2], color=SNAP, scale_factor=1.22), run_time=.75)
        self.to(31)

        # 31–39 s — same q grid, but two ranges give two scales.
        self.text(
            "범위가 넓어지면 scale도 커집니다",
            "같은 8bit라도 0부터 1과 0부터 100에서는\n정수 한 칸이 의미하는 실제 크기가 다릅니다.",
            "0…1: s ≈ 0.0039          0…100: s ≈ 0.392",
        )
        small_scale = self.scale_card("0  ~  1", "1 q-step", "≈ 0.0039", VALUE)
        large_scale = self.scale_card("0  ~  100", "1 q-step", "≈ 0.392", GRID)
        scale_compare = VGroup(small_scale, large_scale).arrange(RIGHT, buff=.45)
        scale_compare.move_to([0, .35, 0])
        self.play(FadeOut(equation), FadeIn(small_scale), run_time=.55)
        self.play(TransformFromCopy(small_scale[1], large_scale[1]),
                  FadeIn(large_scale[0]), FadeIn(large_scale[2]),
                  FadeIn(large_scale[3]), FadeIn(large_scale[4]), run_time=.75)
        self.keep_stage(scale_compare)
        self.play(Indicate(large_scale[-1], color=SNAP, scale_factor=1.12), run_time=.8)
        self.to(39)

        # 39–49 s — quantize 0.43, then interpret q=110 back through the scale.
        self.text(
            "입력은 정수 위치로 갔다가 근사값으로 해석됩니다",
            "0.43을 scale 기준으로 가장 가까운 정수에 대응시키면\nq는 110, 다시 해석한 값은 약 0.431입니다.",
            "0.43     →     q = 110     →     110 × 1/255 ≈ 0.431",
        )
        flow = VGroup(
            self.flow_card("실수 input", "x = 0.43", VALUE),
            self.flow_arrow("quantize"),
            self.flow_card("정수 code", "q = 110", GRID),
            self.flow_arrow("× scale"),
            self.flow_card("근사 실수", "x̂ ≈ 0.431", SNAP),
        ).arrange(DOWN, buff=.18).scale(.92).move_to([0, .2, 0])
        self.play(FadeOut(scale_compare), FadeIn(flow[0]), run_time=.4)
        self.play(GrowArrow(flow[1][0]), FadeIn(flow[1][1]), FadeIn(flow[2]), run_time=.7)
        self.play(GrowArrow(flow[3][0]), FadeIn(flow[3][1]), FadeIn(flow[4]), run_time=.7)
        self.keep_stage(flow)
        self.play(Indicate(flow[2], color=GRID, scale_factor=1.05),
                  Indicate(flow[4], color=SNAP, scale_factor=1.05), run_time=.75)
        self.to(49)

        # 49–55 s — summarize the one idea.
        self.text(
            "Scale은 정수 한 칸의 실제 크기입니다",
            "작은 scale은 촘촘한 구분을 만들고, 큰 scale은\n더 넓은 범위를 담는 대신 간격을 키웁니다.",
            "small scale → 촘촘함     ·     large scale → 넓은 범위",
        )
        summary = VGroup(
            txt("SCALE", 29, SNAP),
            txt("=", 38, MUTED),
            txt("한 칸의 실제 크기", 42, INK),
        ).arrange(DOWN, buff=.28).move_to([0, .65, 0])
        choices = VGroup(
            pill("small · fine", VALUE, 2.5),
            pill("large · wide", GRID, 2.5),
        ).arrange(RIGHT, buff=.45).move_to([0, -1.35, 0])
        summary_stage = VGroup(summary, choices)
        self.play(FadeOut(flow), FadeIn(summary, scale=.92), FadeIn(choices), run_time=.8)
        self.keep_stage(summary_stage)
        self.play(Indicate(summary[-1], color=SNAP, scale_factor=1.08), run_time=.75)
        self.to(55)

        # 55–60 s — ask where real zero belongs when the origins do not align.
        self.text(
            "하지만 실제 범위는 항상 0에서 시작하지 않습니다",
            "−1부터 3을 0부터 255에 대응시키면\n실수 0은 정수의 어느 위치에 놓여야 할까요?",
            "NEXT  ·  0의 위치를 정하는 zero point",
        )
        shifted = MappedAxes((-1, 3), (0, 255), width=6.5).move_to([0, .2, 0])
        zero_real = shifted.real_point(0)
        zero_dot = Dot(zero_real, radius=.12, color=ERROR)
        zero_label = txt("real 0", 22, ERROR).next_to(zero_dot, UP, buff=.22)
        unknown = txt("q = ?", 26, SNAP).move_to(
            shifted.int_axis.point_from_proportion(.25) + DOWN * .58)
        question_line = DashedLine(zero_dot.get_bottom(), unknown.get_top(),
                                   color=ERROR, stroke_width=2, dash_length=.09)
        next_stage = VGroup(shifted, zero_dot, zero_label, unknown, question_line)
        self.play(FadeOut(summary_stage), FadeIn(shifted), FadeIn(zero_dot),
                  FadeIn(zero_label), Create(question_line), FadeIn(unknown), run_time=.9)
        self.keep_stage(next_stage)
        self.play(Indicate(VGroup(zero_dot, unknown), color=SNAP, scale_factor=1.1),
                  run_time=.75)
        self.to(60)

    def range_row(self, range_text, count_text, color, width):
        axis = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=4)
        ends = VGroup(Line(UP * .22, DOWN * .22, color=color, stroke_width=4),
                      Line(UP * .22, DOWN * .22, color=color, stroke_width=4))
        ends[0].move_to(axis.get_start())
        ends[1].move_to(axis.get_end())
        return VGroup(
            txt(range_text, 28, color).next_to(axis, UP, buff=.25),
            VGroup(axis, ends),
            txt(count_text, 20, MUTED).next_to(axis, DOWN, buff=.24),
        )

    def code_box(self, text, color):
        box = RoundedRectangle(width=1.55, height=.66, corner_radius=.13,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.09)
        return VGroup(box, txt(text, 21, color, 1.38))

    def scale_card(self, real_range, q_step, real_step, color):
        box = RoundedRectangle(width=3.35, height=2.55, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        step_line = VGroup(
            Dot(radius=.08, color=GRID),
            DoubleArrow(LEFT * .52, RIGHT * .52, buff=.09, color=SNAP,
                        stroke_width=2, tip_length=.08),
            Dot(radius=.08, color=GRID),
        ).arrange(RIGHT, buff=0).move_to(box.get_center())
        return VGroup(
            box,
            step_line,
            txt(real_range, 27, color).move_to(box.get_center() + UP * .78),
            txt(q_step, 18, MUTED).move_to(box.get_center() + UP * .12),
            txt(real_step, 28, SNAP).move_to(box.get_center() + DOWN * .78),
        )

    def flow_card(self, title, value, color):
        box = RoundedRectangle(width=3.5, height=1.05, corner_radius=.18,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box,
                      txt(title, 18, MUTED).move_to(box.get_center() + UP * .25),
                      txt(value, 28, color).move_to(box.get_center() + DOWN * .2))

    def flow_arrow(self, label):
        arrow = Arrow(UP * .25, DOWN * .25, buff=0, color=SNAP,
                      stroke_width=2.5, tip_length=.11)
        return VGroup(arrow, txt(label, 18, SNAP).next_to(arrow, RIGHT, buff=.18))

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
