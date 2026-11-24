"""Manim scenes for the 220-second probability chapter."""
import json
import math
from pathlib import Path

import numpy as np
from manim import *

DATA = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
config.background_color = '#0B1020'
GOLD, TEAL, BLUE, VIOLET, ORANGE = '#F2B84B', '#26C6B0', '#648CFF', '#B18CFF', '#FF8066'
MUTED = '#A9B7CD'
XS = np.array([-2.66, -2.47, -2.32, -2.18, -2.04, -1.93, -1.77, -1.56,
               1.47, 1.66, 1.84, 2.01, 2.14, 2.24, 2.40, 2.59])


def normal(x, mu=0, sigma=1):
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(math.tau))


def kde(x, h=.43):
    return sum(normal(x, value, h) for value in XS) / len(XS)


def label(words, size=30, color=WHITE):
    return Text(words, font='Malgun Gothic', font_size=size, color=color, line_spacing=.9)


def axes(xmin=-4, xmax=4, ymax=.65, width=10, height=3.25, y=-.55):
    return Axes(x_range=[xmin, xmax, 1], y_range=[0, ymax, ymax/2],
                x_length=width, y_length=height, tips=False,
                axis_config={'include_ticks': False, 'color': MUTED,
                             'stroke_width': 1.5}).move_to(UP*y)


def curve(ax, fn, color=TEAL, width=4):
    return ax.plot(fn, color=color, stroke_width=width, use_smoothing=False,
                   x_range=[ax.x_range[0], ax.x_range[1], (ax.x_range[1]-ax.x_range[0])/160])


def dots(ax, values=XS, radius=.065):
    return VGroup(*(Dot(ax.c2p(value, 0), radius=radius, color=GOLD) for value in values))


def bars(ax, entries, width, color=TEAL):
    return VGroup(*(Rectangle(
        width=np.linalg.norm(ax.c2p(x+width, 0)-ax.c2p(x, 0)),
        height=np.linalg.norm(ax.c2p(x, h)-ax.c2p(x, 0)),
        stroke_width=0, fill_color=color, fill_opacity=.84
    ).move_to(ax.c2p(x, h/2)) for x, h in entries if h > 0))


class ChapterScene(Scene):
    def setup(self):
        shot = next(shot for shot in DATA['scenes'] if shot['class'] == type(self).__name__)
        self.cues = iter(cue for cue in DATA['cues'] if shot['start'] <= cue['start'] < shot['end'])
        self.caption = None

    def title(self, words):
        left = label('CHAPTER 00 / PROBABILITY DISTRIBUTIONS', 16, TEAL).move_to(UP*3.72).to_edge(LEFT, buff=.75)
        path = {
            'ParametricModels': '밀도 추정  /  매개변수적 접근',
            'FrequentistInference': '모수 추정  /  빈도주의',
            'BayesianInference': '모수 추정  /  베이지안',
            'ConjugatePrior': '베이지안 추론  /  켤레성',
            'ModelMisspecification': '매개변수적 접근  /  분포족의 한계',
            'NonparametricDensity': '밀도 추정  /  비모수적 접근',
        }.get(type(self).__name__, words)
        right = label(path, 18, MUTED).move_to(UP*3.72).to_edge(RIGHT, buff=.75)
        rule = Line(LEFT*6.35, RIGHT*6.35, color=TEAL, stroke_width=1).move_to(UP*3.46)
        self.heading = label(words, 34).move_to(UP*2.96).to_edge(LEFT, buff=.75)
        self.add(left, right, rule, self.heading)

    def beat(self, *animations, seconds=1):
        cue = next(self.cues)
        if self.caption is not None:
            self.remove(self.caption)
        words = cue['text']
        if len(words) > 43:
            spaces = [i for i, char in enumerate(words) if char == ' ']
            split = min(spaces, key=lambda i: abs(i - len(words) / 2))
            words = words[:split] + '\n' + words[split + 1:]
        lines = words
        caption = label(lines, 28).move_to(DOWN*3.25)
        if caption.width > 12.25:
            caption.scale_to_fit_width(12.25)
        self.caption = VGroup(
            RoundedRectangle(width=13.1, height=1.08, corner_radius=.12,
                             fill_color='#141D33', fill_opacity=1, stroke_width=0).move_to(caption),
            caption,
        ).set_z_index(20)
        self.add(self.caption)
        duration = cue['end'] - cue['start']
        if animations:
            self.play(*animations, run_time=seconds)
        else:
            seconds = 0
        if duration > seconds:
            self.wait(duration-seconds, frozen_frame=True)


