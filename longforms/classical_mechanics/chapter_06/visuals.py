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
from mechanics import MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi,rho,SAMPLES,HITS,JITTER,OP_A,OP_B,INPUT
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
  self.add(tx('EPILOGUE  /  QUANTUM',-4.9,3.6,18,MUTED,w=4.2),tx('고전역학을 넘어 이어지는 수학',3.4,3.6,22,w=6),Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  self.prepare()
  self.dynamic.add_updater(lambda m:self.replace_live(m,self.geometry(self.clock.get_value())))
  extra=[84,89,104,112,136,149,153,196,202,207,233,245,254,259]
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
 def replace_live(self,m,target):
  m.submobjects=target.submobjects
  return m
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def prepare(self):
  self.cache={}
  self.phase=axes(-3.5,.2,4.7,2.65,[-.8,.8,.4],[-7,7,2])
 def ordinary(self,t):
  q,w=MODEL.state_at(max(t,0));return float(q),float(I*w)
 def text(self,s,x=0,y=2.8,c=INK,size=28,w=12):return tx(s,x,y,size,c,w=w)
 def pend(self,t,x=0,y=2,L=3.5,forces=0):
  q,p=self.ordinary(t);return rig(0,pivot=(x,y,0),L=L,theta=q,omega=p/I,forces=forces)
 def level(self,ax):
  key=(tuple(ax.get_center()),ax.width,ax.height)
  if key not in self.cache:self.cache[key]=VGroup(*[curve(ax,q,p,BLUE,2,.6) for q,p in contour(RB)])
  return self.cache[key].copy()
 def portrait(self,t,ax=None):
  ax=self.phase.copy() if ax is None else ax;q,p=self.ordinary(t)
  return VGroup(ax,self.level(ax),Dot(ax.c2p(q,p),color=GOLD,radius=.07))
 def graph(self,x,y,w,h,mode='rho',t=0):
  ax=axes(x,y,w,h,[-5,5,2],[-.85,.85,.4] if mode!='rho' else [0,.7,.2]);g=VGroup(ax)
  z=psi(X,t)
  if mode=='rho':g.add(curve(ax,X,abs(z)**2,GREEN,3.5))
  else:g.add(curve(ax,X,z.real,BLUE,3),curve(ax,X,z.imag,GOLD,2.5))
  return g,ax
 def action(self,x=0,y=0,w=3,h=2):
  ax=axes(x,y,w,h,[0,1,.5],[-1.1,1.1,.5]);g=VGroup(ax);u=np.linspace(0,1,101);z=.7*np.cos(2*np.pi*u)
  for a,c in [(-.28,BLUE),(0,GOLD),(.28,BLUE)]:g.add(curve(ax,u,z+a*np.sin(np.pi*u),c,3 if a==0 else 1.5,.9 if a==0 else .3))
  return g
 def labels(self,t):
  T=self.text;g=VGroup();i=self.index
  if i==1:
   g.add(T('하나의 진자, 확장되어 온 수학적 표현'))
   if t<6:g.add(T('동일한 운동을 바라보는 여러 관점',y=-2.3,c=GOLD))
   elif t<11:g.add(T('NEWTON',3.2,2,c=BLUE,w=6),eq(r'F=ma',3.2,.8,57,c=BLUE,w=5),T('힘과 운동의 변화',3.2,-1.5,c=MUTED,w=6))
   elif t<16:g.add(T('LAGRANGE',3.2,2,c=GOLD,w=6),eq(r'\delta S=0',3.2,-1.65,43,c=GOLD,w=5))
   elif t<25:g.add(T('HAMILTON',3.2,2,c=GREEN,w=6),eq(r'H(q,p)',3.2,-1.65,40,c=GREEN,w=5))
   else:g.add(T('심플렉틱 구조',3.3,2,c=BLUE,w=6),T('대칭성 ↔ 보존량',3.3,-1.7,c=GREEN,w=6))
  elif i==2:
   g.add(T('새로운 현상은 새로운 상태 기술을 요구했다'),T('전자',-5.4,.1,c=BLUE,size=25,w=2),T('이중 슬릿',-2,2.05,c=MUTED,size=23,w=3),T('반복 측정으로 쌓이는 검출 분포',3.5,2.05,c=GOLD,size=24,w=6),T('경로를 관측하지 않은 전자 이중 슬릿 · 개념도',y=-2.4,c=MUTED,size=22))
   if t>=47:g.add(T('QUANTUM MECHANICS',0,-1.85,c=GREEN,size=30))
  elif i==3:
   g.add(T('상태 자체와, 그 상태에서 얻는 측정 확률'),T('고전 상태',-3.5,2.05,c=BLUE,w=5),eq(r'(q,p)',-3.5,-1.65,43,c=BLUE,w=5))
   if t<79:g.add(eq(r'|\psi\rangle',3.4,.5,72,c=GREEN,w=5),T('양자 상태',3.4,1.9,c=GREEN,w=5),T('일반적으로 하나의 (q,p) 점으로 표현하지 않는다',y=-2.45,c=GOLD,size=25))
   else:
    g.add(eq(r'\psi(x)=\langle x|\psi\rangle',3.4,2.05,32,c=GREEN,w=6),T('실수부',1.8,.45,c=BLUE,size=19,w=2),T('허수부',4.9,.45,c=GOLD,size=19,w=2))
    if t>=84:g.add(eq(r'|\psi(x)|^2',3.4,-1.9,32,c=GREEN,w=5),T('위치 측정의 확률밀도 · 상태 정보의 일부',y=-2.5,c=MUTED,size=23))
    else:g.add(T('복소 진폭: 크기와 상대적 위상 정보',y=-2.35,c=MUTED,size=24))
  elif i==4:
   g.add(T('운동 궤적의 예측과, 측정 확률의 예측'),T('고전: 초기조건 → 운동 궤적',-3.4,2.05,c=BLUE,size=25,w=6),T('양자: 같은 상태 준비 → 위치 측정',3.4,2.05,c=GREEN,size=25,w=6),T('독립적으로 같은 상태를 준비한 반복 실험',3.4,-1.55,c=MUTED,size=20,w=6),T('개별 결과는 확률적으로 · 상태의 시간 진화는 결정적으로',y=-2.4,c=GOLD,size=25))
  elif i==5:
   g.add(T('서로 다른 상태, 이어지는 시간 진화의 역할'),T('고전 · 해밀토니안 함수',-3.5,2.1,c=BLUE,size=26,w=6),T('양자 · 해밀토니안 연산자',3.5,2.1,c=GREEN,size=26,w=6))
   if t<153:
    g.add(eq(r'H(q,p)',-3.5,-1.85,43,c=BLUE,w=5))
    if t>=143:g.add(eq(r'i\hbar\frac{\mathrm d}{\mathrm dt}|\psi\rangle=\hat H|\psi\rangle',0,-2.2,34,c=GOLD,w=12))
    else:g.add(T('H가 상태의 시간 변화를 결정한다',y=-2.45,c=GOLD,size=27))
   else:g.add(eq(r'\dot q=H_p,\quad\dot p=-H_q',-3.5,-1.8,34,c=BLUE,w=6),eq(r'i\hbar\partial_t\psi=\hat H\psi',3.5,-1.8,38,c=GREEN,w=6),T('표현과 물리적 의미는 달라도, 시간 진화를 기술한다',y=-2.45,c=GOLD,size=25))
   g.add(T('실수부',1.7,1.55,c=BLUE,size=18,w=2),T('허수부',4.9,1.55,c=GOLD,size=18,w=2),T('확률밀도 |ψ|²',3.5,-1.13,c=GREEN,size=20,w=5),T('조화 진동자 · 무차원 단위 · 0·1 상태 중첩',3.5,-1.4,c=MUTED,size=16,w=6))
  elif i==6:
   if t<196:
    g.add(T('대칭성과 보존을 잇는 수학적 관계'),T('고전 · 함수',-3.35,1.85,c=BLUE,w=6),T('양자 · 연산자',3.35,1.85,c=GREEN,w=6),eq(r'\{F,H\}',-3.35,.55,60,c=BLUE,w=5),eq(r'[\hat A,\hat B]',3.35,.55,60,c=GREEN,w=5),T('함수의 변화율을 결합',-3.35,-.8,c=MUTED,size=25,w=6),T('적용 순서의 차이',3.35,-.8,c=MUTED,size=25,w=6),T('다른 정의를 가진 연산, 이어지는 물리적 역할',y=-2.3,c=GOLD,size=26))
   elif t<207:
    g.add(T('교환자: 연산의 순서가 달라지면'),eq(r'[\hat A,\hat B]=\hat A\hat B-\hat B\hat A',0,2,42,c=GREEN,w=12),T('먼저 B, 다음 A',-3.4,1.2,c=BLUE,size=25,w=6),T('먼저 A, 다음 B',3.4,1.2,c=GOLD,size=25,w=6),eq(r'\hat A\hat B|\psi\rangle',-3.4,-1.1,35,c=BLUE,w=6),eq(r'\hat B\hat A|\psi\rangle',3.4,-1.1,35,c=GOLD,w=6),T('두 성분의 크기 · 연산 결과는 정규화 전',y=-2.35,c=MUTED,size=23))
   else:
    g.add(T('교환자는 물리량의 시간 변화와 연결된다'),eq(r'\frac{\mathrm d\langle\hat A\rangle}{\mathrm dt}=\frac{1}{i\hbar}\langle[\hat A,\hat H]\rangle',0,1.25,48,c=GREEN,w=12),T('연산자 A에 명시적인 시간 의존성이 없을 때',y=.05,c=MUTED,size=24),eq(r'[\hat A,\hat H]=0\quad\Longrightarrow\quad\langle\hat A\rangle=\mathrm{constant}',0,-1,39,c=GOLD,w=12),T('푸아송 괄호와 교환자는 동일한 연산이 아니다',y=-2.3,c=BLUE,size=25))
  else:
   if t<233:
    g.add(T('뉴턴에서 해밀턴까지 · 같은 운동을 표현하는 언어'))
    for x,name,cap,c in [(-4.4,'NEWTON','힘과 운동의 변화',BLUE),(0,'LAGRANGE','작용의 정지 조건',GOLD),(4.4,'HAMILTON','위상 공간의 흐름',GREEN)]:g.add(T(name,x,2,c=c,size=23,w=3.8),T(cap,x,-1.8,c=c,size=23,w=3.9))
    g.add(T('동일한 운동, 새롭게 드러나는 구조',y=-2.45,c=GOLD,size=27))
   elif t<245:
    g.add(T('표현의 변화가 드러낸 새로운 관계'),eq(r'F=ma',-4.4,1.25,42,c=BLUE,w=3.7),eq(r'\delta S=0',0,1.25,42,c=GOLD,w=3.7),eq(r'H(q,p)',4.4,1.25,42,c=GREEN,w=3.7),T('운동의 예측',-4.4,.1,c=BLUE,size=24,w=3.7),T('공통 원리',0,.1,c=GOLD,size=24,w=3.7),T('상태와 시간 진화',4.4,.1,c=GREEN,size=24,w=3.7),T('기하학적 구조 · 대칭성 · 보존량',y=-1.3,c=GREEN,size=30),T('고전역학의 세 접근은 같은 운동을 기술한다',y=-2.45,c=MUTED,size=25))
   elif t<254:
    g.add(T('새로운 현상과 원리, 이어지는 수학적 사고'),eq(r'H(q,p)',-3.4,1.25,56,c=BLUE,w=5),eq(r'\hat H',3.4,1.25,62,c=GREEN,w=5),T('고전 상태의 시간 진화',-3.4,-.1,c=BLUE,size=27,w=6),T('양자 상태의 시간 진화',3.4,-.1,c=GREEN,size=27,w=6),T('양자역학: 새로운 상태와 측정의 원리',y=-1.3,c=GOLD,size=28),T('같은 이론의 기호 교체를 넘어선 변화',y=-2.4,c=MUTED,size=25))
   elif t>=259:g.add(T('같은 세계를 바라보는, 서로 다른 수학적 언어',y=2.8,c=GOLD,size=30))
  return g
 def geometry(self,t):
  g=VGroup();i=self.index
  if i==1:
   g.add(self.pend(t*.5,x=-3.7,y=2.05,L=3.4,forces=1 if 6<=t<11 else 0))
   if 11<=t<16:g.add(self.action(3.2,.2,4.5,2))
   elif t>=16:
    ax=axes(3.2,.2,4.6,2.7,[-.8,.8,.4],[-7,7,2]);g.add(self.portrait(t*.5,ax))
    if t>=25:
     b,_=packet(min((t-25)*.45,3.5));g.add(Polygon(*[ax.c2p(q,p) for q,p in b],color=GREEN,fill_color=GREEN,fill_opacity=.25,stroke_width=2))
  elif i==2:
   g.add(RoundedRectangle(width=1.35,height=1.3,corner_radius=.12,color=BLUE,fill_color=BLUE,fill_opacity=.07).move_to([-5.4,.1,0]),Arrow([-4.55,.1,0],[-2.45,.1,0],color=MUTED))
   for a,b in [(-1.5,-.58),(-.32,.32),(.58,1.5)]:g.add(Line([-2,a,0],[-2,b,0],stroke_width=11,color=MUTED))
   g.add(Line([3.5,-1.5,0],[3.5,1.5,0],color=MUTED))
   n=min(200,int(max(t-35,0)*8))
   for y,j in zip(HITS[:n],JITTER[:n]):g.add(Dot([3.5+j,y*.29,0],radius=.025,color=GOLD))
   # Density is an accumulated detection distribution, never a tracked post-slit path.
   yy=np.linspace(-5,5,161);density=np.exp(-yy*yy/5)*np.cos(3*yy)**2
   g.add(VMobject(stroke_color=GREEN,stroke_width=2,fill_opacity=0).set_points_as_corners([[4.3+v*.9,y*.29,0] for y,v in zip(yy,density)]))
  elif i==3:
   g.add(self.portrait(0))
   if t>=79:
    v,_=self.graph(3.4,1.15,5.5,1.3,'psi',0);g.add(v)
    if t>=84:
     v,ax=self.graph(3.4,-.85,5.5,1.3,'rho',0);g.add(v)
     if t>=89:g.add(*[Dot(ax.c2p(float(x),0),color=GOLD,radius=.025) for x in SAMPLES[:int((t-89)*10)]])
  elif i==4:
   ax=axes(-3.4,.2,5.4,2.9,[-.8,.8,.4],[-7,7,2]);g.add(self.portrait((t-96)*.6,ax))
   v,ax=self.graph(3.4,.4,5.4,2.8,'rho',0);g.add(v)
   n=0 if t<104 else 1 if t<108 else min(150,int((t-108)*14)+1)
   for j,x in enumerate(SAMPLES[:n]):g.add(Dot(ax.c2p(float(x),-.005-.006*(j%4)),color=GOLD,radius=.026))
  elif i==5:
   g.add(self.portrait((t-121)*.5))
   u=(t-121)*.35
   v,_=self.graph(3.5,.85,5.4,1.0,'psi',u);g.add(v)
   v,_=self.graph(3.5,-.4,5.4,1.0,'rho',u);g.add(v)
  elif i==6 and 196<=t<207:
   for x,c,values in [(-3.4,BLUE,OP_A@OP_B@INPUT),(3.4,GOLD,OP_B@OP_A@INPUT)]:
    for j,val in enumerate(values):
     xx=x+(j-.5)*1.1;g.add(Rectangle(width=.65,height=val*.95,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([xx,-.7+val*.95/2,0]))
    g.add(Line([x-1.6,-.7,0],[x+1.6,-.7,0],color=MUTED))
  elif i==7:
   if t<233:
    g.add(self.pend((t-217)*.5,x=-4.4,y=1.45,L=2.5,forces=1),self.action(0,.05,3.2,2.2),self.portrait((t-217)*.5,axes(4.4,.05,3.2,2.4,[-.8,.8,.4],[-7,7,2])))
   elif 233<=t<245:
    g.add(Arrow([-3,.9,0],[-1.4,.9,0],color=MUTED),Arrow([1.4,.9,0],[3,.9,0],color=MUTED))
   elif t>=254:g.add(self.pend((t-254)*.6,x=0,y=2.1,L=4.1))
  return g
