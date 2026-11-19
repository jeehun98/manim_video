"""157-second portrait: one Euclid calculation, correctness, termination and complexity."""
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
ALGO=json.loads((HERE/'algorithm_data.json').read_text(encoding='utf-8'))
BLUE,PURPLE,GREEN,GOLD,RED,INK,MUTED='#42B8E8','#A18CF3','#65D6AC','#E8B45D','#EF7185','#E8EDF5','#8B9CB7'
RULE=r'\gcd(a,b)=\gcd(b,a\bmod b)'
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=44,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def pair(a,b,x=0,y=2.5,color=BLUE):
 return VGroup(RoundedRectangle(width=3.25,height=1.1,corner_radius=.18,color=color,fill_color=color,fill_opacity=.06),eq(fr'({a},{b})',size=43,color=color,width=3)).move_to([x,y,0])
def remainder_rectangle(a,b,q,r):
 width=min(6.6,3.4*a/b);unit=width/a;height=unit*b;left=-width/2;y=1.35
 tiles=VGroup()
 for i in range(q):
  square=Square(side_length=unit*b,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([left+(i+.5)*unit*b,y,0])
  tiles.add(square,eq(fr'{b}\times{b}',y,34,BLUE,width=unit*b-.12,x=square.get_x()))
 if r:
  rem=Rectangle(width=unit*r,height=height,stroke_color=GOLD,fill_color=GOLD,fill_opacity=.18).move_to([left+(q*b+r/2)*unit,y,0]);tiles.add(rem,eq(str(r),y,40,GOLD,width=unit*r-.1,x=rem.get_x()))
 border=Rectangle(width=width,height=height,stroke_color=INK,stroke_width=1.4).move_to([0,y,0])
 tiles.add(border,eq(str(a),y+height/2+.42,32,x=0),eq(str(b),y,30,x=left-.42,width=.65),eq(fr'{a}={b}\times{q}+{r}',-1.25,46,GOLD),txt(f'남는 폭 {r}' if r else '남는 영역 없음 · 나머지 0',-2.6,31,GOLD))
 return tiles
class EuclidScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel];self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*5.05)
  self.header=VGroup(txt('EUCLIDEAN ALGORITHM  /  48, 18',7.65,16,MUTED))
  active=0 if self.shot<2 else 1 if self.shot<4 else 2
  for i,(x,name,color) in enumerate([(-2.5,'반복',BLUE),(0,'정당성',PURPLE),(2.5,'종료 · 복잡도',GREEN)]):
   box=RoundedRectangle(width=2.3,height=.7,corner_radius=.13,stroke_color=color,stroke_opacity=1 if i==active or self.shot==7 else .35,fill_color=color,fill_opacity=.08 if i==active else .02).move_to([x,6.85,0]);text=txt(name,6.85,25,color,x=x,width=2.1).set_opacity(1 if i==active or self.shot==7 else .6);self.header.add(box,text)
  self.header.add(eq(r'\gcd(48,18)',5.95,33,BLUE,x=-1.65,width=4))
  self.answer=eq(r'=6' if self.shot>=2 else r'=\ ?',5.95,38,GREEN,x=2.15,width=2)
  self.header.add(self.answer);self.header.set_z_index(25);self.add(self.header)
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.header]
  obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def chain(self,start_y=3.7,spacing=1.6):
  rows=[]
  for i,(a,b) in enumerate([(48,18),(18,12),(12,6),(6,0)]):
   y=start_y-i*spacing;rows.append(VGroup(eq(fr'\gcd({a},{b})',y,40,PURPLE,x=-.8,width=4.3),eq(r'=6',y,42,GREEN,x=2.15,width=1.7)))
  return rows
