"""GPU operations 10: two reductions make Softmax a cooperative computation."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=2.8, height=.82, size=24):
    box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.10)
    return VGroup(box, label(value, size, color, width - .2))


def row(values, color=WEIGHT, width=1.32, size=25, gap=.18):
    return VGroup(*[card(str(x), color, width, .78, size) for x in values]).arrange(RIGHT, buff=gap)


def arrow(a, b, color=MUTED):
    return Arrow(a, b, buff=.06, color=color, stroke_width=2.6, tip_length=.13)


def down_chain(values, colors=None, ytop=2.85, step=1.4, width=5.4):
    colors = colors or [WEIGHT] * len(values)
    blocks = VGroup(*[card(v, colors[i], width, .8, 25).move_to([0, ytop-i*step, 0])
                      for i, v in enumerate(values)])
    links = VGroup(*[arrow(blocks[i].get_bottom(), blocks[i+1].get_top(), colors[i+1])
                     for i in range(len(blocks)-1)])
    return VGroup(blocks, links)


class GPUSoftmaxParallel(Scene):
    DURATION = 108

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(VGroup(
            label("GPU OPERATIONS  /  10", 20, MUTED).move_to(UP*7.3),
            label("Softmax는 GPU에서 왜 까다로울까?", 31).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED,
                 stroke_opacity=.35),
        ), self.progress)

        # 1: elementwise ReLU versus a shared Softmax denominator.
        self.copy("ReLU는 혼자, Softmax는 함께", "출력 하나에 다른 입력도 영향")
        left = card("ReLU", GOOD, 3.25, .82, 29).move_to([-2.05, 3, 0])
        right = card("Softmax", ACCENT, 3.25, .82, 29).move_to([2.05, 3, 0])
        l_in = row(("x₀", "x₁"), GOOD, 1.18).move_to([-2.05, 1.1, 0])
        l_out = row(("y₀", "y₁"), GOOD, 1.18).move_to([-2.05, -1.2, 0])
        r_in = row(("x₀", "x₁"), ACCENT, 1.18).move_to([2.05, 1.1, 0])
        r_sum = card("Σ exp(xⱼ)", SPARSE, 2.8, .78, 24).move_to([2.05, -.45, 0])
        r_out = row(("p₀", "p₁"), ACCENT, 1.18).move_to([2.05, -2.05, 0])
        links = VGroup(*[arrow(l_in[i].get_bottom(), l_out[i].get_top(), GOOD)
                          for i in range(2)],
                       *[arrow(r_in[i].get_bottom(), r_sum.get_top(), SPARSE)
                          for i in range(2)],
                       *[arrow(r_sum.get_bottom(), r_out[i].get_top(), ACCENT)
                          for i in range(2)])
        self.show(VGroup(left, right, l_in, l_out, r_in, r_sum, r_out, links,
                         label("yᵢ = max(0, xᵢ)        pᵢ = exp(xᵢ) / Σⱼ exp(xⱼ)",
                               23).move_to([0, -3.45, 0])))
        self.to(9)

        # 2: four local exponentials, one global denominator.
        self.copy("각 Thread의 지수는 구했지만", "공통 분모가 아직 없음")
        a = row(("T₀", "T₁", "T₂", "T₃"), ACCENT).move_to([0, 2.8, 0])
        b = row((1, 2, 3, 4), WEIGHT).move_to([0, 1.2, 0])
        c = row(("e¹", "e²", "e³", "e⁴"), GOOD).move_to([0, -.5, 0])
        den = card("분모 = e¹ + e² + e³ + e⁴", SPARSE, 6.4, .9, 25)
        den.move_to([0, -2.75, 0])
        self.show(VGroup(a, b, c, den,
                         *[arrow(a[i].get_bottom(), b[i].get_top(), ACCENT) for i in range(4)],
                         *[arrow(b[i].get_bottom(), c[i].get_top(), GOOD) for i in range(4)],
                         *[arrow(c[i].get_bottom(), den.get_top(), SPARSE) for i in range(4)]))
        self.to(18)

        # 3: serial accumulation leaves most threads idle.
        self.copy("한 Thread가 모두 더한다면?", "입력이 길수록 병렬성이 부족")
        inputs = row(("a", "b", "c", "d"), WEIGHT).move_to([0, 2.6, 0])
        serial = down_chain(("a + b", "(a+b) + c", "(a+b+c) + d"),
                            [PRUNE]*3, ytop=.9, step=1.35, width=4.8)
        self.show(VGroup(inputs, serial,
                         label("한 줄로 이어지는 의존성", 25, PRUNE)
                         .move_to([0, -3.25, 0])))
        self.to(25)

        # 4: balanced reduction with concurrent partial sums.
        self.copy("합도 병렬로 만든다", "부분합 → 다시 부분합 → 전체 합")
        top = row(("a", "b", "c", "d"), WEIGHT).move_to([0, 2.65, 0])
        mid = row(("a+b", "c+d"), GOOD, 2.35, 25, .55).move_to([0, .6, 0])
        end = card("(a+b) + (c+d)", ACCENT, 4.4, .9, 27).move_to([0, -1.6, 0])
        self.show(VGroup(top, mid, end,
                         *[arrow(top[i].get_bottom(), mid[i//2].get_top(), GOOD)
                           for i in range(4)],
                         *[arrow(mid[i].get_bottom(), end.get_top(), ACCENT)
                           for i in range(2)],
                         label("REDUCTION", 27, ACCENT).move_to([0, -3.2, 0])))
        self.to(33)

        # 5: stable Softmax requires a maximum first.
        self.copy("큰 지수는 범위를 넘을 수 있다", "먼저 최대값 m을 빼기")
        original = card("[1, 2, 1000]", WEIGHT, 5.2, .85, 30).move_to([0, 2.75, 0])
        warn = card("exp(1000)  →  overflow 위험", PRUNE, 6.2, .9, 25)
        warn.move_to([0, 1.05, 0])
        maximum = card("m = max(x) = 1000", ACCENT, 5.3, .85, 27)
        maximum.move_to([0, -.75, 0])
        shifted = card("exp(xᵢ − m)", GOOD, 5.3, .9, 31)
        shifted.move_to([0, -2.5, 0])
        self.show(VGroup(original, warn, maximum, shifted,
                         arrow(original.get_bottom(), warn.get_top(), PRUNE),
                         arrow(warn.get_bottom(), maximum.get_top(), ACCENT),
                         arrow(maximum.get_bottom(), shifted.get_top(), GOOD)))
        self.to(43)

        # 6: max is the first reduction.
        self.copy("첫 번째 Reduction: MAX", "모든 입력을 비교해 m 하나로")
        top = row((1, 7, 3, 5), WEIGHT).move_to([0, 2.7, 0])
        mid = row((7, 5), SPARSE, 2.0, 29, .6).move_to([0, .55, 0])
        end = card("m = max(7, 5) = 7", ACCENT, 5.3, .9, 29)
        end.move_to([0, -1.65, 0])
        self.show(VGroup(top, mid, end,
                         *[arrow(top[i].get_bottom(), mid[i//2].get_top(), SPARSE)
                           for i in range(4)],
                         *[arrow(mid[i].get_bottom(), end.get_top(), ACCENT)
                           for i in range(2)],
                         label("MAX REDUCTION", 25, ACCENT).move_to([0, -3.2, 0])))
        self.to(51)

        # 7: broadcast m, then independent elementwise work.
        self.copy("m을 공유하면 다시 원소별 계산", "각 Thread: exp(xᵢ − m)")
        m = card("공통 m", ACCENT, 3.0, .85, 29).move_to([0, 2.7, 0])
        threads = row(("T₀", "T₁", "T₂", "T₃"), WEIGHT).move_to([0, .65, 0])
        outputs = row(("e⁰", "e⁻¹", "e⁻²", "e⁻³"), GOOD).move_to([0, -1.55, 0])
        self.show(VGroup(m, threads, outputs,
                         *[arrow(m.get_bottom(), threads[i].get_top(), ACCENT)
                           for i in range(4)],
                         *[arrow(threads[i].get_bottom(), outputs[i].get_top(), GOOD)
                           for i in range(4)],
                         label("예: x = [7, 6, 5, 4]", 23, MUTED)
                         .move_to([0, -3.2, 0])))
        self.to(58)

        # 8: sum reduction followed by broadcast and normalization.
        self.copy("두 번째 Reduction: SUM", "합 s를 공유한 뒤 각 출력 정규화")
        exps = row(("u₀", "u₁", "u₂", "u₃"), GOOD).move_to([0, 2.8, 0])
        sums = row(("u₀+u₁", "u₂+u₃"), SPARSE, 2.4, 24, .5).move_to([0, .85, 0])
        total = card("s = Σⱼ exp(xⱼ−m)", ACCENT, 5.6, .82, 27)
        total.move_to([0, -1.05, 0])
        result = card("pᵢ = exp(xᵢ−m) / s", GOOD, 5.8, .82, 27)
        result.move_to([0, -2.95, 0])
        self.show(VGroup(exps, sums, total, result,
                         *[arrow(exps[i].get_bottom(), sums[i//2].get_top(), SPARSE)
                           for i in range(4)],
                         *[arrow(sums[i].get_bottom(), total.get_top(), ACCENT)
                           for i in range(2)],
                         arrow(total.get_bottom(), result.get_top(), GOOD)))
        self.to(67)

        # 9: contrast the execution structures.
        self.copy("ReLU와 Softmax의 차이", "독립 계산  ↔  중간에 두 번 모으기")
        relu = down_chain(("입력 xᵢ", "max(0, xᵢ)", "출력 yᵢ"),
                          [WEIGHT, GOOD, GOOD], ytop=2.8, step=1.35, width=3.15)
        relu.shift(LEFT*2.0)
        soft = down_chain(("입력 x", "MAX", "exp(xᵢ−m)", "SUM", "나누기"),
                          [WEIGHT, ACCENT, GOOD, ACCENT, GOOD],
                          ytop=2.8, step=1.4, width=3.15)
        soft.shift(RIGHT*2.0)
        self.show(VGroup(relu, soft,
                         label("ReLU", 26, GOOD).move_to([-2.0, 4.1, 0]),
                         label("Softmax", 26, ACCENT).move_to([2.0, 4.1, 0])))
        self.to(75)

        # 10: serial phase boundaries are where cooperation matters.
        self.copy("까다로운 이유는 exp만이 아니다", "Elementwise + Reduction + 협력")
        chain = down_chain(("원소별 계산", "MAX Reduction", "원소별 exp",
                            "SUM Reduction", "원소별 나누기"),
                           [GOOD, ACCENT, GOOD, ACCENT, GOOD],
                           ytop=3.25, step=1.55, width=5.6)
        self.show(VGroup(chain,
                         label("Reduction 결과가 나와야 다음 단계 진행", 22, PRUNE)
                         .move_to([0, -4.0, 0])))
        self.to(83)

        # 11: separate kernels can materialize intermediates.
        self.copy("Kernel을 나누면 데이터가 왕복", "중간 Write / Read가 추가될 수 있음")
        chain = down_chain(("MAX Kernel", "Write / Read", "EXP Kernel",
                            "Write / Read", "SUM + DIV Kernel"),
                           [ACCENT, PRUNE, GOOD, PRUNE, SPARSE],
                           ytop=3.25, step=1.5, width=5.8)
        self.show(VGroup(chain, label("Global Memory 왕복", 24, PRUNE)
                         .move_to([0, -4.0, 0])))
        self.to(91)

        # 12: fusion is conditional, reductions remain.
        self.copy("가능하면 한 Kernel 안에서 연결", "두 Reduction은 여전히 필요")
        border = RoundedRectangle(width=6.8, height=5.9, corner_radius=.26,
                                  stroke_color=ACCENT, stroke_width=2,
                                  fill_color=ACCENT, fill_opacity=.035)
        border.move_to([0, .1, 0])
        chain = down_chain(("MAX", "exp(xᵢ−m)", "SUM", "Normalize"),
                           [ACCENT, GOOD, ACCENT, GOOD],
                           ytop=2.05, step=1.23, width=4.8)
        self.show(VGroup(border, chain,
                         label("SOFTMAX KERNEL", 25, ACCENT)
                         .move_to([0, 3.55, 0]),
                         label("큰 입력은 여러 단계로 처리 가능", 21, MUTED)
                         .move_to([0, -3.7, 0])))
        self.to(99)

        # 13: summary and teaser.
        self.copy("짧은 수식, 협력하는 실행", "다음: Reduction은 어떻게 빨라질까?")
        formula = card("pᵢ = exp(xᵢ−m) / Σⱼ exp(xⱼ−m)",
                       WEIGHT, 7.0, 1.05, 27).move_to([0, 2.7, 0])
        flow = down_chain(("MAX Reduction", "원소별 exp",
                           "SUM Reduction", "원소별 나누기"),
                          [ACCENT, GOOD, ACCENT, GOOD],
                          ytop=.9, step=1.26, width=5.4)
        self.show(VGroup(formula, flow))
        self.to(108)

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
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.2, remaining))
            self.wait(max(0, target-self.time))
