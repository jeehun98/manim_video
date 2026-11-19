"""117-second determinant geometry with one exact affine transformation board."""
import json,sys
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
UNIT=np.array([[0,0],[1,0],[1,1],[0,1]],dtype=float)
I=np.eye(2);COLLAPSE=np.array([[1.,1.],[0,0]])
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=44,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def matrix_tex(s,y=3.75):
 # Numeric matrix is maintained by add_board and sync, so it matches every intermediate frame.
 return VGroup()
def clip_segment(a,b,bounds=(-3.6,3.6,-2.55,2.75)):
 d=b-a;lo=0.;hi=1.
 for k,mn,mx in [(0,bounds[0],bounds[1]),(1,bounds[2],bounds[3])]:
  if abs(d[k])<1e-12:
   if a[k]<mn or a[k]>mx:return None
  else:
   u,v=(mn-a[k])/d[k],(mx-a[k])/d[k];lo=max(lo,min(u,v));hi=min(hi,max(u,v))
   if lo>hi:return None
 return a+lo*d,a+hi*d
class TransformBoard(VGroup):
 def __init__(self,A=None,zoom=1,ghost=True):
  super().__init__();self.A=I.copy();self.zoom=zoom;self.origin=np.array([-1.5,-.65,0.]);self.unit=1.6
  frame=Rectangle(width=7.2,height=5.3,stroke_color=MUTED,stroke_opacity=.12,stroke_width=1).move_to([0,.1,0])
  axes=VGroup(Line([-3.6,-.65,0],[3.6,-.65,0],color=MUTED,stroke_opacity=.45,stroke_width=1.5),Line([-1.5,-2.55,0],[-1.5,2.75,0],color=MUTED,stroke_opacity=.45,stroke_width=1.5))
  self.source_segments=[]
  for n in range(-4,5):self.source_segments.extend([(np.array([n,-4.]),np.array([n,4.])),(np.array([-4.,n]),np.array([4.,n]))])
  self.lattice=VGroup(*[VMobject(stroke_color=MUTED,stroke_width=1,stroke_opacity=.35) for _ in self.source_segments])
  self.shape=VMobject(stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.17)
  self.basis=VGroup();self.labels=VGroup();self.markers=VGroup();self.marker_source=[];self.orientation=False
  self.add(frame,axes,self.lattice)
  if ghost:
   outline=Polygon(*[self.point(v,I,1) for v in UNIT],stroke_color=INK,stroke_width=1,stroke_opacity=.22,fill_opacity=0);self.add(outline)
  self.add(self.shape,self.basis,self.markers,self.labels,Dot(self.origin,radius=.035,color=INK))
  self.set_matrix(I if A is None else A,zoom)
 def point(self,p,A=None,zoom=None):
  A=self.A if A is None else A;zoom=self.zoom if zoom is None else zoom
  return self.origin+np.r_[A@np.asarray(p),0]*self.unit*zoom
 def set_matrix(self,A,zoom=1):
  self.A=np.asarray(A,dtype=float).copy();self.zoom=zoom;self.det=float(np.linalg.det(self.A))
  for line,(p,q) in zip(self.lattice,self.source_segments):
   ends=clip_segment(self.point(p),self.point(q))
   if ends is None:line.set_points_as_corners([self.origin,self.origin]).set_opacity(0)
   else:line.set_points_as_corners(ends).set_stroke(opacity=.35)
  pts=[self.point(v) for v in UNIT];self.shape.set_points_as_corners(pts+[pts[0]]).set_fill(opacity=.17 if abs(self.det)>1e-9 else 0)
  arrows=[]
  for v,c in [([1,0],GOLD),([0,1],GREEN)]:
   end=self.point(v)
   arrows.append(Arrow(self.origin,end,buff=0,color=c,stroke_width=3,max_tip_length_to_length_ratio=.13) if np.linalg.norm(end-self.origin)>.002 else Dot(self.origin,radius=.02,color=c))
  self.basis.become(VGroup(*arrows))
  self.markers.become(VGroup(*[Dot(self.point(p),radius=.07,color=c) for p,c in self.marker_source]))
  if self.orientation:
   labels=[]
   for i,pt in enumerate(pts):labels.append(eq(str(i+1),size=25,color=RED,width=.45).move_to(pt+np.array([.14,.17 if i>=2 else -.2,0])))
   for a,b in zip(pts,pts[1:]+pts[:1]):
    if np.linalg.norm(b-a)>.05:labels.append(Arrow(a,b,buff=.12,color=RED,stroke_width=2,max_tip_length_to_length_ratio=.16))
   self.labels.become(VGroup(*labels))
  return self
class DeterminantScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel];self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*6.1)
  self.header=VGroup(txt('LINEAR ALGEBRA  /  MATRIX TRANSFORMATION',7.2,16,MUTED),RoundedRectangle(width=7.5,height=.95,corner_radius=.17,stroke_color=BLUE,stroke_opacity=.25,fill_color=BLUE,fill_opacity=.04).move_to(UP*5.05),eq(r'\det(A)=',5.05,39,BLUE,x=-.8,width=3.5))
  self.det_value=DecimalNumber(1,num_decimal_places=2,font_size=42,color=BLUE).move_to([1.8,5.05,0]);self.header.add(self.det_value);self.header.set_z_index(25);self.add(self.header)
  if self.shot in [5,7]:
   self.det_value.set_opacity(0);self.header.add(eq(r'ad-bc',5.05,33,BLUE,x=1.8,width=3))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.header]
  obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def add_board(self,A=None,zoom=1):
  board=TransformBoard(A,zoom);self.add(board)
  self.matrix_entries=[DecimalNumber(float(v),num_decimal_places=2,font_size=26,color=BLUE) for v in board.A.ravel()]
  live=MobjectMatrix([self.matrix_entries[:2],self.matrix_entries[2:]],h_buff=1.45,v_buff=.5,bracket_h_buff=.15,bracket_v_buff=.13).move_to(UP*3.75)
  self.add(live,eq('A=',3.75,34,BLUE,x=live.get_left()[0]-.65,width=1))
  self.area_value=DecimalNumber(abs(board.det),num_decimal_places=2,font_size=32,color=BLUE).move_to([1.85,-3.3,0]);self.add(txt('넓이 배율 |det A| =',-3.3,28,BLUE,x=-.8,width=4.5),self.area_value);self.sync(board);return board
 def sync(self,b):
  value=0 if abs(b.det)<1e-9 else b.det
  self.det_value.set_value(value).set_color(RED if value<0 else PURPLE if value==0 else BLUE)
  if hasattr(self,'area_value'):self.area_value.set_value(abs(value))
  if hasattr(self,'matrix_entries'):
   for number,v in zip(self.matrix_entries,b.A.ravel()):number.set_value(0 if abs(v)<1e-9 else float(v))
 def morph(self,board,target,seconds=2,zoom=None):
  start=board.A.copy();z0=board.zoom;z1=z0 if zoom is None else zoom
  def update(m,a):m.set_matrix((1-a)*start+a*np.asarray(target),(1-a)*z0+a*z1);self.sync(m)
  self.play(UpdateFromAlphaFunc(board,update),run_time=seconds,rate_func=linear)
class Shot01(DeterminantScene):
 shot=0
 def s01(self):
  self.det_value.set_opacity(0);symbol=eq(r'ad-bc',5.05,36,BLUE,x=1.8,width=3);self.header.add(symbol)
  self.show(eq(r'A=\begin{pmatrix}a&b\\c&d\end{pmatrix}',2,57,BLUE),eq(r'\det(A)=ad-bc',-.3,54),txt('네 원소로 계산하는 하나의 숫자',-2.5,32));self.to(4)
  self.clear_body();b=self.add_board();b.shape.set_opacity(0);self.show(matrix_tex(r'\begin{pmatrix}1&0\\0&1\end{pmatrix}'),txt('두 열 → 변환된 두 기저벡터',-4.3,27,MUTED));self.to(8)
  self.header.remove(symbol);self.remove(symbol);self.det_value.set_opacity(1);b.set_matrix(I);b.shape.set_stroke(opacity=1);self.sync(b);self.show(eq(r'\mathrm{Area}=1',.15,26,BLUE,x=-.7,width=1.7));self.to(12)
