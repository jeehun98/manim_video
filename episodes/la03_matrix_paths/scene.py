"""LA03: A squared joins exactly two edges and sums over intermediate nodes."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
GREEN='#8CE3BB'
A=np.array([[0,0,0,0],[.5,0,0,0],[0,.8,0,.3],[.2,0,0,0]])
A2=A@A
DURATION=100
CAPTIONS=[
(0,'recap','앞에서는 관계를 따라 값이 전달되고,\n같은 목적지에서 더해지는 과정을 봤습니다.'),
(5,'path_setup','이번에는 관계를\n한 번 더 통과시켜 보겠습니다.'),
(9,'indirect','첫 번째와 세 번째는 직접 연결되지 않아도,\n두 번째를 거쳐 이어질 수 있습니다.'),
(14,'weights','첫 연결의 영향은 0.5,\n그다음 연결의 영향은 0.8입니다.'),
(19,'first_pass','출발값을 1로 놓으면,\n첫 연결을 지난 값은 0.5입니다.'),
(24,'second_pass','여기에 다시 0.8을 곱하면,\n도착하는 값은 0.4가 됩니다.'),
(30,'product','한 경로에서는 영향을 곱합니다.\n앞 단계의 결과에 다음 관계가 적용되기 때문입니다.'),
(35,'add_four','이제 네 번째 대상을 추가해,\n또 다른 두 단계 경로를 만들어봅시다.'),
(40,'other_path','네 번째를 거치는 경로의 영향은\n0.2 × 0.3 = 0.06입니다.'),
(46,'parallel_paths','두 경로는 중간 대상이 다르지만,\n출발점과 목적지는 같습니다.'),
(51,'total','따라서 두 기여를 더합니다.\n0.4 + 0.06 = 0.46입니다.'),
(56,'twice','같은 관계를 두 번 적용하는 계산.\n이것이 A²입니다.'),
(61,'matrix_entry','원래 행렬의 3행 1열은 0이지만,\nA²의 같은 자리에는 0.46이 들어갑니다.'),
(67,'sum_formula','이 한 칸은 가능한 중간 대상들을 거쳐,\n같은 출발점과 목적지를 잇는 기여의 합입니다.'),
(73,'intermediate','여기서 k는 중간 대상입니다.\n연결이 없는 경로의 기여는 0이 됩니다.'),
(79,'factor_order','오른쪽 항이 출발점에서 중간으로,\n왼쪽 항이 중간에서 목적지로 가는 관계입니다.'),
(84,'general','서로 다른 관계도 이어 붙일 수 있습니다.\nA 다음 B를 적용하면, BA가 됩니다.'),
(89,'roles','곱셈은 한 경로의 영향을 만들고,\n덧셈은 여러 경로의 기여를 모읍니다.'),
(94,'ending','행렬곱은 두 관계를 이어 붙여,\n새로운 관계를 만드는 연산으로 볼 수 있습니다.'),
]

class PathNetwork(VGroup):
    def __init__(self):
        super().__init__()
        positions=[[-2.7,0,0],[0,1.85,0],[2.7,0,0],[0,-1.85,0]]
        colors=[BLUE,GOLD,PINK,GREEN]
        self.nodes=VGroup(*[VGroup(Circle(radius=.43,color=colors[i],fill_color=shared.config.background_color,fill_opacity=1,stroke_width=3),txt(str(i+1),28,colors[i])).move_to(p) for i,p in enumerate(positions)])
        self.edges={};self.labels={}
        for source,target,value,color in [(0,1,.5,GOLD),(1,2,.8,GOLD),(0,3,.2,GREEN),(3,2,.3,GREEN)]:
            a=np.array(positions[source],dtype=float);b=np.array(positions[target],dtype=float);d=(b-a)/np.linalg.norm(b-a)
            edge=Arrow(a+d*.47,b-d*.47,buff=0,color=color,stroke_width=3,max_tip_length_to_length_ratio=.13)
            label=txt(f'× {value:g}',25,color).move_to((a+b)/2+UP*(.42 if target==1 or source==1 else -.42))
            label.add_background_rectangle(color=shared.config.background_color,opacity=1,buff=.06)
            self.edges[(source,target)]=edge;self.labels[(source,target)]=label
        self.add(*self.edges.values(),*self.labels.values(),self.nodes)

def matrix4(values,title):
    entries=VGroup(*[txt(f'{values[i,j]:g}',25,PINK if (i,j)==(2,0) else INK).move_to([(j-1.5)*.68,(1.5-i)*.66,0]) for i in range(4) for j in range(4)])
    brackets=VGroup(*[VMobject().set_points_as_corners([[s*1.28,1.35,0],[s*1.43,1.35,0],[s*1.43,-1.35,0],[s*1.28,-1.35,0]]).set_stroke(INK,2) for s in [-1,1]])
    name=txt(title,31).move_to(UP*1.95)
    return VGroup(entries,brackets,name)

class MatrixPaths(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   03',19,MUTED).move_to(UP*7),txt('경로를 잇고, 기여를 모은다',36).move_to(UP*6.05))
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
        self.remove(self.note);self.note=txt(s,27).move_to(DOWN*4.55);self.add(self.note)
    def clear(self,title,note=''):
        self.remove(*[m for m in self.mobjects if all(m is not k for k in [self.chrome,self.head,self.note,self.sub])]);self.heading(title);self.formula(note)
    def net_base(self,full=False):
        self.net=PathNetwork()
        self.add(*self.net.nodes[:3],self.net.edges[(0,1)],self.net.edges[(1,2)])
        if full:self.add(self.net)
    def travel(self,key,value,color):
        token=txt(value,25,color).move_to(self.net.edges[key].get_start())
        token.add_background_rectangle(color=shared.config.background_color,opacity=1,buff=.08)
        return Succession(FadeIn(token,run_time=.1),MoveAlongPath(token,self.net.edges[key],run_time=1.05),FadeOut(token,run_time=.1))
    def recap(self):
        self.heading('같은 목적지에서 기여를 더한다');self.formula('여러 출발점 → 하나의 목적지')
        sources=VGroup(*[txt(s,33,c).move_to([-2,1.3-i*1.3,0]) for i,(s,c) in enumerate([('4',GOLD),('2',GREEN)])])
        out=txt('6',44,PINK).move_to([2,.65,0])
        arrows=VGroup(*[Arrow(s.get_right(),out.get_left(),buff=.2,color=c,stroke_width=3) for s,c in zip(sources,[GOLD,GREEN])])
        return [FadeIn(sources),GrowArrow(arrows[0]),GrowArrow(arrows[1]),FadeIn(out)],1.8
    def path_setup(self):
        self.clear('이번에는, 두 단계를 이어보기','새 예시 · 화살표 방향: 주는 대상 → 받는 대상')
        self.net=PathNetwork()
        return [FadeIn(VGroup(*self.net.nodes[:3])),LaggedStart(Create(self.net.edges[(0,1)]),Create(self.net.edges[(1,2)]),lag_ratio=.7)],2
    def indirect(self):
        self.heading('직접 연결은 없어도, 간접 연결은 있습니다');self.formula('1 → 2 → 3     ·     정확히 두 단계')
        self.direct=DashedLine([-2.2,-.45,0],[2.2,-.45,0],color=MUTED,dash_length=.13)
        self.directlabel=txt('직접 연결 없음',24,MUTED).move_to(DOWN*.85)
        return [Create(self.direct),FadeIn(self.directlabel),self.travel((0,1),'→',GOLD)],1.8
    def weights(self):
        self.heading('두 연결의 크기를 정하면');self.formula('1 → 2 : 0.5     2 → 3 : 0.8')
        return [FadeIn(self.net.labels[(0,1)]),FadeIn(self.net.labels[(1,2)])],1
    def first_pass(self):
        self.heading('첫 번째 연결을 통과');self.formula('1 × 0.5 = 0.5')
        self.value=txt('현재 값 0.5',25,GOLD).move_to(UP*2.65)
        return [Succession(self.travel((0,1),'1',BLUE),FadeIn(self.value,run_time=.3))],1.8
    def second_pass(self):
        self.heading('그 결과에, 다음 연결을 적용');self.formula('0.5 × 0.8 = 0.4')
        self.result=txt('도착값 0.4',25,PINK).move_to([2.55,-.9,0])
        return [Succession(self.travel((1,2),'0.5',GOLD),FadeIn(self.result,run_time=.3)),FadeOut(self.value),FadeOut(self.direct),FadeOut(self.directlabel)],1.8
    def product(self):
        self.heading('한 경로 안에서는 곱합니다');self.formula('경로 1 → 2 → 3 : 0.5 × 0.8 = 0.4')
        return [Succession(Indicate(self.net.edges[(0,1)],color=GOLD,scale_factor=1.03),Indicate(self.net.edges[(1,2)],color=GOLD,scale_factor=1.03))],1.8
    def add_four(self):
        self.heading('다른 중간 대상을 거치는 경로');self.formula('1 → 2 → 3     또는     1 → 4 → 3')
        return [FadeOut(self.result),FadeIn(self.net.nodes[3]),Create(self.net.edges[(0,3)]),Create(self.net.edges[(3,2)]),FadeIn(self.net.labels[(0,3)]),FadeIn(self.net.labels[(3,2)])],2
    def other_path(self):
        self.heading('아래 경로에서도 영향을 곱합니다');self.formula('경로 1 → 4 → 3 : 0.2 × 0.3 = 0.06')
        return [Succession(self.travel((0,3),'1',BLUE),self.travel((3,2),'0.2',GREEN))],2.6
    def parallel_paths(self):
        self.heading('같은 출발점 · 같은 목적지');self.formula('위 경로: 0.4     아래 경로: 0.06')
        self.top=txt('0.4',35,GOLD).move_to([-1.05,-3.35,0]);self.bottom=txt('0.06',35,GREEN).move_to([1.05,-3.35,0])
        return [Succession(self.travel((0,1),'1',GOLD),self.travel((1,2),'0.5',GOLD)),Succession(self.travel((0,3),'1',GREEN),self.travel((3,2),'0.2',GREEN)),FadeIn(self.top),FadeIn(self.bottom)],2.6
    def total(self):
        self.heading('여러 경로의 기여는 더합니다');self.formula('1 → 3의 두 단계 영향 = 0.4 + 0.06 = 0.46')
        plus=txt('+',30).move_to([0,-3.35,0]);total=txt('총 0.46',28,PINK).move_to([2.6,-.9,0])
        return [FadeIn(plus),FadeIn(total),Circumscribe(self.net.nodes[2],color=PINK)],1.5
    def twice(self):
        self.clear('같은 관계 A를 두 번 적용','A² = AA     ·     각 원소를 제곱하는 뜻이 아닙니다')
        flow=VGroup(txt('x',43,BLUE),txt('→',36,MUTED),txt('Ax',43,GOLD),txt('→',36,MUTED),txt('A(Ax)',43,PINK)).arrange(RIGHT,buff=.3).move_to(UP*.7)
        equation=txt('A(Ax) = A²x',40).move_to(DOWN*1.5)
        return [FadeIn(flow),FadeIn(equation)],1.6
    def matrix_entry(self):
        self.clear('같은 자리, 새로운 관계','행: 목적지 / 열: 출발점     ·     (A²)₃₁ = 0.46')
        self.ma=matrix4(A,'A · 한 단계').scale(.93).shift(LEFT*2.0)
        self.mb=matrix4(A2,'A² · 두 단계').scale(.93).shift(RIGHT*2.0)
        self.add(self.ma,self.mb)
        return [Circumscribe(self.ma[0][8],color=PINK),Circumscribe(self.mb[0][8],color=PINK)],2
    def sum_formula(self):
        self.clear('한 칸에, 모든 두 단계 경로의 합','(A²)ᵢⱼ = Σₖ Aᵢₖ Aₖⱼ')
        self.net=PathNetwork().scale(.9).shift(UP*.2);self.add(self.net)
        formula=txt('(A²)₃₁ = 0.8 × 0.5 + 0.3 × 0.2',29).move_to(DOWN*3.15)
        return [FadeIn(formula),Indicate(self.net.nodes[0],color=BLUE),Indicate(self.net.nodes[2],color=PINK)],1.8
    def intermediate(self):
        self.heading('k: 중간에 거치는 모든 대상');self.formula('k = 1, 2, 3, 4     ·     이 예에서는 2와 4만 기여')
        return [Circumscribe(self.net.nodes[1],color=GOLD),Circumscribe(self.net.nodes[3],color=GREEN)],2
    def factor_order(self):
        self.clear('출발 j → 중간 k → 도착 i','(A²)ᵢⱼ = Σₖ Aᵢₖ Aₖⱼ')
        flow=VGroup(txt('j',43,BLUE),txt('→',38,MUTED),txt('k',43,GOLD),txt('→',38,MUTED),txt('i',43,PINK)).arrange(RIGHT,buff=.55).move_to(UP*.6)
        first=txt('먼저 Aₖⱼ',28,GOLD).move_to([-1.4,1.7,0]);second=txt('다음 Aᵢₖ',28,PINK).move_to([1.4,1.7,0])
        self.add(flow)
        return [LaggedStart(FadeIn(first),FadeIn(second),lag_ratio=.7)],1.6
    def general(self):
        self.clear('관계가 달라도 이어 붙일 수 있습니다','(BA)ᵢⱼ = Σₖ Bᵢₖ Aₖⱼ')
        flow=VGroup(txt('x',42,BLUE),txt('→',36,MUTED),txt('Ax',42,GOLD),txt('→',36,MUTED),txt('B(Ax)',42,PINK)).arrange(RIGHT,buff=.3).move_to(UP*.5)
        equation=txt('B(Ax) = (BA)x',38).move_to(DOWN*1.3)
        return [FadeIn(flow),FadeIn(equation)],1.6
    def roles(self):
        self.clear('한 경로는 곱하고, 여러 경로는 더한다','A²: 정확히 두 단계인 경로들의 영향')
        first=txt('한 경로의 영향 = 연결들의 곱',32,GOLD).move_to(UP*1)
        second=txt('새 관계의 영향 = 경로들의 합',32,PINK).move_to(DOWN*1)
        return [FadeIn(first),FadeIn(second)],1.3
    def ending(self):
        self.clear('행렬곱: 관계를 이어 붙이는 연산','곱해서 잇고, 더해서 모은다')
        title=txt('두 관계를 거쳐\n새로운 관계로',43).move_to(UP*.7)
        equation=txt('A × A = A²',38,GOLD).move_to(DOWN*1.5)
        return [FadeIn(title),FadeIn(equation)],1.5
