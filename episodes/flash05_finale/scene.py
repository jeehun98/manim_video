"""FlashAttention 05 finale: same attention, different execution and IO."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.flash_series.visuals import (
    HBM_BLUE, INK, K_PINK, MUTED, O_CORAL, P_VIOLET, Q_BLUE,
    S_GOLD, V_GREEN, DataCard, MatrixGrid, txt,
)


class FlashAttentionFinale(Scene):
    DURATION = 84

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("IO-AWARE ATTENTION  /  05  ·  FINALE", 20, MUTED).move_to(UP * 7.25),
            txt("FlashAttention은 무엇을 바꾼 걸까?", 34).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=S_GOLD,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s: both algorithms receive exactly the same Q, K, V.
        self.text(
            "두 방식은 같은 입력에서 시작합니다",
            "Standard Attention과 FlashAttention은 모두\n같은 Query, Key, Value를 입력으로 받습니다.",
            "same Q, K, V     ·     same Attention",
        )
        self.lanes = self.lane_frame()
        left_inputs = self.input_set().move_to([-2.25, .55, 0])
        right_inputs = self.input_set().move_to([2.25, .55, 0])
        inputs = VGroup(left_inputs, right_inputs)
        self.play(FadeIn(self.lanes),
                  LaggedStart(*[FadeIn(card, shift=UP * .12)
                                for group in inputs for card in group], lag_ratio=.08),
                  run_time=1.2)
        self.play(Indicate(left_inputs, color=S_GOLD, scale_factor=1.03),
                  Indicate(right_inputs, color=S_GOLD, scale_factor=1.03), run_time=.75)
        self.to(7)

        # 7–15 s: the standard path materializes S and P before multiplying V.
        self.text(
            "Standard Attention은 전체 행렬을 만듭니다",
            "먼저 전체 Score S를 만들고, Softmax를 적용해\n전체 Attention weight P를 계산합니다.",
            "QKᵀ  →  S  →  softmax  →  P  →  PV",
        )
        standard_chain = self.standard_chain().move_to([-2.25, .25, 0])
        right_wait = VGroup(
            self.tile_icon("Q tile", Q_BLUE),
            self.tile_icon("K tile", K_PINK),
            self.tile_icon("V tile", V_GREEN),
        ).arrange(DOWN, buff=.28).move_to([2.25, .4, 0]).set_opacity(.25)
        stage_standard = VGroup(standard_chain, right_wait)
        self.play(*[FadeOut(card) for group in inputs for card in group],
                  LaggedStart(*[FadeIn(item, shift=DOWN * .1) for item in standard_chain],
                              lag_ratio=.08), FadeIn(right_wait), run_time=1.05)
        self.keep_stage(self.lanes, stage_standard)
        self.play(Indicate(standard_chain[2], color=S_GOLD, scale_factor=1.06),
                  Indicate(standard_chain[6], color=P_VIOLET, scale_factor=1.06), run_time=.8)
        self.to(15)

        # 15–23 s: S and P cross the HBM boundary as large intermediates.
        self.text(
            "큰 중간 결과를 쓰고, 다시 읽습니다",
            "S와 P는 큰 중간 결과로 materialize되고, HBM에\n기록됐다가 다음 연산을 위해 다시 읽힙니다.",
            "N × N S, P     ·     HBM WRITE / READ",
        )
        compute = VGroup(
            DataCard("QKᵀ", "compute", Q_BLUE, 1.35, .85),
            DataCard("softmax", "compute", P_VIOLET, 1.5, .85),
            DataCard("×V", "compute", V_GREEN, 1.25, .85),
        ).arrange(RIGHT, buff=.2).scale(.78).move_to([-2.25, 1.55, 0])
        hbm_box = self.hbm_box(3.65, 1.65).move_to([-2.25, -.9, 0])
        s_token = self.tile_icon("S · N×N", S_GOLD, 1.15, .68).move_to([-2.85, -1.12, 0])
        p_token = self.tile_icon("P · N×N", P_VIOLET, 1.15, .68).move_to([-1.65, -1.12, 0])
        io_arrows = VGroup(
            Arrow(compute[0].get_bottom(), s_token.get_top(), buff=.08,
                  color=S_GOLD, stroke_width=2, tip_length=.12),
            Arrow(s_token.get_top(), compute[1].get_bottom(), buff=.08,
                  color=S_GOLD, stroke_width=2, tip_length=.12),
            Arrow(compute[1].get_bottom(), p_token.get_top(), buff=.08,
                  color=P_VIOLET, stroke_width=2, tip_length=.12),
            Arrow(p_token.get_top(), compute[2].get_bottom(), buff=.08,
                  color=P_VIOLET, stroke_width=2, tip_length=.12),
        )
        io_labels = VGroup(
            txt("W", 16, S_GOLD).next_to(io_arrows[0], LEFT, buff=.03),
            txt("R", 16, S_GOLD).next_to(io_arrows[1], RIGHT, buff=.03),
            txt("W", 16, P_VIOLET).next_to(io_arrows[2], LEFT, buff=.03),
            txt("R", 16, P_VIOLET).next_to(io_arrows[3], RIGHT, buff=.03),
        )
        left_io = VGroup(compute, hbm_box, s_token, p_token, io_arrows, io_labels)
        self.play(*[FadeOut(item) for item in stage_standard], FadeIn(compute),
                  FadeIn(hbm_box), FadeIn(s_token), FadeIn(p_token),
                  LaggedStart(*[GrowArrow(a) for a in io_arrows], lag_ratio=.12),
                  FadeIn(io_labels), run_time=1.15)
        self.keep_stage(self.lanes, left_io)
        self.play(Indicate(io_arrows, color=O_CORAL, scale_factor=1.03), run_time=.75)
        self.to(23)

        # 23–31 s: the right lane tiles the same Q, K, V.
        self.text(
            "FlashAttention은 같은 계산을 tile로 나눕니다",
            "같은 Q, K, V를 작은 블록으로 나누고\n필요한 tile만 on-chip memory로 가져옵니다.",
            "Qᵢ, Kⱼ, Vⱼ     →     on-chip working set",
        )
        tiled_inputs = VGroup(
            self.tiled_column("Q", Q_BLUE),
            self.tiled_column("K", K_PINK),
            self.tiled_column("V", V_GREEN),
        ).arrange(RIGHT, buff=.35).move_to([2.25, 1.1, 0])
        onchip = self.onchip_box(3.75, 1.65).move_to([2.25, -1.0, 0])
        selected = VGroup(
            self.tile_icon("Qᵢ", Q_BLUE),
            self.tile_icon("Kⱼ", K_PINK),
            self.tile_icon("Vⱼ", V_GREEN),
        ).arrange(RIGHT, buff=.12).move_to(onchip.get_center() + DOWN * .18)
        transfer = VGroup(*[
            Arrow(tiled_inputs[i].get_bottom(), selected[i].get_top(), buff=.1,
                  color=COLORS[i], stroke_width=2, tip_length=.11)
            for i in range(3)
        ])
        flash_tiles = VGroup(tiled_inputs, onchip, selected, transfer)
        self.play(left_io.animate.set_opacity(.22), FadeIn(tiled_inputs), FadeIn(onchip),
                  FadeIn(selected), LaggedStart(*[GrowArrow(a) for a in transfer], lag_ratio=.12),
                  run_time=1.05)
        self.keep_stage(self.lanes, left_io, flash_tiles)
        self.play(Indicate(selected, color=S_GOLD, scale_factor=1.05), run_time=.75)
        self.to(31)

        # 31–39 s: update only local score and the compact m,l,O state.
        self.text(
            "각 tile에서 작은 상태를 갱신합니다",
            "local score를 계산하고 현재 최댓값 m, 지수합 ℓ,\nAttention output O를 다음 상태로 갱신합니다.",
            "local score     →     update m, ℓ, O",
        )
        local_score = self.tile_icon("local score", S_GOLD, 1.55, .82).move_to([1.25, .65, 0])
        state = self.state_panel().move_to([3.0, .35, 0])
        state_arrow = Arrow(local_score.get_right(), state.get_left(), buff=.12,
                            color=S_GOLD, stroke_width=2.5, tip_length=.13)
        next_tile = self.tile_icon("next Kⱼ,Vⱼ", V_GREEN, 1.55, .75).move_to([2.15, -1.65, 0])
        loop_arrow = CurvedArrow(next_tile.get_right(), state.get_bottom(), angle=TAU / 4,
                                 color=V_GREEN, stroke_width=2, tip_length=.12)
        flash_state = VGroup(local_score, state, state_arrow, next_tile, loop_arrow)
        self.play(*[FadeOut(item) for item in flash_tiles], FadeIn(local_score),
                  GrowArrow(state_arrow), FadeIn(state), FadeIn(next_tile),
                  Create(loop_arrow), run_time=1.0)
        self.keep_stage(self.lanes, left_io, flash_state)
        self.play(Indicate(state, color=S_GOLD, scale_factor=1.05), run_time=.75)
        self.to(39)

        # 39–47 s: the local score is visibly discarded before the next tile.
        self.text(
            "사용한 local intermediate는 바로 버립니다",
            "현재 tile의 score와 weight는 상태를 갱신한 뒤\n다음 tile로 넘어가기 전에 제거할 수 있습니다.",
            "create     →     use     →     discard",
        )
        discard = VGroup(
            self.tile_icon("score tile", S_GOLD, 1.45, .8),
            txt("→", 27, MUTED),
            self.tile_icon("use with Vⱼ", V_GREEN, 1.55, .8),
            txt("→", 27, MUTED),
            self.tile_icon("discard", O_CORAL, 1.4, .8),
        ).arrange(RIGHT, buff=.12).scale(.78).move_to([2.25, -.95, 0])
        survivor = self.state_panel().scale(.86).move_to([2.25, 1.15, 0])
        flash_discard = VGroup(discard, survivor)
        self.play(*[FadeOut(item) for item in flash_state], FadeIn(discard),
                  FadeIn(survivor), run_time=.9)
        self.keep_stage(self.lanes, left_io, flash_discard)
        self.play(discard[-1].animate.set_opacity(.1),
                  Indicate(survivor, color=V_GREEN, scale_factor=1.04), run_time=.85)
        self.to(47)

        # 47–55 s: compare the large materialized intermediates to compact state.
        self.text(
            "차이는 무엇을 HBM에 남기는가입니다",
            "왼쪽은 전체 S와 P를 HBM에 남기지만, 오른쪽은\n지나간 tile 대신 작은 m, ℓ, O 상태만 유지합니다.",
            "full N × N intermediates     vs     compact running state",
        )
        left_large = VGroup(
            MatrixGrid(5, 5, "Score S", S_GOLD, .27),
            MatrixGrid(5, 5, "Attention P", P_VIOLET, .27),
        ).arrange(DOWN, buff=.55).move_to([-2.25, .3, 0])
        right_small = self.state_panel().move_to([2.25, .35, 0])
        memory_tags = VGroup(
            txt("HBM materialization", 20, O_CORAL).move_to([-2.25, -2.1, 0]),
            txt("on-chip state", 20, V_GREEN).move_to([2.25, -1.4, 0]),
        )
        contrast = VGroup(left_large, right_small, memory_tags)
        self.play(*[FadeOut(item) for item in left_io],
                  *[FadeOut(item) for item in flash_discard], FadeIn(left_large),
                  FadeIn(right_small), FadeIn(memory_tags), run_time=1.0)
        self.keep_stage(self.lanes, contrast)
        self.play(Indicate(left_large, color=O_CORAL, scale_factor=1.025),
                  Indicate(right_small, color=V_GREEN, scale_factor=1.05), run_time=.85)
        self.to(55)

        # 55–63 s: merge the two exact outputs at the center.
        self.text(
            "계산 경로는 달라도 최종 출력은 같습니다",
            "저장 방식과 계산 순서는 다르지만 두 경로가 만드는\nAttention output은 정확히 같습니다.",
            "O_standard     =     O_flash",
        )
        o_standard = DataCard("O", "standard · 5.741", O_CORAL, 2.05, 1.25).move_to([-2.25, .35, 0])
        o_flash = DataCard("O", "flash · 5.741", O_CORAL, 2.05, 1.25).move_to([2.25, .35, 0])
        equals = txt("=", 44, S_GOLD).move_to([0, .35, 0]).set_opacity(0)
        exact = txt("exact Attention", 25, V_GREEN).move_to([0, -1.25, 0]).set_opacity(0)
        outputs = VGroup(o_standard, o_flash, equals, exact)
        self.play(*[FadeOut(item) for item in contrast], FadeIn(o_standard), FadeIn(o_flash),
                  run_time=.75)
        self.keep_stage(self.lanes, outputs)
        self.play(o_standard.animate.move_to([-.95, .35, 0]),
                  o_flash.animate.move_to([.95, .35, 0]),
                  equals.animate.set_opacity(1), exact.animate.set_opacity(1), run_time=1.15)
        self.play(Indicate(VGroup(o_standard, o_flash), color=O_CORAL, scale_factor=1.04),
                  run_time=.75)
        self.to(63)

        # 63–71 s: make the cost distinction explicit—same math, less HBM traffic.
        self.text(
            "핵심은 FLOPs보다 Memory IO입니다",
            "FlashAttention의 핵심은 계산을 근사하거나 답을 바꾸는 것이\n아니라 HBM과 on-chip 사이의 데이터 이동을 줄이는 것입니다.",
            "same math     ·     HBM READ / WRITE ↓",
        )
        same_math = DataCard("FLOPs", "same Attention math", Q_BLUE, 2.65, 1.35).move_to([-2.35, .65, 0])
        io_down = DataCard("HBM IO ↓", "fewer large transfers", S_GOLD, 2.9, 1.35).move_to([2.15, .65, 0])
        not_equal = txt("≠ the main story", 23, MUTED).move_to([-2.35, -1.0, 0])
        io_aware = txt("IO-aware execution", 27, S_GOLD).move_to([2.15, -1.0, 0])
        cost = VGroup(same_math, io_down, not_equal, io_aware)
        self.play(*[FadeOut(item) for item in outputs], FadeOut(self.lanes), FadeIn(cost),
                  run_time=.85)
        self.keep_stage(cost)
        self.play(Indicate(io_down, color=S_GOLD, scale_factor=1.08), run_time=.85)
        self.to(71)

        # 71–78 s: summarize the paper's systems lesson.
        self.text(
            "같은 수학도 실행 구조를 다시 설계할 수 있습니다",
            "수식이 같아도 하드웨어의 메모리 계층을 고려해 계산 순서와\n저장 방식을 바꾸면 실제 실행 비용은 달라질 수 있습니다.",
            "equation     →     algorithm     →     memory hierarchy",
        )
        layers = VGroup(
            DataCard("Attention", "same equation", Q_BLUE, 2.15, 1.2),
            txt("→", 30, MUTED),
            DataCard("Tiled algorithm", "new order", V_GREEN, 2.5, 1.2),
            txt("→", 30, MUTED),
            DataCard("Memory IO", "lower traffic", S_GOLD, 2.25, 1.2),
        ).arrange(RIGHT, buff=.18).scale(.87).move_to([0, .45, 0])
        lesson = VGroup(layers, txt("IO-awareness", 29, S_GOLD).move_to([0, -1.35, 0]))
        self.play(*[FadeOut(item) for item in cost], FadeIn(lesson), run_time=.85)
        self.keep_stage(lesson)
        self.play(LaggedStart(*[Indicate(layers[i], scale_factor=1.04)
                                for i in (0, 2, 4)], lag_ratio=.2), run_time=1.0)
        self.to(78)

        # 78–84 s: final line—same answer, different way of computing it.
        self.text(
            "같은 답을 계산해도, 계산하는 방법은 같지 않습니다",
            "FlashAttention은 같은 Attention을 더 적은 데이터 이동으로\n실행하도록 계산 순서와 저장 방식을 바꿨습니다.",
            "same answer     ·     different execution",
        )
        final_o = DataCard("O", "exact same output", O_CORAL, 2.25, 1.35).move_to([0, .3, 0])
        paths = VGroup(
            CurvedArrow([-3.1, 2.0, 0], final_o.get_left(), angle=-TAU / 8,
                        color=Q_BLUE, stroke_width=2.5, tip_length=.13),
            CurvedArrow([3.1, 2.0, 0], final_o.get_right(), angle=TAU / 8,
                        color=V_GREEN, stroke_width=2.5, tip_length=.13),
            txt("materialize S, P", 21, Q_BLUE).move_to([-2.55, 2.35, 0]),
            txt("tile + m, ℓ, O", 21, V_GREEN).move_to([2.55, 2.35, 0]),
        )
        finale = VGroup(final_o, paths)
        self.play(*[FadeOut(item) for item in lesson], FadeIn(final_o), Create(paths[:2]),
                  FadeIn(paths[2:]), run_time=1.0)
        self.keep_stage(finale)
        self.play(Indicate(final_o, color=O_CORAL, scale_factor=1.08), run_time=.8)
        self.to(84)

    def lane_frame(self):
        return VGroup(
            Line([0, 4.55, 0], [0, -3.75, 0], color=MUTED, stroke_opacity=.24),
            txt("STANDARD", 21, Q_BLUE).move_to([-2.25, 4.25, 0]),
            txt("FLASH", 21, V_GREEN).move_to([2.25, 4.25, 0]),
        )

    def input_set(self):
        return VGroup(
            self.tile_icon("Q", Q_BLUE),
            self.tile_icon("K", K_PINK),
            self.tile_icon("V", V_GREEN),
        ).arrange(RIGHT, buff=.16)

    def standard_chain(self):
        return VGroup(
            self.tile_icon("QKᵀ", Q_BLUE, 1.2, .7), txt("↓", 23, MUTED),
            self.tile_icon("S", S_GOLD, 1.1, .7), txt("↓", 23, MUTED),
            self.tile_icon("softmax", P_VIOLET, 1.45, .7), txt("↓", 23, MUTED),
            self.tile_icon("P", P_VIOLET, 1.1, .7), txt("↓", 23, MUTED),
            self.tile_icon("×V → O", O_CORAL, 1.45, .7),
        ).arrange(DOWN, buff=.13).scale(.86)

    def tile_icon(self, label, color, width=1.0, height=.72):
        box = RoundedRectangle(width=width, height=height, corner_radius=.1,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.1)
        return VGroup(box, txt(label, 20, color, width - .12))

    def hbm_box(self, width, height):
        box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                               stroke_color=HBM_BLUE, stroke_width=2,
                               fill_color=HBM_BLUE, fill_opacity=.08)
        return VGroup(
            box,
            txt("HBM", 22, HBM_BLUE).move_to(box.get_top() + DOWN * .28),
            txt("materialized intermediates", 16, MUTED).move_to(box.get_top() + DOWN * .6),
        )

    def onchip_box(self, width, height):
        box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                               stroke_color=V_GREEN, stroke_width=2,
                               fill_color=V_GREEN, fill_opacity=.08)
        return VGroup(
            box,
            txt("On-chip working set", 21, V_GREEN).move_to(box.get_top() + DOWN * .28),
            txt("small · reusable", 17, MUTED).move_to(box.get_top() + DOWN * .6),
        )

    def tiled_column(self, name, color):
        tiles = VGroup(*[self.tile_icon(f"{name}{i + 1}", color, .8, .55)
                         for i in range(3)]).arrange(DOWN, buff=.08)
        return VGroup(tiles, txt(name, 20, color).next_to(tiles, UP, buff=.12))

    def state_panel(self):
        box = RoundedRectangle(width=2.35, height=2.25, corner_radius=.15,
                               stroke_color=V_GREEN, stroke_width=2,
                               fill_color=V_GREEN, fill_opacity=.07)
        return VGroup(
            box,
            txt("RUNNING STATE", 18, V_GREEN).move_to(box.get_top() + DOWN * .28),
            txt("m", 29, P_VIOLET).move_to(box.get_center() + UP * .38),
            txt("ℓ", 29, S_GOLD).move_to(box.get_center()),
            txt("O", 29, O_CORAL).move_to(box.get_center() + DOWN * .43),
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


COLORS = (Q_BLUE, K_PINK, V_GREEN)

