"""Fixed-scale area-preserving transforms and a unified determinant finale."""
import importlib.util,json,math
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('det_ch04_shared',R.parent/'chapter_04/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
basis=shared.shared;geometry=basis.shared;foundation=geometry.shared
tx,eq,fit=shared.tx,shared.eq,shared.fit
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED
UNIT=np.array([[0,0],[1,0],[1,1],[0,1]],dtype=float)
def transform(kind,t=1):
 if kind=='stretch':k=1+3*t;return np.diag([k,1/k])
 if kind=='shear':return np.array([[1,1.5*t],[0,1]],dtype=float)
 if kind=='rotation':a=t*PI/4;return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
 return np.eye(2)
def shape(M,origin,unit=.5,c=PURPLE):
 return Polygon(*[np.array(origin)+np.r_[np.asarray(M)@p,0]*unit for p in UNIT],stroke_color=c,stroke_width=3,fill_color=c,fill_opacity=.15)
def comparison(t=1,matrices=True):
 group=VGroup();polygons=VGroup();labels=[]
 formulas=[r'I=\begin{pmatrix}1&0\\0&1\end{pmatrix}',r'\begin{pmatrix}4&0\\0&1/4\end{pmatrix}',r'\begin{pmatrix}1&1.5\\0&1\end{pmatrix}',r'\frac1{\sqrt2}\begin{pmatrix}1&-1\\1&1\end{pmatrix}']
 for j,(kind,title,c) in enumerate(zip(['identity','stretch','shear','rotation'],['항등','크기 변환','전단','45° 회전'],[BLUE,GOLD,GREEN,PURPLE])):
  x=-4.8+3.2*j;origin=np.array([x-.75,.15,0])
  grid=VGroup(*[Line([x-1.35,.15+n*.5,0],[x+1.35,.15+n*.5,0],color=MUTED,stroke_width=.8,stroke_opacity=.18) for n in [-1,0,1,2,3]],*[Line([x-.75+n*.5,-.35,0],[x-.75+n*.5,1.65,0],color=MUTED,stroke_width=.8,stroke_opacity=.18) for n in [-1,0,1,2,3,4]])
  ghost=shape(np.eye(2),origin,.5,MUTED).set_fill(opacity=0).set_stroke(opacity=.45,width=1)
  poly=shape(transform(kind,t),origin,.5,c);polygons.add(poly)
  group.add(grid,ghost,poly,tx(title,x,2.1,26,c,w=3))
  if matrices:group.add(eq(formulas[j],x,-1.0,28,c,w=2.95))
  label=eq(r'\det=1',x,-1.95,31,GREEN,w=3);labels.append(label);group.add(label)
 group.polygons=polygons;group.labels=labels
 return group
def concept_map():
 g=VGroup();nodes=VGroup();links=VGroup()
 for j,(x,y,label,c) in enumerate([(-4.1,1.2,'해의 유일성',BLUE),(4.1,1.2,'부피와 방향',GOLD),(-4.1,-1.2,'계산의 구조',GREEN),(4.1,-1.2,'불변성과 효율',PURPLE)]):
  panel=RoundedRectangle(width=3.9,height=1.65,corner_radius=.15,stroke_color=c,stroke_width=1.5,fill_color=c,fill_opacity=.035).move_to([x,y,0])
  node=VGroup(panel,tx(label,x,y+.48,26,c,w=3.5))
  if j==0:node.add(eq('(ad-bc)x=de-bf',x,y-.25,25,c,w=3.5))
  elif j==1:
   icon,p=basis.para(origin=(x-.55,y-.55,0),scale=.38,c=GOLD);node.add(icon)
  elif j==2:node.add(basis.cards((0,1,2),x,y-.25,.37),eq('+',x+1.05,y-.25,28,GREEN,w=.4))
  else:node.add(shared.matrix(shared.U,x,y-.22,29).scale(.4))
  link=Line([x-math.copysign(1.95,x),y,0],[math.copysign(.68,x),math.copysign(.25,y),0],color=c,stroke_opacity=.45,stroke_width=1.5);links.add(link);nodes.add(node)
 center=VGroup(Circle(radius=.76,color=INK,stroke_width=2,fill_color=INK,fill_opacity=.03),eq(r'\det(A)',0,0,34,INK,w=1.35))
 g.add(links,nodes,center);g.nodes=nodes;g.links=links;g.center_node=center
 return g
def extraction():
 grid=shared.symbol_grid(5,-4.6,.55)
 op=VGroup(Circle(radius=.65,color=PURPLE),eq(r'\det',0,.55,37,PURPLE,w=1));op[0].move_to([0,.55,0])
 dest=VGroup(RoundedRectangle(width=2.1,height=1.25,corner_radius=.15,color=GREEN,fill_color=GREEN,fill_opacity=.06).move_to([4.4,.55,0]),eq('d',4.4,.55,60,GREEN,w=1.4))
 lines=VGroup(*[Line(cell.get_right(),[-.65,.55,0],color=PURPLE,stroke_opacity=.16,stroke_width=1) for cell in grid])
 g=VGroup(grid,lines,op,Arrow([.8,.55,0],[3.2,.55,0],buff=.05,color=MUTED),dest,tx('n²개의 원소',-4.6,-1.25,28,MUTED,w=4),tx('정보 추출',0,-.7,27,PURPLE,w=3),tx('하나의 값',4.4,-.7,27,GREEN,w=3))
 g.grid=grid;g.operation=op;g.destination=dest
 return g

class FinaleScene(shared.EliminationScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.masthead=VGroup(tx('CHAPTER 05',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25));self.add(self.masthead)
  self.header=tx('행렬식이 담고 있는 정보',0,2.94,31);self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def shot_01(self):
  self.add(shared.matrix(shared.A,-3.2,.6),shared.matrix(shared.U,3.2,.6),eq(r'\det(A)=\det(U)=2',0,-1.4,46,GREEN))
  self.to(7);self.clear(d=.4)
  self.show(eq(r'A\ne B,\qquad\det(A)=\det(B)',0,.8,57,PURPLE),self.note('행렬식이 같다면 공간의 변형도 같을까?',PURPLE),d=.6);self.to(12)
 def shot_02(self):
  # Fixed origin and fixed unit throughout k=1→4→10. No endpoint matrix interpolation.
  o=np.array([-.7,-.45,0]);unit=.65
  def rect(k):return shape(np.diag([k,1/k]),o,unit,GREEN)
  grid=VGroup(*[Line([-.95,-1.4+j*.65,0],[6.15,-1.4+j*.65,0],color=MUTED,stroke_opacity=.15,stroke_width=1) for j in range(6)],*[Line([-.7+j*.65,-1.4,0],[-.7+j*.65,2.1,0],color=MUTED,stroke_opacity=.15,stroke_width=1) for j in range(11)])
  ghost=rect(1).set_fill(opacity=0).set_stroke(MUTED,1,opacity=.6);poly=rect(1);self.add(grid,ghost,poly)
  nums=[DecimalNumber(v,num_decimal_places=3 if j==3 else 1,font_size=35,color=BLUE if j==0 else GOLD if j==3 else MUTED) for j,v in enumerate([1,0,0,1])]
  mat=MobjectMatrix([nums[:2],nums[2:]],h_buff=1.55,v_buff=.8).move_to([-3.8,.85,0]);self.add(mat);badge=self.status('1')
  formula=eq(r'S=1\times1=1',-3.8,-1.25,38,GREEN,w=5);self.add(formula)
  def morph(start,end,d):
   def upd(m,t):k=(1-t)*start+t*end;m.become(rect(k));nums[0].set_value(k);nums[3].set_value(1/k)
   self.act(d,UpdateFromAlphaFunc(poly,upd))
  self.to(15);morph(1,4,4.5);self.to(20)
  self.act(.5,Transform(formula,eq(r'S=4\times\frac14=1',-3.8,-1.25,38,GREEN,w=5)))
  self.act(.5,Indicate(badge,color=GREEN));self.to(25);morph(4,10,4.5);self.to(30)
  self.act(.5,Transform(formula,eq(r'S=10\times\frac1{10}=1',-3.8,-1.25,38,GREEN,w=5)))
  self.show(self.note('가로 k × 세로 1/k = 1 · 좌표 단위 고정',GREEN),d=.5);self.to(34)
 def shot_03(self):
  g=comparison(0);self.add(g)
  # One parameter controls valid area-preserving paths, including the actual rotation angle.
  kinds=['identity','stretch','shear','rotation']
  self.act(3.7,UpdateFromAlphaFunc(g.polygons,lambda mobs,t:[m.become(shape(transform(kind,t),[-4.8+3.2*j-.75,.15,0],.5,c)) for j,(m,kind,c) in enumerate(zip(mobs,kinds,[BLUE,GOLD,GREEN,PURPLE]))]))
  self.to(40)
  target=eq('1',0,.3,78,INK,w=2)
  self.act(.7,*[TransformFromCopy(label,target.copy()) for label in g.labels])
  self.show(tx('서로 다른 공간의 변환 · 동일한 행렬식',0,-2.4,25,GREEN,w=12),d=.5);self.to(45)
 def shot_04(self):
  g=comparison();g.scale(.8).move_to([0,.7,0]);self.add(g)
  self.show(self.note('방향별 크기 · 기울어짐 · 회전량은 복원할 수 없다',MUTED),d=.5);self.to(53)
  self.clear(d=.3);words=tx('정보의 생략',0,.8,49,MUTED);self.show(words,d=.5)
  self.act(1,Transform(words,tx('필요한 정보의 추출',0,.8,49,GREEN)));self.to(57)
  self.clear(d=.3);g=comparison();self.add(g)
  self.show(eq(r'A\ne B,\quad\det(A)=\det(B)=1',0,-2.4,33,GREEN,w=12),d=.5);self.to(64)
 def shot_05(self):
  timeline=tx('방정식  →  기하학  →  순열  →  소거법  →  정보',0,2.1,26,MUTED);self.add(timeline);self.to(67)
  self.show(foundation.equations(True,x=-3.7,y=.55),eq('(ad-bc)x=de-bf',3,.8,42,BLUE,w=6),eq(r'\det A\ne0',3,-.55,46,BLUE,w=6),self.note('해의 유일성을 판단하는 계수들의 관계',BLUE),d=.7);self.to(73)
 def shot_06(self):
  b=geometry.Board(np.eye(2));self.add(b)
  self.add(eq('ad-bc',-3.7,.8,65,GOLD,w=5),tx('부피와 방향',-3.7,-.45,33,GOLD,w=5))
  self.morph(b,np.array([[3,1],[1,3]]),2)
  self.show(eq(r'S=|ad-bc|',-3.7,-1.5,40,GOLD,w=5),d=.4)
  self.morph(b,np.array([[3,3],[1,1]]),1.5)
  self.show(self.note('같은 숫자가 공간의 변화를 설명한다',GOLD),d=.4);self.to(80)
 def shot_07(self):
  count=eq('27-21=6',0,1.8,59,GREEN);self.add(count)
  for k,p in enumerate(basis.PERMS):
   x=-3.7+(k%3)*3.7;y=.65-(k//3)*1.15;self.show(basis.cards(p,x,y,.48),eq('+' if basis.parity(p)>0 else '-',x+1.25,y,35,GREEN if basis.parity(p)>0 else RED,w=.5),d=.3)
  self.show(eq(basis.FORMULA,0,-1.9,36,GREEN,w=12),d=.5);self.to(87)
 def shot_08(self):
  m=shared.matrix(shared.A,0,.4);self.add(m);self.status('2')
  for k,(target,pivot,factor) in enumerate(shared.OPERATIONS):self.row_update(m,target,shared.STATES[k+1][target],.65)
  self.show(eq(r'\det A=2\times1\times1=2',0,-1.55,46,PURPLE),self.note('불변성을 이용해 계산 구조를 단순화한다',PURPLE),d=.5);self.to(94)
 def shot_09(self):
  g=concept_map();self.add(g.nodes,g.links)
  self.to(96);self.show(g.center_node,d=.7);self.to(99)
  self.act(.7,Indicate(g.nodes[0],color=BLUE),Indicate(g.links[0],color=BLUE));self.to(103)
  self.act(.7,Indicate(g.nodes[1],color=GOLD),Indicate(g.links[1],color=GOLD));self.to(106)
  self.act(.8,Indicate(g.nodes[2],color=GREEN),Indicate(g.nodes[3],color=PURPLE));self.to(110)
 def shot_10(self):
  g=extraction();self.add(g)
  self.show(eq(r'A\in\mathbb R^{n\times n}\xrightarrow{\det}d\in\mathbb R',0,-2.1,40,PURPLE,w=12),d=.5)
  dots=VGroup(*[Dot(cell.get_center(),radius=.025+.006*(k%4),color=PURPLE) for k,cell in enumerate(g.grid)])
  self.add(dots)
  self.act(2.5,LaggedStart(*[dot.animate.move_to([0,.55,0]).set_opacity(0) for dot in dots],lag_ratio=.035))
  self.act(.8,Indicate(g.operation,color=PURPLE),Indicate(g.destination,color=GREEN));self.to(118)
 def shot_11(self):
  for x,title,formula,c in [(-4.2,'다른 열의 배수 더하기',r'd\to d',GREEN),(0,'두 열 교환',r'd\to-d',RED),(4.2,'한 열을 2배',r'd\to2d',GOLD)]:self.add(tx(title,x,1.5,27,c,w=3.9),eq(formula,x,.2,55,c,w=3.9))
  self.to(123);self.clear(d=.3);self.show(eq(r'\det(A)',0,.4,100,INK,w=6),self.note('무엇이 유지되고, 무엇이 달라지는가?',PURPLE),d=.6);self.to(127)
 def shot_12(self):
  m=shared.symbol_grid(5,-4.5,.6);self.add(m,tx('행렬',-4.5,-1.4,28,MUTED,w=3))
  self.show(basis.cube(np.array([[2,1,0],[0,1,1],[0,0,1]]),[-.3,.5,0],1),tx('공간의 부피와 방향',0,-1.4,26,GOLD,w=4),Arrow([-2.8,.5,0],[-2,.5,0],color=MUTED,buff=0,tip_length=.12),d=.8)
  self.to(131)
  self.show(Arrow([1.9,.5,0],[2.8,.5,0],color=MUTED,buff=0,tip_length=.12),eq(r'\det(A)',4.2,.5,62,INK,w=4),tx('하나의 숫자',4.2,-1.4,28,GREEN,w=4),d=.8);self.to(135)
 def shot_13(self):
  central=eq(r'\det(A)',0,.2,67,INK,w=4);self.add(central)
  sources=VGroup(eq('(ad-bc)x=de-bf',-3.9,1.5,31,BLUE,w=5.7),eq('S=|ad-bc|',3.9,1.5,35,GOLD,w=5.7),eq('ad-bc',-3.9,-1.1,42,GREEN,w=5.7),eq(r'\det A=\det U',3.9,-1.1,35,PURPLE,w=5.7));self.show(sources,d=.6)
  self.act(1.5,*[TransformFromCopy(s,central.copy()) for s in sources]);self.to(139)
  self.clear(d=.35)
  self.act(.5,FadeOut(self.header),FadeOut(self.masthead))
  final=eq('ad-bc',0,.45,102,INK,w=10)
  self.show(final,d=.65)
  # End exactly with the final sentence; no extra hold or end card is appended.
  self.to(143)
