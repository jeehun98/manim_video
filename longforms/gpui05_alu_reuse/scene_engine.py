"""Shared adder, two's complement, flag logic and fixed ALU selection."""
import os,json,textwrap
from bisect import bisect_right
from pathlib import Path
import numpy as np
from manim import *
from check_alu import addsub,alu,comparisons
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

class SharedAdder(VGroup):
 """Four bitwise XORs and the first carry-in share the same SUB net."""
 def __init__(self,a=5,b=3,sub=0):
  super().__init__();self.a=a;self.b=b
  self.adder=pill('ADDER · 4-bit',6.8,1.4,GREEN,38).move_to([0,-.8,0]);self.add(self.adder)
  self.blabels=[];self.xoutputs=[];self.xors=VGroup();self.control=VGroup()
  for i,x in enumerate([-2.4,-.8,.8,2.4]):
   bit=3-i
   lb=txt(str((b>>bit)&1),36,PURPLE).move_to([x-.2,4.4,0]);self.blabels.append(lb)
   xo=pill('XOR',1.15,.65,ORANGE,21).move_to([x,1.8,0]);self.xors.add(xo)
   q=txt('0',30,PURPLE).move_to([x,.6,0]);self.xoutputs.append(q)
   self.add(lb,ln((x-.2,4.0),(x-.2,2.125),PURPLE),xo,ln((x,1.475),(x,1),PURPLE),q,ln((x,.2),(x,-.1),PURPLE))
   self.control.add(ln((x+.2,3.3),(x+.2,2.125),ORANGE),Dot([x+.2,3.3,0],radius=.045,color=ORANGE))
  self.control.add(route((-3.1,3.3),(3.8,3.3),(3.8,-.8),(3.4,-.8),c=ORANGE,w=2.5))
  self.sublabel=pill('SUB = 0',2.3,.65,ORANGE,27).move_to([-2.8,3.3,0]);self.cin=txt('Cin=0',25,ORANGE).move_to([4.1,.1,0])
  self.alabel=txt(f'A={a:04b}',29,BLUE).move_to([-3.9,1.2,0]);self.add(route((-4.5,.8),(-4.5,-.8),(-3.4,-.8),c=BLUE))
  self.result=pill('R = 1000',3.2,.8,GREEN,34).move_to([-.7,-2.65,0]);self.carry=pill('Cout=0',2.2,.7,ORANGE,25).move_to([3,-2.65,0])
  self.add(self.control,self.sublabel,self.cin,self.alabel,ln((-.7,-1.5),(-.7,-2.25),GREEN),ln((2.8,-1.5),(2.8,-2.3),ORANGE),self.result,self.carry,txt('B의 각 비트마다 XOR  /  SUB → Cin',24,GRAY).move_to([0,5.2,0]))
  self.state(sub)
 def state(self,sub):
  f=addsub(self.a,self.b,sub)
  setlabel(self.sublabel[1],f'SUB = {sub}',ORANGE,27,2)
  setlabel(self.cin,f'Cin={sub}',ORANGE,25)
  for j,q in enumerate(self.xoutputs):setlabel(q,str((f['b_input']>>(3-j))&1),PURPLE,30)
  setlabel(self.result[1],f'R = {f["result"]:04b}',GREEN,34,2.9);setlabel(self.carry[1],f'Cout={f["carry"]}',ORANGE,25,2)
  self.control.set_stroke(opacity=1 if sub else .42);self.sub=sub;return self

