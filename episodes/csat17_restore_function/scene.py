"""Twenty-six independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT17_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT17_PREVIEW')=='1' else 1080
config.background_color='#0B1020'
WARN='#FB923C'
INK='#F8FAFC';BASE='#38BDF8';EXP='#FACC15';REL='#C084FC';RESULT='#4ADE80';MUTED='#94A3B8'
def tx(s,x=0,y=0,size=28,color=INK,width=14):return text(s,x,y,size,color,width)
def eq(s,x=0,y=.4,size=64,color=INK,width=13):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def card(s,x,y,color=REL,width=4.5):
 return VGroup(RoundedRectangle(width=width,height=1.1,corner_radius=.15,stroke_color=color,stroke_width=1.4,fill_color=color,fill_opacity=.06).move_to([x,y,0]),eq(s,x,y,40,color,width-.4))
class RestoreShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.17',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('도함수와 원래 함수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
  self.add(Line([-7.15,3.55,0],[7.15,3.55,0],color=MUTED,stroke_opacity=.25,stroke_width=1))
  self.add(tx(self.info['title'],y=2.95,size=32))
  self.caption=VGroup().set_z_index(50);self.add(self.caption)
  self.caption.add_updater(self.update_caption);self.update_caption(self.caption)
  self.bound_checks=0
 def update_caption(self,m,dt=0):
  now=self.offset+self.time;i=bisect_right([s['start'] for s in DATA['sentences']],now+1e-6)-1
  if i==self.caption_index:return
  self.caption_index=i
  lines=textwrap.wrap(DATA['sentences'][i]['caption'],width=53,break_long_words=False,break_on_hyphens=False)
  new=tx('\n'.join(lines),y=-3.5,size=28,width=14.1)
  if new.height>1.1:new.scale_to_fit_height(1.1)
  assert new.get_top()[1]<-2.8 and new.get_bottom()[1]>-4.2
  m.become(new).set_z_index(50)
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for m in self.mobjects:
   if m is self.caption or m.width<.001:continue
   assert m.get_left()[0]>=-7.8 and m.get_right()[0]<=7.8,(self.shot,self.time,'x')
   assert m.get_bottom()[1]>-2.65 and m.get_top()[1]<4.4,(self.shot,self.time,'y',m.get_bottom())
  self.bound_checks+=1
 def to(self,t):
  frames=round((t-self.offset-self.time)*30)
  if frames<0:raise RuntimeError(f'Overrun {self.offset+self.time} > {t}')
  if frames:self.wait(frames/30-1e-8)
 def show(self,*ms,rt=.6):self.play(*[FadeIn(m,shift=UP*.08) for m in ms],run_time=rt)
 def morph(self,a,b,rt=.7):self.play(ReplacementTransform(a,b),run_time=rt);return b
 def note(self,s,color=MUTED):
  new=tx('\n'.join(textwrap.wrap(s,width=27,break_long_words=False)),x=-3.7,y=-1.9,size=24,color=color,width=6.1) if hasattr(self,'ax') else tx(s,y=-1.95,size=26,color=color)
  if new.height>.8:new.scale_to_fit_height(.8)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')








 def change(self,m,s,t=None,y=.5,color=REL,size=72,x=0,width=13):
  if t is not None:self.to(t)
  n=eq(s,x,y,size,color,width);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def left(self,s,y=.6,size=53,color=INK):return eq(s,-3.7,y,size,color,width=6.1)
 @staticmethod
 def F(x,c=3):return 2*x**3+5*x+c
 @staticmethod
 def D(x):return 6*x*x+5
 def tangent(self,ax,x,c,color=EXP):
  return Line(ax.c2p(x-.24,RestoreShot.F(x,c)-.24*RestoreShot.D(x)),ax.c2p(x+.24,RestoreShot.F(x,c)+.24*RestoreShot.D(x)),color=color,stroke_width=2.1)
 def original(self,c=0,family=False,points=False,label='원래 함수의 그래프'):
  ax=Axes(x_range=[-1.2,1.2,1],y_range=[-10,12,5],x_length=6.15,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax;self.constant=ValueTracker(c)
  self.add(ax,*[eq(str(v),*(ax.c2p(v,0)+DOWN*.27)[:2],size=22,color=MUTED) for v in [-1,0,1]],tx(label,3.4,2.2,22,MUTED,width=6.5))
  if family:self.add(ax.plot(lambda x:RestoreShot.F(x,0),x_range=[-1,1,.025],color=BASE,stroke_width=2,stroke_opacity=.55))
  self.add(always_redraw(lambda:ax.plot(lambda x:RestoreShot.F(x,self.constant.get_value()),x_range=[-1,1,.025],color=REL,stroke_width=2.6,use_smoothing=False)),always_redraw(lambda:Dot(ax.c2p(0,self.constant.get_value()),radius=.065,color=EXP)))
  if points:self.add(Dot(ax.c2p(0,3),radius=.075,color=EXP),eq('(0,3)',*(ax.c2p(0,3)+LEFT*.72+UP*.25)[:2],size=27,color=EXP))
  return ax
 def derivative(self,fill=False):
  ax=Axes(x_range=[-.15,1.15,.5],y_range=[0,12,2],x_length=6.15,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  self.add(ax,ax.plot(lambda x:6*x*x+5,x_range=[0,1,.012],color=BASE,stroke_width=2.6),tx('도함수 y = 6x² + 5',3.4,2.2,23,BASE,width=6.5),*[eq(str(v),*(ax.c2p(v,0)+DOWN*.26)[:2],size=23,color=MUTED) for v in [0,1]],eq('5',*(ax.c2p(0,5)+LEFT*.25)[:2],size=22,color=MUTED))
  self.edge=ValueTracker(1 if fill else 0)
  def area():
   xs=np.linspace(0,self.edge.get_value(),65);return Polygon(ax.c2p(0,0),*[ax.c2p(x,6*x*x+5) for x in xs],ax.c2p(self.edge.get_value(),0),stroke_width=0,fill_color=BASE,fill_opacity=.3).set_z_index(-1)
  self.add(always_redraw(area));return ax
 def difference(self,ax):
  self.add(Dot(ax.c2p(0,3),radius=.07,color=EXP),Dot(ax.c2p(1,10),radius=.07,color=RESULT),eq('(0,3)',*(ax.c2p(0,3)+LEFT*.7+UP*.25)[:2],size=26,color=EXP),eq('(1,10)',*(ax.c2p(1,10)+LEFT*.75+UP*.25)[:2],size=26,color=RESULT))
  ar=DoubleArrow(ax.c2p(.8,3),ax.c2p(.8,10),buff=0,color=EXP,stroke_width=2,tip_length=.1);self.add(ar,eq('7',*(ax.c2p(.8,6.5)+LEFT*.3)[:2],size=41,color=EXP));return ar
 def s01(self):
  n=tx('17',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  self.show(eq("f'(x)=6x^2+5",y=1.4,size=91,color=BASE),rt=1);self.to(4)
  self.show(eq('f(0)=3',y=-.05,size=83,color=REL));self.to(6);self.show(eq('f(1)=?',y=-1.65,size=82,color=EXP))
 def s02(self):
  ax=self.original(3,label='개념 설명용 곡선 · 함수식은 아직 미공개');self.to(13)
  t=ValueTracker(-.65);self.add(always_redraw(lambda:Dot(ax.c2p(t.get_value(),RestoreShot.F(t.get_value())),radius=.07,color=EXP)),always_redraw(lambda:self.tangent(ax,t.get_value(),3)))
  self.add(self.left("f'(x)",y=1.2,size=101,color=BASE));self.play(t.animate.set_value(.7),run_time=4,rate_func=linear);self.note('각 지점에서의 순간 변화율 = 접선의 기울기')
 def s03(self):
  self.add(eq(r'f(x)\ \longrightarrow\ f\prime(x)',y=1.25,size=84,color=BASE),tx('미분',y=2.1,size=28,color=BASE));self.to(23)
  self.show(eq(r'f\prime(x)\ \longrightarrow\ f(x)',y=-.65,size=84,color=REL),tx('적분 · 미분의 반대 과정',y=-1.95,size=29,color=REL))
 def s04(self):
  m=eq("f'(x)=6x^2+5",size=100,color=BASE);self.add(m);self.to(31)
  self.change(m,r'f(x)=\int(6x^2+5)\,dx',size=86,color=REL)
 def s05(self):
  m=eq(r'\int x^2\,dx=\frac{x^3}{3}+C',size=90,color=REL);self.add(m);m=self.change(m,r'\int6x^2\,dx=6\cdot\frac{x^3}{3}+C',37,size=82);self.change(m,r'\int6x^2\,dx=2x^3+C',39,size=90,color=RESULT)
 def s06(self):
  self.add(eq(r'\int5\,dx=5x+C',y=1.35,size=88,color=BASE));self.to(44)
  self.show(eq('f(x)=2x^3+5x+C',y=-.55,size=89,color=REL));self.note('상수 C를 더한 모든 함수가 같은 도함수를 갖는다',EXP)
 def s07(self):
  self.add(eq('f(x)=2x^3+5x+C',y=1.35,size=86,color=REL));self.to(51);self.show(eq('C=?',y=-.5,size=122,color=EXP))
 def s08(self):
  self.add(eq('f_1(x)=2x^3+5x',y=1.7,size=64,color=BASE));self.to(56)
  self.show(eq('f_2(x)=2x^3+5x+3',y=.15,size=64,color=REL));self.to(59)
  self.play(*[m.animate.scale(.65).shift(LEFT*3.6) for m in list(self.mobjects) if isinstance(m,MathTex)],run_time=.5)
  self.original(3,family=True,label='C = 0과 C = 3 · 높이는 3만큼 다르다')
 def s09(self):
  ax=self.original(3,family=True,label='같은 x에서 접선은 서로 평행');self.add(self.tangent(ax,.4,0,BASE),self.tangent(ax,.4,3,REL));self.add(self.left("f_1'(x)=6x^2+5",y=1.4,size=51,color=BASE));self.to(65)
  self.show(self.left("f_2'(x)=6x^2+5+0",y=0,size=47,color=REL));self.to(67)
  self.note('상수 3을 미분하면 0 → 같은 도함수',EXP)
 def s10(self):
  ax=self.original(0,family=True,label='적분상수 C만 바꾸어 수직 이동');self.add(self.left('f(x)=2x^3+5x+C',y=1.35,size=49,color=REL),self.left("f'(x)=6x^2+5",y=-.1,size=54,color=BASE))
  self.add(always_redraw(lambda:self.tangent(ax,.35,self.constant.get_value())));self.to(72)
  self.play(self.constant.animate.set_value(3),run_time=2);self.to(74)
  self.play(self.constant.animate.set_value(-2),run_time=1.3);self.play(self.constant.animate.set_value(3),run_time=1.3);self.note('높이는 달라져도 같은 x에서의 기울기는 같다',EXP)
 def s11(self):
  self.add(eq(r'\boxed{f(x)=2x^3+5x+C}',y=.7,size=94,color=REL));self.to(81);self.show(eq('C',y=-1.4,size=106,color=EXP))
 def s12(self):
  ax=self.original(-2,label='여러 가능한 그래프 중 한 점을 지나는 그래프');self.add(self.left('f(0)=3',y=1.2,size=90,color=EXP));self.to(86)
  self.play(self.constant.animate.set_value(1),run_time=1.5);self.to(88)
  self.add(Dot(ax.c2p(0,3),radius=.085,color=RESULT),eq('(0,3)',*(ax.c2p(0,3)+LEFT*.7+UP*.25)[:2],size=28,color=RESULT));self.note('x = 0일 때 함수값이 3인 점')
 def s13(self):
  m=eq('f(0)=2(0)^3+5(0)+C',size=85,color=REL);self.add(m);m=self.change(m,'3=0+0+C',95,size=100);m=self.change(m,'3=C',97,size=110,color=EXP);self.change(m,'C=3',100,size=113,color=RESULT)
 def s14(self):
  ax=self.original(-2,points=True,label='점 (0,3)을 지나는 하나의 그래프로 확정');m=self.left('f(x)=2x^3+5x+C',y=1.2,size=49,color=REL);self.add(m);self.to(104)
  self.change(m,'f(x)=2x^3+5x+3',x=-3.7,y=1.2,width=6.1,size=49,color=RESULT);self.play(self.constant.animate.set_value(3),run_time=1.5);self.note('f(0) = C = 3',RESULT)
 def s15(self):
  m=eq('f(1)=?',size=110,color=EXP);self.add(m);m=self.change(m,'f(1)=2(1)^3+5(1)+3',110,size=91);m=self.change(m,'f(1)=2+5+3',112,size=99);self.change(m,r'f(1)=\boxed{10}',114,size=110,color=RESULT)
 def s16(self):
  self.add(tx('방법 ① · 원래 함수 전체 복원',y=1.9,size=31,color=REL));self.to(120)
  self.show(eq(r"f'(x)\ \longrightarrow\ f(x)\ \longrightarrow\ f(1)=10",y=.5,size=71,color=REL));self.note('다른 방법: 시작점에서 얼마나 변했는지 직접 계산')
 def s17(self):
  ax=self.original(3,label='이미 구한 함수의 두 지점 비교');self.add(self.left('f(1)-f(0)',y=1.2,size=74,color=EXP));self.add(Dot(ax.c2p(0,3),radius=.07,color=EXP));self.to(127)
  self.add(Dot(ax.c2p(1,10),radius=.07,color=RESULT));self.to(129);self.difference(ax);self.note('높이 차이 10 − 3 = 7',EXP)
 def s18(self):
  self.derivative();self.add(self.left("f'(x)=6x^2+5",y=1.3,size=56,color=BASE));self.to(134)
  self.show(self.left(r'\int_0^1f\prime(x)\,dx',y=-.1,size=73,color=EXP));self.to(137)
  self.play(self.edge.animate.set_value(1),run_time=2,rate_func=linear);self.note('순간 변화율을 0부터 1까지 누적한다',EXP)
 def s19(self):
  self.derivative(fill=True);self.add(self.left('f(1)-f(0)',y=1.3,size=71,color=EXP));self.to(143)
  self.show(self.left(r'=\int_0^1f\prime(x)\,dx',y=-.15,size=66,color=BASE));self.to(146);self.note('미적분학의 기본정리 · 넓이 = 함수값 변화량',EXP)
 def s20(self):
  self.derivative(fill=True);m=self.left(r'\int_0^1(6x^2+5)\,dx',y=1.25,size=52,color=BASE);self.add(m)
  m=self.change(m,r'[2x^3+5x]_0^1',149,x=-3.7,y=1.25,width=6.1,size=66,color=REL);self.to(151)
  self.change(m,'7',x=-3.7,y=1.25,width=6.1,size=118,color=EXP);self.note('넓이 7 = 두 지점 사이 함수값의 증가량',EXP)
 def s21(self):
  ax=self.original(3,label='도함수의 넓이 7 → 원래 함수의 높이 차이 7');self.difference(ax);m=self.left('f(1)-f(0)=7',y=1.3,size=59,color=EXP);self.add(m);self.to(155)
  m=self.change(m,'f(1)=3+7',x=-3.7,y=1.3,width=6.1,size=74,color=REL);self.change(m,'f(1)=10',158,x=-3.7,y=1.3,width=6.1,size=90,color=RESULT)
 def s22(self):
  self.add(tx('부정적분 풀이',-3.5,1.65,30,REL,width=6),tx('정적분 풀이',3.5,1.65,30,BASE,width=6),eq('f(1)=10',-3.5,.15,80,RESULT,width=6),eq('f(1)=10',3.5,.15,80,RESULT,width=6));self.note('두 결과가 일치한다',RESULT)
 def s23(self):
  m=eq("f'(x)=6x^2+5",y=1.15,size=82,color=BASE);self.add(m);m=self.change(m,'f(x)=2x^3+5x+C',165,y=1.15,size=84,color=REL);self.to(167)
  self.show(eq(r'f(0)=3\quad\Rightarrow\quad C=3',y=-.65,size=76,color=RESULT));self.note('적분 → 함수값 조건으로 적분상수 결정')
 def s24(self):
  self.derivative(fill=True);self.add(self.left(r'f(1)-f(0)=\int_0^1f\prime(x)\,dx',y=1.25,size=43,color=BASE));self.to(174)
  self.show(self.left('=7',y=-.2,size=110,color=EXP));self.note('원래 함수 전체를 구하지 않고 변화량만 계산')
 def s25(self):
  self.add(tx('부정적분',-3.5,1.8,34,REL,width=6),tx('정적분',3.5,1.8,34,BASE,width=6),eq('2x^3+5x+C',-3.5,.5,66,REL,width=6),eq(r'\int_u^v f\prime(x)\,dx',3.5,.5,67,BASE,width=6));self.to(180)
  self.show(tx('원래 함수 전체',-3.5,-1.1,33,REL,width=6),tx('두 지점 사이 변화량',3.5,-1.1,33,BASE,width=6))
 def s26(self):
  self.add(eq("f'(x)=6x^2+5",y=1.65,size=66,color=BASE),eq('f(1)-f(0)=7',y=.2,size=74,color=EXP),eq(r'f(1)=\boxed{10}',y=-1.4,size=87,color=RESULT));self.to(186.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(26):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(RestoreShot,),{'shot':i,'__module__':__name__})
