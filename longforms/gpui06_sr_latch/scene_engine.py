"""NOR feedback, bistability and state retention."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_latch import nor,stable,transition
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
 new=txt(s,size,color);new.scale_to_fit_height(m.height);m.become(new.move_to(m.get_center()));return m

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

class MemoryScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.04:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  06',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/140)))
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
 def latch(self,q=1,equations=True):return self.centered(SRLatch(q,equations),7.7 if VERT else 11)
 def pulse(self,d,s,r,pause=.35):
  before=d.topology();events,final=transition(d.q,s,r);d.inputs(s,r)
  for gate,_,_ in events:
   self.wait(pause);d.gate_event(gate)
  d.settled();assert (d.q,d.qbar)==final and before==d.topology()
 def alublock(self,a=5,b=3):
  g=VGroup(pill('ALU',3,1.3,GREEN,46),txt(f'A={a}',32,BLUE).move_to([-2.8,.45,0]),txt(f'B={b}',32,PURPLE).move_to([-2.8,-.45,0]),ln((-2,.45),(-1.5,.45),BLUE),ln((-2,-.45),(-1.5,-.45),PURPLE),ln((1.5,0),(2.1,0),GREEN),pill(str(a+b),1.4,.9,GREEN,39).move_to([2.8,0,0]))
  return self.centered(g)
 def alu(self):
  g=self.alublock();self.show(g);self.note('ADD · SUB · AND · OR  /  연산 선택')
  self.at(6);self.note('첫 결과를 다음 계산에 사용하려면?');self.play(Indicate(g[-1],color=GREEN),run_time=.7)
 def chain(self):
  eq=self.equation('(5 + 3) + 2',INK,58);self.show(eq);self.note('첫 번째 결과 → 두 번째 입력')
  self.at(16)
  g=VGroup(pill('ADDER 1',2.5,1,BLUE,30).move_to([-2.2,0,0]),pill('ADDER 2',2.5,1,PURPLE,30).move_to([2.2,0,0]),ln((-.95,0),(.95,0),GREEN,4),txt('n-bit',22,GRAY).move_to([0,-.45,0]),txt('5 + 3',35,BLUE).move_to([-2.2,1.2,0]),txt('+ 2',35,PURPLE).move_to([2.2,1.2,0]),ln((3.45,0),(4,0),GREEN),pill('?',1.4,.8,GREEN,35).move_to([4.7,0,0]))
  self.replace(eq,self.centered(g));self.at(20)
  eight=txt('8',35,GREEN).move_to(g[2].get_center()+UP*.65);self.show(eight);self.at(23)
  setlabel(g[-1][1],'10',GREEN);self.note('5 + 3 = 8  →  8 + 2 = 10',GREEN);self.play(Indicate(g[1],color=GREEN),run_time=.7)
  self.at(26);many=VGroup(*[pill('+',.9,.9,GRAY,34) for _ in range(5)]).arrange(RIGHT,buff=.45);self.remove(eight);self.replace(g,self.centered(many));self.note('단계마다 회로를 복제하는 설계 → 소자·배선 증가')
 def reuse(self):
  g=self.alublock();self.show(g);self.note('하나의 ALU, 여러 번의 계산')
  self.at(36)
  y=-1.7 if VERT else -1.25;box=pill('중간 결과: 8',3.4,.8,GREEN,31).move_to([0,y,0]);self.show(box)
  wire=route((2.8,g[-1].get_bottom()[1]),(2.8,y),(1.7,y),c=GREEN);self.show(wire)
  self.at(39);self.note('보관한 8과 새 입력 2 → 다음 계산의 10',GREEN)
  setlabel(g[1],'A=8',BLUE);setlabel(g[2],'B=2',PURPLE);setlabel(g[-1][1],'10',GREEN)
  axy=g[1].get_center();back=route((-1.7,y),(-3.8,y),(-3.8,axy[1]),(-2,axy[1]),c=GREEN)
  self.play(Create(back),Indicate(box,color=GREEN),run_time=.6)
 def combinational(self):
  g=self.alublock();self.show(g);self.note('현재까지의 조합논리 회로 · 이전 상태 저장 없음')
  self.at(46);self.play(Indicate(g[-1],color=GREEN),run_time=.6)
  self.at(49);h=self.alublock(8,2);self.replace(g,h);self.note('입력 8·2 → 출력 10  /  이전 출력 8은 보존되지 않음')
  self.at(52);q=self.centered(VGroup(NORGate(),txt('기억할 수 있을까?',34).shift(DOWN*1.5)));self.replace(h,q)
 def feedback(self):
  g=VGroup(*[pill('논리',1.5,.85,INK,29).move_to([x,0,0]) for x in [-2.5,0,2.5]])
  wires=VGroup(ln((-4,0),(-3.25,0),BLUE),ln((-1.75,0),(-.75,0),BLUE),ln((.75,0),(1.75,0),BLUE),ln((3.25,0),(4,0),BLUE))
  allg=self.centered(VGroup(g,wires));self.show(allg);self.note('입력 → 논리 회로 → 출력')
  self.at(59)
  for w in wires:self.play(Indicate(w,color=BLUE),run_time=.35)
  self.at(63)
  # Conceptual feedback enters a separate pin: do not short it to external input.
  x0=g[0].get_center()[0];y0=g[0].get_bottom()[1];end=wires[-1].get_end()
  fb=route(tuple(end[:2]),(end[0]+.2,end[1]),(end[0]+.2,y0-1.2),(x0,y0-1.2),(x0,y0),c=ORANGE,w=3)
  self.play(Create(fb),run_time=1.4);self.note('출력을 다시 별도 입력으로 연결')
  self.at(68);self.note('Feedback · 되먹임  /  모든 되먹임이 기억은 아님',ORANGE);self.play(Indicate(fb,color=ORANGE),run_time=.7)
 def nor(self):
  a=NORGate(BLUE).shift([0,1.5,0]);b=NORGate(PURPLE).shift([0,-1.5,0]);g=self.centered(VGroup(a,b));self.show(g);self.note('NOR: 두 입력이 0이면 출력 1')
  self.at(75);d=self.latch();self.replace(g,d);self.note('위: R·Q̅ → Q  /  아래: S·Q → Q̅')
 def sethold(self):
  d=self.latch(0);self.show(d);self.note('초기 상태 가정: Q=0, Q̅=1')
  self.at(80);d.inputs(1,0);self.note('S=1 설정 · 전파 지연을 순서로 보여주는 모형',ORANGE)
  self.at(81);d.gate_event(1);self.play(Indicate(d.bottom,color=PURPLE),run_time=.4)
  self.at(82);d.gate_event(0);d.settled();self.note('Q̅=0 → 위 NOR 입력 0·0 → Q=1',GREEN)
  self.at(84);self.pulse(d,0,0);self.note('R=0, S=0인데 Q=1 · Q̅=0 유지',GREEN)
  self.at(87);self.play(Indicate(d.fbq,color=ORANGE),run_time=.7)
 def reset(self):
  d=self.latch(1);self.show(d);d.inputs(0,1);self.note('R=1 초기화 · 전파 지연 모형',ORANGE)
  self.at(91);d.gate_event(0)
  self.at(92);d.gate_event(1);d.settled()
  self.at(93);self.pulse(d,0,0);self.note('R=0, S=0으로 복귀해도 Q=0 유지',GREEN)
 def twostates(self):
  a=SRLatch(1,False);b=SRLatch(0,False)
  for d in [a,b]:d.add(txt('R=0 · S=0',33).move_to([0,3,0]));d.settled()
  g=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=1);self.show(self.centered(g,7.6 if VERT else 14));self.note('같은 외부 입력, 서로 다른 이전 상태',GREEN)
 def bit(self):
  d=self.latch(1);self.show(d);self.note('두 가지 안정 상태 → 1비트 저장',GREEN)
  self.at(104);self.note('전원이 공급되고 정상 동작할 때 상태 유지')
 def controls(self):
  d=self.latch(0);self.show(d);self.note('S=1 → SET · 전파 지연 모형',ORANGE);self.pulse(d,1,0);self.pulse(d,0,0)
  self.at(108);self.note('R=1 → RESET · 전파 지연 모형',ORANGE);self.pulse(d,0,1);self.pulse(d,0,0)
  self.at(110);self.note('S R : 00 유지  /  10 설정  /  01 초기화  /  11 사용 안 함')
  self.at(112);self.note('SR Latch  /  SR 래치',GREEN);self.play(Create(SurroundingRectangle(d,buff=.15,color=GREEN)),run_time=.7)
 def samegates(self):
  d=self.latch(1);self.show(d);self.note('같은 논리 게이트, 새로운 연결 구조')
  self.at(116);self.play(Indicate(d.top,color=BLUE),Indicate(d.bottom,color=PURPLE),run_time=.7)
  self.at(118);self.play(Indicate(d.fbq,color=ORANGE),Indicate(d.fbbar,color=ORANGE),run_time=.7);self.note('논리 게이트 + 상태를 지탱하는 연결 → 기억',GREEN)
 def when(self):
  d=self.latch(1);self.show(d);self.note('언제 바뀌어야 할까?',ORANGE)
  self.at(125)
  wave=route((-3,0),(-2.3,0),(-2.3,1),(-1.5,1),(-1.5,0),(-.8,0),(-.8,1),(0,1),c=BLUE)
  block=pill('저장 상태',2.5,1.2,GREEN,32).move_to([2.4,.5,0]);question=txt('기록 시점?',28,ORANGE).move_to([0,2,0])
  h=self.centered(VGroup(wave,block,question));self.replace(d,h);self.note('시간 제어의 개념도 · SR의 S/R 입력을 D로 바꾼 회로가 아님')
 def timing(self):
  blocks=VGroup(*[pill(s,1.6,1,GREEN if i%2==0 else BLUE,27) for i,s in enumerate(['저장 A','계산','저장 B','계산','저장 C'])]).arrange(DOWN if VERT else RIGHT,buff=.45)
  wires=VGroup(*[Line(blocks[i].get_bottom() if VERT else blocks[i].get_right(),blocks[i+1].get_top() if VERT else blocks[i+1].get_left(),color=ORANGE) for i in range(4)])
  g=self.centered(VGroup(blocks,wires),7.4 if VERT else 13.5);self.show(g);self.note('상태 변화는 연결된 계산 경로에 영향을 준다')
  self.at(132)
  for i in [0,2,4]:self.play(Indicate(blocks[i],color=ORANGE),run_time=.45)
  self.at(135);self.note('값의 유지에 더해, 갱신 시점도 설계해야 한다',GREEN)
  question=txt('언제 갱신할까?',34,ORANGE).move_to([0,5.6 if VERT else 2.4,0]);self.show(question)