class ALUDiagram(VGroup):
 """A single arithmetic candidate, two logic candidates, three distinct MUX pins."""
 def __init__(self,opcode=0,comparison=False):
  super().__init__();self.fixed_wires=VGroup();self.candidates=[];self.paths=VGroup();self.blocks=VGroup()
  self.frame=RoundedRectangle(width=10.4,height=7.0,corner_radius=.2,color=EDGE,stroke_width=2).move_to([-.1,.3,0]);self.add(self.frame)
  self.inputs=VGroup(txt('A=0101',28,BLUE).move_to([-4.3,3.4,0]),txt('B=0011',28,PURPLE).move_to([-2.3,3.4,0]));self.add(self.inputs)
  for x,col in [(-4.3,BLUE),(-3.6,PURPLE)]:
   self.fixed_wires.add(ln((x,2.9),(x,-1.7),col))
   for y in [1.5,0,-1.5]:
    yy=y+(.2 if col==BLUE else -.2);self.fixed_wires.add(route((x,y),(x,yy),(-3,yy),c=col),Dot([x,yy,0],radius=.04,color=col))
  self.fixed_wires.add(route((-2.3,3.05),(-2.3,2.9),(-3.6,2.9),c=PURPLE))
  for j,(y,name,col) in enumerate([(1.5,'ADD/SUB',GREEN),(0,'AND',BLUE),(-1.5,'OR',PURPLE)]):
   block=pill(name,2.1,.9,col,27).move_to([-1.95,y,0]);self.blocks.add(block)
   val=txt('0000',27,INK).move_to([.15,y+.35,0]);self.candidates.append(val)
   self.paths.add(ln((-.9,y),(1.3,y),GRAY,3));self.add(block,val)
  self.mux=Polygon([1.3,2.25,0],[2.45,1.65,0],[2.45,-1.65,0],[1.3,-2.25,0],color=INK,fill_color=PANEL,fill_opacity=1,stroke_width=2)
  self.add(self.fixed_wires,self.paths,self.mux,txt('MUX',25).rotate(PI/2).move_to([1.9,0,0]))
  self.ports=VGroup(*[Dot([1.3,y,0],radius=.065,color=GRAY) for y in [1.5,0,-1.5]]);self.add(self.ports)
  self.outwire=ln((2.45,0),(3,0),GREEN,3);self.out=pill('1000',1.7,.85,GREEN,34).move_to([3.85,0,0]);self.add(self.outwire,self.out)
  self.sel=pill('SEL=00',2.1,.6,ORANGE,25).move_to([1.9,-2.75,0]);self.decoder=pill('DECODE',1.9,.55,ORANGE,20).move_to([-.8,-2.75,0])
  self.ctrl=VGroup(ln((1.9,-2.45),(1.9,-2),ORANGE),ln((.85,-2.75),(.15,-2.75),ORANGE),route((-1.75,-2.75),(-2.95,-2.75),(-2.95,2.35),(-1.95,2.35),(-1.95,1.95),c=ORANGE))
  self.sublabel=txt('SUB=0',21,ORANGE).move_to([-1.95,2.6,0]);self.add(self.ctrl,self.sel,self.decoder,self.sublabel)
  self.codelegend=txt('00 ADD   01 SUB   10 AND   11 OR',23,GRAY).move_to([0,-3.55,0]);self.add(self.codelegend)
  if comparison:
   self.add(pill('FLAGS → COMPARE',3.9,.6,ORANGE,24).move_to([-1.3,4.35,0]),route((-1.4,1.95),(-1.4,3.7),(-1.3,3.7),(-1.3,4.05),c=ORANGE))
  self.state(opcode)
 def state(self,opcode):
  m=alu(5,3,opcode)
  for i,v in enumerate(m['candidates']):setlabel(self.candidates[i],f'{v:04b}',INK,27)
  for i,p in enumerate(self.paths):p.set_color(GREEN if i==m['port'] else GRAY).set_stroke(opacity=1 if i==m['port'] else .45)
  for i,p in enumerate(self.ports):p.set_color(GREEN if i==m['port'] else GRAY)
  setlabel(self.out[1],f'{m["result"]:04b}',GREEN,34,1.4);setlabel(self.sel[1],f'SEL={opcode:02b}',ORANGE,25,1.8);setlabel(self.sublabel,f'SUB={m["sub"]}',ORANGE,21)
  self.opcode=opcode;return self
 def topology(self):
  return tuple(tuple(np.round(p.get_all_points().ravel(),6)) for p in [self.frame,self.fixed_wires,self.paths,self.mux,self.outwire,self.ctrl])

class ALUScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.04:raise RuntimeError(f'Scene {self.index+1} overrun: {self.time}>{target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,c=GRAY):self.notice.become(txt(s,24,c,7.6 if VERT else 14).move_to([0,-3.8 if VERT else -2.15,0]))
 def construct(self):
  self.always_update_mobjects=True;m=MANIFEST[self.index];self.start=m['start'];self.end=m['end'];top=7.2 if VERT else 3.88
  self.add(txt('GPU 개론  /  05',21,GRAY).move_to([0,top,0]),txt(m['title'],36 if VERT else 38,INK,7.85 if VERT else 14.5).move_to([0,top-.73,0]))
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
  bar.add_updater(lambda m:m.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/175)))
  self.add(base,bar,txt(f'{self.index+1:02} / 16',17,GRAY).move_to([x-.55,y+.27,0]))
  getattr(self,m['method'])()
  self.at(self.end)
 def show(self,*objects):self.play(*[FadeIn(o,shift=UP*.1) for o in objects],run_time=.4)
 def replace(self,old,new):self.play(FadeOut(old),FadeIn(new),run_time=.4)
 def centered(self,m,width=7.3):
  if m.width>width:m.scale_to_fit_width(width)
  if m.height>(7.2 if VERT else 4.2):m.scale_to_fit_height(7.2 if VERT else 4.2)
  return m.move_to([0,1.4 if VERT else .35,0])
 def equation(self,s,color=INK,size=65):return self.centered(txt(s,size,color),7 if VERT else 11)
 def blocks(self,names):
  return self.centered(VGroup(*[pill(s,2.6,1.15,GREEN if i==0 else GRAY,28) for i,s in enumerate(names)]).arrange(DOWN if VERT else RIGHT,buff=.6),7.4 if VERT else 12)
 def adder(self):return pill('ADDER · 4-bit',3.8,1.1,GREEN,34)
 def diagram(self,op=0,comparison=False):return self.centered(ALUDiagram(op,comparison),7.6 if VERT else 12.5)
 def shared_diagram(self,sub=0):return self.centered(SharedAdder(sub=sub),7.6 if VERT else 11)
 def state(self,g,op):
  if isinstance(g,ALUDiagram):
   before=g.topology();g.state(op);assert g.topology()==before,'Control must not change physical topology'
  else:g.state(op)
 def newcircuits(self):
  fas=VGroup(*[pill(f'FA {i}',1.2,.8,GREEN,25) for i in [3,2,1,0]]).arrange(RIGHT,buff=.45)
  wires=VGroup(*[Arrow(fas[i+1].get_left(),fas[i].get_right(),buff=.02,color=ORANGE,stroke_width=2) for i in range(3)])
  g=self.centered(VGroup(fas,wires));self.show(g);self.note('네 개의 전가산기 → 4비트 가산기')
  self.at(3);ad=self.centered(self.adder());self.replace(g,ad)
  self.at(5)
  extras=VGroup(pill('SUBTRACT?',2.7,1,GRAY,26),pill('COMPARE?',2.7,1,GRAY,26))
  if VERT:
   self.play(ad.animate.move_to([0,3.3,0]),run_time=.5);extras.arrange(DOWN,buff=.6).move_to([0,.6,0])
  else:
   self.play(ad.animate.move_to([-4.3,.7,0]),run_time=.5);extras.arrange(RIGHT,buff=.55).move_to([2,.7,0])
  self.show(extras);self.note('One Operation → One Circuit?')
  self.at(10)
  detail=VGroup()
  for obj in [ad,*extras]:
   points=VGroup(*[Dot(radius=.04,color=GRAY).move_to(obj.get_bottom()+np.array([x,-.45,0])) for x in [-.65,0,.65]])
   detail.add(points,ln(tuple(points[0].get_center()[:2]),tuple(points[-1].get_center()[:2]),GRAY))
  self.show(detail)
 def cost(self):
  g=self.blocks(['ADD','SUB','COMPARE']);self.show(g)
  area=SurroundingRectangle(g,buff=.35,color=ORANGE);self.show(area);self.note('더 많은 소자 + 배선 + 구현 면적',ORANGE)
  self.play(area.animate.stretch(1.12,0),run_time=1)
  self.at(19);self.play(g[1:].animate.set_opacity(.3),Indicate(g[0],color=GREEN),run_time=.7);self.note('Reuse Existing Hardware',GREEN)
 def complement(self):
  ad=self.adder().move_to([0,-1.0 if VERT else -.8,0]);eq=txt('A − B',56).move_to([0,2.7 if VERT else 1.8,0]);self.show(ad,eq)
  self.at(25);self.play(Transform(eq,txt('A + (−B)',56).move_to(eq)),run_time=.7)
  self.at(30);self.note('고정 n비트: A − B ≡ A + NOT(B) + 1  (mod 2ⁿ)')
  self.at(33)
  bits=VGroup(*[pill(v,.95,.9,PURPLE,39) for v in '0011']).arrange(RIGHT,buff=.2).move_to([0,1 if VERT else .5,0]);self.show(bits)
  for i,v in enumerate('1100'):
   self.play(Transform(bits[i][1],txt(v,39,PURPLE).move_to(bits[i][1])),run_time=.35)
  self.at(36);one=txt('+ 1 → 1101',36,ORANGE).move_to([0,0 if VERT else -1.65,0]);self.show(one)
  self.at(39);self.note('Two’s Complement  /  2의 보수  ·  고정 비트 폭',ORANGE)
 def example(self):
  eq=txt('5 − 3  /  4-bit',45).move_to([0,4.3 if VERT else 1.9,0]);self.show(eq)
  ad=self.adder().move_to([0,.3 if VERT else -.15,0]);self.show(ad)
  self.at(44)
  a=txt('A = 0101',39,BLUE).move_to([-1.8,2.7 if VERT else 1,0]);b=txt('B = 0011',39,PURPLE).move_to([1.8,2.7 if VERT else 1,0]);self.show(a,b)
  self.at(47);self.play(Transform(b,txt('NOT B = 1100',33,PURPLE).move_to(b)),run_time=.7)
  self.at(49);self.play(Transform(b,txt('+ 1 → 1101',33,ORANGE).move_to(b)),run_time=.7)
  self.at(51)
  lines=VGroup(route((-1.8,2.25 if VERT else .7),(-1.8,.85 if VERT else .4),c=BLUE),route((1.8,2.25 if VERT else .7),(1.8,.85 if VERT else .4),c=PURPLE));self.show(lines)
  self.note('0101 + 1101 = 10010₂')
  self.at(54)
  y=-1.6 if VERT else -1.35
  out=pill('R = 0010 = 2',3.1,.75,GREEN,30).move_to([-.6,y,0]);carry=pill('Cout=1',1.7,.65,ORANGE,24).move_to([2.4,y,0])
  self.show(out,carry,ln((-.6,ad.get_bottom()[1]),(-.6,y+.375),GREEN),ln((1.5,ad.get_bottom()[1]),(2.4,y+.325),ORANGE));self.note('결과 버스는 하위 4비트 · Cout은 별도 출력',GREEN)
 def shared(self):
  d=self.shared_diagram(0);self.show(d.adder,d.alabel,d.result,d.carry);self.note('같은 ADDER를 유지하고 입력 경로를 확장')
  self.at(61)
  # Re-add the existing children through their parent; the ADDER is never replaced.
  self.remove(d.adder,d.alabel,d.result,d.carry);self.add(d)
  self.play(Indicate(d.xors,color=ORANGE),run_time=.8);self.note('SUB → B의 네 XOR와 최초 Cin',ORANGE)
  self.at(65);self.state(d,0);self.note('SUB=0: 0101 + 0011 + 0 = 1000',GREEN)
  self.at(67);self.state(d,1);self.note('SUB=1: 0101 + 1100 + 1 = 1 | 0010',GREEN)
 def compare(self):
  ad=self.adder().move_to([-1.8,1.7 if VERT else .8,0]);comp=pill('COMPARE?',2.8,.9,GRAY,28).move_to([2.1,1.7 if VERT else .8,0]);self.show(ad,comp,Line(ad.get_right(),comp.get_left(),color=ORANGE));self.note('공유 가산기를 SUB=1로 사용')
  self.at(73)
  calculation=txt('0101 − 0101 = 0000',37,GREEN).move_to([0,3.7 if VERT else 1.85,0]);self.show(calculation)
  detect=pill('ZERO DETECT',3.2,.8,ORANGE,28).move_to([0,-.1 if VERT else -.35,0]);output=txt('Z=1 → A=B',34,GREEN).move_to([0,-1.3,0]);self.show(detect,output);self.note('추가 검출 논리: Z = NOT(R₃ OR R₂ OR R₁ OR R₀)')
  self.at(78)
  self.play(Transform(calculation,txt('0101 − 0110 = 1111',37,ORANGE).move_to(calculation)),run_time=.5)
  self.remove(detect,output);setlabel(comp[1],'FLAG LOGIC',ORANGE,26)
  lines=VGroup(txt('Z=0   N=1   V=0   Cout=0',29,ORANGE),txt('signed LT = N ⊕ V = 1',29,GREEN),txt('unsigned LT = NOT Cout = 1',29,GREEN)).arrange(DOWN,buff=.25).move_to([0,-.7 if VERT else -.65,0]);self.show(lines)
  self.note('부호 있는 비교: N과 V  /  부호 없는 비교: 빌림 정보')
 def reuse(self):
  old=VGroup(*[pill(s,2.3,.8,GRAY,27) for s in ['ADD','SUB','COMPARE']]).arrange(DOWN,buff=.35)
  shared=VGroup(self.adder(),pill('입력 변환 + 비교 판단',4.5,.7,ORANGE,26).shift(DOWN*1.2))
  g=VGroup(old,shared).arrange(DOWN if VERT else RIGHT,buff=1);self.show(self.centered(g,7.5 if VERT else 12));self.note('독립 계산 경로 → 공통 가산기 + 보조 논리')
  self.at(89);self.play(old.animate.set_opacity(.3),Indicate(shared[0],color=GREEN),run_time=.7);self.note('ADD · SUB · COMPARE  /  Reuse Existing Hardware',GREEN)
 def logic(self):
  shared=self.centered(VGroup(self.adder(),txt('SHARED ARITHMETIC',27,GREEN).shift(DOWN*1.2)));self.show(shared);self.note('공유할 수 있는 산술 경로를 공유')
  self.at(97)
  g=self.blocks(['ADD / SUB','AND','OR']);self.replace(shared,g);self.note('AND · OR에는 별도의 논리 구조')
 def integrate(self):
  d=self.diagram(0);self.show(d.frame,d.fixed_wires,d.inputs,d.blocks);self.note('공통 A·B → 산술 경로와 논리 경로로 분기')
  self.at(106);self.play(Indicate(d.blocks[0],color=GREEN),run_time=.7);self.play(Indicate(d.blocks[1:],color=PURPLE),run_time=.7);self.note('각 연산 회로는 미리 설계된 구조')
 def mux(self):
  d=self.diagram(0);self.show(d);self.note('각 결과선은 서로 다른 MUX 입력 핀에 연결')
  self.at(115);self.play(Indicate(d.mux,color=ORANGE),run_time=.6);self.note('MULTIPLEXER  /  MUX  /  선택 회로',ORANGE)
  self.at(117);self.state(d,2)
  self.at(118.5);self.state(d,3)
 def select(self):
  d=self.diagram(0);self.show(d);self.note('A=0101 · B=0011 고정  /  선택 코드는 예시')
  self.at(123)
  for t,op,name in [(123,0,'ADD'),(124.5,1,'SUB'),(126,2,'AND'),(127.5,3,'OR')]:
   self.at(t);self.state(d,op);self.note(f'SEL={op:02b}  {name} → {alu(5,3,op)["result"]:04b}',GREEN)
 def name(self):
  d=self.diagram(3);self.show(d);self.note('산술 연산 + 논리 연산 + 결과 선택')
  self.at(132)
  box=VGroup(pill('ALU',5,2,GREEN,65),txt('Arithmetic Logic Unit',31).shift(DOWN*1.6));self.replace(d,self.centered(box));self.note('산술논리장치',GREEN)
 def fixed(self):
  d=self.diagram(0);self.show(d);self.note('고정: 회로·배선  /  변화: 제어 신호·값')
  for t,op in [(137,1),(138.5,2),(140,3)]:self.at(t);self.state(d,op)
  self.at(141);self.note('Fixed Hardware, Variable Control',ORANGE)
  for t,op in [(142,0),(144,1),(146,3)]:self.at(t);self.state(d,op)
 def overview(self):
  d=self.diagram(1,comparison=True);self.show(d);self.note('공유 가산기 + 비교 판단 + AND/OR + MUX')
  self.at(152);self.state(d,2);self.play(Indicate(d.frame,color=GREEN),run_time=.8);self.note('Hardware Reuse + Functional Integration',GREEN)
 def limits(self):
  d=self.diagram(3);self.show(d);self.note('DIV: 이 예시 ALU에 직접 구현되지 않음',ORANGE)
  mark=pill('DIV ?',1.8,.7,GRAY,29).move_to([0,4.4 if VERT else 2.25,0]);self.show(mark)
 def conclusion(self):
  old=VGroup(*[pill(s,2.2,.65,GRAY,24) for s in ['ADD','SUB','COMPARE','AND','OR']]).arrange(DOWN,buff=.18)
  new=self.diagram(1);new.scale(.7);g=VGroup(old,new).arrange(DOWN if VERT else RIGHT,buff=.7);self.show(self.centered(g,7.6 if VERT else 12));self.note('공유할 연산 · 별도 기능 · 결과 선택을 함께 설계')
  self.at(167);self.play(Indicate(new.blocks[0],color=GREEN),run_time=.7);self.note('공통 경로를 재사용하고 필요한 기능을 통합')
  self.at(171)
  keys=VGroup(*[txt(s,39,c) for s,c in [('REUSE',GREEN),('INTEGRATE',BLUE),('SELECT',ORANGE)]]).arrange(DOWN if VERT else RIGHT,buff=.6)
  block=VGroup(pill('ALU',3.6,1.2,GREEN,51),keys.shift(DOWN*2))
  self.replace(g,self.centered(block,7.5 if VERT else 12));self.note('REUSE → INTEGRATE → SELECT',GREEN)
