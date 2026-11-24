"""176-second Bernoulli-to-binomial short, using exact user sentence timings."""
import sys,json,math
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.genfunc01_dice.scene import GFScene,txt,eq,INK,MUTED
GREEN,GRAY,GOLD,BLUE='#67E3C1','#8995A8','#FFD166','#67B7FF'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
OBS=[1,0,1,1,0,1,1,0,1,1]
OTHER=[0,1,1,1,0,0,1,1,1,1]
def likelihood(mu):return mu**7*(1-mu)**3
def loglik(mu):return 7*math.log(mu)+3*math.log1p(-mu)
def token(x,size=.57):
 c=GREEN if x else GRAY
 return VGroup(RoundedRectangle(width=size,height=size*.95,corner_radius=.08,stroke_color=c,fill_color=c,fill_opacity=.13),txt(str(x),size=29,color=c,width=size-.1))
def sequence(values,y=0,width=7.1):
 g=VGroup(*[token(x) for x in values]).arrange(RIGHT,buff=.12)
 if g.width>width:g.scale_to_fit_width(width)
 return g.move_to([0,y,0])
def coin(x):
 c=GREEN if x else GRAY
 return VGroup(Circle(radius=.68,color=c,fill_color=c,fill_opacity=.12),txt('앞' if x else '뒤',size=45,color=c))
def bernchart(mu,y=1):
 g=VGroup(Line([-2.5,y-1,0],[2.5,y-1,0],color=MUTED,stroke_width=1.5))
 for x,p,c,label in [(-1.3,1-mu,GRAY,'0'),(1.3,mu,GREEN,'1')]:
  h=max(p*2.7,.01)
  g.add(Rectangle(width=1.05,height=h,fill_color=c,fill_opacity=.85,stroke_width=0).move_to([x,y-1+h/2,0]),txt(label,y-1.5,31,c,x=x),eq(f'{p:.1f}',y-1+h+.35,36,c,x=x))
 return g

def curve_axes(log=False,center=.8):
 a=Axes(x_range=[0,1,.5],y_range=[0,23,5] if log else [0,.0025,.001],x_length=6.5,y_length=2.9,tips=False,axis_config=dict(color=MUTED,stroke_width=1.3)).move_to([0,center,0])
 curve=a.plot((lambda mu:loglik(mu)+28) if log else likelihood,x_range=[.02,.98,.005] if log else [0,1,.005],color=GREEN,stroke_width=3)
 bottom=0
 labels=VGroup(*[eq(str(x),size=24,color=MUTED,x=a.c2p(x,bottom)[0],y=a.c2p(x,bottom)[1]-.35,width=.8) for x in [0,.5,1]],eq(r'\mu',size=31,color=GREEN).move_to(a.c2p(1,bottom)+RIGHT*.45))
 if log:
  labels.add(*[eq(str(v),size=19,color=MUTED).move_to(a.c2p(0,v+28)+LEFT*.36) for v in [-28,-18,-8]])
 return a,curve,labels

def binchart(n=10,mu=.7,y=1):
 g=VGroup(Line([-3.6,y-1.4,0],[3.6,y-1.4,0],color=MUTED,stroke_width=1.5))
 for k in range(n+1):
  p=math.comb(n,k)*mu**k*(1-mu)**(n-k);x=-3.25+6.5*k/n;h=max(p*9,.01)
  g.add(Rectangle(width=.46,height=h,fill_color=GOLD if k==7 else GREEN,fill_opacity=.82,stroke_width=0).move_to([x,y-1.4+h/2,0]),txt(str(k),y-1.8,22,GOLD if k==7 else MUTED,x=x,width=.5))
 return g
