"""Compositional regular languages and structured numerical computation."""
import sys,json
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def node(s,x,y,w=1.6,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=.8,corner_radius=.13,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,24,color,width=w-.15))
def edge(a,b,color=MUTED):return Arrow(a,b,buff=.08,color=color,stroke_width=2.5,max_tip_length_to_length_ratio=.15)
def regex_tree():
    nodes=VGroup(node('연결',0,3.25,2,ACCENT),node('반복 *',-1.9,1.85,2,SPARSE),node('선택 |',-1.9,.3,2,WEIGHT),node('A',-2.8,-1.3,1,WEIGHT),node('B',-1,-1.3,1,WEIGHT),node('ABB',1.9,1.85,2,GOOD))
    links=VGroup(*[Line(nodes[a].get_bottom(),nodes[b].get_top(),color=MUTED,stroke_width=2) for a,b in [(0,1),(0,5),(1,2),(2,3),(2,4)]])
    return VGroup(links,nodes)

class ComposableRegex(Scene):
    DURATION=172
    def show(self,m,d=.35):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def cue(self,i):
        self.to(CUES[i]['start']);new=text(CUES[i]['caption'],y=-6.2,size=26)
        if len(self.caption):self.play(ReplacementTransform(self.caption,new),run_time=.2)
        else:self.add(new)
        self.caption=new
    def finish(self,next_cue):self.to(CUES[next_cue]['start']-.3)
    def section(self,title):
        if len(self.stage):self.play(FadeOut(self.stage),FadeOut(self.head),run_time=.3)
        self.stage=VGroup();self.head=text(title,y=5.05,size=28,color=ACCENT);self.add(self.head)
    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(text('AI 컴파일러  /  03',y=7.35,size=21,color=MUTED),text('무한히 많은 문자열을\n하나의 식으로?',y=6.4,size=33),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('선택 · 연결 · 반복 → 조합 가능한 표현',y=-7.45,size=18,color=MUTED))
        self.section('01  끝없는 나열, 유한한 규칙');self.cue(0)
        listing=VGroup(*[text('A'*i+'B',-2,3.5-i*1.1,33,WEIGHT,width=3.3) for i in range(5)])
        self.show(listing);self.cue(1);self.show(text('…',-2,-2.2,40,WEIGHT))
        regex=self.show(text('A*B',2,1.3,65,ACCENT,width=3.4));self.show(text('한 식 · 무한한 문자열 집합',y=-3.4,size=25,color=GOOD))
        self.cue(2);self.play(Circumscribe(regex,color=ACCENT),run_time=.6)
        self.cue(3);self.show(VGroup(text('A',-1.5,-4.5,34,WEIGHT),text('*',0,-4.5,40,SPARSE),text('B',1.5,-4.5,34,GOOD)));self.finish(4)

        self.section('02  선택: 가능성을 합친다');self.cue(4)
        self.show(text('A | B',y=4,size=52,color=ACCENT))
        a=self.show(node('A',0,2.15,color=WEIGHT));b=self.show(node('B',0,-.15,color=SPARSE))
        self.show(VGroup(Dot(p(-3,1),color=MUTED),Dot(p(3,1),color=MUTED),edge(p(-3,1),p(-.9,2.15),WEIGHT),edge(p(.9,2.15),p(3,1),WEIGHT),edge(p(-3,1),p(-.9,-.15),SPARSE),edge(p(.9,-.15),p(3,1),SPARSE)))
        self.cue(5);token=self.show(Dot(p(-3,1),color=ACCENT))
        for route in [[p(0,2.15),p(3,1)],[p(0,-.15),p(3,1)]]:
            token.move_to(p(-3,1))
            for point in route:self.play(token.animate.move_to(point),run_time=.4)
        self.cue(6);self.show(text('L(A|B) = {A} ∪ {B}',y=-2.25,size=32,color=GOOD))
        self.cue(7);self.show(VGroup(text('A 또는 B · AB가 아님',y=-3.5,size=27,color=WEIGHT),text('경로 개념도 · 정식 오토마타는 아님',y=-4.7,size=21,color=MUTED)));self.finish(8)

        self.section('03  연결: 순서를 만든다');self.cue(8)
        self.show(text('AB',y=4,size=58,color=ACCENT))
        a=self.show(node('A',-1.65,1.8,color=WEIGHT));b=self.show(node('B',1.65,1.8,color=GOOD))
        self.show(edge(p(-.8,1.8),p(.8,1.8),GOOD));self.cue(9)
        token=self.show(Dot(p(-3.3,.7),color=ACCENT))
        for point in [p(-1.65,.7),p(1.65,.7),p(3.3,.7)]:self.play(token.animate.move_to(point),run_time=.55)
        self.cue(10);self.show(text('L(RS) = { uv | u ∈ L(R), v ∈ L(S) }',y=-1.1,size=27,color=GOOD))
        self.show(text('R을 먼저, 그다음 S',y=-2.2,size=29,color=WEIGHT))
        self.cue(11);self.show(VGroup(text('A|B : A 또는 B',y=-3.55,size=27,color=SPARSE),text('AB : A 다음에 B',y=-4.6,size=27,color=GOOD)));self.finish(12)

        self.section('04  반복: 식은 그대로, 경우는 끝없이');self.cue(12)
        self.show(text('A*',y=4.1,size=65,color=ACCENT),.2);self.show(node('A',0,1.6,color=WEIGHT),.2)
        self.show(VGroup(Dot(p(-3,1.6),color=MUTED),Dot(p(3,1.6),color=MUTED),edge(p(-3,1.6),p(-.9,1.6),WEIGHT),edge(p(.9,1.6),p(3,1.6),WEIGHT),CurvedArrow(p(.65,2.1),p(-.65,2.1),angle=PI,color=SPARSE)),.2)
        self.cue(13);self.show(VGroup(CurvedArrow(p(-3,1.4),p(3,1.4),angle=PI/2,color=GOOD),text('0회 → ε (빈 문자열)',y=-.45,size=27,color=GOOD)))
        result=self.show(text('ε',y=-1.8,size=42,color=WEIGHT));self.cue(14)
        for n in range(1,4):self.play(Transform(result,text('A'*n,y=-1.8,size=42,color=WEIGHT)),run_time=.5)
        self.show(text('A¹⁰⁰ · A¹⁰⁰⁰ · …',y=-2.9,size=31,color=SPARSE))
        self.cue(15);self.show(text('반복 횟수가 늘어도 식 A*는 그대로',y=-4,size=28,color=ACCENT))
        self.cue(16);self.show(text('각 문자열은 유한 길이 · 집합은 무한',y=-4.95,size=23,color=MUTED));self.finish(17)

        self.section('05  작은 규칙을 조합하면');self.cue(17)
        formula=self.show(text('(A|B)*ABB',y=4,size=49,color=ACCENT))
        pieces=self.show(VGroup(node('A|B',-2.4,2.45,2,WEIGHT),node('*',0,2.45,1.2,SPARSE),node('ABB',2.4,2.45,2,GOOD)))
        self.cue(18);self.show(text('{A,B}의 문자열 중 ABB로 끝나는 것',y=1.25,size=28,color=GOOD))
        self.cue(19)
        for n in pieces:self.play(Indicate(n),run_time=.45)
        verdict=self.show(text('ABB → 수용',y=-.2,size=34,color=GOOD))
        self.cue(20)
        for s,ok in [('AABB',True),('BABABB',True),('ABA',False),('ABBA',False),('BAA',False)]:
            self.play(Transform(verdict,text(s+(' → 수용' if ok else ' → 거부'),y=-.2,size=34,color=GOOD if ok else PRUNE)),run_time=.55)
        self.show(VGroup(text('ABBA의 마지막 3글자는 BBA → 거부',y=-1.5,size=25,color=PRUNE),text('ABB : 반복 부분이 0회여도 수용',y=-2.65,size=25,color=GOOD)))
        self.cue(21);self.show(VGroup(text('L((A|B)*ABB) = { wABB | w ∈ {A,B}* }',y=-3.85,size=26,color=ACCENT),text('문자열 전체를 판정 · 부분 검색 아님',y=-4.85,size=22,color=MUTED)));self.finish(22)

        self.section('06  텍스트에서 분석 가능한 구조로');self.cue(22)
        formula=self.show(text('(A|B)*ABB',y=4.25,size=39,color=ACCENT))
        self.cue(23);tree=regex_tree();self.show(tree)
        self.show(text('ABB는 연결된 리터럴 3개를 묶어 표시',y=-2.35,size=21,color=MUTED))
        self.cue(24)
        self.play(Indicate(tree[1][2],color=WEIGHT),Indicate(tree[1][1],color=SPARSE),run_time=1)
        self.show(text('선택 → 반복 → 뒤에 ABB 연결',y=-3.3,size=27,color=GOOD))
        self.cue(25);self.show(text('구조를 분석 → 대응하는 인식기로 변환 가능',y=-4.55,size=25,color=ACCENT));self.finish(26)

        self.section('07  수치 계산도 구조로 표현한다');self.cue(26)
        self.show(text('Y = ReLU(XW + b)',y=4.15,size=40,color=ACCENT))
        ops=VGroup(node('MatMul',0,2.25,2.8,WEIGHT),node('Add',0,.5,2.8,SPARSE),node('ReLU',0,-1.25,2.8,GOOD))
        self.cue(27);self.show(ops)
        self.show(VGroup(text('X, W',-2.9,2.25,25,WEIGHT),edge(p(-2.1,2.25),p(-1.5,2.25),WEIGHT),text('b',-2.9,.5,29,SPARSE),edge(p(-2.1,.5),p(-1.5,.5),SPARSE),edge(p(0,1.8),p(0,.95)),edge(p(0,.05),p(0,-.8))))
        self.cue(28);self.show(text('노드: 연산 · 화살표: 데이터 의존성',y=-2.55,size=26,color=MUTED))
        self.cue(29)
        fused=self.show(RoundedRectangle(width=3.35,height=4.7,color=ACCENT,stroke_width=3).move_to(p(0,.5)))
        self.show(VGroup(text('하나의 커널로 실행하는 후보',y=-3.55,size=27,color=ACCENT),text('지원되는 shape·dtype·타깃과 수치 조건에서',y=-4.45,size=22,color=MUTED)))
        self.cue(30);self.play(FadeOut(self.stage),run_time=.35);self.stage=VGroup()
        self.show(VGroup(node('정규 표현식',-2,3.2,3.5,WEIGHT),node('AI 계산 그래프',2,3.2,3.5,GOOD),text('(A|B)*ABB',-2,1.9,30,WEIGHT,width=3.8),text('ReLU(XW+b)',2,1.9,29,GOOD,width=3.8),text('문자열 집합',-2,.65,27,WEIGHT,width=3.8),text('수치 연산·의존성',2,.65,25,GOOD,width=3.8),text('각 표현의 의미와 변환 조건은 다름',y=-1.05,size=29,color=PRUNE)))
        self.cue(31);self.show(text('공통 원리: 작은 구성 요소 → 구조 → 분석',y=-3,size=29,color=ACCENT));self.finish(32)

        self.section('08  표현은 계산을 다루는 출발점');self.cue(32)
        self.show(VGroup(text('(A|B)*ABB',y=3.6,size=46,color=WEIGHT),text('표현 → 구조 → 분석 → 변환',y=1.9,size=34,color=ACCENT)))
        self.cue(33);self.show(text('표현이 바뀌면, 무엇을 보존해야 할까?',y=.05,size=29,color=SPARSE))
        self.cue(34);self.show(VGroup(text('정규식: 인식하는 문자열 집합',y=-1.3,size=27,color=WEIGHT),text('AI 계산: 요구되는 수치 의미·의존성',y=-2.35,size=26,color=GOOD)))
        self.cue(35);self.show(text('복잡한 대상을 다루는 출발점은\n작은 규칙들의 조합으로 표현하는 것입니다.',y=-4.25,size=30,color=ACCENT));self.to(172)
