"""Ratio to distance to accumulated area; one persistent reciprocal graph."""
import sys,os,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#0B1020'
TEAL,GOLD,BLUE,PURPLE,MUTED='#48CEC5','#E9B66C','#78A6FF','#B6A0F5','#8490A8'
def eq(s,y=-2.3,color=WHITE,size=36):
 m=MathTex(s,font_size=size,color=color)
 if m.width>7.65:m.scale_to_fit_width(7.65)
 return m.move_to([0,y,0])
class LogRatioGeometry(QCSScene):
 data=DATA
 def replace(self,old,new):return Scene.replace(self,old,new)
 def setup(self):
  super().setup();self.offset=0
  self.remove(self.mobjects[0]);self.add(text('수학의 연결  /  자연로그의 기하학',y=7.15,size=18,color=MUTED))
  self.form=VGroup();self.body=VGroup();self.overlay=VGroup()
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for m in self.mobjects:
   if m is self.caption or m is self.caption_panel:continue
   if m.width<.001 or m.height<.001:continue
   assert m.get_left()[0]>=-4.39 and m.get_right()[0]<=4.39,('x',self.time,str(m))
   assert m.get_bottom()[1]>=-4.9 and m.get_top()[1]<=7.9,('y',self.time,str(m))
 def drop(self,group):self.remove(*group.get_family())
 def heading(self,n):self.play(Transform(self.title,text(DATA['scenes'][n-1]['title'],y=5.5,size=32,width=7.65)),run_time=.35)
 def formulas(self,*ss,colors=None):
  new=VGroup(*[eq(s,-2.3-i*.95,(colors[i] if colors else WHITE)) for i,s in enumerate(ss)])
  self.play(FadeOut(self.form),FadeIn(new),run_time=.45);self.form=new
 def note_at(self,s,y=4.45,color=MUTED,size=25):
  if hasattr(self,'topnote'):self.drop(self.topnote)
  self.topnote=text(s,y=y,size=size,color=color,width=7.65);self.show(self.topnote,run_time=.35)
 def wipe(self):
  self.drop(self.body);self.drop(self.overlay);self.body=VGroup();self.overlay=VGroup()
  if hasattr(self,'topnote'):self.drop(self.topnote)
 def line(self,y=2):return Line([-3.5,y,0],[3.5,y,0],color=MUTED,stroke_width=2)
 def num(self,s,x,y,color=WHITE,size=25):return text(s,x=x,y=y,size=size,color=color)
 def plane(self,reciprocal=False):
  self.axes=Axes(x_range=[0,6.5,1],y_range=[-.2,1.5,.5],x_length=7,y_length=4.5,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.5}).move_to([0,1.15,0])
  self.curve=self.axes.plot((lambda x:1/x) if reciprocal else np.log,x_range=[.72,6.3 if reciprocal else 4.3,.025],color=TEAL,stroke_width=3)
  labels=VGroup(*[eq(str(x),size=22).move_to(self.axes.c2p(x,0)+DOWN*.32) for x in [1,2,3,4,6]])
  ticks=VGroup(*[Line(self.axes.c2p(x,0)+DOWN*.06,self.axes.c2p(x,0)+UP*.06,color=MUTED) for x in [1,2,3,4,6]])
  self.axislabels=VGroup(labels,ticks,text('x',size=23,color=MUTED).move_to(self.axes.c2p(6.5,0)+DOWN*.27))
  self.add(self.axes,self.axislabels,self.curve)
 def region(self,left,right,color=TEAL,factor=1,opacity=.46):
  xs=np.linspace(left,right,129)
  coords=[(left*factor,0)]+[(x*factor,1/x/factor) for x in xs]+[(right*factor,0)]
  return Polygon(*[self.axes.c2p(x,y) for x,y in coords],color=color,fill_color=color,fill_opacity=opacity,stroke_width=1.4)
 def scale_region(self,mob,start,end,duration=2.5,base=(1,2),color=GOLD):
  def upd(m,t):
   f=(1-t)*start+t*end
   m.become(self.region(*base,color=color,factor=f))
  self.play(UpdateFromAlphaFunc(mob,upd),run_time=duration,rate_func=smooth)
 def s01(self):
  self.formulas(r'\log(ab)=\log a+\log b')
  self.note_at('a > 0, b > 0  ·  밑은 고정된 양수, 1 제외',color=MUTED,size=21)
  self.to(3)
  cards=VGroup(eq(r'a\times b',y=2.4,color=GOLD,size=50),eq(r'\log a+\log b',y=.5,color=TEAL,size=43))
  self.body=cards;self.show(cards);self.play(Indicate(self.form,color=GOLD),run_time=1)
  self.to(7);self.note_at('왜 곱셈이 덧셈으로 바뀔까?',y=3.9,color=TEAL,size=33)
 def s02(self):
  self.heading(2);self.wipe();self.formulas(r'100-10=90',r'1000-100=900',colors=[BLUE,GOLD])
  self.line_axis=self.line(2);self.scale=ValueTracker(120)
  self.dots=VGroup(*[Dot([-3.5+7*v/120,2,0],radius=.06,color=BLUE) for v in [10,100]])
  self.labels=VGroup(self.num('10',0,2.65,BLUE),self.num('100',0,1.35,GOLD))
  for d,v in zip(self.dots,[10,100]):d.add_updater(lambda m,v=v:m.move_to([-3.5+7*v/self.scale.get_value(),2,0]))
  for lab,v,y in zip(self.labels,[10,100],[2.65,1.35]):lab.add_updater(lambda m,v=v,y=y:m.move_to([-3.5+7*v/self.scale.get_value(),y,0]))
  self.show(self.line_axis,self.dots,self.labels,run_time=.35)
  self.play(self.scale.animate.set_value(1000),run_time=1.8)
  for m in [*self.dots,*self.labels]:m.clear_updaters()
  self.dots.add(Dot([3.5,2,0],radius=.06,color=GOLD));self.labels.add(self.num('1000',3.5,2.65,GOLD));self.add(self.dots[-1],self.labels[-1])
  self.body=VGroup(self.line_axis,self.dots,self.labels)
  self.to(15);self.note_at('×10                           ×10',y=3.8,color=GOLD,size=30)
  self.overlay=VGroup(Line(self.dots[0].get_center()+DOWN*.1,self.dots[1].get_center()+DOWN*.1,color=BLUE,stroke_width=5),Line(self.dots[1].get_center()+DOWN*.1,self.dots[2].get_center()+DOWN*.1,color=GOLD,stroke_width=5));self.show(self.overlay)
 def s03(self):
  self.heading(3);self.drop(self.overlay);self.overlay=VGroup();self.note_at('상용로그  log₁₀',color=TEAL)
  self.formulas(r'\log_{10}10=1,\quad\log_{10}100=2,\quad\log_{10}1000=3')
  self.to(23)
  targets=[-2.6,0,2.6]
  self.play(*[d.animate.move_to([x,2,0]) for d,x in zip(self.dots,targets)],*[Transform(l,self.num(str(i+1),x,1.35,TEAL)) for i,(l,x) in enumerate(zip(self.labels,targets))],run_time=2.7)
  self.overlay=VGroup(*[DoubleArrow([x,2.65,0],[x+2.6,2.65,0],buff=.08,color=TEAL,stroke_width=3) for x in [-2.6,0]])
  self.show(self.overlay);self.to(28);self.note_at('같은 배율 → 같은 간격',color=TEAL,size=31)
 def comparison_row(self,y,log=False):
  def pos(v):return -3.5+7*((np.log10(v)-1)/1.35 if log else v/220)
  g=VGroup(self.line(y))
  for i,(v,c) in enumerate([(10,BLUE),(20,BLUE),(100,GOLD),(200,GOLD)]):
   x=pos(v);g.add(Dot([x,y,0],radius=.045,color=c),self.num(str(v),x,y+(.47 if i%2==0 else -.47),c,22))
  for l,r,c in [(10,20,BLUE),(100,200,GOLD)]:g.add(Line([pos(l),y+.1,0],[pos(r),y+.1,0],color=c,stroke_width=5))
  return g
 def s04(self):
  self.heading(4);self.wipe()
  self.upper=self.comparison_row(2.7);self.lower=self.comparison_row(.1);self.body=VGroup(self.upper,self.lower)
  self.show(self.body);self.note_at('위: 일반 눈금   ·   아래: 로그로 바뀔 눈금',size=23)
  self.formulas(r'10\to20:\;\times2\qquad100\to200:\;\times2')
  self.to(40);self.play(Transform(self.lower,self.comparison_row(.1,True)),run_time=2.5)
  self.note_at('위: 일반 눈금   ·   아래: log₁₀ 눈금',size=23,color=TEAL)
  self.formulas(r'\log_{10}20-\log_{10}10=\log_{10}2',r'\log_{10}200-\log_{10}100=\log_{10}2',colors=[BLUE,GOLD])
 def s05(self):
  self.heading(5);self.wipe();self.formulas(r'\Delta x\quad\hbox{vs.}\quad\frac{\Delta x}{x}')
  self.body=VGroup(text('얼마나 늘었나?\n원래 크기에 비해 얼마나 늘었나?',y=1.8,size=35,width=7.5,color=PURPLE));self.show(self.body)
  self.to(49);self.drop(self.body)
  self.body=VGroup(eq(r'100\longrightarrow101',y=2.7,color=BLUE,size=43),eq(r'1000\longrightarrow1010',y=.6,color=GOLD,size=43))
  self.show(self.body);self.formulas(r'\Delta x=1\qquad\Delta x=10')
  self.to(57);self.formulas(r'\frac{101-100}{100}=\frac1{100}=0.01',r'\frac{1010-1000}{1000}=\frac{10}{1000}=0.01',colors=[BLUE,GOLD]);self.note_at('둘 다 정확히 1% 증가',color=PURPLE,size=30)
  self.to(63);self.drop(self.body);self.body=VGroup(eq(r'x\longrightarrow x+\Delta x',y=1.8,color=TEAL,size=48));self.show(self.body);self.formulas(r'\text{relative change}=\frac{\Delta x}{x}')
 def s06(self):
  self.heading(6);self.wipe();self.plane();self.note_at('이제 자연로그  ln x',color=TEAL);self.formulas(r'y=\ln x')
  self.tx=ValueTracker(1)
  dot=always_redraw(lambda:Dot(self.axes.c2p(self.tx.get_value(),np.log(self.tx.get_value())),color=GOLD,radius=.07))
  tangent=always_redraw(lambda:Line(self.axes.c2p(self.tx.get_value()-.35,np.log(self.tx.get_value())-.35/self.tx.get_value()),self.axes.c2p(self.tx.get_value()+.35,np.log(self.tx.get_value())+.35/self.tx.get_value()),color=GOLD,stroke_width=3))
  self.overlay=VGroup(dot,tangent);self.show(self.overlay,run_time=.35)
  self.to(71);self.formulas(r'\frac{d}{dx}\ln x=\frac1x');self.play(self.tx.animate.set_value(4),run_time=2.4)
  self.to(75);self.drop(self.overlay);self.overlay=VGroup()
  x=2;dx=.4;P=self.axes.c2p(x,np.log(x));Q=self.axes.c2p(x+dx,np.log(x+dx));T=self.axes.c2p(x+dx,np.log(x)+dx/x)
  self.overlay=VGroup(Line(P,self.axes.c2p(x+dx,np.log(x)),color=BLUE,stroke_width=4),Line(self.axes.c2p(x+dx,np.log(x)),Q,color=TEAL,stroke_width=4),Dot(Q,color=TEAL,radius=.055),Circle(radius=.065,color=GOLD).move_to(T),Line(P,T,color=GOLD,stroke_width=2))
  self.show(self.overlay);self.formulas(r'\Delta(\ln x)=\ln\!\left(1+\frac{\Delta x}{x}\right)',r'\Delta(\ln x)\approx\frac{\Delta x}{x}\quad(\Delta x/x\to0)',colors=[TEAL,GOLD]);self.note_at('청록: 실제 변화  ·  금색: 접선 근사',size=23)
 def riemann(self,n,right=4):
  xs=np.linspace(1,right,n+1);g=VGroup()
  for a,b in zip(xs,xs[1:]):g.add(Polygon(self.axes.c2p(a,0),self.axes.c2p(a,1/a),self.axes.c2p(b,1/a),self.axes.c2p(b,0),color=TEAL,stroke_width=.6,fill_color=TEAL,fill_opacity=.38))
  return g
 def s07(self):
  self.heading(7);self.drop(self.overlay);self.note_at('작은 상대 변화량을 누적',color=PURPLE)
  self.formulas(r'\sum_k\frac{\Delta x_k}{x_k}')
  newcurve=self.axes.plot(lambda x:1/x,x_range=[.72,6.3,.025],color=TEAL,stroke_width=3)
  self.play(Transform(self.curve,newcurve),run_time=1);self.note_at('y = 1/x  ·  변화율을 누적하는 그래프',size=25,color=TEAL)
  self.rects=self.riemann(8);self.show(self.rects,run_time=.6)
  self.to(85);self.play(Transform(self.rects,self.riemann(32)),run_time=1)
  self.to(87);self.formulas(r'\ln x=\lim\sum_k\frac{\Delta x_k}{x_k}=\int_1^x\frac{dt}{t}')
  area=self.region(1,4);self.play(FadeOut(self.rects),FadeIn(area),run_time=1);self.area=area
 def s08(self):
  self.heading(8);self.note_at('y = 1/x',color=TEAL);self.formulas(r'\ln x=\int_1^x\frac{dt}{t}')
  self.to(95);new=self.region(1,2);self.play(Transform(self.area,new),run_time=1)
  self.formulas(r'A=\int_1^2\frac{dx}{x}=\ln2',colors=[TEAL])
 def s09(self):
  self.heading(9);self.area.set_fill(opacity=.23)
  self.moving=self.region(1,2,GOLD);self.add(self.moving)
  self.formulas(r'(x,y)\longmapsto(2x,y/2)',colors=[GOLD])
  self.scale_region(self.moving,1,2,3.2)
  self.to(103);self.note_at('가로 ×2    ·    세로 ×½',color=GOLD,size=30)
  self.formulas(r'\text{area scale}=2\times\frac12=1')
  self.to(108);self.formulas(r'\int_1^2\frac{dx}{x}=\int_2^4\frac{dx}{x}=\ln2',colors=[TEAL]);self.play(Indicate(self.area,color=TEAL),Indicate(self.moving,color=GOLD),run_time=1)
 def s10(self):
  self.heading(10);self.formulas(r'(x,y)\longmapsto(sx,y/s),\quad s>0',r'\text{area scale}=s\times\frac1s=1')
  self.scale_region(self.moving,2,1.5,1.1);self.scale_region(self.moving,1.5,3,1.5)
  self.to(116);self.note_at('같은 비율 → 같은 넓이',color=TEAL,size=29)
  self.formulas(r'\int_a^{ab}\frac{dx}{x}=\int_1^b\frac{dt}{t}\qquad(a,b>0)',colors=[TEAL])
 def s11(self):
  self.heading(11);self.drop(self.moving);self.area.set_fill(opacity=.46);self.note_at('예시  a = 2, b = 3',size=27,color=TEAL)
  self.formulas(r'A=\int_1^2\frac{dx}{x}=\ln2',colors=[TEAL])
  self.to(125);self.moving=self.region(1,3,GOLD);self.add(self.moving)
  self.formulas(r'B=\int_1^3\frac{dt}{t}=\int_2^6\frac{dx}{x}=\ln3',colors=[GOLD]);self.scale_region(self.moving,1,2,2.7,base=(1,3))
  self.to(130);self.formulas(r'\int_1^2\frac{dx}{x}+\int_2^6\frac{dx}{x}=\int_1^6\frac{dx}{x}',r'\ln2+\ln3=\ln6',colors=[WHITE,TEAL])
  self.play(Indicate(self.area,color=TEAL),Indicate(self.moving,color=GOLD),run_time=1.2)
  self.to(135);self.formulas(r'\ln a+\ln b=\ln(ab)\quad(a,b>0)',colors=[TEAL])
 def s12(self):
  self.heading(12);self.formulas(r'\boxed{\ln(ab)=\ln a+\ln b}',colors=[TEAL]);self.to(140)
  self.note_at('곱셈의 이동 → 넓이의 덧셈',color=TEAL,size=28)
  self.formulas(r'a\xrightarrow{\times b}ab',r'\ln a\xrightarrow{+\ln b}\ln(ab)',colors=[GOLD,TEAL])
 def s13(self):
  self.heading(13);self.formulas(r'd(\ln x)=\frac{dx}{x}',colors=[TEAL]);self.note_at('작은 상대 변화를 쌓으면 자연로그',color=TEAL,size=26)
  thin=self.region(4,4.12,PURPLE);self.overlay=VGroup(thin);self.show(thin)
  self.to(151);self.drop(self.overlay);self.formulas(r'\boxed{\ln(ab)=\ln a+\ln b}',colors=[TEAL]);self.note_at('비율의 곱셈이 넓이의 덧셈이 된다',color=TEAL,size=29)
  signed=text('그림: a,b ≥ 1  ·  0 < x < 1에서는 방향 있는 적분',y=-4.15,size=18,color=MUTED,width=7.65);self.show(signed,run_time=.35)
 def finish_audit(self):
  self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.__class__.__name__+'_captions.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
 def construct(self):
  for i,s in enumerate(DATA['scenes'],1):
   self.next_section(s['id']);getattr(self,f's{i:02}')();self.to(s['end'])
  self.finish_audit()
class AreaPreview(LogRatioGeometry):
 def construct(self):
  self.offset=98;self.plane(True);self.area=self.region(1,2);self.add(self.area);self.s09();self.to(111);self.s10();self.to(121);self.s11();self.to(138);self.finish_audit()
class ScalePreview(LogRatioGeometry):
 def construct(self):
  self.offset=11;self.s02();self.to(20);self.s03();self.to(33);self.finish_audit()

class CalculusPreview(LogRatioGeometry):
 def construct(self):
  self.offset=68;self.s06();self.to(81);self.s07();self.to(92);self.finish_audit()
