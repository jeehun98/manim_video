"""145-second concept-map-led analysis, PDE and dynamics portrait."""
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
MODEL=np.load(HERE/'dynamics_data.npz')
BLUE,PURPLE,GREEN,GOLD,RED,INK,MUTED='#42B8E8','#A18CF3','#65D6AC','#E8B45D','#EF7185','#E8EDF5','#8B9CB7'
HEAT=r'\frac{\partial T}{\partial t}=\alpha\frac{\partial^2T}{\partial x^2}'
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=43,color=INK,width=7.3,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
class ConceptMap(VGroup):
 def __init__(self,state='analysis',large=False):
  super().__init__();self.large=large
  if large:
   outer=RoundedRectangle(width=7.4,height=4.8,corner_radius=.3,color=BLUE).move_to(UP*.4)
   self.add(outer,txt('해석학',2.35,35,BLUE,x=-2.5,width=2))
   positions=[(-1.85,1.05),(1.85,1.05),(0,-1.05)];heights=[1.5,1.5,1.1];widths=[3.2,3.2,6.6];sizes=[28,28,27]
  else:
   outer=RoundedRectangle(width=7.6,height=2.45,corner_radius=.24,color=BLUE,stroke_width=1.6).move_to(UP*6.1)
   self.add(outer,txt('해석학',7.0,22,BLUE,x=-2.9,width=1.6))
   positions=[(-1.85,6.23),(1.85,6.23),(0,5.3)];heights=[.8,.8,.65];widths=[3.2,3.2,6.6];sizes=[19,19,20]
  labels=['미분 · 적분\n극한 · 편미분','미분방정식의 해석\nODE · PDE','동역학적 관점 · 시간 변화와 장기 행동']
  self.parts=[]
  for i,((x,y),h,w,sz,text,color) in enumerate(zip(positions,heights,widths,sizes,labels,[BLUE,PURPLE,GREEN])):
   box=RoundedRectangle(width=w,height=h,corner_radius=.15,stroke_color=color,stroke_width=1.5,fill_color=color,fill_opacity=.07).move_to([x,y,0])
   if i==2:box=DashedVMobject(box,num_dashes=40)
   group=VGroup(box,txt(text,y,sz,color,x=x,width=w-.25));self.parts.append(group);self.add(group)
  a,b,c=positions
  self.add(Line([a[0]+1.6,a[1],0],[b[0]-1.6,b[1],0],color=MUTED,stroke_width=1.4))
  self.add(Arrow([b[0],b[1]-heights[1]/2,0],[b[0],c[1]+heights[2]/2,0],buff=.01,color=GREEN,stroke_width=1.5,max_tip_length_to_length_ratio=.4))
  self.activate(state)
 def activate(self,state):
  active={'analysis':[0,1,2],'derivative':[0],'partial':[0],'pde':[1],'dynamics':[2],'properties':[1,2],'overview':[0,1,2]}[state]
  for i,g in enumerate(self.parts):
   g[0].set_stroke(opacity=1 if i in active else .4).set_fill(opacity=.10 if i in active else .025)
   g[1].set_opacity(1 if i in active else .65)
  return self

def gaussian(x,t):return np.exp(-np.asarray(x)**2/(1+t))/np.sqrt(1+t)
def finite_heat(x,t):return 50+30*np.cos(np.pi*np.asarray(x))*np.exp(-.1*np.pi**2*t)
THERMAL_PALETTE=color_gradient([BLUE,RED],101)
def thermal_color(value):return THERMAL_PALETTE[int(np.clip(value,0,1)*100)]
def heat_display(time,finite=False,y=.5):
 if finite:
  ax=Axes(x_range=[0,1,.25],y_range=[0,100,25],x_length=6.6,y_length=2.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to([0,y-.8,0]);xs=np.linspace(0,1,60);fun=finite_heat
 else:
  ax=Axes(x_range=[-6,6,2],y_range=[0,1.1,.5],x_length=6.6,y_length=2.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to([0,y-.8,0]);xs=np.linspace(-6,6,60);fun=gaussian
 pieces=VGroup(*[Rectangle(width=6.6/60+.005,height=.4,stroke_width=0,fill_opacity=1).move_to([-3.3+(i+.5)*6.6/60,y+1.05,0]) for i in range(60)])
 def recolor(m):
  vals=fun(xs,time.get_value());vals=vals/100 if finite else vals
  for cell,v in zip(m,vals):cell.set_fill(thermal_color(v))
 pieces.add_updater(recolor);recolor(pieces)
 curve=always_redraw(lambda:ax.plot(lambda x:fun(x,time.get_value()),x_range=[xs[0],xs[-1],(xs[-1]-xs[0])/220],color=RED,stroke_width=3))
 return VGroup(ax,pieces,curve)
def lorenz_thumbnail(y=0,width=6.2,height=2.9):
 a=MODEL['lorenz'][0][::10];xy=a[:,[0,2]];lo=np.min(MODEL['lorenz'][:,:,[0,2]],axis=(0,1));hi=np.max(MODEL['lorenz'][:,:,[0,2]],axis=(0,1))
 points=np.c_[((xy-lo)/(hi-lo)-.5)*[width,height],np.zeros(len(xy))];points[:,1]+=y
 return VMobject(color=GREEN,stroke_width=1.4).set_points_as_corners(points)
class AnalysisScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup()
  keep=[self.title,self.caption,self.caption_panel]
  self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*4.05)
  state=['analysis','derivative','partial','pde','dynamics','dynamics','properties','properties','overview'][self.shot]
  self.map=ConceptMap(state).set_z_index(25)
  self.map_note=txt('영상용 개념 흐름 · 엄밀한 학문 분류 아님',4.57,17,MUTED).set_z_index(25)
  self.add(self.map,self.map_note)
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.map,self.map_note]
  obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
