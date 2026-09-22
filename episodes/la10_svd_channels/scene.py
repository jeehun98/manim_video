"""SVD as a sum of orthogonal rank-one input/output channels."""
import importlib.util
from pathlib import Path
import numpy as np
from manim import *
spec=importlib.util.spec_from_file_location('factor',Path(__file__).resolve().parents[1]/'la09_rank_factorization/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
txt=shared.txt
BLUE,GOLD,PINK,INK,MUTED=shared.BLUE,shared.GOLD,shared.PINK,shared.INK,shared.MUTED
COLORS=[BLUE,GOLD,PINK]
s=1/np.sqrt(2)
U=np.array([[s,-s,0],[s,s,0],[0,0,1.]])
V=np.array([[1.,0,0],[0,s,-s],[0,s,s]])
SIGMA=np.array([3.,1.5,.4])
CHANNELS=[SIGMA[i]*np.outer(U[:,i],V[:,i]) for i in range(3)]
A=sum(CHANNELS)
DURATION=109
CAPTIONS=[
(0,'recap','앞에서는 행렬을 독립적인 방향과\n그 조합으로 나누어 보았습니다.'),
(5,'complexity','이번에는 행렬 안의 관계를\n여러 개의 단순한 채널로 나누어 보겠습니다.'),
(11,'separate','복잡하게 겹쳐 있던 관계를\n하나씩 분리해서 보는 겁니다.'),
(17,'one_channel','각 채널은 특정한 입력 패턴을 읽고,\n특정한 출력 패턴으로 보냅니다.'),
(23,'read_component','먼저 입력 x에서, 패턴 vᵢ가\n얼마나 들어 있는지를 읽습니다.'),
(29,'gain','그 성분에 전달 강도 σᵢ를 곱하고,\n출력 패턴 uᵢ 방향으로 보냅니다.'),
(36,'rank_one','그래서 하나의 채널은\nσᵢuᵢvᵢᵀ라는 행렬로 표현됩니다.'),
(42,'orthogonal','SVD에서는 입력 패턴끼리, 출력 패턴끼리\n서로 직교하고, 각 패턴의 길이는 1입니다.'),
(49,'strengths','따라서 같은 크기의 입력 패턴을 넣었을 때,\nσᵢ가 클수록 더 크게 전달됩니다.'),
(56,'all_channels','이런 채널들을 모두 더하면,\n원래 행렬이 정확히 만들어집니다.'),
(63,'recombine','하나의 복잡한 관계는, 여러 단순한 관계가\n겹쳐 작용한 결과로 볼 수 있습니다.'),
(69,'formula_scene','이 분해를 SVD,\n특잇값 분해라고 합니다.'),
(75,'ordered','σᵢ는 특잇값입니다. 큰 값부터 정리하면,\n강한 채널과 약한 채널이 드러납니다.'),
(82,'input_matters','다만 실제 기여는, 그 입력에\n해당 패턴이 얼마나 들어 있는지에도 달려 있습니다.'),
(90,'approximation','약한 채널을 빼면 더 단순해지지만,\n그때부터는 원래 행렬의 근사가 됩니다.'),
(97,'ending','SVD는 행렬 속 관계를,\n입력 패턴과 전달 강도, 출력 패턴으로 나누어 보여줍니다.'),
]

def pattern(values,color):
    g=VGroup(Line([-0.5,0,0],[.5,0,0],color=MUTED,stroke_width=1))
    for j,val in enumerate(values):
        if abs(val)>1e-8:
            g.add(Rectangle(width=.19,height=abs(val)*.7,stroke_width=0,fill_color=color,fill_opacity=.9).move_to([-.32+j*.32,val*.35,0]))
        else:g.add(Dot([-.32+j*.32,0,0],radius=.035,color=color))
    return g

def heat(values,width=2.2):
    g=VGroup();cell=width/3
    for i in range(3):
        for j in range(3):
            value=values[i,j]
            g.add(Square(side_length=cell-.035,stroke_color=MUTED,stroke_width=.5,fill_color=BLUE if value>=0 else PINK,fill_opacity=.08+.8*abs(value)/3).move_to([(j-1)*cell,(1-i)*cell,0]))
    return g

def card(i):
    color=COLORS[i];idx='₁₂₃'[i]
    panel=RoundedRectangle(width=6.6,height=1.75,corner_radius=.14,stroke_color=color,stroke_opacity=.65,stroke_width=1.5,fill_color=color,fill_opacity=.09)
    p=pattern(V[:,i],color).move_to([-2.3,.14,0]);q=pattern(U[:,i],color).move_to([2.3,.14,0])
    labels=VGroup(txt('v'+idx,25,color).move_to([-2.3,-.57,0]),txt('u'+idx,25,color).move_to([2.3,-.57,0]),txt(f'σ{idx} = {SIGMA[i]:g}',28,color).move_to(ORIGIN))
    arrows=VGroup(Arrow([-1.6,0,0],[-.9,0,0],buff=0,color=color,stroke_width=2),Arrow([.9,0,0],[1.6,0,0],buff=0,color=color,stroke_width=2))
    return VGroup(panel,p,q,labels,arrows)

class SVDChannels(shared.RankFactorization):
    def construct(self):
        self.head,self.note,self.sub=VGroup(),VGroup(),VGroup()
        self.chrome=VGroup(txt('LINEAR ALGEBRA   /   10',19,MUTED).move_to(UP*7),txt('SVD: 관계를 채널로 나누어 보기',34).move_to(UP*6.05));self.add(self.chrome)
        for i,(start,action,caption) in enumerate(CAPTIONS):
            end=CAPTIONS[i+1][0] if i+1<len(CAPTIONS) else DURATION
            self.remove(self.sub);self.sub=txt(caption,27).move_to(DOWN*6.15);self.add(self.sub)
            anim,seconds=getattr(self,action)()
            if anim:self.play(*anim,run_time=seconds)
            if end>self.time:self.wait(end-self.time)
            assert abs(end-self.time)<.04
    def recap(self):
        self.clear('방향과 조합에서, 개별 채널로','A = BC  →  입력과 출력의 패턴을 함께 보기')
        return [FadeIn(txt('하나의 행렬\n여러 개의 전달 채널',42).move_to(UP*.3))],1.2
    def complexity(self):
        self.clear('하나의 행렬에 섞여 있는 관계','색의 밝기 = 크기     ·     파랑 + / 분홍 −')
        self.map=heat(A,3.0).move_to(UP*1.5)
        self.net=VGroup()
        for j in range(3):
            for i in range(3):
                if abs(A[i,j])>1e-8:self.net.add(Line([-2.8,-.8-j*.75,0],[2.8,-.8-i*.75,0],color=BLUE if A[i,j]>=0 else PINK,stroke_width=1+abs(A[i,j])*2,stroke_opacity=.65))
        for side in [-1,1]:
            for i in range(3):self.net.add(Dot([side*2.8,-.8-i*.75,0],radius=.10,color=INK))
        return [FadeIn(self.map),Create(self.net)],2
    def separate(self):
        self.clear('겹쳐진 관계를, 채널별로 펼치면','각 레이어는 하나의 Rank 1 행렬')
        self.cards=VGroup(*[card(i).shift(RIGHT*(i-1)*.18+UP*(i-1)*.18) for i in range(3)])
        self.add(self.cards)
        return [self.cards[i].animate.move_to([0,2.35-i*2.25,0]) for i in range(3)],2.5
    def one_channel(self):
        self.clear('하나의 채널: 입력 패턴 → 출력 패턴','vᵢ → σᵢuᵢ')
        self.single=card(0).scale(1.08).move_to(UP*.4)
        return [FadeIn(self.single)],1.2
    def read_component(self):
        self.clear('입력에서 특정 패턴의 성분을 읽습니다','vᵢᵀx = 입력 패턴 vᵢ 방향의 성분')
        self.flow=VGroup(txt('입력 x',34).move_to([-2.5,1,0]),txt('→',35).move_to([-.95,1,0]),txt('vᵢᵀx',40,BLUE).move_to([1,1,0]),txt('패턴과의 내적',28,MUTED).move_to([1,-.1,0]))
        return [FadeIn(self.flow)],1.4
    def gain(self):
        self.clear('성분을 읽고 → 배율을 곱하고 → 출력','x → vᵢᵀx → σᵢ(vᵢᵀx)uᵢ')
        blocks=VGroup(txt('읽기   vᵢᵀx',38,BLUE),txt('↓',30,MUTED),txt('조절   × σᵢ',38,GOLD),txt('↓',30,MUTED),txt('출력   uᵢ 방향',38,PINK)).arrange(DOWN,buff=.35).move_to(UP*.3)
        return [LaggedStart(*[FadeIn(b) for b in blocks],lag_ratio=.3)],2.5
    def rank_one(self):
        self.clear('하나의 채널은 Rank 1 행렬','출력은 언제나 uᵢ가 만드는 한 방향 위에 있습니다')
        return [FadeIn(VGroup(txt('Aᵢ = σᵢuᵢvᵢᵀ',43,BLUE),txt('Aᵢx = σᵢ(vᵢᵀx)uᵢ',35),txt('σᵢ > 0',25,MUTED)).arrange(DOWN,buff=.7))],1.4
    def orthogonal(self):
        self.clear('패턴의 기준을 맞춥니다','입력끼리 직교 · 출력끼리 직교 · 각 패턴의 길이 1')
        left=VGroup(txt('입력 패턴',30,BLUE),txt('vᵢᵀvⱼ = 0  (i ≠ j)',28),txt('‖vᵢ‖ = 1',30)).arrange(DOWN,buff=.6).move_to(UP*1.5)
        right=VGroup(txt('출력 패턴',30,PINK),txt('uᵢᵀuⱼ = 0  (i ≠ j)',28),txt('‖uᵢ‖ = 1',30)).arrange(DOWN,buff=.6).move_to(DOWN*1.4)
        return [FadeIn(left),FadeIn(right)],1.5
    def strengths(self):
        self.clear('같은 크기의 패턴을 넣어 비교하면','Avᵢ = σᵢuᵢ     ·     ‖Avᵢ‖ = σᵢ')
        rows=VGroup()
        for i,val in enumerate(SIGMA):
            y=1.8-i*1.8
            rows.add(txt('v'+'₁₂₃'[i]+' →',30,COLORS[i]).move_to([-2.6,y,0]),Rectangle(width=val,height=.45,stroke_width=0,fill_color=COLORS[i],fill_opacity=.85).move_to([-1+val/2,y,0]),txt(f'{val:g}',27,COLORS[i]).move_to([2.7,y,0]))
        return [FadeIn(rows)],1.6
    def all_channels(self):
        self.clear('채널들을 모두 더하면 원래 행렬','A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + σ₃u₃v₃ᵀ')
        self.cards=VGroup(*[card(i).move_to([0,2.35-i*2.25,0]) for i in range(3)])
        return [LaggedStart(*[FadeIn(c) for c in self.cards],lag_ratio=.25)],1.8
    def recombine(self):
        self.heading('여러 단순한 관계가 겹쳐 하나의 관계로')
        self.play(*[self.cards[i].animate.move_to([.15*(i-1),.15*(i-1),0]) for i in range(3)],run_time=1.6)
        merged=VGroup(heat(A,3),txt('A = A₁ + A₂ + A₃',32).move_to(DOWN*2.2))
        return [FadeOut(self.cards),FadeIn(merged)],1.0
    def formula_scene(self):
        self.clear('SVD · 특잇값 분해','U: 출력 패턴     Σ: 전달 강도     V: 입력 패턴')
        return [FadeIn(VGroup(txt('A = UΣVᵀ',48),txt('A = Σᵢ σᵢuᵢvᵢᵀ',36,BLUE),txt('0이 아닌 채널 수 = Rank(A)',27,MUTED)).arrange(DOWN,buff=.75).move_to(UP*.3))],1.4
    def ordered(self):
        self.clear('특잇값: 채널의 전달 강도','σ₁ ≥ σ₂ ≥ σ₃ ≥ 0')
        return self.strength_rows()
    def strength_rows(self):
        rows=VGroup(*[card(i).move_to([0,2.35-i*2.25,0]) for i in range(3)])
        return [FadeIn(rows)],1.4
    def input_matters(self):
        self.clear('강도와 실제 기여는 구별합니다','실제 기여의 크기 = σᵢ |vᵢᵀx|')
        return [FadeIn(VGroup(txt('σ₁ = 3이어도',38,BLUE),txt('v₁ᵀx = 0이면',36),txt('첫 채널의 출력 = 0',36,GOLD)).arrange(DOWN,buff=.7))],1.4
    def approximation(self):
        self.clear('약한 채널을 빼면, 근사가 됩니다','전체 합 = A     ·     일부만 남기면 A ≈ A₁ + A₂')
        self.cards=VGroup(*[card(i).move_to([0,2.35-i*2.25,0]) for i in range(3)]);self.add(self.cards)
        return [self.cards[2].animate.set_opacity(.12)],1.8
    def ending(self):
        self.clear('입력 패턴 · 전달 강도 · 출력 패턴','SVD: 행렬 속 전달 구조를 분리해서 보기')
        return [FadeIn(VGroup(txt('무엇을 읽는가?   vᵢ',36,BLUE),txt('얼마나 전달하는가?   σᵢ',36,GOLD),txt('어떤 모습으로 내보내는가?   uᵢ',32,PINK)).arrange(DOWN,buff=.85).move_to(UP*.4))],1.8
