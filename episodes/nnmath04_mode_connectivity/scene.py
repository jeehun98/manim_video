"""Neural Network Mathematics 04: a visual experiment in mode connectivity."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def chip(value, color=WEIGHT, width=2.8, size=25):
    box = RoundedRectangle(width=width, height=.82, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.11)
    return VGroup(box, label(value, size, color, width - .2))


class NeuralMathModeConnectivity(Scene):
    DURATION = 114

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  04", 18, MUTED).move_to(UP * 7.3),
            label("서로 다른 두 신경망 사이에도 정답이 있을까?", 27).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:08 — Same task, different starting points.
        self.copy("같은 문제를 두 번 학습합니다", "θ₀ᴬ ≠ θ₀ᴮ",
                  "같은 구조와 데이터, 다른 초기값.\n둘 다 잘 풀지만 마지막 파라미터는 다릅니다.")
        left = self.mini_network(WEIGHT).move_to([-2.0, .6, 0])
        right = self.mini_network(SPARSE).move_to([2.0, .6, 0])
        tags = VGroup(chip("θA  ·  Low Loss", WEIGHT, 3.15, 22).move_to([-2.0, -2.2, 0]),
                      chip("θB  ·  Low Loss", SPARSE, 3.15, 22).move_to([2.0, -2.2, 0]))
        common = label("same task", 22, MUTED).move_to([0, 3.0, 0])
        self.show(VGroup(left, right, tags, common))
        self.to(8)

        # 00:08–00:15 — Two distant low-loss points.
        self.copy("두 개의 좋은 해", "PARAMETER SPACE",
                  "파라미터 공간에서는 서로 다른 두 점.\n둘 다 Low Loss인데, 정말 고립된 정답일까요?")
        a, b = self.ends()
        space = self.space_frame()
        points = VGroup(self.endpoint(a, "θA", WEIGHT),
                        self.endpoint(b, "θB", SPARSE),
                        DashedLine(a, b, color=MUTED, stroke_opacity=.5))
        self.show(VGroup(space, points))
        self.to(15)

        # 00:15–00:26 — Test the straight interpolation.
        self.copy("가장 단순한 실험", "t : 0  →  1",
                  "두 모델의 파라미터를 직선으로 섞습니다.\nt=0은 첫 모델, t=1은 두 번째 모델입니다.")
        a, b = self.ends()
        line = Line(a, b, color=ACCENT, stroke_width=5)
        moving = Dot(a, radius=.15, color=GOOD)
        formula = chip("θ(t) = (1−t)θA + tθB", ACCENT, 6.6, 28)
        formula.move_to([0, 2.9, 0])
        slider = self.slider().move_to([0, -2.25, 0])
        frame = RoundedRectangle(width=7.2, height=4.7, corner_radius=.25,
                                 stroke_color=MUTED, stroke_width=1.7,
                                 fill_color=MUTED, fill_opacity=.02)
        self.show(VGroup(frame, line, self.endpoint(a, "A", WEIGHT),
                         self.endpoint(b, "B", SPARSE), moving, formula, slider))
        self.play(moving.animate.move_to(b), run_time=2.0, rate_func=linear)
        self.to(26)

        # 00:26–00:37 — A possible barrier on that line.
        self.copy("중간 모델의 Loss를 재보면", "STRAIGHT LINE  ·  POSSIBLE BARRIER",
                  "양 끝은 좋지만 직선 중간에서는\nLoss가 높아질 수 있습니다.")
        chart = self.loss_chart(barrier=True)
        dots = VGroup(*[Dot(chart[2].point_from_proportion(t), radius=.08,
                            color=ACCENT if 0 < t < 1 else GOOD)
                        for t in (0, .25, .5, .75, 1)])
        values = label("t = 0      0.25      0.5      0.75      1", 20, MUTED)
        values.move_to([0, -2.6, 0])
        self.show(VGroup(chart, dots, values))
        self.to(37)

        # 00:37–00:46 — Pause on the false conclusion.
        self.copy("두 골짜기 사이에 장벽?", "WE TESTED ONLY ONE LINE",
                  "두 해가 분리된 듯 보입니다.\n하지만 확인한 것은 두 점 사이의 직선뿐입니다.")
        terrain = self.terrain()
        barrier = label("high Loss", 24, PRUNE).move_to([0, 2.45, 0])
        reminder = chip("직선만 확인했다", ACCENT, 4.1, 27).move_to([0, -2.75, 0])
        self.show(VGroup(terrain, barrier, reminder))
        self.to(46)

        # 00:46–00:56 — Reveal a side direction and a bypass.
        self.copy("공간에는 다른 방향이 있습니다", "LOOK BEYOND THE LINE",
                  "직선의 장벽만으로 분리를 결론낼 수 없습니다.\n옆 방향으로 돌아가는 길이 있을 수 있습니다.")
        a, b = self.ends(y=1.2)
        direct = DashedLine(a, b, color=PRUNE, dash_length=.16, stroke_width=3)
        barrier = Circle(radius=.58, stroke_color=PRUNE, fill_color=PRUNE,
                         fill_opacity=.22).move_to([0, 1.2, 0])
        bend = self.bypass(a, b, depth=-1.9)
        grid = VGroup(*[Line([-3.5, y, 0], [3.5, y, 0], color=MUTED,
                             stroke_opacity=.12) for y in np.linspace(-2.3, 2.1, 6)],
                      *[Line([x, -2.4, 0], [x, 2.2, 0], color=MUTED,
                             stroke_opacity=.12) for x in np.linspace(-3.3, 3.3, 9)])
        side = Arrow([0, .1, 0], [0, -2.05, 0], color=GOOD,
                     stroke_width=3, tip_length=.18)
        self.show(VGroup(grid, barrier, direct, bend,
                         self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE),
                         side, label("other direction", 21, GOOD).move_to([1.7, -1.8, 0])))
        self.to(56)

        # 00:56–01:05 — Main experiment: bend the path and flatten its loss.
        self.copy("경로를 휘어봅니다", "LOW-LOSS PATH  ·  CAN BE FOUND",
                  "높은 Loss 영역을 피해 경로를 휘면\n낮은 Loss를 유지하는 길이 발견될 수 있습니다.")
        a, b = self.ends(y=1.45)
        direct = Line(a, b, color=PRUNE, stroke_width=4)
        curved = self.bypass(a, b, depth=-1.25)
        points = VGroup(self.endpoint(a, "A", WEIGHT), self.endpoint(b, "B", SPARSE))
        top_tag = label("parameter path", 21, MUTED).move_to([0, 2.65, 0])
        chart = self.loss_chart(barrier=True).scale(.72).move_to([0, -2.25, 0])
        flat_chart = self.loss_chart(barrier=False).scale(.72).move_to([0, -2.25, 0])
        self.show(VGroup(direct, points, top_tag, chart))
        self.play(Transform(direct, curved), Transform(chart, flat_chart), run_time=2.2)
        self.to(65)

        # 01:05–01:12 — Give the result its name.
        self.copy("좋은 해들이 이어질 수 있습니다", "LOW LOSS  ·  CONNECTED",
                  "저손실 경로로 좋은 해들이 연결될 수 있습니다.\n이 현상이 Mode Connectivity입니다.")
        a, b = self.ends(y=1.3)
        path = self.bypass(a, b, depth=-1.2)
        title = label("Mode Connectivity", 39, ACCENT).move_to([0, -2.2, 0])
        self.show(VGroup(path, self.endpoint(a, "θA", WEIGHT),
                         self.endpoint(b, "θB", SPARSE), title))
        self.to(72)

        # 01:12–01:21 — The familiar 1D valleys are a slice.
        self.copy("익숙한 골짜기 그림", "LOW-DIMENSIONAL SLICE",
                  "고립된 골짜기 그림은\n고차원 공간의 낮은 차원 단면일 수 있습니다.")
        valleys = self.valley_profile()
        slice_tag = chip("one slice", MUTED, 2.6, 23).move_to([0, -2.7, 0])
        self.show(VGroup(valleys, slice_tag))
        self.to(81)

        # 01:21–01:31 — Emphasize the network of paths, not the points.
        self.copy("고차원에서는 연결 구조가 보일 수 있습니다", "POSSIBLE LOW-LOSS NETWORK",
                  "좋은 해들은 여러 경로로 이어진\n큰 저손실 구조의 일부일 수 있습니다.")
        nodes = {"A": np.array([-2.5, .1, 0]), "B": np.array([0, 2.1, 0]),
                 "C": np.array([2.5, .1, 0]), "D": np.array([0, -2.0, 0])}
        edges = VGroup()
        for u, v in (("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")):
            p, q = nodes[u], nodes[v]
            curve = VMobject(color=GOOD, stroke_width=4, stroke_opacity=.72)
            mid = (p + q) / 2 + .18 * np.array([-(q-p)[1], (q-p)[0], 0])
            curve.set_points_smoothly([p, mid, q])
            edges.add(curve)
        marks = VGroup(*[VGroup(Dot(p, radius=.13, color=ACCENT),
                                label("θ" + name, 23, INK).next_to(p, UP, buff=.16))
                         for name, p in nodes.items()])
        self.show(VGroup(edges, marks))
        self.to(91)

        # 01:31–01:42 — Return to episode 02's solution set.
        self.copy("2화의 해 집합을 다시 보면", "SOLUTION SET  +  CONNECTIVITY",
                  "좋은 해의 개수뿐 아니라\n서로 어떻게 연결되는지도 중요합니다.")
        region = Polygon([-3, -.8, 0], [-1.5, 1.65, 0], [.3, .85, 0],
                         [2.4, 1.7, 0], [3.0, -.7, 0], [1.2, -1.55, 0],
                         stroke_color=GOOD, fill_color=GOOD, fill_opacity=.14)
        goal_points = [np.array(p) for p in ((-2, -.3, 0), (-.5, .5, 0), (1.2, .35, 0),
                                             (2.15, -.55, 0))]
        paths = VGroup(*[Line(goal_points[i], goal_points[i+1], color=GOOD,
                              stroke_width=4, stroke_opacity=.8) for i in range(3)])
        starts = VGroup(*[Arrow(start, end, buff=.1, color=WEIGHT,
                                stroke_width=2.5, tip_length=.14)
                          for start, end in zip(([-3, -2.35, 0], [-1.05, -2.4, 0],
                                                 [1.1, -2.4, 0], [3.1, -2.3, 0]),
                                                goal_points)])
        targets = VGroup(*[Dot(p, radius=.11, color=ACCENT) for p in goal_points])
        self.show(VGroup(region, paths, starts, targets))
        self.to(102)

        # 01:42–01:54 — Local directions lead to the next question.
        self.copy("좋은 해의 주변은 어떤 모양일까?", "STEEP  vs  FLAT",
                  "조금만 움직여도 Loss가 커지는 방향과\n멀리 움직여도 거의 변하지 않는 방향은 왜 다를까요?")
        center = Dot([0, -.35, 0], radius=.17, color=ACCENT)
        steep = Arrow([0, -.15, 0], [0, 2.5, 0], buff=0, color=PRUNE,
                      stroke_width=5, tip_length=.22)
        flat = Arrow([.18, -.35, 0], [3.0, -.35, 0], buff=0, color=GOOD,
                     stroke_width=5, tip_length=.22)
        tags = VGroup(label("Loss ↑ quickly", 22, PRUNE).move_to([-1.5, 2.2, 0]),
                      label("Loss ≈ constant", 22, GOOD).move_to([1.5, -1.0, 0]),
                      label("좋은 해의 주변은 어떤 모양일까?", 29, ACCENT).move_to([0, -2.8, 0]))
        self.show(VGroup(center, steep, flat, tags))
        self.to(114)

    def mini_network(self, color):
        cols = ((-1.05, 3), (0, 4), (1.05, 3))
        dots = [[Dot([x, (i-(n-1)/2)*.6, 0], radius=.065, color=color)
                 for i in range(n)] for x, n in cols]
        links = VGroup(*[Line(p.get_center(), q.get_center(), color=color,
                              stroke_opacity=.3, stroke_width=1.4)
                         for left, right in zip(dots[:-1], dots[1:])
                         for p in left for q in right])
        return VGroup(links, *[p for col in dots for p in col])

    def ends(self, y=0):
        return np.array([-2.7, y, 0]), np.array([2.7, y, 0])

    def endpoint(self, point, name, color):
        return VGroup(Dot(point, radius=.13, color=color),
                      label(name, 23, color).next_to(point, UP, buff=.19))

    def space_frame(self):
        frame = RoundedRectangle(width=7.2, height=4.7, corner_radius=.25,
                                 stroke_color=MUTED, stroke_width=1.7,
                                 fill_color=MUTED, fill_opacity=.02)
        return VGroup(frame, label("parameter space", 21, MUTED).move_to([0, -2.8, 0]))

    def slider(self):
        line = Line([-2.6, 0, 0], [2.6, 0, 0], color=MUTED, stroke_width=3)
        ticks = VGroup(*[Line([x, -.12, 0], [x, .12, 0], color=MUTED)
                         for x in np.linspace(-2.6, 2.6, 5)])
        ends = VGroup(label("0", 21, INK).move_to([-2.6, -.4, 0]),
                      label("1", 21, INK).move_to([2.6, -.4, 0]))
        return VGroup(line, ticks, ends)

    def loss_chart(self, barrier=True):
        xaxis = Arrow([-3.0, -1.7, 0], [3.1, -1.7, 0], buff=0,
                      color=MUTED, stroke_width=2, tip_length=.14)
        yaxis = Arrow([-3.0, -1.9, 0], [-3.0, 2.1, 0], buff=0,
                      color=MUTED, stroke_width=2, tip_length=.14)
        curve = VMobject(color=PRUNE if barrier else GOOD, stroke_width=5)
        pts = []
        for t in np.linspace(0, 1, 60):
            height = (.18 + 2.5 * np.sin(np.pi*t)**2) if barrier else (.18 + .18*np.sin(np.pi*t)**2)
            pts.append([-2.75 + 5.6*t, -1.55 + height, 0])
        curve.set_points_smoothly(pts)
        names = VGroup(label("Loss", 19, MUTED).move_to([-3.25, 2.1, 0]),
                       label("t", 19, MUTED).move_to([3.13, -2.0, 0]),
                       label("A", 20, GOOD).move_to([-2.75, -2.05, 0]),
                       label("B", 20, GOOD).move_to([2.85, -2.05, 0]))
        return VGroup(xaxis, yaxis, curve, names)

    def terrain(self):
        path = VMobject(color=PRUNE, stroke_width=6)
        path.set_points_smoothly([[-3.1, -1.45, 0], [-2.25, -1.4, 0],
                                  [-1.1, -.5, 0], [0, 1.9, 0], [1.1, -.5, 0],
                                  [2.25, -1.4, 0], [3.1, -1.45, 0]])
        dots = VGroup(Dot([-2.25, -1.4, 0], radius=.13, color=WEIGHT),
                      Dot([2.25, -1.4, 0], radius=.13, color=SPARSE),
                      label("θA", 23, WEIGHT).move_to([-2.25, -1.95, 0]),
                      label("θB", 23, SPARSE).move_to([2.25, -1.95, 0]))
        return VGroup(path, dots)

    def bypass(self, a, b, depth=-1.6):
        path = VMobject(color=GOOD, stroke_width=5)
        path.set_points_smoothly([a, [-1.75, a[1]-1.15, 0],
                                  [0, depth, 0], [1.75, b[1]-1.15, 0], b])
        return path

    def valley_profile(self):
        curve = VMobject(color=WEIGHT, stroke_width=5)
        pts = [[x, .95*np.cos(2.5*x)+.25*np.cos(5*x)-.1, 0]
               for x in np.linspace(-3.25, 3.25, 90)]
        curve.set_points_smoothly(pts)
        marks = VGroup(*[Dot([x, .95*np.cos(2.5*x)+.25*np.cos(5*x)-.1, 0],
                             radius=.1, color=ACCENT) for x in (-1.25, 1.25)])
        return VGroup(curve, marks)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(width=7.65, height=1.15,
                                             corner_radius=.14, stroke_color=ZERO,
                                             stroke_width=1.2, fill_color=ZERO,
                                             fill_opacity=.32).move_to([0, -5.65, 0])
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
                [-3.8 + width/2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target-self.time))
