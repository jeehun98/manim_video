"""Complex multiplication rendered with actual arithmetic and equal axis units."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,label,text,p,L
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#101622'
INK,BLUE,PURPLE,ORANGE,GOLD,GREEN,MUTED='#F0F3FA','#6DBBEE','#B69BF0','#EAB56B','#F3D17E','#65D3B0','#718096'
def eq(s,x=0,y=0,size=36,color=INK,width=7.4):
 m=MathTex(s,font_size=size*1.35,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to(p(x,y))
def plane(r=2.8,size=6.2,x=0,y=.4):
 a=Axes(x_range=[-r,r,1],y_range=[-r,r,1],x_length=size,y_length=size,tips=False,axis_config={'color':MUTED,'stroke_width':1.1,'include_ticks':False}).move_to(p(x,y))
 assert np.isclose(np.linalg.norm(a.c2p(1,0)-a.c2p(0,0)),np.linalg.norm(a.c2p(0,1)-a.c2p(0,0)))
 return a
def pt(a,z):return a.c2p(complex(z).real,complex(z).imag)
def vec(a,z,color=BLUE):return Arrow(pt(a,0),pt(a,z),buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.17)
def labs(a,unit=False):
 r=VGroup(label('실수 Re',size=18,color=BLUE).move_to(a.get_right()+DOWN*.25+LEFT*.35),label('허수 Im',size=18,color=PURPLE).move_to(a.get_top()+RIGHT*.25+DOWN*.12))
 if unit:
  for z,s in [(1,'1'),(1j,'i'),(-1,'−1'),(-1j,'−i')]:r.add(label(s,size=24,color=PURPLE if z.imag else BLUE).move_to(pt(a,z)+(.25*RIGHT if z.imag else .3*DOWN)))
 return r
class ComplexScene(QCSScene):
 data=DATA
 def replace(self,old,new):return Scene.replace(self,old,new)
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.add(text('수학적 구조  /  복소수와 회전',y=L.brand_y,size=18,color=MUTED))
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for o in self.mobjects:
   if o is getattr(self,'caption',None) or o is getattr(self,'caption_panel',None):continue
   if o.width<.001 or o.height<.001:continue
   assert o.get_left()[0]>=-4.38 and o.get_right()[0]<=4.38,('horizontal',self.shot,self.time)
   assert o.get_bottom()[1]>=-4.9 and o.get_top()[1]<=7.9,('vertical',self.shot,self.time)
 def clear_body(self):
  obs=[o for o in self.mobjects if all(o is not k for k in [self.title,self.caption,self.caption_panel]) and o.get_center()[1]<4.9]
  if obs:self.play(*[FadeOut(o) for o in obs],run_time=.4)
 def turn(self,a,z,start_angle=0,angle=PI/2,duration=2):
  v=vec(a,z,GOLD);d=Dot(pt(a,z),color=GOLD,radius=.09);self.add(v,d)
  self.play(Rotate(v,angle,about_point=pt(a,0)),Rotate(d,angle,about_point=pt(a,0)),run_time=duration)
  arc=Arc(radius=.65,start_angle=start_angle,angle=angle,arc_center=pt(a,0),color=ORANGE,stroke_width=2)
  self.add(arc);return v,d,arc
 def pair(self,r=1.2,normalized=False):
  a=plane(r,3.25,-1.95,.6);b=plane(r,3.25,1.95,.6)
  self.show(a,b,label('h / |h|' if normalized else '입력의 변화 h',x=-1.95,y=2.65,size=23,color=BLUE,width=3.3),label('Δf / |h|' if normalized else '출력의 변화 Δf',x=1.95,y=2.65,size=23,color=GREEN,width=3.3))
  return a,b
 def s01(self):
  a=plane(2.8);nums=VGroup(*[label(str(k),size=24,color=MUTED).move_to(pt(a,k)+DOWN*.35) for k in [-2,-1,0,1,2]])
  self.show(a.x_axis,nums,Dot(pt(a,2),color=BLUE,radius=.09))
  self.note('직선 위의 위치 → 평면 위의 두 좌표')
  self.to(3);self.play(Create(a.y_axis),run_time=1.2);self.show(label('실수',x=2.8,y=0,size=23,color=BLUE),label('허수',x=.55,y=3.3,size=23,color=PURPLE))
 def s02(self):
  a=plane(3.6);self.show(a,labs(a));self.show(vec(a,2+3j),Dot(pt(a,2+3j),color=GOLD,radius=.09),eq('z=2+3i',y=4.45,color=BLUE))
  self.show(Line(pt(a,0),pt(a,2),color=BLUE,stroke_width=4),Line(pt(a,2),pt(a,2+3j),color=PURPLE,stroke_width=4))
  self.show(label('2',size=25,color=BLUE).move_to(pt(a,1)+DOWN*.3),label('3i',size=25,color=PURPLE).move_to(pt(a,2+1.5j)+RIGHT*.35))
  self.to(11);self.note('가로: 실수부 2   ·   세로: 허수부 3')
  self.to(14);self.show(eq('i^2=-1',y=-3.1,size=43,color=PURPLE));self.note('허수 단위 i의 정의')
 def s03(self):
  a=plane(1.8);self.show(a,labs(a,True));self.note('원점을 중심으로 · 길이를 유지하며')
  self.to(22);v=vec(a,1,GOLD);d=Dot(pt(a,1),color=GOLD,radius=.09);self.show(v,d,eq('1',y=4.45,color=GOLD))
  self.to(24);self.play(Rotate(v,PI/2,about_point=pt(a,0)),Rotate(d,PI/2,about_point=pt(a,0)),run_time=2.7)
  self.show(Arc(radius=.8,angle=PI/2,arc_center=pt(a,0),color=ORANGE),eq(r'1\times i=i',y=-3.15,color=PURPLE),label('90°',x=.8,y=1.2,size=27,color=ORANGE))
 def s04(self):
  a=plane(1.8);self.show(a,labs(a,True));v=vec(a,1j,GOLD);d=Dot(pt(a,1j),color=GOLD,radius=.09);self.show(v,d,eq(r'i\times i=-1',y=4.45,color=PURPLE))
  self.to(31);self.play(Rotate(v,PI/2,about_point=pt(a,0)),Rotate(d,PI/2,about_point=pt(a,0)),run_time=3)
  self.show(Arc(radius=.8,start_angle=PI/2,angle=PI/2,arc_center=pt(a,0),color=ORANGE));self.note('iを 곱할 때마다 반시계방향 90°'.replace('を','를'))
  self.to(36);self.show(eq(r'i(x+iy)=-y+ix',y=-2.7,size=31,color=PURPLE),eq(r'(x,y)\longmapsto(-y,x)',y=-3.35,size=28))
 def s05(self):
  a=plane(1.8);self.show(a,labs(a,True));self.add(*[Dot(pt(a,z),radius=.055,color=MUTED) for z in [1,1j,-1,-1j]])
  v=vec(a,-1,GOLD);d=Dot(pt(a,-1),color=GOLD,radius=.09);self.add(v,d)
  self.play(Rotate(v,PI/2,about_point=pt(a,0)),Rotate(d,PI/2,about_point=pt(a,0)),run_time=1.3)
  self.play(Rotate(v,PI/2,about_point=pt(a,0)),Rotate(d,PI/2,about_point=pt(a,0)),run_time=1.3)
  self.show(eq(r'1\to i\to-1\to-i\to1',y=4.45,size=30),eq(r'i^4=1',y=-3.15,color=GOLD),run_time=.4);self.note('90° × 4 = 360°')
 def s06(self):
  a=plane(1.8);self.show(a,labs(a));self.note('まず 1+i 자체의 모양을 살펴보면'.replace('まず ','먼저 '))
  self.to(49);self.show(vec(a,1+1j,GOLD),Dot(pt(a,1+1j),radius=.09,color=GOLD),eq('1+i',y=4.45,color=GOLD))
  self.to(53);self.show(DashedLine(pt(a,1),pt(a,1+1j),color=PURPLE),Line(pt(a,0),pt(a,1),color=BLUE),Arc(radius=.9,angle=PI/4,arc_center=pt(a,0),color=ORANGE))
  self.show(label('1',size=24,color=BLUE).move_to(pt(a,.5)+DOWN*.25),label('1',size=24,color=PURPLE).move_to(pt(a,1+.5j)+RIGHT*.25),label('45°',x=.85,y=.75,size=25,color=ORANGE),eq(r'|1+i|=\sqrt{1^2+1^2}=\sqrt2',y=-3.05,size=32,color=GOLD));self.note('각도 45°   ·   원점에서 거리 √2')
 def s07(self):
  a=plane(2.5);self.show(a,labs(a),eq(r'z\longmapsto(1+i)z',y=4.45,size=36,color=GREEN))
  zs=[1+.25j,-.75+.7j,-.55-1.05j];t=ValueTracker(0)
  ghosts=VGroup(*[vec(a,z,BLUE).set_stroke(opacity=.3) for z in zs]);vs=VGroup(*[vec(a,z,GOLD) for z in zs]);self.show(ghosts,vs)
  for v,z in zip(vs,zs):v.add_updater(lambda m,z=z:m.become(vec(a,z*2**(t.get_value()/2)*np.exp(1j*PI*t.get_value()/4),GOLD)))
  self.show(eq(r'45^\circ\quad\times\sqrt2',y=-2.9,size=38,color=ORANGE));self.note('모든 벡터에 같은 회전과 같은 배율')
  self.play(t.animate.set_value(1),run_time=4.5)
  for v in vs:v.clear_updaters()
  self.to(65);self.show(eq(r'(x,y)\mapsto(x-y,x+y)',y=3.65,size=27,color=GREEN));self.note('서로의 각도는 유지 · 길이는 모두 √2배')
 def s08(self):
  self.show(eq(r'f(z)=z^2',y=4.4,color=GREEN));self.note('입력의 작은 변화와 출력의 변화를 비교한다')
  self.to(73);a,b=self.pair(3.6);z=1+1j;h=.45+.1j
  self.show(Dot(pt(a,z),color=BLUE),Dot(pt(b,z*z),color=GREEN),label('z₀',size=23,color=BLUE).move_to(pt(a,z)+LEFT*.35),label('f(z₀)',size=21,color=GREEN).move_to(pt(b,z*z)+RIGHT*.45))
  self.to(78);self.show(Arrow(pt(a,z),pt(a,z+h),buff=0,color=GOLD),Arrow(pt(b,z*z),pt(b,(z+h)**2),buff=0,color=GOLD))
  self.show(eq(r'\Delta f=f(z_0+h)-f(z_0)',y=-2,size=32),eq(r'\frac{\Delta f}{h}',y=-3.05,size=38,color=GOLD));self.note('유한한 변화 Δf는 아직 단순한 회전·배율이 아니다')
 def s09(self):
  a=plane(1.7);self.show(a,labs(a),eq(r'\lim_{h\to0}\frac{f(z_0+h)-f(z_0)}{h}',y=4.35,size=33,color=GOLD))
  self.show(Line(pt(a,-1.2),pt(a,1.2),color=BLUE,stroke_width=4));self.note('실수: 수직선 위에서 왼쪽 또는 오른쪽')
  self.to(88);self.note('복소수: 평면의 모든 방향 · 모든 경로')
  arrows=VGroup(*[Arrow(pt(a,1.2*np.exp(1j*t)),pt(a,.2*np.exp(1j*t)),buff=0,color=PURPLE,stroke_width=2) for t in np.linspace(0,TAU,8,endpoint=False)]);self.show(arrows)
  curve=ParametricFunction(lambda t:pt(a,(1.3-t)*np.exp(1j*3*t)),t_range=[0,1.28],color=ORANGE,stroke_width=3)
  self.to(91);self.play(Create(curve),run_time=1.4);self.show(eq(r'\text{one limit: }f\prime(z_0)',y=-3.1,size=30,color=GREEN));self.note('몇 방향만 확인하는 것으로는 충분하지 않다')
 def s10(self):
  self.show(eq(r'\Delta f=ch+h^2,\quad c=2+2i',y=4.4,size=31,color=GREEN));a,b=self.pair(3.3,normalized=True)
  self.show(label('두 변화에 같은 확대 배율 1/|h|',y=3.35,size=21,color=MUTED),run_time=.2)
  h=ValueTracker(.36);theta=.3;c=2+2j
  vin=vec(a,np.exp(1j*theta),BLUE);lin=vec(b,c*np.exp(1j*theta),GREEN);exact=Dot(pt(b,c*np.exp(1j*theta)+h.get_value()*np.exp(2j*theta)),color=GOLD,radius=.07)
  self.show(vin,lin,exact,label('청록: 근사   ·   금색 점: 실제 변화',y=-1.65,size=23,color=GREEN))
  self.to(99);self.show(eq(r'\Delta f=f\prime(z_0)h+o(|h|)',y=-2.5,size=34,color=GOLD));self.note('f(z)=z², z₀=1+i  →  f′(z₀)=2+2i')
  
  exact.add_updater(lambda m:m.move_to(pt(b,c*np.exp(1j*theta)+h.get_value()*np.exp(2j*theta))))
  self.to(106);self.play(h.animate.set_value(.065),run_time=3)
  for m in [vin,lin,exact]:m.clear_updaters()
  self.show(eq(r'|h^2|/|h|=|h|\to0',y=-3.15,size=27,color=ORANGE));self.note('작아질수록 실제 변화가 곱셈 ch에 가까워진다')
 def s11(self):
  a,b=self.pair(1.25);c=2+2j;h=.36
  self.show(eq(r'c=f\prime(z_0)=2+2i',y=4.4,size=31,color=GREEN));v=vec(a,h,BLUE);w=vec(b,c*h,GREEN);self.show(v,w)
  self.note('어느 방향의 h에도 같은 복소수 c를 곱한다')
  self.to(117);self.add(vec(a,h,BLUE).set_stroke(opacity=.3),vec(b,c*h,GREEN).set_stroke(opacity=.3))
  self.play(Rotate(v,PI/2,about_point=pt(a,0)),Rotate(w,PI/2,about_point=pt(b,0)),run_time=3.5)
  self.show(eq(r'c(ih)=i(ch)',y=-1.8,size=38,color=GOLD));self.note('입력의 90° 회전 → 출력도 같은 90° 회전')
  self.to(123);self.show(eq(r'u_y+iv_y=i(u_x+iv_x)',y=-2.7,size=30,color=PURPLE),eq(r'=-v_x+i u_x',y=-3.35,size=29,color=PURPLE));self.note('c≠0: 회전·배율   /   c=0: 1차 변화가 0',MUTED)
 def s12(self):
  self.show(eq(r'f=u+iv',y=4.35,size=33),eq(r'u_y+iv_y=-v_x+i u_x',y=2.7,size=34,color=PURPLE),run_time=.4)
  self.show(eq(r'u_x=v_y',y=.95,size=49,color=BLUE),run_time=.5);self.show(eq(r'u_y=-v_x',y=-.45,size=49,color=PURPLE),run_time=.5)
  self.show(label('실수부끼리 · 허수부끼리 같아야 한다',y=-2,size=26),run_time=.4);self.note('실수 전미분가능을 가정할 때 CR 조건과 동치',MUTED)
 def s13(self):
  a=plane(2.2,size=4.8,y=.6);self.show(a,labs(a),eq(r'\Delta f\approx f\prime(z_0)h',y=4.35,size=42,color=GOLD));self.note('각 지점 주변의 아주 작은 변화에 대한 근사')
  t=ValueTracker(0);v=vec(a,.7,BLUE);w=vec(a,(1+.6j)*.7,GREEN);self.show(v,w)
  v.add_updater(lambda m:m.become(vec(a,.7*np.exp(1j*t.get_value()),BLUE)));w.add_updater(lambda m:m.become(vec(a,(1+.6j)*.7*np.exp(1j*t.get_value()),GREEN)))
  self.to(137);self.play(t.animate.set_value(TAU),run_time=4.2,rate_func=linear)
  v.clear_updaters();w.clear_updaters();self.show(label('모든 방향에 하나의 복소수 곱셈',y=-2.4,size=32,color=GREEN))
  self.to(142);self.show(eq(r'\Delta f=ch+o(|h|)',y=-3.25,size=32,color=GOLD));self.note('c=0이면 1차 변화는 0 · 회전각은 정의하지 않는다',MUTED)
