"""Permutation choices, signs, and oriented area; 163 seconds."""
import json,sys,itertools
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene,label
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE,GREEN,GOLD,PURPLE,RED,INK,MUTED='#42B8E8','#65D6AC','#E8B45D','#A18CF3','#EF7185','#E8EDF5','#8B9CB7'
PERMS=list(itertools.permutations((1,2,3)))
TERMS=['aei','afh','bdi','bfg','cdh','ceg']
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def txt(s,y=0,size=34,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=44,color=INK,x=0,width=7.4):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def cards(p,y=0,x=0,scale=1):
 g=VGroup()
 for n in p:
  c={1:BLUE,2:PURPLE,3:GOLD}[n]
  g.add(VGroup(RoundedRectangle(width=.86,height=.94,corner_radius=.12,color=c,fill_color=c,fill_opacity=.12),eq(str(n),size=43,color=c,width=.65)))
 return g.arrange(RIGHT,buff=.18).scale(scale).move_to([x,y,0])
def mat(n=2,y=1.4):
 letters=[['a','b'],['c','d']] if n==2 else [['a','b','c'],['d','e','f'],['g','h','i']]
 m=Matrix(letters,h_buff=1.35,v_buff=.95,element_to_mobject=lambda s:MathTex(s,font_size=49)).move_to([0,y,0])
 labels=VGroup()
 for j in range(n):labels.add(txt(f'{j+1}열',m.get_top()[1]+.55,23,BLUE,x=m.get_columns()[j].get_center()[0],width=.8))
 for i in range(n):labels.add(txt(f'{i+1}행',m.get_rows()[i].get_center()[1],22,MUTED,x=m.get_left()[0]-.65,width=.8))
 return m,labels
def selected(m,p,color):return VGroup(*[SurroundingRectangle(m.get_entries()[i*len(p)+j-1],color=color,buff=.13,corner_radius=.05) for i,j in enumerate(p)])
def smallperm(p,y,x=0):return cards(p,y,x,scale=.62)

class PermScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel]
  self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*6.1)
  self.header=VGroup(txt('LINEAR ALGEBRA  /  DETERMINANT × PERMUTATION',7.2,16,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.25),txt('순열 → 열 선택 → 곱셈 항과 부호',5.05,27,BLUE))
  self.add(self.header)
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.header]
  obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def swap(self,g,i,j,duration=.8):
  self.play(Swap(g[i],g[j],path_arc=PI/2),run_time=duration)
  items=list(g.submobjects);items[i],items[j]=items[j],items[i];g.submobjects=items
 def choose(self,m,p,term,y,color):
  boxes=selected(m,p,color);self.show(boxes,run_time=.3)
  result=eq(term,y,43,color)
  self.play(TransformFromCopy(VGroup(*[m.get_entries()[i*len(p)+j-1] for i,j in enumerate(p)]),result),run_time=.5)
  return boxes,result

class Shot01(PermScene):
 shot=0
 def s01(self):
  m,labels=mat();self.show(m,eq(r'\det(A)=ad-bc',-1,53),txt('왜 이 조합, 왜 이 부호일까?',-3.2,33,PURPLE));self.to(5)
  self.clear_body()
  origin=np.array([-1.8,-.7,0]);pts=[origin,origin+[2.4,0,0],origin+[3.6,1.7,0],origin+[1.2,1.7,0]]
  p=Polygon(*pts,color=BLUE,fill_color=BLUE,fill_opacity=.18);self.show(p,eq(r'|\det A|=2',2.9,44,BLUE),txt('넓이의 배율',-2.1,31,BLUE));self.to(8)
  self.play(Transform(p,Polygon(*[origin,origin+[-1.7,0,0],origin+[-1.7,1.7,0],origin+[0,1.7,0]],color=PURPLE,fill_color=PURPLE,fill_opacity=.17).shift(RIGHT*1.7)),run_time=.8)
  self.show(eq(r'\det B=-1',-3.5,40,PURPLE),txt('방향 반전',1.9,28,PURPLE));self.to(11)
  self.clear_body();self.show(eq(r'\det(A)=ad-bc',1.5,61),txt('기하학적 성질 ↔ 계산 규칙',-.5,35,BLUE),txt('먼저, 순서를 바꾸어 보자',-2.6,32));self.to(15)

