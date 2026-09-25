"""Pruning 03: why 2:4 semi-structured sparsity exists."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, pill, txt,
)


def pattern_grid(rows, cols, alive, cell=.47):
    alive = set(alive)
    grid = VGroup()
    for i in range(rows * cols):
        live = i in alive
        grid.add(RoundedRectangle(
            width=cell * .82, height=cell * .82, corner_radius=.055,
            stroke_color=GOOD if live else ZERO, stroke_width=1.0,
            fill_color=GOOD if live else ZERO,
            fill_opacity=.82 if live else .09,
        ))
    grid.arrange_in_grid(rows, cols, buff=.075)
    return grid


def weight_row(values, live=None, width=1.45, color=WEIGHT):
    live = set(range(len(values)) if live is None else live)
    cells = VGroup()
    for i, value in enumerate(values):
        active = i in live
        box = RoundedRectangle(width=width, height=.86, corner_radius=.13,
                               stroke_color=color if active else ZERO,
                               stroke_width=1.5, fill_color=color if active else ZERO,
                               fill_opacity=.09 if active else .05)
        label = txt(str(value) if active else "0", 23,
                    INK if active else ZERO, width - .18)
        cells.add(VGroup(box, label))
    cells.arrange(RIGHT, buff=.16)
    return cells


def pattern_card(indices, color=SPARSE, scale=.34):
    dots = VGroup(*[
        Dot(radius=.115, color=GOOD if i in indices else ZERO)
        for i in range(4)
    ]).arrange(RIGHT, buff=.18)
    box = RoundedRectangle(width=2.05, height=.72, corner_radius=.12,
                           stroke_color=color, stroke_width=1.2,
                           fill_color=color, fill_opacity=.05)
    return VGroup(box, dots)


class WhyTwoOfFour(Scene):
    DURATION = 90

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("PRUNING & SPARSITY  /  03", 20, MUTED).move_to(UP * 7.25),
            txt("왜 하필 2:4 Sparsity일까?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — unstructured pruning lets the model choose individual weights.
        self.text(
            "모델은 필요한 Weight만 골라 남기고 싶습니다",
            "작은 Weight를 개별적으로 지우면\n남길 위치를 자유롭게 선택할 수 있습니다.",
            "UNSTRUCTURED  ·  선택의 자유",
        )
        alive = (0, 3, 6, 9, 10, 14, 17, 20, 22, 25, 29, 31)
        free_grid = pattern_grid(4, 8, alive).move_to([0, .45, 0])
        choose = VGroup(*[
            SurroundingRectangle(free_grid[i], color=ACCENT, buff=.045,
                                 stroke_width=2) for i in alive[:4]
        ])
        free_tag = pill("어디를 남길지 자유", GOOD, 3.2).next_to(free_grid, DOWN,
                                                                  buff=.48)
        free_stage = VGroup(free_grid, choose, free_tag)
        self.play(FadeIn(free_grid, scale=.96), run_time=.65)
        self.play(LaggedStart(*[Create(x) for x in choose], lag_ratio=.1),
                  FadeIn(free_tag), run_time=.8)
        self.keep_stage(free_stage)
        self.to(7)

        # 7–14 s — that freedom creates irregular surviving positions.
        self.text(
            "하지만 살아남은 위치는 불규칙합니다",
            "모델의 자유로운 선택은\nGPU가 예측하기 어려운 배치가 됩니다.",
            "GPU  →  ?  →  ?  →  ?",
        )
        hops = VGroup()
        hop_indices = (0, 10, 22, 29)
        for a, b in zip(hop_indices, hop_indices[1:]):
            hops.add(CurvedArrow(free_grid[a].get_center(), free_grid[b].get_center(),
                                 angle=.35, color=PRUNE, stroke_width=2,
                                 tip_length=.1))
        irregular = pill("IRREGULAR", PRUNE, 2.65).next_to(free_grid, DOWN, buff=.48)
        self.play(FadeOut(choose), ReplacementTransform(free_tag, irregular),
                  run_time=.5)
        self.play(LaggedStart(*[Create(a) for a in hops], lag_ratio=.14),
                  run_time=1.0)
        self.keep_stage(free_grid, hops, irregular)
        self.to(14)

        # 14–22 s — structured pruning removes whole rows and shrinks dimensions.
        self.text(
            "줄 전체를 지우면 구조는 훨씬 규칙적입니다",
            "행이나 Channel을 제거하면\n행렬의 크기 자체를 줄일 수 있습니다.",
            "STRUCTURED  ·  실제 dimension 축소",
        )
        rows = VGroup(*[
            VGroup(*[RoundedRectangle(width=.62, height=.54, corner_radius=.06,
                                      stroke_color=WEIGHT, stroke_width=1,
                                      fill_color=WEIGHT, fill_opacity=.18)
                     for _ in range(6)]).arrange(RIGHT, buff=.09)
            for _ in range(4)
        ]).arrange(DOWN, buff=.16).move_to([0, .55, 0])
        removed = VGroup(rows[1], rows[3])
        crosses = VGroup(*[
            Line(row.get_left() + LEFT * .08, row.get_right() + RIGHT * .08,
                 color=PRUNE, stroke_width=5) for row in (rows[1], rows[3])
        ])
        structured_tag = pill("ROW / CHANNEL", GOOD, 3.05).next_to(rows, DOWN, buff=.5)
        self.play(FadeOut(free_grid), FadeOut(hops), FadeOut(irregular),
                  FadeIn(rows), run_time=.6)
        self.play(LaggedStart(*[Create(x) for x in crosses], lag_ratio=.18),
                  run_time=.65)
        compact = VGroup(rows[0].copy(), rows[2].copy()).arrange(DOWN, buff=.16)
        compact.move_to([0, .55, 0])
        self.play(FadeOut(rows), FadeOut(crosses), FadeIn(compact),
                  FadeIn(structured_tag), run_time=.75)
        compact_stage = VGroup(compact, structured_tag)
        self.keep_stage(compact_stage)
        self.to(22)

        # 22–30 s — structure can force important weights out with the row.
        self.text(
            "규칙을 지키려면 중요한 Weight도 함께 지워집니다",
            "제거할 구조 안에 큰 값이 있어도\n그 줄 전체를 포기해야 합니다.",
            "구조 단위의 강한 제약",
        )
        values = weight_row(("0.02", "0.91", "−0.04", "−0.83"), width=1.55)
        values.move_to([0, .65, 0])
        for i in (1, 3):
            values[i][0].set_stroke(ACCENT)
            values[i][1].set_color(ACCENT)
        important = VGroup(
            pill("중요", ACCENT, 1.25).next_to(values[1], UP, buff=.35),
            pill("중요", ACCENT, 1.25).next_to(values[3], UP, buff=.35),
        )
        delete_line = Line(values.get_left() + LEFT * .12,
                           values.get_right() + RIGHT * .12,
                           color=PRUNE, stroke_width=7)
        lost = txt("STRUCTURE REMOVED", 26, PRUNE).move_to([0, -1.15, 0])
        loss_stage = VGroup(values, important, delete_line, lost)
        self.play(FadeOut(compact_stage), FadeIn(values), run_time=.55)
        self.play(FadeIn(important),
                  Indicate(values[1], color=ACCENT, scale_factor=1.08),
                  Indicate(values[3], color=ACCENT, scale_factor=1.08), run_time=.75)
        self.play(Create(delete_line), FadeIn(lost),
                  values.animate.set_opacity(.5), important.animate.set_opacity(.7),
                  run_time=.75)
        self.keep_stage(loss_stage)
        self.to(30)

        # 30–38 s — make the model/hardware conflict explicit.
        self.text(
            "모델의 자유와 GPU의 규칙성이 충돌합니다",
            "한쪽을 늘리면 다른 쪽의 장점이\n줄어들기 쉽습니다.",
            "선택의 자유   ↔   규칙적인 구조",
        )
        axis = Line([-3.2, .35, 0], [3.2, .35, 0], color=MUTED, stroke_width=3)
        left = VGroup(
            Circle(.28, color=GOOD, fill_color=GOOD, fill_opacity=.18),
            txt("MODEL", 25, GOOD),
            txt("자유롭게 선택", 22, GOOD),
        ).arrange(DOWN, buff=.28).move_to([-2.85, .55, 0])
        right = VGroup(
            Square(.54, color=WEIGHT, fill_color=WEIGHT, fill_opacity=.18),
            txt("GPU", 25, WEIGHT),
            txt("규칙적인 구조", 22, WEIGHT),
        ).arrange(DOWN, buff=.28).move_to([2.85, .55, 0])
        arrows = VGroup(
            Arrow([-1.0, .35, 0], [-2.1, .35, 0], color=GOOD, buff=0,
                  stroke_width=3, tip_length=.13),
            Arrow([1.0, .35, 0], [2.1, .35, 0], color=WEIGHT, buff=0,
                  stroke_width=3, tip_length=.13),
        )
        conflict = VGroup(axis, left, right, arrows)
        self.play(FadeOut(loss_stage), Create(axis), FadeIn(left), FadeIn(right),
                  run_time=.7)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=.6)
        self.keep_stage(conflict)
        self.to(38)

        # 38–44 s — open a deliberate middle space.
        self.text(
            "둘 사이의 중간을 만들 수는 없을까요?",
            "모델에게 선택권을 남기면서\n하드웨어가 이해할 규칙을 줍니다.",
            "FREEDOM        ?        REGULARITY",
        )
        middle = VGroup(
            Circle(.72, stroke_color=ACCENT, stroke_width=2.5,
                   fill_color=ACCENT, fill_opacity=.08),
            txt("?", 46, ACCENT, weight=BOLD),
        ).move_to([0, .35, 0])
        self.play(arrows[0].animate.shift(RIGHT * .8),
                  arrows[1].animate.shift(LEFT * .8),
                  FadeIn(middle, scale=.6), run_time=.8)
        middle_stage = VGroup(conflict, middle)
        self.keep_stage(middle_stage)
        self.to(44)

        # 44–52 s — group four contiguous weights.
        self.text(
            "먼저 Weight를 4개씩 묶습니다",
            "지원되는 방향의 연속된 4개가\n하나의 작은 선택 단위가 됩니다.",
            "CONTIGUOUS GROUP OF 4",
        )
        group = weight_row(("0.91", "0.03", "−0.72", "0.01"), width=1.55)
        group.move_to([0, .45, 0])
        group_box = SurroundingRectangle(group, color=SPARSE, buff=.22,
                                         corner_radius=.16, stroke_width=2.5)
        indices = VGroup(*[
            txt(str(i + 1), 18, MUTED).next_to(group[i], DOWN, buff=.18)
            for i in range(4)
        ])
        grouped = VGroup(group, group_box, indices)
        self.play(FadeOut(middle_stage),
                  LaggedStart(*[FadeIn(x, shift=UP * .08) for x in group],
                              lag_ratio=.1), run_time=.75)
        self.play(Create(group_box), FadeIn(indices), run_time=.55)
        self.keep_stage(grouped)
        self.to(52)

        # 52–60 s — keep exactly two values in every group of four.
        self.text(
            "각 4개 중 정확히 2개만 남깁니다",
            "이 예에서는 작은 두 값을 0으로 만들고\n큰 두 값을 유지합니다.",
            "2 NON-ZERO  /  4 WEIGHTS",
        )
        pruned_group = weight_row(("0.91", "0.03", "−0.72", "0.01"),
                                  live=(0, 2), width=1.55)
        pruned_group.move_to(group)
        pruned_box = SurroundingRectangle(pruned_group, color=SPARSE, buff=.22,
                                          corner_radius=.16, stroke_width=2.5)
        ratio = pill("2 / 4", ACCENT, 1.75).next_to(pruned_box, DOWN, buff=.5)
        pruned_stage = VGroup(pruned_group, pruned_box, ratio)
        self.play(FadeOut(indices), FadeTransform(group, pruned_group),
                  Transform(group_box, pruned_box), run_time=1.0)
        self.play(FadeIn(ratio, scale=.8), run_time=.45)
        self.keep_stage(pruned_stage)
        self.to(60)

        # 60–69 s — different groups can choose different pairs.
        self.text(
            "고정되는 것은 위치가 아니라 개수입니다",
            "그룹마다 서로 다른 두 위치를\n선택할 수 있습니다.",
            "위치는 자유롭게   ·   개수는 규칙적으로",
        )
        patterns = ((0, 2), (1, 3), (0, 1), (1, 2))
        cards = VGroup(*[pattern_card(p) for p in patterns])
        cards.arrange(DOWN, buff=.22).move_to([0, .4, 0])
        labels = VGroup(*[
            txt(f"Group {i + 1}", 19, MUTED).next_to(cards[i], LEFT, buff=.3)
            for i in range(4)
        ])
        groups_stage = VGroup(cards, labels)
        self.play(FadeOut(pruned_stage),
                  LaggedStart(*[FadeIn(c, shift=RIGHT * .12) for c in cards],
                              lag_ratio=.12),
                  LaggedStart(*[FadeIn(x) for x in labels], lag_ratio=.12),
                  run_time=1.0)
        highlights = VGroup(*[
            SurroundingRectangle(c, color=GOOD, buff=.04, corner_radius=.14,
                                 stroke_width=2.2) for c in cards
        ])
        self.play(LaggedStart(*[FadeIn(h) for h in highlights], lag_ratio=.1),
                  run_time=.4)
        self.play(FadeOut(highlights), run_time=.4)
        self.keep_stage(groups_stage)
        self.to(69)

        # 69–77 s — show all six choices visually.
        self.text(
            "4개 중 2개를 고르는 방법은 6가지입니다",
            "제한된 규칙 안에서도 모델에게\n선택권이 남아 있습니다.",
            "어떤 2개를 남길까?",
        )
        choices = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
        six = VGroup(*[pattern_card(p, ACCENT) for p in choices])
        six.arrange_in_grid(3, 2, buff=(.32, .27)).move_to([0, .45, 0])
        six_stage = VGroup(
            six,
            pill("6 PATTERNS", ACCENT, 2.7).next_to(six, DOWN, buff=.45),
        )
        self.play(FadeOut(groups_stage),
                  LaggedStart(*[FadeIn(c, scale=.72) for c in six],
                              lag_ratio=.09), run_time=1.15)
        self.play(FadeIn(six_stage[1]), run_time=.4)
        self.keep_stage(six_stage)
        self.to(77)

        # 77–90 s — name the compromise and end on the core phrase.
        self.text(
            "2:4는 자유와 규칙 사이의 절충안입니다",
            "완전히 자유롭지도, 줄 전체를 지우지도 않는\nSemi-Structured Sparsity입니다.",
            "위치는 자유롭게, 개수는 규칙적으로",
        )
        line = Line([-3.2, .35, 0], [3.2, .35, 0], color=MUTED, stroke_width=3)
        ticks = VGroup(*[
            Line([x, .16, 0], [x, .54, 0], color=color, stroke_width=3)
            for x, color in ((-3.2, GOOD), (0, ACCENT), (3.2, WEIGHT))
        ])
        names = VGroup(
            txt("UNSTRUCTURED", 20, GOOD).move_to([-2.75, -1.0, 0]),
            txt("2:4", 34, ACCENT, weight=BOLD).move_to([0, -1.0, 0]),
            txt("STRUCTURED", 20, WEIGHT).move_to([2.75, -1.0, 0]),
        )
        center = VGroup(
            Circle(.5, stroke_color=ACCENT, stroke_width=2.5,
                   fill_color=ACCENT, fill_opacity=.12),
            txt("2:4", 25, ACCENT, weight=BOLD),
        ).move_to([0, .35, 0])
        final_stage = VGroup(line, ticks, names, center,
                             pill("SEMI-STRUCTURED", SPARSE, 3.25).move_to([0, 1.85, 0]))
        self.play(FadeOut(six_stage), Create(line), FadeIn(ticks), FadeIn(names),
                  run_time=.75)
        self.play(FadeIn(center, scale=.55), FadeIn(final_stage[-1], shift=DOWN * .12),
                  run_time=.65)
        self.play(Indicate(center, color=ACCENT, scale_factor=1.15), run_time=.75)
        self.keep_stage(final_stage)
        self.to(90)

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 22, ACCENT).move_to(DOWN * 4.72)
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
