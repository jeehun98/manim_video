"""Neural Network Mathematics Part 2, episode 11: Benign Overfitting."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.nnmath2p09_edge_of_stability.scene import (
    NeuralMathPart2EdgeOfStability, card, label,
)
from episodes.prune_series.visuals import ACCENT, GOOD, MUTED, PRUNE, SPARSE, WEIGHT, ZERO


class NeuralMathPart2BenignOverfitting(NeuralMathPart2EdgeOfStability):
    DURATION = 174

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        title = VGroup(label("Benign Overfitting", 24, ACCENT),
                       label("노이즈까지 외웠는데 왜 일반화될까?", 22))
        title.arrange(DOWN, buff=.1).move_to(UP * 6.55)
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 11", 16, MUTED).move_to(UP * 7.55),
            title,
            Line([-3.8, 5.75, 0], [3.8, 5.75, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        self.copy("노이즈까지 따라가면 오버피팅이라고 배웠습니다", "THE CLASSICAL PICTURE",
                  "signal과 noise가 섞인 data에서 모델이 모든 점을 따라가면\n새 data에서의 prediction은 나빠진다는 그림입니다.")
        data = self.noisy_fit_panel()
        self.show(data)
        self.play(Create(data[-1]), run_time=1.0)
        self.to(8)

        self.copy("그런데 train noise를 전부 맞춰도 테스트가 좋을 수 있습니다", "THE PARADOX",
                  "과매개변수화된 모델에서 train data를 정확히 interpolation하고도\nprediction error가 작을 수 있는 조건이 존재합니다.")
        paradox = VGroup(card("TRAIN ERROR = 0", GOOD, 5.4, .88, 28, .14),
                         label("그런데", 23, MUTED),
                         card("TEST ERROR can be small", ACCENT, 6.4, .9, 27, .15))
        paradox.arrange(DOWN, buff=.35).move_to([0, .15, 0])
        self.show(paradox)
        self.to(19)

        self.copy("이 역설을 고차원 linear regression에서 보겠습니다", "SIGNAL + NOISE",
                  "y는 signal인 x transpose w star와 random noise epsilon의 합입니다.\ninterpolation은 관측된 y를 noise까지 모두 맞춥니다.")
        model = VGroup(card("yᵢ = xᵢᵀ w* + εᵢ", WEIGHT, 6.2, 1.05, 34, .13),
                       label("↓", 31, MUTED),
                       card("Xŵ = y", GOOD, 4.4, .92, 34, .14),
                       label("ŷ(xᵢ) = yᵢ  ·  noise included", 22, PRUNE))
        model.arrange(DOWN, buff=.34).move_to([0, .15, 0])
        self.show(model)
        self.to(32)

        self.copy("하지만 data를 맞추는 parameter는 하나가 아닙니다", "MANY INTERPOLATING SOLUTIONS",
                  "parameter가 sample보다 많으면 Xw=y를 만족하는 해가 여러 개입니다.\n모두 train error는 0이지만 새 input에서의 행동은 다를 수 있습니다.")
        family = self.solution_family(False)
        self.show(family)
        self.play(LaggedStart(*[Indicate(p, color=SPARSE) for p in family[-1]],
                              lag_ratio=.12), run_time=1.1)
        self.to(41)

        self.copy("방향이 적으면 noise 하나가 전체 prediction을 흔듭니다", "LOW DIMENSION",
                  "2차원에서 noise를 맞추기 위한 변화가 signal 방향과 크게 겹치면\n훈련점 하나를 맞추려고 새 data의 출력까지 크게 바뀝니다.")
        low = self.low_dim_panel()
        self.show(low)
        self.play(GrowArrow(low[2]), run_time=.8)
        self.to(51)

        self.copy("고차원에서는 여분의 방향이 많아집니다", "2D  →  20D  →  1000D",
                  "prediction에 중요한 signal 축은 그대로 두고,\n개별적으로 영향이 작은 방향이 수많이 존재할 수 있습니다.")
        fan = self.dimension_fan(14)
        self.show(fan)
        self.play(LaggedStart(*[Create(a) for a in fan[1]], lag_ratio=.06), run_time=1.2)
        self.to(59)

        self.copy("많은 방향은 noise의 영향을 나누어 가질 수 있습니다", "ONE LARGE MOVE  vs  MANY SMALL MOVES",
                  "방향이 하나면 큰 변화가 필요하지만, 수많은 방향이 있으면\nnoise fitting에 필요한 변화를 작게 나누어 담을 수 있습니다.")
        compare = self.one_vs_many()
        self.show(compare)
        self.play(Indicate(compare[1], color=GOOD), run_time=.85)
        self.to(68)

        self.copy("하지만 방향의 수만 많다고 충분하지는 않습니다", "DATA COVARIANCE MATTERS",
                  "새 input이 각 parameter 방향으로 얼마나 크게 변하는지,\n즉 data covariance의 spectrum이 중요합니다.")
        cov = self.covariance_axes()
        self.show(cov)
        self.to(77)

        self.copy("큰 eigenvalue와 수많은 작은 eigenvalue를 나누어 봅니다", "HEAD  +  LONG TAIL",
                  "spectrum의 앞쪽은 input variance가 큰 주요 방향입니다.\n뒷쪽은 개별적으로 variance가 작은 많은 방향입니다.")
        spectrum = self.covariance_spectrum(False)
        self.show(spectrum)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in spectrum[1]],
                              lag_ratio=.045), run_time=1.2)
        self.to(86)

        self.copy("noise를 외우되, 새 data가 거의 움직이지 않는 곳에 담습니다", "FIT NOISE IN THE TAIL",
                  "충분히 큰 low-variance tail에 noise fitting 변화가 퍼지면\ntrain sample은 정확히 맞추면서도 population prediction 영향은 작을 수 있습니다.")
        stored = self.noise_in_tail()
        self.show(stored)
        self.play(LaggedStart(*[Indicate(d, color=PRUNE) for d in stored[-1]],
                              lag_ratio=.08), run_time=1.0)
        self.to(98)

        self.copy("훈련점에서는 noise까지 맞았습니다", "EXACT INTERPOLATION",
                  "그러나 새 x는 low-variance 방향으로 크게 변하지 않습니다.\n그 방향에 저장된 noise가 test prediction에 주는 영향은 작을 수 있습니다.")
        train_test = self.train_test_panel()
        self.show(train_test)
        self.to(109)

        self.copy("그래서 고차원이라는 사실만으로는 부족합니다", "NOT DIMENSION ALONE",
                  "benign overfitting은 모든 큰 모델에서 자동으로 나타나지 않습니다.\nsample 수와 signal, covariance tail의 effective rank가 함께 중요합니다.")
        conditions = self.conditions_panel()
        self.show(conditions)
        self.to(119)

        self.copy("또 어떤 interpolating solution을 고르는지가 중요합니다", "SOLUTION SELECTION",
                  "Xw=y를 만족하는 해 중 아무거나 고른다고\n좋은 generalization이 보장되는 것은 아닙니다.")
        choices = self.solution_family(False)
        self.show(choices)
        self.play(Indicate(choices[-1][-1], color=PRUNE), run_time=.8)
        self.to(128)

        self.copy("대표적인 이론은 minimum-norm interpolator를 봅니다", "MINIMUM NORM",
                  "train data를 정확히 맞추는 해들 중 ∥w∥가 가장 작은 해입니다.\n원점에서 solution set에 가장 가까운 점으로 볼 수 있습니다.")
        minimum = self.solution_family(True)
        self.show(minimum)
        self.play(GrowArrow(minimum[-2]), Indicate(minimum[-1][0], color=GOOD), run_time=1.0)
        self.to(139)

        self.copy("이 선택은 implicit bias와 연결됩니다", "OPTIMIZATION CHOOSES A SOLUTION",
                  "overparameterized linear least squares에서 특정 gradient descent 설정은\n여러 해 중 minimum-norm 해로 향하는 bias를 만들 수 있습니다.")
        chain = self.implicit_chain()
        self.show(chain)
        self.play(LaggedStart(*[Indicate(chain[i], color=[WEIGHT, SPARSE, GOOD][i // 2])
                                for i in range(0, 5, 2)], lag_ratio=.2), run_time=1.1)
        self.to(150)

        self.copy("Double Descent와 연결되지만 같은 질문은 아닙니다", "TWO DIFFERENT QUESTIONS",
                  "Double Descent는 model size에 따른 test error 곡선을 묻습니다.\nBenign Overfitting은 noise까지 맞춘 해가 왜 잘 예측할 수 있는지를 묻습니다.")
        self.show(self.double_descent_compare())
        self.to(160)

        self.copy("문제는 noise를 외웠다는 사실만이 아닐 수 있습니다", "WHERE WAS THE NOISE STORED?",
                  "어떤 spectrum에서, 어떤 interpolating solution을 통해\nnoise를 어떤 방향으로 맞춰는지가 generalization을 바꿀 수 있습니다.")
        final = VGroup(card("INTERPOLATION", WEIGHT, 5.0, .84, 27, .12),
                       label("≠", 39, PRUNE),
                       card("BAD GENERALIZATION", PRUNE, 6.2, .9, 26, .12),
                       label("↓", 30, MUTED),
                       card("어떤 방향으로 맞춰는가", ACCENT, 6.5, .92, 27, .15))
        final.arrange(DOWN, buff=.26).move_to([0, .2, 0])
        self.show(final)
        self.to(174)

    def noisy_fit_panel(self):
        origin = np.array([-3.15, -1.55, 0])
        axes = VGroup(Line(origin, origin + RIGHT * 6.3, color=MUTED, stroke_width=1.5),
                      Line(origin, origin + UP * 3.7, color=MUTED, stroke_width=1.5))
        xs = np.linspace(-3, 3, 11)
        base = .42 * xs + .2 * np.sin(1.2 * xs)
        noise = np.array([.12, -.2, .32, -.35, .26, -.12, .38, -.28, .2, -.18, .1])
        dots = VGroup(*[Dot([x, .25 + y + n, 0], radius=.07, color=WEIGHT)
                        for x, y, n in zip(xs, base, noise)])
        smooth_pts = [np.array([x, .25 + .42*x + .2*np.sin(1.2*x), 0]) for x in np.linspace(-3, 3, 120)]
        smooth = VMobject(stroke_color=GOOD, stroke_width=3).set_points_smoothly(smooth_pts)
        over_pts = [np.array([x, .25 + .42*x + .2*np.sin(1.2*x) +
                             .29*np.sin(4.8*x), 0]) for x in np.linspace(-3, 3, 180)]
        over = VMobject(stroke_color=PRUNE, stroke_width=3.5).set_points_smoothly(over_pts)
        return VGroup(axes, dots, smooth, label("signal", 18, GOOD).move_to([-2.55, 2.1, 0]),
                      label("fit every point", 18, PRUNE).move_to([2.15, 2.1, 0]), over)

    def solution_family(self, minimum):
        axes = VGroup(Line([-3.1, -2.35, 0], [3.1, -2.35, 0], color=MUTED, stroke_width=1.4),
                      Line([-2.55, -2.8, 0], [-2.55, 2.55, 0], color=MUTED, stroke_width=1.4))
        line = Line([-2.0, 2.1, 0], [2.9, -1.75, 0], color=SPARSE, stroke_width=4)
        ts = [.12, .34, .56, .78, .96]
        pts = VGroup(*[Dot(line.point_from_proportion(t), radius=.105,
                           color=GOOD if minimum and i == 1 else WEIGHT)
                       for i, t in enumerate(ts)])
        title = label("Xw = y  solution set", 20, SPARSE).move_to([.9, 2.35, 0])
        group = VGroup(axes, line, title)
        if minimum:
            target = pts[1].get_center()
            arrow = Arrow([-2.55, -2.35, 0], target, buff=.13, color=ACCENT,
                          stroke_width=5, max_tip_length_to_length_ratio=.13)
            return VGroup(group, label("∥w∥ minimum", 21, GOOD).move_to([1.3, -2.45, 0]), arrow, pts)
        return VGroup(group, label("all interpolate", 21, ACCENT).move_to([1.25, -2.45, 0]), pts)

    def low_dim_panel(self):
        origin = np.array([-2.7, -1.65, 0])
        signal = Arrow(origin, origin + RIGHT * 5.2, buff=0, color=GOOD, stroke_width=7)
        correction = Arrow(origin + RIGHT * 2.8, origin + RIGHT * 4.4 + UP * 2.1,
                           buff=0, color=PRUNE, stroke_width=7)
        shifted = DashedLine(origin, origin + RIGHT * 4.4 + UP * 2.1,
                             color=ACCENT, dash_length=.14)
        return VGroup(signal, shifted, correction,
                      label("signal direction", 20, GOOD).move_to([0, -2.3, 0]),
                      card("new prediction shifts", PRUNE, 4.8, .72, 21, .12).move_to([0, 2.25, 0]))

    def dimension_fan(self, count):
        origin = np.array([0, -.65, 0])
        main = Arrow([-3.15, -.65, 0], [3.25, -.65, 0], buff=0, color=GOOD, stroke_width=7)
        arrows = VGroup()
        for angle in np.linspace(.35, 2.79, count):
            end = origin + 2.15 * np.array([np.cos(angle), np.sin(angle), 0])
            arrows.add(Arrow(origin, end, buff=0, color=SPARSE, stroke_opacity=.5,
                             stroke_width=3, max_tip_length_to_length_ratio=.11))
        return VGroup(main, arrows, label("important signal", 20, GOOD).move_to([0, -1.4, 0]),
                      label("many weak directions", 20, SPARSE).move_to([0, 2.35, 0]))

    def one_vs_many(self):
        left = VGroup(card("1 DIRECTION", PRUNE, 3.25, .75, 21, .12),
                      Arrow(LEFT*1.1, RIGHT*1.1, color=PRUNE, stroke_width=8),
                      label("one large change", 19, PRUNE)).arrange(DOWN, buff=.58)
        rays = VGroup()
        for a in np.linspace(-1.0, 1.0, 9):
            rays.add(Arrow(ORIGIN, 1.25*np.array([np.cos(a), np.sin(a), 0]), buff=0,
                           color=GOOD, stroke_width=3, max_tip_length_to_length_ratio=.13))
        right = VGroup(card("MANY DIRECTIONS", GOOD, 3.4, .75, 20, .12), rays,
                       label("many small changes", 19, GOOD)).arrange(DOWN, buff=.58)
        return VGroup(left, right).arrange(RIGHT, buff=.55).move_to([0, .1, 0])

    def covariance_axes(self):
        origin = np.array([0, -.55, 0])
        major = DoubleArrow([-3.15, -.55, 0], [3.15, -.55, 0], buff=0,
                            color=GOOD, stroke_width=6)
        weak = VGroup()
        for a in np.linspace(.25, 2.9, 11):
            weak.add(Line(origin, origin + 2.0*np.array([np.cos(a), np.sin(a), 0]),
                          color=SPARSE, stroke_opacity=.38, stroke_width=2))
        return VGroup(weak, major,
                      card("large variance", GOOD, 3.0, .65, 20, .11).move_to([0, -1.45, 0]),
                      card("many low-variance directions", SPARSE, 5.4, .65, 19, .11).move_to([0, 2.35, 0]))

    def covariance_spectrum(self, noise):
        baseline = Line([-3.25, -1.8, 0], [3.25, -1.8, 0], color=MUTED, stroke_width=1.5)
        heights = [3.3, 2.5, 1.8, 1.0, .63, .5, .42, .36, .31, .27, .24, .21, .19, .17]
        bars = VGroup()
        for i, h in enumerate(heights):
            color = GOOD if i < 4 else SPARSE
            bars.add(Rectangle(width=.32, height=h, stroke_width=0,
                               fill_color=color, fill_opacity=.82).align_to(baseline, DOWN)
                     .move_to([-2.85 + i*.43, -1.8 + h/2, 0]))
        labels = VGroup(label("important head", 18, GOOD).move_to([-2.15, 2.15, 0]),
                        label("long low-variance tail", 18, SPARSE).move_to([1.55, .3, 0]))
        dots = VGroup()
        if noise:
            for i in range(5, 14):
                dots.add(Dot(bars[i].get_top() + UP*.18, radius=.065, color=PRUNE))
        return VGroup(baseline, bars, labels, dots)

    def noise_in_tail(self):
        spectrum = self.covariance_spectrum(True)
        brace = Brace(spectrum[1][5:], DOWN, color=ACCENT)
        text = label("noise corrections spread here", 19, ACCENT).next_to(brace, DOWN, buff=.18)
        return VGroup(spectrum[0], spectrum[1], spectrum[2], brace, text, spectrum[3])

    def train_test_panel(self):
        train = VGroup(card("TRAIN SAMPLE", WEIGHT, 3.3, .72, 20, .12),
                       card("signal + noise", PRUNE, 3.3, .78, 23, .12),
                       label("↓", 27, MUTED), card("exact fit", GOOD, 3.3, .72, 22, .13)).arrange(DOWN, buff=.34)
        test = VGroup(card("NEW SAMPLE", ACCENT, 3.3, .72, 20, .12),
                      card("mostly signal", GOOD, 3.3, .78, 23, .12),
                      label("↓", 27, MUTED), card("small impact", GOOD, 3.3, .72, 22, .13)).arrange(DOWN, buff=.34)
        return VGroup(train, test).arrange(RIGHT, buff=.55).move_to([0, .15, 0])

    def conditions_panel(self):
        rows = VGroup(card("OVERPARAMETERIZED", WEIGHT, 6.0, .72, 22, .11),
                      card("SUITABLE COVARIANCE SPECTRUM", SPARSE, 6.0, .72, 21, .12),
                      card("LARGE EFFECTIVE-RANK TAIL", ACCENT, 6.0, .72, 21, .13),
                      card("APPROPRIATE SOLUTION SELECTION", GOOD, 6.0, .72, 20, .12))
        rows.arrange(DOWN, buff=.33).move_to([0, .25, 0])
        return rows

    def implicit_chain(self):
        chain = VGroup(card("MANY SOLUTIONS", WEIGHT, 5.4, .75, 23, .12), label("↓", 28, MUTED),
                       card("GRADIENT DESCENT BIAS", SPARSE, 5.4, .75, 22, .12), label("↓", 28, MUTED),
                       card("MINIMUM-NORM SOLUTION", GOOD, 5.4, .78, 22, .13))
        chain.arrange(DOWN, buff=.28).move_to([0, .15, 0])
        return chain

    def double_descent_compare(self):
        left = VGroup(card("DOUBLE DESCENT", WEIGHT, 3.4, .74, 20, .12),
                      self.dd_curve(), label("model size → test error", 17, MUTED)).arrange(DOWN, buff=.45)
        right = VGroup(card("BENIGN OVERFITTING", ACCENT, 3.55, .74, 19, .13),
                       card("Train error = 0", GOOD, 3.2, .68, 19, .1),
                       label("why can test error stay small?", 16, MUTED)).arrange(DOWN, buff=.45)
        return VGroup(left, right).arrange(RIGHT, buff=.38).move_to([0, .15, 0])

    def dd_curve(self):
        frame = RoundedRectangle(width=3.2, height=2.25, corner_radius=.14,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.1)
        xs = np.linspace(-1.25, 1.25, 120)
        ys = .18 + .32*(xs+.8)**2 + 1.0*np.exp(-((xs+.05)/.24)**2)
        points = [np.array([x, -.8 + y, 0]) for x, y in zip(xs, ys)]
        curve = VMobject(stroke_color=WEIGHT, stroke_width=3.5).set_points_smoothly(points)
        return VGroup(frame, curve)
