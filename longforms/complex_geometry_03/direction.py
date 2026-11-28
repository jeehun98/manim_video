"""Part 03: continuous lifts, local coordinates and actual Cayley transformations."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from longforms.complex_geometry_01.direction import GeometryScene,plane,pt,vec,curve,eq,label,p,INPUT,OUTPUT,GOLD,RED,INK,MUTED
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
assets=HERE.parents[1]/'media'/'complex_geometry_03_assets'/os.getenv('CG_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex');config.text_dir=str(assets/'texts')

def poly(points,color=INPUT,width=1.3,opacity=1):
 return VMobject().set_points_as_corners(points).set_stroke(color,width,opacity=opacity)

def project(q,x=0,y=.3,scale=1,angle=.18):
 X,Y,Z=q;c=np.cos(angle);s=np.sin(angle);X,Y=c*X-s*Y,s*X+c*Y
 return p(x+scale*(.9*X-.38*Y),y+scale*(.28*X+.48*Y+.82*Z))

def torus_q(u,v):
 return np.array([(1.5+.48*np.cos(v))*np.cos(u),(1.5+.48*np.cos(v))*np.sin(u),.48*np.sin(v)])

def torus(x=0,y=.35,scale=1,angle=.18):
 g=VGroup()
 for u in np.linspace(0,TAU,20,endpoint=False):
  g.add(poly([project(torus_q(u,v),x,y,scale,angle) for v in np.linspace(0,TAU,70)],INPUT,1,.45))
 for v in np.linspace(0,TAU,10,endpoint=False):
  g.add(poly([project(torus_q(u,v),x,y,scale,angle) for u in np.linspace(0,TAU,100)],INPUT,1,.55))
 return g

def sphere(x=0,y=.5,r=1.4,color=INPUT):
 g=VGroup(Circle(radius=r,color=color,stroke_width=2).move_to(p(x,y)))
 for h in [-.55,0,.55]:
  g.add(Ellipse(width=2*r*np.sqrt(1-h*h),height=.35*r*np.sqrt(1-h*h),color=color,stroke_width=1,stroke_opacity=.5).move_to(p(x,y+h*r)))
 for w in [.65,1.25]:g.add(Ellipse(width=w*r,height=2*r,color=color,stroke_width=1,stroke_opacity=.5).move_to(p(x,y)))
 return g

def sheet_point(z,k):return p(-2+1.7*z.real+.7*z.imag,1.45-2.2*k+.55*z.imag)
def sheets():
 g=VGroup()
 for k,c in [(0,INPUT),(1,OUTPUT)]:
  corners=[sheet_point(complex(a,b),k) for a,b in [(-1.4,-1.4),(1.4,-1.4),(1.4,1.4),(-1.4,1.4)]]
  g.add(Polygon(*corners,color=c,stroke_width=1.5,fill_color=c,fill_opacity=.045))
  for v in np.linspace(-1.4,1.4,7):
   g.add(Line(sheet_point(complex(v,-1.4),k),sheet_point(complex(v,1.4),k),color=c,stroke_width=.8,stroke_opacity=.3))
   g.add(Line(sheet_point(complex(-1.4,v),k),sheet_point(complex(1.4,v),k),color=c,stroke_width=.8,stroke_opacity=.3))
  for side,col in [(.05,GOLD),(-.05,'#BD93DF')]:
   g.add(Line(sheet_point(-1.4,k)+UP*side,sheet_point(0,k)+UP*side,color=col,stroke_width=3))
  g.add(Dot(sheet_point(0,k),radius=.045,color=RED),Dot(sheet_point(1,k),radius=.07,color=c))
 for side,col in [(.05,GOLD),(-.05,'#BD93DF')]:
  a=sheet_point(-.8,0)+UP*side;b=sheet_point(-.8,1)-UP*side;s=1 if side>0 else -1
  connection=CubicBezier(a,a+RIGHT*.8*s+DOWN*.6,b+LEFT*.8*s+UP*.6,b,color=col,stroke_width=2)
  g.add(DashedVMobject(connection,num_dashes=20))
 return g

def lifted_point(t):
 # Negative-real-axis cut: sheet changes at pi and 3pi, endpoints compared at 2pi and 4pi.
 k=0 if t<PI else 1 if t<3*PI else 0
 for cut,before,after in [(PI,0,1),(3*PI,1,0)]:
  if abs(t-cut)<.13:
   a=(t-cut+.13)/.26;k=before+(after-before)*smooth(a)
 return sheet_point(np.exp(1j*t),k)

def tile_grid(x=3.4,y=.35,unit=1.05):
 g=VGroup()
 for k in range(-2,4):
  g.add(Line(p(x+unit*k,y-2*unit),p(x+unit*k,y+2*unit),color=MUTED,stroke_width=1,stroke_opacity=.6))
 for k in range(-2,3):g.add(Line(p(x-2*unit,y+unit*k),p(x+3*unit,y+unit*k),color=MUTED,stroke_width=1,stroke_opacity=.6))
 g.add(Rectangle(width=unit,height=unit,stroke_color=GOLD,stroke_width=2,fill_color=GOLD,fill_opacity=.06).move_to(p(x+unit/2,y+unit/2)))
 return g

def clip_segment(a,b,rect):
 xmin,xmax,ymin,ymax=rect;d=b-a;t0,t1=0.,1.
 for q,r in [(-d[0],a[0]-xmin),(d[0],xmax-a[0]),(-d[1],a[1]-ymin),(d[1],ymax-a[1])]:
  if abs(q)<1e-12:
   if r<0:return None
  else:
   t=r/q
   if q<0:t0=max(t0,t)
   else:t1=min(t1,t)
   if t0>t1:return None
 return a+t0*d,a+t1*d

def clipped_curve(zs,fn,origin,scale,rect,color,width=1.4):
 values=fn(np.asarray(zs,dtype=complex));points=np.array([origin+scale*p(z.real,z.imag) for z in values])
 g=VGroup();run=[]
 for a,b in zip(points,points[1:]):
  segment=clip_segment(a,b,rect)
  if segment is None:
   if len(run)>1:g.add(poly(run,color,width))
   run=[]
  else:
   a,b=segment
   if run and np.linalg.norm(run[-1]-a)>1e-5:
    if len(run)>1:g.add(poly(run,color,width))
    run=[]
   if not run:run=[a]
   run.append(b)
 if len(run)>1:g.add(poly(run,color,width))
 return g

def cayley_grid(t,x=0,y=-1.55,scale=1.05,rect=(-6.8,6.8,-1.6,1.9),border=True):
 fn=lambda z:1j*(1+z)/(1-t*z)
 g=VGroup()
 for v in [-.8,-.55,-.3,0,.3,.55,.8]:
  extent=np.sqrt(1-v*v)*.999;ts=np.linspace(-extent,extent,150)
  g.add(clipped_curve(ts+1j*v,fn,p(x,y),scale,rect,OUTPUT,1.25))
  g.add(clipped_curve(v+1j*ts,fn,p(x,y),scale,rect,INPUT,1.25))
 if border:
  # z=1 is excluded at the final pole. No artificial line bridges the infinity.
  zs=np.exp(1j*np.linspace(.0005,TAU-.0005,650))
  g.add(clipped_curve(zs,fn,p(x,y),scale,rect,GOLD,2))
 return g

class SurfaceScene(GeometryScene):
 data=DATA
 def s01(self):
  # Brief planar-domain reference specified by the supplied opening narration.
  a=plane(1.8,3.3,-3.5,.4);b=plane(1.8,3.3,3.5,.4)
  left=curve(a,lambda t:np.exp(1j*t)+.25*np.exp(2j*t),INPUT);right=curve(b,lambda t:np.exp(1j*t),OUTPUT)
  self.show(a,b,left,right,Arrow(p(-.9,.4),p(.9,.4),buff=0,color=GOLD),eq(r'F^{-1}',y=1.1,size=30,color=GOLD))
  self.to(3);self.wipe();self.show(eq(r'w^2=z',y=1.4,size=58),label('평면 하나로 충분할까?',y=-.2,size=32,color=GOLD))
  self.to(8);self.wipe();a,b=self.pair(1.4,3.8)
  self.show(curve(a,lambda t:np.exp(1j*t),INPUT),curve(b,lambda t:np.exp(1j*t),OUTPUT),Dot(pt(a,1),color=INPUT),Dot(pt(b,1),color=OUTPUT),label('입력 z',x=-3.5,y=-1.95,color=INPUT),label('제곱근 w',x=3.5,y=-1.95,color=OUTPUT),eq(r'w^2=z',y=2.65,size=30),run_time=.5)
 def s02(self):
  a,b=self.pair(1.4,3.8);theta=ValueTracker(0)
  self.show(curve(a,lambda t:np.exp(1j*t),INPUT),curve(b,lambda t:np.exp(1j*t),OUTPUT),label('입력 z',x=-3.5,y=-1.95,color=INPUT),label('연속적으로 선택한 제곱근 w',x=3.5,y=-1.95,size=25,color=OUTPUT))
  for ax,f,c in [(a,lambda:theta.get_value(),INPUT),(b,lambda:theta.get_value()/2,OUTPUT)]:
   self.add(always_redraw(lambda ax=ax,f=f,c=c:VGroup(vec(ax,np.exp(1j*f()),c),Dot(pt(ax,np.exp(1j*f())),color=c,radius=.075))))
  initial=eq(r'z=1\qquad w=1',y=-2.35,size=26,color=GOLD)
  self.show(eq(r'z=e^{i\theta}\qquad w=e^{i\theta/2}',y=2.65,size=31),initial,run_time=.4)
  self.to(15);self.remove(initial);self.play(theta.animate.set_value(PI/3),run_time=4.5,rate_func=linear)
  self.to(20);self.play(theta.animate.set_value(PI/2),run_time=2,rate_func=linear)
  self.show(label('90°',x=-1.1,y=1.7,size=27,color=GOLD),label('45°',x=5.7,y=1.7,size=27,color=GOLD),run_time=.4)
 def s03(self):
  a,b=self.pair(1.4,3.8)
  self.show(vec(a,np.exp(PI*.25j),OUTPUT),vec(b,1j,INPUT),curve(a,lambda t:np.exp(1j*t),MUTED),curve(b,lambda t:np.exp(1j*t),MUTED),eq(r'w\longmapsto w^2',y=2.65,size=35,color=GOLD),eq(r'(e^{i\varphi})^2=e^{2i\varphi}\quad\Longrightarrow\quad\varphi=\theta/2',y=-1.95,size=33),label('45°',x=-2.1,y=1,size=26,color=OUTPUT),label('90°',x=4.9,y=1,size=26,color=INPUT))
  self.to(27.6);self.wipe();a,b=self.pair(1.4,3.8);theta=ValueTracker(PI/2)
  self.show(curve(a,lambda t:np.exp(1j*t),INPUT),curve(b,lambda t:np.exp(1j*t),OUTPUT),eq(r'z=e^{i\theta}\qquad w=e^{i\theta/2}',y=2.65,size=31),run_time=.4)
  for ax,f,c in [(a,lambda:theta.get_value(),INPUT),(b,lambda:theta.get_value()/2,OUTPUT)]:
   self.add(always_redraw(lambda ax=ax,f=f,c=c:VGroup(vec(ax,np.exp(1j*f()),c),Dot(pt(ax,np.exp(1j*f())),radius=.075,color=c))))
  self.to(29);self.play(theta.animate.set_value(TAU),run_time=5.4,rate_func=linear)
  status=eq(r'\theta=360^\circ:\quad z=1,\quad w=-1',y=-1.95,size=33,color=GOLD);self.show(status,run_time=.5)
  self.to(35);self.note('입력은 돌아왔지만, 따라간 제곱근은 다른 값')
  self.to(40.5);self.remove(self.footnote);self.play(theta.animate.set_value(2*TAU),run_time=2.8,rate_func=linear)
  self.play(Transform(status,eq(r'\theta=720^\circ:\quad z=1,\quad w=1',y=-1.95,size=33,color=OUTPUT)),run_time=.4)
 def s04(self):
  flat=sheets();upper=VGroup(*flat[:19]);lower=VGroup(*flat[19:38]);connections=VGroup(*flat[38:])
  self.show(upper,eq(r'z=1',x=3.9,y=1.6,size=33,color=INPUT),label('첫 번째 겹',x=-5.6,y=2.65,size=24,color=INPUT))
  self.to(49.5);self.show(label('절단선: 음의 실수축',x=3.9,y=.5,size=25,color=MUTED,width=4.7),run_time=.5)
  self.to(50);self.show(lower,eq(r'z=1',x=3.9,y=-.6,size=33,color=OUTPUT),label('두 번째 겹',x=-5.6,y=-1.85,size=24,color=OUTPUT),run_time=1)
  self.play(Create(connections),run_time=1.5)
  self.show(label('위쪽 가장자리 ↔ 다른 겹의 아래쪽',x=3.8,y=-1.5,size=23,width=5.8,color=GOLD))
  self.to(55);self.show(DashedLine(sheet_point(1,0),sheet_point(1,1),color=MUTED,dash_length=.08),run_time=.6)
  self.note('같은 복소좌표 · 서로 다른 위치  |  겹과 연결 규칙의 3차원 개념도')
 def s05(self):
  self.show(sheets(),eq(r'z=1,\quad w=1',x=3.9,y=1.5,size=33,color=INPUT),eq(r'z=1,\quad w=-1',x=3.9,y=-.7,size=33,color=OUTPUT))
  t=ValueTracker(0);dot=always_redraw(lambda:Dot(lifted_point(t.get_value()),radius=.09,color=GOLD));self.add(dot)
  self.to(66.5)
  path=poly([lifted_point(t) for t in np.linspace(0,2*PI,110)],GOLD,2)
  self.play(t.animate.set_value(2*PI),Create(path),run_time=2.2,rate_func=linear)
  path2=poly([lifted_point(t) for t in np.linspace(2*PI,4*PI,110)],GOLD,2)
  self.to(69);self.play(t.animate.set_value(4*PI),Create(path2),run_time=3.2,rate_func=linear)
  self.show(eq(r'0\ \longrightarrow\ 2\pi\ \longrightarrow\ 4\pi',y=2.65,size=31,color=GOLD),run_time=.5)
  self.to(73);self.note('1바퀴: 다른 겹  ·  2바퀴: 처음 위치와 처음 값')
 def s06(self):
  a,b=self.pair(1.5,3.8);w=.7+.7j
  self.show(vec(a,w,INPUT),vec(a,-w,OUTPUT),Dot(pt(a,w),color=INPUT),Dot(pt(a,-w),color=OUTPUT),vec(b,w*w,GOLD),Dot(pt(b,w*w),radius=.09,color=GOLD),eq(r'z=w^2=(-w)^2',y=2.65,size=35),label('새 공간의 좌표 w',x=-3.5,y=-1.95,color=INPUT),label('입력 평면으로의 투영 z',x=3.5,y=-1.95,size=25,color=GOLD))
  self.to(82);self.wipe()
  angle=ValueTracker(-.35)
  def saddle():
   g=VGroup()
   for v in np.linspace(-1.25,1.25,13):
    for swap,c in [(False,INPUT),(True,OUTPUT)]:
     points=[]
     for u in np.linspace(-1.25,1.25,42):
      X,Y=(v,u) if swap else (u,v)
      points.append(project((X,Y,.45*(X*X-Y*Y)),x=-3.35,y=.55,scale=1.2,angle=angle.get_value()))
     g.add(poly(points,c,1.2,.7))
   return g
  mesh=always_redraw(saddle);self.show(mesh,Dot(p(-3.35,.55),color=GOLD),eq(r'w=u+iv',x=3.4,y=1.85,size=36),eq(r'z=w^2',x=3.4,y=.9,size=42,color=GOLD),eq(r'(u,v)\mapsto(u,v,u^2-v^2)',x=3.4,y=-.1,size=30,width=6.8),label('w = 0 주변도 매끄럽다',x=3.4,y=-1.15,size=28,color=OUTPUT))
  self.note('3D 표현의 높이 ∝ Re(w²)  ·  실제 공간 S ⊂ ℂ²의 w 좌표를 이용한 시각화')
  self.play(angle.animate.set_value(.4),run_time=7,rate_func=linear)
  self.to(91);self.wipe();self.show(eq(r'S=\{(z,w)\in\mathbb C^2:z=w^2\}',y=2.15,size=38),eq(r'F:S\longrightarrow\mathbb C,\qquad F(z,w)=w',y=.85,size=39,color=OUTPUT),label('각 위치에 하나의 값',y=-.2,size=32,color=OUTPUT),eq(r'w\ \text{coordinate}:\qquad F(w)=w',y=-1.25,size=36,color=GOLD))
  self.to(98);self.note('함수의 규칙을 바꾸는 대신, 함수가 정의되는 공간을 바꾼다')
 def s07(self):
  globe=sphere(-3.7,.55,1.65);self.show(globe)
  U=Ellipse(width=2.1,height=1.7,color=INPUT,fill_color=INPUT,fill_opacity=.15).move_to(p(-4.15,.9))
  V=Ellipse(width=2.1,height=1.7,color=OUTPUT,fill_color=OUTPUT,fill_opacity=.15).move_to(p(-3.25,.25))
  self.show(U,V,label('U',x=-4.6,y=1.35,color=INPUT),label('V',x=-2.8,y=-.1,color=OUTPUT),label('전체가 평면일 필요는 없다',x=3.3,y=1.6,size=30,width=6.5))
  self.to(110);a=plane(1.5,2.15,1.4,-.1);b=plane(1.5,2.15,5.2,-.1)
  self.show(a,b,eq(r'\varphi',x=1.4,y=1.3,size=30,color=INPUT),eq(r'\psi',x=5.2,y=1.3,size=30,color=OUTPUT),Arrow(p(2.7,-.1),p(3.9,-.1),buff=0,color=GOLD),eq(r'\psi\circ\varphi^{-1}',x=3.3,y=-1.5,size=31,color=GOLD))
  self.to(114);self.note('겹치는 좌표 사이의 변환이 가역 정칙 · 구면의 예: η = 1/ζ (ζ ≠ 0)')
  self.to(117);self.play(Transform(self.title,label('리만 곡면  ·  Riemann Surface',y=self.head_y,size=34)),run_time=.7)
  self.to(120);self.play(Indicate(U,color=GOLD),Indicate(V,color=GOLD),run_time=1.2)
  self.to(126);self.note('국소적인 복소좌표  →  공간 전체의 복소해석적 구조',OUTPUT)
 def s08(self):
  rect=Rectangle(width=3,height=2.5,color=MUTED).move_to(p(-4.6,.45))
  edges=VGroup(*[Line(p(-6.1,y),p(-3.1,y),color=GOLD,stroke_width=3) for y in [-.8,1.7]],*[Line(p(x,-.8),p(x,1.7),color=INPUT,stroke_width=3) for x in [-6.1,-3.1]])
  arrows=VGroup(*[Arrow(p(-4.95,y),p(-4.25,y),buff=0,color=GOLD,stroke_width=2) for y in [-.8,1.7]],*[Arrow(p(x,.05),p(x,.8),buff=0,color=INPUT,stroke_width=2) for x in [-6.1,-3.1]])
  self.show(rect,edges,arrows,label('직사각형',x=-4.6,y=-1.65,size=26))
  self.to(131)
  def rolled(alpha):
   g=VGroup()
   def q(u,v):
    flat=np.array([u/PI*1.15,0,1.2*v]);cyl=np.array([np.sin(u),-np.cos(u),1.2*v])
    return project((1-alpha)*flat+alpha*cyl,-.5,.45,1)
   for u in np.linspace(-PI,PI,20):g.add(poly([q(u,v) for v in np.linspace(-1,1,36)],INPUT,1,.6))
   for v in np.linspace(-1,1,10):g.add(poly([q(u,v) for u in np.linspace(-PI,PI,70)],GOLD if abs(v)>.99 else INPUT,1.5 if abs(v)>.99 else 1,.7))
   return g
  mesh=rolled(0);self.show(mesh);self.play(Transform(mesh,rolled(1)),run_time=1.7)
  self.show(label('원기둥',x=-.5,y=-1.65,size=26),run_time=.3);self.to(134)
  cylinder=mesh.copy();self.add(cylinder)
  self.play(Transform(mesh,torus(4.5,.5,1.05)),run_time=2.5)
  self.show(label('원환면',x=4.5,y=-1.65,size=26),run_time=.3);self.note('반대 변 연결의 위상적 3D 표현 · 복소구조는 평면의 평행이동 좌표로 부여')
  self.to(138);dot=Dot(p(-5.5,.4),color=GOLD);self.show(dot,run_time=.2);self.play(dot.animate.move_to(p(-3.12,.4)),run_time=1.4);self.remove(dot);dot.move_to(p(-6.08,.4));self.add(dot);self.play(dot.animate.move_to(p(-5.5,.4)),run_time=.7)
  self.to(143);self.wipe();grid=tile_grid(x=-1,y=.2,unit=1.05)
  self.show(Rectangle(width=1.05,height=1.05,color=GOLD).move_to(p(-.475,.725)),run_time=.4)
  self.to(146);self.play(Create(grid),run_time=3);self.show(label('같은 직사각형을 가로 · 세로로 반복',x=4.4,y=.8,size=28,width=4.2,color=OUTPUT),eq(r'\mathbb C/(\mathbb Z+i\mathbb Z)',x=4.4,y=-.45,size=30,width=4.5))
 def s09(self):
  x,y,unit=2.5,.15,1.1
  grid=VGroup(*[Line(p(x+unit*k,y-unit),p(x+unit*k,y+2*unit),color=MUTED,stroke_width=1,stroke_opacity=.6) for k in range(-2,4)],*[Line(p(x-2*unit,y+unit*k),p(x+3*unit,y+unit*k),color=MUTED,stroke_width=1,stroke_opacity=.6) for k in range(-1,3)],Rectangle(width=unit,height=unit,stroke_color=GOLD,stroke_width=2,fill_color=GOLD,fill_opacity=.06).move_to(p(x+unit/2,y+unit/2)))
  self.show(torus(-3.8,.45,1.25),grid,label('원환면',x=-3.8,y=2.75,color=INPUT),label('펼쳐진 복소평면',x=3.1,y=2.75,color=OUTPUT))
  t=ValueTracker(0);v=ValueTracker(0)
  pos=lambda:project(torus_q(TAU*t.get_value(),TAU*v.get_value()),-3.8,.45,1.25)
  self.add(always_redraw(lambda:Dot(pos(),color=GOLD,radius=.085)),always_redraw(lambda:Dot(p(x+unit*t.get_value(),y+unit*v.get_value()),color=GOLD,radius=.085)))
  self.show(Dot(p(x,y),color=INK,radius=.045),run_time=.2)
  loop=poly([project(torus_q(u,0),-3.8,.45,1.25) for u in np.linspace(0,TAU,120)],GOLD,2.4)
  self.play(t.animate.set_value(1),Create(loop),run_time=3.1,rate_func=linear)
  status=eq(r'(0,0)\to(1,0)',x=3.2,y=-1.7,size=30,color=OUTPUT)
  horizontal=Arrow(p(x,y),p(x+unit,y),buff=0,color=INPUT)
  self.to(157);self.show(horizontal,status,run_time=.5)
  self.to(160);self.play(t.animate.set_value(2),Transform(horizontal,Arrow(p(x,y),p(x+2*unit,y),buff=0,color=INPUT)),Transform(status,eq(r'(0,0)\to(2,0)',x=3.2,y=-1.7,size=30,color=OUTPUT)),run_time=3,rate_func=linear)
  self.to(166);self.note('두 겹의 구분에서, 무한히 많은 복사본의 구분으로')
  loop2=poly([project(torus_q(0,u),-3.8,.45,1.25) for u in np.linspace(0,TAU,100)],OUTPUT,2.4)
  self.to(170);self.play(v.animate.set_value(2),Create(loop2),Transform(status,eq(r'(0,0)\to(2,2)',x=3.2,y=-1.7,size=30,color=OUTPUT)),run_time=3.2,rate_func=linear)
  self.show(Arrow(p(x+2*unit,y),p(x+2*unit,y+2*unit),buff=0,color=GOLD),eq(r'(m,n)=(2,2)',x=-3.8,y=-1.9,size=32,color=GOLD),run_time=.5)
  self.to(175);self.note('보편피복공간 ℂ  ·  이동 (m,n)은 두 방향으로 감은 횟수',OUTPUT)
 def s10(self):
  self.show(sphere(-4.8,.6,1),torus(0,.6,.85),Circle(radius=1,color=OUTPUT).move_to(p(4.8,.6)),label('각 공간을 펼치면?',y=-1.25,size=31,color=GOLD))
  self.to(182);self.wipe();self.show(label('무엇을 같은 공간으로 볼까?',y=.8,size=40,color=GOLD))
  self.to(187);self.wipe()
  disk=Circle(radius=1.65,color=INPUT,fill_color=INPUT,fill_opacity=.04).move_to(p(-3.8,.35))
  half=Rectangle(width=4.8,height=3.15,stroke_width=0,fill_color=OUTPUT,fill_opacity=.04).move_to(p(3.6,.65))
  self.show(disk,half,Line(p(1.2,-.925),p(6,-.925),color=MUTED),Arrow(p(3.6,-.925),p(3.6,2.35),buff=0,color=MUTED),label('단위원판 𝔻',x=-3.8,y=-1.95,size=28,color=INPUT),label('위쪽 반평면 ℍ',x=3.6,y=-1.95,size=28,color=OUTPUT),Dot(p(-3.8,.35),color=GOLD),Dot(p(3.6,.125),color=GOLD),eq(r'0\longleftrightarrow i',y=2.6,size=30,color=GOLD))
  self.to(190);self.note('겉모양과 크기가 달라도, 가역 정칙변환으로 비교한다')
 def s11(self):
  t=ValueTracker(0);mesh=always_redraw(lambda:cayley_grid(t.get_value()))
  self.show(mesh,Line(p(-6.8,-1.55),p(6.8,-1.55),color=MUTED,stroke_width=1),Dot(p(0,-.5),color=GOLD),eq(r'F_t(z)=i\frac{1+z}{1-tz},\quad 0\leq t\leq1',y=2.4,size=31),run_time=.5)
  self.show(label('고정된 좌표계의 유한 창 · 경계의 z=1은 t=1에서 무한대로',y=-2.2,size=22,color=MUTED),run_time=.3)
  self.play(t.animate.set_value(1),run_time=4,rate_func=smooth)
  self.to(199);self.wipe()
  a,b=self.pair(1.6,3.6);self.show(Circle(radius=1.125,color=INPUT).move_to(pt(a,0)),eq(r'F(z)=i\frac{1+z}{1-z}',y=2.35,size=34,color=GOLD),eq(r'F^{-1}(\zeta)=\frac{\zeta-i}{\zeta+i}',y=-1.65,size=31,color=OUTPUT),Dot(pt(a,0),color=GOLD),Dot(pt(b,1j),color=GOLD),run_time=.5)
  # Orthogonal input vectors and their exact differential images, F'(0)=2i.
  self.show(vec(a,.5,INPUT),vec(a,.5j,OUTPUT),vec(b,1j,INPUT,base=1j),vec(b,-1,OUTPUT,base=1j),eq(r'F\prime(0)=2i',y=.1,size=29,width=2.8,color=GOLD),run_time=.5)
  self.to(202);self.note('작은 변화: 2배 확대 + 90° 회전 · 교차각 보존')
  self.to(205);self.note('가역 정칙변환  ⇔  같은 복소해석적 유형',OUTPUT)
 def s12(self):
  # Precisely classified known examples, without mistaking topology for complex equivalence.
  tops=VGroup(sphere(-4.8,1.9,.62),torus(0,1.9,.45),Circle(radius=.62,color=OUTPUT).move_to(p(4.8,1.9)),Circle(radius=.05,color=OUTPUT).move_to(p(4.8,1.9)))
  self.show(tops,label('구면',x=-4.8,y=1.02,size=21),label('원환면',y=1.02,size=21),label('점이 빠진 원판',x=4.8,y=1.02,size=21))
  for x in [-4.8,0,4.8]:self.show(Arrow(p(x,.65),p(x,-.05),buff=0,color=MUTED,stroke_width=1.5),run_time=.2)
  self.show(label('보편피복',x=2.3,y=.4,size=21,color=GOLD))
  s=sphere(-4.8,-.95,1);a=plane(1.5,2.05,0,-.95);d=Circle(radius=1.03,color=OUTPUT,fill_color=OUTPUT,fill_opacity=.035).move_to(p(4.8,-.95))
  self.to(213.5);self.show(s,a,d,label('리만 구면',x=-4.8,y=-2.25,size=26,color=INPUT),label('복소평면',y=-2.25,size=26),label('단위원판',x=4.8,y=-2.25,size=26,color=OUTPUT),run_time=.5)
  self.to(214);self.play(Indicate(s,color=GOLD),run_time=.7);self.play(Indicate(a,color=GOLD),run_time=.7);self.play(Indicate(d,color=GOLD),run_time=.7)
  self.to(217.5);self.play(Transform(self.title,label('균일화 정리  ·  Uniformization Theorem',y=self.head_y,size=34)),run_time=.5)
  self.add(Dot(p(4.8,-.95),color=GOLD,radius=.05))
