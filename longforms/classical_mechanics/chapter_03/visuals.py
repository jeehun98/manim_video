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
from mechanics import MODEL,I,G,ELL,PERIOD,QUARTER,FIXED_THETA,V0,V,lagrangian,momentum,hamiltonian,contour
config.background_color=BG;config.frame_width=128/9;config.frame_height=8
def axes(x,y,w,h,xrange,yrange):
 a=Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a

def curve(ax,x,y,c=GOLD,width=3,opacity=1):
 return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=opacity,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])


class ChapterScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('CHAPTER 03  /  PHASE SPACE',-4.9,3.6,18,MUTED,w=4.2),tx('새로운 공간에 기록된 운동',3.4,3.6,22,w=6),Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  self.prepare()
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[8,11,16,21,25,33,37,41,48,56,63,70,73,79,82,90,97,102,106,110,116,121,125,132,137,143,151,158,162,165,172,179,183,188,191,196,203,207,211,217,222,227,234,240,245,252,261,270,278,281,285,291,295]
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
  self.state=axes(2.7,.2,6.2,3.7,[-.9,.9,.3],[-2,2,1])
  self.phase=axes(2.7,.2,6.2,3.7,[-1.2,1.2,.4],[-9,9,3])
  self.bigphase=axes(0,.2,10,4.2,[-1.2,1.2,.4],[-9,9,3])
  self.slope=axes(-1.9,.15,7,3.9,[-1.8,1.8,.6],[-9,7,4])
  self.left=axes(-3.5,.3,5.2,3.7,[-1.8,1.8,.6],[-9,7,4])
  self.right=axes(3.5,.3,5.2,3.7,[-7,7,2],[0,8,2])
  self.mini=axes(4.5,.2,3.2,2.9,[-.9,.9,.3],[-7,7,3])
  self.history_ax=axes(0,.1,3.2,2.6,[0,PERIOD,1],[-.9,.9,.3])
  self.sample=np.linspace(0,PERIOD,141)
 def phase_view(self,ax,u,canonical=True,reveal=1,others=False):
  g=VGroup(ax)
  if others:
   for amp in [.35,.95,1.1]:
    th,p=contour(amp,canonical);g.add(curve(ax,th,p,BLUE,1.5,.2))
  th,p=contour(.65,canonical)
  if reveal>=1:g.add(curve(ax,th,p,BLUE,2.5,.65))
  elif reveal>.01:
   tt=np.linspace(0,PERIOD*reveal,max(3,int(141*reveal)));q=np.interp(tt,MODEL.times,MODEL.states[:,0]);v=np.interp(tt,MODEL.times,MODEL.states[:,1]);g.add(curve(ax,q,v*(I if canonical else 1),BLUE))
  q,w=MODEL.state_at(u);g.add(Dot(ax.c2p(q,w*(I if canonical else 1)),radius=.08,color=GOLD))
  return g
 def tangent(self,ax,w):
  p=float(momentum(w));l=float(lagrangian(FIXED_THETA,w));intercept=l-p*w
  pts=[]
  for x in [-1.8,1.8]:
   y=p*x+intercept
   if -9<=y<=7:pts.append(ax.c2p(x,y))
  if abs(p)>1e-8:
   for y in [-9,7]:
    x=(y-intercept)/p
    if -1.8<x<1.8:pts.append(ax.c2p(x,y))
  return Line(pts[0],pts[1],color=GOLD,stroke_width=3) if len(pts)>=2 else VGroup()
 def labels(self,t):
  g=VGroup()
  if self.index==1:
   if t<16:g.add(tx('위치만으로 운동을 정할 수 있을까?',0,2.7,31),eq(r'\theta=\theta_0',3.3,.7,48,c=GOLD,w=5))
   else:g.add(tx('같은 각도, 서로 다른 속도',0,2.7,31),tx('왼쪽으로',-3.4,-1.9,25,BLUE,w=4),tx('오른쪽으로',3.4,-1.9,25,GREEN,w=4))
   if t>=25:g.add(tx('순간 상태 = 위치 + 속도',0,-2.5,28,GOLD))
  elif self.index==2:
   g.add(tx('이상적인 비선형 진자',-4.5,2.75,20,MUTED,w=4),eq(r'\theta',5.9,-.1,31,c=GOLD,w=1),eq(r'\omega=\dot\theta',2.7,2.55,31,c=BLUE,w=3))
   if t<48:g.add(eq(r'(\theta,\omega)',-3.9,-2.1,43,c=GREEN,w=4))
   else:g.add(tx('한 점은 순간 상태, 궤적은 운동',1.4,-2.4,28,GREEN,w=10))
   if t>=63:g.add(tx('각도·각속도 상태 공간',2.7,2.95,23,MUTED,w=6))
  elif self.index==3:
   g.add(tx('라그랑지안',-4.4,2.65,26,GOLD,w=4),eq(r'L=T-V',-4.4,1.7,40,c=GOLD,w=4),tx('위치와 속도의 함수',-4.4,.9,22,MUTED,w=4))
   if t>=82:g.add(tx('작용',0,2.65,26,BLUE,w=4),eq(r'S=\int L\,dt',0,1.6,39,c=BLUE,w=4),tx('부호를 포함한 누적',0,-1.8,23,MUTED,w=4))
   if t>=90:g.add(tx('정지 조건',4.4,2.65,26,GREEN,w=4),eq(r'\delta S=0',4.4,1.7,43,c=GREEN,w=4),tx('작용의 일차 변화가 0',4.4,-1.8,23,MUTED,w=4))
   if t>=97:g.add(eq(r'\delta S=0\ \Rightarrow\ \ddot\theta=-\frac{g}{\ell}\sin\theta',0,-2.35,35,c=INK,w=11))
  elif self.index==4:
   g.add(tx('각도 θ를 고정하고 속도만 바꾼다',0,2.8,29),eq(r'L(\theta_0,\omega)',-3.8,2.15,33,c=GOLD,w=4),eq(r'\omega',1.9,-2.05,31,c=BLUE,w=1))
   if t>=110:g.add(tx('접선의 기울기',4.2,1.5,27,GOLD,w=4))
   if t>=116:g.add(eq(r'p_\theta=\frac{\partial L}{\partial\omega}=I\omega',4.2,.4,37,c=GREEN,w=4.4),tx('각도에 대응하는 정준운동량',4.2,-.55,22,w=4.6))
   if t>=125:g.add(eq(r'(\theta,\omega)\ \longrightarrow\ (\theta,p_\theta)',0,-2.5,37,c=GREEN,w=12))
   else:g.add(tx('이 진자의 관성모멘트 I는 일정',0,-2.5,22,MUTED,w=11))
  elif self.index==5:
   g.add(tx('각도 θ 고정 · 속도 함수의 접선',-3.3,2.85,25,w=6),eq(r'L(\theta_0,\omega)',-3.5,2.3,32,c=GOLD,w=5),eq(r'\omega',-3.5,-1.85,28,c=BLUE,w=1))
   if t<158:
    g.add(tx('입력값 ω',3.3,1.5,29,BLUE,w=5),eq(r'p_\theta=I\omega',3.3,.55,46,c=GREEN,w=5),tx('그 지점에서의 기울기',3.3,-.4,27,GOLD,w=5))
    if t>=143:g.add(tx('기울기를 새로운 입력 변수로',3.3,-1.25,26,w=5.5))
   else:
    g.add(tx('르장드르 변환',3.5,2.85,29,GREEN,w=6),eq(r'H(\theta_0,p_\theta)',3.5,2.3,32,c=GREEN,w=5),eq(r'p_\theta',6.25,-1.9,28,c=BLUE,w=1.3),eq(r'H=p_\theta\omega-L',0,-2.1,44,c=GREEN,w=11))
    if t>=172:g.add(tx('속도에서 운동량으로 · 같은 계의 정보를 재표현',0,-2.55,20,MUTED,w=12))
    else:g.add(tx('접선의 세로축 절편 = −H',0,-2.55,20,GOLD,w=12))
   if t<158:g.add(tx('단순한 축 이름 교체가 아니라, 함수를 다시 구성한다',0,-2.5,23,MUTED,w=12))
  elif self.index==6:
   g.add(tx('이상적인 비선형 진자',-4.5,2.75,20,MUTED,w=4),eq(r'\theta',5.9,-.1,31,c=GOLD,w=1),eq(r'\omega' if t<191 else r'p_\theta=I\omega',2.7,2.7,32,c=BLUE,w=4))
   if t>=196:g.add(tx('위상 공간',2.7,2.15,25,GREEN,w=5))
   if 211<=t<217:g.add(tx('끝점: pθ = 0   /   최저점: |pθ| 최대',.5,-2.45,26,GOLD,w=12))
   elif t>=234:g.add(eq(r'(q_1,\ldots,q_n,p_1,\ldots,p_n)\qquad\dim\Gamma=2n',0,-2.45,33,c=GREEN,w=12))
   else:g.add(tx('한 점은 상태 · 닫힌 궤적은 왕복 운동',1,-2.45,26,GREEN,w=11))
  elif self.index==7:
   g.add(tx('NEWTON',-4.5,2.75,24,BLUE,w=3.5),tx('LAGRANGE',0,2.75,24,GOLD,w=3.5),tx('PHASE SPACE',4.5,2.75,24,GREEN,w=3.5))
   if t>=252:g.add(eq(r'\delta S=0',0,1.95,34,c=GOLD,w=3.5))
   if t>=261:g.add(eq(r'(\theta,p_\theta)',4.5,1.95,32,c=GREEN,w=3.5))
   g.add(tx('힘과 운동의 변화',-4.5,-1.8,22,BLUE,w=3.8),tx('작용의 정지 조건',0,-1.8,22,GOLD,w=3.8),tx('상태와 궤적',4.5,-1.8,22,GREEN,w=3.8),tx('동일한 진자의 운동 · 표현마다 드러나는 다른 구조',0,-2.5,27,w=12))
  else:
   if t<295:
    g.add(tx('현재 상태에서, 다음 순간의 변화로',0,2.85,30),eq(r'\theta',5.45,-.05,30,c=GOLD,w=1),eq(r'p_\theta',.25,2.65,30,c=BLUE,w=1.5),tx('이미 알고 있는 운동법칙을 새로운 함수로 표현할 수 있을까?',0,-2.5,24,MUTED,w=12))
   else:g.add(eq(r'H(q,p)',0,.65,83,c=GREEN,w=9),tx('상태의 시간 변화를 생성하는 함수',0,-1,31,w=11))
  return g
 def geometry(self,t):
  if self.index==1:
   if t<16:return rig(t*.45,pivot=(-2.5,2.1,0),L=3.4)
   g=VGroup()
   for x,w,c in [(-3.4,-1.0,BLUE),(3.4,.55 if t<21 else 1.4,GREEN)]:
    th=.25;pivot=(x,2.1,0);b=bobpoint(th,pivot,3.2);g.add(rig(0,pivot,3.2,theta=th),arr(b,np.array([np.cos(th),np.sin(th),0])*w*.8,c))
   return g
  if self.index==2:
   u=0 if t<48 else (t-48)*.6;g=VGroup(rig(u,pivot=(-4.3,2.15,0),L=3.35))
   g.add(self.phase_view(self.state,u,False,reveal=np.clip((t-48)/8,0,1)))
   if 41<=t<48:
    q,w=MODEL.state_at(0);p=self.state.c2p(q,w);g.add(DashedLine(p,self.state.c2p(q,0),color=GOLD),DashedLine(p,self.state.c2p(0,w),color=BLUE))
   return g
  if self.index==3:
   u=t-70;th,w=MODEL.state_at(u);E=V(.65);T=.5*I*w*w;pot=V(th);g=VGroup()
   for x,val,c in [(-5,T/E,BLUE),(-3.8,pot/E,GOLD)]:
    if val>.001:g.add(Rectangle(width=.6,height=1.5*val,fill_color=c,fill_opacity=.7,stroke_width=0).move_to([x,-.8+.75*val,0]))
   if t>=82:
    tt=np.linspace(0,PERIOD,81);qs=np.interp(tt,MODEL.times,MODEL.states[:,0]);ws=np.interp(tt,MODEL.times,MODEL.states[:,1]);l=lagrangian(qs,ws);a=axes(0,.0,3.3,1.7,[0,PERIOD,1],[-5,5,2]);g.add(a,curve(a,tt,l,GOLD,2))
    for j in range(24):
     x0=PERIOD*j/24;x1=PERIOD*(j+1)/24;v=float(np.interp((x0+x1)/2,tt,l));g.add(Polygon(a.c2p(x0,0),a.c2p(x1,0),a.c2p(x1,v),a.c2p(x0,v),stroke_width=0,fill_color=GREEN if v>0 else RED,fill_opacity=.25))
   if t>=90:
    a=axes(4.4,0,3.3,1.7,[-1,1,.5],[0,1.3,.5]);x=np.linspace(-1,1,51);g.add(a,curve(a,x,.15+x*x,GREEN),Line(a.c2p(-.3,.15),a.c2p(.3,.15),color=GOLD),Dot(a.c2p(0,.15),color=GOLD,radius=.06))
   return g
  if self.index==4:
   a=self.slope;w=1.15*np.sin((t-102)*.3);x=np.linspace(-1.8,1.8,101);l=float(lagrangian(FIXED_THETA,w));g=VGroup(a,curve(a,x,lagrangian(FIXED_THETA,x),BLUE),Dot(a.c2p(w,l),color=GOLD,radius=.08),DashedLine(a.c2p(w,l),a.c2p(w,0),color=MUTED))
   if t>=110:g.add(self.tangent(a,w))
   return g
  if self.index==5:
   a=self.left;w=1.05+.3*np.sin((t-132)*.25);p=float(momentum(w));l=float(lagrangian(FIXED_THETA,w));h=float(hamiltonian(FIXED_THETA,p));x=np.linspace(-1.8,1.8,101)
   g=VGroup(a,curve(a,x,lagrangian(FIXED_THETA,x),BLUE),self.tangent(a,w),Dot(a.c2p(w,l),radius=.075,color=GOLD),DashedLine(a.c2p(w,l),a.c2p(w,0),color=MUTED))
   if t>=158:
    b=self.right;ps=np.linspace(-7,7,101);g.add(b,curve(b,ps,hamiltonian(FIXED_THETA,ps),GREEN),Dot(b.c2p(p,h),radius=.075,color=GOLD),Dot(a.c2p(0,-h),radius=.065,color=GREEN),arr([-.5,.3,0],[1,0,0],GREEN))
   return g
  if self.index==6:
   u=(t-188)*.65;canonical=t>=191;ax=self.phase if canonical else self.state
   g=VGroup(rig(u,pivot=(-4.3,2.15,0),L=3.35),self.phase_view(ax,u,canonical,1,t>=227))
   if 211<=t<217:
    for q,p in [(.65,0),(-.65,0),(0,np.sqrt(2*I*V(.65))),(0,-np.sqrt(2*I*V(.65)))]:g.add(Dot(ax.c2p(q,p),radius=.065,color=GREEN))
   return g
  if self.index==7:
   u=(t-240)*.65;g=VGroup(rig(u,pivot=(-4.5,1.9,0),L=2.2,forces=1))
   if t>=252:
    a=self.history_ax;tt=self.sample;q=np.interp(tt,MODEL.times,MODEL.states[:,0]);g.add(a,curve(a,tt,q,GOLD))
    for e in [-.18,.18]:g.add(curve(a,tt,q+e*np.sin(np.pi*tt/PERIOD),BLUE,1.3,.4))
    q0,_=MODEL.state_at(u%PERIOD);g.add(Dot(a.c2p(u%PERIOD,q0),radius=.06,color=GOLD))
   if t>=261:g.add(self.phase_view(self.mini,u,True))
   return g
  if t>=295:return VGroup()
  u=(t-278)*.65 if t<281 else 1.95;g=self.phase_view(self.bigphase,u,True)
  if t>=285:
   # Analytical Hamiltonian vector field; arrows are revealed as a representation, not new randomness.
   for q in [-.9,-.45,0,.45,.9]:
    for p in [-6,-3,0,3,6]:
     v=self.bigphase.c2p(q+.03*p/I,p-.03*G*ELL*np.sin(q))-self.bigphase.c2p(q,p);v=v/max(np.linalg.norm(v),.001)*.28
     if t>=291:g.add(arr(self.bigphase.c2p(q,p),v,BLUE,.4))
  return g
