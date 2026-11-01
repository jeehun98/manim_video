"""Normal-model sufficiency: fixed observations, normalized likelihood, explicit assumptions."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from data_model import *
ROOT=Path(__file__).resolve().parent
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B78';YELLOW='#F3D277';PURPLE='#B89CFF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
MODEL='독립·동일 정규분포 · 분산 알려짐'
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def box(s,width=6,height=1,color=YELLOW,size=30):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.13,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.35))
def database(width=5.4,height=3.5):
 out=VGroup()
 row_height=min(.5,height/6)
 for y in np.linspace(-height/2+row_height/2,height/2-row_height/2,5):
  out.add(RoundedRectangle(width=width,height=row_height,corner_radius=.1,color=TEAL,fill_color=PANEL,fill_opacity=1,stroke_width=1.5).move_to([0,y,0]))
  out.add(VGroup(*[Dot([x,y,0],radius=.035,color=TEAL) for x in np.linspace(-width*.36,width*.36,10)]))
 return out
def chart(relative=False):
 if relative:
  width,height,center=(6.3,3.3,[0,.65,0]) if VERT else (7.2,2.6,[-2.8,.25,0]);ymax=1.1
 else:
  width,height,center=(6.3,3.1,[0,1,0]) if VERT else (6.3,2.6,[-3.3,.25,0]);ymax=.25
 ax=Axes(x_range=[-1,7,1],y_range=[0,ymax,ymax/5],x_length=width,y_length=height,tips=False,axis_config={'include_ticks':False,'color':MUTED,'stroke_width':1.3}).move_to(center)
 labels=VGroup()
 for x in [-1,1,3,5,7]:labels.add(txt(str(x),20,MUTED).move_to(ax.c2p(x,0)+DOWN*.25))
 xlabel=('후보 μ' if relative else '측정값 x') if VERT else ('μ' if relative else 'x')
 xpos=ax.c2p(6.2,0)+DOWN*.65 if VERT else ax.c2p(7,0)+RIGHT*.3+UP*.1
 labels.add(txt(xlabel,22,PURPLE if relative else TEAL).move_to(xpos))
 labels.add(txt('상대 우도 · 최대값 1' if relative else '확률밀도',21,PURPLE).move_to(ax.c2p(1,ymax)+UP*.25))
 for y in ([0,1] if relative else [0,.2]):labels.add(txt(f'{y:g}',18,MUTED).move_to(ax.c2p(-1,y)+LEFT*.25))
 return VGroup(ax,labels),ax
def curve(ax,fn,color=PURPLE,width=4):
 xs=np.linspace(-1,7,241)
 return VMobject(color=color,stroke_width=width).set_points_as_corners([ax.c2p(x,float(fn(x))) for x in xs])
def observations(values,center,label,color=TEAL,width=6.6):
 c=np.array(center,float);unit=width/7;left=c+LEFT*width*.43
 baseline=Line(left,c+RIGHT*width*.43,color=EDGE,stroke_width=2)
 dots=VGroup();counts={}
 for value in values:
  level=counts.get(value,0);counts[value]=level+1
  dots.add(Dot(left+RIGHT*(value*unit)+UP*(.16+.24*level),radius=.075,color=color))
 ticks=VGroup(*[txt(str(x),17,MUTED).move_to(left+RIGHT*x*unit+DOWN*.3) for x in range(7)])
 mean_line=DashedLine(left+RIGHT*3*unit+DOWN*.12,left+RIGHT*3*unit+UP*.66,color=YELLOW,stroke_width=1.5,dash_length=.08)
 raw=txt(label+' : '+', '.join(f'{x:g}' for x in values),27,color,width).move_to(c+UP*1.05)
 average=txt('x̄ = 3',27,YELLOW).move_to(c+DOWN*.83)
 return VGroup(baseline,dots,ticks,mean_line,raw,average)
def data_pair():
 ca,cb=([0,2.25,0],[0,-.5,0]) if VERT else ([-3.6,.3,0],[3.6,.3,0])
 return observations(A,ca,'A',TEAL,6.2),observations(B,cb,'B',PURPLE,6.2)
def expansion_cards():
 cards=VGroup(box('Q = Σxᵢ²',6 if VERT else 3.9,1,MUTED,31),box('−2μ S = −2μ Σxᵢ',6 if VERT else 5.2,1,YELLOW,31),box('nμ²',6 if VERT else 3,1,PURPLE,35))
 return cards.arrange(DOWN if VERT else RIGHT,buff=.3).move_to([0,.85 if VERT else .25,0])
class SufficiencyScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=YELLOW):
  self.notice.become(txt(s,27 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):
  self.cond.become(box(s,7 if VERT else 12,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   04',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2)
  progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=YELLOW,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/153))))
  self.add(track,progress);getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  rng=np.random.default_rng(404);numbers=VGroup(*[txt(f'{v:.1f}',20,TEAL) for v in rng.normal(100,4,120)]).arrange_in_grid(cols=8 if VERT else 15,buff=(.15,.1));numbers.scale_to_fit_height(5.8 if VERT else 3)
  if numbers.width>(7.1 if VERT else 13.6):numbers.scale_to_fit_width(7.1 if VERT else 13.6)
  numbers.move_to([0,.75 if VERT else .2,0])
  self.play(LaggedStart(*[FadeIn(VGroup(*numbers[i:i+8])) for i in range(0,120,8)],lag_ratio=.02),run_time=1.8);self.note('측정값 일부를 대표 표시',MUTED)
  self.at(3);db=database(5,2.8 if VERT else 2.1).move_to(numbers);self.play(ReplacementTransform(numbers,db),run_time=.8)
  self.condition('부품의 길이 측정');self.add(txt('n = 1,000,000',39,YELLOW).move_to([0,3.2 if VERT else 1.75,0]));self.note('전체 관측 수: 백만 개',MUTED)
 def part_01(self):
  self.condition('개별 부품보다 공장의 평균 길이')
  bars=VGroup()
  for i,length in enumerate([100.5,97.5,106.5,94.5,103.5,99.]):
   y=2.85-i*.6 if VERT else 1.45-i*.47
   bar=Rectangle(width=length/30,height=.2,color=TEAL,fill_color=TEAL,fill_opacity=.65,stroke_width=1).move_to([-3.1+length/60 if VERT else -6.1+length/60,y,0])
   value=txt(f'{length:g} mm',22,TEAL).move_to([2.5 if VERT else -1.5,y,0]);bars.add(VGroup(bar,value))
  self.play(FadeIn(bars),run_time=.7)
  target=box('모집단 평균 μ = ?',6 if VERT else 5.5,1.2,PURPLE,33).move_to([0,-1.8,0] if VERT else [3.4,.3,0]);self.add(target);self.note('μ는 추론할 모수 · 표본평균과 구별',PURPLE)
  self.at(13);self.condition(MODEL);self.play(bars.animate.set_opacity(.4),run_time=.6)
 def part_02(self):
  self.condition(MODEL+' · n 고정')
  db=database(5.6,2.7 if VERT else 2.1).move_to([0,1.3,0] if VERT else [-3.4,.2,0]);self.add(db)
  summary=box('x̄ = (Σxᵢ) / n',6.5 if VERT else 5.6,1.3,YELLOW,38).move_to([0,-1.35,0] if VERT else [3.4,.3,0])
  self.play(TransformFromCopy(db,summary),db.animate.set_opacity(.3),run_time=1.3);self.note('보존하는 것은 μ에 관한 정보',PURPLE)
  self.at(25);name=txt('Sufficient Statistic',30,YELLOW,7).move_to([0,3.35 if VERT else 1.65,0]);self.play(FadeIn(name),run_time=.7);self.note('충분통계량 · 원자료 전체의 복원은 아님')
 def part_03(self):
  self.condition('전체 정보와 모수 정보는 다르다')
  q=txt('무엇이 사라지지\n않는다는 걸까?' if VERT else '무엇이 사라지지 않는다는 걸까?',44,PURPLE,7 if VERT else 13).move_to([0,1.6 if VERT else .6,0]);self.add(q)
  b=box('원자료의 복원 ≠ μ 정보 보존',7 if VERT else 12,1.1,YELLOW,30).move_to([0,-1.05 if VERT else -.8,0]);self.play(FadeIn(b),run_time=.7);self.note('지정한 모형과 추론 대상 아래에서')
 def part_04(self):
  self.condition('관측값 고정 · 예시 σ² = 4 · 후보 μ 변화')
  base,ax=chart(False);self.add(base)
  observed=VGroup(*[Dot(ax.c2p(x,0),radius=.055,color=TEAL) for x in A]);self.add(observed)
  mu=ValueTracker(3)
  def dynamic():
   m=round(mu.get_value(),1);c=curve(ax,lambda x:density(x,m))
   stems=VGroup(*[Line(ax.c2p(x,0),ax.c2p(x,float(density(x,m))),color=TEAL,stroke_width=1.6) for x in A]);heights=VGroup(*[Dot(ax.c2p(x,float(density(x,m))),radius=.045,color=PURPLE) for x in A])
   line=DashedLine(ax.c2p(m,0),ax.c2p(m,.21),color=PURPLE,dash_length=.08,stroke_width=1.5)
   label=txt(f'후보 μ = {m:.1f}',27,PURPLE).move_to([0,3.25,0] if VERT else [3.4,1.2,0])
   return VGroup(c,stems,heights,line,label)
  live=always_redraw(dynamic);self.add(live);self.note('데이터는 고정 · 각 관측값의 밀도를 확인',TEAL)
  self.at(41);self.play(mu.animate.set_value(4.5),run_time=1.8);self.play(mu.animate.set_value(2),run_time=1.8);self.play(mu.animate.set_value(3),run_time=.8)
  self.at(46)
  formula=box('L(μ | x) = ∏ f(xᵢ | μ)',7 if VERT else 6,1,PURPLE,30).move_to([0,-2.25,0] if VERT else [3.4,-.15,0]);self.play(FadeIn(formula),run_time=.7);self.note('독립 관측값의 확률밀도를 곱한 우도',PURPLE)
 def part_05(self):
  self.condition(MODEL+' · n 고정')
  likelihood=txt('L(μ | x) ∝ exp[−Σ(xᵢ − μ)² / (2σ²)]',31,PURPLE,7 if VERT else 14).move_to([0,3.15 if VERT else 1.7,0]);self.add(likelihood)
  original=box('Σ(xᵢ − μ)²',6.5,1.35,PURPLE,43).move_to([0,.65 if VERT else .1,0]);self.add(original);self.note('우도에 등장하는 제곱합',PURPLE)
  self.at(56);cards=expansion_cards();self.play(ReplacementTransform(original,cards),run_time=1.1);self.note('Q − 2μS + nμ² · S = Σxᵢ')
 def part_06(self):
  self.condition(MODEL+' · n 고정');cards=expansion_cards();self.add(cards)
  self.play(Indicate(cards[1],color=YELLOW,scale_factor=1.03),run_time=.7);self.note('μ와 데이터가 함께 등장하는 것은 S = Σxᵢ')
  self.at(69);self.play(cards[0].animate.set_opacity(.3),run_time=.6)
  self.note('Q = Σxᵢ²는 μ와 무관 → C(x)에 포함',MUTED)
 def part_07(self):
  self.condition('n 고정 · σ² 알려짐 · Σxᵢ = n x̄')
  eq=box('L(μ | x) / L(x̄ | x)',7 if VERT else 11,1,PURPLE,38).move_to([0,2.6 if VERT else 1.25,0]);self.add(eq)
  formula=box('= exp[−n(μ − x̄)² / (2σ²)]',7 if VERT else 12,1.3,YELLOW,34).move_to([0,.7 if VERT else -.1,0]);self.play(FadeIn(formula),run_time=.8)
  self.note('최대값 1의 상대 우도 · 모양은 x̄로 결정')
 def part_08(self):
  self.condition('독립·동일 정규모형 · n = 5 · 알려진 σ² = 4')
  a,b=data_pair();self.note('두 기록을 같은 모형에서 비교',MUTED)
  self.at(81);self.play(FadeIn(a),run_time=.35)
  self.at(82);self.play(FadeIn(b),run_time=.4)
  self.at(85);self.play(Indicate(a[-1],color=YELLOW),Indicate(b[-1],color=YELLOW),run_time=.7);self.note('합계 15 · 표본평균은 모두 3')
 def part_09(self):
  self.condition('n = 5 · x̄ = 3 · 알려진 σ² = 4')
  base,ax=chart(True);self.add(base)
  ca=curve(ax,lambda m:relative_likelihood(A,m),TEAL,6)
  cb=DashedVMobject(curve(ax,lambda m:relative_likelihood(B,m),PURPLE,3.8),num_dashes=30)
  self.play(Create(ca),run_time=1);self.play(Create(cb),run_time=1.1)
  legends=VGroup(txt('A',28,TEAL),txt('B',28,PURPLE)).arrange(RIGHT,buff=.7).move_to([0,3.35,0] if VERT else [3.7,1.2,0]);self.add(legends)
  label=box('각 우도를 최대값 1로 정규화',7 if VERT else 5.5,.95,YELLOW,26).move_to([0,-2.25,0] if VERT else [3.7,.1,0]);self.add(label)
  self.note('같은 상대 곡선 · 원래의 절대 높이는 다를 수 있음',MUTED)
  self.at(95);self.note('원자료 복원 불가 · μ에 대한 정보 보존',YELLOW)
 def part_10(self):
  self.condition('표본평균 하나면 언제나 충분할까?')
  a,b=data_pair();self.add(a,b);self.note('표본평균은 모두 3',YELLOW)
  self.at(104);self.condition('모형 변경: μ와 σ² 모두 미지')
  self.at(107);self.play(Indicate(a[1],color=TEAL),Indicate(b[1],color=PURPLE),run_time=.7);self.note('평균에서의 제곱거리 합: A = 10 · B = 36',PURPLE)
 def part_11(self):
  self.condition('미지 모수 (μ, σ²) · 고정 n = 5')
  table=VGroup()
  for label,s,q,c in [('A',15,55,TEAL),('B',15,81,PURPLE)]:
   row=VGroup(box(label,1.2,.95 if VERT else .85,c,30),box(f'Σxᵢ = {s}',2.5 if VERT else 4,.95 if VERT else .85,YELLOW,29),box(f'Σxᵢ² = {q}',2.8 if VERT else 4.5,.95 if VERT else .85,PURPLE,28)).arrange(RIGHT,buff=.15);table.add(row)
  table.arrange(DOWN,buff=.4).move_to([0,1.85 if VERT else .9,0]);self.play(FadeIn(table),run_time=.8)
  summary=box('(Σxᵢ, Σxᵢ²)',6 if VERT else 8,1.2 if VERT else 1,YELLOW,41).move_to([0,-.6 if VERT else -.95,0]);self.add(summary);self.note('평균과 분산의 추론에 필요한 두 요약')
  self.at(117);self.note('추론 대상과 통계 모형이 필요한 정보를 정한다')
 def part_12(self):
  self.condition('예시: 다시 알려진 분산 · 고정 n 정규모형')
  english=txt('Minimal Sufficient Statistic',27,YELLOW,7 if VERT else 13).move_to([0,3.35 if VERT else 1.85,0]);self.add(english);self.note('통계적 정보의 불필요한 구분을 줄인다',MUTED)
  left=box('원본 X\n그 자체도 충분',3.2 if VERT else 5.2,1.15,TEAL,25).move_to([-1.75,1.8,0] if VERT else [-3.5,.8,0])
  right=box('임의의 다른\n충분통계량 S',3.2 if VERT else 5.2,1.15,TEAL,25).move_to([1.75,1.8,0] if VERT else [3.5,.8,0])
  target=box('T = x̄',6 if VERT else 6,1.2,YELLOW,41).move_to([0,-1 if VERT else -.95,0])
  self.at(127);self.play(FadeIn(left),FadeIn(target),run_time=.6)
  al=Arrow(left.get_bottom(),target.get_top()+LEFT*1.25,color=TEAL,buff=.1,stroke_width=2);self.play(GrowArrow(al),run_time=.5)
  self.at(131);self.play(FadeIn(right),run_time=.6)
  ar=Arrow(right.get_bottom(),target.get_top()+RIGHT*1.25,color=TEAL,buff=.1,stroke_width=2);self.play(GrowArrow(ar),run_time=.5);self.note('모든 충분통계량 S에서 T = g(S)로 계산 가능')
 def part_13(self):
  self.condition('서로 다른 최소화 기준')
  a=box('통계적 최소성',6 if VERT else 5.7,1.2,YELLOW,35)
  b=box('저장량·계산량 최소',6 if VERT else 5.7,1.2,RED,32)
  if VERT:a.move_to([0,2.35,0]);b.move_to([0,-.35,0]);neq=txt('≠',59,RED).move_to([0,1,0])
  else:a.move_to([-3.5,.5,0]);b.move_to([3.5,.5,0]);neq=txt('≠',59,RED).move_to([0,.5,0])
  self.add(a,b,neq);self.note('정보를 구분하는 방식의 최소성 · 비트 수 보장 아님',MUTED)
 def part_14(self):
  self.condition(MODEL+' · n 고정')
  db=database(5.5,2.8 if VERT else 2.2).move_to([0,1.2,0] if VERT else [-3.5,.2,0]);self.add(db)
  self.add(txt('n = 1,000,000',32,TEAL).move_to([0,3.35,0] if VERT else [-3.5,1.75,0]));self.note('많이 남기는 것보다, 무엇을 보존하는가?',YELLOW)
  self.at(147)
  summary=box('x̄',6 if VERT else 5,1.5,YELLOW,67).move_to([0,1.2,0] if VERT else [-3.5,.3,0]);self.play(ReplacementTransform(db,summary),run_time=.8)
  info=box('μ를 추론하는 데\n필요한 정보 보존' if VERT else 'μ 추론에 필요한 정보 보존',6.5 if VERT else 6.5,1.3,PURPLE,33).move_to([0,-1.25,0] if VERT else [3.5,.3,0]);self.play(FadeIn(info),run_time=.6)
  self.at(150);self.note('무엇을 알고 싶은가? · 그 정보를 남긴다',YELLOW)
