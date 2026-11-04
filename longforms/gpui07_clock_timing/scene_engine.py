"""Propagation, edge sampling and synchronous timing."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_timing import data,clock,q_at,output_bus,capture_bus,bank,period_ok
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

def nor(a,b):return int(not(a or b))
def stable(s,r,q,b):return q==nor(r,b) and b==nor(s,q)

class NORGate(VGroup):
 def __init__(self,color=INK):
  super().__init__();p=lambda x,y:np.array([x,y,0])
  body=VMobject(color=color,stroke_width=2.3,fill_color=PANEL,fill_opacity=1)
  body.start_new_path(p(-.65,-.55));body.add_cubic_bezier_curve_to(p(.1,-.55),p(.55,-.45),p(.85,0));body.add_cubic_bezier_curve_to(p(.55,.45),p(.1,.55),p(-.65,.55));body.add_cubic_bezier_curve_to(p(-.35,.18),p(-.35,-.18),p(-.65,-.55));body.close_path()
  self.add(body,Circle(radius=.09,color=color,fill_color=config.background_color,fill_opacity=1).move_to([.94,0,0]),ln((-.95,.25),(-.48,.25),color),ln((-.95,-.25),(-.48,-.25),color),ln((1.03,0),(1.25,0),color),txt('NOR',18,color).move_to([.04,0,0]))

class SRLatch(VGroup):
 def __init__(self,q=1,equations=True):
  super().__init__();self.q=q;self.qbar=1-q;self.s=0;self.r=0
  self.top=NORGate(BLUE).shift([0,1.5,0]);self.bottom=NORGate(PURPLE).shift([0,-1.5,0])
  self.external=VGroup(ln((-3,1.75),(-.95,1.75),BLUE),ln((-3,-1.75),(-.95,-1.75),PURPLE))
  self.outwires=VGroup(ln((1.25,1.5),(3,1.5),GREEN),ln((1.25,-1.5),(3,-1.5),GREEN))
  self.fbq=route((1.7,1.5),(2.1,1.5),(2.1,-.55),(-2,-.55),(-2,-1.25),(-.95,-1.25),c=ORANGE,w=2.7)
  # A bridge (no junction dot) where Qbar's path crosses the Q return wire.
  self.fbbar=VGroup(route((1.7,-1.5),(2.8,-1.5),(2.8,.55),(2.23,.55),c=ORANGE,w=2.7),ArcBetweenPoints([2.23,.55,0],[1.97,.55,0],angle=-PI,color=ORANGE,stroke_width=2.7),route((1.97,.55),(-2.5,.55),(-2.5,1.25),(-.95,1.25),c=ORANGE,w=2.7))
  self.junctions=VGroup(Dot([1.7,1.5,0],radius=.045,color=ORANGE),Dot([1.7,-1.5,0],radius=.045,color=ORANGE))
  self.rlabel=pill('R=0',1.4,.65,BLUE,28).move_to([-3.7,1.75,0]);self.slabel=pill('S=0',1.4,.65,PURPLE,28).move_to([-3.7,-1.75,0])
  self.qlabel=pill(f'Q={q}',1.55,.7,GREEN,32).move_to([3.8,1.5,0]);self.blabel=pill(f'Q̅={1-q}',1.55,.7,GREEN,32).move_to([3.8,-1.5,0])
  self.add(self.external,self.outwires,self.fbq,self.fbbar,self.junctions,self.top,self.bottom,self.rlabel,self.slabel,self.qlabel,self.blabel)
  self.formulas=VGroup(txt('Q = NOT(R OR Q̅)',24,BLUE),txt('Q̅ = NOT(S OR Q)',24,PURPLE)).arrange(DOWN,buff=.2).move_to([0,-3,0])
  if equations:self.add(self.formulas)
  self.paint()
 def paint(self):
  for label,s,col in [(self.rlabel,f'R={self.r}',BLUE),(self.slabel,f'S={self.s}',PURPLE),(self.qlabel,f'Q={self.q}',GREEN if self.q else GRAY),(self.blabel,f'Q̅={self.qbar}',GREEN if self.qbar else GRAY)]:setlabel(label[1],s,col)
  for w,v in [(self.fbq,self.q),(self.fbbar,self.qbar)]:w.set_color(ORANGE if v else GRAY).set_stroke(opacity=1 if v else .65)
  for w,v in zip(self.outwires,[self.q,self.qbar]):w.set_color(GREEN if v else GRAY)
  for w,v,col in zip(self.external,[self.r,self.s],[BLUE,PURPLE]):w.set_color(col).set_stroke(opacity=1 if v else .45)
 def inputs(self,s,r):
  assert not(s and r);self.s=s;self.r=r;self.paint()
 def gate_event(self,gate):
  if gate==0:self.q=nor(self.r,self.qbar)
  else:self.qbar=nor(self.s,self.q)
  self.paint()
 def settled(self):assert stable(self.s,self.r,self.q,self.qbar)
 def topology(self):return tuple(tuple(np.round(m.get_all_points().ravel(),6)) for m in [self.external,self.outwires,self.fbq,self.fbbar,self.top,self.bottom])

class DFlipFlopBlock(VGroup):
 def __init__(self,d=0,q=0):
  super().__init__();self.body=pill('D FF',2.4,1.6,INK,35)
  self.triangle=Polygon([-.7,-.8,0],[-.2,-.8,0],[-.45,-.5,0],color=ORANGE,stroke_width=2,fill_opacity=0)
  self.clk=VectorizedPoint([-.45,-1.3,0]);self.din=VectorizedPoint([-1.8,.25,0]);self.qout=VectorizedPoint([1.8,.25,0])
  self.dlabel=txt(f'D={d}',31,BLUE).move_to([-2.45,.25,0]);self.qlabel=txt(f'Q={q}',31,GREEN).move_to([2.45,.25,0]);self.clabel=txt('CLK=0',23,ORANGE).move_to([-.45,-1.65,0])
  self.add(self.body,self.triangle,ln((-1.8,.25),(-1.2,.25),BLUE),ln((1.2,.25),(1.8,.25),GREEN),ln((-.45,-1.3),(-.45,-.8),ORANGE),self.dlabel,self.qlabel,self.clabel,self.clk,self.din,self.qout)
 def state(self,d,q,c):
  assert d in [0,1] and q in [0,1] and c in [0,1]
  setlabel(self.dlabel,f'D={d}',BLUE,31);setlabel(self.qlabel,f'Q={q}',GREEN,31);setlabel(self.clabel,f'CLK={c}',ORANGE,23)
 def wires(self):return tuple(tuple(m.get_all_points().ravel()) for m in [self.body,self.triangle,self.clk,self.din,self.qout])

class ComputePath(VGroup):
 """4-bit data bus; clock line reaches storage's clock pin, never ALU."""
 def __init__(self,value='?',stored='?',clocked=False):
  super().__init__();self.alu=pill('ALU · ADD',2.4,1.3,BLUE,32).move_to([-2.6,0,0])
  self.storage=RoundedRectangle(width=3.1,height=1.5,corner_radius=.12,color=GREEN,fill_color=PANEL,fill_opacity=1).move_to([2.15,0,0])
  self.result=txt(str(value),37,GREEN).move_to([-.55,.55,0]);self.qtext=txt(f'Q={stored}',35,GREEN).move_to([2.15,-.2,0])
  self.add(self.alu,txt('A=5 · B=3',29,BLUE).move_to([-2.6,1.15,0]),ln((-1.4,0),(.6,0),GREEN,3),txt('4-bit',21,GRAY).move_to([-.5,-.4,0]),self.result,self.storage,txt('4-bit 저장',25).move_to([2.15,.38,0]),self.qtext)
  self.clk=VectorizedPoint([1.65,-1.15,0]);self.add(self.clk)
  self.clockparts=VGroup(Polygon([1.4,-.75,0],[1.9,-.75,0],[1.65,-.45,0],color=ORANGE,fill_opacity=0),route((-3,-1.9),(1.65,-1.9),(1.65,-.75),c=ORANGE),txt('CLK',26,ORANGE).move_to([-3.2,-1.9,0]))
  if clocked:self.add(self.clockparts)
 def output(self,v):setlabel(self.result,str(v),GREEN if v==8 else ORANGE,37)
 def capture(self,v):setlabel(self.qtext,f'Q={v}',GREEN if v==8 else ORANGE,35)

