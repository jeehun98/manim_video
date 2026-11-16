"""Seventeen independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT06_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT06_PREVIEW')=='1' else 1080
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
class TrigShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.06',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('항등식과 부호',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
  new=tx(s,y=-1.95,size=26,color=color)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def unit(self,center=(3.4,.3),r=1.65,sector=True,point=True,components=False):
  c=np.array([*center,0.]);self.uc=c;self.ur=r;px=1/np.sqrt(10);py=-3/np.sqrt(10);self.up=c+r*np.array([px,py,0])
  axes=VGroup(Arrow(c+LEFT*r*1.18,c+RIGHT*r*1.18,buff=0,stroke_width=1.2,tip_length=.09,color=MUTED),Arrow(c+DOWN*r*1.18,c+UP*r*1.18,buff=0,stroke_width=1.2,tip_length=.09,color=MUTED))
  circle=Circle(radius=r,color=MUTED,stroke_width=1.7).move_to(c)
  g=VGroup(axes,circle)
  if sector:
   wedge=Sector(radius=r,start_angle=3*PI/2,angle=PI/2,fill_color=EXP,fill_opacity=.12,stroke_width=0).shift(c);g.add(wedge)
   g.add(*[Circle(radius=.045,stroke_color=WARN,stroke_width=1.4,fill_color=config.background_color,fill_opacity=1).move_to(c+r*v) for v in [RIGHT,DOWN]])
  labels=VGroup(eq('x',*(c+RIGHT*(r*1.25))[:2],size=20,color=MUTED),eq('y',*(c+UP*(r*1.28))[:2],size=20,color=MUTED),eq(r'\frac{3\pi}{2}',*(c+DOWN*(r+.35))[:2],size=22,color=MUTED),eq(r'2\pi',*(c+RIGHT*(r+.45)+DOWN*.23)[:2],size=22,color=MUTED))
  g.add(labels);self.add(g)
  if point:
   radial=Line(c,self.up,color=INK,stroke_width=2);dot=Dot(self.up,radius=.06,color=EXP);g.add(radial,dot);self.add(radial,dot)
   if components:
    proj=c+r*np.array([px,0,0]);co=Line(c,proj,color=BASE,stroke_width=4);si=Line(proj,self.up,color=REL,stroke_width=4);g.add(co,si);self.add(co,si)
  return g
 def left(self,s,y=.8,color=INK,size=53):return eq(s,x=-3.8,y=y,size=size,color=color,width=6.3)
 def right(self,s,y=.8,color=INK,size=53):return eq(s,x=3.5,y=y,size=size,color=color,width=6.5)
 def candidates(self,y=.6):return VGroup(card('+3',-3.5,y,EXP,width=3.7),card('-3',3.5,y,EXP,width=3.7))
 def s01(self):
  n=tx('06',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.show(eq(r'\frac{3\pi}{2}<\theta<2\pi',y=1.5,size=47));self.to(2.5);self.show(eq(r'\cos^2\theta=\frac1{10}',y=.2,size=51));self.to(4)
  self.show(eq(r'\tan\theta=?',y=-.85,size=47));opts=VGroup(*[VGroup(tx('①②③④⑤'[i],x-.35,-1.9,21),eq(str(v),x+.3,-1.9,30)) for i,(x,v) in enumerate(zip([-5.4,-2.7,0,2.7,5.4],[-3,-2,-1,2,3]))]);self.play(LaggedStart(*[FadeIn(m) for m in opts],lag_ratio=.1),run_time=1)
 def s02(self):
  a=eq(r'\cos^2\theta=\frac1{10}',y=1,size=60,color=BASE);self.add(a);self.to(11)
  b=eq(r'\tan\theta=?',y=-.7,size=60,color=EXP);self.show(b);self.to(14)
  self.play(a.animate.move_to([-3.7,.6,0]),b.animate.move_to([3.7,.6,0]),run_time=1);self.show(eq(r'\longrightarrow',y=.6,size=47,color=MUTED));self.note('주어진 값과 구하려는 값을 연결하는 항등식은?',EXP)
 def s03(self):
  first=VGroup(eq(r'\sin^2\theta',size=55,color=REL),eq('+',size=55),eq(r'\cos^2\theta',size=55,color=BASE),eq('=1',size=55)).arrange(RIGHT,buff=.18).move_to([0,1.1,0]);self.show(first)
  self.to(25);self.show(eq(r'\tan^2\theta=\frac{\sin^2\theta}{\cos^2\theta}',y=-.75,size=61,color=EXP));self.play(Indicate(first[0],color=REL),run_time=1)
  self.note('cos²θ = 1/10 > 0이므로 나눗셈 가능')
 def s04(self):
  top=eq(r'\sin^2\theta+\cos^2\theta=1',y=1.4,size=48);m=eq(r'\tan^2\theta=\frac{\sin^2\theta}{\cos^2\theta}',y=-.15,size=60,color=EXP);self.add(top,m)
  self.play(TransformMatchingTex(top,eq(r'\sin^2\theta=1-\cos^2\theta',y=1.4,size=48,color=BASE)),run_time=.8)
  self.to(33);m=self.morph(m,eq(r'\tan^2\theta=\frac{1-\cos^2\theta}{\cos^2\theta}',y=-.15,size=60,color=EXP));self.to(36)
  m=self.morph(m,eq(r'\tan^2\theta=\frac1{\cos^2\theta}-\frac{\cos^2\theta}{\cos^2\theta}',y=-.15,size=58,color=EXP));self.to(38.5)
  self.morph(m,eq(r'\tan^2\theta=\frac1{\cos^2\theta}-1',y=-.15,size=64,color=EXP));self.note('cos²θ / cos²θ = 1',BASE)
 def s05(self):
  self.add(eq(r'\cos^2\theta=\frac1{10}',y=1.65,size=44,color=BASE));m=eq(r'\tan^2\theta=\frac1{\frac1{10}}-1',y=-.1,size=65,color=EXP);self.add(m)
  self.to(44);m=self.morph(m,eq(r'\tan^2\theta=10-1',y=-.1,size=65,color=EXP));self.to(46)
  self.morph(m,eq(r'\tan^2\theta=9',y=-.1,size=76,color=EXP));self.note('아직 tan θ의 부호는 결정되지 않았다',WARN)
 def s06(self):
  m=eq(r'\tan^2\theta=9',y=1.2,size=65,color=EXP);self.add(m);self.to(51)
  m=self.morph(m,eq(r'\tan\theta=\pm3',y=1.2,size=65,color=EXP));self.to(54)
  c=self.candidates(y=-.45);self.show(c);self.to(58)
  self.play(FadeOut(m),c.animate.scale(.7).move_to([0,1.65,0]),run_time=.6);self.show(eq(r'\frac{3\pi}{2}<\theta<2\pi',y=-.4,size=62,color=WARN));self.note('어느 부호인지 알려주는 조건은 각도의 범위',WARN)
 def s07(self):
  self.unit(sector=False,point=False);self.add(self.left(r'\frac{3\pi}{2}<\theta<2\pi',y=1.2,color=WARN))
  t=ValueTracker(0);ray=always_redraw(lambda:Line(self.uc,self.uc+self.ur*np.array([np.cos(t.get_value()),np.sin(t.get_value()),0]),color=EXP,stroke_width=2));self.add(ray)
  self.play(t.animate.set_value(3*PI/2),run_time=2.4,rate_func=linear);self.to(64)
  self.add(Sector(radius=self.ur,start_angle=3*PI/2,angle=PI/2,fill_color=EXP,fill_opacity=.14,stroke_width=0).shift(self.uc))
  self.play(t.animate.set_value(TAU-np.arctan(3)),run_time=1.3,rate_func=smooth);ray.clear_updaters()
  self.show(tx('제4사분면',-3.8,-.3,34,EXP,width=6),tx('두 경계는 포함하지 않는다',-3.8,-1.4,24,WARN,width=6))
 def s08(self):
  self.unit();self.add(self.left(r'\frac{3\pi}{2}<\theta<2\pi',y=1.7,color=WARN,size=40))
  px=self.uc+self.ur*np.array([1/np.sqrt(10),0,0]);self.play(Create(Line(self.uc,px,color=BASE,stroke_width=4)),run_time=.6);self.show(self.left(r'\cos\theta>0',y=.8,color=BASE,size=49))
  self.to(69);self.play(Create(Line(px,self.up,color=REL,stroke_width=4)),run_time=.6);self.show(self.left(r'\sin\theta<0',y=-.1,color=REL,size=49))
  self.to(72);self.show(self.left(r'\tan\theta=\frac{\sin\theta}{\cos\theta}<0',y=-1.25,color=EXP,size=46))
 def s09(self):
  self.unit(components=True);plus=eq('+3',-5.2,1,size=65,color=EXP);minus=eq('-3',-2.5,1,size=65,color=EXP);self.add(plus,minus)
  self.play(Create(Cross(plus,stroke_color=WARN,stroke_width=3)),Indicate(minus,color=RESULT),run_time=.7);self.to(78)
  self.show(self.left(r'\tan\theta=-3',y=-.25,color=RESULT,size=63),tx('정답 ①',-3.8,-1.3,31,RESULT,width=6),rt=.5)
 def s10(self):
  self.unit(center=(-3.6,.3),components=True);self.show(self.right(r'\cos^2\theta=\frac1{10}',y=1.2,color=BASE,size=52));self.to(84)
  m=self.right(r'|\cos\theta|=\frac1{\sqrt{10}}',y=-.1,color=BASE,size=56);self.show(m);self.to(87)
  self.morph(m,self.right(r'\cos\theta=\frac1{\sqrt{10}}',y=-.1,color=BASE,size=56));self.show(tx('제4사분면 → 코사인 양수',3.5,-1.5,26,BASE,width=6))
 def s11(self):
  self.unit(center=(-3.6,.3),components=True);self.add(self.right(r'\cos\theta=\frac1{\sqrt{10}}',y=1.9,color=BASE,size=31))
  m=self.right(r'\sin^2\theta=1-\frac1{10}=\frac9{10}',y=.5,color=REL,size=49);self.add(m);self.to(93)
  self.morph(m,self.right(r'|\sin\theta|=\frac3{\sqrt{10}}',y=.5,color=REL,size=58));self.show(tx('이 단계에서는 크기만 계산',3.5,-1.2,26,WARN,width=6))
 def s12(self):
  self.unit(center=(-3.6,.3),components=True);self.add(self.right(r'\cos\theta=\frac1{\sqrt{10}}',y=1.7,color=BASE,size=39));m=self.right(r'|\sin\theta|=\frac3{\sqrt{10}}',y=.45,color=REL,size=54);self.add(m)
  self.play(ReplacementTransform(m,self.right(r'\sin\theta=-\frac3{\sqrt{10}}',y=.45,color=REL,size=54)),run_time=.7);self.to(98)
  self.show(self.right(r'\tan\theta=\frac{-3/\sqrt{10}}{1/\sqrt{10}}',y=-1.15,color=EXP,size=49));self.to(100)
  # Keep the signed sine and cosine above; replace only the ratio.
  self.play(*[FadeOut(o) for o in list(self.mobjects) if isinstance(o,MathTex) and abs(o.get_y()+1.15)<.1],FadeIn(self.right(r'\tan\theta=-3',y=-1.15,color=RESULT,size=60)),run_time=.6)
 def s13(self):
  self.show(tx('항등식 활용',-3.7,1.8,28,EXP,width=6),tx('각각 계산',3.7,1.8,28,MUTED,width=6))
  left=VGroup(eq(r'\tan^2\theta=9',-3.7,.8,49,EXP,width=6),eq(r'\tan\theta=\pm3',-3.7,-.15,49,EXP,width=6),eq(r'\tan\theta=-3',-3.7,-1.15,49,RESULT,width=6));right=VGroup(eq(r'\cos\theta=\frac1{\sqrt{10}}',3.7,.9,42,BASE,width=6),eq(r'\sin\theta=-\frac3{\sqrt{10}}',3.7,-.2,42,REL,width=6),eq(r'\tan\theta=-3',3.7,-1.3,45,RESULT,width=6));self.show(left,right)
  self.to(106);self.play(Create(SurroundingRectangle(left,color=RESULT,buff=.17)),run_time=.6);self.note('필요한 값과 직접 연결되는 항등식 사용',EXP)
 def s14(self):
  self.note('제곱된 값만으로 원래 값의 부호를 결정할 수 없다',WARN);self.to(112)
  a=eq('(+3)^2=9',-3.5,.9,64,EXP,width=6);b=eq('(-3)^2=9',3.5,.9,64,EXP,width=6);self.show(a,b);self.to(117)
  self.play(FadeOut(a),FadeOut(b),FadeIn(eq(r'\cos^2\theta=\frac1{10}',y=1.15,size=59,color=BASE)),run_time=.6);self.to(120)
  self.show(eq(r'\cos\theta=\pm\frac1{\sqrt{10}}',y=-.4,size=66,color=WARN));self.note('각도의 범위를 확인하기 전에는 ± 두 후보가 남는다',WARN)
 def s15(self):
  m=self.left(r'\tan^2\theta=9',y=1.2,color=EXP,size=59);self.add(m);self.morph(m,self.left(r'|\tan\theta|=3',y=1.2,color=EXP,size=59));self.show(tx('① 크기를 구한다',-3.8,-.1,29,EXP,width=6));self.to(126)
  self.unit();self.show(self.left(r'\tan\theta=-3',y=-1.1,color=RESULT,size=59),tx('② 제4사분면에서 부호 결정',-3.8,-2.05,24,WARN,width=6))
 def s16(self):
  cards=VGroup(*[VGroup(RoundedRectangle(width=4.1,height=1.1,corner_radius=.12,stroke_color=c,stroke_width=1.3).move_to([x,1.55,0]),tx(s,x,1.55,27,c,width=3.8)) for x,s,c in [(-4.6,'① 항등식 선택',BASE),(0,'② 크기 계산',EXP),(4.6,'③ 부호 결정',WARN)]])
  self.play(LaggedStart(*[FadeIn(o) for o in cards],lag_ratio=.35),run_time=2.5);self.to(134)
  self.show(eq(r'\tan^2\theta=\frac1{\cos^2\theta}-1=9',x=-2,y=.1,size=49,color=EXP,width=9));self.to(137)
  self.unit(center=(4.5,-.4),r=.75,components=True);self.show(eq(r'\tan\theta=-3',x=-2,y=-1.25,size=64,color=RESULT,width=9));self.note('제4사분면: tan θ < 0',WARN)
 def s17(self):
  self.add(eq(r'\tan\theta=-3',y=.65,size=84,color=RESULT),tx('정답 ①',y=-1.1,size=35,color=RESULT));self.to(141.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(17):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(TrigShot,),{'shot':i,'__module__':__name__})
