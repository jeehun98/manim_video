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
  self.add(txt('GPU 개론  /  12',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/153)))
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




class Circuit(VGroup):
 def __init__(self,stored=False):
  super().__init__();self.nodes={};self.wires={}
  positions={'im':(-3.6,1.6),'ir':(0,1.6),'dec':(3.6,1.6),'alu':(-3.6,0),'addr':(0,0),'mem':(3.6,0),'data':(3.6,-1.6),'mux':(0,-1.6),'reg':(-3.6,-1.6)}
  labels={'im':'명령어 메모리','ir':'명령어 보관','dec':'Decoder','alu':'ALU','addr':'주소 보관','mem':'Data Memory','data':'읽은 값 보관','mux':'Writeback MUX','reg':'Register File'}
  for k,(x,y) in positions.items():
   c=GREEN if k in ['ir','addr','data'] else PURPLE if k=='mem' else BLUE
   value={'im':'LOAD R1, [100]','ir':'LOAD R1, [100]' if stored else '—','dec':'LOAD · 100 · R1','alu':'주소 선택','addr':'100' if stored else '—','mem':'100 : 5','data':'—','mux':'Memory','reg':'R1 = 0'}[k]
   box=pill(value,2.9,.7,c,24).move_to([x,y,0]);label=txt(labels[k],19,c,2.9).next_to(box,UP,buff=.12)
   self.nodes[k]=box;self.add(box,label)
  for a,b in [('im','ir'),('ir','dec'),('alu','addr'),('addr','mem'),('mem','data'),('data','mux'),('mux','reg')]:
   u,v=self.nodes[a],self.nodes[b];horizontal=abs(u.get_x()-v.get_x())>1
   st=u.get_right() if v.get_x()>u.get_x() else u.get_left()
   en=v.get_left() if v.get_x()>u.get_x() else v.get_right()
   if not horizontal:st=u.get_bottom();en=v.get_top()
   line=Line(st,en,color=GRAY,stroke_width=2);self.wires[(a,b)]=line;self.add(line)
  # Destination and opcode stay in IR while the address and data move below.
  self.status=txt('IRWrite=0  ·  RegWrite=0',22,ORANGE).move_to([0,-2.65,0]);self.add(self.status)
 def val(self,k,s,c=INK):
  box=self.nodes[k];new=txt(s,26,c)
  new.scale_to_fit_height(box[0].height*.43)
  if new.width>box[0].width*.9:new.scale_to_fit_width(box[0].width*.9)
  box[1].become(new.move_to(box[0]))
 def status_text(self,s):setlabel(self.status,s,ORANGE,width=self.width)
 def active(self,keys):
  for k,b in self.nodes.items():b[0].set_stroke(width=3 if k in keys else 1.2,opacity=1 if k in keys else .5)
  for (a,b),l in self.wires.items():l.set_stroke(color=GREEN if a in keys and b in keys else GRAY,width=3 if a in keys and b in keys else 1.5)

def board(self,stored=True):return self.centered(Circuit(stored),7.8 if VERT else 13.8)
def emphasize(self,c,*keys):
 c.active(keys);self.play(*[Indicate(c.nodes[k],color=GREEN) for k in keys],run_time=.45)
def request(self):
 c=board(self);self.show(c);c.active(['mem','reg']);self.note('Memory[100] = 5 → R1',PURPLE);self.at(5);emphasize(self,c,'addr','mem','data','mux','reg');self.at(10);c.val('reg','R1 = 0',GREEN);c.val('data','Pending',ORANGE);c.status_text('읽기 요청 · 아직 R1에 기록하지 않음');self.note('LOAD R1, [100]',BLUE)
def pending(self):
 c=board(self,False);self.show(c);c.active(['im','dec']);self.note('동작 LOAD · 주소 100 · 목적지 R1',ORANGE);self.at(22);c.val('addr','100',ORANGE);emphasize(self,c,'addr','mem');self.at(25);c.val('data','Pending',ORANGE);c.status_text('Ready=0  ·  RegWrite=0');self.note('요청 시점과 데이터 준비 시점은 다를 수 있습니다');self.at(29);emphasize(self,c,'dec','reg');self.note('값 5가 도착했을 때 목적지는?',ORANGE)
def changing(self):
 c=board(self,False);self.show(c);c.val('data','Pending',ORANGE);c.val('im','ADD R3, R1, R2',BLUE);c.val('dec','목적지 = ?',ORANGE);self.note('입력을 계속 직접 참조한다면? · 가상 상황');self.at(39);c.val('ir','LOAD · 100 · R1',GREEN);emphasize(self,c,'ir');self.note('현재 명령의 정보를 별도로 보관하자',GREEN)
