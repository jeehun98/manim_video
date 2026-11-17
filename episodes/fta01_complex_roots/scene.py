"""177-second exact-time FTA portrait; independent scenes and shared subtitle renderer."""
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
BLUE,GOLD,RED,GREEN,INK,MUTED='#42B8E8','#F2AF56','#EF6586','#64D6B0','#E8EDF5','#8B9CB7'
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=45,color=INK,width=7.4):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to(UP*y)
def poly(y=2):return VGroup(eq(r'x^5-3x^4+7x^3',size=43),eq(r'-2x^2+5x+11=0',size=43)).arrange(DOWN,buff=.3).move_to(UP*y)
def plane(y,color):
 p=ComplexPlane(x_range=[-2,2,1],y_range=[-1.6,1.6,1],x_length=5.7,y_length=3.5,background_line_style={'stroke_opacity':.18,'stroke_color':color},axis_config={'stroke_opacity':.5}).move_to(UP*y)
 return p
class FTAScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.65)
  self.add(txt('MATHEMATICS  /  COMPLEX ROOTS',7,18,MUTED))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in keep and m.get_center()[1]<6.5],run_time=.5)
 def mapping(self,R=1.15,theta=0):
  a,b=plane(2.7,BLUE),plane(-1.45,GOLD)
  r,t=ValueTracker(R),ValueTracker(theta)
  # Fixed coordinates and scale: output radius is exactly R^5.
  ci=always_redraw(lambda:Circle(radius=max(r.get_value(),.001)*1.15,color=BLUE,stroke_width=3).move_to(a.c2p(0,0)))
  # Use explicit equal unit axes to preserve circles.
  for p in (a,b):p.stretch_to_fit_width(4.6);p.stretch_to_fit_height(3.68)
  ci=always_redraw(lambda:Circle(radius=max(r.get_value(),.001)*1.15,color=BLUE).move_to(a.c2p(0,0)))
  co=always_redraw(lambda:Circle(radius=max(r.get_value()**5,.001)*1.15,color=GOLD).move_to(b.c2p(1,0)))
  di=always_redraw(lambda:Dot(a.c2p(*(r.get_value()*np.array([np.cos(t.get_value()),np.sin(t.get_value())]))),color=BLUE,radius=.075))
  do=always_redraw(lambda:Dot(b.c2p(1+r.get_value()**5*np.cos(5*t.get_value()),r.get_value()**5*np.sin(5*t.get_value())),color=GOLD,radius=.075))
  self.add(a,b,ci,co,di,do,Dot(b.c2p(0,0),color=RED,radius=.07),txt('입력 z',4.8,25,BLUE),txt('출력 P(z)',.6,25,GOLD),txt('0',-1.75,20,RED,x=-.22),txt('1',-1.75,20,GREEN,x=1.15))
  return r,t,a,b
class Shot01(FTAScene):
 shot=0
 def s01(self):
  self.show(txt('모든 다항방정식에는',2.7,43),txt('해가 존재한다',1.35,56,GREEN),txt('복소수 범위 · 1차 이상',-.2,27,MUTED));self.to(3)
  self.clear_body();p=poly(2.1);self.show(txt('5차 방정식',3.9,28,BLUE));self.to(6);self.play(LaggedStart(*[Write(m) for m in p],lag_ratio=.2),run_time=6);self.to(13)
  qs=VGroup(*[eq('?',size=48) for _ in range(5)]).arrange(RIGHT,buff=.72).move_to(DOWN*.6);self.show(qs);self.to(16)
  rs=eq(r'r_1\quad r_2\quad r_3\quad r_4\quad r_5',-.6,40,GOLD);self.play(ReplacementTransform(qs,rs));self.show(txt('5개의 근 · 중복도 포함',-2.4,37,GREEN));self.to(23)
