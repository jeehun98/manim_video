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
from mechanics import MODEL,I,A,EC,H,field,contour,packet,INITIAL
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
  self.add(tx('CHAPTER 05  /  GEOMETRY',-4.9,3.6,18,MUTED,w=4.2),tx('변화 속에서도 보존되는 구조',3.4,3.6,22,w=6),Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50))
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None
  self.prepare()
  self.dynamic.add_updater(lambda m:self.replace_live(m,self.geometry(self.clock.get_value())))
  extra=[]
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
  self.full=axes(0,.1,10.4,4.1,[-1.05,1.05,.5],[-9,9,3])
  self.left=axes(-3.35,.15,5.4,3.7,[-.8,.8,.4],[-7,7,2])
  self.right=axes(3.35,.15,5.4,3.7,[-.8,.8,.4],[-7,7,2])
 def ordinary(self,t):
  q,w=MODEL.state_at(max(t,0));return float(q),float(I*w)
 def level(self,ax,r,c=BLUE,op=.3):
  key=(tuple(ax.get_center()),ax.width,ax.height,r,c,op)
  if key not in self.cache:self.cache[key]=VGroup(*[curve(ax,q,p,c,2,op) for q,p in contour(r)])
  return self.cache[key].copy()
 def pend(self,q,p,x=-3.8,y=2,L=3.2):return rig(0,pivot=(x,y,0),L=L,theta=q,omega=p/I)
 def region(self,ax,u,c=GREEN,dots=False):
  boundary,points=packet(u)
  g=VGroup(Polygon(*[ax.c2p(q,p) for q,p in boundary],color=c,stroke_width=2.5,fill_color=c,fill_opacity=.22))
  if dots:g.add(*[Dot(ax.c2p(q,p),radius=.035,color=c) for q,p in points])
  return g
 def text(self,s,x=0,y=2.8,c=INK,size=29,w=12):return tx(s,x,y,size,c,w=w)
 def labels(self,t):
  g=VGroup();T=self.text
  if self.index==1:
   g.add(T('한 점의 궤적에서, 여러 상태의 흐름으로'),T('각 점 = 서로 조금씩 다른 초기 상태',y=-2.4,c=GOLD,size=25),eq(r'\theta',5.6,.1,30,c=BLUE),eq(r'p_\theta',.3,2.3,30,c=BLUE))
  elif self.index==2:
   g.add(T('변형되는 영역 · 유지되는 넓이'),T('처음',-3.35,2.25,c=BLUE,size=26,w=5),T('시간이 흐른 뒤',3.35,2.25,c=GREEN,size=26,w=5),T('동일한 좌표 축척 · 실제 해밀턴 흐름',y=-2.4,c=MUTED,size=23),eq(r'A(t)/A(0)=1',0,-1.95,35,c=GOLD,w=7))
  elif self.index==3:
   g.add(T('두 변화율의 교차 결합'),eq(r'\dot q=\frac{\partial H}{\partial p}',-3.2,1.7,47,c=BLUE,w=5),eq(r'\dot p=-\frac{\partial H}{\partial q}',3.2,1.7,47,c=GREEN,w=5))
   if t>=71:g.add(T('q의 변화 ↔ p 방향 기울기',-3.2,.65,c=BLUE,size=23,w=5.7),T('p의 변화 ↔ −q 방향 기울기',3.2,.65,c=GREEN,size=23,w=5.7))
   if t>=76:g.add(T('심플렉틱 구조',0,-.25,c=GOLD,size=35),eq(r'\omega=\mathrm dq\wedge\mathrm dp',0,-1.15,39,c=GOLD,w=9))
   if t>=90:g.add(eq(r'\omega=\sum_i\mathrm dq_i\wedge\mathrm dp_i',0,-2.15,35,c=GREEN,w=10))
   elif t>=83:g.add(T('하나의 자유도: 위상 평면의 넓이 보존',y=-2.3,c=GREEN,size=26))
  elif self.index==4:
   g.add(T('영역의 넓이에서, 한 궤적의 보존량으로'),T('이상적인 진자 · 마찰 없음',-3.8,-1.8,c=MUTED,size=21,w=5),T('운동에너지 T',3,.8,c=BLUE,size=25,w=5),T('위치에너지 V',3,-.35,c=GOLD,size=25,w=5),eq(r'H=T+V=\mathrm{constant}',3,-1.6,37,c=GREEN,w=6),T('두 에너지는 바뀌지만, 합은 일정하다',y=-2.45,c=GREEN,size=26))
  elif self.index==5:
   g.add(T('시작 시각이 달라도, 운동 법칙은 동일'),T('실험 A',-5.6,1.6,c=GOLD,size=24,w=2),T('실험 B',-5.6,-.45,c=BLUE,size=24,w=2),T('시간 이동 대칭성',0,-1.65,c=GREEN,size=29))
   if t>=159:g.add(eq(r't\mapsto t+\tau\quad\Longrightarrow\quad E=\mathrm{constant}',0,-2.35,36,c=GOLD,w=11))
   else:g.add(T('같은 초기조건 · 서로 다른 시작 시각',y=-2.35,c=MUTED,size=24))
  elif self.index==6:
   g.add(T('서로 다른 보존법칙을 잇는 하나의 원리'))
   for x,name,law,c in [(-4.4,'시간 이동','에너지',GOLD),(0,'공간 이동','운동량',BLUE),(4.4,'회전','각운동량',GREEN)]:
    g.add(T(name,x,2.05,c=c,size=26,w=3.6),T(law,x,-.95,c=c,size=29,w=3.6))
   g.add(T('자유 입자',0,-1.55,c=MUTED,size=19,w=3.6),T('중심력 운동',4.4,-1.55,c=MUTED,size=19,w=3.6))
   if t>=188:g.add(T('뇌터 정리 · 작용의 연속 대칭 ↔ 보존량',y=-2.35,c=GOLD,size=29))
   else:g.add(T('각 물리계가 가진 연속 대칭에 대응',y=-2.35,c=MUTED,size=25))
  elif self.index==7:
   g.add(T('푸아송 괄호 · 변화와 보존을 계산하다'))
   if t<228:
    g.add(eq(r'F(q,p)',-3.2,1.85,45,c=GOLD,w=5),eq(r'H(q,p)',3.2,1.85,45,c=GREEN,w=5),eq(r'\frac{\mathrm d F}{\mathrm dt}=\{F,H\}+\frac{\partial F}{\partial t}',0,-1.95,40,c=GREEN,w=10),T('일반적으로는 명시적 시간 의존성도 포함',y=-2.55,c=MUTED,size=21))
   elif t<244:
    g.add(eq(r'F(q,p)',-3.1,1.8,46,c=GOLD,w=5),eq(r'H(q,p)',3.1,1.8,46,c=GREEN,w=5),eq(r'\{F,H\}=\frac{\partial F}{\partial q}\frac{\partial H}{\partial p}-\frac{\partial F}{\partial p}\frac{\partial H}{\partial q}',0,.25,48,c=BLUE,w=12),T('두 함수의 변화율을 교차하여 결합',y=-1.05,c=MUTED,size=25),eq(r'\dot F=\{F,H\}\quad(\partial_t F=0)',0,-2.05,38,c=GREEN,w=11))
   else:
    g.add(T('운동량 pθ',-3.3,1.9,c=GOLD,size=25,w=5),T('전체 에너지 H',3.3,1.9,c=GREEN,size=25,w=5),eq(r'\{p_\theta,H\}=-mg\ell\sin\theta',-3.3,-1.1,31,c=GOLD,w=6),eq(r'\{H,H\}=0',3.3,-1.1,40,c=GREEN,w=5),T('명시적 시간 의존성이 없을 때: {F,H} = 0 → 보존',y=-2.25,c=GREEN,size=26))
  elif self.index==8:
   g.add(T('동일한 운동에서, 더 깊은 구조로'))
   for x,name,f,c in [(-4.4,'NEWTON',r'F=ma',BLUE),(0,'LAGRANGE',r'\delta S=0',GOLD),(4.4,'HAMILTON',r'H(q,p)',GREEN)]:g.add(T(name,x,2,c=c,size=23,w=3.8),eq(f,x,1.1,43,c=c,w=3.8))
   if t>=275:g.add(T('심플렉틱 구조',-3.25,-.4,c=BLUE,size=31,w=5.8),T('時間 진화가 보존하는 기하학'.replace('時間','시간'),-3.25,-1.25,c=MUTED,size=23,w=6),T('대칭성과 보존량',3.25,-.4,c=GREEN,size=31,w=5.8),T('뇌터 정리 · 푸아송 괄호',3.25,-1.25,c=MUTED,size=23,w=6))
   g.add(T('상태는 변한다. 그 변화 속의 관계는 유지된다.',y=-2.35,c=GOLD,size=28))
  else:
   g.add(T('상태를 어떻게 표현하고, 시간 변화를 어떻게 기술할까?'),T('고전역학',-3.6,1.9,c=BLUE,size=28,w=5),T('새로운 상태 표현',3.6,1.9,c=GREEN,size=28,w=5),T('상태와 시간 진화라는 질문은 계속된다',y=-2.1,c=GOLD,size=28),T('오른쪽 곡선은 상태 표현의 개념도',3.5,-1.4,c=MUTED,size=18,w=6))
  return g
 def geometry(self,t):
  g=VGroup();i=self.index
  if i==1:
   ax=self.full.copy();g.add(ax)
   for r in [.08,.16,.25,.36]:g.add(self.level(ax,r))
   if t<11:
    q,p=self.ordinary(t*.35);g.add(Dot(ax.c2p(q,p),radius=.08,color=GOLD))
   else:
    u=float(np.clip((t-22)/3.5,0,4));boundary,points=packet(u)
    if t>=19:g.add(self.region(ax,u,GOLD,False))
    g.add(*[Dot(ax.c2p(q,p),radius=.045,color=GOLD) for q,p in points])
  elif i==2:
   u=float(np.clip((t-36)/3.5,0,4))
   for ax,z,c in [(self.left.copy(),0,BLUE),(self.right.copy(),u,GREEN)]:g.add(ax,self.region(ax,z,c,True))
  elif i==3:
   if t>=76:g.add(Line([-5.6,.1,0],[5.6,.1,0],color=MUTED,stroke_opacity=.2))
  elif i==4:
   q,p=self.ordinary((t-105)*.65);g.add(self.pend(q,p))
   E=float(H(.65,0));T=p*p/(2*I);V=float(H(q,0))
   for y,val,c in [(.25,T,BLUE),(-.9,V,GOLD)]:
    g.add(Line([.6,y,0],[5.4,y,0],color=MUTED,stroke_width=16,stroke_opacity=.2))
    if val/E>.0001:g.add(Line([.6,y,0],[.6+4.8*val/E,y,0],color=c,stroke_width=16))
  elif i==5:
   for start,y,c in [(0,1.2,GOLD),(2,-.5,BLUE)]:
    ax=axes(.7,y,9.4,1.0,[0,8,2],[-.75,.75,.5]);g.add(ax)
    end=min(8,start+(t-134)*.25);xs=np.linspace(start,max(start+.001,end),121)
    ys=np.array([self.ordinary((v-start)*.8)[0] for v in xs]);g.add(curve(ax,xs,ys,c,4),Dot(ax.c2p(xs[-1],ys[-1]),color=c,radius=.055))
  elif i==6:
   u=(t-165)*.5
   for x,c in [(-4.4,GOLD),(0,BLUE),(4.4,GREEN)]:g.add(RoundedRectangle(width=3.8,height=3.8,corner_radius=.15,color=c,stroke_opacity=.25).move_to([x,.25,0]))
   xs=np.linspace(-1.5,1.5,100);g.add(VMobject(color=GOLD,fill_opacity=0).set_points_as_corners([[-4.4+x,.5+.45*np.cos(3*x),0] for x in xs]))
   a=(u%3)/3;g.add(Line([-1.45,.35,0],[1.45,.35,0],color=MUTED),Dot([-1.4+2.8*a,.35,0],color=BLUE),arr([-.9,.9,0],[1.5,0,0],BLUE))
   center=np.array([4.4,.4,0]);pos=center+np.array([.85*np.cos(u),.85*np.sin(u),0]);g.add(Circle(radius=.85,color=MUTED,stroke_opacity=.5).move_to(center),Dot(center,radius=.04,color=MUTED),Dot(pos,color=GREEN),arr(pos,np.array([-.55*np.sin(u),.55*np.cos(u),0]),GREEN))
  elif i==7:
   if t<228:
    ax=axes(0,.1,8,2.9,[-.8,.8,.4],[-7,7,2]);q,p=self.ordinary((t-197)*.5);g.add(ax,self.level(ax,float(H(.65,0)/EC),BLUE,.7),Dot(ax.c2p(q,p),color=GOLD,radius=.085))
   elif t>=244:
    for x,c,energy in [(-3.3,GOLD,False),(3.3,GREEN,True)]:
     ax=axes(x,.5,5.3,1.8,[0,6,2],[-6,6,3] if not energy else [0,8,2]);g.add(ax)
     xs=np.linspace(0,min(6,(t-244)*.5+.03),121);ys=[float(H(.65,0)) if energy else self.ordinary(v)[1] for v in xs];g.add(curve(ax,xs,ys,c,4))
  elif i==8:
   if t>=275:g.add(*[RoundedRectangle(width=6.1,height=2.15,corner_radius=.15,stroke_color=c,stroke_opacity=.4,fill_color=c,fill_opacity=.04).move_to([x,-.75,0]) for x,c in [(-3.25,BLUE),(3.25,GREEN)]])
  else:
   ax=axes(-3.6,.05,4.3,2.5,[-.8,.8,.4],[-7,7,2]);q,p=self.ordinary((t-296)*.4);g.add(ax,self.level(ax,float(H(.65,0)/EC),BLUE,.8),Dot(ax.c2p(q,p),color=GOLD))
   xs=np.linspace(-2,2,161);ys=np.exp(-xs*xs)*np.cos(7*xs+(t-296)*.25)
   g.add(VMobject(stroke_color=GREEN,stroke_width=3,fill_opacity=0).set_points_as_corners([[3.6+x,y*.9,0] for x,y in zip(xs,ys)]),Arrow([-0.6,0,0],[.6,0,0],color=MUTED))
  return g
