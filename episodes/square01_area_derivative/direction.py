"""Disjoint square growth, the difference quotient, tangent slopes, and restoring force."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from episodes.energy01_force_gradient.direction import EnergyForceGeometry,eq,text
from episodes.square01_area_derivative.model import area,gain,secant,derivative
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BLUE,ORANGE,TEAL,GOLD,RED,MUTED='#80A8FF','#F1B66D','#43D3C4','#FFD477','#FF887A','#77849C'
class SquareDerivativeGeometry(EnergyForceGeometry):
 data=DATA
 def setup(self):
  super().setup()
  for m in list(self.mobjects):
   if isinstance(m,Text) and '에너지와힘' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  제곱의 미분',y=7.15,size=18,color=MUTED))
 def parts(self,x,dx,u=1.25,origin=(-1.8,.65)):
  ox,oy=origin
  def rect(w,h,left,bottom,color,opacity):
   return Rectangle(width=max(.001,w*u),height=max(.001,h*u),stroke_color=color,stroke_width=1.5,fill_color=color,fill_opacity=opacity).move_to([ox+u*(left+w/2),oy+u*(bottom+h/2),0])
  if dx<=1e-8:return VGroup(rect(x,x,0,0,BLUE,.18),VectorizedPoint([ox+u*x,oy,0]),VectorizedPoint([ox,oy+u*x,0]),VectorizedPoint([ox+u*x,oy+u*x,0]))
  return VGroup(rect(x,x,0,0,BLUE,.18),rect(dx,x,x,0,ORANGE,.4),rect(x,dx,0,x,ORANGE,.4),rect(dx,dx,x,x,TEAL,.55))
 def main_square(self,x=2,dx=.5,labels=False):
  self.px=ValueTracker(x);self.dx=ValueTracker(dx);self.sq=always_redraw(lambda:self.parts(self.px.get_value(),self.dx.get_value()));self.add(self.sq)
  self.add(eq(r'x^2',color=BLUE,size=42).move_to([-1.8+1.25*x/2,.65+1.25*x/2,0]),eq(r'x',color=BLUE,size=30).move_to([-1.8+1.25*x/2,.25,0]))
  if labels:self.area_labels(x,dx)
 def area_labels(self,x=2,dx=.5):
  u=1.25;cx=-1.8+u*(x+dx/2);cy=.65+u*(x+dx/2)
  self.labels=VGroup(eq(r'x\Delta x',size=29,color=ORANGE).move_to([-1.8+u*x/2,cy,0]),eq(r'x\Delta x',size=29,color=ORANGE).move_to([2.5,.65+u*x/2,0]),Line([cx+u*dx/2,.65+u*x/2,0],[1.9,.65+u*x/2,0],color=ORANGE,stroke_width=1.5),eq(r'(\Delta x)^2',size=21,color=TEAL).move_to([cx,cy,0]),eq(r'\Delta x',size=26,color=TEAL).move_to([cx,.25,0]))
  # The corner label is placed outside its small square to preserve readability.
  self.labels[3].move_to([2.4,3.7,0]);self.labels.add(Line([cx,cy,0],[1.75,3.7,0],color=TEAL,stroke_width=1.5));self.show(self.labels)
 def pair(self,x=1,dx=0,tangent=True):
  self.px=ValueTracker(x);self.dx=ValueTracker(dx)
  self.add(always_redraw(lambda:self.parts(self.px.get_value(),self.dx.get_value(),1,(-3.4,1.1))))
  self.ga=Axes(x_range=[0,2.5,.5],y_range=[0,6.25,1],x_length=3.2,y_length=3,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([1.6,2.2,0]);a=self.ga;xs=np.linspace(0,2.45,241)
  self.add(a,self.curve(a,area,xs,BLUE),always_redraw(lambda:Dot(a.c2p(self.px.get_value(),area(self.px.get_value())),radius=.06,color=BLUE)),text('면적 A',x=.3,y=3.95,size=20,color=BLUE),text('변 길이 x',x=3,y=.4,size=20,color=MUTED))
  if tangent:self.add(always_redraw(lambda:Line(a.c2p(self.px.get_value()-.2,area(self.px.get_value())-.2*derivative(self.px.get_value())),a.c2p(self.px.get_value()+.2,area(self.px.get_value())+.2*derivative(self.px.get_value())),color=ORANGE,stroke_width=3.5)))
  if dx>0:
   def steps():
    x=self.px.get_value();h=self.dx.get_value();return VGroup(Line(a.c2p(x,area(x)),a.c2p(x+h,area(x)),color=GOLD,stroke_width=2),Line(a.c2p(x+h,area(x)),a.c2p(x+h,area(x+h)),color=GOLD,stroke_width=2),Dot(a.c2p(x+h,area(x+h)),radius=.05,color=GOLD),DashedLine(a.c2p(x,area(x)),a.c2p(x+h,area(x+h)),color=MUTED,stroke_width=1))
   self.add(always_redraw(steps))
  self.add(text('한 변 x',x=-2.3,y=.45,size=21,color=BLUE),text('넓이 A=x²',x=1.4,y=.1,size=21,color=BLUE))
  xn=DecimalNumber(x,num_decimal_places=2,font_size=28,color=BLUE).move_to([-2.3,-.1,0]);an=DecimalNumber(x*x,num_decimal_places=2,font_size=28,color=BLUE).move_to([1.4,-.45,0]);xn.add_updater(lambda m:m.set_value(self.px.get_value()));an.add_updater(lambda m:m.set_value(area(self.px.get_value())));self.add(xn,an)
  if dx>0:
   self.add(text('증가한 넓이 ΔA',x=-1.4,y=-1.15,size=22,color=GOLD));dn=DecimalNumber(gain(x,dx),num_decimal_places=3,font_size=28,color=GOLD).move_to([1.5,-1.15,0]);dn.add_updater(lambda m:m.set_value(gain(self.px.get_value(),self.dx.get_value())));self.add(dn)
 def physics(self,q=1):
  self.field(q)
  for m in list(self.mobjects):
   if isinstance(m,Text) and m.text.replace(' ','')=='위치x':m.become(text('변위 q',x=3.15,y=1,size=20,color=MUTED))
 def spring_wire(self):
  start=np.array([-3.4,.15,0]);end=np.array([1.7*self.x.get_value()-.15,.15,0]);ps=[start]
  for i in range(17):ps.append(start+(i+1)/18*(end-start)+UP*.09*((-1)**i))
  ps.append(end);return VMobject(stroke_color=ORANGE,stroke_width=2).set_points_as_corners(ps)
 def s01(self):
  a=Axes(x_range=[-2.2,2.2,1],y_range=[0,4.5,1],x_length=6.8,y_length=3.5,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,1.9,0]);xs=np.linspace(-2.1,2.1,301);self.px=ValueTracker(0);self.add(a,self.curve(a,area,xs,BLUE),always_redraw(lambda:Dot(a.c2p(self.px.get_value(),area(self.px.get_value())),color=ORANGE,radius=.07)))
  self.add(always_redraw(lambda:Line(a.c2p(self.px.get_value()-.15,area(self.px.get_value())-.15*derivative(self.px.get_value())),a.c2p(self.px.get_value()+.15,area(self.px.get_value())+.15*derivative(self.px.get_value())),color=ORANGE,stroke_width=3)));self.play(self.px.animate.set_value(1.8),run_time=5,rate_func=linear)
  self.to(6);self.formulas(r'y=x^2',colors=[BLUE]);self.to(9);self.formulas(r'\frac{d}{dx}x^2=2x\quad\text{why?}',colors=[ORANGE])
 def s02(self):
  self.main_square(dx=0);self.note_at('한 변의 길이 x ≥ 0',size=27);self.to(16);self.formulas(r'A(x)=x^2',colors=[BLUE]);self.to(19);self.note_at('한 변을 Δx만큼 늘리면?',size=29,color=ORANGE)
 def s03(self):
  self.main_square(dx=.01);self.formulas(r'(x+\Delta x)^2-x^2',colors=[ORANGE]);self.play(self.dx.animate.set_value(.5),run_time=2)
  self.to(26);self.sq.clear_updaters();self.area_labels();self.note_at('직사각형 두 개 + 모서리 정사각형 하나',size=26,color=ORANGE)
 def s04(self):
  self.main_square(labels=True);self.sq.clear_updaters();self.formulas(r'x\Delta x+x\Delta x',colors=[ORANGE]);self.play(Indicate(self.sq[1],color=ORANGE),Indicate(self.sq[2],color=ORANGE),run_time=1.2)
  self.to(39);self.formulas(r'(\Delta x)^2',colors=[TEAL]);self.play(Indicate(self.sq[3],color=TEAL),run_time=1)
  self.to(44);self.formulas(r'\Delta A=2x\Delta x+(\Delta x)^2',colors=[ORANGE]);self.note_at('겹치지 않는 세 영역의 합',size=27)
 def s05(self):
  self.add(self.parts(1,.3,1,(-3.3,1.1)),self.parts(2,.3,1,(.2,1.1)),text('x=1',x=-2.65,y=.45,size=26,color=BLUE),text('x=2',x=1.35,y=.45,size=26,color=BLUE));self.note_at('같은 Δx=0.3 · 그림의 길이 배율도 동일',size=24);self.formulas(r'\Delta A_{x=1}=0.69',r'\Delta A_{x=2}=1.29',colors=[ORANGE,ORANGE]);self.to(53);self.show(text('두 직사각형의 넓이가 x에 비례해서 증가',y=-.6,size=27,color=ORANGE))
 def s06(self):
  self.main_square();self.formulas(r'\frac{\Delta A}{\Delta x}=\frac{2x\Delta x+(\Delta x)^2}{\Delta x}',colors=[ORANGE]);self.note_at('Δx>0 · 먼저 늘어난 길이로 나눈다',size=25)
  self.to(63);self.formulas(r'\frac{\Delta A}{\Delta x}=2x+\Delta x',colors=[ORANGE]);self.to(66);self.formulas(r'\frac{\Delta A}{\Delta x}=2x+\Delta x',r'\frac{(\Delta x)^2}{\Delta x}=\Delta x\longrightarrow0',colors=[ORANGE,TEAL]);self.play(self.dx.animate.set_value(.035),run_time=4)
  self.to(73);self.formulas(r'\boxed{\frac{dA}{dx}=2x}',colors=[ORANGE]);self.note_at('두 직사각형에서 x+x가 남는다',size=28,color=ORANGE)
 def s07(self):
  self.pair(.7,tangent=False);self.formulas(r'A=x^2',colors=[BLUE]);self.note_at('한 변 x와 그래프의 x좌표는 같은 값',size=25)
  self.to(81);self.play(self.px.animate.set_value(2),run_time=5,rate_func=linear);self.to(87);self.note_at('정사각형의 넓이 = 그래프의 높이',size=27,color=BLUE)
 def s08(self):
  self.pair(.65,.25);self.note_at('같은 Δx=0.25 · 주황은 접선, 노랑은 증가량',size=23);self.formulas(r'\Delta A=2x\Delta x+(\Delta x)^2',colors=[GOLD]);self.to(95);self.play(self.px.animate.set_value(1.8),run_time=4,rate_func=linear)
  self.to(100);self.formulas(r'\text{tangent slope}=2x',r'\text{secant slope}=2x+\Delta x',colors=[ORANGE,MUTED])
 def s09(self):
  self.pair(1.8);self.formulas(r'A^{\prime}(x)=2x',r'\lim_{h\to0}\frac{(x+h)^2-x^2}{h}=2x',colors=[ORANGE,WHITE]);self.show(text('정사각형은 x≥0 · 다항식의 미분 공식은 x∈ℝ',y=-4.15,size=21,color=MUTED));self.to(112);self.note_at('이제 길이 x에서, 양·음의 변위 q로',size=26,color=TEAL)
 def s10(self):
  self.physics(.4);self.add(text('1차원 보존력의 이차 근사 모델',y=-4.15,size=21,color=MUTED));self.formulas(r'V(q)\approx V(0)+\tfrac12kq^2',r'k=V^{\prime\prime}(0)>0',colors=[ORANGE,TEAL]);self.note_at('비퇴화 안정 최소점 · 작은 변위 · q는 양·음 가능',size=22)
  self.play(self.x.animate.set_value(1.5),run_time=3);self.to(120);self.formulas(r'\frac{dV}{dq}=\frac12k\cdot2q=kq',colors=[ORANGE]);self.note_at('이하: 이차 근사 모델 V=V₀+½kq²',size=25);self.play(self.x.animate.set_value(-1.5),run_time=2)
  self.to(124);self.formulas(r'F=-\frac{dV}{dq}=-kq',colors=[RED])
 def s11(self):
  self.physics(.35);self.formulas(r'F=-kq,\qquad |F|=k|q|',colors=[RED]);self.note_at('원점에서 멀수록 더 큰 복원력',size=28,color=RED);self.play(self.x.animate.set_value(1.4),run_time=2);self.play(self.x.animate.set_value(-1.4),run_time=2)
  self.to(134);self.add(always_redraw(self.spring_wire));self.play(self.x.animate.set_value(1.1),run_time=.5);self.play(UpdateFromAlphaFunc(self.x,lambda m,a:m.set_value(1.1*np.cos(a*np.pi/2))),run_time=1.6,rate_func=linear);self.note_at('용수철의 선형 복원력',size=29,color=RED)
 def s12(self):
  self.add(self.parts(1.4,0,1.1,(-3.3,1.6)));a=Axes(x_range=[0,2.1,1],y_range=[0,4.4,1],x_length=2.1,y_length=2.1,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1}).move_to([0,2.65,0]);xs=np.linspace(0,2.05,181);self.add(a,self.curve(a,area,xs,BLUE),Line(a.c2p(1.2,area(1.4)-.2*2.8),a.c2p(1.6,area(1.4)+.2*2.8),color=ORANGE,stroke_width=3),Square(side_length=.5,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([2.65,2.65,0]),Arrow([2.5,3.2,0],[1.5,3.2,0],color=RED,buff=0));self.add(text('넓이',x=-2.5,y=1,size=26,color=BLUE),text('기울기',x=0,y=1,size=26,color=ORANGE),text('복원력',x=2.65,y=1,size=26,color=RED));self.note_at('넓이의 변화 → 포물선의 기울기 → 힘',size=27)
  self.formulas(r'\frac{d}{dx}x^2=2x',r'V(q)=\tfrac12kq^2\quad\Rightarrow\quad F=-kq',colors=[ORANGE,RED]);self.to(144);self.play(Indicate(self.form[0],color=ORANGE),run_time=1)
 def s13(self):
  self.pair(1);self.formulas(r'\boxed{\frac{d}{dx}x^2=2x}',colors=[ORANGE]);self.note_at('공식은 변화의 기하학을 압축한 표현',size=27,color=ORANGE);self.play(self.px.animate.set_value(1.7),run_time=3,rate_func=linear)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
