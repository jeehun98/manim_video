"""User-timed, 176-second generating-function short. Eight replaceable shots."""
import sys,json
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene
from quantum_series.shared.theme import text
shared.FPS=30
config.frame_rate=30
config.background_color='#0F131D'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BLUE,RED,GOLD,GREEN,INK,MUTED='#58C4DD','#FC6255','#FFFF00','#83C167','#F4F5F7','#9CA6B5'
def txt(s,y=0,size=32,color=INK,x=0,width=7.6):return text(s,x,y,size,color,width)
def eq(s,y=0,size=48,color=INK,x=0,width=7.5):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def term(n,c=None,size=48):
 parts=[]
 if c is not None:parts.append(eq(str(c),size=size,color=GREEN))
 parts.append(eq('x',size=size))
 exponent=eq(str(n),size=size*.58,color=GOLD)
 base=VGroup(*parts).arrange(RIGHT,buff=.04)
 exponent.next_to(base,UR,buff=.01).shift(LEFT*.06+DOWN*.1)
 return VGroup(base,exponent)
class DiceFace(VGroup):
 def __init__(self,n,color=BLUE,size=.88):
  super().__init__();self.add(RoundedRectangle(width=size,height=size,corner_radius=.14,fill_color=color,fill_opacity=1,stroke_width=0))
  coords={1:[(0,0)],2:[(-1,1),(1,-1)],3:[(-1,1),(0,0),(1,-1)],4:[(-1,1),(1,1),(-1,-1),(1,-1)],5:[(-1,1),(1,1),(0,0),(-1,-1),(1,-1)],6:[(-1,1),(-1,0),(-1,-1),(1,1),(1,0),(1,-1)]}
  self.add(*[Dot([x*size*.24,y*size*.24,0],radius=size*.065,color='#0F131D') for x,y in coords[n]])
def pair(a,b):return VGroup(DiceFace(a),eq('+',size=30),DiceFace(b,RED)).arrange(RIGHT,buff=.12)
def poly(color=INK):return eq(r'x+x^2+x^3+x^4+x^5+x^6',size=41,color=color)
class GFScene(QCSScene):
 replace=Scene.replace
 data=DATA
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel]
  self.remove(*[m for m in list(self.mobjects) if m not in keep])
  self.title.move_to(UP*5.9)
  self.header=VGroup(txt('MATHEMATICS  /  GENERATING FUNCTIONS',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3))
  self.add(self.header)
 def clear(self):
  keep=[self.title,self.caption,self.caption_panel,self.header]
  objects=[m for m in self.mobjects if m not in keep]
  if objects:self.play(*[FadeOut(m) for m in objects],run_time=.4)
 def title_to(self,s):self.play(Transform(self.title,txt(s,5.9,34)),run_time=.4)
class Shot01(GFScene):
 shot=0
 def s01(self):
  p=pair(2,5).scale(1.6).move_to([0,2.5,0]);q=txt('합 = 7',.2,48,GOLD);question=txt('몇 가지일까요?',-1.4,35)
  self.play(FadeIn(p,scale=.7),Rotate(p,angle=TAU),run_time=1.2);self.show(q,question);self.to(4)
  self.play(FadeOut(p),FadeOut(q),FadeOut(question),run_time=.3)
  pairs=VGroup(*[VGroup(pair(i,7-i),eq(f'{i}+{7-i}=7',size=27,color=MUTED).shift(DOWN*.85)) for i in range(1,7)]).arrange_in_grid(rows=3,cols=2,buff=(1, .65)).move_to([0,1.5,0])
  counter=txt('0가지',-3.2,58,GREEN);self.add(counter)
  for i,o in enumerate(pairs):self.play(FadeIn(o),Transform(counter,txt(f'{i+1}가지',-3.2,58,GREEN)),run_time=.55)
  self.to(9);self.play(pairs.animate.set_opacity(.25),counter.animate.shift(UP*.3),run_time=.5)
  self.show(txt('다항식의 곱셈으로도?',-.2,40),eq(r'(\cdots)\times(\cdots)',-1.4,49,BLUE));self.to(14)
