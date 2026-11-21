"""156-second chapter: observed object → force analysis → deterministic prediction."""
import json,textwrap
from pathlib import Path
from manim import *
from physics import PendulumModel
R=Path(__file__).resolve().parent
BG='#09111E';INK='#EAF0F7';MUTED='#8294AB';BLUE='#65B9EF';GOLD='#EDBC73';GREEN='#62D7B9';RED='#F1848B'
config.background_color=BG;config.frame_width=128/9;config.frame_height=8
MODEL=PendulumModel()
def tx(s,x=0,y=0,size=28,c=INK,w=12):
 m=Text(s,font='Malgun Gothic',font_size=size,color=c)
 if m.width>w:m.scale_to_fit_width(w)
 return m.move_to([x,y,0])
def eq(s,x=0,y=0,size=44,c=INK,w=6):
 m=MathTex(s,font_size=size,color=c)
 if m.width>w:m.scale_to_fit_width(w)
 return m.move_to([x,y,0])
def ball(p,c=GOLD,r=.14,opacity=1):
 p=np.array(p);return VGroup(Dot(p,radius=r*2.5,color=c,fill_opacity=.035,stroke_width=0),Dot(p,radius=r*1.5,color=c,fill_opacity=.1,stroke_width=0),Dot(p,radius=r,color=c),Dot(p+[-r*.25,r*.28,0],radius=r*.32,color=WHITE,fill_opacity=.6))
def arr(p,v,c=BLUE,opacity=1):
 v=np.array(v)
 if np.linalg.norm(v)<.025:return VGroup()
 return Arrow(p,np.array(p)+v,buff=0,stroke_width=4,color=c,max_tip_length_to_length_ratio=.22).set_opacity(opacity)
def bobpoint(theta,pivot,L):return np.array(pivot)+L*np.array([np.sin(theta),-np.cos(theta),0])
def rig(t,pivot=(0,2.25,0),L=3.6,forces=0,trace=True,theta=None,omega=None,opacity=1):
 th,om=MODEL.state_at(t) if theta is None else (theta,0 if omega is None else omega)
 p=np.array(pivot);b=bobpoint(th,p,L);rad=np.array([np.sin(th),-np.cos(th),0]);tan=np.array([np.cos(th),np.sin(th),0]);g=VGroup()
 if trace:
  arc=ParametricFunction(lambda a:bobpoint(a,p,L),t_range=[-.68,.68,.025],color=BLUE,stroke_width=2,stroke_opacity=.2,fill_opacity=0);g.add(arc)
 g.add(Line(p+[-.4,.1,0],p+[.4,.1,0],color=MUTED,stroke_width=5),Dot(p,radius=.055,color=INK),Line(p,b,color=INK,stroke_width=2),ball(b,r=.16))
 if forces>=1:
  g.add(arr(b,[0,-.95,0],GOLD),arr(b,-rad*(MODEL.g*np.cos(th)+MODEL.length*om**2)/MODEL.g*.95,BLUE))
 if forces>=2:
  # Exact orthogonal decomposition of a unit downward gravity vector.
  tang=-np.sin(th)*tan;radial=np.cos(th)*rad
  g.add(arr(b,radial*.95,MUTED,.45),arr(b,tang*.95,GREEN))
 if forces>=3:
  g.add(arr(b,tan*om*.28,RED))
 return g

