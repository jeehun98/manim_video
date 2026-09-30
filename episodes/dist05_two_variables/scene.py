"""Distribution mathematics 05: joint structure beyond two marginals."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, SPARSE, WEIGHT, txt


HEIGHTS = (155, 158, 160, 163, 165, 168, 170, 172, 175, 178, 180, 183, 185)
WEIGHTS = (50, 52, 53, 56, 55, 60, 63, 68, 70, 69, 78, 76, 81)
POSITIVE = tuple(zip(HEIGHTS, WEIGHTS))
NEGATIVE = tuple(zip(HEIGHTS, reversed(WEIGHTS)))


class TwoVariablesTogether(Scene):
    DURATION = 46

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  05", 19, MUTED).move_to(UP * 7.3),
            txt("두 변수를 동시에 보면 무엇이 달라질까?", 31).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: one variable, one axis, two one-dimensional summaries.
        self.copy("지금까지는 변수 하나", "평균은 위치, 분산은 퍼짐")
        axis = Arrow([-3.2, -1.2, 0], [3.25, -1.2, 0], buff=0,
                     color=MUTED, stroke_width=3)
        values = (-2.5, -1.9, -1.5, -1.15, -.8, -.35,
                  .0, .25, .6, 1.0, 1.45, 1.9, 2.45)
        dots = VGroup(*[
            Dot([x, -1.05 + .21 * (i % 3), 0], radius=.12,
                color=WEIGHT)
            for i, x in enumerate(values)
        ])
        x_label = txt("x", 31, WEIGHT).move_to([3.32, -.75, 0])
        stats = VGroup(
            txt("μₓ", 36, ACCENT), txt("σₓ²", 36, GOOD)
        ).arrange(RIGHT, buff=1.1).move_to([0, 2.05, 0])
        self.show(VGroup(axis, dots, x_label, stats), Create(axis),
                  LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=.05),
                  FadeIn(x_label), FadeIn(stats), run_time=1.05)
        self.to(4)

        # 4–8: one person gives a paired observation.
        self.copy("한 사람, 두 값", "키 172 cm · 몸무게 68 kg")
        self.clear_stage()
        person = self.person_icon().move_to([-2.2, .2, 0])
        height = self.value_card("키 = 172 cm", WEIGHT)
        weight = self.value_card("몸무게 = 68 kg", SPARSE)
        height.move_to([1.2, 1.05, 0])
        weight.move_to([1.2, -.15, 0])
        pair = txt("(172, 68)", 39, ACCENT).move_to([0, -2.2, 0])
        self.show(VGroup(person, height, weight, pair), FadeIn(person),
                  FadeIn(height), FadeIn(weight), FadeIn(pair),
                  run_time=1.05)
        self.to(8)

        # 8–12: a pair becomes a point in a plane.
        self.copy("수직선에서 평면으로", "한 사람 = 평면 위의 점 하나")
        self.clear_stage()
        axes = self.plane_axes()
        point = Dot(self.xy(172, 68), radius=.15, color=ACCENT)
        pair = txt("(172, 68)", 29, ACCENT).next_to(point, UP, buff=.25)
        guides = VGroup(
            DashedLine(point.get_center(), [point.get_x(), -2.1, 0],
                       color=MUTED, dash_length=.11),
            DashedLine(point.get_center(), [-3.1, point.get_y(), 0],
                       color=MUTED, dash_length=.11),
        )
        self.show(VGroup(axes, point, pair, guides), Create(axes),
                  Create(guides), FadeIn(point), FadeIn(pair),
                  run_time=1.1)
        self.to(12)

        # 12–16: repeated paired observations form a cloud.
        self.copy("관측이 많아지면", "각 사람은 점 하나, 모두 모이면 점구름")
        self.clear_stage()
        axes = self.plane_axes()
        cloud = self.cloud(POSITIVE, self.xy, WEIGHT)
        self.show(VGroup(axes, cloud), Create(axes),
                  LaggedStart(*[FadeIn(dot, scale=.6) for dot in cloud],
                              lag_ratio=.07), run_time=1.2)
        self.to(16)

        # 16–20: project the same observations to separate axes.
        self.copy("각각 따로 보면", "키의 분포 p(x), 몸무게의 분포 p(y)")
        x_rug, y_rug = self.marginal_rugs()
        projections = VGroup(x_rug, y_rug)
        marginal_labels = VGroup(
            txt("p(x)", 25, WEIGHT).move_to([1.45, -2.78, 0]),
            txt("p(y)", 25, SPARSE).move_to([-2.5, 3.35, 0]),
        )
        self.play(FadeIn(projections), FadeIn(marginal_labels),
                  run_time=.8)
        self.stage.add(projections, marginal_labels)
        self.to(20)

        # 20–25: only the y partners change; both marginal rugs stay fixed.
        self.copy("개별 분포는 같아도", "어떤 키와 어떤 몸무게가 짝인지가 달라집니다")
        title_a = txt("A  같은 방향", 28, GOOD).move_to([0, 2.8, 0])
        title_b = txt("B  반대 방향", 28, SPARSE).move_to(title_a)
        self.play(FadeIn(title_a), run_time=.4)
        self.play(*[
            dot.animate.move_to(self.xy(h, w))
            for dot, (h, w) in zip(cloud, NEGATIVE)
        ], Transform(title_a, title_b), run_time=1.25)
        same = txt("pA(x) = pB(x)    pA(y) = pB(y)", 26, ACCENT)
        same.move_to([0, -3.58, 0])
        self.play(FadeIn(same), run_time=.4)
        self.stage.add(title_a, same)
        self.to(25)

        # 25–29: put the positive and negative pairing side by side.
        self.copy("함께 보면 방향이 다릅니다", "같은 주변분포, 다른 점구름")
        self.clear_stage()
        left = self.small_panel(POSITIVE, -1.85, GOOD, "A")
        right = self.small_panel(NEGATIVE, 1.85, SPARSE, "B")
        self.show(VGroup(left, right), FadeIn(left), FadeIn(right),
                  run_time=.9)
        self.to(29)

        # 29–33: describe the two directions without causal language.
        self.copy("같이 증가하거나 반대로 움직이거나", "A: x↑, y↑     B: x↑, y↓")
        arrow_a = Arrow([-3.0, -2.45, 0], [-.8, -.6, 0],
                        buff=0, color=GOOD, stroke_width=4)
        arrow_b = Arrow([.75, -.6, 0], [3.0, -2.45, 0],
                        buff=0, color=SPARSE, stroke_width=4)
        self.play(GrowArrow(arrow_a), GrowArrow(arrow_b), run_time=.85)
        self.stage.add(arrow_a, arrow_b)
        self.to(33)

        # 33–37: four separate one-variable summaries omit the pairing.
        self.copy("1차원 요약에는 없던 정보", "두 값이 어떻게 함께 움직이는지는 따로 봐야 합니다")
        self.clear_stage()
        left_stats = self.value_card("μₓ     σₓ²", WEIGHT)
        right_stats = self.value_card("μᵧ     σᵧ²", SPARSE)
        left_stats.move_to([-2.0, 1.0, 0])
        right_stats.move_to([2.0, 1.0, 0])
        missing = txt("x        ?        y", 41, ACCENT).move_to([0, -.65, 0])
        note = txt("짝짓기 정보는 여기에서 빠집니다", 27, MUTED)
        note.move_to([0, -2.15, 0])
        self.show(VGroup(left_stats, right_stats, missing, note),
                  FadeIn(left_stats), FadeIn(right_stats),
                  FadeIn(missing), FadeIn(note), run_time=.9)
        self.to(37)

        # 37–41: more points suggest a joint shape and its long direction.
        self.copy("두 변수의 분포에는 방향이 있습니다", "점구름의 관계와 방향")
        self.clear_stage()
        axes = self.plane_axes()
        cloud = self.cloud(POSITIVE, self.xy, WEIGHT)
        contour1 = Ellipse(width=5.3, height=1.45, color=GOOD,
                           stroke_width=2, stroke_opacity=.65,
                           fill_color=GOOD, fill_opacity=.04)
        contour2 = Ellipse(width=4.1, height=.95, color=GOOD,
                           stroke_width=1.5, stroke_opacity=.4)
        contour1.rotate(.58).move_to([-.1, -.2, 0])
        contour2.rotate(.58).move_to([-.1, -.2, 0])
        direction = Arrow([-2.05, -1.48, 0], [1.95, 1.05, 0],
                          buff=0, color=ACCENT, stroke_width=3)
        self.show(VGroup(axes, cloud, contour1, contour2, direction),
                  FadeIn(axes), FadeIn(cloud), Create(contour1),
                  Create(contour2), GrowArrow(direction), run_time=1.05)
        self.to(41)

        # 41–46: preview a numerical measure of co-movement.
        self.copy("두 값이 같이 움직인다는 것은?", "다음 질문: 같은 방향으로 움직이는 정도")
        self.clear_stage()
        axes = self.plane_axes()
        cloud = self.cloud(POSITIVE, self.xy, WEIGHT)
        mean = Dot(self.xy(np.mean(HEIGHTS), np.mean(WEIGHTS)),
                   radius=.17, color=ACCENT)
        rays = VGroup(*[
            Line(mean.get_center(), dot.get_center(), color=MUTED,
                 stroke_width=1.1, stroke_opacity=.4)
            for dot in cloud[::2]
        ])
        prompt = txt("x↑  일 때  y↑  ?", 37, ACCENT).move_to([0, 2.75, 0])
        final = txt("두 값이 같이 움직인다는 것은 무슨 뜻일까?", 29, INK)
        final.move_to([0, -4.05, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.23,
                                     corner_radius=.13)
        cov = txt("Covariance", 24, MUTED).move_to([0, -4.9, 0])
        self.show(VGroup(axes, cloud, mean, rays, prompt, final, frame, cov),
                  FadeIn(axes), FadeIn(cloud), FadeIn(mean),
                  FadeIn(rays), FadeIn(prompt), run_time=.8)
        self.play(FadeIn(final), Create(frame), FadeIn(cov),
                  run_time=.65)
        self.to(46)

    def xy(self, height, weight):
        return np.array([-.1 + (height - 170) * .15,
                         -.2 + (weight - 65) * .105, 0])

    def plane_axes(self):
        x_axis = Arrow([-3.1, -2.1, 0], [3.15, -2.1, 0],
                       buff=0, color=MUTED, stroke_width=2.7)
        y_axis = Arrow([-3.1, -2.1, 0], [-3.1, 2.35, 0],
                       buff=0, color=MUTED, stroke_width=2.7)
        labels = VGroup(
            txt("키 x", 25, WEIGHT).move_to([2.65, -2.55, 0]),
            txt("몸무게 y", 25, SPARSE).move_to([-2.55, 2.7, 0]),
        )
        return VGroup(x_axis, y_axis, labels)

    def cloud(self, pairs, mapper, color):
        return VGroup(*[
            Dot(mapper(h, w), radius=.09, color=color)
            for h, w in pairs
        ])

    def marginal_rugs(self):
        x_rug = VGroup(*[
            Dot([self.xy(h, 65)[0], -2.26, 0], radius=.048,
                color=WEIGHT)
            for h in HEIGHTS
        ])
        y_rug = VGroup(*[
            Dot([-3.27, self.xy(170, w)[1], 0], radius=.048,
                color=SPARSE)
            for w in WEIGHTS
        ])
        return x_rug, y_rug

    def small_panel(self, pairs, xcenter, color, name):
        box = RoundedRectangle(width=3.35, height=3.45,
                               corner_radius=.16, stroke_color=color,
                               stroke_width=1.2, fill_color=color,
                               fill_opacity=.025)
        box.move_to([xcenter, -.25, 0])
        points = VGroup(*[
            Dot([xcenter + (h - 170) * .09,
                 -.25 + (w - 65) * .075, 0],
                radius=.073, color=color)
            for h, w in pairs
        ])
        title = txt(name, 32, color).move_to([xcenter, 2.1, 0])
        return VGroup(box, points, title)

    def person_icon(self):
        head = Circle(radius=.35, stroke_color=WEIGHT,
                      fill_color=WEIGHT, fill_opacity=.12)
        head.move_to([0, 1.3, 0])
        body = Line([0, .95, 0], [0, -.65, 0], color=WEIGHT,
                    stroke_width=4)
        arms = VGroup(
            Line([0, .45, 0], [-.8, -.1, 0], color=WEIGHT,
                 stroke_width=4),
            Line([0, .45, 0], [.8, -.1, 0], color=WEIGHT,
                 stroke_width=4),
        )
        legs = VGroup(
            Line([0, -.65, 0], [-.65, -1.45, 0], color=WEIGHT,
                 stroke_width=4),
            Line([0, -.65, 0], [.65, -1.45, 0], color=WEIGHT,
                 stroke_width=4),
        )
        return VGroup(head, body, arms, legs)

    def value_card(self, value, color):
        box = RoundedRectangle(width=3.25, height=.86,
                               corner_radius=.16, stroke_color=color,
                               stroke_width=1.6, fill_color=color,
                               fill_opacity=.08)
        return VGroup(box, txt(value, 28, color, 3.0))

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.14)
        self.head = txt(heading, 31, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 27, INK).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.25)

    def show(self, stage, *animations, run_time=.9):
        self.stage = stage
        self.play(*animations, run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.26)
        self.stage = VGroup()

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.28, remain))
            self.wait(max(0, target - self.time))
