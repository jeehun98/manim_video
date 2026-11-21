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
from mechanics import MODEL,I,A,EC,H,field,state,contour,patch,PATCH0
config.background_color=BG;config.frame_width=128/9;config.frame_height=8
RB=float(H(.65,0)/EC)
def axes(x,y,w,h,xrange,yrange):
 a=Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a

def curve(ax,x,y,c=GOLD,width=3,opacity=1):
 return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=opacity,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])


class ChapterScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('CHAPTER 04  /  HAMILTON',-4.9,3.6,18,MUTED,w=4.2),tx('에너지 함수로 펼쳐지는 운동',3.4,3.6,22,w=6),Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  self.prepare()
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[15,20,26,34,37,41,47,50,54,57,62,67,73,75,79,84,87,92,100,107,113,117,126,131,136,141,146,151,158,163,168,174,177,182,190,198,201,206,213,219,223,229,234,238,242,247,251,255,264,269,277,281,284,292,297,302,307,312,321,324,329,337,342,346,349,354,361]
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
  self.field_cache={}
  self.phase=axes(2.6,.15,6.1,3.7,[-1.2,1.2,.4],[-9,9,3])
  self.full=axes(0,.15,10.8,4.2,[-1.2,1.2,.4],[-9,9,3])
  self.portrait=axes(2,.15,7.6,3.6,[-np.pi,np.pi,np.pi],[-24,24,8])
  self.mini=axes(4.5,.05,3,2.7,[-1.2,1.2,.6],[-9,9,3])
  self.hist=axes(0,.05,3.1,2.5,[0,3,1],[-.8,.8,.4])
  if self.index in (3,4):
   self.surface_full=self.surface(1)
   self.surface_zero=self.surface(0)
   self.surface_flat=self.surface(1,1)
  if self.index==7:self.energy_labels={k:tx(f'E / Ec = {k/100:.2f}',-4.8,-1.3,22,GOLD,w=3.6) for k in range(10,141)}
 def ordinary(self,t):
  q,w=MODEL.state_at(max(t,0));return q,I*w
 def pend(self,q,p,x=-4.3,y=2.05,L=3.25,forces=False):return rig(0,pivot=(x,y,0),L=L,theta=float(q),omega=float(p/I),forces=1 if forces else 0)
 def level(self,ax,r,c=BLUE,width=2,op=.4):
  return VGroup(*[curve(ax,q,p,c,width,op) for q,p in contour(r)])
 def portrait_view(self,ax,q,p,levels=(RB,),arrows=False):
  g=VGroup(ax)
  for r in levels:g.add(self.level(ax,r,GOLD if abs(r-RB)<1e-6 else BLUE,2,.6 if abs(r-RB)<1e-6 else .2))
  if arrows:g.add(self.direction_field(ax))
  g.add(Dot(ax.c2p(q,p),radius=.08,color=GOLD));return g
 def direction_field(self,ax):
  key=tuple(ax.x_range)+tuple(ax.y_range)+tuple(ax.get_center())+(ax.width,ax.height)
  if key not in self.field_cache:
   group=VGroup();vectors=[]
   for x in np.linspace(-.95,.95,7):
    for y in np.linspace(-7.5,7.5,7):
     v=field(np.array([x,y]));d=ax.c2p(x+.025*v[0],y+.025*v[1])-ax.c2p(x,y);vectors.append((ax.c2p(x,y),d))
   scale=.4/max(np.linalg.norm(d) for _,d in vectors)
   for position,d in vectors:group.add(arr(position,d*scale,BLUE,.45))
   self.field_cache[key]=group
  return self.field_cache[key].copy().set_z_index(-1)
 def project(self,q,p,h=0):
  x=q*1.7;y=p/16*2.0;z=h/A*.55
  return np.array([.9*x+.45*y,-.25*x+.35*y+.9*z-.65,0])
 def surface(self,rise=1,top=0):
  g=VGroup();qs=np.linspace(-2,2,15);ps=np.linspace(-16,16,13);flat=axes(0,.15,10.8,4.2,[-2,2,1],[-16,16,8])
  cells=[]
  for q0,q1 in zip(qs,qs[1:]):
   for p0,p1 in zip(ps,ps[1:]):
    pts=[(1-top)*self.project(q,p,float(H(q,p))*rise)+top*flat.c2p(q,p) for q,p in [(q0,p0),(q1,p0),(q1,p1),(q0,p1)]]
    val=float(H((q0+q1)/2,(p0+p1)/2));color=interpolate_color(ManimColor(BLUE),ManimColor(GOLD),min(val/65,1));poly=Polygon(*pts,stroke_color=BLUE,stroke_width=.5,stroke_opacity=.38*(1-top),fill_color=color,fill_opacity=.24*(1-top));cells.append((p0-q0,poly))
  for _,poly in sorted(cells,key=lambda x:x[0]):g.add(poly)
  return g
 def energy_ratio(self,t):
  if t<251:r=.15+.85*np.clip((t-234)/17,0,1)
  elif t<255:r=1
  elif t<264:r=1+.3*(t-255)/9
  else:r=1.3
  return round(r,2)
 def labels(self,t):
  g=VGroup()
  if self.index==1:
   if t<15:g.add(tx('현재 상태에서 다음 순간의 변화로',0,2.7,30))
   elif t<34:g.add(tx('르장드르 변환',0,2.7,30,GOLD),eq(r'p_\theta=\frac{\partial L}{\partial\omega}',3.4,1.45,39,c=BLUE,w=5),eq(r'H=p_\theta\omega-L',3.4,.15,44,c=GREEN,w=5),tx('속도 대신 운동량을 입력으로',3.4,-1,25,w=5.4))
   else:g.add(tx('HAMILTONIAN',0,2.4,29,GREEN),eq(r'H(q,p)',0,.8,77,c=GOLD,w=9),tx('해밀토니안',0,-1,33,w=8))
   if t<15:g.add(tx('다음 순간은 어느 방향으로?',0,-2.4,30,GOLD))
  elif self.index==2:
   g.add(tx('이상적인 강체 막대 진자 · 마찰 없음',-3.5,2.75,20,MUTED,w=6))
   if t<50:g.add(eq(r'H=T+V',3.3,1.5,54,c=GREEN,w=5),tx('전체 역학적 에너지',3.3,2.4,26,GREEN,w=5))
   else:g.add(eq(r'L=T-V',1.2,1.8,40,c=GOLD,w=3.8),eq(r'H=T+V',4.9,1.8,40,c=GREEN,w=3.8),tx('합은 일정 · 차이는 변화',3,-1.7,27,w=6))
   g.add(tx('운동에너지 T',3.2,.55,23,BLUE,w=5),tx('위치에너지 V',3.2,-1.15,23,GOLD,w=5))
   if t>=67:g.add(tx('에너지에서 운동의 변화를 얻으려면?',0,-2.45,29,GOLD))
  elif self.index==3:
   g.add(tx('상태마다 에너지 높이를 부여한다',0,2.85,30),eq(r'H(\theta,p_\theta)=\frac{p_\theta^2}{2I}+mg\ell(1-\cos\theta)',0,-2.25,38,c=GREEN,w=12),tx('각도 θ',4.8,-1.6,23,GOLD,w=2),tx('운동량 pθ',-4.7,-1.35,23,BLUE,w=2.5))
   if t>=100:g.add(tx('에너지 H',0,2.25,24,GOLD,w=3))
  elif self.index==4:
   if t<126:g.add(tx('같은 높이에서 곡면을 자르면',0,2.85,31),tx('수평 단면 → 같은 에너지의 상태',0,-2.4,27,GOLD))
   else:
    g.add(tx('같은 에너지의 등고선',2.6,2.75,29,GREEN,w=6),eq(r'\theta',5.9,-.05,29,c=GOLD,w=1),eq(r'p_\theta',2.65,2.2,30,c=BLUE,w=1.5),tx('이상적인 진자 · 전체 에너지 일정',0,-2.4,25,MUTED,w=12))
  elif self.index==5:
   if t<177:g.add(tx('등고선은 모양을, 시간 법칙은 방향과 속도를',0,2.85,29),tx('에너지가 같다는 조건만으로는 충분하지 않다',0,-2.45,26,GOLD))
   else:
    g.add(tx('H의 두 변화율 → 상태의 시간 변화',0,2.85,29),eq(r'\dot\theta=\frac{\partial H}{\partial p_\theta}',-3.3,1.85,40,c=BLUE,w=5),eq(r'\dot p_\theta=-\frac{\partial H}{\partial\theta}',3.3,1.85,40,c=GREEN,w=5))
    if t<190:g.add(tx('운동량 방향 변화율 → 각도의 변화',0,-2.45,27,BLUE))
    elif t<201:g.add(tx('각도 방향 변화율 → 부호를 바꾼 운동량의 변화',0,-2.45,26,GREEN))
    else:g.add(tx('곡면의 내리막이 아니라, 등고선을 따르는 흐름',0,-2.45,25,GOLD))
  elif self.index==6:
   g.add(tx('NEWTON',-3.4,2.8,27,BLUE,w=5),tx('HAMILTON',3.4,2.8,27,GREEN,w=5),eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',-3.4,1.75,41,c=BLUE,w=5),eq(r'\dot\theta=\frac{p_\theta}{I},\quad\dot p_\theta=-mg\ell\sin\theta',3.4,1.75,34,c=GREEN,w=6),tx('같은 초기조건, 같은 운동',0,-2.4,28,GOLD))
  elif self.index==7:
   r=self.energy_ratio(t);name='왕복 운동' if r<1 else '임계 궤적 · 최고점에 점근적 접근' if r==1 else '한 방향으로 회전'
   g.add(tx('하나의 에너지 함수, 달라지는 운동의 종류',0,2.9,29),tx('강체 막대 진자',-4.8,2.15,21,MUTED,w=3.6),tx(name,2,2.2,26,GOLD,w=8),tx('−π',-1.8,-1.95,23,MUTED,w=1),tx('π',5.8,-1.95,23,MUTED,w=1),tx('−π와 π는 같은 각도 · 좌우 경계 연결',1.9,-2.45,23,MUTED,w=10))
   if t>=277:g.add(tx('분리곡선',-4.8,-1.95,25,GREEN,w=3.8))
  elif self.index==8:
   if t<329:
    g.add(tx('NEWTON',-4.5,2.8,24,BLUE,w=3.5),tx('LAGRANGE',0,2.8,24,GOLD,w=3.5),tx('HAMILTON',4.5,2.8,24,GREEN,w=3.5),tx('힘과 운동 변화',-4.5,-1.8,23,BLUE,w=3.8),tx('작용의 정지 조건',0,-1.8,23,GOLD,w=3.8),tx('상태의 시간 진화',4.5,-1.8,23,GREEN,w=3.8),tx('하나의 운동 · 서로 다른 수학적 표현',0,-2.5,28))
    if t>=307:g.add(eq(r'\delta S=0',0,1.9,32,c=GOLD,w=3.5))
    if t>=312:g.add(eq(r'X_H',4.5,1.9,32,c=GREEN,w=3))
   else:g.add(tx('위상 공간 전체의 흐름',0,2.85,31,GREEN),tx('H: 시간에 따른 상태 변화를 생성하는 함수',0,-2.45,28,GOLD))
  else:
   g.add(tx('상태는 변한다. 그 속에 유지되는 구조는?',0,2.85,30),tx('같은 초기 영역을 해밀턴 방정식으로 이동',0,-2.45,24,MUTED,w=12))
   if t>=354:g.add(tx('금색: 처음',-3,1.8,23,GOLD,w=4),tx('초록: 시간이 흐른 뒤',3,1.8,23,GREEN,w=5))
  if self.index==5 and t>=206:g.add(self.direction_field(axes(0,-.2,10.8,3.3,[-1.2,1.2,.4],[-9,9,3])))
  if (self.index==8 and t>=329) or self.index==9:g.add(self.direction_field(self.full))
  if self.index==3:
   if t<92:g.add(self.surface_zero.copy().set_z_index(-2))
   elif t>=100:g.add(self.surface_full.copy().set_z_index(-2))

  return g
 def geometry(self,t):
  if self.index==1:
   if t>=34:return VGroup()
   ax=self.phase.copy();q,p=self.ordinary(1);g=self.portrait_view(ax,q,p)
   if t>=15:
    g.scale(.65).shift(LEFT*4.2)
    g.add(arr([-.8,.2,0],[1.2,0,0],GREEN))
   return g
  if self.index==2:
   q,p=self.ordinary(t-37);T=p*p/(2*I);pot=A*(1-np.cos(q));E=H(.65,0);g=self.pend(q,p,x=-3.5,y=2.1,L=3.3)
   for y,v,c in [(.0,T/E,BLUE),(-.7,pot/E,GOLD)]:
    g.add(Line([.5,y,0],[6,y,0],color=MUTED,stroke_opacity=.25))
    if v>.001:g.add(Line([.5,y,0],[.5+5.5*v,y,0],color=c,stroke_width=12))
   return g
  if self.index==3:
   rise=np.clip((t-92)/8,0,1);g=self.surface(rise) if 92<=t<100 else VGroup()
   q=1.1*np.sin((t-73)*.18);p=11*np.cos((t-73)*.2);b=self.project(q,p,0);top=self.project(q,p,float(H(q,p))*(np.clip((t-84)/8,0,1)))
   g.add(DashedLine(b,top if np.linalg.norm(top-b)>.01 else b+[0,.01,0],color=GOLD),Dot(b,radius=.06,color=BLUE),Dot(top,radius=.08,color=GOLD));return g
  if self.index==4:
   if t<126:
    alpha=np.clip((t-117)/9,0,1);g=self.surface_full.copy();
    for cell,original,flat_cell in zip(g,self.surface_full,self.surface_flat):cell.set_points((1-alpha)*original.points+alpha*flat_cell.points).set_fill(opacity=.24*(1-alpha)).set_stroke(opacity=.38*(1-alpha))
    q,p=contour(RB)[0];flat=axes(0,.15,10.8,4.2,[-2,2,1],[-16,16,8]);pts=[(1-alpha)*self.project(a,b,EC*RB)+alpha*flat.c2p(a,b) for a,b in zip(q,p)];g.add(VMobject(stroke_color=GOLD,stroke_width=4,fill_opacity=0).set_points_as_corners(pts));return g
   q,p=self.ordinary((t-136)*.65 if t>=136 else 0);ax=self.phase.copy();return VGroup(self.pend(q,p),self.portrait_view(ax,q,p,levels=(.05,RB,.2,.35)))
  if self.index==5:
   ax=self.full.copy();q,p=self.ordinary((t-213)*.8 if t>=213 else 1)
   if t<177:return self.portrait_view(ax,q,p)
   ax=axes(0,-.2,10.8,3.3,[-1.2,1.2,.4],[-9,9,3]);g=self.portrait_view(ax,q,p,arrows=False)
   b=ax.c2p(q,p);d=field(np.array([q,p]));tip=ax.c2p(q+.2*d[0],p+.2*d[1]);g.add(arr(b,tip-b,GOLD))
   if 182<=t<190:g.add(arr(b,[0,.65*np.sign(p),0],BLUE),arr(b,ax.c2p(q+.2*d[0],p)-b,BLUE))
   elif 190<=t<206:g.add(arr(b,[.65*np.sign(np.sin(q)),0,0],GREEN),arr(b,ax.c2p(q,p+.2*d[1])-b,GREEN))
   return g
  if self.index==6:
   q,p=self.ordinary(t-219);return VGroup(self.pend(q,p,-3.4,.8,2.1),self.pend(q,p,3.4,.8,2.1))
  if self.index==7:
   r=self.energy_ratio(t);q,p=state(r,min((t-234)*.45,11.9));wrapped=(q+np.pi)%(2*np.pi)-np.pi;ax=self.portrait.copy();g=VGroup(ax)
   for e in [.25,.6,1,1.3]:g.add(self.level(ax,e,GREEN if e==1 else BLUE,2,.55 if e==1 else .18))
   g.add(self.energy_labels[round(r*100)].copy(),self.level(ax,r,GOLD,4,.95),Dot(ax.c2p(wrapped,p),color=GOLD,radius=.08),self.pend(q,p,-4.8,.1,1.5))
   g.add(Line([-1.7,-2.12,0],[5.7,-2.12,0],color=MUTED,stroke_opacity=.3),Dot([-1.7+(r-.1)/1.3*7.4,-2.12,0],radius=.075,color=GOLD))
   return g
  if self.index==8:
   q,p=self.ordinary((t-297)*.65)
   if t>=329:
    ax=self.full.copy();g=self.portrait_view(ax,q,p,arrows=False)
    if t>=337:
     for offset in [0,.5,1,1.5,2]:
      a,b=self.ordinary((t-337)*.65+offset);g.add(Dot(ax.c2p(a,b),radius=.06,color=GREEN))
    return g
   g=VGroup(self.pend(q,p,-4.5,1.65,2.0,forces=True))
   if t>=307:
    a=self.hist.copy();tt=np.linspace(0,3,81);qs=np.interp(tt,MODEL.times,MODEL.states[:,0]);g.add(a,curve(a,tt,qs,GOLD))
    for e in [-.13,.13]:g.add(curve(a,tt,qs+e*np.sin(np.pi*tt/3),BLUE,1.2,.4))
   if t>=312:g.add(self.portrait_view(self.mini.copy(),q,p,arrows=False))
   return g
  ax=self.full.copy();q,p=self.ordinary((t-342)*.5);g=self.portrait_view(ax,q,p,arrows=False)
  u=np.clip((t-346)/4,0,4);points=patch(float(u));coords=[ax.c2p(a,b) for a,b in points];g.add(Polygon(*coords,stroke_color=GREEN,stroke_width=3,fill_color=GREEN,fill_opacity=.25))
  if t>=354:g.add(Polygon(*[ax.c2p(a,b) for a,b in PATCH0],stroke_color=GOLD,stroke_width=2,fill_opacity=0))
  return g
