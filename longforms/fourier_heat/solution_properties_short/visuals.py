"""Independent vertical scenes using exact heat evolution and sampled Brownian paths."""
from pathlib import Path
import json,textwrap
import numpy as np
from manim import *
from mechanics import X,K,T,N,PATHS,ENDPOINTS,initial,solution,slope,step_points,kernel,lower
R=Path(__file__).resolve().parent
BG='#09111E';INK='#EAF0F7';MUTED='#8294AB';BLUE='#65B9EF';GOLD='#EDBC73';GREEN='#62D7B9';PURPLE='#A596EF';RED='#F1848B'
config.frame_width=9;config.frame_height=16;config.background_color=BG
TC={}
def tx(s,x=0,y=0,size=28,c=INK,w=7.2):
 key=(s,size,c,w)
 if key not in TC:
  o=Text(s,font='Malgun Gothic',font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  TC[key]=o
 return TC[key].copy().move_to([x,y,0])
def eq(s,x=0,y=0,size=36,c=INK,w=7.2):return tx(s,x,y,size,c,w)
def plot(xs,ys,y=0,h=3,w=7.1,yr=100,c=GREEN,width=3):
 p=np.column_stack((np.asarray(xs)*w/9,y-h/2+np.asarray(ys)*h/yr,np.zeros(len(xs))))
 return VMobject(stroke_color=c,stroke_width=width).set_points_as_corners(p)
def dot(x,v,y=0,h=3,c=GOLD,r=.075):return Dot([x*7.1/9,y-h/2+v*h/100,0],radius=r,color=c)
def axes(y=0,h=3):
 return VGroup(Line([-3.55,y-h/2,0],[3.55,y-h/2,0],color=MUTED,stroke_width=1.2),Line([-3.55,y-h/2,0],[-3.55,y+h/2,0],color=MUTED,stroke_width=1.2))
def dash(y,c=GOLD):return DashedLine([-3.55,y,0],[3.55,y,0],color=c,stroke_width=2,dash_length=.12)
def clip(q):return float(np.clip(q,0,1))
class HeatScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[];self.body_audit=[];self.current=None
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  self.add(tx('열방정식의 해가 가지는 특별한 성질',0,7.15,25),Line([-3.7,6.65,0],[3.7,6.65,0],color=MUTED,stroke_opacity=.35))
  self.add(RoundedRectangle(width=7.8,height=2.0,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([-.1,-5.9,0]).set_z_index(50))
  self.caption=VGroup();self.labels_now=VGroup();self.dynamic=VGroup();self.clock=ValueTracker(self.start);self.add(self.clock,self.dynamic)
  def update(m):
   t=self.clock.get_value();g=self.geometry(t)
   if len(g):
    assert g.get_left()[0]>=-4.05 and g.get_right()[0]<=4.05 and g.get_bottom()[1]>=-4.7 and g.get_top()[1]<=6.4,('geometry',self.index,t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
   m.submobjects=g.submobjects
  self.dynamic.add_updater(update)
  events=sorted(set([self.start,self.end]+[z for z in [5,7,12,19,22,27,31,35,38,43,46,54,63,67,75,81,84,94,102,104,106,108,112,117,127,134,139,142,150,159,163,167] if self.start<z<self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=(round(b*config.frame_rate)-round(a*config.frame_rate))/config.frame_rate,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(dict(captions=self.audit,labels=self.body_audit,geometry_checked_every_frame=True),indent=2),encoding='utf-8')
 def update_text(self,t):
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  if line!=self.current:
   self.remove(self.caption);self.current=line
   self.caption=VGroup(*[tx(p,size=28,w=7.2) for p in textwrap.wrap(line['text'],width=27,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.12)
   if self.caption.height>1.5:self.caption.scale_to_fit_height(1.5)
   self.caption.move_to([-.1,-5.9,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=line['start'],end=line['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1]),height=float(self.caption.height)))
  self.remove(self.labels_now);self.labels_now=self.labels(t);self.add(self.labels_now)
  for m in self.labels_now:
   assert m.get_left()[0]>=-4.05 and m.get_right()[0]<=4.05 and m.get_bottom()[1]>=-4.7 and m.get_top()[1]<=6.4,('label',self.index,t,m.get_center())
  self.body_audit.append(dict(time=t,bottom=float(self.labels_now.get_bottom()[1]),top=float(self.labels_now.get_top()[1])))
 def labels(self,t):
  i=self.index;g=VGroup();titles=['방정식, 그리고 그 해','첫 번째 · 매끄러움','두 번째 · 최댓값 원리','세 번째 · 하르나크 부등식','같은 해, 다른 표현','무작위 운동의 평균','가우스 분포로 평균한다','하나의 해에 담긴 수학적 구조']
  g.add(tx(titles[i-1],0,5.9,31,c=GOLD))
  if i==1:
   g.add(tx('EQUATION',0,4.7,22,c=MUTED),eq('∂ₜu = κΔu',0,3.65,49,c=GREEN))
   if t<5:g.add(eq('y′ = y',-2,1.8,32,c=MUTED,w=2.5),eq('Δv = 0',2,1.8,32,c=MUTED,w=2.5),tx('해를 구한다 → 해의 성질을 묻는다',0,-3.6,28))
   else:
    g.add(tx('SOLUTION  ·  u(x,t)',0,2.25,27,c=GREEN),tx('위치 x',2.7,-2.1,21,c=MUTED,w=2),tx('시간에 따른 온도 분포',0,-3.6,27))
    if t>=12:g.add(tx('서로 다른 초기조건에 대응하는 해',0,-4.4,22,c=MUTED))
  elif i==2:
   g.add(tx('SMOOTHING PROPERTY',0,4.85,22,c=MUTED),tx('전체 실수 공간 · 유계 초기함수',0,-4.35,21,c=MUTED))
   if t<27:g.add(eq('t = 0',0,-2.45,34,c=GOLD),tx('불연속과 뾰족한 변화',0,3.6,27,c=GOLD))
   else:g.add(eq('t > 0',0,-2.45,34,c=GREEN))
   if 31<=t<35:g.add(tx('접선도 연속적으로 변한다',0,3.6,26,c=GREEN))
   if 35<=t<38:g.add(eq('∂ₓu    ∂ₓ²u    ∂ₓ³u    ⋯',0,3.6,35,c=GREEN))
   if t>=38:g.add(eq('u(·,t) ∈ C∞    (t > 0)',0,3.6,36,c=GREEN),tx('공간에 대해 무한 번 미분 가능',0,-3.4,27,c=GREEN))
  elif i==3:
   g.add(tx('MAXIMUM PRINCIPLE',0,4.85,22,c=MUTED),tx('같은 초기함수 · 내부 열원 없음',0,3.75,25,c=MUTED),tx('100°C',2.9,2.9,23,c=GOLD,w=1.8),tx('0°C',2.95,-1.6,23,c=BLUE,w=1.8))
   if t>=54:g.add(eq('0°C ≤ u(x,t) ≤ 100°C',0,-3,35,c=GREEN),tx('전체 공간 예시 · 그래프 끝은 표시 범위',0,-4.25,21,c=MUTED))
   else:g.add(tx('봉우리는 낮아지고 골짜기는 올라간다',0,-3.3,25,c=GREEN))
  elif i==4:
   g.add(tx('HARNACK INEQUALITY' if t>=63 else '다른 위치의 온도에도 제약이 있을까?',0,4.85,22,c=MUTED),tx('양의 해 · x ∈ ℝ · 0 < t₁ < t₂',0,4,25,c=MUTED),tx('이른 시간 t₁',-2,3.2,25,c=GOLD,w=3),tx('나중 시간 t₂',2,3.2,25,c=PURPLE,w=3))
   if t>=75:
    g.add(eq('u(y,t₂) ≥ c · u(x,t₁)',0,-1.85,35,c=GREEN),tx('미래 값의 하한',0,-2.65,25,c=GREEN))
    if t<81:g.add(eq('c = √(t₁/t₂) exp(−d²/(4κΔt))',0,-3.5,28),tx('d = |x−y|     Δt = t₂−t₁',0,-4.35,24,c=MUTED))
    elif t<84:g.add(tx('공간적 거리 d  ·  시간 간격 Δt',0,-3.5,26),tx('시각 t₁, t₂도 계수에 반영',0,-4.35,22,c=MUTED))
    else:g.add(tx('현재 값 → 다른 위치의 미래 값',0,-3.5,27),tx('양의 해가 만족하는 시공간적 제약',0,-4.35,23,c=MUTED))
   else:g.add(tx('같은 곡선 위의 두 점이 아닌',0,-2.2,27),tx('서로 다른 시각의 두 함수값',0,-3.1,29,c=GREEN))
  elif i==5:
   for y,s in [(4,'매끄러움  ·  규칙성'),(2.5,'최댓값 원리  ·  값의 범위'),(1,'하르나크  ·  시공간 관계')]:g.add(tx(s,0,y,28,c=GREEN))
   g.add(eq('∂ₜu = κΔu',0,-1,43),tx('해의 성질' if t<94 else '해를 표현하는 또 다른 방법',0,-3.2,30,c=GOLD))
  elif i==6:
   if t<108:
    g.add(tx('BROWNIAN MOTION',0,4.8,22,c=MUTED),tx('시작 위치 x',-2.3,3.45,24,c=GOLD,w=2.8),tx('경로의 가로축 = 경과 시간 s',0,-2.4,24,c=MUTED),eq('Xₛ = x + √(2κ) Bₛ',0,-3.5,32,c=GREEN),tx('가우스 증가량으로 생성한 경로 근사',0,-4.35,21,c=MUTED))
   else:
    g.add(tx('끝점 Xₜ에서 초기 함수 f를 읽는다',0,4.7,26),eq('u(x,t) = 𝔼[f(x + √(2κ) Bₜ)]',0,-3.25,32,c=GREEN),tx('표준 브라운 운동 Bₜ · 전체 실수 공간',0,-4.35,21,c=MUTED))
    if t>=117:g.add(tx('FEYNMAN–KAC · 확률적 표현의 기본 사례',0,3.65,22,c=GOLD))
  elif i==7:
   if t<139:
    g.add(tx('같은 시간에 도착한 끝점들을 모으면',0,4.75,26),tx('도착 위치',0,-.9,22,c=MUTED),eq('20 ≤ f ≤ 95  ⇒  20 ≤ 평균 ≤ 95',0,-2.3,28,c=GREEN),tx('표본의 도착 빈도 → 가우스 확률밀도' if t>=134 else '끝점의 분포 · 가중평균의 범위',0,-3.45,25,c=GREEN),eq('분산 = 2κt',0,-4.3,25,c=MUTED))
   else:
    g.add(tx('초기 함수 f와 가우스 가중치',0,4.8,26),eq('u(x,t) = ∫ Gₜ(x−y) f(y) dy',0,-3.2,30,c=GREEN),tx('주변 값의 가중평균 → 매끄러운 해',0,-4.3,25,c=GREEN))
  elif i==8:
   if t<159:
    g.add(eq('∂ₜu = κΔu',0,4.55,43,c=GREEN))
    for y,s in [(2.7,'매끄러움 · 규칙성'),(.55,'最댓값 원리 · 범위'),(-1.6,'하르나크 · 시공간 관계')]:g.add(tx(s.replace('最','최'),0,y,28,c=INK))
    g.add(tx('가우스 평균은 앞의 두 성질에 직관을 준다',0,-3.75,22,c=MUTED),tx('하르나크의 정량적 관계에는 추가 추론이 필요',0,-4.4,20,c=MUTED))
   else:
    g.add(tx('미분방정식',0,4.7,25,c=MUTED),eq('∂ₜu = κΔu,  u(x,0) = f(x)',0,3.65,33,c=GREEN),tx('확률적 표현',0,2.4,25,c=MUTED),eq('𝔼[f(x + √(2κ) Bₜ)]',0,1.4,35,c=GOLD),eq('같은 해  u(x,t)',0,-2.6,36,c=GREEN))
    if t>=167:g.add(tx('하나의 방정식, 그 해에 숨겨진 구조',0,-4.15,27))
  return g
 def geometry(self,t):
  i=self.index;g=VGroup()
  if i==1 and t>=7:
   if t<12:g.add(axes(0,3),plot(X,solution(X,.05+(t-7)*.12),0,3))
   else:
    for j,x in enumerate([-2.5,0,2.5]):
     c=VGroup(axes(0,3),plot(X,solution(X+(j-1)*1.2,.25),0,3,c=[GREEN,BLUE,PURPLE][j])).scale(.3).move_to([x,0,0]);g.add(c)
  elif i==2:
   g.add(axes(.5,4));sx,sy=step_points()
   if t<=27:g.add(plot(sx,sy,.5,4,c=GOLD))
   else:
    tt=.0008+clip((t-27)/4)*.4;g.add(plot(X,solution(X,tt),.5,4))
    if t<31:g.add(plot(sx,sy,.5,4,c=GOLD,width=1).set_opacity(.22))
    if 31<=t<35:
     x=-2.8+clip((t-31)/4)*5.6;v=float(solution(x,tt));sl=float(slope(x,tt));q=np.array([x-.35,x+.35]);g.add(plot(q,v+sl*(q-x),.5,4,c=GOLD),dot(x,v,.5,4))
  elif i==3:
   tt=.4+clip((t-46)/8)*1.5;g.add(axes(.6,4),dash(2.6,GOLD),dash(-1.4,BLUE),plot(X,solution(X,tt),.6,4))
   if t>=54:g.add(Rectangle(width=7.1,height=4,stroke_width=0,fill_color=GREEN,fill_opacity=.05).move_to([0,.6,0]))
  elif i==4:
   t1=.25;t2=.9;x=-1.2;y=1.15 if t<81 else 1.15+.6*np.sin((t-81)*.8);u1=float(solution(x,t1));u2=float(solution(y,t2))
   g.add(axes(.95,3.3),plot(X,solution(X,t1),.95,3.3,c=GOLD),plot(X,solution(X,t2),.95,3.3,c=PURPLE))
   a=dot(x,u1,.95,3.3,c=GOLD);b=dot(y,u2,.95,3.3,c=PURPLE);g.add(a,b,tx('A',a.get_x()-.3,a.get_y()+.45,24,c=GOLD,w=1),tx('B',b.get_x()+.3,b.get_y()+.45,24,c=PURPLE,w=1))
   if t>=75:g.add(tx(f'A={u1:.1f}   B={u2:.1f}   하한={lower(x,y,t1,t2):.1f}',0,-.98,23,c=MUTED))
  elif i==5 and t>=94:g.add(Dot([0,-1.9,0],radius=.09,color=GOLD))
  elif i==6:
   if t<108:
    g.add(Line([-3.55,-1.4,0],[3.55,-1.4,0],color=MUTED,stroke_width=1))
    progress=clip((t-98)/4);count=1 if t<102 else min(12,1+int((t-102)*2))
    for j in range(count):
     frac=progress if count==1 else (1 if j<count-1 else clip((t-102)*2%1));n=max(2,int(frac*N)+1)
     xs=np.linspace(-3.4,3.4,N+1)[:n];ys=.8+PATHS[j,:n]*.9
     p=np.column_stack((xs,ys,np.zeros(n)));g.add(VMobject(stroke_color=[GREEN,BLUE,PURPLE][j%3],stroke_width=2 if j==count-1 else 1,stroke_opacity=1 if j==count-1 else .3).set_points_as_corners(p))
     if j==count-1:g.add(Dot(p[-1],radius=.075,color=GOLD))
   else:
    sx,sy=step_points();g.add(axes(1.1,3.4),plot(sx,sy,1.1,3.4,c=GREEN));n=7 if t<112 else min(60,7+int((t-112)*11))
    for j in range(min(n,20)):
     x=ENDPOINTS[j];v=float(initial(x));p=dot(x,v,1.1,3.4,c=GOLD,r=.052);g.add(p,DashedLine([x*7.1/9,-.6,0],p.get_center(),color=GOLD,stroke_width=1,dash_length=.07))
    mean=float(np.mean(initial(ENDPOINTS[:n])));exact=float(solution(0,T))
    if t>=112:g.add(tx(f'{n}개 표본 평균 ≈ {mean:.1f}',0,-1.5,27,c=GOLD),tx(f'기댓값 u(0,t) = {exact:.1f}',0,-2.25,25,c=GREEN))
  elif i==7:
   if t<139:
    n=min(1200,20+int(clip((t-122)/12)*1180));ends=ENDPOINTS[:n];g.add(axes(1.7,3))
    if t<127:
     for j,x in enumerate(ends[:100]):g.add(Dot([x*7.1/9,.25+(j%4)*.11,0],radius=.035,color=GOLD))
    else:
     hist,edges=np.histogram(ends,bins=np.linspace(-4.5,4.5,25),density=False);dens=hist/(n*(edges[1]-edges[0]))
     for a,b,v in zip(edges,edges[1:],dens):
      height=max(.005,v*4.4);g.add(Rectangle(width=(b-a)*7.1/9*.92,height=height,stroke_width=0,fill_color=BLUE,fill_opacity=.45).move_to([(a+b)/2*7.1/9,.2+height/2,0]))
    if t>=134:g.add(plot(X,kernel(X,T),1.7,3,yr=3/4.4,c=GREEN))
   else:
    sx,sy=step_points();g.add(axes(2.7,2.2),plot(sx,sy,2.7,2.2,c=GOLD,width=2))
    x=-3.3+clip((t-139)/6)*6.6;weights=kernel(X-x,T);g.add(plot(X,weights,.1,1.8,yr=.65,c=BLUE),tx('가우스 가중치',0,-1.25,22,c=BLUE))
    g.add(dot(x,float(solution(x,T)),2.7,2.2,c=GREEN))
    if t>=142:
     mask=X<=x;g.add(plot(X[mask],solution(X[mask],T),2.7,2.2,c=GREEN,width=4))
  elif i==8:
   if t<159:
    for y,kind in [(1.8,0),(-.35,1),(-2.5,2)]:
     g.add(plot(X,solution(X,.45 if kind<2 else .9),y,1,w=5,c=GREEN if kind<2 else PURPLE))
     if kind==1:g.add(Line([-2.5,y+.5,0],[2.5,y+.5,0],color=GOLD,stroke_width=1),Line([-2.5,y-.5,0],[2.5,y-.5,0],color=BLUE,stroke_width=1))
   else:
    if t<163:
     for x,c in [(-1.8,GREEN),(1.8,GOLD)]:g.add(plot(X,solution(X,T),-1,1.6,w=3,c=c).shift(RIGHT*x))
    else:
     shift=1.8*(1-clip((t-163)/3))
     for x,c in [(-shift,GREEN),(shift,GOLD)]:g.add(plot(X,solution(X,T),-1,1.6,w=3,c=c).shift(RIGHT*x))
  return g
