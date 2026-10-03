"""Neural Network Mathematics Part 2, episode 03: Polysemanticity."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


FEATURE_COLORS = (WEIGHT, PRUNE, GOOD, SPARSE, ACCENT)
FEATURE_ANGLES = (12, 52, 142, 220, 308)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.86, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .25))


class NeuralMathPart2Polysemanticity(Scene):
    DURATION = 108

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 03", 17, MUTED).move_to(UP * 7.3),
            label("뉴런 하나는 하나의 의미를 담당할까?", 28).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 1 — Select one neuron and observe a high activation for CAT.
        self.copy(
            "뉴런 하나를 꺼내봅시다", "HIDDEN LAYER  ·  NEURON 17",
            "고양이에서 강하게 반응합니다.\n이 뉴런은 고양이를 표현할까요?",
        )
        layer = self.neuron_grid(5, 7, 16).move_to([-1.75, .25, 0])
        selected = layer[16]
        halo = Circle(radius=.28, color=ACCENT, stroke_width=3).move_to(selected)
        input_card = self.concept_card("CAT", WEIGHT, self.cat_icon()).move_to([1.85, 1.25, 0])
        arrow = Arrow([.15, .65, 0], [1.0, 1.05, 0], buff=0,
                      color=MUTED, stroke_width=3, tip_length=.17)
        meter = self.activation_meter(.94, PRUNE).move_to([1.85, -1.35, 0])
        self.show(VGroup(layer, halo, input_card, arrow, meter,
                         card("Neuron 17", ACCENT, 2.5, .72, 22, .14).move_to([-1.75, -2.75, 0])))
        self.play(Indicate(halo, color=ACCENT, scale_factor=1.18), run_time=.8)
        self.to(7)

        # 2 — Present the intuitive one-neuron/one-feature story.
        self.copy(
            "익숙하고 편한 해석", "ONE NEURON  =  ONE FEATURE?",
            "뉴런마다 역할 하나가 있다면\n모델 내부를 쉽게 읽을 수 있을 것 같습니다.",
        )
        mappings = VGroup(
            self.mapping_row("N₁", "CAT", WEIGHT),
            self.mapping_row("N₂", "CAR", PRUNE),
            self.mapping_row("N₃", "FACE", GOOD),
        ).arrange(DOWN, buff=.5).move_to([0, .45, 0])
        premise = card("inspect neuron  →  name concept", ACCENT, 5.8, .76, 22, .12)
        premise.move_to([0, -2.65, 0])
        self.show(VGroup(mappings, premise))
        self.to(14)

        # 3 — More data breaks the simple label.
        self.copy(
            "그런데 입력을 더 넣어보면", "NEURON 17  ·  ACTIVATION RANKING",
            "같은 뉴런이 바퀴와 곡선에도 반응합니다.\n이 뉴런의 진짜 의미는 무엇일까요?",
        )
        ranking = VGroup(
            self.rank_row(1, "CAT", .94, WEIGHT),
            self.rank_row(2, "WHEEL", .92, PRUNE),
            self.rank_row(3, "CAT", .91, WEIGHT),
            self.rank_row(4, "ARC", .88, SPARSE),
            self.rank_row(5, "CAT", .86, WEIGHT),
        ).arrange(DOWN, buff=.22).move_to([0, .35, 0])
        question = card("CAT?   WHEEL?   ARC?", ACCENT, 5.4, .78, 24, .14).move_to([0, -2.75, 0])
        self.show(VGroup(ranking, question))
        self.to(21)

        # 4 — Replace the box metaphor with a geometric possibility.
        self.copy(
            "한 상자에 세 의미가 든 걸까요?", "RECALL: SUPERPOSITION",
            "그렇게 볼 수도 있지만 Superposition은\n전혀 다른 해석을 제시합니다.",
        )
        box = RoundedRectangle(width=3.0, height=4.5, corner_radius=.22,
                               color=ACCENT, fill_color=ACCENT, fill_opacity=.04)
        box.move_to([-2.15, .2, 0])
        contents = VGroup(
            card("CAT", WEIGHT, 1.85, .65, 20, .12),
            card("WHEEL", PRUNE, 1.85, .65, 20, .12),
            card("ARC", SPARSE, 1.85, .65, 20, .12),
        ).arrange(DOWN, buff=.32).move_to(box)
        neuron_tag = label("Neuron 17", 21, ACCENT).move_to([-2.15, 2.8, 0])
        shift = Arrow([-.4, .2, 0], [.55, .2, 0], buff=0,
                      color=MUTED, stroke_width=3, tip_length=.17)
        geometry = self.feature_space(1.55, labels=False).move_to([2.15, .2, 0])
        self.show(VGroup(box, contents, neuron_tag, shift, geometry,
                         label("container?", 19, PRUNE).move_to([-2.15, -2.6, 0]),
                         label("shared coordinates?", 19, GOOD).move_to([2.15, -2.6, 0])))
        self.to(28)

        # 5 — Neurons form coordinates; features need not align with axes.
        self.copy(
            "뉴런은 좌표, feature는 방향일 수 있습니다", "h = (h₁, h₂)",
            "두 뉴런은 2차원 공간의 좌표가 됩니다.\nfeature가 축과 일치할 이유는 없습니다.",
        )
        axes = self.axes_box()
        coordinate_tags = VGroup(
            card("Neuron 1", WEIGHT, 2.05, .62, 19, .1).move_to([2.45, -.45, 0]),
            card("Neuron 2", PRUNE, 2.05, .62, 19, .1).move_to([.6, 2.45, 0]),
        )
        features = VGroup(
            self.direction(0, 0, 2.05, "vA"),
            self.direction(2, 48, 2.05, "vB"),
            self.direction(3, 310, 2.05, "vC"),
        )
        self.show(VGroup(axes, coordinate_tags, features,
                         card("Neuron = coordinate axis", ACCENT, 4.8, .74, 22, .12)
                         .move_to([0, -2.75, 0])))
        self.play(LaggedStart(*[GrowArrow(item[0]) for item in features], lag_ratio=.18), run_time=1.0)
        self.to(35)

        # 6 — Three feature vectors all project onto neuron 1.
        self.copy(
            "같은 뉴런 축에 여러 feature가 걸칩니다", "h₁ = a₁f₁ + a₂f₂ + a₃f₃ + ···",
            "서로 다른 feature들이 모두\n첫 번째 뉴런에 성분을 가질 수 있습니다.",
        )
        axes = self.axes_box()
        specs = ((0, 2.2), (48, 2.1), (310, 2.0))
        vectors = VGroup(*[
            self.direction(i if i == 0 else i + 1, angle, length, f"v{chr(65+i)}")
            for i, (angle, length) in enumerate(specs)
        ])
        projections = VGroup()
        projection_dots = VGroup()
        for i, (angle, length) in enumerate(specs):
            end = np.array([length * np.cos(angle * DEGREES), length * np.sin(angle * DEGREES), 0])
            foot = np.array([end[0], 0, 0])
            projections.add(DashedLine(end, foot, color=FEATURE_COLORS[i if i == 0 else i + 1],
                                       dash_length=.1, stroke_opacity=.75))
            projection_dots.add(Dot(foot, radius=.08,
                                    color=FEATURE_COLORS[i if i == 0 else i + 1]))
        neuron_axis = Line([-2.75, 0, 0], [2.75, 0, 0], color=WEIGHT, stroke_width=5)
        self.show(VGroup(axes, neuron_axis, vectors, projections, projection_dots,
                         label("Neuron 1 receives all three components", 20, ACCENT)
                         .move_to([0, -2.75, 0])))
        self.to(42)

        # 7 — Make the perspective flip explicit.
        self.copy(
            "관점을 뒤집습니다", "NEURON  ≠  FEATURE",
            "뉴런은 representation의 좌표축이고\nfeature는 공간 안의 방향일 수 있습니다.",
        )
        old = VGroup(
            self.mapping_row("N₁", "Feature A", WEIGHT),
            self.mapping_row("N₂", "Feature B", PRUNE),
        ).arrange(DOWN, buff=.45).scale(.82).move_to([-2.05, .25, 0])
        cross = VGroup(
            Line([-3.15, -1.2, 0], [-.95, 1.7, 0], color=PRUNE, stroke_width=5),
            Line([-3.15, 1.7, 0], [-.95, -1.2, 0], color=PRUNE, stroke_width=5),
        )
        new = self.feature_space(1.55, labels=True).move_to([2.05, .25, 0])
        switch = Arrow([-.5, .25, 0], [.55, .25, 0], buff=0,
                       color=ACCENT, stroke_width=4, tip_length=.2)
        self.show(VGroup(old, cross, switch, new,
                         card("coordinates  ≠  meanings", ACCENT, 5.2, .78, 24, .14)
                         .move_to([0, -2.8, 0])))
        self.to(49)

        # 8 — A basis change alters coordinates, not the point.
        self.copy(
            "좌표축은 공간을 읽는 방법입니다", "SAME POINT  ·  DIFFERENT BASIS",
            "같은 점도 basis를 회전하면 좌표가 바뀝니다.\n구조가 축 하나에 맞을 필요는 없습니다.",
        )
        left = self.basis_panel(False).move_to([-2.05, .25, 0])
        right = self.basis_panel(True).move_to([2.05, .25, 0])
        same = Arrow([-.6, .25, 0], [.6, .25, 0], buff=0,
                     color=ACCENT, stroke_width=3, tip_length=.17)
        self.show(VGroup(left, right, same,
                         card("geometry stays  ·  coordinates change", GOOD, 6.0, .76, 21, .12)
                         .move_to([0, -2.82, 0])))
        self.to(57)

        # 9 — Return to Neuron 17 with projections from different features.
        self.copy(
            "Neuron 17을 다시 봅시다", "SHARED NEURON AXIS",
            "세 의미를 상자에 저장했다기보다\n서로 다른 feature들이 같은 축을 공유할 수 있습니다.",
        )
        axis = Line([-3.0, -1.2, 0], [3.0, -1.2, 0], color=PRUNE, stroke_width=5)
        axis_tag = card("Neuron 17 axis", PRUNE, 3.2, .7, 21, .14).move_to([0, -2.15, 0])
        concepts = VGroup(
            self.concept_card("CAT", WEIGHT, self.cat_icon()).scale(.74),
            self.concept_card("WHEEL", PRUNE, self.wheel_icon()).scale(.74),
            self.concept_card("ARC", SPARSE, self.arc_icon()).scale(.74),
        ).arrange(RIGHT, buff=.5).move_to([0, 1.75, 0])
        rays = VGroup()
        for i, concept in enumerate(concepts):
            foot = np.array([-2.0 + i * 2.0, -1.2, 0])
            rays.add(Arrow(concept.get_bottom(), foot, buff=.08,
                           color=FEATURE_COLORS[(0, 1, 3)[i]], stroke_width=3,
                           tip_length=.14))
        self.show(VGroup(axis, axis_tag, concepts, rays))
        self.to(64)

        # 10 — Name polysemanticity only after the geometry is established.
        self.copy(
            "하나의 뉴런, 여러 연관된 feature", "POLYSEMANTICITY",
            "여러 feature와 연관되면 Polysemantic,\n하나와 명확히 대응하면 Monosemantic입니다.",
        )
        mono = self.semantic_panel(False).move_to([-2.05, .3, 0])
        poly = self.semantic_panel(True).move_to([2.05, .3, 0])
        divider = Line([0, -2.2, 0], [0, 2.5, 0], color=ZERO, stroke_width=2)
        self.show(VGroup(mono, divider, poly,
                         card("Polysemanticity", ACCENT, 4.4, .82, 27, .15)
                         .move_to([0, -2.85, 0])))
        self.to(71)

        # 11 — Superposition can produce polysemantic coordinates.
        self.copy(
            "Superposition과 연결하면 자연스럽습니다", "CAN EMERGE  ·  NOT AN IDENTITY",
            "차원보다 많은 feature가 겹치면 좌표축마다\n여러 성분이 나타날 수 있습니다.",
        )
        space = self.feature_space(1.55, labels=False).move_to([-2.2, .3, 0])
        implication = Arrow([-.35, .3, 0], [.55, .3, 0], buff=0,
                            color=ACCENT, stroke_width=4, tip_length=.2)
        neuron = self.poly_neuron_icon().move_to([2.15, .3, 0])
        labels = VGroup(
            label("5 feature directions", 19, SPARSE).move_to([-2.2, -2.05, 0]),
            label("polysemantic neuron", 19, PRUNE).move_to([2.15, -2.05, 0]),
        )
        caveat = card("Superposition  →  can emerge", ACCENT, 5.8, .78, 22, .13)
        caveat.move_to([0, -2.85, 0])
        self.show(VGroup(space, implication, neuron, labels, caveat))
        self.to(78)

        # 12 — Labeling each neuron produces ambiguity.
        self.copy(
            "뉴런 하나씩 이름 붙이면 충분할까요?", "NEURON-CENTRIC INTERPRETATION",
            "각 뉴런의 label이 뒤섞인다면\n내부 feature를 완전히 설명하기 어렵습니다.",
        )
        grid = self.neuron_grid(4, 6, -1).scale(.9).move_to([-1.7, .4, 0])
        tags = VGroup(
            card("cat?", WEIGHT, 1.25, .55, 17, .1).move_to([1.35, 1.65, 0]),
            card("wheel?", PRUNE, 1.55, .55, 17, .1).move_to([2.55, .75, 0]),
            card("curve?", SPARSE, 1.55, .55, 17, .1).move_to([1.45, -.2, 0]),
            card("face?", GOOD, 1.35, .55, 17, .1).move_to([2.45, -1.15, 0]),
        )
        links = VGroup(*[
            Line(grid[i * 3 % len(grid)].get_center(), tags[i].get_left(),
                 color=FEATURE_COLORS[i], stroke_opacity=.45, stroke_width=1.5)
            for i in range(4)
        ])
        self.show(VGroup(links, grid, tags,
                         card("1000 neurons  ·  ambiguous labels", PRUNE, 5.7, .75, 21, .12)
                         .move_to([0, -2.8, 0])))
        self.to(85)

        # 13 — Search directions, not only axes.
        self.copy(
            "우리가 찾고 싶은 것은 축이 아닐 수 있습니다", "SEARCH FOR FEATURES",
            "의미를 가진 대상은 neuron axis 자체가 아니라\n공간 속 feature 방향일 수 있습니다.",
        )
        axes = VGroup(*[
            Line([-3.1, -1.8 + i * .45, 0], [3.1, -1.8 + i * .45, 0],
                 color=MUTED, stroke_opacity=.12, stroke_width=1.2)
            for i in range(9)
        ])
        directions = VGroup()
        for i, angle in enumerate((18, 62, 128, 198, 244, 315)):
            rad = angle * DEGREES
            directions.add(Arrow(ORIGIN, [2.15 * np.cos(rad), 2.15 * np.sin(rad), 0],
                                 buff=.04, color=FEATURE_COLORS[i % 5],
                                 stroke_width=4, tip_length=.18))
        instruction = VGroup(
            card("Don't only search neurons", MUTED, 5.6, .7, 20, .06),
            label("↓", 28, ACCENT),
            card("Search for features", ACCENT, 5.6, .78, 24, .14),
        ).arrange(DOWN, buff=.18).move_to([0, -2.65, 0])
        self.show(VGroup(axes, directions, instruction))
        self.to(92)

        # 14 — Decompose one activation into a sparse feature dictionary.
        self.copy(
            "섞인 activation을 feature로 다시 분해합니다", "h ≈ z₁v₁ + z₂v₂ + ··· + zₘvₘ",
            "그 순간 실제로 켜진 소수의 feature를\n찾아내는 것이 다음 문제입니다.",
        )
        mixed = Arrow([-3.1, .45, 0], [-1.7, 1.9, 0], buff=.04,
                      color=INK, stroke_width=7, tip_length=.24)
        mixed_tag = card("h", INK, .85, .7, 25, .08).move_to([-2.7, -.5, 0])
        split = Arrow([-.95, .45, 0], [.1, .45, 0], buff=0,
                      color=ACCENT, stroke_width=4, tip_length=.2)
        dictionary = VGroup()
        coeffs = ("0", ".8", "0", ".4", "0")
        for i, angle in enumerate(FEATURE_ANGLES):
            rad = angle * DEGREES
            active = coeffs[i] != "0"
            direction = Arrow([1.65, .55, 0],
                              [1.65 + 1.45 * np.cos(rad), .55 + 1.45 * np.sin(rad), 0],
                              buff=.03, color=FEATURE_COLORS[i],
                              stroke_width=4 if active else 2,
                              stroke_opacity=1 if active else .14,
                              tip_length=.15)
            dictionary.add(direction)
        z_rows = VGroup(*[
            card(f"z{i+1} = {coeffs[i]}", FEATURE_COLORS[i] if coeffs[i] != "0" else MUTED,
                 1.45, .52, 16, .1 if coeffs[i] != "0" else .02)
            for i in range(5)
        ]).arrange(DOWN, buff=.12).move_to([3.15, .45, 0])
        sparse_tag = card("sparse z", GOOD, 3.3, .72, 22, .13).move_to([1.65, -2.45, 0])
        self.show(VGroup(mixed, mixed_tag, split, dictionary, z_rows, sparse_tag))
        self.to(100)

        # 15 — End with the change in interpretive unit and SAE teaser.
        self.copy(
            "모델을 보는 기본 단위가 달라집니다", "NEURON VIEW  →  FEATURE VIEW",
            "뉴런은 좌표이고 의미는 방향에 있을 수 있습니다.\n겹친 feature를 다시 분리할 수 있을까요?",
        )
        neuron_view = self.neuron_view_panel().move_to([-2.1, .35, 0])
        feature_view = self.feature_view_panel().move_to([2.1, .35, 0])
        transition = Arrow([-.5, .35, 0], [.55, .35, 0], buff=0,
                           color=ACCENT, stroke_width=4, tip_length=.2)
        teaser = VGroup(
            card("h  →  {v₁, v₂, ···, vₘ}", ACCENT, 5.6, .78, 23, .14),
            label("NEXT  ·  SPARSE AUTOENCODER", 18, GOOD),
        ).arrange(DOWN, buff=.25).move_to([0, -2.75, 0])
        self.show(VGroup(neuron_view, transition, feature_view, teaser))
        self.to(108)

    def neuron_grid(self, rows, cols, selected):
        group = VGroup()
        for r in range(rows):
            for c in range(cols):
                index = r * cols + c
                color = ACCENT if index == selected else ZERO
                dot = Circle(radius=.13, color=color, stroke_width=2,
                             fill_color=color, fill_opacity=.28 if index == selected else .06)
                dot.move_to([(c - (cols - 1) / 2) * .48,
                             ((rows - 1) / 2 - r) * .55, 0])
                group.add(dot)
        return group

    def concept_card(self, name, color, icon):
        box = RoundedRectangle(width=2.25, height=2.1, corner_radius=.18,
                               color=color, fill_color=color, fill_opacity=.05)
        icon.scale(.62).move_to([0, .3, 0])
        title = label(name, 20, color).move_to([0, -.72, 0])
        return VGroup(box, icon, title)

    def cat_icon(self):
        head = Circle(radius=.62, color=WEIGHT, fill_color=WEIGHT, fill_opacity=.08)
        ears = VGroup(
            Triangle(color=WEIGHT, fill_color=WEIGHT, fill_opacity=.08).scale(.28).rotate(.12).move_to([-.42, .55, 0]),
            Triangle(color=WEIGHT, fill_color=WEIGHT, fill_opacity=.08).scale(.28).rotate(-.12).move_to([.42, .55, 0]),
        )
        eyes = VGroup(Dot([-.22, .1, 0], radius=.05, color=WEIGHT),
                      Dot([.22, .1, 0], radius=.05, color=WEIGHT))
        return VGroup(ears, head, eyes)

    def wheel_icon(self):
        circle = Circle(radius=.65, color=PRUNE, stroke_width=3)
        hub = Dot(radius=.08, color=PRUNE)
        spokes = VGroup(*[
            Line(ORIGIN, [.58 * np.cos(i * PI / 3), .58 * np.sin(i * PI / 3), 0],
                 color=PRUNE, stroke_width=2) for i in range(6)
        ])
        return VGroup(circle, spokes, hub)

    def arc_icon(self):
        return VGroup(
            Arc(radius=.7, start_angle=-PI / 3, angle=4 * PI / 3,
                color=SPARSE, stroke_width=4),
            Arc(radius=.4, start_angle=-PI / 3, angle=4 * PI / 3,
                color=SPARSE, stroke_width=2, stroke_opacity=.55),
        )

    def activation_meter(self, value, color):
        bar = RoundedRectangle(width=4.2, height=.52, corner_radius=.15,
                               color=ZERO, fill_color=ZERO, fill_opacity=.15)
        fill = RoundedRectangle(width=3.9 * value, height=.36, corner_radius=.11,
                                stroke_width=0, fill_color=color, fill_opacity=.9)
        fill.align_to(bar, LEFT).shift(RIGHT * .14)
        number = label(f"activation  {value:.2f}", 20, color).next_to(bar, DOWN, buff=.25)
        return VGroup(bar, fill, number)

    def mapping_row(self, neuron, feature, color):
        left = card(neuron, color, 1.35, .72, 22, .12)
        arrow = Arrow(ORIGIN, RIGHT * 1.25, buff=0, color=MUTED,
                      stroke_width=3, tip_length=.16)
        right = card(feature, color, 2.35, .72, 21, .12)
        return VGroup(left, arrow, right).arrange(RIGHT, buff=.35)

    def rank_row(self, rank, name, value, color):
        rank_label = label(str(rank), 19, MUTED)
        concept = card(name, color, 2.0, .62, 19, .1)
        track = RoundedRectangle(width=3.0, height=.35, corner_radius=.1,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.12)
        fill = RoundedRectangle(width=2.7 * value, height=.22, corner_radius=.07,
                                stroke_width=0, fill_color=color, fill_opacity=.85)
        fill.align_to(track, LEFT).shift(RIGHT * .12)
        value_label = label(f"{value:.2f}", 18, color)
        return VGroup(rank_label, concept, VGroup(track, fill), value_label).arrange(RIGHT, buff=.25)

    def axes_box(self):
        frame = RoundedRectangle(width=6.3, height=5.0, corner_radius=.22,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.025)
        x = Arrow([-2.75, 0, 0], [2.75, 0, 0], buff=0,
                  color=MUTED, stroke_opacity=.48, stroke_width=2, tip_length=.15)
        y = Arrow([0, -2.2, 0], [0, 2.2, 0], buff=0,
                  color=MUTED, stroke_opacity=.48, stroke_width=2, tip_length=.15)
        return VGroup(frame, x, y)

    def direction(self, index, angle, length, name=None, origin=ORIGIN):
        origin = np.array(origin, dtype=float)
        rad = angle * DEGREES
        end = origin + np.array([length * np.cos(rad), length * np.sin(rad), 0])
        arrow = Arrow(origin, end, buff=.04, color=FEATURE_COLORS[index],
                      stroke_width=4, tip_length=.18)
        if name is None:
            return VGroup(arrow)
        tag = label(name, 20, FEATURE_COLORS[index]).move_to(origin + 1.14 * (end - origin))
        return VGroup(arrow, tag)

    def feature_space(self, radius=1.55, labels=False):
        axes = VGroup(
            Line([-radius * 1.25, 0, 0], [radius * 1.25, 0, 0],
                 color=MUTED, stroke_opacity=.32),
            Line([0, -radius * 1.25, 0], [0, radius * 1.25, 0],
                 color=MUTED, stroke_opacity=.32),
        )
        vectors = VGroup(*[
            self.direction(i, FEATURE_ANGLES[i], radius,
                           f"v{i+1}" if labels else None)
            for i in range(5)
        ])
        return VGroup(axes, vectors)

    def basis_panel(self, rotated):
        box = RoundedRectangle(width=3.4, height=4.65, corner_radius=.2,
                               color=ZERO, fill_color=ZERO, fill_opacity=.035)
        angle = 45 * DEGREES if rotated else 0
        ex = np.array([1.25 * np.cos(angle), 1.25 * np.sin(angle), 0])
        ey = np.array([-1.25 * np.sin(angle), 1.25 * np.cos(angle), 0])
        origin = np.array([0, .2, 0])
        axes = VGroup(
            Arrow(origin - ex, origin + ex, buff=0, color=WEIGHT,
                  stroke_width=2.5, tip_length=.12),
            Arrow(origin - ey, origin + ey, buff=0, color=PRUNE,
                  stroke_width=2.5, tip_length=.12),
        )
        point_position = origin + np.array([.95, .55, 0])
        point = Dot(point_position, radius=.1, color=ACCENT)
        guide = DashedLine(origin, point_position, color=ACCENT,
                           dash_length=.1, stroke_opacity=.65)
        coordinates = "(0.78, −0.35)" if rotated else "(0.8, 0.3)"
        tag = card(coordinates, ACCENT, 2.5, .68, 20, .11).move_to([0, -1.65, 0])
        title = label("rotated basis" if rotated else "original basis", 19, MUTED).move_to([0, 1.8, 0])
        return VGroup(box, axes, guide, point, title, tag)

    def semantic_panel(self, poly):
        box = RoundedRectangle(width=3.45, height=4.55, corner_radius=.22,
                               color=PRUNE if poly else GOOD,
                               fill_color=PRUNE if poly else GOOD, fill_opacity=.035)
        title = label("POLYSEMANTIC" if poly else "MONOSEMANTIC", 20,
                      PRUNE if poly else GOOD).move_to([0, 1.75, 0])
        neuron = Circle(radius=.5, color=ACCENT, fill_color=ACCENT, fill_opacity=.08)
        neuron_label = label("N", 24, ACCENT).move_to(neuron)
        targets = VGroup()
        links = VGroup()
        names = ("CAT", "WHEEL", "ARC") if poly else ("CAT",)
        for i, name in enumerate(names):
            y = .9 - i * .8 if poly else .0
            target = card(name, FEATURE_COLORS[(0, 1, 3)[i]], 1.45, .55, 16, .1)
            target.move_to([.95, y, 0])
            targets.add(target)
            links.add(Line([-.15, 0, 0], target.get_left(),
                           color=FEATURE_COLORS[(0, 1, 3)[i]], stroke_width=2))
        core = VGroup(neuron, neuron_label).move_to([-.85, .05, 0])
        result = label("one clear feature" if not poly else "multiple associations",
                       18, MUTED).move_to([0, -1.75, 0])
        return VGroup(box, title, links, core, targets, result)

    def poly_neuron_icon(self):
        neuron = Circle(radius=.72, color=PRUNE, fill_color=PRUNE, fill_opacity=.08)
        center = label("N", 27, PRUNE).move_to(neuron)
        cards = VGroup(
            card("CAT", WEIGHT, 1.35, .5, 15, .08).move_to([1.15, 1.0, 0]),
            card("WHEEL", PRUNE, 1.55, .5, 15, .08).move_to([1.35, 0, 0]),
            card("ARC", SPARSE, 1.35, .5, 15, .08).move_to([1.15, -1.0, 0]),
        )
        links = VGroup(*[
            Line([.5, 0, 0], item.get_left(), color=FEATURE_COLORS[(0, 1, 3)[i]],
                 stroke_width=2, stroke_opacity=.7)
            for i, item in enumerate(cards)
        ])
        return VGroup(links, neuron, center, cards)

    def neuron_view_panel(self):
        box = RoundedRectangle(width=3.35, height=4.7, corner_radius=.22,
                               color=MUTED, fill_color=MUTED, fill_opacity=.035)
        title = label("NEURON VIEW", 21, MUTED).move_to([0, 1.85, 0])
        rows = VGroup(*[
            card(f"Neuron {i+1}", MUTED, 2.2, .57, 17, .04) for i in range(5)
        ]).arrange(DOWN, buff=.17).move_to([0, -.15, 0])
        return VGroup(box, title, rows)

    def feature_view_panel(self):
        box = RoundedRectangle(width=3.35, height=4.7, corner_radius=.22,
                               color=ACCENT, fill_color=ACCENT, fill_opacity=.035)
        title = label("FEATURE VIEW", 21, ACCENT).move_to([0, 1.85, 0])
        space = self.feature_space(1.25, labels=False).move_to([0, -.1, 0])
        return VGroup(box, title, space)

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
