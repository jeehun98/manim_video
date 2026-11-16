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
config.pixel_width=640 if os.getenv('CSAT03_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT03_PREVIEW')=='1' else 1080
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
class SigmaShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.03',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('수열의 합',x=6.2,y=3.95,size=19,color=BASE,width=2))
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
 def sigma(self,upper=5,size=48,color=INK):
  glyph=eq(r'\sum',y=0,size=size)
  top=eq(str(upper),y=.6,size=size*.46,color=color)
  bottom=eq('k=1',y=-.66,size=size*.43,color=color)
  return VGroup(glyph,top,bottom)
 def condition(self,coef=2,value='19',x=0,y=.5,size=48,width=13):
  sig=self.sigma(size=size)
  terms=VGroup(eq('(',size=size),eq(('2' if coef==2 else '')+'a_k',size=size,color=BASE),eq('+',size=size),eq('b_k',size=size,color=REL),eq(')',size=size)).arrange(RIGHT,buff=.05)
  result=eq('='+value,size=size) if value else VGroup()
  row=VGroup(sig,terms,result).arrange(RIGHT,buff=.18)
  if row.width>width:row.scale_to_fit_width(width)
  row.move_to([x,y,0]);row.sig=sig;row.a=terms[1];row.b=terms[3];return row
 def conditions(self):
  a=self.condition(y=1.25);b=self.condition(coef=1,value='10',y=-.55);self.add(a,b);return a,b
 def asum(self,upper=5,x=0,y=.5,color=BASE,size=58):return eq(r'\sum_{k=1}^{'+str(upper)+r'}a_k',x,y,size,color)
 def s01(self):
  n=tx('03',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  a=self.condition(y=1.4,size=41);self.play(Write(a),run_time=1.5);self.to(4)
  b=self.condition(coef=1,value='10',y=-.05,size=41);self.show(b);self.to(6)
  target=eq(r'\sum_{k=1}^{5}a_k=?',y=-1.55,size=42,color=BASE);self.show(target);self.play(Create(SurroundingRectangle(target,color=EXP,buff=.12)),run_time=.6)
 def s02(self):
  a,b=self.conditions();self.play(a.animate.scale(.8).move_to([-3.7,.65,0]),b.animate.scale(.8).move_to([3.7,.65,0]),run_time=1)
  self.play(Indicate(a.sig,color=EXP),Indicate(b.sig,color=EXP),run_time=1.1);self.note('계산을 시작하기 전에, 두 조건의 구조부터 비교',EXP)
 def s03(self):
  a=self.condition(y=1.25,size=55);self.add(a)
  self.to(17);self.play(Indicate(a.sig[2],color=BASE),run_time=.8);self.play(Indicate(a.sig[1],color=BASE),run_time=.8)
  self.to(20);expanded=eq(r'(2a_1+b_1)+(2a_2+b_2)+\cdots+(2a_5+b_5)',y=-.6,size=39,width=13.7);self.show(expanded);self.note('k = 1부터 5까지, 같은 형태의 항을 더한다')
 def s04(self):
  a,b=self.conditions();self.play(Indicate(b.a,color=BASE),Indicate(b.b,color=REL),run_time=1)
  self.to(27);self.play(Create(SurroundingRectangle(a.sig,color=RESULT,buff=.12)),Create(SurroundingRectangle(b.sig,color=RESULT,buff=.12)),run_time=.6);self.note('합산 범위가 같다: k = 1부터 5',RESULT)
  self.to(29);self.play(Indicate(a.b,color=REL),Indicate(b.b,color=REL),run_time=.8);self.note('bₖ의 계수는 모두 1  ·  aₖ의 계수는 2와 1',EXP)
 def s05(self):
  a,b=self.conditions();minus=eq('-',x=-4.7,y=-.55,size=65,color=EXP);self.show(minus)
  self.play(Create(Line([-4.7,-1.35,0],[4.6,-1.35,0],color=EXP,stroke_width=2)),run_time=.6)
  self.note('첫 번째 식 − 두 번째 식',EXP)
 def s06(self):
  original=eq(r'(2a_k+b_k)-(a_k+b_k)',y=.8,size=61);self.add(original)
  terms=VGroup(eq('2a_k',size=61,color=BASE),eq('-a_k',size=61,color=BASE),eq('+b_k',size=61,color=REL),eq('-b_k',size=61,color=REL)).arrange(RIGHT,buff=.18).move_to([0,.8,0])
  self.play(ReplacementTransform(original,terms),run_time=.6);self.note('마이너스는 두 번째 괄호의 모든 항에 적용',EXP)
  self.to(38);mid=(terms[2].get_center()+terms[3].get_center())/2
  self.play(FadeOut(terms[2],shift=(mid-terms[2].get_center())*.8),FadeOut(terms[3],shift=(mid-terms[3].get_center())*.8),run_time=1)
  self.to(40);self.play(ReplacementTransform(VGroup(terms[0],terms[1]),eq('a_k',y=.8,size=78,color=BASE)),run_time=.6)
 def s07(self):
  m=eq('a_k',y=.6,size=72,color=BASE);self.add(m)
  m=self.morph(m,self.asum(y=.6));self.to(44)
  m=self.morph(m,eq(r'\sum_{k=1}^{5}a_k=19-10',y=.6,size=61,color=BASE));self.to(47)
  m=self.morph(m,eq(r'\sum_{k=1}^{5}a_k=9',y=.6,size=67,color=RESULT));self.play(Circumscribe(m,color=RESULT),run_time=.7)
 def s08(self):
  self.add(eq(r'\sum_{k=1}^{5}a_k=9',y=.6,size=67,color=RESULT));answer=tx('정답 ④',y=-1.2,size=35,color=RESULT);self.show(answer,rt=.4);self.play(Create(SurroundingRectangle(answer,color=RESULT,buff=.2)),run_time=.5)
 def s09(self):
  a=self.asum(x=-3.5,y=.9,size=59);b=eq(r'\sum_{k=1}^{5}b_k',x=3.5,y=.9,size=59,color=REL);self.add(a,b);self.note('각 수열의 합 전체를 하나의 문자로 놓는다')
  self.to(57);aa=eq('A',x=-3.5,y=.9,size=72,color=BASE);bb=eq('B',x=3.5,y=.9,size=72,color=REL)
  self.play(ReplacementTransform(a,aa),ReplacementTransform(b,bb),run_time=1)
  self.to(62);self.play(aa.animate.scale(.6).move_to([-5.5,1.8,0]),bb.animate.scale(.6).move_to([5.5,1.8,0]),run_time=.6)
  self.show(self.algebra(2,'19',y=.8),self.algebra(1,'10',y=-.6));self.note('같은 합에는 같은 문자를 대응시킨다',EXP)
 def algebra(self,c,value,x=0,y=.5):return VGroup(eq('2A' if c==2 else 'A',size=57,color=BASE),eq('+B',size=57,color=REL),eq('='+value,size=57)).arrange(RIGHT,buff=.15).move_to([x,y,0])
 def s10(self):
  a=self.algebra(2,'19',y=1.2);b=self.algebra(1,'10',y=-.25);self.add(a,b)
  self.play(Indicate(a[1],color=REL),Indicate(b[1],color=REL),run_time=.8)
  self.to(69);self.play(FadeOut(a),FadeOut(b),FadeIn(eq('A=19-10=9',y=.55,size=67,color=RESULT)),run_time=.7)
  self.to(71);self.play(*[FadeOut(m) for m in list(self.mobjects) if isinstance(m,MathTex)],run_time=.4)
  self.show(eq(r'\sum_{k=1}^{5}a_k=9',-3.5,.6,55,BASE,width=6),eq('A=9',3.5,.6,65,BASE,width=6));self.note('직접 소거와 문자 치환: 같은 결과',RESULT)
 def s11(self):
  self.note('시그마를 더하거나 빼기 전에 합산 범위부터 확인',WARN);self.to(78)
  left=self.asum(5,x=-3.5,y=.8);right=self.asum(4,x=3.5,y=.8,color=WARN);self.show(left,right)
  self.to(83);top=VGroup(*[eq(f'a_{i}',size=43,color=BASE) for i in range(1,6)]).arrange(RIGHT,buff=.8).move_to([0,1.1,0]);bottom=VGroup(*[eq(f'a_{i}',size=43,color=BASE) for i in range(1,5)]).arrange(RIGHT,buff=.8)
  for i,m in enumerate(bottom):m.move_to(top[i].get_center()+DOWN*1.3)
  signs=VGroup(*[eq('+',x=(top[i].get_x()+top[i+1].get_x())/2,y=1.1,size=29) for i in range(4)],*[eq('+',x=(bottom[i].get_x()+bottom[i+1].get_x())/2,y=-.2,size=29) for i in range(3)])
  self.play(ReplacementTransform(left,top),ReplacementTransform(right,bottom),FadeIn(signs),run_time=.7)
  self.to(85);self.play(*[FadeOut(m) for m in [*list(top)[:4],*bottom,signs]],top[4].animate.move_to([0,.5,0]).set_color(WARN),run_time=1)
  self.to(87);self.play(ReplacementTransform(top[4],eq(r'\sum_{k=1}^{5}a_k-\sum_{k=1}^{4}a_k=a_5',y=.5,size=53,color=WARN)),run_time=.7);self.note('공통 범위 1~4는 사라지고, a₅가 남는다',WARN)
 def s12(self):
  a,b=self.conditions();self.play(Create(SurroundingRectangle(a.sig,color=RESULT,buff=.1)),Create(SurroundingRectangle(b.sig,color=RESULT,buff=.1)),run_time=.6)
  self.to(92);self.play(*[FadeOut(m) for m in list(self.mobjects) if m is a or m is b or isinstance(m,SurroundingRectangle)],run_time=.4)
  m=eq(r'\sum_{k=1}^{5}\bigl[(2a_k+b_k)-(a_k+b_k)\bigr]',y=.5,size=51);self.show(m);self.to(94)
  self.morph(m,self.asum(y=.5,size=69));self.note('같은 시작과 끝 → 시그마 안에서 직접 뺄 수 있다',RESULT)
 def s13(self):
  cards=VGroup(*[VGroup(RoundedRectangle(width=4.1,height=1.2,corner_radius=.12,stroke_color=c,stroke_width=1.4).move_to([x,1.3,0]),tx(s,x,1.3,28,c,width=3.8)) for x,s,c in [(-4.6,'① 범위 확인',RESULT),(0,'② 조건 비교',EXP),(4.6,'③ 소거',BASE)]])
  self.play(LaggedStart(*[FadeIn(m) for m in cards],lag_ratio=.4),run_time=2.5)
  self.to(101);self.show(eq(r'\sum_{k=1}^{5}a_k=19-10=9',y=-.3,size=62,color=RESULT));self.note('정답 ④',RESULT)
  self.to(106);self.note('항을 구하기 전에, 식의 관계를 확인하자',BASE);self.to(108.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(13):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(SigmaShot,),{'shot':i,'__module__':__name__})