class OpeningDistributions(ChapterScene):
    def construct(self):
        self.title('확률분포와 관측 데이터')
        ax = axes()
        gaussian = curve(ax, normal)
        binomial = bars(ax, [(k-4, math.comb(8,k)/2**8) for k in range(9)], .52)
        poisson = bars(ax, [(k-4, math.exp(-3)*3**k/math.factorial(k))
                            for k in range(9)], .52)
        mixture = curve(ax, kde)
        self.add(ax)
        self.beat(Succession(Create(gaussian), ReplacementTransform(gaussian, binomial),
                             ReplacementTransform(binomial, poisson),
                             ReplacementTransform(poisson, mixture)), seconds=6)
        sample = dots(ax)
        notation = label('관측 데이터  D = (x₁, …, xₙ)', 34, GOLD).move_to(UP*1.75)
        self.beat(Succession(LaggedStart(*(FadeIn(dot) for dot in sample), lag_ratio=.10),
                             AnimationGroup(FadeOut(mixture), FadeIn(notation))), seconds=5)
        estimate = DashedVMobject(curve(ax, kde), num_dashes=40)
        self.beat(Create(estimate), FadeIn(label('밀도 추정', 29, TEAL).move_to(UP*1.13)))


class IIDAssumption(ChapterScene):
    def construct(self):
        self.title('표본을 얻는 가정')
        small_axes = [axes(width=3.1, height=1.65, y=0).shift(RIGHT*x) for x in [-4.2,0,4.2]]
        panels = VGroup(*(VGroup(a, curve(a, kde)) for a in small_axes))
        sample = VGroup(*(dots(a, [x], .085) for a,x in zip(small_axes, XS[[1, 9, 14]])))
        self.beat(FadeIn(panels), LaggedStart(*(FadeIn(dot) for dot in sample), lag_ratio=.5), seconds=4)
        iid = label('독립 동일 분포  ·  i.i.d.', 36, TEAL).move_to(UP*1.68)
        self.beat(Write(iid), seconds=2)
        independence = label('독립  ·  한 관측을 알아도 다른 관측의 분포는 그대로', 29, GOLD).move_to(DOWN*1.52)
        identical = label('동일분포  ·  모든 관측에 같은 확률법칙 적용', 29, TEAL).move_to(DOWN*2.12)
        factorization = label('p(x₁, …, xₙ) = ∏ᵢ p(xᵢ)', 29, TEAL).move_to(UP*1.05)
        self.beat(Succession(FadeIn(independence), Indicate(sample[0]), FadeIn(identical), FadeIn(factorization),
                             AnimationGroup(*(Indicate(panel[1]) for panel in panels))), seconds=9)
        ax = axes(height=2.0)
        question = label('관측값으로 분포를 어떻게 추정할까?', 36).move_to(UP*1.45)
        self.beat(FadeOut(VGroup(panels, sample, iid, independence, identical, factorization)),
                  FadeIn(VGroup(ax, dots(ax), question)), seconds=3)