class Shot01(AnalysisScene):
 shot=0
 def s01(self):
  t=ValueTracker(0);line=Line([-3,2.3,0],[3,2.3,0],color=MUTED);dot=always_redraw(lambda:Dot([-2.7+1.1*t.get_value(),2.3,0],color=BLUE))
  wave=always_redraw(lambda:FunctionGraph(lambda x:.3*np.sin(2*x-t.get_value()),x_range=[-3,3],color=GREEN).shift(DOWN*.6));self.add(line,dot,wave,txt('물체의 운동',3.15,26,BLUE),txt('파동',-1.4,26,GREEN));self.play(t.animate.set_value(1.4),run_time=2,rate_func=linear)
  self.show(txt('현상은 달라도, 공통된 질문',.8,33),eq(r'\frac{dx}{dt}\qquad\frac{\partial T}{\partial t}\qquad\frac{\partial u}{\partial t}',-2.8,42,PURPLE));self.play(t.animate.set_value(4.3),run_time=5,rate_func=linear);self.to(10)
  self.clear_body();self.show(txt('해석학 · Analysis',2,47,BLUE),txt('극한 · 미분 · 적분 · 연속성',-.1,36),txt('연속적인 변화와 그 성질을 연구한다',-2.2,30));self.to(14)
class Shot02(AnalysisScene):
 shot=1
 def s02(self):
  ax=Axes(x_range=[0,2.5,.5],y_range=[0,6,2],x_length=6.2,y_length=3.1,tips=False,axis_config={'color':MUTED,'stroke_width':1.3}).move_to(UP*.5);curve=ax.plot(lambda t:t*t,x_range=[0,2.4],color=BLUE);pos=ValueTracker(.3)
  dot=always_redraw(lambda:Dot(ax.c2p(pos.get_value(),pos.get_value()**2),color=BLUE));self.show(ax,curve,eq(r'x(t)=t^2',3.1,43,BLUE),txt('시간 t → 위치 x(t)',-2,28,MUTED));self.add(dot);self.to(19)
  self.play(pos.animate.set_value(1),run_time=2);self.to(22)
  h=ValueTracker(1.1);other=always_redraw(lambda:Dot(ax.c2p(1+h.get_value(),(1+h.get_value())**2),color=GOLD));sec=always_redraw(lambda:Line(ax.c2p(.35,1+(2+h.get_value())*(.35-1)),ax.c2p(2,1+(2+h.get_value())),color=GOLD))
  self.add(other,sec);fraction=eq(r'\frac{x(t+\Delta t)-x(t)}{\Delta t}',-3.1,40,GOLD);self.show(fraction);self.play(h.animate.set_value(.25),run_time=5);self.to(29)
  self.play(h.animate.set_value(.02),run_time=2)
  self.play(Transform(fraction,eq(r'\frac{dx}{dt}=\lim_{\Delta t\to0}\frac{x(t+\Delta t)-x(t)}{\Delta t}',-3.1,37,GREEN)),run_time=.6);self.to(34)
  self.show(eq(r't=1:\quad v=2',-4.25,32,GREEN));self.to(37)
