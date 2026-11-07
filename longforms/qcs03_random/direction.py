"""EP.03: shared exact timing/captions; native layouts for prediction and query models."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,label,tile,text,p,L,PORTRAIT,BLUE,PURPLE,GREEN,ORANGE,INK,MUTED
from .physics_model import random_bits,growth,EXACT,ESTIMATE,ERROR

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))

def bit_grid(seed=2008,hidden=False):
    values=random_bits(seed);size=.59 if PORTRAIT else .43
    g=VGroup(*[tile('?' if hidden else str(v),ORANGE if hidden else BLUE,size,size*.78) for v in values])
    g.arrange_in_grid(cols=8,buff=.065).move_to(p(0,.7))
    return g

def box(s,color=PURPLE,w=4.1,h=1.25):return tile(s,color,w,h)

def probability(value,y=0,color=PURPLE,name='YES'):
    assert 0<=value<=1
    bg=Rectangle(width=6,height=.32,stroke_width=0,fill_color=MUTED,fill_opacity=.18).move_to(p(0,y))
    bar=Rectangle(width=6*value,height=.32,stroke_width=0,fill_color=color,fill_opacity=.9).move_to(p(-3+3*value,y))
    return VGroup(bg,bar,label(f'{name}  {value:.0%}',y=y+.75,size=36,color=color),
                  label(f'NO  {1-value:.0%}' if name=='YES' else '',y=y-.65,size=24,color=MUTED))

def gates():
    g=VGroup(*[box(s,PURPLE,.95,.65) for s in ['H','Uₓ','R','Uₓ','H']])
    g.arrange(RIGHT,buff=.22).move_to(p(0,.8))
    return g

class EpisodeThreeScene(QCSScene):
    data=DATA

    def s01(self):
        g=VGroup(*[tile(str(v),BLUE,.72,.65) for v in [1,2,4,8,1,2,4,8]])
        g.arrange_in_grid(cols=4 if PORTRAIT else 8,buff=.15).move_to(p(0,.8))
        self.show(g);a=SurroundingRectangle(VGroup(*g[:4]),color=BLUE,buff=.12)
        self.play(Create(a),run_time=.6);self.to(6)
        b=SurroundingRectangle(VGroup(*g[4:]),color=GREEN,buff=.12)
        self.play(Create(b),run_time=.6);self.show(label('주기 r = 4',y=-1.4,size=40,color=GREEN))
        self.note('쇼어 알고리즘 · 반복되는 구조의 활용')

    def s02(self):
        g=bit_grid();self.show(g)
        self.play(g.animate.set_opacity(.35),run_time=.6)
        self.show(label('규칙을 활용할 수 없다면?',y=.4,size=38))
        self.note('독립적으로 선택한 0과 1 · 균등 무작위 입력')

    def s03(self):
        self.show(label('2008',y=1.5,size=88,color=BLUE))
        self.show(label('Scott Aaronson\nAndris Ambainis',y=-.5,size=33,color=PURPLE))
        self.show(label('낮은 차수의 다항식에 관한 추측',y=-2.5,size=27))
        self.note('추측 제안 2008 · 원논문 2009 / 저널판 2014')

    def s04(self):
        g=bit_grid();self.play(LaggedStart(*[FadeIn(g[i:i+8]) for i in range(0,64,8)],lag_ratio=.08),run_time=1.4)
        self.show(label('x = (x₁, x₂, …, xₙ)',y=-2.6,size=32,color=BLUE))
        self.note('격자 전체가 하나의 입력 x')

    def s05(self):
        g=bit_grid();self.add(g)
        for i in [5,19,42]:
            cursor=SurroundingRectangle(g[i],color=BLUE,buff=.04)
            self.play(Create(cursor),run_time=.3)
            self.play(Indicate(g[i],color=INK),run_time=.4);self.remove(cursor)
        self.show(label('i → xᵢ',y=-2.6,size=40,color=BLUE))
        self.note('특정 위치를 선택해 비트 하나를 읽는다')

    def s06(self):
        g=bit_grid().scale(.78).move_to(p(0,1.65));self.add(g)
        chosen=[2,7,17,28,39,48,56]
        self.play(*[g[i][0].animate.set_stroke(PURPLE,3).set_fill(PURPLE,.24) for i in chosen],run_time=.7)
        f=label('Σᵢ αᵢ |i⟩|0⟩',y=-1,size=36,color=PURPLE);self.show(f)
        self.to(36);self.replace(f,'Σᵢ αᵢ |i⟩|xᵢ⟩',PURPLE,36)
        self.show(label('Uₓ |i,b⟩ = |i, b ⊕ xᵢ⟩',y=-2.65,size=27,color=PURPLE))
        self.note('하나의 중첩 상태 · 모든 비트를 따로 읽은 결과가 아님')

    def s07(self):
        g=bit_grid();self.add(g)
        for seed in [2026,2027]:
            new=bit_grid(seed);self.play(Transform(g,new),run_time=.7)
        self.to(44);self.play(g.animate.set_opacity(.26),run_time=.4)
        self.show(label('무작위 입력에서도\n지수적인 조회 가속?',y=.6,size=40))
        self.note('무작위라는 이유만으로 모든 계산 성질이 사라지는 것은 아님')

    def s08(self):
        g=gates();self.show(g)
        q=label('계산의 조회 횟수는?',y=-1.2,size=34,color=PURPLE);self.show(q)
        self.to(56)
        target=box('양자 알고리즘',PURPLE).move_to(p(0,1.5))
        self.play(Transform(g,target),FadeOut(q),run_time=.8)
        self.show(label('입력 x → 출력 확률 p(x)',y=-.5,size=35,color=GREEN))
        self.show(label('고전 조회로 예측할 수 있을까?',y=-2.2,size=32,color=BLUE))
        self.note('회로 내부에서 입력과 출력의 관계로 관점 이동')

    def s09(self):
        centers=[p(0,2.7),p(0,.7),p(0,-1.5)] if PORTRAIT else [p(-4.6,.5),p(0,.5),p(4.6,.5)]
        nodes=[box('입력 x',BLUE,2.6,1.1),box('양자 알고리즘',PURPLE,3.4,1.1),VGroup(box('YES',GREEN,1.5,.75),box('NO',ORANGE,1.5,.75)).arrange(DOWN,buff=.25)]
        for o,c in zip(nodes,centers):o.move_to(c);self.show(o)
        for a,b in zip(nodes,nodes[1:]):self.play(GrowArrow(Arrow(a.get_bottom() if PORTRAIT else a.get_right(),b.get_top() if PORTRAIT else b.get_left(),buff=.15,color=MUTED)),run_time=.4)
        self.note('YES / NO는 가능한 출력 · 한 실행에서 결과 하나를 관측')

    def s10(self):
        g=VGroup(*[tile(str(v),BLUE,.55,.55) for v in random_bits()[:8]]).arrange(RIGHT,buff=.08).move_to(p(0,2.5))
        a=label('입력 A',y=3.55,size=27,color=BLUE);bars=probability(.7,y=-.2)
        self.show(a,g,bars);self.to(76)
        j=2;v=1-int(random_bits()[j]);self.play(Transform(g[j],tile(str(v),ORANGE,.55,.55).move_to(g[j])),Transform(a,label('입력 B',y=3.55,size=27,color=ORANGE)),Transform(bars,probability(.4,y=-.2)),run_time=1)
        self.note('개념 예시 · 특정 회로를 계산한 수치가 아님')

    def s11(self):
        g=bit_grid(hidden=True);self.show(g)
        for i in [3,17,29,46]:
            self.play(Transform(g[i],tile(str(random_bits()[i]),BLUE,g[i][0].width,g[i][0].height).move_to(g[i])),run_time=.3)
        self.show(label('p(x)를 예측할 수 있을까?',y=-2.7,size=33,color=GREEN))
        self.note('확인하지 않은 비트는 ? · 아직 근사 성공을 가정하지 않음')

    def s12(self):
        g=gates();self.show(g)
        t=label('내부 계산 전체를 재현?',y=-1.1,size=34,color=PURPLE);self.show(t)
        self.to(91);self.play(FadeOut(g),FadeOut(t),run_time=.4)
        self.show(label('출력 확률  p(x) = 0.70',y=2.05,size=34,color=PURPLE),label('근삿값  p̃(x) = 0.68',y=.3,size=34,color=GREEN))
        self.show(label('|p(x) − p̃(x)| = 0.02',y=-1.7,size=35,color=ORANGE))
        self.note('개념 예시 · 모든 입력에 대해 오차 0.02를 보장한다는 뜻은 아님')

    def s13(self):
        centers=[p(0,2.0),p(0,-.7)] if PORTRAIT else [p(-3.7,.8),p(3.7,.8)]
        a=VGroup(box('양자 알고리즘',PURPLE),label('T번 조회',y=-1.2,size=37,color=PURPLE)).move_to(centers[0])
        b=VGroup(box('고전 근사 알고리즘',BLUE),label('poly(T)번 조회 ?',y=-1.2,size=35,color=BLUE)).move_to(centers[1])
        self.show(a);self.to(98);self.show(b)
        self.show(label('같은 입력 x의 출력 확률을 근사',y=-2.7,size=28,color=GREEN))
        self.note('근사 오차 ε와 예외 입력 비율 δ를 고정한 질문')

    def s14(self):
        ax=VGroup(Line(p(-3,-1.5),p(3.2,-1.5),color=MUTED),Line(p(-3,-1.5),p(-3,2.65),color=MUTED))
        def pos(t,v):return p(-3+t*.6,-1.5+v/1024*4)
        paths=[]
        for index,c in [(0,BLUE),(1,ORANGE)]:
            path=VMobject(color=c,stroke_width=3).set_points_as_corners([pos(t,growth(t)[index]) for t in np.linspace(0,10,101)])
            paths.append(path)
        self.add(ax,label('0',x=-3.2,y=-1.85,size=17,color=MUTED),label('10',x=3,y=-1.85,size=17,color=MUTED),label('T',x=3.5,y=-1.5,size=20,color=MUTED),label('1,024',x=-3.5,y=2.55,size=17,color=MUTED))
        self.play(*[Create(o) for o in paths],run_time=1)
        self.show(label('T²',x=-1.8,y=2.6,size=27,color=BLUE),label('2ᵀ',x=1.1,y=2.6,size=27,color=ORANGE))
        self.show(label('T = 10 : 100  /  1,024',y=-2.6,size=28))
        self.note('성장의 개념 비교 · 실제 알고리즘의 조회 수가 아님')

    def s15(self):
        cards=VGroup(*[tile(format(i,'05b'),MUTED,1.1,.62) for i in range(20)])
        cards.arrange_in_grid(cols=4 if PORTRAIT else 5,buff=.14).move_to(p(0,1.2));self.show(cards)
        self.to(113)
        self.play(*[c[0].animate.set_stroke(ORANGE if i in [5,17] else GREEN).set_fill(ORANGE if i in [5,17] else GREEN,.13) for i,c in enumerate(cards)],run_time=.7)
        self.show(label('오차 ≤ ε  인 입력 비율 ≥ 1 − δ',y=-1.75,size=28,color=GREEN))
        self.show(label('ε : 한 입력의 오차\nδ : 예외 입력의 비율',y=-2.75,size=23,color=ORANGE))
        self.note('균등 무작위 입력 · 카드 색 비율은 설명용 예시')

    def s16(self):
        self.show(label('x₁, x₂, …, xₙ',y=2.2,size=37,color=BLUE))
        self.show(label('↓',y=.8,size=40,color=MUTED))
        self.show(label('p(x₁, x₂, …, xₙ)',y=-.6,size=39,color=PURPLE))
        self.show(label('0 ≤ p(x) ≤ 1',y=-2.35,size=30,color=GREEN))
        self.note('입력은 0·1 비트 · 낮은 차수의 다항식에 관한 추측')

    def s17(self):
        a=probability(EXACT,y=2,color=PURPLE,name='양자 출력 확률');b=probability(ESTIMATE,y=-.3,color=GREEN,name='고전 근삿값')
        self.show(a);self.to(128);self.show(b)
        self.show(label('추측이 성립한다면\npoly(T, 1/ε, 1/δ) 조회',y=-2.5,size=27,color=BLUE))
        self.note('개념 예시: 0.70과 0.68 · 균등 입력 대부분에서 오차 ε 이내')

    def s18(self):
        self.show(label('T → poly(T)',y=1.9,size=48,color=GREEN))
        self.show(label('출력 확률 근사의\n지수적인 조회 차이를 제한',y=-.2,size=36))
        self.show(label('균등 무작위 입력 대부분\n고정된 근사 오차·예외 비율',y=-2.3,size=26,color=BLUE))
        self.note('추측이 성립할 때의 귀결 · 전체 실행시간에 대한 결론은 아님')

    def s19(self):
        self.show(label('2008 → 2026',y=1.4,size=50,color=PURPLE))
        self.show(label('18년 동안 남았던 질문',y=-.4,size=37))
        self.show(label('낮은 차수의 다항식\n그리고 입력 비트의 영향',y=-2.2,size=28,color=BLUE))
        self.note('추측의 제안에서 시작하는 역사적 서술')

    def s20(self):
        g=bit_grid().set_opacity(.15);self.add(g)
        f=label('출력 확률 ↔ 다항식',y=.7,size=41,color=PURPLE);self.show(f)
        self.to(149);self.play(FadeOut(f),run_time=.4)
        self.play(*[g[i].animate.set_opacity(.75) for i in [3,17,29,46]],run_time=.5)
        self.show(label('어떤 입력이\n결과에 영향을 줄까?',y=.5,size=42))
        self.note('p(x₁, x₂, …, xₙ)')
