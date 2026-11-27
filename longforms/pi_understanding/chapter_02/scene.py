"""388 seconds; confirmed narration; spatial Fourier and Gaussian constructions."""
import os,sys,json,math
from pathlib import Path
from bisect import bisect_right
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]))
from longforms.pi_understanding.chapter_00.scene import t,e,pi_center,geometry,INK,MUTED,GOLD,BLUE,VIOLET,GREEN,FONT
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.tex_dir=str(HERE.parents[2]/'media/pi_ch02/tex')

def card(label,formula,x=0,y=0,color=BLUE,w=3.4,h=1.4):
 r=RoundedRectangle(width=w,height=h,corner_radius=.08,color=color,stroke_width=1,fill_color='#101A29',fill_opacity=.9).move_to([x,y,0])
 a=t(label,x,y+.38,19,color,width=w-.3);b=e(formula,x,y-.23,29,width=w-.35)
 if b.height>.65:b.scale_to_fit_height(.65)
 return VGroup(r,a,b)

def axes(x=0,y=.2,w=11,h=3,xrange=(-PI,PI,PI),yrange=(-1.5,1.5,1)):
 return Axes(x_range=xrange,y_range=yrange,x_length=w,y_length=h,tips=False,axis_config=dict(color=MUTED,stroke_opacity=.4,stroke_width=1)).move_to([x,y,0])

def wave(ax,n=0,color=VIOLET):
 return ax.plot(lambda x:math.sin(x)+(.5*math.sin(3*x) if n>0 else 0)+(.3*math.sin(5*x) if n>1 else 0),x_range=[-PI,PI,.025],color=color,stroke_width=2.6)

def rotor(x=0,y=.4,r=1.55,n=1,theta=0,color=BLUE):
 c=np.array([x,y,0]);v=c+r*np.array([math.cos(n*theta),math.sin(n*theta),0])
 return VGroup(Line(c+[-r-.2,0,0],c+[r+.2,0,0],color=MUTED,stroke_width=1,stroke_opacity=.35),Line(c+[0,-r-.2,0],c+[0,r+.2,0],color=MUTED,stroke_width=1,stroke_opacity=.35),Circle(r,color=color,stroke_width=1.5).move_to(c),Line(c,v,color=color,stroke_width=2.5),Dot(v,radius=.055,color=GOLD))

def spin(scene,x=0,y=.4,r=1.55,n=1,seconds=2,turns=1,color=BLUE):
 q=ValueTracker(0);g=always_redraw(lambda:rotor(x,y,r,n,q.get_value(),color));scene.add(g);scene.play(q.animate.set_value(TAU*turns),run_time=seconds,rate_func=linear);g.clear_updaters();return g

def saw(ax,color=BLUE):
 g=VGroup()
 for k in [-1,0,1]:
  lo=max(-3*PI,-PI+TAU*k);hi=min(3*PI,PI+TAU*k)
  g.add(Line(ax.c2p(lo,-PI),ax.c2p(hi,PI),color=color,stroke_width=2),Dot(ax.c2p(lo,-PI),radius=.035,color=color,fill_opacity=0),Dot(ax.c2p(hi,PI),radius=.035,color=color,fill_opacity=0))
 return g

def saw_axes():return axes(w=12,h=3.2,xrange=(-3*PI,3*PI,PI),yrange=(-3.8,3.8,PI))
def saw_sum(ax,n):return ax.plot(lambda x:2*sum((-1)**(k+1)*math.sin(k*x)/k for k in range(1,n+1)),x_range=[-3*PI,3*PI,.025],color=VIOLET,stroke_width=2.4)

def bars(values,x=0,y=0,w=9,h=2,color=VIOLET):
 g=VGroup();step=w/len(values)
 g.add(Line([x-w/2,y,0],[x+w/2,y,0],color=MUTED,stroke_width=1))
 for i,v in enumerate(values):
  if abs(v)<1e-9:continue
  g.add(Rectangle(width=step*.62,height=abs(v)*h,color=color,stroke_width=.5,fill_opacity=.65).move_to([x-w/2+step*(i+.5),y+v*h/2,0]))
 return g

def normal_board(A=1,area=True,x=0,y=.4,w=11,h=2.7):
 ax=axes(x,y,w,h,(-4,4,1),(0,1.1,.5));curve=ax.plot(lambda q:A*math.exp(-q*q/2),x_range=[-4,4,.035],color=GREEN,stroke_width=2.6)
 g=VGroup(ax)
 if area:g.add(ax.get_area(curve,x_range=[-4,4],color=GREEN,opacity=.12))
 g.add(curve);return g

def proj(x,y,z,top=0):
 # Linear projection of genuine 3D coordinates. top=1 is overhead.
 return np.array([.90*x-.65*(1-top)*y,(.32*(1-top)*x+.42*(1-top)*y+1.8*(1-top)*z+.9*top*y)-.5,0])

def mesh(top=0):
 g=VGroup()
 for v in np.linspace(-3,3,17):
  for swap in [False,True]:
   points=[proj(v,u,math.exp(-(v*v+u*u)/2),top) if not swap else proj(u,v,math.exp(-(v*v+u*u)/2),top) for u in np.linspace(-3,3,61)]
   g.add(VMobject(color=GREEN,stroke_width=.8,stroke_opacity=.6).set_points_as_corners(points))
 return g

def contours(x=0,y=.2,r=2):return VGroup(*[Circle(radius=q,color=GREEN,stroke_width=1,stroke_opacity=.65).move_to([x,y,0]) for q in np.linspace(.2,r,9)])

def link(a,b,color=MUTED):
 delta=b.get_center()-a.get_center()
 if abs(delta[0])>abs(delta[1]):start=a.get_right() if delta[0]>0 else a.get_left();end=b.get_left() if delta[0]>0 else b.get_right()
 else:start=a.get_top() if delta[1]>0 else a.get_bottom();end=b.get_bottom() if delta[1]>0 else b.get_top()
 return Arrow(start,end,buff=.08,color=color,stroke_width=1.1,max_tip_length_to_length_ratio=.08)

