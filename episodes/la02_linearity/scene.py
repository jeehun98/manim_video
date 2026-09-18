"""LA02: scalar multiplication, addition, and a nonlinear counterexample."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *

spec = importlib.util.spec_from_file_location('la01_shared', Path(__file__).resolve().parents[1] / 'la01_matrix_as_transformation/scene.py')
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
txt, matrix = shared.txt, shared.matrix
BLUE, GOLD, INK, MUTED, PINK = shared.BLUE, shared.GOLD, shared.INK, shared.MUTED, shared.PINK
A = shared.A
DURATION = 164
CAPTIONS = [
 (0,'recap','앞에서 행렬은 공간을 어떻게 바꿀지를\n기록하는 규칙이라고 했습니다.'),
 (6,'scope','여기서는 평면의 벡터에\n이차 정사각행렬을 곱하는 변환을 말합니다.'),
 (12,'rules','모든 변화가 가능한 것은 아닙니다.\n행렬 변환에는 두 가지 중요한 조건이 있습니다.'),
 (18,'scale_start','먼저 벡터 하나를 보겠습니다.\n같은 벡터로 두 가지 순서를 비교해봅시다.'),
 (24,'scale_first','위에서는 벡터를 먼저 두 배로 늘립니다.\n아래에서는 먼저 행렬로 변환합니다.'),
 (31,'scale_second','이제 위에서는 행렬로 변환하고,\n아래에서는 변환된 벡터를 두 배로 늘립니다.'),
 (38,'scale_equal','순서가 달라도 도착점이 같습니다.\n두 배뿐 아니라, 어떤 실수 배율도 마찬가지입니다.'),
 (46,'sum_start','벡터를 더하는 경우도 보겠습니다.\n이번에는 서로 다른 두 벡터입니다.'),
 (52,'sum_first','위에서는 두 벡터를 먼저 더합니다.\n화살표의 머리와 꼬리를 이어 붙이면 됩니다.'),
 (59,'sum_second','그 합을 변환한 결과와,\n각 벡터를 변환한 뒤 더한 결과를 비교합니다.'),
 (67,'sum_equal','이번에도 도착점이 같습니다.\n변환이 벡터의 덧셈을 보존하는 것입니다.'),
 (74,'definition','배수와 덧셈을 보존하는 성질.\n이 두 가지를 함께 선형성이라고 합니다.'),
 (82,'linear_grid','그래서 선형 변환은\n직선을 곡선으로 휘게 만들지 않습니다.'),
 (89,'collapse','다만 공간이 납작해지는 변환에서는\n직선이 한 점으로 줄어들 수도 있습니다.'),
 (96,'nonlinear_start','이번에는 엑스 좌표를 제곱하는\n다른 변환을 보겠습니다.'),
 (102,'diagonal','가로와 세로 격자선만 보면 놓치기 쉽습니다.\n대각선 하나를 함께 따라가 봅시다.'),
 (109,'bend','이 직선은 포물선으로 휘어집니다.\n가로와 세로 격자는 간격이 바뀌고 겹쳐집니다.'),
 (117,'counter_start','배수 관계도 확인해볼까요?\n벡터를 일, 일로 잡아보겠습니다.'),
 (123,'counter_result','두 배 벡터를 변환하면 사, 이.\n먼저 변환하고 두 배로 늘리면 이, 이입니다.'),
 (131,'counter_equal','두 결과가 다릅니다.\n이 변환은 선형 변환이 아닙니다.'),
 (137,'conclusion','행렬이 표현하는 것은 모든 변화가 아니라,\n덧셈과 배율 관계를 보존하는 변화입니다.'),
 (145,'basis','이 성질 덕분에 몇 개의 기본 벡터가\n어디로 가는지만으로 전체 변화를 알 수 있습니다.'),
 (153,'next','그렇다면 왜 두 기저 벡터만으로\n평면 전체를 알 수 있을까요?\n다음에는 벡터의 조합을 더 자세히 보겠습니다.'),
]

class Linearity(shared.MatrixAsTransformation):
    def construct(self):
        self.head, self.note, self.sub = VGroup(), VGroup(), VGroup()
        self.chrome = VGroup(txt('LINEAR ALGEBRA   /   02',19,MUTED).move_to(UP*7),txt('왜 선형 변환일까?',41).move_to(UP*6.05))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub); self.sub=txt(caption,27).move_to(DOWN*6.15); self.add(self.sub)
            animations,seconds=getattr(self,action)()
            if animations: self.play(*animations,run_time=seconds)
            if end-self.time>1e-5: self.wait(end-self.time)
            if abs(self.time-end)>.04: raise ValueError(f'Timeline drift: {action}')

    def fresh(self,title,formula=''):
        self.clear_stage(); self.heading(title); self.formula(formula)

    def panel_point(self,v,row):
        return np.array([-1.3,.9 if row==0 else -2.45,0])+ .68*np.array([*v,0])

    def pa(self,v,row,color=BLUE,start=(0,0)):
        return Arrow(self.panel_point(start,row),self.panel_point(np.array(start)+v,row),buff=0,color=color,stroke_width=5,max_tip_length_to_length_ratio=.16)

    def panels(self,top,bottom):
        for row,label in enumerate([top,bottom]):
            y=3.5 if row==0 else .15
            self.add(txt(label,25,MUTED).move_to(UP*y))
            for x in range(-2,6):
                self.add(Line(self.panel_point((x,-.35),row),self.panel_point((x,3.1),row),stroke_width=.7,color=MUTED,stroke_opacity=.18))
            for y in range(4):
                self.add(Line(self.panel_point((-2,y),row),self.panel_point((5,y),row),stroke_width=.7,color=MUTED,stroke_opacity=.18))
            self.add(Dot(self.panel_point((0,0),row),radius=.04))

    def recap(self):
        self.fresh('空間을 바꾸는 규칙'.replace('空間','공간'),'첫 번째 열과 두 번째 열: 기저 벡터의 도착점')
        self.board(); self.add(matrix([[2,-1],[1,2]],26).move_to(UP*3.7))
        return self.warp(np.eye(2),A),3

    def scope(self):
        self.heading('평면 → 평면의 행렬 변환'); self.formula('T(v) = Av     ·     A: 2 × 2 실수 행렬')
        return [Indicate(self.ex),Indicate(self.ey)],1.5

    def rules(self):
        self.fresh('두 가지 약속')
        a=txt('01   배수를 보존한다',36,BLUE).move_to(UP*1.4)
        b=txt('02   덧셈을 보존한다',36,GOLD).move_to(DOWN*.6)
        return [LaggedStart(FadeIn(a),FadeIn(b),lag_ratio=.6)],2

    def scale_start(self):
        self.fresh('01  /  배수 관계','v = (1, 0)     ·     A = 앞 편의 행렬')
        self.panels('위: 두 배 → 변환','아래: 변환 → 두 배')
        self.top=self.pa(np.array([1,0]),0); self.bottom=self.pa(np.array([1,0]),1)
        return [GrowArrow(self.top),GrowArrow(self.bottom)],1.5

    def scale_first(self):
        self.formula('위: 2v = (2, 0)     아래: Av = (2, 1)')
        return [Transform(self.top,self.pa(np.array([2,0]),0)),Transform(self.bottom,self.pa(np.array([2,1]),1,GOLD))],2.5

    def scale_second(self):
        self.formula('위: A(2v) = (4, 2)     아래: 2Av = (4, 2)')
        return [Transform(self.top,self.pa(np.array([4,2]),0,PINK)),Transform(self.bottom,self.pa(np.array([4,2]),1,PINK))],2.5

    def scale_equal(self):
        self.heading('순서를 바꿔도 같은 도착점'); self.formula('A(cv) = cAv     ·     모든 실수 c')
        markers=VGroup(*[Dot(self.panel_point((4,2),r),color=PINK,radius=.09) for r in [0,1]])
        labels=VGroup(*[txt('(4, 2)',24,PINK).next_to(m,UP,buff=.12) for m in markers])
        return [FadeIn(markers),FadeIn(labels)],1.4

    def sum_start(self):
        self.fresh('02  /  덧셈 관계','u = (0, 1)     v = (1, 0)')
        self.panels('위: 더하기 → 변환','아래: 각각 변환 → 더하기')
        self.ut,self.vt=self.pa(np.array([0,1]),0,GOLD),self.pa(np.array([1,0]),0)
        self.ub,self.vb=self.pa(np.array([0,1]),1,GOLD),self.pa(np.array([1,0]),1)
        return [GrowArrow(m) for m in [self.ut,self.vt,self.ub,self.vb]],1.8

    def sum_first(self):
        self.formula('u + v = (1, 1)')
        self.sumtop=self.pa(np.array([1,1]),0,PINK)
        return [Transform(self.vt,self.pa(np.array([1,0]),0,BLUE,(0,1))),GrowArrow(self.sumtop)],2.4

    def sum_second(self):
        self.formula('A(u + v) = (1, 3)     Au + Av = (1, 3)')
        return [Transform(self.ut,self.pa(np.array([-1,2]),0,GOLD)),Transform(self.vt,self.pa(np.array([2,1]),0,BLUE,(-1,2))),Transform(self.sumtop,self.pa(np.array([1,3]),0,PINK)),Transform(self.ub,self.pa(np.array([-1,2]),1,GOLD)),Succession(Transform(self.vb,self.pa(np.array([2,1]),1)),Transform(self.vb,self.pa(np.array([2,1]),1,BLUE,(-1,2))))],4

    def sum_equal(self):
        self.heading('덧셈의 결과도 그대로 연결됩니다'); self.formula('A(u + v) = Au + Av')
        self.sumbottom=self.pa(np.array([1,3]),1,PINK)
        return [GrowArrow(self.sumbottom),Indicate(self.sumtop)],1.8

    def definition(self):
        self.fresh('이 두 성질이 ‘선형성’입니다','모든 벡터 u, v와 모든 실수 c에 대해')
        a=txt('A(cv) = cAv',42,BLUE).move_to(UP*1.3)
        b=txt('A(u + v) = Au + Av',37,GOLD).move_to(DOWN*.5)
        return [FadeIn(a),FadeIn(b)],1.6

    def linear_grid(self):
        self.fresh('직선을 곡선으로 휘게 하지 않습니다','평행한 직선의 상: 평행하거나 겹침 · 점으로 붕괴 가능')
        self.board()
        return self.warp(np.eye(2),np.array([[1.,.7],[0.,1.]])),3.5

    def collapse(self):
        self.fresh('예외가 아니라, 선형 변환의 한 경우','(x, y) → (x, 0)     ·     세로 직선은 한 점으로')
        self.g=self.grid(np.eye(2)); self.add(self.g)
        lines=VGroup(*[Line(self.p((x,-2.5)),self.p((x,2.5)),color=GOLD,stroke_width=3) for x in [-2,0,2]])
        self.add(lines)
        return [Transform(lines,VGroup(*[Dot(self.p((x,0)),color=GOLD,radius=.09) for x in [-2,0,2]]))],3

    def nonlinear_start(self):
        self.fresh('다른 규칙: x를 제곱한다','F(x, y) = (x², y)')
        self.ng=self.non_grid(0); self.add(self.ng)
        return [FadeIn(txt('x → x²',34,PINK).move_to(UP*3.45))],1.5

    def npnt(self,x,y):
        return np.array([-.8+1.05*x,-.4+1.05*y,0])

    def curve(self,coords,color,width=2):
        return VMobject().set_points_as_corners([self.npnt(x,y) for x,y in coords]).set_stroke(color,width)

    def non_grid(self,alpha):
        def f(x): return (1-alpha)*x+alpha*x*x
        out=VGroup()
        for k in np.linspace(-1.8,1.8,9):
            out.add(self.curve([(f(k),t) for t in np.linspace(-1.8,1.8,41)],MUTED,1).set_opacity(.4))
            out.add(self.curve([(f(t),k) for t in np.linspace(-1.8,1.8,81)],MUTED,1).set_opacity(.4))
        return out

    def diag(self,alpha):
        return self.curve([((1-alpha)*t+alpha*t*t,t) for t in np.linspace(-1.8,1.8,101)],GOLD,4)

    def diagonal(self):
        self.heading('斜めの直線'.replace('斜めの直線','対角線').replace('対角線','대각선도 직선입니다'))
        self.formula('변환 전: (t, t)     ·     y = x')
        self.diagonal_line=self.diag(0)
        return [Create(self.diagonal_line)],2

    def bend(self):
        self.heading('직선이 포물선으로'); self.formula('변환 후: (t², t)     ·     x = y²')
        moving=VGroup(self.ng,self.diagonal_line)
        def update(m,a):
            self.ng.become(self.non_grid(a)); self.diagonal_line.become(self.diag(a))
        return [UpdateFromAlphaFunc(moving,update)],4

    def cp(self,v): return np.array([-1.8,-1.2,0])+.85*np.array([*v,0])

    def ca(self,v,color): return Arrow(self.cp((0,0)),self.cp(v),buff=0,color=color,stroke_width=5)

    def counter_start(self):
        self.fresh('배수 보존이 성립하는지 확인','v = (1, 1)     F(v) = (1, 1)')
        self.cv=self.ca((1,1),BLUE)
        self.add(Dot(self.cp((0,0)),radius=.045))
        return [GrowArrow(self.cv)],1.5

    def counter_result(self):
        self.formula('F(2v) = (4, 2)     2F(v) = (2, 2)')
        self.cfirst,self.csecond=self.ca((4,2),PINK),self.ca((2,2),GOLD)
        labels=VGroup(txt('F(2v) = (4, 2)',25,PINK).move_to([1.6,2.0,0]),txt('2F(v) = (2, 2)',25,GOLD).move_to([-1.5,2.8,0]))
        return [GrowArrow(self.cfirst),GrowArrow(self.csecond),FadeIn(labels)],2.8

    def counter_equal(self):
        self.heading('두 결과가 다릅니다'); self.formula('F(2v) ≠ 2F(v)     →     비선형 변환')
        return [Indicate(self.cfirst),Indicate(self.csecond)],1.6

    def conclusion(self):
        self.fresh('선형대수학이 다루는 핵심 관계','선형성 = 덧셈 보존 + 배수 보존')
        main=txt('T(au + bv)\n= aT(u) + bT(v)',39).move_to(UP*.7)
        return [FadeIn(main)],1.5

    def basis(self):
        self.heading('조합을 알면, 도착점도 알 수 있습니다'); self.formula('p = a e₁ + b e₂   →   T(p) = aT(e₁) + bT(e₂)')
        return [],0

    def next(self):
        self.fresh('다음 이야기','03  /  기저: 평면을 만드는 두 방향')
        title=txt('왜 두 벡터면 충분할까?',40).move_to(UP*.7)
        subtitle=txt('모든 벡터를 만드는 조합',28,MUTED).move_to(DOWN*.6)
        return [FadeIn(title),FadeIn(subtitle)],1.5
