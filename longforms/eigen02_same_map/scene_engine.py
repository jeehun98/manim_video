"""Same linear map, two coordinate representations. All geometry uses A, D and P."""
import os
import numpy as np
from manim import *
VERT=os.environ.get('EIGEN_LAYOUT','longform')=='shorts'
config.frame_width=8 if VERT else 128/9
config.frame_height=128/9 if VERT else 8
config.background_color='#09121F'
BLUE='#458EFA';PURPLE='#B68AFA';TEAL='#20BCA5';ORANGE='#F0A34E';YELLOW='#F3CF75';INK='#EDF3F7';MUTED='#91A4BA';GRID='#2A3D54'
A=np.array([[2.,1.],[1.,2.]]);D=np.diag([3.,1.]);P=np.array([[1.,1.],[1.,-1.]])
BOUNDS=[0,7,15,31,43,53,64,77,89,99,106,110,115,120]
TITLES=['숫자가 다른 두 행렬','같은 숫자, 다른 출력','같은 표준 좌표계에서 비교','변환 대신, 표현의 기준을 바꾸면','두 대각선이 새로운 좌표축','벡터는 그대로, 좌표는 다르게','두 좌표계에서 각각 계산','다른 좌표 숫자, 같은 실제 결과','한 벡터만의 우연일까?','성분의 혼합이 독립적인 배율로','왜 하필 이 두 방향일까?','같은 변환을 표현하는 닮음 관계','숫자는 달라도, 변환은 같을 수 있다']
def text(s,size=27,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def fmt(v):return '('+', '.join(f'{q:g}'.replace('-', '−') for q in v)+')'
class SimilarityScene(Scene):
 index=0
 def construct(self):
  self.i=self.index;duration=BOUNDS[self.i+1]-BOUNDS[self.i];self.footer=None
  top=6.1 if VERT else 3.35
  self.add(text('고윳값과 고유벡터  /  02',16,MUTED).move_to([0,top+.48,0]),text(TITLES[self.i],30,width=7.2 if VERT else 13).move_to([0,top,0]),Line([-3.6 if VERT else -6.6,top-.45,0],[3.6 if VERT else 6.6,top-.45,0],color=GRID,stroke_width=1))
  i=self.i;cs=self.centers()
  if i==0:
   cards=[self.matrix_card(A,'A',BLUE,cs[0]),self.matrix_card(D,'D',PURPLE,cs[1])]
   self.add(*cards);self.until(1)
   self.play(Indicate(cards[0][1][0][1],color=INK),Indicate(cards[0][1][0][2],color=INK),run_time=.8)
   self.play(Indicate(cards[1][1][0][0],color=INK),Indicate(cards[1][1][0][3],color=INK),run_time=.8)
   self.note('A: 2와 1     /     D: 대각선의 3과 1')
  elif i==1:
   self.add(self.matrix_card(A,'A',BLUE,cs[0],small=True),self.matrix_card(D,'D',PURPLE,cs[1],small=True))
   for c,m,col in zip(cs,[A,D],[BLUE,PURPLE]):
    self.add(text('(1, 0)',28).move_to(c+[0,-.45,0]));self.play(FadeIn(text('↓',28,col).move_to(c+[0,-.95,0])),FadeIn(text(fmt(m@np.array([1,0])),32,col).move_to(c+[0,-1.45,0])),run_time=.5)
   self.until(3);self.note('같은 좌표 숫자 → 서로 다른 출력 숫자')
  elif i==2:
   ps=[self.panel(c,label,col) for c,label,col in zip(cs,['A · 표준 기저','D · 표준 기저'],[BLUE,PURPLE])]
   grids=[self.mesh(p,np.eye(2),.55) for p in ps]
   squares=[Polygon(*[p(q) for q in [[0,0],[1,0],[1,1],[0,1]]],color=col,fill_color=col,fill_opacity=.18,stroke_width=3) for p,col in zip(ps,[BLUE,PURPLE])]
   arrows=[[self.arrow(p,[1,0],TEAL),self.arrow(p,[0,1],ORANGE)] for p in ps]
   self.add(*grids,*squares,*[v for group in arrows for v in group]);self.until(5)
   for idx,(mat,col,target) in enumerate([(A,BLUE,10),(D,PURPLE,15)]):
    p=ps[idx]
    self.play(Transform(grids[idx],self.mesh(p,mat,.55)),Transform(squares[idx],Polygon(*[p(mat@np.array(q)) for q in [[0,0],[1,0],[1,1],[0,1]]],color=col,fill_color=col,fill_opacity=.18,stroke_width=3)),*[Transform(arrows[idx][j],self.arrow(p,mat[:,j],[TEAL,ORANGE][j])) for j in range(2)],run_time=2)
    self.until(target)
   self.note('고정된 같은 척도 · 단위 정사각형의 변형')
  elif i==3:
   p=self.world();self.add(self.axes(p),self.arrow(p,[2,1],INK),self.dot(p,[2,1]));self.note('실제 입력 벡터 x = (2, 1)');self.until(3)
   self.play(Indicate(self.mobjects[-2],color=INK),run_time=.7);self.until(6)
   self.add(text('고정: 실제 벡터',27,INK).move_to([0,3.6 if VERT else 2.2,0]));self.note('바뀌는 것: 기저 · 눈금 · 좌표 숫자')
  elif i==4:
   p=self.world();old=self.axes(p);v=self.arrow(p,[2,1],INK);self.add(old,v,self.dot(p,[2,1]));new=self.basis(p,ticks=False)
   self.play(old.animate.set_opacity(.18),Create(new),run_time=2);self.until(6)
   self.play(FadeIn(self.ticks(p)),run_time=.8);self.note('v₁ = (1, 1)   ·   v₂ = (1, −1)\n새 축의 1단위 길이 = √2')
  elif i==5:
   p=self.world();v=self.arrow(p,[2,1],INK);self.add(self.axes(p).set_opacity(.22),self.basis(p),v,self.dot(p,[2,1]));self.note('실제 벡터의 위치와 방향은 그대로');self.until(6)
   a=np.array([1.5,1.5]);b=np.array([.5,-.5]);self.play(GrowArrow(self.arrow(p,a,TEAL)),run_time=.8);self.play(GrowArrow(self.arrow(p,b,ORANGE,start=a)),Create(DashedLine(p([0,0]),p(b),color=ORANGE)),Create(DashedLine(p(b),p([2,1]),color=TEAL)),run_time=.8)
   self.add(text('표준 좌표 (2, 1)',26,BLUE).move_to([0,3.7 if VERT else 2.2,0]),text('고유좌표 (1.5, 0.5)',26,PURPLE).move_to([0,3.0 if VERT else 1.55,0]));self.note('(2, 1) = 1.5(1, 1) + 0.5(1, −1)')
  elif i==6:
   ps=[self.panel(c,label,col) for c,label,col in zip(cs,['표준좌표 숫자 · A','고유좌표 숫자 · D'],[BLUE,PURPLE])]
   self.add(*[self.axes(p,extent=5.5) for p in ps]);ins=[np.array([2.,1.]),np.array([1.5,.5])];outs=[A@ins[0],D@ins[1]]
   vs=[self.arrow(p,x,INK) for p,x in zip(ps,ins)];self.add(*vs)
   labels=[text(fmt(x),24,INK).move_to(c+[1.7,-1.15,0]) for c,x in zip(cs,ins)];self.add(*labels);self.note('左右 모두 좌표 숫자를 그린 평면'.replace('左右','양쪽'));self.until(4)
   self.play(Transform(vs[0],self.arrow(ps[0],outs[0],BLUE)),Transform(labels[0],text(fmt(outs[0]),25,BLUE).move_to(cs[0]+[1.7,-1.15,0])),run_time=1.7);self.until(8)
   self.play(Transform(vs[1],self.arrow(ps[1],outs[1],PURPLE)),Transform(labels[1],text(fmt(outs[1]),25,PURPLE).move_to(cs[1]+[1.7,-1.15,0])),run_time=1.7);self.note('(2, 1) → (5, 4)\n(1.5, 0.5) → (4.5, 0.5)')
  elif i==7:
   ps=[self.panel(c,label,col) for c,label,col in zip(cs,['표준 좌표 → 실제 공간','고유좌표 → 실제 공간'],[BLUE,PURPLE])]
   panel_chrome=VGroup(*self.mobjects[-4:])
   leftgrid=self.axes(ps[0],extent=5.5);rightgrid=self.axes(ps[1],extent=5.5);left=self.arrow(ps[0],[5,4],BLUE);right=self.arrow(ps[1],[4.5,.5],PURPLE)
   self.add(leftgrid,rightgrid,left,right);self.note('출력 좌표 (5, 4) ≠ (4.5, 0.5)');self.until(2)
   first=self.arrow(ps[1],[4.5,4.5],TEAL);second=self.arrow(ps[1],[.5,-.5],ORANGE,start=[4.5,4.5])
   self.play(Transform(rightgrid,self.mapped_axes(ps[1],P,extent=3.2)),GrowArrow(first),run_time=1.2);self.play(GrowArrow(second),Transform(right,self.arrow(ps[1],P@np.array([4.5,.5]),PURPLE)),run_time=1.1)
   self.note('4.5(1, 1) + 0.5(1, −1) = (5, 4)');self.until(5)
   # Both outputs map into the same real-space frame; no independent rotation.
   dest=self.world(scale=.52);target=self.arrow(dest,[5,4],YELLOW)
   self.play(FadeOut(panel_chrome),FadeOut(leftgrid),FadeOut(rightgrid),FadeOut(first),FadeOut(second),Transform(left,target.copy().set_color(BLUE)),Transform(right,target.copy().set_color(PURPLE)),run_time=2)
   self.add(self.axes(dest,extent=5.5).set_opacity(.35));self.remove(left,right);self.add(target);self.play(Indicate(target,color=YELLOW,scale_factor=1.03),run_time=.5);self.note('두 계산, 하나의 실제 결과')
  elif i==8:
   p=self.world(scale=1.0);self.add(self.axes(p,extent=3));self.note('좌표를 바꿔도 같은 실제 결과');self.until(4)
   xlist=[np.array([1.,0.]),np.array([0.,1.]),np.array([-1.,1.])]
   current=VGroup()
   for x in xlist:
    eig=np.linalg.solve(P,x);a=A@x;b=P@(D@eig);assert np.allclose(a,b)
    self.remove(current);current=VGroup(self.arrow(p,x,INK),self.arrow(p,a,BLUE),self.arrow(p,b,PURPLE).set_stroke(width=2));self.add(current)
    self.note(f'입력 {fmt(x)} → 실제 출력 {fmt(a)}\nA x = P D P⁻¹ x');self.play(Indicate(current[1],color=YELLOW,scale_factor=1.04),run_time=.6);self.add(self.arrow(p,a,YELLOW).set_opacity(.25));self.wait(.8)
   self.note('AP = PD   ·   어떤 입력에서도 같은 결과')
  elif i==9:
   ps=[self.panel(c,label,col) for c,label,col in zip(cs,['표준 기저 · 성분이 섞임','고유기저 · 독립적인 배율'],[BLUE,PURPLE])]
   self.add(*[self.axes(p,extent=5.5) for p in ps]);vs=[self.arrow(ps[0],[2,1],INK),self.arrow(ps[1],[1.5,.5],INK)];self.add(*vs)
   self.play(Transform(vs[0],self.arrow(ps[0],[5,4],BLUE)),Transform(vs[1],self.arrow(ps[1],[4.5,.5],PURPLE)),run_time=2)
   for c,s,col in zip(cs,['(x, y) → (2x+y, x+2y)','(a, b) → (3a, b)'],[BLUE,PURPLE]):self.add(text(s,23,col,width=5.8).move_to(c+[0,-1.55,0]))
   self.note('같은 선형변환의 두 좌표 표현')
  elif i==10:
   p=self.world(scale=.6);self.add(self.basis(p));a=self.arrow(p,[1,1],TEAL);b=self.arrow(p,[1,-1],ORANGE);self.add(a,b)
   self.play(Transform(a,self.arrow(p,[3,3],TEAL)),Indicate(b,color=ORANGE),run_time=1.5);self.note('Av₁ = 3v₁   ·   Av₂ = v₂')
  elif i==11:
   if VERT:
    self.add(self.matrix_card(A,'A · 표준 기저',BLUE,[0,2.0,0]),self.matrix_card(D,'D · 고유기저',PURPLE,[0,-1.5,0]));mid=[0,.2,0]
   else:
    self.add(self.matrix_card(A,'A · 표준 기저',BLUE,cs[0]),self.matrix_card(D,'D · 고유기저',PURPLE,cs[1]));mid=[0,.2,0]
   self.add(text('기저 변경',23,MUTED).move_to(mid));self.note('D = P⁻¹ A P\nP = [[1, 1], [1, −1]]');self.until(2);self.play(FadeIn(text('닮음 관계',31,YELLOW).move_to([0,3.8 if VERT else 2.15,0])),run_time=.6)
  else:
   p=self.world(scale=.48);self.add(self.axes(p,extent=5.5).set_opacity(.25),self.arrow(p,[5,4],YELLOW))
   self.add(text('A',40,BLUE).move_to([-2,3 if VERT else 1.7,0]),text('D',40,PURPLE).move_to([2,3 if VERT else 1.7,0]),text('같은 선형변환',31,YELLOW).move_to([0,3.9 if VERT else 2.45,0]));self.note('다른 기저, 다른 숫자\nD = P⁻¹ A P')
  self.until(duration)
 def until(self,t):
  if self.time<t:self.wait(t-self.time)
  elif self.time>t+.04:raise RuntimeError(f'scene {self.i+1} overrun {self.time}>{t}')
 def note(self,s):
  if self.footer:self.remove(self.footer)
  self.footer=text(s,21 if VERT else 23,MUTED,width=6.9 if VERT else 12.5).move_to([0,-4.25 if VERT else -2.8,0]);self.add(self.footer)
 def centers(self):return [np.array([0,2.05,0]),np.array([0,-1.8,0])] if VERT else [np.array([-3.45,.05,0]),np.array([3.45,.05,0])]
 def world(self,scale=.8):
  origin=np.array([-1.25,-.8 if VERT else -.7,0]);return lambda v:origin+scale*np.r_[np.array(v,dtype=float),0]
 def panel(self,c,label,color):
  c=np.array(c);width=6.7 if VERT else 6.1
  self.add(RoundedRectangle(width=width,height=3.55,corner_radius=.15,stroke_color=GRID,stroke_width=1,fill_color='#0D1928',fill_opacity=1).move_to(c),text(label,23,color,width=width-.4).move_to(c+[0,1.43,0]))
  origin=c+[-1.15,-.65,0];return lambda v:origin+.40*np.r_[np.array(v,dtype=float),0]
 def axes(self,p,extent=3):
  group=VGroup();lo=-.8;ymax=min(extent,4.5)
  for n in range(0,int(ymax)+1):
   group.add(Line(p([lo,n]),p([extent,n]),color=GRID,stroke_width=.8,stroke_opacity=.5),Line(p([n,lo]),p([n,ymax]),color=GRID,stroke_width=.8,stroke_opacity=.5))
  group.add(Line(p([lo,0]),p([extent,0]),color=MUTED,stroke_width=1.1),Line(p([0,lo]),p([0,ymax]),color=MUTED,stroke_width=1.1));return group
 def mapped_axes(self,p,matrix,extent=3):
  return VGroup(Line(p(matrix@np.array([-extent,0])),p(matrix@np.array([extent,0])),color=TEAL,stroke_width=1.5),Line(p(matrix@np.array([0,-extent])),p(matrix@np.array([0,extent])),color=ORANGE,stroke_width=1.5))
 def basis(self,p,ticks=True):
  g=self.mapped_axes(p,P,extent=2.4)
  g.add(self.arrow(p,[1,1],TEAL),self.arrow(p,[1,-1],ORANGE))
  if ticks:g.add(self.ticks(p))
  return g
 def ticks(self,p):
  g=VGroup()
  for v,c,label in [([1,1],TEAL,'v₁ · 1'),([1,-1],ORANGE,'v₂ · 1')]:
   q=p(v);normal=np.array([-v[1],v[0],0],dtype=float);normal=normal/np.linalg.norm(normal)*.08
   g.add(Line(q-normal,q+normal,color=c,stroke_width=2),text(label,20,c).move_to(q+[.38,.15 if v[1]>0 else -.2,0]))
  return g
 def arrow(self,p,v,c=INK,start=None):
  s=np.zeros(2) if start is None else np.array(start);v=np.array(v)
  if np.linalg.norm(v)<1e-8:return Dot(p(s),radius=.035,color=c)
  return Arrow(p(s),p(s+v),buff=0,color=c,stroke_width=4,max_tip_length_to_length_ratio=.13)
 def dot(self,p,v):return Dot(p(v),radius=.045,color=INK)
 def mesh(self,p,matrix,scale):
  # Each segment is transformed by the exact column action; fixed plotting scale.
  g=VGroup()
  for k in [-.5,0,.5,1,1.5]:
   for a,b in [([-.5,k],[1.5,k]),([k,-.5],[k,1.5])]:g.add(Line(p(matrix@np.array(a)),p(matrix@np.array(b)),color=GRID,stroke_width=1.2))
  return g
 def matrix(self,matrix,color,size=32):
  entries=VGroup(*[text(f'{v:g}'.replace('-','−'),size,color) for v in np.array(matrix).flat]).arrange_in_grid(rows=2,cols=2,buff=(.65,.32))
  box=entries.copy();h=entries.height+.3;w=entries.width+.45
  left=VGroup(Line([-.5*w,-h/2,0],[-.5*w,h/2,0],color=color),Line([-.5*w,h/2,0],[-.5*w+.12,h/2,0],color=color),Line([-.5*w,-h/2,0],[-.5*w+.12,-h/2,0],color=color))
  right=left.copy().rotate(PI).shift(RIGHT*w)
  # Brackets share the entries' center, without TeX installation.
  right=VGroup(Line([w/2,-h/2,0],[w/2,h/2,0],color=color),Line([w/2,h/2,0],[w/2-.12,h/2,0],color=color),Line([w/2,-h/2,0],[w/2-.12,-h/2,0],color=color))
  return VGroup(entries,left,right)
 def matrix_card(self,matrix,name,color,center,small=False):
  c=np.array(center);box=RoundedRectangle(width=5.7 if VERT else 5.6,height=3.3,corner_radius=.15,color=GRID,stroke_width=1,fill_color='#0D1928',fill_opacity=1).move_to(c)
  m=self.matrix(matrix,color,28 if small else 35).move_to(c+[0,.45 if small else -.15,0]);label=text(name,24,color,width=5).move_to(c+[0,1.2,0]);return VGroup(box,m,label)
