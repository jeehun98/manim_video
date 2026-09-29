"""Neural Network Mathematics 05: Hessian spectrum as a map of local shape."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def card(value, color=WEIGHT, width=3.0, size=25):
    box = RoundedRectangle(width=width, height=.84, corner_radius=.15,
                           stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=.11)
    return VGroup(box, label(value, size, color, width-.2))


class NeuralMathHessianSpectrum(Scene):
    DURATION = 84

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  05", 18, MUTED).move_to(UP*7.3),
            label("좋은 해의 주변은 어떤 모양일까?", 29).move_to(UP*6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 00:00–00:06 — Zoom from mode connectivity onto a single good solution.
        self.copy("저손실 경로 위의 한 점", "MODE CONNECTIVITY  →  LOCAL SHAPE",
                  "연결된 좋은 해 중 하나를 확대합니다.\n그 주변은 어떤 모양일까요?")
        a, b = np.array([-3, 1.25, 0]), np.array([3, 1.25, 0])
        path = VMobject(color=GOOD, stroke_width=5)
        path.set_points_smoothly([a, [-1.6, -.5, 0], [0, -1.1, 0], [1.6, -.5, 0], b])
        theta = Dot([0, -1.1, 0], radius=.15, color=ACCENT)
        halo = Circle(radius=.4, color=ACCENT, stroke_opacity=.5).move_to(theta)
        self.show(VGroup(path, Dot(a, radius=.1, color=WEIGHT),
                         Dot(b, radius=.1, color=SPARSE), theta, halo,
                         label("θ*", 27, ACCENT).next_to(theta, DOWN, buff=.2)))
        self.play(halo.animate.scale(1.5).set_stroke(opacity=.2), run_time=.9)
        self.to(6)

        # 00:06–00:12 — One steep directional slice.
        self.copy("한 방향으로 자르면", "L(θ* + αv₁)",
                  "이 방향에서는 Loss가 빠르게 커집니다.\n단면은 좁고 가파릅니다.")
        sharp = self.slice_chart(2.2, PRUNE, "steep").move_to([0, -.25, 0])
        self.show(sharp)
        self.to(12)

        # 00:12–00:19 — Same point, another much flatter slice.
        self.copy("다른 방향의 단면", "SAME θ*  ·  DIFFERENT DIRECTION",
                  "같은 점에서 다른 방향은 거의 평평합니다.\n바라보는 방향에 따라 모양이 다릅니다.")
        left = self.slice_chart(2.2, PRUNE, "steep").scale(.78).move_to([-1.95, -.2, 0])
        right = self.slice_chart(.2, GOOD, "flat").scale(.78).move_to([1.95, -.2, 0])
        divide = Line([0, 2.4, 0], [0, -2.45, 0], color=MUTED, stroke_opacity=.3)
        self.show(VGroup(left, right, divide))
        self.to(19)

        # 00:19–00:26 — The number of directions explodes.
        self.copy("이런 방향이 수백만 개", "v₁, v₂, v₃, …, vD",
                  "실제 신경망에는 이런 방향이 아주 많습니다.\n보이지 않는 고차원 지형을 어떻게 잴까요?")
        rays = self.rays(28)
        center = Dot(ORIGIN, radius=.16, color=ACCENT)
        count = label("D ≈ 1,000,000 directions", 25, INK).move_to([0, 2.75, 0])
        self.show(VGroup(rays, center, count))
        self.to(26)

        # 00:26–00:36 — Name the Hessian through its eigen-directions.
        self.copy("방향별 휘어짐을 재는 도구", "HESSIAN  ·  LOCAL CURVATURE",
                  "Hessian의 특별한 방향 vᵢ마다\n국소 곡률 값 λᵢ가 대응합니다.")
        equation = card("H vᵢ = λᵢ vᵢ", ACCENT, 6.1, 40).move_to([0, 1.15, 0])
        direction = card("vᵢ  ·  direction", WEIGHT, 3.1, 22).move_to([-1.75, -1.3, 0])
        curvature = card("λᵢ  ·  curvature", GOOD, 3.1, 22).move_to([1.75, -1.3, 0])
        self.show(VGroup(equation, direction, curvature))
        self.to(36)

        # 00:36–00:44 — Collect values into a spectrum.
        self.copy("값을 모두 모아봅시다", "HESSIAN SPECTRUM",
                  "방향마다 나온 고유값을 모아\n분포로 그린 것이 Hessian Spectrum입니다.")
        pairs = VGroup(*[card(f"v{i}  →  λ{i}", color, 2.4, 22)
                         for i, color in ((1, PRUNE), (2, WEIGHT), (3, GOOD))])
        pairs.arrange(DOWN, buff=.35).move_to([-1.7, .2, 0])
        arrow = Arrow([-.25, .15, 0], [1.0, .15, 0], color=ACCENT,
                      stroke_width=4, tip_length=.18)
        spectrum = self.spectrum_bars().scale(.55).move_to([2.05, .15, 0])
        self.show(VGroup(pairs, arrow, spectrum))
        self.to(44)

        # 00:44–00:53 — A conceptual spectrum at a smooth local minimum.
        self.copy("분포의 모양을 읽습니다", "CONCEPTUAL EXAMPLE  ·  LOCAL MINIMUM",
                  "0 근처 값은 많고 큰 양의 값은 일부.\n큰 값은 가파르고, 작은 값은 국소적으로 평평합니다.")
        histogram = self.spectrum_bars().move_to([0, -.45, 0])
        flat_tag = card("near 0  →  flat", GOOD, 3.1, 22).move_to([-1.85, 2.75, 0])
        steep_tag = card("large +  →  steep", PRUNE, 3.25, 22).move_to([1.85, 2.75, 0])
        self.show(VGroup(histogram, flat_tag, steep_tag))
        self.to(53)

        # 00:53–01:00 — Conditional interpretation, not a universal count.
        self.copy("모든 방향이 똑같지는 않습니다", "IF MOST λᵢ ARE NEAR ZERO",
                  "이런 분포라면 강하게 제약된 방향은\n전체 차원 중 일부일 수 있습니다.")
        rays = self.rays(30)
        center = Dot(ORIGIN, radius=.16, color=ACCENT)
        large = VGroup(*[rays[i] for i in (1, 8, 15, 22)])
        self.show(VGroup(rays, center, label("D = 1,000,000", 28).move_to([0, 2.85, 0])))
        self.play(*[ray.animate.set_stroke(opacity=.06) for i, ray in enumerate(rays)
                    if i not in (1, 8, 15, 22)],
                  *[ray.animate.set_stroke(color=PRUNE, opacity=.95, width=4)
                    for ray in large], run_time=1.1)
        self.to(60)

        # 01:00–01:10 — Earlier episodes are related viewpoints, not a causal chain.
        self.copy("앞의 이야기와 함께 보면", "DIFFERENT VIEWS OF THE SAME SPACE",
                  "작은 학습 자유도, 함수의 중복 표현,\n저손실 연결성은 서로 다른 관점입니다.")
        cards = VGroup(card("01  d ≪ D", WEIGHT, 5.4, 26),
                       card("03  fθ = fθ′", SPARSE, 5.4, 26),
                       card("04  low-loss path", GOOD, 5.4, 26),
                       card("05  local curvature", ACCENT, 5.4, 26))
        cards.arrange(DOWN, buff=.32).move_to([0, .05, 0])
        self.show(cards)
        self.to(70)

        # 01:10–01:17 — Replace the symmetric bowl with an elongated valley.
        self.copy("단순한 그릇보다 긴 계곡", "DIRECTION-DEPENDENT SHAPE",
                  "좋은 해 주변은 한쪽으로 좁고\n다른 방향으로 길고 평평할 수 있습니다.")
        contours = VGroup(*[Ellipse(width=w, height=h, color=GOOD,
                                     stroke_opacity=.55-.11*i, stroke_width=3)
                            for i, (w, h) in enumerate(((1.7, .45), (3.5, .8),
                                                          (5.5, 1.15), (7.0, 1.5)))])
        contours.rotate(25*DEGREES).move_to([0, .15, 0])
        point = Dot([0, .15, 0], radius=.12, color=ACCENT)
        steep = Arrow([0, .15, 0], [-.55, 1.45, 0], color=PRUNE,
                      stroke_width=3, tip_length=.17)
        flat = Arrow([0, .15, 0], [2.65, 1.35, 0], color=GOOD,
                     stroke_width=3, tip_length=.17)
        self.show(VGroup(contours, point, steep, flat,
                         label("narrow", 21, PRUNE).move_to([-1.15, 1.75, 0]),
                         label("extended", 21, GOOD).move_to([2.6, 1.8, 0])))
        self.to(77)

        # 01:17–01:24 — Set up the next episode's caveat.
        self.copy("평평하면 더 좋은 모델일까?", "FLAT MINIMUM  =  BETTER GENERALIZATION  ?",
                  "평평한 해가 더 잘 일반화할까요?\n간단해 보이지만 함정이 있는 질문입니다.")
        sharp = self.slice_chart(2.4, PRUNE, "Sharp").scale(.75).move_to([-1.9, .25, 0])
        flat = self.slice_chart(.22, GOOD, "Flat").scale(.75).move_to([1.9, .25, 0])
        question = label("Better Generalization?", 29, ACCENT).move_to([0, -3.05, 0])
        self.show(VGroup(sharp, flat, question))
        self.to(84)

    def slice_chart(self, curvature, color, name):
        xaxis = Line([-2.0, -1.45, 0], [2.0, -1.45, 0], color=MUTED, stroke_opacity=.6)
        yaxis = Line([-2.0, -1.45, 0], [-2.0, 1.8, 0], color=MUTED, stroke_opacity=.6)
        curve = VMobject(color=color, stroke_width=5)
        pts = [[x, -.75 + curvature*(x/1.8)**2, 0] for x in np.linspace(-1.65, 1.65, 65)]
        curve.set_points_smoothly(pts)
        dot = Dot([0, -.75, 0], radius=.1, color=ACCENT)
        tags = VGroup(label(name, 24, color).move_to([0, -1.9, 0]),
                      label("θ*", 20, ACCENT).move_to([.38, -.95, 0]))
        return VGroup(xaxis, yaxis, curve, dot, tags)

    def rays(self, count):
        rays = VGroup()
        for i in range(count):
            angle = TAU*i/count
            length = 2.2 + .4*(i%3)
            rays.add(Line(ORIGIN, [length*np.cos(angle), .7*length*np.sin(angle), 0],
                          color=WEIGHT, stroke_width=1.7, stroke_opacity=.3))
        return rays

    def spectrum_bars(self):
        base = Line([-3.0, -1.55, 0], [3.05, -1.55, 0], color=MUTED)
        yaxis = Line([-3.0, -1.55, 0], [-3.0, 1.8, 0], color=MUTED)
        heights = (2.5, 2.9, 2.65, 2.25, 1.8, 1.35, 1.0, .7, .45,
                   .25, .12, .18, .14, .32, .22, .48)
        bars = VGroup()
        for i, height in enumerate(heights):
            x = -2.75 + .35*i
            color = GOOD if i < 10 else PRUNE
            bars.add(Rectangle(width=.25, height=height, stroke_width=0,
                               fill_color=color, fill_opacity=.8).move_to([x, -1.55+height/2, 0]))
        names = VGroup(label("0", 18, MUTED).move_to([-2.75, -1.86, 0]),
                       label("eigenvalue λ", 19, MUTED).move_to([1.4, -2.08, 0]),
                       label("count", 19, MUTED).move_to([-3.35, 1.7, 0]))
        return VGroup(base, yaxis, bars, names)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP*5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN*4.45)
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