class Shot02(DeterminantScene):
 shot=1
 def s02(self):
  b=self.add_board();self.add(matrix_tex(r'\begin{pmatrix}2&1\\0&1\end{pmatrix}'));self.morph(b,[[2,1],[0,1]],6);self.to(19)
  note=txt('넓이의 배율 = 행렬식의 절댓값',-4.3,30,BLUE);self.show(note);self.to(23)
  self.play(Circumscribe(b.shape,color=BLUE),run_time=.6);self.to(25)
  self.clear_body();b=self.add_board([[2,1],[0,1]]);self.add(matrix_tex(r'\begin{pmatrix}0.5&0\\0&1\end{pmatrix}'));self.morph(b,[[.5,0],[0,1]],2.4);self.show(txt('넓이 2배 → 넓이 절반',-4.3,29,BLUE),run_time=.3);self.to(29)
class Shot03(DeterminantScene):
 shot=2
 def s03(self):
  b=self.add_board();self.add(matrix_tex(r'\begin{pmatrix}1&t\\0&1-t\end{pmatrix}'));question=txt('행렬식이 0이 된다면?',-4.3,35,PURPLE);self.show(question);self.to(33)
  self.morph(b,[[1,.45],[0,.55]],3.5);self.to(37);self.morph(b,COLLAPSE,4.5);self.to(42)
  self.show(txt('넓이 0',1.1,42,PURPLE));self.to(44)
  self.play(Transform(question,txt('2D → 1D · 차원의 붕괴',-4.3,31,PURPLE)),run_time=.4);self.to(48)
  self.show(txt('다른 특이행렬에서는 한 점으로 붕괴할 수도 있다',-2.75,22,MUTED));self.to(51)
class Shot04(DeterminantScene):
 shot=3
 def s04(self):
  b=self.add_board();b.marker_source=[([0,1],RED),([1,0],GOLD),([2,-1],PURPLE)];b.set_matrix(I)
  reminder=txt('같은 붕괴를 서로 다른 점의 관점에서',-4.3,26,MUTED);self.add(reminder)
  self.morph(b,COLLAPSE,3)
  self.show(eq(r'(0,1),(1,0),(2,-1)\ \mapsto\ (1,0)',1.6,35,PURPLE),txt('어느 원래 점이었는지 하나로 정할 수 없다',-2.8,28));self.to(57)
  self.play(Transform(reminder,txt('역행렬 없음 · 유일한 복원 불가능',-4.3,30,RED)),run_time=.6);self.to(62)
class Shot05(DeterminantScene):
 shot=4
 def s05(self):
  self.det_value.set_value(-1).set_color(RED);self.show(eq(r'\det(A)=-1',2.3,64,RED));self.to(64)
  self.show(txt('넓이도 −1이라는 뜻일까?',.1,41),txt('넓이는 음수가 될 수 없다',-2.2,32,BLUE));self.to(69)
  self.clear_body();b=self.add_board();self.add(matrix_tex(r'\begin{pmatrix}-1&0\\0&1\end{pmatrix}'));self.morph(b,[[-1,0],[0,1]],2);self.to(72)
  self.show(txt('좌우 반사 전후의 넓이는 모두 1',-4.3,29,BLUE));self.to(74)
  self.clear_body();b=self.add_board();b.orientation=True;b.set_matrix(I);self.add(matrix_tex(r'\begin{pmatrix}-1&0\\0&1\end{pmatrix}'));orientation_note=txt('번호 순서 1 → 2 → 3 → 4',-4.3,28,RED);self.show(orientation_note,run_time=.3)
  self.to(76);self.morph(b,[[-1,0],[0,1]],2);self.show(txt('반시계 방향 → 시계 방향',1.7,35,RED),run_time=.4);self.to(80)
  self.play(Transform(orientation_note,eq(r'|\det(A)|=1,\quad\det(A)=-1',-4.3,32,RED)),run_time=.6);self.to(85)
