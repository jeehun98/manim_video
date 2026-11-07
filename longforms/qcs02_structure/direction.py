"""EP.02: exact 161-second narrative using EP.01's layout, captions and quantum diagrams."""
import json
from pathlib import Path
from math import gcd
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import (QCSScene,label,tile,grid,grover_states,text,p,
    L,PORTRAIT,BLUE,PURPLE,GREEN,ORANGE,INK,MUTED)
from .physics_model import (modular_sequence,multiplicative_order,factors_from_period,
                           periodic_input_state,qft_example,toy_period_candidate)

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))

def sequence_cards():
    cards=VGroup()
    for x,value in enumerate(modular_sequence()):
        c=VGroup(tile(str(value),PURPLE,1.22,.8),text(f'x={x}',size=18,color=MUTED).move_to([0,.65,0]))
        cards.add(c)
    cards.arrange_in_grid(cols=4 if PORTRAIT else 8,buff=(.18,.5)).move_to(p(0,0))
    return cards

class FourierBars(VGroup):
    def __init__(self,state):
        super().__init__();state=np.asarray(state);assert np.isclose(np.vdot(state,state),1)
        self.state=state;self.xs=np.linspace(-3.2,3.2,len(state));self.rects=[]
        self.add(Line(p(-3.65,-1),p(3.65,-1),color=MUTED,stroke_width=1.3))
        for k,(x,a) in enumerate(zip(self.xs,state)):
            amp=float(abs(a));prob=amp**2;h=max(amp*3,.006);color=PURPLE if amp else MUTED
            bar=Rectangle(width=.53,height=L.y(h),stroke_width=0,fill_color=color,fill_opacity=.9).move_to(p(x,-1+h/2))
            self.rects.append(bar)
            self.add(bar,label(f'{amp:.3g}',x,-1+h+.2,18,color,width=.8),
                     label(str(k),x,-1.55,20,BLUE,width=.7),label(f'{prob*100:g}%',x,-2.2,17,MUTED,width=.8))

def comparison_panels(detailed=False):
    groups=VGroup()
    centers=[p(0,1.55),p(0,-1.55)] if PORTRAIT else [p(-3.65,0),p(3.65,0)]
    width,height=(6.8,2.35) if PORTRAIT else (6.3,3.2)
    for i,(title,c,center) in enumerate(zip(['GROVER','SHOR'],[BLUE,GREEN],centers)):
        panel=RoundedRectangle(width=width,height=height,corner_radius=.12,color=c,stroke_width=1.5,fill_color=c,fill_opacity=.05)
        top=text(title,y=.78 if PORTRAIT else 1.1,size=28,color=c)
        middle=text('비구조적 검색' if i==0 else '주기 구조를 이용한 인수분해',size=26,color=INK,width=width-.4)
        bottom=text(('Θ(√N) 오라클 질의' if i==0 else '입력 비트 수의 다항시간') if detailed else '중첩 + 간섭',
                    y=-.78 if PORTRAIT else -1.1,size=24,color=c,width=width-.4)
        groups.add(VGroup(panel,top,middle,bottom).move_to(center))
    return groups

