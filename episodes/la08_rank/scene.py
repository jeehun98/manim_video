"""LA08: rank counts independent output directions, not matrix entries."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
A=np.array([[1.,2.],[2.,4.]])
B=np.array([[1.,1.],[1.,-1.]])
DURATION=107
CAPTIONS=[
(0,'recap','앞에서 독립인 벡터는, 서로 대체할 수 없는\n새로운 자유도를 제공한다고 했습니다.'),
(6,'matrix_a','이번에는 행렬 안에 독립적인 자유도가\n실제로 몇 개 있는지 세어보겠습니다.'),
(12,'size','이 행렬에는 숫자가 4개, 행과 열이 각각 2개입니다.\n그렇다면 자유도도 2개일까요?'),
(18,'dependent_rows','두 번째 행은 첫 번째 행의 정확히 2배입니다.\n새로운 관계를 추가한 것이 아닙니다.'),
(24,'equations','입력에 적용해보면, 두 번째 출력은\n언제나 첫 번째 출력의 2배입니다.'),
(31,'samples','입력을 다르게 넣어도\n이 출력 관계는 바뀌지 않습니다.'),
(37,'line','그래서 출력은 평면 전체가 아니라,\ny₂ = 2y₁이라는 한 직선에만 놓입니다.'),
(43,'rank_one','출력은 두 성분이지만,\n독립적으로 움직일 수 있는 방향은 하나. Rank는 1입니다.'),
(50,'matrix_b','이번에는 두 행이 서로 독립인\n다른 행렬을 보겠습니다.'),
(55,'sum_difference','첫 출력은 입력의 합, 두 번째는 차이입니다.\n한쪽 출력이 다른 쪽의 배수로 정해지지 않습니다.'),
(62,'plane','이 행렬의 출력은\n평면의 두 방향으로 독립적으로 움직일 수 있습니다.'),
(68,'comparison','같은 2×2 행렬이어도,\n하나는 Rank 1, 다른 하나는 Rank 2입니다.'),
(75,'row_column','Rank는 독립인 행의 최대 개수이고,\n독립인 열의 최대 개수와도 같습니다.'),
(82,'geometric','기하학적으로는 출력이 만들 수 있는 공간의 차원.\n직선이면 1, 평면이면 2입니다.'),
(89,'large','그래서 행렬이 커 보여도,\n많은 행이 서로의 조합이라면 Rank는 작을 수 있습니다.'),
(96,'meaning','Rank는 숫자의 개수보다,\n결과에 실제로 몇 개의 독립적인 자유도가 남는지를 봅니다.'),
(102,'ending','행렬의 크기가 아니라,\n그 안의 독립적인 구조를 세는 값입니다.'),
]

def mat(values,title='A',size=35,spacing=.95):
    values=np.asarray(values);nr,nc=values.shape
    entries=VGroup(*[txt(f'{values[i,j]:g}'.replace('-','−'),size,BLUE if i==0 else GOLD).move_to([(j-(nc-1)/2)*spacing,((nr-1)/2-i)*.8,0]) for i in range(nr) for j in range(nc)])
    w=(nc-1)*spacing/2+.55;h=(nr-1)*.8/2+.4
    brackets=VGroup(*[VMobject().set_points_as_corners([[s*(w-.14),h,0],[s*w,h,0],[s*w,-h,0],[s*(w-.14),-h,0]]).set_stroke(INK,2) for s in [-1,1]])
    label=txt(title,29,INK).move_to(UP*(h+.55))
    return VGroup(entries,brackets,label)

class Rank(Scene):
    origin=np.array([-.2,-.5,0.]);unit=.65
    def p(self,v):return self.origin+self.unit*np.array([v[0],v[1],0])
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   08',19,MUTED).move_to(UP*7),txt('Rank: 실제로 남는 자유도',36).move_to(UP*6.05))
        self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(DOWN*6.15);self.add(self.sub)
            anim,seconds=getattr(self,action)()
            if anim:self.play(*anim,run_time=seconds)
            if end-self.time>1e-5:self.wait(end-self.time)
            if abs(self.time-end)>.04:raise ValueError(f'Timeline drift: {action}')
    def heading(self,s):
        self.remove(self.head);self.head=txt(s,30).move_to(UP*4.65);self.add(self.head)
    def formula(self,s):
        self.remove(self.note);self.note=txt(s,26).move_to(DOWN*4.55);self.add(self.note)
    def clear(self,title,note=''):
        self.remove(*[m for m in self.mobjects if all(m is not k for k in [self.chrome,self.head,self.note,self.sub])]);self.heading(title);self.formula(note)
    def grid(self):
        g=VGroup()
        for x in range(-4,5):g.add(Line(self.p((x,-4)),self.p((x,4)),color=MUTED,stroke_width=1 if x==0 else .65,stroke_opacity=.5 if x==0 else .18))
        for y in range(-4,5):g.add(Line(self.p((-4,y)),self.p((4,y)),color=MUTED,stroke_width=1 if y==0 else .65,stroke_opacity=.5 if y==0 else .18))
        return g
    def board(self):
        self.add(self.grid(),Dot(self.origin,radius=.04,color=INK),txt('y₁',23,MUTED).move_to(self.p((4.5,0))),txt('y₂',23,MUTED).move_to(self.p((0,4.5))))
    def patch(self,matrix,extent=.8):
        coords=np.linspace(-extent,extent,7)
        dots=VGroup(*[Dot(self.p(matrix@np.array([a,b])),radius=.045,color=BLUE) for a in coords for b in coords])
        lines=VGroup()
        for t in coords:
            for ends in [[(t,-extent),(t,extent)],[(-extent,t),(extent,t)]]:
                lines.add(Line(*[self.p(matrix@np.array(e)) for e in ends],color=BLUE,stroke_width=1,stroke_opacity=.4))
        return VGroup(lines,dots)
    def recap(self):
        self.heading('서로 대신할 수 없는 자유도');self.formula('독립적인 방향을 몇 개 만들 수 있을까?')
        arrows=VGroup(Arrow(LEFT*1.3+DOWN,RIGHT*1.6+DOWN,buff=0,color=BLUE),Arrow(LEFT*1.3+DOWN,LEFT*1.3+UP*1.7,buff=0,color=GOLD))
        return [Create(arrows)],1.4
    def matrix_a(self):
        self.clear('행렬 안의 독립적인 구조를 세어봅시다','A = [[1, 2], [2, 4]]')
        self.ma=mat(A).scale(1.4).move_to(UP*.5)
        return [FadeIn(self.ma)],1.3
    def size(self):
        self.heading('숫자는 4개 · 행과 열은 2개');self.formula('행렬 크기: 2 × 2     ·     Rank는?')
        return [Circumscribe(self.ma[0],color=PINK)],1.5
    def dependent_rows(self):
        self.heading('두 번째 행은 첫 번째 행의 2배');self.formula('(2, 4) = 2 × (1, 2)')
        return [Circumscribe(VGroup(*self.ma[0][:2]),color=BLUE),Circumscribe(VGroup(*self.ma[0][2:]),color=GOLD)],1.8
    def equations(self):
        self.clear('출력 사이에도 같은 관계가 생깁니다','모든 입력 x에 대해 y₂ = 2y₁')
        first=txt('y₁ = x₁ + 2x₂',39,BLUE).move_to(UP*1.6)
        second=txt('y₂ = 2x₁ + 4x₂',39,GOLD).move_to(UP*.1)
        third=txt('= 2(x₁ + 2x₂) = 2y₁',35,GOLD).move_to(DOWN*1.4)
        return [FadeIn(first),FadeIn(second),FadeIn(third)],1.7
    def samples(self):
        self.clear('입력은 달라도, 출력은 이 관계 위에','y = Ax     ·     출력 좌표를 표시합니다')
        self.board();self.dot=Dot(self.p((1,2)),color=PINK,radius=.09)
        self.label=txt('x = (1, 0)  →  y = (1, 2)',27).move_to(UP*3.15)
        self.add(self.dot,self.label)
        self.add(Dot(self.p((1,2)),color=PINK,radius=.055))
        return [Succession(AnimationGroup(self.dot.animate.move_to(self.p((2,4))),Transform(self.label,txt('x = (0, 1)  →  y = (2, 4)',27).move_to(UP*3.15)),run_time=1.1),AnimationGroup(self.dot.animate.move_to(self.origin),Transform(self.label,txt('x = (2, −1)  →  y = (0, 0)',27).move_to(UP*3.15)),run_time=1.1),AnimationGroup(self.dot.animate.move_to(self.p((-1,-2))),Transform(self.label,txt('x = (−1, 0)  →  y = (−1, −2)',27).move_to(UP*3.15)),run_time=1.1))],3.3
    def line(self):
        self.remove(self.label)
        self.heading('가능한 출력은 한 직선뿐');self.formula('y₂ = 2y₁     ·     가로·세로를 따로 조절할 수 없음')
        self.outputline=Line(self.p((-2,-4)),self.p((2,4)),color=PINK,stroke_width=4)
        return [Create(self.outputline),self.dot.animate.move_to(self.p((1.5,3)))],1.8
    def rank_one(self):
        self.heading('출력의 독립적인 방향: 1개');self.formula('Rank(A) = 1')
        rank=txt('Rank 1',34,PINK).move_to([-1.7,1.65,0])
        return [FadeIn(rank)],1.2
    def matrix_b(self):
        self.clear('서로 독립인 두 행을 가진 행렬','B: 합과 차이를 각각 읽는 두 관계')
        self.mb=mat(B,'B').scale(1.4).move_to(UP*.5)
        return [FadeIn(self.mb)],1.3
    def sum_difference(self):
        self.clear('합과 차이를 별도로 조절할 수 있습니다','두 출력 사이에 고정된 선형 상쇄 관계가 없습니다')
        eq1=txt('y₁ = x₁ + x₂',40,BLUE).move_to(UP*1.2)
        eq2=txt('y₂ = x₁ − x₂',40,GOLD).move_to(DOWN*.4)
        inverse=txt('원하는 y에 대해 x₁ = (y₁ + y₂)/2, x₂ = (y₁ − y₂)/2',23,MUTED).move_to(DOWN*2.35)
        return [FadeIn(eq1),FadeIn(eq2),FadeIn(inverse)],1.5
    def plane(self):
        self.clear('출력은 두 방향을 독립적으로 만듭니다','B(1/2, 1/2) = (1, 0)     ·     B(1/2, −1/2) = (0, 1)')
        self.board();patch=self.patch(np.eye(2),1.4);self.add(patch)
        # This is a bounded input patch, not a claim that the output is bounded.
        note=txt('평면 일부의 변환을 표시',20,MUTED).move_to(UP*3.25);self.add(note)
        vx=Arrow(self.origin,self.p((1,0)),buff=0,color=BLUE);vy=Arrow(self.origin,self.p((0,1)),buff=0,color=GOLD)
        return [Transform(patch,self.patch(B,1.4)),GrowArrow(vx),GrowArrow(vy)],2
    def comparison(self):
        self.clear('같은 2 × 2, 서로 다른 Rank','행렬의 모양만으로 자유도를 알 수 없습니다')
        self.ca=mat(A,'A').move_to([-2,1.6,0]);self.cb=mat(B,'B').move_to([2,1.6,0]);self.add(self.ca,self.cb)
        left=VGroup(Line([-2.7,-2.9,0],[-1.3,-.5,0],color=PINK,stroke_width=4),txt('Rank 1 · 직선',25,PINK).move_to([-2,-3.5,0]))
        right=VGroup(Polygon([.85,-1.7,0],[2,-.5,0],[3.15,-1.7,0],[2,-2.9,0],color=BLUE,fill_opacity=.15),txt('Rank 2 · 평면',25,BLUE).move_to([2,-3.5,0]))
        return [FadeIn(left),FadeIn(right)],1.4
    def row_column(self):
        self.clear('행으로 세어도, 열로 세어도 같습니다','독립인 행의 최대 개수 = 독립인 열의 최대 개수')
        self.ma=mat(A).scale(1.25).move_to(UP*.3);self.add(self.ma)
        row=VGroup(*self.ma[0][:2]);col=VGroup(self.ma[0][0],self.ma[0][2])
        eq=txt('행 2 = 2 × 행 1\n열 2 = 2 × 열 1',28,MUTED).move_to(DOWN*2.2);self.add(eq)
        return [Succession(Circumscribe(row,color=BLUE,run_time=1.1),Circumscribe(col,color=GOLD,run_time=1.1))],2.2
    def geometric(self):
        self.clear('Rank = 출력 공간의 차원','Rank(A) = dim{ Ax | x는 입력 벡터 }')
        self.board();self.patch_in=self.patch(np.eye(2));self.add(self.patch_in)
        return [Transform(self.patch_in,self.patch(A))],2.3
    def large(self):
        self.clear('큰 숫자표도, 독립적인 구조는 적을 수 있습니다','각 행이 (1, 2, 3)의 배수     ·     Rank = 1')
        large=np.outer([1,2,3],[1,2,3]);self.large_mat=mat(large,'3 × 3 행렬',32,1.05).move_to(UP*.3)
        return [FadeIn(self.large_mat)],1.4
    def meaning(self):
        self.clear('결과에 남는 독립적인 자유도를 센다','Rank = 출력 공간의 차원')
        words=VGroup(txt('원소 4개 · 2 × 2 행렬',30,MUTED),txt('하지만',30,PINK),txt('독립적인 방향 1개 · Rank 1',34,BLUE)).arrange(DOWN,buff=.45).move_to(UP*.6)
        return [FadeIn(words)],1.3
    def ending(self):
        self.clear('Rank: 실제로 남는 자유도','숫자표의 크기보다, 독립적인 구조')
        title=txt('출력이 움직일 수 있는\n독립적인 방향은 몇 개인가?',36).move_to(UP*.5)
        return [FadeIn(title)],1.3
