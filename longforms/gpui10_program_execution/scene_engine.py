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

class ProgramScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+1/config.frame_rate+.005:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  10',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/165)))
  self.add(base,bar,txt(f'{self.index+1:02} / 15',17,GRAY).move_to([x-.55,y+(.27 if VERT else -.2),0]).set_z_index(32))
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
  setlabel(self.op,'OP = '+['ADD','SUB','AND','OR'][d['op']],ORANGE)
  if calculate:self.calculate()
 def calculate(self):
  d=decode(self.word);setlabel(self.op,'OP = '+['ADD','SUB','AND','OR'][d['op']],ORANGE);_,v=execute(self.word,self.values,False);setlabel(self.result,str(v),GREEN)
 def save(self):
  self.values,v=execute(self.word,self.values);d=decode(self.word)
  for i,(r,value) in enumerate(zip(self.regs,self.values)):setlabel(r[1],f'R{i} = {value}',GREEN)
  self.writepaths[d['rd']].set_stroke(GREEN,opacity=1,width=3);self.back.set_stroke(GREEN,width=3);setlabel(self.wc,'WE = 1 · CLK ↑',ORANGE)
 def hold(self):setlabel(self.wc,'WE = 0 · CLK',ORANGE)


from check_program import MEMORY,next_pc,commit_pc
class InstructionMemory(VGroup):
 def __init__(self,branch=False):
  super().__init__();self.branch=branch;self.rows=VGroup();self.selected=None
  content=['ADD R3,R1,R2\n00110110','SUB R3,R3,R1\n01111101','미정 · —'] if not branch else ['이전 명령어','조건 분기 · 예시','다음 명령어','목표 명령어']
  ys=[1.1,0,-1.1] if not branch else [1.5,.5,-.5,-1.5]
  for i,(s,y) in enumerate(zip(content,ys)):
   row=pill(f'{i}   {s}',4.6,.95,GRAY,25).move_to([0,y,0]);self.rows.add(row)
  self.box=RoundedRectangle(width=5.1,height=4.8 if branch else 4.2,corner_radius=.14,stroke_color=BLUE,stroke_width=1.7)
  self.add(self.box,self.rows,txt('Instruction Memory',27,BLUE).move_to([0,2.85 if branch else 2.5,0]))
 def select(self,index):
  self.selected=index
  for i,r in enumerate(self.rows):r[0].set_stroke(BLUE if i==index else GRAY,width=2.7 if i==index else 1);r[1].set_color(BLUE if i==index else GRAY)

class ProgramCounter(VGroup):
 def __init__(self,value=0):
  super().__init__();self.value=value;self.box=pill(f'PC\n{value}',1.6,1.4,GREEN,38);self.d=Dot([-1.15,0,0],radius=.035,color=GREEN);self.q=Dot([1.15,0,0],radius=.035,color=GREEN)
  self.add(self.box,self.d,self.q,ln((-1.15,0),(-.8,0),GREEN),ln((.8,0),(1.15,0),GREEN),txt('D',20,GRAY).move_to([-1.15,.4,0]),txt('Q',20,GRAY).move_to([1.15,.4,0]))
  self.clk=txt('CLK ↑',23,ORANGE).move_to([0,-1.3,0]);self.add(self.clk,ln((0,-.7),(0,-1),ORANGE))
 def store(self,value):self.value=value;setlabel(self.box[1],f'PC\n{value}',GREEN)

class FetchCircuit(VGroup):
 def __init__(self,pc=0):
  super().__init__();self.pc=ProgramCounter(pc).move_to([-3.7,.45,0]);self.mem=InstructionMemory().move_to([1.1,.45,0]);self.mem.select(pc)
  self.addr=Line(self.pc.q.get_center(),self.mem.box.get_left(),color=GREEN,stroke_width=3)
  self.inc=pill(f'PC + 1 = {pc+1}',2.7,.7,ORANGE,25).move_to([-3.4,-2.8,0]);self.out=pill(f'{MEMORY[pc]:08b}',3.2,.7,BLUE,32).move_to([1.1,-2.8,0]);self.add(self.pc,self.mem,self.addr,self.inc,self.out)
  q=self.pc.q.get_center();d=self.pc.d.get_center()
  self.add(route((q[0],q[1]),(-2.25,q[1]),(-2.25,-2.8),(-2.05,-2.8),c=ORANGE),route((-4.75,-2.8),(-5.2,-2.8),(-5.2,d[1]),(d[0],d[1]),c=ORANGE),Line(self.mem.box.get_bottom(),self.out.get_top(),color=BLUE),txt('Address',21,GREEN).move_to([-1.8,1.1,0]))
 def advance(self):
  n=next_pc(self.pc.value,0,False);self.pc.store(n);self.mem.select(n);setlabel(self.inc[1],f'PC + 1 = {n+1}',ORANGE);setlabel(self.out[1],f'{MEMORY[n]:08b}',BLUE)

