"""Exact affine geometry, area dissection, orientation, and projected 3D volume."""
import importlib.util,json
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('det_ch01_shared',R.parent/'chapter_01/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
tx,eq,fit=shared.tx,shared.eq,shared.fit
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED
I=np.eye(2);A=np.array([[3.,1.],[1.,3.]]);C=np.array([[3.,3.],[1.,1.]])
UNIT=np.array([[0,0],[1,0],[1,1],[0,1]])
def mat(values,x=-3.65,y=.85,size=42):
 m=Matrix([[str(v) for v in row] for row in values],h_buff=1.2,v_buff=.8,element_to_mobject=lambda s:MathTex(s,font_size=size)).move_to([x,y,0])
 for j,c in enumerate([BLUE,GOLD,GREEN][:len(values[0])]):m.get_columns()[j].set_color(c)
 return m
def clip(a,b,bounds):
 lo,hi=0.,1.;d=b-a
 for k,mn,mx in [(0,bounds[0],bounds[1]),(1,bounds[2],bounds[3])]:
  if abs(d[k])<1e-10:
   if not mn<=a[k]<=mx:return None
  else:
   u,v=(mn-a[k])/d[k],(mx-a[k])/d[k];lo=max(lo,min(u,v));hi=min(hi,max(u,v))
   if lo>hi:return None
 return a+lo*d,a+hi*d
class Board(VGroup):
 def __init__(self,M=I,origin=(1,-1.6,0),unit=.85,bounds=(-.3,6.25,-1.95,2.35),markers=False):
  super().__init__();self.origin=np.array(origin,dtype=float);self.unit=unit;self.bounds=bounds;self.marker_source=[]
  self.sources=[]
  for n in range(-7,9):self.sources.extend([(np.array([n,-8]),np.array([n,8])),(np.array([-8,n]),np.array([8,n]))])
  self.grid=VGroup(*[VMobject(stroke_color=MUTED,stroke_opacity=.25,stroke_width=1) for _ in self.sources]);self.shape=VMobject();self.basis=VGroup();self.markers=VGroup()
  self.axes=VGroup(Line([bounds[0],origin[1],0],[bounds[1],origin[1],0],color=MUTED,stroke_opacity=.45),Line([origin[0],bounds[2],0],[origin[0],bounds[3],0],color=MUTED,stroke_opacity=.45))
  self.ghost=Polygon(*[self.pt(p,I) for p in UNIT],color=MUTED,stroke_width=1,stroke_opacity=.6,fill_opacity=0)
  self.add(self.axes,self.grid,self.ghost,self.shape,self.basis,self.markers)
  self.update_matrix(M)
 def pt(self,p,M=None):return self.origin+self.unit*np.r_[(self.M if M is None else M)@np.asarray(p,dtype=float),0]
 def update_matrix(self,M):
  self.M=np.array(M,dtype=float)
  for line,(p,q) in zip(self.grid,self.sources):
   ends=clip(self.pt(p),self.pt(q),self.bounds)
   if ends is None:line.set_points_as_corners([self.origin,self.origin]).set_stroke(opacity=0)
   else:line.set_points_as_corners(ends).set_stroke(opacity=.25)
  verts=[self.pt(p) for p in UNIT]
  self.shape.set_points_as_corners(verts+[verts[0]]).set_stroke(PURPLE,3).set_fill(PURPLE,opacity=.18 if abs(np.linalg.det(self.M))>1e-9 else 0)
  self.basis.become(VGroup(*[Arrow(self.origin,self.pt(p),buff=0,color=c,stroke_width=4,max_tip_length_to_length_ratio=.15) for p,c in [([1,0],BLUE),([0,1],GOLD)]]))
  visible=[]
  for p,c in self.marker_source:
   pos=self.pt(p)
   if self.bounds[0]<=pos[0]<=self.bounds[1] and self.bounds[2]<=pos[1]<=self.bounds[3]:visible.append(Dot(pos,color=c,radius=.075))
  self.markers.become(VGroup(*visible))
  return self
def outline(points,c=PURPLE):return Polygon(*points,color=c,stroke_width=3,fill_color=c,fill_opacity=.15)
def numbered_square(center,reflected=False):
 o=np.array(center,dtype=float);pts=[o+np.array([(-1 if reflected else 1)*1.7*x,1.7*y,0]) for x,y in UNIT]
 poly=outline(pts,RED if reflected else GREEN)
 nums=VGroup(*[eq(str(i+1),*(p+np.array([-.16 if reflected else .16,-.24 if i<2 else .24,0]))[:2],size=25,c=INK,w=.5) for i,p in enumerate(pts)])
 arrows=VGroup(*[Arrow(p,q,buff=.25,color=RED if reflected else GREEN,stroke_width=2,max_tip_length_to_length_ratio=.15) for p,q in zip(pts,pts[1:]+pts[:1])])
 return VGroup(poly,nums,arrows),pts

class GeometryScene(shared.ChapterScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.add(tx('CHAPTER 02',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25))
  self.header=tx('행렬식의 기하학적 정체',0,2.94,31);self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def morph(self,b,target,d):
  start=b.M.copy();target=np.asarray(target,dtype=float)
  self.act(d,UpdateFromAlphaFunc(b,lambda m,t:m.update_matrix((1-t)*start+t*target)))
 def shot_01(self):
  s=shared.equations(True,x=-3.5,y=.6);m=mat([['a','b'],['c','d']],3,.6)
  # Preserve the chapter-one matrix/column idea, then return to the equations.
  self.add(s,m,eq(r'\det(A)=ad-bc',0,-1.6,47,PURPLE))
  self.to(5);self.show(tx('같은 배열, 다른 관점',0,2.05,29,PURPLE));self.to(8)
  rows=VGroup(*[SurroundingRectangle(row,color=c,buff=.15) for row,c in zip(m.get_rows(),[BLUE,GOLD])]);self.show(rows,d=.5)
  self.show(self.note('한 행 = 하나의 방정식에 대한 계수',MUTED));self.to(12)
  cols=VGroup(*[SurroundingRectangle(col,color=c,buff=.15) for col,c in zip(m.get_columns(),[BLUE,GOLD])])
  self.act(.7,ReplacementTransform(rows,cols))
  self.act(.8,Transform(s,eq(r'\mathbf v_1=(a,c),\quad\mathbf v_2=(b,d)',-3,.45,38,w=6)))
  self.to(18)
 def shot_02(self):
  b=Board();b.shape.set_fill(opacity=0);self.add(b)
  self.add(eq(r'\mathbf e_1=\binom10',-3.8,1.2,43,BLUE,w=5),eq(r'\mathbf e_2=\binom01',-3.8,-.2,43,GOLD,w=5))
  self.to(22);self.show(tx('가로 길이 1 · 세로 길이 1',-3.8,-1.4,26,MUTED,w=5));self.to(27)
  p=b.pt([3,2]);self.show(Dot(p,color=GREEN),eq('P=(3,2)',*(p+UP*.35)[:2],size=29,c=GREEN,w=2.3),d=.4)
  steps=VGroup(*[Arrow(b.pt([x,0]),b.pt([x+1,0]),buff=.04,color=BLUE,stroke_width=4) for x in range(3)],*[Arrow(b.pt([3,y]),b.pt([3,y+1]),buff=.04,color=GOLD,stroke_width=4) for y in range(2)])
  self.act(.9,LaggedStart(*[Create(x) for x in steps],lag_ratio=.15))
  self.show(self.note(r'p = 3e₁ + 2e₂',GREEN),d=.4);self.to(31)
 def shot_03(self):
  b=Board();b.marker_source=[([x,y],MUTED) for x in [0,1,2] for y in [0,1,2]];b.update_matrix(I);self.add(b)
  m=mat([['a','b'],['c','d']]);self.add(m)
  self.show(eq(r'A\mathbf e_1=(a,c)',-3.7,-.7,35,BLUE,w=5),eq(r'A\mathbf e_2=(b,d)',-3.7,-1.5,35,GOLD,w=5),d=.5)
  self.to(35);self.act(.7,Transform(m,mat([[3,1],[1,3]])))
  self.to(39);self.morph(b,A,3.5);self.to(43)
  self.show(eq(r'\mathrm{Area}_{\mathrm{before}}=1',-3.7,2.15,27,MUTED,w=5),eq(r'S=?',3.1,.25,48,PURPLE,w=2),d=.4)
  self.show(self.note('단위 정사각형 → 평행사변형',PURPLE),d=.5);self.to(48)
 def shot_04(self):
  # a=d=3, b=c=1: all components positive and ad-bc positive.
  o=np.array([-5.8,-1.8,0]);u=.94
  def pt(x,y):return o+u*np.array([x,y,0])
  O,U,V,T=pt(0,0),pt(3,1),pt(1,3),pt(4,4)
  para=outline([O,U,T,V]);question=eq('S=?',-3.85,.05,50,PURPLE,w=3);self.add(para,question)
  self.add(tx('a, b, c, d > 0  ·  ad−bc > 0',-3.8,2.35,20,MUTED,w=5.2))
  for s,p,c in [('(a,c)',U+RIGHT*.5,BLUE),('(b,d)',V+LEFT*.45,GOLD)]:self.add(eq(s,*p[:2],size=24,c=c,w=1.5))
  self.to(52)
  rect=Polygon(O,pt(4,0),T,pt(0,4),stroke_color=MUTED,stroke_width=2,fill_opacity=0)
  self.act(.6,Create(rect))
  self.show(eq('a+b',-3.92,-2.15,29,w=4),eq('c+d',-6.25,.1,29,w=1),eq('(a+b)(c+d)',2.7,1.55,41,w=6),d=.4);self.to(56)
  groups=[
   (GOLD,[[pt(0,0),pt(3,0),pt(3,1)],[pt(1,3),pt(1,4),pt(4,4)]],['ac/2','ac/2'],r'-ac'),
   (GREEN,[[pt(0,0),pt(0,3),pt(1,3)],[pt(3,1),pt(4,1),pt(4,4)]],['bd/2','bd/2'],r'-bd'),
   (RED,[[pt(0,3),pt(1,3),pt(1,4),pt(0,4)],[pt(3,0),pt(4,0),pt(4,1),pt(3,1)]],['bc','bc'],r'-2bc')]
  outside=VGroup()
  for k,(c,vertices,labels,term) in enumerate(groups):
   shapes=VGroup(*[Polygon(*verts,stroke_color=c,stroke_width=1.5,fill_color=c,fill_opacity=.25) for verts in vertices]);outside.add(shapes)
   texts=VGroup(*[eq(label,*np.mean(verts,axis=0)[:2],size=23,c=c,w=1) for label,verts in zip(labels,vertices)])
   self.show(shapes,texts,eq(term,1.4+k*1.4,.5,37,c,w=1.4),d=.5)
   self.act(.35,shapes.animate.set_fill(opacity=.07));self.to(58+k*2)
  self.to(62)
  expanded=fit(MathTex('ac','+ad','+bc','+bd','-ac','-bd','-2bc',font_size=33),6.1).move_to([2.75,-.6,0]);self.show(expanded,d=.4)
  self.to(63);self.show(*[Cross(expanded[k],stroke_color=RED,stroke_width=2) for k in [0,4,3,5]],d=.4)
  self.show(eq('S=ad-bc',2.75,-1.65,57,PURPLE,w=6),d=.5)
  self.act(.4,Transform(question,eq('S=8',-3.85,.05,50,PURPLE,w=3)));self.to(66)
 def shot_05(self):
  self.add(shared.equations(True,x=-3.5,y=1),eq('(ad-bc)x=de-bf',-3.5,-.8,37,PURPLE,w=5.7))
  b=Board(A,unit=.65,origin=(1.2,-1.3,0));b.grid.set_opacity(.1);self.add(b,eq('S=ad-bc',3.2,-1.95,40,PURPLE,w=5))
  self.show(tx('서로 다른 문제에서 등장한 동일한 식',0,2.25,28,PURPLE));self.to(71)
  self.clear();self.show(eq(r'\frac{S_{\mathrm{after}}}{S_{\mathrm{before}}}=|\det A|',0,1.3,56,GREEN),eq(r'\det\begin{pmatrix}3&1\\1&3\end{pmatrix}=9-1=8',0,-.25,48,PURPLE),self.note('원래 넓이 1 → 변환 후 넓이 8',GREEN),d=.6);self.to(78)
 def shot_06(self):
  b=Board(A);b.marker_source=[([x,y],MUTED) for x in [0,1] for y in [0,1]];b.update_matrix(A);self.add(b)
  nums=[DecimalNumber(v,num_decimal_places=2,font_size=34,color=BLUE if k%2==0 else GOLD) for k,v in enumerate(A.ravel())]
  live=MobjectMatrix([nums[:2],nums[2:]],h_buff=1.5,v_buff=.8).move_to([-3.7,.85,0])
  self.add(live,eq(r'\det A\longrightarrow0',-3.7,-.6,43,PURPLE,w=5))
  val=DecimalNumber(8,num_decimal_places=2,font_size=47,color=PURPLE).move_to([-3.7,-1.65,0]);self.add(val)
  self.to(82)
  def animate_to(target,d):
   start=b.M.copy()
   def upd(m,t):
    m.update_matrix((1-t)*start+t*target);val.set_value(max(0,float(np.linalg.det(m.M))))
    for n,v in zip(nums,m.M.ravel()):n.set_value(float(v))
   self.act(d,UpdateFromAlphaFunc(b,upd))
  animate_to(.6*C+.4*A,2.7);self.to(85)
  animate_to(C,3.8)
  self.show(self.note('이 예시: 평면 → 직선 · 넓이 0',RED),d=.4);self.to(90)
 def shot_07(self):
  self.add(mat([[3,3],[1,1]]),eq('P=(1,0)',-3.7,-.6,35,BLUE,w=5),eq('Q=(0,1)',-3.7,-1.35,35,GOLD,w=5))
  b=Board(I);b.marker_source=[([1,0],BLUE),([0,1],GOLD)];b.update_matrix(I);self.add(b)
  self.morph(b,C,3.8);self.show(eq('AP=AQ=(3,1)',3,1.9,33,RED,w=5),d=.4);self.to(95)
  self.show(self.note('P ≠ Q 인데 AP = AQ · 원래 입력을 구별할 수 없다',RED),d=.5)
  self.to(99)
 def shot_08(self):
  self.add(eq(r'A=\begin{pmatrix}3&3\\1&1\end{pmatrix}',-3.7,1.15,43,w=5),eq(r'A\mathbf x=\mathbf b',-3.7,-.05,46,PURPLE,w=5),eq(r'\det A=0',-3.7,-1.25,45,RED,w=5))
  b=Board(C);b.grid.set_opacity(.12);self.add(b)
  # The full image is a line, longer than the image of the unit square.
  im=Line(b.pt([-.2,-.2]),b.pt([1,1]),color=RED,stroke_width=5);self.add(im)
  inside=Dot(b.pt([.65,.65]),color=GREEN);outside=Dot([4.3,1.35,0],color=RED)
  self.show(inside,tx('상공간 위: 무한히 많은 해',3.2,-2.35,23,GREEN,w=5.6),d=.5)
  self.to(103)
  self.show(outside,tx('상공간 밖: 해 없음',3.5,1.85,23,RED,w=5),d=.5);self.to(107)
 def shot_09(self):
  left,lpts=numbered_square([-4.5,-.65,0]);right,rpts=numbered_square([3.8,-.65,0]);self.add(left,right)
  self.add(eq(r'\det I=1',-3.65,-1.5,40,GREEN,w=4),eq(r'F=\begin{pmatrix}-1&0\\0&1\end{pmatrix}',2.7,2.05,37,RED,w=6))
  self.to(110)
  # A reflection is applied pointwise; vertex identities are maintained.
  target,tpts=numbered_square([3.8,-.65,0],True)
  self.act(3.5,Transform(right,target));self.to(114)
  self.show(eq(r'\det F=-1',3,-1.5,42,RED,w=5),self.note('넓이는 1 그대로 · 꼭짓점의 순서는 반전',RED),d=.6);self.to(119)
 def shot_10(self):
  left,lpts=numbered_square([-4.5,-.65,0]);right,rpts=numbered_square([3.8,-.65,0],True);self.add(left,right)
  self.add(tx('반시계 방향',-3.65,1.8,31,GREEN,w=5),tx('시계 방향',3,1.8,31,RED,w=5))
  dot1=Dot(lpts[0],color=GREEN);dot2=Dot(rpts[0],color=RED);self.add(dot1,dot2)
  for k in range(4):self.act(.8,dot1.animate.move_to(lpts[(k+1)%4]),dot2.animate.move_to(rpts[(k+1)%4]))
  self.to(124);self.show(eq(r'|\det F|=1',-3.65,-1.65,42,GREEN,w=5),eq(r'\det F=-1',3,-1.65,42,RED,w=5),d=.5)
  self.show(self.note('절댓값: 넓이 배율      부호: 공간의 방향',PURPLE),d=.5);self.to(128)
 def shot_11(self):
  # Explicit orthographic projection of 3D vertices; transformation precedes projection.
  verts=np.array([[x,y,z] for x in [0,1] for y in [0,1] for z in [0,1]],dtype=float)
  proj=np.array([[1.,.55,0],[-.25,.4,1.]])
  faces=[[0,4,6,2],[0,2,3,1],[0,1,5,4],[4,5,7,6],[2,6,7,3],[1,3,7,5]]
  B=np.array([[2,1,0],[0,1,1],[0,0,1]],dtype=float)
  def cube(M,center,scale=1.3,c=PURPLE):
   points=(verts@M.T)@proj.T;points-=(verts@proj.T).mean(axis=0)
   pp=[np.r_[p,0]*scale+np.array(center) for p in points]
   return VGroup(*[Polygon(*[pp[i] for i in f],color=c,stroke_width=2,fill_color=c,fill_opacity=.06) for f in faces],*[Arrow(pp[0],pp[i],buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.15) for i,color in [(4,BLUE),(2,GOLD),(1,GREEN)]])
  old=cube(np.eye(3),[-3.7,.2,0],1.6,BLUE);new=cube(np.eye(3),[1.9,.2,0],1.3,PURPLE)
  self.add(old,new,eq(r'V=1',-3.7,-1.65,39,BLUE,w=4))
  self.to(131)
  self.show(eq(r'B=\begin{pmatrix}2&1&0\\0&1&1\\0&0&1\end{pmatrix}',0,2.15,26,w=5),d=.5)
  self.act(4.5,UpdateFromAlphaFunc(new,lambda m,t:m.become(cube((1-t)*np.eye(3)+t*B,[1.9,.2,0],1.3,PURPLE))))
  self.show(eq(r'V=|\det B|=2',2.8,-1.65,39,PURPLE,w=5),d=.5);self.to(139)
  self.clear();self.show(eq(r'2D\ \longrightarrow\ 3D\ \longrightarrow\ nD',0,1,56,PURPLE),self.note('넓이 → 부피 → n차원 부피',GREEN),d=.6);self.to(142)
 def shot_12(self):
  for x,title,formula,c in [(-4.3,'크기 변화',r'|\det A|',GREEN),(0,'차원 붕괴',r'\det A=0',RED),(4.3,'방향 반전',r'\det A<0',RED)]:
   self.add(tx(title,x,1.4,31,c,w=3.8),eq(formula,x,.25,41,c,w=3.8))
  self.show(eq(r'\det A',0,-1.25,65,PURPLE),d=.5);self.to(147)
  self.clear();self.show(eq('ad-bc',0,1.6,62,PURPLE),tx('방정식',-3.4,.45,31,BLUE,w=5),tx('기하학',3.4,.45,31,GOLD,w=5),tx('해를 유일하게 결정할 수 있는가?',-3.4,-.5,25,BLUE,w=6),tx('변환이 입력을 구별할 수 있는가?',3.4,-.5,25,GOLD,w=6),self.note('0일 때: 공간의 차원과 입력을 구별하는 정보가 사라진다',RED),d=.7);self.to(154)
 def shot_13(self):
  m=mat([['a','b'],['c','d']],-3.8,.8);self.add(m)
  pts=[np.array([.6,-1,0]),np.array([3.8,-.1,0]),np.array([4.9,1.7,0]),np.array([1.7,.8,0])]
  para=outline(pts);self.add(para)
  path=VGroup(*[Arrow(p,q,buff=.15,color=GREEN,stroke_width=2,max_tip_length_to_length_ratio=.18) for p,q in zip(pts,pts[1:]+pts[:1])]);self.add(path)
  value=eq('ad-bc',-3.8,-1.25,45,PURPLE,w=5);self.add(value)
  self.to(156)
  target=mat([['b','a'],['d','c']],-3.8,.8);target.get_columns()[0].set_color(GOLD);target.get_columns()[1].set_color(BLUE)
  self.act(1.2,*[Transform(m.get_entries()[k],target.get_entries()[k]) for k in range(4)])
  rpts=[pts[0],pts[3],pts[2],pts[1]]
  rev=VGroup(*[Arrow(p,q,buff=.15,color=RED,stroke_width=2,max_tip_length_to_length_ratio=.18) for p,q in zip(rpts,rpts[1:]+rpts[:1])])
  self.act(.5,Transform(path,rev),Transform(value,eq('bc-ad=-(ad-bc)',-3.8,-1.25,38,RED,w=5.5)))
  self.show(self.note('같은 평행사변형 · 반대 방향 · 반대 부호',PURPLE),d=.4);self.to(160)
  cards=VGroup(*[VGroup(RoundedRectangle(width=.7,height=.65,corner_radius=.08,color=c,fill_color=c,fill_opacity=.13),eq(s,size=29,c=c,w=.5)) for s,c in [('2',GOLD),('1',BLUE)]]).arrange(RIGHT,buff=.16).move_to([-3.8,2.2,0])
  self.show(cards,tx('순열: 선택한 열의 순서',3,.4,28,PURPLE,w=5),d=.5);self.to(164)