class ChapterScene(Scene):
 replace=Scene.replace
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1;self.records=[];self.bounds=[]
  self.header=VGroup(t('CHAPTER 02  /  THE STRUCTURE OF π',-4.7,4.05,17,MUTED,width=6),t('원주율은 왜 중요한 수인가',5,4.05,17,MUTED,width=5),Line([-7.2,3.7,0],[7.2,3.7,0],color=MUTED,stroke_width=1,stroke_opacity=.3))
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
  c=pi_center();nodes=[card(a,b,x,y,col) for a,b,x,y,col in [('기하학',r'C/d',-4.8,1,BLUE),('함수',r'\sin x',4.8,1,VIOLET),('적분',r'\int f(x)\,dx',-4.8,-1.3,GREEN),('무한급수',r'4(1-\frac13+\cdots)',4.8,-1.3,VIOLET)]]
  self.add(c)
  for node in nodes:self.play(Create(link(c,node)),FadeIn(node),run_time=.65)
  self.show(t('같은 수를 표현하는 서로 다른 수학적 언어',y=-2.45,size=25))

class Shot02(ChapterScene):
 shot=1
 def s02(self):
  ax=axes(-3.8,.4,5.6,2.6);g=wave(ax,2);n=normal_board(.8,x=3.8,w=5.6)
  self.play(Create(ax),Create(g),FadeIn(n),run_time=1.5)
  self.show(card('파동의 분석',r'\frac{1}{2\pi}',-3.8,-1.9,VIOLET),card('확률밀도의 정규화',r'\frac{1}{\sqrt{2\pi}}',3.8,-1.9,GREEN))

class Shot03(ChapterScene):
 shot=2
 def s03(self):
  c=geometry(-4,0,1.5);self.add(c)
  a=card('파동',r'e^{ix}',3.5,1,VIOLET);b=card('확률',r'e^{-x^2/2}',3.5,-1,GREEN)
  self.show(a,b);self.play(Create(link(c,a,GOLD)),Create(link(c,b,GOLD)),run_time=1)
  self.show(t('원의 비율은 다른 문제에서 어떤 구조를 나타낼까?',y=-2.35,size=28))

class Shot04(ChapterScene):
 shot=3
 def s04(self):
  a=card('지수함수',r'e^{ix}',-4,.4,VIOLET,w=4,h=1.8);b=card('삼각함수',r'\cos x+i\sin x',4,.4,BLUE,w=4,h=1.8)
  self.show(a,b);self.play(Create(link(a,b,GOLD)),run_time=1)
  self.show(e(r'e^{ix}=\cos x+i\sin x',y=-1.6,size=48))

class Shot05(ChapterScene):
 shot=4
 def s05(self):
  self.show(e(r'e^x=\sum_{n=0}^{\infty}\frac{x^n}{n!}',y=1.7,size=43))
  self.show(e(r'\cos x=\sum_{k=0}^{\infty}\frac{(-1)^kx^{2k}}{(2k)!}',y=.1,size=39),e(r'\sin x=\sum_{k=0}^{\infty}\frac{(-1)^kx^{2k+1}}{(2k+1)!}',y=-1.6,size=39))

class Shot06(ChapterScene):
 shot=5
 def s06(self):
  a=e(r'e^{ix}=1+ix-\frac{x^2}{2!}-i\frac{x^3}{3!}+\frac{x^4}{4!}+\cdots',y=1.6,size=39);self.show(a)
  b=e(r'\left(1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots\right)+i\left(x-\frac{x^3}{3!}+\cdots\right)',y=.1,size=37)
  self.play(TransformFromCopy(a,b),run_time=1.8)
  self.show(t('짝수 차수 → 코사인',-3.5,-1.3,25,BLUE),t('홀수 차수 → 사인',3.5,-1.3,25,VIOLET))
  self.show(e(r'e^{ix}=\cos x+i\sin x',y=-2.2,size=43))

class Shot07(ChapterScene):
 shot=6
 def s07(self):
  self.add(rotor(theta=.7));self.show(e(r'(\cos x,\sin x)',x=4,y=.6,size=37),t('실수부',0,-1.8,22,BLUE),t('허수부',-2.4,1.5,22,VIOLET))

class Shot08(ChapterScene):
 shot=7
 def s08(self):
  self.add(e(r'|e^{ix}|=1',x=4,y=.6,size=42));spin(self,x=-2,r=1.8,seconds=3.4,turns=.8)
  self.show(t('크기는 일정하고, 방향이 변한다',y=-2.35,size=27))

class Shot09(ChapterScene):
 shot=8
 def s09(self):
  spin(self,x=-2,r=1.7,seconds=3,turns=1,color=GOLD)
  self.show(e(r'e^{i(x+2\pi)}=e^{ix}',x=3.3,y=.7,size=39,width=6.1),t('각도 2π 라디안 = 한 바퀴',3.3,-.7,25,GOLD,width=6))

