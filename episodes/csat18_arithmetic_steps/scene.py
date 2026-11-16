"""Twenty-nine independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT18_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT18_PREVIEW')=='1' else 1080
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
class ArithmeticShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.18',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('등차수열과 공차',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def row(self,indices=None,values=None,y=.55):
  ids=indices or list(range(1,7));xs=np.linspace(-6.1,6.1,len(ids));self.term_xs=xs;self.row_y=y;self.term_ids=ids;terms=[]
  for i,(n,x) in enumerate(zip(ids,xs)):
   val=values[i] if values is not None else rf'a_{{{n}}}'
   color=BASE if n==1 else (REL if n==6 else INK)
   m=eq(str(val),x,y,size=67 if values is not None else 61,color=color,width=1.7);self.add(m,eq(rf'a_{{{n}}}',x,y+1.1,size=31,color=MUTED,width=1.8));terms.append(m)
  self.terms=terms;return terms
 def steps(self,label='+d',reverse=False,show=True):
  xs=self.term_xs;y=self.row_y;objects=[]
  for a,b in zip(xs,xs[1:]):
   start=[b-.65,y,0] if reverse else [a+.65,y,0];end=[a+.65,y,0] if reverse else [b-.65,y,0]
   group=VGroup(Arrow(start,end,buff=0,tip_length=.11,stroke_width=1.8,color=EXP),eq(label,(a+b)/2,y+.55,size=28,color=EXP,width=1.2));objects.append(group)
  if show:self.add(*objects)
  return objects
 def graph(self,line=True):
  ax=Axes(x_range=[0,7,1],y_range=[0,18,3],x_length=6.25,y_length=3.6,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  labs=VGroup(*[eq(str(n),*(ax.c2p(n,0)+DOWN*.26)[:2],size=21,color=MUTED) for n in [1,2,3,4,5,6]],*[eq(str(v),*(ax.c2p(0,v)+LEFT*.28)[:2],size=21,color=MUTED) for v in [5,10,15]],tx('항 번호 n',3.4,-2.1,22,MUTED,width=6))
  self.add(ax,labs,tx('점들이 수열 · 직선은 규칙의 보조선',3.4,2.2,21,MUTED,width=6.6))
  dots=VGroup(*[Dot(ax.c2p(n,17-2*n),radius=.07,color=EXP) for n in range(1,7)]);self.add(dots);self.dots=dots
  self.rule=ax.plot(lambda n:17-2*n,x_range=[1,6,.1],color=BASE,stroke_width=1.7,stroke_opacity=.45)
  if line:self.add(self.rule)
  return ax
 def triangle(self,a=2,b=5):
  ax=self.ax;va=17-2*a;vb=17-2*b
  h=Arrow(ax.c2p(a,va),ax.c2p(b,va),buff=0,tip_length=.09,color=BASE,stroke_width=2)
  v=Arrow(ax.c2p(b,va),ax.c2p(b,vb),buff=0,tip_length=.09,color=WARN,stroke_width=2)
  labs=VGroup(eq(rf'\Delta n={b-a}',*(ax.c2p((a+b)/2,va)+UP*.28)[:2],size=28,color=BASE),eq(rf'\Delta a={vb-va}',*(ax.c2p(b,(va+vb)/2)+RIGHT*.68)[:2],size=28,color=WARN))
  return h,v,labs
 def s01(self):
  n=tx('18',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1)
  self.show(eq('a_6=5',y=1.45,size=99,color=REL));self.to(3)
  self.show(eq('a_5=a_2-6',y=-.05,size=91));self.to(5);self.show(eq('a_1=?',y=-1.75,size=79,color=EXP),rt=.5)
 def s02(self):
  self.row();self.to(9);self.steps('+d');self.note('각 항 사이에 같은 변화량이 반복된다',EXP)
 def s03(self):
  self.add(eq('a_n',-4.2,.6,105,color=BASE),eq('a_{n+1}',4.2,.6,105,color=REL));self.to(16)
  self.play(Create(Arrow([-2.4,.6,0],[2.4,.6,0],color=EXP)),FadeIn(eq('+d',y=1.4,size=65,color=EXP)),run_time=1);self.to(21)
  self.show(eq('a_{n+1}=a_n+d',y=-1.15,size=76,color=EXP));self.note('d는 공차')
 def s04(self):
  self.row(indices=[1,2,3,4],values=[1,3,5,7]);self.to(27);self.steps('+2');self.to(30);self.show(eq('d=2',y=-1.55,size=79,color=RESULT),rt=.5)
 def s05(self):
  self.row(indices=[1,2,3,4],values=[7,5,3,1]);self.steps('-2');self.to(34);self.show(eq('d=-2',y=-1.05,size=80,color=RESULT));self.note('일정하게 감소하면 공차는 음수')
 def s06(self):
  self.row(values=['?','?','?','?','?',5]);self.to(38)
  self.show(eq('a_6=5',-3.4,-1.25,65,REL,width=6),eq('a_5=a_2-6',3.4,-1.25,65,width=6));self.to(42)
  self.play(Indicate(self.terms[1],color=EXP),Indicate(self.terms[4],color=EXP),run_time=1)
 def s07(self):
  m=eq('a_5=a_2-6',size=109);self.add(m);self.change(m,'a_5-a_2=-6',48,size=110,color=WARN)
 def s08(self):
  self.row(indices=[2,3,4,5]);arrows=self.steps('+d',show=False);self.to(55)
  for i,t in enumerate([55,57,59]):self.to(t);self.play(FadeIn(arrows[i]),Indicate(self.terms[i+1],color=EXP),run_time=.8)
  self.show(eq('5-2=3',y=-1.5,size=76,color=EXP),rt=.5)
 def s09(self):
  self.row(indices=[2,3,4,5]);self.steps('+d');self.to(64)
  m=eq('a_5-a_2=d+d+d',y=-1.2,size=76,color=EXP);self.show(m);self.change(m,'a_5-a_2=3d',67,y=-1.2,size=86,color=EXP)
 def s10(self):
  m=eq('a_5-a_2=3d=-6',size=95,color=WARN);self.add(m);m=self.change(m,'3d=-6',71,size=112);self.change(m,r'\boxed{d=-2}',73,size=112,color=RESULT)
 def s11(self):
  self.row(values=['?','?','?','?','?',5]);self.steps('-2');self.show(eq('d=-2',y=-1.5,size=83,color=RESULT))
 def s12(self):
  self.row(values=['?','?','?','?','?',5]);self.to(85);arrows=self.steps('-2',show=False)
  for a in arrows:self.play(FadeIn(a),run_time=.4)
  self.show(eq('6-1=5',y=-.95,size=82,color=EXP));self.note('항은 6개, 그 사이의 간격은 5개')
 def s13(self):
  m=eq(r'5\times(-2)=-10',y=1.3,size=102,color=EXP);self.add(m);self.to(92)
  self.show(eq('a_6=a_1-10',y=-.15,size=95));self.to(94);self.show(eq('5=a_1-10',y=-1.65,size=79,color=REL))
 def s14(self):
  m=eq('5=a_1-10',size=109);self.add(m);self.change(m,r'\boxed{a_1=15}',96.4,size=118,color=RESULT)
 def s15(self):
  self.row(values=['?','?','?','?','?','?']);arrows=self.steps('-2',show=False);values=[15,13,11,9,7,5];self.to(101)
  targets=[101,103,105,106,107,108]
  for i,t in enumerate(targets):
   self.to(t);n=eq(str(values[i]),self.term_xs[i],self.row_y,size=67,color=BASE if i==0 else (REL if i==5 else INK),width=1.7)
   self.play(ReplacementTransform(self.terms[i],n),*([FadeIn(arrows[i-1])] if i else []),run_time=.5);self.terms[i]=n
 def s16(self):
  self.row(values=[15,13,11,9,7,5]);self.steps('-2');self.play(Indicate(self.terms[5],color=RESULT),run_time=.8);self.show(tx('a₆ = 5  ✓',y=-1.55,size=39,color=RESULT))
 def s17(self):
  self.row(values=[15,13,11,9,7,5]);self.play(Indicate(self.terms[1],color=EXP),Indicate(self.terms[4],color=EXP),run_time=.8);self.to(117)
  self.show(eq('7=13-6',y=-1.2,size=91,color=RESULT));self.note('두 조건 모두 만족')
 def s18(self):
  self.add(eq(r'a_1=\boxed{15}',y=.7,size=119,color=RESULT),tx('정답 15',y=-1.3,size=38,color=RESULT))
 def s19(self):
  self.graph(line=False);self.add(self.left('a_n',y=1.2,size=99,color=EXP));self.note('항 번호와 값을 좌표 (n, aₙ)으로 표시')
 def s20(self):
  self.add(eq('a_1',-4.8,1.25,72,BASE,width=4),eq('a_2=a_1+d',0,1.25,58,color=EXP,width=4),eq('a_3=a_1+2d',4.8,1.25,58,color=EXP,width=4));self.to(130)
  self.show(eq('a_n=a_1+(n-1)d',y=-.6,size=93,color=REL));self.to(133);self.note('첫째항에 공차를 n−1번 더한다')
 def s21(self):
  self.add(eq(r'a_1\xrightarrow{+d}a_2\xrightarrow{+d}\cdots\xrightarrow{+d}a_n',y=1.1,size=78,color=EXP));self.to(139)
  self.show(eq('n-1',y=-.65,size=122,color=EXP));self.note('항이 n개이면 사이의 간격은 n−1개')
 def s22(self):
  m=eq('a_n=a_1+(n-1)d',y=.9,size=91,color=REL);self.add(m);self.change(m,'a_n=dn+(a_1-d)',143,y=.9,size=91,color=BASE);self.to(144.2);self.note('이번 문제는 d = −2 ≠ 0 · 항 번호 n에 대한 일차식')
 def s23(self):
  ax=self.graph(line=False);self.add(self.left('a_n=17-2n',y=1.2,size=73,color=REL));self.to(149)
  self.play(*[Indicate(dot,color=EXP) for dot in self.dots],run_time=.8);self.to(151)
  self.play(Create(self.rule),run_time=1);self.note('수열은 자연수 n에서의 점들 · 직선은 보조선')
 def s24(self):
  self.graph();h,v,labs=self.triangle(2,3);self.add(self.left(r'\Delta n=1',y=1.3,size=74,color=BASE));self.play(Create(h),run_time=.7);self.to(155)
  self.play(Create(v),FadeIn(labs),run_time=.8);self.show(self.left(r'\Delta a=-2',y=-.2,size=72,color=WARN))
 def s25(self):
  self.graph();h,v,labs=self.triangle(2,3);self.add(h,v,labs,self.left(r'd=\frac{\Delta a}{\Delta n}',y=1.2,size=66,color=EXP),self.left(r'=\frac{-2}{1}=-2',y=-.45,size=74,color=RESULT))
 def s26(self):
  ax=self.graph();self.add(self.left(r'(2,13),\quad(5,7)',y=1.5,size=46,color=EXP));self.to(165)
  h,v,labs=self.triangle();self.play(Create(h),Create(v),FadeIn(labs),run_time=1);self.to(168)
  m=self.left(r'd=\frac{a_5-a_2}{5-2}',y=-.1,size=59,color=REL);self.show(m);self.change(m,r'd=\frac{-6}{3}=-2',171,x=-3.7,y=-.1,width=6.1,size=72,color=RESULT)
 def s27(self):
  self.add(eq(r'a_m\ \longrightarrow\ a_n',y=1.35,size=93,color=REL));self.to(176)
  self.show(eq('a_n-a_m=(n-m)d',y=-.3,size=94,color=EXP));self.note('n > m일 때 이동 횟수는 n−m')
 def s28(self):
  self.row(values=['?','?','?','?','?',5]);m=eq(r'3d=-6\ \Rightarrow\ d=-2',y=-1.3,size=75,color=RESULT);self.add(m);self.to(183)
  arrows=self.steps('+2',reverse=True,show=False);vals=[15,13,11,9,7,5]
  for i in range(4,-1,-1):
   n=eq(str(vals[i]),self.term_xs[i],self.row_y,size=67,color=RESULT if i==0 else INK,width=1.7);self.play(FadeIn(arrows[i]),ReplacementTransform(self.terms[i],n),run_time=.45)
  self.to(186);self.note('여섯째항 5에서 왼쪽으로 +2씩 다섯 번 → 15',RESULT)
 def s29(self):
  self.add(eq('a_n-a_m=(n-m)d',y=1.5,size=79,color=EXP),eq(r'd=-2,\quad a_1=\boxed{15}',y=-.1,size=88,color=RESULT),tx('정답 15',y=-1.7,size=35,color=RESULT));self.to(190.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(29):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(ArithmeticShot,),{'shot':i,'__module__':__name__})