def instruction(self):
 bits=VGroup(*[pill(str(i%2),.8,1,GREEN,32).move_to([(i-2)*1.05,0,0]) for i in range(5)]);clock=txt('공통 CLK ↑ → 여러 비트를 함께 저장',26,ORANGE).next_to(bits,DOWN,buff=.65);g=self.centered(VGroup(bits,clock),7.5 if VERT else 11);self.show(g);self.note('플립플롭들을 묶은 저장 회로');self.at(48);self.play(FadeOut(g),run_time=.3);c=board(self,False);self.show(c);emphasize(self,c,'im','ir','dec');self.at(50);c.val('ir','LOAD R1, [100]',GREEN);c.status_text('IRWrite=1 · CLK ↑ : 저장');self.at(52);c.val('im','ADD R3, R1, R2',BLUE);c.status_text('IRWrite=0 : 입력이 바뀌어도 유지');self.note('입력 ADD ≠ 저장된 출력 LOAD',GREEN);self.at(57);self.note('명령어 레지스터 · Instruction Register (IR)',GREEN);emphasize(self,c,'ir')
def intermediate(self):
 c=board(self);self.show(c);self.note('명령어뿐 아니라 중간값도 보관할 수 있습니다');self.at(65);c.val('alu','100 + 4 = 104',BLUE);c.val('addr','104',GREEN);c.status_text('별도 주소 계산 예시 · CLK ↑ : 104 저장');self.note('이 장면만 별도 예시 · 주 LOAD의 주소는 100',ORANGE);emphasize(self,c,'alu','addr');self.at(69);c.val('alu','다른 입력',BLUE);c.val('mem','주소 입력 = 104',PURPLE);self.note('ALU 출력이 바뀌어도 저장된 104는 유지',GREEN)
def order(self):
 c=board(self);self.show(c);c.val('data','5',GREEN);c.active([]);self.note('정보가 있어도 동작 순서를 정해야 합니다');self.at(76);emphasize(self,c,'im','ir');c.status_text('IRWrite=1 · 명령어 저장');self.at(78);emphasize(self,c,'addr','mem','data');c.status_text('MemRead=1 · RegWrite=0');self.at(80);emphasize(self,c,'data','mux','reg');c.status_text('RegWrite=1 · 결과 기록');self.at(82);c.status_text('MemRead=1 · RegWrite=0');c.active(['mem','data']);self.note('비활성 제어 ≠ 전원 차단');self.at(85);c.status_text('현재 단계 = ?');self.note('현재 수행하는 단계를 기억해야 합니다',ORANGE)

def state_rows():
 labels=['00  명령어 인출','01  주소 결정','10  데이터 읽기','11  결과 기록']
 g=VGroup(*[pill(s,3.0,.72,GRAY,24) for s in labels])
 if VERT:g.arrange(DOWN,buff=.3)
 else:g.arrange(RIGHT,buff=.28)
 return g

def steps(self):
 c=board(self,False);self.show(c);self.note('00 · 명령어 인출',ORANGE);c.status_text('IRWrite=1 · CLK ↑');c.val('ir','LOAD R1, [100]',GREEN);emphasize(self,c,'im','ir');self.at(92);c.status_text('01 · 주소 저장 · CLK ↑');c.val('addr','100',GREEN);emphasize(self,c,'ir','addr');self.at(95);c.status_text('10 · MemRead=1 · Ready=1');c.val('data','5',GREEN);emphasize(self,c,'mem','data');self.at(98);c.status_text('11 · RegWrite=1 · CLK ↑');c.val('reg','R1 = 5',GREEN);emphasize(self,c,'data','mux','reg');self.note('Memory[100] = 5 유지 · R1 = 5',GREEN)
def control(self):
 g=self.centered(state_rows(),7.5 if VERT else 13.4);self.show(g);self.note('00 → 01 → 10 → 11 → 00',ORANGE);self.at(104);self.play(Indicate(g[2],color=ORANGE),run_time=.45);self.note('Ready=0이면 10에 머뭄 · Ready=1이면 다음 상태');self.at(106);self.play(FadeOut(g),run_time=.3);f=controller(self);self.show(f);self.note('논리 회로는 다음 상태를 계산 · CLK ↑에서 상태 저장',ORANGE);self.at(109);setlabel(f.state[1],'현재 상태 11',GREEN,width=3);setlabel(f.next[1],'다음 상태 00',ORANGE,width=3);setlabel(f.signal[1],'RegWrite = 1',ORANGE,width=3)