class Shot10(ChapterScene):
 shot=9
 def s10(self):
  # Time is a third coordinate: a helix, a circular end view, and a sine side view.
  def P(q):return np.array([-5+q*.65+math.cos(q)*.9,.6+math.sin(q)*1.05+math.cos(q)*.55,0])
  self.title.become(t('회전에서 파동으로',y=3.23,size=29))
  path=ParametricFunction(P,t_range=[0,TAU*2,.035],color=VIOLET)
  for anchor in [0,TAU,TAU*2]:
   ring=ParametricFunction(lambda u:np.array([-5+anchor*.65+math.cos(u)*.9,.6+math.sin(u)*1.05+math.cos(u)*.55,0]),t_range=[0,TAU,.06],color=MUTED,stroke_width=.7,stroke_opacity=.25)
   self.add(ring)
  axis=Line([-5.5,.6,0],[4.1,.6,0],color=MUTED,stroke_opacity=.3)
  self.add(axis,e(r'\gamma(t)=(t,\cos t,\sin t)',y=2.6,size=32))
  q=ValueTracker(0);dot=always_redraw(lambda:Dot(P(q.get_value()),color=GOLD,radius=.065))
  self.add(dot);self.play(Create(path),q.animate.set_value(TAU*2),run_time=3.2,rate_func=linear);dot.clear_updaters()
  self.show(rotor(5.2,.5,.95),t('끝에서 본 회전',5.2,-.9,20,BLUE,width=3))
  side=VMobject(color=BLUE).set_points_as_corners([[ -5+z*.67,-1.6+.55*math.sin(z),0] for z in np.linspace(0,TAU*2,250)])
  self.play(TransformFromCopy(path,side),run_time=1.2)
  self.show(e(r'T=2\pi',x=5.1,y=-1.9,size=36,color=GOLD),t('시간축을 따라 펼치면 주기적인 파동이 된다',y=-2.5,size=24))

class Shot11(ChapterScene):
 shot=10
 def s11(self):
  for x,n in [(-4,1),(0,2),(4,3)]:self.add(rotor(x,.5,1.05,n,.4),e(r'e^{i'+str(n)+r'x}',x,-1.4,size=32))
  q=ValueTracker(0);g=always_redraw(lambda:VGroup(*[rotor(x,.5,1.05,n,q.get_value()) for x,n in [(-4,1),(0,2),(4,3)]]));self.add(g);self.play(q.animate.set_value(TAU),run_time=1.7,rate_func=linear);g.clear_updaters()

class Shot12(ChapterScene):
 shot=11
 def s12(self):
  ax=axes(y=1,w=11,h=2.3);curve=wave(ax);self.add(ax);self.play(Create(curve),run_time=.8)
  for n in [1,2]:self.play(Transform(curve,wave(ax,n)),run_time=1)
  self.show(e(r'f(x)=\sin x+0.5\sin 3x+0.3\sin 5x',y=-.7,size=38))
  for x,n,a in [(-4,1,1),(0,3,.5),(4,5,.3)]:
   small=axes(x,-1.95,3.3,.75);self.show(small,small.plot(lambda q:a*math.sin(n*q),color=VIOLET),run_time=.4)

class Shot13(ChapterScene):
 shot=12
 def s13(self):
  q=ValueTracker(0)
  g=always_redraw(lambda:VGroup(*[rotor(x,.4,1.2,n,q.get_value(),VIOLET) for x,n in [(-4.3,1),(0,3),(4.3,5)]]))
  self.add(g)
  for x,n in [(-4.3,1),(0,3),(4.3,5)]:self.add(e(r'e^{i'+str(n)+r'x}',x,-1.5,size=35))
  self.play(q.animate.set_value(TAU),run_time=3.8,rate_func=linear);g.clear_updaters()
  self.show(t('진동수 n ↔ 회전 속도 n',y=-2.45,size=26))

class Shot14(ChapterScene):
 shot=13
 def s14(self):
  b=bars([1,.5,.3],y=-.7,w=9,h=2.5);self.play(Create(b),run_time=1.4)
  for x,n,a in [(-3,1,1),(0,3,.5),(3,5,.3)]:self.show(e(f'b_{n}={a:g}',x,-1.25,size=30),run_time=.35)
  self.show(e(r'c_n=\frac{a_n-i b_n}{2}\quad(n>0)',y=-2.25,size=32),t('그림의 막대: 실수 사인 계수 bₙ',y=2.35,size=24,color=VIOLET))

class Shot15(ChapterScene):
 shot=14
 def s15(self):
  self.show(e(r'c_n=\frac{1}{2\pi}\int_0^{2\pi}f(x)e^{-inx}\,dx',y=.4,size=48))
  self.show(t('2π 주기 함수의 복소 푸리에 계수',y=-1.5,size=26,color=VIOLET))

class Shot16(ChapterScene):
 shot=15
 def s16(self):
  ax=axes(-3,.3,5.8,3.6,(-1.6,1.6,1),(-1.2,1.2,1))
  f=lambda x:math.cos(x)+.5*math.cos(2*x)
  point=lambda x:ax.c2p(f(x)*math.cos(x),-f(x)*math.sin(x))
  curve=ParametricFunction(point,t_range=[0,TAU,.025],color=VIOLET)
  self.add(ax,e(r'g_1(x)=f(x)e^{-ix}',x=3.5,y=1.7,size=32,width=6),e(r'f(x)=\cos x+\tfrac12\cos2x',x=3.5,y=.7,size=30,width=6))
  q=ValueTracker(0);vector=always_redraw(lambda:Arrow(ax.c2p(0,0),point(q.get_value()),buff=0,color=BLUE,stroke_width=2,max_tip_length_to_length_ratio=.1))
  self.add(vector);self.play(Create(curve),q.animate.set_value(TAU),run_time=3.4,rate_func=linear);vector.clear_updaters()
  self.show(Dot(ax.c2p(.5,0),color=GOLD,radius=.085),e(r'c_1=\frac12',x=3.5,y=-.65,size=43,color=GOLD))
  self.show(t('함수값으로 가중한 벡터의 평균',y=-2.15,size=25),t('곡선은 단위원 자체가 아니다 · |g₁(x)| = |f(x)|',y=-2.65,size=19,color=MUTED))

class Shot17(ChapterScene):
 shot=16
 def s17(self):
  ring=Circle(1.6,color=GOLD).move_to([-3.6,.4,0]);self.add(ring,e(r'2\pi',-3.6,-1.7,size=38))
  interval=Line([.1,.4,0],[6.1,.4,0],color=GOLD,stroke_width=3)
  self.play(TransformFromCopy(ring,interval),run_time=1.6);self.show(e('0',.1,-.1,size=28),e(r'2\pi',6.1,-.1,size=28))
  self.show(e(r'\text{mean}=\frac{1}{2\pi}\int_0^{2\pi}g_n(x)\,dx',y=-2,size=39),t('한 주기의 길이로 나누어 평균을 구한다',y=2.45,size=26))

