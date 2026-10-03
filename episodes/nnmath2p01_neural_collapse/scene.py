"""Neural Network Mathematics Part 2, episode 01: Neural Collapse."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


CLASS_COLORS = (WEIGHT, PRUNE, GOOD)
OFFSETS = (
    (-.62, .18), (-.35, .55), (-.12, -.42), (.18, .28),
    (.48, -.18), (.58, .48), (-.48, -.52), (.08, .68),
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=2.8, height=.9, size=24, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .2))


def marker(kind, point, color, scale=.14, opacity=1):
    if kind == 0:
        obj = Circle(radius=scale)
    elif kind == 1:
        obj = Triangle().scale(scale * 1.25)
    else:
        obj = Square(side_length=scale * 1.8)
    obj.set_stroke(color, width=2, opacity=opacity)
    obj.set_fill(color, opacity=.28 * opacity)
    return obj.move_to(point)


class NeuralMathPart2NeuralCollapse(Scene):
    DURATION = 110

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 01", 17, MUTED).move_to(UP * 7.3),
            label("분류만 하면 되는데 왜 클래스는 정삼각형을 만들까?", 28).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1,
            stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 1 — The ordinary goal: separate three classes.
        self.copy(
            "분류의 목표는 단순해 보입니다", "THREE CLASSES  ·  FEATURE SPACE",
            "세 종류의 데이터를 분류하는 신경망입니다.\n목표는 서로 다른 클래스를 구분하는 것입니다.",
        )
        frame = self.feature_frame()
        mixed = VGroup()
        mixed_points = [(-2.3, 1.4), (-1.45, -.2), (-.6, 1.0), (.2, -1.2),
                        (1.05, .7), (2.2, -.55), (-2.0, -1.55), (-.1, .2),
                        (1.8, 1.55), (.8, -1.8), (2.55, .35), (-1.0, 1.85)]
        for i, point in enumerate(mixed_points):
            kind = i % 3
            mixed.add(marker(kind, [point[0], point[1], 0], CLASS_COLORS[kind], .13))
        legend = self.legend().move_to([0, -2.85, 0])
        self.show(VGroup(frame, mixed, legend))
        self.to(6)

        # 2 — Irregular separation is already enough for classification.
        self.copy(
            "불규칙하게 떨어져 있어도 충분합니다", "TRAINING ERROR  ≈  0",
            "위치와 간격이 불규칙해도 세 그룹이 떨어져 있으면\n훈련 데이터를 정확히 분류할 수 있습니다.",
        )
        centers = ((-2.0, 1.15), (1.85, .85), (.2, -1.45))
        regions = VGroup(
            Ellipse(width=2.6, height=1.85, color=WEIGHT, fill_color=WEIGHT,
                    fill_opacity=.05).move_to([*centers[0], 0]),
            Ellipse(width=2.25, height=1.55, color=PRUNE, fill_color=PRUNE,
                    fill_opacity=.05).rotate(.25).move_to([*centers[1], 0]),
            Ellipse(width=2.8, height=1.4, color=GOOD, fill_color=GOOD,
                    fill_opacity=.05).rotate(-.18).move_to([*centers[2], 0]),
        )
        clusters = VGroup(*[self.cluster(i, centers[i], .52, 6) for i in range(3)])
        check = card("Accuracy  ≈  100%", GOOD, 4.1, .75, 24, .14).move_to([0, -2.75, 0])
        self.show(VGroup(self.feature_frame(), regions, clusters, check))
        self.to(12)

        # 3 — Epochs continue after accuracy saturation.
        self.copy(
            "그런데 학습은 여기서 멈추지 않습니다", "ACCURACY ≈ 100%   ·   EPOCH ↑",
            "정확도가 이미 거의 100%인데도 학습을 계속하면\n특정 조건에서 representation은 계속 변할 수 있습니다.",
        )
        epoch_cards = VGroup(*[
            card(str(v), ACCENT if v == 1000 else MUTED, 1.25, .62, 18,
                 .16 if v == 1000 else .05)
            for v in (100, 200, 500, 1000)
        ]).arrange(RIGHT, buff=.22).move_to([0, 2.15, 0])
        arrow = Arrow([-2.9, 1.45, 0], [2.9, 1.45, 0], buff=0,
                      color=ACCENT, stroke_width=3, tip_length=.16)
        clusters = VGroup(*[self.cluster(i, centers[i], .48, 6) for i in range(3)])
        accuracy = card("Training Accuracy", GOOD, 4.8, .72, 22).move_to([0, -2.55, 0])
        self.show(VGroup(epoch_cards, arrow, clusters, accuracy))
        self.play(clusters[0].animate.scale(.82), clusters[1].animate.scale(.82),
                  clusters[2].animate.scale(.82), run_time=1.0)
        self.to(18)

        # 4 — Within-class representations contract toward each mean.
        self.copy(
            "먼저 클래스 내부가 무너집니다", "h(xᵢ)  →  μc",
            "같은 클래스의 representation들이 평균으로 모이며\n클래스 내부의 차이가 작아집니다.",
        )
        start_centers = ((-2.15, 1.1), (1.95, .85), (.1, -1.45))
        groups = VGroup(*[self.cluster(i, start_centers[i], .68, 7) for i in range(3)])
        means = VGroup(*[
            Dot([*start_centers[i], 0], radius=.105, color=CLASS_COLORS[i]) for i in range(3)
        ])
        arrows = VGroup()
        for i, group in enumerate(groups):
            for point in group:
                arrows.add(Arrow(point.get_center(), means[i].get_center(), buff=.13,
                                 color=CLASS_COLORS[i], stroke_opacity=.35,
                                 stroke_width=1.5, tip_length=.09))
        self.show(VGroup(self.feature_frame(), arrows, groups, means))
        animations = []
        for i, group in enumerate(groups):
            center = np.array([*start_centers[i], 0])
            for point in group:
                animations.append(point.animate.move_to(center + .12 * (point.get_center() - center)))
        self.play(*animations, arrows.animate.set_stroke(opacity=.08), run_time=1.4)
        self.to(25)

        # 5 — Name the first visible component without introducing NC numbering.
        self.copy(
            "같은 클래스 안의 차이가 사라집니다", "WITHIN-CLASS VARIABILITY ↓",
            "Within-class variability가 사라지는 것은\nNeural Collapse의 첫 번째 특징입니다.",
        )
        before = VGroup(*[self.cluster(i, (-2.15, 1.55 - i * 1.55), .5, 6)
                          for i in range(3)])
        after = VGroup(*[
            marker(i, [2.0, 1.55 - i * 1.55, 0], CLASS_COLORS[i], .2)
            for i in range(3)
        ])
        arrows = VGroup(*[
            Arrow([-.75, 1.55 - i * 1.55, 0], [1.4, 1.55 - i * 1.55, 0],
                  buff=0, color=CLASS_COLORS[i], stroke_width=3, tip_length=.17)
            for i in range(3)
        ])
        self.show(VGroup(before, arrows, after,
                         label("many representations", 19, MUTED).move_to([-2.1, -2.75, 0]),
                         label("one class mean", 19, GOOD).move_to([2.0, -2.75, 0])))
        self.to(31)

        # 6 — Collapse within classes does not require symmetric means.
        self.copy(
            "하지만 중심은 아무렇게나 놓여도 됩니다", "ALREADY SEPARABLE",
            "클래스 중심은 불규칙하게 떨어져 있어도\n서로 구분만 된다면 충분합니다.",
        )
        irregular = ((-2.15, 1.45), (2.2, .35), (-.45, -1.65))
        means = VGroup(*[
            VGroup(marker(i, [*irregular[i], 0], CLASS_COLORS[i], .24),
                   label(f"μ{i+1}", 20, CLASS_COLORS[i]).next_to([*irregular[i], 0], UP, buff=.25))
            for i in range(3)
        ])
        boundaries = VGroup(
            DashedLine([-.7, 2.45, 0], [.55, -2.2, 0], color=MUTED, dash_length=.14),
            DashedLine([-2.9, -.4, 0], [2.8, -1.0, 0], color=MUTED, dash_length=.14),
        )
        self.show(VGroup(self.feature_frame(), boundaries, means,
                         card("100% classified", GOOD, 3.4, .72, 22, .13).move_to([0, -2.75, 0])))
        self.to(37)

        # 7 — The class means themselves approach a symmetric arrangement.
        self.copy(
            "그런데 중심들도 움직입니다", "LATE-TRAINING GEOMETRY",
            "학습 후반에는 세 중심이\n대칭적인 방향으로 이동할 수 있습니다.",
        )
        target = self.triangle_points(2.0)
        moving = VGroup(*[
            marker(i, [*irregular[i], 0], CLASS_COLORS[i], .24) for i in range(3)
        ])
        trails = VGroup(*[
            DashedLine([*irregular[i], 0], target[i], color=CLASS_COLORS[i],
                       dash_length=.12, stroke_opacity=.55) for i in range(3)
        ])
        self.show(VGroup(self.feature_frame(), trails, moving))
        self.play(*[moving[i].animate.move_to(target[i]) for i in range(3)], run_time=1.7)
        edges = VGroup(*[
            Line(target[i], target[(i + 1) % 3], color=MUTED, stroke_opacity=.55)
            for i in range(3)
        ])
        self.play(FadeIn(edges), run_time=.5)
        self.stage.add(edges)
        self.to(44)

        # 8 — Centering and normalization expose 120-degree directions.
        self.copy(
            "전체 중심을 빼고 방향을 정규화하면", "CENTER  ·  NORMALIZE  ·  120°",
            "전체 평균을 제거하고 정규화하면\n세 클래스 방향은 서로 120°씩 벌어집니다.",
        )
        origin = Dot(ORIGIN, radius=.07, color=MUTED)
        points = self.triangle_points(2.15)
        vectors = VGroup(*[
            Arrow(ORIGIN, points[i], buff=.14, color=CLASS_COLORS[i],
                  stroke_width=4, tip_length=.19) for i in range(3)
        ])
        means = VGroup(*[marker(i, points[i], CLASS_COLORS[i], .2) for i in range(3)])
        arcs = VGroup(*[
            Arc(radius=.72, start_angle=PI / 2 + i * TAU / 3,
                angle=TAU / 3, color=ACCENT, stroke_width=2.5)
            for i in range(3)
        ])
        angle_tags = VGroup(*[
            label("120°", 18, ACCENT).move_to(.95 * np.array([
                np.cos(PI / 2 + (i + .5) * TAU / 3),
                np.sin(PI / 2 + (i + .5) * TAU / 3), 0]))
            for i in range(3)
        ])
        equation = card("⟨μ̃ᵢ, μ̃ⱼ⟩ = −1/(C−1)   ·   i≠j", ACCENT,
                        6.4, .78, 22, .13).move_to([0, -2.72, 0])
        self.show(VGroup(origin, vectors, means, arcs, angle_tags, equation))
        self.to(52)

        # 9 — Triangle, tetrahedron, then the abstract C-class simplex.
        self.copy(
            "Simplex Equiangular Tight Frame", "SIMPLEX ETF",
            "서로 다른 방향의 내적이 같은 Simplex ETF.\n핵심은 균형 잡힌 대칭입니다.",
        )
        tri = self.simplex_triangle(.8).move_to([-2.55, .35, 0])
        tetra = self.tetrahedron().scale(.72).move_to([0, .35, 0])
        abstract = self.abstract_simplex().scale(.78).move_to([2.55, .35, 0])
        tags = VGroup(
            label("3 classes", 18, WEIGHT).move_to([-2.55, -1.75, 0]),
            label("4 classes", 18, PRUNE).move_to([0, -1.75, 0]),
            label("C classes", 18, GOOD).move_to([2.55, -1.75, 0]),
        )
        subspace = label("simplex lies in a (C−1)-dimensional subspace", 18, MUTED)
        subspace.move_to([0, -2.55, 0])
        self.show(VGroup(tri, tetra, abstract, tags, subspace))
        self.to(59)

        # 10 — Classifier weights align with centered class means.
        self.copy(
            "Classifier까지 같은 기하학에 맞춰집니다", "wc  ∥  μ̃c",
            "마지막 classifier의 weight도\n각 클래스 평균의 방향과 정렬될 수 있습니다.",
        )
        points = self.triangle_points(1.75)
        means = VGroup(*[marker(i, points[i], CLASS_COLORS[i], .2) for i in range(3)])
        mean_vectors = VGroup(*[
            Arrow(ORIGIN, points[i], buff=.18, color=CLASS_COLORS[i],
                  stroke_width=3, tip_length=.16) for i in range(3)
        ])
        initial_ends = ([-1.5, 1.4, 0], [1.75, .65, 0], [.25, -1.95, 0])
        weights = VGroup(*[
            Arrow(ORIGIN, initial_ends[i], buff=.1, color=INK,
                  stroke_width=5, tip_length=.2) for i in range(3)
        ])
        self.show(VGroup(mean_vectors, means, weights,
                         label("classifier weights", 20, INK).move_to([0, -2.65, 0])))
        aligned = VGroup(*[
            Arrow(ORIGIN, 1.32 * points[i], buff=.1, color=INK,
                  stroke_width=5, tip_length=.2) for i in range(3)
        ])
        self.play(Transform(weights, aligned), run_time=1.3)
        self.to(66)

        # 11 — The classifier agrees with nearest class center geometry.
        self.copy(
            "결정 규칙도 단순한 거리에 가까워집니다", "NEAREST CLASS CENTER",
            "가장 가까운 클래스 중심을 고르는 기하학이\nclassifier의 결정과 일치하게 됩니다.",
        )
        points = self.triangle_points(2.0)
        centers_group = VGroup(*[
            VGroup(marker(i, points[i], CLASS_COLORS[i], .22),
                   label(f"μ{i+1}", 19, CLASS_COLORS[i]).next_to(points[i], UP, buff=.22))
            for i in range(3)
        ])
        sample = Dot([.62, -.55, 0], radius=.12, color=INK)
        distances = VGroup(*[
            DashedLine(sample.get_center(), points[i], color=CLASS_COLORS[i],
                       dash_length=.12, stroke_opacity=.75 if i == 1 else .3)
            for i in range(3)
        ])
        result = card("Class 2", PRUNE, 2.4, .72, 24, .16).move_to([0, -2.65, 0])
        self.show(VGroup(centers_group, sample, distances,
                         label("h(x)", 20, INK).next_to(sample, RIGHT, buff=.18), result))
        self.to(73)

        # 12 — Recap the entire transformation without NC1–NC4 labels.
        self.copy(
            "분리에서 대칭까지", "NEURAL COLLAPSE",
            "분리 → 클래스 내부 붕괴 → 대칭적 배치\n→ classifier 정렬",
        )
        steps = VGroup(
            card("분리", WEIGHT, 1.45, .72, 21),
            label("→", 25, MUTED),
            card("내부 붕괴", PRUNE, 1.75, .72, 20),
            label("→", 25, MUTED),
            card("대칭", GOOD, 1.45, .72, 21),
            label("→", 25, MUTED),
            card("정렬", ACCENT, 1.45, .72, 21),
        ).arrange(RIGHT, buff=.12).move_to([0, 2.25, 0])
        initial = self.mini_mixed().move_to([-2.5, -.45, 0])
        collapsed = self.mini_triangle().move_to([0, -.45, 0])
        aligned = self.mini_aligned().move_to([2.5, -.45, 0])
        links = VGroup(
            Arrow([-1.55, -.45, 0], [-.95, -.45, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.13),
            Arrow([.95, -.45, 0], [1.55, -.45, 0], buff=0,
                  color=MUTED, stroke_width=2, tip_length=.13),
        )
        self.show(VGroup(steps, initial, collapsed, aligned, links))
        self.to(81)

        # 13 — Both geometries classify perfectly; only one is highly regular.
        self.copy(
            "왼쪽도 이미 정답입니다", "WHY THIS EXTRA REGULARITY?",
            "왼쪽도 이미 정답인데 왜 학습은\n오른쪽처럼 더 규칙적인 구조를 만들까요?",
        )
        left = self.irregular_means_panel().move_to([-2.0, .2, 0])
        right = self.symmetric_means_panel().move_to([2.0, .2, 0])
        equal = card("Training Accuracy  ≈  100%", GOOD, 5.0, .72, 22, .12)
        equal.move_to([0, -2.75, 0])
        self.show(VGroup(left, right, equal))
        self.to(88)

        # 14 — Link parameter-space selection to representation-space regularity.
        self.copy(
            "1부의 해 선택이 내부 구조로 나타납니다", "PARAMETER SPACE  →  REPRESENTATION SPACE",
            "Neural Collapse는 학습이 고른 해가 내부 representation에\n남긴 강한 규칙성으로 볼 수 있습니다.",
        )
        field = RoundedRectangle(width=3.0, height=4.1, corner_radius=.2,
                                 color=WEIGHT, fill_color=WEIGHT, fill_opacity=.035)
        field.move_to([-2.15, .15, 0])
        solutions = VGroup(*[
            Dot([-2.15 + x, .15 + y, 0], radius=.07, color=GOOD)
            for x, y in ((-.9, 1.3), (.6, 1.15), (-.7, -.1), (.75, -.65), (.15, .3))
        ])
        path = VMobject(color=ACCENT, stroke_width=4)
        path.set_points_smoothly([[-3.1, -1.5, 0], [-2.6, -.6, 0], [-2.0, -.35, 0], [-1.4, -.5, 0]])
        arrow = Arrow([-.45, .15, 0], [.55, .15, 0], buff=0,
                      color=MUTED, stroke_width=3, tip_length=.17)
        geometry = self.simplex_triangle(.95).move_to([2.15, .15, 0])
        self.show(VGroup(field, solutions, path, arrow, geometry,
                         label("many low-loss solutions", 18, MUTED).move_to([-2.15, -2.35, 0]),
                         label("selected geometry", 18, GOOD).move_to([2.15, -2.35, 0])))
        self.to(95)

        # 15 — Contrast architectural complexity and geometric simplicity.
        self.copy(
            "복잡한 신경망, 단순한 기하학", "COMPLEX NETWORK  →  SIMPLE GEOMETRY",
            "Complex Network\n→ Simple Geometry",
        )
        network = self.network().move_to([-2.15, .25, 0])
        geometry = self.simplex_triangle(1.1).move_to([2.15, .25, 0])
        arrow = Arrow([-.55, .25, 0], [.65, .25, 0], buff=0,
                      color=ACCENT, stroke_width=4, tip_length=.2)
        labels = VGroup(
            label("millions of parameters", 19, WEIGHT).move_to([-2.15, -2.45, 0]),
            label("120° · 120° · 120°", 20, GOOD).move_to([2.15, -2.45, 0]),
        )
        self.show(VGroup(network, arrow, geometry, labels))
        self.to(102)

        # 16 — End on the unresolved symmetry question.
        self.copy(
            "분류에는 필요 없어 보이는 대칭", "NEURAL COLLAPSE",
            "분류에 필요 없어 보이는 대칭을\n학습은 왜 만들어낼까요?",
        )
        geometry = self.simplex_triangle(1.35)
        overlays = VGroup()
        points = self.triangle_points(2.34)
        for i, point in enumerate(points):
            for j, (dx, dy) in enumerate(OFFSETS[:6]):
                overlays.add(marker(i, point + np.array([dx, dy, 0]) * .08,
                                    CLASS_COLORS[i], .07, .6))
        question = card("Why does learning create symmetry?", ACCENT,
                        6.7, .9, 25, .15).move_to([0, -2.8, 0])
        self.show(VGroup(geometry, overlays, question))
        self.to(110)

    def feature_frame(self):
        return RoundedRectangle(width=7.0, height=5.1, corner_radius=.25,
                                stroke_color=MUTED, stroke_width=1.8,
                                fill_color=MUTED, fill_opacity=.015)

    def legend(self):
        items = VGroup()
        for i, name in enumerate(("Class 1", "Class 2", "Class 3")):
            items.add(VGroup(marker(i, ORIGIN, CLASS_COLORS[i], .1),
                             label(name, 17, CLASS_COLORS[i])))
        return items.arrange(RIGHT, buff=.55)

    def cluster(self, kind, center, spread=.5, count=7):
        center = np.array([center[0], center[1], 0.0])
        return VGroup(*[
            marker(kind, center + np.array([dx, dy, 0]) * spread,
                   CLASS_COLORS[kind], .12)
            for dx, dy in OFFSETS[:count]
        ])

    def triangle_points(self, radius):
        return [np.array([radius * np.cos(PI / 2 + i * TAU / 3),
                          radius * np.sin(PI / 2 + i * TAU / 3), 0])
                for i in range(3)]

    def simplex_triangle(self, scale=1.0):
        points = self.triangle_points(1.65 * scale)
        edges = VGroup(*[
            Line(points[i], points[(i + 1) % 3], color=MUTED, stroke_width=2.5)
            for i in range(3)
        ])
        vertices = VGroup(*[
            marker(i, points[i], CLASS_COLORS[i], .19 * scale) for i in range(3)
        ])
        return VGroup(edges, vertices)

    def tetrahedron(self):
        pts = [np.array([0, 1.55, 0]), np.array([-1.25, -.75, 0]),
               np.array([1.25, -.75, 0]), np.array([0, -.1, 0])]
        edges = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                edges.add(Line(pts[i], pts[j], color=MUTED,
                               stroke_width=2, stroke_opacity=.7 if j < 3 else .35))
        vertices = VGroup(*[Dot(p, radius=.13, color=(WEIGHT, PRUNE, GOOD, ACCENT)[i])
                            for i, p in enumerate(pts)])
        return VGroup(edges, vertices)

    def abstract_simplex(self):
        pts = [np.array([1.45 * np.cos(PI / 2 + i * TAU / 5),
                         1.45 * np.sin(PI / 2 + i * TAU / 5), 0])
               for i in range(5)]
        edges = VGroup(*[
            Line(pts[i], pts[j], color=MUTED, stroke_opacity=.25, stroke_width=1.5)
            for i in range(5) for j in range(i + 1, 5)
        ])
        vertices = VGroup(*[Dot(p, radius=.11, color=(WEIGHT, PRUNE, GOOD, ACCENT, SPARSE)[i])
                            for i, p in enumerate(pts)])
        return VGroup(edges, vertices)

    def mini_mixed(self):
        group = VGroup()
        for i, (dx, dy) in enumerate(OFFSETS[:8]):
            kind = i % 3
            group.add(marker(kind, [dx, dy, 0], CLASS_COLORS[kind], .08))
        return group

    def mini_triangle(self):
        return self.simplex_triangle(.5)

    def mini_aligned(self):
        tri = self.simplex_triangle(.5)
        vectors = VGroup(*[
            Arrow(ORIGIN, p * .52, buff=.08, color=CLASS_COLORS[i],
                  stroke_width=2, tip_length=.11)
            for i, p in enumerate(self.triangle_points(1.65))
        ])
        return VGroup(tri, vectors)

    def irregular_means_panel(self):
        frame = RoundedRectangle(width=3.45, height=4.6, corner_radius=.2,
                                 color=MUTED, stroke_width=2)
        pts = ((-.95, 1.15), (.85, .55), (-.25, -1.2))
        means = VGroup(*[marker(i, [*pts[i], 0], CLASS_COLORS[i], .2) for i in range(3)])
        tag = label("irregular", 20, MUTED).move_to([0, -1.9, 0])
        return VGroup(frame, means, tag)

    def symmetric_means_panel(self):
        frame = RoundedRectangle(width=3.45, height=4.6, corner_radius=.2,
                                 color=GOOD, stroke_width=2)
        tri = self.simplex_triangle(.72)
        tag = label("symmetric", 20, GOOD).move_to([0, -1.9, 0])
        return VGroup(frame, tri, tag)

    def network(self):
        layers = (3, 5, 5, 3)
        xs = (-1.25, -.4, .45, 1.3)
        nodes = []
        group = VGroup()
        for li, count in enumerate(layers):
            layer = []
            for j in range(count):
                y = (j - (count - 1) / 2) * .62
                dot = Dot([xs[li], y, 0], radius=.075,
                          color=(MUTED, WEIGHT, SPARSE, GOOD)[li])
                layer.append(dot)
                group.add(dot)
            nodes.append(layer)
        lines = VGroup()
        for left, right in zip(nodes, nodes[1:]):
            for a in left:
                for b in right:
                    lines.add(Line(a.get_center(), b.get_center(), color=MUTED,
                                   stroke_width=.65, stroke_opacity=.22))
        return VGroup(lines, group)

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
