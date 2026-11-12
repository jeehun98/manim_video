"""Four-bit registers, input selection and non-destructive datapath reads."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
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
  self.add(txt('GPU 개론  /  13',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/148)))
  self.add(base,bar,txt(f'{self.index+1:02} / 12',17,GRAY).move_to([x-.55,y+(.27 if VERT else -.2),0]).set_z_index(32))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)




RED='#F87171'
def value(box,s,color=INK):
 t=txt(s,27,color);t.scale_to_fit_height(box[0].height*(.035 if s.strip()=='—' else .44))
 if t.width>box[0].width*.9:t.scale_to_fit_width(box[0].width*.9)
 box[1].become(t.move_to(box[0]))
def card(name,address,dest,color):
 a=pill(f'{name}   LOAD {dest}, [{address}]',5.3,.9,color,30)
 b=pill(f'주소 {address}  ·  목적지 {dest}',5.3,.8,color,29).next_to(a,DOWN,buff=.3)
 return VGroup(a,b)

class Hardware(VGroup):
 def __init__(self):
  super().__init__();self.blocks=[];self.outputs=[]
  names=['명령어 메모리','주소 계산 · ALU','데이터 메모리','레지스터 기록']
  vals=['PC0 → LOAD R1,[100]','주소 선택 100','[100] → 5','R1 = 0']
  for i,(name,v) in enumerate(zip(names,vals)):
   xy=[(-2.5,1.5),(2.5,1.5),(-2.5,-1.3),(2.5,-1.3)][i] if VERT else [(-5.3,0),(-1.8,0),(1.8,0),(5.3,0)][i]
   b=pill(v,4.4 if VERT else 3.2,1.05,GRAY,25).move_to([*xy,0]);lab=txt(name,25,INK,b.width).next_to(b,UP,buff=.3);self.add(b,lab);self.blocks.append(b)
  self.outline=SurroundingRectangle(self,buff=.45,color=EDGE,corner_radius=.15);self.add(self.outline)
 def activate(self,items):
  for i,b in enumerate(self.blocks):b[0].set_stroke(BLUE if i in items else GRAY,width=3 if i in items else 1,opacity=1 if i in items else .45)

def hw(self):return self.centered(Hardware(),7.8 if VERT else 14)
class DualMemory(VGroup):
 def __init__(self,both=False):
  super().__init__();self.im=pill('현재 인출 없음',5.5,1.1,GRAY,29);self.dm=pill('A : [100] → 5',5.5,1.1,BLUE,32)
  if VERT:self.im.move_to([0,2.0,0]);self.dm.move_to([0,-1.8,0])
  else:self.im.move_to([-3.5,0,0]);self.dm.move_to([3.5,0,0])
  self.il=txt('명령어 메모리',29,INK).next_to(self.im,UP,buff=.3);self.dl=txt('데이터 메모리',29,INK).next_to(self.dm,UP,buff=.3)
  self.ia=pill('명령어 주소 PC = 1',4.3,.65,ORANGE,25).next_to(self.im,DOWN,buff=.6);self.da=pill('데이터 주소 = 100',4.3,.65,ORANGE,25).next_to(self.dm,DOWN,buff=.6)
  self.iln=Line(self.ia.get_top(),self.im.get_bottom(),color=GRAY);self.dln=Line(self.da.get_top(),self.dm.get_bottom(),color=BLUE)
  self.add(self.im,self.dm,self.il,self.dl,self.ia,self.da,self.iln,self.dln)
  if both:self.concurrent()
 def concurrent(self):
  value(self.im,'B : LOAD R2, [101]',PURPLE);self.im[0].set_stroke(PURPLE,width=3);self.iln.set_stroke(PURPLE,width=3);self.dm[0].set_stroke(BLUE,width=3)

def dual(self,both=False):return self.centered(DualMemory(both),7.8 if VERT else 13.5)

class Pipeline(VGroup):
 def __init__(self,registers=False,named=False):
  super().__init__();self.stages=[];self.regs=[];self.reglabels=[];self.paths=VGroup();self.add(self.paths)
  names=['F · 명령어 인출','D · 주소 결정','M · 데이터 읽기','W · 결과 기록']
  for i,name in enumerate(names):
   xy=(-1.85,3-i*2) if VERT else (-5.4+i*3.6,.8)
   b=pill('—',3.1 if VERT else 3,1,GRAY,28).move_to([*xy,0]);lab=txt(name,24,INK,3).next_to(b,UP,buff=.17);self.add(b,lab);self.stages.append(b)
  for i in range(3):
   xy=(1.85,2-i*2) if VERT else (-3.6+i*3.6,-1.0)
   b=pill('—',3.45 if VERT else 3.3,.85,GREEN,25).move_to([*xy,0]);lab=txt(['F/D','D/M','M/W'][i] if named else '次の段階へ'.replace('次の段階へ','次段 저장'.replace('次段','다음 단계')),21,GREEN,3.4).next_to(b,UP,buff=.13)
   self.regs.append(b);self.reglabels.append(lab);self.add(b,lab)
  self.visible_regs=registers;self.draw_paths(registers)
  if not registers:
   for b,l in zip(self.regs,self.reglabels):b.set_opacity(0);l.set_opacity(0)
 def draw_paths(self,regs):
  self.paths.remove(*list(self.paths))
  for i in range(3):
   a,b=self.stages[i],self.stages[i+1]
   if regs:
    r=self.regs[i]
    for u,v in [(a,r),(r,b)]:
     st=u.get_bottom();en=v.get_top();middle=np.array([en[0],st[1],0]);self.paths.add(VMobject(stroke_color=GRAY,stroke_width=2).set_points_as_corners([st,middle,en]))
   else:self.paths.add(Line(a.get_bottom() if VERT else a.get_right(),b.get_top() if VERT else b.get_left(),color=GRAY,stroke_width=2))
  self.paths.set_z_index(-1)
 def reveal(self):
  self.visible_regs=True
  for b,l in zip(self.regs,self.reglabels):
   b[0].set_stroke(GREEN,opacity=1);b[0].set_fill(PANEL,opacity=1);b[1].set_opacity(1);l.set_opacity(1)
  self.draw_paths(True)
 def packet(self,index,owner,text):
  c=BLUE if owner=='A' else PURPLE if owner=='B' else GRAY;b=self.regs[index];b[0].set_stroke(c if owner else GREEN,width=2.7);value(b,owner+' · '+text if owner else '—',c)
 def stage(self,index,owner,text):
  c=BLUE if owner=='A' else PURPLE if owner=='B' else GRAY;b=self.stages[index];b[0].set_stroke(c,width=3 if owner else 1);value(b,owner+' · '+text if owner else '—',c)
 def cycle(self,n):
  for i in range(4):
   who='A' if i==n-1 else 'B' if i==n-2 else '';addr=100 if who=='A' else 101;rd='R1' if who=='A' else 'R2';data=5 if who=='A' else 3
   text=[f'LOAD {rd}',f'주소{addr}',f'[{addr}] → {data}',f'{rd} ← {data}'][i];self.stage(i,who,text)
  for j in range(3):
   i=j+1;who='A' if i==n-1 else 'B' if i==n-2 else '';addr=100 if who=='A' else 101;rd='R1' if who=='A' else 'R2';data=5 if who=='A' else 3
   fields=[f'LOAD {rd},[{addr}]',f'{addr} · {rd} · 읽기',f'{data} · {rd} · 기록'][j];self.packet(j,who,fields)

def pipe(self,regs=True,named=False):return self.centered(Pipeline(regs,named),7.9 if VERT else 14.1)

def overview(self):
 h=hw(self);self.show(h);self.note('한 프로세서 내부의 기능별 구분 · 상세 배선은 생략');self.at(5);h.activate([0]);self.play(Indicate(h.blocks[0],color=BLUE),run_time=.5);self.note('서로 다른 회로가 맡는 역할을 살펴봅니다')
def functions(self):
 h=hw(self);self.show(h);h.activate([0]);self.at(12);h.activate([1]);value(h.blocks[1],'100 + 4 → 104',ORANGE);self.note('ALU 기능 시연 · LOAD [100]과는 별도 예시',ORANGE);self.at(16);h.activate([2]);self.play(Indicate(h.blocks[2],color=BLUE),run_time=.5);self.note('데이터 주소100 → 값5',BLUE);self.at(19);h.activate([0,1,2]);self.note('한 프로세서에 속한 서로 다른 회로')
def independent(self):
 d=dual(self);self.show(d);self.note('독립적인 메모리 접근 경로를 가정합니다',ORANGE);self.at(28);self.play(Indicate(d.dm,color=BLUE),run_time=.55);self.note('A는 데이터 메모리 사용 · 명령어 인출 경로는 비어 있음');self.at(35);self.play(Indicate(d.im,color=PURPLE),run_time=.5);self.note('비어 있는 인출 회로를 B에 사용한다면?',PURPLE)
def concurrent(self):
 d=dual(self,True);self.show(d);self.note('A · 데이터 읽기 / B · 명령어 인출');self.at(41);self.play(Indicate(d.im,color=PURPLE),Indicate(d.dm,color=BLUE),ShowPassingFlash(d.iln.copy().set_stroke(width=5),time_width=.4),ShowPassingFlash(d.dln.copy().set_stroke(width=5),time_width=.4),run_time=1.4);self.at(46);self.note('같은 시간 · 서로 다른 회로 · 결과 기록은 아직 하지 않음')
def identity(self):
 a=card('A',100,'R1',BLUE);b=card('B',101,'R2',PURPLE);g=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=1.0);self.centered(g,7.6 if VERT else 13.5);self.show(g);self.note('같은 시간에 존재하는 두 명령어의 정보');self.at(53);self.play(Indicate(a,color=BLUE),run_time=.5);self.at(58);self.play(Indicate(b,color=PURPLE),run_time=.5);self.at(62);self.note('주소와 목적지를 각각 구분해야 합니다',ORANGE)
def overwrite(self):
 need=pill('A가 아직 필요한 정보 : 100 · R1',6.8,.8,BLUE,29);reg=pill('100 · R1',5,1.1,BLUE,37);incoming=pill('B의 입력 : 101 · R2',6.8,.8,PURPLE,30);g=VGroup(need,reg,incoming).arrange(DOWN,buff=.7);self.centered(g,7.6 if VERT else 10);self.show(g);self.note('잘못된 공유 설계의 예시 · 한 저장 위치');self.at(71);self.note('CLK ↑ : B 정보로 갱신',PURPLE);value(reg,'101 · R2',PURPLE);reg[0].set_stroke(RED,width=3);self.play(Indicate(reg,color=RED),run_time=.5);self.note('A의 100 · R1을 더 이상 보관하지 못함',RED)
def insert(self):
 p=pipe(self,False);self.show(p);self.note('필요한 정보를 단계별로 따로 저장한다');self.at(79);self.play(Indicate(p.stages[1],color=GREEN),run_time=.45);self.note('이미 배운 여러 비트 저장 회로를 재사용',GREEN);self.at(83);p.reveal();self.play(*[Indicate(r,color=GREEN) for r in p.regs],run_time=.6);self.note('명령어 / 주소·목적지 / 데이터·목적지',GREEN)
def preserve(self):
 p=pipe(self);p.packet(1,'A','100 · R1 · 읽기');p.stage(2,'A','[100] → 5');self.show(p);self.note('앞선 A : 주소100 · 목적지R1',BLUE);self.at(90);self.play(Indicate(p.regs[1],color=BLUE),run_time=.5);self.at(93);p.packet(0,'B','LOAD R2,[101]');p.stage(1,'B','주소101 → R2');self.note('B가 주소101을 계산해도 저장된 A 정보는 유지',PURPLE);self.at(97);self.play(Indicate(p.regs[1],color=BLUE),Indicate(p.stages[1],color=PURPLE),run_time=.5);self.at(99);p.packet(0,'','');p.packet(2,'A','5 · R1 · 기록');p.packet(1,'B','101 · R2 · 읽기');p.stage(2,'B','[101] → 3');p.stage(3,'A','R1 ← 5');p.stage(1,'','');self.note('CLK ↑ : A 데이터5/R1과 B 주소101/R2를 각각 보관',GREEN);self.play(Indicate(p.regs[2],color=BLUE),Indicate(p.regs[1],color=PURPLE),run_time=.6)
def registers(self):
 p=pipe(self,True,True);p.cycle(4);self.show(p);self.note('파이프라인 레지스터 · Pipeline Register',GREEN);self.at(108);self.play(*[Indicate(r,color=GREEN) for r in p.regs],run_time=.6);self.note('데이터 + 목적지 + 단계에 필요한 제어 정보',GREEN)
def execute(self):
 p=pipe(self,True,True);self.show(p)
 for t,n in [(111.5,1),(112.4,2),(113.3,3),(114.2,4),(115.1,5)]:
  self.at(t);p.cycle(n);self.note(f'클럭 구간 {n} · 단계별로 서로 다른 명령어 처리',ORANGE);self.wait(.25)
 self.at(116);self.note('명령어 파이프라인 · Instruction Pipeline',GREEN);self.at(119);p.cycle(3);self.note('같은 클럭 구간: A는 M / B는 D · 전역 단일 단계 선택 없음');self.at(121);p.cycle(5);self.note('실행 완료: R1 = 5 · R2 = 3',GREEN)

class Schedule(VGroup):
 def __init__(self):
  super().__init__();self.cells=[];x0=-2.4;dx=.9
  for c in range(8):self.add(txt(str(c+1),24,ORANGE).move_to([x0+c*dx,2.05,0]))
  entries=[('순차 A',BLUE,['F','D','M','W','·','·','·','·']),('순차 B',PURPLE,['·','·','·','·','F','D','M','W']),('중첩 A',BLUE,['F','D','M','W','·','·','·','·']),('중첩 B',PURPLE,['·','F','D','M','W','·','·','·'])]
  for i,(name,c,row) in enumerate(entries):
   y=1.2-i*.95;self.add(txt(name,25,c).move_to([-4,y,0]))
   for j,v in enumerate(row):
    b=pill(v,.78,.68,c if v!='·' else GRAY,25).move_to([x0+j*dx,y,0]);self.add(b)
    if v=='W':self.cells.append(b)
  self.add(txt('클럭 구간 · 동일 주기/단계당 1주기/충돌 없음 가정',23,GRAY,10).move_to([.5,-3,0]))
def throughput(self):
 g=self.centered(Schedule(),7.7 if VERT else 13);self.show(g);self.note('A 완료: 두 방식 모두 4번째 구간',BLUE);self.play(Indicate(g.cells[0],color=BLUE),Indicate(g.cells[2],color=BLUE),run_time=.6);self.at(127);self.play(Indicate(g.cells[1],color=PURPLE),Indicate(g.cells[3],color=PURPLE),run_time=.6);self.note('B 완료: 순차 8 / 파이프라인 5 · 전체 처리량 증가 가능',GREEN)
def dependency(self):
 a=pill('LOAD R1, [100]',6,.95,BLUE,32);b=pill('ADD R3, R1, R2',6,.95,PURPLE,32);a.move_to([0,1.5,0]);b.move_to([0,-1.1,0]);line=Line(a.get_bottom(),b.get_top(),color=ORANGE);q=txt('R1의 새 값 ?',30,ORANGE).move_to([2,0,0]);g=self.centered(VGroup(a,b,line,q),7.7 if VERT else 12);self.show(g);self.note('지금부터는 별도 예시: LOAD → ADD');self.at(137);self.play(Indicate(a,color=BLUE),run_time=.5);self.note('LOAD가 새 R1 값을 가져오는 중',BLUE);self.at(141);self.play(Indicate(b,color=ORANGE),run_time=.5);self.note('ADD는 그 값을 필요로 함 · 준비 전에는 계산하지 않음',ORANGE);self.at(144);self.note('필요한 값이 준비되었는지 어떻게 확인할까?',ORANGE)
for n in ['overview','functions','independent','concurrent','identity','overwrite','insert','preserve','registers','execute','throughput','dependency']:setattr(MemoryScene,n,globals()[n])
