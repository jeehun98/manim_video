"""Continuous world tour, rendered in replaceable exact-duration segments."""
from pathlib import Path
import sys,importlib.util,json,textwrap
import numpy as np
from manim import *
R=Path(__file__).resolve().parent;P=R.parent/'chapter_01';sys.path.append(str(P))
spec=importlib.util.spec_from_file_location('common_classical_visuals',P/'visuals.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
tx,eq,rig,arr=base.tx,base.eq,base.rig,base.arr
BG,INK,MUTED,BLUE,GOLD,GREEN,RED=base.BG,base.INK,base.MUTED,base.BLUE,base.GOLD,base.GREEN,base.RED
from mechanics import MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi
FW=128/9;config.frame_width=FW;config.frame_height=8;config.background_color=BG
RB=float(H(.65,0)/EC);PURPLE='#B69AE7'

TEXT_CACHE={}
def tx(s,x=0,y=0,size=28,c=INK,w=12):
 key=('text',s,x,y,size,str(c),w)
 if key not in TEXT_CACHE:TEXT_CACHE[key]=base.tx(s,x,y,size,c,w)
 return TEXT_CACHE[key].copy()
def eq(s,x=0,y=0,size=44,c=INK,w=6):
 key=('math',s,x,y,size,str(c),w)
 if key not in TEXT_CACHE:TEXT_CACHE[key]=base.eq(s,x,y,size,c,w)
 return TEXT_CACHE[key].copy()

REGIONS=[('01','NEWTON','힘과 초기조건',BLUE),('02','LAGRANGE','에너지와 작용',GOLD),('03','PHASE SPACE','상태 · 점 · 궤적',GREEN),('04','HAMILTON','상태의 시간 진화',GOLD),('05','STRUCTURE','기하학 · 대칭성',BLUE),('EP','QUANTUM','새로운 상태 표현',PURPLE)]
def ease(u):u=np.clip(u,0,1);return float(u*u*(3-2*u))
def blend(a,b,t,lo,hi):return a+(b-a)*ease((t-lo)/(hi-lo))
def camera_at(t):
 # World centers stay fixed. Only the camera traverses or changes its width.
 keys=[(0,0,FW),(4,0,FW),(8,0,16.2),(12,0,FW),(19,0,FW),(28,14,FW),(35,14,FW),(43,28,FW),(48,28,FW),(54,42,FW),(58,56,FW),(66,56,FW),(71,70,FW),(74,70,FW),(81,35,87),(85,35,87),(91,0,FW)]
 for (a,x,w),(b,y,v) in zip(keys,keys[1:]):
  if a<=t<=b:return blend(x,y,t,a,b),blend(w,v,t,a,b)
 return keys[-1][1:]
def axes(x,y,w,h,xr,yr):
 ax=Axes(x_range=xr,y_range=yr,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));ax.move_to([x,y,0]);return ax
