"""LA04: repeated application, scale-normalized shape, and an eigenvector hint."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
COLORS=[BLUE,GOLD,PINK]
A=np.array([[1.,.5,0],[.5,1.5,.5],[0,.5,1.]])
X=np.array([4.,3.,2.]);V=np.array([1.,2.,1.]);W=np.array([1.,0.,-1.]);Z=np.array([1.,-1.,1.])
DURATION=110
CAPTIONS=[
(0,'recap','앞에서는 관계를 두 번 통과하면,\n간접적인 관계가 만들어질 수 있다는 걸 봤습니다.'),
(6,'repeat','이번에는 같은 관계를 계속 반복합니다.\nx, Ax, A²x, A³x로 이어집니다.'),
(12,'matrix_intro','반복할 행렬을 새로 정하겠습니다.\n이 관계를 매번 똑같이 적용합니다.'),
(17,'initial','처음 값은 4, 3, 2.\n왼쪽은 실제 값, 오른쪽은 각 값의 비중입니다.'),
(23,'once','한 번 적용하면 값이 달라집니다.\n비중은 전체 합을 100%로 맞춰 비교합니다.'),
(29,'twice','한 번 더 적용하면,\n같은 관계망 안에서 값이 다시 전달되고 섞입니다.'),
(35,'four_times','여러 번 반복하면, 값의 크기뿐 아니라\n서로의 비율에도 변화가 나타납니다.'),
(41,'eight_times','이 예에서는 값은 계속 커지지만,\n비율은 점점 1:2:1에 가까워집니다.'),
(48,'shape','숫자가 같아지는 것은 아닙니다.\n전체 크기를 맞춰 보면 모양이 가까워지는 것입니다.'),
(54,'special','이번에는 처음부터\n1, 2, 1이라는 패턴을 넣어봅시다.'),
(59,'double','한 번 적용하면 2, 4, 2.\n다시 적용하면 4, 8, 4가 됩니다.'),
(66,'same_ratio','전체 크기는 2배씩 커지지만,\n1:2:1이라는 비율은 그대로입니다.'),
(72,'different_patterns','모든 패턴이 이렇게 커지는 것은 아닙니다.\n이 행렬에도 그대로 남거나 작아지는 패턴이 있습니다.'),
(79,'decay','예를 들어 1, −1, 1은\n적용할 때마다 절반으로 줄어듭니다.'),
(85,'relative','처음 상태에 여러 패턴이 섞여 있다면,\n더 빠르게 커지는 패턴이 상대적으로 두드러질 수 있습니다.'),
(92,'condition','물론 모든 행렬과 초기값에서\n이처럼 하나의 비율로 모이는 것은 아닙니다.'),
(98,'hint','변환해도 상수배로만 바뀌는 벡터,\n그리고 그 크기를 바꾸는 배율.\n고유벡터와 고유값으로 이어지는 단서입니다.'),
(105,'ending','반복되는 관계 속에서,\n어떤 패턴이 남는가를 보는 것입니다.'),
]

def vector(values,size=33):
    entries=VGroup(*[txt(str(v),size,COLORS[i]) for i,v in enumerate(values)]).arrange(DOWN,buff=.25)
    h=entries.height+.3;w=entries.width+.45
    brackets=VGroup(*[VMobject().set_points_as_corners([[s*(w/2-.12),h/2,0],[s*w/2,h/2,0],[s*w/2,-h/2,0],[s*(w/2-.12),-h/2,0]]).set_stroke(INK,2) for s in [-1,1]])
    return VGroup(entries,brackets)

def matrix():
    entries=VGroup(*[txt(f'{A[i,j]:g}',32,COLORS[j]).move_to([(j-1)*1.1,(1-i)*.85,0]) for i in range(3) for j in range(3)])
    brackets=VGroup(*[VMobject().set_points_as_corners([[s*1.55,1.25,0],[s*1.7,1.25,0],[s*1.7,-1.25,0],[s*1.55,-1.25,0]]).set_stroke(INK,2) for s in [-1,1]])
    return VGroup(entries,brackets)

class RepeatedPatterns(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   04',19,MUTED).move_to(UP*7),txt('반복하면 어떤 패턴이 남을까?',35).move_to(UP*6.05))
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
        self.heading('관계를 두 번 잇는 계산');self.formula('A(Ax) = A²x')
        flow=VGroup(txt('x',47,BLUE),txt('→',38,MUTED),txt('Ax',47,GOLD),txt('→',38,MUTED),txt('A²x',47,PINK)).arrange(RIGHT,buff=.35).move_to(UP*.5)
        return [FadeIn(flow)],1.3
    def repeat(self):
        self.clear('같은 관계를 계속 통과하면','Aⁿx : 같은 행렬 A를 n번 적용한 결과')
        self.chain=VGroup(*[txt(s,38,c) for s,c in [('x',BLUE),('→',MUTED),('Ax',GOLD),('→',MUTED),('A²x',PINK),('→',MUTED),('A³x',INK)]]).arrange(RIGHT,buff=.22)
        if self.chain.width>7.5:self.chain.scale_to_fit_width(7.5)
        return [LaggedStart(*[FadeIn(m) for m in self.chain],lag_ratio=.15)],2
    def matrix_intro(self):
        self.clear('이번 편의 새로운 관계 A','자기 자신에게 주는 영향도 포함한 예시')
        self.mat=matrix().move_to(UP*.3)
        return [FadeIn(self.mat)],1.3
    def state(self,n):return np.linalg.matrix_power(A,n)@X
    def display_vector(self,n):
        vals=self.state(n)
        return vector([f'{v:.3f}'.rstrip('0').rstrip('.') for v in vals],29).move_to([-2.55,.1,0])
    def bar(self,j,ratio):
        h=max(.008,4*ratio)
        return Rectangle(width=.7,height=h,stroke_width=0,fill_color=COLORS[j],fill_opacity=.85).move_to([.3+j*1.15,-1.45+h/2,0])
    def proportion(self,j,ratio):return txt(f'{ratio*100:.1f}%',23,COLORS[j]).move_to([.3+j*1.15,-1.45+4*ratio+.35,0])
    def initial(self):
        self.clear('초기 상태 · n = 0','오른쪽은 비교용 비중: 각 값 ÷ 전체 합')
        self.raw=self.display_vector(0);ratios=self.state(0)/self.state(0).sum()
        self.bars=VGroup(*[self.bar(i,r) for i,r in enumerate(ratios)])
        self.percents=VGroup(*[self.proportion(i,r) for i,r in enumerate(ratios)])
        labels=VGroup(txt('실제 값 Aⁿx',25).move_to([-2.55,2.7,0]),txt('합계 100%로 비교',25).move_to([1.45,2.7,0]),txt('값 표시는 소수 셋째 자리 반올림',17,MUTED).move_to([-2.2,-3.1,0]))
        axis=Line([-.15,-1.45,0],[3.2,-1.45,0],color=MUTED,stroke_width=1)
        ids=VGroup(*[txt(str(i+1),22,COLORS[i]).move_to([.3+i*1.15,-1.85,0]) for i in range(3)])
        self.add(labels,axis,ids)
        return [FadeIn(self.raw),FadeIn(self.bars),FadeIn(self.percents)],1.6
    def step(self,n):
        self.heading(f'같은 A를 {n}번 적용 · n = {n}')
        ratios=self.state(n)/self.state(n).sum()
        return [Transform(self.raw,self.display_vector(n)),*[Transform(self.bars[i],self.bar(i,r)) for i,r in enumerate(ratios)],*[Transform(self.percents[i],self.proportion(i,r)) for i,r in enumerate(ratios)]],1.8
    def once(self):return self.step(1)
    def twice(self):return self.step(2)
    def four_times(self):
        anim,seconds=self.step(4);self.formula('반복 횟수를 늘려, 크기와 비율을 함께 관찰')
        return anim,seconds
    def eight_times(self):
        anim,seconds=self.step(8);self.formula('비중은 25% : 50% : 25%에 가까워집니다')
        return anim,seconds
    def shape(self):
        self.heading('커지는 값 · 가까워지는 모양');self.formula('1 : 2 : 1     ↔     25% : 50% : 25%')
        guides=VGroup(*[DashedLine([.3+i*1.15-.43,-1.45+4*r,0],[.3+i*1.15+.43,-1.45+4*r,0],color=INK,stroke_width=2,dash_length=.09) for i,r in enumerate([.25,.5,.25])])
        return [Create(guides)],1.2
    def special(self):
        self.clear('처음부터 이 패턴을 넣으면?','v = (1, 2, 1)')
        self.v1=vector([1,2,1],40).move_to(LEFT*2.65)
        self.add(txt('v',28,BLUE).next_to(self.v1,UP,buff=.45))
        return [FadeIn(self.v1)],1.2
    def double(self):
        self.heading('한 번 지날 때마다, 전체가 2배');self.formula('Av = 2v     ·     A²v = 4v')
        self.v2=vector([2,4,2],40).move_to(ORIGIN);self.v3=vector([4,8,4],40).move_to(RIGHT*2.65)
        arrows=VGroup(txt('→',32,MUTED).move_to(LEFT*1.35),txt('→',32,MUTED).move_to(RIGHT*1.35))
        labels=VGroup(txt('A 적용',20,MUTED).move_to([-1.35,.65,0]),txt('A 적용',20,MUTED).move_to([1.35,.65,0]))
        return [Succession(AnimationGroup(FadeIn(arrows[0]),FadeIn(labels[0]),TransformFromCopy(self.v1,self.v2),run_time=1.3),AnimationGroup(FadeIn(arrows[1]),FadeIn(labels[1]),TransformFromCopy(self.v2,self.v3),run_time=1.3))],2.6
    def same_ratio(self):
        self.heading('숫자는 커져도, 비율은 그대로');self.formula('1 : 2 : 1 = 2 : 4 : 2 = 4 : 8 : 4')
        ratios=VGroup(*[txt('1 : 2 : 1',23,PINK).move_to([x,-2.2,0]) for x in [-2.65,0,2.65]])
        return [FadeIn(ratios)],1.2
    def different_patterns(self):
        self.clear('이 행렬이 각 패턴에 하는 일','A를 한 번 적용했을 때의 배율')
        self.patterns=VGroup()
        for name,y,values,label,color in [('v',2,[1,2,1],'2배 · 성장',GOLD),('w',0,[1,0,-1],'1배 · 유지',BLUE),('z',-2,[1,-1,1],'1/2배 · 감소',PINK)]:
            v=vector(values,25).move_to([-2,y,0]);desc=txt(label,29,color).move_to([1.1,y,0]);name_label=txt(name+' =',24,color).move_to([-3.1,y,0]);self.patterns.add(VGroup(name_label,v,desc))
        return [LaggedStart(*[FadeIn(m) for m in self.patterns],lag_ratio=.25)],1.8
    def decay(self):
        self.clear('작아지는 패턴도 있습니다','Az = (1/2)z     ·     z = (1, −1, 1)')
        self.small=vector([1,'−1',1],37).move_to(LEFT*2.5);self.half=vector(['0.5','−0.5','0.5'],37).move_to(RIGHT*2.1)
        self.add(self.small,txt('A',25,PINK).move_to([0,.7,0]),txt('→',35,MUTED))
        return [TransformFromCopy(self.small,self.half)],1.5
    def relative(self):
        self.clear('빠르게 커지는 패턴이 상대적으로 남는다','이 예의 초기값: x = 2v + w + z')
        expr=txt('Aⁿx = 2·2ⁿv + w + (1/2)ⁿz',32).move_to(UP*1.5)
        labels=VGroup(txt('성장',29,GOLD),txt('유지',29,BLUE),txt('감소',29,PINK)).arrange(RIGHT,buff=1.05).move_to(DOWN*.1)
        desc=txt('크기를 맞춰 비교하면 v의 모양이 두드러집니다',25,MUTED).move_to(DOWN*2)
        return [FadeIn(expr),FadeIn(labels),FadeIn(desc)],1.5
    def condition(self):
        self.clear('항상 같은 모양으로 모이는 것은 아닙니다','반복의 결과는 행렬과 초기 상태에 따라 달라집니다')
        text=txt('비율이 가까워질 수도,\n방향이 계속 달라질 수도 있습니다',34).move_to(UP*.5)
        return [FadeIn(text)],1.2
    def hint(self):
        self.clear('모양을 보존하는 패턴의 이름','이번 예: v = (1, 2, 1), λ = 2')
        eq=txt('Av = λv',55).move_to(UP*1.5)
        names=VGroup(txt('v  ·  고유벡터',30,BLUE),txt('λ  ·  고유값',30,GOLD)).arrange(DOWN,buff=.5).move_to(DOWN*.6)
        return [FadeIn(eq),FadeIn(names)],1.5
    def ending(self):
        self.clear('반복 속에서 남는 패턴을 본다','Aⁿx     ·     다음 이야기: 고유벡터와 고유값')
        title=txt('어떤 모양은 바뀌지 않고,\n크기만 달라진다',39).move_to(UP*.5)
        return [FadeIn(title)],1.2
