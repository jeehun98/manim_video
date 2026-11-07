"""Four-bit registers, input selection and non-destructive datapath reads."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_memory import Machine,writeback,reg_write,mem_write
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
 pos=m.get_center();oldh=m.height;oldw=m.width;new=txt(s,size,color)
 new.scale_to_fit_height(oldh)
 limit=width if width else max(oldw*1.5,.6)
 if new.width>limit:new.scale_to_fit_width(limit)
 m.become(new.move_to(pos));m._labelkey=key;return m


class MemoryScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+1/config.frame_rate+.005:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  11',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/174)))
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



class RegisterBank(VGroup):
 def __init__(self,values=(0,0,0,0)):
  super().__init__();self.values=tuple(values);self.cells=VGroup(*[pill(f'R{i} = {v}',1.95,.67,GREEN,27).move_to([0,1.35-i*.9,0]) for i,v in enumerate(values)])
  self.add(self.cells,txt('Registers',25,GREEN).move_to([0,2.05,0]))
 def sync(self,values):
  self.values=tuple(values)
  for i,(c,v) in enumerate(zip(self.cells,values)):setlabel(c[1],f'R{i} = {v}',GREEN)

class DataMemory(VGroup):
 def __init__(self,n=4,named=True,addresses=True):
  super().__init__();self.values={100+i:([5,3]+[0]*(n-2))[i] for i in range(n)};self.rows=VGroup();self.addresses=VGroup();self.outputs=VGroup();self.n=n
  for i,(a,v) in enumerate(self.values.items()):
   y=(n-1)*.35-i*.7;rect=RoundedRectangle(width=3.0,height=.58,corner_radius=.06,stroke_color=GRAY,stroke_width=1,fill_color=PANEL,fill_opacity=1).move_to([0,y,0]);addr=txt(str(a),22,ORANGE).move_to([-.85,y,0]);value=txt(str(v),29,PURPLE).move_to([.65,y,0]);self.rows.add(VGroup(rect,addr,value));self.addresses.add(addr);self.outputs.add(value)
  self.box=RoundedRectangle(width=3.35,height=n*.7+.35,corner_radius=.12,stroke_color=PURPLE,stroke_width=1.7);self.name=txt('Data Memory' if named else '저장 공간',26,PURPLE).move_to([0,self.box.height/2+.45,0]);self.add(self.box,self.rows,self.name)
  if not addresses:self.addresses.set_opacity(0)
 def select(self,address):
  for a,row in zip(self.values,self.rows):row[0].set_stroke(PURPLE if a==address else GRAY,width=2.7 if a==address else 1)
  return self.values[address]
 def sync(self,values):
  self.values.update(values)
  for a,row in zip(self.values,self.rows):setlabel(row[2],str(self.values[a]),PURPLE)
 def reveal_addresses(self):self.addresses.set_opacity(1)

class MemoryRead(VGroup):
 def __init__(self,named=True,addresses=True):
  super().__init__();self.mem=DataMemory(named=named,addresses=addresses).move_to([.8,0,0]);self.addr=pill('地址 = 100'.replace('地址','주소'),2.6,.7,ORANGE,27).move_to([-3.1,.7,0]);self.read=pill('Read = 5',2.7,.7,PURPLE,30).move_to([.8,-2.65,0]);self.add(self.mem,self.addr,self.read,Line(self.addr.get_right(),self.mem.box.get_left()+UP*.4,color=ORANGE),Line(self.mem.box.get_bottom(),self.read.get_top(),color=PURPLE));self.mem.select(100)
 def select(self,address):
  value=self.mem.select(address);setlabel(self.addr[1],f'주소 = {address}',ORANGE);setlabel(self.read[1],f'Read = {value}',PURPLE)

class WritebackChoice(VGroup):
 def __init__(self,named=True,connected=True,regs=(0,0,0,0)):
  super().__init__();self.regs=RegisterBank(regs).move_to([3.6,.1,0]);self.alu=pill('ALU Result = 8',3.2,.85,BLUE,29).move_to([-3.5,1.25,0]);self.mem=pill('Memory Read = 5',3.2,.85,PURPLE,28).move_to([-3.5,-.9,0]);self.mux=Polygon([-1.1,1.7,0],[-1.1,-1.4,0],[.65,-.85,0],[.65,1.15,0],stroke_color=ORANGE,fill_color=PANEL,fill_opacity=1);self.muxlabel=txt('MUX' if named else '?',29,ORANGE).move_to([-.25,.15,0]);self.paths=[ln((-1.9,1.25),(-1.1,1.25),BLUE),ln((-1.9,-.9),(-1.1,-.9),PURPLE)]
  self.data=txt('Write Data = 8',25,BLUE).move_to([.25,2.2,0]);self.sel=txt('Source = ALU',25,ORANGE).move_to([-.3,-2.2,0]);self.dest=txt('Destination = R3',25,ORANGE).move_to([3.6,-2.2,0]);self.we=txt('RegWE = 0 · CLK',23,ORANGE).move_to([3.5,-3,0]);self.add(self.regs,self.alu,self.mem,*self.paths,self.mux,self.muxlabel,self.data,self.sel,self.dest,self.we,ln((-.3,-1.8),(-.3,-1.1),ORANGE))
  self.out=VGroup(*[route((.65,.15),(2.1,.15),(2.1,c.get_left()[1]),(c.get_left()[0],c.get_left()[1]),c=GREEN) for c in self.regs.cells]);self.add(self.out);self.source='ALU';self.rd=3
  for i,p in enumerate(self.out):p.set_stroke(opacity=1 if i==3 else .12)
  if not connected:self.mux.set_stroke(opacity=0);self.mux.set_fill(opacity=0);self.muxlabel.set_opacity(0);self.out.set_stroke(opacity=0);self.data.set_opacity(0);self.sel.set_opacity(0)
 def select(self,source,rd):
  self.source=source;self.rd=rd;value=writeback(8,5,source)
  for p,c in zip(self.paths,[BLUE,PURPLE]):p.set_stroke(c,opacity=1 if c== (BLUE if source=='ALU' else PURPLE) else .3,width=3)
  setlabel(self.data,f'Write Data = {value}',BLUE if source=='ALU' else PURPLE);setlabel(self.sel,f'Source = {source}',ORANGE);setlabel(self.dest,f'Destination = R{rd}',ORANGE)
  for i,p in enumerate(self.out):p.set_stroke(GREEN,opacity=1 if i==rd else .12)
 def pulse(self):
  value=writeback(8,5,self.source);self.regs.sync(reg_write(self.regs.values,self.rd,value));setlabel(self.we,'RegWE = 1 · CLK ↑',ORANGE)
 def hold(self):setlabel(self.we,'RegWE = 0 · CLK',ORANGE)

class MemorySystem(VGroup):
 """Existing two-read datapath, a distinct store path, two-input writeback mux."""
 def __init__(self,regs=(0,0,0,0),context=False):
  super().__init__();self.machine=Machine(regs);self.regs=RegisterBank(regs).move_to([-4.6,.25,0]);self.mem=DataMemory().move_to([5.1,.45,0]);self.reads=VGroup();self.muxes=VGroup()
  for j,cy in enumerate([1.15,-.6]):
   box=pill('A' if j==0 else 'B',.9,1.3,BLUE,27).move_to([-1.4,cy,0]);self.muxes.add(box)
   for i,c in enumerate(self.regs.cells):
    y=cy+.4-i*.27;lane=-3.35+i*.25+j*.07;q=c.get_right();self.reads.add(route((q[0],q[1]),(lane,q[1]),(lane,y),(-1.85,y),c=GRAY,w=1.4))
  self.alu=pill('ALU +',1.85,1.4,BLUE,29).move_to([1, .3,0]);self.result=txt('ALU 대기',23,GRAY).move_to([1,1.65,0]);self.result_value=0
  self.add(self.regs,self.reads,self.muxes,self.alu,self.result,route((-.95,1.15),(-.25,1.15),(-.25,.65),(.075,.65),c=BLUE),route((-.95,-.6),(-.15,-.6),(-.15,-.05),(.075,-.05),c=BLUE))
  self.address=pill('Address = 100',3.2,.65,ORANGE,25).move_to([5.1,3,0]);self.add(self.mem,self.address,Line(self.address.get_bottom(),self.mem.box.get_top(),color=ORANGE))
  # ALU and memory data remain two physically distinct MUX candidates.
  self.wbmux=Polygon([.8,-2.45,0],[.8,-3.8,0],[-.8,-3.45,0],[-.8,-2.8,0],stroke_color=ORANGE,fill_color=PANEL,fill_opacity=1);self.wblabel=txt('WB MUX',23,ORANGE).move_to([0,-3.12,0])
  self.alupath=route((1.925,.3),(2.75,.3),(2.75,-2.75),(.8,-2.75),c=BLUE)
  q=self.mem.box.get_right();self.mempath=route((q[0],q[1]),(7.4,q[1]),(7.4,-3.48),(.8,-3.48),c=PURPLE)
  self.writeselect=pill('DST = R1',2.45,.65,ORANGE,24).move_to([-4.1,-3.12,0]);self.regwe=txt('RegWE = 0',22,ORANGE).move_to([-4.1,-3.9,0]);self.sel=txt('WB = MEM',22,ORANGE).move_to([0,-4.25,0]);self.memwe=txt('MemWE = 0',22,ORANGE).move_to([5.1,-2.05,0]);self.valid=txt('Ready = 1',21,GRAY).move_to([5.1,-2.55,0])
  self.regwrites=VGroup()
  for i,c in enumerate(self.regs.cells):
   d=c.get_left();x=-6.1-i*.11;self.regwrites.add(route((-5.325,-3.12),(x,-3.12),(x,d[1]),(d[0],d[1]),c=GRAY,w=1.3))
  self.add(self.wbmux,self.wblabel,self.alupath,self.mempath,self.writeselect,self.regwe,self.sel,self.memwe,self.valid,self.regwrites,ln((-.8,-3.12),(-2.875,-3.12),GREEN))
  # B-port data goes to memory WD directly; the ALU is not in the Store data path.
  self.storepath=route((-.95,-.6),(-.55,-.6),(-.55,-1.75),(3.05,-1.75),(3.05,-.65),(self.mem.box.get_left()[0],-.65),c=PURPLE)
  self.wd=txt('Write Data = 0',21,PURPLE).move_to([1.5,-2.05,0]);self.add(self.storepath,self.wd);self.mode='';self.address_value=100;self.rd=1;self.src=3
  if context:
   self.context=VGroup(pill('PC',1,.6,GREEN,22).move_to([-4.8,3.5,0]),pill('Instruction Memory',3.5,.6,GRAY,22).move_to([-2.1,3.5,0]),pill('Decoder',1.7,.6,ORANGE,22).move_to([.8,3.5,0]),ln((-4.3,3.5),(-3.85,3.5),GRAY),ln((-.35,3.5),(-.05,3.5),ORANGE));self.add(self.context)
  self.quiet()
 def quiet(self):
  self.reads.set_stroke(opacity=.25);self.alupath.set_stroke(opacity=.25);self.mempath.set_stroke(opacity=.25);self.storepath.set_stroke(opacity=.25);self.regwrites.set_stroke(opacity=.25)
  setlabel(self.regwe,'RegWE = 0',ORANGE);setlabel(self.memwe,'MemWE = 0',ORANGE)
 def update_reg_values(self):self.regs.sync(self.machine.regs)
 def prepare_load(self,address=100,rd=1,ready=True):
  self.quiet();self.mode='LOAD';setlabel(self.result,'ALU 대기',GRAY);self.address_value=address;self.rd=rd;self.mem.select(address);setlabel(self.address[1],f'Address = {address}',ORANGE);setlabel(self.sel,'WB = MEM',ORANGE);setlabel(self.writeselect[1],f'DST = R{rd}',ORANGE);setlabel(self.valid,'Ready = '+str(int(ready)),GRAY if ready else ORANGE);self.mempath.set_stroke(PURPLE,opacity=1,width=3);self.regwrites[rd].set_stroke(GREEN,opacity=1,width=2.5)
 def prepare_add(self):
  self.quiet();self.mode='ADD';self.result_value=self.machine.regs[1]+self.machine.regs[2];setlabel(self.result,f'Result = {self.result_value}',BLUE);setlabel(self.sel,'WB = ALU',ORANGE);setlabel(self.writeselect[1],'DST = R3',ORANGE);self.reads[1].set_stroke(BLUE,opacity=1,width=3);self.reads[6].set_stroke(BLUE,opacity=1,width=3);self.alupath.set_stroke(BLUE,opacity=1,width=3);self.regwrites[3].set_stroke(GREEN,opacity=1,width=2.5)
 def prepare_store(self,address=102,src=3):
  self.quiet();self.mode='STORE';setlabel(self.result,'ALU 대기',GRAY);setlabel(self.sel,'WB: 사용 안 함',GRAY);setlabel(self.writeselect[1],'DST: 대기',GRAY);self.address_value=address;self.src=src;self.mem.select(address);setlabel(self.address[1],f'Address = {address}',ORANGE);setlabel(self.wd,f'Write Data = {self.machine.regs[src]}',PURPLE);self.reads[4+src].set_stroke(PURPLE,opacity=1,width=3);self.storepath.set_stroke(PURPLE,opacity=1,width=3)
 def pulse(self,ready=True):
  if self.mode=='LOAD':
   self.machine.load(self.address_value,self.rd,ready=ready);self.update_reg_values();setlabel(self.regwe,'RegWE = '+str(int(ready))+' · CLK ↑',ORANGE)
  elif self.mode=='ADD':self.machine.add();self.update_reg_values();setlabel(self.regwe,'RegWE = 1 · CLK ↑',ORANGE)
  elif self.mode=='STORE':self.machine.store(self.address_value,self.src);self.mem.sync(self.machine.memory);setlabel(self.memwe,'MemWE = 1 · 更新'.replace('更新','갱신'),ORANGE)

class OriginalCore(VGroup):
 def __init__(self):
  super().__init__();self.regs=RegisterBank((0,5,3,0)).move_to([-3.2,0,0]);self.alu=pill('ALU +',2,1.4,BLUE,34).move_to([1.2,0,0]);self.result=txt('8',40,BLUE).move_to([3.1,0,0]);self.a=pill('MUX A',1.2,.8,BLUE,21).move_to([-.9,.9,0]);self.b=pill('MUX B',1.2,.8,BLUE,21).move_to([-.9,-.9,0]);self.we=txt('RegWE = 0 · CLK',23,ORANGE).move_to([0,-2.5,0]);self.add(self.regs,self.alu,self.result,self.a,self.b,self.we)
  for cell,box,pin in [(self.regs.cells[1],self.a,.35),(self.regs.cells[2],self.b,-.35)]:
   q=cell.get_right();self.add(route((q[0],q[1]),(-2,q[1]),(-2,box.get_left()[1]),(box.get_left()[0],box.get_left()[1]),c=BLUE));p=box.get_right();self.add(route((p[0],p[1]),(-.05,p[1]),(-.05,pin),(.2,pin),c=BLUE))
  d=self.regs.cells[3].get_left();self.returnpath=route((2.2,0),(3.7,0),(3.7,-2),(-4.6,-2),(-4.6,d[1]),(d[0],d[1]),c=BLUE);self.add(self.returnpath)
  self.context=VGroup(pill('PC',1,.55,GREEN,22).move_to([-3.6,3,0]),pill('Instruction Memory',3.5,.55,GRAY,22).move_to([-1,3,0]),pill('Decoder',1.7,.55,ORANGE,22).move_to([2.1,3,0]),ln((-3.1,3),(-2.75,3),GRAY),ln((.75,3),(1.25,3),ORANGE));self.add(self.context)
 def pulse(self):self.regs.sync((0,5,3,8));setlabel(self.we,'RegWE = 1 · CLK ↑',ORANGE)

def hook(self):
 c=self.centered(OriginalCore(),7.8 if VERT else 12);self.show(c);self.note('PC → 명령어 인출 → 해독 → 레지스터·ALU');self.at(6);c.pulse();self.play(Indicate(c.regs.cells[3],color=GREEN),run_time=.5);self.at(10);setlabel(c.we,'RegWE = 0 · CLK',ORANGE);self.note('계산할 값 5와3이 이미 준비되었다고 가정했습니다');self.play(Indicate(c.regs.cells[1],color=GREEN),Indicate(c.regs.cells[2],color=GREEN),run_time=.6)
def capacity(self):
 regs=RegisterBank().move_to([-3,0,0]);cards=VGroup(*[pill(str(i+1),.7,.55,GRAY,20).move_to([.2+i%5*.85,1.35-i//5*.8,0]) for i in range(20)]);label=txt('수백 · 수천 개의 데이터',28,GRAY).move_to([2,-2.3,0]);g=self.centered(VGroup(regs,cards,label),7.8 if VERT else 12);self.show(g);self.at(19);self.note('한 시점에 레지스터에 보관할 수 있는 양은 제한됩니다');self.play(Indicate(regs,color=GREEN),run_time=.6);self.at(23)
 frame=SurroundingRectangle(cards,buff=.25,color=PURPLE,corner_radius=.1);self.show(frame);self.note('별도 저장 공간에 두고 필요한 값만 가져온다면?',PURPLE)
def locations(self):
 r=self.centered(MemoryRead(named=False,addresses=False),7.8 if VERT else 10);setlabel(r.addr[1],'선택 정보 ?',ORANGE);self.show(r);self.note('첫 번째 예시 위치와 두 번째 예시 위치');self.at(34);self.play(Indicate(r.mem.rows[0],color=PURPLE),Indicate(r.mem.rows[1],color=PURPLE),run_time=.6);self.at(38);r.select(101);setlabel(r.addr[1],'선택 정보 ?',ORANGE);self.note('어느 칸을 선택할지 지정할 정보가 필요합니다')
def address(self):
 r=self.centered(MemoryRead(named=False,addresses=True),7.8 if VERT else 10);self.show(r);self.note('주소 100 ≠ 데이터 5 · 주소 101 ≠ 데이터 3',ORANGE);self.at(47);r.select(101);self.play(Indicate(r.mem.rows[1],color=PURPLE),run_time=.5);self.at(49);r.select(100);self.at(51);setlabel(r.mem.name,'Data Memory',PURPLE);self.note('읽기와 쓰기는 서로 다른 제어 동작입니다',PURPLE)
def connection(self):
 core=OriginalCore().scale(.68).move_to([-2.5,0,0]);mem=MemoryRead().scale(.59).move_to([3.7,0,0]);g=self.centered(VGroup(core,mem),7.8 if VERT else 13.5);self.show(g);self.note('읽어 온 5를 어디에 연결할까?');self.at(61);self.play(Indicate(core.a,color=BLUE),Indicate(core.b,color=BLUE),run_time=.6);self.note('지금까지는 레지스터의 값을 ALU에 전달했습니다');self.at(66);self.play(Indicate(mem.read,color=PURPLE),run_time=.6);self.note('메모리 결과를 레지스터에 기록할 연결이 필요합니다',PURPLE)
def candidates(self):
 w=self.centered(WritebackChoice(named=False,connected=False),7.8 if VERT else 12);self.show(w);self.note('기존 결과 후보 : ALU = 8',BLUE);self.at(73);w.regs.sync((0,0,0,8));setlabel(w.we,'RegWE = 1 · CLK ↑',ORANGE);self.play(Indicate(w.regs.cells[3],color=GREEN),run_time=.5);self.at(75);w.hold();self.play(Indicate(w.mem,color=PURPLE),run_time=.5);self.note('ALU의8과메모리의5는서로다른쓰기입력후보',PURPLE)
def writeback_scene(self):
 w=self.centered(WritebackChoice(named=False),7.8 if VERT else 12);self.show(w);self.note('출처를 선택해도 아직 저장값은 바뀌지 않습니다');self.at(82);w.select('MEM',1);self.at(84);setlabel(w.muxlabel,'MUX',ORANGE);self.note('같은선택원리 · 이번에는쓰기입력의출처선택',ORANGE);self.play(Indicate(w.mux,color=ORANGE),run_time=.6);self.at(88);w.select('ALU',3);w.pulse();self.play(Indicate(w.regs.cells[3],color=GREEN),run_time=.5);self.at(90);w.hold();w.select('MEM',1);self.at(91);w.pulse();self.play(Indicate(w.regs.cells[1],color=GREEN),run_time=.5);self.note('Source / Destination / RegWE·CLK는 별도입니다')
def controls(self):
 s=self.centered(MemorySystem(context=True),7.8 if VERT else 14);s.storepath.set_stroke(opacity=0);s.wd.set_opacity(0);self.show(s);self.note('주소 ? · 데이터 출처 ? · 목적지 ? · 쓰기 허용 ?',ORANGE);self.at(99);self.play(Indicate(s.context[-3],color=ORANGE),run_time=.5);self.note('명령어를 해독해 필요한 제어 신호를 만들 수 있습니다');self.at(103);s.prepare_load(100,1);self.note('읽을 주소100 · 저장 위치R1 · 동작: 메모리 읽기',PURPLE);self.play(Indicate(s.mem.rows[0],color=PURPLE),Indicate(s.writeselect,color=ORANGE),run_time=.6)
def load(self):
 s=self.centered(MemorySystem(context=True),7.8 if VERT else 14);s.prepare_load(100,1);self.show(s);self.note('LOAD R1, [100]  ·  Memory → Register',PURPLE);self.at(111);self.play(Indicate(s.mem.rows[0],color=PURPLE),run_time=.6);self.at(113);s.pulse();self.play(Indicate(s.regs.cells[1],color=GREEN),run_time=.5);self.at(114.5);s.quiet();self.note('R1 = 5 · Memory[100] = 5 유지',GREEN)
def store(self):
 s=self.centered(MemorySystem(regs=(0,5,3,8),context=True),7.8 if VERT else 14);self.show(s);self.note('R3의8을 메모리주소102에 보관하려면?',PURPLE);self.at(119);s.prepare_store(102,3);self.play(Indicate(s.regs.cells[3],color=GREEN),run_time=.6);self.at(122);self.note('Address = 102 · Write Data = 8 · RegWE = 0',ORANGE);self.at(124);s.pulse();self.play(Indicate(s.mem.rows[2],color=PURPLE),run_time=.5);self.at(126);s.quiet();self.note('STORE R3, [102]  ·  Register → Memory',PURPLE)
def program(self):
 s=self.centered(MemorySystem(context=True),7.8 if VERT else 14);self.show(s);s.prepare_load(100,1);self.note('① LOAD R1, [100]',PURPLE);self.at(133);s.pulse();self.play(Indicate(s.regs.cells[1],color=GREEN),run_time=.4);self.at(134.5);s.prepare_load(101,2);self.note('② LOAD R2, [101]',PURPLE);self.at(135.5);s.pulse();self.play(Indicate(s.regs.cells[2],color=GREEN),run_time=.4);self.at(137);s.prepare_add();self.note('③ ADD R3, R1, R2  →  5 + 3 = 8',BLUE);self.at(138.5);s.pulse();self.play(Indicate(s.regs.cells[3],color=GREEN),run_time=.4);self.at(140);s.prepare_store(102,3);self.note('④ STORE R3, [102]',PURPLE);self.at(141.5);s.pulse();self.play(Indicate(s.mem.rows[2],color=PURPLE),run_time=.5);self.at(142.5);s.quiet()
def expanded(self):
 s=MemorySystem(context=True);s.machine.load(100,1);s.machine.load(101,2);s.machine.add();s.machine.store();s.update_reg_values();s.mem.sync(s.machine.memory);s.prepare_add();s.quiet();self.show(self.centered(s,7.8 if VERT else 14));self.note('레지스터에 미리 있던 값만 계산하던 구조에서');self.at(148);s.prepare_load(100,1);self.note('메모리에서 가져오기 → 계산하기 → 다시 저장하기',PURPLE);self.at(150);s.prepare_store(102,3);self.play(Indicate(s.mem.rows[2],color=PURPLE),run_time=.5)
def latency(self):
 s=self.centered(MemorySystem(context=True),7.8 if VERT else 14);s.prepare_load(100,1,ready=False);s.pulse(ready=False);self.show(s);self.note('LOAD R1, [100] · 데이터 응답이 아직 준비되지 않았다면?',ORANGE);self.at(156);self.play(Indicate(s.valid,color=ORANGE),run_time=.6);self.note('Ready = 0 → RegWE = 0 · 미완성 값을 기록하지 않음');self.at(161);self.note('유지할 정보: 수행 동작 LOAD · 주소100 · 목적지R1',ORANGE);self.play(Indicate(s.writeselect,color=ORANGE),Indicate(s.address,color=ORANGE),run_time=.7)
def state(self):
 g=VGroup(*[pill(t,5,.8,c,31).move_to([0,1.4-i*1.3,0]) for i,(t,c) in enumerate([('수행 중: LOAD',ORANGE),('읽을 주소: 100',ORANGE),('결과를 기록할 곳: R1',GREEN)])]);self.show(self.centered(g,7.8 if VERT else 11));self.note('주소 결정 → 데이터 응답 대기 → 레지스터 기록')
for name,fn in [('hook',hook),('capacity',capacity),('locations',locations),('address',address),('connection',connection),('candidates',candidates),('writeback',writeback_scene),('controls',controls),('load',load),('store',store),('program',program),('expanded',expanded),('latency',latency),('state',state)]:setattr(MemoryScene,name,fn)
