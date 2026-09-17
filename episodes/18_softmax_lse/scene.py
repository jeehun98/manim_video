"""Softmax 07 — log-sum-exp geometry and directional sensitivity. 176s."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=176
CAPTIONS=[
 (0, 'Max는 여러 값 중에서\n가장 큰 값 하나를 그대로 고르는 함수입니다.'),
 (5, '예를 들어 2와 5를 넣으면,\n큰 값인 5가 나옵니다.'),
 (10, '작은 값을 2에서 4로 올려도 결과는 5입니다.\n아직 가장 큰 값이 아니기 때문입니다.'),
 (16, '하지만 6이 되면, 이제 그 값을 따라갑니다.'),
 (20, '한 값을 0으로 고정하면 더 익숙합니다.\nMax(t, 0)는 바로 ReLU입니다.'),
 (26, '0을 기준으로 따라가는 입력이 바뀌면서\n그래프가 꺾입니다.'),
 (31, '이 모서리를 부드럽게 이어서,\n최댓값과 비슷한 값을 내게 만들 수 있을까요?'),
 (37, '그런 함수 중 하나가 Log-Sum-Exp,\n즉 로그섬엑스프입니다.'),
 (42, '각 입력에 지수함수를 적용하고,\n모두 더한 뒤 로그를 취합니다.'),
 (47, '노란 Max 곡선과 비슷하지만,\n민트색 곡선은 모서리 없이 부드럽게 이어집니다.'),
 (53, '숫자로 비교해볼까요? 2와 5의 Max는 5이고,\n로그섬엑스프는 약 5.05입니다.'),
 (60, '0과 10처럼 두 값이 멀어지면,\n약 10.00005로 최댓값에 더 가까워집니다.'),
 (66, '반대로 두 값이 같으면 차이가 더 남습니다.\n로그섬엑스프는 최댓값과 똑같은 함수는 아닙니다.'),
 (72, '가장 큰 값을 중심으로 하되,\n작은 값의 영향도 남기는 부드러운 근사입니다.'),
 (77, '여기까지 두 함수 모두 출력은 숫자 하나입니다.\n이제 각 입력의 영향력을 살펴보겠습니다.'),
 (83, '입력을 조금 바꿀 때 출력이 얼마나 변하는지,\n그 영향력을 나타내는 것이 미분입니다.'),
 (89, '로그를 미분하면 전체 합의 역수가 나오고,\n안쪽의 합을 미분하면 e의 xᵢ제곱이 남습니다.'),
 (96, '정리하면 바로 소프트맥스입니다.\n각 입력의 영향력이 소프트맥스 값으로 나타납니다.'),
 (102, '각 입력에 대한 미분을 모은 벡터,\n그래디언트가 소프트맥스라는 뜻입니다.'),
 (108, '그래프 위 접선으로 살펴보겠습니다.\n첫 번째 입력 t만 움직여봅시다.'),
 (114, 't가 작으면 접선이 완만합니다.\n작은 입력도 영향을 주지만, 그 정도가 작습니다.'),
 (120, 't가 커지면 접선이 가팔라집니다.\n이제 첫 번째 입력의 영향력이 커집니다.'),
 (126, '두 입력이 같을 때는 각각의 영향력이 0.5입니다.\nMax와 달리 양쪽의 영향이 부드럽게 이어집니다.'),
 (133, '입력이 세 개여도 같습니다.\n[1, 2, 3]의 각 입력을 하나씩 늘려보겠습니다.'),
 (139, '가로축은 입력을 늘린 양,\n세로축은 로그섬엑스프가 증가한 양입니다.'),
 (144, '같은 양을 늘려도, 큰 입력을 늘릴 때\n함수값이 더 많이 증가합니다.'),
 (149, '출발점에서의 기울기는\n약 0.09, 0.24, 0.67입니다.'),
 (154, '각 입력의 영향력을 모으면\n바로 소프트맥스 분포가 됩니다.'),
 (159, '정리하면, 로그섬엑스프는 부드러운 최댓값 하나를 만들고,\n소프트맥스는 각 입력이 그 값에 미치는\n영향력을 나타냅니다.'),
 (167, 'Max에서 Smooth Max로,\n그 기울기를 모으면 Softmax가 됩니다.'),
 (171, '다음에는 이 관계를 이용한\n안정적인 계산 방법을 살펴보겠습니다.'),
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
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('가장 큰 값 하나를 고르는 함수',30,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('07  /  Smooth Max의 기울기',25,MINT).move_to(UP*4.65),self.head,self.sub)
  self.heading('Max: 가장 큰 값 하나를 고릅니다')
  example=txt('max(2, 5) = 5',44,GOLD).move_to(UP*.8)
  note=txt('출력은 숫자 하나',29,MUTED).move_to(DOWN*1)
  self.play(FadeIn(example),FadeIn(note),run_time=.5)
  self.cue(1);self.play(Indicate(example),run_time=.6)
  self.cue(2)
  self.play(Transform(example,txt('max(4, 5) = 5',44,GOLD).move_to(example)),Transform(note,txt('작은 입력을 올려도 출력은 그대로',28,BLUE).move_to(note)),run_time=.7)
  self.cue(3)
  self.play(Transform(example,txt('max(6, 5) = 6',44,GOLD).move_to(example)),Transform(note,txt('최댓값이 바뀌면, 따라가는 입력도 바뀝니다',27,PINK).move_to(note)),run_time=.7)
  self.cue(4);self.play(FadeOut(example),FadeOut(note),run_time=.3);self.heading('max(t, 0) = ReLU(t)')
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
  self.heading('비슷하지만, 정확히 같지는 않습니다')
  inputs=txt('입력 [2, 5]',37,BLUE).move_to(UP*2.25)
  maximum=txt('Max = 5',39,GOLD).move_to(UP*.8)
  approximation=txt('Log-Sum-Exp ≈ 5.04859',34,MINT).move_to(DOWN*.5)
  diff=txt('차이 ≈ 0.04859',28,MUTED).move_to(DOWN*1.8)
  scalar=txt('두 함수 모두 숫자 하나를 출력합니다',27,MUTED).move_to(DOWN*3.4)
  self.play(FadeIn(inputs),FadeIn(maximum),FadeIn(approximation),FadeIn(diff),FadeIn(scalar),run_time=.5)
  self.cue(11)
  self.play(Transform(inputs,txt('입력 [0, 10]',37,BLUE).move_to(inputs)),Transform(maximum,txt('Max = 10',39,GOLD).move_to(maximum)),Transform(approximation,txt('Log-Sum-Exp ≈ 10.00005',34,MINT).move_to(approximation)),Transform(diff,txt('차이 ≈ 0.00005',28,MUTED).move_to(diff)),run_time=.8)
  self.cue(12)
  self.play(Transform(inputs,txt('입력 [2, 2]',37,BLUE).move_to(inputs)),Transform(maximum,txt('Max = 2',39,GOLD).move_to(maximum)),Transform(approximation,txt('Log-Sum-Exp ≈ 2.69315',34,MINT).move_to(approximation)),Transform(diff,txt('차이 = log 2 ≈ 0.69315',28,MUTED).move_to(diff)),run_time=.8)
  self.cue(13);self.heading('Log-Sum-Exp는 Smooth Max의 한 예')
  self.cue(14);self.play(Indicate(scalar),run_time=.6)
  self.cue(15)
  self.play(*[FadeOut(m) for m in [inputs,maximum,approximation,diff,scalar]],run_time=.3);self.heading('각 입력의 영향력 = 출력의 변화율')
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
  summary=VGroup(txt('Log-Sum-Exp',39,MINT),txt('출력: 부드럽게 근사한 최댓값 하나',27,MUTED),txt('↓  각 입력 방향으로 미분',28,GOLD),txt('Softmax',43,BLUE),txt('출력: 각 입력의 영향력을 모은 벡터',27,BLUE)).arrange(DOWN,buff=.4).move_to(UP*.2)
  self.play(FadeIn(summary),run_time=.5)
  self.cue(29);self.play(Indicate(summary[3]),run_time=.7)
  self.cue(30);self.play(FadeOut(summary),run_time=.3);self.heading('NEXT  /  안정적으로 계산하는 방법')
  end=VGroup(txt('Log-Sum-Exp ↔ Softmax',35,MINT),txt('수학적 구조에서 실제 계산으로',29,GOLD)).arrange(DOWN,buff=.7).move_to(UP*.3)
  self.play(FadeIn(end),run_time=.5);self.until(DURATION)
