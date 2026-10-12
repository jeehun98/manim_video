"""Neural Network Mathematics Part 2, episode 12: Mode Connectivity."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.nnmath2p09_edge_of_stability.scene import (
    NeuralMathPart2EdgeOfStability, card, label,
)
from episodes.prune_series.visuals import ACCENT, GOOD, MUTED, PRUNE, SPARSE, WEIGHT, ZERO


class NeuralMathPart2ModeConnectivity(NeuralMathPart2EdgeOfStability):
    DURATION = 173

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        title = VGroup(label("Mode Connectivity", 24, ACCENT),
                       label("서로 다른 두 minimum은 정말 떨어져 있을까?", 21))
        title.arrange(DOWN, buff=.1).move_to(UP * 6.55)
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 12", 16, MUTED).move_to(UP * 7.55),
            title,
            Line([-3.8, 5.75, 0], [3.8, 5.75, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0], color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        self.copy("같은 문제를 두 번 학습했습니다", "SAME TASK · DIFFERENT INITIALIZATION",
                  "구조와 data는 같지만 시작 weight가 다릅니다.\n두 모델 모두 낮은 Loss에 도착했지만 parameter는 다릅니다.")
        nets = self.network_pair()
        self.show(nets)
        self.to(7)

        self.copy("파라미터 공간에서 두 해는 멀리 떨어져 있습니다", "DISTANCE  ∥θA − θB∥",
                  "두 신경망을 점으로 바꾸면 A와 B 사이의 거리가 보입니다.\n그러면 서로 다른 골짜기에 도착한 것처럼 보입니다.")
        self.show(self.parameter_distance())
        self.to(16)

        self.copy("우리는 보통 loss landscape를 이렇게 상상합니다", "THE FAMILIAR PICTURE",
                  "A와 B가 각각 다른 골짜기의 minimum이고,\n그 사이에는 높은 Loss의 산이 있다고 생각하기 쉽습니다.")
        self.show(self.double_basin())
        self.to(25)

        self.copy("가장 짧은 직선으로 두 모델을 연결해 봅시다", "LINEAR INTERPOLATION",
                  "theta of t를 A와 B의 가중평균으로 두면\n양 끝의 Loss는 낮지만 중간 모델의 Loss는 크게 올라갈 수 있습니다.")
        direct = self.straight_barrier()
        self.show(direct)
        self.play(MoveAlongPath(direct[-1], direct[1]), run_time=1.3, rate_func=linear)
        self.to(35)

        self.copy("직선만 보면 두 해는 분리된 것처럼 보입니다", "A AND B ARE DISCONNECTED?",
                  "중간의 높은 장벽을 보면 결론이 명확해 보입니다.\n하지만 우리가 확인한 것은 두 점 사이의 직선 하나뿐입니다.")
        self.show(self.false_conclusion())
        self.to(42)

        self.copy("지금까지 본 풍경은 전체 공간이 아닙니다", "IT WAS ONLY A SLICE",
                  "loss landscape 시각화는 거대한 parameter space의 몇 방향을\n잘라낸 단면입니다. 화면 밖의 방향은 보이지 않았습니다.")
        flat = self.slice_view(False)
        tilted = self.slice_view(True)
        self.show(flat)
        self.play(ReplacementTransform(flat, tilted), run_time=1.4)
        self.stage = tilted
        self.to(51)

        self.copy("보이지 않던 방향으로 먼저 이동하면 어떨까요?", "A HIDDEN DIRECTION OPENS",
                  "A에서 B로 바로 가지 않고 새로 열린 축으로 빠져나가면\n산을 넘는 대신 옆으로 돌아가는 길이 생깁니다.")
        bypass = self.hidden_bypass()
        self.show(bypass)
        self.play(MoveAlongPath(bypass[-1], bypass[2]), run_time=1.5, rate_func=smooth)
        self.to(58)

        self.copy("시작과 도착은 같고 경로만 다릅니다", "STRAIGHT  vs  CURVED",
                  "직선은 높은 Loss를 지나지만,\n굽은 경로는 양 끝 사이에서 낮은 Loss를 유지할 수 있습니다.")
        self.show(self.path_comparison())
        self.to(66)

        self.copy("서로 다른 solution이 낮은 Loss의 길로 이어질 수 있습니다", "MODE CONNECTIVITY",
                  "gamma의 시작은 theta A, 끝은 theta B입니다.\n경로 위의 모델들이 낮은 Loss를 유지하는 현상을 Mode Connectivity라고 합니다.")
        self.show(self.mode_definition())
        self.to(75)

        self.copy("직선의 장벽은 전체 공간의 장벽이 아닙니다", "LINE BARRIER  ≠  DISCONNECTED",
                  "linear interpolation이 실패했다는 사실만으로\n두 해가 parameter space에서 완전히 분리됐다고 말할 수는 없습니다.")
        self.show(self.line_not_space())
        self.to(84)

        self.copy("차원이 열리면 우회할 선택지도 늘어납니다", "2D  →  3D  →  HIGH-D",
                  "2차원에서는 벽 하나가 길을 막지만 차원을 하나 더 열면 우회할 수 있습니다.\n고차원에서 한 방향이 막혔다고 모든 방향이 막힌 것은 아닙니다.")
        self.show(self.dimension_escape())
        self.to(92)

        self.copy("단면의 산이 전체 공간을 막는 것은 아닙니다", "ONE PATH BARRIER  ≠  GLOBAL DISCONNECTION",
                  "높은 산처럼 보인 구조도 고차원에서는\n다른 방향으로 우회할 수 있는 ridge나 장벽의 일부일 수 있습니다.")
        ridge_a = self.ridge_view(False)
        ridge_b = self.ridge_view(True)
        self.show(ridge_a)
        self.play(ReplacementTransform(ridge_a, ridge_b), run_time=1.2)
        self.stage = ridge_b
        self.to(102)

        self.copy("그런데 직선의 장벽에는 다른 문제도 있습니다", "SECOND REVERSAL · PARAMETER ALIGNMENT",
                  "장벽의 일부는 지형이 아니라 두 모델의 parameter 좌표가\n서로 정렬되지 않아서 생겼을 수 있습니다.")
        perm_a = self.permutation_network(False)
        perm_b = self.permutation_network(True)
        self.show(perm_a)
        self.play(ReplacementTransform(perm_a, perm_b), run_time=1.1)
        self.stage = perm_b
        self.to(114)

        self.copy("좌표 순서 그대로 평균내면 서로 다른 feature가 섞입니다", "MISALIGNED AVERAGE",
                  "A의 첫 neuron과 B의 첫 neuron이 같은 역할이라는 보장은 없습니다.\n대응이 틀린 채 평균내면 중간 모델의 기능이 깨질 수 있습니다.")
        self.show(self.feature_mix(False))
        self.to(123)

        self.copy("대응하는 neuron을 먼저 정렬하면 그림이 달라집니다", "ALIGN → INTERPOLATE",
                  "일부 설정에서는 permutation을 맞춘 뒤 직선 Loss barrier가 크게 줄어듭니다.\n함수적으로는 가까운데 parameter의 이름표가 달라 멀어 보였을 수 있습니다.")
        before = self.feature_mix(False)
        after = self.feature_mix(True)
        self.show(before)
        self.play(ReplacementTransform(before, after), run_time=1.2)
        self.stage = after
        self.to(136)

        self.copy("서로 다른 골짜기가 아니라 같은 협곡일 수 있습니다", "ONE CONNECTED LOW-LOSS CANYON",
                  "좋은 해들이 고립된 웅덩이처럼 떨어져 있는 것이 아니라,\n구불구불한 low-loss 협곡 바닥의 멀리 떨어진 지점일 수 있습니다.")
        self.show(self.connected_region())
        self.to(146)

        self.copy("파라미터 거리와 분리는 같은 말이 아닙니다", "FAR APART  ≠  DISCONNECTED",
                  "A와 B의 Euclidean distance가 크더라도\n낮은 Loss를 유지하는 굽은 경로가 존재할 수 있습니다.")
        self.show(self.far_but_connected())
        self.to(157)

        self.copy("한 직선에 산이 보였다고 전체 공간이 막힌 것은 아닙니다", "MODE CONNECTIVITY",
                  "두 해가 사실은 하나의 거대한 low-loss 협곡 위의 두 지점일 수 있습니다.\n서로 다른 해 사이에도 낮은 Loss를 유지하는 길이 존재할 수 있습니다.")
        self.show(self.final_summary())
        self.to(173)

    def mini_network(self, color, swap=False):
        xs = (-1.05, 0, 1.05)
        counts = (3, 4, 2)
        cols = []
        for x, n in zip(xs, counts):
            colors = [color] * n
            if x == 0:
                colors = [GOOD, ACCENT, SPARSE, PRUNE]
                if swap:
                    colors = [ACCENT, GOOD, SPARSE, PRUNE]
            cols.append([Dot([x, (i-(n-1)/2)*.62, 0], radius=.075, color=colors[i]) for i in range(n)])
        links = VGroup(*[Line(p, q, color=color, stroke_opacity=.28, stroke_width=1.3)
                         for left, right in zip(cols[:-1], cols[1:]) for p in left for q in right])
        return VGroup(links, *[p for col in cols for p in col])

    def network_pair(self):
        a = VGroup(self.mini_network(WEIGHT), card("θA  ·  LOW LOSS", WEIGHT, 3.2, .72, 21, .12))
        a.arrange(DOWN, buff=.75)
        b = VGroup(self.mini_network(SPARSE, True), card("θB  ·  LOW LOSS", SPARSE, 3.2, .72, 21, .12))
        b.arrange(DOWN, buff=.75)
        return VGroup(a, b).arrange(RIGHT, buff=.7).move_to([0, .15, 0])

    def endpoint(self, point, text, color):
        return VGroup(Dot(point, radius=.14, color=color), label(text, 22, color).next_to(point, UP, buff=.18))

    def parameter_distance(self):
        a, b = np.array([-2.75, .2, 0]), np.array([2.75, .2, 0])
        frame = RoundedRectangle(width=7.4, height=4.5, corner_radius=.2,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.08)
        line = DashedLine(a, b, color=MUTED, dash_length=.16)
        return VGroup(frame, line, self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE),
                      card("∥θA − θB∥  ≫  0", ACCENT, 4.5, .78, 28, .14).move_to([0, -2.2, 0]))

    def double_basin(self):
        xs = np.linspace(-3.25, 3.25, 150)
        ys = .23*(xs**2-4.0)**2 - 1.2
        ys = np.clip(ys, -1.2, 2.5)
        curve = VMobject(stroke_color=WEIGHT, stroke_width=5).set_points_smoothly(
            [np.array([x, y, 0]) for x, y in zip(xs, ys)])
        return VGroup(curve, self.endpoint([-2, -1.2, 0], "A", WEIGHT),
                      self.endpoint([2, -1.2, 0], "B", SPARSE),
                      label("HIGH LOSS", 20, PRUNE).move_to([0, 2.2, 0]))

    def loss_curve(self, barrier=True, width=5.3):
        pts = []
        for t in np.linspace(0, 1, 100):
            h = .18 + (2.1 if barrier else .12) * np.sin(np.pi*t)**2
            pts.append(np.array([-width/2 + width*t, -1.45 + h, 0]))
        return VMobject(stroke_color=PRUNE if barrier else GOOD, stroke_width=4).set_points_smoothly(pts)

    def straight_barrier(self):
        a, b = np.array([-2.7, 1.65, 0]), np.array([2.7, 1.65, 0])
        path = Line(a, b, color=ACCENT, stroke_width=4)
        moving = Dot(a, radius=.12, color=GOOD)
        formula = card("θ(t) = (1−t)θA + tθB", ACCENT, 6.4, .82, 27, .13).move_to([0, 2.65, 0])
        chart = VGroup(Line([-3, -1.55, 0], [3, -1.55, 0], color=MUTED), self.loss_curve(True),
                       label("A", 18, WEIGHT).move_to([-2.65, -1.9, 0]),
                       label("B", 18, SPARSE).move_to([2.65, -1.9, 0]))
        return VGroup(formula, path, self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE), chart, moving)

    def false_conclusion(self):
        return VGroup(self.double_basin().scale(.9).move_to([0, .35, 0]),
                      card("A와 B는 서로 다른 basin?", PRUNE, 6.3, .88, 27, .14).move_to([0, -2.55, 0]))

    def slice_view(self, tilted):
        if not tilted:
            plane = RoundedRectangle(width=7.1, height=4.2, corner_radius=.18,
                                     color=WEIGHT, fill_color=WEIGHT, fill_opacity=.04)
            barrier = Ellipse(width=1.35, height=3.2, color=PRUNE,
                              fill_color=PRUNE, fill_opacity=.22)
            return VGroup(plane, barrier, self.endpoint([-2.75, 0, 0], "A", WEIGHT),
                          self.endpoint([2.75, 0, 0], "B", SPARSE),
                          label("2D SLICE", 22, WEIGHT).move_to([0, -2.55, 0]))
        plane = Polygon([-3.45, -1.55, 0], [2.6, -2.2, 0], [3.45, 1.3, 0], [-2.6, 1.95, 0],
                        color=WEIGHT, fill_color=WEIGHT, fill_opacity=.045)
        grid = VGroup(*[Line([-3.25+i*.7, -1.5+i*.075, 0], [-2.4+i*.7, 1.88+i*.075, 0],
                                 color=MUTED, stroke_opacity=.14) for i in range(9)])
        depth = Arrow([-3.0, -1.7, 0], [-3.0, 2.65, 0], color=GOOD, stroke_width=4)
        return VGroup(plane, grid, depth, label("hidden direction", 20, GOOD).move_to([-2.05, 2.5, 0]),
                      self.endpoint([-2.45, -.45, 0], "A", WEIGHT), self.endpoint([2.45, -.95, 0], "B", SPARSE))

    def curved_path(self, a, b, color=GOOD, depth=-1.6):
        path = VMobject(stroke_color=color, stroke_width=5)
        path.set_points_smoothly([a, [-1.6, depth, 0], [0, depth-.35, 0], [1.6, depth, 0], b])
        return path

    def hidden_bypass(self):
        a, b = np.array([-2.8, 1.0, 0]), np.array([2.8, 1.0, 0])
        grid = VGroup(*[Line([-3.4, y, 0], [3.4, y, 0], color=MUTED, stroke_opacity=.1)
                        for y in np.linspace(-2.3, 2.2, 7)],
                      *[Line([x, -2.3, 0], [x, 2.2, 0], color=MUTED, stroke_opacity=.1)
                        for x in np.linspace(-3.4, 3.4, 9)])
        obstacle = Ellipse(width=1.6, height=2.3, color=PRUNE, fill_color=PRUNE, fill_opacity=.23)
        path = self.curved_path(a, b, GOOD, -1.45)
        moving = Dot(a, radius=.12, color=ACCENT)
        return VGroup(grid, obstacle, path, self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE), moving)

    def mini_path_panel(self, title, curved):
        frame = RoundedRectangle(width=3.5, height=4.45, corner_radius=.2,
                                 color=GOOD if curved else PRUNE,
                                 fill_color=GOOD if curved else PRUNE, fill_opacity=.025)
        a, b = np.array([-1.25, 1.05, 0]), np.array([1.25, 1.05, 0])
        obstacle = Circle(radius=.42, color=PRUNE, fill_color=PRUNE, fill_opacity=.2).move_to([0, 1.05, 0])
        path = self.curved_path(a, b, GOOD, -.15) if curved else Line(a, b, color=PRUNE, stroke_width=4)
        loss = self.loss_curve(not curved, 2.4).scale(.75).move_to([0, -1.0, 0])
        return VGroup(frame, label(title, 20, GOOD if curved else PRUNE).move_to([0, 1.85, 0]),
                      obstacle, path, Dot(a, radius=.08, color=WEIGHT), Dot(b, radius=.08, color=SPARSE), loss)

    def path_comparison(self):
        return VGroup(self.mini_path_panel("STRAIGHT PATH", False),
                      self.mini_path_panel("CURVED PATH", True)).arrange(RIGHT, buff=.35).move_to([0, .1, 0])

    def mode_definition(self):
        a, b = np.array([-2.8, 1.2, 0]), np.array([2.8, 1.2, 0])
        path = self.curved_path(a, b, GOOD, -1.0)
        dots = VGroup(*[Dot(path.point_from_proportion(t), radius=.08, color=ACCENT)
                        for t in np.linspace(0, 1, 9)])
        return VGroup(path, dots, self.endpoint(a, "γ(0)=θA", WEIGHT), self.endpoint(b, "γ(1)=θB", SPARSE),
                      card("L(γ(t))  ≈  LOW", GOOD, 4.7, .8, 28, .14).move_to([0, -2.15, 0]),
                      label("MODE CONNECTIVITY", 27, ACCENT).move_to([0, 2.65, 0]))

    def line_not_space(self):
        left = VGroup(card("STRAIGHT-LINE BARRIER", PRUNE, 5.8, .85, 24, .12), label("≠", 44, ACCENT),
                      card("DISCONNECTED SOLUTIONS", WEIGHT, 5.8, .85, 23, .12))
        left.arrange(DOWN, buff=.5).move_to([0, .2, 0])
        return left

    def dimension_escape(self):
        left_frame = RoundedRectangle(width=3.35, height=4.4, corner_radius=.2, color=PRUNE)
        wall = Rectangle(width=.42, height=3.1, fill_color=PRUNE, fill_opacity=.35,
                         stroke_color=PRUNE).move_to([0, .1, 0])
        left = VGroup(left_frame, wall, Dot([-1.15, .1, 0], color=WEIGHT), Dot([1.15, .1, 0], color=SPARSE),
                      label("2D · BLOCKED", 19, PRUNE).move_to([0, 1.75, 0]))
        right_frame = RoundedRectangle(width=3.35, height=4.4, corner_radius=.2, color=GOOD)
        wall2 = Rectangle(width=.42, height=2.1, fill_color=PRUNE, fill_opacity=.3,
                          stroke_color=PRUNE)
        path = ArcBetweenPoints([-1.15, -.55, 0], [1.15, -.55, 0], angle=-PI*.85, color=GOOD, stroke_width=4)
        right = VGroup(right_frame, wall2, path, Dot([-1.15, -.55, 0], color=WEIGHT), Dot([1.15, -.55, 0], color=SPARSE),
                       label("3D · BYPASS", 19, GOOD).move_to([0, 1.75, 0]))
        return VGroup(left, right).arrange(RIGHT, buff=.4).move_to([0, .15, 0])

    def ridge_view(self, side):
        frame = RoundedRectangle(width=7.0, height=4.4, corner_radius=.2, color=ZERO,
                                 fill_color=ZERO, fill_opacity=.08)
        if not side:
            ridge = self.loss_curve(True, 6.0).scale(1.25).move_to([0, .2, 0])
            text = label("front view · mountain", 21, PRUNE).move_to([0, -2.2, 0])
        else:
            ridge = Rectangle(width=5.8, height=.34, color=PRUNE, fill_color=PRUNE, fill_opacity=.35)
            bypass = ArcBetweenPoints([-2.7, -.8, 0], [2.7, -.8, 0], angle=-PI*.55, color=GOOD, stroke_width=5)
            text = label("another direction · bypass exists", 20, GOOD).move_to([0, -2.2, 0])
            return VGroup(frame, ridge, bypass, text)
        return VGroup(frame, ridge, text)

    def permutation_network(self, swapped):
        net = self.mini_network(WEIGHT, swapped).scale(1.25).move_to([0, .55, 0])
        order = "[ EAR, FACE ]" if not swapped else "[ FACE, EAR ]"
        return VGroup(net, card(order, ACCENT, 5.1, .78, 25, .13).move_to([0, -2.25, 0]),
                      label("fθA(x) = fθB(x)   ·   θA ≠ θB", 23, GOOD).move_to([0, 2.75, 0]))

    def feature_mix(self, aligned):
        a = VGroup(card("EAR", WEIGHT, 2.2, .7, 21, .12), card("FACE", SPARSE, 2.2, .7, 21, .12)).arrange(DOWN, buff=.3)
        if aligned:
            b = VGroup(card("EAR", WEIGHT, 2.2, .7, 21, .12), card("FACE", SPARSE, 2.2, .7, 21, .12)).arrange(DOWN, buff=.3)
            result = card("LOW LINEAR BARRIER", GOOD, 5.2, .78, 22, .14)
        else:
            b = VGroup(card("FACE", SPARSE, 2.2, .7, 21, .12), card("EAR", WEIGHT, 2.2, .7, 21, .12)).arrange(DOWN, buff=.3)
            result = card("MIXED FEATURES · HIGH LOSS", PRUNE, 5.5, .78, 21, .13)
        top = VGroup(VGroup(label("MODEL A", 18, MUTED), a).arrange(DOWN, buff=.28),
                     label("AVERAGE", 20, ACCENT),
                     VGroup(label("MODEL B", 18, MUTED), b).arrange(DOWN, buff=.28)).arrange(RIGHT, buff=.48)
        return VGroup(top, label("↓", 30, MUTED), result).arrange(DOWN, buff=.55).move_to([0, .15, 0])

    def connected_region(self):
        canyon_points = [[-3.1, -.3, 0], [-2.15, 1.1, 0], [-.75, .45, 0],
                         [.45, -.8, 0], [1.7, .65, 0], [3.1, -.15, 0]]
        canyon = VMobject(stroke_color=GOOD, stroke_width=58, stroke_opacity=.16)
        canyon.set_points_smoothly(canyon_points)
        center = VMobject(stroke_color=GOOD, stroke_width=4, stroke_opacity=.9)
        center.set_points_smoothly(canyon_points)
        pts = [(-2.55, .45, "A"), (-.8, .45, "B"), (.5, -.7, "C"), (2.25, .35, "D")]
        marks = VGroup(*[self.endpoint([x, y, 0], name, ACCENT) for x, y, name in pts])
        return VGroup(canyon, center, marks)

    def far_but_connected(self):
        a, b = np.array([-3.0, 1.15, 0]), np.array([3.0, 1.15, 0])
        distance = DashedLine(a, b, color=MUTED, dash_length=.13)
        path = self.curved_path(a, b, GOOD, -1.25)
        return VGroup(distance, path, self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE),
                      card("FAR APART  ≠  DISCONNECTED", ACCENT, 6.4, .88, 27, .15).move_to([0, -2.35, 0]))

    def final_summary(self):
        chain = VGroup(card("A  ──  B", PRUNE, 4.5, .72, 24, .11), label("직선 barrier", 18, PRUNE),
                       label("↓  hidden directions", 22, MUTED),
                       card("A  ╰─╮  B", GOOD, 4.5, .72, 24, .12), label("low-loss path", 18, GOOD),
                       card("SAME LOW-LOSS CANYON", GOOD, 5.7, .72, 20, .12),
                       card("BARRIER ON A LINE  ≠  BARRIER IN SPACE", ACCENT, 7.0, .86, 21, .14))
        chain.arrange(DOWN, buff=.2).move_to([0, .15, 0])
        return chain
