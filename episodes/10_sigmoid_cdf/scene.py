"""Sigmoid finale: standard Logistic CDF and probability integral transform."""
import os
import numpy as np
from manim import *

config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,GOLD,BLUE,PINK='#EDF3F7','#94A7B7','#61E4CF','#F3CF75','#68D9F0','#FF8C9D'
COLORS=[BLUE,'#8DADFF',MINT,GOLD,PINK]
DURATION=137
CAPTIONS=[
 (0, '앞에서 어떤 입력 분포에서는 Sigmoid를 통과한 뒤의\n분포를 정확하게 예측할 수 있다고 했습니다.'),
 (6, '대표적인 경우가 위치 0, 척도 1인\n표준 Logistic 분포입니다.'),
 (13, 'Sigmoid는 바로 이 분포의\n누적분포함수, CDF와 같습니다.'),
 (20, 'CDF는 어떤 값보다 작거나 같은 값이\n나올 확률을 나타냅니다.'),
 (27, 'CDF가 0.7이라면, 그 값 이하에\n전체 확률의 70퍼센트가 누적되어 있다는 뜻입니다.'),
 (35, '그렇다면 표준 Logistic 입력에\nSigmoid를 적용하면 어떻게 될까요?'),
 (41, '각 입력값은 자신의 위치까지\n누적된 확률로 바뀝니다.'),
 (48, '데이터가 많이 모이는 중앙에서는\n작은 입력 차이에도 누적확률이 빠르게 변합니다.'),
 (55, '반대로 데이터가 드문 양끝에서는\n같은 확률 차이를 만들기 위해\n더 큰 입력 간격이 필요합니다.'),
 (63, '그 결과 출력은\n0과 1 사이의 균등분포를 따릅니다.'),
 (70, '즉 출력에서 길이가 같은 구간마다\n같은 확률이 배정됩니다.'),
 (77, '물론 이것이 실제로 뽑힌 값들이\n항상 정확히 같은 간격으로 놓인다는 뜻은 아닙니다.'),
 (85, '많은 표본을 반복해서 관찰했을 때,\n각 구간에서 값이 나타날 확률이 같다는 의미입니다.'),
 (90, '그리고 이 성질은\nSigmoid만의 특별한 현상이 아닙니다.'),
 (96, '연속인 누적분포함수를 가진 확률변수라면,'),
 (101, '자신의 CDF를 적용한 결과는\n0과 1 사이의 균등분포가 됩니다.'),
 (108, '원래 입력값 자체를 보는 대신,\n그 값이 전체 분포에서'),
 (113, '어디쯤 위치하는지를 나타내는\n누적확률로 다시 표현한 것입니다.'),
 (120, '즉 입력 공간의 좌표를\n누적확률이라는 새로운 좌표로 바꾼 셈입니다.'),
 (127, 'Sigmoid에서 시작한 비균일 압축은 이렇게\nCDF와 확률분포의 변환으로 이어집니다.'),
]

def sig(x):return 1/(1+np.exp(-x))
def logit(p):return np.log(p/(1-p))
def txt(s,size=29,color=INK):
    t=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if t.width>7.6:t.scale_to_fit_width(7.6)
    return t
def axes(yrange):
    return Axes(x_range=[-6,6,2],y_range=yrange,x_length=6.7,y_length=3.8,
      axis_config={'color':MUTED,'stroke_width':1.4,'include_ticks':False,'tip_width':.12,'tip_height':.12}).move_to(UP*.4)

