"""FlashAttention 03: online softmax with a running max and exponential sum."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.flash_series.visuals import (
    INK, K_PINK, MUTED, O_CORAL, P_VIOLET, Q_BLUE,
    S_GOLD, V_GREEN, DataCard, txt,
)


BLOCKS = ((1, 3, 2), (2, 5, 4), (0, 4, 1))
BLOCK_COLORS = (Q_BLUE, K_PINK, V_GREEN)


class ScoreBlock(VGroup):
    def __init__(self, values, name, color, **kwargs):
        super().__init__(**kwargs)
        cells = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=.9, height=.9, corner_radius=.1,
                stroke_color=color, stroke_width=1.8,
                fill_color=color, fill_opacity=.08,
            )
            cells.add(VGroup(box, txt(str(value), 29, color)))
        cells.arrange(RIGHT, buff=.12)
        label = txt(name, 21, color).next_to(cells, UP, buff=.18)
        self.cells = cells
        self.values = tuple(values)
        self.add(cells, label)


class OnlineSoftmax(Scene):
    DURATION = 78

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.add(
            txt("IO-AWARE ATTENTION  /  03", 20, MUTED).move_to(UP * 7.25),
            txt("전체를 저장하지 않고 Softmax할 수 있을까?", 33).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=S_GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s: recover the stable-softmax normalizer from episode 2's question.
        self.text(
            "분모에는 모든 score가 들어갑니다",
            "Softmax의 분모를 계산하려면 모든 score의\n지수값을 더해야 합니다.",
            "softmax(xᵢ) = exp(xᵢ − m) / ℓ",
        )
        scores = self.score_row((1, 3, 2, 2, 5, 4, 0, 4, 1), S_GOLD, .66)
        scores.move_to([0, 1.25, 0])
        m_def = DataCard("m = max(x)", "stability reference", P_VIOLET, 2.7, 1.15).move_to([-1.65, -.65, 0])
        l_def = DataCard("ℓ = Σ exp(x − m)", "denominator state", S_GOLD, 3.25, 1.15).move_to([1.65, -.65, 0])
        normalizer = VGroup(scores, m_def, l_def)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * .12) for cell in scores],
                              lag_ratio=.06), run_time=1.15)
        self.play(FadeIn(m_def), FadeIn(l_def), run_time=.7)
        self.play(Indicate(l_def, color=S_GOLD, scale_factor=1.06), run_time=.75)
        self.to(7)

        # 7–14 s: split the row into blocks; simultaneous storage is not required.
        self.text(
            "하지만 한꺼번에 기억할 필요는 없습니다",
            "score를 작은 블록으로 나누고\n하나씩 순서대로 살펴볼 수 있습니다.",
            "Block 1     →     Block 2     →     Block 3",
        )
        blocks = VGroup(*[
            ScoreBlock(values, f"Block {i + 1}", color)
            for i, (values, color) in enumerate(zip(BLOCKS, BLOCK_COLORS))
        ]).arrange(DOWN, buff=.65).move_to([0, .35, 0])
        order_arrows = VGroup(*[
            Arrow(blocks[i].get_bottom(), blocks[i + 1].get_top(), buff=.1,
                  color=MUTED, stroke_width=2, tip_length=.12)
            for i in range(2)
        ])
        self.play(FadeOut(normalizer),
                  LaggedStart(*[FadeIn(block, shift=RIGHT * .12) for block in blocks],
                              lag_ratio=.18), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in order_arrows], lag_ratio=.2), run_time=.6)
        self.to(14)

        # 14–22 s: initialize the state from block 1.
        self.text(
            "첫 블록에서 상태를 시작합니다",
            "첫 블록의 최댓값을 구하고, 그 값을 기준으로\n안정적인 지수합을 계산합니다.",
            "Block 1     ·     m₁ = 3     ·     ℓ₁ = 1.503",
        )
        block1 = ScoreBlock(BLOCKS[0], "Block 1", Q_BLUE).move_to([-1.9, .55, 0])
        block1[1].set_opacity(0)
        max_marker = self.max_marker(block1, 1, "current max 3", Q_BLUE)
        state1 = self.state_card("STATE 1", "m = 3", "ℓ = 1.503", Q_BLUE).move_to([2.15, .35, 0])
        calc1 = txt("e⁻² + e⁰ + e⁻¹ = 1.503", 25, S_GOLD).move_to([0, -1.8, 0])
        flow1 = Arrow(block1.get_right(), state1.get_left(), buff=.18,
                      color=Q_BLUE, stroke_width=3, tip_length=.15)
        self.play(FadeOut(blocks), FadeOut(order_arrows), FadeIn(block1), run_time=.65)
        self.play(FadeIn(max_marker), run_time=.55)
        self.play(GrowArrow(flow1), FadeIn(state1), FadeIn(calc1), run_time=.85)
        self.play(Indicate(state1, color=Q_BLUE, scale_factor=1.06), run_time=.7)
        self.to(22)

        # 22–31 s: block 2 reveals a larger maximum.
        self.text(
            "다음 블록에서 더 큰 값이 나타납니다",
            "두 번째 블록의 5는 지금까지의 3보다 큽니다.\n새로운 기준 최댓값은 5가 됩니다.",
            "m : 3     →     5",
        )
        block2 = ScoreBlock(BLOCKS[1], "Block 2", K_PINK).move_to([-1.9, .55, 0])
        block2[1].set_opacity(0)
        new_marker = self.max_marker(block2, 1, "new max 5", K_PINK)
        state_transition = VGroup(
            self.state_card("OLD", "m = 3", "ℓ = 1.503", Q_BLUE),
            txt("→", 36, MUTED),
            self.state_card("NEW", "m = 5", "ℓ = ?", K_PINK),
        ).arrange(RIGHT, buff=.25).scale(.82).move_to([1.25, -.85, 0])
        self.play(FadeOut(VGroup(block1, max_marker, state1, calc1, flow1)),
                  FadeIn(block2), FadeIn(new_marker), run_time=.75)
        self.play(FadeIn(state_transition), run_time=.7)
        self.play(Indicate(state_transition[-1], color=K_PINK, scale_factor=1.06), run_time=.75)
        self.to(31)

        # 31–42 s: rescale the old sum instead of revisiting old scores.
        self.text(
            "기존 합의 기준만 바꿉니다",
            "최댓값이 바뀌어도 처음부터 다시 계산하지 않습니다.\n이전 합을 새 기준에 맞게 작게 보정합니다.",
            "old contribution :  ℓ₁ × exp(m₁ − m₂)",
        )
        old_sum = DataCard("1.503", "old ℓ₁", Q_BLUE, 1.65, 1.15).move_to([-2.75, .75, 0])
        factor = DataCard("e³⁻⁵", "= 0.135", K_PINK, 1.65, 1.15).move_to([-.65, .75, 0])
        scaled = DataCard("0.203", "rescaled old", P_VIOLET, 1.85, 1.15).move_to([1.75, .75, 0])
        mult = txt("×", 34, MUTED).move_to([-1.7, .75, 0])
        equal = txt("=", 34, MUTED).move_to([.55, .75, 0])
        old_values = VGroup(old_sum, factor, scaled, mult, equal)
        old_block_ghost = ScoreBlock(BLOCKS[0], "Block 1 discarded", MUTED).scale(.65).move_to([0, -2.1, 0]).set_opacity(.2)
        strike = Line(old_block_ghost.get_corner(UL), old_block_ghost.get_corner(DR),
                      color=O_CORAL, stroke_width=4)
        self.play(FadeOut(VGroup(block2, new_marker, state_transition)), FadeIn(old_values),
                  run_time=.75)
        self.play(FadeIn(old_block_ghost), Create(strike), run_time=.6)
        self.play(Indicate(scaled, color=P_VIOLET, scale_factor=1.08), run_time=.75)
        self.to(42)

        # 42–51 s: add block 2's local contribution and keep only the updated state.
        self.text(
            "새 블록의 기여량을 더합니다",
            "새 기준으로 보정한 이전 합에, 두 번째 블록에서\n계산한 지수합을 더하면 됩니다.",
            "ℓ₂ = 1.503e³⁻⁵ + (e⁻³ + e⁰ + e⁻¹) = 1.621",
        )
        old_contrib = DataCard("0.203", "rescaled old", P_VIOLET, 1.9, 1.15).move_to([-2.65, .7, 0])
        new_contrib = DataCard("1.418", "Block 2", K_PINK, 1.9, 1.15).move_to([-.2, .7, 0])
        state2 = self.state_card("STATE 2", "m = 5", "ℓ = 1.621", S_GOLD).move_to([2.55, .5, 0])
        plus = txt("+", 34, MUTED).move_to([-1.42, .7, 0])
        equals = txt("=", 34, MUTED).move_to([1.1, .7, 0])
        updated = VGroup(old_contrib, new_contrib, state2, plus, equals)
        block2_small = ScoreBlock(BLOCKS[1], "Block 2", K_PINK).scale(.7).move_to([0, -1.8, 0])
        self.play(*[FadeOut(item) for item in old_values], FadeOut(old_block_ghost),
                  FadeOut(strike), FadeIn(updated),
                  FadeIn(block2_small), run_time=.8)
        self.remove(old_values, *list(old_values), old_block_ghost, strike)
        self.play(Indicate(state2, color=S_GOLD, scale_factor=1.07), run_time=.75)
        self.play(FadeOut(block2_small, shift=LEFT * .25), run_time=.55)
        self.to(51)

        # 51–59 s: repeat with block 3; blocks disappear but m and l remain.
        self.text(
            "지나간 score는 버려도 됩니다",
            "세 번째 블록까지 같은 갱신을 반복하면, 숫자들은\n사라지고 현재 최댓값과 누적 지수합만 남습니다.",
            "Block 3 passes     ·     STATE remains",
        )
        block3 = ScoreBlock(BLOCKS[2], "Block 3", V_GREEN).move_to([-2.1, .55, 0])
        state3 = self.state_card("FINAL STATE", "m = 5", "ℓ = 2.014", V_GREEN).move_to([2.25, .35, 0])
        update_arrow = Arrow(block3.get_right(), state3.get_left(), buff=.15,
                             color=V_GREEN, stroke_width=3, tip_length=.15)
        keep_m = txt("max stays 5", 23, V_GREEN).move_to([-2.1, -1.05, 0])
        self.play(*[FadeOut(item) for item in updated], FadeIn(block3), FadeIn(keep_m),
                  run_time=.65)
        self.remove(updated, *list(updated), block2_small)
        self.play(GrowArrow(update_arrow), FadeIn(state3), run_time=.75)
        self.play(FadeOut(block3, shift=LEFT * .3), FadeOut(keep_m),
                  Indicate(state3, color=V_GREEN, scale_factor=1.08), run_time=.85)
        self.to(59)

        # 59–67 s: full and block-wise accumulation agree numerically.
        self.text(
            "한꺼번에 계산한 결과와 같습니다",
            "모든 score를 한 번에 본 경우와 블록을 순서대로\n본 경우의 마지막 최댓값과 지수합은 같습니다.",
            "Full scan     =     Block-wise scan",
        )
        full = VGroup(
            txt("FULL", 22, Q_BLUE),
            self.score_row((1, 3, 2, 2, 5, 4, 0, 4, 1), Q_BLUE, .38),
            self.state_card("RESULT", "m = 5", "ℓ = 2.014", Q_BLUE).scale(.82),
        ).arrange(DOWN, buff=.35).move_to([-2.25, .25, 0])
        online = VGroup(
            txt("BLOCK-WISE", 22, V_GREEN),
            VGroup(*[
                self.tile_token(f"B{i + 1}", color)
                for i, color in enumerate(BLOCK_COLORS)
            ]).arrange(RIGHT, buff=.16),
            self.state_card("RESULT", "m = 5", "ℓ = 2.014", V_GREEN).scale(.82),
        ).arrange(DOWN, buff=.35).move_to([2.25, .25, 0])
        same = txt("=", 45, S_GOLD).move_to([0, -.15, 0])
        comparison = VGroup(full, online, same)
        self.play(*[FadeOut(item) for item in state3], FadeOut(update_arrow),
                  FadeIn(comparison), run_time=.85)
        self.remove(state3, *list(state3), update_arrow)
        self.play(Indicate(full[-1], color=S_GOLD, scale_factor=1.05),
                  Indicate(online[-1], color=S_GOLD, scale_factor=1.05), run_time=.9)
        self.to(67)

        # 67–73 s: collapse the score inventory into the compact sufficient state.
        self.text(
            "전체 score 대신 작은 상태만 남습니다",
            "Softmax에 필요한 정보는 전체 score 목록이 아니라\n현재의 m과 ℓ로 계속 누적할 수 있습니다.",
            "many scores     →     two running values",
        )
        long_row = self.score_row((1, 3, 2, 2, 5, 4, 0, 4, 1), MUTED, .62).move_to([0, 1.25, 0])
        compact = VGroup(
            DataCard("m = 5", "running max", P_VIOLET, 2.35, 1.2),
            DataCard("ℓ = 2.014", "running exp sum", S_GOLD, 2.65, 1.2),
        ).arrange(RIGHT, buff=.45).move_to([0, -.75, 0])
        collapse_arrows = VGroup(*[
            Arrow(cell.get_bottom(), compact.get_top(), buff=.18, color=MUTED,
                  stroke_width=1.5, tip_length=.1)
            for cell in long_row
        ])
        self.play(*[FadeOut(item) for item in full], *[FadeOut(item) for item in online],
                  FadeOut(same), FadeIn(long_row), FadeIn(collapse_arrows), run_time=.7)
        self.remove(comparison, full, online, *list(full), *list(online), same)
        self.play(FadeIn(compact), long_row.animate.set_opacity(.1),
                  collapse_arrows.animate.set_opacity(.08), run_time=.9)
        self.play(Indicate(compact, color=S_GOLD, scale_factor=1.04), run_time=.65)
        self.to(73)

        # 73–78 s: pass the output-state recurrence to episode 4.
        self.text(
            "이 상태로 Attention output도 갱신할 수 있을까?",
            "다음에는 m과 ℓ 옆에 output state O를 더해\nAttention 결과까지 tile마다 갱신해 보겠습니다.",
            "next  ·  m, ℓ, O를 함께 갱신하기",
        )
        m_token = DataCard("m", "running max", P_VIOLET, 1.55, 1.05)
        l_token = DataCard("ℓ", "running sum", S_GOLD, 1.55, 1.05)
        o_token = DataCard("O", "output state", O_CORAL, 1.8, 1.05)
        question = txt("?", 46, INK)
        finale = VGroup(m_token, l_token, txt("+", 34, MUTED), o_token, question)
        finale.arrange(RIGHT, buff=.28).move_to([0, .35, 0])
        self.play(FadeOut(long_row), FadeOut(collapse_arrows),
                  *[FadeOut(item) for item in compact], FadeIn(finale),
                  run_time=.8)
        self.remove(long_row, collapse_arrows, compact, *list(compact))
        self.play(Indicate(o_token, color=O_CORAL, scale_factor=1.1), run_time=.8)
        self.to(78)

    def score_row(self, values, color, cell_width):
        row = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=cell_width, height=.72, corner_radius=.08,
                stroke_color=color, stroke_width=1.5,
                fill_color=color, fill_opacity=.07,
            )
            row.add(VGroup(box, txt(str(value), 23, color)))
        row.arrange(RIGHT, buff=.08)
        return row

    def state_card(self, name, m_text, l_text, color):
        box = RoundedRectangle(
            width=2.65, height=2.0, corner_radius=.16,
            stroke_color=color, stroke_width=2,
            fill_color=color, fill_opacity=.07,
        )
        return VGroup(
            box,
            txt(name, 20, color).move_to(box.get_top() + DOWN * .32),
            txt(m_text, 28, INK).move_to(box.get_center() + UP * .15),
            txt(l_text, 27, INK).move_to(box.get_center() + DOWN * .45),
        )

    def max_marker(self, block, index, label, color):
        cell = block.cells[index]
        arrow = Arrow(cell.get_top() + UP * .7, cell.get_top(), buff=.08,
                      color=color, stroke_width=3, tip_length=.15)
        text = txt(label, 22, color).next_to(arrow, UP, buff=.08)
        return VGroup(arrow, text)

    def tile_token(self, label, color):
        box = RoundedRectangle(
            width=.85, height=.68, corner_radius=.1,
            stroke_color=color, stroke_width=1.8,
            fill_color=color, fill_opacity=.1,
        )
        return VGroup(box, txt(label, 20, color))

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
