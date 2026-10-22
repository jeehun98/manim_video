"""Discover singular directions by measurements; all geometry comes from one matrix."""
import json,math,textwrap
from pathlib import Path
import numpy as np
from manim import *
config.background_color='#09121F';config.frame_width=128/9;config.frame_height=8
FONT='Malgun Gothic';INK='#EDF4FC';MUTED='#8EA3BA';BLUE_IN='#64AEFF';TEAL='#51D9C5';GOLD='#FFD077';PURPLE='#BC9AFF'
ROOT=Path(__file__).resolve().parent
SENTENCES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['sentences']
def text(s,n=23,c=INK):return Text(s,font=FONT,font_size=n,color=c,line_spacing=1.1)
def rot(d):
 a=math.radians(d);return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
MATRIX=rot(60)@np.diag([2.,.5])@rot(-30)
V1=rot(30)[:,0];V2=rot(30)[:,1];U1=rot(60)[:,0];U2=rot(60)[:,1]
def blend(a,b,t):return a+(b-a)*smooth(float(np.clip(t,0,1)))
def angle(t):
 if t<9:return blend(0,90,t/7)
 if t<12:return 90
 if t<21:return blend(0,90,(t-12)/9)
 if t<26:return 45
 if t<27:return blend(45,0,t-26)
 if t<32:return 0
 if t<45:return (t-32)*360/13
 if t<46:return blend(360,390,t-45)
 if t<47:return 390
 if t<48:return blend(390,480,t-47)
 if t<49:return 480
 if t<51:return blend(120,30,(t-49)/2)
 if t<53:return 30
 if t<55:return blend(30,120,(t-53)/2)
 if t<66:return 120
 if t<70:return 0
 if t<75:return (t-70)*180/5
 if t<78:return 180+(t-75)*180/3
 if t<80:return blend(360,390,(t-78)/2)
 if t<89:return 30
 if t<91:return blend(30,120,(t-89)/2)
 if t<93:return 120
 if t<105:return 30
 if t<108:return blend(30,120,(t-105)/3)
 if t<120:return 30
 if t<124:return 30
 if t<129:return 120
 if t<140:return 30
 if t<142:return blend(30,75,(t-140)/2)
 return 75

def values(t):
 a=math.radians(angle(t));x=np.array([math.cos(a),math.sin(a)]);m=np.diag([1.,.1]) if t<27 else MATRIX
 return x,m@x

def trace_fraction(t):
 if t<70:return 0
 if t<75:return (t-70)/10
 return min(1,.5+(t-75)/6)

