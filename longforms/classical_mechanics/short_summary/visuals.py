"""9:16 layout sharing the longform pendulum and quantum animation models."""
from pathlib import Path
import sys,importlib.util,json,textwrap
import numpy as np
from manim import *
R=Path(__file__).resolve().parent;P=R.parent/'chapter_01';sys.path.append(str(P))
spec=importlib.util.spec_from_file_location('common_pendulum_visuals',P/'visuals.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
BG,INK,MUTED,BLUE,GOLD,GREEN,RED=base.BG,base.INK,base.MUTED,base.BLUE,base.GOLD,base.GREEN,base.RED
rig,arr=base.rig,base.arr
from mechanics import MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi,rho,HISTORY_T,HISTORY_Q,HISTORY_W
config.frame_width=9;config.frame_height=16;config.background_color=BG
RB=float(H(.65,0)/EC)
def tx(s,x=0,y=0,size=30,c=INK,w=7.8):return base.tx(s,x,y,size,c,w=w)
def eq(s,x=0,y=0,size=45,c=INK,w=7.8):return base.eq(s,x,y,size,c,w=w)
def axes(x,y,w,h,xrange,yrange):
 a=Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a
def curve(ax,x,y,c=GOLD,width=3,op=1):return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=op,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])
class SummaryScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def replace_live(self,m,new):m.submobjects=new.submobjects;return m
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('뉴턴에서 해밀토니안까지',0,7.25,28,w=8),Line([-3.9,6.75,0],[3.9,6.75,0],stroke_color=MUTED,stroke_opacity=.3))
  self.add(RoundedRectangle(width=8.3,height=1.85,corner_radius=.13,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-6.85,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None;self.prepare()
  self.dynamic.add_updater(lambda m:self.replace_live(m,self.geometry(self.clock.get_value())))
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[x for x in [33,38,55,60,67,71,76,82,87,94,102,109,114,118,127,133,142,148,155,164,166,168] if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,indent=2),encoding='utf-8')
 def update_text(self,t):
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  if line!=self.current:
   self.remove(self.caption);self.current=line
   self.caption=VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=line['start'],end=line['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1])))
  self.remove(self.static);self.static=self.labels(t);self.add(self.static)
  for m in self.static:assert m.get_left()[0]>-4.2 and m.get_right()[0]<4.2 and m.get_bottom()[1]>-5.65 and m.get_top()[1]<6.4,('label',self.index,t,m.get_center())
 def prepare(self):self.cache={}
 def ordinary(self,t):
  q,w=MODEL.state_at(max(0,t));return float(q),float(I*w)
 def pend(self,t,x=0,y=4.3,L=3.8,forces=0):
  q,p=self.ordinary(t);return rig(0,pivot=(x,y,0),L=L,theta=q,omega=p/I,forces=forces)
 def level(self,ax,r=RB,c=BLUE,op=.5):
  key=(tuple(ax.get_center()),ax.width,ax.height,r,c,op)
  if key not in self.cache:self.cache[key]=VGroup(*[curve(ax,q,p,c,2,op) for q,p in contour(r)])
  return self.cache[key].copy()
 def phase(self,t,y=-2,h=3.7,w=6.5,levels=True,moving=True):
  ax=axes(0,y,w,h,[-.8,.8,.4],[-7,7,2]);g=VGroup(ax)
  if levels:g.add(self.level(ax))
  if moving:
   q,p=self.ordinary(t);g.add(Dot(ax.c2p(q,p),color=GOLD,radius=.075))
  return g,ax
 def field_arrows(self,ax):
  key=('field',tuple(ax.get_center()),ax.width,ax.height)
  if key not in self.cache:
   vals=[]
   for q in np.linspace(-.65,.65,7):
    for p in np.linspace(-5.5,5.5,7):
     v=field(np.array([q,p]));d=ax.c2p(q+.03*v[0],p+.03*v[1])-ax.c2p(q,p);vals.append((ax.c2p(q,p),d))
   scale=.44/max(np.linalg.norm(d) for _,d in vals);self.cache[key]=VGroup(*[arr(a,d*scale,BLUE,.4) for a,d in vals])
  return self.cache[key].copy()
 def labels(self,t):
  i=self.index;g=VGroup()
  title=['이미 예측할 수 있었는데, 왜?','힘에서 에너지와 작용으로','작용에서 얻은 같은 운동 법칙','운동을 하나의 점으로 기록하다','시간 변화를 생성하는 함수','변화 속에서 보존되는 넓이','대칭성과 보존량의 연결','달라진 상태, 이어지는 역할','같은 운동에서 발견한 새로운 구조'][i-1]
  g.add(tx(title,0,5.95,32,c=GOLD))
  if i==1:
   g.add(eq(r'F=ma',0,-1.2,65,c=BLUE),tx('힘 + 초기조건 → 이후의 운동',0,-2.55,29,c=BLUE),tx('NEWTON  →  LAGRANGE  →  HAMILTON',0,-4.4,22,c=MUTED))
  elif i==2:
   g.add(tx('운동에너지 T',-1.85,-.65,25,c=BLUE,w=3.5),tx('위치에너지 V',1.85,-.65,25,c=GOLD,w=3.5))
   if t>=33:g.add(eq(r'L=T-V',0,-2,52,c=GOLD))
   if t>=38:g.add(eq(r'S=\int_{t_1}^{t_2} L\,\mathrm dt',0,-4.75,36,c=GREEN),tx('時間별 값 → 경로 전체의 값'.replace('時間','시간'),0,-5.5,21,c=MUTED))
  elif i==3:
   g.add(tx('시작과 끝의 위치·시각을 고정',0,4.9,25,c=MUTED),tx('실제 경로',0,.25,27,c=GOLD))
   if t>=55:g.add(eq(r'\delta S=0',0,-1.1,63,c=GREEN),tx('작용 자체가 아닌, 일차 변화가 0',0,-2.3,24,c=MUTED))
   if t>=60:g.add(eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',0,-3.65,43,c=BLUE),tx('같은 운동 · 다른 수학적 원리',0,-5.05,28,c=GOLD))
  elif i==4:
   if t>=71:g.add(eq(r'(\theta,p_\theta)',0,.65,44,c=GREEN),tx('각도와 정준운동량',0,-4.5,26,c=MUTED))
   if t>=82:g.add(tx('하나의 점 = 순간적인 상태',0,-5.3,28,c=GOLD))
  elif i==5:
   if t<102:
    g.add(eq(r'p_\theta=\frac{\partial L}{\partial\dot\theta}',0,4.45,46,c=BLUE),tx('속도 방향의 기울기 → 운동량',0,-.65,26,c=MUTED),eq(r'H=p_\theta\dot\theta-L',0,-2.1,48,c=GREEN),tx('르장드르 변환',0,-3.45,30,c=GREEN),tx('위치·속도 → 위치·운동량',0,-4.85,27,c=GOLD))
   else:
    g.add(eq(r'H(\theta,p_\theta)=T+V',0,4.4,43,c=GREEN),tx('이상적인 진자 · 마찰 없음',0,3.45,22,c=MUTED))
    if t<114:g.add(tx('같은 에너지의 상태 → 등고선',0,-4.6,27,c=GOLD))
    else:g.add(eq(r'\dot\theta=H_{p_\theta},\quad\dot p_\theta=-H_\theta',0,-4.1,36,c=BLUE),tx('방향과 속도를 함께 결정',0,-5.15,27,c=GOLD))
  elif i==6:
   g.add(tx('같은 영역을 실제 해밀턴 흐름으로 이동',0,4.75,23,c=MUTED),eq(r'A(t)/A(0)=1',0,-3.5,47,c=GREEN),tx('하나의 자유도 · 정준 위상 공간',0,-4.6,23,c=MUTED))
   if t>=133:g.add(tx('심플렉틱 구조',0,-5.3,30,c=GOLD))
  elif i==7:
   g.add(tx('시간 이동 대칭성',0,4.65,29,c=GOLD),tx('에너지 보존',0,1.6,32,c=GOLD),tx('공간 이동 대칭성',0,.25,29,c=BLUE),tx('자유 입자 · 운동량 보존',0,-2.1,27,c=BLUE))
   if t>=148:g.add(tx('뇌터 정리',0,-3.8,38,c=GREEN),tx('작용의 연속 대칭 ↔ 보존량',0,-5,26,c=MUTED))
  elif i==8:
   g.add(tx('고전 상태 (q,p)',0,4.7,27,c=BLUE),eq(r'|\psi\rangle',-2.7,.05,45,c=GREEN,w=2),tx('양자 상태 · 복소 진폭',.65,.1,25,c=GREEN,w=5.8),tx('실수부',-1.9,-2.65,21,c=BLUE,w=3),tx('허수부',1.9,-2.65,21,c=GOLD,w=3),tx('새로운 상태와 측정의 물리 이론',0,-3.5,25,c=MUTED))
   if t>=155:g.add(eq(r'i\hbar\frac{\mathrm d}{\mathrm dt}|\psi\rangle=\hat H|\psi\rangle',0,-4.75,39,c=GREEN))
  else:
   if t<168:g.add(tx('NEWTON · LAGRANGE · HAMILTON',0,-4.7,23,c=MUTED))
   else:g.add(tx('서로 다른 수학적 언어',0,-2.1,34,c=GREEN),tx('이전에는 보이지 않던 관계와 구조',0,-3.4,27,c=GOLD))
  if i==5 and t>=118:
   ax=axes(0,-.3,6.7,5.1,[-.8,.8,.4],[-7,7,2]);g.add(self.field_arrows(ax))
  return g
 def geometry(self,t):
  i=self.index;g=VGroup()
  if i==1:g.add(self.pend(t*.65,forces=1 if t<22 else 2))
  elif i==2:
   u=(t-25)*.5 if t<38 else (t-38)*.35;g.add(self.pend(u,y=4.65,L=3.4));q,p=self.ordinary(u);E=float(H(.65,0));vals=[p*p/(2*I),float(H(q,0))]
   for x,v,c in [(-1.85,vals[0],BLUE),(1.85,vals[1],GOLD)]:
    g.add(Line([x-1.55,-1.3,0],[x+1.55,-1.3,0],color=MUTED,stroke_width=13,stroke_opacity=.2))
    if v/E>.00001:g.add(Line([x-1.55,-1.3,0],[x-1.55+3.1*v/E,-1.3,0],color=c,stroke_width=13))
   if t>=38:
    ax=axes(0,-3.35,6.5,1.8,[0,2.5,.5],[-5,5,2]);g.add(ax);ts=np.linspace(0,min(2.45,(t-38)*.35)+.001,100);qs=np.interp(ts,MODEL.times,MODEL.states[:,0]);ws=np.interp(ts,MODEL.times,MODEL.states[:,1]);ls=.5*I*ws**2-A*(1-np.cos(qs));g.add(curve(ax,ts,ls,GOLD))
    for a,b,v in zip(ts[:-1],ts[1:],ls[:-1]):
     if abs(v)>.001:g.add(Polygon(ax.c2p(a,0),ax.c2p(a,v),ax.c2p(b,v),ax.c2p(b,0),stroke_width=0,fill_color=GREEN if v>=0 else RED,fill_opacity=.28))
  elif i==3:
   ax=axes(0,2.6,6.5,3.5,[0,2,.5],[-1,1,.5]);g.add(ax)
   for e in [-.24,-.12,0,.12,.24]:g.add(curve(ax,HISTORY_T,HISTORY_Q+e*np.sin(np.pi*HISTORY_T/2),GOLD if e==0 else BLUE,4 if e==0 else 2,1 if e==0 else .35))
   g.add(Dot(ax.c2p(0,HISTORY_Q[0]),color=GOLD),Dot(ax.c2p(2,HISTORY_Q[-1]),color=GOLD))
  elif i==4:
   g.add(self.pend((t-64)*.65,y=4.65,L=3.2))
   if 67<=t<71:
    q,p=self.ordinary((t-64)*.65);pos=np.array([3.2*np.sin(q),4.65-3.2*np.cos(q),0]);g.add(arr(pos,[-np.cos(q),-np.sin(q),0],BLUE),arr(pos,[np.cos(q),np.sin(q),0],GOLD))
   if t>=71:
    v,ax=self.phase((t-64)*.65,y=-2,h=3.7,levels=t>=82);g.add(v)
  elif i==5:
   if t<102:
    ax=axes(0,2,6.4,3.2,[-1.5,1.5,.5],[-4,4,2]);w=.65;V=A*(1-np.cos(.35));xx=np.linspace(-1.45,1.45,101);yy=.5*I*xx**2-V;g.add(ax,curve(ax,xx,yy,GOLD),curve(ax,[-.3,1.3],[I*w*(-.3-w)+.5*I*w*w-V,I*w*(1.3-w)+.5*I*w*w-V],BLUE),Dot(ax.c2p(w,.5*I*w*w-V),color=BLUE))
   else:
    v,ax=self.phase((t-102)*.65,y=-.3,h=5.1,w=6.7,moving=t>=118)
    for r in [.035,.14,.2]:v.add(self.level(ax,r,BLUE,.2))
    g.add(v)
  elif i==6:
   ax=axes(0,.7,6.7,5.7,[-.8,.8,.4],[-7,7,2]);g.add(ax)
   for r in [.035,.14,.2]:g.add(self.level(ax,r,BLUE,.2))
   u=float(np.clip((t-127)*.6,0,4));b,pts=packet(u)
   g.add(Polygon(*[ax.c2p(q,p) for q,p in INITIAL],color=BLUE,stroke_opacity=.6,fill_opacity=0),Polygon(*[ax.c2p(q,p) for q,p in b],color=GREEN,fill_color=GREEN,fill_opacity=.25,stroke_width=3),*[Dot(ax.c2p(q,p),color=GOLD,radius=.035) for q,p in pts])
  elif i==7:
   for offset,y,c in [(0,3.65,GOLD),(1,2.6,BLUE)]:
    ax=axes(0,y,6.6,.8,[0,5,1],[-.8,.8,.4]);xx=np.linspace(offset,4.9,81);yy=[self.ordinary((x-offset)*.7)[0] for x in xx];g.add(ax,curve(ax,xx,yy,c))
   g.add(Line([-3,-1,0],[3,-1,0],color=MUTED));x=-2.8+5.6*((t-137)%4)/4;g.add(Dot([x,-1,0],color=BLUE),arr([-1.5,-.65,0],[2,0,0],BLUE))
  elif i==8:
   v,_=self.phase((t-150)*.65,y=2.8,h=2.5,w=5.4);g.add(v)
   ax=axes(0,-1.4,6.8,1.9,[-5,5,2],[-.85,.85,.4]);z=psi(X,(t-150)*.5);g.add(ax,curve(ax,X,z.real,BLUE),curve(ax,X,z.imag,GOLD))
  else:
   if t<164:g.add(self.pend((t-162)*.65,forces=1))
   elif t<166:
    ax=axes(0,1.8,6.5,4.5,[0,2,.5],[-1,1,.5]);g.add(ax,curve(ax,HISTORY_T,HISTORY_Q,GOLD,4))
   elif t<168:
    v,_=self.phase((t-166)*.65,y=1.7,h=4.5,w=6.5);g.add(v)
   else:g.add(self.pend((t-168)*.65))
  return g
