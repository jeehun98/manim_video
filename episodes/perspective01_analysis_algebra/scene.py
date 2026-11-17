"""Exact user timing; two approaches to one strictly positive quartic."""
import json,sys
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene,label
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE,GOLD,GREEN,RED,INK,MUTED='#42B8E8','#E8B45D','#65D6AC','#EF7185','#E8EDF5','#8B9CB7'
POLY=r'x^4-x^2-6x+10'
SQUARES=r'(x^2-1)^2+(x-3)^2'
def polynomial(x):return x**4-x**2-6*x+10

def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=45,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def graph(y=0):
 ax=Axes(x_range=[-2,3,1],y_range=[0,30,10],x_length=6.6,y_length=3.3,tips=False,axis_config={'color':MUTED,'stroke_width':1.5}).move_to(UP*y)
 g=ax.plot(polynomial,x_range=[-1.55,2.5,.025],color=BLUE,stroke_width=3)
 return ax,g
class PerspectiveScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.6)
  self.add(txt('MATHEMATICS  /  ANALYSIS & ALGEBRA',7,17,MUTED))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]+getattr(self,"proof_fixed",[])
  obs=[m for m in self.mobjects if m not in keep and m.get_center()[1]<6.5]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def row(self,lines):
  return VGroup(*[eq(s,y,sz,c) for s,y,sz,c in lines])
 def proof_reference(self):
  formula=MathTex(r'f(x)=',r'x^4-x^2',r'-6x+10',font_size=40,color=INK).move_to(UP*4.65)
  formula[1].set_color(BLUE);formula[2].set_color(GOLD)
  goal=eq(r'\mathrm{Goal}:\quad f(x)>0',-4.35,28,GREEN)
  self.proof_fixed=[formula,goal]
  self.add(*self.proof_fixed)
 def proof_equation(self,s,y,size,color):
  m=MathTex(s,font_size=size,color=color,substrings_to_isolate=[r'x^4-x^2',r'10-6x'])
  if color==INK:
   m.set_color_by_tex(r'x^4-x^2',BLUE)
   m.set_color_by_tex(r'10-6x',GOLD)
   if s==r'6x\leq9':m.set_color(GOLD)
  if m.width>7.4:m.scale_to_fit_width(7.4)
  return m.move_to(UP*y)
 def reveal_panel(self,panel):
  # Condition -> term estimates -> lower bound, within the fixed speech window.
  self.show(panel[0],run_time=.3)
  for line in panel[1:]:self.show(line,run_time=.4)
 def intervals(self,done=0):
  ax=NumberLine(x_range=[-2,3,1],length=7,tick_size=.08,include_numbers=False,color=MUTED).move_to(UP*3.5)
  self.add(ax)
  for x,y in [(-1,3.95),(1,3.95),(1.5,3.1),(2,3.95)]:
   self.add(Dot(ax.n2p(x),radius=.045,color=INK),eq(str(x),y,24,x=ax.n2p(x)[0],width=1))
  cuts=[-2,-1,1,1.5,2,3]
  seg=[Line(ax.n2p(a),ax.n2p(b),color=GREEN if i<done else MUTED,stroke_width=7) for i,(a,b) in enumerate(zip(cuts,cuts[1:]))]
  self.add(*seg,txt('←',3.5,24,MUTED,x=-3.8),txt('→',3.5,24,MUTED,x=3.8))
  return seg
 def panel(self,condition,formulas):
  return VGroup(txt(condition,2.45,34,BLUE),*[self.proof_equation(s,y,sz,c) for s,y,sz,c in formulas])