class SignalTimeline(VGroup):
 def __init__(self,sample=None):
  super().__init__();self.origin=-3.7;self.span=7.4
  x=lambda t:self.origin+self.span*t/10
  self.add(Rectangle(width=x(6)-x(0),height=.8,color=ORANGE,fill_color=ORANGE,fill_opacity=.09).move_to([(x(0)+x(6))/2,.2,0]),Rectangle(width=x(10)-x(6),height=.8,color=GREEN,fill_color=GREEN,fill_opacity=.09).move_to([(x(6)+x(10))/2,.2,0]),txt('출력 안정 전',26,ORANGE).move_to([x(3),.25,0]),txt('결과 8 안정',26,GREEN).move_to([x(8),.25,0]),Arrow([x(0),-.6,0],[x(10),-.6,0],buff=0,color=GRAY,stroke_width=2),txt('입력 변화',23,GRAY).move_to([x(.8),-1.05,0]),txt('시간 →',23,GRAY).move_to([x(9),-1.05,0]))
  self.sampleline=DashedLine([x(sample or 3),-.7,0],[x(sample or 3),1.4,0],color=ORANGE,stroke_width=2)
  self.tag=txt('저장',27,ORANGE).move_to([x(sample or 3),1.7,0])
  if sample is not None:self.add(self.sampleline,self.tag)
  self.anchor0=VectorizedPoint([x(0),0,0]);self.anchor10=VectorizedPoint([x(10),0,0]);self.add(self.anchor0,self.anchor10)
 def move_sample(self,t):
  x=self.anchor0.get_center()[0]+(self.anchor10.get_center()[0]-self.anchor0.get_center()[0])*t/10
  self.sampleline.shift(RIGHT*(x-self.sampleline.get_center()[0]));self.tag.shift(RIGHT*(x-self.tag.get_center()[0]))

