"""Thirteen independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT02_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT02_PREVIEW')=='1' else 1080
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
class DerivativeShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.02',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('미분계수',x=6.2,y=3.95,size=19,color=BASE,width=2))
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
 def quotient(self,ref='1',x=0,y=.5,coefficient='',size=50):
  # Numerator, denominator and three reference points stay independently addressable.
  num=VGroup(eq('f(x)-f(',size=size),eq(ref,size=size,color=BASE),eq(')',size=size)).arrange(RIGHT,buff=.025)
  den=VGroup(eq(coefficient+'(x-' if coefficient else 'x-',size=size),eq(ref,size=size,color=BASE),eq(')',size=size) if coefficient else VGroup()).arrange(RIGHT,buff=.025)
  w=max(num.width,den.width)+.25;num.move_to([.7,.55,0]);den.move_to([.7,-.55,0])
  line=Line([.7-w/2,0,0],[.7+w/2,0,0],stroke_width=2)
  lim=eq(r'\lim',size=size).move_to([.7-w/2-.8,.1,0])
  approach=VGroup(eq(r'x\to',size=24),eq(ref,size=24,color=BASE)).arrange(RIGHT,buff=.04).move_to(lim.get_center()+DOWN*.53)
  g=VGroup(lim,approach,num,line,den).move_to([x,y,0]);g.num=num;g.den=den;g.refs=[approach[1],num[1],den[1]]
  return g
 def opts(self,y=-1.8):
  return VGroup(*[VGroup(tx('①②③④⑤'[i],x-.3,y,23),eq(str(i+1),x+.3,y,32)) for i,x in enumerate([-5.4,-2.7,0,2.7,5.4])])
 def s01(self):
  n=tx('02',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.show(eq(r'f(x)=3x^2-x+1',y=1.5,size=48));self.to(4)
  self.show(eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{x-1}',y=-.15,size=55));self.to(7)
  self.play(LaggedStart(*[FadeIn(m) for m in self.opts()],lag_ratio=.12),run_time=1)
 def s02(self):
  self.add(eq(r'f(x)=3x^2-x+1',x=-4.7,y=2,size=29,color=MUTED,width=4.5))
  q=self.quotient(size=58);self.add(q);self.to(12)
  box=SurroundingRectangle(q.num,color=BASE,buff=.15);self.play(Create(box),run_time=.6);self.show(tx('함수값의 차이',x=4.3,y=1.15,size=27,color=BASE,width=4))
  self.to(15);self.play(Create(SurroundingRectangle(q.den,color=EXP,buff=.15)),run_time=.6)
  self.show(tx('입력값의 차이',x=4.3,y=-.2,size=27,color=EXP,width=4));self.note('분자와 분모가 어떤 변화량을 나타내는지 확인')
 def s03(self):
  q=self.quotient(y=.8,size=58);self.add(q)
  for r in q.refs:self.play(Indicate(r,color=BASE,scale_factor=1.4),run_time=1)
  self.to(23);label=tx('공통 기준점 = 1',y=-1.6,size=28,color=BASE);self.show(label)
  lines=VGroup(*[Line(r.get_bottom()+DOWN*.08,[0,-1.18,0],color=BASE,stroke_opacity=.5,stroke_width=1.3) for r in q.refs]);self.play(Create(lines),run_time=.8)
  self.to(26);self.play(FadeOut(lines),q.animate.scale(.8).move_to([0,1,0]),run_time=.6)
  self.show(eq(r'=f\,^{\prime}(1)',y=-.75,size=57,color=EXP));self.note('미분계수의 정의와 같은 형태',EXP)
 def s04(self):
  q=self.quotient(ref='a',x=1.1,y=.5);lhs=eq(r'f\,^{\prime}(a)=',x=-3.5,y=.5,size=54,color=EXP);self.add(q,lhs)
  self.note('극한이 존재하면, 그 값이 a에서의 미분계수')
  self.to(35);target=self.quotient(ref='1',x=1.1,y=.5)
  self.play(*[ReplacementTransform(a,b) for a,b in zip(q.refs,target.refs)],ReplacementTransform(lhs,eq(r'f\,^{\prime}(1)=',x=-3.5,y=.5,size=54,color=EXP)),run_time=1)
  self.to(39);self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption and (isinstance(m,MathTex) or m is q or m in target.refs)],run_time=.3)
  self.remove(q,*q.get_family(),*target.refs)
  self.show(eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{x-1}=f\,^{\prime}(1)',y=.35,size=58,color=EXP));self.note('주어진 극한 → f′(1)',BASE)
 def s05(self):
  f=eq(r'f(x)=3x^2-x+1',y=1.5,size=55);self.add(f);self.to(46)
  cols=[]
  for x,old,new,t in [(-4,'3x^2','6x',46),(0,'-x','-1',48),(4,'1','0',50)]:
   self.to(t);g=VGroup(eq(old,x,.4,48),eq(r'\downarrow',x,-.3,32,BASE),eq(new,x,-1,48,EXP));self.show(g,rt=.6);cols.append(g)
  self.to(52);self.play(*[FadeOut(g) for g in cols],FadeOut(f),run_time=.4)
  self.show(eq(r'f\,^{\prime}(x)=6x-1',y=.4,size=68,color=EXP));self.note('상수항의 도함수는 0')
 def s06(self):
  m=eq(r'f\,^{\prime}(1)=6\times1-1',y=.65,size=61);self.add(m);opts=self.opts(-1.3);self.add(opts)
  self.to(57);m=self.morph(m,eq(r'f\,^{\prime}(1)=5',y=.65,size=66,color=RESULT),rt=.5)
  self.to(58);self.play(Create(SurroundingRectangle(opts[4],color=RESULT,buff=.15)),run_time=.5);self.note('정답 ⑤',RESULT)
 def s07(self):
  self.add(eq(r'f\,^{\prime}(1)=5',x=-5,y=2,size=28,color=RESULT,width=4))
  m=eq(r'\frac{f(x)-f(1)}{x-1}',y=.5,size=65);self.add(m);self.to(63)
  self.show(eq(r'f(1)=3-1+1=3',y=-1.2,size=38,color=BASE));self.to(66)
  m=self.morph(m,eq(r'\frac{3x^2-x+1-3}{x-1}',y=.5,size=65));self.to(68)
  self.morph(m,eq(r'\frac{3x^2-x-2}{x-1}',y=.5,size=65))
 def s08(self):
  m=eq(r'\lim_{x\to1}\frac{3x^2-x-2}{x-1}',y=.55,size=57);self.add(m)
  self.to(71)
  common=eq('(x-1)',x=-.5,y=1.05,size=52,color=BASE)
  rest=eq('(3x+2)',x=2.1,y=1.05,size=52)
  denominator=eq('x-1',x=.8,y=-.15,size=52,color=BASE)
  bar=Line([-1.9,.5,0],[3.8,.5,0],stroke_width=2)
  lim=eq(r'\lim_{x\to1}',x=-3,y=.5,size=45)
  factored=VGroup(common,rest,denominator,bar,lim)
  self.play(ReplacementTransform(m,factored),run_time=.7);m=factored
  self.play(Create(SurroundingRectangle(common,color=BASE,buff=.08)),Create(SurroundingRectangle(denominator,color=BASE,buff=.08)),run_time=.6)
  self.note('공통인수: x − 1',BASE)
  self.to(75);self.note('약분은 x ≠ 1에서 수행한 뒤, x → 1의 극한을 취한다')
  marks=VGroup(Line(common.get_left()+DOWN*.1,common.get_right()+UP*.1,color=BASE),Line(denominator.get_left()+DOWN*.1,denominator.get_right()+UP*.1,color=BASE))
  self.play(Create(marks),run_time=.6)
  self.to(77)
  for o in list(self.mobjects):
   if isinstance(o,SurroundingRectangle):self.remove(o)
  self.remove(marks)
  m=self.morph(m,eq(r'\lim_{x\to1}(3x+2)',y=.55,size=62));self.to(79)
  self.morph(m,eq(r'3(1)+2=5',y=.55,size=68,color=RESULT));self.note('대수적으로 계산해도 같은 극한값',RESULT)
 def s09(self):
  left=VGroup(tx('미분계수 활용',-3.7,1.5,28,BASE,width=6),eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{x-1}',-3.7,.35,42,width=6),eq(r'\downarrow\;f\,^{\prime}(1)=5',-3.7,-1.15,45,RESULT,width=6))
  right=VGroup(tx('대수적 풀이',3.7,1.5,28,MUTED,width=6),eq(r'3x^2-x-2',3.7,.5,42,width=6),eq(r'\downarrow\;(x-1)(3x+2)',3.7,-.4,37,width=6),eq(r'\longrightarrow 5',3.7,-1.3,39,RESULT,width=6))
  self.show(left,right);self.to(86);self.play(Create(SurroundingRectangle(left,color=RESULT,buff=.2)),run_time=.6);self.note('형태를 알아보면 전개와 인수분해를 줄일 수 있다',BASE)
 def s10(self):
  self.note('분자·분모의 변화량이 서로 대응하는가?',WARN);self.to(91)
  q=self.quotient(x=-1,y=.6);self.show(q)
  self.show(tx('입력 변화량: x − 1',x=4,y=1,size=27,color=BASE,width=5),tx('실제 분모: x − 1',x=4,y=-.3,size=27,color=BASE,width=5))
  self.play(Create(SurroundingRectangle(q.den,color=BASE,buff=.15)),run_time=.6)
 def s11(self):
  q=self.quotient(y=.55);self.add(q);self.to(97)
  m=eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{2x-2}',y=.55,size=62,color=WARN);self.play(ReplacementTransform(q,m),run_time=.7)
  self.to(100);m=self.morph(m,eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{2(x-1)}',y=.55,size=62,color=WARN));self.note('2x − 2 = 2(x − 1)',WARN)
  self.to(102);m=self.morph(m,eq(r'\frac12\lim_{x\to1}\frac{f(x)-f(1)}{x-1}',y=.55,size=62,color=EXP))
  self.to(104);m=self.morph(m,eq(r'\frac12 f\,^{\prime}(1)',y=.55,size=74,color=RESULT));self.note('분모의 계수 2 → 결과에 1/2을 곱한다',WARN)
 def s12(self):
  self.show(tx('변화량이 일치',-3.5,1.5,27,BASE,width=6),tx('계수 2가 추가',3.5,1.5,27,WARN,width=6),eq(r'x-1',-3.5,.5,60,BASE,width=6),eq(r'2(x-1)',3.5,.5,60,WARN,width=6))
  self.to(110);self.show(eq(r'\downarrow\ f\,^{\prime}(1)',-3.5,-.9,50,RESULT,width=6),eq(r'\downarrow\ \frac12f\,^{\prime}(1)',3.5,-.9,50,RESULT,width=6));self.note('입력 변화량과 분모를 정확히 비교한다')
 def s13(self):
  cards=VGroup(*[VGroup(RoundedRectangle(width=4.1,height=1.05,corner_radius=.12,stroke_color=c,stroke_width=1.5).move_to([x,1.4,0]),tx(s,x,1.4,27,c,width=3.8)) for x,s,c in [(-4.6,'① 형태 확인',BASE),(0,'② 기준점 찾기',BASE),(4.6,'③ 계수 확인',WARN)]])
  self.play(LaggedStart(*[FadeIn(m) for m in cards],lag_ratio=.3),run_time=2)
  self.to(117);m=eq(r'\lim_{x\to1}\frac{f(x)-f(1)}{x-1}',y=-.25,size=58);self.show(m)
  self.to(119);m=self.morph(m,eq(r'f\,^{\prime}(1)=6-1=5',y=-.25,size=64,color=RESULT));self.note('정답 ⑤  ·  전개하기 전에 미분계수인지 확인',BASE)
  self.to(122);self.show(tx('02 / 30',y=-1.2,size=22,color=MUTED));self.to(123.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(13):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(DerivativeShot,),{'shot':i,'__module__':__name__})