class SigmoidCDF(Scene):
    def until(self,t):
        if self.time>t+.05:raise ValueError(f'Timing overrun {self.time} > {t}')
        if t>self.time:self.wait(t-self.time)
    def cue(self,i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub,txt(CAPTIONS[i][1]).move_to(DOWN*5.85)),run_time=.4)
    def construct(self):
        series=txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85)
        title=txt('Sigmoid',66).move_to(UP*5.65)
        episode=txt('05  /  누적확률이라는 새 좌표',25,MINT).move_to(UP*4.65)
        heading=txt('어떤 입력이 균등한 출력을 만들까요?',28,GOLD).move_to(UP*3.65)
        self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85)
        da=axes([0,.28,.1]);dc=da.plot(lambda x:sig(x)*(1-sig(x)),x_range=[-6,6,.03],color=BLUE,stroke_width=5)
        dl=VGroup(*[txt(str(v).replace('-','−'),20,MUTED).next_to(da.c2p(v,0),DOWN,buff=.12) for v in [-6,-3,0,3,6]],
             txt('확률밀도',23,BLUE).move_to(UP*2.95),txt('0.25',20,MUTED).next_to(da.c2p(-6,.25),LEFT,buff=.1))
        density=VGroup(da,dc,dl)
        badge=txt('표준 Logistic 분포',32,BLUE).move_to(DOWN*3.2)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(heading),FadeIn(self.sub),FadeIn(density),FadeIn(badge),run_time=1)
        self.cue(1)
        self.play(Transform(heading,txt('위치 μ = 0  ·  척도 s = 1',30,BLUE).move_to(heading)),run_time=.7)
        self.cue(2)
        ca=axes([0,1.1,.5]);p=ca.c2p
        cc=ca.plot(sig,x_range=[-6,6,.03],color=MINT,stroke_width=5)
        cl=VGroup(*[txt(str(v).replace('-','−'),20,MUTED).next_to(p(v,0),DOWN,buff=.12) for v in [-6,-3,0,3,6]],
            *[txt(str(v),20,MUTED).next_to(p(-6,v),LEFT,buff=.1) for v in [.5,1]],txt('누적확률 F(x)',23,MINT).move_to(UP*2.95))
        cg=VGroup(ca,cc,cl)
        self.play(FadeOut(density),FadeIn(cg),Transform(heading,txt('F(x) = σ(x) = 1 / (1 + e⁻ˣ)',30,MINT).move_to(heading)),
                  Transform(badge,txt('CDF = 누적분포함수',31,MINT).move_to(badge)),run_time=.8)
        self.play(Transform(badge,txt('CDF = 누적분포함수',31,MINT).move_to(badge)),run_time=.4)
        self.cue(3)
        self.play(Transform(badge,txt('F(x) = P(X ≤ x)',34,GOLD).move_to(badge)),run_time=.7)
        self.cue(4)
        v=float(logit(.7))
        guides=VGroup(DashedLine(p(-6,.7),p(v,.7),color=GOLD),DashedLine(p(v,0),p(v,.7),color=GOLD),Dot(p(v,.7),color=GOLD,radius=.09))
        marker=txt('x ≈ 0.847',23,GOLD).move_to(DOWN*2.25)
        self.play(Create(guides),FadeIn(marker),Transform(badge,txt('F(0.847…) = 0.7 = 70%',30,GOLD).move_to(badge)),run_time=1)
        self.cue(5)
        self.play(FadeOut(cg),FadeOut(guides),FadeOut(marker),FadeOut(badge),run_time=.7)
        # Twenty equal-probability representatives are NOT an iid random sample.
        probs=(np.arange(20)+.5)/20;xs=logit(probs)
        def xp(x):return 6.7*x/8
        def up(u):return -3.35+6.7*u
        top=Line([-3.35,1.5,0],[3.35,1.5,0],color=MUTED)
        bottom=Line([-3.35,-1.3,0],[3.35,-1.3,0],color=MUTED)
        labels=VGroup(txt('입력값 x',26,BLUE).move_to(UP*2.4),txt('누적확률 u = F(x)',26,MINT).move_to(DOWN*2.05),
            *[txt(str(x).replace('-','−'),20,MUTED).move_to([xp(x),1.1,0]) for x in [-4,-2,0,2,4]],
            *[txt(f'{u:g}',20,MUTED).move_to([up(u),-1.65,0]) for u in [0,.2,.4,.6,.8,1]])
        sources=VGroup(*[Dot([xp(x),1.5,0],radius=.062,color=COLORS[i//4]) for i,x in enumerate(xs)])
        targets=VGroup(*[Dot([up(u),-1.3,0],radius=.062,color=COLORS[i//4]) for i,u in enumerate(probs)])
        note=txt('그림: 동일한 확률 간격으로 고른 대표값 20개',21,MUTED).move_to(DOWN*3.4)
        self.play(FadeIn(top),FadeIn(bottom),FadeIn(labels),FadeIn(sources),FadeIn(note),
                  Transform(heading,txt('값을 누적확률로 바꿉니다',30,MINT).move_to(heading)),run_time=.8)
        self.cue(6)
        links=VGroup(*[Line(a.get_center(),b.get_center(),color=a.get_color(),stroke_width=1).set_opacity(.3) for a,b in zip(sources,targets)])
        self.play(Create(links),TransformFromCopy(sources,targets),run_time=2.5)
        self.cue(7)
        def interval(a,b,c):
            return VGroup(Line([xp(logit(a)),1.9,0],[xp(logit(b)),1.9,0],color=c,stroke_width=6),
                          Line([up(a),-.85,0],[up(b),-.85,0],color=c,stroke_width=6))
        middle=interval(.45,.55,GOLD)
        self.play(FadeIn(middle),Transform(note,txt('중앙: Δx ≈ 0.401  →  Δu = 0.10',27,GOLD).move_to(note)),run_time=.5)
        self.play(Transform(note,txt('중앙: Δx ≈ 0.401  →  Δu = 0.10',27,GOLD).move_to(note)),run_time=.4)
        self.cue(8)
        tail=interval(.05,.15,BLUE)
        self.play(FadeOut(middle),FadeIn(tail),Transform(note,txt('양끝 쪽: Δx ≈ 1.210  →  Δu = 0.10',26,BLUE).move_to(note)),run_time=.8)
        self.cue(9)
        self.play(FadeOut(top),FadeOut(bottom),FadeOut(labels),FadeOut(sources),FadeOut(targets),FadeOut(links),FadeOut(tail),FadeOut(note),run_time=.7)
        ua=Axes(x_range=[0,1,.2],y_range=[0,1.2,.5],x_length=6.7,y_length=2.9,
                axis_config={'color':MUTED,'stroke_width':1.4,'include_ticks':False,'tip_width':.12,'tip_height':.12}).move_to(UP*.3)
        rects=VGroup()
        for i,c in enumerate(COLORS):
            a,b=i*.2,(i+1)*.2
            rects.add(Polygon(ua.c2p(a,0),ua.c2p(b,0),ua.c2p(b,1),ua.c2p(a,1),stroke_color=c,stroke_width=1.5,fill_color=c,fill_opacity=.4))
        ul=VGroup(*[txt(f'{u:g}',21,MUTED).next_to(ua.c2p(u,0),DOWN,buff=.15) for u in np.linspace(0,1,6)],
            txt('1',23,GOLD).next_to(ua.c2p(0,1),LEFT,buff=.15),txt('확률밀도',24,MINT).move_to(UP*2.65))
        law=txt('X ~ Logistic(0, 1)  →  σ(X) ~ Uniform(0, 1)',27,GOLD).move_to(DOWN*3.25)
        self.play(FadeIn(ua),FadeIn(ul),FadeIn(rects),FadeIn(law),Transform(heading,txt('결과는 균등분포',34,MINT).move_to(heading)),run_time=.8)
        self.cue(10)
        masses=VGroup(*[txt('20%',24,c).move_to(ua.c2p(i*.2+.1,.5)) for i,c in enumerate(COLORS)])
        self.play(FadeIn(masses),run_time=.8)
        self.cue(11)
        sample_note=txt('분포의 성질 ≠ 표본의 정확한 등간격',25,MUTED).move_to(DOWN*4.2)
        self.play(FadeIn(sample_note),run_time=.6)
        self.cue(12)
        self.play(Indicate(masses,scale_factor=1.05),run_time=1)
        self.cue(13)
        self.play(FadeOut(ua),FadeOut(ul),FadeOut(rects),FadeOut(masses),FadeOut(law),FadeOut(sample_note),run_time=.7)
        general=VGroup(txt('확률적분변환',36,MINT),txt('Probability Integral Transform',25,MUTED),
            txt('U = Fₓ(X)',43,GOLD),txt('U ~ Uniform(0, 1)',35,GOLD),txt('조건: X의 누적분포함수 Fₓ가 연속',25,MUTED)).arrange(DOWN,buff=.45).move_to(UP*.15)
        self.play(FadeIn(general),Transform(heading,txt('자신의 CDF를 적용하면',31,MINT).move_to(heading)),run_time=.8)
        self.cue(14)
        self.play(Indicate(general[4],scale_factor=1.04),run_time=.8)
        self.cue(15)
        self.play(Indicate(general[3],scale_factor=1.07),run_time=1)
        self.cue(16)
        self.play(FadeOut(general),run_time=.6)
        ending=VGroup(txt('입력값의 좌표',34,BLUE),txt('↓',38,MUTED),txt('누적확률이라는 좌표',34,GOLD)).arrange(DOWN,buff=.5).move_to(UP*.2)
        self.play(FadeIn(ending),run_time=.8)
        self.cue(17)
        self.play(Indicate(ending[2],scale_factor=1.05),run_time=.8)
        self.cue(18)
        self.play(Transform(heading,txt('입력 좌표 → 누적확률 좌표',30,MINT).move_to(heading)),run_time=.8)
        self.cue(19)
        self.play(Transform(heading,txt('다음 이야기: CDF와 분포변환',29,MINT).move_to(heading)),
                  Transform(episode,txt('SIGMOID  /  SERIES FINALE',23,MINT).move_to(episode)),run_time=.8)
        self.until(DURATION)
