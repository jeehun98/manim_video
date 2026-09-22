"""LA09: exact rank factorization A=BC, basis columns and coefficient columns."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('relations_visuals',Path(__file__).resolve().parents[1]/'la01_matrix_relations/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
GREEN='#8CE3BB'
B=np.array([[1,0],[0,1],[1,1]])
C=np.array([[1,0,2,1],[0,1,-1,3]])
A=B@C
DURATION=112
CAPTIONS=[
(0,'recap','앞에서는 Rank로\n독립적인 방향의 개수를 셌습니다.'),
(5,'four_columns','이번에는 네 개의 열을 가진 행렬을\n다른 방식으로 기록해보겠습니다.'),
(11,'rank_two','네 열은 서로 다르지만, 이 행렬의 Rank는 2입니다.\n독립적인 두 방향만으로 모든 열을 만들 수 있습니다.'),
(17,'basis','여기서는 첫 두 열을 고르겠습니다.\n이 둘은 서로 독립이며, 나머지 열을 만드는 재료입니다.'),
(23,'third_column','첫 열을 2배 하고 두 번째 열을 빼면,\n세 번째 열이 됩니다.'),
(30,'fourth_column','첫 열에 두 번째 열의 3배를 더하면,\n네 번째 열도 만들 수 있습니다.'),
(37,'coefficients','그렇다면 각 열을 통째로 기록하는 대신,\n두 방향과 그 조합 계수를 따로 기록할 수 있습니다.'),
(43,'factorization','독립적인 방향은 B에,\n각 열을 만드는 계수는 C에 담습니다.'),
(50,'rebuild','B와 C를 곱하면,\n각 열이 다시 만들어져 원래 행렬 A가 됩니다.'),
(56,'roles','B는 어떤 방향을 사용할지,\nC는 그 방향들을 얼마나 섞을지를 기록합니다.'),
(62,'dimensions','m×n 행렬의 Rank가 r이면,\nm×r 행렬과 r×n 행렬의 곱으로 표현할 수 있습니다.'),
(69,'counts','기록할 원소 수는 mn개에서\nmr + rn개로 바뀝니다.'),
(75,'small_example','물론 항상 숫자가 줄어드는 것은 아닙니다.\n방금 작은 예제는 12개 대신 14개를 기록합니다.'),
(81,'large_example','하지만 1000×1000 행렬의 Rank가 10이라면,\n100만 개 대신 2만 개의 값으로 표현할 수 있습니다.'),
(89,'exact','여기서는 정보를 버린 것이 아닙니다.\n실제 Rank에 맞춰 분해했으므로 원래 행렬을 정확히 복원합니다.'),
(96,'structure','중복된 열을 따로 저장하는 대신,\n독립적인 구조와 그 조합을 기록한 것입니다.'),
(102,'ending','행렬을 분해한다는 것은,\n필요한 방향과 그것을 조합하는 방법을 나누어 보는 일입니다.'),
]

class Table(VGroup):
    def __init__(self,values,name,colnames=None,coefficient=False,size=30,spacing=.78):
        super().__init__();values=np.asarray(values);nr,nc=values.shape;self.entries=VGroup();self.cols=VGroup()
        colors=[BLUE,GOLD,PINK,GREEN]
        for j in range(nc):
            col=VGroup()
            for i in range(nr):
                color=colors[i] if coefficient else colors[j]
                entry=txt(f'{values[i,j]:g}'.replace('-','−'),size,color).move_to([(j-(nc-1)/2)*spacing,((nr-1)/2-i)*.68,0])
                self.entries.add(entry);col.add(entry)
            self.cols.add(col)
        w=(nc-1)*spacing/2+.42;h=(nr-1)*.68/2+.34
        brackets=VGroup(*[VMobject().set_points_as_corners([[s*(w-.12),h,0],[s*w,h,0],[s*w,-h,0],[s*(w-.12),-h,0]]).set_stroke(INK,2) for s in [-1,1]])
        self.labels=VGroup()
        if colnames:
            for j,title in enumerate(colnames):self.labels.add(txt(title,21,colors[j]).move_to([(j-(nc-1)/2)*spacing,h+.3,0]))
        self.name=txt(name,28,INK).move_to(UP*(h+(.88 if colnames else .55)))
        self.add(self.cols,brackets,self.labels,self.name)

class RankFactorization(Scene):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   09',19,MUTED).move_to(UP*7),txt('방향과 조합으로 나누어 기록하기',34).move_to(UP*6.05))
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
    def recap(self):
        self.heading('Rank = 독립적인 방향 수');self.formula('같은 구조를, 행렬의 표현에 적용해봅시다')
        eq=txt('Rank(A) = r',48).move_to(UP*.5)
        return [FadeIn(eq)],1.2
    def four_columns(self):
        self.clear('네 개의 열을 가진 행렬','A = [ a₁  a₂  a₃  a₄ ]')
        self.ma=Table(A,'A',['a₁','a₂','a₃','a₄'],size=37,spacing=1.05).move_to(UP*.2)
        return [FadeIn(self.ma)],1.3
    def rank_two(self):
        self.heading('열은 4개 · 독립적인 방향은 2개');self.formula('Rank(A) = 2')
        return [Circumscribe(self.ma.cols[0],color=BLUE),Circumscribe(self.ma.cols[1],color=GOLD)],1.6
    def basis(self):
        self.heading('독립인 두 열을 재료로 고릅니다');self.formula('a₁ = (1, 0, 1)     ·     a₂ = (0, 1, 1)')
        return [self.ma.cols[2].animate.set_opacity(.2),self.ma.cols[3].animate.set_opacity(.2),Indicate(self.ma.cols[0],color=BLUE,scale_factor=1.05),Indicate(self.ma.cols[1],color=GOLD,scale_factor=1.05)],1.5
    def relation(self,coeffs,result,title):
        self.clear(title)
        left=Table((coeffs[0]*B[:,0]).reshape(-1,1),f'{coeffs[0]:g}a₁',size=35).move_to([-2.6,.1,0])
        mid=Table((coeffs[1]*B[:,1]).reshape(-1,1),f'{coeffs[1]:g}a₂'.replace('-','−'),size=35).move_to([-.1,.1,0]);mid.cols.set_color(GOLD)
        right=Table(result.reshape(-1,1),'a₃' if coeffs[1]==-1 else 'a₄',size=35).move_to([2.4,.1,0]);right.cols.set_color(PINK if coeffs[1]==-1 else GREEN)
        self.add(txt('+',32).move_to([-1.35,-.25,0]),txt('=',32).move_to([1.15,-.25,0]))
        return [FadeIn(left),FadeIn(mid),FadeIn(right)],1.5
    def third_column(self):
        anim,seconds=self.relation([2,-1],A[:,2],'세 번째 열을 만드는 방법')
        self.formula('a₃ = 2a₁ − a₂ = (2, −1, 1)')
        return anim,seconds
    def fourth_column(self):
        anim,seconds=self.relation([1,3],A[:,3],'네 번째 열도 같은 재료로')
        self.formula('a₄ = a₁ + 3a₂ = (1, 3, 4)')
        return anim,seconds
    def coefficients(self):
        self.clear('각 열마다, 두 개의 계수만 기록','각 열의 계수: (1, 0), (0, 1), (2, −1), (1, 3)')
        self.mc=Table(C,'C · 조합 계수',['a₁','a₂','a₃','a₄'],coefficient=True,size=36,spacing=1.08).move_to(UP*.3)
        self.add(txt('a₁의 배수',22,BLUE).move_to([-3,self.mc.cols[0][0].get_y(),0]),txt('a₂의 배수',22,GOLD).move_to([-3,self.mc.cols[0][1].get_y(),0]))
        return [FadeIn(self.mc)],1.5
    def factors(self):
        self.ma=Table(A,'A',['a₁','a₂','a₃','a₄'],size=28,spacing=.85).shift(UP*1.4)
        self.mb=Table(B,'B · 방향',size=30,spacing=.8).shift(LEFT*2+DOWN*2)
        self.mc=Table(C,'C · 조합',coefficient=True,size=28,spacing=.7).shift(RIGHT*1.45+DOWN*2)
        self.add(self.ma,self.mb,self.mc,txt('×',30,MUTED).move_to([-.45,-2.15,0]))
    def factorization(self):
        self.clear('방향은 B에, 조합은 C에','A = BC     ·     B의 두 열은 a₁, a₂')
        self.factors()
        return [TransformFromCopy(self.ma.cols[0],self.mb.cols[0]),TransformFromCopy(self.ma.cols[1],self.mb.cols[1])],1.6
    def rebuild(self):
        self.heading('곱하면, 각 열이 정확히 다시 만들어집니다');self.formula('A의 j번째 열 = B × C의 j번째 열')
        return [Succession(*[AnimationGroup(Circumscribe(self.mc.cols[j],color=[BLUE,GOLD,PINK,GREEN][j]),Circumscribe(self.ma.cols[j],color=[BLUE,GOLD,PINK,GREEN][j]),run_time=.7) for j in range(4)])],2.8
    def roles(self):
        self.heading('필요한 방향과, 그 방향의 사용법');self.formula('B: 어떤 방향인가?     C: 얼마씩 조합하는가?')
        return [Circumscribe(self.mb,color=BLUE),Circumscribe(self.mc,color=GOLD)],1.6
    def dimensions(self):
        self.clear('Rank r이면, r개의 방향으로 충분합니다','A = BC     ·     (m×r)(r×n) → m×n')
        # Schematic dimensions; widths illustrate compatible inner dimensions.
        a=Rectangle(width=2.0,height=2.4,color=INK).move_to([-2.5,.4,0]);b=Rectangle(width=.75,height=2.4,color=BLUE).move_to([.05,.4,0]);c=Rectangle(width=2.1,height=.9,color=GOLD).move_to([2.35,.4,0])
        labels=VGroup(txt('A',32).move_to(a),txt('B',30,BLUE).move_to(b),txt('C',32,GOLD).move_to(c),txt('m × n',26).move_to([-2.5,-1.4,0]),txt('m × r',26,BLUE).move_to([.05,-1.4,0]),txt('r × n',26,GOLD).move_to([2.35,-1.4,0]),txt('=',28).move_to([-1.15,.4,0]),txt('×',28).move_to([.92,.4,0]))
        return [Create(a),Create(b),Create(c),FadeIn(labels)],1.6
    def counts(self):
        self.clear('기록하는 원소 수를 비교하면','r(m + n) < mn일 때 숫자 저장량이 줄어듭니다')
        eq=txt('mn  →  mr + rn',43).move_to(UP*.7)
        note=txt('r이 m, n보다 충분히 작을 때',29,MUTED).move_to(DOWN*1.3)
        return [FadeIn(eq),FadeIn(note)],1.4
    def small_example(self):
        self.clear('작은 예제에서는 숫자가 더 많을 수도','분해 가능성과 저장량 감소는 구별해야 합니다')
        top=txt('A: 3 × 4 = 12개',35).move_to(UP*1.5)
        bottom=txt('B, C: 3 × 2 + 2 × 4 = 14개',32).move_to(DOWN*.5)
        return [FadeIn(top),FadeIn(bottom)],1.3
    def large_example(self):
        self.clear('1000 × 1000, Rank 10이라면','10,000 + 10,000 = 20,000     ·     원소 수 98% 감소')
        a=txt('1,000,000',48).move_to(UP*1.7);arrow=txt('↓',45,MUTED).move_to(UP*.2);b=txt('20,000',51,BLUE).move_to(DOWN*1.4)
        return [FadeIn(a),FadeIn(arrow),FadeIn(b)],1.5
    def exact(self):
        self.clear('실제 Rank로 분해하면, 정확히 같은 행렬','근사가 아니라 A = BC     ·     더 작은 Rank의 근사와 구별')
        self.ma=Table(A,'원래 A',size=29,spacing=.72).shift(LEFT*2)
        self.rebuilt=Table(B@C,'복원한 BC',size=29,spacing=.72).shift(RIGHT*2)
        self.add(txt('=',30).move_to(DOWN*.15))
        return [FadeIn(self.ma),FadeIn(self.rebuilt)],1.5
    def structure(self):
        self.clear('중복된 기록을, 방향과 조합으로','새 정보를 덜어낸 것이 아니라, 같은 구조를 다르게 기록')
        title=VGroup(txt('독립적인 방향 B',36,BLUE),txt('×',32,MUTED),txt('각 열의 조합 C',36,GOLD)).arrange(DOWN,buff=.5).move_to(UP*.5)
        return [FadeIn(title)],1.3
    def ending(self):
        self.clear('행렬 분해: 구조와 조합을 분리해서 보기','A = BC')
        main=txt('필요한 방향은 무엇인가?\n각 열은 어떻게 만들어지는가?',35).move_to(UP*.5)
        return [FadeIn(main)],1.3
