"""Quantization 01: limiting the set of representable values."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE,
    QuantizationLine, ValueDot, pill, txt, value_dots,
)


class WhatIsQuantization(Scene):
    DURATION = 52
    VALUES = (.17, .21, .24, .31, .36)
    LEVELS = (0, .25, .50, .75, 1.0)

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  01", 20, MUTED).move_to(UP * 7.25),
            txt("Quantization은 숫자를 어떻게 줄이는 걸까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — hook: five distinct nearby values.
        self.text(
            "이 숫자들을 전부 구분해야 할까요?",
            "AI 모델 안에는 서로 아주 가까운 숫자들이\n수없이 많이 들어 있습니다.",
            "0.17   ·   0.21   ·   0.24   ·   0.31   ·   0.36",
        )
        line = QuantizationLine(width=7.0, show_labels=False).move_to([0, .25, 0])
        dots = value_dots(self.VALUES, line, alternating=True)
        hook = VGroup(line, dots)
        self.play(Create(line.axis), LaggedStart(*[FadeIn(d, scale=.7) for d in dots],
                                                 lag_ratio=.12), run_time=1.35)
        self.play(LaggedStart(*[Indicate(d.dot, color=SNAP, scale_factor=1.7)
                                for d in dots], lag_ratio=.1), run_time=1.0)
        self.to(7)

        # 7–14 s — a real interval has extremely dense possible values.
        self.text(
            "실수의 표현 공간은 아주 촘촘합니다",
            "0.21과 0.22도 다르고,\n0.221과 0.222도 서로 다른 값입니다.",
            "값과 값 사이에도 또 다른 값이 있습니다",
        )
        dense_line = QuantizationLine(width=7.0, show_labels=False).move_to([0, .3, 0])
        dense_values = [0.10 + i * .02 for i in range(41)]
        dense_ticks = VGroup(*[
            Line(dense_line.point(v, -.10), dense_line.point(v, .10),
                 color=VALUE, stroke_width=1.6, stroke_opacity=.75)
            for v in dense_values
        ])
        magnified = VGroup(
            txt("0.221", 25, VALUE).move_to([-1.2, 1.2, 0]),
            txt("0.222", 25, VALUE).move_to([1.2, 1.2, 0]),
            DoubleArrow([-0.72, 1.2, 0], [0.72, 1.2, 0], buff=0,
                        color=MUTED, stroke_width=2, tip_length=.1),
        )
        dense = VGroup(dense_line, dense_ticks, magnified)
        self.play(FadeOut(hook), FadeIn(dense_line.axis),
                  LaggedStart(*[Create(t) for t in dense_ticks], lag_ratio=.018), run_time=1.0)
        self.play(FadeIn(magnified), run_time=.55)
        self.keep_stage(dense)
        self.to(14)

        # 14–22 s — introduce only the allowed positions.
        self.text(
            "Quantization은 사용할 위치를 제한합니다",
            "이제 아무 숫자나 표현하는 대신,\n정해진 위치 중 하나를 선택해야 합니다.",
            "표현 가능한 위치",
        )
        grid_line = QuantizationLine(width=7.0, grid_values=self.LEVELS).move_to([0, .2, 0])
        grid_title = pill("5개의 대표값", GRID, 2.45).move_to([0, 1.55, 0])
        self.play(FadeOut(dense), FadeIn(grid_line.axis), run_time=.45)
        self.play(LaggedStart(*[FadeIn(g, scale=1.6) for g in grid_line.grid], lag_ratio=.13),
                  LaggedStart(*[FadeIn(l) for l in grid_line.labels], lag_ratio=.13),
                  FadeIn(grid_title, shift=DOWN * .12), run_time=1.15)
        self.keep_stage(grid_line, grid_title)
        self.play(Indicate(grid_line.grid, color=SNAP, scale_factor=1.08), run_time=.8)
        self.to(22)

        # 22–33 s — main visual: all five values snap into one representative.
        self.text(
            "가까운 값들은 같은 대표값으로 모입니다",
            "서로 다른 값들이 가장 가까운 격자로 이동해\n하나의 값으로 취급될 수 있습니다.",
            "0.17 · 0.21 · 0.24 · 0.31 · 0.36   →   0.25",
        )
        source_dots = value_dots(self.VALUES, grid_line, alternating=True)
        self.play(FadeOut(grid_title), LaggedStart(*[FadeIn(d) for d in source_dots],
                                                   lag_ratio=.08), run_time=.7)
        arrows = VGroup(*[
            CurvedArrow(d.dot.get_center() + UP * .06, grid_line.point(.25) + UP * .12,
                        angle=(-.18 + i * .09), color=SNAP,
                        stroke_width=2, tip_length=.1)
            for i, d in enumerate(source_dots)
        ])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=.08), run_time=.65)
        self.play(
            *[d.dot.animate.move_to(grid_line.point(.25)) for d in source_dots],
            *[FadeOut(VGroup(d.label, d.stem)) for d in source_dots],
            run_time=1.4, rate_func=smooth,
        )
        merged = Dot(grid_line.point(.25), radius=.18, color=SNAP)
        merged_label = txt("0.25", 31, SNAP).next_to(merged, UP, buff=.28)
        self.play(FadeOut(arrows), FadeOut(source_dots), FadeIn(merged, scale=1.8),
                  FadeIn(merged_label), Flash(merged, color=SNAP, flash_radius=.5), run_time=.85)
        snap_stage = VGroup(grid_line, merged, merged_label)
        self.keep_stage(snap_stage)
        self.play(Indicate(VGroup(merged, merged_label), color=SNAP, scale_factor=1.18),
                  run_time=.8)
        self.to(33)

        # 33–41 s — essence: fewer representable kinds, not smaller magnitudes.
        self.text(
            "핵심은 숫자의 크기가 아닙니다",
            "Quantization은 숫자를 작게 만드는 게 아니라\n표현 가능한 값의 종류를 줄입니다.",
            "많은 값의 종류     →     적은 값의 종류",
        )
        many = VGroup(*[Dot(radius=.075, color=VALUE) for _ in range(13)]).arrange(RIGHT, buff=.12)
        many.move_to([-2.2, .45, 0])
        few = VGroup(*[Dot(radius=.13, color=GRID) for _ in range(4)]).arrange(RIGHT, buff=.48)
        few.move_to([2.2, .45, 0])
        essence = VGroup(
            many, few,
            txt("많은 값", 24, VALUE).move_to([-2.2, -1.0, 0]),
            txt("적은 대표값", 24, GRID).move_to([2.2, -1.0, 0]),
            Arrow([-1.0, .45, 0], [1.0, .45, 0], buff=.12,
                  color=SNAP, stroke_width=3, tip_length=.15),
        )
        self.play(FadeOut(snap_stage), FadeIn(many), run_time=.5)
        self.play(GrowArrow(essence[-1]), FadeIn(few), FadeIn(essence[2:4]), run_time=.9)
        self.keep_stage(essence)
        self.play(Indicate(few, color=SNAP, scale_factor=1.12), run_time=.8)
        self.to(41)

        # 41–47 s — the explicit trade-off.
        self.text(
            "저장 비용은 줄고, 작은 오차가 생깁니다",
            "적은 값만 표현하면 더 적은 비트로 저장할 수 있지만,\n원래 숫자와 완전히 같지는 않습니다.",
            "저장 비용 ↓                         오차 ↑ 가능",
        )
        memory_before = VGroup(*[Square(.26, stroke_width=0, fill_color=GOOD,
                                              fill_opacity=.85) for _ in range(16)])
        memory_before.arrange_in_grid(2, 8, buff=.06).move_to([-2.25, .65, 0])
        memory_after = VGroup(*[Square(.26, stroke_width=0, fill_color=GOOD,
                                             fill_opacity=.85) for _ in range(4)])
        memory_after.arrange(RIGHT, buff=.06).move_to([-2.25, -.75, 0])
        shrink_arrow = Arrow([-2.25, .18, 0], [-2.25, -.42, 0], color=GOOD,
                             stroke_width=2.5, tip_length=.13)
        error_line = NumberLine(x_range=[.15, .30, .05], length=2.8, include_numbers=False,
                                color=MUTED, stroke_width=2).move_to([2.15, .15, 0])
        original = Dot(error_line.n2p(.21), radius=.1, color=VALUE)
        approx = Dot(error_line.n2p(.25), radius=.12, color=SNAP)
        error_arrow = DoubleArrow(original.get_center(), approx.get_center(), buff=.02,
                                  color=ERROR, stroke_width=2.5, tip_length=.08)
        tradeoff = VGroup(memory_before, memory_after, shrink_arrow, error_line,
                          original, approx, error_arrow,
                          txt("compact", 22, GOOD).move_to([-2.25, -1.35, 0]),
                          txt("error", 22, ERROR).move_to([2.15, -1.0, 0]))
        self.play(FadeOut(essence), FadeIn(memory_before), GrowArrow(shrink_arrow),
                  FadeIn(memory_after), FadeIn(error_line), FadeIn(original), run_time=.8)
        self.play(TransformFromCopy(original, approx), GrowArrow(error_arrow),
                  FadeIn(tradeoff[-2:]), run_time=.75)
        self.keep_stage(tradeoff)
        self.to(47)

        # 47–52 s — next episode: bit count controls the number of positions.
        self.text(
            "그렇다면 몇 개의 값을 남겨야 할까요?",
            "표현 가능한 위치의 개수를 결정하는 것이\n바로 bit 수입니다.",
            "NEXT  ·  8bit와 4bit는 무엇이 다를까?",
        )
        fine = QuantizationLine(width=6.8, grid_values=[i / 16 for i in range(17)],
                                show_labels=False).scale(.88).move_to([0, 1.0, 0])
        coarse = QuantizationLine(width=6.8, grid_values=[i / 4 for i in range(5)],
                                  show_labels=False).scale(.88).move_to([0, -.9, 0])
        next_stage = VGroup(
            fine, coarse,
            txt("촘촘한 격자", 22, VALUE).next_to(fine, UP, buff=.35),
            txt("거친 격자", 22, GRID).next_to(coarse, UP, buff=.35),
        )
        self.play(FadeOut(tradeoff), FadeIn(next_stage), run_time=.9)
        self.keep_stage(next_stage)
        self.play(Indicate(fine.grid, color=VALUE, scale_factor=1.03),
                  Indicate(coarse.grid, color=SNAP, scale_factor=1.08), run_time=.75)
        self.to(52)

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
