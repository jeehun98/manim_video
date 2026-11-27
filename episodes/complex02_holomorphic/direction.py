"""170 seconds, equal-unit complex coordinates and exact supplied narration."""
import json
import os
from pathlib import Path
import numpy as np
from manim import *
import longforms.qcs01_speed.direction as shared
from episodes.complex01_rotation_derivative.direction import ComplexScene,plane,pt,vec,eq,label,p,L
HERE=Path(__file__).resolve().parent
assets=HERE.parents[1]/'media'/'complex02_assets'/os.environ.get('COMPLEX02_ASSET_KEY',f'check_{os.getpid()}')
for kind in ['Tex','texts']:(assets/kind).mkdir(parents=True,exist_ok=True)
config.tex_dir=str(assets/'Tex')
config.text_dir=str(assets/'texts')
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1019'
INK,BLUE,GOLD,GREEN,RED,PURPLE,MUTED='#E5E7EB','#60A5FA','#FBBF24','#34D399','#F87171','#A78BFA','#8D9BB6'

def grid(r=2,size=5.8,x=0,y=.4):
 a=NumberPlane(x_range=[-r,r,1],y_range=[-r,r,1],x_length=size,y_length=size,
  background_line_style={'stroke_color':'#334155','stroke_width':1,'stroke_opacity':.6},
  axis_config={'stroke_color':MUTED,'stroke_width':1.3,'include_ticks':False,'include_tip':False}).move_to(p(x,y))
 return a