def curve(ax,x,y,c=GOLD,width=3,op=1):return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=op,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])
class IntroScene(MovingCameraScene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def replace_live(self,m,new):m.submobjects=new.submobjects;return m
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[];self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  self.prepare();self.clock=ValueTracker(self.start);self.world=VGroup();self.ui=VGroup().set_z_index(50);self.add(self.clock,self.world,self.ui);self.set_camera(self.start)
  self.world.add_updater(lambda m:self.update_world(m,self.clock.get_value()));self.ui.add_updater(lambda m:self.replace_live(m,self.anchor_ui(self.screen_ui(self.clock.get_value()),self.clock.get_value())))
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[x for x in [4,8,12,19,28,32,35,39,43,48,54,58,66,71,74,79,81,85] if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):
   self.audit_caption(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.world.clear_updaters();self.ui.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,indent=2),encoding='utf-8')
 def set_camera(self,t):
  x,w=camera_at(t);self.camera.frame.set(width=w).move_to([x,0,0])
 def update_world(self,m,t):self.set_camera(t);return self.replace_live(m,self.geometry(t))
 def anchor_ui(self,g,t):
  x,w=camera_at(t);return g.scale(w/FW,about_point=ORIGIN).shift([x,0,0]).set_z_index(50)
 def caption(self,t):
  line=next(x for x in self.lines if x['start']<=min(t,90.999999)<x['end'])
  return VGroup(*[tx(p,size=25,w=12.2) for p in textwrap.wrap(line['text'],width=60,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-3.3,0]).set_z_index(55)
 def audit_caption(self,t):
  line=next(x for x in self.lines if x['start']<=min(t,90.999999)<x['end'])
  if any(x['start']==line['start'] for x in self.audit):return
  c=self.caption(t);self.audit.append(dict(start=line['start'],end=line['end'],left=float(c.get_left()[0]),right=float(c.get_right()[0]),bottom=float(c.get_bottom()[1]),top=float(c.get_top()[1])))
 def prepare(self):
  self.cache={};self.ui_cache={};self.station_cache={}
  self.history_t=np.linspace(0,2,161);self.history_q=np.interp(self.history_t,MODEL.times,MODEL.states[:,0])
 def ordinary(self,t):
  q,w=MODEL.state_at(max(t,0));return float(q),float(I*w)
 def pend(self,t,x=-2.3,y=1.8,L=3.2,forces=0):
  q,p=self.ordinary(t);return rig(0,pivot=(x,y,0),L=L,theta=q,omega=p/I,forces=forces)
 def level(self,ax,r=RB,c=BLUE,op=.5):
  key=(tuple(ax.get_center()),ax.width,ax.height,r,c,op)
  if key not in self.cache:self.cache[key]=VGroup(*[curve(ax,q,p,c,2,op) for q,p in contour(r)])
  return self.cache[key].copy()
 def portrait(self,t,x=0,y=-.1,w=8.2,h=3.7):
  ax=axes(x,y,w,h,[-.9,.9,.3],[-8,8,2]);q,p=self.ordinary(t);return VGroup(ax,self.level(ax),Dot(ax.c2p(q,p),color=GOLD,radius=.075)),ax
 def arrows(self,ax):
  key=('field',tuple(ax.get_center()),ax.width,ax.height)
  if key not in self.cache:
   vectors=[]
   for q in np.linspace(-.7,.7,7):
    for p in np.linspace(-6,6,7):
     v=field(np.array([q,p]));d=ax.c2p(q+.03*v[0],p+.03*v[1])-ax.c2p(q,p);vectors.append((ax.c2p(q,p),d))
   scale=.42/max(np.linalg.norm(d) for _,d in vectors);self.cache[key]=VGroup(*[arr(a,d*scale,BLUE,.45) for a,d in vectors])
  return self.cache[key].copy()
 def region(self,i,t):
  _,name,subtitle,c=REGIONS[i];g=VGroup(tx(name,0,2.78,31,c,w=10),tx(subtitle,0,2.2,22,MUTED,w=10))
  g.add(RoundedRectangle(width=11.8,height=5.75,corner_radius=.2,color=c,stroke_width=1,stroke_opacity=.13).move_to([0,.1,0]))
  u=t*.65
  if i==0:
   g.add(self.pend(u,forces=1 if t>=12 else 0),eq(r'F=ma',2.7,.75,58,c=BLUE,w=5),tx('力 + 초기조건 → 운동 예측'.replace('力','힘'),2.7,-.5,25,w=5.8))
  elif i==1:
   g.add(self.pend(u,x=-3.6,y=1.65,L=3.2))
   q,p=self.ordinary(u);E=float(H(.65,0));vals=[p*p/(2*I),float(H(q,0))]
   for y,v,col in [(1.35,vals[0],BLUE),(.65,vals[1],GOLD)]:
    g.add(Line([-.6,y,0],[4.6,y,0],color=MUTED,stroke_width=10,stroke_opacity=.2))
    if v/E>.00001:g.add(Line([-.6,y,0],[-.6+5.2*v/E,y,0],color=col,stroke_width=10))
   g.add(eq(r'L=T-V',2,-.05,37,c=GOLD,w=5))
   ax=axes(2,-1.25,5.3,1.65,[0,2,.5],[-1,1,.5]);g.add(ax)
   for e in [-.22,0,.22]:g.add(curve(ax,self.history_t,self.history_q+e*np.sin(np.pi*self.history_t/2),GOLD if e==0 else BLUE,3 if e==0 else 1.5,1 if e==0 else .35))
   g.add(eq(r'\delta S=0',-3.6,-2.2,31,c=GREEN,w=4))
  elif i==2:
   g.add(self.pend(u,x=-3.8,y=1.7,L=3.2));v,ax=self.portrait(u,x=2.1,y=-.15,w=5.5,h=3.4);g.add(v,eq(r'(\theta,p_\theta)',2.1,-2.3,35,c=GREEN,w=5),Arrow([-.9,0,0],[-.25,0,0],color=MUTED))
  elif i==3:
   v,ax=self.portrait(u,w=8.2,h=3.45)
   for r in [.06,.18]:v.add(self.level(ax,r,BLUE,.22))
   g.add(self.arrows(ax),v,eq(r'H(\theta,p_\theta)',0,-2.3,37,c=GOLD,w=8))
  elif i==4:
   ax=axes(-2.6,-.1,5.5,3.5,[-.9,.9,.3],[-8,8,2]);g.add(ax,self.level(ax,RB,BLUE,.25));b,pts=packet(float(np.clip((t-58)*.5,0,4)))
   g.add(Polygon(*[ax.c2p(q,p) for q,p in INITIAL],color=BLUE,fill_opacity=0,stroke_opacity=.6),Polygon(*[ax.c2p(q,p) for q,p in b],color=GREEN,fill_color=GREEN,fill_opacity=.25),*[Dot(ax.c2p(q,p),radius=.025,color=GOLD) for q,p in pts],eq(r'A(t)=A(0)',-2.6,-2.25,31,c=GREEN,w=5),tx('連続 대칭'.replace('連続','연속'),3,1.1,28,c=BLUE,w=4),Arrow([3,.65,0],[3,-.25,0],color=MUTED),tx('보존량',3,-.65,34,c=GOLD,w=4),tx('뇌터 정리',3,-1.65,25,c=GREEN,w=4))
  else:
   ax=axes(0,.2,8.8,2.3,[-5,5,2],[-.85,.85,.4]);z=psi(X,(t-66)*.4);g.add(ax,curve(ax,X,z.real,BLUE,3),curve(ax,X,z.imag,GOLD,2.5),eq(r'|\psi\rangle',-4.3,1.4,35,c=PURPLE,w=2),eq(r'\hat H:\quad i\hbar\partial_t|\psi\rangle=\hat H|\psi\rangle',0,-1.8,37,c=PURPLE,w=10),tx('같은 좌표 변환이 아닌, 새로운 물리 이론',0,-2.45,22,MUTED,w=10))
  return g.shift([14*i,0,0])
 def geometry(self,t):
  x,w=camera_at(t);g=VGroup()
  # All stations remain fixed in one world; cull only wholly off-screen stations.
  for i in range(5):g.add(Line([14*i+5.8,-2.55,0],[14*(i+1)-5.8,-2.55,0],color=GOLD,stroke_width=2,stroke_opacity=.3))
  g.add(DashedLine([61.8,-2.55,0],[64.2,-2.55,0],color=PURPLE,stroke_opacity=.65))
  for i in range(6):
   if abs(14*i-x)<w/2+7:
    active=int(np.clip(round(x/14),0,5))
    if not (74<=t<=85) and i==active:g.add(self.region(i,t))
    else:
     if i not in self.station_cache:self.station_cache[i]=self.region(i,[16,30,44,52,62,70][i])
     g.add(self.station_cache[i])
  return g
 def screen_ui(self,t):
  line=next(x for x in self.lines if x['start']<=min(t,90.999999)<x['end']);stage=0 if t<24 else 1 if t<35 else 2 if t<48 else 3 if t<58 else 4 if t<66 else 5
  overview=79<=t<=85
  key=(line['id'],stage,overview,85<=t)
  if key not in self.ui_cache:
   g=VGroup(tx('CHAPTER 00  /  INTRO',-4.9,3.6,18,MUTED,w=4.2),tx('고전역학의 발전을 따라가는 지도',3.3,3.6,22,w=6.3),Line([-6.4,3.25,0],[6.4,3.25,0],color=MUTED,stroke_opacity=.25),RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]),self.caption(t))
   if overview:
    g.add(tx('고전역학은 어떻게 발전해 왔는가?',0,2.65,33,c=GOLD,w=12),tx('하나의 운동, 여러 수학적 표현',0,-1.25,31,w=12),tx('그 표현 속에서 무엇을 새롭게 발견할 수 있을까?',0,-2.2,25,MUTED,w=12))
    for i,(number,name,_,c) in enumerate(REGIONS):
     xx=(14*i-35)*FW/87;g.add(tx(name,xx,.95,18,c,w=2.1),tx(number,xx,1.45,20,MUTED,w=1.8),Dot([xx,1.16,0],radius=.045,color=c))
   elif t<10:g.add(tx('이미 예측할 수 있었는데, 왜 새로운 역학이 필요했을까?',0,-2.65,26,c=GOLD,w=12))
   elif t>=85:g.add(tx('하나의 진자에서 출발하는 탐험',0,-2.65,27,c=GOLD,w=12))
   self.ui_cache[key]=g
  return self.ui_cache[key].copy()
