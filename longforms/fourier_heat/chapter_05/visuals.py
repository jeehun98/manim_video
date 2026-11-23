"""Heat on fixed manifolds, operator index, evolving metrics, final synthesis."""
import importlib.util,json,textwrap,sys
from pathlib import Path
import numpy as np
from manim import *
from mechanics import sphere_kernel,plane_kernel,radius,paired_traces
R=Path(__file__).resolve().parent
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
common=load('heat5_common',R.parent/'chapter_01/visuals.py')
tx=common.tx;eq=common.eq;path=common.path;arr=common.arr
BG='#10131C';INK='#F1F4FA';MUTED='#8E9BB0';GRID='#8EA4C2';BLUE='#4A9EFF';GREEN='#36C7A3';ORANGE='#F0A45D';PURPLE='#B69AFF';GOLD='#E9C46A';YELLOW='#F3CE77'
config.frame_width=128/9;config.frame_height=8;config.background_color=BG;config.tex_dir=str(R.parents[2]/'media/Tex')
REUSE={};BASE={}
def prior(ch):
 if ch not in REUSE:
  old=sys.modules.get('mechanics');sys.modules['mechanics']=load(f'heat{ch}_mechanics_reuse',R.parent/f'chapter_{ch:02d}/mechanics.py')
  try:REUSE[ch]=load(f'heat{ch}_visuals_reuse',R.parent/f'chapter_{ch:02d}/visuals.py')
  finally:
   if old is None:sys.modules.pop('mechanics',None)
   else:sys.modules['mechanics']=old
  config.background_color=BG
 return REUSE[ch]
def reuse(ch,index,q):
 key=(ch,index)
 if key not in BASE:
  m=prior(ch);cls={2:'FourierScene',3:'PropertiesScene',4:'ProbabilityScene'}[ch];s=getattr(m,cls)();s.index=index;s.init_scene();BASE[key]=s
 s=BASE[key];return s.geometry(s.start+np.clip(q,0,.99999)*(s.end-s.start))
