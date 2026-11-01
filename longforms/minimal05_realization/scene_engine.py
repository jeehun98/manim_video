"""Minimal realization with independent output trajectories and equal-scale state axes."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from data_model import *
ROOT=Path(__file__).resolve().parent
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B78';YELLOW='#F3D277';BLUE='#75A7FF';BLUE2='#A5C4FF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def box(s,width=6,height=1,color=YELLOW,size=30):return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.13,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.35))

def original(t=None):
 out=VGroup();u=txt('u',34,TEAL).move_to(LEFT*2.8)
 s1=box('x₁',2.45,.9,BLUE,34).move_to(UP*.75);s2=box('x₂',2.45,.9,BLUE2,34).move_to(DOWN*.75)
 if t is not None:
  s1[1].become(always_redraw(lambda:txt(f'x₁ = {state(t.get_value())[0]:.2f}',29,BLUE,2.1).move_to(UP*.75)))
  s1[1].add_updater(lambda m:m.become(txt(f'x₁ = {state(t.get_value())[0]:.2f}',29,BLUE,2.1).move_to(UP*.75)))
  s2[1].add_updater(lambda m:m.become(txt(f'x₂ = {state(t.get_value())[1]:.2f}',29,BLUE2,2.1).move_to(DOWN*.75)))
 out.add(u,s1,s2)
 for s in [s1,s2]:out.add(Arrow(LEFT*2.45,s.get_left(),buff=.12,color=TEAL,stroke_width=2),Arrow(s.get_right(),RIGHT*2.35,buff=.12,color=YELLOW,stroke_width=2))
 out.add(Circle(radius=.24,color=YELLOW).move_to(RIGHT*2.6),txt('+',28,YELLOW).move_to(RIGHT*2.6),txt('y',30,YELLOW).move_to(RIGHT*3.15))
 return out

def reduced_diagram():
 return VGroup(txt('u',34,TEAL).move_to(LEFT*2.8),box('z',2.8,1,YELLOW,42),Arrow(LEFT*2.4,LEFT*1.5,buff=.05,color=TEAL,stroke_width=2),Arrow(RIGHT*1.5,RIGHT*2.5,buff=.05,color=YELLOW,stroke_width=2),txt('y = z',30,YELLOW).move_to(RIGHT*3.2))

def chart(center,width=6.4,height=2.5,yrange=(-1,3),duration=8):
 ax=Axes(x_range=[0,duration,1],y_range=[yrange[0],yrange[1],1],x_length=width,y_length=height,tips=False,axis_config={'include_ticks':False,'color':EDGE,'stroke_width':1.5}).move_to(center)
 labels=VGroup()
 for t in [0,2,4,6,8]:
  if t<=duration:labels.add(txt(str(t),17,MUTED).move_to(ax.c2p(t,yrange[0])+DOWN*.2))
 for y in [yrange[0],0,yrange[1]]:labels.add(txt(f'{y:g}',17,MUTED).move_to(ax.c2p(0,y)+LEFT*.25))
 labels.add(txt('t',21,MUTED).move_to(ax.c2p(duration,yrange[0])+RIGHT*.2))
 return VGroup(ax,labels),ax

def path_from(ax,values,color,width=4):return VMobject(color=color,stroke_width=width).set_points_as_corners([ax.c2p(t,v) for t,v in zip(TIME[::4],values[::4])]).set_z_index(2 if color==YELLOW else 1)

def state_axes(center=None):
 center=([0,.7,0] if VERT else [-3.5,.15,0]) if center is None else center
 side=4.3 if VERT else 3.25
 ax=Axes(x_range=[-2,2,1],y_range=[-2,2,1],x_length=side,y_length=side,tips=False,axis_config={'include_ticks':False,'color':MUTED,'stroke_width':1.5}).move_to(center)
 labels=VGroup(txt('x₁',24,BLUE).move_to(ax.c2p(2,0)+RIGHT*.25),txt('x₂',24,BLUE2).move_to(ax.c2p(0,2)+UP*.25),txt('0',18,MUTED).move_to(ax.c2p(0,0)+LEFT*.16+DOWN*.16))
 su=Line(ax.c2p(-1.6,-1.6),ax.c2p(1.6,1.6),color=YELLOW,stroke_width=4);di=DashedLine(ax.c2p(-1.6,1.6),ax.c2p(1.6,-1.6),color=RED,stroke_width=3,dash_length=.12)
 return VGroup(ax,labels),ax,su,di

class RealizationScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=YELLOW):self.notice.become(txt(s,27 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):self.cond.become(box(s,7 if VERT else 12,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   05',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2)
  progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=YELLOW,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/154))))
  self.add(track,progress);getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  self.condition('내부 상태 2개')
  t=ValueTracker(0);cards=VGroup(box('x₁ = 1.50',3.2,1.25,BLUE,33),box('x₂ = 0.50',3.2,1.25,BLUE2,33)).arrange(RIGHT,buff=.35).move_to([0,1.3 if VERT else .5,0]);self.add(cards)
  for j in [0,1]:
   cards[j][1].add_updater(lambda m,j=j:m.become(txt(f'x{["₁","₂"][j]} = {state(t.get_value())[j]:.2f}',33,[BLUE,BLUE2][j],2.8).move_to(cards[j][0])))
  self.note('시스템을 설명하는 상태도 반드시 두 개일까?');self.play(t.animate.set_value(1),run_time=5.7,rate_func=linear)
  self.at(6);self.play(FadeOut(cards),run_time=.5)
  diagram=original().move_to([0,1.1 if VERT else .2,0]);self.play(FadeIn(diagram),run_time=.8);self.note('입력 u → 내부 상태 → 출력 y',TEAL)
 def part_01(self):
  self.condition('초기값은 달라도 · 변화 법칙은 같다')
  diagram=original().move_to([0,1.5 if VERT else .35,0]);self.add(diagram)
  eq=box('ẋ₁ = −x₁ + u\nẋ₂ = −x₂ + u',7 if VERT else 6,1.55,BLUE,34).move_to([0,-1.1 if VERT else .2,0])
  if not VERT:diagram.shift(LEFT*3.7);eq.shift(RIGHT*3.6)
  self.play(FadeIn(eq),run_time=.7);self.note('각 상태가 같은 입력 u를 받는다',TEAL)
  self.at(16);self.play(Indicate(diagram[0],color=TEAL),Indicate(eq,color=TEAL),run_time=.8);self.note('출력 y = x₁ + x₂ · 두 상태의 합')
  self.at(21);self.play(Indicate(diagram[-1],color=YELLOW),run_time=.7)
 def part_02(self):
  self.condition('내부 상태를 달리해도 · 같은 합이면 같은 출력')
  a=box('x₁ = 1.5',3.2,1.1,BLUE,34);b=box('x₂ = 0.5',3.2,1.1,BLUE2,34);pair=VGroup(a,b).arrange(RIGHT,buff=.35).move_to([0,2 if VERT else .8,0]);self.add(pair)
  total=box('y = 2',6.5,1.35,YELLOW,49).move_to([0,-.25 if VERT else -.8,0]);self.add(total)
  self.note('이 예시에서는 출력의 시간 변화로도 차이를 구별할 수 없다',MUTED)
  self.at(27);self.play(Transform(a,box('x₁ = 1.2',3.2,1.1,BLUE,34).move_to(a)),Transform(b,box('x₂ = 0.8',3.2,1.1,BLUE2,34).move_to(b)),run_time=1)
  self.at(30);self.note('두 상태를 따로 추적할 필요가 있을까?')
 def part_03(self):
  self.condition('새로운 상태 z를 정의')
  pair=VGroup(box('x₁',3,1.1,BLUE,42),box('x₂',3,1.1,BLUE2,42)).arrange(RIGHT,buff=.4).move_to([0,1.5 if VERT else .5,0]);self.add(pair)
  self.at(35);target=box('z = x₁ + x₂',7 if VERT else 9,1.3,YELLOW,42).move_to(pair)
  self.play(ReplacementTransform(pair,target),run_time=1.1);self.note('두 상태를 더한 값을 하나의 새 상태로')
  self.at(38);eq=box('ẋ₁ + ẋ₂ = (−x₁ + u) + (−x₂ + u)',7 if VERT else 13,1.1,BLUE,31).move_to([0,-1.1 if VERT else -.9,0]);self.play(FadeIn(eq),run_time=.8);self.note('원래 두 변화 방정식을 더한다')
 def part_04(self):
  self.condition('z 자신과 입력만으로 변화가 정해진다')
  eq=box('ż = (−x₁ + u) + (−x₂ + u)',7 if VERT else 12,1.25,BLUE,35).move_to([0,1.7 if VERT else .8,0]);self.add(eq)
  self.play(Transform(eq,box('ż = −(x₁ + x₂) + 2u',7 if VERT else 12,1.25,YELLOW,38).move_to(eq)),run_time=.9)
  self.play(Transform(eq,box('ż = −z + 2u',7 if VERT else 12,1.25,YELLOW,45).move_to(eq)),run_time=.9);self.note('닫힌 상태 방정식 · x₁과 x₂를 따로 알 필요 없음')
  self.at(45);out=box('y = z',6.5,1.1,YELLOW,45).move_to([0,-.6 if VERT else -.8,0]);self.play(FadeIn(out),run_time=.6)
 def part_05(self):
  self.condition('같은 입력 u(t) · z(0) = x₁(0) + x₂(0) = 2')
  centers=([-1.8,2.0,0],[1.8,2.0,0]) if VERT else ([-3.6,1.1,0],[3.6,1.1,0])
  left=original().scale(.44 if VERT else .55).move_to(centers[0]);right=reduced_diagram().scale(.44 if VERT else .55).move_to(centers[1]);self.add(left,right)
  self.add(txt('원래 · 상태 2개',23,BLUE).move_to(np.array(centers[0])+UP*.8),txt('축소 · 상태 1개',23,YELLOW).move_to(np.array(centers[1])+UP*.8))
  t=ValueTracker(0)
  ulabel=always_redraw(lambda:txt(f'같은 입력 u = {input_value(t.get_value()):.2f}',25,TEAL).move_to([0,3.8 if VERT else 1.92,0]));self.add(ulabel)
  spark_center=np.array([0,3.45 if VERT else 1.4,0])
  def upoint(ti):return spark_center+RIGHT*(-1.15+2.3*ti/8)+UP*((input_value(ti)-.5)*.17)
  spark=VMobject(color=TEAL,stroke_width=2).set_points_as_corners([upoint(ti) for ti in TIME])
  cursor=Dot(color=TEAL,radius=.04);cursor.add_updater(lambda m:m.move_to(upoint(t.get_value())));self.add(spark,cursor)
  base,ax=chart([0,-.65 if VERT else -.7,0],6.5 if VERT else 12.8,2.35 if VERT else 1.5,(-1,3));self.add(base)
  full_a=path_from(ax,Y_ORIGINAL,BLUE,8);full_b=path_from(ax,Y_REDUCED,YELLOW,5)
  ca=VMobject(color=BLUE,stroke_width=8).set_z_index(1);cb=DashedVMobject(full_b,num_dashes=50,equal_lengths=False).set_z_index(2)
  ca.add_updater(lambda m:m.pointwise_become_partial(full_a,0,max(.0001,t.get_value()/8)))
  for j,dash in enumerate(cb):dash.add_updater(lambda m,j=j:m.set_stroke(opacity=1 if t.get_value()/8 >= (j+1)/50 else 0))
  self.add(ca,cb)
  for j,values,col in [(0,Y_ORIGINAL,BLUE),(1,Y_REDUCED,YELLOW)]:
   loc=np.array([centers[j][0],1.12 if VERT else .2,0])
   self.add(always_redraw(lambda values=values,col=col,loc=loc:txt(f'y = {np.interp(t.get_value(),TIME,values):.3f}',22,col).move_to(loc)))
  self.note('x₁(0)=1.5 · x₂(0)=0.5 · z(0)=2',MUTED)
  self.play(t.animate.set_value(3),run_time=6.5,rate_func=linear)
  self.at(54);self.note('파랑: 원래 출력 · 노랑 점선: 축소 출력 · 정확히 중첩')
  self.play(t.animate.set_value(8),run_time=6.5,rate_func=linear)
 def part_06(self):
  self.condition('단순 삭제와 상태 결합은 다르다')
  pair=VGroup(box('x₁',3,1.1,BLUE,42),box('x₂',3,1.1,BLUE2,42)).arrange(RIGHT,buff=.4).move_to([0,1.6 if VERT else .6,0]);self.add(pair)
  cross=Cross(pair[1],stroke_color=RED,stroke_width=5);self.play(Create(cross),run_time=.6);self.note('x₂만 버리면 원래 출력 y = x₁ + x₂를 재현하지 못한다',RED)
  self.at(65);self.play(FadeOut(cross),run_time=.4)
  target=box('z = x₁ + x₂',7 if VERT else 10,1.3,YELLOW,43).move_to(pair);self.play(ReplacementTransform(pair,target),run_time=1.1)
  self.add(box('ż = −z + 2u    ·    y = z',7 if VERT else 12,1.1,YELLOW,32).move_to([0,-.7 if VERT else -.9,0]));self.note('필요한 두 상태의 합을 새 좌표로 보존한다')
 def part_07(self):
  self.condition('입출력 관계 유지 · 상태 차원 최소화')
  self.add(txt('Minimal Realization',37,YELLOW,7 if VERT else 13).move_to([0,3 if VERT else 1.7,0]))
  diagram=reduced_diagram().move_to([0,.8 if VERT else .2,0]);self.add(diagram);self.note('최소 실현 · 외부 동작을 설명하는 가장 작은 상태')
  self.at(76);cards=VGroup(box('입출력 관계 유지',6.5 if VERT else 5.7,1,YELLOW,31),box('상태 차원 최소화',6.5 if VERT else 5.7,1,TEAL,31)).arrange(DOWN if VERT else RIGHT,buff=.3).move_to([0,-1.6 if VERT else -1,0]);self.play(FadeIn(cards),run_time=.7)
 def part_08(self):
  self.condition('어떤 내부 방향이 외부 동작에 필요한가?')
  self.add(original().scale(1 if VERT else .85).move_to([0,1.4 if VERT else .8,0]));self.note('입력에서 상태로 · 상태에서 출력으로',MUTED)
  self.at(86);cards=VGroup(box('입력 → 상태',3.3 if VERT else 5,.95,TEAL,30),box('상태 → 출력',3.3 if VERT else 5,.95,YELLOW,30)).arrange(RIGHT,buff=.3).move_to([0,-1.5 if VERT else -.9,0]);self.play(FadeIn(cards),run_time=.65)
 def part_09(self):
  self.condition('제어 가능성 · Controllability')
  base,ax,su,di=state_axes();self.add(base,su,di.set_opacity(.2));self.note('이 예시에서 입력은 합 방향 (1, 1)을 움직인다',TEAL)
  label=box('입력 u → 상태 변화',6.6 if VERT else 6,1,TEAL,30).move_to([0,-2.45,0] if VERT else [3.5,.7,0]);self.add(label)
  self.at(92);dot=Dot(ax.c2p(0,0),color=TEAL,radius=.1);self.add(dot)
  self.play(dot.animate.move_to(ax.c2p(1.2,1.2)),run_time=1.4);self.play(dot.animate.move_to(ax.c2p(-.7,-.7)),run_time=1.4)
  if not VERT:self.add(txt('입력으로 움직일 수 있는 방향',25,TEAL,6).move_to([3.5,-.5,0]))
 def part_10(self):
  self.condition('관측 가능성 · Observability')
  base,ax,su,di=state_axes();self.add(base,su,di)
  p=Dot(ax.c2p(1.5,.5),color=BLUE,radius=.09);q=Dot(ax.c2p(1.2,.8),color=BLUE2,radius=.09);self.add(p,q,DashedLine(ax.c2p(0,2),ax.c2p(2,0),color=RED,dash_length=.08,stroke_width=2))
  self.add(box('서로 다른 상태\n같은 합 y = 2',6.6 if VERT else 6,1.2,YELLOW,31).move_to([0,-2.45,0] if VERT else [3.5,.6,0]));self.note('차이 방향으로 달라도 · 출력 전체로 구별되지 않는다',RED)
  self.at(100);self.play(Indicate(p,color=YELLOW),Indicate(q,color=YELLOW),run_time=.7)
 def part_11(self):
  self.condition('차이 d = x₁ − x₂ · 입력에 영향받지 않음')
  base,ax,su,di=state_axes();self.add(base,su.set_opacity(.2),di)
  eq=box('d = x₁ − x₂\nḋ = −d',6.6 if VERT else 6,1.3,RED,34).move_to([0,-2.4,0] if VERT else [3.5,.7,0]);self.add(eq)
  self.note('차이 방향 (1, −1) · 합 방향과 직교',RED)
  self.at(108);dot=Dot(ax.c2p(1.3,-1.3),color=RED,radius=.1);self.add(dot)
  self.play(dot.animate.move_to(ax.c2p(1.3*np.exp(-2),-1.3*np.exp(-2))),run_time=3,rate_func=lambda a:(1-np.exp(-2*a))/(1-np.exp(-2)))
  self.note('d는 스스로 감쇠 · 입력항 없음 · 출력 y에도 없음',RED)
 def part_12(self):
  self.condition('합 z = x₁ + x₂ · 입력과 출력을 연결')
  base,ax,su,di=state_axes();self.add(base,su,di.set_opacity(.18))
  eq=box('ż = −z + 2u\ny = z',6.6 if VERT else 6,1.3,YELLOW,35).move_to([0,-2.4,0] if VERT else [3.5,.7,0]);self.add(eq)
  self.note('합 방향 (1, 1) · 입력에 반응하고 출력에 직접 나타난다')
  dot=Dot(ax.c2p(.2,.2),color=YELLOW,radius=.1);self.add(dot);self.play(dot.animate.move_to(ax.c2p(1.3,1.3)),run_time=3)
  self.at(118);self.play(FadeOut(di),run_time=.5);self.note('외부 동작을 재현하는 데 필요한 상태: z 하나')
 def part_13(self):
  self.condition('유한차원 선형 시불변 시스템 · LTI')
  a=box('제어 가능',6.5 if VERT else 5.5,1.1,TEAL,36);b=box('관측 가능',6.5 if VERT else 5.5,1.1,YELLOW,36)
  pair=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.35).move_to([0,1.8 if VERT else .9,0]);self.add(pair)
  result=box('두 조건 모두 충족 → 최소 실현',7 if VERT else 12,1,YELLOW,31).move_to([0,-.6 if VERT else -.7,0]);self.play(FadeIn(result),run_time=.8);self.note('축소된 1차 시스템: 입력 계수 2 · 출력 계수 1',MUTED)
 def part_14(self):
  self.condition('일반적 동등성 기준: 영 초기 상태의 입출력 관계')
  pair=VGroup(box('원래 · 상태 2개\nG(s) = 2 / (s + 1)',7 if VERT else 6,1.5,BLUE,31),box('축소 · 상태 1개\nG(s) = 2 / (s + 1)',7 if VERT else 6,1.5,YELLOW,31)).arrange(DOWN if VERT else RIGHT,buff=.4).move_to([0,1.4 if VERT else .8,0]);self.add(pair)
  self.note('같은 전달함수 · 일반적으로 x(0) = 0을 기준으로')
  self.at(135);extra=box('이번 예시: z(0) = x₁(0) + x₂(0)이면\n영 초기 상태가 아니어도 출력 일치',7 if VERT else 12,1.2,YELLOW,27).move_to([0,-1.5 if VERT else -.95,0]);self.play(FadeIn(extra),run_time=.7);self.note('모든 내부 상태의 복원을 보장한다는 뜻은 아님',MUTED)
 def part_15(self):
  self.condition('내부 변수 수와 최소 독립 상태 차원은 다르다')
  pair=VGroup(box('x₁',3.1,1.05,BLUE,40),box('x₂',3.1,1.05,BLUE2,40)).arrange(RIGHT,buff=.35).move_to([0,2.5 if VERT else 1.2,0]);self.add(pair)
  base,ax=chart([0,-1 if VERT else -.7,0],6.4 if VERT else 11.5,2 if VERT else 1.4,(-1,3));self.add(base,path_from(ax,Y_ORIGINAL,BLUE,8),DashedVMobject(path_from(ax,Y_REDUCED,YELLOW,5),num_dashes=40));self.note('같은 입출력 관계를 유지하는 데 필요한 독립 상태는?')
  self.at(146);target=box('z = x₁ + x₂',7 if VERT else 9,1.1,YELLOW,41).move_to(pair);self.play(ReplacementTransform(pair,target),run_time=1.1)
  self.note('이 시스템의 최소 상태 차원은 1',YELLOW)