class Shot01(EuclidScene):
 shot=0
 def s01(self):
  self.show(eq('48',3.2,75,BLUE,x=-1.9),eq('18',3.2,75,GOLD,x=1.9),txt('최대공약수는?',1.5,39));self.to(3)
  self.show(txt('48의 약수',.5,27,BLUE,x=-1.95),txt('18의 약수',.5,27,GOLD,x=1.95),eq(r'1,2,3,4,6',-.5,30,BLUE,x=-1.95,width=3.6),eq(r'8,12,16,24,48',-1.35,30,BLUE,x=-1.95,width=3.6),eq(r'1,2,3',-.5,31,GOLD,x=1.95,width=3.6),eq(r'6,9,18',-1.35,31,GOLD,x=1.95,width=3.6),txt('공약수: 1, 2, 3, 6',-2.65,32,GREEN));self.to(9)
  self.clear_body();self.show(pair(48,18,y=2.7),txt('약수를 나열하지 않고도 찾는다',.7,37));self.to(13)
  self.show(txt('유클리드 알고리즘',-1.1,42,BLUE),eq(r'(a,b)\mapsto(b,a\bmod b)',-3,41,BLUE));self.to(15)
class Shot02(EuclidScene):
 shot=1
 def s02(self):
  g=remainder_rectangle(48,18,2,12);self.show(g);self.to(19)
  self.play(ReplacementTransform(g,g2:=remainder_rectangle(18,12,1,6)),run_time=.6);self.show(txt('남은 직사각형을 돌려서 같은 계산',-4,25,MUTED));self.to(23)
  self.clear_body();self.show(remainder_rectangle(12,6,2,0));self.to(26)
  self.clear_body();self.play(Transform(self.answer,eq(r'=6',5.95,38,GREEN,x=2.15,width=2)),run_time=.4)
  self.show(eq(r'48=18\times2+12',3.4,43,BLUE),eq(r'18=12\times1+6',1.95,43,BLUE),eq(r'12=6\times2+0',.5,43,BLUE),eq(r'\gcd(48,18)=6',-1.5,57,GREEN),txt('마지막 0이 아닌 나머지',-3.1,32));self.to(30)
class Shot03(EuclidScene):
 shot=2
 def s03(self):
  self.show(pair(48,18,x=-1.95,y=3),pair(18,12,x=1.95,y=3,color=PURPLE),eq(r'\longrightarrow',1.6,52,PURPLE),txt('왜 같은 답을 줄까?',-.2,39));self.to(33)
  self.show(eq(r'\gcd(48,18)=\gcd(18,12)',-1.8,43,PURPLE),txt('숫자는 바뀌어도 최대공약수는 유지',-3.4,31,GREEN));self.to(38)
  self.clear_body();base=eq(r'48=18\times2+12',3.6,48,GOLD);self.show(base,eq(r'12=48-18\times2',1.9,48,GOLD));self.to(41)
  forward=VGroup(eq(r'48=6\times8,\quad18=6\times3',.2,39,PURPLE),eq(r'12=6\times(8-2\times3)',-1.3,41,PURPLE));self.show(forward);self.to(44)
  general=VGroup(eq(r'd\mid48,\ d\mid18',.2,43,PURPLE),eq(r'\Longrightarrow\ d\mid(48-2\times18)=12',-1.3,39,PURPLE));self.play(ReplacementTransform(forward,general),run_time=.6);self.to(46)
  self.play(FadeOut(general));self.show(eq(r'd\mid18,\ d\mid12',.2,43,PURPLE),eq(r'\Longrightarrow\ d\mid(2\times18+12)=48',-1.3,39,PURPLE),txt('반대 방향도 성립',-3.2,30,GREEN));self.to(50)
  self.clear_body()
  for x,title,color in [(-1.95,'48과 18의 공약수',BLUE),(1.95,'18과 12의 공약수',PURPLE)]:
   box=RoundedRectangle(width=3.4,height=2.4,corner_radius=.18,color=color).move_to([x,2,0]);self.show(box,txt(title,2.8,25,color,x=x,width=3.2),eq(r'\{1,2,3,6\}',1.5,38,color,x=x,width=3.1),run_time=.5)
  self.show(eq(r'\gcd(48,18)=\gcd(18,12)',-.3,44,PURPLE),txt('공약수 집합이 정확히 같다',-2,36,GREEN));self.to(56)
  self.show(txt('최댓값인 최대공약수도 같다',-3.7,31));self.to(59)
