"""Distribution mathematics 14: soft membership in a Gaussian mixture."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, txt


WEIGHTS = (.4, .6)
MEANS = (-.5, .5)
SIGMA_X = .4
X_RIGHT = SIGMA_X**2 * np.log(14 / 9)
X_LEFT = -X_RIGHT
SCALE = 2.5


def normal_1d(value, mean, std):
    return np.exp(-.5 * ((value - mean) / std)**2) / (np.sqrt(2 * np.pi) * std)


# Set the vertical Gaussian scale so the example is internally consistent:
# at X_RIGHT, pi_1 p_1(x)=.12 and pi_2 p_2(x)=.28.
VERTICAL_STD = WEIGHTS[0] * normal_1d(X_RIGHT, MEANS[0], SIGMA_X) / (.12 * np.sqrt(2*np.pi))
COV = np.diag([SIGMA_X**2, VERTICAL_STD**2])


def weighted_density(x, k):
    return WEIGHTS[k] * normal_1d(x, MEANS[k], SIGMA_X) * normal_1d(0, 0, VERTICAL_STD)


def responsibility(x, k=0):
    values = [weighted_density(x, j) for j in range(2)]
    return values[k] / sum(values)


class ResponsibilityDiscovery(Scene):
    DURATION = 45

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("PART IV  /  DISTRIBUTION MATHEMATICS 14", 18, MUTED).move_to(UP * 7.3),
            txt("꼭 하나의 집단이어야 할까? | Responsibility", 27, INK, 7.7).move_to(UP * 6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–3: one point in the overlap of two Gaussian components.
        self.copy("이 점은 어느 쪽일까?", "두 Gaussian이 겹치는 곳의 x")
        shapes = self.gaussian_pair()
        centers = self.centers()
        dot = Dot(self.pos(X_LEFT), radius=.14, color=ACCENT)
        self.show(VGroup(shapes, centers, dot), FadeIn(shapes),
                  FadeIn(centers), FadeIn(dot), run_time=.85)
        self.to(3)

        # 3–6: nearest-center assignment labels the point as component 1.
        self.copy("가까운 중심을 고르면", "d₁ < d₂    →    x → 1")
        lines = self.distance_lines(X_LEFT)
        hard = self.hard_badge(1)
        self.play(Create(lines), FadeIn(hard), run_time=.65)
        self.stage = VGroup(shapes, centers, dot, lines, hard)
        self.to(6)

        # 6–9: a very small move across the midpoint flips that hard label.
        self.copy("아주 조금 옮기자", "d₁ > d₂    →    1 → 2")
        self.play(dot.animate.move_to(self.pos(X_RIGHT)),
                  Transform(lines, self.distance_lines(X_RIGHT)),
                  Transform(hard, self.hard_badge(2)), run_time=.75)
        self.to(9)

        # 9–12: show how little the observation moved relative to the label.
        self.copy("점은 거의 같은 곳인데", "소속만 1에서 2로 뒤집혔습니다")
        old = Dot(self.pos(X_LEFT), radius=.075, color=PRUNE)
        boundary = DashedLine([0, -2.8, 0], [0, 2.8, 0],
                              color=PRUNE, stroke_width=2)
        shift_arrow = Arrow(self.pos(X_LEFT)+UP*.45,
                            self.pos(X_RIGHT)+UP*.45,
                            buff=0, color=ACCENT, stroke_width=3)
        self.play(FadeIn(old), Create(boundary), GrowArrow(shift_arrow),
                  run_time=.6)
        self.stage = VGroup(shapes, centers, dot, lines, hard, old, boundary, shift_arrow)
        self.to(12)

        # 12–15: overlap itself suggests a softer answer.
        self.copy("선명한 경계가 정말 있을까?", "두 Gaussian 모두 이 점에 밀도를 줍니다")
        self.play(FadeOut(lines), FadeOut(hard), FadeOut(old),
                  FadeOut(boundary), FadeOut(shift_arrow), run_time=.35)
        glow = Circle(radius=.55, color=ACCENT, stroke_width=2.6,
                      fill_color=ACCENT, fill_opacity=.08).move_to(dot)
        self.play(FadeIn(glow), run_time=.3)
        self.stage = VGroup(shapes, centers, dot, glow)
        self.to(15)

        # 15–18: keep both explanations instead of forcing one label.
        self.copy("하나만 고르지 않는다면?", "두 가능성을 그대로 남겨봅니다")
        connectors = VGroup(DashedLine(dot.get_center(), centers[0].get_center(),
                                        color=GOOD),
                            DashedLine(dot.get_center(), centers[1].get_center(),
                                        color=WEIGHT))
        possibilities = VGroup(txt("?", 33, GOOD).move_to([-2.3, 2.6, 0]),
                               txt("?", 33, WEIGHT).move_to([2.3, 2.6, 0]))
        self.play(Create(connectors), FadeIn(possibilities), run_time=.6)
        self.stage = VGroup(shapes, centers, dot, glow, connectors, possibilities)
        self.to(18)

        # 18–21.5: evaluate both Gaussian densities at the observed location.
        self.copy("각 분포가 주는 밀도", "p(x|1)=0.30,    p(x|2)≈0.47")
        self.clear_stage()
        bars = self.bars((.30, .4666666666667), ("p(x|1)", "p(x|2)"),
                         ("0.30", "≈0.47"))
        self.show(bars, FadeIn(bars), run_time=.8)
        self.to(21.5)

        # 21.5–25: multiply density by each component's mixture weight.
        self.copy("섞인 비율도 반영하면", "π₁=0.4, π₂=0.6")
        products = self.bars((.12, .28), ("π₁p(x|1)", "π₂p(x|2)"),
                             ("0.12", "0.28"))
        self.play(Transform(bars, products), run_time=.75)
        self.to(25)

        # 25–28: normalize the two contributions to 30 and 70 percent.
        self.copy("합으로 나누면", "0.12 + 0.28 = 0.40")
        normalized = self.bars((.30, .70), ("P(1|x)", "P(2|x)"),
                               ("30%", "70%"))
        division = txt("0.12 / 0.40      0.28 / 0.40", 28, ACCENT)
        division.move_to([0, -3.8, 0])
        self.play(Transform(bars, normalized), FadeIn(division), run_time=.75)
        self.stage = VGroup(bars, division)
        self.to(28)

        # 28–31.5: formalize the soft component probabilities.
        self.copy("단정 대신 두 가능성을", "30%   +   70%   =   100%")
        self.clear_stage()
        pair = self.gaussian_pair()
        dot = Dot(self.pos(X_RIGHT), radius=.14, color=ACCENT)
        labels = VGroup(txt("30%", 38, GOOD).move_to([-2.3, -2.8, 0]),
                        txt("70%", 38, WEIGHT).move_to([2.3, -2.8, 0]))
        connectors = VGroup(DashedLine(dot.get_center(), [-1.25, 0, 0], color=GOOD),
                            DashedLine(dot.get_center(), [1.25, 0, 0], color=WEIGHT))
        self.show(VGroup(pair, dot, labels, connectors), FadeIn(pair),
                  FadeIn(dot), Create(connectors), FadeIn(labels), run_time=.85)
        self.to(31.5)

        # 31.5–35: introduce the name and its normalized formula.
        self.copy("Responsibility", "성분 k가 관측점 x를 설명할 확률")
        self.clear_stage()
        numerator = txt("πₖ p(x|k)", 37, ACCENT).move_to([0, .7, 0])
        fraction_line = Line([-2.0, .15, 0], [2.0, .15, 0], color=INK,
                             stroke_width=2)
        denominator = txt("Σⱼ πⱼ p(x|j)", 37, ACCENT).move_to([0, -.4, 0])
        name = txt("γₖ(x) =", 39, INK).move_to([-2.8, .15, 0])
        definition = txt("P(z=k | x)", 35, GOOD).move_to([0, -2.15, 0])
        group = VGroup(numerator, fraction_line, denominator, name, definition)
        self.show(group, FadeIn(group), run_time=.8)
        self.to(35)

        # 35–38: show a continuous transition across the former hard boundary.
        self.copy("경계 대신 부드러운 변화", "x가 움직이면 소속 확률도 서서히 변합니다")
        self.clear_stage()
        gradient = self.gradient_strip()
        pointer = Triangle(color=ACCENT, fill_color=ACCENT,
                           fill_opacity=1).scale(.13).rotate(PI)
        pointer.move_to([-3.2, .5, 0])
        labels = VGroup(txt("γ₁≈1", 27, GOOD).move_to([-2.95, -1.2, 0]),
                        txt("γ₁=0.5", 27, INK).move_to([0, -1.2, 0]),
                        txt("γ₁≈0", 27, WEIGHT).move_to([2.95, -1.2, 0]))
        self.show(VGroup(gradient, pointer, labels), FadeIn(gradient),
                  FadeIn(pointer), FadeIn(labels), run_time=.55)
        self.play(pointer.animate.move_to([3.2, .5, 0]), run_time=.9,
                  rate_func=linear)
        self.to(38)

        # 38–41: leave uncertainty instead of a forced 0/1 decision.
        self.copy("Hard에서 Soft로", "0 또는 1   →   0≤γₖ≤1")
        self.clear_stage()
        hard_card = self.assignment_card(-2, PRUNE, "Hard", "0  or  1")
        arrow = Arrow([-.7, 0, 0], [.7, 0, 0], buff=0,
                      color=MUTED, stroke_width=3)
        soft_card = self.assignment_card(2, GOOD, "Soft", "0.30 / 0.70")
        self.show(VGroup(hard_card, arrow, soft_card), FadeIn(hard_card),
                  GrowArrow(arrow), FadeIn(soft_card), run_time=.75)
        self.to(41)

        # 41–45: ask what the 70% means, briefly revealing an unseen choice z.
        self.copy("70%는 무엇의 확률일까?", "보이지 않는 선택  →  관측된 x")
        self.clear_stage()
        hidden = self.assignment_card(-2, ACCENT, "?", "숨은 선택")
        arrow = Arrow([-.7, 0, 0], [.7, 0, 0], buff=0,
                      color=MUTED, stroke_width=3)
        observed = self.assignment_card(2, WEIGHT, "x", "관측된 점")
        self.show(VGroup(hidden, arrow, observed), FadeIn(hidden),
                  GrowArrow(arrow), FadeIn(observed), run_time=.75)
        z = txt("z", 45, ACCENT).move_to([-2, .4, 0])
        question = txt("보이지 않는 변수가 분포를 만든다면?", 30, INK, 7.3)
        question.move_to([0, -3.25, 0])
        teaser = txt("Latent Variable", 26, MUTED).move_to([0, -4.2, 0])
        self.play(Transform(hidden[1], z), FadeIn(question),
                  FadeIn(teaser), run_time=.6)
        self.stage = VGroup(hidden, arrow, observed, question, teaser)
        self.to(45)

    def pos(self, x, y=0):
        return np.array([SCALE*x, SCALE*y, 0])

    def gaussian_pair(self):
        group = VGroup()
        for k, color in enumerate((GOOD, WEIGHT)):
            for radius, opacity in ((2.2, .025), (1.55, .045), (.95, .06)):
                ellipse = Ellipse(width=2*SCALE*SIGMA_X*radius,
                                  height=2*SCALE*VERTICAL_STD*radius,
                                  color=color, stroke_width=1.8,
                                  stroke_opacity=.8,
                                  fill_color=color, fill_opacity=opacity)
                ellipse.move_to(self.pos(MEANS[k]))
                group.add(ellipse)
        return group

    def centers(self):
        return VGroup(*[Dot(self.pos(mean), radius=.1, color=color)
                        for mean, color in zip(MEANS, (GOOD, WEIGHT))])

    def distance_lines(self, x):
        return VGroup(*[DashedLine(self.pos(x), self.pos(mean), color=color,
                                  stroke_width=2.1)
                        for mean, color in zip(MEANS, (GOOD, WEIGHT))])

    def hard_badge(self, which):
        label = txt(f"x → {which}", 35, PRUNE)
        label.move_to([0, -3.25, 0])
        frame = SurroundingRectangle(label, color=PRUNE, buff=.16,
                                     corner_radius=.1)
        return VGroup(frame, label)

    def bars(self, values, names, numbers):
        bars = VGroup()
        baseline = Line([-3.5, -2.4, 0], [3.5, -2.4, 0], color=MUTED)
        bars.add(baseline)
        for k, (value, name, number, color) in enumerate(zip(
                values, names, numbers, (GOOD, WEIGHT))):
            x = -1.65 if k == 0 else 1.65
            height = 3.65 * value / max(values)
            rect = Rectangle(width=1.25, height=height,
                             stroke_color=color, stroke_width=1.8,
                             fill_color=color, fill_opacity=.22)
            rect.move_to([x, -2.4 + height/2, 0])
            value_label = txt(number, 34, color).move_to([x, -2.4+height+.45, 0])
            name_label = txt(name, 27, INK).move_to([x, -3.15, 0])
            bars.add(rect, value_label, name_label)
        return bars

    def gradient_strip(self):
        colors = (ManimColor(GOOD), ManimColor(WEIGHT))
        pieces = VGroup()
        for i in range(54):
            alpha = i/53
            color = interpolate_color(colors[0], colors[1], alpha)
            block = Rectangle(width=6.5/54+.01, height=.62,
                              stroke_width=0, fill_color=color,
                              fill_opacity=.85)
            block.move_to([-3.25+(i+.5)*6.5/54, 0, 0])
            pieces.add(block)
        return pieces

    def assignment_card(self, x, color, title, detail):
        box = RoundedRectangle(width=2.5, height=2.5, corner_radius=.16,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.05)
        box.move_to([x, 0, 0])
        header = txt(title, 38, color, 2.25).move_to([x, .4, 0])
        note = txt(detail, 25, INK, 2.25).move_to([x, -.55, 0])
        return VGroup(box, header, note)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.14)
        self.head = txt(heading, 30, INK, 7.25).move_to([0, 4.95, 0])
        self.caption = txt(caption, 26, INK, 7.25).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.24)

    def show(self, stage, *animations, run_time=.9):
        self.stage = stage
        self.play(*animations, run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.26)
            self.remove(*self.stage)
        self.stage = VGroup()

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width/2, -7.36, 0]), run_time=min(.28, remain))
            tail = target - self.time
            if tail > .001:
                self.wait(tail)