def controller(self):
 f=VGroup();f.state=pill('현재 상태 10',3.2,.85,GREEN,28);f.logic=pill('제어·전이 논리',3.2,.85,ORANGE,26);f.next=pill('다음 상태 11',3.2,.85,ORANGE,27);f.signal=pill('MemRead = 1',3.2,.85,ORANGE,27)
 if VERT:
  coords=[(0,2),(0,.4),(-1.8,-1.4),(1.8,-1.4)]
 else:coords=[(-4,1),(0,1),(4,1),(0,-1.2)]
 for o,p in zip([f.state,f.logic,f.next,f.signal],coords):o.move_to([*p,0]);f.add(o)
 for a,b in [(f.state,f.logic),(f.logic,f.next),(f.logic,f.signal)]:f.add(Line(a.get_center(),b.get_center(),color=ORANGE).set_z_index(-1))
 f.add(txt('명령어 · Ready → 制御'.replace('制御','제어'),23,GRAY).next_to(f.logic,UP,buff=.25))
 # Next-state logic feeds the state D input; stored state changes on an edge.
 if VERT:
  feedback=route((-1.8,-1.85),(-3.65,-1.85),(-3.65,2),(-1.6,2),c=GREEN)
  edge=txt('CLK ↑',19,GREEN).move_to([-2.95,.9,0])
 else:
  feedback=route((4,1.43),(4,2.4),(-4,2.4),(-4,1.43),c=GREEN)
  edge=txt('CLK ↑',19,GREEN).move_to([-4,2.72,0])
 f.add(feedback,edge)
 return self.centered(f,7.6 if VERT else 13)
def fsm(self):
 f=controller(self);self.show(f);self.note('상태 레지스터 + 제어·다음 상태 논리',GREEN);self.at(115);self.note('Finite State Machine · FSM · 유한 상태 기계',ORANGE);self.play(Circumscribe(f,color=ORANGE),run_time=.7)
def cycles(self):
 c=board(self,False);self.show(c);self.note('단일 LOAD · 클럭마다 다음 단계로',ORANGE)
 for t,state,keys in [(119.7,'1 · 인출',['im','ir']),(120.5,'2 · 주소',['ir','addr']),(121.3,'3 · 읽기',['mem','data']),(122.1,'4 · 기록',['data','mux','reg'])]:
  self.at(t);c.status_text('CLK ↑ · '+state);c.active(keys)
  if state.startswith('1'):c.val('ir','LOAD R1, [100]',GREEN)
  if state.startswith('2'):c.val('addr','100',GREEN)
  if state.startswith('3'):c.val('data','5',GREEN)
  if state.startswith('4'):c.val('reg','R1 = 5',GREEN)
 self.at(123);self.note('레지스터는 정보를 유지 · 제어 회로는 순서를 선택');c.status_text('IR 유지 · 주소100 유지 · 읽은 데이터5 유지');self.at(128);self.note('다중 사이클 실행 구조 · Multi-cycle Execution',GREEN);c.status_text('한 명령어 → 여러 클럭 · 사이클 수는 설계별로 다름')
def idle(self):
 c=board(self);self.show(c);self.note('명령어 인출과 데이터 읽기가 독립된 예시');self.at(137);c.active(['addr','mem','data']);c.val('data','Pending',ORANGE);c.val('im','인출 경로 대기',GRAY);c.status_text('10 · Ready=0 : 현재 상태 유지');self.note('메모리 응답 대기 · IR의 LOAD는 유지');self.at(143);c.val('im','다음 ADD ?',BLUE);self.play(Indicate(c.nodes['im'],color=BLUE),run_time=.5);self.note('가능성만 제시 · IR을 덮어쓰거나 실행하지 않음',ORANGE)
def possibility(self):
 c=board(self);self.show(c);c.val('data','Pending',ORANGE);c.val('im','다음 명령어 ?',BLUE);c.active(['mem','data']);self.note('서로 다른 단계의 자원을 함께 사용할 수 있을까?');c.status_text('현재 LOAD 유지 · 다음 명령어를 위한 별도 저장은?')
for n in ['request','pending','changing','instruction','intermediate','order','steps','control','fsm','cycles','idle','possibility']:setattr(MemoryScene,n,globals()[n])