class Shot03(AnalysisScene):
 shot=2
 def s03(self):
  self.show(eq(r'x(t)',2,57,BLUE,x=-1.9),eq(r'T(x,t)',2,57,RED,x=1.9),txt('시간',.7,30,x=-1.9),txt('위치와 시간',.7,30,x=1.9));self.to(41)
  self.clear_body();time=ValueTracker(0);g=heat_display(time,finite=True,y=.5);self.show(g,eq(r'T=T(x,t)',3.1,45,RED),txt('위치 x와 시간 t에 의존',-2.8,30));self.play(time.animate.set_value(.8),run_time=4,rate_func=linear);self.to(47)
  self.show(txt('위치를 바꾸기 / 시간를 바꾸기',-4.1,26,MUTED));self.to(50)
  self.clear_body();self.show(eq(r'\frac{\partial T}{\partial t}',2,65,GOLD,x=-1.9),eq(r'\frac{\partial T}{\partial x}',2,65,BLUE,x=1.9),txt('시간 방향의 변화',.3,29,GOLD,x=-1.9,width=3.5),txt('공간 방향의 변화',.3,29,BLUE,x=1.9,width=3.5),txt('위치 x 고정',-1,28,x=-1.9),txt('시간 t 고정',-1,28,x=1.9),txt('한 변수만 바꾸어 살펴본다',-3.2,30));self.to(56)
  self.clear_body();self.map.activate('pde');self.show(eq(HEAT,1.6,55,PURPLE),txt('편미분방정식 · PDE',-.6,39,PURPLE),txt('여러 변화율을 하나의 법칙으로 연결',-2.5,31));self.to(61)
class Shot04(AnalysisScene):
 shot=3
 def s04(self):
  self.show(eq(HEAT,2.1,55,PURPLE),txt('열방정식 · Heat Equation',.2,38));self.to(63)
  self.clear_body();time=ValueTracker(0);g=heat_display(time,y=.5);self.add(g)
  self.show(eq(HEAT,3.15,42,PURPLE),txt('무한히 긴 막대 · 가우시안 초기 분포',2.2,25,MUTED),txt('봉우리의 공간적 굽음 → 온도의 시간 변화',-2.9,29),eq(r'\partial_{xx}T(0,t)<0\quad\Rightarrow\quad\partial_tT(0,t)<0',-4.1,30,GREEN));self.to(69)
  self.play(time.animate.set_value(7),run_time=6,rate_func=linear);self.to(76)
class Shot05(AnalysisScene):
 shot=4
 def s05(self):
  self.show(eq(r'T(x,0)\to T(x,\Delta t)\to T(x,2\Delta t)\to\cdots',2.5,34,PURPLE),txt('시간이 아주 오래 흐르면?',.4,42,GREEN));self.to(80)
  self.show(eq(r't=0\ \to\ 10\ \to\ 100\ \to\ \infty',-2,42,GOLD));self.to(83)
  self.clear_body();time=ValueTracker(0);g=heat_display(time,finite=True,y=.5);self.add(g)
  self.show(txt('새 조건 · 단열된 유한한 막대',3.15,29,GOLD),eq(r'\partial_xT(0,t)=\partial_xT(1,t)=0',2.25,30,MUTED),eq(r'T(x,t)\longrightarrow T_{\rm eq}=50',-2.8,39,GREEN),txt('초기 평균 온도를 보존하며 평탄해진다',-4.1,25,MUTED));self.play(time.animate.set_value(6),run_time=4,rate_func=linear);self.to(89)
  self.clear_body();self.show(ConceptMap('dynamics',large=True),txt('시간 변화도 동역학적으로 연구할 수 있다',-2.9,29,GREEN),txt('연구의 연결 · 포함관계를 뜻하는 화살표 아님',-4.1,23,MUTED));self.to(96)
