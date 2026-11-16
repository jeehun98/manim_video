"""Eleven independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT_PREVIEW')=='1' else 1080
config.background_color='#0B1020'
INK='#F5F5F5';BASE='#38BDF8';EXP='#FACC15';REL='#C084FC';RESULT='#4ADE80';MUTED='#94A3B8'
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
  self.add(tx('수능 수학  /  EP.01',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('지수법칙',x=6.2,y=3.95,size=19,color=BASE,width=2))
  self.add(Line([-7.15,3.55,0],[7.15,3.55,0],color=MUTED,stroke_opacity=.25,stroke_width=1))
  self.add(tx(self.info['title'],y=2.95,size=34))
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
  if frames:self.wait(frames/30)
 def show(self,*ms,rt=.6):self.play(*[FadeIn(m,shift=UP*.08) for m in ms],run_time=rt)
 def morph(self,a,b,rt=.7):self.play(ReplacementTransform(a,b),run_time=rt);return b
 def note(self,s,color=MUTED):
  new=tx(s,y=-1.95,size=26,color=color)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.35)
  else:self.show(new,rt=.35)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def s01(self):
  a=eq(r'\sqrt[3]{9}',-2,.5);b=eq(r'3^{-\frac53}',2,.5);times=eq(r'\times',0,.5)
  self.show(a,b,times);self.show(tx('2027학년도 6월 모의평가 · 공통 1번',y=1.8,size=22,color=MUTED))
  self.to(3);boxes=VGroup(SurroundingRectangle(a,color=MUTED,buff=.22),SurroundingRectangle(b,color=MUTED,buff=.22));self.play(Create(boxes),run_time=.6)
  self.to(7);self.note('첫 관찰  ·  같은 밑의 거듭제곱으로 나타낼 수 있을까?',BASE)
  self.play(Indicate(a,color=BASE),Indicate(b,color=BASE),run_time=1.2)
 def s02(self):
  m=eq(r'\sqrt[3]{9}');self.add(m);self.note('세제곱근 = 1/3제곱')
  m=self.morph(m,eq(r'9^{\frac13}'));self.to(17)
  m=self.morph(m,eq(r'(3^2)^{\frac13}'));self.show(eq(r'(a^m)^n=a^{mn}',y=-.95,size=34,color=MUTED))
  self.to(19.5);m=self.morph(m,eq(r'3^{\frac23}',color=BASE));self.to(22)
  m=self.morph(m,eq(r'{{3}}^{\frac23}\times{{3}}^{-\frac53}'))
  m.set_color_by_tex('3',BASE);self.note('밑이 모두 3으로 같아졌다',BASE)
 def s03(self):
  m=eq(r'3^{\frac23}\times3^{-\frac53}');self.add(m)
  self.show(eq(r'a^m\times a^n=a^{m+n}',y=1.8,size=35,color=EXP))
  self.note('밑은 그대로, 지수는 더한다',EXP);self.to(26)
  m=self.morph(m,eq(r'3^{\frac23+(-\frac53)}',color=EXP));self.to(29)
  m=self.morph(m,eq(r'3^{\frac23-\frac53}=3^{-1}'));self.to(32)
  m=self.morph(m,eq(r'3^{-1}=\frac13',color=RESULT));self.to(35)
  self.note('정답 ②',RESULT);self.play(Circumscribe(m,color=RESULT),run_time=.65)
 def s04(self):
  self.note('곱해지는 수의 개수를 세어보자',BASE);self.to(40)
  m=eq(r'3^2\times3^3',y=1.55);self.show(m);self.to(44)
  left=VGroup(*[eq('3',size=54,color=BASE) for _ in range(2)]).arrange(RIGHT,buff=.7).move_to([-2.5,0,0])
  right=VGroup(*[eq('3',size=54,color=EXP) for _ in range(3)]).arrange(RIGHT,buff=.7).move_to([2,0,0])
  muls=VGroup(*[eq(r'\times',x,0,size=32,color=MUTED) for x in [-2.5,1.0,3.0]])
  # Multiplication signs are positioned between neighboring factors.
  muls=VGroup(*[eq(r'\times',*( (left[i].get_center()+left[i+1].get_center())[:2]/2 ),size=30,color=MUTED) for i in range(1)],*[eq(r'\times',*((right[i].get_center()+right[i+1].get_center())[:2]/2),size=30,color=MUTED) for i in range(2)])
  boxes=VGroup(SurroundingRectangle(left,color=BASE,buff=.2),SurroundingRectangle(right,color=EXP,buff=.2))
  self.show(left,right,muls);self.play(Create(boxes),run_time=.6);self.to(47)
  self.play(FadeOut(boxes),FadeOut(muls),*[o.animate.move_to([x,0,0]) for o,x in zip([*left,*right],[-3,-1.5,0,1.5,3])],run_time=1.3)
  signs=VGroup(*[eq(r'\times',x,0,size=30,color=MUTED) for x in [-2.25,-.75,.75,2.25]])
  self.show(signs,rt=.3);self.to(50)
  self.play(FadeOut(left),FadeOut(right),FadeOut(signs),ReplacementTransform(m,eq(r'3^{2+3}=3^5',y=.6,color=RESULT)),run_time=1)
  self.to(53);self.play(*[FadeOut(o) for o in list(self.mobjects) if isinstance(o,MathTex)],run_time=.4)
  law=eq(r'a^m\times a^n=a^{m+n}',y=.7,size=60,color=BASE);self.show(law);self.note('거듭제곱: 반복 곱셈을 압축한 표현');self.to(57)
  self.show(eq(r'a^1a^{-1}=a^0=1',-3.5,-.6,35,EXP,width=6),eq(r'(a^{1/2})^2=a',3.5,-.6,35,REL,width=6))
  self.note('양의 밑 a > 0  ·  규칙을 유지하도록 음수·분수 지수로 확장',MUTED)
 def s05(self):
  self.note('자체 제작 응용문제',MUTED);self.to(66)
  self.show(tx('조건',x=-5.8,y=1.5,size=24,color=REL),eq(r'3^x+3^{-x}=4',y=1.4,color=REL));self.to(71)
  self.show(tx('구할 값',x=-5.8,y=-.3,size=24,color=BASE),eq(r'3^{3x}+3^{-3x}=?',y=-.3,color=BASE))
 def s06(self):
  m=eq(r'3^x+3^{-x}=4',y=1.2,color=REL);self.add(m)
  probe=eq('x=?',y=-.6,size=48,color=MUTED);self.show(probe);self.note('x를 직접 구하면 계산이 복잡해질 수 있다')
  self.to(79);self.play(FadeOut(probe),run_time=.4);self.to(80)
  self.show(card('3^x=a',-3.4,-.4,BASE),card('3^{-x}=b',3.4,-.4,EXP));self.note('반복되는 지수식에 새로운 이름을 붙인다',BASE)
  self.to(83);self.morph(m,eq(r'a+b=4',y=1.2,color=REL))
 def s07(self):
  # Avoid floating point ceil adding a frame to exact-frame waits in this shot.
  raw_wait=self.wait
  self.wait=lambda duration=1,**kw: raw_wait(max(1/30-1e-8,duration-1e-8),**kw)
  a=card('a+b=4',-3.4,1.7);self.add(a);self.note('합은 이미 알고 있다',REL);self.to(88)
  m=eq(r'ab=3^x\times3^{-x}',y=.25,size=55);self.show(m)
  self.to(89.5);m=self.morph(m,eq(r'ab=3^{x-x}=3^0=1',y=.25,size=55,color=EXP))
  self.to(91);self.show(card('ab=1',3.4,1.7));self.note('합 = 4     ·     곱 = 1',REL)
 def s08(self):
  self.relations();m=eq(r'3^{3x}+3^{-3x}',y=.05,size=55);self.add(m)
  m=self.morph(m,eq(r'(3^x)^3+(3^{-x})^3',y=.05,size=55));self.to(95.5)
  m=self.morph(m,eq(r'a^3+b^3',y=.05,size=60,color=BASE));self.to(98)
  self.play(FadeOut(m),run_time=.3)
  expand=eq(r'(a+b)^3=a^3+3a^2b+3ab^2+b^3',y=.2,size=43);self.show(expand)
  grouped=eq(r'3a^2b+3ab^2=3ab(a+b)',y=-1.05,size=35,color=EXP);self.show(grouped);self.to(101.5)
  self.play(FadeOut(expand),FadeOut(grouped),run_time=.35)
  identity=eq(r'a^3+b^3=(a+b)^3-3ab(a+b)',y=.15,size=49,color=BASE);self.show(identity)
  self.note('세제곱 전개식에서 가운데 두 항을 뺀다',EXP)
 def s09(self):
  a,b=self.relations();m=eq(r'a^3+b^3=(a+b)^3-3ab(a+b)',y=.1,size=49);self.add(m)
  self.note('합과 곱의 값을 대응하는 자리에 대입',REL)
  self.play(Indicate(a,color=REL),Indicate(b,color=REL),run_time=1)
  self.to(110);m=self.morph(m,eq(r'4^3-3\times1\times4',y=.1,size=60));self.to(112)
  m=self.morph(m,eq(r'64-12=52',y=.1,size=68,color=RESULT));self.play(Circumscribe(m,color=RESULT),run_time=.7)
 def s10(self):
  self.add(eq('52',x=5.8,y=1.8,size=45,color=RESULT))
  self.show(tx('x를 직접 구하지 않아도, 필요한 값은 구할 수 있다',y=.65,size=32,color=BASE));self.to(120)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if isinstance(m,MathTex) or (isinstance(m,Text) and abs(m.get_y()-.65)<.1)],run_time=.4)
  self.show(tx('기본 문제',-3.6,1.75,25,BASE),tx('응용문제',3.6,1.75,25,REL))
  self.show(eq(r'\sqrt[3]{9}\cdot3^{-5/3}',-3.6,.65,46,width=6),eq(r'3^x+3^{-x}=4',3.6,.65,46,width=6))
  self.to(123);self.show(eq(r'\downarrow',-3.6,-.05,35,BASE),eq(r'\downarrow',3.6,-.05,35,REL))
  self.show(eq(r'3^{2/3-5/3}',-3.6,-.8,45,BASE,width=6),eq(r'a+b=4,\quad ab=1',3.6,-.8,39,REL,width=6))
  self.note('밑을 통일한다                          표현을 치환한다')
 def s11(self):
  self.show(eq(r'\sqrt[3]{9}\to3^{2/3}',-3.6,1.5,47,BASE,width=6),eq(r'3^x\to a',3.6,1.5,47,REL,width=6))
  self.show(tx('복잡한 표현',x=-3.5,y=.1,size=31,color=MUTED),eq(r'\longrightarrow',y=.1,size=48,color=BASE),tx('드러나는 관계',x=3.5,y=.1,size=31,color=RESULT))
  self.to(134);self.show(tx('어떤 형태로 바꾸면\n필요한 관계가 드러날까?',y=-1.4,size=33,color=INK))
  self.to(142.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(11):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ExponentShot,),{'shot':i,'__module__':__name__})