class Shot02(GFScene):
 shot=1
 def s02(self):
  dice=VGroup(*[DiceFace(i,size=1.04) for i in range(1,7)]).arrange_in_grid(rows=2,cols=3,buff=(1.3,1.5)).move_to([0,1.8,0])
  self.play(LaggedStart(*[FadeIn(d,scale=.7) for d in dice],lag_ratio=.15),run_time=1.4);self.to(19)
  terms=VGroup(*[term(i).move_to(dice[i-1].get_center()+DOWN*.95) for i in range(1,7)])
  self.play(*[TransformFromCopy(d,t) for d,t in zip(dice,terms)],run_time=1.2);self.to(22)
  for i in range(6):self.play(Indicate(dice[i],scale_factor=1.12),Indicate(terms[i][1],color=GOLD),run_time=.55)
  p=poly(BLUE).move_to([0,-2.1,0]);self.play(TransformFromCopy(terms,p),run_time=1.2);self.show(txt('지수 = 주사위 눈',-3.5,30,GOLD));self.to(30)
  self.play(FadeOut(dice),FadeOut(terms),p.animate.move_to([0,2,0]),run_time=.6)
  self.show(eq(r'\times',.6,48),poly(RED).move_to([0,-.8,0]));self.to(33)
class Shot03(GFScene):
 shot=2
 def s03(self):
  law=eq(r'x^a\,x^b=x^{a+b}',3.8,57);self.show(law,txt('거듭제곱의 곱셈 → 지수의 덧셈',2.5,29,GOLD));self.to(39)
  example=VGroup(eq('x^2',size=68,color=BLUE),eq(r'\times',size=46),eq('x^5',size=68,color=RED),eq('=',size=46),term(7,size=68)).arrange(RIGHT,buff=.28).move_to([0,.5,0])
  self.play(TransformFromCopy(law,example),run_time=1.1);self.show(eq('2+5=7',-1.1,47,GOLD));self.to(44)
  self.show(pair(2,5).move_to([0,-3,0]));self.to(49);self.clear()
  rows=VGroup(*[VGroup(eq(f'x^{i}',size=53,color=BLUE),eq(r'\times',size=37),eq(f'x^{7-i}',size=53,color=RED),eq('=',size=37),term(7,size=53)).arrange(RIGHT,buff=.25) for i in range(1,7)]).arrange(DOWN,buff=.35).move_to([0,1,0])
  self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.2),run_time=2.5);self.to(55)
  results=VGroup(*[r[-1] for r in rows]);target=term(7,6,size=112).move_to([0,-2.4,0])
  self.play(*[r[:-1].animate.set_opacity(.3) for r in rows],run_time=.5)
  self.play(ReplacementTransform(results.copy(),target),run_time=1.5);self.show(txt('같은 결과를 만드는 항을 모은다',4.4,29));self.to(60)
  self.play(FadeOut(rows),target.animate.move_to([0,1,0]).scale(1.25),run_time=.8)
  self.show(txt('계수 6 = 경우의 수',-1.5,37,GREEN),txt('지수 7 = 두 눈의 합',-2.6,37,GOLD));self.to(66)
class Shot04(GFScene):
 shot=3
 def s04(self):
  cells=VGroup()
  for i in range(1,7):
   for j in range(1,7):
    c=GREEN if i+j==7 else '#293243'
    cell=VGroup(RoundedRectangle(width=.75,height=.64,corner_radius=.06,fill_color=c,fill_opacity=1,stroke_width=0),txt(str(i+j),size=26,color='#0F131D' if i+j==7 else INK,width=.6)).move_to([(j-3.5)*.87,4-(i-1)*.76,0]);cells.add(cell)
  self.show(cells,run_time=.7)
  labels=VGroup(*[txt(str(i),4.65,23,RED,x=(i-3.5)*.87) for i in range(1,7)],*[txt(str(i),4-(i-1)*.76,23,BLUE,x=-3.2) for i in range(1,7)])
  self.show(labels);self.to(70)
  bars=VGroup()
  for k in range(2,13):
   count=6-abs(7-k);x=(k-7)*.64;h=count*.32
   bars.add(VGroup(Rectangle(width=.45,height=h,fill_color=GREEN if k==7 else '#59677C',fill_opacity=1,stroke_width=0).move_to([x,-2.1+h/2,0]),txt(str(k),-2.45,21,GOLD if k==7 else MUTED,x=x,width=.55),txt(str(count),-1.85+h,21,GREEN if k==7 else MUTED,x=x,width=.55)))
  self.play(TransformFromCopy(cells,bars),run_time=1.2);self.to(74)
  self.play(FadeOut(cells),FadeOut(labels),bars.animate.shift(UP*3.3),run_time=.6)
  p=VGroup(eq(r'x^2+2x^3+3x^4+4x^5',size=37),eq(r'+5x^6+6x^7+5x^8',size=37),eq(r'+4x^9+3x^{10}+2x^{11}+x^{12}',size=37)).arrange(DOWN,buff=.28).move_to([0,-1.2,0]);self.show(p)
  self.show(txt('지수 = 결과의 크기',-3.2,30,GOLD),txt('계수 = 그 결과를 만드는 경우의 수',-4.1,28,GREEN));self.to(79)
