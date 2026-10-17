"""Execution cost comes from paths, merged states, and precomputed transitions."""
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
from episodes.aic06_regex_execution.execution_model import EDGES,trace,subsets,splits,count,show_set
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))

def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def box(s,x,y,w=2.2,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=.85,corner_radius=.12,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,24,color,w-.18))
def arrow(a,b,color=MUTED):return Arrow(p(*a),p(*b),buff=.25,color=color,stroke_width=2.4,max_tip_length_to_length_ratio=.16)

def nfa(active=()):
    pos={0:(-3.1,1.5),1:(-.9,1.5),2:(1.3,-.3),3:(2.7,1.5)}
    parts=[];nodes={}
    for a,label,b in EDGES:
        x,y=pos[a];u,v=pos[b];color=WEIGHT if label=='a' else GOOD if label=='b' else MUTED
        if a==b:
            path=CurvedArrow(p(x-.25,y+.35),p(x+.25,y+.35),angle=-TAU*.8,color=color)
            lab=text('a',x,y+1.3,25,color,.6)
        elif (a,b)==(2,1):
            path=CurvedArrow(p(x-.15,y-.4),p(u-.35,v-.15),angle=-PI/2,color=color)
            lab=text('a',-.6,-.4,25,color,.6)
        else:
            path=arrow((x,y),(u,v),color);lab=text(label or 'ε',(x+u)/2,(y+v)/2+.4,25,color,.6)
        parts.extend((path,lab))
    for q,(x,y) in pos.items():
        color=GOOD if q==3 else WEIGHT
        circle=Circle(.36,color=color,fill_color=ACCENT if q in active else BG,fill_opacity=.8 if q in active else 1).move_to(p(x,y))
        nodes[q]=VGroup(circle,text('q'+str(q),x,y,20,INK,.58));parts.append(nodes[q])
        if q==3:parts.append(Circle(.28,color=GOOD).move_to(p(x,y)))
    parts.append(arrow((-4,1.5),(-3.45,1.5),MUTED))
    g=VGroup(*parts);g.nodes=nodes
    return g

def merge_picture():
    return VGroup(box('1 + 1',-2.25,2.7,2.5,WEIGHT),box('2',-2.25,.7,2.5,SPARSE),
        arrow((-1,2.7),(1.25,1.7),WEIGHT),arrow((-1,.7),(1.25,1.7),SPARSE),
        box('q1 · 위치 2',2,1.7,2.4,ACCENT),
        text('같은 상태 · 같은 입력 위치',y=-.8,size=30,color=ACCENT),
        text('남은 입력은 둘 다 aaac',y=-2.2,size=28,color=MUTED))

def comparison():
    data=[('백트래킹','경로를 선택 → 실패하면 되돌리기',WEIGHT),('NFA 시뮬레이션','같은 위치의 중복 상태를 합치기',SPARSE),('DFA 실행','준비된 전이표를 조회하기',GOOD)]
    parts=[]
    for j,(label,desc,color) in enumerate(data):
        y=3.25-j*2.35
        parts.extend((box(label,0,y,5.5,color),text(desc,y=y-.9,size=26,color=color)))
    return VGroup(*parts)

