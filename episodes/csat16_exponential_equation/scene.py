"""Twenty-three independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT16_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT16_PREVIEW')=='1' else 1080
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
class ExponentShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.16',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('지수방정식과 밑 통일',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def original(self,y=.5,size=95):return eq(r'3^{x-6}=\left(\frac19\right)^x',y=y,size=size)
 def graph(self):
  ax=Axes(x_range=[-2,2,1],y_range=[0,10,2],x_length=6.2,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to([3.4,.05,0]);self.ax=ax
  curve=ax.plot(lambda t:3**t,x_range=[-2,2,.025],color=BASE,stroke_width=2.7,use_smoothing=False);self.add(ax)
  self.add(*[eq(str(t),*(ax.c2p(t,0)+DOWN*.28)[:2],size=22,color=MUTED) for t in [-2,-1,0,1,2]],*[eq(str(v),*(ax.c2p(0,v)+LEFT*.3)[:2],size=22,color=MUTED) for v in [1,3,9]],tx('y = 3ᵗ',3.4,2.2,26,BASE,width=6))
  return ax,curve
 def s01(self):
  n=tx('16',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  m=self.original(size=99);self.show(m,rt=1);self.to(4);self.play(Indicate(m,color=EXP),run_time=.8);self.note('구하려는 값 x = ?',EXP)
 def s02(self):
  self.add(eq('3',-3.4,.65,117,BASE,width=6),eq(r'\frac19',3.4,.65,117,REL,width=6));self.to(9)
  self.play(Create(DoubleArrow([-1.5,.65,0],[1.5,.65,0],buff=0,color=EXP)),run_time=.8);self.note('같은 수의 거듭제곱으로 표현할 수 있을까?')
 def s03(self):
  self.add(self.original(y=1.4,size=91));self.to(14)
  self.show(tx('밑 3',-3.5,-.15,33,BASE,width=6),eq('x-6',-3.5,-1.3,58,EXP,width=6));self.to(18)
  self.show(tx('밑 1/9',3.5,-.15,33,REL,width=6),eq('x',3.5,-1.3,58,EXP,width=6));self.to(20)
  self.play(Indicate(eq('3',-3.5,-.15,55,BASE),color=BASE),Indicate(eq(r'\frac19',3.5,-.15,55,REL),color=REL),run_time=.8)
 def s04(self):
  m=eq('9',y=1.45,size=105,color=REL);self.add(m);self.change(m,'9=3^2',23.3,y=1.45,size=99,color=BASE);self.to(25)
  n=eq(r'\frac19',y=-.55,size=105,color=REL);self.add(n);self.change(n,r'\frac19=\frac1{3^2}',26,y=-.55,size=97,color=BASE)
 def s05(self):
  m=eq('a^{-1}',size=115,color=REL);self.add(m);self.to(32)
  self.change(m,r'a^{-1}=\frac1a',size=113,color=REL);self.note('a ≠ 0 · −1제곱은 역수')
 def s06(self):
  m=eq('3^{-1}',y=1.35,size=100,color=BASE);self.add(m);self.change(m,r'3^{-1}=\frac13',36,y=1.35,size=100,color=BASE);self.to(39)
  n=eq('3^{-2}',y=-.7,size=100,color=REL);self.add(n);self.change(n,r'3^{-2}=\frac1{3^2}=\frac19',40,y=-.7,size=95,color=REL)
 def s07(self):
  wrong=eq('3^{-2}=-9',y=1.15,size=92,color=WARN);self.add(wrong,Cross(wrong,stroke_color=WARN,stroke_width=3));self.to(46)
  self.show(eq(r'3^{-2}=\frac19>0',y=-.7,size=96,color=RESULT));self.note('음수 지수는 결과의 음수 부호가 아니다',WARN)
 def s08(self):
  m=self.original(size=98);self.add(m);self.change(m,r'3^{x-6}=\left(3^{-2}\right)^x',50,size=99,color=REL);self.note('바깥 지수 x는 그대로 · 밑 1/9만 바꾼다')
 def s09(self):
  self.add(eq(r'(a^m)^n=a^{mn}\quad(a>0)',y=1.8,size=53,color=MUTED));m=eq(r'(3^{-2})^x',size=122,color=REL);self.add(m)
  self.to(57);self.show(card('-2',-3.4,-1.35,EXP,width=3),card('x',3.4,-1.35,EXP,width=3));self.to(59)
  self.change(m,r'(3^{-2})^x=3^{(-2)x}',size=99,color=EXP)
 def s10(self):
  m=eq('3^{(-2)x}',size=126,color=EXP);self.add(m);self.change(m,'3^{-2x}',62.4,size=135,color=RESULT)
 def s11(self):
  m=eq('3^{x-6}=3^{-2x}',y=.9,size=120,color=BASE);self.add(m);self.to(72)
  self.play(Indicate(m,color=BASE),run_time=.8);self.to(74)
  self.show(card('3',-3.4,-1.05,BASE,width=3.5),card('3',3.4,-1.05,BASE,width=3.5));self.note('양쪽의 공통 밑은 3',BASE)
 def s12(self):
  ax,curve=self.graph();self.add(self.left('y=3^t',y=1.3,size=89,color=BASE));self.play(Create(curve),run_time=1.5);self.to(79)
  t=ValueTracker(-1);dot=always_redraw(lambda:Dot(ax.c2p(t.get_value(),3**t.get_value()),radius=.075,color=EXP));self.add(dot);self.play(t.animate.set_value(1.8),run_time=2.5,rate_func=linear);self.note('지수가 증가하면 함수값도 항상 증가한다',BASE)
 def s13(self):
  ax,curve=self.graph();self.add(curve,self.left('3^A=3^B',y=1.25,size=86,color=BASE));self.play(Create(Line(ax.c2p(-2,3),ax.c2p(2,3),color=REL,stroke_width=1.6)),FadeIn(Dot(ax.c2p(1,3),radius=.075,color=EXP)),run_time=.8);self.to(85)
  self.show(self.left('A=B',y=-.25,size=103,color=RESULT));self.note('같은 높이의 수평선과 만나는 입력값은 하나')
 def s14(self):
  m=eq('3^{x-6}=3^{-2x}',size=119,color=BASE);self.add(m);self.to(89)
  self.change(m,'x-6=-2x',size=117,color=EXP)
 def s15(self):
  m=eq('x-6=-2x',size=119,color=EXP);self.add(m);m=self.change(m,'x+2x=6',94,size=119);m=self.change(m,'3x=6',96,size=124);self.change(m,r'\boxed{x=2}',98,size=126,color=RESULT)
 def s16(self):
  m=eq('3^{x-6}',y=.75,size=135,color=BASE);self.add(m);self.to(104)
  m=self.change(m,'3^{2-6}=3^{-4}',104,y=.75,size=115,color=BASE);self.to(107)
  self.change(m,r'3^{-4}=\frac1{81}',y=.75,size=117,color=RESULT);self.note('원래 식의 왼쪽에 x = 2 대입')
 def s17(self):
  self.add(eq(r'3^{-4}=\frac1{81}',y=2,size=43,color=BASE));m=eq(r'\left(\frac19\right)^2',y=-.1,size=100,color=REL);self.add(m);self.change(m,r'\left(\frac19\right)^2=\frac1{81}',110,y=-.1,size=90,color=REL);self.to(113)
  self.show(tx('양변 일치 · 정답 2',y=-1.65,size=41,color=RESULT))
 def s18(self):
  a=card('3',-3.4,1.2,BASE);b=card(r'\frac19',3.4,1.2,REL);self.add(a,b);self.to(119)
  m=eq(r'\frac19=\frac1{3^2}',y=-.65,size=99,color=REL);self.show(m);self.change(m,r'\frac19=3^{-2}',123,y=-.65,size=108,color=RESULT)
 def s19(self):
  m=self.original(size=100);self.add(m);m=self.change(m,'3^{x-6}=3^{-2x}',129,size=110,color=BASE);self.change(m,'x-6=-2x',131,size=114,color=EXP)
 def s20(self):
  self.add(eq(r'a^u=a^v\ \Longrightarrow\ u=v',y=1.75,size=64,color=BASE));self.to(138)
  self.show(eq(r'a>0,\quad a\ne1',y=.45,size=74,color=RESULT),eq('1^2=1^5=1',y=-1.05,size=67,color=WARN));self.to(142)
  self.note('a > 1: 증가 · 0 < a < 1: 감소 · 두 경우 모두 일대일')
 def s21(self):
  m=eq('9=3^2',y=1.25,size=110,color=BASE);self.add(m);self.to(149)
  self.show(eq(r'\frac19=3^{-2}',y=-.7,size=111,color=REL))
 def s22(self):
  self.add(eq('a>0',y=1.9,size=45,color=MUTED));m=eq(r'\left(\frac1{a^n}\right)^x',size=116,color=REL);self.add(m);self.change(m,r'\left(\frac1{a^n}\right)^x=a^{-nx}',153,size=102,color=RESULT);self.to(155)
  self.note('분수의 밑 → 음수 지수 → 같은 밑으로 통일',RESULT)
 def s23(self):
  self.add(eq('3^{x-6}=3^{-2x}',y=1.65,size=76,color=BASE),eq('x-6=-2x',y=.15,size=82,color=EXP),eq(r'\boxed{x=2}',y=-1.45,size=96,color=RESULT));self.to(159.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(23):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ExponentShot,),{'shot':i,'__module__':__name__})
