"""Shared geometry and timing for nineteen independently replaceable scenes.

The surface uses a fixed oblique orthographic projection (compressed height).
Every input-plane plot uses equal x/y units, including normal/tangent arrows.
Text/caption helpers follow classical_mechanics/chapter_01/visuals.py.
"""
from pathlib import Path
from functools import lru_cache
import json, textwrap, os
import numpy as np
from manim import *
R=Path(__file__).resolve().parent
BG='#0C1420';INK='#E9E6DC';MUTED='#8291A3';BLUE='#58BDD1';GOLD='#DCBA6E';GREEN='#91BE88';RED='#DC7C75';PURPLE='#A495C5'
config.background_color=BG;config.frame_width=128/9;config.frame_height=8
def tx(s,x=0,y=0,size=28,c=INK,w=12):
 m=Text(s,font='Malgun Gothic',font_size=size,color=c)
 if m.width>w:m.scale_to_fit_width(w)
 return m.move_to([x,y,0])
@lru_cache(maxsize=180)
def _tex(s,size,c):return MathTex(s,font_size=size,color=c)
def eq(s,x=0,y=0,size=40,c=INK,w=6):
 m=_tex(s,size,c).copy()
 if m.width>w:m.scale_to_fit_width(w)
 return m.move_to([x,y,0])
def F(x,y):return 2*x+10*y-x*x+2*x*y-3*y*y
def grad(x,y):return np.array([2-2*x+2*y,10+2*x-6*y])
def f(x):return 19-(x-4)**2
def df(x):return 8-2*x
def level(c,t):
 a=np.sqrt(19-c);return np.array([4+a*np.cos(t)+a/np.sqrt(2)*np.sin(t),3+a/np.sqrt(2)*np.sin(t)])
def arr(p,v,c=GOLD):
 v=np.array(v,dtype=float);p=np.array(p,dtype=float)
 if np.linalg.norm(v)<.015:return VGroup()
 return Arrow(p,p+v,buff=0,color=c,stroke_width=4,max_tip_length_to_length_ratio=.2)