class Shot01(PerspectiveScene):
 shot=0
 def s01(self):
  self.show(eq(r'f(x)=x^2',2.6,60),txt('하나의 대상',1.2,29,MUTED));self.to(3)
  self.show(txt('해석학',-.1,44,BLUE,x=-2),txt('대수학',-.1,44,GOLD,x=2),txt('Analysis',-1,25,BLUE,x=-2),txt('Algebra',-1,25,GOLD,x=2));self.to(7)
  self.clear_body();ax=Axes(x_range=[-2,2,1],y_range=[0,4,1],x_length=6,y_length=3,tips=False).move_to(UP*.3);g=ax.plot(lambda x:x*x,x_range=[-1.9,1.9],color=BLUE);t=ValueTracker(-1.8)
  dot=always_redraw(lambda:Dot(ax.c2p(t.get_value(),t.get_value()**2),color=BLUE));self.show(ax,g,txt('극한 · 연속성 · 변화',3.5,39,BLUE),eq(r'x\to a\quad f(x)\to f(a)',-2.6,38,BLUE));self.add(dot);self.play(t.animate.set_value(1),run_time=4.5);self.to(13)
  self.clear_body();a=eq(r'(a+b)^2',1,66,GOLD);self.show(a,txt('연산 · 규칙 · 구조',3.5,39,GOLD));self.play(TransformMatchingTex(a,eq(r'a^2+2ab+b^2',1,57,GOLD)),run_time=1.5);self.to(18)
  self.clear_body();self.show(txt('같은 문제를',2,43),txt('두 방식으로 증명한다면?',.4,43,GREEN));self.to(23)
class Shot02(PerspectiveScene):
 shot=1
 def s02(self):
  self.to(25);p=eq(r'f(x)='+POLY,3.3,47);self.play(Write(p),run_time=2.5);self.to(28)
  a,g=graph(-.1);self.show(a,g,eq(r'f(x)>0\quad(\forall x\in\mathbb R)',-2.75,43,GREEN),txt('그래프는 관찰 · 증명은 이제부터',-4,24,MUTED));self.to(33)
class Shot03(PerspectiveScene):
 shot=2
 def s03(self):
  self.proof_reference();seg=self.intervals();self.show(txt('같은 식을 구간별로 비교',1.3,37),txt('파랑: 앞의 두 항  /  노랑: 나머지 두 항',-.2,26,MUTED));self.to(37)
  self.clear_body();seg=self.intervals();self.play(seg[0].animate.set_color(BLUE),run_time=.3)
  p=self.panel('①  x ≤ −1',[(r'x^4-x^2=x^2(x^2-1)\geq0',1,40,INK)]);self.reveal_panel(p);self.to(42)
  q=self.row([(r'10-6x\geq16>0',-.6,43,GOLD),(r'f(x)=(x^4-x^2)+(10-6x)>0',-2.3,37,GREEN)]);self.show(q);self.play(seg[0].animate.set_color(GREEN));self.to(46)
  self.play(FadeOut(p),FadeOut(q));self.show(txt('다른 구간에도 그대로 쓸 수 있을까?',2.3,31,RED),eq(r'x=\frac12:\quad x^4=\frac1{16}<\frac14=x^2',.5,40,RED));self.to(52)
  self.show(txt('남은 구간에는 다른 비교가 필요',-2,33,BLUE));self.to(55)
class Shot04(PerspectiveScene):
 shot=3
 def s04(self):
  self.proof_reference();seg=self.intervals(done=1);self.play(seg[1].animate.set_color(BLUE),run_time=.3)
  p=self.panel('②  −1 ≤ x ≤ 1',[(r'x^4\geq0,\quad -x^2\geq-1,\quad -6x\geq-6',1.1,36,INK),(r'x^4-x^2-6x\geq-7\geq-8',-.3,41,INK),(r'f(x)\geq-8+10=2>0',-2,46,GREEN)])
  self.reveal_panel(p);self.to(61)
  self.play(FadeOut(p),seg[1].animate.set_color(GREEN),seg[2].animate.set_color(BLUE),run_time=.4)
  p=self.panel('③  1 ≤ x ≤ 1.5',[(r'x^4-x^2\geq0',1.1,43,INK),(r'6x\leq9',-.3,44,INK),(r'f(x)\geq0-9+10=1>0',-2,45,GREEN)]);self.reveal_panel(p);self.to(68)
  self.play(FadeOut(p),seg[2].animate.set_color(GREEN),seg[3].animate.set_color(BLUE),run_time=.4)
  p=self.panel('④  1.5 ≤ x ≤ 2',[(r'x^4-x^2=x^2(x^2-1)\geq\frac{45}{16}>2',1.05,38,INK),(r'10-6x\geq-2',-.5,43,INK),(r'f(x)>2-2=0',-2.2,48,GREEN)]);self.reveal_panel(p);self.to(76)
  self.play(FadeOut(p),seg[3].animate.set_color(GREEN),seg[4].animate.set_color(BLUE),run_time=.4)
  p=self.panel('⑤  x ≥ 2',[(r'x^4-x^2-6x=x(x-2)(x^2+2x+3)\geq0',1,33,INK),(r'x^4-x^2\geq6x',-.5,43,INK),(r'f(x)\geq6x-6x+10=10>0',-2.2,42,GREEN)]);self.reveal_panel(p);self.to(82)
  self.play(FadeOut(p),seg[4].animate.set_color(GREEN),run_time=.4)
  self.show(txt('다섯 구간이 모든 실수를 덮는다',1.4,34,GREEN),eq(r'\boxed{f(x)>0\quad\forall x\in\mathbb R}',-.6,47,GREEN),txt('구간별 비교로 증명 완료',-2.4,32));self.to(86)
