"""Value definitions and uses: common IR, shared dataflow and SSA."""
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
from episodes.aic08_ast_to_ir.ir_model import CODE_A,CODE_B,CHAIN,BRANCH
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def box(s,x,y,w=2.5,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=.85,corner_radius=.12,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,25,color,w-.18))
def arrow(a,b,color=MUTED,buff=.45):return Arrow(p(*a),p(*b),buff=buff,color=color,stroke_width=2.3,max_tip_length_to_length_ratio=.18)

def source_pair():
    return VGroup(text('중첩 표현식',y=4.1,size=25,color=WEIGHT),text(CODE_A,y=2.9,size=37,color=WEIGHT),text('중간 변수를 사용한 코드',y=1.3,size=25,color=SPARSE),text(CODE_B,y=-.5,size=33,color=SPARSE),text('표기는 달라도 연산은 같은 순서',y=-3.9,size=27,color=MUTED))

def ast_picture():
    specs=[('할당',0,3.3,ACCENT),('y',-2.9,1.8,WEIGHT),('Call: relu',.8,1.8,GOOD),('+',.8,.3,SPARSE),('@',-.8,-1.2,SPARSE),('b',2.5,-1.2,WEIGHT),('x',-1.7,-2.7,WEIGHT),('W',.1,-2.7,WEIGHT)]
    nodes=[box(s,x,y,2.1 if s.startswith('Call') else 1.2,color) for s,x,y,color in specs]
    links=VGroup(*[Line(nodes[a].get_bottom(),nodes[b].get_top(),color=MUTED,stroke_width=2) for a,b in [(0,1),(0,2),(2,3),(3,4),(3,5),(4,6),(4,7)]])
    return VGroup(links,*nodes)

def flow(branch=False):
    model=BRANCH if branch else CHAIN
    pos={'v0':(0,2.9),'v1':(-2.2,.5),'v2':(2.2,.5),'v3':(0,-2.2)} if branch else {'v0':(0,2.7),'v1':(0,.5),'v2':(0,-1.7)}
    colors={'MatMul':WEIGHT,'Add':ACCENT,'ReLU':GOOD,'Sigmoid':SPARSE}
    nodes={n['id']:box(n['op'],*pos[n['id']],2.7,colors[n['op']]) for n in model.nodes}
    edges={}
    for n in model.nodes:
        for a in n['args']:
            if a in pos:edges[(a,n['id'])]=arrow(pos[a],pos[n['id']],colors[n['op']])
    g=VGroup(*edges.values(),*nodes.values())
    g.add(text('x, W',-2.65,2.9 if branch else 2.7,25,WEIGHT,2),arrow((-1.9,2.9 if branch else 2.7),(-1.35,2.9 if branch else 2.7),WEIGHT,buff=.03))
    if branch:g.add(text('a',.35,1.85,26,WEIGHT,.6),text('b',-1.25,-.7,25,GOOD,.6),text('c',1.25,-.7,25,SPARSE,.6),text('y',0,-3.35,26,ACCENT,.6))
    else:g.add(text('t1',.5,1.6,25,WEIGHT,1),text('t2',.5,-.6,25,SPARSE,1),text('b',-2.65,.5,25,SPARSE,1),arrow((-1.9,.5),(-1.35,.5),SPARSE,buff=.03),text('y',0,-2.9,27,GOOD,1))
    g.nodes=nodes;g.edges=edges
    return g

def ssa_lines():
    return VGroup(text('x₀ = 2',y=3.1,size=40,color=WEIGHT),text('x₁ = x₀ + 3',y=1,size=40,color=SPARSE),text('y₀ = x₁ * 4',y=-1.1,size=40,color=GOOD),arrow((-2,2.5),(-2,1.5),WEIGHT,buff=.03),arrow((-2,.4),(-2,-.6),SPARSE,buff=.03),text('각 사용은 하나의 정의로 연결',y=-3.5,size=29,color=ACCENT))

