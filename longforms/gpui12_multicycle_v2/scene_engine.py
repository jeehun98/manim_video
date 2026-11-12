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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/161)))
  self.add(base,bar,txt(f'{self.index+1:02} / 11',17,GRAY).move_to([x-.55,y+(.27 if VERT else -.2),0]).set_z_index(32))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)




class Processor(VGroup):
 def __init__(self,storage=False):
  super().__init__();self.nodes={};self.labels={};self.storage=set(['ir','addr','mdr']) if storage else set();self.active_keys=[]
  if VERT:pos={'pc':(-2.7,2.4),'im':(0,2.4),'ir':(2.7,2.4),'dec':(2.7,.65),'addr':(0,.65),'mem':(-2.7,.65),'mdr':(-2.7,-1.1),'mux':(0,-1.1),'reg':(2.7,-1.1)}
  else:pos={'pc':(-5.8,1),'im':(-3.3,1),'ir':(-.5,1),'dec':(2.3,1),'addr':(5.1,1),'mem':(5.1,-1),'mdr':(2.3,-1),'mux':(-.5,-1),'reg':(-3.3,-1)}
  labels={'pc':'명령어 주소','im':'명령어 메모리','ir':'명령어 보관','dec':'해독 회로','addr':'주소 보관','mem':'데이터 메모리','mdr':'읽은 값 보관','mux':'쓰기 경로 선택','reg':'레지스터'}
  values={'pc':'PC = 0','im':'LOAD R1, [100]','ir':'—','dec':'100 → R1','addr':'—','mem':'100 : 5','mdr':'—','mux':'MUX','reg':'R1 = 0'}
  for k,xy in pos.items():
   color=GREEN if k in ['ir','addr','mdr'] else PURPLE if k=='mem' else BLUE
   box=pill(values[k],2.35 if VERT else 2.45,.7,color,24).move_to([*xy,0]);lab=txt(labels[k],19,color,2.4).next_to(box,UP,buff=.12)
   self.nodes[k]=box;self.labels[k]=lab
   if k in ['ir','addr','mdr'] and k not in self.storage:box.set_opacity(0);lab.set_opacity(0)
   self.add(box,lab)
  self.paths=VGroup();self.add(self.paths);self.rewire()
  self.stage=txt('LOAD R1, [100]',25,INK,7.4 if VERT else 12).move_to([0,-2.2 if VERT else -2.05,0]);self.add(self.stage)
 def rewire(self):
  order=['pc','im']+(['ir'] if 'ir' in self.storage else [])+['dec']+(['addr'] if 'addr' in self.storage else [])+['mem']+(['mdr'] if 'mdr' in self.storage else [])+['mux','reg']
  self.paths.remove(*list(self.paths));self.edges=[]
  for a,b in zip(order,order[1:]):
   u,v=self.nodes[a],self.nodes[b];delta=v.get_center()-u.get_center()
   if abs(delta[1])<.2:st=u.get_right() if delta[0]>0 else u.get_left();en=v.get_left() if delta[0]>0 else v.get_right();points=[st,en]
   elif abs(delta[0])<.2:points=[u.get_bottom(),v.get_top()]
   else:
    st=u.get_right() if delta[0]>0 else u.get_left();en=v.get_top();points=[st,np.array([en[0],st[1],0]),en]
   line=VMobject(stroke_color=GRAY,stroke_width=2).set_points_as_corners(points);self.paths.add(line);self.edges.append((a,b,line))
  self.paths.set_z_index(-1)
 def value(self,k,s,color=INK):
  b=self.nodes[k];t=txt(s,27,color);t.scale_to_fit_height(b[0].height*.43)
  if t.width>b[0].width*.92:t.scale_to_fit_width(b[0].width*.92)
  b[1].become(t.move_to(b[0]))
 def activate(self,keys):
  self.active_keys=list(keys)
  for k,b in self.nodes.items():
   if k not in ['ir','addr','mdr'] or k in self.storage:b[0].set_stroke(width=3 if k in keys else 1.2,opacity=1 if k in keys else .4);b[1].set_opacity(1 if k in keys else .55);self.labels[k].set_opacity(1 if k in keys else .55)
  for a,b,line in self.edges:line.set_stroke(color=GREEN if a in keys and b in keys else GRAY,width=3 if a in keys and b in keys else 1.5,opacity=1 if a in keys and b in keys else .4)
 def stage_text(self,s,color=ORANGE):
  t=txt(s,25,color,7.5 if VERT else 12.7);t.scale_to_fit_height(self.stage.height);self.stage.become(t.move_to(self.stage))
 def reveal(self,k):
  self.storage.add(k);self.nodes[k].set_opacity(1);self.labels[k].set_opacity(1);self.rewire()

