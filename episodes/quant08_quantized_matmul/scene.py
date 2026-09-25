"""Quantization 08: move the core matrix multiplication into integers."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.quant_series.visuals import (
    ERROR, GOOD, GRID, INK, MUTED, SNAP, VALUE, pill, txt,
)


class QuantizedMatMul(Scene):
    DURATION = 60

    def construct(self):
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.chrome = VGroup(
            txt("QUANTIZATION  /  08", 20, MUTED).move_to(UP * 7.25),
            txt("Quantized 모델은 행렬곱을 어떻게 계산할까?", 30).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED,
                 stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=SNAP,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0–7 s — hook: a familiar floating-point matrix multiplication.
        self.text(
            "Quantization 뒤에도 핵심 연산은 행렬곱입니다",
            "소수로 이루어진 W와 X를 곱하던 계산은\n실제로 어떻게 정수 연산으로 바뀔까요?",
            "Y = W X",
        )
        w_float = self.matrix_card("W", [["0.42", "−0.81"],
                                          ["0.17", "0.63"]], VALUE)
        x_float = self.matrix_card("X", [["0.54"], ["−0.28"]], GRID)
        equals = txt("×", 38, MUTED)
        y_label = pill("Y", SNAP, 1.05)
        hook = VGroup(w_float, equals, x_float, txt("→", 32, MUTED), y_label)
        hook.arrange(RIGHT, buff=.28).move_to([0, .15, 0])
        self.play(FadeIn(w_float), FadeIn(equals), FadeIn(x_float), run_time=.65)
        self.play(FadeIn(hook[3], shift=RIGHT * .08),
                  FadeIn(y_label, scale=.8), run_time=.55)
        self.keep_stage(hook)
        self.play(Indicate(VGroup(w_float, x_float), color=SNAP,
                           scale_factor=1.04), run_time=.65)
        self.to(7)

        # 7–16 s — decompose W into an integer matrix and one scale.
        self.text(
            "Weight를 정수 행렬과 scale로 나눕니다",
            "실수 W를 작은 정수 Q_w와 scale s_w의 곱으로 근사하면\n행렬에는 정수만 남고 실제 크기는 scale이 기억합니다.",
            "W  ≈  s_w · Q_w          where  s_w = 0.02",
        )
        w_source = self.matrix_card("W", [["0.42", "−0.81"],
                                           ["0.17", "0.63"]], VALUE)
        qw = self.matrix_card("Q_w", [["21", "−40"], ["8", "31"]], SNAP)
        scale_w = self.scale_card("s_w", "0.02", GOOD)
        weight_row = VGroup(w_source, txt("≈", 38, MUTED), scale_w,
                            txt("×", 32, MUTED), qw)
        weight_row.arrange(RIGHT, buff=.2).scale(.88).move_to([0, .2, 0])
        self.play(FadeOut(hook), FadeIn(w_source), run_time=.45)
        self.play(FadeIn(weight_row[1:]), run_time=.75)
        self.keep_stage(weight_row)
        self.play(Indicate(qw, color=SNAP, scale_factor=1.05),
                  Indicate(scale_w, color=GOOD, scale_factor=1.05), run_time=.75)
        self.to(16)

        # 16–23 s — decompose X the same way.
        self.text(
            "Input도 같은 방식으로 표현할 수 있습니다",
            "X 역시 정수 Q_x와 별도의 scale s_x로 나누면\n원래 행렬곱에 두 정수 표현을 대입할 수 있습니다.",
            "X  ≈  s_x · Q_x          where  s_x = 0.02",
        )
        x_source = self.matrix_card("X", [["0.54"], ["−0.28"]], GRID)
        qx = self.matrix_card("Q_x", [["27"], ["−14"]], SNAP)
        scale_x = self.scale_card("s_x", "0.02", GOOD)
        input_row = VGroup(x_source, txt("≈", 38, MUTED), scale_x,
                           txt("×", 32, MUTED), qx)
        input_row.arrange(RIGHT, buff=.25).move_to([0, .2, 0])
        self.play(FadeOut(weight_row), FadeIn(x_source), run_time=.45)
        self.play(FadeIn(input_row[1:]), run_time=.7)
        self.keep_stage(input_row)
        self.play(Indicate(qx, color=SNAP, scale_factor=1.05),
                  Indicate(scale_x, color=GOOD, scale_factor=1.05), run_time=.7)
        self.to(23)

        # 23–33 s — substitute and pull both scalar scales outside GEMM.
        self.text(
            "두 scale은 밖으로, 핵심 GEMM은 정수로",
            "W와 X의 표현을 대입하면 두 scale은 하나의 계수가 되고\n행렬끼리 곱하는 중심 계산은 Q_w Q_x로 남습니다.",
            "W X  ≈  (s_w Q_w)(s_x Q_x)  =  s_w s_x (Q_w Q_x)",
        )
        line1 = self.formula_card("W X", VALUE, 1.55)
        line2 = self.formula_card("(s_w Q_w) (s_x Q_x)", GRID, 4.25)
        line3 = self.formula_card("s_w s_x  ( Q_w Q_x )", SNAP, 4.35)
        formulas = VGroup(line1, txt("≈", 30, MUTED), line2,
                          txt("=", 30, MUTED), line3)
        formulas.arrange(DOWN, buff=.28).move_to([0, .35, 0])
        integer_focus = SurroundingRectangle(line3[1], color=SNAP,
                                             stroke_width=3, buff=.12)
        integer_label = txt("INTEGER GEMM", 19, SNAP).next_to(integer_focus, DOWN,
                                                               buff=.14)
        derivation = VGroup(formulas, integer_focus, integer_label)
        self.play(FadeOut(input_row), FadeIn(line1), run_time=.4)
        self.play(FadeIn(formulas[1]), TransformFromCopy(line1, line2), run_time=.65)
        self.play(FadeIn(formulas[3]), TransformFromCopy(line2, line3), run_time=.75)
        self.play(Create(integer_focus), FadeIn(integer_label), run_time=.5)
        self.keep_stage(derivation)
        self.play(Indicate(line3[1], color=SNAP, scale_factor=1.06), run_time=.7)
        self.to(33)

        # 33–43 s — do the integer products and apply the combined scale once.
        self.text(
            "실제 중심 계산에는 정수만 들어갑니다",
            "Q_w와 Q_x를 곱해 정수 누적값을 만든 뒤\ns_w s_x, 즉 0.0004를 한 번 적용해 실수 결과로 해석합니다.",
            "Q_w Q_x = [1127, −218]ᵀ      ·      s_w s_x = 0.0004",
        )
        qw_num = self.matrix_card("Q_w", [["21", "−40"], ["8", "31"]], SNAP)
        qx_num = self.matrix_card("Q_x", [["27"], ["−14"]], SNAP)
        acc = self.matrix_card("ACC", [["1127"], ["−218"]], GRID)
        integer_row = VGroup(qw_num, txt("×", 32, MUTED), qx_num,
                             txt("=", 32, MUTED), acc)
        integer_row.arrange(RIGHT, buff=.22).scale(.92).move_to([0, 1.05, 0])
        product_scale = self.scale_card("s_w · s_x", "0.0004", GOOD)
        output = self.matrix_card("Ŷ", [["0.4508"], ["−0.0872"]], VALUE)
        restore_row = VGroup(acc.copy(), txt("×", 30, MUTED), product_scale,
                             txt("=", 30, MUTED), output)
        restore_row.arrange(RIGHT, buff=.2).scale(.82).move_to([0, -1.25, 0])
        numeric = VGroup(integer_row, restore_row)
        self.play(FadeOut(derivation), FadeIn(qw_num), FadeIn(qx_num),
                  FadeIn(integer_row[1]), run_time=.55)
        self.play(FadeIn(integer_row[3]), FadeIn(acc, shift=RIGHT * .12), run_time=.6)
        self.play(TransformFromCopy(acc, restore_row[0]), FadeIn(restore_row[1:]),
                  run_time=.8)
        self.keep_stage(numeric)
        self.play(Indicate(product_scale, color=GOOD, scale_factor=1.07),
                  Indicate(output, color=VALUE, scale_factor=1.05), run_time=.75)
        self.to(43)

        # 43–51 s — hardware-facing pipeline, with integer GEMM at the center.
        self.text(
            "계산 경로의 중심이 Integer GEMM으로 이동합니다",
            "Quantized weight와 input으로 정수 곱셈과 덧셈을 수행하고\n누적이 끝난 뒤 scale을 적용해 출력의 실제 크기를 복원합니다.",
            "Q_w , Q_x  →  INTEGER GEMM  →  ACCUMULATOR  →  SCALE  →  Ŷ",
        )
        inputs = VGroup(pill("Q_w", SNAP, 1.25), pill("Q_x", SNAP, 1.25))
        inputs.arrange(DOWN, buff=.22)
        gemm = self.pipeline_box("INTEGER\nGEMM", SNAP, 1.75)
        accumulator = self.pipeline_box("ACC", GRID, 1.35)
        scale = self.pipeline_box("× SCALE", GOOD, 1.5)
        out = pill("Ŷ", VALUE, 1.0)
        blocks = VGroup(inputs, gemm, accumulator, scale, out)
        blocks.arrange(RIGHT, buff=.27).scale(.88).move_to([0, .3, 0])
        arrows = VGroup(*[
            Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=.05,
                  color=MUTED, stroke_width=2.5, tip_length=.1)
            for i in range(len(blocks) - 1)
        ])
        ops = VGroup(*[
            txt(op, 18, SNAP) for op in ("21×27", "−40×−14", "8×27", "31×−14")
        ]).arrange(DOWN, buff=.13).next_to(gemm, DOWN, buff=.42)
        pipeline = VGroup(blocks, arrows, ops)
        self.play(FadeOut(numeric), FadeIn(blocks),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.12),
                  run_time=.9)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * .05) for o in ops],
                              lag_ratio=.08), run_time=.55)
        self.keep_stage(pipeline)
        self.play(Indicate(gemm, color=SNAP, scale_factor=1.06), run_time=.7)
        self.to(51)

        # 51–56 s — approximation is introduced before GEMM, not by the identity.
        self.text(
            "같은 계산 경로지만 결과는 근사값입니다",
            "W와 X를 정수 격자에 맞출 때 이미 정보가 바뀌었으므로\n복원된 출력도 원래 실수 행렬곱과 완전히 같지는 않습니다.",
            "Y = [0.4536, −0.0846]ᵀ       ≈       Ŷ = [0.4508, −0.0872]ᵀ",
        )
        exact = self.result_card("FLOAT GEMM", ["0.4536", "−0.0846"], VALUE)
        approx = self.result_card("INTEGER GEMM + SCALE",
                                  ["0.4508", "−0.0872"], SNAP)
        comparison = VGroup(exact, txt("≈", 44, MUTED), approx)
        comparison.arrange(RIGHT, buff=.35).scale(.85).move_to([0, .25, 0])
        reason = pill("approximation entered during quantization", ERROR, 4.85)
        reason.move_to([0, -1.55, 0])
        approx_stage = VGroup(comparison, reason)
        self.play(FadeOut(pipeline), FadeIn(comparison), run_time=.7)
        self.play(FadeIn(reason, shift=UP * .1), run_time=.4)
        self.keep_stage(approx_stage)
        self.to(56)

        # 56–60 s — multiplication is INT8, but repeated sums need a wider range.
        self.text(
            "그런데 누적 결과도 INT8이면 괜찮을까?",
            "INT8끼리 곱해도 많은 결과를 계속 더하면 값은 커집니다.\n다음에는 accumulator가 더 높은 precision을 쓰는 이유를 봅니다.",
            "NEXT  ·  Why INT8 × INT8 accumulates into INT32",
        )
        additions = VGroup(*[
            txt(v, 28, SNAP if i < 4 else ERROR)
            for i, v in enumerate(("+567", "+560", "−434", "+216", "= 1127 …"))
        ]).arrange(DOWN, buff=.18, aligned_edge=RIGHT).move_to([0, .45, 0])
        question = VGroup(
            pill("INT8 × INT8", SNAP, 2.3), txt("→", 30, MUTED),
            pill("INT32 ACC ?", ERROR, 2.35),
        ).arrange(RIGHT, buff=.3).move_to([0, -1.45, 0])
        next_stage = VGroup(additions, question)
        self.play(FadeOut(approx_stage),
                  LaggedStart(*[FadeIn(v, shift=UP * .05) for v in additions],
                              lag_ratio=.08), run_time=.7)
        self.play(FadeIn(question), run_time=.4)
        self.keep_stage(next_stage)
        self.to(60)

    def matrix_card(self, name, rows, color):
        nrows, ncols = len(rows), len(rows[0])
        cell_w = .82 if ncols > 1 else 1.0
        cells = VGroup()
        for row in rows:
            for value in row:
                box = RoundedRectangle(width=cell_w, height=.62,
                                       corner_radius=.07, stroke_color=color,
                                       stroke_width=1.2, fill_color=color,
                                       fill_opacity=.08)
                cells.add(VGroup(box, txt(value, 20, color).move_to(box)))
        cells.arrange_in_grid(rows=nrows, cols=ncols, buff=(.08, .08))
        left = Line(cells.get_corner(UL) + LEFT * .12 + UP * .08,
                    cells.get_corner(DL) + LEFT * .12 + DOWN * .08,
                    color=color, stroke_width=2.4)
        right = Line(cells.get_corner(UR) + RIGHT * .12 + UP * .08,
                     cells.get_corner(DR) + RIGHT * .12 + DOWN * .08,
                     color=color, stroke_width=2.4)
        label = txt(name, 21, color).next_to(cells, UP, buff=.18)
        return VGroup(cells, left, right, label)

    def scale_card(self, symbol, value, color):
        box = RoundedRectangle(width=1.35, height=1.25, corner_radius=.15,
                               stroke_color=color, stroke_width=1.8,
                               fill_color=color, fill_opacity=.08)
        return VGroup(box,
                      txt(symbol, 19, MUTED).move_to(box.get_center() + UP * .25),
                      txt(value, 23, color).move_to(box.get_center() + DOWN * .25))

    def formula_card(self, formula, color, width):
        box = RoundedRectangle(width=width, height=.82, corner_radius=.14,
                               stroke_color=color, stroke_width=1.7,
                               fill_color=color, fill_opacity=.07)
        label = txt(formula, 25, color).move_to(box)
        return VGroup(box, label)

    def pipeline_box(self, label, color, width):
        box = RoundedRectangle(width=width, height=1.35, corner_radius=.16,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.09)
        return VGroup(box, txt(label, 19, color).move_to(box))

    def result_card(self, label, values, color):
        box = RoundedRectangle(width=2.8, height=2.0, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.07)
        return VGroup(
            box,
            txt(label, 17, MUTED, 2.5).move_to(box.get_center() + UP * .6),
            txt(values[0], 25, color).move_to(box.get_center() + UP * .08),
            txt(values[1], 25, color).move_to(box.get_center() + DOWN * .48),
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