class ParametricModels(ChapterScene):
    def construct(self):
        self.title('매개변수적 확률분포')
        a = axes(-.5, 6.5, .36, 3.4, 2.15).shift(LEFT*4.1)
        b = axes(-.5, 2.5, 8, 3.4, 2.15)
        c = axes(width=3.4, height=2.15).shift(RIGHT*4.1)
        panels = VGroup(
            VGroup(a, bars(a, [(k, math.comb(6,k)/64) for k in range(7)], .62),
                   label('이항분포 · 성공 횟수', 25).move_to([ -4.1, 1.16, 0])),
            VGroup(b, bars(b, enumerate([5, 3, 7]), .62),
                   label('다항분포 · 범주별 횟수', 25).move_to([0, 1.16, 0])),
            VGroup(c, curve(c, normal), label('가우시안 · 연속값', 25).move_to([4.1, 1.16, 0])),
        )
        vector = label('관측 벡터  (5, 3, 7)', 23, MUTED).move_to(DOWN*1.96)
        binary_ax = axes(-.5, 1.5, .8, 3.4, 2.15).shift(LEFT*4.1)
        binary = VGroup(binary_ax, bars(binary_ax, [(0,.4),(1,.6)], .43),
                        label('베르누이 · 한 번의 0 또는 1', 24).move_to([-4.1,1.16,0]))
        self.beat(Succession(FadeIn(binary), ReplacementTransform(binary, panels[0]),
                             FadeIn(VGroup(panels[1], vector))), seconds=6)
        self.beat(FadeIn(panels[2]), seconds=2)
        self.beat(Indicate(panels, color=TEAL))
        ax = axes()
        center, sigma = ValueTracker(0), ValueTracker(1)
        distribution = always_redraw(lambda: curve(ax, lambda x: normal(x, center.get_value(), sigma.get_value())))
        marker = always_redraw(lambda: DashedLine(ax.c2p(center.get_value(), 0),
                                                   ax.c2p(center.get_value(), .56), color=GOLD))
        formula = label('p(x | μ, σ²)', 37, TEAL).move_to(UP*1.85)
        self.beat(FadeOut(panels), FadeOut(vector), FadeIn(VGroup(ax, formula)),
                  FadeIn(distribution), FadeIn(marker), seconds=3)
        roles = label('평균 μ   ·   위치                 분산 σ²   ·   퍼짐', 28).move_to(UP*1.26)
        self.beat(FadeIn(roles), Succession(center.animate.set_value(1.05),
                                           sigma.animate.set_value(.73)), seconds=6)
        distribution.clear_updaters()
        marker.clear_updaters()
        family = VGroup(*(curve(ax, lambda x: normal(x, mu, sig), TEAL, 2).set_opacity(.52)
                          for mu,sig in [(-1.45,.85),(-.4,1.35),(1.4,1.08)]))
        self.beat(FadeOut(marker), FadeIn(family),
                  Transform(formula, label('분포족은 선택하고, 모수 θ는 추정한다', 33, TEAL).move_to(formula)),
                  seconds=4)


class FrequentistInference(ChapterScene):
    def construct(self):
        self.title('최대가능도추정')
        ax = axes()
        point = dots(ax)
        center = ValueTracker(-1.8)
        fit = always_redraw(lambda: curve(ax, lambda x: normal(x, center.get_value(), 2.15)))
        fixed = label('고정된 관측 데이터    →    변화하는 모수 θ', 31, TEAL).move_to(UP*1.75)
        self.beat(FadeIn(VGroup(ax, point, fixed)))
        self.add(fit)
        self.beat(center.animate.set_value(float(XS.mean())), seconds=7)
        fit.clear_updaters()
        like = axes(-2.7, 2.7, 1.16)
        mean, sd = float(XS.mean()), 2.15 / math.sqrt(len(XS))
        likelihood = lambda x: math.exp(-.5*((x-mean)/sd)**2)
        formula = label('L(θ; D) = ∏ᵢ p(xᵢ | θ)', 34).move_to(UP*1.78)
        labels = VGroup(label('L / L(max)', 22).next_to(like.c2p(-2.7,1.16), UP),
                        label('θ', 26, TEAL).next_to(like.c2p(2.7,0), RIGHT))
        self.beat(FadeOut(VGroup(ax,point,fit,fixed)), FadeIn(VGroup(like,formula,labels)), seconds=2)
        tracker = ValueTracker(-1.38)
        cursor = always_redraw(lambda: Dot(like.c2p(tracker.get_value(), likelihood(tracker.get_value())),
                                          color=GOLD, radius=.10))
        self.beat(Create(curve(like, likelihood)), FadeIn(cursor), seconds=4)
        estimate = label('θ̂ = argmax L(θ; D)', 30, GOLD).move_to(UP*1.13)
        self.beat(tracker.animate.set_value(mean), FadeIn(estimate), seconds=3)


