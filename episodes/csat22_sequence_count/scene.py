"""Twenty-six independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT22_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT22_PREVIEW')=='1' else 1080
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
class CountShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.22',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('수열의 생성 규칙과 개수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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











 def change(self,m,s,t=None,y=.4,color=REL,size=66,x=0,width=13):
  if t is not None:self.to(t)
  n=eq(s,x,y,size,color,width);self.play(TransformMatchingTex(m,n),run_time=.6);return n
 def node(self,index,value,x,y,width=1.9,color=BASE):
  return VGroup(RoundedRectangle(width=width,height=1.05,corner_radius=.12,stroke_color=color,stroke_width=1.5,fill_color=color,fill_opacity=.07).move_to([x,y,0]),eq(('n='+str(index)) if isinstance(index,int) else ('a_{'+str(index)+'}'),x,y+.25,24,INK,width-.2),eq(str(value),x,y-.19,39,color,width-.2))
 def tree(self,actual=False,root=1,x=0,spread=4.6,width=1.9):
  val=1 if root==1 else 4
  inds=[2*root,4*root+1,4*root+3] if actual else ['2n','4n+1','4n+3']
  vals=[val+1,val+4,val+4] if actual else ['v+1','v+4','v+4']
  parent=self.node(root if actual else 'n',val if actual else 'v',x,1.35,width)
  children=VGroup(*[self.node(n,v,xx,-.75,width,EXP if i==0 else REL) for i,(n,v,xx) in enumerate(zip(inds,vals,[x-spread,x,x+spread]))])
  edges=VGroup()
  for i,xx in enumerate([x-spread,x,x+spread]):
   color=EXP if i==0 else REL
   a=Arrow([x,.8,0],[xx,-.18,0],buff=.04,color=color,stroke_width=2,tip_length=.11)
   label=eq('+1' if i==0 else '+4',(x+xx)/2+(.35 if i==1 else 0),.62,28,color,width=1)
   edges.add(a,label)
  return parent,children,edges
 def reverse(self,general=False):
  left=eq(r'N(v-1)' if general else 'N(9)',-4.5,1.0,58,EXP,width=4)
  right=eq(r'N(v-4)' if general else 'N(6)',4.5,1.0,58,REL,width=4)
  target=eq(r'N(v)' if general else 'N(10)',0,-.7,70,WARN,width=4)
  arrows=VGroup(Arrow([-3.7,.5,0],[-.8,-.3,0],buff=.05,color=EXP,stroke_width=2.5),Arrow([3.5,.5,0],[.7,-.3,0],buff=.05,color=REL,stroke_width=2.5),Arrow([4.5,.45,0],[1.5,-.65,0],buff=.05,color=REL,stroke_width=2.5))
  self.show(left,right,target,arrows)
  self.add(tx('+1 · 한 갈래',-4.5,1.85,25,EXP,width=3.5),tx('+4 · 두 갈래',4.5,1.85,25,REL,width=3.5))
 def table(self,known=4):
  self.cells={};self.counts={};values=[1,1,1,2,4,6,8,12,20,32]
  self.add(eq('v',-6.85,.8,32,MUTED,width=1),eq('N(v)',-6.85,-.3,29,WARN,width=1.2))
  for v in range(1,11):
   x=-5.4+1.2*(v-1)
   box=RoundedRectangle(width=1.04,height=1.8,corner_radius=.09,stroke_color=MUTED,stroke_width=1,stroke_opacity=.4).move_to([x,.25,0]);self.cells[v]=box
   count=eq(str(values[v-1]) if v<=known else '?',x,-.3,43,WARN if v<=known else MUTED,width=.9);self.counts[v]=count
   self.add(box,eq(str(v),x,.8,37,BASE,width=.9),count)
 def reveal(self,v):
  nums=[1,1,1,2,4,6,8,12,20,32];old=self.counts[v];new=eq(str(nums[v-1]),-5.4+1.2*(v-1),-.3,43,RESULT if v==10 else WARN,width=.9)
  self.play(ReplacementTransform(old,new),self.cells[v].animate.set_stroke(RESULT if v==10 else WARN,opacity=1),run_time=.3);self.counts[v]=new
 def s01(self):
  self.show(eq(r'a_1=1,\quad a_3=4',y=1.7,size=49,color=BASE));self.to(2)
  self.show(eq(r'a_{2n}=a_n+1,\qquad a_{4n+1}=a_{4n+3}=a_n+4',y=.35,size=48));self.to(5)
  self.show(tx('값이 10인 항은 몇 개?',y=-1.3,size=40,color=RESULT))
 def s02(self):
  a,b,e=self.tree();self.show(a);self.to(9);self.show(e,b);self.note('항을 순서대로 나열하기보다, 생성 규칙을 본다')
 def s03(self):
  self.show(eq(r'n\longrightarrow 2n',y=1.3,size=73,color=INK));self.to(17)
  self.show(eq(r'a_{2n}=a_n+1',y=-.1,size=85,color=EXP));self.note('인덱스는 두 배 · 값은 +1')
 def s04(self):
  self.show(eq(r'n\longrightarrow 4n+1,\ 4n+3',y=1.3,size=63));self.show(eq(r'a_{4n+1}=a_{4n+3}=a_n+4',y=-.25,size=65,color=REL));self.note('서로 다른 두 인덱스 · 각각 값은 +4')
 def s05(self):
  a,b,e=self.tree();self.show(a);self.to(31);self.show(e,b);self.note('+1 한 갈래, +4 두 갈래')
 def s06(self):
  a,b,e=self.tree(actual=True);self.show(a);self.to(40);self.show(e,b);self.note('위: 인덱스 n  /  아래: 항의 값 aₙ')
 def s07(self):
  a,b,e=self.tree(True,1,-3.65,2.4,1.5);c,d,f=self.tree(True,3,3.65,2.4,1.5)
  self.show(a,b,e,c,d,f);self.note('시작점은 n=1과 n=3인 두 나무')
 def s08(self):
  self.show(eq(r'2n,\quad 4n+1,\quad 4n+3\qquad(n\ge1)',y=1.7,size=53))
  self.show(tx('짝수',-4.5,.7,29,EXP,width=3),tx('4로 나눈 나머지 1',0,.7,27,REL,width=4),tx('4로 나눈 나머지 3',4.5,.7,27,REL,width=4));self.to(53)
  self.show(eq(r'\frac{k}{2}',-4.5,-.3,56),eq(r'\frac{k-1}{4}',0,-.3,56),eq(r'\frac{k-3}{4}',4.5,-.3,56));self.to(56)
  self.note('1과 3을 제외하면 부모가 하나로 정해지고, 인덱스는 작아진다')
 def s09(self):
  self.show(tx('같은 값을 갖는 항들을 한 묶음으로',y=1.5,size=33,color=MUTED));self.to(64)
  self.show(eq(r'N(v)=\#\{k\in\mathbb N:a_k=v\}',y=-.1,size=75,color=WARN));self.note('N(v)는 항의 값이 아니라, 그 값을 갖는 항의 개수')
 def s10(self):
  self.show(eq(r'a_k=10',y=1.75,size=60,color=RESULT));self.to(70)
  self.show(eq(r'9\xrightarrow{+1}10',x=-3.6,y=.2,size=64,color=EXP,width=6));self.to(74)
  self.show(eq(r'6\xrightarrow{+4}10',x=3.6,y=.2,size=64,color=REL,width=6));self.note('값 9에서 한 갈래, 값 6에서 두 갈래')
 def s11(self):
  self.reverse();self.note('값 6인 항 하나에서 값 10인 항 두 개가 만들어진다')
 def s12(self):
  self.show(eq(r'N(10)=N(9)+2N(6)',y=.5,size=83,color=WARN));self.note('중복 생성이 없으므로 그대로 더할 수 있다')
 def s13(self):
  self.show(eq(r'N(v)=N(v-1)+2N(v-4)',y=.5,size=75,color=WARN));self.show(eq(r'v\ge5',y=-1.0,size=39,color=MUTED));self.note('v=1,2,3,4는 초기값으로 먼저 정한다')
 def s14(self):
  self.show(self.node(1,1,0,1.25,2.3));self.to(101)
  self.show(eq('N(1)=1',y=-.35,size=82,color=WARN));self.note('값은 생성될 때마다 증가하므로 다른 항은 값 1이 될 수 없다')
 def s15(self):
  for x,n,v in [(-4,1,1),(0,2,2),(4,4,3)]:self.add(self.node(n,v,x,1.0,2))
  self.add(Arrow([-2.9,1,0],[-1.1,1,0],color=EXP,buff=.05),Arrow([1.1,1,0],[2.9,1,0],color=EXP,buff=.05))
  self.show(eq('N(2)=1,\quad N(3)=1',y=-.8,size=65,color=WARN));self.note('인덱스 1 → 2 → 4, 값 1 → 2 → 3')
 def s16(self):
  self.show(self.node(3,4,-3,1,2.4),self.node(8,4,3,1,2.4));self.to(112)
  self.show(tx('처음부터 주어진 항',-3,-.15,29,REL,width=5),eq(r'a_1\to a_2\to a_4\to a_8',3,-.15,37,EXP,width=5.5));self.to(114)
  self.show(eq('N(4)=2',y=-1.3,size=67,color=WARN))
 def s17(self):
  self.table(4);self.note('초기값: 1, 1, 1, 2 — a₃=4도 포함한다')
 def s18(self):
  self.table(4);self.show(eq(r'N(v)=N(v-1)+2N(v-4)',y=1.95,size=45,color=WARN));self.note('초기값에서 출발해 차례로 계산한다')
 def s19(self):
  self.table(4);self.add(eq(r'N(v)=N(v-1)+2N(v-4)',y=1.95,size=43,color=MUTED));m=None
  for when,v,formula in [(125,5,r'N(5)=2+2\cdot1=4'),(126.3,6,r'N(6)=4+2\cdot1=6'),(127.6,7,r'N(7)=6+2\cdot1=8')]:
   self.to(when);self.reveal(v)
   new=eq(formula,y=-1.4,size=47,color=WARN)
   if m is None:self.show(new,rt=.3)
   else:self.play(TransformMatchingTex(m,new),run_time=.3)
   m=new
 def s20(self):
  self.table(7);self.add(eq(r'N(v)=N(v-1)+2N(v-4)',y=1.95,size=43,color=MUTED));self.reveal(8)
  m=eq(r'N(8)=8+2\cdot2=12',y=-1.4,size=48,color=WARN);self.show(m,rt=.3);self.to(132)
  self.reveal(9);self.change(m,r'N(9)=12+2\cdot4=20',y=-1.4,size=48,color=WARN)
 def s21(self):
  self.table(9);self.add(eq(r'N(10)=N(9)+2N(6)',y=1.95,size=51,color=WARN));self.to(137)
  self.play(self.cells[6].animate.set_stroke(REL,opacity=1),self.cells[9].animate.set_stroke(EXP,opacity=1),run_time=.4)
  self.show(eq(r'N(10)=20+2\cdot6',y=-1.4,size=64,color=WARN))
 def s22(self):
  self.table(9);self.add(eq(r'N(10)=20+2\cdot6',y=1.95,size=54,color=WARN));self.to(142)
  self.reveal(10);self.show(eq('N(10)=32',y=-1.4,size=75,color=RESULT))
 def s23(self):
  a,b,e=self.tree();self.show(a,b,e);self.note('개별 항을 나열하는 대신, 생성 규칙을 이용한다')
 def s24(self):
  self.show(eq(r'+1:\ \times1\qquad +4:\ \times2',y=1.4,size=67,color=REL));self.show(eq(r'N(v)=N(v-1)+2N(v-4)',y=-.1,size=72,color=WARN));self.note('값의 변화량과 서로 다른 항의 개수를 함께 본다')
 def s25(self):
  self.show(tx('개별 항 → 생성 규칙 → 값별 개수',y=1.1,size=43,color=BASE));self.show(eq(r'N(10)=N(9)+2N(6)=32',y=-.5,size=65,color=RESULT));self.note('복잡한 수열도 생성 규칙에 집중하면 단순해진다')
 def s26(self):
  self.show(eq(r'N(10)=32',y=.7,size=87,color=RESULT));self.note('값의 변화와 생성되는 갈래 수를 세어라')

for i in range(26):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(CountShot,),{'shot':i})
