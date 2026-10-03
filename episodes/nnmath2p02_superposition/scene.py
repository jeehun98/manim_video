"""Neural Network Mathematics Part 2, episode 02: Superposition."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


FEATURE_COLORS = (WEIGHT, PRUNE, GOOD, SPARSE, ACCENT)
FEATURE_ANGLES = (18, 90, 157, 225, 306)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.86, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .25))


class NeuralMathPart2Superposition(Scene):
    DURATION = 102

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 02", 17, MUTED).move_to(UP * 7.3),
            label("2차원 공간에 5개의 특징을 저장할 수 있을까?", 28).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 1 — Begin with the dimensionality puzzle.
        self.copy(
            "2차원에는 독립적인 축이 두 개뿐입니다", "h = (h₁, h₂) ∈ R²",
            "그렇다면 서로 다른 특징도\n두 개까지만 담을 수 있을까요?",
        )
        axes = self.coordinate_plane()
        axis_tags = VGroup(
            card("h₁", WEIGHT, 1.0, .62, 22, .12).move_to([2.95, -.35, 0]),
            card("h₂", PRUNE, 1.0, .62, 22, .12).move_to([.45, 2.75, 0]),
        )
        count = card("2 independent axes", ACCENT, 4.0, .74, 22, .12).move_to([0, -2.75, 0])
        self.show(VGroup(axes, axis_tags, count))
        self.to(6)

        # 2 — Two orthogonal features are interference-free.
        self.copy(
            "가장 쉬운 방법: 특징 하나에 축 하나", "f₁ᵀ f₂ = 0",
            "두 방향이 직교하면\n서로의 신호가 섞이지 않습니다.",
        )
        axes = self.coordinate_plane()
        f1 = self.vector(0, 0, 2.35, "f₁")
        f2 = self.vector(1, 90, 2.35, "f₂")
        angle = VGroup(
            Line([.28, 0, 0], [.28, .28, 0], color=ACCENT, stroke_width=2),
            Line([0, .28, 0], [.28, .28, 0], color=ACCENT, stroke_width=2),
        )
        self.show(VGroup(axes, f1, f2, angle,
                         card("2 features  ·  no interference", GOOD, 5.5, .72, 21, .12)
                         .move_to([0, -2.75, 0])))
        self.to(12)

        # 3 — The third orthogonal direction does not fit.
        self.copy(
            "그런데 세 번째 특징이 온다면?", "3 FEATURES  ·  ONLY 2 ORTHOGONAL DIRECTIONS",
            "평면에서는 세 방향을 모두\n서로 직교하게 만들 수 없습니다.",
        )
        axes = self.coordinate_plane()
        used = VGroup(self.vector(0, 0, 2.1, "f₁"), self.vector(1, 90, 2.1, "f₂"))
        third = card("f₃", GOOD, 1.0, .7, 24, .15).move_to([1.75, 1.55, 0])
        blocked = VGroup(
            Circle(radius=.52, color=PRUNE, stroke_width=3).move_to(third),
            Line([1.38, 1.18, 0], [2.12, 1.92, 0], color=PRUNE, stroke_width=4),
        )
        self.show(VGroup(axes, used, third, blocked,
                         label("x축도 사용 중   ·   y축도 사용 중", 21, MUTED)
                         .move_to([0, -2.7, 0])))
        self.to(18)

        # 4 — Increasing dimension is clean, but assume the bottleneck is fixed.
        self.copy(
            "차원을 늘리면 해결됩니다", "R²  →  R³  ·  BUT THE BOTTLENECK IS FIXED",
            "세 번째 독립 축을 만들 수 있습니다.\n하지만 차원이 두 개로 고정되어 있다면요?",
        )
        left = self.dimension_panel("R²", 2, WEIGHT).move_to([-2.05, .15, 0])
        right = self.dimension_panel("R³", 3, GOOD).move_to([2.05, .15, 0])
        link = Arrow([-.65, .15, 0], [.65, .15, 0], buff=0,
                     color=ACCENT, stroke_width=4, tip_length=.2)
        fixed = card("Only 2 dimensions", PRUNE, 4.25, .78, 23, .14).move_to([0, -2.85, 0])
        self.show(VGroup(left, link, right, fixed))
        self.to(24)

        # 5 — Place five non-orthogonal feature directions in R2.
        self.copy(
            "독립성을 포기하면 다섯 방향을 둘 수 있습니다", "5 NON-ORTHOGONAL DIRECTIONS IN R²",
            "다섯 독립 축이 아니라\n서로 다른 다섯 비직교 방향입니다.",
        )
        axes = self.coordinate_plane(.35)
        vectors = self.feature_vectors(2.2, labels=True)
        self.show(VGroup(axes, vectors,
                         card("5 features  ·  2 dimensions", ACCENT, 4.8, .76, 23, .14)
                         .move_to([0, -2.8, 0])))
        self.play(LaggedStart(*[GrowArrow(v[0]) for v in vectors], lag_ratio=.08), run_time=1.2)
        self.to(31)

        # 6 — Linear superposition creates cross terms.
        self.copy(
            "하지만 공짜는 아닙니다", "h = Σ xᵢ fᵢ",
            "방향이 직교하지 않으므로 한 feature를 읽을 때\n다른 신호가 함께 섞입니다.",
        )
        mini = self.feature_vectors(1.72, labels=False).move_to([-2.2, .45, 0])
        selected = mini[0].copy().set_opacity(1)
        projections = VGroup(
            DashedLine([-2.2, .45, 0], [-.95, 1.72, 0], color=PRUNE,
                       dash_length=.12, stroke_opacity=.8),
            DashedLine([-2.2, .45, 0], [-.72, -.45, 0], color=ACCENT,
                       dash_length=.12, stroke_opacity=.8),
        )
        equations = VGroup(
            card("f₁ᵀ f₂ ≠ 0", PRUNE, 2.55, .72, 22, .12),
            card("f₁ᵀ f₅ ≠ 0", ACCENT, 2.55, .72, 22, .12),
            card("Interference", INK, 2.55, .78, 23, .08),
        ).arrange(DOWN, buff=.28).move_to([2.15, .35, 0])
        self.show(VGroup(mini, selected, projections, equations))
        self.to(38)

        # 7 — State the core trade-off.
        self.copy(
            "두 가지 표현 전략", "INDEPENDENCE  ↔  CAPACITY",
            "적은 특징을 독립적으로 표현할 것인가,\n간섭을 허용하고 더 많이 넣을 것인가.",
        )
        orth = self.strategy_panel("ORTHOGONAL", 2, False).move_to([-2.05, .2, 0])
        shared = self.strategy_panel("SHARED", 5, True).move_to([2.05, .2, 0])
        versus = card("VS", ACCENT, 1.0, .7, 23, .13)
        trade = card("More Features  ↔  More Interference", PRUNE, 6.5, .78, 22, .12)
        trade.move_to([0, -2.85, 0])
        self.show(VGroup(orth, shared, versus, trade))
        self.to(45)

        # 8 — Dense activation makes all cross-talk relevant.
        self.copy(
            "모든 특징이 동시에 켜진다면", "DENSE ACTIVATION",
            "여러 신호가 계속 겹치며\ninterference 비용이 커집니다.",
        )
        dense = self.activation_scene((1, 1, 1, 1, 1), dense=True)
        self.show(dense)
        self.play(Indicate(dense[-1], color=PRUNE, scale_factor=1.06), run_time=.8)
        self.to(52)

        # 9 — Sparse activation reduces simultaneous collisions.
        self.copy(
            "한 번에 한두 개만 켜진다면", "SPARSE FEATURES",
            "함께 활성화되는 feature가 적으면\n실제로 충돌할 기회도 줄어듭니다.",
        )
        sparse = self.activation_scene((1, 0, 0, 1, 0), dense=False)
        self.show(sparse)
        self.to(60)

        # 10 — Different examples reuse the same directions over time.
        self.copy(
            "같은 공간을 입력마다 다르게 사용합니다", "SHARED SPACE  ·  DIFFERENT INPUTS",
            "입력이 바뀔 때마다 다른 방향이 켜집니다.\n모든 특징이 동시에 필요하지는 않습니다.",
        )
        states = VGroup(
            self.state_card("Input A", (1, 0, 0, 1, 0), WEIGHT),
            self.state_card("Input B", (0, 1, 0, 0, 0), PRUNE),
            self.state_card("Input C", (0, 0, 1, 0, 1), GOOD),
        ).arrange(RIGHT, buff=.25).move_to([0, .25, 0])
        timeline = Arrow([-3.25, -2.1, 0], [3.25, -2.1, 0], buff=0,
                         color=MUTED, stroke_width=2, tip_length=.16)
        self.show(VGroup(states, timeline,
                         label("same 2D space, reused across inputs", 20, ACCENT)
                         .move_to([0, -2.65, 0])))
        self.to(67)

        # 11 — Compare the expected interference visually.
        self.copy(
            "Sparsity가 간섭의 기회를 줄입니다", "EXPECTED INTERFERENCE CAN DECREASE",
            "feature가 더 sparse할수록\n공간을 공유하는 비용은 작아질 수 있습니다.",
        )
        dense_panel = self.collision_panel("DENSE", 5, PRUNE).move_to([-2.05, .25, 0])
        sparse_panel = self.collision_panel("SPARSE", 2, GOOD).move_to([2.05, .25, 0])
        self.show(VGroup(dense_panel, sparse_panel,
                         card("not zero  ·  but less frequent", ACCENT, 5.7, .76, 21, .12)
                         .move_to([0, -2.85, 0])))
        self.to(74)

        # 12 — Only now introduce the name.
        self.copy(
            "제한된 차원에 더 많은 특징을 겹쳐 표현합니다", "SUPERPOSITION",
            "Features가 dimensions보다 많아도\n비직교 방향으로 함께 표현할 수 있습니다.",
        )
        axes = self.coordinate_plane(.22)
        vectors = self.feature_vectors(2.25, labels=True)
        title = card("SUPERPOSITION", ACCENT, 5.4, .92, 29, .16).move_to([0, -2.55, 0])
        inequality = label("5 features  >  2 dimensions", 22, INK).move_to([0, -3.3, 0])
        self.show(VGroup(axes, vectors, title, inequality))
        self.to(81)

        # 13 — Neurons are coordinates; features are directions.
        self.copy(
            "뉴런은 좌표축, 특징은 공간의 방향", "ONE NEURON  ≠  ONE FEATURE",
            "뉴런 하나와 feature 하나가\n일대일로 대응할 필요는 없습니다.",
        )
        neurons = VGroup(
            card("Neuron 1", WEIGHT, 2.2, .78, 21, .14),
            card("Neuron 2", PRUNE, 2.2, .78, 21, .14),
        ).arrange(DOWN, buff=.42).move_to([-2.55, .25, 0])
        bottleneck = RoundedRectangle(width=1.1, height=4.1, corner_radius=.2,
                                      color=MUTED, fill_color=MUTED, fill_opacity=.05)
        bottleneck.move_to([0, .25, 0])
        coords = VGroup(label("h₁", 24, WEIGHT), label("h₂", 24, PRUNE)).arrange(DOWN, buff=.65)
        coords.move_to(bottleneck)
        features = VGroup(*[
            card(f"f{i+1}", FEATURE_COLORS[i], 1.25, .62, 20, .11)
            for i in range(5)
        ]).arrange(DOWN, buff=.17).move_to([2.55, .25, 0])
        links = VGroup()
        for i, feature in enumerate(features):
            for j in range(2):
                if (i + j) % 3 != 0:
                    links.add(Line(coords[j].get_right(), feature.get_left(),
                                   color=FEATURE_COLORS[i], stroke_width=1.4,
                                   stroke_opacity=.35))
        self.show(VGroup(links, neurons, bottleneck, coords, features))
        self.to(88)

        # 14 — More directions mean smaller angles and greater interference.
        self.copy(
            "특징을 계속 추가하면 방향은 가까워집니다", "CAPACITY  vs  INTERFERENCE",
            "모델은 어떤 특징을 보존할지,\n얼마나 많은 간섭을 허용할지 결정해야 합니다.",
        )
        sequence = VGroup(
            self.direction_disk(2, WEIGHT),
            self.direction_disk(5, SPARSE),
            self.direction_disk(9, PRUNE),
        ).arrange(RIGHT, buff=.48).move_to([0, .45, 0])
        tags = VGroup(
            label("low", 18, GOOD), label("medium", 18, ACCENT), label("high", 18, PRUNE)
        ).arrange(RIGHT, buff=1.35).move_to([0, -1.55, 0])
        axis = Arrow([-3.1, -2.3, 0], [3.1, -2.3, 0], buff=0,
                     color=MUTED, stroke_width=2, tip_length=.15)
        self.show(VGroup(sequence, tags, axis,
                         label("represented features  →", 20, MUTED).move_to([0, -2.75, 0])))
        self.to(95)

        # 15 — Contrast with episode 1 and open the polysemanticity question.
        self.copy(
            "1화의 수렴, 2화의 중첩", "WHAT DOES ONE NEURON REPRESENT?",
            "적은 차원에 여러 feature가 겹친다면\n뉴런 하나는 몇 가지 의미를 가질까요?",
        )
        collapse = self.collapse_icon().move_to([-2.1, .35, 0])
        superpose = self.superposition_icon().move_to([2.1, .35, 0])
        comparison = VGroup(
            label("many samples", 19, MUTED).move_to([-2.1, 2.7, 0]),
            label("few class centers", 19, GOOD).move_to([-2.1, -2.0, 0]),
            label("few dimensions", 19, MUTED).move_to([2.1, 2.7, 0]),
            label("many features", 19, ACCENT).move_to([2.1, -2.0, 0]),
        )
        question = card("One Neuron  ≠  One Feature?", ACCENT, 6.3, .86, 25, .15)
        question.move_to([0, -2.85, 0])
        self.show(VGroup(collapse, superpose, comparison, question))
        self.to(102)

    def coordinate_plane(self, opacity=.55):
        frame = RoundedRectangle(width=6.4, height=5.1, corner_radius=.22,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.025)
        x_axis = Arrow([-2.85, 0, 0], [2.85, 0, 0], buff=0,
                       color=MUTED, stroke_opacity=opacity, stroke_width=2,
                       tip_length=.16)
        y_axis = Arrow([0, -2.3, 0], [0, 2.3, 0], buff=0,
                       color=MUTED, stroke_opacity=opacity, stroke_width=2,
                       tip_length=.16)
        return VGroup(frame, x_axis, y_axis)

    def vector(self, index, angle, length=2.0, name=None, opacity=1):
        rad = angle * DEGREES
        end = np.array([length * np.cos(rad), length * np.sin(rad), 0.0])
        arrow = Arrow(ORIGIN, end, buff=.04, color=FEATURE_COLORS[index],
                      stroke_width=4, stroke_opacity=opacity, tip_length=.18)
        if name is None:
            return VGroup(arrow)
        tag = label(name, 21, FEATURE_COLORS[index]).move_to(end * 1.14)
        return VGroup(arrow, tag)

    def feature_vectors(self, length=2.1, labels=True):
        return VGroup(*[
            self.vector(i, FEATURE_ANGLES[i], length, f"f{i+1}" if labels else None)
            for i in range(5)
        ])

    def dimension_panel(self, name, dimensions, color):
        box = RoundedRectangle(width=2.8, height=4.2, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04)
        title = label(name, 28, color).move_to([0, 1.55, 0])
        origin = np.array([0, -.25, 0])
        vectors = VGroup(
            Arrow(origin, origin + np.array([1.0, 0, 0]), buff=.04, color=WEIGHT, tip_length=.14),
            Arrow(origin, origin + np.array([0, 1.0, 0]), buff=.04, color=PRUNE, tip_length=.14),
        )
        if dimensions == 3:
            vectors.add(Arrow(origin, origin + np.array([-.7, -.75, 0]), buff=.04,
                              color=GOOD, tip_length=.14))
        count = label(f"{dimensions} independent axes", 18, MUTED).move_to([0, -1.55, 0])
        return VGroup(box, title, vectors, count)

    def strategy_panel(self, title, count, shared):
        box = RoundedRectangle(width=3.25, height=4.25, corner_radius=.22,
                               color=ZERO, fill_color=ZERO, fill_opacity=.04)
        name = label(title, 21, ACCENT if shared else GOOD).move_to([0, 1.62, 0])
        directions = VGroup()
        angles = FEATURE_ANGLES if shared else (0, 90)
        for i, angle in enumerate(angles[:count]):
            rad = angle * DEGREES
            directions.add(Arrow(ORIGIN, [1.08 * np.cos(rad), 1.08 * np.sin(rad), 0],
                                 buff=.03, color=FEATURE_COLORS[i % 5],
                                 stroke_width=3, tip_length=.13))
        result = label("5 features / interference" if shared else "2 features / clean",
                       18, PRUNE if shared else GOOD).move_to([0, -1.55, 0])
        return VGroup(box, name, directions, result)

    def activation_scene(self, state, dense=False):
        vectors = self.feature_vectors(2.05, labels=True)
        for i, active in enumerate(state):
            vectors[i].set_opacity(1 if active else .13)
        rows = VGroup()
        for i, active in enumerate(state):
            dot = Dot(radius=.075, color=GOOD if active else ZERO)
            status = label("ON" if active else "OFF", 17, GOOD if active else MUTED)
            row = VGroup(label(f"f{i+1}", 18, FEATURE_COLORS[i]), dot, status)
            row.arrange(RIGHT, buff=.18)
            rows.add(row)
        rows.arrange(DOWN, buff=.16).move_to([2.65, .15, 0])
        vectors.scale(.78).move_to([-1.55, .35, 0])
        interference = card("HIGH INTERFERENCE" if dense else "FEWER COLLISIONS",
                            PRUNE if dense else GOOD, 4.2, .78, 22, .14)
        interference.move_to([0, -2.75, 0])
        return VGroup(vectors, rows, interference)

    def state_card(self, name, state, color):
        box = RoundedRectangle(width=2.25, height=4.35, corner_radius=.2,
                               color=color, fill_color=color, fill_opacity=.04)
        title = label(name, 20, color).move_to([0, 1.65, 0])
        rows = VGroup(*[
            VGroup(label(f"f{i+1}", 17, FEATURE_COLORS[i]),
                   Dot(radius=.07, color=GOOD if active else ZERO),
                   label("ON" if active else "OFF", 15, GOOD if active else MUTED))
            .arrange(RIGHT, buff=.13)
            for i, active in enumerate(state)
        ]).arrange(DOWN, buff=.17).move_to([0, -.2, 0])
        return VGroup(box, title, rows)

    def collision_panel(self, title, active_count, color):
        box = RoundedRectangle(width=3.35, height=4.4, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035)
        name = label(title, 23, color).move_to([0, 1.7, 0])
        points = [
            np.array([1.0 * np.cos(a * DEGREES), 1.0 * np.sin(a * DEGREES), 0])
            for a in FEATURE_ANGLES
        ]
        rays = VGroup(*[
            Line(ORIGIN, points[i], color=FEATURE_COLORS[i], stroke_width=3,
                 stroke_opacity=1 if i < active_count else .12)
            for i in range(5)
        ])
        collisions = VGroup()
        for i in range(active_count):
            for j in range(i + 1, active_count):
                collisions.add(Line(points[i], points[j], color=PRUNE,
                                    stroke_width=1, stroke_opacity=.18))
        count = label(f"active: {active_count} / 5", 18, MUTED).move_to([0, -1.65, 0])
        return VGroup(box, name, collisions, rays, count)

    def direction_disk(self, count, color):
        circle = Circle(radius=1.0, color=ZERO, fill_color=ZERO, fill_opacity=.035)
        rays = VGroup()
        for i in range(count):
            angle = TAU * i / count
            rays.add(Line(ORIGIN, [.82 * np.cos(angle), .82 * np.sin(angle), 0],
                          color=color, stroke_width=2.5, stroke_opacity=.8))
        return VGroup(circle, rays)

    def collapse_icon(self):
        colors = (WEIGHT, PRUNE, GOOD)
        group = VGroup()
        centers = ((0, 1.35), (-1.2, -.75), (1.2, -.75))
        for i, center in enumerate(centers):
            center = np.array([center[0], center[1], 0.0])
            for dx, dy in ((-.35, .2), (.28, .25), (-.2, -.3), (.25, -.22)):
                group.add(Dot(center + np.array([dx, dy, 0]), radius=.075,
                              color=colors[i], fill_opacity=.55))
            group.add(Arrow(center + np.array([0, .7, 0]), center, buff=.12,
                            color=colors[i], stroke_width=2, tip_length=.1))
        return group

    def superposition_icon(self):
        axes = VGroup(
            Line([-1.65, 0, 0], [1.65, 0, 0], color=MUTED, stroke_opacity=.35),
            Line([0, -1.65, 0], [0, 1.65, 0], color=MUTED, stroke_opacity=.35),
        )
        vectors = self.feature_vectors(1.45, labels=False)
        return VGroup(axes, vectors)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
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
