"""Four-bit registers, input selection and non-destructive datapath reads."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_instruction import decode,alu,execute
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

class InstructionScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+1/config.frame_rate+.005:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  09',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
  self.notice=txt(' ',24);self.add(self.notice);self.note(' ')
  starts=[r['start'] for r in TIMING]
  def idx():
   now=self.start+self.time;i=bisect_right(starts,now+1e-7)-1
   return i if 0<=i<len(TIMING) and now<TIMING[i]['end']-1e-7 else -1
  def caption(i):
   s='\n'.join(textwrap.wrap(TIMING[i]['text'] if i>=0 else ' ',width=26 if VERT else 52))
   c=txt(s,30 if VERT else 29,INK,7.55 if VERT else 14.2)
   if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
   return c.move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(31)
  self.active_caption=idx();self.caption=caption(self.active_caption)
  def update(m):
   i=idx()
   if i!=self.active_caption:m.become(caption(i));m.set_z_index(31);self.active_caption=i
  self.caption.add_updater(update)
  panel=Rectangle(width=8.2 if VERT else 15,height=2.25 if VERT else 1.4,stroke_width=0,fill_color=config.background_color,fill_opacity=1).move_to(self.caption).set_z_index(29)
  self.add(panel,self.caption)
  x=3.9 if VERT else 7.3;y=-7.24 if VERT else -4.1;base=ln((-x,y),(x,y),EDGE,2);bar=base.copy().set_color(BLUE)
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/141)))
  self.add(base,bar,txt(f'{self.index+1:02} / 14',17,GRAY).move_to([x-.55,y+(.27 if VERT else -.2),0]).set_z_index(32))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)


COLORS=[ORANGE,GREEN,BLUE,PURPLE]
class InstructionBits(VGroup):
 def __init__(self,word=54):
  super().__init__();self.fields=VGroup();self.word=word
  for i,(name,value,c) in enumerate(zip(['OP','RD','RS1','RS2'],decode(word).values(),COLORS)):
   x=(i-1.5)*1.8;field=VGroup(pill(f'{value:02b}',1.6,.85,c,39).move_to([x,0,0]),txt(name,23,c).move_to([x,.85,0]));self.fields.add(field)
  self.add(self.fields);self.caption=txt('교육용 8-bit 형식',22,GRAY).move_to([0,-.85,0]);self.add(self.caption)
 def change(self,word):
  self.word=word
  for field,v,c in zip(self.fields,decode(word).values(),COLORS):setlabel(field[0][1],f'{v:02b}',c)

class DataPath(VGroup):
 def __init__(self):
  super().__init__();self.values=(0,5,3,0);self.word=54;self.readpaths=[];self.writepaths=[]
  self.regs=VGroup(*[pill(f'R{i} = {v}',1.9,.72,GREEN,27).move_to([-4,y,0]) for i,(v,y) in enumerate(zip(self.values,[1.9,.7,-.5,-1.7]))]);self.add(self.regs)
  self.muxes=VGroup()
  for j,cy in enumerate([1.1,-1.1]):
   box=pill('MUX '+('A' if j==0 else 'B'),1.5,1.45,BLUE if j==0 else PURPLE,26).move_to([-.8,cy,0]);self.muxes.add(box)
   for i,y in enumerate([1.9,.7,-.5,-1.7]):
    lane=-2.85+i*.3+j*.08;p=route((-3.05,y),(lane,y),(lane,cy+.48-i*.32),(-1.55,cy+.48-i*.32),c=GRAY,w=1.4);p.set_stroke(opacity=.4);self.add(p);self.readpaths.append(p)
  self.alu=pill('ALU',2,1.45,PURPLE,32).move_to([2.4,0,0]);self.result=txt('?',37,GREEN).move_to([4.2,0,0]);self.al=txt('A = ?',23,BLUE).move_to([.7,1.75,0]);self.bl=txt('B = ?',23,PURPLE).move_to([.7,-1.8,0]);self.op=txt('OP = ?',24,ORANGE).move_to([2.4,1.7,0])
  self.add(self.muxes,self.alu,self.result,self.al,self.bl,self.op,route((-.05,1.1),(.65,1.1),(.65,.4),(1.4,.4),c=BLUE),route((-.05,-1.1),(.85,-1.1),(.85,-.4),(1.4,-.4),c=PURPLE),ln((3.4,0),(3.8,0),GREEN))
  self.writer=pill('Write → R3',2.6,.7,ORANGE,25).move_to([-.2,-3,0]);self.wc=txt('WE = 0 · CLK',23,ORANGE).move_to([2.8,-3,0]);self.back=route((4.2,-.4),(4.8,-.4),(4.8,-2.4),(-.2,-2.4),(-.2,-2.65),c=GRAY)
  self.add(self.writer,self.wc,self.back)
  for i,y in enumerate([1.9,.7,-.5,-1.7]):
   x=-5.6-i*.15;p=route((-1.5,-3),(-2-i*.1,-3),(-2-i*.1,-3.4-i*.15),(x,-3.4-i*.15),(x,y),(-4.95,y),c=GRAY,w=1.4);p.set_stroke(opacity=.25);self.writepaths.append(p);self.add(p)
  self.selA=txt('A: --',22,BLUE).move_to([-.8,2.2,0]);self.selB=txt('B: --',22,PURPLE).move_to([-.8,-2.25,0]);self.add(self.selA,self.selB)
 def select(self,word=54,calculate=True):
  self.word=word;d=decode(word)
  for p in self.readpaths:p.set_stroke(GRAY,opacity=.25,width=1.4)
  self.readpaths[d['rs1']].set_stroke(BLUE,opacity=1,width=3);self.readpaths[4+d['rs2']].set_stroke(PURPLE,opacity=1,width=3)
  setlabel(self.selA,f'A: {d["rs1"]:02b}',BLUE);setlabel(self.selB,f'B: {d["rs2"]:02b}',PURPLE);setlabel(self.al,f'A = {self.values[d["rs1"]]}',BLUE);setlabel(self.bl,f'B = {self.values[d["rs2"]]}',PURPLE)
  setlabel(self.writer[1],f'Write → R{d["rd"]}',ORANGE)
  if calculate:self.calculate()
 def calculate(self):
  d=decode(self.word);setlabel(self.op,'OP = '+['ADD','SUB','AND','OR'][d['op']],ORANGE);_,v=execute(self.word,self.values,False);setlabel(self.result,str(v),GREEN)
 def save(self):
  self.values,v=execute(self.word,self.values);d=decode(self.word)
  for i,(r,value) in enumerate(zip(self.regs,self.values)):setlabel(r[1],f'R{i} = {value}',GREEN)
  self.writepaths[d['rd']].set_stroke(GREEN,opacity=1,width=3);self.back.set_stroke(GREEN,width=3);setlabel(self.wc,'WE = 1 · CLK ↑',ORANGE)
 def hold(self):setlabel(self.wc,'WE = 0 · CLK',ORANGE)

class Decoder(VGroup):
 def __init__(self):
  super().__init__();self.bits=InstructionBits().move_to([0,2,0]);self.block=pill('Instruction Decoder',4.5,1,ORANGE,31).move_to([0,.15,0]);self.outputs=VGroup();self.leads=VGroup()
  self.add(self.bits,self.block)
  for i,(s,c) in enumerate(zip(['ALU OP\n00 · ADD','Write RD\n11 · R3','Read A\n01 · R1','Read B\n10 · R2'],COLORS)):
   x=(i-1.5)*1.9;o=pill(s,1.7,1.1,c,23).move_to([x,-1.7,0]);self.outputs.add(o)
   self.leads.add(route((x,1.55),(x,.95),(x*.65,.95),(x*.65,.65),c=c),route((x*.65,-.35),(x*.65,-.9),(x,-.9),(x,-1.15),c=c))
  self.add(self.leads,self.outputs)

class ControlledPath(VGroup):
 def __init__(self):
  super().__init__();self.data=DataPath();self.bits=InstructionBits();self.decoder=pill('Decoder',2.3,.7,ORANGE,26);self.control=VGroup()
  if VERT:
   self.data.scale(.77).move_to([0,-1.5,0]);self.bits.move_to([0,3.8,0]);self.decoder.move_to([0,2.25,0]);self.add(ln((0,2.9),(0,2.6),ORANGE))
   destinations=[self.data.op,self.data.writer,self.data.selA,self.data.selB]
   for i,(target,c) in enumerate(zip(destinations,COLORS)):
    origin=np.array([(i-1.5)*.5,1.9,0]);end=target.get_top()+UP*.1;self.control.add(DashedLine(origin,end,color=c,stroke_width=1.5,dash_length=.08))
  else:
   self.data.scale(.67).move_to([2.15,-.2,0]);self.bits.scale(.75).move_to([-3.9,1.3,0]);self.decoder.move_to([-3.9,-.3,0]);self.add(ln((-3.9,.5),(-3.9,.05),ORANGE))
   for i,(target,c) in enumerate(zip([self.data.op,self.data.writer,self.data.selA,self.data.selB],COLORS)):
    self.control.add(DashedLine(self.decoder.get_right()+DOWN*(i-1.5)*.13,target.get_left()+LEFT*.06,color=c,stroke_width=1.5,dash_length=.07))
  self.add(self.control,self.data,self.bits,self.decoder)

# Section functions keep the same circuit object while values/control signals change.
def hook(self):
 d=self.centered(DataPath(),7.8 if VERT else 11);self.show(d);self.at(1);d.select();self.at(4);d.save();self.at(7);d.hold();self.note('읽기 주소 A · 읽기 주소 B · ALU 연산 · 쓰기 대상',ORANGE);self.at(13);self.note('여러 선택을 하나의 정보로 묶는다면?',ORANGE)
def choices(self):
 d=self.centered(DataPath(),7.8 if VERT else 11);self.show(d);self.note('R1 = 5  /  R2 = 3  /  R3 = 0',GREEN);self.at(22);self.note('목표: R3 ← R1 + R2');self.at(27);d.select(calculate=False);self.play(Indicate(d.regs[1],color=BLUE),Indicate(d.regs[2],color=PURPLE),run_time=.6);self.at(30);d.calculate();self.note('OP = ADD · 목적지 R3',ORANGE);self.at(33);d.save();self.play(Indicate(d.regs[3],color=GREEN),run_time=.5);self.at(36);d.hold();self.note('서로 다른 제어 입력으로 선택을 지정했습니다',ORANGE)
def encode_scene(self):
 g=VGroup(pill('숫자 5\n0101',2.6,1.8,GREEN,39).move_to([-2,0,0]),pill('동작 ADD\n??',2.6,1.8,ORANGE,39).move_to([2,0,0]));self.show(self.centered(g));self.at(43);setlabel(g[1][1],'동작 ADD\n00',ORANGE);self.note('숫자와 동작 모두 인코딩 규칙을 정할 수 있습니다')
def opcodes(self):
 g=VGroup(*[pill(s,2.3,1.3,ORANGE,34).move_to([(-1 if i%2==0 else 1)*1.5,(1 if i<2 else -1)*.95,0]) for i,s in enumerate(['00  ADD','01  SUB','10  AND','11  OR'])]);self.show(self.centered(g));self.note('이 영상에서 정한 예시 인코딩',ORANGE);self.at(49);self.play(Indicate(g[0],color=ORANGE),run_time=.5);self.at(51);self.play(Indicate(g[1],color=ORANGE),run_time=.5)
def registers(self):
 g=VGroup(*[pill(f'R{i}  ↔  {i:02b}',3.4,.8,[GRAY,BLUE,PURPLE,GREEN][i],32).move_to([0,1.5-i,0]) for i in range(4)]);self.show(self.centered(g));self.note('레지스터 번호 ≠ 레지스터에 저장된 데이터')
def fields(self):
 b=self.centered(InstructionBits(),7.6 if VERT else 11);self.show(b);self.note('OP  |  RD  |  RS1  |  RS2');self.at(59);self.play(LaggedStart(*[Indicate(f,color=c) for f,c in zip(b.fields,COLORS)],lag_ratio=.4),run_time=2);self.at(63);self.note('00110110  ·  하나의 명령어',ORANGE);self.play(Circumscribe(b,color=ORANGE),run_time=.7)
def meaning(self):
 b=InstructionBits().move_to([0,1.5,0]);g=VGroup(b,txt('00110110',35,ORANGE).move_to([0,-.1,0]),txt('ADD R3, R1, R2',38).move_to([0,-1.1,0]),txt('R3 ← R1 + R2',37,GREEN).move_to([0,-2.1,0]));self.show(self.centered(g,7.7 if VERT else 11));self.note('OP: ADD · RD: R3 · RS1: R1 · RS2: R2')
def roles(self):
 g=VGroup(pill('00110110',3.2,.9,ORANGE,35).move_to([-2.3,0,0]),pill('ALU',2,1.4,PURPLE,36).move_to([2.4,0,0]),txt('Data A / Data B / OP',25,GRAY).move_to([2.2,-1.4,0]),txt('?',45,ORANGE).move_to([.35,0,0]));self.show(self.centered(g));self.note('명령어 전체를 ALU 데이터 입력에 넣는 것이 아닙니다');self.at(78);dec=self.centered(Decoder(),7.7 if VERT else 11);self.replace(g,dec);self.note('필드의 위치와 역할을 회로로 연결해야 합니다')
def decoder(self):
 d=self.centered(Decoder(),7.7 if VERT else 11);self.show(d);self.note('해독도 미리 설계된 논리 회로의 동작입니다',ORANGE);self.at(86)
 for t,i in [(87,2),(89,3),(91,0),(93,1)]:
  self.at(t);self.play(Indicate(d.bits.fields[i],color=COLORS[i]),Indicate(d.outputs[i],color=COLORS[i]),run_time=.5)
 self.note('주소 필드는 선택선으로 전달 · OP는 ALU 제어로 해석')
def execute_scene(self):
 g=self.centered(ControlledPath(),7.85 if VERT else 14);self.show(g);self.note('00110110 → ADD R3, R1, R2',ORANGE);self.at(96);g.data.select(calculate=False);self.play(Indicate(g.data.muxes[0],color=BLUE),run_time=.5);self.at(98);self.play(Indicate(g.data.muxes[1],color=PURPLE),run_time=.5);self.at(100);g.data.calculate();self.play(Indicate(g.data.alu,color=PURPLE),run_time=.5);self.at(102);g.data.save();self.play(Indicate(g.data.regs[3],color=GREEN),run_time=.5);self.note('쓰기 대상 R3 + WE + CLK ↑ → R3 = 8',GREEN);self.at(104);g.data.hold()
def fixed(self):
 g=self.centered(ControlledPath(),7.85 if VERT else 14);g.data.select();g.data.save();g.data.hold();self.show(g);self.note('ADD → SUB · 배선과 블록 위치는 그대로');self.at(108);g.bits.change(118);g.data.select(118);self.play(Indicate(g.data.alu,color=ORANGE),run_time=.5);self.note('5 − 3 = 2 · WE = 0이므로 R3는 8 유지',ORANGE);self.at(111);self.note('ALU · MUX · 레지스터 = 이미 설계된 하드웨어');self.at(114);g.bits.change(54);g.data.select();self.note('선택 신호가 데이터와 연산 기능을 지정합니다',ORANGE)
def unified(self):
 g=self.centered(ControlledPath(),7.85 if VERT else 14);g.data.select();g.data.save();g.data.hold();self.show(g);self.note('하나의 명령어 → 여러 제어 신호',ORANGE);self.at(122);self.play(Indicate(g.bits,color=ORANGE),run_time=.6);self.at(124);self.play(Indicate(g.decoder,color=ORANGE),run_time=.6)
def next_scene(self):
 g=self.centered(VGroup(pill('명령어 입력\n00110110',4,1.4,ORANGE,35),txt('다음 입력: ?',29,GRAY).move_to([0,-1.5,0])));self.show(g);self.note('현재 만든 구조에는 자동으로 가져오는 기능이 없습니다');self.at(130)
 stack=VGroup(*[pill(s,5,.9,ORANGE if i==0 else GRAY,29).move_to([0,1.3-i*1.3,0]) for i,s in enumerate(['주소 0   00110110','주소 1   ????????','주소 2   ????????'])]);self.replace(g,self.centered(stack));self.note('나머지 칸은 아직 정하지 않은 자리 표시자입니다')
def closing(self):
 g=VGroup(*[pill(s,4,.8,c,29).move_to([0,1.8-i*1.2,0]) for i,(s,c) in enumerate([('명령어 00110110',ORANGE),('해독 → 제어 신호',ORANGE),('R1 + R2 → R3',GREEN)])]);self.show(self.centered(g));self.note('하나의 명령어로 계산과 저장을 지정합니다',ORANGE)
for n,f in [('hook',hook),('choices',choices),('encode',encode_scene),('opcodes',opcodes),('registers',registers),('fields',fields),('meaning',meaning),('roles',roles),('decoder',decoder),('execute',execute_scene),('fixed',fixed),('unified',unified),('next',next_scene),('closing',closing)]:setattr(InstructionScene,n,f)
