"""264-second chapter; fixed user narration, 47 replaceable 4K shots."""
import os,sys,json,math
from pathlib import Path
from bisect import bisect_right
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]))
from longforms.pi_understanding.chapter_00.scene import t,e,box,pi_center,geometry,network,INK,MUTED,GOLD,BLUE,VIOLET,GREEN,FONT
DATA=json.loads((HERE/"timing.json").read_text(encoding="utf-8"))
ORANGE,RED="#FB923C","#F87171"
config.tex_dir=str(HERE.parents[2]/"media/pi_ch01/tex")

def S(x,n=16):return sum((-1)**k*x**(2*k+1)/math.factorial(2*k+1) for k in range(n))
def C(x,n=16):return sum((-1)**k*x**(2*k)/math.factorial(2*k) for k in range(n))
def first_root():
 a,b=3.,4.
 for _ in range(60):
  mid=(a+b)/2
  if S(mid)>0:a=mid
  else:b=mid
 return (a+b)/2
X0=first_root()
def circle_axes(x=-3.8):
 ax=Axes(x_range=[-1.3,1.3,1],y_range=[-1.3,1.3,1],x_length=4.16,y_length=4.16,tips=False,axis_config=dict(color=MUTED,stroke_opacity=.3))
 ax.move_to([x,0,0]);circ=Circle(radius=1.6,color=BLUE).move_to(ax.c2p(0,0));return ax,circ
def half(x=0,y=-.5,r=1.6,color=BLUE,fill=False):
 arc=Arc(radius=r,start_angle=0,angle=PI,color=color).shift([x,y,0])
 if fill:
  arc.add_line_to(np.array([x+r,y,0]));arc.set_fill(color,opacity=.16)
 return arc
def half_board(n=None,x=0,w=7):
 ax=Axes(x_range=[-1,1,.5],y_range=[0,1.1,.5],x_length=w,y_length=2.5,tips=False,axis_config=dict(stroke_opacity=.3,color=MUTED)).move_to([x,.15,0])
 f=ax.plot(lambda q:math.sqrt(max(0,1-q*q)),x_range=[-1,1,.008],color=VIOLET)
 group=VGroup(ax,f)
 if n:
  dx=2/n;rects=VGroup()
  for i in range(n):
   left=-1+i*dx;h=math.sqrt(max(0,1-(left+dx/2)**2));bottom=ax.c2p(left,0);top=ax.c2p(left+dx,h)
   rects.add(Rectangle(width=top[0]-bottom[0],height=top[1]-bottom[1],color=GREEN,stroke_width=.7,fill_opacity=.25).move_to((bottom+top)/2))
  group.add(rects)
 return group
