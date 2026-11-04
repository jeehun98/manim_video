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
def experiment(candidate,reveal=False):
 # The same numeric scale and fixed observations are used for both records.
 def draw():
  mu=round(candidate.get_value(),1);out=VGroup()
  badge=box(f'후보 평균 = {mu:.1f}',5 if VERT else 6,.62,YELLOW,29).move_to([0,3.7 if VERT else 1.85,0]);out.add(badge)
  for values,label,color,c in [(A,'A',TEAL,np.array([0,2.1,0]) if VERT else np.array([-3.6,.35,0])),(B,'B',PURPLE,np.array([0,-.65,0]) if VERT else np.array([3.6,.35,0]))]:
   unit=.88;left=c+LEFT*2.64
   out.add(txt(label+' : '+', '.join(f'{x:g}' for x in values),26,color,6.1).move_to(c+UP*1.02))
   out.add(Line(left,c+RIGHT*2.64,color=EDGE,stroke_width=2))
   for x in range(7):out.add(txt(str(x),17,MUTED).move_to(left+RIGHT*x*unit+DOWN*.2))
   for j,x in enumerate(values):
    y=.18+j*.12;point=left+RIGHT*x*unit+UP*y;anchor=left+RIGHT*mu*unit+UP*y
    out.add(Line(point,anchor,color=color,stroke_width=2,stroke_opacity=.65),Dot(point,radius=.055,color=color))
   out.add(DashedLine(left+RIGHT*mu*unit+DOWN*.07,left+RIGHT*mu*unit+UP*.78,color=YELLOW,dash_length=.07,stroke_width=2))
   score=float(np.sum((values-mu)**2))
   out.add(box(f'제곱거리 합 = {score:.1f}',6.1,.72,color,29).move_to(c+DOWN*.85))
  out.add(box('두 기록의 차이 = 26.0' if reveal else '두 기록의 차이는?',6.6 if VERT else 8,.65,YELLOW,28).move_to([0,-2.8 if VERT else -1.25,0]))
  return out
 return always_redraw(draw)

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
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/158))))
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
  self.at(26);name=txt('Sufficient Statistic',30,YELLOW,7).move_to([0,3.35 if VERT else 1.65,0]);self.play(FadeIn(name),run_time=.7);self.note('충분통계량 · 원자료 전체의 복원은 아님')
 def part_03(self):
  self.condition('전체 정보와 모수 정보는 다르다')
  q=txt('무엇이 사라지지\n않는다는 걸까?' if VERT else '무엇이 사라지지 않는다는 걸까?',44,PURPLE,7 if VERT else 13).move_to([0,1.6 if VERT else .6,0]);self.add(q)
  b=box('원자료의 복원 ≠ μ 정보 보존',7 if VERT else 12,1.1,YELLOW,30).move_to([0,-1.05 if VERT else -.8,0]);self.play(FadeIn(b),run_time=.7);self.note('지정한 모형과 추론 대상 아래에서')
 def part_04(self):
  self.condition('독립·동일 정규분포 · n = 5 · 알려진 같은 분산')
  a,b=data_pair();a[-1].set_opacity(0);b[-1].set_opacity(0)
  self.at(35);self.play(FadeIn(a),run_time=.6)
  self.at(37);self.play(FadeIn(b),run_time=.7)
  self.at(40);self.note('A는 모여 있고 · B는 더 넓게 퍼져 있다',MUTED)
  self.play(Indicate(a[1],color=TEAL),Indicate(b[1],color=PURPLE),run_time=.7)
  self.at(46);a[-1].set_opacity(1);b[-1].set_opacity(1)
  self.play(Indicate(a[-1],color=YELLOW),Indicate(b[-1],color=YELLOW),run_time=.7);self.note('서로 다른 기록 · 평균은 모두 3')
 def part_05(self):
  self.condition('데이터는 그대로 · 평균 후보를 비교')
  a,b=data_pair();self.add(a,b);self.note('기록 A와 B 각각에서 같은 질문을 한다',MUTED)
  self.at(50)
  cards=VGroup(box('후보 평균 3',3.25 if VERT else 5.5,.9,TEAL,29),box('후보 평균 5',3.25 if VERT else 5.5,.9,PURPLE,29)).arrange(RIGHT,buff=.35).move_to([0,-2.65 if VERT else -1.05,0])
  self.play(FadeIn(cards),run_time=.7)
  self.at(56);self.note('어느 평균이 관측된 기록을 더 그럴듯하게 설명할까?')
 def part_06(self):
  self.condition('알려진 같은 분산 · 예시 σ² = 4')
  candidate=ValueTracker(3);self.add(experiment(candidate,False))
  self.note('각 점까지의 거리 → 제곱 → 모두 더하기',MUTED)
  self.at(68);self.note('같은 기록에서 비교: 제곱거리 합이 작을수록 더 그럴듯하다')
  self.play(candidate.animate.set_value(5),run_time=2)
  self.play(candidate.animate.set_value(3),run_time=1.5)
 def part_07(self):
  self.condition('관측값 고정 · 후보 평균만 이동 · σ² = 4')
  candidate=ValueTracker(3);self.add(experiment(candidate,False))
  self.note('평균 후보 3: A = 10 · B = 36',MUTED)
  self.at(77);self.note('후보 평균이 움직이면 두 점수도 함께 변한다',MUTED);self.play(candidate.animate.set_value(5),run_time=2.5)
  self.note('평균 후보 5: A = 30 · B = 56',MUTED)
  self.at(80);self.note('두 점수 사이에는 어떤 관계가 있을까?',YELLOW)
 def part_08(self):
  self.condition('관측값 고정 · 후보 평균만 이동 · σ² = 4')
  candidate=ValueTracker(5);self.add(experiment(candidate,True))
  self.note('56 − 30 = 26',YELLOW)
  self.at(87);self.note('어떤 후보 평균에서도 B − A = 26',YELLOW);self.play(candidate.animate.set_value(1),run_time=1.25);self.play(candidate.animate.set_value(3),run_time=1.25)
  self.note('어떤 후보 평균에서도 B − A = 26',YELLOW)
 def part_09(self):
  self.condition('같은 n · 같은 알려진 분산 → 같은 상대적 지지')
  table=VGroup()
  for label,c,lo,hi in [('A',TEAL,10,30),('B',PURPLE,36,56)]:
   row=box(f'{label}    평균 3: {lo}   →   평균 5: {hi}',7 if VERT else 11,.95 if VERT else .7,c,29)
   table.add(row)
  table.arrange(DOWN,buff=.25).move_to([0,2.25 if VERT else 1.05,0]);self.add(table)
  delta=box('후보 3 → 5의 점수 증가: 둘 다 +20',7 if VERT else 12,.85 if VERT else .65,YELLOW,27).move_to([0,.25 if VERT else -.3,0]);self.add(delta)
  self.note('점수 자체는 달라도 · 후보 사이의 비교는 같다')
  self.at(95)
  same=box('평균 3을 기준 1로 두면\n평균 5의 그럴듯함: 둘 다 약 0.082',7 if VERT else 11,1.25 if VERT else .8,PURPLE,27).move_to([0,-1.5 if VERT else -1.15,0]);self.play(FadeIn(same),run_time=.7)
  self.note('원본 기록은 복원 불가 · 평균 추론 정보는 보존',MUTED)
  self.at(101);self.play(FadeOut(same),run_time=.4)
  mean=box('이 비교를 결정하는 요약: x̄ = 3',7 if VERT else 11,.95,YELLOW,29).move_to([0,-1.5 if VERT else -1.15,0]);self.play(FadeIn(mean),run_time=.6);self.note('고정 n · 알려진 분산에서 표본평균은 충분하다')
 def part_10(self):
  self.condition('표본평균 하나면 언제나 충분할까?')
  a,b=data_pair();self.add(a,b);self.note('두 기록의 평균은 모두 3',YELLOW)
  self.at(108);self.note('항상 충분한 것은 아니다',RED)
  self.at(109);self.condition('모형 변경: 평균과 분산을 모두 모름')
  self.at(112);self.play(Indicate(a[1],color=TEAL),Indicate(b[1],color=PURPLE),run_time=.7);self.note('퍼짐은 다르다 · 평균에서의 제곱거리 합: 10과 36',PURPLE)
 def part_11(self):
  self.condition('평균과 분산 모두 미지 · 표본 수 n 고정')
  table=VGroup()
  for label,q,c in [('A',55,TEAL),('B',81,PURPLE)]:
   table.add(VGroup(box(label,1.1,.95,c,29),box('Σxᵢ = 15',2.5 if VERT else 4,.95,YELLOW,29),box(f'Σxᵢ² = {q}',2.8 if VERT else 4,.95,PURPLE,29)).arrange(RIGHT,buff=.15))
  table.arrange(DOWN,buff=.4).move_to([0,1.9 if VERT else .9,0]);self.add(table)
  self.add(box('합과 제곱합을 함께 보존',7 if VERT else 10,1,YELLOW,32).move_to([0,-.65 if VERT else -.8,0]));self.note('같은 평균이어도 · 퍼짐을 구분해야 한다',MUTED)
  self.at(122);self.note('필요한 요약은 추론 대상과 통계 모형에 따라 달라진다')
 def part_12(self):
  self.condition('예시: 다시 알려진 분산 · 고정 n 정규모형')
  self.add(txt('Minimal Sufficient Statistic',27,YELLOW,7 if VERT else 13).move_to([0,3.35 if VERT else 1.85,0]));self.note('불필요한 구분을 줄이고 · 모수 정보는 유지',MUTED)
  left=box('원본 데이터 X\n그 자체도 충분',3.2 if VERT else 5.2,1.15,TEAL,25).move_to([-1.75,1.8,0] if VERT else [-3.5,.8,0])
  right=box('다른 모든\n충분통계량 S',3.2 if VERT else 5.2,1.15,TEAL,25).move_to([1.75,1.8,0] if VERT else [3.5,.8,0])
  target=box('T = x̄',6,1.2,YELLOW,41).move_to([0,-1 if VERT else -.95,0])
  self.at(133);self.play(FadeIn(left),FadeIn(target),run_time=.6)
  self.play(GrowArrow(Arrow(left.get_bottom(),target.get_top()+LEFT*1.25,color=TEAL,buff=.1,stroke_width=2)),run_time=.5)
  self.at(138);self.play(FadeIn(right),run_time=.6)
  self.play(GrowArrow(Arrow(right.get_bottom(),target.get_top()+RIGHT*1.25,color=TEAL,buff=.1,stroke_width=2)),run_time=.5);self.note('어떤 충분통계량 S에서도 T = g(S)로 계산 가능')
 def part_13(self):
  self.condition('서로 다른 최소화 기준')
  a=box('통계적 최소성',6 if VERT else 5.7,1.2,YELLOW,35);b=box('저장량·계산량 최소',6 if VERT else 5.7,1.2,RED,32)
  if VERT:a.move_to([0,2.35,0]);b.move_to([0,-.35,0]);neq=txt('≠',59,RED).move_to([0,1,0])
  else:a.move_to([-3.5,.5,0]);b.move_to([3.5,.5,0]);neq=txt('≠',59,RED).move_to([0,.5,0])
  self.add(a,b,neq);self.note('통계적 정보의 구분을 줄이는 최소성',MUTED)
 def part_14(self):
  self.condition(MODEL+' · n 고정')
  db=database(5.5,2.8 if VERT else 2.2).move_to([0,1.2,0] if VERT else [-3.5,.2,0]);self.add(db)
  self.add(txt('n = 1,000,000',32,TEAL).move_to([0,3.35,0] if VERT else [-3.5,1.75,0]));self.note('얼마나 많이 남길까? → 무엇을 보존할까?')
  self.at(152);summary=box('x̄',6 if VERT else 5,1.5,YELLOW,67).move_to(db)
  self.play(ReplacementTransform(db,summary),run_time=.8)
  info=box('평균을 추론하는 데\n필요한 정보 보존' if VERT else '평균 추론에 필요한 정보 보존',6.5,1.3,PURPLE,33).move_to([0,-1.25,0] if VERT else [3.5,.3,0]);self.play(FadeIn(info),run_time=.6)
  self.note('알고 싶은 대상에 관한 정보를 남긴다')
