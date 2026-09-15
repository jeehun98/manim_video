"""Sigmoid 04: empirical distributions from deterministic normal quantiles."""
import os
from statistics import NormalDist
import numpy as np
from manim import *

config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,GOLD,PINK,BLUE='#EDF3F7','#94A7B7','#61E4CF','#F3CF75','#FF8C9D','#68D9F0'
DURATION=100
CAPTIONS=[
 (0,'지금까지는 하나의 입력값이 Sigmoid를\n통과하면서 어떻게 변하는지 살펴봤습니다.'),
 (6,'이번에는 많은 값들을\n한꺼번에 넣어보겠습니다.'),
 (12,'입력값들이 0 근처에 많이 모여 있다면,'),
 (18,'Sigmoid를 통과한 뒤에도\n많은 값들이 0.5 근처에 모입니다.'),
 (25,'하지만 입력의 범위가 더 넓어지면\n상황이 달라집니다.'),
 (32,'큰 음수들은 0 근처로,\n큰 양수들은 1 근처로 압축됩니다.'),
 (40,'Sigmoid는 각 값을 독립적으로 변환하지만,\n그 결과 데이터 전체의 분포 형태도 함께 바뀝니다.'),
 (48,'중앙의 입력 차이는 양끝에 비해 더 많이 남고,\n양끝에 있던 값들은 더 좁은 출력 구간으로 몰립니다.'),
 (57,'여기서 중요한 점은 Sigmoid가\n항상 같은 분포를 만드는 것은 아니라는 것입니다.'),
 (64,'출력 분포는 Sigmoid의 모양뿐 아니라,\n입력이 원래 어떻게 분포했는지에 따라서도 달라집니다.'),
 (73,'예를 들어 입력이 양수 쪽에 모여 있다면,\n출력도 0.5보다 큰 쪽에 많이 모입니다.'),
 (81,'즉 같은 함수라도 입력 분포가 달라지면\n출력 분포 역시 달라집니다.'),
 (88,'그런데 입력 분포가 수학적으로 주어지면,\n변환 뒤의 분포도 계산할 수 있습니다.'),
 (94,'어떤 입력 분포에서는 그 결과가\n아주 익숙한 분포가 되기도 합니다.'),
]

def sig(x):return 1/(1+np.exp(-x))
def txt(s,size=29,color=INK):
    t=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if t.width>7.6:t.scale_to_fit_width(7.6)
    return t

# A fixed set of normal quantiles makes comparisons reproducible, with no
# random sampling noise between cases. All 240 values remain inside [-8,8].
Q=np.array([NormalDist().inv_cdf((i+.5)/240) for i in range(240)])
XBINS=np.linspace(-8,8,33)
YBINS=np.linspace(0,1,21)
CASES=[(.0,.5,'A  /  0 근처에 모인 입력',MINT),
       (.0,2.5,'B  /  더 넓게 퍼진 입력',GOLD),
       (2.,.5,'C  /  양수 쪽에 모인 입력',PINK)]

def xpos(v,output=False):return -3.35+6.7*(v if output else (v+8)/16)
def base(output=False):return -3.15 if output else .55
def hist(values,output=False,color=MINT):
    edges=YBINS if output else XBINS
    counts,_=np.histogram(values,edges)
    bars=VGroup()
    for a,b,n in zip(edges[:-1],edges[1:],counts):
        height=max(.001,n*1.8/120)
        bars.add(Rectangle(width=(xpos(b,output)-xpos(a,output))*.9,height=height,
             stroke_width=0,fill_color=color,fill_opacity=.85 if n else 0).move_to([(xpos(a,output)+xpos(b,output))/2,base(output)+height/2,0]))
    return bars

def dots(values,output=False):
    edges=YBINS if output else XBINS
    counts={}
    result=VGroup()
    for v in values:
        j=int(np.clip(np.searchsorted(edges,v,side='right')-1,0,len(edges)-2))
        k=counts.get(j,0);counts[j]=k+1
        result.add(Dot([xpos(v,output),base(output)+(k+.5)*1.8/120,0],radius=.025,
                       color=BLUE if (v<.5 if output else v<0) else PINK))
    return result

def chart_axes(output=False):
    b=base(output)
    ticks=[0,.25,.5,.75,1] if output else [-8,-4,0,4,8]
    group=VGroup(Line([-3.35,b,0],[3.35,b,0],color=MUTED,stroke_width=1.5))
    for v in ticks:
        x=xpos(v,output)
        group.add(Line([x,b,0],[x,b-.08,0],color=MUTED),txt(f'{v:g}'.replace('-','−'),19,MUTED).move_to([x,b-.25,0]))
    for n in [60,120]:
        y=b+n*1.8/120
        group.add(DashedLine([-3.35,y,0],[3.35,y,0],color=MUTED,stroke_width=.8).set_opacity(.25),txt(str(n),17,MUTED).move_to([-3.7,y,0]))
    group.add(txt('출력 y = σ(x)' if output else '입력 x',24,MINT if output else INK).move_to([0,b+2.2,0]))
    return group

