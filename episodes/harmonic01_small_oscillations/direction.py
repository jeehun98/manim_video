"""Energy shape -> restoring force -> differential equation -> small oscillations."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text
from episodes.harmonic01_small_oscillations import tex_compat
from episodes.harmonic01_small_oscillations.model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BLUE,ORANGE,TEAL,PURPLE,GOLD,MUTED,RED='#80A8FF','#F1B66D','#43D3C4','#BD9BFA','#FFD477','#77849C','#FF887A'
class HarmonicGeometry(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup();self.offset=self.info['start']
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  조화 진동자',y=7.15,size=18,color=MUTED))
 def curve(self,a,fn,xs,color=BLUE,width=3):
  return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners([a.c2p(float(x),float(y)) for x,y in zip(xs,fn(xs))])
 def coil(self,start,end,color=ORANGE,turns=8,amp=.16):
  start=np.array(start);end=np.array(end);points=[start,start+.12*(end-start)]
  for i in range(2*turns+1):
   s=.15+.7*i/(2*turns);points.append(start+s*(end-start)+UP*amp*((-1)**i))
  points.extend([start+.88*(end-start),end]);return VMobject(stroke_color=color,stroke_width=2).set_points_as_corners(points)
 def spring(self,q=0,y=2.7,x=0,scale=1,force_arrow=False):
  wall=np.array([x-3*scale,y,0]);body=np.array([x+q*scale,y,0])
  g=VGroup(Line(wall+UP*.55*scale,wall+DOWN*.55*scale,color=MUTED),Line([x-3.1*scale,y-.48*scale,0],[x+2.6*scale,y-.48*scale,0],color=MUTED,stroke_width=1),self.coil(wall,body+LEFT*.34*scale,amp=.16*scale),RoundedRectangle(width=.68*scale,height=.75*scale,corner_radius=.06*scale,color=TEAL,fill_color=TEAL,fill_opacity=.2).move_to(body),DashedLine([x,y-.55*scale,0],[x,y+.65*scale,0],color=MUTED,stroke_width=1))
  if force_arrow and abs(q)>.025:g.add(Arrow(body,body+LEFT*q*1.2*scale,buff=.1*scale,color=RED,stroke_width=4,max_tip_length_to_length_ratio=.2))
  return g
 def pendulum(self,theta=.2,x=0,y=3.5,scale=1):
  p=np.array([x,y,0]);end=p+scale*1.9*np.array([np.sin(theta),-np.cos(theta),0])
  return VGroup(Line(p+LEFT*.4*scale,p+RIGHT*.4*scale,color=MUTED),DashedLine(p,p+DOWN*1.9*scale,color=MUTED,stroke_width=1),Line(p,end,color=WHITE,stroke_width=2),Dot(end,radius=.16*scale,color=TEAL))
 def molecule(self,q=0,x=0,y=2.6,scale=1):
  left=np.array([x-(.8+.18*q)*scale,y,0]);right=np.array([x+(.8+.18*q)*scale,y,0])
  return VGroup(self.coil(left,right,PURPLE,6,.12*scale),Dot(left,radius=.22*scale,color=BLUE),Dot(right,radius=.22*scale,color=PURPLE))
 def miniature(self,kind,t,x,y,scale=.42):
  if kind==0:return self.spring(.7*np.cos(1.4*t),y,x+.4,scale)
  if kind==1:return self.pendulum(.2*np.cos(1.8*t),x,y+.6,scale*1.4)
  return self.molecule(np.cos(2.2*t),x,y,scale*1.6)
 def potential_axes(self):
  return Axes(x_range=[-1.8,1.8,1],y_range=[0,3.5,1],x_length=6.8,y_length=2.8,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,2.55,0])
 def potential_graph(self,epsilon=1,approx=False):
  a=self.potential_axes();xs=np.linspace(-1.8,1.8,361);g=VGroup(a,self.curve(a,lambda u:scaled(u,epsilon),xs,BLUE))
  if approx:g.add(self.curve(a,quadratic,xs,ORANGE))
  g.add(Dot(a.c2p(0,0),radius=.065,color=TEAL));return g,a
 def potential_base(self,epsilon=1,approx=False):
  self.pg,self.pa=self.potential_graph(epsilon,approx);self.add(self.pg)
  self.vlabel=text('에너지 V',x=-3.25,y=4.1,size=20,color=BLUE);self.qlabel=text('위치 q',x=3.15,y=.85,size=20,color=MUTED)
  self.add(self.vlabel,self.qlabel,text('평형점 0',x=0,y=.8,size=21,color=TEAL))
 def normalized_labels(self):
  self.vlabel.become(text('ΔV / ε²',x=-3.25,y=4.1,size=20,color=BLUE));self.qlabel.become(text('u=q/ε',x=3.15,y=.85,size=20,color=MUTED))
 def force_panel(self,approx=False):
  self.potential_base(approx=approx);self.q=ValueTracker(1)
  fn=quadratic if approx else potential;ff=(lambda q:-q) if approx else force
  point=always_redraw(lambda:Dot(self.pa.c2p(self.q.get_value(),fn(self.q.get_value())),color=TEAL,radius=.065))
  def tangent():
   q=self.q.get_value();h=.25;d=-float(ff(q));return Line(self.pa.c2p(q-h,fn(q)-h*d),self.pa.c2p(q+h,fn(q)+h*d),color=ORANGE,stroke_width=3)
  # Tangents stay within plot energy bounds at the displayed displacements.
  tan=always_redraw(tangent)
  rail=Line([-3.2,-.1,0],[3.2,-.1,0],color=MUTED,stroke_width=1.2)
  body=always_redraw(lambda:Square(side_length=.28,color=TEAL,fill_color=TEAL,fill_opacity=.8).move_to([1.7*self.q.get_value(),-.1,0]))
  def arrow():
   q=self.q.get_value();pos=np.array([1.7*q,.15,0]);f=float(ff(q))
   if abs(f)<.025:return VectorizedPoint(pos)
   return Arrow(pos,pos+RIGHT*.85*f,buff=.025,color=RED,stroke_width=4,max_tip_length_to_length_ratio=.2)
  ar=always_redraw(arrow);self.add(point,tan,rail,body,ar,text('실제 물체의 위치',y=-.8,size=22,color=TEAL))
 def wave_axes(self,y=-.25,h=1.7):
  return Axes(x_range=[0,4*np.pi,np.pi],y_range=[-1.2,1.2,1],x_length=6.8,y_length=h,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,y,0])
 def s01(self):
  self.t=ValueTracker(0);icons=VGroup(*[always_redraw(lambda k=k,x=x:self.miniature(k,self.t.get_value(),x,3.0)) for k,x in enumerate([-2.5,0,2.5])]);self.add(icons)
  self.add(*[text(n,x=x,y=1.85,size=23,color=[ORANGE,TEAL,PURPLE][k]) for k,(x,n) in enumerate(zip([-2.5,0,2.5],['용수철','작은 진자','분자 진동']))]);self.play(self.t.animate.set_value(5),run_time=5,rate_func=linear)
  axes=VGroup();waves=VGroup()
  for x,w,c in zip([-2.5,0,2.5],[1.4,1.8,2.2],[ORANGE,TEAL,PURPLE]):
   a=Axes(x_range=[0,7,1],y_range=[-1.2,1.2,1],x_length=2.05,y_length=1.5,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1}).move_to([x,.4,0]);axes.add(a);waves.add(self.curve(a,lambda t,w=w:np.cos(w*t),np.linspace(0,7,181),c,2.5))
  self.show(axes,waves);self.play(self.t.animate.set_value(9.3),run_time=4.3,rate_func=linear)
  self.to(10);self.formulas(r'\sin(\omega t+\phi),\quad\cos(\omega t+\phi)',colors=[TEAL]);self.to(13);self.note_at('왜 같은 수학적 형태가 반복될까?',color=TEAL,size=29)
 def s02(self):
  xs=np.linspace(-2.1,2.1,181);bowl=VMobject(stroke_color=BLUE,stroke_width=4).set_points_as_corners([[x,1.5+.42*x*x,0] for x in xs]);self.show(bowl)
  self.to(20);q=ValueTracker(1.6);ball=always_redraw(lambda:Dot([q.get_value(),1.68+.42*q.get_value()**2,0],radius=.17,color=TEAL));self.add(ball)
  self.note_at('실제 그릇의 단면 · 마찰이 있으면 정착',size=24);self.play(q.animate.set_value(0),run_time=5,rate_func=smooth)
  self.to(27);self.formulas(r'V(x_0)\ \text{is a local minimum}',colors=[TEAL]);self.show(text('안정적인 평형점',y=.55,size=30,color=TEAL))
 def s03(self):
  self.q=ValueTracker(1);g=always_redraw(lambda:self.spring(self.q.get_value(),force_arrow=True));self.add(g);self.note_at('평형점에서 조금 벗어나면',size=27);self.formulas(r'q=x-x_0',colors=[GOLD])
  self.to(34);self.play(self.q.animate.set_value(-1),run_time=2,rate_func=smooth);self.to(37);self.note_at('힘은 평형점을 향한다',size=30,color=RED)
 def s04(self):
  self.force_panel();self.formulas(r'F(q)=-\frac{dV}{dq}',colors=[RED]);self.note_at('위는 에너지 그래프 · 아래는 실제 위치',size=24)
  self.play(self.q.animate.set_value(-1),run_time=3,rate_func=smooth)
  self.to(46);self.play(self.q.animate.set_value(1),run_time=2.5,rate_func=smooth);self.note_at('에너지가 낮아지는 쪽으로 힘이 작용',size=25,color=RED)
 def s05(self):
  self.potential_base();self.formulas(r'V(q)=\tfrac12q^2+0.12q^3+0.08q^4',colors=[BLUE]);self.note_at('실제 퍼텐셜을 본뜬 비대칭 예시',size=25)
  self.to(54);self.play(Indicate(self.pg[1],color=BLUE),run_time=1)
  self.to(57);self.formulas(r'q=\varepsilon u,\quad\frac{V(\varepsilon u)-V(0)}{\varepsilon^2}',colors=[GOLD]);self.normalized_labels();self.note_at('작은 변위를 확대 · 에너지는 ε²로 정규화',size=24)
  new,_=self.potential_graph(.25,True);self.play(Transform(self.pg,new),run_time=2)
 def s06(self):
  self.potential_base();self.formulas(r'V(x_0+q)=V(x_0)+V^{\prime}(x_0)q',r'\qquad+\frac{V^{\prime\prime}(x_0)}{2}q^2+O(q^3)',colors=[BLUE,ORANGE]);self.note_at('q=x−x₀ · 평형점에서 전개',size=25)
  self.to(66);self.formulas(r'V^{\prime}(x_0)=0',r'V^{\prime}(x_0)q=0',colors=[TEAL,MUTED]);self.play(Indicate(self.pg[-1],color=TEAL),run_time=1)
  self.to(70);self.note_at('평형점에서는 기울기가 0 → 일차항 소멸',size=26,color=TEAL)
 def s07(self):
  self.potential_base(approx=True);self.formulas(r'k=V^{\prime\prime}(x_0)>0',r'V(x_0+q)\approx V(x_0)+\tfrac12kq^2',colors=[TEAL,ORANGE]);self.note_at('V″>0인 비퇴화 안정 최소점 · 작은 변위',size=23)
  self.to(77);self.formulas(r'\frac{V(\varepsilon u)-V(0)}{\varepsilon^2}\to\frac12u^2',r'\varepsilon:1\longrightarrow0.2',colors=[ORANGE,GOLD]);self.normalized_labels()
  new,_=self.potential_graph(.2,True);self.play(Transform(self.pg,new),run_time=2)
 def s08(self):
  self.force_panel(approx=True);self.formulas(r'V(q)=\tfrac12kq^2',r'F=-kq',colors=[ORANGE,RED]);self.note_at('여기서는 이차 근사 모델',size=25)
  self.to(86);self.play(self.q.animate.set_value(.35),run_time=2);self.play(self.q.animate.set_value(1.15),run_time=2);self.play(self.q.animate.set_value(-1.15),run_time=2)
  self.to(94);self.note_at('용수철의 복원력과 같은 형태',size=28,color=RED)
 def s09(self):
  self.add(self.spring(1,force_arrow=True));self.formulas(r'F=-kq',colors=[RED]);self.note_at('마찰·외부 구동 없는 운동',size=25)
  self.to(101);self.formulas(r'F=m\ddot q',r'm\ddot q=-kq',colors=[WHITE,RED]);self.add(text('질량 m',x=1,y=1.7,size=24,color=TEAL))
  self.to(105);self.show(Arrow([1,1.25,0],[-.6,1.25,0],buff=0,color=RED),text('가속도는 변위와 반대 방향',y=.45,size=27,color=RED));self.to(110);self.note_at('위치 q를 두 번 미분한 것이 가속도',size=26,color=TEAL)
 def s10(self):
  self.formulas(r'\ddot q=-\frac{k}{m}q=-\omega^2q',r'\omega=\sqrt{\frac{k}{m}}',colors=[TEAL,GOLD]);self.add(self.spring(.8,force_arrow=True));self.note_at('양의 상수 ω² · 위치와 반대 방향의 가속도',size=24)
  self.to(117);self.show(eq(r'\sin(\omega t)\xrightarrow{d/dt}\omega\cos(\omega t)',y=.6,color=TEAL,size=34))
  self.to(121);self.show(eq(r'\omega\cos(\omega t)\xrightarrow{d/dt}-\omega^2\sin(\omega t)',y=-.4,color=TEAL,size=32));self.play(Indicate(self.form[0],color=TEAL),run_time=1)
 def s11(self):
  self.t=ValueTracker(0);self.add(always_redraw(lambda:self.spring(float(displacement(self.t.get_value())),force_arrow=True)))
  a=self.wave_axes();xs=np.linspace(0,4*np.pi,361);self.add(a,self.curve(a,displacement,xs,TEAL),text('시간 t →',x=2.8,y=-1.45,size=20,color=MUTED))
  dot=always_redraw(lambda:Dot(a.c2p(self.t.get_value(),displacement(self.t.get_value())),radius=.065,color=GOLD));self.add(dot);self.formulas(r'q(t)=C\cos(\omega t)+D\sin(\omega t)',r'=A\cos(\omega t+\phi)',colors=[TEAL,TEAL]);self.note_at('물체의 변위와 시간 그래프를 동기화',size=24)
  self.to(132);self.play(self.t.animate.set_value(5.7),run_time=5.7,rate_func=linear);self.to(138);self.note_at('단순 조화 운동',color=TEAL,size=31)
 def s12(self):
  self.t=ValueTracker(0);self.add(always_redraw(lambda:self.pendulum(.2*np.cos(self.t.get_value()),x=-1.8,y=3.8)),always_redraw(lambda:self.molecule(np.cos(1.4*self.t.get_value()),x=1.8,y=2.55,scale=.85)))
  self.add(text('작은 각도 θ',x=-1.8,y=1.1,size=23,color=TEAL),text('작은 결합 변위 q',x=1.8,y=1.1,size=23,color=PURPLE));self.formulas(r'\ddot\theta+\frac{g}{\ell}\theta\approx0\quad(|\theta|\ll1)',r'\ddot q+\frac{k}{\mu}q\approx0',colors=[TEAL,PURPLE]);self.note_at('작은 진동 · 분자는 한 결합의 1차원 모델',size=23)
  self.to(143);self.show(eq(r'\mu=\frac{m_1m_2}{m_1+m_2}',y=-.35,color=PURPLE,size=32));self.play(self.t.animate.set_value(6),run_time=6,rate_func=linear)
 def circuit(self):
  left,right=-2.1,2.1;top,bottom=3.6,1.25
  g=VGroup(Line([left,top,0],[-1.1,top,0],color=BLUE),self.coil([-1.1,top,0],[1.1,top,0],PURPLE,7,.2),Line([1.1,top,0],[right,top,0],color=BLUE),Line([right,top,0],[right,2.65,0],color=BLUE),Line([right-.45,2.65,0],[right+.45,2.65,0],color=TEAL,stroke_width=4),Line([right-.45,2.25,0],[right+.45,2.25,0],color=TEAL,stroke_width=4),Line([right,2.25,0],[right,bottom,0],color=BLUE),Line([right,bottom,0],[left,bottom,0],color=BLUE),Line([left,bottom,0],[left,top,0],color=BLUE),text('L',x=0,y=4.05,size=25,color=PURPLE),text('C',x=3,y=2.45,size=25,color=TEAL));return g
 def energy_bars(self,t):
  ec,el=lc_energies(t);g=VGroup()
  for x,value,c in [(-1.5,ec,TEAL),(1.5,el,PURPLE)]:
   g.add(Rectangle(width=.65,height=max(.012,float(value)*1.3),fill_color=c,fill_opacity=.8,stroke_width=0).move_to([x,-.6+float(value)*.65,0]))
  return g
 def s13(self):
  self.t=ValueTracker(0);self.add(self.circuit(),always_redraw(lambda:self.energy_bars(self.t.get_value())),text('축전기 전기 에너지',x=-1.5,y=-1.05,size=21,color=TEAL,width=3),text('코일 자기 에너지',x=1.5,y=-1.05,size=21,color=PURPLE,width=3))
  self.note_at('저항 없는 이상적 LC 회로 · 총에너지 일정',size=23);self.formulas(r'L\ddot Q+\frac QC=0',r'\ddot Q+\frac1{LC}Q=0',colors=[WHITE,TEAL]);self.play(self.t.animate.set_value(4.5),run_time=4.5,rate_func=linear)
 def s14(self):
  names=['용수철','작은 진자','분자 진동','LC 회로'];ss=[r'k/m',r'g/\ell',r'k/\mu',r'1/(LC)'];colors=[ORANGE,TEAL,PURPLE,BLUE]
  self.cards=VGroup()
  for i,(n,s,c) in enumerate(zip(names,ss,colors)):
   y=3.6-i*1.05;self.cards.add(text(n,x=-2.2,y=y,size=25,color=c),eq(r'\omega^2='+s,y=y,color=c,size=32).move_to([1.5,y,0]))
  self.show(self.cards);self.formulas(r'\ddot q+\omega^2q=0',colors=[TEAL]);self.note_at('물리계마다 ω는 달라도, 방정식의 형태는 같다',size=24,color=TEAL)
  self.to(163);self.drop(self.cards);pg,_=self.potential_graph(.2,True);self.show(pg);self.formulas(r'V\approx V_0+\tfrac12kq^2\ \Rightarrow\ F\approx-kq',r'\Rightarrow\quad\ddot q+\omega^2q\approx0',colors=[ORANGE,TEAL]);self.note_at('안정 최소점 · 작은 변위 · V″>0',size=25)
 def s15(self):
  self.t=ValueTracker(0);self.add(*[always_redraw(lambda k=k,x=x:self.miniature(k,self.t.get_value(),x,2.8)) for k,x in enumerate([-2.5,0,2.5])])
  self.show(text('안정 평형점의 작은 진동',y=.5,size=31,color=TEAL));self.formulas(r'\boxed{\ddot q+\omega^2q=0}',r'q(t)=A\cos(\omega t+\phi)',colors=[TEAL,TEAL]);self.note_at('다양한 자연현상을 잇는 공통 구조',size=27,color=TEAL);self.play(self.t.animate.set_value(5.5),run_time=5.5,rate_func=linear)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
