"""Discover e by area, then swap input and output in data coordinates."""
import sys,json,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
from manim import *
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text,TEAL,BLUE,PURPLE,MUTED
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
GOLD='#FFD477';ORANGE='#F0B66C'
class EAreaGeometry(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup()
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  넓이에서 발견하는 e',y=7.15,size=18,color=MUTED))
  self.inverse_mode=False
 def heading(self,n):self.play(Transform(self.title,text(DATA['scenes'][n-1]['title'],y=5.5,size=32,width=7.65)),run_time=.35)
 def endpoint(self):return float(np.exp(self.u.get_value()) if self.inverse_mode else self.s.get_value())
 def curve_point(self,x,color=GOLD):return Dot(self.axes.c2p(x,1/x),radius=.065,color=color)
 def install_accumulation(self,start=1):
  self.s=ValueTracker(start)
  self.area=always_redraw(lambda:self.region(1,self.endpoint(),TEAL))
  self.marker=always_redraw(lambda:VGroup(Line(self.axes.c2p(self.endpoint(),0),self.axes.c2p(self.endpoint(),1/self.endpoint()),color=GOLD,stroke_width=2),Dot(self.axes.c2p(self.endpoint(),0),radius=.055,color=GOLD)))
  self.counter=DecimalNumber(np.log(start),num_decimal_places=3,font_size=35,color=TEAL).move_to([1.8,4.45,0])
  self.counter.add_updater(lambda m:m.set_value(np.log(self.endpoint())).move_to([1.8,4.45,0]))
  self.counter_label=text('누적 넓이 ≈',x=-1.1,y=4.45,size=27,color=TEAL)
  self.counter_group=VGroup(self.counter_label,self.counter)
  self.add(self.area,self.marker,self.counter_group)
 def drop_counter(self):
  self.counter.clear_updaters();self.drop(self.counter_group)
 def reciprocal_small(self):
  self.rec_graph=VGroup(self.axes,self.axislabels,self.curve)
  self.play(self.rec_graph.animate.stretch(.52,1).scale(.9).move_to([0,3,0]),run_time=.8)
 def make_log_panel(self):
  self.logaxes=Axes(x_range=[0,4.5,1],y_range=[-.3,1.6,.5],x_length=6.3,y_length=2.4,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,-.25,0])
  self.logticks=VGroup(*[eq(str(i),size=19).move_to(self.logaxes.c2p(i,0)+DOWN*.22) for i in [1,2,3,4]])
  self.logdot=always_redraw(lambda:Dot(self.logaxes.c2p(self.endpoint(),np.log(self.endpoint())),radius=.055,color=BLUE))
  self.flowlabel=text('끝점 x → 누적 넓이 A(x)',y=1.43,size=23,color=BLUE)
  self.add(self.logaxes,self.logticks,self.logdot,self.flowlabel)
 def square_plane(self):
  self.inv_axes=Axes(x_range=[-.6,3.7,1],y_range=[-.6,3.7,1],x_length=5.6,y_length=5.6,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,1.15,0])
  unitx=np.linalg.norm(self.inv_axes.c2p(1,0)-self.inv_axes.c2p(0,0));unity=np.linalg.norm(self.inv_axes.c2p(0,1)-self.inv_axes.c2p(0,0));assert np.isclose(unitx,unity)
  self.inv_ticks=VGroup(*[eq(str(i),size=19).move_to(self.inv_axes.c2p(i,0)+DOWN*.22) for i in [0,1,2,3]],*[eq(str(i),size=19).move_to(self.inv_axes.c2p(0,i)+LEFT*.24) for i in [1,2,3]])
  self.diagonal=DashedLine(self.inv_axes.c2p(-.4,-.4),self.inv_axes.c2p(3.5,3.5),color=MUTED,stroke_width=1.4)
  self.xs=np.linspace(.65,3.6,160)
  self.ln_curve=VMobject(color=BLUE,stroke_width=3).set_points_as_corners([self.inv_axes.c2p(x,np.log(x)) for x in self.xs])
  self.exp_curve=self.ln_curve.copy().set_color(PURPLE)
  self.add(self.inv_axes,self.inv_ticks,self.diagonal,self.ln_curve,self.exp_curve)
 def reflected_curve(self,mob,t):
  mob.set_points_as_corners([self.inv_axes.c2p((1-t)*x+t*np.log(x),(1-t)*np.log(x)+t*x) for x in self.xs])
 def s01(self):
  c=Circle(radius=1.4,color=BLUE).move_to([0,1.8,0]);d=Line(c.get_left(),c.get_right(),color=GOLD,stroke_width=3)
  self.body=VGroup(c,d,text('둘레 ÷ 지름',y=-.1,size=30,color=BLUE));self.show(self.body,run_time=.6);self.formulas(r'\pi=\frac{C}{d}')
  self.to(3);self.formulas(r'e\approx2.718281828\ldots',colors=[GOLD]);self.note_at('이 숫자는 어디에서 나올까?',color=GOLD,size=30)
  self.play(self.body.animate.set_opacity(.25),run_time=.5)
  self.to(10);self.wipe();self.plane(True);self.curve.set_opacity(0)
 def s02(self):
  self.heading(2);self.play(self.curve.animate.set_opacity(1),run_time=.8);self.formulas(r'y=\frac1x,\quad x>0',colors=[TEAL])
  self.pointx=ValueTracker(1)
  self.point=always_redraw(lambda:self.curve_point(self.pointx.get_value()))
  self.projection=always_redraw(lambda:Line(self.axes.c2p(self.pointx.get_value(),0),self.axes.c2p(self.pointx.get_value(),1/self.pointx.get_value()),color=GOLD,stroke_width=2))
  self.add(self.point,self.projection)
  self.to(17);self.note_at('x: 1 → 2 → 3    ·    높이: 1 → ½ → ⅓',size=25,color=GOLD);self.play(self.pointx.animate.set_value(2),run_time=1.7);self.play(self.pointx.animate.set_value(3),run_time=1.7)
  self.to(23);self.play(self.pointx.animate.set_value(1),run_time=.9)
 def s03(self):
  self.heading(3);self.drop(self.point);self.drop(self.projection);self.note_at('가로 ×2   ·   세로 ×½',size=29,color=ORANGE)
  self.source_area=self.region(1,2,TEAL,opacity=.24);self.moving=self.region(1,2,ORANGE);self.add(self.source_area,self.moving)
  self.formulas(r'(x,y)\longmapsto(2x,y/2)',colors=[ORANGE])
  self.to(31);self.scale_region(self.moving,1,2,3,base=(1,2),color=ORANGE)
  self.to(35);self.formulas(r'2\times\frac12=1',r'\int_1^2\frac{dx}{x}=\int_2^4\frac{dx}{x}',colors=[ORANGE,TEAL])
  self.to(41);self.formulas(r'(x,y)\longmapsto(ax,y/a),\quad a>0');self.scale_region(self.moving,2,1.5,.7,color=ORANGE);self.scale_region(self.moving,1.5,3,.8,color=ORANGE)
 def s04(self):
  self.heading(4);self.drop(self.source_area);self.drop(self.moving);self.note_at('어떤 함수가 이 배율 조건을 만족할까?',size=26,color=TEAL)
  self.to(46);self.formulas(r'f(ax)=\frac{f(x)}a\qquad(a,x>0)',colors=[TEAL])
  self.pointx.set_value(1.3);self.add(self.point,self.projection);self.play(self.pointx.animate.set_value(3),run_time=2.5)
  self.to(53);self.normalization_tail()
 def normalization_tail(self):
  self.formulas(r'x=1:\quad f(a)=\frac{f(1)}a',r'f(x)=\frac Cx,\qquad C=f(1)',colors=[WHITE,TEAL])
  self.drop(self.point);self.drop(self.projection)
  for C in [.75,1.15]:
   other=self.axes.plot(lambda x,C=C:C/x,x_range=[.85,6.3,.025],color=TEAL,stroke_width=3)
   self.play(Transform(self.curve,other),run_time=.65)
  self.to(58);self.formulas(r'f(1)=1\Rightarrow C=1\Rightarrow f(x)=\frac1x',colors=[TEAL])
  self.play(Transform(self.curve,self.axes.plot(lambda x:1/x,x_range=[.72,6.3,.025],color=TEAL,stroke_width=3)),run_time=1)
  self.pointx.set_value(1);self.add(self.point,self.projection)
 def s05(self):
  self.heading(5);self.drop(self.point);self.drop(self.projection)
  if hasattr(self,'topnote'):self.drop(self.topnote)
  self.install_accumulation();self.formulas(r'A(s)=\int_1^s\frac{dt}{t}')
  self.to(66);self.play(self.s.animate.set_value(2.5),run_time=4)
  self.to(71);self.formulas(r'A(s)=1\quad\Longrightarrow\quad s=?',colors=[GOLD]);self.play(self.s.animate.set_value(2.69),run_time=2.3)
 def s06(self):
  self.heading(6);self.play(self.s.animate.set_value(np.e),run_time=1.1)
  self.to(77);self.formulas(r'\boxed{\int_1^e\frac{dt}{t}=1}',r'e\approx2.718281828\ldots',colors=[TEAL,GOLD])
  self.e_label=eq('e',size=30,color=GOLD).move_to(self.axes.c2p(np.e,0)+DOWN*.42);self.show(self.e_label,run_time=.4)
 def s07(self):
  self.heading(7);self.drop_counter();self.drop(self.e_label);self.reciprocal_small();self.make_log_panel()
  self.note_at('넓이의 끝점 x ↔ 누적 넓이 A(x)',color=TEAL,size=24);self.formulas(r'x\longmapsto A(x)')
  self.to(87);self.s.set_value(1)
  self.logcurve=always_redraw(lambda:self.logaxes.plot(np.log,x_range=[1,max(1.00001,self.endpoint()),.025],color=BLUE,stroke_width=3))
  self.add(self.logcurve);self.formulas(r'A(x)=\int_1^x\frac{dt}{t}=\ln x',colors=[BLUE]);self.play(self.s.animate.set_value(4),run_time=3)
  self.logcurve.clear_updaters()
 def s08(self):
  self.heading(8);self.play(self.s.animate.set_value(2.3),run_time=.7);self.dx=ValueTracker(.45)
  thin=always_redraw(lambda:self.region(self.endpoint(),self.endpoint()+self.dx.get_value(),ORANGE))
  def secant():
   x=self.endpoint();h=self.dx.get_value();slope=np.log1p(h/x)/h
   return Line(self.logaxes.c2p(x-.3,np.log(x)-.3*slope),self.logaxes.c2p(x+.5,np.log(x)+.5*slope),color=ORANGE,stroke_width=3)
  sec=always_redraw(secant);self.overlay=VGroup(thin,sec);self.add(self.overlay)
  self.formulas(r'\Delta A\approx\frac{\Delta x}{x}',r'\frac{\Delta A}{\Delta x}\longrightarrow\frac1x',colors=[ORANGE,BLUE]);self.play(self.dx.animate.set_value(.03),run_time=3)
  self.to(98);self.formulas(r'\boxed{A\prime(x)=\frac{d}{dx}\ln x=\frac1x}',colors=[BLUE])
 def s09(self):
  self.heading(9);self.drop(self.overlay);self.formulas(r'x\xrightarrow{\ A\ }u\qquad u\xrightarrow{\ E\ }x');self.note_at('입력과 출력의 역할을 바꾸면',color=PURPLE,size=26)
  self.to(104);self.u=ValueTracker(np.log(self.s.get_value()));self.inverse_mode=True
  self.play(self.u.animate.set_value(0),run_time=.6);self.play(self.u.animate.set_value(.5),run_time=1);self.play(self.u.animate.set_value(1),run_time=1)
  self.note_at('넓이 u: 0 → 0.5 → 1  ·  끝점: 1 → 1.649 → e',size=21,color=PURPLE)
  self.to(109)
  self.area.clear_updaters();self.marker.clear_updaters();self.logdot.clear_updaters()
  self.reciprocal_panel=VGroup(self.axes,self.axislabels,self.curve,self.area,self.marker).copy()
  for group in [self.rec_graph,self.area,self.marker,self.logaxes,self.logticks,self.logdot,self.logcurve,self.flowlabel]:self.drop(group)
  self.square_plane();self.play(UpdateFromAlphaFunc(self.exp_curve,self.reflected_curve),run_time=1.6)
  self.formulas(r'(x,\ln x)\longleftrightarrow(\ln x,x)',r'E=A^{-1},\qquad E(u)=e^u',colors=[WHITE,PURPLE]);self.note_at('파랑: ln x   ·   보라: E(u)   ·   점선: y = x',size=23)
 def s10(self):
  self.heading(10)
  x=2;u=np.log(x)
  p=Dot(self.inv_axes.c2p(x,u),radius=.065,color=BLUE)
  t=Line(self.inv_axes.c2p(x-.45,u-.45/x),self.inv_axes.c2p(x+.45,u+.45/x),color=BLUE,stroke_width=4)
  self.original_tangent=VGroup(p,t);self.add(self.original_tangent)
  self.formulas(r'A\prime(2)=\frac12',colors=[BLUE])
  q=p.copy().set_color(GOLD);qt=t.copy().set_color(GOLD);self.reflected_tangent=VGroup(q,qt);self.add(self.reflected_tangent)
  self.play(q.animate.move_to(self.inv_axes.c2p(u,x)),Transform(qt,Line(self.inv_axes.c2p(u-.45/x,x-.45),self.inv_axes.c2p(u+.45/x,x+.45),color=GOLD,stroke_width=4)),run_time=2.3)
  self.formulas(r'E\prime(\ln2)=2\qquad E(\ln2)=2',r'E\prime(u)=\frac1{A\prime(E(u))}=E(u)',colors=[GOLD,PURPLE])
  self.to(119);self.note_at('역함수의 기울기 x = 역함수의 출력 E(u)',size=25,color=PURPLE)
 def exponential_dynamic(self):
  self.eu=ValueTracker(0)
  self.exp_dot=always_redraw(lambda:Dot(self.inv_axes.c2p(self.eu.get_value(),np.exp(self.eu.get_value())),radius=.07,color=PURPLE))
  def tangent():
   u=self.eu.get_value();v=np.exp(u)
   return Line(self.inv_axes.c2p(u-.18,v-.18*v),self.inv_axes.c2p(u+.18,v+.18*v),color=GOLD,stroke_width=3)
  self.exp_tangent=always_redraw(tangent)
  value=DecimalNumber(1,num_decimal_places=3,font_size=29,color=PURPLE).move_to([-.65,4.45,0]);slope=DecimalNumber(1,num_decimal_places=3,font_size=29,color=GOLD).move_to([2.6,4.45,0])
  value.add_updater(lambda m:m.set_value(np.exp(self.eu.get_value())).move_to([-.65,4.45,0]));slope.add_updater(lambda m:m.set_value(1/(1/np.exp(self.eu.get_value()))).move_to([2.6,4.45,0]))
  self.output_numbers=VGroup(text('함수값 ≈',x=-2.1,y=4.45,size=21,color=PURPLE),value,text('기울기 ≈',x=1.1,y=4.45,size=21,color=GOLD),slope)
  self.add(self.exp_dot,self.exp_tangent,self.output_numbers)
 def s11(self):
  self.heading(11);self.drop(self.ln_curve);self.drop(self.diagonal);self.drop(self.original_tangent);self.drop(self.reflected_tangent);self.drop(self.topnote)
  self.exponential_dynamic();self.formulas(r'E\prime(u)=E(u),\qquad E(0)=1',colors=[PURPLE]);self.play(self.eu.animate.set_value(.5),run_time=1.5);self.play(self.eu.animate.set_value(1),run_time=1.5)
  self.to(127);self.formulas(r'\boxed{\frac{d}{du}e^u=e^u}',r'u\in\mathbb R,\quad E(u)>0',colors=[PURPLE,MUTED])
 def s12(self):
  self.heading(12)
  self.exp_dot.clear_updaters();self.exp_tangent.clear_updaters()
  for m in self.output_numbers:m.clear_updaters()
  self.drop(self.output_numbers)
  self.exponential_panel=VGroup(self.inv_axes,self.inv_ticks,self.exp_curve,self.exp_dot,self.exp_tangent)
  self.play(self.exponential_panel.animate.scale(.55).move_to([0,-.3,0]),run_time=.8)
  self.add(self.reciprocal_panel);self.note_at('위: 넓이 1을 만드는 끝점   ·   아래: 입력 1의 출력',size=22,color=GOLD)
  self.formulas(r'\int_1^e\frac{dt}{t}=1',r'E(1)=e\approx2.71828',colors=[TEAL,GOLD])
  self.to(135);self.play(Indicate(self.reciprocal_panel,color=TEAL),Indicate(self.exp_dot,color=GOLD),run_time=1)
 def s13(self):
  self.heading(13);self.formulas(r'(x,y)\mapsto(ax,y/a)\quad\longrightarrow\quad A(x)')
  self.to(144);self.formulas(r'A(x)=\int_1^x\frac{dt}{t}',r'E=A^{-1}',colors=[BLUE,PURPLE]);self.note_at('넓이를 누적하고, 입력과 출력을 바꾸면',size=25,color=TEAL)
  self.to(148);self.formulas(r'E\prime(u)=E(u),\qquad E(1)=e',colors=[PURPLE])
  self.to(151);self.formulas(r'\boxed{e\approx2.718281828\ldots}',colors=[GOLD]);self.note_at('넓이에서 발견하고, 미분에서 다시 만나는 숫자',size=25,color=GOLD)
  self.to(155);self.play(FadeOut(self.reciprocal_panel),FadeOut(self.exponential_panel),run_time=.8);self.drop(self.reciprocal_panel);self.drop(self.exponential_panel)
  self.play(self.form.animate.move_to([0,1.3,0]),run_time=.8)
 def finish_audit(self):
  self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.__class__.__name__+'_captions.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
 def construct(self):
  for i,s in enumerate(DATA['scenes'],1):
   self.next_section(s['id']);getattr(self,f's{i:02}')();self.to(s['end'])
  self.finish_audit()