class Shot06(DeterminantScene):
 shot=5
 def s06(self):
  self.show(txt('절댓값',3.4,38,BLUE),txt('넓이의 배율',2.5,30),eq(r'|\det A|',1.55,45,BLUE),txt('부호',.2,38,RED),txt('방향의 보존 / 반전',-.75,30));self.to(91)
  self.show(txt('0 여부',-2.15,38,PURPLE),txt('더 낮은 차원으로 붕괴',-3.2,30),eq(r'\det A=0',-4.3,38,PURPLE));self.to(95)
class Shot07(DeterminantScene):
 shot=6
 def s07(self):
  b=self.add_board();self.matrix_entries[3].num_decimal_places=4;self.matrix_entries[3].set_value(1);self.matrix_entries[3].font_size=21;self.add(matrix_tex(r'\begin{pmatrix}s&0\\0&1/s\end{pmatrix}'));question=txt('det A = 1이면 모양도 같을까?',-4.3,30,GREEN);self.show(question);self.to(98)
  def update(m,a):
   s=100**a;z=min(1.,3.1/s);m.set_matrix([[s,0],[0,1/s]],z);self.sync(m)
  self.play(Transform(question,txt('균일 줌아웃 · 원래 좌표의 넓이는 계속 1',-4.3,27,GREEN)),run_time=.3)
  self.play(UpdateFromAlphaFunc(b,update),run_time=4,rate_func=linear);self.show(txt('가로 100 · 세로 0.01 · 선 두께는 실제 높이 아님',-2.75,23,MUTED),run_time=.3);self.to(103)
  self.clear_body();self.det_value.set_value(1).set_color(BLUE)
  left=Square(side_length=1.6,color=BLUE,fill_color=BLUE,fill_opacity=.17).move_to([-2,1.4,0])
  right=Rectangle(width=3,height=.0003,color=BLUE,fill_color=BLUE,fill_opacity=.17,stroke_width=2).move_to([1.8,1.4,0])
  self.show(left,right,eq(r'1\times1',2.9,33,BLUE,x=-2,width=3.4),eq(r'100\times0.01',2.9,33,BLUE,x=1.8,width=3.4),eq(r'\mathrm{Area}=1',-.2,34,BLUE,x=-2,width=3.5),eq(r'\mathrm{Area}=1',-.2,34,BLUE,x=1.8,width=3.5),txt('같은 넓이 ≠ 같은 모양',-1.9,40,GREEN),txt('표시 배율은 서로 다름 · 치수는 변환 좌표 기준',-3.35,24,MUTED),txt('매우 얇은 높이는 윤곽선으로 표시',-4.3,24,MUTED));self.to(109)
class Shot08(DeterminantScene):
 shot=7
 def s08(self):
  matrices=[[[2,1],[0,1]],COLLAPSE,[[-1,0],[0,1]],[[5,0],[0,.2]]]
  groups=VGroup()
  for A,x,y,title in zip(matrices,[-1.9,1.9,-1.9,1.9],[2,2,-.8,-.8],['넓이 배율','차원 붕괴','방향 반전','모양은 달라도 넓이 1']):
   b=TransformBoard(A,zoom=.6,ghost=False).scale(.43).move_to([x,y,0]);groups.add(b,txt(title,y-1.4,22,BLUE,x=x,width=3.4))
  self.show(groups);self.to(113)
  self.clear_body();self.show(eq(r'\boxed{\det(A)}',2.3,77,BLUE),txt('크기 변화와 방향의 반전을',.2,38),txt('하나의 숫자로 압축한다',-1.3,38,GREEN),txt('공간의 모든 모양 정보를 담는 값은 아니다',-3.5,27,MUTED));self.to(117)
