"""GPU operations 01: source multiply/add can contract into FMA."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (  # reuse the current vertical series palette
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


def label(text, size=26, color=INK, width=7.6):
    return txt(text, size, color, width)


def card(text, color=WEIGHT, width=2.35, height=.95, size=27):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.17,
        stroke_color=color, stroke_width=2.2,
        fill_color=color, fill_opacity=.10,
    )
    return VGroup(box, label(text, size, color, width - .2))


def down_arrow(start, end, color=MUTED):
    return Arrow(start, end, buff=.06, color=color, stroke_width=3,
                 tip_length=.17)


class GPUFMAIntroduction(Scene):
    DURATION = 73

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.sub = VGroup()
        self.note = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  01", 20, MUTED).move_to(UP * 7.3),
            label("내가 쓴 a*b+c가 그대로 실행될까?", 31).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–6: code, with the two source operators colored independently.
        self.copy("CUDA kernel에는 두 연산이 보입니다", "곱셈 한 번 · 덧셈 한 번")
        source = self.code_line().move_to([0, 1.1, 0])
        mul_tag = label("MUL ?", 22, ACCENT).move_to([-.6, -.25, 0])
        add_tag = label("ADD ?", 22, GOOD).move_to([1.5, -.25, 0])
        self.show(VGroup(source, mul_tag, add_tag))
        self.play(Indicate(source[1], color=ACCENT),
                  Indicate(source[3], color=GOOD), run_time=.9)
        self.to(6)

        # 6–12: set up the plausible, but not guaranteed, execution path.
        self.copy("GPU도 정말 이 순서대로 실행할까요?", "소스의 연산자 2개 → 명령 2개?")
        formula = label("a × b + c", 42, INK).move_to([0, 2.55, 0])
        mul = card("MUL", ACCENT).move_to([0, .8, 0])
        add = card("ADD", GOOD).move_to([0, -1.25, 0])
        chain = VGroup(formula, mul, add,
                       down_arrow([0, 2.05, 0], [0, 1.34, 0]),
                       down_arrow([0, .25, 0], [0, -.7, 0]))
        self.show(chain)
        self.to(12)

        # 12–20: compiler contraction is the first reversal.
        self.copy("조건이 맞으면 하나로 합쳐집니다", "MUL + ADD  →  FMA")
        compiler = card("Compiler", SPARSE, 3.4, 1.0).move_to([0, -.25, 0])
        fused = card("FMA", GOOD, 3.1, 1.15, 36).move_to([0, -2.55, 0])
        before = VGroup(card("MUL", ACCENT, 2.15).move_to([-1.35, 2.0, 0]),
                        card("ADD", GOOD, 2.15).move_to([1.35, 2.0, 0]))
        arrows = VGroup(
            down_arrow([-1.3, 1.45, 0], [-.65, .35, 0], SPARSE),
            down_arrow([1.3, 1.45, 0], [.65, .35, 0], SPARSE),
            down_arrow([0, -.8, 0], [0, -1.9, 0], GOOD),
        )
        self.show(VGroup(before, compiler, fused, arrows))
        self.play(Indicate(fused, color=GOOD, scale_factor=1.08), run_time=.7)
        self.to(20)

        # 20–27: define the operation without promising a speedup.
        self.copy("FMA = Fused Multiply-Add", "세 입력 · 한 번의 fused 연산")
        inputs = VGroup(*[card(x, c, 1.35, .85, 30) for x, c in
                          zip(("a", "b", "c"), (ACCENT, ACCENT, WEIGHT))])
        inputs.arrange(RIGHT, buff=.48).move_to([0, 2.3, 0])
        core = card("FMA", GOOD, 3.1, 1.2, 38).move_to([0, .15, 0])
        output = label("a × b + c", 39, INK).move_to([0, -2.15, 0])
        arr = VGroup(*[down_arrow(x.get_bottom(),
                                  core.get_top() + RIGHT * dx, GOOD)
                       for x, dx in zip(inputs, (-.65, 0, .65))],
                     down_arrow(core.get_bottom(), output.get_top(), GOOD))
        self.show(VGroup(inputs, core, output, arr))
        self.to(27)

        # 27–38: the second reversal is floating-point semantics.
        self.copy("반올림 위치도 달라집니다", "float: 결과가 달라질 수 있음")
        left = self.rounding_column("MUL + ADD", ACCENT, True).move_to([-2.0, .05, 0])
        right = self.rounding_column("FMA", GOOD, False).move_to([2.0, .05, 0])
        divider = Line([0, 3.1, 0], [0, -3.25, 0], color=MUTED,
                       stroke_opacity=.3)
        self.show(VGroup(left, right, divider))
        self.play(Indicate(left[-1], color=ACCENT),
                  Indicate(right[-1], color=GOOD), run_time=.9)
        self.to(38)

        # 38–44: return to the unmodified source expression.
        self.copy("하지만 FMA는 쓰지 않았습니다", "FMA는 어디서 생겼을까?")
        code = self.code_line().move_to([0, 1.25, 0])
        mystery = label("FMA  ?", 48, GOOD).move_to([0, -1.3, 0])
        self.show(VGroup(code, mystery))
        self.to(44)

        # 44–51: one brief view of the compilation layers.
        self.copy("CUDA source는 실행 코드가 아닙니다", "Compiler를 거쳐 GPU 명령으로")
        names = ("CUDA Source", "Compiler", "PTX", "Machine Code", "GPU")
        colors = (WEIGHT, SPARSE, ACCENT, GOOD, WEIGHT)
        widths = (4.0, 3.2, 2.2, 4.0, 2.1)
        boxes = VGroup(*[card(n, c, w, .74, 22)
                         for n, c, w in zip(names, colors, widths)])
        boxes.arrange(DOWN, buff=.42).move_to([0, .05, 0])
        links = VGroup(*[down_arrow(boxes[i].get_bottom(), boxes[i + 1].get_top())
                         for i in range(4)])
        self.show(VGroup(boxes, links))
        self.play(Indicate(boxes[1], color=SPARSE, scale_factor=1.08), run_time=.65)
        self.to(51)

        # 51–59: revisit contraction within the compiler.
        self.copy("Compiler는 계산의 연결을 봅니다", "조건이 허용되면 FMA contraction")
        graph = VGroup(
            card("MUL", ACCENT, 2.3).move_to([0, 2.1, 0]),
            card("ADD", GOOD, 2.3).move_to([0, .35, 0]),
            down_arrow([0, 1.55, 0], [0, .9, 0]),
        )
        frame = SurroundingRectangle(graph, color=SPARSE, buff=.38,
                                     corner_radius=.2)
        result = card("FMA", GOOD, 3.0, 1.08, 35).move_to([0, -2.7, 0])
        self.show(VGroup(graph, frame, result,
                         down_arrow([0, -.62, 0], [0, -2.08, 0], GOOD)))
        self.to(59)

        # 59–66: show the broader menu without explaining each one.
        self.copy("Compiler Optimization", "FMA는 변환의 한 예입니다")
        center = card("Compiler", SPARSE, 3.3, 1.05).move_to([0, 1.8, 0])
        ops = VGroup(*[
            card("FMA contraction", GOOD, 5.5, .64, 20),
            card("Inlining", WEIGHT, 5.5, .64, 20),
            card("Dead Code Elimination", PRUNE, 5.5, .64, 20),
            card("Constant Folding", ACCENT, 5.5, .64, 20),
            card("Loop Unrolling", SPARSE, 5.5, .64, 20),
        ]).arrange(DOWN, buff=.17).move_to([0, -1.15, 0])
        self.show(VGroup(center, ops,
                         down_arrow(center.get_bottom(), ops.get_top())))
        self.to(66)

        # 66–73: seven-second series question.
        self.copy("Source Code ≠ Executed Instructions",
                  "컴파일러는 코드를 어디까지 바꿀 수 있을까?")
        source_box = card("우리가 작성한 코드", WEIGHT, 5.1, .93, 25).move_to([0, 2.3, 0])
        compiler_box = card("Compiler", SPARSE, 3.8, 1.1, 30).move_to([0, .35, 0])
        items = VGroup(*[card(x, c, 1.55, .73, 19) for x, c in
                         zip(("FMA", "Inlining", "DCE", "Unrolling"),
                             (GOOD, WEIGHT, PRUNE, ACCENT))])
        items.arrange(RIGHT, buff=.29).move_to([0, -2.2, 0])
        branches = VGroup(*[
            down_arrow(compiler_box.get_bottom(), box.get_top(), box[0].get_stroke_color())
            for box in items
        ])
        self.show(VGroup(source_box, compiler_box, items, branches,
                         down_arrow(source_box.get_bottom(), compiler_box.get_top())))
        self.to(73)

    def code_line(self):
        parts = VGroup(*[
            label("out[i] = a[i]", 27),
            label("*", 31, ACCENT),
            label("b[i]", 27),
            label("+", 31, GOOD),
            label("c[i];", 27),
        ])
        parts.arrange(RIGHT, buff=.08)
        parts.scale_to_fit_width(min(parts.width, 7.4))
        return parts

    def rounding_column(self, title, color, separate):
        lines = (["a × b", "round", "+ c", "round"] if separate
                 else ["a × b", "+ c", "round"])
        nodes = VGroup(*[card(x, color if x == "round" else MUTED,
                              2.9, .72, 23) for x in lines])
        nodes.arrange(DOWN, buff=.38)
        arrows = VGroup(*[down_arrow(nodes[i].get_bottom(), nodes[i+1].get_top(),
                                     color) for i in range(len(nodes)-1)])
        head = label(title, 26, color, 3.4).next_to(nodes, UP, buff=.5)
        return VGroup(head, nodes, arrows,
                      label("2 rounds" if separate else "1 round", 22, color)
                      .next_to(nodes, DOWN, buff=.45))

    def copy(self, heading, subtitle):
        old = VGroup(self.head, self.sub, self.note)
        if len(old):
            self.play(FadeOut(old), run_time=.15)
        self.head = label(heading, 30).move_to(UP * 5.12)
        self.note = label(subtitle, 22, ACCENT).move_to(DOWN * 4.8)
        self.sub = VGroup()  # reserve lower area for separately muxed SRT
        self.play(FadeIn(self.head), FadeIn(self.note), run_time=.32)

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
