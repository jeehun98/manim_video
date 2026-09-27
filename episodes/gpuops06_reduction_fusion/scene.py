"""GPU operations 06: fuse elementwise production into parallel reduction state."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=2.7, height=.85, size=25, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.15,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .18))


def mini(value, color, width=1.35, height=.54, size=17):
    return card(value, color, width, height, size, .16)


def arrow(start, end, color=MUTED, width=2.7):
    return Arrow(start, end, buff=.06, color=color, stroke_width=width,
                 tip_length=.15)


class GPUReductionFusion(Scene):
    DURATION = 90

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("GPU OPERATIONS  /  06", 20, MUTED).move_to(UP * 7.3),
            label("여러 값이 필요한 연산도 합칠 수 있을까?", 30)
            .move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0],
                 color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–8: recall the single-value lifetime from epilogue fusion.
        self.copy(
            "이전 편: 값 하나를 계속 들고 갑니다", "ONE LIVE VALUE",
            "cᵢⱼ 하나를 놓지 않고 Bias와 ReLU에 전달했습니다.\n현재 값만 필요한 원소별 연산의 Fusion이었습니다.",
        )
        chain = self.horizontal_flow(
            ("cᵢⱼ", "+ Bias", "ReLU", "STORE"),
            (ACCENT, WEIGHT, GOOD, PRUNE),
            widths=(1.35, 1.55, 1.55, 1.65), height=.72,
        ).move_to([0, .6, 0])
        frame = SurroundingRectangle(chain, color=GOOD, buff=.5,
                                     corner_radius=.22)
        tag = label("same live value", 22, GOOD).next_to(frame, UP, buff=.38)
        self.show(VGroup(chain, frame, tag))
        self.to(8)

        # 8–14: ReLU remains elementwise, SUM introduces fan-in.
        self.copy(
            "이번에는 여러 결과가 만나야 합니다", "y = Σᵢ ReLU(xᵢ)",
            "각 xᵢ의 ReLU는 따로 계산할 수 있습니다.\n하지만 마지막 SUM은 모든 결과의 정보를 필요로 합니다.",
        )
        inputs = VGroup(*[
            mini(f"x{i}", WEIGHT, 1.1, .58, 19) for i in range(4)
        ]).arrange(DOWN, buff=.3).move_to([-2.8, .55, 0])
        relus = VGroup(*[
            mini("ReLU", GOOD, 1.35, .58, 18) for _ in range(4)
        ]).arrange(DOWN, buff=.3).move_to([-.55, .55, 0])
        results = VGroup(*[
            mini(f"r{i}", ACCENT, 1.05, .58, 19) for i in range(4)
        ]).arrange(DOWN, buff=.3).move_to([1.55, .55, 0])
        total = card("SUM", SPARSE, 1.65, 1.05, 29).move_to([3.15, .55, 0])
        links = VGroup(*[
            arrow(inputs[i].get_right(), relus[i].get_left(), GOOD, 1.8)
            for i in range(4)
        ], *[
            arrow(relus[i].get_right(), results[i].get_left(), ACCENT, 1.8)
            for i in range(4)
        ], *[
            arrow(results[i].get_right(), total.get_left() + UP * (.36 - i * .24),
                  SPARSE, 1.8)
            for i in range(4)
        ])
        self.show(VGroup(inputs, relus, results, total, links))
        self.to(14)

        # 14–22: one element is insufficient for the reduction result.
        self.copy(
            "원소 하나로는 최종 합을 결정할 수 없습니다", "one value  ≠  reduction result",
            "ReLU(x₂)는 x₂ 하나만 보면 됩니다.\nSUM에는 다른 ReLU 결과들도 함께 필요합니다.",
        )
        formula = label("y = Σᵢ ReLU(xᵢ)", 39).move_to([0, 2.9, 0])
        focus = card("x₂  →  ReLU  →  r₂", ACCENT, 4.4, .95, 27).move_to([0, .65, 0])
        question = label("y  =  ?", 47, PRUNE).move_to([0, -1.65, 0])
        missing = label("r₀, r₁, r₃, … 가 아직 필요", 21, MUTED).move_to([0, -2.65, 0])
        self.show(VGroup(formula, focus, question, missing))
        self.play(Indicate(question, color=PRUNE, scale_factor=1.06), run_time=.7)
        self.to(22)

        # 22–32: separated kernels materialize the full ReLU tensor.
        self.copy(
            "분리 실행은 중간 Tensor를 만듭니다", "ReLU Kernel  →  Tensor  →  Reduction Kernel",
            "ReLU 결과 전체를 Global Memory에 STORE합니다.\nReduction Kernel은 그 Tensor를 다시 LOAD합니다.",
        )
        relu_kernel = card("ReLU Kernel", GOOD, 3.2, .72, 22).move_to([0, 3.25, 0])
        tensor = card("R = [0, 2.1, 0, 3.4, …]", ACCENT, 5.6, .8, 23).move_to([0, 1.65, 0])
        store = mini("STORE", PRUNE, 2.1).move_to([0, .35, 0])
        memory = card("Global Memory", SPARSE, 3.9, .82, 23).move_to([0, -1.0, 0])
        load = mini("LOAD", WEIGHT, 2.1).move_to([0, -2.25, 0])
        reduce_kernel = card("Reduction Kernel", SPARSE, 3.7, .72, 21).move_to([0, -3.3, 0])
        flow = VGroup(relu_kernel, tensor, store, memory, load, reduce_kernel)
        links = VGroup(*[
            arrow(flow[i].get_bottom(), flow[i + 1].get_top(),
                  flow[i + 1][0].get_stroke_color(), 2.0)
            for i in range(len(flow) - 1)
        ])
        self.show(VGroup(flow, links))
        self.to(32)

        # 32–38: distinguish the disposable tensor from the required answer.
        self.copy(
            "최종 출력에 배열 자체가 필요할까요?", "need SUM  ·  not the full R tensor",
            "중간 배열 R은 계산 과정의 표현일 뿐입니다.\n최종적으로 필요한 정보는 모든 원소의 합입니다.",
        )
        tensor = card("R = [0, 2.1, 0, 3.4, …]", ACCENT, 6.1, 1.0, 25).move_to([0, 2.2, 0])
        cross = VGroup(
            Line([-2.9, 2.75, 0], [2.9, 1.65, 0], color=PRUNE, stroke_width=5),
            Line([-2.9, 1.65, 0], [2.9, 2.75, 0], color=PRUNE, stroke_width=5),
        )
        sum_expr = card("0 + 2.1 + 0 + 3.4 + …", GOOD, 6.2, .95, 27).move_to([0, -.25, 0])
        answer = card("SUM", SPARSE, 2.3, 1.0, 31).move_to([0, -2.45, 0])
        self.show(VGroup(tensor, cross, sum_expr, answer,
                         arrow(sum_expr.get_bottom(), answer.get_top(), GOOD)))
        self.to(38)

        # 38–46: update only the state as each result is produced.
        self.copy(
            "중간값 대신 partial state를 갱신", "state  ←  state + ReLU(xᵢ)",
            "ReLU 결과가 생기는 즉시 partial sum에 반영합니다.\n원소 배열을 보관하지 않고 필요한 상태만 남깁니다.",
        )
        values = VGroup(*[
            mini(x, c, 1.2, .58, 19) for x, c in
            zip(("+ 0", "+ 2.1", "+ 0", "+ 3.4"),
                (MUTED, ACCENT, MUTED, ACCENT))
        ]).arrange(RIGHT, buff=.42).move_to([0, 2.45, 0])
        states = VGroup(*[
            mini(x, GOOD, 1.25, .68, 21) for x in ("0", "0", "2.1", "2.1", "5.5")
        ]).arrange(RIGHT, buff=.3).move_to([0, -.25, 0])
        state_links = VGroup(*[
            arrow(states[i].get_right(), states[i + 1].get_left(), GOOD, 1.9)
            for i in range(len(states) - 1)
        ])
        updates = VGroup(*[
            arrow(values[i].get_bottom(),
                  (states[i + 1].get_top()), values[i][0].get_stroke_color(), 1.8)
            for i in range(4)
        ])
        tag = label("partial sum state", 24, GOOD).move_to([0, -1.8, 0])
        self.show(VGroup(values, states, state_links, updates, tag))
        self.to(46)

        # 46–55: parallel execution creates several partial states.
        self.copy(
            "GPU에서는 partial sum도 병렬로 만듭니다", "Thread groups  →  partial results",
            "여러 Thread가 동시에 ReLU 결과를 처리합니다.\n각 실행 그룹은 자신이 맡은 값들의 partial sum을 만듭니다.",
        )
        top_threads = VGroup(*[
            mini(f"T{i}", WEIGHT, 1.0, .55, 17) for i in range(4)
        ]).arrange(RIGHT, buff=.22).move_to([-1.25, 2.15, 0])
        bottom_threads = VGroup(*[
            mini(f"T{i}", WEIGHT, 1.0, .55, 17) for i in range(4, 8)
        ]).arrange(RIGHT, buff=.22).move_to([-1.25, -.8, 0])
        p0 = card("partial 0", GOOD, 2.1, .8, 24).move_to([2.75, 2.15, 0])
        p1 = card("partial 1", ACCENT, 2.1, .8, 24).move_to([2.75, -.8, 0])
        top_links = VGroup(*[
            arrow(t.get_right(), p0.get_left() + UP * (.3 - i * .2), GOOD, 1.6)
            for i, t in enumerate(top_threads)
        ])
        bottom_links = VGroup(*[
            arrow(t.get_right(), p1.get_left() + UP * (.3 - i * .2), ACCENT, 1.6)
            for i, t in enumerate(bottom_threads)
        ])
        groups = VGroup(
            SurroundingRectangle(top_threads, color=GOOD, buff=.25, corner_radius=.15),
            SurroundingRectangle(bottom_threads, color=ACCENT, buff=.25, corner_radius=.15),
        )
        self.show(VGroup(top_threads, bottom_threads, p0, p1,
                         top_links, bottom_links, groups))
        self.to(55)

        # 55–64: partial results merge through a tree.
        self.copy(
            "부분 결과를 다시 합치면 전체 결과", "parallel reduction tree",
            "SUM은 부분적으로 계산한 결과를 다시 합칠 수 있습니다.\npartial results를 merge해 final sum을 만듭니다.",
        )
        leaves = VGroup(*[
            mini(f"partial {i}", c, 1.55, .62, 18) for i, c in
            enumerate((GOOD, ACCENT, WEIGHT, SPARSE))
        ]).arrange(RIGHT, buff=.32).move_to([0, 2.65, 0])
        mid0 = card("p₀ + p₁", GOOD, 2.2, .75, 23).move_to([-1.75, .3, 0])
        mid1 = card("p₂ + p₃", SPARSE, 2.2, .75, 23).move_to([1.75, .3, 0])
        final = card("final SUM", ACCENT, 3.0, .9, 28).move_to([0, -2.3, 0])
        links = VGroup(
            arrow(leaves[0].get_bottom(), mid0.get_top() + LEFT * .45, GOOD, 2),
            arrow(leaves[1].get_bottom(), mid0.get_top() + RIGHT * .45, GOOD, 2),
            arrow(leaves[2].get_bottom(), mid1.get_top() + LEFT * .45, SPARSE, 2),
            arrow(leaves[3].get_bottom(), mid1.get_top() + RIGHT * .45, SPARSE, 2),
            arrow(mid0.get_bottom(), final.get_top() + LEFT * .5, ACCENT, 2.2),
            arrow(mid1.get_bottom(), final.get_top() + RIGHT * .5, ACCENT, 2.2),
        )
        equation = label("(a + b) + (c + d)", 23, MUTED).move_to([0, -3.4, 0])
        self.show(VGroup(leaves, mid0, mid1, final, links, equation))
        self.to(64)

        # 64–72: show the fused producer-to-state path.
        self.copy(
            "중간 Tensor 전체를 완성하지 않습니다", "produce  →  reduce state  →  result",
            "각 값은 생성되면서 작은 partial state로 축약됩니다.\n전체 ReLU Tensor의 materialization을 피할 수 있습니다.",
        )
        flow = self.horizontal_flow(
            ("xᵢ", "ReLU", "partial\nreduction", "result"),
            (WEIGHT, GOOD, SPARSE, ACCENT),
            widths=(1.2, 1.45, 2.15, 1.55), height=.78,
        ).move_to([0, 1.35, 0])
        tensor = card("[r₀, r₁, …, rₙ]", ZERO, 4.2, .82, 23).move_to([0, -1.6, 0])
        cross = VGroup(
            Line([-1.9, -2.05, 0], [1.9, -1.15, 0], color=PRUNE, stroke_width=5),
            Line([-1.9, -1.15, 0], [1.9, -2.05, 0], color=PRUNE, stroke_width=5),
        )
        self.show(VGroup(flow, tensor, cross,
                         label("no full intermediate tensor", 20, GOOD)
                         .move_to([0, -2.95, 0])))
        self.to(72)

        # 72–81: explicitly contrast the two fusion patterns.
        self.copy(
            "값 전달에서 상태 축약으로", "Epilogue Fusion  ↔  Reduction Fusion",
            "Epilogue는 live value를 그대로 다음 연산에 넘깁니다.\nReduction은 여러 값을 작은 partial state로 축약합니다.",
        )
        left_chain = VGroup(
            label("EPILOGUE", 21, GOOD),
            mini("value", ACCENT, 2.2),
            mini("next op", GOOD, 2.2),
            mini("next op", GOOD, 2.2),
        ).arrange(DOWN, buff=.35).move_to([-2.1, .35, 0])
        right_values = VGroup(*[
            mini(x, WEIGHT, .9, .5, 16) for x in ("v₀", "v₁", "v₂", "v₃")
        ]).arrange(RIGHT, buff=.15).move_to([2.1, 1.4, 0])
        state = card("partial state", SPARSE, 2.8, .8, 23).move_to([2.1, -.1, 0])
        merged = card("merge", ACCENT, 2.2, .72, 22).move_to([2.1, -1.75, 0])
        fan = VGroup(*[
            arrow(v.get_bottom(), state.get_top() + RIGHT * x, SPARSE, 1.7)
            for v, x in zip(right_values, (-.65, -.22, .22, .65))
        ])
        right_tag = label("REDUCTION", 21, SPARSE).move_to([2.1, 2.75, 0])
        divider = Line([0, 3.15, 0], [0, -3.15, 0], color=MUTED,
                       stroke_opacity=.3)
        self.show(VGroup(left_chain, right_values, state, merged, fan, right_tag,
                         arrow(state.get_bottom(), merged.get_top(), ACCENT), divider))
        self.to(81)

        # 81–90: generalize the state and leave Softmax as the next question.
        self.copy(
            "어떤 작은 상태로 모아 합칠 수 있을까?", "SUM  ·  MAX  ·  MIN  ·  Softmax ?",
            "SUM, MAX, MIN은 partial state를 다시 merge할 수 있습니다.\n더 복잡한 Softmax에는 어떤 상태가 필요할까요?",
        )
        states = VGroup(
            card("SUM\nstate: s", GOOD, 2.1, 1.1, 23),
            card("MAX\nstate: m", ACCENT, 2.1, 1.1, 23),
            card("MIN\nstate: m", WEIGHT, 2.1, 1.1, 23),
        ).arrange(RIGHT, buff=.42).move_to([0, 2.05, 0])
        merge = label("partial states  →  merge  →  result", 25, SPARSE)
        merge.move_to([0, .15, 0])
        softmax = card("Softmax  ?", PRUNE, 3.8, 1.0, 31).move_to([0, -1.85, 0])
        fp_note = label(
            "※ float SUM은 reduction 순서에 따라 반올림 결과가 달라질 수 있음",
            16, MUTED, 7.2,
        ).move_to([0, -3.35, 0])
        self.show(VGroup(states, merge, softmax, fp_note,
                         arrow(merge.get_bottom(), softmax.get_top(), PRUNE)))
        self.to(90)

    def horizontal_flow(self, names, colors, widths=None, height=.82):
        if widths is None:
            widths = tuple(1.7 for _ in names)
        nodes = VGroup(*[
            card(n, c, w, height, 21, .12)
            for n, c, w in zip(names, colors, widths)
        ])
        nodes.arrange(RIGHT, buff=.44)
        links = VGroup(*[
            arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                  colors[i + 1], 2.1)
            for i in range(len(nodes) - 1)
        ])
        return VGroup(nodes, links)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 30).move_to(UP * 5.12)
        self.note = label(note, 21, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2,
            fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note),
                  FadeIn(self.caption_box), FadeIn(self.caption), run_time=.2)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