def proc(self,storage=False):return self.centered(Processor(storage),7.9 if VERT else 14)
def pulse(self,p,keys):
 p.activate(keys);self.play(*[Indicate(p.nodes[k],color=GREEN) for k in keys if k not in ['ir','addr','mdr'] or k in p.storage],run_time=.45)

def phases():
 g=VGroup(*[pill(t,3.0,.8,GRAY,25) for t in ['命令'.replace('命令','명령어 인출'),'주소 결정','데이터 읽기','결과 기록']])
 g.arrange(DOWN if VERT else RIGHT,buff=.38)
 arrows=VGroup(*[Arrow(a.get_bottom() if VERT else a.get_right(),b.get_top() if VERT else b.get_left(),buff=.08,color=GRAY,stroke_width=2,max_tip_length_to_length_ratio=.2) for a,b in zip(g,g[1:])])
 wave=route((-3.0,-3.1),(-2.6,-3.1),(-2.6,-2.75),(-1.8,-2.75),(-1.8,-3.1),(-1,-3.1),(-1,-2.75),(-.2,-2.75),(-.2,-3.1),(.6,-3.1),(.6,-2.75),(1.4,-2.75),(1.4,-3.1),(2.2,-3.1),(2.2,-2.75),(3,-2.75),c=ORANGE)
 if VERT:wave.shift(DOWN*.5)
 clock=txt('CLK  1     2     3     4',22,ORANGE).next_to(wave,DOWN,buff=.2)
 return VGroup(g,arrows,wave,clock)

def question(self):
 p=proc(self);self.show(p);p.activate([]);self.note('기존 프로세서 · 새로운 계산 장치는 추가하지 않습니다');self.at(6);self.note('어떤 장치를 먼저 사용할까?',ORANGE);self.at(9);pulse(self,p,['mem','reg']);self.note('Memory[100] = 5  →  R1 = 5',PURPLE)
def load(self):
 p=proc(self);self.show(p);pulse(self,p,['pc','im']);p.stage_text('① PC=0 → 명령어 인출');self.at(17);pulse(self,p,['im','dec']);p.stage_text('② 해독 → 주소100 · 목적지R1');self.at(24);pulse(self,p,['dec','mem']);p.stage_text('③ 주소100의 데이터 읽기');self.at(27);pulse(self,p,['mem','mux','reg']);self.at(29);p.value('reg','R1 = 5',GREEN);p.stage_text('④ 결과 기록 · 명령어 완료');self.note('메모리 값 5는 그대로 · R1만 0 → 5',GREEN)
def devices(self):
 p=proc(self);self.show(p);p.activate([]);self.note('하나의 명령어에 포함된 서로 다른 동작');self.at(37);pulse(self,p,['pc','im']);p.stage_text('명령어 인출 → 명령어 메모리');self.at(40);pulse(self,p,['dec','mem']);p.stage_text('데이터 읽기 → 데이터 메모리');self.at(43);pulse(self,p,['mux','reg']);p.stage_text('결과 기록 → 레지스터');self.note('지금은 작업 구분 · 아직 클럭 수를 정하지 않았습니다')
def clocks(self):
 g=phases();self.centered(g,7.5 if VERT else 13.4);self.show(g);self.note('하나의 명령어, 여러 단계');self.at(50)
 # Distinct clock intervals, not a claim about any physical clock period.
 for t,i,result in [(50,0,'명령어'),(53,1,'주소100 · 목적지R1'),(57,2,'데이터5'),(59.3,3,'R1=5')]:
  self.at(max(t,self.start+self.time));g[0][i][0].set_stroke(ORANGE,width=3);self.play(Indicate(g[0][i],color=ORANGE),run_time=.35);self.note(f'CLK ↑  {i+1} · 남아 있어야 할 정보: {result}',ORANGE)
 self.note('교육용 클럭 배치 · 단계 완료 후 다음 경계에서 갱신',ORANGE)
