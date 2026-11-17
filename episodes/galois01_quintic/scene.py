"""Exact-time portrait Galois explanation; reusable narration subtitle band."""
import json
import sys
from itertools import permutations
from pathlib import Path
from manim import *

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from longforms.qcs01_speed.direction import QCSScene, label

DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BG,INK,MUTED='#101923','#EDF3FC','#8B9CB7'
BLUE,GOLD,GREEN,RED='#61AEFF','#FFD275','#52E2A8','#FF747F'
config.background_color=BG

def txt(s,y=0,size=36,color=INK,x=0,width=7.5):
    return label(s,x=x,y=y,size=size,color=color,width=width)

def eq(s,y=0,size=48,color=INK,width=7.3):
    m=MathTex(s,font_size=size,color=color)
    if m.width>width:m.scale_to_fit_width(width)
    return m.move_to(UP*y)

def token(s,x,y,r=.52,size=34):
    return VGroup(Circle(radius=r,color=BLUE,fill_opacity=.13,stroke_width=3),
                  txt(s,size=size,width=2*r-.1)).move_to([x,y,0])

def roots(names,y=0,spacing=1.4):
    return VGroup(*[token(s,(i-(len(names)-1)/2)*spacing,y,r=.45,size=28) for i,s in enumerate(names)])

def box(s,y,color=GOLD,width=7.1,height=1):
    return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.16,
        stroke_color=color,fill_color=color,fill_opacity=.06),txt(s,y=0,size=30,color=color,width=width-.35)).move_to(UP*y)

class GaloisScene(QCSScene):
    data=DATA
    def setup(self):
        super().setup()
        self.remove(self.mobjects[0])
        self.title.move_to(UP*5.35)
        self.add(txt('5차 방정식  /  GALOIS THEORY',y=7,size=20,color=MUTED))
    def swap(self,a,b,run_time=1):
        self.play(Swap(a,b),run_time=run_time)
    def permute(self,group,p,run_time=.6):
        # p maps a position to its new position; tokens retain their identities.
        positions=[m.get_center().copy() for m in group]
        self.play(*[m.animate(path_arc=PI/3).move_to(positions[p[i]]) for i,m in enumerate(group)],run_time=run_time)
        return VGroup(*[group[p.index(i)] for i in range(len(p))])

class Shot01(GaloisScene):
    shot=0
    def s01(self):
        quadratic=eq(r'ax^2+bx+c=0',2.7)
        formula=eq(r'x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}',.6,44)
        self.show(quadratic,formula)
        self.to(3)
        checks=VGroup(box('2차  ·  근호 공식',-1.6,GREEN),box('3차 · 4차  ·  근호 공식',-2.9,GREEN))
        self.show(checks)
        self.to(6)
        self.play(FadeOut(VGroup(quadratic,formula,checks)))
        question=txt('5차에는 왜 없을까?',2.3,51,GOLD)
        points=roots(['α','β','γ','δ','ε'],-.2)
        self.show(question,points)
        self.to(10)
        self.swap(points[0],points[3])
        self.swap(points[1],points[4])
        self.show(txt('답은 해의 대칭에 있다',-2.7,38,GREEN))

class Shot02(GaloisScene):
    shot=1
    def s02(self):
        polynomial=eq(r'x^2-5x+6=0',3.4)
        self.show(polynomial)
        self.to(19)
        self.show(eq(r'(x-2)(x-3)=0',2.1,40))
        a,b=token('2',-1.65,.35),token('3',1.65,.35)
        self.show(a,b)
        self.to(21)
        self.show(eq(r'2+3=5',-1.3,44,GREEN),eq(r'2\times3=6',-2.45,44,GREEN))
        self.to(23)
        self.swap(a,b,1.7)
        self.show(txt('순서가 바뀌어도 합과 곱은 같다',-3.65,28,GREEN))
        self.to(28)
        self.play(Indicate(polynomial,color=GREEN))
        self.show(txt('순서 변경의 예시 · 두 유리수는 각각 고정',4.35,19,MUTED))

class Shot03(GaloisScene):
    shot=2
    def s03(self):
        row=roots(['1','2','3'],2.5)
        self.show(row,txt('숫자는 해를 구별하는 이름',3.7,23,MUTED))
        self.to(34)
        self.swap(row[1],row[2])
        self.to(37)
        self.play(FadeOut(row))
        arrangements=VGroup(*[roots([str(x) for x in p],spacing=.68).scale(.6) for p in permutations((1,2,3))])
        arrangements.arrange_in_grid(rows=3,cols=2,buff=(1.1,.4)).move_to(UP*1.6)
        self.show(arrangements,txt('3! = 6',-1.05,47,GOLD))
        self.to(39.5)
        count=txt('4! = 24',-2.2,43,GOLD)
        self.show(count)
        self.to(42)
        self.show(txt('5! = 120',-3.4,43,GOLD))
        self.to(44)
        self.play(FadeOut(VGroup(arrangements,count,*[m for m in self.mobjects if m is not self.title and m is not self.caption and m is not self.caption_panel and m.get_center()[1]<-1])))
        row=roots(['1','2','3'],1.7)
        self.show(row,txt('순열  +  순열',-.2,41,GOLD))
        row=self.permute(row,[1,0,2])
        row=self.permute(row,[1,2,0])
        self.show(txt('결과도 순열',-1.7,38,GREEN),txt('합성이라는 연산  →  군',-3.2,34,GOLD))

