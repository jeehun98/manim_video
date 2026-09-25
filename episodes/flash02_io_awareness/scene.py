"""FlashAttention 02: shift the cost model from FLOPs to memory traffic."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.flash_series.visuals import (
    HBM_BLUE, INK, K_PINK, MUTED, O_CORAL, P_VIOLET, Q_BLUE,
    S_GOLD, V_GREEN, DataCard, MatrixGrid, MemoryBox, txt,
)


class FlashAttentionIO(Scene):
    DURATION = 72

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.add(
            txt("IO-AWARE ATTENTION  /  02", 20, MUTED).move_to(UP * 7.25),
            txt("계산보다 데이터 이동이 문제라면?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=S_GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–6 s: recap the quadratic intermediates from episode 1.
        self.text(
            "앞에서 발견한 두 중간 행렬",
            "앞에서는 Attention 계산 과정에서\n큰 중간 행렬 S와 P가 생기는 것을 봤습니다.",
            "QKᵀ  →  S  →  softmax  →  P  →  O",
        )
        chain = self.attention_chain()
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * .12) for item in chain],
                              lag_ratio=.1), run_time=1.25)
        self.play(Indicate(chain[2], color=S_GOLD, scale_factor=1.08),
                  Indicate(chain[6], color=P_VIOLET, scale_factor=1.08), run_time=.8)
        self.to(6)

        # 6–13 s: introduce location as part of the cost.
        self.text(
            "값의 위치도 계산 비용을 만듭니다",
            "문제는 값을 계산하는 것뿐 아니라,\n어디에 저장하고 다시 읽느냐에도 있습니다.",
            "same arithmetic     ·     different data movement",
        )
        hbm = self.hbm_region().move_to([0, 1.4, 0])
        onchip = self.onchip_region().move_to([0, -1.25, 0])
        bridge = DoubleArrow(hbm.get_bottom(), onchip.get_top(), buff=.15,
                             color=MUTED, stroke_width=2.5, tip_length=.13)
        hierarchy = VGroup(hbm, onchip, bridge)
        self.play(FadeOut(chain), FadeIn(hbm), FadeIn(onchip), GrowFromCenter(bridge),
                  run_time=.85)
        self.play(Indicate(bridge, color=S_GOLD, scale_factor=1.04), run_time=.8)
        self.to(13)

        # 13–20 s: HBM is capacious, but repeated transfers are not free.
        self.text(
            "HBM은 크지만, 이동에는 비용이 듭니다",
            "HBM은 많은 데이터를 저장할 수 있지만, 계산 중에\n큰 값을 계속 읽고 쓰면 데이터 이동이 반복됩니다.",
            "large capacity     ·     repeated READ / WRITE",
        )
        s_big = MatrixGrid(6, 6, "Score  S", S_GOLD, .34).move_to(hbm.get_center())
        down = Arrow(onchip.get_top() + LEFT * 1.1, hbm.get_bottom() + LEFT * 1.1,
                     buff=.12, color=S_GOLD, stroke_width=3, tip_length=.15)
        up = Arrow(hbm.get_bottom() + RIGHT * 1.1, onchip.get_top() + RIGHT * 1.1,
                   buff=.12, color=S_GOLD, stroke_width=3, tip_length=.15)
        write = txt("WRITE", 18, S_GOLD).next_to(down, LEFT, buff=.08)
        read = txt("READ", 18, S_GOLD).next_to(up, RIGHT, buff=.08)
        self.play(FadeOut(bridge), FadeIn(s_big), GrowArrow(down), FadeIn(write), run_time=.75)
        self.play(GrowArrow(up), FadeIn(read), run_time=.75)
        self.play(Indicate(VGroup(down, up), color=S_GOLD, scale_factor=1.05), run_time=.75)
        self.to(20)

        # 20–27 s: on-chip memory is small and close to compute.
        self.text(
            "On-chip memory는 작고 가깝습니다",
            "반대로 GPU 안쪽의 메모리는 훨씬 작지만,\n계산 장치 가까이에서 사용할 수 있습니다.",
            "small capacity     ·     close to compute",
        )
        compute = DataCard("Compute", "matrix operations", V_GREEN, 2.25, 1.0).move_to([2.35, -1.25, 0])
        onchip_target = self.onchip_region().move_to([-.8, -1.25, 0])
        near = DoubleArrow(onchip_target.get_right(), compute.get_left(), buff=.12,
                           color=V_GREEN, stroke_width=3, tip_length=.14)
        self.play(FadeOut(VGroup(s_big, down, up, write, read)),
                  Transform(onchip, onchip_target), FadeIn(compute), GrowFromCenter(near),
                  hbm.animate.set_opacity(.3), run_time=.9)
        self.play(Indicate(VGroup(onchip, compute), color=V_GREEN, scale_factor=1.04),
                  run_time=.75)
        self.to(27)

        # 27–36 s: standard materialized attention writes and rereads S.
        self.text(
            "Score S를 쓰고, Softmax가 다시 읽습니다",
            "일반적인 Attention은 점수 행렬을 계산해 HBM에\n기록하고, Softmax를 위해 다시 읽습니다.",
            "QKᵀ  →  WRITE S  →  HBM  →  READ S  →  softmax",
        )
        standard = self.standard_io_diagram(first_half=True)
        self.play(FadeOut(VGroup(hbm, onchip, compute, near)), FadeIn(standard.base), run_time=.8)
        self.play(GrowArrow(standard.arrows[0]), FadeIn(standard.labels[0]),
                  FadeIn(standard.tokens[0]), run_time=.65)
        self.play(GrowArrow(standard.arrows[1]), FadeIn(standard.labels[1]), run_time=.65)
        self.play(Indicate(standard.tokens[0], color=S_GOLD, scale_factor=1.08), run_time=.7)
        self.to(36)

        # 36–44 s: P repeats the same round trip before multiplying V.
        self.text(
            "Attention P도 다시 왕복할 수 있습니다",
            "Softmax로 만든 가중치도 다시 저장하고,\nValue와 곱하기 위해 다시 읽을 수 있습니다.",
            "softmax  →  WRITE P  →  HBM  →  READ P  →  ×V",
        )
        self.play(GrowArrow(standard.arrows[2]), FadeIn(standard.labels[2]),
                  FadeIn(standard.tokens[1]), run_time=.65)
        self.play(GrowArrow(standard.arrows[3]), FadeIn(standard.labels[3]), run_time=.65)
        self.play(Indicate(standard.tokens[1], color=P_VIOLET, scale_factor=1.08), run_time=.7)
        traffic = txt("two N × N round trips", 26, O_CORAL).move_to([0, -2.85, 0])
        self.play(FadeIn(traffic), Indicate(standard.arrows, color=O_CORAL), run_time=.8)
        self.to(44)

        # 44–51 s: replace a FLOP-only view with an IO-aware view.
        self.text(
            "연산 횟수만으로는 보이지 않는 비용",
            "FlashAttention은 FLOP만 세는 대신, GPU 메모리\n사이의 read와 write까지 함께 봅니다.",
            "FLOPs only     →     FLOPs + memory IO",
        )
        flop_card = DataCard("FLOPs", "arithmetic", Q_BLUE, 2.45, 1.45).move_to([-2.35, .55, 0])
        io_card = DataCard("Memory IO", "HBM ↔ on-chip", S_GOLD, 2.75, 1.45).move_to([2.15, .55, 0])
        plus = txt("+", 42, MUTED).move_to([0, .55, 0])
        meter = VGroup(
            flop_card, plus, io_card,
            txt("IO-aware cost model", 28, S_GOLD).move_to([0, -1.35, 0]),
        )
        self.play(FadeOut(VGroup(standard, traffic)), FadeIn(meter), run_time=.85)
        self.play(Indicate(io_card, color=S_GOLD, scale_factor=1.08), run_time=.85)
        self.to(51)

        # 51–59 s: partition Q, K, and V and move only one tile on chip.
        self.text(
            "전체 대신 작은 tile을 가져옵니다",
            "전체 행렬을 한꺼번에 처리하지 않고, 필요한 부분을\n작은 블록으로 나눠 GPU 안쪽으로 가져옵니다.",
            "Q, K, V blocks     →     one on-chip working set",
        )
        tiled = VGroup(
            self.tiled_matrix("Q", Q_BLUE),
            self.tiled_matrix("K", K_PINK),
            self.tiled_matrix("V", V_GREEN),
        ).arrange(RIGHT, buff=.48).move_to([0, 1.35, 0])
        local = self.onchip_region(width=4.4, height=1.35).move_to([0, -1.3, 0])
        q_tile = self.tile_token("Qᵢ", Q_BLUE).move_to(tiled[0].get_center())
        k_tile = self.tile_token("Kⱼ", K_PINK).move_to(tiled[1].get_center())
        v_tile = self.tile_token("Vⱼ", V_GREEN).move_to(tiled[2].get_center())
        tile_group = VGroup(q_tile, k_tile, v_tile)
        self.play(FadeOut(flop_card), FadeOut(plus), FadeOut(io_card), FadeOut(meter[3]),
                  FadeIn(tiled), FadeIn(local), run_time=.8)
        self.remove(meter, flop_card, plus, io_card, meter[3])
        self.play(tile_group.animate.arrange(RIGHT, buff=.25).move_to(local.get_center() + DOWN * .12),
                  run_time=1.2)
        self.play(Indicate(tile_group, color=S_GOLD, scale_factor=1.05), run_time=.7)
        self.to(59)

        # 59–66 s: keep the intermediate work local and update compact state.
        self.text(
            "가져온 데이터로 가능한 계산을 이어갑니다",
            "블록 안에서는 local score를 계산하고 상태를 갱신해,\n거대한 중간 행렬 전체를 HBM에 남기지 않습니다.",
            "local score  →  state update  →  output state",
        )
        local_big = self.onchip_region(width=6.6, height=3.1).move_to([0, .15, 0])
        local_flow = VGroup(
            DataCard("local score", "QᵢKⱼᵀ", S_GOLD, 1.85, 1.0),
            txt("→", 30, MUTED),
            DataCard("state", "update", P_VIOLET, 1.55, 1.0),
            txt("→", 30, MUTED),
            DataCard("output", "state", O_CORAL, 1.65, 1.0),
        ).arrange(RIGHT, buff=.2).move_to([0, -.05, 0])
        no_matrix = VGroup(
            MatrixGrid(5, 5, "N × N intermediate", MUTED, .26).set_opacity(.22),
            Line([-1.0, .75, 0], [1.0, -.75, 0], color=O_CORAL, stroke_width=4),
        ).move_to([0, -2.45, 0]).scale(.72)
        self.play(*[FadeOut(matrix) for matrix in tiled], FadeOut(local), FadeOut(tile_group),
                  FadeIn(local_big),
                  LaggedStart(*[FadeIn(item, shift=RIGHT * .08) for item in local_flow],
                              lag_ratio=.12), run_time=1.2)
        self.remove(tiled, *list(tiled), local, tile_group)
        self.play(FadeIn(no_matrix), run_time=.55)
        self.play(Indicate(local_flow, color=S_GOLD, scale_factor=1.025), run_time=.75)
        self.to(66)

        # 66–72 s: hand the exact-softmax problem to episode 3.
        self.text(
            "그런데 Softmax는 전체가 필요하지 않을까?",
            "분모의 합을 구하려면 모든 score를\n먼저 알아야 하는 것처럼 보입니다.",
            "next  ·  전체를 저장하지 않고 Softmax하기",
        )
        score_tiles = VGroup(*[
            self.tile_token(f"S{i + 1}", [Q_BLUE, K_PINK, V_GREEN, P_VIOLET][i], 1.05, .82)
            for i in range(4)
        ]).arrange(RIGHT, buff=.3).move_to([0, 1.6, 0])
        arrows = VGroup(*[
            Arrow(tile.get_bottom(), [0, .1, 0], buff=.12, color=tile[0].get_stroke_color(),
                  stroke_width=2, tip_length=.12)
            for tile in score_tiles
        ])
        softmax_q = DataCard("Softmax ?", "needs all scores?", S_GOLD, 3.0, 1.25).move_to([0, -.55, 0])
        formula = txt("exp(xᵢ)  /  Σⱼ exp(xⱼ)", 29, INK).move_to([0, -2.15, 0])
        self.play(FadeOut(VGroup(local_big, local_flow, no_matrix)), FadeIn(score_tiles),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12),
                  FadeIn(softmax_q), run_time=1.1)
        self.play(FadeIn(formula), Indicate(softmax_q, color=S_GOLD, scale_factor=1.06),
                  run_time=.8)
        self.to(72)

    def attention_chain(self):
        items = VGroup(
            DataCard("QKᵀ", "compute", Q_BLUE, 1.25, .86),
            txt("→", 25, MUTED),
            DataCard("S", "N × N", S_GOLD, 1.1, .86),
            txt("→", 25, MUTED),
            DataCard("softmax", "row-wise", P_VIOLET, 1.55, .86),
            txt("→", 25, MUTED),
            DataCard("P", "N × N", P_VIOLET, 1.1, .86),
            txt("→", 25, MUTED),
            DataCard("O", "output", O_CORAL, 1.1, .86),
        ).arrange(RIGHT, buff=.18).move_to([0, .45, 0])
        return items

    def hbm_region(self):
        box = RoundedRectangle(width=6.9, height=1.85, corner_radius=.16,
                               stroke_color=HBM_BLUE, stroke_width=2,
                               fill_color=HBM_BLUE, fill_opacity=.09)
        return VGroup(
            box,
            txt("HBM", 28, HBM_BLUE).move_to(box.get_left() + RIGHT * .7),
            txt("large capacity", 20, MUTED).move_to(box.get_right() + LEFT * 1.35),
        )

    def onchip_region(self, width=3.7, height=1.4):
        box = RoundedRectangle(width=width, height=height, corner_radius=.16,
                               stroke_color=V_GREEN, stroke_width=2,
                               fill_color=V_GREEN, fill_opacity=.08)
        return VGroup(
            box,
            txt("On-chip memory", 23, V_GREEN, width - .25).move_to(
                box.get_top() + DOWN * .3
            ),
            txt("small · close", 18, MUTED).move_to(box.get_top() + DOWN * .65),
        )

    def standard_io_diagram(self, first_half=False):
        base = VGroup(
            DataCard("QKᵀ", "compute", Q_BLUE, 1.65, 1.0).move_to([-2.65, 1.75, 0]),
            DataCard("softmax", "compute", P_VIOLET, 1.85, 1.0).move_to([0, 1.75, 0]),
            DataCard("× V", "compute", V_GREEN, 1.65, 1.0).move_to([2.65, 1.75, 0]),
            MemoryBox(width=7.3, height=1.75).move_to([0, -1.15, 0]),
        )
        s = DataCard("S", "N × N", S_GOLD, 1.15, .72).move_to([-.9, -1.38, 0])
        p = DataCard("P", "N × N", P_VIOLET, 1.15, .72).move_to([1.45, -1.38, 0])
        arrows = VGroup(
            Arrow(base[0].get_bottom(), s.get_top(), buff=.1, color=S_GOLD,
                  stroke_width=2.5, tip_length=.14),
            Arrow(s.get_top() + RIGHT * .18, base[1].get_bottom() + LEFT * .28,
                  buff=.1, color=S_GOLD, stroke_width=2.5, tip_length=.14),
            Arrow(base[1].get_bottom() + RIGHT * .28, p.get_top(), buff=.1,
                  color=P_VIOLET, stroke_width=2.5, tip_length=.14),
            Arrow(p.get_top() + RIGHT * .18, base[2].get_bottom(), buff=.1,
                  color=P_VIOLET, stroke_width=2.5, tip_length=.14),
        )
        labels = VGroup(
            txt("WRITE", 17, S_GOLD).move_to([-2.08, .32, 0]),
            txt("READ", 17, S_GOLD).move_to([-.78, .37, 0]),
            txt("WRITE", 17, P_VIOLET).move_to([.82, .37, 0]),
            txt("READ", 17, P_VIOLET).move_to([2.15, .32, 0]),
        )
        group = VGroup(base, arrows, labels, s, p)
        group.base, group.arrows, group.labels, group.tokens = base, arrows, labels, VGroup(s, p)
        return group

    def tiled_matrix(self, label, color):
        grid = MatrixGrid(6, 4, label, color, .32)
        left_x = grid.cells.get_left()[0] - .04
        right_x = grid.cells.get_right()[0] + .04
        y_one = grid.cells[7].get_bottom()[1]
        y_two = grid.cells[15].get_bottom()[1]
        separators = VGroup(
            Line([left_x, y_one, 0], [right_x, y_one, 0], color=color, stroke_width=3),
            Line([left_x, y_two, 0], [right_x, y_two, 0], color=color, stroke_width=3),
        )
        return VGroup(grid, separators)

    def tile_token(self, label, color, width=1.0, height=.72):
        box = RoundedRectangle(width=width, height=height, corner_radius=.1,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.14)
        return VGroup(box, txt(label, 21, color, width - .15))

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
