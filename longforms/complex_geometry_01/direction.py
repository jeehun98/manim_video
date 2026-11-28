"""Part 01: exact narration, native landscape, arithmetic-driven vector animation."""
import os
os.environ['QCS_LAYOUT']='longform'
import json
from pathlib import Path
import numpy as np
from manim import *
import longforms.qcs01_speed.direction as shared
from quantum_series.shared.theme import text
from longforms.qcs01_speed.direction import QCSScene
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
shared.FPS=30
config.frame_rate=30
config.background_color='#101722'
assets=HERE.parents[1]/'media'/'complex_geometry_01_assets'/os.getenv('CG_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex');config.text_dir=str(assets/'texts')
INK,INPUT,OUTPUT,GOLD,RED,MUTED='#E5E7EB','#58C4DD','#83C167','#FFCC66','#F87171','#8D9BB0'
def p(x,y):return np.array([x,y,0.])
def label(s,x=0,y=0,size=27,color=INK,width=13.8):return text(s,x,y,size,color,width)
def eq(s,x=0,y=0,size=35,color=INK,width=13.6):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to(p(x,y))
def plane(r=2,size=4.4,x=0,y=.3):
 return NumberPlane(x_range=[-r,r,1],y_range=[-r,r,1],x_length=size,y_length=size,
  background_line_style={'stroke_color':'#324255','stroke_width':1,'stroke_opacity':.62},
  axis_config={'stroke_color':MUTED,'stroke_width':1.3,'include_ticks':False,'include_tip':False}).move_to(p(x,y))
def pt(a,z):return a.c2p(complex(z).real,complex(z).imag)
def vec(a,z,c=INPUT,base=0,width=3):
 if abs(z)<1e-7:z=1e-7+0j
 return Arrow(pt(a,base),pt(a,base+z),buff=0,color=c,stroke_width=width,max_tip_length_to_length_ratio=.2)
def curve(a,fn,c=OUTPUT):return ParametricFunction(lambda t:pt(a,fn(t)),t_range=[0,TAU,.035],color=c,stroke_width=3)
def chain(values,x=0,y=.3,scale=1,c=OUTPUT):
 g=VGroup();z=0j
 for v in values:
  if abs(v)>1e-8:g.add(Arrow(p(x+scale*z.real,y+scale*z.imag),p(x+scale*(z+v).real,y+scale*(z+v).imag),buff=0,color=c,stroke_width=2,max_tip_length_to_length_ratio=.28))
  z+=v
 return g
def circle_samples(a,fn,c=OUTPUT):
 return VGroup(curve(a,fn,c),*[Dot(pt(a,fn(t)),radius=.04,color=GOLD if j==0 else c) for j,t in enumerate(np.linspace(0,TAU,16,endpoint=False))])

