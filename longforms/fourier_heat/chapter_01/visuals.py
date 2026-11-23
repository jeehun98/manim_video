"""Chapter 1: mathematical vector animation, exact user timing, 16:9."""
import json, textwrap
from pathlib import Path
import numpy as np
from manim import *
import manim.utils.tex_file_writing as _tex
# MiKTeX in this restricted workspace can finish TeX but fail writing its
# per-user diagnostic log. Accept only a complete DVI and an error-free TeX log;
# genuine TeX errors still propagate, and SVG conversion remains mandatory.
_compile_tex=_tex.compile_tex
def _workspace_compile(tex_file,tex_compiler,output_format):
 try:return _compile_tex(tex_file,tex_compiler,output_format)
 except ValueError:
  result=tex_file.with_suffix(output_format);log=tex_file.with_suffix('.log')
  contents=log.read_text(errors='replace') if log.exists() else ''
  if result.exists() and result.stat().st_size>0 and 'Output written on' in contents and '\n!' not in contents:return result
  raise
_tex.compile_tex=_workspace_compile
R=Path(__file__).resolve().parent
BG='#0B1020';INK='#EDF3FA';MUTED='#8799B6';HOT='#FF8066';COLD='#65BFFF';GOLD='#F3C77C';MINT='#66E0C2';PURPLE='#B99BFF'
config.frame_width=128/9;config.frame_height=8;config.background_color=BG
TC={};EC={}
def tx(s,x=0,y=0,size=28,c=INK,w=12.3):
 key=(s,size,c,w)
 if key not in TC:
  o=Text(s,font='Malgun Gothic',font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  TC[key]=o
 return TC[key].copy().move_to([x,y,0])
def eq(s,x=0,y=0,size=42,c=INK,w=12):
 key=(s,size,c,w)
 if key not in EC:
  o=MathTex(s,font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  EC[key]=o
 return EC[key].copy().move_to([x,y,0])
def path(points,c=GOLD,width=3,opacity=1):
 return VMobject(stroke_color=c,stroke_width=width,stroke_opacity=opacity).set_points_as_corners(np.asarray(points))
def graph(f,x0=-5.5,x1=5.5,y=-.7,scale=1,n=140,c=GOLD):
 x=np.linspace(x0,x1,n);return path([[v,y+scale*f(v),0] for v in x],c)
def arr(p,q,c=GOLD,width=3):return Arrow(p,q,buff=0,color=c,stroke_width=width,max_tip_length_to_length_ratio=.18)
def rod(vals,y=1,w=10,h=.48,x=0):
 return VGroup(*[Rectangle(width=w/len(vals)+.006,height=h,stroke_width=0,fill_opacity=1,fill_color=interpolate_color(ManimColor(COLD),ManimColor(HOT),np.clip(v,0,1))).move_to([x-w/2+w*(j+.5)/len(vals),y,0]) for j,v in enumerate(vals)])
def heat(x,t):
 # Neumann boundaries on [0,1]; exactly solves u_t=.08 u_xx.
 return .5+.28*np.cos(np.pi*x)*np.exp(-.08*np.pi**2*t)+.13*np.cos(3*np.pi*x)*np.exp(-.08*(3*np.pi)**2*t)+.06*np.cos(7*np.pi*x)*np.exp(-.08*(7*np.pi)**2*t)
def distribution(t,y=-.7,w=10):
 x=np.linspace(0,1,56);g=rod(heat(x,t),1.25,w=w)
 g.add(Line([-w/2,-1.9,0],[w/2,-1.9,0],stroke_color=MUTED,stroke_width=1),Line([-w/2,-1.9,0],[-w/2,.8,0],stroke_color=MUTED,stroke_width=1))
 g.add(path([[w*(v-.5),-1.9+2.7*heat(v,t),0] for v in np.linspace(0,1,160)],GOLD))
 return g
def project(p):
 x,y,z=p;return np.array([.91*x-.42*y,.28*x+.50*y+.87*z,0])
def surface(p,kind='sheet',warm=False):
 g=VGroup()
 if kind=='sheet':
  for v in np.linspace(-2.4,2.4,13):
   for axis in [0,1]:
    pts=[]
    for u in np.linspace(-2.6,2.6,65):
     x,y=(u,v) if axis==0 else (v,u);z=p*.6*np.cos(.9*x)*np.sin(.8*y)
     pts.append(project([x,y,z])+[0,.3,0])
    g.add(path(pts,COLD if not warm else interpolate_color(ManimColor(COLD),ManimColor(HOT),np.exp(-v*v/(.15+2*p))),1.4))
 else:
  def pt(a,b):
   rr=1.9*(1+.18*(1-p)*np.cos(3*a)*np.sin(b)**2)
   return project([rr*np.cos(a)*np.sin(b),rr*np.sin(a)*np.sin(b),rr*np.cos(b)])+[0,.3,0]
  for b in np.linspace(.12,np.pi-.12,12):g.add(path([pt(a,b) for a in np.linspace(0,TAU,90)],MINT,1.2))
  for a in np.linspace(0,TAU,18,endpoint=False):g.add(path([pt(a,b) for b in np.linspace(0,np.pi,65)],COLD,1.2))
 return g
def wave(x):return .8*np.sin(x)+.35*np.sin(2*x)+.2*np.sin(4*x)
class HeatScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  rng=np.random.default_rng(20261123)
  self.walks=np.concatenate([np.zeros((110,1,2)),np.cumsum(rng.normal(0,.14,(110,96,2)),axis=1)],axis=1)
  self.price=np.cumsum(rng.normal(0,.10,(7,120)),axis=1)
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.caption=VGroup();self.static=VGroup()
  self.add(self.clock,self.dynamic)
  self.add(RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#141E33',fill_opacity=.98).move_to([0,-3.27,0]).set_z_index(50))
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[t for t in [17,50,52,63,71,77,83,97,104,107,114,122,129,134,148,151,158,161,163,166] if self.start<t<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=(b-a),rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  self.remove(self.caption,self.static)
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  chunks=textwrap.wrap(line['text'],width=57,break_long_words=False,break_on_hyphens=False)
  self.caption=VGroup(*[tx(s,size=25,w=12.0) for s in chunks]).arrange(DOWN,buff=.09).move_to([0,-3.27,0]).set_z_index(51)
  self.static=self.labels(t);self.add(self.caption,self.static)
  for kind,group in [('caption',self.caption),('label',self.static),('geometry',self.geometry(t))]:
   if not len(group):continue
   r=dict(kind=kind,time=t,left=float(group.get_left()[0]),right=float(group.get_right()[0]),bottom=float(group.get_bottom()[1]),top=float(group.get_top()[1]))
   self.audit.append(r)
   assert r['left']>=-6.85 and r['right']<=6.85 and r['top']<=3.8,(self.index,r)
   assert r['bottom']>=(-3.8 if kind=='caption' else -2.65),(self.index,r)
 def labels(self,t):
  i=self.index;g=VGroup()
  titles={2:'온도 차이는 줄어든다',3:'열방정식',4:'스테판 문제',5:'나비에–스토크스 방정식',6:'헬레–쇼 문제',7:'물리 현상 너머로',8:'브라운 운동',9:'블랙–숄즈 방정식',10:'공간 위의 수학',11:'열핵 방법과 지표정리',12:'기하학적 흐름',13:'푸앵카레 추측',14:'서로 다른 문제, 공통된 구조',15:'열은 왜 퍼질까?',16:'두 가지 물리 법칙',17:'에너지 보존 법칙',18:'푸리에의 열전도 법칙',19:'두 원리에서 하나의 방정식으로',20:'방정식의 해 = 위치와 시간의 함수',21:'시간에 따라 변하는 상태',22:'복잡한 온도 분포는 어떻게 계산할까?',23:'복잡한 함수를 단순한 진동의 합으로'}
  if i!=1:g.add(tx(titles[i],0,3.18,30,c=GOLD))
  if i==2:g.add(tx('뜨거움',-4,2.05,23,c=HOT,w=2),tx('차가움',4,2.05,23,c=COLD,w=2),tx('접촉 후 열의 재분배',0,-2.35,21,c=MUTED))
  elif i==3:g.add(eq(r'\partial_t u=\kappa\Delta u',0,.5,65),tx('하나의 방정식, 여러 분야',0,-1.1,29,c=MINT))
  elif i==4:g.add(tx('얼음',-3.5,1.7,28,c=COLD),tx('물',3,1.7,28,c=MINT),tx('Stefan problem · 상변화와 잠열',0,-2.3,22,c=MUTED))
  elif i==5:g.add(eq(r'\partial_t\mathbf v+(\mathbf v\cdot\nabla)\mathbf v=-\nabla p/\rho+\nu\Delta\mathbf v',0,-1.6,32),tx('점성항의 확산 구조 · 흐름 개념도',0,-2.3,21,c=MUTED))
  elif i==6:g.add(tx('두 평행판 사이의 유체 경계',0,2.35,23,c=MINT),eq(r'\mathbf v\propto-\nabla p,\quad\Delta p=0',0,-1.85,31),tx('자유경계·라플라스 구조 · 개념도',0,-2.4,20,c=MUTED))
  elif i==7:g.add(tx('개별 입자 → 위치의 분포',0,-2.2,28,c=MINT))
  elif i==8:g.add(tx('개별 경로',-3.6,2.3,22,c=COLD),tx('위치의 확률밀도',3,2.3,22,c=MINT),eq(r'\partial_t p=\kappa\Delta p',2.8,-1.9,32,c=MINT,w=5),tx('확산계수 κ인 브라운 운동',-3.4,-1.9,20,c=MUTED,w=5))
  elif i==9:
   if t<52:g.add(eq(r'V_t+\frac12\sigma^2 S^2V_{SS}+rSV_S-rV=0',0,-1.3,37),tx('V : 옵션 가격 함수',0,-2.2,22,c=MUTED))
   else:g.add(eq(r'V(S,t)\ \longrightarrow\ u(x,\tau)',0,-.6,35),eq(r'u_\tau=\kappa u_{xx}',0,-1.7,40,c=MINT),tx('상수 금리·변동성의 표준 모형 · 변수변환',0,2.3,21,c=MUTED))
  elif i==10:g.add(tx('평면에서 곡면으로',0,-2.2,24,c=MINT))
  elif i==11:g.add(tx('Geometry',-4.7,.6,25,c=COLD,w=3),tx('Topology',4.7,.6,25,c=PURPLE,w=3),tx('열연산자를 이용하는 해석적 방법',0,-2.3,22,c=MUTED))
  elif i==12:g.add(eq(r'\partial_t g=-2\,\mathrm{Ric}(g)',3.5,.4,33,c=MINT,w=4.9),tx('리치 흐름 · 거리 구조의 변화',0,-1.95,23,c=MINT),tx('변형은 개념도 · 일반적으로 특이점이 생길 수 있음',0,-2.45,19,c=MUTED))
  elif i==13:g.add(tx('POINCARÉ CONJECTURE',0,1.5,35,c=MINT),tx('1904 → 2002–2003',0,.55,26),tx('해밀턴의 리치 흐름 · 페렐만의 특이점 분석과 수술',0,-1.4,24,c=COLD),tx('닫힌 단일연결 3차원 다양체 → 3차원 구면 S³',0,-2.25,22,c=MUTED))
  elif i==14:g.add(tx('확산 · 흐름 · 자유경계 · 기하학',0,-2.35,25,c=MINT))
  elif i==15:g.add(tx('가장 익숙한 현상으로 돌아가기',0,-2,26,c=MINT))
  elif i==16:g.add(tx('에너지 보존 법칙',0,-1.4,30,c=MINT),tx('작은 구간에 들어오는 열과 나가는 열',0,-2.2,23,c=MUTED))
  elif i==17:g.add(tx('유입 − 유출 = 에너지 변화',0,2.3,30,c=MINT),tx('에너지 증가' if t<107 else '에너지 감소',0,-1.1,29,c=HOT if t<107 else COLD),tx('내부 열원 없음 · 입자는 에너지 흐름의 기호',0,-2.3,20,c=MUTED))
  elif i==18:g.add(eq(r'\mathbf q=-k\nabla u',0,-1.6,42,c=MINT),tx('온도 구배가 커지면 열유속도 커진다',0,-2.35,23,c=MUTED))
  elif i==19:
   g.add(tx('에너지 보존',-3.6,1.85,28,c=COLD),tx('열전도 법칙',3.6,1.85,28,c=HOT))
   if t>=122:g.add(eq(r'\partial_t u=\kappa\Delta u',0,-.1,64),tx('시간 변화 = κ × 공간 변화',0,-1.25,27,c=MINT),tx('균질·등방성 물질 · 일정한 κ · 내부 열원 없음',0,-2.2,21,c=MUTED))
  elif i==20:g.add(eq(r'u(x,t)',4.7,2.3,39,c=MINT,w=2),tx('위치 x',5.3,-2.25,21,c=MUTED,w=2),tx('온도 u',-5.7,2.3,21,c=MUTED,w=2),tx('양 끝 단열 · 해석해의 실제 감쇠',0,-2.4,20,c=MUTED))
  elif i==21:
   for x,s,c in [(-4.2,'온도',HOT),(0,'확률밀도',MINT),(4.2,'속도',COLD)]:g.add(tx(s,x,1.9,25,c=c,w=3))
   g.add(tx('각 문제의 방정식과 조건에 따라 변화',0,-2.3,23,c=MUTED))
  elif i==22:g.add(tx('처음의 온도 분포',0,2.15,25,c=MUTED),tx('각 위치의 미래 온도는?',0,-2.15,27,c=MINT))
  elif i==23:
   if t<163:g.add(tx('조제프 푸리에',-4.4,1.7,29,c=GOLD,w=3.5),tx('Joseph Fourier',-4.4,.85,24,w=3.5),tx('1768–1830',-4.4,.2,22,c=MUTED,w=3.5))
   else:g.add(tx('FOURIER ANALYSIS',0,2.25,31,c=GOLD))
   g.add(tx('하나의 복잡한 함수 = 단순한 진동 함수들의 합',0,-2.35,23,c=MINT))
  return g
 def geometry(self,t):
  i=self.index;p=np.clip((t-self.start)/(self.end-self.start),0,1);g=VGroup()
  if i==1:
   g.add(rod(np.ones(60)*(.95-.5*p),y=.25,w=9,h=.8))
   for j in range(3):g.add(RoundedRectangle(width=9+.23*j,height=.8+.23*j,corner_radius=.1,stroke_color=HOT,stroke_opacity=(1-p)*.15/(j+1),stroke_width=14,fill_opacity=0).move_to([0,.25,0]))
  elif i==2:
   # Analytic cosine profile, insulated ends; same profile in rod and graph.
   tau=2*p;g=distribution(tau);g.add(arr([-1,2,0],[1,2,0],HOT))
  elif i==3:
   for a in np.linspace(0,TAU,10,endpoint=False):
    r=2+1.4*p;g.add(Line([1.7*np.cos(a),.5+1.7*np.sin(a),0],[r*np.cos(a),.5+.65*r*np.sin(a),0],stroke_color=COLD,stroke_opacity=.3))
  elif i==4:
   b=-1.8+2.6*np.sqrt(p);left=-5;right=5
   g.add(Rectangle(width=b-left,height=2.2,fill_color=COLD,fill_opacity=.32,stroke_width=0).move_to([(b+left)/2,.1,0]),Rectangle(width=right-b,height=2.2,fill_color='#137D9B',fill_opacity=.35,stroke_width=0).move_to([(right+b)/2,.1,0]),Line([b,-1,0],[b,1.2,0],color=INK,stroke_width=4),arr([b,.1,0],[b+1.1,.1,0],INK))
   for x in np.linspace(-4.6,b-.15,10):g.add(Line([x,-.8,0],[x+.25,-.35,0],stroke_color=COLD,stroke_opacity=.45))
  elif i==5:
   for r in np.linspace(.35,1.5,8):
    pts=[[2.2*r*np.cos(a),.5+.68*r*np.sin(a),0] for a in np.linspace(0,TAU,90)];g.add(path(pts,COLD,1.5,.65))
    a=TAU*(p*.8+r);g.add(Dot([2.2*r*np.cos(a),.5+.68*r*np.sin(a),0],radius=.045,color=MINT))
   for y in [-.45,.15,.75,1.35]:g.add(arr([-5,y,0],[-3.8,y,0],COLD),arr([3.8,y,0],[5,y,0],COLD))
  elif i==6:
   for y in [-.14,.14]:g.add(RoundedRectangle(width=7.6,height=3.0,corner_radius=.12,stroke_color=COLD,stroke_opacity=.4,fill_opacity=.015).move_to([0,y+.2,0]))
   a=np.linspace(0,TAU,200);rr=(.15+1.08*p)*(1+.32*p*np.cos(7*a)+.13*p*np.sin(11*a));pts=[[1.5*r*np.cos(z),.2+r*np.sin(z),0] for r,z in zip(rr,a)]
   poly=Polygon(*pts,fill_color=MINT,fill_opacity=.35,stroke_color=MINT,stroke_width=2);g.add(poly,Dot([0,.2,0],radius=.07,color=INK))
  elif i in [7,8]:
   f=p if i==7 else .12+.88*p;k=min(95,int(f*95));blend=f*95-k
   pos=self.walks[:,k,:]*(1-blend)+self.walks[:,k+1,:]*blend
   if i==7:
    for x,y in pos:g.add(Dot([x*1.3,y*.5+.2,0],radius=.028,color=MINT))
   else:
    # Genuine seeded Gaussian random-walk samples, histogram from these endpoints.
    for j,(x,y) in enumerate(pos):
     if j<7:g.add(path([[v[0]*.65-3.6,v[1]*.55+.25,0] for v in self.walks[j,:k+1,:]],COLD,1,.3))
     g.add(Dot([x*.65-3.6,y*.55+.25,0],radius=.025,color=COLD))
    vals=pos[:,0];bins=np.linspace(-4.5,4.5,19);h,_=np.histogram(vals,bins=bins,density=True)
    for j,v in enumerate(h):g.add(Rectangle(width=.24,height=max(.005,3*v),fill_color=MINT,fill_opacity=.35,stroke_width=0).move_to([.5+(j+.5)*.25,-1+1.5*v,0]))
    sig=.14*np.sqrt(max(1,f*96));xs=np.linspace(-4.5,4.5,120)
    g.add(path([[2.75+x*.5,-1+3*np.exp(-x*x/(2*sig*sig))/(sig*np.sqrt(TAU)),0] for x in xs],MINT),arr([-.7,.5,0],[.2,.5,0],GOLD))
  elif i==9:
   if t<52:
    n=max(3,int(119*min(1,p*1.7)))
    for j in range(7):g.add(path([[-5+10*k/119,1.4+.33*self.price[j,k],0] for k in range(n)],COLD if j%2 else MINT,1.6,.7))
   else:g.add(Line([-4,1,0],[4,1,0],stroke_color=MUTED,stroke_opacity=.3))
  elif i==10:g=surface(p)
  elif i==11:
   g=surface(1, warm=True)
   for r in [.3,.65,1.,1.35]:
    rr=r+.6*p;g.add(path([project([rr*np.cos(a),rr*np.sin(a),.6*np.cos(.9*rr*np.cos(a))*np.sin(.8*rr*np.sin(a))])+[0,.3,0] for a in np.linspace(0,TAU,90)],HOT,2,.6))
   g.add(Line([-3.1,.6,0],[-2.4,.6,0],stroke_color=COLD),Line([2.4,.6,0],[3.1,.6,0],stroke_color=PURPLE))
  elif i==12:g=surface(p,'sphere').shift(LEFT*2)
  elif i==13:
   # Symbolic loop, not a 2D sphere masquerading as a 3-manifold.
   r=.65*(1-.6*p);g.add(path([[r*np.cos(a),-.35+.35*r*np.sin(a),0] for a in np.linspace(0,TAU,100)],MINT,3))
  elif i==14:
   names=['열','자유경계','유체','확률','금융','기하학']
   for j,s in enumerate(names):
    a=TAU*j/6;r=3.4*(1-.35*p);x=r*np.cos(a);y=.35+1.5*np.sin(a)
    g.add(Line([0,.35,0],[x,y,0],stroke_color=COLD,stroke_opacity=.4),Circle(radius=.38,stroke_color=COLD,fill_color=BG,fill_opacity=1).move_to([x,y,0]),tx(s,x,y,19,w=.7))
   g.add(Circle(radius=.62,stroke_color=MINT,fill_color=BG,fill_opacity=1).move_to([0,.35,0]),tx('구조',0,.35,25,c=MINT,w=1.1))
  elif i==15:g=rod(heat(np.linspace(0,1,60),.15),y=.4)
  elif i in [16,17]:
   g=rod(np.ones(60)*.5,y=.5)
   g.add(DashedVMobject(Rectangle(width=1.7,height=1.25,stroke_color=INK).move_to([0,.5,0]),num_dashes=24))
   incoming=5 if i==16 or t<107 else 2;outgoing=2 if i==16 or t<107 else 5
   for j in range(incoming):g.add(Dot([-3.3+((p*4+j/5)%1)*2.45,.15+j*.14,0],radius=.055,color=HOT))
   for j in range(outgoing):g.add(Dot([.85+((p*4+j/5)%1)*2.45,.3+j*.14,0],radius=.055,color=GOLD))
   g.add(arr([-3.3,1.5,0],[-.9,1.5,0],HOT,5 if incoming==5 else 2),arr([.9,1.5,0],[3.3,1.5,0],GOLD,5 if outgoing==5 else 2))
   if i==17:g.add(Rectangle(width=1.6,height=.46,stroke_width=0,fill_color=HOT if t<107 else COLD,fill_opacity=.5+.3*np.sin(p*np.pi)**2).move_to([0,.5,0]))
  elif i==18:
   steep=.3+.7*p;xx=np.linspace(0,1,60);vals=.5-.42*np.tanh((xx-.5)*(2+7*p))
   g=rod(vals,y=1.1);g.add(graph(lambda x:-.65*np.tanh(x*(.2+.6*p)),y=-.2,c=GOLD),arr([-.4,.4,0],[.5+1.4*steep,.4,0],HOT,2+4*p))
  elif i==19:
   g.add(arr([-3.6,1.2,0],[-1.3,.4,0],COLD),arr([3.6,1.2,0],[1.3,.4,0],HOT))
   if t<122:g.add(Circle(radius=.45,stroke_color=MINT).move_to([0,.15,0]))
  elif i==20:
   tau=max(0,(t-131)/7)*1.5;g=distribution(tau)
   x=.32;u=heat(x,tau);g.add(Dot([10*(x-.5),-1.9+2.7*u,0],radius=.065,color=MINT),Line([10*(x-.5),-1.9,0],[10*(x-.5),1.5,0],stroke_color=MINT,stroke_opacity=.3))
   g.add(tx(f't = {tau:.1f}',0,2.3,26,c=MINT,w=3))
  elif i==21:
   for x in [-4.2,0,4.2]:g.add(Line([x-1.65,-1.4,0],[x+1.65,-1.4,0],stroke_color=MUTED,stroke_width=1))
   for x,c,fn in [(-4.2,HOT,lambda z:1+.5*np.cos(z)*np.exp(-2*p)),(0,MINT,lambda z:np.exp(-z*z/(.4+2*p))/(np.sqrt(.4+2*p))),(4.2,COLD,lambda z:.8+.5*np.sin(z)*np.exp(-p))]:
    g.add(path([[x+z,-1.4+fn(z),0] for z in np.linspace(-1.6,1.6,90)],c))
  elif i==22:
   g.add(Line([-5.5,-1.5,0],[5.5,-1.5,0],stroke_color=MUTED,stroke_width=1),graph(lambda x:wave(x*1.1),y=.1,c=GOLD))
   g.add(rod(.5+.3*np.array([wave(x) for x in np.linspace(-6,6,60)]),y=1.35))
  elif i==23:
   if t<158:
    g.add(graph(lambda x:wave(x*1.1),x0=-1.8,x1=5.5,y=.2,c=GOLD))
   else:
    q=np.clip((t-158)/5,0,1);xs=np.linspace(-5.2,5.2,150)
    colors=[COLD,MINT,PURPLE];amps=[.8,.35,.2];freq=[1,2,4];offsets=[1.05,-.15,-1.35]
    for a,k,y,c in zip(amps,freq,offsets,colors):g.add(path([[x,q*y+(1-q)*.2+a*.55*np.sin(k*x*1.1),0] for x in xs],c,2.5,q))
    g.add(path([[x,1.5+(1-q)*(-1.3)+.55*wave(x*1.1),0] for x in xs],GOLD,3))
  return g
