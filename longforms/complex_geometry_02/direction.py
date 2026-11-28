"""Part 02: coordinate-bound Cauchy derivation and exact conformal heat transport."""
import os,json,math
from pathlib import Path
import numpy as np
from scipy.special import j0,jn_zeros
from manim import *
from longforms.complex_geometry_01.direction import GeometryScene,plane,pt,vec,curve,circle_samples,eq,label,p,INPUT,OUTPUT,GOLD,RED,INK,MUTED
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
assets=HERE.parents[1]/'media'/'complex_geometry_02_assets'/os.getenv('CG_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex');config.text_dir=str(assets/'texts')
W=.3+.2j
HEAT_COLORS=[ManimColor(c) for c in ['#3464A5','#E9D77D','#DF5B43']]
def contour(a,r=1.5,center=0,color=INPUT):return curve(a,lambda t:center+r*np.exp(1j*t),color)
def direction_arcs(a,r,center=0,color=INPUT,clockwise=False):
 g=VGroup();sg=-1 if clockwise else 1
 for t in np.linspace(0,TAU,4,endpoint=False):
  g.add(Arrow(pt(a,center+r*np.exp(1j*t)),pt(a,center+r*np.exp(1j*(t+sg*.18))),buff=0,color=color,stroke_width=2,max_tip_length_to_length_ratio=.8))
 return g
def mesh_edges():
 edges=[]
 for i in range(4):
  for j in range(3):
   vs=[complex(i-2,j-1.5),complex(i-1,j-1.5),complex(i-1,j-.5),complex(i-2,j-.5)]
   edges.extend((vs[k],vs[(k+1)%4]) for k in range(4))
 return edges
def temp_color(t):
 alpha=float(np.clip((t-20)/60,0,1));stops=HEAT_COLORS
 return interpolate_color(stops[0 if alpha<.5 else 1],stops[1 if alpha<.5 else 2],alpha*2 if alpha<.5 else (alpha-.5)*2)
def F(z):return z+.4*z*z
class TemperatureMesh(VGroup):
 """Material labels and colors live on disk coordinates; F moves the actual vertices."""
 def __init__(self,x=0,y=.3,size=1.7,morph=0,fill=True):
  super().__init__();self.samples=[];self.centers=[];self.origin=p(x,y);self.unit=size
  for k in range(10):
   r0=k/10;r1=(k+1)/10
   for j in range(60):
    t0=TAU*j/60;t1=TAU*(j+1)/60
    vs=np.array([r0*np.exp(1j*t0),r1*np.exp(1j*t0),r1*np.exp(1j*t1),r0*np.exp(1j*t1)])
    z=(r0+r1)/2*np.exp(1j*(t0+t1)/2);self.samples.append(vs);self.centers.append(z)
    pts=[self.point(v,morph) for v in vs];c=temp_color(50+30*z.real)
    self.add(Polygon(*pts,stroke_color=c,stroke_width=.5,stroke_opacity=1 if fill else 0,fill_color=c,fill_opacity=1 if fill else 0))
  self.centers=np.array(self.centers);self.morph=morph
 def point(self,z,m):
  q=z+m*.4*z*z;return self.origin+self.unit*p(q.real,q.imag)
 def set_morph(self,m):
  for patch,vs in zip(self,self.samples):patch.set_points_as_corners([self.point(v,m) for v in [*vs,vs[0]]])
  self.morph=m;return self
 def heat_time(self,t):
  rho=abs(self.centers);beta=float(jn_zeros(0,1)[0]);ts=50+30*self.centers.real+12*np.exp(-beta*beta*t)*j0(beta*rho)
  for patch,v in zip(self,ts):patch.set_fill(temp_color(v),opacity=1).set_stroke(temp_color(v),opacity=1)
  return self
def rim(x=0,y=.3,size=1.7,m=0,color=INK):
 return ParametricFunction(lambda t:p(x,y)+size*p((np.exp(1j*t)+m*.4*np.exp(2j*t)).real,(np.exp(1j*t)+m*.4*np.exp(2j*t)).imag),t_range=[0,TAU,.025],color=color,stroke_width=2)
