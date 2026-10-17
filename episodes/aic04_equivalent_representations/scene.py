"""Language equality across regular expressions and finite automata."""
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
class EquivalentRepresentations(Scene):
    DURATION=164
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
        from episodes.aic01_neurons_regex.scene import automaton
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(text('AI 컴파일러  /  04',y=7.35,size=21,color=MUTED),text('수식과 기계, 어느 쪽이\n더 강력할까?',y=6.4,size=32),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('정규 표현식과 유한 오토마타 · 표현력의 동등성',y=-7.45,size=18,color=MUTED))
        self.section('01  어느 쪽이 더 많은 규칙을 표현할까?');self.cue(0);
        self.show(VGroup(text('수식 R',-2,3.8,28,WEIGHT),text('기계 M',2,3.8,28,SPARSE),text('A*B',-2,1.75,59,WEIGHT,width=3.6),automaton(0).scale(.43).move_to(p(2,1.75))))
        self.cue(1);self.show(VGroup(text('기호의 조합',-2,-.5,26,WEIGHT,width=3.7),text('상태와 전이',2,-.5,26,SPARSE,width=3.7)))
        self.cue(2);self.show(text('어느 쪽이 더 많은 언어를 표현할까?',y=-2,size=31,color=ACCENT))
        self.cue(3);self.show(text('선택과 반복 · 유한한 기호',y=-3.1,size=27,color=WEIGHT))
        self.cue(4);self.show(text('유한한 상태 · 반복 가능한 경로',y=-4.1,size=27,color=SPARSE))
        self.show(text('겉모습만으로 표현력을 비교할 수는 없다',y=-5,size=23,color=MUTED));self.finish(5)

        self.section('02  한 쌍의 예시는 같아 보인다');self.cue(5);
        machine=self.show(automaton(2),.15);self.show(text('R = A*B',y=4.3,size=37,color=WEIGHT),.15)
        token=self.show(Dot(p(-2.5,2),radius=.12,color=ACCENT),.15);sample=self.show(text('B, AB, AAB, …',y=-.6,size=32),.15);result=self.show(text('입력 종료에서 판정',y=-2,size=25,color=MUTED),.15)
        self.cue(6);self.show(text('L(R) = { AⁿB | n ≥ 0 }',y=-3.15,size=28,color=GOOD))
        self.play(Circumscribe(machine,color=ACCENT),run_time=.7)
        self.cue(7);
        self.play(Indicate(machine[1][0]),token.animate.move_to(p(0,2)),run_time=.8)
        self.play(Transform(result,text('B 다음에 입력이 끝나야 수용',y=-2,size=27,color=GOOD)),run_time=.3)
        def run(s):
            token.move_to(p(-2.5,2));q=0
            self.play(Transform(sample,text('입력: '+s,y=-.6,size=34)),run_time=.2)
            for ch in s:
                q=0 if q==0 and ch=='A' else 1 if q==0 else 2
                self.play(token.animate.move_to(p([-2.5,0,2.5][q],2)),run_time=.25)
            self.play(Transform(result,text('R과 M 모두 '+('수용' if q==1 else '거부'),y=-2,size=29,color=GOOD if q==1 else PRUNE)),run_time=.2)
        self.cue(8);
        for s in ['B','AB','AAB']:run(s)
        
        for s in ['BA']:run(s)
        self.cue(9);self.show(text('이 예시의 R과 M: 같은 언어',y=-4.1,size=27,color=GOOD))
        self.cue(10);self.show(text('한 쌍의 일치 ≠ 두 표현 체계의 표현력 비교',y=-5,size=23,color=ACCENT));self.finish(11)

        self.section('03  문자열 집합들의 부류를 비교한다');self.cue(11);
        self.show(text('개별 표현: L(R)와 L(M)',y=4.05,size=30,color=MUTED))
        
        self.show(VGroup(node('ℒ_RE',-2,2.65,3.4,WEIGHT),node('ℒ_FA',2,2.65,3.4,SPARSE),text('정규식으로 표현하는\n모든 언어',-2,1.2,25,WEIGHT,width=3.6),text('유한 오토마타로 인식하는\n모든 언어',2,1.2,24,SPARSE,width=3.6),text('원소는 문자열이 아니라 언어 L₁, L₂, …',y=-.6,size=26,color=ACCENT)))
        self.show(VGroup(text('어느 한쪽에만 언어가 있다면, 능력은 다르다',y=-2.4,size=26,color=PRUNE),text('전체 언어 부류의 양방향 포함을 확인해야 한다',y=-4.1,size=25,color=GOOD)));self.finish(12)

        self.section('04  정방향: 모든 정규식을 기계로');self.cue(12);
        self.show(text('모든 R에 대해, L(R)=L(M)인 M이 있을까?',y=3.7,size=28,color=ACCENT))
        self.cue(13);self.show(VGroup(text('기초: 문자 · ε · ∅',y=2.1,size=30,color=WEIGHT),text('조합: 선택 · 연결 · 반복',y=.6,size=30,color=SPARSE)))
        self.show(text('작은 언어를 보존하는 작은 기계부터',y=-1.8,size=28,color=GOOD))
        self.cue(14);self.play(FadeOut(self.stage),run_time=.3);self.stage=VGroup()
        self.show(text('A | B',y=4.1,size=50,color=ACCENT))
        coords=[(-3,1.25),(-1.2,2.35),(1.2,2.35),(-1.2,.15),(1.2,.15),(3,1.25)]
        states=VGroup(*[Circle(.23,color=SPARSE if i==5 else WEIGHT).move_to(p(x,y)) for i,(x,y) in enumerate(coords)])
        states[5].add(Circle(.16,color=SPARSE).move_to(p(3,1.25)));self.show(states)
        
        self.show(VGroup(edge(p(-.9,2.35),p(.9,2.35),WEIGHT),text('A',0,2.8,28,WEIGHT),edge(p(-.9,.15),p(.9,.15),GOOD),text('B',0,.65,28,GOOD)))
        self.play(Indicate(states),run_time=.65)
        self.cue(15);
        self.show(VGroup(*[edge(p(*coords[a]),p(*coords[b]),MUTED) for a,b in [(0,1),(0,3),(2,5),(4,5)]],text('ε',-2.25,2.3,25,MUTED),text('ε',-2.25,.25,25,MUTED),text('ε',2.25,2.3,25,MUTED),text('ε',2.25,.25,25,MUTED),edge(p(-3.85,1.25),p(-3.3,1.25))))
        self.show(VGroup(text('ε : 입력 문자를 읽지 않고 이동',y=-1.45,size=27,color=MUTED),text('입력 전체를 읽고 수용 상태에 닿는 경로가 있으면 수용',y=-2.8,size=24,color=GOOD),text('A와 B 중 하나의 경로 · AB를 읽는 기계가 아님',y=-4.25,size=24,color=ACCENT)));self.finish(16)

        self.section('05  연산을 조합하면 정방향이 완성된다');self.cue(16);
        self.show(text('AB · 순서대로 연결',y=4.05,size=32,color=ACCENT))
        top=VGroup(*[Circle(.22,color=WEIGHT).move_to(p(x,2.6)) for x in [-3,-1,1,3]])
        top[3].add(Circle(.15,color=GOOD).move_to(p(3,2.6)));self.show(top)
        self.show(VGroup(edge(p(-2.7,2.6),p(-1.3,2.6),WEIGHT),edge(p(-.7,2.6),p(.7,2.6)),edge(p(1.3,2.6),p(2.7,2.6),GOOD),text('A',-2,3.1,26,WEIGHT),text('ε',0,3.1,26,MUTED),text('B',2,3.1,26,GOOD)))
        self.cue(17);self.show(text('A* · 돌아오는 경로와 나가는 경로',y=1.4,size=30,color=SPARSE))
        bottom=VGroup(*[Circle(.22,color=SPARSE).move_to(p(x,-.7)) for x in [-3,-1,1,3]])
        bottom[3].add(Circle(.15,color=GOOD).move_to(p(3,-.7)));self.show(bottom)
        self.show(VGroup(edge(p(-2.7,-.7),p(-1.3,-.7)),edge(p(-.7,-.7),p(.7,-.7),WEIGHT),edge(p(1.3,-.7),p(2.7,-.7)),text('ε',-2,-.2,24,MUTED),text('A',0,-.2,26,WEIGHT),text('ε',2,-.2,24,MUTED)))
        self.show(VGroup(CurvedArrow(p(1,-.4),p(-1,-.4),angle=PI,color=SPARSE),text('ε · 다시 반복',y=.95,size=23,color=SPARSE)))
        self.show(VGroup(CurvedArrow(p(-3,-1),p(3,-1),angle=PI/2,color=GOOD),text('ε · 0회 반복도 수용',y=-2.6,size=24,color=GOOD)))
        self.show(VGroup(text('선택 → 분기   연결 → 순서   반복 → 순환',y=-3.75,size=26,color=ACCENT),text('경로 구성 원리 · 입력 전체 판정',y=-4.55,size=21,color=MUTED)));self.play(Circumscribe(top),Circumscribe(bottom),run_time=.8)
        self.cue(18);self.show(text('모든 정규식 → 같은 언어의 유한 오토마타',y=-5.1,size=22,color=GOOD));self.finish(19)


        self.section('06  한 방향만으로는 부족하다');self.cue(19);
        self.show(text('지금 확인한 것',y=4.1,size=29,color=ACCENT))
        self.show(text('ℒ_RE ⊆ ℒ_FA',y=2.9,size=45,color=GOOD))
        outer=self.show(Ellipse(width=7,height=3.5,color=SPARSE).move_to(p(0,.4)))
        inner=self.show(Ellipse(width=3.3,height=2.2,color=WEIGHT).move_to(p(-1.55,.4)))
        self.show(VGroup(text('ℒ_RE',-1.55,.9,31,WEIGHT),text('L₁, L₂, …',-1.55,-.1,24,WEIGHT),text('ℒ_FA',1.85,1.45,27,SPARSE)))
        self.show(text('다른 언어가\n더 있을 수도?',1.85,.1,25,ACCENT,width=2.6))
        self.cue(20);self.show(text('엄밀 포함을 뜻하는 그림은 아님\n아직 배제하지 못한 가능성',y=-2.5,size=23,color=MUTED))
        self.cue(21);self.show(text('반대 방향 ℒ_FA ⊆ ℒ_RE도 필요',y=-4.05,size=30,color=ACCENT));self.finish(22)

        self.section('07  역방향: 기계의 경로를 식으로');self.cue(22);
        self.show(text('경로의 언어를 유지하며 상태를 줄인다',y=4.05,size=29,color=ACCENT));
        gnfa=self.show(VGroup(node('i',-2.7,1.85,1,WEIGHT),node('k',0,1.85,1,SPARSE),node('j',2.7,1.85,1,GOOD),edge(p(-2.1,1.85),p(-.6,1.85)),edge(p(.6,1.85),p(2.1,1.85)),text('P',-1.35,2.35,26),text('Q',1.35,2.35,26),CurvedArrow(p(.4,2.3),p(-.4,2.3),angle=PI,color=SPARSE),text('R',0,3.15,26,SPARSE),CurvedArrow(p(-2.7,1.3),p(2.7,1.3),angle=PI/2,color=MUTED),text('T',0,-.35,26,MUTED)))
        self.cue(23);self.show(VGroup(text('직접 가거나, k를 거쳐 갈 수 있음',y=-1.55,size=25,color=MUTED),text('T | P R* Q',y=-2.7,size=39,color=ACCENT),text('k를 없애도 같은 경로의 문자열을 표현',y=-4.05,size=25,color=GOOD)))
        self.cue(24);
        reduced=VGroup(node('i',-2.7,1.85,1,WEIGHT),node('j',2.7,1.85,1,GOOD),edge(p(-2.1,1.85),p(2.1,1.85)),text('T | P R* Q',0,2.65,31,ACCENT))
        self.play(ReplacementTransform(gnfa,reduced),run_time=1);self.stage.remove(gnfa);self.stage.add(reduced)
        self.cue(25);self.show(text('시작에서 수용까지의 언어 → 하나의 정규식',y=-5.05,size=22,color=GOOD));self.finish(26)

        self.section('08  양방향 포함이 정확한 일치를 만든다');self.cue(26);
        self.show(text('ℒ_RE ⊆ ℒ_FA',y=4,size=38,color=WEIGHT))
        self.cue(27);self.show(text('ℒ_FA ⊆ ℒ_RE',y=2.8,size=38,color=SPARSE))
        
        a=self.show(Ellipse(width=5.5,height=2.8,color=WEIGHT,stroke_width=3).move_to(p(-.4,.6)))
        b=self.show(Ellipse(width=5.5,height=2.8,color=SPARSE,stroke_width=3).move_to(p(.4,.6)))
        self.play(a.animate.move_to(p(0,.6)),b.animate.move_to(p(0,.6)),run_time=.8)
        self.cue(28);self.show(text('ℒ_RE = ℒ_FA',y=.6,size=40,color=GOOD))
        self.cue(29);self.show(VGroup(text('클레이니 정리 · 같은 정규 언어의 부류',y=-2.25,size=29,color=ACCENT),text('표현력의 동등성 ≠ 식 크기·상태 수·실행 비용의 동일성',y=-4.1,size=22,color=MUTED)));self.finish(30)

        self.section('09  표현 가능한 범위와 보존할 의미');self.cue(30);
        self.show(text('Y = ReLU(XW + b)',y=4.05,size=40,color=ACCENT))
        graph=self.show(VGroup(node('MatMul',0,2.45,2.7,WEIGHT),node('Add',0,.85,2.7,SPARSE),node('ReLU',0,-.75,2.7,GOOD),edge(p(0,2),p(0,1.3)),edge(p(0,.4),p(0,-.3)),text('X,W',-2.8,2.45,25,WEIGHT),edge(p(-2.1,2.45),p(-1.45,2.45)),text('b',-2.8,.85,27,SPARSE),edge(p(-2.1,.85),p(-1.45,.85))))
        self.cue(31);self.show(text('수식 · 연산 그래프 · 실행 코드',y=-2.25,size=29,color=WEIGHT))
        self.show(text('다른 형태 ≠ 반드시 다른 계산 능력',y=-3.15,size=27,color=GOOD))
        self.cue(32);self.show(text('먼저 정해야 하는 것: 보존할 의미와 조건',y=-4.35,size=26,color=ACCENT))
        self.cue(33);self.play(FadeOut(self.stage),run_time=.35);self.stage=VGroup()
        self.show(VGroup(node('정규식 ↔ 오토마타',0,3.5,6.7,WEIGHT),text('보존 대상: 수용하는 문자열 집합',y=2.3,size=29,color=WEIGHT),node('AI 수식 ↔ 그래프 / 코드',0,.55,6.7,GOOD),text('보존 대상: 정해진 수치 결과와 동작',y=-.65,size=28,color=GOOD)))
        self.show(VGroup(text('부동소수점 반올림·연산 순서·효과도 조건에 포함',y=-2.55,size=24,color=PRUNE),text('수용 언어의 동등성과 수치 계산의 계약은 다름',y=-4.1,size=24,color=MUTED)));self.finish(34)


        self.section('10  수식과 기계, 어느 쪽이 더 강력할까?');self.cue(34);
        self.show(VGroup(text('고전적 정규 표현식',-2,3.65,26,WEIGHT,width=3.7),text('유한 오토마타',2,3.65,26,SPARSE,width=3.7),text('?',y=2.15,size=59,color=ACCENT)))
        self.cue(35);self.show(text('어느 쪽에만 표현할 수 있는 언어가 있을까?',y=.65,size=27,color=MUTED))
        self.cue(36);self.play(FadeOut(self.stage[0][2]),run_time=.2);self.show(text('같은 표현력',y=2.15,size=34,color=GOOD));self.show(text('ℒ_RE = ℒ_FA',y=-.65,size=43,color=GOOD))
        self.show(text('서로 다른 방식 · 정확히 같은 언어의 범위',y=-2.45,size=28,color=SPARSE))
        self.cue(37);self.show(text('표현이 다르다는 것은,\n표현할 수 있는 것까지 다르다는 뜻은 아닙니다.',y=-4.3,size=30,color=ACCENT));self.to(164)
