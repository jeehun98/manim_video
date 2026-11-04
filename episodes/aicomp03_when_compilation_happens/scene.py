"""Code generation, reuse, dispatch and execution on conceptual timelines."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.aicomp01_what_is_ai_compiler.scene import t, box, chain
from visual_library.manim import BG, INK, MUTED, WEIGHT, SPARSE, ACCENT, GOOD, configure_vertical

configure_vertical()
config.disable_caching = True
ROOT=Path(__file__).resolve().parent

def link(a,b,color=MUTED):
    return Arrow(a.get_bottom(),b.get_top(),buff=.12,color=color,stroke_width=2)

def column(names,ys=None,colors=None):
    ys=ys or [3,.7,-1.6]
    colors=colors or [WEIGHT,SPARSE,GOOD]
    nodes=VGroup(*[box(s,y=y,w=6.3,h=1.1,color=c) for s,y,c in zip(names,ys,colors)])
    return VGroup(nodes,*[link(a,b) for a,b in zip(nodes,nodes[1:])])

def timeline(jit=False,y=1.2):
    """Event positions encode order, never measured elapsed time."""
    line=Arrow([-3.7,y,0],[3.8,y,0],buff=0,color=MUTED,stroke_width=2)
    xs=[-2.75,-.3,2.5]
    labels=['사전 준비','호출 1','호출 2']
    g=VGroup(line)
    for x,label in zip(xs,labels):
        g.add(Line([x,y-.15,0],[x,y+.15,0],color=MUTED),t(label,x,y+.55,22,MUTED,2))
    if jit:
        g.add(box('코드 생성',-.3,y-1.1,w=2.25,h=.75,color=SPARSE),box('실행',1.4,y-1.1,w=.9,h=.75,color=WEIGHT),box('재사용',2.9,y-1.1,w=1.6,h=.75,color=GOOD))
    else:
        g.add(box('코드 생성',-2.75,y-1.1,w=2.25,h=.75,color=SPARSE),box('실행',-.3,y-1.1,w=1.6,h=.75,color=WEIGHT),box('재사용',2.5,y-1.1,w=1.6,h=.75,color=GOOD))
    return g

class WhenCompilationHappens(Scene):
    def banner(self):
        return VGroup(t('AI 컴파일러  /  03',y=7.35,size=21,color=MUTED),t('컴파일러는 언제\n코드를 만들까?',y=6.45,size=34),Line([-3.9,5.65,0],[3.9,5.65,0],color=MUTED,stroke_opacity=.35),t('AOT · JIT · Runtime Dispatch',y=-7.45,size=20,color=MUTED))

    def construct(self):
        data=json.loads(ROOT.joinpath('timing.json').read_text(encoding='utf-8'))
        titles=['실행할 때마다 새로 만들까?','같은 계산을 시간 위에 놓기','먼저 만들고, 보관한다','입력이 오면 준비된 코드로 실행','AOT · 실행 전에 컴파일','미리 아는 조건을 활용할 수 있다','JIT · 코드 없이 첫 호출이 오면?','첫 호출 중 필요한 코드를 만든다','JIT · 실행 과정에서 컴파일','두 번째 호출이 들어온다면?','저장된 코드가 유효하면 재사용','JIT가 매번 컴파일은 아니다','조건이 다른 코드 두 개','현재 입력에 맞는 코드 선택','Runtime Dispatch · 선택하는 작업','선택 조건과 지원 범위는 다양하다','선택은 세 번째 컴파일 방식이 아니다','생성 시점을 같은 시간축에 놓기','만들어진 코드는 재사용하거나 선택','생성 · 선택 · 실행은 다른 작업']
        caps=['같은 신경망을 실행할 때마다\n새 코드를 만들어야 할까요?','Y = ReLU(XW + b)를\n시간의 흐름에 놓아 보겠습니다.','입력이 오기 전에 컴파일하고\n만들어진 실행 프로그램을 보관합니다.','실제 입력이 오면 런타임이\n준비된 프로그램으로 실행을 요청합니다.','코드 생성과 사용 시점이\n서로 떨어져 있습니다.','알려진 크기 · 자료형 · 하드웨어 조건을\n미리 활용할 수 있습니다.','실행 코드가 준비되지 않은 상태에서\n첫 번째 입력이 들어옵니다.','첫 호출 중에 코드를 만들고 실행합니다.\n현재 입력 조건을 참고할 수도 있습니다.','프로그램 실행 과정에서 컴파일합니다.\n여기서는 첫 호출 생성의 예입니다.','앞서 만든 코드가 보관되어 있고,\n이번 입력에도 쓸 수 있다면 어떨까요?','같은 코드를 다시 만들지 않고\n저장된 코드를 꺼내 실행할 수 있습니다.','코드 생성과 생성된 코드의 재사용은\n서로 다른 작업입니다.','Batch = 8인 Code A와\nBatch = 64인 Code B를 준비합니다.','현재 입력의 조건을 확인해\n사용할 수 있는 코드를 고릅니다.','새 코드를 만드는 대신\n이미 준비된 코드 중에서 선택합니다.','크기 외에도 조건은 다양하며,\n한 코드가 여러 크기를 처리할 수도 있습니다.','AOT로 만든 코드도, JIT로 만든 코드도\n실행 중 선택할 수 있습니다.','실행 전에 만들 수도 있고,\n실제 호출 과정에서 만들 수도 있습니다.','유효한 코드는 다시 사용하거나\n여러 구현 중 하나를 골라 실행합니다.','컴파일 시점과 실제 실행 시점은\n반드시 같지 않습니다.']
        notes=['매번 호출 ≠ 매번 코드 생성','성능 비교가 아닌 작업 순서 보기','컴파일 경로의 개념 예시','요청과 실제 계산 완료는 구분','AOT · Ahead-of-Time','실제 입력 전에도 조건은 알 수 있음','JIT · Just-in-Time','첫 호출에서 생성하는 설명용 사례','모든 JIT가 첫 호출 전체를 컴파일하지는 않음','보관되어 있고, 현재 조건에 맞는 경우','Compiler는 새 코드를 만들지 않음','순서 개념도 · 소요 시간 비례 아님','설명용 예시 · 서로 다른 조건의 구현','현재 입력: Batch = 8','Dispatch = 준비된 코드 선택','정확한 Shape 일치만 요구하는 것은 아님','생성 시점과 선택은 다른 축','순서 개념도 · 소요 시간 비례 아님','사용 조건에 맞는 경우','언제 만들고, 무엇을 고르고, 언제 실행할까?']
        for i,seg in enumerate(data['segments']):
            self.clear()
            self.add(self.banner(),t(titles[i],y=5.05,size=26,color=ACCENT),t(caps[i],y=-6.25,size=24),t(notes[i],y=-4.8,size=18,color=MUTED))
            panel=self.panel(i)
            self.play(FadeIn(panel,shift=UP*.1),run_time=.4)
            if i==2:
                card=box('Code A',x=-2.7,y=-2.9,w=2,h=.75,color=SPARSE)
                self.add(card);self.play(card.animate.move_to([0,-2.9,0]),run_time=.85)
            elif i in [3,7,10]:
                token=Dot([0,2.5,0],radius=.1,color=GOOD)
                self.add(token);self.play(token.animate.move_to([0,-2.8,0]),run_time=1.1);self.remove(token)
            elif i==9:
                self.play(Circumscribe(panel[1],color=GOOD),run_time=.75)
            elif i==13:
                self.play(Circumscribe(panel[1],color=ACCENT),run_time=.8)
                self.play(panel[2].animate.set_opacity(.28),run_time=.5)
            elif i==14:
                choice=box('Code A',x=0,y=.7,w=2.4,h=.75,color=ACCENT)
                self.add(choice);self.play(choice.animate.move_to([0,-.65,0]),run_time=1)
            elif i==16:
                self.play(Circumscribe(panel[2],color=ACCENT),run_time=.8)
            self.add(self.banner())
            remaining=seg['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-142)<1/30+.001

    def panel(self,i):
        if i==0:return VGroup(box('같은 신경망 프로그램',y=3,w=6.5),chain(['호출 1','호출 2','호출 3'],.6),t('새 코드?       새 코드?       새 코드?',y=-.7,size=24,color=SPARSE),t('?',y=-2.6,size=65,color=ACCENT))
        if i==1:return VGroup(t('Y = ReLU(XW + b)',y=3.3,size=37,color=ACCENT),chain(['MatMul','Bias Add','ReLU'],1.2),Arrow([-3.6,-1.3,0],[3.7,-1.3,0],color=MUTED,buff=0),t('준비           호출 1           호출 2',y=-2.2,size=25,color=MUTED))
        if i==2:return VGroup(column(['Model','Compiler','실행 프로그램 보관'],ys=[3,1,-1],colors=[WEIGHT,SPARSE,GOOD]),t('아직 실제 입력이 오기 전',y=-3.9,size=25,color=MUTED))
        if i==3:return column(['실제 입력 도착','보관된 Code A + Runtime','GPU · 실행 요청'],colors=[WEIGHT,GOOD,WEIGHT])
        if i==4:return VGroup(t('AOT · Ahead-of-Time',y=3.4,size=29,color=SPARSE),timeline(False,1.5),t('먼저 생성 → 나중에 사용',y=-2.7,size=31,color=GOOD))
        if i==5:return VGroup(box('미리 제공된 입력 조건',y=3,w=6.7,color=ACCENT),box('Shape',x=-2.65,y=1,w=2.15),box('Dtype',y=1,w=2.15,color=SPARSE),box('Hardware',x=2.65,y=1,w=2.15,color=GOOD),box('Compiler',y=-1.3,w=6,color=SPARSE),t('실제 입력값 전체를 미리 알 필요는 없음',y=-3,size=23,color=MUTED))
        if i==6:return VGroup(box('첫 입력 · 호출 1',y=3,w=6,color=WEIGHT),box('코드 보관함\n아직 비어 있음',y=.6,w=6,h=1.6,color=MUTED),t('필요한 코드를 이제 준비',y=-2,size=31,color=SPARSE))
        if i==7:return column(['첫 호출의 입력 조건','Compiler → Code A','Runtime → GPU 실행 요청'],colors=[WEIGHT,SPARSE,GOOD])
        if i==8:return VGroup(t('JIT · Just-in-Time',y=3.5,size=29,color=SPARSE),timeline(True,1.5),t('호출 중 생성 → 실행',y=-2.7,size=31,color=GOOD))
        if i==9:return VGroup(box('두 번째 입력 · 호출 2',y=3,w=6),box('보관된 Code A',y=.7,w=5.8,h=1.25,color=GOOD),box('이번 입력에도 사용 가능?',y=-1.6,w=6,color=ACCENT),link(box('임시',y=3,w=6),box('임시',y=.7,w=6)))
        if i==10:return VGroup(column(['호출 2 · 조건이 맞음','보관된 Code A 사용','Runtime → GPU 실행 요청'],colors=[ACCENT,GOOD,WEIGHT]),t('Compiler · 추가 생성 없음',y=-3.5,size=26,color=MUTED))
        if i==11:return VGroup(t('JIT의 첫 호출',y=3.5,size=25,color=SPARSE),chain(['입력','코드 생성','실행'],2),t('다음 호출 · 조건이 맞으면',y=.1,size=25,color=GOOD),chain(['입력','저장 코드','실행'],-1.5,[WEIGHT,GOOD,WEIGHT]))
        if i in [12,13]:
            return VGroup(box('준비된 두 구현' if i==12 else 'Input · Batch = 8',y=3.2,w=6,color=WEIGHT),box('Code A\nBatch = 8',x=-1.95,y=.6,w=3.5,h=1.8,color=GOOD),box('Code B\nBatch = 64',x=1.95,y=.6,w=3.5,h=1.8,color=SPARSE),t('현재 조건에 맞는 구현',y=-2,size=29,color=ACCENT),t('새 코드 생성이 필요한 장면이 아님',y=-3.3,size=23,color=MUTED))
        if i==14:return VGroup(box('현재 입력 조건',y=3,w=6,color=WEIGHT),box('Runtime Dispatcher',y=1.5,w=6,color=ACCENT),box('선택된 코드로 실행 요청',y=-2.1,w=6,color=GOOD),t('선택',x=2.8,y=-.3,size=26,color=ACCENT))
        if i==15:return VGroup(box('현재 조건 확인',y=3,w=6,color=ACCENT),t('Shape · Dtype · Device · …',y=1.5,size=28,color=MUTED),box('여러 크기를 처리하는 코드',y=-.4,w=7,h=1.25,color=GOOD),t('한 코드로 Batch = 8, 16, …',y=-2,size=27,color=GOOD),t('지원 범위는 구현과 조건에 따라',y=-3.2,size=23,color=MUTED))
        if i==16:
            a=box('AOT로 만든 코드',x=-1.95,y=2.8,w=3.5,h=1.4,color=SPARSE);b=box('JIT로 만든 코드',x=1.95,y=2.8,w=3.5,h=1.4,color=SPARSE);select=box('조건에 맞는 코드 선택',y=.2,w=6.5,color=ACCENT);run=box('Runtime → 실행',y=-2.3,w=6,color=GOOD)
            return VGroup(a,b,select,run,link(a,select),link(b,select),link(select,run))
        if i==17:return VGroup(t('AOT',x=-3.2,y=3.8,size=27,color=SPARSE),timeline(False,2.4),t('JIT',x=-3.2,y=-.1,size=27,color=SPARSE),timeline(True,-1.5))
        if i==18:return VGroup(box('이미 만들어진 코드',y=3,w=6,color=SPARSE),box('유효한 코드 재사용',x=-1.95,y=.6,w=3.5,h=1.5,color=GOOD),box('조건에 맞는 코드 선택',x=1.95,y=.6,w=3.5,h=1.5,color=ACCENT),box('실행 요청 → 하드웨어',y=-2,w=6,color=WEIGHT))
        if i==19:return VGroup(box('생성 · 프로그램을 만든다',y=3,w=7,h=1.1,color=SPARSE),box('선택 · 사용할 코드를 고른다',y=.8,w=7,h=1.1,color=ACCENT),box('실행 · 하드웨어에서 계산한다',y=-1.4,w=7,h=1.1,color=WEIGHT),t('컴파일 시점 ≠ 실행 시점',y=-3.4,size=31,color=GOOD))
        raise ValueError(i)