class Shot04(GaloisScene):
    shot=3
    def s04(self):
        self.show(box('모든 해의 순열',2.8,BLUE),txt('어떤 변환이 허용될까?',.9,36))
        self.to(54)
        self.show(Arrow(UP*1.95,UP*.05,color=GREEN),box('기준체의 대수적 관계 보존',-.6,GREEN))
        self.show(txt('계수와 유리수의 값을 고정',-1.85,26,MUTED))
        self.to(58)
        self.show(box('갈루아 군',-3.2,GOLD))

def radical_scene(scene):
    axis=NumberLine(x_range=[-2,2,1],length=6.5,color=MUTED).shift(DOWN*.25)
    a,b=token('−√2',-2.3,-.25,r=.62,size=29),token('√2',2.3,-.25,r=.62,size=32)
    return axis,a,b

class Shot05(GaloisScene):
    shot=4
    def s05(self):
        self.show(txt('근호와 대칭은 어떻게 연결될까?',2.8,36,GOLD))
        self.to(66)
        self.show(eq(r'x^2-2=0',1.7))
        self.to(69)
        axis,a,b=radical_scene(self)
        self.show(axis,a,b)
        self.to(72)
        result=eq(r'(-\sqrt2)^2=(\sqrt2)^2=2',-2,42,GREEN)
        self.show(result)
        self.to(76)
        self.swap(a,b,1.5)
        self.play(Indicate(result,color=GREEN))
        self.show(txt('유리수 계수의 관계를 보존',-3.5,29,GREEN))

class Shot06(GaloisScene):
    shot=5
    def s06(self):
        axis,a,b=radical_scene(self)
        self.add(axis,a,b,eq(r'x^2-2=0',3.4))
        arrow=DoubleArrow([-1.3,1.3,0],[1.3,1.3,0],color=GOLD,buff=0)
        self.show(arrow,txt('√2를 새 기준으로 고정',2.4,35,GREEN))
        self.to(82)
        pin=VGroup(Circle(radius=.79,color=GREEN,stroke_width=5),txt('고정',y=-1.5,size=26,color=GREEN)).move_to(b.get_center()+DOWN*.65)
        # Separate ring and label to keep the ring centered on the fixed root.
        pin[0].move_to(b)
        pin[1].move_to(b.get_center()+DOWN*1.25)
        self.show(pin)
        self.to(84)
        self.play(arrow.animate.set_color(RED))
        cross=Cross(arrow,stroke_color=RED,stroke_width=6)
        self.show(cross)
        self.to(87)
        self.play(FadeOut(arrow),FadeOut(cross))
        self.show(eq(r'\{\mathrm{id},\sigma\}\ \longrightarrow\ \{\mathrm{id}\}',-2.9,43,GOLD))
        self.show(txt('남는 것은 항등변환',-4,29,GREEN),txt('Q  →  Q(√2)',4.35,25,MUTED))

class Shot07(GaloisScene):
    shot=6
    def s07(self):
        self.show(txt('근호로 풀 수 있다',3.2,41,GREEN),txt('↕',2.1,46,GOLD))
        self.to(98)
        chain=VGroup(*[box(s,y,GOLD,width=w,height=.8) for s,y,w in [('G₀',.9,6.5),('G₁',-.35,5.4),('G₂',-1.6,4.3),('{e}',-2.85,3.2)]])
        for item in chain:self.show(item,run_time=.45)
        self.show(txt('정규부분군 + 가환 몫군',-4.15,27,GREEN))
        self.to(103)
        self.play(FadeOut(chain))
        self.show(box('3차 · 4차  :  가능',-.1,GREEN),box('일반 5차  :  구조를 확인',-1.65,GOLD))