class EpisodeTwoScene(QCSScene):
    data=DATA

    def s01(self):
        chart=self.chart();self.add(chart)
        self.phase_flip(chart,1)
        mean=chart.mean_line();self.show(mean,run_time=.4)
        chart.set_state(grover_states(4,3,1)[2]);self.play(FadeOut(mean),run_time=.3)
        self.to(3.2);self.show(label('O(N) → O(√N)',y=3.7,size=38,color=GREEN))
        self.note('비구조적 검색 · 오라클 조회 횟수')

    def s02(self):
        rng=np.random.default_rng(42)
        dots=VGroup(*[Dot(p(*rng.uniform([-3,-1.5],[3,1.5])),radius=.055,color=PURPLE) for _ in range(25)])
        self.show(dots)
        self.show(label('모든 문제에서\n더 빠를 수 있을까?',y=.1,size=43))
        self.play(dots.animate.set_opacity(.18),run_time=.5)

    def s03(self):
        centers=[p(0,1.65),p(0,-1.65)] if PORTRAIT else [p(-3.8,0),p(3.8,0)]
        grids=[]
        for center,name,c in zip(centers,['고전 검색','그로버 검색'],[BLUE,PURPLE]):
            g=grid(64,8,.34,False).move_to(center);grids.append(g)
            self.show(g,text(name,size=25,color=c).next_to(g,UP,buff=.25))
        self.to(15)
        for i in range(12):self.play(grids[0][i][0].animate.set_fill(BLUE,.6),run_time=.2)
        self.note('고전: 최악 O(N) 조회')
        self.to(22)
        states=grover_states(64,63,6)
        for k in range(1,7):self.play(*self.mark_grid(grids[1],states[2*k]**2),run_time=.5)
        self.note('양자: O(√N) · 오라클 + 확산')

    def s04(self):
        f=label('O(√N)보다 더 빠르게?',y=1.9,size=40,color=PURPLE);self.show(f)
        guess=label('O(log N)  ?',y=-.5,size=38,color=MUTED);self.show(guess)
        self.to(32);self.play(Create(Cross(guess,stroke_color=ORANGE,stroke_width=4)),run_time=.6)
        self.replace(f,'Q(N) = Ω(√N)',ORANGE,48)
        self.note('비구조적 오라클 검색 · 정답 1개 · 성공률 ≥ 2/3')
        self.to(41);self.show(label('이 검색 모델에서는\n제곱근 수준의 가속이 한계',y=-2.3,size=29,color=ORANGE))

    def s05(self):
        f=label('다른 문제에는 다른 접근',y=2.8,size=33,color=PURPLE);self.show(f)
        value=label('15',size=72,color=INK);self.show(value)
        self.to(52);self.replace(f,'SHOR’S ALGORITHM',GREEN,34)
        self.to(55);self.replace(value,'15 = 3 × 5',GREEN,58)
        self.note('큰 정수를 소인수로 분해하는 문제')

    def s06(self):
        trial=label('2, 3, 4, 5, …\n약수 후보를 직접 확인',y=1.7,size=29,color=BLUE)
        periodic=label('f(x) = 2ˣ mod 15',y=-.7,size=40,color=PURPLE)
        self.show(trial);self.show(periodic)
        self.play(trial.animate.set_opacity(.3),Indicate(periodic,color=GREEN),run_time=.6)
        self.note('시행 나눗셈은 단순한 고전 방법의 예')

    def s07(self):
        self.show(label('f(x) = 2ˣ mod 15',y=3.7,size=37,color=PURPLE))
        cards=sequence_cards();self.to(69)
        for c in cards:self.show(c,run_time=.45)
        self.show(label('2⁴ = 16  →  16 mod 15 = 1',y=-2.8,size=29,color=GREEN))

    def s08(self):
        r=multiplicative_order(2,15)
        cards=sequence_cards();self.add(cards)
        boxes=VGroup(SurroundingRectangle(VGroup(*cards[:4]),buff=.12,color=GREEN),SurroundingRectangle(VGroup(*cards[4:]),buff=.12,color=GREEN))
        self.show(boxes,run_time=.4)
        self.show(label(f'r = {r}',y=3.7,size=43,color=GREEN),label(f'f(x + {r}) = f(x)',y=-2.8,size=31,color=GREEN),run_time=.4)

    def s09(self):
        f=label('2⁴ mod 15 = 1',y=1.8,size=44,color=PURPLE);self.show(f)
        self.to(80);self.show(label('2⁴ − 1 = 15',y=-.5,size=52,color=GREEN))
        self.note('이 예에서는 15 · 일반적으로는 원래 정수의 배수')

    def s10(self):
        f=label('2⁴ − 1',size=55,color=PURPLE);self.show(f)
        self.to(85.5);self.replace(f,'(2²)² − 1²',PURPLE,49)
        self.to(87.5);self.replace(f,'(2² − 1)(2² + 1)',PURPLE,43)
        self.to(88.6)
        parts=VGroup(label('(2² − 1)',size=39,color=BLUE),label('×',size=32),label('(2² + 1)',size=39,color=GREEN)).arrange(RIGHT,buff=.25)
        self.play(Transform(f,parts),run_time=.6)

    def s11(self):
        a,b=factors_from_period(2,15,multiplicative_order(2,15))
        self.show(label(f'2² − 1 = {a}',-1.95,1.7,34,BLUE,width=3.6),label(f'2² + 1 = {b}',1.95,1.7,34,GREEN,width=3.6))
        self.to(93);self.show(label(f'15 = {a} × {b}',y=-.3,size=55,color=GREEN))
        self.to(95);self.show(label(f'gcd({a},15) = {a} · gcd({b},15) = {b}',y=-2.2,size=24,color=MUTED))
        self.note('짝수 주기 등 조건 필요 · 일반적으로 gcd 계산')

    def s12(self):
        self.show(label('15 = ? × ?',y=2.2,size=43,color=BLUE))
        self.show(label('↓',y=.7,size=35,color=MUTED),label('2ˣ mod 15의 주기는?',y=-.4,size=37,color=PURPLE))
        self.show(label('r = ?',y=-2.2,size=46,color=GREEN))

    def s13(self):
        cards=sequence_cards();self.add(cards)
        self.play(*[Transform(cards[i],cards[i].copy().fade(.85)) for i in range(8) if i not in [0,4]],
                  cards[0][0][0].animate.set_stroke(GREEN,width=3),cards[4][0][0].animate.set_stroke(GREEN,width=3),run_time=.4)
        self.show(label('f(x) = 1인 입력 위치: 0, 4',y=3.7,size=29,color=GREEN),
                  label('|ψ⟩ = (|0⟩ + |4⟩)/√2',y=-2.8,size=31,color=PURPLE),run_time=.4)

    def s14(self):
        initial,result=qft_example();chart=FourierBars(initial);self.add(chart)
        stage=label('입력 레지스터의 주기적 진폭',y=3.7,size=29,color=PURPLE);self.show(stage,run_time=.4)
        self.note('Q = 8 단순 예시 · 막대: 진폭 크기 · 아래: 확률')
        self.to(107.5);self.play(FadeOut(chart),run_time=.3)
        chart=FourierBars(result);self.show(chart,run_time=.4)
        self.replace(stage,'QFT → 짝수 인덱스 0, 2, 4, 6',GREEN,29)
        self.to(109);self.note('반복 간격 4 → 주파수 인덱스 간격 2')

    def s15(self):
        candidate=toy_period_candidate(2)
        chart=FourierBars(qft_example()[1]);self.add(chart)
        self.play(Indicate(chart.rects[2],color=GREEN),run_time=.6)
        self.play(FadeOut(chart),run_time=.4)
        self.show(label('측정 예: k = 2  (확률 25%)',y=3.7,size=29,color=GREEN))
        self.show(label('2/8 = 1/4',y=.8,size=58,color=PURPLE))
        self.to(116);self.show(label(f'후보 r = {candidate}',y=-1,size=43,color=GREEN),label('검증: 2⁴ mod 15 = 1',y=-2.6,size=27,color=BLUE))
        self.note('선택된 성공 예 · 후보 검증·반복 측정이 필요할 수 있음')

    def s16(self):
        self.show(label('입력 비트 수에 대해 다항시간',y=3.7,size=28,color=GREEN))
        names=[('주기 찾기',PURPLE),('QFT·측정',PURPLE),('고전 후처리',BLUE),('인수 3, 5',GREEN)]
        flow=VGroup()
        for i,(name,c) in enumerate(names):
            if i:flow.add(text('↓' if PORTRAIT else '→',size=25,color=MUTED))
            flow.add(tile(name,c,6.2 if PORTRAIT else 2.5,.63))
        flow.arrange(DOWN if PORTRAIT else RIGHT,buff=.18).move_to(p(0,-.2))
        self.show(flow);self.note('알려진 고전 알고리즘 대비 · 장치 실행시간과 구별')

    def s17(self):
        panels=comparison_panels();self.show(panels)
        self.show(label('공통 원리: 중첩과 간섭',y=3.7,size=29,color=PURPLE))
        self.note('검색과 소인수분해는 서로 다른 문제')

    def s18(self):
        panels=comparison_panels(True);self.add(panels)
        original=panels.copy()
        self.play(Transform(panels[1],original[1].copy().fade(.7)),run_time=.4)
        self.note('검색 후보 수 N과 정수의 입력 비트 수는 다른 척도')
        self.to(135);self.play(Transform(panels[0],original[0].copy().fade(.7)),Transform(panels[1],original[1]),run_time=.5)
        self.note('고전 소인수분해의 난도가 증명된 것은 아님')

    def s19(self):
        self.show(label('중첩의 개수만으로는\n속도를 결정할 수 없다',y=2.8,size=35,color=ORANGE))
        rng=np.random.default_rng(17)
        cloud=VGroup(*[Dot(p(*rng.uniform([-3,-1.5],[3,1])),radius=.05,color=PURPLE) for _ in range(64)])
        self.show(cloud)
        self.to(149);self.play(FadeOut(cloud),run_time=.4)
        cards=sequence_cards();self.show(cards)
        self.show(label('수학적 구조 + 효율적인 활용',y=-2.8,size=32,color=GREEN))

    def s20(self):
        rng=np.random.default_rng(161)
        bits=VGroup(*[tile(str(int(v)),PURPLE,.6,.45) for v in rng.integers(0,2,48)])
        bits.arrange_in_grid(cols=8,buff=.1).set_opacity(.16);self.add(bits)
        self.show(label('무작위 입력에서도\n지수적인 가속이 가능할까?',y=.2,size=40,color=INK))
        self.play(bits.animate.shift(RIGHT*.12),run_time=2,rate_func=there_and_back)