class BernoulliScene(GFScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.header)
  self.header=VGroup(txt('STATISTICS  /  BERNOULLI & BINOMIAL',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
class Shot01(BernoulliScene):
 shot=0
 def s01(self):
  c=coin(1).scale(1.7).move_to([0,2.4,0]);self.play(FadeIn(c),Rotate(c,angle=TAU),run_time=1.2);self.show(txt('불확실성을 어떻게 표현할까?',-.2,37));self.to(4)
  self.show(txt('확률 → 결과  :  예측',-1.5,34,GREEN),txt('결과 → 확률  :  추정',-3,34,GOLD));self.to(12)
  self.clear();pair=VGroup(coin(1),coin(0)).arrange(RIGHT,buff=2.3).move_to([0,2.6,0]);self.show(pair,eq(r'X\sim\mathrm{Bern}(\mu)',-2.2,57,GREEN));self.to(15)
  outcomes=VGroup(eq('1',size=86,color=GREEN),eq('0',size=86,color=GRAY)).arrange(RIGHT,buff=3.2).move_to([0,.2,0]);self.play(TransformFromCopy(pair,outcomes),run_time=.8);self.to(20)
  self.clear();chart=bernchart(.5,1.8);self.show(chart,txt('이산확률변수  /  x ∈ {0, 1}',4.7,29));self.to(26)
  conditions=eq(r'P(X=x)\geq0,\qquad\sum_x P(X=x)=1',-1.6,44);self.show(conditions);self.to(31)
  self.play(FadeOut(conditions),run_time=.3)
  probs=eq(r'P(X=1)=\mu,\quad P(X=0)=1-\mu',-.9,43);self.show(probs)
  self.play(Transform(chart,bernchart(.7,1.8)),run_time=1);self.play(Transform(chart,bernchart(.3,1.8)),run_time=1);self.to(37)
  self.show(eq(r'P(X=x\mid\mu)=\mu^x(1-\mu)^{1-x}',-2.4,48),txt('0 ≤ μ ≤ 1',-.1,24,MUTED));self.to(41)
  self.show(eq(r'\mathbb E[X]=\mu,\quad\mathrm{Var}(X)=\mu(1-\mu)',-4,44,GOLD));self.to(46)
class Shot02(BernoulliScene):
 shot=1
 def s02(self):
  question=eq(r'\mu=?',2,101,GOLD);self.show(question,txt('알 수 없는 성공 확률',-.1,35));self.to(50)
  self.clear();row=sequence(OBS,3.7);self.play(LaggedStart(*[FadeIn(t) for t in row],lag_ratio=.1),run_time=1.4);self.show(txt('앞면 7회 · 뒷면 3회',1.8,38,GOLD));self.to(54)
  factors=VGroup(*[eq(r'\mu' if x else r'1-\mu',size=23,color=GREEN if x else GRAY,width=.7).move_to([t.get_x(),2.65,0]) for x,t in zip(OBS,row)]);self.show(factors,txt('독립 · 동일한 성공 확률 μ',.4,29,MUTED))
  expression=eq(r'L(\mu)=\prod_{i=1}^{10}P(X_i=x_i\mid\mu)=\mu^7(1-\mu)^3',-1.6,43)
  self.play(TransformFromCopy(factors,expression),run_time=1);self.show(txt('특정 관측 순서 전체의 확률 · 조합계수 없음',-3.5,25,MUTED));self.to(63)
  self.clear();self.show(txt('관측 고정: N=10, k=7',4.8,29,GOLD),eq(r'L(\mu)=\mu^7(1-\mu)^3',3.5,53,GREEN))
  axes,curve,labels=curve_axes(center=1);self.show(axes,curve,labels)
  tracker=ValueTracker(.35);dot=Dot(axes.c2p(.35,likelihood(.35)),radius=.08,color=GOLD);dot.add_updater(lambda m:m.move_to(axes.c2p(tracker.get_value(),likelihood(tracker.get_value()))));self.add(dot)
  value=DecimalNumber(.35,num_decimal_places=2,font_size=37,color=GOLD).move_to([.6,-1.45,0]);value.add_updater(lambda m:m.set_value(tracker.get_value()));self.show(eq(r'\mu=',-1.45,40,GOLD,x=-.4),value);self.to(66)
  for mu in [.2,.5,.9]:self.play(tracker.animate.set_value(mu),run_time=1,rate_func=linear)
  self.show(txt('가능도 함수',-2.6,36,GREEN),txt('μ의 확률분포가 아니다',-3.8,25,MUTED));self.to(72)
  self.play(tracker.animate.set_value(.69),run_time=1.1);self.show(txt('최대가능도추정  /  MLE',-4.5,26,GOLD),run_time=.5);self.to(77);dot.clear_updaters();value.clear_updaters()
class Shot03(BernoulliScene):
 shot=2
 def s03(self):
  expression=eq(r'L(\mu)=\mu^7(1-\mu)^3',4.4,57,GREEN);self.show(expression)
  axes,curve,labels=curve_axes(center=.7);self.show(axes,curve,labels,txt('어떻게 최대화할 수 있을까?',-2.6,34,GOLD));self.to(79)
  self.show(txt('로그함수와 미적분학',-4,34));self.to(82)
  self.clear();expression=eq(r'L(\mu)=\mu^7(1-\mu)^3',4.6,49,GREEN);logexpr=eq(r'\ell(\mu)=\ln L(\mu)=7\ln\mu+3\ln(1-\mu)',3,47)
  self.show(expression);self.play(TransformFromCopy(expression,logexpr),run_time=1)
  axes,curve,labels=curve_axes(center=.4);self.show(axes,curve,labels);self.to(87)
  newaxes,newcurve,newlabels=curve_axes(True,center=.4)
  self.play(Transform(axes,newaxes),Transform(curve,newcurve),Transform(labels,newlabels),run_time=1.3)
  line=DashedLine(newaxes.c2p(.7,0),newaxes.c2p(.7,loglik(.7)+28),color=GOLD);self.show(line,txt('단조증가 → 최댓값의 가로 위치는 동일',-2.4,28,GOLD),txt('로그가능도: 0 < μ < 1',-3.6,26,MUTED));self.to(91)
  self.clear();self.show(eq(r'\ell(\mu)=7\ln\mu+3\ln(1-\mu)',4.4,52))
  derivative=eq(r'\ell\prime(\mu)=\frac7\mu-\frac3{1-\mu}=0',2.2,65);self.show(derivative)
  self.show(eq(r'7(1-\mu)-3\mu=0',.1,57),eq(r'\ell\prime\prime(\mu)=-\frac7{\mu^2}-\frac3{(1-\mu)^2}<0',-3.8,38,MUTED));self.to(96)
  estimate=eq(r'\hat\mu=\frac7{10}=0.7',-1.7,83,GOLD);self.show(estimate);self.to(99)
  self.clear();row=sequence(OBS,3.5);self.show(row,eq(r'\frac{1+0+1+1+0+1+1+0+1+1}{10}=\frac7{10}',1,49,GOLD));self.to(103)
  self.show(eq(r'\hat\mu_{\mathrm{MLE}}=\frac1N\sum_{i=1}^N X_i=\bar X',-1.7,62,GREEN),txt('최대가능도추정량 = 표본평균',-3.6,32));self.to(107)
class Shot04(BernoulliScene):
 shot=3
 def s04(self):
  a=sequence(OBS,3.5);b=sequence(OTHER,1.8);self.show(a,b,txt('서로 다른 두 관측 순서',4.7,29,MUTED));self.to(111)
  self.play(Indicate(a,color=GOLD),Indicate(b,color=GOLD),run_time=1)
  f=eq(r'L(\mu)=\mu^7(1-\mu)^3',-.5,62);self.play(TransformFromCopy(VGroup(a,b),f),run_time=1);self.show(txt('둘 다 성공 횟수 k=7',-2.1,35,GOLD));self.to(116)
  self.clear();seven=eq('7',3.1,110,GOLD);self.play(TransformFromCopy(a,seven),run_time=.7)
  self.show(eq(r'T(X_1,\ldots,X_N)=\sum_{i=1}^N X_i',1.1,58),eq(r'L(\mu)=\mu^T(1-\mu)^{N-T}',-.8,50),txt('μ에 관한 표본 정보는 유지',-2.3,32,GREEN));self.to(124)
  self.show(txt('충분통계량  /  Sufficient Statistic',-3.8,29,GOLD));self.to(126)
  self.clear();line=NumberLine(x_range=[0,10,1],length=7,include_numbers=True,font_size=22).move_to([0,1.1,0]);self.show(line,Dot(line.n2p(7),radius=.13,color=GOLD),eq(r'K=\sum_{i=1}^N X_i',3.5,64),txt('성공 횟수 자체는 어떤 분포를 따를까?',-1.6,33));self.to(131)
class Shot05(BernoulliScene):
 shot=4
 def s05(self):
  label=eq(r'K\sim\mathrm{Bin}(N,\mu)',4.6,56,GREEN);self.show(label,run_time=.4);self.to(132)
  rows=VGroup(*[VGroup(sequence(xs,width=2.5),eq(r'\mu^2(1-\mu)',size=43,color=GREEN)).arrange(RIGHT,buff=.6) for xs in [[1,1,0],[1,0,1],[0,1,1]]]).arrange(DOWN,buff=.6).move_to([0,1.9,0]);example_note=txt('3번 중 성공 2번',-1.1,32,GOLD);self.show(rows[0],example_note);self.to(137)
  self.play(FadeIn(rows[1]),FadeIn(rows[2]),run_time=1)
  total=eq(r'P(K=2)=3\mu^2(1-\mu)',-2.9,60,GOLD);self.play(TransformFromCopy(rows,total),run_time=1);self.to(144)
  self.play(FadeOut(rows),FadeOut(example_note),run_time=.4)
  combination=eq(r'\binom32=3',2,76,GOLD);self.show(combination,txt('하나의 순서 확률 × 가능한 순서 수',.1,31));self.to(150)
  self.play(Transform(combination,eq(r'\binom Nk=\frac{N!}{k!(N-k)!}',2,67,GOLD)),run_time=.7);self.to(153)
  self.play(FadeOut(total),run_time=.3);self.show(eq(r'P(K=k)=\binom Nk\mu^k(1-\mu)^{N-k}',-2.3,56,GREEN),txt('k = 0, 1, …, N',-3.7,29,MUTED));self.to(159)
  self.clear();chart=binchart();self.show(chart,txt('이항분포: N=10, μ=0.7 고정',4.7,30,GREEN),eq(r'P(K=k)=\binom{10}{k}0.7^k0.3^{10-k}',3.5,43),txt('가로축: 성공 횟수 k',-1.8,30,GOLD),txt('가능도: k=7 고정, μ를 변화',-3.2,29,MUTED));self.to(166)
class Shot06(BernoulliScene):
 shot=5
 def s06(self):
  left=VGroup(eq(r'X\sim\mathrm{Bern}(\mu)',size=39,color=GREEN,width=3.4),txt('한 번의 시행',-1,28));right=VGroup(eq(r'K\sim\mathrm{Bin}(N,\mu)',size=39,color=GOLD,width=3.4),txt('여러 시행의 성공 횟수',-1,25,width=3.5));VGroup(left,right).arrange(RIGHT,buff=.5).move_to([0,3.4,0]);self.show(left,right)
  self.show(txt('기댓값 · 분산',1.5,35),txt('가능도 → 로그 → 미분 → 모수 추정',.1,31,GOLD));self.to(171)
  self.show(txt('충분통계량 → 이항분포',-1.4,34,GREEN));self.to(174)
  self.show(txt('가장 단순한 확률분포에서\n시작되는 통계학',-3.4,36));self.to(176)
