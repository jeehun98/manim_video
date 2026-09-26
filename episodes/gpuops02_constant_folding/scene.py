"""GPU operations 02: a compile-time constant expression disappears."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)


def label(text, size=27, color=INK, width=7.6):
    return txt(text, size, color, width)


def card(text, color=WEIGHT, width=3.0, height=.9, size=26):
    box = RoundedRectangle(width=width, height=height, corner_radius=.16,
                           stroke_color=color, stroke_width=2.1,
                           fill_color=color, fill_opacity=.09)
    return VGroup(box, label(text, size, color, width - .18))


def arrow(start, end, color=MUTED):
    return Arrow(start, end, buff=.07, color=color, stroke_width=3,
                 tip_length=.16)


class GPUConstantFolding(Scene):
    DURATION = 90

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  02", 20, MUTED).move_to(UP * 7.3),
            label("GPU가 계산하기 전에 끝난 계산", 31).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–6: a CUDA source expression with its literal multiplication highlighted.
        self.copy("아주 간단한 곱셈을 넣어봅니다", "CUDA kernel  ·  2.0f * 3.0f")
        code = self.code_line(False).move_to([0, 1.1, 0])
        marker = label("두 값이 모두 숫자", 25, ACCENT).move_to([0, -.65, 0])
        self.show(VGroup(code, marker))
        self.play(Indicate(code[1], color=ACCENT, scale_factor=1.06),
                  run_time=.8)
        self.to(6)

        # 6–13: the intuitive runtime path.
        self.copy("실행할 때마다 2 × 3을 계산할까요?", "예상: GPU가 곱셈 후 덧셈")
        x = card("x[i]", WEIGHT, 2.3).move_to([-2.1, 1.7, 0])
        multiply = card("2 × 3", ACCENT, 2.3).move_to([2.0, 1.7, 0])
        six = card("6", ACCENT, 1.6, .8, 30).move_to([2.0, -.15, 0])
        add = card("x[i] + 6", GOOD, 3.5, 1.0).move_to([0, -2.1, 0])
        paths = VGroup(arrow(multiply.get_bottom(), six.get_top(), ACCENT),
                       arrow(x.get_bottom(), add.get_top() + LEFT * .8, WEIGHT),
                       arrow(six.get_bottom(), add.get_top() + RIGHT * .8, ACCENT))
        self.show(VGroup(x, multiply, six, add, paths))
        self.to(13)

        # 13–19: remove the suspected runtime multiplication.
        self.copy("곱셈이 GPU까지 오지 않을 수 있습니다", "2 × 3  →  6.0f")
        old = card("2.0f * 3.0f", PRUNE, 4.4, 1.0, 29).move_to([0, 1.1, 0])
        strike = Line([-2.25, .45, 0], [2.25, 1.75, 0],
                      color=PRUNE, stroke_width=6)
        new = card("6.0f", GOOD, 2.5, 1.05, 35).move_to([0, -1.7, 0])
        self.show(VGroup(old, strike, new,
                         arrow([0, .25, 0], [0, -1.05, 0], GOOD)))
        self.to(19)

        # 19–30: the actual constant-folding rewrite.
        self.copy("값을 미리 알면 식을 접을 수 있습니다", "Constant Folding")
        before = card("x[i] + (2.0f * 3.0f)", WEIGHT, 6.8, 1.15, 29)
        before.move_to([0, 2.2, 0])
        compiler = card("Compiler", SPARSE, 3.3, .95).move_to([0, .15, 0])
        after = card("x[i] + 6.0f", GOOD, 5.1, 1.15, 31).move_to([0, -2.1, 0])
        self.show(VGroup(before, compiler, after,
                         arrow(before.get_bottom(), compiler.get_top(), SPARSE),
                         arrow(compiler.get_bottom(), after.get_top(), GOOD)))
        self.play(Indicate(after, color=GOOD, scale_factor=1.05), run_time=.7)
        self.to(30)

        # 30–38: connect to episode 1 without losing the distinction.
        self.copy("1화에서는 변형, 이번에는 제거", "실행할 연산의 수가 달라짐")
        fma = VGroup(label("01  FMA", 25, GOOD),
                     card("a*b+c", WEIGHT, 3.0),
                     label("↓", 30, MUTED),
                     card("FMA", GOOD, 3.0))
        folding = VGroup(label("02  Constant Folding", 25, ACCENT),
                         card("2.0f*3.0f", WEIGHT, 3.0),
                         label("↓", 30, MUTED),
                         card("6.0f", ACCENT, 3.0))
        for col in (fma, folding):
            col.arrange(DOWN, buff=.4)
        fma.move_to([-2.0, .1, 0]); folding.move_to([2.0, .1, 0])
        divider = Line([0, 2.9, 0], [0, -3.0, 0], color=MUTED,
                       stroke_opacity=.3)
        self.show(VGroup(fma, folding, divider))
        self.to(38)

        # 38–44: central mystery.
        self.copy("GPU에서 사라진 계산은 누가 했을까?", "2 × 3 = 6  ·  계산의 장소는?")
        question = label("2 × 3", 60, ACCENT).move_to([0, 1.35, 0])
        who = label("누가 계산했을까?", 39, INK).move_to([0, -1.1, 0])
        self.show(VGroup(question, who))
        self.to(44)

        # 44–59: offline nvcc compilation is a host-side program.
        self.copy("nvcc는 호스트에서 실행됩니다", "CPU에서 코드를 분석하고 GPU용 코드를 생성")
        pc = card("HOST  /  CPU", WEIGHT, 5.6, .9, 25).move_to([0, 3.0, 0])
        source = card("kernel.cu", INK, 3.7, .8).move_to([0, 1.45, 0])
        tool = card("nvcc  /  Compiler", SPARSE, 4.5, .95).move_to([0, -.25, 0])
        optimized = card("optimized GPU code", GOOD, 5.4, .9, 24)
        optimized.move_to([0, -2.3, 0])
        hint = label("상수식  2 × 3 → 6", 22, ACCENT).next_to(tool, RIGHT, buff=.15)
        if hint.get_right()[0] > 4.1:
            hint.move_to([0, -1.17, 0])
        self.show(VGroup(pc, source, tool, optimized, hint,
                         arrow(source.get_bottom(), tool.get_top(), SPARSE),
                         arrow(tool.get_bottom(), optimized.get_top(), GOOD)))
        self.to(59)

        # 59–68: the key compile-time / runtime split.
        self.copy("계산이 끝나는 시점이 다릅니다", "컴파일할 때  →  커널을 실행할 때")
        split = Line([-3.8, -.12, 0], [3.8, -.12, 0],
                     color=MUTED, stroke_opacity=.55)
        top = VGroup(
            label("COMPILE TIME  /  CPU", 26, ACCENT).move_to([0, 3.45, 0]),
            card("2 × 3", ACCENT, 2.5, .8).move_to([0, 2.1, 0]),
            label("↓", 27, MUTED).move_to([0, 1.45, 0]),
            card("6.0f", GOOD, 2.5, .8).move_to([0, .82, 0]),
        )
        bottom = VGroup(
            label("RUNTIME  /  GPU", 26, WEIGHT).move_to([0, -.75, 0]),
            card("out[i] = x[i] + 6.0f;", GOOD, 6.6, 1.05, 25)
            .move_to([0, -2.35, 0]),
        )
        self.show(VGroup(split, top, bottom,
                         arrow([0, .37, 0], [0, -1.55, 0], SPARSE)))
        self.to(68)

        # 68–78: where the compile-time boundary ends.
        self.copy("CPU가 x[i]까지 계산하는 것은 아닙니다", "상수는 미리 · 입력 데이터는 실행 때")
        known = VGroup(
            card("2.0f * 3.0f", ACCENT, 3.25, .85, 24),
            label("두 값이 이미 알려짐", 22, ACCENT, 3.2),
            card("compile time 가능", GOOD, 3.25, .75, 20),
        ).arrange(DOWN, buff=.33).move_to([-2.0, .15, 0])
        unknown = VGroup(
            card("x[i] * 3.0f", WEIGHT, 3.25, .85, 24),
            label("x[i]는 실행 때 알게 됨", 22, WEIGHT, 3.25),
            card("runtime 필요", PRUNE, 3.25, .75, 20),
        ).arrange(DOWN, buff=.33).move_to([2.0, .15, 0])
        self.show(VGroup(known, unknown,
                         Line([0, 2.3, 0], [0, -2.2, 0], color=MUTED,
                              stroke_opacity=.3)))
        self.to(78)

        # 78–84: one compile-time computation for many launches.
        self.copy("커널을 몇 번 실행해도", "상수 곱셈을 다시 할 필요는 없습니다")
        compile_box = card("COMPILE TIME  ·  2 × 3 → 6", ACCENT,
                           6.6, 1.0, 25).move_to([0, 2.1, 0])
        launch = VGroup(*[card(x, GOOD, 1.9, .9, 25) for x in
                          ("×1", "×1,000", "×1,000,000")])
        launch.arrange(RIGHT, buff=.35).move_to([0, -1.2, 0])
        self.show(VGroup(compile_box, launch,
                         arrow(compile_box.get_bottom(), [0, -.45, 0], SPARSE),
                         label("RUNTIME  /  GPU", 23, WEIGHT)
                         .move_to([0, -2.65, 0])))
        self.to(84)

        # 84–90: close on time-shifting work out of execution.
        self.copy("미리 할 수 있는 일은 미리 합니다", "Compile Time  →  Runtime")
        left = card("COMPILE TIME", ACCENT, 3.25, 1.05, 24)
        right = card("RUNTIME", GOOD, 3.25, 1.05, 24)
        left.move_to([-2.0, 1.1, 0]); right.move_to([2.0, 1.1, 0])
        finish = label("실행 전에 끝낼 수 있는 계산", 30, INK)
        finish.move_to([0, -1.45, 0])
        self.show(VGroup(left, right, finish,
                         arrow(left.get_right(), right.get_left(), SPARSE)))
        self.to(90)

    def code_line(self, folded):
        if folded:
            pieces = (("out[i] = x[i] + ", INK), ("6.0f", GOOD), (";", INK))
        else:
            pieces = (("out[i] = x[i] + (", INK),
                      ("2.0f * 3.0f", ACCENT), (");", INK))
        group = VGroup(*[label(part, 27, color) for part, color in pieces])
        group.arrange(RIGHT, buff=.02)
        group.scale_to_fit_width(min(group.width, 7.4))
        return group

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
