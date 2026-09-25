"""Quantization 05: snapping error and many-to-one information loss."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class QuantizationError(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  05", 20, MUTED).move_to(UP * 7.25),
            txt("Quantization을 하면 원래 숫자에서 무엇이 사라질까?", 31).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — resume the final frame from zero point.
        self.text(
            "원래 값이 격자 위에 없다면 어떻게 될까요?",
            "Scale과 zero point로 실수 격자의 위치를 정해도\n모든 입력이 격자 위에 정확히 놓이지는 않습니다.",
            "x = 0.43     →     nearest grid = 0.44",
        )
        previous = self.snap_example(.38, .48, .02, .43, .44, 6.0)
        previous.move_to([0, .25, 0])
        self.play(FadeIn(previous[0]), FadeIn(previous[1]),
                  FadeIn(previous[2]), FadeIn(previous[3]),
                  FadeIn(previous[4]), run_time=.7)
        self.play(GrowArrow(previous[-2]), FadeIn(previous[-1]), run_time=.6)
        self.keep_stage(previous)
        self.play(Indicate(previous[-1], color=ERROR, scale_factor=1.15), run_time=.75)
        self.to(7)

        # 7–15 s — zoom into a simple coarse grid and snap 0.43 to 0.45.
        self.text(
            "Quantization은 가장 가까운 격자를 선택합니다",
            "확대해서 보면 원래 값 0.43은 표현 가능한 위치 중\n더 가까운 0.45로 이동할 수 있습니다.",
            "0.43     →     0.45",
        )
        axis = NumberLine(x_range=[.40, .50, .05], length=6.2,
                          include_numbers=False, color=MUTED,
                          stroke_width=2.5).move_to([0, .25, 0])
        ticks = VGroup(*[
            VGroup(Line(UP * .28, DOWN * .28, color=GRID, stroke_width=3),
                   txt(f"{v:.2f}", 22, GRID).shift(DOWN * .58)).move_to(axis.n2p(v))
            for v in (.40, .45, .50)
        ])
        source = Dot(axis.n2p(.43), radius=.13, color=VALUE)
        source_label = txt("0.43", 25, VALUE).next_to(source, UP, buff=.3)
        ghost = source.copy().set_opacity(.22)
        target = Dot(axis.n2p(.45), radius=.16, color=SNAP)
        target_label = txt("0.45", 25, SNAP).next_to(target, UP, buff=.3)
        move_arrow = CurvedArrow(source.get_center() + UP * .12,
                                 target.get_center() + UP * .12,
                                 angle=-TAU / 8, color=SNAP,
                                 stroke_width=2.5, tip_length=.12)
        snap = VGroup(axis, ticks, ghost, source, source_label,
                      target, target_label, move_arrow)
        self.play(FadeOut(previous), FadeIn(axis), FadeIn(ticks),
                  FadeIn(source), FadeIn(source_label), run_time=.7)
        self.play(FadeIn(ghost), Create(move_arrow),
                  Transform(source, target), Transform(source_label, target_label),
                  run_time=1.1, rate_func=smooth)
        self.keep_stage(snap)
        self.play(Flash(target.get_center(), color=SNAP, flash_radius=.42), run_time=.65)
        self.to(15)

        # 15–22 s — define signed quantization error.
        self.text(
            "두 값의 차이가 Quantization Error입니다",
            "표현된 값에서 원래 값을 뺀 차이를 e라고 하면,\n이 예시의 error는 0.02입니다.",
            "e = x̂ − x = 0.45 − 0.43 = 0.02",
        )
        original = Dot([-1.45, .55, 0], radius=.14, color=VALUE)
        represented = Dot([1.45, .55, 0], radius=.16, color=SNAP)
        distance = DoubleArrow(original.get_center(), represented.get_center(),
                               buff=.12, color=ERROR, stroke_width=3,
                               tip_length=.13)
        error_def = VGroup(
            original, represented, distance,
            txt("0.43", 28, VALUE).next_to(original, UP, buff=.28),
            txt("0.45", 28, SNAP).next_to(represented, UP, buff=.28),
            pill("difference = 0.02", ERROR, 3.15).move_to([0, -1.0, 0]),
        )
        self.play(FadeOut(snap), FadeIn(original), FadeIn(represented),
                  GrowArrow(distance), FadeIn(error_def[3]),
                  FadeIn(error_def[4]), FadeIn(error_def[5]), run_time=.9)
        self.keep_stage(error_def)
        self.play(Indicate(error_def[-1], color=ERROR, scale_factor=1.1), run_time=.75)
        self.to(22)

        # 22–32 s — multiple real values collapse into the same 0.50 code.
        self.text(
            "서로 다른 여러 값이 하나의 값으로 합쳐집니다",
            "0.50 주변의 서로 다른 입력들도 가장 가까운 격자를\n선택하면 모두 같은 0.50으로 표현될 수 있습니다.",
            "many real values     →     one quantized value",
        )
        values = (.46, .48, .49, .51, .53)
        line = NumberLine(x_range=[.40, .60, .10], length=6.6,
                          include_numbers=False, color=MUTED,
                          stroke_width=2.4).move_to([0, -.25, 0])
        grid = VGroup(*[
            VGroup(Line(UP * .3, DOWN * .3, color=GRID, stroke_width=3.5),
                   txt(f"{v:.2f}", 21, GRID).shift(DOWN * .62)).move_to(line.n2p(v))
            for v in (.40, .50, .60)
        ])
        dots = VGroup(*[Dot(line.n2p(v) + UP * (1.2 + .32 * (i % 2)),
                            radius=.105, color=VALUE)
                        for i, v in enumerate(values)])
        labels = VGroup(*[txt(f"{v:.2f}", 19, VALUE).next_to(dots[i], UP, buff=.12)
                          for i, v in enumerate(values)])
        merge_arrows = VGroup(*[
            Arrow(d.get_bottom(), line.n2p(.50) + UP * .16, buff=.06,
                  color=SNAP, stroke_width=2, tip_length=.09)
            for d in dots
        ])
        merged = Dot(line.n2p(.50), radius=.19, color=SNAP)
        many_to_one = VGroup(line, grid, dots, labels, merge_arrows, merged)
        self.play(FadeOut(error_def), FadeIn(line), FadeIn(grid),
                  LaggedStart(*[FadeIn(d, scale=.7) for d in dots], lag_ratio=.1),
                  FadeIn(labels), run_time=.85)
        self.play(LaggedStart(*[GrowArrow(a) for a in merge_arrows], lag_ratio=.08),
                  run_time=.75)
        self.play(*[d.animate.move_to(line.n2p(.50)) for d in dots],
                  FadeOut(labels), run_time=1.1)
        self.play(FadeOut(dots), FadeOut(merge_arrows), FadeIn(merged, scale=1.8),
                  Flash(merged, color=SNAP, flash_radius=.48), run_time=.7)
        self.keep_stage(many_to_one)
        self.to(32)

        # 32–39 s — show irreversibility: one output has several possible inputs.
        self.text(
            "합쳐진 뒤에는 원래 값을 구분할 수 없습니다",
            "Quantization 이후 0.50만 보면 원래 값이 0.48인지,\n0.49인지, 0.51인지 완전히 복원할 수 없습니다.",
            "information loss     ·     many-to-one mapping",
        )
        inputs = VGroup(*[pill(f"{v:.2f}", VALUE, 1.25) for v in (.48, .49, .51)])
        inputs.arrange(DOWN, buff=.23).move_to([-2.15, .35, 0])
        output = pill("0.50", SNAP, 1.55).move_to([2.15, .35, 0])
        forward = VGroup(*[
            Arrow(card.get_right(), output.get_left(), buff=.12,
                  color=SNAP, stroke_width=2.3, tip_length=.11)
            for card in inputs
        ])
        reverse = VGroup(
            CurvedArrow(output.get_left() + DOWN * .35, [-1.35, -1.45, 0],
                        angle=-TAU / 8, color=ERROR, stroke_width=2,
                        tip_length=.1),
            txt("어느 값이었을까?", 22, ERROR).move_to([0, -1.75, 0]),
            txt("?", 34, ERROR).move_to([-1.75, -1.45, 0]),
        )
        loss = VGroup(inputs, output, forward, reverse)
        self.play(FadeOut(many_to_one), FadeIn(inputs), FadeIn(output),
                  LaggedStart(*[GrowArrow(a) for a in forward], lag_ratio=.1), run_time=.85)
        self.play(Create(reverse[0]), FadeIn(reverse[1:]), run_time=.65)
        self.keep_stage(loss)
        self.play(Indicate(reverse, color=ERROR, scale_factor=1.05), run_time=.7)
        self.to(39)

        # 39–47 s — nearest rounding bounds the error to half a step.
        self.text(
            "최근접 반올림의 최대 오차는 반 칸입니다",
            "Clipping 없이 가장 가까운 격자를 고르면 오차의 크기는\n보통 격자 간격 Δ의 절반을 넘지 않습니다.",
            "|e| ≤ Δ / 2",
        )
        left_grid = np.array([-2.8, .35, 0])
        right_grid = np.array([2.8, .35, 0])
        midpoint = np.array([0, .35, 0])
        step_line = Line(left_grid, right_grid, color=MUTED, stroke_width=3)
        endpoints = VGroup(Dot(left_grid, radius=.15, color=GRID),
                           Dot(right_grid, radius=.15, color=GRID))
        midpoint_mark = VGroup(
            Line(midpoint + UP * .28, midpoint + DOWN * .28,
                 color=ERROR, stroke_width=2.5),
            txt("midpoint", 19, ERROR).next_to(midpoint, UP, buff=.35),
        )
        delta = DoubleArrow(left_grid + DOWN * .65, right_grid + DOWN * .65,
                            buff=.03, color=SNAP, stroke_width=2.5,
                            tip_length=.1)
        halves = VGroup(
            BraceBetweenPoints(left_grid + UP * .5, midpoint + UP * .5,
                               direction=UP, color=VALUE),
            BraceBetweenPoints(midpoint + UP * .5, right_grid + UP * .5,
                               direction=UP, color=VALUE),
            txt("Δ/2", 22, VALUE).move_to([-1.4, 1.25, 0]),
            txt("Δ/2", 22, VALUE).move_to([1.4, 1.25, 0]),
            txt("step size  Δ", 22, SNAP).next_to(delta, DOWN, buff=.16),
        )
        bound = VGroup(step_line, endpoints, midpoint_mark, delta, halves)
        self.play(FadeOut(loss), FadeIn(step_line), FadeIn(endpoints),
                  FadeIn(midpoint_mark), GrowArrow(delta), FadeIn(halves), run_time=.95)
        self.keep_stage(bound)
        self.play(Indicate(halves[:4], color=VALUE, scale_factor=1.06), run_time=.75)
        self.to(47)

        # 47–54 s — reconnect bit count to possible movement distance.
        self.text(
            "같은 범위라면 촘촘한 격자가 오차를 줄입니다",
            "8bit는 입력과 가까운 위치를 고를 수 있지만, 4bit에서는\n같은 입력이 더 먼 위치로 이동할 수 있습니다.",
            "more bits → smaller Δ → smaller possible error",
        )
        dense = self.bit_error_row("8bit · 256", 256, .43, round(.43 * 255) / 255,
                                   VALUE).move_to([0, 1.25, 0])
        coarse = self.bit_error_row("4bit · 16", 16, .43, round(.43 * 15) / 15,
                                    GRID).move_to([0, -1.15, 0])
        bit_compare = VGroup(dense, coarse)
        self.play(FadeOut(bound), FadeIn(dense), FadeIn(coarse), run_time=.95)
        self.keep_stage(bit_compare)
        self.play(Indicate(dense[-1], color=GOOD, scale_factor=1.15),
                  Indicate(coarse[-1], color=ERROR, scale_factor=1.15), run_time=.8)
        self.to(54)

        # 54–60 s — bit count is not enough; range also controls step size.
        self.text(
            "하지만 error는 bit 수만으로 결정되지 않습니다",
            "같은 8bit라도 표현 범위가 넓어지면 한 칸의 크기 Δ가\n커지고, 가능한 Quantization Error도 함께 커집니다.",
            "NEXT  ·  Range와 Resolution의 관계",
        )
        narrow = self.range_resolution_row("Range  −1…1", "256 values", "Δ ≈ 0.0078",
                                           VALUE, True).move_to([0, 1.2, 0])
        wide = self.range_resolution_row("Range  −100…100", "256 values", "Δ ≈ 0.784",
                                         GRID, False).move_to([0, -1.15, 0])
        next_stage = VGroup(narrow, wide)
        self.play(FadeOut(bit_compare), FadeIn(narrow), FadeIn(wide), run_time=.9)
        self.keep_stage(next_stage)
        self.play(Indicate(wide[-1], color=SNAP, scale_factor=1.1), run_time=.75)
        self.to(60)

    def snap_example(self, lo, hi, step, x, xhat, width):
        axis = NumberLine(x_range=[lo, hi, step], length=width,
                          include_numbers=False, color=MUTED, stroke_width=2.5)
        ticks = VGroup(*[
            Line(UP * .23, DOWN * .23, color=GRID, stroke_width=3).move_to(axis.n2p(v))
            for v in np.arange(lo, hi + step / 2, step)
        ])
        source = Dot(axis.n2p(x), radius=.13, color=VALUE)
        target = Dot(axis.n2p(xhat), radius=.16, color=SNAP)
        labels = VGroup(txt(f"{x:.2f}", 23, VALUE).next_to(source, UP, buff=.28),
                        txt(f"{xhat:.2f}", 23, SNAP).next_to(target, DOWN, buff=.28))
        arrow = DoubleArrow(source.get_center() + UP * .62,
                            target.get_center() + UP * .62,
                            buff=.02, color=ERROR, stroke_width=2.3,
                            tip_length=.08)
        error = txt("error", 22, ERROR).next_to(arrow, UP, buff=.1)
        return VGroup(axis, ticks, source, target, labels, arrow, error)

    def bit_error_row(self, title, count, x, xhat, color):
        width = 6.4
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=MUTED, stroke_width=2.2)
        ticks = VGroup(*[
            Line(UP * (.13 if count <= 16 else .07),
                 DOWN * (.13 if count <= 16 else .07),
                 color=color, stroke_width=1.8 if count <= 16 else .7,
                 stroke_opacity=.75).move_to(axis.point_from_proportion(i / (count - 1)))
            for i in range(count)
        ])
        source = Dot(axis.point_from_proportion(x) + UP * .45,
                     radius=.095, color=ERROR)
        target = Dot(axis.point_from_proportion(xhat), radius=.12, color=SNAP)
        arrow = Arrow(source.get_center(), target.get_center(), buff=.04,
                      color=SNAP, stroke_width=2, tip_length=.09)
        return VGroup(axis, ticks,
                      txt(title, 21, color).next_to(axis, UP, buff=.32).align_to(axis, LEFT),
                      source, target, arrow)

    def range_resolution_row(self, title, count, delta, color, dense):
        width = 6.3
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=MUTED, stroke_width=2.2)
        n = 33 if dense else 7
        ticks = VGroup(*[
            Line(UP * .13, DOWN * .13, color=color, stroke_width=1.6)
            .move_to(axis.point_from_proportion(i / (n - 1)))
            for i in range(n)
        ])
        return VGroup(axis, ticks,
                      txt(title, 21, color).next_to(axis, UP, buff=.3).align_to(axis, LEFT),
                      txt(count, 18, MUTED).next_to(axis, DOWN, buff=.26).align_to(axis, LEFT),
                      pill(delta, SNAP, 2.15).next_to(axis, DOWN, buff=.2).align_to(axis, RIGHT))

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