class Shot18(ChapterScene):
 shot=17
 def s18(self):
  a=card('회전',r'e^{inx}',-4.6,.6,BLUE);b=card('주기',r'T=2\pi',0,.6,GOLD);c=card('성분의 크기',r'c_n',4.6,.6,VIOLET)
  self.add(a);self.play(Create(link(a,b)),FadeIn(b),run_time=1);self.play(Create(link(b,c)),FadeIn(c),run_time=1)
  self.show(e(r'f(x)\ \longleftrightarrow\ \{c_n\}_{n\in\mathbb Z}',y=-1.6,size=44))

class Shot19(ChapterScene):
 shot=18
 def s19(self):
  a=card('함수의 분해',r'f\longleftrightarrow\{c_n\}',-3.6,.4,VIOLET,w=4.5);b=card('새로운 계산 문제',r'\sum_{n=1}^{\infty}\frac1{n^2}',3.6,.4,BLUE,w=4.5)
  self.show(a);self.play(Create(link(a,b,GOLD)),FadeIn(b),run_time=1.2)

class Shot20(ChapterScene):
 shot=19
 def s20(self):
  self.show(e(r'1+\frac14+\frac19+\frac1{16}+\cdots',y=.8,size=55));self.show(e(r'\sum_{n=1}^{\infty}\frac1{n^2}',y=-1.2,size=47))

class Shot21(ChapterScene):
 shot=20
 def s21(self):
  b=bars([1]+[0]*11,y=-.4,h=2.5,color=BLUE);self.play(Create(b),run_time=1.5)
  value=DecimalNumber(1,num_decimal_places=8,font_size=36,color=INK).move_to([0,-1.6,0]);self.add(value)
  count=Integer(1,font_size=28,color=GOLD).move_to([4,-1.6,0]);self.add(e('N=',3.2,-1.6,size=28),count)
  for n in [2,4,8,12]:self.play(ChangeDecimalToValue(value,sum(1/k**2 for k in range(1,n+1))),ChangeDecimalToValue(count,n),Transform(b,bars([1/k**2 if k<=n else 0 for k in range(1,13)],y=-.4,h=2.5,color=BLUE)),run_time=.5)
  self.show(e(r'S_N=\sum_{n=1}^N\frac1{n^2}',y=2.3,size=37),t('부분합은 증가하지만, 각 항은 빠르게 작아진다',y=-2.4,size=25))

class Shot22(ChapterScene):
 shot=21
 def s22(self):
  self.show(t('바젤 문제',y=1.3,size=36),e(r'\sum_{n=1}^{\infty}\frac1{n^2}=?',y=-.3,size=51))

class Shot23(ChapterScene):
 shot=22
 def s23(self):
  a=e(r'1+\frac14+\frac19+\cdots',x=-3.7,y=.3,size=43,width=6)
  b=Circle(1.3,color=BLUE).move_to([4,.3,0]);self.show(a,b)
  self.show(DashedLine([- .4,.3,0],[2.3,.3,0],color=MUTED),e('?',x=1,y=1,size=42,color=GOLD),t('역제곱의 합과 원은 어떻게 연결될까?',y=-2,size=27))

class Shot24(ChapterScene):
 shot=23
 def s24(self):
  a=card('수의 문제',r'\sum\frac1{n^2}',-3.6,.4,BLUE,w=4)
  b=card('함수의 문제',r'f(x)=x,\quad -\pi<x<\pi',3.6,.4,VIOLET,w=5)
  self.show(a);self.play(Create(link(a,b,GOLD)),FadeIn(b),run_time=1.5)

class Shot25(ChapterScene):
 shot=24
 def s25(self):
  ax=saw_axes();g=saw(ax);self.add(ax);self.play(Create(g),run_time=2.2)
  self.show(e(r'f(x)=x\quad(-\pi<x<\pi)',y=-1.9,size=36),e(r'f(x+2\pi)=f(x)',y=-2.6,size=29))
  self.show(e(r'-\pi',-2,-.3,size=23),e(r'\pi',2,-.3,size=23),e(r'2\pi',4,-.3,size=23))

class Shot26(ChapterScene):
 shot=25
 def s26(self):
  ax=saw_axes();target=saw(ax);target.set_stroke(opacity=.25);curve=saw_sum(ax,1);self.add(ax,target,curve)
  for n in [3,5,15]:self.play(Transform(curve,saw_sum(ax,n)),run_time=.8)
  self.show(e(r'f_N(x)=2\sum_{n=1}^N\frac{(-1)^{n+1}}n\sin(nx)',y=-1.95,size=36),t('점프 이외에서 수렴 · L² 수렴 · 점프 부근에는 Gibbs 진동',y=-2.65,size=20,color=MUTED))

class Shot27(ChapterScene):
 shot=26
 def s27(self):
  self.show(t('파르세발 항등식',y=1.8,size=34,color=VIOLET),e(r'\frac1{\pi}\int_{-\pi}^{\pi}|f(x)|^2\,dx=\frac{a_0^2}{2}+\sum_{n=1}^{\infty}(a_n^2+b_n^2)',y=.15,size=38))
  self.show(t('2π 주기의 제곱 적분 가능한 실수 함수',y=-1.7,size=25,color=MUTED))

