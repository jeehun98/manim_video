"""Fourier analysis: shared visual vocabulary, computed curves and exact timing."""
import importlib.util,json,textwrap
from pathlib import Path
import numpy as np
from manim import *
from mechanics import K,A,KAPPA,component,solution,square_partial,product_integral
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('heat_chapter1_helpers',R.parent/'chapter_01/visuals.py')
common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
tx=common.tx;eq=common.eq;path=common.path;arr=common.arr
BG='#10131C';INK='#F1F4FA';MUTED='#8E9BB0';BLUE='#4A9EFF';GREEN='#36C7A3';ORANGE='#F0A45D';PURPLE='#B69AFF';YELLOW='#F3CE77'
COLORS=[BLUE,GREEN,ORANGE]
config.frame_width=128/9;config.frame_height=8;config.background_color=BG
# Reuse content-addressed vector formula SVGs across independent shots.
config.tex_dir=str(R.parents[2]/'media/Tex')
TAU=2*np.pi;X=np.linspace(0,TAU,241)
def progress(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def chart(fn,c=INK,cx=0,cy=0,w=10,h=1.9,axis=True,opacity=1,portion=1):
 xs=X[X<=TAU*max(.005,portion)];g=VGroup()
 if axis:g.add(Line([cx-w/2,cy,0],[cx+w/2,cy,0],stroke_color=MUTED,stroke_width=1,stroke_opacity=.4))
 g.add(path([[cx+w*(x/TAU-.5),cy+h/2*float(fn(x)),0] for x in xs],c,2.8,opacity))
 return g
def fill_product(m=1,n=3,cx=0,cy=-.15,w=10,h=2.2,cut=1):
 xs=X[X<=TAU*max(.005,cut)];v=np.sin(m*xs)*np.sin(n*xs);g=VGroup()
 for sign,c in [(1,GREEN),(-1,ORANGE)]:
  y=np.maximum(v,0) if sign==1 else np.minimum(v,0)
  pts=[[cx-w/2,cy,0]]+[[cx+w*(x/TAU-.5),cy+h/2*z,0] for x,z in zip(xs,y)]+[[cx+w*(xs[-1]/TAU-.5),cy,0]]
  g.add(Polygon(*pts,stroke_width=0,fill_color=c,fill_opacity=.35))
 g.add(chart(lambda x:np.sin(m*x)*np.sin(n*x),PURPLE,cx,cy,w,h))
 return g
def rows(tau=0,offset=1,cx=.7,w=9,amplitudes=True):
 g=VGroup()
 for j,y in enumerate([1.2,0,-1.2]):
  g.add(chart(lambda x:component(x,j,tau) if amplitudes else np.sin(K[j]*x),COLORS[j],cx,y*offset,w,1.1))
 return g
def color_rod(tau,y=1.2,w=10):
 vals=solution(np.linspace(0,TAU,60),tau);g=VGroup()
 for j,v in enumerate(vals):g.add(Rectangle(width=w/60+.006,height=.38,stroke_width=0,fill_opacity=1,fill_color=interpolate_color(ManimColor(BLUE),ManimColor(ORANGE),.5+v/3.5)).move_to([-w/2+w*(j+.5)/60,y,0]))
 return g
def coefficient_bars(active=None,cx=0,cy=-1.1,w=7):
 g=VGroup()
 for j,(k,a,c) in enumerate(zip(K,A,COLORS)):
  x=cx+(j-1)*w/3;g.add(Rectangle(width=.75,height=1.3*a,stroke_color=c,stroke_width=2,fill_color=c,fill_opacity=.7 if active==j else .3).move_to([x,cy+1.3*a/2,0]))
  g.add(tx(f'k={int(k)}',x,cy-.3,20,c=MUTED,w=1.8),tx(f'{a:g}',x,cy+1.3*a+.25,23,c=c,w=1.8))
 return g
def section(t):
 for end,label in [(67,'합성에서 분해로'),(123,'직교성 · 곱의 적분'),(185,'진동 성분의 계수 추출'),(248,'고유함수 · 독립적인 감쇠'),(292,'선형성 · 해의 재결합'),(325,'분해 → 독립 계산 → 재결합')]:
  if t<end:return label
class FourierScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def init_scene(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  self.caption=VGroup();self.static=VGroup();self.header=VGroup()
 def construct(self):
  self.init_scene();self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#192031',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  extra=[6,21,28,33,37,43,53,58,62,71,75,80,87,99,103,107,112,119,128,136,139,142,145,150,158,160,168,176,178,180,193,201,203,206,209,215,221,228,232,241,252,253,257,265,268,271,276,283,296,303,309,315,318,322]
  events=sorted(set([self.start,self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]+[t for t in extra if self.start<t<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  self.remove(self.caption,self.static,self.header)
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  # Scale the whole caption together so short final lines keep the same size.
  self.caption=VGroup(*[tx(s,size=25,w=30) for s in textwrap.wrap(line['text'],width=49,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.09)
  if self.caption.width>12:self.caption.scale_to_fit_width(12)
  if self.caption.height>.82:self.caption.scale_to_fit_height(.82)
  self.caption.move_to([0,-3.27,0]).set_z_index(51)
  self.static=self.labels(t)
  self.header=VGroup(tx('CHAPTER 02  /  FOURIER ANALYSIS',-4.25,3.69,16,c=MUTED,w=5.4),tx(section(t),4.1,3.69,19,c=INK,w=5.6),Line([-6.4,3.45,0],[6.4,3.45,0],stroke_color=MUTED,stroke_opacity=.25))
  self.add(self.caption,self.static,self.header)
  for kind,group in [('caption',self.caption),('label',self.static),('header',self.header),('geometry',self.geometry(t))]:
   if not len(group):continue
   d=dict(kind=kind,time=t,left=float(group.get_left()[0]),right=float(group.get_right()[0]),bottom=float(group.get_bottom()[1]),top=float(group.get_top()[1]))
   self.audit.append(d)
   assert d['left']>=-6.9 and d['right']<=6.9 and d['top']<=3.88,(self.index,d)
   assert d['bottom']>=(-3.8 if kind=='caption' else -2.65),(self.index,d)
   if kind=='label':assert d['top']<3.35,(self.index,d)
 def labels(self,t):
  i=self.index;g=VGroup();title=self.rec['title']
  g.add(tx(title,0,2.98,29,c=YELLOW))
  if i==1:
   g.add(tx('복잡한 온도 분포',0,1.9,24,c=MUTED))
   if t>=6:g.add(tx('이 곡선 안에는 어떤 진동이 숨어 있을까?',0,-1.9,29,c=GREEN))
  elif i==2:
   for j,k in enumerate([1,3,5]):
    if t>=11+j*4:g.add(eq(r'\sin x' if k==1 else rf'\sin {k}x',-5.5,1.2-j*1.2,30,c=COLORS[j],w=2.4),tx(f'{k}번 진동',5.4,1.2-j*1.2,20,c=COLORS[j],w=2))
   g.add(tx('같은 구간 0 ≤ x ≤ 2π · 진폭은 동일',0,-2.35,22,c=MUTED))
  elif i==3:
   g.add(eq(r'\sin x',-3.4,1.9,28,c=BLUE,w=4),eq(r'a\sin3x',-3.4,-.15,28,c=GREEN,w=4),eq(r'f(x)=\sin x+a\sin3x',3.1,1.9,31,w=6))
   g.add(tx('같은 x에서 높이를 더한다' if t<37 else '진폭 = 전체 곡선에 기여하는 크기',0,-2.35,24,c=GREEN))
  elif i in [4,5,10,14]:
   g.add(eq(r'f(x)=\sin x+0.5\sin3x+0.25\sin5x',0,2.05,34))
   if i==4:g.add(tx('단순한 함수들의 합 → 복잡한 함수',0,-2.35,24,c=GREEN))
   elif i==5:g.add(tx('합성하는 것과 성분을 찾아내는 것은 다른 문제',0,-2.35,24,c=PURPLE))
   elif i==10:g.add(tx('첫 번째 진동은 얼마나 포함되어 있을까?',0,-2.35,24,c=BLUE))
   else:g.add(tx('분해 → 계수 추출 → 원래 함수의 복원',0,-2.35,24,c=GREEN))
  elif i==6:
   g.add(eq(r'\mathbf e_1\cdot\mathbf e_2=0',-3.6,2,33,c=BLUE,w=5),eq(r'\langle f,g\rangle=0\;?',3.2,2,33,c=PURPLE,w=5))
   g.add(tx('벡터의 직교',-3.6,-1.9,24,c=BLUE,w=5),tx('함수의 직교',3.2,-1.9,24,c=PURPLE,w=5),tx('그래프가 직각으로 교차한다는 뜻이 아니다',0,-2.4,21,c=MUTED))
  elif i==7:
   g.add(eq(r'f=\sin x',-5.5,1.35,27,c=BLUE,w=2.5),eq(r'g=\sin3x',-5.5,.45,27,c=GREEN,w=2.5),eq(r'fg',-5.5,-.85,29,c=PURPLE,w=2.4))
   g.add(eq(r'\langle f,g\rangle=\int_0^{2\pi}f(x)g(x)\,dx',0,-2.1,35,c=PURPLE))
  elif i==8:
   g.add(eq(r'\int_0^{2\pi}\sin x\sin3x\,dx=0',0,2.1,37,c=PURPLE),tx('양수 넓이',-3.8,-1.85,23,c=GREEN,w=4),tx('음수 넓이',3.8,-1.85,23,c=ORANGE,w=4),tx('[0, 2π] · 서로 다른 양의 정수 주파수',0,-2.4,21,c=MUTED))
  elif i==9:g.add(eq(r'\int_0^{2\pi}\sin^2x\,dx=\pi>0',0,2.05,38,c=BLUE),tx('서로 다른 성분: 0       같은 성분: π',0,-2.15,26,c=PURPLE))
  elif i==11:
   g.add(eq(r'\int_0^{2\pi}f(x)\sin x\,dx',0,2.1,36,c=BLUE))
   for j,(s,c) in enumerate([(r'\sin^2x',BLUE),(r'0.5\sin3x\sin x',GREEN),(r'0.25\sin5x\sin x',ORANGE)]):g.add(eq(s,(j-1)*4.2,1.35,27,c=c,w=3.8))
   if t<142:g.add(eq(r'\pi',-4.2,-1.25,38,c=BLUE),eq('0',0,-1.25,38,c=GREEN),eq('0',4.2,-1.25,38,c=ORANGE))
   else:g.add(eq(r'a_1=\frac{\langle f,\sin x\rangle}{\langle\sin x,\sin x\rangle}=\frac{\pi}{\pi}=1',0,-1.65,39,c=BLUE))
   g.add(tx('他 성분은 상쇄 · 자기 성분은 남는다'.replace('他','다른'),0,-2.4,22,c=MUTED))
  elif i==12:
   k=3 if t<150 else 5;c=GREEN if k==3 else ORANGE
   g.add(eq(rf'a_{k}=\frac1\pi\int_0^{{2\pi}}f(x)\sin{k}x\,dx='+('0.5' if k==3 else '0.25'),0,2.0,37,c=c),tx('같은 내적 계산으로 얻은 계수',0,-2.35,24,c=MUTED))
  elif i==13:
   g.add(eq(r'\mathbf v=3\mathbf e_1+2\mathbf e_2',-3.7,1.95,31,c=BLUE,w=5.5),eq(r'f=1\phi_1+0.5\phi_3+0.25\phi_5',3.1,1.95,29,w=6.4),tx('벡터의 좌표',-3.5,-2.1,24,c=BLUE,w=5),tx('함수의 진동 성분 계수',3.1,-2.1,24,c=PURPLE,w=6))
  elif i==15:
   n=self.partial_n(t);g.add(eq(r'S_N(x)=\frac4\pi\sum_{j=0}^{N-1}\frac{\sin((2j+1)x)}{2j+1}',0,2.0,33),tx(f'진동 성분 N = {n}',-3.5,-1.85,25,c=GREEN,w=5),tx('점선: 목표 사각파',3.4,-1.85,23,c=MUTED,w=5),tx('불연속점에서는 좌우 극한의 평균 · 경계 부근의 깁스 현상',0,-2.4,21,c=MUTED))
  elif i==16:g.add(eq(r'f(x)=a_0+\sum_{n=1}^{\infty}\left(a_n\cos nx+b_n\sin nx\right)',0,.75,41),tx('FOURIER SERIES · 푸리에 급수',0,-.6,31,c=PURPLE),tx('주기적 함수의 예 · a₀는 상수항 자체',0,-2.3,22,c=MUTED))
  elif i==17:g.add(eq(r'\partial_tu=\kappa\partial_{xx}u',0,2,42,c=YELLOW),tx('각 성분을 계산하면 전체 변화도 알 수 있을까?',0,-1.9,25,c=GREEN),tx('주기적 경계조건 · 기준 온도에 대한 편차 u',0,-2.4,21,c=MUTED))
  elif i==18:
   formula=r'\sin x\ \xrightarrow{d/dx}\ \cos x' if t<203 else r'\sin x\ \xrightarrow{d/dx}\ \cos x\ \xrightarrow{d/dx}\ -\sin x'
   g.add(eq(formula,0,2,39,c=YELLOW),tx('공간 미분 두 번 → 원래 함수의 상수배',0,-2.25,26,c=PURPLE))
  elif i==19:g.add(eq(r'\frac{d^2}{dx^2}\sin(kx)=-k^2\sin(kx)',0,2,41,c=YELLOW),tx('고유함수 Eigenfunction',0,-1.85,30,c=PURPLE),tx('아래 곡선은 형태 비교: sin(3x)와 −sin(3x) · 고유값 −9',0,-2.4,20,c=MUTED))
  elif i==20:g.add(eq(r'u(x,t)=e^{-\kappa t}\sin x',0,2,43,c=BLUE),tx('봉우리와 골짜기의 위치는 그대로',0,-1.9,26,c=GREEN),tx('u는 기준 온도에 대한 편차 · κ = 0.12',0,-2.4,21,c=MUTED))
  elif i==21:
   for j,(k,c) in enumerate(zip([1,3,5],COLORS)):g.add(eq(rf'e^{{-{k*k}\kappa t}}',-5.4,1.2-j*1.2,29,c=c,w=2.5))
   g.add(tx('같은 시간 · 높은 주파수일수록 빠른 감쇠',0,-2.4,23,c=YELLOW))
  elif i==22:
   g.add(eq(r'A_k^{\prime}(t)=-\kappa k^2A_k(t)',0,2.05,41,c=YELLOW))
   for j,(k,c) in enumerate(zip([1,3,5],COLORS)):g.add(eq(rf'A_{k}(t)=A_{k}(0)e^{{-{k*k}\kappa t}}',(j-1)*4.15,-1.65,27,c=c,w=4))
   g.add(tx('각 진폭 방정식에는 다른 성분의 계수가 없다',0,-2.4,23,c=MUTED))
  elif i==23:
   g.add(tx('먼저 합한 뒤 연산',-3.5,2,23,c=BLUE,w=5),tx('각각 연산한 뒤 합산',3.5,2,23,c=GREEN,w=5))
   g.add(eq(r'L(af+bg)=aL(f)+bL(g)',0,-1.8,43,c=PURPLE),tx('L = ∂ₓₓ · a, b는 상수',0,-2.4,21,c=MUTED))
  elif i==24:
   g.add(eq(r'u_1',-3.6,1.9,34,c=BLUE,w=3),eq(r'u_2',-3.6,-.1,34,c=GREEN,w=3),eq(r'u=u_1+u_2' if t<268 else r'u=au_1+bu_2',3,1.9,36,w=6))
   g.add(tx('중첩의 원리' if t>=271 else '두 해의 합도 열방정식의 해',0,-1.95,28,c=PURPLE),tx('열원 없는 동차 방정식 · 같은 주기적 경계조건',0,-2.45,20,c=MUTED))
  elif i in [25,26]:
   g.add(eq(r'u=e^{-\kappa t}\sin x+0.5e^{-9\kappa t}\sin3x+0.25e^{-25\kappa t}\sin5x',0,2.05,32))
   g.add(tx('독립적으로 계산한 해를 같은 위치에서 더한다' if i==25 else '작은 요철이 먼저 사라진다 · 점선은 초기 분포',0,-2.35,23,c=GREEN))
  elif i==27:
   for x,s,c in [(-4.5,'분해',PURPLE),(0,'독립 계산',YELLOW),(4.5,'재결합',GREEN)]:g.add(tx(s,x,1.95,27,c=c,w=3.5))
   g.add(tx('하나의 복잡한 PDE → 여러 진폭 ODE → 전체 해',0,-2.3,25,c=INK))
  elif i==28:g.add(eq(r'\langle\sin(mx),\sin(nx)\rangle=0\quad(m\ne n)',0,2,35,c=PURPLE),tx('직교성 — 성분을 구별하고 계수를 구한다',0,-2.35,26,c=PURPLE))
  elif i==29:g.add(eq(r'\partial_{xx}\sin(kx)=-k^2\sin(kx)',0,2,39,c=YELLOW),tx('고유함수 — 미분을 각 성분의 상수배로 바꾼다',0,-2.35,25,c=YELLOW))
  elif i==30:g.add(eq(r'L(u_1+u_2+u_3)=L(u_1)+L(u_2)+L(u_3)',0,2,35,c=GREEN),tx('선형성 — 각각의 해를 합쳐 전체 해를 만든다',0,-2.35,25,c=GREEN))
  elif i==31:
   if t<322:g.add(tx('하나의 복잡한 문제를, 수많은 간단한 문제로.',0,-2.25,29,c=GREEN))
   if t<318:
    for x,s,c in [(-4.3,'직교성 · 분해',PURPLE),(0,'고유함수 · 계산',YELLOW),(4.3,'선형성 · 결합',GREEN)]:g.add(tx(s,x,2,23,c=c,w=4))
  return g
 @staticmethod
 def partial_n(t):return 1 if t<176 else 3 if t<178 else 10 if t<180 else 30
 def geometry(self,t):
  i=self.index;p=progress(t,self.start,self.end);g=VGroup()
  if i==1:
   q=progress(t,6,11)
   old=lambda x:.8*np.sin(1.1*(x/TAU*10.4-5.2))+.35*np.sin(2.2*(x/TAU*10.4-5.2))+.2*np.sin(4.4*(x/TAU*10.4-5.2))
   g.add(chart(lambda x:(1-q)*old(x)+q*solution(x),INK,cy=.1,h=2.2))
  elif i==2:
   for j,k in enumerate([1,3,5]):
    if t>=11+4*j:g.add(chart(lambda x:np.sin(k*x),COLORS[j],cx=.1,cy=1.2-j*1.2,w=8.2,h=1.0,portion=progress(t,11+j*4,15+j*4)))
  elif i==3:
   a=.5 if t<33 else (.5*(1-progress(t,33,37)) if t<37 else progress(t,37,43))
   g.add(chart(lambda x:np.sin(x),BLUE,-3.4,1,4.8,1.2),chart(lambda x:a*np.sin(3*x),GREEN,-3.4,-1.1,4.8,1.2),chart(lambda x:np.sin(x)+a*np.sin(3*x),INK,3.1,.1,5,1.7))
   z=TAU*p
   for cx,cy,w,h,v,c in [(-3.4,1,4.8,1.2,np.sin(z),BLUE),(-3.4,-1.1,4.8,1.2,a*np.sin(3*z),GREEN),(3.1,.1,5,1.7,np.sin(z)+a*np.sin(3*z),INK)]:
    xx=cx+w*(z/TAU-.5);g.add(Line([xx,cy,0],[xx,cy+h*v/2,0],stroke_color=c,stroke_width=4),Dot([xx,cy+h*v/2,0],radius=.045,color=c))
   g.add(tx(f'a = {a:.2f}',-3.4,-1.9,25,c=GREEN,w=3))
  elif i==4:
   for j,y in enumerate([.8,0,-.8]):g.add(chart(lambda x:component(x,j),COLORS[j],cy=y*(1-p),h=1.7,opacity=1-.6*p))
   g.add(chart(solution,INK,cy=0,h=1.7,portion=p))
  elif i==5:
   if t<58:
    g.add(chart(solution,INK,cy=.1,h=1.9),arr([-1,-1.55,0],[1,-1.55,0],PURPLE) if t<53 else arr([1,-1.55,0],[-1,-1.55,0],PURPLE))
   else:
    q=progress(t,58,62)
    for j,y in enumerate([1.1,0,-1.1]):g.add(chart(lambda x:component(x,j),COLORS[j],cx=.5,cy=q*y,w=9,h=1.2))
    if t>=62:
     for j,(k,a) in enumerate(zip(K,A)):g.add(tx(f'k={int(k)}  a={a:g}',-5.6,1.1-j*1.1,20,c=COLORS[j],w=2.3))
  elif i==6:
   o=np.array([-4.5,-.8,0]);g.add(arr(o,o+[2.3,0,0],BLUE),arr(o,o+[0,2.1,0],GREEN),Line(o+[.3,0,0],o+[.3,.3,0],stroke_color=INK),Line(o+[.3,.3,0],o+[0,.3,0],stroke_color=INK))
   if t>=75:g.add(chart(lambda x:np.sin(x),BLUE,3,.75,5.1,1.0),chart(lambda x:np.sin(3*x),GREEN,3,-.65,5.1,1.0))
  elif i==7:
   g.add(chart(lambda x:np.sin(x),BLUE,.7,1.35,8.8,.65),chart(lambda x:np.sin(3*x),GREEN,.7,.45,8.8,.65),fill_product(cx=.7,cy=-.85,w=8.8,h=1.2,cut=p))
  elif i==8:
   q=progress(t,99,112);g=fill_product(cut=q)
   z=TAU*q;g.add(Line([-5+10*q,-1.35,0],[-5+10*q,1.2,0],stroke_color=PURPLE,stroke_opacity=.65))
   integral=float(product_integral(z));g.add(tx(f'누적 적분 = {integral:+.3f}',0,-1.75,25,c=PURPLE,w=5))
  elif i==9:
   q=progress(t,115,119)
   g.add(chart(lambda x:(1-q)*np.sin(x)*np.sin(3*x)+q*np.sin(x)**2,PURPLE,cy=.1,h=2))
   if t>=119:g.add(fill_product(1,1,cy=.1,h=2,cut=progress(t,119,123)))
  elif i==10:
   g.add(chart(solution,INK,cy=.55,h=1.6))
   if t>=128:g.add(chart(lambda x:np.sin(x),BLUE,cy=-1.1,h=1),tx('×',-5.6,-1.05,30,c=BLUE,w=1))
  elif i==11:
   for j,(k,a,c) in enumerate(zip(K,A,COLORS)):
    opacity=1 if j==0 or t<139 else .15
    g.add(chart(lambda x:a*np.sin(k*x)*np.sin(x),c,(j-1)*4.2,.15,3.5,1.4,opacity=opacity))
    if j>0 and t>=139:g.add(Line([(j-1)*4.2-.9,-.5,0],[(j-1)*4.2+.9,.8,0],stroke_color=ORANGE,stroke_width=3))
   if t>=142:g.add(tx('÷ π',4.8,-1.65,25,c=BLUE,w=2))
  elif i==12:g=coefficient_bars(1 if t<150 else 2,cy=-1.3)
  elif i==13:
   o=np.array([-5.2,-1.1,0]);q=progress(t,154,160)
   g.add(arr(o,o+[3.5,0,0],MUTED),arr(o,o+[0,2.4,0],MUTED),arr(o,o+[2.8,1.8,0],BLUE),DashedLine(o+[2.8,1.8,0],o+[2.8,0,0],color=BLUE,stroke_opacity=q),DashedLine(o+[2.8,1.8,0],o+[0,1.8,0],color=GREEN,stroke_opacity=q),tx('3',-2.4,-1.45,24,c=BLUE,w=1),tx('2',-5.6,.7,24,c=GREEN,w=1),coefficient_bars(cx=3.3,cy=-1.1,w=5))
  elif i==14:
   q=p
   for j,y in enumerate([1.1,0,-1.1]):g.add(chart(lambda x:component(x,j),COLORS[j],cy=y*(1-q),h=1.6,opacity=1-.6*q))
   g.add(chart(solution,INK,cy=0,h=1.6,portion=q))
  elif i==15:
   g.add(chart(lambda x:square_partial(x,self.partial_n(t)),INK,cy=.1,h=1.9))
   target=path([[-5,.1,0],[-5,1.05,0],[0,1.05,0],[0,-.85,0],[5,-.85,0]],MUTED,2,.5);g.add(DashedVMobject(target,num_dashes=55))
  elif i==16:
   for j in range(3):g.add(chart(lambda x:component(x,j),COLORS[j],cx=(j-1)*4.2,cy=-1.55,w=3.5,h=.8))
  elif i==17:g.add(color_rod(0,y=1.2),chart(solution,INK,cy=-.3,h=1.65))
  elif i==18:
   if t<203:q=progress(t,198,203);fn=lambda x:(1-q)*np.sin(x)+q*np.cos(x)
   else:q=progress(t,203,209);fn=lambda x:(1-q)*np.cos(x)-q*np.sin(x)
   g.add(chart(lambda x:np.sin(x),BLUE,cy=0,h=2,opacity=.25),chart(fn,YELLOW if t<209 else PURPLE,cy=0,h=2))
  elif i==19:g.add(chart(lambda x:np.sin(3*x),BLUE,cy=0,h=1.8,opacity=.6),chart(lambda x:-np.sin(3*x),PURPLE,cy=0,h=1.8))
  elif i==20:
   tau=4*progress(t,221,225);g.add(color_rod(tau,y=1.2),chart(lambda x:np.sin(x)*np.exp(-KAPPA*tau),BLUE,cy=-.25,h=2),tx(f't = {tau:.1f}',0,-1.6,25,c=YELLOW,w=3))
   # The rod must match this single-mode demonstration, not the three-mode sum.
   g.remove(g[0]);vals=np.sin(np.linspace(0,TAU,60))*np.exp(-KAPPA*tau)
   single=VGroup(*[Rectangle(width=10/60+.006,height=.38,stroke_width=0,fill_opacity=1,fill_color=interpolate_color(ManimColor(BLUE),ManimColor(ORANGE),.5+v/3.5)).move_to([-5+10*(j+.5)/60,1.2,0]) for j,v in enumerate(vals)]);g.add(single)
  elif i==21:
   tau=3*progress(t,228,236);g=rows(tau,cx=.4,w=8.2)
   g.add(tx(f't = {tau:.1f}',5.7,2.15,22,c=YELLOW,w=2))
  elif i==22:
   tau=1.5*p
   for j,c in enumerate(COLORS):
    cx=(j-1)*4.15;g.add(RoundedRectangle(width=3.8,height=2.6,corner_radius=.12,stroke_color=c,stroke_opacity=.35).move_to([cx,.3,0]),chart(lambda x:component(x,j,tau),c,cx,.5,3.3,1.5),tx(f'A = {A[j]*np.exp(-KAPPA*K[j]**2*tau):.3f}',cx,-.55,23,c=c,w=3.2))
  elif i==23:
   # d²/dx² applied to f=sin x, g=.5 sin3x with a=b=1.
   q=progress(t,253,261)
   fn=lambda x:-np.sin(x)-4.5*np.sin(3*x)
   for cx in [-3.5,3.5]:g.add(chart(lambda x:fn(x)/5.5,BLUE if cx<0 else GREEN,cx,.2,5,1.8))
   g.add(eq('=',0,.2,45,c=PURPLE,w=.7),arr([-5.5,1.4,0],[-1.5,1.4,0],BLUE),arr([1.5,1.4,0],[5.5,1.4,0],GREEN),Dot([-5.5+4*q,1.4,0],radius=.055,color=YELLOW),Dot([1.5+4*q,1.4,0],radius=.055,color=YELLOW),tx('동일한 결과 · 표시 배율 1/5.5',0,-.9,22,c=MUTED))
  elif i==24:
   tau=1.6*p;a=1 if t<268 else .7;b=1 if t<268 else 1.4
   g.add(chart(lambda x:a*component(x,0,tau),BLUE,-3.6,.95,4.5,1.1),chart(lambda x:b*component(x,1,tau),GREEN,-3.6,-1.1,4.5,1.1),chart(lambda x:a*component(x,0,tau)+b*component(x,1,tau),INK,3,.0,5,1.8),arr([-.9,0,0],[.2,0,0],PURPLE))
   if t>=268:g.add(tx('a=0.7, b=1.4',3,-1.3,23,c=MUTED,w=5))
  elif i in [25,30]:
   q=p;tau=.35+.3*q if i==25 else .35+.4*q
   for j,y in enumerate([1.05,0,-1.05]):g.add(chart(lambda x:component(x,j,tau),COLORS[j],cy=y*(1-q),h=1.8,opacity=1-.6*q))
   g.add(chart(lambda x:solution(x,tau),INK,cy=0,h=1.8,opacity=q))
  elif i==26:
   tau=.65+2.35*p;g.add(chart(solution,MUTED,cy=-.25,h=2,opacity=.25),chart(lambda x:solution(x,tau),INK,cy=-.25,h=2),color_rod(tau,y=1.2),tx(f't = {tau:.2f}',0,-1.8,24,c=YELLOW,w=3))
  elif i==27:
   g.add(chart(solution,INK,-4.5,0,3.2,1.5),arr([-2.65,0,0],[-1.95,0,0],PURPLE),arr([1.95,0,0],[2.65,0,0],GREEN),chart(lambda x:solution(x,1.7),INK,4.5,0,3.2,1.5))
   for j in range(3):g.add(chart(lambda x:component(x,j,1.7*p),COLORS[j],0,.85-j*.85,3.2,.8))
  elif i==28:g.add(chart(solution,INK,cy=.8,h=1.5),coefficient_bars(cy=-1.7,w=8))
  elif i==29:
   for j,c in enumerate(COLORS):g.add(chart(lambda x:component(x,j,1.5*p),c,cx=(j-1)*4.15,cy=.1,w=3.5,h=1.7),eq(rf'\times(-{int(K[j]**2)})',(j-1)*4.15,-1.4,30,c=YELLOW,w=3.5))
  elif i==31:
   if t<318:
    q=np.sin(np.pi*progress(t,312,318))
    for j,y in enumerate([1,0,-1]):g.add(chart(lambda x:component(x,j,progress(t,312,318)),COLORS[j],cy=y*q,h=1.8,opacity=.9))
   else:
    tau=1+2*progress(t,318,324);g.add(chart(lambda x:solution(x,tau),INK,cy=.1,h=2.0),color_rod(tau,y=1.55))
  return g
