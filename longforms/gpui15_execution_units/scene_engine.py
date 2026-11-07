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
  self.add(txt('GPU 개론  /  15',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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




from check_logic import INITIAL,A,B,alu,execute,write_edge

def value(box,s,color=INK):
 t=txt(s,27,color);t.scale_to_fit_height(box[0].height*(.035 if s.strip()=='—' else .42))
 if t.width>box[0].width*.9:t.scale_to_fit_width(box[0].width*.9)
 box[1].become(t.move_to(box[0]))
def pair_cards():
 a=VGroup(pill('A : ADD R3, R1, R2',5.7,.85,BLUE,30),pill('R1=5 · R2=3 → R3=8',5.7,.75,BLUE,29)).arrange(DOWN,buff=.2)
 b=VGroup(pill('B : SUB R6, R4, R5',5.7,.85,PURPLE,30),pill('R4=9 · R5=2 → R6=7',5.7,.75,PURPLE,29)).arrange(DOWN,buff=.2)
 return VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.8)

class DualPath(VGroup):
 def __init__(self,reads=2,writes=1,connected=False,outputs=False):
  super().__init__();self.state=dict(INITIAL);self.results=[];self.ports=[];self.inputs=[];self.controls=[];self.alus=[];self.buffers=[];self.writeports=[];self.wires=[];self.outwires=[];self.labels=[]
  self.rf=pill('R1=5  R2=3  R4=9  R5=2' if VERT else 'R1=5 · R2=3\nR4=9 · R5=2',7.4 if VERT else 3.3,.85 if VERT else 2.6,BLUE,28).move_to([0,3.7,0] if VERT else [-5.8,0,0]);self.add(self.rf,txt('Register File',24,INK).next_to(self.rf,UP,buff=.2))
  for i,(r,v) in enumerate([(1,5),(2,3),(4,9),(5,2)]):
   xy=(-2.7+i*1.8,2.5) if VERT else (-3.1,1.4-i*.9)
   b=pill(f'R{r}:{v}',1.6 if VERT else 1.7,.6,BLUE if i<2 else GREEN,24).move_to([*xy,0]);self.ports.append(b);self.add(b)
   line=Line(self.rf.get_bottom() if VERT else self.rf.get_right(),b.get_top() if VERT else b.get_left(),color=GRAY,stroke_width=1.5);self.add(line.set_z_index(-1));self.inputs.append(line)
  for i in range(2):
   c=BLUE if i==0 else PURPLE;x=-2 if i==0 else 2
   control=pill('Operation ?',3.4 if VERT else 2.9,.6,ORANGE,25).move_to([x,1.3,0] if VERT else [.3,2 if i==0 else -1,0])
   alub=pill('ADD / SUB',3.4 if VERT else 2.9,.9,GREEN if i else BLUE,30).move_to([x,0,0] if VERT else [.3,1 if i==0 else -2,0]);label=txt(f'ALU {i} · ADD/SUB',21,INK,3.4).next_to(alub,UP if VERT else DOWN,buff=.12)
   buf=pill('—',3.4 if VERT else 2.8,.8,GREEN,27).move_to([x,-1.5,0] if VERT else [3.55,1 if i==0 else -2,0]);bl=txt(f'Result {i} · 목적지 보관',20,GREEN,3.2).next_to(buf,UP,buff=.12)
   wp=pill(f'Write {i}',3.4 if VERT else 2.4,.65,BLUE if i==0 else GREEN,25).move_to([x,-2.8,0] if VERT else [6.4,1 if i==0 else -2,0])
   self.controls.append(control);self.alus.append(alub);self.buffers.append(buf);self.writeports.append(wp);self.labels.extend([label,bl]);self.add(control,alub,label,buf,bl,wp)
   for port in self.ports[i*2:i*2+2]:
    st=port.get_bottom() if VERT else port.get_right();en=alub.get_top()+(LEFT if port is self.ports[i*2] else RIGHT)*.5 if VERT else alub.get_left()+(UP if port is self.ports[i*2] else DOWN)*.2
    path=VMobject(stroke_color=c,stroke_width=2).set_points_as_corners([st,np.array([st[0],en[1]+.2,0]) if VERT else np.array([en[0]-.2,st[1],0]),en]);self.wires.append(path);self.add(path.set_z_index(-1))
   ctl=Line(control.get_bottom(),alub.get_top(),color=ORANGE,stroke_width=2);self.add(ctl.set_z_index(-1));self.wires.append(ctl)
   out=Line(alub.get_bottom() if VERT else alub.get_right(),buf.get_top() if VERT else buf.get_left(),color=c,stroke_width=2);write=Line(buf.get_bottom() if VERT else buf.get_right(),wp.get_top() if VERT else wp.get_left(),color=c,stroke_width=2);self.add(out.set_z_index(-1),write.set_z_index(-1));self.outwires.extend([out,write])
   if not outputs:buf.set_opacity(0);bl.set_opacity(0);out.set_stroke(opacity=0);write.set_stroke(opacity=0);wp.set_opacity(0)
  self.summary=pill('R3 = 0   ·   R6 = 0',7.4 if VERT else 6.5,.65,GRAY,27).move_to([0,-4,0] if VERT else [1.9,-3.25,0]);self.add(self.summary)
  self.outputs=outputs;self.set_reads(reads);self.set_writes(writes)
  if not connected:
   for l in self.wires:l.set_stroke(opacity=0)
   for l in self.inputs:l.set_stroke(opacity=0)
  else:self.connect(reads)
 def set_reads(self,n):
  self.read_count=n
  for i,(b,l) in enumerate(zip(self.ports,self.inputs)):
   b[0].set_stroke(opacity=1 if i<n else 0);b[0].set_fill(opacity=1 if i<n else 0);b[1].set_opacity(1 if i<n else 0);l.set_stroke(opacity=1 if i<n else 0)
 def connect(self,reads=4):
  self.set_reads(reads)
  for i,l in enumerate(self.wires):
   lane=i//3;l.set_stroke(opacity=1 if lane==0 or reads>=4 else 0)
  value(self.controls[0],'ADD',ORANGE);value(self.controls[1],'SUB',ORANGE)
 def expose_outputs(self):
  self.outputs=True
  for b in self.buffers:b[0].set_stroke(opacity=1);b[0].set_fill(PANEL,opacity=1);b[1].set_opacity(1)
  for label in [self.labels[1],self.labels[3]]:label.set_opacity(1)
  for l in self.outwires:l.set_stroke(opacity=1)
  self.set_writes(self.write_count)
 def set_writes(self,n):
  self.write_count=n
  for i,b in enumerate(self.writeports):
   active=self.outputs and i<n;b[0].set_stroke(opacity=1 if active else 0);b[0].set_fill(PANEL,opacity=1 if active else 0);b[1].set_opacity(1 if active else 0)
   self.outwires[i*2+1].set_stroke(opacity=1 if active else 0)
 def compute(self):
  self.results=execute(self.state,[A,B],self.read_count)
  for i,b in enumerate(self.alus):
   c=BLUE if i==0 else PURPLE
   if i<len(self.results):value(b,'5 + 3 = 8' if i==0 else '9 − 2 = 7',c)
   else:value(b,'입력 대기',ORANGE)
 def capture(self):
  self.expose_outputs()
  for i,b in enumerate(self.buffers):
   if i<len(self.results):r=self.results[i];value(b,f'{r["value"]} · 목적지 R{r["dest"]}',BLUE if i==0 else PURPLE)
   else:value(b,'—',GRAY)
 def write_edge(self):
  self.state,self.results=write_edge(self.state,self.results,self.write_count);value(self.summary,f'R3 = {self.state[3]}   ·   R6 = {self.state[6]}',GREEN)
  for i,b in enumerate(self.writeports):
   if i<self.write_count:value(b,'CLK ↑ · R3' if i==0 else 'CLK ↑ · R6',BLUE if i==0 else PURPLE)

def circuit(self,reads=2,writes=1,connected=False,outputs=False):return self.centered(DualPath(reads,writes,connected,outputs),7.9 if VERT else 14.2)

def intro(self):
 old=VGroup(pill('LOAD R1,[100]',5.5,.8,BLUE,30),pill('ADD R3,R1,R2',5.5,.8,PURPLE,30)).arrange(DOWN,buff=.7);line=Line(old[0].get_bottom(),old[1].get_top(),color=ORANGE);g=self.centered(VGroup(old,line),7.6 if VERT else 11);self.show(g);self.note('앞선 결과가 필요한 관계');self.at(6);new=self.centered(pair_cards(),7.6 if VERT else 13.5);self.replace(g,new);self.note('새 예시: 서로의 결과를 사용하지 않습니다')
def independent(self):
 g=self.centered(pair_cards(),7.6 if VERT else 13.5);self.show(g);self.note('입력 R1/R2와 R4/R5 · 목적지 R3와 R6');self.at(17);self.play(Indicate(g[0],color=BLUE),run_time=.45);self.at(19);self.play(Indicate(g[1],color=PURPLE),run_time=.45);self.note('ADD → SUB : R3=8 · R6=7');self.at(21);self.play(Indicate(g[1],color=PURPLE),Indicate(g[0],color=BLUE),run_time=.6);self.note('SUB → ADD : 동일한 R3=8 · R6=7',GREEN)
def single(self):
 a=pill('A : 5 + 3',4.5,.8,BLUE,31);b=pill('B : 9 − 2',4.5,.8,PURPLE,31);alu0=pill('ALU 한 개',5,1,GREEN,37);g=VGroup(a,b,alu0).arrange(DOWN,buff=.5);self.centered(g,7.5 if VERT else 11);self.show(g);self.note('두 명령어는 이미 실행 준비 완료');self.at(28);value(alu0,'ADD : 5 + 3 = 8',BLUE);self.play(Indicate(a,color=BLUE),run_time=.5);self.note('A가 ALU 사용 중 · B는 대기',ORANGE);self.at(31);value(alu0,'SUB : 9 − 2 = 7',PURPLE);self.play(Indicate(b,color=PURPLE),run_time=.5);self.note('한 입력·제어 세트로 한 번에 한 연산')
def duplicate(self):
 a=pill('ALU 0 · ADD / SUB',5,.95,BLUE,32);b=pill('ALU 1 · ADD / SUB',5,.95,GREEN,32);g=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.9);self.centered(g,7.5 if VERT else 13);self.show(a);self.note('기존 ALU를 재사용해 실행 자원을 하나 더 만듭니다');self.at(38);self.play(FadeIn(b),run_time=.6);self.at(43);self.play(Indicate(a,color=BLUE),Indicate(b,color=GREEN),run_time=.6);self.note('두 ALU 모두 ADD와 SUB 지원 · 아직 경로 연결 전',GREEN)
