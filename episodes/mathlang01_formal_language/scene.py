"""164 seconds; natural language -> logical structure -> set-theoretic language."""
import json,sys
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene,label
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE,GOLD,PURPLE,GREEN,RED,INK,MUTED='#42B8E8','#F0B65D','#A18CF3','#64D6B0','#EF7185','#E8EDF5','#8B9CB7'
QUANT=r'\forall n\in\mathbb N,\quad\exists m\in\mathbb N:\ m>n'
SUBSET=r'\forall x\,(x\in A\Rightarrow x\in B)'
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=45,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def logic_formula(y=3.9,size=39):
 m=MathTex(r'\forall',r'n\in\mathbb N,',r'\exists',r'm\in\mathbb N:',r'm>n',font_size=size,color=PURPLE)
 m[0].set_color(BLUE);m[2].set_color(BLUE)
 if m.width>7.4:m.scale_to_fit_width(7.4)
 return m.move_to(UP*y)
def english(s,y):
 m=Text(s,font='Malgun Gothic',font_size=29,color=INK,t2c={'is':GOLD},line_spacing=1)
 if m.width>7.3:m.scale_to_fit_width(7.3)
 return m.move_to(UP*y)
class LanguageScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.6)
  self.add(txt('MATHEMATICS  /  LANGUAGE & LOGIC',7,18,MUTED))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]
  obs=[m for m in self.mobjects if m not in keep and m.get_center()[1]<6.5]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
class Shot01(LanguageScene):
 shot=0
 def s01(self):
  formulas=VGroup(eq(r'e^{i\pi}+1=0',3.4,49),eq(r'\int_a^b f(x)\,dx',1.7,45),eq(r'\forall x\in\mathbb R:\ x^2\geq0',-.1,42),eq(r'A\cong B',-1.8,47))
  self.play(LaggedStart(*[FadeIn(m) for m in formulas],lag_ratio=.3),run_time=2)
  symbols=eq(r'\forall\quad\exists\quad\land\quad\neg\quad=\quad\in',.8,56,BLUE)
  self.play(ReplacementTransform(formulas,symbols),run_time=1.2);self.to(5)
  self.play(ReplacementTransform(symbols,eq(SUBSET,1.3,45,GREEN)),run_time=1)
  self.show(txt('논리학',3.6,36,BLUE,x=-1.8),txt('집합론',3.6,36,PURPLE,x=1.8),txt('기호 + 문법 + 공리',-1,35),txt('현대 수학의 대부분을 형식화',-2.6,29,MUTED));self.to(11)
  self.clear_body();self.show(txt('What does “is” mean?',1.3,43,GOLD));self.to(13)
class Shot02(LanguageScene):
 shot=1
 def s02(self):
  ys=[3.7,1,-1.7];cards=[english('five is ...',y) for y in ys]
  self.show(*cards);self.to(16)
  sentences=['five is the square root\nof twenty-five.','five is less than ten.','five is a prime number.']
  for i,at in enumerate([18,20,22]):
   self.play(Transform(cards[i],english(sentences[i],ys[i])),run_time=.6);self.to(at)
  self.show(txt('같은 단어 · 서로 다른 관계',-3.8,29,GOLD));self.to(26)
  self.show(eq(r'5=\sqrt{25}',2.5,44,GREEN),eq(r'5<10',-.05,44,BLUE));self.to(31)
  self.show(eq(r'5\in P',-2.75,44,PURPLE));self.to(35)
  self.show(txt('P: 소수들의 집합',-4.35,23,PURPLE));self.to(40)
class Shot03(LanguageScene):
 shot=2
 def s03(self):
  self.show(eq(r'5<10',2.8,49,BLUE),eq(r'5\in P',1.1,49,PURPLE));self.to(43)
  self.clear_body();self.show(eq(r'(5<10)\land(5\in P)',1.5,45,GREEN),txt('기호의 의미 + 결합 규칙',-.5,36),txt('P: 소수들의 집합',-2,24,PURPLE));self.to(47)
  self.clear_body();self.show(txt('모든 자연수에 대한 문장은?',1.6,40));self.to(51)
  self.show(txt('논리학 · Logic',-.2,43,BLUE),eq(r'\forall\quad\exists\quad\land\quad\lor\quad\neg',-2,52,BLUE));self.to(53)
