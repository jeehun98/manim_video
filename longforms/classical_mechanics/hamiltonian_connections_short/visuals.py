"""9:16 layout sharing the longform pendulum and quantum animation models."""
from pathlib import Path
import sys,importlib.util,json,textwrap
import numpy as np
from manim import *
R=Path(__file__).resolve().parent;P=R.parent/'chapter_01';sys.path.append(str(P))
spec=importlib.util.spec_from_file_location('common_pendulum_visuals',P/'visuals.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
BG,INK,MUTED,BLUE,GOLD,GREEN,RED=base.BG,base.INK,base.MUTED,base.BLUE,base.GOLD,base.GREEN,base.RED
rig,arr=base.rig,base.arr
from mechanics import MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi,rho,HISTORY_T,HISTORY_Q,HISTORY_W,ENERGIES,probabilities,orbit
config.frame_width=9;config.frame_height=16;config.background_color=BG
RB=float(H(.65,0)/EC)
def tx(s,x=0,y=0,size=30,c=INK,w=7.8):return base.tx(s,x,y,size,c,w=w)
def eq(s,x=0,y=0,size=45,c=INK,w=7.8):return base.eq(s,x,y,size,c,w=w)
def axes(x,y,w,h,xrange,yrange):
 a=Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(include_ticks=False,stroke_color=MUTED,stroke_width=1.5));a.move_to([x,y,0]);return a