class Shot05(PerspectiveScene):
 shot=4
 def s05(self):
  a=eq(POLY,1.7,53);self.show(a,txt('이번에는 식의 구조에 주목',3.9,33,GOLD));self.to(89)
  b=eq(r'(x^4-2x^2+1)+(x^2-6x+9)',1.7,42);b.set_color_by_tex('x',GOLD)
  self.play(TransformMatchingTex(a,b,transform_mismatches=True),run_time=1.6)
  c=MathTex(r'(x^2-1)^2','+',r'(x-3)^2',font_size=55).move_to(UP*1.7);c[0].set_color(BLUE);c[2].set_color(GOLD)
  self.play(TransformMatchingTex(b,c,transform_mismatches=True),run_time=1.6);self.to(94)
  self.show(eq(r'(x^2-1)^2\geq0',-.1,41,BLUE),eq(r'(x-3)^2\geq0',-1.2,41,GOLD))
  self.show(eq(r'x=\pm1\qquad\ne\qquad x=3',-2.5,38,RED),txt('동시에 0이 될 수 없다',-3.8,31,GREEN));self.to(99)
  self.clear_body();self.show(eq(SQUARES,2.4,50,GOLD),eq(r'\boxed{f(x)>0\quad\forall x\in\mathbb R}',.4,46,GREEN),txt('두 제곱항이 동시에 0이 될 수 없기 때문',-1.8,28));self.to(102)
class Shot06(PerspectiveScene):
 shot=5
 def s06(self):
  self.show(txt('구간별 비교',3.8,32,BLUE,x=-2),txt('구조 변형',3.8,32,GOLD,x=2))
  left=VGroup(*[eq(s,sz,28,BLUE,width=3.3,x=-2) for s,sz in [(r'x\leq-1',2.4),(r'-1\leq x\leq1',1.4),(r'1\leq x\leq1.5',.4),(r'1.5\leq x\leq2',-.6),(r'x\geq2',-1.6)]])
  self.show(left,eq(POLY,2,29,GOLD,width=3.5,x=2),eq(r'\Downarrow',.8,37,GOLD,x=2),eq(SQUARES,-.5,28,GOLD,width=3.5,x=2),eq(r'f(x)>0',-3.2,52,GREEN));self.to(109)
  self.clear_body();self.show(txt('짧은 증명 = 더 좋은 증명?',1.8,40,GOLD));self.to(112);self.show(txt('반드시 그렇지는 않다',-.3,40,GREEN));self.to(114)
  self.clear_body();self.show(txt('각 단계의 근거를 확인',3.9,37,BLUE))
  for s,y in [(r'x\leq-1\Rightarrow f(x)>0',2.3),(r'-1\leq x\leq1\Rightarrow f(x)\geq2',1.1),(r'1\leq x\leq1.5\Rightarrow f(x)\geq1',-.1),(r'1.5\leq x\leq2\Rightarrow f(x)>0',-1.3),(r'x\geq2\Rightarrow f(x)\geq10',-2.5)]:self.show(eq(s,y,35,BLUE),run_time=.6)
  self.to(120);self.clear_body();self.show(eq(POLY,2.8,46),eq(r'\Downarrow\quad?',1.2,64,RED),eq(SQUARES,-.5,47,GOLD),txt('어떻게 이 형태를 발견했을까?',-2.5,34,GOLD));self.to(126)
  self.clear_body();self.show(txt('해석적 관점의 예시',2.7,37,BLUE),txt('구간별 성질을 비교',1.4,29),txt('대수적 관점의 예시',-.7,37,GOLD),txt('다른 표현에서 구조를 발견',-2,29),txt('학문 전체를 정의하는 구분은 아니다',-3.8,24,MUTED));self.to(132)
