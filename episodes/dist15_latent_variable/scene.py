"""Distribution mathematics 15: generation, hidden choices, and inference."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, txt


# Match the GMM and the 30/70 observation used in episode 14.
WEIGHTS = (.4, .6)
MEANS = (-.5, .5)
STD_X = .4
OBSERVED_X = STD_X**2 * np.log(14 / 9)
STD_Y = WEIGHTS[0] * np.exp(-.5*((OBSERVED_X-MEANS[0])/STD_X)**2) / (
    2*np.pi*STD_X*.12)
COV = np.diag([STD_X**2, STD_Y**2])
SCALE = 2.5
COLORS = (GOOD, WEIGHT)


def fixed_points():
    rng = np.random.default_rng(15)
    groups = [rng.normal(size=(count, 2)) @ np.linalg.cholesky(COV).T
              + np.array([mean, 0])
              for count, mean in zip((24, 36), MEANS)]
    groups[1][0] = [OBSERVED_X, 0]
    return tuple(groups)


POINTS = fixed_points()


class LatentVariableDiscovery(Scene):
    DURATION = 100

    def construct(self):
        self.stage = VGroup()
        self.head = VGroup()
        self.caption = VGroup()
        self.chrome = VGroup(
            txt("PART IV  /  DISTRIBUTION MATHEMATICS 15", 18, MUTED).move_to(UP*7.3),
            txt("관측된 데이터 뒤에는 무엇이 숨어 있을까? | Latent Variable", 27, INK, 7.7).move_to(UP*6.48),
            Line([-3.8, 5.83, 0], [3.8, 5.83, 0], color=MUTED,
                 stroke_opacity=.35),
        )
        self.progress = Rectangle(width=.01, height=.035,
                                  fill_color=ACCENT, fill_opacity=1,
                                  stroke_width=0).move_to([-3.8, -7.36, 0])
        self.add(self.chrome, self.progress)

        # 0–4: pick up the exact ambiguity left by episode 14.
        self.copy("14화의 한 점에서 출발", "γ₁(x)=0.3,   γ₂(x)=0.7")
        pair = self.gaussian_pair()
        dot = Dot(self.pos(OBSERVED_X), radius=.14, color=ACCENT)
        links = self.links(dot.get_center())
        labels = VGroup(txt("30%", 35, GOOD).move_to([-2.1, -2.95, 0]),
                        txt("70%", 35, WEIGHT).move_to([2.1, -2.95, 0]))
        self.show(VGroup(pair, dot, links, labels), FadeIn(pair),
                  FadeIn(dot), Create(links), FadeIn(labels), run_time=.9)
        self.to(4)

        # 4–7.5: turn the percentage into a question about the hidden origin.
        self.copy("70%는 무엇의 확률일까?", "70% of what?")
        self.clear_stage()
        numbers = VGroup(txt("30%", 50, GOOD).move_to([-1.8, 1.3, 0]),
                         txt("70%", 50, WEIGHT).move_to([1.8, 1.3, 0]))
        question = txt("두 번째 Gaussian에서 나왔을 가능성?", 31, INK, 7.2)
        question.move_to([0, -1.05, 0])
        self.show(VGroup(numbers, question), FadeIn(numbers),
                  FadeIn(question), run_time=.7)
        self.to(7.5)

        # 7.5–11: rewind before x existed.
        self.copy("점이 생기기 전으로", "관측 x를 잠시 지웁니다")
        self.clear_stage()
        pair = self.gaussian_pair()
        dot = Dot(self.pos(OBSERVED_X), radius=.14, color=ACCENT)
        rewind = txt("↶", 52, ACCENT).move_to([0, 2.9, 0])
        self.show(VGroup(pair, dot, rewind), FadeIn(pair),
                  FadeIn(dot), FadeIn(rewind), run_time=.6)
        self.play(FadeOut(dot), run_time=.55)
        self.stage = VGroup(pair, rewind)
        self.to(11)

        # 11–15.5: only two distributions and their selection weights remain.
        self.copy("아직 데이터는 없습니다", "π₁=0.4     π₂=0.6")
        weights = VGroup(txt("Gaussian 1\n40%", 29, GOOD).move_to([-2, 2.7, 0]),
                         txt("Gaussian 2\n60%", 29, WEIGHT).move_to([2, 2.7, 0]))
        self.play(FadeOut(rewind), FadeIn(weights), run_time=.55)
        self.stage = VGroup(pair, weights)
        self.to(15.5)

        # 15.5–20: draw the component selector, then choose Gaussian 2.
        self.copy("먼저 어느 분포를 쓸지 선택", "40% / 60% 중 이번에는 두 번째")
        selector = self.selector()
        self.play(FadeIn(selector), run_time=.65)
        chosen = txt("z = 2", 39, ACCENT).move_to([0, -3.55, 0])
        self.play(FadeIn(chosen), pair[1].animate.set_stroke(width=3.1),
                  run_time=.65)
        self.stage = VGroup(pair, weights, selector, chosen)
        self.to(20)

        # 20–24: explicitly assign meaning to the symbol z.
        self.copy("이 선택을 z라고 쓰면", "1번이면 z=1, 2번이면 z=2")
        self.clear_stage()
        z = txt("z = 2", 56, ACCENT).move_to([0, 1.35, 0])
        choices = txt("z ∈ {1, 2}", 38, INK).move_to([0, -.2, 0])
        explanation = txt("분포를 고르는 선택값 하나", 29, MUTED)
        explanation.move_to([0, -1.75, 0])
        self.show(VGroup(z, choices, explanation), FadeIn(z),
                  FadeIn(choices), FadeIn(explanation), run_time=.75)
        self.to(24)

        # 24–28: draw x from the selected component, at the observed location.
        self.copy("선택된 분포에서 x를 뽑습니다", "x | z=2 ~ N(μ₂, Σ₂)")
        self.clear_stage()
        pair = self.gaussian_pair()
        pair[0].set_stroke(opacity=.2)
        pair[0].set_fill(opacity=.008)
        dot = Dot(self.pos(MEANS[1]), radius=.14, color=ACCENT)
        x_label = txt("x", 35, ACCENT).move_to(self.pos(OBSERVED_X)+UP*.5)
        self.show(VGroup(pair, dot, x_label), FadeIn(pair),
                  FadeIn(dot), FadeIn(x_label), run_time=.65)
        self.play(dot.animate.move_to(self.pos(OBSERVED_X)), run_time=.7)
        self.to(28)

        # 28–31.5: state the complete two-step generative model.
        self.copy("생성 과정은 두 단계", "z → Gaussian k → x")
        self.clear_stage()
        formula1 = txt("z ~ Categorical(π)", 35, ACCENT).move_to([0, 2.3, 0])
        formula2 = txt("x | z=k ~ N(μₖ, Σₖ)", 35, WEIGHT).move_to([0, -.15, 0])
        arrow = Arrow([0, 1.6, 0], [0, .55, 0], buff=0, color=MUTED)
        simple = txt("z  →  x", 38, INK).move_to([0, -2.45, 0])
        self.show(VGroup(formula1, formula2, arrow, simple),
                  FadeIn(formula1), GrowArrow(arrow), FadeIn(formula2),
                  FadeIn(simple), run_time=.85)
        self.to(31.5)

        # 31.5–36: repeating the two steps creates a colored mixture sample.
        self.copy("이 과정을 반복하면", "zᵢ → xᵢ   /   여러 관측점")
        self.clear_stage()
        pair = self.gaussian_pair()
        cloud = self.cloud(True)
        self.show(VGroup(pair, cloud), FadeIn(pair),
                  LaggedStart(*[FadeIn(group) for group in cloud],
                              lag_ratio=.5), run_time=1.0)
        self.to(36)

        # 36–40: labels are known to the animation's generator.
        self.copy("만들 때는 출처를 압니다", "색과 숫자 = 각 점을 만든 zᵢ")
        tags = self.sample_tags()
        legend = self.legend()
        self.play(FadeIn(tags), FadeIn(legend), run_time=.65)
        self.stage = VGroup(pair, cloud, tags, legend)
        self.to(40)

        # 40–44: remove source labels from what an observer receives.
        self.copy("관측할 때는 z가 빠집니다", "(xᵢ, zᵢ)  →  xᵢ만 남음")
        self.play(FadeOut(tags), FadeOut(legend),
                  Transform(cloud, self.cloud(False)), run_time=.85)
        self.stage = VGroup(pair, cloud)
        self.to(44)

        # 44–48: an unseen choice remains behind each observed x.
        self.copy("보이는 것은 x뿐", "z=?  →  x")
        self.clear_stage()
        hidden = self.flow_box("z = ?", -2.15, ACCENT)
        arrow = Arrow([-.85, 0, 0], [.85, 0, 0], buff=0,
                      color=MUTED, stroke_width=3)
        observed = self.flow_box("관측 x", 2.15, WEIGHT)
        label = txt("생성 과정에는 있었지만 기록되지 않은 선택", 27, INK, 7.3)
        label.move_to([0, -2.4, 0])
        self.show(VGroup(hidden, arrow, observed, label),
                  FadeIn(hidden), GrowArrow(arrow), FadeIn(observed),
                  FadeIn(label), run_time=.8)
        self.to(48)

        # 48–53: name the latent variable only after the mechanism is clear.
        self.copy("이 모델의 Latent Variable", "잠재변수 z = 관측되지 않은 성분 선택")
        name = txt("Latent Variable / 잠재변수", 35, ACCENT)
        name.move_to([0, 2.45, 0])
        self.play(FadeIn(name), run_time=.45)
        self.stage = VGroup(hidden, arrow, observed, label, name)
        self.to(53)

        # 53–58: return to the point from episode 14 and its two possibilities.
        self.copy("이제 70%의 뜻을 알 수 있습니다", "관측 x 뒤의 z를 거꾸로 추론")
        self.clear_stage()
        pair = self.gaussian_pair()
        dot = Dot(self.pos(OBSERVED_X), radius=.14, color=ACCENT)
        links = self.links(dot.get_center())
        labels = VGroup(txt("P(z=1|x)=0.3", 28, GOOD).move_to([-2.0, -3.0, 0]),
                        txt("P(z=2|x)=0.7", 28, WEIGHT).move_to([2.0, -3.0, 0]))
        self.show(VGroup(pair, dot, links, labels), FadeIn(pair),
                  FadeIn(dot), Create(links), FadeIn(labels), run_time=.85)
        self.to(58)

        # 58–62: generation and inference traverse opposite directions.
        self.copy("생성은 z에서 x로", "추론은 x에서 P(z|x)로")
        self.clear_stage()
        flow = self.two_directions()
        self.show(flow, FadeIn(flow), run_time=.85)
        self.to(62)

        # 62–66.5: responsibility is the inferred posterior, not a known label.
        self.copy("이것이 Responsibility", "γₖ(x) = P(z=k | x)")
        formula = txt("γₖ(x) = P(z=k | x)", 40, ACCENT, 7.2)
        formula.move_to([0, -3.4, 0])
        self.play(FadeIn(formula), run_time=.5)
        self.stage = VGroup(flow, formula)
        self.to(66.5)

        # 66.5–71: prepare to generalize beyond a categorical switch.
        self.copy("GMM의 z는 작은 스위치", "z∈{1,2}   /   다른 z도 가능")
        self.clear_stage()
        switch = self.switch_panel()
        self.show(switch, FadeIn(switch), run_time=.8)
        self.to(71)

        # 71–75.5: a continuous z can change an observation smoothly.
        self.copy("연속적인 잠재변수라면", "z: 0.1 → 0.5 → 0.9")
        self.clear_stage()
        slider = self.slider_panel()
        self.show(slider, FadeIn(slider), run_time=.7)
        knob, output = slider[1], slider[3]
        self.play(knob.animate.move_to([2.65, 1.1, 0]),
                  output.animate.move_to([1.55, -1.35, 0]),
                  run_time=1.05)
        self.to(75.5)

        # 75.5–80: a few hidden coordinates can generate rich observations.
        self.copy("여러 숨은 요인도 가능합니다", "z∈R²  →  x∈R¹⁰⁰")
        self.clear_stage()
        small = self.latent_space()
        large = self.observation_grid()
        arrow = Arrow([-.85, 0, 0], [.75, 0, 0], buff=0,
                      color=ACCENT, stroke_width=3)
        self.show(VGroup(small, large, arrow), FadeIn(small),
                  GrowArrow(arrow), FadeIn(large), run_time=.85)
        self.to(80)

        # 80–84.5: revisit the conceptual message through the observed cloud.
        self.copy("복잡한 결과 뒤의 단순한 구조", "관측의 복잡성 ≠ 원인의 복잡성")
        self.clear_stage()
        cloud = self.cloud(False)
        source = self.flow_box("숨은 z", -2.45, ACCENT, y=2.7, width=2.0)
        arrow = Arrow([-1.35, 2.4, 0], [-.25, 1.4, 0],
                      buff=.05, color=ACCENT, stroke_width=2.5)
        self.show(VGroup(cloud, source, arrow), FadeIn(cloud),
                  FadeIn(source), GrowArrow(arrow), run_time=.85)
        self.to(84.5)

        # 84.5–89: both the hidden assignment and component parameters may be unknown.
        self.copy("현실에서는 둘 다 미지수", "zᵢ=?,   μₖ=?,   Σₖ=?")
        contours = VGroup(*[DashedVMobject(self.one_contour(k, 1.6),
                                           num_dashes=30) for k in range(2)])
        unknowns = VGroup(txt("zᵢ=?", 29, PRUNE).move_to([-2.5, -2.65, 0]),
                          txt("μₖ, Σₖ = ?", 29, PRUNE).move_to([2.25, 2.7, 0]))
        self.play(FadeOut(source), FadeOut(arrow), Create(contours),
                  FadeIn(unknowns), run_time=.75)
        self.stage = VGroup(cloud, contours, unknowns)
        self.to(89)

        # 89–100: leave the circular inference problem for the EM episode.
        self.copy("둘 다 모르면 어디서 시작할까?", "Expectation–Maximization")
        self.clear_stage()
        top = self.flow_box("분포를 알아야 소속을 안다", 0, GOOD,
                            y=1.2, width=6.6)
        bottom = self.flow_box("소속을 알아야 분포를 안다", 0, WEIGHT,
                               y=-1.05, width=6.6)
        question = txt("무엇을 먼저 구해야 할까?", 31, INK)
        question.move_to([0, -3.45, 0])
        self.show(VGroup(top, bottom, question), FadeIn(top),
                  FadeIn(bottom), FadeIn(question), run_time=.65)
        self.to(100)

    def pos(self, x, y=0):
        return np.array([SCALE*x, SCALE*y, 0])

    def one_contour(self, k, radius):
        ellipse = Ellipse(width=2*SCALE*STD_X*radius,
                          height=2*SCALE*STD_Y*radius,
                          color=COLORS[k], stroke_width=2.2,
                          fill_color=COLORS[k], fill_opacity=.035)
        return ellipse.move_to(self.pos(MEANS[k]))

    def gaussian_pair(self):
        return VGroup(*[VGroup(*[self.one_contour(k, radius)
                                 for radius in (2.15, 1.5, .9)])
                        for k in range(2)])

    def links(self, start):
        return VGroup(*[DashedLine(start, self.pos(MEANS[k]), color=COLORS[k],
                                  stroke_width=2.1) for k in range(2)])

    def selector(self):
        box = RoundedRectangle(width=2.15, height=1.0, corner_radius=.15,
                               stroke_color=ACCENT, fill_color=ACCENT,
                               fill_opacity=.07).move_to([0, 2.8, 0])
        question = txt("z = ?", 33, ACCENT).move_to(box)
        arrows = VGroup(Arrow([-.45, 2.2, 0], [-1.65, 1.1, 0],
                              buff=.07, color=GOOD),
                        Arrow([.45, 2.2, 0], [1.65, 1.1, 0],
                              buff=.07, color=WEIGHT))
        return VGroup(box, question, arrows)

    def cloud(self, colored):
        return VGroup(*[VGroup(*[Dot(self.pos(point[0], point[1]),
                                   radius=.061,
                                   color=COLORS[k] if colored else INK)
                                 for point in group])
                        for k, group in enumerate(POINTS)])

    def sample_tags(self):
        labels = VGroup()
        for k, group in enumerate(POINTS):
            for point in group[:5]:
                labels.add(txt(str(k+1), 19, COLORS[k]).move_to(
                    self.pos(point[0], point[1])+UP*.22))
        return labels

    def legend(self):
        return VGroup(txt("z=1", 27, GOOD).move_to([-2.4, -3.2, 0]),
                      txt("z=2", 27, WEIGHT).move_to([2.4, -3.2, 0]))

    def flow_box(self, label, x, color, y=0, width=2.5):
        box = RoundedRectangle(width=width, height=1.3, corner_radius=.16,
                               stroke_color=color, stroke_width=2,
                               fill_color=color, fill_opacity=.06)
        box.move_to([x, y, 0])
        title = txt(label, 28, INK, width-.2).move_to(box)
        return VGroup(box, title)

    def two_directions(self):
        top = VGroup(txt("Generation", 27, GOOD).move_to([-2.45, 2, 0]),
                     txt("z  →  x", 38, INK).move_to([.5, 2, 0]))
        bottom = VGroup(txt("Inference", 27, WEIGHT).move_to([-2.45, -.3, 0]),
                        txt("x  →  P(z|x)", 36, INK).move_to([.65, -.3, 0]))
        line = Line([-3.5, .85, 0], [3.5, .85, 0],
                    color=MUTED, stroke_opacity=.5)
        meanings = VGroup(txt("숨은 선택 → 관측 결과", 27, MUTED).move_to([0, 1.25, 0]),
                          txt("관측 결과 → 숨은 선택 추론", 27, MUTED).move_to([0, -1.05, 0]))
        return VGroup(top, bottom, line, meanings)

    def switch_panel(self):
        left = self.flow_box("z=1", -2, GOOD)
        right = self.flow_box("z=2", 2, WEIGHT)
        or_label = txt("또는", 27, MUTED).move_to([0, 0, 0])
        note = txt("GMM에서는 이산적인 선택", 31, INK).move_to([0, -2.4, 0])
        return VGroup(left, right, or_label, note)

    def slider_panel(self):
        line = Line([-2.65, 1.1, 0], [2.65, 1.1, 0],
                    color=MUTED, stroke_width=4)
        knob = Dot([-2.65, 1.1, 0], radius=.16, color=ACCENT)
        box = RoundedRectangle(width=4.2, height=2.1, corner_radius=.16,
                               stroke_color=WEIGHT, fill_color=WEIGHT,
                               fill_opacity=.035).move_to([0, -1.35, 0])
        output = Dot([-1.55, -1.35, 0], radius=.16, color=WEIGHT)
        labels = VGroup(txt("z=0.1", 25, ACCENT).move_to([-2.65, 1.85, 0]),
                        txt("z=0.9", 25, ACCENT).move_to([2.65, 1.85, 0]),
                        txt("x의 모습도 연속적으로 변함", 27, INK).move_to([0, -3.15, 0]))
        return VGroup(line, knob, box, output, labels)

    def latent_space(self):
        box = RoundedRectangle(width=2.3, height=2.3, corner_radius=.15,
                               stroke_color=ACCENT).move_to([-2.35, 0, 0])
        dots = VGroup(*[Dot([-2.35+.35*np.cos(t), .35*np.sin(t), 0],
                            radius=.07, color=ACCENT)
                        for t in np.linspace(0, TAU, 9, endpoint=False)])
        label = txt("z ∈ R²", 29, ACCENT).move_to([-2.35, -1.65, 0])
        return VGroup(box, dots, label)

    def observation_grid(self):
        cells = VGroup()
        for row in range(10):
            for col in range(10):
                intensity = .2 + .7*np.sin((row+1)*.8+(col+2)*.55)**2
                square = Square(side_length=.22, stroke_width=.45,
                                stroke_color=WEIGHT, fill_color=WEIGHT,
                                fill_opacity=intensity)
                square.move_to([2.25+(col-4.5)*.255,
                                (4.5-row)*.255, 0])
                cells.add(square)
        label = txt("x ∈ R¹⁰⁰", 29, WEIGHT).move_to([2.25, -1.65, 0])
        return VGroup(cells, label)

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
        width = max(.01, 7.6*target/self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8+width/2, -7.36, 0]), run_time=min(.28, remain))
            tail = target-self.time
            if tail > .001:
                self.wait(tail)