def curve(ax,x,y,c=GOLD,width=3,op=1):return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=op,fill_opacity=0).set_points_as_corners([ax.c2p(float(a),float(b)) for a,b in zip(x,y)])
class ConnectionScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def replace_live(self,m,new):m.submobjects=new.submobjects;return m
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('물리학의 수학적 언어',0,7.25,28,w=8),Line([-3.9,6.75,0],[3.9,6.75,0],stroke_color=MUTED,stroke_opacity=.3))
  self.add(RoundedRectangle(width=8.3,height=1.85,corner_radius=.13,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-6.85,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None;self.prepare()
  self.dynamic.add_updater(lambda m:self.replace_live(m,self.geometry(self.clock.get_value())))
  extra=[1.4,2.8,4.2,6,12,15,22,26,33,35,40,45,51,56,60,66,70,77,81,87,91,94,101,108,112,118,122,126,137,141,148,152,160]
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[x for x in extra if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=(round(b*config.frame_rate)-round(a*config.frame_rate))/config.frame_rate,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,indent=2),encoding='utf-8')
 def update_text(self,t):
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  if line!=self.current:
   self.remove(self.caption);self.current=line
   self.caption=VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=line['start'],end=line['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1])))
  self.remove(self.static);self.static=self.labels(t);self.add(self.static)
  for m in self.static:assert m.get_left()[0]>-4.2 and m.get_right()[0]<4.2 and m.get_bottom()[1]>-5.65 and m.get_top()[1]<6.4,('label',self.index,t,m.get_center())
 def prepare(self):self.cache={};self.rng=np.random.default_rng(169);self.gas_positions=self.rng.uniform(-1,1,(28,2));self.gas_velocities=self.rng.uniform(-.5,.5,(28,2))
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


 def cached_eq(self,s,x=0,y=0,size=42,c=INK,w=7.7):
  key=('formula',s,x,y,size,c,w)
  if key not in self.cache:self.cache[key]=eq(s,x,y,size,c,w)
  return self.cache[key].copy()
 def wall(self,t,dim=1,ordered=False):
  formulas=[r'R_{mu\nu}-\frac12Rg_{mu\nu}+\Lambda g_{mu\nu}=\frac{8\pi G}{c^4}T_{mu\nu}',r'(i\gamma^\mu\partial_\mu-m)\psi=0',r'(D_\mu F^{\mu\nu})^a=J^{a\nu}',r'Z[J]=\int\mathcal D\phi\; e^{\frac{i}{\hbar}(S[\phi]+\int d^4x\,J\phi)}']
  names=['아인슈타인 장방정식','디랙 방정식 · 자연단위계','양–밀스 방정식','양자장론 · 생성 범함수']
  g=VGroup()
  for i,(f,name) in enumerate(zip(formulas,names)):
   if not ordered and t<i*1.4:continue
   y=4.25-2.05*i;u=1 if ordered else float(np.clip((t-i*1.4)/.8,0,1))
   fobj=self.cached_eq(f,0,y,36,BLUE if i%2==0 else GOLD,7.6).shift([(-1 if i%2==0 else 1)*(1-u)*.3,0,0]).set_opacity(dim*u)
   nameobj=tx(name,0,y+.65,21,c=MUTED,w=7.6).set_opacity(dim*u)
   g.add(fobj,nameobj)
  if not ordered and t>=6:
   extras=[r'\nabla_\mu T^{\mu\nu}=0',r'\partial_\mu F^{\mu\nu}=J^\nu',r'\delta S=0',r'\langle\phi(x)\phi(y)\rangle',r'[\hat x,\hat p]=i\hbar',r'Z=\operatorname{Tr} e^{-\beta\hat H}']
   for j,f in enumerate(extras):
    x=(-1 if j%2==0 else 1)*1.8;y=5.05-j*1.65;g.add(self.cached_eq(f,x,y,30,MUTED,3.6).set_opacity(dim*.2))
  return g
 def wave(self,t,y=-1.7,h=2.2):
  ax=axes(0,y,6.7,h,[-5,5,2],[-.85,.85,.4]);z=psi(X,t)
  return VGroup(ax,curve(ax,X,z.real,BLUE,3),curve(ax,X,z.imag,GOLD,3))
 def probability_graph(self,y=-1.8,h=2.8,w=6.6,labels=False):
  ax=axes(0,y,w,h,[-.7,3.7,1],[0,.8,.2]);g=VGroup(ax)
  for i,p in enumerate(probabilities()):
   left=ax.c2p(i-.27,0);right=ax.c2p(i+.27,p)
   g.add(Rectangle(width=right[0]-left[0],height=right[1]-left[1],stroke_width=0,fill_color=[GREEN,BLUE,GOLD,RED][i],fill_opacity=.9).move_to((left+right)/2))
   if labels:g.add(tx(f'{p*100:.1f}%',ax.c2p(i,p)[0],ax.c2p(i,p)[1]+.25,21,w=1.5),tx(f'E={i}',ax.c2p(i,0)[0],ax.c2p(i,0)[1]-.35,20,c=MUTED,w=1.5))
  return g
 def roles(self,t):
  g=VGroup()
  for y,name,f,role,c in [(4.4,'고전역학',r'H(q,p)','운동 상태의 시간 변화',BLUE),(1.15,'양자역학',r'\hat H','양자 상태의 시간 변화',GOLD),(-2.1,'통계물리학',r'P(s)=e^{-\beta H(s)}/Z','열평형 상태의 확률분포',GREEN)]:
   g.add(RoundedRectangle(width=7.4,height=2.65,corner_radius=.16,stroke_color=c,stroke_opacity=.35,fill_color=c,fill_opacity=.035).move_to([0,y-.5,0]),tx(name,0,y+.35,28,c=c),self.cached_eq(f,0,y-.45,42,c,6.5),tx(role,0,y-1.2,25,c=c))
  return g
 def labels(self,t):
  i=self.index;g=VGroup()
  if i==1:
   if 12<=t<15:g.add(RoundedRectangle(width=7.8,height=2.25,corner_radius=.15,stroke_width=0,fill_color=BG,fill_opacity=.95).move_to([0,.25,0]),tx('이 수식들을',0,.7,36),tx('어떻게 이해할 수 있을까?',0,-.15,34,c=GOLD))
   elif t>=15:g.add(tx('서로 다른 수식 속의 공통 구조',0,-4.9,28,c=GOLD))
  elif i==2:
   g.add(tx('반복해서 등장하는 수학적 대상',0,5.8,28,c=GOLD),tx('HAMILTONIAN',0,3.8,33,c=GREEN),tx('해밀토니안',0,2.8,35))
   if t<26:g.add(self.cached_eq(r'H',0,.45,115,GREEN))
   else:g.add(self.cached_eq(r'H(q,p)',0,.65,67,BLUE),tx('함수',0,-.5,26,c=BLUE),self.cached_eq(r'\hat H',0,-2.2,75,GOLD),tx('연산자',0,-3.5,26,c=GOLD))
  elif i==3:
   g.add(tx('고전역학 · 현재 상태에서 시간 변화로',0,5.95,29,c=GOLD))
   if t>=35:g.add(tx('이상적인 진자 · 마찰 없음',0,5.12,21,c=MUTED))
   if t>=40 and not 51<=t<56:g.add(self.cached_eq(r'(\theta,p_\theta)',0,.6,40,GREEN))
   if 45<=t<51:g.add(self.cached_eq(r'H(\theta,p_\theta)',0,-4.75,45,GREEN))
   elif 51<=t<56:g.add(self.cached_eq(r'H=T+V',0,-4.6,48,GREEN),tx('전체 에너지는 일정',0,-5.35,24,c=MUTED),tx('T',-1.8,.75,24,c=BLUE,w=2),tx('V',1.8,.75,24,c=GOLD,w=2))
   elif t>=56:g.add(self.cached_eq(r'\dot\theta=\frac{\partial H}{\partial p_\theta},\quad\dot p_\theta=-\frac{\partial H}{\partial\theta}',0,-4.6,37,BLUE),tx('해밀턴 방정식 · 방향과 속도',0,-5.4,23,c=GOLD))
   if t>=60:g.add(self.field_arrows(axes(0,-2,6.5,3.7,[-.8,.8,.4],[-7,7,2])))
  elif i==4:
   g.add(tx('다른 물리계, 공통된 운동의 형식',0,5.95,30,c=GOLD),tx('진자',0,5,25,c=BLUE),tx('행성의 공전',0,-.15,25,c=GOLD),self.cached_eq(r'H_{\rm pend}=\frac{p_\theta^2}{2I}+mg\ell(1-\cos\theta)',0,1.05,31,BLUE),self.cached_eq(r'H_{\rm orbit}=\frac{\mathbf p^2}{2m}-\frac{GMm}{r}',0,-4,32,GOLD),self.cached_eq(r'\dot q_i=H_{p_i},\quad\dot p_i=-H_{q_i}',0,-5,35,GREEN))
  elif i==5:
   g.add(tx('양자역학 · 상태 표현이 달라진다',0,5.95,30,c=GOLD),tx('고전 상태',0,5,25,c=BLUE),self.cached_eq(r'(q,p)',0,1.25,37,BLUE))
   if t>=81:g.add(self.cached_eq(r'|\psi\rangle',-2.8,.2,40,GREEN,2),tx('양자 상태',1,.2,26,c=GREEN,w=4.8))
   if t>=87:g.add(tx('실수부',-1.7,-3,20,c=BLUE,w=3),tx('허수부',1.7,-3,20,c=GOLD,w=3),tx('파동함수 ψ(x) · 복소 진폭',0,-3.65,23,c=MUTED))
   if 91<=t<94:g.add(self.cached_eq(r'H(q,p)\qquad\hat H',0,-4.8,44,GREEN))
   elif t>=94:g.add(self.cached_eq(r'i\hbar\frac{\mathrm d}{\mathrm dt}|\psi\rangle=\hat H|\psi\rangle',0,-4.75,38,GREEN))
   if t>=101:g.add(tx('이어지는 역할: 상태의 시간 진화',0,-5.4,23,c=GOLD))
  elif i==6:
   g.add(tx('통계물리학 · 에너지에서 평형 확률로',0,5.95,29,c=GOLD))
   if t<112:g.add(tx('많은 입자, 수많은 가능한 상태',0,-3.4,28,c=BLUE),tx('미시 상태를 나타낸 개념도',0,-4.6,22,c=MUTED))
   elif t<118:g.add(tx('가능한 미시 상태의 예',0,4.9,26,c=BLUE),tx('각 상태에 서로 다른 에너지를 대응',0,-4.7,25,c=MUTED))
   else:g.add(tx('서로 다른 네 미시 상태의 예',0,4.75,25,c=BLUE),tx('에너지 E = 0, 1, 2, 3',0,3.65,28,c=GOLD),self.cached_eq(r'P(s)=\frac{e^{-\beta H(s)}}{Z}',0,1.8,49,GREEN),tx('정준 앙상블 · kBT = 1',0,.5,24,c=MUTED),tx('같은 온도에서 상태별 확률 비교',0,-4.65,24,c=GREEN),tx('Z는 전체 확률을 1로 정규화',0,-5.35,21,c=MUTED))
  elif i==7:
   g.add(tx('서로 다른 이론에서 이어지는 역할',0,5.95,29,c=GOLD),self.roles(t))
   if t<137:g.add(tx('서로 다른 상태 · 서로 다른 수학적 대상',0,-5.35,23,c=MUTED))
   elif t<141:g.add(tx('하나로 모든 이론을 설명한다는 뜻은 아니다',0,-5.35,22,c=MUTED))
   else:g.add(tx('HAMILTONIAN',0,-5.3,29,c=GREEN))
  else:
   if t<152:g.add(tx('처음의 수식들을 다시 바라보면',0,5.95,30,c=GOLD))
   elif t<160:g.add(tx('어떤 상태를 표현하는가?',0,2,33,c=GREEN),tx('그 변화는 무엇이 결정하는가?',0,0,29,c=BLUE),tx('그 분포는 무엇이 결정하는가?',0,-2,29,c=GOLD))
   else:g.add(tx('복잡한 방정식을 이해하는 방법',0,2.35,31),tx('반복되는 구조와',0,.75,39,c=GREEN),tx('그 역할을 찾는 것',0,-.6,37,c=GREEN),tx('THE LANGUAGE OF PHYSICS',0,4.9,21,c=MUTED),tx('HAMILTONIAN',0,-4.75,27,c=GOLD))
  if i==1 and t>=6:g.add(self.wall(t,.14 if 12<=t<15 else 1).set_z_index(-1))
  elif i==2:g.add(self.wall(22,.08,True).set_z_index(-1))
  elif i==8:g.add(self.wall(t,.55 if t<152 else .12,True).set_z_index(-1))
  return g
 def geometry(self,t):
  g=VGroup();i=self.index
  if i==1:
   if t<6:g.add(self.wall(t,1))
   if t>=15:
    y=4.9-(t-15)/7*9.1;g.add(Line([-3.8,y,0],[3.8,y,0],color=GREEN,stroke_width=2,stroke_opacity=.7))
  elif i==2:pass
  elif i==3:
   u=(t-33)*.65;g.add(self.pend(u,y=4.6,L=3.25))
   if 51<=t<56:
    q,p=self.ordinary(u);E=float(H(.65,0))
    for xx,val,c in [(-1.8,p*p/(2*I),BLUE),(1.8,float(H(q,0)),GOLD)]:
     g.add(Line([xx-1.3,.2,0],[xx+1.3,.2,0],color=MUTED,stroke_width=10,stroke_opacity=.2))
     if val/E>.00001:g.add(Line([xx-1.3,.2,0],[xx-1.3+2.6*val/E,.2,0],color=c,stroke_width=10))
   if t>=40:
    v,ax=self.phase(u,y=-2,h=3.7,levels=t>=45);g.add(v)
    if 45<=t<51:
     q,p=self.ordinary(u);vv=field(np.array([q,p]));d=ax.c2p(q+.06*vv[0],p+.06*vv[1])-ax.c2p(q,p);g.add(arr(ax.c2p(q,p),d,BLUE))
  elif i==4:
   u=(t-66)*.7;g.add(self.pend(u,y=4.35,L=2.7));ts=np.linspace(0,2*np.pi,181);q,_=orbit(ts);center=np.array([.55,-1.95,0]);scale=1.4
   g.add(VMobject(stroke_color=GOLD,stroke_width=2,fill_opacity=0).set_points_as_corners([center+np.r_[v*scale,0] for v in q]),Dot(center,color=GOLD,radius=.13))
   pos,vel=orbit(u);g.add(Dot(center+np.r_[pos*scale,0],color=BLUE,radius=.09),arr(center+np.r_[pos*scale,0],np.r_[vel*.4,0],BLUE))
  elif i==5:
   v,_=self.phase((t-77)*.5,y=3.1,h=2.5,w=5.5);g.add(v)
   if t>=81:g.add(self.wave((t-77)*.35 if t>=94 else 0,y=-1.55,h=2.1))
  elif i==6:
   if t<112:
    g.add(RoundedRectangle(width=6.7,height=5,corner_radius=.15,color=MUTED).move_to([0,1,0]))
    xy=self.gas_positions+(t-108)*self.gas_velocities;xy=1-abs((xy+1)%4-2)
    g.add(*[Dot([p[0]*3.1,1+p[1]*2.25,0],color=BLUE if j%2 else GOLD,radius=.045) for j,p in enumerate(xy)])
   elif t<118:
    for j,(x,y) in enumerate([(-1.9,2.7),(1.9,2.7),(-1.9,-.5),(1.9,-.5)]):
     g.add(RoundedRectangle(width=3.2,height=2.7,corner_radius=.12,color=[GREEN,BLUE,GOLD,RED][j],stroke_opacity=.5).move_to([x,y,0]),tx(f's{j}',x,y+1,25,c=[GREEN,BLUE,GOLD,RED][j],w=2))
     for a in range(5):g.add(Dot([x+.9*np.sin(a*2.1+j),y+.55*np.cos(a*1.7+j),0],color=BLUE,radius=.055))
   else:g.add(self.probability_graph(y=-1.65,h=3,w=6.6,labels=True))
  elif i==8:pass
  return g