class Shot02(FTAScene):
 shot=1
 def s02(self):
  chain=eq(r'\mathbb N\subset\mathbb Z\subset\mathbb Q\subset\mathbb R\subset\mathbb C',3.8,41,BLUE);self.show(chain,txt('어떻게 가능할까?',1.9,43,GOLD));self.to(30)
  a=eq(r'2-5=-3\quad\in\mathbb Z',1.3);b=eq(r'1\div2=\frac12\quad\in\mathbb Q',-.3);self.show(a,b);self.to(35)
  self.play(FadeOut(a),FadeOut(b));self.show(eq(r'x^2=-1',1.4,60),txt('실수에서는 불가능',-.2,31,RED));self.to(39)
  self.clear_body();p=plane(.1,BLUE);self.show(p,eq(r'i^2=-1',3.6,54,GOLD));self.show(Dot(p.c2p(0,1),color=GOLD),txt('i',1.6,30,GOLD,x=.35));self.to(44)
  dot=Dot(p.c2p(1,1),color=GREEN);self.show(dot,eq(r'a+bi',-2.6,49,GREEN));self.play(Create(DashedLine(p.c2p(0,0),p.c2p(1,0),color=BLUE)),Create(DashedLine(p.c2p(1,0),p.c2p(1,1),color=GOLD)));self.to(48)
class Shot03(FTAScene):
 shot=2
 def s03(self):
  self.show(eq(r'\mathbb C',3.6,95,BLUE),txt('새로운 종류의 수가 필요 없다',1.8,34));self.to(51)
  for y,s in [(0,r'z^2+1'),(-1.1,r'z^3-1'),(-2.2,r'z^5+\cdots')]:self.show(eq(s+r'=0\quad\checkmark',y,39,GREEN))
  self.to(59);self.clear_body();self.show(eq(r'P(z)=0\quad\exists z\in\mathbb C',2.4,44,GREEN),txt('복소수 계수 · n ≥ 1 · 최고차항 계수 ≠ 0',3.7,23,MUTED));self.to(64)
  self.show(eq(r'P(z)=a_n\prod_{k=1}^{n}(z-r_k)',.6,43),txt('n차 → n개의 복소수 근',-1.1,38,GOLD),txt('중복도 포함',-2.1,29,MUTED));self.to(70);self.show(txt('대수학의 기본정리',-3.5,43,GREEN));self.to(73)
class Shot04(FTAScene):
 shot=3
 def s04(self):
  self.show(txt('왜 반드시 근이 존재할까?',1.5,43,GOLD));self.to(78);self.clear_body()
  r,t,a,b=self.mapping(1.12);self.add(txt('간단한 예시  P(z)=z⁵+1',6.2,23,MUTED));self.show(eq(r'z\longmapsto P(z)',-4.05,34));self.to(82)
  self.play(t.animate.set_value(TAU),run_time=5,rate_func=linear);self.to(87)
  self.play(t.animate.set_value(2*TAU),run_time=5,rate_func=linear)
class Shot05(FTAScene):
 shot=4
 def s05(self):
  self.show(eq(r'z=Re^{it}',3.9,43,BLUE),eq(r'a_5z^5=a_5R^5e^{5it}',2.65,43,GOLD),txt('충분히 큰 원: 최고차항이 지배',1.4,29,MUTED));self.to(97)
  t=ValueTracker(0);a=np.array([-2, -.7,0]);b=np.array([2,-.7,0]);rad=1.35
  self.show(Circle(radius=rad,color=BLUE).move_to(a),Circle(radius=rad,color=GOLD).move_to(b),txt('입력 1회전 → 출력 5회전',-3,34,GREEN))
  self.add(always_redraw(lambda:Dot(a+rad*np.array([np.cos(t.get_value()),np.sin(t.get_value()),0]),color=BLUE)),always_redraw(lambda:Dot(b+rad*np.array([np.cos(5*t.get_value()),np.sin(5*t.get_value()),0]),color=GOLD)))
  counter=Integer(0,font_size=48,color=GOLD).move_to([2,-.7,0]);counter.add_updater(lambda m:m.set_value(min(5,int(5*t.get_value()/TAU+1e-6))));self.add(counter,txt('최고차항 모델',-4.1,24,MUTED));self.play(t.animate.set_value(TAU),run_time=6,rate_func=linear);self.to(104)
