"""Four-bit registers, input selection and non-destructive datapath reads."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_datapath import bits,integer,mux,write,compute
R=Path(__file__).resolve().parent;VERT=os.getenv('GPUI_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1020'
INK='#F8FAFC';BLUE='#60A5FA';PURPLE='#A78BFA';GREEN='#34D399';GRAY='#64748B';ORANGE='#F59E0B';EDGE='#29374D';PANEL='#142037'
TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'));MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=29,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def pill(s,w=2,h=.65,color=INK,size=25):return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=color,stroke_width=1.3,fill_color=PANEL,fill_opacity=1),txt(s,size,color,w-.22))
def ln(a,b,c=GRAY,w=2.3):return Line([*a,0],[*b,0],color=c,stroke_width=w)
def route(*pts,c=GRAY,w=2):return VMobject(color=c,stroke_width=w).set_points_as_corners([np.array([*p,0]) for p in pts])
def label_update(m,s,c=INK):
 if getattr(m,'_word',None)!=s:
  new=txt(s,26,c);new.scale_to_fit_height(m.height);new.move_to(m);m.become(new);m._word=s
 return m
def setlabel(m,s,color=INK,size=27,width=None):
 key=(s,str(color))
 if getattr(m,'_labelkey',None)==key:return m
 new=txt(s,size,color);new.scale_to_fit_height(m.height);m.become(new.move_to(m.get_center()));m._labelkey=key;return m

class DatapathScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+1/config.frame_rate+.005:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  08',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
  self.notice=txt(' ',24);self.add(self.notice);self.note(' ')
  starts=[r['start'] for r in TIMING]
  def idx():
   now=self.start+self.time;i=bisect_right(starts,now+1e-7)-1
   return i if 0<=i<len(TIMING) and now<TIMING[i]['end']-1e-7 else -1
  def caption(i):
   s='\n'.join(textwrap.wrap(TIMING[i]['text'] if i>=0 else ' ',width=26 if VERT else 52))
   return txt(s,30 if VERT else 29,INK,7.55 if VERT else 14.2).move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(31)
  self.active_caption=idx();self.caption=caption(self.active_caption)
  def update(m):
   i=idx()
   if i!=self.active_caption:m.become(caption(i));m.set_z_index(31);self.active_caption=i
  self.caption.add_updater(update)
  panel=Rectangle(width=8.2 if VERT else 15,height=2.25 if VERT else 1.4,stroke_width=0,fill_color=config.background_color,fill_opacity=1).move_to(self.caption).set_z_index(29)
  self.add(panel,self.caption)
  x=3.9 if VERT else 7.3;y=-7.24 if VERT else -4.1;base=ln((-x,y),(x,y),EDGE,2);bar=base.copy().set_color(BLUE)
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/153)))
  self.add(base,bar,txt(f'{self.index+1:02} / 14',17,GRAY).move_to([x-.55,y+.27,0]))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)

class Register(VGroup):
 def __init__(self,value=5):
  super().__init__();self.cells=VGroup();self.value=value
  for i,b in enumerate(bits(value)):
   x=(i-1.5)*1.25;cell=pill(str(b),1,.95,GREEN,38).move_to([x,0,0]);self.cells.add(cell)
  self.add(self.cells,txt('4-bit Register',26,BLUE).move_to([0,1.3,0]),txt('CLK  ↑',23,ORANGE).move_to([-2.5,-1.2,0]),ln((-1.8,-1.2),(1.88,-1.2),ORANGE))
  for i in range(4):
   x=(i-1.5)*1.25;self.add(ln((x,-1.2),(x,-.5),ORANGE),txt('D',17,GRAY).move_to([x,.8,0]))
  self.decimal=txt(f'= {value}',30,GREEN).move_to([0,-2,0]);self.add(self.decimal)
 def store(self,n):
  self.value=n
  for c,b in zip(self.cells,bits(n)):setlabel(c[1],str(b),GREEN)
  setlabel(self.decimal,f'= {n}',GREEN)

class Reuse(VGroup):
 def __init__(self,sel=0,b=3,saved=8):
  super().__init__();self.saved=saved;self.sel=sel;self.b=b
  self.external=pill('5',1,.65,BLUE).move_to([-3.1,1.4,0]);self.reg=pill(f'R = {saved}',1.7,.8,GREEN).move_to([-3.1,-1.2,0])
  self.mux=Polygon([-.9,1.6,0],[-.9,-.7,0],[.3,-.3,0],[.3,1.2,0],color=BLUE,fill_color=PANEL,fill_opacity=1)
  self.add(self.external,self.reg,self.mux,txt('MUX',23).move_to([-.4,.45,0]))
  self.paths=[route((-2.6,1.4),(-1.8,1.4),(-1.8,1),(-.9,1)),route((-2.25,-1.2),(-1.5,-1.2),(-1.5,-.1),(-.9,-.1))]
  self.alu=pill('ALU  +',2,1.4,PURPLE,30).move_to([2,.5,0]);self.result=txt('8',38,GREEN).move_to([4,.5,0]);self.bl=txt(f'B = {b}',25,PURPLE).move_to([1.6,2,0]);self.sl=txt(f'SEL = {sel}',24,ORANGE).move_to([-.4,-1.5,0]);self.we=txt('WE = 0',23,ORANGE).move_to([1,-2.6,0]);self.av=txt('A = 5',23,BLUE).move_to([.65,1.5,0])
  self.add(*self.paths,self.alu,self.result,self.bl,self.sl,self.we,self.av,ln((.3,.5),(1,.5),BLUE),route((2,1.7),(2,1.2),c=PURPLE),ln((3,.5),(3.6,.5),GREEN),route((4,0),(4,-2),(-3.1,-2),(-3.1,-1.6),c=GRAY),ln((-.4,-1.2),(-.4,-.7),ORANGE))
  self.state(sel,b)
 def state(self,sel,b):
  self.sel=sel;self.b=b
  for i,p in enumerate(self.paths):p.set_stroke(BLUE if i==sel else GRAY,opacity=1 if i==sel else .35)
  setlabel(self.sl,f'SEL = {sel}',ORANGE);setlabel(self.bl,f'B = {b}',PURPLE);a=mux(5,self.saved,sel);setlabel(self.av,f'A = {a}',BLUE);setlabel(self.result,str(a+b),GREEN)
 def store(self,n):self.saved=n;setlabel(self.reg[1],f'R = {n}',GREEN)

class DataCircuit(VGroup):
 def __init__(self):
  super().__init__();self.regs=VGroup(*[pill(s,2,.75,GREEN,25).move_to([-4,y,0]) for s,y in zip(['R1 = 5','R2 = 3','R3 = 0'],[1.7,0,-1.7])]);self.add(self.regs)
  self.reads=[]
  for j,cy in enumerate([1.2,-1.2]):
   box=pill('MUX '+('A' if j==0 else 'B'),1.5,1.4,BLUE if j==0 else PURPLE,23).move_to([0,cy,0]);self.add(box)
   for i,y in enumerate([1.7,0,-1.7]):
    lane=-2.7+i*.45+j*.12;p=route((-3,y),(lane,y),(lane,cy+.4-i*.4),(-.75,cy+.4-i*.4),c=GRAY,w=1.5);self.add(p);self.reads.append(p)
  self.alu=pill('ALU  +',2,1.5,PURPLE,30).move_to([3,0,0]);self.add(self.alu,route((.75,1.2),(1.4,1.2),(1.4,.4),(2,.4),c=BLUE),route((.75,-1.2),(1.6,-1.2),(1.6,-.4),(2,-.4),c=PURPLE))
  self.writer=pill('Write → R3',2.5,.7,ORANGE,24).move_to([.4,-2.7,0]);self.result=txt('8',33,GREEN).move_to([4.7,.6,0]);self.wl=txt('WE = 0   CLK ↑',21,ORANGE).move_to([2.9,-2.7,0])
  self.back=route((4,0),(5.3,0),(5.3,-2.1),(.4,-2.1),(.4,-2.35),c=GRAY)
  self.add(self.writer,self.result,self.wl,self.back,route((-.85,-2.7),(-5.5,-2.7),(-5.5,-1.7),(-5,-1.7),c=ORANGE),txt('A: R1',21,BLUE).move_to([0,2.3,0]),txt('B: R2',21,PURPLE).move_to([0,-.2,0]))
 def read(self):
  self.reads[0].set_stroke(BLUE,opacity=1,width=3);self.reads[4].set_stroke(PURPLE,opacity=1,width=3)
 def save(self):setlabel(self.regs[2][1],'R3 = 8',GREEN);setlabel(self.wl,'WE = 1   CLK ↑',ORANGE);self.back.set_stroke(GREEN,width=3)

# Each section is a complete, independently replaceable clip.
def hook(self):
 r=self.centered(Register(1),5);self.show(r);self.note('저장된 값과 계산 회로를 연결한다');self.at(6)
 g=VGroup(pill('저장된 값',2.3,.9,GREEN).move_to([-2.3,0,0]),pill('ALU',2,.9,PURPLE).move_to([2.2,0,0]),DashedLine(LEFT,RIGHT,color=GRAY));self.replace(r,self.centered(g));self.at(11)
def onebit(self):
 c=self.centered(VGroup(pill('D',1,.7,BLUE).move_to([-2,0,0]),pill('D Flip-Flop',2.8,1.4,GREEN),pill('Q = 0',1.6,.8,GREEN).move_to([3,0,0]),txt('CLK ↑',25,ORANGE).move_to([0,-1.4,0])),7.5);self.show(c);self.at(14);self.note('1 bit = 두 상태 중 하나를 저장');self.at(18);setlabel(c[2][1],'Q = 1',GREEN);self.play(Indicate(c[1],color=ORANGE),run_time=.5);self.at(20);self.replace(c,self.equation('5 → 0101\n3 → 0011\n8 → 1000',BLUE,43));self.note('이 영상에서는 4비트로 표현합니다')
def bits_scene(self):
 r=self.centered(Register(5),6);self.show(r);self.note('5 = 0101  ·  각 자리마다 별도의 저장 요소');self.at(27);self.play(LaggedStart(*[Indicate(c,color=BLUE) for c in r.cells],lag_ratio=.2),run_time=1)
def register_scene(self):
 r=self.centered(Register(5),6);self.show(r);self.at(35);self.note('서로 다른 4개의 D 입력 · 하나의 공통 CLK',ORANGE);self.play(Indicate(r,color=ORANGE),run_time=.7);self.at(41);self.note('4개의 1비트 저장 요소 → 4비트 레지스터',GREEN)
def stored(self):
 r=self.centered(Register(5),6);self.show(r);self.at(46);self.note('D = 1000  →  CLK ↑  →  Q = 1000',ORANGE);self.at(48);r.store(8);self.play(Indicate(r.cells,color=GREEN),run_time=.5);self.at(50);self.note('이 값을 다음 계산에 사용하려면?');self.at(52);self.replace(r,self.centered(Reuse(1,2,8),7.8 if VERT else 11));self.note('저장된 8을 ALU의 입력으로 전달',BLUE)
def sequence(self):
 d=self.centered(Reuse(0,3,0),7.8 if VERT else 11);self.show(d);self.note('(5 + 3) + 2 = 10');self.at(65);self.play(Indicate(d.alu,color=PURPLE),run_time=.6);self.at(69);setlabel(d.we,'WE = 1 · CLK ↑',ORANGE);d.store(8);self.play(Indicate(d.reg,color=GREEN),run_time=.5);self.at(72);setlabel(d.we,'WE = 0',ORANGE);d.state(1,2);self.note('첫 결과 8을 보관한 뒤, 다음 입력으로 사용',GREEN)
def mux_scene(self):
 d=self.centered(Reuse(0,2,8),7.8 if VERT else 11);self.show(d);self.note('두 후보를 같은 입력에 직접 연결하지 않습니다');self.at(81);self.play(Indicate(d.mux,color=BLUE),run_time=.6);self.note('MUX가 후보 중 하나만 선택합니다',BLUE);self.at(86);d.state(1,2);self.play(Indicate(d.paths[1],color=BLUE),run_time=.5)
def reuse_scene(self):
 d=self.centered(Reuse(0,3,8),7.8 if VERT else 11);self.show(d);self.note('① SEL = 0 : 5 + 3 = 8');self.at(94);setlabel(d.we,'WE = 1 · CLK ↑',ORANGE);self.play(Indicate(d.reg,color=GREEN),run_time=.5);self.at(95);setlabel(d.we,'WE = 0',ORANGE);d.state(1,2);self.note('② SEL = 1 : 8 + 2 = 10 · 레지스터는 8 유지');self.at(97);self.play(Indicate(d.alu,color=PURPLE),run_time=.6);self.note('동일한 배선 · 동일한 ALU · 서로 다른 입력')
def many(self):
 r=self.centered(Register(5),6);self.show(r);self.note('레지스터 하나에는 한 시점에 하나의 값');self.at(104);r.store(3);self.at(106);r.store(8);self.at(107)
 g=VGroup(*[pill(s,3,.9,GREEN,29).move_to([0,y,0]) for s,y in zip(['R1   0101 = 5','R2   0011 = 3','R3   1000 = 8'],[1.4,0,-1.4])]);self.replace(r,self.centered(g));self.note('여러 값을 동시에 보관하려면 여러 레지스터')
def readwrite(self):
 d=self.centered(DataCircuit(),7.8 if VERT else 12.5);self.show(d);d.read();self.note('읽기: R1, R2  →  계산: 5 + 3');self.at(115);d.save();self.note('쓰기: R3 선택 + WE + CLK 상승 에지',ORANGE);self.play(Indicate(d.regs[2],color=GREEN),run_time=.5)
def datapath(self):
 d=self.centered(DataCircuit(),7.8 if VERT else 12.5);self.show(d);self.note('독립된 두 읽기 경로 A / B',BLUE);self.at(120);d.read();self.at(122);self.play(Indicate(d.alu,color=PURPLE),run_time=.5);self.at(124);d.save();self.note('선택 → 연산 → 다시 저장 = Datapath',GREEN)
def roles(self):
 d=self.centered(DataCircuit(),7.8 if VERT else 12.5);d.read();d.save();self.show(d);self.note('ALU : 계산',PURPLE);self.play(Indicate(d.alu,color=PURPLE),run_time=.6);self.at(130);self.note('Register : 값 보관',GREEN);self.play(Indicate(d.regs,color=GREEN),run_time=.6);self.at(132);self.note('Datapath : 선택과 전달을 포함하는 연결 구조',BLUE);self.at(134);self.play(Indicate(d.reads[0],color=BLUE),Indicate(d.reads[4],color=PURPLE),run_time=.7);self.at(136);self.note('읽어도 R1 = 5, R2 = 3은 유지됩니다');self.play(Indicate(d.regs,color=GREEN),run_time=.7)
def control(self):
 g=VGroup(*[pill(s,3,.9,c,28).move_to([0,y,0]) for s,y,c in [('어떤 값을 읽을까?',1.5,BLUE),('어떤 연산을 할까?',0,PURPLE),('어디에 기록할까?',-1.5,GREEN)]]);self.show(self.centered(g));self.at(142);self.note('입력 선택 · 연산 선택 · 쓰기 대상',ORANGE)
def instruction(self):
 g=VGroup(pill('명령어',2.8,1,ORANGE,35).move_to([0,1.8,0]),pill('입력 선택',2,.7,BLUE).move_to([-2.4,-.6,0]),pill('연산 선택',2,.7,PURPLE).move_to([0,-.6,0]),pill('저장 제어',2,.7,GREEN).move_to([2.4,-.6,0]))
 for x in [-2.4,0,2.4]:g.add(DashedLine([x*.35,1.3,0],[x,-.1,0],color=ORANGE))
 self.show(self.centered(g));self.note('제어 신호가 데이터 경로의 동작을 선택합니다')
for name,fn in [('hook',hook),('onebit',onebit),('bits',bits_scene),('register',register_scene),('stored',stored),('sequence',sequence),('mux',mux_scene),('reuse',reuse_scene),('many',many),('readwrite',readwrite),('datapath',datapath),('roles',roles),('control',control),('instruction',instruction)]:setattr(DatapathScene,name,fn)

