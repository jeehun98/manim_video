"""69-second visual prologue, reusing the four chapters' verified geometry."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from longforms.complex_geometry_01.direction import GeometryScene,plane,pt,vec,curve,circle_samples,eq,label,p,INPUT,OUTPUT,GOLD,RED,INK,MUTED
from longforms.complex_geometry_02.direction import TemperatureMesh,conformal_grid,rim as heat_rim
from longforms.complex_geometry_03.direction import sphere,torus,sheets,lifted_point,project,poly
from longforms.complex_geometry_04.direction import DiskPattern,rim,hcircle,rings
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
assets=HERE.parents[1]/'media'/'complex_geometry_00_assets'/os.getenv('CG_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex');config.text_dir=str(assets/'texts')

class IntroScene(GeometryScene):
 data=DATA
 def s01(self):
  a=plane(1.2,4.2,x=-3.4);border=rim(-3.4,R=1.75,c=INPUT)
  self.show(a,border,label('평평한 원판 안에',x=3.5,y=1.2,size=31,width=6.5),label('얼마나 넓은 공간을 담을 수 있을까?',x=3.5,y=.1,size=29,width=6.7,color=GOLD),run_time=.8)
  self.to(4);pattern=DiskPattern(x=-3.4,R=1.75);self.play(FadeOut(a),FadeIn(pattern),run_time=1)
  self.play(UpdateFromAlphaFunc(pattern,lambda m,a:m.set_observer(.36*smooth(a))),run_time=3,rate_func=linear)
  self.to(8);self.show(label('From Complex Numbers to Geometry',x=3.5,y=-1.1,size=22,width=6.5,color=MUTED),run_time=.4)
  self.play(UpdateFromAlphaFunc(pattern,lambda m,a:m.set_observer(.36-.12*a)),run_time=3.5,rate_func=linear)
  self.to(12);self.wipe();b=plane(1.6,3.8,x=-3.5)
  self.show(b,vec(b,1,INPUT),eq(r'z\longmapsto az',x=3.5,y=.8,size=43,color=INPUT),run_time=.5)
 def s02(self):
  a=plane(1.6,3.8,x=-3.5);v=vec(a,1,INPUT)
  self.add(a,v,eq(r'z\longmapsto az',x=3.5,y=.8,size=43,color=INPUT))
  self.play(Transform(v,vec(a,1.3*np.exp(.65j),OUTPUT)),run_time=2)
  self.to(16);self.wipe();a,b=self.pair(1.6,3.6)
  left=circle_samples(a,lambda t:.65*np.exp(1j*t),INPUT);right=circle_samples(b,lambda t:.65*np.exp(1j*t),INPUT)
  self.show(left,right,vec(a,.65,INPUT),vec(a,.65j,GOLD),run_time=.4)
  self.to(19);self.play(Transform(right,circle_samples(b,lambda t:1.15*np.exp(1j*(t+.65)),OUTPUT)),run_time=1.5)
  self.show(eq(r'\Delta f\approx f\prime(z)\Delta z',y=2.5,size=36,color=GOLD),label('복소미분 · 각 점 주변의 변화 규칙',y=-2,size=29,color=OUTPUT),run_time=.5)
 def s03(self):
  a=plane(1.7,4,x=-3.5);w=.3+.2j;shrink=ValueTracker(0);theta=ValueTracker(0)
  field=VGroup(*[Circle(radius=.085,color=OUTPUT,stroke_width=1.1).move_to(pt(a,x+1j*y)) for x in np.linspace(-1,1,7) for y in np.linspace(-1,1,7) if x*x+y*y<1.5])
  border=always_redraw(lambda:Circle(radius=(1.5*(1-shrink.get_value())+.27*shrink.get_value())*4/3.4,color=INPUT,stroke_width=2.3).move_to(pt(a,shrink.get_value()*w)))
  dot=always_redraw(lambda:Dot(pt(a,shrink.get_value()*w+(1.5*(1-shrink.get_value())+.27*shrink.get_value())*np.exp(1j*theta.get_value())),color=GOLD,radius=.05))
  self.show(a,field,border,Dot(pt(a,w),color=GOLD),label('각 점의 조건',x=3.5,y=1.7,size=30,color=OUTPUT),label('경계와 내부의 관계로',x=3.5,y=.5,size=30,color=INPUT),run_time=.5)
  self.to(24);self.play(FadeOut(field),run_time=.4);self.add(dot);self.play(theta.animate.set_value(TAU),run_time=2.3,rate_func=linear)
  self.to(27);self.play(shrink.animate.set_value(1),run_time=1.4)
  self.to(28.5);self.show(eq(r'f(w)=\frac{1}{2\pi i}\oint_\Gamma\frac{f(z)}{z-w}\,dz',x=3.5,y=-.8,size=32,width=7),label('코시 적분 공식',x=3.5,y=-1.9,size=28,color=GOLD),run_time=.5)
  self.note('원과 내부를 포함하는 열린 영역에서 정칙인 함수')
 def s04(self):
  left=TemperatureMesh(x=-3.5,size=1.65,morph=1);right=TemperatureMesh(x=3.5,size=1.65,morph=0)
  m=ValueTracker(1)
  boundary=always_redraw(lambda:heat_rim(-3.5,size=1.65,m=m.get_value()))
  grid=always_redraw(lambda:conformal_grid(-3.5,size=1.65,m=m.get_value()))
  self.show(left,right,boundary,grid,heat_rim(3.5,size=1.65),conformal_grid(3.5,size=1.65),label('형태가 복잡한 영역',x=-3.5,y=2.65,size=24),label('계산하기 쉬운 영역',x=3.5,y=2.65,size=24),run_time=.6)
  self.show(Arrow(p(.9,.9),p(-.9,.9),buff=0,color=GOLD),Arrow(p(-.9,-.2),p(.9,-.2),buff=0,color=INPUT),eq(r'F',y=1.45,size=29,color=GOLD),eq(r'F^{-1}',y=-.75,size=29,color=INPUT),run_time=.4)
  self.to(33);self.play(m.animate.set_value(0),UpdateFromAlphaFunc(left,lambda obj,a:obj.set_morph(1-a)),run_time=2.4,rate_func=smooth)
  self.to(36);self.play(m.animate.set_value(1),UpdateFromAlphaFunc(left,lambda obj,a:obj.set_morph(a)),run_time=1.8,rate_func=smooth)
  self.show(eq(r'\Delta T=0',x=-3.5,y=-1.9,size=34),eq(r'\Delta U=0',x=3.5,y=-1.9,size=34),run_time=.4);self.note('온도 정보와 격자를 함께 옮기는 실제 등각 변환')
 def s05(self):
  a,b=self.pair(1.5,3.3)
  self.show(Dot(pt(a,1),color=INPUT),Dot(pt(b,1),color=OUTPUT),Dot(pt(b,-1),color=OUTPUT),eq(r'z=1\qquad\longmapsto\qquad w=\pm1',y=2.5,size=34,color=GOLD),run_time=.4)
  self.to(41);self.wipe();g=sheets().scale(.72,about_point=ORIGIN).shift(p(-1.8,0));t=ValueTracker(0)
  self.show(g,label('두 겹의 공간을 교차 연결',x=3.4,y=1.2,size=29,width=6.4,color=OUTPUT),eq(r'w^2=z',x=3.4,y=-.1,size=42,color=GOLD),run_time=.4)
  self.add(always_redraw(lambda:Dot(.72*lifted_point(t.get_value())+p(-1.8,0),radius=.065,color=GOLD)))
  self.play(t.animate.set_value(TAU),run_time=2.8,rate_func=linear)
  self.to(45);self.wipe();angle=ValueTracker(-.3)
  def saddle():
   mesh=VGroup()
   for v in np.linspace(-1.2,1.2,11):
    for swap,c in [(False,INPUT),(True,OUTPUT)]:
     points=[]
     for u in np.linspace(-1.2,1.2,35):
      X,Y=(v,u) if swap else (u,v)
      points.append(project((X,Y,.45*(X*X-Y*Y)),-3.4,.4,1.2,angle.get_value()))
     mesh.add(poly(points,c,1.2,.75))
   return mesh
  self.show(always_redraw(saddle),eq(r'S=\{(z,w)\in\mathbb C^2:z=w^2\}',x=3.4,y=.2,size=32,width=6.8),label('리만 곡면',x=3.4,y=1.5,size=34,color=OUTPUT),run_time=.4)
  self.note('두 겹의 연결 개념도에서, w 좌표를 이용한 매끄러운 3D 표현으로')
  self.play(angle.animate.set_value(.3),run_time=1.8,rate_func=linear)
 def s06(self):
  self.show(sphere(-4.8,1.65,.55),torus(0,1.65,.42),Circle(radius=.55,color=OUTPUT).move_to(p(4.8,1.65)),Circle(radius=.045,color=OUTPUT).move_to(p(4.8,1.65)),label('구면',x=-4.8,y=.85,size=20),label('원환면',y=.85,size=20),label('점이 빠진 원판',x=4.8,y=.85,size=20),run_time=.4)
  arrows=VGroup(*[Arrow(p(x,.5),p(x,-.1),buff=0,color=GOLD,stroke_width=1.8) for x in [-4.8,0,4.8]])
  self.play(Create(arrows),run_time=1)
  self.show(sphere(-4.8,-1,.8),plane(1.5,1.7,0,-1),Circle(radius=.85,color=OUTPUT).move_to(p(4.8,-1)),label('리만 구면',x=-4.8,y=-2.05,size=25,color=INPUT),label('복소평면',y=-2.05,size=25),label('단위원판',x=4.8,y=-2.05,size=25,color=OUTPUT),run_time=.5)
  self.note('균일화 정리 · 분류하는 대상은 각 리만 곡면의 보편피복공간')
  self.to(52);self.show(eq(r'\widehat{\mathbb C},\quad\mathbb C,\quad\mathbb D',y=2.65,size=30,color=GOLD),run_time=.4)
 def s07(self):
  a=ValueTracker(0)
  self.show(rim(-3.5,R=1.9),always_redraw(lambda:hcircle(a.get_value(),.16,x=-3.5,R=1.9)),eq(r'|T_a\prime(0)|=1-|a|^2',x=3.5,y=1.4,size=36,color=GOLD,width=6.6),label('복소미분 → 길이의 변화',x=3.5,y=.25,size=27,color=OUTPUT,width=6.6),run_time=.5)
  self.to(56);self.play(a.animate.set_value(.85),run_time=1.6,rate_func=smooth)
  self.to(58);self.show(eq(r'ds=\frac{2|dz|}{1-|z|^2}',x=3.5,y=-1.25,size=40,color=OUTPUT,width=6.6),run_time=.4);self.note('표준 정규화 · 새로운 길이 측정의 규칙')
  self.to(60);self.wipe();self.show(rim(-3.5,R=1.9),rim(3.5,R=1.9),label('새로운 거리의 눈금',x=-3.5,y=-2.05,size=25,color=GOLD),label('쌍곡평면',x=3.5,y=-2.05,size=25,color=OUTPUT),run_time=.4)
  self.play(Create(rings(-3.5,R=1.9)),run_time=2)
  self.to(63);self.show(DiskPattern(x=3.5,R=1.9),run_time=.7)
 def s08(self):
  border=rim(R=1.9);pattern=DiskPattern(R=1.9,observer=.24)
  self.add(border,pattern)
  self.play(FadeOut(pattern),FadeOut(border),run_time=.5)
  a=plane(2.5,4.7);self.show(a,run_time=.4)
  self.to(67.3);self.play(FadeOut(a.background_lines),FadeOut(a.y_axis),run_time=.7)
  self.remove(a);self.add(a.x_axis)
  self.to(68);self.show(Dot(pt(a,1),color=INPUT),label('실수',x=3,y=.2,size=25,color=INPUT),run_time=.2)