class Shot04(LanguageScene):
 shot=3
 def s04(self):
  formula=logic_formula();self.show(formula,txt('문장의 구조와 추론 규칙',2.4,34,BLUE));self.to(56)
  self.clear_body();formula=logic_formula();self.add(formula)
  line=NumberLine(x_range=[0,6,1],length=7,include_numbers=True,font_size=24).move_to(UP*.8)
  n=ValueTracker(0)
  dn=always_redraw(lambda:Dot(line.n2p(n.get_value()),color=BLUE,radius=.09));dm=always_redraw(lambda:Dot(line.n2p(n.get_value()+1),color=GOLD,radius=.09))
  ln=always_redraw(lambda:eq('n',1.4,29,BLUE,x=line.n2p(n.get_value())[0]));lm=always_redraw(lambda:eq('m',.05,29,GOLD,x=line.n2p(n.get_value()+1)[0]))
  self.add(line,dn,dm,ln,lm);self.show(eq(r'm=n+1>n',-1.7,44,GREEN))
  self.play(n.animate.set_value(2),run_time=1.5);self.play(n.animate.set_value(4),run_time=1.5);self.to(61)
  self.clear_body();formula=logic_formula();self.add(formula)
  for text,s,y,c in [('모든 자연수 n',r'\forall n\in\mathbb N',2,BLUE),('자연수 m이 존재',r'\exists m\in\mathbb N',-.1,GOLD),('m은 n보다 크다',r'm>n',-2.2,GREEN)]:
   a=txt(text,y,32,c);b=eq(s,y,43,c);self.show(a,run_time=.3);self.play(ReplacementTransform(a,b),run_time=.6)
  self.to(67);self.clear_body();self.add(logic_formula())
  self.show(eq(r'\forall',1.4,108,BLUE,x=-1.9),eq(r'\exists',1.4,108,GOLD,x=1.9),txt('모든',-.2,36,BLUE,x=-1.9),txt('존재한다',-.2,36,GOLD,x=1.9),txt('범위의 모든 대상',-1.5,24,x=-1.9,width=3.4),txt('조건을 만족하는 대상',-1.5,24,x=1.9,width=3.4));self.to(72)
  self.clear_body();self.add(logic_formula())
  for x,s,t in [(-3,r'\forall','모든'),(-1.5,r'\exists','존재'),(0,r'\land','그리고'),(1.5,r'\lor','또는'),(3,r'\neg','아니다')]:self.show(eq(s,1.1,62,BLUE,x=x),txt(t,-.2,25,x=x,width=1.4),run_time=.3)
  self.show(eq(r'P\land Q\qquad P\lor Q\qquad\neg P',-2,42,GREEN),txt('여기서 P, Q는 명제',-3.5,24,MUTED));self.to(78)
class Shot05(LanguageScene):
 shot=4
 def s05(self):
  self.show(logic_formula(2.7),txt('그런데 자연수란 무엇일까?',.7,39,PURPLE),txt('문장 구조와 대상의 정의는 다른 일',-1.1,29,MUTED));self.to(84)
  self.clear_body();self.show(txt('집합론 · Set Theory',3.8,43,PURPLE));self.to(86)
  container=Circle(radius=1.7,color=PURPLE,fill_opacity=.06).move_to(UP*.2)
  members=eq(r'2,3,7,11,\ldots',.7,31,PURPLE);five=eq('5',-2.7,52,GOLD)
  self.show(container,members,five,eq(r'P',2.4,36,PURPLE));self.play(five.animate.move_to([0,-.5,0]),run_time=1.2);self.show(eq(r'5\in P',-2.6,51,PURPLE),txt('P: 소수들의 집합 · 일부 원소만 표시',-4,23,MUTED));self.to(92)
  self.clear_body();self.show(eq(r'0=\varnothing',3.5,49,PURPLE,x=-1.9,width=3.5),eq(r'1=\{\varnothing\}',3.5,49,PURPLE,x=1.9,width=3.5))
  empty=Circle(radius=1.15,color=PURPLE).move_to([-1.9,.8,0]);outer=Circle(radius=1.15,color=PURPLE).move_to([1.9,.8,0]);inner=VGroup(Circle(radius=.52,color=GOLD),eq(r'\varnothing',size=34,color=GOLD)).move_to([1.9,.8,0])
  self.show(empty,outer,txt('원소 0개',-1,29,PURPLE,x=-1.9),txt('원소 1개',-1,29,PURPLE,x=1.9));self.play(FadeIn(inner,scale=.7),run_time=1);self.show(txt('공집합 ≠ 공집합을 원소로 갖는 집합',-3.1,29,GREEN));self.to(98)
  self.clear_body();self.show(eq(r'0=\varnothing\quad1=\{\varnothing\}',3.9,40,PURPLE))
  for s,y,t in [(r'\mathbb N',2,'자연수'),(r'\mathbb Z,\ \mathbb R',0,'정수 · 실수'),(r'f:A\to B',-2,'함수 · 관계')]:self.show(eq(s,y,49,PURPLE),txt(t,y-.8,27,MUTED),run_time=.6)
  self.to(105);self.clear_body();self.show(txt('논리학',3.7,40,BLUE,x=-1.9),txt('집합론',3.7,40,PURPLE,x=1.9),eq(r'\forall,\exists,\land,\neg',2.2,37,BLUE,width=3.4,x=-1.9),eq(r'\varnothing,\in,\{\ \}',2.2,37,PURPLE,width=3.4,x=1.9),txt('문장 · 추론',.9,27,BLUE,x=-1.9),txt('대상 · 관계',.9,27,PURPLE,x=1.9),logic_formula(-1.3),txt('구조와 대상이 함께 문장을 만든다',-3.4,31,GREEN));self.to(111)
