"""Softmax 05 — the Jacobian maps every input to every output. 119 s."""
import os
import numpy as np
from manim import *
config.pixel_width=int(os.getenv('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.getenv('VIDEO_HEIGHT','1920'))
config.frame_width,config.frame_height=9,16
config.frame_rate=30
config.background_color='#091119'
INK,MUTED,MINT,BLUE,GOLD,PINK='#EDF3F7','#94A7B7','#61E4CF','#68D9F0','#F3CF75','#FF8C9D'
DURATION=119
CAPTIONS=[
(0,'앞에서 소프트맥스는 여러 점수를 하나의 분포로 바꾸고,\n그 전체 합은 항상 1이 된다고 했습니다.'),
(6,'그렇다면 한 입력값만 조금 커지면\n무슨 일이 일어날까요?'),
(10,'예를 들어 소프트맥스 출력이\n[0.2, 0.3, 0.5]라고 해보겠습니다.'),
(15,'세 번째 입력값이 커져서\n세 번째 출력 비중이 증가해도,\n전체 합은 여전히 1이어야 합니다.'),
(21.5,'이때 나머지 입력들은 그대로여도,\n공통 분모가 커지므로 다른 출력 비중은 함께 줄어듭니다.'),
(28,'즉 소프트맥스의 각 출력은\n서로 독립적으로 움직이지 않습니다.'),
(32.5,'하나의 입력 변화가\n여러 출력에 동시에 영향을 줍니다.'),
(37,'이 관계는 미분에서도 그대로 나타납니다.'),
(40,'출력 pᵢ를 입력 xⱼ로 미분하면\n다음과 같이 쓸 수 있습니다.'),
(45,'여기서 델타는 i와 j가 같으면 1,\n다르면 0입니다.'),
(49,'자신의 입력을 변화시키는 경우에는\npᵢ와 1 빼기 pᵢ를 곱한 값이 됩니다.'),
(54,'입력이 커지면 자신의 출력도 커지는 방향입니다.'),
(57.5,'반대로 다른 입력이 변하는 경우에는\n마이너스 pᵢ 곱하기 pⱼ가 됩니다.'),
(62.5,'값이 음수라는 것은, 다른 입력이 커질수록\n내 출력은 작아진다는 뜻입니다.'),
(68,'즉 소프트맥스 안에서는 각 값들이 서로 경쟁합니다.\n한쪽의 비중이 커지면 다른 쪽은 줄어듭니다.'),
(74.5,'그래서 소프트맥스의 미분은\n하나의 숫자가 아니라 행렬로 표현됩니다.'),
(79.5,'각 열은 어떤 입력을 바꾸는지,\n각 행은 어떤 출력이 반응하는지를 나타냅니다.'),
(85,'한 칸에는 그 입력이 변할 때,\n그 출력이 얼마나 변하는지가 들어갑니다.'),
(90,'이처럼 모든 입력과 출력의 변화 관계를 담은 행렬,\n이것을 자코비안이라고 합니다.'),
(96,'예를 들어 세 번째 열만 보면,\n세 번째 입력 하나가 모든 출력에 주는 영향을\n한눈에 읽을 수 있습니다.'),
(103,'ReLU나 Sigmoid처럼 각 원소를 독립적으로\n바꾸는 함수와 달리, 소프트맥스는\n전체 값들의 관계를 함께 고려합니다.'),
(111,'다음에는 입력이 두 개뿐일 때\n이 소프트맥스가 익숙한 다른 함수와\n어떻게 연결되는지 살펴보겠습니다.'),
]
def txt(s,size=29,color=INK):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if m.width>7.5:m.scale_to_fit_width(7.5)
 return m
def frac(a,b):
 l=Line(LEFT,RIGHT,color=INK).set_width(max(a.width,b.width)+.25)
 return VGroup(a.next_to(l,UP,buff=.12),l,b.next_to(l,DOWN,buff=.12))
def derivative(i='i',j='j'):
 ids={'i':'ᵢ','j':'ⱼ'}
 return frac(txt('∂p'+ids[i],36),txt('∂x'+ids[j],36))
def equation(kind):
 rhs={'all':'pᵢ (δᵢⱼ − pⱼ)','self':'pᵢ (1 − pᵢ)','other':'−pᵢ pⱼ'}[kind]
 return VGroup(derivative('i','i' if kind=='self' else 'j'),txt('=',34),txt(rhs,38,MINT if kind=='self' else PINK if kind=='other' else GOLD)).arrange(RIGHT,buff=.25).move_to(UP*.7)
def bars(values):
 g=VGroup()
 for x,p,c,label in zip([-2.4,0,2.4],values,[BLUE,GOLD,PINK],['p₁','p₂','p₃']):
  h=4*p
  g.add(Rectangle(width=1.2,height=h,stroke_width=0,fill_color=c,fill_opacity=.9).move_to([x,-1.4+h/2,0]))
  g.add(txt(f'{p:.2f}',31,c).move_to([x,-1.4+h+.35,0]))
  g.add(txt(label,28,c).move_to([x,-1.9,0]))
 g.add(Line([-3.3,-1.4,0],[3.3,-1.4,0],color=MUTED,stroke_width=1))
 return g

def matrix(symbolic=True,diagonal=False):
 g=VGroup();cells=VGroup()
 values=np.diag([.2,.3,.5])-np.outer([.2,.3,.5],[.2,.3,.5])
 for i,y in enumerate([1.15,0,-1.15]):
  for j,x in enumerate([-1.9,0,1.9]):
   s=(f'∂p{["₁","₂","₃"][i]}/∂x{["₁","₂","₃"][j]}' if symbolic else f'{values[i,j]:.2f}')
   if diagonal and i!=j:s='0'
   cells.add(txt(s,24 if symbolic else 31,MINT if i==j else MUTED if diagonal else PINK).move_to([x,y,0]))
 g.add(cells)
 for x in [-3.05,3.05]:
  inward=.2 if x<0 else -.2
  g.add(VMobject(color=INK,stroke_width=2).set_points_as_corners([[x+inward,1.7,0],[x,1.7,0],[x,-1.7,0],[x+inward,-1.7,0]]))
 return g,cells

class SoftmaxJacobian(Scene):
 def until(self,t):
  if self.time>t+.05:raise ValueError(f'Timing overrun {self.time}>{t}')
  if t>self.time:self.wait(t-self.time)
 def cue(self,i):
  self.until(CAPTIONS[i][0]);new=txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
  self.play(FadeOut(self.sub),FadeIn(new),run_time=.2);self.sub=new
 def heading(self,s):self.play(Transform(self.head,txt(s,30,MINT).move_to(UP*3.65)),run_time=.3)
 def construct(self):
  self.sub=txt(CAPTIONS[0][1]).move_to(DOWN*5.85);self.head=txt('전체 합은 항상 1',31,MINT).move_to(UP*3.65)
  self.add(txt('ACTIVATION FUNCTION SERIES',19,MUTED).move_to(UP*6.85),txt('Softmax',66).move_to(UP*5.65),txt('05  /  서로 연결된 출력과 자코비안',24,MINT).move_to(UP*4.65),self.head,self.sub)
  b=bars([.2,.3,.5]);total=txt('0.2 + 0.3 + 0.5 = 1',32,MINT).move_to(DOWN*3)
  self.play(FadeIn(b),FadeIn(total),run_time=.5)
  self.cue(1);self.heading('세 번째 입력만 커진다면?')
  self.cue(2);self.play(Indicate(b),run_time=.6)
  self.cue(3)
  change=txt('x₃ ↑   ·   x₁, x₂는 고정',29,GOLD).move_to(UP*2.4)
  self.play(FadeIn(change),Transform(b,bars([.16,.24,.6])),Transform(total,txt('0.16 + 0.24 + 0.60 = 1',32,MINT).move_to(total)),run_time=.9)
  self.cue(4)
  reason=txt('같은 분모 ↑  →  p₁, p₂ ↓',28,BLUE).move_to(DOWN*4)
  self.play(FadeIn(reason),run_time=.4)
  self.cue(5);self.heading('각 출력은 독립적이지 않습니다')
  self.cue(6)
  self.play(*[FadeOut(m) for m in [b,total,change,reason]],run_time=.3)
  source=txt('입력 x₃ ↑',36,GOLD).move_to(UP*2)
  targets=VGroup(*[txt(s,33,c).move_to([x,-1,0]) for s,c,x in zip(['p₁ ↓','p₂ ↓','p₃ ↑'],[BLUE,BLUE,PINK],[-2.5,0,2.5])])
  arrows=VGroup(*[Arrow([0,1.45,0],[x,-.4,0],buff=.1,color=MUTED,stroke_width=2) for x in [-2.5,0,2.5]])
  self.play(FadeIn(source),FadeIn(targets),Create(arrows),run_time=.5)
  self.cue(7);self.heading('변화의 관계를 미분으로 쓰면')
  self.cue(8)
  self.play(FadeOut(source),FadeOut(targets),FadeOut(arrows),run_time=.3)
  eq=equation('all');self.play(FadeIn(eq),run_time=.4)
  tag=txt('기본 Softmax · T = 1',22,MUTED).move_to(DOWN*3.8);self.play(FadeIn(tag),run_time=.3)
  self.cue(9)
  delta=txt('δᵢⱼ = 1  (i = j)\nδᵢⱼ = 0  (i ≠ j)',28,GOLD).move_to(DOWN*1.6)
  self.play(FadeIn(delta),run_time=.4)
  self.cue(10);self.heading('자기 입력에 대한 반응  /  i = j')
  self.play(Transform(eq,equation('self')),FadeOut(delta),run_time=.5)
  sign=txt('양수  →  자신의 출력 ↑',30,MINT).move_to(DOWN*1.6)
  self.cue(11);self.play(FadeIn(sign),run_time=.4)
  self.cue(12);self.heading('다른 입력에 대한 반응  /  i ≠ j')
  self.play(Transform(eq,equation('other')),Transform(sign,txt('음수  →  내 출력 ↓',30,PINK).move_to(sign)),run_time=.5)
  self.cue(13);self.play(Indicate(sign),run_time=.6)
  self.cue(14);self.heading('같은 분포 안에서 비중을 나눕니다')
  self.play(FadeOut(eq),FadeOut(sign),FadeOut(tag),run_time=.3)
  self.play(FadeIn(source),FadeIn(targets),Create(arrows),run_time=.5)
  self.cue(15)
  self.play(FadeOut(source),FadeOut(targets),FadeOut(arrows),run_time=.3);self.heading('입력 × 출력의 모든 관계를 한곳에')
  mat,cells=matrix();self.play(FadeIn(mat),run_time=.5)
  self.cue(16)
  columns=VGroup(*[txt(s,26,GOLD).move_to([x,2.05,0]) for x,s in zip([-1.9,0,1.9],['x₁','x₂','x₃'])])
  rows=VGroup(*[txt(s,25,BLUE).move_to([-3.65,y,0]) for y,s in zip([1.15,0,-1.15],['p₁','p₂','p₃'])])
  orientation=txt('열 = 바꾸는 입력   ·   행 = 반응하는 출력',25,MUTED).move_to(DOWN*2.65)
  self.play(FadeIn(columns),FadeIn(rows),FadeIn(orientation),run_time=.5)
  self.cue(17)
  box=SurroundingRectangle(cells[2],buff=.13,color=GOLD)
  meaning=txt('이 칸: x₃ 변화에 대한 p₁의 변화율',25,GOLD).move_to(DOWN*3.7)
  self.play(Create(box),FadeIn(meaning),run_time=.5)
  self.cue(18);self.heading('Jacobian  /  자코비안')
  self.play(FadeOut(box),Transform(meaning,txt('모든 입력과 출력의 변화 관계를 담은 행렬',27,MINT).move_to(meaning)),run_time=.4)
  self.cue(19)
  numerical,ncells=matrix(False)
  self.play(Transform(mat,numerical),Transform(meaning,txt('p = [0.2, 0.3, 0.5]에서의 자코비안',25,MUTED).move_to(meaning)),run_time=.5)
  colbox=Rectangle(width=1.65,height=3.2,color=GOLD,fill_color=GOLD,fill_opacity=.06).move_to(RIGHT*1.9)
  self.play(Create(colbox),Indicate(columns[2]),run_time=.5)
  self.play(Transform(orientation,txt('x₃ ↑  →  p₁ ↓,  p₂ ↓,  p₃ ↑',28,GOLD).move_to(orientation)),run_time=.4)
  self.cue(20)
  self.play(*[FadeOut(m) for m in [mat,columns,rows,orientation,meaning,colbox]],run_time=.3)
  self.heading('독립적인 원소 변환과 다른 점')
  compare=VGroup(txt('원소별 ReLU · Sigmoid',28,BLUE),txt('다른 입력에 대한 미분 = 0',28,MUTED),txt('Softmax',32,MINT),txt('다른 입력에 대한 미분 = −pᵢpⱼ',28,PINK)).arrange(DOWN,buff=.5).move_to(UP*.2)
  self.play(FadeIn(compare),run_time=.5)
  self.cue(21);self.play(FadeOut(compare),run_time=.3);self.heading('NEXT  /  입력이 두 개라면?')
  end=VGroup(txt('Softmax',43,MINT),txt('입력 두 개',30,MUTED),txt('익숙한 함수와 연결됩니다',32,GOLD)).arrange(DOWN,buff=.55).move_to(UP*.3)
  self.play(FadeIn(end),run_time=.5);self.until(DURATION)
