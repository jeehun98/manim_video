"""Softmax 07 — log-sum-exp geometry and directional sensitivity. 180s."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=180
CAPTIONS=[
(0,'앞에서 소프트맥스는 여러 점수를\n하나의 분포로 바꾸는 함수라고 했습니다.'),
(5,'그런데 소프트맥스는\n조금 더 큰 수학적 구조 안에 들어 있습니다.'),
(10,'먼저 여러 값 중에서\n가장 큰 값을 고르는 함수를 생각해보겠습니다.'),
(15,'예를 들어 [1, 2, 3]의 최댓값은 3입니다.'),
(19,'그래프로 보기 위해 두 입력 [t, 0]을 생각해보겠습니다.\n최댓값은 t가 음수면 0, 양수면 t입니다.'),
(26,'가장 큰 값이 바뀌는 지점에서는\n그래프가 꺾이고, 기울기가 매끄럽게 이어지지 않습니다.'),
(32,'그래서 최댓값과 비슷하게 동작하면서도\n더 부드러운 함수를 생각할 수 있습니다.'),
(37,'그중 하나가 로그섬엑스프,\nLog-Sum-Exp입니다.'),
(41,'각 값을 지수함수에 넣고, 모두 더한 뒤,\n마지막에 로그를 취합니다.'),
(46,'그래프에서는 꺾인 모서리가 부드럽게 이어집니다.\n왜 이것이 최댓값과 관련이 있을까요?'),
(52,'가장 큰 입력을 m이라고 하면,\n다음과 같이 식을 바꿔 쓸 수 있습니다.'),
(58,'가장 큰 값에 해당하는 항은\ne의 0제곱, 즉 1이 됩니다.'),
(63,'그보다 작은 값들은 음수의 지수를 가집니다.\n최댓값과의 차이가 커지면 그 항들은 작아집니다.'),
(70,'따라서 최댓값을 중심으로 움직이면서도,\n나머지 값들의 영향은 남겨둡니다.'),
(76,'이런 이유로 로그섬엑스프를\n최댓값의 부드러운 형태, 스무스 맥스로 볼 수 있습니다.'),
(82,'그런데 여기서 더 흥미로운 일이 생깁니다.\n이 함수를 한 입력에 대해 미분해보겠습니다.'),
(88,'로그를 미분하면 전체 합의 역수가 나오고,\n안쪽의 합을 미분하면 e의 xᵢ제곱이 남습니다.'),
(95,'정리하면 우리가 계속 봐왔던 그 식,\n바로 소프트맥스가 됩니다.'),
(101,'각 입력에 대한 미분을 모은 그래디언트가\n소프트맥스라는 뜻입니다.'),
(107,'이제 그래프 위에서 기울기를 보겠습니다.\n두 입력 [t, 0] 중 첫 입력만 움직여봅시다.'),
(113,'t가 작을 때는 접선이 완만하고,\n첫 입력의 소프트맥스 값도 작습니다.'),
(119,'t가 커지면 접선이 가팔라지고,\n첫 입력의 소프트맥스 값도 커집니다.'),
(125,'로그섬엑스프는 여러 입력을 받아 하나의 값을 만들고,\n소프트맥스는 각 입력 방향의 증가율을 나타냅니다.'),
(132,'이번에는 입력 [1, 2, 3]에서\n각 입력을 하나씩 조금 늘려보겠습니다.'),
(138,'그래프의 가로축은 늘린 양,\n세로축은 로그섬엑스프가 증가한 양입니다.'),
(143,'같은 양을 늘려도, 점수가 큰 세 번째 입력을\n늘릴 때 함수값이 더 많이 증가합니다.'),
(149,'각 곡선의 시작점 기울기는\n약 0.09, 0.24, 0.67입니다.'),
(154,'이 값들을 모으면\n바로 [1, 2, 3]의 소프트맥스 분포가 됩니다.'),
(159,'따라서 소프트맥스는 확률 분포로 해석할 수 있을 뿐 아니라,\n스무스 맥스가 각 입력에 얼마나 민감한지를\n나타내는 기울기이기도 합니다.'),
(167,'점수를 분포로 바꾸던 함수가,\n최댓값을 부드럽게 만든 함수의 그래디언트였던 것입니다.'),
(173,'다음에는 이 관계가 컴퓨터에서 소프트맥스를\n안정적으로 계산하는 방법과 어떻게 연결되는지\n살펴보겠습니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def inline(*a):return VGroup(*a).arrange(RIGHT,buff=.2)
def exp(power,color=INK):
 b=txt('e',38,color);s=txt(power,22,color).next_to(b,UR,buff=.02).shift(DOWN*.1);return VGroup(b,s)
def frac(a,b):
 l=Line(LEFT,RIGHT,color=INK).set_width(max(a.width,b.width)+.3)
 return VGroup(a.next_to(l,UP,buff=.14),l,b.next_to(l,DOWN,buff=.14))
def lse(x):
 x=np.asarray(x,dtype=float);m=x.max();return m+np.log(np.exp(x-m).sum())
def sig(t):return 1/(1+np.exp(-t))
def softplus(t):return np.logaddexp(0,t)
def base_axes():
 ax=Axes(x_range=[-4,4,1],y_range=[0,4.5,1],x_length=6.5,y_length=4.2,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.3,'tip_width':.12,'tip_height':.12}).move_to(UP*.2)
 labels=VGroup(*[txt(str(v).replace('-','−'),20,MUTED).next_to(ax.c2p(v,0),DOWN,buff=.13) for v in [-4,-2,0,2,4]],*[txt(str(v),20,MUTED).next_to(ax.c2p(-4,v),LEFT,buff=.13) for v in [0,2,4]])
 return ax,labels
class SoftmaxLSE(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('Softmax를 만드는 더 큰 구조',30,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('07  /  Smooth Max의 기울기',25,MINT).move_to(UP*4.65),self.head,self.sub)
  intro=VGroup(txt('여러 점수',36,BLUE),txt('↓',30,MUTED),txt('하나의 분포',36,MINT)).arrange(DOWN,buff=.5).move_to(UP*.3)
  self.play(FadeIn(intro),run_time=.5)
  self.cue(1);self.heading('분포 뒤에 숨어 있는 곡선')
  self.cue(2);self.play(FadeOut(intro),run_time=.3)
  example=txt('max([1, 2, 3]) = 3',40,GOLD).move_to(UP*.5);self.play(FadeIn(example),run_time=.5)
  self.cue(3);self.play(Indicate(example),run_time=.6)
  self.cue(4);self.play(FadeOut(example),run_time=.3);self.heading('한 입력만 움직이는 단면: [t, 0]')
  ax,labs=base_axes()
  hard=VGroup(Line(ax.c2p(-4,0),ax.c2p(0,0),color=GOLD,stroke_width=5),Line(ax.c2p(0,0),ax.c2p(4,4),color=GOLD,stroke_width=5))
  legend=txt('노랑: max(t, 0)',25,GOLD).move_to(UP*2.9)
  xlabel=txt('움직이는 첫 입력 t  ·  두 번째 입력은 0',23,MUTED).move_to(DOWN*2.7)
  self.play(FadeIn(ax),FadeIn(labs),Create(hard),FadeIn(legend),FadeIn(xlabel),run_time=.8)
  self.cue(5)
  corner=Circle(radius=.25,color=PINK).move_to(ax.c2p(0,0));sides=txt('왼쪽 기울기 0  →  오른쪽 기울기 1',26,GOLD).move_to(DOWN*3.7)
  self.play(Create(corner),FadeIn(sides),run_time=.5)
  self.cue(6);self.heading('최댓값의 모서리를 부드럽게')
  smooth=ax.plot(softplus,x_range=[-4,4,.035],color=MINT,stroke_width=4)
  self.play(Create(smooth),FadeOut(corner),FadeOut(sides),run_time=1.2)
  self.cue(7)
  self.play(Transform(legend,txt('노랑: Max   ·   민트: Log-Sum-Exp',23,MINT).move_to(legend)),run_time=.4)
  self.cue(8)
  definition=inline(txt('LSE(x) = log',30),inline(txt('Σᵢ',29),exp('xᵢ'))).move_to(DOWN*3.7)
  self.play(FadeIn(definition),run_time=.5)
  self.cue(9)
  near=Dot(ax.c2p(0,np.log(2)),color=MINT);gap=Line(ax.c2p(0,0),ax.c2p(0,np.log(2)),color=PINK,stroke_width=4)
  self.play(FadeIn(near),Create(gap),run_time=.5)
  self.cue(10)
  self.play(*[FadeOut(m) for m in [ax,labs,hard,smooth,legend,xlabel,definition,near,gap]],run_time=.3)
  self.heading('최댓값 m을 밖으로 꺼내면')
  formula=inline(txt('LSE(x) = m + log',29),txt('Σᵢ',29),exp('xᵢ − m',GOLD)).move_to(UP*1.2)
  mlabel=txt('m = max(x₁, …, xₙ)',28,GOLD).move_to(UP*2.5)
  self.play(FadeIn(formula),FadeIn(mlabel),run_time=.5)
  self.cue(11)
  terms=txt('[1, 2, 3] → [−2, −1, 0]',31,BLUE).move_to(DOWN*.3)
  weights=txt('지수값: [0.135, 0.368, 1]',30,MINT).move_to(DOWN*1.5)
  self.play(FadeIn(terms),FadeIn(weights),run_time=.5)
  self.cue(12)
  self.play(Transform(terms,txt('[−3, 0, 3] → [−6, −3, 0]',30,BLUE).move_to(terms)),Transform(weights,txt('지수값: [0.0025, 0.0498, 1]',28,MINT).move_to(weights)),run_time=1)
  self.cue(13)
  correction=txt('LSE ≈ 3 + 0.051 = 3.051',30,GOLD).move_to(DOWN*2.7)
  self.play(FadeIn(correction),run_time=.5)
  self.cue(14)
  bound=txt('max(x) ≤ LSE(x) ≤ max(x) + log n',25,MUTED).move_to(DOWN*3.9)
  self.play(FadeIn(bound),run_time=.5)
  self.cue(15)
  self.play(*[FadeOut(m) for m in [formula,mlabel,terms,weights,correction,bound]],run_time=.3);self.heading('Smooth Max를 미분하면?')
  start=inline(frac(txt('∂',34),txt('∂xᵢ',34)),txt('log',34),txt('Σⱼ',32),exp('xⱼ')).move_to(UP*.7)
  self.play(FadeIn(start),run_time=.5)
  self.cue(16)
  chain=inline(frac(txt('1',36),inline(txt('Σⱼ',30),exp('xⱼ'))),txt('×',34),exp('xᵢ',GOLD)).move_to(UP*.7)
  self.play(ReplacementTransform(start,chain),run_time=.6)
  chainnote=txt('로그의 미분  ×  안쪽 합의 미분',27,MUTED).move_to(DOWN*1.5);self.play(FadeIn(chainnote),run_time=.4)
  self.cue(17)
  result=inline(frac(txt('∂LSE',33),txt('∂xᵢ',33)),txt('=',32),frac(exp('xᵢ',GOLD),inline(txt('Σⱼ',30),exp('xⱼ')))).move_to(UP*.7)
  self.play(ReplacementTransform(chain,result),Transform(chainnote,txt('바로 Softmax의 i번째 출력',29,MINT).move_to(chainnote)),run_time=.6)
  self.cue(18)
  gradient=txt('∇LSE(x) = softmax(x)',38,MINT).move_to(DOWN*3)
  self.play(FadeIn(gradient),run_time=.5)
  self.cue(19)
  self.play(FadeOut(result),FadeOut(chainnote),FadeOut(gradient),run_time=.3);self.heading('접선의 기울기 = 첫 번째 Softmax 값')
  ax,labs=base_axes();smooth=ax.plot(softplus,x_range=[-4,4,.035],color=MINT,stroke_width=4)
  label=txt('LSE([t, 0]) = log(1 + exp(t))',26,MINT).move_to(UP*2.9)
  xlabel=txt('첫 입력 t  ·  두 번째 입력 0 고정',24,MUTED).move_to(DOWN*2.7)
  tracker=ValueTracker(-3)
  dot=always_redraw(lambda:Dot(ax.c2p(tracker.get_value(),softplus(tracker.get_value())),color=GOLD,radius=.09))
  tangent=always_redraw(lambda:Line(ax.c2p(tracker.get_value()-.8,softplus(tracker.get_value())-.8*sig(tracker.get_value())),ax.c2p(tracker.get_value()+.8,softplus(tracker.get_value())+.8*sig(tracker.get_value())),color=GOLD,stroke_width=4))
  readlabel=txt('기울기 = p₁ =',29,GOLD).move_to([-1,-3.5,0]);number=DecimalNumber(sig(-3),mob_class=Text,num_decimal_places=3,font_size=31,color=GOLD).move_to([1.6,-3.5,0]);number.add_updater(lambda m:m.set_value(sig(tracker.get_value())))
  bar=always_redraw(lambda:Rectangle(width=6*sig(tracker.get_value()),height=.24,stroke_width=0,fill_color=GOLD,fill_opacity=.9).move_to([-3+3*sig(tracker.get_value()),-4.2,0]))
  self.play(FadeIn(ax),FadeIn(labs),Create(smooth),FadeIn(label),FadeIn(xlabel),run_time=.7);self.add(dot,tangent,readlabel,number,bar)
  self.cue(20);self.play(tracker.animate.set_value(-1.5),run_time=3,rate_func=linear)
  self.cue(21);self.play(tracker.animate.set_value(3),run_time=4,rate_func=linear)
  self.cue(22);self.play(tracker.animate.set_value(0),run_time=2.5)
  self.cue(23)
  graph=VGroup(ax,labs,smooth,label,xlabel,dot,tangent,readlabel,number,bar)
  for mob in graph.get_family():mob.clear_updaters()
  self.play(FadeOut(graph),run_time=.3)
  self.heading('3개의 입력 방향, 3개의 기울기')
  base=np.array([1.,2.,3.]);basevalue=lse(base);p=np.exp(base-base.max());p/=p.sum()
  ax2=Axes(x_range=[0,.6,.2],y_range=[0,.5,.1],x_length=6.3,y_length=3.5,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.3,'tip_width':.12,'tip_height':.12}).move_to(UP*.2)
  lab2=VGroup(*[txt(str(v),20,MUTED).next_to(ax2.c2p(v,0),DOWN,buff=.12) for v in [0,.2,.4,.6]],*[txt(str(v),20,MUTED).next_to(ax2.c2p(0,v),LEFT,buff=.12) for v in [0,.2,.4]])
  def change(i,e):
   x=base.copy();x[i]+=e;return lse(x)-basevalue
  curves=VGroup(*[ax2.plot(lambda e,i=i:change(i,e),x_range=[0,.6,.01],color=c,stroke_width=4) for i,c in enumerate([BLUE,GOLD,PINK])])
  legend=VGroup(*[txt(s,22,c) for s,c in zip(['x₁만 증가','x₂만 증가','x₃만 증가'],[BLUE,GOLD,PINK])]).arrange(RIGHT,buff=.35).move_to(UP*2.65)
  xname=txt('한 입력을 늘린 양 ε',24,MUTED).move_to(DOWN*2.5)
  yname=txt('세로축: LSE의 증가량  ·  기준 입력 [1, 2, 3]',23,MUTED).move_to(UP*3.1)
  self.play(FadeIn(ax2),FadeIn(lab2),FadeIn(legend),FadeIn(xname),FadeIn(yname),run_time=.6)
  self.cue(24);self.play(Create(curves),run_time=1.3)
  eps=ValueTracker(0)
  markers=always_redraw(lambda:VGroup(*[Dot(ax2.c2p(eps.get_value(),change(i,eps.get_value())),radius=.075,color=c) for i,c in enumerate([BLUE,GOLD,PINK])]))
  self.add(markers)
  self.cue(25);self.play(eps.animate.set_value(.5),run_time=3,rate_func=linear)
  self.cue(26)
  slopes=VGroup(*[Line(ax2.c2p(0,0),ax2.c2p(.23,float(pi)*.23),color=c,stroke_width=6) for pi,c in zip(p,[BLUE,GOLD,PINK])])
  self.play(Create(slopes),run_time=.6)
  numeric=txt('시작점 기울기: [0.090, 0.245, 0.665]',27,MINT).move_to(DOWN*3.4)
  self.play(FadeIn(numeric),run_time=.4)
  self.cue(27);self.play(Transform(numeric,txt('∇LSE([1, 2, 3]) = softmax([1, 2, 3])',26,MINT).move_to(numeric)),run_time=.5)
  self.cue(28)
  group=VGroup(ax2,lab2,legend,xname,yname,curves,markers,slopes,numeric)
  for mob in group.get_family():mob.clear_updaters()
  self.play(FadeOut(group),run_time=.3);self.heading('확률이면서, 입력별 민감도')
  summary=VGroup(txt('Log-Sum-Exp',39,MINT),txt('여러 입력 → 하나의 부드러운 최댓값',27,MUTED),txt('↓  각 입력 방향으로 미분',28,GOLD),txt('Softmax',43,BLUE),txt('입력별 기울기를 모은 벡터',29,BLUE)).arrange(DOWN,buff=.4).move_to(UP*.2)
  self.play(FadeIn(summary),run_time=.5)
  self.cue(29);self.play(Indicate(summary[3]),run_time=.7)
  self.cue(30);self.play(FadeOut(summary),run_time=.3);self.heading('NEXT  /  안정적으로 계산하는 방법')
  end=VGroup(txt('Log-Sum-Exp ↔ Softmax',35,MINT),txt('수학적 구조에서 실제 계산으로',29,GOLD)).arrange(DOWN,buff=.7).move_to(UP*.3)
  self.play(FadeIn(end),run_time=.5);self.until(DURATION)
