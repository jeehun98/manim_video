"""Continuous equation → elimination → matrix → column-vector chapter."""
import json, textwrap
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
BLUE='#52A9E8'; GOLD='#E8AF5C'; GREEN='#42D6B1'; PURPLE='#B08AE2'; RED='#F07178'; INK='#ECF1FA'; MUTED='#8F9DAF'
config.background_color='#0C1422'
config.frame_width=14.2222222222;config.frame_height=8
def fit(m,w):
 if m.width>w:m.scale_to_fit_width(w)
 return m
def tx(s,x=0,y=0,size=30,c=INK,w=12):return fit(Text(s,font='Malgun Gothic',font_size=size,color=c),w).move_to([x,y,0])
def eq(s,x=0,y=0,size=44,c=INK,w=12):return fit(MathTex(s,font_size=size,color=c),w).move_to([x,y,0])
def equations(general=False,x=-3.7,y=.8,second='x+y=3'):
 a=eq('ax+by=e' if general else '2x+y=5',x,y+.55,c=BLUE,w=5)
 b=eq('cx+dy=f' if general else second,x,y-.55,c=GOLD,w=5)
 brace=Brace(VGroup(a,b),LEFT,color=MUTED,buff=.25)
 return VGroup(a,b,brace)
def plane(x=3.1,y=.25):
 p=NumberPlane(x_range=[-1,6,1],y_range=[-2,6,1],x_length=5.2,y_length=4.8,background_line_style=dict(stroke_color='#334256',stroke_width=1,stroke_opacity=.55),axis_config=dict(stroke_color=MUTED,stroke_width=2,include_tip=False))
 p.move_to([x,y,0])
 labels=VGroup(tx('x',*p.c2p(6,-.3)[:2],size=20,c=MUTED,w=1),tx('y',*p.c2p(-.3,6)[:2],size=20,c=MUTED,w=1))
 for n in [1,2,3,4,5]:labels.add(eq(str(n),*p.c2p(n,-.3)[:2],size=17,c=MUTED,w=.4))
 p.labels=labels
 return p
def clipped(p,a,b,rhs,c,width=4):
 pts=[]
 for x in [-1,6]:
  y=(rhs-a*x)/b
  if -2-1e-8<=y<=6+1e-8:pts.append(p.c2p(x,y))
 for y in [-2,6]:
  if abs(a)>1e-9:
   x=(rhs-b*y)/a
   if -1-1e-8<=x<=6+1e-8:pts.append(p.c2p(x,y))
 return Line(pts[0],pts[-1],color=c,stroke_width=width)
def graph_state(second=(1,1,3),dots=True):
 p=plane();l1=clipped(p,2,1,5,BLUE);l2=clipped(p,*second,GOLD)
 g=VGroup(p,p.labels,l1,l2)
 if dots:g.add(Dot(p.c2p(2,1),color=GREEN,radius=.085),eq('(2,1)',*p.c2p(2.8,1.45)[:2],size=28,c=GREEN,w=1.5))
 return g
def coefficient_system(x=-3.7,y=.8):
 rows=VGroup()
 for i,letters in enumerate([['a','x','+','b','y','=','e'],['c','x','+','d','y','=','f']]):
  row=VGroup(*[eq(s,size=43,c=(BLUE if i==0 else GOLD) if j in [0,3] else MUTED,w=1) for j,s in enumerate(letters)])
  row.arrange(RIGHT,buff=.1).move_to([x,y-i*1.15,0]);rows.add(row)
 return rows
def matrix(x=0,y=.5):
 m=Matrix([['a','b'],['c','d']],h_buff=1.25,v_buff=.9,element_to_mobject=lambda s:MathTex(s,font_size=47))
 m.move_to([x,y,0]);m.get_entries()[0:2].set_color(BLUE);m.get_entries()[2:4].set_color(GOLD)
 return m

class ChapterScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.add(tx('CHAPTER 01',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25))
  # The term determinant is deliberately absent before absolute second 106.
  self.header=tx('방정식에서 나타나는 특별한 숫자',0,2.94,31)
  self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end]
  self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')()
  self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def set_caption(self,t):
  line=next((l for l in self.lines if l['start']<=t<l['end']),None)
  if line is None or line==self.current:return
  self.current=line
  parts=textwrap.wrap(line['text'],width=55,break_long_words=False,break_on_hyphens=False)
  m=VGroup(*[tx(s,size=25,w=12.3) for s in parts]).arrange(DOWN,buff=.10).move_to([0,-3.3,0]).set_z_index(51)
  self.remove(self.cap);self.cap=m;self.add(m)
  self.audit.append(dict(start=line['start'],end=line['end'],left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1])))
 def to(self,target):
  now=self.start+self.time
  if target<now-1e-5:raise ValueError((self.index,now,target))
  for l in self.schedule:
   if now+1e-5<l['start']<=target:
    self.wait(l['start']-(self.start+self.time));self.set_caption(l['start'])
  dt=target-self.start-self.time
  if dt>1e-6:self.wait(dt)
  self.set_caption(target)
 def act(self,duration,*animations):
  end=self.start+self.time+duration
  boundaries=[l['start'] for l in self.schedule if self.start+self.time+1e-5<l['start']<end-1e-5]
  assert not boundaries,('animation crosses subtitle boundary',boundaries)
  self.play(*animations,run_time=duration);self.set_caption(self.start+self.time)
 def show(self,*m,d=.5):self.act(d,*[FadeIn(x) for x in m])
 def clear(self,d=.4):
  keep=[self.header,self.panel,self.cap]
  obs=[m for m in self.mobjects if m not in keep and m.get_center()[1]<2.6]
  if obs:self.act(d,*[FadeOut(m) for m in obs])
 def note(self,s,c=INK):return tx(s,0,-2.25,27,c,w=12)
 def shot_01(self):
  system=equations(x=0,y=.6)
  question=tx('두 식을 동시에 만족하는 값은?',0,1.9,33)
  self.show(question)
  self.to(2);self.show(system[0],d=.6);self.to(5);self.show(system[1],system[2],d=.6);self.to(8)
  self.act(.8,system.animate.shift(LEFT*3.7),FadeOut(question))
  p=plane();self.show(p,p.labels,d=.6)
  self.act(.7,Create(clipped(p,2,1,5,BLUE)));self.act(.7,Create(clipped(p,1,1,3,GOLD)))
  dot=Dot(p.c2p(2,1),radius=.085,color=GREEN);label=eq('(2,1)',*p.c2p(2.8,1.45)[:2],size=28,c=GREEN,w=1.5)
  self.show(dot,label,d=.4);self.to(13)
  self.show(DashedLine(p.c2p(2,1),p.c2p(2,0),color=GREEN),DashedLine(p.c2p(2,1),p.c2p(0,1),color=GREEN),d=.5)
  check1=eq('2(2)+1=5',-3.7,-1.05,34,GREEN,w=4.7);check2=eq('2+1=3',-3.7,-1.65,34,GREEN,w=4.7)
  self.show(check1,check2,d=.6);self.to(18)
  self.act(.4,FadeOut(check1),FadeOut(check2),dot.animate.set_opacity(.3),label.animate.set_opacity(.3))
  self.show(self.note('답을 구하기 전에, 답이 하나인지 알 수 있을까?',PURPLE));self.to(23)
 def shot_02(self):
  s=equations(x=0,y=.5);self.add(s)
  self.show(tx('숫자에서 일반적인 계수로',0,1.95,30,MUTED));self.to(27)
  target=equations(True,x=0,y=.5)
  self.act(1.2,TransformMatchingTex(s[0],target[0]),TransformMatchingTex(s[1],target[1]))
  self.show(self.note('a, b, c, d : 계수     e, f : 우변',MUTED));self.to(33)
 def shot_03(self):
  s=equations(True,x=-3.65,y=1);self.add(s)
  lab=tx('두 식의 y항을 같게 만든다',0,2.03,29,PURPLE);self.add(lab)
  mult=VGroup(eq(r'\times d',-.6,1.55,32,PURPLE),eq(r'\times b',-.6,.45,32,PURPLE))
  self.show(mult,d=.5)
  top=MathTex('ad','x','+','bd','y','=','de',font_size=43).move_to([3.25,1.55,0]);bottom=MathTex('bc','x','+','bd','y','=','bf',font_size=43).move_to([3.25,.45,0])
  top[3:5].set_color(PURPLE);bottom[3:5].set_color(PURPLE)
  self.act(1,TransformFromCopy(s[0],top));self.act(1,TransformFromCopy(s[1],bottom))
  self.show(Line([.7,-.25,0],[5.9,-.25,0],color=MUTED),eq('-',.5,.45,38),d=.4);self.to(39)
  self.act(.6,Create(SurroundingRectangle(top[3:5],color=PURPLE)),Create(SurroundingRectangle(bottom[3:5],color=PURPLE)))
  cancel=eq('bdy-bdy=0',3.2,-.8,35,PURPLE);self.show(cancel,d=.5)
  result=eq('adx-bcx=de-bf',0,-1.65,47);self.show(result,d=.5)
  self.to(42)
  fact=MathTex('(', 'ad-bc', ')x=de-bf',font_size=52).move_to([0,-1.65,0]);fact[1].set_color(PURPLE)
  self.act(.8,TransformMatchingTex(result,fact))
  self.show(SurroundingRectangle(fact[1],color=PURPLE,buff=.13),d=.4);self.to(45)
 def shot_04(self):
  s=coefficient_system();self.add(s)
  value=eq('ad-bc',3,.25,72,PURPLE,w=4)
  box=SurroundingRectangle(value,color=PURPLE,buff=.3,corner_radius=.15)
  self.show(value,box)
  curves=VGroup()
  for row,col,target in [(0,0,value.get_left()+UP*.18),(0,3,value.get_left()+DOWN*.18),(1,0,value.get_right()+DOWN*.18),(1,3,value.get_right()+UP*.18)]:
   curves.add(CurvedArrow(s[row][col].get_right(),target,angle=.3 if row==0 else -.3,color=BLUE if row==0 else GOLD,stroke_width=2,tip_length=.12))
  self.act(1,Create(curves));self.show(self.note('미지수와 우변이 아니라, 네 계수 사이의 관계',PURPLE));self.to(51)
  self.clear();v=eq('ad-bc',0,1.8,57,PURPLE);self.show(v,d=.3)
  self.show(eq(r'ad-bc\ne0',-3.3,.25,48,GREEN),eq('ad-bc=0',3.3,.25,48,RED),tx('유일하게 결정 가능',-3.3,-.85,29,GREEN,w=5),tx('어떤 일이 생길까?',3.3,-.85,29,RED,w=5),d=.6);self.to(55)
 def shot_05(self):
  cond=eq(r'ad-bc\ne0',0,2,44,GREEN);self.add(cond)
  old=eq('(ad-bc)x=de-bf',0,.55,56);self.add(old)
  self.show(eq(r'\div(ad-bc)',0,-.55,35,PURPLE),d=.5)
  self.to(58)
  new=MathTex('x=',r'\frac{de-bf}{ad-bc}',font_size=57).move_to([-2.5,.2,0]);new.set_color_by_tex('frac',PURPLE)
  self.act(.8,TransformMatchingTex(old,new));self.to(62)
  y=eq(r'y=\frac{af-ce}{ad-bc}',2.7,.2,57,PURPLE,w=5);self.show(y,d=.5)
  self.show(self.note('두 미지수 모두 같은 0이 아닌 값으로 나눈다',GREEN),d=.4);self.to(64)
  self.clear(d=.25);self.show(eq('ad-bc=0',0,.9,67,RED),tx('이 값으로 나눌 수 없다',0,-.4,32,RED),d=.4);self.to(66)
 def shot_06(self):
  p=plane();first=clipped(p,2,1,5,BLUE);t=ValueTracker(0)
  second=always_redraw(lambda:clipped(p,1+3*t.get_value(),1+t.get_value(),3,GOLD))
  s=equations(x=-3.7,y=1.25);self.add(p,p.labels,first,second,s)
  self.show(tx('계수만 변경 · 우변은 3',-3.7,-.45,27,GOLD,w=5),d=.4)
  # Coordinate entries follow the very same tracker as the moving line.
  form=VGroup(DecimalNumber(1,num_decimal_places=2,color=GOLD),eq('x+',size=34),DecimalNumber(1,num_decimal_places=2,color=GOLD),eq('y=3',size=34)).arrange(RIGHT,buff=.07).move_to([-3.7,-1.2,0]).scale(.8)
  form[0].add_updater(lambda m:m.set_value(1+3*t.get_value()));form[2].add_updater(lambda m:m.set_value(1+t.get_value()))
  dval=DecimalNumber(1,num_decimal_places=2,color=PURPLE,font_size=39).move_to([-2.1,-2.15,0]);dval.add_updater(lambda m:m.set_value(1-t.get_value()))
  self.show(form,eq('ad-bc=',-4,-2.15,38,PURPLE,w=3),dval,d=.4)
  def moving_point():
   z=t.get_value()
   if z>.99999:return VGroup()
   x=(2+5*z)/(1-z);y=5-2*x
   return Dot(p.c2p(x,y),radius=.08,color=GREEN) if -1<=x<=6 and -2<=y<=6 else VGroup()
  dot=always_redraw(moving_point);self.add(dot)
  # Complete the continuous coefficient change within its spoken sentence.
  self.act(3.8,t.animate.set_value(1));self.to(71)
  self.act(.4,Transform(s[1],eq('4x+2y=3',-3.7,.7,44,GOLD,w=5)))
  self.show(eq(r'2\times2-1\times4=0',-3.7,-.05,32,RED,w=5),d=.5);self.to(76)
  self.act(.3,FadeOut(form))
  self.show(tx('평행한 두 직선 · 교점 없음',-3.7,-1.25,27,RED,w=5),d=.5);self.to(80)
 def shot_07(self):
  p=plane();rhs=ValueTracker(3);s=equations(x=-3.7,y=1.25,second='4x+2y=3')
  first=clipped(p,2,1,5,BLUE,6);second=always_redraw(lambda:clipped(p,4,2,rhs.get_value(),GOLD,3))
  self.add(p,p.labels,first,second,s,eq('ad-bc=0',-3.7,-.4,44,PURPLE,w=5))
  counter=DecimalNumber(3,num_decimal_places=1,color=GOLD,font_size=40).move_to([-2.15,-1.3,0]);counter.add_updater(lambda m:m.set_value(rhs.get_value()))
  self.add(eq('4x+2y=',-4.1,-1.3,36,GOLD,w=3.6),counter)
  self.show(tx('우변만 변경 · 계수는 그대로',-3.7,2.25,24,GOLD,w=5),d=.4)
  self.act(4.6,rhs.animate.set_value(10));self.to(86)
  self.act(.4,Transform(s[1],eq('4x+2y=10',-3.7,.7,44,GOLD,w=5)))
  points=VGroup(*[Dot(p.c2p(x,5-2*x),radius=.065,color=GREEN) for x in np.linspace(0,3,13)])
  self.act(.7,LaggedStart(*[FadeIn(d) for d in points],lag_ratio=.06))
  self.show(self.note('겹친 직선 위의 모든 점이 해',GREEN),d=.4);self.to(90)
 def shot_08(self):
  for x,rhs,title in [(-3.2,3,'해 없음'),(3.2,10,'무한히 많은 해')]:
   self.add(eq('2x+y=5',x,1.5,42,BLUE,w=5),eq(f'4x+2y={rhs}',x,.55,42,GOLD,w=5),tx(title,x,-.45,33,RED if rhs==3 else GREEN,w=5))
  self.show(eq('ad-bc=0',0,-1.3,49,PURPLE),d=.5)
  self.show(self.note('두 경우 모두, 유일한 해는 존재하지 않는다',RED),d=.5);self.to(97)
 def shot_09(self):
  s=coefficient_system(x=-3.3,y=1);self.add(s)
  value=eq('ad-bc',3.2,.4,66,PURPLE,w=4);self.add(value)
  self.show(self.note('방정식의 계수만으로 결정되는 특별한 값',PURPLE));self.to(103)
  m=matrix(3.2,.4);entries=m.get_entries()
  self.act(.35,FadeOut(value))
  self.show(m.get_brackets(),d=.25)
  self.act(1.2,*[TransformFromCopy(s[i][j],entries[k]) for k,(i,j) in enumerate([(0,0),(0,3),(1,0),(1,3)])])
  self.show(tx('행과 열의 관계를 유지해 배열',3.2,-1.35,24,MUTED,w=5),d=.4);self.to(106)
 def shot_10(self):
  m=matrix(-3.4,.45);self.add(m,eq('A=',-5.3,.45,44,w=1.4))
  det=eq(r'\det(A)=\begin{vmatrix}a&b\\c&d\end{vmatrix}',2.25,.45,50,w=6)
  self.show(det,d=.8)
  self.show(tx('행렬식  ·  Determinant',0,2.05,36,PURPLE),d=.5)
  self.show(eq(r'\det(A)=ad-bc',0,-1.6,56,PURPLE,w=10),d=.7);self.to(112)
 def shot_11(self):
  g=graph_state();self.add(g)
  self.add(eq(r'\det(A)\ne0',-3.7,1.25,51,GREEN,w=5),eq(r'\Updownarrow',-3.7,.25,42,GREEN,w=1),tx('유일한 해',-3.7,-.75,38,GREEN,w=5))
  self.show(self.note('해의 유일성을 결정하는 계수들의 관계',PURPLE),d=.5);self.to(120)
 def shot_12(self):
  m=matrix(-3.6,.5);self.add(m,eq('A=',-5.3,.5,41,w=1))
  cols=m.get_columns();c1=SurroundingRectangle(cols[0],color=BLUE,buff=.16,corner_radius=.1);c2=SurroundingRectangle(cols[1],color=GOLD,buff=.16,corner_radius=.1)
  self.show(c1,c2,d=.4)
  p=NumberPlane(x_range=[-1,4,1],y_range=[-1,4,1],x_length=4.8,y_length=4,background_line_style=dict(stroke_color='#334256',stroke_opacity=.5),axis_config=dict(stroke_color=MUTED,stroke_width=1.5)).move_to([3,.3,0])
  self.show(p,d=.4)
  origin=p.c2p(0,0);u=p.c2p(2.4,.9);v=p.c2p(.8,2.4)
  a=Arrow(origin,u,buff=0,color=BLUE,stroke_width=5);b=Arrow(origin,v,buff=0,color=GOLD,stroke_width=5)
  self.act(.8,TransformFromCopy(cols[0],a),TransformFromCopy(cols[1],b))
  self.show(eq('(a,c)',*(u+DOWN*.3)[:2],size=29,c=BLUE,w=1.8),eq('(b,d)',*(v+UP*.3)[:2],size=29,c=GOLD,w=1.8),d=.4)
  outline=VGroup(DashedLine(u,u+v-origin,color=PURPLE),DashedLine(v,u+v-origin,color=PURPLE),Polygon(origin,u,u+v-origin,v,stroke_width=0,fill_color=PURPLE,fill_opacity=.1))
  self.act(.6,Create(outline));self.show(self.note('이 숫자는 왜 공간의 넓이까지 나타낼까?',PURPLE),d=.5)
  self.add(tx('열벡터 배치의 개념도',3,2.5,18,MUTED,w=4))
  # Keep the final matrix and parallelogram visible for the next chapter.
  self.to(126)