def remember(self):
 g=self.centered(phases(),7.5 if VERT else 13.4);self.show(g);self.note('현재 어느 과정을 실행 중일까?',ORANGE);self.at(66);self.play(Indicate(g[0][2],color=ORANGE),run_time=.45);self.at(70);self.play(FadeOut(g),run_time=.3)
 bits=VGroup(pill('0',1,1,GREEN,40),pill('0',1,1,GREEN,40)).arrange(RIGHT,buff=.35);clock=txt('CLK ↑',25,ORANGE).next_to(bits,DOWN,buff=.5);b=self.centered(VGroup(bits,clock),6 if VERT else 9);self.show(b);self.note('여러 비트를 함께 기억하는 기존 저장 회로',GREEN);self.at(74);self.note('저장할 대상: 숫자 대신 현재 실행 단계',GREEN)

def state(self):
 p=proc(self);p.scale(.8 if VERT else .78).shift(DOWN*(.65 if VERT else .2));self.show(p)
 sr=pill('현재 단계 00',3.6,.8,GREEN,29).move_to([0,4.55 if VERT else 2.15,0]);self.show(sr);self.note('실행 단계의 번호 · PC의 명령어 주소와 다릅니다',ORANGE)
 mapping=[(77.8,'00','명령어 인출',['pc','im']),(79.5,'01','주소 결정',['dec','mem']),(81.3,'10','데이터 읽기',['mem']),(83.1,'11','결과 기록',['mux','reg'])]
 for t,bits,name,keys in mapping:
  self.at(t);setlabel(sr[1],f'현재 단계 {bits}',GREEN,width=3.2);p.stage_text(bits+' · '+name);pulse(self,p,keys)
 self.at(85);p.value('reg','R1 = 5',GREEN);self.note('상태값 ↔ 활성 장치 ↔ 저장된 결과',GREEN)

class Control(VGroup):
 def __init__(self,feedback=False):
  super().__init__();self.state=pill('현재 상태 00',3.1,.85,GREEN,28);self.logic=pill('제어 논리',3.1,.85,ORANGE,28);self.device=pill('명령어 인출',3.1,.85,BLUE,27);self.next=pill('다음 상태 01',3.1,.85,ORANGE,27)
  coords=[(0,2.1),(0,.55),(0,-1.0),(-2.0,-2.6)] if VERT else [(-4.3,.9),(0,.9),(4.3,.9),(0,-1.25)]
  for o,xy in zip([self.state,self.logic,self.device,self.next],coords):
   o.move_to([*xy,0])
   if o is not self.next:self.add(o)
  for a,b in [(self.state,self.logic),(self.logic,self.device)]:self.add(Line(a.get_center(),b.get_center(),color=ORANGE).set_z_index(-1))
  self.feedback=VGroup()
  self.feedback.add(Line(self.logic.get_center(),self.next.get_center(),color=ORANGE).set_z_index(-1))
  if VERT:path=route((-2,-3.025),(-3.8,-3.025),(-3.8,2.1),(-1.55,2.1),c=GREEN);clk=txt('CLK ↑',22,GREEN).move_to([-2.9,1.4,0])
  else:path=route((0,-1.675),(-6.1,-1.675),(-6.1,.9),(-5.85,.9),c=GREEN);clk=txt('CLK ↑',22,GREEN).move_to([-5,-1.2,0])
  self.feedbackpath=path;self.feedback.add(self.next,path,clk);self.add(self.feedback);self.feedback.set_opacity(1 if feedback else 0);path.set_fill(opacity=0);self.feedback_visible=feedback
  self.cell=pill('PC0 → LOAD',2.8,.6,BLUE,24)
  self.cell.next_to(self.device,DOWN,buff=.2)
  self.add(self.cell)
 def change(self,bits,nextbits,device):
  setlabel(self.state[1],'현재 상태 '+bits,GREEN,width=2.8);setlabel(self.next[1],'다음 상태 '+nextbits,ORANGE,width=2.8);setlabel(self.device[1],device,BLUE,width=2.8)
  setlabel(self.cell[1],{'00':'PC0 → LOAD','10':'[100] → 5','11':'R1 : 0 → 5'}.get(bits,'주소100'),GREEN,width=2.6)
  if not self.feedback_visible:self.next.set_opacity(0)

