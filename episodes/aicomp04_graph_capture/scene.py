"""Graph capture boundaries, distinct FX/Dynamo examples and runtime execution."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.aicomp01_what_is_ai_compiler.scene import t, box, chain
from visual_library.manim import BG, INK, MUTED, WEIGHT, SPARSE, ACCENT, GOOD, PRUNE, configure_vertical

configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent

def down(a,b,color=MUTED):
    return Arrow(a.get_bottom(),b.get_top(),buff=.12,color=color,stroke_width=2)

def code(branch=False,y=1.4):
    lines=['def forward(x, W, b):','    h = x @ W','    z = h + b','    return torch.relu(z)']
    if branch:lines=['def forward(x, W, b):','    y = x @ W','    if y.sum() > 0:','        y = torch.relu(y)','    return y + b']
    group=VGroup(*[Text(s,font='Consolas',font_size=25,color=ACCENT if branch and i==2 else INK) for i,s in enumerate(lines)])
    group.arrange(DOWN,aligned_edge=LEFT,buff=.28).move_to([0,y,0])
    if group.width>7.1:group.scale_to_fit_width(7.1)
    frame=RoundedRectangle(width=7.7,height=group.height+.7,corner_radius=.12,color=SPARSE if branch else WEIGHT,stroke_width=1.6).move_to(group)
    return VGroup(frame,group)

def branch_graph(runtime=False):
    """A conceptual split, not a literal captured Dynamo graph dump."""
    a=box('Graph A\nMatMul → Sum',y=3.1,w=6.7,h=1.2,color=WEIGHT)
    cond=box('Python · y.sum() > 0',y=1,w=5.4,h=.9,color=ACCENT)
    yes=box('True\nReLU → Add',x=-1.95,y=-1.1,w=3.5,h=1.5,color=GOOD)
    no=box('False\nAdd',x=1.95,y=-1.1,w=3.5,h=1.5,color=SPARSE)
    arrows=VGroup(down(a,cond),down(cond,yes),down(cond,no))
    return VGroup(a,cond,yes,no,arrows,t('이후 포착 가능한 구간' if not runtime else '선택된 경로의 후속 계산',y=-2.7,size=24,color=MUTED))

def dual_trace():
    g=VGroup()
    for x,title,c in [(-2,'실제 실행',WEIGHT),(2,'FX Symbolic Tracing',SPARSE)]:
        g.add(t(title,x,3.3,23,c,3.8))
    left=[box('실제 텐서 원소\n[1.2, −0.3, …]',-2,1.9,w=3.6,h=1.3),box('연산 수행',-2,-.1,w=3.6,h=1.1),box('결과 값',-2,-2.1,w=3.6,h=1.1,color=GOOD)]
    right=[box('Proxy x',2,1.9,w=3.6,h=1.3,color=SPARSE),box('연산 호출 기록',2,-.1,w=3.6,h=1.1,color=SPARSE),box('FX Graph',2,-2.1,w=3.6,h=1.1,color=GOOD)]
    return VGroup(g,VGroup(*left),VGroup(*right),*[down(a,b) for row in [left,right] for a,b in zip(row,row[1:])],Line([0,3.7,0],[0,-3.4,0],color=MUTED,stroke_opacity=.3))

class GraphCaptureBoundaries(Scene):
    def banner(self):
        return VGroup(t('AI 컴파일러  /  04',y=7.35,size=21,color=MUTED),t('파이썬 신경망은 어떻게\n계산 그래프가 될까?',y=6.45,size=31),Line([-3.9,5.65,0],[3.9,5.65,0],color=MUTED,stroke_opacity=.35),t('Graph Capture · Tracing · Graph Break',y=-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads(ROOT.joinpath('timing.json').read_text(encoding='utf-8'))
        titles=['프로그램 전체가 하나의 그래프일까?','코드에서 계산의 관계로','연산과 전달되는 값을 연결한다','Graph Capture · 계산을 포착한다','값을 모두 계산해야 할까?','Tracing · 흐름을 따라 기록하기','FX · 실제 입력 대신 Proxy','숫자 대신 연산과 값의 관계가 남는다','계산하는 것과 기록하는 것은 다르다','FX와 TorchDynamo는 다른 접근','값에 따라 달라지는 Python 분기','실제 결과가 다음 경로를 결정한다','Graph Break · 포착 경계가 끊긴다','포착 중단이 실행 실패는 아니다','포착·컴파일과 실제 실행을 구분','프로그램 하나 · 여러 컴파일 구간','하나의 그래프를 요구한다면?','분기 자체가 표현 불가능한 것은 아니다','포착 범위는 방식과 지원에 따라','넓게 포착하면 함께 분석할 기회','프로그램의 경계 ≠ 그래프의 경계']
        caps=['프로그램의 모든 코드를\n하나의 계산 그래프로 만들 수 있을까요?','변수 할당과 함수 호출 속에서\n텐서 계산의 관계를 살펴봅니다.','MatMul의 결과를 Add가,\nAdd의 결과를 ReLU가 받습니다.','분석하고 변환할 수 있는 계산 표현을\n프로그램에서 얻는 과정입니다.','실제 텐서의 모든 원소를 계산해야만\n그래프를 만들 수 있을까요?','실행 흐름을 따라 연산을 기록하는\n접근을 Tracing이라고 합니다.','FX Symbolic Tracing은 실제 입력 대신\n연산을 기록하는 대리 객체를 사용합니다.','연산 호출마다 노드가 추가되고\n어떤 값이 어디에 쓰이는지가 남습니다.','값을 계산하는 일과\n계산 구조를 기록하는 일은 다릅니다.','torch.compile에서는 TorchDynamo가\nPython 바이트코드를 분석해 포착합니다.','행렬곱 결과의 합이 0보다 클 때만\nReLU를 적용하는 예로 바꿉니다.','어느 경로인지는 실제 결과에 달려 있어\n그대로 포착하기 어려울 수 있습니다.','데이터 의존 분기가\n그래프 포착을 중단시킬 수 있습니다.','그래프가 끊겨도 프로그램 실행이\n반드시 실패하는 것은 아닙니다.','부분 그래프를 컴파일할 수 있고,\n실행 중에는 Python 구간과 이어 수행합니다.','프로그램은 하나여도\n컴파일 대상 그래프는 여러 조각일 수 있습니다.','전체 함수를 한 그래프로 요구하면\n포착할 수 없는 코드에서 오류가 날 수 있습니다.','지원되는 구조화된 분기 연산으로\n데이터 의존 분기를 표현할 수도 있습니다.','같은 프로그램도 포착 방식과\n지원 범위에 따라 다르게 포착됩니다.','함께 분석할 기회가 늘어도\n항상 전체가 한 그래프가 되지는 않습니다.','원래 프로그램의 범위와\n컴파일러가 포착한 범위는 다를 수 있습니다.']
        notes=['Python 코드 전체와 포착 범위를 비교','Y = ReLU(XW + b)','화살표는 값의 사용 관계','단순한 코드 문장 그림이 아님','실제 실행과 Symbolic Tracing 예시 비교','연산 기록 접근의 한 예','Proxy 예시는 FX에만 연결','Proxy는 실제 결과 숫자를 만드는 객체가 아님','실제 값 계산 ≠ 연산 기록','서로 다른 그래프 포착 접근','별도 변형 예시 · ReLU 뒤에 편향 덧셈','데이터 의존 조건 · 크기 분기와 구분','TorchDynamo 예시 · 분할 위치는 개념도','부분 포착을 허용하는 경우','JIT에서는 이 과정이 호출 중 이어질 수 있음','실제 분할 위치·개수는 구현과 설정별','fullgraph=False / True 개념 비교','torch.cond · 지원 범위와 제약이 있음','전체 프로그램 테두리와 포착 경계를 구분','더 넓은 포착이 항상 더 빠름을 보장하지 않음','포착할 수 있는 계산이 컴파일 범위를 결정']
        for i,seg in enumerate(data['segments']):
            self.clear()
            self.add(self.banner(),t(titles[i],y=5.05,size=25,color=ACCENT),t(caps[i],y=-6.25,size=23),t(notes[i],y=-4.8,size=18,color=MUTED))
            panel=self.panel(i)
            self.play(FadeIn(panel,shift=UP*.1),run_time=.4)
            if i==2:
                dot=Dot([-2.65,1.3,0],radius=.09,color=ACCENT);self.add(dot)
                self.play(dot.animate.move_to([0,1.3,0]),run_time=.65);self.play(dot.animate.move_to([2.65,1.3,0]),run_time=.65);self.remove(dot)
            elif i==3:
                self.play(Circumscribe(panel[1],color=ACCENT),run_time=.85)
            elif i==7:
                # Proxy token records nodes; no tensor values travel on this path.
                proxy=box('Proxy',x=-2.65,y=2.5,w=1.6,h=.65,color=SPARSE);self.add(proxy)
                for j,x in enumerate([-2.65,0,2.65]):
                    self.play(proxy.animate.move_to([x,2.5,0]),run_time=.45)
                    self.play(FadeIn(box(['MatMul','Add','ReLU'][j],x,-.1,w=2.15,h=.9,color=GOOD)),run_time=.35)
                self.play(Create(Arrow([-1.45,-.1,0],[-1.2,-.1,0],buff=0,color=MUTED)),Create(Arrow([1.2,-.1,0],[1.45,-.1,0],buff=0,color=MUTED)),run_time=.3)
            elif i==11:
                a=t('sum = +2 → True',y=-2.7,size=28,color=GOOD)
                b=t('sum = −1 → False',y=-2.7,size=28,color=SPARSE)
                self.play(FadeIn(a),run_time=.3);self.wait(1);self.play(Transform(a,b),run_time=.5)
            elif i==12:
                cut=DashedLine([-3.7,2,0],[3.7,2,0],color=PRUNE,stroke_width=3)
                self.play(Create(cut),run_time=.65);self.play(FadeIn(t('Graph Break',x=2.5,y=2.35,size=19,color=PRUNE,width=2.5)),run_time=.3)
            elif i==14:
                # Capture/compile is shown first without real values.
                self.play(Circumscribe(panel[0],color=WEIGHT),run_time=.65)
                self.wait(1.4)
                self.clear();self.add(self.banner(),t('Runtime Execution · 실제 입력으로 실행',y=5.05,size=25,color=GOOD),t(caps[i],y=-6.25,size=23),t('실행 예시: sum = +2 · True 경로만 수행',y=-4.8,size=19,color=MUTED))
                graph=branch_graph(True);self.add(graph)
                dot=Dot([0,3.1,0],radius=.11,color=ACCENT);self.add(dot)
                self.play(Indicate(graph[0],color=ACCENT),run_time=.45)
                self.play(dot.animate.move_to([0,1,0]),run_time=.6)
                self.play(FadeIn(t('sum = +2 → True',y=.1,size=23,color=GOOD)),graph[3].animate.set_opacity(.2),graph[4][2].animate.set_opacity(.2),run_time=.5)
                self.play(dot.animate.move_to([-1.95,-1.1,0]),run_time=.75)
                self.play(Indicate(graph[2],color=ACCENT),run_time=.5);self.remove(dot)
            self.add(self.banner())
            remaining=seg['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining>0:self.wait(remaining)
        assert abs(self.time-152)<1/30+.001

    def panel(self,i):
        if i==0:return VGroup(code(),t('이 함수 전체가 한 그래프일까?',y=-2.2,size=31,color=ACCENT),t('?',y=-3.5,size=50,color=SPARSE))
        if i==1:return VGroup(code(y=2.5),t('Y = ReLU(XW + b)',y=-.4,size=36,color=ACCENT),chain(['MatMul','Add','ReLU'],-2.4))
        if i in [2,3]:return VGroup(t('X · W                       b',y=3.3,size=27,color=WEIGHT),chain(['MatMul','Add','ReLU'],1.3),t('h = XW           z = h + b          y = ReLU(z)',y=-.1,size=22,color=MUTED),box('연산 + 값의 사용 관계',y=-2.2,w=6.6,color=GOOD))
        if i in [4,5,6,8]:return dual_trace()
        if i==7:return VGroup(t('FX Symbolic Tracing',y=3.6,size=28,color=SPARSE),t('연산 호출을 따라 이동',y=1.45,size=25,color=MUTED),box('FX Graph · 연산 기록',y=-2,w=6.8,color=GOOD),t('실제 텐서 결과값을 출력하는 경로가 아님',y=-3.4,size=21,color=MUTED))
        if i==9:
            a=box('FX Symbolic Tracing\nProxy로 연산 기록',x=-1.95,y=2.3,w=3.6,h=1.8,color=SPARSE);b=box('TorchDynamo\nPython 바이트코드 분석',x=1.95,y=2.3,w=3.6,h=1.8,color=WEIGHT);capture=box('Graph Capture',y=-.4,w=6,color=GOOD)
            return VGroup(a,b,capture,down(a,capture),down(b,capture),t('torch.compile의 포착 → TorchDynamo',y=-2.4,size=26,color=WEIGHT))
        if i==10:return VGroup(code(True,y=1.8),t('if y.sum() > 0:',y=-1,size=34,color=ACCENT),t('True: ReLU → Add     False: Add',y=-2.6,size=26,color=MUTED))
        if i==11:return VGroup(box('MatMul 결과 y',y=3,w=6),box('sum(y) > 0 ?',y=1.1,w=5.2,color=ACCENT),box('True\nReLU → Add',x=-1.95,y=-.9,w=3.5,h=1.4,color=GOOD),box('False\nAdd',x=1.95,y=-.9,w=3.5,h=1.4,color=SPARSE))
        if i in [12,13]:
            g=branch_graph()
            return VGroup(g,t('Graph Capture · 포착 범위',y=4.2,size=22,color=WEIGHT),t('포착 중단 ≠ 실행 실패' if i==13 else '연산 기록의 경계',y=-3.6,size=27,color=GOOD if i==13 else PRUNE))
        if i==14:return VGroup(box('Graph Capture + Compile',y=3,w=7,color=WEIGHT),box('Graph A',x=-2.5,y=.6,w=2.15,color=WEIGHT),box('Python 분기',y=.6,w=2.15,color=ACCENT),box('후속 그래프',x=2.5,y=.6,w=2.15,color=GOOD),t('포착한 구간을 컴파일',y=-1.3,size=29,color=WEIGHT),t('다음 화면에서 실제 입력을 실행',y=-2.9,size=25,color=MUTED))
        if i in [15,18,19,20]:
            frame=RoundedRectangle(width=7.8,height=6.6,corner_radius=.15,color=MUTED,stroke_width=1.5).move_to([0,.4,0])
            return VGroup(frame,t('하나의 Python 프로그램',y=3.1,size=27,color=INK),box('포착된 Graph A',y=1.6,w=6,color=WEIGHT),box('일반 Python 처리',y=-.2,w=6,color=ACCENT),box('후속 포착 그래프',y=-2,w=6,color=GOOD),t('프로그램 전체와 포착 범위는 다를 수 있음',y=-3.7,size=23,color=ACCENT))
        if i==16:return VGroup(t('torch.compile 설정 예시',y=3.7,size=24,color=MUTED),box('fullgraph=False',x=-1.95,y=2,w=3.6,color=GOOD),box('fullgraph=True',x=1.95,y=2,w=3.6,color=SPARSE),box('부분 그래프\n+ Python 실행',x=-1.95,y=-.2,w=3.6,h=1.7,color=GOOD),box('단일 그래프 포착\n불가 → 오류 가능',x=1.95,y=-.2,w=3.6,h=1.7,color=PRUNE),t('포착 중단을 허용하는 정책이 다름',y=-2.6,size=27,color=MUTED))
        if i==17:return VGroup(box('지원되는 구조화된 분기',y=3,w=7,color=GOOD),box('torch.cond',y=1,w=5.5,color=SPARSE),box('True 경로',x=-1.95,y=-1.4,w=3.5,color=GOOD),box('False 경로',x=1.95,y=-1.4,w=3.5,color=WEIGHT),Arrow([0,.5,0],[-1.95,-.9,0],buff=.1,color=MUTED),Arrow([0,.5,0],[1.95,-.9,0],buff=.1,color=MUTED),t('분기를 그래프 연산으로 표현',y=-3,size=26,color=GOOD))
        raise ValueError(i)