class Shot28(ChapterScene):
 shot=27
 def s28(self):
  ax=axes(-3.8,.7,5.3,2.4,(-PI,PI,PI),(-PI,PI,PI));line=ax.plot(lambda x:x,color=BLUE);self.add(ax,line)
  b=bars([2*(-1)**(n+1)/n for n in range(1,7)],x=3.8,y=.6,w=5,h=.7);self.show(b)
  ax2=axes(-3.8,-1.25,5.3,1.2,(-PI,PI,PI),(0,10,5));sq=ax2.plot(lambda x:x*x,color=BLUE);self.play(TransformFromCopy(line,sq),Create(ax2),run_time=1)
  squared=bars([4/n**2 for n in range(1,7)],x=3.8,y=-1.8,w=5,h=.28)
  self.play(TransformFromCopy(b,squared),run_time=1);self.show(e('=',y=-1.2,size=44,color=GOLD),e(r'\frac1{\pi}\int f^2\,dx',x=-3.8,y=-2.45,size=28),e(r'\sum b_n^2',x=3.8,y=-2.45,size=28))

class Shot29(ChapterScene):
 shot=28
 def s29(self):
  formulas=[r'\frac1{\pi}\int_{-\pi}^{\pi}x^2\,dx=\sum_{n=1}^{\infty}\left(\frac{2(-1)^{n+1}}n\right)^2',r'\frac1{\pi}\int_{-\pi}^{\pi}x^2\,dx=4\sum_{n=1}^{\infty}\frac1{n^2}',r'\sum_{n=1}^{\infty}\frac1{n^2}=\frac1{4\pi}\int_{-\pi}^{\pi}x^2\,dx']
  for y,f in zip([1.8,.1,-1.7],formulas):self.show(e(f,y=y,size=36),run_time=.8)

class Shot30(ChapterScene):
 shot=29
 def s30(self):
  self.show(e(r'\frac1{4\pi}\int_{-\pi}^{\pi}x^2\,dx=\frac1{4\pi}\left[\frac{x^3}3\right]_{-\pi}^{\pi}',y=1.1,size=38))
  result=e(r'\sum_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}{6}',y=-1.1,size=51)
  self.show(result);self.play(Create(SurroundingRectangle(result,color=GOLD,buff=.2)),run_time=.7)

class Shot31(ChapterScene):
 shot=30
 def s31(self):
  self.show(bars([1/n**2 for n in range(1,9)],x=-3.7,y=-.3,w=5.4,h=2,color=BLUE))
  ax=axes(3.7,.4,5.4,2.4,(-3*PI,3*PI,PI),(-3.8,3.8,PI));self.show(ax,saw(ax))
  self.show(t('역제곱의 무한급수',-3.7,-1.6,25,BLUE),t('주기함수의 분해',3.7,-1.6,25,VIOLET),t('파르세발 항등식이 두 문제를 연결한다',y=-2.5,size=26,color=GOLD))

class Shot32(ChapterScene):
 shot=31
 def s32(self):
  labels=[('푸리에 해석',r'f\leftrightarrow\{b_n\}',VIOLET),('파르세발',r'\int f^2\leftrightarrow\sum b_n^2',VIOLET),('바젤 문제',r'\sum n^{-2}=\pi^2/6',GOLD)]
  nodes=[card(a,b,x,.5,c,w=4.0) for x,(a,b,c) in zip([-4.9,0,4.9],labels)]
  for i,node in enumerate(nodes):
   self.show(node)
   if i:self.play(Create(link(nodes[i-1],node)),run_time=.5)
  self.show(t('한 분야의 관계가 다른 문제의 계산 방법이 된다',y=-1.8,size=28))

class Shot33(ChapterScene):
 shot=32
 def s33(self):
  self.show(normal_board(.8));self.show(t('확률론',y=-1.9,size=32,color=GREEN))

class Shot34(ChapterScene):
 shot=33
 def s34(self):
  self.show(normal_board(1/math.sqrt(TAU)));self.show(e(r'p(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}',y=-1.9,size=45))

class Shot35(ChapterScene):
 shot=34
 def s35(self):
  g=normal_board(.8);self.add(g)
  self.play(Transform(g,normal_board(1/math.sqrt(TAU))),run_time=1.8)
  self.show(e(r'\int_{-\infty}^{\infty}p(x)\,dx=1',y=-1.9,size=44),t('확률 전체의 합은 1',y=2.35,size=25,color=GREEN))

class Shot36(ChapterScene):
 shot=35
 def s36(self):
  g=normal_board(.55);self.add(g,e(r'g(x)=A e^{-x^2/2}',y=-1.4,size=39))
  self.play(Transform(g,normal_board(1)),run_time=1.4)
  self.show(e(r'A\int_{-\infty}^{\infty}e^{-x^2/2}\,dx=1',y=-2.15,size=36))

class Shot37(ChapterScene):
 shot=36
 def s37(self):
  self.show(e(r'I=\int_{-\infty}^{\infty}e^{-x^2/2}\,dx',y=.9,size=52),t('초등함수로 표현되는 부정적분이 없다',y=-.6,size=29,color=MUTED),t('정적분의 값을 구할 다른 관점이 필요하다',y=-1.8,size=28))

class Shot38(ChapterScene):
 shot=37
 def s38(self):
  self.show(e(r'I^2=\left(\int_{\mathbb R}e^{-x^2/2}\,dx\right)\left(\int_{\mathbb R}e^{-y^2/2}\,dy\right)',y=1.6,size=37))
  self.show(e(r'I^2=\iint_{\mathbb R^2}e^{-(x^2+y^2)/2}\,dx\,dy',y=-.2,size=42))
  self.show(t('비음수 함수이므로 반복 적분과 이중 적분을 연결할 수 있다',y=-2.1,size=24,color=MUTED))

class Shot39(ChapterScene):
 shot=38
 def s39(self):
  g=mesh();c1=ParametricFunction(lambda u:proj(u,0,math.exp(-u*u/2)),t_range=[-3,3,.03],color=BLUE);c2=ParametricFunction(lambda u:proj(0,u,math.exp(-u*u/2)),t_range=[-3,3,.03],color=VIOLET)
  VGroup(g,c1,c2).scale(.85).shift([0,.5,0])
  self.play(Create(c1),Create(c2),run_time=.7);self.play(TransformFromCopy(VGroup(c1,c2),g),run_time=1.4);self.play(FadeOut(c1),FadeOut(c2),run_time=.2)
  self.show(e(r'z=e^{-(x^2+y^2)/2}',y=-2.3,size=38),t('x',4.9,.3,24),t('y',-3.9,.7,24),t('z',0,1.7,24))