class Shot07(PerspectiveScene):
 shot=6
 def s07(self):
  ax,g=graph(.6);t=ValueTracker(-1.3);dot=always_redraw(lambda:Dot(ax.c2p(t.get_value(),polynomial(t.get_value())),color=BLUE));self.add(ax,g,dot)
  self.show(txt('어떻게 변할까?',3.7,35,BLUE),txt('어떤 값에 가까워질까?',-2,32,BLUE),txt('그 과정에서 무엇이 유지될까?',-3.1,30));self.play(t.animate.set_value(1.3),run_time=4);self.to(138)
  self.clear_body();self.show(eq(r'(a+b)^2=a^2+2ab+b^2',3.7,42,GOLD))
  pieces=VGroup()
  for w,h,c,x,y,s in [(2,2,BLUE,-.7,.7,'a²'),(2,1,GOLD,-.7,-.8,'ab'),(1,2,GOLD,.8,.7,'ab'),(1,1,GREEN,.8,-.8,'b²')]:
   pieces.add(VGroup(Rectangle(width=w,height=h,fill_color=c,fill_opacity=.22,stroke_color=c),txt(s,size=28,color=c)).move_to([x,y,0]))
  self.show(pieces,txt('연산의 규칙 · 표현 사이의 관계',-2.7,30,GOLD));self.play(pieces.animate.arrange_in_grid(rows=2,cols=2,buff=.35).move_to(DOWN*.1),run_time=1.2);self.to(145)
  self.clear_body();self.show(txt('함수의 성질',2.8,41,BLUE),eq(r'\updownarrow',1.1,68,GREEN),txt('연산과 구조',-.5,41,GOLD),txt('하나의 문제에 두 관점을 함께 사용',-2.5,31),txt('실제 수학에서 두 분야는 연결되어 있다',-3.7,26,MUTED));self.to(151)
class Shot08(PerspectiveScene):
 shot=7
 def s08(self):
  self.show(eq(POLY,3.9,47),txt('같은 대상',2.7,30,MUTED));a,g=graph(-.2);small=VGroup(a,g).scale(.5).move_to([-2,.3,0]);self.show(small,eq(SQUARES,.4,31,GOLD,width=3.6,x=2),eq(r'f(x)>0',-1.8,38,GREEN,x=-2),eq(r'f(x)>0',-1.8,38,GREEN,x=2),txt('서로 다른 성질에 주목',-3.4,35,GREEN));self.to(158)
  self.play(Circumscribe(small,color=BLUE),Circumscribe(self.mobjects[-4],color=GOLD),run_time=1)
  self.show(txt('조건을 하나씩 추적  /  표현을 바꾸어 발견',-4.3,24,MUTED));self.to(164)
class Shot09(PerspectiveScene):
 shot=8
 def s09(self):
  self.show(txt('계산을 넘어',3.2,44),txt('무엇을 관찰할 것인가?',1.2,44,GREEN));self.to(169)
  self.show(txt('해석학',-.8,41,BLUE,x=-1.7),txt('대수학',-.8,41,GOLD,x=1.7),txt('같은 문제, 서로 다른 관점',-2.7,35),txt('관점을 선택하는 것도 문제 해결의 일부',-4,25,MUTED));self.to(173)