def conformal_grid(x=0,y=.3,size=1.7,m=0):
 g=VGroup()
 for k in np.linspace(-.8,.8,9):
  extent=np.sqrt(1-k*k)
  for vertical in [False,True]:
   def fn(t,k=k,v=vertical):
    z=complex(k,t) if v else complex(t,k);q=z+m*.4*z*z
    return p(x,y)+size*p(q.real,q.imag)
   g.add(ParametricFunction(fn,t_range=[-extent,extent,.03],color=MUTED,stroke_width=1,stroke_opacity=.65))
 return g

class AnalysisScene(GeometryScene):
 data=DATA
 def s01(self):
  a=plane(3,5.6);self.show(a,eq(r'\oint_\Gamma f(z)\,dz=0',x=5,y=1.5,size=36,width=4.5))
  edges=mesh_edges();g=VGroup(*[Line(pt(a,u),pt(a,v),color=MUTED,stroke_width=1) for u,v in edges]);self.play(Create(g),run_time=1.8)
  self.to(4);arrows=VGroup(*[Arrow(pt(a,u)+.055*(pt(a,v)-pt(a,u)),pt(a,v)-.055*(pt(a,v)-pt(a,u)),buff=0,color=INPUT,stroke_width=1.8,max_tip_length_to_length_ratio=.13) for u,v in edges]);self.play(LaggedStart(*[GrowArrow(o) for o in arrows],lag_ratio=.025),run_time=3)
  self.note('모든 조각은 반시계방향 · 각 조각과 그 주변에서 정칙')
  self.to(9);self.show(SurroundingRectangle(VGroup(*arrows[20:28]),color=GOLD,buff=.06),run_time=.5)
 def s02(self):
  a=plane(2,4.5,x=-3.5);self.show(a)
  self.show(Rectangle(width=3.8,height=2.6,color=MUTED).move_to(p(-3.5,.3)),DashedLine(p(-3.5,-1),p(-3.5,1.6),color=GOLD),Arrow(p(-3.7,-.8),p(-3.7,1.4),buff=0,color=INPUT),Arrow(p(-3.3,1.4),p(-3.3,-.8),buff=0,color=OUTPUT))
  self.show(eq(r'\int_\gamma f(z)\,dz',x=3.5,y=1.6,size=34,color=INPUT),eq(r'+\int_{-\gamma}f(z)\,dz',x=3.5,y=.3,size=34,color=OUTPUT))
  self.to(17);self.show(eq('A-A=0',x=3.5,y=-1.1,size=42,color=RED));self.note('같은 함수 · 같은 경로 · 반대 방향')
  self.to(20);self.wipe();a=plane(3,5.2,x=-3.5);edges=mesh_edges();inner=[];outer=[]
  for u,v in edges:
   boundary=(u.real==v.real and abs(u.real)==2) or (u.imag==v.imag and abs(u.imag)==1.5)
   o=Arrow(pt(a,u),pt(a,v),buff=0,color=OUTPUT if boundary else INPUT,stroke_width=2,max_tip_length_to_length_ratio=.15)
   (outer if boundary else inner).append(o)
  self.add(a,*inner,*outer);self.play(*[FadeOut(o) for o in inner],run_time=2.5)
  self.to(25);self.show(eq(r'\sum_k\oint_{\partial D_k}f(z)\,dz',x=3.8,y=1.3,size=34,width=6),eq(r'=\oint_{\partial D}f(z)\,dz=0',x=3.8,y=-.2,size=34,width=6,color=OUTPUT));self.note('내부 경계는 상쇄되고 바깥 경계만 남는다')
 def s03(self):
  a=plane(2.1,4.7,x=-3.5);outer=contour(a,1.6);inner=contour(a,.7,color=OUTPUT);innerdirs=direction_arcs(a,.7,color=OUTPUT,clockwise=True);self.show(a,outer,inner,direction_arcs(a,1.6),innerdirs)
  self.show(eq(r'\oint_{\Gamma_1}f(z)dz-\oint_{\Gamma_2}f(z)dz=0',x=3.7,y=1.3,size=31,width=6.4));self.note('두 경계 사이에서 정칙 · 안쪽 영역은 제외')
  self.to(35);div=VGroup(*[Line(pt(a,.7*np.exp(1j*t)),pt(a,1.6*np.exp(1j*t)),color=MUTED,stroke_width=1) for t in np.linspace(0,TAU,12,endpoint=False)],contour(a,1.15,color=MUTED));self.play(Create(div),run_time=2)
  self.to(39);self.play(FadeOut(div),run_time=2)
  self.to(44);self.play(Transform(innerdirs,direction_arcs(a,.7,color=OUTPUT)),run_time=.5);self.show(eq(r'\boxed{\oint_{\Gamma_1}f(z)dz=\oint_{\Gamma_2}f(z)dz}',x=3.7,y=-.6,size=32,width=6.6,color=OUTPUT));self.note('Γ₁, Γ₂를 모두 반시계방향으로 쓰면 적분값이 같다')
 def s04(self):
  a=plane(2,4.7,x=-3.5);theta=ValueTracker(.7);z=lambda:1.5*np.exp(1j*theta.get_value())
  self.show(a,contour(a),Dot(pt(a,W),color=GOLD),label('w',x=-2.9,y=.45,color=GOLD),eq('f(w)=?',x=3.7,y=1.4,size=43,color=GOLD))
  self.to(56);samples=VGroup(*[Dot(pt(a,1.5*np.exp(1j*t)),radius=.04,color=INPUT) for t in np.linspace(0,TAU,24,endpoint=False)]);self.show(samples,label('경계의 f(z)는 알려져 있다',x=3.7,y=.1,size=28,color=INPUT))
  self.to(61);denom=eq(r'z-w',x=3.7,y=-1.2,size=38,color=OUTPUT);dot=always_redraw(lambda:Dot(pt(a,z()),color=INPUT));v=always_redraw(lambda:vec(a,z()-W,OUTPUT,base=W));self.show(dot,v,denom);self.play(theta.animate.set_value(1.8),run_time=1.5)
  self.to(64);self.show(eq(r'g_w(z)=\frac{f(z)}{z-w}',x=3.7,y=2.15,size=34));self.to(67)
  dot.clear_updaters();v.clear_updaters();self.play(dot.animate.move_to(pt(a,W)).set_color(RED),Transform(v,vec(a,.0001,OUTPUT,base=W)),run_time=1.6)
  self.play(Transform(denom,eq(r'z-w\to0',x=3.7,y=-1.2,size=35,color=RED)),run_time=.6);self.to(72);self.note('원래 f는 정칙 · 새 적분 대상 g_w에서만 w를 제외한다',OUTPUT)
 def s05(self):
  a=plane(2,4.6,x=-3.5);s=ValueTracker(0)
  center=lambda:s.get_value()*W;radius=lambda:1.5*(1-s.get_value())+.15*s.get_value()
  moving=always_redraw(lambda:contour(a,radius(),center(),OUTPUT));self.show(a,DashedVMobject(contour(a)),moving,Dot(pt(a,W),color=GOLD))
  self.show(eq(r'\oint_\Gamma\frac{f(z)}{z-w}dz',x=3.7,y=1.4,size=36),eq(r'=\oint_{C_r(w)}\frac{f(z)}{z-w}dz',x=3.7,y=-.1,size=36,color=OUTPUT))
  self.play(s.animate.set_value(1),run_time=3.6,rate_func=smooth);self.to(80);self.note('w를 통과하지 않고 안쪽에 남겨 둔 채 경로를 축소한다');self.play(Indicate(moving,color=GOLD),run_time=1.5)
 def s06(self):
  a=plane(1.5,4.4,x=-3.5);t=ValueTracker(.4);rad=always_redraw(lambda:vec(a,np.exp(1j*t.get_value()),INPUT));dot=always_redraw(lambda:Dot(pt(a,np.exp(1j*t.get_value())),color=INPUT))
  self.show(a,contour(a,1,color=MUTED),dot,Dot(pt(a,0),color=GOLD));self.play(t.animate.set_value(.8),run_time=1.5)
  self.to(91);self.show(rad,eq(r'z=w+re^{i\theta}',x=3.5,y=1.8,size=37),eq(r'z-w=re^{i\theta}',x=3.5,y=.6,size=40,color=INPUT));self.play(t.animate.set_value(2.1),run_time=2.8)
  self.to(96);tan=always_redraw(lambda:vec(a,.5j*np.exp(1j*t.get_value()),OUTPUT,base=np.exp(1j*t.get_value())))
  copy=rad.copy().clear_updaters();self.add(copy);self.play(Rotate(copy,PI/2,about_point=pt(a,0)),run_time=1);self.play(FadeOut(copy),FadeIn(tan),run_time=.4)
  self.show(eq(r'\times i\quad\Longrightarrow\quad90^\circ',x=3.5,y=-.5,size=31,color=GOLD))
  self.to(101);self.show(eq(r'dz=ire^{i\theta}d\theta',x=3.5,y=-1.65,size=37,color=OUTPUT));self.note('접선 방향 화살표는 미소 이동량 dz를 확대해 표시')
 def s07(self):
  a=plane(1.5,3.7,x=-4.5);self.show(a,contour(a,1,color=MUTED),vec(a,np.exp(.8j),INPUT),vec(a,.55j*np.exp(.8j),OUTPUT,base=np.exp(.8j)))
  first=eq(r'\frac{f(z)}{z-w}\,dz',x=2.5,y=1.9,size=40);expanded=MathTex(r'\frac{f(z)}{re^{i\theta}}\;ire^{i\theta}d\theta',substrings_to_isolate=[r're^{i\theta}'],font_size=40).move_to(p(2.5,.45))
  self.show(first,expanded);self.to(111)
  factors=[expanded.id_to_vgroup_dict[part_id] for tex,part_id in expanded.matched_strings_and_ids if tex==r're^{i\theta}']
  self.play(*[Create(Cross(part,stroke_color=RED,stroke_width=2)) for part in factors],run_time=1)
  self.show(eq(r'\frac{re^{i\theta}}{re^{i\theta}}=1',x=-4.5,y=-1.65,size=27,color=RED),eq(r'\boxed{if(z)d\theta}',x=2.5,y=-1.15,size=44,color=OUTPUT))
  self.to(114);self.note('반지름 r과 절대 각도 θ는 소거 · 90° 회전 i와 미소 각도 dθ는 남는다')
 def s08(self):
  a,b=self.pair(2.2,4.3);r=ValueTracker(.65)
  inp=always_redraw(lambda:circle_samples(a,lambda t:W+r.get_value()*np.exp(1j*t),INPUT))
  out=always_redraw(lambda:circle_samples(b,lambda t:(W+r.get_value()*np.exp(1j*t))**2,OUTPUT))
  self.show(inp,out,Dot(pt(a,W),color=GOLD),Dot(pt(b,W*W),color=GOLD),label('입력 z → w',x=-3.5,y=2.65,size=27,color=INPUT),label('출력 f(z) → f(w)',x=3.5,y=2.65,size=27,color=OUTPUT))
  self.to(121);self.play(r.animate.set_value(.018),run_time=6);self.to(129);self.show(eq(r'\int_0^{2\pi}d\theta=2\pi',y=-1.85,size=39,color=GOLD));self.note('연속성: 원 위 모든 함수값이 중심의 함수값으로 모인다')
 def s09(self):
  a=plane(1.4,3.8,x=-4.3);self.show(a,contour(a,.8,W),Dot(pt(a,W),color=GOLD))
  self.show(eq(r'i\int_0^{2\pi}f(w+re^{i\theta})d\theta',x=2.5,y=1.8,size=35,width=8),eq(r'\xrightarrow{r\to0}\;2\pi i f(w)',x=2.5,y=.4,size=42,color=GOLD))
  self.to(138);self.show(eq(r'f(w)=\frac1{2\pi i}\oint_\Gamma\frac{f(z)}{z-w}dz',x=2.5,y=-1.2,size=36,width=8,color=OUTPUT))
  self.to(142);self.note('검산 예: f(z)=z², w=0.3+0.2i → f(w)=0.05+0.12i');self.to(146);self.show(label('코시 적분 공식',x=-4.3,y=2.65,size=29,color=OUTPUT))
 def s10(self):
  a=plane(2,4.2,x=-4.7);w=ValueTracker(.15);self.show(a,contour(a,1.5),Dot(pt(a,1.5*np.exp(.9j)),color=INPUT))
  dot=always_redraw(lambda:Dot(pt(a,w.get_value()+.2j),color=GOLD));line=always_redraw(lambda:DashedLine(dot.get_center(),pt(a,1.5*np.exp(.9j)),color=GOLD));self.show(dot,line)
  formula=eq(r'f(w)=\frac1{2\pi i}\oint_\Gamma\frac{f(z)}{z-w}dz',x=2.2,y=1.75,size=34,width=8.5);self.show(formula);self.note('원과 내부를 포함하는 열린 영역에서 정칙 · 경계 Γ는 고정')
  self.to(158);self.play(w.animate.set_value(.65),run_time=3);self.show(eq(r'\frac{\partial}{\partial w}\frac1{z-w}=\frac1{(z-w)^2}',x=2.2,y=.35,size=35,width=8.5,color=GOLD))
  self.to(165);self.show(eq(r'f\prime(w)=\frac1{2\pi i}\oint_\Gamma\frac{f(z)}{(z-w)^2}dz',x=2.2,y=-1.15,size=34,width=8.5,color=OUTPUT))
  self.to(167);self.wipe();self.show(eq(r'f^{(n)}(w)=\frac{n!}{2\pi i}\oint_\Gamma\frac{f(z)}{(z-w)^{n+1}}dz',y=.6,size=46,color=OUTPUT),label('같은 경계 정보로 모든 차수의 미분값',y=-1.4,size=30))
 def s11(self):
  a=Axes(x_range=[-1.2,1.2,1],y_range=[-1.5,2.5,1],x_length=4.4,y_length=3.2,tips=False).move_to(p(-3.5,.3));b=a.copy().move_to(p(3.5,.3))
  self.show(a,b,a.plot(lambda x:x*abs(x),x_range=[-1.1,1.1,.02],color=INPUT),b.plot(lambda x:2*abs(x),x_range=[-1.1,1.1,.02],color=OUTPUT),eq('f(x)=x|x|',x=-3.5,y=2.4,size=35),eq(r'f\prime(x)=2|x|',x=3.5,y=2.4,size=35))
  self.show(Dot(b.c2p(0,0),color=RED),label('0에서 두 번째 미분 불가',x=3.5,y=-1.65,color=RED));self.to(178);self.wipe();self.show(eq(r'f\to f\prime\to f^{\prime\prime}\to\cdots\to f^{(n)}',y=.8,size=46,color=OUTPUT),label('열린 영역 전체에서 복소미분 가능',y=-.8,size=32),label('모든 차수의 미분이 존재',y=-1.65,size=28,color=OUTPUT))
 def s12(self):
  a=Axes(x_range=[-2,2,1],y_range=[0,8,2],x_length=6.8,y_length=3.6,tips=False).move_to(p(-2.8,.35));f=a.plot(np.exp,x_range=[-2,2,.025],color=INPUT);poly=a.plot(lambda x:1+x,x_range=[-1,2,.03],color=OUTPUT)
  self.show(a,f,poly,eq(r'e^z=\sum_{n=0}^{\infty}\frac{z^n}{n!}',x=4.3,y=1.2,size=37,width=5.5),label('eᶻ의 실수축 단면',x=-2.8,y=2.55,size=24,color=INPUT));tag=label('테일러 다항식 n=1',x=4.3,y=-.2,size=27,color=OUTPUT);self.show(tag)
  for n in [3,6,12]:
   self.play(Transform(poly,a.plot(lambda x,n=n:sum(x**k/math.factorial(k) for k in range(n+1)),x_range=[-2,2,.025],color=OUTPUT)),Transform(tag,label(f'테일러 다항식 n={n}',x=4.3,y=-.2,size=27,color=OUTPUT)),run_time=1.3)
  self.to(192);self.wipe();a,b=self.pair(2,3.7);self.show(contour(a,1.5),Dot(pt(a,0),color=GOLD),contour(b,1.5,color=OUTPUT),Dot(pt(b,0),color=GOLD))
  rays=VGroup(*[DashedLine(pt(a,1.5*np.exp(1j*t)),pt(a,0),color=INPUT,stroke_width=1) for t in np.linspace(0,TAU,12,endpoint=False)])
  rings=VGroup(*[contour(b,r,color=OUTPUT) for r in [.35,.7,1.05]])
  self.show(rays,rings,label('경계 → 내부',x=-3.5,y=-1.95,color=INPUT),label('한 점의 모든 미분값 → 주변',x=3.5,y=-1.95,size=26,color=OUTPUT));self.to(200);self.note('각 점의 국소적인 조건이 함수의 여러 부분을 연결한다')
 def s13(self):
  a=plane(1.3,4,x=-3.5);self.show(a,contour(a,1),label('수학적 영역',x=-3.5,y=2.65,size=27,color=INPUT));plate=Circle(radius=1.7,color=MUTED,fill_color='#7C8A99',fill_opacity=1).move_to(p(3.5,.3));self.show(plate)
  self.to(209);field=TemperatureMesh(3.5,.3,1.7).heat_time(0);self.play(FadeOut(plate),FadeIn(field),run_time=1);self.add(rim(3.5,.3));self.show(label('경계 온도는 고정',x=3.5,y=2.65,size=27),label('20°C',x=1.4,y=.3,size=23,color=INPUT),label('80°C',x=5.6,y=.3,size=23,color=RED))
  self.to(213);self.play(UpdateFromAlphaFunc(field,lambda m,t:m.heat_time(1.5*t)),run_time=6,rate_func=linear);self.to(221)
  arrows=VGroup(*[Arrow(p(4.5,y),p(2.5,y),buff=0,color=INK,stroke_width=2) for y in [-.35,.3,.95]]);self.show(arrows,eq(r'\frac{\partial T}{\partial t}\to0,\quad\Delta T=0',x=-3.5,y=.5,size=37,width=5.5));self.note('열은 계속 흐르지만 각 부분에 축적되는 열은 없다')
  self.to(226);self.show(Dot(p(3.5+1.7*.2,.3),color=GOLD))
 def s14(self):
  field=TemperatureMesh(-3.5,.3,1.7);self.show(field,rim(-3.5,.3),eq('T(x,y)=50+30x',x=3.5,y=1.8,size=36))
  center=.2;cr=.4;circle=Circle(radius=1.7*cr,color=INK).move_to(p(-3.5+1.7*center,.3));badge=label('56°C',x=-3.5+1.7*center,y=-.2,size=28,color=GOLD);panel=BackgroundRectangle(badge,color='#101722',fill_opacity=.95,buff=.08);self.show(circle,Dot(circle.get_center(),color=GOLD),panel,badge)
  for z,s in [(center-cr,'44'),(center+cr,'68'),(center+cr*1j,'56'),(center-cr*1j,'56')]:
   pos=p(-3.5+1.7*complex(z).real,.3+1.7*complex(z).imag);offset=.3*(pos-circle.get_center())/(1.7*cr)
   self.show(Dot(pos,radius=.05,color=INK),label(s,size=23,color='#101722').move_to(pos+offset),run_time=.15)
  self.show(eq(r'\frac{44+56+68+56}{4}=56',x=3.5,y=.3,size=38,color=GOLD));self.note('이 선형 예시에서는 대칭인 네 표본의 평균도 정확히 일치')
  self.to(235);self.show(eq(r'f(z)=50+30z',x=3.5,y=-.9,size=36,color=OUTPUT));self.to(239);self.note('공통 방정식: ΔT = Δu = 0 · 일반적인 평균값 성질은 원 둘레 전체의 평균')
 def s15(self):
  left=TemperatureMesh(-3.7,.2,1.5,morph=1,fill=False);right=TemperatureMesh(3.7,.2,1.5,fill=True)
  boundary=VGroup(*[Line(left.point(np.exp(1j*t),1),left.point(np.exp(1j*(t+TAU/80)),1),color=temp_color(50+30*np.cos(t)),stroke_width=5) for t in np.linspace(0,TAU,80,endpoint=False)])
  self.show(left,boundary,rim(3.7,.2,1.5,color=MUTED),eq(r'F(\zeta)=\zeta+0.4\zeta^2',y=2.55,size=32),label('복잡한 영역',x=-3.7,y=-1.8,size=27),label('계산하기 쉬운 원판',x=3.7,y=-1.8,size=27));self.note('경계의 온도만 알고 있는 문제')
  self.to(248);self.play(Indicate(boundary,color=GOLD),run_time=1)
  self.to(252);moving=TemperatureMesh(-3.7,.2,1.5,morph=1,fill=False);lines=conformal_grid(-3.7,.2,1.5,m=1);self.show(lines)
  targetgrid=conformal_grid(3.7,.2,1.5,m=0);self.play(Transform(lines,targetgrid),Transform(boundary,VGroup(*[Line(right.point(np.exp(1j*t),0),right.point(np.exp(1j*(t+TAU/80)),0),color=temp_color(50+30*np.cos(t)),stroke_width=5) for t in np.linspace(0,TAU,80,endpoint=False)])),run_time=4)
  self.to(258);self.note('각 경계점의 온도를 그대로 대응점에 옮긴다');self.to(263);self.play(FadeIn(right),run_time=.7)
  result=TemperatureMesh(-3.7,.2,1.5,morph=1);self.play(TransformFromCopy(right,result),run_time=1.5);self.note('T(F(ζ)) = U(ζ) · 좌표가 바뀌어도 점에 연결된 온도는 유지')
 def s16(self):
  a,b=self.pair(2,3.8);l=curve(a,lambda t:.6*np.cos(t)+1.1j*np.sin(t),RED);r=curve(b,lambda t:.85*np.exp(1j*t),OUTPUT);self.show(l,r,label('방향마다 다른 확대',x=-3.5,y=2.5,size=27,color=RED),label('회전과 균일한 확대',x=3.5,y=2.5,size=27,color=OUTPUT))
  self.show(eq(r'T(x,y)=x^2-y^2:\quad\Delta T=0',y=-1.95,size=30));self.to(270);self.note('비균일 변환 뒤: x²/4 − y²/9 → 라플라스 값이 0이 아니다',RED)
  self.to(273);self.wipe();self.show(eq(r'\Delta_\zeta(T\circ F)=|F\prime(\zeta)|^2(\Delta_zT)\circ F',y=1.5,size=40,color=INPUT),eq(r'\Delta_zT=0\quad\Longrightarrow\quad\Delta_\zeta(T\circ F)=0',y=-.1,size=39,color=OUTPUT));self.note('국소 배율의 제곱이 곱해져도 0은 그대로 0')
  self.to(278);self.show(eq(r'\Delta z\approx F\prime(\zeta)\Delta\zeta',y=-1.4,size=35,color=GOLD));self.to(284);self.wipe()
  self.show(rim(-3.7,.2,1.5,m=1,color=INPUT),conformal_grid(-3.7,.2,1.5,m=1),rim(3.7,.2,1.5,color=OUTPUT),conformal_grid(3.7,.2,1.5),Arrow(p(-.7,.2),p(.7,.2),buff=0,color=GOLD),eq(r'\Delta T=0',x=-3.7,y=-1.8,size=33,color=INPUT),eq(r'\Delta U=0',x=3.7,y=-1.8,size=33,color=OUTPUT),label('다른 모양, 같은 수학적 성질',y=2.5,size=30))
