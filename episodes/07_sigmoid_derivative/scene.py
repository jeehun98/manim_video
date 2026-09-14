"""Sigmoid 02: derivative as local change retention. Silent, 100 seconds."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT = '#EDF3F7', '#94A7B7', '#61E4CF'
GOLD, BLUE, PINK = '#F3CF75', '#68D9F0', '#FF8C9D'

CAPTIONS = [
    (0, '앞에서 Sigmoid는 입력 공간을\n위치에 따라 서로 다른 비율로 압축한다고 했습니다.'),
    (6, '그렇다면 그 압축 비율은\n어떻게 알 수 있을까요?'),
    (11, '그래프의 한 지점을 아주 가까이서 보면,\n그 주변에서는 거의 직선처럼 볼 수 있습니다.'),
    (19, '이때 기울기는 입력이 조금 변할 때\n출력이 얼마나 변하는지를 나타냅니다.'),
    (26, '출력 변화량을 입력 변화량으로 나누면\n그 구간의 평균 변화율을 구할 수 있습니다.'),
    (33, '입력 변화량을 0에 한없이 가깝게 보내면,\n한 점에서의 순간 변화율, 즉 미분계수가 됩니다.'),
    (41, 'Sigmoid의 기울기는 시그모이드 값에\n1에서 시그모이드 값을 뺀 값을 곱한 것입니다.'),
    (49, '가운데, 입력이 0일 때\n기울기는 가장 큰 0.25입니다.'),
    (56, '즉 입력이 아주 조금 변하면, 출력에서는\n대략 그 변화의 4분의 1이 나타납니다.'),
    (64, '하지만 양끝으로 갈수록\n기울기는 점점 0에 가까워집니다.'),
    (71, '작은 입력 변화가\n출력에서는 거의 드러나지 않는다는 뜻입니다.'),
    (77, '결국 Sigmoid의 기울기는 단순히\n그래프가 얼마나 가파른지를 나타내는 값이 아니라,'),
    (84, '각 위치에서 작은 입력 차이를 얼마나 남기는지\n보여주는 국소적인 압축률로 볼 수 있습니다.'),
    (91, '이 값이 작을수록 더 강하게 압축됩니다.'),
    (95, '그리고 이 값이 거의 0이 되는 영역에서는\n또 다른 문제가 시작됩니다.'),
]
DURATION = 100

def sig(x):
    return 1/(1+np.exp(-x))

def slope(x):
    return sig(x)*(1-sig(x))

def txt(s, size=30, color=INK):
    t = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.15)
    if t.width > 7.6:
        t.scale_to_fit_width(7.6)
    return t

def axes(xrange, yrange, height=4.3):
    return Axes(x_range=xrange, y_range=yrange, x_length=6.8, y_length=height,
                axis_config={'color':MUTED,'stroke_width':1.4,'include_ticks':False,
                             'tip_width':.12,'tip_height':.12}).move_to(UP*.4)

def overview():
    ax = axes([-6,6,2],[0,1.1,.5])
    p = ax.c2p
    labels = VGroup(*[txt(str(x).replace('-', '−'),20,MUTED).next_to(p(x,0),DOWN,buff=.15) for x in [-6,-3,0,3,6]],
        *[txt(str(y),20,MUTED).next_to(p(-6,y),LEFT,buff=.13) for y in [0,.5,1]],
        txt('입력 x',21,MUTED).move_to(DOWN*2.65),txt('출력 σ(x)',21,MUTED).move_to(LEFT*2.5+UP*3))
    guides = VGroup(*[DashedLine(p(-6,y),p(6,y),color=MUTED,stroke_width=1).set_opacity(.4) for y in [.5,1]])
    graph = ax.plot(sig,x_range=[-6,6,.035],color=MINT,stroke_width=5)
    return ax,VGroup(ax,labels,guides,graph)

class SigmoidDerivative(Scene):
    def until(self,t):
        if self.time>t+.05:
            raise ValueError(f'Timing overrun {self.time} > {t}')
        if t>self.time:
            self.wait(t-self.time)

    def cue(self,i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub,txt(CAPTIONS[i][1],29).move_to(DOWN*5.8)),run_time=.4)

    def construct(self):
        self.sub = txt(CAPTIONS[0][1],29).move_to(DOWN*5.8)
        series = txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85)
        title = txt('Sigmoid',66).move_to(UP*5.65)
        episode = txt('02  /  기울기로 읽는 압축률',25,MINT).move_to(UP*4.65)
        headline = txt('같은 입력 변화, 다른 출력 변화',29,MINT).move_to(UP*3.65)
        ax,whole = overview()
        badge = txt('중앙은 덜 압축 · 양끝은 더 압축',27,GOLD).move_to(DOWN*3.65)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(headline),FadeIn(self.sub),run_time=.8)
        self.play(FadeIn(whole),FadeIn(badge),run_time=1)
        self.cue(1)
        focus = Circle(radius=.35,color=GOLD,stroke_width=3).move_to(ax.c2p(0,.5))
        self.play(Create(focus),Transform(badge,txt('한 점 주변의 변화를 살펴봅니다',28,GOLD).move_to(badge)),run_time=.8)

        self.cue(2)
        # Magnified local coordinates: both axes explicitly show displacement.
        local = axes([-.2,.2,.1],[-.05,.05,.025])
        p = local.c2p
        local_labels = VGroup(
            *[txt(f'{v:g}'.replace('-','−'),19,MUTED).next_to(p(v,0),DOWN,buff=.13) for v in [-.2,0,.2]],
            *[txt(f'{v:g}'.replace('-','−'),19,MUTED).next_to(p(-.2,v),LEFT,buff=.12) for v in [-.05,.05]],
            txt('입력 변화 x − 0',22,MUTED).move_to(DOWN*2.65),
            txt('출력 변화 σ(x) − 0.5',22,MUTED).move_to(UP*3))
        lc = local.plot(lambda x:sig(x)-.5,x_range=[-.2,.2,.002],color=MINT,stroke_width=6)
        tangent = DashedLine(p(-.19,-.19*.25),p(.19,.19*.25),color=GOLD,stroke_width=3)
        zoom = VGroup(local,local_labels,lc,tangent)
        self.play(FadeOut(whole),FadeOut(focus),FadeIn(zoom),
                  Transform(headline,txt('x = 0 주변 확대',31,MINT).move_to(headline)),
                  Transform(badge,txt('곡선 ≈ 접선',32,GOLD).move_to(badge)),run_time=1.5)
        self.play(Indicate(lc,scale_factor=1),run_time=1)

        self.cue(3)
        h = ValueTracker(.16)
        tri = always_redraw(lambda: VGroup(
            Line(p(0,0),p(h.get_value(),0),color=BLUE,stroke_width=5),
            Line(p(h.get_value(),0),p(h.get_value(),sig(h.get_value())-.5),color=PINK,stroke_width=5),
            Dot(p(0,0),radius=.08,color=GOLD),Dot(p(h.get_value(),sig(h.get_value())-.5),radius=.08,color=GOLD)))
        secant = always_redraw(lambda: Line(p(-.19,-.19*(sig(h.get_value())-.5)/h.get_value()),
            p(.19,.19*(sig(h.get_value())-.5)/h.get_value()),color=GOLD,stroke_width=2))
        legend = VGroup(txt('가로: Δx',24,BLUE),txt('세로: Δy',24,PINK)).arrange(RIGHT,buff=.65).move_to(DOWN*3.3)
        self.play(FadeOut(badge),FadeOut(tangent),FadeIn(tri),FadeIn(secant),FadeIn(legend),run_time=.8)
        ratio = txt('평균 변화율 = Δy / Δx',30,GOLD).move_to(DOWN*4.25)
        self.cue(4)
        self.play(FadeIn(ratio),run_time=.6)
        self.cue(5)
        self.play(h.animate.set_value(.045),run_time=3)
        self.play(Transform(ratio,txt('Δx → 0    Δy / Δx → σ′(x)',29,GOLD).move_to(ratio)),run_time=.8)
        self.play(Transform(headline,txt('순간 변화율 = 미분계수',30,MINT).move_to(headline)),run_time=.6)

        self.cue(6)
        tri.clear_updaters(); secant.clear_updaters()
        formula = txt('σ′(x) = σ(x) · [1 − σ(x)]',34,GOLD).move_to(UP*1.3)
        definition = txt('σ(x) = 1 / (1 + e⁻ˣ)',30,MINT).move_to(UP*2.6)
        derivation = VGroup(txt('s = σ(x)',27,MUTED),txt('s(1 − s) = 0.25 − (s − 0.5)²',29,INK)).arrange(DOWN,buff=.4).move_to(DOWN*.4)
        self.play(FadeOut(zoom),FadeOut(tri),FadeOut(secant),FadeOut(legend),FadeOut(ratio),
                  FadeIn(formula),FadeIn(definition),FadeIn(derivation),
                  Transform(headline,txt('Sigmoid의 미분',31,MINT).move_to(headline)),run_time=1)
        self.cue(7)
        maximum = txt('x = 0  →  0.5 × 0.5 = 0.25',31,GOLD).move_to(DOWN*2.1)
        maxnote = txt('0 < σ′(x) ≤ 0.25',29,MINT).move_to(DOWN*3.5)
        self.play(FadeIn(maximum),FadeIn(maxnote),run_time=.8)
        self.play(Indicate(derivation[-1]),run_time=.8)
        self.cue(8)
        example = VGroup(txt('Δy ≈ σ′(x) · Δx',33,GOLD),
            txt('x = 0 에서  Δx = 0.01',27,MUTED),txt('Δy ≈ 0.25 × 0.01 = 0.0025',30,MINT)).arrange(DOWN,buff=.45).move_to(DOWN*1.2)
        self.play(FadeOut(derivation),FadeOut(maximum),FadeOut(maxnote),FadeIn(example),run_time=.8)

        self.cue(9)
        da = axes([-6,6,2],[0,.28,.1])
        dp = da.c2p
        dlabels = VGroup(*[txt(str(x).replace('-','−'),20,MUTED).next_to(dp(x,0),DOWN,buff=.15) for x in [-6,-3,0,3,6]],
            txt('0.25',21,GOLD).next_to(dp(-6,.25),LEFT,buff=.12),
            txt('기울기 σ′(x)',22,GOLD).move_to(UP*3),txt('입력 x',22,MUTED).move_to(DOWN*2.65))
        dcurve = da.plot(slope,x_range=[-6,6,.035],color=GOLD,stroke_width=5)
        top = DashedLine(dp(-6,.25),dp(6,.25),color=MUTED,stroke_width=1)
        dgraph = VGroup(da,dlabels,dcurve,top)
        self.play(FadeOut(formula),FadeOut(definition),FadeOut(example),FadeIn(dgraph),
                  Transform(headline,txt('기울기 자체를 그려 보면',30,MINT).move_to(headline)),run_time=1)
        center = Dot(dp(0,.25),color=GOLD,radius=.09)
        ends = VGroup(*[Dot(dp(x,slope(x)),color=BLUE,radius=.09) for x in [-5,5]])
        values = txt('x = ±5    σ′(x) ≈ 0.00665',28,BLUE).move_to(DOWN*3.6)
        self.play(FadeIn(center),TransformFromCopy(center,ends),FadeIn(values),run_time=1.5)
        self.cue(10)
        self.play(Transform(values,txt('Δx = 0.01 → Δy ≈ 0.0000665\nx = ±5에서의 국소 근사',26,BLUE).move_to(values)),run_time=.7)
        self.cue(11)
        self.play(Transform(headline,txt('기울기 = 작은 차이가 남는 비율',28,MINT).move_to(headline)),run_time=.7)
        self.cue(12)
        self.play(Transform(values,txt('Δy ≈ σ′(x) · Δx',34,GOLD).move_to(values)),run_time=.7)
        self.cue(13)
        self.play(Indicate(ends),Transform(episode,txt('작은 기울기 → 강한 국소 압축',25,MINT).move_to(episode)),run_time=.8)
        self.cue(14)
        self.play(Transform(values,txt('기울기가 거의 0이라면?',34,PINK).move_to(values)),run_time=.7)
        self.until(DURATION)
