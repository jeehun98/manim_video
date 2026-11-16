"""Twenty-one independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT07_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT07_PREVIEW')=='1' else 1080
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
class ExtremaShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.07',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('극대와 극소',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
  new=tx('\n'.join(textwrap.wrap(s,width=29,break_long_words=False)),x=-3.9,y=-1.95,size=23,color=color,width=6) if getattr(self,'graph_active',False) else tx(s,y=-1.95,size=26,color=color)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def f(self,x):return x**3-3*x+9
 def point(self,x,y):return np.array([3.25+1.25*x,-2.1+.29*y,0])
 def graph(self,colored=False,markers=False):
  self.graph_active=True
  p=self.point
  axis=VGroup(Arrow(p(-2.5,0),p(2.5,0),buff=0,stroke_width=1.2,tip_length=.09,color=MUTED),Arrow(p(0,0),p(0,15.5),buff=0,stroke_width=1.2,tip_length=.09,color=MUTED))
  labels=VGroup(eq('x',*p(2.7,0)[:2],size=19,color=MUTED),eq('y',*p(0,15.9)[:2],size=19,color=MUTED))
  for x in [-2,-1,1,2]:labels.add(eq(str(x),*(p(x,0)+DOWN*.23)[:2],size=19,color=MUTED))
  for y in [7,9,11]:labels.add(eq(str(y),*(p(0,y)+LEFT*.23)[:2],size=19,color=MUTED))
  curves=VGroup()
  for i,(a,b) in enumerate([(-2.3,-1),(-1,1),(1,2.3)]):
   m=VMobject(stroke_width=2.8,color=([BASE,REL,RESULT][i] if colored else INK));m.set_points_as_corners([p(x,self.f(x)) for x in np.linspace(a,b,120)]);curves.add(m)
  g=VGroup(axis,labels,curves);self.add(g);self.branches=curves
  self.maxdot=Dot(p(-1,11),radius=.065,color=EXP);self.mindot=Dot(p(1,7),radius=.065,color=RESULT)
  if markers:self.add(self.maxdot,self.mindot);g.add(self.maxdot,self.mindot)
  return g
 def left(self,s,y=.8,color=INK,size=51):return eq(s,x=-3.9,y=y,size=size,color=color,width=6)
 def move_dot(self,start,end,color,duration=2):
  t=ValueTracker(start);dot=always_redraw(lambda:Dot(self.point(t.get_value(),self.f(t.get_value())),radius=.065,color=color));self.add(dot);self.play(t.animate.set_value(end),run_time=duration,rate_func=smooth);dot.clear_updaters();return dot
 def table(self,stage=3):
  xs=[-5.95,-4.8,-3.6,-2.4,-1.05]
  headers=[r'x<-1','-1',r'-1<x<1','1',r'x>1'];signs=['+','0','-','0','+'];arrows=[r'\nearrow','',r'\searrow','',r'\nearrow'];colors=[BASE,EXP,REL,RESULT,RESULT]
  g=VGroup(eq('x',-7,1.65,22,MUTED,width=.6),eq("f'(x)",-7,.6,21,BASE,width=.75),eq('f(x)',-7,-.4,21,MUTED,width=.75))
  for i,x in enumerate(xs):
   g.add(eq(headers[i],x,1.65,22,MUTED,width=1.17))
   known=i in [1,3] or (i==0 and stage>=1) or (i==2 and stage>=2) or (i==4 and stage>=3)
   g.add(eq(signs[i] if known else '?',x,.6,38,colors[i] if known else MUTED,width=1))
   if arrows[i] and known:g.add(eq(arrows[i],x,-.4,35,colors[i],width=1))
  g.add(Line([-7.35,1.1,0],[-.35,1.1,0],color=MUTED,stroke_width=1,stroke_opacity=.4),Line([-7.35,.05,0],[-.35,.05,0],color=MUTED,stroke_width=1,stroke_opacity=.4))
  self.add(g);return g
 def s01(self):
  n=tx('07',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.show(eq('f(x)=x^3+ax+9',y=1.35,size=63));self.to(4)
  condition=tx('x = −1에서 극대',y=.05,size=32,color=EXP);self.show(condition);self.play(Create(SurroundingRectangle(condition,color=EXP,buff=.17)),run_time=.6);self.to(7)
  self.show(tx('극솟값 = ?',y=-.9,size=30));opts=VGroup(*[VGroup(tx('①②③④⑤'[i],x-.35,-1.85,21),eq(str(6+i),x+.3,-1.85,30)) for i,x in enumerate([-5.4,-2.7,0,2.7,5.4])]);self.play(LaggedStart(*[FadeIn(o) for o in opts],lag_ratio=.1),run_time=1)
 def s02(self):
  self.show(tx('극대점의 접선 기울기',x=-3.9,y=1.5,size=30,color=EXP,width=6),tx('극대점 개념도 · 실제 함수 그래프 아님',x=3.25,y=2.1,size=21,color=MUTED,width=6))
  center=np.array([3.25,.7,0]);curve=VMobject(color=INK,stroke_width=2.6).set_points_as_corners([center+np.array([x,-.7*x*x,0]) for x in np.linspace(-1.7,1.7,100)]);self.add(curve)
  t=ValueTracker(-1.5)
  dot=always_redraw(lambda:Dot(center+np.array([t.get_value(),-.7*t.get_value()**2,0]),radius=.065,color=EXP))
  tangent=always_redraw(lambda:Line(center+np.array([t.get_value()-.65,-.7*t.get_value()**2+1.4*t.get_value()*.65,0]),center+np.array([t.get_value()+.65,-.7*t.get_value()**2-1.4*t.get_value()*.65,0]),color=BASE,stroke_width=2))
  self.add(dot,tangent);self.play(t.animate.set_value(0),run_time=5);dot.clear_updaters();tangent.clear_updaters();self.to(15)
  self.show(self.left(r"f'(-1)=0",y=.2,color=BASE,size=65));self.note('이번 함수는 다항함수이므로 미분 가능')
 def s03(self):
  m=eq('f(x)=x^3+ax+9',y=1.45,size=61);self.add(m);self.to(25)
  terms=VGroup(*[VGroup(eq(a,x,.35,47),eq(r'\downarrow',x,-.3,30,BASE),eq(b,x,-1,47,BASE)) for x,a,b in [(-4,'x^3','3x^2'),(0,'ax','a'),(4,'9','0')]])
  self.play(LaggedStart(*[FadeIn(o) for o in terms],lag_ratio=.25),run_time=2)
  self.to(28);self.play(FadeOut(m),FadeOut(terms),FadeIn(eq(r"f'(x)=3x^2+a",y=.5,size=69,color=BASE)),run_time=.7)
 def s04(self):
  self.add(eq(r"f'(-1)=0",y=1.7,size=43,color=EXP));m=eq(r"f'(x)=3x^2+a",y=.1,size=62,color=BASE);self.add(m)
  self.to(32);m=self.morph(m,eq(r"f'(-1)=3(-1)^2+a=0",y=.1,size=62,color=BASE));self.to(35)
  m=self.morph(m,eq('3+a=0',y=.1,size=69,color=BASE));self.to(40)
  self.morph(m,eq('a=-3',y=.1,size=78,color=RESULT))
 def s05(self):
  m=eq('f(x)=x^3+ax+9',y=.5,size=66);self.add(m);m=self.morph(m,eq('f(x)=x^3-3x+9',y=.5,size=66,color=BASE));self.to(45)
  self.play(m.animate.scale(.65).move_to([-3.9,1,0]),run_time=.6);self.graph()
 def s06(self):
  self.graph();self.add(self.left('f(x)=x^3-3x+9',y=1.2,size=45),self.maxdot);self.play(Indicate(self.maxdot,color=EXP),run_time=.7)
  self.to(52);self.show(eq('?',*(self.point(1,7)+DOWN*.6)[:2],size=50,color=RESULT),tx('극소가 되는 위치는?',-3.9,-.5,29,RESULT,width=6))
 def s07(self):
  m=eq(r"f'(x)=3x^2-3",y=.5,size=68,color=BASE);self.add(m);self.to(57)
  m=self.morph(m,eq(r"f'(x)=3(x^2-1)",y=.5,size=68,color=BASE));self.to(60)
  self.morph(m,eq(r"f'(x)=3(x-1)(x+1)",y=.5,size=68,color=BASE));self.note('x² − 1 = (x − 1)(x + 1)')
 def s08(self):
  self.graph();self.add(self.left('3(x-1)(x+1)=0',y=1.4,color=BASE,size=47));self.to(65)
  self.show(self.left('x=-1',y=.15,color=EXP,size=61),self.left('x=1',y=-1.2,color=RESULT,size=61),self.maxdot,self.mindot)
 def s09(self):
  self.graph(markers=True);self.add(self.left(r"f'(-1)=f'(1)=0",y=1.3,color=BASE,size=45))
  tangents=VGroup(*[Line(self.point(x,y)+LEFT*.55,self.point(x,y)+RIGHT*.55,color=BASE,stroke_width=2) for x,y in [(-1,11),(1,7)]])
  self.play(Create(tangents),run_time=1);self.to(71);self.show(tx('기울기는 둘 다 0',-3.9,.2,30,BASE,width=6));self.to(74)
  self.show(tx('극대? 극소? 둘 다 아닐 수도 있음',-3.9,-.9,24,WARN,width=6));self.note('판단하려면 도함수의 부호 변화를 확인',WARN)
 def s10(self):
  self.graph();self.table(1);self.play(self.branches[0].animate.set_color(BASE),run_time=.4)
  self.show(tx('x < −1:  (−) × (−) = (+)',-3.9,-1.3,26,BASE,width=6));self.to(80)
  self.move_dot(-2.1,-1.1,BASE,2);self.note('도함수 양수 → 증가',BASE)
 def s11(self):
  self.graph();self.table(2);self.branches[0].set_color(BASE);self.play(self.branches[1].animate.set_color(REL),run_time=.4)
  self.show(tx('−1 < x < 1:  (+) × (−) = (−)',-3.9,-1.3,25,REL,width=6));self.to(85)
  self.move_dot(-.85,.85,REL,2);self.note('도함수 음수 → 감소',REL)
 def s12(self):
  self.graph();self.table(3);self.branches[0].set_color(BASE);self.branches[1].set_color(REL);self.play(self.branches[2].animate.set_color(RESULT),run_time=.4)
  self.show(tx('x > 1:  (+) × (+) = (+)',-3.9,-1.3,26,RESULT,width=6));self.to(91)
  self.move_dot(1.1,2.1,RESULT,1.4);self.note('도함수 양수 → 증가',RESULT)
 def s13(self):
  self.graph(colored=True,markers=True);self.table(3);self.to(96)
  self.show(tx('극대',-4.8,-.45,24,EXP,width=1),tx('극대',* (self.point(-1,11)+UP*.4)[:2],size=23,color=EXP,width=2));self.play(Indicate(self.maxdot,color=EXP),run_time=.6)
  self.to(99);self.show(tx('극소',-2.4,-.45,24,RESULT,width=1),tx('극소',*(self.point(1,7)+DOWN*.45)[:2],size=23,color=RESULT,width=2));self.play(Indicate(self.mindot,color=RESULT),run_time=.6)
 def s14(self):
  self.graph(markers=True);self.add(self.left('f(x)=x^3-3x+9',y=1.35,size=45))
  self.play(Create(DashedLine(self.point(1,0),self.point(1,7),color=RESULT,dash_length=.06,stroke_width=1.3)),run_time=.6)
  m=self.left(r'f(1)=1^3-3(1)+9',y=-.15,color=RESULT,size=49);self.to(105);self.show(m);self.to(107)
  self.morph(m,self.left('f(1)=1-3+9=7',y=-.15,color=RESULT,size=49));self.show(eq('(1,7)',*(self.point(1,7)+RIGHT*.8+DOWN*.55)[:2],size=27,color=RESULT,width=2))
 def s15(self):
  self.graph(markers=True);self.add(self.left('f(1)=7',y=.9,color=RESULT,size=80));self.to(111);self.show(tx('극솟값 7  ·  정답 ②',-3.9,-.8,30,RESULT,width=6),rt=.5)
 def s16(self):
  self.graph();self.note('도함수 0은 극값의 충분조건이 아니다',WARN);self.to(114)
  self.show(self.left(r"f'(a)=0",y=1.2,color=BASE,size=66));self.to(117)
  self.show(tx('극대?  극소?',-3.9,-.05,32,WARN,width=6),tx('도함수의 부호 변화가 필요',-3.9,-1.15,27,WARN,width=6))
 def s17(self):
  self.add(self.left('g(x)=x^3',y=1.4,color=WARN,size=58),self.left(r"g'(x)=3x^2",y=.3,color=BASE,size=55))
  p=lambda x,y:np.array([3.25+1.5*x,.1+.55*y,0])
  axis=VGroup(Arrow(p(-1.6,0),p(1.6,0),buff=0,color=MUTED,stroke_width=1.2,tip_length=.08),Arrow(p(0,-3.2),p(0,3.5),buff=0,color=MUTED,stroke_width=1.2,tip_length=.08))
  curve=VMobject(color=WARN,stroke_width=2.8).set_points_as_corners([p(x,x**3) for x in np.linspace(-1.4,1.4,150)]);self.add(axis,curve)
  t=ValueTracker(-1.1);dot=always_redraw(lambda:Dot(p(t.get_value(),t.get_value()**3),radius=.065,color=RESULT));self.add(dot)
  self.to(123);self.play(t.animate.set_value(0),run_time=1.3);self.show(Line(p(-.6,0),p(.6,0),color=BASE,stroke_width=2),self.left(r"g'(0)=0",y=-.8,color=BASE,size=49));self.to(125)
  self.play(t.animate.set_value(1.1),run_time=2);dot.clear_updaters();self.note('원점 양쪽에서 계속 증가 → 극대도 극소도 아님',WARN)
 def s18(self):
  self.graph(markers=True);self.play(Indicate(self.mindot,color=RESULT),run_time=.7);self.add(self.left('(1,7)',y=1.6,color=RESULT,size=67));self.to(132)
  self.play(Create(DashedLine(self.point(1,0),self.point(1,7),color=BASE,dash_length=.06,stroke_width=1.3)),run_time=.6);self.show(tx('극소가 되는 x값 = 1',-3.9,.3,29,BASE,width=6));self.to(135)
  self.play(Create(DashedLine(self.point(0,7),self.point(1,7),color=RESULT,dash_length=.06,stroke_width=1.3)),run_time=.6);self.show(tx('극솟값 = f(1) = 7',-3.9,-1,30,RESULT,width=6))
 def s19(self):
  for t,x,s,c in [(138,-4.6,'① 미분 조건',BASE),(141,0,'② 도함수 0인 위치',EXP),(144,4.6,'③ 부호 변화',REL)]:
   self.to(t);self.show(VGroup(RoundedRectangle(width=4.1,height=1.1,corner_radius=.12,stroke_color=c,stroke_width=1.3).move_to([x,1.4,0]),tx(s,x,1.4,25,c,width=3.8)))
  self.show(eq(r"f'(x)=3(x+1)(x-1)",y=-.1,size=58,color=BASE));self.note('− → +로 바뀌는 x = 1에서 극소',RESULT)
 def s20(self):
  m=eq('x=1',y=.9,size=77,color=BASE);self.add(m);self.to(150)
  self.morph(m,eq('f(1)=7',y=.9,size=80,color=RESULT));self.show(tx('문제에서 구하는 것은 극솟값 7',y=-.9,size=33,color=RESULT))
 def s21(self):
  self.add(eq(r'f(1)=1-3+9=7',y=.55,size=72,color=RESULT),tx('정답 ②',y=-1.1,size=35,color=RESULT));self.to(155.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(21):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ExtremaShot,),{'shot':i,'__module__':__name__})
