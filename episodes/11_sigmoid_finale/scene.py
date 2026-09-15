"""Sigmoid 06: gradient products, probabilities, gates and tradeoffs. 150s."""
import os
import numpy as np
from manim import *

config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,GOLD,BLUE,PINK='#EDF3F7','#94A7B7','#61E4CF','#F3CF75','#68D9F0','#FF8C9D'
DURATION=150
CAPTIONS=[
 (0,'앞에서 Sigmoid의 포화 영역에서는\n기울기가 0에 가까워지고,\n역전파되는 학습 신호도 작아질 수 있다고 했습니다.'),
 (8,'그렇다면 이런 작은 기울기가\n여러 층에서 반복해서 곱해지면 어떻게 될까요?'),
 (15,'역전파에서는 각 층을 거슬러 올라가며\n그 층의 미분값을 곱합니다.'),
 (22,'단순한 예로, 각 단계에서 곱해지는 값이\n모두 0.2라고 해보겠습니다.'),
 (29,'한 번 곱하면 0.2,\n두 번 곱하면 0.04,'),
 (35,'세 번 곱하면 0.008이 됩니다.\n단계를 거칠수록 빠르게 작아집니다.'),
 (42,'Sigmoid 자체의 기울기는\n가장 큰 값도 0.25입니다.'),
 (49,'이런 작은 값의 곱셈이 반복되면\n앞쪽 층에 전달되는 학습 신호가\n매우 작아질 수 있습니다.'),
 (57,'다만 실제 역전파에는 가중치 등도 영향을 주므로,\n전체 기울기가 항상 줄어든다는 뜻은 아닙니다.'),
 (65,'이것이 깊은 신경망의 은닉층에서\nSigmoid를 덜 사용하는 이유 중 하나입니다.'),
 (72,'하지만 그렇다고\nSigmoid가 쓸모없는 함수라는 뜻은 아닙니다.'),
 (78,'어떤 실수 입력도 0과 1 사이로 부드럽게 바꾸고,\n입력이 커질수록 출력도 항상 커집니다.'),
 (87,'그래서 이진 분류에서는 그 출력을\n한 클래스에 속할 확률로 모델링할 수 있습니다.'),
 (95,'또 정보를 얼마나 통과시킬지\n0과 1 사이의 비율로 조절하기에도 알맞습니다.'),
 (103,'이 때문에 이진 분류의 출력이나,\nLSTM과 같은 구조의 게이트에서도\n중요한 역할을 합니다.'),
 (112,'결국 활성화 함수에는\n항상 좋은 함수와 나쁜 함수가 있는 것이 아니라,'),
 (119,'어떤 성질이 필요한지에 따라\n적절한 함수가 달라집니다.'),
 (126,'Sigmoid의 압축은 어떤 상황에서는\n학습 신호를 약하게 만드는 한계가 되지만,'),
 (133,'다른 상황에서는 바로 그 제한된 범위 자체가\n필요한 기능이 되기도 합니다.'),
 (141,'하나의 함수가 가진 성질은 문제가 될 수도 있고,\n동시에 그 함수를 선택하는\n이유가 될 수도 있습니다.'),
]

def sig(x):return 1/(1+np.exp(-x))
def txt(s,size=29,color=INK):
    t=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if t.width>7.6:t.scale_to_fit_width(7.6)
    return t

