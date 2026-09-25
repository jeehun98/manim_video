"""Pruning 04: optimization as a model, mathematics, and hardware problem."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, pill, txt,
)


def cell_row(labels, live=None, width=1.2, color=WEIGHT):
    live = set(range(len(labels)) if live is None else live)
    row = VGroup()
    for i, label in enumerate(labels):
        active = i in live
        box = RoundedRectangle(width=width, height=.76, corner_radius=.12,
                               stroke_color=color if active else ZERO,
                               stroke_width=1.4, fill_color=color if active else ZERO,
                               fill_opacity=.09 if active else .04)
        row.add(VGroup(box, txt(str(label) if active else "0", 21,
                                INK if active else ZERO, width - .14)))
    row.arrange(RIGHT, buff=.13)
    return row


def sparse_grid(rows, cols, alive, cell=.38, groups=False):
    alive = set(alive)
    grid = VGroup()
    for i in range(rows * cols):
        live = i in alive
        grid.add(RoundedRectangle(
            width=cell * .82, height=cell * .82, corner_radius=.05,
            stroke_color=GOOD if live else ZERO, stroke_width=1,
            fill_color=GOOD if live else ZERO,
            fill_opacity=.82 if live else .08,
        ))
    grid.arrange_in_grid(rows, cols, buff=.065)
    return grid


def gpu_box(label="GPU"):
    body = RoundedRectangle(width=2.35, height=1.5, corner_radius=.18,
                            stroke_color=WEIGHT, stroke_width=2,
                            fill_color=WEIGHT, fill_opacity=.08)
    pins = VGroup(*[
        Line(LEFT * .16, RIGHT * .16, color=WEIGHT, stroke_width=2)
        for _ in range(8)
    ])
    pins.arrange(DOWN, buff=.09).next_to(body, LEFT, buff=0)
    pins2 = pins.copy().next_to(body, RIGHT, buff=0)
    return VGroup(body, pins, pins2, txt(label, 27, WEIGHT))


class HardwareAwareOptimization(Scene):
    DURATION = 100

    def construct(self):
        self.head = VGroup(); self.note = VGroup(); self.sub = VGroup()
        self.chrome = VGroup(
            txt("PRUNING & SPARSITY  /  04", 20, MUTED).move_to(UP * 7.25),
            txt("신경망 최적화는 왜 하드웨어를 알아야 할까?", 32).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0]); self.add(self.progress)

        # 0–6 — recap the 2:4 rule.
        self.text("2:4에서는 Weight의 절반이 0입니다",
                  "연속된 4개마다 정확히 2개를 남기는\n규칙적인 sparsity입니다.",
                  "50% REMOVED  ·  2 NON-ZERO / 4")
        patterns = ((0, 2), (1, 3), (0, 1), (1, 2))
        groups = VGroup(*[cell_row(("●", "●", "●", "●"), p, .78, GOOD)
                          for p in patterns])
        groups.arrange(DOWN, buff=.2).move_to([0, .45, 0])
        braces = VGroup(*[SurroundingRectangle(g, color=SPARSE, buff=.1,
                                               corner_radius=.12) for g in groups])
        recap = VGroup(groups, braces,
                       pill("2 / 4", ACCENT, 1.75).next_to(groups, DOWN, buff=.45))
        self.play(LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=.1), run_time=.8)
        self.play(FadeIn(braces), FadeIn(recap[-1]), run_time=.55)
        self.keep_stage(recap); self.to(6)

        # 6–16 — zeros still occupy dense storage and dense execution.
        self.text("0으로 만들었다고 계산이 자동으로 사라지지는 않습니다",
                  "Dense 형태로 그대로 저장하고 실행하면\n0도 공간과 연산 위치를 차지합니다.",
                  "ZERO VALUE  ≠  REMOVED OPERATION")
        dense_row = cell_row(("a", "0", "c", "0"), width=1.35).move_to([0, .55, 0])
        slots = VGroup(*[txt("stored", 17, MUTED).next_to(x, DOWN, buff=.18)
                         for x in dense_row])
        dense_stage = VGroup(dense_row, slots,
                             pill("4 STORAGE SLOTS", PRUNE, 2.85).move_to([0, -1.25, 0]))
        self.play(FadeOut(recap), FadeIn(dense_row), FadeIn(slots), run_time=.65)
        self.play(FadeIn(dense_stage[-1]),
                  Indicate(dense_row[1], color=PRUNE, scale_factor=1.08),
                  Indicate(dense_row[3], color=PRUNE, scale_factor=1.08), run_time=.75)
        self.keep_stage(dense_stage); self.to(16)

        # 16–29 — supported 2:4 representation stores values plus metadata.
        self.text("지원되는 2:4 경로는 규칙을 압축해 표현합니다",
                  "살아남은 값과 위치 정보를 이용해\n어느 두 Weight를 계산할지 나타냅니다.",
                  "VALUES  +  POSITION METADATA")
        values = cell_row(("a", "c"), width=1.25, color=GOOD).move_to([-1.35, .55, 0])
        meta = cell_row(("0", "2"), width=.88, color=ACCENT).move_to([2.0, .55, 0])
        plus = txt("+", 38, MUTED).move_to([.45, .55, 0])
        labels = VGroup(txt("VALUES", 20, GOOD).next_to(values, UP, buff=.3),
                        txt("POSITIONS", 20, ACCENT).next_to(meta, UP, buff=.3))
        path = Arrow([0, -1.1, 0], [0, -1.85, 0], color=WEIGHT,
                     stroke_width=3, tip_length=.14)
        supported = pill("SUPPORTED SPARSE OP", WEIGHT, 3.65).move_to([0, -2.3, 0])
        packed = VGroup(values, meta, plus, labels, path, supported)
        self.play(FadeOut(dense_stage), FadeIn(values), FadeIn(plus), FadeIn(meta),
                  FadeIn(labels), run_time=.75)
        self.play(GrowArrow(path), FadeIn(supported), run_time=.65)
        self.keep_stage(packed); self.to(29)

        # 29–36 — positions vary, count stays predictable.
        self.text("위치는 달라도 구조는 항상 2 / 4입니다",
                  "하드웨어는 각 그룹에서 처리할 값이\n항상 두 개라는 사실을 알고 있습니다.",
                  "VARIABLE POSITIONS  ·  FIXED COUNT")
        p_alive = ((0, 2), (1, 3), (0, 1))
        cards = VGroup(*[cell_row(("●", "●", "●", "●"), p, .82, GOOD)
                         for p in p_alive]).arrange(DOWN, buff=.28).move_to([0, .55, 0])
        funnels = VGroup(*[
            Arrow(c.get_right(), [3.0, c.get_center()[1], 0], color=ACCENT,
                  stroke_width=2, tip_length=.1) for c in cards
        ])
        rule = pill("ALWAYS 2 / 4", ACCENT, 2.85).move_to([0, -1.85, 0])
        regular = VGroup(cards, funnels, rule)
        self.play(FadeOut(packed), LaggedStart(*[FadeIn(c) for c in cards],
                                               lag_ratio=.12), run_time=.75)
        self.play(LaggedStart(*[GrowArrow(a) for a in funnels], lag_ratio=.1),
                  FadeIn(rule), run_time=.75)
        self.keep_stage(regular); self.to(36)

        # 36–48 — compare nominal sparsity percentages.
        self.text("어느 쪽이 더 최적화된 모델일까요?",
                  "90%를 자유롭게 지운 모델과\n50%를 규칙적으로 지운 모델을 비교해봅시다.",
                  "90% UNSTRUCTURED        vs        50% 2:4")
        random_alive = (3, 14, 16, 28)
        two4_alive = (0, 2, 5, 7, 8, 9, 13, 15, 17, 19, 20, 22, 25, 26, 28, 31)
        random = sparse_grid(4, 8, random_alive).move_to([-2.1, .55, 0])
        two4 = sparse_grid(4, 8, two4_alive).move_to([2.1, .55, 0])
        compare = VGroup(
            random, two4,
            pill("90% ZERO", PRUNE, 2.25).next_to(random, UP, buff=.4),
            pill("50% · 2:4", GOOD, 2.25).next_to(two4, UP, buff=.4),
            txt("MORE REMOVED", 19, PRUNE).next_to(random, DOWN, buff=.4),
            txt("MORE REGULAR", 19, GOOD).next_to(two4, DOWN, buff=.4),
        )
        self.play(FadeOut(regular), FadeIn(random), FadeIn(compare[2]), run_time=.6)
        self.play(FadeIn(two4), FadeIn(compare[3:]), run_time=.65)
        self.keep_stage(compare); self.to(48)

        # 48–59 — hardware support can invert the intuitive ranking.
        self.text("더 많이 지운 구조가 항상 더 빠른 것은 아닙니다",
                  "불규칙한 90%보다 하드웨어가 직접 지원하는\n50% 구조가 실행에 더 유리할 수 있습니다.",
                  "얼마나 제거?  →  하드웨어가 이용 가능?")
        gpu = gpu_box().move_to([2.75, .2, 0])
        random_icon = sparse_grid(3, 6, (2, 9), .3).move_to([-3.0, 1.35, 0])
        regular_icon = sparse_grid(3, 6, (0,2,5,6,9,11,12,13,16), .3).move_to([-3.0, -.9, 0])
        tangled = VGroup(*[
            CurvedArrow(random_icon.get_right(), gpu.get_left(), angle=a, color=PRUNE,
                        stroke_width=1.5, tip_length=.08) for a in (-.5, .15, .55)
        ])
        direct = Arrow(regular_icon.get_right(), gpu.get_left(), color=GOOD,
                       stroke_width=5, tip_length=.15)
        path_labels = VGroup(
            pill("SUPPORT ?", PRUNE, 2.0).next_to(random_icon, DOWN, buff=.25),
            pill("SUPPORTED PATH", GOOD, 2.8).next_to(regular_icon, DOWN, buff=.25),
        )
        hardware_stage = VGroup(gpu, random_icon, regular_icon, tangled, direct, path_labels)
        self.play(FadeOut(compare), FadeIn(gpu), FadeIn(random_icon),
                  FadeIn(regular_icon), run_time=.7)
        self.play(LaggedStart(*[Create(a) for a in tangled], lag_ratio=.1),
                  GrowArrow(direct), FadeIn(path_labels), run_time=.9)
        self.keep_stage(hardware_stage); self.to(59)

        # 59–68 — hardware constraints also constrain the model.
        self.text("하드웨어에 맞추면 모델은 제약을 받습니다",
                  "네 값이 모두 중요해 보여도\n2:4에서는 두 개만 사용할 수 있습니다.",
                  "PARAMETER SPACE ↓")
        full = cell_row(("0.91", "0.87", "0.84", "0.79"), width=1.45).move_to([0, 1.05, 0])
        masked = cell_row(("0.91", "0.87", "0.84", "0.79"), live=(0,1), width=1.45)
        masked.move_to([0, -.75, 0])
        down = Arrow([0, .42, 0], [0, -.15, 0], color=PRUNE,
                     stroke_width=3, tip_length=.14)
        mask_tag = pill("FORCE 2:4", PRUNE, 2.35).move_to([0, -2.0, 0])
        constraint = VGroup(full, masked, down, mask_tag)
        self.play(FadeOut(hardware_stage), FadeIn(full), run_time=.55)
        self.play(GrowArrow(down), FadeIn(masked), FadeIn(mask_tag), run_time=.75)
        self.play(Indicate(masked[2], color=PRUNE, scale_factor=1.08),
                  Indicate(masked[3], color=PRUNE, scale_factor=1.08), run_time=.65)
        self.keep_stage(constraint); self.to(68)

        # 68–80 — training can adapt within the supported constraint.
        self.text("모델도 하드웨어 제약에 맞춰 적응할 수 있습니다",
                  "Training이나 fine-tuning으로 남은 Weight를 조정해\n제한된 구조 안에서 표현을 다시 찾습니다.",
                  "2:4 CONSTRAINT  →  LEARNING  →  ADAPTATION")
        steps = VGroup(
            pill("2:4 MASK", PRUNE, 2.1), pill("TRAIN", ACCENT, 1.9),
            pill("ADAPTED", GOOD, 2.15),
        ).arrange(RIGHT, buff=.55).move_to([0, 1.65, 0])
        step_arrows = VGroup(*[
            Arrow(steps[i].get_right(), steps[i+1].get_left(), buff=.1,
                  color=MUTED, stroke_width=2.5, tip_length=.11) for i in range(2)
        ])
        w0 = cell_row(("0.91", "0.87", "0", "0"), width=1.2).move_to([0, -.15, 0])
        w1 = cell_row(("1.04", "0.73", "0", "0"), width=1.2).move_to(w0)
        loss_axis = VGroup(
            Line([-2.8,-1.8,0],[2.8,-1.8,0],color=MUTED,stroke_width=1.5),
            VMobject(color=GOOD, stroke_width=4).set_points_smoothly([
                [-2.5,-.75,0],[-1.4,-1.05,0],[-.2,-1.35,0],[1.2,-1.58,0],[2.5,-1.68,0]
            ]),
            txt("loss ↓", 20, GOOD).move_to([2.55,-1.25,0]),
        )
        learning = VGroup(steps, step_arrows, w0, loss_axis)
        self.play(FadeOut(constraint), FadeIn(steps[0]), run_time=.45)
        self.play(GrowArrow(step_arrows[0]), FadeIn(steps[1]), FadeIn(w0), run_time=.65)
        self.play(Transform(w0, w1), Create(loss_axis[1]), FadeIn(loss_axis[0]),
                  FadeIn(loss_axis[2]), run_time=1.1)
        self.play(GrowArrow(step_arrows[1]), FadeIn(steps[2]), run_time=.55)
        self.keep_stage(learning); self.to(80)

        # 80–90 — optimization sits at the intersection of three concerns.
        self.text("최적화는 수학 × 모델 × 하드웨어의 공동 문제입니다",
                  "줄일 수 있는 계산, 유지해야 할 표현력,\n지원되는 실행 구조를 함께 봐야 합니다.",
                  "MATHEMATICS  ×  LEARNING  ×  HARDWARE")
        circles = VGroup(
            Circle(1.55, color=ACCENT, fill_color=ACCENT, fill_opacity=.08).shift(LEFT*1.25),
            Circle(1.55, color=GOOD, fill_color=GOOD, fill_opacity=.08).shift(RIGHT*1.25),
            Circle(1.55, color=WEIGHT, fill_color=WEIGHT, fill_opacity=.08).shift(DOWN*1.3),
        ).move_to([0, .65, 0])
        labels3 = VGroup(
            txt("MATH", 22, ACCENT).move_to([-2.0,1.35,0]),
            txt("MODEL", 22, GOOD).move_to([2.0,1.35,0]),
            txt("HARDWARE", 22, WEIGHT).move_to([0,-1.25,0]),
            pill("OPTIMIZATION", INK, 2.8).move_to([0,.45,0]),
        )
        triad = VGroup(circles, labels3)
        self.play(FadeOut(learning), LaggedStart(*[Create(c) for c in circles],
                                                 lag_ratio=.12), run_time=.9)
        self.play(FadeIn(labels3), run_time=.65)
        self.keep_stage(triad); self.to(90)

        # 90–100 — the playlist-level conclusion.
        self.text("좋은 최적화의 기준은 실행 가능한 구조입니다",
                  "가장 적은 계산보다, 모델이 적응할 수 있고\n하드웨어가 효율적으로 실행할 수 있는 계산이 중요합니다.",
                  "BEST EXECUTABLE STRUCTURE")
        wrong = VGroup(txt("BEST MATH?", 34, MUTED),
                       Line([-1.7,0,0],[1.7,0,0],color=PRUNE,stroke_width=6))
        wrong.move_to([0, 1.55, 0])
        arrow = Arrow([0,.8,0],[0,.05,0],color=ACCENT,stroke_width=3,tip_length=.14)
        answer = VGroup(
            RoundedRectangle(width=6.7,height=1.35,corner_radius=.2,
                             stroke_color=GOOD,stroke_width=2.5,
                             fill_color=GOOD,fill_opacity=.08),
            txt("BEST EXECUTABLE\nSTRUCTURE", 33, GOOD, weight=BOLD),
        ).move_to([0,-.85,0])
        qualifiers = VGroup(
            pill("MODEL CAN ADAPT", GOOD, 2.8),
            pill("HARDWARE CAN RUN", WEIGHT, 3.05),
        ).arrange(RIGHT,buff=.35).move_to([0,-2.55,0])
        finale = VGroup(wrong,arrow,answer,qualifiers)
        self.play(FadeOut(triad), FadeIn(wrong), run_time=.55)
        self.play(GrowArrow(arrow), FadeIn(answer,shift=UP*.15), run_time=.75)
        self.play(FadeIn(qualifiers), Indicate(answer,color=GOOD,scale_factor=1.04),
                  run_time=.75)
        self.keep_stage(finale); self.to(100)

    def text(self, head, sub, note):
        old=VGroup(self.head,self.note,self.sub)
        if len(old): self.play(FadeOut(old,shift=UP*.08),run_time=.18)
        self.head=txt(head,30).move_to(UP*5.15)
        self.note=txt(note,22,ACCENT).move_to(DOWN*4.72)
        self.sub=txt(sub,27).move_to(DOWN*6.08)
        self.play(FadeIn(self.head),FadeIn(self.note),FadeIn(self.sub),run_time=.35)

    def keep_stage(self,*allowed):
        roots=(self.chrome,self.progress,self.head,self.note,self.sub,*allowed); keep=set()
        for root in roots: keep.update(root.get_family())
        for mob in list(self.mobjects):
            if mob not in keep: self.remove(mob)

    def to(self,target):
        remain=target-self.time
        if remain<-.04: raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2,-7.35,0]),run_time=min(.28,remain))
            self.wait(max(0,target-self.time))