def stepped(events,initial,y,color,x0=-3.5,scale=.7,until=10):
 pts=[(x0,y+initial*.65)];v=initial
 for t,new in events:
  if t>until:break
  pts.extend([(x0+t*scale,y+v*.65),(x0+t*scale,y+new*.65)]);v=new
 pts.append((x0+until*scale,y+v*.65));return route(*pts,c=color,w=2.5)

class Waveforms(VGroup):
 def __init__(self,cursor):
  super().__init__();self.cursor=cursor
  self.add(stepped([(1,1),(6,0)],0,1.6,BLUE),stepped([(2,1),(4,0),(8,1),(9.5,0)],0,0,ORANGE),stepped([(2.3,1),(8.3,0)],0,-1.6,GREEN))
  for y,s,c in [(1.6,'D',BLUE),(0,'CLK',ORANGE),(-1.6,'Q',GREEN)]:self.add(txt(s,25,c).move_to([-4.15,y+.25,0]))
  for e in [2,8]:self.add(DashedLine([-3.5+e*.7,-1.8,0],[-3.5+e*.7,2.6,0],color=ORANGE,stroke_width=1))
  self.add(txt('상승 에지 → 짧은 지연 → Q 변화',23,GRAY).move_to([0,-2.3,0]))
  self.anchor=VectorizedPoint([-3.5,-1.8,0]);self.end=VectorizedPoint([3.5,2.6,0]);self.add(self.anchor,self.end)
  self.scan=Line(self.anchor.get_center(),np.array([-3.5,2.6,0]),color=INK,stroke_width=1.4);self.add(self.scan)
  def update(m):
   a=self.anchor.get_center();b=self.end.get_center();x=a[0]+(b[0]-a[0])*min(10,cursor.get_value())/10;m.put_start_and_end_on([x,a[1],0],[x,b[1],0])
  self.scan.add_updater(update)

