"""Distribution mathematics 06: covariance from signed deviations."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt


POSITIVE = (
    (-2.35, -1.7), (-1.75, -1.35), (-1.15, -.72), (-.55, -.42),
    (.55, .42), (1.15, .72), (1.75, 1.35), (2.35, 1.7),
)
NEGATIVE = tuple((x, -y) for x, y in POSITIVE)


class WhatIsCovariance(Scene):
    DURATION = 49

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("DISTRIBUTION MATHEMATICS  /  06", 19, MUTED).move_to(UP * 7.3),
            txt("두 값이 같이 움직인다는 것은 무슨 뜻일까?", 31).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0)
        self.progress.move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: pick up the upward cloud from episode 05.
        self.copy("두 값이 같이 움직입니다", "x↑, y↑")
        axes = self.axes()
        cloud = self.dots(POSITIVE, WEIGHT)
        trend = Arrow([-2.35, -1.7, 0], [2.35, 1.7, 0],
                      buff=0, color=ACCENT, stroke_width=3)
        self.show(VGroup(axes, cloud, trend), FadeIn(axes),
                  FadeIn(cloud), GrowArrow(trend), run_time=1.05)
        self.to(4)

        # 4–8: the mean point is the origin of the signed-deviation map.
        self.copy("평균점을 기준으로", "(μₓ, μᵧ)를 지나도록 평면을 나눕니다")
        self.clear_stage()
        axes = self.axes()
        cloud = self.dots(POSITIVE, WEIGHT)
        mean = Dot(ORIGIN, radius=.16, color=ACCENT)
        guides = VGroup(
            DashedLine([-3.1, 0, 0], [3.1, 0, 0],
                       color=ACCENT, dash_length=.12),
            DashedLine([0, -2.6, 0], [0, 2.6, 0],
                       color=ACCENT, dash_length=.12),
        )
        label = txt("(μₓ, μᵧ)", 29, ACCENT).move_to([1.0, -.48, 0])
        self.show(VGroup(axes, cloud, mean, guides, label),
                  FadeIn(axes), FadeIn(cloud), Create(guides),
                  FadeIn(mean), FadeIn(label), run_time=1.05)
        self.to(8)

        # 8–12: both deviations of an upper-right point are positive.
        self.copy("오른쪽 위의 점", "x−μₓ > 0     y−μᵧ > 0")
        point = cloud[-2]
        horizontal = Arrow([0, 0, 0], [point.get_x(), 0, 0],
                           buff=0, color=GOOD, stroke_width=3)
        vertical = Arrow([point.get_x(), 0, 0], point.get_center(),
                         buff=0, color=GOOD, stroke_width=3)
        signs = txt("(+, +)", 39, GOOD).move_to([2.45, 2.65, 0])
        self.play(Indicate(point, color=GOOD, scale_factor=1.7),
                  GrowArrow(horizontal), GrowArrow(vertical),
                  FadeIn(signs), run_time=1.15)
        self.stage.add(horizontal, vertical, signs)
        self.to(12)

        # 12–16: both deviations of a lower-left point are negative.
        self.copy("왼쪽 아래도 같은 방향", "x−μₓ < 0     y−μᵧ < 0")
        self.clear_stage()
        axes = self.axes()
        cloud = self.dots(POSITIVE, WEIGHT)
        point = cloud[1]
        horizontal = Arrow([0, 0, 0], [point.get_x(), 0, 0],
                           buff=0, color=GOOD, stroke_width=3)
        vertical = Arrow([point.get_x(), 0, 0], point.get_center(),
                         buff=0, color=GOOD, stroke_width=3)
        signs = VGroup(
            txt("(+, +)", 34, GOOD).move_to([2.15, 2.3, 0]),
            txt("(−, −)", 34, GOOD).move_to([-2.15, -2.3, 0]),
        )
        self.show(VGroup(axes, cloud, horizontal, vertical, signs),
                  FadeIn(axes), FadeIn(cloud),
                  Indicate(point, color=GOOD, scale_factor=1.6),
                  GrowArrow(horizontal), GrowArrow(vertical),
                  FadeIn(signs), run_time=1.05)
        self.to(16)

        # 16–20: multiplication maps both concordant quadrants to plus.
        self.copy("두 편차를 곱하면", "(+)(+) = +     (−)(−) = +")
        self.clear_stage()
        first = txt("(x − μₓ)", 37, WEIGHT)
        second = txt("(y − μᵧ)", 37, SPARSE)
        times = txt("×", 36, MUTED)
        formula = VGroup(first, times, second).arrange(RIGHT, buff=.3)
        formula.move_to([0, 1.4, 0])
        examples = VGroup(
            self.sign_card("(+) × (+) = +", GOOD),
            self.sign_card("(−) × (−) = +", GOOD),
        ).arrange(DOWN, buff=.35).move_to([0, -.7, 0])
        self.show(VGroup(formula, examples), FadeIn(formula),
                  FadeIn(examples), run_time=.95)
        self.to(20)

        # 20–23: opposite-sign deviations produce a negative product.
        self.copy("반대로 움직이면", "(+)(−) = −     (−)(+) = −")
        self.clear_stage()
        axes = self.axes()
        points = self.dots(NEGATIVE, SPARSE)
        products = VGroup(
            txt("(−)(+) = −", 30, PRUNE).move_to([-2.1, 2.25, 0]),
            txt("(+)(−) = −", 30, PRUNE).move_to([2.1, -2.25, 0]),
        )
        self.show(VGroup(axes, points, products), FadeIn(axes),
                  FadeIn(points), FadeIn(products), run_time=.9)
        self.to(23)

        # 23–27: map the sign of a product over all four quadrants.
        self.copy("평면의 네 영역에 부호가 생깁니다", "같은 부호는 +, 다른 부호는 −")
        self.clear_stage()
        shades = VGroup(*[
            Rectangle(width=3.15, height=2.55, stroke_width=0,
                      fill_color=color, fill_opacity=.1).move_to([x, y, 0])
            for x, y, color in ((-1.58, 1.28, PRUNE),
                                (1.58, 1.28, GOOD),
                                (-1.58, -1.28, GOOD),
                                (1.58, -1.28, PRUNE))
        ])
        axes = self.axes()
        signs = VGroup(*[
            txt(sign, 56, color).move_to([x, y, 0])
            for x, y, sign, color in ((-1.6, 1.3, "−", PRUNE),
                                      (1.6, 1.3, "+", GOOD),
                                      (-1.6, -1.3, "+", GOOD),
                                      (1.6, -1.3, "−", PRUNE))
        ])
        self.show(VGroup(shades, axes, signs), FadeIn(shades),
                  FadeIn(axes), FadeIn(signs), run_time=.95)
        self.to(27)

        # 27–31: average the products, not merely their sign counts.
        self.copy("모든 점의 기여를 평균내면", "Cov(X,Y) = E[(X−μₓ)(Y−μᵧ)]")
        self.clear_stage()
        chips = VGroup(*[
            self.sign_card(sign, GOOD if sign == "+" else PRUNE,
                           width=.72, size=29)
            for sign in ("+", "+", "+", "−", "+", "−", "+")
        ]).arrange(RIGHT, buff=.14).move_to([0, 1.5, 0])
        formula = txt("Cov(X,Y) = E[(X−μₓ)(Y−μᵧ)]", 32, ACCENT)
        formula.move_to([0, -.25, 0])
        name = txt("공분산  /  Covariance", 31, GOOD)
        name.move_to([0, -1.65, 0])
        self.show(VGroup(chips, formula, name),
                  LaggedStart(*[FadeIn(chip) for chip in chips],
                              lag_ratio=.07), FadeIn(formula),
                  FadeIn(name), run_time=1.0)
        self.to(31)

        # 31–34: an upward cloud gives a positive covariance.
        self.copy("양의 공분산", "함께 늘고 함께 줄어드는 방향")
        self.clear_stage()
        axes = self.axes()
        cloud = self.dots(POSITIVE, GOOD)
        arrow = Arrow([-2.4, -1.75, 0], [2.4, 1.75, 0],
                      buff=0, color=GOOD, stroke_width=3)
        label = txt("Cov(X,Y) > 0", 34, GOOD).move_to([0, 2.8, 0])
        self.show(VGroup(axes, cloud, arrow, label), FadeIn(axes),
                  FadeIn(cloud), GrowArrow(arrow), FadeIn(label),
                  run_time=.9)
        self.to(34)

        # 34–37: a downward cloud gives a negative covariance.
        self.copy("음의 공분산", "하나는 늘고 다른 하나는 줄어드는 방향")
        self.clear_stage()
        axes = self.axes()
        cloud = self.dots(NEGATIVE, SPARSE)
        arrow = Arrow([-2.4, 1.75, 0], [2.4, -1.75, 0],
                      buff=0, color=SPARSE, stroke_width=3)
        label = txt("Cov(X,Y) < 0", 34, SPARSE).move_to([0, 2.8, 0])
        self.show(VGroup(axes, cloud, arrow, label), FadeIn(axes),
                  FadeIn(cloud), GrowArrow(arrow), FadeIn(label),
                  run_time=.9)
        self.to(37)

        # 37–40: circular symmetry cancels positive and negative products.
        self.copy("0에 가까운 공분산", "양·음의 선형 기여가 서로 상쇄됩니다")
        self.clear_stage()
        axes = self.axes()
        circle = self.dots([
            (1.75 * np.cos(t), 1.75 * np.sin(t))
            for t in np.linspace(0, TAU, 16, endpoint=False)
        ], WEIGHT)
        label = txt("Cov(X,Y) ≈ 0", 34, MUTED).move_to([0, 2.85, 0])
        self.show(VGroup(axes, circle, label), FadeIn(axes),
                  FadeIn(circle), FadeIn(label), run_time=.9)
        self.to(40)

        # 40–44: summarize signs with three small panels.
        self.copy("공분산의 부호가 보여주는 것", "+   같은 방향     0   상쇄     −   반대 방향")
        self.clear_stage()
        panels = VGroup(
            self.mini_panel(35 * DEGREES, -2.45, GOOD, "+"),
            self.mini_panel(0, 0, MUTED, "≈ 0"),
            self.mini_panel(-35 * DEGREES, 2.45, SPARSE, "−"),
        )
        self.show(panels, FadeIn(panels), run_time=.95)
        self.to(44)

        # 44–49: rotate one fixed elongated point set. Its shape remains.
        self.copy("같은 점구름을 회전하면?", "Cov: +  →  0  →  −")
        self.clear_stage()
        axes = self.axes()
        cloud = self.ellipse_cloud(35 * DEGREES, scale=1)
        outline = self.ellipse_outline(35 * DEGREES)
        sign = txt("Cov > 0", 36, GOOD).move_to([0, 2.85, 0])
        self.show(VGroup(axes, cloud, outline, sign), FadeIn(axes),
                  FadeIn(cloud), Create(outline), FadeIn(sign),
                  run_time=.7)
        mid_sign = txt("Cov = 0", 36, MUTED).move_to(sign)
        self.play(Transform(cloud, self.ellipse_cloud(0, scale=1)),
                  Transform(outline, self.ellipse_outline(0)),
                  Transform(sign, mid_sign), run_time=.7)
        neg_sign = txt("Cov < 0", 36, SPARSE).move_to(sign)
        self.play(Transform(cloud, self.ellipse_cloud(-35 * DEGREES, scale=1)),
                  Transform(outline, self.ellipse_outline(-35 * DEGREES)),
                  Transform(sign, neg_sign), run_time=.7)
        final = txt("공분산과 기울기는 어떻게 연결될까?", 31, INK)
        final.move_to([0, -4.2, 0])
        frame = SurroundingRectangle(final, color=ACCENT, buff=.24,
                                     corner_radius=.13)
        self.play(FadeIn(final), Create(frame), run_time=.55)
        self.stage = VGroup(axes, cloud, outline, sign, final, frame)
        self.to(49)

    def axes(self):
        x_axis = Arrow([-3.35, 0, 0], [3.35, 0, 0], buff=0,
                       color=MUTED, stroke_width=2.6)
        y_axis = Arrow([0, -2.65, 0], [0, 2.65, 0], buff=0,
                       color=MUTED, stroke_width=2.6)
        labels = VGroup(
            txt("x", 25, WEIGHT).move_to([3.52, -.25, 0]),
            txt("y", 25, SPARSE).move_to([-.27, 2.8, 0]),
        )
        return VGroup(x_axis, y_axis, labels)

    def dots(self, pairs, color):
        return VGroup(*[
            Dot([x, y, 0], radius=.1, color=color)
            for x, y in pairs
        ])

    def ellipse_coords(self, angle, scale=1, n=24):
        c, s = np.cos(angle), np.sin(angle)
        return [
            (scale * (2.3 * np.cos(t) * c - .6 * np.sin(t) * s),
             scale * (2.3 * np.cos(t) * s + .6 * np.sin(t) * c))
            for t in np.linspace(0, TAU, n, endpoint=False)
        ]

    def ellipse_cloud(self, angle, scale=1):
        return self.dots(self.ellipse_coords(angle, scale), WEIGHT)

    def ellipse_outline(self, angle):
        return Ellipse(width=4.85, height=1.45, color=ACCENT,
                       stroke_width=2, stroke_opacity=.7,
                       fill_color=ACCENT, fill_opacity=.035).rotate(angle)

    def mini_panel(self, angle, xcenter, color, sign):
        box = RoundedRectangle(width=2.25, height=3.1, corner_radius=.15,
                               stroke_color=color, stroke_width=1.2,
                               fill_color=color, fill_opacity=.025)
        box.move_to([xcenter, -.15, 0])
        dots = self.ellipse_cloud(angle, scale=.38)
        dots.shift(RIGHT * xcenter)
        label = txt("Cov " + sign, 26, color).move_to([xcenter, -2.2, 0])
        return VGroup(box, dots, label)

    def sign_card(self, value, color, width=3.15, size=30):
        box = RoundedRectangle(width=width, height=.8,
                               corner_radius=.15, stroke_color=color,
                               stroke_width=1.5, fill_color=color,
                               fill_opacity=.09)
        return VGroup(box, txt(value, size, color, width - .15))

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.14)
        self.head = txt(heading, 31, INK).move_to([0, 4.95, 0])
        self.caption = txt(caption, 27, INK).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.24)

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
