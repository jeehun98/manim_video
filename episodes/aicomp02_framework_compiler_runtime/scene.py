"""Functional roles of framework, compiler and runtime; user-paced 141s."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.aicomp01_what_is_ai_compiler.scene import t, box, chain
from visual_library.manim import BG, INK, MUTED, WEIGHT, SPARSE, ACCENT, GOOD, configure_vertical

configure_vertical()
config.disable_caching = True
ROOT = Path(__file__).resolve().parent

def arrow(a,b,color=MUTED):
    return Arrow(a.get_bottom(),b.get_top(),buff=.12,color=color,stroke_width=2)

def stack(names,ys=None,colors=None,w=6.3):
    ys=ys or [3, .7, -1.6]
    colors=colors or [WEIGHT,SPARSE,GOOD]
    nodes=VGroup(*[box(s,y=y,w=w,h=1.1,color=c) for s,y,c in zip(names,ys,colors)])
    return VGroup(nodes,*[arrow(a,b) for a,b in zip(nodes,nodes[1:])])

class FrameworkCompilerRuntime(Scene):
    def banner(self):
        return VGroup(t('AI 컴파일러  /  02',y=7.35,size=21,color=MUTED),t('컴파일러는\n어디에 있을까?',y=6.45,size=35),Line([-3.9,5.65,0],[3.9,5.65,0],color=MUTED,stroke_opacity=.35),t('Framework · Compiler · Runtime',y=-7.45,size=20,color=MUTED))

    def construct(self):
        data=json.loads(ROOT.joinpath('timing.json').read_text(encoding='utf-8'))
        titles=['실행 버튼 뒤에서는 누가 일할까?','하나의 신경망 프로그램','Framework · 계산을 표현한다','사용할 수 있는 연산과 실행 환경','Compiler · 계산의 구조를 받는다','구조와 조건을 분석한다','실행 가능한 프로그램을 만든다','만드는 것과 실행하는 것은 다르다','Runtime · 메모리를 준비한다','실행 요청과 완료는 다르다','준비된 작업을 실제 실행으로','코드와 함께 계획을 전달한다','세 프로그램이 아니라 세 역할','항상 거치는 고정 순서는 아니다','Eager Execution · 또 다른 실행 방식','준비된 구현을 호출할 수 있다','표현하고, 실행 프로그램으로 바꾸고','준비된 작업의 실행을 관리한다','하나의 신경망을 위한 협력']
        caps=['코드가 GPU 계산이 되기까지,\n누가 어떤 일을 할까요?','행렬곱 → 편향 덧셈 → ReLU로\n이어지는 프로그램입니다.','텐서와 연산을 사용해\n신경망 모델을 구성합니다.','연산 인터페이스를 제공하고\n입력과 장치에 맞춰 실행을 지원합니다.','연결된 포착 기능이 계산의 일부를\n컴파일러가 다룰 표현으로 바꿉니다.','연산 관계 · 크기 · 자료형 · 하드웨어로\n실행 방법을 검토합니다.','실행 코드를 생성하거나\n연산 라이브러리를 호출하도록 구성합니다.','프로그램을 만들었다고\nGPU 계산까지 끝난 것은 아닙니다.','필요한 메모리를 준비하거나 재사용하고\n입력과 출력을 연결합니다.','실행 요청 뒤에도 계산은 진행됩니다.\n필요한 작업이 끝나야 결과를 사용합니다.','런타임은 준비된 작업을\n실제 실행으로 연결하고 관리합니다.','컴파일러의 메모리 계획을 활용해\n런타임이 실제 메모리를 준비할 수 있습니다.','상자는 제품이 아니라 역할입니다.\n한 시스템 안에 여러 기능이 들어갈 수 있습니다.','모든 실행이 세 단계를\n차례대로 거치는 것은 아닙니다.','연산 호출에 따라 준비된 구현을 선택하고\n런타임 기능을 통해 실행을 요청합니다.','모델의 별도 그래프 컴파일 없이도,\n이미 컴파일된 연산 구현을 사용할 수 있습니다.','프레임워크는 표현과 실행을 지원하고,\n컴파일러는 실행 프로그램으로 변환합니다.','런타임은 준비된 작업을\n하드웨어에서 수행하도록 관리합니다.','독립된 프로그램도, 고정 단계도 아닙니다.\n신경망 실행을 위해 협력하는 역할들입니다.']
        notes=['Y = ReLU(XW + b)','같은 계산을 끝까지 따라갑니다','사용자가 계산을 작성하는 인터페이스','Tensor · Operator · Device','컴파일 경로의 예 · 포착 범위는 시스템별','어떻게 실행할지 검토하는 단계','생성 코드 + 라이브러리 호출','실행할 프로그램 ≠ 계산 완료','기존 버퍼도 재사용 가능','요청 → 계산 진행 → 완료 → 결과 사용','GPU가 실제 계산을 수행','코드 + 실행에 필요한 계획 · 구성은 시스템별','경계와 책임 분담은 시스템마다 다름','컴파일 경로와 준비된 구현 호출 경로','즉시 실행도 실행 요청과 완료는 구분','컴파일 기술이 전혀 없다는 뜻은 아님','기능적 역할로 바라보기','실제 실행 요청과 필요한 완료 관리','표현 · 변환 · 실행의 협력']
        for i,seg in enumerate(data['segments']):
            self.clear();self.add(self.banner(),t(titles[i],y=5.05,size=26,color=ACCENT),t(caps[i],y=-6.25,size=24),t(notes[i],y=-4.8,size=19,color=MUTED))
            panel=self.panel(i)
            self.play(FadeIn(panel,shift=UP*.1),run_time=.45)
            if i==4:
                dot=Dot([-2.5,2.65,0],radius=.09,color=WEIGHT)
                self.add(dot);self.play(dot.animate.move_to([0,.8,0]),run_time=.8);self.remove(dot)
                self.play(Circumscribe(panel[0][1],color=SPARSE),run_time=.65)
            elif i==7:
                self.play(Circumscribe(panel[0][1],color=ACCENT),run_time=.8)
                self.play(Indicate(panel[1],color=GOOD),run_time=.65)
            elif i==8:
                token=box('재사용',x=-2.5,y=.1,w=1.5,h=.65,color=GOOD)
                self.add(token);self.play(token.animate.move_to([0,-.55,0]),run_time=.9)
            elif i==9:
                self.wait(.8)
                marker=Dot([-2.7,1.2,0],radius=.12,color=ACCENT)
                self.add(marker)
                self.play(marker.animate.move_to([0,1.2,0]),run_time=1.1)
                self.wait(.6)
                self.play(marker.animate.move_to([2.7,1.2,0]),run_time=1.1)
                self.play(FadeIn(t('완료된 결과를 사용',y=-3.1,size=24,color=GOOD)),run_time=.2)
            elif i==11:
                parcel=box('코드 + 계획',x=0,y=.3,w=3.1,h=.85,color=ACCENT)
                self.add(parcel);self.play(parcel.animate.move_to([0,-.45,0]),run_time=1.1)
            elif i in [14,17]:
                dot=Dot([0,2.7,0],radius=.08,color=GOOD)
                self.add(dot);self.play(dot.animate.move_to([0,-2.3,0]),run_time=1);self.remove(dot)
            # Re-add the banner after transient animation cleanup so it remains
            # present during the held frame as well as the animated transition.
            self.add(self.banner())
            remaining=seg['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-141)<1/30+.001

    def panel(self,i):
        if i==0:
            return VGroup(box('Python\ny = relu(x @ w + b)',y=2.6,w=6.7,h=1.6),box('실행 ▶',y=.3,w=2.8,h=1,color=ACCENT),box('GPU',y=-2,w=4,h=1.1,color=GOOD),t('?',x=2.7,y=.2,size=50,color=ACCENT))
        if i==1:return VGroup(t('Y = ReLU(XW + b)',y=3,size=37,color=ACCENT),chain(['MatMul','Bias Add','ReLU'],.8),t('X · 입력     W · 가중치     b · 편향',y=-1.2,size=25),t('하나의 프로그램',y=-2.7,color=GOOD))
        if i==2:return VGroup(box('Framework',y=3,w=7,color=WEIGHT),box('텐서 X · W · b',y=1.4,w=5.8),chain(['MatMul','Bias Add','ReLU'],-.4),t('텐서 + 연산 → 모델 구성',y=-2.4,size=30,color=WEIGHT))
        if i==3:return VGroup(box('Framework',y=3,w=7),box('연산 API',x=-1.9,y=.9,w=3.5,h=1.4),box('입력 · 장치 정보',x=1.9,y=.9,w=3.5,h=1.4,color=SPARSE),t('X.shape   ·   FP32   ·   GPU',y=-1,size=29,color=ACCENT),t('표현하고, 실행을 지원',y=-2.5,color=WEIGHT))
        if i==4:return stack(['프레임워크의 계산','연결된 그래프 포착 기능','컴파일러가 다룰 표현'])
        if i==5:return VGroup(chain(['MatMul','Bias Add','ReLU'],2.8),box('Shape · Dtype',x=-1.9,y=.5,w=3.5,h=1.2,color=WEIGHT),box('Target Hardware',x=1.9,y=.5,w=3.5,h=1.2,color=SPARSE),t('구조와 조건 → 실행 방법 검토',y=-1.6,size=29,color=ACCENT),t('분석 · 변환',y=-3,color=SPARSE))
        if i==6:
            root=box('Compiler',y=3,w=5.7,color=SPARSE)
            a=box('실행 코드 생성',x=-1.9,y=.6,w=3.5,h=1.5,color=WEIGHT);b=box('연산 라이브러리\n호출',x=1.9,y=.6,w=3.5,h=1.5,color=GOOD)
            return VGroup(root,a,b,arrow(root,a),arrow(root,b),box('실행할 프로그램',y=-2,w=6,color=ACCENT))
        if i==7:
            flow=stack(['Compiler','실행할 프로그램'],ys=[3,.6],colors=[SPARSE,ACCENT])
            gpu=box('GPU · 아직 실행 전',y=-2,w=6,color=MUTED)
            return VGroup(flow,gpu,t('만들기',x=2.7,y=1.8,size=23,color=SPARSE))
        if i==8:return VGroup(box('Runtime',y=3,w=6,color=GOOD),box('입력 버퍼',x=-2.5,y=.9,w=2),box('기존 버퍼',y=.9,w=2,color=GOOD),box('출력 버퍼',x=2.5,y=.9,w=2,color=SPARSE),box('실행 프로그램에 연결',y=-1.5,w=6,color=ACCENT),t('준비 / 재사용',y=-3,size=27,color=GOOD))
        if i==9:
            nodes=VGroup(*[box(s,x,2.1,w=2.2,color=c) for s,x,c in zip(['실행 요청','계산 진행','완료'],[-2.7,0,2.7],[WEIGHT,ACCENT,GOOD])])
            return VGroup(nodes,Line([-2.7,1.2,0],[2.7,1.2,0],color=MUTED),box('GPU 작업 A',x=-1.8,y=-.4,w=3,color=WEIGHT),box('결과를 쓰는 작업 B',x=1.8,y=-1.8,w=3.5,color=GOOD),Arrow([-.3,-.6,0],[.2,-1.5,0],color=ACCENT,buff=.1))
        if i==10:return stack(['준비된 프로그램','Runtime · 실행 요청과 관리','GPU · 실제 계산 수행'],colors=[ACCENT,GOOD,WEIGHT])
        if i==11:return VGroup(box('Compiler',y=3,w=6,color=SPARSE),box('실행 코드',x=-1.9,y=1.5,w=3.5,color=WEIGHT),box('메모리 사용 계획',x=1.9,y=1.5,w=3.5,color=ACCENT),box('Runtime',y=-1.6,w=6,color=GOOD),t('계획에 맞춰 메모리 준비 · 재사용',y=-3,size=25,color=GOOD))
        if i==12:
            frame=DashedVMobject(RoundedRectangle(width=7.7,height=6,corner_radius=.2,color=MUTED).move_to([0,.3,0]),num_dashes=45)
            return VGroup(frame,t('하나의 시스템',y=2.7,size=25,color=MUTED),box('Framework\n표현 · 실행 지원',x=-1.7,y=1,w=3.5,h=1.6),box('Compiler\n프로그램 변환',x=1.7,y=1,w=3.5,h=1.6,color=SPARSE),box('Runtime\n실행 관리',y=-1.2,w=4.5,h=1.5,color=GOOD),t('제품 이름이 아니라 기능의 구분',y=-3.5,size=24,color=ACCENT))
        if i==13:
            return VGroup(t('컴파일 경로의 예',y=3.4,size=23,color=SPARSE),chain(['Framework','Compiler','Runtime'],2),t('준비된 구현을 호출하는 경로',y=.1,size=23,color=GOOD),box('Framework',x=-2,y=-1.6,w=3),box('Runtime 기능',x=2,y=-1.6,w=3,color=GOOD),Arrow([-.4,-1.6,0],[.4,-1.6,0],buff=.05,color=GOOD))
        if i==14:return stack(['연산 호출','준비된 구현 선택','Runtime 기능 → 실행 요청'],colors=[WEIGHT,ACCENT,GOOD])
        if i==15:return VGroup(box('지금 작성한 신경망',y=3,w=6),t('별도 그래프 컴파일 없이',y=1.5,size=26,color=MUTED),box('이미 준비된 연산 구현',y=0,w=6,color=ACCENT),t('구현 자체는 이미 컴파일되어 있을 수 있음',y=-1.5,size=23,color=GOOD),box('실행 요청 → 하드웨어',y=-3,w=6,color=GOOD))
        if i==16:return VGroup(box('Framework',y=3,w=6),t('신경망 프로그램 표현 · 실행 지원',y=1.8,size=26,color=WEIGHT),box('Compiler',y=-.2,w=6,color=SPARSE),t('계산 분석 → 실행 프로그램으로 변환',y=-1.5,size=26,color=SPARSE))
        if i==17:return stack(['준비된 작업','Runtime · 실행 관리','Hardware · 실제 수행'],colors=[ACCENT,GOOD,WEIGHT])
        if i==18:
            nodes=VGroup(box('Framework\n표현 · 실행 지원',x=-1.8,y=2,w=3.5,h=1.6),box('Compiler\n프로그램 변환',x=1.8,y=2,w=3.5,h=1.6,color=SPARSE),box('Runtime\n실행 관리',y=-.5,w=4,h=1.5,color=GOOD))
            return VGroup(nodes,arrow(nodes[0],nodes[2]),arrow(nodes[1],nodes[2]),t('Y = ReLU(XW + b)',y=-2.6,size=34,color=ACCENT),t('하나의 계산을 위한 협력',y=-3.6,size=27,color=GOOD))
        raise ValueError(i)