class Processor(VGroup):
 def __init__(self,pc=0,regs=(0,5,3,0)):
  super().__init__();self.pc=ProgramCounter(pc);self.mem=InstructionMemory();self.data=DataPath();self.data.values=regs
  for r,i,v in zip(self.data.regs,range(4),regs):setlabel(r[1],f'R{i} = {v}',GREEN)
  self.decoder=pill('Decoder\n????????',2.7,1.2,PURPLE,27);self.word=MEMORY[pc];self.controls=VGroup()
  if VERT:
   self.mem.scale(.78).move_to([1,3.1,0]);self.pc.scale(.78).move_to([-2.8,3.15,0]);self.decoder.move_to([.8,.55,0]);self.data.scale(.65).move_to([0,-2.25,0]);self.inc=pill('PC + 1',1.8,.65,ORANGE,24).move_to([-2.8,.75,0])
   self.fetchwire=Line(self.mem.box.get_bottom(),self.decoder.get_top(),color=GRAY,stroke_width=2)
  else:
   self.mem.scale(.76).move_to([-2.2,.6,0]);self.pc.scale(.76).move_to([-5.8,.8,0]);self.decoder.move_to([2.7,2.1,0]);self.data.scale(.61).move_to([3.5,-.65,0]);self.inc=pill('PC + 1',1.7,.65,ORANGE,24).move_to([-5.8,-1.6,0])
   self.fetchwire=VMobject(color=GRAY,stroke_width=2).set_points_as_corners([self.mem.box.get_right(),np.array([.45,self.mem.box.get_right()[1],0]),np.array([.45,2.1,0]),self.decoder.get_left()])
  self.addrwire=Line(self.pc.q.get_center(),self.mem.box.get_left(),color=GREEN,stroke_width=2.5)
  q=self.pc.q.get_center();d=self.pc.d.get_center();incR=self.inc.get_right();incL=self.inc.get_left();outer=d[0]-.25
  self.feedback=VGroup(route((q[0],q[1]),(q[0]+.15,q[1]),(q[0]+.15,incR[1]),(incR[0],incR[1]),c=ORANGE),route((incL[0],incL[1]),(outer,incL[1]),(outer,d[1]),(d[0],d[1]),c=ORANGE))
  for i,(target,c) in enumerate(zip([self.data.selA,self.data.selB,self.data.op,self.data.writer],[BLUE,PURPLE,ORANGE,GREEN])):
   self.controls.add(DashedLine(self.decoder.get_bottom()+RIGHT*(i-1.5)*.23,target.get_top(),color=c,stroke_width=1.3,dash_length=.08))
  self.add(self.mem,self.pc,self.inc,self.feedback,self.addrwire,self.fetchwire,self.controls,self.decoder,self.data)
 def fetch(self):
  self.word=MEMORY[self.pc.value];self.mem.select(self.pc.value);setlabel(self.decoder[1],f'Decoder\n{self.word:08b}',PURPLE);self.fetchwire.set_stroke(BLUE,width=3)
 def decode(self):self.data.select(self.word,calculate=False)
 def calculate(self):self.data.calculate()
 def save(self):self.data.save()
 def advance(self):self.pc.store(self.pc.value+1);self.mem.select(self.pc.value);self.data.hold()

