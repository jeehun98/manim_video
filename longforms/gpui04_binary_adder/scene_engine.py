"""Binary addition: half/full adders, ripple dependency and carry lookahead."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_arithmetic import half,full,ripple,lookahead
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
class AdderScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.04:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  04',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/143)))
  self.add(base,bar,txt(f'{self.index+1:02} / 15',17,GRAY).move_to([x-.55,y+.27,0]))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 3.5):m.scale_to_fit_height(7.2 if VERT else 3.5)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)
 def question(self):
  g=VGroup(pill('NAND',2,1),pill('XOR',2,1,GREEN),pill('AND',2,1,ORANGE)).arrange(RIGHT,buff=.35)
  self.show(self.centered(g));self.note('입력 → 연결 구조 → 출력')
  self.at(4);e=self.equation('A + B = ?');self.replace(g,e)
  self.at(9);self.replace(e,self.equation('0 / 1  +  0 / 1',BLUE,48))
 def onebit(self):
  rows=VGroup(*[txt(s,43,GREEN) for s in ['0 + 0 = 0','0 + 1 = 1','1 + 0 = 1']]).arrange(DOWN,buff=.45)
  rows=self.centered(rows);self.show(rows);self.note('두 입력 · 한 자리의 합')
  self.at(15);e=self.equation('1 + 1 = 2',ORANGE);self.replace(rows,e)
  self.at(18);e2=VGroup(txt('1 + 1 = 10₂',58),txt('한 비트로 표현할 수 없음',29,ORANGE)).arrange(DOWN,buff=.65);self.replace(e,self.centered(e2))
 def split(self):
  e=txt('1 + 1 = 10₂',55).move_to([0,3.8 if VERT else 2.1,0]);self.show(e)
  cards=VGroup(VGroup(pill('1',1.8,1.3,ORANGE,55),txt('CARRY',26,ORANGE).shift(DOWN*1.2)),VGroup(pill('0',1.8,1.3,GREEN,55),txt('SUM',26,GREEN).shift(DOWN*1.2))).arrange(RIGHT,buff=1.4).move_to([0,.6 if VERT else 0,0])
  self.show(cards);self.note('다음 자리 ← 올림수  |  현재 자리의 합')
  self.at(26);self.play(Indicate(cards[1],color=GREEN),run_time=.7);self.play(Indicate(cards[0],color=ORANGE),run_time=.7)
 def table(self,kind):
  col=GREEN if kind=='XOR' else ORANGE;data=['A   B   '+('S' if kind=='XOR' else 'C')]
  for a,b in [(0,0),(0,1),(1,0),(1,1)]:data.append(f'{a}   {b}   {half(a,b)[0 if kind=="XOR" else 1]}')
  tab=VGroup(*[txt(s,39,col if i else INK) for i,s in enumerate(data)]).arrange(DOWN,buff=.22)
  formula=VGroup(pill(kind,2.5,1,col,34),txt('S = A ⊕ B' if kind=='XOR' else 'C = A ∧ B',36,col)).arrange(DOWN,buff=.65)
  g=VGroup(tab,formula).arrange(DOWN if VERT else RIGHT,buff=.7 if VERT else 2);return self.centered(g,7.3 if VERT else 12)
 def xor(self):
  t=self.table('XOR');self.show(t);self.note('입력이 서로 다르면 SUM = 1',GREEN)
  self.at(34);self.play(Indicate(t[0][2],color=GREEN),Indicate(t[0][3],color=GREEN),run_time=.8)
  self.at(38);self.play(Indicate(t[1],color=GREEN),run_time=.8)
 def and_method(self):
  t=self.table('AND');self.show(t);self.note('두 입력이 모두 1이면 CARRY = 1',ORANGE);self.play(Indicate(t[0][-1],color=ORANGE),run_time=.7)
 def halfdiagram(self,a=1,b=1):
  s,c=half(a,b);g=VGroup()
  for x,name,v,col in [(-2.9,'A',a,BLUE),(-2,'B',b,PURPLE)]:
   g.add(txt(f'{name}={v}',27,col).move_to([x,2.5,0]),ln((x,2.1),(x,-1),col))
   for y in [1,-1]:g.add(ln((x,y),(-.95,y+( .2 if name=='A' else -.2)),col),Dot([x,y,0],radius=.045,color=col))
  for y,kind,out,col in [(1,'XOR',f'S = {s}',GREEN),(-1,'AND',f'C = {c}',ORANGE)]:
   g.add(pill(kind,1.9,.9,col,30).move_to([0,y,0]),ln((.95,y),(1.7,y),col),pill(out,1.6,.85,col,30).move_to([2.5,y,0]))
  return self.centered(g)
 def half(self):
  g=self.halfdiagram();self.show(g);self.note('같은 A·B → SUM과 CARRY를 병렬로 계산')
  self.at(49);self.play(Indicate(g[-1],color=ORANGE),Indicate(g[-4],color=GREEN),run_time=.8)
  self.at(52);self.note('HALF ADDER  /  반가산기',GREEN)
 def binary(self,phase=0):
  g=VGroup(txt('11₂ + 01₂ = 100₂' if phase>1 else '11₂ + 01₂ = ?',39).move_to([0,3.2,0]))
  for x,a,b in [(-1.1,1,0),(1.1,1,1)]:
   g.add(txt(str(a),57,BLUE).move_to([x,1.7,0]),txt(str(b),57,PURPLE).move_to([x,.7,0]),ln((x-.7,0),(x+.7,0),INK))
   g.add(txt('0' if phase and (x>0 or phase>1) else '?',57,GREEN if phase else GRAY).move_to([x,-.7,0]))
  if phase:
   g.add(route((1.1,-1.35),(1.1,-2),(-2.1,-2),(-2.1,2.4),(-1.1,2.4),c=ORANGE,w=3),pill('C = 1',1.5,.65,ORANGE).move_to([0,-2,0]))
  if phase>1:g.add(txt('1',57,ORANGE).move_to([-2.7,-.7,0]),pill('Cin = 1',1.8,.65,ORANGE).move_to([-1.1,2.55,0]))
  return self.centered(g)
 def columns(self):
  g=self.halfdiagram();self.show(g);self.note('反가산기의 입력은 두 개'.replace('反','반'))
  self.at(59);self.replace(g,self.binary());self.note('오른쪽부터 계산 · 이진수 자리값')
 def carry(self):
  g=self.binary(1);self.show(g);self.note('오른쪽 1 + 1 → 합 0, 올림수 1')
  self.at(67);h=self.binary(2);self.replace(g,h);self.note('왼쪽은 1 + 0 + 1 → 합 0, 올림수 1',ORANGE)
 def fullnet(self):
  # Two separate carry wires terminate at distinct OR input pins.
  g=VGroup()
  for x,name in [(-2,'HA 1'),(1,'HA 2')]:g.add(pill(name,1.7,1.15,GREEN,27).move_to([x,.8,0]))
  g.add(txt('A=1',26,BLUE).move_to([-3.5,1.6,0]),txt('B=0',26,PURPLE).move_to([-3.5,.7,0]),ln((-3,1.1),(-2.85,1.1),BLUE),ln((-3,.55),(-2.85,.55),PURPLE),ln((-1.15,1.05),(.15,1.05),GREEN),txt('X=1',21,GREEN).move_to([-.5,1.5,0]),route((-.6,2.5),(-.6,.55),(.15,.55),c=ORANGE),txt('Cin=1',26,ORANGE).move_to([-.6,2.9,0]),ln((1.85,1.05),(2.7,1.05),GREEN),txt('S=0',30,GREEN).move_to([3.2,1.05,0]))
  gate=pill('OR',1.6,.9,ORANGE,27).move_to([1,-1.8,0]);g.add(gate)
  g.add(route((-2,.225),(-2,-1.58),(.2,-1.58),c=ORANGE),route((1,.225),(2.2,.225),(2.2,-.65),(-.1,-.65),(-.1,-2.02),(.2,-2.02),c=ORANGE),txt('c₁=0',22,ORANGE).move_to([-2.4,-.8,0]),txt('c₂=1',22,ORANGE).move_to([2.6,-.5,0]),ln((1.8,-1.8),(2.7,-1.8),ORANGE),txt('Cout=1',27,ORANGE).move_to([3.4,-1.8,0]),txt('HA 1: A+B   /   HA 2: X+Cin',23,GRAY).move_to([0,-2.8,0]))
  return self.centered(g,7.6 if VERT else 12)
 def full(self):
  g=VGroup(pill('A',1.5,.8,BLUE),pill('B',1.5,.8,PURPLE),pill('Cin',1.5,.8,ORANGE)).arrange(RIGHT,buff=.4);self.show(self.centered(g));self.note('세 입력 → 합 S + 다음 자리 올림수 Cout')
  self.at(74);self.note('FULL ADDER  /  전가산기',GREEN)
  self.at(75);self.replace(g,self.fullnet());self.note('S = (A ⊕ B) ⊕ Cin  |  Cout = c₁ OR c₂')
 def chain(self,resolved=0,scale=1):
  g=VGroup();self.blocks=[];self.carrywires=[]
  for i in range(4):
   x=2.7-i*1.8;col=GREEN if i<resolved else GRAY
   block=pill(f'FA {i}',1.25,1,col,25).move_to([x,0,0]);self.blocks.append(block);g.add(block)
   g.add(txt('A=1',22,BLUE).move_to([x,1.8,0]),txt(f'B={1 if i==0 else 0}',22,PURPLE).move_to([x,1.2,0]),ln((x-.22,.9),(x-.22,.5),BLUE),ln((x+.22,.9),(x+.22,.5),PURPLE),ln((x,-.5),(x,-1),col),txt('0' if i<resolved else '…',32,col).move_to([x,-1.4,0]))
   if i<3:
    w=Arrow([x-.625,0,0],[x-1.8+.625,0,0],buff=0,stroke_width=3,max_tip_length_to_length_ratio=.3,color=ORANGE if i<resolved else GRAY);g.add(w);self.carrywires.append(w)
  g.add(route((3.8,-1.9),(3.8,0),(3.325,0),c=ORANGE),route((-3.325,0),(-3.8,0),(-3.8,-1),c=ORANGE if resolved==4 else GRAY),txt('Cin=0',22,ORANGE).move_to([3.3,-2.2,0]),txt('1' if resolved==4 else '?',32,ORANGE).move_to([-3.8,-1.4,0]),txt('상위 자리 ← CARRY ← 하위 자리',22,GRAY).move_to([0,2.6,0]))
  # This is a block diagram; all A/B inputs are visible before any carry resolves.
  return g.scale(scale)
 def ripple(self):
  g=self.centered(self.chain(4));self.show(g);self.note('1111₂ + 0001₂ = 10000₂')
  self.at(85);self.note('RIPPLE CARRY ADDER  /  리플 캐리 가산기',ORANGE)
 def delay(self):
  g=self.centered(self.chain(0));self.show(g);self.note('A·B는 모든 자리에 동시에 공급됨')
  self.at(89);self.note('상위 자리의 최종 합은 이전 자리의 CARRY에 의존',ORANGE)
  self.at(95)
  for i in range(1,5):
   h=self.centered(self.chain(i));self.replace(g,h);g=h;self.at(95+i)
  self.at(100);self.note('1111₂ + 0001₂ = 10000₂  /  최악의 경로 예시',GREEN)
  marks=VGroup(*[txt(f't{i+1}',24,ORANGE).move_to([2.7-i*1.8,-2.6,0]) for i in range(4)])
  if not VERT:marks.scale(.8).move_to([0,-1.6,0])
  self.show(marks);self.note('논리적 도착 순서 모형 · 실측 시간 아님')
 def gp(self):
  q=self.centered(self.chain(0));self.show(q);self.note('올림수를 기다리기 전에 알 수 있는 조건은?')
  self.at(108)
  cards=VGroup(*[VGroup(pill(f'bit {i}',1.5,.65,INK),txt(f'G={1 if i==0 else 0}',25,ORANGE).shift(DOWN*.9),txt(f'P={0 if i==0 else 1}',25,GREEN).shift(DOWN*1.6)) for i in [3,2,1,0]]).arrange(RIGHT,buff=.25)
  formulas=VGroup(txt('G = A ∧ B',36,ORANGE),txt('P = A ⊕ B',36,GREEN)).arrange(DOWN,buff=.4)
  g=self.centered(VGroup(cards,formulas).arrange(DOWN,buff=.8));self.replace(q,g);self.note('각 자리에서 동시에 계산 · 발생 Generate / 전달 Propagate')
 def lanet(self,stage=0):
  g=VGroup();cols=[-2.7,-.9,.9,2.7]
  for j,x in enumerate(cols):
   g.add(pill(f'G{3-j}, P{3-j}',1.5,.65,ORANGE if stage else GRAY,22).move_to([x,2.5,0]))
  for j,x in enumerate(cols):
   g.add(pill(f'C{4-j} 논리항',1.5,.8,GREEN if stage>=2 else GRAY,20).move_to([x,.5,0]),pill('OR',1.25,.65,ORANGE if stage>=3 else GRAY,22).move_to([x,-1,0]),txt('1' if stage>=3 else '…',30,ORANGE if stage>=3 else GRAY).move_to([x,-2,0]))
   for k in range(j,4):
    xx=cols[k];g.add(route((xx,2.15),(xx,1.7-.13*j),(x,1.7-.13*j),(x,.9),c=GREEN if stage>=2 else EDGE,w=1.2))
   g.add(ln((x,.1),(x,-.675),ORANGE if stage>=3 else GRAY),ln((x,-1.325),(x,-1.7),ORANGE if stage>=3 else GRAY))
  return self.centered(g)
 def lookahead(self):
  g=self.lanet(1);self.show(g);self.note('G·P → 여러 올림수의 조건을 각각 전개')
  self.at(115);h=self.lanet(2);self.replace(g,h);g=h;self.note('예: C₂ = G₁ OR (P₁ AND G₀)  /  Cin=0')
  self.at(117);h=self.lanet(3);self.replace(g,h);g=h;self.note('논리항 계산 → OR 결합 → 각 자리 합 계산')
  self.at(118.5);self.note('1111₂ + 0001₂ = 10000₂  /  두 회로의 결과는 동일',GREEN)
 def tradeoff(self):
  g=self.lanet(3);self.show(g);self.note('CARRY LOOKAHEAD  /  캐리 룩어헤드',ORANGE)
  self.at(123);self.note('의존 경로를 줄이기 위한 추가 논리 회로와 배선')
  self.play(Indicate(g,color=ORANGE),run_time=.8)
  self.at(127)
  cards=VGroup(*[VGroup(pill(a,2.7,1,c,34),txt(b,24,c).shift(DOWN*.9)) for a,b,c in [('SPEED','얼마나 빠르게?',GREEN),('AREA','회로와 배선',BLUE),('ENERGY','구조·부하·전환',ORANGE)]]).arrange(DOWN if VERT else RIGHT,buff=.65)
  self.replace(g,self.centered(cards,7.3 if VERT else 12));self.note('같은 덧셈 · 다른 하드웨어  /  Same Arithmetic')
 def alu(self):
  g=self.halfdiagram();self.show(g);self.note('논리 게이트의 조합 → 실제 산술 연산',GREEN)
  self.at(136);q=self.centered(pill('ADDER',3.6,1.5,GREEN,42));self.replace(g,q)
  self.at(138)
  ops=VGroup(pill('ADD',2.6,1,GREEN,34),pill('SUBTRACT',2.6,1,BLUE,30),pill('COMPARE',2.6,1,PURPLE,30)).arrange(DOWN if VERT else RIGHT,buff=.5)
  box=SurroundingRectangle(ops,buff=.4,color=GRAY);h=self.centered(VGroup(ops,box));self.replace(q,h)
  self.at(140);self.note('Arithmetic Logic Unit  /  ALU',INK)

# Python keyword cannot be used as a method definition.
setattr(AdderScene,'and',AdderScene.and_method)
