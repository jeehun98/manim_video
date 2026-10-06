"""Neural Network Mathematics 12: permutation symmetry and quotient space."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.82, size=23, fill=.11):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .22))


class NeuralMathPermutationQuotient(Scene):
    DURATION = 122

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  12", 18, MUTED).move_to(UP * 7.3),
            label("서로 다른 파라미터가 어떻게 같은 신경망이 될까?", 27).move_to(UP * 6.46),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT,
            fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.chrome.set_z_index(100)
        self.progress.set_z_index(101)
        self.add(self.chrome, self.progress)
        self.add_foreground_mobjects(self.chrome, self.progress)

        # 00:00–00:10 — Turn from input space to parameter space.
        self.copy("이번에는 파라미터 공간을 봅니다", "INPUT SPACE  →  PARAMETER SPACE",
                  "입력 공간에서 시선을 돌리면, 서로 다른 좌표가\n같은 신경망을 나타내는 이상한 일이 생깁니다.")
        left = self.space_panel("Input Space", [-2.1, .6, 0], WEIGHT)
        right = self.space_panel("Parameter Space", [2.1, .6, 0], SPARSE)
        arrow = Arrow(left.get_right(), right.get_left(), buff=.25,
                      color=ACCENT, stroke_width=5, tip_length=.22)
        question = card("θ_A ≠ θ_B   but   f_A = f_B ?", ACCENT, 6.3, .9, 25, .12)
        question.move_to([0, -2.4, 0])
        self.show(VGroup(left, right, arrow, question))
        self.to(10)

        # 00:10–00:22 — Build a two-hidden-unit network and a persistent graph.
        self.copy("은닉 뉴런 두 개에서 시작합니다", "y = v₁h₁ + v₂h₂",
                  "h₁과 h₂는 서로 다른 연결을 가지지만,\n출력에서는 두 항이 더해집니다.")
        net = self.swappable_network()
        graph = self.function_graph().move_to([2.15, .65, 0])
        graph_title = label("input → output", 19, MUTED).next_to(graph, UP, buff=.18)
        theta_card = card("θ_A = [h₁ links | h₂ links]", WEIGHT, 5.2, .72, 20, .1)
        theta_card.move_to([0, -2.65, 0])
        self.show(VGroup(net["group"], graph, graph_title, theta_card))
        self.to(22)

        # 00:22–00:35 — Swap actual neuron objects; edges follow with updaters.
        self.copy("뉴런과 연결을 함께 교환합니다", "h₁ ↔ h₂     ·     graph unchanged",
                  "뉴런의 자리와 모든 입·출력 연결을 함께 바꾸면\n파라미터 배열은 달라도 함수는 그대로입니다.")
        h1, h2 = net["h1"], net["h2"]
        p1, p2 = h1.get_center(), h2.get_center()
        self.play(
            MoveAlongPath(h1, ArcBetweenPoints(p1, p2, angle=-PI / 1.7)),
            MoveAlongPath(h2, ArcBetweenPoints(p2, p1, angle=-PI / 1.7)),
            Transform(theta_card, card("θ_B = [h₂ links | h₁ links]", SPARSE, 5.2, .72, 20, .1)
                      .move_to(theta_card)),
            run_time=2.8, rate_func=smooth,
        )
        self.play(Indicate(graph, color=GOOD), run_time=1.1)
        self.stage = VGroup(net["group"], graph, graph_title, theta_card)
        self.to(36)

        # 00:35–00:45 — Verify equality on several inputs.
        self.copy("입력을 바꿔도 출력은 같습니다", "θ_A ≠ θ_B     ·     f_{θ_A} = f_{θ_B}",
                  "덧셈의 두 항이 순서만 바뀌었으므로\n모든 입력에서 두 네트워크의 출력은 같습니다.")
        rows = VGroup(
            self.equal_row("x = −1", "−0.4", "−0.4"),
            self.equal_row("x =  0", "+0.2", "+0.2"),
            self.equal_row("x = +1", "+1.1", "+1.1"),
        ).arrange(DOWN, buff=.34).move_to([0, .55, 0])
        headers = VGroup(label("input", 19, MUTED), label("f_A(x)", 19, WEIGHT),
                         label("f_B(x)", 19, SPARSE)).arrange(RIGHT, buff=1.05)
        headers.move_to([0, 2.65, 0])
        proof = card("v₁h₁ + v₂h₂  =  v₂h₂ + v₁h₁", GOOD, 6.4, .82, 23, .12)
        proof.move_to([0, -2.35, 0])
        self.show(VGroup(headers, rows, proof))
        self.to(48)

        # 00:45–00:58 — Signature projection from parameters to functions.
        self.copy("두 파라미터 점, 하나의 함수 점", "PARAMETER SPACE  →  FUNCTION SPACE",
                  "파라미터 공간에서는 멀리 떨어져 있어도\n함수 공간에서는 같은 점으로 겹칠 수 있습니다.")
        parameter_box = self.space_box("Parameter Space", [0, 1.55, 0], 7.0, 2.55, SPARSE)
        function_box = self.space_box("Function Space", [0, -2.05, 0], 7.0, 1.65, GOOD)
        a, b = Dot([-2.35, 1.35, 0], radius=.14, color=WEIGHT), Dot([2.35, 1.7, 0], radius=.14, color=ACCENT)
        a_tag = label("θ_A", 23, WEIGHT).next_to(a, UP, buff=.15)
        b_tag = label("θ_B", 23, ACCENT).next_to(b, UP, buff=.15)
        f = Dot([0, -2.05, 0], radius=.18, color=GOOD)
        f_tag = label("same f", 24, GOOD).next_to(f, DOWN, buff=.16)
        arrows = VGroup(
            Arrow(a.get_center(), f.get_center(), buff=.22, color=WEIGHT, stroke_width=4, tip_length=.18),
            Arrow(b.get_center(), f.get_center(), buff=.22, color=ACCENT, stroke_width=4, tip_length=.18),
        )
        self.show(VGroup(parameter_box, function_box, arrows, a, b, a_tag, b_tag, f, f_tag))
        self.play(LaggedStart(Indicate(a), Indicate(b), Indicate(f), lag_ratio=.28), run_time=1.8)
        self.to(62)

        # 01:02–01:12 — Same function gives the same predictions and loss.
        self.copy("같은 함수라면 loss도 같습니다", "SAME FUNCTION → SAME OUTPUT → SAME LOSS",
                  "같은 데이터에 같은 예측 기반 loss를 적용하면,\n함수가 같을 때 출력과 loss도 같습니다.")
        loss_chain = self.loss_chain()
        assumption = label("same data · prediction-based loss", 18, MUTED).move_to([0, -2.75, 0])
        self.show(VGroup(loss_chain, assumption))
        self.play(LaggedStart(*[Indicate(item) for item in loss_chain[0::2]], lag_ratio=.25), run_time=1.6)
        self.to(72)

        # 01:12–01:22 — Distant symmetric minima.
        self.copy("같은 minimum이 대칭적으로 복제됩니다", "L(θ_A) = L(θ_B)",
                  "그래서 loss landscape의 서로 먼 최솟값 중 일부는\n같은 함수의 대칭 복제본일 수 있습니다.")
        landscape = self.loss_landscape()
        same = card("f_A=f_B  ⇒  L(θ_A)=L(θ_B)", GOOD, 5.7, .78, 23, .12)
        same.move_to([0, -2.65, 0])
        self.show(VGroup(landscape, same))
        self.to(82)

        # 01:22–01:35 — Show parameter points replicating factorially.
        self.copy("같은 함수의 점들이 공간 곳곳에 늘어납니다", "n hidden units  →  up to n! parameter points",
                  "서로 구별되는 뉴런이 n개라면 순열만으로도\n같은 함수의 표현이 최대 n!개 생깁니다.")
        replicas = VGroup(
            self.replica_column(2, "2! = 2", WEIGHT),
            self.replica_column(6, "3! = 6", GOOD),
            self.replica_column(24, "4! = 24", SPARSE),
        ).arrange(RIGHT, buff=.38).move_to([0, .45, 0])
        caveat = label("distinct hidden units · permutation symmetry only", 18, MUTED)
        caveat.move_to([0, -2.75, 0])
        self.show(VGroup(replicas, caveat))
        self.play(LaggedStart(*[ShowIncreasingSubsets(col[1]) for col in replicas], lag_ratio=.25),
                  run_time=1.8)
        self.to(95)

        # 01:35–01:48 — Name the equivalence class after grouping points.
        self.copy("같은 것으로 취급할 점들을 한 묶음으로", "EQUIVALENCE CLASS  [θ]",
                  "순열만 다른 점들을 하나의 동치류로 묶습니다.\n동치류는 같은 것으로 보기로 한 점들의 집합입니다.")
        orbits = self.symmetry_orbits()
        theta_tags = self.orbit_point_labels(orbits[0])
        class_card = card("[θ] = { θ′ | θ′ ~ θ }", ACCENT, 4.8, .75, 22, .12)
        class_card.move_to([0, -2.75, 0])
        self.show(VGroup(orbits, theta_tags, class_card))
        self.play(Indicate(orbits[0], color=ACCENT, scale_factor=1.04), run_time=1.4)
        self.to(108)

        # 01:48–02:02 — Collapse each class and explain the quotient slash.
        self.copy("각 동치류 전체를 하나의 점으로 봅니다", "PARAMETER SPACE / PERMUTATION SYMMETRY",
                  "슬래시는 숫자 나눗셈이 아니라, 대칭으로 같은 점들을\n하나로 식별해 새 공간을 만든다는 뜻입니다.")
        self.play(FadeOut(theta_tags), FadeOut(class_card), run_time=.25)
        reps = VGroup(
            Dot([-2.1, .65, 0], radius=.18, color=WEIGHT),
            Dot([0, .65, 0], radius=.18, color=GOOD),
            Dot([2.1, .65, 0], radius=.18, color=SPARSE),
        )
        self.play(*[ReplacementTransform(orbits[i], reps[i]) for i in range(3)], run_time=2.3)
        orbit_labels = VGroup(
            label("[θ]₁", 22, WEIGHT).next_to(reps[0], DOWN, buff=.22),
            label("[θ]₂", 22, GOOD).next_to(reps[1], DOWN, buff=.22),
            label("[θ]₃", 22, SPARSE).next_to(reps[2], DOWN, buff=.22),
        )
        slash = card("/  =  identify equivalent points", MUTED, 5.5, .7, 19, .09)
        slash.move_to([0, -1.15, 0])
        quotient = card("Θ / Sₙ", ACCENT, 3.1, .95, 34, .14).move_to([0, -2.55, 0])
        self.play(FadeIn(orbit_labels), FadeIn(slash), FadeIn(quotient), run_time=.8)
        self.stage = VGroup(reps, orbit_labels, slash, quotient)
        self.wait(2.0)

        summary = self.final_chain()
        self.play(FadeOut(self.stage), run_time=.3)
        self.play(FadeIn(summary, shift=UP * .12), run_time=.45)
        self.stage = summary
        self.to(122)

    def space_panel(self, title, center, color):
        box = RoundedRectangle(width=3.1, height=3.4, corner_radius=.2,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06).move_to(center)
        dots = VGroup(*[
            Dot(np.array(center) + [x, y, 0], radius=.065, color=color)
            for x, y in ((-.8, .55), (.55, .8), (-.3, -.2), (.75, -.65), (-.9, -.85))
        ])
        tag = label(title, 22, color).next_to(box, UP, buff=.2)
        return VGroup(box, dots, tag)

    def swappable_network(self):
        x_node = Dot([-3.35, .7, 0], radius=.18, color=INK)
        h1 = Dot([-1.75, 1.7, 0], radius=.22, color=WEIGHT)
        h2 = Dot([-1.75, -.3, 0], radius=.22, color=SPARSE)
        y_node = Dot([-.15, .7, 0], radius=.2, color=ACCENT)
        edges = VGroup(
            always_redraw(lambda: Line(x_node.get_center(), h1.get_center(), color=WEIGHT, stroke_width=5)),
            always_redraw(lambda: Line(h1.get_center(), y_node.get_center(), color=WEIGHT, stroke_width=5)),
            always_redraw(lambda: Line(x_node.get_center(), h2.get_center(), color=SPARSE, stroke_width=3)),
            always_redraw(lambda: Line(h2.get_center(), y_node.get_center(), color=SPARSE, stroke_width=3)),
        )
        tags = VGroup(
            label("x", 22, INK).next_to(x_node, LEFT, buff=.16),
            always_redraw(lambda: label("h₁", 21, WEIGHT).next_to(h1, UP, buff=.12)),
            always_redraw(lambda: label("h₂", 21, SPARSE).next_to(h2, DOWN, buff=.12)),
            label("y", 22, ACCENT).next_to(y_node, RIGHT, buff=.16),
        )
        group = VGroup(edges, x_node, h1, h2, y_node, tags)
        return {"group": group, "h1": h1, "h2": h2}

    def function_graph(self):
        axes = Axes(x_range=[-1.2, 1.2, 1], y_range=[-.5, 1.3, .5],
                    x_length=2.6, y_length=2.6, tips=False,
                    axis_config={"color": MUTED, "stroke_width": 1.6})
        curve = axes.plot(lambda x: .32 * x * x + .38 * x + .15,
                          x_range=[-1.1, 1.1], color=GOOD, stroke_width=5)
        return VGroup(axes, curve)

    def equal_row(self, x_text, a_text, b_text):
        return VGroup(
            card(x_text, MUTED, 1.7, .68, 19, .08),
            card(a_text, WEIGHT, 1.65, .68, 20, .1),
            label("=", 23, GOOD),
            card(b_text, SPARSE, 1.65, .68, 20, .1),
        ).arrange(RIGHT, buff=.24)

    def space_box(self, title, center, width, height, color):
        box = RoundedRectangle(width=width, height=height, corner_radius=.18,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.045).move_to(center)
        tag = card(title, color, 2.8, .62, 19, .12).move_to(
            np.array(center) + [0, height / 2 - .2, 0]
        )
        return VGroup(box, tag)

    def loss_chain(self):
        items = VGroup(
            card("f_A = f_B", WEIGHT, 4.4, .72, 23, .11),
            label("↓", 28, ACCENT),
            card("same predictions", GOOD, 4.4, .72, 22, .11),
            label("↓", 28, ACCENT),
            card("L(θ_A) = L(θ_B)", SPARSE, 4.4, .72, 23, .11),
        ).arrange(DOWN, buff=.2).move_to([0, .35, 0])
        return items

    def replica_column(self, count, result, color):
        frame = RoundedRectangle(width=2.25, height=4.1, corner_radius=.18,
                                 stroke_color=color, stroke_width=2,
                                 fill_color=color, fill_opacity=.05)
        cols = 2 if count <= 6 else 4
        rows = int(np.ceil(count / cols))
        dx = .48 if cols == 2 else .38
        dy = .52 if rows <= 3 else .32
        nodes = VGroup()
        for i in range(count):
            row, col = divmod(i, cols)
            x = (col - (cols - 1) / 2) * dx
            y = .8 - (row - (rows - 1) / 2) * dy
            nodes.add(Dot([x, y - .8, 0], radius=.075 if count > 6 else .105, color=color))
        n_tag = label("same f", 18, MUTED).move_to([0, 1.55, 0])
        result_tag = card(result, color, 1.8, .65, 21, .13).move_to([0, -1.55, 0])
        return VGroup(frame, nodes, n_tag, result_tag)

    def loss_landscape(self):
        axis = Arrow([-3.45, -2.0, 0], [3.5, -2.0, 0], buff=0,
                     color=MUTED, stroke_width=2, tip_length=.14)
        curve = VMobject(color=ACCENT, stroke_width=5)
        pts = [
            [-3.2, 1.8, 0], [-2.7, .5, 0], [-2.1, -1.25, 0], [-1.45, -.15, 0],
            [-.4, 1.15, 0], [.45, .95, 0], [1.4, -.2, 0], [2.1, -1.25, 0],
            [2.75, .45, 0], [3.2, 1.75, 0],
        ]
        curve.set_points_smoothly(pts)
        a, b = Dot([-2.1, -1.25, 0], radius=.14, color=WEIGHT), Dot([2.1, -1.25, 0], radius=.14, color=SPARSE)
        tags = VGroup(label("θ_A", 22, WEIGHT).next_to(a, DOWN, buff=.18),
                      label("θ_B", 22, SPARSE).next_to(b, DOWN, buff=.18),
                      label("same loss", 21, GOOD).move_to([0, -1.45, 0]))
        bridge = DashedLine(a.get_center(), b.get_center(), color=GOOD, dash_length=.15)
        return VGroup(axis, curve, bridge, a, b, tags)

    def symmetry_orbits(self):
        centers = ([-2.3, .45, 0], [0, .45, 0], [2.3, .45, 0])
        colors = (WEIGHT, GOOD, SPARSE)
        groups = VGroup()
        for center, color in zip(centers, colors):
            ellipse = Ellipse(width=1.85, height=3.15, color=color,
                              stroke_width=2, fill_color=color, fill_opacity=.05).move_to(center)
            points = VGroup(*[
                Dot(np.array(center) + [dx, dy, 0], radius=.095, color=color)
                for dx, dy in ((-.45, .85), (.35, .55), (-.25, -.05), (.42, -.7), (-.4, -1.0))
            ])
            groups.add(VGroup(ellipse, points))
        return groups

    def orbit_point_labels(self, orbit):
        points = orbit[1]
        tags = VGroup()
        directions = (UL, UR, LEFT, DR)
        for i, direction in enumerate(directions):
            tags.add(label(f"θ{i + 1}", 17, WEIGHT).next_to(points[i], direction, buff=.1))
        return tags

    def final_chain(self):
        texts = (
            ("Different Parameters", WEIGHT),
            ("Same Function", GOOD),
            ("Equivalence", SPARSE),
            ("Equivalence Class", ACCENT),
            ("Quotient Space", INK),
        )
        items = VGroup()
        for i, (text_value, color) in enumerate(texts):
            items.add(card(text_value, color, 5.2, .58, 20, .1))
            if i < len(texts) - 1:
                items.add(label("↓", 22, MUTED))
        return items.arrange(DOWN, buff=.12).move_to([0, .3, 0])

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.remove_foreground_mobjects(self.heading, self.note,
                                            self.caption_box, self.caption)
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 28).move_to(UP * 5.12)
        self.note = label(note, 18, ACCENT).move_to(DOWN * 4.42)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2,
            fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.heading.set_z_index(100)
        self.note.set_z_index(100)
        self.caption_box.set_z_index(100)
        self.caption.set_z_index(101)
        self.play(FadeIn(self.heading), FadeIn(self.note), FadeIn(self.caption_box),
                  FadeIn(self.caption), run_time=.2)
        self.add_foreground_mobjects(self.chrome, self.heading, self.note,
                                    self.caption_box, self.caption, self.progress)
        self.restore_layers()

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        if len(self.stage):
            self.play(FadeIn(self.stage, shift=UP * .1), run_time=.4)
        self.restore_layers()

    def restore_layers(self):
        self.chrome[0].set_opacity(1)
        self.chrome[1].set_opacity(1)
        self.chrome[2].set_stroke(opacity=.35)
        self.heading.set_opacity(1)
        self.note.set_opacity(1)
        self.caption_box.set_opacity(1)
        self.caption.set_opacity(1)
        self.add(self.chrome, self.progress)
        self.bring_to_front(self.chrome, self.heading, self.note,
                            self.caption_box, self.caption, self.progress)

    def to(self, target):
        self.restore_layers()
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
