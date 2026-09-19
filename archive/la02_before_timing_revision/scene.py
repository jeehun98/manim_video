"""LA02: each output sums weighted contributions from every input."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *

spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
txt,RelationTable,Network=shared.txt,shared.RelationTable,shared.Network
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
COLORS=shared.COLORS
A=np.array(shared.VALUES)
X=np.array([10.,5.,20.])
Y=A@X
DURATION=120
CAPTIONS=[
(0,'recap','앞에서 행렬은 대상 사이의 관계를\n숫자로 기록하는 방법이라고 했습니다.'),
(6,'values','이제 세 대상에 실제 값을 넣어봅시다.\n현재 값은 각각 십, 오, 이십입니다.'),
(12,'destination','먼저 첫 번째 대상에 들어오는\n기여만 모아보겠습니다.'),
(18,'second','두 번째 대상의 값은 오.\n첫 번째에게 주는 영향은 영 점 팔입니다.'),
(25,'multiply','따라서 이 연결이 만드는 기여는\n영 점 팔 곱하기 오, 즉 사입니다.'),
(32,'third','세 번째 대상에서도 값이 들어옵니다.\n영 점 일 곱하기 이십, 즉 이만큼 기여합니다.'),
(40,'arrive','출발점은 다르지만 목적지는 같습니다.\n같은 곳에 도착한 기여들을 더합니다.'),
(47,'sum','사 더하기 이는 육.\n이것이 첫 번째 대상의 결과입니다.'),
(53,'zero','자기 자신에게서 오는 기여도 포함하면,\n영 곱하기 십 더하기 사 더하기 이입니다.'),
(60,'symbolic','숫자 대신 기호로 적어도 같습니다.\n각 출발점의 값에 연결의 크기를 곱하고,\n그 기여들을 모두 더합니다.'),
(69,'roles','곱셈은 연결마다 기여를 만들고,\n덧셈은 같은 목적지의 기여를 모읍니다.'),
(76,'second_output','두 번째 대상도 똑같습니다.\n같은 입력값에서 오는 기여를 더하면 십삼입니다.'),
(83,'third_output','세 번째 대상은 오 점 오.\n목적지마다 기여를 모아 결과를 하나씩 얻습니다.'),
(90,'all_outputs','이 계산을 한 번에 적으면,\ny = Ax입니다.'),
(97,'interpret','행렬은 관계, 벡터는 현재 값.\n행렬과 벡터의 곱은 관계를 반영한 결과입니다.'),
(105,'row_meaning','행렬의 한 행은 한 목적지를 봅니다.\n그 행과 입력 벡터를 곱해 더하면,\n그 목적지의 결과 하나가 나옵니다.'),
(113,'ending','행렬과 벡터의 곱.\n핵심은 여러 출발점에서 온 기여의 총합입니다.'),
]

def column(values,color=INK,size=34):
    entries=VGroup(*[txt(f'{v:g}' if isinstance(v,(int,float,np.floating)) else v,size,color) for v in values]).arrange(DOWN,buff=.37)
    h=entries.height+.32;w=entries.width+.48
    brackets=VGroup(*[VMobject().set_points_as_corners([[s*(w/2-.13),h/2,0],[s*w/2,h/2,0],[s*w/2,-h/2,0],[s*(w/2-.13),-h/2,0]]).set_stroke(INK,2) for s in [-1,1]])
    return VGroup(entries,brackets)

class MatrixVectorProduct(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   02',19,MUTED).move_to(UP*7),txt('기여를 모으면 결과가 된다',37).move_to(UP*6.05))
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
    def flow_board(self,target=0):
        self.target=target
        self.sources=VGroup();self.edges=VGroup();self.weights=VGroup();self.terms=VGroup()
        for j in range(3):
            y=2.1-2.1*j
            box=RoundedRectangle(width=1.6,height=1.12,corner_radius=.15,color=COLORS[j],fill_color=COLORS[j],fill_opacity=.09,stroke_width=2).move_to([-2.65,y,0])
            value=txt(f'x{["₁","₂","₃"][j]} = {X[j]:g}',27,COLORS[j]).move_to(box)
            self.sources.add(VGroup(box,value))
            edge=Arrow([-1.77,y,0],[1.53,0,0],buff=.06,color=COLORS[j],stroke_width=3,tip_length=.15)
            weight=txt(f'× {A[target,j]:g}',25,COLORS[j]).move_to([-.9,y*.7+.52,0])
            weight.add_background_rectangle(color=shared.config.background_color,opacity=1,buff=.05)
            self.edges.add(edge);self.weights.add(weight)
            term=txt(f'{A[target,j]*X[j]:g}',36,COLORS[j]).move_to([(j-1)*1.65,-3.35,0])
            self.terms.add(term)
        circle=Circle(radius=.63,color=COLORS[target],stroke_width=3,fill_color=shared.config.background_color,fill_opacity=1).move_to([2.2,0,0])
        self.answer=txt('?',40,COLORS[target]).move_to(circle)
        self.dest=VGroup(circle,self.answer,txt(f'받는 대상 {target+1}',23,COLORS[target]).move_to([2.2,1.15,0]))
        self.add(self.sources,self.dest)
        self.add(txt('현재 값 x · 고정',22,MUTED).move_to([-2.55,3.25,0]))
    def recap(self):
        self.heading('관계를 기록한 행렬');self.formula('행: 받는 대상    ·    열: 주는 대상')
        self.table=RelationTable().scale(1.2)
        return [FadeIn(self.table)],1.5
    def values(self):
        self.clear('관계 안으로 실제 값이 들어옵니다','x₁ = 10     x₂ = 5     x₃ = 20')
        self.net=Network().scale(.95)
        labels=VGroup(*[txt(f'x{["₁","₂","₃"][i]} = {X[i]:g}',27,COLORS[i]).next_to(node,UP if i==0 else DOWN,buff=.2) for i,node in enumerate(self.net.nodes)])
        return [FadeIn(self.net),FadeIn(labels)],2
    def destination(self):
        self.clear('첫 번째 목적지로 모아보기','왼쪽: 출발점의 현재 값     오른쪽: 계산 결과')
        self.flow_board()
        return [],0
    def second(self):
        self.heading('출발점 2 → 목적지 1');self.formula('연결의 크기 0.8 × 출발점의 값 5')
        return [GrowArrow(self.edges[1]),FadeIn(self.weights[1])],1.8
    def moving_contribution(self,j):
        token=txt(f'{A[self.target,j]*X[j]:g}',26,COLORS[j]).move_to(self.edges[j].get_start())
        token.add_background_rectangle(color=shared.config.background_color,opacity=1,buff=.08)
        return Succession(FadeIn(token,run_time=.15),MoveAlongPath(token,self.edges[j],run_time=1.4),FadeOut(token,run_time=.15))
    def multiply(self):
        self.heading('곱셈이 기여 하나를 만듭니다');self.formula('0.8 × 5 = 4')
        return [self.moving_contribution(1),FadeIn(self.terms[1])],2.2
    def third(self):
        self.heading('출발점 3에서도 기여가 옵니다');self.formula('0.1 × 20 = 2')
        return [Succession(AnimationGroup(GrowArrow(self.edges[2]),FadeIn(self.weights[2]),run_time=1),self.moving_contribution(2),FadeIn(self.terms[2],run_time=.4))],3
    def arrive(self):
        self.heading('서로 다른 출발점 · 같은 목적지');self.formula('같은 목적지로 들어온 기여를 더하기')
        plus=txt('+',32).move_to([.82,-3.35,0]);self.add(plus)
        return [self.moving_contribution(1),self.moving_contribution(2),Indicate(self.terms[1],color=GOLD),Indicate(self.terms[2],color=PINK)],2.2
    def sum(self):
        self.heading('첫 번째 결과는 두 기여의 합');self.formula('y₁ = 4 + 2 = 6')
        return [Transform(self.answer,txt('6',40,BLUE).move_to(self.answer)),Circumscribe(self.dest[0],color=BLUE)],1.8
    def zero(self):
        self.heading('모든 출발점의 기여를 포함하면');self.formula('y₁ = 0 × 10 + 0.8 × 5 + 0.1 × 20 = 6')
        self.edges[0].set_stroke(opacity=.35);self.edges[0].get_tip().set_opacity(.35)
        plus=txt('+',32).move_to([-.82,-3.35,0])
        return [GrowArrow(self.edges[0]),FadeIn(self.weights[0]),FadeIn(self.terms[0]),FadeIn(plus)],1.8
    def symbolic(self):
        self.clear('각 연결의 기여를, 같은 목적지로','y₁ = A₁₁x₁ + A₁₂x₂ + A₁₃x₃')
        terms=VGroup(*[txt(s,34,COLORS[i]) for i,s in enumerate(['A₁₁ × x₁','A₁₂ × x₂','A₁₃ × x₃'])]).arrange(DOWN,buff=.75).move_to(LEFT*1.8)
        labels=VGroup(*[txt(f'출발점 {i+1}',20,MUTED).next_to(t,LEFT,buff=.2) for i,t in enumerate(terms)])
        dest=VGroup(Circle(radius=.6,color=BLUE),txt('y₁',36,BLUE)).move_to(RIGHT*2.25)
        arrows=VGroup(*[Arrow(t.get_right()+RIGHT*.1,dest.get_left(),buff=.1,color=COLORS[i],stroke_width=2) for i,t in enumerate(terms)])
        gather=txt('모두 더하기',24).move_to([1.7,1.7,0])
        self.symbols=VGroup(terms,labels,dest,arrows,gather)
        return [FadeIn(terms),FadeIn(labels),FadeIn(dest),Create(arrows),FadeIn(gather)],2.5
    def roles(self):
        self.heading('곱해서 만들고, 더해서 모읍니다');self.formula('곱셈: 연결별 기여     ·     덧셈: 목적지별 총합')
        return [Indicate(self.symbols[0],scale_factor=1.03,color=INK),Circumscribe(self.symbols[2],color=BLUE)],2
    def output_board(self,target):
        self.clear(f'{target+1}번째 목적지도 같은 계산','모든 결과는 같은 입력 x = (10, 5, 20)에서 계산')
        self.flow_board(target)
        self.add(self.edges,self.weights,self.terms)
        self.add(*[txt('+',32).move_to([x,-3.35,0]) for x in [-.82,.82]])
        return [LaggedStart(*[self.moving_contribution(j) for j in range(3) if A[target,j]!=0],lag_ratio=.3),Transform(self.answer,txt(f'{Y[target]:g}',36,COLORS[target]).move_to(self.answer))],2.6
    def second_output(self):
        animations,duration=self.output_board(1)
        self.formula('y₂ = 0.3 × 10 + 0 × 5 + 0.5 × 20 = 13')
        return animations,duration
    def third_output(self):
        animations,duration=self.output_board(2)
        self.formula('y₃ = 0.2 × 10 + 0.7 × 5 + 0 × 20 = 5.5')
        return animations,duration
    def all_outputs(self):
        self.clear('한 번에 적으면  y = Ax','관계 A × 현재 값 x = 목적지별 기여의 총합 y')
        self.table=RelationTable().scale(.92);self.table.labels.set_opacity(0)
        # Align by cells, since invisible row/column headings remain in bounds.
        self.table.shift(np.array([-1.9,.3,0])-self.table.cells.get_center())
        self.xcol=column(X,INK,32).move_to([.8,.3,0]);self.ycol=column(Y,INK,32).move_to([2.85,.3,0])
        self.add(txt('×',28,MUTED).move_to([-.15,.3,0]),txt('=',28,MUTED).move_to([1.7,.3,0]))
        self.names=VGroup(txt('A · 관계',26,GOLD).move_to([-1.9,2.25,0]),txt('x · 현재 값',22,BLUE).move_to([.5,-2.2,0]),txt('y · 결과',22,PINK).move_to([2.85,-2.2,0]))
        return [FadeIn(self.table),FadeIn(self.xcol),FadeIn(self.ycol),FadeIn(self.names)],2
    def interpret(self):
        self.heading('관계 × 현재 값 → 결과');self.formula('입력값은 그대로 두고, 목적지마다 기여를 합산')
        return [LaggedStart(*[Indicate(m,color=c,scale_factor=1.05) for m,c in [(self.table.entries,GOLD),(self.xcol,BLUE),(self.ycol,PINK)]],lag_ratio=.5)],3
    def row_meaning(self):
        self.heading('한 행이, 한 목적지의 결과를 만듭니다');self.formula('첫 번째 행 · 입력 벡터 → 첫 번째 결과 6')
        return [Circumscribe(VGroup(*self.table.cells[:3]),color=BLUE),Circumscribe(self.xcol,color=BLUE),Circumscribe(self.ycol[0][0],color=BLUE)],2.5
    def ending(self):
        self.clear('핵심: 여러 출발점의 기여를 더한다','행렬과 벡터의 곱  y = Ax')
        title=txt('한 목적지의 결과',38,BLUE).move_to(UP*1.8)
        eq=txt('=',42).move_to(UP*.5)
        body=txt('모든 출발점에서 온\n기여의 총합',40).move_to(DOWN*.9)
        return [FadeIn(title),FadeIn(eq),FadeIn(body)],1.5
