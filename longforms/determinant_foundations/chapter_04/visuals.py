"""Data-driven row operations, invariance, and triangular determinant calculation."""
import importlib.util,json,itertools,math
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('det_ch03_shared',R.parent/'chapter_03/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
tx,eq,fit=shared.tx,shared.eq,shared.fit
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED
PERMS=shared.PERMS;parity=shared.parity
A=np.array([[2,1,1],[4,3,3],[2,2,3]],dtype=int)
OPERATIONS=[(1,0,2),(2,0,1),(2,1,1)]
STATES=[A.copy()];L=np.eye(3,dtype=int)
for target,pivot,factor in OPERATIONS:
 nxt=STATES[-1].copy();nxt[target]-=factor*nxt[pivot];STATES.append(nxt);L[target,pivot]=factor
U=STATES[-1]
def matrix(a,x=0,y=.4,size=43):
 return Matrix([[str(v) for v in row] for row in a],h_buff=1.1,v_buff=.8,element_to_mobject=lambda s:MathTex(s,font_size=size,color=MUTED if s=='0' else INK)).move_to([x,y,0])
def symbol_grid(n,x=0,y=.4):
 g=VGroup(*[Square(side_length=2.3/n,stroke_width=0,fill_color=PURPLE,fill_opacity=.65 if i==j else .2).move_to([x+(j-(n-1)/2)*2.6/n,y+((n-1)/2-i)*2.6/n,0]) for i in range(n) for j in range(n)])
 return g
class EliminationScene(shared.RuleScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.add(tx('CHAPTER 04',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25))
  self.header=tx('행렬식의 효율적 계산 · 불변성과 소거법',0,2.94,31);self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def status(self,s='2',c=GREEN):
  badge=VGroup(RoundedRectangle(width=2.15,height=.52,corner_radius=.1,stroke_color=c,stroke_opacity=.3,fill_color=c,fill_opacity=.04).move_to([5.25,2.3,0]),eq(r'\det='+s,5.25,2.3,27,c,w=1.9))
  self.add(badge);return badge
 def row_update(self,m,row,values,d=.7):
  n=len(values);entries=m.get_entries()
  self.act(d,*[Transform(entries[row*n+j],eq(str(v),*entries[row*n+j].get_center()[:2],size=43,c=GREEN if v==0 else INK,w=1).match_height(entries[row*n+j])) for j,v in enumerate(values)])
 def shot_01(self):
  self.add(shared.cube(np.eye(3),[-3.8,.4,0],1.35),eq(shared.FORMULA,2.6,.5,34,PURPLE,w=7.1))
  self.to(7);self.clear();g=symbol_grid(3,0,.65);count=eq('3!=6',0,-1.3,49,PURPLE);self.show(g,count,d=.5)
  self.to(9);self.act(.7,Transform(g,symbol_grid(4,0,.65)),Transform(count,eq('4!=24',0,-1.3,49,PURPLE)))
  self.to(11);self.act(.7,Transform(g,symbol_grid(5,0,.65)),Transform(count,eq('5!=120',0,-1.3,49,PURPLE)));self.to(13)
  self.clear()
  for x,n in [(-4.2,3),(0,5),(4.2,10)]:self.show(symbol_grid(n,x,.75),tx(f'{n}×{n}',x,-.9,28,MUTED,w=3),tx(f'{math.factorial(n):,}',x,-1.65,35,RED if n==10 else PURPLE,w=3.8),d=.5)
  self.to(21);self.clear();self.show(eq('A\longrightarrow U',0,.85,78,PURPLE),self.note('행렬을 계산하기 쉬운 형태로 바꿀 수 있을까?',PURPLE),d=.6);self.to(26)
 def shot_02(self):
  k=ValueTracker(0);o=np.array([.6,-1.3,0]);unit=.95
  def geometry(z):
   u=unit*np.array([2,z,0]);v=unit*np.array([0,1,0]);pts=[o,o+u,o+u+v,o+v]
   return VGroup(shared.shared.outline(pts),Arrow(o,o+u,buff=0,color=BLUE,stroke_width=4),Arrow(o,o+v,buff=0,color=GOLD,stroke_width=4))
  g=geometry(0);self.add(g)
  nums=[DecimalNumber(v,num_decimal_places=1,font_size=35,color=BLUE if i%2==0 else GOLD) for i,v in enumerate([2,0,0,1])]
  m=MobjectMatrix([nums[:2],nums[2:]],h_buff=1.5,v_buff=.8).move_to([-3.7,.85,0]);self.add(m,eq(r'u=(2,0),\ v=(0,1)',-3.7,-.8,32,w=5.5));badge=self.status()
  self.to(30)
  def update(obj,t):z=2*t;obj.become(geometry(z));nums[2].set_value(z)
  self.act(3,UpdateFromAlphaFunc(g,update));self.to(34)
  base=Brace(Line(o,o+unit*UP),LEFT,color=GOLD);height=DoubleArrow(o+DOWN*.3,o+unit*2*RIGHT+DOWN*.3,buff=0,color=MUTED,tip_length=.12)
  self.show(base,eq('1',-.05,-.85,30,GOLD,w=.5),height,eq('2',1.55,-1.87,30,MUTED,w=1),tx('밑변 = 고정된 v',4.65,1.25,26,GOLD,w=3.4),tx('높이 = 수평거리 2',4.65,.55,25,MUTED,w=3.4),d=.5)
  self.to(39);self.show(self.note('모양은 달라져도 부호 있는 넓이는 2',GREEN),d=.5);self.act(.6,Indicate(badge,color=GREEN));self.to(42)
 def shot_03(self):
  self.add(eq(r'\det(u+kv,v)',0,1.95,51,PURPLE))
  self.show(eq(r'\det(a+b,c)=\det(a,c)+\det(b,c)',0,.8,43,w=12),d=.5);self.to(47)
  self.clear()
  for x,u,v,label in [(-4.1,(2,1),(0,1),r'\det(u+kv,v)'),(0,(2,0),(0,1),r'\det(u,v)'),(4.1,(0,1),(0,1),r'k\det(v,v)')]:
   g,p=shared.para(u,v,origin=(x-1,-.5,0),scale=.95);self.add(g,eq(label,x,-1.25,32,w=3.9))
  plus=eq('+',2.15,.1,40,GOLD,w=.8);equals=eq('=',-2,.1,40,w=.8);self.add(plus,equals)
  self.show(eq(r'\det(u+kv,v)=\det(u,v)+k\det(v,v)',0,1.95,40,w=12),d=.5);self.to(53)
  zero=eq('0',4.1,.95,55,RED,w=2);self.show(zero,d=.5)
  self.show(self.note('동일한 두 벡터: det(v,v)=0',RED),d=.5);self.to(59)
  self.clear(d=.3);self.show(eq(r'\det(u+kv,v)=\det(u,v)',0,.55,60,GREEN),d=.5);self.to(61)
 def shot_04(self):
  self.add(tx('열 연산',-3.4,2.05,30,BLUE,w=5),tx('행 연산',3.4,2.05,30,GOLD,w=5),eq(r'\begin{pmatrix}a+kb&b\\c+kd&d\end{pmatrix}',-3.4,.8,45,BLUE,w=5.8),eq(r'\begin{pmatrix}a+kc&b+kd\\c&d\end{pmatrix}',3.4,.8,45,GOLD,w=5.8),eq(r'C_1\leftarrow C_1+kC_2',-3.4,-.35,35,BLUE,w=5.7),eq(r'R_1\leftarrow R_1+kR_2',3.4,-.35,35,GOLD,w=5.7),eq(r'\det(A^T)=\det(A)',0,-1.5,42,PURPLE))
  self.to(66);self.clear(d=.3)
  self.show(eq(r'R_i\leftarrow R_i+kR_j\quad(i\ne j)',0,.95,53,GOLD),eq(r'\det(A^{\prime})=\det(A)',0,-.65,55,GREEN),d=.6);self.to(71)
 def shot_05(self):
  m=matrix([[2,1],[4,3]],-3.5,.5);self.add(m);self.show(SurroundingRectangle(m.get_entries()[2],color=RED,buff=.15),self.note('행렬식을 유지하며 이 원소를 0으로 만들 수 있을까?',PURPLE),d=.5);self.to(74)
  self.clear(d=.3);m=matrix([[2,1],[4,3]],-3.5,.6);self.add(m);self.status()
  self.show(eq(r'2\times3-1\times4=2',3,.6,44,GREEN,w=6),d=.5);self.to(79)
  self.clear(d=.3);m=matrix([[2,1],[4,3]],-3.5,.6);m.get_rows()[0].set_color(BLUE);self.add(m);self.status()
  self.show(eq(r'R_2\leftarrow R_2-2R_1',2.7,1.4,40,GOLD,w=6),eq('4-2(2)=0',2.7,.35,40,GREEN,w=6),eq('3-2(1)=1',2.7,-.65,40,w=6),d=.5)
  self.row_update(m,1,[0,1],1);self.to(84)
  self.clear(d=.3);self.status()
  self.show(matrix([[2,1],[4,3]],-3.3,.7),matrix([[2,1],[0,1]],3.3,.7),eq('2(3)-1(4)=2',-3.3,-.85,37,GREEN,w=5.7),eq('2(1)-1(0)=2',3.3,-.85,37,GREEN,w=5.7),self.note('원소는 단순해지고, 행렬식은 유지된다',GREEN),d=.5);self.to(89)
 def shot_06(self):
  m=matrix(A,0,.35);self.add(m);self.status()
  label=eq(r'R_2\leftarrow R_2-2R_1',0,2.15,36,GOLD,w=7);self.add(label)
  for k,(target,pivot,factor) in enumerate(OPERATIONS):
   if k:self.act(.2,Transform(label,eq(fr'R_{target+1}\leftarrow R_{target+1}-'+(str(factor) if factor!=1 else '')+fr'R_{pivot+1}',0,2.15,36,GOLD,w=7)))
   self.row_update(m,target,STATES[k+1][target],.85)
  self.to(94)
  for i,e in enumerate(m.get_entries()):e.set_color(GREEN if i//3==i%3 else MUTED if i//3>i%3 else INK)
  diagonal=Line(m.get_entries()[0].get_center()+UL*.3,m.get_entries()[8].get_center()+DR*.3,color=GREEN,stroke_opacity=.35)
  self.show(diagonal,tx('상삼각행렬 · Upper Triangular Matrix',0,-1.55,30,GREEN),eq(r'u_{ij}=0\quad(i>j)',0,-2.3,30,MUTED),d=.5);self.to(99)
 def shot_07(self):
  m=matrix(U,-3.7,.4);self.add(m);self.status()
  tags=VGroup(*[shared.cards(p,1.2+(k%3)*1.7,1.65-(k//3)*.65,.35) for k,p in enumerate(PERMS)]);self.add(tags)
  self.to(103)
  terms=VGroup()
  for k,p in enumerate(PERMS):
   values=[int(U[row,col]) for col,row in enumerate(p)];value=parity(p)*math.prod(values);c=GREEN if value else MUTED
   boxes=VGroup(*[SurroundingRectangle(m.get_entries()[row*3+col],color=GREEN if U[row,col] else RED,buff=.1) for col,row in enumerate(p)])
   text=eq(('+' if parity(p)>0 else '-')+'('+r'\times'.join(map(str,values))+')='+str(value),3,-.05-k*.32,27,c,w=5.9);terms.add(text)
   self.act(.25,FadeIn(boxes));self.act(.45,TransformFromCopy(VGroup(*[m.get_entries()[row*3+col] for col,row in enumerate(p)]),text));self.act(.25,FadeOut(boxes))
  self.to(111)
  self.act(.5,*[FadeOut(t) for t in list(terms)[1:]])
  self.show(eq(r'\det(U)=2\times1\times1=2',0,-2.2,44,GREEN,w=12),d=.5)
  # The first column forces row1, then column2 forces row2, and so on.
  for j in range(3):
   box=SurroundingRectangle(m.get_entries()[j*3+j],color=GREEN,buff=.1);self.show(box,d=.3)
  self.show(tx('일반형: det(U)=∏ uᵢᵢ',3,.45,27,GREEN,w=5.7),d=.3);self.to(116)
 def shot_08(self):
  self.add(matrix(A,-3.2,.6),matrix(U,3.2,.6),eq(r'\det A=\det U=2',0,-1.3,48,GREEN),self.note('가우스 소거법 · Gaussian Elimination',PURPLE));self.to(120)
 def shot_09(self):
  m=matrix([[0,2],[3,1]],-3,.55);m.get_rows()[0].set_color(BLUE);m.get_rows()[1].set_color(GOLD);self.add(m)
  badge=self.status('-6',RED);count=tx('행 교환: 0회',3,.6,33,MUTED,w=5);self.add(count)
  self.show(SurroundingRectangle(m.get_entries()[0],color=RED,buff=.14),d=.4);self.to(123)
  rows=m.get_rows();self.act(1,Swap(rows[0],rows[1],path_arc=PI/2),Transform(badge[1],eq(r'\det=+6',5.25,2.3,27,GREEN,w=1.9)),Transform(count,tx('행 교환: 1회',3,.6,33,GOLD,w=5)))
  self.show(eq(r'\det A=(-1)^1(3\times2)=-6',0,-1.05,43,RED),d=.5)
  self.show(eq(r'\det A=(-1)^s\prod_i u_{ii}',0,-2.15,39,PURPLE),d=.5);self.to(130)
 def shot_10(self):
  l=matrix(np.eye(3,dtype=int),-3.2,.45);u=matrix(U,3.2,.45);self.add(l,u);self.status()
  self.add(tx('L · 소거에 사용한 배수 기록',-3.2,2.0,26,BLUE,w=5.8),tx('U · 상삼각행렬',3.2,1.75,27,GOLD,w=5))
  for target,pivot,factor in OPERATIONS:
   entry=l.get_entries()[target*3+pivot];self.act(.6,Transform(entry,eq(str(factor),*entry.get_center()[:2],size=43,c=BLUE,w=1)))
  self.to(135)
  self.show(eq('A=LU',0,-1.3,49,PURPLE),eq(r'\det A=\det L\det U=1\times2=2',0,-2.2,42,GREEN),d=.5)
  self.show(tx('행 교환이 필요하면 PA=LU',0,2.35,20,MUTED,w=8),d=.4);self.to(141)
 def shot_11(self):
  axes=Axes(x_range=[2,16,2],y_range=[0,14,2],x_length=6.2,y_length=3.5,axis_config=dict(color=MUTED,include_tip=False,font_size=18)).move_to([2.7,.3,0]);self.add(axes)
  self.add(tx('log₁₀ 성장률 · 실제 실행시간 아님',2.7,2.35,21,MUTED,w=6.5))
  xs=list(range(2,16));fact=VMobject(color=RED).set_points_as_corners([axes.c2p(n,math.lgamma(n+1)/math.log(10)) for n in xs]);cubic=VMobject(color=GREEN).set_points_as_corners([axes.c2p(n,math.log10(n**3)) for n in xs])
  self.act(1.3,Create(fact),Create(cubic))
  self.show(eq(r'n!\ \mathrm{terms}',-3.8,1.25,43,RED,w=4.7),eq(r'O(n\cdot n!)',-3.8,.3,40,RED,w=4.7),eq(r'O(n^3)',-3.8,-1.1,55,GREEN,w=4.7),tx('단순 직접 전개의 산술연산',-3.8,-.3,20,MUTED,w=4.8),d=.5)
  self.show(tx('log₁₀(n!)',5.3,2.0,20,RED,w=2.5),tx('log₁₀(n³)',4.8,-1.1,20,GREEN,w=2.5),self.note('(n−1)² + (n−2)² + … + 1² = O(n³)',GREEN),d=.5);self.to(149)
 def shot_12(self):
  left=VGroup(*[eq(r'\times',-5+(k%4)*.9,1.5-(k//4)*.8,34,PURPLE,w=.7) for k in range(12)])
  right=VGroup(*[eq(r'\times' if k<3 else '0',1+(k%4)*.9,1.5-(k//4)*.8,34,GREEN if k<3 else MUTED,w=.7) for k in range(12)])
  self.add(left,right,tx('같은 곱셈을 반복',-3.65,-1.25,28,PURPLE,w=5.5),tx('필요한 계산 자체를 줄임',2.35,-1.25,28,GREEN,w=6));self.to(154)
  self.clear(d=.3)
  self.show(matrix(A,-3.2,.7),matrix(U,3.2,.7),eq('18+8+6-12-12-6=2',-3.2,-1.05,30,PURPLE,w=6),eq(r'2\times1\times1=2',3.2,-1.05,39,GREEN,w=6),self.note('구하려는 값은 유지하고, 계산 구조를 바꾼다',GREEN),d=.6);self.to(160)
 def shot_13(self):
  labels=[('다중선형성·교대성','행렬식의 성질'),('불변성','값을 보존하는 연산'),('상삼각행렬','계산하기 쉬운 구조'),('가우스 소거법','효율적인 알고리즘')]
  for k,(a,b) in enumerate(labels):
   x=-4.8+k*3.2;self.show(tx(a,x,.85,27,PURPLE if k==0 else GREEN,w=3),tx(b,x,-.2,21,MUTED,w=3),d=.4)
   if k:self.show(Arrow([x-1.9,.5,0],[x-1.5,.5,0],buff=0,color=MUTED,tip_length=.1),d=.2)
  self.show(self.note('수학적 성질의 이해 → 새로운 계산 알고리즘',PURPLE),d=.4);self.to(165)
 def shot_14(self):
  # Both panels use the same screen coordinate unit; the elongated shape is not rescaled.
  self.add(eq(r'I=\begin{pmatrix}1&0\\0&1\end{pmatrix}',-3.5,1.65,37,w=5),eq(r'B=\begin{pmatrix}4&0\\0&0.25\end{pmatrix}',3.2,1.65,37,w=5.8))
  square=Rectangle(width=1.15,height=1.15,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([-3.5,-.35,0]);flat=Rectangle(width=4.6,height=.2875,stroke_color=GOLD,fill_color=GOLD,fill_opacity=.12).move_to([3.2,-.35,0])
  self.add(square,flat,eq(r'\det I=1',-3.5,-1.35,38,GREEN,w=5),eq(r'\det B=1',3.2,-1.35,38,GREEN,w=5))
  self.show(self.note('행렬식은 공간의 변화를 어디까지 알려줄까?',PURPLE),d=.5);self.to(171)