class Shot02(PermScene):
 shot=1
 def s02(self):
  g=cards((1,2,3),1.6);self.show(g,txt('같은 세 원소',-.4,34));self.to(19)
  self.swap(g,1,2);self.swap(g,1,2,.6);self.swap(g,0,1,.6);self.to(21.6)
  self.clear_body()
  for k,p in enumerate(PERMS):
   self.to(22+k*1.2);self.show(cards(p,2.7-(k//2)*1.5,-1.9 if k%2==0 else 1.9,.78),run_time=.4)
  self.to(30);self.show(eq(r'3!=3\times2\times1=6',-2.9,39,GREEN),run_time=.4);self.to(31)
  self.show(txt('순열  Permutation',4,35,BLUE),txt('같은 원소, 다른 순서',-4.1,29));self.to(35)

class Shot03(PermScene):
 shot=2
 def s03(self):
  g=cards((1,2,3),1.7);self.show(g,txt('두 원소의 자리를 맞바꾸기',-.1,32),txt('Swap',3.4,32,BLUE));self.to(41)
  self.swap(g,1,2,1);self.show(txt('교환 1회 · 홀수',-1.9,38,GOLD),eq('-',-3.3,70,GOLD));self.to(47)
  self.clear_body();g=cards((1,2,3),1.7);count=txt('교환 0회',-.3,35,BLUE);self.show(g,count,run_time=.3)
  self.swap(g,0,1,.8);self.play(Transform(count,txt('교환 1회',-.3,35,GOLD)),run_time=.3)
  self.swap(g,1,2,.8);self.play(Transform(count,txt('교환 2회 · 짝수',-.3,35,GREEN)),run_time=.3);self.show(eq('+',-2.2,65,GREEN),run_time=.3);self.to(52)
  self.clear_body();self.show(txt('짝순열  +',3.7,31,GREEN,x=-1.9,width=3.4),txt('홀순열  −',3.7,31,GOLD,x=1.9,width=3.4),run_time=.3)
  for col,ps in enumerate([[(1,2,3),(2,3,1),(3,1,2)],[(1,3,2),(2,1,3),(3,2,1)]]):
   for row,p in enumerate(ps):self.show(cards(p,2.1-row*1.6,-1.9+col*3.8,.72),run_time=.3)
  self.show(eq(r'\mathrm{sgn}(\sigma)=(-1)^{\#\mathrm{swaps}}',-3.7,34,PURPLE),run_time=.3);self.to(61)
  self.clear_body()
  self.show(txt('같은 도착 순열: (1, 3, 2)',3.7,31,BLUE),eq(r'(1,2,3)\to(1,3,2)',2.3,36,GOLD),txt('2와 3 교환 · 1회',1.35,27,GOLD),eq(r'(1,2,3)\to(2,1,3)\to(1,2,3)\to(1,3,2)',-.1,27,GOLD),txt('1·2 교환 → 되돌리기 → 2·3 교환',-1.1,24,MUTED),txt('3회 · 홀수',-2.1,31,GOLD),txt('횟수는 달라도 홀짝성은 같다',-3.8,31,PURPLE),run_time=.4);self.to(66)

class Shot04(PermScene):
 shot=3
 def s04(self):
  self.show(cards((1,2),3.2),txt('이제 숫자는 선택할 열 번호',1.4,32,BLUE));self.to(70)
  self.clear_body();m,labels=mat(y=1.7);self.show(m,labels,txt('각 행에서 하나, 각 열도 한 번',-3.8,29,BLUE));self.to(73)
  formula=eq(r'\det(A)=ad-bc',-1,48);self.show(formula);self.to(76)
  box,a=self.choose(m,(1,2),'ad',-2.5,GREEN);self.to(79)
  self.play(FadeOut(box),FadeOut(a),run_time=.3);box,b=self.choose(m,(2,1),'bc',-2.5,GOLD);self.to(82)
  self.play(FadeOut(box),FadeOut(b),run_time=.3);self.to(85)
  self.clear_body()
  left,lab1=mat(y=1.6);left.scale(.8).shift(LEFT*1.95);lab1.scale(.8).shift(LEFT*1.95)
  right,lab2=mat(y=1.6);right.scale(.8).shift(RIGHT*1.95);lab2.scale(.8).shift(RIGHT*1.95)
  self.show(left,right,cards((1,2),3.65,-1.95,.72),cards((2,1),3.65,1.95,.72),selected(left,(1,2),GREEN),selected(right,(2,1),GOLD),run_time=.4)
  self.show(eq('ad',-.7,46,GREEN,x=-1.95,width=2),eq('bc',-.7,46,GOLD,x=1.95,width=2),txt('열 번호를 그대로 / 한 번 교환',-2.2,30));self.to(91)
  self.show(eq('+',-1.35,50,GREEN,x=-1.95,width=1),eq('-',-1.35,50,GOLD,x=1.95,width=1),txt('짝순열',.2,27,GREEN,x=-1.95,width=2.5),txt('홀순열',.2,27,GOLD,x=1.95,width=2.5),txt('부호는 각 곱셈 항의 계수',-3.3,27,MUTED));self.to(97)
  self.show(eq(r'\boxed{\det(A)=ad-bc}',-4.3,40,BLUE),run_time=.4);self.to(100)

class Shot05(PermScene):
 shot=4
 def s05(self):
  m,l=mat(3,y=2.3);self.show(m,l,txt('행마다 하나 · 같은 열 중복 없음',-.1,28,BLUE),run_time=.4);self.to(102)
  rows=[]
  for k,(p,term) in enumerate(zip(PERMS,TERMS)):
   color=GREEN if sign(p)>0 else GOLD;boxes=selected(m,p,color)
   self.play(FadeIn(boxes),run_time=.2)
   row=VGroup(smallperm(p,-1.2-(k//2)*1.1,-2 if k%2==0 else 1.7),eq(('+' if sign(p)>0 else '-')+term,-1.2-(k//2)*1.1,29,color,x=-.4 if k%2==0 else 3.2,width=1.3))
   self.play(TransformFromCopy(VGroup(*[m.get_entries()[i*3+j-1] for i,j in enumerate(p)]),row),run_time=.5);self.play(FadeOut(boxes),run_time=.2);rows.append(row)
  self.to(108);self.show(eq('3!=6',-4.3,34,BLUE),run_time=.3);self.to(112)
  self.clear_body();self.show(txt('짝순열의 세 항',3.4,33,GREEN),eq(r'+aei+bfg+cdh',2.3,44,GREEN),txt('홀순열의 세 항',.7,33,GOLD),eq(r'-afh-bdi-ceg',-.4,44,GOLD),eq(r'\det A=aei+bfg+cdh-afh-bdi-ceg',-2.5,33,BLUE),txt('모든 선택을 합한다 · 부호는 홀짝성',-4.1,27),run_time=.4);self.to(116)

class Shot06(PermScene):
 shot=5
 def s06(self):
  self.show(eq(r'+\qquad-',1.8,90,PURPLE),txt('왜 부호를 구분할까?',-.5,38));self.to(119)
  self.clear_body()
  o=np.array([-2.5,-.5,0]);u=np.array([3.,0,0]);v=np.array([1.5,1.5,0])
  poly=Polygon(o,o+u,o+u+v,o+v,color=PURPLE,fill_color=PURPLE,fill_opacity=.12)
  arrows=VGroup(Arrow(o,o+u,buff=0,color=BLUE),Arrow(o,o+v,buff=0,color=GOLD));self.show(poly,arrows,eq(r'A=[u\ v]=\begin{pmatrix}2&1\\0&1\end{pmatrix}',3.5,35),txt('u',-.9,30,BLUE,x=.4,width=.4),txt('v',1.4,30,GOLD,x=-1,width=.4),eq(r'\det A=+2',-3.4,43,GREEN),run_time=.4)
  seq=[o,o+u,o+u+v,o+v,o]
  self.add(VGroup(*[Arrow(a+.38*(b-a),a+.62*(b-a),buff=0,color=GREEN,stroke_width=3,max_tip_length_to_length_ratio=.5) for a,b in zip(seq,seq[1:])]),eq(r'O\to u\to u+v\to v\to O',-1.35,26,GREEN))
  path=VMobject(color=GREEN,stroke_width=6).set_points_as_corners([o,o+u,o+u+v,o+v,o]);self.play(ShowPassingFlash(path,time_width=.5),run_time=1.6);self.to(123)
  self.clear_body()
  self.add(poly,arrows,eq(r'B=[v\ u]=\begin{pmatrix}1&2\\1&0\end{pmatrix}',3.5,35),txt('u',-.9,30,BLUE,x=.4,width=.4),txt('v',1.4,30,GOLD,x=-1,width=.4),eq(r'\det B=-2',-3.4,43,GOLD))
  seq=[o,o+v,o+u+v,o+u,o]
  self.add(VGroup(*[Arrow(a+.38*(b-a),a+.62*(b-a),buff=0,color=GOLD,stroke_width=3,max_tip_length_to_length_ratio=.5) for a,b in zip(seq,seq[1:])]),eq(r'O\to v\to u+v\to u\to O',-1.35,26,GOLD))
  path=VMobject(color=GOLD,stroke_width=6).set_points_as_corners([o,o+v,o+u+v,o+u,o]);self.play(ShowPassingFlash(path,time_width=.5),run_time=1.6);self.to(126)
  self.show(txt('같은 넓이 · 반대 순회 방향',-2.15,31,PURPLE),cards((1,2),2.1,-1.8,.65),cards((2,1),2.1,1.8,.65),txt('→',2.1,32,PURPLE),txt('열 교환 1회 → 부호 반전',-4.4,27,PURPLE),run_time=.4);self.to(131)

class Shot07(PermScene):
 shot=6
 def s07(self):
  m=Matrix([['1','1'],['2','2']],h_buff=1.6,v_buff=1).move_to([0,2.1,0]);cols=m.get_columns();boxes=VGroup(*[SurroundingRectangle(c,color=RED,buff=.18) for c in cols]);self.show(m,boxes,txt('서로 같은 두 열',.1,34,RED));self.to(134)
  self.play(Swap(cols[0],cols[1],path_arc=PI/2),run_time=1);self.show(txt('교환해도 행렬 A는 그대로',-1.3,31));self.to(137)
  self.show(txt('열 교환 → 행렬식 부호 반전',-2.5,30,PURPLE));self.to(140)
  self.clear_body();self.show(eq(r'\det A=-\det A',2.7,51,PURPLE),run_time=.4);self.to(142)
  self.show(eq(r'2\det A=0',.8,49),run_time=.4);self.to(144)
  self.show(eq(r'\boxed{\det A=0}',-1.3,58,RED),run_time=.4);self.to(146)
  self.clear_body();self.show(eq(r'A=\begin{pmatrix}1&1\\2&2\end{pmatrix}',3.5,40,RED),run_time=.3)
  o=np.array([-1.3,-2.5,0]);unit=.9
  def shape(A):return Polygon(*[o+np.r_[A@np.array(p),0]*unit for p in [(0,0),(1,0),(1,1),(0,1)]],color=RED,fill_color=RED,fill_opacity=.12)
  start=np.eye(2);target=np.array([[1.,1.],[2.,2.]]);p=shape(start);self.add(p)
  self.play(UpdateFromAlphaFunc(p,lambda m,a:m.become(shape((1-a)*start+a*target))),run_time=2,rate_func=linear)
  self.show(eq(r'\mathrm{Area}=0',-3.6,42,RED),txt('두 열벡터가 겹침 · 평면 → 선분',-4.4,26,RED),run_time=.4);self.to(152)

class Shot08(PermScene):
 shot=7
 def s08(self):
  m,l=mat(3,y=2.1);self.show(m,l,run_time=.3)
  for p in PERMS:
   b=selected(m,p,GREEN if sign(p)>0 else GOLD);self.play(FadeIn(b),run_time=.2);self.play(FadeOut(b),run_time=.3)
  self.show(txt('각 행·각 열에서 하나씩 고른 곱',-.7,32,BLUE),eq(r'+aei+bfg+cdh',-2,36,GREEN),eq(r'-afh-bdi-ceg',-3.1,36,GOLD),run_time=.4);self.to(157)
  self.clear_body();self.show(txt('순열',3.4,44,BLUE),txt('어떤 원소를 곱할 것인가',2.35,31),txt('홀짝성',.6,44,PURPLE),txt('어떤 부호를 붙일 것인가',-.45,31),eq(r'\det A=ad-bc',-2.1,47,BLUE),txt('가능한 선택과 공간의 방향을 함께 계산한다',-3.9,29),run_time=.4);self.to(163)
