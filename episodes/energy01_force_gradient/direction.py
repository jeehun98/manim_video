"""Work, energy gradients, conservative forces, and the arbitrary energy zero."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text
from episodes.energy01_force_gradient import tex_compat
from episodes.energy01_force_gradient.model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BLUE,ORANGE,TEAL,GOLD,RED,MUTED='#80A8FF','#F1B66D','#43D3C4','#FFD477','#FF887A','#77849C'
class EnergyForceGeometry(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup();self.offset=self.info['start']
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('물리의 연결  /  에너지와 힘',y=7.15,size=18,color=MUTED))
 def curve(self,a,fn,xs,color=ORANGE,width=3):
  return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners([a.c2p(float(x),float(y)) for x,y in zip(xs,fn(xs))])
 def lift(self,h=0):
  self.h=ValueTracker(h)
  axis=Line([-3.4,.6,0],[-3.4,3.5,0],color=MUTED,stroke_width=1.2)
  ticks=VGroup(*[VGroup(Line([-3.48,.6+1.2*j,0],[-3.32,.6+1.2*j,0],color=MUTED),text(str(j),x=-3.75,y=.6+1.2*j,size=19,color=MUTED)) for j in [0,1,2]])
  block=always_redraw(lambda:RoundedRectangle(width=.65,height=.55,corner_radius=.06,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([-2.25,.6+1.2*self.h.get_value(),0]))
  ext=always_redraw(lambda:Arrow([-2.85,.6+1.2*self.h.get_value(),0],[-2.85,1.35+1.2*self.h.get_value(),0],buff=0,color=TEAL,stroke_width=3,max_tip_length_to_length_ratio=.2))
  grav=always_redraw(lambda:Arrow([-1.65,.6+1.2*self.h.get_value(),0],[-1.65,-.15+1.2*self.h.get_value(),0],buff=0,color=RED,stroke_width=3,max_tip_length_to_length_ratio=.2))
  a=Axes(x_range=[0,2.3,1],y_range=[0,23,10],x_length=2.8,y_length=3,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([1.7,2.1,0])
  self.add(axis,ticks,block,ext,grav,a,self.curve(a,gravity_potential,np.linspace(0,2.2,181)),always_redraw(lambda:Dot(a.c2p(self.h.get_value(),gravity_potential(self.h.get_value())),color=GOLD,radius=.065)))
  self.add(text('h / m',x=-3.4,y=3.85,size=20,color=BLUE),text('V / J',x=.45,y=3.85,size=20,color=ORANGE),text('h / m',x=3.2,y=.25,size=20,color=MUTED),text('높이 h',x=-2.2,y=-.55,size=22,color=BLUE),text('퍼텐셜 증가 ΔV',x=1.7,y=-.55,size=22,color=ORANGE))
  hn=DecimalNumber(h,num_decimal_places=1,font_size=32,color=BLUE).move_to([-2.4,-1.1,0]);vn=DecimalNumber(10*h,num_decimal_places=1,font_size=32,color=ORANGE).move_to([1.4,-1.1,0])
  hn.add_updater(lambda m:m.set_value(self.h.get_value()));vn.add_updater(lambda m:m.set_value(10*self.h.get_value()));self.add(hn,vn,text('m',x=-1.6,y=-1.1,size=24,color=BLUE),text('J',x=2.4,y=-1.1,size=24,color=ORANGE),text('외부 힘 +10 N',x=-2,y=-1.7,size=21,color=TEAL),text('중력 −10 N',x=1.8,y=-1.7,size=21,color=RED))
 def field_axes(self,y=2.6,height=2.7,yr=(0,5)):
  return Axes(x_range=[-2,2,1],y_range=[*yr,1],x_length=6.8,y_length=height,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,y,0])
 def field(self,x=1.5,offset=0,ghost=False):
  self.x=ValueTracker(x);self.c=ValueTracker(offset);self.a=self.field_axes();xs=np.linspace(-2,2,321);self.add(self.a,text('에너지 V',x=-3.2,y=4.1,size=20,color=ORANGE),text('위치 x',x=3.15,y=1,size=20,color=MUTED))
  if ghost:
   self.add(self.curve(self.a,potential,xs,BLUE).set_stroke(opacity=.35),always_redraw(lambda:Dot(self.a.c2p(self.x.get_value(),potential(self.x.get_value())),color=BLUE,radius=.045)),always_redraw(lambda:self.tangent_mob(self.x.get_value(),0,TEAL)))
  self.add(always_redraw(lambda:self.curve(self.a,lambda u:potential(u,self.c.get_value()),xs)),always_redraw(lambda:Dot(self.a.c2p(self.x.get_value(),potential(self.x.get_value(),self.c.get_value())),color=GOLD,radius=.065)),always_redraw(lambda:self.tangent_mob(self.x.get_value(),self.c.get_value(),WHITE)))
  self.add(Line([-3.4,.15,0],[3.4,.15,0],color=MUTED,stroke_width=1.2),always_redraw(lambda:Square(side_length=.3,color=BLUE,fill_color=BLUE,fill_opacity=.7).move_to([1.7*self.x.get_value(),.15,0])),always_redraw(self.force_arrow),text('실제 물체 · 힘은 위치축 방향',y=-.6,size=23,color=BLUE))
 def tangent_mob(self,x,c,color):
  h=.32;return Line(self.a.c2p(x-h,tangent(x-h,x,c)),self.a.c2p(x+h,tangent(x+h,x,c)),color=color,stroke_width=3)
 def force_arrow(self):
  x=self.x.get_value();p=np.array([1.7*x,.45,0]);f=float(force(x))
  if abs(f)<.025:return VectorizedPoint(p)
  return Arrow(p,p+RIGHT*.8*f,buff=.025,color=RED,stroke_width=4,max_tip_length_to_length_ratio=.2)
 def s01(self):
  block=Square(side_length=.8,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([0,2.3,0]);arrow=Arrow([.5,2.3,0],[2,2.3,0],color=RED,buff=0);self.show(block,arrow);self.formulas(r'F\;?',colors=[RED])
  self.to(4);self.play(FadeOut(arrow),FadeOut(block),run_time=.5);self.field(x=1);self.formulas(r'x\ \longrightarrow\ V(x)\ \longrightarrow\ F(x)\;?',colors=[ORANGE])
  self.to(9);self.note_at('에너지의 변화가 힘을 알려 준다면?',size=29,color=TEAL)
 def s02(self):
  self.lift();self.note_at('중력 10 N 일정 · 천천히 들어 올림',size=24)
  self.to(16);self.formulas(r'F_{\rm ext}=+10\,\mathrm N,\quad F_g=-10\,\mathrm N',colors=[WHITE])
  self.to(20);self.play(self.h.animate.set_value(1.5),run_time=3,rate_func=linear)
 def s03(self):
  self.lift();self.note_at('에너지의 크기보다, 이동에 따른 증가량',size=25);self.formulas(r'\Delta V=(10\,\mathrm{J/m})\Delta h',colors=[GOLD])
  self.to(31);self.play(self.h.animate.set_value(1),run_time=2,rate_func=linear);self.formulas(r'1\,\mathrm m\ \longrightarrow\ 10\,\mathrm J',colors=[GOLD]);self.play(self.h.animate.set_value(2),run_time=3,rate_func=linear);self.formulas(r'2\,\mathrm m\ \longrightarrow\ 20\,\mathrm J',colors=[GOLD])
  self.to(39);self.formulas(r'\frac{10\,\mathrm J}{1\,\mathrm m}=\frac{20\,\mathrm J}{2\,\mathrm m}',colors=[GOLD]);self.note_at('높이가 1 m 늘 때마다 에너지는 10 J 증가',size=24)
 def s04(self):
  self.lift();self.formulas(r'\Delta V=10\,\mathrm J\quad(\Delta h=1\,\mathrm m)',colors=[GOLD]);self.to(48);self.note_at('일 W = 힘이 이동을 통해 전달한 에너지',size=26,color=TEAL)
  self.to(51);self.play(self.h.animate.set_value(1),run_time=2,rate_func=linear);self.formulas(r'W_{\rm ext}=\Delta V',colors=[TEAL])
 def s05(self):
  self.q=ValueTracker(-2);self.add(Line([-3.4,2,0],[3.4,2,0],color=MUTED),always_redraw(lambda:Square(side_length=.65,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([self.q.get_value(),2.35,0])),always_redraw(lambda:Arrow([self.q.get_value(),2.8,0],[self.q.get_value()+1.2,2.8,0],buff=0,color=TEAL)))
  self.note_at('크기 일정 · 힘과 이동이 같은 방향',size=26);self.formulas(r'W=F\,\Delta x',colors=[TEAL]);self.play(self.q.animate.set_value(2),run_time=4,rate_func=linear);self.show(DoubleArrow([-2,1.3,0],[2,1.3,0],color=GOLD,buff=0),eq(r'\Delta x',y=.65,color=GOLD,size=34))
  self.to(61);self.formulas(r'F=\frac{W}{\Delta x}',r'10\,\mathrm{J/m}=10\,\mathrm N',colors=[TEAL,GOLD]);self.note_at('힘 = 단위 거리당 전달되는 에너지',size=27,color=TEAL)
 def s06(self):
  self.lift();self.note_at('천천히 이동 · 운동에너지 변화 ΔK≈0',size=24);self.to(69);self.formulas(r'W_{\rm ext}=+\Delta V',colors=[TEAL]);self.play(self.h.animate.set_value(1.8),run_time=3,rate_func=linear)
  self.to(75);self.formulas(r'W_g=-\Delta V',colors=[RED]);self.note_at('상승: 외부의 일은 양수 · 중력의 일은 음수',size=24)
  self.to(79);self.formulas(r'W_{\rm ext}=+\Delta V',r'W_g=-\Delta V',colors=[TEAL,RED])
 def s07(self):
  a=Axes(x_range=[0,2.2,1],y_range=[0,22,10],x_length=6.4,y_length=3.1,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,2.35,0]);self.add(a,self.curve(a,gravity_potential,np.linspace(0,2.15,241)),text('V / J',x=-3,y=4.1,size=22,color=ORANGE),text('h / m',x=3,y=.45,size=22,color=MUTED))
  dx=ValueTracker(.9);h=.7
  step=always_redraw(lambda:VGroup(Line(a.c2p(h,10*h),a.c2p(h+dx.get_value(),10*h),color=GOLD,stroke_width=3),Line(a.c2p(h+dx.get_value(),10*h),a.c2p(h+dx.get_value(),10*(h+dx.get_value())),color=GOLD,stroke_width=3),Dot(a.c2p(h,10*h),radius=.06,color=TEAL),Dot(a.c2p(h+dx.get_value(),10*(h+dx.get_value())),radius=.06,color=GOLD)))
  self.add(step);self.formulas(r'W_g=F_g\Delta h=-\Delta V',colors=[RED]);self.to(87);self.formulas(r'\lim_{\Delta h\to0}\frac{\Delta V}{\Delta h}=\frac{dV}{dh}',colors=[GOLD]);self.play(dx.animate.set_value(.05),run_time=3)
  self.to(93);self.formulas(r'F_g=-\frac{dV}{dh}',r'\frac{dV}{dh}=10\,\mathrm{J/m},\quad F_g=-10\,\mathrm N',colors=[RED,GOLD]);self.note_at('미소 이동: dW=F dh, dV=−F dh',size=25)
 def s08(self):
  self.lift(1);self.formulas(r'\frac{dV}{dh}=+10\,\mathrm{J/m}',r'F_g=-\frac{dV}{dh}=-10\,\mathrm N',colors=[ORANGE,RED]);self.to(100);self.play(self.h.animate.set_value(1.8),run_time=3,rate_func=linear)
  self.to(105);self.note_at('위쪽: 에너지 증가 · 아래쪽: 중력',size=28,color=RED)
 def s09(self):
  self.field(.7);self.note_at('세로축은 에너지 · 가로축은 실제 위치',size=24);self.to(112);self.formulas(r'V(x)=\tfrac12x^2',colors=[ORANGE]);self.to(116);self.play(self.x.animate.set_value(1.5),run_time=2);self.formulas(r'V^{\prime}(x)>0\quad\Rightarrow\quad F(x)<0',colors=[RED])
 def s10(self):
  self.field(1.5);self.formulas(r'F(x)=-V^{\prime}(x)',colors=[RED]);self.play(self.x.animate.set_value(-1.5),run_time=3);self.formulas(r'V^{\prime}(x)<0\quad\Rightarrow\quad F(x)>0',colors=[RED])
  self.to(127);self.play(self.x.animate.set_value(0),run_time=1.5);self.formulas(r'V^{\prime}(0)=0\quad\Rightarrow\quad F(0)=0',colors=[TEAL]);self.to(131);self.note_at('이 예시는 국소 최소점 · 주변의 힘은 안쪽으로',size=24,color=TEAL);self.formulas(r'V^{\prime\prime}(0)=1>0',r'\text{local minimum}\quad\Rightarrow\quad\text{stable}',colors=[TEAL,TEAL])
 def s11(self):
  self.field(1,ghost=True);self.note_at('같은 위치 x에서 비교',size=25);self.to(139);self.formulas(r'\widetilde V(x)=V(x)+C',colors=[ORANGE]);self.to(143);self.play(self.c.animate.set_value(2),run_time=3)
  self.formulas(r'\frac{d}{dx}[V(x)+C]=\frac{dV}{dx}',colors=[WHITE]);self.to(148);self.note_at('접선은 평행 · 실제 물체의 힘은 그대로',size=27,color=RED)
 def s12(self):
  self.field(1,offset=2,ghost=True);self.formulas(r'\widetilde F=-\frac{d}{dx}(V+C)=-\frac{dV}{dx}=F',colors=[RED]);self.note_at('에너지의 절댓값이 아닌 위치에 따른 변화율',size=25,color=ORANGE)
  self.to(158);self.note_at('1차원 · 위치 퍼텐셜로 표현되는 보존력',size=25,color=TEAL);self.show(text('모든 힘에 적용되는 공식은 아닙니다',y=-3.65,size=25,color=MUTED))
 def s13(self):
  a=self.field_axes(y=2.8,height=2.2,yr=(0,2.3));fa=Axes(x_range=[-2,2,1],y_range=[-2.2,2.2,1],x_length=6.8,y_length=1.7,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,-.15,0]);xs=np.linspace(-2,2,321)
  self.add(a,self.curve(a,potential,xs),fa,text('퍼텐셜 V(x)',x=-2.35,y=4.1,size=22,color=ORANGE),text('힘 F(x)',x=-2.65,y=1.15,size=22,color=RED));self.play(Create(self.curve(fa,force,xs,RED)),run_time=1.5)
  self.x=ValueTracker(-1.5);self.add(always_redraw(lambda:Dot(a.c2p(self.x.get_value(),potential(self.x.get_value())),color=GOLD,radius=.06)),always_redraw(lambda:Dot(fa.c2p(self.x.get_value(),force(self.x.get_value())),color=GOLD,radius=.06)))
  self.formulas(r'F(x)=-\frac{dV}{dx}',colors=[RED]);self.note_at('에너지의 공간적 변화 → 힘의 방향과 크기',size=26,color=TEAL);self.play(self.x.animate.set_value(1.5),run_time=3)
  self.to(168);self.show(text('퍼텐셜에는 공간의 힘에 대한 정보가 담겨 있다',y=-3.65,size=27,color=TEAL,width=7.6));self.play(self.x.animate.set_value(-1.5),run_time=4)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
