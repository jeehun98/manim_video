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
config.pixel_width=640 if os.getenv('CSAT10_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT10_PREVIEW')=='1' else 1080
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
class LogShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.10',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('로그의 밑변환',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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

 def change(self,m,s,t=None,y=.5,color=REL,size=72):
  if t is not None:self.to(t)
  n=eq(s,y=y,size=size,color=color);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def values(self):self.add(card(r'x=\frac83',-3.3,1.85,REL),card(r'y=\frac23',3.3,1.85,REL))
 def pair(self):self.add(eq(r'\frac{x}{2}+y=2',-3.5,1.65,45,width=6),eq('x=4y',3.5,1.65,45,color=REL,width=6))
 def s01(self):
  n=tx('10',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  self.show(eq(r'\log_9 a+\log_3 b=2',y=1.3,size=60),rt=1);self.to(3)
  self.show(eq(r'\log_3 a=8\log_9 b',y=-.05,size=60),rt=1);self.to(6)
  self.show(eq(r'a,b>0\qquad \frac ab=?',y=-1.7,size=48,color=EXP))
 def s02(self):
  a=eq(r'\log_9 a,\quad\log_9 b',-3.5,.55,59,BASE,width=6);b=eq(r'\log_3 a,\quad\log_3 b',3.5,.55,59,REL,width=6)
  self.add(a,b,tx('밑이 9',-3.5,1.7,30,BASE),tx('밑이 3',3.5,1.7,30,REL));self.to(12)
  self.play(Indicate(a,color=BASE),Indicate(b,color=REL),run_time=1);self.to(15);self.note('밑을 통일할 수 있을까?',EXP)
 def s03(self):
  m=eq('9',y=1.65,size=65,color=BASE);self.add(m);self.change(m,'9=3^2',18,y=1.65,color=BASE,size=65)
  self.to(19);m=eq(r'\log_9 a=\frac{\log_3 a}{\log_3 9}',y=-.25,size=64);self.show(m)
  self.to(21);self.show(eq(r'\log_3 9=2',y=-1.85,size=40,color=EXP))
 def s04(self):
  m=eq(r'\log_9 a',size=83,color=BASE);self.add(m)
  m=self.change(m,r'\log_9 a=\frac{\log_3 a}{\log_3 9}',24,color=BASE)
  m=self.change(m,r'\log_9 a=\frac{\log_3 a}{2}',26,color=BASE)
  m=self.change(m,r'\log_9 a=\frac12\log_3 a',28,color=BASE)
  self.play(Circumscribe(m,color=BASE),run_time=.7)
 def s05(self):
  m=eq(r'\log_9 a=\frac12\log_3 a',y=1.3,size=59,color=BASE);self.add(m)
  b=eq(r'\log_9 b=\frac{\log_3 b}{2}',y=-.6,size=59,color=BASE)
  self.play(TransformFromCopy(m,b),run_time=1);self.to(32)
  self.change(b,r'\log_9 b=\frac12\log_3 b',y=-.6,color=BASE,size=59)
 def s06(self):
  m=eq(r'\log_9 z=\frac12\log_3 z\quad(z>0)',y=1.4,size=58,color=BASE);self.add(m);self.to(38)
  self.show(eq(r'\frac12\log_3 a+\log_3 b=2',y=-.05,size=48),eq(r'\log_3 a=8\left(\frac12\log_3 b\right)',y=-1.5,size=48))
 def s07(self):
  a=eq(r'\log_3 a',-3.4,.6,75,REL,width=6);b=eq(r'\log_3 b',3.4,.6,75,REL,width=6);self.add(a,b)
  self.to(43);self.play(TransformMatchingTex(a,eq(r'x=\log_3 a',-3.4,.6,63,REL,width=6)),run_time=1)
  self.to(45);self.play(TransformMatchingTex(b,eq(r'y=\log_3 b',3.4,.6,63,REL,width=6)),run_time=1);self.note('긴 로그식을 간단한 문자로 바꾼다')
 def s08(self):
  m=eq(r'\frac12\log_3 a+\log_3 b=2',size=66);self.add(m);self.change(m,r'\frac{x}{2}+y=2',49,size=80)
 def s09(self):
  self.add(eq(r'\frac{x}{2}+y=2',y=1.85,size=43));m=eq(r'\log_3 a=8\log_9 b',size=70);self.add(m)
  m=self.change(m,r'x=8\left(\frac y2\right)',53,size=76);self.change(m,r'x=4y',56,size=88)
 def s10(self):
  self.pair();m=eq(r'\frac{x}{2}+y=2',y=-.25,size=73);self.add(m);self.to(60)
  # Explicitly move the replacement term from the second condition into the work area.
  token=eq('4y',3.5,.9,46,color=EXP);self.add(token);self.play(token.animate.move_to([-1.25,-.05,0]),run_time=.8);self.remove(token)
  m=self.change(m,r'\frac{4y}{2}+y=2',size=73);self.change(m,r'2y+y=2',63,size=78)
 def s11(self):
  m=eq('2y+y=2',size=80);self.add(m);m=self.change(m,'3y=2',65.2,size=84);self.change(m,r'y=\frac23',66.5,color=RESULT,size=88)
 def s12(self):
  m=eq('x=4y',size=80,color=REL);self.add(m);m=self.change(m,r'x=4\left(\frac23\right)',69,size=80);m=self.change(m,r'x=\frac83',71,color=RESULT,size=88)
  self.to(72);self.play(FadeOut(m),run_time=.3);self.values()
 def s13(self):
  self.values();self.to(78);self.show(eq(r'\frac ab=?',y=-.1,size=99,color=EXP));self.note('구한 것은 로그값, 구하려는 것은 a/b')
 def s14(self):
  m=eq(r'\log_3\frac ab',size=86,color=REL);self.add(m);self.change(m,r'\log_3\frac ab=\log_3 a-\log_3 b',83,size=66);self.note('로그 안의 나눗셈 → 로그값의 뺄셈',EXP)
 def s15(self):
  m=eq(r'\log_3\frac ab=\log_3 a-\log_3 b',size=66);self.add(m);m=self.change(m,r'\log_3\frac ab=x-y',87,size=79);self.to(89);self.play(Indicate(m,color=EXP),run_time=1)
 def s16(self):
  self.values();m=eq(r'x-y=\frac83-\frac23',y=-.2,size=74);self.add(m);m=self.change(m,r'x-y=\frac63',93,y=-.2,size=78);self.change(m,'x-y=2',94,y=-.2,color=RESULT,size=83)
 def s17(self):
  m=eq(r'\log_3\frac ab=2',size=91,color=REL);self.add(m);self.to(97);self.play(Indicate(m,color=EXP),run_time=1)
  self.change(m,r'\frac ab=3^2',99,color=RESULT,size=96);self.note('밑 3의 몇 제곱이 a/b인가? → 2제곱')
 def s18(self):
  m=eq(r'\frac ab=3^2',size=96,color=RESULT);self.add(m);self.change(m,r'\frac ab=9',103.3,color=RESULT,size=102);self.to(105);self.show(tx('정답 ③',y=-1.65,size=36,color=RESULT),rt=.5)
 def s19(self):
  self.add(tx('개별 값을 계산',-3.6,1.7,30,MUTED,width=6),eq(r'a=3^x,\quad b=3^y',-3.6,.5,48,MUTED,width=6));self.to(110)
  self.show(tx('로그값의 차이를 이용',3.6,1.7,30,REL,width=6),eq(r'\log_3\frac ab=x-y=2',3.6,.5,51,REL,width=6));self.to(114)
  self.show(tx('계산 가능하지만 불필요',-3.6,-1.2,25,MUTED,width=6),eq(r'\frac ab=3^2=9',3.6,-1.2,52,RESULT,width=6))
 def s20(self):
  self.add(tx('x, y를 각각 구하지 않고',y=1.8,size=28,color=EXP));self.to(120)
  m=eq(r'\log_3 a=8\log_9 b',size=74);self.show(m);self.change(m,'x=4y',123,size=92);self.note('구해야 하는 관계는 x − y')
 def s21(self):
  m=eq(r'\log_3\frac ab=x-y',size=77);self.add(m);m=self.change(m,r'\log_3\frac ab=4y-y',126.2,size=77);self.change(m,r'\log_3\frac ab=3y',128,size=83,color=EXP)
 def s22(self):
  self.add(eq('x-y=3y',y=1.85,size=50,color=EXP));m=eq(r'\frac{x}{2}+y=2',size=76);self.add(m)
  m=self.change(m,r'\frac{4y}{2}+y=2',130.2,size=76);m=self.change(m,'3y=2',132,size=84,color=EXP)
  self.change(m,r'\boxed{x-y=3y=2}',134,size=80,color=RESULT)
 def s23(self):
  self.add(eq(r'\log_3\frac ab=x-y=2',y=1.15,size=71,color=REL));self.to(138)
  self.show(eq(r'\frac ab=9',y=-.5,size=95,color=RESULT));self.note('개별 로그값 계산 생략')
 def s24(self):
  self.add(eq(r'\log_9 a\qquad\log_3 a',y=1.45,size=60,color=BASE));self.to(145)
  wrong=eq(r'\log_9 a=2\log_3 a',y=.1,size=60,color=WARN);cross=Cross(wrong,stroke_color=WARN,stroke_width=3)
  self.show(VGroup(wrong,cross));self.to(149)
  self.show(eq(r'\log_9 a=\frac12\log_3 a',y=-1.5,size=63,color=RESULT))
 def s25(self):
  wrong=eq(r'\log_3\frac ab=\frac{\log_3 a}{\log_3 b}',y=1.2,size=61,color=WARN);self.add(wrong,Cross(wrong,stroke_color=WARN,stroke_width=3));self.to(155)
  self.show(eq(r'\log_3\frac ab=\log_3 a-\log_3 b',y=-.7,size=65,color=RESULT));self.note('비율의 로그는 로그값의 차이')
 def s26(self):
  self.show(tx('① 밑 통일',-4.7,1.6,30,BASE,width=4),eq(r'\log_9 a=\frac12\log_3 a',-4.7,.35,40,BASE,width=4.5));self.to(161)
  self.show(tx('② 치환',0,1.6,30,REL,width=4),eq(r'x,\ y',0,.35,60,REL,width=4));self.to(164)
  self.show(tx('③ 관계 계산',4.7,1.6,30,EXP,width=4),eq('x-y=2',4.7,.35,54,EXP,width=4.5));self.note('표현을 단순하게 바꾸고 필요한 관계를 찾는다')
 def s27(self):
  self.add(tx('두 수의 곱',-3.6,1.75,30,BASE,width=6),eq(r'\log_3(ab)=x+y',-3.6,.45,54,BASE,width=6));self.to(169)
  self.show(tx('두 수의 비율',3.6,1.75,30,REL,width=6),eq(r'\log_3\frac ab=x-y',3.6,.45,55,REL,width=6));self.to(172)
  self.note('a, b를 각각 계산하기 전에 목표에 필요한 관계를 확인')
 def s28(self):
  self.add(eq(r'\log_9 a=\frac12\log_3 a',y=1.65,size=52,color=BASE),eq(r'\log_3\frac ab=x-y=2',y=.2,size=60,color=REL),eq(r'\frac ab=9',y=-1.45,size=71,color=RESULT));self.to(176.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(28):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(LogShot,),{'shot':i,'__module__':__name__})
