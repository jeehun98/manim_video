"""Twenty-two independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT21_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT21_PREVIEW')=='1' else 1080
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
class LargestRootShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.21',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('가장 큰 실근의 불연속',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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











 def change(self,m,s,t=None,y=.45,color=REL,size=66,x=0,width=13):
  if t is not None:self.to(t)
  n=eq(s,x,y,size,color,width);self.play(TransformMatchingTex(m,n),run_time=.7);return n
 def left(self,s,y=.5,size=48,color=INK):return eq(s,-3.65,y,size,color,6.2)
 @staticmethod
 def roots(height):
  if abs(height-4)<1e-7:return [-5.,1.]
  vals=np.roots([1,3,-9,9-height]);return sorted(float(v.real) for v in vals if abs(v.imag)<1e-5)
 @staticmethod
 def largest(height):return LargestRootShot.roots(height)[-1]
 def cubic(self,height=7,moving=True,labels=False):
  ax=Axes(x_range=[-5.4,2.5,1],y_range=[-4,39,10],x_length=6.2,y_length=3.7,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.45,.05,0]);self.ax=ax
  f=ax.plot(lambda x:x**3+3*x*x-9*x+9,x_range=[-5.3,2.4,.025],color=BASE,stroke_width=2.6,use_smoothing=False).set_fill(opacity=0)
  self.add(ax,f,tx('청록: 삼차함수 · 노랑: 수평선',3.45,2.25,21,MUTED,width=6.3))
  self.height=ValueTracker(height)
  self.add(always_redraw(lambda:Line(ax.c2p(-5.35,self.height.get_value()),ax.c2p(2.45,self.height.get_value()),color=EXP,stroke_width=2)))
  if moving:
   self.add(always_redraw(lambda:VGroup(*[Dot(ax.c2p(x,self.height.get_value()),radius=.075 if i==len(LargestRootShot.roots(self.height.get_value()))-1 else .05,color=RESULT if i==len(LargestRootShot.roots(self.height.get_value()))-1 else MUTED) for i,x in enumerate(LargestRootShot.roots(self.height.get_value()))])))
  if labels:
   self.add(eq('1',*(ax.c2p(1,0)+DOWN*.24)[:2],size=23,color=REL),eq('4',*(ax.c2p(0,4)+RIGHT*.2+UP*.12)[:2],size=23,color=REL))
  return ax
 def ggraph(self,numeric=False):
  ax=Axes(x_range=[0,6,1],y_range=[-6.5,2,1],x_length=6.1,y_length=3.65,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.5,.05,0]);self.ax=ax
  # t!=3: the unique left root tends to -5. Never join it to the isolated point.
  for lo,hi in [(0,2.999),(3.001,6)]:
   curve=ax.plot(lambda t:LargestRootShot.largest(4-(t-3)**2),x_range=[lo,hi,.025],color=RESULT,stroke_width=2.5,use_smoothing=False).set_fill(opacity=0);self.add(curve)
  self.add(ax,Circle(radius=.065,color=RESULT,stroke_width=2,fill_color=config.background_color,fill_opacity=1).move_to(ax.c2p(3,-5)),Dot(ax.c2p(3,1),radius=.075,color=RESULT),DashedLine(ax.c2p(3,-5),ax.c2p(3,1),color=MUTED,stroke_opacity=.2,stroke_width=1),eq('3',*(ax.c2p(3,0)+DOWN*.24)[:2],size=24,color=EXP),tx('가장 큰 실근 g(t)',3.5,2.25,22,RESULT,width=6))
  if numeric:
   self.add(eq('g(3)=1',*(ax.c2p(3,1)+RIGHT*1.1)[:2],size=28,color=RESULT),eq('-5',*(ax.c2p(0,-5)+LEFT*.3)[:2],size=24,color=MUTED))
 def s01(self):
  self.show(eq(r'f(\alpha)=f^{\prime}(t)-4t^2+4',y=1.55,size=66));self.to(2)
  self.show(tx('g(t): 가장 큰 실근',y=.15,size=40,color=RESULT));self.to(6)
  self.show(eq(r'g(3)=1,\qquad f(2)=\ ?',y=-1.3,size=55,color=EXP))
 def s02(self):
  m=eq(r'f(\alpha)=f^{\prime}(t)-4t^2+4',y=.5,size=69);self.show(m)
  m=self.change(m,r'h(t)=f^{\prime}(t)-4t^2+4',17,color=EXP)
  m=self.change(m,r'f(\alpha)=h(t)',20,color=EXP);self.note('t가 정해지면 h(t)는 하나의 높이')
 def s03(self):
  ax=self.cubic(9);self.show(self.left(r'f(\alpha)=h(t)',y=1.2))
  self.show(self.left(r'g(t)=\max\{\alpha:f(\alpha)=h(t)\}',y=-.15,size=36,color=RESULT))
  self.to(29);self.note('가장 오른쪽 교점의 x좌표가 g(t)')
 def s04(self):
  self.cubic(12);self.show(self.left(r'y=h(t)',color=EXP));self.to(37)
  self.play(self.height.animate.set_value(5),run_time=3);self.note('높이가 바뀌면 교점도 이동한다')
 def s05(self):
  self.cubic(4);self.show(self.left(r'h(t)<L',color=WARN));self.to(42)
  self.play(self.height.animate.set_value(2.8),run_time=1.8);self.note('L은 극솟값 · 그 아래에서는 왼쪽 교점만 남는다',WARN)
 def s06(self):
  self.ggraph();self.show(self.left(r'\lim_{t\to3}g(t)\ne g(3)',size=44,color=WARN));self.to(51)
  self.note('t=3에서만 가장 큰 실근이 달라진다',WARN)
 def s07(self):
  self.show(tx('최고차항의 계수는 1',y=1.6,size=30,color=MUTED));self.to(58)
  self.show(eq(r'f(x)=x^3+ax^2+bx+c',y=.35,size=75));self.note('미지 계수 a, b, c를 결정한다')
 def s08(self):
  m=eq(r'f^{\prime}(t)=3t^2+2at+b',y=.8,size=62);self.show(m)
  m=self.change(m,r'h(t)=-t^2+2at+b+4',69,y=.8,color=EXP)
  self.to(73);self.show(eq(r'h(t)=-(t-a)^2+(a^2+b+4)',y=-.65,size=56,color=EXP));self.note('아래로 열린 포물선 · 꼭짓점의 t좌표는 a')
 def s09(self):
  self.add(tx('극솟값 L과 수평선의 높이 h(t)를 비교',y=2.1,size=27,color=MUTED))
  # Normalize horizontal position to t-a and height to h-L.
  cases=[(-4.8,-.6,'최고 높이 < L','도달 0번',WARN),(0,.6,'최고 높이 > L','도달 2번',WARN),(4.8,0,'최고 높이 = L','도달 1번',RESULT)]
  for index,(x,v,title,note,color) in enumerate(cases):
   ax=Axes(x_range=[-1.6,1.6,1],y_range=[-2.1,1.1,1],x_length=3.7,y_length=2.8,tips=False,axis_config={'color':MUTED,'stroke_width':.8}).move_to([x,.1,0])
   xmax=min(1.5,np.sqrt(v+2.05));curve=ax.plot(lambda u,peak=v:peak-u*u,x_range=[-xmax,xmax,.025],color=EXP,stroke_width=2.5,use_smoothing=False).set_fill(opacity=0)
   group=VGroup(ax,curve,Line(ax.c2p(-1.5,0),ax.c2p(1.5,0),color=REL,stroke_width=1.8),tx(title,x,1.65,23,color,width=4),tx(note,x,-1.6,25,color,width=4))
   if v>=0:
    for u in ([-np.sqrt(v),np.sqrt(v)] if v>0 else [0]):group.add(Dot(ax.c2p(u,0),radius=.065,color=color))
   self.to(77+index*2);self.show(group)
  self.note('정확히 한 번: 포물선의 꼭짓점이 극솟값에 닿는다',RESULT)
 def s10(self):
  self.show(eq(r'h(t)=-(t-a)^2+(a^2+b+4)',y=1.1,size=58,color=EXP));self.show(eq(r't=a=3',y=-.35,size=85,color=RESULT));self.note('유일한 불연속 시각 t=3이 꼭짓점')
 def s11(self):
  self.cubic(4,labels=False);self.show(self.left(r'g(3)=1',y=1.25,color=RESULT));self.to(97)
  self.show(self.left(r'x=1',y=-.1,color=REL));self.note('가장 오른쪽 교점이 극솟점이다')
 def s12(self):
  self.cubic(4,labels=True);self.show(self.left(r'f^{\prime}(1)=0',color=REL));self.note('극솟점의 접선은 수평이다')
 def s13(self):
  self.show(eq(r'f^{\prime}(x)=3x^2+6x+b',y=1.55,size=53,color=MUTED))
  m=eq(r'3+6+b=0',y=.1,size=79);self.show(m);m=self.change(m,r'b=-9',109,y=.1,color=RESULT);self.note('a=3과 f′(1)=0을 이용')
 def s14(self):
  m=eq(r'h(t)=-t^2+6t-5',y=.5,size=73,color=EXP);self.show(m)
  m=self.change(m,r'h(t)=4-(t-3)^2',115,color=EXP)
  self.to(117);self.show(eq(r'h(3)=4',y=-.8,size=65,color=RESULT))
 def s15(self):
  self.cubic(4,labels=True);self.show(self.left(r'L=h(3)=4',y=1.15,size=42,color=REL));self.to(123)
  self.show(self.left(r'f(1)=4',y=-.15,color=RESULT));self.note('포물선의 최고 높이 = 삼차함수의 극솟값')
 def s16(self):
  self.show(eq(r'f(1)=1+3-9+c',y=1.4,size=59,color=MUTED));m=eq(r'c-5=4',y=-.1,size=80);self.show(m)
  m=self.change(m,r'c=9',130,y=-.1,color=RESULT);self.note('극솟값 f(1)=4를 이용')
 def s17(self):
  self.show(eq(r'a=3,\quad b=-9,\quad c=9',y=1.5,size=53,color=RESULT));self.to(134)
  self.show(eq(r'f(x)=x^3+3x^2-9x+9',y=-.1,size=74,color=BASE))
 def s18(self):
  self.show(eq(r'f(2)=8+12-18+9',y=.8,size=69));self.to(142)
  self.show(eq(r'f(2)=11',y=-.7,size=88,color=RESULT))
 def s19(self):
  self.show(eq(r'f(\alpha)=h(t)',y=1.3,size=74));self.show(tx('방정식의 근 → 움직이는 교점',y=-.3,size=40,color=RESULT));self.note('필요한 것은 근의 공식이 아니라 교점의 변화')
 def s20(self):
  self.cubic(4);self.show(self.left(r'h(t)=L',y=1.2,color=REL));self.to(150)
  self.play(self.height.animate.set_value(3.1),run_time=1.2);self.to(152)
  self.play(self.height.animate.set_value(4),run_time=1.2);self.note('접하는 순간 가장 오른쪽 실근이 달라진다',WARN)
 def s21(self):
  self.ggraph(numeric=True);self.show(self.left(r'\lim_{t\to3}g(t)=-5',y=1.1,size=41,color=MUTED));self.show(self.left(r'g(3)=1',y=-.35,color=RESULT));self.note('실근의 연속성은 교점의 움직임으로 해석')
 def s22(self):
  self.show(eq(r'f(\alpha)=h(t)\quad\Longrightarrow\quad f(2)=11',y=.7,size=62,color=RESULT));self.note('움직이는 수평선과 가장 오른쪽 교점에 주목한다')

for i in range(22):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(LargestRootShot,),{'shot':i})