class Shot04(EuclidScene):
 shot=3
 def s04(self):
  self.show(eq(r'\gcd(48,18)=\gcd(18,12)',2.5,44,PURPLE),txt('같은 규칙을 다시 적용한다면?',.2,38));self.to(62)
  self.clear_body();rows=self.chain()
  for i,row in enumerate(rows):
   self.show(row,run_time=.5)
   if i<3:self.show(eq(r'\downarrow',2.9-i*1.6,30,PURPLE),run_time=.2)
  self.show(txt('불변성 · Invariant',-3.7,28,MUTED));self.to(68)
  self.clear_body();self.show(txt('수학적 귀납법',3.6,41,PURPLE),eq(r'(a_0,b_0)\to(a_1,b_1)\to\cdots\to(a_k,b_k)',1.65,35,PURPLE),eq(r'\gcd(a_k,b_k)=\gcd(a_0,b_0)=G',-.3,40,GREEN),txt('P(k): k번 변환해도 원래 최대공약수를 유지',-2.7,29));self.to(73)
  self.clear_body();self.show(txt('기초 단계 · 처음에 성립',3.6,33,PURPLE),eq(r'P(0)',2.3,57,PURPLE),txt('귀납 단계 · 한 단계에서 다음 단계로',.6,31,PURPLE),eq(r'P(k)\Longrightarrow P(k+1)',-.9,49,PURPLE),txt('한 번의 나머지 변환이 최대공약수를 보존',-3,29,GREEN));self.to(79)
  self.clear_body();self.show(eq(r'(48,18)\to(18,12)',3.2,44,PURPLE),eq(r'\to(12,6)\to(6,0)',1.5,44,PURPLE),eq(r'\gcd=6',-.4,56,GREEN),txt('반복해도 변하지 않는 정답',-2.5,37));self.to(83)
class Shot05(EuclidScene):
 shot=4
 def s05(self):
  self.show(eq(r'18\to12\to6\to0',2.9,57,BLUE),txt('끝없이 반복할 수도 있을까?',.5,39));self.to(88)
  self.clear_body();self.show(eq(r'a=bq+r,\quad b>0',3.2,45),eq(r'0\leq r<b',1.4,64,GREEN),txt('나머지는 비음 정수이며 나누는 수보다 작다',-1.1,29));self.to(92)
  self.clear_body();self.add(Line([-3.6,-.3,0],[3.6,-.3,0],color=MUTED))
  for x,n in [(-2.7,18),(-.9,12),(.9,6),(2.7,0)]:
   h=n/18*3.1;shape=Rectangle(width=.95,height=max(.02,h),fill_color=BLUE,fill_opacity=.7,stroke_width=0).move_to([x,-.3+h/2,0]);self.show(shape,eq(str(n),-1,39,x=x,width=1.2),run_time=.4)
  self.show(txt('비음 정수가 계속 엄격하게 줄어들 수는 없다',-2.5,30),txt('0에 도달하면 종료',-4,34,GREEN));self.to(97)
  self.clear_body();self.show(txt('정답 보존',2.6,44,PURPLE),txt('+',1.1,46),txt('반드시 종료',-.4,44,GREEN),txt('올바른 답을 내고 끝나는 알고리즘',-2.6,34));self.to(101)