def logic(self):
 c=self.centered(Control(),7.6 if VERT else 13.5);self.show(c);self.note('현재 상태 → 논리 회로 → 실제 장치 동작',ORANGE);self.at(95);c.change('00','01','명령어 인출');self.play(Indicate(c.device,color=BLUE),run_time=.45);self.at(98);c.change('10','11','데이터 메모리 읽기');self.play(Indicate(c.device,color=PURPLE),run_time=.45);self.at(101);c.feedback.set_opacity(1);c.feedbackpath.set_fill(opacity=0);c.feedback_visible=True;self.note('다음 상태는 논리로 계산 · CLK ↑에서 저장',GREEN);self.at(103);c.change('11','00','레지스터 기록');self.play(Indicate(c.state,color=GREEN),run_time=.45)
def fsm(self):
 c=self.centered(Control(True),7.6 if VERT else 13.5);c.change('10','11','데이터 메모리 읽기');self.show(c);self.note('현재 상태 저장 + 제어 논리 + 상태 전이',GREEN);self.at(109);self.play(Circumscribe(c,color=GREEN),run_time=.65);self.note('유한 상태 기계 · Finite State Machine (FSM)',ORANGE)
def storage(self):
 p=proc(self);self.show(p);p.activate([]);self.note('순서뿐 아니라, 다음 단계에 필요한 정보도 유지해야 합니다');self.at(116);pulse(self,p,['im','dec']);p.stage_text('명령어 · 주소 · 읽은 데이터');self.at(120);self.note('단계가 끝나도 필요한 정보는 남아 있어야 합니다',GREEN);self.at(124);self.note('기존 레지스터를 필요한 경로에 추가',GREEN);self.at(126);p.reveal('ir');p.value('ir','LOAD R1, [100]',GREEN);pulse(self,p,['im','ir','dec']);self.at(128.1);p.reveal('addr');p.value('addr','100',GREEN);pulse(self,p,['dec','addr','mem']);self.at(130.2);p.reveal('mdr');p.value('mdr','5',GREEN);pulse(self,p,['mem','mdr','mux']);self.note('명령어 보관 · 주소 보관 · 읽은 데이터 보관',GREEN);p.stage_text('저장 회로는 필요한 값만 필요한 동안 유지')
def complete(self):
 p=proc(self,True);self.show(p);self.note('완성된 회로로 LOAD 한 개 실행',GREEN)
 for t,bits,name,keys in [(133.5,'00','명령어 인출',['pc','im','ir']),(134.5,'01','주소 결정',['ir','dec','addr']),(135.5,'10','데이터 읽기',['addr','mem','mdr']),(136.6,'11','결과 기록',['mdr','mux','reg'])]:
  self.at(t);p.stage_text('상태 '+bits+' · '+name+' · CLK ↑');pulse(self,p,keys)
  if bits=='00':p.value('ir','LOAD R1, [100]',GREEN)
  if bits=='01':p.value('addr','100',GREEN)
  if bits=='10':p.value('mdr','5',GREEN)
  if bits=='11':p.value('reg','R1 = 5',GREEN)
 self.at(138);self.note('다중 사이클 실행 구조 · Multi-cycle Processor',GREEN);p.stage_text('하나의 명령어를 여러 클럭에 나누어 실행')
def overlap(self):
 p=proc(self,True);p.value('ir','LOAD R1, [100]',GREEN);p.value('addr','100',GREEN);p.value('mdr','5',GREEN);self.show(p);p.activate(['addr','mem','mdr']);self.note('명령어 인출과 데이터 읽기가 독립된 예시');self.at(147);p.stage_text('현재 LOAD : 데이터 메모리 사용 중');self.note('명령어 인출 경로는 사용하지 않는 순간',ORANGE);self.at(153);p.value('im','다음 ADD ?',BLUE);self.play(Indicate(p.nodes['im'],color=BLUE),run_time=.5);self.note('다음 명령어를 미리 가져온다면?',BLUE);self.at(157);self.note('현재 LOAD 정보는 유지 · 다른 명령어는 아직 실행하지 않음');p.stage_text('명령어 A : 데이터 읽기 / 명령어 B : 인출 ?')
for n in ['question','load','devices','clocks','remember','state','logic','fsm','storage','complete','overlap']:setattr(MemoryScene,n,globals()[n])
