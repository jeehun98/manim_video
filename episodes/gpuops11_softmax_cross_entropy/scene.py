"""GPU operations 11: compute cross entropy from logits without materializing p."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, height=.85, size=25):
    box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.1)
    return VGroup(box, label(value, size, color, width-.2))


def arrow(a, b, color=MUTED):
    return Arrow(a, b, buff=.06, color=color, stroke_width=2.7, tip_length=.13)


def row(values, color=WEIGHT, width=1.35, size=25, gap=.18):
    return VGroup(*[card(str(v), color, width, .8, size) for v in values]).arrange(RIGHT, buff=gap)


def chain(values, colors, top=3.0, step=1.35, width=5.3):
    blocks = VGroup(*[card(v, colors[i], width, .8, 25).move_to([0, top-i*step, 0])
                      for i,v in enumerate(values)])
    links = VGroup(*[arrow(blocks[i].get_bottom(), blocks[i+1].get_top(), colors[i+1])
                     for i in range(len(blocks)-1)])
    return VGroup(blocks, links)


class GPUSoftmaxCrossEntropy(Scene):
    DURATION = 100

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(VGroup(
            label("GPU OPERATIONS  /  11", 20, MUTED).move_to(UP*7.3),
            label("Softmax와 Cross Entropy는 한 번의 GPU Kernel로 계산된다", 30)
            .move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED,
                 stroke_opacity=.35),
        ), self.progress)

        # 1: classification pipeline and numerically correct illustrative row.
        self.copy("분류 모델 끝에서 만나는 두 연산", "logits  →  확률  →  loss")
        flow = chain(("Model", "Logits", "Softmax", "Cross Entropy"),
                     [WEIGHT, WEIGHT, ACCENT, GOOD], top=3.25, step=1.28,
                     width=4.6)
        nums = card("[2.1, 0.7, −1.2, 3.0]", WEIGHT, 6.0, .78, 24)
        nums.move_to([0, -2.1, 0])
        probs = card("≈ [0.267, 0.066, 0.010, 0.657]", GOOD, 6.2, .78, 22)
        probs.move_to([0, -3.2, 0])
        self.show(VGroup(flow, nums, probs))
        self.to(10)

        # 2: familiar formula and two-stage computational interpretation.
        self.copy("교과서에서는 두 단계", "Softmax 확률을 만든 뒤 −log")
        p = card("pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)", ACCENT, 6.5, 1.0, 28)
        p.move_to([0, 2.6, 0])
        l = card("L = −log(pᵧ)", GOOD, 5.0, 1.0, 31)
        l.move_to([0, .4, 0])
        graph = chain(("Logits z", "Softmax p", "−log pᵧ", "Loss L"),
                      [WEIGHT, ACCENT, GOOD, GOOD], top=-1.3, step=.83,
                      width=3.8)
        self.show(VGroup(p, l, arrow(p.get_bottom(), l.get_top(), GOOD), graph))
        self.to(19)

        # 3: select target class, making the unnecessary output visible.
        self.copy("정말 확률 전체가 필요할까?", "한 샘플의 정답 클래스 y만 사용")
        logits = row(("z₀", "z₁", "z₂", "z₃"), WEIGHT)
        logits.move_to([0, 2.6, 0])
        probabilities = row(("p₀", "p₁", "p₂", "p₃"), MUTED)
        probabilities.move_to([0, .4, 0])
        selected = card("pᵧ = p₃ ≈ 0.657", GOOD, 4.9, .95, 28)
        selected.move_to([0, -1.7, 0])
        probabilities[3][0].set_stroke(GOOD)
        probabilities[3][1].set_color(GOOD)
        self.show(VGroup(logits, probabilities, selected,
                         *[arrow(logits[i].get_bottom(), probabilities[i].get_top(),
                                 GOOD if i==3 else MUTED) for i in range(4)],
                         arrow(probabilities[3].get_bottom(), selected.get_top(), GOOD),
                         label("다른 확률은 이 loss에 사용하지 않음", 23, MUTED)
                         .move_to([0, -3.25, 0])))
        self.to(28)

        # 4: substitution and stable log-sum-exp.
        self.copy("두 식을 합치면 p Tensor가 사라진다", "안정적인 logits → loss 계산")
        step1 = card("L = −log[ exp(zᵧ) / Σⱼ exp(zⱼ) ]", WEIGHT,
                     7.1, .9, 25).move_to([0, 2.85, 0])
        step2 = card("L = −zᵧ + log Σⱼ exp(zⱼ)", ACCENT,
                     6.8, .9, 27).move_to([0, .95, 0])
        step3 = card("m = maxⱼ zⱼ", SPARSE, 4.5, .8, 27)
        step3.move_to([0, -.9, 0])
        step4 = card("L = −(zᵧ−m) + log Σⱼ exp(zⱼ−m)", GOOD,
                     7.25, 1.0, 25).move_to([0, -2.8, 0])
        self.show(VGroup(step1, step2, step3, step4,
                         arrow(step1.get_bottom(), step2.get_top(), ACCENT),
                         arrow(step2.get_bottom(), step3.get_top(), SPARSE),
                         arrow(step3.get_bottom(), step4.get_top(), GOOD)))
        self.to(40)

        # 5: separate kernels create a full intermediate p materialization.
        self.copy("따로 실행하면 중간 확률을 저장", "Write p  →  Global Memory  →  Read p")
        blocks = chain(("Softmax Kernel", "Write p", "Global Memory",
                        "Read p", "Cross Entropy Kernel"),
                       [ACCENT, PRUNE, WEIGHT, PRUNE, GOOD],
                       top=3.15, step=1.45, width=5.7)
        self.show(VGroup(blocks,
                         label("중간 p Tensor의 메모리 왕복", 23, PRUNE)
                         .move_to([0, -4.05, 0])))
        self.to(50)

        # 6: the combined path, explicitly conditional on implementation.
        self.copy("조건이 맞으면 결합해 계산", "하나의 fused Kernel 또는 결합된 연산")
        border = RoundedRectangle(width=7.0, height=6.45, corner_radius=.25,
                                  stroke_color=GOOD, stroke_width=2,
                                  fill_color=GOOD, fill_opacity=.035)
        border.move_to([0, .25, 0])
        blocks = chain(("Logits", "MAX + exp / SUM", "정답 logit zᵧ", "Loss L"),
                       [WEIGHT, ACCENT, SPARSE, GOOD],
                       top=2.9, step=1.45, width=5.3)
        self.show(VGroup(border, blocks,
                         label("중간 Softmax Tensor 없음", 23, GOOD)
                         .move_to([0, -3.75, 0])))
        self.to(60)

        # 7: retain both reductions, remove full-vector normalization output.
        self.copy("두 Reduction은 그대로 남는다", "전체 확률 Tensor의 완성만 생략")
        before = chain(("MAX", "exp", "SUM", "모든 pᵢ normalize"),
                       [ACCENT, GOOD, ACCENT, PRUNE],
                       top=2.7, step=1.35, width=3.15)
        before.shift(LEFT*2.05)
        after = chain(("MAX", "exp", "SUM", "정답 loss 직접 계산"),
                      [ACCENT, GOOD, ACCENT, GOOD],
                      top=2.7, step=1.35, width=3.15)
        after.shift(RIGHT*2.05)
        self.show(VGroup(before, after,
                         label("Softmax만", 23, PRUNE)
                         .move_to([-2.05, 3.8, 0]),
                         label("Softmax + CE", 23, GOOD)
                         .move_to([2.05, 3.8, 0])))
        self.to(69)

        # 8: max subtraction also protects numerical range.
        self.copy("수치적으로도 더 안정적", "max를 뺀 log-sum-exp")
        large = card("z = [1000, 999, 998]", WEIGHT, 5.7, .9, 28)
        large.move_to([0, 2.85, 0])
        danger = card("exp(1000)  →  overflow 위험", PRUNE, 6.5, .9, 25)
        danger.move_to([0, 1.0, 0])
        shift = card("m = 1000  →  z−m = [0, −1, −2]", ACCENT, 6.6, .9, 25)
        shift.move_to([0, -.9, 0])
        stable = card("L = −(zᵧ−m) + log Σ exp(zⱼ−m)", GOOD,
                      7.1, 1.0, 25).move_to([0, -2.8, 0])
        self.show(VGroup(large, danger, shift, stable,
                         arrow(large.get_bottom(), danger.get_top(), PRUNE),
                         arrow(danger.get_bottom(), shift.get_top(), ACCENT),
                         arrow(shift.get_bottom(), stable.get_top(), GOOD)))
        self.to(78)

        # 9: operator boundaries need not be execution boundaries.
        self.copy("수식의 경계 ≠ 실행의 경계", "최종 출력이 loss라는 정보 활용")
        separate = chain(("Softmax", "p Tensor", "Cross Entropy"),
                          [ACCENT, PRUNE, GOOD],
                          top=2.2, step=1.5, width=3.15)
        separate.shift(LEFT*2.0)
        combined = card("Fused Loss", GOOD, 3.4, 1.45, 30)
        combined.move_to([2.05, .7, 0])
        self.show(VGroup(separate, combined,
                         label("따로", 24, PRUNE).move_to([-2.0, 3.6, 0]),
                         label("결합 가능", 24, GOOD).move_to([2.05, 3.6, 0]),
                         arrow(separate.get_right()+RIGHT*.15,
                               combined.get_left()+LEFT*.15, ACCENT)))
        self.to(88)

        # 10: strong ending with the implementation caveat on screen.
        self.copy("필요 없는 중간 결과는 만들지 않는다", "단일 Kernel 여부는 구현과 크기에 따라 다름")
        top = card("Logits", WEIGHT, 4.6, .95, 30).move_to([0, 2.75, 0])
        fused = card("Fused Loss", GOOD, 5.8, 1.12, 34).move_to([0, .45, 0])
        result = card("L ≈ 0.420  (y = 3)", ACCENT, 5.8, .95, 28)
        result.move_to([0, -1.85, 0])
        caveat = label("확률 전체가 필요하면 저장해야 함", 22, MUTED)
        caveat.move_to([0, -3.5, 0])
        self.show(VGroup(top, fused, result, caveat,
                         arrow(top.get_bottom(), fused.get_top(), GOOD),
                         arrow(fused.get_bottom(), result.get_top(), ACCENT)))
        self.to(100)

    def copy(self, heading, note):
        old = VGroup(self.heading, self.note)
        if len(old):
            self.play(FadeOut(old), run_time=.14)
        self.heading = label(heading, 30).move_to(UP*5.12)
        self.note = label(note, 22, ACCENT).move_to(DOWN*4.9)
        self.play(FadeIn(self.heading), FadeIn(self.note), run_time=.27)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.22)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP*.1), run_time=.48)

    def to(self, target):
        remaining = target-self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.2, remaining))
            self.wait(max(0, target-self.time))
