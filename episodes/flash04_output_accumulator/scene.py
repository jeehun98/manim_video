"""FlashAttention 04: update the attention output alongside online softmax."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.flash_series.visuals import (
    HBM_BLUE, INK, K_PINK, MUTED, O_CORAL, P_VIOLET, Q_BLUE,
    S_GOLD, V_GREEN, DataCard, MatrixGrid, MemoryBox, txt,
)


SCORES = ((1, 3, 2), (2, 5, 4), (0, 4, 1))
VALUES = ((1, 2, 4), (3, 6, 8), (2, 5, 7))
COLORS = (Q_BLUE, K_PINK, V_GREEN)


class NumberBlock(VGroup):
    def __init__(self, values, name, color, cell_width=.78, **kwargs):
        super().__init__(**kwargs)
        self.cells = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=cell_width, height=.78, corner_radius=.09,
                stroke_color=color, stroke_width=1.7,
                fill_color=color, fill_opacity=.08,
            )
            self.cells.add(VGroup(box, txt(str(value), 26, color)))
        self.cells.arrange(RIGHT, buff=.1)
        self.name = txt(name, 21, color).next_to(self.cells, UP, buff=.16)
        self.add(self.cells, self.name)


class AttentionOutputAccumulator(Scene):
    DURATION = 80

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("IO-AWARE ATTENTION  /  04", 20, MUTED).move_to(UP * 7.25),
            txt("Attention 출력도 바로 누적할 수 있을까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=S_GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s: recap the compact online-softmax state.
        self.text(
            "앞에서는 두 값만 계속 갱신했습니다",
            "score 전체를 저장하지 않고도 현재 최댓값 m과\n누적 지수합 ℓ을 블록마다 갱신할 수 있었습니다.",
            "score blocks pass     ·     m, ℓ remain",
        )
        passing = VGroup(*[
            NumberBlock(scores, f"S{i + 1}", color, .62).scale(.78)
            for i, (scores, color) in enumerate(zip(SCORES, COLORS))
        ]).arrange(RIGHT, buff=.45).move_to([0, 1.45, 0])
        state_ml = VGroup(
            DataCard("m = 5", "running max", P_VIOLET, 2.35, 1.15),
            DataCard("ℓ = 2.014", "running exp sum", S_GOLD, 2.65, 1.15),
        ).arrange(RIGHT, buff=.4).move_to([0, -.65, 0])
        arrows_ml = VGroup(*[
            Arrow(block.get_bottom(), state_ml.get_top(), buff=.15, color=color,
                  stroke_width=2, tip_length=.11)
            for block, color in zip(passing, COLORS)
        ])
        recap = VGroup(passing, state_ml, arrows_ml)
        self.play(LaggedStart(*[FadeIn(block, shift=RIGHT * .12) for block in passing],
                              lag_ratio=.15), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_ml], lag_ratio=.12),
                  FadeIn(state_ml), run_time=.85)
        self.play(Indicate(state_ml, color=S_GOLD, scale_factor=1.04), run_time=.7)
        self.to(7)

        # 7–14 s: attention ultimately needs a value-weighted output.
        self.text(
            "하지만 목적은 Softmax 자체가 아닙니다",
            "Attention의 목적은 Softmax 가중치로\nValue를 섞어 최종 출력 O를 만드는 것입니다.",
            "Softmax weights  ×  V  →  O",
        )
        p = NumberBlock((.1, .6, .3), "weights", P_VIOLET, .82).move_to([-2.45, .45, 0])
        v = NumberBlock((1, 2, 4), "Value", V_GREEN, .82).move_to([.15, .45, 0])
        o = DataCard("O", "weighted output", O_CORAL, 1.8, 1.2).move_to([3.0, .45, 0])
        times = txt("×", 36, MUTED).move_to([-1.15, .4, 0])
        arrow_o = Arrow(v.get_right(), o.get_left(), buff=.16, color=O_CORAL,
                        stroke_width=3, tip_length=.15)
        objective = VGroup(p, v, o, times, arrow_o)
        self.play(*[FadeOut(block) for block in passing], FadeOut(arrows_ml),
                  *[FadeOut(card) for card in state_ml], FadeIn(p), FadeIn(v),
                  FadeIn(times), GrowArrow(arrow_o), FadeIn(o), run_time=.9)
        self.remove(recap, passing, state_ml, arrows_ml, *list(passing), *list(state_ml))
        self.play(Indicate(o, color=O_CORAL, scale_factor=1.08), run_time=.75)
        self.to(14)

        # 14–23 s: pair each score block with its corresponding value block.
        self.text(
            "Key와 Value block을 함께 가져옵니다",
            "첫 번째 Key block의 score를 계산할 때,\n그 위치에 대응하는 Value block도 함께 가져옵니다.",
            "QᵢK₁ᵀ  →  scores₁     +     V₁",
        )
        q = DataCard("Qᵢ", "query block", Q_BLUE, 1.7, 1.05).move_to([-3.0, 1.35, 0])
        k1 = DataCard("K₁", "key block", K_PINK, 1.7, 1.05).move_to([-.75, 1.35, 0])
        s1 = NumberBlock(SCORES[0], "local scores₁", S_GOLD).move_to([2.25, 1.35, 0])
        v1 = NumberBlock(VALUES[0], "Value V₁", V_GREEN).move_to([0, -1.15, 0])
        multiply = txt("×", 34, MUTED).move_to([-1.88, 1.3, 0])
        score_arrow = Arrow(k1.get_right(), s1.get_left(), buff=.14,
                            color=S_GOLD, stroke_width=3, tip_length=.15)
        pair = VGroup(q, k1, s1, v1, multiply, score_arrow)
        self.play(*[FadeOut(item) for item in objective], FadeIn(q), FadeIn(k1),
                  FadeIn(multiply), GrowArrow(score_arrow), FadeIn(s1), FadeIn(v1),
                  run_time=1.0)
        self.remove(objective, *list(objective))
        self.play(Indicate(VGroup(s1, v1), color=S_GOLD, scale_factor=1.04), run_time=.75)
        self.to(23)

        # 23–32 s: compute the first block's normalized output state.
        self.text(
            "현재 block의 출력 기여를 계산합니다",
            "현재 score의 지수 가중치와 V₁을 곱해\n지금까지의 Attention 출력을 만듭니다.",
            "weighted sum 3.607     ÷     ℓ₁ 1.503     =     O₁ 2.399",
        )
        weights1 = NumberBlock((".135", "1", ".368"), "exp(score − 3)", S_GOLD, .82).move_to([-2.7, .75, 0])
        value1 = NumberBlock(VALUES[0], "V₁", V_GREEN, .82).move_to([-.05, .75, 0])
        state1 = self.state_panel("STATE 1", "m = 3", "ℓ = 1.503", "O = 2.399", Q_BLUE).move_to([2.75, .35, 0])
        times1 = txt("×", 34, MUTED).move_to([-1.38, .7, 0])
        update1 = Arrow(value1.get_right(), state1.get_left(), buff=.15,
                        color=O_CORAL, stroke_width=3, tip_length=.14)
        first_state = VGroup(weights1, value1, state1, times1, update1)
        self.play(*[FadeOut(item) for item in pair], FadeIn(weights1), FadeIn(value1),
                  FadeIn(times1), GrowArrow(update1), FadeIn(state1), run_time=.9)
        self.remove(pair, *list(pair))
        self.play(Indicate(state1, color=Q_BLUE, scale_factor=1.05), run_time=.75)
        self.to(32)

        # 32–41 s: block 2 updates the max and denominator exactly as before.
        self.text(
            "다음 K₂, V₂ block이 들어옵니다",
            "새 score에서 더 큰 값 5가 나타나면\nm과 ℓ을 새로운 기준으로 갱신합니다.",
            "m : 3 → 5     ·     ℓ : 1.503 → 1.621",
        )
        k2 = DataCard("K₂", "key block", K_PINK, 1.55, 1.0).move_to([-3.0, 1.45, 0])
        v2 = NumberBlock(VALUES[1], "V₂", V_GREEN, .72).move_to([-3.0, -.15, 0])
        s2 = NumberBlock(SCORES[1], "scores₂", S_GOLD, .72).move_to([-.55, 1.45, 0])
        state_change = VGroup(
            self.state_panel("OLD", "m = 3", "ℓ = 1.503", "O = 2.399", Q_BLUE),
            txt("→", 34, MUTED),
            self.state_panel("UPDATE", "m = 5", "ℓ = 1.621", "O = ?", K_PINK),
        ).arrange(RIGHT, buff=.22).scale(.7).move_to([1.45, -.75, 0])
        block2_scene = VGroup(k2, v2, s2, state_change)
        self.play(*[FadeOut(item) for item in first_state], FadeIn(k2), FadeIn(v2),
                  FadeIn(s2), FadeIn(state_change), run_time=.9)
        self.remove(first_state, *list(first_state))
        self.play(Indicate(s2.cells[1], color=S_GOLD, scale_factor=1.15),
                  Indicate(state_change[-1], color=K_PINK, scale_factor=1.04), run_time=.8)
        self.to(41)

        # 41–51 s: rescale the old weighted contribution, add the new one, renormalize.
        self.text(
            "이전 출력의 기여량도 같은 기준으로 보정합니다",
            "이전 output이 가진 weight mass를 새 최댓값 기준으로\n줄이고, 새 block의 Value 기여를 더해 다시 정규화합니다.",
            "rescale old contribution     +     add new V contribution",
        )
        old = DataCard("old O mass", "× exp(3−5)", Q_BLUE, 2.25, 1.2).move_to([-2.65, .7, 0])
        new = DataCard("new V₂ mass", "weighted by scores₂", K_PINK, 2.45, 1.2).move_to([.05, .7, 0])
        state2 = self.state_panel("STATE 2", "m = 5", "ℓ = 1.621", "O = 5.910", S_GOLD).move_to([2.85, .45, 0])
        plus = txt("+", 35, MUTED).move_to([-1.3, .65, 0])
        arrow2 = Arrow(new.get_right(), state2.get_left(), buff=.13,
                       color=O_CORAL, stroke_width=3, tip_length=.14)
        correction = VGroup(old, new, state2, plus, arrow2)
        self.play(*[FadeOut(item) for item in block2_scene], FadeIn(old), FadeIn(new),
                  FadeIn(plus), GrowArrow(arrow2), FadeIn(state2), run_time=.9)
        self.remove(block2_scene, *list(block2_scene))
        scale_tag = txt("same reference m = 5", 23, P_VIOLET).move_to([-1.3, -1.0, 0])
        self.play(FadeIn(scale_tag), Indicate(state2, color=S_GOLD, scale_factor=1.05),
                  run_time=.8)
        self.to(51)

        # 51–60 s: repeat for the last block and explicitly discard prior tiles.
        self.text(
            "block이 지나가면 score와 weight는 버립니다",
            "같은 갱신을 반복하면 지나간 score와 Softmax weight를\n남기지 않고 m, ℓ, O 세 상태만 유지할 수 있습니다.",
            "Kⱼ, Vⱼ pass     ·     m, ℓ, O remain",
        )
        tiles = VGroup(*[
            VGroup(
                DataCard(f"K{i + 1}", "tile", K_PINK, 1.15, .8),
                DataCard(f"V{i + 1}", "tile", V_GREEN, 1.15, .8),
            ).arrange(DOWN, buff=.18)
            for i in range(3)
        ]).arrange(RIGHT, buff=.55).move_to([-1.65, .45, 0])
        final_state = self.state_panel("FINAL STATE", "m = 5", "ℓ = 2.014", "O = 5.741", V_GREEN).move_to([2.65, .35, 0])
        flow_tiles = VGroup(*[
            Arrow(tile.get_right(), final_state.get_left(), buff=.16,
                  color=COLORS[i], stroke_width=2.2, tip_length=.12)
            for i, tile in enumerate(tiles)
        ])
        self.play(*[FadeOut(item) for item in correction], FadeOut(scale_tag),
                  FadeIn(tiles), LaggedStart(*[GrowArrow(a) for a in flow_tiles], lag_ratio=.12),
                  FadeIn(final_state), run_time=1.05)
        self.keep_stage(tiles, flow_tiles, final_state)
        self.play(LaggedStart(*[FadeOut(tile, shift=LEFT * .2) for tile in tiles],
                              lag_ratio=.14), flow_tiles.animate.set_opacity(.12), run_time=1.0)
        self.keep_stage(flow_tiles, final_state)
        self.play(Indicate(final_state, color=V_GREEN, scale_factor=1.06), run_time=.7)
        self.to(60)

        # 60–68 s: standard and block-wise attention yield the same numerical O.
        self.text(
            "한꺼번에 만든 Attention과 결과는 같습니다",
            "모든 score와 Softmax weight를 먼저 만든 경우와\nblock-wise로 갱신한 마지막 출력 O는 같습니다.",
            "Standard Attention     =     Block-wise Attention",
        )
        standard = VGroup(
            txt("STANDARD", 22, Q_BLUE),
            DataCard("S → P → PV", "full intermediates", Q_BLUE, 2.8, 1.15),
            DataCard("O = 5.741", "final output", O_CORAL, 2.4, 1.15),
        ).arrange(DOWN, buff=.35).move_to([-2.25, .15, 0])
        blockwise = VGroup(
            txt("BLOCK-WISE", 22, V_GREEN),
            DataCard("tiles → state", "m, ℓ, O", V_GREEN, 2.8, 1.15),
            DataCard("O = 5.741", "final output", O_CORAL, 2.4, 1.15),
        ).arrange(DOWN, buff=.35).move_to([2.25, .15, 0])
        same = txt("=", 45, S_GOLD).move_to([0, -.05, 0])
        compare = VGroup(standard, blockwise, same)
        self.play(*[FadeOut(item) for item in final_state], FadeOut(flow_tiles),
                  FadeIn(compare), run_time=.85)
        self.keep_stage(compare)
        self.play(Indicate(standard[-1], color=O_CORAL, scale_factor=1.06),
                  Indicate(blockwise[-1], color=O_CORAL, scale_factor=1.06), run_time=.9)
        self.to(68)

        # 68–75 s: answer episode 1—the quadratic S and P need not be materialized.
        self.text(
            "거대한 중간 행렬을 완성할 필요가 없습니다",
            "Score S와 Attention P 전체를 HBM에 저장하지 않고도\ntile과 작은 상태만으로 같은 O를 만들 수 있습니다.",
            "no full S     ·     no full P     ·     same O",
        )
        s_matrix = MatrixGrid(6, 6, "Score  S", S_GOLD, .31).move_to([-2.55, .7, 0]).set_opacity(.22)
        p_matrix = MatrixGrid(6, 6, "Attention  P", P_VIOLET, .31).move_to([-.15, .7, 0]).set_opacity(.22)
        strike_s = Line(s_matrix.get_corner(UL), s_matrix.get_corner(DR), color=O_CORAL, stroke_width=4)
        strike_p = Line(p_matrix.get_corner(UL), p_matrix.get_corner(DR), color=O_CORAL, stroke_width=4)
        compact = VGroup(
            DataCard("tiles", "Kⱼ, Vⱼ", V_GREEN, 1.65, 1.05),
            txt("→", 29, MUTED),
            DataCard("m, ℓ, O", "state", S_GOLD, 1.9, 1.05),
            txt("→", 29, MUTED),
            DataCard("O", "same output", O_CORAL, 1.6, 1.05),
        ).arrange(RIGHT, buff=.18).move_to([1.2, -1.55, 0]).scale(.82)
        answer = VGroup(s_matrix, p_matrix, strike_s, strike_p, compact)
        self.play(*[FadeOut(item) for item in standard],
                  *[FadeOut(item) for item in blockwise], FadeOut(same),
                  FadeIn(s_matrix), FadeIn(p_matrix), Create(strike_s), Create(strike_p),
                  FadeIn(compact), run_time=1.0)
        self.keep_stage(answer)
        self.play(Indicate(compact[-1], color=O_CORAL, scale_factor=1.08), run_time=.75)
        self.to(75)

        # 75–80 s: return to the hardware question for the finale.
        self.text(
            "그렇다면 GPU에서는 왜 더 빠를까?",
            "마지막에는 HBM 왕복과 on-chip tile 계산을 나란히 놓고,\nFlashAttention이 실제로 줄인 것을 정리합니다.",
            "next  ·  FlashAttention은 무엇을 줄였을까?",
        )
        hbm_box = RoundedRectangle(width=2.7, height=1.55, corner_radius=.15,
                                   stroke_color=HBM_BLUE, fill_color=HBM_BLUE,
                                   fill_opacity=.08, stroke_width=2)
        hbm = VGroup(
            hbm_box,
            txt("HBM", 25, HBM_BLUE).move_to(hbm_box.get_center() + UP * .2),
            txt("large · far", 19, MUTED).move_to(hbm_box.get_center() + DOWN * .25),
        ).move_to([-2.35, .45, 0])
        onchip = VGroup(
            RoundedRectangle(width=2.6, height=1.55, corner_radius=.15,
                             stroke_color=V_GREEN, fill_color=V_GREEN,
                             fill_opacity=.08, stroke_width=2),
            txt("On-chip", 24, V_GREEN).move_to([0, .2, 0]),
            txt("tile compute", 19, MUTED).move_to([0, -.25, 0]),
        ).move_to([2.35, .45, 0])
        io = DoubleArrow(hbm.get_right(), onchip.get_left(), buff=.16,
                         color=S_GOLD, stroke_width=3, tip_length=.14)
        question = txt("IO ?", 31, S_GOLD).move_to([0, -1.25, 0])
        self.play(*[FadeOut(item) for item in answer], FadeIn(hbm), FadeIn(onchip),
                  GrowFromCenter(io), FadeIn(question), run_time=.9)
        self.keep_stage(hbm, onchip, io, question)
        self.play(Indicate(io, color=S_GOLD, scale_factor=1.05), run_time=.75)
        self.to(80)

    def state_panel(self, name, m_text, l_text, o_text, color):
        box = RoundedRectangle(
            width=2.7, height=2.55, corner_radius=.16,
            stroke_color=color, stroke_width=2,
            fill_color=color, fill_opacity=.07,
        )
        return VGroup(
            box,
            txt(name, 20, color).move_to(box.get_top() + DOWN * .3),
            txt(m_text, 27, INK).move_to(box.get_center() + UP * .43),
            txt(l_text, 26, INK).move_to(box.get_center() + DOWN * .13),
            txt(o_text, 27, O_CORAL).move_to(box.get_center() + DOWN * .72),
        )

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.18)
        self.head = txt(head, 30).move_to(UP * 5.15)
        self.note = txt(note, 23, S_GOLD).move_to(DOWN * 4.72)
        self.sub = txt(sub, 27).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.35)

    def keep_stage(self, *allowed):
        """Remove animation-promoted duplicates while preserving the current stage."""
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
            self.play(
                self.progress.animate.stretch_to_fit_width(width).move_to(
                    [-3.8 + width / 2, -7.35, 0]
                ),
                run_time=min(.28, remain),
            )
            self.wait(max(0, target - self.time))