def potential(self):
 a=pill('ALU 0 : 5 + 3 → 8',5.5,1.1,BLUE,32);b=pill('ALU 1 : 9 − 2 → 7',5.5,1.1,PURPLE,32);g=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.9);self.centered(g,7.6 if VERT else 13);self.show(g);self.note('두 ALU가 있다면 가능한 동작 · 아직 연결 전 예시');self.play(Indicate(a,color=BLUE),Indicate(b,color=PURPLE),run_time=.7);self.at(54);value(a,'ALU 0 : 입력 ?',ORANGE);value(b,'ALU 1 : 입력 ?',ORANGE);self.note('각각의 숫자와 제어 정보는 어디서 가져올까?',ORANGE)
def inputs(self):
 p=circuit(self);self.show(p);self.note('각 ALU : 피연산자 두 개 + 연산 제어');self.at(61);self.play(Indicate(p.controls[0],color=ORANGE),Indicate(p.controls[1],color=ORANGE),run_time=.5);self.at(64);p.connect(2);self.note('기존 읽기 포트 2개 → 한 계산의 두 입력',BLUE);self.at(67);p.connect(4);self.play(Indicate(p.ports[2],color=GREEN),Indicate(p.ports[3],color=GREEN),run_time=.6);self.note('읽기 포트 4개로 확장 · 두 ALU에 독립적인 입력 전달',GREEN)
