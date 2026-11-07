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
  self.add(txt('GPU 개론  /  14',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/147)))
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




from check_logic import operand,dependency
RED='#EF4444'
def value(box,s,color=INK):
 t=txt(s,27,color);t.scale_to_fit_height(box[0].height*(.035 if s.strip()=='—' else .43))
 if t.width>box[0].width*.9:t.scale_to_fit_width(box[0].width*.9)
 box[1].become(t.move_to(box[0]))

class FiveStage(VGroup):
 def __init__(self):
  super().__init__();self.stages=[]
  labels=['IF · 명령어 인출','ID · 해독/읽기','EX · ALU','MEM · 데이터 읽기','WB · 결과 기록']
  for i,l in enumerate(labels):
   xy=(-1.2,3.2-i*1.6) if VERT else (-5.6+i*2.8,.3)
   b=pill('—',3.7 if VERT else 2.5,.9,GRAY,27).move_to([*xy,0]);lab=txt(l,22,INK,b.width).next_to(b,UP,buff=.12);self.stages.append(b);self.add(b,lab)
  for a,b in zip(self.stages,self.stages[1:]):self.add(Line(a.get_bottom() if VERT else a.get_right(),b.get_top() if VERT else b.get_left(),color=GRAY).set_z_index(-1))
  self.pc=pill('PC = 2',3,.65,ORANGE,25).move_to([2.4,3.2,0] if VERT else [-4.2,1.9,0]);self.ctrl=pill('제어 비교',3,.7,GREEN,25).move_to([2.4,0,0] if VERT else [0,1.9,0]);self.add(self.pc,self.ctrl)
 def phase(self,stall=False):
  for b in self.stages:value(b,'—',GRAY);b[0].set_stroke(GRAY,width=1)
  for i,who,s in ([(1,'B','ID 유지'),(2,'','BUBBLE'),(3,'A','LOAD · [100]')] if stall else [(1,'B','ADD R3,R1,R2'),(2,'A','LOAD 주소100')]):
   c=BLUE if who=='A' else PURPLE if who=='B' else ORANGE;value(self.stages[i],who+' · '+s if who else s,c);self.stages[i][0].set_stroke(c,width=2.5)
  value(self.pc,'PC 유지' if stall else 'PC = 2',ORANGE);value(self.ctrl,'IF/ID 유지' if stall else '검사: R1 필요',GREEN)
 def completed(self):
  value(self.stages[1],'—',GRAY);value(self.stages[2],'B · 5 + 3 = 8',PURPLE);value(self.stages[3],'BUBBLE',ORANGE);value(self.stages[4],'A · R1 ← 5',BLUE);value(self.pc,'PC 진행',GREEN);value(self.ctrl,'MEM/WB → EX',GREEN)

def five(self):return self.centered(FiveStage(),7.9 if VERT else 14)