class SigmoidFinale(Scene):
    def until(self,t):
        if self.time>t+.05:raise ValueError(f'Timing overrun {self.time} > {t}')
        if t>self.time:self.wait(t-self.time)
    def cue(self,i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub,txt(CAPTIONS[i][1]).move_to(DOWN*5.85)),run_time=.4)
    def construct(self):
        series=txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85)
        title=txt('Sigmoid',66).move_to(UP*5.65)
        episode=txt('06  /  한계와 선택의 이유',25,MINT).move_to(UP*4.65)
        heading=txt('작은 기울기가 반복된다면?',31,GOLD).move_to(UP*3.65)
        self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85)
        intro=VGroup(txt('포화',36,BLUE),txt('↓',36,MUTED),txt('σ′(x) ≈ 0',40,GOLD),txt('↓',36,MUTED),txt('약해질 수 있는 학습 신호',30,PINK)).arrange(DOWN,buff=.3).move_to(UP*.2)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(heading),FadeIn(self.sub),FadeIn(intro),run_time=1)
        self.cue(1)
        self.play(FadeOut(intro),run_time=.6)
        blocks=VGroup()
        for i,x in enumerate([-2.5,0,2.5]):
            box=RoundedRectangle(width=1.7,height=1.2,corner_radius=.15,color=MINT,fill_color=MINT,fill_opacity=.05).move_to([x,1.5,0])
            blocks.add(VGroup(box,txt(f'층 {i+1}',28,MINT).move_to(box)))
        arrows=VGroup(*[Arrow([x,1.5,0],[x- .8,1.5,0],buff=0,color=GOLD,stroke_width=3) for x in [1.65,-.85]])
        direction=txt('앞쪽 층  ←  역전파  ←  손실 쪽',26,GOLD).move_to(UP*2.65)
        self.play(FadeIn(blocks),FadeIn(arrows),FadeIn(direction),run_time=.8)
        self.cue(2)
        chain=txt('기울기 × 미분값 × 미분값 × …',30,GOLD).move_to(DOWN*.2)
        self.play(FadeIn(chain),run_time=.7)
        self.cue(3)
        self.play(Transform(chain,txt('1 × 0.2 × 0.2 × 0.2',35,GOLD).move_to(chain)),run_time=.7)
        note=txt('단순화한 예: 각 단계의 미분값을 0.2로 가정',21,MUTED).move_to(DOWN*4.2)
        value=txt('시작 기울기: 1',32,PINK).move_to(DOWN*1.5)
        track=Rectangle(width=6.4,height=.3,stroke_color=MUTED,stroke_width=1).move_to(DOWN*2.5)
        def bar(v):return Rectangle(width=6.4*v,height=.3,stroke_width=0,fill_color=PINK,fill_opacity=1).move_to([-3.2+3.2*v,-2.5,0])
        amount=bar(1)
        self.play(FadeIn(note),FadeIn(value),FadeIn(track),FadeIn(amount),run_time=.7)
        self.cue(4)
        self.play(Indicate(blocks[2]),Transform(value,txt('1회: 0.2',34,PINK).move_to(value)),Transform(amount,bar(.2)),run_time=1.2)
        self.wait(.6)
        self.play(Indicate(blocks[1]),Transform(value,txt('2회: 0.04',34,PINK).move_to(value)),Transform(amount,bar(.04)),run_time=1.2)
        self.cue(5)
        self.play(Indicate(blocks[0]),Transform(value,txt('3회: 0.008',34,PINK).move_to(value)),Transform(amount,bar(.008)),run_time=1.2)
        self.cue(6)
        self.play(Transform(heading,txt('Sigmoid 자체의 미분계수',31,MINT).move_to(heading)),
                  Transform(chain,txt('0 < σ′(x) ≤ 0.25',37,GOLD).move_to(chain)),run_time=.8)
        self.cue(7)
        self.play(Transform(value,txt('0.25⁵ ≈ 0.00098',34,PINK).move_to(value)),Transform(amount,bar(.25**5)),
                  Transform(note,txt('Sigmoid 미분계수 5개만 곱한 상한',23,MUTED).move_to(note)),run_time=.8)
        self.cue(8)
        self.play(Transform(chain,txt('실제 역전파: 가중치와 다른 미분값도 포함',27,GOLD).move_to(chain)),
                  Transform(note,txt('위 수치는 전체 네트워크 기울기의 상한이 아닙니다',21,MUTED).move_to(note)),run_time=.8)
        self.cue(9)
        self.play(Transform(heading,txt('깊은 은닉층에서는 한계가 됩니다',29,PINK).move_to(heading)),run_time=.7)
        self.cue(10)
        self.play(*[FadeOut(m) for m in [blocks,arrows,direction,chain,note,value,track,amount]],
                  Transform(heading,txt('그렇다면, 어디에 유용할까요?',31,MINT).move_to(heading)),run_time=.8)
        ax=Axes(x_range=[-6,6,2],y_range=[0,1.1,.5],x_length=6.7,y_length=3.8,
           axis_config={'color':MUTED,'stroke_width':1.3,'include_ticks':False,'tip_width':.12,'tip_height':.12}).move_to(UP*.5)
        curve=ax.plot(sig,x_range=[-6,6,.03],color=MINT,stroke_width=5)
        labs=VGroup(*[txt(str(x).replace('-','−'),20,MUTED).next_to(ax.c2p(x,0),DOWN,buff=.15) for x in [-6,0,6]],
           *[txt(str(y),20,MUTED).next_to(ax.c2p(-6,y),LEFT,buff=.15) for y in [0,.5,1]])
        graph=VGroup(ax,curve,labs)
        rule=txt('0 < σ(x) < 1  ·  매끄럽고 단조 증가',28,MINT).move_to(DOWN*3.3)
        self.play(FadeIn(graph),FadeIn(rule),run_time=.8)
        self.cue(11)
        dot=Dot(ax.c2p(-5,sig(-5)),radius=.09,color=GOLD)
        self.play(MoveAlongPath(dot,ax.plot(sig,x_range=[-5,5,.03])),run_time=3)
        self.cue(12)
        self.play(FadeOut(graph),FadeOut(dot),FadeOut(rule),Transform(heading,txt('이진 분류: 확률을 모델링',30,MINT).move_to(heading)),run_time=.7)
        prob=VGroup(txt('모델의 점수 z',27,MUTED),txt('z = 1.386…',34,BLUE),txt('↓  Sigmoid',29,MINT),txt('P(y = 1 | 입력) = 0.8',34,GOLD)).arrange(DOWN,buff=.35).move_to(UP*.9)
        gauge=VGroup(Rectangle(width=6.4,height=.4,stroke_color=MUTED),Rectangle(width=5.12,height=.4,stroke_width=0,fill_color=GOLD,fill_opacity=.8).shift(LEFT*.64)).move_to(DOWN*1.6)
        pn=txt('한 클래스에 속할 모델의 예측 확률',24,MUTED).move_to(DOWN*3)
        self.play(FadeIn(prob),FadeIn(gauge),FadeIn(pn),run_time=.8)
        self.cue(13)
        self.play(FadeOut(prob),FadeOut(gauge),FadeOut(pn),Transform(heading,txt('게이트: 얼마나 통과시킬까요?',30,MINT).move_to(heading)),run_time=.7)
        gate=VGroup(txt('통과 비율 g = σ(z)',32,GOLD),txt('출력 = g × 입력',33,MINT)).arrange(DOWN,buff=.45).move_to(UP*1.7)
        example=txt('0.2 × 8 = 1.6',39,BLUE).move_to(DOWN*.2)
        gatebar=bar(.2).set_color(BLUE)
        self.play(FadeIn(gate),FadeIn(example),FadeIn(track),FadeIn(gatebar),run_time=.8)
        self.play(Transform(example,txt('0.8 × 8 = 6.4',39,BLUE).move_to(example)),Transform(gatebar,bar(.8).set_color(BLUE)),run_time=2)
        self.cue(14)
        lstm=txt('LSTM: 입력 · 망각 · 출력 게이트',28,GOLD).move_to(DOWN*3.5)
        self.play(FadeIn(lstm),run_time=.7)
        self.cue(15)
        self.play(*[FadeOut(m) for m in [gate,example,track,gatebar,lstm]],Transform(heading,txt('좋고 나쁨보다, 필요한 성질',31,MINT).move_to(heading)),run_time=.8)
        top=VGroup(txt('깊은 은닉층',27,PINK),txt('작은 미분계수의 반복 곱',30,INK),txt('학습 신호가 약해질 수 있음',27,PINK)).arrange(DOWN,buff=.35).move_to(UP*1.4)
        bottom=VGroup(txt('이진 분류 출력 · 게이트',27,MINT),txt('0과 1 사이의 제한된 범위',30,INK),txt('확률 모델링과 통과 비율',27,MINT)).arrange(DOWN,buff=.35).move_to(DOWN*1.6)
        self.play(FadeIn(top),FadeIn(bottom),run_time=.8)
        self.cue(16)
        self.play(Transform(heading,txt('역할에 맞는 활성화 함수를 선택합니다',28,MINT).move_to(heading)),run_time=.7)
        self.cue(17)
        self.play(Indicate(top,scale_factor=1.04),run_time=1)
        self.cue(18)
        self.play(Indicate(bottom,scale_factor=1.04),run_time=1)
        self.cue(19)
        self.play(FadeOut(top),FadeOut(bottom),run_time=.7)
        end=VGroup(txt('같은 성질',39,GOLD),txt('한계가 되기도,',32,PINK),txt('선택의 이유가 되기도 합니다.',32,MINT)).arrange(DOWN,buff=.65).move_to(UP*.3)
        self.play(FadeIn(end),Transform(episode,txt('SIGMOID  /  SERIES FINALE',23,MINT).move_to(episode)),run_time=.8)
        self.until(DURATION)
