"""166-second probability modelling portrait; seeded data and exact narration timing."""
import json,sys
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene,label
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
MODEL=np.load(HERE/'model_data.npz')
BLUE,PURPLE,ORANGE,GREEN,GOLD,RED,INK,MUTED='#42B8E8','#A18CF3','#EF946C','#65D6AC','#E8B45D','#EF7185','#E8EDF5','#8B9CB7'
D=float(MODEL['D']);TC=float(MODEL['Tc'])
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=45,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def density(x,t):return np.exp(-np.asarray(x)**2/(4*D*t))/np.sqrt(4*np.pi*D*t)
def density_axes(y=.3):return Axes(x_range=[-6,6,2],y_range=[0,.65,.2],x_length=6.8,y_length=3.2,tips=False,axis_config={'color':MUTED,'stroke_width':1.4}).move_to(UP*y)
def cloud(n=50,y=1):
 rng=np.random.default_rng(71);positions=rng.uniform([-3.2,-1.4],[3.2,1.4],(n,2));vel=rng.uniform(-1,1,(n,2));t=ValueTracker(0)
 dots=VGroup(*[Dot([a,b+y,0],radius=.04,color=BLUE) for a,b in positions])
 def update(m):
  z=positions+vel*t.get_value();z[:,0]=3.2-np.abs((z[:,0]+3.2)%12.8-6.4);z[:,1]=1.4-np.abs((z[:,1]+1.4)%5.6-2.8)
  for dot,(x,v) in zip(m,z):dot.move_to([x,v+y,0])
 dots.add_updater(update);return dots,t
class SpinGrid(VGroup):
 def __init__(self,states,tracker,center=(-1.9,.7,0),spacing=.28):
  super().__init__();self.states=states;self.tracker=tracker;self.current=-1;self.positions=[]
  for i in range(12):
   for j in range(12):
    pos=np.array(center)+np.array([(j-5.5)*spacing,(5.5-i)*spacing,0]);self.positions.append(pos)
    self.add(Arrow(pos+DOWN*.095,pos+UP*.095,buff=0,color=PURPLE,stroke_width=2,max_tip_length_to_length_ratio=.32))
  self.add_updater(self.refresh);self.refresh(self)
 def refresh(self,m,dt=0):
  k=min(len(self.states)-1,max(0,int(self.tracker.get_value())))
  if k==self.current:return
  self.current=k
  for a,pos,s in zip(self,self.positions,self.states[k].ravel()):
   direction=UP if s>0 else DOWN
   a.become(Arrow(pos-direction*.095,pos+direction*.095,buff=0,color=PURPLE if s>0 else ORANGE,stroke_width=2,max_tip_length_to_length_ratio=.32))
class ProbabilityScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.6)
  self.add(txt('MATHEMATICS  /  PROBABILITY & MODELS',7,17,MUTED))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]
  obs=[m for m in self.mobjects if m not in keep and m.get_center()[1]<6.5]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def brownian_plot(self,start=0,end=4,y=.4):
  times=MODEL['times'];values=MODEL['path'];mask=(times>=start)&(times<=end);tt=times[mask];xx=values[mask];stride=max(1,len(tt)//700);tt=tt[::stride];xx=xx[::stride]
  lo,hi=float(xx.min()),float(xx.max());pad=max(.02,(hi-lo)*.15)
  ax=Axes(x_range=[start,end,max((end-start)/4,.001)],y_range=[lo-pad,hi+pad,max((hi-lo)/4,.001)],x_length=6.6,y_length=3.3,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(UP*y)
  path=VMobject(color=GREEN,stroke_width=2).set_points_as_corners([ax.c2p(t,x) for t,x in zip(tt,xx)])
  return VGroup(ax,path)
class Shot01(ProbabilityScene):
 shot=0
 def s01(self):
  tank=Rectangle(width=7.2,height=3.4,color=BLUE,fill_opacity=.025).move_to(UP*1.1);self.show(tank)
  dots,t=cloud(65,1.1);self.add(dots);self.play(t.animate.set_value(3),run_time=4,rate_func=linear);self.to(5)
  selected=always_redraw(lambda:Circle(radius=.18,color=GOLD).move_to(dots[0]));self.add(selected);self.play(t.animate.set_value(6),run_time=3,rate_func=linear);self.to(9)
  self.show(eq(r'\vec x_i,\quad\vec v_i,\quad\vec F_i',-1.8,41,BLUE),txt('이 모든 충돌을 계산해야 할까?',-3.3,34),txt('입자 운동의 개념도',3.6,24,MUTED));self.play(t.animate.set_value(10),run_time=4,rate_func=linear);self.to(15)
class Shot02(ProbabilityScene):
 shot=1
 def s02(self):
  tank=Rectangle(width=7.2,height=2.2,color=BLUE).move_to(UP*2.65);self.add(tank,txt('수평 위치를 구간별로 집계',4.3,29,BLUE))
  t=ValueTracker(.08);dots=VGroup(*[Dot(radius=.033,color=BLUE) for _ in range(96)])
  def update(m):
   time=t.get_value()
   for i,dot in enumerate(m):dot.move_to([np.interp(time,MODEL['diff_times'],MODEL['diff'][i]),2.65+MODEL['diff_y'][i],0])
  dots.add_updater(update);self.add(dots)
  ax=Axes(x_range=[-3.5,3.5,1],y_range=[0,2,.5],x_length=6.8,y_length=2.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(DOWN*.8);self.add(ax)
  initial=np.array([np.interp(.08,MODEL['diff_times'],p) for p in MODEL['diff']]);edges=np.linspace(-3.5,3.5,19);counts,_=np.histogram(initial,edges);bars=VGroup()
  for c,a,b in zip(counts,edges[:-1],edges[1:]):
   h=c/(96*(b-a));rect=Rectangle(width=(b-a)*6.8/7*.9,height=max(.003,h*2.5/2),stroke_width=0,fill_color=BLUE,fill_opacity=.55).move_to(ax.c2p((a+b)/2,h/2));bars.add(rect)
  distribution_label=txt('표본의 위치 히스토그램',-2.7,26,MUTED);self.show(bars,distribution_label);self.to(20)
  curve=always_redraw(lambda:ax.plot(lambda x:density(x,t.get_value()),x_range=[-3.5,3.5,.04],color=BLUE,stroke_width=3))
  self.play(FadeOut(bars),Transform(distribution_label,txt('모형이 예측하는 이론 확률밀도',-2.7,26,BLUE)));self.add(curve);self.play(t.animate.set_value(.8),run_time=5,rate_func=linear);self.to(27)
  self.clear_body();ax=density_axes(.9);curve=ax.plot(lambda x:density(x,.8),x_range=[-6,6,.04],color=BLUE);self.show(ax,curve,txt('개별 운동의 추적 → 전체 분포의 분석',-1.6,31,GREEN),txt('이론 밀도 · 1차원 확산 · 경계 영향 무시',-3,24,MUTED));self.to(35)
class Shot03(ProbabilityScene):
 shot=2
 def s03(self):
  line=NumberLine(x_range=[0,2,.5],length=6.8,color=MUTED).move_to(UP*.8);dot=Dot(line.n2p(.2),color=BLUE)
  self.show(line,dot,txt('조건의 변화',-1,36));self.play(dot.animate.move_to(line.n2p(1)),run_time=2);self.to(39)
  self.show(DashedLine(line.n2p(1)+DOWN*.6,line.n2p(1)+UP*1.2,color=RED),eq(r'T_c',2.9,54,RED),txt('임계값 · Critical Point',-2.8,36,GOLD));self.to(41)
class Shot04(ProbabilityScene):
 shot=3
 def s04(self):
  magnet=VGroup(Rectangle(width=3.2,height=1.5,color=PURPLE,fill_opacity=.18).shift(LEFT*1.6),Rectangle(width=3.2,height=1.5,color=ORANGE,fill_opacity=.18).shift(RIGHT*1.6),txt('N',size=54,color=PURPLE,x=-1.6),txt('S',size=54,color=ORANGE,x=1.6)).shift(UP*1.6)
  self.show(magnet,txt('온도를 올리면 내부의 질서는?',-.7,36));self.to(45);self.clear_body()
  idx=ValueTracker(0);states=MODEL['spins'];temps=MODEL['temps'];grid=SpinGrid(states,idx);self.add(grid)
  self.show(eq(r's_i\in\{-1,+1\}',4.5,37,PURPLE),txt('2차원 이징 모형 · 외부 자기장 0',3.55,25,MUTED),txt('유한 격자의 두 자기 상태',-1.4,23,PURPLE,x=-1.9,width=3.6))
  m=DecimalNumber(states[0].mean(),num_decimal_places=2,font_size=33,color=PURPLE).move_to([-1.7,-2.15,0]);m.add_updater(lambda q:q.set_value(states[min(len(states)-1,int(idx.get_value()))].mean()));self.add(m,eq(r'm_N=',-2.15,27,PURPLE,x=-3.05,width=1.1))
  tempnum=DecimalNumber(temps[0]/TC,num_decimal_places=2,font_size=31,color=ORANGE).move_to([.55,2.85,0]);tempnum.add_updater(lambda q:q.set_value(np.interp(idx.get_value(),np.arange(len(temps)),temps)/TC));self.add(tempnum,eq(r'T/T_c=',2.85,27,ORANGE,x=-.75,width=1.7))
  ax=Axes(x_range=[0,1.8,.5],y_range=[0,1.1,.5],x_length=3.1,y_length=2.45,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([2,.55,0])
  def spontaneous(r):return (max(0,1-np.sinh(2/(TC*max(r,.05)))**(-4)))**.125 if r<1 else 0
  vals=np.r_[np.linspace(.05,.99,160),np.linspace(.99,1,180),np.linspace(1,1.8,60)]
  curve=VMobject(color=GOLD,stroke_width=2.5).set_points_as_corners([ax.c2p(r,spontaneous(r)) for r in vals]);self.add(ax,curve,DashedLine(ax.c2p(1,0),ax.c2p(1,1),color=RED),txt('T_c',-1.05,22,RED,x=2.15),txt('열역학적 극한의 자발 자화',-1.7,21,GOLD,x=2,width=3.6))
  marker=always_redraw(lambda:Dot(ax.c2p(np.interp(idx.get_value(),np.arange(len(temps)),temps)/TC,spontaneous(np.interp(idx.get_value(),np.arange(len(temps)),temps)/TC)),color=GOLD,radius=.055));self.add(marker)
  self.to(49);self.play(idx.animate.set_value(5),run_time=4,rate_func=linear);self.to(54)
  self.play(idx.animate.set_value(24),run_time=6,rate_func=linear);self.to(60)
  self.play(idx.animate.set_value(45),run_time=5,rate_func=linear);self.to(65)
  self.show(txt('개별 자기 상태는 남고, 전체 정렬은 사라진다',-3.1,29,GREEN),txt('유한 표본 m_N은 0 부근에서 계속 요동',-4.3,24,MUTED));self.play(idx.animate.set_value(len(states)-1),run_time=4,rate_func=linear);self.to(71)
class Shot05(ProbabilityScene):
 shot=4
 def s05(self):
  self.show(txt('상전이 · Phase Transition',3.7,39,GOLD),eq(r'T<T_c\quad\longrightarrow\quad T>T_c',1.6,46),txt('거시적 정렬',-.2,31,PURPLE,x=-2),txt('자발 자화 소멸',-.2,31,ORANGE,x=2),txt('조건의 변화 → 거시적 상태의 변화',-2.4,33,GREEN),txt('엄밀한 상전이는 열역학적 극한의 성질',-4,23,MUTED));self.to(77)
  self.clear_body();box=Rectangle(width=6.8,height=3.4,color=BLUE).move_to(UP*1)
  rng=np.random.default_rng(81);xy=rng.uniform([-2.8,-.4],[2.8,.2],(48,2));dots=VGroup(*[Dot([x,y,0],radius=.045,color=BLUE) for x,y in xy]);self.show(box,dots,txt('액체 → 기체',-1.8,38,GOLD),txt('온도와 압력에 따라 달라지는 상태',-3.5,27,MUTED))
  targets=rng.uniform([-2.8,-.4],[2.8,2.4],(48,2));self.play(*[d.animate.move_to([x,y,0]) for d,(x,y) in zip(dots,targets)],run_time=2);self.to(81)
  self.clear_body();self.show(txt('자석의 자기 상태',2.8,37,PURPLE),txt('액체·기체의 분자',1.2,37,BLUE),eq(r'\Downarrow',-.1,48),txt('개별 요소들의 상호작용',-1.5,35),txt('집단적인 성질',-3.2,40,GREEN));self.to(86)
class Shot06(ProbabilityScene):
 shot=5
 def s06(self):
  self.show(txt('충돌 · 힘 · 속도 · 관성',3.6,37,BLUE),txt('유체의 움직임 · 온도',2.2,35,ORANGE),eq(r'\Downarrow',.7,47),txt('Mathematical Model',-.9,38,GREEN));self.to(90)
  self.show(txt('무엇을 남기고 무엇을 생략할까?',-2.5,34,GOLD),txt('분석 목적에 맞는 통계적 성질을 선택',-4,27,MUTED));self.to(96)
  self.clear_body();self.show(txt('브라운 운동',1.8,53,GREEN),txt('Brownian Motion',.4,33,MUTED));self.to(98)
class Shot07(ProbabilityScene):
 shot=6
 def s07(self):
  box=Rectangle(width=7,height=3.6,color=BLUE).move_to(UP*1.1);dots,t=cloud(55,1.1);path=MODEL['walk'];k=ValueTracker(0)
  big=always_redraw(lambda:Dot(np.r_[path[min(int(k.get_value()),len(path)-1)]+[0,1.1],0],radius=.13,color=GOLD));trace=TracedPath(big.get_center,stroke_color=GOLD,stroke_width=2)
  self.add(box,dots,big,trace);self.show(txt('주변 분자와의 충돌 · 개념도',-2,29,MUTED));self.play(t.animate.set_value(5),k.animate.set_value(299),run_time=4,rate_func=linear);self.to(103)
  self.clear_body();g=self.brownian_plot();self.show(g,eq(r'X(t)',3.8,46,GREEN),txt('시간 t →',-1.8,25,MUTED),txt('불규칙하지만 순간이동하지 않는 경로',-3.1,31),txt('독립 정규 증가량을 누적한 유한 해상도 근사',-4.3,22,MUTED));self.to(110)
class Shot08(ProbabilityScene):
 shot=7
 def s08(self):
  g=self.brownian_plot();interval=txt('0 ≤ t ≤ 4',-2.1,27,MUTED);self.show(g,txt('같은 경로의 시간 구간을 확대',3.9,32,GREEN),interval);self.to(112)
  self.play(Transform(g,self.brownian_plot(.9,1.1)),Transform(interval,txt('0.9 ≤ t ≤ 1.1',-2.1,27,MUTED)),run_time=.8);self.to(114)
  self.play(Transform(g,self.brownian_plot(.99,1.01)),Transform(interval,txt('0.99 ≤ t ≤ 1.01',-2.1,27,MUTED)),run_time=.8);self.show(txt('확률 1로, 모든 지점에서 미분 불가능',-3.2,30,GOLD),txt('이상적 브라운 경로의 성질 · 화면은 선분 근사',-4.3,22,MUTED));self.to(116)
  self.clear_body();self.show(eq(r'\Delta X\sim\mathcal N(0,2D\Delta t)',3.8,44,GREEN))
  ax=Axes(x_range=[0,4,1],y_range=[-5,5,1],x_length=6.6,y_length=3.3,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(UP*.7);self.add(ax);rng=np.random.default_rng(110)
  for i in range(5):
   vals=np.r_[0,np.cumsum(rng.normal(0,np.sqrt(2*D*4/400),400))];curve=VMobject(color=GREEN,stroke_width=1.5,stroke_opacity=.7).set_points_as_corners([ax.c2p(t,x) for t,x in zip(np.linspace(0,4,401),vals)])
   self.show(curve,run_time=.4)
  self.show(txt('경로는 달라도 증가량의 통계 규칙은 같다',-2.6,31,GREEN));self.to(123)
  self.clear_body();self.show(txt('실제 입자 운동',3,39,BLUE),txt('충돌 · 관성 · 유체와의 상호작용',1.8,27),eq(r'\ne',.3,62,RED),txt('이상적 브라운 운동',-1.2,39,GREEN),txt('적절한 시간·공간 척도에서 유효한 모형',-2.7,27),txt('모든 미시적 세부를 그대로 재현하지 않는다',-4.1,24,MUTED));self.to(128)
class Shot09(ProbabilityScene):
 shot=8
 def s09(self):
  self.show(eq(r'X_0=0,\quad X_t\sim\mathcal N(0,2Dt)',4,41,GREEN));ax=density_axes(.6);t=ValueTracker(1)
  curve=always_redraw(lambda:ax.plot(lambda x:density(x,t.get_value()),x_range=[-6,6,.04],color=BLUE,stroke_width=3));self.add(ax,curve)
  self.show(txt('많은 경로의 같은 시각 위치 → 확률분포',-1.8,30),txt('1차원 · 표류 없음 · 이상적 확산',-3.3,25,MUTED));self.to(134)
  self.play(t.animate.set_value(4),run_time=5,rate_func=linear);self.show(txt('넓어지고 낮아져도 전체 면적은 1',-4.4,24,GOLD));self.to(140)
class Shot10(ProbabilityScene):
 shot=9
 def s10(self):
  self.show(eq(r'\operatorname{Var}(X_t)=2Dt',4.2,48,GOLD),eq(r't\to4t\quad\Rightarrow\quad2Dt\to8Dt',3.05,35,GOLD))
  ax=density_axes(.15);narrow=ax.plot(lambda x:density(x,1),x_range=[-6,6,.04],color=BLUE,stroke_width=3);wide=ax.plot(lambda x:density(x,4),x_range=[-6,6,.04],color=GOLD,stroke_width=3)
  self.add(ax,narrow,wide);note=txt('분산은 시간에 비례',-2.1,31,GOLD);self.show(txt('t',1.8,26,BLUE,x=-2.8),txt('4t',1.8,26,GOLD,x=2.8),note);self.to(145);self.play(FadeOut(note),run_time=.3)
  sigma=np.sqrt(2*D)
  bar1=DoubleArrow(ax.c2p(-sigma,0)+DOWN*.45,ax.c2p(sigma,0)+DOWN*.45,buff=0,color=BLUE,stroke_width=3)
  bar2=DoubleArrow(ax.c2p(-2*sigma,0)+DOWN*.95,ax.c2p(2*sigma,0)+DOWN*.95,buff=0,color=GOLD,stroke_width=3)
  self.show(bar1,bar2,eq(r'\sigma(t)=\sqrt{2Dt},\quad\sigma(4t)=2\sigma(t)',-3.7,37,GREEN));self.to(150)
  self.clear_body();self.show(txt('개별 경로의 방향은 몰라도',2.6,38,BLUE),txt('분포가 얼마나 퍼질지는 예측한다',.5,37,GREEN),eq(r't\times4\quad\Rightarrow\quad\sigma\times2',-1.5,49,GOLD));self.to(154)
class Shot11(ProbabilityScene):
 shot=10
 def s11(self):
  self.show(txt('입자들 → 확률분포',3.6,36,BLUE),txt('자기 상태들 → 전체 자화',1.9,36,PURPLE),txt('무작위 경로 → 분산의 법칙',.2,36,GREEN),eq(r'\operatorname{Var}(X_t)=2Dt',-1.5,46,GOLD),txt('무엇을 남기고, 무엇을 생략할 것인가?',-3.5,30));self.to(160)
  self.clear_body();self.show(txt('복잡한 현상에서',3,44),txt('중요한 구조를 찾아내다',1.4,44,GREEN),txt('전체적인 행동을 이해하는 수학적 모형',-1,32),txt('확률과 수학적 모형',-3,32,MUTED));self.to(166)
