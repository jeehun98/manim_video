"""Properties of the heat equation, with analytic graphs and computed bounds."""
import importlib.util,json,textwrap
from pathlib import Path
import numpy as np
from manim import *
from mechanics import KAPPA,initial,temperature,mode,mode_coeff,kernel,harnack
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('heat_common',R.parent/'chapter_01/visuals.py');common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
tx=common.tx;eq=common.eq;path=common.path;arr=common.arr
BG='#10131C';INK='#F1F4FA';MUTED='#8E9BB0';BLUE='#4A9EFF';GREEN='#36C7A3';ORANGE='#F0A45D';PURPLE='#B69AFF';YELLOW='#F3CE77';RED='#F17C85'
config.frame_width=128/9;config.frame_height=8;config.background_color=BG;config.tex_dir=str(R.parents[2]/'media/Tex')
GRID=np.unique(np.r_[np.linspace(-np.pi,np.pi,301),-1.6,-.5,.65,1.2,1.75])
def prog(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def chart(fn,c=BLUE,cx=0,cy=-1.2,w=10,scale=.025,xr=(-np.pi,np.pi),opacity=1,axis=True,dashed=False):
 x=GRID if xr==(-np.pi,np.pi) else np.linspace(*xr,241);y=np.asarray(fn(x))+np.zeros_like(x)
 pts=np.column_stack([cx+w*((x-xr[0])/(xr[1]-xr[0])-.5),cy+scale*y,np.zeros_like(x)])
 g=VGroup()
 if axis:g.add(Line([cx-w/2,cy,0],[cx+w/2,cy,0],stroke_color=MUTED,stroke_opacity=.35,stroke_width=1))
 curve=path(pts,c,3,opacity)
 if dashed:curve=DashedVMobject(curve,num_dashes=65)
 g.add(curve);return g
def coordinate(x,value,cx=0,cy=-1.2,w=10,scale=.025,xr=(-np.pi,np.pi)):
 return np.array([cx+w*((x-xr[0])/(xr[1]-xr[0])-.5),cy+scale*value,0])
def initial_plot(c=INK,cx=0,cy=-1.2,w=10,scale=.025,opacity=1):
 # Separate paths at genuine jumps: never join discontinuous values by a slope.
 pieces=[[(-np.pi,0),(-1.6,0)],[(-1.6,100),(-.5,100)],[(-.5,0),(.65,0)],[(.65,0),(1.2,85),(1.75,0)],[(1.75,0),(np.pi,0)]]
 return VGroup(*[path([coordinate(x,v,cx=cx,cy=cy,w=w,scale=scale) for x,v in piece],c,3,opacity) for piece in pieces])
def marker(x,value,c=PURPLE,**kwargs):
 pt=coordinate(x,value,**kwargs);cy=kwargs.get('cy',-1.2)
 return VGroup(DashedLine([pt[0],cy,0],pt,color=c,stroke_opacity=.5),Dot(pt,radius=.055,color=c))
def limits(cy=-1.2,w=10,scale=.025):
 return VGroup(Line([-w/2,cy+100*scale,0],[w/2,cy+100*scale,0],stroke_color=RED,stroke_width=2),Line([-w/2,cy,0],[w/2,cy,0],stroke_color=GREEN,stroke_width=2),tx('100°C',-5.7,cy+100*scale,21,c=RED,w=1.5),tx('0°C',-5.7,cy,21,c=GREEN,w=1.5))
def timeline(tau,maximum=3,y=-1.95):
 q=np.clip(tau/maximum,0,1);return VGroup(Line([-3,y,0],[3,y,0],stroke_color=MUTED,stroke_opacity=.4),Dot([-3+6*q,y,0],radius=.045,color=YELLOW),tx(f't = {tau:.2f}',4.2,y,22,c=YELLOW,w=2.7))
def rod(fn,xr=(-np.pi,np.pi),y=1.55):
 vals=fn(np.linspace(*xr,60));g=VGroup()
 for j,v in enumerate(vals):g.add(Rectangle(width=10/60+.006,height=.35,stroke_width=0,fill_opacity=1,fill_color=interpolate_color(ManimColor(BLUE),ManimColor(ORANGE),np.clip(v/100,0,1))).move_to([-5+10*(j+.5)/60,y,0]))
 return g
def section(t):
 return '매끄러움 · 해의 규칙성' if t<80 else '최댓값 원리 · 범위와 유일성' if t<139 else '하르나크 · 공간과 시간의 관계' if t<208 else '세 가지 성질, 하나의 해' if t<234 else '열의 확산을 확률로 바라보다'
class PropertiesScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def init_scene(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.header=VGroup()
  rng=np.random.default_rng(20261123);n=150;steps=70
  first=rng.normal(0,np.sqrt(2*KAPPA*.2),(n,1));self.walks=np.concatenate([first,first+np.cumsum(rng.normal(0,np.sqrt(2*KAPPA*1.4/steps),(n,steps)),axis=1)],axis=1)
 def construct(self):
  self.init_scene();self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#192031',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[9,14,21,24,29,40,45,50,60,64,66,68,69,70,72,82,86,90,96,102,108,112,118,123,130,135,142,147,157,165,170,174,178,182,185,190,195,200,204,208,215,219,225,230,237,242,246,249,252]
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[t for t in extra if self.start<t<self.end]))
  for a,b in zip(events,events[1:]):self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  self.remove(self.caption,self.static,self.header);line=next(x for x in self.lines if x['start']<=t<x['end'])
  self.caption=VGroup(*[tx(s,size=25,w=30) for s in textwrap.wrap(line['text'],width=49,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.09)
  if self.caption.width>12:self.caption.scale_to_fit_width(12)
  if self.caption.height>.82:self.caption.scale_to_fit_height(.82)
  self.caption.move_to([0,-3.27,0]).set_z_index(51);self.static=self.labels(t)
  self.header=VGroup(tx('CHAPTER 03  /  HEAT EQUATION',-4.25,3.69,16,c=MUTED,w=5.4),tx(section(t),4.1,3.69,19,c=INK,w=5.6),Line([-6.4,3.45,0],[6.4,3.45,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(self.caption,self.static,self.header)
  for kind,g in [('caption',self.caption),('label',self.static),('header',self.header),('geometry',self.geometry(t))]:
   if not len(g):continue
   d=dict(kind=kind,time=t,left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1]));self.audit.append(d)
   assert d['left']>=-6.9 and d['right']<=6.9 and d['top']<=3.88,(self.index,d)
   assert d['bottom']>=(-3.8 if kind=='caption' else -2.65),(self.index,d)
   if kind=='label':assert d['top']<3.35,(self.index,d)
 def labels(self,t):
  i=self.index;g=VGroup(tx(self.rec['title'],0,2.98,29,c=YELLOW))
  if i==1:
   if t<9:g.add(eq(r'u_0=\sin x+0.5\sin3x+0.25\sin5x',0,2.05,34))
   else:g.add(tx('계산한 해에는 어떤 규칙이 있을까?',0,-2.3,25,c=GREEN))
  elif i==2:g.add(tx('불연속 경계와 뾰족한 봉우리',0,2.05,25,c=INK),tx('균질한 열방정식 · 주기적 경계조건 · κ = 0.4',0,-2.4,21,c=MUTED))
  elif i==3:
   g.add(eq(r'e^{-\kappa n^2t}',0,2.05,40,c=YELLOW))
   for j,n in enumerate([1,5,15]):g.add(tx(f'n = {n}',-5.6,1.1-j*1.0,22,c=[BLUE,GREEN,ORANGE][j],w=1.9))
   g.add(tx('동일한 초기값의 성분 · 각 행은 별도 고정 배율',0,-2.4,22,c=MUTED))
  elif i==4:g.add(tx('t = 0 · 불연속 초기값',0,2.05,26,c=INK),tx('완만해지는 것보다 강한 결론이 있다',0,-2.3,27,c=PURPLE))
  elif i==5:
   g.add(eq(r'u(\cdot,t)\in C^\infty\qquad(t>0)',0,2.1,40,c=PURPLE))
   if t<68:g.add(tx('t = 0  →  t = 0.05',0,-1.9,26,c=YELLOW))
   else:
    for j,s in enumerate([r'u_x',r'u_{xx}',r'u_{xxx}']):
     if t>=68+j:g.add(eq(s,-5.6,1.1-j*1.0,28,c=PURPLE,w=1.8))
   g.add(tx('유계 초기값 · 상수 κ > 0 · 미분 곡선은 각각 고정 배율',0,-2.4,20,c=MUTED))
  elif i==6:g.add(tx('초기값 t = 0',-3.4,1.9,25,c=INK,w=5),tx('양의 시간 t = 0.2',3.4,1.9,25,c=BLUE,w=5),eq(r'|n|^m e^{-\kappa n^2t}\longrightarrow0\quad(|n|\to\infty,\;t>0)',0,-2.25,30,c=PURPLE))
  elif i==7:
   g.add(tx('100°C를 넘는 새 최고 온도?',0,2.05,28,c=RED),tx('열원 없음 · 주기적 경계조건',0,-2.4,22,c=MUTED))
  elif i==8:g.add(eq(r'u_{xx}\leq0\quad\Rightarrow\quad u_t\leq0',0,2.05,38,c=RED),tx('국소 최고점 · 열이 양옆으로 빠져나간다',0,-2.35,25,c=ORANGE))
  elif i==9:g.add(eq(r'u_{xx}\geq0\quad\Rightarrow\quad u_t\geq0',0,2.05,38,c=GREEN),tx('국소 최저점 · 주변에서 열이 들어온다',0,-2.35,24,c=GREEN))
  elif i==10:g.add(eq(r'\min u_0\leq u(x,t)\leq\max u_0',0,2.05,38,c=GREEN),tx('열원 없음 · 주기적 경계조건 · 초기 범위 [0, 100]',0,-2.4,21,c=MUTED))
  elif i==11:
   if t<135:g.add(eq(r'u_0\leq v_0\quad\Rightarrow\quad u\leq v',0,2.05,36,c=GREEN),tx('비교 예시: v₀ = u₀ + 10',0,-2.4,22,c=MUTED))
   else:g.add(eq(r'w=u-v,\quad w_0=0\quad\Rightarrow\quad w=0',0,2.05,35,c=PURPLE),tx('유일성 설정: 같은 초기값·경계조건 → 같은 해',0,-2.4,23,c=PURPLE))
  elif i==12:g.add(tx('다른 위치, 다른 시각의 값도 비교할 수 있을까?',0,2.05,27,c=PURPLE),tx('전체 범위에서 두 지점의 관계로',0,-2.35,24,c=MUTED))
  elif i==13:g.add(eq(r'K(x,t)=\frac{e^{-x^2/(4\kappa t)}}{\sqrt{4\pi\kappa t}}',0,2.05,37,c=BLUE),tx('전체 실수선의 1차원 양의 열핵 예시 · u > 0',0,-2.4,21,c=MUTED))
  elif i==14:
   g.add(tx('A: 이른 시각 t₁ = 0.6',-3.3,2.05,24,c=BLUE,w=5.5),tx('B: 더 늦은 시각 t₂',3.3,2.05,24,c=PURPLE,w=5.5),tx('0 < t₁ < t₂ · 위치와 시간을 함께 비교',0,-2.4,23,c=MUTED))
  elif i==15:
   g.add(eq(r'u(B,t_2)\geq\frac{u(A,t_1)}{C}',0,2.05,39,c=PURPLE),tx('A의 실제 값',-3,1.35,23,c=BLUE,w=3),tx('B의 비교용 시험값',3,1.35,23,c=PURPLE,w=4),tx('시험값 막대는 실제 해의 시간 변화가 아님',0,-2.4,21,c=MUTED))
  elif i==16:g.add(tx('거리와 시간 간격에 따라 달라지는 제한',0,2.05,27,c=PURPLE),tx('전체 실수선의 양의 열핵 · x = 0, t₁ = 0.6',0,-2.4,21,c=MUTED))
  elif i==17:
   if t<204:g.add(eq(r'u(x,t_1)\leq u(y,t_2)\sqrt{\frac{t_2}{t_1}}\exp\!\left(\frac{|x-y|^2}{4\kappa(t_2-t_1)}\right)',0,2.05,33,c=PURPLE))
   else:g.add(tx('서로 다른 위치와 시간의 값에도 제약이 있다',0,2.05,27,c=PURPLE))
   g.add(eq(r'u(B,1.6)\geq u(A,0.6)/C=0.143',0,-1.75,31,c=PURPLE),tx('전체 실수선 · n = 1 · 양의 해 · 0 < t₁ < t₂',0,-2.4,21,c=MUTED))
  elif i in [18,19,20]:
   text={18:'매끄러움 — 해의 규칙성',19:'최댓값 원리 — 초기 범위 보존',20:'하르나크 — 공간·시간 값의 제약'}[i]
   g.add(tx(text,0,2.05,28,c={18:BLUE,19:GREEN,20:PURPLE}[i]))
   g.add(tx('주기적 열방정식의 실제 해' if i!=20 else '전체 실수선의 양의 해 예시',0,-2.4,22,c=MUTED))
  elif i==21:
   for x,s,c in [(-4.3,'매끄러움',BLUE),(0,'범위 보존',GREEN),(4.3,'시공간 비교',PURPLE)]:g.add(tx(s,x,2.05,23,c=c,w=3.5))
   g.add(tx('해의 변화에는 수학적 규칙이 존재한다',0,-2.35,27,c=INK))
  elif i==22:g.add(tx('열방정식 → 시간에 따른 분포',0,2.05,28,c=BLUE),tx('열핵을 이용한 확산 분포 · 정규화된 예시',0,-2.4,21,c=MUTED))
  elif i==23:g.add(tx('연속적인 분포 → 무작위 입자의 위치 분포',0,2.05,27,c=GREEN),tx('입자가 열에서 생겨난다는 뜻이 아닌, 표현 관점의 전환',0,-2.4,21,c=MUTED))
  elif i==24:g.add(tx('BROWNIAN MOTION',0,2.0,30,c=GREEN),tx('FEYNMAN–KAC FORMULA',0,1.32,27,c=PURPLE),tx('무작위 운동과 확산 방정식의 연결',0,-2.4,24,c=GREEN))
  return g
 def geometry(self,t):
  i=self.index;p=prog(t,self.start,self.end);g=VGroup()
  if i==1:
   tau=2.8*min(p*2,1)
   fn=lambda x:np.sin(x)*np.exp(-.12*tau)+.5*np.sin(3*x)*np.exp(-1.08*tau)+.25*np.sin(5*x)*np.exp(-3*tau)
   if t<9:
    for n,a,c in [(1,1,BLUE),(3,.5,GREEN),(5,.25,ORANGE)]:g.add(chart(lambda x:a*np.sin(n*x)*np.exp(-.12*n*n*tau),c,cy=.0,scale=.9,opacity=.35))
   g.add(chart(fn,BLUE,cy=.0,scale=.9))
   if t>=9:
    x=-np.pi+2*np.pi*prog(t,9,18);g.add(marker(x,float(fn(x)),YELLOW,cy=0,scale=.9))
  elif i==2:
   tau=0 if t<29 else .6*prog(t,29,36)
   g.add(initial_plot() if tau==0 else chart(lambda x:temperature(x,tau)),timeline(tau,1))
   if 24<=t<29:
    for x,y in [(-1.6,50),(-.5,50),(1.2,85)]:g.add(Circle(radius=.12,stroke_color=RED).move_to(coordinate(x,y)))
  elif i==3:
   tau=.5*prog(t,45,56)
   for j,n in enumerate([1,5,15]):
    a,b=mode_coeff(n);norm=max(1,np.hypot(a,b));g.add(chart(lambda x:mode(x,n,tau)/norm,[BLUE,GREEN,ORANGE][j],cx=.4,cy=1.1-j,scale=.4,w=8.7))
   if t>=50:
    # Small exact recombined profile; modes shown above are selected examples.
    g.add(chart(lambda x:(temperature(x,tau)-mode_coeff(0)[0])/100,INK,cy=-1.65,scale=.35,axis=False))
  elif i==4:
   g.add(initial_plot())
   for x in [-1.6,-.5]:g.add(Circle(radius=.14,stroke_color=RED,stroke_width=3).move_to(coordinate(x,50)))
  elif i==5:
   if t<68:
    tau=.05*prog(t,64,66);g.add(initial_plot() if tau==0 else chart(lambda x:temperature(x,tau)))
   else:
    for j,d in enumerate([1,2,3]):
     if t>=68+j:
      ref=max(abs(temperature(GRID,.05,d)));g.add(chart(lambda x:temperature(x,.05,d)/ref,PURPLE,cx=.4,cy=1.1-j,scale=.37,w=8.5))
  elif i==6:
   g.add(initial_plot(cx=-3.4,cy=-1.15,w=5.3,scale=.022),chart(lambda x:temperature(x,.2),BLUE,cx=3.4,cy=-1.15,w=5.3,scale=.022),arr([-.55,.0,0],[.55,.0,0],PURPLE))
  elif i==7:
   tau=.02+.15*p;g.add(chart(lambda x:temperature(x,tau)),limits(),timeline(tau,1))
   y=float(temperature(-1.05,tau));g.add(marker(-1.05,y,RED))
  elif i==8:
   tau=.08+.65*p;xr=(-1.9,-.2);z=np.linspace(*xr,241);v=temperature(z,tau);j=int(np.argmax(v));x=z[j];pt=coordinate(x,v[j],xr=xr)
   g.add(chart(lambda x:temperature(x,tau),BLUE,xr=xr),Dot(pt,radius=.06,color=RED),arr(pt+[-.1,.4,0],pt+[-1.3,.4,0],ORANGE),arr(pt+[.1,.4,0],pt+[1.3,.4,0],ORANGE),timeline(tau,1))
  elif i==9:
   tau=.4+.6*p;xr=(2.15,4.25);z=np.linspace(*xr,241);v=temperature(z,tau);j=int(np.argmin(v));pt=coordinate(z[j],v[j],xr=xr,scale=.04)
   g.add(chart(lambda x:temperature(x,tau),BLUE,xr=xr,scale=.04),Dot(pt,radius=.06,color=GREEN),arr(pt+[-1.4,.5,0],pt+[-.1,.5,0],GREEN),arr(pt+[1.4,.5,0],pt+[.1,.5,0],GREEN),tx('주기적 구간을 연장한 골짜기 확대',0,-1.95,22,c=MUTED))
  elif i==10:
   tau=.05+2.8*p;g.add(initial_plot(opacity=.2),chart(lambda x:temperature(x,tau)),limits(),timeline(tau,3))
  elif i==11:
   tau=.1+.8*p;u=lambda x:temperature(x,tau)
   if t<135:
    g.add(chart(u,BLUE,cy=-.1,scale=.017),chart(lambda x:u(x)+10,GREEN,cy=-.1,scale=.017),chart(lambda x:np.full_like(x,-10),PURPLE,cy=-1.55,scale=.025),tx('w = u − v = −10',4.7,-1.7,21,c=PURPLE,w=3.5))
   else:
    g.add(chart(u,BLUE,cy=-.1,scale=.017),chart(u,GREEN,cy=-.1,scale=.017,dashed=True),chart(lambda x:np.zeros_like(x),PURPLE,cy=-1.55,scale=.025),tx('w ≤ 0 그리고 −w ≤ 0',0,-1.9,23,c=PURPLE))
  elif i==12:
   tau=.7+.4*p;g.add(chart(lambda x:temperature(x,tau)))
   if t<147:g.add(limits())
   else:
    for x,c,s in [(-1.05,BLUE,'A'),(1.2,PURPLE,'B')]:
     y=float(temperature(x,tau));pt=coordinate(x,y);g.add(marker(x,y,c),tx(s,pt[0],pt[1]+.3,24,c=c,w=1))
  elif i==13:
   tau=.2+1.1*prog(t,157,161);xr=(-3,3);g.add(chart(lambda x:kernel(x,tau),BLUE,scale=2.6,xr=xr))
   for x,c,s in [(0,BLUE,'A'),(1.2,PURPLE,'B')]:
    y=float(kernel(x,tau));pt=coordinate(x,y,scale=2.6,xr=xr);g.add(marker(x,y,c,scale=2.6,xr=xr),tx(s,pt[0],pt[1]+.3,23,c=c,w=1))
   g.add(timeline(tau,2))
  elif i in [14,20]:
   t1=.6;t2=.8+.8*p if i==14 else 1.6;xr=(-3,3)
   g.add(chart(lambda x:kernel(x,t1),BLUE,scale=3,xr=xr,opacity=.5),chart(lambda x:kernel(x,t2),PURPLE,scale=3,xr=xr),marker(0,float(kernel(0,t1)),BLUE,scale=3,xr=xr),marker(1.2,float(kernel(1.2,t2)),PURPLE,scale=3,xr=xr),timeline(t2,2))
   a=coordinate(0,kernel(0,t1),scale=3,xr=xr);b=coordinate(1.2,kernel(1.2,t2),scale=3,xr=xr);g.add(DashedLine(a,b,color=PURPLE,stroke_opacity=.6))
  elif i==15:
   d=harnack(0,1.2,.6,1.6);test=max(d['lower'],.36-(.36-d['lower'])*prog(t,178,182));cy=-1.1;scale=3.5
   for x,v,c in [(-3,d['A'],BLUE),(3,test,PURPLE)]:g.add(Rectangle(width=1.1,height=scale*v,stroke_color=c,fill_color=c,fill_opacity=.35).move_to([x,cy+scale*v/2,0]))
   g.add(Line([1.6,cy+scale*d['lower'],0],[4.4,cy+scale*d['lower'],0],stroke_color=RED,stroke_width=3),tx('허용 하한 0.143',5.1,-.85,20,c=RED,w=3),tx(f"A = {d['A']:.3f}   C = {d['C']:.3f}   실제 B = {d['B']:.3f}",0,-1.9,24,c=MUTED))
  elif i==16:
   y=.6+1.2*prog(t,185,190);t2=1.6+.8*prog(t,190,195);d=harnack(0,y,.6,t2);xr=(-3,3)
   g.add(chart(lambda x:kernel(x,.6),BLUE,scale=3,xr=xr,opacity=.3),chart(lambda x:kernel(x,t2),PURPLE,scale=3,xr=xr),marker(y,d['B'],PURPLE,scale=3,xr=xr),marker(0,d['A'],BLUE,scale=3,xr=xr),tx(f'거리 = {y:.2f}    시간 간격 = {t2-.6:.2f}    하한 = {d["lower"]:.3f}',0,-1.9,24,c=PURPLE))
  elif i==17:
   d=harnack(0,1.2,.6,1.6);xr=(-3,3)
   for cx,tau,x,c in [(-3.4,.6,0,BLUE),(3.4,1.6,1.2,PURPLE)]:g.add(chart(lambda x:kernel(x,tau),c,cx=cx,cy=-.9,w=5.1,scale=3,xr=xr),marker(x,float(kernel(x,tau)),c,cx=cx,cy=-.9,w=5.1,scale=3,xr=xr),tx(f't = {tau:.1f}',cx,1.35,24,c=c,w=4))
   g.add(arr([-.5,-.2,0],[.5,-.2,0],PURPLE))
  elif i in [18,19]:
   tau=.6*p if i==18 else .6+.4*p;g.add(initial_plot(opacity=.15),initial_plot(c=BLUE) if tau==0 else chart(lambda x:temperature(x,tau)),timeline(tau,2))
   if i==19:g.add(limits())
  elif i==21:
   tau=.5+1.4*p;g.add(chart(lambda x:temperature(x,.3),INK,opacity=.2),chart(lambda x:temperature(x,tau)),limits(),timeline(tau,2))
   for x,c in [(-1.05,BLUE),(1.2,PURPLE)]:g.add(marker(x,float(temperature(x,tau)),c))
  elif i==22:
   tau=.3+1*p;xr=(-4,4);g.add(chart(lambda x:kernel(x,tau),BLUE,cy=-1.1,scale=2.7,xr=xr),rod(lambda x:100*kernel(x,tau),xr=xr,y=1.35),timeline(tau,2))
  elif i in [23,24]:
   q=prog(t,242,255);u=q*70;k=min(69,int(u));a=u-k;pos=(1-a)*self.walks[:,k]+a*self.walks[:,k+1];tau=.2+1.4*q;xr=(-4.5,4.5)
   for j,x in enumerate(pos):g.add(Dot([10*x/9,-1.5+.48*(j%6)/5,0],radius=.025,color=GREEN))
   g.add(chart(lambda x:kernel(x,tau),BLUE if i==23 else GREEN,cy=-.75,scale=2.0,xr=xr,opacity=.35 if i==23 and t<246 else 1,dashed=i==23))
   if i==24:
    edges=np.linspace(-4.5,4.5,25);heights,_=np.histogram(pos,bins=edges,density=True)
    for j,v in enumerate(heights):g.add(Rectangle(width=10/24-.012,height=max(.004,2*v),stroke_width=0,fill_color=GREEN,fill_opacity=.2).move_to([-5+10*(j+.5)/24,-.75+v,0]))
  return g