class Shot06(LanguageScene):
 shot=5
 def s06(self):
  self.show(txt('ZFC Set Theory',4,40,PURPLE),txt('Zermelo–Fraenkel Set Theory with Choice',3.1,20,MUTED),eq(r'2+3=5\quad f:A\to B',1.5,37),eq(r'x\leq y\quad A\subseteq B\quad x\in A',.1,38));self.to(114)
  self.clear_body();self.show(txt('기본 비논리 관계 기호',4,32,PURPLE),eq(r'\in',1.6,145,PURPLE),txt('원소 관계 · Membership',-.6,34),txt('논리 기호 · 등호 · 변수 · 괄호도 필요',-2.4,26,MUTED));self.to(116)
  self.clear_body();a=eq(r'A\subseteq B',2.6,59,GOLD);self.show(a,txt('부분집합 기호를 풀어 쓰면',4,29))
  b=MathTex(r'\forall x\,(x',r'\in',r'A\Rightarrow x',r'\in',r'B)',font_size=43,color=BLUE);b[1].set_color(PURPLE);b[3].set_color(PURPLE);b.move_to(UP*.7)
  self.play(TransformMatchingTex(a,b,transform_mismatches=True),run_time=1.5);self.show(txt('같은 관계를 더 기본적인 언어로 표현',-1.3,30,GREEN),txt('∈ + 논리 문법 + 집합론의 공리',-3.2,28,PURPLE));self.to(121)
  self.clear_body();self.show(eq(r'x\in A',3.4,53,PURPLE),eq(SUBSET,1.6,40,BLUE),txt('정의와 정리를 형식화',-.4,38,GREEN),txt('수 · 함수 · 공간 · 대수적 구조',-2,32),txt('기호와 규칙, 공리가 함께 필요',-3.7,27,MUTED));self.to(126)
class Shot07(LanguageScene):
 shot=6
 def s07(self):
  self.show(txt('중요한 구분',2,46,RED));self.to(127)
  self.clear_body();self.show(txt('표현 가능',2.6,43,BLUE),eq(r'\not\Rightarrow',.9,74,RED),txt('증명 가능',-.8,43,GREEN),txt('문장을 쓰는 일 ≠ 공리에서 도출하는 일',-2.7,29));self.to(133)
  self.clear_body();self.show(txt('괴델의 불완전성 정리',4.1,37,RED),txt('충분한 산술 · 일관성 · 효과적 공리화',3,25,MUTED),txt('조건을 만족하는 형식 체계 T',2.1,24,MUTED))
  for x,s,c in [(-2.4,r'T\vdash A',GREEN),(0,r'T\vdash\neg B',BLUE),(2.4,r'G',RED)]:
   card=VGroup(RoundedRectangle(width=2.1,height=1.3,corner_radius=.14,color=c),eq(s,size=31,color=c,width=1.8)).move_to([x,.7,0]);self.show(card,run_time=.4)
  self.show(eq(r'T\nvdash G\qquad T\nvdash\neg G',-1.2,45,RED),txt('T 안에서 증명도 반증도 할 수 없는 문장',-2.7,29),txt('현대적 Gödel–Rosser 형태',-4,21,MUTED));self.to(143)
  self.clear_body();self.show(txt('표현하는 능력',2.3,43,BLUE),eq(r'\ne',.7,72,RED),txt('증명하는 능력',-.9,43,GREEN),txt('결정할 수 없다는 것은 거짓이라는 뜻이 아니다',-3,25,MUTED));self.to(148)
class Shot08(LanguageScene):
 shot=7
 def s08(self):
  self.show(eq(SUBSET,3.2,43,BLUE),eq(r'0=\varnothing,\quad1=\{\varnothing\}',1.3,43,PURPLE),eq(r'5=\sqrt{25}\quad5<10\quad5\in P',-.6,40,GOLD),txt('계산을 편하게 하는 기호를 넘어',-2.7,32));self.to(153)
  self.clear_body()
  for t,detail,y,c in [('정의','대상을 정한다',3.5,PURPLE),('관계','성질을 표현한다',1.3,GOLD),('추론','규칙에 따라 결론을 도출한다',-.9,BLUE)]:self.show(txt(t,y,43,c),txt(detail,y-.8,28),run_time=.5)
  self.show(txt('수학적 형식언어',-3.5,37,GREEN));self.to(159)
  self.clear_body();self.show(eq(r'\forall\quad\exists\quad\in\quad=',2.4,75,BLUE),txt('단순한 규칙, 다양한 표현',.2,40,GREEN),txt('수학의 언어와 문법',-1.7,34),txt('기호 · 논리 규칙 · 공리',-3.4,28,MUTED));self.to(164)
