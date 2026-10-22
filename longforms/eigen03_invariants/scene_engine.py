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
BOUNDS=[0,9,18,24,33,44,53,60,69,75,87,96,107,114,121]
TITLES=['반복 변환에서 드러나는 고윳값','같은 변환, 달라지는 숫자','좌표계가 달라져도 남는 것은?','두 고유방향의 배율','좌표계가 바뀌면 행렬도 바뀐다','변하지 않는 고윳값 3과 1','좌표계를 바꿔도 유지되는 성질','대각합과 행렬식','더하면 4, 곱하면 3','변하는 표현, 고정된 불변량','값이 같으면 같은 변환일까?','같은 불변량, 다른 공간 변형','불변량과 변환 전체는 다르다','표현을 넘어 구조를 본다는 것']
YELLOW='#F4CF63'
BASES=[np.eye(2),np.array([[1.,-1.],[1.,1.]]),np.array([[1.,1.],[0.,1.]])]
def text(s,size=27,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def fmt(v):return '('+', '.join(f'{q:g}'.replace('-', '−') for q in v)+')'
class InvariantScene(Scene):
 index=0
 def construct(self):
  self.i=self.index;duration=BOUNDS[self.i+1]-BOUNDS[self.i];self.footer=None
  top=6.1 if VERT else 3.35
  self.add(text('고윳값과 고유벡터  /  03',16,MUTED).move_to([0,top+.48,0]),text(TITLES[self.i],30,width=7.2 if VERT else 13).move_to([0,top,0]),Line([-3.6 if VERT else -6.6,top-.45,0],[3.6 if VERT else 6.6,top-.45,0],color=GRID,stroke_width=1))
  i=self.i;cs=self.centers()
  if i==0:
   p=self.world() if VERT else (lambda v:np.array([-.8,.1,0])+.6*np.r_[np.array(v,dtype=float),0]);self.add(self.axes(p));v=self.arrow(p,[2.4,0],BLUE);self.add(v)
   for k in [1,2,3,5]:
    x=np.linalg.matrix_power(A,k)@np.array([1.,0.]);x=x/np.linalg.norm(x)*2.4;self.play(Transform(v,self.arrow(p,x,BLUE)),run_time=.8)
   self.until(5);self.play(Create(self.mapped_axes(p,P,extent=2.3)),run_time=.6);self.invariants();self.note('길이를 맞춰 방향만 관찰')
  elif i==1:
   p=self.world(scale=.7);axes=self.axes(p);v=self.arrow(p,[2,1],INK);self.add(axes,v)
   m=self.matrix(A,BLUE).move_to([0,3.4,0] if VERT else [-3.7,1.4,0]);label=text('좌표 (2, 1)',26,BLUE).move_to([0,2.2,0] if VERT else [-3.7,.1,0]);self.add(m,label)
   self.play(axes.animate.set_opacity(.2),Create(self.basis(p)),Transform(m,self.matrix(D,PURPLE).move_to(m)),run_time=2.4);self.until(5)
   self.play(Transform(label,text('좌표 (1.5, 0.5)',26,PURPLE).move_to(label)),run_time=.7);self.note('실제 벡터 고정 · 좌표와 행렬 표현만 변경')
  elif i==2:
   m=self.matrix(A,BLUE,42).move_to([0,.5,0]);self.add(m)
   q=text('좌표계가 바뀌어도\n변하지 않는 것은?',35,YELLOW,width=7 if VERT else 12).move_to([0,3.4 if VERT else 2,0]);self.add(q);self.until(4);self.play(Indicate(m,color=PURPLE),run_time=.7);self.note('행렬의 표현과 변환의 성질을 구분해 보겠습니다')
  elif i==3:
   p=self.world(scale=.6) if VERT else (lambda v:np.array([-.8,.1,0])+.5*np.r_[np.array(v,dtype=float),0]);self.add(self.basis(p));v=self.arrow(p,[1,1],TEAL);w=self.arrow(p,[1,-1],ORANGE);self.add(v,w)
   self.play(Transform(v,self.arrow(p,[3,3],TEAL)),Indicate(w,color=ORANGE),run_time=2);self.invariants();self.note('Av₁ = 3v₁   ·   Av₂ = v₂')
  elif i==4:
   tracker=self.live_basis(0);self.note('현재 기저 P에 대한 표현: P⁻¹ A P');self.until(3)
   self.play(tracker.animate.set_value(1),run_time=4.5,rate_func=smooth);self.until(8);self.play(tracker.animate.set_value(2),run_time=2.5,rate_func=smooth)
  elif i==5:
   tracker=self.live_basis(2);self.invariants();self.note('행렬 원소는 변해도 고윳값은 그대로')
   self.play(tracker.animate.set_value(1),run_time=2.5);self.until(3)
   p=self.live_point;v=self.arrow(p,[1,1],TEAL);w=self.arrow(p,[1,-1],ORANGE);self.add(v,w)
   self.play(Transform(v,self.arrow(p,[3,3],TEAL)),Indicate(w,color=ORANGE),tracker.animate.set_value(0),run_time=2.5)
   self.note('고유벡터의 좌표는 변해도 실제 배율은 같다')
  elif i==6:
   self.add(text('불변량',43,YELLOW).move_to([0,2.8 if VERT else 1.9,0]),text('Invariant',22,MUTED).move_to([0,2.05 if VERT else 1.25,0]))
   self.invariants();self.note('좌표계를 바꿔도 유지되는 성질');self.until(4)
   for c,s in zip(cs,['대각합  ?','행렬식  ?']):
    q=np.array([0,.8 if s.startswith('대각') else -.8,0]) if VERT else c+[0,-.25,0]
    self.add(RoundedRectangle(width=5.6 if VERT else 5.5,height=1,corner_radius=.12,color=GRID,stroke_width=1).move_to(q),text(s,28,MUTED).move_to(q))
  elif i==7:
   card=self.matrix_card(A,'대각 원소를 더하면',BLUE,cs[0]);self.add(card)
   self.play(Indicate(card[1][0][0],color=YELLOW),Indicate(card[1][0][3],color=YELLOW),run_time=.8)
   self.add(text('대각합 = 2 + 2 = 4',26,YELLOW).move_to(cs[0]+[0,-1.18,0]));self.until(2.5)
   p=self.panel(cs[1],'부호 포함 면적 배율',PURPLE)
   p=lambda v:cs[1]+[-1.,-.65,0]+.55*np.r_[np.array(v,dtype=float),0]
   poly=self.square(p,np.eye(2),PURPLE);self.add(poly.copy().set_opacity(.15),poly);self.play(Transform(poly,self.square(p,A,PURPLE)),run_time=2)
   self.add(text('면적 1 → 3',26,YELLOW).move_to(cs[1]+[0,-1.25,0]));self.until(6);self.note('대각합 4     ·     행렬식 2×2 − 1×1 = 3')
  elif i==8:
   numbers=text('3       1',58,YELLOW).move_to([0,2.2 if VERT else 1.7,0]);self.add(numbers);self.until(1)
   add=text('3 + 1 = 4',40,YELLOW).move_to([0,.8 if VERT else .45,0]);self.play(FadeIn(add),run_time=.6)
   self.add(text('대각합',23,MUTED).next_to(add,DOWN,buff=.2));self.until(3)
   mul=text('3 × 1 = 3',40,YELLOW).move_to([0,-1.2 if VERT else -1.1,0]);self.play(FadeIn(mul),run_time=.6);self.add(text('행렬식',23,MUTED).next_to(mul,DOWN,buff=.2));self.until(5)
   self.play(Indicate(add,color=YELLOW),Indicate(mul,color=YELLOW),run_time=.6)
  elif i==9:
   tracker=self.live_basis(0);self.invariants(all_values=True)
   self.note('tr(A) = Σ λᵢ    ·    det(A) = Π λᵢ\n정사각행렬 · 복소 고윳값 포함 · 중복 횟수 반영')
   self.play(tracker.animate.set_value(1),run_time=3.5);self.play(tracker.animate.set_value(2),run_time=3.5);self.until(8);self.play(tracker.animate.set_value(0),run_time=3.5)
  elif i==10:
   self.add(text('고윳값 · 대각합 · 행렬식이 같다면?',28,YELLOW,width=7 if VERT else 12).move_to([0,4.3 if VERT else 2.3,0]));self.until(3)
   self.add(self.matrix_card(np.eye(2),'항등행렬 I',BLUE,cs[0]),self.matrix_card(np.array([[1,1],[0,1]]),'전단행렬 B',PURPLE,cs[1]));self.note('이 값들이 같다고 닮음 관계가 보장될까?')
  elif i==11:
   ps=[self.panel(c,label,col) for c,label,col in zip(cs,['항등행렬 I','전단행렬 B'],[BLUE,PURPLE])]
   # Match the physical scale in the two panels; only B shears the square.
   ps=[(lambda v,c=c:np.array(c)+[-.9,-.45,0]+.8*np.r_[np.array(v,dtype=float),0]) for c in cs]
   mats=[np.eye(2),np.array([[1.,1.],[0.,1.]])];grids=[self.mesh(p,np.eye(2),1) for p in ps];polys=[self.square(p,np.eye(2),c) for p,c in zip(ps,[BLUE,PURPLE])];self.add(*grids,*polys);self.until(3)
   self.play(Indicate(polys[0],color=BLUE),Transform(grids[1],self.mesh(ps[1],mats[1],1)),Transform(polys[1],self.square(ps[1],mats[1],PURPLE)),run_time=2.5);self.until(6)
   for c in cs:self.add(text('λ: 1, 1   ·   tr: 2   ·   det: 1',21,YELLOW,width=5.6).move_to(c+[0,-1.3,0]))
   self.until(8);self.note('P⁻¹ I P = I ≠ B\n항등행렬은 어떤 기저에서도 항등행렬')
  elif i==12:
   labels=[('좌표계를 바꿔도\n유지되는 성질',YELLOW),('변환 전체를\n결정하는 정보',PURPLE)]
   for c,(s,col) in zip(cs,labels):self.add(RoundedRectangle(width=5.7,height=2.6,corner_radius=.15,color=GRID,stroke_width=1).move_to(c),text(s,30,col,width=5.2).move_to(c))
   self.note('불변량이 같아도 닮음 관계는 아닐 수 있다')
  else:
   self.add(self.matrix(A,BLUE,34).move_to([-2.0,1.8,0] if VERT else [-3.,.3,0]),self.matrix(D,PURPLE,34).move_to([2.0,1.8,0] if VERT else [3.,.3,0]),text('고윳값 3, 1',44,YELLOW).move_to([0,0 if VERT else -1.25,0]))
   self.add(text('표현은 달라져도\n보존되는 성질은 존재한다',31,INK,width=7 if VERT else 12).move_to([0,3.8 if VERT else 2.05,0]));self.note('불변량 몇 개가 변환의 모든 정보를 담지는 않는다')
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
 def invariants(self,all_values=False):
  s='고윳값 3, 1' if not all_values else '고윳값 3, 1   ·   대각합 4   ·   행렬식 3'
  loc=[0,-3.1 if VERT else -1.9,0]
  self.add(RoundedRectangle(width=6.8 if VERT else 11.8,height=.75,corner_radius=.12,color=YELLOW,stroke_width=1,fill_color='#24221B',fill_opacity=.6).move_to(loc),text(s,24 if VERT else 28,YELLOW,width=6.4 if VERT else 11.3).move_to(loc))
 def square(self,p,mat,color):
  return Polygon(*[p(mat@np.array(v)) for v in [[0,0],[1,0],[1,1],[0,1]]],color=color,fill_color=color,fill_opacity=.18,stroke_width=3)
 def basis_at(self,t):
  t=float(np.clip(t,0,2));i=min(int(t),1);f=t-i;return BASES[i]*(1-f)+BASES[i+1]*f
 def live_basis(self,initial=0):
  tracker=ValueTracker(initial);self.add(tracker)
  center=np.array([0,3.5,0]) if VERT else np.array([-3.8,.8,0])
  self.add(text('현재 행렬 · 소수 첫째 자리 표시',20,PURPLE).move_to(center+[0,1.1,0]))
  entries=VGroup(*[text('0',31,PURPLE).move_to(center+[x,y,0]) for y in [.35,-.35] for x in [-.65,.65]])
  brackets=VGroup(Line(center+[-1.35,-.7,0],center+[-1.35,.7,0],color=PURPLE),Line(center+[1.35,-.7,0],center+[1.35,.7,0],color=PURPLE))
  for x in [-1.35,1.35]:
   for y in [-.7,.7]:brackets.add(Line(center+[x,y,0],center+[x-np.sign(x)*.15,y,0],color=PURPLE))
  self.add(entries,brackets)
  origin=np.array([-1.1,-.6,0]) if VERT else np.array([2.4,.1,0]);scale=.65 if VERT else .5;point=lambda v:origin+scale*np.r_[np.array(v,dtype=float),0];self.live_point=point
  # Matrix and coordinate grid use precisely the same continuously varying basis.
  segments=[]
  for n in [-1.5,-.75,0,.75,1.5]:segments.extend([([n,-1.5],[n,1.5]),([-1.5,n],[1.5,n])])
  lines=VGroup(*[Line(point(a),point(b),color=GRID,stroke_width=1.3) for a,b in segments]);self.add(lines)
  basis_arrows=VGroup(self.arrow(point,[1,0],PURPLE),self.arrow(point,[0,1],PURPLE));self.add(basis_arrows)
  coord_pos=np.array([0,1.9,0]) if VERT else np.array([3.4,1.9,0])
  coords=text('',19,TEAL).move_to(coord_pos);self.add(coords)
  cache={};previous=[None]*4;coord_previous=[None]
  def update(_):
   b=self.basis_at(tracker.get_value());m=np.linalg.solve(b,A@b)
   for n,val in enumerate(m.flat):
    val=round(float(val),1);val=0 if abs(val)<.05 else val;key=f'{val:g}'.replace('-','−')
    if key!=previous[n]:
     if key not in cache:cache[key]=text(key,31,PURPLE)
     pos=entries[n].get_center();entries[n].become(cache[key].copy().move_to(pos));previous[n]=key
   vcoords=np.linalg.solve(b,np.array([1.,1.]));ck='v'+fmt(np.round(vcoords,1))
   if ck!=coord_previous[0]:
    if ck not in cache:cache[ck]=text('[v₁] = '+fmt(np.round(vcoords,1)),21,TEAL)
    coords.become(cache[ck].copy().move_to(coord_pos));coord_previous[0]=ck
   for line,(a,c) in zip(lines,segments):line.put_start_and_end_on(point(b@np.array(a)),point(b@np.array(c)))
   for j in range(2):basis_arrows[j].become(self.arrow(point,b[:,j],PURPLE))
  tracker.add_updater(update);update(tracker)
  self.add(self.arrow(point,[1,1],TEAL).set_opacity(.5),self.arrow(point,[1,-1],ORANGE).set_opacity(.5))
  return tracker
