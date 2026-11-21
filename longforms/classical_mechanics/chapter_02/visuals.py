"""Lagrange: one pendulum → coordinates → energies → histories → stationary action."""
from pathlib import Path
import sys,importlib.util,json,textwrap
import numpy as np
from manim import *
R=Path(__file__).resolve().parent
P=R.parent/'chapter_01'
sys.path.append(str(P))
spec=importlib.util.spec_from_file_location('classical_ch01_visuals',P/'visuals.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
tx,eq,ball,arr,bobpoint,rig=base.tx,base.eq,base.ball,base.arr,base.bobpoint,base.rig
BG,INK,MUTED,BLUE,GOLD,GREEN,RED=base.BG,base.INK,base.MUTED,base.BLUE,base.GOLD,base.GREEN,base.RED
from variational import MODEL,TIME,DURATION,THETA,OMEGA,EPS,ACTIONS,S0,history,energies,lagrangian,action,action_at
config.background_color=BG;config.frame_width=128/9;config.frame_height=8

def axes(x,y,w,h,xrange,yrange):
 a=Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a

def curve(ax,x,y,c=GOLD,width=3,opacity=1):
 return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=opacity,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])

def endpoint_dots(ax):return VGroup(*[Dot(ax.c2p(t,q),radius=.065,color=INK) for t,q in [(0,THETA[0]),(DURATION,THETA[-1])]])

def bars(th,om):
 T,V=energies(th,om);E=.5*MODEL.length**2*MODEL.states[0,1]**2+MODEL.g*MODEL.length*(1-np.cos(.65));T=float(T/E);V=float(V/E)
 g=VGroup()
 for y,value,c in [(1.45,T,BLUE),(.55,V,GOLD)]:
  g.add(RoundedRectangle(width=4.8,height=.34,corner_radius=.06,stroke_color=MUTED,stroke_opacity=.3,fill_opacity=0).move_to([3.4,y,0]))
  if value>.001:g.add(Rectangle(width=4.8*value,height=.32,stroke_width=0,fill_color=c,fill_opacity=.8).move_to([1+2.4*value,y,0]))
 return g

class ChapterScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('CHAPTER 02  /  LAGRANGE',-4.9,3.6,18,MUTED,w=4.2),tx('하나의 원리로 설명되는 운동',3.4,3.6,22,w=6),Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  self.prepare()
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[8,13,18,27,36,40,46,51,54,58,65,72,78,85,87,91,96,100,102,104,109,111,113,116,121,126,133,142,150,155,160,164,169,175]
  events=sorted(set([self.start,self.end]+[l['start'] for l in self.lines if self.start<l['start']<self.end]+[x for x in extra if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  l=next(x for x in self.lines if x['start']<=t<x['end'])
  if l!=self.current:
   self.remove(self.caption);self.current=l
   parts=textwrap.wrap(l['text'],width=52,break_long_words=False,break_on_hyphens=False)
   self.caption=VGroup(*[tx(p,size=25,w=12.2) for p in parts]).arrange(DOWN,buff=.1).move_to([0,-3.3,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=l['start'],end=l['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1])))
  self.remove(self.static);self.static=self.labels(t);self.add(self.static)
  for m in self.static:
   assert m.get_left()[0]>-6.8 and m.get_right()[0]<6.8 and m.get_bottom()[1]>-2.75 and m.get_top()[1]<3.15,('label safe area',self.index,t)
 def prepare(self):
  self.ts=np.linspace(0,DURATION,101)
  self.path_ax=axes(2,.1,7.3,3.5,[0,1.2,.2],[-1.1,1.1,.5])
  self.small_path=axes(-3.5,.65,5.2,2.55,[0,1.2,.2],[-1.1,1.1,.5])
  self.l_ax=axes(3.05,.35,5.7,3,[0,1.2,.2],[-7,13,5])
  self.action_axes={}
  for k in (1,2,3):
   peak=float(ACTIONS[k].max()-S0)
   self.action_axes[k]=axes(3.25,.4,5,2.8,[-.35,.35,.1],[S0-peak*.15,S0+peak*1.2,peak/3])
  self.phase_ax=axes(3.6,.25,4.1,3.1,[-.8,.8,.4],[-6,6,3])
 def labels(self,t):
  g=VGroup()
  if self.index==1:
   g.add(tx('이상적인 진자 · 마찰 무시',-4.6,2.75,20,MUTED,w=4))
   if 8<=t<13:g.add(tx('가로 x, 세로 y',3.4,1.5,30,BLUE,w=4))
   if t>=13:g.add(eq(r'\theta',3.1,1.3,64,c=GOLD,w=2),tx('각도 하나로 위치를 표현',3.1,.3,29,w=5))
   if t>=18:g.add(tx('일반화 좌표',3.1,-.65,32,GREEN,w=5))
  elif self.index==2:
   g.add(tx('이상적인 진자 · 에너지 상대값',-4.1,2.75,20,MUTED,w=4.8),tx('운동에너지 T',1.85,2.0,25,BLUE,w=3),tx('위치에너지 V',1.85,1.05,25,GOLD,w=3))
   if t<36:g.add(tx('높이 ↔ 속력',3.3,-.55,30,w=5))
   elif t<40:g.add(eq(r'E=T+V',3.4,-.6,52,c=GREEN,w=5),tx('합은 일정하다',3.4,-1.5,27,GREEN,w=5))
   elif t<46:g.add(eq(r'T-V',3.4,-.6,60,c=INK,w=5),tx('같은 에너지, 다른 결합',3.4,-1.5,27,w=5))
   else:g.add(eq(r'L=T-V',3.4,-.6,52,c=GOLD,w=5),tx('라그랑지안 · 순간마다 달라지는 값',3.4,-1.65,25,GOLD,w=5.5))
  elif self.index==3:
   if t<58:g.add(eq(r'L=T-V',3.2,1,52,c=GOLD),tx('이 함수에서 운동을 어떻게 얻을까?',2.5,-.3,29,w=7))
   else:
    g.add(tx('공간의 길이 아니라, 시간에 따른 각도',1.7,2.75,28,w=8),eq(r'\theta(t)',-1.9,2.05,32,c=GOLD,w=2),tx('시간 t',5.65,-1.9,23,MUTED,w=2),tx('실제 운동',-4.6,2.1,22,GOLD,w=3))
    if t>=65:g.add(tx('같은 시작·끝 시각과 위치',1.7,-2.35,26,GREEN,w=8),tx('금색: 실제 경로   파랑: 가상 경로',1.7,2.1,21,MUTED,w=7))
  elif self.index==4:
   g.add(tx('운동 경로',-3.5,2.7,28,GOLD,w=5),eq(r'\theta(t),\ \dot\theta(t)',-3.5,2.1,33,w=5),tx('각도와 각속도 → 순간의 L',3,2.7,25,BLUE,w=6),eq(r'L(t)',.35,2.1,30,w=1.5),tx('시간 t',5.7,-1.15,20,MUTED,w=2))
   g.add(tx('양의 기여',1.5,-1.65,22,GREEN,w=3),tx('음의 기여',4.6,-1.65,22,RED,w=3))
   if t>=85:g.add(eq(r'S=\int_{t_0}^{t_1}L\,dt',-3.5,-1.85,42,c=GREEN,w=5),tx('작용 · 부호를 포함한 누적',2.8,-2.3,25,GREEN,w=6))
   if t>=87:g.add(tx('다른 가상 경로 → 다른 작용',-3.5,-.95,22,BLUE,w=5))
  elif self.index==5:
   if t>=113:
    g.add(eq(r'\delta S=0',-3.4,1,58,c=GREEN,w=4),eq(r'\frac{d}{dt}\frac{\partial L}{\partial\dot\theta}-\frac{\partial L}{\partial\theta}=0',2.4,1,43,w=6.8),eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',0,-.7,51,c=GOLD,w=6),tx('작용의 정지 조건 → 운동방정식',0,-2.2,29,GREEN))
   else:
    mode=self.variation(t)[1]
    g.add(tx('끝점은 고정, 중간 움직임만 변형',-3.5,2.7,25,w=5.7),eq(r'\theta_\varepsilon(t)',-3.5,2.05,34,c=BLUE,w=4),eq(r'S(\varepsilon)',3.3,2.7,36,c=GREEN,w=4),tx('경로 변형 ε',4.7,-1.5,22,MUTED,w=3))
    g.add(tx(f'변형 {mode} · 실제 경로의 작용 S(0) = {S0:.3f}',3.25,-2.1,22,w=5.7),tx('끝점이 고정된 모든 허용 미소 변형에서 정지' if t>=109 else '선택한 변형의 예 · 정지 ≠ 항상 최소',0,-2.55,20,MUTED,w=12))
    if t>=104:g.add(tx('실제 운동에서 접선은 수평',3.25,2.05,24,GREEN,w=5))
    if t>=109:g.add(eq(r'\delta S=0',-3.5,-1.35,43,c=GREEN,w=4),tx('작용의 정지 조건',-3.5,-2.05,25,GREEN,w=5))
  elif self.index==6:
   if t<126:
    g.add(tx('서로 다른 표현, 같은 운동방정식',0,2.7,31),eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',-3.4,1,43,c=BLUE,w=5),eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',3.4,1,43,c=GOLD,w=5),tx('뉴턴의 법칙',-3.4,2,26,BLUE,w=5),tx('작용의 정지 조건',3.4,2,26,GOLD,w=5),tx('같은 초기조건 → 같은 운동',0,-2.25,29,GREEN))
   elif t<150:
    g.add(tx('NEWTON',-3.3,2.75,26,BLUE,w=5),tx('LAGRANGE',3.3,2.75,26,GOLD,w=5),eq(r'\mathbf F=m\mathbf a',-3.3,1.95,37,c=BLUE,w=4),eq(r'\delta S=0',3.3,1.95,40,c=GREEN,w=4),tx('동일한 초기조건 · 하나의 운동',0,-2.5,24,MUTED))
   else:g.add(tx('운동은 같고, 수학적 표현은 다르다',0,2.75,33,GOLD),tx('작용의 정지 조건 → 운동방정식',3.2,.7,28,GREEN,w=6))
  else:
   if t<169:
    g.add(tx('같은 원리, 다양한 제약과 좌표',0,2.75,30),eq(r'q=(\theta_1,\theta_2,\ldots)',0,1.95,33,c=BLUE,w=7),eq(r'L(q,\dot q)=T-V',0,-1.75,36,c=GOLD,w=7),tx('좌표 배치 개념도 · 연결계 동역학 시뮬레이션 아님',0,-2.4,19,MUTED,w=12))
   elif t<175:g.add(tx('작용의 정지 조건 → 운동방정식',2.8,1.35,30,GREEN,w=6.5),tx('같은 운동을 이해하는 새로운 언어',2.8,.2,27,w=6.5))
   else:g.add(tx('가능한 운동 상태를 한 공간에',2.8,2.75,29,w=7),eq(r'\theta',5.9,.1,29,c=GOLD,w=1),eq(r'p_\theta',3.7,2.15,29,c=BLUE,w=1.5),tx('위치와 운동량',3.6,-1.9,24,MUTED,w=5))
  return g
 def variation(self,t):
  mode=1 if t<100 or t>=104 else 2 if t<102 else 3
  if t<96:e=.28*np.sin((t-91)*1.5)
  elif t<100:e=.28*np.cos((t-96)*1.5)
  elif t<104:e=.22*np.sin((t-100)*2)
  elif t<109:e=.25*(109-t)/5
  else:e=0
  return e,mode
 def geometry(self,t):
  if self.index==1:
   u=t*.65+51;th,om=MODEL.state_at(u);pivot=(-2.7,2.1,0);L=3.6;b=bobpoint(th,pivot,L);g=rig(u,pivot,L)
   if 8<=t<13:g.add(DashedLine(b,[pivot[0],b[1],0],color=BLUE),DashedLine(b,[b[0],pivot[1],0],color=BLUE))
   if t>=13:
    g.add(DashedLine(pivot,np.array(pivot)+[0,-L,0],color=MUTED,stroke_opacity=.4))
    if abs(th)>.01:g.add(Arc(radius=.6,start_angle=-PI/2,angle=th,arc_center=pivot,color=GOLD,fill_opacity=0))
   return g
  if self.index==2:
   u=t-22;th,om=MODEL.state_at(u);g=rig(u,pivot=(-3.6,2.2,0),L=3.5);g.add(bars(th,om))
   T,V=energies(th,om);E=MODEL.g*MODEL.length*(1-np.cos(.65));v=float((T-V)/E)
   if 36<=t<40:g.add(Line([1,-.05,0],[5.8,-.05,0],color=GREEN,stroke_width=8))
   if t>=40:
    g.add(Line([1,-.05,0],[5.8,-.05,0],color=MUTED,stroke_opacity=.25),Dot([3.4+2.4*v,-.05,0],radius=.085,color=GOLD),Line([3.4,-.25,0],[3.4,.12,0],color=MUTED))
   return g
  if self.index==3:
   if t<58:return rig(t-22,pivot=(-3,2.1,0),L=3.4)
   a=self.path_ax;u=min((t-58)/7,1)*DURATION if t<65 else (t-65)/13*DURATION
   th,om=history(0,times=np.array([u]));g=VGroup(a,rig(0,pivot=(-4.7,1.6,0),L=2.75,theta=float(th[0])))
   q=self.ts[self.ts<=max(u,.012)] if t<65 else self.ts
   g.add(curve(a,q,history(times=q)[0]),endpoint_dots(a),Dot(a.c2p(u,th[0]),radius=.075,color=GOLD))
   if t>=65:
    for e,k in [(.22,2),(-.2,3)]:
     h,w=history(e,k,self.ts);g.add(curve(a,self.ts,h,BLUE,2,.5))
     theta=float(history(e,k,np.array([u]))[0][0]);p=bobpoint(theta,(-4.7,1.6,0),2.75);g.add(Dot(p,radius=.065,color=BLUE,fill_opacity=.55))
   return g
  if self.index==4:
   e=0 if t<87 else .18;k=2;a=self.small_path;b=self.l_ax
   h,w=history(e,k,self.ts);l=lagrangian(e,k,self.ts)
   g=VGroup(a,b,curve(a,self.ts,h,GOLD if e==0 else BLUE),endpoint_dots(a),curve(b,self.ts,l,GOLD))
   progress=np.clip((t-78)/7,0,1)
   if t>=85:progress=1
   for j in range(40):
    x0=j*DURATION/40;x1=(j+1)*DURATION/40
    if x1>progress*DURATION:continue
    val=float(lagrangian(e,k,np.array([(x0+x1)/2]))[0]);color=GREEN if val>=0 else RED
    g.add(Polygon(b.c2p(x0,0),b.c2p(x1,0),b.c2p(x1,val),b.c2p(x0,val),stroke_width=0,fill_color=color,fill_opacity=.23))
   # A signed scalar bar condenses the actual integral, not unsigned geometric area.
   if t>=85:
    s=action_at(e,k);g.add(arr([-1,-1.55,0],[.7,0,0],GREEN),Line([.2,-2.0,0],[.2+min(s/2,4),-2.0,0],color=GREEN if s>=0 else RED,stroke_width=7))
   return g
  if self.index==5:
   if t>=113:return VGroup(arr([-1.8,1,0],[.65,0,0],GREEN),arr([0,.35,0],[0,-.5,0],GOLD))
   e,k=self.variation(t);a=self.small_path;b=self.action_axes[k];h,_=history(e,k,self.ts);g=VGroup(a,b,curve(a,self.ts,history(times=self.ts)[0],GOLD,3,.55),curve(a,self.ts,h,BLUE),endpoint_dots(a),curve(b,EPS,ACTIONS[k],GREEN),Dot(b.c2p(e,action_at(e,k)),radius=.075,color=GOLD))
   if t>=104:
    dh=.004;slope=(action_at(e+dh,k)-action_at(e-dh,k))/(2*dh);x0=max(-.35,e-.1);x1=min(.35,e+.1);s=action_at(e,k)
    g.add(Line(b.c2p(x0,s+slope*(x0-e)),b.c2p(x1,s+slope*(x1-e)),color=GOLD,stroke_width=4),DashedLine(b.c2p(0,S0),b.c2p(0,S0+(ACTIONS[k].max()-S0)*1.05),color=MUTED,stroke_opacity=.3))
   return g
  if self.index==6:
   u=t-116
   if t<126:
    return VGroup(rig(u,pivot=(-3.4,.1,0),L=1.65),rig(u,pivot=(3.4,.1,0),L=1.65))
   if t<150:return VGroup(rig(u,pivot=(-3.3,1.05,0),L=2.5,forces=1),rig(u,pivot=(3.3,1.05,0),L=2.5))
   return rig(u,pivot=(-3.1,2.1,0),L=3.4)
  if t<169:
   g=VGroup()
   for origin,angles in [((-4,1.1,0),[.4]),((-.6,1.1,0),[.45,-.6]),((3.1,1.1,0),[.5,-.55,.4])]:
    p=np.array(origin,dtype=float);g.add(Dot(p,radius=.05,color=INK))
    for th in angles:
     q=bobpoint(th,p,.8);g.add(Line(p,q,color=INK),ball(q,r=.1));p=q
   return g
  u=t-116;g=rig(u,pivot=(-3.4,2.1,0),L=3.4)
  if t>=175:
   th,om=MODEL.state_at(u);g.add(self.phase_ax,Dot(self.phase_ax.c2p(th,MODEL.length**2*om),radius=.08,color=GOLD))
  return g
