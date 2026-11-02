"""Dual-layout mathematical animation with exact user-supplied speech clock."""
import json,os,textwrap
from pathlib import Path
from functools import lru_cache
import numpy as np
from manim import *
R=Path(__file__).resolve().parent
VERT=os.getenv('INTRINSIC_LAYOUT','longform')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0D1117'
INK='#E5EDF5';GRAY='#8294AA';BLUE='#4DA6FF';YELLOW='#F2C94C';ORANGE='#FF8C69';GREEN='#47D7AC';PANEL='#151D29';EDGE='#293645'
MANIFEST=json.loads((R/'manifest.json').read_text(encoding='utf-8'));TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'))
def text(s,size=30,c=INK,width=None):
 o=Text(s,font='Malgun Gothic',font_size=size,color=c,line_spacing=1.15)
 if width and o.width>width:o.scale_to_fit_width(width)
 return o
def card(s,w=3,h=.8,c=BLUE,size=29):return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.13,color=c,stroke_width=1.4,fill_color=PANEL,fill_opacity=1),text(s,size,c,w-.3))
@lru_cache(maxsize=48)
def glyph(ch,c):return Text(ch,font='Consolas',font_size=33,color=c)
def digits(v,c):return VGroup(*[glyph(ch,c).copy().move_to([i*.23,-.13 if ch=='.' else 0,0]) for i,ch in enumerate(f'{v:+.2f}')]).move_to(ORIGIN)
def readout(tracker,c):
 o=digits(tracker.get_value(),c);o.last_value=f'{tracker.get_value():+.2f}'
 def update(m):
  value=f'{tracker.get_value():+.2f}'
  if value!=m.last_value:m.become(digits(tracker.get_value(),c).move_to(m));m.last_value=value
 o.add_updater(update);return o
def network(w=6,h=2,sizes=(4,6,6,3)):
 ps=[[np.array([x,y,0]) for y in np.linspace(-h/2,h/2,n)] for x,n in zip(np.linspace(-w/2,w/2,len(sizes)),sizes)]
 edges=VGroup(*[Line(a,b,color=GRAY,stroke_width=1.2,stroke_opacity=.45) for p,q in zip(ps,ps[1:]) for a in p for b in q])
 layers=VGroup(*[VGroup(*[Dot(p,radius=.07,color=INK) for p in layer]) for layer in ps]);return VGroup(edges,layers)
def outputs(values,vertical=False):
 out=VGroup()
 for i,(v,c) in enumerate(zip(values,[BLUE,GREEN,ORANGE])):
  node=VGroup(Circle(radius=.25,color=c,fill_color=PANEL,fill_opacity=1),text(str(i+1),22,c))
  value=VGroup(text(f'h{i+1} =',27,c),readout(v,c)).arrange(RIGHT,buff=.15)
  row=VGroup(node,value).arrange(RIGHT if vertical else DOWN,buff=.28);out.add(row)
 return out.arrange(DOWN if vertical else RIGHT,buff=.65)
def curve_model(center,width=6.1,height=3.8):
 ax=ThreeDAxes(x_range=[-1.3,1.3,1],y_range=[-.3,1.6,1],z_range=[-1.8,1.8,1],x_length=4.3,y_length=3.2,z_length=3.9,axis_config={'color':GRAY,'include_ticks':False,'stroke_width':1.5,'include_tip':False})
 ax.rotate(66*DEGREES,axis=RIGHT).rotate(-32*DEGREES,axis=OUT)
 curve=ParametricFunction(lambda t:ax.c2p(t,t*t,t*t*t),t_range=[-1.1,1.1,.015],color=BLUE,stroke_width=4.5)
 labs=VGroup(*[text(s,21,GRAY).move_to(axis.get_end()+UP*.2) for s,axis in zip(['h1','h2','h3'],[ax.x_axis,ax.y_axis,ax.z_axis])])
 model=VGroup(ax,curve,labs);model.scale_to_fit_width(width)
 if model.height>height:model.scale_to_fit_height(height)
 model.move_to(center);return model,ax,curve,labs
