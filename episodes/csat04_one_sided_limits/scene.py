"""Sixteen independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT04_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT04_PREVIEW')=='1' else 1080
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
class LimitShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.04',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('좌·우극한',x=6.2,y=3.95,size=19,color=BASE,width=2))
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
 def point(self,x,y):return np.array([2.8+1.15*x,-.5+1.15*y,0])
 def graph(self):
  data=json.loads((HERE/'graph_data.json').read_text());self.graphdata=data
  p=self.point
  axis=VGroup(Arrow(p(-2.8,0),p(2.8,0),buff=0,stroke_width=1.3,tip_length=.09,color=MUTED),Arrow(p(0,-1.4),p(0,2.55),buff=0,stroke_width=1.3,tip_length=.09,color=MUTED))
  labels=VGroup(eq('x',*p(2.9,0)[:2],size=20,color=MUTED),eq('y',*p(0,2.65)[:2],size=20,color=MUTED))
  for x in [-2,-1,1,2]:labels.add(eq(str(x),*(p(x,0)+DOWN*.25)[:2],size=21,color=MUTED))
  for y in [-1,1,2]:labels.add(eq(str(y),*(p(0,y)+LEFT*.25)[:2],size=21,color=MUTED))
  dash=VGroup(*[DashedLine(p(x,0),p(x,y),color=MUTED,stroke_width=1,dash_length=.06,stroke_opacity=.4) for x,y in [(-1,2),(-1,-1),(1,1)]],*[DashedLine(p(0,y),p(x,y),color=MUTED,stroke_width=1,dash_length=.06,stroke_opacity=.4) for x,y in [(-1,2),(-1,-1),(1,1)]])
  self.left=Line(p(-2.65,.65),p(-1,-1),color=INK,stroke_width=2.6)
  self.middle=VMobject(color=INK,stroke_width=2.6).set_points_as_corners([p(x,y) for x,y in data['middle']])
  self.right=Line(p(1,1),p(2.6,-.6),color=INK,stroke_width=2.6)
  self.open=VGroup(*[Circle(radius=.07,stroke_color=INK,stroke_width=2,fill_color=config.background_color,fill_opacity=1).move_to(p(x,y)) for x,y in data['open_points']])
  self.closed=VGroup(*[Dot(p(x,y),radius=.07,color=REL) for x,y in data['closed_points']])
  g=VGroup(axis,labels,dash,self.left,self.middle,self.right,self.open,self.closed);self.add(g);return g
 def formula(self,s,color=INK,y=1):return eq(s,x=-4.3,y=y,size=40,color=color,width=5.5)
 def leftlimit(self,result=False):return self.formula(r'\lim_{x\to-1^-}f(x)'+('=-1' if result else ''),BASE)
 def rightlimit(self,result=False):return self.formula(r'\lim_{x\to1^+}f(x)'+('=1' if result else ''),EXP)
 def move_dot(self,start,end,branch,color,duration=3,projection=False):
  t=ValueTracker(start)
  f=(lambda x:-x-2) if branch=='left' else (lambda x:2-x) if branch=='right' else lambda x:float(np.interp(x,np.array(self.graphdata['middle'])[:,0],np.array(self.graphdata['middle'])[:,1]))
  dot=always_redraw(lambda:Dot(self.point(t.get_value(),f(t.get_value())),radius=.065,color=color))
  self.add(dot)
  guide=None
  if projection:
   guide=always_redraw(lambda:DashedLine(self.point(0,f(t.get_value())),self.point(t.get_value(),f(t.get_value())),dash_length=.06,color=color,stroke_width=1.5));self.add(guide)
  self.play(t.animate.set_value(end),run_time=duration,rate_func=smooth)
  dot.clear_updaters()
  if guide:guide.clear_updaters()
  return dot
 def highlight(self,m,color):self.play(m.animate.set_color(color),run_time=.5)
 def s01(self):
  n=tx('04',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.show(self.formula(r'\lim_{x\to-1^-}f(x)',y=1.15),self.formula(r'+\lim_{x\to1^+}f(x)',y=-.25));self.to(3);self.graph()
 def s02(self):
  self.graph();self.show(self.formula(r'x\to-1^-',BASE,1.2),tx('− : 왼쪽에서',-4.3,.3,25,BASE,width=5));self.to(8)
  self.show(self.formula(r'x\to1^+',EXP,-.65),tx('+ : 오른쪽에서',-4.3,-1.45,25,EXP,width=5))
  self.play(Create(Arrow(self.point(-2.4,-.25),self.point(-1.25,-.25),color=BASE,buff=0,tip_length=.1)),Create(Arrow(self.point(2.4,-.25),self.point(1.25,-.25),color=EXP,buff=0,tip_length=.1)),run_time=.6)
 def s03(self):
  self.graph();self.add(self.leftlimit());self.highlight(self.left,BASE);self.show(tx('x < −1',-4.3,-.2,29,BASE,width=5));self.to(15)
  samples=eq(r'-2\to-1.5\to-1.2\to-1.05',x=-4.3,y=-1.1,size=25,color=BASE,width=5.5);self.show(samples)
  self.to(19);self.move_dot(-2.1,-1.14,'left',BASE,duration=4)
 def s04(self):
  self.graph();self.add(self.leftlimit());self.highlight(self.left,BASE)
  self.move_dot(-1.25,-1.04,'left',BASE,4)
  self.to(29);self.move_dot(-1.04,-1.012,'left',BASE,3,projection=True)
  self.to(33);self.show(self.formula('=-1',RESULT,y=-.4),tx('접근하는 높이: −1',-4.3,-1.3,27,BASE,width=5))
 def s05(self):
  self.graph();self.add(self.formula(r'\lim_{x\to-1^-}f(x)=-1',MUTED,y=1.8));self.to(38)
  self.show(self.rightlimit());self.highlight(self.right,EXP);self.to(42)
  self.show(self.formula('x>1',EXP,y=-.15),eq(r'2\to1.5\to1.2\to1.05',x=-4.3,y=-1.2,size=26,color=EXP,width=5.5))
 def s06(self):
  self.graph();self.add(self.rightlimit());self.highlight(self.right,EXP)
  self.move_dot(2.2,1.09,'right',EXP,4)
  self.to(52);self.move_dot(1.09,1.012,'right',EXP,3,projection=True)
  self.to(56);self.show(self.formula('=1',RESULT,y=-.4),tx('접근하는 높이: 1',-4.3,-1.3,27,EXP,width=5))
 def s07(self):
  self.graph();m=self.formula('-1+1',RESULT,y=.9);self.add(m);self.to(60);self.morph(m,self.formula('-1+1=0',RESULT,y=.9));self.to(62);self.show(tx('정답 ③',-4.3,-.6,35,RESULT,width=5),rt=.4)
 def s08(self):
  self.graph();self.show(tx('함수값은 어느 점일까?',-4.3,1.2,29,WARN,width=5.5));self.to(65)
  self.play(Create(DashedLine(self.point(-1,-1.25),self.point(-1,2.2),color=WARN,stroke_width=1.5,dash_length=.07)),run_time=.6)
  for m in [self.open[0],self.open[1],self.closed[0]]:self.play(Circumscribe(m,color=WARN,buff=.08),run_time=1)
  self.to(70);self.play(Indicate(self.closed[0],color=REL,scale_factor=1.8),run_time=1)
  self.show(tx('채워진 점 = 실제 함수값',-4.3,-.1,27,REL,width=5.5),self.formula('f(-1)=1',REL,y=-1.15))
 def s09(self):
  self.graph();self.add(self.formula('f(-1)=1',REL,y=1.2));self.play(Indicate(self.closed[0],color=REL),run_time=.6)
  self.to(77);self.move_dot(-1.7,-1.025,'left',BASE,2,projection=True);self.show(self.formula(r'\lim_{x\to-1^-}f(x)=-1',BASE,y=-1))
 def s10(self):
  self.graph();self.add(self.formula('f(1)=0',REL,y=1.2));self.play(Indicate(self.closed[1],color=REL),run_time=.6)
  self.to(83);self.move_dot(1.7,1.025,'right',EXP,2,projection=True);self.show(self.formula(r'\lim_{x\to1^+}f(x)=1',EXP,y=-1))
 def s11(self):
  self.graph();self.show(tx('실제 함수값',-4.3,1.1,28,REL,width=5),tx('접근하는 높이',-4.3,-.1,28,BASE,width=5))
  self.to(88);self.show(tx('같지 않을 수도 있다',-4.3,-1.3,29,WARN,width=5.5),rt=.5)
 def s12(self):
  self.graph();self.add(self.leftlimit(result=True));self.show(self.formula(r'\lim_{x\to-1^+}f(x)=2',REL,y=-.6))
  left_t=ValueTracker(-1.7);right_t=ValueTracker(-.3)
  middle=np.array(self.graphdata['middle'])
  a=always_redraw(lambda:Dot(self.point(left_t.get_value(),-left_t.get_value()-2),radius=.065,color=BASE))
  b=always_redraw(lambda:Dot(self.point(right_t.get_value(),float(np.interp(right_t.get_value(),middle[:,0],middle[:,1]))),radius=.065,color=REL));self.add(a,b)
  self.to(93);self.play(left_t.animate.set_value(-1.025),right_t.animate.set_value(-.975),run_time=3);a.clear_updaters();b.clear_updaters()
  self.to(96);self.show(self.formula(r'-1\ne2',WARN,y=.3),tx('양쪽 극한은 존재하지 않음',-4.3,-1.5,25,WARN,width=5.5),rt=.5)
 def s13(self):
  self.graph();self.highlight(self.middle,MUTED);self.add(self.leftlimit(),self.formula(r'\lim_{x\to1^+}f(x)',EXP,y=-.6))
  self.to(101);self.highlight(self.left,BASE);self.highlight(self.right,EXP)
  self.to(103);self.highlight(self.middle,INK);self.show(tx('주어진 방향의 가지를 따라간다',-4.3,-1.7,25,BASE,width=5.5))
 def s14(self):
  self.graph()
  for t,s,c,y in [(107,'① 방향 확인',BASE,1.4),(110,'② 그래프 추적',EXP,.2),(112,'③ 접근 높이 확인',RESULT,-1)]:
   self.to(t);self.show(tx(s,-4.3,y,29,c,width=5.5));
   if t==110:self.move_dot(-1.5,-1.04,'left',BASE,1)
 def s15(self):
  self.graph();openmark=Circle(radius=.12,stroke_color=INK,stroke_width=2,fill_color=config.background_color,fill_opacity=1).move_to([-5.6,.9,0]);closedmark=Dot([-3,.9,0],radius=.12,color=REL)
  self.show(openmark,closedmark,tx('열린 원',-5.6,.2,23,MUTED,width=2.5),tx('채워진 점',-3,.2,23,REL,width=2.5));self.to(117)
  self.show(tx('극한값은\n접근하는 높이로 판단',-4.3,-1.1,30,BASE,width=5.5));self.move_dot(1.6,1.025,'right',EXP,2)
 def s16(self):
  self.graph();self.add(self.formula(r'\lim_{x\to-1^-}f(x)',BASE,y=1.7),self.formula(r'+\lim_{x\to1^+}f(x)',EXP,y=.5),self.formula('=-1+1=0',RESULT,y=-.8));self.show(tx('정답 ③',-4.3,-1.8,30,RESULT,width=5.5),rt=.4);self.to(122.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(16):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(LimitShot,),{'shot':i,'__module__':__name__})
