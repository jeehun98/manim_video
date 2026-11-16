"""One sine curve, local derivative data, and exact Taylor polynomials."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from episodes.taylor01_local_geometry import tex_compat
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text
from episodes.taylor01_local_geometry.model import polynomial,derivative
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BLUE,ORANGE,TEAL,PURPLE,GOLD,MUTED='#80A8FF','#F1B66D','#43D3C4','#BD9BFA','#FFD477','#77849C'
class TaylorGeometry(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup();self.offset=self.info['start']
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  테일러 전개의 기하학',y=7.15,size=18,color=MUTED))
 def graph(self,a=1,n=None,xr=(-.7,2.7),yr=(-1.6,1.6),original=True):
  ax=Axes(x_range=[*xr,1],y_range=[*yr,1],x_length=7,y_length=4.4,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,1.5,0])
  g=VGroup(ax)
  def path(fn,color,opacity=1):
   xs=np.linspace(*xr,601);ys=fn(xs);mask=(ys>=yr[0]+.015)&(ys<=yr[1]-.015);pieces=VGroup();cuts=np.split(np.arange(len(xs)),np.where(np.diff(mask.astype(int))!=0)[0]+1)
   for ids in cuts:
    if len(ids)>1 and mask[ids[0]]:
     pieces.add(VMobject(stroke_color=color,stroke_width=3.5,stroke_opacity=opacity).set_points_as_corners([ax.c2p(x,y) for x,y in zip(xs[ids],ys[ids])]))
   return pieces
  if original:g.add(path(np.sin,BLUE))
  if n is not None:g.add(path(lambda x:polynomial(x,a,n),[GOLD,ORANGE,TEAL,PURPLE,PURPLE,PURPLE,PURPLE,PURPLE][n]))
  g.add(DashedLine(ax.c2p(a,0),ax.c2p(a,np.sin(a)),color=TEAL,stroke_width=1.2),Dot(ax.c2p(a,np.sin(a)),radius=.075,color=TEAL))
  return g,ax
 def base(self,a=1,n=None,xr=(-.7,2.7),yr=(-1.6,1.6),original=True):
  self.g,self.ax=self.graph(a,n,xr,yr,original);self.add(self.g)
  self.legend=VGroup(text('원본 곡선',x=-2.35,y=-1.3,size=21,color=BLUE),text('기준점 a = '+str(a),x=1.9,y=-1.3,size=21,color=TEAL));self.show(self.legend,run_time=.3)
 def change(self,a=1,n=None,xr=(-.7,2.7),yr=(-1.6,1.6),duration=1.5,original=True):
  new,ax=self.graph(a,n,xr,yr,original);self.play(Transform(self.g,new),run_time=duration);self.ax=ax
  if hasattr(self,'legend'):self.legend[1].become(text('기준점 a = '+str(a),x=1.9,y=-1.3,size=21,color=TEAL))
 def s01(self):
  self.g,self.ax=self.graph(xr=(-4,5));self.play(Create(self.g),run_time=2)
  self.to(4);self.formulas(r'P=(a,f(a))',colors=[TEAL]);self.change(duration=2)
  self.to(9);self.note_at('한 점의 정보 → 그 주변의 곡선',color=TEAL,size=30)
 def s02(self):
  self.base();self.to(16);self.play(Indicate(self.g[-1],color=TEAL),run_time=.7)
  self.to(18);self.formulas(r'P=(a,f(a))',r'P_0(x)=f(a)',colors=[TEAL,GOLD])
  self.to(21);self.change(n=0,original=False);self.note_at('같은 점을 지나는 곡선은 무수히 많다',size=27)
  self.legend[0].become(text('가능한 곡선들',x=-2.35,y=-1.3,size=21,color=BLUE))
  candidates=VGroup()
  for k in [-.65,.65]:
   xs=np.linspace(.05,1.95,151);ys=np.sin(1)+k*(xs-1)**2
   candidates.add(VMobject(stroke_color=BLUE,stroke_width=2,stroke_opacity=.4).set_points_as_corners([self.ax.c2p(x,y) for x,y in zip(xs,ys)]))
  self.show(candidates)
 def s03(self):
  self.base();self.formulas(r'f^{\prime}(a)=\text{slope}')
  self.to(29);p=self.ax.c2p(1,np.sin(1));q=self.ax.c2p(1.65,np.sin(1)+.65*np.cos(1));corner=np.array([q[0],p[1],0])
  triangle=VGroup(Line(p,corner,color=GOLD),Line(corner,q,color=GOLD));self.show(triangle)
  self.formulas(r'\frac{\Delta y}{\Delta x}\longrightarrow f^{\prime}(a)',colors=[GOLD])
  self.to(35);self.drop(triangle);self.change(n=1,duration=2);self.formulas(r'P_1(x)=f(a)+f^{\prime}(a)(x-a)',colors=[ORANGE]);self.note_at('함수값과 기울기를 동시에 맞춘다',color=ORANGE,size=27)
  self.to(41);self.note_at('일차 근사 · 접선',color=ORANGE,size=30)
 def s04(self):
  self.base(n=1);self.formulas(r'P_1^{\prime}(x)=f^{\prime}(a)\quad\text{constant}',colors=[ORANGE])
  self.to(45);errors=VGroup()
  for x in [.1,.35,1.65,2.1]:errors.add(Line(self.ax.c2p(x,np.sin(x)),self.ax.c2p(x,polynomial(x,1,1)),color=GOLD,stroke_width=3))
  self.play(Create(errors),run_time=1.5);self.note_at('접선의 기울기는 일정 · 곡선의 기울기는 변화',size=25)
  self.to(50);self.play(Indicate(errors,color=GOLD),run_time=1)
 def s05(self):
  self.base(n=1);self.formulas(r'f^{\prime\prime}(a)=\frac{d}{dx}f^{\prime}(x)\big|_{x=a}',colors=[TEAL])
  self.to(56);self.note_at('이차 미분 = 기울기의 변화율',color=TEAL,size=28)
  tangents=VGroup()
  for x in [.45,1,1.55]:
   tangents.add(Line(self.ax.c2p(x-.18,np.sin(x)-.18*np.cos(x)),self.ax.c2p(x+.18,np.sin(x)+.18*np.cos(x)),color=TEAL,stroke_width=5))
  self.show(tangents)
  self.to(59);self.drop(tangents);self.change(n=2,duration=2.5)
  self.formulas(r'P_2(x)=f(a)+f^{\prime}(a)h+\frac{f^{\prime\prime}(a)}{2!}h^2',r'h=x-a',colors=[TEAL,WHITE]);self.note_at('함수값 · 기울기 · 기울기의 변화',color=TEAL,size=27)
  self.to(68);self.play(Indicate(self.form[0],color=TEAL),run_time=1)
 def s06(self):
  self.base(n=2);self.formulas(r'P_n(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k',colors=[PURPLE])
  self.note_at('2차 → 3차 → 4차',color=PURPLE,size=30)
  self.change(n=3,duration=1.8);self.to(73);self.change(n=4,duration=2)
  self.to(77);self.note_at('왜 미분값을 계수로 쓸 수 있을까?',color=GOLD,size=29)
 def s07(self):
  self.base(n=4);self.formulas(r'P(x)=c_0+c_1h+c_2h^2+c_3h^3+\cdots',r'h=x-a',colors=[PURPLE,WHITE])
  self.to(83);self.formulas(r'P^{\prime}(x)=c_1+2c_2h+3c_3h^2+\cdots',r'P^{\prime\prime}(x)=2c_2+6c_3h+\cdots',colors=[ORANGE,TEAL])
  self.to(87);self.formulas(r'P^{(n)}(a)=n!\,c_n',r'c_n=\frac{f^{(n)}(a)}{n!}',colors=[GOLD,TEAL]);self.note_at('미분한 뒤 x=a, 즉 h=0을 대입',color=GOLD,size=28)
 def s08(self):
  self.base(n=3);chain=VGroup(*[eq(s,y=3.9-i*.65,size=40,color=GOLD) for i,s in enumerate([r'x^3',r'\downarrow\;d/dx',r'3x^2',r'\downarrow\;d/dx',r'6x',r'\downarrow\;d/dx',r'6=3!'])]);self.drop(self.g);self.drop(self.legend);self.show(chain)
  self.to(97);self.formulas(r'\frac{d^3}{dx^3}\big[c_3(x-a)^3\big]=6c_3',r'c_3=\frac{f^{(3)}(a)}{6}=\frac{f^{(3)}(a)}{3!}',colors=[GOLD,TEAL])
  self.to(103);self.note_at('n번 미분하면 생기는 n!을 나눈다',color=GOLD,size=28)
 def s09(self):
  self.base();self.formulas(r'f(x)=\sin x',colors=[BLUE]);self.note_at('같은 곡선, 기준점만 이동',color=TEAL,size=28)
  self.to(109);self.change(a=0,xr=(-3,3),duration=.8)
  self.to(110);self.formulas(r'f(0)=0,\quad f^{\prime}(0)=1,\quad f^{\prime\prime}(0)=0',r'P_1(x)=x',colors=[BLUE,ORANGE]);self.change(a=0,n=1,xr=(-3,3),duration=2)
  self.note_at('기준점 a = 0 · 원점에서 전개',color=TEAL,size=27)
 def s10(self):
  self.base(a=0,n=1,xr=(-3,3));self.formulas(r'P_1(x)=x',colors=[ORANGE]);self.note_at('원본 sin x는 그대로 · 근사식만 바뀐다',size=25)
  self.change(a=0,n=3,xr=(-3,3),duration=2.3);self.formulas(r'P_3(x)=x-\frac{x^3}{3!}',colors=[PURPLE])
  self.to(122);self.change(a=0,n=5,xr=(-3,3),duration=2.5);self.formulas(r'P_5(x)=x-\frac{x^3}{3!}+\frac{x^5}{5!}',colors=[PURPLE])
  self.to(126);self.note_at('한 항씩 보완하며 원래 곡선에 가까워진다',color=PURPLE,size=26)
 def s11(self):
  self.base(a=0,n=5,xr=(-3,3));self.formulas(r'f(0),\ f^{\prime}(0),\ f^{\prime\prime}(0),\ldots',r'\Downarrow\quad c_k=\frac{f^{(k)}(0)}{k!}',colors=[TEAL,PURPLE])
  self.to(135);self.note_at('한 점의 값 · 변화율 · 변화율의 변화',color=TEAL,size=26);self.play(Indicate(self.g[-1],color=TEAL),run_time=1)
  self.show(text('국소 정보 → 다항식 → 주변의 형태',y=-4.2,size=26,color=PURPLE))
 def s12(self):
  self.base(a=0,n=1,xr=(-3,3));self.formulas(r'0<|h|<1:\quad |h|^5<|h|^3<|h|',colors=[GOLD]);self.note_at('고정된 유한 차수에서 h → 0',size=25)
  self.to(146);self.change(a=0,n=1,xr=(-.6,.6),yr=(-.65,.65),duration=2.5)
  self.to(149);self.formulas(r'\sin x\approx x',r'|\sin x-x|\leq\frac{|x|^3}{3!}',colors=[ORANGE,GOLD]);self.note_at('가로·세로를 함께 확대 · 같은 함수, 같은 접선',size=24)
  self.show(text('x=0.5: 오차 ≈ 0.0206',x=-1.85,y=-4.2,size=21,color=GOLD,width=3.4),text('x=0.1: 오차 ≈ 0.000167',x=1.85,y=-4.2,size=21,color=TEAL,width=3.4))
 def s13(self):
  self.base(a=0,n=1,xr=(-.6,.6),yr=(-.65,.65));self.change(a=0,n=1,xr=(-3,3),duration=1.5)
  self.formulas(r'\text{local approximation}\;\neq\;\text{global equality}',colors=[GOLD]);self.note_at('국소적인 근사 ≠ 모든 구간에서 정확한 일치',size=25,color=GOLD)
  self.show(text('sin x의 무한급수는 모든 실수에서 수렴',y=-3.3,size=23,color=BLUE),text('일반 매끄러운 함수는 무한급수로도 복원되지 않을 수 있음',y=-4.05,size=20,color=MUTED,width=7.6))
 def s14(self):
  self.base(a=0,n=1,xr=(-3,3));self.formulas(r'P_1\ \longrightarrow\ P_3\ \longrightarrow\ P_5\ \longrightarrow\ P_7',colors=[PURPLE])
  for n in [3,5,7]:self.change(a=0,n=n,xr=(-3,3),duration=1.4)
  self.to(168);self.change(a=0,n=7,xr=(-1,1),yr=(-1.1,1.1),duration=1.5)
  self.note_at('한 점의 정보로, 그 주변의 구조를 이해한다',size=28,color=TEAL)
  self.formulas(r'f(a+h)\approx f(a)+f^{\prime}(a)h+\frac{f^{\prime\prime}(a)}{2!}h^2+\cdots',colors=[TEAL])
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