class Shot05(GFScene):
 shot=4
 def s05(self):
  seq=VGroup(*[eq('a_'+str(i),size=54,color=GREEN) for i in range(4)],eq(r'\cdots',size=42)).arrange(RIGHT,buff=.7).move_to([0,3.2,0])
  self.show(seq,txt('유한한 목록에서 무한한 수열로',1.4,32));self.to(83)
  self.clear();cards=VGroup()
  for n in range(4):
   c=VGroup(RoundedRectangle(width=1.55,height=1.5,corner_radius=.13,fill_color='#263242',fill_opacity=.7,stroke_color=MUTED),txt(f'n = {n}',size=26,color=GOLD).shift(DOWN*.45))
   if n:c.add(VGroup(*[Square(side_length=.23,fill_color=BLUE,fill_opacity=1,stroke_width=0) for _ in range(n)]).arrange(RIGHT,buff=.08).shift(UP*.2))
   else:c.add(eq(r'\varnothing',size=35,color=MUTED).shift(UP*.2))
   cards.add(c)
  cards.arrange(RIGHT,buff=.3).move_to([0,3.5,0]);a=VGroup(*[eq('a_'+str(i),size=48,color=GREEN,x=c.get_x(),y=1.8) for i,c in enumerate(cards)])
  self.show(cards,a,txt('상자는 구조의 크기를 표시',4.8,22,MUTED));self.to(88)
  terms=VGroup(*[VGroup(eq('a_'+str(i),size=43,color=GREEN),term(i,size=43)).arrange(RIGHT,buff=.02).move_to([c.get_x(),-.2,0]) for i,c in enumerate(cards)])
  arrows=VGroup(*[Arrow([c.get_x(),1.25,0],[c.get_x(),.35,0],color=MUTED,buff=.1) for c in cards])
  self.show(arrows);self.play(*[TransformFromCopy(a[i],terms[i][0]) for i in range(4)],run_time=1.1);self.show(*[t[1] for t in terms]);self.to(94)
  plus=VGroup(*[eq('+',-.2,29,x=(terms[i].get_x()+terms[i+1].get_x())/2) for i in range(3)])
  description=txt('상수항부터 무한히 더한 멱급수',-2.7,29)
  self.show(plus,eq(r'+\cdots',-1.5,43),description);self.to(101)
  self.play(*[Indicate(t[1][1],color=GOLD) for t in terms],run_time=1.2);self.show(txt('거듭제곱 = 항의 위치',-3.8,31,GOLD));self.to(106)
  extract=eq(r'[x^3]G(x)=a_3',-2.9,45,color=GREEN);self.play(FadeOut(description),TransformFromCopy(terms[3][0],extract),run_time=1.2);self.to(113)
  self.clear();self.show(eq(r'G(x)=\sum_{n=0}^{\infty}a_nx^n',2,66),txt('생성함수',-.2,58,BLUE),txt('Generating Function',-1.3,27,MUTED),txt('계수는 정보, 지수는 위치',-3,35));self.to(119)
