"""A metric derived from actual disk automorphisms; exact finite circles and distances."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from longforms.complex_geometry_01.direction import GeometryScene,plane,pt,vec,curve,circle_samples,eq,label,p,INPUT,OUTPUT,GOLD,RED,INK,MUTED
from longforms.complex_geometry_03.direction import sphere,torus,sheets
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
assets=HERE.parents[1]/'media'/'complex_geometry_04_assets'/os.getenv('CG_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex');config.text_dir=str(assets/'texts')

def mobius(z,a):return (z+a)/(1+np.conj(a)*z)
def inverse(z,a):return (z-a)/(1-np.conj(a)*z)
def derivative(z,a):return (1-abs(a)**2)/(1+np.conj(a)*z)**2
def distance(z,w):return 2*np.arctanh(np.clip(abs((z-w)/(1-np.conj(w)*z)),0,1-1e-15))
def circle_parameters(a,rho=.23):
 den=1-rho*rho*abs(a)**2
 return (1-rho*rho)*a/den,(1-abs(a)**2)*rho/den
def xy(z,x=0,y=.25,R=2.1):return p(x+R*complex(z).real,y+R*complex(z).imag)
def rim(x=0,y=.25,R=2.1,c=MUTED):return Circle(radius=R,color=c,stroke_width=1.7).move_to(p(x,y))
def hcircle(a,rho=.23,x=0,y=.25,R=2.1,c=OUTPUT,width=2):
 center,r=circle_parameters(a,rho)
 return Circle(radius=R*r,color=c,stroke_width=width).move_to(xy(center,x,y,R))
def disk_grid(a=0,x=0,y=.25,R=2.1):
 g=VGroup()
 for v in np.linspace(-.8,.8,9):
  end=np.sqrt(1-v*v)
  for vertical,c in [(False,OUTPUT),(True,INPUT)]:
   g.add(ParametricFunction(lambda t,v=v,vertical=vertical:xy(mobius(complex(v,t) if vertical else complex(t,v),a),x,y,R),t_range=[-end,end,.025],color=c,stroke_width=1,stroke_opacity=.45))
 return g
def rings(x=0,y=.25,R=2.1):
 return VGroup(*[Circle(radius=R*np.tanh(d/2),color=OUTPUT,stroke_width=1.1,stroke_opacity=.72).move_to(p(x,y)) for d in np.arange(.5,6.51,.5)],*[Line(xy(0,x,y,R),xy(np.exp(1j*t),x,y,R),color=MUTED,stroke_width=.8,stroke_opacity=.38) for t in np.linspace(0,TAU,12,endpoint=False)])
def ruler(y=0,x=-5.8,width=11.6,hyper=False):
 g=VGroup(Line(p(x,y),p(x+width,y),color=OUTPUT if hyper else INPUT,stroke_width=2))
 vals=np.tanh(np.arange(0,8.5,.5)/2) if hyper else np.linspace(0,1,17)
 for j,r in enumerate(vals):
  g.add(Line(p(x+width*r,y-.03),p(x+width*r,y+(.24 if j%2==0 else .14)),color=OUTPUT if hyper else INPUT,stroke_width=1.6))
 return g

def pattern_centers():
 rho=.16;R=2*np.arctanh(rho);centers=[0j]
 # Enough world rings to reveal new circles throughout an observer shift up to a=.65.
 for k in range(1,9):
  d=.8*k;n=max(6,int(PI/np.arcsin(np.sinh(R)/np.sinh(d))))
  pts=np.tanh(d/2)*np.exp(1j*(np.arange(n)*TAU/n+(k%2)*PI/n))
  keep=np.zeros(n,dtype=bool)
  for a in [0,.2,.4,.65]:
   _,rr=circle_parameters(inverse(pts,a),rho)
   keep|=rr>.0028
  centers.extend(pts[keep])
 return np.array(centers)

class DiskPattern(VGroup):
 def __init__(self,x=0,y=.25,R=2.1,observer=0):
  super().__init__();self.centers=pattern_centers();self.x=x;self.y=y;self.R=R
  self.unit=Circle(radius=1).points.copy()
  for j,a in enumerate(self.centers):
   self.add(VMobject(stroke_color=INPUT if j%3==0 else OUTPUT,stroke_width=1.1,fill_opacity=.015,fill_color=OUTPUT))
  self.set_observer(observer)
 def set_observer(self,a):
  centers,radii=circle_parameters(inverse(self.centers,a),.16)
  for m,c,r in zip(self,centers,radii):m.set_points(self.unit*(self.R*r)+xy(c,self.x,self.y,self.R))
  return self

class MetricScene(GeometryScene):
 data=DATA
 def s01(self):
  a=plane(1.5,2.6,0,.55);s=sphere(-4.8,.55,1.3);d=rim(4.8,.55,1.3,OUTPUT)
  self.show(s,a,d,label('리만 구면',x=-4.8,y=-1.25,color=INPUT),label('복소평면',y=-1.25),label('단위원판',x=4.8,y=-1.25,color=OUTPUT))
  dots=VGroup(*[Dot(pt(a,.75*k),radius=.045,color=GOLD) for k in [-1,0,1]])
  self.show(dots);self.to(5);self.play(*[q.animate.move_to(pt(a,0)) for q in dots],run_time=1)
  self.to(6);self.show(label('구면 기하학',x=-4.8,y=-2.05,size=25),label('유클리드 기하학',y=-2.05,size=25),label('쌍곡 기하학',x=4.8,y=-2.05,size=25))
  self.to(11);self.wipe();disk=rim(0,.3,2,INPUT);grid=disk_grid(0,0,.3,2)
  self.show(disk,grid);self.to(14);self.play(VGroup(disk,grid).animate.stretch(.25,1),run_time=1)
  self.play(VGroup(disk,grid).animate.stretch(4,1),run_time=3)
  self.to(20);self.note('같은 평평한 원판에서, 어떻게 다른 기하학이 나타날까?',GOLD)
 def s02(self):
  x=-3.3;R=2.1;a=ValueTracker(0)
  self.show(rim(x,R=R),Dot(xy(0,x,R=R),color=INPUT),hcircle(0,.16,x=x,R=R,c=INPUT))
  mesh=always_redraw(lambda:disk_grid(a.get_value(),x=x,R=R));small=always_redraw(lambda:hcircle(a.get_value(),.16,x=x,R=R))
  marker=always_redraw(lambda:Dot(xy(a.get_value(),x,R=R),color=GOLD,radius=.02))
  self.add(mesh,small,marker)
  self.to(26);self.show(eq(r'T_a(z)=\frac{z+a}{1+\overline a z}',x=3.4,y=1.8,size=37,width=6.7),eq(r'T_a(0)=a,\qquad |a|<1',x=3.4,y=.4,size=33,width=6.7),label('원판 전체를 자기 자신으로',x=3.4,y=-.6,size=28,width=6.2,color=OUTPUT))
  self.to(33);self.play(a.animate.set_value(.3),run_time=2.5,rate_func=smooth)
  self.to(36)
  for target in [.6,.85,.95]:
   self.add(hcircle(a.get_value(),.16,x=x,R=R,c=INPUT,width=1).set_stroke(opacity=.38))
   self.play(a.animate.set_value(target),run_time=1.5,rate_func=smooth)
  self.to(41);self.play(Circumscribe(rim(x,R=R),color=GOLD),run_time=.7)
  self.note('경계는 집합으로 보존된다 · 경계의 개별 점은 움직인다')
 def s03(self):
  x=-3.4;R=2.05;self.show(rim(x,R=R))
  positions=[0,.55,.8,.95]
  for a in positions:self.show(hcircle(a,.16,x=x,R=R),run_time=.25)
  self.show(label('새로운 이동의 조건',x=3.5,y=1.5,size=30,color=GOLD),label('이 변환에서도 거리와 크기를 유지한다',x=3.5,y=.5,size=27,width=6.4,color=OUTPUT))
  self.to(51);diameters=VGroup()
  for a in positions:
   c,r=circle_parameters(a,.16);diameters.add(Line(xy(c-r,x,R=R),xy(c+r,x,R=R),color=GOLD,stroke_width=2))
  measure=ruler(y=-2.1,x=-5.6,width=4.4)
  self.show(diameters,measure,run_time=.5)
  self.show(label('화면상의 직경은 서로 다르다',x=3.5,y=-.6,size=28,width=6.2,color=RED));self.to(56)
  self.play(FadeOut(measure),run_time=.4);self.note('어느 위치에서 길이를 얼마나 다르게 측정해야 할까?',GOLD)
 def s04(self):
  # Same coordinate planes and vector palette as part 01's local multiplication view.
  a,b=self.pair(1.6,3.8);left=circle_samples(a,lambda t:.65*np.exp(1j*t),INPUT);right=circle_samples(b,lambda t:.65*np.exp(1j*t),INPUT)
  self.show(left,right,vec(a,.65,INPUT),vec(a,.65j,GOLD),eq(r'\Delta f\approx f\prime(z)\Delta z',y=2.55,size=35))
  self.to(63);self.play(Transform(right,circle_samples(b,lambda t:1.3*np.exp(1j*(t+.65)),OUTPUT)),run_time=2.5)
  self.show(vec(b,1.3*np.exp(.65j),OUTPUT),vec(b,1.3j*np.exp(.65j),GOLD),eq(r'|\Delta f|\approx |f\prime(z)|\,|\Delta z|',y=-1.95,size=35,color=GOLD))
  self.note('이번에는 회전보다 길이의 배율 |f′(z)|에 주목한다')
 def s05(self):
  x=-3.6;R=1.9;a=ValueTracker(.65);eps=.18
  self.show(rim(x,R=R),eq(r'T_a(z)=\frac{z+a}{1+\overline a z}',x=3.4,y=1.9,size=34,width=6.9))
  original=Line(xy(-eps*1j,x,R=R),xy(eps*1j,x,R=R),color=INPUT,stroke_width=4)
  moved=always_redraw(lambda:ParametricFunction(lambda t:xy(mobius(1j*t,a.get_value()),x,R=R),t_range=[-eps,eps,.01],color=OUTPUT,stroke_width=4))
  self.show(original,moved,Dot(xy(0,x,R=R),color=INPUT),always_redraw(lambda:Dot(xy(a.get_value(),x,R=R),color=GOLD,radius=.06)),label('미소 길이의 이동',x=x,y=-1.95,size=25,color=MUTED))
  self.to(74);q=eq(r'T_a\prime(z)=\frac{(1+\overline a z)-\overline a(z+a)}{(1+\overline a z)^2}',x=3.4,y=.4,size=32,width=6.9);self.show(q)
  self.to(79);self.play(Transform(q,eq(r'T_a\prime(z)=\frac{1-|a|^2}{(1+\overline a z)^2}',x=3.4,y=.4,size=35,width=6.9)),run_time=1)
  self.show(eq(r'\overline a a=|a|^2',x=3.4,y=-.65,size=28,color=MUTED))
  self.to(82);self.show(eq(r'\boxed{T_a\prime(0)=1-|a|^2}',x=3.4,y=-1.55,size=38,color=GOLD,width=6.9));self.note('원점에서의 국소 축소 비율 · 유한한 도형의 직경과는 구분한다')
  self.to(86);self.wipe();ax=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=4.7,y_length=3.5,axis_config={'color':MUTED,'include_tip':False}).move_to(p(3.4,.4))
  graph=ax.plot(lambda r:1-r*r,x_range=[0,1],color=OUTPUT);a.set_value(0)
  self.show(rim(-3.6,R=1.8),ax,graph,eq(r'1-|a|^2',x=3.4,y=2.5,size=30,color=OUTPUT),always_redraw(lambda:Dot(ax.c2p(a.get_value(),1-a.get_value()**2),color=GOLD)),always_redraw(lambda:Line(xy(a.get_value(),-3.6,R=1.8)-UP*.23*(1-a.get_value()**2),xy(a.get_value(),-3.6,R=1.8)+UP*.23*(1-a.get_value()**2),color=OUTPUT,stroke_width=4)),run_time=.4)
  self.play(a.animate.set_value(.98),run_time=3.8,rate_func=linear)
 def s06(self):
  def row(y,factor,position):
   return VGroup(Line(p(-5.5,y),p(-5.5+3*factor,y),color=INPUT,stroke_width=5),Arrow(p(-1.6,y),p(.6,y),buff=0,color=GOLD),Line(p(1.7,y),p(4.7,y),color=OUTPUT,stroke_width=5),label(f'|a| = {position:.3f}',x=-5,y=y+.47,size=22,color=MUTED),label(f'×{1/factor:g}',x=-.5,y=y+.45,size=28,color=GOLD),label(f'{factor:g}  →  1',x=5.8,y=y,size=27,color=OUTPUT))
  self.show(row(1.8,1,0),row(.35,.5,np.sqrt(.5)))
  self.to(98);self.show(row(-1.1,.25,np.sqrt(.75)))
  self.to(102);self.note('원점 대비 상대적인 길이 보정 · 작은 길이의 극한에서 성립')
  self.to(105);self.show(eq(r'(1-|a|^2)\times\frac{1}{1-|a|^2}=1',y=-1.85,size=32,color=GOLD),run_time=.5)
 def s07(self):
  x=-3.6;R=1.9;a=ValueTracker(0);z=-.2+.2j;h=.13j
  self.show(rim(x,R=R),always_redraw(lambda:Dot(xy(mobius(z,a.get_value()),x,R=R),color=GOLD)),always_redraw(lambda:Line(xy(mobius(z,a.get_value()),x,R=R),xy(mobius(z+h,a.get_value()),x,R=R),color=OUTPUT,stroke_width=4)))
  density=VGroup(*[Annulus(inner_radius=R*k/14,outer_radius=R*(k+1)/14,stroke_width=0,fill_color=GOLD,fill_opacity=.015+.1*(k/14)**3).move_to(p(x,.25)) for k in range(14)])
  self.add(density);self.show(eq(r'ds=C\frac{|dz|}{1-|z|^2}',x=3.5,y=1.9,size=39,width=6.7),eq(r'\frac{|T_a\prime(z)|}{1-|T_a(z)|^2}=\frac{1}{1-|z|^2}',x=3.5,y=.4,size=31,width=7),label('이동 전후의 작은 길이를 같은 값으로',x=3.5,y=-.8,size=25,width=6.6,color=OUTPUT))
  self.play(a.animate.set_value(.7),run_time=4,rate_func=smooth);self.play(a.animate.set_value(-.35),run_time=3,rate_func=smooth)
  self.to(119);self.wipe();self.show(eq(r'\boxed{ds=\frac{2|dz|}{1-|z|^2}}',y=1.1,size=55,color=GOLD),label('푸앵카레 계량 · 표준 정규화: 곡률 −1',y=-.35,size=27,color=MUTED),label('점 사이의 거리는 이 길이 요소로 잰 경로 길이의 최솟값',y=-1.5,size=25,color=OUTPUT),run_time=.5)
 def s08(self):
  x=-3.6;R=1.95;self.show(rim(x,R=R),ruler(y=1.3,x=.1,width=6.1),label('화면상 같은 간격',x=3.2,y=1.95,size=26,color=INPUT))
  ticks=ruler(y=-.1,x=.1,width=6.1);self.show(ticks,label('새 거리에서 같은 간격',x=3.2,y=.6,size=26,color=OUTPUT));self.to(125);self.play(Transform(ticks,ruler(y=-.1,x=.1,width=6.1,hyper=True)),run_time=1)
  self.to(126);self.play(Create(rings(x,R=R)),run_time=3)
  self.to(130);segments=VGroup()
  for n in [0,2,5]:
   lo=np.tanh(n*.5/2);hi=np.tanh((n+1)*.5/2)
   segments.add(Line(xy(lo,x,R=R),xy(hi,x,R=R),color=GOLD,stroke_width=4))
  self.show(segments,eq(r'r_n=\tanh\frac{n\ell}{2},\quad\ell=0.5',x=3.2,y=-1.15,size=32,width=6.6),label('각 눈금 사이의 쌍곡 거리 = 0.5',x=3.2,y=-2.05,size=25,color=GOLD))
 def s09(self):
  x=-3.6;R=1.95;n=ValueTracker(0)
  self.show(rim(x,R=R),rings(x,R=R),always_redraw(lambda:Dot(xy(np.tanh(n.get_value()*.25),x,R=R),color=GOLD,radius=.075)))
  value=DecimalNumber(0,num_decimal_places=1,font_size=43,color=GOLD).move_to(p(3.2,1.1));value.add_updater(lambda m:m.set_value(n.get_value()*.5).move_to(p(3.2,1.1)))
  self.show(label('원점에서 걸어온 쌍곡 거리',x=3.2,y=1.9,size=27),value,label('한 걸음 = 0.5',x=3.2,y=.1,size=29,color=OUTPUT))
  self.to(139)
  for k in range(1,6):self.play(n.animate.set_value(k),run_time=.9,rate_func=linear)
  self.to(144);self.play(n.animate.set_value(8),run_time=2.7,rate_func=linear)
  self.to(148);self.note('화면의 틈은 작아져도, 같은 거리의 눈금은 계속 남아 있다',GOLD)
  # A separate finite Euclidean zoom follows the near-boundary walker; the whole disk stays visible.
  line=Line(p(.4,-1.05),p(6.2,-1.05),color=MUTED);zoom_ticks=VGroup()
  r0=np.tanh(6*.25)
  for k in range(6,19):
   loc=.4+5.8*(np.tanh(k*.25)-r0)/(1-r0)
   zoom_ticks.add(Line(p(loc,-1.15),p(loc,-.82),color=OUTPUT,stroke_width=1.2))
  self.show(line,zoom_ticks,label('경계 부근 확대 · 오른쪽 끝은 경계',x=3.3,y=-1.7,size=23,color=MUTED))
 def s10(self):
  self.show(label('화면상의 이동량',x=-3.9,y=2.4,size=28,color=INPUT),label('각 구간의 실제 쌍곡 거리',x=3.4,y=2.4,size=28,color=OUTPUT))
  rows=VGroup()
  for n in range(5):
   y=1.6-.66*n;lo=1-2.**(-n);hi=1-2.**(-(n+1));delta=float(distance(lo,hi))
   row=VGroup(Line(p(-6,y),p(-6+4.8*2**(-n),y),color=INPUT,stroke_width=4),label(f'1/{2**(n+1)}',x=-.3,y=y,size=23,color=INPUT),label(f'{delta:.4f}',x=3.4,y=y,size=27,color=OUTPUT))
   rows.add(row);self.show(row,run_time=.3)
  self.to(157);self.note('rₙ = 1 − 2⁻ⁿ  ·  경계까지의 화면 간격을 계속 반으로')
  self.to(161);self.wipe();x=-4;R=1.7;r=ValueTracker(.5)
  self.show(rim(x,R=R),always_redraw(lambda:Dot(xy(r.get_value(),x,R=R),color=GOLD)),eq(r'\Delta r\ \longrightarrow\ 0',x=3.3,y=1.8,size=37,color=INPUT),eq(r'\lambda(r)=\frac{2}{1-r^2}\ \longrightarrow\ \infty',x=3.3,y=.35,size=36,color=GOLD,width=7),run_time=.5)
  self.play(r.animate.set_value(.98),run_time=3.5,rate_func=smooth)
  self.to(166);self.show(eq(r'\Delta d_n=\log\frac{2^{n+2}-1}{2^{n+1}-1}>\log2',x=3.3,y=-1.3,size=32,color=OUTPUT,width=7));self.note('각 반분 구간의 실제 거리 · ln 2보다 크고 그 값에 수렴한다')
 def s11(self):
  self.show(eq(r'\frac12+\frac14+\frac18+\cdots=1',y=1.8,size=43,color=INPUT),label('유한한 화면상의 이동',y=.9,size=28,color=INPUT))
  self.to(175);self.show(eq(r'\sum_{n=0}^{\infty}\Delta d_n\ \geq\ \sum_{n=0}^{\infty}\log2=\infty',y=-.25,size=39,color=OUTPUT),run_time=.5)
  self.to(180);self.show(label('경계까지의 거리: ∞',y=-1.65,size=37,color=GOLD));self.note('경계는 원판 안의 점이 아니며, 유한한 쌍곡 거리로 도달할 수 없다')
 def s12(self):
  x=-3.4;R=2.1;self.show(rim(x,R=R))
  for a in [0,.55,.82,.95]:self.show(hcircle(a,.16,x=x,R=R),Dot(xy(a,x,R=R),radius=.035,color=GOLD),run_time=.3)
  self.show(eq(r'R_h=2\operatorname{artanh}(0.16)',x=3.5,y=1.6,size=35,width=6.6),label('쌍곡 반지름이 모두 같은 원',x=3.5,y=.4,size=29,width=6.7,color=OUTPUT),label('화면상의 중심과 쌍곡 중심은 다를 수 있다',x=3.5,y=-.7,size=23,width=6.4,color=MUTED))
  self.to(189);self.wipe();pattern=DiskPattern(x=0,y=.25,R=2.15);self.show(rim(R=2.15),pattern,run_time=1.1);self.note('모든 원은 같은 쌍곡 반지름 · 원의 배치 패턴이며 엄밀한 타일링은 아님')
  self.to(193);self.show(eq(r'T_a^{-1}(z)=\frac{z-a}{1-\overline a z}',x=4.9,y=1.4,size=31,width=4.6),label('관찰자를 중심으로 옮기는 이동',x=4.9,y=.25,size=23,width=4.5,color=OUTPUT),eq(r'a:0\longrightarrow0.65',x=4.9,y=-.7,size=29,color=GOLD,width=4.5),run_time=.5)
  self.play(UpdateFromAlphaFunc(pattern,lambda m,a:m.set_observer(.65*smooth(a))),run_time=5,rate_func=linear)
  self.to(199);self.play(Transform(self.title,label('푸앵카레 원판  ·  Poincaré Disk',y=self.head_y,size=34)),run_time=.5)
 def s13(self):
  x=-3.5;R=1.95;a=ValueTracker(0);z=-.4+.1j;w=.25+.25j
  self.show(rim(x,R=R),always_redraw(lambda:disk_grid(a.get_value(),x=x,R=R)),always_redraw(lambda:Dot(xy(mobius(z,a.get_value()),x,R=R),color=INPUT)),always_redraw(lambda:Dot(xy(mobius(w,a.get_value()),x,R=R),color=GOLD)),label('이동을 정하면, 그에 맞는 거리',x=3.5,y=1.7,size=29,width=6.5,color=GOLD))
  self.to(206);self.show(eq(r'd(T_a(z),T_a(w))=d(z,w)',x=3.5,y=.3,size=32,width=7,color=OUTPUT));self.play(a.animate.set_value(.7),run_time=4,rate_func=smooth)
  self.to(212);self.wipe();self.show(rim(-3.5,R=1.8,c=INPUT),disk_grid(0,x=-3.5,R=1.8),rim(3.5,R=1.8,c=OUTPUT),rings(3.5,R=1.8),eq(r'ds=|dz|',x=-3.5,y=-1.95,size=34,color=INPUT),eq(r'ds=\frac{2|dz|}{1-|z|^2}',x=3.5,y=-1.95,size=32,color=OUTPUT),label('같은 점들',y=2.6,size=29,color=GOLD),run_time=.5)
 def s14(self):
  a=plane(2,4.05,x=-3.5);v=vec(a,1,INPUT);self.show(a,v,eq(r'z\longmapsto az',x=3.5,y=1.2,size=43,color=INPUT),label('회전과 확대 · 축소',x=3.5,y=-.1,size=30))
  self.play(Transform(v,vec(a,1.7*np.exp(.65j),OUTPUT)),run_time=2)
  self.to(224);self.wipe();a,b=self.pair(1.6,3.4);self.show(circle_samples(a,lambda t:.65*np.exp(1j*t),INPUT),circle_samples(b,lambda t:1.1*np.exp(1j*(t+.65)),OUTPUT),eq(r'\Delta f\approx f\prime(z)\Delta z',y=2.45,size=36,color=GOLD),run_time=.5)
  self.to(228);self.wipe();boundary=Circle(radius=1.5,color=INPUT).move_to(p(-3.5,.3));self.show(boundary,Dot(p(-3.5,.3),color=GOLD),*[DashedLine(boundary.point_at_angle(t),p(-3.5,.3),color=INPUT,stroke_width=1,dash_length=.1) for t in np.linspace(0,TAU,12,endpoint=False)],torus(3.5,.3,.9),run_time=.5)
  self.to(233);self.wipe();pattern=DiskPattern(x=-3.4,y=.25,R=2.05);self.show(rim(-3.4,R=2.05),pattern,eq(r'|T_a\prime(0)|=1-|a|^2',x=3.5,y=1.4,size=36,color=GOLD,width=6.6),eq(r'ds=\frac{2|dz|}{1-|z|^2}',x=3.5,y=-.2,size=41,color=OUTPUT,width=6.6),run_time=.5)
  self.to(238.2);self.wipe();last=DiskPattern(x=-3.4,y=.25,R=2.05,observer=.25)
  self.show(rim(-3.4,R=2.05),last,label('우리는 수를 연구하기 시작했지만,',x=3.4,y=1.1,size=28,width=6.8),label('어느 순간 공간을 연구하고 있었습니다.',x=3.4,y=-.1,size=29,color=OUTPUT,width=6.8),run_time=.4)
  self.play(UpdateFromAlphaFunc(last,lambda m,a:m.set_observer(.25+.03*a)),run_time=4,rate_func=linear)