class BranchCircuit(VGroup):
 def __init__(self):
  super().__init__();self.pc=ProgramCounter(1).move_to([3.4,.3,0]);self.taken=False
  self.seq=pill('PC + 1 = 2',2.8,.9,GREEN,28).move_to([-3,1.4,0]);self.target=pill('Target = 3',2.8,.9,ORANGE,28).move_to([-3,-.65,0])
  self.mux=Polygon([-.8,2,0],[-.8,-1.25,0],[.65,-.8,0],[.65,1.55,0],stroke_color=ORANGE,fill_color=PANEL,fill_opacity=1)
  self.paths=[route((-1.6,1.4),(-.8,1.4)),route((-1.6,-.65),(-.8,-.65))];self.selectlabel=txt('Taken = 0',25,ORANGE).move_to([0,-1.9,0]);self.dlabel=txt('D = 2',25,GREEN).move_to([1.45,1.2,0]);self.condition=txt('조건값 = 1  →  0이 아님',25,ORANGE).move_to([-1,2.8,0])
  self.slots=VGroup(*[pill(str(i),1.25,.75,GRAY,30).move_to([(i-1.5)*1.8,-3,0]) for i in range(4)]);self.slots[1][0].set_stroke(BLUE,width=3)
  self.add(self.pc,self.seq,self.target,self.mux,txt('MUX',29).move_to([-.2,.4,0]),*self.paths,self.selectlabel,self.dlabel,self.condition,self.slots,txt('명령어 메모리 주소 · 내용은 유지',23,BLUE).move_to([0,-3.9,0]),Line([.65,.3,0],self.pc.d.get_center(),color=GREEN,stroke_width=3),ln((0,-1.6),(0,-1),ORANGE))
  self.select(False)
 def select(self,taken):
  self.taken=taken
  for i,p in enumerate(self.paths):p.set_stroke(GREEN if i==int(taken) else GRAY,opacity=1 if i==int(taken) else .3,width=3)
  setlabel(self.selectlabel,f'Taken = {int(taken)}',ORANGE);setlabel(self.dlabel,f'D = {next_pc(1,3,taken)}',GREEN);setlabel(self.condition,'조건값 = 0  →  분기 참' if taken else '조건값 = 1  →  분기 거짓',ORANGE)
 def clock(self):
  value=commit_pc(1,next_pc(1,3,self.taken),True,True);self.pc.store(value)
  for i,s in enumerate(self.slots):s[0].set_stroke(BLUE if i==value else GRAY,width=3 if i==value else 1)

def hook(self):
 d=self.centered(DataPath(),7.8 if VERT else 11);self.show(d);d.select();self.note('00110110 → 해독 → ADD R3,R1,R2',ORANGE);self.at(6);d.save();self.play(Indicate(d.regs[3],color=GREEN),run_time=.5);self.at(10)
 m=self.centered(InstructionMemory(),6.5 if VERT else 8);self.replace(d,m);self.note('프로그램에는 여러 명령어가 있습니다');self.at(14);self.note('다음에 가져올 명령어의 위치는?',ORANGE)
def memory(self):
 m=self.centered(InstructionMemory(),6.7 if VERT else 8.5);self.show(m);self.note('명령어도 저장 가능한 비트 정보',BLUE);self.at(22);self.play(Indicate(m.rows[0],color=BLUE),run_time=.5);self.at(27);m.select(0);self.note('주소 0: ADD  /  주소 1: SUB');self.at(30);m.select(1);self.play(Indicate(m.rows[1],color=BLUE),run_time=.6)
def address(self):
 m=InstructionMemory();g=VGroup(m,txt('Address = ?',32,ORANGE).move_to([-4,0,0]),ln((-2.8,0),(-2.55,0),ORANGE));self.show(self.centered(g,7.8 if VERT else 11));self.note('저장은 했지만, 읽을 위치를 지정해야 합니다');self.at(37);self.play(Indicate(m.rows,color=BLUE),run_time=.5);self.at(40);self.note('메모리의 주소 입력에 무엇을 연결할까?',ORANGE)
def pc_scene(self):
 p=self.centered(ProgramCounter(8),3.3);self.show(p);self.note('이미 알고 있는 저장 회로를 활용합니다');self.at(47);p.store(0);self.note('저장값의 역할: 계산 결과 → 명령어 주소',GREEN);self.at(51);f=self.centered(FetchCircuit(0),7.8 if VERT else 11.5);self.replace(p,f);self.note('Program Counter · PC = 인출할 주소',GREEN)