class Shot06(GFScene):
 shot=5
 def s06(self):
  dice=VGroup(*[DiceFace(5,size=.9) for _ in range(10)]).arrange_in_grid(rows=2,cols=5,buff=.42).move_to([0,2.8,0])
  question=txt('어떤 이점이 있을까요?',-.2,38)
  self.show(*dice[:2],question);self.to(122)
  self.play(FadeOut(question),LaggedStart(*[FadeIn(d,scale=.5) for d in dice[2:]],lag_ratio=.1),run_time=2);self.to(126)
  count=eq('36',-.9,65,GREEN);self.show(count,txt('전체 가능한 순서 있는 조합',.1,27,MUTED))
  for n in range(3,11):self.play(Transform(count,eq(f'{6**n:,}',-.9,65,GREEN)),run_time=.3)
  self.to(130)
  self.show(eq(r'6^{10}=60{,}466{,}176',-2,38,GREEN),eq(r'(x+x^2+\cdots+x^6)^{10}',-3.25,47),txt('표현은 간결하게 · 계수 추출에는 계산 필요',-4.3,24,MUTED));self.to(138)
class Shot07(GFScene):
 shot=6
 def s07(self):
  ones=VGroup(*[VGroup(RoundedRectangle(width=.65,height=.85,corner_radius=.1,color=GREEN,fill_color=GREEN,fill_opacity=.08),eq('1',size=37,color=GREEN)) for _ in range(8)],eq(r'\cdots',size=32)).arrange(RIGHT,buff=.18).move_to([0,3.7,0])
  self.show(ones,txt('무한한 항들을 하나의 식으로?',1.4,35));self.to(143)
  self.play(LaggedStart(*[Indicate(o,color=GREEN) for o in ones[:8]],lag_ratio=.12),run_time=1.5);self.to(146)
  series=eq(r'1+x+x^2+x^3+\cdots',1.2,59);self.play(TransformFromCopy(ones,series),run_time=1.2);self.show(txt('각 위치에 거듭제곱을 붙인다',-.2,29,GOLD));self.to(153)
  self.clear()
  def aligned(y,shifted=False):
   entries=[(r'xG=' if shifted else 'G=',-3.25),('x',-1.05),('+',-.4),('x^2',.35),('+',1.05),('x^3',1.8),('+',2.5),(r'\cdots',3.15)]
   if not shifted:entries += [('1',-2.25),('+',-1.7)]
   return VGroup(*[eq(t,y,40,RED if shifted else INK,x=x,width=1.1) for t,x in entries])
  g=aligned(3.2);xg=aligned(1.8,True)
  self.show(g);self.play(TransformFromCopy(g,xg),run_time=.7);self.to(155)
  cross=VGroup(*[Line([x-.2,y+.23,0],[x+.2,y-.23,0],color=RED,stroke_width=4) for y in [3.2,1.8] for x in [-1.05,.35,1.8]])
  self.show(cross,run_time=.4);self.show(eq(r'(1-x)G=1',-.1,53),run_time=.4);self.to(157)
  fraction=eq(r'G(x)=\frac{1}{1-x}',-2,76,color=BLUE);self.play(TransformFromCopy(VGroup(g,xg),fraction),run_time=1.1)
  self.show(txt('형식적 멱급수의 항등식',-3.7,26,MUTED),txt('실수 급수로 해석하면 |x| < 1',-4.4,23,MUTED),run_time=.3);self.to(160)
  self.play(FadeOut(g),FadeOut(xg),FadeOut(cross),fraction.animate.move_to([0,1.5,0]).scale(1.25),run_time=1)
  self.show(txt('무한한 정보 → 유한한 대수적 표현',-.6,32,GREEN));self.to(164)
class Shot08(GFScene):
 shot=7
 def s08(self):
  pairs=VGroup(pair(1,2),pair(2,3),pair(4,5),pair(3,6)).arrange_in_grid(rows=2,cols=2,buff=(1,.5)).move_to([0,3.1,0])
  self.show(pairs,txt('조합적 구조',4.9,30,MUTED));f=eq(r'G(x)=\sum_{n\geq0}a_nx^n',-.4,61)
  self.play(TransformFromCopy(pairs,f),run_time=1.3);self.to(169)
  self.show(eq(r'+\qquad\times',-2.3,70,BLUE),txt('대수적 연산으로 다루기',-3.8,33));self.to(174)
  self.play(FadeOut(pairs),FadeOut(f),run_time=.4);self.show(txt('구조를 세는 문제에서\n수식을 다루는 문제로.',2,42,GREEN),run_time=.6);self.to(176)