class AnalysisScene(ComplexScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.mobjects[-1])
  self.add(label('수학적 구조  /  복소해석학',y=7.15,size=18,color=MUTED))
 def wipe(self):
  self.clear_body()
 def s01(self):
  self.show(eq(r'f:\mathbb R\to\mathbb R',y=2.6,color=BLUE),eq(r'f:\mathbb C\to\mathbb C',y=.5,color=GOLD))
  self.note('함수의 입력이 직선에서 평면으로')
  self.to(9);self.wipe();a=grid(3,5.8,y=.2)
  self.show(a.x_axis,Dot(pt(a,2),color=BLUE),eq('x=2',y=3.9,color=BLUE))
  self.to(13);self.play(Create(a.y_axis),FadeIn(a.background_lines),run_time=1)
  d=Dot(pt(a,2),color=GOLD);self.add(d);self.play(d.animate.move_to(pt(a,2+1j)),run_time=1.3)
  self.show(vec(a,2+1j,GOLD),eq(r'z=2+i',y=-3.15,color=GOLD));self.note('실수부 2  ·  허수부 1')
 def s02(self):
  a=grid(2,3.1,-1.95,1);b=grid(2,3.1,1.95,1)
  self.show(a.x_axis,b.x_axis,eq('f(x)=x^2',y=3.9,color=INK))
  d=Dot(pt(a,1),color=BLUE);e=Dot(pt(b,1),color=GOLD);self.show(d,e)
  self.to(21);self.play(FadeIn(a.y_axis),FadeIn(b.y_axis),FadeIn(a.background_lines),FadeIn(b.background_lines),run_time=.7)
  self.play(d.animate.move_to(pt(a,1+1j)),e.animate.move_to(pt(b,2j)),run_time=.6)
  self.show(eq('f(z)=z^2',y=3.1,color=GREEN),Arrow(p(-.35,1),p(.35,1),buff=0,color=INK),vec(a,1+1j),vec(b,2j,GOLD))
  self.show(eq('1+i',x=-1.95,y=-1.1,size=27,color=BLUE),eq('2i',x=1.95,y=-1.1,size=27,color=GOLD))
  self.to(24);g=VGroup()
  for k in np.linspace(-1,1,7):
   for vertical in [False,True]:
    g.add(ParametricFunction(lambda t,k=k,v=vertical:pt(a,complex(k,t) if v else complex(t,k)),t_range=[-1,1,.05],color=BLUE,stroke_width=1.4))
  self.show(g,run_time=.3)
  target=VGroup()
  for k in np.linspace(-1,1,7):
   for vertical in [False,True]:
    target.add(ParametricFunction(lambda t,k=k,v=vertical:pt(b,(complex(k,t) if v else complex(t,k))**2),t_range=[-1,1,.05],color=GOLD if vertical else BLUE,stroke_width=1.4))
  self.play(Transform(g,target),run_time=2.3);self.note('점의 대응을 모으면 평면의 변환')
  self.to(28);self.show(eq(r'\frac{f(z+h)-f(z)}h\quad h\to0',y=-2.7,size=32,color=GREEN))
 def s03(self):
  a=Axes(x_range=[-1,3,1],y_range=[-1,8,2],x_length=6.3,y_length=5.4,tips=False).move_to(p(0,.8))
  curve=a.plot(lambda x:x*x,x_range=[-.7,2.7],color=BLUE);h=ValueTracker(1.2)
  q=always_redraw(lambda:Dot(a.c2p(1+h.get_value(),(1+h.get_value())**2),color=GOLD))
  line=always_redraw(lambda:Line(a.c2p(.4,1+(.4-1)*(2+h.get_value())),a.c2p(2.4,1+(2.4-1)*(2+h.get_value())),color=GOLD))
  self.show(a,curve,Dot(a.c2p(1,1),color=BLUE),q,line)
  self.show(eq(r'\frac{(1+h)^2-1}{h}=2+h',y=-2.7,size=33));self.note('기준점 x=1  ·  두 점 사이의 변화율')
  self.play(h.animate.set_value(.08),run_time=4)
  self.to(40);self.play(h.animate.set_value(-.7),run_time=1.2);self.play(h.animate.set_value(-.03),run_time=3)
  self.show(eq(r'h\to0^-\quad 2\quad h\to0^+',y=4.2,size=32,color=GREEN))
  self.to(47);self.note('직선의 두 방향에서 평면의 모든 경로로')
 def s04(self):
  a=grid(2,5.4,y=1);self.show(a,Dot(pt(a,0),color=GOLD),eq(r'f\prime(z_0)=\lim_{h\to0}\frac{f(z_0+h)-f(z_0)}h',y=-2.65,size=31))
  arrows=VGroup(*[Arrow(pt(a,1.7*np.exp(1j*t)),pt(a,.2*np.exp(1j*t)),buff=0,color=BLUE,stroke_width=2) for t in np.linspace(0,TAU,12,endpoint=False)])
  self.play(LaggedStart(*[GrowArrow(v) for v in arrows],lag_ratio=.08),run_time=2)
  self.play(Create(ParametricFunction(lambda t:pt(a,(1.8-t)*np.exp(3j*t)),t_range=[0,1.78,.02],color=PURPLE)),run_time=2)
  self.note('직선뿐 아니라 곡선 경로도 모두 포함')
  self.to(56);self.wipe();a=grid(1.4,3.1,-1.95,1);b=grid(1.4,3.1,1.95,1)
  self.show(a,b,eq(r'f(z)=z^2,\ z_0=1+i',y=3.8,size=32),label('h → 0',x=-1.95,y=-1.1,size=27,color=BLUE),label('차분비 → 2+2i',x=1.95,y=-1.1,size=25,color=GREEN))
  rays=VGroup(*[Line(pt(a,0),pt(a,np.exp(1j*t)),color=BLUE) for t in np.linspace(0,TAU,8,endpoint=False)])
  dots=VGroup(*[Dot(pt(b,.8*np.exp(1j*t)),radius=.06,color=GREEN) for t in np.linspace(0,TAU,8,endpoint=False)])
  self.show(rays,dots);self.play(rays.animate.scale(.05,about_point=pt(a,0)),*[d.animate.move_to(pt(b,0)) for d in dots],run_time=2.4)
  self.show(eq(r'\frac{(z_0+h)^2-z_0^2}{h}=2z_0+h',y=-2.65,size=31));self.note('오른쪽 좌표계의 중심은 2+2i')
 def s05(self):
  a=grid(2,5.5,y=.7);self.show(a,eq(r'f(z)=\overline z',y=4.1,color=GOLD))
  v=vec(a,1+1j);d=Dot(pt(a,1+1j),color=BLUE);self.show(v,d,eq(r'x+iy\longmapsto x-iy',y=-2.8,size=34));self.note('실수축은 고정 · 허수부의 부호만 반전')
  self.to(69);self.play(Transform(v,vec(a,1-1j,GOLD)),d.animate.move_to(pt(a,1-1j)).set_color(GOLD),run_time=2)
 def s06(self):
  a=grid(1.3,3.1,-1.95,1);b=grid(1.3,3.1,1.95,1);self.show(a,b)
  self.show(label('입력 변화량 h',x=-1.95,y=3.1,size=24,color=BLUE),label('차분비',x=1.95,y=3.1,size=24,color=GOLD))
  t=ValueTracker(0);r=ValueTracker(1)
  v=always_redraw(lambda:vec(a,r.get_value()*np.exp(1j*t.get_value()),BLUE))
  d=always_redraw(lambda:Dot(pt(b,np.exp(-2j*t.get_value())),radius=.1,color=GOLD))
  self.show(v,d,Circle(radius=3.1/2.6,color=MUTED,stroke_opacity=.4).move_to(pt(b,0)),eq(r'\frac{\overline h}h=e^{-2i\theta}',y=-2.4,size=39))
  self.show(eq(r'h=t:\ +1',x=-1.8,y=-1.25,size=27,color=GREEN))
  self.play(t.animate.set_value(PI/2),r.animate.set_value(.6),run_time=2)
  self.show(eq(r'h=it:\ -1',x=1.8,y=-1.25,size=27,color=RED));self.to(81)
  self.play(t.animate.set_value(2.5*PI),r.animate.set_value(.045),run_time=4,rate_func=linear)
  self.note('h는 0으로 · 차분비는 단위원 위에 남는다',RED)
 def s07(self):
  self.show(eq('f(x+iy)=u(x,y)+iv(x,y)',y=3.6,size=34))
  self.to(90);self.show(eq(r'h=t:\quad u_x+i v_x',y=1.6,size=36,color=BLUE),eq(r'h=it:\quad v_y-i u_y',y=.1,size=36,color=GOLD))
  self.note('두 방향의 차분비가 같아야 한다')
  self.to(96);self.show(eq(r'u_x=v_y\qquad u_y=-v_x',y=-2.1,size=36,color=GREEN))
  self.to(99);self.wipe();a=grid(1.5,3.1,-1.95,.8);b=grid(1.5,3.1,1.95,.8)
  sq=lambda a,c:Polygon(*[pt(a,z) for z in [0,.8,.8+.8j,.8j]],color=c,fill_opacity=.15)
  s=sq(a,BLUE);q=sq(b,GREEN);self.show(a,b,s,q,eq(r'J_f=\begin{pmatrix}a&-b\\b&a\end{pmatrix}',y=3.7,size=32))
  self.play(Rotate(q,PI/5,about_point=pt(b,0)),run_time=1.5);self.note('미분값 ≠ 0: 국소적으로 회전과 균일 확대')
  self.to(104);self.show(label('전단 ×   비균일 확대 ×',y=-1.6,size=28,color=RED),label('복소수 곱셈 ✓',y=-2.5,size=31,color=GREEN));self.note('실수 전미분가능 가정하에 CR과 동치 · 미분값 0도 허용')
 def s08(self):
  self.show(label('더 강한 조건이 만드는 성질',y=3.6,size=34,color=GREEN))
  self.to(114)
  for y,f,s,c in [(1.8,lambda x:x*abs(x),r'f(x)=x|x|',BLUE),(-.1,lambda x:2*abs(x),r'f\prime(x)=2|x|',GOLD)]:
   a=Axes(x_range=[-1,1,1],y_range=[-1,2,1],x_length=4.4,y_length=1.5,tips=False).move_to(p(0,y))
   self.show(a,a.plot(f,x_range=[-1,1,.03],color=c),eq(s,x=0,y=y+1.0,size=25,color=c),run_time=.4)
  self.show(eq(r'f^{\prime\prime}(0)\ \mathrm{does\ not\ exist}',y=-2.65,size=29,color=RED));self.note('1차 미분은 존재하지만 0에서 2차 미분 불가')
 def s09(self):
  a=grid(2,4.5,y=1.1);region=Circle(radius=2,color=GREEN,fill_opacity=.07).move_to(a)
  dots=VGroup(*[Dot(pt(a,x+1j*y),radius=.045,color=GREEN) for x in np.arange(-1.2,1.3,.4) for y in np.arange(-1.2,1.3,.4) if x*x+y*y<1.6])
  self.show(a,DashedVMobject(region),dots,label('열린 영역 Ω 전체에서 복소미분 가능',y=4.1,size=27,color=GREEN))
  self.show(eq(r'f\to f\prime\to f^{\prime\prime}\to\cdots\to f^{(n)}',y=-2.05,size=35,color=GREEN));self.note('한 점에서의 미분가능만으로는 보장되지 않는다')
 def s10(self):
  a=grid(1.2,5.4,y=.8);self.show(a,eq(r'f(z)=\frac1{1-z}',y=4.1,size=32))
  self.note('원과 내부를 포함하는 열린 영역에서 정칙')
  self.to(133);c=Circle(radius=1.575,color=PURPLE,fill_opacity=.07).move_to(pt(a,0));self.play(Create(c),run_time=1.5)
  self.show(eq(r'C:\ |\zeta|=0.7',y=-2.65,size=31,color=PURPLE),Dot(pt(a,.2+.15j),color=GOLD),label('z',x=.8,y=1.5,size=25,color=GOLD))
  arc=Arc(radius=1.575,start_angle=.4,angle=.65,arc_center=pt(a,0),color=PURPLE).add_tip(tip_length=.14);self.show(arc)
 def s11(self):
  a=grid(1.2,3.3,x=-1.7,y=1.5);b=plane(1.6,2.8,x=2,y=1.5);c=Circle(radius=.9625,color=PURPLE,fill_opacity=.06).move_to(pt(a,0));z=.2+.15j
  self.show(a,b,c,Dot(pt(a,z),color=GOLD),eq(r'f(z)=\frac1{2\pi i}\oint_C\frac{f(\zeta)}{\zeta-z}\,d\zeta',y=-1.9,size=31),label('경계의 정보',x=-1.7,y=3.65,size=23,color=PURPLE),label('적분의 누적값',x=2,y=3.65,size=23,color=GREEN))
  ts=np.linspace(0,TAU,721);ws=.7*np.exp(1j*ts);integrand=ws/((1-ws)*(ws-z))/TAU
  sums=np.r_[0,np.cumsum((integrand[1:]+integrand[:-1])/2*np.diff(ts))]
  value=lambda theta:complex(np.interp(theta,ts,sums.real),np.interp(theta,ts,sums.imag))
  t=ValueTracker(0);d=always_redraw(lambda:Dot(pt(a,.7*np.exp(1j*t.get_value())),color=PURPLE));ray=always_redraw(lambda:DashedLine(pt(a,z),d.get_center(),color=BLUE))
  accumulated=always_redraw(lambda:Dot(pt(b,value(t.get_value())),color=GREEN,radius=.075))
  trace=ParametricFunction(lambda theta:pt(b,value(theta)),t_range=[0,TAU,.025],color=GREEN,stroke_width=2)
  self.show(d,ray,accumulated);self.play(t.animate.set_value(TAU),Create(trace),run_time=3.8,rate_func=linear)
  self.show(eq(r'f(0.2+0.15i)=1.20755+0.22642i',y=-2.9,size=24,color=GREEN));self.note('반시계방향 경계의 연속적인 함수값을 적분')
 def s12(self):
  for y,n in [(3.4,0),(1.5,1),(-.4,2),(-2.3,3)]:
   left='f(z)' if n==0 else r'f\prime(z)' if n==1 else r'f^{\prime\prime}(z)' if n==2 else r'f^{(n)}(z)'
   coeff='1' if n<2 else '2!' if n==2 else 'n!';power=str(n+1) if n<3 else 'n+1'
   self.show(eq(left+r'=\frac{'+coeff+r'}{2\pi i}\oint_C\frac{f(\zeta)}{(\zeta-z)^{'+power+r'}}\,d\zeta',y=y,size=30,color=PURPLE if n==0 else INK),run_time=.6)
   if n<3:self.wait(.5)
  self.note('경계 정보로 모든 차수의 미분값까지')
 def s13(self):
  self.show(eq(r'\frac1{1-z}=\sum_{k=0}^{\infty}z^k,\quad |z|<1',y=4.1,size=31,color=GOLD))
  a=grid(1,4.6,y=.9);self.show(a)
  zs=[r*np.exp(1j*t) for r in [.25,.5,.8] for t in np.linspace(0,TAU,12,endpoint=False)]
  base=VGroup(*[Dot(pt(a,z),radius=.048,color=GOLD) for z in zs]);self.show(base)
  # Compare actual complex outputs of f and Taylor polynomials on |z|<1.
  b=plane(5,4.6,y=.9);self.play(Transform(a,b),Transform(base,VGroup(*[Dot(pt(b,1/(1-z)),radius=.048,color=GOLD) for z in zs])),run_time=.5)
  approx=VGroup(*[Dot(pt(b,sum(z**k for k in range(2))),radius=.035,color=BLUE) for z in zs]);self.add(approx)
  tag=label('테일러 다항식 n=1',y=-2.4,size=26,color=BLUE);self.show(tag)
  for n in [5,20]:
   self.play(Transform(approx,VGroup(*[Dot(pt(b,sum(z**k for k in range(n+1))),radius=.035,color=BLUE) for z in zs])),Transform(tag,label(f'테일러 다항식 n={n}',y=-2.4,size=26,color=BLUE)),run_time=.7)
  self.note('금색: 실제 함수값 · 파랑: 다항식의 복소 출력')
 def s14(self):
  self.show(label('정칙함수',y=3.6,size=42,color=GREEN),eq(r'f:\Omega\to\mathbb C',y=2.2,size=35))
  self.show(label('열린 영역 Ω의 모든 점에서\n복소미분 가능한 함수',y=.4,size=32,color=INK))
  self.show(label('무한 번 미분 가능\n국소적으로 테일러 급수와 일치',y=-2,size=28,color=GREEN));self.note('정의와 그로부터 따라오는 성질')
 def s15(self):
  a=grid(2,3.5,y=2);self.show(a.x_axis,Dot(pt(a,1),color=BLUE))
  self.play(Create(a.y_axis),FadeIn(a.background_lines),run_time=.9)
  self.show(vec(a,1+1j),eq(r'\mathbb R\ \longrightarrow\ \mathbb C',y=4.4,size=34))
  self.show(label('같은 미분의 정의',y=-.5,size=32),Arrow(p(0,-1),p(0,-1.6),color=GREEN,buff=0),label('더 강한 조건',y=-2.1,size=33,color=GOLD),label('무한 미분 · 해석적 구조',y=-3.3,size=30,color=GREEN))
