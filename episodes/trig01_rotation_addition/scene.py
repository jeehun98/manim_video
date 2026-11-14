"""One persistent coordinate system; narration boundaries supplied by the user."""
import sys,json,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,text,FONT
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#0B1020'
A=PI/6; B=40*DEGREES
TEAL,BLUE,GOLD,PURPLE,RED,MUTED='#48CEC5','#66A5FF','#F1B763','#B89CFF','#F08088','#7F8CA5'
def eq(s,y=-2.45,color=WHITE,size=36):
 m=MathTex(s,font_size=size,color=color)
 if m.width>7.65:m.scale_to_fit_width(7.65)
 return m.move_to([0,y,0])
def col(x,y):return r'\begin{pmatrix}'+x+r'\\'+y+r'\end{pmatrix}'
M=r'\begin{pmatrix}\cos\beta&-\sin\beta\\\sin\beta&\cos\beta\end{pmatrix}'
COS=r'\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta'
SIN=r'\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta'
class TrigAdditionGeometry(QCSScene):
 data=DATA
 def replace(self,old,new):return Scene.replace(self,old,new)
 def setup(self):
  super().setup();self.offset=0
  self.remove(self.mobjects[0]);self.add(text('수학의 연결  /  회전의 세 가지 표현',y=7.15,size=18,color=MUTED))
  self.form=VGroup();self.overlay=VGroup();self.graph_ready=False
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for o in self.mobjects:
   if o is self.caption or o is self.caption_panel:continue
   if o.width<.001 or o.height<.001:continue
   assert o.get_left()[0]>=-4.39 and o.get_right()[0]<=4.39,('x',self.time,str(o))
   assert o.get_bottom()[1]>=-4.9 and o.get_top()[1]<=7.9,('y',self.time,str(o))
 def heading(self,i):
  self.play(Transform(self.title,text(DATA['scenes'][i-1]['title'],y=5.5,size=33,width=7.7)),run_time=.35)
 def formulas(self,*strings,colors=None):
  new=VGroup(*[eq(s,y=-2.25-i*.95,color=(colors[i] if colors else WHITE)) for i,s in enumerate(strings)])
  if len(self.form):self.play(FadeOut(self.form),FadeIn(new),run_time=.45)
  else:self.play(FadeIn(new),run_time=.45)
  self.form=new
 def clean(self):
  if len(self.overlay):self.remove(*self.overlay.get_family())
  self.overlay=VGroup()
 def graph(self,angle=0):
  self.axes=Axes(x_range=[-1.3,1.3,1],y_range=[-1.3,1.3,1],x_length=5.8,y_length=5.8,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.4}).move_to([0,1.25,0])
  self.origin=self.axes.c2p(0,0);self.unit=np.linalg.norm(self.axes.c2p(1,0)-self.origin)
  self.circle=Circle(radius=self.unit,color=MUTED,stroke_width=1.4,stroke_opacity=.5).move_to(self.origin)
  self.theta=ValueTracker(angle)
  self.vector=always_redraw(lambda:self.arrow(np.exp(1j*self.theta.get_value()),TEAL))
  self.dot=always_redraw(lambda:Dot(self.pt(np.exp(1j*self.theta.get_value())),radius=.07,color=TEAL))
  self.axis_labels=VGroup(text('x',size=22,color=MUTED).move_to(self.axes.get_right()+DOWN*.25),text('y',size=22,color=MUTED).move_to(self.axes.get_top()+RIGHT*.25))
  self.add(self.axes,self.circle,self.axis_labels,self.vector,self.dot);self.graph_ready=True
 def pt(self,z):return self.axes.c2p(complex(z).real,complex(z).imag)
 def arrow(self,z,c,start=0):return Arrow(self.pt(start),self.pt(start+z),buff=0,color=c,stroke_width=5,max_tip_length_to_length_ratio=.15)
 def arc(self,start,angle,c,r=.6):return Arc(radius=r,start_angle=start,angle=angle,arc_center=self.origin,color=c,stroke_width=3)
 def project(self,z,c=TEAL):
  return VGroup(DashedLine(self.pt(z),self.pt(z.real),color=c,stroke_width=2),DashedLine(self.pt(z),self.pt(1j*z.imag),color=c,stroke_width=2))
 def turn(self,value,seconds=2):self.play(self.theta.animate.set_value(value),run_time=seconds)
 def s01(self):
  self.formulas(r'\sin(\alpha+\beta)\;=?')
  self.to(2);self.formulas(SIN,colors=[GOLD])
  self.to(8);self.formulas(SIN,COS,colors=[GOLD,BLUE])
  self.to(14);self.show(text('각도의 덧셈이\n왜 곱과 합이 될까?',y=1.4,size=43,width=7.5,color=TEAL))
  self.question=self.mobjects[-1];self.to(19);self.remove(self.question,self.form);self.form=VGroup()
 def s02(self):
  self.heading(2);self.graph();self.formulas(r'\mathbf v_0=(1,0),\qquad |\mathbf v_0|=1')
  self.to(24);self.turn(A,2.5)
  self.overlay=VGroup(self.arc(0,A,GOLD),self.project(np.exp(1j*A)),eq(r'\alpha=30^\circ',y=4.5,color=GOLD,size=27));self.show(self.overlay)
  self.formulas(r'\mathbf v_\alpha='+col(r'\cos\alpha',r'\sin\alpha'))
 def s03(self):
  self.heading(3);self.clean();self.overlay=VGroup(self.arc(0,A,GOLD),self.arc(A,B,PURPLE,r=.85));self.show(self.overlay);self.to(33)
  ghost=self.arrow(np.exp(1j*A),GOLD).set_opacity(.3);self.add(ghost);self.overlay.add(ghost)
  self.turn(A+B,3);self.overlay.add(self.project(np.exp(1j*(A+B))));self.add(self.overlay[-1]);self.formulas(r'\mathbf v_{\alpha+\beta}='+col(r'\cos(\alpha+\beta)',r'\sin(\alpha+\beta)'))
  self.show(text('β = 40°   ·   α + β = 70°',y=-3.8,size=25,color=PURPLE));self.beta_note=self.mobjects[-1]
 def components(self,rotated=False):
  self.h=self.arrow(np.cos(A)*np.exp(1j*(B if rotated else 0)),BLUE)
  self.k=self.arrow(np.sin(A)*np.exp(1j*(PI/2+(B if rotated else 0))),GOLD)
  self.add(self.h,self.k)
 def s04(self):
  self.heading(4);self.clean();self.remove(self.beta_note);self.turn(A,1.4)
  self.to(45);self.components();self.formulas(col(r'\cos\alpha',r'\sin\alpha')+'='+col(r'\cos\alpha','0')+'+'+col('0',r'\sin\alpha'))
  self.play(self.vector.animate.set_opacity(.28),run_time=.3)
 def s05(self):
  self.heading(5);self.play(Rotate(self.h,B,about_point=self.origin),run_time=2.5)
  z=np.cos(A)*np.exp(1j*B);self.overlay=VGroup(self.project(z,BLUE),self.arc(0,B,PURPLE));self.show(self.overlay)
  self.formulas(r'R(\beta)\mathbf h='+col(r'\cos\alpha\cos\beta',r'\cos\alpha\sin\beta'),colors=[BLUE])
 def s06(self):
  self.heading(6);self.clean();self.play(self.h.animate.set_opacity(.3),Rotate(self.k,B,about_point=self.origin),run_time=2.5)
  z=np.sin(A)*np.exp(1j*(PI/2+B))
  self.overlay=VGroup(self.project(z,GOLD),self.arrow(z.real,RED),text('왼쪽으로 → x < 0',y=4.5,size=26,color=RED));self.show(self.overlay)
  self.formulas(r'R(\beta)\mathbf k='+col(r'-\sin\alpha\sin\beta',r'\sin\alpha\cos\beta'),colors=[GOLD])
 def s07(self):
  self.heading(7);self.clean();self.h.set_opacity(1)
  zh=np.cos(A)*np.exp(1j*B);self.play(self.k.animate.shift(self.pt(zh)-self.origin),run_time=1.8)
  self.turn(A+B,1);self.formulas(r'R(\beta)\mathbf h+R(\beta)\mathbf k=\mathbf v_{\alpha+\beta}')
  self.to(68);self.formulas(col(r'\cos\alpha\cos\beta',r'\cos\alpha\sin\beta')+'+'+col(r'-\sin\alpha\sin\beta',r'\sin\alpha\cos\beta'),colors=[TEAL])
 def s08(self):
  self.heading(8);self.formulas(COS,colors=[BLUE])
  zh=np.cos(A)*np.exp(1j*B);zk=np.sin(A)*np.exp(1j*(PI/2+B))
  self.overlay=VGroup(self.arrow(zh.real,BLUE),self.arrow(zk.real,RED,start=zh.real));self.show(self.overlay)
  self.to(80);self.clean();self.formulas(COS,SIN,colors=[BLUE,GOLD])
  self.overlay=VGroup(self.arrow(1j*zh.imag,BLUE),self.arrow(1j*zk.imag,GOLD,start=1j*zh.imag));self.show(self.overlay)
  self.to(85);self.play(Circumscribe(self.form,color=TEAL),run_time=1.3)
  self.to(89);self.clean();self.remove(self.h,self.k);self.show(text('각도를 더한 결과 = 회전한 성분들의 합',y=4.5,size=25,width=7.5,color=TEAL))
  self.summary=self.mobjects[-1];self.turn(0,1);self.turn(A,1);self.turn(A+B,1.3)
 def s09(self):
  self.heading(9);self.remove(self.summary);self.formulas(col(r'\cos\beta',r'\sin\beta')+r'\qquad'+col(r'-\sin\beta',r'\cos\beta'))
  e1=self.arrow(1,BLUE);e2=self.arrow(1j,GOLD);self.add(e1,e2)
  self.play(Rotate(e1,B,about_point=self.origin),Rotate(e2,B,about_point=self.origin),run_time=1.7)
  self.to(98)
  matrix=Matrix([[r'\cos\beta',r'-\sin\beta'],[r'\sin\beta',r'\cos\beta']],h_buff=1.9).scale(.65).move_to([.7,-2.7,0])
  matrix.get_columns()[0].set_color(BLUE);matrix.get_columns()[1].set_color(GOLD)
  prefix=eq(r'R(\beta)=',y=-2.7,size=32).move_to([-2.3,-2.7,0]);new=VGroup(prefix,matrix)
  self.play(ReplacementTransform(self.form,new),run_time=1);self.form=new
  self.overlay=VGroup(e1,e2)
  self.show(text('첫째 열: 가로 단위벡터   ·   둘째 열: 세로 단위벡터',y=4.5,size=22,width=7.6,color=MUTED));self.column_note=self.mobjects[-1]
  self.to(103);self.clean();self.turn(A,1);self.turn(A+B,2)
  self.formulas(r'R(\beta)'+col('x','y')+'='+col(r'x\cos\beta-y\sin\beta',r'x\sin\beta+y\cos\beta'))
 def s10(self):
  self.heading(10);self.remove(self.column_note);self.turn(0,1)
  self.formulas(r'R(\alpha)\quad\longrightarrow\quad R(\beta)')
  self.to(113);self.formulas(r'R(\beta)\bigl(R(\alpha)\mathbf v_0\bigr)');self.turn(A,1.7);self.turn(A+B,1.7)
  self.to(119);self.formulas(r'R(\beta)R(\alpha)=R(\alpha+\beta)',colors=[PURPLE])
  direct=self.arrow(1,GOLD).set_opacity(.55);self.add(direct);self.overlay.add(direct)
  self.play(Rotate(direct,A+B,about_point=self.origin),run_time=2.2)
 def s11(self):
  self.heading(11);self.clean();self.formulas(r'R(\beta)R(\alpha)='+M+r'\begin{pmatrix}\cos\alpha&-\sin\alpha\\\sin\alpha&\cos\alpha\end{pmatrix}')
  self.to(126);self.formulas(col(r'\cos\beta\cos\alpha-\sin\beta\sin\alpha',r'\sin\beta\cos\alpha+\cos\beta\sin\alpha')+'='+col(r'\cos(\alpha+\beta)',r'\sin(\alpha+\beta)'),colors=[TEAL])
 def s12(self):
  self.heading(12);self.formulas(r'(x,y)\quad\longleftrightarrow\quad z=x+iy')
  self.to(133)
  new=VGroup(text('Re',size=21,color=BLUE).move_to(self.axis_labels[0]),text('Im',size=21,color=GOLD).move_to(self.axis_labels[1]))
  self.play(Transform(self.axis_labels,new),run_time=.7)
  self.formulas(r'z=\cos\theta+i\sin\theta')
  self.to(138);self.formulas(r'e^{i\theta}=\cos\theta+i\sin\theta',r'|e^{i\theta}|=1\qquad\arg z=\theta\pmod{2\pi}',colors=[TEAL,MUTED]);self.overlay=self.project(np.exp(1j*(A+B)));self.show(self.overlay)
 def s13(self):
  self.heading(13);self.clean();self.turn(0,1);self.formulas(r'(r_1e^{i\alpha})(r_2e^{i\beta})=r_1r_2e^{i(\alpha+\beta)}')
  self.to(148);self.formulas(r'1\xrightarrow{\times e^{i\alpha}}e^{i\alpha}',colors=[GOLD]);self.turn(A,2)
  self.overlay=VGroup(self.arc(0,A,GOLD));self.add(self.overlay)
  self.to(151.5);self.formulas(r'e^{i\alpha}\xrightarrow{\times e^{i\beta}}e^{i(\alpha+\beta)}',colors=[PURPLE]);self.turn(A+B,2)
  self.overlay.add(self.arc(A,B,PURPLE,r=.85));self.add(self.overlay[-1])
 def s14(self):
  self.heading(14);self.formulas(r'R(\beta)R(\alpha)=R(\alpha+\beta)',r'e^{i\beta}e^{i\alpha}=e^{i(\alpha+\beta)}',colors=[BLUE,PURPLE])
  self.play(Indicate(self.vector,color=TEAL),run_time=1.5)
 def s15(self):
  self.heading(15);self.clean();self.formulas(r'(\cos(\alpha+\beta),\;\sin(\alpha+\beta))',r'R(\beta)R(\alpha)\quad\longleftrightarrow\quad e^{i\beta}e^{i\alpha}',colors=[TEAL,PURPLE])
  self.show(text('좌표 성분  ·  행렬  ·  복소수',y=4.5,size=28,color=TEAL));self.last_note=self.mobjects[-1]
  self.to(169);self.turn(0,1);self.turn(A,1.2);self.turn(A+B,1.6)
  self.formulas(r'\alpha+\beta\quad\longleftrightarrow\quad R(\beta)\circ R(\alpha)',colors=[TEAL])
  self.play(Transform(self.last_note,text('각도의 덧셈은 회전의 합성이다',y=4.5,size=30,color=TEAL,width=7.6)),run_time=.6)
 def construct(self):
  for i,s in enumerate(DATA['scenes'],1):
   self.next_section(s['id']);getattr(self,f's{i:02}')();self.to(s['end'])
  self.finish_audit()
 def finish_audit(self):
  self.caption.remove_updater(self.update_caption)
  target=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));target.mkdir(parents=True,exist_ok=True)
  (target/(self.__class__.__name__+'_captions.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
class ComponentsPreview(TrigAdditionGeometry):
 def construct(self):
  self.offset=49;self.graph(A);self.components();self.s05();self.to(56);self.s06();self.to(64);self.s07();self.to(75);self.finish_audit()
class MatrixPreview(TrigAdditionGeometry):
 def construct(self):
  self.offset=95;self.graph(A+B);self.summary=VGroup();self.s09();self.to(110);self.finish_audit()
