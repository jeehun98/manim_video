"""Sigmoid 03: saturation and the local backward multiplier, 100 seconds."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width, config.frame_height = 9,16
config.frame_rate = 30
config.background_color = '#091119'
INK,MUTED,MINT = '#EDF3F7','#94A7B7','#61E4CF'
GOLD,BLUE,PINK = '#F3CF75','#68D9F0','#FF8C9D'
DURATION = 100
CAPTIONS = [
 (0,'앞에서 Sigmoid의 기울기는\n작은 입력 차이를 얼마나 남기는지 보여주는\n국소적인 압축률이라고 했습니다.'),
 (7,'그런데 양끝으로 갈수록\n이 기울기는 점점 0에 가까워집니다.'),
 (13,'이 영역에서는 입력이 조금 변해도\n출력은 거의 변하지 않습니다.'),
 (19,'이처럼 출력이 양끝의 값에 가까워져\n입력 변화에 둔감해진 상태를 포화라고 합니다.'),
 (26,'예를 들어 입력이 이미 큰 양수라면,\n값이 조금 더 커져도 출력은 거의 1에 머뭅니다.'),
 (34,'큰 음수에서도 마찬가지입니다.\n출력은 거의 0에 머물고,\n입력 변화는 잘 드러나지 않습니다.'),
 (42,'문제는 이 기울기가\n순전파에서만 중요한 것이 아니라는 점입니다.'),
 (48,'학습할 때는 손실을 줄이기 위해,\n각 값이 손실에 미치는 영향을 역방향으로 계산합니다.'),
 (56,'역전파에서는 출력 쪽 손실 기울기에\nSigmoid의 기울기를 곱해\n입력 쪽 손실 기울기를 구합니다.'),
 (66,'포화 영역에서는 곱해지는 값이 거의 0이므로,\n이 함수를 통과하는 학습 신호가 크게 줄어듭니다.'),
 (74,'즉 Sigmoid의 양끝에서는\n출력에 드러나는 작은 입력 차이뿐 아니라,'),
 (80,'입력 쪽으로 전달되는\n손실의 기울기까지 작아질 수 있습니다.'),
 (86,'이것이 Sigmoid의 포화가\n기울기 소실, Vanishing Gradient와 연결되는 이유입니다.'),
 (94,'그렇다면 이런 작은 값의 곱셈이\n여러 층에서 반복되면 어떻게 될까요?'),
]

def sig(x): return 1/(1+np.exp(-x))
def slope(x): return sig(x)*(1-sig(x))
def txt(s,size=29,color=INK):
    t=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if t.width>7.6: t.scale_to_fit_width(7.6)
    return t

class SigmoidSaturation(Scene):
    def until(self,t):
        if self.time>t+.05: raise ValueError(f'Timing overrun: {self.time} > {t}')
        if t>self.time: self.wait(t-self.time)
    def cue(self,i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub,txt(CAPTIONS[i][1]).move_to(DOWN*5.8)),run_time=.4)

    def construct(self):
        series=txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85)
        title=txt('Sigmoid',66).move_to(UP*5.65)
        episode=txt('03  /  포화와 작아지는 학습 신호',24,MINT).move_to(UP*4.65)
        headline=txt('σ′(x) = σ(x) · [1 − σ(x)]',31,GOLD).move_to(UP*3.65)
        self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.8)
        ax=Axes(x_range=[-7,7,2],y_range=[0,1.1,.5],x_length=6.8,y_length=4.3,
                axis_config={'color':MUTED,'stroke_width':1.4,'include_ticks':False,'tip_width':.12,'tip_height':.12}).move_to(UP*.4)
        p=ax.c2p
        labels=VGroup(*[txt(str(v).replace('-','−'),20,MUTED).next_to(p(v,0),DOWN,buff=.15) for v in [-6,-3,0,3,6]],
            *[txt(str(v),20,MUTED).next_to(p(-7,v),LEFT,buff=.12) for v in [0,.5,1]],
            txt('입력 x',21,MUTED).move_to(DOWN*2.65),txt('출력 σ(x)',21,MUTED).move_to(LEFT*2.5+UP*3))
        guides=VGroup(*[DashedLine(p(-7,y),p(7,y),color=MUTED,stroke_width=1).set_opacity(.45) for y in [.5,1]])
        curve=ax.plot(sig,x_range=[-7,7,.04],color=MINT,stroke_width=5)
        graph=VGroup(ax,labels,guides,curve)
        badge=txt('중앙: 0.25    양끝: 0에 가까움',28,GOLD).move_to(DOWN*3.7)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(headline),FadeIn(self.sub),run_time=.8)
        self.play(FadeIn(graph),FadeIn(badge),run_time=1)
        self.cue(1)
        tails=VGroup(ax.plot(sig,x_range=[-7,-3.5,.03],color=BLUE,stroke_width=8),ax.plot(sig,x_range=[3.5,7,.03],color=PINK,stroke_width=8))
        self.play(Create(tails),run_time=1)
        self.cue(2)
        self.play(Indicate(tails,scale_factor=1),run_time=1)
        self.cue(3)
        self.play(Transform(headline,txt('포화  /  Saturation',34,GOLD).move_to(headline)),
                  Transform(badge,txt('출력이 입력 변화에 둔감해집니다',28,GOLD).move_to(badge)),run_time=.8)
        self.cue(4)
        x=ValueTracker(5)
        dot=always_redraw(lambda:Dot(p(x.get_value(),sig(x.get_value())),radius=.1,color=PINK))
        guide=always_redraw(lambda:DashedLine(p(x.get_value(),0),p(x.get_value(),sig(x.get_value())),color=PINK,stroke_width=1.5))
        positive=txt('x: 5 → 6\nσ(x): 0.9933 → 0.9975',29,PINK).move_to(badge)
        self.play(FadeIn(dot),FadeIn(guide),Transform(badge,positive),run_time=.6)
        self.play(x.animate.set_value(6),run_time=3)
        self.cue(5)
        # Reposition offscreen between demonstrations; avoid implying a tail-only sweep.
        self.play(FadeOut(dot),FadeOut(guide),run_time=.3)
        x.set_value(-5)
        self.play(FadeIn(dot),FadeIn(guide),Transform(badge,txt('x: −5 → −6\nσ(x): 0.0067 → 0.0025',29,BLUE).move_to(badge)),run_time=.6)
        self.play(x.animate.set_value(-6),run_time=3)
        self.cue(6)
        dot.clear_updaters(); guide.clear_updaters()
        self.play(FadeOut(graph),FadeOut(tails),FadeOut(dot),FadeOut(guide),FadeOut(badge),
                  Transform(headline,txt('순전파에서 역전파로',32,MINT).move_to(headline)),run_time=.8)
        box=RoundedRectangle(width=2.5,height=1.25,corner_radius=.18,color=MINT,fill_color=MINT,fill_opacity=.06).move_to(UP*1.6)
        block=VGroup(box,txt('Sigmoid',31,MINT).move_to(box))
        inp=txt('x',40,BLUE).move_to(LEFT*3+UP*1.6)
        out=txt('y',40,PINK).move_to(RIGHT*3+UP*1.6)
        forwards=VGroup(Arrow(inp.get_right(),box.get_left(),buff=.15,color=MUTED,stroke_width=3),Arrow(box.get_right(),out.get_left(),buff=.15,color=MUTED,stroke_width=3))
        ftext=txt('순전파: y = σ(x)',28,MINT).move_to(UP*2.9)
        self.play(FadeIn(block),FadeIn(inp),FadeIn(out),Create(forwards),FadeIn(ftext),run_time=.8)
        self.cue(7)
        loss=txt('손실 L',27,MUTED).move_to(RIGHT*2.8+DOWN*.2)
        back=Arrow(RIGHT*3+DOWN*1.15,LEFT*3+DOWN*1.15,buff=0,color=GOLD,stroke_width=4)
        backlabel=txt('역전파: 손실의 기울기',28,GOLD).move_to(DOWN*2)
        self.play(FadeIn(loss),GrowArrow(back),FadeIn(backlabel),run_time=1)
        self.cue(8)
        chain=txt('∂L/∂x = ∂L/∂y × σ′(x)',33,GOLD).move_to(DOWN*3.4)
        incoming=txt('∂L/∂y',25,PINK).move_to(RIGHT*2.7+DOWN*.55)
        outgoing=txt('∂L/∂x',25,BLUE).move_to(LEFT*2.7+DOWN*.55)
        factor=txt('× σ′(x)',28,GOLD).move_to(DOWN*.55)
        self.play(FadeIn(chain),FadeOut(loss),FadeIn(incoming),FadeIn(outgoing),FadeIn(factor),run_time=.8)
        pulse=Dot(RIGHT*3+DOWN*1.15,radius=.13,color=PINK)
        self.play(FadeIn(pulse),run_time=.3)
        self.play(pulse.animate.move_to(DOWN*1.15),run_time=1)
        self.play(pulse.animate.scale(.35).move_to(LEFT*3+DOWN*1.15),run_time=1)
        self.play(FadeOut(pulse),run_time=.3)
        self.cue(9)
        self.play(Transform(headline,txt('x = 5: σ′(5) ≈ 0.00665',30,GOLD).move_to(headline)),
                  Transform(incoming,txt('1',32,PINK).move_to(incoming)),
                  Transform(outgoing,txt('0.00665',28,BLUE).move_to(outgoing)),
                  Transform(factor,txt('× 0.00665',27,GOLD).move_to(factor)),
                  Transform(chain,txt('1 × 0.00665 ≈ 0.00665',32,GOLD).move_to(chain)),run_time=.8)
        note=txt('예: 출력 쪽 손실 기울기가 1일 때',22,MUTED).move_to(DOWN*4.25)
        self.play(FadeIn(note),run_time=.5)
        self.cue(10)
        self.play(FadeOut(block),FadeOut(inp),FadeOut(out),FadeOut(forwards),FadeOut(ftext),FadeOut(back),FadeOut(backlabel),
                  FadeOut(incoming),FadeOut(outgoing),FadeOut(factor),FadeOut(chain),FadeOut(note),run_time=.7)
        upper=VGroup(txt('순전파',25,MINT),txt('작은 입력 차이 → 더 작은 출력 차이',29,INK),txt('Δy ≈ σ′(x) · Δx',31,MINT)).arrange(DOWN,buff=.35).move_to(UP*1.4)
        lower=VGroup(txt('역전파',25,GOLD),txt('출력 쪽 기울기 → 입력 쪽 기울기',29,INK),txt('∂L/∂x = σ′(x) · ∂L/∂y',31,GOLD)).arrange(DOWN,buff=.35).move_to(DOWN*1.4)
        self.play(FadeIn(upper),Transform(headline,txt('같은 작은 미분계수가 곱해집니다',28,MINT).move_to(headline)),run_time=.8)
        self.cue(11)
        self.play(FadeIn(lower),run_time=.8)
        self.cue(12)
        self.play(FadeOut(upper),FadeOut(lower),run_time=.6)
        ending=VGroup(txt('포화',38,MINT),txt('↓',36,MUTED),txt('작은 Sigmoid 미분계수',30,GOLD),txt('↓',36,MUTED),txt('약해질 수 있는 학습 신호',30,PINK)).arrange(DOWN,buff=.28).move_to(UP*.1)
        keyword=txt('Vanishing Gradient',38,PINK).move_to(DOWN*3.6)
        self.play(FadeIn(ending),FadeIn(keyword),run_time=.8)
        self.cue(13)
        self.play(FadeOut(ending),Transform(keyword,txt('작은 값이 계속 곱해진다면?',33,PINK).move_to(DOWN*2.7)),
                  Transform(headline,txt('다음: 여러 층을 거슬러 올라가면',28,MINT).move_to(headline)),run_time=.7)
        product=txt('… × σ′(x₃) × σ′(x₂) × σ′(x₁)',30,GOLD).move_to(UP*.8)
        scope=txt('역전파에는 가중치 등 다른 미분값도 곱해집니다',21,MUTED).move_to(DOWN*.6)
        self.play(FadeIn(product),FadeIn(scope),run_time=.8)
        self.until(DURATION)