class Shot06(AnalysisScene):
 shot=5
 def s06(self):
  self.show(eq(r'S_0\to S_1\to S_2\to\cdots',2.3,50,GREEN),txt('다음 순간을 넘어',.3,40));self.to(100)
  self.show(txt('장기 행동 · Long-term behavior',-1.5,34,GOLD),txt('동역학은 ODE · PDE · 이산계도 다룬다',-3.3,26,MUTED));self.to(104)
  self.clear_body();ax1=Axes(x_range=[0,6,2],y_range=[-1.2,1.2,1],x_length=3.1,y_length=2.4,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to([-1.9,.8,0]);ax2=ax1.copy().move_to([1.9,.8,0])
  self.show(ax1,ax2,txt('평형에 접근',2.7,30,BLUE,x=-1.9),txt('주기적으로 반복',2.7,30,GOLD,x=1.9),eq(r'\dot u=-u',-1.3,35,BLUE,x=-1.9),eq(r'\ddot u=-u',-1.3,35,GOLD,x=1.9));self.play(Create(ax1.plot(lambda t:np.exp(-t),x_range=[0,6],color=BLUE)),Create(ax2.plot(np.cos,x_range=[0,6],color=GOLD)),run_time=3);self.to(110)
  self.clear_body();self.show(eq(r'\dot x=10(y-x),\quad\dot y=x(28-z)-y',3.1,29,GREEN),eq(r'\dot z=xy-\tfrac83z',2.45,30,GREEN),txt('같은 Lorenz 방정식 · 초기 x만 10⁻⁵ 차이',1.8,24,MUTED))
  values=MODEL['lorenz'];lo=np.min(values[:,:,[0,2]],axis=(0,1));hi=np.max(values[:,:,[0,2]],axis=(0,1));k=ValueTracker(2)
  for i,c in [(0,BLUE),(1,GOLD)]:
   def path_at(i=i,c=c):
    end=max(2,int(k.get_value()));xy=values[i,:end:4][:,[0,2]];points=np.c_[((xy-lo)/(hi-lo)-.5)*[6.5,2.9],np.zeros(len(xy))];points[:,1]-=.25
    return VGroup(VMobject(color=c,stroke_width=1.8).set_points_as_corners(points),Dot(points[-1],radius=.06,color=c))
   self.add(always_redraw(path_at))
  self.show(txt('x-z 평면 투영 · 수치해',-2.1,22,MUTED),txt('작은 초기 차이 → 큰 장기적 차이',-3.1,31,GREEN),txt('결정론적 규칙 · 무작위 운동과는 구별',-4.3,23,MUTED),run_time=.3)
  self.play(k.animate.set_value(values.shape[1]-1),run_time=4.5,rate_func=linear);self.to(116)
class Shot07(AnalysisScene):
 shot=6
 def s07(self):
  self.show(txt('평형',2.9,32,BLUE,x=-2.4),txt('주기',2.9,32,GOLD,x=0),txt('카오스',2.9,32,GREEN,x=2.4))
  chaos=lorenz_thumbnail(1,width=2,height=1.6).shift(RIGHT*2.4)
  a=FunctionGraph(lambda x:.6*np.exp(-2*(x+1)),x_range=[-1,1],color=BLUE).shift(LEFT*2.4+UP*.7);b=FunctionGraph(lambda x:.6*np.cos(5*x),x_range=[-1,1],color=GOLD).shift(UP*.7)
  self.show(a,b,chaos,txt('순간의 규칙과 장기 행동은 다른 질문',-1.6,34),txt('서로 다른 예시 시스템의 행동',-3,25,MUTED));self.to(123)
  self.clear_body();self.map.activate('properties');self.show(txt('방정식의 해는 어떤 성질을 가질까?',1.7,39,PURPLE),txt('그 분석에도 해석학적 도구가 필요하다',-.4,32),eq(HEAT,-2.3,42,PURPLE));self.to(127)
class Shot08(AnalysisScene):
 shot=7
 def s08(self):
  for title,question,y,c in [('존재성','해가 존재하는가?',2.7,BLUE),('유일성','초기조건으로 해가 하나로 정해지는가?',.8,PURPLE),('안정성','작은 변화에 얼마나 민감한가?',-1.1,GOLD),('장기 거동','오랜 시간 뒤 어떤 상태에 접근하는가?',-3,GREEN)]:
   self.show(txt(title,y,34,c),txt(question,y-.7,26),run_time=.6)
  self.to(135)
class Shot09(AnalysisScene):
 shot=8
 def s09(self):
  big=ConceptMap('overview',large=True);self.show(big,eq(r'\frac{dx}{dt}\qquad\frac{\partial T}{\partial t}=\alpha\frac{\partial^2T}{\partial x^2}',-3.2,36,PURPLE),txt('순간의 변화 → 해의 변화 → 장기 행동',-4.3,25,GREEN));self.to(139)
  self.clear_body();self.show(txt('순간의 변화에서',2.1,43,BLUE),txt('장기적인 행동까지',.5,43,GREEN),txt('해석학은 변화가 만드는 구조를 연구한다',-1.6,31),txt('미분 · 미분방정식 · 동역학적 관점',-3.4,27,MUTED));self.to(143)
  self.clear_body();self.show(txt('순간의 변화가 만드는 미래',.8,43,GREEN));self.to(145)
