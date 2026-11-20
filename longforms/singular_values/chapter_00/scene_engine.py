from manim import *
import numpy as np
import json,textwrap
from pathlib import Path
config.background_color='#0d121d'
config.frame_width=14.222222
config.frame_height=8
BLUEC='#58a6ff'; ORANGE='#ff963e'; GREEN='#47e78b'; PURPLE='#bd87ff'; MUTED='#94a3b8'
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
B=np.array([[1.,2.],[0.,1.]])
def txt(s,size=28,color=WHITE):return Text(s,font='Malgun Gothic',font_size=size,color=color)
def label(s,p,size=28,color=WHITE):return txt(s,size,color).move_to(p)
def arrow(c,v,color,scale=1):return Arrow(np.array(c),np.array(c)+np.r_[v,0]*scale,buff=0,stroke_width=4,max_tip_length_to_length_ratio=.16,color=color)
def clipped(p,q):
 d=q-p;lo=0.;hi=1.
 for k,limit in [(0,2.75),(1,1.7)]:
  if abs(d[k])<1e-9:
   if abs(p[k])>limit:return None
  else:
   a,b=sorted(((-limit-p[k])/d[k],(limit-p[k])/d[k]));lo=max(lo,a);hi=min(hi,b)
 if hi<=lo:return None
 return p+lo*d,p+hi*d

def grid(c,M=np.eye(2),scale=.9):
 g=VGroup();c=np.array(c)
 for axis in [0,1]:
  for x in np.arange(-5,5.01,.5):
   p=np.array([x,-5.]) if axis==0 else np.array([-5.,x]);q=np.array([x,5.]) if axis==0 else np.array([5.,x])
   pair=clipped(M@p*scale,M@q*scale)
   if pair:
    a,b=pair;g.add(Line(c+np.r_[a,0],c+np.r_[b,0],color=MUTED,stroke_width=1,stroke_opacity=.38 if abs(x)<.01 else .13))
 return g

def shape(c,M=np.eye(2),color=BLUEC,scale=.9):
 c=np.array(c);pts=[c+np.r_[M@np.array(p)*scale,0] for p in [(0,0),(1,0),(1,1),(0,1)]]
 return VGroup(Polygon(*pts,color=color,fill_opacity=.14,stroke_width=3),arrow(c,M@np.array([1,0]),color,scale),arrow(c,M@np.array([0,1]),color,scale))