def smooth_axes():
 ax=Axes(x_range=[-3,3,1],y_range=[0,1.7,.5],x_length=11.6,y_length=2.9,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([0,.1,0]);return ax
def hill(x):return .45+math.exp(-x*x/3)
def polygon(ax,n):
 xs=np.linspace(-3,3,n+1);p=VMobject(color=ORANGE,stroke_width=2.5);p.set_points_as_corners([ax.c2p(x,hill(x)) for x in xs]);return p
def power_axes():return Axes(x_range=[-6.5,6.5,1],y_range=[-2.2,2.2,1],x_length=12,y_length=3.2,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([0,.15,0])
def clipped(ax,f,color=VIOLET):
 path=VMobject(color=color,stroke_width=2.5);new=True
 for x in np.linspace(-6.5,6.5,801):
  y=f(float(x))
  if abs(y)>2.2:new=True;continue
  if new:path.start_new_path(ax.c2p(x,y));new=False
  else:path.add_line_to(ax.c2p(x,y))
 return path
def root_board():
 ax=Axes(x_range=[0,6.4,1],y_range=[-1.3,1.3,1],x_length=11.8,y_length=2.8,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([0,.15,0]);curve=ax.plot(S,x_range=[0,6.4,.02],color=VIOLET);return ax,curve
def paths_map():
 positions=[(-5,1.6),(0,2),(5,1.6),(-5,-1.5),(0,-1.7),(5,-1.5)]
 labels=[('기하학',r'x^2+y^2=1',BLUE),('멱급수',r'\sum a_nx^n',VIOLET),('삼각함수',r'S(x)',VIOLET),('미적분학',r'\frac d{dx},\ \int',GREEN),('무한급수',r'1-\frac13+\cdots',VIOLET),('확률론',r'\sqrt{2\pi}',MUTED)]
 center=pi_center();nodes=VGroup(*[box(a,b,x,y,c,w=3.4,h=.95) for (x,y),(a,b,c) in zip(positions,labels)]);links=VGroup(*[Line(center.get_center(),[x,y,0],color=c,stroke_width=1.1,stroke_opacity=.5) for (x,y),(a,b,c) in zip(positions,labels)])
 return VGroup(links,center,nodes)

class ChapterScene(Scene):
 replace=Scene.replace
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1;self.records=[];self.bounds=[]
  self.header=VGroup(t('CHAPTER 01  /  THE STRUCTURE OF π',-4.7,4.05,17,MUTED,width=6),t('원주율은 왜 중요한 수인가',5,4.05,17,MUTED,width=5),Line([-7.2,3.7,0],[7.2,3.7,0],color=MUTED,stroke_width=1,stroke_opacity=.3))
  self.title=t(self.info['title'],y=3.23,size=29)
  self.panel=Rectangle(width=15.3,height=1.32,fill_color=config.background_color,fill_opacity=1,stroke_width=0).move_to([0,-3.65,0]).set_z_index(39)
  self.caption=VGroup().set_z_index(40);self.add(self.header,self.title,self.panel,self.caption);self.update_caption(self.caption);self.caption.add_updater(self.update_caption)
 def update_caption(self,mob,dt=0):
  now=self.offset+self.time;index=bisect_right([r['start'] for r in DATA['sentences']],now+1e-7)-1
  if index==self.caption_index:return
  self.caption_index=index;lines=[];line=''
  for word in DATA['sentences'][index]['text'].split():
   if line and len(line)+len(word)+1>72:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  lines.append(line);cap=Text('\n'.join(lines),font=FONT,font_size=25,color=INK,line_spacing=1.05)
  if cap.width>14.4:cap.scale_to_fit_width(14.4)
  if cap.height>1.1:cap.scale_to_fit_height(1.1)
  cap.move_to([0,-3.65,0]);mob.become(cap).set_z_index(40)
  self.records.append(dict(sentence=index+1,at=round(now,6),lines=len(lines),left=cap.get_left()[0],right=cap.get_right()[0],bottom=cap.get_bottom()[1],top=cap.get_top()[1]))
 def to(self,target):
  assert target<=self.info['end']+1e-6
  endpoints=[r['start'] for r in DATA['sentences'] if self.offset+self.time+1e-6<r['start']<target]+[target]
  for end in endpoints:
   frames=round((end-self.offset-self.time)*30)
   if frames<0:raise RuntimeError(f'{self.info["id"]}: overrun {self.offset+self.time}>{end}')
   if frames:self.wait(frames/30,frozen_frame=True)
   self.update_caption(self.caption)
 def show(self,*mobs,run_time=.6):self.play(*[FadeIn(m) for m in mobs],run_time=run_time)
 def clear_board(self):
  keep=[self.header,self.title,self.caption,self.panel];m=[o for o in self.mobjects if o not in keep]
  if m:self.play(*[FadeOut(o) for o in m],run_time=.35)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.clear_updaters()
  for m in self.mobjects:
   if m in [self.caption,self.panel] or not m.width or not m.height:continue
   assert m.get_left()[0]>=-7.8 and m.get_right()[0]<=7.8,(self.info['id'],m)
   assert m.get_bottom()[1]>=-2.8 and m.get_top()[1]<=4.35,(self.info['id'],m)
  audit=Path(os.environ['QCS_AUDIT_DIR']);audit.mkdir(parents=True,exist_ok=True);(audit/(self.info['id']+'.json')).write_text(json.dumps(self.records),encoding='utf-8')


class Shot01(ChapterScene):
 shot=0
 def s01(self):
  g=network(six=True);self.add(g);target=geometry(0,0,1.45)
  self.play(*[FadeOut(m) for m in g[:2]],ReplacementTransform(g[2],target),run_time=1.6)
  self.show(e('d',y=-.35,size=32,color=GOLD),t('하나의 수, 여러 개의 정의',y=-2.25,size=29));self.to(4)

class Shot02(ChapterScene):
 shot=1
 def s02(self):
  r=ValueTracker(1);shape=always_redraw(lambda:geometry(-3.8,0,r.get_value()))
  cbar=always_redraw(lambda:Rectangle(width=TAU*r.get_value()*.42,height=.22,color=BLUE,fill_opacity=.8).move_to([2.3+TAU*r.get_value()*.21,1.1,0]))
  dbar=always_redraw(lambda:Rectangle(width=2*r.get_value()*.42,height=.22,color=GOLD,fill_opacity=.8).move_to([2.3+r.get_value()*.42,0,0]))
  self.add(shape,cbar,dbar);self.show(t('둘레 C',2.8,1.65,24,BLUE),t('지름 d',2.8,.55,24,GOLD),e(r'C/d=\pi',4,-1.4,66))
  self.play(r.animate.set_value(1.7),run_time=1.4);self.play(r.animate.set_value(.7),run_time=1.4);self.play(r.animate.set_value(1.4),run_time=1.4)
  for m in [shape,cbar,dbar]:m.clear_updaters()
  self.to(10)

class Shot03(ChapterScene):
 shot=2
 def s03(self):
  a=e(r'\frac Cd=\frac{2C}{2d}=\frac{3C}{3d}',y=1,size=66);self.add(a)
  self.play(ReplacementTransform(a,e(r'\pi:=\frac Cd',size=100)),run_time=1);self.to(13)

class Shot04(ChapterScene):
 shot=3
 def s04(self):
  shapes=VGroup(*[geometry(x,.6,r) for x,r in [(-5,.55),(0,1.05),(5,1.5)]]);self.show(shapes)
  self.show(*[e(r'C/d=\pi',x,-1.5,48) for x in [-5,0,5]],e(r'\frac{\lambda C}{\lambda d}=\frac Cd=\pi\qquad(\lambda>0)',y=-2.3,size=32));self.to(19)

class Shot05(ChapterScene):
 shot=4
 def s05(self):
  old=geometry(-4,0,1.5);self.add(old);ax,circ=circle_axes(4)
  self.play(TransformFromCopy(old,circ),Create(ax),GrowArrow(Arrow([-1.4,0,0],[1.4,0,0],color=MUTED)),run_time=1.4)
  self.show(t('기하학적 대상',-4,-2.3,27,BLUE),t('좌표와 방정식',4,-2.3,27,VIOLET));self.to(24)

class Shot06(ChapterScene):
 shot=5
 def s06(self):
  ax,circ=circle_axes();self.add(ax,circ);pt=ax.c2p(.8,.6)
  self.show(Line(ax.c2p(0,0),pt,color=GOLD),Dot(pt,color=GOLD),e('r=1',3.5,.3,75,color=GOLD),t('단위원  /  Unit Circle',3.5,1.8,31,BLUE));self.to(28)

class Shot07(ChapterScene):
 shot=6
 def s07(self):
  ax,circ=circle_axes();angle=ValueTracker(.6);point=lambda:ax.c2p(math.cos(angle.get_value()),math.sin(angle.get_value()))
  triangle=always_redraw(lambda:VGroup(Line(ax.c2p(0,0),point(),color=GOLD),Line(ax.c2p(0,0),ax.c2p(math.cos(angle.get_value()),0),color=BLUE),Line(ax.c2p(math.cos(angle.get_value()),0),point(),color=VIOLET),Dot(point(),radius=.055,color=GOLD)))
  self.add(ax,circ,triangle);self.show(e(r'x^2+y^2=1^2',3.4,1,67),e(r'x^2+y^2=1',3.4,-.8,64,color=BLUE))
  self.play(angle.animate.set_value(2.4),run_time=2.6);triangle.clear_updaters();self.to(33)

class Shot08(ChapterScene):
 shot=7
 def s08(self):
  ax,circ=circle_axes(-4);self.add(ax,circ)
  h=half(4,-.7,1.6,VIOLET);self.play(TransformFromCopy(circ,h),run_time=1.1)
  self.show(e(r'y=\pm\sqrt{1-x^2}',-4,-2.1,40),e(r'f(x)=\sqrt{1-x^2}',4,-2.1,43,color=VIOLET),t('위쪽 반원: y ≥ 0',4,1.7,26,VIOLET));self.to(38)

class Shot09(ChapterScene):
 shot=8
 def s09(self):
  a=half(-4,-.6,1.7);b=half_board(x=4,w=4.2);self.add(a);self.play(TransformFromCopy(a,b),run_time=1.3)
  self.show(e(r'\longleftrightarrow',size=66,color=MUTED),t('기하학적 반원',-4,-2.1,27,BLUE),e(r'f(x)=\sqrt{1-x^2}',4,-2.1,41,color=VIOLET));self.to(42)

class Shot10(ChapterScene):
 shot=9
 def s10(self):
  a=half(-4,-.5,1.7);self.add(a);b=half(4,-.5,1.7,GREEN,True);self.play(TransformFromCopy(a,b),run_time=.9)
  self.show(e(r'f(x)=\sqrt{1-x^2}',y=2.1,size=46),t('곡선의 길이 L',-4,-1.7,29,BLUE),t('곡선 아래의 넓이 A',4,-1.7,29,GREEN));self.to(47)

class Shot11(ChapterScene):
 shot=10
 def s11(self):
  ax=smooth_axes();curve=ax.plot(hill,x_range=[-3,3,.02],color=BLUE);self.show(ax);self.play(Create(curve),run_time=1.2);self.show(t('곡선의 길이를 어떻게 계산할까?',y=2.3,size=31, color=BLUE));self.to(51)

class Shot12(ChapterScene):
 shot=11
 def s12(self):
  ax=smooth_axes();curve=ax.plot(hill,x_range=[-3,3,.02],color=BLUE);poly=polygon(ax,4);self.add(ax,curve,poly);label=e('N=4',y=2.3,size=40,color=ORANGE);self.add(label)
  for n,at in [(8,52),(16,54),(32,56)]:
   self.to(at);self.play(Transform(poly,polygon(ax,n)),Transform(label,e('N='+str(n),y=2.3,size=40,color=ORANGE)),run_time=.7)
  self.show(e(r'L_N=\sum_{i=1}^N\Delta s_i',y=-2.15,size=36));self.to(58)

class Shot13(ChapterScene):
 shot=12
 def s13(self):
  a=np.array([-5,-1,0]);b=np.array([-1,1.5,0]);q=np.array([-1,-1,0])
  tri=VGroup(Line(a,q,color=BLUE),Line(q,b,color=VIOLET),Line(a,b,color=ORANGE),RightAngle(Line(q,a),Line(q,b),length=.2,color=MUTED));self.show(tri,e(r'\Delta x',-3,-1.45,35,color=BLUE),e(r'\Delta y',-.5,.2,35,color=VIOLET),e(r'\Delta s',-3,1,35,color=ORANGE))
  self.show(e(r'\Delta s=\sqrt{\Delta x^2+\Delta y^2}',3.4,1.4,46,width=7));self.to(61)
  self.show(e(r'ds=\sqrt{1+[f^\prime(x)]^2}\,dx',3.4,-.1,44,color=ORANGE,width=7));self.to(64)
  self.show(e(r'L=\int_a^b\sqrt{1+[f^\prime(x)]^2}\,dx',y=-2.1,size=39));self.to(66)

class Shot14(ChapterScene):
 shot=13
 def s14(self):
  self.add(half(-4,-.4,1.7));self.show(e(r'f(x)=\sqrt{1-x^2}',3.3,1.7,47,color=VIOLET),e(r'f^\prime(x)=-\frac{x}{\sqrt{1-x^2}}',3.3,.2,44,color=ORANGE,width=7))
  self.to(69);length=e(r'L=\int_{-1}^{1}\sqrt{1+\frac{x^2}{1-x^2}}\,dx',y=-1.4,size=45);self.show(length);self.to(72)
  self.play(ReplacementTransform(length,e(r'L=\int_{-1}^{1}\frac{dx}{\sqrt{1-x^2}}',y=-1.6,size=49)),run_time=.7);self.add(t('−1 < x < 1 · 끝점은 이상적분',-4,1.8,20,MUTED,width=5));self.to(74)

class Shot15(ChapterScene):
 shot=14
 def s15(self):
  bottom=DashedVMobject(Circle(radius=1.5,color=MUTED),num_dashes=35).move_to([-4,0,0]);arc=half(-4,0,1.5,GOLD);self.add(bottom,arc)
  self.show(e(r'C=2\pi',-4,-2.2,43),e(r'L=\frac C2=\pi',3.3,.8,70),e(r'\pi=\int_{-1}^{1}\frac{dx}{\sqrt{1-x^2}}',3.3,-1.1,45,width=7),t('끝점에서의 극한으로 정의되는 수렴하는 이상적분',3.3,-2.35,19,MUTED,width=7));self.to(79)

class Shot16(ChapterScene):
 shot=15
 def s16(self):
  a=half(-4,-.5,1.6);self.add(a);self.play(TransformFromCopy(a,half(4,-.5,1.6,GREEN,True)),GrowArrow(Arrow([-1.3,0,0],[1.3,0,0],color=MUTED)),run_time=.9);self.show(t('곡선의 길이',-4,-1.8,29,BLUE),t('곡선 아래의 넓이',4,-1.8,29,GREEN));self.to(82)

class Shot17(ChapterScene):
 shot=16
 def s17(self):
  board=half_board(4);self.add(board);label=e('N=4',y=2.3,size=40,color=GREEN);self.add(label)
  for n,at in [(8,83),(16,84.5),(32,86)]:
   self.to(at);self.play(Transform(board,half_board(n)),Transform(label,e('N='+str(n),y=2.3,size=40,color=GREEN)),run_time=.6)
  self.show(e(r'A_N=\sum_{i=1}^N f(x_i^*)\Delta x',y=-2.1,size=36,color=GREEN));self.to(88)

class Shot18(ChapterScene):
 shot=17
 def s18(self):
  boards=VGroup(*[half_board(n,x,w=3.6).scale(.9).shift(UP*.6) for n,x in [(4,-5),(12,0),(48,5)]]);self.play(LaggedStart(*[FadeIn(b) for b in boards],lag_ratio=.2),run_time=1.2)
  self.show(*[e('N='+str(n),x,2.5,30,color=GREEN) for n,x in [(4,-5),(12,0),(48,5)]],e(r'\lim_{N\to\infty}\sum_{i=1}^Nf(x_i^*)\Delta x=\int_{-1}^{1}f(x)\,dx',y=-1.3,size=36),e(r'A=\int_{-1}^{1}\sqrt{1-x^2}\,dx',y=-2.3,size=32,color=GREEN));self.to(95)

class Shot19(ChapterScene):
 shot=18
 def s19(self):
  self.add(half(-4,-.5,1.7,GREEN,True));self.show(e(r'\pi/2',-4,.15,59),e(r'A=\frac{\pi}{2}',3.2,.8,75),e(r'\frac{\pi}{2}=\int_{-1}^{1}\sqrt{1-x^2}\,dx',3.2,-1,44,width=7));self.to(99)

class Shot20(ChapterScene):
 shot=19
 def s20(self):
  original=half(0,1.6,.7,VIOLET);self.add(original);a=half(-4,-.1,1.2,BLUE);b=half(4,-.1,1.2,GREEN,True)
  self.play(TransformFromCopy(original,a),TransformFromCopy(original,b),run_time=1)
  self.show(t('곡선의 길이',-4,-.8,27,BLUE),t('곡선 아래의 넓이',4,-.8,27,GREEN),e(r'\pi=\int_{-1}^{1}\frac{dx}{\sqrt{1-x^2}}',-4,-1.8,35,width=7),e(r'\pi=2\int_{-1}^{1}\sqrt{1-x^2}\,dx',4,-1.8,35,width=7));self.to(107)

class Shot21(ChapterScene):
 shot=20
 def s21(self):
  old=geometry(-4,0,1.4);self.add(old);target=VGroup(e('f(x)',4,1,65,color=VIOLET),e(r'\frac d{dx}\quad\int',4,-.8,70,color=GREEN))
  self.play(TransformFromCopy(old,target),GrowArrow(Arrow([-1.4,0,0],[1.4,0,0],color=MUTED)),run_time=1.1);self.show(t('기하학',-4,-2.1,28,BLUE),t('해석학',4,-2.1,28,VIOLET));self.to(112)

class Shot22(ChapterScene):
 shot=21
 def s22(self):
  card=box('함수와 무한급수',r'f(x),\ \sum',4,0,VIOLET,w=4,h=1.6);card[1].shift(UP*.2);card[2].shift(DOWN*.1);self.add(geometry(-4,0,1.4),card);self.show(Arrow([2,0,0],[-2,0,0],color=GOLD),t('새로운 접근 방향',y=-1.4,size=30,color=GOLD));self.to(117)

class Shot23(ChapterScene):
 shot=22
 def s23(self):
  center=np.array([-4,0,0]);circle=Circle(radius=1.4,color=BLUE).move_to(center);a=ValueTracker(.2)
  radius=always_redraw(lambda:Line(center,center+1.4*np.array([math.cos(a.get_value()),math.sin(a.get_value()),0]),color=GOLD))
  ax=Axes(x_range=[0,6.4,1],y_range=[-1.3,1.3,1],x_length=7,y_length=3,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([3.2,0,0]);curve=ax.plot(math.sin,x_range=[0,6.3,.02],color=VIOLET)
  self.add(circle,radius,ax);self.play(Create(curve),a.animate.set_value(TAU),run_time=2.4);radius.clear_updaters();self.show(e(r'P(\theta)=(\cos\theta,\sin\theta)',y=-2.3,size=38));self.to(122)

class Shot24(ChapterScene):
 shot=23
 def s24(self):
  a=geometry(-5,0,1);angle=VGroup(Line([-1,-.7,0],[1,-.7,0],color=GOLD),Line([-1,-.7,0],[.4,.8,0],color=GOLD),e(r'\theta',0,-.2,38,color=GOLD));wave=FunctionGraph(math.sin,x_range=[-PI,PI,.02],color=VIOLET).scale(.6).move_to([5,0,0])
  self.show(a);self.play(TransformFromCopy(a,angle),run_time=.7);self.play(TransformFromCopy(angle,wave),run_time=.7);self.show(t('원',-5,-1.7,29,BLUE),t('각도',0,-1.7,29,GOLD),t('사인 함수',5,-1.7,29,VIOLET));self.to(128)

class Shot25(ChapterScene):
 shot=24
 def s25(self):
  old=VGroup(geometry(-4,0,1),e(r'\theta',0,0,70,color=MUTED));self.add(old);self.play(old.animate.set_opacity(.12),FadeIn(e('f(x):=?',4,0,72,color=VIOLET)),run_time=1);self.show(t('해석학적 정의',4,-1.5,30,VIOLET));self.to(132)

class Shot26(ChapterScene):
 shot=25
 def s26(self):
  cards=VGroup(*[box('+' if k%2==0 else '−',rf'\frac{{x^{2*k+1}}}{{{2*k+1}!}}',x,0,BLUE if k%2==0 else RED,w=2.7,h=1.8) for k,x in enumerate([-5.1,-1.7,1.7,5.1])])
  for card in cards:card[1].shift(UP*.35);card[2].shift(DOWN*.1)
  for k,card in enumerate(cards):self.to(132+2*k);self.show(card,run_time=.7)
  self.show(e(r'S(x):=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\cdots',y=2.15,size=48),t('홀수 차수 · 교대 부호 · 팩토리얼',y=-2,size=28,color=MUTED));self.to(142)

class Shot27(ChapterScene):
 shot=26
 def s27(self):
  old=e(r'x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots',y=1,size=62);self.add(old)
  self.play(ReplacementTransform(old,e(r'S(x)=\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n+1}}{(2n+1)!}',size=66)),run_time=.8);self.show(t('멱급수  /  Power Series',y=-1.9,size=31,color=VIOLET));self.to(145)

class Shot28(ChapterScene):
 shot=27
 def s28(self):
  ax=power_axes();curve=clipped(ax,lambda x:x);self.add(ax);self.play(Create(curve),run_time=1)
  self.show(e(r'S_1(x)=x',y=2.35,size=51,color=VIOLET),e(r'S_N(x)=\sum_{n=0}^{N-1}\frac{(-1)^nx^{2n+1}}{(2n+1)!}',y=-2.2,size=32));self.to(150)

class Shot29(ChapterScene):
 shot=28
 def s29(self):
  ax=power_axes();curve=clipped(ax,lambda x:x);self.add(ax,curve);lab=e('N=1',y=2.35,size=43,color=VIOLET);self.add(lab)
  for n,at in [(2,151),(3,152.4),(5,154),(8,155.6),(12,157)]:
   self.to(at);self.play(Transform(curve,clipped(ax,lambda x,n=n:S(x,n))),Transform(lab,e('N='+str(n),y=2.35,size=43,color=VIOLET)),run_time=.55)
  self.add(t('유한한 구간에서 부분합이 사인 함수에 가까워진다',y=-2.45,size=23,color=MUTED));self.to(158)

class Shot30(ChapterScene):
 shot=29
 def s30(self):
  ax=power_axes();curve=clipped(ax,S);self.add(ax,curve);self.show(e(r'\sin x:=\lim_{N\to\infty}S_N(x)=\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n+1}}{(2n+1)!}',y=2.35,size=37,color=VIOLET),t('모든 실수 x에서 수렴하는 멱급수',y=-2.4,size=25,color=MUTED));self.to(162)

class Shot31(ChapterScene):
 shot=30
 def s31(self):
  self.show(e(r'S(x)=\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n+1}}{(2n+1)!}',y=2,size=62,color=VIOLET))
  cards=VGroup(*[box(a,b,x,.1,VIOLET,w=2.8,h=1.3) for a,b,x in [('실수','x',-5.1),('거듭제곱','x^n',-1.7),('팩토리얼','n!',1.7),('무한합',r'\sum',5.1)]])
  for card in cards:card[1].shift(UP*.15);card[2].shift(DOWN*.1)
  self.show(cards,t('원 · 각도 · 원주율을 먼저 사용하지 않는 정의',y=-2,size=31,color=MUTED));self.to(169)

class Shot32(ChapterScene):
 shot=31
 def s32(self):
  ax,curve=root_board();self.add(ax,curve);pt=Dot(ax.c2p(0,0),color=GOLD,radius=.07);self.add(pt)
  path=ParametricFunction(lambda q:ax.c2p(q,S(q)),t_range=[0,X0,.015],color=VIOLET)
  self.play(MoveAlongPath(pt,path),run_time=2.8);self.show(DashedLine(ax.c2p(X0,0),ax.c2p(X0,-1.2),color=GOLD),e(r'x_0=\min\{x>0:S(x)=0\}',y=-2.2,size=47,color=GOLD));self.to(175)

class Shot33(ChapterScene):
 shot=32
 def s33(self):
  self.add(geometry(-4,0,1.3));ax,curve=root_board();g=VGroup(ax,curve).scale(.5).move_to([4,0,0]);self.add(g)
  self.show(e(r'C/d',-4,-1.8,49),e(r'x_0=\min\{x>0:S(x)=0\}',4,-1.8,33,width=7),e(r'\pi=x_0',y=2.1,size=77),t('수치적 근사는 직관이며 정확한 동치의 증명은 별도이다',y=-2.5,size=19,color=MUTED));self.to(180)

class Shot34(ChapterScene):
 shot=33
 def s34(self):
  self.show(e(r'S(t)=\sum_{n=0}^\infty\frac{(-1)^nt^{2n+1}}{(2n+1)!}',-3.8,2,36,color=VIOLET,width=7),e(r'C(t)=\sum_{n=0}^\infty\frac{(-1)^nt^{2n}}{(2n)!}',3.8,2,36,color=VIOLET,width=7))
  self.to(182);self.show(e(r'S^\prime=C,\quad C^\prime=-S',-4.1,.5,43,width=7),e(r'C^2+S^2=1',-4.1,-.65,48),e(r'\|\gamma^\prime(t)\|=1',-4.1,-1.75,43))
  center=np.array([3.8,-.4,0]);path=ParametricFunction(lambda q:center+1.4*np.array([C(q),S(q),0]),t_range=[0,X0,.01],color=GOLD)
  dot=Dot(path.get_start(),radius=.06,color=GOLD);self.add(dot);self.to(184);self.play(Create(path),MoveAlongPath(dot,path),run_time=3)
  self.show(e(r'\gamma(0)=(1,0),\quad\gamma(x_0)=(-1,0)',3.8,-2.35,27,width=7),t('단위 속력 × 시간 x₀ = 반원의 길이 π',3.8,-1.1,22,GOLD,width=7),e(r'\gamma(t)=(C(t),S(t))',3.8,-1.8,28,width=7));self.to(190)

class Shot35(ChapterScene):
 shot=34
 def s35(self):
  self.show(e(r'S(x)=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots',y=1.5,size=54,color=VIOLET))
  self.show(e(r'1-\frac13+\frac15-\frac17+\cdots',y=-.8,size=65),t('서로 다른 급수 표현',y=-2.25,size=28,color=MUTED));self.to(194)

class Shot36(ChapterScene):
 shot=35
 def s36(self):
  ax=Axes(x_range=[1,64,10],y_range=[.6,1.02,.1],x_length=11.8,y_length=3,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([0,-.1,0])
  sums=np.cumsum([(-1)**k/(2*k+1) for k in range(64)])
  def graph(n):
   g=VMobject(color=BLUE,stroke_width=1.8);g.set_points_as_corners([ax.c2p(i+1,sums[i]) for i in range(n)]);return g
  curve=graph(4);lab=e('N=4',y=2.3,size=41,color=BLUE);value=e(f'S_N={sums[3]:.8f}',y=-2.3,size=39)
  self.add(ax,curve,lab,value,DashedLine(ax.c2p(1,PI/4),ax.c2p(64,PI/4),color=GOLD),e(r'\pi/4',5.8,.25,28))
  for n,at in [(8,195),(16,197),(32,199),(64,201)]:
   self.to(at);self.play(Transform(curve,graph(n)),Transform(lab,e('N='+str(n),y=2.3,size=41,color=BLUE)),Transform(value,e(f'S_N={sums[n-1]:.8f}',y=-2.3,size=39)),run_time=.7)
  self.to(203)

class Shot37(ChapterScene):
 shot=36
 def s37(self):
  self.show(t('라이프니츠 급수',y=1.6,size=34,color=VIOLET),e(r'\sum_{n=0}^{\infty}\frac{(-1)^n}{2n+1}=\frac{\pi}{4}',y=-.2,size=78));self.to(205)

class Shot38(ChapterScene):
 shot=37
 def s38(self):
  top=VGroup(*[box('',str(n),x,1.3,BLUE,w=1.5,h=.8) for n,x in zip([1,3,5,7,9,11],[-6,-3.6,-1.2,1.2,3.6,6])]);self.show(top)
  for i,(n,x) in enumerate(zip([1,3,5,7,9,11],[-6,-3.6,-1.2,1.2,3.6,6])):
   self.play(TransformFromCopy(top[i],e(r'\frac1{'+str(n)+'}',x,-.2,53)),FadeIn(e('+' if i%2==0 else '-',x,-1.5,45,color=BLUE if i%2==0 else RED)),run_time=.45)
  self.show(t('홀수 → 역수 → 교대 부호 → 무한합',y=-2.5,size=27,color=MUTED));self.to(212)

class Shot39(ChapterScene):
 shot=38
 def s39(self):
  f=e(r'4\left(1-\frac13+\frac15-\frac17+\cdots\right)',y=1,size=70);self.add(f);self.play(ReplacementTransform(f,e(r'\pi',size=125)),run_time=1);self.show(t('무한급수의 정확한 극한값',y=-1.8,size=28,color=GOLD));self.to(215)

class Shot40(ChapterScene):
 shot=39
 def s40(self):
  cards=VGroup(*[box(a,b,x,.8,c,w=3.1,h=1.8) for a,b,x,c in [('기하학',r'C/d',-5.5,BLUE),('곡선 길이',r'\int ds',-1.85,BLUE),('넓이',r'2\int f(x)\,dx',1.85,GREEN),('함수의 영점',r'S(x_0)=0',5.5,VIOLET)]])
  for card in cards:card[1].shift(UP*.3);card[2].shift(DOWN*.12)
  self.show(cards)
  bottom=box('자연수의 교대급수',r'4(1-\frac13+\frac15-\cdots)',0,-1.7,VIOLET,w=7,h=1.6);bottom[1].shift(UP*.3);bottom[2].shift(DOWN*.12)
  self.show(bottom);self.to(221)

class Shot41(ChapterScene):
 shot=40
 def s41(self):
  g=paths_map()
  for node in g[2]:
   node[0].stretch_to_fit_height(1.5);node[1].shift(UP*.15);node[2].scale(.7).shift(DOWN*.07)
  g[2][4].shift(UP*.15)
  self.add(g[2]);self.play(Create(g[0]),FadeIn(g[1]),run_time=1);self.to(224)

class Shot42(ChapterScene):
 shot=41
 def s42(self):
  card=box('여러 해석학적 표현',r'\int,\quad S(x_0)=0,\quad\sum',4,0,VIOLET,w=4.6,h=2.2);card[1].shift(UP*.4);card[2].shift(DOWN*.1);self.add(geometry(-4,0,1.3),card)
  self.show(e(r'C/d',-4,-2.1,48),t('어느 정의가 대상의 본질에 더 가까운가?',y=2.1,size=31,color=GOLD));self.to(231)

class Shot43(ChapterScene):
 shot=42
 def s43(self):
  target=pi_center().move_to([4,0,0]);self.add(target)
  for y,label,c in [(1.7,'기하학',BLUE),(.6,'적분',GREEN),(-.6,'함수',VIOLET),(-1.7,'급수',VIOLET)]:
   path=CubicBezier([-5,y,0],[-2,y,0],[1,0,0],[3.25,0,0],color=c);self.play(Create(path),FadeIn(t(label,-6.3,y,25,c,width=2)),run_time=.45)
  self.to(235)

class Shot44(ChapterScene):
 shot=43
 def s44(self):
  start=box('정의','',-5,0,BLUE,w=2,h=1.2);self.add(start)
  for y,label in [(1.5,'성질'),(0,'표현'),(-1.5,'연산')]:
   node=box(label,'',0,y,VIOLET,w=2.7,h=.8);self.play(Create(Line([-4,0,0],[-1.4,y,0],color=MUTED)),FadeIn(node),Create(Line([1.4,y,0],[4.7,y/2,0],color=GREEN)),run_time=.6)
  self.show(t('이해의 확장',5.7,0,31,GREEN,width=3));self.to(240)

class Shot45(ChapterScene):
 shot=44
 def s45(self):
  g=paths_map()
  for node in g[2]:
   node[0].stretch_to_fit_height(1.5);node[1].shift(UP*.15);node[2].scale(.7).shift(DOWN*.07)
  g[2][4].shift(UP*.15)
  self.add(g);self.play(*[node.animate.set_opacity(.15) for node in list(g[2])[1:]],run_time=1)
  self.show(e(r'\pi=\frac Cd',x=4.7,y=.1,size=53,width=4),t('원의 크기와 비율의 불변성',x=-4.5,y=-.1,size=23,color=BLUE,width=5));self.to(246)

class Shot46(ChapterScene):
 shot=45
 def s46(self):
  g=paths_map()
  for node in g[2]:
   node[0].stretch_to_fit_height(1.5);node[1].shift(UP*.15);node[2].scale(.7).shift(DOWN*.07)
  g[2][4].shift(UP*.15)
  self.add(g)
  a=ArcBetweenPoints([-5,2.35,0],[5,2.35,0],angle=-.5,color=GOLD);b=ArcBetweenPoints([-6.7,1.6,0],[-6.7,-1.5,0],angle=.5,color=GOLD)
  self.play(Create(a),Create(b),run_time=1.2);self.to(251)
  self.play(Create(DashedLine([-3.3,-1.5,0],[-1.7,-1.55,0],color=GREEN)),run_time=.7);self.show(t('적분과 무한급수의 연결은 별도 유도가 필요하다',y=-2.65,size=20,color=MUTED));self.to(256)

class Shot47(ChapterScene):
 shot=46
 def s47(self):
  g=paths_map()
  for node in g[2]:
   node[0].stretch_to_fit_height(1.5);node[1].shift(UP*.15);node[2].scale(.7).shift(DOWN*.07)
  g[2][4].shift(UP*.15)
  self.add(g);self.play(Create(Line([-3.3,1.6,0],[-1.7,2,0],color=GOLD)),Create(Line([1.7,2,0],[3.3,1.6,0],color=GOLD)),run_time=1.1)
  self.show(t('서로 다른 표현 · 동일한 대상 · 새롭게 발견되는 관계',y=-2.6,size=28,color=INK));self.to(264)
