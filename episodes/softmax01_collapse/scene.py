"""106-second standalone portrait short. User supplied sentence endpoints."""
import json, os, sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import configure_vertical, FONT
configure_vertical()
config.background_color='#080F20'
ROOT=Path(__file__).resolve().parent
CYAN='#39DACD'; RED='#FF657A'; GREEN='#B6ED79'; WHITE='#F0F4FF'; GRAY='#8795AE'; GOLD='#FFD078'

def tx(s,y=0,size=32,c=WHITE,x=0,w=7.5):
    m=Text(s,font=FONT,font_size=size,color=c,line_spacing=1.2)
    if m.width>w:m.scale_to_fit_width(w)
    return m.move_to([x,y,0])

def network(y=0):
    layers=[[Dot([x,v+y,0],radius=.12,color=CYAN) for v in vals] for x,vals in [(-2.7,[-1.4,0,1.4]),(-.9,[-2,-.7,.7,2]),(.9,[-1.4,0,1.4]),(2.7,[0])]]
    edges=VGroup(*[Line(a.get_center(),b.get_center(),color=CYAN,stroke_width=1.3,stroke_opacity=.28) for l,r in zip(layers,layers[1:]) for a in l for b in r])
    return VGroup(edges,*[VGroup(*l) for l in layers])

def bars(p):
    g=VGroup(Line([-3,-2,0],[3,-2,0],color=GRAY))
    for k,v in enumerate([p,*[(1-p)/3]*3]):
        h=max(.035,4*v);x=-2.4+1.6*k
        g.add(Rectangle(width=.78,height=h,color=CYAN if k==0 else GRAY,fill_opacity=.85).move_to([x,-2+h/2,0]),tx('정답' if k==0 else str(k+1),-2.5,21,CYAN if k==0 else GRAY,x=x,w=1.2))
    return g

def card(label,formula,y,c):
    return VGroup(RoundedRectangle(width=7.1,height=2.15,corner_radius=.16,color=c,fill_color='#111D32',fill_opacity=1).move_to([0,y,0]),tx(label,y+.62,24,c),tx(formula,y-.25,38,c))

TITLES=['똑똑해질수록 위험해지는 계산','Softmax','2026.10 · 계산 방식의 결함','정답일 확률','학습이 진행되면','더 높은 확신','거의 100%, 그러나 아직','여기서 문제가 발생합니다','컴퓨터의 정밀도는 유한합니다','서로 다른 값이 하나로','왜 문제가 될까요?','기울기가 학습 방향을 알려줍니다','정답 로짓에 대한 기울기','작아져도, 0은 아닙니다','반올림이 지워버린 차이','정답 클래스의 학습 신호 소실','Softmax Collapse','계산 경로를 바꾸면?','확률의 합은 1','작은 확률을 직접 합산','수학적으로 같은 계산','같은 수학, 다른 계산 결과','반복되는 손실 급등','개선 계산에서는 급등 제거','신경망 구조는 그대로','바뀐 것은 계산 방식','작은 차이를 지키는 계산']
ENDS=[3,5,13,17,20,22,25,29,32,36,37,41,47,52,57,60,64,66,70,76,79,86,90,93,96,101,106]

