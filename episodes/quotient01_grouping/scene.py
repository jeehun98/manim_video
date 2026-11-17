"""Portrait quotient-group discovery; common exact-time captions and audited D4 actions."""
import json
import os
import sys
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from longforms.qcs01_speed.direction import QCSScene,label
from episodes.quotient01_grouping import model

DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BG,INK,MUTED='#101923','#EDF3FC','#8B9CB7'
BLUE,GOLD,GREEN,RED='#61AEFF','#FFD275','#52E2A8','#FF747F'
config.background_color=BG
def txt(s,y=0,size=33,c=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=c,width=width)
def math(s,y=0,size=43,c=INK,width=7.3):
    m=MathTex(s,font_size=size,color=c)
    if m.width>width:m.scale_to_fit_width(width)
    return m.move_to(UP*y)
def panel(s,y,c=GREEN,size=28,width=7.1,height=.95):
    return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.15,stroke_color=c,fill_color=c,fill_opacity=.06),txt(s,size=size,c=c,width=width-.3)).move_to(UP*y)
def token(s,x,y,c,size=31):
    return VGroup(Circle(radius=.52,color=c,fill_color=c,fill_opacity=.09,stroke_width=2),txt(s,size=size,c=c,width=.9)).move_to([x,y,0])
def bucket(title,contents,y,c):
    return VGroup(RoundedRectangle(width=7.05,height=1.9,corner_radius=.22,stroke_color=c,fill_color=c,fill_opacity=.05),
                  txt(title,.43,33,c),txt(contents,-.43,25,c)).move_to(UP*y)
def operation(a,b,result,y,operator='+'):
    colors={'짝':BLUE,'홀':GOLD,'회전':BLUE,'반사':GOLD,'[0]':BLUE,'[1]':GOLD,'R':BLUE,'F':GOLD}
    return VGroup(txt(a,y,36,colors[a],x=-2.65,width=1.5),txt(operator,y,32,x=-1.35,width=.7),
                  txt(b,y,36,colors[b],x=0,width=1.5),txt('=',y,32,x=1.35,width=.7),txt(result,y,36,colors[result],x=2.65,width=1.5))
def table(names=('[0]','[1]'),y=.1,scale=1):
    values=[['+',*names],[names[0],names[0],names[1]],[names[1],names[1],names[0]]]
    cells=VGroup()
    for r,row in enumerate(values):
        for col,s in enumerate(row):
            c=BLUE if s==names[0] else GOLD if s==names[1] else INK
            cell=VGroup(Square(side_length=1.38,color=MUTED,stroke_width=1.5),txt(s,size=31,c=c,width=1.2))
            cell.move_to([(col-1)*1.38,(1-r)*1.38,0]);cells.add(cell)
    return cells.scale(scale).move_to(UP*y)

class SquareDiagram(VGroup):
    def __init__(self,y=1.4,size=2.2):
        super().__init__();self.center=np.array([0.,y,0.]);self.unit=size/2;self.matrix=model.I.copy()
        points=np.column_stack((model.VERTICES*self.unit,np.zeros(4)))+self.center
        self.outline=Polygon(*points,color=BLUE,fill_color=BLUE,fill_opacity=.09,stroke_width=3)
        self.dots=VGroup(*[Dot(p,radius=.1,color=c) for p,c in zip(points,(BLUE,GOLD,GREEN,RED))])
        self.labels=VGroup(*[txt(s,size=23,c=c,width=.6).move_to(self.center+(p-self.center)*1.23)
            for p,s,c in zip(points,'ABCD',(BLUE,GOLD,GREEN,RED))])
        self.add(self.outline,self.dots,self.labels)