class Shot06(FTAScene):
 shot=5
 def s06(self):
  r,t,a,b=self.mapping(1.12,PI/5);self.add(txt('간단한 예시  P(z)=z⁵+1',6.2,23,MUTED),eq(r'P(Re^{it})=1+R^5e^{5it}',-4.15,30))
  self.play(r.animate.set_value(1),run_time=3);self.play(r.animate.set_value(.7),run_time=3);self.to(110)
  self.play(r.animate.set_value(0),run_time=4);self.show(txt('P(0)=1',-3.4,28,GREEN));self.to(115)
class Shot07(FTAScene):
 shot=6
 def s07(self):
  r,t,a,b=self.mapping(1.12,PI/5);self.add(txt('같은 수축을 다시 살펴보면',6.2,23,MUTED))
  status=txt('R > 1  ·  감김수 5',-3.8,30,GOLD);self.add(status);self.play(r.animate.set_value(1.02),run_time=5);self.to(121)
  self.play(r.animate.set_value(1),run_time=.6);self.play(Transform(status,txt('R = 1  ·  감김수 정의되지 않음',-3.8,27,RED)),Flash(b.c2p(0,0),color=RED,flash_radius=.35),run_time=.7);self.to(123)
  self.show(eq(r'z=r\ \Longrightarrow\ P(r)=0',-4.45,32,RED));self.play(Indicate(Dot(a.c2p(np.cos(PI/5),np.sin(PI/5)),color=RED),color=RED),run_time=1)
  self.to(127);self.play(r.animate.set_value(.72),Transform(status,txt('R < 1  ·  감김수 0',-3.8,30,GREEN)),run_time=2);self.to(129)
  self.show(txt('출력 0 → 방정식의 근',-.05,25,GREEN));self.to(132)
class Shot08(FTAScene):
 shot=7
 def s08(self):
  self.show(txt('감김수는 유지된다',3.4,43,GOLD),txt('원점을 지나지 않는\n연속적인 변형에서',1.6,35),txt('WINDING NUMBER',.2,24,MUTED),txt('기하학적 직관 · 엄밀한 증명에는 불변성 필요',-1.2,25,MUTED));self.to(139)
  self.clear_body();self.show(txt('해를 계산',3.1,38,MUTED),eq(r'r_1,r_2,\ldots',1.9,40,MUTED),txt('존재를 증명',-.1,43,GREEN),eq(r'\exists z:P(z)=0',-1.4,47,GREEN));self.to(145)
  self.clear_body();self.show(eq(r'\mathbb C',3,95,BLUE),txt('대수적으로 닫혀 있다',.8,44,GREEN),txt('Algebraically Closed',-.5,29),txt('다항식의 근에 대한 성질',-2.2,29,MUTED));self.to(152)
class Shot09(FTAScene):
 shot=8
 def s09(self):
  self.show(poly(2.6));self.to(156)
  self.show(eq(r'r_1\quad r_2\quad r_3\quad r_4\quad r_5',.1,39,GOLD),txt('값은 아직 모른다',-1.2,30,MUTED));self.to(160)
  box=RoundedRectangle(width=7.5,height=3.2,color=BLUE,corner_radius=.3).move_to(DOWN*.5);self.show(box,txt('모두 복소수 범위에 존재',-2.8,37,GREEN));self.to(166)
  self.clear_body();self.show(txt('해를 계산하는 것',2.4,42),eq(r'\ne',.6,65,GOLD),txt('존재를 증명하는 것',-1.2,42,GREEN));self.to(171)
  self.clear_body();self.show(txt('대수학의 기본정리',3,47,GREEN),txt('Fundamental Theorem of Algebra',1.9,23,MUTED),eq(r'\exists z\in\mathbb C:\ P(z)=0',.1,46),txt('복소수 계수 · 1차 이상',-1.3,26,MUTED),txt('해를 찾기 전부터,\n그 존재는 보장된다',-3,36,GREEN));self.to(177)
