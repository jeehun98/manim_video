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
  self.add(txt('GPU 개론  /  3부 마무리',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  self.add(base,bar,txt(f'{self.index+1:02} / 13',17,GRAY).move_to([x-.55,y+(.27 if VERT else -.2),0]).set_z_index(32))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)




from shared_components import DualMemory,FiveStage,ForwardUnit,DualPath,value

class Core(VGroup):
 def __init__(self,level=0):
  super().__init__();self.nodes={};self.labels={};self.edges=[];self.level_number=level
  pos={'pc':(-2.6,3.1),'im':(0,3.1),'dec':(2.6,3.1),'reg':(-2.6,1.2),'alu':(0,1.2),'result':(2.6,1.2),'state':(-2.6,-.7),'pipe':(0,-.7),'mem':(2.6,-.7),'ctrl':(-2.6,-2.6),'hazard':(0,-2.6),'alu2':(2.6,-2.6)} if VERT else {'pc':(-5.6,1.8),'im':(-2.8,1.8),'dec':(0,1.8),'ctrl':(2.8,1.8),'reg':(-4.2,0),'alu':(-1.4,0),'result':(1.4,0),'mem':(4.2,0),'state':(-4.2,-1.8),'pipe':(-1.4,-1.8),'hazard':(1.4,-1.8),'alu2':(4.2,-1.8)}
  labels={'pc':'명령어 주소','im':'명령어 메모리','dec':'해독 회로','reg':'레지스터 파일','alu':'ALU 0','result':'결과 보관','mem':'데이터 메모리','state':'실행 상태','ctrl':'제어 논리','pipe':'단계 사이 저장','hazard':'준비 시점 제어','alu2':'ALU 1'}
  texts={'pc':'PC = 0','im':'ADD R3,R1,R2','dec':'입력 · 연산 · 목적지','reg':'R1=5 · R2=3','alu':'5 + 3','result':'R3 ← 8','mem':'100:5 · 102:0','state':'00 → 01 → 10 → 11','ctrl':'상태 → 동작','pipe':'명령 · 데이터 · 목적지','hazard':'대기 / 직접 전달','alu2':'9 − 2 → R6'}
  self.groups=[['pc','im','dec','reg','alu','result'],['mem'],['state','ctrl'],['pipe'],['hazard'],['alu2']]
  for k,xy in pos.items():
   b=pill(texts[k],2.35 if VERT else 2.5,.8,GRAY,24).move_to([*xy,0]);lab=txt(labels[k],19,GRAY,2.4).next_to(b,UP,buff=.13);self.nodes[k]=b;self.labels[k]=lab;self.add(b,lab)
  for a,b,feature in [('pc','im',0),('im','dec',0),('reg','alu',0),('alu','result',0),('result','mem',1),('dec','ctrl',2),('ctrl','state',2),('state','pipe',3),('pipe','hazard',4),('hazard','alu2',5)]:
   u,v=self.nodes[a],self.nodes[b];d=v.get_center()-u.get_center()
   st=u.get_right() if abs(d[0])>.5 else u.get_bottom();en=v.get_left() if abs(d[0])>.5 else v.get_top()
   l=Line(st,en,color=GRAY,stroke_width=1.5).set_z_index(-1);self.add(l);self.edges.append((feature,l))
  self.set_level(level)
  if level>=2:self.val('mem','100:5 · 102:8',PURPLE)
 def val(self,k,s,c=INK):value(self.nodes[k],s,c)
 def set_level(self,n):
  self.level_number=n
  visible=sum(self.groups[:n+1],[])
  for k,b in self.nodes.items():
   show=k in visible;b[0].set_stroke(GRAY,opacity=1 if show else 0);b[0].set_fill(PANEL,opacity=1 if show else 0);b[1].set_opacity(1 if show else 0);self.labels[k].set_opacity(1 if show else 0)
  for feature,line in self.edges:line.set_stroke(opacity=1 if feature<=n else 0)
  if n>=3:self.val('ctrl','단계별 제어',ORANGE);self.val('state','각 단계의 유효 상태',ORANGE)
 def highlight(self,n):
  for k,b in self.nodes.items():
   if any(k in g for g in self.groups[:self.level_number+1]):b[0].set_stroke(GREEN if k in self.groups[n] else GRAY,width=3 if k in self.groups[n] else 1.2)
  for feature,l in self.edges:l.set_stroke(GREEN if feature==n else GRAY,width=3 if feature==n else 1.5)

def core(self,level=0):return self.centered(Core(level),7.9 if VERT else 14)
def zoom(self,o,w=None):return self.centered(o,w or (7.8 if VERT else 14))

class PipelineView(VGroup):
 def __init__(self):
  super().__init__();self.stages=[];self.regs=[]
  for i,s in enumerate(['IF · 인출','ID · 해독','EX · ALU 한 개','MEM · 읽기','WB · 기록']):
   xy=(-1.4,3.3-i*1.65) if VERT else (-5.6+i*2.8,.8)
   b=pill('—',3 if VERT else 2.5,.85,GRAY,25).move_to([*xy,0]);self.stages.append(b);self.add(b,txt(s,21,INK,3).next_to(b,UP,buff=.12))
  for i in range(4):
   xy=(1.9,2.48-i*1.65) if VERT else (-4.2+i*2.8,-.8)
   b=pill('—',3 if VERT else 2.5,.7,GREEN,23).move_to([*xy,0]);self.regs.append(b);self.add(b)
   a,c=self.stages[i],self.stages[i+1]
   self.add(Line(a.get_bottom() if VERT else a.get_right(),b.get_top(),color=GRAY).set_z_index(-1),Line(b.get_bottom(),c.get_top() if VERT else c.get_left(),color=GRAY).set_z_index(-1))
 def show_packets(self):
  value(self.stages[0],'B : ADD R3',PURPLE);value(self.stages[3],'A : [100] → 5',BLUE)
  value(self.regs[2],'A : 100 · R1 · 읽기',BLUE);value(self.regs[0],'—',GRAY)
 def advance(self):
  value(self.regs[0],'B : R1 · R2 → R3',PURPLE)
  value(self.stages[0],'—',GRAY);value(self.stages[1],'B : R1/R2 읽기',PURPLE);value(self.stages[3],'—',GRAY);value(self.stages[4],'A : R1 ← 5',BLUE);value(self.regs[2],'—',GRAY);value(self.regs[3],'A : 5 · R1 · 기록',BLUE)

def basic(self):
 p=core(self);self.show(p);self.note('기본 프로세서 · 하나의 명령어를 실행');self.at(3);self.play(Indicate(p.nodes['alu'],color=BLUE),run_time=.5);self.at(6);p.val('result','R3 = 8',BLUE);self.play(Indicate(p.nodes['reg'],color=BLUE),Indicate(p.nodes['result'],color=BLUE),run_time=.5)
def memory(self):
 p=core(self);p.val('reg','R1=0 · R2=3',GRAY);p.val('alu','입력 준비 전',GRAY);p.val('result','R3 = 0',GRAY);self.show(p);self.note('필요한 값5는 레지스터 바깥 Memory[100]에 있습니다');self.at(14);p.set_level(1);p.highlight(1);self.play(Indicate(p.nodes['mem'],color=GREEN),run_time=.6);self.at(18);p.val('im','LOAD R1,[100]',BLUE);p.val('reg','R1=5 · R2=3',BLUE);self.note('메모리 → 레지스터 → 계산 → 메모리',GREEN);self.at(19);p.val('pc','PC = 1',ORANGE);p.val('im','ADD R3,R1,R2',BLUE);p.val('alu','5 + 3 = 8',BLUE);p.val('result','R3 = 8',BLUE);self.at(20);p.val('pc','PC = 2',ORANGE);p.val('im','STORE R3,[102]',BLUE);p.val('mem','100:5 · 102:8',PURPLE)
def sequence(self):
 p=core(self,1);p.val('im','LOAD R1,[100]',BLUE);self.show(p);self.note('인출 → 주소 결정 → 데이터 읽기 → 결과 기록')
 for t,k in [(23,'im'),(25,'alu'),(27,'mem'),(28.5,'reg')]:
  self.at(t);self.play(Indicate(p.nodes[k],color=ORANGE),run_time=.4)
 self.at(30);p.set_level(2);p.highlight(2);self.note('상태 레지스터 + 제어 논리 · FSM',GREEN)
 for t,bits,target in [(31,'00','im'),(32.1,'01','alu'),(33.2,'10','mem'),(34.3,'11','reg')]:
  self.at(t);p.val('state',bits,GREEN);p.val('ctrl',{'00':'명령어 인출','01':'주소 결정','10':'데이터 읽기','11':'결과 기록'}[bits],ORANGE);self.play(Indicate(p.nodes[target],color=GREEN),run_time=.35)
 self.at(36);self.note('클럭 경계마다 상태 갱신 · 다중 사이클 실행',GREEN);p.val('state','00 · 다음 명령어',GREEN)
def simultaneous(self):
 p=core(self,2);self.show(p);self.note('실행 순서를 제어하는 구조에서 새로운 가능성으로');self.at(43);d=zoom(self,DualMemory());self.replace(p,d);self.note('명령어 인출과 데이터 읽기는 독립적인 접근 경로');self.at(48);d.concurrent();value(d.im,'B : ADD R3,R1,R2',PURPLE);self.play(Indicate(d.im,color=PURPLE),Indicate(d.dm,color=BLUE),run_time=1);self.note('A 데이터 읽기 / B 인출 · 다음 단계 사용 시점은 별도 제어')
def pipeline(self):
 p=core(self,2);self.show(p);p.set_level(3);p.highlight(3);self.note('전역 단일 단계 선택에서 단계별 동시 제어로 확장',ORANGE);self.at(56);v=zoom(self,PipelineView());v.show_packets();self.replace(p,v);self.note('단계마다 해당 명령어의 데이터·목적지·제어 보관',GREEN);self.at(60);v.advance();self.play(Indicate(v.stages[1],color=PURPLE),Indicate(v.stages[4],color=BLUE),run_time=.6);self.note('서로 다른 단계 동시 사용 · EX의 ALU는 아직 한 개');self.at(64);self.note('파이프라인 · 서로 다른 명령어의 실행 단계를 겹친다',GREEN)
def dependency(self):
 a=pill('A : LOAD R1,[100]',6,.9,BLUE,31);b=pill('B : ADD R3,R1,R2',6,.9,PURPLE,31);g=VGroup(a,b).arrange(DOWN,buff=.9);line=Line(a.get_bottom(),b.get_top(),color=ORANGE);zoom(self,VGroup(g,line));self.show(g,line);self.note('A의 목적지 R1 = B가 사용할 입력 R1',ORANGE);self.at(70);value(b,'이전 값 0 + 3 → 3 ?',ORANGE);self.note('필요한 새 값은5 · 기대 결과는 5+3=8',ORANGE);self.play(Indicate(b,color=ORANGE),run_time=.5)
def stall(self):
 p=core(self,3);self.show(p);p.set_level(4);p.highlight(4);self.note('의존성과 값의 준비 시점을 검사한다',GREEN);self.at(77);f=zoom(self,FiveStage());f.phase();self.replace(p,f);self.at(78);f.phase(True);self.play(Indicate(f.stages[1],color=ORANGE),Indicate(f.stages[3],color=BLUE),run_time=.5);self.note('Stall : A는 진행 · B/PC는 유지 · EX에는 무효 Bubble',ORANGE)
def forward(self):
 u=zoom(self,ForwardUnit(True,True));self.show(u);self.note('별도 예시: ADD R3의8 → SUB R4,R3,R5',BLUE);self.at(84);self.play(Indicate(u.boxes['saved'],color=BLUE),run_time=.5);self.at(85);u.select();self.play(ShowPassingFlash(u.forwardpath.copy().set_stroke(width=5),time_width=.4),run_time=.8);self.note('R3=0이어도 준비된8을 선택 · 8−2=6',GREEN);self.at(89);p=core(self,4);p.highlight(4);self.replace(u,p);self.note('값이 없으면 대기 · 준비된 결과는 직접 전달')
def single(self):
 p=core(self,4);self.show(p);self.play(Indicate(p.nodes['alu'],color=BLUE),run_time=.5);self.note('여기까지는 ALU 한 개');self.at(98);a=pill('A : 5 + 3 → R3=8',6,.9,BLUE,31);b=pill('B : 9 − 2 → R6=7',6,.9,PURPLE,31);alu0=pill('같은 ALU를 번갈아 사용',6,.85,GRAY,29);g=zoom(self,VGroup(a,b,alu0).arrange(DOWN,buff=.5));self.replace(p,g);self.note('별도 독립 명령어 ADD와 SUB · 서로의 결과를 사용하지 않음')
def multiple(self):
 p=core(self,4);self.show(p);p.set_level(5);p.highlight(5);self.note('두 번째 ALU + 각각의 입력·제어·결과 경로',GREEN);self.at(106);d=zoom(self,DualPath(4,2,True,True));self.replace(p,d);d.compute();self.at(108);d.capture();self.note('각 결과와 목적지 보관: 8/R3 · 7/R6',GREEN);self.at(110);d.write_edge();self.play(Indicate(d.summary,color=GREEN),run_time=.5);self.note('같은 시간의 독립 계산 · 두 명령어는 이미 준비된 예시')
def cumulative(self):
 p=core(self,5);self.show(p);self.note('기본 프로세서에서 다섯 번의 구조 확장')
 for t,n,label in [(114.7,1,'① 메모리와 Load/Store 경로'),(116.2,2,'② 실행 상태와 제어 논리'),(117.7,3,'③ 단계별 저장과 동시 실행'),(119.2,4,'④ 의존성 검사·Stall·Forwarding'),(120.7,5,'⑤ 여러 ALU와 입력·출력 경로')]:
  self.at(t);p.highlight(n);self.note(label,GREEN);self.play(*[Indicate(p.nodes[k],color=GREEN) for k in p.groups[n]],run_time=.4)
 self.at(122);self.note('하나의 명령어 실행 → 여러 명령어의 작업 중첩',GREEN)

class Limits(VGroup):
 def __init__(self):
  super().__init__();self.units=VGroup(*[pill(f'ALU {i}',1.6,.7,BLUE if i<2 else GRAY,24).move_to([(i%4-1.5)*1.9,1.7-(i//4)*1.05,0]) for i in range(8)])
  self.feed=pill('유한한 데이터 공급',6.6,.75,ORANGE,29).move_to([0,-1.6,0]);self.add(self.units,self.feed)
  for i in range(4):self.add(Line(self.feed.get_top(),self.units[i].get_bottom(),color=GRAY,stroke_width=1).set_z_index(-1))
  for i,b in enumerate(self.units):b.set_opacity(1 if i<2 else 0)
  self.caption=txt('준비된 독립 작업은 두 개뿐인 예시',25,ORANGE,7.5).move_to([0,-2.5,0]);self.add(self.caption)
 def expand(self,count=8):
  for i,b in enumerate(self.units):
   b[0].set_stroke(BLUE if i<2 else GRAY,width=3 if i<2 else 1);value(b,'연산 중' if i<2 else '대기',BLUE if i<2 else GRAY);b.set_opacity(1 if i<count else 0)

def limits(self):
 p=zoom(self,Limits());self.show(p);self.note('계산 회로의 수 ≠ 항상 같은 비율의 성능 향상');self.at(126);p.expand(4);self.at(127);p.expand(8);self.at(128);self.play(Indicate(p.units[6],color=GRAY),run_time=.4);self.at(129);value(p.units[0],'R3 생성',BLUE);value(p.units[2],'R3 대기',ORANGE);value(p.units[3],'데이터 대기',ORANGE);a=p.units[0].get_top();b=p.units[2].get_top();link=VMobject(stroke_color=ORANGE,stroke_width=2).set_points_as_corners([a,a+UP*.35,np.array([b[0],a[1]+.35,0]),b]);self.add(link);self.note('앞선 결과를 기다리는 작업 + 유한한 데이터 공급',ORANGE);self.play(Indicate(p.feed,color=ORANGE),run_time=.6);self.at(132);self.note('회로가 남아 있어도 필요한 값이 없다면 계산할 수 없습니다')
def ending(self):
 p=core(self,5);self.show(p);p.highlight(5);p.val('alu2','입력 준비 대기',ORANGE);self.note('계산 회로를 늘리는 것만으로 충분할까?',ORANGE);self.at(138);self.play(Indicate(p.nodes['hazard'],color=ORANGE),Indicate(p.nodes['mem'],color=ORANGE),run_time=.6)
for n in ['basic','memory','sequence','simultaneous','pipeline','dependency','stall','forward','single','multiple','cumulative','limits','ending']:setattr(MemoryScene,n,globals()[n])