def outputs(self):
 p=circuit(self,4,1,True);self.show(p);p.compute();self.note('두 ALU가 같은 클럭 구간에 결과8과7 생성');self.at(72.5);p.capture();self.play(Indicate(p.buffers[0],color=BLUE),Indicate(p.buffers[1],color=PURPLE),run_time=.5);self.note('결과8/R3 · 결과7/R6를 각각 보관',GREEN);self.at(74.3);self.note('쓰기 포트 한 개면 한 에지에 두 결과 기록 불가',ORANGE);self.at(75.5);p.set_writes(2);self.play(Indicate(p.writeports[1],color=GREEN),run_time=.45);self.at(76.3);p.write_edge();self.note('CLK ↑ : 쓰기 포트 2개 → R3=8 · R6=7',GREEN)
def complete(self):
 p=circuit(self,4,2,True,True);self.show(p);p.compute();p.capture();self.note('독립적인 두 명령어의 입력과 출력까지 연결');self.at(80);p.write_edge();self.play(Indicate(p.summary,color=GREEN),run_time=.5);self.at(83);self.note('다중 실행 유닛 구조 · Multiple Execution Units',GREEN);self.at(86);self.play(Indicate(p.alus[1],color=GREEN),run_time=.5);self.note('같은 실행 단계 안의 여러 회로 · 자동 두 명령어 공급은 별도')
