"""SVD 06: condition number as directional imbalance."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.svd_series.visuals import BLUE, GOLD, GREEN, INK, MUTED, PINK, txt


DURATION = 60
EPSILON = 0.30
SCALE = 0.92
CENTER = np.array([-0.75, 1.55, 0.0])


class SVD06ConditionNumber(Scene):
    def construct(self):
        self.sigma_min = ValueTracker(1.0)
        self.theta = ValueTracker(0.0)

        self.add(
            txt("SVD  /  06", 20, MUTED).move_to(UP * 7.25),
            txt("Condition Number: 방향의 불균형", 35).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=BLUE, fill_opacity=1, stroke_width=0
        ).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        self.heading = VGroup()
        self.caption = VGroup()
        self.note = VGroup()

        self.set_text(
            "같은 크기의 오차, 다른 결과",
            "크기가 같은 작은 오차라도\n방향에 따라 결과는 달라질 수 있습니다.",
            "x₁ = (1, ε)     ·     x₂ = (1, −ε)",
        )
        self.axes = self.make_axes()
        self.circle = Circle(radius=SCALE, color=BLUE, stroke_width=4).move_to(CENTER)
        self.input_points = VGroup(
            Dot(CENTER + [SCALE, SCALE * EPSILON, 0], radius=.105, color=PINK),
            Dot(CENTER + [SCALE, -SCALE * EPSILON, 0], radius=.105, color=GREEN),
        )
        self.input_gap = DoubleArrow(
            self.input_points[1].get_center(), self.input_points[0].get_center(),
            buff=.12, color=GOLD, stroke_width=3, tip_length=.12,
        )
        self.input_gap_label = txt("같은 작은 차이  2ε", 24, GOLD).next_to(
            self.input_gap, RIGHT, buff=.18
        )
        self.play(Create(self.axes), Create(self.circle), FadeIn(self.input_points), run_time=1.8)
        self.play(GrowArrow(self.input_gap), FadeIn(self.input_gap_label), run_time=1.2)
        self.wait_to(7)

        self.set_text(
            "행렬은 방향마다 다르게 늘립니다",
            "A를 적용하면 단위원은 타원이 되고,\n두 입력점도 함께 이동합니다.",
            "A = diag(3, 1)",
        )
        ellipse_static = Ellipse(
            width=6 * SCALE, height=2 * SCALE, color=GOLD, stroke_width=4
        ).move_to(CENTER)
        output_targets = VGroup(
            Dot(CENTER + [3 * SCALE, SCALE * EPSILON, 0], radius=.105, color=PINK),
            Dot(CENTER + [3 * SCALE, -SCALE * EPSILON, 0], radius=.105, color=GREEN),
        )
        a_badge = VGroup(
            RoundedRectangle(width=1.28, height=.72, corner_radius=.12,
                             stroke_color=MUTED, fill_color="#17243A", fill_opacity=.95),
            txt("× A", 28, GOLD),
        ).move_to([-.75, 3.9, 0])
        self.play(
            FadeOut(self.input_gap), FadeOut(self.input_gap_label), FadeIn(a_badge),
            Transform(self.circle, ellipse_static),
            Transform(self.input_points, output_targets),
            run_time=2.4,
        )
        self.dynamic_ellipse = always_redraw(
            lambda: Ellipse(
                width=6 * SCALE,
                height=2 * SCALE * self.sigma_min.get_value(),
                color=GOLD,
                stroke_width=4,
            ).move_to(CENTER)
        )
        self.output_points = always_redraw(self.make_output_points)
        self.remove(self.circle, self.input_points)
        self.add(self.dynamic_ellipse, self.output_points)
        self.dashboard = self.make_dashboard()
        self.play(FadeIn(self.dashboard, shift=LEFT * .15), run_time=1.1)
        self.wait_to(15)

        self.set_text(
            "입력 오차의 크기는 그대로",
            "작은 입력 오차를 한 바퀴 돌리면,\n출력 오차의 길이는 계속 달라집니다.",
            "δx(θ) = ε(cos θ, sin θ)",
        )
        self.dial = self.make_input_dial()
        self.output_arrow = always_redraw(self.make_output_arrow)
        self.play(FadeOut(a_badge), FadeIn(self.dial), GrowArrow(self.output_arrow), run_time=1.2)
        self.play(self.theta.animate.set_value(PI / 2), run_time=6.5, rate_func=linear)
        self.wait_to(25)

        self.set_text(
            "장축 방향은 크게 보존됩니다",
            "장축 방향의 작은 변화는\n출력에서 3배 길이로 나타납니다.",
            "‖Aδx‖ = σmax ‖δx‖ = 3‖δx‖",
        )
        self.play(self.theta.animate.set_value(0), run_time=1.6)
        major = Line(CENTER, CENTER + RIGHT * 3 * SCALE, color=BLUE, stroke_width=8)
        major_label = txt("σmax = 3", 26, BLUE).next_to(major, UP, buff=.18)
        self.play(Create(major), FadeIn(major_label), run_time=1.0)
        self.play(Indicate(VGroup(major, major_label), color=BLUE, scale_factor=1.04), run_time=1.2)
        self.play(FadeOut(major), FadeOut(major_label), run_time=.5)
        self.wait_to(32)

        self.set_text(
            "단축 방향은 약하게 보존됩니다",
            "방향을 90도 돌리면 같은 입력 오차가\n훨씬 짧은 출력으로 바뀝니다.",
            "‖Aδx‖ = σmin ‖δx‖",
        )
        self.play(self.theta.animate.set_value(PI / 2), run_time=1.6)
        minor = Line(CENTER, CENTER + UP * SCALE, color=GREEN, stroke_width=8)
        minor_label = txt("σmin = 1", 26, GREEN).next_to(minor, LEFT, buff=.18)
        self.play(Create(minor), FadeIn(minor_label), run_time=.9)
        self.play(Indicate(VGroup(minor, minor_label), color=GREEN, scale_factor=1.04), run_time=1.0)
        self.play(FadeOut(minor), FadeOut(minor_label), run_time=.4)
        self.wait_to(38)

        self.set_text(
            "두 극단의 격차를 비교하면",
            "가장 크게 보존되는 방향과 가장 약하게\n보존되는 방향의 비율을 봅니다.",
            "κ(A) = σmax / σmin",
        )
        formula = VGroup(
            RoundedRectangle(width=5.5, height=1.02, corner_radius=.14,
                             stroke_color=GOLD, fill_color="#111D30", fill_opacity=.96),
            txt("κ(A) = σmax / σmin = 3", 35, GOLD),
        ).move_to([-.75, -2.65, 0])
        self.play(FadeOut(self.dial), FadeOut(self.output_arrow), FadeIn(formula), run_time=1.0)
        self.play(Circumscribe(formula, color=GOLD), run_time=1.2)
        self.wait_to(44)

        self.set_text(
            "σmin이 작아질수록 타원은 납작해집니다",
            "단축 방향의 정보가 압축되는 동안\nκ는 3에서 30까지 커집니다.",
            "σmin : 1 → 0.1     ·     κ : 3 → 30",
        )
        gap_line = always_redraw(self.make_gap_line)
        gap_value = always_redraw(self.make_gap_value)
        self.play(FadeOut(formula), FadeIn(gap_line), FadeIn(gap_value), run_time=.8)
        self.play(self.sigma_min.animate.set_value(.1), run_time=7.2, rate_func=smooth)
        self.wait_to(53)

        self.set_text(
            "서로 다른 입력이 거의 같은 출력으로",
            "타원이 납작할수록 어떤 방향의 정보는 거의 지워집니다.\n복원할 때는 작은 오차가 크게 드러날 수 있습니다.",
            "Ax₁ ≈ Ax₂     →     역문제는 민감해집니다",
        )
        halo = always_redraw(
            lambda: SurroundingRectangle(
                self.output_points, color=PINK, buff=.16, corner_radius=.10, stroke_width=3
            )
        )
        fair = VGroup(
            RoundedRectangle(width=7.1, height=1.0, corner_radius=.14,
                             stroke_color=BLUE, fill_color="#101C2E", fill_opacity=.96),
            txt("Condition number = 방향을 얼마나 공평하게 다루는가", 27, BLUE),
        ).move_to([0, -3.25, 0])
        self.play(FadeIn(halo), FadeIn(fair, shift=UP * .12), run_time=1.0)
        self.play(Indicate(halo, color=PINK, scale_factor=1.35), run_time=1.1)
        self.wait_to(60)

    def set_text(self, heading, caption, note):
        new_heading = txt(heading, 30).move_to(UP * 5.18)
        new_note = txt(note, 25, GOLD).move_to(DOWN * 4.72)
        new_caption = txt(caption, 27).move_to(DOWN * 6.08)
        old = VGroup(self.heading, self.note, self.caption)
        self.play(FadeOut(old, shift=UP * .08), run_time=.22) if len(old) else None
        self.heading, self.note, self.caption = new_heading, new_note, new_caption
        self.play(FadeIn(new_heading), FadeIn(new_note), FadeIn(new_caption), run_time=.38)

    def wait_to(self, target):
        width = max(.01, 7.6 * target / DURATION)
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}s: {self.time:.2f}")
        if remaining > 0:
            self.play(
                self.progress.animate.stretch_to_fit_width(width).move_to(
                    [-3.8 + width / 2, -7.35, 0]
                ),
                run_time=min(.3, remaining),
            )
            self.wait(max(0, target - self.time))

    def make_axes(self):
        return VGroup(
            Line([-4.0, CENTER[1], 0], [2.2, CENTER[1], 0], color=MUTED, stroke_opacity=.28),
            Line([CENTER[0], .25, 0], [CENTER[0], 2.85, 0], color=MUTED, stroke_opacity=.28),
            Dot(CENTER, radius=.055, color=INK),
        )

    def make_output_points(self):
        s = self.sigma_min.get_value()
        return VGroup(
            Dot(CENTER + [3 * SCALE, SCALE * s * EPSILON, 0], radius=.105, color=PINK),
            Dot(CENTER + [3 * SCALE, -SCALE * s * EPSILON, 0], radius=.105, color=GREEN),
        )

    def make_dashboard(self):
        panel = RoundedRectangle(
            width=2.05, height=2.7, corner_radius=.14,
            stroke_color=MUTED, stroke_opacity=.45,
            fill_color="#111D30", fill_opacity=.95,
        ).move_to([2.85, -1.05, 0])
        labels = VGroup(
            txt("σmax", 23, BLUE).move_to([2.35, -.32, 0]),
            txt("σmin", 23, GREEN).move_to([2.35, -1.02, 0]),
            txt("κ", 25, GOLD).move_to([2.35, -1.82, 0]),
        )
        max_value = txt("3.00", 27, BLUE).move_to([3.27, -.32, 0])
        min_value = always_redraw(
            lambda: txt(f"{self.sigma_min.get_value():.2f}", 27, GREEN).move_to([3.27, -1.02, 0])
        )
        kappa_value = always_redraw(
            lambda: txt(f"{3 / self.sigma_min.get_value():.1f}", 29, GOLD).move_to([3.27, -1.82, 0])
        )
        return VGroup(panel, labels, max_value, min_value, kappa_value)

    def make_input_dial(self):
        center = np.array([-2.65, -1.25, 0])
        radius = .72
        circle = Circle(radius=radius, color=BLUE, stroke_opacity=.45).move_to(center)
        arrow = always_redraw(
            lambda: Arrow(
                center,
                center + radius * np.array([
                    np.cos(self.theta.get_value()), np.sin(self.theta.get_value()), 0
                ]),
                buff=0, color=BLUE, stroke_width=4, tip_length=.15,
            )
        )
        label = txt("입력  ‖δx‖ = ε", 22, BLUE).next_to(circle, DOWN, buff=.22)
        return VGroup(circle, arrow, label)

    def make_output_arrow(self):
        t = self.theta.get_value()
        s = self.sigma_min.get_value()
        vector = SCALE * np.array([3 * np.cos(t), s * np.sin(t), 0])
        return Arrow(CENTER, CENTER + vector, buff=0, color=PINK,
                     stroke_width=6, tip_length=.17)

    def make_gap_line(self):
        points = self.make_output_points()
        return DoubleArrow(points[1].get_center(), points[0].get_center(), buff=.11,
                           color=PINK, stroke_width=3, tip_length=.11)

    def make_gap_value(self):
        value = 2 * EPSILON * self.sigma_min.get_value()
        number = txt(f"{value:.2f}", 25, PINK)
        label = VGroup(txt("출력 간격", 22, PINK), number).arrange(RIGHT, buff=.18)
        return label.move_to([1.45, 3.15, 0])