class RegexExecution(Scene):
    DURATION=154
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow: {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def show(self,m,d=.45):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def cue(self,i,title):
        self.to(CUES[i]['start'])
        cap=text(CUES[i]['caption'],y=-6.25,size=26)
        head=text(title,y=5.05,size=27,color=ACCENT)
        anim=[]
        if len(self.stage):anim.append(FadeOut(self.stage))
        if len(self.caption):anim.append(ReplacementTransform(self.caption,cap))
        else:self.add(cap)
        if len(self.head):anim.append(ReplacementTransform(self.head,head))
        else:self.add(head)
        if anim:self.play(*anim,run_time=.2)
        self.caption=cap;self.head=head;self.stage=VGroup()
    def construct(self):
        self.stage=VGroup();self.caption=VGroup();self.head=VGroup()
        self.add(text('AI 컴파일러 / 06',y=7.35,size=21,color=MUTED),text('같은 정규식인데\n왜 실행 속도는 다를까?',y=6.4,size=33),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('같은 수용 언어 · 서로 다른 실행 비용',y=-7.45,size=19,color=MUTED))

        self.cue(0,'01  같은 입력, 서로 다른 계산량')
        self.show(text('(a|aa)*b',y=3.5,size=56,color=ACCENT));self.show(comparison().scale(.77).shift(DOWN*.7))
        self.cue(1,'01  입력 전체를 판정한다')
        self.show(text('(a | aa)* b',y=3.7,size=55,color=ACCENT))
        self.show(VGroup(box('a 또는 aa',-1.65,1.6,3,WEIGHT),box('b',2.3,1.6,1.2,GOOD),arrow((-.1,1.6),(1.55,1.6)),text('0회 이상 반복 → 마지막 b',y=-.2,size=30,color=SPARSE),text('b · ab · aab · aaab · …',y=-2,size=33,color=GOOD),text('부분 검색이 아닌 전체 문자열 수용 여부',y=-4.1,size=23,color=MUTED)))
        self.cue(2,'01  언어가 같아도 계산량은 다르다')
        self.show(VGroup(text('(a|aa)*b',y=3.3,size=52,color=WEIGHT),text('같은 언어',y=1.8,size=28,color=MUTED),text('a*b',y=.2,size=60,color=GOOD),text('같은 결과 ≠ 같은 실행 비용',y=-2.6,size=36,color=ACCENT),text('식의 단순화도 가능한 최적화',y=-4.2,size=23,color=MUTED)))

        self.cue(3,'02  실패를 확인하는 데 드는 비용')
        self.show(VGroup(text('(a|aa)*b',y=3.5,size=45,color=ACCENT),text('a a a a a',x=-.55,y=1.5,size=47,color=WEIGHT,width=5.5),text('c',x=3,y=1.5,size=47,color=PRUNE,width=.7),text('입력: aaaaac',y=-.1,size=30,color=MUTED),text('b로 끝나지 않음 → 거부',y=-2,size=36,color=PRUNE),text('판정 결과와 탐색 비용은 별개',y=-4,size=25,color=MUTED)))
        self.cue(4,'02  하나를 시도하고, 실패하면 돌아간다')
        self.show(VGroup(box('시작',0,3.7,2,ACCENT),box('a 1개',-2,1.5,2,WEIGHT),box('a 2개',2,1.5,2,SPARSE),arrow((0,3.25),(-2,1.95),WEIGHT),arrow((0,3.25),(2,1.95),SPARSE),text('1 + 1 + 1 + 1 + 1  →  c ≠ b',y=-.4,size=27,color=PRUNE)))
        token=self.show(Dot(p(0,3.7),color=ACCENT))
        for pt in [(-2,1.5),(0,-1.5),(-2,1.5),(0,3.7),(2,1.5)]:self.play(token.animate.move_to(p(*pt)),run_time=.3)
        self.show(text('실패 → 이전 선택 → 다른 경로',y=-3.7,size=28,color=ACCENT))
        self.cue(5,'02  a 다섯 개를 나누는 여덟 가지 방법')
        rows=VGroup(*[text(' + '.join(map(str,s)),y=3.65-j*.82,size=29,color=WEIGHT if s[0]==1 else SPARSE) for j,s in enumerate(splits(5))])
        self.show(rows);self.show(text('각 분해는 하나의 선택 경로',y=-3.7,size=26,color=MUTED))
        self.cue(6,'02  작은 문제 두 개로 다시 나뉜다')
        self.show(VGroup(box('T(5)',0,3.8,2,ACCENT),box('1 + 남은 4개',-2,1.8,3.5,WEIGHT),box('2 + 남은 3개',2,1.8,3.5,SPARSE),arrow((0,3.35),(-2,2.25)),arrow((0,3.35),(2,2.25)),text('T(4) = 5',-2,.3,30,WEIGHT,3),text('T(3) = 3',2,.3,30,SPARSE,3),text('T(5) = T(4) + T(3) = 8',y=-1.5,size=34,color=ACCENT),text('T(n) = T(n−1) + T(n−2)',y=-3.1,size=34,color=GOOD),text('T(0)=1, T(1)=1 · 분해 수의 점화식',y=-4.4,size=22,color=MUTED)))
        self.cue(7,'02  반복되는 분기, 지수적으로 늘어나는 경로')
        for j,n in enumerate([5,10,15,20]):
            y=3.4-j*1.7
            self.show(VGroup(text(f'a {n}개',-2.5,y,27,WEIGHT,2),text(f'{count(n):,}가지',1.25,y,35,ACCENT,4)),.25)
        self.show(text('경로 분해 수 · 실행 시간 실측이 아님',y=-4.1,size=23,color=MUTED))
        self.cue(8,'02  단순 경로 탐색의 최악 사례')
        self.show(VGroup(text('중복을 제거하지 않는 탐색',y=3.5,size=32,color=WEIGHT),text('같은 남은 문제를 여러 번 처리',y=1.7,size=30,color=PRUNE),text('실패 입력에서 경로 탐색이 커질 수 있음',y=-.1,size=27,color=PRUNE),Line(p(-3.5,-1.3),p(3.5,-1.3),color=MUTED),text('실제 엔진은 구현과 최적화가 다양함',y=-2.5,size=29,color=GOOD),text('상태 추적 · 식 단순화 · 사전 실패 검사',y=-4,size=25,color=MUTED)))

        self.cue(9,'03  경로를 모두 기억해야 할까?')
        self.show(VGroup(text('여러 경로',y=3.6,size=40,color=WEIGHT),box('1 + 1',-2,1.7,2,WEIGHT),box('2',2,1.7,2,SPARSE),arrow((-2,1.2),(0,-.3)),arrow((2,1.2),(0,-.3)),box('같은 남은 계산',0,-.8,4,ACCENT),text('한 번만 처리할 수 있다면?',y=-3.3,size=34,color=GOOD)))
        self.cue(10,'03  도달 가능한 상태를 집합으로')
        g=self.show(nfa(trace('a')[1]));self.show(text('설명을 위한 동등한 소형 ε-NFA',y=4.1,size=24,color=MUTED))
        self.show(VGroup(text('a 한 글자 뒤: '+show_set(trace('a')[1]),y=-2.1,size=30,color=ACCENT),text('노란 채움 = 현재 가능한 상태',y=-3.3,size=24,color=MUTED),text('여러 경로의 이력 대신 상태 집합 유지',y=-4.5,size=25,color=SPARSE)))
        self.cue(11,'03  같은 위치에서 같은 상태에 도착')
        self.show(merge_picture())
        self.show(text('수용 여부만 판정 · 캡처 결과는 범위 밖',y=-4.3,size=23,color=MUTED))
        self.cue(12,'03  남은 계산이 같으면 한 번만')
        g=self.show(merge_picture())
        self.play(Circumscribe(g[4],color=ACCENT),run_time=.7)
        self.show(text('지나온 경로가 달라도\n중복된 상태는 하나로',y=-4,size=31,color=GOOD))
        self.cue(13,'03  ε-closure → 문자 이동 → ε-closure')
        history=trace('aaaaac');g=self.show(nfa(history[0]))
        self.show(text('입력: aaaaac · 현재 상태 집합',y=4.1,size=25,color=MUTED))
        label=self.show(text('시작: '+show_set(history[0]),y=-2.15,size=31,color=ACCENT))
        for j,states in enumerate(history[1:],1):
            self.play(*[mob[0].animate.set_fill(ACCENT if q in states else BG,opacity=.8 if q in states else 1) for q,mob in g.nodes.items()],Transform(label,text(f'{j}글자 뒤: '+show_set(states),y=-2.15,size=31,color=ACCENT if states else PRUNE)),run_time=.45)
        self.show(text('마지막에 q3 없음 → 거부',y=-4,size=29,color=PRUNE))
        self.cue(14,'03  경로 수와 상태 수는 다르다')
        self.show(VGroup(text('가능한 경로의 수',y=3.6,size=29,color=WEIGHT),text('8 → 89 → 987 → 10,946',y=2.2,size=36,color=PRUNE),text('한 입력 위치의 상태 집합',y=.3,size=30,color=SPARSE),text('최대 m개',y=-1.2,size=49,color=GOOD),text('m = NFA 전체 상태 수',y=-2.6,size=25,color=MUTED),text('같은 입력 위치에서 중복 방문을 제거',y=-4.2,size=26,color=ACCENT)))
        self.cue(15,'03  정규식을 고정하면 입력 길이에 선형')
        self.show(VGroup(text('상태 수 m · 입력 길이 n',y=3.5,size=30,color=MUTED),text('O(mn)',y=1.8,size=65,color=SPARSE),text('정규식 고정 → m은 상수',y=-.1,size=30,color=WEIGHT),text('O(n)',y=-1.8,size=65,color=GOOD),text('상태 집합 유지 ≠ 하드웨어 병렬 실행',y=-4.1,size=24,color=MUTED)))

        self.cue(16,'04  상태 집합 자체를 하나의 상태로')
        self.show(VGroup(box('{q1, q2}',-2,1.8,3,SPARSE),arrow((-.4,1.8),(.9,1.8),GOOD),box('Q1',2.1,1.8,2,GOOD),text('NFA 집합 → DFA 상태',y=-.5,size=34,color=ACCENT),text('같은 가능성을 다른 표현으로',y=-2.5,size=28,color=MUTED)))
        self.cue(17,'04  집합 사이의 전이를 계산한다')
        states,table=subsets()
        self.show(text('이 NFA에서 도달 가능한 집합',y=4.1,size=25,color=MUTED))
        for j,s in enumerate(states):self.show(VGroup(box('Q'+str(j),-2.7,2.8-j*1.45,1.2,GOOD),text(show_set(s),.6,2.8-j*1.45,29,SPARSE,5)),.22)
        self.show(text('Q1에서 a → Q1 · b → Q2 · c → Q3',y=-3.9,size=25,color=ACCENT))
        self.cue(18,'04  준비된 전이표를 조회한다')
        self.show(text('현재 상태      a       b       c',y=3.8,size=28,color=ACCENT))
        for q in range(len(states)):
            self.show(text('Q'+str(q)+'              '+'       '.join('Q'+str(table[q,ch]) for ch in ('a','b','c')),y=2.5-q*1.15,size=28,color=GOOD if 3 in states[q] else INK),.2)
        self.show(VGroup(text('Q0 ─a→ Q1 ─a→ Q1 ─b→ Q2',y=-2.9,size=28,color=GOOD),text('Q2는 수용 · Q3는 거부 상태',y=-4.25,size=24,color=MUTED)))
        self.cue(19,'04  실행 전에 지불하는 비용')
        self.show(VGroup(box('사전 계산',-2,2.1,3,WEIGHT),box('전이표 저장',2,2.1,3,SPARSE),text('준비 시간',-2,.7,29,WEIGHT,3),text('메모리',2,.7,29,SPARSE,3),arrow((-2,.1),(0,-1.4)),arrow((2,.1),(0,-1.4)),box('실행 중 조회',0,-1.9,3.5,GOOD),text('준비 비용과 실행 비용을 구분',y=-4.1,size=27,color=MUTED)))
        self.cue(20,'04  일반적인 최악의 경우: 상태 증가')
        self.show(VGroup(text('NFA 상태 m개',y=3.5,size=36,color=SPARSE),text('가능한 부분집합',y=1.8,size=29,color=MUTED),text('최대 2^m개',y=.1,size=59,color=ACCENT),text('일부 언어에서는 지수적 증가가 필요',y=-2.1,size=28,color=PRUNE),text('지금의 예시가 아니라 일반적인 최악의 경우',y=-4,size=23,color=MUTED)))
        self.cue(21,'04  지금의 예시는 작은 DFA로 충분하다')
        self.show(text('(a|aa)*b ≡ a*b',y=3.8,size=43,color=ACCENT))
        self.show(VGroup(box('시작',-2.3,1.3,2,WEIGHT),box('수용',2.3,1.3,2,GOOD),arrow((-1.25,1.3),(1.25,1.3),GOOD),text('b',0,1.8,26,GOOD),CurvedArrow(p(-2.65,1.9),p(-1.95,1.9),angle=-TAU*.8,color=WEIGHT),text('a',-2.3,2.9,26,WEIGHT),box('거부',0,-1.4,2,PRUNE),arrow((2.3,.8),(.5,-1),PRUNE),arrow((-2.3,.8),(-.5,-1),PRUNE),text('a,b,c',2.2,-.3,21,PRUNE,1.4),text('c',-2.2,-.3,22,PRUNE,.8),text('거부 상태는 이후 모든 입력에서 유지',y=-3,size=24,color=MUTED),text('부분집합 구성 4상태 → 최소화하면 3상태',y=-4.4,size=23,color=GOOD)))

        self.cue(22,'05  빠르고 느린 순위보다 비용 배분')
        self.show(comparison());self.show(text('같은 언어 · 서로 다른 실행 전략',y=-4.2,size=25,color=ACCENT))
        self.cue(23,'05  탐색 · 병합 · 사전 계산')
        g=self.show(comparison())
        for j in range(3):self.play(Circumscribe(g[j*2],color=ACCENT),run_time=.6)
        self.show(text('NFA/DFA는 모델 · 탐색/집합 추적은 알고리즘',y=-4.35,size=22,color=MUTED))
        self.cue(24,'06  AI 컴파일러도 실행 비용을 선택한다')
        self.show(VGroup(box('미리 계산',0,3.1,4.5,WEIGHT),box('결과 저장',0,.8,4.5,SPARSE),box('실행 중 재계산',0,-1.5,4.5,GOOD),text('의미를 보존할 수 있는 조건에서 선택',y=-4,size=27,color=ACCENT)))
        self.cue(25,'06  재사용과 사전 계산')
        self.show(VGroup(text('같은 계산의 결과 재사용',y=3.7,size=29,color=SPARSE),box('공유 계산 f(X)',0,2.3,4,SPARSE),arrow((-.6,1.85),(-2,.8),SPARSE),arrow((.6,1.85),(2,.8),SPARSE),box('사용 1',-2,.3,2.5,GOOD),box('사용 2',2,.3,2.5,GOOD),text('입력에 의존하지 않는 상수 계산',y=-1.5,size=28,color=WEIGHT),text('2 × 3 → 미리 계산한 6',y=-2.9,size=34,color=WEIGHT),text('효과·타입·실행 조건이 허용할 때',y=-4.4,size=23,color=MUTED)))
        self.cue(26,'06  줄어드는 계산과 늘어나는 비용')
        self.show(VGroup(box('재사용',-2,2.5,3,SPARSE),box('사전 계산',2,2.5,3,WEIGHT),text('저장 공간',-2,.9,29,SPARSE,3),text('준비 시간',2,.9,29,WEIGHT,3),text('메모리 접근',-2,-.4,28,SPARSE,3),text('전처리 비용',2,-.4,28,WEIGHT,3),text('계산을 줄여도 다른 비용이 생긴다',y=-2.6,size=31,color=ACCENT),text('전체 비용을 기준으로 실행 전략 선택',y=-4.1,size=25,color=MUTED)))
        self.cue(27,'06  같은 알고리즘이 아닌, 공통된 비용 관점')
        self.show(VGroup(text('정규식 실행',-2,3.2,29,WEIGHT,3.4),text('AI 컴파일러',2,3.2,29,SPARSE,3.4),text('상태 중복 병합',-2,1.5,25,WEIGHT,3.5),text('계산 결과 재사용',2,1.5,25,SPARSE,3.5),text('전이 사전 계산',-2,-.1,25,WEIGHT,3.5),text('상수 계산',2,-.1,25,SPARSE,3.5),text('전이표 저장',-2,-1.7,25,WEIGHT,3.5),text('저장 비용',2,-1.7,25,SPARSE,3.5),text('구체적인 규칙은 다름 · 의미 보존이 전제',y=-3.7,size=25,color=MUTED)))
        self.cue(28,'결론  같은 규칙, 다른 계산 방식')
        self.show(VGroup(text('같은 규칙을 인식해도',y=2.6,size=40,color=INK),text('같은 방식으로\n계산할 필요는 없습니다',y=.2,size=40,color=ACCENT),text('경로 탐색 · 상태 병합 · 전이 조회',y=-3.3,size=28,color=GOOD)))
        self.cue(29,'결론  실행 비용을 바꾸는 선택')
        self.show(VGroup(text('어떤 계산을',y=3,size=38,color=WEIGHT),text('언제 수행하고',y=1.25,size=38,color=SPARSE),text('어떤 결과를 남길 것인가',y=-.5,size=38,color=GOOD),text('같은 의미 · 서로 다른 실행 비용',y=-3.3,size=32,color=ACCENT)))
        self.to(self.DURATION)
