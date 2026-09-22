"""SVD 07: a small output error grows during inverse reconstruction."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.svd_series.visuals import BLUE, GOLD, GREEN, INK, MUTED, PINK, txt


class SVD07InverseError(Scene):
    DURATION = 60

    def construct(self):
        self.gap = ValueTracker(.01)
        self.shape_mix = ValueTracker(0)
        self.head = VGroup()
        self.note = VGroup()
        self.sub = VGroup()
        self.add(
            txt("SVD  /  07", 20, MUTED).move_to(UP * 7.25),
            txt("역행렬이 오차를 키우는 이유", 36).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=BLUE,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        self.text("납작한 타원에서 이어집니다",
                  "앞에서 A는 세로 방향 정보를\n0.1배로 압축했습니다.",
                  "A = diag(3, 0.1)     ·     κ(A) = 30")
        self.center = np.array([-1.0, 1.35, 0.0])
        self.geometry = always_redraw(self.make_geometry)
        self.panel_label = txt("출력 공간  y = Ax", 26, GOLD).move_to([-1.0, 3.55, 0])
        self.play(Create(self.geometry), FadeIn(self.panel_label), run_time=1.7)
        self.to(7)

        self.text("복원하려는 출력에 작은 오차가 생기면",
                  "정확한 출력 y와 관측값 ỹ는\n세로로 단 0.01만큼 다릅니다.",
                  "y = (3, 0)     ·     ỹ = (3, 0.01)")
        self.top_pair = always_redraw(self.make_top_pair)
        self.play(FadeIn(self.top_pair), run_time=.9)
        self.play(Indicate(self.top_pair, color=PINK, scale_factor=1.7), run_time=1.3)
        self.to(15)

        self.text("그림을 확대해서 보면",
                  "거의 붙어 있는 두 점이지만,\n작은 차이는 실제로 남아 있습니다.",
                  "점 주변 확대 · 아래 비교창은 같은 척도")
        self.lens = self.make_lens()
        self.lens_pair = always_redraw(self.make_lens_pair)
        self.gap_number = always_redraw(self.make_gap_number)
        self.play(FadeIn(self.lens), FadeIn(self.lens_pair), FadeIn(self.gap_number), run_time=1.2)
        self.to(22)

        self.text("이제 화살표를 반대로 돌립니다",
                  "출력에서 원래 입력을 찾으려면\n역행렬 A⁻¹을 적용합니다.",
                  "y = Ax     →     x = A⁻¹y")
        self.reverse_badge = VGroup(
            RoundedRectangle(width=2.2, height=.72, corner_radius=.12,
                             stroke_color=BLUE, fill_color="#17243A", fill_opacity=.95),
            txt("A⁻¹  ↶", 28, BLUE),
        ).move_to([2.55, 3.45, 0])
        self.play(FadeIn(self.reverse_badge), run_time=.8)
        self.to(29)

        self.text("압축의 반대는 확대",
                  "세로를 0.1배로 줄였으니\n복원할 때는 그 방향을 10배 키웁니다.",
                  "A⁻¹ = diag(1/3, 10)")
        self.inverse_card = VGroup(
            RoundedRectangle(width=3.0, height=1.05, corner_radius=.13,
                             stroke_color=BLUE, fill_color="#101C2E", fill_opacity=.96),
            txt("세로 방향  × 10", 28, BLUE),
        ).move_to([2.35, -.05, 0])
        self.play(FadeIn(self.inverse_card), run_time=.8)
        self.to(36)

        self.text("오차도 함께 10배 커집니다",
                  "거의 붙어 있던 두 점이 역변환을 통과하면\n복원된 입력에서는 크게 벌어집니다.",
                  "δy = 0.01     →     δx = 0.10")
        self.play(
            self.shape_mix.animate.set_value(1),
            self.gap.animate.set_value(.10),
            Transform(self.panel_label, txt("복원된 입력  x = A⁻¹y", 26, BLUE).move_to([-1.0, 3.55, 0])),
            run_time=5.1, rate_func=smooth,
        )
        self.play(Indicate(self.lens_pair, color=PINK, scale_factor=1.05), run_time=1.0)
        self.to(46)

        self.text("원래 신호만 커지는 것이 아닙니다",
                  "복원 과정은 유용한 세로 성분과\n관측에 섞인 오차를 구별하지 못합니다.",
                  "A⁻¹(y + δy) = x + A⁻¹δy")
        self.signal_noise = VGroup(
            txt("신호 성분  × 10", 27, GREEN),
            txt("오차 성분  × 10", 27, PINK),
        ).arrange(DOWN, buff=.32).move_to([2.25, .2, 0])
        self.play(FadeOut(self.reverse_badge), FadeOut(self.inverse_card),
                  FadeIn(self.signal_noise), run_time=.9)
        self.to(53)

        self.text("약하게 남은 정보일수록 복원이 민감해집니다",
                  "Condition number는 이런 방향별 격차를 경고합니다.\n다음엔 연립방정식의 교점으로 보겠습니다.",
                  "κ = 30     ·     이 예제의 세로 오차 증폭은 10배")
        self.play(Circumscribe(self.lens, color=GOLD), run_time=1.1)
        self.to(60)

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP * .08), run_time=.2)
        self.head = txt(head, 30).move_to(UP * 5.18)
        self.note = txt(note, 25, GOLD).move_to(DOWN * 4.72)
        self.sub = txt(sub, 27).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.4)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.35, 0]), run_time=min(.3, remaining))
            self.wait(max(0, target - self.time))

    def make_geometry(self):
        mix = self.shape_mix.get_value()
        width = (6 - 4 * mix) * .85
        height = (.2 + 1.8 * mix) * .85
        outline = Ellipse(width=width, height=height,
                          color=interpolate_color(ManimColor(GOLD), ManimColor(BLUE), mix),
                          stroke_width=4).move_to(self.center)
        axes = VGroup(
            Line(self.center + LEFT * 3, self.center + RIGHT * 3,
                 color=MUTED, stroke_opacity=.25),
            Line(self.center + DOWN * 1.25, self.center + UP * 1.25,
                 color=MUTED, stroke_opacity=.25),
        )
        return VGroup(axes, outline)

    def make_top_pair(self):
        mix = self.shape_mix.get_value()
        x = self.center[0] + (2.55 - 1.7 * mix)
        offset = .85 * self.gap.get_value()
        return VGroup(
            Dot([x, self.center[1], 0], radius=.095, color=GREEN),
            Dot([x, self.center[1] + offset, 0], radius=.095, color=PINK),
        )

    def make_lens(self):
        box = RoundedRectangle(width=7.2, height=2.65, corner_radius=.17,
                               stroke_color=MUTED, stroke_opacity=.55,
                               fill_color="#111D30", fill_opacity=.96).move_to([0, -1.8, 0])
        title = txt("두 점 주변 확대 · 변위는 동일 척도", 22, MUTED).move_to([0, -.85, 0])
        axis = Line([-2.6, -2.45, 0], [-2.6, -1.18, 0], color=MUTED, stroke_opacity=.45)
        return VGroup(box, title, axis)

    def make_lens_pair(self):
        base = np.array([-2.6, -2.45, 0])
        offset = 10 * self.gap.get_value()
        dot0 = Dot(base, radius=.085, color=GREEN)
        dot1 = Dot(base + UP * offset, radius=.085, color=PINK)
        connector = Line(dot0.get_center(), dot1.get_center(), color=PINK,
                         stroke_width=4, stroke_opacity=.7)
        labels = VGroup(
            txt("기준값", 21, GREEN).move_to([-1.4, -2.46, 0]),
            txt("관측값 / 복원값", 21, PINK).move_to([-.7, -1.3, 0]),
        )
        return VGroup(connector, dot0, dot1, labels)

    def make_gap_number(self):
        value = self.gap.get_value()
        return VGroup(
            txt("두 점의 차이", 23, MUTED),
            txt(f"{value:.3f}", 34, PINK),
        ).arrange(DOWN, buff=.12).move_to([2.25, -1.85, 0])
