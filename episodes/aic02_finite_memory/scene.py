"""Finite states cannot distinguish every positive A-prefix length."""
import sys,json
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import configure_vertical,txt,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD
configure_vertical();config.disable_caching=True
CUES=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
def p(x,y):return np.array([x,y,0.])
def text(s,x=0,y=0,size=28,color=INK,width=7.7):return txt(str(s),size,color,width).move_to(p(x,y))
def state(s,x,y,color=WEIGHT):return VGroup(Circle(.55,color=color,fill_color=BG,fill_opacity=1).move_to(p(x,y)),text(s,x,y,25,color))
def box(title,body,y,color):
    return VGroup(RoundedRectangle(width=7.2,height=2.3,color=color,stroke_width=2).move_to(p(0,y)),text(title,y=y+.65,size=35,color=color),text(body,y=y-.45,size=25))

class FiniteMemory(Scene):
    DURATION=140
    def show(self,m,d=.35):self.play(FadeIn(m),run_time=d);self.stage.add(m);return m
    def to(self,t):
        if self.time>t+1/30:raise RuntimeError(f'Timeline overflow {self.time} > {t}')
        if t-self.time>.001:self.wait(t-self.time)
    def cue(self,i):
        self.to(CUES[i]['start']);new=text(CUES[i]['caption'],y=-6.2,size=26)
        if len(self.caption):self.play(ReplacementTransform(self.caption,new),run_time=.2)
        else:self.add(new)
        self.caption=new
    def section(self,title):
        if len(self.stage):self.play(FadeOut(self.stage),FadeOut(self.head),run_time=.3)
        self.stage=VGroup();self.head=text(title,y=5.05,size=28,color=ACCENT);self.add(self.head)
    def construct(self):
        self.stage=VGroup();self.head=VGroup();self.caption=VGroup()
        self.add(text('AI 컴파일러  /  02',y=7.35,size=21,color=MUTED),text('유한한 기억으로\n모든 규칙을 인식할까?',y=6.4,size=32),Line(p(-3.9,5.65),p(3.9,5.65),color=MUTED,stroke_opacity=.35),text('Finite Automaton · Stack · Recurrent State',y=-7.45,size=18,color=MUTED))
        self.section('01  입력 전체 대신 현재 상태');self.cue(0)
        from episodes.aic01_neurons_regex.scene import automaton
        machine=self.show(automaton(1.6));self.show(text('A*B · 전체 문자열 판정',y=4.25,size=30,color=ACCENT))
        token=self.show(Dot(p(-2.5,1.6),radius=.12,color=ACCENT))
        self.cue(1);self.show(text('A   A   A   A   B',y=-.8,size=36,color=WEIGHT))
        self.cue(2)
        for _ in range(4):self.play(Indicate(machine[1][0],color=WEIGHT),run_time=.4)
        self.play(token.animate.move_to(p(0,1.6)),run_time=.6)
        self.show(text('입력 종료 → 수용 · 추가 입력은 거부',y=-2.3,size=25,color=GOOD))
        self.cue(3);self.show(text('판정에 필요한 정보만 현재 상태로',y=-4,size=30,color=ACCENT));self.to(20.7)

        self.section('02  조금 달라진 규칙');self.cue(4)
        self.show(text('AⁿBⁿ  ·  n ≥ 1',y=3.7,size=45,color=SPARSE))
        self.cue(5)
        self.show(VGroup(text('AB',y=2.1,size=35,color=WEIGHT),text('AABB',y=.8,size=35,color=WEIGHT),text('AAABBB',y=-.5,size=35,color=WEIGHT)))
        self.show(text('모든 A가 먼저 · A와 B의 개수가 같음',y=-2.4,size=27,color=GOOD))
        self.cue(6);self.show(text('A의 개수가 나중의 판정을 바꾼다',y=-4,size=30,color=ACCENT));self.to(33.7)

        self.section('03  개수마다 상태를 만들면?');self.cue(7)
        self.show(text('1개      2개      3개',y=3.8,size=25,color=WEIGHT))
        for i in range(3):self.show(state(str(i+1),-2.4+i*2.4,2.7))
        self.cue(8)
        for row in range(3):
            self.show(VGroup(*[state(str(4+row*6+k),-3.1+k*1.25,.9-row*1.05).scale(.55) for k in range(6)]),.45)
        self.show(VGroup(text('상태 k개 · A¹, A², …, Aᵏ⁺¹',y=-2.65,size=27,color=ACCENT),text('k+1개의 과거 → 어떤 qᵢ = qⱼ  (i < j)',y=-3.65,size=25,color=GOOD),text('n에 상한이 있다면 유한 상태로 가능',y=-4.65,size=22,color=MUTED)));self.to(46.7)

        self.section('04  서로 다른 과거가 합쳐지는 순간');self.cue(9)
        self.show(text('같은 상태가 되면, 차이는 어디에 남을까?',y=4.2,size=29,color=ACCENT))
        self.show(text('아래 2회·5회는 충돌 상황의 설명용 예시',y=3.35,size=22,color=MUTED))
        self.cue(10)
        self.show(VGroup(text('AA',-2.4,2.35,37,WEIGHT),text('AAAAA',2.1,2.35,37,SPARSE)))
        qleft=self.show(state('q',-2,1,WEIGHT));qright=self.show(state('q',2,1,SPARSE))
        self.play(qleft.animate.move_to(p(0,.7)),qright.animate.move_to(p(0,.7)),run_time=1.2)
        self.play(FadeOut(qright),run_time=.2);self.stage.remove(qright)
        self.show(VGroup(Arrow(p(-2.1,1.9),p(-.5,1.1),buff=.05,color=WEIGHT),Arrow(p(2.1,1.9),p(.5,1.1),buff=.05,color=SPARSE)))
        self.cue(11)
        self.show(text('같은 입력\nBB',x=1.6,y=-.6,size=28,color=GOOD,width=2.5),.15)
        r=self.show(state('r',0,-2,ACCENT),.15);moving=self.show(Dot(p(0,.7),radius=.11,color=GOOD),.15)
        self.show(Arrow(p(0,.1),p(0,-1.4),buff=0,color=GOOD),.15)
        self.play(moving.animate.move_to(p(.35,-2)),run_time=.8)
        self.cue(12);self.show(VGroup(text('AABB : 수용 필요',-1.9,-3.25,26,GOOD,width=3.7),text('AAAAABB : 거부 필요',1.9,-3.25,25,PRUNE,width=3.7)))
        self.cue(13);self.show(text('그런데 최종 상태는 하나 · 판정도 하나',y=-4.3,size=28,color=PRUNE))
        self.cue(14);self.play(Circumscribe(r,color=ACCENT),run_time=.7)
        self.cue(15);self.show(text('AⁱBⁱ ∈ L  ·  AʲBⁱ ∉ L  ·  1 ≤ i < j',y=-5.05,size=22,color=MUTED));self.to(74.7)

        self.section('05  필요에 따라 늘어나는 기억 공간');self.cue(16)
        self.show(text('유한 제어 상태 + 크기 제한 없는 스택',y=4.15,size=27,color=SPARSE))
        self.show(VGroup(Line(p(-.8,.1),p(-.8,2.8),color=MUTED),Line(p(.8,.1),p(.8,2.8),color=MUTED),Line(p(-.8,.1),p(.8,.1),color=MUTED),text('스택',y=-.5,size=24,color=MUTED)))
        letters=self.show(VGroup(*[text(c,(i-1.5)*.9,-1.7,36,WEIGHT if c=='A' else GOOD) for i,c in enumerate('AABB')]))
        blocks=VGroup();self.cue(17)
        for i in range(2):
            b=Square(.6,color=WEIGHT,fill_color=WEIGHT,fill_opacity=.3).move_to(p(0,.45+i*.7));blocks.add(b);self.stage.add(b)
            self.play(FadeIn(b),Indicate(letters[i]),run_time=.55)
        for i in range(2):self.play(FadeOut(blocks[1-i]),Indicate(letters[2+i]),run_time=.55)
        self.cue(18);self.show(VGroup(text('AABB 종료 · 스택 비었음 → 수용',y=-2.9,size=26,color=GOOD),text('B 뒤의 A · 빈 스택에서 B → 거부',y=-3.8,size=22,color=MUTED)))
        self.cue(19);self.show(text('Pushdown Automaton · 푸시다운 오토마타',y=-4.8,size=23,color=SPARSE));self.to(90.7)

        self.section('06  미래를 위해 무엇을 남길까?');self.cue(20)
        self.show(text('RNN · Recurrent Neural Network',y=4.1,size=27,color=SPARSE))
        self.cue(21);self.show(text('hₜ = fθ(hₜ₋₁, xₜ)',y=2.95,size=43,color=ACCENT))
        boxes=VGroup(*[VGroup(RoundedRectangle(width=1.6,height=1.1,color=SPARSE).move_to(p(x,1)),text(label,x,1,25)) for x,label in [(-2.7,'hₜ₋₁'),(0,'fθ'),(2.7,'hₜ')]])
        self.show(boxes);self.show(VGroup(Arrow(p(-1.85,1),p(-.85,1),buff=0,color=MUTED),Arrow(p(.85,1),p(1.85,1),buff=0,color=MUTED),text('xₜ',0,-.5,29,WEIGHT),Arrow(p(0,-.1),p(0,.4),buff=0,color=WEIGHT)))
        self.cue(22);self.show(text('이전 상태 + 새 입력 → 다음 상태',y=-1.6,size=28,color=GOOD))
        self.cue(23);self.show(text('공통점: 과거를 상태로 요약하며 입력 처리',y=-2.7,size=25,color=WEIGHT))
        self.cue(24);self.show(VGroup(text('설계 예시: 명시적 전이 δ(q, x)',y=-3.8,size=25,color=WEIGHT),text('RNN: 학습한 상태 갱신 fθ(h, x)',y=-4.8,size=25,color=SPARSE)))
        self.cue(25);self.play(FadeOut(self.stage),run_time=.35);self.stage=VGroup()
        self.show(VGroup(text('AA',-2,3.65,34,WEIGHT),text('AAAAA',2,3.65,34,SPARSE),state('q',0,2.1,ACCENT),Arrow(p(-1.7,3.2),p(-.5,2.5),buff=.08,color=WEIGHT),Arrow(p(1.7,3.2),p(.5,2.5),buff=.08,color=SPARSE),text('서로 다른 판정이 필요한 과거의 차이',y=.75,size=27,color=PRUNE)))
        self.cue(26);self.show(text('RNN의 은닉 상태는 어떤 차이를 유지할까?',y=-.35,size=28,color=SPARSE))
        self.cue(27);self.show(VGroup(text('AⁿBⁿ에 필요한 정보',y=-1.55,size=27,color=ACCENT),text('현재 구간 · 아직 대응되지 않은 A의 개수',y=-2.55,size=25,color=GOOD)))
        self.cue(28);self.show(text('같은 상태 + 같은 후속 입력으로는 차이 복원 불가',y=-3.7,size=23,color=PRUNE))
        self.cue(29);self.show(text('입력 전체 대신 · 미래 판정에 필요한 정보',y=-4.8,size=25,color=WEIGHT))
        self.cue(30);self.play(FadeOut(self.stage),run_time=.4);self.stage=VGroup()
        self.show(VGroup(text('무엇을 구별할 수 있도록\n기억하는가',y=2.45,size=40,color=ACCENT),text('모든 후속 입력에서 판정이 같다면\n서로 다른 과거도 같은 상태로 묶을 수 있습니다.',y=-.25,size=26,color=GOOD),text('어떤 후속 입력에서 다른 판정이 필요하다면\n그 과거들은 구별해야 합니다.',y=-3.15,size=26,color=SPARSE)))
        self.to(140)