class Shot40(ChapterScene):
 shot=39
 def s40(self):
  c=np.array([-3.5,.3,0]);r=1.7;v=c+r*np.array([.8,.6,0]);corner=np.array([v[0],c[1],0])
  self.add(Circle(r,color=GREEN,stroke_width=1).move_to(c),Line(c+[-2.2,0,0],c+[2.2,0,0],color=MUTED,stroke_opacity=.3),Line(c+[0,-2,0],c+[0,2,0],color=MUTED,stroke_opacity=.3))
  self.play(Create(Line(c,corner,color=BLUE)),Create(Line(corner,v,color=VIOLET)),Create(Line(c,v,color=GOLD)),run_time=1)
  self.show(e('x',-2.8,.05,size=27,color=BLUE),e('y',-1.9,.8,size=27,color=VIOLET),e('r',-3,1.05,size=30,color=GOLD),e(r'x^2+y^2=r^2',x=3.4,y=1.2,size=41),e(r'e^{-(x^2+y^2)/2}=e^{-r^2/2}',x=3.4,y=-.6,size=35,width=6))

class Shot41(ChapterScene):
 shot=40
 def s41(self):
  self.add(contours(-3.3,.3,1.7),e(r'g(x,y)=e^{-r^2/2}',x=3.4,y=1.7,size=36))
  q=ValueTracker(.5);c=np.array([-3.3,.3,0]);r=1.3
  pointer=always_redraw(lambda:VGroup(Line(c,c+r*np.array([math.cos(q.get_value()),math.sin(q.get_value()),0]),color=GOLD),Dot(c+r*np.array([math.cos(q.get_value()),math.sin(q.get_value()),0]),color=GOLD)))
  bar=Rectangle(width=.7,height=2.7*math.exp(-r*r/2),fill_color=GREEN,fill_opacity=.5,color=GREEN).move_to([3.4,0,0])
  self.add(pointer,bar,e(r'r=1.3,\quad g=e^{-1.3^2/2}',x=3.4,y=-1.5,size=30,width=6))
  self.play(q.animate.set_value(TAU+.5),run_time=3,rate_func=linear);pointer.clear_updaters();self.show(t('각도는 변해도 반지름과 함수값은 일정하다',y=-2.45,size=25))

class Shot42(ChapterScene):
 shot=41
 def s42(self):
  g=contours();axesg=VGroup(Line([-2.3,.2,0],[2.3,.2,0],color=MUTED),Line([0,-2.1,0],[0,2.5,0],color=MUTED))
  self.add(g,axesg);self.play(Rotate(axesg,PI/3,about_point=[0,.2,0]),run_time=2)
  self.show(t('좌표축을 돌려도 같은 거리에서 같은 함수값',y=-2.5,size=26))

class Shot43(ChapterScene):
 shot=42
 def s43(self):
  self.add(contours(-3.6,.4,1.5),contours(3.6,.4,1.5));self.play(GrowArrow(Arrow([-1.6,.4,0],[1.6,.4,0],color=GOLD)),run_time=.8)
  self.show(t('회전 불변성',y=-1.65,size=30,color=GREEN),e(r'g(R_\theta\mathbf x)=g(\mathbf x)',y=-2.4,size=35))

class Shot44(ChapterScene):
 shot=43
 def s44(self):
  q=ValueTracker(0);g=always_redraw(lambda:mesh(q.get_value()));self.add(g)
  self.play(q.animate.set_value(1),run_time=3,rate_func=smooth);g.clear_updaters()
  rings=contours(r=1.85).move_to([0,.1,0]);self.play(ReplacementTransform(g,rings),run_time=1)
  self.show(t('같은 함수값을 갖는 점들이 원을 이룬다',y=-2.45,size=25))

class Shot45(ChapterScene):
 shot=44
 def s45(self):
  left=VGroup(*[Line([-5.8+i*.5,-1.5,0],[-5.8+i*.5,1.5,0],color=BLUE,stroke_width=.7,stroke_opacity=.5) for i in range(7)],*[Line([-5.8,-1.5+i*.5,0],[-2.8,-1.5+i*.5,0],color=BLUE,stroke_width=.7,stroke_opacity=.5) for i in range(7)])
  polar=VGroup(contours(3.5,0,1.8),*[Line([3.5,0,0],[3.5+1.8*math.cos(q),1.8*math.sin(q),0],color=GREEN,stroke_width=.7,stroke_opacity=.6) for q in np.linspace(0,TAU,16,endpoint=False)])
  self.add(left);self.play(Create(link(left,polar)),FadeIn(polar),run_time=1.2);self.show(e(r'x=r\cos\theta,\quad y=r\sin\theta',y=-2.3,size=34))
  self.to(250);self.clear_board()
  # An annular sector has area 1/2((r+dr)^2-r^2)dtheta, asymptotically r dr dtheta.
  origin=np.array([-5,-1.3,0]);a=.25;b=.7;r=2.4;dr=.45
  points=[origin+q*np.array([math.cos(z),math.sin(z),0]) for q,z in [(r,a)]]+[origin+(r+dr)*np.array([math.cos(z),math.sin(z),0]) for z in np.linspace(a,b,45)]+[origin+r*np.array([math.cos(z),math.sin(z),0]) for z in np.linspace(b,a,45)]
  wedge=Polygon(*points,color=GREEN,fill_opacity=.2,stroke_width=1.5)
  self.add(Line(origin,origin+r*np.array([math.cos(a),math.sin(a),0]),color=MUTED,stroke_width=1),Line(origin,origin+(r+dr)*np.array([math.cos(b),math.sin(b),0]),color=MUTED,stroke_width=1),Arc(radius=.65,start_angle=a,angle=b-a,color=VIOLET).shift(origin),e('r',x=-3.8,y=-1.2,size=26,color=BLUE),e(r'd\theta',x=-4.2,y=-.8,size=23,color=VIOLET))
  rect=Rectangle(width=3,height=.9,color=GREEN,fill_opacity=.2).move_to([3,.4,0]);self.show(wedge,e(r'r\,d\theta',-2.1,1,size=29,color=GOLD),e(r'dr',-2,-.8,size=27,color=GOLD))
  self.play(TransformFromCopy(wedge,rect),run_time=1.2)
  self.show(e(r'r\,d\theta',3,1.2,size=30,color=GOLD),e(r'dr',5,.4,size=30,color=GOLD),e(r'dA=r\,dr\,d\theta',y=-1.8,size=43),t('미소 영역의 면적 요소 · r ≥ 0, 0 ≤ θ < 2π',y=-2.6,size=22,color=MUTED))