class ForwardUnit(VGroup):
 def __init__(self,showpath=False,mux=False,load=False):
  super().__init__();self.load=load
  pos={'reg':(-2,2.8),'saved':(2,2.8),'mux':(0,.7),'alu':(0,-1.3),'other':(-2.8,-1.3),'out':(2.8,-1.3)} if VERT else {'reg':(-4.4,1.2),'saved':(-4.4,-1.1),'mux':(-.9,0),'alu':(2.3,0),'other':(2.3,-1.8),'out':(5.5,0)}
  texts={'reg':'R1 = 0' if load else 'R3 = 0','saved':'데이터 미도착' if load else '결과 8','mux':'선택 전','alu':'계산 대기','other':'R2 = 3' if load else 'R5 = 2','out':'결과 —'}
  labels={'reg':'레지스터 파일','saved':'MEM/WB' if load else 'EX/MEM','mux':'입력 선택','alu':'ALU · 한 개','other':'다른 입력','out':'R3에 기록할 값' if load else 'R4에 기록할 값'}
  self.boxes={};self.labels={}
  for k,xy in pos.items():
   c=BLUE if k=='saved' else GREEN if k=='mux' else PURPLE if k=='out' else GRAY
   w=(3.5 if k in ['reg','saved'] else 2.2) if VERT else (3.2 if k in ['reg','saved'] else 2.35)
   b=pill(texts[k],w,.8,c,26).move_to([*xy,0]);lab=txt(labels[k],21,INK,w).next_to(b,UP,buff=.15);self.boxes[k]=b;self.labels[k]=lab;self.add(b,lab)
  def connect(a,b,color):
   u,v=self.boxes[a],self.boxes[b]
   if VERT and a in ['reg','saved']:st=u.get_bottom();en=v.get_top()+(LEFT if a=='reg' else RIGHT)*.45;mid=np.array([st[0],en[1]+.2,0]);return VMobject(stroke_color=color,stroke_width=2).set_points_as_corners([st,mid,en])
   st=u.get_right();en=v.get_left()+(UP if a=='reg' else DOWN)*.2;mid=np.array([en[0]-.25,st[1],0]);return VMobject(stroke_color=color,stroke_width=2).set_points_as_corners([st,mid,en])
  self.regpath=connect('reg','mux',GRAY);self.forwardpath=connect('saved','mux',GREEN);self.outputpath=connect('alu','out',PURPLE);self.muxpath=Line(self.boxes['mux'].get_bottom() if VERT else self.boxes['mux'].get_right(),self.boxes['alu'].get_top() if VERT else self.boxes['alu'].get_left(),color=GRAY);self.otherpath=Line(self.boxes['other'].get_right() if VERT else self.boxes['other'].get_top(),self.boxes['alu'].get_left() if VERT else self.boxes['alu'].get_bottom(),color=GRAY)
  self.add(self.regpath,self.forwardpath,self.outputpath,self.muxpath,self.otherpath)
  for l in [self.regpath,self.forwardpath,self.outputpath,self.muxpath,self.otherpath]:l.set_z_index(-1)
  if not showpath:self.forwardpath.set_stroke(opacity=0)
  if not mux:self.boxes['mux'].set_opacity(0);self.labels['mux'].set_opacity(0)
 def path(self):self.forwardpath.set_stroke(GREEN,width=3,opacity=1)
 def reveal_mux(self):
  b=self.boxes['mux'];b[0].set_stroke(GREEN,opacity=1);b[0].set_fill(PANEL,opacity=1);b[1].set_opacity(1);self.labels['mux'].set_opacity(1)
 def select(self,ready=True):
  self.reveal_mux();self.path()
  if not ready:
   value(self.boxes['mux'],'선택 보류',ORANGE);value(self.boxes['alu'],'필요한 값 대기',ORANGE);value(self.boxes['out'],'쓰기 없음',GRAY);return
  num=5 if self.load else 8;other=3 if self.load else 2;result=num+other if self.load else num-other
  value(self.boxes['saved'],f'데이터 {num}' if self.load else f'결과 {num}',BLUE);value(self.boxes['mux'],str(num),GREEN);value(self.boxes['alu'],f'{num} + {other}' if self.load else f'{num} − {other}',PURPLE);value(self.boxes['out'],str(result),PURPLE);self.muxpath.set_stroke(GREEN,width=3)

def unit(self,path=False,mux=False,load=False):return self.centered(ForwardUnit(path,mux,load),7.9 if VERT else 14)

def intro(self):
 p=five(self);p.phase();self.show(p);self.note('IF · ID · EX · MEM · WB의 교육용 5단계 구조');self.at(5);self.note('LOAD의 새 R1 → 다음 ADD가 필요로 하는 입력',ORANGE);self.play(Indicate(p.stages[1],color=PURPLE),Indicate(p.stages[2],color=BLUE),run_time=.6)