class DiscoveryPreview(EAreaGeometry):
 def construct(self):
  self.offset=63;self.plane(True);self.point=VGroup();self.projection=VGroup();self.s05();self.to(75);self.s06();self.to(83);self.finish_audit()
class InversePreview(EAreaGeometry):
 def construct(self):
  self.offset=101;self.plane(True);self.install_accumulation(2.3);self.drop_counter();self.rec_graph=VGroup(self.axes,self.axislabels,self.curve).stretch(.52,1).scale(.9).move_to([0,3,0]);self.make_log_panel();self.logcurve=self.logaxes.plot(np.log,x_range=[1,4,.025],color=BLUE);self.add(self.logcurve)
  self.s09();self.to(112);self.s10();self.to(122);self.s11();self.to(131);self.s12();self.to(139);self.finish_audit()

class AccumulationPreview(EAreaGeometry):
 def construct(self):
  self.offset=83;self.plane(True);self.install_accumulation(np.e);self.e_label=VGroup();self.s07();self.to(92);self.s08();self.to(101);self.finish_audit()

class NormalizationPatch(EAreaGeometry):
 def construct(self):
  self.offset=53;self.title.become(text(DATA['scenes'][3]['title'],y=5.5,size=32,width=7.65));self.plane(True)
  self.pointx=ValueTracker(3);self.point=always_redraw(lambda:self.curve_point(self.pointx.get_value()))
  self.projection=always_redraw(lambda:Line(self.axes.c2p(self.pointx.get_value(),0),self.axes.c2p(self.pointx.get_value(),1/self.pointx.get_value()),color=GOLD,stroke_width=2))
  self.add(self.point,self.projection)
  self.topnote=text('어떤 함수가 이 배율 조건을 만족할까?',y=4.45,size=26,color=TEAL,width=7.65);self.add(self.topnote)
  self.form=VGroup(eq(r'f(ax)=\frac{f(x)}a\qquad(a,x>0)',color=TEAL));self.add(self.form)
  self.normalization_tail();self.to(63);self.finish_audit()
