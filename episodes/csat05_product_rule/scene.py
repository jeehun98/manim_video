"""Eighteen independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT05_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT05_PREVIEW')=='1' else 1080
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
class ProductShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.05',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('곱의 미분법',x=6.2,y=3.95,size=19,color=BASE,width=2))
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
 def original(self,y=.5,color=True,size=57):
  p=VGroup(eq('f(x)=',size=size),eq('(3x-1)',size=size,color=BASE if color else INK),eq('(x^2-2x+2)',size=size,color=REL if color else INK)).arrange(RIGHT,buff=.13).move_to([0,y,0]);return p
 def rule(self,arg='x',y=.5,size=44,values=None):
  strs=[f"g'({arg})",f'h({arg})',f'g({arg})',f"h'({arg})"]
  factors=VGroup(*[eq(values[i] if values else s,x,y,size,BASE if i in [0,2] else REL,width=1.8) for i,(x,s) in enumerate(zip([-3.8,-1.8,1.8,3.8],strs))])
  prefix=eq(f"f'({arg})=",x=-6.2,y=y,size=size,width=2)
  symbols=VGroup(eq(r'\times',-2.8,y,size*.65),eq('+',0,y,size*.9,EXP),eq(r'\times',2.8,y,size*.65))
  group=VGroup(prefix,factors,symbols);group.factors=factors;return group
 def valuecards(self,status=(None,None,None,None),y=1.1):
  labels=[r"g'(2)",'h(2)','g(2)',r"h'(2)"];cards=VGroup()
  for i,x in enumerate([-4.8,-1.6,1.6,4.8]):
   c=BASE if i in [0,2] else REL
   box=RoundedRectangle(width=2.8,height=.95,corner_radius=.1,stroke_color=c,stroke_width=1.2).move_to([x,y,0])
   label=eq(labels[i]+'=',x-.35,y,size=28,color=c,width=1.7);val=eq(str(status[i]) if status[i] is not None else '?',x+.8,y,size=34,color=RESULT if status[i] is not None else MUTED,width=.65)
   card=VGroup(box,label,val);card.value=val;cards.add(card)
  return cards
 def board(self,status):
  self.add(self.rule('2',y=2.1,size=27));c=self.valuecards(status);self.add(c);return c
 def fill(self,cards,i,value):
  target=eq(str(value),*cards[i].value.get_center()[:2],size=34,color=RESULT,width=.65)
  self.play(ReplacementTransform(cards[i].value,target),run_time=.5);cards[i].value=target
 def s01(self):
  n=tx('05',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.play(Write(self.original(y=1.2,color=False,size=52)),run_time=1.5);self.to(4);self.show(eq(r"f'(2)=?",y=-.2,size=56));self.to(6)
  opts=VGroup(*[VGroup(tx('①②③④⑤'[i],x-.4,-1.6,22),eq(str(16+2*i),x+.3,-1.6,31)) for i,x in enumerate([-5.4,-2.7,0,2.7,5.4])]);self.play(LaggedStart(*[FadeIn(m) for m in opts],lag_ratio=.1),run_time=1)
 def s02(self):
  p=self.original(y=1.3);self.add(p);self.play(Create(SurroundingRectangle(p[1],color=BASE,buff=.14)),Create(SurroundingRectangle(p[2],color=REL,buff=.14)),run_time=.6)
  self.to(10);self.show(tx('전개 후 미분',-3.8,-.1,27,MUTED,width=6),tx('곱의 미분법',3.8,-.1,27,EXP,width=6),eq(r'3x^3-7x^2+8x-2',-3.8,-1.05,36,MUTED,width=6),eq(r"(gh)'",3.8,-1.05,48,EXP,width=6));self.to(12)
  self.note('먼저 곱의 구조를 유지할 수 있는지 확인',EXP)
 def s03(self):
  pair=lambda x,y:VGroup(eq('g(x)',size=59,color=BASE),eq('h(x)',size=59,color=REL)).arrange(RIGHT,buff=.2).move_to([x,y,0])
  first=pair(-3.3,1.2);self.add(first);self.note('첫 번째 함수만 미분 · 두 번째 함수는 유지',BASE)
  self.play(ReplacementTransform(first[0],eq("g'(x)",*first[0].get_center()[:2],size=59,color=BASE)),run_time=1)
  self.to(17);second=pair(3.3,1.2);self.show(second);self.note('첫 번째 함수는 유지 · 두 번째 함수만 미분',REL)
  self.play(ReplacementTransform(second[1],eq("h'(x)",*second[1].get_center()[:2],size=59,color=REL)),run_time=1)
  self.to(21)
  # Reassemble both terms into one complete rule, retaining their colors.
  keep=[m for m in list(self.mobjects) if m is not self.caption and (isinstance(m,MathTex) or m is first or m is second)]
  self.play(*[FadeOut(m) for m in keep],FadeIn(self.rule(y=.25,size=44)),run_time=.7);self.note('한 번에 하나씩 미분한 두 결과를 더한다',EXP)
 def s04(self):
  p=self.original(y=.9,size=56);self.add(p);self.to(26)
  self.play(Indicate(p[1],color=BASE),run_time=1);self.play(Indicate(p[2],color=REL),run_time=1);self.to(32)
  g=eq('g(x)=3x-1',-3.5,-.7,45,BASE,width=6);h=eq('h(x)=x^2-2x+2',3.5,-.7,43,REL,width=6)
  self.play(TransformFromCopy(p[1],g),TransformFromCopy(p[2],h),run_time=1);self.note('첫 번째 괄호를 g, 두 번째 괄호를 h로')
 def s05(self):
  r=self.rule();self.add(r);self.play(Indicate(VGroup(r.factors[0],r.factors[1]),color=BASE),run_time=1)
  self.to(39);self.play(Indicate(VGroup(r.factors[2],r.factors[3]),color=REL),run_time=1);self.to(42)
  self.play(ReplacementTransform(r,self.rule('2')),run_time=1);self.note('문제에서 필요한 것은 f′(2)',EXP)
 def s06(self):
  r=self.rule('2',y=1.3);self.add(r)
  self.play(LaggedStart(*[Circumscribe(f,color=EXP,buff=.1) for f in r.factors],lag_ratio=.15),run_time=1.5)
  self.to(48);self.show(self.valuecards(y=-.4));self.note('함수값 두 개 + 도함수값 두 개',EXP)
 def s07(self):
  c=self.board((None,None,None,None));m=eq('g(x)=3x-1',y=-.35,size=57,color=BASE);self.add(m)
  self.to(53);m=self.morph(m,eq(r'g(2)=3\times2-1=5',y=-.35,size=56,color=BASE));self.to(55.5);self.fill(c,2,5)
  self.to(57);m=self.morph(m,eq(r"g'(x)=3\quad\Rightarrow\quad g'(2)=3",y=-.35,size=52,color=BASE));self.fill(c,0,3)
 def s08(self):
  c=self.board((3,None,5,None));m=eq('h(x)=x^2-2x+2',y=-.35,size=57,color=REL);self.add(m);self.to(66)
  m=self.morph(m,eq(r'h(2)=2^2-2(2)+2',y=-.35,size=57,color=REL));self.to(67.5)
  m=self.morph(m,eq(r'h(2)=4-4+2=2',y=-.35,size=57,color=REL));self.to(69);self.fill(c,1,2)
 def s09(self):
  c=self.board((3,2,5,None));m=eq('h(x)=x^2-2x+2',y=-.35,size=56,color=REL);self.add(m)
  m=self.morph(m,eq(r"h'(x)=2x-2",y=-.35,size=60,color=REL));self.to(73)
  m=self.morph(m,eq(r"h'(2)=4-2=2",y=-.35,size=60,color=REL));self.fill(c,3,2)
 def s10(self):
  c=self.board((3,2,5,2));r=self.rule('2',y=-.35);self.add(r)
  for i,v in enumerate([3,2,5,2]):
   target=eq(str(v),*r.factors[i].get_center()[:2],size=52,color=BASE if i in [0,2] else REL)
   self.play(FadeOut(r.factors[i]),TransformFromCopy(c[i].value,target),run_time=.6)
  self.to(81)
  self.remove(*r.get_family())
  for m in list(self.mobjects):
   if m is r or (isinstance(m,MathTex) and abs(m.get_y()+.35)<.1):self.remove(m)
  result=eq(r"f'(2)=6+10=16",y=-.35,size=68,color=RESULT);self.show(result);self.note('정답 ①',RESULT)
 def s11(self):
  self.add(eq("f'(2)=16",x=-5.3,y=2,size=27,color=RESULT,width=3))
  m=self.original(y=.65);self.add(m);self.to(88)
  m=self.morph(m,eq(r'3x(x^2-2x+2)-(x^2-2x+2)',y=.65,size=48));self.to(91)
  m=self.morph(m,eq(r'3x^3-6x^2+6x-x^2+2x-2',y=.65,size=53));self.note('−6x² − x² = −7x²   ·   6x + 2x = 8x',EXP)
  self.to(93);self.morph(m,eq(r'f(x)=3x^3-7x^2+8x-2',y=.65,size=58))
 def s12(self):
  m=eq(r'f(x)=3x^3-7x^2+8x-2',y=.7,size=57);self.add(m)
  self.to(96);m=self.morph(m,eq(r"f'(x)=9x^2-14x+8",y=.7,size=61,color=EXP));self.to(100)
  m=self.morph(m,eq(r"f'(2)=36-28+8=16",y=.7,size=61,color=RESULT));self.note('전개 후 미분해도 같은 결과',RESULT)
 def s13(self):
  self.show(eq('16',-3.6,-.9,60,RESULT),eq('16',3.6,-.9,60,RESULT));self.to(106)
  self.show(tx('곱의 미분법',-3.6,1.65,28,BASE,width=6),tx('전개 후 미분',3.6,1.65,28,MUTED,width=6),eq(r"g'h+gh'",-3.6,.7,47,BASE,width=6),eq(r'9x^2-14x+8',3.6,.7,43,MUTED,width=6))
  self.to(111);vals=eq(r'3\times2+5\times2',-3.6,-.1,40,EXP,width=6);self.show(vals);self.play(Create(SurroundingRectangle(vals,color=EXP,buff=.12)),run_time=.6);self.note('이번 문제에서는 전체 전개 없이 필요한 값만 계산 가능',EXP)
 def s14(self):
  self.note('일반적으로 성립하지 않는 잘못된 공식',WARN);self.to(117)
  self.show(eq('f(x)=g(x)h(x)',y=1.2,size=57))
  wrong=eq(r"f'(x)=g'(x)h'(x)",y=-.2,size=59,color=WARN);mark=Cross(stroke_color=WARN,stroke_width=4).scale(.22).move_to([5,-.2,0]);self.show(wrong,mark)
  self.to(120);self.show(tx('두 함수를 동시에 미분한 뒤 곱하지 않는다',y=-1.25,size=27,color=WARN))
 def s15(self):
  a=eq(r"g'h",-3.4,.9,72,BASE);b=eq(r"gh'",3.4,.9,72,REL);self.show(a,b)
  self.show(tx('첫 번째 함수만 미분',-3.4,-.3,25,BASE,width=6),tx('두 번째 함수만 미분',3.4,-.3,25,REL,width=6));self.to(126)
  self.play(a.animate.move_to([-1.3,.9,0]),b.animate.move_to([1.3,.9,0]),FadeIn(eq('+',y=.9,size=65,color=EXP)),run_time=.8)
  self.note("(gh)′ = g′h + gh′",RESULT)
 def s16(self):
  self.show(tx('전개 후 미분',-3.6,1.4,31,MUTED,width=6),tx('곱의 미분법',3.6,1.4,31,BASE,width=6),eq(r'3x^3-7x^2+8x-2',-3.6,.25,40,MUTED,width=6),eq(r"g'h+gh'",3.6,.25,52,BASE,width=6));self.to(131)
  self.show(tx('전개가 간단할 때',-3.6,-1,26,MUTED,width=6),tx('곱의 구조를 유지할 때',3.6,-1,26,BASE,width=6));self.note('어떤 형태를 유지하면 계산하기 편리할까?',EXP)
 def s17(self):
  c=self.valuecards((3,2,5,2),y=1.5);r=self.rule('2',y=.1);self.add(c,r)
  self.play(LaggedStart(*[Indicate(f,color=EXP) for f in r.factors],lag_ratio=.1),run_time=1.2);self.to(138)
  self.play(ReplacementTransform(r,self.rule('2',y=.1,values=['3','2','5','2'])),run_time=.8);self.to(140)
  self.show(eq('=16',y=-1.2,size=65,color=RESULT));self.note('특정 지점에서는 필요한 값만 계산한다',EXP)
 def s18(self):
  self.add(eq(r"f'(2)=3\times2+5\times2=16",y=.55,size=62,color=RESULT));self.add(tx('정답 ①',y=-1.1,size=34,color=RESULT));self.to(144.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(18):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ProductShot,),{'shot':i,'__module__':__name__})
