"""Build actual Thompson fragments bottom-up, then execute their transition data."""
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
from episodes.aic05_thompson_construction.nfa_model import MODEL
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def node(s,x,y,w=1.4,color=WEIGHT):
    return VGroup(RoundedRectangle(width=w,height=.72,corner_radius=.1,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,23,color,width=w-.12))
POS={0:(-1.8,2),1:(-.6,2),2:(-1.8,0),3:(-.6,0),4:(-2.9,1),5:(.5,1),6:(-3.8,1),7:(1.4,1),8:(2.3,1),9:(3.7,1),10:(3.7,-1),11:(2.3,-1),12:(2.3,-2.8),13:(3.7,-2.8)}

def graph(names=('root',),accept=False):
    fragments=[MODEL.fragments[name] for name in names]
    states=sorted(set().union(*(set(f['states']) for f in fragments)))
    edges=sorted(set().union(*(set(f['edges']) for f in fragments)))
    node_map={q:VGroup(Circle(.2,color=WEIGHT if q<8 else GOOD,fill_color=BG,fill_opacity=1).move_to(p(*POS[q])),text(str(q),*POS[q],size=14,width=.32)) for q in states}
    edge_map={}
    for i in edges:
        a,s,b=MODEL.edges[i];color=WEIGHT if s=='A' else SPARSE if s=='B' else MUTED
        if (a,b)==(5,4):
            points=[p(.5,1.28),p(.5,3),p(-2.9,3),p(-2.9,1.28)]
            path=VGroup(Line(points[0],points[1],color=color),Line(points[1],points[2],color=color),Arrow(points[2],points[3],buff=0,color=color))
            label=text('ε',-1.2,3.32,20,color,width=.5)
        elif (a,b)==(6,7):
            points=[p(-3.8,.72),p(-3.8,-1.2),p(1.4,-1.2),p(1.4,.72)]
            path=VGroup(Line(points[0],points[1],color=color),Line(points[1],points[2],color=color),Arrow(points[2],points[3],buff=0,color=color))
            label=text('ε · 0회',-1.1,-1.6,19,color,width=1.8)
        else:
            x1,y1=POS[a];x2,y2=POS[b]
            path=Arrow(p(x1,y1),p(x2,y2),buff=.24,color=color,stroke_width=2,max_tip_length_to_length_ratio=.18)
            lx,ly=(x1+x2)/2,(y1+y2)/2
            if abs(x2-x1)<.1:lx+=.35
            else:ly+=.32
            label=text(s or 'ε',lx,ly,20,color,width=.6)
        edge_map[i]=VGroup(path,label)
    group=VGroup(VGroup(*edge_map.values()),VGroup(*node_map.values()))
    if accept and MODEL.root['end'] in states:
        group.add(Circle(.14,color=GOOD).move_to(p(*POS[MODEL.root['end']])))
    if len(fragments)==1:
        x,y=POS[fragments[0]['start']]
        group.add(Arrow(p(x-.62,y),p(x-.26,y),buff=0,color=GOOD,stroke_width=2))
    group.state_map=node_map;group.edge_map=edge_map
    return group

def tree():
    specs=[('root','연결',0,3.15,ACCENT),('repeat','반복',-2.3,1.8,SPARSE),('suffix_ABB','연결',1.6,1.8,GOOD),('choice','선택',-2.3,.45,WEIGHT),('suffix_A','A',.6,.45,WEIGHT),('suffix_BB','연결',2.6,.45,GOOD),('choice_A','A',-3.1,-.9,WEIGHT),('choice_B','B',-1.5,-.9,SPARSE),('suffix_B1','B',1.8,-.9,SPARSE),('suffix_B2','B',3.4,-.9,SPARSE)]
    nodes={name:node(label,x,y,1.15,color) for name,label,x,y,color in specs}
    pairs=[('root','repeat'),('root','suffix_ABB'),('repeat','choice'),('choice','choice_A'),('choice','choice_B'),('suffix_ABB','suffix_A'),('suffix_ABB','suffix_BB'),('suffix_BB','suffix_B1'),('suffix_BB','suffix_B2')]
    g=VGroup(VGroup(*[Line(nodes[a].get_bottom(),nodes[b].get_top(),color=MUTED,stroke_width=1.5) for a,b in pairs]),VGroup(*nodes.values()))
    g.node_map=nodes
    return g