def fetch_scene(self):
 f=self.centered(FetchCircuit(0),7.8 if VERT else 11.5);self.show(f);self.note('가상 명령어 슬롯 주소 · 명령어 1개당 +1');self.at(59);self.play(Indicate(f.pc.box,color=GREEN),Indicate(f.mem.rows[0],color=BLUE),run_time=.7);self.at(61);self.play(Indicate(f.out,color=BLUE),run_time=.5)
def decode_execute(self):
 p=self.centered(Processor(),7.85 if VERT else 14);self.show(p);p.fetch();self.note('주소 0 → 00110110 → Decoder',BLUE);self.at(66);p.decode();self.note('OP 00 · RD 11 · RS1 01 · RS2 10',ORANGE);self.at(69);self.play(Indicate(p.data.muxes,color=BLUE),run_time=.6);self.at(72);p.calculate();self.play(Indicate(p.data.alu,color=PURPLE),run_time=.5);self.at(74);p.save();self.play(Indicate(p.data.regs[3],color=GREEN),run_time=.5);self.note('5 + 3 = 8 · 유효한 쓰기 에지에서 R3 갱신',GREEN)
def advance(self):
 f=self.centered(FetchCircuit(0),7.8 if VERT else 11.5);self.show(f);self.note('R3 = 8 유지 · PC는 아직 0');self.at(80);self.note('D에 다음 주소 1 제공 → CLK ↑ → PC = 1',ORANGE);self.play(Indicate(f.inc,color=ORANGE),run_time=.6);self.at(83);f.advance();self.play(Indicate(f.pc.box,color=GREEN),Indicate(f.mem.rows[1],color=BLUE),run_time=.6)
def stages(self):
 p=self.centered(Processor(1,(0,5,3,8)),7.85 if VERT else 14);self.show(p);self.note('① 인출: PC = 1 → 01111101',BLUE);p.fetch();self.at(87);p.decode();self.note('② 해독: SUB R3,R3,R1',PURPLE);self.at(88.5);p.calculate();self.note('③ 실행: 8 − 5 = 3',GREEN);self.play(Indicate(p.data.alu,color=PURPLE),run_time=.5);self.at(90);p.save();p.data.hold()
 # At completion, stop displaying sampled operands as live register outputs.
 for path in p.data.readpaths:path.set_stroke(GRAY,opacity=.25,width=1.4)
 for label,value in [(p.data.al,'A: 완료'),(p.data.bl,'B: 완료'),(p.data.result,'완료'),(p.data.selA,'A: 대기'),(p.data.selB,'B: 대기')]:setlabel(label,value,GRAY)
 setlabel(p.data.op,'연산 완료',GRAY);p.fetchwire.set_stroke(GRAY,width=2);p.controls.set_stroke(opacity=.25);self.note('③ 실행 완료 · R3 = 3에 기록',GREEN);self.play(Indicate(p.data.regs[3],color=GREEN),run_time=.5);self.at(91);p.advance();setlabel(p.decoder[1],'Decoder\n실행 완료',GRAY);self.note('Fetch → Decode → Execute · 다음 PC = 2')

def condition(self):
 m=self.centered(InstructionMemory(branch=True),6 if VERT else 7.5);m.select(1);self.show(m);self.note('별도의 분기 예시 · 현재 PC = 1');self.at(98);self.note('조건값이 0이면 주소 2를 건너뛰고 싶다면?',ORANGE);self.at(101);self.play(Indicate(m.rows[3],color=ORANGE),run_time=.6);self.at(103);g=VGroup(pill('순차 후보\nPC + 1 = 2',3,1.4,GREEN,34).move_to([-1.8,0,0]),pill('분기 후보\nTarget = 3',3,1.4,ORANGE,34).move_to([1.8,0,0]));self.replace(m,self.centered(g,7.6 if VERT else 10));self.note('条件과 목표 주소가 결정된 뒤의 선택을 살펴봅니다'.replace('条件','조건'))