class GeometryScene(QCSScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.brand=label('복소평면에 숨겨진 기하학',y=4.02,size=18,color=MUTED);self.add(self.brand)
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for m in self.mobjects:
   if m is getattr(self,'caption',None) or m is getattr(self,'caption_panel',None):continue
   if m.width<.001 or m.height<.001:continue
   assert m.get_left()[0]>=-7.88 and m.get_right()[0]<=7.88,('horizontal',self.shot,self.time,m)
   assert m.get_bottom()[1]>=-2.6 and m.get_top()[1]<=4.4,('vertical',self.shot,self.time,m)
 def wipe(self):
  keep=[self.title,self.caption,self.caption_panel,self.brand]
  obs=[m for m in self.mobjects if all(m is not k for k in keep) and m.get_center()[1]<2.85]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def pair(self,r=2,size=4.2):
  a=plane(r,size,-3.5,.3);b=plane(r,size,3.5,.3);self.show(a,b)
  return a,b
 def s01(self):
  a=plane(2.5,4.7);d=Dot(pt(a,1),color=INPUT);v=vec(a,1)
  self.show(a.x_axis,d,label('실수',x=3,y=.2,size=25,color=INPUT),run_time=.4)
  self.to(1.5);self.play(Create(a.y_axis),FadeIn(a.background_lines),GrowArrow(v),run_time=1)
  self.to(4);self.play(Rotate(v,PI/2,about_point=pt(a,0)),d.animate.move_to(pt(a,1j)),run_time=2)
  self.show(Arc(radius=.75,angle=PI/2,arc_center=pt(a,0),color=GOLD),eq(r'z\mapsto iz',x=4.7,y=1.1,color=INPUT),label('90° 회전',x=4.7,y=.1,color=GOLD))
  self.to(9);self.play(Rotate(v,-PI/2,about_point=pt(a,0)),d.animate.move_to(pt(a,1)),run_time=.6)
  self.play(Transform(v,vec(a,1.6*np.exp(.65j),OUTPUT)),d.animate.move_to(pt(a,1.6*np.exp(.65j))).set_color(OUTPUT),run_time=2.2)
  self.show(eq(r'z\mapsto az',x=-4.8,y=1,size=35,color=OUTPUT),label('같은 회전 · 같은 배율',x=-4.8,y=-.2,size=25,color=OUTPUT));self.note('복소수 곱셈을 공간의 움직임으로')
  self.to(16);self.show(eq(r'\Delta z\ \longmapsto\ \Delta f',y=-1.95,size=34,color=GOLD))
 def s02(self):
  a,b=self.pair(3);z=1+1j;h=.3+.1j
  self.show(Dot(pt(a,z),color=GOLD),Dot(pt(b,z*z),color=GOLD),vec(a,h,INPUT,base=z),vec(b,(z+h)**2-z*z,OUTPUT,base=z*z))
  self.show(eq(r'f(z)=z^2',y=2.6,size=31),label('입력의 변화',x=-3.5,y=-1.95,color=INPUT),label('출력의 변화',x=3.5,y=-1.95,color=OUTPUT))
  self.to(25);self.wipe();a=plane(2,4.3,x=-3.5);b=plane(2,4.3,x=3.5)
  self.show(a.x_axis,Dot(pt(a,0),color=GOLD),label('실수에서의 접근',x=-3.5,y=-1.95,size=25))
  ds=VGroup(Dot(pt(a,-1.5),color=INPUT),Dot(pt(a,1.5),color=INPUT));self.show(ds,run_time=.3);self.play(*[q.animate.move_to(pt(a,0)) for q in ds],run_time=1.2)
  self.to(28);self.show(b,Dot(pt(b,0),color=GOLD),label('복소평면에서의 접근',x=3.5,y=-1.95,size=25),run_time=.3)
  arrows=VGroup(*[Arrow(pt(b,1.6*np.exp(1j*t)),pt(b,.16*np.exp(1j*t)),buff=0,color=INPUT,stroke_width=2) for t in np.linspace(0,TAU,8,endpoint=False)])
  paths=VGroup(*[ParametricFunction(lambda t,sg=sg:pt(b,(1.65-t)*np.exp(sg*2j*t)),t_range=[0,1.62,.025],color=OUTPUT) for sg in [-1,1]])
  self.play(LaggedStart(*[GrowArrow(v) for v in arrows],lag_ratio=.1),Create(paths),run_time=2)
  self.to(34);self.wipe();a,b=self.pair(3);center=2+2j
  # Both planes retain actual complex coordinates; quotient limit is 2+2i.
  self.show(eq(r'\frac{(z_0+h)^2-z_0^2}{h}=2z_0+h,\quad z_0=1+i',y=2.35,size=31),label('입력 변화량 h',x=-3.5,y=-1.95,color=INPUT),label('차분비 → 2+2i',x=3.5,y=-1.95,color=OUTPUT))
  dots=VGroup(*[Dot(pt(b,center+.6*np.exp(1j*t)),radius=.05,color=OUTPUT) for t in np.linspace(0,TAU,8,endpoint=False)])
  ins=VGroup(*[Dot(pt(a,.6*np.exp(1j*t)),radius=.05,color=INPUT) for t in np.linspace(0,TAU,8,endpoint=False)])
  self.show(ins,dots,Dot(pt(b,center),color=GOLD,radius=.07),run_time=.3)
  self.play(*[q.animate.move_to(pt(a,0)) for q in ins],*[q.animate.move_to(pt(b,center)) for q in dots],run_time=2.5)
  self.note('방향과 경로에 관계없이 같은 극한')
 def s03(self):
  a,b=self.pair(3,4.2)
  left=circle_samples(a,lambda t:.6*np.exp(1j*t),INPUT);right=circle_samples(b,lambda t:.6*np.exp(1j*t),INPUT)
  self.show(left,right,label('방향마다 다른 확대',x=-3.5,y=2.65,size=26),label('복소수 곱셈',x=3.5,y=2.65,size=26))
  self.to(44);self.play(Indicate(left,color=GOLD),Indicate(right,color=GOLD),run_time=1)
  self.to(49);self.play(Transform(left,circle_samples(a,lambda t:1.2*np.cos(t)+1.8j*np.sin(t),RED)),run_time=3)
  self.show(eq(r'(x,y)\mapsto(2x,3y)',x=-3.5,y=-1.95,size=28,color=RED),run_time=.4)
  self.to(54);self.note('가로 ×2 · 세로 ×3 → 타원',RED)
  self.to(56);target=circle_samples(b,lambda t:1.8*np.exp(1j*(t+.65)),OUTPUT)
  marker=vec(b,.6,INPUT);self.add(marker)
  self.play(Transform(right,target),Transform(marker,vec(b,1.8*np.exp(.65j),OUTPUT)),run_time=2.5)
  self.show(eq(r'h\mapsto ch',x=3.5,y=-1.95,size=32,color=OUTPUT));self.note('모든 방향에 같은 회전과 같은 배율')
 def s04(self):
  a,b=self.pair(1.4,4.2);w=1+1j;c=2*w;r=ValueTracker(.65)
  self.show(label('입력점 주변 확대',x=-3.5,y=2.65,size=26,color=INPUT),label('출력점 주변 확대',x=3.5,y=2.65,size=26,color=OUTPUT),eq(r'f(z)=z^2,\quad w=1+i',y=-1.9,size=29))
  # Same magnification 1/r for both views, plus a fixed 1/|2w| calibration on output.
  fin=lambda t:np.exp(1j*t)
  fout=lambda t:(c*np.exp(1j*t)+r.get_value()*np.exp(2j*t))/abs(c)
  l=circle_samples(a,fin,INPUT);q=always_redraw(lambda:circle_samples(b,fout,OUTPUT))
  ideal=DashedVMobject(curve(b,lambda t:c*np.exp(1j*t)/abs(c),GOLD),num_dashes=48)
  self.show(l,q,ideal,Dot(pt(a,0),color=GOLD),Dot(pt(b,0),color=GOLD))
  radius=DecimalNumber(r.get_value(),num_decimal_places=3,font_size=32,color=GOLD).move_to(p(0,.4))
  radius.add_updater(lambda m:m.set_value(r.get_value()).move_to(p(0,.4)))
  self.show(label('실제 반지름 r',x=0,y=1.05,size=21,width=2.6,color=GOLD),radius,eq(r'\times\frac1r',x=0,y=-.45,size=29,color=MUTED))
  self.to(64);self.note('두 화면을 함께 확대 · 금색 점선: 미분이 예측한 원')
  self.to(68);self.play(r.animate.set_value(.035),run_time=6,rate_func=smooth)
  self.to(76);self.wipe();self.show(eq(r'\Delta f=2w\,h+h^2',y=1.7,size=43),eq(r'\Delta f\approx f\prime(w)h',y=.4,size=43,color=OUTPUT),label('미분값의 크기 → 배율   ·   각도 → 회전',y=-.9,size=30,color=GOLD));self.note('f′(w) ≠ 0인 점의 국소적 근사 · f′(w)=0도 복소미분 가능')
 def s05(self):
  a,b=self.pair(1.6,4);self.show(vec(a,1),vec(a,1j,GOLD),vec(b,1),eq(r'f(z)=\overline z',y=2.65,size=35))
  up=vec(b,1j,GOLD);self.add(up);self.to(82.5);self.play(Transform(up,vec(b,-1j,RED)),run_time=1.5)
  self.to(84);self.show(label('오른쪽은 유지',x=-3.5,y=-1.95,color=INPUT),label('위쪽은 아래로',x=3.5,y=-1.95,color=RED))
  self.to(89);self.wipe();a=plane(1.7,4.1);vs=VGroup(vec(a,1,INPUT),vec(a,1j,GOLD));self.show(a,vs)
  self.play(Rotate(vs,PI,about_point=pt(a,0)),run_time=2);self.show(label('위쪽을 뒤집으면 오른쪽도 뒤집힌다',x=4.5,y=.5,size=26,width=4.5,color=RED))
  self.to(94);self.wipe();self.show(eq(r'h=t:\quad\frac{\overline h}h=+1',x=-3.7,y=.8,size=37,color=INPUT),eq(r'h=it:\quad\frac{\overline h}h=-1',x=3.7,y=.8,size=37,color=RED),label('하나의 극한으로 모이지 않는다',y=-1.2,size=32,color=RED));self.note('t는 0이 아닌 실수 · t → 0')
 def s06(self):
  self.show(eq(r'f(x+iy)=u(x,y)+iv(x,y)',y=2.1,size=38))
  a=eq(r'u_x+i v_x',x=-3.7,y=.6,size=42,color=INPUT);b=eq(r'v_y-i u_y',x=3.7,y=.6,size=42,color=OUTPUT)
  self.show(a,b,label('실수축 방향의 차분비',x=-3.7,y=1.4,size=25,color=INPUT),label('허수축 방향의 차분비',x=3.7,y=1.4,size=25,color=OUTPUT))
  self.to(103);self.show(eq('=',y=.6,size=40),eq(r'\boxed{u_x=v_y,\quad u_y=-v_x}',y=-1,size=41,color=GOLD));self.note('실수부끼리 · 허수부끼리 같아야 한다')
  self.to(108);self.wipe();self.show(label('같은 미분의 정의',y=1.5,size=36),eq(r'h\in\mathbb R\quad\longrightarrow\quad h\in\mathbb C',y=.2,size=42),label('두 방향에서 모든 방향과 경로로',y=-1.1,size=31,color=GOLD));self.note('코시–리만 방정식은 복소미분의 필요조건')
 def s07(self):
  a=plane(2.6,4.3,x=-3.5);b=plane(2.6,4.3,x=3.5);self.show(a,b)
  border=DashedVMobject(curve(b,lambda t:(1.9+.13*np.cos(3*t))*np.exp(1j*t),INPUT),num_dashes=48)
  self.show(Dot(pt(a,0),color=GOLD),Circle(radius=.55,color=GOLD).move_to(pt(a,0)),border,label('한 점에서의 조건',x=-3.5,y=-1.95,size=27),label('열린 영역 Ω 전체',x=3.5,y=-1.95,size=27))
  self.to(121);self.show(label('정칙함수  ·  Holomorphic Function',y=2.65,size=29,color=OUTPUT),run_time=.5)
  self.to(123);circles=VGroup()
  for x in [-1,0,1]:
   for y in [-1,0,1]:
    circles.add(Circle(radius=.23,color=OUTPUT,stroke_width=1.5).move_to(pt(b,x+1j*y)),Dot(pt(b,x+1j*y),radius=.035,color=OUTPUT))
  self.play(LaggedStart(*[FadeIn(o) for o in circles],lag_ratio=.08),run_time=3)
  self.to(131);self.play(circles.animate.set_opacity(.3),border.animate.set_color(OUTPUT),run_time=2);self.note('각 점의 국소적 제약을 영역 전체에 부여한다')
 def s08(self):
  n=12;zs=np.exp(1j*np.linspace(0,TAU,n+1));dz=np.diff(zs);c=.8+.6j
  a=plane(1.5,4.1,x=-3.5);b=plane(1.5,4.1,x=3.5);self.show(a,b)
  polygon=VGroup(*[vec(a,v,INPUT,base=z,width=2) for z,v in zip(zs,dz)])
  self.show(polygon,label('경로의 이동량 Δz',x=-3.5,y=2.65,size=27,color=INPUT),label('함수값 × 이동량',x=3.5,y=2.65,size=27,color=OUTPUT))
  self.to(142);k=2;v=vec(a,dz[k],GOLD,base=zs[k]);formula=eq(r'f(z_k)\,\Delta z_k',y=-1.95,size=34);self.show(v,vec(b,c*dz[k],OUTPUT),formula)
  self.play(Rotate(v,np.angle(c),about_point=pt(a,zs[k])),run_time=1.2)
  contributions=VGroup(*[vec(b,c*d,OUTPUT,base=.7*np.exp(1j*t),width=2) for t,d in zip(np.linspace(0,TAU,n,endpoint=False),dz)])
  self.show(contributions);self.note('방향까지 포함한 복소수 벡터의 합')
  self.to(149);self.show(eq(r'f(z)=c=0.8+0.6i',y=.15,size=27,color=GOLD,width=3.3));self.to(152)
  self.play(FadeOut(formula),Transform(contributions,chain(c*dz,x=3.5+1.3*c.real,y=.3+1.3*c.imag,scale=1.3,c=OUTPUT)),run_time=2.5)
  self.show(eq(r'\sum_k\Delta z_k=0',x=-3.5,y=-1.65,size=30,color=INPUT),run_time=.4)
  self.to(157);self.show(eq(r'\sum_k c\Delta z_k=0',x=3.5,y=-1.65,size=30,color=OUTPUT));self.note('같은 회전·확대를 적용해도 벡터 다각형은 닫혀 있다')
 def s09(self):
  w=1+1j;r=.55;a=plane(2,4.1,x=-3.5);self.show(a)
  zs=[r*np.exp(1j*t) for t in np.linspace(0,TAU,12,endpoint=False)]
  vals=VGroup(*[vec(a,.22*(w+h)**2,OUTPUT,base=h,width=2) for h in zs]);self.show(vals,label('위치에 따라 달라지는 함수값',x=-3.5,y=2.65,size=26,color=OUTPUT),eq('f(z)=z^2',x=3.5,y=1.5,size=40))
  self.to(164);self.show(eq(r'f(w+h)=w^2+2wh+h^2',x=3.5,y=.2,size=32,width=6.5));self.note('앞서 본 국소 근사를 다시 사용한다')
  self.to(171);self.wipe();self.show(eq(r'f(w+h)=w^2+2wh+h^2',y=2.5,size=39))
  for x,fn,c,title in [(-4.8,lambda h:w*w,INPUT,'상수항'),(0,lambda h:2*w*h,OUTPUT,'일차항'),(4.8,lambda h:h*h,GOLD,'오차항')]:
   b=plane(1.4,2.8,x,.1);vs=VGroup(*[vec(b,.23*fn(h),c,base=h,width=2) for h in zs])
   self.show(b,vs,label(title,x=x,y=-1.65,size=27,color=c),run_time=.5)
  self.note('중심값 + 위치에 비례하는 변화 + 근사에서 남는 차이')
 def s10(self):
  a=plane(1.4,3.4,x=-4.8,y=.3);b=plane(1.4,3.4,x=0,y=.3)
  t=ValueTracker(0);v=always_redraw(lambda:vec(a,np.exp(1j*t.get_value()),INPUT));q=always_redraw(lambda:vec(b,1j*np.exp(2j*t.get_value()),OUTPUT))
  self.show(a,b,v,q,label('경로: 한 바퀴',x=-4.8,y=2.45,size=25,color=INPUT),label('일차항의 적분 기여: 두 바퀴',x=0,y=2.45,size=25,color=OUTPUT),eq(r'(z-w)\,dz=ir^2e^{2i\theta}d\theta',x=4.8,y=1.25,size=28,width=4.8),run_time=.4)
  self.play(t.animate.set_value(TAU),run_time=3.4,rate_func=linear)
  angles=np.linspace(0,TAU,16,endpoint=False);c=chain(.25j*np.exp(2j*angles),x=4.8,y=.05,scale=2,c=OUTPUT)
  self.show(c,eq(r'\oint c\,dz=0',x=-4.8,y=-1.85,size=30,color=INPUT),eq(r'\oint a(z-w)\,dz=0',x=0,y=-1.85,size=30,color=OUTPUT),run_time=.4);self.note('반대 방향의 적분 기여들이 상쇄된다')
 def s11(self):
  verts=[p(-5.9,-1.1),p(-2.3,-1.1),p(-4.1,2)]
  outline=Polygon(*verts,color=INPUT,fill_opacity=.04);self.show(outline,label('하나의 영역',x=-4.1,y=2.6,size=26,color=INPUT))
  def subdiv(vs):
   a,b,c=vs;ab=(a+b)/2;bc=(b+c)/2;ca=(c+a)/2
   return [[a,ab,ca],[ab,b,bc],[ca,bc,c],[ab,bc,ca]]
  current=verts;alltris=VGroup()
  for j in range(3):
   parts=subdiv(current);g=VGroup(*[Polygon(*v,color=INPUT,stroke_width=1.5,fill_opacity=.025) for v in parts]);alltris.add(g)
   chosen=Polygon(*parts[2],color=GOLD,fill_color=GOLD,fill_opacity=.16)
   self.play(Create(g),FadeIn(chosen),run_time=.7);current=parts[2]
  self.show(eq(r'f(z)=f(w)+f\prime(w)(z-w)+R(z)',x=3.2,y=1.7,size=32,width=7.4),eq(r'R(z)=o(|z-w|)',x=3.2,y=.6,size=37,color=GOLD))
  self.note('분할과 오차의 크기를 함께 제어 · 구르사 논증의 직관')
  self.to(191);self.wipe();a=plane(2,4.25,x=-3.5);c=curve(a,lambda t:1.5*np.exp(1j*t),OUTPUT)
  self.show(a,c,Dot(pt(a,0),color=GOLD),label('원과 내부를 포함하는 열린 영역에서 정칙',x=-3.5,y=2.65,size=24,width=6.7,color=OUTPUT))
  theta=ValueTracker(0);d=always_redraw(lambda:Dot(pt(a,1.5*np.exp(1j*theta.get_value())),radius=.07,color=GOLD));self.add(d)
  self.show(eq(r'\boxed{\oint_\Gamma f(z)\,dz=0}',x=3.5,y=.7,size=45,width=6.8,color=OUTPUT))
  accumulated=lambda t:(1.5**3/3)*(np.exp(3j*t)-1)
  endpoint=lambda t:p(3.5+.55*accumulated(t).real,-1.15+.55*accumulated(t).imag)
  trace=ParametricFunction(endpoint,t_range=[0,TAU,.025],color=OUTPUT,stroke_width=2)
  dot=always_redraw(lambda:Dot(endpoint(theta.get_value()),radius=.055,color=GOLD))
  self.add(dot,Dot(endpoint(0),radius=.035,color=INK),label('누적합 예: f(z)=z²',x=3.5,y=-1.95,size=21,color=MUTED))
  self.play(theta.animate.set_value(TAU),Create(trace),run_time=4,rate_func=linear)
  self.to(199);self.show(label('코시 적분 정리',x=3.5,y=1.9,size=32,color=OUTPUT));self.note('경계 Γ는 반시계방향 · 국소적 제약에서 영역 전체의 관계로')