class BayesianInference(ChapterScene):
    def construct(self):
        self.title('베이지안 추론')
        ax = axes(-3.5, 3.5, .9)
        self.beat(FadeIn(ax), Write(label('모수 θ에 대한 불확실성', 33).move_to(UP*1.86)), seconds=3)
        prior = curve(ax, lambda x: normal(x, -.76, .87), BLUE)
        prior_label = label('사전분포', 27, BLUE).move_to(LEFT*3.4+UP*.38)
        self.beat(Create(prior), FadeIn(prior_label), seconds=2)
        formula = label('p(θ | D) ∝ p(D | θ) p(θ)', 34).move_to(UP*1.18)
        self.beat(FadeIn(dots(ax, XS, .047)), Write(formula), seconds=4)
        sd_l = 2.15/math.sqrt(len(XS))
        variance = 1/(1/.87**2+1/sd_l**2)
        mean = variance*(-.76/.87**2+XS.mean()/sd_l**2)
        posterior = curve(ax, lambda x: normal(x, mean, math.sqrt(variance)), VIOLET)
        self.beat(Create(posterior), FadeIn(label('사후분포', 27, VIOLET).move_to(RIGHT*2.35+UP*.78)),
                  seconds=2)


class ConjugatePrior(ChapterScene):
    def construct(self):
        self.title('베타–베르누이 켤레성')
        ax = axes(0,1,3.65)
        prior = curve(ax, lambda p: 6*p*(1-p), BLUE)
        post = curve(ax, lambda p: 252*p**6*(1-p)**2, VIOLET)
        legend = VGroup(label('사전   Beta(α, β)', 29, BLUE),
                        label('사후   Beta(α′, β′)', 29, VIOLET)).arrange(RIGHT, buff=1.15).move_to(UP*1.82)
        p_axis = label('성공 확률  p', 24, TEAL).next_to(ax, DOWN, buff=.1)
        self.beat(FadeIn(VGroup(ax, p_axis, legend[0])), Create(prior), seconds=3)
        self.beat(Create(post), FadeIn(legend[1]), seconds=4)
        results = VGroup(*(Dot(radius=.085, color=GOLD if success else MUTED)
                           for success in [1,1,0,1,1,1])).arrange(RIGHT, buff=.18).move_to(UP*1.12)
        update = label('Beta(2, 2)   →   Beta(2 + 5, 2 + 1)', 32).move_to(UP*1.82)
        self.beat(FadeIn(results), Transform(legend, update), seconds=5)
        general = label('Beta(α + k, β + N − k)', 34, VIOLET).move_to(UP*1.82)
        self.beat(Transform(legend, general), seconds=3)
        self.beat(FadeOut(results), FadeIn(label('같은 분포족 안에서 모수 갱신', 27, GOLD).move_to(UP*1.12)),
                  seconds=2)


class ModelMisspecification(ChapterScene):
    def construct(self):
        self.title('분포족을 잘못 고르면')
        ax = axes(ymax=.55)
        observations = dots(ax)
        mean, sd = ValueTracker(float(XS.mean())), ValueTracker(float(XS.std()))
        fit = always_redraw(lambda: curve(ax, lambda x: normal(x, mean.get_value(), sd.get_value())))
        model = label('단일 가우시안', 30, TEAL).move_to(UP*1.73)
        self.beat(FadeIn(VGroup(ax, observations, model)), FadeIn(fit), seconds=3)
        self.beat(Indicate(model), seconds=3)
        outlines = VGroup(*(SurroundingRectangle(cluster, color=ORANGE, buff=.22, corner_radius=.12)
                            for cluster in [observations[:8], observations[8:]]))
        self.beat(Create(outlines), seconds=2)
        self.beat(Succession(mean.animate.set_value(-1.7), sd.animate.set_value(1),
                             mean.animate.set_value(1.35)), seconds=5)
        self.beat(FadeOut(fit), FadeOut(model), FadeOut(outlines),
                  Write(label('분포의 형태를 미리 정하지 않는다면?', 36).move_to(UP*1.35)), seconds=2)