class DirectionScene(Scene):
 start_time=0;end_time=154
 def construct(self):
  clock=ValueTracker(self.start_time);now=lambda:clock.get_value();self.add(clock)
  self.add(text('행렬이 가장 잘 구별하는 방향은 어디일까?',32).move_to([0,3.43,0]),text('관측 실험  /  02     방향별 반응을 측정하다',15,MUTED).move_to([0,3.87,0]),Line([-6.65,2.98,0],[6.65,2.98,0],color='#25364B',stroke_width=1))
  L=np.array([-3.65,.48,0]);R=np.array([3.65,.48,0]);unit=.88
  def world(o,v):return o+unit*np.array([*v,0])
  for o,col in [(L,BLUE_IN),(R,TEAL)]:
   self.add(RoundedRectangle(width=5.45,height=3.8,corner_radius=.16,stroke_color='#2A3D54',stroke_width=1.1,fill_color='#101E2D',fill_opacity=1).move_to(o+[0,.06,0]))
   for k in [-2,-1,0,1,2]:
    self.add(Line(o+[-2.25*unit,k*.8*unit,0],o+[2.25*unit,k*.8*unit,0],color='#203247',stroke_width=.65))
   self.add(Arrow(o+[-2.3*unit,0,0],o+[2.3*unit,0,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.022),Arrow(o+[0,-1.6*unit,0],o+[0,1.85*unit,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.025),text('1',14,MUTED).move_to(o+[unit,-.17,0]))
  self.add(text('입력 공간   /   변화의 크기 = 1',21,BLUE_IN).move_to([-3.65,2.7,0]),text('출력 공간   /   관측한 반응',21,TEAL).move_to([3.65,2.7,0]))
  circle=DashedVMobject(Circle(radius=unit,fill_opacity=0,color=BLUE_IN,stroke_width=1.3),num_dashes=55).move_to(L)
  circle.add_updater(lambda m:m.set_stroke(opacity=.7 if now()>=12 else 0));self.add(circle)
  self.add(RoundedRectangle(width=1.02,height=1.32,corner_radius=.12,fill_color='#142337',fill_opacity=1,stroke_color='#425772').move_to([0,.55,0]),text('행렬 A',20).move_to([0,.84,0]),Arrow([-.48,-.34,0],[.48,-.34,0],buff=0,color=TEAL,stroke_width=2))
  old=text('가로 ×1\n세로 ×0.1',13,MUTED).move_to([0,.3,0]);old.add_updater(lambda m:m.set_opacity(1 if now()<27 else 0));self.add(old)
  new=text('새 행렬\n이후 고정',14,TEAL).move_to([0,.3,0]);new.add_updater(lambda m:m.set_opacity(1 if now()>=27 else 0));self.add(new)
  # Output trace is computed in advance for reproducibility but cannot appear before measurement.
  def outpoint(theta):return world(R,MATRIX@np.array([math.cos(theta),math.sin(theta)]))
  whole=VMobject().set_points_as_corners([outpoint(t) for t in np.linspace(0,TAU,721)]).set_stroke(TEAL,width=2.5)
  trail=whole.copy()
  def update_trail(m):
   f=trace_fraction(now());m.pointwise_become_partial(whole,0,max(f,1e-7));m.set_stroke(opacity=0 if now()<70 else .2 if now()>=129 else .85)
  trail.add_updater(update_trail);self.add(trail)
  # Extreme response pairs, keeping unit input directions distinct from scaled outputs.
  for i,(v,u,s,col) in enumerate([(V1,U1,2,GOLD),(V2,U2,.5,PURPLE)],1):
   vi=Arrow(L,world(L,v),buff=0,color=col,stroke_width=3,max_tip_length_to_length_ratio=.14)
   yo=Arrow(R,world(R,s*u),buff=0,color=col,stroke_width=3,tip_length=.13,max_tip_length_to_length_ratio=.2)
   def active():return (49<=now()<62) or now()>=102
   vi.add_updater(lambda m:m.set_opacity(.9 if active() else 0));self.add(vi)
   yo.add_updater(lambda m:m.set_opacity(.9 if active() and now()<140 else 0));self.add(yo)
   vi_label=text(f'{30 if i==1 else 120}°',16,col).move_to(world(L,v)+[.22,.16 if i==1 else .23,0]);vi_label.add_updater(lambda m:m.set_opacity(1 if active() else 0));self.add(vi_label)
   # Output axes are axes in OUTPUT space, not copied input angles.
   axis=DashedLine(world(R,-s*u),world(R,s*u),color=col,stroke_width=1.8,dash_length=.09)
   axis.add_updater(lambda m,i=i:m.set_opacity(.75 if (86<=now()<129 and (i==1 or now()>=89)) else 0));self.add(axis)
   ol=text(f'{60 if i==1 else 150}°',15,col).move_to(world(R,s*u)+[.2,.13,0]);ol.add_updater(lambda m:m.set_opacity(1 if 86<=now()<129 else 0));self.add(ol)
   # u_i is a unit direction. The whole output vector is sigma_i times that unit direction.
   marker=Circle(radius=.04,color=col,fill_opacity=0,stroke_width=2).move_to(world(R,u))
   marker.add_updater(lambda m:m.set_stroke(opacity=1 if 108<=now()<129 else 0));self.add(marker)
   unit_label=text(('u₁' if i==1 else 'u₂')+' (길이 1)',12,col).move_to(world(R,u)+[-.5 if i==1 else -.4,.18,0])
   unit_label.add_updater(lambda m:m.set_opacity(1 if 108<=now()<129 else 0));self.add(unit_label)
  # Right angle mark in the selected input basis.
  p=L+unit*.15*np.array([*(V1+V2),0]);q1=L+unit*.15*np.array([*V1,0]);q2=L+unit*.15*np.array([*V2,0])
  right=VMobject().set_points_as_corners([q1,p,q2]).set_stroke(MUTED,width=1.2)
  right.add_updater(lambda m:m.set_stroke(opacity=1 if 49<=now()<62 or now()>=102 else 0));self.add(right)
  def endpoint(o,index):return world(o,values(now())[index])
  for o,index,col in [(L,0,BLUE_IN),(R,1,TEAL)]:
   arrow=Arrow(o,endpoint(o,index),buff=0,color=col,stroke_width=3,max_tip_length_to_length_ratio=.12)
   def update_arrow(m,o=o,index=index):
    m.put_start_and_end_on(o,endpoint(o,index));m.set_opacity(0 if index==1 and 62<=now()<66 or index==1 and now()>=140 else .85)
   arrow.add_updater(update_arrow)
   dot=Dot(endpoint(o,index),radius=.045,color=col);dot.add_updater(lambda m,o=o,index=index:m.move_to(endpoint(o,index)).set_opacity(0 if index==1 and 62<=now()<66 or index==1 and now()>=140 else 1))
   self.add(arrow,Dot(o,color=MUTED,radius=.04),dot,text('A',15,MUTED).move_to(o+[-.17,-.2,0]))
   lab=text('B',17,col);lab.add_updater(lambda m,o=o,index=index:m.move_to(endpoint(o,index)+np.array([.16,-.2,0] if now()>=49 else [.16,.13,0])).set_opacity(0 if (index==1 and (now()>=140 or 62<=now()<66)) or (index==0 and now()>=140) else 1));self.add(lab)
  # Readouts are rounded measurements at 5 Hz; moving vectors always use the full frame clock.
  cache={}
  def cached(label,n,c):
   key=(label,n,c)
   if key not in cache:cache[key]=text(label,n,c)
   return cache[key].copy()
  for o,index,col in [(L,0,BLUE_IN),(R,1,TEAL)]:
   read=VGroup(text(' ',18))
   def update_read(m,o=o,index=index,col=col):
    t=math.floor(now()*5)/5;x,y=values(t)
    label=f'입력 거리 1.000   /   θ ≈ {angle(t)%360:.0f}°' if index==0 else f'출력 거리 ≈ {np.linalg.norm(y):.2f}'
    m.become(cached(label,18,col).move_to(o+[0,-1.72,0]))
   read.add_updater(update_read);self.add(read)
  # Distance-vs-input-angle graph: only lengths, never a trace of output positions.
  GX=-5.65;GW=11.3;GY=-2.46;GH=.47
  graph_bg=RoundedRectangle(width=13,height=1.15,corner_radius=.1,fill_color='#102135',fill_opacity=1,stroke_width=0).move_to([0,-2.01,0]);self.add(graph_bg)
  graph_items=VGroup(Line([GX,GY,0],[GX+GW,GY,0],color=MUTED,stroke_width=1),text('출력\n거리',12,MUTED).move_to([-6.2,-1.94,0]))
  for d in [0,90,180,270,360]:graph_items.add(text(str(d)+'°',12,MUTED).move_to([GX+GW*d/360,GY-.17,0]))
  def gp(deg):
   a=math.radians(deg);dist=np.linalg.norm(MATRIX@np.array([math.cos(a),math.sin(a)]));return np.array([GX+GW*deg/360,GY+GH*dist,0])
  full=VMobject().set_points_as_corners([gp(d) for d in np.linspace(0,360,721)]).set_stroke(TEAL,width=2)
  measure=full.copy()
  def update_graph(m):
   frac=1 if now()>=45 else np.clip((now()-32)/13,0,1)
   m.pointwise_become_partial(full,0,max(frac,1e-7));m.set_stroke(opacity=1 if 35<=now()<66 else .2 if 66<=now()<108 else 0)
  measure.add_updater(update_graph);self.add(measure)
  graph_items.add_updater(lambda m:m.set_opacity(1 if 35<=now()<66 else .25 if 66<=now()<108 else 0));self.add(graph_items)
  for d,lab,col in [(30,'최대 2.0',GOLD),(120,'최소 0.5',PURPLE)]:
   dot=Dot(gp(d),radius=.045,color=col);label=text(lab,16,col).move_to(gp(d)+[.9,.02,0]);g=VGroup(dot,label);g.add_updater(lambda m:m.set_opacity(1 if 45<=now()<66 else 0));self.add(g)
  # Exact symbolic definitions; never label a length-2 arrow as a unit u-vector.
  term_v=text('vᵢ  오른쪽 특이벡터\n입력의 단위 방향',20,BLUE_IN).move_to([-4.1,-1.93,0]);term_v.add_updater(lambda m:m.set_opacity(1 if now()>=108 else 0));self.add(term_v)
  term_u=text('uᵢ  왼쪽 특이벡터\n출력의 단위 방향',20,TEAL).move_to([4.1,-1.93,0]);term_u.add_updater(lambda m:m.set_opacity(1 if now()>=111 else 0));self.add(term_u)
  term_s=text('σᵢ  특잇값\n변화의 배율',20,GOLD).move_to([0,-1.93,0]);term_s.add_updater(lambda m:m.set_opacity(1 if now()>=114 else 0));self.add(term_s)
  for lo,hi,label,col in [(0,9,'기준 실험: diag(1, 0.1)  /  같은 입력 거리 · 다른 출력 거리',MUTED),(9,12,'가장 잘 구별되는 방향은 어디일까?',INK),(12,27,'입력의 변화 크기 = 1    /    바뀌는 것은 방향뿐',BLUE_IN),(27,35,'새로운 행렬 A    /    비스듬한 방향도 측정한다',TEAL),(35,45,'길이만 측정한다 · 출력 끝점의 궤적은 아직 기록하지 않는다',MUTED),(45,62,'최대 입력 방향 30° → 거리 2    /    최소 입력 방향 120° → 거리 0.5',GOLD),(62,70,'출력 거리 측정 → 출력 위치도 기록',TEAL),(70,78,'같은 행렬 · 같은 단위 입력 · 끝점 기록 중',TEAL),(78,86,'타원은 미리 정한 그림이 아니라, 측정해서 얻은 결과',INK),(86,93,'출력의 장축 60°    /    출력의 단축 150°',GOLD),(93,102,'출력의 방향 ≠ 그 출력을 만든 입력의 방향',INK),(102,108,'입력 30° ↔ 출력 60°    /    입력 120° ↔ 출력 150°',GOLD),(108,120,'단위 입력 vᵢ → 실제 출력 σᵢuᵢ    /    σ₁ = 2,  σ₂ = 0.5',INK),(120,124,'A v₁ = 2 u₁',GOLD),(124,129,'A v₂ = 0.5 u₂',PURPLE),(129,140,'같은 크기의 변화를 시험해, 가장 강한 반응과 가장 약한 반응을 찾았다',INK),(140,149,'임의의 입력 x · 두 직교 방향의 성분을 함께 가진다',BLUE_IN),(149,154,'방향별 성분들을 어떻게 하나의 출력으로 만들까?',INK)]:
   mob=text(label,20,col).move_to([0,-2.88,0]);mob.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(mob)
  # Project an arbitrary input onto the TWO RIGHT singular directions only.
  arbitrary=np.array([math.cos(math.radians(75)),math.sin(math.radians(75))])
  for v,col in [(V1,GOLD),(V2,PURPLE)]:
   component=float(arbitrary@v)*v
   proj=Line(L,world(L,component),color=col,stroke_width=4)
   drop=DashedLine(world(L,arbitrary),world(L,component),color=col,stroke_width=1.3,dash_length=.06)
   proj.add_updater(lambda m:m.set_opacity(.85 if now()>=145 else 0))
   drop.add_updater(lambda m:m.set_opacity(.8 if now()>=145 else 0))
   self.add(proj,drop)
  xlab=text('x',21,BLUE_IN);xlab.add_updater(lambda m:m.move_to(endpoint(L,0)+[.2,.18,0]).set_opacity(1 if now()>=140 else 0));self.add(xlab)
  # Focus question at 9–12 seconds; independent of the narration subtitle below.
  veil=Rectangle(width=13,height=3.8,fill_color='#09121F',fill_opacity=.9,stroke_width=0).move_to([0,.55,0]);question=text('가장 잘 구별되는 방향은 어디일까?',35).move_to([0,.6,0])
  veil.add_updater(lambda m:m.set_opacity(.94 if 9<=now()<12 else 0));question.add_updater(lambda m:m.set_opacity(1 if 9<=now()<12 else 0));self.add(veil,question)
  self.add(Rectangle(width=14.23,height=.87,fill_color='#070D16',fill_opacity=1,stroke_width=0).move_to([0,-3.55,0]))
  for rec in SENTENCES:
   if rec['end']<=self.start_time or rec['start']>=self.end_time:continue
   cap=text('\n'.join(textwrap.wrap(rec['text'],49)),21).move_to([0,-3.52,0])
   if cap.width>13.1:cap.scale_to_fit_width(13.1)
   if cap.height>.73:cap.scale_to_fit_height(.73)
   cap.add_updater(lambda m,r=rec:m.set_opacity(1 if r['start']<=now()<r['end'] else 0));self.add(cap)
  self.update_mobjects(0)
  self.play(clock.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)