class Shot06(EuclidScene):
 shot=5
 def s06(self):
  self.show(txt('그렇다면 얼마나 빠를까?',2,44,GREEN));self.to(104)
  self.show(txt('계산 복잡도',-.1,46,GREEN),txt('Computational Complexity',-1.3,29,MUTED));self.to(107)
  self.clear_body();self.show(pair(48,18,x=-1.95,y=3.25),pair(987,610,x=1.95,y=3.25,color=GREEN),txt('나눗셈 3회',1.3,35,BLUE,x=-1.95),txt('나눗셈 14회',1.3,35,GREEN,x=1.95),txt('숫자의 값과 반복 횟수는 다른 척도',-.8,33),txt('마지막 나머지 0을 만드는 나눗셈도 포함',-2.8,25,MUTED));self.to(113)
  self.clear_body();ax=Axes(x_range=[0,1000,250],y_range=[0,24,6],x_length=6.5,y_length=3.2,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(UP*1.2);curve=ax.plot(lambda n:2*np.log2(n+1),x_range=[0,1000,3],color=GREEN)
  self.show(ax,curve,txt('나머지 연산 횟수',3.65,27,GREEN),txt('입력 숫자의 값 →',-1.1,26,MUTED),txt('로그 증가를 설명하는 개념 곡선',-2.5,29),txt('개별 입력의 실제 측정 그래프는 아님',-4,23,MUTED));self.to(118)
  self.clear_body();self.show(eq(r'O(\log\min(a,b))',2.5,64,GREEN),txt('작은 입력 값에 대해 로그 수준의 반복',.4,34),txt('양의 정수 입력 · 나머지 연산 횟수의 상한',-1.5,27,MUTED),txt('한 번의 큰 정수 나눗셈 비용과는 구별',-3.3,27,MUTED));self.to(123)
class Shot07(EuclidScene):
 shot=6
 def s07(self):
  self.show(txt('연속한 피보나치 수 · 많은 반복이 필요한 예시',4,27,GREEN))
  for i,row in enumerate(ALGO['fib_examples']):
   y=3-i*.86;n=row['divisions'];bar=Rectangle(width=n*.22,height=.45,stroke_width=0,fill_color=GREEN,fill_opacity=.65).move_to([-.8+n*.11,y,0]);self.show(eq(fr"({row['a']},{row['b']})",y,29,x=-2.6,width=2.5),bar,txt(f'{n}회',y,26,GREEN,x=3,width=1.2),run_time=.4)
  self.show(txt('마지막 나머지 0까지 센 실제 나눗셈 횟수',-2.7,26,MUTED),txt('입력 값의 배수만큼 반복 횟수가 늘지는 않는다',-4,25));self.to(130)
  self.clear_body();self.show(eq(r'n=\min(a,b)',3.2,47),eq(r'O(\log n)',1.5,69,GREEN),txt('큰 입력에서도 효율적인 반복',-.8,37),txt('입력의 표기 길이 L ≈ log₂n에 대해서는 O(L)회',-2.5,25,MUTED),txt('실제 실행 시간은 개별 나눗셈 비용에도 좌우된다',-4,24,MUTED));self.to(137)
class Shot08(EuclidScene):
 shot=7
 def s08(self):
  p=eq(r'(48,18)',2.7,64,BLUE);self.show(p)
  for pair_text in [r'(18,12)',r'(12,6)',r'(6,0)']:self.play(Transform(p,eq(pair_text,2.7,64,BLUE)),run_time=.4)
  self.show(eq(r'\gcd=6',.5,52,GREEN));self.to(141)
  self.clear_body();questions=[]
  for title,detail,y,c in [('반복','어떤 규칙으로 계산하는가?',3.1,BLUE),('정당성 · 귀납법','왜 반복해도 정답이 유지되는가?',.7,PURPLE),('계산 복잡도','입력이 커지면 얼마나 계산해야 하는가?',-1.7,GREEN)]:
   questions.append(VGroup(txt(title,y,38,c),txt(detail,y-.8,29)))
  self.show(questions[0]);self.to(143);self.show(questions[1]);self.to(146);self.show(questions[2]);self.to(149)
  self.clear_body();heading=txt('알고리즘을 이해한다는 것',3.5,43);words=txt('계산 규칙 + 정당성 + 효율성',1.9,34,GREEN);core=eq(RULE,-.2,49,PURPLE);note=txt('방법을 넘어, 왜 옳고 얼마나 효율적인가',-2.5,31)
  self.show(heading,words,core,note);self.to(155)
  self.play(FadeOut(heading),FadeOut(words),FadeOut(note),FadeOut(self.header),FadeOut(self.title),run_time=.6);self.to(157)