def load_goal(self):
 g=VGroup(pill('A : Memory[100] = 5',6,.9,BLUE,32),pill('현재 R1 = 0',6,.8,GRAY,31),pill('B : R1 + R2   ·   R2 = 3',6,.9,PURPLE,31)).arrange(DOWN,buff=.5);self.centered(g,7.5 if VERT else 11);self.show(g);self.note('R1에 새 값 5가 필요합니다',BLUE);self.at(15);self.note('기대하는 계산: 5 + 3 = 8',PURPLE);self.play(Indicate(g[2],color=PURPLE),run_time=.5)
def old_input(self):
 u=unit(self,False,True,True);self.show(u);value(u.boxes['mux'],'0 · 이전 값',RED);value(u.boxes['alu'],'0 + 3',PURPLE);u.regpath.set_stroke(RED,width=3);self.note('메모리 읽기가 아직 끝나지 않은 상황',ORANGE);self.at(22);self.play(Indicate(u.boxes['reg'],color=RED),run_time=.5);self.note('이 입력으로 계산하면 3 · 기대 결과는 8',RED);self.at(27);value(u.boxes['out'],'쓰기 없음',GRAY);self.note('ALU가 아니라 입력값의 준비 시점이 문제입니다',ORANGE)
def compare(self):
 a=pill('A의 목적지 : R1',4.5,.9,BLUE,31);b=pill('B의 입력 : R1 · R2',4.5,.9,PURPLE,30);g=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.7);comp=pill('번호 비교',4.5,.8,GREEN,31).next_to(g,DOWN,buff=.6);cond=txt('유효한 쓰기 · 실제 소스 사용 · 필요한 시점',25,ORANGE,7.3 if VERT else 12).next_to(comp,DOWN,buff=.5);allg=self.centered(VGroup(g,comp,cond),7.7 if VERT else 13);self.show(allg);self.note('명령어 해독 정보로 비교합니다');self.at(34);self.play(Indicate(a,color=BLUE),Indicate(b,color=PURPLE),run_time=.5);self.at(40);value(comp,'R1 = R1',GREEN);self.at(41);self.note('번호 일치 + 필요한 시점에 값이 없음 → 대기',ORANGE);self.play(Indicate(comp,color=GREEN),run_time=.5)
def stall(self):
 p=five(self);p.phase();self.show(p);self.note('A: EX · 주소 계산 / B: ID · R1 필요');self.at(51);self.play(Indicate(p.ctrl,color=GREEN),run_time=.5);self.at(53);p.phase(True);self.note('CLK ↑ : A는 MEM으로 · B와 PC는 유지',ORANGE);self.play(Indicate(p.stages[1],color=ORANGE),Indicate(p.stages[3],color=BLUE),run_time=.6);self.at(56);self.note('ID/EX에는 무효한 BUBBLE · 결과 기록 없음',ORANGE);self.at(59);self.note('Stall · 필요한 값을 기다리는 실행 지연',ORANGE)
def alu_example(self):
 a=pill('A : ADD R3, R1, R2',6,.9,BLUE,31);b=pill('B : SUB R4, R3, R5',6,.9,PURPLE,31);g=VGroup(a,b).arrange(DOWN,buff=.8);self.centered(g,7.5 if VERT else 11);self.show(g);self.note('지금부터 별도 예시 · 같은 ALU를 다른 클럭에 사용');self.at(67);self.note('R1=5 · R2=3 · R5=2 / A 결과8 → B 결과6',ORANGE);self.play(Indicate(a,color=BLUE),Indicate(b,color=PURPLE),run_time=.6)
def bypass_path(self):
 u=unit(self);self.show(u);self.note('앞선 클럭: A가 ALU에서 5 + 3 = 8 계산',BLUE);self.at(76);self.play(Indicate(u.boxes['saved'],color=BLUE),run_time=.5);self.at(78);self.note('EX/MEM에는 8 · 레지스터 R3는 아직 0');self.play(Indicate(u.boxes['reg'],color=GRAY),run_time=.5);self.at(81);self.note('다음 클럭의 B가 사용할 ALU 입력으로 연결한다',GREEN);self.at(85);u.path();self.play(Create(u.forwardpath),run_time=.8);self.note('기존 결과 저장 위치 → 동일 ALU의 입력 선택 위치',GREEN)