class SoftmaxCollapse(Scene):
    def panel(self,i):
        if i==0:return VGroup(network(),tx('정답 확률 ↑',3,38,CYAN),tx('수치적 결함',-3.3,38,RED))
        if i==1:return VGroup(tx('Softmax',1.5,68,CYAN),tx('pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)',-.4,32),bars(.75).scale(.65).shift(DOWN*2))
        if i==2:return VGroup(RoundedRectangle(width=7.1,height=2.8,corner_radius=.16,color=CYAN).move_to([0,2,0]),tx('RESEARCH · 22 OCT 2026',2.95,24,CYAN),tx('A Fix for Softmax',2.1,36,CYAN),tx('and Cross-Entropy',1.15,30),tx('Barron · Gnanapragasam · Tschannen',-.3,23,GRAY),tx('Google DeepMind',-1.2,29),tx('arXiv:2610.31642',-2.3,26,CYAN),tx('Softmax  +  Cross-Entropy',-3.4,32,GOLD))
        if 3<=i<=7:
            v=['90%','99%','99.9%','99.999999%','99.999999%'][i-3]
            return VGroup(tx(v,3.3,56,RED if i==7 else CYAN),bars([.9,.99,.999,.99999999,.99999999][i-3]),tx('정답 클래스의 예측 확률',-3.6,25,GRAY))
        if i in [8,9,10]:
            g=VGroup(tx('FP32 · 32-bit floating point',3.3,25,GRAY),Line([-3,0,0],[3,0,0],color=GRAY),*[Line([x,-.16,0],[x,.16,0],color=WHITE) for x in [-3,-1,1,3]],tx('0.9999999404',-.65,21,GRAY,x=-1.8,w=3),tx('1.0',-.65,26,RED,x=3,w=1),tx('1 근처의 표현 가능한 이진수 눈금',-2.9,23,GRAY))
            if i>=9:g.add(tx('0.99999999  →  1.0',2,38,RED),tx('FP32로 반올림',-1.9,29,RED))
            else:g.add(tx('모든 실수를 담을 수는 없다',2,34,CYAN))
            if i==10:g.add(tx('?',-4,58,GOLD))
            return g
        if i==11:
            a=Axes(x_range=[-3,3,1],y_range=[0,5,1],x_length=6.3,y_length=4,tips=False).shift(DOWN)
            return VGroup(a,a.plot(lambda x:.45*x*x+.2,color=CYAN),Dot(a.c2p(2,2),color=GOLD),Arrow(a.c2p(2,2),a.c2p(1, .65),color=GOLD,buff=.1),tx('손실 L',3.5,32),tx('Gradient → 손실이 줄어드는 방향',-3.6,27,CYAN))
        if i==12:return VGroup(tx('∂L / ∂zₜ',2.3,50,CYAN),tx('=',.8,42),tx('pₜ − 1',-.8,72,GOLD),tx('pₜ : 정답 확률    zₜ : 정답 로짓',-3,25,GRAY),tx('one-hot 정답 · 유한한 로짓',-4,22,GRAY))
        if i==13:return VGroup(tx('−0.1',2.7,50,CYAN),tx('↓',1.5,35,GRAY),tx('−0.01',.4,50,CYAN),tx('↓',-.8,35,GRAY),tx('−0.00000001',-2,47,CYAN),tx('여전히 0보다 작다',-3.8,29,GOLD))
        if i==16:return VGroup(tx('SOFTMAX',2.7,58,RED),tx('COLLAPSE',1.3,58,RED),card('컴퓨터가 계산한 정답 기울기','gₜ = 0',-1.3,RED),tx('다른 클래스의 기울기는 남을 수 있음',-3.7,24,GRAY))
        if i in [14,15]:return VGroup(card('수학적 계산','0.99999999 − 1 = −10⁻⁸',2,CYAN),card('FP32 계산','1.0 − 1.0 = 0',-1,RED),tx('정답 성분만 0 · 다른 성분은 남을 수 있음',-3.3,22,GRAY),tx('Computed target gradient = 0',-4.2,27,RED))
        if i==17:return VGroup(tx('pₜ − 1',2,65,RED),tx('↓',.5,50,GRAY),tx('다른 계산 경로',-1.2,43,GREEN),tx('작은 값을 처음부터 지킨다',-3,30,GREEN))
        if i==18:return VGroup(bars(.9),tx('pₜ + Σⱼ≠ₜ pⱼ = 1',3.4,43,GREEN),tx('정답 확률 + 나머지 확률 = 전체',-3.7,27,GRAY))
        if i==19:return VGroup(tx('나머지 클래스의 작은 확률',3.6,29,GREEN),*[card(f'클래스 {k+2}',v,y,GREEN).scale(.72).move_to([0,y,0]) for k,(v,y) in enumerate([('2 × 10⁻⁹',2),('3 × 10⁻⁹',.2),('5 × 10⁻⁹',-1.6)])],tx('−(2 + 3 + 5) × 10⁻⁹ = −10⁻⁸',-3.5,31,GREEN),tx('로짓 차이의 작은 지수항부터 안정적으로 계산',-4.4,21,GRAY))
        if i==20:return VGroup(tx('pₜ − 1',2.1,62,RED),tx('=',.5,56,GOLD),tx('−Σⱼ≠ₜ pⱼ',-1.3,62,GREEN),tx('실수의 수학에서 완전히 동치',-3.5,29,GRAY))
        if i==21:return VGroup(card('기존 경로 · 정보 손실','pₜ − 1  →  0',2,RED),card('개선 경로 · 정보 보존','−Σⱼ≠ₜ pⱼ  →  −10⁻⁸',-1.1,GREEN),tx('이미 1로 반올림된 pₜ를 재사용하지 않는다',-3.6,22,GRAY),tx('표현 가능한 작은 값의 정밀도 보존',-4.4,23,GREEN))
        if i in [22,23]:
            a=Axes(x_range=[0,10,2],y_range=[0,1.5,.5],x_length=6.5,y_length=4,tips=False).move_to([0,.3,0])
            fn=lambda x:.15+.6*np.exp(-x*.6)+sum(.9*np.exp(-((x-t)/.14)**2) for t in [3.4,6,8.6])
            g=VGroup(a,a.plot(fn,x_range=[0,10,.035],color=RED,stroke_width=3),tx('훈련 손실',3.2,27,GRAY),tx('학습 단계 →',-2.3,25,GRAY),tx('개념도 · 논문 실험 수치 아님',-4,24,GRAY),tx('실험 조건에서 관찰한 현상',-4.7,21,GRAY))
            if i==23:g.add(a.plot(lambda x:.15+.6*np.exp(-x*.6),color=GREEN,stroke_width=5),tx('기존 계산',-3.1,25,RED,x=-1.8,w=3),tx('개선 계산',-3.1,25,GREEN,x=1.8,w=3))
            else:g.add(tx('Slingshot · 반복되는 급등',-3.1,29,RED))
            return g
        if i in [24,25]:return VGroup(network(1),tx('동일한 신경망 구조',3.8,35,CYAN),card('계산 블록','pₜ − 1' if i==24 else '−Σⱼ≠ₜ pⱼ',-2.5,RED if i==24 else GREEN))
        return VGroup(tx('1.00000000',2.8,52,GRAY),tx('↓  작은 차이를 보존',1.1,30,GREEN),tx('0.99999999',-.4,52,GREEN),tx('같은 수학',-2.5,42),tx('≠ 같은 컴퓨터 계산',-3.6,39,GREEN))

    def construct(self):
        segments=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['segments']
        for i,end in enumerate(ENDS):
            self.clear()
            start=0 if i==0 else ENDS[i-1]
            s=next(s for s in segments if s['start']<=start<s['end'])
            caption=s['caption']
            self.add(tx('NUMERICAL PRECISION',7.35,20,GRAY),tx('Softmax의 치명적인 결함',6.5,35),Line([-3.7,5.75,0],[3.7,5.75,0],color=GRAY,stroke_opacity=.35),tx(TITLES[i],5.2,27,GREEN if i>=17 else CYAN),tx(caption,-6.1,25),tx('Barron et al. · 2026  |  arXiv:2610.31642',-7.35,17,GRAY))
            p=self.panel(i)
            self.play(FadeIn(p,shift=UP*.1),run_time=.3)
            if i in [0,24,25]:self.play(LaggedStart(*[Indicate(layer,color=GREEN) for layer in p[0][1:]],lag_ratio=.12),run_time=1.2)
            if i==9:
                dot=Dot([1.7,.25,0],color=GOLD);self.add(dot);self.play(dot.animate.move_to([3,.25,0]).set_color(RED),run_time=1.2)
            if i==19:
                self.play(*[Indicate(p[k],color=GREEN) for k in [1,2,3]],run_time=1.5)
            if i in [14,21]:self.play(Indicate(p[1],color=RED if i==14 else GREEN),run_time=1.2)
            remaining=end-self.time
            if remaining<-.04:raise RuntimeError(f'Cut {i+1} overruns: {self.time} > {end}')
            self.wait(max(0,remaining))
        assert abs(self.time-106)<.04
