"""Finite binary memory, unbounded input length, and regular languages."""
import json
import sys
from pathlib import Path
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from visual_library.manim import configure_vertical, txt, BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD
configure_vertical()
config.disable_caching = True
CUES = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))

def p(x,y): return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):
    return txt(str(s),size,color,width).move_to(p(x,y))
def neuron(x,y,name):
    return VGroup(Circle(.48,color=WEIGHT,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(name,x,y,23))
def network(y=1,names=('N₁','N₂','N₃')):
    nodes=VGroup(neuron(-2,y+1,names[0]),neuron(-2,y-1,names[1]),neuron(1.8,y,names[2]))
    edges=VGroup(*[Arrow(n.get_right(),nodes[2].get_left(),buff=.12,color=MUTED) for n in nodes[:2]])
    return VGroup(edges,nodes)
def automaton(y=1.1):
    nodes=VGroup(*[VGroup(Circle(.55,color=c).move_to(p(x,y)),text(s,x,y,25)) for x,s,c in [(-2.5,'q₀',WEIGHT),(0,'q₁',GOOD),(2.5,'q×',PRUNE)]])
    nodes[1].add(Circle(.45,color=GOOD).move_to(p(0,y)))
    edges=VGroup(Arrow(p(-3.7,y),p(-3.1,y),buff=0,color=MUTED),
        Arrow(p(-1.9,y),p(-.6,y),buff=0,color=GOOD),text('B',-1.25,y+.42,25,GOOD),
        Arrow(p(.6,y),p(1.9,y),buff=0,color=PRUNE),text('A, B',1.25,y+.42,22,PRUNE))
    for x,s,c in [(-2.5,'A',WEIGHT),(2.5,'A, B',PRUNE)]:
        edges.add(ArcBetweenPoints(p(x-.35,y+.42),p(x+.35,y+.42),angle=-TAU*.8,color=c),
                  Triangle(color=c,fill_opacity=1).scale(.07).rotate(PI).move_to(p(x+.35,y+.42)),text(s,x,y+1.65,24,c))
    return VGroup(edges,nodes,text('시작',-2.5,y-.95,21,MUTED),text('수용 후보',0,y-.95,21,GOOD),text('거부',2.5,y-.95,21,PRUNE))

class NeuronsRegex(Scene):
    DURATION=192
    def show(self,mob,d=.35):
        self.play(FadeIn(mob),run_time=d);self.stage.add(mob);return mob
    def to(self,t):
        if self.time>t+1/30: raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def cue(self,i):
        cue=CUES[i];self.to(cue['start'])
        new=text(cue['caption'],y=-6.2,size=26)
        if len(self.caption):self.play(ReplacementTransform(self.caption,new),run_time=.2)
        else:self.add(new)
        self.caption=new
    def section(self,title):
        if len(self.stage):self.play(FadeOut(self.stage),FadeOut(self.head),run_time=.3)
        self.stage=VGroup();self.head=text(title,y=5.05,size=28,color=ACCENT);self.add(self.head)
    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(text('AI 컴파일러  /  01',y=7.35,size=21,color=MUTED),
                 text('유한한 뉴런으로\n무한한 패턴을?',y=6.4,size=34),
                 Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),
                 text('신경망에서 정규 표현식까지',y=-7.45,size=19,color=MUTED))
        self.section('01  유한한 뉴런, 무한한 패턴');self.cue(0)
        net=self.show(network(1.5));self.show(text('3개 뉴런 · 인식 장치의 개념도',y=-.7,size=21,color=MUTED))
        self.cue(1)
        incoming=self.show(text('B  →  입력 종료',y=3.9,size=29,color=GOOD))
        for s in ['B','AB','AAB','AAAB']:
            self.play(Transform(incoming,text(s+'  →  입력 종료',y=3.9,size=29,color=GOOD)),Indicate(net[1][2],color=GOOD),run_time=.65)
        self.cue(2);self.show(text('A를 반복한 뒤 B · 종료 때 판정',y=-1.8,color=GOOD))
        for s in ['BA','ABA']:
            self.play(Transform(incoming,text(s+'  →  입력 종료: 거부',y=3.9,size=27,color=PRUNE)),run_time=.65)
        self.cue(3)
        self.show(VGroup(text('A × 100  + B',y=-2.8,color=WEIGHT),text('A × 1000 + B',y=-3.65,color=WEIGHT),text('…',y=-4.4,color=WEIGHT)))
        self.cue(4);self.play(Circumscribe(net,color=ACCENT),run_time=.8);self.to(29.7)

        self.section('02  뉴런을 논리로 표현하다');self.cue(5)
        self.show(VGroup(text('1943',y=4,size=44,color=ACCENT),text('Warren McCulloch · Walter Pitts',y=3.1,size=24),text('발화 / 비발화의 형식적 모형',y=2.4,size=22,color=MUTED)))
        net=self.show(network(.1,('A','B','C')));self.cue(6)
        self.show(text('조건 충족 → 1     그 외 → 0',y=-2,color=WEIGHT))
        self.cue(7)
        formula=self.show(text('C(t + 1) = A(t) ∧ B(t)',y=-3,size=32,color=ACCENT))
        result=self.show(text('A = 1, B = 0  →  C = 0',y=-4,size=26))
        for a,b in [(1,0),(0,1),(1,1)]:
            self.play(Transform(result,text(f'A = {a}, B = {b}  →  C = {a*b}',y=-4,size=26,color=GOOD if a*b else MUTED)),
                net[1][0][0].animate.set_fill(GOOD if a else BG,opacity=1),net[1][1][0].animate.set_fill(GOOD if b else BG,opacity=1),run_time=.7)
            self.play(net[1][2][0].animate.set_fill(GOOD if a*b else BG,opacity=1),run_time=.35)
        self.cue(8)
        self.show(VGroup(CurvedArrow(p(2.3,.1),p(-2,.8),angle=PI/2,color=SPARSE),text('이전 시각 → 다음 시각',y=-1.25,size=23,color=SPARSE)))
        self.cue(9);self.show(text('역사적 형식 신경망 · 현대 딥러닝과 구분',y=-4.85,size=20,color=MUTED));self.to(62.7)

        self.section('03  과거를 모두 저장하지 않는다');self.cue(10)
        machine=self.show(automaton(1.4));self.show(text('입력 알파벳 {A, B} · 전체 문자열 판정',y=4.25,size=22,color=MUTED))
        self.cue(11);self.show(text('A의 개수 대신 현재 상태',y=-.3,size=30,color=ACCENT))
        self.cue(12)
        letters=self.show(VGroup(*[text(c,(k-2.5)*.75,-2,36,WEIGHT if c=='A' else GOOD) for k,c in enumerate('AAAAAB')]))
        token=self.show(Dot(p(-2.5,1.4),radius=.12,color=ACCENT))
        for k in range(5):
            self.play(Indicate(letters[k],color=ACCENT),Indicate(machine[1][0],color=WEIGHT),run_time=.6)
        self.cue(13);self.play(Indicate(letters[5]),token.animate.move_to(p(0,1.4)),run_time=.7)
        self.show(text('B 도착: 아직 입력 종료 전',y=-3.15,size=24,color=MUTED))
        self.cue(14);verdict=self.show(text('AAAAAB 종료 → 수용',y=-4.1,size=29,color=GOOD))
        self.cue(15);self.play(token.animate.move_to(p(2.5,1.4)),Transform(verdict,text('AAAAABA 종료 → 거부',y=-4.1,size=29,color=PRUNE)),run_time=.6)
        self.show(text('추가 A 또는 B → 거부 상태에 머무름',y=-4.95,size=21,color=PRUNE));self.to(98.7)

        self.section('04  무한한 목록을 유한한 식으로');self.cue(16)
        rows=self.show(VGroup(*[text('A'*k+'B',y=3.9-k*1.05,size=34,color=WEIGHT) for k in range(5)]),.6)
        self.cue(17);self.show(text('…  반복 횟수에 상한이 없음',y=-1.9,color=ACCENT))
        self.cue(18)
        regex=text('A*B',y=1.5,size=82,color=ACCENT)
        self.play(ReplacementTransform(rows,regex),run_time=1.2);self.stage.remove(rows);self.stage.add(regex)
        self.show(text('{ AⁿB | n = 0, 1, 2, … }',y=3.7,size=31,color=WEIGHT))
        self.cue(19);self.show(VGroup(text('*  =  0회 이상 반복',y=-.3,size=34,color=GOOD),text('n = 0일 때는 B',y=-2.8,color=MUTED)))
        self.cue(20);self.show(text('전체 문자열이 A*B에 속하는가?',y=-4.15,size=27,color=ACCENT));self.to(128.7)

        self.section('05  클레이니가 연결한 두 표현');self.cue(21)
        self.show(VGroup(text('Stephen C. Kleene',y=4.25,size=31,color=ACCENT),text('1951 보고서 → 1956 출판',y=3.45,size=23,color=MUTED)))
        self.cue(22);self.show(text('선택  |     연결  AB     반복  *',y=2.4,size=29,color=SPARSE))
        self.cue(23)
        self.show(VGroup(text('정규 표현식',-2,.9,24,WEIGHT),text('A*B',-2,-.1,48,ACCENT),text('유한 오토마타',2,.9,24,GOOD)))
        mini=automaton(0).scale(.45).move_to(p(2,-.45));self.show(mini)
        sample=self.show(text('B  →  양쪽 수용',y=-2,size=29,color=GOOD))
        for s,ok in [('AAB',True),('AAAAAB',True),('BA',False),('ABB',False)]:
            self.play(Transform(sample,text(s+('  →  양쪽 수용' if ok else '  →  양쪽 거부'),y=-2,size=29,color=GOOD if ok else PRUNE)),run_time=.65)
        self.cue(24);self.show(text('L(A*B) = L(대응 오토마타)',y=-3.3,size=30,color=ACCENT))
        self.cue(25);self.show(VGroup(text('모든 정규식 ↔ 대응하는 유한 오토마타',y=-4.2,size=25,color=GOOD),text('표현은 달라도 같은 문자열 집합',y=-4.95,size=23,color=MUTED)));self.to(161.7)

        self.section('06  유한한 상태로 무한한 경우를');self.cue(26)
        self.show(VGroup(RoundedRectangle(width=7.2,height=3.9,color=MUTED).move_to(p(0,2)),
            text('정규식 검색 · 줄 전체 판정',y=3.45,size=23,color=MUTED),text('^A*B$',y=2.6,size=38,color=ACCENT),
            text('B     AB     AAB',y=1.5,size=31,color=GOOD),text('BA     ABA     ABB',y=.5,size=29,color=PRUNE)))
        self.cue(27);self.show(text('신경 활동을 논리적 계산으로 표현',y=-1.25,size=27,color=WEIGHT))
        self.cue(28);self.show(text('패턴마다 저장 공간을 늘리는 대신',y=-2.3,size=26,color=MUTED))
        self.cue(29);self.show(text('현재 상태에 필요한 정보만 유지',y=-3.35,size=30,color=GOOD))
        self.cue(30)
        self.play(FadeOut(self.stage),run_time=.4);self.stage=VGroup()
        self.show(VGroup(network(3).scale(.7).move_to(p(0,3.6)),text('형식적 신경망',y=2.1,size=23,color=WEIGHT),
            automaton(0).scale(.7).move_to(p(0,.45)),text('유한 상태',y=-1.1,size=23,color=GOOD),
            text('A*B',y=-2.3,size=54,color=ACCENT),text('무한한 입력 집합\n유한한 상태 · 유한한 규칙',y=-4.25,size=31,color=ACCENT)))
        self.to(192)