class QuotientScene(QCSScene):
    data=DATA
    def setup(self):
        super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.35)
        self.add(txt('부분군 · 정규부분군 · 몫군',7,19,MUTED));self.actions=[]
    def act(self,square,target,duration=.65):
        before=square.matrix.copy();after=target@before
        points=np.column_stack((model.VERTICES@after.T*square.unit,np.zeros(4)))+square.center
        polygon=Polygon(*points,color=BLUE if model.symmetry_class(after)==0 else GOLD,
            fill_color=BLUE if model.symmetry_class(after)==0 else GOLD,fill_opacity=.09,stroke_width=3)
        at=self.offset+self.time
        self.play(Transform(square.outline,polygon),
            *[dot.animate.move_to(p) for dot,p in zip(square.dots,points)],
            *[letter.animate.move_to(square.center+(p-square.center)*1.23) for letter,p in zip(square.labels,points)],run_time=duration)
        square.matrix=after
        self.actions.append(dict(at=round(at,6),end=round(self.offset+self.time,6),before=before.tolist(),
            transform=target.tolist(),after=after.tolist(),class_index=model.symmetry_class(after),name=model.name(after)))
    def rotate_square(self,square,duration=.6):
        before=square.matrix.copy();at=self.offset+self.time
        self.play(Rotate(square,PI/2,about_point=square.center),run_time=duration)
        square.matrix=model.R@before
        # Keep vertex letters upright, at their transformed vertex positions.
        for letter in square.labels:letter.rotate(-PI/2)
        self.actions.append(dict(at=round(at,6),end=round(self.offset+self.time,6),before=before.tolist(),
            transform=model.R.tolist(),after=square.matrix.tolist(),class_index=model.symmetry_class(square.matrix),name=model.name(square.matrix)))
    def construct(self):
        super().construct()
        audit=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'audit')))
        (audit/(self.info['id']+'_actions.json')).write_text(json.dumps(self.actions),encoding='utf-8')