def branch(self):
 b=self.centered(BranchCircuit(),7.8 if VERT else 11);self.show(b);self.note('분기 예시 · 후보 배선은 고정되어 있습니다');self.at(109);self.play(Indicate(b.paths[0],color=GREEN),run_time=.6);self.at(111);b.select(True);self.play(Indicate(b.paths[1],color=ORANGE),run_time=.6);self.at(114);self.note('다음 PC = 3 선택 · 아직 PC에는 1 저장',ORANGE);self.at(116);b.clock();self.play(Indicate(b.pc.box,color=GREEN),Indicate(b.slots[3],color=BLUE),run_time=.7);self.note('조건 → 다음 PC 선택 → 갱신 에지 → 다른 명령어 인출',GREEN)
def paths(self):
 rows=VGroup(txt('순차 실행',32,BLUE).move_to([0,1.8,0]),txt('0 → 1 → 2 → 3',49,BLUE).move_to([0,.9,0]),txt('분기 실행',32,ORANGE).move_to([0,-.7,0]),txt('0 → 1 → 3',49,ORANGE).move_to([0,-1.6,0]));self.show(self.centered(rows,7.5 if VERT else 11));self.note('동일한 명령어 메모리 · 달라지는 실행 경로')
def assemble(self):
 wave=route((-4.8,0),(-4.3,0),(-4.3,.7),(-3.8,.7),(-3.8,0),(-3.3,0),c=BLUE,w=3)
 gates=VGroup(pill('XOR',1.4,.7,BLUE).move_to([-1.3,.7,0]),pill('AND',1.4,.7,GREEN).move_to([-1.3,-.7,0]),txt('Sum',23,BLUE).move_to([.25,.7,0]),txt('Carry',23,GREEN).move_to([.25,-.7,0]))
 g=VGroup(wave,txt('0 / 1',29,BLUE).move_to([-4,-1.2,0]),gates,pill('가산기',1.8,1.8,PURPLE,29).move_to([2,0,0]),pill('ALU',1.6,1.8,PURPLE,35).move_to([4.2,0,0]),ln((-3.3,0),(-2.3,0),BLUE),ln((.8,0),(1.1,0),PURPLE),ln((2.9,0),(3.4,0),PURPLE));self.show(self.centered(g,7.8 if VERT else 12));self.note('전기 신호에서 연산 회로까지');self.at(132);d=self.centered(DataPath(),7.8 if VERT else 11);d.select();d.save();self.replace(g,d);self.note('기억 + CLK + Register + MUX → Datapath',GREEN);self.at(135);self.play(Indicate(d.regs,color=GREEN),run_time=.6)
def processor(self):
 p=self.centered(Processor(),7.85 if VERT else 14);self.show(p);self.note('PC · 명령어 메모리 · 해독 · 데이터 경로');self.at(139);p.fetch();self.play(Indicate(p.pc.box,color=GREEN),run_time=.6);self.at(141);p.decode();self.note('주소 선택 → 명령어 인출 → 해독 → 연산');self.at(143);p.calculate();self.play(Indicate(p.data.alu,color=PURPLE),run_time=.5);self.at(145);p.save();self.play(Indicate(p.data.regs[3],color=GREEN),run_time=.5);self.at(147);p.advance();self.note('계산 → 저장 → 명령어 실행 · 다음 주소 갱신',GREEN)
def limits(self):
 p=self.centered(Processor(),7.5 if VERT else 11);p.fetch();p.decode();self.show(p);self.note('기본 관계를 보여주는 교육용 개념도');self.at(151);self.play(Circumscribe(p,color=GRAY),run_time=.7);self.at(153);self.note('실제 CPU·GPU에는 더 많은 구조가 필요합니다')
def speed(self):
 g=VGroup(txt('동일한 명령어들',39,BLUE).move_to([0,1.5,0]),txt('실행 시간을 줄이려면?',43,INK).move_to([0,.2,0]),txt('회로 · 실행 순서 · 자원 활용',28,ORANGE).move_to([0,-1.4,0]));self.show(self.centered(g,7.8 if VERT else 11));self.note('성능을 결정하는 구조의 문제');self.at(159);self.play(Indicate(g[1],color=ORANGE),run_time=.7)
for n,f in [('hook',hook),('memory',memory),('address',address),('pc',pc_scene),('fetch',fetch_scene),('decode_execute',decode_execute),('advance',advance),('stages',stages),('condition',condition),('branch',branch),('paths',paths),('assemble',assemble),('processor',processor),('limits',limits),('speed',speed)]:setattr(ProgramScene,n,f)
