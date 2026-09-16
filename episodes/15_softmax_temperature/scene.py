"""Softmax 04: temperature and probability concentration. 108 seconds."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=108
CAPTIONS=[
(0,'앞에서 소프트맥스는 입력값 사이의 차이를\n지수적인 비율 차이로 바꾼다고 했습니다.'),
(5.5,'그렇다면 이 차이 자체를\n조절하면 어떻게 될까요?'),
(9,'소프트맥스에서는 입력값을\nTemperature라고 부르는 양수 T로 나누기도 합니다.'),
(15,'T가 1일 때는 원래 소프트맥스와 같습니다.'),
(18.5,'하지만 T가 1보다 작아지면\n입력값 사이의 차이는 더 커집니다.'),
(23,'예를 들어 [1, 2, 3]을\n0.5로 나누면 [2, 4, 6]이 됩니다.'),
(28,'값 사이의 간격이 두 배로 벌어졌습니다.'),
(31,'이 차이는 소프트맥스 안에서 지수적으로 반영되어,\n가장 큰 값의 비중이 더 커지고\n분포는 더 뾰족해집니다.'),
(38,'반대로 T가 커지면\n값 사이의 차이는 줄어듭니다.'),
(42,'[1, 2, 3]을 2로 나누면\n[0.5, 1, 1.5]가 됩니다.'),
(47,'각 값의 차이가 작아지면서 출력도 서로 비슷해지고,\n분포는 더 평평해집니다.'),
(53,'즉 Temperature는 새로운 정보를 추가하기보다,\n기존 점수들 사이의 차이를\n확대하거나 축소하는 역할을 합니다.'),
(60,'이 성질은 생성 모델에서도 사용됩니다.'),
(63,'모델이 다음 토큰 후보마다 여러 점수를 만들면,'),
(67,'Temperature를 낮췄을 때는\n높은 점수를 받은 토큰에 더 많은 확률이 몰립니다.'),
(73,'그래서 높은 점수의 토큰을\n더 일관되게 고르는 경향이 생깁니다.'),
(78,'반대로 Temperature를 높이면\n분포가 평평해져, 낮은 점수의 후보도\n선택될 여지가 커집니다.'),
(85,'결과적으로 출력의 다양성도 커질 수 있습니다.'),
(89,'즉 Temperature를 조절한다는 것은\n확률을 임의로 바꾸는 것이 아니라,'),
(94,'소프트맥스에 들어가는\n점수 사이의 차이를 조절하는 것입니다.'),
(99,'다음에는 소프트맥스의 한 입력값이 커질 때\n왜 다른 출력 비중들은 함께 작아지는지\n살펴보겠습니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def probs(t):
 z=np.array([1.,2.,3.])/t;w=np.exp(z-z.max());return w/w.sum()
def exp(power):
 b=txt('e',40);e=txt(power,23).next_to(b,UR,buff=.02).shift(DOWN*.1);return VGroup(b,e)
def frac(a,b):
 l=Line(LEFT,RIGHT,color=INK).set_width(max(a.width,b.width)+.3)
 return VGroup(a.next_to(l,UP,buff=.14),l,b.next_to(l,DOWN,buff=.14))
def chart(t,tokens=False):
 g=VGroup();p=probs(t)
 baseline=-1.5
 for i,(v,c,x) in enumerate(zip(p,[BLUE,GOLD,PINK],[-2.4,0,2.4])):
  h=3.1*v
  g.add(Rectangle(width=1.15,height=h,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([x,baseline+h/2,0]))
  g.add(txt(f'{v*100:.1f}%',25,c).move_to([x,baseline+h+.35,0]))
  g.add(txt(['토큰 A','토큰 B','토큰 C'][i] if tokens else ['항목 1','항목 2','항목 3'][i],25,c).move_to([x,baseline-.45,0]))
 g.add(Line([-3.3,baseline,0],[3.3,baseline,0],color=MUTED,stroke_width=1))
 return g
class SoftmaxTemperature(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('차이를 조절하면 분포가 바뀝니다',30,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('04  /  Temperature로 분포 조절하기',24,MINT).move_to(UP*4.65),self.head,self.sub)
  intro=VGroup(txt('입력의 차이',37,BLUE),txt('↓',30,MUTED),txt('지수적인 출력 비율',35,GOLD)).arrange(DOWN,buff=.5).move_to(UP*.3)
  self.play(FadeIn(intro),run_time=.5)
  self.cue(1);self.heading('그 차이를 키우거나 줄인다면?')
  self.cue(2);self.play(FadeOut(intro),run_time=.3)
  formula=VGroup(txt('pᵢ(T) =',32),frac(exp('xᵢ / T'),VGroup(txt('Σⱼ',32),exp('xⱼ / T')).arrange(RIGHT,buff=.15))).arrange(RIGHT,buff=.3).move_to(UP*.9)
  condition=txt('Temperature  T > 0',29,GOLD).move_to(DOWN*1.2)
  self.play(FadeIn(formula),FadeIn(condition),run_time=.5)
  self.cue(3);self.play(FadeOut(formula),FadeOut(condition),run_time=.3)
  self.heading('T = 1  /  원래 분포')
  calc=txt('[1, 2, 3] ÷ 1 = [1, 2, 3]',32,BLUE).move_to(UP*2.5)
  bars=chart(1);note=txt('막대: 출력 확률 · 같은 높이 척도',22,MUTED).move_to(DOWN*3)
  self.play(FadeIn(calc),FadeIn(bars),FadeIn(note),run_time=.5)
  self.cue(4);self.heading('0 < T < 1  /  간격 확대')
  self.cue(5)
  self.play(Transform(calc,txt('[1, 2, 3] ÷ 0.5 = [2, 4, 6]',31,BLUE).move_to(calc)),run_time=.4)
  gap=txt('인접한 간격: 1 → 2',28,GOLD).move_to(DOWN*4)
  self.play(FadeIn(gap),run_time=.3)
  self.cue(6);self.play(Indicate(gap),run_time=.6)
  self.cue(7);self.heading('T = 0.5  /  더 뾰족한 분포')
  self.play(Transform(bars,chart(.5)),run_time=.8)
  self.cue(8);self.heading('T > 1  /  간격 축소')
  self.cue(9)
  self.play(Transform(calc,txt('[1, 2, 3] ÷ 2 = [0.5, 1, 1.5]',30,BLUE).move_to(calc)),Transform(gap,txt('인접한 간격: 1 → 0.5',28,GOLD).move_to(gap)),run_time=.5)
  self.cue(10);self.heading('T = 2  /  더 평평한 분포')
  self.play(Transform(bars,chart(2)),run_time=.8)
  self.cue(11)
  self.play(*[FadeOut(m) for m in [calc,bars,note,gap]],run_time=.3);self.heading('새 정보 대신, 점수 간격을 조절')
  summary=VGroup(txt('T ↓   간격 ↑   더 뾰족하게',32,PINK),txt('T ↑   간격 ↓   더 평평하게',32,BLUE),txt('입력의 순위는 그대로',27,MUTED)).arrange(DOWN,buff=.75).move_to(UP*.4)
  self.play(FadeIn(summary),run_time=.5)
  self.cue(12);self.heading('생성 모델: 다음 토큰 고르기')
  self.play(FadeOut(summary),run_time=.3)
  tokennote=txt('설명용 후보 3개 · 점수 [1, 2, 3]',24,MUTED).move_to(UP*2.5)
  temp=txt('T = 1',32,GOLD).move_to(DOWN*3)
  bars=chart(1,True)
  self.play(FadeIn(tokennote),FadeIn(temp),FadeIn(bars),run_time=.5)
  self.cue(13);self.play(Indicate(tokennote),run_time=.6)
  self.cue(14)
  self.play(Transform(temp,txt('T = 0.5',32,GOLD).move_to(temp)),Transform(bars,chart(.5,True)),run_time=.8)
  self.cue(15)
  sampling=txt('확률에 따라 선택 · 무작위성은 남을 수 있음',22,MUTED).move_to(DOWN*4)
  self.play(FadeIn(sampling),run_time=.4)
  self.cue(16)
  self.play(Transform(temp,txt('T = 2',32,GOLD).move_to(temp)),Transform(bars,chart(2,True)),run_time=.8)
  self.cue(17)
  self.play(Transform(sampling,txt('점수의 순위는 유지 · 확률은 더 고르게',21,MUTED).move_to(sampling)),run_time=.4)
  self.cue(18)
  self.play(*[FadeOut(m) for m in [tokennote,temp,bars,sampling]],run_time=.3);self.heading('Temperature는 점수 간격의 조절 장치')
  flow=VGroup(txt('입력 점수',34,BLUE),txt('↓  T로 나누기',29,GOLD),txt('조절된 점수 간격',34,GOLD),txt('↓  Softmax',29,MUTED),txt('더 뾰족하거나 평평한 분포',31,MINT)).arrange(DOWN,buff=.3).move_to(UP*.2)
  self.play(FadeIn(flow),run_time=.5)
  self.cue(19);self.play(Indicate(flow[2]),run_time=.6)
  self.cue(20);self.play(FadeOut(flow),run_time=.3);self.heading('NEXT  /  출력들은 왜 함께 움직일까요?')
  end=VGroup(txt('한 입력 점수 ↑',38,PINK),txt('↓',30,MUTED),txt('다른 출력 비중 ↓',38,BLUE)).arrange(DOWN,buff=.5).move_to(UP*.3)
  self.play(FadeIn(end),run_time=.5);self.until(DURATION)