class Shot08(GaloisScene):
    shot=7
    def s08(self):
        dots=roots(['1','2','3','4','5'],1.8)
        self.show(dots,txt('S₅',3.4,62,GOLD))
        dots=self.permute(dots,[2,0,4,1,3],1)
        self.show(txt('모든 순열 · 5! = 120',-.1,35,GOLD))
        self.to(113)
        outer=RoundedRectangle(width=7.2,height=3.5,color=GOLD,corner_radius=.3).move_to(DOWN*1.65)
        inner=box('A₅ · 짝순열 60개',-1.8,RED,width=5.8,height=1.25)
        self.show(outer,inner)
        self.to(116)
        self.show(txt('S₅의 정규부분군',-3.5,26,MUTED))
        self.play(Indicate(inner,color=RED))
        self.show(txt('핵심은 크기가 아닌 연산 구조',4.45,27,GREEN))

class Shot09(GaloisScene):
    shot=8
    def s09(self):
        self.show(txt('A₅ 안의 두 변환',3.9,32,RED),txt('A = (1 2 3)   B = (3 4 5)',2.85,29,GOLD))
        top=roots(['1','2','3','4','5'],1.35,1.25)
        bottom=roots(['1','2','3','4','5'],-1.4,1.25)
        self.show(top,bottom,txt('A 먼저 → B',2.1,22,MUTED),txt('B 먼저 → A',-.6,22,MUTED))
        # Left actions on labels. Position permutation induces the same cycle action.
        a=[1,2,0,3,4];b=[0,1,3,4,2]
        # Animate values f(i) in fixed input slots; transforms are applied to labels.
        for group,seq in [(top,(a,b)),(bottom,(b,a))]:
            values=list(range(5))
            for p in seq:
                values=[p[v] for v in values]
                self.play(*[Transform(group[i][1],txt(str(v+1),size=28).move_to(group[i])) for i,v in enumerate(values)],run_time=.45)
        self.show(txt('B ∘ A  ≠  A ∘ B',-2.85,37,RED))
        self.show(txt('각 단계의 몫군이 가환이어야 한다',-4.05,26,GREEN))

class Shot10(GaloisScene):
    shot=9
    def s10(self):
        self.show(txt('S₄ : 가환 몫군으로 분해',4.05,29,GREEN))
        names=['S₄','A₄','V₄','C₂','{e}']
        xs=[-3,-1.5,0,1.5,3]
        nodes=VGroup(*[txt(s,2.65,32,GREEN,x=x,width=1.1) for s,x in zip(names,xs)])
        arrows=VGroup(*[Arrow([x+.43,2.65,0],[x+1.04,2.65,0],buff=0,color=GREEN,stroke_width=2,max_tip_length_to_length_ratio=.2) for x in xs[:-1]])
        quotient=VGroup(*[txt(s,1.8,22,GREEN,x=x+.75,width=1.2) for x,s in zip(xs,['C₂','C₃','C₂','C₂'])])
        self.show(nodes,arrows,quotient)
        self.show(txt('화살표 아래: 각 단계의 몫군',1.05,22,MUTED))
        self.to(130)
        self.show(txt('S₅  ▹  A₅  ▹  {e}',-.4,45,RED))
        self.show(txt('C₂',-1.4,27,GREEN,x=-1.45),txt('A₅',-1.4,30,RED,x=1.45))
        self.to(133)
        self.show(box('A₅ : 비가환 단순군',-2.7,RED),txt('중간 정규부분군이 없고, 몫도 비가환',-4,26,RED))

class Shot11(GaloisScene):
    shot=10
    def s11(self):
        self.show(eq(r'ax^5+bx^4+cx^3+dx^2+ex+f=0',3.3,37))
        statement=box('모든 5차에 통하는 근호 공식은 없다',1.6,RED)
        self.show(statement)
        self.to(143)
        self.show(box('특정한 5차는 근호로 가능',-.05,GREEN),eq(r'x^5-32=0\quad\Rightarrow\quad x=2',-1.2,39,BLUE))
        self.to(145.5)
        self.show(eq(r'x^5-x-1=0',-2.3,38),txt('실근 ≈ 1.1673 · 수치 근사 가능',-3.35,29,BLUE))
        self.to(148)
        self.play(Indicate(statement,color=RED))
        self.show(txt('제약: 사칙연산과 근호만 사용한 일반해',4.4,23,MUTED))

class Shot12(GaloisScene):
    shot=11
    def s12(self):
        dots=roots(['α','β','γ','δ','ε'],2.6)
        self.show(dots)
        dots=self.permute(dots,[1,3,0,4,2],.9)
        lines=VGroup(*[ArcBetweenPoints(dots[i].get_center(),dots[j].get_center(),angle=PI/3,color=GOLD,stroke_width=2) for i,j in [(0,2),(1,4),(0,4),(2,3)]])
        self.show(lines)
        self.show(txt('해의 대칭을 분석해',.4,41,GOLD),txt('풀이의 가능성을 밝힌다',-1.15,38,GREEN))
        self.to(159)
        self.play(dots.animate.set_opacity(.35))
        self.show(txt('갈루아 이론',-3.1,48,GOLD),run_time=.5)
        self.to(161)
