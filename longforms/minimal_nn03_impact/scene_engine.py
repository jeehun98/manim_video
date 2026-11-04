"""Actual matrix cells, computed activations and loss-direction examples."""
import os,json,textwrap
from pathlib import Path
import numpy as np
from manim import *
R=Path(__file__).resolve().parent;D=np.load(R/'demonstration_data.npz')
VERT=os.getenv('INTRINSIC_LAYOUT','longform')=='shorts';config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0D1117'
INK='#E5EDF5';GRAY='#8294AA';BLUE='#4DA6FF';YELLOW='#F2C94C';ORANGE='#FF8C69';GREEN='#47D7AC';RED='#E76875';PANEL='#151D29';EDGE='#293645'
M=json.loads((R/'manifest.json').read_text(encoding='utf-8'));TIMING=json.loads((R/'timing.json').read_text(encoding='utf-8'))
def text(s,size=30,c=INK,width=None):
 o=Text(s,font='Malgun Gothic',font_size=size,color=c,line_spacing=1.15)
 if width and o.width>width:o.scale_to_fit_width(width)
 return o
def card(s,w=3,h=.8,c=BLUE,size=29):return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.13,color=c,stroke_width=1.4,fill_color=PANEL,fill_opacity=1),text(s,size,c,w-.3))
def grid(a,cell=.28,c=BLUE,limit=None):
 a=np.asarray(a);a=a[:,None] if a.ndim==1 else a
 limit=max(float(np.max(abs(a))),.001) if limit is None else limit
 out=VGroup(*[Square(side_length=cell*.87,stroke_width=0,fill_color=interpolate_color(ManimColor(PANEL),ManimColor(c if v>=0 else RED),min(1,abs(float(v))/limit)),fill_opacity=1).move_to([j*cell,-i*cell,0]) for (i,j),v in np.ndenumerate(a)])
 return out.move_to(ORIGIN)
def network(w=6,h=2):
 sizes=[4,6,6,3];ps=[[np.array([x,y,0]) for y in np.linspace(-h/2,h/2,n)] for x,n in zip(np.linspace(-w/2,w/2,4),sizes)]
 return VGroup(VGroup(*[Line(a,b,color=GRAY,stroke_width=1.2,stroke_opacity=.4) for p,q in zip(ps,ps[1:]) for a in p for b in q]),VGroup(*[Dot(p,radius=.07,color=INK) for layer in ps for p in layer]))
class ImpactScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.035:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.0001:self.wait(target-self.time)
 def note(self,s,c=YELLOW):self.notice.become(text(s,29,c,7.65 if VERT else 14.2).move_to([0,-4.25 if VERT else -2.35,0]))
 def construct(self):
  m=M[self.index];self.start=m['start'];self.end=m['end'];top=7.25 if VERT else 3.85
  self.add(text('최소 조건 2부  /  신경망 03',22,GRAY).move_to([0,top,0]))
  titles=['필요한 차원만 남길 수 있을까?','큰 행렬을 두 작은 행렬로','복원 오차와 예측은 다른 문제','IMPACT는 활성화에서 출발한다','활성화 복원만으로 충분할까?','성능에 중요한 방향을 남긴다','성능을 유지하며 더 작게','복원할 것인가, 기능을 보존할 것인가','모든 층에 같은 차원이 필요할까?']
  self.add(text(titles[self.index],36 if VERT else 39,INK,7.85 if VERT else 14.7).move_to([0,top-.8,0]))
  self.notice=text('',25);self.add(self.notice)
  line=Line([-3.85 if VERT else -7.3,-7.2 if VERT else -4.12,0],[3.85 if VERT else 7.3,-7.2 if VERT else -4.12,0],color=EDGE,stroke_width=3)
  progress=line.copy().set_color(BLUE);progress.add_updater(lambda o:o.put_start_and_end_on(line.get_start(),line.get_start()+RIGHT*max(.001,line.width*(self.start+self.time)/156)));self.add(line,progress)
  for row in TIMING:
   if row['end']<=self.start or row['start']>=self.end:continue
   s='\n'.join(textwrap.wrap(row['text'],width=25 if VERT else 49));cap=text(s,29 if VERT else 28,INK,7.75 if VERT else 14.5).move_to([0,-5.95 if VERT else -3.3,0]).set_z_index(20)
   cap.add_updater(lambda o,r=row:o.set_opacity(1 if r['start']-.00001<=self.start+self.time<r['end']-.00001 else 0));self.add(cap)
  [self.opening,self.factorization,self.error_direction,self.activations,self.activation_space,self.importance,self.results,self.function,self.layers][self.index]();self.at(self.end)
 def opening(self):
  n=network(6.5 if VERT else 10,3).move_to([0,1.2 if VERT else .4,0]);self.play(LaggedStart(Create(n[0]),FadeIn(n[1]),lag_ratio=.2),run_time=1.6)
  self.at(3);q=text('이 차원이 모두 필요할까?',43,YELLOW,7.5 if VERT else 13).move_to([0,3.7 if VERT else 2.1,0]);self.play(FadeIn(q),run_time=.7)
  self.at(7);self.play(n.animate.set_opacity(.15),run_time=.4)
  curve=ParametricFunction(lambda t:np.array([2*t,t*t-.5,.2*t*t*t]),t_range=[-1.2,1.2,.025],color=BLUE,stroke_width=5).move_to([0,.7,0]);self.play(Create(curve),run_time=1.3);self.note('내부 표현의 낮은 차원',BLUE)
  self.at(13);unknown=card('측정 차원 = ?',4.8,.9,YELLOW,36).move_to([0,-1.2,0]);self.play(FadeIn(unknown),run_time=.6)
  self.at(16);self.play(FadeOut(curve),FadeOut(n),FadeOut(unknown),FadeOut(q),run_time=.5)
  move=VGroup(text('Measure',42,GRAY),text('→',45,INK),text('Compress',42,BLUE)).arrange(DOWN if VERT else RIGHT,buff=.35).move_to([0,1,0]);self.play(FadeIn(move),run_time=.7);self.note('몇 차원인지 대신, 실제로 줄여보자',GREEN)
 def factorization(self):
  blocks=VGroup(*[card(s,2.1,.9,GRAY,25) for s in ['Attention','FFN','Output']]).arrange(DOWN if VERT else RIGHT,buff=.3).move_to([0,1.5 if VERT else .4,0])
  self.play(FadeIn(blocks),run_time=.6);self.at(23);self.play(FadeOut(blocks),run_time=.3)
  w=grid(D['W'],.35,GRAY).move_to([0,2.8,0] if VERT else [-3.8,.3,0]);wl=text('W : 8 × 8',30,GRAY).next_to(w,UP,buff=.2)
  x=card('입력 x',2,.7,YELLOW,28).move_to([0,5.4,0] if VERT else [-6.4,.3,0]);y=card('출력 Wx',2.5,.7,YELLOW,28).move_to([0,.65,0] if VERT else [0,.3,0])
  self.play(FadeIn(w),FadeIn(wl),FadeIn(x),FadeIn(y),run_time=.7);self.note('행렬로 입력을 변환합니다',GRAY);self.at(28)
  self.play(FadeOut(x),FadeOut(y),run_time=.3)
  def factors(r):
   a=grid(D[f'A{r}'],.35,BLUE);b=grid(D[f'B{r}'],.35,BLUE)
   group=VGroup(a,text('×',35,BLUE),b).arrange(RIGHT,buff=.4).move_to([0,-1.25,0] if VERT else [3.35,.3,0])
   labels=VGroup(text(f'A : 8 × {r}',27,BLUE).next_to(a,UP,buff=.25),text(f'B : {r} × 8',27,BLUE).next_to(b,UP,buff=.25))
   return group,labels
  fact,labels=factors(3);self.play(FadeIn(fact),FadeIn(labels),run_time=.8)
  count=text('64 → 48 parameters',35,BLUE,7.6).move_to([0,-3.3,0] if VERT else [0,-1.65,0]);self.play(FadeIn(count),run_time=.6);self.note('W ≈ AB',BLUE)
  self.at(33);f2,l2=factors(2);self.play(Transform(fact,f2),Transform(labels,l2),Transform(count,text('64 → 32 parameters',35,BLUE).move_to(count)),run_time=.9)
  self.note('r(m + n) < mn 일 때 크기 감소',GREEN)
 def decision(self):
  # Equal units on both axes: equal Euclidean errors must have equal screen length.
  unit=(3.9 if VERT else 3.1)/2.2
  ax=Axes(x_range=[-1.4,1.4,1],y_range=[-.8,1.4,1],x_length=2.8*unit,y_length=2.2*unit,tips=False,axis_config={'color':EDGE,'include_ticks':False}).move_to([0,1.7,0] if VERT else [-2.7,.35,0])
  h=np.array([.3,.2]);p=ax.c2p(*h);a=ax.c2p(.3,.95);b=ax.c2p(-.45,.2)
  boundary=DashedLine(ax.c2p(0,-.8),ax.c2p(0,1.4),color=GRAY,dash_length=.1,stroke_width=2)
  point=Dot(p,radius=.085,color=INK);e1=Arrow(p,a,buff=0,color=GREEN,stroke_width=4);e2=Arrow(p,b,buff=0,color=RED,stroke_width=4)
  labs=VGroup(text('A',28,GREEN).move_to(ax.c2p(.95,1.2)),text('B',28,RED).move_to(ax.c2p(-1,1.2)),text('예측 경계',22,GRAY).next_to(boundary,DOWN,buff=.15))
  return VGroup(ax,boundary,point,labs),ax,e1,e2
 def error_direction(self):
  comp=VGroup()
  x=D['example_input']
  for i,(a,label,c) in enumerate([(D['W'],'원본 W',GRAY),(D['A2']@D['B2'],'압축 AB',BLUE)]):
   mat=grid(a,.25,c);vec=grid(a@x,.25,YELLOW);arr=Arrow(ORIGIN,RIGHT*.8,color=GRAY,buff=0)
   row=VGroup(mat,arr,vec).arrange(RIGHT,buff=.2);lab=text(label,29,c).next_to(row,UP,buff=.2);panel=VGroup(row,lab)
   panel.move_to([0,2.8-i*3.5,0] if VERT else [-3.8+i*7.6,.5,0]);comp.add(panel)
  self.play(FadeIn(comp),run_time=.8);self.note('같은 입력 · 달라진 출력',RED);self.at(42)
  self.play(FadeOut(comp),run_time=.35)
  err=grid(D['W']-D['A2']@D['B2'],.4,RED,limit=np.max(abs(D['W']))).move_to([0,.75 if VERT else .25,0]);label=text('가중치 복원 오차  W − AB',33,RED).next_to(err,UP,buff=.3)
  self.play(FadeIn(err),FadeIn(label),run_time=.6)
  self.note('가중치의 복원 오차를 줄이는 목표',GRAY)
  for r in [3,4]:self.play(Transform(err,grid(D['W']-D[f'A{r}']@D[f'B{r}'],.4,RED,limit=np.max(abs(D['W']))).move_to(err)),run_time=.65)
  self.note('원래 행렬과의 차이를 줄이는 목표',GRAY);self.at(46);self.play(FadeOut(err),FadeOut(label),run_time=.3)
  q=text('복원 오차가 작으면\n예측도 같을까?',42,YELLOW,7.6 if VERT else 12).move_to([0,.8,0]);self.play(FadeIn(q),run_time=.5);self.at(48);self.play(FadeOut(q),run_time=.3)
  model,ax,e1,e2=self.decision();self.play(FadeIn(model),run_time=.6);self.note('작은 복원 오차 ≠ 예측 유지',RED);self.play(GrowArrow(e1),run_time=.6);self.play(GrowArrow(e2),run_time=.6)
  outcomes=VGroup(card('수직 오차: A → A',3.8,.75,GREEN,28),card('수평 오차: A → B',3.8,.75,RED,28)).arrange(DOWN,buff=.35).move_to([0,-1.95,0] if VERT else [4.6,.35,0])
  self.play(FadeIn(outcomes),run_time=.5);self.at(53);self.note('||ε1|| = ||ε2||  ·  방향은 다릅니다',YELLOW)
  self.play(Indicate(e1,color=GREEN),Indicate(e2,color=RED),run_time=1)
 def spectrum(self,key,title,c,center):
  vals=D[key];bars=VGroup(*[Rectangle(width=.38,height=max(.025,float(v)*1.8),stroke_width=0,fill_color=c,fill_opacity=1).move_to([i*.53,float(v)*.9,0]) for i,v in enumerate(vals)])
  base=Line([-.3,0,0],[4.1,0,0],color=GRAY,stroke_width=1.3)
  out=VGroup(bars,base,text(title,29,c).move_to([1.8,2.3,0]));return out.move_to(center)
 def activations(self):
  paper=VGroup(text('IMPACT',66,BLUE),text('Importance-Aware\nActivation Space Reconstruction',30,INK,7.5 if VERT else 13),text('Chowdhury et al. · ACL 2026',25,ORANGE)).arrange(DOWN,buff=.3).move_to([0,1.5 if VERT else .7,0])
  self.play(FadeIn(paper),run_time=.9);self.note('활성화 구조 + 기울기 기반 중요도',GREEN);self.at(66)
  source=text('IMPACT · ACL 2026',25,ORANGE).move_to([0,5.25 if VERT else 2.25,0]);self.play(ReplacementTransform(paper,source),run_time=.4)
  w=grid(D['W'],.26,GRAY).move_to([0,2.95,0] if VERT else [-3.8,.3,0]);wl=text('고정된 가중치 W',27,GRAY).next_to(w,DOWN if VERT else UP,buff=.2)
  target=grid(D['Y'][:8],.22,YELLOW).move_to([0,-.7,0] if VERT else [3.8,.3,0]);yl=text('입력마다 달라지는 활성화 Y',26,YELLOW,7.3).next_to(target,UP,buff=.3)
  sample=card('입력 x1',2.4,.55,YELLOW,24).move_to([0,4.4,0] if VERT else [-6.5,.3,0]);self.play(FadeIn(w),FadeIn(wl),FadeIn(yl),FadeIn(sample),run_time=.6)
  collected=VGroup()
  for i in range(8):
   row=VGroup(*list(target)[i*8:(i+1)*8]);collected.add(row)
   self.play(FadeIn(row),Transform(sample,card(f'입력 x{i+1}',2.4,.55,YELLOW,24).move_to(sample)),run_time=.38)
  self.note('y = Wx · W는 고정, 입력과 활성화는 변화',YELLOW);self.at(72)
  self.play(FadeOut(w),FadeOut(wl),FadeOut(yl),FadeOut(sample),FadeOut(collected),run_time=.4)
  a=self.spectrum('weight_spectrum','가중치 W',GRAY,[0,2.7,0] if VERT else [-3.8,.35,0]);b=self.spectrum('activation_spectrum','활성화 Y',YELLOW,[0,-.75,0] if VERT else [3.8,.35,0])
  self.play(FadeIn(a),FadeIn(b),run_time=.8);self.note('활성화가 일부 방향에 더 집중될 수 있습니다',YELLOW)
 def activation_space(self):
  _,_,vt=np.linalg.svd(D['Y'],full_matrices=False);points=D['Y']@vt[:3].T;points=points/np.std(points[:,0])*.85
  center=np.array([0,1.4,0] if VERT else [-2.2,.4,0])
  def project(p):x,y,z=p;return center+np.array([.9*x+.45*y,.25*x+.65*y+.9*z,0])
  plane=Polygon(*[project(p) for p in [(-2,-2,0),(2,-2,0),(2,2,0),(-2,2,0)]],stroke_color=BLUE,stroke_width=2,fill_color=BLUE,fill_opacity=.1)
  cloud=VGroup(*[Dot(project(p),radius=.038,color=YELLOW) for p in points])
  u=Arrow(project([0,0,0]),project([2.5,0,0]),color=BLUE,buff=0);v=Arrow(project([0,0,0]),project([0,2.5,0]),color=BLUE,buff=0)
  self.play(FadeIn(cloud),run_time=.8);self.play(Create(plane),GrowArrow(u),GrowArrow(v),run_time=.8)
  phrase=card('활성화의 주요 방향',5.3,.85,BLUE,32).move_to([0,-1.7,0] if VERT else [4.5,.5,0]);self.play(FadeIn(phrase),run_time=.6)
  self.at(84);self.note('모든 방향이 예측에 똑같이 중요할까?',ORANGE)
 def importance(self):
  model,ax,e1,e2=self.decision();self.add(model)
  g=Arrow(ax.c2p(.3,.2),ax.c2p(-.7,.2),buff=0,color=ORANGE,stroke_width=6)
  gl=text('손실 기울기 g = (−1, 0)',25,ORANGE).move_to([0,4.3,0] if VERT else [-2.7,2.25,0]);self.play(GrowArrow(g),FadeIn(gl),run_time=.7)
  formula=card('ΔL ≈ g · ε',4.1,.85,ORANGE,34).move_to([0,-1.55,0] if VERT else [4.6,1.2,0]);self.play(FadeIn(formula),run_time=.6)
  self.note('활성화 교란에 대한 국소 손실 변화',ORANGE);self.at(91);self.note('같은 오차 크기 0.75 · 방향만 다릅니다',YELLOW)
  self.play(GrowArrow(e1),run_time=.6)
  a=text('수직 방향: g · ε1 = 0',27,GREEN,7).move_to([0,-2.65,0] if VERT else [4.6,.2,0]);self.play(FadeIn(a),run_time=.5)
  self.play(GrowArrow(e2),run_time=.6)
  b=text('평행 방향: g · ε2 = 0.75',27,RED,7).move_to([0,-3.3,0] if VERT else [4.6,-.75,0]);self.play(FadeIn(b),run_time=.5)
  self.at(97);keep=Line(ax.c2p(-1.35,0),ax.c2p(1.35,0),color=ORANGE,stroke_width=5);self.play(Create(keep),e1.animate.set_stroke(opacity=.2),run_time=.7);self.note('성능에 민감한 방향의 오차를 우선 줄입니다',ORANGE)
  self.at(102);self.play(*[FadeOut(o) for o in [model,g,gl,formula,e1,e2,a,b,keep]],run_time=.4)
  inputs=VGroup(card('활성화 구조',3.1,.8,YELLOW,28),text('+',32,INK),card('기울기 중요도',3.1,.8,ORANGE,28)).arrange(RIGHT,buff=.2).move_to([0,3.45 if VERT else 1.8,0])
  cov=card('중요도 가중 공분산',6.1,.85,ORANGE,31).move_to([0,1.65 if VERT else .45,0]);basis=card('복원 기저 → 저랭크 행렬',6.5,.9,BLUE,30).move_to([0,-.3 if VERT else -1,0])
  self.play(FadeIn(inputs),run_time=.6);self.play(FadeIn(cov),GrowArrow(Arrow(inputs.get_bottom(),cov.get_top(),buff=.12,color=ORANGE)),run_time=.6)
  self.play(FadeIn(basis),GrowArrow(Arrow(cov.get_bottom(),basis.get_top(),buff=.12,color=BLUE)),run_time=.6);self.note('같은 랭크 · 더 적합한 보존 방향',GREEN)
 def results(self):
  source=text('IMPACT · ACL 2026',26,ORANGE).move_to([0,4.9 if VERT else 2.25,0]);self.add(source)
  a=card('여러 언어모델',5.6,1,GRAY,36);b=card('여러 평가 작업',5.6,1,GRAY,36);panels=VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.45).move_to([0,2.3 if VERT else .75,0])
  self.play(FadeIn(panels),run_time=.8);accuracy=card('비슷하거나 더 나은 정확도',7.3,.95,GREEN,33).move_to([0,-.4 if VERT else -.85,0]);self.play(FadeIn(accuracy),run_time=.7)
  self.note('평가한 압축 방법들과 비교',GRAY);self.at(117);self.play(FadeOut(panels),FadeOut(accuracy),run_time=.35)
  label=text('기존 비교 방법 대비',34,GRAY).move_to([0,3.2 if VERT else 1.65,0]);num=text('최대 55.4%',80,GREEN,7.8 if VERT else 14).move_to([0,1.4 if VERT else .3,0]);caption=text('더 큰 모델 크기 감소',39,GREEN,7.8 if VERT else 14).move_to([0,-.1 if VERT else -1,0])
  self.play(FadeIn(label),FadeIn(num,shift=UP*.15),FadeIn(caption),run_time=.8);self.note('정확도를 유지한 비교에서 보고된 최대 개선량',GREEN)
  self.at(123);conditions=VGroup(*[card(s,2.2,.65,GRAY,25) for s in ['모델','평가 작업','압축 조건']]).arrange(RIGHT,buff=.25).move_to([0,-2,0] if VERT else [0,-1.75,0]);self.play(FadeIn(conditions),run_time=.7);self.note('결과는 모델과 조건에 따라 달라집니다',GRAY)
 def function(self):
  self.note('중요한 차이: 무엇을 보존하느냐',GREEN);self.at(130)
  limit=np.max(abs(D['W']));a=grid(D['W']-D['A2']@D['B2'],.28,RED,limit=limit);b=grid(D['W']-D['W_function'],.28,RED,limit=limit)
  left=VGroup(text('행렬 복원',33,GRAY),a,card('예측 A → B',3.5,.7,RED,29)).arrange(DOWN,buff=.35)
  right=VGroup(text('기능 보존',33,GREEN),b,card('예측 A → A',3.5,.7,GREEN,29)).arrange(DOWN,buff=.35)
  if VERT:left.scale(.82).move_to([0,2.7,0]);right.scale(.82).move_to([0,-.8,0])
  else:left.move_to([-3.9,.3,0]);right.move_to([3.9,.3,0])
  self.play(FadeIn(left),FadeIn(right),run_time=.8);self.note('같은 랭크 · 서로 다른 보존 목표',BLUE);self.at(137)
  self.play(left.animate.set_opacity(.2),Indicate(right,color=GREEN),run_time=.9);self.note('모든 정보를 그대로 복원할 필요는 없습니다',GREEN)
  self.at(141);self.play(FadeOut(left),FadeOut(right),run_time=.5)
  q=text('어떤 정보를 제거하면\n실제 기능이 달라질까?',46,GREEN,7.7 if VERT else 13).move_to([0,1,0]);self.play(FadeIn(q),run_time=.7)
 def layers(self):
  blocks=VGroup(*[VGroup(RoundedRectangle(width=1.3 if not VERT else 4.8,height=1.6 if not VERT else .75,corner_radius=.1,color=GRAY,fill_color=PANEL,fill_opacity=1),text(f'층 {i+1}',27,GRAY)) for i in range(5)])
  blocks.arrange(DOWN if VERT else RIGHT,buff=.45).move_to([0,1.2 if VERT else .5,0]);self.play(FadeIn(blocks),run_time=.8)
  self.at(150)
  for i,ratio in enumerate([.9,.48,.96,.65,.75]):
   shape=blocks[i][0];lab=blocks[i][1]
   target=lab.get_center() if VERT else shape.get_bottom()+DOWN*.35
   self.play(shape.animate.stretch_to_fit_width(shape.width*ratio).set_stroke(color=BLUE).set_fill(BLUE,opacity=.12),lab.animate.move_to(target).set_color(BLUE),run_time=.35)
  self.note('층마다 유지해야 할 차원도 다를까?',YELLOW)
