"""FlashAttention 01: reveal the quadratic intermediates of standard attention."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.flash_series.visuals import (
    HBM_BLUE, INK, K_PINK, MUTED, O_CORAL, P_VIOLET, Q_BLUE,
    S_GOLD, V_GREEN, DataCard, MatrixGrid, MemoryBox, txt,
)


class FlashAttentionStorage(Scene):
    DURATION = 64

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.add(
            txt("IO-AWARE ATTENTION  /  01", 20, MUTED).move_to(UP * 7.25),
            txt("Attention은 무엇을 저장하고 있을까?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=S_GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s: establish the three inputs and the purpose of attention.
        self.text(
            "관계를 계산하고, 정보를 조합합니다",
            "Attention은 Query와 Key의 관계를 계산하고,\n그 결과로 Value를 조합합니다.",
            "Q, K  →  관계      ·      P, V  →  출력",
        )
        inputs = VGroup(
            DataCard("Q", "Query", Q_BLUE),
            DataCard("K", "Key", K_PINK),
            DataCard("V", "Value", V_GREEN),
        ).arrange(RIGHT, buff=.42).move_to([0, .45, 0])
        self.play(LaggedStart(*[FadeIn(card, shift=UP * .15) for card in inputs],
                              lag_ratio=.18), run_time=1.2)
        self.play(Indicate(inputs[0], color=Q_BLUE), Indicate(inputs[1], color=K_PINK),
                  run_time=.8)
        self.play(Indicate(inputs[2], color=V_GREEN), run_time=.55)
        self.to(6)

        # 6–14 s: QK^T materializes a score matrix.
        self.text(
            "먼저 모든 Query와 Key를 비교합니다",
            "각 Query를 모든 Key와 비교해\n하나의 점수 행렬 S를 만듭니다.",
            "S = QKᵀ",
        )
        q = MatrixGrid(5, 3, "Q", Q_BLUE, .38).move_to([-2.9, .4, 0])
        k = MatrixGrid(5, 3, "K", K_PINK, .38).move_to([2.9, .4, 0])
        score = MatrixGrid(5, 5, "Score  S", S_GOLD, .46).move_to([0, .35, 0])
        formula = txt("QKᵀ", 31, S_GOLD).move_to([0, 2.25, 0])
        arrows = VGroup(
            Arrow(q.get_right(), score.get_left(), buff=.12, color=Q_BLUE,
                  stroke_width=2.5, tip_length=.13),
            Arrow(k.get_left(), score.get_right(), buff=.12, color=K_PINK,
                  stroke_width=2.5, tip_length=.13),
        )
        self.play(FadeOut(inputs), FadeIn(q), FadeIn(k), FadeIn(formula), run_time=.75)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=.6)
        self.play(LaggedStart(*[FadeIn(cell, scale=.65) for cell in score.cells],
                              lag_ratio=.035), FadeIn(score.name), run_time=1.75)
        self.to(14)

        # 14–20 s: make the quadratic footprint explicit.
        self.text(
            "길이가 N이면, N²개의 점수",
            "입력 길이가 N이라면 이 행렬에는\nN × N, 즉 N²개의 값이 생깁니다.",
            "sequence length N     →     N² scores",
        )
        top_dim = Brace(score.cells, UP, color=S_GOLD)
        top_label = txt("N", 24, S_GOLD).next_to(top_dim, UP, buff=.08)
        side_dim = Brace(score.cells, RIGHT, color=S_GOLD)
        side_label = txt("N", 24, S_GOLD).next_to(side_dim, RIGHT, buff=.08)
        n2 = txt("N² values", 33, S_GOLD).move_to([0, -2.0, 0])
        self.play(FadeOut(q), FadeOut(k), FadeOut(arrows), FadeOut(formula),
                  FadeOut(score.name),
                  score.animate.scale(1.18).move_to([0, .55, 0]), run_time=.8)
        self.play(GrowFromCenter(top_dim), FadeIn(top_label),
                  GrowFromCenter(side_dim), FadeIn(side_label), run_time=.65)
        self.play(FadeIn(n2, shift=UP * .15), Indicate(score.cells, color=S_GOLD),
                  run_time=.9)
        self.to(20)

        # 20–27 s: row-wise softmax changes scores into attention weights.
        self.text(
            "각 행을 확률 분포로 바꿉니다",
            "각 행에 Softmax를 적용하면 점수는\n합이 1인 Attention weight가 됩니다.",
            "P = softmax(S)      ·      each row sums to 1",
        )
        weights = MatrixGrid(
            5, 5, "Attention  P", P_VIOLET, .46,
            values=[
                [".41", ".22", ".18", ".12", ".07"],
                [".08", ".16", ".44", ".20", ".12"],
                [".14", ".11", ".19", ".38", ".18"],
                [".27", ".31", ".09", ".21", ".12"],
                [".10", ".17", ".24", ".15", ".34"],
            ],
        ).move_to(score)
        softmax = txt("softmax row by row", 24, P_VIOLET).move_to([0, -2.15, 0])
        row_box = SurroundingRectangle(score.row(0), buff=.04, color=P_VIOLET,
                                       stroke_width=2.5)
        self.play(FadeOut(VGroup(top_dim, top_label, side_dim, side_label, n2)),
                  Create(row_box), run_time=.55)
        self.play(Transform(score, weights), FadeIn(softmax), run_time=1.15)
        self.play(row_box.animate.move_to(score.row(1)), run_time=.35)
        self.play(row_box.animate.move_to(score.row(2)), run_time=.35)
        self.play(FadeOut(row_box), Indicate(score.cells, color=P_VIOLET), run_time=.65)
        self.to(27)

        # 27–34 s: P combines V and only O is consumed downstream.
        self.text(
            "가중치로 Value를 조합합니다",
            "이 가중치로 Value들을 섞으면\n최종 Attention 출력 O가 만들어집니다.",
            "O = PV",
        )
        p_small = MatrixGrid(
            5, 5, "P", P_VIOLET, .34,
            values=[
                [".41", ".22", ".18", ".12", ".07"],
                [".08", ".16", ".44", ".20", ".12"],
                [".14", ".11", ".19", ".38", ".18"],
                [".27", ".31", ".09", ".21", ".12"],
                [".10", ".17", ".24", ".15", ".34"],
            ],
        ).move_to([-2.65, .65, 0])
        v = MatrixGrid(5, 3, "V", V_GREEN, .34).move_to([.15, .65, 0])
        out = MatrixGrid(5, 3, "O", O_CORAL, .34).move_to([2.85, .65, 0])
        times = txt("×", 37, MUTED).move_to([-1.15, .55, 0])
        equals = txt("=", 37, MUTED).move_to([1.65, .55, 0])
        self.play(FadeOut(softmax), FadeOut(score), FadeIn(p_small), FadeIn(v),
                  FadeIn(times), FadeIn(equals), run_time=.75)
        self.play(LaggedStart(*[FadeIn(cell, shift=RIGHT * .08) for cell in out.cells],
                              lag_ratio=.055), FadeIn(out.name), run_time=1.4)
        self.play(Indicate(out, color=O_CORAL, scale_factor=1.06), run_time=.8)
        self.to(34)

        # 34–42 s: pull back from math to the data objects created along the way.
        self.text(
            "하지만 최종적으로 필요한 것은 O입니다",
            "그 O를 만들기까지 N² 크기의 Score S와\nAttention P가 중간 결과로 생겼습니다.",
            "final output O     ·     quadratic intermediates S, P",
        )
        s_card = DataCard("S", "N × N scores", S_GOLD, 2.45, 1.35).move_to([-2.65, .65, 0])
        p_card = DataCard("P", "N × N weights", P_VIOLET, 2.45, 1.35).move_to([0, .65, 0])
        o_card = DataCard("O", "final output", O_CORAL, 2.45, 1.35).move_to([2.65, .65, 0])
        data_life = VGroup(s_card, p_card, o_card)
        self.play(FadeOut(VGroup(p_small, v, out, times, equals)), FadeIn(data_life),
                  run_time=.75)
        self.play(Indicate(s_card, color=S_GOLD, scale_factor=1.06),
                  Indicate(p_card, color=P_VIOLET, scale_factor=1.06), run_time=.85)
        n2_pair = VGroup(
            txt("N²", 35, S_GOLD).next_to(s_card, DOWN, buff=.35),
            txt("N²", 35, P_VIOLET).next_to(p_card, DOWN, buff=.35),
        )
        self.play(FadeIn(n2_pair, shift=UP * .1), run_time=.55)
        self.to(42)

        # 42–52 s: show the materialized standard-attention path through HBM.
        self.text(
            "연산 사이에서 쓰고, 다시 읽습니다",
            "표준적인 구현은 이런 중간 결과를 HBM에 쓰고,\n다음 연산에서 다시 읽어 계산을 이어갑니다.",
            "QKᵀ  →  write S  →  softmax  →  write P  →  ×V",
        )
        compute_top = VGroup(
            DataCard("QKᵀ", "compute", Q_BLUE, 1.65, 1.0),
            DataCard("softmax", "compute", P_VIOLET, 1.85, 1.0),
            DataCard("× V", "compute", V_GREEN, 1.65, 1.0),
        ).arrange(RIGHT, buff=.58).move_to([0, 1.65, 0])
        hbm = MemoryBox().move_to([0, -1.3, 0])
        s_token = DataCard("S", "N × N", S_GOLD, 1.15, .72).move_to([-.85, -1.52, 0])
        p_token = DataCard("P", "N × N", P_VIOLET, 1.15, .72).move_to([1.45, -1.52, 0])
        paths = VGroup(
            Arrow(compute_top[0].get_bottom(), s_token.get_top(), buff=.1,
                  color=S_GOLD, stroke_width=2.5, tip_length=.14),
            Arrow(s_token.get_top() + RIGHT * .2, compute_top[1].get_bottom() + LEFT * .3,
                  buff=.1, color=S_GOLD, stroke_width=2.5, tip_length=.14),
            Arrow(compute_top[1].get_bottom() + RIGHT * .3, p_token.get_top(), buff=.1,
                  color=P_VIOLET, stroke_width=2.5, tip_length=.14),
            Arrow(p_token.get_top() + RIGHT * .2, compute_top[2].get_bottom(), buff=.1,
                  color=P_VIOLET, stroke_width=2.5, tip_length=.14),
        )
        io_labels = VGroup(
            txt("WRITE", 17, S_GOLD).move_to([-2.15, .3, 0]),
            txt("READ", 17, S_GOLD).move_to([-.95, .35, 0]),
            txt("WRITE", 17, P_VIOLET).move_to([.95, .35, 0]),
            txt("READ", 17, P_VIOLET).move_to([2.2, .3, 0]),
        )
        self.play(FadeOut(VGroup(data_life, n2_pair)), FadeIn(compute_top), FadeIn(hbm),
                  run_time=.8)
        self.play(GrowArrow(paths[0]), FadeIn(io_labels[0]), FadeIn(s_token), run_time=.65)
        self.play(GrowArrow(paths[1]), FadeIn(io_labels[1]), run_time=.65)
        self.play(GrowArrow(paths[2]), FadeIn(io_labels[2]), FadeIn(p_token), run_time=.65)
        self.play(GrowArrow(paths[3]), FadeIn(io_labels[3]), run_time=.65)
        self.play(Indicate(VGroup(s_token, p_token), scale_factor=1.06), run_time=.75)
        self.to(52)

        # 52–60 s: erase the intermediates while preserving the exact output.
        self.text(
            "이 두 행렬을 꼭 남겨야 할까?",
            "거대한 Attention 중간 행렬을 전부 저장하지 않고도\n같은 출력 O를 만들 수 있을까요?",
            "store less intermediates     ·     keep the same O",
        )
        question_s = MatrixGrid(6, 6, "Score  S", S_GOLD, .34).move_to([-2.25, .75, 0])
        question_p = MatrixGrid(6, 6, "Attention  P", P_VIOLET, .34).move_to([.2, .75, 0])
        arrow_o = Arrow([1.45, .75, 0], [2.45, .75, 0], buff=.05, color=O_CORAL,
                        stroke_width=3, tip_length=.15)
        final_o = DataCard("O", "same output", O_CORAL, 1.8, 1.15).move_to([3.25, .75, 0])
        strike_s = Line(question_s.get_corner(UL), question_s.get_corner(DR),
                        color=MUTED, stroke_width=4)
        strike_p = Line(question_p.get_corner(UL), question_p.get_corner(DR),
                        color=MUTED, stroke_width=4)
        self.play(FadeOut(VGroup(compute_top, hbm, s_token, p_token, paths, io_labels)),
                  FadeIn(question_s), FadeIn(question_p), GrowArrow(arrow_o), FadeIn(final_o),
                  run_time=.85)
        self.play(Create(strike_s), Create(strike_p), run_time=.75)
        self.play(question_s.animate.set_opacity(.12), question_p.animate.set_opacity(.12),
                  strike_s.animate.set_opacity(.18), strike_p.animate.set_opacity(.18),
                  Indicate(final_o, color=O_CORAL, scale_factor=1.08), run_time=1.0)
        self.to(60)

        # 60–64 s: name the paper and leave only a tiny tile as the next clue.
        self.text(
            "FlashAttention은 여기서 시작합니다",
            "수학적 답은 그대로 둔 채, 무엇을 저장하고\n어떤 순서로 계산할지를 다시 묻습니다.",
            "next  ·  계산보다 데이터를 움직이는 방법",
        )
        tile = VGroup(
            Square(side_length=.9, stroke_color=S_GOLD, stroke_width=2.5,
                   fill_color=S_GOLD, fill_opacity=.12),
            txt("tile", 21, S_GOLD),
        ).move_to([0, .45, 0])
        title = txt("FlashAttention", 40, INK).move_to([0, 2.15, 0])
        exact = txt("same answer", 24, O_CORAL).move_to([0, -1.25, 0])
        self.play(FadeOut(VGroup(question_s, question_p, arrow_o, final_o,
                                 strike_s, strike_p)), FadeIn(title), FadeIn(tile),
                  run_time=.8)
        self.play(Circumscribe(tile, color=S_GOLD, buff=.18), FadeIn(exact), run_time=.85)
        self.to(64)

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 23, S_GOLD).move_to(DOWN * 4.72)
        self.sub = txt(sub, 27).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.35)

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(
                self.progress.animate.stretch_to_fit_width(width).move_to(
                    [-3.8 + width / 2, -7.35, 0]
                ),
                run_time=min(.28, remain),
            )
            self.wait(max(0, target - self.time))