class ChapterScene(Scene):
 index=0
 def title(self,s):self.add(label(s,[0,3.15,0],32))
 def add_caption(self):
  text=DATA[self.index]['text'];wrapped=textwrap.wrap(text,width=48,break_long_words=False)
  # Korean wrapping at word boundaries, independent of visual title area.
  cap=VGroup(*[txt(s,25) for s in wrapped]).arrange(DOWN,buff=.12)
  if cap.width>12.8:cap.scale_to_fit_width(12.8)
  cap.move_to([0,-3.25,0]);self.add(Rectangle(width=14.22,height=1.25,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-3.35,0]),cap)
  assert cap.get_bottom()[1]>-3.98
 def finish(self):
  duration=DATA[self.index]['end']-DATA[self.index]['start'];remain=duration-self.time
  if remain>1e-6:self.wait(remain)
  elif remain<-.04:raise ValueError((self.index,self.time,duration))
 def construct(self):
  i=self.index;L=np.array([-3.45,.3,0]);R=np.array([3.45,.3,0]);C=np.array([0,.35,0])
  if i==0:
   self.title('선형변환 속의 특별한 방향');self.add(grid(L),grid(R),label('B',[0,.65,0],24),Arrow([-.65,.3,0],[.65,.3,0],color=MUTED))
   before=VGroup();after=VGroup()
   for theta in np.arange(0,2*np.pi,np.pi/4):
    v=np.array([np.cos(theta),np.sin(theta)]);color=GREEN if abs(v[1])<1e-8 else BLUEC
    before.add(arrow(L,v,color,1.2));after.add(arrow(R,v,color,1.2))
   self.add(before,after);self.add_caption();self.wait(1)
   target=VGroup(*[arrow(R,B@np.array([np.cos(t),np.sin(t)]),GREEN if abs(np.sin(t))<1e-8 else ORANGE,1.2) for t in np.arange(0,2*np.pi,np.pi/4)])
   self.play(Transform(after,target),run_time=2);self.add(DashedLine(R+LEFT*2.6,R+RIGHT*2.6,color=GREEN));self.wait(2);self.add(label('Bv = λv',[0,-2,0],35,GREEN))
  elif i in [1,2]:
   self.title('고윳값이 같다면?' if i==1 else '성분 하나가 다른 두 행렬')
   for c,name,vals in [(L,'A',[[1,0],[0,1]]),(R,'B',[[1,2],[0,1]])]:
    self.add(RoundedRectangle(width=4.8,height=3.3,corner_radius=.18,color='#354458',fill_color='#1a2536',fill_opacity=1).move_to(c),label('Matrix '+name,c+UP*.95,30))
    if i==1:self.add(label('λ₁ = 1,  λ₂ = 1',c+DOWN*.25,31,GREEN))
    else:
     m=Matrix(vals,element_to_mobject=lambda s:txt(str(s),34),h_buff=.85,v_buff=.65).scale(.8).move_to(c+DOWN*.25)
     if name=='B':m.get_entries()[1].set_color(ORANGE)
     self.add(m)
   self.add(label('?' if i==1 else '≠',[0,.3,0],48,PURPLE));self.add_caption()
  elif i in [3,4]:
   self.title('항등변환  A = I' if i==3 else '전단변환 B')
   self.add(grid(L),shape(L),Arrow([-.6,.3,0],[.6,.3,0],color=WHITE),label('변환 이전',L+DOWN*2.1,25,MUTED),label('변환 이후',R+DOWN*2.1,25,BLUEC if i==3 else ORANGE))
   moving=VGroup(grid(R),shape(R));self.add(moving);self.add_caption();self.wait(.5)
   if i==4:self.play(Transform(moving,VGroup(grid(R,B),shape(R,B,ORANGE))),run_time=2)
   else:self.play(Indicate(moving,color=BLUEC,scale_factor=1),run_time=1.5)
   self.add(label('Av = v' if i==3 else 'B(1, 0) = (1, 0)     B(0, 1) = (2, 1)',[0,-2.3,0],26,GREEN if i==3 else ORANGE))
  elif i==5:
   self.title('같은 행렬, 서로 다른 길이 변화');self.add(grid(L),grid(R),shape(R,B,ORANGE).set_opacity(.2),Arrow([-.6,.3,0],[.6,.3,0]),label('B',[0,.8,0],24));self.add_caption();self.wait(2)
   u=np.array([1.,2.])/np.sqrt(5);v=np.array([-2.,1.])/np.sqrt(5)
   vec=VGroup(arrow(R,u,BLUEC,1.05),arrow(R,v,PURPLE,1.05));self.add(arrow(L,u,BLUEC,1.05),arrow(L,v,PURPLE,1.05),vec,label('두 입력 길이: 1',L+DOWN*2,26,MUTED));self.wait(1)
   self.play(Transform(vec,VGroup(arrow(R,B@u,BLUEC,1.05),arrow(R,B@v,PURPLE,1.05))),run_time=2)
   self.add(label('팽창 ≈ 2.41배',R+DOWN*1.95,27,BLUEC),label('수축 ≈ 0.45배',R+DOWN*2.4,27,PURPLE))
  elif i==6:
   self.title('변환은 다르지만, 고윳값은 같다');self.add(grid(L),grid(R,B),shape(L),shape(R,B,ORANGE),label('항등변환 A',L+UP*2,28,BLUEC),label('전단변환 B',R+UP*2,28,ORANGE));self.add_caption();self.wait(.6)
   a=label('λ₁ = λ₂ = 1',L+DOWN*2,34,GREEN);b=label('λ₁ = λ₂ = 1',R+DOWN*2,34,GREEN)
   self.play(FadeIn(a),FadeIn(b),run_time=.5);self.add(label('=',[0,-1.7,0],42,GREEN));self.play(Indicate(a,scale_factor=1.08),Indicate(b,scale_factor=1.08),run_time=1)
  elif i==7:
   self.title('고윳값이 관찰하는 방향');self.add(grid(C),label('Bv = λv',[0,2.45,0],30,GREEN));others=VGroup()
   for t in np.arange(0,2*np.pi,np.pi/6):
    v=np.array([np.cos(t),np.sin(t)]);a=arrow(C,v,GREEN if abs(v[1])<1e-8 else MUTED,1.5)
    if abs(v[1])<1e-8:self.add(a)
    else:others.add(a.set_opacity(.3))
   self.add(others,DashedLine(C+LEFT*2.7,C+RIGHT*2.7,color=GREEN),label('λ = 1',C+RIGHT*2+UP*.5,27,GREEN),label('나머지 방향의 길이 변화는?',[0,-2.15,0],28,MUTED));self.add_caption();self.wait(5);self.play(others.animate.set_opacity(1).set_color(BLUEC),run_time=2)
  elif i==8:
   self.title('방향에서 길이로');c=np.array([-2.6,.2,0]);v=np.array([1.,2.])/np.sqrt(5)
   plane=grid(c);guide=DashedLine(c-v[0]*2*RIGHT-v[1]*2*UP,c+v[0]*2*RIGHT+v[1]*2*UP,color=GREEN)
   self.add(plane,guide);self.add_caption();self.play(FadeOut(guide),run_time=2)
   self.play(GrowArrow(arrow(c,v,BLUEC,1.2)),GrowArrow(arrow(c,B@v,ORANGE,1.2)),run_time=2)
   self.wait(1)
   bars=VGroup(label('길이만 비교',[3.5,1.7,0],28),label('입력 길이',[2.4,1,0],23,BLUEC),Line([2,.55,0],[3,.55,0],stroke_width=12,color=BLUEC),label('출력 길이',[2.4,-.2,0],23,ORANGE),Line([2,-.65,0],[2+np.linalg.norm(B@v),-.65,0],stroke_width=12,color=ORANGE))
   self.play(FadeIn(bars),plane.animate.set_opacity(.2),run_time=1);self.add(label('길이의 변화만 측정할 수 있을까?',[0,-2.25,0],30,PURPLE))
  elif i==9:
   self.add(Circle(radius=1.35,color=BLUEC,stroke_opacity=.22),Ellipse(width=6.2,height=1.3,color=PURPLE,stroke_opacity=.3).rotate(.35));self.add_caption()
   self.play(GrowFromCenter(label('σ',[0,1.25,0],95,PURPLE)),run_time=.7);self.play(FadeIn(label('특잇값',[0,-.1,0],56)),FadeIn(label('Singular Value',[0,-1,0],30,MUTED)),run_time=.6)
  else:
   self.title('특잇값이 알려주는 것');self.add_caption()
   for x,title,sub in [(-4.4,'기하학적 구조','Geometry'),(0,'정보의 손실','Information Loss'),(4.4,'계산의 안정성','Numerical Stability')]:
    self.add(RoundedRectangle(width=4.05,height=4.15,corner_radius=.13,color='#344256',fill_color='#151e2b',fill_opacity=1).move_to([x,.1,0]),label(title,[x,-1.15,0],27),label(sub,[x,-1.65,0],19,MUTED))
   def ellipse(x):return Ellipse(width=2.7,height=.85,color=PURPLE).rotate(.4).move_to([x,.55,0])
   g=Circle(radius=1.15,color=BLUEC).move_to([-4.4,.55,0]);self.add(g);self.play(Transform(g,ellipse(-4.4)),run_time=2);self.wait(1)
   h=ellipse(0);self.add(h);self.play(Transform(h,Line([-1.4,.55,0],[1.4,.55,0],color=BLUEC,stroke_width=5)),run_time=2);self.wait(1)
   self.add(Ellipse(width=2.7,height=.28,color=PURPLE).move_to([4.4,.55,0]));err=Arrow([4.4,.55,0],[4.4,.85,0],buff=0,color='#ff627e');self.add(err);self.play(Transform(err,Arrow([4.4,.55,0],[4.4,1.8,0],buff=0,color='#ff627e')),run_time=2);self.add(label('오차',[5.15,1.65,0],21,'#ff627e'));self.wait(1)
   content=[m for m in self.mobjects if m.get_center()[1]>-2.6];self.play(*[FadeOut(m) for m in content],run_time=1)
  self.finish()
