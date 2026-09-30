"""Distribution mathematics 16: solve the circular GMM inference problem with EM."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, txt


COLORS = (GOOD, WEIGHT)
SCALE = 1.8


def observations():
    rng = np.random.default_rng(16)
    left = rng.multivariate_normal((-.95, .62), ((.16, .04), (.04, .12)), 27)
    right = rng.multivariate_normal((1.02, -.55), ((.2, -.035), (-.035, .13)), 33)
    return np.vstack((left, right))


POINTS = observations()


def posterior(points, weights, means, covs):
    scores = []
    for k in range(2):
        delta = points - means[k]
        inverse = np.linalg.inv(covs[k])
        _, logdet = np.linalg.slogdet(covs[k])
        quadratic = np.einsum("ni,ij,nj->n", delta, inverse, delta)
        scores.append(np.log(weights[k]) - np.log(2*np.pi)
                      - .5*logdet - .5*quadratic)
    scores = np.array(scores).T
    shift = scores.max(axis=1, keepdims=True)
    exponentials = np.exp(scores-shift)
    total = exponentials.sum(axis=1, keepdims=True)
    log_likelihood = float(np.sum(shift + np.log(total)))
    return exponentials/total, log_likelihood


def em_history(points, initial_means, steps=8):
    weights = np.array([.5, .5])
    means = np.array(initial_means, dtype=float)
    covs = np.array([np.eye(2)*.25, np.eye(2)*.25])
    history = []
    for t in range(steps+1):
        gamma, likelihood = posterior(points, weights, means, covs)
        history.append((weights.copy(), means.copy(), covs.copy(),
                        gamma.copy(), likelihood))
        n_k = gamma.sum(axis=0)
        weights = n_k/len(points)
        means = gamma.T @ points / n_k[:, None]
        for k in range(2):
            delta = points-means[k]
            covs[k] = (delta*gamma[:, k, None]).T @ delta/n_k[k]
            covs[k] += np.eye(2)*.002
    return history


HISTORY = em_history(POINTS, ((-1.05, -.45), (1.05, .45)))
OTHER = em_history(POINTS, ((1.95, .48), (.7, -.61)), steps=12)


class ExpectationMaximizationDiscovery(Scene):
    DURATION = 110

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("PART IV  /  DISTRIBUTION MATHEMATICS 16", 18, MUTED).move_to(UP*7.3),
            txt("닭과 달걀의 문제 | Expectation-Maximization", 26, INK, 7.7).move_to(UP*6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–7: continue the unresolved circular question from episode 15.
        self.copy("닭이 먼저냐, 달걀이 먼저냐", "분포를 알아야 소속을, 소속을 알아야 분포를 안다")
        left = self.box("분포 ?", -2.25, GOOD)
        right = self.box("소속 ?", 2.25, WEIGHT)
        arrows = VGroup(
            Arrow([-1, .3, 0], [1, .3, 0], buff=.08, color=ACCENT),
            Arrow([1, -.3, 0], [-1, -.3, 0], buff=.08, color=ACCENT),
        )
        loop = txt("?", 55, ACCENT).move_to([0, -2.2, 0])
        self.show(VGroup(left, right, arrows, loop), FadeIn(left),
                  FadeIn(right), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  FadeIn(loop), run_time=1.15)
        self.to(7)

        # 7–13: the only observations are unlabeled points.
        self.copy("실제로는 둘 다 모릅니다", "xᵢ만 관측  /  zᵢ=?,  μₖ=?,  Σₖ=?")
        self.clear_stage()
        cloud = self.cloud()
        unknown = txt("zᵢ=?,    μₖ=?,    Σₖ=?", 35, PRUNE).move_to([0, -3.4, 0])
        self.show(VGroup(cloud, unknown), FadeIn(cloud), FadeIn(unknown),
                  run_time=1.0)
        self.to(13)

        # 13–20: a visibly imperfect initial model makes the process possible.
        self.copy("완벽한 답을 기다리지 않습니다", "일단 현재의 추정 θ⁽⁰⁾에서 출발")
        self.play(FadeOut(unknown), run_time=.3)
        model = self.model(HISTORY[0])
        label = txt("Initial Guess  /  θ⁽⁰⁾", 28, ACCENT).move_to([0, 3.55, 0])
        self.play(FadeIn(model), FadeIn(label), run_time=1.0)
        self.stage = VGroup(cloud, model, label)
        self.to(20)

        # 20–28: keep the model fixed and infer soft memberships.
        self.copy("현재 분포를 기준으로 소속을 추정", "한 점에도 두 성분의 가능성이 함께 남습니다")
        connections = self.connections((10, 30, 48), HISTORY[0])
        values = self.soft_values((10, 30, 48), HISTORY[0])
        self.play(Create(connections), FadeIn(values), run_time=1.15)
        colored = self.cloud(HISTORY[0][3])
        self.play(Transform(cloud, colored), run_time=1.25)
        self.stage = VGroup(cloud, model, label, connections, values)
        self.to(28)

        # 28–34: name the E-step after the soft assignment is visible.
        self.copy("이것이 E-step", "현재 θ에서 P(zᵢ=k | xᵢ, θ)를 계산")
        step = self.badge("E-step", GOOD, 3.4)
        self.play(FadeOut(label), FadeIn(step), run_time=.5)
        self.stage = VGroup(cloud, model, connections, values, step)
        self.to(34)

        # 34–41: responsibilities act as fractional weights in the new mean.
        self.copy("이제 소속의 무게로 중심을 계산", "90%인 점은 크게, 10%인 점은 작게 반영")
        self.clear_stage()
        weighted = self.weighted_cloud(HISTORY[0][3][:, 0])
        mean0 = Dot(self.pos(*HISTORY[0][1][0]), radius=.13, color=PRUNE)
        mean1 = Dot(self.pos(*HISTORY[1][1][0]), radius=.13, color=GOOD)
        mean_arrow = Arrow(mean0.get_center(), mean1.get_center(),
                           buff=.13, color=ACCENT, stroke_width=3)
        formula = txt("μₖ = Σᵢ γᵢₖ xᵢ / Σᵢ γᵢₖ", 34, INK, 7.2)
        formula.move_to([0, -3.5, 0])
        self.show(VGroup(weighted, mean0, mean1, mean_arrow, formula),
                  FadeIn(weighted), FadeIn(mean0), FadeIn(mean1),
                  GrowArrow(mean_arrow), FadeIn(formula), run_time=1.2)
        self.to(41)

        # 41–48: move both model ellipses to the actual weighted update.
        self.copy("분포도 다시 맞춥니다", "중심 μₖ  /  퍼짐 Σₖ  /  혼합 비율 πₖ")
        self.clear_stage()
        cloud = self.cloud(HISTORY[0][3])
        model = self.model(HISTORY[0])
        self.show(VGroup(cloud, model), FadeIn(cloud), FadeIn(model),
                  run_time=.8)
        self.play(Transform(model, self.model(HISTORY[1])), run_time=1.55)
        self.stage = VGroup(cloud, model)
        self.to(48)

        # 48–54: name the M-step after seeing the model update.
        self.copy("이것이 M-step", "추정한 소속을 가중치로 써 θ를 다시 찾습니다")
        step = self.badge("M-step", WEIGHT, 3.4)
        self.play(FadeIn(step), run_time=.5)
        self.stage = VGroup(cloud, model, step)
        self.to(54)

        # 54–60: the changed model changes the posterior.
        self.copy("하지만 한 번으로 끝나지 않습니다", "새로운 분포에서 소속을 다시 계산")
        self.play(FadeOut(step), run_time=.25)
        first = txt("E  →  P(z|x, θ⁽¹⁾)", 33, GOOD).move_to([0, 3.5, 0])
        self.play(FadeIn(first), Transform(cloud, self.cloud(HISTORY[1][3])),
                  run_time=1.2)
        self.stage = VGroup(cloud, model, first)
        self.to(60)

        # 60–66: update the model again from the new soft memberships.
        self.copy("그리고 다시 분포를 개선", "E  →  M  →  E  →  M")
        second = txt("M  →  θ⁽²⁾", 33, WEIGHT).move_to([0, 3.5, 0])
        self.play(ReplacementTransform(first, second),
                  Transform(model, self.model(HISTORY[2])), run_time=1.35)
        self.stage = VGroup(cloud, model, second)
        self.to(66)

        # 66–74: show several real EM iterations, not a fabricated fit.
        self.copy("번갈아 반복합니다", "불완전한 추정이 다음 추정의 출발점이 됩니다")
        for t in (3, 4, 6, 8):
            self.play(Transform(model, self.model(HISTORY[t])),
                      Transform(cloud, self.cloud(HISTORY[t][3])),
                      Transform(second, txt(f"Iteration {t}", 31, ACCENT)
                                .move_to([0, 3.5, 0])), run_time=.95)
        self.stage = VGroup(cloud, model, second)
        self.to(74)

        # 74–81: show the alternating feedback as the answer to the loop.
        self.copy("서로를 번갈아 개선합니다", "분포 → 소속 추정 → 분포 추정 → …")
        self.clear_stage()
        feedback = self.feedback()
        self.show(feedback, FadeIn(feedback), run_time=1.0)
        self.to(81)

        # 81–88: collect the discovered cycle into the EM name.
        self.copy("Expectation-Maximization", "현재 θ → E: 숨은 z의 분포 → M: 새로운 θ")
        self.clear_stage()
        summary = self.summary()
        self.show(summary, FadeIn(summary), run_time=1.0)
        self.to(88)

        # 88–95: initialization can affect the solution reached.
        self.copy("시작점은 중요합니다", "서로 다른 초기 추정은 다른 해로 갈 수 있습니다")
        self.clear_stage()
        alternatives = self.alternatives()
        self.show(alternatives, FadeIn(alternatives), run_time=1.05)
        self.to(95)

        # 95–103: observed log likelihood rises in the computed example.
        self.copy("그런데 왜 나아질까?", "이 예시의 log p(X|θ)는 반복하며 올라갑니다")
        self.clear_stage()
        graph = self.likelihood_graph()
        self.show(graph, FadeIn(graph), run_time=1.0)
        self.to(103)

        # 103–110: pose the mathematical guarantee as the next episode's question.
        self.copy("EM은 왜 정말 좋아지는가?", "Likelihood  &  Lower Bound")
        question = txt("왜 likelihood가 내려가지 않을까?", 32, ACCENT, 7.2)
        question.move_to([0, -4.2, 0])
        self.play(FadeIn(question), run_time=.5)
        self.stage = VGroup(graph, question)
        self.to(110)

    def pos(self, x, y):
        return np.array([SCALE*x, SCALE*y, 0])

    def cloud(self, gamma=None):
        points = VGroup()
        for i, (x, y) in enumerate(POINTS):
            if gamma is None:
                color = INK
            else:
                color = interpolate_color(ManimColor(COLORS[1]),
                                          ManimColor(COLORS[0]),
                                          float(gamma[i, 0]))
            points.add(Dot(self.pos(x, y), radius=.066, color=color))
        return points

    def weighted_cloud(self, weights):
        return VGroup(*[Dot(self.pos(x, y), radius=.035+.105*float(w),
                            color=GOOD, fill_opacity=.22+.78*float(w))
                        for (x, y), w in zip(POINTS, weights)])

    def model(self, state):
        weights, means, covs, _, _ = state
        shapes = VGroup()
        for k in range(2):
            eigenvalues, eigenvectors = np.linalg.eigh(covs[k])
            major = int(np.argmax(eigenvalues))
            minor = 1-major
            angle = np.arctan2(eigenvectors[1, major],
                               eigenvectors[0, major])
            ellipse = Ellipse(
                width=4*SCALE*np.sqrt(eigenvalues[major]),
                height=4*SCALE*np.sqrt(eigenvalues[minor]),
                stroke_color=COLORS[k], stroke_width=2.6,
                fill_color=COLORS[k], fill_opacity=.035,
            ).rotate(angle).move_to(self.pos(*means[k]))
            center = Dot(self.pos(*means[k]), radius=.13, color=COLORS[k])
            number = txt(f"{int(round(weights[k]*100))}%", 24, COLORS[k])
            number.move_to(self.pos(*means[k])+UP*.43)
            shapes.add(VGroup(ellipse, center, number))
        return shapes

    def connections(self, indices, state):
        return VGroup(*[DashedLine(self.pos(*POINTS[i]),
                                   self.pos(*state[1][k]),
                                   color=COLORS[k], stroke_width=1.25,
                                   stroke_opacity=.65)
                        for i in indices for k in range(2)])

    def soft_values(self, indices, state):
        return VGroup(*[txt(f"{state[3][i,0]:.2f} / {state[3][i,1]:.2f}",
                            21, ACCENT).move_to(self.pos(*POINTS[i])+UP*.37)
                        for i in indices])

    def box(self, label, x, color, y=0, width=2.7):
        outline = RoundedRectangle(width=width, height=1.28,
                                   corner_radius=.16,
                                   stroke_color=color, stroke_width=2,
                                   fill_color=color, fill_opacity=.06)
        outline.move_to([x, y, 0])
        return VGroup(outline, txt(label, 31, INK, width-.2).move_to(outline))

    def badge(self, label, color, y):
        box = RoundedRectangle(width=3.35, height=.92,
                               corner_radius=.15, stroke_color=color,
                               fill_color=color, fill_opacity=.075)
        box.move_to([0, y, 0])
        return VGroup(box, txt(label, 32, color).move_to(box))

    def feedback(self):
        top = self.box("현재 분포 θ", 0, GOOD, 2.7, 4.6)
        middle = self.box("E  /  소속 확률", 0, ACCENT, .15, 4.6)
        bottom = self.box("M  /  새 분포", 0, WEIGHT, -2.4, 4.6)
        arrows = VGroup(
            Arrow([0, 1.97, 0], [0, .9, 0], buff=0, color=MUTED),
            Arrow([0, -.58, 0], [0, -1.67, 0], buff=0, color=MUTED),
            CurvedArrow([2.55, -2.35, 0], [2.55, 2.65, 0],
                        angle=PI/2, color=ACCENT, stroke_width=2.4),
        )
        return VGroup(top, middle, bottom, arrows)

    def summary(self):
        title = txt("Expectation-Maximization", 38, ACCENT, 7.2)
        title.move_to([0, 3.3, 0])
        lines = VGroup(
            txt("θ⁽ᵗ⁾", 39, GOOD).move_to([0, 1.85, 0]),
            txt("↓", 35, MUTED).move_to([0, 1.15, 0]),
            txt("E :  P(z | x, θ⁽ᵗ⁾)", 36, INK).move_to([0, .35, 0]),
            txt("↓", 35, MUTED).move_to([0, -.4, 0]),
            txt("M :  θ⁽ᵗ⁺¹⁾", 36, INK).move_to([0, -1.2, 0]),
            txt("↺  다시 E-step", 30, WEIGHT).move_to([0, -2.65, 0]),
        )
        return VGroup(title, lines)

    def alternatives(self):
        # These are genuine outputs of two different starts on the same points.
        panels = VGroup()
        for j, history in enumerate((HISTORY, OTHER)):
            x_offset = -1.92 if j == 0 else 1.92
            label = txt(f"Initial Guess {chr(65+j)}", 26, COLORS[j])
            label.move_to([x_offset, 3.15, 0])
            small_points = VGroup(*[Dot([x_offset+v[0]*.78,
                                         v[1]*.78, 0], radius=.036,
                                         color=INK) for v in POINTS])
            end = history[-1]
            means = VGroup(*[Dot([x_offset+m[0]*.78, m[1]*.78, 0],
                                 radius=.105, color=COLORS[k])
                             for k, m in enumerate(end[1])])
            frame = RoundedRectangle(width=3.55, height=5.2,
                                     corner_radius=.16,
                                     stroke_color=MUTED,
                                     stroke_opacity=.45).move_to([x_offset, 0, 0])
            score = txt(f"log L = {end[4]:.1f}", 23, MUTED)
            score.move_to([x_offset, -3.1, 0])
            panels.add(VGroup(frame, label, small_points, means, score))
        return panels

    def likelihood_graph(self):
        values = np.array([state[4] for state in HISTORY])
        lo, hi = float(values.min()), float(values.max())
        y = (values-lo)/(hi-lo if hi > lo else 1)
        coords = [np.array([-2.65+i*.66, -2.35+3.65*v, 0])
                  for i, v in enumerate(y)]
        axes = VGroup(Line([-2.85, -2.55, 0], [3.1, -2.55, 0], color=MUTED),
                      Line([-2.85, -2.55, 0], [-2.85, 1.65, 0], color=MUTED))
        curve = VMobject(stroke_color=ACCENT, stroke_width=4)
        curve.set_points_as_corners(coords)
        dots = VGroup(*[Dot(p, radius=.075, color=ACCENT) for p in coords])
        labels = VGroup(
            txt("log p(X|θ)", 29, INK).move_to([-1.65, 2.7, 0]),
            txt("Iteration", 25, MUTED).move_to([1.6, -3.15, 0]),
        )
        return VGroup(axes, curve, dots, labels)

    def copy(self, heading, caption):
        self.play(FadeOut(self.head), FadeOut(self.caption), run_time=.15)
        self.head = txt(heading, 30, INK, 7.25).move_to([0, 4.95, 0])
        self.caption = txt(caption, 26, INK, 7.25).move_to([0, -5.8, 0])
        self.play(FadeIn(self.head), FadeIn(self.caption), run_time=.27)

    def show(self, stage, *animations, run_time=.9):
        self.stage = stage
        self.play(*animations, run_time=run_time)

    def clear_stage(self):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.28)
            self.remove(*self.stage)
        self.stage = VGroup()

    def to(self, target):
        remain = target-self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.3, remain))
            tail = target-self.time
            if tail > .001:
                self.wait(tail)
