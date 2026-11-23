"""Brownian samples -> heat semigroup -> path weights -> risk-neutral pricing."""
import importlib.util,json,textwrap
from pathlib import Path
import numpy as np
from manim import *
from mechanics import KAPPA,DT,N,X0,HEAT_T,RATE,SIGMA,STRIKE,f,f2,heat,density,potential,call,dataset,walk_at
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('heat_common',R.parent/'chapter_01/visuals.py');common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
tx=common.tx;eq=common.eq;path=common.path;arr=common.arr
BG='#10131C';INK='#F1F4FA';MUTED='#8E9BB0';BLUE='#4A9EFF';GREEN='#36C7A3';ORANGE='#F0A45D';PURPLE='#B69AFF';GOLD='#E9C46A';YELLOW='#F3CE77'
config.frame_width=128/9;config.frame_height=8;config.background_color=BG;config.tex_dir=str(R.parents[2]/'media/Tex')
def prog(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def point(x,y,cx=0,cy=-1.1,w=10,scale=3,xr=(-6,6)):
 return np.array([cx+w*((x-xr[0])/(xr[1]-xr[0])-.5),cy+scale*y,0])
def plot(fn,c=BLUE,cx=0,cy=-1.1,w=10,scale=3,xr=(-6,6),opacity=1,axis=True):
 x=np.linspace(*xr,241);y=np.asarray(fn(x))+np.zeros_like(x);g=VGroup()
 if axis:g.add(Line([cx-w/2,cy,0],[cx+w/2,cy,0],stroke_color=MUTED,stroke_opacity=.35,stroke_width=1))
 g.add(path(np.column_stack([cx+w*((x-xr[0])/(xr[1]-xr[0])-.5),cy+scale*y,np.zeros_like(x)]),c,3,opacity));return g
def marker(x,y,c=GREEN,**kw):
 p=point(x,y,**kw);base=np.array([p[0],kw.get('cy',-1.1),0]);g=VGroup()
 if np.linalg.norm(p-base)>1e-8:g.add(DashedLine(base,p,color=c,stroke_opacity=.45))
 g.add(Dot(p,radius=.05,color=c));return g
def hist(values,cx=0,cy=-1.1,w=10,scale=3,xr=(-6,6),bins=36):
 edges=np.linspace(*xr,bins+1);count,_=np.histogram(values,bins=edges);heights=count/(len(values)*(edges[1]-edges[0]));g=VGroup()
 for j,v in enumerate(heights):g.add(Rectangle(width=w/bins-.01,height=max(.003,scale*v),stroke_width=0,fill_color=BLUE,fill_opacity=.27).move_to([cx-w/2+w*(j+.5)/bins,cy+scale*v/2,0]))
 return g
def particles(tau,cx=0,cy=-1.7,w=10,xr=(-6,6),number=96):
 values=walk_at(tau,np.arange(number));return VGroup(*[Dot([cx+w*((v-xr[0])/(xr[1]-xr[0])-.5),cy+.35*(j%8)/7,0],radius=.022,color=GREEN) for j,v in enumerate(values)])
def time_label(tau,x=4.8,y=-1.95):return tx(f't = {tau:.2f}',x,y,22,c=YELLOW,w=2.3)
def planar_path(d,j,q=1,opacity=1,solo=False):
 k=max(1,min(190,int(q*140)));a=d['planar'][j,:k+1]
 ref=d['planar'][0:1,:141] if solo else d['planar'][:4,:141]
 extent=np.max(np.abs(ref),axis=(0,1));zoom=min(4/max(extent[0],.01),(1.1 if solo else 1.5)/max(extent[1],.01))
 pts=np.column_stack([zoom*a[:,0],zoom*a[:,1]+.05,np.zeros(len(a))]);return VGroup(path(pts,GREEN,2,opacity),Dot(pts[-1],radius=.09,color=GREEN))
def stock_paths(d,q=1,cx=0,cy=-1.3,w=10,h=2.7,number=10):
 paths=d['stock'][:number];low=float(paths.min())-12;high=float(paths.max())+12;k=max(1,min(96,int(q*96)));g=VGroup()
 for j,values in enumerate(paths):
  points=[[cx-w/2+w*i/96,cy+h*(v-low)/(high-low),0] for i,v in enumerate(values[:k+1])];g.add(path(points,GOLD if j%2 else GREEN,1.8,.65),Dot(points[-1],radius=.035,color=GOLD))
 g.add(Line([cx-w/2,cy,0],[cx+w/2,cy,0],stroke_color=MUTED,stroke_opacity=.35));return g
def fplot(fn=f,c=INK,cx=0,w=10,opacity=1):return plot(fn,c,cx=cx,w=w,cy=-1.2,scale=.027,opacity=opacity)
def section(t):
 return '입자에서 확률분포로' if t<119 else '무작위 평균에서 이차 미분으로' if t<167 else '도착한 함수값의 평균' if t<228 else '파인만–카츠 · 경로의 기댓값' if t<252 else '위험중립 확률과 옵션 가격' if t<318 else '하나의 확산 구조, 여러 관점'
class ProbabilityScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def init_scene(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.header=VGroup();self.d=dataset()
 def construct(self):
  self.init_scene();self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#192031',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[4,9,16,22,28,36,40,53,57,62,71,76,80,85,90,100,104,108,113,124,128,135,138,143,147,152,157,160,171,182,187,191,193,195,197,202,208,215,218,222,228,234,238,242,246,252,256,261,265,267,271,274,278,281,285,289,293,296,302,304,306,308,318,325,331,337,340,346,352]
  events=sorted(set([self.start,self.end]+[l['start'] for l in self.lines if self.start<l['start']<self.end]+[z for z in extra if self.start<z<self.end]))
  for a,b in zip(events,events[1:]):self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  self.remove(self.caption,self.static,self.header);line=next(l for l in self.lines if l['start']<=t<l['end'])
  self.caption=VGroup(*[tx(s,size=25,w=30) for s in textwrap.wrap(line['text'],width=49,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.09)
  if self.caption.width>12:self.caption.scale_to_fit_width(12)
  if self.caption.height>.82:self.caption.scale_to_fit_height(.82)
  self.caption.move_to([0,-3.27,0]).set_z_index(51);self.static=self.labels(t)
  self.header=VGroup(tx('CHAPTER 04  /  PROBABILITY',-4.25,3.69,16,c=MUTED,w=5.4),tx(section(t),4.1,3.69,19,c=INK,w=5.6),Line([-6.4,3.45,0],[6.4,3.45,0],stroke_color=MUTED,stroke_opacity=.25));self.add(self.caption,self.static,self.header)
  for kind,g in [('caption',self.caption),('label',self.static),('header',self.header),('geometry',self.geometry(t))]:
   if not len(g):continue
   d=dict(kind=kind,time=t,left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1]));self.audit.append(d)
   assert d['left']>=-6.9 and d['right']<=6.9 and d['top']<=3.88,(self.index,d)
   assert d['bottom']>=(-3.8 if kind=='caption' else -2.65),(self.index,d)
   if kind=='label':assert d['top']<3.35,(self.index,d)
 def labels(self,t):
  i=self.index;g=VGroup(tx(self.rec['title'],0,2.98,29,c=YELLOW))
  if i==1:g.add(tx('열의 확산',-3.3,1.8,27,c=BLUE,w=5),tx('입자의 움직임',3.3,1.8,27,c=GREEN,w=5),tx('?',0,.1,48,c=PURPLE,w=1),tx('같은 현상을 이해하는 다른 관점',0,-2.35,26,c=PURPLE))
  elif i==2:
   if t>=28:g.add(tx('Brownian Motion · 브라운 운동',0,2.05,29,c=GREEN))
   g.add(tx('분자 충돌은 개념도 · 경로는 이상화한 확률 모형',0,-2.4,21,c=MUTED))
  elif i==3:g.add(tx('같은 출발점에서 반복한 네 개의 시행',0,2.05,26,c=GREEN),tx('한 경로의 도착점과 위치의 확률분포를 구별한다',0,-2.4,22,c=MUTED))
  elif i==4:g.add(eq(r'X_t=x+\sqrt{2\kappa}B_t,\qquad\kappa=1',0,2.05,35,c=GREEN),tx('통계: 4,096경로 · 점은 일부만 표시 · 1차원 위치를 세로 정렬',0,-2.4,20,c=MUTED))
  elif i in [5,6]:
   g.add(eq(r'p(x,t)=\frac{e^{-x^2/(4\kappa t)}}{\sqrt{4\pi\kappa t}}' if i==5 else r'\mathrm{Var}(X_t)=2\kappa t',0,2.05,36,c=BLUE if i==5 else ORANGE),tx('전체 실수선의 위치 밀도 · 그래프는 일부 구간 · κ = 1',0,-2.4,20,c=MUTED))
  elif i==7:g.add(eq(r'\partial_t p=\kappa\partial_{xx}p',0,2.05,45,c=BLUE),tx('확률밀도가 따르는 시간 변화 법칙',0,-2.35,27,c=GREEN))
  elif i==8:
   g.add(eq(r'\partial_t u=\kappa u_{xx}',-3.4,2,35,c=INK,w=5.5),eq(r'\partial_t p=\kappa p_{xx}',3.4,2,35,c=BLUE,w=5.5),tx('온도 분포',-3.4,1.25,25,c=INK,w=5),tx('확률밀도',3.4,1.25,25,c=BLUE,w=5),tx('서로 다른 물리량, 동일한 확산 연산',0,-2.35,27,c=PURPLE))
  elif i==9:g.add(eq(r'x\longrightarrow x+\Delta X',0,2.05,42,c=ORANGE),tx('아주 짧은 시간 Δt 동안의 이동',0,-2.3,27,c=MUTED))
  elif i==10:g.add(eq(r'\mathbb E[\Delta X]=\frac{-a+a}{2}=0',0,2.05,40,c=ORANGE),tx('좌우 이동 확률은 각각 1/2',0,-2.3,27,c=MUTED))
  elif i==11:
   g.add(eq(r'\mathbb E[(\Delta X)^2]=a^2>0',0,2.05,40,c=ORANGE))
   if t>=143:g.add(eq(r'a^2=2\kappa\Delta t',0,-1.7,40,c=YELLOW))
   g.add(tx('대칭 이동 모형으로 보는 작은 시간의 분산 관계',0,-2.4,21,c=MUTED))
  elif i==12:
   if t<152:g.add(eq(r'\frac{f(x-a)+f(x+a)}2',0,2.05,40,c=PURPLE))
   else:g.add(eq(r'\frac{f(x-a)+f(x+a)}2\approx f(x)+\frac{a^2}{2}f^{\prime\prime}(x)',0,2.05,35,c=PURPLE))
   g.add(tx('반대 부호의 1차항은 상쇄 · 2차항은 남는다',0,-2.4,24,c=ORANGE))
  elif i==13:g.add(eq(r'\frac{\mathbb E[f(x+\Delta X)]-f(x)}{\Delta t}\longrightarrow\kappa f^{\prime\prime}(x)',0,1.8,39,c=PURPLE),eq(r'\partial_tu=\kappa u_{xx}',0,-.2,52,c=INK),tx('매끄러운 함수 · 적절한 작은 시간 극한',0,-2.35,23,c=MUTED))
  elif i==14:g.add(tx('입자의 위치 분포 → 도착한 위치의 함수값',0,2.05,27,c=PURPLE),tx('무작위 움직임으로 미래의 함수를 계산할 수 있을까?',0,-2.35,26,c=GREEN))
  elif i==15:g.add(eq(r'f(x)=u(x,0)',0,2.05,42,c=INK),tx('처음 주어진 함수는 고정 · 출발 위치 x = 0.6',0,-2.35,25,c=GREEN))
  elif i==16:g.add(eq(r'X_t\quad\longmapsto\quad f(X_t)',0,2.05,42,c=GREEN),tx('입자는 위치축에서 이동하고, 도착 위치를 f에 입력한다',0,-2.4,23,c=MUTED))
  elif i==17:
   g.add(eq(r'u(x,t)=\mathbb E[f(x+\sqrt{2\kappa}B_t)]',0,2.05,38,c=PURPLE),tx('유한 표본평균 ≈ 기댓값 · 출발 위치 x=0.6, t=0.8',0,-2.4,22,c=MUTED))
  elif i==18:
   g.add(eq(r'\mathbb E_x[f(X_t)]=\int_{\mathbb R}f(y)p_t(y\mid x)\,dy',0,2.05,36,c=PURPLE),tx('같은 분포의 반복 표본평균은 이 기댓값의 근사',0,-2.4,23,c=MUTED))
  elif i==19:g.add(eq(r'u(x,t)=\int_{\mathbb R}f(y)\,G_t(y-x)\,dy',0,2.05,39,c=PURPLE),tx('출발 위치 x를 반영한 가우스 가중평균',0,-2.4,24,c=MUTED))
  elif i==20:
   g.add(tx('FEYNMAN–KAC FORMULA',0,2.03,30,c=PURPLE))
   if t>=234:g.add(eq(r'u_t=Lu-cu',-3.4,.9,38,c=INK,w=5),eq(r'\mathbb E_x\!\left[e^{-\int_0^t c(X_s)\,ds}f(X_t)\right]',3.1,.9,33,c=PURPLE,w=6.1),tx('미분방정식의 해',-3.4,-.2,25,w=5),tx('확률적 경로의 기댓값',3.1,-.2,25,c=PURPLE,w=6))
   g.add(tx('단순한 열방정식에서는 c=0 · 적절한 정칙성·적분 조건',0,-2.4,21,c=MUTED))
  elif i==21:g.add(eq(r'\mathrm{weight}=\exp\!\left(-\int_0^t c(X_s)\,ds\right)',0,2.05,35,c=PURPLE),tx('c(x)=0.15+0.06 sin x · 실제 경로 적분으로 계산한 가중치',0,-2.4,21,c=MUTED))
  elif i==22:g.add(eq(r'X_t\longrightarrow S_t',0,2.05,42,c=GOLD),tx('좌표축과 확률 모형의 의미가 바뀐다',0,-2.35,26,c=GOLD))
  elif i==23:g.add(eq(r'\Phi(S_T)=\max(S_T-K,0)',0,2.05,40,c=GOLD),tx('유럽형 콜옵션 · K=100 · 만기 지급액과 현재 가격은 별개',0,-2.4,21,c=MUTED))
  elif i==24:g.add(eq(r'dS_t=rS_t\,dt+\sigma S_t\,dB_t^{\mathbb Q}',0,2.05,37,c=GOLD),tx('모형 예시 · 무배당 · r=0.04 · σ=0.2 · S₀=100',0,-2.4,21,c=MUTED))
  elif i==25:g.add(eq(r'V(S,t)=e^{-r(T-t)}\mathbb E^{\mathbb Q}[\Phi(S_T)\mid S_t=S]',0,2.05,35,c=GOLD),tx('Q는 무차익 가격결정용 확률 · 실제 주가 확률을 그대로 뜻하지 않음',0,-2.4,20,c=MUTED))
  elif i==26:
   if t<296:g.add(tx('BLACK–SCHOLES EQUATION',0,2.05,31,c=GOLD))
   else:g.add(eq(r'V_t+\frac12\sigma^2S^2V_{SS}+rSV_S-rV=0',0,2.05,39,c=GOLD))
   g.add(tx('일정한 r, σ · 무배당·무차익 모형 · 시간에 따른 옵션 가격 V',0,-2.4,21,c=MUTED))
  elif i==27:
   if t<304:
    g.add(eq(r'x=\log(S/K),\quad\tau=\frac{\sigma^2}{2}(T-t),\quad q=\frac{2r}{\sigma^2}',0,2.0,32),eq(r'v_\tau=v_{xx}+(q-1)v_x-qv,\quad v=V/K',0,.25,35,c=GOLD),tx('로그 가격 · 시간 반전과 재척도',0,-2.3,25,c=MUTED))
   elif t<306:
    g.add(eq(r'v=e^{ax+b\tau}w,\quad a=\frac{1-q}{2},\quad b=-\frac{(q+1)^2}{4}',0,1.65,34,c=GOLD),eq(r'w_\tau=w_{xx}',0,-.3,58,c=INK),tx('함수의 지수 보정으로 나머지 항을 제거',0,-2.3,25,c=MUTED))
   else:g.add(eq(r'\frac{\partial w}{\partial\tau}=\frac{\partial^2w}{\partial x^2}',0,.4,64,c=INK),tx('변수와 함수를 함께 바꾸어 얻은 열방정식',0,-2.3,26,c=GOLD))
  elif i in [28,32]:
   for x,s,c in [(-4.4,'열의 확산',INK),(0,'위치의 확률밀도',BLUE),(4.4,'옵션 가격',GOLD)]:g.add(tx(s,x,2.05,24,c=c,w=3.8))
   g.add(tx('서로 다른 현상 속에서 반복되는 확산 구조',0,-2.35,26,c=PURPLE))
  elif i==29:g.add(eq(r'\partial_t p=\kappa p_{xx}',0,2.05,42,c=BLUE),tx('브라운 운동 — 위치 확률분포의 진화',0,-2.4,26,c=GREEN))
  elif i==30:g.add(eq(r'u(x,t)=\mathbb E_x[f(X_t)]',0,2.05,42,c=PURPLE),tx('파인만–카츠 — 확률적 기댓값으로 해 표현',0,-2.4,25,c=PURPLE))
  elif i==31:g.add(eq(r'V=e^{-r(T-t)}\mathbb E^{\mathbb Q}[\Phi(S_T)]',0,2.05,39,c=GOLD),tx('블랙–숄즈 — 무차익 조건 아래의 확률적 가격결정',0,-2.4,24,c=GOLD))
  elif i==33:g.add(tx('공간의 기하학도 열의 퍼짐으로 연구할 수 있을까?',0,-1.95,27,c=PURPLE),tx('고정된 곡면 위의 확산 개념도 · 기하학적 흐름과 구별',0,-2.45,18,c=MUTED))
  return g
 def geometry(self,t):
  i=self.index;p=prog(t,self.start,self.end);d=self.d;g=VGroup()
  if i==1:
   tau=.64+.4*p;g.add(plot(lambda x:density(x,tau),BLUE,cx=-3.3,w=5.1,cy=-1.2,scale=4),Dot([3.3+.4*np.sin(t),-.1+.2*np.cos(t*1.7),0],radius=.1,color=GREEN))
  elif i==2:
   g=planar_path(d,0,prog(t,16,32),solo=True);pt=g[-1].get_center()
   for j in range(26):
    a=2*np.pi*j/26+t*1.5;r=.18+.07*(j%4);g.add(Dot(pt+[r*np.cos(a),r*np.sin(a),0],radius=.018,color=BLUE).set_opacity(.6))
  elif i==3:
   active=0 if t<36 else 1 if t<40 else 3
   for j in range(active+1):g.add(planar_path(d,j,prog(t,32+2*j,36+2*j),.3 if j<active else 1))
  elif i==4:
   tau=.05+.3*p if t<53 else 0 if t<57 else .3*prog(t,57,67)
   q=prog(t,57,62) if t>=53 else 1
   pos=walk_at(tau,np.arange(120))
   for j,x in enumerate(pos):g.add(Dot([10*x/12,-.2+q*(-1.3+.55*(j%8)/7),0],radius=.025,color=GREEN))
   g.add(Line([-5,-1.6,0],[5,-1.6,0],stroke_color=MUTED,stroke_opacity=.25),time_label(tau))
  elif i==5:
   tau=.3+.15*p;g.add(particles(tau),hist(walk_at(tau),cy=-1.05,scale=3.5))
   if t>=76:g.add(plot(lambda x:density(x,tau),BLUE,cy=-1.05,scale=3.5))
   g.add(time_label(tau))
  elif i in [6,29]:
   tau=.45+.95*p if i==6 else .3+.7*p
   g.add(hist(walk_at(tau),cy=-1.05,scale=3.5),plot(lambda x:density(x,.3),MUTED,cy=-1.05,scale=3.5,opacity=.3),plot(lambda x:density(x,tau),BLUE,cy=-1.05,scale=3.5),time_label(tau))
   sd=np.sqrt(2*KAPPA*tau);a=point(-sd,0,cy=-1.7);b=point(sd,0,cy=-1.7);g.add(Line(a,b,color=ORANGE,stroke_width=3),Dot(a,radius=.04,color=ORANGE),Dot(b,radius=.04,color=ORANGE),tx(f'분산 = {2*KAPPA*tau:.2f}',0,-1.95,24,c=ORANGE,w=4))
  elif i==7:
   tau=.5+.6*p;g.add(plot(lambda x:density(x,tau),BLUE,scale=4),time_label(tau))
  elif i==8:
   tau=.2+.8*p
   g.add(plot(lambda x:80*density(x,tau)/density(0,.2),INK,cx=-3.4,w=5.3,cy=-1.2,scale=.027),plot(lambda x:density(x,tau),BLUE,cx=3.4,w=5.3,cy=-1.2,scale=.027*80/density(0,.2)))
  elif i in [9,10]:
   g.add(Line([-5,-.6,0],[5,-.6,0],stroke_color=MUTED,stroke_opacity=.4),Dot([0,-.6,0],radius=.08,color=GREEN))
   if i==9:g.add(arr([0,-.6,0],[1.7*p,-.6,0],ORANGE) if p>.02 else Dot([0,-.6,0],radius=.02,color=ORANGE),tx('x',0,-1.1,26,c=GREEN,w=1),tx('x + ΔX',2,-1.1,26,c=ORANGE,w=3))
   else:g.add(arr([0,-.6,0],[-2.8,-.6,0],BLUE),arr([0,-.6,0],[2.8,-.6,0],ORANGE),tx('−a',-2.8,.1,35,c=BLUE,w=2),tx('+a',2.8,.1,35,c=ORANGE,w=2),tx('1/2',-2.8,-1.3,28,c=MUTED,w=2),tx('1/2',2.8,-1.3,28,c=MUTED,w=2))
  elif i==11:
   for x,s,c in [(-2.8,r'(-a)^2=a^2',BLUE),(2.8,r'(+a)^2=a^2',ORANGE)]:g.add(eq(s,x,.4,41,c=c,w=5))
   g.add(arr([-2,.0,0],[-.4,-.8,0],BLUE),arr([2,.0,0],[.4,-.8,0],ORANGE),eq(r'a^2',0,-.7,43,c=YELLOW,w=2))
  elif i==12:
   a=.45-.25*p;xr=(-.6,1.8);g.add(plot(f,INK,cy=-1.3,scale=.035,xr=xr))
   for z,c in [(X0-a,BLUE),(X0,GREEN),(X0+a,ORANGE)]:g.add(marker(z,float(f(z)),c,cy=-1.3,scale=.035,xr=xr))
   mean=.5*(f(X0-a)+f(X0+a));pa=point(X0-a,mean,cy=-1.3,scale=.035,xr=xr);pb=point(X0+a,mean,cy=-1.3,scale=.035,xr=xr);g.add(Line(pa,pb,color=PURPLE,stroke_width=3),tx('1차항 상쇄',-3.5,-1.9,24,c=PURPLE,w=5),tx('2차항 유지',3.5,-1.9,24,c=ORANGE,w=5))
  elif i==13:g.add(arr([-4.4,.1,0],[-2.4,.1,0],GREEN),arr([4.4,.1,0],[2.4,.1,0],GREEN))
  elif i==14:
   q=prog(t,171,178);g.add(plot(lambda x:(1-q)*60*density(x,.5)+q*f(x),BLUE if q<.5 else INK,cy=-1.2,scale=.027))
  elif i==15:
   g.add(fplot(),marker(X0,0,GREEN,cy=-1.2,scale=.027),tx('x = 0.6',point(X0,0)[0],-1.7,25,c=GREEN,w=3))
  elif i==16:
   if t<191:j=0;q=prog(t,187,191)
   else:j=min(3,1+int((t-191)/2));q=((t-191)%2)/2
   xx=X0+float(walk_at(HEAT_T*q,[j])[0]);vv=float(f(xx));g.add(fplot(cx=-1.5,w=8),marker(xx,vv,GREEN,cx=-1.5,w=8,cy=-1.2,scale=.027),Dot(point(xx,0,cx=-1.5,w=8,cy=-1.2,scale=.027),radius=.07,color=GREEN),tx('출발 x',point(X0,0,cx=-1.5,w=8)[0],-1.7,23,c=MUTED,w=2))
   g.add(RoundedRectangle(width=3.1,height=1.25,corner_radius=.12,stroke_color=PURPLE,fill_opacity=0).move_to([4.6,.0,0]),tx(f'f(X) = {vv:.2f}',4.6,.0,26,c=PURPLE,w=2.8))
  elif i in [17,30]:
   q=p;n=max(16,min(N,int(16*(N/16)**q)));estimate=float(d['means'][n-1]);exact=float(heat(X0,HEAT_T));se=float(d['values'][:n].std(ddof=1)/np.sqrt(n))
   g.add(fplot(cx=-3.3,w=5.2,opacity=.2),fplot(lambda x:heat(x,HEAT_T),INK,cx=-3.3,w=5.2),marker(X0,exact,PURPLE,cx=-3.3,w=5.2,cy=-1.2,scale=.027))
   indices=np.unique(np.geomspace(16,n,90).astype(int));pts=[[.1+5.6*(np.log(k/16)/np.log(N/16)),-1.3+.07*(d['means'][k-1]-35),0] for k in indices]
   g.add(path(pts,PURPLE,2.5),Line([.1,-1.3+.07*(exact-35),0],[5.7,-1.3+.07*(exact-35),0],stroke_color=INK,stroke_opacity=.4),tx(f'N = {n:,}',3,1.25,24,c=GREEN,w=5),tx(f'표본평균 {estimate:.2f} ± {1.96*se:.2f}',3,.7,25,c=PURPLE,w=5.6),tx(f'정확한 해 {exact:.2f}',3,-1.8,25,c=INK,w=5))
  elif i==18:
   g.add(fplot(opacity=.25),fplot(lambda x:heat(x,HEAT_T),INK),marker(X0,float(heat(X0,HEAT_T)),PURPLE,cy=-1.2,scale=.027),tx('평균이 주는 값은 출발 위치의 u(x,t)',0,-1.95,25,c=PURPLE))
  elif i==19:
   g.add(plot(lambda y:f(y)*density(y,HEAT_T,X0),PURPLE,cy=-1.3,scale=.12),tx(f'실제 적분 = {float(heat(X0,HEAT_T)):.3f}',0,-1.95,25,c=PURPLE))
   xs=np.linspace(-6,6,161);ys=f(xs)*density(xs,HEAT_T,X0);pts=[[-5,-1.3,0]]+[[10*(x/12),-1.3+.12*v,0] for x,v in zip(xs,ys)]+[[5,-1.3,0]];g.add(Polygon(*pts,stroke_width=0,fill_color=PURPLE,fill_opacity=.18))
  elif i==20:
   if t<234:
    for j in range(6):
     a=d['walk'][j,:81];g.add(path([[-5+10*k/80,-.4+.25*v,0] for k,v in enumerate(a)],GREEN,1.4,.45))
    g.add(eq(r'u(x,t)=\mathbb E_x[f(X_t)]',0,-1.6,40,c=PURPLE))
   else:g.add(arr([-.9,.4,0],[.7,.4,0],PURPLE),tx('L = κ ∂ₓₓ',0,-1.55,28,c=MUTED))
  elif i==21:
   for j in range(5):
    cy=1.0-j*.5;a=d['walk'][j,:81];weight=float(d['weights'][j]);g.add(path([[-5+7*k/80,cy+.13*v,0] for k,v in enumerate(a)],GREEN,1.8,.7),tx(f'가중치 {weight:.3f}',4,cy,23,c=PURPLE,w=3.5))
   g.add(tx(f'가중 표본평균 ≈ {float(d["weighted"].mean()):.2f}',0,-1.9,25,c=PURPLE))
  elif i==22:
   if t<256:
    a=d['walk'][0,:101];g.add(path([[-5+10*k/100,.25*v,0] for k,v in enumerate(a)],GREEN,3))
   else:g.add(stock_paths(d,prog(t,256,261)),tx('시간',5.6,-1.75,22,c=MUTED,w=2),tx('주가 S',-5.7,1.6,22,c=GOLD,w=2))
  elif i==23:
   s=120 if t<267 else 80;pay=max(s-100,0)
   for x,title,value,c in [(-4,'행사가격 K','100',MUTED),(0,'만기 주가 S',str(s),GOLD),(4,'만기 지급액',str(pay),GREEN)]:
    g.add(RoundedRectangle(width=3.4,height=2.0,corner_radius=.12,stroke_color=c,stroke_opacity=.5).move_to([x,.0,0]),tx(title,x,.55,24,c=c,w=3),tx(value,x,-.25,44,c=c,w=3))
  elif i==24:g.add(stock_paths(d,prog(t,271,281)),tx('현재 주가 100',-4.2,-1.85,22,c=MUTED,w=4),tx('만기 T = 1',4.5,-1.85,22,c=MUTED,w=3))
  elif i in [25,31]:
   n=max(32,min(N,int(32*(N/32)**p)));pay=d['payoff'][:n];mc=float(np.exp(-RATE)*pay.mean());se=float(d['discounted'][:n].std(ddof=1)/np.sqrt(n))
   for j in range(5):g.add(tx(f'만기 지급액 {d["payoff"][j]:.2f}',-3.5,1.2-j*.6,23,c=GOLD,w=5))
   g.add(arr([-.3,0,0],[.8,0,0],PURPLE),tx(f'할인계수 e⁻ʳᵀ = {np.exp(-RATE):.3f}',3.7,1.25,23,c=MUTED,w=5.5),tx(f'가격 추정 {mc:.2f}',3.7,.2,32,c=GOLD,w=5),tx(f'95% 근사 오차폭 ±{1.96*se:.2f}',3.7,-.5,22,c=MUTED,w=5.5),tx(f'모형의 정확한 값 {float(call(100,1)):.2f}',3.7,-1.35,24,c=INK,w=5.5))
  elif i==26:
   remaining=1-.85*p;g.add(plot(lambda s:call(s,remaining),GOLD,xr=(40,160),cy=-1.3,scale=.035),plot(lambda s:np.maximum(s-100,0),MUTED,xr=(40,160),cy=-1.3,scale=.035,opacity=.35),tx(f'만기까지 {remaining:.2f}년',0,-1.95,24,c=GOLD),tx('주가 S',5.6,-1.7,22,c=MUTED,w=2))
  elif i==27:
   if t>=306:g.add(Line([-4,-1,0],[4,-1,0],stroke_color=MUTED,stroke_opacity=.3))
  elif i in [28,32]:
   tau=.5+.4*p
   g.add(plot(lambda x:heat(x,tau),INK,cx=-4.4,w=3.5,cy=-1.0,scale=.025),plot(lambda x:density(x,tau),BLUE,cx=0,w=3.5,cy=-1,scale=3),plot(lambda s:call(s,.7),GOLD,cx=4.4,w=3.5,xr=(50,150),cy=-1,scale=.035),Line([-2.35,-.1,0],[-2.05,-.1,0],stroke_color=PURPLE),Line([2.05,-.1,0],[2.35,-.1,0],stroke_color=PURPLE))
   if i==32:g.add(eq(r'\partial_tu=\kappa\Delta u',0,-1.9,37,c=INK))
  elif i==33:
   q=prog(t,346,352);g=common.surface(q)
   if t>=352:
    for radius in [.35,.7,1.05]:
     r=radius+.25*prog(t,352,357);g.add(path([common.project([r*np.cos(a),r*np.sin(a),.6*np.cos(.9*r*np.cos(a))*np.sin(.8*r*np.sin(a))])+[0,.3,0] for a in np.linspace(0,2*np.pi,90)],ORANGE,1.8,.5))
  return g