def path(points,c=BLUE,width=3,op=1):return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=op,fill_opacity=0).set_points_as_corners(points)
def lerp(a,b,t):return (1-t)*np.array(a)+t*np.array(b)
def ramp(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def keys(t,seq):
 for (a,x),(b,y) in zip(seq,seq[1:]):
  if t<=b:return float(x+(y-x)*ramp(t,a,b))
 return float(seq[-1][1])
def axes(x=0,y=.15,size=4.65,maximum=5):
 a=Axes(x_range=[0,maximum,1],y_range=[0,maximum,1],x_length=size,y_length=size,tips=False,axis_config=dict(include_ticks=False,stroke_width=1.2,stroke_color=MUTED)).move_to([x,y,0])
 g=VGroup(a)
 for k in range(1,maximum+1):
  g.add(Line(a.c2p(k,0),a.c2p(k,maximum),stroke_color=MUTED,stroke_width=.7,stroke_opacity=.15),Line(a.c2p(0,k),a.c2p(maximum,k),stroke_color=MUTED,stroke_width=.7,stroke_opacity=.15),tx(str(k),*a.c2p(k,0)[:2]+[0,-.17],size=15,w=.5),tx(str(k),*a.c2p(0,k)[:2]+[-.17,0],size=15,w=.5))
 g.add(tx('x',*a.c2p(maximum,0)[:2]+[.25,0],size=19),tx('y',*a.c2p(0,maximum)[:2]+[0,.22],size=19))
 return a,g
def hyper(a,c,width=2,op=.4):
 xs=np.linspace(max(c/5,.08),5,160);return path([a.c2p(x,c/x) for x in xs],BLUE,width,op)
def right_angle(p,u,v,s=.17):
 u=np.array(u)/np.linalg.norm(u)*s;v=np.array(v)/np.linalg.norm(v)*s
 return path([p+u,p+u+v,p+v],INK,1.6)

class OptimizationScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.add(self.clock)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  self.add(tx('GEOMETRY OF OPTIMIZATION',-4.7,3.6,16,MUTED,w=4.2),tx(self.rec['title'],3.4,3.6,21,INK,w=6.2),Line([-6.5,3.25,0],[6.5,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13.05,height=1.03,corner_radius=.1,stroke_width=0,fill_color='#142131',fill_opacity=1).move_to([0,-3.31,0]).set_z_index(50))
  self.caption=VGroup();self.labels=VGroup();self.last=None
  self.prepare();self.dynamic=VGroup();self.add(self.dynamic)
  self.numbers=VGroup()
  if self.index in (3,9):
   for y,c in [(1.2,INK),(.15,GOLD)] if self.index==3 else [(.8,PURPLE),(-.2,GOLD)]:
    self.numbers.add(DecimalNumber(0,num_decimal_places=2,font_size=36,color=c).move_to([4.3,y,0]))
   self.add(self.numbers)
   def update_numbers(m):
    t=self.clock.get_value()
    values=[self.moving_x(t),df(self.moving_x(t))] if self.index==3 else [self.theta(t)*180/PI,np.sqrt(8)*np.cos(self.theta(t))]
    for number,value in zip(m,values):
     center=number.get_center();number.set_value(0 if abs(value)<.005 else value).move_to(center)
   self.numbers.add_updater(update_numbers);update_numbers(self.numbers)
  if os.environ.get('LAGRANGE_SNAPSHOT'):
   t=float(os.environ['LAGRANGE_SNAPSHOT']);self.clock.set_value(t);self.numbers.update();self.update_text(t);self.add(self.geometry(t));return
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[31,39,42,49,55,59,63,67,71,75,80,87,91,96,101,104,107,112,117,121,124,128,135,138,142,146,151,156,159,164,168,171,175,181,184,188,192,197,200,204,207,209,214,219,224,230,235,240,245,252,257,263,267,273,278,284,291,297,301,305,308,314,319,323,327,331,335,339,343,347,351,355,358,363,370,373,376,380,384,388,394,398,401,405,408,411,414,419,423]
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[t for t in extra if self.start<t<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  l=next(x for x in self.lines if x['start']<=t<x['end'])
  if l!=self.last:
   self.remove(self.caption);self.last=l
   parts=textwrap.wrap(l['text'],width=58,break_long_words=False,break_on_hyphens=False)
   self.caption=VGroup(*[tx(p,size=25,w=12.25) for p in parts]).arrange(DOWN,buff=.10).move_to([0,-3.31,0]).set_z_index(51)
   assert len(parts)<=3
   self.add(self.caption);self.record('caption',self.caption,t)
  self.remove(self.labels);self.labels=self.label_group(t);self.add(self.labels)
  for m in self.labels:self.record('label',m,t)
 def record(self,kind,m,t):
  if not len(m.get_all_points()):return
  bounds=dict(left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1]))
  assert bounds['left']>=-6.75 and bounds['right']<=6.75,(self.index,t,kind,bounds)
  assert (bounds['bottom']>=-3.85 and bounds['top']<=-2.8) if kind=='caption' else (bounds['bottom']>=-2.7 and bounds['top']<=3.15),(self.index,t,kind,bounds)
  self.audit.append(dict(kind=kind,time=t,**bounds))
 def prepare(self):
  self.ax1=Axes(x_range=[0,8,1],y_range=[0,22,5],x_length=7.2,y_length=4.15,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.2)).move_to([-1.65,.2,0])
  self.curve1=path([self.ax1.c2p(x,f(x)) for x in np.linspace(0,8,161)],BLUE,3.5)
  self.ax,self.grid=axes(-2.5,.1,4.6,5)
  self.ellax,self.ellgrid=axes(-1.8,.15,5,8)
  self.mesh=self.surface()
  self.dimension_x=eq('x',size=30,c=BLUE);self.dimension_y=eq('y',size=30,c=BLUE);self.area_label=eq('xy',size=38,c=GREEN)
  self.ellipses=VGroup(*[self.ellipse(c) for c in [13,15,16,17,18]])
  self.hypers=VGroup(*[hyper(self.ax,c) for c in [1,2,3,4,5,6]])
  self.constraint=Line(self.ax.c2p(0,4),self.ax.c2p(4,0),color=RED,stroke_width=3.5)
  if self.index in (3,):self.add(self.ax1,self.curve1)
  if self.index in (6,7):self.add(self.mesh)
  if self.index==11:self.add(self.ellgrid,self.ellipses)
  if self.index in (13,14,15,16):self.add(self.grid,self.hypers,self.constraint)
 def project(self,x,y,z):return np.array([.91*(x-4)+.49*(y-3)-1.6,-.21*(x-4)+.43*(y-3)+.145*(z-12),0])
 def surface(self,extent=1):
  g=VGroup()
  # Shared section y=3 remains exactly the opening parabola.
  for y in np.linspace(1.8,4.2,15):g.add(path([self.project(x,y,F(x,y)) for x in np.linspace(1.6,6.4,70)],BLUE,1.05,.52))
  for x in np.linspace(1.6,6.4,19):g.add(path([self.project(x,y,F(x,y)) for y in np.linspace(1.8,4.2,55)],BLUE,.95,.42))
  return g
 def ellipse(self,c,width=1.8,op=.4):return path([self.ellax.c2p(*level(c,t)) for t in np.linspace(0,TAU,161)],BLUE,width,op)
 def plane(self,x,y,size=.8):
  v=grad(x,y);z=F(x,y)
  pts=[self.project(x+u,y+w,z+v@[u,w]) for u,w in [(-size,-size),(size,-size),(size,size),(-size,size)]]
  return Polygon(*pts,color=GOLD,stroke_width=2,fill_color=GOLD,fill_opacity=.14)
 def tangent1(self,x):
  p=self.ax1.c2p(x,f(x));u=self.ax1.c2p(x+1,f(x)+df(x))-p;u=u/np.linalg.norm(u)*1.8
  return VGroup(Line(p-u,p+u,color=GOLD,stroke_width=3),Dot(p,color=GREEN,radius=.075),DashedLine(self.ax1.c2p(x,0),p,color=MUTED,stroke_width=1))
 def input_arrows(self,x,y,normal=True,tangent=True,constraint=True):
  p=self.ax.c2p(x,y);g=VGroup(Dot(p,color=GREEN,radius=.075))
  if normal:g.add(arr(p,self.ax.c2p(x+.48*y,y+.48*x)-p,GOLD))
  if constraint:g.add(arr(p,self.ax.c2p(x+.48,y+.48)-p,RED))
  if tangent:g.add(arr(p,self.ax.c2p(x+.85,y-.85)-p,PURPLE))
  return g
 def label_group(self,t):
  g=VGroup();i=self.index
  if i==1:
   if t<14:g.add(tx('최댓값과 최솟값',0,2.75,31),eq(r'\max_x f(x)',-3,-2.3,35,GREEN),eq(r'\min_x f(x)',3,-2.3,35,GREEN))
   elif t<22:
    g.add(tx('목적함수',0,2.75,31,BLUE),tx('이동 거리  s(t)',-4.7,1.5,23),tx('에너지  E(x)',4.7,1.5,23),tx('생산 비용  C(q)',-4.7,-1.8,23),tx('모델 오차  L(θ)',4.7,-1.8,23))
   else:g.add(tx('미분은 최적화에서 어떤 역할을 할까?',0,2.75,31,GOLD))
  elif i==2:
   g.add(eq(r'f(x)=19-(x-4)^2',3.65,2.5,34,BLUE,w=4.4))
   if t<39:g.add(eq(r'\frac{f(3+h)-f(3)}{h}\to f\prime(3)',3.65,.8,36,GOLD,w=4.5),eq(r'h\to0',3.65,-.2,30,PURPLE))
   elif t<49:g.add(eq(r'P=(3,18)',3.65,1.15,34,GREEN),eq(r'L(x)=18+2(x-3)',3.65,-.1,32,GOLD,w=4.5),tx('接点 근처를 확대' .replace('接点','접점'),3.65,-1.2,23))
   else:g.add(eq(r'f(3+h)=18+2h-h^2',3.65,.9,31,w=4.7),eq(r'f(x_0+h)\approx f(x_0)+f\prime(x_0)h',3.65,-.6,31,GOLD,w=4.9))
  elif i==3:
   x=keys(t,[(55,2),(59,2),(67,4),(68,2),(71,2.7),(72,6),(75,5.3),(80,4)])
   g.add(eq(r'f(x)=19-(x-4)^2',3.6,2.5,33,BLUE,w=4.7),eq(r'x=',2.9,1.2,35),eq(r'f\prime(x)=',2.7,.15,37,GOLD),tx('정의역 내부 · 미분 가능',3.6,-1.3,23,MUTED,w=4.7))
   if t>=75:g.add(eq(r'f\prime(4)=0',3.6,-2.2,38,GREEN))
  elif i==4:g.add(tx('극대점',-4.3,2.6,27,GREEN),tx('극소점',0,2.6,27,GREEN),tx('수평인 변곡점',4.3,2.6,27,MUTED),eq(r'f\prime(x)=0',0,-1.4,44,GOLD),tx('극값의 필요조건 · 후보를 찾는 조건',0,-2.35,27))
  elif i==5:
   g.add(eq(r'f(x)=F(x,3)',3.9,2.4,36,BLUE,w=4.4),eq(r'F(x,y)=2x+10y-x^2+2xy-3y^2',3.9,.8,32,w=4.7),tx('같은 곡선 · 더 넓은 입력 공간',3.9,-.6,23,w=4.8),eq(r'y=3',-4.9,2.4,30,GOLD,w=2))
   if t>=101:g.add(tx('x 방향 / y 방향 / 함께 변화',3.9,-1.7,23,PURPLE,w=4.8))
  elif i in (6,7):
   if t<124:g.add(eq(r'P=(2,2,16)',4,2.45,34,GREEN,w=4.5),eq(r'z=16+2(x-2)+2(y-2)',4,1,33,GOLD,w=4.6),tx('접평면: 곡면의 일차 근사',4,-.6,24,w=4.7))
   elif t<142:
    g.add(eq(r'F_x=2-2x+2y',4,2.4,32,GOLD,w=4.5),eq(r'F_y=10+2x-6y',4,1.3,32,GOLD,w=4.5))
    g.add(eq(r'(2,2)\longrightarrow(4,3)',4,-.3,32,GREEN,w=4.6))
    if t<128:g.add(eq(r'F_x(2,2)=F_y(2,2)=2',4,-1.5,29,GOLD,w=4.5))
    elif t<135:g.add(tx('최적점으로 이동하는 접평면',4,-1.5,23,w=4.5))
    elif t<138:g.add(tx('기울어진 평면: 증가 방향 존재',4,-1.5,22,GOLD,w=4.5))
    else:g.add(tx('두 기울기가 모두 0',4,-1.5,25,GREEN,w=4.5))
   else:
    g.add(eq(r'\begin{cases}2-2x+2y=0\\10+2x-6y=0\end{cases}',4,1.8,34,GOLD,w=4.7),eq(r'x=4,\quad y=3',4,-.1,36,GREEN,w=4.5),tx('내부 극값의 후보',4,-1.4,25,w=4.5),eq(r'F(4,3)=19',4,-2.25,32,GREEN,w=4.5))
  elif i==8:
   g.add(eq(r'\nabla F=\begin{pmatrix}F_x\\F_y\end{pmatrix}=\begin{pmatrix}2-2x+2y\\10+2x-6y\end{pmatrix}',3.6,2.1,34,GOLD,w=5.5),eq(r'\nabla F(2,2)=\begin{pmatrix}2\\2\end{pmatrix}',3.6,.55,33,GOLD,w=5.2),tx('입력 공간 xy의 벡터',3.6,-.65,24,MUTED,w=5.2))
   if t>=164:g.add(eq(r'dF=\nabla F\cdot\mathbf h',3.6,-1.65,37,w=5.2),eq(r'\Delta F\approx dF',3.6,-2.4,28,PURPLE,w=5.2))
  elif i==9:
   theta=self.theta(t)
   g.add(eq(r'dF=\|\nabla F\|\,\|\mathbf h\|\cos\theta',3.6,2.2,37,w=5.2),eq(r'\theta\ ({}^\circ)=',2.6,.8,36,PURPLE),eq(r'dF=',2.9,-.2,37,GOLD),tx('변위의 길이는 일정',3.6,-1.2,24,MUTED,w=5.2))
   if t>=192:g.add(eq(r'\theta=90^\circ\Rightarrow dF=0',3.6,-2.25,32,GREEN,w=5.4))
  elif i==10:g.add(tx('같은 높이로 자른 단면',3.9,2.4,27,BLUE,w=4.8),eq(r'z=c',3.9,1.1,40),eq(r'F(x,y)=c',3.9,-.2,40,BLUE),tx('수평 단면 → 입력 평면에 투영',3.9,-1.5,23,w=4.8))
  elif i==11:
   g.add(eq(r'F(x,y)=16',4,2.5,38,BLUE,w=4.4),tx('등위선을 따라: 함수값 일정',4,1.25,23,w=4.5))
   if t>=214:g.add(eq(r'\mathbf h=(x\prime(t),y\prime(t))',4,.2,31,PURPLE,w=4.6))
   if t>=219:g.add(eq(r'\nabla F\cdot\mathbf h=0',4,-.8,35,GOLD,w=4.5))
   if t>=224:g.add(eq(r'\nabla F\ne\mathbf0\ \Rightarrow\ \nabla F\perp\mathbf h',4,-1.8,31,GREEN,w=4.8),tx('접선 직선 이동: 일차 변화만 0',4,-2.5,20,MUTED,w=4.8))
  elif i==12:
   g.add(tx('둘레가 정해진 직사각형',3.7,2.45,28,w=5),eq(r'F(x,y)=xy',3.7,1.15,42,BLUE,w=5),eq(r'2x+2y=8',3.7,-.1,40,RED,w=5),eq(r'x+y=4',3.7,-1.25,40,RED,w=5),tx('가로와 세로를 모두 늘릴 수 없다',3.7,-2.35,22,w=5.1))
  elif i in (13,14,15,16):
   g.add(eq(r'F(x,y)=xy',3.75,2.55,35,BLUE,w=4.8),eq(r'G(x,y)=x+y=4',3.75,1.55,33,RED,w=4.8))
   if i==13:
    g.add(eq(r'\mathbf h=(1,-1)',3.75,.25,35,PURPLE,w=4.8),tx('제약곡선의 접선 방향',3.75,-.7,24,PURPLE,w=4.8))
    if t>=284:g.add(tx('∇F 방향은 제약을 위반할 수 있다',3.75,-1.65,22,GOLD,w=4.8))
   elif i==14:
    x=keys(t,[(297,1),(301,1.5),(305,1),(308,2),(319,2)])
    g.add(eq(r'P=(x,4-x)',3.75,.35,32,GREEN,w=4.8),eq(r'dF(\mathbf h)=4-2x',3.75,-.65,34,PURPLE,w=4.8))
    if t>=308:g.add(eq(r'dF(\mathbf h)=0,\quad\nabla F\ne\mathbf0',3.75,-1.8,31,GOLD,w=4.9))
   elif i==15:
    if t<331:g.add(eq(r'\nabla F\perp\mathbf h,\quad\nabla G\perp\mathbf h',3.75,.15,32,w=4.9),tx('같은 접선에 수직 → 서로 평행',3.75,-1.1,23,w=4.9))
    else:g.add(eq(r'\nabla F=\lambda\nabla G',3.75,.05,44,GOLD,w=5),eq(r'\nabla G\ne\mathbf0',3.75,-1.1,33,RED,w=5),tx('λ: 라그랑주 승수',3.75,-2.25,26,GOLD,w=4.9))
   else:g.add(eq(r'\begin{cases}\nabla F=\lambda\nabla G\\G(x,y)=4\end{cases}',3.75,.05,38,GOLD,w=5),tx('제약 극값의 후보를 찾는 필요조건',3.75,-1.45,22,w=5),tx('미분 가능 · 정칙 제약 ∇G ≠ 0',3.75,-2.35,20,MUTED,w=5))
  elif i==17:
   g.add(tx('직사각형의 최대 넓이',-3.2,2.7,29),eq(r'F=xy,\quad G=x+y=4',3.4,2.55,33,w=5.6))
   if t>=363:g.add(eq(r'\nabla F=(y,x),\quad\nabla G=(1,1)',3.4,1.5,31,w=5.6))
   if t>=370:g.add(eq(r'(y,x)=\lambda(1,1)\Rightarrow x=y',3.4,.35,32,GOLD,w=5.7))
   if t>=376:g.add(eq(r'x+y=4\Rightarrow x=y=2',3.4,-.75,34,GREEN,w=5.7))
   if t>=380:g.add(eq(r'F(2,2)=4,\quad F(0,4)=F(4,0)=0',3.4,-1.85,31,GREEN,w=5.9),tx('x,y ≥ 0인 닫힌 선분에서 경계까지 비교',3.4,-2.5,19,MUTED,w=5.9))
  elif i==18:
   g.add(tx('일변수',-4.3,2.7,27),tx('다변수',0,2.7,27),tx('제약 최적화',4.3,2.7,27),eq(r'f\prime(x)=0',-4.3,-1.7,34,GOLD,w=3.7))
   if t>=394:g.add(eq(r'\nabla F=\mathbf0',0,-1.7,34,GOLD,w=3.7))
   if t>=401:g.add(eq(r'\nabla F=\lambda\nabla G',4.3,-1.7,32,GOLD,w=3.7))
   g.add(tx('접선 → 접평면 → 그래디언트와 등위선',0,-2.5,26,w=12))
  elif i==19:
   g.add(tx('제약조건 없음',-3.3,2.6,28),tx('제약조건 존재',3.3,2.6,28),tx('모든 방향',-3.3,-1.3,25,PURPLE,w=5),tx('허용된 접선 방향',3.3,-1.3,25,PURPLE,w=5))
   g.add(eq(r'\nabla F=\mathbf0',-3.3,-2.15,35,GOLD,w=5.7),eq(r'\nabla F\cdot\mathbf h=0',3.3,-2.15,35,GOLD,w=5.7))
  return g
 def theta(self,t):return keys(t,[(171,PI/4),(175,PI/4),(181,0),(184,0),(188,PI),(192,0),(197,PI/2)])
 def moving_x(self,t):return keys(t,[(55,2),(59,2),(67,4),(68,2),(71,2.7),(72,6),(75,5.3),(80,4)])
 def geometry(self,t):
  i=self.index;g=VGroup()
  if i==1:
   xs=np.linspace(-4.7,4.7,180);pts=[np.array([x,.05+.055*x**3-.65*x,0]) for x in xs]
   g.add(Line([-5.5,-1.9,0],[5.5,-1.9,0],color=MUTED,stroke_width=1),path(pts[:max(2,int(len(pts)*ramp(t,0,5)))],BLUE,3.5))
   if t>=6:
    for x in [-np.sqrt(.65/.165),np.sqrt(.65/.165)]:
     p=np.array([x,.05+.055*x**3-.65*x,0]);g.add(Dot(p,color=GREEN),DashedLine(p,[x,-1.9,0],color=GREEN,stroke_opacity=.5))
  elif i==2:
   zoom=1+7*ramp(t,42,49)*(1-ramp(t,50,55));center=self.ax1.c2p(3,18);origin=np.array([-1.8,.25,0]);p0=self.ax1.c2p(3,18)
   project=lambda p:origin+(p-center)*zoom
   lo=max(0,3-3.4/zoom);hi=min(8,3+3.4/zoom)
   curve=path([project(self.ax1.c2p(x,f(x))) for x in np.linspace(lo,hi,120)],BLUE,3.7)
   h=keys(t,[(26,1.7),(31,1.3),(39,.005),(55,.005)]);slope=(f(3+h)-f(3))/h
   tan=path([project(self.ax1.c2p(x,18+slope*(x-3))) for x in [lo,hi]],GOLD,2.7)
   g.add(Line([-5.4,-2.3,0],[1.7,-2.3,0],stroke_color=MUTED,stroke_opacity=.3),curve,tan,Dot(origin,color=GREEN,radius=.075))
   if t<39:g.add(Dot(project(self.ax1.c2p(3+h,f(3+h))),color=PURPLE,radius=.065))
  elif i==3:
   x=keys(t,[(55,2),(59,2),(67,4),(68,2),(71,2.7),(72,6),(75,5.3),(80,4)]);g.add(self.tangent1(x))
   if 67<=t<75:
    p=self.ax1.c2p(x,f(x));g.add(arr(p+[0,-.4,0],[.7*np.sign(df(x)),0,0],PURPLE))
  elif i==4:
   for x0,kind in [(-4.3,-1),(0,1),(4.3,0)]:
    points=[np.array([x0+u,.3+(kind*u*u*.55 if kind else u**3*.4),0]) for u in np.linspace(-1.3,1.3,80)]
    g.add(path(points,BLUE,3),Line([x0-1,.3,0],[x0+1,.3,0],color=GOLD,stroke_width=2),Dot([x0,.3,0],color=GREEN,radius=.07))
  elif i==5:
   a=ramp(t,91,96)
   # Existing section continuously rotates from a flat curve into the mesh.
   xs=np.linspace(1.3,6.7,100)
   g.add(path([lerp([-1.6+(x-4)*1.05,(f(x)-13)*.23,0],self.project(x,3,f(x)),a) for x in xs],GOLD,3))
   if a>0:g.add(self.mesh.copy().set_stroke(opacity=.5*a))
   if t>=101:
    p=self.project(2,2,F(2,2))
    for dx,dy,c in [(1,0,GOLD),(0,1,PURPLE),(1,1,GREEN)]:g.add(path([self.project(2+s*dx,2+s*dy,F(2+s*dx,2+s*dy)) for s in np.linspace(0,1,25)],c,3))
   if t>=107:
    for ang in np.linspace(0,PI,6):
     v=np.array([np.cos(ang),np.sin(ang)]);g.add(path([self.project(2+s*v[0],2+s*v[1],16+2*s*np.sum(v)) for s in [-.8,.8]],GOLD,1.7,.7))
  elif i in (6,7):
   a=ramp(t,128,135);x=2+2*a;y=2+a
   if 135<=t<138:x,y=2,2
   g.add(self.plane(x,y),Dot(self.project(x,y,F(x,y)),color=GREEN,radius=.075))
   if 124<=t<128:
    for dx,dy,c in [(1,0,GOLD),(0,1,PURPLE)]:g.add(path([self.project(x+s*dx,y+s*dy,F(x+s*dx,y+s*dy)) for s in np.linspace(-.85,.85,40)],c,3.4))
  elif i==8:
   g.add(self.grid);p=self.ax.c2p(2,2);q=self.ax.c2p(4,4)
   g.add(arr(p,q-p,GOLD),Dot(p,color=GREEN,radius=.08),DashedLine(p,self.ax.c2p(4,2),color=BLUE),DashedLine(self.ax.c2p(4,2),q,color=BLUE))
   if t>=164:g.add(arr(p,self.ax.c2p(2.4,2.2)-p,PURPLE))
  elif i==9:
   p=np.array([-2.7,.15,0]);th=self.theta(t);ga=PI/4;v=np.array([np.cos(ga),np.sin(ga),0]);h=np.array([np.cos(ga+th),np.sin(ga+th),0])
   g.add(Circle(radius=1,color=MUTED,stroke_opacity=.22).move_to(p),arr(p,np.sqrt(8)*v,GOLD),arr(p,h,PURPLE),Dot(p,color=INK,radius=.055))
   if th>.015:g.add(Arc(radius=.55,start_angle=ga,angle=th,color=INK,stroke_width=1.4).shift(p))
   foot=p+np.cos(th)*v;g.add(DashedLine(p+h,foot,color=PURPLE,stroke_width=1.5))
  elif i==10:
   a=ramp(t,204,209)
   if a<1:g.add(self.mesh.copy().set_stroke(opacity=.5*(1-a)))
   for c in [13,15,16,17,18]:
    if t<200+(c-13)*.45:continue
    pts=[]
    for ang in np.linspace(0,TAU,121):
     x,y=level(c,ang);pts.append(lerp(self.project(x,y,c),self.ellax.c2p(x,y),a))
    g.add(path(pts,BLUE,2.4))
    if 200<=t<204:
     corners=[self.project(x,y,c) for x,y in [(1.2,1.5),(6.8,1.5),(6.8,4.5),(1.2,4.5)]]
     g.add(Polygon(*corners,stroke_color=MUTED,stroke_width=.8,stroke_opacity=.3,fill_opacity=.025,fill_color=INK))
   if a>0:g.add(self.ellgrid.copy().set_opacity(a))
  elif i==11:
   ang=keys(t,[(209,3.55),(214,4.2),(224,4.2),(235,9.8),(240,9.8)]);x,y=level(16,ang);p=self.ellax.c2p(x,y);v=grad(x,y);v=v/np.linalg.norm(v);h=np.array([-v[1],v[0]])
   g.add(self.ellipse(16,3.3,1),Dot(p,color=GREEN,radius=.075))
   if t>=214:g.add(arr(p,[h[0],h[1],0],PURPLE))
   if t>=219:g.add(arr(p,[v[0],v[1],0],GOLD))
   if t>=224:g.add(right_angle(p,[*h,0],[*v,0]))
  elif i==12:
   x=keys(t,[(240,1),(252,1),(257,1),(263,3),(267,1)]);y=4-x
   rect=Rectangle(width=x*.95,height=y*.95,color=RED,stroke_width=4,fill_color=GREEN,fill_opacity=.09).move_to([-2.6,.2,0]);g.add(rect)
   g.add(self.dimension_x.copy().next_to(rect,UP,buff=.23),self.dimension_y.copy().next_to(rect,RIGHT,buff=.25),self.area_label.copy().move_to(rect))
   # No stretched dimensions: the perimeter stays 8 at all times.
   g.add(Line(rect.get_corner(UL)+[0,.16,0],rect.get_corner(UR)+[0,.16,0],color=BLUE),Line(rect.get_corner(UR)+[.16,0,0],rect.get_corner(DR)+[.16,0,0],color=BLUE))
  elif i in (13,14,15,16):
   if i==13:x=keys(t,[(267,1),(278,1),(284,1.5),(291,1),(297,1)])
   elif i==14:x=keys(t,[(297,1),(301,1.5),(305,1),(308,2),(319,2)])
   else:x=2
   y=4-x;p=self.ax.c2p(x,y)
   g.add(hyper(self.ax,x*y,3.6,1),self.input_arrows(x,y,normal=t>=284,tangent=t>=278,constraint=t>=319))
   if i==15:g.add(right_angle(p,[1,-1,0],[1,1,0]))
   if i==13 and 284<=t<291:
    u=np.array([y,x]);q=self.ax.c2p(*(np.array([x,y])+.22*u));g.add(Dot(q,color=GOLD,radius=.055),DashedLine(p,q,color=GOLD))
  elif i==17:
   x=keys(t,[(355,1),(358,1),(363,1.3),(370,1.5),(376,2),(426,2)]);y=4-x
   g.add(Rectangle(width=x*.95,height=y*.95,color=RED,stroke_width=4,fill_color=GREEN,fill_opacity=.12).move_to([-3.2,.15,0]))
   if t>=376:
    g.add(eq(r'2',-3.2,1.4,31,GREEN),eq(r'2',-1.95,.15,31,GREEN),eq(r'4',-3.2,.15,48,GREEN))
  elif i==18:
   pts=[[-4.3+u,.6-.8*u*u,0] for u in np.linspace(-1.35,1.35,80)];g.add(path(pts,BLUE,3),Line([-5.2,.6,0],[-3.4,.6,0],color=GOLD),Dot([-4.3,.6,0],color=GREEN,radius=.07))
   if t>=394:
    mesh=self.mesh.copy().scale(.39).move_to([0,.1,0]);plane=self.plane(4,3).scale(.39).move_to([0,1,0]);g.add(mesh,plane)
   if t>=401:
    a,grid=axes(4.3,.2,2.7,5);g.add(grid,hyper(a,4,2.5,1),Line(a.c2p(0,4),a.c2p(4,0),color=RED),Dot(a.c2p(2,2),color=GREEN,radius=.06),arr(a.c2p(2,2),[.8,.8,0],GOLD))
  elif i==19:
   left=np.array([-3.3,.4,0]);right=np.array([3.3,.4,0]);g.add(Line([0,-2.5,0],[0,2.8,0],color=MUTED,stroke_opacity=.25))
   for radius in [.5,.95,1.4]:g.add(Circle(radius=radius,color=BLUE,stroke_opacity=.45).stretch(.75,1).move_to(left))
   for ang in np.linspace(0,TAU,8,endpoint=False):g.add(arr(left,[1.15*np.cos(ang),1.15*np.sin(ang),0],PURPLE))
   g.add(Dot(left,color=GREEN,radius=.075))
   if t>=411:
    g.add(path([right+[u,4/(2+u)-2,0] for u in np.linspace(-.9,1.8,80)],BLUE,3),Line(right+[-1.3,1.3,0],right+[1.3,-1.3,0],color=RED,stroke_width=2.7),arr(right,[.8,.8,0],GOLD),arr(right,[.9,-.9,0],PURPLE),arr(right,[-.9,.9,0],PURPLE),Dot(right,color=GREEN,radius=.075))
  return g
