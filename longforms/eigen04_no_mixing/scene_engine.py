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
YELLOW='#F4CF63'
BOUNDS=[0,8,18,27,35,45,52,62,75,86,93,98,101,104,110,115]
TITLES=['좌표 성분의 섞임을 없앨 수 있을까?','두 입력이 두 출력에 영향을 준다','좌표축을 선택할 자유','아무 기저에서나 사라지지는 않는다','비대각 원소가 뜻하는 것','다른 축 성분을 만들지 않는 방향','첫 축의 출력이 자기 축에 남으면','독립적인 두 고유축을 선택하면','각 성분의 배율만 남는다','고유기저로 표현하는 대각화','첫 단계: 고유좌표로 표현','두 번째 단계: 고윳값을 곱하기','세 번째 단계: 원래 좌표로 복원','세 단계가 하나의 대각화 공식으로','성분이 섞이지 않는 좌표계']
S=np.array([[1.,1.],[0.,1.]])
T=np.array([[1.,0.],[1.,1.]])
R=np.array([[1.,0.],[.2,-1.]])
H=np.array([[1.,0.],[1.,-1.]])
BASES=[R,H,P]
def text(s,size=27,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def fmt(v):return '('+', '.join(f'{q:g}'.replace('-', '−') for q in v)+')'
class DiagonalScene(Scene):
 index=0
 def construct(self):
  self.i=self.index;duration=BOUNDS[self.i+1]-BOUNDS[self.i];self.footer=None
  top=6.1 if VERT else 3.35
  self.add(text('고윳값과 고유벡터  /  04',16,MUTED).move_to([0,top+.48,0]),text(TITLES[self.i],30,width=7.2 if VERT else 13).move_to([0,top,0]),Line([-3.6 if VERT else -6.6,top-.45,0],[3.6 if VERT else 6.6,top-.45,0],color=GRID,stroke_width=1))
  i=self.i;p=self.geometry();mc=self.matrix_center()
  if i==0:
   self.add(self.axes(p));m=self.colored_matrix(A).move_to(mc);self.add(m);v=self.arrow(p,[1,0],BLUE);self.add(v);self.play(Transform(v,self.arrow(p,[2,1],PURPLE)),run_time=1.5)
   self.play(Indicate(m[0][1],color=YELLOW),Indicate(m[0][2],color=YELLOW),run_time=.7);self.until(4);self.note('非対角 원소 = 다른 축으로의 영향'.replace('非対角','비대각'))
  elif i==1:
   m=self.colored_matrix(A).move_to(mc if VERT else [0,2.0,0]);self.add(m);nodes,links=self.network(False);self.add(nodes);self.until(2)
   self.play(Create(links[0]),Create(links[1]),run_time=1.3);self.until(8);self.play(Create(links[2]),Create(links[3]),run_time=1.2);self.note('x′ = 2x + y    ·    y′ = x + 2y')
  elif i==2:
   old=self.grid(p,np.eye(2));real=self.arrow(p,[2,1],BLUE);self.add(old,real);self.until(2)
   self.play(Transform(old,self.grid(p,S)),run_time=2.5);self.add(self.basis_lines(p,S,MUTED),self.units(p,S));self.note('b₁ = (1, 0)   ·   b₂ = (1, 1)\n평행하지 않은 두 벡터로 새 기저 구성')
  elif i==3:
   m=self.colored_matrix(np.linalg.solve(S,A@S)).move_to(mc);self.add(m,self.grid(p,S),self.basis_lines(p,S,MUTED),self.units(p,S));v=self.arrow(p,S[:,0],BLUE);self.add(v);self.note('새 기저에서도 M₂₁ = 1이 남는다');self.until(5)
   self.add(v.copy().set_opacity(.3));self.play(Transform(v,self.arrow(p,A@S[:,0],PURPLE)),run_time=1.4);self.note('Ab₁ = (2, 1)   ·   첫 번째 축에서 벗어남')
  elif i==4:
   m=self.colored_matrix(np.linalg.solve(S,A@S)).move_to(mc);axes=self.grid(p,S);rails=self.basis_lines(p,S,MUTED)
   parts=VGroup(self.arrow(p,[1,0],BLUE),self.arrow(p,[1,1],YELLOW,start=[1,0]),self.arrow(p,[2,1],PURPLE),DashedLine(p([0,0]),p([1,1]),color=YELLOW));self.add(m,axes,rails)
   self.play(GrowArrow(parts[0]),run_time=.7);self.play(GrowArrow(parts[1]),GrowArrow(parts[2]),Create(parts[3]),run_time=.9);self.play(Indicate(m[0][2],color=YELLOW),run_time=.6);self.note('Ab₁ = b₁ + b₂   →   M₂₁ = 1');self.until(7)
   self.remove(*parts.submobjects,axes,rails);m2=self.colored_matrix(np.linalg.solve(T,A@T)).move_to(mc);self.play(Transform(m,m2),run_time=.4);self.add(self.grid(p,T),self.basis_lines(p,T,MUTED));v=self.arrow(p,T[:,1],BLUE);self.add(v);self.play(Transform(v,self.arrow(p,A@T[:,1],PURPLE)),run_time=.9);self.note('다른 임의 기저: 두 번째 축에서도 섞임 발생')
  elif i==5:
   tracker=self.live_basis(0,column=0);self.note('첫 축을 고유방향으로 맞추는 중');self.play(tracker.animate.set_value(1),run_time=4.5);self.until(5);self.play(Indicate(self.live_entries[2],color=TEAL),run_time=.7);self.note('첫 축이 고유방향에 도달 → M₂₁ = 0')
  elif i==6:
   tracker=self.live_basis(1,column=0);self.note('Av₁ = 3v₁ + 0b₂\n첫 축은 다른 출력 성분을 만들지 않는다');self.until(4);self.play(Indicate(self.live_entries[2],color=TEAL),run_time=.8);self.note('M₂₁ = 0   ·   아직 M₁₂ = −1은 남아 있다')
  elif i==7:
   tracker=self.live_basis(1,column=1);self.note('첫 고유축은 고정: M₂₁ = 0');self.until(6)
   self.play(tracker.animate.set_value(2),run_time=5.7);self.play(Indicate(self.live_entries[1],color=TEAL),Indicate(self.live_entries[2],color=TEAL),run_time=.7);self.note('서로 독립인 두 고유축 → M₁₂ = M₂₁ = 0')
  elif i==8:
   self.add(self.colored_matrix(D).move_to(mc),self.basis_lines(p,P,MUTED));a=np.array([1.5,1.5]);b=np.array([.5,-.5]);c1=self.arrow(p,a,TEAL);c2=self.arrow(p,b,ORANGE,start=a);v=self.arrow(p,a+b,BLUE);self.add(c1,c2,v);self.play(Transform(c1,self.arrow(p,3*a,TEAL)),Transform(c2,self.arrow(p,b,ORANGE,start=3*a)),Transform(v,self.arrow(p,3*a+b,PURPLE)),run_time=2.5);self.note('x = av₁ + bv₂   →   Ax = 3av₁ + bv₂');self.until(5);self.add(text('(a, b) → (3a, b)',27,TEAL,width=6.8).move_to([0,2.55 if VERT else -1.7,0]));self.note('첫 성분 ×3   ·   두 번째 성분 ×1')
  elif i==9:
   centers=[np.array([0,2.8,0]),np.array([0,.5,0]),np.array([0,-1.8,0])] if VERT else [np.array([-4.5,.4,0]),np.array([0,.4,0]),np.array([4.5,.4,0])]
   for center,mat,label,col in zip(centers,[A,P,D],['A · 원래 표현','P = [v₁  v₂]','D · 고유기저 표현'],[BLUE,TEAL,PURPLE]):
    self.add(RoundedRectangle(width=5.6 if VERT else 3.7,height=2.05 if VERT else 2.8,corner_radius=.14,color=GRID,stroke_width=1).move_to(center),text(label,22,col).move_to(center+[0,.77 if VERT else 1.05,0]),self.matrix(mat,col,28).move_to(center+[0,-.18,0]))
   self.add(text('대각화',32,YELLOW).move_to([0,4.55 if VERT else 2.3,0]));self.note('D = P⁻¹ A P   ·   같은 변환, 다른 기저')
  elif i==10:
   self.steps(0);self.add(self.basis_lines(p,P,MUTED),self.arrow(p,[2,1],BLUE));coord=text('표준 좌표 (2, 1)',28,BLUE).move_to([0,2.1 if VERT else 1.4,0]);self.add(coord);self.until(2);self.play(Transform(coord,text('고유좌표 (1.5, 0.5)',28,TEAL).move_to(coord)),run_time=.9);self.note('P⁻¹ : 실제 벡터는 고정, 좌표로 다시 읽기')
  elif i==11:
   self.steps(1);self.add(self.basis_lines(p,P,MUTED));a=np.array([1.5,1.5]);b=np.array([.5,-.5]);u=self.arrow(p,a,TEAL);w=self.arrow(p,b,ORANGE,start=a);v=self.arrow(p,a+b,BLUE);self.add(u,w,v);self.play(Transform(u,self.arrow(p,3*a,TEAL)),Transform(w,self.arrow(p,b,ORANGE,start=3*a)),Transform(v,self.arrow(p,3*a+b,PURPLE)),run_time=1.8);self.note('D : (1.5, 0.5) → (4.5, 0.5)')
  elif i==12:
   self.steps(2);self.add(self.basis_lines(p,P,MUTED),self.arrow(p,[5,4],PURPLE));coord=text('고유좌표 (4.5, 0.5)',28,ORANGE).move_to([0,2.1 if VERT else 1.4,0]);self.add(coord);self.play(Transform(coord,text('표준 좌표 (5, 4)',28,BLUE).move_to(coord)),run_time=1);self.add(self.arrow(p,A@np.array([2,1]),BLUE).set_stroke(width=2));self.note('P : 4.5v₁ + 0.5v₂ = (5, 4) = A(2, 1)')
  elif i==13:
   centers=[np.array([0,2.9,0]),np.array([0,.85,0]),np.array([0,-1.2,0])] if VERT else [np.array([-4.5,.65,0]),np.array([0,.65,0]),np.array([4.5,.65,0])]
   for n,(c,s,label,col) in enumerate(zip(centers,['(2, 1) → (1.5, 0.5)','(1.5, 0.5) → (4.5, 0.5)','(4.5, 0.5) → (5, 4)'],['① P⁻¹ · 고유좌표','② D · 배율 적용','③ P · 원래 좌표'],[TEAL,YELLOW,ORANGE])):
    self.add(RoundedRectangle(width=6.5 if VERT else 4.15,height=1.55,corner_radius=.13,color=col,stroke_width=1).move_to(c),text(label,24,col,width=6 if VERT else 3.8).move_to(c+[0,.42,0]),text(s,24,INK,width=6 if VERT else 3.8).move_to(c+[0,-.3,0]))
    if n<2:self.add(text('↓' if VERT else '→',27,MUTED).move_to((c+centers[n+1])/2))
   formula=VGroup(*[text(t,35,c) for t,c in zip(['A','=','P','D','P⁻¹'],[INK,INK,ORANGE,YELLOW,TEAL])]).arrange(RIGHT,buff=.2).move_to([0,-3.1 if VERT else -1.75,0]);self.add(formula);self.note('공식의 오른쪽부터: P⁻¹ → D → P')
   for j in [4,3,2]:self.play(Indicate(formula[j],color=formula[j].get_color()),run_time=.7)
   self.until(4);self.note('변환 자체는 그대로 · 좌표 표현을 선택한 것')
  else:
   self.add(self.colored_matrix(D).move_to(mc if VERT else [0,2.0,0]));nodes,links=self.network(True);self.add(nodes,links[0],links[2]);self.note('독립적인 고유벡터 기저에서 각자의 배율만 남는다')
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
 def geometry(self):
  origin=np.array([-1.2,-.7,0]) if VERT else np.array([1.1,-.45,0]);scale=.6
  return lambda v:origin+scale*np.r_[np.array(v,dtype=float),0]
 def matrix_center(self):return np.array([0,3.6,0]) if VERT else np.array([-3.8,.8,0])
 def colored_matrix(self,m):
  obj=self.matrix(m,PURPLE,34)
  for k in [1,2]:obj[0][k].set_color(TEAL if abs(m.flat[k])<1e-10 else YELLOW)
  return obj
 def basis_lines(self,p,b,col=MUTED):return self.mapped_axes(p,b,extent=2.0).set_color(col)
 def grid(self,p,b):return self.mesh(p,b,1)
 def units(self,p,b):
  g=VGroup()
  for j in range(2):
   q=p(b[:,j]);d=b[:,j];normal=np.array([-d[1],d[0],0]);normal=normal/np.linalg.norm(normal)*.07
   g.add(Line(q-normal,q+normal,color=MUTED),text('1',18,MUTED).move_to(q+[.16,.2,0]))
  return g
 def network(self,diagonal=False):
  xleft=-2.55 if VERT else -3.7;xright=2.1 if VERT else 3.35
  ys=[.9,-1.2];nodes=VGroup();left=[];right=[]
  for j,y in enumerate(ys):
   col=TEAL if diagonal and j==0 else ORANGE if j==1 else BLUE
   l=text(['a','b'][j] if diagonal else ['x','y'][j],36,col).move_to([xleft,y,0]);rr=text(['3a','b'][j] if diagonal else ['2x + y','x + 2y'][j],34,col if diagonal else PURPLE,width=2.5 if VERT else 4).move_to([xright,y,0]);nodes.add(l,rr);left.append(l);right.append(rr)
  links=VGroup()
  for j,k in [(0,0),(1,0),(1,1),(0,1)]:links.add(Arrow(left[j].get_right()+RIGHT*.15,right[k].get_left()-RIGHT*.15,buff=0,color=(TEAL if j==0 else ORANGE) if diagonal else MUTED if j==k else YELLOW,stroke_width=3))
  return nodes,links
 def steps(self,active):
  centers=[np.array([-2.45,3.8 if VERT else 2.3,0]),np.array([0,3.8 if VERT else 2.3,0]),np.array([2.45,3.8 if VERT else 2.3,0])]
  for n,(c,s,col) in enumerate(zip(centers,['P⁻¹','D','P'],[TEAL,YELLOW,ORANGE])):
   self.add(RoundedRectangle(width=1.9,height=.78,corner_radius=.1,color=col if n==active else GRID,stroke_width=2 if n==active else 1).move_to(c),text(s,30,col if n==active else MUTED).move_to(c))
   if n<2:self.add(text('→',22,MUTED).move_to((c+centers[n+1])/2))
 def basis_at(self,t):
  t=float(np.clip(t,0,2));j=min(int(t),1);f=t-j;return BASES[j]*(1-f)+BASES[j+1]*f
 def live_basis(self,initial,column=0):
  tracker=ValueTracker(initial);self.add(tracker);c=self.matrix_center();p=self.geometry()
  self.add(text('현재 기저의 표현 · 반올림 표시',20,PURPLE,width=6.8 if VERT else 5.8).move_to(c+[0,1.1,0]))
  entries=VGroup(*[text('0',31,PURPLE).move_to(c+[x,y,0]) for y in [.35,-.35] for x in [-.7,.7]]);self.live_entries=entries
  brackets=VGroup()
  for x in [-1.4,1.4]:
   brackets.add(Line(c+[x,-.7,0],c+[x,.7,0],color=PURPLE))
   for y in [-.7,.7]:brackets.add(Line(c+[x,y,0],c+[x-np.sign(x)*.15,y,0],color=PURPLE))
  self.add(entries,brackets)
  segments=[]
  for k in [-1.25,-.625,0,.625,1.25]:segments.extend([([k,-1.25],[k,1.25]),([-1.25,k],[1.25,k])])
  lines=VGroup(*[Line(p(a),p(b),color=GRID,stroke_width=1.2) for a,b in segments]);axes=self.basis_lines(p,BASES[int(initial)]);ins=self.arrow(p,BASES[int(initial)][:,column],BLUE);out=self.arrow(p,A@BASES[int(initial)][:,column],PURPLE);self.add(lines,axes,ins,out)
  unit_lines=VGroup(Line(p([0,0]),p([.01,0])),Line(p([0,0]),p([.01,0])));unit_labels=VGroup(text('1',18,MUTED),text('1',18,MUTED));self.add(unit_lines,unit_labels)
  cache={};previous=[None]*4
  def update(_):
   b=self.basis_at(tracker.get_value());m=np.linalg.solve(b,A@b)
   for n,val in enumerate(m.flat):
    zero=abs(val)<1e-10
    if n in [1,2]:
     label='0' if zero else '≈0' if abs(val)<.005 else f'{val:.2f}'.rstrip('0').rstrip('.');col=TEAL if zero else YELLOW
    else:label=f'{val:.1f}'.rstrip('0').rstrip('.');col=PURPLE
    label=label.replace('-','−');key=(label,col)
    if key!=previous[n]:
     if key not in cache:cache[key]=text(label,31,col)
     entries[n].become(cache[key].copy().move_to(entries[n]));previous[n]=key
   for line,(a,z) in zip(lines,segments):line.put_start_and_end_on(p(b@np.array(a)),p(b@np.array(z)))
   for j in range(2):
    q=p(b[:,j]);d=b[:,j];normal=np.r_[-d[1],d[0],0];normal=normal/np.linalg.norm(normal)*.07;unit_lines[j].put_start_and_end_on(q-normal,q+normal);unit_lines[j].set_color(MUTED);unit_labels[j].move_to(q+[.16,.2,0])
   axes.become(self.basis_lines(p,b));ins.become(self.arrow(p,b[:,column],BLUE));out.become(self.arrow(p,A@b[:,column],PURPLE))
  tracker.add_updater(update);update(tracker)
  return tracker