class ChapterScene(Scene):
 index=1
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.clock=ValueTracker(self.start);self.dynamic=VGroup();self.add(self.clock,self.dynamic)
  self.add(tx('CHAPTER 01  /  NEWTON',-4.9,3.6,18,MUTED,w=4),tx('예측이 가능해진 물체의 운동',3.4,3.6,22,w=6))
  self.add(Line([-6.4,3.25,0],[6.4,3.25,0],stroke_color=MUTED,stroke_opacity=.25))
  self.panel=RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50);self.add(self.panel)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.static=VGroup();self.current=None;self.stage=None
  # Only geometry is rebuilt per frame; text changes only at actual event boundaries.
  self.dynamic.add_updater(lambda m:m.become(self.geometry(self.clock.get_value())))
  events=sorted(set([self.start,self.end]+[l['start'] for l in self.lines if self.start<l['start']<self.end]+[x for x in [3,6,9,15,20,25,27,33,36,38,44,46,49,55,59,62,66,71,76,80,86,89,93,98,104,110,120,127,132,141,149,153] if self.start<x<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=b-a,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def update_text(self,t):
  l=next(x for x in self.lines if x['start']<=t<x['end'])
  if l!=self.current:
   self.remove(self.caption);self.current=l
   parts=textwrap.wrap(l['text'],width=52,break_long_words=False,break_on_hyphens=False)
   self.caption=VGroup(*[tx(p,size=25,w=12.2) for p in parts]).arrange(DOWN,buff=.1).move_to([0,-3.3,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(kind='caption',start=l['start'],end=l['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1])))
  self.remove(self.static);self.static=self.labels(t);self.add(self.static)
  for m in self.static:
   assert m.get_left()[0]>-6.8 and m.get_right()[0]<6.8 and m.get_bottom()[1]>-2.75 and m.get_top()[1]<3.2,('label outside safe area',t)
 def labels(self,t):
  g=VGroup()
  if t<20:
   if t>=3:g.add(tx('같은 위치',0,2.35,30),tx('서로 다른 속도 → 서로 다른 미래',0,-2.2,27,BLUE))
   if t>=15:g.add(tx('예측하려면 무엇을 알아야 할까?',0,1.5,31,GOLD))
  elif t<44:
   g.add(tx('힘은 운동을 변화시킨다',0,2.35,33))
   if t>=25:g.add(tx('알짜힘',3,1.05,24,BLUE))
   if 27<=t<33:g.add(eq(r'\mathbf F=\frac{d\mathbf p}{dt}',0,-1.15,45))
   if 33<=t<36:g.add(eq(r'\mathbf F=m\mathbf a',0,-1.1,66,c=GOLD))
   elif t>=36:g.add(eq(r'\mathbf F=m\mathbf a',4.9,2.35,36,c=GOLD,w=2.4))
   if t>=38:g.add(tx('힘이 없어도 운동은 계속된다',0,-2.2,25,MUTED))
  elif t<59:
   g.add(tx('이상적인 진자 · 마찰 무시',-4.5,2.7,20,MUTED,w=4))
   if t>=55:g.add(tx('이 움직임을 계산할 수 있을까?',0,-2.25,29,GOLD))
  elif t<89:
   g.add(tx('이상적인 진자 · 마찰 무시',-4.5,2.7,20,MUTED,w=4))
   if t>=62:g.add(tx('중력',4.8,1.65,26,GOLD),tx('장력',4.8,.95,26,BLUE))
   if t>=66:g.add(tx('실의 길이 일정',-4.6,1.3,24,MUTED,w=3))
   if t>=71:g.add(tx('접선 방향 성분',4.8,.1,25,GREEN,w=3.1),eq(r'F_{\mathrm{tan}}=-mg\sin\theta',4.8,-.65,29,c=GREEN,w=3.2))
   if 76<=t<80:g.add(tx('최저점: 접선력 0 / 속력 최대',0,-2.25,27,GREEN),tx('순간 정지 · 상태 분석',-4.5,.4,21,MUTED,w=3.8))
   elif t>=80:g.add(tx('힘의 방향은 평형 위치 쪽으로',0,-2.25,27,GREEN))
  elif t<110:
   g.add(tx('물리적 대상',-3.1,2.8,24,MUTED),tx('계산으로 얻은 모델',3.2,2.8,24,BLUE))
   if t>=93:g.add(eq(r'\ddot\theta=-\frac{g}{\ell}\sin\theta',3.25,1.8,47,c=GOLD,w=4.4))
   if t>=98:g.add(tx('초기 각도 0.65 rad  ·  초기 각속도 0',3.25,.65,22,w=5.3),tx('현재 상태 + 운동 법칙 → 미래의 위치',0,-2.25,27,GREEN))
   else:g.add(tx('힘의 관계를 운동방정식으로',3.25,.65,25,w=5))
   if 98<=t<104:g.add(tx('+0.1 s     +0.2 s     +0.3 s',3.3,.25,24,BLUE,w=5))
   if t>=104:g.add(tx('계산된 위치와 움직임의 일치',3.25,.25,25,BLUE,w=5))
  elif t<132:
   if t<120:g.add(eq(r'\text{Force}+\text{Initial state}\ \longrightarrow\ \text{Prediction}',2.1,1.4,33,w=7),tx('관찰을 넘어, 법칙에서 운동을 계산한다',2.1,-.1,27,w=7))
   elif t<127:g.add(tx('진자',-4.5,2.6,24),tx('낙하',0,2.6,24),tx('충돌',2.2,2.6,24),tx('공전',4.8,2.6,24),eq(r'\mathbf F=\frac{d\mathbf p}{dt}',0,-2.1,43))
   else:g.add(tx('힘과 초기조건 → 운동의 예측',0,2.55,36,GOLD))
  else:
   if t<141:g.add(tx('힘과 제약 조건의 분석',0,2.65,29))
   elif t<149:g.add(tx('연결된 물체 · 늘어나는 제약 조건',0,2.65,29),tx('연결계의 힘 분석 개념도',0,-2.35,20,MUTED))
   else:
    g.add(tx('다양한 운동을 설명하는 공통 원리는?',0,2.65,31,GOLD))
    if t>=153:g.add(tx('운동에너지  T',-4,1,29,BLUE,w=3.4),tx('위치에너지  V',4,1,29,GOLD,w=3.4))
  return g
 def geometry(self,t):
  if self.index==1:
   g=VGroup();q=min(max((t-3)/6,0),1)
   if t<3:return ball([-2+min(t,2)*.8,0,0])
   for i,(v,y,c) in enumerate([(-1.3,.7,BLUE),(.65,0,GOLD),(1.6,-.7,GREEN)]):
    x=v*q*2.3;g.add(DashedLine([0,y,0],[x if abs(x)>.01 else .01,y,0],color=c,stroke_opacity=.35),ball([x,y,0],c,opacity=.65),arr([x,y,0],[v*.65,0,0],c))
   g.add(DashedLine([0,-1.3,0],[0,1.3,0],stroke_color=MUTED,stroke_opacity=.25))
   return g
  if self.index==2:
   u=t-20
   # One continuous trajectory: no force before t=25, constant acceleration afterwards.
   z=max(u-5,0);x=-4+.2*u+.009*z*z
   g=ball([x,.2,0]);g.add(arr([x,.2,0],[.4+.036*z,0,0],GREEN))
   if t>=25:g.add(arr([x,.65,0],[1.4,0,0],BLUE))
   g.add(Line([-5,-.2,0],[5,-.2,0],stroke_color=MUTED,stroke_opacity=.25))
   return g
  if self.index==3:
   th=0 if t<46 else .65*min((t-46)/3,1) if t<49 else None
   return rig(max(t-49,0) if t<55 else 6,theta=th)
  if self.index==4:
   # Lowest-point hold illustrates zero tangent force with nonzero velocity; time is visibly analyzed, not re-integrated.
   if 76<=t<80:return rig(0,forces=3,theta=0,omega=-np.sqrt(2*MODEL.g/MODEL.length*(1-np.cos(.65))))
   return rig((t-59)*.65+6,forces=1 if t<71 else 2)
  if self.index==5:
   u=0 if t<98 else max(0,t-104)
   g=rig(u,pivot=(-3.1,2.25,0),L=3.45)
   # Right: identical model, same physical length/time; screen scale is a separate layout choice.
   rp=(3.2,-.15,0);L=1.65
   g.add(rig(u,pivot=rp,L=L,trace=True))
   if t>=98:
    count=min(8,int((t-98)*2)+1)
    for k in range(1,count+1):
     future=k*.1;th,_=MODEL.state_at(future);p=bobpoint(th,rp,L)
     g.add(Line(rp,p,color=BLUE,stroke_opacity=.13,stroke_width=1),Dot(p,radius=.065,color=BLUE,fill_opacity=.45))
   return g
  if self.index==6:
   if t<120:return rig(t-104,pivot=(-3.5,2.25,0),L=3.5)
   if t>=127:return rig(t-104)
   g=rig(t-104,pivot=(-4.5,2.15,0),L=2.65)
   z=(t-120)%1.6;h=1.8-1.5*z*z;g.add(Line([-.8,-1.9,0],[.8,-1.9,0],color=MUTED),ball([0,h,0],BLUE),arr([0,h,0],[0,-.65,0],GOLD))
   # Equal masses in a 1D elastic collision; velocities exchange at impact.
   z=(t-120)%3;d=abs(z-1.5)*.45+.14
   g.add(ball([2.2-d,.25,0],BLUE,r=.13),ball([2.2+d,.25,0],GOLD,r=.13))
   # Elliptical Kepler motion, focus at origin of inverse-square force.
   M=(t-120)*1.1;E=M
   for _ in range(8):E-=(E-.45*np.sin(E)-M)/(1-.45*np.cos(E))
   center=np.array([4.8,.3,0]);a=1.15;e=.45;b=a*np.sqrt(1-e*e);p=center+[a*np.cos(E),b*np.sin(E),0];sun=center+[-a*e,0,0]
   g.add(Ellipse(width=2*a,height=2*b,color=BLUE,stroke_opacity=.4).move_to(center),ball(sun,GOLD,.1),ball(p,BLUE,.09),arr(p,(sun-p)/np.linalg.norm(sun-p)*.5,GOLD))
   return g
  if t<141:return rig(t-104,forces=2)
  if t>=149:return rig(t-104)
  # Static conceptual constraint network. No invented dynamics or tension magnitudes.
  g=VGroup();p=np.array([0,2.15,0]);g.add(Dot(p,color=INK,radius=.05))
  for k,(ang,L) in enumerate([(.55,1.2),(-.7,1.15),(.65,1.15)]):
   q=p+L*np.array([np.sin(ang),-np.cos(ang),0]);g.add(Line(p,q,color=INK),ball(q,r=.13),arr(q,[0,-.55,0],GOLD),arr(q,(p-q)/L*.55,BLUE))
   if k<2:g.add(arr(q,-(p-q)/L*.45,BLUE,.5))
   p=q
  return g
