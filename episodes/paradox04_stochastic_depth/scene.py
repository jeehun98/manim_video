"""Stochastic depth: identity bypasses, shared weights and expected loss."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
MASK5=[1,0,1,1,0,1,0,1]
MASK4=[0,1,0,1,1,0,1,0]
MASK6=[1,1,0,1,1,1,0,1]

def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def box(s,x=0,y=0,w=2,h=.7,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.1,color=color,fill_color=BG,fill_opacity=1,stroke_width=1.5).move_to([x,y,0]),t(s,y,x,size=25,color=color,width=w-.2))

def route(points,color=GOOD,width=3):
    return VMobject(color=color,stroke_width=width).set_points_as_corners([np.array(p) for p in points])

def residual(on=True):
    # Split and merge are shared by the residual and existing identity paths.
    left=route([[0,2.7,0],[-1.7,2.7,0],[-1.7,.85,0],[-1.7,-1.1,0],[0,-1.1,0]],WEIGHT if on else MUTED)
    left.set_stroke(opacity=1 if on else .2).set_fill(opacity=0)
    identity=route([[0,2.7,0],[1.7,2.7,0],[1.7,-1.1,0],[0,-1.1,0]],GOOD)
    transform=box('F(x)' if on else 'F(x) · OFF',-1.7,.85,2.2,1.1,WEIGHT if on else MUTED)
    if not on:transform.set_opacity(.35)
    return VGroup(Arrow([0,3.65,0],[0,2.7,0],buff=.05,color=INK),left,identity,transform,
                  Circle(.21,color=INK,fill_color=BG,fill_opacity=1).move_to([0,-1.1,0]),t('+',-1.1,size=25),
                  Arrow([0,-1.32,0],[0,-2.2,0],buff=0,color=INK),t('입력 x',4.05,size=25),
                  t('변환 경로',-.25,-2,size=23,color=WEIGHT,width=2.2),t('항등 경로',.85,2.85,size=23,color=GOOD,width=2.1),
                  t('x + F(x)' if on else 'x + 0 = x',-2.8,size=35,color=ACCENT),
                  t('b = 1' if on else 'b = 0',1.85,-1.7,size=23,color=ACCENT,width=2),
                  t('같은 차원 · 합산 뒤 비선형성은 생략한 모형',-4.3,size=20,color=MUTED))

def ladder(mask=None,scale=1):
    mask=[1]*8 if mask is None else mask
    g=VGroup()
    for i,on in enumerate(mask):
        y=3.35-i*.88
        color=WEIGHT if on else MUTED
        branch=route([[1.4,y+.38,0],[-.9,y+.38,0],[-.9,y-.38,0],[1.4,y-.38,0]],color,1.5)
        branch.set_stroke(opacity=.75 if on else .16).set_fill(opacity=0)
        identity=Line([1.4,y+.44,0],[1.4,y-.44,0],color=GOOD,stroke_width=3)
        f=box(f'F{i+1}' if on else f'F{i+1} OFF',-.9,y,1.8,.49,color)
        if not on:f.set_opacity(.3)
        g.add(VGroup(branch,identity,f,Dot([1.4,y-.38,0],radius=.045,color=GOOD)))
    g.add(t(f'{sum(mask)} / 8',4.05,-2.65,size=30,color=ACCENT,width=2.4),t('변환',3.35,-2.75,size=20,color=MUTED,width=1.5),
          t('항등 경로는 유지',-3.8,size=24,color=GOOD),t('켜진 잔차 변환의 수',-4.5,size=20,color=MUTED))
    return g.scale(scale)

def trio(mask=(1,1,1)):
    g=VGroup()
    for j,on in enumerate(mask):
        x=-2.5+j*2.5
        g.add(box(f'F{j+1}',x,1.3,1.7,1,WEIGHT if on else MUTED))
        if not on:g[-1].set_opacity(.25)
        g.add(route([[x-.85,1.3,0],[x-.85,2.7,0],[x+.85,2.7,0],[x+.85,1.3,0]],GOOD,2))
        if j<2:g.add(Arrow([x+.85,1.3,0],[x+1.65,1.3,0],buff=.05,color=MUTED,stroke_width=2))
    return g

def combinations():
    g=VGroup()
    for i in range(256):
        color=interpolate_color(ManimColor(MUTED),ManimColor(WEIGHT),i.bit_count()/8)
        g.add(Square(.32,color=color,stroke_width=.8,fill_color=color,fill_opacity=.35).move_to([(i%16-7.5)*.36,(7.5-i//16)*.36+.1,0]))
    return VGroup(g,t('2⁸ = 256',3.8,size=47,color=ACCENT),t('각 칸 = 블록 ON/OFF 조합 하나',-3.5,size=25,color=MUTED),t('256개 깊이가 아니라 256개 구성',-4.4,size=23,color=WEIGHT))

def shared():
    rows=VGroup()
    for y,mask in [(2.5,MASK5),(.75,MASK4),(-1,MASK6)]:
        row=VGroup(*[box(f'F{j+1}',-3.15+j*.9,y,.69,.62,WEIGHT if on else MUTED) for j,on in enumerate(mask)])
        for j,on in enumerate(mask):
            if not on:row[j].set_opacity(.22)
        rows.add(row)
    return VGroup(rows,t('조합은 달라도 θ₁, …, θ₈는 공유',-2.5,size=29,color=WEIGHT),t('각 경로마다 별도 모델을 만드는 것이 아님',-3.6,size=23,color=MUTED))

class StochasticDepthPaths(Scene):
    def chrome(self,i):
        titles=['깊은 구조 · 얕은 학습 경로','Stochastic Depth','깊어질수록 길어지는 경로','중간 계산을 건너뛴다면?','Residual Block · 기존의 두 길','원래 입력에 변환 결과를 더한다',
                '변환은 끄고 지름길은 남긴다','순방향도 역방향도 항등 경로로','8개 블록 · 각각 ON 또는 OFF','8개의 선택 · 256가지 구성','같은 구조에서 다른 깊이로','왜 도움이 될까?',
                '특정 앞단 표현에 의존한다면','앞쪽 변환이 사라지는 순간','변환이 없는 입력에서도 작동하도록','표현력을 추가하는 것이 아니다','표현 가능한 함수와 선택되는 함수',
                '하나의 고정 경로를 넘어서','여러 경로의 평균 손실을 줄인다','부분 신경망들이 가중치를 공유','특정 경로에 대한 의존을 억제','추론에서는 전체 블록을 사용',
                '작은 모델이 더 강해지는 걸까?','여러 부분 경로에서도 작동하는 해','전체 구조는 깊게 · 학습 경로는 다양하게','Stochastic Depth의 역설']
        return VGroup(t('신경망의 역설  /  04',7.35,size=20,color=MUTED),t('신경망은 얕게 학습해야\n더 깊어진다?',6.45,size=32),
                      Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(titles[i],5.05,size=25,color=ACCENT),t('Stochastic Depth · 경로와 학습 목표',-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['더 깊은 신경망을 학습시키기 위해\n학습에서는 일부러 얕은 경로를 사용합니다.','바로 Stochastic Depth입니다.',
              '깊은 구조는 복잡한 계산을 표현하지만\n계산과 기울기 전달이 어려워질 수 있습니다.','중간의 계산을\n통째로 건너뛰면 어떨까요?',
              '입력을 변환하는 길과,\n그대로 전달하는 지름길이 있습니다.','두 결과를 더해\n입력에 새로운 계산 결과를 추가합니다.',
              '일부 잔차 변환을 무작위로 끄되\n입력을 전달하는 지름길은 남겨둡니다.','변환을 건너뛰어도 입력과 기울기는\n항등 경로를 통해 전달됩니다.',
              '8개 블록을 각각\n켜거나 끌 수 있다고 해보겠습니다.','가능한 조합은\n256가지입니다.',
              '이번에는 5개, 다음에는 다른 4개.\n서로 다른 구성으로 학습할 수 있습니다.','왜 이렇게 깊이를 바꾸면\n도움이 될까요?',
              '뒤쪽 블록이 앞쪽의 특정한 표현에\n지나치게 의존할 수 있습니다.','앞쪽 변환이\n무작위로 사라진다면 어떨까요?',
              '뒤쪽 블록은 그 변환이 없는 입력에도\n작동하도록 학습되어야 합니다.','핵심은 전체 신경망의\n표현력을 늘리는 것이 아닙니다.',
              '표현할 수 있는 함수와\n학습이 선택하는 함수는 다른 문제입니다.','하나의 고정된 경로만\n잘 작동하도록 학습시키지 않습니다.',
              '여러 깊이와 블록 조합에 걸친\n평균 손실을 줄이도록 학습합니다.','모든 부분 신경망은\n같은 블록의 가중치를 공유합니다.',
              '특정 경로에 대한 지나친 의존을\n억제하는 정규화 효과가 나타날 수 있습니다.',
              '추론에서는 전체 블록을 사용하며, 원래 방법은\n잔차 출력을 생존 확률에 맞춰 조정합니다.',
              '작은 신경망이 더 뛰어난\n표현력을 갖는다는 뜻이 아닙니다.',
              '여러 부분 신경망에서도 작동하도록 학습해\n전체 신경망이 더 좋은 해를 찾도록 유도합니다.',
              '전체는 깊게 유지하면서\n학습에서는 다양한 깊이의 지름길을 사용합니다.','이것이 Stochastic Depth의\n역설입니다.']
        for i,s in enumerate(data['segments']):
            self.clear();self.add(self.chrome(i),t(caps[i],-6.15,size=24))
            p=self.panel(i);self.play(FadeIn(p),run_time=.3)
            if i in [0,10,17,24]:
                if i==0:self.wait(.4)
                self.play(Transform(p[0],ladder(MASK4 if i==10 else MASK5)),run_time=.9)
            if i==6:
                self.play(Transform(p[0],residual(False)),run_time=1)
            if i==7:
                dot=Dot([0,2.7,0],color=ACCENT,radius=.1);self.add(dot)
                path=route([[0,2.7,0],[1.7,2.7,0],[1.7,-1.1,0],[0,-1.1,0]])
                self.play(MoveAlongPath(dot,path),run_time=1.1)
                self.play(dot.animate.set_color(PRUNE),run_time=.2)
                self.play(MoveAlongPath(dot,path.copy().reverse_points()),run_time=1.1)
                self.add(t('순방향 x  /  역방향 gradient',-3.6,size=25,color=GOOD))
            if i==13:
                self.play(Transform(p[0],trio((0,1,1))),run_time=.9)
            if i==14:
                self.play(Circumscribe(p[0][6],color=ACCENT),run_time=.8)
            if i==18:
                self.play(Indicate(p[1],color=ACCENT),run_time=.9)
            if i==19:
                self.play(*[Circumscribe(row[3],color=ACCENT) for row in p[0]],run_time=1)
            if i==21:
                self.play(Transform(p[1],t('추론: x다음 = x + pₗ Fₗ(x)',-2.7,size=34,color=GOOD)),run_time=.9)
            remaining=s['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-133)<1/30+.001

    def panel(self,i):
        if i in [0,1,2,3,8,10,11,17,24]:
            mask=MASK5 if i in [10,11] else [1]*8
            return VGroup(ladder(mask))
        if i in [4,5,6,7]:return VGroup(residual(i!=7))
        if i==9:return combinations()
        if i in [12,13,14]:
            return VGroup(trio((0,1,1) if i==14 else (1,1,1)),t('같은 F3 · 달라지는 앞단의 변환 구성',-.2,size=27,color=ACCENT),
                          t('앞단 표현 A' if i==12 else '앞단 변환이 빠진 표현 B',-1.5,size=30,color=WEIGHT),
                          t('후단 블록의 가중치는 그대로 공유',-2.75,size=26,color=GOOD),t('과도한 경로 의존을 줄일 수 있음',-4,size=24,color=MUTED))
        if i in [15,16,22]:
            return VGroup(box('전체 구조가 표현할 수 있는 함수',0,2.8,7.5,1.2,WEIGHT),t('≠',1.35,size=40,color=ACCENT),box('학습 과정에서 선택되는 함수',0,-.1,7.5,1.2,SPARSE),
                          t('구조의 표현력과 학습의 편향을 구별',-2,size=29,color=GOOD),t('부분 신경망이 전체보다 더 강한 표현력을 갖는 것은 아님',-3.8,size=21,color=MUTED))
        if i in [18,20,23]:
            return VGroup(shared().scale(.9).shift(UP*.4),t('minθ Eᵦ[L(fθ,ᵦ(x), y)]',-3.65,size=33,color=ACCENT),t('마스크를 표본 추출해 평균 목표를 향해 갱신',-4.55,size=20,color=MUTED))
        if i==19:return shared()
        if i==21:
            g=ladder().scale(.7).shift(UP*1.2)
            return VGroup(g,t('학습: x다음 = x + bₗ Fₗ(x)',-2.7,size=34,color=WEIGHT),t('pₗ = 해당 블록의 생존 확률',-3.7,size=25,color=MUTED),t('원래 방법 · 전체 마스크 출력의 정확한 평균은 아님',-4.55,size=19,color=MUTED))
        return VGroup(t('전체 구조는 깊게',2.6,size=44,color=WEIGHT),t('학습 경로는 다양하게',.65,size=40,color=GOOD),t('공유된 가중치로\n여러 경로에서 작동하는 해를 찾는다',-1.5,size=31,color=ACCENT),t('효과는 모델·데이터·확률 설정에 따라 다름',-4,size=23,color=MUTED))
