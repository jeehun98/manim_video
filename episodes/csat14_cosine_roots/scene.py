"""Thirty-four independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT14_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT14_PREVIEW')=='1' else 1080
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
class CosineShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.14',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('코사인과 실근 개수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def roots(c,b=1):
  if c < -1-1e-10 or c > 1+1e-10:return []
  q=np.arccos(np.clip(c,-1,1));values=[]
  for k in range(-1,b+2):
   for angle in [q+2*np.pi*k,-q+2*np.pi*k]:
    x=angle/(b*np.pi)
    if -1e-9<=x<=2+1e-9 and not any(abs(x-v)<1e-8 for v in values):values.append(float(np.clip(x,0,2)))
  return sorted(values)
 def graph(self,b=1,theta=True,example=False):
  self.cycles=b;self.theta_mode=theta
  ax=Axes(x_range=[0,2,1/b],y_range=[-1.7,1.3,1],x_length=6.35,y_length=3.6,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  curve=ax.plot(lambda x:np.cos(b*np.pi*x),x_range=[0,2,.005],color=INK,stroke_width=2.3,use_smoothing=False);self.add(ax,curve)
  marks=[(0,'0'),(1,r'\pi'),(2,r'2\pi')] if theta else [(0,'0'),(2,'2')]
  self.add(*[eq(s,*(ax.c2p(x,0)+DOWN*.29)[:2],size=23,color=MUTED) for x,s in marks],*[eq(str(y),*(ax.c2p(0,y)+LEFT*.25)[:2],size=23,color=MUTED) for y in [-1,1]])
  label='입력각 θ · 코사인 한 주기' if theta else (f'예시: b = {b} · 0 ≤ x ≤ 2' if example else f'b = {b} · 0 ≤ x ≤ 2')
  self.add(tx(label,3.4,2.25,22,MUTED,width=6.6))
  return ax
 def level(self,c,color=REL,points=True):
  tracker=ValueTracker(c);ax=self.ax;b=self.cycles
  line=always_redraw(lambda:Line(ax.c2p(0,tracker.get_value()),ax.c2p(2,tracker.get_value()),color=color,stroke_width=1.8))
  group=VGroup(line)
  if points:
   dots=always_redraw(lambda:VGroup(*[Dot(ax.c2p(x,tracker.get_value()),radius=.065,color=EXP,stroke_width=1,stroke_color=config.background_color) for x in CosineShot.roots(tracker.get_value(),b)]).set_z_index(5));group.add(dots)
  self.add(group);return tracker,group
 def count(self,n,color=EXP):self.note(f'한 주기에서 서로 다른 교점 {n}개',color)
 def s01(self):
  n=tx('14',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=2)
  self.show(eq(r'\left(\cos(b\pi x)-\frac12\right)\left(a\cos(b\pi x)+\frac{a+2}{2}\right)=0',y=1.15,size=53),rt=1);self.to(5)
  self.show(eq(r'0\le x\le2,\quad a>0,\quad b\in\mathbb N',y=-.25,size=49));self.to(7)
  self.show(tx('서로 다른 실근 15개',-3.2,-1.75,31,EXP,width=6),eq('a+b=?',3.2,-1.75,56,EXP,width=6))
 def s02(self):
  self.graph();self.add(self.left(r'\cos\theta=c',y=1.1,size=69,color=REL));self.to(12);self.level(.5,BASE);self.note('실근의 개수 = 그래프와 수평선의 교점 개수',EXP)
 def s03(self):
  m=eq(r'\left(\cos(b\pi x)-\frac12\right)\left(a\cos(b\pi x)+\frac{a+2}{2}\right)=0',size=55);self.add(m);self.to(19)
  self.play(Indicate(m,color=EXP),run_time=1);self.change(m,r'A(x)\cdot B(x)=0',22,size=87);self.to(26)
  self.show(eq('A(x)=0',-3.5,-1.35,65,BASE,width=6),eq('B(x)=0',3.5,-1.35,65,REL,width=6))
 def s04(self):
  m=eq(r'\cos(b\pi x)-\frac12=0',size=87,color=BASE);self.add(m);self.change(m,r'\cos(b\pi x)=\frac12',30,size=91,color=BASE)
 def s05(self):
  m=eq(r'a\cos(b\pi x)+\frac{a+2}{2}=0',size=75,color=REL);self.add(m);m=self.change(m,r'a\cos(b\pi x)=-\frac{a+2}{2}',37,size=77);self.change(m,r'\cos(b\pi x)=-\frac{a+2}{2a}',40,size=83);self.note('a > 0이므로 양변을 a로 나눌 수 있다')
 def s06(self):
  self.add(eq(r'y=\cos\theta',y=1.8,size=61));self.to(48);self.graph();self.to(52)
  self.show(self.left(r'\cos(\theta+2\pi)=\cos\theta',y=.8,size=43,color=EXP));self.note('입력각이 2π 증가하면 같은 모양을 반복')
 def s07(self):
  self.graph();m=self.left(r'\theta=b\pi x',y=1.3,size=62,color=REL);self.add(m);self.to(60)
  m=self.change(m,r'b\pi T=2\pi',x=-3.7,y=1.3,width=6.1,size=65);self.change(m,r'T=\frac2b',62,x=-3.7,y=1.3,width=6.1,size=81,color=RESULT);self.note('x가 2/b 증가하면 입력각은 2π 증가')
 def s08(self):
  ax=self.graph(3,theta=False,example=True);self.add(self.left(r'T=\frac2b',y=1.3,size=65,color=REL));self.to(68)
  self.show(self.left(r'\frac{2}{2/b}=b',y=-.3,size=73,color=RESULT));self.play(*[Create(DashedLine(ax.c2p(x,-1.25),ax.c2p(x,1.05),color=MUTED,stroke_width=1)) for x in [2/3,4/3]],run_time=.8);self.note('길이 2인 구간에 b개의 완전한 주기')
 def s09(self):
  self.graph();self.add(self.left(r'\cos(b\pi x)=\frac12',y=1.1,size=58,color=BASE));self.to(74);self.level(.5,BASE);self.to(76);self.count(2)
 def s10(self):
  self.graph(3,theta=False,example=True);self.level(.5,BASE);self.add(self.left(r'2\times b',y=1.25,size=83,color=EXP));self.to(80)
  self.show(self.left('N_1=2b',y=-.35,size=81,color=BASE))
 def s11(self):
  ax=self.graph(3,theta=False,example=True);self.level(.5,BASE);self.add(self.left(r'\cos0=1',y=1.4,size=58),self.left(r'\cos(2b\pi)=1',y=.1,size=52));self.to(85)
  self.add(Dot(ax.c2p(0,1),color=WARN),Dot(ax.c2p(2,1),color=WARN));self.note('끝점의 값 1 ≠ 1/2 → 추가되는 해 없음',WARN)
 def s12(self):
  ax=self.graph();self.to(89)
  self.show(self.left(r'-1\le\cos(b\pi x)\le1',y=.9,size=50,color=EXP));self.add(DashedLine(ax.c2p(0,1),ax.c2p(2,1),color=MUTED),DashedLine(ax.c2p(0,-1),ax.c2p(2,-1),color=MUTED));self.note('코사인 그래프의 높이는 −1부터 1 사이')
 def s13(self):
  self.graph();self.level(-.75,REL);self.add(self.left(r'c(a)=-\frac{a+2}{2a}',y=1.2,size=63,color=REL));self.to(98)
  self.show(self.left(r'a>0\quad\Rightarrow\quad c(a)<0',y=-.35,size=45,color=EXP));self.note('두 번째 수평선은 항상 x축 아래 · 표시 높이는 예시')
 def s14(self):
  m=eq(r'-\frac{a+2}{2a}\ge-1',size=92,color=REL);self.add(m);m=self.change(m,r'a+2\le2a',106,size=94);self.change(m,r'a\ge2',108,size=106,color=RESULT);self.note('−2a < 0을 곱하면 부등호 방향이 바뀐다',WARN)
 def s15(self):
  self.add(card('0<a<2',-4.6,.6,WARN,width=4),card('a=2',0,.6,EXP,width=4),card('a>2',4.6,.6,REL,width=4))
 def s16(self):
  self.graph();self.add(self.left('0<a<2',y=1.4,size=74,color=WARN));tr,_=self.level(-.8,REL);self.play(tr.animate.set_value(-1.5),run_time=2);self.to(118)
  self.show(self.left(r'a=1\ \Rightarrow\ c=-\frac32',y=-.1,size=48,color=REL));self.note('높이 예시 a = 1 · 일반적으로 c(a) < −1');self.to(120)
  self.show(self.left('N_2=0',y=-1.2,size=57,color=WARN))
 def s17(self):
  self.add(eq(r'N_1=2b,\quad N_2=0',y=1.4,size=69));self.show(eq('N=2b',y=-.25,size=105,color=WARN));self.note('0 < a < 2인 경우')
 def s18(self):
  self.graph();tr,_=self.level(-1.5,REL);self.add(self.left('a>2',y=1.4,size=77,color=REL));self.play(tr.animate.set_value(-.75),run_time=3);self.to(133)
  self.show(self.left(r'a=4\ \Rightarrow\ c=-\frac34',y=0,size=48,color=REL));self.to(136);self.count(2);self.to(139)
  self.show(self.left('-1<c(a)<0',y=-1.1,size=54,color=EXP))
 def s19(self):
  self.graph();self.level(.5,BASE);self.level(-.75,REL);self.add(self.left('N_1=2b',y=1.4,size=65,color=BASE),self.left('N_2=2b',y=.1,size=65,color=REL));self.to(144)
  self.note('두 수평선의 높이가 다르므로 같은 x가 해일 수 없다');self.to(147)
  self.show(self.left('N=4b',y=-1.05,size=65,color=EXP))
 def s20(self):
  self.add(eq('N=15',y=1.9,size=83,color=EXP));self.to(153)
  a=card('N=2b',-3.5,.2,WARN);b=card('N=4b',3.5,.2,WARN);self.show(a,b);self.note('자연수 b에 대해 2b와 4b는 항상 짝수');self.to(157)
  self.play(Create(Cross(a,stroke_color=WARN,stroke_width=3)),Create(Cross(b,stroke_color=WARN,stroke_width=3)),run_time=1)
 def s21(self):
  self.add(eq('a=2',y=1.8,size=76,color=RESULT));self.to(163)
  m=eq(r'\cos(b\pi x)=-\frac{2+2}{2\cdot2}',size=83,color=REL);self.show(m);self.change(m,r'\cos(b\pi x)=-1',166,size=92)
 def s22(self):
  self.graph();tr,_=self.level(-1.4,REL);self.add(self.left(r'\min\cos\theta=-1',y=1.3,size=60,color=EXP));self.to(170)
  self.play(tr.animate.set_value(-1),run_time=3,rate_func=linear);self.to(173);self.count(1);self.to(176)
  self.show(self.left('N_2=b',y=-.3,size=82,color=REL))
 def s23(self):
  self.graph(3,theta=False,example=True);self.level(-1,REL);self.add(self.left('N_2=b',y=.8,size=100,color=REL));self.note('각 주기의 최저점에서 하나씩')
 def s24(self):
  m=eq('2b+b=15',size=97,color=EXP);self.add(m);m=self.change(m,'3b=15',184,size=104);self.change(m,'b=5',186,size=113,color=RESULT)
 def s25(self):
  self.add(card('a=2',-3.4,1.8,RESULT),card('b=5',3.4,1.8,RESULT));self.to(192)
  self.show(eq(r'a+b=2+5=\boxed7',y=-.2,size=95,color=RESULT));self.to(194);self.show(tx('정답 ③',y=-1.85,size=34,color=RESULT),rt=.5)
 def s26(self):
  self.graph();self.add(self.left(r'\cos\theta=c',y=1.25,size=77,color=REL));self.to(197)
  tr,_=self.level(-.7,REL);self.to(200);self.play(tr.animate.set_value(-.9),run_time=1.4);self.note('수평선의 높이에 따라 교점 개수가 변한다')
 def s27(self):
  self.graph();self.level(-.7,REL);self.add(self.left(r'-1<c<1',y=1.3,size=77,color=REL));self.to(205);self.show(self.left('2',y=-.2,size=110,color=EXP));self.count(2)
 def s28(self):
  self.graph();tr,_=self.level(-.7,REL);self.add(self.left(r'c\to-1^+',y=1.2,size=88,color=REL));self.play(tr.animate.set_value(-.97),run_time=2,rate_func=linear);self.to(210)
  self.play(tr.animate.set_value(-1),run_time=2,rate_func=linear);self.note('같은 최저점으로 모여 서로 다른 교점은 하나가 된다',RESULT)
 def s29(self):
  ax=self.graph();self.level(-1,REL);m=self.left(r'2\ \longrightarrow\ 1',y=1,size=95,color=EXP);self.add(m);self.to(216)
  self.play(Indicate(Dot(ax.c2p(1,-1),radius=.09,color=EXP),color=EXP),run_time=.8);self.count(1,RESULT)
 def s30(self):
  self.graph(5,theta=False);self.level(.5,BASE);self.add(self.left('N_1=10',y=1.2,size=77,color=BASE));self.to(220)
  self.level(-1,REL);self.show(self.left('N_2=5',y=-.1,size=77,color=REL));self.note('10개 + 5개 = 15개의 서로 다른 실근',RESULT)
 def s31(self):
  self.graph();self.add(self.left(r'c_1=\frac12>0',y=1.4,size=61,color=BASE),self.left(r'c_2=-\frac{a+2}{2a}<0',y=-.1,size=50,color=REL));self.to(228)
  self.level(.5,BASE);self.level(-1,REL);self.to(232);self.note('같은 x에서 코사인값이 양수이면서 음수일 수 없다',EXP)
 def s32(self):
  self.show(tx('① 방정식 분리',-4.7,1.7,29,BASE,width=4.4),eq('A(x)B(x)=0',-4.7,.3,46,BASE,width=4.4));self.to(239)
  self.show(tx('② 주기 계산',0,1.7,29,REL,width=4.4),eq(r'T=\frac2b',0,.3,65,REL,width=4.4));self.to(242)
  self.show(tx('③ 교점 확인',4.7,1.7,29,EXP,width=4.4),eq('N=15',4.7,.3,66,EXP,width=4.4));self.note('방정식과 그래프를 대응해 실근을 센다')
 def s33(self):
  self.graph();self.level(-1,REL);self.add(self.left(r'\cos(b\pi x)=-1',y=1.25,size=58,color=REL));self.to(249)
  self.show(self.left('2b+b=15',y=-.2,size=77,color=EXP));self.count(1,RESULT)
 def s34(self):
  self.add(eq(r'a=2,\quad b=5',y=1.6,size=66,color=RESULT),eq(r'a+b=\boxed7',y=.05,size=91,color=RESULT),tx('정답 ③',y=-1.6,size=35,color=RESULT));self.to(254.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(34):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(CosineShot,),{'shot':i,'__module__':__name__})
