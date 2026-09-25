"""Quantization 06: one outlier expands the range for every other value."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class QuantizationOutlier(Scene):
    DURATION = 60
    VALUES = (-.80, -.40, -.10, .20, .60)

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  06", 20, MUTED).move_to(UP * 7.25),
            txt("값 하나가 Quantization 전체를 망칠 수 있는 이유", 31).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–8 s — hook: one point sits far outside a dense central cluster.
        self.text(
            "대부분은 −1…1인데, 값 하나만 20이라면?",
            "멀리 떨어진 값 하나 때문에 나머지 수많은 값의\n표현이 더 거칠어질 수 있습니다.",
            "many small values                         one outlier",
        )
        hook_axis = Line([-3.35, .05, 0], [3.35, .05, 0],
                         color=MUTED, stroke_width=2.5)
        cluster_x = np.linspace(-3.2, -2.55, 13)
        cluster = VGroup(*[
            Dot([x, .05 + .12 * ((i % 3) - 1), 0], radius=.07, color=VALUE)
            for i, x in enumerate(cluster_x)
        ])
        cluster_brace = BraceBetweenPoints([-3.3, -.45, 0], [-2.45, -.45, 0],
                                           direction=DOWN, color=VALUE)
        cluster_label = txt("−1  ~  1", 23, VALUE).next_to(cluster_brace, DOWN, buff=.12)
        outlier = Dot([3.2, .05, 0], radius=.16, color=ERROR)
        outlier_label = txt("20", 30, ERROR).next_to(outlier, UP, buff=.3)
        gap = DashedLine([-2.25, .05, 0], [2.85, .05, 0], color=MUTED,
                         stroke_width=1.3, dash_length=.1, stroke_opacity=.4)
        hook = VGroup(hook_axis, gap, cluster, cluster_brace,
                      cluster_label, outlier, outlier_label)
        self.play(Create(hook_axis), FadeIn(cluster), GrowFromCenter(cluster_brace),
                  FadeIn(cluster_label), run_time=.8)
        self.play(Create(gap), FadeIn(outlier, scale=1.8), FadeIn(outlier_label),
                  Flash(outlier, color=ERROR, flash_radius=.45), run_time=.85)
        self.keep_stage(hook)
        self.play(Indicate(outlier, color=ERROR, scale_factor=1.5), run_time=.7)
        self.to(8)

        # 8–17 s — without the outlier, all 16 levels serve the dense range.
        self.text(
            "Outlier가 없으면 좁은 범위를 촘촘히 나눕니다",
            "같은 16개 위치를 −1부터 1 안에 배치하면 대부분의 값은\n가까운 격자로 아주 조금만 이동합니다.",
            "Range −1…1     ·     16 levels     ·     Δ ≈ 0.133",
        )
        narrow_axis = self.quant_axis(-1, 1, 16, 6.6, VALUE).move_to([0, -.25, 0])
        sample_values = (-.72, -.18, .24, .63)
        sample_dots = VGroup(*[
            Dot(narrow_axis[0].point_from_proportion((v + 1) / 2) + UP * .75,
                radius=.1, color=ERROR)
            for v in sample_values
        ])
        sample_labels = VGroup(*[
            txt(f"{v:.2f}", 18, ERROR).next_to(sample_dots[i], UP, buff=.1)
            for i, v in enumerate(sample_values)
        ])
        targets = [round((v + 1) / (2 / 15)) * (2 / 15) - 1 for v in sample_values]
        target_dots = VGroup(*[
            Dot(narrow_axis[0].point_from_proportion((v + 1) / 2),
                radius=.105, color=SNAP)
            for v in targets
        ])
        arrows = VGroup(*[
            Arrow(sample_dots[i].get_bottom(), target_dots[i].get_center(), buff=.05,
                  color=SNAP, stroke_width=1.8, tip_length=.08)
            for i in range(len(sample_values))
        ])
        narrow = VGroup(narrow_axis, sample_dots, sample_labels, target_dots, arrows)
        self.play(FadeOut(hook), FadeIn(narrow_axis), FadeIn(sample_dots),
                  FadeIn(sample_labels), run_time=.75)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.1),
                  FadeIn(target_dots), run_time=.75)
        self.keep_stage(narrow)
        self.play(Indicate(target_dots, color=GOOD, scale_factor=1.35), run_time=.75)
        self.to(17)

        # 17–26 s — include 20: same number of levels across a 10.5x wider range.
        self.text(
            "Outlier를 포함하면 전체 범위가 늘어납니다",
            "값 20을 표현하기 위해 범위를 −1부터 20까지 넓혀도\n사용할 수 있는 격자 위치의 개수는 그대로입니다.",
            "same 16 levels     ·     Range −1…20     ·     Δ = 1.4",
        )
        wide_axis = self.quant_axis(-1, 20, 16, 6.6, GRID).move_to([0, -.25, 0])
        compressed = VGroup(*[
            Dot(wide_axis[0].point_from_proportion((v + 1) / 21) + UP * .72,
                radius=.095, color=VALUE)
            for v in sample_values
        ])
        wide_outlier = Dot(wide_axis[0].get_end() + UP * .72,
                           radius=.15, color=ERROR)
        wide_outlier_label = txt("20", 27, ERROR).next_to(wide_outlier, UP, buff=.14)
        wide = VGroup(wide_axis, compressed, wide_outlier, wide_outlier_label)
        self.play(FadeOut(VGroup(sample_labels, target_dots, arrows)),
                  Transform(narrow_axis, wide_axis),
                  Transform(sample_dots, compressed),
                  FadeIn(wide_outlier, scale=1.7), FadeIn(wide_outlier_label),
                  run_time=1.45, rate_func=smooth)
        range_arrow = DoubleArrow(narrow_axis[0].get_start() + DOWN * .75,
                                  narrow_axis[0].get_end() + DOWN * .75,
                                  buff=.02, color=SNAP, stroke_width=2.3,
                                  tip_length=.09)
        range_label = txt("range expanded", 21, SNAP).next_to(range_arrow, DOWN, buff=.12)
        self.play(GrowArrow(range_arrow), FadeIn(range_label), run_time=.6)
        wide_stage = VGroup(narrow_axis, sample_dots, wide_outlier,
                            wide_outlier_label, range_arrow, range_label)
        self.keep_stage(wide_stage)
        self.play(Indicate(wide_outlier, color=ERROR, scale_factor=1.45), run_time=.7)
        self.to(26)

        # 26–36 s — zoom back into -1..1: only two of the fixed levels land there.
        self.text(
            "대부분의 값이 있는 구간에는 격자가 거의 남지 않습니다",
            "넓어진 격자를 −1부터 1 구간만 확대하면 표현 가능한 값은\n−1과 0.4 정도뿐이라 여러 입력이 같은 값으로 합쳐집니다.",
            "−0.8 · −0.4 → −1.0          −0.1 · 0.2 · 0.6 → 0.4",
        )
        zoom_axis = NumberLine(x_range=[-1, 1, .2], length=6.4,
                               include_numbers=False, color=MUTED,
                               stroke_width=2.4).move_to([0, -.35, 0])
        available = VGroup(
            self.grid_marker(zoom_axis.n2p(-1), "−1.0"),
            self.grid_marker(zoom_axis.n2p(.4), "0.4"),
        )
        value_dots = VGroup(*[
            Dot(zoom_axis.n2p(v) + UP * (1.15 + .28 * (i % 2)),
                radius=.1, color=VALUE)
            for i, v in enumerate(self.VALUES)
        ])
        value_labels = VGroup(*[
            txt(f"{v:g}", 18, VALUE).next_to(value_dots[i], UP, buff=.1)
            for i, v in enumerate(self.VALUES)
        ])
        mapped = (-1, -1, .4, .4, .4)
        merge_arrows = VGroup(*[
            Arrow(value_dots[i].get_bottom(), zoom_axis.n2p(mapped[i]) + UP * .14,
                  buff=.05, color=SNAP, stroke_width=2, tip_length=.08)
            for i in range(len(self.VALUES))
        ])
        zoom = VGroup(zoom_axis, available, value_dots, value_labels, merge_arrows)
        self.play(FadeOut(wide_stage), FadeIn(zoom_axis), FadeIn(available),
                  FadeIn(value_dots), FadeIn(value_labels), run_time=.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in merge_arrows], lag_ratio=.08),
                  run_time=.75)
        self.play(*[value_dots[i].animate.move_to(zoom_axis.n2p(mapped[i]))
                    for i in range(len(self.VALUES))],
                  FadeOut(value_labels), run_time=1.05)
        self.keep_stage(zoom)
        self.play(Indicate(available, color=SNAP, scale_factor=1.12), run_time=.7)
        self.to(36)

        # 36–44 s — causal chain: the collateral damage is the real issue.
        self.text(
            "문제는 outlier 하나의 오차만이 아닙니다",
            "그 하나가 전체 range와 scale을 키우면서 나머지 값들의\n표현 해상도까지 떨어뜨릴 수 있다는 점입니다.",
            "outlier ↑  →  range ↑  →  scale ↑  →  resolution ↓",
        )
        chain = VGroup(
            self.cause_card("OUTLIER", "20", ERROR), txt("→", 30, MUTED),
            self.cause_card("RANGE", "−1…20", GRID), txt("→", 30, MUTED),
            self.cause_card("SCALE", "1.4", SNAP), txt("→", 30, MUTED),
            self.cause_card("RESOLUTION", "DOWN", VALUE),
        ).arrange(RIGHT, buff=.12).scale(.79).move_to([0, .5, 0])
        contrast = VGroup(
            pill("no outlier · fine grid", GOOD, 2.85),
            pill("with outlier · coarse grid", ERROR, 3.3),
        ).arrange(RIGHT, buff=.35).scale(.9).move_to([0, -1.25, 0])
        cause = VGroup(chain, contrast)
        self.play(FadeOut(zoom), FadeIn(chain), FadeIn(contrast), run_time=.9)
        self.keep_stage(cause)
        self.play(LaggedStart(*[Indicate(chain[i], scale_factor=1.05)
                                for i in (0, 2, 4, 6)], lag_ratio=.12), run_time=.9)
        self.to(44)

        # 44–51 s — tensors can contain many small entries and a few tall spikes.
        self.text(
            "실제 tensor에서도 일부 값만 크게 튈 수 있습니다",
            "Weight나 activation의 대부분이 작은 범위에 모여 있어도\n소수의 큰 값이 전체 scale에 영향을 줄 수 있습니다.",
            "many small values                     a few large values",
        )
        heights = (.55, .82, .42, .72, .35, .64, .48, .76, .39, .58,
                   .45, .68, .52, 3.65, .38, .61, .47, .78, .43, .56)
        bars = VGroup(*[
            Rectangle(width=.24, height=h, stroke_width=0,
                      fill_color=ERROR if h > 2 else VALUE,
                      fill_opacity=.9).align_to(DOWN * 1.6, DOWN)
            for h in heights
        ]).arrange(RIGHT, buff=.08, aligned_edge=DOWN).move_to([0, .1, 0])
        baseline = Line([-3.45, -1.65, 0], [3.45, -1.65, 0],
                        color=MUTED, stroke_width=2)
        spike_label = txt("outlier", 23, ERROR).next_to(bars[13], UP, buff=.2)
        spike_arrow = Arrow(spike_label.get_bottom(), bars[13].get_top(), buff=.08,
                            color=ERROR, stroke_width=2, tip_length=.1)
        tensor = VGroup(bars, baseline, spike_label, spike_arrow)
        self.play(FadeOut(cause), FadeIn(baseline),
                  LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=.025),
                  run_time=.9)
        self.play(FadeIn(spike_label), GrowArrow(spike_arrow), run_time=.55)
        self.keep_stage(tensor)
        self.play(Indicate(bars[13], color=ERROR, scale_factor=1.08), run_time=.7)
        self.to(51)

        # 51–60 s — ask why differently sized channels must share one scale.
        self.text(
            "서로 다른 크기의 채널을 왜 같은 자로 재야 할까요?",
            "하나의 scale을 공유하면 작은 Channel A가 거칠어지지만,\n각 채널에 별도 scale을 주면 각 범위에 맞출 수 있습니다.",
            "NEXT  ·  Per-Tensor vs Per-Channel Quantization",
        )
        channel_a = self.channel_card("CHANNEL A", "−0.5  ~  0.5", VALUE)
        channel_b = self.channel_card("CHANNEL B", "−10  ~  10", GRID)
        channels = VGroup(channel_a, channel_b).arrange(DOWN, buff=.55).move_to([0, .55, 0])
        shared = pill("one shared scale", ERROR, 2.8).move_to([0, -1.75, 0])
        separate = VGroup(pill("scale A", VALUE, 1.8), pill("scale B", GRID, 1.8))
        separate.arrange(RIGHT, buff=.55).move_to([0, -1.75, 0])
        next_stage = VGroup(channels, shared, separate)
        self.play(FadeOut(tensor), FadeIn(channels), FadeIn(shared), run_time=.85)
        self.play(FadeOut(shared, shift=DOWN * .08), FadeIn(separate, shift=UP * .08),
                  run_time=.85)
        self.keep_stage(next_stage)
        self.play(Indicate(separate, color=SNAP, scale_factor=1.06), run_time=.75)
        self.to(60)

    def quant_axis(self, lo, hi, levels, width, color):
        axis = Line(LEFT * width / 2, RIGHT * width / 2,
                    color=MUTED, stroke_width=2.5)
        ticks = VGroup(*[
            Line(UP * .19, DOWN * .19, color=color, stroke_width=2.3)
            .move_to(axis.point_from_proportion(i / (levels - 1)))
            for i in range(levels)
        ])
        labels = VGroup(
            txt(f"{lo:g}".replace("-", "−"), 21, color).next_to(axis, LEFT, buff=.1),
            txt(f"{hi:g}", 21, color).next_to(axis, RIGHT, buff=.1),
            txt(f"{levels} fixed levels", 19, MUTED).next_to(axis, DOWN, buff=.3),
        )
        return VGroup(axis, ticks, labels)

    def grid_marker(self, point, label):
        return VGroup(
            Line(point + UP * .32, point + DOWN * .32,
                 color=GRID, stroke_width=4),
            Dot(point, radius=.12, color=SNAP),
            txt(label, 22, GRID).next_to(point, DOWN, buff=.42),
        )

    def cause_card(self, title, value, color):
        box = RoundedRectangle(width=1.8, height=1.55, corner_radius=.17,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box,
                      txt(title, 17, MUTED, 1.55).move_to(box.get_center() + UP * .35),
                      txt(value, 25, color, 1.55).move_to(box.get_center() + DOWN * .3))

    def channel_card(self, name, value_range, color):
        box = RoundedRectangle(width=5.8, height=1.45, corner_radius=.18,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        ruler = Line(LEFT * 1.35, RIGHT * 1.35, color=color, stroke_width=3)
        ruler.move_to(box.get_center() + RIGHT * 1.0)
        return VGroup(
            box,
            txt(name, 21, color).move_to(box.get_center() + LEFT * 1.75 + UP * .25),
            txt(value_range, 22, INK).move_to(box.get_center() + LEFT * 1.75 + DOWN * .25),
            ruler,
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
