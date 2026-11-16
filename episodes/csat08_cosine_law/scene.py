"""Twenty independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT08_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT08_PREVIEW')=='1' else 1080
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
  self.add(tx('수능 수학  /  EP.08',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('코사인법칙',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
  new=tx('\n'.join(textwrap.wrap(s,width=29,break_long_words=False)),x=-3.8,y=-2.15,size=23,color=color,width=6) if getattr(self,'triangle_active',False) else tx(s,y=-1.95,size=26,color=color)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def triangle(self,ac='x',angle=True,reveal=True):
  self.triangle_active=True
  A=np.array([-5.3,-.65,0]);B=A+.65*np.array([-1,np.sqrt(15),0]);C=A+.65*np.array([6,0,0]);self.A,self.B,self.C=A,B,C
  self.AB=Line(A,B,color=BASE,stroke_width=3);self.BC=Line(B,C,color=REL,stroke_width=3);self.AC=Line(A,C,color=EXP,stroke_width=3)
  self.arc=Arc(radius=.45,start_angle=0,angle=np.arccos(-.25),arc_center=A,color=WARN,stroke_width=2.5)
  vertices=VGroup(eq('A',*(A+LEFT*.15+DOWN*.28)[:2],size=28),eq('B',*(B+UP*.28)[:2],size=28),eq('C',*(C+RIGHT*.25+DOWN*.12)[:2],size=28),*[Dot(v,radius=.035,color=INK) for v in [A,B,C]])
  ab=eq('4',*((A+B)/2+LEFT*.35)[:2],size=40,color=BASE)
  bc=eq('8',*((B+C)/2+np.array([.15,.3,0]))[:2],size=40,color=REL)
  acl=eq(ac,*((A+C)/2+DOWN*.35)[:2],size=40,color=RESULT if ac=='6' else EXP)
  self.lengths=VGroup(ab,bc,acl);g=VGroup(self.AB,self.BC,self.AC,vertices)
  if angle:g.add(self.arc)
  if reveal:g.add(self.lengths)
  self.add(g);return g
 def right(self,s,y=.8,color=INK,size=51):return eq(s,x=3.4,y=y,size=size,color=color,width=6.8)
 def conditions(self):self.add(eq(r'\cos A=-\frac14',x=-3.8,y=-1.5,size=36,color=WARN,width=6))
 def opposite(self):
  mid=(self.B+self.C)/2
  self.play(Indicate(self.arc,color=WARN),run_time=.6)
  self.play(Create(DashedLine(self.A+RIGHT*.45+UP*.3,mid,color=REL,dash_length=.07,stroke_width=1.4)),run_time=.6)
  self.play(Indicate(self.BC,color=REL),run_time=.6)
 def law(self,actual=False,y=.65):
  pieces=[('8^2' if actual else 'a^2',REL),('=',INK),('4^2' if actual else 'b^2',BASE),('+',INK),('x^2' if actual else 'c^2',EXP),('-',WARN),(r'2(4)(x)\cos A' if actual else r'2bc\cos A',WARN)]
  g=VGroup(*[eq(s,size=42,color=c) for s,c in pieces]).arrange(RIGHT,buff=.1)
  if g.width>6.8:g.scale_to_fit_width(6.8)
  return g.move_to([3.4,y,0])
 def s01(self):
  n=tx('08',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.triangle(ac='?',angle=False,reveal=False);self.play(Create(self.AB),Create(self.BC),Create(self.AC),run_time=1.5);self.to(4)
  self.show(self.lengths[0],self.lengths[1]);self.to(6)
  self.show(self.right(r'\cos A=-\frac14',y=1.1,color=WARN),self.right('AC=?',y=-.45,color=EXP),self.lengths[2],rt=.6)
 def s02(self):
  self.triangle(ac='?',angle=False);self.conditions();self.play(Indicate(self.AB,color=BASE),Indicate(self.BC,color=REL),run_time=1)
  self.to(11);self.play(Create(self.arc),run_time=.6);self.show(tx('코사인법칙',3.4,.5,39,EXP,width=6.8));self.note('각과 변의 위치 관계를 먼저 확인')
 def s03(self):
  self.triangle(ac='?');self.conditions();self.show(self.right('AB=4',y=1.5,color=BASE,size=43),self.right('BC=8',y=.4,color=REL,size=43));self.to(20)
  new=eq('x',*self.lengths[2].get_center()[:2],size=40,color=EXP);self.play(ReplacementTransform(self.lengths[2],new),run_time=.7);self.show(self.right('AC=x',y=-.8,color=EXP,size=51))
 def s04(self):
  self.triangle();self.conditions();self.opposite();self.to(27)
  self.show(self.right(r'\angle A\longleftrightarrow BC',y=1.2,color=REL,size=43),tx('맞은편 변 = 8',3.4,-.2,33,REL,width=6.8))
 def s05(self):
  self.triangle();self.conditions();law=self.law();self.show(law)
  self.play(Indicate(law[0],color=REL),Indicate(self.BC,color=REL),run_time=1);self.show(tx('a: 각 A의 맞은편 변',3.4,-.6,26,REL,width=6.8));self.to(33)
  self.play(Indicate(law[2],color=BASE),Indicate(law[4],color=EXP),Indicate(self.AB,color=BASE),Indicate(self.AC,color=EXP),run_time=1)
  self.to(36);self.play(Indicate(law[6],color=WARN),Indicate(self.arc,color=WARN),run_time=1);self.show(tx('나머지 두 변과 그 사이각 A',3.4,-1.4,25,WARN,width=6.8))
 def s06(self):
  self.triangle();self.conditions();m=self.law();self.add(m)
  self.play(Indicate(self.lengths[1],color=REL),Transform(m[0],eq('8^2',*m[0].get_center()[:2],size=42,color=REL)),run_time=.7)
  self.to(44)
  self.play(Indicate(self.lengths[0],color=BASE),Transform(m[2],eq('4^2',*m[2].get_center()[:2],size=42,color=BASE)),run_time=.6)
  self.play(Indicate(self.lengths[2],color=EXP),Transform(m[4],eq('x^2',*m[4].get_center()[:2],size=42,color=EXP)),run_time=.6)
  self.to(46)
  self.morph(m,self.law(actual=True));self.note('좌변에는 각 A의 맞은편 변 BC의 제곱',REL)
 def s07(self):
  self.triangle();self.conditions();m=self.law(actual=True);self.add(m)
  m=self.morph(m,self.right(r'8^2=4^2+x^2-8x\left(-\frac14\right)',y=.65,color=WARN,size=46));self.to(52)
  m=self.morph(m,self.right(r'64=16+x^2-8x\left(-\frac14\right)',y=.65,color=WARN,size=46));self.to(55)
  self.morph(m,self.right('64=16+x^2+2x',y=.65,color=INK,size=55))
 def s08(self):
  self.triangle();self.conditions();m=self.right(r'-8x\left(-\frac14\right)',y=1.15,color=WARN,size=67);self.add(m)
  self.show(self.right(r'(-)\times(-)=(+)',y=-.1,color=WARN,size=48));self.to(60)
  m=self.morph(m,self.right('=+2x',y=1.15,color=RESULT,size=76));self.to(62)
  self.show(self.right('64=16+x^2+2x',y=-1.15,color=INK,size=46));self.note('코사인법칙의 −와 cos A의 −가 만나 +',WARN)
 def s09(self):
  self.triangle();self.conditions();m=self.right('64=16+x^2+2x',y=.65,size=56);self.add(m)
  target=self.right('x^2+2x+16-64=0',y=.65,size=56)
  self.play(TransformMatchingTex(m,target),run_time=.8);self.to(67)
  self.morph(target,self.right('x^2+2x-48=0',y=.65,color=EXP,size=59))
 def s10(self):
  self.triangle();m=self.right('x^2+2x-48=0',y=1.2,color=EXP,size=55);self.add(m)
  self.show(self.right(r'8\times(-6)=-48',y=-.05,size=39),self.right('8+(-6)=2',y=-1,size=39));self.to(72)
  m=self.morph(m,self.right('(x+8)(x-6)=0',y=1.2,color=EXP,size=60));self.note('곱해서 −48, 더해서 2가 되는 두 수')
 def s11(self):
  self.triangle();self.conditions();self.add(self.right('(x+8)(x-6)=0',y=1.65,color=EXP,size=43))
  neg=eq('x=-8',x=1.7,y=.2,size=54,color=WARN);pos=eq('x=6',x=5.3,y=.2,size=54,color=EXP);self.show(neg,pos);self.to(78)
  self.play(Indicate(self.AC,color=EXP),run_time=.7);self.show(tx('x는 변의 길이이므로 x > 0',3.4,-1.2,26,WARN,width=6.8));self.to(80)
  self.play(Create(Cross(neg,stroke_color=WARN,stroke_width=3)),Indicate(pos,color=RESULT),run_time=.8)
 def s12(self):
  self.triangle();new=eq('6',*self.lengths[2].get_center()[:2],size=40,color=RESULT);self.play(ReplacementTransform(self.lengths[2],new),run_time=.6)
  self.add(self.right('AC=6',y=.8,color=RESULT,size=82));self.to(84);self.show(tx('정답 ④',3.4,-.8,34,RESULT,width=6.8),rt=.4)
 def s13(self):
  self.triangle(ac='6');self.add(self.right(r'\cos A=-\frac14<0',y=1.2,color=WARN,size=56));self.to(87)
  self.play(Indicate(self.arc,color=WARN,scale_factor=1.25),run_time=1);self.to(90)
  self.show(self.right(r'90^\circ<A<180^\circ',y=-.2,color=WARN,size=47),tx('각 A는 둔각',3.4,-1.35,32,WARN,width=6.8))
 def s14(self):
  self.triangle(ac='6');self.opposite();self.to(95)
  self.show(self.right('BC=8',y=1.3,color=REL,size=65),self.right(r'8>6,\quad 8>4',y=-.3,color=RESULT,size=51));self.note('둔각 A의 맞은편 변 BC가 가장 길다',REL)
 def s15(self):
  self.triangle(ac='6');self.show(self.right(r'AB=4,\quad AC=6',y=1.5,size=42),self.right('BC=8',y=.45,color=REL,size=49));self.to(102)
  self.show(self.right('8>6>4',y=-.7,color=RESULT,size=67));self.to(105)
  self.note('조건과 일치하는지 검산할 수 있지만, 이 조건만으로 6을 구할 수는 없다',WARN)
 def s16(self):
  self.triangle(ac='6');self.conditions();self.to(110);self.opposite();self.to(113)
  self.show(self.right(r'\angle A\longleftrightarrow BC',y=1.35,color=REL,size=42),self.law(actual=True,y=-.25));self.note('코사인법칙의 좌변에 들어갈 변부터 확인',WARN)
 def s17(self):
  for t,x,label,formula,c in [(115,-4.6,'① 변 대응','BC=8',REL),(118,0,'② 부호 계산','(-)(-)=+',WARN),(120,4.6,'③ 해 선택','x>0',RESULT)]:
   self.to(t);self.show(VGroup(RoundedRectangle(width=4.1,height=2.4,corner_radius=.12,stroke_color=c,stroke_width=1.3).move_to([x,.6,0]),tx(label,x,1.25,27,c,width=3.8),eq(formula,x,.1,45,c,width=3.7)))
 def s18(self):
  for t,x,label,c in [(122,-4.6,'① 변 대응',REL),(125,0,'② 공식 적용',EXP),(128,4.6,'③ 해 선택',RESULT)]:
   self.to(t);self.show(VGroup(RoundedRectangle(width=4.1,height=1.1,corner_radius=.12,stroke_color=c,stroke_width=1.3).move_to([x,1.4,0]),tx(label,x,1.4,27,c,width=3.8)))
   if t==125:self.show(eq(r'8^2=4^2+x^2-2(4)(x)\cos A',y=-.2,size=51))
   if t==128:self.note('AC = 6',RESULT)
 def s19(self):
  self.triangle(ac='6');self.add(self.right('x^2+2x-48=0',y=1.5,color=EXP,size=48));self.show(self.right(r'x=-8\quad\mathrm{or}\quad x=6',y=.2,size=48));self.to(134)
  self.show(self.right('AC=6>0',y=-1.2,color=RESULT,size=60));self.note('6 > 0이며, 4 + 6 > 8도 만족한다',RESULT)
 def s20(self):
  self.add(eq('AC=6',y=.7,size=88,color=RESULT),tx('정답 ④',y=-1.1,size=35,color=RESULT));self.to(137.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(20):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(CosineShot,),{'shot':i,'__module__':__name__})
