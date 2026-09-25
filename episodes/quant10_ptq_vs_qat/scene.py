"""Quantization 10: Post-Training Quantization versus QAT."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class PTQvsQAT(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  10", 20, MUTED).move_to(UP * 7.25),
            txt("Quantization은 언제 적용해야 할까?", 31).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–8 s — one trained model, two different timings.
        self.text(
            "같은 Quantization도 적용 시점이 다릅니다",
            "학습이 끝난 모델을 나중에 줄일 수도 있고, 학습 중부터\nQuantization 오차를 경험하게 만들 수도 있습니다.",
            "AFTER TRAINING  ·  PTQ             DURING TRAINING  ·  QAT",
        )
        model = self.model_card("TRAINED\nFP MODEL", VALUE).move_to([0, 1.55, 0])
        ptq = self.branch_card("PTQ", "학습 완료 후", SNAP).move_to([-2.05, -.75, 0])
        qat = self.branch_card("QAT", "학습 중 고려", GRID).move_to([2.05, -.75, 0])
        branches = VGroup(
            Arrow(model.get_bottom(), ptq.get_top(), buff=.12,
                  color=SNAP, stroke_width=2.6, tip_length=.12),
            Arrow(model.get_bottom(), qat.get_top(), buff=.12,
                  color=GRID, stroke_width=2.6, tip_length=.12),
        )
        hook = VGroup(model, ptq, qat, branches)
        self.play(FadeIn(model, scale=.9), run_time=.45)
        self.play(GrowArrow(branches[0]), FadeIn(ptq),
                  GrowArrow(branches[1]), FadeIn(qat), run_time=.75)
        self.keep_stage(hook)
        self.play(Indicate(ptq, color=SNAP, scale_factor=1.05),
                  Indicate(qat, color=GRID, scale_factor=1.05), run_time=.75)
        self.to(8)

        # 8–17 s — PTQ transforms a completed model without full retraining.
        self.text(
            "PTQ는 완성된 모델을 나중에 Quantize합니다",
            "Post-Training Quantization은 이미 학습된 FP 모델을 받아\n전체 학습을 처음부터 다시 하지 않고 INT 모델로 변환합니다.",
            "TRAINED FP MODEL  →  QUANTIZATION  →  INT8 / INT4 MODEL",
        )
        ptq_flow = VGroup(
            self.process_box("TRAINED\nFP MODEL", VALUE, 1.8),
            self.process_box("QUANTIZE", SNAP, 1.65),
            self.process_box("INT8 / INT4\nMODEL", GOOD, 1.95),
        ).arrange(RIGHT, buff=.65).move_to([0, .35, 0])
        arrows = VGroup(*[
            Arrow(ptq_flow[i].get_right(), ptq_flow[i + 1].get_left(), buff=.08,
                  color=MUTED, stroke_width=2.6, tip_length=.12)
            for i in range(2)
        ])
        no_retrain = pill("NO FULL RETRAINING", GOOD, 3.2).move_to([0, -1.45, 0])
        ptq_stage = VGroup(ptq_flow, arrows, no_retrain)
        self.play(FadeOut(hook), FadeIn(ptq_flow[0]), run_time=.45)
        for i in range(2):
            self.play(GrowArrow(arrows[i]), FadeIn(ptq_flow[i + 1]), run_time=.5)
        self.play(FadeIn(no_retrain, shift=UP * .08), run_time=.4)
        self.keep_stage(ptq_stage)
        self.play(Indicate(ptq_flow[-1], color=GOOD, scale_factor=1.06), run_time=.7)
        self.to(17)

        # 17–27 s — PTQ introduces an error the original training never saw.
        self.text(
            "PTQ 모델은 이 오차를 학습 중 경험하지 못했습니다",
            "원래 값이 가장 가까운 격자로 이동하면 작은 차이가 생기지만,\n완료된 학습은 그 Quantization Error를 고려하지 않았습니다.",
            "trained in FP space          quantization error appears afterward",
        )
        axis = Line([-3.2, .15, 0], [3.2, .15, 0], color=MUTED, stroke_width=2.5)
        ticks = VGroup(*[
            Line(UP * .28, DOWN * .28, color=GRID, stroke_width=3)
            .move_to(axis.point_from_proportion(i / 5)) for i in range(6)
        ])
        props = (.08, .27, .43, .69, .88)
        targets = (.0, .2, .4, .6, 1.0)
        dots = VGroup(*[
            Dot(axis.point_from_proportion(p) + UP * (.9 + .25 * (i % 2)),
                radius=.105, color=VALUE) for i, p in enumerate(props)
        ])
        ghosts = dots.copy().set_opacity(.22)
        move_arrows = VGroup(*[
            Arrow(dots[i].get_bottom(), axis.point_from_proportion(targets[i]) + UP * .1,
                  buff=.05, color=ERROR, stroke_width=1.8, tip_length=.08)
            for i in range(len(dots))
        ])
        unseen = VGroup(
            pill("FP TRAINING", VALUE, 1.9), txt("→", 25, MUTED),
            pill("NEW ERROR", ERROR, 1.8),
        ).arrange(RIGHT, buff=.25).move_to([0, -1.45, 0])
        error_stage = VGroup(axis, ticks, dots, ghosts, move_arrows, unseen)
        self.play(FadeOut(ptq_stage), Create(axis), FadeIn(ticks), FadeIn(dots),
                  run_time=.65)
        self.add(ghosts)
        self.play(LaggedStart(*[GrowArrow(a) for a in move_arrows], lag_ratio=.08),
                  *[dots[i].animate.move_to(axis.point_from_proportion(targets[i]))
                    for i in range(len(dots))], run_time=.9)
        self.play(FadeIn(unseen), run_time=.45)
        self.keep_stage(error_stage)
        self.play(Indicate(ghosts, color=ERROR, scale_factor=1.04), run_time=.7)
        self.to(27)

        # 27–39 s — QAT places simulated quantization in the forward loop.
        self.text(
            "QAT는 학습 루프 안에 Quantization 효과를 넣습니다",
            "FP weight를 fake quantization해 forward에서 오차를 경험하고,\n그 결과의 loss를 이용해 학습 가능한 FP weight를 업데이트합니다.",
            "FP WEIGHT → FAKE QUANT → FORWARD → LOSS → BACKWARD → UPDATE",
        )
        nodes = VGroup(
            self.loop_box("FP\nWEIGHT", VALUE),
            self.loop_box("FAKE\nQUANT", SNAP),
            self.loop_box("FORWARD", GRID),
            self.loop_box("LOSS", ERROR),
            self.loop_box("BACKWARD", GRID),
            self.loop_box("UPDATE\nFP W", GOOD),
        ).arrange_in_grid(rows=2, cols=3, buff=(.48, .58)).move_to([0, .35, 0])
        # Explicit route: top row left-to-right, then bottom row right-to-left.
        route_pairs = ((0, 1), (1, 2), (2, 5), (5, 4), (4, 3), (3, 0))
        loop_arrows = VGroup(*[
            self.routed_arrow(nodes[a], nodes[b], i) for i, (a, b) in enumerate(route_pairs)
        ])
        forward_tag = pill("QUANTIZATION ERROR IS IN THE FORWARD PASS", SNAP, 5.25)
        forward_tag.move_to([0, -2.05, 0])
        qat_loop = VGroup(nodes, loop_arrows, forward_tag)
        self.play(FadeOut(error_stage), FadeIn(nodes), run_time=.7)
        self.play(LaggedStart(*[Create(a) for a in loop_arrows], lag_ratio=.08),
                  run_time=.95)
        self.play(FadeIn(forward_tag, shift=UP * .08), run_time=.4)
        self.keep_stage(qat_loop)
        self.play(Indicate(nodes[1], color=SNAP, scale_factor=1.08),
                  Indicate(nodes[5], color=GOOD, scale_factor=1.08), run_time=.75)
        self.to(39)

        # 39–49 s — training can reposition FP weights around the fixed grid.
        self.text(
            "모델은 오차가 있는 환경에 맞춰 Weight를 조정합니다",
            "Quantization Error를 없애는 것이 아니라 그 오차가 있어도\nloss가 작아지도록 FP weight의 위치를 조금씩 바꿉니다.",
            "repeat: quantize → measure loss → update FP weights → quantize again",
        )
        before = self.adaptation_row("초기 FP weights", (.10, .31, .56, .82), VALUE)
        after = self.adaptation_row("QAT 후 FP weights", (.18, .39, .61, .79), GOOD)
        rows = VGroup(before, after).arrange(DOWN, buff=1.0).move_to([0, .25, 0])
        down_arrows = VGroup(*[
            Arrow(before[2][i].get_center(), after[2][i].get_center(), buff=.14,
                  color=GOOD, stroke_width=1.8, tip_length=.08)
            for i in range(4)
        ])
        fit = pill("BETTER ADAPTED TO THE SAME GRID", GOOD, 4.2).move_to([0, -1.95, 0])
        adapt = VGroup(rows, down_arrows, fit)
        self.play(FadeOut(qat_loop), FadeIn(before), run_time=.55)
        self.play(LaggedStart(*[GrowArrow(a) for a in down_arrows], lag_ratio=.08),
                  FadeIn(after), run_time=.85)
        self.play(FadeIn(fit, shift=UP * .08), run_time=.4)
        self.keep_stage(adapt)
        self.play(Indicate(after[2], color=GOOD, scale_factor=1.05), run_time=.7)
        self.to(49)

        # 49–58 s — side-by-side summary centered on exposure to the error.
        self.text(
            "가장 큰 차이는 오차를 학습 중 경험했는가입니다",
            "PTQ는 빠르게 적용하지만 사전 적응이 없고, QAT는 추가 학습이\n필요한 대신 Quantization 환경에 적응할 기회를 줍니다.",
            "PTQ  ·  error after training       QAT  ·  error during training",
        )
        ptq_compare = self.compare_card(
            "PTQ", ("학습 완료 후 적용", "재학습 부담 적음", "사전 적응 없음"), SNAP)
        qat_compare = self.compare_card(
            "QAT", ("학습 중 효과 포함", "추가 학습 필요", "오차에 적응 가능"), GRID)
        comparison = VGroup(ptq_compare, qat_compare).arrange(RIGHT, buff=.42).scale(.9)
        comparison.move_to([0, .35, 0])
        key = pill("DID TRAINING EXPERIENCE THE ERROR?", ERROR, 4.8)
        key.move_to([0, -1.9, 0])
        summary_stage = VGroup(comparison, key)
        self.play(FadeOut(adapt), FadeIn(comparison), run_time=.75)
        self.play(FadeIn(key, shift=UP * .08), run_time=.4)
        self.keep_stage(summary_stage)
        self.play(Indicate(key, color=ERROR, scale_factor=1.05), run_time=.7)
        self.to(58)

        # 58–60 s — self-contained closing statement, no next-episode teaser.
        self.text(
            "PTQ는 나중에 줄이고, QAT는 오차와 함께 학습합니다",
            "적용 시점이 달라지면 모델이 Quantization Error에\n적응할 기회를 가졌는지도 달라집니다.",
            "PTQ = quantize after training     ·     QAT = train with quantization effects",
        )
        close = VGroup(
            pill("TRAIN", VALUE, 1.4), txt("→", 24, MUTED),
            pill("PTQ", SNAP, 1.2), txt("│", 28, MUTED),
            pill("QAT LOOP", GRID, 1.7), txt("→", 24, MUTED),
            pill("ADAPTED MODEL", GOOD, 2.35),
        ).arrange(RIGHT, buff=.18).scale(.9).move_to([0, .25, 0])
        self.play(FadeOut(summary_stage), run_time=.32)
        self.remove(summary_stage, comparison, key, ptq_compare, qat_compare)
        self.play(FadeIn(close), run_time=.33)
        self.keep_stage(close)
        self.to(60)

    def model_card(self, label, color):
        box = RoundedRectangle(width=2.45, height=1.5, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box, txt(label, 22, color).move_to(box))

    def branch_card(self, title, subtitle, color):
        box = RoundedRectangle(width=2.75, height=1.65, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        return VGroup(
            box,
            txt(title, 27, color).move_to(box.get_center() + UP * .35),
            txt(subtitle, 19, INK).move_to(box.get_center() + DOWN * .37),
        )

    def process_box(self, label, color, width):
        box = RoundedRectangle(width=width, height=1.5, corner_radius=.18,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box, txt(label, 20, color).move_to(box))

    def loop_box(self, label, color):
        box = RoundedRectangle(width=1.72, height=1.2, corner_radius=.15,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box, txt(label, 17, color).move_to(box))

    def routed_arrow(self, source, target, index):
        # Horizontal edges use straight arrows; row changes use an elbow path.
        if index in (0, 1, 3, 4):
            if target.get_center()[0] > source.get_center()[0]:
                return Arrow(source.get_right(), target.get_left(), buff=.06,
                             color=MUTED, stroke_width=2, tip_length=.09)
            return Arrow(source.get_left(), target.get_right(), buff=.06,
                         color=MUTED, stroke_width=2, tip_length=.09)
        if index == 2:
            return CurvedArrow(source.get_bottom(), target.get_top(), angle=-PI / 3,
                               color=MUTED, stroke_width=2, tip_length=.09)
        return CurvedArrow(source.get_top(), target.get_bottom(), angle=-PI / 3,
                           color=GOOD, stroke_width=2, tip_length=.09)

    def adaptation_row(self, label, proportions, color):
        axis = Line(LEFT * 2.9, RIGHT * 2.9, color=MUTED, stroke_width=2.2)
        ticks = VGroup(*[
            Line(UP * .23, DOWN * .23, color=GRID, stroke_width=2.5)
            .move_to(axis.point_from_proportion(i / 5)) for i in range(6)
        ])
        dots = VGroup(*[
            Dot(axis.point_from_proportion(p) + UP * .46,
                radius=.1, color=color) for p in proportions
        ])
        title = txt(label, 19, color).next_to(axis, LEFT, buff=.25)
        return VGroup(axis, ticks, dots, title)

    def compare_card(self, title, lines, color):
        box = RoundedRectangle(width=3.65, height=3.15, corner_radius=.22,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06)
        items = VGroup(*[txt(line, 20, INK) for line in lines])
        items.arrange(DOWN, buff=.32).move_to(box.get_center() + DOWN * .25)
        return VGroup(
            box,
            txt(title, 28, color).move_to(box.get_center() + UP * 1.05),
            items,
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
