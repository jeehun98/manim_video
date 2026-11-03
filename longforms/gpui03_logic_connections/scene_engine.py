"""Switch topology, CMOS NAND, NAND-only composition and physical design costs."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from logic_model import nand_state,NETLISTS,evaluate
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
def ground(x,y):return VGroup(*[ln((x-v/2,y-i*.13),(x+v/2,y-i*.13),INK) for i,v in enumerate([.9,.6,.3])])
class Switch(VGroup):
 def __init__(self,name,q,color):
  super().__init__();self.q=q
  self.contacts=VGroup(Dot([-.46,0,0],radius=.05,color=INK),Dot([.46,0,0],radius=.05,color=INK));self.lever=ln((-.46,0),(.3,.52))
  def update(m):
   a=self.contacts[0].get_center();b=self.contacts[1].get_center();m.put_start_and_end_on(a,a+rotate_vector(b-a,(1-q.get_value())*.63));m.set_color(GREEN if q.get_value()>.85 else GRAY)
  self.lever.add_updater(update);self.add(self.contacts,self.lever,txt(name,26,color).move_to([0,.82,0]))
class SwitchNetwork(VGroup):
 def __init__(self,mode='series',a=None,b=None):
  super().__init__();self.mode=mode;self.a=a if a is not None else ValueTracker(0);self.b=b if b is not None else ValueTracker(0)
  self.sa=Switch('A',self.a,BLUE);self.sb=Switch('B',self.b,PURPLE)
  self.wires=VGroup();self.branches=VGroup()
  def active():return self.a.get_value()>.85 and self.b.get_value()>.85 if mode=='series' else self.a.get_value()>.85 or self.b.get_value()>.85
  if mode=='series':
   self.sa.shift([-1.35,1.05,0]);self.sb.shift([1.2,1.05,0])
   for a0,b0 in [((-3.2,1.05),(-1.81,1.05)),((-.89,1.05),(.74,1.05)),((1.66,1.05),(3.2,1.05)),((-3.2,-.15),(-3.2,1.05)),((3.2,1.05),(3.2,-.15))]:self.wires.add(ln(a0,b0))
  else:
   self.sa.shift([0,1.05,0]);self.sb.shift([0,-.35,0])
   self.wires.add(route((-3.2,-.15),(-3.2,.35),(-2.5,.35)),route((2.5,.35),(3.2,.35),(3.2,-.15)))
   for y,q in [(1.05,self.a),(-.35,self.b)]:
    branch=VGroup(route((-2.5,.35),(-2.5,y),(-.46,y)),route((.46,y),(2.5,y),(2.5,.35)))
    branch.add_updater(lambda m,v=q:m.set_color(GREEN if v.get_value()>.85 else GRAY).set_stroke(opacity=1 if v.get_value()>.85 else .5));self.branches.add(branch)
  self.wires.add(route((3.2,-.85),(3.2,-1.8),(-3.2,-1.8),(-3.2,-.85)))
  self.wires.add_updater(lambda m:m.set_color(GREEN if active() else GRAY).set_stroke(opacity=1 if active() else .5))
  source=VGroup(Circle(radius=.35,color=BLUE).move_to([-3.2,-.5,0]),txt('+',23,BLUE).move_to([-3.2,-.38,0]),txt('−',23,BLUE).move_to([-3.2,-.63,0]))
  self.load=Circle(radius=.35,color=GRAY,fill_color=GREEN).move_to([3.2,-.5,0]);self.load.add_updater(lambda m:m.set_fill(GREEN,.45 if active() else 0).set_stroke(GREEN if active() else GRAY))
  self.status=pill('경로 차단',w=2.5,size=23).move_to([0,-2.25,0]);self.status[1]._word='경로 차단'
  self.status[1].add_updater(lambda m:label_update(m,'경로 연결' if active() else '경로 차단',GREEN if active() else GRAY))
  self.add(self.wires,self.branches,source,self.load,self.sa,self.sb,self.status)
class NandCircuit(VGroup):
 def __init__(self,a=0,b=0):
  super().__init__();self.a=ValueTracker(a);self.b=ValueTracker(b)
  self.supply=VGroup(ln((0,3.05),(0,2.5),INK),ln((-.5,3.05),(.5,3.05),INK),txt('VDD',25).move_to([0,3.43,0]))
  self.ground=VGroup(ln((0,-2.35),(0,-2.8)),ground(0,-2.8),txt('GND',23,GRAY).move_to([0,-3.25,0]))
  self.upper_common=VGroup(ln((-1.5,2.5),(1.5,2.5)),ln((-1.5,.55),(1.5,.55)),ln((0,.55),(0,0)))
  self.upper=VGroup()
  for x,q in [(-1.5,self.a),(1.5,self.b)]:
   branch=VGroup(ln((x,2.5),(x,2)),ln((x,2),(x,1.1),w=4),ln((x,1.1),(x,.55)))
   branch.add_updater(lambda m,v=q:m.set_color(GREEN if v.get_value()<.5 else GRAY).set_opacity(1 if v.get_value()<.5 else .45));self.upper.add(branch)
  self.lower_common=VGroup(ln((0,0),(0,-.35)),ln((0,-1.2),(0,-1.5)))
  self.lower=VGroup(ln((0,-.35),(0,-1.2),w=4),ln((0,-1.5),(0,-2.35),w=4))
  for segment,q in zip(self.lower,[self.a,self.b]):segment.add_updater(lambda m,v=q:m.set_color(GREEN if v.get_value()>=.5 else GRAY).set_opacity(1 if v.get_value()>=.5 else .45))
  self.upper_common.add_updater(lambda m:m.set_color(GREEN if self.state()['up'] else GRAY).set_opacity(1 if self.state()['up'] else .45))
  self.lower_common.add_updater(lambda m:m.set_color(GREEN if self.state()['down'] else GRAY).set_opacity(1 if self.state()['down'] else .45))
  self.ground[0].add_updater(lambda m:m.set_color(GREEN if self.state()['down'] else GRAY))
  # Gate buses stay outside the output wire: there are no ambiguous crossings.
  self.control=VGroup(ln((-1.83,1.1),(-1.83,2),BLUE),ln((1.83,1.1),(1.83,2),PURPLE),Circle(radius=.09,color=BLUE,fill_color=config.background_color,fill_opacity=1).move_to([-1.98,1.55,0]),Circle(radius=.09,color=PURPLE,fill_color=config.background_color,fill_opacity=1).move_to([1.98,1.55,0]),route((-3.8,2),(-3.8,-.775),(-.33,-.775),c=BLUE),ln((-.33,-.35),(-.33,-1.2),BLUE),route((3.8,2),(3.8,-1.925),(.33,-1.925),c=PURPLE),ln((.33,-1.5),(.33,-2.35),PURPLE),ln((-3.8,1.55),(-2.07,1.55),BLUE),ln((3.8,1.55),(2.07,1.55),PURPLE))
  self.inputs=VGroup(pill(f'A = {a}',1.5,.65,BLUE).move_to([-3.8,2.35,0]),pill(f'B = {b}',1.5,.65,PURPLE).move_to([3.8,2.35,0]))
  self.control.add(ln((-1.89,1.55),(-1.83,1.55),BLUE),ln((1.89,1.55),(1.83,1.55),PURPLE))
  for card,q,name,col in [(self.inputs[0],self.a,'A',BLUE),(self.inputs[1],self.b,'B',PURPLE)]:
   card[1]._word=f'{name} = {int(q.get_value())}';card[1].add_updater(lambda m,v=q,k=name,c=col:label_update(m,f'{k} = {int(v.get_value()>=.5)}',c))
  self.node=Dot([0,0,0],radius=.08,color=INK);self.out_wire=ln((0,0),(.95,0),INK)
  self.output=pill(f'Y = {int(not(a and b))}',2.5,.8,INK,size=34).move_to([2.25,0,0]);self.output[1]._word=f'Y = {int(not(a and b))}'
  self.output[1].add_updater(lambda m:label_update(m,f'Y = {self.state()["y"]}',INK))
  self.names=VGroup(txt('pMOS A',21,BLUE).move_to([-1.5,2.85,0]),txt('pMOS B',21,PURPLE).move_to([1.5,2.85,0]),txt('nMOS A',21,BLUE).move_to([-1.25,-1.16,0]),txt('nMOS B',21,PURPLE).move_to([1.3,-2.3,0]))
  self.add(self.supply,self.ground,self.upper_common,self.upper,self.lower_common,self.lower,self.control,self.inputs,self.node,self.out_wire,self.output,self.names)
 def state(self):return nand_state(self.a.get_value()>=.5,self.b.get_value()>=.5)
class NandGlyph(VGroup):
 def __init__(self):
  super().__init__()
  body=VMobject(color=INK,stroke_width=1.6,fill_color=PANEL,fill_opacity=1)
  body.start_new_path(np.array([-.6,-.45,0]));body.add_line_to(np.array([-.6,.45,0]));body.add_line_to(np.array([.05,.45,0]));body.add_cubic_bezier_curve_to(np.array([.82,.45,0]),np.array([.82,-.45,0]),np.array([.05,-.45,0]));body.close_path()
  self.pa=VectorizedPoint([-.95,.22,0]);self.pb=VectorizedPoint([-.95,-.22,0]);self.po=VectorizedPoint([1.0,0,0])
  self.add(body,Circle(radius=.085,color=INK,fill_color=config.background_color,fill_opacity=1).move_to([.72,0,0]),ln((-.95,.22),(-.6,.22),INK,1.5),ln((-.95,-.22),(-.6,-.22),INK,1.5),ln((.81,0),(1,0),INK,1.5),txt('NAND',14,INK).move_to([-.08,0,0]),self.pa,self.pb,self.po)
def nand_network(name):
 """Draw exactly the netlist in logic_model.py; tied input nodes are explicit."""
 out=VGroup();gates=VGroup();wires=VGroup();out.gates=gates;out.wires=wires
 if name=='NOT':
  g=NandGlyph();gates.add(g)
  wires.add(route((-2,0),(-1.3,0),(-1.3,.22),(-.95,.22),c=BLUE),route((-1.3,0),(-1.3,-.22),(-.95,-.22),c=BLUE),ln((1,0),(2,0),INK))
  out.add(txt('A',23,BLUE).move_to([-2.3,0,0]),txt('Y',23,INK).move_to([2.3,0,0]))
 elif name=='AND':
  g=NandGlyph().shift([-1.5,0,0]);h=NandGlyph().shift([1,0,0]);gates.add(g,h)
  wires.add(ln((-3.3,.22),(-2.45,.22),BLUE),ln((-3.3,-.22),(-2.45,-.22),PURPLE),route((-.5,0),(-.15,0),(-.15,.22),(.05,.22),c=INK),route((-.15,0),(-.15,-.22),(.05,-.22),c=INK),ln((2,0),(3.1,0),INK))
  out.add(txt('A',22,BLUE).move_to([-3.6,.3,0]),txt('B',22,PURPLE).move_to([-3.6,-.3,0]),txt('Y',23).move_to([3.4,0,0]))
 elif name=='OR':
  gates.add(NandGlyph().shift([-1.4,.85,0]),NandGlyph().shift([-1.4,-.85,0]),NandGlyph().shift([1.4,0,0]))
  for y,col in [(.85,BLUE),(-.85,PURPLE)]:
   wires.add(route((-3.4,y),(-2.7,y),(-2.7,y+.22),(-2.35,y+.22),c=col),route((-2.7,y),(-2.7,y-.22),(-2.35,y-.22),c=col))
  wires.add(route((-.4,.85),(.1,.85),(.1,.22),(.45,.22),c=INK),route((-.4,-.85),(.1,-.85),(.1,-.22),(.45,-.22),c=INK),ln((2.4,0),(3.4,0),INK))
  out.add(txt('A',22,BLUE).move_to([-3.7,.85,0]),txt('B',22,PURPLE).move_to([-3.7,-.85,0]),txt('Y',23).move_to([3.7,0,0]))
 else:
  gates.add(NandGlyph().shift([-2,0,0]),NandGlyph().shift([1,1,0]),NandGlyph().shift([1,-1,0]),NandGlyph().shift([3.5,0,0]))
  wires.add(route((-4,1.4),(-3.3,1.4),(-3.3,.22),(-2.95,.22),c=BLUE),route((-3.3,1.4),(-.3,1.4),(-.3,1.22),(.05,1.22),c=BLUE),route((-4,-1.4),(-3.3,-1.4),(-3.3,-.22),(-2.95,-.22),c=PURPLE),route((-3.3,-1.4),(-.3,-1.4),(-.3,-1.22),(.05,-1.22),c=PURPLE),route((-1,0),(-.5,0),(-.5,.78),(.05,.78),c=INK),route((-.5,0),(-.5,-.78),(.05,-.78),c=INK),route((2,1),(2.4,1),(2.4,.22),(2.55,.22),c=INK),route((2,-1),(2.4,-1),(2.4,-.22),(2.55,-.22),c=INK),ln((4.5,0),(5,0),INK))
  out.add(txt('A',22,BLUE).move_to([-4.3,1.4,0]),txt('B',22,PURPLE).move_to([-4.3,-1.4,0]),txt('Y',23).move_to([5.3,0,0]))
 out.add(wires,gates);return out

class LogicScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.04:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  03',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/164)))
  self.add(base,bar,txt(f'{self.index+1:02} / 14',17,GRAY).move_to([x-.55,y+.27,0]))
  [self.switches,self.series,self.parallel,self.rules,self.physical_rule,self.voltage,self.nand_build,self.nand_states,self.compose,self.complete,self.fixed,self.costs,self.tradeoffs,self.arithmetic][self.index]()
  self.at(self.end)
 def change(self,n,a,b,d=.55):self.play(n.a.animate.set_value(a),n.b.animate.set_value(b),run_time=d)
 def net(self,mode='series',a=None,b=None):
  n=SwitchNetwork(mode,a,b).scale(.95 if VERT else .86).move_to([0,1.3 if VERT else .55,0]);n.update(0);return n
 def paired(self):
  a=SwitchNetwork('series');b=SwitchNetwork('parallel',a.a,a.b)
  if VERT:a.scale(.72).move_to([0,3.4,0]);b.scale(.72).move_to([0,-.3,0])
  else:a.scale(.88).move_to([-4,.45,0]);b.scale(.88).move_to([4,.45,0])
  a.update(0);b.update(0);return a,b
 def nand(self,a=0,b=0):
  n=NandCircuit(a,b).scale(.78 if VERT else .60).move_to([0,1.3 if VERT else .3,0]);n.update(0);return n

 def switches(self):
  q=ValueTracker(0)
  body=Rectangle(width=5.8,height=1.8,color=GRAY,fill_color=PANEL,fill_opacity=1).move_to([0,.4,0])
  regions=VGroup(*[Rectangle(width=1.05,height=.65,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([x,.97,0]) for x in [-2.1,2.1]])
  oxide=Rectangle(width=3.2,height=.18,color=INK,fill_color=GRAY,fill_opacity=.2).move_to([0,1.42,0]);gate=Rectangle(width=3.2,height=.4,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([0,1.75,0])
  channel=Rectangle(width=3.3,height=.12,stroke_width=0,fill_color=GREEN).move_to([0,1.21,0]);channel.add_updater(lambda m:m.set_fill(GREEN,q.get_value()*.8))
  section=VGroup(body,regions,channel,oxide,gate).move_to([0,1.5 if VERT else .5,0]);self.add(section)
  self.play(q.animate.set_value(1),run_time=1.2);self.note('전압이 전도 경로를 제어')
  self.at(4);a=Switch('A',q,BLUE).scale(1.4).move_to([0,1.4 if VERT else .4,0])
  self.play(FadeOut(section),FadeIn(a),run_time=.6)
  self.play(q.animate.set_value(0),run_time=.6);self.play(q.animate.set_value(1),run_time=.6);self.play(q.animate.set_value(0),run_time=.6)
  self.at(9);b=Switch('B',ValueTracker(0),PURPLE).scale(1.4).move_to([2.2,1.4 if VERT else .4,0])
  self.play(a.animate.move_to([-2.2,1.4 if VERT else .4,0]),TransformFromCopy(a,b),run_time=.9);self.note('같은 기능의 스위치 A · B')

 def series(self):
  n=self.net();self.play(FadeIn(n),run_time=.7)
  self.change(n,1,0,.55);self.wait(.2);self.change(n,0,1,.55)
  self.at(16);self.change(n,1,1,.7);self.note('두 스위치가 모두 닫힐 때만 전체 경로 연결',GREEN)

 def parallel(self):
  n=self.net();n.a.set_value(1);n.b.set_value(1);n.update(0);self.add(n)
  self.change(n,0,0,.45)
  p=self.net('parallel',n.a,n.b)
  # Transform the existing A/B, then replace the old wiring with two branches.
  n.wires.suspend_updating();n.status.suspend_updating()
  self.play(Transform(n.sa,p.sa),Transform(n.sb,p.sb),FadeOut(n.wires),FadeOut(n.status),FadeIn(p.wires),FadeIn(p.branches),run_time=1.3)
  self.remove(n,*list(n));self.add(p)
  self.at(22);self.change(p,1,0,.7);self.note('A 경로 하나만 연결해도 통로 확보',GREEN)
  self.at(26);self.play(Indicate(p.sa,color=BLUE),Indicate(p.sb,color=PURPLE),run_time=.7)
  self.at(28);self.change(p,0,1,.7);self.wait(.8);self.change(p,1,1,.7);self.note('연결 방식이 바뀌면 연결 조건도 바뀝니다',INK)

 def rules(self):
  a,b=self.paired();self.add(a,b);self.note('참·거짓은 경로의 연결 조건 · CMOS 출력 전압과 구별')
  self.change(a,1,0,.6);self.at(36)
  namea=txt('AND',32,INK).next_to(a,UP,buff=.15);self.play(FadeIn(namea),run_time=.5);self.change(a,1,1,.6)
  self.at(40);nameb=txt('OR',32,INK).next_to(b,UP,buff=.15);self.play(FadeIn(nameb),run_time=.5);self.change(a,0,1,.6)

 def physical_rule(self):
  a,b=self.paired();self.add(a,b);self.change(a,1,0,.6);self.at(45)
  code=pill('if A and B: ...',w=3.7,h=.5,color=GRAY,size=24).move_to([0,5.6 if VERT else 2.5,0]);self.play(FadeIn(code),run_time=.5)
  self.change(a,0,1,.6);self.play(code.animate.set_opacity(.15),run_time=.6);self.change(a,1,1,.6);self.play(FadeOut(code),run_time=.4)
  self.at(50);self.note('Physical Connection → Logical Rule',INK)
  self.change(a,0,0,.7);self.change(a,1,0,.7);self.play(Indicate(a.wires,color=ORANGE),Indicate(b.branches,color=ORANGE),run_time=.8)

 def voltage(self):
  cx=0;cy=1.2 if VERT else .3
  top=ln((cx,cy+2),(cx,cy),GREEN,3);bottom=ln((cx,cy),(cx,cy-2),GRAY,3)
  labels=VGroup(txt('VDD',27).move_to([cx,cy+2.4,0]),ground(cx,cy-2),txt('GND',24,GRAY).move_to([cx,cy-2.6,0]))
  dot=Dot([cx,cy,0],radius=.1,color=INK);wire=ln((cx,cy),(cx+1.6,cy),INK)
  out=pill('Y = HIGH',2.6,.8,INK,30).move_to([cx+2.7,cy,0])
  diagram=VGroup(top,bottom,labels,dot,wire,out)
  if not VERT:diagram.scale(.8).move_to([0,.5,0])
  self.play(FadeIn(diagram),run_time=.8);self.note('전원 연결 → HIGH',GREEN)
  self.at(59);new=pill('Y = LOW',2.6,.8,INK,30).match_height(out).move_to(out)
  self.play(top.animate.set_color(GRAY).set_opacity(.4),bottom.animate.set_color(GREEN),Transform(out,new),run_time=.8)
  self.note('접지 연결 → LOW · 경로 조건과 출력 전압은 다릅니다',BLUE)

 def nand_build(self):
  n=self.nand(0,0)
  self.add(n.node,n.output,n.out_wire,n.supply,n.ground)
  self.play(FadeIn(n.lower),FadeIn(n.lower_common),run_time=.8);self.note('아래쪽: nMOS A · B 직렬')
  self.at(66);self.play(FadeIn(n.upper),FadeIn(n.upper_common),run_time=.8);self.note('위쪽: pMOS A · B 병렬')
  self.at(69);self.play(FadeIn(n.control),FadeIn(n.inputs),FadeIn(n.names),run_time=.7)
  self.note('네 소자 · 하나의 출력 노드 · 두 상보적 네트워크',INK)

 def truth_table(self,name='NAND'):
  group=VGroup(txt('A   B     Y',24,GRAY))
  for a,b in [(0,0),(0,1),(1,0),(1,1)]:
   y=nand_state(a,b)['y'] if name=='NAND' else evaluate(name,a,b)['Y'];group.add(txt(f'{a}   {b}     {y}',27,INK))
  return group.arrange(DOWN,buff=.24)
 def nand_states(self):
  n=self.nand(1,1);self.add(n);self.note('A=B=1 → 전원 차단 · 접지 연결 · Y=0',INK)
  self.at(75)
  table=self.truth_table()
  if VERT:
   self.play(n.animate.scale(.74).move_to([0,2.1,0]),run_time=.4);table.scale(.72).move_to([0,-1.7,0])
  else:
   self.play(n.animate.move_to([-3.8,.3,0]),run_time=.4);table.move_to([3.7,.35,0])
  self.play(FadeIn(table),run_time=.4)
  for i,(a,b) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
   self.change(n,a,b,.55)
   state=nand_state(a,b);self.note(f'A B = {a}{b} → {"VDD 연결" if state["up"] else "GND 연결"} · Y={state["y"]}',INK)
   self.play(Indicate(table[i+1],color=GREEN),run_time=.35)
  self.note('정적 논리 상태의 경로 검증 · 스위칭 과도 상태는 생략')

 def compositions(self):
  groups=VGroup()
  for i,name in enumerate(['NOT','AND','OR']):
   net=nand_network(name);net.scale((.90 if name=='NOT' else .73) if VERT else (.73 if name=='NOT' else .58))
   lab=txt(name,29,INK).next_to(net,UP,buff=.22);g=VGroup(net,lab)
   g.move_to([0,[3.65,1.45,-1.1][i],0] if VERT else [[-4.9,0,4.9][i],.45,0]);groups.add(g)
  return groups
 def compose(self):
  n=self.nand(1,1);self.add(n);symbol=NandGlyph().scale(1.5).move_to([0,1.3 if VERT else .4,0])
  self.play(FadeOut(n),FadeIn(symbol),run_time=1);self.note('같은 NAND 출력을 다른 NAND 입력에 연결')
  self.at(84);groups=self.compositions();self.play(FadeOut(symbol),run_time=.35)
  self.play(LaggedStart(*[FadeIn(g) for g in groups],lag_ratio=.5),run_time=1.65)

 def complete(self):
  groups=self.compositions();self.add(groups);self.note('NOT(A)=NAND(A,A)  ·  드모르간 법칙으로 OR 구성')
  self.at(91);self.play(*[Indicate(g[0].gates,color=GREEN) for g in groups],run_time=1)
  self.at(93);self.play(groups.animate.set_opacity(.35),run_time=.4)
  title=VGroup(txt('기능적 완전성',38,INK),txt('Functional Completeness',26,INK),txt('유한한 이진 입력의 임의 불 함수',24,GRAY)).arrange(DOWN,buff=.25).move_to([0,1.5 if VERT else .45,0])
  bg=RoundedRectangle(width=7.5 if VERT else 11,height=2.3,corner_radius=.15,stroke_color=EDGE,fill_color=config.background_color,fill_opacity=1).move_to(title)
  self.play(FadeIn(bg),FadeIn(title),run_time=.6)

 def fixed(self):
  andnet=nand_network('AND').scale(.94 if VERT else 1.2).move_to([0,2 if VERT else .5,0]);self.add(andnet)
  tag=txt('고정된 AND 회로',28).next_to(andnet,UP,buff=.35);self.add(tag)
  self.note('같은 입력 A·B를 넣는 고정 단일 기능 회로의 예시')
  values=pill('A B = 00   →   Y = 0',w=5.1,size=29).move_to([0,-.3 if VERT else -1.3,0]);self.play(FadeIn(values),run_time=.6)
  for a,b in [(0,1),(1,0),(1,1)]:self.play(Transform(values,pill(f'A B = {a}{b}   →   Y = {evaluate("AND",a,b)["Y"]}',5.1,size=29).move_to(values)),run_time=.6)
  self.at(100);self.play(FadeOut(values),run_time=.4)
  compare=VGroup(txt('A B       AND    XOR',26,GRAY),txt('0 1          0  ≠  1',35,ORANGE)).arrange(DOWN,buff=.35).move_to([0,-1.2 if VERT else -.9,0]);self.play(FadeIn(compare),run_time=.7)
  self.at(106);self.play(Indicate(andnet.wires,color=ORANGE),run_time=.9);self.note('Fixed Connections · 입력값은 배선을 바꾸지 않습니다',ORANGE)
  self.at(111);self.play(FadeOut(compare),run_time=.4)
  xor=nand_network('XOR').scale(.68 if VERT else .62)
  if VERT:self.play(andnet.animate.scale(.75).move_to([0,3.6,0]),tag.animate.move_to([0,4.65,0]),run_time=.6);xor.move_to([0,-.5,0])
  else:self.play(andnet.animate.scale(.65).move_to([-4,.5,0]),tag.animate.move_to([-4,2,0]),run_time=.6);xor.move_to([3.6,.35,0])
  lab=txt('XOR: 다른 연결 구조 · NAND 4개',26,INK,7.2).next_to(xor,UP,buff=.3)
  self.play(FadeIn(xor),FadeIn(lab),run_time=1.3);self.note('ALU의 미리 구현된 기능 선택과 구별합니다')

 def gate_grid(self,n=16):
  cols=4 if VERT else 6;g=VGroup(*[NandGlyph().scale(.57 if VERT else .55) for _ in range(n)])
  g.arrange_in_grid(cols=cols,buff=(.35,.35)).move_to([0,1.25 if VERT else .35,0])
  wires=VGroup(*[Line(g[i].po.get_center(),g[i+1].pa.get_center(),color=GRAY,stroke_width=1) for i in range(n-1) if (i+1)%cols])
  return VGroup(wires,g)
 def costs(self):
  grid=self.gate_grid(16 if VERT else 24);outline=SurroundingRectangle(grid,buff=.35,color=ORANGE,stroke_width=1.5)
  self.play(LaggedStart(*[FadeIn(g) for g in grid[1]],lag_ratio=.04),Create(grid[0]),Create(outline),run_time=2)
  self.note('Area / Transistors / Wiring',ORANGE);self.at(124)
  self.play(FadeOut(grid),FadeOut(outline),run_time=.3)
  chain=VGroup(*[NandGlyph().scale(.85) for _ in range(4)]).arrange(DOWN if VERT else RIGHT,buff=.7).move_to([0,1.4 if VERT else .5,0])
  links=VGroup();values=VGroup()
  for i,g in enumerate(chain):
   values.add(txt(str(1-i%2),25,GREEN if i%2==0 else GRAY).next_to(g,RIGHT if VERT else UP,buff=.2))
   if i==0:continue
   prev=chain[i-1].po.get_center();pa=g.pa.get_center();pb=g.pb.get_center();yc=g.get_center()[1]
   if VERT:
    branch=VGroup(route(tuple(prev[:2]),(1.5,prev[1]),(1.5,yc+.6),(-1.5,yc+.6),(-1.5,yc),(pa[0]-.2,yc),c=GRAY,w=1.3))
   else:branch=VGroup(route(tuple(prev[:2]),(pa[0]-.2,prev[1]),(pa[0]-.2,yc),c=GRAY,w=1.3))
   branch.add(route((pa[0]-.2,yc),(pa[0]-.2,pa[1]),tuple(pa[:2]),c=GRAY,w=1.3),route((pa[0]-.2,yc),(pa[0]-.2,pb[1]),tuple(pb[:2]),c=GRAY,w=1.3));links.add(branch)
  pa=chain[0].pa.get_center();pb=chain[0].pb.get_center();yc=chain[0].get_center()[1]
  source=pill('IN = 0',w=1.3,h=.6,color=BLUE,size=23).move_to([-3 if VERT else -6.1,yc,0])
  fork=pa[0]-.3
  feed=VGroup(ln((source.get_right()[0],yc),(fork,yc),BLUE,1.4),route((fork,yc),(fork,pa[1]),tuple(pa[:2]),c=BLUE,w=1.4),route((fork,yc),(fork,pb[1]),tuple(pb[:2]),c=BLUE,w=1.4))
  self.play(FadeIn(chain),FadeIn(links),FadeIn(values),FadeIn(source),Create(feed),run_time=.5);self.note('Propagation Delay · 입력 전환 후 단계별 출력 변화')
  self.play(Transform(source,pill('IN = 1',w=1.3,h=.6,color=BLUE,size=23).move_to(source)),run_time=.35)
  for i,g in enumerate(chain):
   new=txt(str(i%2),25,GREEN if i%2 else GRAY).move_to(values[i]);self.play(Indicate(g,color=GREEN),Transform(values[i],new),run_time=.65)
  self.at(129);self.play(FadeOut(chain),FadeOut(links),FadeOut(values),FadeOut(source),FadeOut(feed),run_time=.3)
  # Equivalent output load, with capacitive charging/discharging rather than particles.
  cy=1.3 if VERT else .5
  voltage=ValueTracker(0);charging=ValueTracker(0)
  pullup=VGroup(ln((0,cy+2),(0,cy+1.3)),ln((0,cy+1.3),(0,cy+.6),w=4),ln((0,cy+.6),(0,cy)))
  pulldown=VGroup(ln((0,cy),(0,cy-.5)),ln((0,cy-.5),(0,cy-1.2),w=4),ln((0,cy-1.2),(0,cy-1.85)))
  pullup.add_updater(lambda m:m.set_color(GREEN if charging.get_value()>.5 else GRAY).set_opacity(1 if charging.get_value()>.5 else .4))
  pulldown.add_updater(lambda m:m.set_color(GREEN if charging.get_value()<.5 else GRAY).set_opacity(1 if charging.get_value()<.5 else .4))
  circuit=VGroup(pullup,pulldown,ln((-.35,cy+.7),(-.35,cy+1.2),PURPLE),ln((-.35,cy-.6),(-.35,cy-1.1),PURPLE),ground(0,cy-1.85),ln((0,cy),(2.5,cy),INK),Dot([0,cy,0],radius=.08,color=INK),ln((2.5,cy),(2.5,cy-.6),INK),ln((2,cy-.6),(3,cy-.6),INK),ln((2,cy-.85),(3,cy-.85),INK),ln((2.5,cy-.85),(2.5,cy-1.65),INK),ground(2.5,cy-1.65),txt('VDD',26).move_to([0,cy+2.3,0]),txt('C load',26,BLUE).move_to([1.2,cy-.7,0]))
  meter=Rectangle(width=.65,height=1.8,color=BLUE,stroke_width=1.3).move_to([-2.2,cy,0])
  fill=Rectangle(width=.62,height=.01,fill_color=BLUE,fill_opacity=.5,stroke_width=0)
  fill.add_updater(lambda m:m.stretch_to_fit_height(max(.01,1.75*voltage.get_value())).move_to(meter.get_bottom()+UP*max(.005,.875*voltage.get_value())))
  self.play(FadeIn(circuit),FadeIn(meter),FadeIn(fill),run_time=.6);self.note('출력 부하의 등가 정전용량 · 전압 변화의 모형')
  charging.set_value(1);self.play(voltage.animate.set_value(1),run_time=1.5);charging.set_value(0);self.play(voltage.animate.set_value(0),run_time=1.5)
  self.at(135)
  heat=VGroup(*[VMobject(color=ORANGE,stroke_width=2).set_points_smoothly([[x,cy+.2,0],[x+.15,cy+.55,0],[x-.05,cy+.85,0],[x+.1,cy+1.15,0]]) for x in [-1,-.6,-.2]])
  charging.set_value(1);self.play(Create(heat),voltage.animate.set_value(1),run_time=1.2);charging.set_value(0);self.play(voltage.animate.set_value(0),heat.animate.shift(UP*.2).set_stroke(opacity=.4),run_time=1.2)
  self.note('충전·방전의 에너지 비용 · 누설 손실도 존재',ORANGE)

 def tradeoffs(self):
  grid=self.gate_grid(8);grid.scale(.74).move_to([0,1.7 if VERT else .55,0]);self.add(grid)
  labels=VGroup(pill('Area · 소자와 배선',3.5,.8,ORANGE,25),pill('Delay · 깊이와 부하',3.5,.8,ORANGE,25),pill('Energy · 전환과 누설',3.5,.8,ORANGE,25))
  if VERT:labels.arrange(DOWN,buff=.28).move_to([0,-1.4,0])
  else:labels.arrange(RIGHT,buff=.6).move_to([0,-1.2,0])
  self.play(FadeIn(labels),run_time=.8);self.note('Function + Area + Delay + Energy',INK)
  self.at(145);larger=self.gate_grid(16).scale(.74).move_to(grid)
  self.play(ReplacementTransform(grid,larger),Indicate(labels[0],color=ORANGE),run_time=1.1)
  self.play(Indicate(labels[1],color=ORANGE),run_time=.8);self.play(Indicate(labels[2],color=ORANGE),run_time=.8)
  self.note('소자 수만으로 지연·에너지 증가 비율을 정할 수는 없습니다')

 def arithmetic(self):
  n=self.nand(1,1);self.add(n);g=NandGlyph().scale(1.6).move_to([0,1.4 if VERT else .4,0])
  self.play(FadeOut(n),FadeIn(g),run_time=1)
  block=pill('논리 회로',w=3.3,h=1.7,color=INK,size=35).move_to(g)
  self.play(ReplacementTransform(g,block),run_time=1.2);self.note('스위치의 연결 → 논리 연산',INK)
  self.at(158);self.play(Transform(block,pill('연산 블록',w=3.0,h=2.2,color=INK,size=32).move_to(block)),run_time=.8)
  cy=block.get_center()[1]
  inputs=VGroup(pill('A',1,.7,BLUE).move_to([-3,cy+.55,0]),pill('B',1,.7,PURPLE).move_to([-3,cy-.55,0]))
  inw=VGroup(ln((-2.5,cy+.55),(-1.5,cy+.55),BLUE),ln((-2.5,cy-.55),(-1.5,cy-.55),PURPLE))
  self.play(FadeIn(inputs),Create(inw),run_time=.6);self.at(161)
  outputs=VGroup(pill('SUM  ?',2.0,.7,INK).move_to([3,cy+.55,0]),pill('CARRY  ?',2.0,.7,INK).move_to([3,cy-.55,0]))
  wires=VGroup(ln((1.5,cy+.55),(2,cy+.55),INK),ln((1.5,cy-.55),(2,cy-.55),INK))
  self.play(Create(wires),FadeIn(outputs),run_time=.7);self.note('논리 게이트 → 이진수 덧셈?',INK)