class ThompsonConstruction(Scene):
    DURATION=147
    def show(self,m,d=.35):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def cue(self,i):
        self.to(CUES[i]['start']);new=text(CUES[i]['caption'],y=-6.2,size=26)
        if len(self.caption):self.play(ReplacementTransform(self.caption,new),run_time=.2)
        else:self.add(new)
        self.caption=new
    def finish(self,i):self.to(CUES[i]['start']-.3)
    def section(self,title):
        if len(self.stage):self.play(FadeOut(self.stage),FadeOut(self.head),run_time=.3)
        self.stage=VGroup();self.head=text(title,y=5.05,size=28,color=ACCENT);self.add(self.head)
    def replace_graph(self,old,new,d=1):
        self.play(ReplacementTransform(old,new),run_time=d);self.stage.remove(old);self.stage.add(new);return new
    def mark_states(self,g,states,d=.3):
        self.play(*[mob[0].animate.set_fill(ACCENT if q in states else BG,opacity=.65 if q in states else 1) for q,mob in g.state_map.items()],run_time=d)
    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(text('AI 컴파일러  /  05',y=7.35,size=21,color=MUTED),text('수식은 어떻게\n실행 가능한 기계가 될까?',y=6.4,size=32),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text("Thompson's Construction · 구조를 따르는 변환",y=-7.45,size=18,color=MUTED))
        self.section('01  몇 개의 규칙으로 수많은 식을');self.cue(0)
        self.show(text('작은 변환 규칙 × 식의 구조',y=3.5,size=34,color=ACCENT))
        self.cue(1);self.show(VGroup(text('(A|B)*ABB',y=1.7,size=57,color=WEIGHT),text('{A,B}의 문자열 중 ABB로 끝나는 것',y=.3,size=27,color=GOOD)))
        self.cue(2);self.show(VGroup(node('문자 조각',-2.5,-2.1,2.2),node('부분 기계',0,-2.1,2.2,SPARSE),node('전체 기계',2.5,-2.1,2.2,GOOD),text('만들기 → 조합하기 → 다시 조합하기',y=-3.65,size=27,color=ACCENT)));self.finish(3)

        self.section('02  자식의 변환 결과가 부모의 입력');self.cue(3)
        self.show(text('(A|B)*ABB',y=4.25,size=35,color=ACCENT));ast=self.show(tree())
        self.show(text('문자 발생 위치마다 별도의 잎',y=-2.15,size=24,color=MUTED))
        self.cue(4)
        self.play(*[Indicate(ast.node_map[n],color=ACCENT) for n in ['choice_A','choice_B','suffix_A','suffix_B1','suffix_B2']],run_time=.6)
        for n in ['choice','repeat','suffix_BB','suffix_ABB','root']:self.play(Indicate(ast.node_map[n],color=ACCENT),run_time=.35)
        self.show(text('자식 먼저 → 부모 규칙으로 결합',y=-3.7,size=31,color=GOOD));self.finish(5)

        self.section('03  모든 조각에 입구와 출구를');self.cue(5)
        a=self.show(graph(('choice_A',)).scale(1.65).move_to(p(0,2.05)))
        self.show(text('A를 읽는 조각 · 상태 0 → 상태 1',y=3.8,size=25,color=WEIGHT))
        self.cue(6);b=self.show(graph(('choice_B',)).scale(1.65).move_to(p(0,-.25)))
        self.show(VGroup(text('입구',-2.2,-1.5,26,WEIGHT),text('출구',2.2,-1.5,26,GOOD),text('작은 조각도, 조립된 조각도 같은 인터페이스',y=-3,size=27,color=ACCENT),text('중간 조각의 출구 ≠ 전체 기계의 수용 상태',y=-4.35,size=22,color=MUTED)));self.finish(7)

        self.section('04  ε: 글자를 읽지 않는 연결');self.cue(7)
        dots=VGroup(*[Circle(.25,color=WEIGHT).move_to(p(x,1.5)) for x in [-3,-1,1,3]])
        self.show(VGroup(dots,Arrow(p(-2.7,1.5),p(-1.3,1.5),buff=0,color=WEIGHT),Arrow(p(-.7,1.5),p(.7,1.5),buff=0,color=MUTED),Arrow(p(1.3,1.5),p(2.7,1.5),buff=0,color=SPARSE),text('A',-2,2.1,30,WEIGHT),text('ε',0,2.1,30,ACCENT),text('B',2,2.1,30,SPARSE)))
        cursor=self.show(Dot(p(-1,1.5),color=ACCENT));self.play(cursor.animate.move_to(p(1,1.5)),run_time=.6)
        self.show(VGroup(text('입력 위치는 바뀌지 않음',y=-.2,size=31,color=ACCENT),text('입력은 A와 B뿐 · ε라는 문자는 필요 없음',y=-1.7,size=26,color=GOOD),text('표현력을 늘리지 않고 조립을 돕는 연결 장치',y=-3.4,size=24,color=MUTED)));self.finish(8)

        self.section('05  완성된 부분 기계도 하나의 조각');self.cue(8)
        label=self.show(text('선택 노드: A | B',y=4.15,size=34,color=WEIGHT))
        g=self.show(graph(('choice',)).scale(1.15).move_to(p(0,1.35)))
        choice_hint=self.show(text('A와 B의 자식 조각을 ε로 조립',y=-1.1,size=27,color=WEIGHT))
        self.cue(9)
        self.play(FadeOut(choice_hint),run_time=.2);self.stage.remove(choice_hint)
        new=graph(('repeat',)).scale(.92).move_to(p(0,.65));g=self.replace_graph(g,new,1.15)
        self.play(Transform(label,text('부모 반복 노드: (A|B)*',y=4.15,size=34,color=SPARSE)),run_time=.35)
        self.cue(10);self.show(text('선택 기계 전체가 반복의 한 조각으로',y=-2.95,size=26,color=SPARSE))
        self.cue(11);self.show(text('같은 입구·출구 연결 규칙을 재사용',y=-4,size=28,color=ACCENT))
        self.cue(12);self.play(Circumscribe(g,color=ACCENT),run_time=.8)
        self.cue(13);self.show(text('자식 변환 → 결과를 조각 삼아 부모 변환',y=-4.95,size=25,color=GOOD));self.finish(14)

        self.section('06  마지막 연결로 식 전체를 완성');self.cue(14)
        self.show(text('(A|B)*  +  A  +  B  +  B',y=4.2,size=34,color=ACCENT))
        g=graph().scale(.88).move_to(p(0,.7))
        joins=[i for i,(a,s,b) in enumerate(MODEL.edges) if (a,b) in [(7,8),(9,10),(11,12)]]
        for i in joins:g.edge_map[i].set_opacity(0)
        self.show(g,.25)
        for i in joins:self.play(g.edge_map[i].animate.set_opacity(1),run_time=.4)
        self.cue(15)
        final=g.state_map[MODEL.root['end']]
        self.show(Circle(.14*.88,color=GOOD).move_to(final.get_center()))
        self.show(text('식 전체의 출구를 최종 수용 상태로',y=-3.55,size=26,color=GOOD))
        self.show(text('14개 상태 · 문자 전이 5개 · ε-전이 11개',y=-4.5,size=23,color=MUTED))
        self.cue(16);self.show(text("Thompson's Construction",y=-5.1,size=24,color=ACCENT),.2);self.finish(17)

        self.section('07  조립한 전이 자료로 입력 판정');self.cue(17)
        self.show(text('ε-NFA 자료 → 시뮬레이터',y=4.2,size=30,color=ACCENT))
        g=self.show(graph(accept=True).scale(.82).move_to(p(0,.7)))
        self.show(text('노란 채움: 도달 가능한 상태',y=-2.7,size=20,color=MUTED))
        status=self.show(text('시작 상태에서 실행',y=-4.6,size=26,color=MUTED))
        self.cue(18)
        word=self.show(text('A A B B',y=-3.55,size=34,color=WEIGHT))
        steps=MODEL.trace('AABB');self.mark_states(g,steps[0]['closed'],.4)
        for step in steps[1:]:
            self.mark_states(g,step['moved'],.3);self.mark_states(g,step['closed'],.35)
        self.play(Transform(status,text('ε-closure → 문자 이동 → ε-closure',y=-4.6,size=25,color=ACCENT)),run_time=.25)
        self.cue(19);self.play(Transform(status,text('입력 종료 · 수용 상태 13 포함 → 수용',y=-4.6,size=25,color=GOOD)),run_time=.35)
        self.cue(20)
        self.play(Transform(word,text('A B B A',y=-3.55,size=34,color=PRUNE)),run_time=.25)
        for step in MODEL.trace('ABBA')[1:]:self.mark_states(g,step['closed'],.3)
        self.play(Transform(status,text('ABBA : 수용 상태 13 미포함 → 거부',y=-4.6,size=26,color=PRUNE)),run_time=.3);self.finish(21)

        self.section('08  AI 컴파일러의 구조적 변환');self.cue(21)
        self.show(text('Y = ReLU(XW + b)',y=4.15,size=39,color=ACCENT))
        self.cue(22)
        self.show(VGroup(text('계산 IR',-2,3,27,WEIGHT),node('MatMul',-2,1.9,2.3,WEIGHT),node('Add',-2,.45,2.3,SPARSE),node('ReLU',-2,-1,2.3,GOOD),Arrow(p(-2,1.45),p(-2,.9),buff=0,color=MUTED),Arrow(p(-2,0),p(-2,-.55),buff=0,color=MUTED),Arrow(p(-.6,.45),p(.6,.45),buff=0,color=ACCENT),text('하위 IR / 호출 구조',2,3,25,GOOD,width=3.6),RoundedRectangle(width=3.2,height=3.8,color=GOOD).move_to(p(2,.45)),text('타깃 연산\n메모리 연산\n커널 호출',2,.45,25,GOOD,width=2.9)))
        self.cue(23);self.show(VGroup(text('dtype · layout · 효과 · 하드웨어 조건',y=-2.6,size=25,color=MUTED),text('구체적인 변환 규칙은 다름',y=-3.65,size=27,color=PRUNE)))
        self.cue(24);self.show(VGroup(text('작은 부분을 변환하고 결과를 조합',y=-4.6,size=27,color=ACCENT),text('AI lowering이 항상 단순 트리 순서인 것은 아님',y=-5.25,size=19,color=MUTED)));self.finish(25)

        self.section('09  작은 규칙의 반복이 전체를 바꾼다');self.cue(25)
        self.show(VGroup(text('작은 부분을 변환',y=3.1,size=36,color=WEIGHT),text('↓',y=1.85,size=45,color=MUTED),text('결과를 다시 하나의 조각으로',y=.55,size=34,color=SPARSE),text('↓',y=-.75,size=45,color=MUTED),text('부모 규칙으로 결합하고 반복',y=-2.05,size=34,color=GOOD),text('구조를 따라 변환 규칙을 재사용',y=-4.1,size=31,color=ACCENT)));self.to(147)
