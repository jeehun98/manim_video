"""Thirty-one independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT12_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT12_PREVIEW')=='1' else 1080
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
class GeoShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.12',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('등비수열의 공비',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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



 def change(self,m,s,t=None,y=.5,color=REL,size=72):
  if t is not None:self.to(t)
  n=eq(s,y=y,size=size,color=color);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def sequence(self,count=6,animate=False,y=.65):
  xs=[-6.2+i*2.48 for i in range(6)];terms=[];arrows=[]
  for i in range(count):
   s='a' if i==0 else ('ar' if i==1 else rf'ar^{{{i}}}')
   m=eq(s,xs[i],y,size=57,color=BASE if i==0 else REL,width=1.9)
   label=tx(f'{i+1}번째 항',xs[i],y+1.05,23,MUTED,width=2)
   group=VGroup(m,label);terms.append(group)
   if i==0 or not animate:self.add(group)
   if i:
    arrow=VGroup(Arrow([xs[i-1]+.72,y,0],[xs[i]-.72,y,0],buff=0,tip_length=.12,stroke_width=1.8,color=REL),eq(r'\times r',(xs[i-1]+xs[i])/2,y+.52,size=28,color=REL,width=1.1));arrows.append(arrow)
    if animate:self.play(FadeIn(arrow),FadeIn(group),run_time=.55)
    else:self.add(arrow)
  return terms,arrows
 def conditions(self):
  a=eq(r'a^2(1+r^2)=10',y=1.25,size=65,color=BASE);b=eq(r'a^2r(1+r)=4',y=-.65,size=65,color=REL);self.add(a,b);return a,b
 def known(self):self.add(card('a^2=9',-3.4,1.8,BASE),card(r'r=\frac13',3.4,1.8,REL))
 def quotient(self):
  # Separate MathTex arguments make the repeated factor independently highlightable.
  m=MathTex(r'\frac{',r'a^2',r'(1+r^2)}{',r'a^2',r'r(1+r)}',r'=\frac{10}{4}',font_size=75)
  m.move_to([0,.5,0]);m.set_color_by_tex('a^2',BASE,substring=False);return m
 def s01(self):
  n=tx('12',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=2)
  self.show(eq(r'2a_1(a_1+a_3)=5a_2(a_1+a_2)=20',y=1,size=61),rt=1);self.to(5)
  self.show(eq('r>0',y=-.45,size=61,color=REL));self.to(7);m=eq('a_1a_6=?',y=-1.85,size=55,color=EXP);self.show(m);self.play(Circumscribe(m,color=EXP),run_time=.7)
 def s02(self):
  m=eq(r'a_1,\ a_2,\ a_3,\ \ldots,\ a_6',size=76);self.add(m);self.change(m,r'a,\ r',12,size=101);self.note('여러 항을 첫째항과 공비, 두 변수로 표현')
 def s03(self):
  a=eq('a_1',-4.2,.7,83,BASE,width=3);b=eq('a_2',0,.7,83,REL,width=3);c=eq('a_3',4.2,.7,83,REL,width=3);self.add(a)
  self.play(Create(Arrow([-3.2,.7,0],[-1,.7,0],color=REL)),FadeIn(b),run_time=1.2);self.to(18)
  self.show(eq(r'\times r',-2.1,1.55,48,REL));self.to(20)
  self.play(Create(Arrow([1,.7,0],[3.2,.7,0],color=REL)),FadeIn(c),FadeIn(eq(r'\times r',2.1,1.55,48,REL)),run_time=1)
  self.show(eq('a_{n+1}=ra_n',y=-1.1,size=64,color=REL));self.note('매번 같은 수 r을 곱한다: 공비')
 def s04(self):
  self.add(eq('a_1=a',y=1.75,size=56,color=BASE),tx('r = 공비',y=-1.8,size=29,color=REL));self.to(26)
  self.show(eq('a_2=ar',-3.5,.05,75,REL,width=6));self.to(28)
  self.show(eq('a_3=ar^2',3.5,.05,75,REL,width=6))
 def s05(self):
  self.sequence();self.add(eq(r'a_n=ar^{n-1}',y=-1.15,size=53,color=REL));self.to(32)
  self.show(eq('a_6=ar^5',y=-2.05,size=48,color=EXP))
 def s06(self):
  self.add(eq('a_1=a',-3.7,1.75,54,BASE,width=6),eq('a_6=ar^5',3.7,1.75,54,REL,width=6));m=eq(r'a_1a_6=a\cdot ar^5',size=76);self.show(m)
  self.change(m,'a_1a_6=a^2r^5',38,size=83,color=EXP);self.to(41);self.note('필요한 값은 a²과 r',EXP)
 def s07(self):
  m=eq(r'2a_1(a_1+a_3)=5a_2(a_1+a_2)=20',y=1.6,size=58);self.add(m);self.to(46)
  a=eq(r'2a_1(a_1+a_3)=20',y=.05,size=59,color=BASE);self.play(TransformFromCopy(m,a),run_time=1);self.to(49)
  self.play(TransformFromCopy(m,eq(r'5a_2(a_1+a_2)=20',y=-1.55,size=59,color=REL)),run_time=1)
 def s08(self):
  m=eq(r'2a_1(a_1+a_3)=20',y=1,size=77,color=BASE);self.add(m);self.to(55);self.play(Indicate(m,color=BASE),run_time=1);self.to(58)
  self.show(eq('a_1=a',-3.3,-.9,62,BASE,width=6),eq('a_3=ar^2',3.3,-.9,62,REL,width=6))
 def s09(self):
  m=eq(r'2a_1(a_1+a_3)=20',size=82,color=BASE);self.add(m);self.change(m,r'2a(a+ar^2)=20',62,size=85,color=BASE)
 def s10(self):
  m=eq(r'2a(a+ar^2)=20',size=83,color=BASE);self.add(m);m=self.change(m,r'2a^2(1+r^2)=20',67,size=82,color=BASE);self.change(m,r'a^2(1+r^2)=10',69,size=84,color=BASE)
 def s11(self):
  self.add(eq(r'a^2(1+r^2)=10',y=1.9,size=43,color=BASE));self.to(75)
  self.show(eq(r'5a_2(a_1+a_2)=20',y=.25,size=77,color=REL));self.note('a₁ = a,  a₂ = ar',REL)
 def s12(self):
  m=eq(r'5a_2(a_1+a_2)=20',size=82,color=REL);self.add(m);m=self.change(m,r'5ar(a_1+ar)=20',80,size=82,color=REL);self.change(m,r'5ar(a+ar)=20',83,size=86,color=REL)
 def s13(self):
  m=eq(r'5ar(a+ar)=20',size=84,color=REL);self.add(m);m=self.change(m,r'5a^2r(1+r)=20',87,size=85,color=REL);self.change(m,r'a^2r(1+r)=4',89,size=89,color=REL)
 def s14(self):
  a,b=self.conditions();self.to(93);self.play(Indicate(a,color=BASE),run_time=1);self.to(97);self.play(Indicate(b,color=REL),run_time=1)
 def s15(self):
  a,b=self.conditions();self.to(102);self.play(Indicate(a,color=BASE),Indicate(b,color=BASE),run_time=1);self.to(105)
  m=self.quotient();self.play(ReplacementTransform(VGroup(a,b),m),run_time=1);self.note('a²(1+r²) = 10이므로 a² ≠ 0 · r > 0',BASE)
 def s16(self):
  m=self.quotient();self.add(m);self.play(Indicate(m[1],color=EXP),Indicate(m[3],color=EXP),run_time=1);self.to(111)
  marks=VGroup(*[Line(o.get_corner(DL),o.get_corner(UR),color=WARN,stroke_width=3) for o in [m[1],m[3]]]);self.play(Create(marks),run_time=.7);self.to(113)
  self.remove(marks);self.change(m,r'\frac{1+r^2}{r(1+r)}=\frac{10}{4}',size=83);self.note('a² 소거 → 공비 r 하나만 포함하는 식',EXP)
 def s17(self):
  m=eq(r'\frac{1+r^2}{r(1+r)}=\frac{10}{4}',size=83);self.add(m);self.to(118);self.play(Indicate(m,color=EXP),run_time=1);self.change(m,r'4(1+r^2)=10r(1+r)',120,size=78)
 def s18(self):
  m=eq(r'4(1+r^2)=10r(1+r)',size=78);self.add(m);m=self.change(m,r'4+4r^2=10r+10r^2',122.3,size=76);m=self.change(m,r'6r^2+10r-4=0',124,size=82);self.change(m,r'3r^2+5r-2=0',126,size=87,color=EXP)
 def s19(self):
  m=eq(r'3r^2+5r-2=0',size=88,color=EXP);self.add(m);self.to(130);self.change(m,r'(3r-1)(r+2)=0',size=89,color=REL);self.note('중간항: 6r − r = 5r')
 def s20(self):
  self.add(eq(r'(3r-1)(r+2)=0',y=1.65,size=55,color=REL));self.show(card(r'r=\frac13',-3.4,-.1,REL),card('r=-2',3.4,-.1,WARN))
 def s21(self):
  self.add(eq('r>0',y=1.75,size=70,color=REL));a=card(r'r=\frac13',-3.4,.1,REL);b=card('r=-2',3.4,.1,WARN);self.add(a,b);self.to(138)
  self.play(Create(Cross(b,stroke_color=WARN,stroke_width=3)),b.animate.set_opacity(.4),run_time=1);self.to(141)
  self.play(Indicate(a,color=RESULT),run_time=.7);self.note('양수 공비 r = 1/3',RESULT)
 def s22(self):
  self.add(card(r'r=\frac13',0,1.85,REL));self.to(145);self.show(eq(r'a^2(1+r^2)=10',size=84,color=BASE))
 def s23(self):
  m=eq(r'a^2\left(1+\frac19\right)=10',size=83,color=BASE);self.add(m);m=self.change(m,r'a^2\cdot\frac{10}{9}=10',152,size=85,color=BASE);self.change(m,'a^2=9',154,size=103,color=BASE)
 def s24(self):
  self.known();self.show(eq('a_1a_6=a^2r^5',y=-.6,size=77,color=EXP))
 def s25(self):
  self.known();m=eq('a_1a_6=a^2r^5',y=-.25,size=79,color=EXP);self.add(m);m=self.change(m,'a_1a_6=9r^5',163,y=-.25,size=82);self.change(m,r'a_1a_6=9\left(\frac13\right)^5',165,y=-.25,size=79,color=RESULT)
 def s26(self):
  m=eq(r'9\left(\frac13\right)^5',size=97,color=RESULT);self.add(m);m=self.change(m,r'\frac9{243}',168,size=104,color=RESULT);self.change(m,r'\boxed{\frac1{27}}',170,size=107,color=RESULT);self.to(172);self.show(tx('정답 ①',y=-1.85,size=34,color=RESULT),rt=.5)
 def s27(self):
  self.add(eq('a^2=9',y=1.8,size=70,color=BASE));self.to(176)
  self.show(card('a=3',-3.4,.2,BASE),card('a=-3',3.4,.2,BASE));self.to(180)
  self.show(tx('둘 다 가능',y=-1.05,size=29,color=RESULT));self.to(183)
  self.show(eq('a_1a_6=a^2r^5',y=-2.03,size=48,color=EXP));self.to(186)
  self.play(Indicate(self.mobjects[-1],color=EXP),run_time=.8)
 def s28(self):
  self.sequence(animate=True,y=.7);self.to(191.5);self.note('첫째항 → 여섯째항: ×r 화살표는 총 5개',REL);self.to(194)
  wrong=eq('a_6=ar^6',-3.4,-.9,58,WARN,width=6);self.show(VGroup(wrong,Cross(wrong,stroke_color=WARN,stroke_width=3)),eq('a_6=ar^5',3.4,-.9,58,RESULT,width=6))
 def s29(self):
  m=eq(r'a_1,\ a_2,\ a_3,\ \ldots,\ a_6',size=79);self.add(m);self.change(m,r'a_n=ar^{n-1}',200,size=94,color=REL);self.to(202);self.note('첫째항 a · 공비 r',REL)
 def s30(self):
  self.show(tx('① 항 통일',-4.7,1.6,29,REL,width=4.4),eq(r'a_n=ar^{n-1}',-4.7,.3,48,REL,width=4.4));self.to(207)
  self.show(tx('② 공통인수 소거',0,1.6,29,BASE,width=4.4),eq('a^2',0,.3,67,BASE,width=4.4));self.to(209)
  self.show(tx('③ 필요한 값',4.7,1.6,29,EXP,width=4.4),eq('a^2r^5',4.7,.3,61,EXP,width=4.4));self.note('r = 1/3, a² = 9 → 필요한 곱만 계산',RESULT)
 def s31(self):
  self.add(eq('a_1a_6=a^2r^5',y=1.35,size=69,color=EXP),eq(r'=\boxed{\frac1{27}}',y=-.3,size=91,color=RESULT),tx('정답 ①',y=-1.9,size=32,color=RESULT));self.to(214.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(31):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(GeoShot,),{'shot':i,'__module__':__name__})
