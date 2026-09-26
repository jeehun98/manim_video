"""GPU operations 03: loop unrolling exposes work and has a cost."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=2.7, height=.85, size=25):
    box = RoundedRectangle(width=width, height=height, corner_radius=.16,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.09)
    return VGroup(box, label(value, size, color, width - .18))


def arrow(start, end, color=MUTED):
    return Arrow(start, end, buff=.06, color=color, stroke_width=2.7,
                 tip_length=.15)


def code_lines(lines, size=24, color=INK):
    group = VGroup(*[label(line, size, color, 7.4) for line in lines])
    group.arrange(DOWN, buff=.26, aligned_edge=LEFT)
    return group


class GPULoopUnrolling(Scene):
    DURATION = 84

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  03", 20, MUTED).move_to(UP * 7.3),
            label("왜 더 긴 코드가 최적화일까?", 31).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–7: the compact source loop.
        self.copy("네 번의 곱셈과 덧셈", "소스에는 짧은 for문 하나")
        code = code_lines((
            "float sum = 0.0f;",
            "for (int k = 0; k < 4; ++k)",
            "    sum += a[k] * b[k];",
        ), 27).move_to([0, .55, 0])
        loop_frame = SurroundingRectangle(code[1:], color=ACCENT,
                                          buff=.14, corner_radius=.18)
        self.show(VGroup(code, loop_frame,
                         label("4 iterations", 24, ACCENT)
                         .next_to(code, DOWN, buff=.55)))
        self.to(7)

        # 7–15: loop-carried control flow exists alongside the math.
        self.copy("반복에는 제어 흐름도 있습니다", "k 증가 · 조건 검사 · 다음 반복")
        names = ("k = 0", "계산", "k++", "k < 4 ?")
        colors = (WEIGHT, GOOD, ACCENT, PRUNE)
        nodes = VGroup(*[card(n, c, 3.4, .82, 26)
                         for n, c in zip(names, colors)])
        nodes.arrange(DOWN, buff=.42).move_to([0, .25, 0])
        links = VGroup(*[arrow(nodes[i].get_bottom(), nodes[i+1].get_top())
                         for i in range(3)])
        back = CurvedArrow(nodes[3].get_right(), nodes[1].get_right(),
                           angle=PI/2, color=PRUNE, stroke_width=2.7,
                           tip_length=.15)
        self.show(VGroup(nodes, links, back))
        self.to(15)

        # 15–22: materialize all four iterations.
        self.copy("반복 횟수를 알면 펼칠 수 있습니다", "Loop Unrolling")
        short = card("for (k = 0; k < 4; ++k)", WEIGHT,
                     6.3, .85, 25).move_to([0, 2.6, 0])
        rows = code_lines(tuple(f"sum += a[{k}] * b[{k}];" for k in range(4)),
                          27, GOOD).move_to([0, -.9, 0])
        self.show(VGroup(short, rows,
                         arrow(short.get_bottom(), rows.get_top(), ACCENT),
                         label("4개의 계산이 드러남", 23, ACCENT)
                         .next_to(rows, DOWN, buff=.45)))
        self.play(Indicate(rows, color=GOOD, scale_factor=1.02), run_time=.8)
        self.to(22)

        # 22–29: generated code gets longer.
        self.copy("생성 코드는 오히려 길어집니다", "짧은 소스  →  더 긴 실행 코드")
        left = VGroup(
            label("SOURCE", 23, WEIGHT),
            card("for (...) { ... }", WEIGHT, 3.2, 1.1, 24),
            label("1개의 루프 구조", 21, MUTED),
        ).arrange(DOWN, buff=.48).move_to([-2.0, .2, 0])
        right = VGroup(
            label("UNROLLED", 23, GOOD),
            *[card(f"a[{i}] * b[{i}]", GOOD, 3.2, .6, 21)
              for i in range(4)],
            label("4개의 본문", 21, MUTED),
        ).arrange(DOWN, buff=.26).move_to([2.0, .2, 0])
        self.show(VGroup(left, right,
                         Line([0, 2.8, 0], [0, -3.0, 0],
                              color=MUTED, stroke_opacity=.3)))
        self.to(29)

        # 29–39: control overhead is one gain; wider visibility is the focus.
        self.copy("왜 길게 만드는 게 유리할까?", "제어 감소 + 더 넓은 최적화 범위")
        control = VGroup(
            card("계산", WEIGHT, 2.25),
            card("compare", PRUNE, 2.25),
            card("branch", PRUNE, 2.25),
            card("계산", WEIGHT, 2.25),
        ).arrange(DOWN, buff=.2).move_to([-2.05, .0, 0])
        exposed = VGroup(*[card(f"계산 {i}", GOOD, 2.25)
                           for i in range(4)])
        exposed.arrange(DOWN, buff=.2).move_to([2.05, .0, 0])
        headings = VGroup(label("LOOP CONTROL", 22, PRUNE)
                          .next_to(control, UP, buff=.35),
                          label("EXPOSED WORK", 22, GOOD)
                          .next_to(exposed, UP, buff=.35))
        self.show(VGroup(control, exposed, headings))
        self.to(39)

        # 39–51: four products are independent, while sum is a chain.
        self.copy("여러 연산이 한꺼번에 보입니다", "독립적인 곱셈 · 누적에는 의존성")
        products = VGroup(*[card(f"a{i} × b{i}", ACCENT, 1.62, .85, 24)
                            for i in range(4)])
        products.arrange(RIGHT, buff=.27).move_to([0, 1.5, 0])
        independent = label("Independent products", 24, ACCENT)
        independent.move_to([0, 2.65, 0])
        chain = VGroup(*[card(f"sum {i}", GOOD, 1.55, .72, 20)
                         for i in range(4)])
        chain.arrange(RIGHT, buff=.38).move_to([0, -1.55, 0])
        chain_arrows = VGroup(*[arrow(chain[i].get_right(),
                                       chain[i+1].get_left(), GOOD)
                                 for i in range(3)])
        self.show(VGroup(products, independent, chain, chain_arrows,
                         label("sum은 순서대로 누적", 22, GOOD)
                         .move_to([0, -2.7, 0])))
        self.play(Indicate(products, color=ACCENT, scale_factor=1.03),
                  run_time=.8)
        self.to(51)

        # 51–64: unrolling exposes each multiply-add for possible FMA contraction.
        self.copy("1화의 FMA도 다시 등장합니다", "Unrolling  →  조건부 FMA contraction")
        top = card("for loop", WEIGHT, 3.2, .75, 25)
        top.move_to([0, 3.2, 0])
        expressions = VGroup(*[card(f"sum + a{i}×b{i}", ACCENT,
                                    1.7, .8, 19) for i in range(4)])
        expressions.arrange(RIGHT, buff=.23).move_to([0, .65, 0])
        fmas = VGroup(*[card("FMA", GOOD, 1.7, .8, 24)
                        for _ in range(4)])
        fmas.arrange(RIGHT, buff=.23).move_to([0, -2.0, 0])
        self.show(VGroup(top, expressions, fmas,
                         arrow(top.get_bottom(), [0, 1.2, 0], ACCENT),
                         label("Unrolling", 22, ACCENT)
                         .move_to([2.4, 2.05, 0]),
                         arrow([0, .05, 0], [0, -1.4, 0], GOOD),
                         label("Contraction?", 22, GOOD)
                         .move_to([2.4, -.68, 0]),
                         label("FMA 누적 순서는 유지", 20, MUTED)
                         .move_to([0, -3.1, 0])))
        self.to(64)

        # 64–75: unrolling spends code size and may increase register pressure.
        self.copy("많이 펼칠수록 항상 좋지는 않습니다", "긴 루프: 코드 크기 ↑  ·  레지스터 압박 가능")
        factors = VGroup(*[card(x, c, 1.55, .8, 23) for x, c in
                           zip(("1×", "2×", "4×", "8×"),
                               (WEIGHT, GOOD, ACCENT, PRUNE))])
        factors.arrange(RIGHT, buff=.3).move_to([0, 2.05, 0])
        costs = VGroup(
            card("CODE SIZE  ↑", PRUNE, 5.1, .9, 25),
            card("REGISTERS  ↑  ?", ACCENT, 5.1, .9, 25),
            label("중간 값을 더 오래 보관할 수도 있음", 22, MUTED),
        ).arrange(DOWN, buff=.38).move_to([0, -.95, 0])
        self.show(VGroup(factors, costs,
                         arrow([0, 1.48, 0], [0, .25, 0], PRUNE)))
        self.to(75)

        # 75–84: illustrative non-monotonic performance curve.
        self.copy("얼마나 펼치는 것이 유리할까?", "실제 GPU에서 확인해야 합니다")
        x_axis = Line([-2.9, -2.25, 0], [3.2, -2.25, 0],
                      color=MUTED, stroke_width=2)
        y_axis = Line([-2.9, -2.25, 0], [-2.9, 2.25, 0],
                      color=MUTED, stroke_width=2)
        coords = [(-2.3, -1.05, 0), (-.55, .45, 0),
                  (1.15, 1.45, 0), (2.8, .4, 0)]
        curve = VMobject(color=GOOD, stroke_width=4)
        curve.set_points_smoothly(coords)
        dots = VGroup(*[Dot(p, radius=.09, color=ACCENT) for p in coords])
        ticks = VGroup(*[label(f"{n}×", 20, MUTED)
                         .move_to([p[0], -2.7, 0])
                         for n, p in zip((1, 2, 4, 8), coords)])
        graph = VGroup(x_axis, y_axis, curve, dots, ticks,
                       label("상대 성능", 21, MUTED)
                       .move_to([-2.9, 2.65, 0]),
                       label("긴 루프의 펼침 계수", 21, MUTED)
                       .move_to([2.5, -3.25, 0]),
                       label("개념도 · 측정값 아님", 20, ACCENT)
                       .move_to([0, 3.35, 0]))
        self.show(graph)
        self.to(84)

    def copy(self, heading, note):
        old = VGroup(self.heading, self.note)
        if len(old):
            self.play(FadeOut(old), run_time=.15)
        self.heading = label(heading, 30).move_to(UP * 5.12)
        self.note = label(note, 22, ACCENT).move_to(DOWN * 4.8)
        self.play(FadeIn(self.heading), FadeIn(self.note), run_time=.32)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.3)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.65)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
