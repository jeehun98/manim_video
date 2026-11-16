"""Thirty independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT19_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT19_PREVIEW')=='1' else 1080
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
class TangentShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.19',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('미분과 접선의 방정식',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def f(x):return x**3-5*x*x+3*x+6
 @staticmethod
 def df(x):return 3*x*x-10*x+3
 @staticmethod
 def tangent(ax,t):
  m=TangentShot.df(t);c=TangentShot.f(t)-m*t;xs=[]
  for x in [-.65,2.45]:
   if -1.8<=m*x+c<=10.8:xs.append(x)
  if abs(m)>1e-9:
   for y in [-1.8,10.8]:
    x=(y-c)/m
    if -.65<=x<=2.45:xs.append(x)
  return Line(ax.c2p(min(xs),m*min(xs)+c),ax.c2p(max(xs),m*max(xs)+c),color=EXP,stroke_width=2.5)
 def plane(self,tangent=True,dim=False,point=True):
  ax=Axes(x_range=[-.7,2.5,1],y_range=[-2,11,1],x_length=6.15,y_length=3.6,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  curve=ax.plot(lambda x:x**3-5*x*x+3*x+6,x_range=[-.6,2.4,.02],color=BASE,stroke_width=2.4,use_smoothing=False).set_stroke(opacity=.3 if dim else 1).set_fill(opacity=0);self.curve=curve
  self.add(ax,curve,tx('곡선: 청록 · 접선: 노랑',3.4,2.2,22,MUTED,width=6.5),*[eq(str(v),*(ax.c2p(v,0)+DOWN*.26)[:2],size=22,color=MUTED) for v in [0,1,2]],*[eq(str(v),*(ax.c2p(0,v)+LEFT*.24)[:2],size=22,color=MUTED) for v in [1,5,9]])
  if point:self.add(Dot(ax.c2p(1,5),radius=.075,color=REL),eq('P(1,5)',*(ax.c2p(1,5)+LEFT*.55+DOWN*.36)[:2],size=28,color=REL))
  if tangent:self.fixed_tangent=TangentShot.tangent(ax,1);self.add(self.fixed_tangent)
  return ax
 def intercept(self,label='(0,9)'):
  ax=self.ax;self.add(Dot(ax.c2p(0,9),radius=.085,color=RESULT),eq(label,*(ax.c2p(0,9)+RIGHT*.65+UP*.25)[:2],size=31,color=RESULT))
 def moves(self,reverse=False,labels=True):
  ax=self.ax;start=(1,5);corner=(0,5) if reverse else (2,5);end=(0,9) if reverse else (2,1)
  h=Arrow(ax.c2p(*start),ax.c2p(*corner),buff=0,color=WARN,stroke_width=2.4,tip_length=.09);v=Arrow(ax.c2p(*corner),ax.c2p(*end),buff=0,color=WARN,stroke_width=2.4,tip_length=.09)
  labs=VGroup(eq(r'\Delta x=-1' if reverse else r'\Delta x=1',*(ax.c2p((start[0]+corner[0])/2,5)+UP*.28)[:2],size=25,color=WARN),eq(r'\Delta y=4' if reverse else r'\Delta y=-4',*(ax.c2p(corner[0],(5+end[1])/2)+(LEFT*.5 if reverse else RIGHT*.52))[:2],size=25,color=WARN))
  return h,v,labs
 def moving(self,start=.1):
  ax=self.plane(tangent=False,point=False);self.t=ValueTracker(start)
  self.add(always_redraw(lambda:TangentShot.tangent(ax,self.t.get_value())),always_redraw(lambda:Dot(ax.c2p(self.t.get_value(),TangentShot.f(self.t.get_value())),radius=.075,color=REL)))
  return ax
 def s01(self):
  n=tx('19',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  self.show(eq('f(x)=x^3-5x^2+3x+6',y=1.4,size=79,color=BASE));self.to(4);self.show(eq('P=(1,5)',y=-.15,size=89,color=REL));self.to(6)
  self.show(tx('구하려는 값: 접선의 y절편',y=-1.75,size=38,color=EXP))
 def s02(self):
  ax=self.plane(tangent=False);self.to(11);self.play(Create(TangentShot.tangent(ax,1)),run_time=1);self.to(14)
  self.show(self.left('P=(1,5)',y=1.25,size=74,color=REL),self.left('m=?',y=-.35,size=92,color=EXP));self.note('직선은 한 점과 기울기로 결정된다')
 def s03(self):
  ax=self.plane();self.add(self.left('P=(1,5)',y=1.25,size=78,color=REL));self.play(Indicate(Dot(ax.c2p(1,5),radius=.11,color=REL)),run_time=.8);self.to(22)
  self.show(self.left('m=?',y=-.3,size=104,color=EXP));self.note('주어진 점은 알고 있다 · 기울기를 구하면 된다')
 def s04(self):
  self.moving(0);self.add(self.left("m=f'(t)",y=1.2,size=80,color=EXP));self.play(self.t.animate.set_value(.6),run_time=4);self.to(31)
  self.play(self.t.animate.set_value(1.5),run_time=2);self.to(33);self.play(self.t.animate.set_value(.8),run_time=3,rate_func=linear);self.note('곡선 위의 위치가 바뀌면 접선의 기울기도 달라진다')
 def s05(self):
  self.plane();m=self.left('f(x)=x^3-5x^2+3x+6',y=1.2,size=43,color=BASE);self.add(m);self.to(39)
  self.play(Indicate(m,color=BASE),run_time=.8);self.to(44);self.change(m,"f'(x)=3x^2-10x+3",x=-3.7,y=1.2,width=6.1,size=49,color=EXP)
 def s06(self):
  m=eq(r'\frac{d}{dx}(6)=0',size=112,color=WARN);self.add(m);self.to(51);self.play(Indicate(m,color=WARN),run_time=.6)
 def s07(self):
  self.moving(.8);m=self.left("f'(x)=3x^2-10x+3",y=1.2,size=51,color=EXP);self.add(m);self.play(self.t.animate.set_value(1),run_time=2);self.to(57)
  m=self.change(m,"f'(1)=3(1)^2-10(1)+3",x=-3.7,y=1.2,width=6.1,size=45,color=EXP);m=self.change(m,"f'(1)=3-10+3",59,x=-3.7,y=1.2,width=6.1,size=56,color=EXP);self.change(m,"f'(1)=-4",62,x=-3.7,y=1.2,width=6.1,size=76,color=RESULT)
 def s08(self):
  self.plane();self.add(self.left("m=f'(1)=-4",y=.9,size=73,color=EXP));self.note('접점 (1,5)에서 기울기 −4로 고정')
 def s09(self):
  self.plane(dim=True);self.add(self.left(r'm=\frac{\Delta y}{\Delta x}',y=1.1,size=83,color=EXP));self.to(71)
  h,v,labs=self.moves();self.play(Create(h),run_time=.7);self.to(73);self.play(Create(v),FadeIn(labs),run_time=.7)
 def s10(self):
  ax=self.plane(dim=True);h,v,labs=self.moves();self.add(self.left(r'm=\frac{-4}{1}=-4',y=1.2,size=76,color=EXP));self.play(Create(h),run_time=1.5);self.to(78)
  self.play(Create(v),FadeIn(labs),FadeIn(Dot(ax.c2p(2,1),radius=.065,color=EXP)),run_time=1.5);self.note('(2,1)은 접선 위의 점 · 곡선 위의 점은 아님',WARN)
 def s11(self):
  self.plane(dim=True);h,v,labs=self.moves();self.add(h,v,labs,self.left('m=-4<0',y=1.1,size=89,color=EXP));self.note('오른쪽으로 내려가는 직선')
 def s12(self):
  self.plane();self.add(self.left('P=(1,5)',y=1.25,size=78,color=REL),self.left('m=-4',y=-.3,size=92,color=EXP))
 def s13(self):
  self.plane();m=self.left('y-y_1=m(x-x_1)',y=1.25,size=57);self.add(m);self.to(90)
  self.change(m,'y-5=-4(x-1)',x=-3.7,y=1.25,width=6.1,size=67,color=EXP);self.to(93);self.note('접점과 기울기를 점기울기식에 대입')
 def s14(self):
  self.plane();m=self.left('y-5=-4(x-1)',y=1.1,size=65,color=EXP);self.add(m);self.change(m,'y-5=-4x+4',97,x=-3.7,y=1.1,width=6.1,size=68,color=EXP)
 def s15(self):
  self.plane();m=self.left('y-5=-4x+4',y=1.1,size=67,color=EXP);self.add(m);self.change(m,'y=-4x+9',101,x=-3.7,y=1.1,width=6.1,size=83,color=RESULT)
 def s16(self):
  self.plane();self.add(self.left('y=-4x+9',y=1.1,size=83,color=RESULT));self.to(108);self.intercept('(0,?)');self.note('y절편은 직선과 y축의 교점의 y좌표')
 def s17(self):
  ax=self.plane();m=self.left('x=0',y=1.2,size=102,color=EXP);self.add(m);self.play(Indicate(Line(ax.c2p(0,-1.8),ax.c2p(0,10.8),color=RESULT)),run_time=.8);self.to(114)
  m=self.change(m,'y=-4(0)+9',x=-3.7,y=1.2,width=6.1,size=75,color=EXP);self.change(m,'y=0+9',117,x=-3.7,y=1.2,width=6.1,size=88,color=RESULT)
 def s18(self):
  self.plane();self.intercept();self.add(self.left('y=9',y=1.1,size=112,color=RESULT));self.to(120);self.note('y절편 = 9 · 정답 9',RESULT)
 def s19(self):
  self.plane(dim=True);self.add(self.left('P=(1,5)',y=1.25,size=80,color=REL));self.to(127);self.show(self.left('m=-4',y=-.2,size=97,color=EXP));self.note('방정식을 전개하지 않고 좌표 이동으로 계산')
 def s20(self):
  self.plane(dim=True);self.add(self.left('m=-4',y=1.25,size=95,color=EXP),self.left('P=(1,5)',y=-.25,size=81,color=REL))
 def s21(self):
  self.plane(dim=True);h,v,labs=self.moves();g=VGroup(h,v,labs);self.add(g,self.left(r'\Delta x=1,\ \Delta y=-4',y=1.15,size=51,color=WARN));self.to(139)
  self.play(FadeOut(g),run_time=.4);h,v,labs=self.moves(reverse=True);self.play(Create(h),Create(v),FadeIn(labs),run_time=1.5);self.show(self.left(r'\Delta x=-1,\ \Delta y=4',y=-.3,size=51,color=RESULT))
 def s22(self):
  ax=self.plane(dim=True);h,v,labs=self.moves(reverse=True);self.add(self.left(r'(1,5)\to(0,5)',y=1.15,size=66,color=WARN));self.play(Create(h),run_time=2);self.to(146)
  self.add(Dot(ax.c2p(0,5),radius=.05,color=MUTED));self.note('(0,5)는 이동 경로의 보조점 · 접선 위의 점 아님')
 def s23(self):
  self.plane(dim=True);h,v,labs=self.moves(reverse=True);self.add(h,self.left('5+4=9',y=1.2,size=103,color=RESULT));self.play(Create(v),FadeIn(labs),run_time=2);self.to(150)
  self.intercept();self.to(152);self.note('접선이 지나는 점은 (0,9) → y절편 9',RESULT)
 def s24(self):
  self.add(tx('방정식 이용',-3.5,1.8,32,EXP,width=6),tx('좌표 이동 이용',3.5,1.8,32,WARN,width=6),eq('y=-4x+9',-3.5,.35,67,EXP,width=6),eq(r'(1,5)\to(0,9)',3.5,.35,67,WARN,width=6));self.note('두 방법 모두 y절편 9',RESULT)
 def s25(self):
  self.moving(.2);self.add(self.left("m=f'(t)",y=1.2,size=86,color=EXP));self.to(162)
  self.play(self.t.animate.set_value(1.5),run_time=2);self.to(165);self.play(self.t.animate.set_value(1),run_time=1.5);self.note('한 점을 고정하면 접선은 하나의 직선')
 def s26(self):
  self.plane();m=self.left("f'(x)=3x^2-10x+3",y=1.15,size=50,color=BASE);self.add(m);self.change(m,"f'(1)=-4",170,x=-3.7,y=1.15,width=6.1,size=81,color=EXP)
 def s27(self):
  self.plane();m=self.left(r'(1,5),\quad m=-4',y=1.2,size=59,color=REL);self.add(m);self.change(m,'y=-4x+9',173,x=-3.7,y=1.2,width=6.1,size=84,color=RESULT)
 def s28(self):
  self.add(eq(r'f(x)\longrightarrow f\prime(x)',y=1.6,size=79,color=BASE));self.to(180)
  self.show(eq("m=f'(1)=-4",y=.1,size=91,color=EXP),eq('y-5=-4(x-1)',y=-1.45,size=78,color=RESULT))
 def s29(self):
  self.plane(dim=True);h,v,labs=self.moves(reverse=True);self.add(self.left('5+(-4)(0-1)=9',y=1.2,size=61,color=RESULT));self.play(Create(h),run_time=3);self.to(188)
  self.play(Create(v),FadeIn(labs),run_time=2);self.intercept();self.note('왼쪽 1, 위로 4 → y절편 9',RESULT)
 def s30(self):
  self.plane();self.intercept();self.add(self.left("f'(1)=-4",y=1.5,size=69,color=EXP),self.left('y=-4x+9',y=.15,size=76,color=EXP));self.to(196)
  self.show(tx('y절편 = 9',-3.7,-1.35,42,RESULT,width=6.1));self.to(199)
  # Clear graph updaters before final fade; the plane here is static.
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=3)
for i in range(30):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(TangentShot,),{'shot':i,'__module__':__name__})