class SigmoidDistribution(Scene):
    def until(self,t):
        if self.time>t+.05:raise ValueError(f'Timing overrun {self.time} > {t}')
        if t>self.time:self.wait(t-self.time)
    def cue(self,i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub,txt(CAPTIONS[i][1]).move_to(DOWN*5.8)),run_time=.4)
    def construct(self):
        series=txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85)
        title=txt('Sigmoid',66).move_to(UP*5.65)
        episode=txt('04  /  값에서 분포로',25,MINT).move_to(UP*4.65)
        heading=txt('하나의 값 → 많은 값',30,GOLD).move_to(UP*3.65)
        self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.8)
        single=VGroup(txt('0',43,BLUE),txt('→  Sigmoid  →',32,MINT),txt('0.5',43,PINK)).arrange(RIGHT,buff=.35).move_to(UP*.4)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(heading),FadeIn(self.sub),FadeIn(single),run_time=1)
        self.cue(1)
        self.play(FadeOut(single),run_time=.4)
        topax,botax=chart_axes(),chart_axes(True)
        connector=txt('↓  각 값에 같은 Sigmoid 적용',23,GOLD).move_to(DOWN*.3)
        note=txt('240개 표본 · 세로축: 구간별 개수',21,MUTED).move_to(DOWN*4.15)
        # Fixed bin widths and scales across all three cases.
        binsnote=txt('입력 구간 폭 0.5  /  출력 구간 폭 0.05',19,MUTED).move_to(DOWN*4.6)
        values=Q*.5
        source=dots(values)
        self.play(FadeIn(topax),FadeIn(botax),FadeIn(connector),FadeIn(note),FadeIn(binsnote),FadeIn(source),run_time=1)
        self.cue(2)
        self.play(Transform(heading,txt(CASES[0][2],29,MINT).move_to(heading)),run_time=.6)
        self.cue(3)
        target=dots(sig(values),True)
        self.play(TransformFromCopy(source,target),run_time=2.5)
        ih,oh=hist(values),hist(sig(values),True)
        self.play(ReplacementTransform(source,ih),ReplacementTransform(target,oh),run_time=1)
        self.cue(4)
        wide=Q*2.5
        self.play(Transform(heading,txt(CASES[1][2],29,GOLD).move_to(heading)),FadeOut(oh),
                  Transform(ih,hist(wide,color=GOLD)),run_time=1.5)
        self.cue(5)
        source=dots(wide);target=dots(sig(wide),True)
        self.play(FadeIn(source),ih.animate.set_opacity(.2),run_time=.5)
        self.play(TransformFromCopy(source,target),run_time=3)
        oh=hist(sig(wide),True,GOLD)
        self.play(FadeOut(source),ReplacementTransform(target,oh),ih.animate.set_opacity(1),run_time=.7)
        self.cue(6)
        self.play(Indicate(oh,scale_factor=1),run_time=1)
        self.cue(7)
        # Highlight actual output bins rather than suggesting endpoint atoms.
        self.play(oh[0].animate.set_color(BLUE),oh[-1].animate.set_color(PINK),run_time=.7)
        self.play(Indicate(oh[0],scale_factor=1.15),Indicate(oh[-1],scale_factor=1.15),run_time=1)
        self.cue(8)
        self.play(Transform(heading,txt('같은 함수가 같은 분포를 만들까요?',28,GOLD).move_to(heading)),run_time=.7)
        self.cue(9)
        self.play(Transform(heading,txt(CASES[0][2],29,MINT).move_to(heading)),
                  Transform(ih,hist(values)),Transform(oh,hist(sig(values),True)),run_time=1.5)
        self.cue(10)
        shifted=2+Q*.5
        self.play(Transform(heading,txt(CASES[2][2],29,PINK).move_to(heading)),
                  Transform(ih,hist(shifted,color=PINK)),Transform(oh,hist(sig(shifted),True,PINK)),run_time=2)
        self.cue(11)
        self.play(Transform(heading,txt('입력 분포가 바뀌면 출력 분포도 바뀝니다',26,MINT).move_to(heading)),run_time=.6)
        self.play(Transform(ih,hist(wide,color=GOLD)),Transform(oh,hist(sig(wide),True,GOLD)),run_time=1.3)
        self.play(Transform(ih,hist(values)),Transform(oh,hist(sig(values),True)),run_time=1.3)
        self.cue(12)
        self.play(FadeOut(ih),FadeOut(oh),FadeOut(topax),FadeOut(botax),FadeOut(connector),FadeOut(note),FadeOut(binsnote),run_time=.7)
        question=VGroup(txt('입력 분포',33,BLUE),txt('↓  Sigmoid',30,MINT),txt('예측 가능한 출력 분포',33,GOLD)).arrange(DOWN,buff=.65).move_to(UP*.3)
        self.play(FadeIn(question),Transform(heading,txt('변환 뒤의 분포도 계산할 수 있을까요?',28,MINT).move_to(heading)),run_time=.8)
        self.cue(13)
        ending=txt('어떤 입력이 어떤 분포를 만들까요?',31,GOLD).move_to(DOWN*3)
        self.play(FadeIn(ending),run_time=.8)
        self.until(DURATION)
