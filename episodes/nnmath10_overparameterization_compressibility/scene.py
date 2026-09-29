"""Neural Network Mathematics 10: finding versus representing a solution."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, size=25, height=.85):
    box = RoundedRectangle(width=width, height=height, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.10)
    return VGroup(box, label(value, size, color, width-.18))


class NeuralMathOverparameterizationCompressibility(Scene):
    DURATION = 87

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  10", 18, MUTED).move_to(UP*7.3),
            label("작게 만들 수 있는데 왜 크게 학습할까?", 27).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 1: a conditional compression case, with stable behavior.
        self.copy("큰 모델을 학습한 뒤 줄인다", "100M  →  70M  →  20M",
                  "학습 후 압축해도 성능이\n상당히 유지되는 경우가 있습니다.")
        sizes = VGroup(card("100M", WEIGHT, 1.75, 27), card("70M", SPARSE, 1.75, 27),
                       card("20M", GOOD, 1.75, 27)).arrange(RIGHT, buff=.54).move_to([0, 1.35, 0])
        graph = self.performance_graph()
        self.show(VGroup(sizes, graph))
        self.to(6)

        # 2: the tempting shortcut.
        self.copy("그럼 처음부터 작게?", "SMALL MODEL  →  TRAIN",
                  "작은 모델에 답이 담긴다면\n처음부터 그 크기로 시작하면 될까요?")
        large = card("100M", WEIGHT, 2.1, 30).move_to([-2, .8, 0])
        small = card("20M", GOOD, 2.1, 30).move_to([2, .8, 0])
        shortcut = CurvedArrow([-1.2, 1.15, 0], [1.1, 1.15, 0], angle=-TAU/7,
                               color=ACCENT, stroke_width=3)
        question = card("Start training here?", GOOD, 5.7, 27).move_to([0, -1.5, 0])
        self.show(VGroup(large, small, shortcut, question))
        self.to(11)

        # 3: different training routes.
        self.copy("같은 최적화 문제는 아닙니다", "TRAIN LARGE  ≠  TRAIN SMALL",
                  "큰 모델을 학습한 뒤 줄이는 것과\n처음부터 작게 학습하는 것은 다릅니다.")
        left = self.route_panel("Large → Train", "→ Compress", WEIGHT, GOOD)
        right = self.route_panel("Small → Train", "?", SPARSE, PRUNE)
        left.move_to([-1.9, 0, 0]); right.move_to([1.9, 0, 0])
        self.show(VGroup(left, right))
        self.to(17)

        # 4: representable and reachable.
        self.copy("8화의 구분이 돌아옵니다", "REPRESENTABLE  ≠  REACHABLE",
                  "좋은 답이 존재하는 것과\n학습으로 찾는 것은 별개입니다.")
        frame = RoundedRectangle(width=6.9, height=4.5, corner_radius=.25,
                                 stroke_color=SPARSE, fill_color=SPARSE, fill_opacity=.04)
        star = label("★", 55, GOOD).move_to([2.05, .8, 0])
        start = Dot([-2.3, -.9, 0], radius=.12, color=WEIGHT)
        tag = label("good solution", 22, GOOD).next_to(star, DOWN, buff=.24)
        labels = VGroup(label("exists", 22, GOOD).move_to([1.9, -1.85, 0]),
                        label("path?", 22, PRUNE).move_to([-1.8, -1.85, 0]))
        self.show(VGroup(frame, star, start, tag, labels))
        self.to(23)

        # 5: an optimization path can miss a good solution.
        self.copy("작은 공간의 제한된 경로", "SOLUTION EXISTS  ·  PATH IS HARD",
                  "작은 모델에도 좋은 해는 있지만\n그곳에 가는 길을 찾기 어려울 수 있습니다.")
        frame = RoundedRectangle(width=6.9, height=4.7, corner_radius=.24,
                                 stroke_color=SPARSE, fill_color=SPARSE, fill_opacity=.035)
        traj = self.polyline([[-2.5, -.9, 0], [-1.3, -.4, 0], [-.25, -1.15, 0],
                              [.9, -1.45, 0]], PRUNE, 5)
        target = label("★", 55, GOOD).move_to([1.55, 1.05, 0])
        end = Dot([.9, -1.45, 0], radius=.12, color=PRUNE)
        self.show(VGroup(frame, traj, Dot([-2.5, -.9, 0], color=WEIGHT),
                         target, end, label("missed", 21, PRUNE).next_to(end, DOWN)))
        self.to(29)

        # 6: parameter expansion also changes optimization directions.
        self.copy("움직일 방향도 늘어납니다", "Rᵈ  →  Rᴰ     D ≫ d",
                  "파라미터가 늘면 함수 표현뿐 아니라\n학습이 움직이는 방향도 바뀝니다.")
        small_space = Rectangle(width=4.3, height=2.2, color=SPARSE,
                                fill_color=SPARSE, fill_opacity=.09).move_to([0, -.45, 0])
        big_space = Rectangle(width=6.8, height=4.65, color=WEIGHT,
                              fill_color=WEIGHT, fill_opacity=.025).move_to([0, .05, 0])
        directions = VGroup()
        for angle in np.linspace(0, TAU, 10, endpoint=False):
            d = np.array([np.cos(angle), np.sin(angle), 0])
            directions.add(Arrow(.16*d, 1.35*d, buff=0, color=ACCENT,
                                 stroke_width=2.2, tip_length=.13))
        self.show(VGroup(big_space, small_space, directions,
                         label("small space", 20, SPARSE).move_to([0, -1.24, 0]),
                         label("expanded space", 20, WEIGHT).move_to([0, 2.17, 0])))
        self.to(35)

        # 7: conceptual alternate path.
        self.copy("다른 경로가 열릴 수 있습니다", "MORE DIRECTIONS  ·  DIFFERENT PATHS",
                  "큰 공간에서는 다른 경로로\n좋은 해에 접근할 수도 있습니다.")
        start = Dot([-2.8, -1.5, 0], radius=.13, color=WEIGHT)
        target = label("★", 52, GOOD).move_to([2.75, 1.4, 0])
        obstacle = Ellipse(width=2.3, height=2.35, color=PRUNE,
                           fill_color=PRUNE, fill_opacity=.10).move_to([0, -.15, 0])
        direct = DashedLine(start.get_center(), target.get_center(), color=PRUNE,
                            stroke_width=3, dash_length=.18)
        around = self.polyline([[-2.8, -1.5, 0], [-2.55, 1.65, 0], [-.8, 2.13, 0],
                                [1.15, 2.1, 0], [2.75, 1.4, 0]], GOOD, 5)
        self.show(VGroup(obstacle, direct, around, start, target,
                         label("possible, not guaranteed", 19, MUTED).move_to([0, -2.5, 0])))
        self.to(41)

        # 8: the two effects of overparameterization.
        self.copy("큰 모델의 두 효과", "REPRESENTATION  +  OPTIMIZATION",
                  "표현할 수 있는 함수가 늘고\n학습 공간의 모양도 바뀝니다.")
        left = self.tall_panel("Representation", "More functions", WEIGHT)
        right = self.tall_panel("Optimization", "Different geometry", GOOD)
        self.show(VGroup(left.move_to([-1.9, 0, 0]), right.move_to([1.9, 0, 0])))
        self.to(46)

        # 9: a successful large-model run, as a conditional premise.
        self.copy("큰 공간에서 답을 찾았다", "θ₀  →  ···  →  θ*",
                  "큰 모델이 좋은 해에 도착했다고 해보죠.\n이제 필요한 크기를 다시 묻습니다.")
        path = self.polyline([[-2.8, -1.5, 0], [-1.85, -.9, 0], [-1, .3, 0],
                              [.2, -.15, 0], [1.4, 1.25, 0], [2.4, 1.15, 0]], GOOD, 5)
        self.show(VGroup(path, Dot([-2.8, -1.5, 0], color=WEIGHT),
                         label("θ₀", 24, WEIGHT).move_to([-2.8, -2.1, 0]),
                         label("★ θ*", 39, GOOD).move_to([2.4, 1.8, 0])))
        self.to(51)

        # 10: conditional approximate functional preservation.
        self.copy("찾은 뒤에는 줄일 수 있다", "fθ*(x)  ≈  fθ̃(x)  ON TESTED INPUTS",
                  "일부 자유도를 줄여도 관심 있는 입력에서\n출력이 비슷하게 유지될 수 있습니다.")
        dots = VGroup(*[Dot([x, 1.05, 0], radius=.075, color=WEIGHT)
                        for x in np.linspace(-2.5, 2.5, 19)])
        kept = VGroup(*[Dot([x, -.55, 0], radius=.085, color=GOOD)
                        for x in np.linspace(-1.65, 1.65, 7)])
        arrow = Arrow([0, .6, 0], [0, -.1, 0], color=ACCENT, buff=.08)
        output = card("similar outputs", GOOD, 4.5, 26).move_to([0, -2.0, 0])
        self.show(VGroup(dots, kept, arrow, output))
        self.to(57)

        # 11: the main statement.
        self.copy("찾는 크기와 담는 크기", "SIZE TO FIND  ≠  SIZE TO REPRESENT",
                  "찾는 데 유리한 크기와\n답을 담는 크기는 같을 필요가 없습니다.")
        left = self.tall_panel("FIND", "large workspace", WEIGHT)
        right = self.tall_panel("REPRESENT", "compact answer", GOOD)
        left.move_to([-1.9, 0, 0]); right.move_to([1.9, 0, 0])
        self.show(VGroup(left, right, label("≠", 40, ACCENT).move_to([0, 0, 0])))
        self.to(63)

        # 12: scaffolding analogy, explicitly labeled as analogy.
        self.copy("비계의 비유", "SCAFFOLD DURING BUILD  →  BUILDING REMAINS",
                  "비계는 건물을 지을 때 돕지만\n완성된 건물에는 남지 않습니다.")
        building = VGroup(Rectangle(width=2.5, height=3.0, color=GOOD,
                                    fill_color=GOOD, fill_opacity=.15).move_to([.1, -.25, 0]),
                          Polygon([-1.4, 1.25, 0], [.1, 2.3, 0], [1.6, 1.25, 0],
                                  color=GOOD, fill_color=GOOD, fill_opacity=.13))
        windows = VGroup(*[Rectangle(width=.45, height=.5, color=GOOD).move_to([x, y, 0])
                           for x in (-.55, .75) for y in (-.7, .25)])
        scaffold = VGroup(*[Line([x, -2.1, 0], [x, 2.3, 0], color=WEIGHT, stroke_width=3)
                            for x in (-2.0, 2.1)],
                          *[Line([-2.1, y, 0], [2.2, y, 0], color=WEIGHT, stroke_width=3)
                            for y in (-1.8, -.6, .6, 1.8)])
        self.show(VGroup(building, windows, scaffold,
                         label("analogy", 18, MUTED).move_to([0, -2.65, 0])))
        self.to(69)

        # 13: arbitrary deletion can damage the function.
        self.copy("아무거나 지우면 무너집니다", "COMPRESSIBLE  ≠  ARBITRARY DELETION",
                  "무엇을 보존하느냐에 따라\n압축 성능은 크게 달라집니다.")
        bars = VGroup(*[Rectangle(width=.28, height=h, color=WEIGHT,
                                  fill_color=WEIGHT, fill_opacity=.55).move_to([x, -1.35+h/2, 0])
                        for x, h in zip(np.linspace(-2.9, 2.9, 17),
                                        [1.4, 2.2, 2.9, 2.2, 1.1, 2.8, 2.3, 1.7, 3.2,
                                         1.5, 2.4, 2.8, 1.2, 2.6, 2.0, 2.7, 1.5])])
        crosses = VGroup(*[label("×", 31, PRUNE).move_to(bars[i]) for i in (1, 3, 5, 7, 8, 10, 12, 14)])
        fall = self.polyline([[.1, -2.15, 0], [1.7, -2.15, 0], [2.5, -2.8, 0]], PRUNE, 4)
        self.show(VGroup(bars, crosses, fall))
        self.to(75)

        # 14: whole sequence.
        self.copy("한 줄로 다시 보면", "LARGE SPACE  →  FIND  →  COMPRESS",
                  "큰 공간에서 답을 찾고\n동작을 보존하며 작게 옮기는 과정입니다.")
        steps = VGroup(card("Large parameter space", WEIGHT, 5.5, 26),
                       label("↓", 26, MUTED), card("Find θ*", SPARSE, 5.5, 27),
                       label("↓", 26, MUTED), card("Preserve behavior", GOOD, 5.5, 26),
                       label("↓", 26, MUTED), card("Compact representation", ACCENT, 5.5, 24))
        steps.arrange(DOWN, buff=.12).move_to([0, 0, 0])
        self.show(steps)
        self.to(81)

        # 15: the next episode's complexity question.
        self.copy("그럼 진짜 복잡도는?", "PARAMETER COUNT  ?=  MODEL COMPLEXITY",
                  "파라미터 수만으로는 충분할까요?\n모델의 실질적 복잡도는 무엇일까요?")
        large = card("100M parameters", WEIGHT, 3.5, 25).move_to([-1.9, 1.25, 0])
        small = card("20M parameters", GOOD, 3.5, 25).move_to([1.9, 1.25, 0])
        same = card("similar function", ACCENT, 5.3, 29).move_to([0, -.35, 0])
        query = label("Parameter Count  ?=  Complexity", 27, INK).move_to([0, -2.2, 0])
        self.show(VGroup(large, small, same, query))
        self.to(87)

    def performance_graph(self):
        axes = VGroup(Line([-3.0, -1.95, 0], [3.0, -1.95, 0], color=MUTED),
                      Line([-3.0, -1.95, 0], [-3.0, .15, 0], color=MUTED))
        curve = self.polyline([[-2.8, -.25, 0], [-1.7, -.27, 0],
                               [-.2, -.33, 0], [1.25, -.38, 0], [2.7, -.5, 0]], GOOD, 5)
        caption = label("performance substantially retained", 22, GOOD).move_to([0, -2.5, 0])
        return VGroup(axes, curve, caption)

    def route_panel(self, line1, line2, color, result):
        frame = RoundedRectangle(width=3.4, height=4.45, corner_radius=.2,
                                 stroke_color=color, stroke_width=2,
                                 fill_color=color, fill_opacity=.055)
        title = label(line1, 23, color, 3.0).move_to([0, 1.3, 0])
        arrow = label("↓", 32, MUTED).move_to([0, .25, 0])
        bottom = label(line2, 23, result, 3.0).move_to([0, -.8, 0])
        return VGroup(frame, title, arrow, bottom)

    def tall_panel(self, title, detail, color):
        frame = RoundedRectangle(width=3.4, height=4.35, corner_radius=.2,
                                 stroke_color=color, stroke_width=2,
                                 fill_color=color, fill_opacity=.065)
        title_mob = label(title, 24, color, 3.0).move_to([0, .95, 0])
        detail_mob = label(detail, 21, INK, 3.0).move_to([0, -.75, 0])
        return VGroup(frame, title_mob, detail_mob)

    def polyline(self, points, color, width):
        line = VMobject(color=color, stroke_width=width)
        line.set_points_as_corners(points)
        return line

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP*5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN*4.45)
        self.caption_box = RoundedRectangle(width=7.65, height=1.15, corner_radius=.14,
                                            stroke_color=ZERO, stroke_width=1.2,
                                            fill_color=ZERO, fill_opacity=.32).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note), FadeIn(self.caption_box),
                  FadeIn(self.caption), run_time=.2)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP*.12), run_time=.4)

    def to(self, target):
        remaining = target-self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target-self.time))
