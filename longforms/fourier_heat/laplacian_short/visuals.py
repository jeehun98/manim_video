"""Vertical educational layouts; analytic temperature, tangent, and Fourier modes."""
from pathlib import Path
import json,textwrap
import numpy as np
from manim import *
from mechanics import X,ALPHA,insulated,slope,steady,component,fourier
R=Path(__file__).resolve().parent
BG='#09111E';INK='#EAF0F7';MUTED='#8294AB';BLUE='#65B9EF';GOLD='#EDBC73';GREEN='#62D7B9';RED='#F1848B'
config.frame_width=9;config.frame_height=16;config.background_color=BG
TC={};EC={}
def tx(s,x=0,y=0,size=28,c=INK,w=7.7):
 key=(s,size,c,w)
 if key not in TC:
  o=Text(s,font='Malgun Gothic',font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  TC[key]=o
 return TC[key].copy().move_to([x,y,0])
def eq(s,x=0,y=0,size=42,c=INK,w=7.7):
 key=(s,size,c,w)
 if key not in EC:
  o=MathTex(s,font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  EC[key]=o
 return EC[key].copy().move_to([x,y,0])
def axes(y=0,h=3,w=6.8,xr=(0,1,.2),yr=(0,100,20),x=0):
 a=Axes(x_range=xr,y_range=yr,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a
def curve(a,x,y,c=GOLD,width=3):return VMobject(stroke_color=c,stroke_width=width,fill_opacity=0).set_points_as_corners([a.c2p(float(u),float(v)) for u,v in zip(x,y)])
def arrow(p,q,c=GOLD):return Arrow(p,q,buff=0,stroke_width=3,color=c,max_tip_length_to_length_ratio=.23)
def rod(y,vals,w=6.8):
 g=VGroup();n=48
 for j in range(n):
  v=float(vals[j]);c=interpolate_color(ManimColor(BLUE),ManimColor(RED),np.clip((v-15)/70,0,1))
  g.add(Rectangle(width=w/n+.008,height=.48,stroke_width=0,fill_color=c,fill_opacity=1).move_to([-w/2+w*(j+.5)/n,y,0]))
 return g
class HeatScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[];self.prepare()
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('삼각함수 · 열방정식 · 라플라스',0,7.25,26),Line([-3.9,6.75,0],[3.9,6.75,0],stroke_color=MUTED,stroke_opacity=.3))
  self.add(RoundedRectangle(width=8.3,height=1.85,corner_radius=.13,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-6.85,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  def update(m):m.submobjects=self.geometry(self.clock.get_value()).submobjects
  self.dynamic.add_updater(update)
  extra=[121.5,134.5,136,137.5]
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[x for x in extra if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=(round(b*config.frame_rate)-round(a*config.frame_rate))/config.frame_rate,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,indent=2),encoding='utf-8')
 def prepare(self):self.cache={}
 def update_text(self,t):
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  if line!=self.current:
   self.remove(self.caption);self.current=line
   self.caption=VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=line['start'],end=line['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1])))
  self.remove(self.static);self.static=self.labels(t);self.add(self.static)
  for m in self.static:assert m.get_left()[0]>-4.2 and m.get_right()[0]<4.2 and m.get_bottom()[1]>-5.65 and m.get_top()[1]<6.4,('label',self.index,t,m.get_center())
 def labels(self,t):
  i=self.index;g=VGroup();titles=['왜 하필 삼각함수일까?','열이 퍼지면 온도 곡선이 변한다','곡선의 기울기, 그리고 휘어짐','봉우리는 낮아지고 골짜기는 높아진다','열은 흘러도 온도는 일정할 수 있다','모든 공간 방향의 휘어짐을 더한다','두 번 미분해도 같은 함수의 형태','특정 함수에서는 미분이 곱셈으로','복잡한 곡선을 단순한 성분의 합으로']
  g.add(tx(titles[i-1],0,5.9,29,c=GOLD))
  if i==1:
   for y,s in [(4.5,'진동'),(1.1,'파동'),(-2.3,'온도 분포')]:g.add(tx(s,-2.8,y,24,c=MUTED,w=2))
   if t>=3:g.add(tx('현상을 설명하기 좋은 표현',0,-4.95,29,c=GREEN))
  elif i==2:
   g.add(tx('뜨거움',-2.8,3.9,24,c=RED,w=2),tx('차가움',2.8,3.9,24,c=BLUE,w=2),tx('양 끝 단열 · 내부에서 열이 재분배',0,-4.9,21,c=MUTED))
   if t>=23:g.add(eq(r'\frac{\partial T}{\partial t}=\alpha\frac{\partial^2T}{\partial x^2}',0,-2.7,48),tx('시간 변화',-1.8,-3.8,23,c=GOLD,w=3),tx('공간의 휘어짐',1.8,-3.8,23,c=BLUE,w=3))
  elif i==3:
   g.add(tx('위치 x',2.8,-.1,23,c=MUTED,w=2),tx('온도 T',-2.8,4.7,23,c=MUTED,w=2),tx('막대의 같은 위치와 연결',0,-4.6,23,c=MUTED))
   g.add(eq(r'\frac{dT}{dx}' if t<36 else r'\frac{d}{dx}\left(\frac{dT}{dx}\right)=\frac{d^2T}{dx^2}',0,-2.6,46,c=GREEN))
  elif i==4:
   g.add(tx('봉우리',-2.8,4.9,24,c=RED,w=2),tx('골짜기',-2.8,.1,24,c=BLUE,w=2))
   if t<59:
    g.add(eq(r'+\quad\longrightarrow\quad-',0,1.95,34,c=RED),eq(r'T_{xx}<0',2.6,3.9,30,c=RED,w=2.2),eq(r'-\quad\longrightarrow\quad+',0,-2.85,34,c=BLUE),eq(r'T_{xx}>0',2.6,-.9,30,c=BLUE,w=2.2))
   else:g.add(tx('주변으로 유출 → 냉각',0,1.65,25,c=RED),tx('주변에서 유입 → 가열',0,-3.15,25,c=BLUE),eq(r'J=-\kappa T_x',0,-4.7,33,c=GREEN))
  elif i==5:
   g.add(tx('양 끝 온도 고정 · 정상상태',0,4.8,23,c=MUTED),eq(r'T(x)=80-60x',0,1,36,c=BLUE),tx('같은 양 유입',-2.3,-1.6,24,c=GOLD,w=3.1),tx('같은 양 유출',2.3,-1.6,24,c=GOLD,w=3.1),eq(r'T_{xx}=0\quad\Rightarrow\quad\partial_tT=0',0,-3.9,39,c=GREEN))
   if t>=92:g.add(eq(r'\partial_tT=\alpha T_{xx}',0,-5,36))
  elif i==6:
   g.add(tx('2차원 온도 곡면 · 높이 = 온도',0,4.75,21,c=MUTED))
   if t<107:g.add(tx('x',2.9,1.2,24,c=BLUE,w=1),tx('y',-2.9,1.2,24,c=GREEN,w=1))
   else:g.add(tx('공간 방향 x · y · z',0,-.65,22,c=MUTED))
   f=r'\nabla^2T=\frac{\partial^2T}{\partial x^2}+\frac{\partial^2T}{\partial y^2}' if t<107 else r'\nabla^2T=\frac{\partial^2T}{\partial x^2}+\frac{\partial^2T}{\partial y^2}+\frac{\partial^2T}{\partial z^2}'
   g.add(eq(f,0,-2,40,w=7.5),tx('2차원 공간' if t<107 else '3차원 공간 · 직교좌표',0,-3.5,26,c=MUTED))
   if t>=111:g.add(tx('라플라스 작용소',0,-4.85,33,c=GREEN))
  elif i==7:
   if t<119:g.add(eq(r'\nabla^2\sin(kx)=?',0,-3.8,43,c=GREEN))
   elif t<124:
    f=r'\sin x\ \longrightarrow\ \cos x' if t<121.5 else r'\sin x\ \longrightarrow\ \cos x\ \longrightarrow\ -\sin x'
    g.add(eq(f,0,-3.8,37,c=GREEN))
   elif t<128:g.add(eq(r'\cos x\ \longrightarrow\ -\sin x\ \longrightarrow\ -\cos x',0,-3.8,36,c=GREEN))
   elif t<132:g.add(eq(r'f^{\prime\prime}=-f',0,-3.8,43,c=GREEN),tx('반전되어도 형태는 유지',0,-4.9,24,c=MUTED))
   else:
    k=1 if t<134.5 else 2 if t<136 else 3
    g.add(eq(r'\frac{d^2}{dx^2}\sin('+str(k)+r'x)=-'+str(k*k)+r'\sin('+str(k)+r'x)',0,-3.65,38,c=GREEN),tx('k: 공간 각파수 · 가로축 x',0,-4.85,22,c=MUTED))
   g.add(tx('원래 함수',-2.7,4.7,24,c=BLUE,w=2.5),tx('미분 결과',-2.7,.35,24,c=GOLD,w=2.5))
  elif i==8:
   g.add(tx('이차 미분',-2.05,4.3,27,c=BLUE,w=3),tx('상수 곱셈',2.05,4.3,27,c=GOLD,w=3),eq(r'\frac{d^2}{dx^2}\sin(2x)',-2,3.1,33,c=BLUE,w=3.4),eq(r'-4\sin(2x)',2,3.1,33,c=GOLD,w=3.4),eq(r'=',0,3.1,30),tx('두 결과가 정확히 일치',0,-.65,26,c=GREEN))
   if t>=145:g.add(tx('고유함수 · EIGENFUNCTION',0,-2.1,30,c=GREEN),eq(r'\nabla^2 f=\lambda f',0,-3.2,43))
   g.add(tx('특정 함수에 적용할 때의 관계',0,-4.35,23,c=MUTED),tx('고유함수의 선택은 영역·경계조건에 의존',0,-5.05,19,c=MUTED))
  elif i==9:
   g.add(tx('전체 온도 분포',0,4.8,23,c=GOLD),tx('양 끝 0으로 고정 · 기준 온도와의 차이',0,-5.2,19,c=MUTED),eq(r'k_n=n\pi/L',2.4,4.3,25,c=MUTED,w=2.2))
   if t<160:g.add(eq(r'T(x,0)=\sum_n a_n\sin(k_nx)',0,-3.7,37))
   elif t<164:g.add(eq(r'\partial_{xx}\sin(k_nx)=-k_n^2\sin(k_nx)',0,-3.7,35,c=GREEN))
   else:g.add(eq(r'T(x,t)=\sum_n a_ne^{-\alpha k_n^2t}\sin(k_nx)',0,-3.7,34,c=GREEN),tx('FOURIER SERIES',0,-4.55,26,c=GOLD))
  return g
 def geometry(self,t):
  i=self.index;g=VGroup()
  if i==1:
   for j,y in enumerate([3.5,.1,-3.3]):
    a=axes(y,1.6,5.5,(-np.pi,np.pi,1),(-1.2,1.2,.5),x=.55);x=np.linspace(-np.pi,np.pi,100);v=np.sin(x-t*.9) if j<2 else .65*np.sin(x)+.2*np.sin(3*x)
    g.add(a,curve(a,x,v,[GOLD,BLUE,RED][j]));g.add(Dot(a.c2p(.8,np.sin(.8-t*.9)),radius=.07,color=GREEN) if j<2 else VGroup())
  elif i==2:
   u=np.clip((t-19)/4,0,1)*1.2;g.add(rod(3.1,insulated(np.linspace(0,1,48),u)));a=axes(.5,2.8);g.add(a,curve(a,X,insulated(X,u)),curve(a,X,insulated(X,0),MUTED,1.2))
  elif i==3:
   a=axes(2.5,3.5);g.add(a,curve(a,X,insulated(X)));g.add(rod(-.8,insulated(np.linspace(0,1,48))))
   u=.12+.76*np.clip((t-32)/11,0,1);v=insulated(u);dx=.07
   g.add(Dot(a.c2p(u,v),radius=.075,color=GREEN),Line(a.c2p(u-dx,v-slope(u)*dx),a.c2p(u+dx,v+slope(u)*dx),color=GREEN,stroke_width=4),DashedLine(a.c2p(u,v),[a.c2p(u,v)[0],-.8,0],color=MUTED,stroke_width=1))
  elif i==4:
   xx=np.linspace(-1.45,1.45,90);amp=1 if t<59 else np.exp(-.12*(t-59))
   for y,sgn,c in [(3.45,1,RED),(-1.35,-1,BLUE)]:
    a=axes(y,2.4,5.5,(-1.5,1.5,1),(-1.2,1.2,.5));g.add(a,curve(a,xx,sgn*amp*np.cos(xx),c),Dot(a.c2p(0,sgn*amp),color=c,radius=.07))
    if t<59:
     u=-.8+1.6*((t-43)/7%1);v=sgn*np.cos(u);m=-sgn*np.sin(u);g.add(Line(a.c2p(u-.27,v-m*.27),a.c2p(u+.27,v+m*.27),color=GREEN,stroke_width=3))
    else:
     for side in [-1,1]:
      p=a.c2p(side*.6,sgn*amp*np.cos(.6));v=np.array([sgn*side*.65*amp,0,0]);g.add(arrow(p,p+v,c))
  elif i==5:
   a=axes(3,2.4);g.add(a,curve(a,X,steady(X),BLUE),rod(-.1,steady(np.linspace(0,1,48))))
   g.add(Rectangle(width=1.4,height=.9,fill_opacity=0,stroke_color=GREEN).move_to([0,-.1,0]))
   for xx in [-2.4,1.3]:g.add(arrow([xx,-.1,0],[xx+1.1,-.1,0],GOLD))
   phase=(t-71)%1
   for xx in np.arange(-3,3,.7):g.add(Dot([xx+.6*phase,-.1,0],radius=.035,color=INK))
  elif i==6:
   def p(x,y):return np.array([1.18*(x-y),2.2+.38*(x+y)+.6*(np.cos(x)+.7*np.cos(y)),0])
   z=np.linspace(-1.4,1.4,25)
   for v in np.linspace(-1.4,1.4,11):
    g.add(VMobject(stroke_color=BLUE,stroke_opacity=.55,stroke_width=1.4,fill_opacity=0).set_points_as_corners([p(u,v) for u in z]),VMobject(stroke_color=GREEN,stroke_opacity=.55,stroke_width=1.4,fill_opacity=0).set_points_as_corners([p(v,u) for u in z]))
   if t>=107:
    origin=np.array([0,.1,0]);g.add(arrow(origin,origin+[1,0,0],BLUE),arrow(origin,origin+[-.6,.6,0],GREEN),arrow(origin,origin+[0,1.1,0],GOLD))
  elif i==7:
   xx=np.linspace(-np.pi,np.pi,151);k=1 if t<134.5 else 2 if t<136 else 3;f=np.cos(xx) if 124<=t<128 else np.sin(k*xx)
   result=f if t<119 else np.cos(xx) if t<121.5 else -np.sin(xx) if t<124 else -np.cos(xx) if t<128 else -k*k*f
   a=axes(3,2.5,6.4,(-np.pi,np.pi,1),(-1.2,1.2,1));b=axes(-1.3,2.5,6.4,(-np.pi,np.pi,1),(-10,10,5) if t>=132 else (-1.2,1.2,1));g.add(a,b,curve(a,xx,f,BLUE),curve(b,xx,result,GOLD))
   if t>=132:g.add(tx('±10',-3.5,-.2,18,c=MUTED,w=.7))
  elif i==8:
   xx=np.linspace(-np.pi,np.pi,151);a=axes(1,2.7,6.6,(-np.pi,np.pi,1),(-4.8,4.8,2));g.add(a,curve(a,xx,-4*np.sin(2*xx),BLUE,7),curve(a,xx,-4*np.sin(2*xx),GOLD,2.5))
   u=-np.pi+2*np.pi*((t-139)/4%1);g.add(Dot(a.c2p(u,-4*np.sin(2*u)),radius=.07,color=GREEN))
  elif i==9:
   tau=max(0,t-164)*.1;a=axes(3,2.3,6.5,(0,1,.2),(0,55,10));g.add(a,curve(a,X,fourier(X,tau),GOLD))
   for j,n in enumerate([1,3,5]):
    b=axes(.9-j*1.35,1,6.5,(0,1,.2),(-45,45,20));g.add(b,curve(b,X,component(X,n,tau),[BLUE,GREEN,RED][j],2.5),tx(f'n={n}',-3.7,.9-j*1.35,18,c=MUTED,w=.7))
  return g