class RegisterBank(VGroup):
 def __init__(self):
  super().__init__();self.cells=VGroup();self.bits=[]
  for x in [-1.35,-.45,.45,1.35]:
   cell=pill('0',.75,.9,GREEN,35).move_to([x,0,0]);self.cells.add(cell);self.bits.append(cell[1]);self.add(Polygon([x-.13,-.45,0],[x+.13,-.45,0],[x,-.28,0],color=ORANGE),ln((x,-.45),(x,-1),ORANGE))
  self.add(self.cells,ln((-1.35,-1),(1.35,-1),ORANGE),ln((0,-1),(0,-1.5),ORANGE),txt('4 × DFF  /  4-bit',29).move_to([0,1.15,0]),txt('CLK',23,ORANGE).move_to([0,-1.8,0]))
 def capture(self,values):
  assert len(values)==4
  for m,v in zip(self.bits,values):setlabel(m,str(v),GREEN,35)

class ClockScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.04:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  07',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
  self.notice=txt(' ',24);self.add(self.notice);self.note(' ')
  starts=[r['start'] for r in TIMING]
  def idx():
   now=self.start+self.time;i=bisect_right(starts,now+1e-7)-1
   return i if 0<=i<len(TIMING) and now<TIMING[i]['end']-1e-7 else -1
  def caption(i):
   s='\n'.join(textwrap.wrap(TIMING[i]['text'] if i>=0 else ' ',width=26 if VERT else 52))
   return txt(s,30 if VERT else 29,INK,7.55 if VERT else 14.2).move_to([0,-5.73 if VERT else -3.19,0]).set_z_index(31)
  self.active_caption=idx();self.caption=caption(self.active_caption)
  def update(m):
   i=idx()
   if i!=self.active_caption:m.become(caption(i));m.set_z_index(31);self.active_caption=i
  self.caption.add_updater(update)
  panel=Rectangle(width=8.2 if VERT else 15,height=2.25 if VERT else 1.4,stroke_width=0,fill_color=config.background_color,fill_opacity=1).move_to(self.caption).set_z_index(29)
  self.add(panel,self.caption)
  x=3.9 if VERT else 7.3;y=-7.24 if VERT else -4.1;base=ln((-x,y),(x,y),EDGE,2);bar=base.copy().set_color(BLUE)
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/135)))
  self.add(base,bar,txt(f'{self.index+1:02} / 14',17,GRAY).move_to([x-.55,y+.27,0]))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)
 def clockwave(self,period=3):
  edges=[];v=0
  for t in np.arange(.8,10,period/2):v=1-v;edges.append((float(t),v))
  return stepped(edges,0,0,ORANGE)
 def pair(self,a,b,width=None):return self.centered(VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.8),width or (7.6 if VERT else 14))
 def pipeline(self,sample=3,value=0,stored='?',clocked=False):
  p=ComputePath(value,stored,clocked);t=SignalTimeline(sample);g=self.centered(VGroup(p,t).arrange(DOWN,buff=.6),7.7 if VERT else 12);return g,p,t
 def memory(self):
  g=self.centered(SRLatch(1));self.show(g);self.note('S=R=0 · 이전 값 유지')
  self.at(3);box=self.centered(pill('저장',3,1.3,GREEN,44));self.replace(g,box)
  self.at(5);self.note('계산 결과를 언제 저장해야 할까?',ORANGE)
 def delay(self):
  p=self.centered(ComputePath('?', '?'));self.show(p.alu,p[1],p[2],p[3],p.result);self.note('ADD: A=5, B=3')
  self.at(12);p.output(8);self.note('수학적으로 5 + 3 = 8',GREEN)
  self.at(15)
  self.remove(p.alu,p[1],p[2],p[3],p.result)
  timeline=SignalTimeline();p=ComputePath('?', '?');p.remove(p.storage,p.qtext,p[6]);g=self.centered(VGroup(p,timeline).arrange(DOWN,buff=.7));self.show(g);self.note('입력 변화와 출력 안정 사이에는 시간이 있다')
 def propagation(self):
  blocks=VGroup(*[pill(f'G{i+1}',1.3,.85,GRAY,28) for i in range(3)]).arrange(RIGHT,buff=.8)
  wires=VGroup(*[Line(blocks[i].get_right(),blocks[i+1].get_left(),color=BLUE) for i in range(2)])
  g=self.centered(VGroup(blocks,wires));self.show(g);self.note('게이트 출력의 전압 변화가 순서대로 반영됨')
  for b in blocks:self.play(Indicate(b,color=BLUE),run_time=.6)
  self.at(24)
  fas=VGroup(*[pill(f'FA {i}',1.25,.9,GRAY,25) for i in [3,2,1,0]]).arrange(RIGHT,buff=.55)
  lines=VGroup(*[Arrow(fas[i+1].get_left(),fas[i].get_right(),buff=.03,color=GRAY,stroke_width=2) for i in range(3)])
  h=self.centered(VGroup(fas,lines));self.replace(g,h);self.note('0111₂ + 0001₂ = 1000₂  /  올림수는 오른쪽→왼쪽')
  for i in [2,1,0]:self.play(lines[i].animate.set_color(ORANGE),run_time=.45)
 def settling(self):
  fast=VGroup(txt('빠른 경로',27,BLUE),pill('G',1.3,.8,BLUE)).arrange(RIGHT,buff=.5)
  slow=VGroup(txt('느린 경로',27,PURPLE),*[pill('G',1.1,.8,PURPLE) for _ in range(3)]).arrange(RIGHT,buff=.4)
  g=self.centered(VGroup(fast,slow).arrange(DOWN,buff=1));self.show(g);self.note('지연은 게이트 종류·부하·배선 등에도 영향받음')
  self.play(Indicate(fast,color=BLUE),run_time=.5);self.wait(.5);self.play(Indicate(slow,color=PURPLE),run_time=.5)
  self.at(33);t=self.centered(SignalTimeline());self.replace(g,t);self.note('과도 상태는 가능한 일시적 변화의 예시')
  self.at(36);self.note('시간이 지나면 의도한 결과 8로 안정',GREEN)
 def sampling(self):
  g,p,t=self.pipeline(3,0,'?');self.show(g);self.note('ALU → 4비트 계산 결과 → 추상 저장 회로')
  self.at(42);p.capture(0);self.note('안정 전 저장: 예시 버스값 0 기록',ORANGE)
  self.at(45);p.output(8);self.note('ALU는 8로 안정됐지만, 이미 저장한 Q=0은 그대로',ORANGE)
  self.at(50);t.move_sample(8);self.play(Indicate(t.sampleline,color=ORANGE),run_time=.6)
  self.at(52);p.capture(8);self.note('출력 안정과 필요한 시간 여유 후에 기록 → Q=8',GREEN)
 def dff(self):
  b=self.centered(pill('?',3,1.6,GREEN,52));self.show(b);self.note('정해진 시점의 입력을 보존하는 저장 방식')
  self.at(59)
  d=DFlipFlopBlock(0,0);curve=VGroup(stepped([(1,1),(3,0),(5,1),(7,0)],0,.8,BLUE,until=8),stepped([(5.2,1)],0,-.8,GREEN,until=8),txt('D: 변화하는 데이터',26,BLUE).move_to([0,2,0]),txt('Q: 특정 시점의 값을 유지',26,GREEN).move_to([0,-1.8,0]));h=self.centered(curve);self.replace(b,h);self.note('이 비교는 SR 래치의 연속 추종을 뜻하지 않음')
  self.at(65);self.replace(h,self.centered(d));self.note('D Flip-Flop  /  D 플립플롭',GREEN)
 def edge(self):
  cursor=ValueTracker(0);d=DFlipFlopBlock(0,0);w=Waveforms(cursor);g=self.pair(d,w);self.show(g);self.note('정상 샘플링 예시 · D는 에지 전후로 안정')
  def update(m):m.state(data(cursor.get_value()),q_at(cursor.get_value()),clock(cursor.get_value()))
  d.add_updater(update)
  self.play(cursor.animate.set_value(6),run_time=5.6,rate_func=linear)
  self.at(73);self.note('D가 0으로 바뀌어도 Q는 다음 상승 에지까지 1 유지',GREEN)
  self.play(cursor.animate.set_value(10),run_time=3.6,rate_func=linear)
  d.remove_updater(update)
 def clock(self):
  wave=self.centered(VGroup(self.clockwave(3),txt('Clock',36,ORANGE).shift(UP*1.4),DoubleArrow([-2.94,-1,0],[-.84,-1,0],buff=0,color=ORANGE,stroke_width=2),txt('주기 T',26,ORANGE).move_to([-1.89,-1.6,0])));self.show(wave);self.note('클럭은 주기적으로 두 전압 상태를 반복')
  self.at(79);self.note('0: 낮은 전압  /  1: 높은 전압  /  상승 에지 간격 = 주기 T')
  self.at(82);d=VGroup(*[DFlipFlopBlock(i%2,0).scale(.55) for i in range(3)]).arrange(DOWN if VERT else RIGHT,buff=.7);h=self.centered(d,7.5 if VERT else 14);self.replace(wave,h)
  # Common branch is attached only to clock anchors.
  points=[o.clk.get_center() for o in d]
  if VERT:
   x=min(o.get_left()[0] for o in d)-.35;bus=VGroup(Line([x,min(p[1] for p in points),0],[x,max(p[1] for p in points),0],color=ORANGE),*[Line([x,p[1],0],p,color=ORANGE) for p in points])
  else:
   y=min(o.get_bottom()[1] for o in d)-.3;bus=VGroup(Line([min(p[0] for p in points),y,0],[max(p[0] for p in points),y,0],color=ORANGE),*[Line([p[0],y,0],p,color=ORANGE) for p in points])
  self.show(bus);self.note('공통 CLK · 각 플립플롭은 자신의 D를 기록')
  self.at(85);self.play(Indicate(bus,color=ORANGE),run_time=.4)
  for i,o in enumerate(d):o.state(i%2,0,1)
  self.wait(.3)
  for i,o in enumerate(d):o.state(i%2,i%2,1)
 def fast(self):
  g,p,t=self.pipeline(8,8,8,True);self.show(g);self.note('클럭 주기가 짧아지면 저장 시점도 앞당겨진다')
  self.at(90);t.move_sample(3);p.output('?');self.note('다음 에지가 계산 완료보다 먼저 도착')
  self.at(92);self.note('계산 미완료',ORANGE)
  self.at(93);p.capture('?');self.note('값·샘플링 조건을 보장할 수 없음  /  ?는 확정값이 아님',ORANGE)
 def period(self):
  a=VGroup(txt('너무 짧은 주기',31,ORANGE),SignalTimeline(3).shift(DOWN*2.4));b=VGroup(txt('시간 여유 확보',31,GREEN),SignalTimeline(8).shift(DOWN*2.4));g=self.pair(a,b);self.show(g);self.note('계산 완료 + 저장 요소가 요구하는 안정 여유')
  self.at(102);self.play(Indicate(b,color=GREEN),run_time=.7);self.note('전파·setup·clock-to-Q 등을 고려 · hold 조건도 별도 필요')
 def roles(self):
  p=self.centered(ComputePath('?', '?',True),7.6 if VERT else 12);self.show(p);self.note('ALU: 계산  /  저장 회로: 기록  /  CLK: 갱신 기준')
  self.at(110);p.output('?');self.play(Indicate(p.alu,color=BLUE),run_time=.7)
  self.at(112);p.output(8);self.note('계산 → 결과 안정 → 저장',GREEN)
  self.at(114);self.play(Indicate(p.clockparts,color=ORANGE),run_time=.4);p.capture(8)
 def sync(self):
  ds=VGroup(*[DFlipFlopBlock(v,0).scale(.6) for v in [1,0,1]]).arrange(DOWN if VERT else RIGHT,buff=.75);g=self.centered(ds,7.5 if VERT else 14);self.show(g)
  pts=[o.clk.get_center() for o in ds]
  if VERT:
   x=min(o.get_left()[0] for o in ds)-.35;bus=VGroup(Line([x,min(p[1] for p in pts),0],[x,max(p[1] for p in pts),0],color=ORANGE),*[Line([x,p[1],0],p,color=ORANGE) for p in pts])
  else:
   y=min(o.get_bottom()[1] for o in ds)-.3;bus=VGroup(Line([min(p[0] for p in pts),y,0],[max(p[0] for p in pts),y,0],color=ORANGE),*[Line([p[0],y,0],p,color=ORANGE) for p in pts])
  self.show(bus);self.note('공통 시간 기준 · 각 입력 D는 서로 다를 수 있음')
  self.at(119)
  for i,o in enumerate(ds):o.state([1,0,1][i],0,1)
  self.wait(.3)
  for i,o in enumerate(ds):o.state([1,0,1][i],[1,0,1][i],1)
  self.note('실제 Q 변화에는 전파 지연과 클럭 스큐가 존재')
  self.at(122);self.note('Synchronous Circuit  /  동기식 회로',GREEN)
 def register(self):
  r=RegisterBank();ad=pill('ALU: 5+3=8',3.6,1.1,BLUE,35);g=self.pair(ad,r);self.show(g);self.note('8 = 1000₂  /  단일 플립플롭은 1비트만 저장')
  if VERT:
   a=ad.get_left();b=r.cells.get_left();x=min(a[0],b[0])-.45;wire=route(tuple(a[:2]),(x,a[1]),(x,b[1]),tuple(b[:2]),c=GREEN,w=3)
  else:wire=Line(ad.get_right(),r.cells.get_left(),color=GREEN,stroke_width=3)
  self.show(wire)
  self.at(127);self.play(Indicate(r,color=ORANGE),run_time=.4)
  self.at(128);r.capture([1,0,0,0]);self.note('4비트 결과를 네 개의 DFF에 기록',GREEN)
 def choose(self):
  regs=VGroup(*[pill(s,2.7,.9,GREEN,31).move_to([-3.8,y,0]) for s,y in zip(['R1 = 5','R2 = 3','R3 = 8'],[1.3,0,-1.3])]);select=pill('선택?',2.1,3.2,GRAY,35);ad=pill('ALU',2.5,1.8,BLUE,45).move_to([3.5,0,0])
  paths=VGroup(*[DashedLine(o.get_right(),[-1.05,y,0],color=GRAY,stroke_width=1.5) for o,y in zip(regs,[1.3,0,-1.3])],ln((1.05,.35),(2.25,.35),GRAY),ln((1.05,-.35),(2.25,-.35),GRAY))
  g=self.centered(VGroup(regs,select,ad,paths),7.7 if VERT else 13);self.show(g);self.note('다음 계산에는 어떤 저장값을 사용할까?',ORANGE)