class Shot01(QuotientScene):
    shot=0
    def s01(self):
        positions=[(-2.6,3),(-.8,2.1),(1.7,3.4),(2.7,1.6),(-2.1,.2),(.4,.4),(-.5,-1.1),(2.5,-1.5)]
        numbers=VGroup(*[txt(str(i+1),y,39,MUTED,x=x) for i,(x,y) in enumerate(positions)])
        self.play(LaggedStart(*[FadeIn(n) for n in numbers],lag_ratio=.12),run_time=1.5)
        self.to(4)
        self.play(*[n.animate.move_to([(-1.8 if i%2 else 1.8)+(i%2)*.1,2-(i//2)*.85,0]) for i,n in enumerate(numbers)],run_time=1.4)
        self.show(txt('서로 다른 것을 하나로 묶어도',-2.7,33),txt('연산은 유지될까?',-4,40,GREEN))
        self.to(8);self.play(Indicate(numbers,color=GREEN))

class Shot02(QuotientScene):
    shot=1
    def s02(self):
        axis=NumberLine(x_range=[-4,5,1],length=7.2,color=MUTED).shift(UP*2.4)
        numbers=VGroup(*[txt(str(i),1.75,24,BLUE if i%2==0 else GOLD,x=axis.n2p(i)[0],width=.65) for i in range(-4,6)])
        self.show(axis,numbers)
        self.to(14);self.show(panel('1, 3  →  나머지 1',.4,GOLD))
        self.to(17);self.show(panel('2, 4  →  나머지 0',-1,BLUE))
        self.to(20)
        self.play(FadeOut(axis),FadeOut(numbers),run_time=.4)
        self.show(bucket('짝수 · 나머지 0','…, −4, −2, 0, 2, 4, …',2.55,BLUE),bucket('홀수 · 나머지 1','…, −3, −1, 1, 3, 5, …',-3,GOLD))

class Shot03(QuotientScene):
    shot=2
    def s03(self):
        examples=VGroup(math('2+4=6',3.3,44,BLUE),math('3+5=8',1.2,44,GOLD),math('2+3=5',-.9,44,GOLD))
        self.show(examples)
        self.to(30)
        first,second=operation('짝','짝','짝',3.3),operation('홀','홀','짝',1.2)
        self.play(Transform(examples[0],first),Transform(examples[1],second),run_time=.8)
        self.to(34);self.play(Transform(examples[2],operation('짝','홀','홀',-.9)),run_time=.8)
        self.to(37)
        self.show(txt('3+5=8   /   7+9=16',-2.6,31,GOLD),panel('합은 달라도 결과 집단은 짝수',-4,GREEN))

class Shot04(QuotientScene):
    shot=3
    def s04(self):
        outer=RoundedRectangle(width=7.4,height=7.3,corner_radius=.25,color=MUTED).move_to(UP*.5)
        self.show(outer,txt('정수 ℤ',3.6,34,MUTED))
        self.to(45)
        subgroup=bucket('짝수 2ℤ','…, −4, −2, 0, 2, 4, …',1.75,BLUE);self.show(subgroup)
        self.to(49)
        self.show(txt('닫힘: 2 + 4 = 6',-.1,29,BLUE),txt('항등원: 2 + 0 = 2',-1.15,29,BLUE),txt('역원: 2 + (−2) = 0',-2.2,29,BLUE))
        self.to(54);self.play(Circumscribe(subgroup,color=GREEN))
        self.to(57)
        self.show(panel('부분군: 2ℤ ≤ ℤ',-4.1,GREEN),txt('결합법칙은 정수 덧셈에서 물려받는다',4.55,21,MUTED))

class Shot05(QuotientScene):
    shot=4
    def s05(self):
        note=txt('묶음의 연산에는 추가 조건이 필요하다',4.3,26,MUTED)
        first=math('1+3=4',2.5,49,GOLD);self.show(note,first)
        self.to(67)
        second=math('5+7=12',1,49,GOLD);self.show(second)
        requirement=panel('어떤 대표를 골라도 결과 집단은 같다',-1,GREEN,size=26);self.show(requirement)
        self.to(73)
        reminder=txt('두 결과 모두 짝수 집단',-2.5,31,BLUE);self.show(reminder)
        self.to(77)
        self.play(FadeOut(VGroup(note,first,second,requirement,reminder)),run_time=.4)
        name=txt('정규부분군',4,45,GREEN);self.show(name)
        self.to(80)
        equation=math(r'gNg^{-1}=N\quad(\forall g\in G)',2.6,43,GREEN)
        boundary=RoundedRectangle(width=6.8,height=2.1,corner_radius=.2,color=BLUE).move_to(UP*.5)
        dots=VGroup(*[token(s,x,.5,BLUE,29) for s,x in zip(('e','r','r²','r³'),(-2.25,-.75,.75,2.25))])
        self.show(equation,boundary,dots)
        self.play(Swap(dots[1],dots[3]),run_time=1)
        explanation=txt('예: 원소는 바뀌어도 집합 N은 그대로',-1.3,27,BLUE)
        key=txt('r: 90° 회전   /   g: 반사',-2.5,25,MUTED)
        self.show(explanation,key)
        self.to(86)
        self.play(FadeOut(VGroup(equation,boundary,dots,explanation,key)),run_time=.35)
        self.show(math(r'g+n-g=n',1.5,54,BLUE),panel('정수 덧셈은 가환 → 2ℤ는 정규부분군',-.5,GREEN,size=26),txt('여기서는 각 원소도 그대로 유지된다',-2.1,26,MUTED))

class Shot06(QuotientScene):
    shot=5
    def s06(self):
        evens=bucket('0 + 2ℤ','…, −4, −2, 0, 2, 4, …',2.7,BLUE)
        odds=bucket('1 + 2ℤ','…, −3, −1, 1, 3, 5, …',.2,GOLD)
        self.show(evens,odds)
        self.to(94)
        rule=txt('차이가 짝수이면 같은 묶음',-2,32,GREEN);self.show(rule)
        self.to(97)
        self.play(Transform(evens,panel('[0] : 짝수 집단',2.7,BLUE)),Transform(odds,panel('[1] : 홀수 집단',1.4,GOLD)),FadeOut(rule),run_time=.8)
        self.to(101)
        self.show(txt('몫군 · Quotient Group',4.3,33,GREEN))
        self.show(table(y=-1.2,scale=.72),math(r'\mathbb Z/2\mathbb Z=\{[0],[1]\}',-4.1,34,GREEN))

class Shot07(QuotientScene):
    shot=6
    def s07(self):
        calculation=math(r'1{,}234{,}567+9{,}876{,}543',2.7,42,GOLD);self.show(calculation)
        self.to(111)
        self.show(operation('홀','홀','짝',.6),txt('정확한 합을 몰라도 홀짝성은 안다',-1.2,30,GREEN))
        self.to(118)
        self.play(calculation.animate.set_opacity(.22))
        self.show(math(r'[a]+[b]=[a+b]',-2.9,47,GREEN),txt('잃는 정보: 개별 값  /  남는 정보: 덧셈 구조',4.3,23,MUTED))

class Shot08(QuotientScene):
    shot=7
    def s08(self):
        square=SquareDiagram(y=2.3,size=2.2);self.show(square)
        self.to(126)
        for _ in range(3):self.rotate_square(square,.45)
        rot=txt('회전: 0° · 90° · 180° · 270°',.4,28,BLUE)
        self.show(rot)
        # Return to identity, then display each reflection with its fixed axis.
        self.rotate_square(square,.35)
        for k,target in enumerate(model.REFLECTIONS):
            relative=target@square.matrix.T
            self.act(square,relative,duration=.3)
        refl=txt('반사: 가로 · 세로 · 두 대각선',-.6,28,GOLD);self.show(refl,run_time=.4)
        self.to(130)
        self.show(panel('회전 C₄ : 정규부분군',-2,GREEN))
        self.show(math(r'srs^{-1}=r^{-1}\in C_4',-3.4,36,BLUE),txt('90°가 −90°로 바뀌어도 여전히 회전',-4.3,24,MUTED))

class Shot09(QuotientScene):
    shot=8
    def s09(self):
        rows=VGroup(operation('회전','회전','회전',3.35,'∘'),operation('반사','반사','회전',1.65,'∘'),operation('회전','반사','반사',-.05,'∘'))
        for row in rows:self.show(row,run_time=.45)
        self.show(txt('결과의 집단만 추적한다',4.5,26,MUTED))
        self.to(142)
        self.show(txt('짝수 ↔ 회전    홀수 ↔ 반사',-1.7,29,GREEN))
        self.show(math(r'\mathbb Z/2\mathbb Z\cong D_4/C_4',-3.05,42,GREEN),txt('대상은 달라도 같은 두 원소의 군',-4.25,27,GREEN))

class Shot10(QuotientScene):
    shot=9
    def s10(self):
        self.show(panel('부분군: 큰 군 안의 작은 군',3.1,BLUE))
        self.to(151)
        self.show(panel('정규부분군: 묶음의 연산을 보장',.8,GREEN))
        self.to(154)
        self.show(panel('몫군: 묶음들이 새로운 원소',-1.5,GOLD))
        self.show(txt('원소 선택 → 조건 확인 → 묶음의 군',-3.8,28,MUTED))

class Shot11(QuotientScene):
    shot=10
    def s11(self):
        exact=txt('…, −4, −3, −2, −1, 0, 1, 2, 3, 4, …',3.5,29,MUTED)
        self.show(exact)
        self.to(160)
        self.play(exact.animate.set_opacity(.2),run_time=.5)
        self.show(panel('[0] : 짝수',1.6,BLUE),panel('[1] : 홀수',.2,GOLD))
        self.show(operation('[1]','[1]','[0]',-2),txt('구체적인 값 대신 필요한 연산 구조를 남긴다',-4.05,26,GREEN))

class Shot12(QuotientScene):
    shot=11
    def s12(self):
        self.show(txt('무엇을 구분할 것인가?',2.6,40,MUTED))
        self.to(169)
        self.show(txt('무엇을 같은 것으로\n취급할 수 있는가?',-.3,45,GREEN))
        self.show(txt('묶음 속에서도 유지되는 연산',-3.1,29,GOLD))
        self.to(173)
