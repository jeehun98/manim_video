"""Exact-clock, dual-layout vector animation. No external raster assets or TeX."""
import os,json,textwrap
from pathlib import Path
import numpy as np
from functools import lru_cache
from manim import *
R=Path(__file__).resolve().parent
VERT=os.getenv('INTRINSIC_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16
config.frame_height=16 if VERT else 9
config.background_color='#0E1117'
INK='#F0F3F8';GRAY='#8892A0';BLUE='#4DA6FF';YELLOW='#F2C94C';GREEN='#47D7AC';EDGE='#293343';PANEL='#151C27';RED='#ED7D92'
MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'))
def text(s,size=32,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def card(s,w=3.2,h=.85,c=BLUE,size=30):
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.13,stroke_color=c,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),text(s,size,c,w-.3))
@lru_cache(maxsize=48)
def glyph(ch,color):return Text(ch,font='Consolas',font_size=35,color=color)
def number_strip(value,color):
 # Fixed cells avoid DecimalNumber/MathTex dependency and glyph overlap.
 s=f'{value:+.2f}'
 return VGroup(*[glyph(ch,color).copy().move_to([i*.24,-.14 if ch=='.' else 0,0]) for i,ch in enumerate(s)]).move_to(ORIGIN)
def net(w=6,h=3,c=GRAY):
 sizes=[4,6,6,3];pts=[[np.array([x,y,0]) for y in np.linspace(-h/2,h/2,n)] for x,n in zip(np.linspace(-w/2,w/2,4),sizes)]
 edges=VGroup(*[Line(a,b,color=c,stroke_width=1.3,stroke_opacity=.55) for p,q in zip(pts,pts[1:]) for a in p for b in q])
 nodes=VGroup(*[Dot(p,radius=.07,color=INK) for layer in pts for p in layer])
 return VGroup(edges,nodes)
class IntrinsicScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.035:raise RuntimeError(f'Overrun {self.index}: {self.time} > {target}')
  if target-self.time>.0001:self.wait(target-self.time)
 def note(self,s,c=YELLOW):
  self.notice.become(text(s,30 if VERT else 29,c,7.65 if VERT else 14).move_to([0,-4.25 if VERT else -2.35,0]))
 def pair(self,a,b):
  if VERT:a.move_to([0,2.7,0]);b.move_to([0,-.95,0])
  else:a.move_to([-3.8,.25,0]);b.move_to([3.65,.25,0])
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  top=7.25 if VERT else 3.85
  self.add(text('최소 조건 2부  /  신경망 01',22,GRAY).move_to([0,top,0]))
  titles=['모든 가중치를 따로 조정해야 할까?','신경망은 그대로, 학습 방식만 바꾸면','가중치 3개를 변수 하나로','작은 좌표에서 전체 가중치로','199,210개와 약 750개','연결은 그대로 남아 있습니다','내재 차원을 측정하는 방법','750은 보편적인 상수가 아닙니다','파라미터 수와 학습 자유도']
  self.add(text(titles[self.index],37 if VERT else 39,INK,7.8 if VERT else 14.6).move_to([0,top-.8,0]))
  self.notice=text('',26).move_to([0,-4.25 if VERT else -2.35,0]);self.add(self.notice)
  base=Line([-3.85 if VERT else -7.3,-7.2 if VERT else -4.12,0],[3.85 if VERT else 7.3,-7.2 if VERT else -4.12,0],color=EDGE,stroke_width=3)
  progress=base.copy().set_color(BLUE)
  progress.add_updater(lambda obj:obj.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/129)))
  self.add(base,progress)
  # Captions are rendered once per sentence and switched at supplied half-open boundaries.
  for row in TIMING:
   if row['end']<=self.start or row['start']>=self.end:continue
   s='\n'.join(textwrap.wrap(row['text'],width=25 if VERT else 49))
   caption=text(s,29 if VERT else 28,INK,7.75 if VERT else 14.5).move_to([0,-5.95 if VERT else -3.3,0]).set_z_index(20)
   caption.add_updater(lambda obj,r=row:obj.set_opacity(1 if r['start']-.00001<=self.start+self.time<r['end']-.00001 else 0))
   self.add(caption)
  [self.question,self.research,self.three_weights,self.projection,self.result,self.connections,self.measurement,self.conditions,self.conclusion][self.index]()
  self.at(self.end)
 def question(self):
  n=net(w=6.5 if VERT else 10,h=3.1).move_to([0,1.3 if VERT else .45,0])
  self.play(LaggedStart(Create(n[0]),FadeIn(n[1]),lag_ratio=.25),run_time=2)
  count=text('가중치 200,000개',41,BLUE).move_to([0,3.65 if VERT else 2.35,0]);self.play(FadeIn(count),run_time=.6)
  labels=VGroup(*[text(f'w{i+1} = {v:+.2f}',23,BLUE).move_to([x,y,0]) for i,(v,x,y) in enumerate([(.42,-2.3,1.2),(-.81,.1,.6),(.13,2.5,1.3)])])
  if VERT:labels.shift(UP*.8)
  self.play(FadeIn(labels),run_time=.6)
  for j in range(3):
   replacement=VGroup(*[text(f'w{i+1} = {np.sin(j*2+i):+.2f}',23,BLUE).move_to(o) for i,o in enumerate(labels)])
   self.play(Transform(labels,replacement),n[0].animate.set_color(BLUE if j%2==0 else GRAY),run_time=1.2)
  self.at(8);self.play(n.animate.set_opacity(.22),FadeOut(labels),run_time=.6)
  q=text('모두 독립적으로\n조정해야 할까?',48,YELLOW,7.3 if VERT else 12).move_to([0,.5,0]);self.play(FadeIn(q,shift=UP*.2),run_time=.9)
  self.note('파라미터 수 = 학습 자유도 ?')
 def research(self):
  paper=VGroup(text('ICLR 2018',32,GREEN),text('Measuring the Intrinsic Dimension\nof Objective Landscapes',25,INK,7.1),text('Li · Farkhoor · Liu · Yosinski',20,GRAY)).arrange(DOWN,buff=.22).move_to([0,2.9 if VERT else 1.5,0])
  self.play(FadeIn(paper),run_time=.8);self.at(18)
  n=net(6.5 if VERT else 7,2.6).move_to([0,.5 if VERT else -.25,0])
  if VERT:self.play(paper.animate.scale(.65).move_to([0,4.45,0]),FadeIn(n),run_time=.8)
  else:self.play(ReplacementTransform(paper,text('Li et al. · ICLR 2018',24,GREEN).move_to([0,2.35,0])),FadeIn(n),run_time=.8)
  number=text('D = 199,210',37,BLUE).move_to([0,2.55 if VERT else 1.65,0]);self.play(FadeIn(number),run_time=.6);self.at(22)
  controls=VGroup(*[card(f'w{i+1}',1,.55,BLUE,22) for i in range(5)]).arrange(RIGHT,buff=.15).move_to([0,-1.7,0])
  self.play(FadeIn(controls),run_time=.65);self.note('通常 학습: 각 파라미터를 독립적으로'.replace('通常','일반'));self.at(25)
  small=VGroup(*[card(f'z{i+1}',1,.55,YELLOW,22) for i in range(2)]).arrange(RIGHT,buff=.25).move_to(controls)
  self.play(ReplacementTransform(controls,small),n[0].animate.set_color(YELLOW),run_time=1)
  self.note('신경망 유지 · 학습 변수만 제한')
 def three_weights(self):
  # An explicit linear projection of R^3 preserves all coordinates of the example.
  # The displayed straight line is exactly p(t)=p0+t*(2,-1,1).
  vals=[ValueTracker(x) for x in [1,2,3]]
  colors=[BLUE,GREEN,RED]
  readouts=VGroup()
  for i,v in enumerate(vals):
   lab=text(f'w{i+1}',32,colors[i]);num=number_strip(v.get_value(),colors[i])
   row=VGroup(lab,num).arrange(RIGHT,buff=.35)
   def update_number(obj,v=v,c=colors[i]):
    obj.become(number_strip(v.get_value(),c).move_to(obj.get_center()))
   num.add_updater(update_number)
   readouts.add(row)
  readouts.arrange(DOWN,buff=.4)
  center=np.array([0,-.85,0]) if VERT else np.array([3.5,.55,0])
  origin=center+np.array([-.8,-1,0]);basis=np.array([[.55,-.08,0],[.35,.3,0],[0,.56,0]])
  def p(v):return origin+np.array(v)@basis
  axes=VGroup(*[Arrow(origin,p(np.eye(3)[i]*5),buff=0,color=colors[i],stroke_width=2,max_tip_length_to_length_ratio=.08) for i in range(3)])
  labs=VGroup(*[text(f'w{i+1}',22,colors[i]).move_to(p(np.eye(3)[i]*5)+[.15,.15,0]) for i in range(3)])
  point=Dot(p([1,2,3]),radius=.09,color=INK).set_z_index(3);point.add_updater(lambda obj:obj.move_to(p([v.get_value() for v in vals])))
  readouts.move_to([0,3.35,0] if VERT else [-4.2,.7,0])
  self.play(FadeIn(readouts),Create(axes),FadeIn(labs),FadeIn(point),run_time=.8)
  dof=text('학습 자유도 3',32,BLUE).move_to([0,-2.7,0] if VERT else [-4.2,-1.5,0]);self.at(32)
  self.play(FadeIn(dof),run_time=.4)
  for i,new in enumerate([2.3,1.1,4.1]):self.play(vals[i].animate.set_value(new),run_time=.85)
  self.play(*[v.animate.set_value(x) for v,x in zip(vals,[1,2,3])],run_time=.7)
  self.at(36)
  formula=text('w = (1, 2, 3) + t (2, −1, 1)',29,YELLOW,7.5 if VERT else 13).move_to([0,1.55 if VERT else 2,0])
  self.play(FadeIn(formula),Transform(dof,text('학습 자유도 1',32,YELLOW).move_to(dof)),run_time=.7)
  self.at(38)
  line=Line(p(np.array([1,2,3])-.65*np.array([2,-1,1])),p(np.array([1,2,3])+1.25*np.array([2,-1,1])),color=YELLOW,stroke_width=5)
  t=ValueTracker(0)
  for i,v in enumerate(vals):v.add_updater(lambda obj,i=i:obj.set_value([1,2,3][i]+[2,-1,1][i]*t.get_value()))
  self.add(*vals,t)
  track=Line(LEFT*1.7,RIGHT*1.7,color=GRAY).move_to([0,4.7,0] if VERT else [-4.2,-.85,0])
  knob=Dot(track.get_center(),color=YELLOW,radius=.09);knob.add_updater(lambda obj:obj.move_to(track.get_center()+RIGHT*t.get_value()*1.3))
  tl=text('t',27,YELLOW).next_to(track,LEFT)
  self.play(Create(line),FadeIn(VGroup(track,knob,tl)),axes.animate.set_opacity(.45),run_time=.6)
  self.play(t.animate.set_value(1),run_time=1.6,rate_func=smooth)
  self.play(t.animate.set_value(-.5),run_time=1.6,rate_func=smooth)
  self.at(43);self.note('파라미터 3개 · 학습 자유도 1개')
  self.play(t.animate.set_value(.6),run_time=2)
  self.play(Indicate(line,color=YELLOW),run_time=.8)
 def projection(self):
  dims=text('D = 199,210',45,INK).move_to([0,3.3 if VERT else 1.85,0])
  self.play(FadeIn(dims),run_time=.7)
  formula=text('θ = θ₀ + Pz',65,INK).move_to([0,1.65 if VERT else .6,0]);self.play(FadeIn(formula),run_time=.8)
  self.note('3차원 예시 → 전체 파라미터 공간');self.at(52)
  a=card('z  학습 변수',3.1,.85,BLUE);b=card('θ  전체 가중치',3.6,.85,INK)
  if VERT:a.move_to([0,-.1,0]);b.move_to([0,-2.5,0]);arrow=Arrow(a.get_bottom(),b.get_top(),color=GRAY,buff=.15)
  else:a.move_to([-4.5,-.85,0]);b.move_to([4.1,-.85,0]);arrow=Arrow(a.get_right(),b.get_left(),color=GRAY,buff=.2)
  fixed=text('P: 고정된 무작위 방향',26,GRAY,7).move_to([0,-1.25,0] if VERT else [0,-.45,0])
  self.play(FadeIn(a),GrowArrow(arrow),FadeIn(b),FadeIn(fixed),run_time=1)
  self.note('θ₀와 P는 고정 · z만 학습',BLUE)
  self.play(Indicate(a,color=BLUE),Indicate(b,color=YELLOW),run_time=1.2)
  self.at(58);self.play(*[o.animate.set_opacity(.2) for o in [a,b,arrow,fixed,formula,dims]],run_time=.5)
 def result(self):
  label=text('MNIST · 완전연결 신경망',29,GRAY).move_to([0,4.3 if VERT else 2.3,0])
  arch=text('784 → 200 → 200 → 10',30,GRAY).move_to([0,3.7 if VERT else 1.75,0])
  self.play(FadeIn(label),FadeIn(arch),run_time=.7)
  self.note('Li et al. · ICLR 2018 · MNIST',GRAY)
  a=VGroup(text('전체 파라미터',27,GRAY),text('199,210',76,INK)).arrange(DOWN,buff=.25)
  b=VGroup(text('학습 변수',27,BLUE),text('≈ 750',76,GREEN)).arrange(DOWN,buff=.25)
  self.pair(a,b)
  if VERT:a.shift(DOWN*.55)
  self.play(FadeIn(a,shift=UP*.2),run_time=1)
  self.at(63)
  # These are labelled digit illustrations, not claimed to be sampled MNIST images.
  digits=VGroup(*[text(str(i),37,GRAY).rotate((i-2)*.05) for i in [2,7,1,9,3]]).arrange(RIGHT,buff=.35).move_to([0,1.1 if VERT else -.85,0])
  self.play(FadeIn(digits),run_time=.65);self.at(66);self.play(FadeIn(b,shift=UP*.2),run_time=.8)
  self.at(69);self.note('기준 모델 정확도의 90% 이상',GREEN)
  self.at(71);self.play(FadeOut(digits),FadeOut(a),FadeOut(b),FadeOut(arch),run_time=.45)
  ratio=750/199210;barw=7 if VERT else 12
  bar=Rectangle(width=barw,height=.55,color=GRAY,fill_color=GRAY,fill_opacity=.3).move_to([0,1.1 if VERT else .8,0])
  tiny=Rectangle(width=barw*ratio,height=.55,stroke_width=0,fill_color=GREEN,fill_opacity=1).align_to(bar,LEFT).set_y(bar.get_y())
  calc=text('750 / 199,210 × 100',35,GRAY).move_to([0,-.1,0]);pct=text('≈ 0.38%',72,GREEN).move_to([0,-1.35,0])
  self.play(Create(bar),FadeIn(tiny),FadeIn(calc),FadeIn(pct),run_time=.9)
  self.note('正比例 막대: 초록 영역 = 750 / 199,210'.replace('正比例','실제 비율'),GREEN)
 def connections(self):
  left=net(5.4 if VERT else 5.5,2,c=GRAY);right=net(5.4 if VERT else 5.5,2,c=BLUE)
  self.pair(left,right)
  labels=VGroup(text('연결 제거 · 개념 비교',24,GRAY).next_to(left,UP,buff=.3),text('이번 실험: 모든 연결 유지',24,BLUE).next_to(right,UP,buff=.3))
  self.play(FadeIn(left),FadeIn(right),FadeIn(labels),run_time=.7);self.at(78)
  removed=VGroup(*list(left[0])[::3]);self.play(removed.animate.set_opacity(.05),run_time=1)
  self.at(81);self.play(right[0].animate.set_color(GREEN).set_stroke(opacity=.8),run_time=.8)
  self.note('모든 가중치는 계산에 사용됩니다',GREEN)
  self.at(84)
  control=card('z  학습 변수',2.6,.5,YELLOW,22).move_to(right.get_top()+UP*1.1)
  self.play(FadeIn(control),right[0].animate.set_color(YELLOW),run_time=.5)
  # All edges remain present; one scalar changes their visual weight together.
  for sign in [1,-1]:
   self.play(*[edge.animate.set_stroke(width=1.4+(.8+.7*np.sin(k))*sign*.5,opacity=.55+.2*np.sin(k+sign)) for k,edge in enumerate(right[0])],run_time=.8)
  self.note('줄어든 것은 학습 자유도',YELLOW)
 def chart(self):
  ax=Axes(x_range=[0,1500,750],y_range=[0,1.1,.5],x_length=6.1 if VERT else 10.5,y_length=3.7 if VERT else 2.7,tips=False,axis_config={'color':GRAY,'include_ticks':False}).move_to([0,.7 if VERT else .25,0])
  def f(x):return 1-np.exp(-x/(750/np.log(10)))
  curve=ax.plot(f,x_range=[0,1500,15],color=BLUE,stroke_width=4)
  labs=VGroup(text('기준 모델 대비 정확도',23,GRAY).next_to(ax,UP,buff=.25),text('학습 부분공간의 차원 d',24,GRAY).next_to(ax,DOWN,buff=.5),text('0',20,GRAY).next_to(ax.c2p(0,0),DOWN),text('750',20,GRAY).next_to(ax.c2p(750,0),DOWN),text('1500',20,GRAY).next_to(ax.c2p(1500,0),DOWN))
  return ax,curve,labs
 def measurement(self):
  self.note('파라미터 수 ≠ 필요한 학습 자유도')
  q=text('199,210 ≠ 750',55,YELLOW).move_to([0,2 if VERT else .5,0]);self.play(FadeIn(q),run_time=.6);self.at(89)
  self.play(FadeOut(q),run_time=.35);ax,curve,labs=self.chart()
  self.play(Create(ax),FadeIn(labs),run_time=.75);self.play(Create(curve),run_time=3.5)
  self.note('개념도 · 원문 측정 곡선의 복원이 아님',GRAY);self.at(96)
  threshold=DashedLine(ax.c2p(0,.9),ax.c2p(1500,.9),color=GREEN,dash_length=.12)
  tag=text('기준 성능의 90%',23,GREEN).next_to(threshold,UP,buff=.13).align_to(ax,RIGHT)
  self.play(Create(threshold),FadeIn(tag),run_time=.9);self.at(100)
  marker=Dot(ax.c2p(750,.9),radius=.095,color=YELLOW)
  drop=DashedLine(ax.c2p(750,0),ax.c2p(750,.9),color=YELLOW)
  self.play(Create(drop),FadeIn(marker),run_time=.65)
  self.note('내재 차원 d_int90 ≈ 750',YELLOW)
  self.play(Circumscribe(marker,color=YELLOW),run_time=.9)
 def conditions(self):
  ax,curve,labs=self.chart();self.add(ax,curve,labs)
  self.note('개념도 · 조건에 따라 달라지는 곡선',GRAY)
  curves=VGroup(*[ax.plot(lambda x,k=k:1-np.exp(-x/k),x_range=[0,1500,15],color=c,stroke_width=3) for k,c in [(180,GREEN),(580,YELLOW),(950,RED)]])
  self.play(Create(curves),run_time=1.5)
  self.at(109)
  tags=VGroup(*[card(s,2.15,.65,c,25) for s,c in [('모델 구조',BLUE),('데이터',GREEN),('성능 기준',YELLOW)]]).arrange(RIGHT,buff=.2).move_to([0,3.8 if VERT else 2.1,0])
  self.play(LaggedStart(*[FadeIn(t) for t in tags],lag_ratio=.3),run_time=1.3)
  self.at(113);self.play(FadeOut(curves),FadeOut(curve),FadeOut(ax),FadeOut(labs),run_time=.8)
  message=text('파라미터의 수와\n학습에 필요한 자유도는\n다를 수 있습니다',43,INK,7.5 if VERT else 13).move_to([0,.5,0]);self.play(FadeIn(message),run_time=.8)
 def conclusion(self):
  rng=np.random.default_rng(18)
  cloud=VGroup(*[Dot([x,y,0],radius=.025,color=GRAY).set_opacity(.55) for x,y in rng.uniform([-3,-1.2],[3,2.8],(180,2))])
  if not VERT:cloud.stretch(1.7,0).shift(DOWN*.3)
  self.play(FadeIn(cloud),run_time=.8)
  self.note('네트워크의 크기: 전체 파라미터 수',GRAY);self.at(119)
  direction=Line([-2.7,-.7,0],[2.7,2.3,0],color=YELLOW,stroke_width=5)
  if not VERT:direction.stretch(1.7,0).shift(DOWN*.3)
  point=Dot(direction.get_start(),color=GREEN,radius=.1)
  self.play(Create(direction),FadeIn(point),cloud.animate.set_opacity(.22),run_time=.7)
  self.play(MoveAlongPath(point,direction),run_time=2.2)
  self.note('더 적은 독립 변수로 학습할 가능성',GREEN);self.at(124)
  self.play(FadeOut(cloud),FadeOut(direction),FadeOut(point),run_time=.5)
  question=text('문제를 해결하는 데 필요한\n진짜 차원은\n무엇으로 결정될까요?',46,YELLOW,7.7 if VERT else 13).move_to([0,.8,0])
  self.play(FadeIn(question,shift=UP*.15),run_time=.9);self.note('파라미터 수 ≠ 학습 자유도',GRAY)