def prog(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def projection(p):
 a=np.asarray(p);x,y,z=a[...,0],a[...,1],a[...,2]
 return np.stack([.91*x-.42*y,.24*x+.52*y+.82*z,np.zeros_like(x)],axis=-1)
def sph(theta,phi):return np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
def heatcolor(v):
 # Fixed monotone color transfer; never renormalize each frame's maximum.
 v=max(0,float(v));return interpolate_color(ManimColor('#233752'),ManimColor(ORANGE),v/(v+.13))
def sphere(t=.2,cx=0,cy=.1,s=1.65,warm=True,deform=0,ricci=None):
 # The surface is fixed during scalar diffusion; optional deformation is topology only.
 g=VGroup();rr=1 if ricci is None else float(radius(ricci))
 def xyz(th,ph):
  a=sph(th,ph);return a*np.array([1+.32*deform,1-.14*deform,1-.16*deform])*rr
 def pt(th,ph):return s*projection(xyz(th,ph))+[cx,cy,0]
 for th in np.linspace(.09,np.pi-.09,18):
  v=float(sphere_kernel(th,t));g.add(path([pt(th,ph) for ph in np.linspace(0,2*np.pi,65)],heatcolor(v) if warm else BLUE,3.2 if warm else 1.4,.85))
 for ph in np.linspace(0,2*np.pi,14,endpoint=False):g.add(path([pt(th,ph) for th in np.linspace(0,np.pi,49)],GRID if warm else PURPLE,1,.32))
 return g
def plane(t=.2,cx=0,cy=.1,s=1):
 g=VGroup()
 for a in np.linspace(-2.3,2.3,13):
  for axis in [0,1]:
   pts=np.array([[v,a,0] if axis==0 else [a,v,0] for v in np.linspace(-2.5,2.5,35)])
   g.add(path(s*projection(pts)+[cx,cy,0],GRID,1,.38))
 for r in np.linspace(.05,2.4,24):
  g.add(path([s*projection([r*np.cos(ph),r*np.sin(ph),.01])+[cx,cy,0] for ph in np.linspace(0,2*np.pi,65)],heatcolor(float(plane_kernel(r,t))),3.2,.9))
 return g
def torus(cx=0,cy=.1,s=1,deform=0):
 g=VGroup()
 def pt(a,b):
  rr=1.45+.56*np.cos(b);p=np.array([rr*np.cos(a)*(1+.18*deform),rr*np.sin(a)*(1-.12*deform),.56*np.sin(b)+.13*deform*np.sin(2*a)])
  return s*projection(p)+[cx,cy,0]
 for b in np.linspace(0,2*np.pi,12,endpoint=False):g.add(path([pt(a,b) for a in np.linspace(0,2*np.pi,70)],GREEN,1.5,.8))
 for a in np.linspace(0,2*np.pi,22,endpoint=False):g.add(path([pt(a,b) for b in np.linspace(0,2*np.pi,35)],GRID,1,.45))
 return g
def morph(q):
 # Visual transition of a parameter patch; not a heat evolution or a homeomorphism.
 g=VGroup()
 def pt(u,v):
  a=np.array([2*u,2*v,0]);b=sph((v+1)*np.pi/2,(u+1)*np.pi);return 1.65*projection((1-q)*a+q*b)+[0,.1,0]
 for v in np.linspace(-.94,.94,15):g.add(path([pt(u,v) for u in np.linspace(-1,1,65)],GRID,1.5,.7))
 for u in np.linspace(-1,1,17):g.add(path([pt(u,v) for v in np.linspace(-1,1,65)],BLUE,1.2,.6))
 return g
def curves(t,cx=3.1,cy=-1.3,w=5,h=2.1):
 theta=np.linspace(0,np.pi,130);k=sphere_kernel(theta,t)
 return VGroup(Line([cx-w/2,cy,0],[cx+w/2,cy,0],stroke_color=MUTED,stroke_opacity=.4),path(np.column_stack([cx-w/2+w*theta/np.pi,cy+h*k,np.zeros(len(theta))]),ORANGE,3))
def neck(q,cx=-2.7):
 g=VGroup()
 def pt(z,a):
  rr=.82-.58*q*np.exp(-z*z/.28);return projection([z,rr*np.cos(a),rr*np.sin(a)])+[cx,.0,0]
 for z in np.linspace(-1.8,1.8,19):g.add(path([pt(z,a) for a in np.linspace(0,2*np.pi,40)],PURPLE,1.4,.8))
 for a in np.linspace(0,2*np.pi,12,endpoint=False):g.add(path([pt(z,a) for z in np.linspace(-1.8,1.8,65)],GOLD,1.2,.6))
 return g
def nodes(q):
 g=VGroup();locations=[(-4.5,1.4),(-4.5,-1.15),(0,-1.65),(4.5,-1.15),(4.5,1.4)];labels=['열전도','푸리에 해석','해의 성질','확률과 금융','기하학과 위상'];colors=[ORANGE,BLUE,PURPLE,GOLD,GREEN]
 for (x,y),label,c in zip(locations,labels,colors):
  g.add(Line([0,.25,0],[x,y,0],stroke_color=c,stroke_opacity=.2+.5*q,stroke_width=1.5),RoundedRectangle(width=2.75,height=1.0,corner_radius=.15,stroke_color=c,fill_color=BG,fill_opacity=1).move_to([x,y,0]),tx(label,x,y,25,c=c,w=2.5))
 g.add(RoundedRectangle(width=4.15,height=1.12,corner_radius=.15,stroke_color=INK,fill_color=BG,fill_opacity=1).move_to([0,.25,0]),eq(r'\partial_tu=\kappa\Delta u',0,.25,33,w=3.8));return g
def section(t):return '평면에서 곡면으로' if t<58 else '열핵에서 기하학의 정보로' if t<89 else '기하학과 위상수학의 연결' if t<139 else '온도의 변화에서 계량의 변화로' if t<193 else '하나의 방정식에서 이어진 수학'
class GeometryScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def init_scene(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.header=VGroup()
 def construct(self):
  self.init_scene();self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#192031',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[8,12,19,24,29,35,41,47,53,58,64,67,72,76,80,85,89,94,99,105,111,116,120,126,130,133,139,144,150,154,162,168,173,179,185,193,199,206,215,219,224,230,233,235,237,241,245,251,257,261,264,267,274,280]
  events=sorted(set([self.start,self.end]+[l['start'] for l in self.lines if self.start<l['start']<self.end]+[z for z in extra if self.start<z<self.end]))
  for a,b in zip(events,events[1:]):self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters();(R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  self.remove(self.caption,self.static,self.header);line=next(l for l in self.lines if l['start']<=t<l['end'])
  self.caption=VGroup(*[tx(s,size=25,w=30) for s in textwrap.wrap(line['text'],width=49,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.09)
  if self.caption.width>12:self.caption.scale_to_fit_width(12)
  if self.caption.height>.82:self.caption.scale_to_fit_height(.82)
  self.caption.move_to([0,-3.27,0]).set_z_index(51);self.static=self.labels(t)
  self.header=VGroup(tx('CHAPTER 05  /  GEOMETRY',-4.25,3.69,16,c=MUTED,w=5.4),tx(section(t),4.1,3.69,19,c=INK,w=5.6),Line([-6.4,3.45,0],[6.4,3.45,0],stroke_color=MUTED,stroke_opacity=.25));self.add(self.caption,self.static,self.header)
  for kind,g in [('caption',self.caption),('label',self.static),('header',self.header),('geometry',self.geometry(t))]:
   if not len(g):continue
   d=dict(kind=kind,time=t,left=float(g.get_left()[0]),right=float(g.get_right()[0]),bottom=float(g.get_bottom()[1]),top=float(g.get_top()[1]));self.audit.append(d)
   assert d['left']>=-6.9 and d['right']<=6.9 and d['top']<=3.88,(self.index,d)
   assert d['bottom']>=(-3.8 if kind=='caption' else -2.65),(self.index,d)
   if kind=='label':assert d['top']<3.35,(self.index,d)
 def labels(self,t):
  i=self.index;g=VGroup(tx(self.rec['title'],0,2.98,29,c=YELLOW))
  if i==1:g.add(eq(r'\partial_tu=\kappa\Delta u',0,2.05,38),tx('변화하는 양에서, 그 변화가 일어나는 공간으로',0,-2.4,25,c=PURPLE))
  elif i==2:g.add(tx('평면의 열핵 · κ = 1' if t<24 else '평면 → 구면 · 공간을 바꾸는 개념 전환',0,2.05,26,c=ORANGE),tx('색은 온도 · 이후 구면 확산은 별도로 계산',0,-2.4,22,c=MUTED))
  elif i==3:
   g.add(tx('평면',-3.3,2.05,26,c=GRID,w=4),tx('구면',3.3,2.05,26,c=BLUE,w=4),tx('공간 속 직선거리와 표면을 따른 거리는 다르다' if t>=35 else '같은 확산 법칙, 서로 다른 바탕 공간',0,-2.4,24,c=PURPLE))
  elif i==4:
   g.add(eq(r'ds^2=dx^2+dy^2',-3.3,1.95,30,w=5.5),eq(r'ds^2=d\theta^2+\sin^2\!\theta\,d\phi^2',3.3,1.95,30,c=BLUE,w=5.7),eq(r'\Delta\quad\longrightarrow\quad\Delta_g',0,-1.8,38,c=PURPLE))
   if t>=47:g.add(tx('라플라스–벨트라미 작용소',0,-2.4,24,c=PURPLE))
  elif i==5:g.add(eq(r'\partial_tu=\kappa\Delta_gu',0,2.05,42,c=ORANGE),tx('고정된 단위 구면 · κ = 1 · 구면 열핵의 스펙트럼 계산',0,-2.4,21,c=MUTED))
  elif i==6:g.add(tx('공간 → 열의 퍼짐' if t<64 else '열의 퍼짐 → 공간의 정보',0,2.05,30,c=PURPLE),tx('열핵은 기하학적 정보를 담는다 · 모든 모양을 유일하게 복원한다는 뜻은 아님',0,-2.4,19,c=MUTED))
  elif i==7:g.add(eq(r'K(t,x,y)',0,2.05,43,c=PURPLE),tx('출발 y',-4.8,1.3,23,c=ORANGE,w=2),tx('관찰 x',-1.8,-1.5,23,c=PURPLE,w=2),tx('단위 구면 · y는 북극 · θ는 y로부터의 구면 거리',0,-2.4,21,c=MUTED))
  elif i==8:
   g.add(eq(r'K(t,x,x)\sim(4\pi t)^{-n/2}\!\left(1+\frac{\mathrm{Scal}(x)}6t+\cdots\right)',0,1.9,34,c=PURPLE),tx('차원 n',-3.5,-1.95,27,c=BLUE,w=4),tx('스칼라 곡률 Scal',3.5,-1.95,27,c=PURPLE,w=5),tx('경계 없는 매끄러운 공간 · κ=1 · t → 0⁺의 점근식',0,-2.45,20,c=MUTED))
  elif i in [9,10]:
   g.add(tx('구면 S²',-3.25,2.05,27,c=BLUE,w=5),tx('도넛 표면 T²',3.25,2.05,27,c=GREEN,w=5),tx('길이·각도·곡률은 변한다' if t<99 else '찢거나 붙이지 않는 변형에서 위상은 유지된다',0,-2.4,23,c=PURPLE))
  elif i==11:
   g.add(eq(r'\mathrm{ind}(D)=\dim\ker D-\dim\ker D^*',0,1.9,35,c=PURPLE),tx('미분 작용소의 해 공간',-3.5,.65,26,c=BLUE,w=5.5),tx('기하학·위상적 특성',3.5,.65,26,c=GREEN,w=5.5),tx('적절한 타원형 작용소 · 닫힌 다양체의 경우',0,-2.4,22,c=MUTED))
  elif i==12:
   g.add(eq(r'\mathrm{ind}(D)=\mathrm{Tr}(e^{-tD^*D})-\mathrm{Tr}(e^{-tDD^*})',0,2.0,34,c=PURPLE),tx('대응하는 양의 고유값 성분들은 상쇄된다',0,-1.95,25,c=GREEN),tx('작용소의 열 흔적 차이 · 일반적인 온도 그림으로 구멍을 세는 과정과 구별',0,-2.45,19,c=MUTED))
  elif i==13:g.add(tx('고정된 계량 g · 온도 u의 변화' if t<144 else '온도 분포를 걷어내고 계량 g에 주목한다',0,2.05,28,c=ORANGE if t<144 else PURPLE),tx('색의 변화와 공간의 거리 구조 변화를 구별한다',0,-2.4,24,c=MUTED))
  elif i==14:g.add(tx('열방정식 · u(t)',-3.3,2.05,27,c=ORANGE,w=5.5),tx('리치 흐름 · g(t)',3.3,2.05,27,c=PURPLE,w=5.5),tx('오른쪽: 2차원 구면의 정확한 예 · g(t)=(1−2t)g₀',0,-2.4,22,c=MUTED))
  elif i==15:g.add(eq(r'\partial_tu=\kappa\Delta_gu',-3.3,1.8,35,c=ORANGE,w=5.7),eq(r'\partial_tg=-2\operatorname{Ric}(g)',3.3,1.8,35,c=PURPLE,w=5.7),tx('함수의 변화',-3.3,-1.9,25,c=ORANGE,w=5),tx('계량의 변화',3.3,-1.9,25,c=PURPLE,w=5),tx('리치 흐름은 좌표 자유도를 조정하면 엄밀한 포물형 구조가 드러난다',0,-2.45,20,c=MUTED))
  elif i==16:g.add(tx('특이점: 곡률이 집중될 수 있다',-2.8,2.05,25,c=PURPLE,w=6),tx('2차원 표면은 시각적 비유 · 푸앵카레 추측의 대상은 3차원 공간',0,-2.4,20,c=MUTED))
  elif i==17:
   for x,a,b,c in [(-4.3,'곡면 위 확산','온도 u(t)',ORANGE),(0,'열핵','공간의 정보',BLUE),(4.3,'리치 흐름','계량 g(t)',PURPLE)]:g.add(tx(a,x,2.05,26,c=c,w=3.8),tx(b,x,-1.85,24,c=c,w=3.8))
   g.add(tx('열의 확산을 연구하는 수학에서 공간의 기하학을 연구하는 수학으로',0,-2.45,22,c=INK))
  elif i==18:
   g.add(tx('에너지 보존  +  푸리에의 열전도 법칙',0,2.05,27,c=ORANGE),eq(r'\partial_tu=\kappa\Delta u',0,-1.85,43),tx('1장 · 열의 이동에서 출발',0,-2.45,21,c=MUTED))
  elif i==19:g.add(eq(r'f(x)=\sin x+\tfrac12\sin3x+\tfrac14\sin5x',0,2.05,35),tx('2장 · 같은 주기적 함수와 같은 세 진동 성분',0,-2.4,22,c=MUTED))
  elif i==20:
   g.add(eq(r'\langle\sin mx,\sin nx\rangle=0\;(m\ne n)' if t<219 else r'\partial_{xx}\sin(kx)=-k^2\sin(kx)',0,2.05,37,c=PURPLE if t<219 else GOLD),tx('직교성 · 성분을 구별한다' if t<219 else '고유함수 · 미분을 상수배로 바꾼다',0,-2.4,25,c=PURPLE))
  elif i==21:g.add(eq(r'u(x,t)=\sum_k a_ke^{-\kappa k^2t}\sin(kx)',0,2.05,39),tx('선형성 · 독립적으로 구한 해를 합친다',0,-2.4,25,c=GREEN))
  elif i==22:g.add(tx('매끄러움' if t<233 else '최댓값 원리' if t<235 else '하르나크 부등식',0,2.05,29,c=PURPLE),tx('3장 · 같은 초기 분포와 같은 비교 원리',0,-2.4,22,c=MUTED))
  elif i==23:g.add(eq(r'\partial_tp=\kappa\Delta p',0,2.05,41,c=BLUE),tx('4장 · 같은 브라운 경로의 위치 분포',0,-2.4,24,c=GREEN))
  elif i==24:g.add(eq(r'u(x,t)=\mathbb E_x[f(X_t)]' if t<251 else r'V=e^{-r(T-t)}\mathbb E^{\mathbb Q}[\Phi(S_T)]',0,2.05,38,c=PURPLE if t<251 else GOLD),tx('기댓값은 표본평균으로 근사 · 금융에서는 위험중립 확률과 할인',0,-2.4,21,c=MUTED))
  elif i==25:g.add(tx('곡면의 열핵 → 기하학 정보 → 작용소와 위상 → 계량의 흐름',0,2.05,25,c=PURPLE),tx('열방정식 자체와, 관련된 다른 방정식을 구별한다',0,-2.4,23,c=MUTED))
  elif i in [26,27]:g.add(tx('하나의 아이디어가 새로운 문제를 이해하는 방법이 된다' if t<280 else '다른 현상들 속에서 공통된 구조를 발견하다',0,-2.4,25,c=PURPLE))
  return g
 def geometry(self,t):
  i=self.index;p=prog(t,self.start,self.end);tau=.05+.7*p;g=VGroup()
  if i==1:
   if t<8:g=reuse(4,28,prog(t,0,8)).scale(.8).shift([0,.1,0])
   else:g=plane(.05+.2*prog(t,8,15),s=.8)
  elif i==2:g=plane(.035+.45*prog(t,15,24),s=.9) if t<24 else morph(prog(t,24,29))
  elif i==3:
   g.add(plane(tau,cx=-3.3,s=.58),sphere(tau,cx=3.3,s=1.5))
   if t>=35:
    a=sph(.45,1.2);b=sph(1.8,1.2);pts=[1.5*projection(sph(th,1.2))+[3.3,.1,0] for th in np.linspace(.45,1.8,65)];pa=1.5*projection(a)+[3.3,.1,0];pb=1.5*projection(b)+[3.3,.1,0]
    g.add(DashedLine(pa,pb,color=INK,stroke_opacity=.7),path(pts,GREEN,4),Dot(pa,color=GREEN,radius=.055),Dot(pb,color=GREEN,radius=.055))
  elif i==4:g.add(plane(.3,cx=-3.3,s=.56),sphere(.3,cx=3.3,s=1.4,warm=False))
  elif i==5:g=sphere(tau,s=1.8)
  elif i==6:g.add(plane(tau,cx=-3.3,s=.6),sphere(tau,cx=3.3,s=1.65),arr([-.7,0,0],[.7,0,0],PURPLE) if t<64 else arr([.7,0,0],[-.7,0,0],PURPLE))
  elif i==7:
   tau=.06+.65*p;g.add(sphere(tau,cx=-3.3,s=1.7),curves(tau),tx(f't = {tau:.2f}',3.2,1.15,24,c=YELLOW,w=3),tx('거리 θ',5.4,-1.65,20,c=MUTED,w=2))
   for th,c in [(0,ORANGE),(1.05,PURPLE)]:g.add(Dot(1.7*projection(sph(th,.1))+[-3.3,.1,0],radius=.07,color=c))
   th=1.05;v=float(sphere_kernel(th,tau));g.add(Dot([.6+5*th/np.pi,-1.3+2.1*v,0],radius=.06,color=PURPLE),tx(f'K(t,x,y) = {v:.3f}',3.2,-1.95,24,c=PURPLE,w=5))
  elif i==8:
   g.add(plane(.25,cx=-3.3,cy=-.1,s=.48),sphere(.25,cx=3.3,cy=-.1,s=1.2))
   g.add(tx('n = 2 · Scal = 0',-3.3,-1.35,23,c=BLUE,w=4),tx('n = 2 · Scal = 2',3.3,-1.35,23,c=PURPLE,w=4))
  elif i in [9,10]:
   q=.5+.5*np.sin(2*np.pi*p);g.add(sphere(cx=-3.25,s=1.45,warm=False,deform=q),torus(cx=3.25,s=.95,deform=q))
   if i==10:g.add(tx('손잡이 0개 · χ = 2',-3.25,-1.9,25,c=BLUE,w=5),tx('손잡이 1개 · χ = 0',3.25,-1.9,25,c=GREEN,w=5))
  elif i==11:
   g.add(sphere(cx=-3.5,cy=-.75,s=.7,warm=False),torus(cx=3.5,cy=-.75,s=.5),arr([-1.4,-.65,0],[1.4,-.65,0],PURPLE),tx('해석적 지표  =  위상적 지표',0,-1.9,28,c=GREEN))
  elif i==12:
   # A concrete de Rham supertrace on S², not the scalar heat trace alone.
   tau=.08+1.2*p;a,b,c=paired_traces(tau);heights=[.055*a,.055*b,.055*c];colors=[BLUE,PURPLE,GREEN]
   for x,v,h,c0,label in zip([-3.7,0,3.7],[a,b,c],heights,colors,['0-형식','1-형식','2-형식']):
    g.add(Rectangle(width=1.5,height=max(.01,h),stroke_color=c0,fill_color=c0,fill_opacity=.3).move_to([x,-1.2+h/2,0]),tx(label,x,-1.55,22,c=c0,w=3),tx(f'{v:.2f}',x,-1.05+h,22,c=c0,w=3))
   g.add(tx(f'S²의 예:  Tr₀ − Tr₁ + Tr₂ = {a-b+c:.0f} = χ(S²)',0,.95,25,c=GREEN),tx(f'열 시간 t = {tau:.2f}',0,.35,23,c=MUTED))
  elif i==13:g=sphere(tau,s=1.8,warm=t<144)
  elif i in [14,15]:
   rt=.32*p if i==14 else .2+.16*p;g.add(sphere(tau,cx=-3.3,s=1.55),sphere(cx=3.3,s=1.55,warm=False,ricci=rt))
   if i==14:
    r=float(radius(rt));g.add(tx('단위 반지름 고정',-3.3,-1.8,24,c=ORANGE,w=5),tx(f'반지름 R(t) = {r:.2f}',3.3,-1.8,24,c=PURPLE,w=5))
  elif i==16:
   g.add(neck(.3+.65*p),tx('리처드 해밀턴',3.2,1.2,29,c=INK,w=5),tx('리치 흐름의 발전',3.2,.65,23,c=PURPLE,w=5))
   if t>=173:g.add(tx('그리고리 페렐만',3.2,-.2,29,c=INK,w=5),tx('특이점 분석 · 푸앵카레 추측 해결',3.2,-.75,21,c=GOLD,w=5.5))
   g.add(tx('목이 가늘어지는 모습은 특이점의 개념도',-2.7,-1.7,20,c=MUTED,w=6))
  elif i==17:
   g.add(sphere(tau,cx=-4.3,s=1.05),curves(.12+.35*p,cx=0,cy=-.7,w=3.3,h=1.5),sphere(cx=4.3,s=1.05,warm=False,ricci=.32*p))
  elif i==18:g.add(common.distribution(2.5*p).scale(.85).shift([0,.1,0]))
  elif i==19:g=reuse(2,14,1-p).scale(.9)
  elif i==20:g=reuse(2,28,prog(t,215,219)) if t<219 else reuse(2,29,prog(t,219,224))
  elif i==21:g=reuse(2,30,p)
  elif i==22:g=reuse(3,18,prog(t,230,233)) if t<233 else reuse(3,19,prog(t,233,235)) if t<235 else reuse(3,20,prog(t,235,237))
  elif i==23:g=reuse(4,4,p) if t<241 else reuse(4,5,prog(t,241,245))
  elif i==24:g=reuse(4,17,prog(t,245,251)) if t<251 else reuse(4,25,prog(t,251,257))
  elif i==25:
   if t<261:g=morph(prog(t,257,259)) if t<259 else sphere(.05+.5*prog(t,259,261))
   elif t<264:g.add(sphere(.15,cx=-3.2,s=1.4),curves(.15,cx=3.1),tx('열핵의 짧은 시간 거동에 곡률 정보',0,-1.95,25,c=PURPLE))
   else:g.add(sphere(cx=-3.2,s=1.4,warm=False,ricci=.3*prog(t,264,267)),eq(r'\mathrm{ind}(D)\longleftrightarrow\text{Topology}',3.0,.0,32,c=GREEN,w=5.5))
  elif i in [26,27]:g=nodes(.2+.8*p if i==27 else p)
  return g