class Shot46(ChapterScene):
 shot=45
 def s46(self):
  self.add(Circle(1.6,color=GREEN).move_to([-3.5,.2,0]))
  arc=Arc(radius=1.6,start_angle=0,angle=TAU-.001,color=GOLD,stroke_width=4).shift([-3.5,.2,0]);self.play(Create(arc),run_time=1.3)
  self.show(e(r'\int_0^{2\pi}d\theta=2\pi',x=3,y=.2,size=48,width=7),t('각도 방향의 적분: 한 바퀴',y=-2.2,size=27))

class Shot47(ChapterScene):
 shot=46
 def s47(self):
  self.show(e(r'I^2=\int_0^{2\pi}d\theta\int_0^\infty e^{-r^2/2}r\,dr',y=1.6,size=37))
  self.show(e(r'=2\pi\left[-e^{-r^2/2}\right]_0^\infty=2\pi',y=.1,size=39))
  self.show(e(r'I=\sqrt{2\pi}\quad(I>0)',y=-1.75,size=46,color=GOLD))

class Shot48(ChapterScene):
 shot=47
 def s48(self):
  g=normal_board(1);self.add(g);self.play(Transform(g,normal_board(1/math.sqrt(TAU))),run_time=1.8)
  self.show(e(r'p(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}',y=-1.6,size=39),e(r'\int_{\mathbb R}p(x)\,dx=1',y=-2.4,size=30))

class Shot49(ChapterScene):
 shot=48
 def s49(self):
  a=normal_board(1,x=-4.7,w=3.6,h=1.8);b=mesh().scale(.45).move_to([0,.5,0]);c=contours(4.8,.5,1.3)
  self.show(a);self.play(Create(link(a,b)),FadeIn(b),run_time=.8);self.play(Create(link(b,c)),FadeIn(c),run_time=.8)
  for x,label in [(-4.7,'가우스 적분'),(0,'이차원 확장'),(4.8,'회전 불변성')]:self.show(t(label,x,-1.2,23,GREEN),run_time=.3)
  self.show(e(r'I=\sqrt{2\pi}',y=-2.3,size=45,color=GOLD))

class Shot50(ChapterScene):
 shot=49
 def s50(self):
  # One persistent world for all eight sentences, 277–347 s.
  self.title.become(t('수학적 대상에서 수학적 구조로',y=3.23,size=29))
  world=VGroup();nodes={};previous={}
  def addnode(key,label,formula,x,y,col,parent=None):
   node=card(label,formula,x,y,col,w=3.5,h=.85);node[1].move_to([x,y+.21,0]).scale(.8);node[2].move_to([x,y-.16,0]).scale(.78)
   if parent:
    edge=link(nodes[parent],node,col);world.add(edge);self.play(Create(edge),run_time=.4)
   world.add(node);nodes[key]=node;self.play(FadeIn(node),run_time=.45)
  addnode('geo','기하학적 정의',r'\pi=C/d',-5,2.3,BLUE)
  self.to(281)
  addnode('unit','원의 함수 표현',r'x^2+y^2=1',-5,1.15,BLUE,'geo')
  addnode('calc','미적분: 단위 반원',r'L=\pi,\quad A=\pi/2',-5,0,GREEN,'unit')
  self.to(289)
  addnode('power','멱급수의 출발점',r'S(x)=\sum\frac{(-1)^nx^{2n+1}}{(2n+1)!}',-5,-1.15,VIOLET)
  addnode('zero','첫 양의 영점',r'S(\pi)=0',-5,-2.3,GOLD,'power')
  # Two approaches meet at pi, without identifying their assumptions.
  self.play(Circumscribe(nodes['zero'],color=GOLD,buff=.04),run_time=.7)
  self.to(296)
  addnode('exp','지수함수의 멱급수',r'e^z=\sum z^n/n!',0,2.3,VIOLET,'power')
  addnode('euler','오일러 공식',r'e^{ix}=\cos x+i\sin x',0,1.15,VIOLET,'exp')
  self.to(304)
  addnode('period','회전과 주기성',r'e^{i(x+2\pi)}=e^{ix}',0,0,GOLD,'euler')
  # A local rotation is animated inside the already established world.
  spark=Dot(nodes['period'].get_right()+[-.2,0,0],color=GOLD,radius=.05);self.add(spark);self.play(Circumscribe(nodes['period'],color=GOLD,buff=.04),run_time=1);self.remove(spark)
  self.to(310)
  addnode('fourier','푸리에 해석',r'f\longleftrightarrow\{c_n\}',0,-1.15,VIOLET,'period')
  addnode('basel','파르세발 → 바젤',r'\sum n^{-2}=\pi^2/6',0,-2.3,GOLD,'fourier')
  self.to(316)
  self.play(Circumscribe(nodes['fourier'],color=VIOLET,buff=.04),run_time=1);self.play(Circumscribe(nodes['basel'],color=GOLD,buff=.04),run_time=1)
  self.to(322)
  addnode('gauss','가우스 함수',r'e^{-x^2/2}',5,2.3,GREEN)
  addnode('2d','이차원으로 확장',r'e^{-(x^2+y^2)/2}',5,1.15,GREEN,'gauss')
  addnode('rot','회전 불변성',r'x^2+y^2=r^2',5,0,GREEN,'2d')
  addnode('polar','극좌표와 면적 요소',r'dA=r\,dr\,d\theta',5,-1.15,GREEN,'rot')
  addnode('norm','표준정규분포',r'I=\sqrt{2\pi}',5,-2.3,GOLD,'polar')
  self.to(333)
  edge=DashedLine(nodes['period'].get_right(),nodes['rot'].get_left(),color=GOLD,stroke_width=1);world.add(edge);self.play(Create(edge),run_time=1.3)
  note=t('회전 구조',2.5,.2,14,GOLD,width=1.3);world.add(note);self.add(note)
  for key in ['geo','power','euler','fourier','basel','rot','norm']:
   self.play(Circumscribe(nodes[key],color=GOLD,buff=.04),run_time=.7)
  self.to(342)
  self.play(AnimationGroup(*[Circumscribe(node,color=GOLD,buff=.04) for node in nodes.values()]),run_time=1.4)

