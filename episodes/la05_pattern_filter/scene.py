"""LA05: a mixed input contains eigenpatterns with different gains."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('repeat_visuals',Path(__file__).resolve().parents[1]/'la04_repeated_patterns/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt,matrix=shared.txt,shared.matrix
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
A=shared.A
V1=np.array([1.,2.,1.]);V2=np.array([1.,-1.,1.]);X=V1+V2;Y=A@X
DURATION=99
CAPTIONS=[
(0,'recap','앞에서는 같은 관계를 반복하면,\n어떤 패턴은 두드러지고 어떤 패턴은 작아지는 걸 봤습니다.'),
(6,'viewpoint','이번에는 한 번의 변환 안에서,\n입력에 섞인 패턴들이 어떻게 달라지는지 보겠습니다.'),
(12,'same_matrix','행렬은 앞 편과 같습니다.\n이 하나의 행렬에 서로 다른 패턴을 넣어봅시다.'),
(17,'grow','1, 2, 1이라는 패턴은\n2, 4, 2가 됩니다. 모양은 같고 크기는 2배입니다.'),
(24,'shrink','반면 1, −1, 1이라는 패턴은\n같은 행렬을 지나면 절반 크기로 줄어듭니다.'),
(30,'contrast','같은 행렬인데도 반응은 다릅니다.\n첫 패턴은 키우고, 두 번째 패턴은 줄입니다.'),
(36,'mixed','이제 두 패턴이 섞인 입력을 보겠습니다.\n성분끼리 더하면 2, 1, 2입니다.'),
(42,'split','하나의 입력 안에\n두 가지 모양이 함께 들어 있는 것입니다.'),
(47,'separate','행렬은 이 혼합을 어떻게 바꿀까요?\n각 패턴에 적용한 결과를 다시 더해볼 수 있습니다.'),
(53,'gains','첫 번째 패턴에는 2배,\n두 번째 패턴에는 1/2배가 적용됩니다.'),
(59,'combine','바뀐 두 패턴을 다시 합치면,\n결과는 2.5, 3.5, 2.5입니다.'),
(65,'result','처음에는 가운데가 낮았지만, 이제는 높습니다.\n입력 안의 패턴들이 서로 다른 배율로 바뀌었기 때문입니다.'),
(73,'symbolic','일반적으로도, 섞여 있는 고유벡터 성분에는\n각각의 고유값이 배율로 적용됩니다.'),
(80,'filter','이 관점에서 행렬을 패턴 필터로 볼 수 있습니다.\n어떤 패턴은 강조하고, 어떤 패턴은 억제합니다.'),
(87,'emphasis','각 숫자의 변화만 보면 놓치기 쉽습니다.\n입력 안의 어떤 패턴이 커지고 줄었는지를 봐야 합니다.'),
(93,'ending','하나의 입력, 서로 다른 패턴별 배율.\n행렬의 작용을 읽는 또 하나의 방법입니다.'),
]

class PatternPlot(VGroup):
    """All panels share one fixed value scale; signed components are visible."""
    def __init__(self,values,color,title):
        super().__init__();self.values=np.array(values)
        xs=[-1.12,0,1.12];baseline=-.45;unit=.44
        axes=VGroup(Line([-1.5,baseline,0],[1.5,baseline,0],stroke_color=MUTED,stroke_width=1.3))
        axes.add(txt('0',16,MUTED).move_to([-1.68,baseline,0]))
        for val in [2,4]:axes.add(Line([-1.5,baseline+val*unit,0],[1.5,baseline+val*unit,0],stroke_color=MUTED,stroke_width=.6,stroke_opacity=.2))
        points=[np.array([x,baseline+unit*v,0]) for x,v in zip(xs,values)]
        stems=VGroup(*[Line([x,baseline,0],point,color=color,stroke_width=4,stroke_opacity=.48) for x,point in zip(xs,points)])
        line=VMobject().set_points_as_corners(points).set_stroke(color,3)
        dots=VGroup(*[Dot(p,radius=.065,color=color) for p in points])
        numbers=VGroup(*[txt(f'{v:g}'.replace('-','−'),22,color).move_to(p+UP*(.23 if v>=0 else -.23)) for p,v in zip(points,values)])
        ids=VGroup(*[txt(str(i+1),18,MUTED).move_to([x,-1.45,0]) for i,x in enumerate(xs)])
        title_obj=txt(title,27,color,width=3.3).move_to([0,2.05,0])
        self.add(axes,stems,line,dots,numbers,ids,title_obj)

class PatternFilter(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   05',19,MUTED).move_to(UP*7),txt('같은 입력, 다른 패턴별 배율',35).move_to(UP*6.05))
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
    def panels(self,left,right,left_title,right_title,left_color=GOLD,right_color=PINK):
        self.left=PatternPlot(left,left_color,left_title).shift(LEFT*2)
        self.right=PatternPlot(right,right_color,right_title).shift(RIGHT*2)
        self.add(txt('가로: 성분 1, 2, 3   /   세로: 값',19,MUTED).move_to(DOWN*2.65))
        return [FadeIn(self.left),FadeIn(self.right)],1.5
    def recap(self):
        self.heading('반복 속에서 두드러지는 패턴');self.formula('어떤 패턴은 성장하고, 어떤 패턴은 감소합니다')
        one=txt('× 2',54,GOLD).move_to([-2,1,0]);two=txt('× 1/2',50,PINK).move_to([2,1,0])
        labels=VGroup(txt('강조',28,GOLD).move_to([-2,-.5,0]),txt('억제',28,PINK).move_to([2,-.5,0]))
        return [FadeIn(one),FadeIn(two),FadeIn(labels)],1.3
    def viewpoint(self):
        self.clear('이번에는, 한 번의 변환을 들여다봅니다','한 입력 안에 섞인 패턴들이 어떻게 달라질까?')
        flow=VGroup(txt('입력',34,BLUE),txt('→',35,MUTED),txt('A',52,INK),txt('→',35,MUTED),txt('결과',34,BLUE)).arrange(RIGHT,buff=.4)
        return [FadeIn(flow)],1.3
    def same_matrix(self):
        self.clear('앞 편과 같은 하나의 행렬 A','패턴에 따라 서로 다른 반응')
        return [FadeIn(matrix())],1.2
    def grow(self):
        self.clear('첫 패턴은 2배로 커집니다','v₁ = (1, 2, 1)     →     Av₁ = 2v₁')
        return self.panels(V1,2*V1,'입력 v₁','결과 2v₁',GOLD,GOLD)
    def shrink(self):
        self.clear('두 번째 패턴은 절반으로 줄어듭니다','v₂ = (1, −1, 1)     →     Av₂ = (1/2)v₂')
        return self.panels(V2,.5*V2,'입력 v₂','결과 (1/2)v₂',PINK,PINK)
    def contrast(self):
        self.clear('같은 A · 다른 패턴 · 다른 배율','이 두 패턴은 A의 고유벡터입니다')
        a=VGroup(txt('v₁',43,GOLD),txt('→',32,MUTED),txt('2v₁',43,GOLD)).arrange(RIGHT,buff=.6).move_to(UP*1.5)
        b=VGroup(txt('v₂',43,PINK),txt('→',32,MUTED),txt('(1/2)v₂',43,PINK)).arrange(RIGHT,buff=.6).move_to(DOWN*.8)
        return [FadeIn(a),FadeIn(b)],1.3
    def mixed(self):
        self.clear('두 패턴이 섞인 하나의 입력','x = v₁ + v₂ = (2, 1, 2)')
        self.inputplot=PatternPlot(X,BLUE,'혼합 입력 x').scale(1.2).shift(UP*.1)
        return [FadeIn(self.inputplot)],1.5
    def split(self):
        self.heading('하나의 입력을, 두 패턴으로 보기');self.formula('(1, 2, 1) + (1, −1, 1) = (2, 1, 2)')
        self.left=PatternPlot(V1,GOLD,'패턴 v₁').shift(LEFT*2)
        self.right=PatternPlot(V2,PINK,'패턴 v₂').shift(RIGHT*2)
        return [Succession(FadeOut(self.inputplot,scale=.9,run_time=.45),AnimationGroup(FadeIn(self.left,shift=RIGHT*.7),FadeIn(self.right,shift=LEFT*.7),run_time=1.15))],1.6
    def separate(self):
        self.heading('섞어서 적용해도, 따로 적용해 더해도');self.formula('A(v₁ + v₂) = Av₁ + Av₂     ·     선형성')
        self.plus=txt('+',33,INK).move_to(DOWN*2.5)
        self.add(self.plus)
        return [Circumscribe(self.left,color=GOLD),Circumscribe(self.right,color=PINK)],1.8
    def gains(self):
        self.heading('입력 안의 패턴마다 다른 배율');self.formula('v₁ → 2v₁     ·     v₂ → (1/2)v₂')
        newleft=PatternPlot(2*V1,GOLD,'강조 · ×2').shift(LEFT*2)
        newright=PatternPlot(.5*V2,PINK,'억제 · ×1/2').shift(RIGHT*2)
        return [Transform(self.left,newleft),Transform(self.right,newright)],2
    def combine(self):
        self.heading('바뀐 패턴들을 다시 합치면');self.formula('Ax = 2v₁ + (1/2)v₂ = (2.5, 3.5, 2.5)')
        self.outputplot=PatternPlot(Y,BLUE,'합쳐진 결과 Ax').scale(1.2).shift(UP*.1)
        return [Succession(AnimationGroup(FadeOut(self.plus),FadeOut(self.left,shift=RIGHT*.6),FadeOut(self.right,shift=LEFT*.6),run_time=.65),FadeIn(self.outputplot,scale=.92,run_time=.95))],1.6
    def result(self):
        self.clear('다르게 조절된 패턴이, 다른 모양을 만듭니다','동일한 세로 눈금으로 비교 · 가운데의 변화에 주목')
        return self.panels(X,Y,'입력 x','결과 Ax',BLUE,BLUE)
    def symbolic(self):
        self.clear('고유벡터 성분마다, 고유값만큼','Av₁ = λ₁v₁     ·     Av₂ = λ₂v₂')
        self.expr1=txt('x = c₁v₁ + c₂v₂',38).move_to(UP*1.6)
        self.expr2=txt('Ax = c₁λ₁v₁ + c₂λ₂v₂',36).move_to(DOWN*.4)
        note=txt('이 예: c₁ = c₂ = 1, λ₁ = 2, λ₂ = 1/2',25,MUTED).move_to(DOWN*2.35)
        return [FadeIn(self.expr1),FadeIn(self.expr2),FadeIn(note)],1.6
    def filter(self):
        self.clear('패턴 필터로 읽는 행렬','한 입력 안에서, 어떤 패턴은 강조하고 다른 패턴은 억제')
        self.left=PatternPlot(V1,GOLD,'v₁ 성분: ×2').scale(.85).move_to([-2,1.3,0])
        self.right=PatternPlot(V2,PINK,'v₂ 성분: ×1/2').scale(.85).move_to([2,1.3,0])
        bottom=txt('패턴별 배율이 달라집니다',34).move_to(DOWN*2.2)
        return [FadeIn(self.left),FadeIn(self.right),FadeIn(bottom)],1.5
    def emphasis(self):
        self.clear('숫자 변화 뒤에 있는, 패턴의 변화','첫 패턴의 계수: 1 → 2     /     두 번째 패턴의 계수: 1 → 1/2')
        title=txt('한 입력에 섞인 패턴들을',35).move_to(UP*1.4)
        words=VGroup(txt('강조',46,GOLD),txt('또는',28,MUTED),txt('억제',46,PINK)).arrange(RIGHT,buff=.45).move_to(DOWN*.3)
        return [FadeIn(title),FadeIn(words)],1.3
    def ending(self):
        self.clear('하나의 입력, 서로 다른 패턴별 배율','행렬을 이해하는 또 하나의 관점')
        main=txt('어떤 패턴을 키우고,\n어떤 패턴을 줄이는가',40).move_to(UP*.5)
        return [FadeIn(main)],1.3
