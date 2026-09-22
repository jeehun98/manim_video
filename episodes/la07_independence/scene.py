"""LA07: redundant coefficients, cancellation, and independent degrees of freedom."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
DURATION=108
CAPTIONS=[
(0,'opening','벡터 두 개를 조합해\n하나의 점을 표현한다고 해봅시다.'),
(5,'weights','a와 b는 각 벡터를\n얼마나 사용할지 정하는 계수입니다.'),
(10,'dependent','그런데 두 번째 벡터가 첫 번째의 2배라면,\n벡터는 두 개여도 같은 방향만 가리킵니다.'),
(16,'two_ways','같은 점을 첫 벡터의 2배로도,\n두 번째 벡터의 1배로도 만들 수 있습니다.'),
(23,'sliding','계수를 이렇게 바꿔도 결과는 움직이지 않습니다.\n표현이 하나로 정해지지 않는 겁니다.'),
(30,'cancellation','그 이유는 2v₁ − v₂ = 0.\n0이 아닌 계수들로도 서로를 상쇄할 수 있기 때문입니다.'),
(37,'freedom','두 번째 벡터를 추가했지만, 갈 수 있는 곳은\n여전히 한 직선입니다. 새로운 자유도는 없습니다.'),
(43,'new_direction','이번에는 두 번째 벡터를\n같은 직선 밖의 방향으로 바꿔보겠습니다.'),
(49,'plane','이제 가로와 세로를 따로 조절할 수 있습니다.\n두 개의 독립적인 자유도가 생깁니다.'),
(55,'unique_point','예를 들어 이 점을 만들려면,\na는 2, b는 1이어야 합니다.'),
(61,'change_a','a를 바꾸면 가로 위치가 달라집니다.\n이 차이를 b로 대신할 수 있을까요?'),
(67,'try_cancel','b를 아무리 바꿔도 세로로만 움직입니다.\n가로에서 생긴 차이를 완전히 지울 수 없습니다.'),
(74,'zero_relation','원점으로 돌아오는 경우도 마찬가지입니다.\na와 b가 모두 0일 때만 조합이 0이 됩니다.'),
(81,'independent','이런 벡터들을 선형독립이라고 합니다.\n서로 대체할 수 없는 방향을 제공하는 것입니다.'),
(87,'uniqueness','만약 같은 점의 표현이 두 개라면,\n두 표현을 뺀 것이 0을 만드는 상쇄 관계가 됩니다.'),
(94,'only_zero','독립인 벡터에는 그런 상쇄가 없으므로,\n두 표현의 계수 차이도 모두 0이어야 합니다.'),
(101,'ending','새로운 자유도, 숨겨진 상쇄가 없음,\n표현의 유일성. 같은 구조를 보는 세 가지 관점입니다.'),
]

class Independence(Scene):
    origin=np.array([-1.1,-.65,0.]);unit=.9
    def p(self,v):return self.origin+self.unit*np.array([v[0],v[1],0])
    def arrow(self,v,color,start=(0,0),width=4):
        v=np.asarray(v);start=np.asarray(start)
        if np.linalg.norm(v)<.015:return VGroup(Dot(self.p(start),radius=.04,color=color))
        return VGroup(Arrow(self.p(start),self.p(start+v),buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.16))
    def grid(self):
        g=VGroup()
        for x in range(-2,6):g.add(Line(self.p((x,-2)),self.p((x,3)),color=MUTED,stroke_width=1 if x==0 else .7,stroke_opacity=.5 if x==0 else .18))
        for y in range(-2,4):g.add(Line(self.p((-2,y)),self.p((5,y)),color=MUTED,stroke_width=1 if y==0 else .7,stroke_opacity=.5 if y==0 else .18))
        return g
    def board(self):self.add(self.grid(),Dot(self.origin,radius=.04,color=INK))
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   07',19,MUTED).move_to(UP*7),txt('벡터가 늘면 자유도도 늘까?',36).move_to(UP*6.05))
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
    def opening(self):
        self.heading('두 벡터로 하나의 점을 표현하기');self.formula('벡터는 재료, 계수는 사용하는 양')
        eq=txt('x = av₁ + bv₂',49).move_to(UP*.5)
        return [FadeIn(eq)],1.3
    def weights(self):
        self.clear('계수 두 개로 결과를 정합니다','a, b를 바꾸면 조합도 달라집니다')
        line1=txt('a × v₁',43,BLUE).move_to([-1.9,.7,0]);line2=txt('b × v₂',43,GOLD).move_to([1.9,.7,0]);plus=txt('+',35).move_to([0,.7,0])
        return [FadeIn(line1),FadeIn(plus),FadeIn(line2)],1.3
    def dependent(self):
        self.clear('두 번째 벡터가 같은 직선 위에 있다면','v₁ = (1, 0)     ·     v₂ = (2, 0) = 2v₁')
        self.board();self.v2=self.arrow([2,0],GOLD,width=7);self.v1=self.arrow([1,0],BLUE,width=4)
        labels=VGroup(txt('v₁',27,BLUE).move_to(self.p((.5,.4))),txt('v₂ = 2v₁',27,GOLD).move_to(self.p((1.7,-.55))))
        return [Create(self.v2),Create(self.v1),FadeIn(labels)],1.8
    def two_ways(self):
        self.clear('다른 계수, 같은 점','2v₁ + 0v₂ = 0v₁ + 1v₂ = (2, 0)')
        self.board();self.target=Dot(self.p((2,0)),color=PINK,radius=.1);self.add(self.target)
        self.part1=self.arrow([2,0],BLUE);self.part2=self.arrow([0,0],GOLD,[2,0]);self.add(self.part1,self.part2)
        self.coeff=txt('(a, b) = (2, 0)',32,BLUE).move_to(UP*2.65)
        self.add(self.coeff)
        return [Succession(Wait(.5),AnimationGroup(Transform(self.part1,self.arrow([0,0],BLUE)),Transform(self.part2,self.arrow([2,0],GOLD)),Transform(self.coeff,txt('(a, b) = (0, 1)',32,GOLD).move_to(UP*2.65)),run_time=1.8))],2.3
    def sliding(self):
        self.heading('계수는 변해도, 결과는 고정');self.formula('a + 2b = 2     ·     가능한 계수는 무한히 많습니다')
        self.remove(self.coeff)
        la=txt('a =',29,BLUE).move_to([-2.1,2.7,0]);lb=txt('b =',29,GOLD).move_to([.6,2.7,0])
        da=DecimalNumber(0,num_decimal_places=2,mob_class=Text,font_size=30,color=BLUE).move_to([-1.1,2.7,0]);db=DecimalNumber(1,num_decimal_places=2,mob_class=Text,font_size=30,color=GOLD).move_to([1.6,2.7,0])
        self.add(la,lb,da,db)
        moving=VGroup(self.part1,self.part2,da,db)
        def update(m,t):
            t=round(t,2)  # Keep displayed two-decimal coefficients exactly consistent.
            a=2*t;b=1-t
            self.part1.become(self.arrow([a,0],BLUE));self.part2.become(self.arrow([2*b,0],GOLD,[a,0]))
            da.set_value(a);db.set_value(b)
        return [UpdateFromAlphaFunc(moving,update)],3
    def cancellation(self):
        self.clear('숨겨진 상쇄 관계가 있습니다','2v₁ − v₂ = 0     ·     계수 (2, −1)은 (0, 0)이 아닙니다')
        self.board();right=self.arrow([2,0],BLUE,width=7);left=self.arrow([-2,0],GOLD,[2,0],width=3)
        self.add(txt('+ 2v₁',27,BLUE).move_to(self.p((1,.5))),txt('− v₂',27,GOLD).move_to(self.p((1,-.55))))
        self.cancel_arrows=VGroup(right,left)
        return [Succession(Create(right,run_time=1.1),Create(left,run_time=1.1),Circumscribe(Dot(self.origin,radius=.1),color=PINK,run_time=.8))],3
    def freedom(self):
        self.clear('벡터는 2개 · 움직일 수 있는 방향은 1개','v₁과 v₂의 조합은 이 직선을 벗어나지 못합니다')
        self.board();self.line=Line(self.p((-2,0)),self.p((5,0)),color=PINK,stroke_width=4)
        moving=Dot(self.p((-1,0)),color=PINK,radius=.09)
        self.add(self.line,moving)
        return [moving.animate.move_to(self.p((4,0)))],2
    def new_direction(self):
        self.clear('같은 직선 밖으로, 새 방향 하나','v₁ = (1, 0)     ·     새 v₂ = (0, 1)')
        self.board();self.v1=self.arrow([1,0],BLUE);self.v2=self.arrow([2,0],GOLD);self.add(self.v2,self.v1)
        return [Transform(self.v2,self.arrow([0,1],GOLD))],1.8
    def plane(self):
        self.heading('가로와 세로를 독립적으로 조절');self.formula('av₁ + bv₂ = (a, b)     ·     출력의 자유도 2개')
        horizontal=Line(self.p((-1,1)),self.p((4,1)),color=BLUE,stroke_width=3)
        vertical=Line(self.p((2,-1)),self.p((2,3)),color=GOLD,stroke_width=3)
        self.add(Dot(self.p((2,1)),color=PINK,radius=.085))
        dots=VGroup(*[Dot(self.p((a,b)),color=PINK,radius=.04) for a in [-1,0,1,2,3,4] for b in [-1,0,1,2]])
        return [Create(horizontal),Create(vertical),FadeIn(dots)],2
    def unique_point(self):
        self.clear('이 점을 만드는 계수는 하나입니다','x = (2, 1) = 2v₁ + 1v₂')
        self.board();self.a=2.;self.b=1.
        self.apart=self.arrow([2,0],BLUE);self.bpart=self.arrow([0,1],GOLD,[2,0]);self.dot=Dot(self.p((2,1)),color=PINK,radius=.09)
        self.fixed=Circle(radius=.16,color=PINK,stroke_width=2).move_to(self.p((2,1)))
        self.add(self.fixed,txt('목표 x',24,PINK).next_to(self.fixed,LEFT,buff=.15))
        return [Create(self.apart),Create(self.bpart),FadeIn(self.dot)],1.8
    def change_a(self):
        self.heading('a를 2에서 3으로 바꾸면');self.formula('a = 3, b = 1     →     (3, 1) ≠ (2, 1)')
        return [Transform(self.apart,self.arrow([3,0],BLUE)),Transform(self.bpart,self.arrow([0,1],GOLD,[3,0])),self.dot.animate.move_to(self.p((3,1)))],1.8
    def try_cancel(self):
        self.heading('b로는 가로의 차이를 지울 수 없습니다');self.formula('a = 3 고정     ·     b가 변해도 첫 성분은 항상 3')
        guide=DashedLine(self.p((3,-1.2)),self.p((3,3)),color=GOLD,dash_length=.12);self.add(guide)
        moving=VGroup(self.bpart,self.dot)
        def update(m,t):
            b=1+1.5*np.sin(2*PI*t)
            self.bpart.become(self.arrow([0,b],GOLD,[3,0]));self.dot.move_to(self.p((3,b)))
        return [UpdateFromAlphaFunc(moving,update,rate_func=linear)],3.5
    def zero_relation(self):
        self.clear('상쇄하려면, 두 계수가 모두 0이어야','av₁ + bv₂ = 0     ⇒     a = b = 0')
        self.board();ha=self.arrow([2,0],BLUE);va=self.arrow([0,1],GOLD,[2,0]);dot=Dot(self.p((2,1)),color=PINK,radius=.09);self.add(ha,va,dot)
        moving=VGroup(ha,va,dot)
        def update(m,t):
            a=2*(1-t);b=1-t
            ha.become(self.arrow([a,0],BLUE));va.become(self.arrow([0,b],GOLD,[a,0]));dot.move_to(self.p((a,b)))
        return [UpdateFromAlphaFunc(moving,update)],2.3
    def independent(self):
        self.clear('선형독립 · 대체할 수 없는 자유도','계수가 전부 0인 경우만 0벡터를 만듭니다')
        eq=txt('av₁ + bv₂ = 0',43).move_to(UP*1.3)
        then=txt('a = b = 0',43,PINK).move_to(DOWN*.5)
        return [FadeIn(eq),FadeIn(then)],1.3
    def uniqueness(self):
        self.clear('표현이 두 개 있다고 가정하면','두 식을 빼면, 계수 차이가 만드는 상쇄 관계')
        first=txt('x = av₁ + bv₂',35).move_to(UP*2)
        second=txt('x = a′v₁ + b′v₂',35).move_to(UP*.5)
        diff=txt('0 = (a − a′)v₁ + (b − b′)v₂',31,PINK).move_to(DOWN*1.5)
        return [FadeIn(first),FadeIn(second),FadeIn(diff)],1.6
    def only_zero(self):
        self.heading('상쇄가 없으니, 두 표현은 같습니다');self.formula('a − a′ = 0, b − b′ = 0     →     a = a′, b = b′')
        eq=txt('표현 가능한 점마다, 계수는 유일',31,BLUE).move_to(DOWN*2.8)
        return [FadeIn(eq)],1.2
    def ending(self):
        self.clear('자유도와 상쇄는 같은 구조의 양면','선형독립인 벡터들의 조합에서는 표현이 유일합니다')
        words=VGroup(txt('서로 대체할 수 없는 자유도',34,BLUE),txt('↕',33,MUTED),txt('비자명한 상쇄 관계 없음',34,GOLD),txt('↕',33,MUTED),txt('표현의 유일성',34,PINK)).arrange(DOWN,buff=.25).move_to(UP*.3)
        return [FadeIn(words)],1.5
