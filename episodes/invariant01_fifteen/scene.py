"""Independent portrait claims with exact narration timing and audited legal moves."""
import json
import os
import sys
from pathlib import Path
from manim import *

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from longforms.qcs01_speed.direction import QCSScene,label
from episodes.invariant01_fifteen.model import SOLVED,IMPOSSIBLE,neighbors,parity,color,invariant,move,samples

DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BG,INK,MUTED='#101923','#EDF3FC','#8B9CB7'
BLUE,GOLD,GREEN,RED='#61AEFF','#FFD275','#52E2A8','#FF747F'
LIGHT,DARK='#607287','#192A40'
config.background_color=BG

def txt(s,y=0,size=34,c=INK,x=0,width=7.5):
    return label(s,x=x,y=y,size=size,color=c,width=width)

def panel(s,y,c=GREEN,w=7.1,h=.9,size=29):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.15,stroke_color=c,
        fill_color=c,fill_opacity=.05),txt(s,size=size,c=c,width=w-.3)).move_to(UP*y)

def letters(y):
    return VGroup(*[VGroup(RoundedRectangle(width=1.25,height=1.25,corner_radius=.15,
        stroke_color=BLUE,fill_color=BLUE,fill_opacity=.12),txt(s,size=44,c=BLUE)).move_to([x,y,0])
        for s,x in zip('ABC',(-1.65,0,1.65))])

