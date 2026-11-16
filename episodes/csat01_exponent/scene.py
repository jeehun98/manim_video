"""Nine independent shots, exact supplied sentence times, landscape only."""
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
  self.add(tx('수능 수학  /  EP.01',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('지수법칙',x=6.2,y=3.95,size=19,color=BASE,width=2))
  self.add(Line([-7.15,3.55,0],[7.15,3.55,0],color=MUTED,stroke_opacity=.25,stroke_width=1))
  self.add(tx(self.info['title'],y=2.95,size=32))
  if self.shot>0:
   self.add(eq(r'\sqrt[3]{9}\times3^{-\frac53}',x=5.5,y=2.25,size=27,color=MUTED,width=3.1))
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
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.35)
  else:self.show(new,rt=.35)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def problem(self,y=.5):
  a=eq(r'\sqrt[3]{9}',-2,y);b=eq(r'3^{-\frac53}',2,y);c=eq(r'\times',0,y)
  self.add(a,b,c);return a,b,c
 def options(self,y=-1.35):
  values=[r'\frac19',r'\frac13','1','3','9'];g=VGroup()
  for i,(x,v) in enumerate(zip([-5.4,-2.7,0,2.7,5.4],values)):
   g.add(VGroup(tx('①②③④⑤'[i],x-.55,y,24),eq(v,x+.2,y,36,width=1)))
  return g
 def s01(self):
  n=tx('01',y=.5,size=100,color=BASE);self.show(n)
  self.to(2);self.play(n.animate.scale(.36).move_to([-6.7,2.75,0]),run_time=1)
  a=eq(r'\sqrt[3]{9}\times3^{-\frac53}',y=.6,size=72);self.show(a)
  self.to(5);self.play(LaggedStart(*[FadeIn(o) for o in self.options()],lag_ratio=.15),run_time=1.5)
 def s02(self):
  a,b,c=self.problem();self.note('계산 전에, 밑부터 확인',BASE)
  self.to(11);self.play(Indicate(a,color=BASE),run_time=.8);self.play(Indicate(b,color=BASE),run_time=.8)
  self.to(14);self.show(eq(r'{{a}}^m\times{{a}}^n={{a}}^{m+n}',y=-.9,size=43,color=EXP));self.note('같은 밑일 때 적용하는 규칙',EXP)
 def s03(self):
  a,b,c=self.problem();self.play(b.animate.set_color(BASE),run_time=.6)
  self.note('오른쪽 항의 밑은 3',BASE);self.to(21)
  self.play(Indicate(a,color=BASE),b.animate.set_color(MUTED),run_time=.8)
  self.to(23);self.show(eq(r'\sqrt[3]{9}\longrightarrow3^{\,?}',y=-.85,size=47,color=BASE));self.note('목표: 왼쪽 항도 밑이 3인 거듭제곱으로',BASE)
 def s04(self):
  a,b,c=self.problem();self.note('세제곱근 → 1/3제곱')
  a=self.morph(a,eq(r'9^{\frac13}',-2,.5));self.to(31)
  a=self.morph(a,eq(r'(3^2)^{\frac13}',-2,.5));law=eq(r'(a^m)^n=a^{mn}',y=-.9,size=40,color=EXP);self.show(law)
  self.to(34);a=self.morph(a,eq(r'{{3}}^{\frac23}',-2,.5,color=BASE));self.note('지수끼리 곱한다: 2 × 1/3 = 2/3',EXP)
  self.to(36.5);self.play(FadeOut(law),run_time=.4)
 def s05(self):
  a=eq(r'{{3}}^{\frac23}\times{{3}}^{-\frac53}',y=.55);a.set_color_by_tex('3',BASE);self.add(a)
  self.note('밑이 모두 3으로 같아졌다',BASE);self.to(40)
  a=self.morph(a,eq(r'3^{\frac23+(-\frac53)}',y=.55,color=EXP));self.to(42)
  self.show(eq(r'\frac23-\frac53=-\frac33=-1',y=-.85,size=40,color=EXP))
  self.to(43.5);self.morph(a,eq(r'3^{-1}',y=.55,color=RESULT))
 def s06(self):
  m=eq(r'3^{-1}',y=.75);self.add(m);opts=self.options(-1);self.add(opts)
  self.morph(m,eq(r'3^{-1}=\frac13',y=.75,color=RESULT));self.to(47)
  self.play(Create(SurroundingRectangle(opts[1],color=RESULT,buff=.2)),run_time=.6);self.note('정답 ②',RESULT)
 def s07(self):
  self.note('지수를 더하려면, 먼저 밑이 같아야 한다',WARN);self.to(52)
  wrong=eq(r'2^3\times3^2\ne{{6^5}}',y=.6,size=56,color=WARN)
  # The invalid result is crossed out from its first visible frame.
  target=eq(r'6^5',size=56);target.move_to(wrong.get_right()+LEFT*target.width/2)
  cross=Cross(target,stroke_color=WARN,stroke_width=4)
  self.show(wrong,cross);self.to(57)
  good=eq(r'{{3}}^2\times{{3}}^3={{3}}^5',y=-.85,size=52,color=BASE);self.show(good)
  self.note('처음부터 지수만 계산하지 말고, 밑 통일 가능 여부를 확인',WARN)
 def s08(self):
  bad=eq(r'3^{-1}\ne{{-3}}',x=-3.5,y=.45,size=59,color=WARN,width=6)
  target=eq('-3',size=59);target.move_to(bad.get_right()+LEFT*target.width/2)
  cross=Cross(target,stroke_color=WARN,stroke_width=4);self.show(bad,cross);self.note('음수 지수 ≠ 음수 결과',WARN)
  self.to(66);good=eq(r'3^{-1}=\frac13',x=3.5,y=.45,size=59,color=RESULT,width=6);self.show(good)
  self.show(tx('역수',x=3.5,y=-.9,size=30,color=RESULT));self.note('a⁻¹ = 1/a  (a ≠ 0)',MUTED)
 def s09(self):
  cards=VGroup()
  for x,label,formula,color in [(-4.5,'① 밑 확인',r'\sqrt[3]{9}',MUTED),(0,'② 밑 통일',r'3^{2/3}',BASE),(4.5,'③ 지수 계산',r'3^{-1}',EXP)]:
   cards.add(VGroup(RoundedRectangle(width=3.8,height=2,corner_radius=.12,stroke_color=color,stroke_width=1.2).move_to([x,.9,0]),tx(label,x,1.4,25,color,width=3.5),eq(formula,x,.45,46,color,width=3)))
  self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.3),run_time=2)
  self.to(74);self.show(eq(r'\sqrt[3]{9}\times3^{-5/3}=3^{2/3-5/3}=3^{-1}=\frac13',y=-1.15,size=43,color=RESULT,width=13.8))
  self.to(78);self.note('밑 통일 → 지수법칙',BASE);self.to(81.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(9):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ExponentShot,),{'shot':i,'__module__':__name__})
