"""Quantization 09: fixed weights versus input-dependent activations."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class WeightVsActivation(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  09", 20, MUTED).move_to(UP * 7.25),
            txt("왜 Weight보다 Activation이 더 까다로울까?", 30).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — hook: both are arrays, but only one stays still.
        self.text(
            "둘 다 숫자 배열이지만 성격은 완전히 다릅니다",
            "Weight는 같은 값이 멈춰 있고, activation은 입력이 바뀔 때마다\n새로운 값으로 다시 만들어집니다.",
            "WEIGHT  ·  fixed                         ACTIVATION  ·  changing",
        )
        divider = Line([0, -1.8, 0], [0, 2.15, 0], color=MUTED,
                       stroke_width=1.3, stroke_opacity=.35)
        weight_matrix = self.value_grid([[.2, -.6, .8], [-.4, .1, .5],
                                         [.7, -.2, -.5]], VALUE, "WEIGHT")
        weight_matrix.move_to([-2.05, .25, 0])
        activation = self.value_grid([[.1], [.7], [-.3], [.4]], GRID, "ACTIVATION")
        activation.move_to([2.0, .25, 0])
        act_b = self.value_grid([[-1.2], [2.4], [.2], [1.1]], GRID, "ACTIVATION")
        act_b.move_to(activation)
        act_c = self.value_grid([[.05], [4.8], [-2.1], [.6]], GRID, "ACTIVATION")
        act_c.move_to(activation)
        hook = VGroup(divider, weight_matrix, activation)
        self.play(Create(divider), FadeIn(weight_matrix), FadeIn(activation),
                  run_time=.65)
        self.play(Transform(activation, act_b), run_time=.55)
        self.play(Transform(activation, act_c), run_time=.55)
        self.keep_stage(hook)
        self.play(Indicate(weight_matrix, color=VALUE, scale_factor=1.03),
                  Indicate(activation, color=GRID, scale_factor=1.05), run_time=.65)
        self.to(7)

        # 7–15 s — weights are known before inference.
        self.text(
            "Weight는 inference 전에 이미 알고 있습니다",
            "학습이 끝난 weight는 inference 동안 거의 고정되므로\n전체 분포와 최솟값·최댓값을 미리 분석할 수 있습니다.",
            "known before inference          range  −2.1 … 1.8",
        )
        matrix = self.value_grid([[.4, -.8, .1, .6], [-.3, .2, .7, -.5],
                                  [.9, -.2, .3, -.7]], VALUE, "TRAINED WEIGHT")
        matrix.scale(.78).move_to([-1.9, .45, 0])
        hist = self.histogram([.25, .45, .8, 1.35, 1.8, 1.5, .95, .55, .28],
                              VALUE, "distribution")
        hist.move_to([1.85, .5, 0])
        range_tag = pill("−2.1  …  1.8", SNAP, 2.35).move_to([1.85, -1.45, 0])
        known = VGroup(matrix, hist, range_tag)
        self.play(FadeOut(hook), FadeIn(matrix),
                  LaggedStart(*[GrowFromEdge(b, DOWN) for b in hist[0]],
                              lag_ratio=.04), FadeIn(hist[1:]), run_time=.8)
        self.play(FadeIn(range_tag, shift=UP * .1), run_time=.4)
        self.keep_stage(known)
        self.play(Indicate(range_tag, color=SNAP, scale_factor=1.06), run_time=.65)
        self.to(15)

        # 15–23 s — analyze and quantize once, then reuse.
        self.text(
            "한 번 Quantize한 Weight를 계속 재사용합니다",
            "분포를 보고 scale을 미리 정한 뒤 INT8이나 INT4로 저장하면\n여러 입력을 처리할 때 같은 quantized weight를 다시 씁니다.",
            "FP16 WEIGHT  →  ANALYZE  →  CHOOSE SCALE  →  INT8 / INT4",
        )
        stages = VGroup(
            self.process_box("FP16\nWEIGHT", VALUE, 1.45),
            self.process_box("ANALYZE", GRID, 1.4),
            self.process_box("SCALE", GOOD, 1.3),
            self.process_box("INT8 / INT4", SNAP, 1.65),
        ).arrange(RIGHT, buff=.38).scale(.92).move_to([0, .55, 0])
        arrows = VGroup(*[
            Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=.06,
                  color=MUTED, stroke_width=2.3, tip_length=.1)
            for i in range(3)
        ])
        reuse = VGroup(
            pill("INPUT 1", MUTED, 1.45), pill("INPUT 2", MUTED, 1.45),
            pill("INPUT 3", MUTED, 1.45), txt("→  SAME WEIGHT", 21, SNAP),
        ).arrange(RIGHT, buff=.2).scale(.85).move_to([0, -1.2, 0])
        prepared = VGroup(stages, arrows, reuse)
        self.play(FadeOut(known), FadeIn(stages[0]), run_time=.4)
        for i in range(3):
            self.play(GrowArrow(arrows[i]), FadeIn(stages[i + 1]), run_time=.38)
        self.play(FadeIn(reuse, shift=UP * .08), run_time=.45)
        self.keep_stage(prepared)
        self.play(Indicate(stages[-1], color=SNAP, scale_factor=1.06), run_time=.65)
        self.to(23)

        # 23–34 s — activations change with every input.
        self.text(
            "Activation은 입력마다 범위와 분포가 달라집니다",
            "같은 layer라도 입력 데이터와 이전 layer의 결과에 따라\n실행할 때마다 새로운 activation이 만들어집니다.",
            "INPUT A  −1…1       INPUT B  −5…7       INPUT C  −0.3…12",
        )
        layer = self.process_box("SAME\nLAYER", GRID, 1.55).move_to([0, .25, 0])
        input_card = pill("INPUT A", VALUE, 1.6).move_to([-2.8, .25, 0])
        output_range = pill("−1  …  1", SNAP, 1.75).move_to([2.7, 1.25, 0])
        act_hist = self.histogram([.2, .55, 1.1, 1.65, 1.1, .55, .2],
                                  SNAP, "activation")
        act_hist.scale(.72).move_to([2.7, -.55, 0])
        flow = VGroup(
            Arrow(input_card.get_right(), layer.get_left(), buff=.08,
                  color=MUTED, stroke_width=2.3, tip_length=.1),
            Arrow(layer.get_right(), output_range.get_left() + DOWN * .35,
                  buff=.08, color=MUTED, stroke_width=2.3, tip_length=.1),
        )
        dynamic = VGroup(input_card, layer, output_range, act_hist, flow)
        self.play(FadeOut(prepared), FadeIn(dynamic), run_time=.75)

        input_b = pill("INPUT B", VALUE, 1.6).move_to(input_card)
        range_b = pill("−5  …  7", ERROR, 1.75).move_to(output_range)
        hist_b = self.histogram([.65, .3, .5, 1.0, .45, .25, 1.6],
                                ERROR, "activation").scale(.72).move_to(act_hist)
        self.play(Transform(input_card, input_b), Transform(output_range, range_b),
                  Transform(act_hist, hist_b), run_time=.85)

        input_c = pill("INPUT C", VALUE, 1.6).move_to(input_card)
        range_c = pill("−0.3  …  12", ERROR, 2.15).move_to(output_range)
        hist_c = self.histogram([.25, 1.45, .8, .35, .2, .15, 1.85],
                                ERROR, "activation").scale(.72).move_to(act_hist)
        self.play(Transform(input_card, input_c), Transform(output_range, range_c),
                  Transform(act_hist, hist_c), run_time=.85)
        self.keep_stage(dynamic)
        self.play(Indicate(output_range, color=ERROR, scale_factor=1.07), run_time=.65)
        self.to(34)

        # 34–43 s — a fixed activation scale faces a clipping/resolution tradeoff.
        self.text(
            "하나의 고정 Scale은 모든 입력에 맞지 않을 수 있습니다",
            "범위를 좁게 잡으면 큰 activation이 잘리고, 넓게 잡으면\n작은 activation이 쓰는 격자가 성겨져 표현이 거칠어집니다.",
            "narrow range  →  clipping          wide range  →  coarse resolution",
        )
        narrow = self.range_panel("NARROW FIXED RANGE", "−1", "1", VALUE)
        narrow.move_to([-2.0, .35, 0])
        overflow = VGroup(
            Dot(narrow[1].get_end() + RIGHT * .48, radius=.11, color=ERROR),
            txt("7", 20, ERROR).next_to(narrow[1].get_end() + RIGHT * .48, UP,
                                        buff=.13),
            Line(narrow[1].get_end() + UP * .38, narrow[1].get_end() + DOWN * .38,
                 color=ERROR, stroke_width=4),
            pill("CLIPPING", ERROR, 1.65).next_to(narrow, DOWN, buff=.42),
        )
        wide = self.range_panel("WIDE FIXED RANGE", "−5", "12", GRID, levels=5)
        wide.move_to([2.0, .35, 0])
        cluster = VGroup(*[
            Dot(wide[1].point_from_proportion(.28 + i * .018) + UP * .45,
                radius=.075, color=VALUE) for i in range(5)
        ])
        coarse = pill("COARSE GRID", GRID, 1.85).next_to(wide, DOWN, buff=.42)
        failure = VGroup(narrow, overflow, wide, cluster, coarse)
        self.play(FadeOut(dynamic), FadeIn(narrow), FadeIn(wide), run_time=.75)
        self.play(FadeIn(overflow), FadeIn(cluster), FadeIn(coarse), run_time=.6)
        self.keep_stage(failure)
        self.play(Indicate(overflow[0:3], color=ERROR, scale_factor=1.08),
                  Indicate(cluster, color=GRID, scale_factor=1.08), run_time=.7)
        self.to(43)

        # 43–50 s — concise comparison.
        self.text(
            "차이는 고정된 값과 실행 중 변하는 값입니다",
            "Weight는 미리 분석하고 scale을 고정하기 상대적으로 쉽지만,\nactivation은 입력별 변화까지 고려해야 해서 더 까다롭습니다.",
            "WEIGHT  ·  offline / fixed       ACTIVATION  ·  runtime / dynamic",
        )
        weight_card = self.compare_card("WEIGHT", ("고정", "미리 분석", "scale 재사용"),
                                        VALUE)
        act_card = self.compare_card("ACTIVATION", ("입력 의존", "매번 변화", "scale 선택 어려움"),
                                     GRID)
        cards = VGroup(weight_card, act_card).arrange(RIGHT, buff=.42).scale(.9)
        cards.move_to([0, .25, 0])
        self.play(FadeOut(failure), FadeIn(cards), run_time=.75)
        self.keep_stage(cards)
        self.play(Indicate(weight_card, color=VALUE, scale_factor=1.04),
                  Indicate(act_card, color=GRID, scale_factor=1.04), run_time=.7)
        self.to(50)

        # 50–56 s — weight-only quantization is a practical consequence.
        self.text(
            "그래서 Weight만 낮은 bit로 줄이기도 합니다",
            "큰 weight matrix는 INT4로 저장하고 activation은 FP16으로 유지해\n메모리 이점을 얻으면서 activation의 난점을 피하는 방식입니다.",
            "WEIGHT-ONLY QUANTIZATION          Weight INT4  ·  Activation FP16",
        )
        model = RoundedRectangle(width=6.25, height=2.9, corner_radius=.25,
                                 stroke_color=MUTED, stroke_width=1.5,
                                 fill_color=MUTED, fill_opacity=.035)
        model_title = txt("LLM LAYER", 18, MUTED).next_to(model, UP, buff=.15)
        w_block = self.memory_block("WEIGHT", "INT4", SNAP, 4.7).move_to([0, .65, 0])
        a_block = self.memory_block("ACTIVATION", "FP16", GRID, 3.8).move_to([0, -.75, 0])
        weight_only = VGroup(model, model_title, w_block, a_block)
        self.play(FadeOut(cards), FadeIn(model), FadeIn(model_title), run_time=.5)
        self.play(FadeIn(w_block, shift=RIGHT * .1),
                  FadeIn(a_block, shift=RIGHT * .1), run_time=.65)
        self.keep_stage(weight_only)
        self.play(Indicate(w_block, color=SNAP, scale_factor=1.04), run_time=.65)
        self.to(56)

        # 56–60 s — next: choose scales before or during execution.
        self.text(
            "Activation의 Scale은 언제 정해야 할까?",
            "실행 전에 고정할 수도 있고 입력이 들어올 때 새로 계산할 수도 있습니다.\n다음에는 Static과 Dynamic Quantization을 비교합니다.",
            "NEXT  ·  Static vs Dynamic Quantization",
        )
        static = self.decision_card("STATIC", "미리 scale 결정", VALUE)
        dynamic_card = self.decision_card("DYNAMIC", "실행 중 scale 결정", GRID)
        decisions = VGroup(static, txt("OR", 22, MUTED), dynamic_card)
        decisions.arrange(RIGHT, buff=.38).move_to([0, .2, 0])
        clock = txt("BEFORE INFERENCE                 DURING INFERENCE", 18, SNAP)
        clock.move_to([0, -1.4, 0])
        next_stage = VGroup(decisions, clock)
        self.play(FadeOut(weight_only), FadeIn(decisions), FadeIn(clock), run_time=.75)
        self.keep_stage(next_stage)
        self.to(60)

    def value_grid(self, rows, color, label):
        nrows, ncols = len(rows), len(rows[0])
        cells = VGroup()
        for row in rows:
            for value in row:
                box = RoundedRectangle(width=.7, height=.58, corner_radius=.07,
                                       stroke_color=color, stroke_width=1,
                                       fill_color=color, fill_opacity=.08)
                value_text = f"{value:g}".replace("-", "−")
                cells.add(VGroup(box, txt(value_text, 17, color).move_to(box)))
        cells.arrange_in_grid(rows=nrows, cols=ncols, buff=(.07, .07))
        title = txt(label, 19, color).next_to(cells, UP, buff=.2)
        return VGroup(cells, title)

    def histogram(self, heights, color, label):
        bars = VGroup(*[
            Rectangle(width=.26, height=h, stroke_width=0,
                      fill_color=color, fill_opacity=.78)
            for h in heights
        ]).arrange(RIGHT, buff=.055, aligned_edge=DOWN)
        baseline = Line(bars.get_corner(DL) + LEFT * .1,
                        bars.get_corner(DR) + RIGHT * .1,
                        color=MUTED, stroke_width=1.5)
        name = txt(label, 17, MUTED).next_to(baseline, DOWN, buff=.14)
        return VGroup(bars, baseline, name)

    def process_box(self, label, color, width):
        box = RoundedRectangle(width=width, height=1.25, corner_radius=.16,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box, txt(label, 18, color).move_to(box))

    def range_panel(self, title, lo, hi, color, levels=9):
        box = RoundedRectangle(width=3.5, height=2.45, corner_radius=.2,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=color, fill_opacity=.04)
        axis = Line(LEFT * 1.28, RIGHT * 1.28, color=MUTED, stroke_width=2)
        axis.move_to(box.get_center() + DOWN * .15)
        ticks = VGroup(*[
            Line(UP * .16, DOWN * .16, color=color, stroke_width=2.2)
            .move_to(axis.point_from_proportion(i / (levels - 1)))
            for i in range(levels)
        ])
        return VGroup(
            box,
            axis,
            ticks,
            txt(title, 17, color).move_to(box.get_center() + UP * .78),
            txt(lo, 17, MUTED).next_to(axis, LEFT, buff=.08),
            txt(hi, 17, MUTED).next_to(axis, RIGHT, buff=.08),
        )

    def compare_card(self, title, lines, color):
        box = RoundedRectangle(width=3.6, height=3.15, corner_radius=.22,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06)
        items = VGroup(*[txt(line, 21, INK) for line in lines])
        items.arrange(DOWN, buff=.32).move_to(box.get_center() + DOWN * .25)
        return VGroup(box,
                      txt(title, 24, color).move_to(box.get_center() + UP * 1.05),
                      items)

    def memory_block(self, label, dtype, color, width):
        bar = RoundedRectangle(width=width, height=.9, corner_radius=.14,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.18)
        return VGroup(bar,
                      txt(label, 20, INK).move_to(bar.get_center() + LEFT * width * .25),
                      pill(dtype, color, 1.2).move_to(bar.get_center() + RIGHT * width * .3))

    def decision_card(self, title, description, color):
        box = RoundedRectangle(width=3.0, height=2.15, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        return VGroup(
            box,
            txt(title, 25, color).move_to(box.get_center() + UP * .45),
            txt(description, 20, INK).move_to(box.get_center() + DOWN * .42),
        )

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
