"""AI compiler introduction, paced to the user's 23 utterance boundaries."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import BG, INK, MUTED, WEIGHT, SPARSE, ACCENT, GOOD, txt, configure_vertical

configure_vertical()
config.disable_caching = True
ROOT = Path(__file__).resolve().parent

def t(s,x=0,y=0,size=28,color=INK,width=7.6):
    return txt(s,size,color,width).move_to([x,y,0])

def box(s,x=0,y=0,w=2.15,h=.9,color=WEIGHT):
    text=t(s,x,y,24,color,w-.25)
    if text.height>h-.2: text.scale_to_fit_height(h-.2)
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,color=color,fill_color=BG,fill_opacity=1,stroke_width=2).move_to([x,y,0]),text)

def chain(names,y=1,colors=None):
    colors=colors or [WEIGHT,SPARSE,GOOD]
    xs=np.linspace(-2.65,2.65,len(names)) if len(names)>1 else [0]
    nodes=VGroup(*[box(s,x,y,color=colors[i%len(colors)]) for i,(s,x) in enumerate(zip(names,xs))])
    arrows=VGroup(*[Arrow(a.get_right(),b.get_left(),buff=.08,color=MUTED,stroke_width=2) for a,b in zip(nodes,nodes[1:])])
    return VGroup(nodes,arrows)

def grid(rows,cols,x,y,color=WEIGHT):
    return VGroup(*[Square(.39,stroke_width=1.3,color=color,fill_color=color,fill_opacity=.12).move_to([x+(j-(cols-1)/2)*.45,y+((rows-1)/2-i)*.45,0]) for i in range(rows) for j in range(cols)])

class WhatIsAICompiler(Scene):
    def construct(self):
        data=json.loads(ROOT.joinpath('timing.json').read_text(encoding='utf-8'))
        self.stage=VGroup();self.head=VGroup();self.cap=VGroup()
        self.add(t('AI 컴파일러  /  01',y=7.35,size=21,color=MUTED),t('AI 컴파일러란\n무엇일까?',y=6.45,size=35),Line([-3.9,5.65,0],[3.9,5.65,0],color=MUTED,stroke_opacity=.35),t('텐서의 구조에서 하드웨어 실행까지',y=-7.45,size=19,color=MUTED))
        titles=['왜 별도의 이름이 있을까?','신경망도 컴퓨터 프로그램','실행에는 구체적인 명령이 필요하다','명령은 보이고, 구조는 흐려진다','같은 계산의 다른 높이','연산의 연결 관계가 드러난다','행렬곱 구조가 주는 선택','중간 결과를 따로 저장해야 할까?','여러 층을 하나의 계산 구조로','일반 컴파일러와 공유하는 능력','분석의 단위와 보존할 의미','각 축의 크기와 역할','어느 축으로 합치고 펼칠까?','의존성은 지켜야 한다','정보가 변환 판단의 근거가 된다','하나의 프로그램을 따라가 보자','프레임워크에서 컴파일 시스템으로','분석하고 변환한다','하드웨어에 맞는 실행 프로그램','컴파일 시스템 안에서 역할을 나눈다','실제 시스템도 여러 요소의 결합','공유하는 컴파일 원리','텐서의 의미를 실행으로']
        notes=['두 이름은 무엇이 다를까?','Y = ReLU(XW + b)','개념적 명령 · 실제 ISA 아님','같은 계산 · 다른 표현 수준','표현 비교 · 실제 역변환 단계 아님','MatMul → Bias Add → ReLU','크기·타깃에 맞는 후보 검토','가능 여부와 이득은 조건에 따라','연산의 의미 + 연결 관계','고수준 IR · 라이브러리 정보','Tensor Semantics + Graph','예시: FP32 · M × K × N','K축 Reduction · M축 Broadcasting','ReLU는 Bias Add의 결과를 사용','의미·조건·타깃을 함께 확인','컴파일 경로 예시','포착 범위와 전달 방식은 시스템별','항상 빨라짐을 보장하는 것은 아님','대상별 코드 · 라이브러리 호출','모든 기능이 한 컴파일러 안에 있지는 않음','구성 요소와 지원 경로는 시스템별','분석 → 중간 표현 → 변환 → 코드 생성','구조를 이해하고 · 의미를 지키고 · 실행으로']
        captions=['일반 컴파일러도 최적화하는데,\n왜 AI 컴파일러가 따로 있을까요?','입력 × 가중치 + 편향,\n그리고 ReLU를 적용합니다.','읽기 · 곱셈 · 누적 · 저장이\n실행 명령으로 구체화됩니다.','명령을 펼치면 원래의 수학적 구조는\n알아보기 어려워질 수 있습니다.','수많은 곱셈과 덧셈이\n하나의 행렬곱을 이루고 있습니다.','계산은 같지만,\n표현하는 수준이 달라집니다.','구현 선택이나 블록 분할을\n검토할 수 있습니다.','후속 연산까지 보면\n중간 저장을 줄일 수 있는지 판단합니다.','여러 층의 연산 관계를 유지하면\n전체 계산을 분석할 수 있습니다.','일반 컴파일러도 고수준 정보를\n활용해 행렬 연산을 최적화합니다.','무엇을 기본 단위로 분석하고,\n어떤 의미와 제약을 보존할까요?','자료형과 축의 크기,\n각 축의 역할이 중요합니다.','합산하는 축과 펼쳐 적용하는 축을\n알아야 합니다.','실행 방법을 바꿔도\n프로그램의 의미는 지켜야 합니다.','이 정보로 가능한 변환과\n실행 방법을 검토합니다.','하나의 신경망 프로그램이\n실행 코드가 되는 과정을 보겠습니다.','텐서 연산과 연결 관계가\n컴파일 시스템으로 전달됩니다.','구조와 조건을 분석하고 변환해\n실행 가능한 형태로 바꿉니다.','코드를 생성하거나\n최적화된 라이브러리를 호출합니다.','역전파와 변하는 입력도 관심사이며,\n구성 요소들이 역할을 나눕니다.','XLA와 torch.compile도\n실제 컴파일 시스템의 사례입니다.','일반 컴파일러와\n분석·IR·변환·코드 생성 원리를 공유합니다.','텐서와 그래프의 의미를 유지하며\n효율적인 실행 프로그램으로 바꿉니다.']
        def base():
            return VGroup(t('AI 컴파일러  /  01',y=7.35,size=21,color=MUTED),t('AI 컴파일러란\n무엇일까?',y=6.45,size=35),Line([-3.9,5.65,0],[3.9,5.65,0],color=MUTED,stroke_opacity=.35),t('텐서의 구조에서 하드웨어 실행까지',y=-7.45,size=19,color=MUTED))
        for i,seg in enumerate(data['segments']):
            # The flip preserves the low-level command card from the prior shot.
            if i==4:
                self.clear();self.add(base(),self.stage)
                self.head=t(titles[i],y=5.05,size=27,color=ACCENT)
                self.cap=t(captions[i],y=-6.25,size=25)
                self.add(self.head,self.cap)
                self.play(self.stage.animate.stretch(.015,0),run_time=.4)
                self.clear();self.add(base(),self.head.copy(),self.cap.copy())
                self.stage=VGroup(box('MatMul\nXW',y=1.3,w=5.8,h=2.3),t('수많은 곱셈 + K축 누적',y=-.5,size=26,color=GOOD))
                self.stage.stretch(.015,0);self.add(self.stage)
                self.play(self.stage.animate.stretch(1/.015,0),run_time=.55)
            else:
                self.clear();self.add(base())
                self.head=t(titles[i],y=5.05,size=27,color=ACCENT)
                self.cap=t(captions[i],y=-6.25,size=25)
                self.stage=self.panel(i)
                self.add(self.head,self.cap)
                self.play(FadeIn(self.stage,shift=UP*.12),run_time=.45)
            note=t(notes[i],y=-4.8,size=20,color=MUTED)
            self.stage.add(note);self.add(note)
            if i in [1,5,13,16,17,18,22]:
                dot=Dot([-3.3,-3.8,0],radius=.07,color=GOOD)
                self.add(dot);self.play(dot.animate.move_to([3.3,-3.8,0]),run_time=.8);self.remove(dot)
            if i==6:
                tiles=VGroup(*[Rectangle(width=.9,height=.9,color=ACCENT,stroke_width=3).move_to([x,y,0]) for x in [-2.95,-2.05] for y in [1.975,1.075]])
                self.stage.add(tiles);self.play(Create(tiles),run_time=.9)
            remaining=seg['end']-self.time
            if remaining < -.04: raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-161)<1/30+.001

    def panel(self,i):
        if i==0:
            return VGroup(box('일반 컴파일러',y=2,w=5.8,h=1.2),t('?',y=.25,size=65,color=ACCENT),box('AI 컴파일러',y=-1.6,w=5.8,h=1.2,color=GOOD))
        if i==1:
            return VGroup(t('Y = ReLU(XW + b)',y=3,size=39,color=ACCENT),chain(['MatMul','Bias Add','ReLU'],.8),t('X · 입력     W · 가중치     b · 편향',y=-1,size=25),t('신경망의 한 층',y=-2.5,color=GOOD))
        if i in [2,3]:
            lines=['Load X[i,k], W[k,j]','Multiply X[i,k] × W[k,j]','Accumulate into C[i,j]','Store C[i,j]']
            if i==3:lines=lines*2
            return VGroup(*[t(s,y=3-j*(.65 if i==3 else 1.2),size=22 if i==3 else 25,color=[MUTED,WEIGHT,ACCENT,SPARSE][j%4]) for j,s in enumerate(lines)],t('for i · for j · for k',y=-3.2,size=23,color=MUTED))
        if i==5:return VGroup(t('Y = ReLU(XW + b)',y=3,size=36,color=ACCENT),chain(['MatMul','Bias Add','ReLU'],.7),t('XW                  + b                max(0, ·)',y=-.6,size=22,color=MUTED))
        if i==6:return VGroup(grid(4,4,-2.5,1.3),t('×',x=-.8,y=1.3,size=35),grid(4,4,.6,1.3,SPARSE),t('→',x=2,y=1.3),box('Y',x=3,y=1.3,w=1),t('크기에 맞는 구현 선택',y=3.3,color=WEIGHT),t('Tile A           Tile B',y=-1.4,color=GOOD),t('계산을 작은 블록으로 나누기',y=-2.7,size=24,color=MUTED))
        if i==7:return VGroup(chain(['MatMul','Bias Add','ReLU'],2.5),t('중간 저장      중간 저장',y=1.3,size=22,color=MUTED),Arrow([0,.8,0],[0,-.15,0],color=ACCENT),box('MatMul + Bias + ReLU',y=-1.2,w=7.1,h=1.4,color=GOOD),t('결합 가능한 실행 후보',y=-2.6,size=24,color=GOOD))
        if i==8:
            return VGroup(*[chain(['MatMul','Bias Add','ReLU'],y) for y in [3,.6,-1.8]],*[Arrow([2.65,y-.5,0],[-2.65,y-1.9,0],color=MUTED,buff=.1) for y in [3,.6]])
        if i==9:return VGroup(box('일반 컴파일러',y=2.5,w=6,color=WEIGHT),box('고수준 IR · 라이브러리 정보',y=.5,w=7,color=SPARSE),box('행렬 연산 최적화',y=-1.5,w=6,color=GOOD),*[Arrow([0,y-.5,0],[0,y-1.5,0],buff=.1,color=MUTED) for y in [2.5,.5]])
        if i in [10,14]:return VGroup(box('분석 단위: 텐서 연산 · 연결 관계',y=2.5,w=7,h=1.2),box('보존 조건: Shape · Dtype · 의존성',y=.5,w=7,h=1.2,color=SPARSE),box('조건에 맞는 변환 · 실행 후보',y=-1.5,w=7,h=1.2,color=GOOD))
        if i==11:return VGroup(grid(3,4,0,1.2),t('X : [M, K]',y=3.1,size=37,color=WEIGHT),t('M · 행 / 입력 묶음',y=-.6),t('K · 곱한 값을 합칠 축',y=-1.7,color=SPARSE),t('Dtype : FP32',y=-2.8,color=GOOD))
        if i==12:return VGroup(t('X[M,K] × W[K,N] → C[M,N]',y=3,size=28,color=WEIGHT),t('C[i,j] = Σₖ X[i,k] W[k,j]',y=1.7,size=31,color=ACCENT),box('K축을 따라 합산',y=.4,w=5.8,color=SPARSE),t('C[M,N] + b[N] → Z[M,N]',y=-1.2,size=29,color=GOOD),t('b를 M축으로 펼쳐 적용',y=-2.5,size=26,color=GOOD))
        if i==13:return VGroup(chain(['MatMul','Bias Add','ReLU'],1.6),t('t1                 t2                  Y',y=.4,size=24,color=ACCENT),t('Y = max(0, t2)',y=-1.4,size=37,color=GOOD),t('입력 결과가 준비된 뒤 실행',y=-2.7,size=25))
        if i in [15,16,17,22]:
            names=['신경망 프로그램','컴파일 시스템','실행 프로그램']
            if i==16:names=['텐서 연산 · 연결 관계','컴파일 시스템','실행 프로그램']
            if i==17:names=['구조·조건 분석','의미를 보존하는 변환','실행 가능한 형태']
            if i==22:names=['텐서 · 연산 그래프','의미를 유지하는 변환','효율적인 실행 프로그램']
            nodes=VGroup(*[box(s,y=y,w=6.6,h=1.2,color=c) for s,y,c in zip(names,[3,.5,-2],[WEIGHT,SPARSE,GOOD])])
            return VGroup(nodes,*[Arrow(a.get_bottom(),b.get_top(),buff=.12,color=MUTED) for a,b in zip(nodes,nodes[1:])])
        if i==18:
            root=box('분석된 계산',y=3,w=5)
            targets=VGroup(*[box(s,x,y=.3,w=2.2,color=c) for s,x,c in zip(['CPU','GPU','AI 가속기'],[-2.7,0,2.7],[WEIGHT,SPARSE,GOOD])])
            return VGroup(root,targets,*[Arrow(root.get_bottom(),b.get_top(),buff=.1,color=MUTED) for b in targets],box('생성 코드  /  연산 라이브러리 호출',y=-2,w=7,color=ACCENT))
        if i==19:return VGroup(box('머신러닝 컴파일 시스템',y=3,w=7,color=ACCENT),box('역전파 계산 구성',x=-1.95,y=.7,w=3.6,h=1.4),box('변하는 입력 크기',x=1.95,y=.7,w=3.6,h=1.4,color=SPARSE),t('프레임워크 · 별도 구성 요소 · 백엔드',y=-1.5,size=25,color=GOOD),t('구현마다 기능과 책임의 경계가 다름',y=-2.7,size=23,color=MUTED))
        if i==20:return VGroup(box('XLA',y=3,w=6,color=WEIGHT),t('머신러닝 계산 → 여러 하드웨어 대상',y=1.9,size=25),box('torch.compile',y=.3,w=6,color=SPARSE),box('TorchDynamo\n그래프 포착',x=-1.95,y=-1.5,w=3.6,h=1.5),box('TorchInductor\n코드 생성',x=1.95,y=-1.5,w=3.6,h=1.5,color=GOOD))
        if i==21:return VGroup(*[box(s,y=y,w=6,color=c) for s,y,c in zip(['분석','중간 표현 · IR','변환','코드 생성'],[3,1.3,-.4,-2.1],[WEIGHT,SPARSE,ACCENT,GOOD])])
        raise ValueError(i)