class AstToIR(Scene):
    DURATION=170
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def show(self,m,d=.45):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def cue(self,i,title):
        self.to(CUES[i]['start']);cap=text(CUES[i]['caption'],y=-6.2,size=26);head=text(title,y=5.05,size=27,color=ACCENT)
        anim=[]
        if len(self.stage):anim.append(FadeOut(self.stage))
        if len(self.caption):anim.append(ReplacementTransform(self.caption,cap))
        else:self.add(cap)
        if len(self.head):anim.append(ReplacementTransform(self.head,head))
        else:self.add(head)
        if anim:self.play(*anim,run_time=.2)
        self.stage=VGroup();self.caption=cap;self.head=head
    def construct(self):
        self.stage=VGroup();self.caption=VGroup();self.head=VGroup()
        self.add(text('AI 컴파일러 / 08',y=7.35,size=21,color=MUTED),text('코드의 모양을 지우면\n무엇이 남을까?',y=6.4,size=34),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('AST → 계산 IR · 값의 정의와 사용',y=-7.45,size=19,color=MUTED))
        self.cue(0,'01  다른 표기, 같은 계산 흐름')
        self.show(source_pair())
        self.cue(1,'01  같다고 말하기 위한 조건')
        self.show(VGroup(text('중첩 표현식 ↔ 중간 변수',y=3.5,size=36,color=ACCENT),box('같은 연산 의미',0,1.6,5,WEIGHT),box('같은 타입·형상',0,-.1,5,SPARSE),box('부작용 조건 확인',0,-1.8,5,GOOD),text('추가 로컬 변수 자체는 관찰 대상에서 제외',y=-4.2,size=23,color=MUTED)))
        self.cue(2,'01  왜 코드를 다시 표현할까?')
        self.show(VGroup(text('소스의 모양',y=2.7,size=43,color=WEIGHT),arrow((0,1.7),(0,.2),ACCENT),text('분석하기 좋은 계산 표현',y=-.7,size=37,color=ACCENT),text('어떤 값이 만들어지고, 어디에서 쓰일까?',y=-3.6,size=28,color=GOOD)))

        self.cue(3,'02  AST: 소스의 구문 구조')
        self.show(ast_picture());self.show(text('할당 · 함수 호출 · 이항 연산',y=-4.35,size=27,color=GOOD))
        self.cue(4,'02  값이 만들어지고 사용되는 관계')
        g=self.show(flow());self.show(text('생산자 → 값 → 소비자',y=4.1,size=32,color=ACCENT));self.show(text('연산 사이의 데이터 의존성을 명시',y=-4.2,size=28,color=GOOD))
        self.cue(5,'02  중간 값의 출처를 이름으로')
        g=self.show(flow());self.show(text('t1 = MatMul(x, W)',y=4.1,size=29,color=WEIGHT));self.show(text('t2 = Add(t1, b) · y = ReLU(t2)',y=-4.2,size=27,color=GOOD))
        for q in ['v0','v1','v2']:self.play(Circumscribe(g.nodes[q],color=ACCENT),run_time=.5)
        self.cue(6,'02  같은 연산과 데이터 의존성으로')
        self.show(VGroup(box('중첩 코드',-2.2,3.5,3.3,WEIGHT),box('중간 변수 코드',2.2,3.5,3.3,SPARSE),arrow((-2.2,2.8),(-.3,1.9),WEIGHT),arrow((2.2,2.8),(.3,1.9),SPARSE)))
        self.show(flow().scale(.66).move_to(p(0,-.9)));self.show(text('계산 IR의 한 예 · 특정 방언의 문법이 아님',y=-4.4,size=23,color=MUTED))
        self.cue(7,'02  완전히 다른 종류로 나누는 것이 아니다')
        self.show(VGroup(text('AST도 연산 관계를 나타냅니다',y=3.3,size=34,color=WEIGHT),box('IR이라는 넓은 범주',0,1.2,6.5,SPARSE),box('AST',-1.6,-.3,2.5,WEIGHT),box('계산 IR',1.6,-.3,2.5,GOOD),text('계산 분석과 변환에 맞춘 표현에 주목',y=-2.8,size=29,color=ACCENT),text('표현의 목적과 추상화 수준',y=-4.2,size=25,color=MUTED)))

        self.cue(8,'03  하나의 결과를 두 연산이 사용한다')
        self.show(flow(True));self.show(text('a = x @ W',y=4.2,size=32,color=WEIGHT));self.show(text('b = relu(a) · c = sigmoid(a) · y = b + c',y=-4.5,size=24,color=MUTED))
        self.cue(9,'03  생산자 하나에서 두 소비자로')
        g=self.show(flow(True));self.show(text('행렬곱은 이 예시에서 한 번 정의',y=4.2,size=29,color=WEIGHT))
        self.play(Circumscribe(g.nodes['v0'],color=ACCENT),run_time=.6)
        for e in [('v0','v1'),('v0','v2')]:self.play(Indicate(g.edges[e],color=ACCENT),run_time=.5)
        self.show(text('두 참조를 같은 값의 정의에 연결',y=-4.5,size=26,color=GOOD))
        self.cue(10,'03  DAG: 방향 비순환 그래프')
        self.show(flow(True));self.show(text('Directed Acyclic Graph',y=4.2,size=30,color=ACCENT));self.show(text('이 순수·직선 계산 예시는 DAG로 표현 가능',y=-4.5,size=24,color=MUTED))
        self.cue(11,'03  준비 조건과 독립적인 두 소비자')
        g=self.show(flow(True));self.show(text('a가 준비되면 두 소비자의 입력 조건 충족',y=4.2,size=27,color=ACCENT))
        self.play(Indicate(g.nodes['v1'],color=GOOD),Indicate(g.nodes['v2'],color=SPARSE),run_time=.8)
        self.show(text('ReLU ↔ Sigmoid 직접 데이터 의존성 없음',y=-4.5,size=25,color=MUTED))
        self.cue(12,'03  마지막 연산은 두 값을 모두 필요로 한다')
        g=self.show(flow(True))
        self.play(Indicate(g.edges['v1','v3'],color=GOOD),Indicate(g.edges['v2','v3'],color=SPARSE),run_time=.8)
        self.show(text('Add는 b와 c를 모두 입력으로 사용',y=4.2,size=28,color=ACCENT));self.show(text('a가 사용 가능해야 함 ≠ 별도 DRAM 저장 강제',y=-4.5,size=23,color=MUTED))
        self.cue(13,'03  데이터 흐름과 실행 계획은 구분한다')
        self.show(VGroup(box('의존성 분석',0,3.3,5,WEIGHT),text('무엇을 기다리는가 · 무엇을 공유하는가',y=1.7,size=28,color=WEIGHT),box('실제 실행 계획',0,-.2,5,SPARSE),text('부작용 · 메모리 · 하드웨어 자원 확인',y=-1.8,size=27,color=SPARSE),text('직접 의존성이 없다고 동시 실행이 보장되지는 않음',y=-4,size=23,color=MUTED)))

        self.cue(14,'04  같은 이름이 다른 값을 나타낸다')
        self.show(VGroup(text('x = 2\nx = x + 3\ny = x * 4',y=1.9,size=45,color=WEIGHT),text('같은 x, 서로 다른 정의',y=-2.2,size=34,color=ACCENT),text('이 코드의 y는 20',y=-3.9,size=29,color=GOOD)))
        self.cue(15,'04  이름보다 값의 출처를 구별한다')
        self.show(VGroup(box('처음 x',-2.1,2.7,3.2,WEIGHT),box('다음 x',2.1,2.7,3.2,SPARSE),text('2',-2.1,.8,65,WEIGHT,2),text('5',2.1,.8,65,SPARSE,2),arrow((-1,.8),(1,.8),ACCENT),text('+3',0,1.4,28,ACCENT,1.4),text('x * 4는 어느 x를 사용하는가?',y=-1.8,size=34,color=ACCENT),text('마지막 정의의 값 5를 사용 → 20',y=-3.7,size=29,color=GOOD)))
        self.cue(16,'04  서로 다른 정의에 서로 다른 이름')
        g=self.show(ssa_lines());self.show(text('x₀ = 처음 정의 · x₁ = 다음 정의',y=4.4,size=25,color=MUTED))
        self.cue(17,'04  SSA: 정적 단일 할당')
        self.show(VGroup(text('Static Single Assignment',y=3.5,size=35,color=ACCENT),text('각 SSA 이름은 하나의 정적 정의',y=1.8,size=31,color=GOOD),text('x₀ = 2',y=.1,size=39,color=WEIGHT),text('x₁ = x₀ + 3',y=-1.5,size=39,color=SPARSE),text('프로그램 실행 횟수를 한 번으로 제한하는 뜻은 아님',y=-4,size=23,color=MUTED)))
        self.cue(18,'04  각 사용을 해당 정의로 추적한다')
        g=self.show(ssa_lines())
        for j in range(3):self.play(Circumscribe(g[j],color=ACCENT),run_time=.5)
        self.cue(19,'04  제어 흐름이 있으면 값의 연결도 필요하다')
        self.show(VGroup(box('분기 경로 1',-2,3.2,3.4,WEIGHT),box('분기 경로 2',2,3.2,3.4,SPARSE),text('x_left',-2,1.9,28,WEIGHT,3),text('x_right',2,1.9,28,SPARSE,3),arrow((-2,1.3),(0,.1),WEIGHT),arrow((2,1.3),(0,.1),SPARSE),box('합류 값',0,-.3,3.3,ACCENT),text('φ 노드 / 블록 인수 등',y=-1.9,size=28,color=GOOD),text('반복에서도 제어 흐름에 맞는 값 연결이 필요',y=-3.5,size=26,color=MUTED),text('이름에 번호를 붙이는 것 이상의 표현 방식',y=-4.6,size=24,color=ACCENT)))

        self.cue(20,'05  분석 가능한 계산 관계')
        self.show(VGroup(box('반복된 계산?',0,3.2,5.4,WEIGHT),box('공유되는 값?',0,1.1,5.4,SPARSE),box('연산의 의존성?',0,-1,5.4,GOOD),text('정의와 사용 관계가 분석의 출발점',y=-3.7,size=31,color=ACCENT)))
        self.cue(21,'05  변환을 선택하기 위한 표현')
        self.show(VGroup(box('저장',-2.5,2.5,2.2,WEIGHT),box('재사용',0,2.5,2.2,SPARSE),box('커널 결합',2.5,2.5,2.2,GOOD),text('메모리 비용 · 재계산 비용 · 실행 비용',y=.2,size=29,color=MUTED),text('구조를 바탕으로 선택을 검토',y=-2.3,size=34,color=ACCENT),text('IR이 있다고 모든 변환이 자동 적용되지는 않음',y=-4.2,size=23,color=MUTED)))
        self.cue(22,'05  표현 생성과 성능 개선은 별개')
        self.show(VGroup(text('IR 생성 ≠ 자동 최적화',y=3.3,size=42,color=ACCENT),box('의미를 보존하는가?',0,1.2,5.5,WEIGHT),box('실제 비용이 줄어드는가?',0,-.8,5.5,SPARSE),text('합법성과 비용을 함께 확인',y=-3.5,size=32,color=GOOD)))
        self.cue(23,'결론  다른 코드, 공통된 계산 표현')
        self.show(VGroup(box('중첩 표현식',-2.1,3.1,3.5,WEIGHT),box('중간 변수 코드',2.1,3.1,3.5,SPARSE),arrow((-2.1,2.5),(0,1.2),WEIGHT),arrow((2.1,2.5),(0,1.2),SPARSE),box('공통 계산 IR',0,.6,5,ACCENT),text('연산 · 데이터 의존성 · 정의와 사용',y=-2.2,size=29,color=GOOD)))
        self.cue(24,'결론  컴파일러가 코드를 다시 표현하는 이유')
        self.show(VGroup(text('어떤 값이 만들어지고',y=3,size=39,color=WEIGHT),text('어디에서 사용되는가',y=1.4,size=39,color=SPARSE)))
        self.show(flow(True).scale(.63).move_to(p(0,-1.6)));self.show(text('분석하고 변환하기 좋은 구조로',y=-4.5,size=30,color=ACCENT))
        self.to(self.DURATION)
