"""Softmax 06 — two logits, one sigmoid; synchronized graph animation. 124s."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=124
CAPTIONS=[
(0,'앞에서 소프트맥스는 여러 개의 점수를\n하나의 분포로 바꾸는 함수라고 했습니다.'),
(5.5,'그런데 입력이 두 개뿐이라면\n조금 익숙한 형태가 나타납니다.'),
(10,'두 입력을 x₁, x₂라고 해보겠습니다.'),
(13.5,'첫 번째 출력은 다음과 같습니다.'),
(17,'여기서 분자와 분모를\ne의 x₁제곱으로 나눠보겠습니다.'),
(22,'그러면 분자는 1이 되고,\n분모에는 1 더하기 e의 x₂ 빼기 x₁제곱이 남습니다.'),
(28,'지수 부분의 부호를 바꾸어 쓰면\n이렇게 표현할 수 있습니다.'),
(32.5,'어디서 본 식과 닮았습니다.\n바로 시그모이드입니다.'),
(37,'시그모이드의 입력 자리에\n두 점수의 차이를 넣으면 같은 식이 됩니다.'),
(42,'즉 입력이 두 개뿐인 소프트맥스에서 첫 번째 출력은,\n두 입력의 차이에 시그모이드를 적용한 것과 같습니다.'),
(49,'두 번째 출력은 반대 방향의 차이,\nx₂ 빼기 x₁에 시그모이드를 적용한 값입니다.'),
(55,'그리고 두 값의 합은 항상 1입니다.'),
(58,'이 관계를 그래프로 살펴보겠습니다.'),
(61,'가로축은 두 점수의 차이,\n세로축은 소프트맥스의 출력 비중입니다.'),
(66,'중요한 것은 두 입력의 절대적인 크기가 아니라,\n두 값의 차이라는 점입니다.'),
(72,'두 입력에 같은 수를 더해도 차이는 그대로이고,\n그래프 위의 위치와 출력도 바뀌지 않습니다.'),
(79,'두 입력이 같다면 차이는 0입니다.\n시그모이드의 출력은 0.5이므로,\n소프트맥스도 [0.5, 0.5]가 됩니다.'),
(87,'첫 번째 값이 두 번째보다 커질수록 차이는 양수가 되고,\n첫 번째 출력은 1에 가까워집니다.'),
(95,'반대로 첫 번째 값이 더 작아지면,\n차이는 음수가 되고 첫 번째 출력은 0에 가까워집니다.'),
(103,'즉 두 클래스만 있는 경우, 첫 번째 클래스의 확률은\n두 점수의 차이에 시그모이드를 적용해 구할 수 있습니다.'),
(110,'두 함수는 이 경우, 같은 확률 분포를\n서로 다른 형태로 표현하고 있는 것입니다.'),
(116,'다음에는 소프트맥스가 또 다른 익숙한 함수의 미분으로\n나타나는 관계를 살펴보겠습니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def exp(power,color=INK):
 base=txt('e',39,color);sup=txt(power,22,color).next_to(base,UR,buff=.02).shift(DOWN*.1)
 return VGroup(base,sup)
def inline(*a):return VGroup(*a).arrange(RIGHT,buff=.2)
def frac(a,b):
 line=Line(LEFT,RIGHT,color=INK).set_width(max(a.width,b.width)+.3)
 return VGroup(a.next_to(line,UP,buff=.15),line,b.next_to(line,DOWN,buff=.15))
def form(kind):
 if kind==0:f=frac(exp('x₁',BLUE),inline(exp('x₁',BLUE),txt('+',31),exp('x₂',PINK)))
 else:f=frac(txt('1',38),inline(txt('1 +',33),exp({1:'x₂ − x₁',2:'−(x₁ − x₂)',3:'−z'}[kind],GOLD)))
 return inline(txt('σ(z) =' if kind==3 else 'p₁ =',34,BLUE),f).move_to(UP*.65)
def sigmoid(z):return 1/(1+np.exp(-z))
class SoftmaxSigmoid(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('두 입력으로 만든 하나의 분포',30,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('06  /  두 입력의 Softmax와 Sigmoid',24,MINT).move_to(UP*4.65),self.head,self.sub)
  intro=VGroup(txt('[x₁, x₂]',45,GOLD),txt('↓  Softmax',29,MUTED),txt('[p₁, p₂]',45,BLUE)).arrange(DOWN,buff=.55).move_to(UP*.3)
  self.play(FadeIn(intro),run_time=.5)
  self.cue(1);self.heading('입력이 두 개라면?')
  self.cue(2);self.play(Indicate(intro[0]),run_time=.6)
  self.cue(3);self.play(FadeOut(intro),run_time=.3)
  eq=form(0);self.play(FadeIn(eq),run_time=.5)
  self.cue(4)
  divide=inline(txt('분자와 분모를',27),exp('x₁',GOLD),txt('로 나누기',27)).move_to(DOWN*1.8)
  self.play(FadeIn(divide),run_time=.4)
  self.cue(5);self.play(Transform(eq,form(1)),run_time=.65)
  self.cue(6);self.play(Transform(eq,form(2)),FadeOut(divide),run_time=.65)
  identity=txt('x₂ − x₁ = −(x₁ − x₂)',31,GOLD).move_to(DOWN*1.8)
  self.play(FadeIn(identity),run_time=.4)
  self.cue(7);self.heading('익숙한 S자 곡선, Sigmoid')
  self.play(Transform(eq,form(3)),FadeOut(identity),run_time=.5)
  self.cue(8)
  substitution=txt('z = x₁ − x₂',36,GOLD).move_to(DOWN*1.6)
  self.play(FadeIn(substitution),run_time=.4)
  self.cue(9)
  self.play(FadeOut(eq),FadeOut(substitution),run_time=.3)
  first=txt('p₁ = σ(x₁ − x₂)',42,BLUE).move_to(UP*1.3)
  self.play(FadeIn(first),run_time=.5)
  self.cue(10)
  second=txt('p₂ = σ(x₂ − x₁)',40,PINK).move_to(DOWN*.3)
  self.play(FadeIn(second),run_time=.5)
  self.cue(11)
  total=txt('p₁ + p₂ = 1',35,MINT).move_to(DOWN*2)
  self.play(FadeIn(total),run_time=.4)
  self.cue(12);self.play(FadeOut(first),FadeOut(second),FadeOut(total),run_time=.3)
  self.heading('점수 차이와 출력이 함께 움직입니다')
  z=ValueTracker(1);offset=ValueTracker(2)
  ax=Axes(x_range=[-5,5,1],y_range=[0,1,.5],x_length=6.8,y_length=3.3,
      axis_config={'color':MUTED,'stroke_width':1.3,'include_ticks':False,'tip_width':.12,'tip_height':.12}).move_to(UP*.1)
  curves=VGroup(ax.plot(sigmoid,x_range=[-5,5,.04],color=BLUE,stroke_width=4),ax.plot(lambda v:1-sigmoid(v),x_range=[-5,5,.04],color=PINK,stroke_width=3))
  labels=VGroup(*[txt(str(v).replace('-','−'),20,MUTED).next_to(ax.c2p(v,0),DOWN,buff=.12) for v in [-4,-2,0,2,4]],*[txt(str(v),20,MUTED).next_to(ax.c2p(-5,v),LEFT,buff=.12) for v in [0,.5,1]])
  xlabel=txt('점수 차이  z = x₁ − x₂',24,GOLD).move_to(DOWN*2.5)
  legend=VGroup(txt('p₁ = σ(z)',23,BLUE),txt('p₂ = 1 − σ(z)',23,PINK)).arrange(RIGHT,buff=.5).move_to(UP*2.55)
  def readout(label,fn,x,color):
   l=txt(label,24,color).move_to([x-.65,3.05,0]);n=DecimalNumber(fn(),mob_class=Text,num_decimal_places=1,font_size=25,color=color).move_to([x+.35,3.05,0]);n.add_updater(lambda m:m.set_value(fn()));return VGroup(l,n)
  reads=VGroup(readout('x₁ =',lambda:offset.get_value()+z.get_value(),-2.25,BLUE),readout('x₂ =',lambda:offset.get_value(),1.35,PINK))
  dots=always_redraw(lambda:VGroup(Dot(ax.c2p(z.get_value(),sigmoid(z.get_value())),radius=.09,color=BLUE),Dot(ax.c2p(z.get_value(),1-sigmoid(z.get_value())),radius=.075,color=PINK)))
  guide=always_redraw(lambda:DashedLine(ax.c2p(z.get_value(),0),ax.c2p(z.get_value(),1),color=GOLD,stroke_width=1.5,dash_length=.09))
  def strip():
   p=sigmoid(z.get_value());return VGroup(Rectangle(width=6.6*p,height=.42,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to([-3.3+3.3*p,-3.25,0]),Rectangle(width=6.6*(1-p),height=.42,stroke_width=0,fill_color=PINK,fill_opacity=.9).move_to([3.3*p,-3.25,0]))
  band=always_redraw(strip)
  probability=VGroup()
  for x,label,fn,color in [(-1.8,'p₁ =',lambda:sigmoid(z.get_value()),BLUE),(1.8,'p₂ =',lambda:1-sigmoid(z.get_value()),PINK)]:
   l=txt(label,24,color).move_to([x-.5,-4,0]);n=DecimalNumber(fn(),mob_class=Text,num_decimal_places=3,font_size=26,color=color).move_to([x+.5,-4,0]);n.add_updater(lambda m,f=fn:m.set_value(f()));probability.add(l,n)
  self.play(FadeIn(ax),FadeIn(labels),Create(curves),FadeIn(xlabel),FadeIn(legend),FadeIn(reads),run_time=.8)
  self.add(guide,dots,band,probability)
  self.cue(13);self.play(Indicate(xlabel),run_time=.6)
  self.cue(14);self.heading('절대 크기보다, 두 값의 차이')
  self.cue(15)
  self.play(offset.animate.set_value(102),run_time=2.5,rate_func=smooth)
  self.cue(16);self.heading('x₁ = x₂  →  z = 0')
  self.play(offset.animate.set_value(2),z.animate.set_value(0),run_time=1.5)
  self.play(Indicate(dots),run_time=.6)
  self.cue(17);self.heading('x₁ > x₂  →  p₁은 1에 가까워집니다')
  self.play(z.animate.set_value(4),run_time=4.5,rate_func=smooth)
  self.cue(18);self.heading('x₁ < x₂  →  p₁은 0에 가까워집니다')
  self.play(z.animate.set_value(-4),run_time=4.5,rate_func=smooth)
  self.cue(19);self.heading('두 클래스의 확률을 표현하는 두 방식')
  self.play(z.animate.set_value(0),run_time=1.2)
  self.cue(20)
  graph=VGroup(ax,labels,curves,xlabel,legend,reads,guide,dots,band,probability)
  for mob in graph.get_family():mob.clear_updaters()
  self.play(FadeOut(graph),run_time=.4)
  final=VGroup(txt('Softmax([x₁, x₂])',36,MINT),txt('=',35,MUTED),txt('[σ(x₁ − x₂), 1 − σ(x₁ − x₂)]',31,BLUE)).arrange(DOWN,buff=.5).move_to(UP*.4)
  self.play(FadeIn(final),run_time=.5)
  self.cue(21);self.heading('NEXT  /  다른 함수의 미분으로 만나는 Softmax')
  self.play(FadeOut(final),run_time=.3)
  end=VGroup(txt('어떤 함수의 미분일까요?',34,GOLD),txt('미분  →  Softmax',36,MINT)).arrange(DOWN,buff=.8).move_to(UP*.3)
  self.play(FadeIn(end),run_time=.5);self.until(DURATION)