class Shot51(ChapterScene):
 shot=50
 def s51(self):
  center=pi_center();self.add(center)
  for x,y,a,b,c in [(-4.7,1.5,'기하학',r'C/d',BLUE),(0,2.1,'주기성',r'2\pi',VIOLET),(4.7,1.5,'확률론',r'1/\sqrt{2\pi}',GREEN),(-4.7,-1.7,'초월성',r'\pi\notin\overline{\mathbb Q}',MUTED),(0,-2,'자릿수의 분포',r'3.14159\ldots',MUTED),(4.7,-1.7,'계산 공식',r'\text{BBP}',MUTED)]:
   node=card(a,b,x,y,c,w=3.3,h=1.1)
   direction=node.get_center()-center.get_center();start=center.get_center()+direction/np.linalg.norm(direction)*.85
   edge=DashedLine(start,node.get_center(),color=c,stroke_opacity=.4) if c==MUTED else Line(start,node.get_center(),color=c,stroke_width=1)
   edge.set_z_index(-1);self.add(edge);self.show(node,run_time=.35)

class Shot52(ChapterScene):
 shot=51
 def s52(self):
  a=card('푸리에 계수',r'\frac1{2\pi}',-4,1.1,VIOLET,w=4.5,h=1.6);b=card('정규분포',r'\frac1{\sqrt{2\pi}}',4,1.1,GREEN,w=4.5,h=1.6)
  c=rotor(0,-1.1,.9,theta=.8,color=GOLD);self.show(a,b,c)
  self.play(Create(link(a,c,VIOLET)),Create(link(b,c,GREEN)),run_time=1.3)
  self.show(t('같은 상수는 관계를 탐구할 단서가 된다',y=-2.55,size=27))

class Shot53(ChapterScene):
 shot=52
 def s53(self):
  positions=[[-4,1.8,0],[4,1.8,0],[-4,-1.6,0],[4,-1.6,0]]
  center=pi_center();dots=VGroup(*[Dot(p,color=BLUE,radius=.1) for p in positions]);spokes=VGroup(*[Line(ORIGIN,p,color=BLUE,stroke_width=1) for p in positions])
  self.add(spokes,center,dots);self.to(364)
  self.play(center.animate.set_opacity(.25),spokes.animate.set_stroke(opacity=.25),run_time=1)
  edges=VGroup(*[Line(positions[i],positions[j],color=VIOLET,stroke_width=1.8) for i in range(4) for j in range(i+1,4)])
  self.play(Create(edges),run_time=1.8);self.show(t('대상에 관한 지식 → 대상 사이 관계에 관한 지식',y=-2.5,size=26))

class Shot54(ChapterScene):
 shot=53
 def s54(self):
  rows=[('기하학','좌표와 함수 표현','함수와 해석학',BLUE),('푸리에 해석','파르세발 항등식','바젤 문제',VIOLET),('회전 대칭성','극좌표 변환','가우스 적분',GREEN)]
  for y,(a,b,c,col) in zip([1.8,0,-1.8],rows):
   left=card(a,'',-5,y,col,w=3.3,h=1.05);middle=card(b,'',0,y,col,w=3.7,h=1.05);right=card(c,'',5,y,col,w=3.3,h=1.05)
   for node in [left,middle,right]:node[1].move_to(node[0].get_center())
   self.show(left,middle,right);self.play(Create(link(left,middle)),Create(link(middle,right)),run_time=.7)

class Shot55(ChapterScene):
 shot=54
 def s55(self):
  center=pi_center();self.add(center);labels=['기하학','함수','멱급수','주기성','푸리에 해석','무한급수','확률론','미적분학'];nodes=[]
  for i,label in enumerate(labels):
   angle=PI-TAU*i/8;p=np.array([5.7*math.cos(angle),1.8*math.sin(angle),0]);node=Dot(p,color=VIOLET if i%2 else BLUE,radius=.07);nodes.append(node)
   text=t(label,p[0],p[1]+(.3 if p[1]>=0 else -.25),22,MUTED,width=2.5)
   self.play(Create(Line(center.get_center()+p/np.linalg.norm(p)*.85,p,color=BLUE,stroke_width=.8,stroke_opacity=.45)),FadeIn(node),FadeIn(text),run_time=.45)
  polygon=Polygon(*[n.get_center() for n in nodes],color=GOLD,stroke_width=1,stroke_opacity=.4)
  self.play(Create(polygon),run_time=1.4);self.show(t('하나의 수를 통해 발견하는 수학적 관계',y=-2.5,size=26))