def dependency(self):
 a=pill('ALU 0 : ADD R3,R1,R2',6,.9,BLUE,31);b=pill('ALU 1 : SUB R4,R3,R5',6,.9,PURPLE,31);g=VGroup(a,b).arrange(DOWN,buff=1);line=Line(a.get_bottom(),b.get_top(),color=ORANGE);self.centered(VGroup(g,line),7.7 if VERT else 12);self.show(g,line);self.note('독립적인 작업이 없으면 두 회로를 모두 활용하기 어렵습니다');self.at(93);self.note('회로 수가 두 배라고 프로그램 전체 속도가 두 배는 아님',ORANGE);self.at(95);value(a,'A : R3의 새 결과 생성 중',BLUE);value(b,'B : 새 R3 값 대기',ORANGE);self.play(Indicate(b,color=ORANGE),run_time=.6);self.note('이번에는 B가 A의 결과를 사용하는 별도 예시')
def resources(self):
 p=circuit(self,2,1,True);self.show(p);p.compute();self.note('읽기 포트가 2개뿐이면 두 번째 ALU의 입력이 부족',ORANGE);self.at(104);p.connect(4);p.compute();p.capture();self.note('읽기 확장 후에도 쓰기 한 포트라면 기록 단계에 제약',ORANGE);self.at(107);p.write_edge();self.note('R3=8 기록 · R6 결과7은 별도 버퍼에 유지',PURPLE);self.at(110);p.set_writes(2);p.state=dict(INITIAL);p.compute();p.capture();p.write_edge();self.note('읽기·결과 보관·기록 경로와 제어를 함께 확장',GREEN)
def integrate(self):
 p=circuit(self,4,2,True,True);p.compute();p.capture();p.write_edge();self.show(p);self.note('명령어 중첩 + 여러 실행 회로 + 데이터 공급/기록');self.at(118);self.play(Indicate(p.alus[0],color=BLUE),Indicate(p.alus[1],color=PURPLE),run_time=.6);self.note('동시 처리 가능성은 주변 자원과 제어에도 달려 있습니다')
def assign(self):
 texts=['ADD R3, R1, R2','SUB R6, R4, R5','ADD R7, R3, R8','SUB R9, R10, R11'];cards=VGroup(*[pill(t,6.6,.7,[BLUE,PURPLE,ORANGE,GREEN][i],27) for i,t in enumerate(texts)]).arrange(DOWN,buff=.25);alus=VGroup(pill('ALU 0',3,.85,BLUE,31),pill('ALU 1',3,.85,GREEN,31)).arrange(RIGHT,buff=.6).next_to(cards,DOWN,buff=.8);g=self.centered(VGroup(cards,alus),7.7 if VERT else 12);self.show(g);self.note('여러 명령어가 대기 중 · 배정 회로는 아직 없음');self.at(126);self.play(Indicate(alus[0],color=BLUE),Indicate(alus[1],color=GREEN),run_time=.5);self.note('어떤 명령어를 어느 회로로 보낼까?',ORANGE);self.at(130);cards[2][0].set_stroke(ORANGE,width=3);cards[3][0].set_stroke(GREEN,width=3);self.note('세 번째는 R3 대기 / 네 번째는 독립적인 입력 준비');self.at(134);self.play(Indicate(cards[2],color=ORANGE),Indicate(cards[3],color=GREEN),run_time=.6);self.at(136);self.note('필요한 데이터와 실행 자원을 보고 선택한다면?')
for n in ['intro','independent','single','duplicate','potential','inputs','outputs','complete','dependency','resources','integrate','assign']:setattr(MemoryScene,n,globals()[n])
