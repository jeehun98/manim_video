"""LA06: a nontrivial kernel erases differences between inputs."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
A=np.array([[1.,0.],[0.,0.]])
X1=np.array([2.,2.]);X2=np.array([2.,-1.])
DURATION=100
CAPTIONS=[
(0,'recap','앞에서는 행렬이 어떤 패턴은 키우고,\n어떤 패턴은 줄일 수 있다는 걸 봤습니다.'),
(5,'zero_question','그렇다면 어떤 패턴의 배율이\n아예 0이라면 어떻게 될까요?'),
(10,'rule','이번에는 첫 성분은 남기고,\n둘째 성분을 0으로 만드는 행렬을 보겠습니다.'),
(16,'vanish','위쪽을 향하는 이 벡터는,\n변환 뒤에 0벡터가 됩니다. 패턴이 사라진 겁니다.'),
(22,'inputs','서로 다른 두 입력을 놓아봅시다.\n하나는 (2, 2), 다른 하나는 (2, −1)입니다.'),
(28,'outputs','같은 행렬을 적용하면,\n둘 다 (2, 0)이 됩니다.'),
(34,'same','입력은 달랐는데 출력은 같습니다.\n두 입력을 구분하던 차이는 어디로 갔을까요?'),
(39,'difference','두 입력의 차이는 (0, 3)입니다.\n서로를 구분하던 차이가 세로 방향에 있습니다.'),
(45,'move_difference','그 차이 벡터만 따로 꺼내\n같은 행렬에 넣어보겠습니다.'),
(51,'difference_zero','역시 0이 됩니다.\n두 입력의 차이 자체가 변환으로 사라진 것입니다.'),
(57,'nullspace','이렇게 A를 적용했을 때 0이 되는\n모든 벡터의 집합을 영공간이라고 합니다.'),
(64,'all_kernel','이 예에서는 모든 세로 방향 벡터가 사라집니다.\n0벡터도 영공간에 포함됩니다.'),
(70,'shifted','어떤 입력에 이 방향의 차이를 더해도,\n변환 뒤의 결과는 같습니다.'),
(76,'collapse','평면 전체로 보면,\n세로 방향의 차이가 눌려 하나의 선으로 모입니다.'),
(82,'unrecoverable','출력만 보고는 원래 입력이\n어느 높이에 있었는지 구분할 수 없습니다.'),
(88,'general','0이 아닌 벡터가 영공간에 있다면,\n서로 다른 입력이 같은 출력으로 겹칠 수 있습니다.'),
(94,'ending','영공간은 변환이 구분하지 못하는 차이입니다.\n행렬은 정보를 바꾸면서, 어떤 차이는 지울 수 있습니다.'),
]

class Nullspace(Scene):
    origin=np.array([-.8,-.1,0.]);unit=.88
    def p(self,v):return self.origin+self.unit*np.array([v[0],v[1],0])
    def arrow(self,v,color,start=(0,0)):
        return Arrow(self.p(start),self.p(np.array(start)+v),buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.14)
    def grid(self):
        g=VGroup()
        for x in range(-3,5):g.add(Line(self.p((x,-3)),self.p((x,3)),color=MUTED,stroke_width=1.2 if x==0 else .7,stroke_opacity=.65 if x==0 else .2))
        for y in range(-3,4):g.add(Line(self.p((-3,y)),self.p((4,y)),color=MUTED,stroke_width=1.2 if y==0 else .7,stroke_opacity=.65 if y==0 else .2))
        return g
    def board(self):
        self.g=self.grid();self.add(self.g,Dot(self.origin,radius=.045,color=INK))
        self.add(txt('첫 성분',19,MUTED).move_to(self.p((3.6,-.4))),txt('둘째 성분',19,MUTED).move_to(self.p((.05,3.4))))
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   06',19,MUTED).move_to(UP*7),txt('행렬이 지우는 차이',40).move_to(UP*6.05))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(DOWN*6.15);self.add(self.sub)
            animations,seconds=getattr(self,action)()
            if animations:self.play(*animations,run_time=seconds)
            if end-self.time>1e-5:self.wait(end-self.time)
            if abs(self.time-end)>.04:raise ValueError(f'Timeline drift {action}')
    def heading(self,s):
        self.remove(self.head);self.head=txt(s,30).move_to(UP*4.65);self.add(self.head)
    def formula(self,s):
        self.remove(self.note);self.note=txt(s,26).move_to(DOWN*4.55);self.add(self.note)
    def clear(self,title,note=''):
        self.remove(*[m for m in self.mobjects if all(m is not k for k in [self.chrome,self.head,self.note,self.sub])]);self.heading(title);self.formula(note)
    def recap(self):
        self.heading('패턴마다 다른 배율');self.formula('키우거나, 줄이거나')
        group=VGroup(txt('× 2',50,GOLD),txt('× 1/2',50,PINK)).arrange(RIGHT,buff=1.3).move_to(UP*.6)
        return [FadeIn(group)],1.2
    def zero_question(self):
        self.clear('배율이 0이라면?','0이 아닌 패턴도 사라질 수 있습니다')
        eq=txt('Av = 0',57,PINK).move_to(UP*.6)
        self.add(txt('v ≠ 0',28,MUTED).move_to(DOWN*1.2))
        return [FadeIn(eq)],1.3
    def rule(self):
        self.clear('새 예시: 세로 성분을 지우는 행렬','A(a, b) = (a, 0)')
        rows=VGroup(txt('1     0',43),txt('0     0',43)).arrange(DOWN,buff=.5)
        brackets=VGroup(*[VMobject().set_points_as_corners([[s*1.45,1.15,0],[s*1.6,1.15,0],[s*1.6,-1.15,0],[s*1.45,-1.15,0]]).set_stroke(INK,2) for s in [-1,1]])
        label=txt('A =',39).move_to(LEFT*2.7)
        return [FadeIn(VGroup(rows,brackets,label))],1.2
    def vanish(self):
        self.clear('위쪽 벡터가 0벡터로','v = (0, 1)     →     Av = (0, 0)')
        self.board();self.v=self.arrow([0,1],PINK);self.add(self.v)
        end=Dot(self.origin,color=PINK,radius=.085)
        return [Succession(Indicate(self.v,color=PINK,scale_factor=1.05,run_time=.8),Transform(self.v,end,run_time=1.3))],2.1
    def inputs(self):
        self.clear('서로 다른 두 입력','x₁ = (2, 2)     ·     x₂ = (2, −1)')
        self.board();self.a1=self.arrow(X1,BLUE);self.a2=self.arrow(X2,GOLD)
        self.d1=Dot(self.p(X1),color=BLUE,radius=.09);self.d2=Dot(self.p(X2),color=GOLD,radius=.09)
        self.labels=VGroup(txt('x₁',26,BLUE).next_to(self.d1,RIGHT,buff=.18),txt('x₂',26,GOLD).next_to(self.d2,RIGHT,buff=.18))
        return [GrowArrow(self.a1),GrowArrow(self.a2),FadeIn(self.d1),FadeIn(self.d2),FadeIn(self.labels)],1.5
    def outputs(self):
        self.heading('같은 출력으로 겹칩니다');self.formula('Ax₁ = Ax₂ = (2, 0)')
        self.add(self.d1.copy().set_opacity(.22),self.d2.copy().set_opacity(.22))
        return [Transform(self.a1,self.arrow([2,0],BLUE)),Transform(self.a2,self.arrow([2,0],GOLD)),self.d1.animate.move_to(self.p((2,0))),Transform(self.d2,Circle(radius=.16,color=GOLD,stroke_width=2).move_to(self.p((2,0)))),FadeOut(self.labels)],2
    def same(self):
        self.heading('다른 입력, 같은 결과');self.formula('x₁ ≠ x₂     하지만     Ax₁ = Ax₂')
        out=txt('(2, 0)',26,INK).next_to(self.d1,DOWN,buff=.22)
        return [FadeIn(out),Circumscribe(self.d2,color=PINK)],1.4
    def difference(self):
        self.clear('두 입력 사이의 차이를 꺼내면','d = x₁ − x₂ = (0, 3)')
        self.board();self.d1=Dot(self.p(X1),color=BLUE,radius=.085);self.d2=Dot(self.p(X2),color=GOLD,radius=.085)
        self.add(self.d1,self.d2,txt('x₁',25,BLUE).next_to(self.d1,RIGHT,buff=.2),txt('x₂',25,GOLD).next_to(self.d2,RIGHT,buff=.2))
        self.diff=self.arrow(X1-X2,PINK,X2)
        return [GrowArrow(self.diff)],1.5
    def move_difference(self):
        self.heading('같은 차이 벡터를 원점에서 보기');self.formula('A(x₁ − x₂) = A(0, 3)')
        self.add(self.diff.copy().set_opacity(.18))
        return [Transform(self.diff,self.arrow([0,3],PINK))],1.6
    def difference_zero(self):
        self.heading('차이 벡터가 통째로 사라집니다');self.formula('A(x₁ − x₂) = Ax₁ − Ax₂ = 0')
        return [Transform(self.diff,Dot(self.origin,color=PINK,radius=.095)),Circumscribe(self.diff,color=PINK)],1.8
    def nullspace(self):
        self.clear('영공간 · A가 0으로 보내는 벡터들','ker(A) = { v | Av = 0 }')
        self.board();self.kernel=Line(self.p((0,-3)),self.p((0,3)),color=PINK,stroke_width=4)
        self.kdots=VGroup(*[Dot(self.p((0,t)),radius=.065,color=PINK) for t in [-2.5,-1.5,0,1.5,2.5]])
        return [Create(self.kernel),FadeIn(self.kdots)],1.5
    def all_kernel(self):
        self.heading('이 예의 영공간은 세로축 전체');self.formula('ker(A) = { (0, t) | t ∈ ℝ }     ·     0벡터 포함')
        moving=self.kdots.copy();self.add(moving)
        return [*[d.animate.move_to(self.origin) for d in moving]],1.8
    def shifted(self):
        self.clear('영공간 방향으로 달라도 결과는 같습니다','x에 v를 더해도: A(x + v) = Ax     (Av = 0)')
        self.board();self.family=DashedLine(self.p((2,-3)),self.p((2,3)),color=BLUE,dash_length=.14)
        self.familydots=VGroup(*[Dot(self.p((2,t)),radius=.075,color=c) for t,c in [(-2.5,BLUE),(-1,GOLD),(0,INK),(1.5,PINK),(2.5,BLUE)]])
        self.add(self.family,self.familydots)
        self.add(txt('세로축과 평행한 입력들의 집합',21,MUTED).move_to(DOWN*3.6))
        return [*[dot.animate.move_to(self.p((2,0))) for dot in self.familydots]],2
    def collapse(self):
        self.clear('평면을 한 선으로 누르면','(a, b) → (a, 0)     ·     세로 방향의 차이 소실')
        self.board();reference=self.g.copy().set_opacity(.07);self.add(reference);self.bring_to_back(reference)
        points=VGroup(*[Dot(self.p((a,b)),radius=.055,color=BLUE if b>0 else GOLD) for a in [-2,-1,0,1,2,3] for b in [-2,-1,1,2]])
        self.add(points)
        projected=self.g.copy().apply_matrix(np.diag([1,0,1]),about_point=self.origin)
        return [Transform(self.g,projected),*[dot.animate.move_to(np.array([dot.get_x(),self.origin[1],0])) for dot in points]],2.4
    def unrecoverable(self):
        self.heading('출력만으로는 원래 높이를 알 수 없습니다');self.formula('(2, 2), (2, −1), (2, 5), …     →     (2, 0)')
        return [Circumscribe(Dot(self.p((2,0)),radius=.13),color=PINK)],1.5
    def general(self):
        self.clear('0이 아닌 차이가 사라질 수 있다면','0벡터만 있는 영공간과 구별해야 합니다')
        first=txt('v ≠ 0,   Av = 0',43,PINK).move_to(UP*1.7)
        second=txt('x ≠ x + v',37).move_to(UP*.1)
        third=txt('Ax = A(x + v)',40,BLUE).move_to(DOWN*1.6)
        return [FadeIn(first),FadeIn(second),FadeIn(third)],1.5
    def ending(self):
        self.clear('영공간: 변환이 지우는 차이','서로 다른 입력을 같은 출력으로 만드는 방향')
        title=txt('출력에서 더 이상\n구분할 수 없는 정보',40).move_to(UP*.5)
        return [FadeIn(title)],1.3
