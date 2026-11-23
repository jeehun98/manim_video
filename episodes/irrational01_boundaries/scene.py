"""174-second portrait short: proof, open irrationality questions, approximation."""
import sys,json,math
from pathlib import Path
from fractions import Fraction
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.genfunc01_dice.scene import GFScene,txt,eq,INK,MUTED
BLUE,GREEN,RED,GOLD='#67B7FF','#67E3C1','#FF6B75','#FFD166'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
PHI=(1+math.sqrt(5))/2
PAIRS=[(1,1),(2,1),(3,2),(5,3),(8,5),(13,8)]
def card(tex,color=BLUE,width=3,height=1.2,size=49):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.15,stroke_color=color,fill_color=color,fill_opacity=.09),eq(tex,size=size,color=color,width=width-.25))
def coprime(y=4.7):return eq(r'\gcd(a,b)=1',y,34,BLUE)
def golden_rect():
 h=3.9;w=PHI*h;left=-w/2;bottom=-.6
 frame=Rectangle(width=w,height=h,color=GOLD).move_to([0,bottom+h/2,0])
 square=Square(side_length=h,color=GOLD,fill_color=GOLD,fill_opacity=.1).move_to([left+h/2,bottom+h/2,0])
 remainder=Rectangle(width=w-h,height=h,color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([left+h+(w-h)/2,bottom+h/2,0])
 return frame,square,remainder
class IrrationalScene(GFScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.header)
  self.header=VGroup(txt('MATHEMATICS  /  IRRATIONAL NUMBERS',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
class Shot01(IrrationalScene):
 shot=0
 def s01(self):
  examples=VGroup(*[eq(s,size=65,color=BLUE) for s in [r'\frac12',r'\frac34',r'-\frac73']]).arrange(RIGHT,buff=1.1).move_to([0,3.4,0]);self.show(examples,run_time=.6)
  general=eq(r'\frac ab\qquad(a,b\in\mathbb Z,\ b\ne0)',1.1,55);self.play(TransformFromCopy(examples,general),run_time=.8)
  self.show(txt('이 형태로 나타낼 수 없는 실수',-.8,33),txt('무리수',-2.4,57,GREEN));self.to(6)
  self.clear();self.show(eq(r'\sqrt2',1.5,135,GREEN),run_time=.6);self.to(8)
class Shot02(IrrationalScene):
 shot=1
 def s02(self):
  f=eq(r'\sqrt2=\frac ab',2.8,90,BLUE);self.show(f,txt('분수라고 가정',4.7,29,MUTED));self.to(13)
  reduction=VGroup(card(r'\frac68',BLUE,2.3),eq(r'\longrightarrow',size=44),card(r'\frac34',GREEN,2.3)).arrange(RIGHT,buff=.35).move_to([0,-.1,0]);self.show(reduction,run_time=.7);self.to(17)
  self.show(coprime(-2.4),txt('공통인수는 미리 약분할 수 있다',-3.7,30));self.to(22)
class Shot03(IrrationalScene):
 shot=2
 def s03(self):
  self.show(coprime(),eq(r'\sqrt2=\frac ab',3,65,BLUE))
  f=eq('a^2=2b^2',1.1,76);self.show(f);self.to(26)
  odd=card(r'(2k+1)^2=2(2k^2+2k)+1',MUTED,6.9,1.15,40).move_to([0,-.7,0]);self.show(odd,txt('홀수의 제곱은 홀수',-1.8,29,MUTED))
  self.show(txt('a²이 짝수 → a도 짝수',-2.8,35,GREEN));self.to(30)
  self.play(FadeOut(odd),run_time=.3);self.show(eq('a=2c',-.7,78,GREEN));self.to(33)
class Shot04(IrrationalScene):
 shot=3
 def s04(self):
  condition=coprime();self.show(condition,eq('a=2c',3.4,57,GREEN))
  f=eq('4c^2=2b^2',1.7,74);self.show(f);self.to(37)
  self.play(Transform(f,eq('b^2=2c^2',1.7,74)),run_time=.7);self.to(40)
  b_even=eq('b=2d',-.1,67,GREEN);self.show(b_even);self.to(42)
  boxes=VGroup(card('a=2c',GREEN),card('b=2d',GREEN)).arrange(RIGHT,buff=.5).move_to([0,-1.7,0]);self.show(boxes)
  contradiction=eq(r'\gcd(a,b)\geq2',-3.4,58,RED);self.show(contradiction);self.to(46)
  self.play(FadeOut(b_even),Indicate(condition,color=RED),Indicate(contradiction,color=RED),run_time=.9);self.show(txt('서로소라는 가정과 모순!',.4,36,RED));self.to(49)
  self.clear();self.show(eq(r'\sqrt2\notin\mathbb Q',1.5,101,GREEN),txt('정수의 비로 나타낼 수 없다',-.7,36));self.to(53)
class Shot05(IrrationalScene):
 shot=4
 def s05(self):
  row=VGroup(*[card(s,GREEN,2.1,1.6,69) for s in [r'\sqrt2',r'\pi','e']]).arrange(RIGHT,buff=.35).move_to([0,2.8,0]);self.show(row,txt('모두 무리수',.8,39,GREEN));self.to(57)
  self.show(txt('√2는 대수적 수',-.8,31,MUTED),txt('π와 e는 초월수',-2.1,40,GOLD),txt('유리수 계수의 0이 아닌 다항식의 근이 아닌 수',-3.6,25,MUTED));self.to(62)
class Shot06(IrrationalScene):
 shot=5
 def s06(self):
  self.show(eq(r'e=\sum_{n=0}^{\infty}\frac1{n!}',3.4,77,GREEN))
  series=eq(r'1+\frac1{1!}+\frac1{2!}+\frac1{3!}+\cdots',1.1,56);self.show(series)
  number=DecimalNumber(2,num_decimal_places=6,font_size=67,color=BLUE).move_to([0,-1.1,0]);self.show(number,txt('부분합',-2.2,28,MUTED));self.to(68)
  for n in range(2,7):
   total=sum(1/math.factorial(k) for k in range(n+1));self.play(ChangeDecimalToValue(number,total),run_time=.65)
  self.to(73);self.show(txt('이 급수에서 출발하는 무리성 증명',-3.6,29,GREEN));self.to(76)
class Shot07(IrrationalScene):
 shot=6
 def s07(self):
  pause=txt('그런데…',1.5,55,GOLD);self.show(pause);self.to(78)
  self.play(FadeOut(pause),run_time=.3)
  row=VGroup(card(r'\pi',GREEN,2.5,1.6,86),eq('+',size=62),card('e',GREEN,2.5,1.6,86)).arrange(RIGHT,buff=.35).move_to([0,2.8,0]);self.show(row,txt('무리수',1.3,30,GREEN,x=-1.85),txt('무리수',1.3,30,GREEN,x=1.85));self.to(82)
  self.show(eq(r'\pi+e\quad\text{irrational?}',-.5,62,GOLD),txt('아직 모른다',-2,46,GOLD));self.to(85)
  self.show(eq(r'\pi^e\quad\text{irrational?}',-3.6,51,GOLD));self.to(88)
class Shot08(IrrationalScene):
 shot=7
 def s08(self):
  self.show(eq(r'\gamma=\lim_{n\to\infty}\left(\sum_{k=1}^n\frac1k-\ln n\right)',3.3,48),eq(r'0.5772156649\ldots',1.1,61,GOLD))
  choices=VGroup(card(r'\mathbb Q',BLUE,2.7),eq('?',size=62,color=GOLD),card(r'\mathbb R\setminus\mathbb Q',GREEN,2.7,1.2,44)).arrange(RIGHT,buff=.25).move_to([0,-1.2,0]);self.show(choices,txt('유리수인지 무리수인지도 미해결',-3.3,33,GOLD));self.to(95)
class Shot09(IrrationalScene):
 shot=8
 def s09(self):
  f=eq(r'\zeta(3)=\sum_{n=1}^{\infty}\frac1{n^3}',3.5,72);self.show(f)
  terms=VGroup(*[eq(t,size=53) for t in ['1',r'\frac1{2^3}',r'\frac1{3^3}',r'\frac1{4^3}',r'\cdots']]).arrange(RIGHT,buff=.5).move_to([0,1,0]);self.play(LaggedStart(*[FadeIn(t) for t in terms],lag_ratio=.15),run_time=1.3);self.to(101)
  self.show(eq(r'\zeta(3)\notin\mathbb Q',-1.3,78,GREEN),txt('무리수임이 증명됨',-3,38,GREEN));self.to(106)
class Shot10(IrrationalScene):
 shot=9
 def s10(self):
  cards=VGroup(*[card(r'\zeta('+str(n)+')',GREEN if n==3 else GOLD,1.35,1,36) for n in [3,5,7,9,11]]).arrange(RIGHT,buff=.16).move_to([0,3.4,0]);self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.15),run_time=1.4)
  self.show(eq(r'\zeta(13),\;\zeta(15),\;\zeta(17),\;\ldots',1.7,44,GOLD));self.to(110)
  self.show(txt('무리수인 값이 무한히 많다',-.4,39,GREEN),txt('특정 항목마다 체크한 것은 아니다',-2,30,MUTED));self.to(114)
  self.show(txt('무한히 존재한다는 증명',-3.3,32,GREEN));self.to(119)
  self.show(txt('어느 항이 무리수인가?',.6,34,GOLD));self.to(122)
class Shot11(IrrationalScene):
 shot=10
 def s11(self):
  f=eq(r'\varphi=1+\frac1{\varphi}',4.6,65,GOLD);self.show(f);self.to(125)
  frame,square,rest=golden_rect();self.show(frame,eq(r'\varphi',3.8,41,GOLD),eq('1',1.35,36,GOLD,x=-3.6),run_time=.6)
  self.show(square,rest,eq(r'1\times1',1.3,46,GOLD,x=-1.2),txt('남은 직사각형',1.8,24,BLUE,x=2,width=2.1),eq(r'1\times\frac1{\varphi}',.8,35,BLUE,x=2,width=2.2));self.to(131)
  moving=rest.copy();self.add(moving)
  self.play(Rotate(moving,angle=PI/2),run_time=1)
  self.play(moving.animate.scale(PHI).move_to(frame.get_center()),run_time=1.2)
  self.play(Circumscribe(frame,color=GREEN),run_time=.8)
  self.show(eq(r'\frac{1}{\varphi-1}=\varphi',-2.2,56,GOLD),txt('회전하고 확대하면 같은 비율',-3.6,31));self.to(138)
class Shot12(IrrationalScene):
 shot=11
 def s12(self):
  self.show(eq(r'\varphi^2=\varphi+1',4.4,66,GOLD))
  solution=eq(r'\varphi=\frac{1+\sqrt5}{2}',2.5,79,GOLD);self.show(solution);self.to(143)
  fib=VGroup(*[card(str(n),BLUE,.78,.8,33) for n in [1,1,2,3,5,8,13]]).arrange(RIGHT,buff=.22).move_to([0,.3,0]);self.show(fib);self.to(145)
  ratio=eq(r'\frac11',-1.6,85,GREEN);self.show(ratio,run_time=.4)
  for a,b in PAIRS[1:]:self.play(Transform(ratio,eq(r'\frac{'+str(a)+'}{'+str(b)+'}',-1.6,85,GREEN)),run_time=.6)
  self.show(txt('연속된 피보나치 수의 비',-3.5,31,MUTED));self.to(152)
class Shot13(IrrationalScene):
 shot=12
 def s13(self):
  self.show(eq(r'\varphi\approx1.6180339\ldots',4.5,60,GOLD),run_time=.4)
  line=NumberLine(x_range=[1.48,1.70,.02],length=7,include_numbers=False,color=MUTED).move_to([0,1.3,0]);self.show(line,run_time=.4)
  target=DashedLine(line.n2p(PHI)+DOWN*.4,line.n2p(PHI)+UP*1.4,color=GOLD);self.show(target,run_time=.3)
  labels=[]
  for a,b,y in [(3,2,2.6),(5,3,2.6),(8,5,.2),(13,8,3.2)]:
   point=line.n2p(a/b);dot=Dot(point,color=BLUE,radius=.08);label=eq(r'\frac{'+str(a)+'}{'+str(b)+'}',y,34,BLUE,x=point[0],width=.7)
   self.play(FadeIn(dot),FadeIn(label),run_time=.3);labels.extend([dot,label])
  self.show(txt('분모의 크기에 비해 얼마나 가까운가',-1.1,31,GOLD),eq(r'q^2\left|\varphi-\frac pq\right|',-2.5,61),txt('연분수·Hurwitz 정리의 기준',-3.45,22,MUTED),txt('임의로 가까운 근사도 가능하다',-4.2,27,GREEN),run_time=.4);self.to(159)
class Shot14(IrrationalScene):
 shot=13
 def s14(self):
  self.show(txt('정의',4.6,27,MUTED),txt('정수의 비로 나타낼 수 없는 실수',3.5,36,GREEN),txt('그 정의 너머의 질문들',1.9,32));self.to(163)
  row=VGroup(card(r'\sqrt2',GREEN,2.15,1.4,67),card(r'\pi+e',GOLD,2.15,1.4,54),card(r'\varphi',GOLD,2.15,1.4,70)).arrange(RIGHT,buff=.28).move_to([0,0,0]);self.show(row,txt('증명',-1.2,29,GREEN,x=-2.4),txt('미해결',-1.2,29,GOLD),txt('근사',-1.2,29,GOLD,x=2.4));self.to(169)
  self.show(txt('무리수들 사이에서도\n유리수 근사의 성질은 다르다',-3.4,36));self.to(174)