LAYER_Y=[.18,.42,.95,.78,.56,.35,.2]
class RepresentationScene(ThreeDScene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.035:raise RuntimeError(f'Overrun {self.index}: {self.time} > {target}')
  if target-self.time>.0001:self.wait(target-self.time)
 def note(self,s,c=YELLOW):self.notice.become(text(s,29,c,7.7 if VERT else 14).move_to([0,-4.25 if VERT else -2.35,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  top=7.25 if VERT else 3.85
  self.add(text('최소 조건 2부  /  신경망 02',22,GRAY).move_to([0,top,0]))
  titles=['뉴런 4,096개 = 독립적인 정보 4,096개?','2019년, 표현의 차원을 측정하다','세 뉴런이 출력하는 세 숫자','하나의 t가 세 출력을 결정한다','좌표는 3개, 내재 차원은 1','계층에 따라 달라지는 측정 차원','표현의 확장과 정리라는 해석','2026년, 측정 방법을 다시 묻다','점의 위치로 차원을 알아낼 수 있을까?','측정 차원과 실제 차원을 구분해야','저차원 구조의 존재와 차원 추정','우리는 무엇을 세고 있을까?']
  self.add(text(titles[self.index],36 if VERT else 39,INK,7.85 if VERT else 14.7).move_to([0,top-.8,0]))
  self.notice=text('',25);self.add(self.notice)
  base=Line([-3.85 if VERT else -7.3,-7.2 if VERT else -4.12,0],[3.85 if VERT else 7.3,-7.2 if VERT else -4.12,0],color=EDGE,stroke_width=3)
  progress=base.copy().set_color(BLUE);progress.add_updater(lambda o:o.put_start_and_end_on(base.get_start(),base.get_start()+RIGHT*max(.001,base.width*(self.start+self.time)/153)))
  self.add(base,progress)
  for row in TIMING:
   if row['end']<=self.start or row['start']>=self.end:continue
   s='\n'.join(textwrap.wrap(row['text'],width=25 if VERT else 49))
   caption=text(s,29 if VERT else 28,INK,7.75 if VERT else 14.5).move_to([0,-5.95 if VERT else -3.3,0]).set_z_index(20)
   caption.add_updater(lambda o,r=row:o.set_opacity(1 if r['start']-.00001<=self.start+self.time<r['end']-.00001 else 0));self.add(caption)
  [self.opening,self.research2019,self.three_outputs,self.curve,self.definition,self.layers,self.interpretation,self.research2026,self.sampling,self.estimated_true,self.structure,self.question][self.index]()
  self.at(self.end)
 def opening(self):
  n=network(6.4 if VERT else 10,2.8).move_to([0,1.5 if VERT else .3,0]);self.play(LaggedStart(Create(n[0]),FadeIn(n[1]),lag_ratio=.2),run_time=1.6)
  count=text('4,096 neurons',53,BLUE).move_to([0,3.65 if VERT else 2.25,0]);self.play(FadeIn(count),run_time=.7)
  self.at(4)
  h=VGroup(*[card(f'h{i+1}',1.1,.55,BLUE,23) for i in range(3)]).arrange(RIGHT,buff=.3).move_to([0,-.8 if VERT else -1.3,0])
  self.play(FadeIn(h),n[1].animate.set_color(BLUE),run_time=.5);self.note('独立적인 정보도 4,096개일까?'.replace('独立','독립'))
 def research2019(self):
  p=VGroup(text('Intrinsic Dimension of Data Representations\nin Deep Neural Networks',26,INK,7.4 if VERT else 13),text('Ansuini et al. · NeurIPS 2019',25,BLUE)).arrange(DOWN,buff=.3).move_to([0,3.85 if VERT else 1.95,0])
  self.play(FadeIn(p),run_time=.7)
  rng=np.random.default_rng(19)
  matrix=VGroup(*[Square(side_length=.19,stroke_width=0,fill_color=interpolate_color(ManimColor(PANEL),ManimColor(BLUE),float(v)),fill_opacity=1).move_to([x*.25,y*.25,0]) for (y,x),v in np.ndenumerate(rng.uniform(.1,1,(6,10)))])
  matrix.move_to([0,1 if VERT else -.25,0]);self.play(LaggedStart(*[FadeIn(x) for x in matrix],lag_ratio=.01),run_time=1)
  self.note('학습을 마친 신경망의 내부 표현',GRAY);self.at(12)
  comparison=VGroup(card('뉴런의 개수',3,.75,GRAY),text('≫',45,YELLOW),card('측정 차원',3,.75,YELLOW)).arrange(DOWN if VERT else RIGHT,buff=.25).move_to([0,-1.6 if VERT else -.65,0])
  self.play(FadeOut(matrix),FadeIn(comparison),run_time=.7);self.note('훨씬 낮은 측정 차원',YELLOW)
  self.at(16);self.play(FadeOut(comparison),run_time=.3)
  self.play(FadeIn(text('차원이란 무엇일까?',43,YELLOW).move_to([0,.2,0])),run_time=.6)
 def three_outputs(self):
  vals=[ValueTracker(v) for v in [.2,.6,.9]];out=outputs(vals,vertical=not VERT).move_to([0,2 if VERT else .25,0] if VERT else [-3.7,.25,0])
  self.play(LaggedStart(*[FadeIn(o) for o in out],lag_ratio=.2),run_time=1)
  dof=card('독립 변수 3개',4,.9,BLUE,34).move_to([0,-1.5,0] if VERT else [3.7,.25,0]);self.at(22);self.play(FadeIn(dof),run_time=.5)
  for i,v in enumerate(vals):self.play(v.animate.set_value([.85,-.35,.4][i]),run_time=.85)
  self.note('각 출력을 따로 변경할 수 있습니다',BLUE)
 def core(self):
  t=ValueTracker(.2);vals=[ValueTracker(.2**i) for i in [1,2,3]]
  for i,v in enumerate(vals,1):v.add_updater(lambda o,i=i:o.set_value(t.get_value()**i))
  self.add(t,*vals)
  out=outputs(vals,vertical=not VERT).move_to([0,3.35,0] if VERT else [-4,.35,0])
  formula=text('h1 = t    h2 = t²    h3 = t³',30,BLUE,7.7 if VERT else 13).move_to([0,4.7 if VERT else 2.15,0])
  track=Line(LEFT*1.9,RIGHT*1.9,color=GRAY).move_to([0,1.9,0] if VERT else [-4,-1.45,0])
  knob=Dot(color=BLUE,radius=.085);knob.add_updater(lambda o:o.move_to(track.get_center()+RIGHT*t.get_value()*1.5));tl=text('t',29,BLUE).next_to(track,LEFT)
  return t,vals,out,formula,VGroup(track,knob,tl)
 def curve(self):
  t,vals,out,formula,track=self.core();self.play(FadeIn(out),FadeIn(formula),run_time=.7)
  self.play(FadeIn(track),run_time=.6);self.note('하나의 변수 t',BLUE);self.at(33)
  self.play(t.animate.set_value(1),run_time=1.4);self.play(t.animate.set_value(-.8),run_time=1.5)
  self.at(37)
  model,ax,curve,labs=curve_model([0,-.75,0] if VERT else [3.75,.2,0],6.5,3.7)
  point=Dot3D(ax.c2p(t.get_value(),t.get_value()**2,t.get_value()**3),radius=.075,color=INK,resolution=(4,4))
  point.add_updater(lambda o:o.move_to(ax.c2p(t.get_value(),t.get_value()**2,t.get_value()**3)))
  self.play(Create(ax),FadeIn(labs),FadeIn(point),run_time=.7)
  self.play(Create(curve),t.animate.set_value(1.05),run_time=2.4,rate_func=linear)
  self.play(t.animate.set_value(.85),run_time=.5)
  self.note('세 좌표 · 하나의 독립 변수',GREEN)
 def definition(self):
  model,ax,curve,labs=curve_model([0,-.75,0] if VERT else [3.75,.2,0],6.5,3.7)
  self.add(model,Dot3D(ax.c2p(.85,.85**2,.85**3),radius=.075,color=INK,resolution=(4,4)))
  a=VGroup(text('출력 공간의 차원',28,GRAY),text('3',70,GRAY)).arrange(DOWN,buff=.15)
  b=VGroup(text('곡선의 내재 차원',28,BLUE),text('1',70,BLUE)).arrange(DOWN,buff=.15)
  cards=VGroup(a,b).arrange(RIGHT if VERT else DOWN,buff=.75).move_to([0,3.35,0] if VERT else [-4,.3,0])
  self.play(FadeIn(cards),run_time=.5)
  for axis in ax:self.play(Indicate(axis,color=GRAY),run_time=.5)
  self.at(45);self.play(ax.animate.set_opacity(.2),labs.animate.set_opacity(.35),curve.animate.set_stroke(width=6),run_time=.8)
  self.note('Intrinsic Dimension = 1',BLUE)
 def layer_chart(self):
  ax=Axes(x_range=[0,6,1],y_range=[0,1.1,.5],x_length=6.35 if VERT else 10.7,y_length=3.35 if VERT else 2.2,tips=False,axis_config={'color':GRAY,'include_ticks':False}).move_to([0,-.1 if VERT else -.15,0])
  labels=VGroup(text('측정된 내재 차원',25,YELLOW).next_to(ax,UP,buff=.25),text('초기층',23,GRAY).next_to(ax.c2p(0,0),DOWN,buff=.2),text('후반층',23,GRAY).next_to(ax.c2p(6,0),DOWN,buff=.2))
  pts=[ax.c2p(i,y) for i,y in enumerate(LAYER_Y)]
  segments=VGroup(*[Line(a,b,color=YELLOW,stroke_width=4) for a,b in zip(pts,pts[1:])]);dots=VGroup(*[Dot(p,radius=.07,color=YELLOW) for p in pts])
  return ax,labels,segments,dots
 def layer_net(self):return network(6.2 if VERT else 10.5,1.35 if VERT else .8,sizes=(3,4,4,4,4,3,2)).move_to([0,3.65 if VERT else 1.95,0])
 def layers(self):
  n=self.layer_net();ax,labs,segs,dots=self.layer_chart();self.play(FadeIn(n),Create(ax),FadeIn(labs),run_time=.8)
  self.at(53);self.add(dots[0]);self.play(n[1][0].animate.set_color(BLUE),run_time=.3)
  for i,seg in enumerate(segs):self.play(Create(seg),FadeIn(dots[i+1]),n[1][i+1].animate.set_color(BLUE if i<2 else GREEN),run_time=.75)
  self.at(59);self.note('표현 확장 → 표현 정리',BLUE)
  self.play(Indicate(VGroup(*list(segs)[:2]),color=BLUE),Indicate(VGroup(*list(segs)[2:]),color=GREEN),run_time=1.3)
 def interpretation(self):
  n=self.layer_net();ax,labs,segs,dots=self.layer_chart();self.add(n,ax,labs,segs,dots)
  self.play(VGroup(*list(segs)[:2]).animate.set_color(BLUE),run_time=.7)
  self.note('초기층: 표현 확장',BLUE);self.at(68)
  self.play(VGroup(*list(segs)[2:]).animate.set_color(GREEN),run_time=.7);self.note('후반층: 필요한 특징을 선택하고 정리',GREEN)
  self.at(71);self.play(n.animate.set_opacity(.2),segs.animate.set_opacity(.35),dots.animate.set_opacity(.35),run_time=.6)
  q=card('정말 차원이 변한 것일까?',6.6,1,YELLOW,34).move_to([0,3.5 if VERT else 1.95,0]);self.play(FadeIn(q),run_time=.6)
 def research2026(self):
  p=VGroup(text('Rethinking Intrinsic Dimension Estimation\nin Neural Representations',27,INK,7.4 if VERT else 13),text('Schulte & Rügamer · AISTATS 2026',25,ORANGE)).arrange(DOWN,buff=.3).move_to([0,3.4 if VERT else 1.6,0])
  years=VGroup(card('2019 · 측정 결과',3.3,.85,YELLOW,26),text('→',40,GRAY),card('2026 · 추정 방법',3.3,.85,ORANGE,26)).arrange(DOWN if VERT else RIGHT,buff=.25).move_to([0,.4 if VERT else -.25,0])
  self.play(FadeIn(p),FadeIn(years),run_time=.8);self.at(79)
  self.play(FadeOut(years),run_time=.4);est=card('Estimator · 차원 추정',5.4,.9,YELLOW,32).move_to([0,.4,0]);self.play(FadeIn(est),run_time=.6)
  self.at(82)
  if VERT:self.play(FadeOut(est),p.animate.scale(.7).move_to([0,4.4,0]),run_time=.6)
  else:self.play(FadeOut(est),ReplacementTransform(p,text('Schulte & Rügamer · AISTATS 2026',24,ORANGE).move_to([0,2.25,0])),run_time=.6)
  model,ax,curve,labs=curve_model([0,.25,0],7 if VERT else 9,4 if VERT else 3)
  samples=VGroup(*[Dot(ax.c2p(t,t*t,t*t*t),radius=.045,color=INK) for t in np.linspace(-1.1,1.1,22)])
  self.play(Create(curve),FadeIn(samples),run_time=.7);self.play(curve.animate.set_stroke(opacity=.07),run_time=1)
  self.note('点の位置 → 차원의 추정'.replace('点の位置','점의 위치'),YELLOW);self.at(87)
  q=text('차원 = ?',57,YELLOW).move_to([0,-2.7 if VERT else -1.5,0]);self.play(FadeIn(q),run_time=.8)
 def sampling(self):
  center=np.array([0,1.5,0] if VERT else [-1.4,.45,0]);w=6.4 if VERT else 9
  line=Line(center+LEFT*w/2,center+RIGHT*w/2,color=BLUE,stroke_width=4)
  rng=np.random.default_rng(26);xs=np.linspace(-w/2,w/2,24);offset=rng.uniform(-.65,.65,24)
  points=VGroup(*[Dot(center+RIGHT*x,radius=.06,color=INK) for x in xs]);self.play(Create(line),FadeIn(points),run_time=.8)
  box=card('차원 추정',3.1,.85,YELLOW,32).move_to([0,-1.4,0] if VERT else [5.45,.45,0]);self.play(FadeIn(box),run_time=.5)
  self.note('점들 사이의 기하학적 관계',GRAY);self.at(95)
  guides=VGroup(*[DashedLine(center+RIGHT*x,center+RIGHT*x+UP*y,color=ORANGE,dash_length=.07,stroke_width=1.2) for x,y in zip(xs,offset)])
  self.play(*[p.animate.shift(UP*y) for p,y in zip(points,offset)],Create(guides),run_time=1.6)
  neighbors=VGroup(Line(points[10].get_center(),points[11].get_center(),color=YELLOW,stroke_width=4),Line(points[10].get_center(),points[12].get_center(),color=YELLOW,stroke_width=3))
  halo=Circle(radius=.45,color=YELLOW,stroke_width=2).move_to(points[10]);self.play(Create(neighbors),Create(halo),run_time=.7)
  self.note('작은 위치 변화도 거리 관계를 바꿉니다',ORANGE);self.at(101)
  self.play(FadeOut(guides),FadeOut(neighbors),FadeOut(halo),run_time=.3)
  fewer=VGroup(*[Dot(center+RIGHT*x,radius=.065,color=INK) for x in np.linspace(-w/2,w/2,9)])
  self.play(ReplacementTransform(points,fewer),run_time=.6);self.note('표본 수 · 데이터 분포',YELLOW)
  dense=VGroup(*[Dot(center+RIGHT*x+UP*y,radius=.045,color=INK) for x,y in zip(np.r_[np.linspace(-w/2,0,28),np.linspace(.2,w/2,8)],rng.uniform(-.13,.13,36))])
  self.play(ReplacementTransform(fewer,dense),run_time=.8)
 def estimated_true(self):
  ax,labs,segs,dots=self.layer_chart();self.play(Create(ax),FadeIn(labs),Create(segs),FadeIn(dots),run_time=1.1)
  self.note('추정기는 실제 기하학적 차원을 추적할까?',ORANGE)
  self.at(109);self.play(Indicate(VGroup(segs,dots),color=YELLOW),run_time=1.1)
  self.at(113)
  estimated=card('측정된 내재 차원',5.1,.8,YELLOW,31).move_to([0,3.65 if VERT else 2.15,0]);self.play(FadeIn(estimated),run_time=.7)
  self.at(118);self.play(VGroup(ax,labs,segs,dots).animate.scale(.75).move_to([0,.7 if VERT else -.15,0]),run_time=.6)
  actual=card('실제 차원 = ?',4.2,.85,BLUE,33).move_to([0,-2.1,0] if VERT else [4.4,-1.35,0])
  self.play(FadeIn(actual),run_time=.6);self.note('측정값의 변화만으로 단정할 수 없습니다',ORANGE)
  self.play(Indicate(estimated,color=YELLOW),Indicate(actual,color=BLUE),run_time=.9)
 def structure(self):
  center=[0,.7,0] if VERT else [0,.2,0];model,ax,curve,labs=curve_model(center,7.2 if VERT else 9,4 if VERT else 3)
  points=VGroup(*[Dot(ax.c2p(t,t*t,t*t*t),radius=.047,color=INK) for t in np.linspace(-1.1,1.1,24)])
  self.play(FadeIn(model),run_time=.7);self.note('저차원 구조는 존재할 수 있습니다',GREEN);self.at(129)
  self.play(FadeIn(points),curve.animate.set_stroke(opacity=.08),ax.animate.set_opacity(.2),labs.animate.set_opacity(.2),run_time=.9)
  self.note('구조 자체와 그 구조에 대한 추정',GREEN);self.at(134)
  self.play(FadeOut(model),FadeOut(points),run_time=.4)
  left,lax,lcurve,llabs=curve_model([0,2.5,0] if VERT else [-4,.35,0],5.5,2.9)
  right,rax,rcurve,rlabs=curve_model([0,-1.1,0] if VERT else [4,.35,0],5.5,2.9)
  right.remove(rcurve);rax.set_opacity(.15);rlabs.set_opacity(.15)
  samples=VGroup(*[Dot(rax.c2p(t,t*t,t*t*t),radius=.055,color=INK) for t in np.linspace(-1.1,1.1,20)])
  tl=text('구조를 아는 경우',29,BLUE).move_to([0,4.45,0] if VERT else [-4,2.2,0])
  tr=text('표본에서 추정하는 경우',29,YELLOW).move_to([0,.6,0] if VERT else [4,2.2,0])
  self.play(FadeIn(left),FadeIn(right),FadeIn(samples),FadeIn(tl),FadeIn(tr),run_time=1)
  self.note('뉴런 수 ≠ 실제 차원 ≠ 추정 차원',GREEN)
 def question(self):
  cards=VGroup(*[card(s,6.6 if VERT else 4.1,1.2,c,33) for s,c in [('뉴런의 개수',GRAY),('독립적인 변수',BLUE),('추정 방법의 숫자',YELLOW)]])
  cards.arrange(DOWN if VERT else RIGHT,buff=.6 if VERT else .45).move_to([0,1.2 if VERT else .55,0]);self.play(FadeIn(cards),run_time=.7)
  neuron=network(1.1,.7,sizes=(2,3,2))
  curve=ParametricFunction(lambda t:np.array([.45*t,.3*t*t,.2*t*t*t]),t_range=[-1,1,.03],color=BLUE,stroke_width=3)
  samples=VGroup(*[Dot([x,y,0],radius=.045,color=INK) for x,y in [(-.4,-.15),(-.2,.15),(0,-.1),(.2,.05),(.4,.2)]])
  icons=VGroup(neuron,curve,samples)
  for i,icon in enumerate(icons):
   if VERT:
    icon.scale(.7).move_to(cards[i].get_left()+RIGHT*.7)
    cards[i][1].shift(RIGHT*.35).scale(.9)
   else:icon.move_to(cards[i].get_center()+UP*1.4)
  self.play(FadeIn(icons),run_time=.5)
  self.at(143);self.play(Indicate(VGroup(cards[0],icons[0]),color=INK),run_time=.65)
  self.at(145);self.play(Indicate(VGroup(cards[1],icons[1]),color=BLUE),run_time=.8)
  self.at(148);self.play(Indicate(VGroup(cards[2],icons[2]),color=YELLOW),run_time=.65)
  self.at(150);self.play(FadeOut(cards),FadeOut(icons),run_time=.35)
  q=text('신경망의 진짜 차원은\n과연 몇 개일까요?',49,GREEN,7.7 if VERT else 13).move_to([0,1 if VERT else .5,0]);self.play(FadeIn(q,shift=UP*.15),run_time=.6)
