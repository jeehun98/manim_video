"""Pruning 02: why 90% sparsity does not automatically mean 10x speed."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, BG, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, pill, txt,
)


def dot_matrix(rows=6, cols=8, alive=None, cell=.48):
    alive = set(alive if alive is not None else range(rows * cols))
    cells = VGroup()
    for i in range(rows * cols):
        live = i in alive
        square = RoundedRectangle(
            width=cell * .82, height=cell * .82, corner_radius=.055,
            stroke_color=WEIGHT if live else ZERO,
            stroke_width=1.0, fill_color=GOOD if live else ZERO,
            fill_opacity=.72 if live else .1,
        )
        cells.add(square)
    cells.arrange_in_grid(rows, cols, buff=.07)
    cells.rows = rows
    cells.cols = cols
    cells.alive_indices = alive
    return cells


def card(label, color, width=1.25, height=.72):
    box = RoundedRectangle(width=width, height=height, corner_radius=.12,
                           stroke_color=color, stroke_width=1.4,
                           fill_color=color, fill_opacity=.08)
    return VGroup(box, txt(label, 20, color, width - .14))


class WhyNotTenTimes(Scene):
    DURATION = 82
    SURVIVORS = (2, 13, 16, 27, 38)

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("PRUNING & SPARSITY  /  02", 20, MUTED).move_to(UP * 7.25),
            txt("90%를 지웠는데 왜 10배 빨라지지 않을까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s — 90% pruning creates a tempting speedup expectation.
        self.text(
            "Weight의 90%를 지웠습니다",
            "계산량도 90% 줄고,\n정말 10배 빨라질까요?",
            "90% ZEROS   →   10× FASTER?",
        )
        dense = dot_matrix().move_to([0, .5, 0])
        dense_tag = pill("DENSE", WEIGHT, 2.0).next_to(dense, UP, buff=.45)
        self.play(FadeIn(dense, scale=.96), FadeIn(dense_tag), run_time=.7)
        sparse = dot_matrix(alive=self.SURVIVORS).move_to(dense)
        sparse_tag = pill("90% ZEROS", PRUNE, 2.5).move_to(dense_tag)
        self.play(FadeTransform(dense, sparse),
                  ReplacementTransform(dense_tag, sparse_tag), run_time=1.2)
        question = txt("10× ?", 38, ACCENT, weight=BOLD).next_to(sparse, DOWN, buff=.5)
        self.play(FadeIn(question, shift=UP * .12), run_time=.45)
        self.keep_stage(sparse, sparse_tag, question)
        self.to(6)

        # 6–14 s — dense GEMM still walks the unchanged rectangular matrix.
        self.text(
            "Dense 행렬곱에서는 크기가 그대로입니다",
            "값이 0으로 바뀌어도\n행과 열의 개수는 줄지 않습니다.",
            "6 × 8 matrix   →   still 6 × 8",
        )
        dense_scan = dot_matrix(alive=self.SURVIVORS).move_to([0, .4, 0])
        outline = SurroundingRectangle(dense_scan, color=WEIGHT, buff=.16,
                                       stroke_width=2)
        scanner = SurroundingRectangle(VGroup(*dense_scan[:8]), color=ACCENT,
                                       buff=.06, stroke_width=2.3)
        scan_stage = VGroup(dense_scan, outline, scanner)
        self.play(FadeOut(sparse), FadeOut(sparse_tag), FadeOut(question),
                  FadeIn(dense_scan), Create(outline), FadeIn(scanner), run_time=.75)
        for row in range(1, 6):
            target = SurroundingRectangle(
                VGroup(*dense_scan[row * 8:(row + 1) * 8]), color=ACCENT,
                buff=.06, stroke_width=2.3,
            )
            self.play(Transform(scanner, target), run_time=.23, rate_func=linear)
        self.keep_stage(scan_stage)
        self.to(14)

        # 14–21 s — distinguish a zero value from an omitted operation.
        self.text(
            "0이라는 값과 계산의 제거는 다릅니다",
            "Dense kernel은 0도\n행렬의 한 원소로 처리합니다.",
            "VALUE = 0        OPERATION ≠ 0",
        )
        ops = VGroup(*[
            card(label, PRUNE if label == "x × 0" else WEIGHT, 1.35)
            for label in ("x × .8", "x × 0", "x × −.6", "x × 0")
        ]).arrange_in_grid(2, 2, buff=(.35, .35)).move_to([0, .45, 0])
        equals = VGroup(
            txt("0", 28, PRUNE), txt("이어도", 22, MUTED),
            txt("곱셈 명령은 존재", 25, ACCENT),
        ).arrange(RIGHT, buff=.18).move_to([0, -1.35, 0])
        op_stage = VGroup(ops, equals)
        self.play(FadeOut(scan_stage), LaggedStart(*[FadeIn(x) for x in ops],
                                                   lag_ratio=.08), run_time=.7)
        self.play(FadeIn(equals, shift=UP * .1), run_time=.45)
        self.keep_stage(op_stage)
        self.to(21)

        # 21–28 s — introduce the sparse-kernel idea without claiming it is free.
        self.text(
            "그럼 0인 곳만 건너뛰면 되지 않을까요?",
            "남아 있는 값만 계산하면\n곱셈 수는 크게 줄일 수 있습니다.",
            "●만 계산하면 된다?",
        )
        skip_grid = dot_matrix(alive=self.SURVIVORS).move_to([0, .35, 0])
        zero_cells = [skip_grid[i] for i in range(48) if i not in self.SURVIVORS]
        live_cells = [skip_grid[i] for i in self.SURVIVORS]
        skip_label = pill("SKIP ZEROS?", ACCENT, 2.65).next_to(skip_grid, DOWN, buff=.5)
        self.play(FadeOut(op_stage), FadeIn(skip_grid), run_time=.55)
        self.play(*[cell.animate.set_opacity(.035) for cell in zero_cells],
                  *[Indicate(cell, color=GOOD, scale_factor=1.35)
                    for cell in live_cells], run_time=.85)
        self.play(FadeIn(skip_label), run_time=.4)
        self.keep_stage(skip_grid, skip_label)
        self.to(28)

        # 28–36 s — survivors are scattered, so their positions matter.
        self.text(
            "남은 Weight는 불규칙하게 흩어져 있습니다",
            "값만으로는 부족합니다.\n어디에 남았는지도 알아야 합니다.",
            "(row, col) 위치가 필요",
        )
        coords = ((0, 2), (1, 5), (2, 0), (3, 3), (4, 6))
        coord_labels = VGroup()
        for index, coord in zip(self.SURVIVORS, coords):
            label = txt(str(coord), 18, ACCENT).next_to(skip_grid[index], RIGHT,
                                                        buff=.1)
            coord_labels.add(label)
        self.play(FadeOut(skip_label),
                  LaggedStart(*[FadeIn(x, shift=LEFT * .08) for x in coord_labels],
                              lag_ratio=.12), run_time=1.0)
        self.play(LaggedStart(*[
            Indicate(skip_grid[i], color=GOOD, scale_factor=1.35)
            for i in self.SURVIVORS
        ], lag_ratio=.08), run_time=.75)
        self.keep_stage(skip_grid, coord_labels)
        self.to(36)

        # 36–46 s — compare sequential reads with gather-like jumps.
        self.text(
            "규칙적으로 읽던 흐름이 점프로 바뀝니다",
            "Dense는 정해진 순서로 읽지만,\nSparse는 위치를 확인하며 입력을 찾아갑니다.",
            "SEQUENTIAL READ          POSITION LOOKUP",
        )
        dense_flow = self.flow_row(range(8), WEIGHT, "DENSE").move_to([0, 1.55, 0])
        sparse_flow = self.flow_row((2, 5, 0, 3), ACCENT, "SPARSE").move_to([0, -.65, 0])
        jump_arrows = VGroup(*[
            CurvedArrow(sparse_flow[0][i].get_right(), sparse_flow[0][i + 1].get_left(),
                        angle=(-.28 if i % 2 == 0 else .28), color=ACCENT,
                        stroke_width=1.8, tip_length=.09)
            for i in range(3)
        ])
        flow_stage = VGroup(dense_flow, sparse_flow, jump_arrows)
        self.play(FadeOut(skip_grid), FadeOut(coord_labels),
                  FadeIn(dense_flow), run_time=.55)
        self.play(LaggedStart(*[GrowArrow(a) for a in dense_flow[1]],
                              lag_ratio=.08), run_time=.7)
        self.play(FadeIn(sparse_flow), LaggedStart(*[Create(a) for a in jump_arrows],
                                                   lag_ratio=.12), run_time=.85)
        self.keep_stage(flow_stage)
        self.to(46)

        # 46–54 s — make the metadata and gather cost explicit.
        self.text(
            "연산을 줄이는 대신 위치 정보가 생깁니다",
            "0은 저장하지 않지만 index를 읽고,\n그 위치의 입력을 가져와야 합니다.",
            "개념적 sparse 표현",
        )
        value_cards = VGroup(*[card(v, GOOD, 1.05) for v in
                               ("0.8", "−0.6", "0.4", "0.9")])
        value_cards.arrange(RIGHT, buff=.16).move_to([.45, 1.35, 0])
        pos_cards = VGroup(*[card(v, ACCENT, 1.05) for v in
                             ("2", "5", "0", "3")])
        pos_cards.arrange(RIGHT, buff=.16).move_to([.45, -.15, 0])
        labels = VGroup(
            txt("VALUES", 20, GOOD).move_to([-3.05, 1.35, 0]),
            txt("POSITIONS", 20, ACCENT).move_to([-3.05, -.15, 0]),
        )
        input_row = VGroup(*[card(f"x{i}", WEIGHT, .7, .58) for i in range(6)])
        input_row.arrange(RIGHT, buff=.11).move_to([0, -1.85, 0])
        gather = VGroup(*[
            Arrow(pos_cards[i].get_bottom(), input_row[p].get_top(), buff=.08,
                  color=ACCENT, stroke_width=1.5, tip_length=.08)
            for i, p in enumerate((2, 5, 0, 3))
        ])
        metadata_stage = VGroup(value_cards, pos_cards, labels, input_row, gather)
        self.play(FadeOut(flow_stage), FadeIn(labels), FadeIn(value_cards),
                  FadeIn(pos_cards), run_time=.65)
        self.play(FadeIn(input_row), LaggedStart(*[GrowArrow(a) for a in gather],
                                                 lag_ratio=.1), run_time=.9)
        self.keep_stage(metadata_stage)
        self.to(54)

        # 54–65 s — regular thread lanes versus variable work and locations.
        self.text(
            "GPU의 규칙적인 병렬 처리도 어려워질 수 있습니다",
            "Thread마다 필요한 위치와 작업량이 달라지면\n메모리 접근과 실행이 가지런하지 않습니다.",
            "REGULAR LANES              IRREGULAR LANES",
        )
        dense_threads = self.thread_panel(False).move_to([-2.15, .35, 0])
        sparse_threads = self.thread_panel(True).move_to([2.15, .35, 0])
        divider = Line([0, -2.1, 0], [0, 2.8, 0], color=MUTED,
                       stroke_width=1, stroke_opacity=.3)
        thread_stage = VGroup(dense_threads, sparse_threads, divider)
        self.play(FadeOut(metadata_stage), FadeIn(dense_threads),
                  FadeIn(divider), run_time=.65)
        self.play(FadeIn(sparse_threads), run_time=.65)
        self.play(Indicate(dense_threads[1], color=GOOD, scale_factor=1.03),
                  Indicate(sparse_threads[1], color=PRUNE, scale_factor=1.03),
                  run_time=.8)
        self.keep_stage(thread_stage)
        self.to(65)

        # 65–73 s — arithmetic savings remain real, but overhead competes with them.
        self.text(
            "곱셈 감소는 이득의 잠재력입니다",
            "실제 속도는 그 이득에서\nSparse 처리 비용을 함께 계산한 결과입니다.",
            "ARITHMETIC ↓     OVERHEAD ↑",
        )
        before = Rectangle(width=6.7, height=.58, stroke_width=0,
                           fill_color=WEIGHT, fill_opacity=.82).move_to([0, 1.85, 0])
        after = Rectangle(width=.67, height=.58, stroke_width=0,
                          fill_color=GOOD, fill_opacity=.9).align_to(before, LEFT)
        after.shift(DOWN * 1.25)
        bars = VGroup(
            before, after,
            txt("100% multiplications", 21, WEIGHT).next_to(before, UP, buff=.18),
            txt("10%", 21, GOOD).next_to(after, DOWN, buff=.18),
        )
        overhead = VGroup(
            pill("INDEXING", ACCENT, 2.05),
            pill("MEMORY ACCESS", PRUNE, 2.65),
            pill("LOAD IMBALANCE", SPARSE, 2.65),
        ).arrange(DOWN, buff=.22).move_to([1.65, -1.25, 0])
        tradeoff = VGroup(bars, overhead)
        self.play(FadeOut(thread_stage), FadeIn(before), FadeIn(bars[2]), run_time=.55)
        self.play(TransformFromCopy(before, after), FadeIn(bars[3]), run_time=.75)
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * .12) for x in overhead],
                              lag_ratio=.12), run_time=.85)
        self.keep_stage(tradeoff)
        self.to(73)

        # 73–82 s — same zero count, different structure; set up structured pruning.
        self.text(
            "중요한 건 얼마나, 그리고 어떻게 지웠는가입니다",
            "같은 수의 0이라도 배치 구조가 다르면\n하드웨어가 처리하는 방식도 달라집니다.",
            "NEXT  ·  줄 단위로 지우면 무엇이 달라질까?",
        )
        random_alive = (0, 3, 6, 9, 10, 12, 15, 17, 20, 22, 25, 27, 28, 29, 30, 31)
        structured_alive = tuple(range(8, 24))
        random_grid = dot_matrix(4, 8, random_alive, .34).move_to([-2.15, .45, 0])
        structured_grid = dot_matrix(4, 8, structured_alive, .34).move_to([2.15, .45, 0])
        final_stage = VGroup(
            random_grid, structured_grid,
            pill("RANDOM", PRUNE, 2.0).next_to(random_grid, UP, buff=.45),
            pill("ROW-WISE", GOOD, 2.25).next_to(structured_grid, UP, buff=.45),
            txt("same 50% zeros", 23, ACCENT).move_to([0, -1.25, 0]),
        )
        self.play(FadeOut(tradeoff), FadeIn(random_grid),
                  FadeIn(final_stage[2]), run_time=.6)
        self.play(FadeIn(structured_grid), FadeIn(final_stage[3]), run_time=.6)
        self.play(FadeIn(final_stage[4]),
                  Indicate(structured_grid, color=GOOD, scale_factor=1.04), run_time=.7)
        self.keep_stage(final_stage)
        self.to(82)

    def flow_row(self, values, color, title):
        boxes = VGroup(*[card(f"x{i}", color, .68, .62) for i in values])
        boxes.arrange(RIGHT, buff=.16)
        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=.035,
                  color=color, stroke_width=1.4, tip_length=.07)
            for i in range(len(boxes) - 1)
        ])
        label = txt(title, 20, color).next_to(boxes, LEFT, buff=.28)
        return VGroup(boxes, arrows, label)

    def thread_panel(self, irregular):
        title = pill("SPARSE" if irregular else "DENSE",
                     PRUNE if irregular else GOOD, 2.0)
        lanes = VGroup()
        positions = ((2, 9), (5,), (1, 14, 27), (8, 11)) if irregular else (
            (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)
        )
        for i, items in enumerate(positions):
            label = txt(f"T{i}", 18, MUTED)
            work = VGroup(*[card(str(v), PRUNE if irregular else GOOD,
                                 .46, .44) for v in items]).arrange(RIGHT, buff=.07)
            lane = VGroup(label, work).arrange(RIGHT, buff=.14, aligned_edge=DOWN)
            lanes.add(lane)
        lanes.arrange(DOWN, buff=.24, aligned_edge=LEFT)
        panel = VGroup(title, lanes).arrange(DOWN, buff=.42)
        return panel

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
