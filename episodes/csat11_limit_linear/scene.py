"""Twenty-eight independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT11_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT11_PREVIEW')=='1' else 1080
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
  self.add(tx('수능 수학  /  EP.11',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('극한과 일차함수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')


 def change(self,m,s,t=None,y=.5,color=REL,size=72,x=0,width=13):
  if t is not None:self.to(t)
  n=eq(s,x=x,y=y,size=size,color=color,width=width);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def left(self,s,y=.5,size=57,color=INK):return eq(s,-3.7,y,size,color,width=6.1)
 def given(self,t,y=.6,size=65):return eq(r'\lim_{x\to '+str(t)+r'}\frac{f(x+2)}{x(f(x)-3)}',y=y,size=size)
 def pair(self):self.add(card('f(2)=0',-3.4,1.8,BASE),card('f(3)=3',3.4,1.8,WARN))
 def linear(self,line=False,third=False):
  ax=Axes(x_range=[0,5,1],y_range=[-1,7,1],x_length=6.2,y_length=3.75,tips=False,axis_config={'color':MUTED,'stroke_width':1.2,'include_ticks':True}).move_to([3.45,.1,0]);self.ax=ax
  labs=VGroup(*[eq(str(v),*(ax.c2p(v,0)+DOWN*.25)[:2],size=20,color=MUTED) for v in [0,1,2,3,4,5]],*[eq(str(v),*(ax.c2p(0,v)+LEFT*.22)[:2],size=20,color=MUTED) for v in [3,6]])
  dots=VGroup(Dot(ax.c2p(2,0),radius=.075,color=BASE),Dot(ax.c2p(3,3),radius=.075,color=WARN));labels=VGroup(eq('(2,0)',*(ax.c2p(2,0)+LEFT*.65+DOWN*.65)[:2],size=28,color=BASE),eq('(3,3)',*(ax.c2p(3,3)+LEFT*.75+UP*.35)[:2],size=28,color=WARN))
  self.add(ax,labs,dots,labels)
  self.line_graph=ax.plot(lambda x:3*x-6,x_range=[5/3,13/3],color=REL,stroke_width=2.7)
  if line:self.add(self.line_graph)
  if third:self.add(Dot(ax.c2p(4,6),radius=.08,color=RESULT),eq('(4,6)',*(ax.c2p(4,6)+LEFT*.7+UP*.3)[:2],size=28,color=RESULT))
  return ax
 def rational(self):
  ax=Axes(x_range=[-1,6,1],y_range=[-4,4,1],x_length=6.3,y_length=3.6,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.35,.05,0]);self.ax=ax
  labs=VGroup(*[eq(str(v),*(ax.c2p(v,0)+DOWN*.25)[:2],size=20,color=MUTED) for v in [0,3,6]],eq('x',*(ax.c2p(6,0)+RIGHT*.25)[:2],size=22,color=MUTED))
  branches=VGroup(ax.plot(lambda x:1/(x-3),x_range=[-1,2.74,.01],color=BASE,stroke_width=2.3,use_smoothing=False),ax.plot(lambda x:1/(x-3),x_range=[3.26,6,.01],color=REL,stroke_width=2.3,use_smoothing=False))
  asym=DashedLine(ax.c2p(3,-4),ax.c2p(3,4),color=WARN,stroke_width=1.4,dash_length=.08)
  hole=Circle(radius=.07,color=EXP,stroke_width=2,fill_color=config.background_color,fill_opacity=1).move_to(ax.c2p(0,-1/3)).set_z_index(6)
  self.add(ax,labs,asym,branches,hole);self.hole=hole;return ax
 def s01(self):
  n=tx('11',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  self.show(eq(r'\lim_{x\to a}\frac{f(x+2)}{x(f(x)-3)}',y=1.25,size=64),rt=1);self.to(4)
  self.show(tx('a = 0: 유한한 극한 존재',-3.5,-.45,27,BASE,width=6),tx('a = 3: 극한 미존재',3.5,-.45,27,WARN,width=6));self.to(7)
  self.show(eq('f(4)=?',y=-1.9,size=51,color=EXP))
 def s02(self):
  a=card('a=0',-3.4,1.1,BASE);b=card('a=3',3.4,1.1,WARN);self.add(a,b,tx('존재하려면?',-3.4,-.4,33,BASE,width=6),tx('존재하지 않으려면?',3.4,-.4,33,WARN,width=6));self.to(13)
  self.play(Indicate(a,color=BASE),b.animate.set_opacity(.4),run_time=1);self.note('극한의 값보다 존재 조건을 먼저 분석한다')
 def s03(self):
  self.add(self.given(0,y=1.4,size=63));self.to(19)
  self.show(eq(r'x\to0',-3.4,-.2,58,BASE,width=6),eq(r'f(x)-3\to f(0)-3',3.2,-.2,42,REL,width=6));self.to(22)
  self.show(eq(r'x(f(x)-3)\to0',y=-1.6,size=57,color=BASE));self.to(24)
 def s04(self):
  self.add(tx('문제의 조건: 유한한 극한값 존재',y=1.9,size=31,color=BASE));self.to(29)
  self.show(tx('개념 예시 · 실제 함수값이 아님',y=1.05,size=23,color=MUTED),eq(r'\frac1{0.1}=10\qquad\frac1{0.01}=100',y=-.15,size=64,color=WARN));self.to(33)
  self.note('분자 → 0이 아닌 값, 분모 → 0이면 유한한 수렴 불가능',WARN)
 def s05(self):
  self.add(eq(r'f(x+2)\to0',y=.9,size=83,color=BASE));self.to(38)
  self.show(eq(r'x\to0\quad\Rightarrow\quad x+2\to2',y=-.8,size=52,color=EXP),rt=.5)
 def s06(self):
  self.add(eq(r'x\to0\quad\Rightarrow\quad x+2\to2',y=1.65,size=49));m=eq(r'f(x+2)\to f(2)',size=76,color=BASE);self.show(m);self.to(42)
  self.change(m,r'f(2)=0',color=BASE,size=90);self.to(45);self.note('극한이 존재하기 위해 필요한 조건',BASE)
 def s07(self):
  self.add(card('f(2)=0',-4.8,1.95,BASE,width=3.6));self.to(49)
  self.show(self.given(3,y=.15,size=70));self.to(52);self.note('유한한 극한값이 존재하지 않는다',WARN)
 def s08(self):
  self.add(eq(r'f(x)=mx+n\quad(m\ne0)',y=1.8,size=53,color=REL));self.to(57)
  m=eq(r'x(f(x)-3)',size=74);self.add(m);self.change(m,r'3(f(3)-3)',59,size=74,color=WARN);self.to(61)
  self.note('분모의 극한이 0이 아니면 → 연속성으로 대입 가능',BASE)
 def s09(self):
  self.add(tx('분모의 극한이 0이 아니면 → 유한한 극한 존재',y=1.7,size=28,color=MUTED));self.to(65)
  self.show(tx('실제로 극한이 없으므로',y=.7,size=31,color=WARN));self.to(67)
  self.show(eq(r'3(f(3)-3)=0',y=-.5,size=77,color=WARN));self.note('미존재 조건에서 얻은 필요조건')
 def s10(self):
  m=eq(r'x(f(x)-3)',size=83);self.add(m);self.to(73)
  m=self.change(m,r'3(f(3)-3)=0',color=WARN,size=80);self.show(eq(r'3\ne0',y=-1.6,size=45,color=EXP));self.to(76)
  m=self.change(m,r'f(3)-3=0',color=WARN,size=83);self.to(79);self.change(m,'f(3)=3',color=WARN,size=90)
 def s11(self):
  a=eq('f(2)=0',-3.4,.7,77,BASE,width=6);b=eq('f(3)=3',3.4,.7,77,WARN,width=6);self.add(a,b);self.to(83)
  self.play(TransformMatchingTex(a,eq('(2,0)',-3.4,.7,85,BASE,width=6)),TransformMatchingTex(b,eq('(3,3)',3.4,.7,85,WARN,width=6)),run_time=.8)
 def s12(self):
  self.add(self.left(r'f(x)=mx+n',y=1.3,size=53,color=REL),tx('일차함수',-3.7,-.2,38,REL,width=6));self.to(89)
  self.linear();self.to(92);self.play(Create(self.line_graph.copy().set_opacity(.35)),run_time=1);self.note('서로 다른 두 점을 지나는 직선은 하나')
 def s13(self):
  ax=self.linear();self.add(self.left(r'(2,0),\quad(3,3)',y=1.1,size=52,color=EXP));seg=Line(ax.c2p(2,0),ax.c2p(3,3),color=REL,stroke_width=3)
  self.play(Create(seg),run_time=1.5);self.to(96);self.play(ReplacementTransform(seg,self.line_graph),run_time=1.2);self.note('이 두 점을 지나는 일차함수')
 def s14(self):
  ax=self.linear(line=True);self.add(self.left(r'\Delta x=3-2=1',y=1.5,size=46,color=BASE));self.play(Create(Line(ax.c2p(2,0),ax.c2p(3,0),color=BASE,stroke_width=4)),run_time=.7);self.to(101)
  self.show(self.left(r'\Delta y=3-0=3',y=.2,size=46,color=WARN));self.play(Create(Line(ax.c2p(3,0),ax.c2p(3,3),color=WARN,stroke_width=4)),run_time=.7);self.to(103)
  self.show(self.left(r'm=\frac{\Delta y}{\Delta x}=\frac31=3',y=-1.25,size=49,color=RESULT),rt=.6)
 def s15(self):
  self.linear(line=True);m=self.left(r'f(x)=m(x-x_1)+y_1',y=1.15,size=46);self.add(m);self.to(105)
  m=self.change(m,r'f(x)=3(x-2)',x=-3.7,y=1.15,width=6.1,size=57,color=REL);self.to(111)
  self.change(m,r'f(x)=3x-6',x=-3.7,y=1.15,width=6.1,size=61,color=RESULT)
 def s16(self):
  ax=self.linear(line=True);m=self.left('f(4)=?',y=.9,size=73,color=EXP);self.add(m);self.to(116)
  m=self.change(m,r'f(4)=3\cdot4-6',x=-3.7,y=.9,width=6.1,size=58,color=REL)
  self.play(Create(DashedLine(ax.c2p(4,0),ax.c2p(4,6),color=RESULT)),FadeIn(Dot(ax.c2p(4,6),radius=.08,color=RESULT)),FadeIn(eq('(4,6)',*(ax.c2p(4,6)+LEFT*.7+UP*.3)[:2],size=28,color=RESULT)),run_time=.8);self.to(119)
  self.change(m,'f(4)=12-6=6',x=-3.7,y=.9,width=6.1,size=61,color=RESULT)
 def s17(self):
  self.add(eq(r'f(4)=\boxed6',y=.8,size=97,color=RESULT),tx('정답 ①',y=-1.35,size=38,color=RESULT))
 def s18(self):
  self.add(eq('f(x)=3x-6',y=1.85,size=49,color=RESULT));self.to(126)
  m=eq(r'f(x+2)=3(x+2)-6',size=70,color=REL);self.show(m);self.to(129)
  m=self.change(m,r'f(x+2)=3x+6-6',size=71,color=REL);self.change(m,r'f(x+2)=3x',131,size=81,color=BASE)
 def s19(self):
  m=eq(r'\frac{f(x+2)}{x(f(x)-3)}',size=89);self.add(m);m=self.change(m,r'\frac{3x}{x(f(x)-3)}',133,size=89,color=REL)
  self.change(m,r'\frac{3x}{x(3x-9)}',135,size=89,color=REL)
 def s20(self):
  m=eq(r'\frac{3x}{x(3x-9)}',size=91,color=REL);self.add(m);m=self.change(m,r'\frac3{3x-9}',138,size=91,color=REL)
  m=self.change(m,r'R(x)=\frac1{x-3}',140,size=91,color=REL);self.to(141);self.show(eq(r'x\ne0,\quad x\ne3',y=-1.65,size=51,color=WARN))
 def s21(self):
  ax=self.rational();self.add(self.left(r'\lim_{x\to0}R(x)=-\frac13',y=1.2,size=53,color=BASE),self.left(r'x\ne0,3',y=-.35,size=38,color=WARN))
  tr=ValueTracker(.7);a=Dot(radius=.05,color=EXP).add_updater(lambda m:m.move_to(ax.c2p(-tr.get_value(),1/(-tr.get_value()-3))));b=Dot(radius=.05,color=EXP).add_updater(lambda m:m.move_to(ax.c2p(tr.get_value(),1/(tr.get_value()-3))));self.add(a,b)
  self.to(145);self.play(tr.animate.set_value(.06),run_time=1.5,rate_func=linear);self.note('원래 식의 x = 0은 빈 점 · 극한값은 −1/3',BASE)
 def s22(self):
  ax=self.rational();self.add(self.left(r'\lim_{x\to3^-}R(x)=-\infty',y=1.3,size=46,color=WARN),self.left(r'\lim_{x\to3^+}R(x)=+\infty',y=-.25,size=46,color=REL));self.to(150)
  self.play(Indicate(DashedLine(ax.c2p(3,-4),ax.c2p(3,4),color=WARN),color=WARN),run_time=.8);self.to(152)
  tr=ValueTracker(1);a=Dot(radius=.06,color=WARN).add_updater(lambda m:m.move_to(ax.c2p(3-tr.get_value(),-1/tr.get_value())));b=Dot(radius=.06,color=REL).add_updater(lambda m:m.move_to(ax.c2p(3+tr.get_value(),1/tr.get_value())));self.add(a,b);self.play(tr.animate.set_value(.26),run_time=1.5,rate_func=linear);self.to(154)
  self.note('x → 0: 존재  ✓      x → 3: 미존재  ✓',RESULT)
 def s23(self):
  self.add(tx('0/0은 극한의 형태이지 계산 결과가 아니다',y=1.9,size=29,color=WARN));self.to(158)
  self.show(eq(r'\frac{x}{x}=1\quad(x\ne0)',-3.6,.65,61,BASE,width=6),eq(r'\frac{x}{x^2}=\frac1x\quad(x\ne0)',3.6,.65,57,WARN,width=6));self.to(161)
  self.show(tx('x → 0: 유한한 극한 존재',-3.6,-1.1,27,BASE,width=6),tx('x → 0: 극한 미존재',3.6,-1.1,27,WARN,width=6))
 def s24(self):
  self.add(card('f(2)=0',-3.4,.8,BASE),tx('필요조건 도출',-3.4,-.5,29,BASE,width=6));self.to(166)
  self.show(eq(r'\lim_{x\to0}\frac1{x-3}=-\frac13',3.4,.8,51,RESULT,width=6),tx('실제 식을 정리해 검증',3.4,-.5,29,RESULT,width=6));self.note('필요조건만으로 끝내지 않고 실제 극한을 확인')
 def s25(self):
  a=eq(r'\frac{x-3}{x-3}',-3.6,.8,78,BASE,width=6);b=eq(r'\frac1{x-3}',3.6,.8,78,WARN,width=6);self.add(a,b,tx('개념 예시 · x → 3',y=1.95,size=26,color=MUTED));self.to(172)
  self.play(TransformMatchingTex(a,eq(r'1\quad(x\ne3)',-3.6,.8,61,BASE,width=6)),run_time=.8);self.show(tx('약분 후 극한값 1',-3.6,-.8,30,BASE,width=6));self.to(176)
  self.show(tx('좌 −∞ / 우 +∞',3.6,-.8,30,WARN,width=6));self.note('분모 → 0만으로 극한 미존재를 단정하지 않는다',WARN)
 def s26(self):
  self.show(tx('① 분모 확인',-4.7,1.7,29,WARN,width=4.4),eq(r'x(f(x)-3)',-4.7,.4,45,WARN,width=4.4));self.to(183)
  self.show(tx('② 분자 분석',0,1.7,29,BASE,width=4.4),eq(r'f(x+2)',0,.4,48,BASE,width=4.4));self.to(186)
  self.show(tx('③ 함수값 조건',4.7,1.7,29,EXP,width=4.4),eq('f(2)=0',4.7,.55,43,EXP,width=4.4),eq('f(3)=3',4.7,-.4,43,EXP,width=4.4));self.note('극한 존재 여부를 미지 함수의 조건으로 바꾼다')
 def s27(self):
  self.linear();self.add(self.left(r'f(2)=0,\ f(3)=3',y=1.2,size=48,color=EXP));self.to(192);self.play(Create(self.line_graph),run_time=1.3);self.to(195)
  self.show(self.left(r'f(x)=3x-6',y=-.5,size=64,color=RESULT))
 def s28(self):
  self.add(eq(r'f(2)=0,\quad f(3)=3',y=1.7,size=55,color=EXP),eq('f(x)=3x-6',y=.25,size=65,color=RESULT),eq(r'f(4)=\boxed6',y=-1.3,size=75,color=RESULT));self.to(199.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(28):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(LimitShot,),{'shot':i,'__module__':__name__})
