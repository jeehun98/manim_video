"""Voltage-controlled conduction, insulated-gate cross section, CMOS inversion."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
R=Path(__file__).resolve().parent
VERT=os.getenv('GPUI_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9
config.background_color='#0B1020'
INK='#F8FAFC';BLUE='#4299E1';GREEN='#34D399';GRAY='#64748B';PURPLE='#A78BFA';ORANGE='#F59E0B';EDGE='#28364C';PANEL='#131F33'
TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'))
MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def pill(s,w=2,h=.7,color=BLUE,size=26):
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.13,fill_color=PANEL,fill_opacity=1,stroke_color=color,stroke_width=1.4),txt(s,size,color,w-.22))
def label_update(mob,s,color):
 if getattr(mob,'_word',None)!=s:
  new=txt(s,26,color);new.scale_to_fit_height(mob.height);new.move_to(mob)
  mob.become(new);mob._word=s
 return mob
def line(a,b,color=GRAY,width=2.3):return Line(np.array([*a,0]),np.array([*b,0]),color=color,stroke_width=width)
def simple_mos(p=False):
 channel=line((0,-.52),(0,.52),GRAY,3)
 gate=line((-.42,-.42),(-.42,.42),PURPLE,2.5)
 wires=VGroup(line((0,.52),(.55,.52)),line((0,-.52),(.55,-.52)),line((-.95,0),(-.42,0),PURPLE))
 bubble=Circle(radius=.09,color=PURPLE,stroke_width=1.8).move_to([-.55,0,0]) if p else VGroup()
 return VGroup(channel,gate,wires,bubble)

class SwitchCircuit(VGroup):
 def __init__(self,controlled=False):
  super().__init__();self.state=ValueTracker(0)
  self.wires=VGroup(line((-2.7,1),(-.55,1)),line((.55,1),(2.7,1)),line((2.7,1),(2.7,.65)),line((2.7,-.25),(2.7,-1.5)),line((2.7,-1.5),(-2.7,-1.5)),line((-2.7,-1.5),(-2.7,-.65)),line((-2.7,.25),(-2.7,1)))
  self.contacts=VGroup(Dot([-.55,1,0],radius=.065,color=INK),Dot([.55,1,0],radius=.065,color=INK))
  self.lever=line((-.55,1),(.34,1.65),GRAY,3)
  def lever_update(m):
   a=self.contacts[0].get_center();b=self.contacts[1].get_center();theta=(1-self.state.get_value())*.62
   end=a+rotate_vector(b-a,theta);m.put_start_and_end_on(a,end).set_color(GREEN if self.state.get_value()>.85 else GRAY)
  self.lever.add_updater(lever_update)
  self.wires.add_updater(lambda m:m.set_color(GREEN if self.state.get_value()>.85 else BLUE).set_opacity(1 if self.state.get_value()>.85 else .5))
  source=VGroup(Circle(radius=.45,color=BLUE).move_to([-2.7,-.2,0]),txt('+',25,BLUE).move_to([-2.7,-.04,0]),txt('−',25,BLUE).move_to([-2.7,-.37,0]),txt('전원',21,GRAY).move_to([-2.7,-1,0]))
  self.bulb=Circle(radius=.45,color=GRAY,fill_color=GREEN,fill_opacity=0).move_to([2.7,.2,0])
  self.bulb.add_updater(lambda m:m.set_fill(GREEN,opacity=.45 if self.state.get_value()>.85 else 0).set_stroke(GREEN if self.state.get_value()>.85 else GRAY))
  cross=VGroup(line((2.43,-.07),(2.97,.47)),line((2.43,.47),(2.97,-.07)))
  self.add(self.wires,source,self.contacts,self.lever,self.bulb,cross)
  self.control=VGroup(line((0,-2.35),(0,-.05),PURPLE),DashedLine([0,-.05,0],[0,.65,0],color=PURPLE,dash_length=.10),pill('LOW',w=2.2,color=PURPLE).move_to([0,-2.7,0]))
  self.control[-1][1].add_updater(lambda m:label_update(m,'HIGH' if self.state.get_value()>.5 else 'LOW',PURPLE))
  if controlled:self.add(self.control)

class Section(VGroup):
 def __init__(self,names=False):
  super().__init__();self.state=ValueTracker(0)
  self.body=Rectangle(width=6.2,height=2.4,color=GRAY,fill_color='#1C2942',fill_opacity=1).move_to([0,-.4,0])
  self.source=Rectangle(width=1.2,height=.9,color=BLUE,fill_color=BLUE,fill_opacity=.23).move_to([-2.2,.35,0])
  self.drain=self.source.copy().move_to([2.2,.35,0])
  self.oxide=Rectangle(width=3.25,height=.28,color=INK,stroke_width=1.2,fill_color=GRAY,fill_opacity=.25).move_to([0,.94,0])
  self.gate=Rectangle(width=3.25,height=.4,color=PURPLE,fill_color=PURPLE,fill_opacity=.25).move_to([0,1.32,0])
  self.channel=Rectangle(width=3.3,height=.14,stroke_width=0,fill_color=GREEN,fill_opacity=0).move_to([0,.68,0])
  self.channel.add_updater(lambda m:m.set_fill(GREEN,opacity=.8*self.state.get_value()))
  self.terminals=VGroup(line((-2.2,.8),(-2.2,1.1),BLUE),line((-2.2,1.1),(-3.65,1.1),BLUE),line((2.2,.8),(2.2,1.1),BLUE),line((2.2,1.1),(3.65,1.1),BLUE),line((0,1.52),(0,2.08),PURPLE))
  self.fields=VGroup(*[Arrow([x,1.10,0],[x,.30,0],buff=0,stroke_width=1.4,tip_length=.11,color=ORANGE) for x in [-1,-.5,0,.5,1]])
  self.fields.add_updater(lambda m:m.set_opacity(.7*self.state.get_value()))
  self.charges=VGroup()
  for i in range(14):
   d=Dot(radius=.045,color=BLUE)
   def charge_update(m,j=i):
    region=self.source if j<7 else self.drain
    off=region.get_center()+RIGHT*((j%3-1)*region.width*.21)+UP*((j%2-.5)*region.height*.35)
    on=self.channel.get_left()+RIGHT*(self.channel.width*(j+.5)/14)
    m.move_to(interpolate(off,on,self.state.get_value()))
   d.add_updater(charge_update);self.charges.add(d)
  holes=VGroup(*[txt('+',17,ORANGE).move_to([x,y,0]) for x,y in [(-1.3,-.65),(-.3,-.95),(.8,-.55),(1.5,-1.0),(-2.3,-1.15)]])
  self.doping=VGroup(txt('n+',22,BLUE).move_to(self.source),txt('n+',22,BLUE).move_to(self.drain),txt('p-type body',21,GRAY).move_to([0,-1.35,0]))
  self.insulation=VGroup(txt('절연막',19,INK).move_to([3.72,.53,0]),line((3.2,.65),(1.64,.95),GRAY,1))
  self.names=VGroup(txt('Source',25,BLUE).move_to([-2.4,1.7,0]),txt('Drain',25,BLUE).move_to([2.4,1.7,0]),txt('Gate',25,PURPLE).move_to([0,2.37,0]))
  self.add(self.body,self.source,self.drain,self.channel,holes,self.charges,self.oxide,self.gate,self.fields,self.terminals,self.doping,self.insulation)
  if not names:self.names.set_opacity(0)
  self.add(self.names)

class CMOS(VGroup):
 def __init__(self,initial=0,names=True):
  super().__init__();self.input=ValueTracker(initial);self.output=ValueTracker(1-initial)
  self.p_path=VGroup(line((0,2.55),(0,1.95)),line((0,1.95),(0,1.05),GRAY,4),line((0,1.05),(0,0)))
  self.n_path=VGroup(line((0,0),(0,-1.05)),line((0,-1.05),(0,-1.95),GRAY,4),line((0,-1.95),(0,-2.55)))
  self.p_path.add_updater(lambda m:m.set_color(GREEN if self.input.get_value()<.5 else GRAY).set_opacity(1 if self.input.get_value()<.5 else .45))
  self.n_path.add_updater(lambda m:m.set_color(GREEN if self.input.get_value()>=.5 else GRAY).set_opacity(1 if self.input.get_value()>=.5 else .45))
  self.supply=VGroup(line((-.55,2.55),(.55,2.55),INK),txt('VDD',27,INK).move_to([0,2.95,0]))
  self.ground=VGroup(*[line((-w/2,-2.6-i*.14),(w/2,-2.6-i*.14),INK) for i,w in enumerate([1,.65,.3])],txt('GND',24,GRAY).move_to([0,-3.2,0]))
  self.gates=VGroup(line((-.38,1.05),(-.38,1.95),PURPLE),line((-.38,-1.95),(-.38,-1.05),PURPLE),Circle(radius=.095,color=PURPLE,fill_color=config.background_color,fill_opacity=1).move_to([-.56,1.5,0]),line((-1.25,1.5),(-.65,1.5),PURPLE),line((-1.25,-1.5),(-.38,-1.5),PURPLE),line((-1.25,-1.5),(-1.25,1.5),PURPLE),line((-2.1,0),(-1.25,0),PURPLE))
  self.in_card=pill('LOW / 0' if not initial else 'HIGH / 1',w=1.75,h=.75,color=PURPLE,size=23).move_to([-3.0,0,0])
  self.in_card[1]._word='LOW / 0' if not initial else 'HIGH / 1'
  self.in_card[1].add_updater(lambda m:label_update(m,'LOW / 0' if self.input.get_value()<.5 else 'HIGH / 1',PURPLE))
  self.node=Dot([0,0,0],radius=.095,color=GREEN if not initial else BLUE)
  self.node.add_updater(lambda m:m.set_color(interpolate_color(ManimColor(BLUE),ManimColor(GREEN),self.output.get_value())))
  self.out_wire=line((0,0),(1.9,0),GREEN)
  self.out_wire.add_updater(lambda m:m.set_color(interpolate_color(ManimColor(BLUE),ManimColor(GREEN),self.output.get_value())))
  self.out_card=pill('HIGH / 1' if not initial else 'LOW / 0',w=1.75,h=.75,color=GREEN if not initial else BLUE,size=23).move_to([2.85,0,0])
  self.out_card[1]._word='HIGH / 1' if not initial else 'LOW / 0'
  def output_label(m):
   v=self.output.get_value();label_update(m,'LOW / 0' if v<.15 else 'HIGH / 1' if v>.85 else '전환 중',BLUE if v<.15 else GREEN if v>.85 else ORANGE)
  self.out_card[1].add_updater(output_label)
  self.labels=VGroup(txt('INPUT',20,PURPLE).move_to([-3,.65,0]),txt('OUTPUT',20,GRAY).move_to([2.85,.65,0]))
  self.names=VGroup(txt('pMOS',25,INK).move_to([1.1,1.5,0]),txt('nMOS',25,INK).move_to([1.1,-1.5,0]))
  self.add(self.supply,self.ground,self.p_path,self.n_path,self.gates,self.in_card,self.node,self.out_wire,self.out_card,self.labels)
  if names:self.add(self.names)

class TransistorScene(Scene):
 index=0
 def at(self,t):
  local=t-self.start
  if self.time>local+.04:raise RuntimeError(f'Scene {self.index+1}: overrun {self.time}>{local}')
  if local-self.time>.001:self.wait(local-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  # Wait segments must still update the scene clock, captions and circuit states.
  self.always_update_mobjects=True
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  02',21,GRAY).move_to([0,top,0]),txt(m['title'],37 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
  self.notice=txt(' ',24);self.add(self.notice);self.note(' ')
  starts=[r['start'] for r in TIMING]
  def idx():
   now=self.start+self.time;i=bisect_right(starts,now+1e-7)-1
   return i if 0<=i<len(TIMING) and now<TIMING[i]['end']-1e-7 else -1
  def caption(i):
   s='\n'.join(textwrap.wrap(TIMING[i]['text'] if i>=0 else ' ',width=26 if VERT else 52))
   return txt(s,30 if VERT else 29,INK,7.55 if VERT else 14.2).move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(31)
  self.active_caption=idx();self.caption=caption(self.active_caption)
  def update_caption(mob):
   i=idx()
   if i!=self.active_caption:mob.become(caption(i));mob.set_z_index(31);self.active_caption=i
  self.caption.add_updater(update_caption)
  panel=Rectangle(width=8.2 if VERT else 15,height=2.25 if VERT else 1.4,stroke_width=0,fill_color=config.background_color,fill_opacity=1).move_to(self.caption).set_z_index(29)
  self.add(panel,self.caption)
  y=-7.24 if VERT else -4.1;x=3.9 if VERT else 7.3
  base=line((-x,y),(x,y),EDGE,2);progress=base.copy().set_color(BLUE)
  progress.add_updater(lambda o:o.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/142)))
  self.add(base,progress,txt(f'{self.index+1:02} / 10',17,GRAY).move_to([x-.55,y+.27,0]))
  [self.need,self.manual,self.control,self.field,self.electronic,self.mosfet,self.output,self.inverter,self.physical,self.networks][self.index]()
  self.at(self.end)
 def circuit(self,controlled=False):
  c=SwitchCircuit(controlled)
  if controlled and not VERT:c.scale(.75).shift(UP*.8)
  else:c.shift(UP*(1.2 if VERT else .3))
  c.update(0);return c
 def section(self,names=False):return Section(names).scale(.91 if VERT else .88).move_to([0,1.5 if VERT else .35,0])
 def cmos(self,initial=0,names=True):
  c=CMOS(initial,names).scale(.9 if VERT else .66).move_to([0,1.25 if VERT else .25,0]);c.update(0);return c
 def invert(self,c,high):
  self.play(c.input.animate.set_value(high),run_time=.25);self.wait(.12)
  self.play(c.output.animate.set_value(1-high),run_time=.48)

 def need(self):
  low=pill('LOW  /  0',2.6,1,BLUE,34);high=pill('HIGH  /  1',2.6,1,GREEN,34)
  pair=VGroup(low,high).arrange(DOWN,buff=.6).move_to([0,1.5 if VERT else .5,0])
  self.play(FadeIn(pair),run_time=1);self.at(5)
  box=VGroup(RoundedRectangle(width=2.6,height=2,corner_radius=.18,color=GRAY,fill_color=PANEL,fill_opacity=1),txt('?',66))
  if VERT:
   self.play(pair.animate.scale(.7).move_to([-2.5,1.5,0]),run_time=.7);box.move_to([.7,1.5,0])
  else:
   self.play(pair.animate.scale(.8).move_to([-4.4,.5,0]),run_time=.7);box.move_to([0,.5,0])
  a=Arrow(pair.get_right(),box.get_left(),color=PURPLE,buff=.2)
  out=line((box.get_right()[0]+.12,box.get_center()[1]),(3.5 if VERT else 5.5,box.get_center()[1]),GRAY)
  self.play(FadeIn(box),GrowArrow(a),Create(out),run_time=1)
  self.note('INPUT  →  ?  →  OUTPUT')
  self.at(11)
  for target in [high,low,high]:self.play(Indicate(target,color=PURPLE),run_time=.8)
  self.note('입력에 반응하는 장치가 필요합니다',INK)

 def manual(self):
  c=self.circuit();self.play(FadeIn(c),run_time=1.2)
  self.note('전원 · 스위치 · 부하 · 돌아오는 경로')
  self.at(20);self.play(Indicate(c.contacts,scale_factor=1.5,color=INK),run_time=.8)
  self.at(22);self.play(c.state.animate.set_value(1),run_time=.7);self.note('연결 → 전류가 흐를 수 있는 닫힌 회로',GREEN)
  self.at(25);self.play(c.state.animate.set_value(0),run_time=.7);self.note('차단 → 열린 회로')

 def control(self):
  c=self.circuit(True);self.add(c);self.note('보라색: 제어 입력  /  파란색: 별도 전류 경로')
  self.play(Create(c.control[0]),FadeIn(c.control[1:]),run_time=1.4)
  self.at(33);self.play(c.state.animate.set_value(1),run_time=.7);self.wait(1)
  self.play(c.state.animate.set_value(0),run_time=.7);self.wait(.6);self.play(c.state.animate.set_value(1),run_time=.7)
  self.at(38)
  self.note('CONTROL SIGNAL ≠ CURRENT PATH',PURPLE)
  self.play(Indicate(c.control,color=PURPLE),run_time=1)

 def field(self):
  c=self.circuit();c.scale(.7);self.add(c);self.note('움직이는 접점 없이 가능할까?')
  self.play(c.state.animate.set_value(1),run_time=.7);self.play(c.state.animate.set_value(0),run_time=.7)
  self.at(47);s=self.section();self.play(FadeOut(c),FadeIn(s.body),run_time=.8)
  self.play(FadeIn(s.source),FadeIn(s.drain),FadeIn(s.charges),FadeIn(s.doping),run_time=.8)
  self.at(50)
  self.play(FadeIn(s.oxide),FadeIn(s.gate),FadeIn(s.fields),FadeIn(s.insulation),run_time=.9)
  self.add(s.channel)
  self.play(s.state.animate.set_value(.85),run_time=2.4)
  self.note('전기장 → 전하 분포 변화',ORANGE)
  self.at(55);self.add(s.terminals)
  self.play(s.state.animate.set_value(1),run_time=.8);self.note('표면 근처에 전도 채널 형성',GREEN)
  self.wait(1);self.play(s.state.animate.set_value(0),run_time=1.1);self.wait(.5);self.play(s.state.animate.set_value(1),run_time=1.1)

 def electronic(self):
  left=SwitchCircuit();right=Section()
  if VERT:left.scale(.61).move_to([0,3.3,0]);right.scale(.70).move_to([0,-.6,0])
  else:left.scale(.73).move_to([-4,.35,0]);right.scale(.73).move_to([3.65,.35,0])
  labels=VGroup(txt('기계식 접점',25,GRAY).next_to(left,UP,buff=.2),txt('전하 분포·전도성',25,PURPLE).next_to(right,UP,buff=.2))
  self.add(left,right,labels)
  self.play(left.state.animate.set_value(1),right.state.animate.set_value(1),run_time=.9)
  self.play(left.state.animate.set_value(0),right.state.animate.set_value(0),run_time=.9)
  self.at(65)
  self.play(FadeOut(left),FadeOut(labels),right.animate.scale(1.3).move_to([0,1.5 if VERT else .4,0]),run_time=1.2)
  self.play(right.state.animate.set_value(1),run_time=.8);self.note('기계적 이동 → 전기적 제어',PURPLE)

 def mosfet(self):
  s=self.section();s.state.set_value(1);self.add(s)
  title=pill('MOSFET',w=3.5,h=.8,color=INK,size=36).move_to([0 if VERT else -5,4.8 if VERT else 2.4,0]);self.play(FadeIn(title),run_time=.8)
  self.note('n채널 강화형 · 설명용 단면')
  self.at(73)
  # Names inherit the same transform as the section; do not replace them with floating labels.
  for n in s.names:n.set_opacity(1)
  self.play(LaggedStart(*[FadeIn(n) for n in s.names],lag_ratio=.5),run_time=2)
  self.at(79)
  status=pill('VGS  HIGH',w=2.8,color=PURPLE,size=26).move_to(title)
  low=pill('VGS  LOW',w=2.8,color=PURPLE,size=26).move_to(title)
  self.play(Transform(title,low),s.state.animate.set_value(0),run_time=.7)
  self.note('VGS: Source 기준 Gate 전압 · VDS > 0 가정')
  self.play(s.state.animate.set_value(1),Transform(title,status.copy()),run_time=1.2);self.wait(.5)
  self.play(s.state.animate.set_value(0),Transform(title,pill('VGS  LOW',2.8,color=PURPLE).move_to(title)),run_time=1.2)
  self.wait(.4);self.play(s.state.animate.set_value(1),Transform(title,status.copy()),run_time=1.2)
  self.at(87)
  symbol=simple_mos().scale(2.0).move_to([0,1.1 if VERT else .4,0])
  labels=VGroup(txt('Gate',27,PURPLE).next_to(symbol,LEFT,buff=.4),txt('Drain',27,BLUE).next_to(symbol,UP,buff=.3),txt('Source',27,BLUE).next_to(symbol,DOWN,buff=.3))
  self.play(FadeOut(s),FadeIn(symbol),FadeIn(labels),run_time=1.3)
  self.note('절연된 제어 단자와 별도의 전도 경로')

 def output(self):
  c=self.cmos(0,False)
  self.add(c.node,c.out_wire,c.labels[1])
  self.note('출력은 별도의 노드 전압입니다')
  self.at(95);self.play(FadeIn(c.supply),FadeIn(c.p_path),FadeIn(c.out_card),run_time=1.2)
  self.note('VDD에 연결 → HIGH',GREEN)
  self.at(100);c.input.set_value(1)
  self.play(FadeIn(c.ground),FadeIn(c.n_path),c.output.animate.set_value(0),run_time=1.2)
  self.note('GND에 연결 → LOW',BLUE)
  self.at(104);c.in_card.update(0)
  self.play(FadeIn(c.gates),FadeIn(c.in_card),FadeIn(c.labels[0]),run_time=.9)
  self.invert(c,0);self.note('공통 입력이 두 경로의 전도 상태를 선택',PURPLE)

 def truth(self):
  return VGroup(txt('INPUT       OUTPUT',25,GRAY),txt('0       →       1',34,GREEN),txt('1       →       0',34,BLUE)).arrange(DOWN,buff=.35)
 def inverter(self):
  c=self.cmos(0);self.add(c);self.note('입력 LOW · pMOS ON / nMOS OFF',GREEN)
  self.at(113);self.invert(c,1);self.note('입력 HIGH · pMOS OFF / nMOS ON',BLUE)
  self.at(116);table=self.truth()
  if VERT:
   self.play(c.animate.scale(.72).move_to([0,2.2,0]),run_time=.6);table.scale(.75).move_to([0,-1.55,0])
  else:
   self.play(c.animate.move_to([-3.8,.3,0]),run_time=.6);table.move_to([3.6,.25,0])
  self.play(FadeIn(table),run_time=.7)
  self.at(119);self.note('NOT / INVERTER',INK)

 def physical(self):
  c=self.cmos(1);self.add(c);self.note('별도 프로그램 없이 연결 구조가 동작을 결정',INK)
  self.at(123)
  for v in [0,1,0]:self.invert(c,v);self.wait(.6)
  self.note('출력 전압의 상승·하강에는 지연이 있습니다')
  self.at(130)
  labels=['INPUT SIGNAL','PHYSICAL CIRCUIT','OUTPUT SIGNAL']
  cards=VGroup(*[pill(s,w=3.35 if VERT else 3.8,h=.85,color=PURPLE if i==0 else GREEN if i==2 else INK,size=24) for i,s in enumerate(labels)])
  cards.arrange(DOWN if VERT else RIGHT,buff=.65 if VERT else 1).move_to([0,2.0 if VERT else 1.05,0])
  arrows=VGroup(*[Arrow(cards[i].get_bottom() if VERT else cards[i].get_right(),cards[i+1].get_top() if VERT else cards[i+1].get_left(),buff=.12,color=GRAY) for i in range(2)])
  table=self.truth().scale(.8).move_to([0,-1.5 if VERT else -.8,0])
  self.play(FadeOut(c),FadeIn(cards),FadeIn(arrows),FadeIn(table),run_time=1.2)
  self.note('연결 구조가 입력과 출력의 관계를 만듭니다',INK)

 def networks(self):
  old=VGroup(simple_mos().move_to([0,1.2 if VERT else .5,0]));self.add(old)
  for n in [2,4,8]:
   new=VGroup(*[simple_mos().scale(.85 if VERT else 1) for _ in range(n)])
   new.arrange_in_grid(rows=2 if n>=4 else 1,cols=n//2 if n>=4 else n,buff=(.65,.65)).move_to([0,1.3 if VERT else .6,0])
   self.play(*[TransformFromCopy(old[min(j//2,len(old)-1)],new[j]) for j in range(n)],run_time=.65)
   self.remove(old,*list(old));self.add(new);old=new
  self.at(139)
  links=VGroup()
  for i in range(3):
   links.add(Line(old[i].get_right(),old[i+1].get_left(),color=BLUE,stroke_width=1.6),Line(old[i+4].get_right(),old[i+5].get_left(),color=BLUE,stroke_width=1.6))
  links.add(Line(old[0].get_left(),old[4].get_left(),color=BLUE,stroke_width=1.6),Line(old[3].get_right(),old[7].get_right(),color=BLUE,stroke_width=1.6))
  self.play(Create(links),run_time=.9)
  q=txt('?',68,INK).move_to([0,-1.4 if VERT else -1,0]);self.play(FadeIn(q),old.animate.set_opacity(.45),links.animate.set_opacity(.35),run_time=.7)
  self.note('스위치의 연결이 계산 규칙이 된다.',INK)