class Board(VGroup):
    def __init__(self,state=SOLVED,y=1.25,side=5.5,checker=False):
        super().__init__()
        self.state=tuple(state);self.count=0;self.step=side/4
        self.positions=[np.array([(i%4-1.5)*self.step,y+(1.5-i//4)*self.step,0]) for i in range(16)]
        self.slots=VGroup(*[Square(side_length=self.step-.04,stroke_width=1,stroke_color=MUTED,
            fill_color=(LIGHT if (i//4+i%4)%2==0 else DARK) if checker else DARK,
            fill_opacity=1).move_to(self.positions[i]) for i in range(16)])
        self.tiles={n:VGroup(RoundedRectangle(width=self.step-.13,height=self.step-.13,corner_radius=.1,
                    stroke_color=BLUE,stroke_width=2,fill_color=BLUE,fill_opacity=.12),
                    txt(str(n),size=34,c=INK,width=self.step-.25)).move_to(self.positions[i])
                    for i,n in enumerate(state) if n}
        self.blank=VGroup(Square(side_length=self.step-.15,stroke_color=GOLD,stroke_width=3),
                         txt('빈칸',size=18,c=GOLD,width=self.step-.25)).move_to(self.positions[state.index(0)])
        self.add(self.slots,*self.tiles.values(),self.blank)
    def checker(self,scene):
        scene.play(*[m.animate.set_fill(LIGHT if (i//4+i%4)%2==0 else DARK,opacity=1)
            for i,m in enumerate(self.slots)],run_time=.8)
    def status(self,y=-2.4,full=False):
        p,c=parity(self.state),color(self.state)
        first=f'전체 순열: {"짝" if p==0 else "홀"}   ·   빈칸: {"밝음" if c==0 else "어두움"}'
        if full:return VGroup(txt(first,y,27,GOLD),panel(f'I = p ⊕ c = {invariant(self.state)}',y-1.15,GREEN))
        return txt(f'{self.count}회 이동   ·   순열 {"짝" if p==0 else "홀"}   ·   {"밝음" if c==0 else "어두움"}',y,27,GOLD)
    def slide(self,scene,index,duration=.65,hud=None,full=False):
        old=self.state;blank=old.index(0);n=old[index]
        new=move(old,index)
        self.state=new;self.count+=1
        animations=[self.tiles[n].animate.move_to(self.positions[blank]),self.blank.animate.move_to(self.positions[index])]
        if hud is not None:animations.append(Transform(hud,self.status(full=full)))
        at=scene.offset+scene.time
        scene.play(*animations,run_time=duration)
        scene.transitions.append(dict(at=round(at,6),end=round(scene.offset+scene.time,6),
            before=list(old),after=list(new),tile=n,index=index,count=self.count,p=parity(new),c=color(new),I=invariant(new)))
    def tile(self,scene,n,**kw):self.slide(scene,self.state.index(n),**kw)

class InvariantScene(QCSScene):
    data=DATA
    def setup(self):
        super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.35)
        self.add(txt('불변량  /  INVARIANT',7,19,MUTED));self.transitions=[]
    def construct(self):
        super().construct()
        audit=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'audit')))
        (audit/(self.info['id']+'_moves.json')).write_text(json.dumps(self.transitions),encoding='utf-8')
    def exchange(self,group,i,j,duration=.8):
        self.play(Swap(group[i],group[j]),run_time=duration)
        items=list(group);items[i],items[j]=items[j],items[i]
        return VGroup(*items)

def graph():
    positions=[(-3,0),(-1.7,1.45),(-1.5,-1.6),(-.1,2.6),(.15,.6),(.15,-2.5),(1.7,1.55),(1.8,-.85)]
    nodes=VGroup(*[Dot([x,y+.7,0],radius=.13,color=BLUE) for x,y in positions])
    edges=VGroup(*[Line(nodes[a].get_center(),nodes[b].get_center(),color=BLUE,stroke_width=2)
                  for a,b in [(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(4,6),(4,7),(5,7)]])
    target=Dot([3.1,2.9,0],radius=.17,color=RED)
    return nodes,edges,target

class Shot01(InvariantScene):
    shot=0
    def s01(self):
        nodes,edges,target=graph()
        self.show(nodes[0],txt('시작',-.1,24,BLUE,x=-3))
        self.play(LaggedStart(*[Create(e) for e in edges],lag_ratio=.12),FadeIn(nodes[1:]),run_time=2.4)
        self.to(5)
        self.show(target,txt('목표',3.6,26,RED,x=3.05,width=1.3))
        self.to(10)
        self.show(txt('모든 경로를 확인해야 할까?',-3.2,35))
        self.to(16)
        self.play(Indicate(target,color=RED))
        self.to(18)
        marks=VGroup(*[Circle(radius=.25,color=GREEN,stroke_width=3).move_to(n) for n in nodes])
        self.show(marks)
        self.play(edges.animate.set_opacity(.22))
        self.show(txt('움직여도 유지되는 규칙',-4.25,29,GREEN))

class Shot02(InvariantScene):
    shot=1
    def s02(self):
        board=Board();self.show(board)
        self.to(28)
        self.show(txt('빈칸과 인접한 타일만 이동',-2.6,29,BLUE))
        for n in (15,11,11,15):board.tile(self,n,duration=.7)
        assert board.state==SOLVED
        self.to(34)
        notice=txt('설정: 타일을 들어 14·15만 교환',4.45,24,RED)
        self.show(notice)
        a,b=board.tiles[14],board.tiles[15]
        self.play(a.animate.shift(UP*.3),b.animate.shift(UP*.3),run_time=.35)
        self.play(Swap(a,b),run_time=1)
        self.play(a.animate.move_to(board.positions[14]),b.animate.move_to(board.positions[13]),run_time=.35)
        board.state=IMPOSSIBLE
        self.play(a[0].animate.set_stroke(RED,4),b[0].animate.set_stroke(RED,4))
        self.to(39)
        self.show(panel('이 배열에서는 되돌릴 수 없다',-3.9,RED))

class Shot03(InvariantScene):
    shot=2
    def s03(self):
        row=letters(2.6);self.show(row)
        self.to(49);row=self.exchange(row,0,1)
        self.to(52);row=self.exchange(row,1,2)
        path=txt('ABC  →  BAC  →  BCA',.7,33,BLUE)
        self.show(path)
        self.to(56)
        self.play(FadeOut(row),FadeOut(path))
        self.show(txt('같은 결과 BAC를 만드는 두 방법',3.7,29))
        upper=letters(2);lower=letters(-.8)
        self.show(upper,lower)
        upper=self.exchange(upper,0,1)
        self.show(txt('1번 교환 · 홀수',.8,29,GOLD))
        self.to(61)
        for _ in range(3):lower=self.exchange(lower,0,1,.6)
        self.show(txt('3번 교환 · 홀수',-2,29,GOLD))
        self.to(67)
        self.show(panel('순열의 홀짝성',-3.7,GOLD))

class Shot04(InvariantScene):
    shot=3
    def s04(self):
        upper=letters(2.5);lower=letters(-.6)
        self.show(upper,lower)
        upper=self.exchange(upper,0,1)
        self.show(txt('ABC → BAC  ·  1번: 홀순열',1.2,29,GOLD))
        self.to(74)
        lower=self.exchange(lower,0,1)
        lower=self.exchange(lower,1,2)
        self.show(txt('ABC → BAC → BCA',-1.9,29,BLUE),txt('2번 교환: 짝순열',-3.1,32,GOLD))
        self.to(81)
        self.play(FadeOut(VGroup(upper,lower)),run_time=.5)
        self.show(txt('퍼즐에서는 어떤 교환이 가능할까?',4.3,26,GREEN))

class Shot05(InvariantScene):
    shot=4
    def s05(self):
        board=Board();self.show(board)
        rule=txt('임의의 두 숫자 교환은 금지',-2.5,29,RED);self.show(rule)
        self.to(88)
        self.play(Transform(rule,txt('빈칸과 인접한 숫자만 교환',-2.5,29,BLUE)))
        board.tile(self,15)
        self.to(91)
        self.show(panel('타일 1번 이동 = 빈칸과 1번 교환',-3.8,GOLD))
        board.tile(self,15)
        board.tile(self,12)
        board.tile(self,12)
        self.to(97)
        board.checker(self)
        self.show(txt('색은 움직이는 타일이 아닌 고정된 칸의 색',4.45,22,MUTED))

class Shot06(InvariantScene):
    shot=5
    def s06(self):
        board=Board(checker=True);self.add(board)
        hud=board.status();self.add(hud)
        board.tile(self,15,hud=hud)
        self.to(104)
        board.tile(self,15,hud=hud)
        self.to(106)
        self.show(panel('빈칸 원위치 → 반드시 짝수 번 이동',-3.8,GREEN))
        for n in (12,12):board.tile(self,n,hud=hud,duration=.6)
        self.to(111)
        for n in (15,11,11,15):board.tile(self,n,hud=hud,duration=.6)
        assert board.state==SOLVED and board.count%2==0
        self.show(txt('순열은 빈칸까지 포함한 16개 원소 기준',4.45,22,MUTED))

class Shot07(InvariantScene):
    shot=6
    def s07(self):
        board=Board(IMPOSSIBLE,checker=True);self.show(board)
        for n in (14,15):board.tiles[n][0].set_stroke(RED,4)
        self.show(txt('14·15만 교환 · 빈칸은 그대로',4.45,24,RED))
        self.to(122)
        self.show(panel('목표 배열: 1번 교환 → 홀순열',-2.5,RED))
        self.to(125)
        self.show(panel('빈칸 원위치 → 짝수 이동 → 짝순열',-3.65,GREEN,size=26))
        self.play(Indicate(board.blank,color=GREEN))
        self.to(130)
        self.play(FadeOut(board),run_time=.5)
        self.show(txt('홀순열  ≠  짝순열',1.7,46,RED),txt('두 조건을 동시에 만족할 수 없다',.1,32))
        self.to(132)
        self.show(panel('도달 불가능',-1.25,RED))
        self.to(134)
        self.show(txt('시도 횟수의 문제가 아니다',3.6,29,GREEN))

class Shot08(InvariantScene):
    shot=7
    def s08(self):
        board=Board(checker=True,y=1.4,side=5.3);self.add(board)
        hud=board.status(full=True);self.add(hud)
        self.show(txt('순열 p: 짝=0 · 홀=1   /   색 c: 밝음=0 · 어두움=1',4.45,20,MUTED))
        for at,n in [(138,15),(140,11),(142,12),(144,15)]:
            self.to(at);board.tile(self,n,hud=hud,full=True,duration=.65)
        self.to(146)
        self.play(Circumscribe(hud,color=GREEN,buff=.14),run_time=1)
        self.to(148)
        self.show(txt('불변량 · Invariant',-4.35,29,GREEN))
        self.to(149)
        board.tile(self,11,hud=hud,full=True)
        self.to(150)
        board.tile(self,12,hud=hud,full=True)

class Shot09(InvariantScene):
    shot=8
    def s09(self):
        left=list(samples(SOLVED,8));right=list(samples(IMPOSSIBLE,8))
        assert all(invariant(s)==0 for s in left) and all(invariant(s)==1 for s in right)
        areas=VGroup(RoundedRectangle(width=3.2,height=4.6,color=GREEN,corner_radius=.2).move_to([-1.85,.7,0]),
                     RoundedRectangle(width=3.2,height=4.6,color=RED,corner_radius=.2).move_to([1.85,.7,0]))
        self.show(areas,txt('I = 0',3.65,40,GREEN,x=-1.85,width=3),txt('I = 1',3.65,40,RED,x=1.85,width=3))
        dots=VGroup(*[Dot([x+(k%2-.5)*1.1,2.1-(k//2)*.85,0],radius=.15,color=col)
                     for states,x,col in [(left,-1.85,GREEN),(right,1.85,RED)] for k,_ in enumerate(states)])
        self.play(LaggedStart(*[FadeIn(m) for m in dots],lag_ratio=.04),run_time=1.2)
        self.show(txt('완성 상태',-2.25,28,GREEN,x=-1.85,width=3),txt('14·15 교환',-2.25,28,RED,x=1.85,width=3))
        self.show(panel('불변량이 다르면 연결될 수 없다',-3.65,GREEN))
        self.show(txt('실제 합법 이동으로 얻은 상태들의 개념도',4.6,20,MUTED))

class Shot10(InvariantScene):
    shot=9
    def s10(self):
        question=txt('무엇을 바꿀 수 있는가?',2.8,40,BLUE)
        self.show(question)
        self.to(159)
        self.play(question.animate.scale(.8).move_to(UP*3.7),run_time=.7)
        answer=txt('무엇을 해도\n변하지 않는 것은 무엇인가?',.6,43,GREEN)
        self.show(answer)
        self.to(162)
        self.show(txt('불변량',-2.1,55,GREEN),txt('Invariant',-3.35,28,MUTED))
        self.to(164)