class NonparametricDensity(ChapterScene):
    def construct(self):
        self.title('비모수적 밀도 추정')
        ax = axes(ymax=.58)
        sample = dots(ax)
        self.add(ax, sample)
        idea = label('데이터에 맞춰 밀도를 추정한다', 31).move_to(UP*1.74)
        heights, edges = np.histogram(XS, bins=np.arange(-4,4.1,1), density=True)
        histogram = bars(ax, zip((edges[:-1]+edges[1:])/2, heights), .97)
        self.beat(FadeIn(idea), FadeIn(histogram), seconds=4)
        self.beat(Transform(idea, label('히스토그램   ·   커널 밀도 추정', 31, TEAL).move_to(idea)),
                  seconds=2)
        kernels = VGroup(*(curve(ax, lambda x: normal(x, v, .43)/len(XS), BLUE, 2) for v in XS))
        density = curve(ax, kde)
        self.beat(FadeOut(histogram),
                  Transform(idea, label('관측값별 커널의 평균', 31, TEAL).move_to(idea)),
                  Succession(LaggedStart(*(Create(k) for k in kernels), lag_ratio=.10),
                             Create(density)), seconds=6)


def roadmap_node(title, detail, x, y, color, width=3.65):
    card = RoundedRectangle(width=width, height=.9, corner_radius=.12,
                            stroke_color=color, stroke_width=1.6, fill_color='#141D33', fill_opacity=1)
    copy = VGroup(label(title, 24, color), label(detail, 17, MUTED)).arrange(DOWN, buff=.07)
    if copy.width > width - .34:
        copy.scale_to_fit_width(width - .34)
    return VGroup(card, copy).move_to([x,y,0])


class ChapterOverview(ChapterScene):
    def construct(self):
        self.title('확률분포를 이해하기 위한 수학적 로드맵')
        root = roadmap_node('관측 데이터 → 밀도 추정', '데이터를 생성한 분포를 추정', 0, 1.86, GOLD, 4.7)
        parametric = roadmap_node('매개변수적 접근', '분포족 선택과 모수 추정', -2.5, .61, TEAL, 4.2)
        flexible = roadmap_node('비모수적 접근', '히스토그램 · 커널 밀도 추정', 4.15, .61, BLUE)
        models = roadmap_node('확률분포', '베르누이 · 이항 · 다항 · 가우시안', -4.52, -.66, TEAL)
        estimates = roadmap_node('모수 추정', '데이터로 모수 알아내기', -.5, -.66, TEAL)
        frequentist = roadmap_node('빈도주의', '가능도 · 최대가능도추정', -2.65, -1.94, GOLD)
        bayesian = roadmap_node('베이지안', '사전 · 사후 · 켤레성', 1.65, -1.94, VIOLET)
        levels = [(parametric, flexible), (models, estimates), (frequentist,bayesian)]
        connectors = [
            VGroup(*(Line(a.get_bottom(), b.get_top(), color=MUTED, stroke_width=2)
                     for a,b in pairs))
            for pairs in [[(root,parametric),(root,flexible)],
                          [(parametric,models),(parametric,estimates)],
                          [(estimates,frequentist),(estimates,bayesian)]]
        ]
        self.beat(Succession(FadeIn(root), *(
            AnimationGroup(Create(links), *(FadeIn(node) for node in level))
            for links,level in zip(connectors, levels)
        )), seconds=7)
        focus = roadmap_node('베르누이 분포', '가능한 결과 0과 1', -4.52, -.66, GOLD)
        others = VGroup(root,parametric,flexible,estimates,frequentist,bayesian,*connectors)
        self.beat(others.animate.set_opacity(.22), ReplacementTransform(models,focus), seconds=4)
        ax = axes(-.55,1.55,.72,7,2.9,y=-.33)
        pmf = bars(ax, [(0,.4),(1,.6)],.34)
        ticks = VGroup(*(label(str(k),23).next_to(ax.c2p(k,0), DOWN, buff=.12) for k in (0,1)))
        next_topic = label('베르누이 분포', 34, GOLD).move_to(UP*1.78)
        self.beat(FadeOut(others), FadeOut(self.heading),
                  ReplacementTransform(focus, next_topic), FadeIn(VGroup(ax,pmf,ticks)), seconds=3)

