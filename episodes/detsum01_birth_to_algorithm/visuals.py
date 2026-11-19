"""Portrait summary; shared geometry and exact row/permutation data."""
import importlib.util,json,textwrap,itertools,math
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('detsum_shared',R.parents[1]/'longforms/determinant_foundations/chapter_04/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
basis=shared.shared;geometry=basis.shared;foundation=geometry.shared
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED
config.frame_width=9;config.frame_height=16;config.frame_rate=30
def tx(s,y=0,size=34,c=INK,x=0,w=7.5):return foundation.tx(s,x,y,size,c,w)
def eq(s,y=0,size=48,c=INK,x=0,w=7.5):return foundation.eq(s,x,y,size,c,w)
def mat(a,y=2,size=47):return shared.matrix(a,0,y,size)
def board(M=None):return geometry.Board(np.eye(2) if M is None else M,origin=(-2.6,-.8,0),unit=1.2,bounds=(-3.65,3.65,-1.7,4.1))
def para(k=0):
 o=np.array([-2.3,-1.4,0]);u=np.array([4.,k*1.4,0]);v=np.array([0,1.4,0])
 return VGroup(geometry.outline([o,o+u,o+u+v,o+v]),Arrow(o,o+u,buff=0,color=BLUE),Arrow(o,o+v,buff=0,color=GOLD))
def combinations():
 return VGroup(*[basis.cards(p,-2.65+(j%3)*2.65,3.7-(j//3)*.73,.36) for j,p in enumerate(basis.COMBINATIONS)])
def graph(second=(1,1,3),dots=True):return foundation.graph_state(second,dots).scale(1.12).move_to([0,.7,0])

class SummaryScene(foundation.ChapterScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  phase=0 if self.start<29 else 1 if self.start<58 else 2 if self.start<102 else 3 if self.start<144 else 4
  titles=['행렬식은 왜 만들어졌을까?','공간의 부피와 방향','행렬식은 왜 순열로 계산할까?','성질을 이용해 계산을 바꾸다','행렬식이 추출하는 정보']
  self.masthead=VGroup(tx('DETERMINANT',7.1,19,MUTED),*[Line([-3.5+j*1.43,6.65,0],[-2.35+j*1.43,6.65,0],color=PURPLE if j<=phase else MUTED,stroke_width=4,stroke_opacity=1 if j<=phase else .2) for j in range(5)])
  self.header=tx(titles[phase],5.95,34);self.add(self.masthead,self.header)
  self.panel=RoundedRectangle(width=8,height=1.65,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-5.35,0]).set_z_index(50)
  self.cap=VGroup();self.add(self.panel,self.cap);self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f's{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def set_caption(self,t):
  line=next((l for l in self.lines if l['start']<=t<l['end']),None)
  if line is None or line==self.current:return
  self.current=line;parts=textwrap.wrap(line['text'],width=31,break_long_words=False,break_on_hyphens=False)
  m=VGroup(*[tx(s,size=25,w=7.5) for s in parts]).arrange(DOWN,buff=.12).move_to([0,-5.35,0]).set_z_index(51)
  self.remove(self.cap);self.cap=m;self.add(m)
  self.audit.append(dict(start=line['start'],end=line['end'],left=float(m.get_left()[0]),right=float(m.get_right()[0]),bottom=float(m.get_bottom()[1]),top=float(m.get_top()[1])))
 def clear(self,d=.3):
  keep=[self.masthead,self.header,self.panel,self.cap];obs=[m for m in self.mobjects if m not in keep]
  if obs:self.act(d,*[FadeOut(m) for m in obs])
 def note(self,s,c=INK):return tx(s,-3.65,29,c)
 def morph(self,b,M,d):
  old=b.M.copy();self.act(d,UpdateFromAlphaFunc(b,lambda m,t:m.update_matrix((1-t)*old+t*np.array(M))))
 def s01(self):
  m=foundation.matrix(0,2.8);self.add(m)
  es=m.get_entries();self.act(.55,Create(Line(es[0].get_center(),es[3].get_center(),color=BLUE)),Create(Line(es[1].get_center(),es[2].get_center(),color=GOLD)))
  self.show(eq('ad-bc',-.1,69,PURPLE),d=.5);self.to(3);self.clear()
  self.show(tx('역사적 발전 순서',4.1,31,GOLD),eq('ad-bc',2.7,65,PURPLE),tx('17세기 후반 · 행렬식 연구',1.7,28,GOLD),Arrow([0,1,0],[0,-.1,0],color=MUTED,buff=0),foundation.matrix(0,-1.2),tx('19세기 · 현대 행렬 이론',-2.6,28,PURPLE),d=.5)
  self.to(8);self.clear();self.show(foundation.equations(True,0,1.7),self.note('출발점은 연립방정식',BLUE),d=.5);self.to(13)
 def s02(self):
  e=foundation.equations(True,0,2.9);self.add(e)
  expanded=eq(r'\begin{aligned}ad\,x+bd\,y&=de\\bc\,x+bd\,y&=bf\end{aligned}',.4,48,BLUE)
  self.act(.8,TransformFromCopy(e,expanded));self.show(eq(r'(ad-bc)x=de-bf',-2.2,51,PURPLE),self.note('같은 y항을 빼서 제거',MUTED),d=.6);self.to(17)
 def s03(self):
  g=graph();self.add(g);status=VGroup(eq(r'\det(A)=1',4.2,45,GREEN),tx('유일한 해',-2.6,37,GREEN));self.add(status)
  self.to(18.5);n=graph((4,2,3),False);self.act(.5,Transform(g,n),Transform(status,VGroup(eq(r'\det(A)=0',4.2,45,RED),tx('해 없음',-2.6,37,RED))))
  self.to(20.5);n=graph((4,2,10),False)
  self.act(.5,Transform(g,n),Transform(status,VGroup(eq(r'\det(A)=0',4.2,45,GOLD),tx('무한히 많은 해',-2.6,37,GOLD))))
  self.to(23)
 def s04(self):
  self.add(foundation.equations(True,0,3.3));m=foundation.matrix(0,.25);self.show(m,d=.5)
  self.show(eq(r'\det(A)=ad-bc',-2.0,56,PURPLE),self.note('해의 유일성을 판단하는 값',GREEN),d=.5)
  self.to(27);self.act(.7,*[m.get_columns()[j].animate.set_color(c) for j,c in enumerate([BLUE,GOLD])]);self.to(29)
 def s05(self):
  m=foundation.matrix(0,3.5);self.add(m,eq(r'\mathbf v_1=(a,c)',1.7,43,BLUE),eq(r'\mathbf v_2=(b,d)',.7,43,GOLD));self.to(33);self.clear()
  b=board();self.add(b,eq(r'A=\begin{pmatrix}3&1\\1&3\end{pmatrix}',4.9,39,PURPLE))
  self.morph(b,[[3,1],[1,3]],3.6);self.show(eq(r'\mathbf e_1\to(3,1),\quad\mathbf e_2\to(1,3)',-2.6,35,BLUE),self.note('단위 정사각형 → 평행사변형',PURPLE),d=.5);self.to(39)
 def s06(self):
  o=np.array([-2.7,-.8,0]);u=1.35
  def p(x,y):return o+u*np.array([x,y,0])
  poly=geometry.outline([p(0,0),p(3,1),p(4,4),p(1,3)]);self.add(poly,tx('양의 성분 · 양의 행렬식 예시',4.9,24,MUTED))
  outside=VGroup(*[Polygon(*[p(*v) for v in verts],stroke_width=1,stroke_color=c,fill_color=c,fill_opacity=.25) for c,verts in [(BLUE,[(0,0),(3,0),(3,1)]),(BLUE,[(1,3),(1,4),(4,4)]),(GOLD,[(0,0),(0,3),(1,3)]),(GOLD,[(3,1),(4,1),(4,4)]),(RED,[(0,3),(1,3),(1,4),(0,4)]),(RED,[(3,0),(4,0),(4,1),(3,1)])]])
  self.show(outside,eq(r'(a+b)(c+d)-ac-bd-2bc',-1.8,33,MUTED),d=.5)
  self.act(.8,FadeOut(outside));self.show(eq(r'S=|ad-bc|=8',-2.75,55,PURPLE),d=.5);self.to(44)
 def s07(self):
  b=board([[3,1],[1,3]]);self.add(b);self.morph(b,[[3,3],[1,1]],2.2)
  self.show(eq(r'\det(A)=0',-2.7,51,RED),d=.4);self.to(47);self.clear(.25)
  pts=[[-1.5,-.2,0],[1.5,-.2,0],[1.5,2.8,0],[-1.5,2.8,0]]
  g=VGroup(geometry.outline(pts),basis.arrows([np.array(p) for p in pts],c=GREEN),*[eq(str(j+1),p[1],27,GREEN,x=p[0]) for j,p in enumerate(pts)])
  self.add(g);self.act(1.2,g.animate.apply_matrix(np.diag([-1,1,1])).set_color(RED));self.show(eq(r'\det(B)=-1',-2.5,50,RED),d=.4);self.to(50)
 def s08(self):
  cube=basis.cube(np.eye(3),[0,1.25,0],2.1);self.add(cube,tx('3차원 · 단위 정육면체',4.6,31,BLUE))
  new=basis.cube(np.diag([2,1,1]),[-.9,1.25,0],1.7);self.act(2,Transform(cube,new));self.show(eq(r'V=|\det(A)|',-1.8,55,PURPLE),tx('n차원에서도 부피의 배율',-3.0,31,GREEN),d=.5);self.to(58)
  self.act(.7,*[cube[j].animate.set_fill(opacity=.015).set_stroke(opacity=.15) for j in range(6)])
  self.show(self.note('부피와 방향의 성질 → 계산 공식',PURPLE),d=.4);self.to(62)
 def s09(self):
  o=np.array([-2.5,.8,0]);v=np.array([4.,2.,0]);self.add(Arrow(o,o+v,buff=0,color=BLUE),DashedLine(o,o+[4,0,0],color=BLUE),DashedLine(o+[4,0,0],o+v,color=BLUE),eq(r'\mathbf v_1=a\mathbf e_1+c\mathbf e_2',4.3,44,BLUE),eq(r'\mathbf v_2=b\mathbf e_1+d\mathbf e_2',-.3,44,GOLD));self.to(65);self.clear()
  self.add(eq(r'\det(a\mathbf e_1+c\mathbf e_2,',4.2,37,BLUE),eq(r'b\mathbf e_1+d\mathbf e_2)',3.35,37,GOLD))
  terms=[r'ab\det(\mathbf e_1,\mathbf e_1)',r'+ad\det(\mathbf e_1,\mathbf e_2)',r'+bc\det(\mathbf e_2,\mathbf e_1)',r'+cd\det(\mathbf e_2,\mathbf e_2)']
  for j,s in enumerate(terms):self.show(eq(s,1.8-j*1.25,43,PURPLE),d=.45)
  self.show(self.note('각 열벡터에 대한 선형성',GREEN),d=.4);self.to(71)
 def s10(self):
  self.add(eq(r'\mathbf v_j=a_{1j}\mathbf e_1+a_{2j}\mathbf e_2+a_{3j}\mathbf e_3',4.8,35,BLUE),tx('세 열에서 방향을 하나씩 선택',3.9,28,MUTED))
  g=combinations().scale(.82).shift(DOWN*.5);self.act(3,LaggedStart(*[FadeIn(x) for x in g],lag_ratio=.06))
  self.show(eq(r'3\times3\times3=27',-3.5,51,PURPLE),d=.5);self.to(78)
 def s11(self):
  self.add(basis.cards((0,0,1),0,4.6,.65),eq(r'(\mathbf e_1,\mathbf e_1,\mathbf e_2)',3.3,42,RED))
  M=np.array([[1,1,0],[0,0,1],[0,0,0]])
  flat=basis.cube(M,[0,1.0,0],1.6);self.add(flat,tx('같은 방향이 반복되면',-.2,31,RED),eq('V=0',-1.2,57,RED))
  self.show(eq(r'\det(\mathbf e_1,\mathbf e_2,\mathbf e_3)=1',-2.8,39,GREEN),d=.5);self.to(83)
 def s12(self):
  g=combinations();self.add(g);bad=[i for i,p in enumerate(basis.COMBINATIONS) if len(set(p))<3]
  crosses=VGroup(*[Cross(g[i],stroke_color=RED,stroke_width=2) for i in bad]);self.act(1.5,LaggedStart(*[Create(c) for c in crosses],lag_ratio=.025));self.to(87)
  self.act(.7,FadeOut(crosses),*[FadeOut(g[i]) for i in bad])
  good=[i for i,p in enumerate(basis.COMBINATIONS) if len(set(p))==3]
  self.act(1.2,*[g[i].animate.move_to([-1.8+3.6*(j%2),2.9-(j//2)*1.7,0]).scale(1.5) for j,i in enumerate(good)])
  self.show(eq(r'3^3=27\quad\longrightarrow\quad3!=6',-2.7,42,GREEN),d=.4);self.to(91);self.show(tx('순열 · Permutation',-3.6,32,PURPLE),d=.4);self.to(92)
 def s13(self):
  g=basis.cards((0,1,2),0,2.7,1);sign=eq('+1',.8,65,GREEN);self.add(g,sign,tx('두 벡터의 순서를 교환',4.5,32,MUTED))
  self.act(.8,Swap(g[0],g[1]));self.act(.3,Transform(sign,eq('-1',.8,65,RED)))
  self.to(95);self.act(.8,Swap(g[1],g[2]));self.act(.3,Transform(sign,eq('+1',.8,65,GREEN)))
  self.show(eq(r'\text{even}: +\qquad\text{odd}: -',-1.3,40,PURPLE),self.note('교환할 때마다 방향과 부호 반전',PURPLE),d=.4);self.to(99);self.clear()
  self.show(tx('라이프니츠 공식',4.3,37,PURPLE),eq(r'\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)',1.8,43,PURPLE),eq(r'\cdot\prod_{j=1}^{n}a_{\sigma(j),j}',-.2,49,BLUE),tx('각 열에서 하나씩 · 서로 다른 행',-2.5,30,GREEN),d=.5);self.to(102)
 def s14(self):
  for j,(n,count) in enumerate([(3,'6'),(5,'120'),(10,'3,628,800')]):
   y=4-j*2.25;self.show(eq(f'{n}\\times{n}',y,38,PURPLE,x=-2.5,w=2),eq(f'{n}!= {count}',y,42,RED if n==10 else INK,x=1,w=4.8),d=.4)
  self.to(107);self.act(.7,Indicate(self.mobjects[-1],color=RED));self.to(111)
  self.show(self.note('값을 보존하며 구조를 바꿀 수 있다면?',GREEN),d=.6);self.to(115)
 def s15(self):
  p=para(0);self.add(p,eq(r'\det(\mathbf u+k\mathbf v,\mathbf v)',4.0,43,PURPLE),eq(r'=\det(\mathbf u,\mathbf v)',2.8,43,GREEN))
  self.act(3.2,UpdateFromAlphaFunc(p,lambda m,t:m.become(para(1.5*t))))
  self.show(eq(r'S=4\times1.4=5.6',-2.1,43,GREEN),self.note('모양은 변해도 부호 있는 넓이는 유지',GREEN),d=.5);self.to(122)
 def s16(self):
  m=mat(shared.A,1.7);self.add(m,eq(r'\det(A)=2',-2.5,50,GREEN));op=eq(r'R_2\leftarrow R_2-2R_1',4.4,34,BLUE);self.add(op)
  labels=[r'R_2\leftarrow R_2-2R_1',r'R_3\leftarrow R_3-R_1',r'R_3\leftarrow R_3-R_2']
  for j in range(3):
   self.act(.3,Transform(op,eq(labels[j],4.4,34,BLUE)));self.act(.9,Transform(m,mat(shared.STATES[j+1],1.7)))
  self.show(self.note('행 교환이 있으면 부호를 함께 보정',MUTED),d=.4);self.to(128)
 def s17(self):
  m=mat(shared.U,1.7);self.add(m,tx('상삼각행렬',4.4,34,GREEN))
  ps=basis.PERMS;labels=VGroup(*[eq(('+' if basis.parity(p)>0 else '-')+r'('+r'\cdot'.join(str(shared.U[p[j],j]) for j in range(3))+')',-1.1-(k//2)*.75,26,GREEN if k==0 else MUTED,x=-1.8+(k%2)*3.6,w=3.4) for k,p in enumerate(ps)])
  self.show(labels,d=.5);self.act(.7,*[labels[k].animate.set_opacity(.2) for k in range(1,6)])
  boxes=VGroup(*[SurroundingRectangle(m.get_entries()[i*3+i],color=GREEN,buff=.15) for i in range(3)])
  self.show(boxes,eq(r'\det(A)=2\times1\times1=2',-3.4,39,GREEN),d=.5);self.to(133)
  self.act(.6,Indicate(boxes,color=GREEN));self.to(137)
 def s18(self):
  self.add(tx('순열 항의 개수',4.1,31,MUTED),eq('n!',2.9,70,RED),tx('단순 직접 전개의 산술연산',1.4,29,MUTED),eq(r'O(n\cdot n!)',.2,58,RED),Arrow([0,-.6,0],[0,-1.3,0],buff=0,color=MUTED),eq(r'O(n^3)',-2.3,66,GREEN),self.note('행 연산으로 계산 구조를 단순화',GREEN));self.to(144)
 def s19(self):
  o=np.array([-3.2,.8,0]);unit=.65
  def shape(k):return Polygon(o,o+[unit*k,0,0],o+[unit*k,unit/k,0],o+[0,unit/k,0],color=GREEN,fill_color=GREEN,fill_opacity=.2)
  p=shape(1);ghost=shape(1).set_fill(opacity=0).set_stroke(MUTED,1)
  k=ValueTracker(1);nums=VGroup(DecimalNumber(1,num_decimal_places=1,font_size=48,color=BLUE),DecimalNumber(1,num_decimal_places=3,font_size=48,color=GOLD)).arrange(RIGHT,buff=1.5).move_to([0,3.4,0])
  self.add(p,ghost,nums,tx('가로 k',4.4,31,BLUE,x=-1.2,w=3),tx('세로 1/k',4.4,31,GOLD,x=1.4,w=3))
  def update(m,t):v=1+9*t;m.become(shape(v));nums[0].set_value(v);nums[1].set_value(1/v)
  self.act(4.3,UpdateFromAlphaFunc(p,update));self.to(149)
  self.show(eq(r'\det(A)=10\times\frac1{10}=1',-1.3,46,GREEN),d=.5);self.to(153)
  self.show(tx('형태의 세부 정보는 담지 않는다',-3.1,32,PURPLE),d=.5);self.to(157)
 def s20(self):
  g=shared.symbol_grid(5,0,3);self.add(g,Arrow([0,1.3,0],[0,.2,0],buff=0,color=MUTED),eq(r'\det(A)',-.6,68,PURPLE),tx('전체 부피와 방향',-2.6,39,GREEN));self.to(161)
 def s21(self):
  formulas=[r'(ad-bc)x=de-bf',r'S=|\det A|',r'\sum_{\sigma}\operatorname{sgn}(\sigma)\prod_j a_{\sigma(j),j}',r'\det A=\prod_i u_{ii}']
  titles=['대수학 · 해의 유일성','기하학 · 부피와 방향','순열 · 계산 공식','불변성 · 효율적인 계산']
  boxes=VGroup()
  for j in range(4):
   y=4.05-j*2.05;c=[BLUE,GOLD,GREEN,PURPLE][j];box=RoundedRectangle(width=7.1,height=1.8,corner_radius=.12,color=c,stroke_opacity=.5).move_to([0,y-.25,0]);boxes.add(box);self.add(box,tx(titles[j],y+.25,28,c),eq(formulas[j],y-.55,31,c,w=6.7))
  for j in range(4):self.act(1.6,Indicate(boxes[j],color=[BLUE,GOLD,GREEN,PURPLE][j],scale_factor=1.025))
  self.to(168)
 def s22(self):
  grid=shared.symbol_grid(5,0,3.1);self.add(grid,tx('복잡한 수학적 대상',4.9,31,MUTED))
  op=eq(r'\det(A)',.3,75,PURPLE);self.show(Arrow([0,1.5,0],[0,.95,0],buff=0,color=MUTED),op,d=.6)
  self.show(tx('부피와 방향을 하나의 값으로',-1.4,35,GREEN),tx('중요한 성질을 추출하면',-2.65,31,INK),tx('서로 다른 문제가 연결된다',-3.6,33,PURPLE),d=.6)
  self.act(1.3,Indicate(op,color=PURPLE));self.to(177)