def mux(self):
 u=unit(self,True);self.show(u);self.note('입력 후보: 기존 R3=0 / 준비된 EX/MEM 결과8');self.at(93);u.reveal_mux();value(u.boxes['mux'],'0',GRAY);self.play(Indicate(u.boxes['mux'],color=GREEN),run_time=.5);self.at(97);u.select();self.play(ShowPassingFlash(u.forwardpath.copy().set_stroke(width=5),time_width=.4),run_time=.9);self.note('R3 기록 전에도 8 − 2 = 6 계산 가능',PURPLE);self.at(103);self.note('Forwarding / Bypassing · 준비된 결과 직접 전달',GREEN)
def load_limit(self):
 u=unit(self,True,True,True);self.show(u);u.select(False);self.note('경로가 있어도 값이 아직 없다면?');self.at(109);setlabel(u.labels['saved'],'EX/MEM · 주소',ORANGE,width=3);value(u.boxes['saved'],'주소 100',ORANGE);self.note('별도 LOAD → ADD 예시로 돌아옵니다');self.at(113);self.note('LOAD의 EX 결과는 주소100 · 필요한 피연산자는 데이터5',ORANGE);self.at(115);u.forwardpath.set_stroke(ORANGE,width=2);self.play(Indicate(u.boxes['saved'],color=ORANGE),run_time=.5);self.note('주소100을 데이터처럼 선택하지 않습니다',ORANGE);self.at(121);u.select(False);self.note('메모리 데이터가 준비될 때까지 대기',ORANGE)
def wait_forward(self):
 u=unit(self,True,True,True);u.select(False);self.show(u);self.note('Stall : 먼저 데이터를 기다림',ORANGE);self.at(126);value(u.boxes['saved'],'데이터 5',BLUE);u.select();self.note('CLK ↑ · MEM/WB의5 전달 → 5 + 3 = 8',GREEN);self.play(ShowPassingFlash(u.forwardpath.copy().set_stroke(width=5),time_width=.4),run_time=.8);self.at(129);self.note('메모리 읽기 1주기 예시 · 실제 대기 시간은 달라질 수 있음')
def integrate(self):
 p=five(self);p.phase(True);self.show(p);self.note('필요하면 대기 · 준비된 결과는 직접 전달',GREEN);self.at(133);p.completed();self.play(Indicate(p.ctrl,color=GREEN),Indicate(p.stages[2],color=PURPLE),run_time=.6);self.note('의존성 검사 + 갱신 제어 + ALU 입력 선택 경로')
def independent(self):
 a=pill('ADD R3, R1, R2',5.5,.8,BLUE,30);b=pill('SUB R4, R5, R6',5.5,.8,PURPLE,30);alu=pill('ALU 한 개',4,1,GREEN,34);g=VGroup(a,b,alu).arrange(DOWN,buff=.5);self.centered(g,7.5 if VERT else 11);self.show(g);self.note('서로의 결과를 사용하지 않는 두 명령어');self.at(139);self.play(Indicate(alu,color=GREEN),run_time=.5);self.note('독립적인 계산에도 하나의 ALU만 사용해야 할까?',ORANGE);self.at(143);outline=DashedVMobject(alu[0].copy().set_fill(opacity=0),num_dashes=24).next_to(alu,RIGHT,buff=.45)
 if outline.get_right()[0]>config.frame_width/2-.3:outline.scale(.7).next_to(alu,DOWN,buff=.3)
 self.show(outline);self.at(145);self.note('계산 회로를 하나 더 배치한다면?')
for n in ['intro','load_goal','old_input','compare','stall','alu_example','bypass_path','mux','load_limit','wait_forward','integrate','independent']:setattr(MemoryScene,n,globals()[n])
