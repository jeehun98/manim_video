"""Softmax 08 — entropy summarizes concentration. 166 seconds."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=166
CAPTIONS=[
(0,'앞에서 소프트맥스는 여러 점수를\n하나의 분포로 바꾼다고 했습니다.'),
(5,'그런데 같은 소프트맥스라도\n분포의 모양은 크게 달라질 수 있습니다.'),
(10,'[0.98, 0.01, 0.01]처럼\n한 값에 거의 모든 비중이 몰릴 수도 있고,'),
(16,'[0.34, 0.33, 0.33]처럼\n거의 고르게 퍼질 수도 있습니다.'),
(22,'두 경우 모두 합은 1이지만,\n선택 결과를 예측하기 쉬운 정도는 다릅니다.'),
(28,'첫 번째는 한 선택지에 강하게 몰려 있고,\n두 번째는 세 선택지의 확률이 거의 같습니다.'),
(34,'이 차이를 숫자 하나로 표현하는 것이\n엔트로피입니다.'),
(39,'확률분포의 엔트로피는\n각 확률에 그 확률의 로그를 곱한 뒤,\n모두 더하고 부호를 바꾼 값입니다.'),
(47,'이 식의 의미를\n극단적인 경우부터 살펴보겠습니다.'),
(51,'[1, 0, 0]이라면\n어떤 선택지가 나올지 완전히 정해져 있습니다.'),
(57,'이때 엔트로피는 0으로 가장 작습니다.'),
(61,'반대로 세 확률이 모두 3분의 1이면,\n어느 선택지가 나올지 가장 예측하기 어렵습니다.'),
(68,'같은 세 선택지 안에서는\n이때 엔트로피가 가장 큽니다.'),
(73,'즉 낮은 엔트로피는 집중된 분포,\n높은 엔트로피는 더 고르게 퍼진 분포를 뜻합니다.'),
(80,'이제 Temperature와 연결해보겠습니다.\n점수 [1, 2, 3]은 고정하고 온도만 바꿉니다.'),
(87,'Temperature를 낮추면 높은 점수에 확률이 몰리고,\n엔트로피도 낮아집니다.'),
(94,'반대로 Temperature를 높이면 분포가 평평해지고,\n엔트로피는 높아집니다.'),
(101,'Temperature는 분포의 모양을 바꾸고,\n엔트로피는 그 집중 정도를 숫자로 요약합니다.'),
(108,'생성 모델의 다음 토큰 분포도\n같은 관점으로 볼 수 있습니다.'),
(113,'한두 후보에 확률이 강하게 몰려 있다면\n엔트로피가 낮습니다.'),
(119,'여러 후보의 확률이 비슷하다면\n엔트로피가 높습니다.'),
(125,'다만 엔트로피가 낮다고 해서\n모델의 선택이 반드시 옳다는 뜻은 아닙니다.'),
(132,'틀린 후보에 확률이 몰려 있어도\n엔트로피는 낮을 수 있습니다.'),
(138,'엔트로피가 나타내는 것은 정답 여부가 아니라,\n현재 분포가 얼마나 집중되어 있는가입니다.'),
(145,'소프트맥스가 점수들을 분포로 바꾼다면,\n엔트로피는 그 분포의 집중도를\n숫자 하나로 요약합니다.'),
(152,'한쪽으로 몰릴수록 낮아지고,\n고르게 퍼질수록 높아집니다.'),
(158,'다음에는 이 소프트맥스 분포가\nAttention에서 실제로 어떤 역할을 하는지\n살펴보겠습니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def entropy(p):
 p=np.asarray(p);q=p[p>0];return max(0.0,float(-np.sum(q*np.log(q))))
def probs(t):
 z=np.array([1.,2.,3.])/t;w=np.exp(z-z.max());return w/w.sum()
def chart(p,labels=None):
 labels=labels or ['A','B','C'];g=VGroup()
 for x,v,c,label in zip([-2.4,0,2.4],p,[BLUE,GOLD,PINK],labels):
  h=max(.008,2.6*v)
  g.add(Rectangle(width=1.15,height=h,stroke_width=0,fill_color=c,fill_opacity=.9 if v>0 else 0).move_to([x,-.9+h/2,0]))
  g.add(txt(f'{v:.3f}',28,c).move_to([x,-.9+h+.35,0]),txt(label,25,c).move_to([x,-1.4,0]))
 g.add(Line([-3.3,-.9,0],[3.3,-.9,0],color=MUTED,stroke_width=1))
 return g
def hlabel(p):return txt(f'H = {entropy(p):.3f} nats',36,MINT).move_to(DOWN*2.5)
class SoftmaxEntropy(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('같은 합 1, 서로 다른 분포',30,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('08  /  분포의 집중도를 읽는 Entropy',24,MINT).move_to(UP*4.65),self.head,self.sub)
  sharp=np.array([.98,.01,.01]);flat=np.array([.34,.33,.33]);p=sharp.copy()
  b=chart(p);note=txt('확률의 합 = 1',28,MUTED).move_to(DOWN*2.5)
  self.play(FadeIn(b),FadeIn(note),run_time=.5)
  self.cue(1);self.heading('얼마나 한쪽에 몰려 있을까요?')
  self.cue(2);self.play(Indicate(b[0]),run_time=.6)
  self.cue(3);self.play(Transform(b,chart(flat)),run_time=1)
  self.cue(4);self.play(Indicate(note),run_time=.6)
  self.cue(5);self.play(Transform(b,chart(sharp)),run_time=.7);self.wait(.7);self.play(Transform(b,chart(flat)),run_time=.7)
  self.cue(6);self.heading('Entropy  /  엔트로피')
  h=hlabel(flat);self.play(ReplacementTransform(note,h),run_time=.5)
  self.cue(7)
  self.play(FadeOut(b),FadeOut(h),run_time=.3)
  formula=txt('H(p) = −Σᵢ pᵢ log pᵢ',42,GOLD).move_to(UP*.8)
  units=txt('자연로그 사용 · 단위: nat',27,MUTED).move_to(DOWN*.5)
  zero=txt('p = 0인 항은 0으로 계산합니다',25,MUTED).move_to(DOWN*1.7)
  self.play(FadeIn(formula),FadeIn(units),FadeIn(zero),run_time=.5)
  self.cue(8);self.heading('가장 집중된 경우부터')
  self.cue(9)
  self.play(FadeOut(formula),FadeOut(units),FadeOut(zero),run_time=.3)
  b=chart([1,0,0]);h=hlabel([1,0,0]);extreme=txt('이상적인 극한 분포 · 유한 Softmax 입력은 모두 양수',20,MUTED).move_to(DOWN*3.65)
  self.play(FadeIn(b),FadeIn(h),FadeIn(extreme),run_time=.6)
  self.cue(10);self.play(Indicate(h),run_time=.6)
  self.cue(11);self.heading('세 선택지가 모두 같은 확률')
  self.play(Transform(b,chart([1/3]*3)),Transform(h,hlabel([1/3]*3)),Transform(extreme,txt('각 확률 = 1/3 · 표시값은 반올림',23,MUTED).move_to(extreme)),run_time=1)
  self.cue(12)
  self.play(Transform(extreme,txt('세 선택지: 0 ≤ H ≤ log 3 ≈ 1.099',25,GOLD).move_to(extreme)),run_time=.4)
  self.cue(13)
  self.play(Transform(b,chart(sharp)),Transform(h,hlabel(sharp)),run_time=.7);self.wait(.8)
  self.play(Transform(b,chart(flat)),Transform(h,hlabel(flat)),run_time=.7)
  self.cue(14)
  self.play(FadeOut(b),FadeOut(h),FadeOut(extreme),run_time=.3);self.heading('같은 점수에서 Temperature만 변경')
  temp=ValueTracker(1)
  small=always_redraw(lambda:chart(probs(temp.get_value())).scale(.65,about_point=ORIGIN).shift(UP*1.3))
  read=DecimalNumber(1,mob_class=Text,num_decimal_places=2,font_size=27,color=GOLD).move_to([.8,3.05,0]);read.add_updater(lambda m:m.set_value(temp.get_value()))
  tl=txt('T =',27,GOLD).move_to([-.5,3.05,0])
  ax=Axes(x_range=[0,4,1],y_range=[0,1.2,.4],x_length=6.2,y_length=2.35,axis_config={'include_ticks':False,'color':MUTED,'stroke_width':1.2,'tip_width':.1,'tip_height':.1}).move_to(DOWN*1.8)
  curve=ax.plot(lambda t:entropy(probs(t)),x_range=[.15,4,.03],color=MINT,stroke_width=4)
  labs=VGroup(*[txt(str(v),19,MUTED).next_to(ax.c2p(v,0),DOWN,buff=.12) for v in [0,1,2,3,4]],*[txt(str(v),19,MUTED).next_to(ax.c2p(0,v),LEFT,buff=.12) for v in [0,.5,1]])
  cap=txt('가로: T   세로: 엔트로피 H (nats)',22,MUTED).move_to(DOWN*3.6)
  dot=always_redraw(lambda:Dot(ax.c2p(temp.get_value(),entropy(probs(temp.get_value()))),radius=.085,color=GOLD))
  hn=DecimalNumber(entropy(probs(1)),mob_class=Text,num_decimal_places=3,font_size=27,color=MINT).move_to([1,-4.3,0]);hn.add_updater(lambda m:m.set_value(entropy(probs(temp.get_value()))))
  hl=txt('H =',26,MINT).move_to([-.3,-4.3,0])
  self.play(FadeIn(ax),FadeIn(labs),Create(curve),FadeIn(cap),FadeIn(tl),run_time=.7);self.add(small,read,dot,hn,hl)
  self.cue(15);self.play(temp.animate.set_value(.3),run_time=3.5)
  self.cue(16);self.play(temp.animate.set_value(4),run_time=4.5,rate_func=linear)
  self.cue(17);self.play(temp.animate.set_value(1),run_time=2.5)
  self.cue(18)
  graph=VGroup(ax,labs,curve,cap,tl,small,read,dot,hn,hl)
  for mob in graph.get_family():mob.clear_updaters()
  self.play(FadeOut(graph),run_time=.3);self.heading('다음 토큰 후보의 분포')
  b=chart(sharp,['토큰 A','토큰 B','토큰 C']);h=hlabel(sharp)
  tokennote=txt('설명용 후보 3개 · 실제 모델 출력이 아님',23,MUTED).move_to(DOWN*3.7)
  self.play(FadeIn(b),FadeIn(h),FadeIn(tokennote),run_time=.5)
  self.cue(19);self.play(Indicate(h),run_time=.6)
  self.cue(20);self.play(Transform(b,chart(flat,['토큰 A','토큰 B','토큰 C'])),Transform(h,hlabel(flat)),run_time=.8)
  self.cue(21);self.heading('집중도와 정답 여부는 다릅니다')
  self.play(Transform(b,chart(sharp,['토큰 A','토큰 B','토큰 C'])),Transform(h,hlabel(sharp)),run_time=.7)
  self.cue(22)
  self.play(Transform(tokennote,txt('예: 정답이 B여도, A에 98%가 몰릴 수 있습니다',24,PINK).move_to(tokennote)),run_time=.5)
  self.cue(23);self.play(Indicate(h),run_time=.6)
  self.cue(24)
  self.play(FadeOut(b),FadeOut(h),FadeOut(tokennote),run_time=.3);self.heading('분포를 만들고, 집중도를 읽습니다')
  summary=VGroup(txt('점수',35,BLUE),txt('↓  Softmax',28,MUTED),txt('확률 분포',35,GOLD),txt('↓  Entropy',28,MUTED),txt('집중도를 요약한 숫자 하나',31,MINT)).arrange(DOWN,buff=.32).move_to(UP*.2)
  self.play(FadeIn(summary),run_time=.5)
  self.cue(25);self.play(FadeOut(summary),run_time=.3)
  end=VGroup(txt('집중될수록  H ↓',35,BLUE),txt('고르게 퍼질수록  H ↑',35,PINK)).arrange(DOWN,buff=.8).move_to(UP*.4);self.play(FadeIn(end),run_time=.5)
  self.cue(26);self.heading('NEXT  /  Attention에서의 Softmax')
  self.play(FadeOut(end),run_time=.3)
  teaser=VGroup(txt('어떤 정보에 얼마나 주목할까요?',32,GOLD),txt('Softmax → Attention',37,MINT)).arrange(DOWN,buff=.8).move_to(UP*.3)
  self.play(FadeIn(teaser),run_time=.5);self.until(DURATION)
