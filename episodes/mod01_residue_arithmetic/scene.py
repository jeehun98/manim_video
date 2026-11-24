"""178-second modular-arithmetic short; exact narration, native portrait at 60fps."""
import sys,json,math
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.padic01_local_global.scene import PadicScene,node,txt,eq,INK,MUTED
import longforms.qcs01_speed.direction as shared
shared.FPS=60
config.frame_rate=60
BLUE,GOLD,GREEN,PURPLE,RED,GRAY='#58C4DD','#F0C75E','#83C167','#B39DDB','#FC6255','#667785'
COLORS=[GRAY,GOLD,BLUE,GREEN,PURPLE]
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
def residue(r,x,y):return node('['+str(r)+']',x,y,COLORS[r],1.05,.9,43)
def dots(n,x,y,c=BLUE):
 return VGroup(*[Dot([x+(i%4-1.5)*.35,y-(i//4)*.4,0],radius=.1,color=c) for i in range(n)])
def sample_grid(y=2.8):
 return VGroup(*[eq(str(n),size=28,color=INK).move_to([((n+5)%10-4.5)*.68,y-((n+5)//10)*1.15,0]) for n in range(-5,25)])
class ModularScene(PadicScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.header)
  self.header=VGroup(txt('NUMBER THEORY  /  MODULAR ARITHMETIC',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
class Shot01(ModularScene):
 shot=0
 def s01(self):
  self.show(eq(r'17\bmod5=2',4.2,85,GOLD),run_time=.7)
  left=node(r'c\equiv m^e\pmod n',-1.95,1.2,BLUE,3.5,1.7,39);right=node(r'x^n+y^n=z^n',1.95,1.2,PURPLE,3.5,1.7,43)
  self.show(left,right,txt('현대 암호학',-.4,28,BLUE,x=-1.95,width=3.5),txt('수론의 문제',-.4,28,PURPLE,x=1.95,width=3.5))
  self.show(Line([0,3.2,0],[-1.95,2.05,0],color=MUTED),Line([0,3.2,0],[1.95,2.05,0],color=MUTED));self.to(11)
  self.show(eq('?',-2.2,113,GOLD),txt('단순한 나머지가 어떻게 수학적 도구가 될까?',-3.9,30));self.to(16)
class Shot02(ModularScene):
 shot=1
 def s02(self):
  numbers=sample_grid(3.8);self.play(LaggedStart(*[FadeIn(n) for n in numbers],lag_ratio=.02),run_time=1.2);ellipsis=eq(r'\ldots,-2,-1,0,1,2,\ldots',-.2,44,MUTED);self.show(ellipsis);self.to(20);self.remove(ellipsis)
  targets=[[(n%5-2)*1.4,3.5-((n+5)//5)*.65,0] for n in range(-5,25)]
  self.play(*[n.animate.move_to(t).set_color(COLORS[v%5]) for n,t,v in zip(numbers,targets,range(-5,25))],run_time=1.5)
  self.show(*[residue(r,(r-2)*1.4,-1.1) for r in range(5)],txt('나머지는 0, 1, 2, 3, 4뿐',-2.6,35,GOLD));self.to(26)
  self.play(*[n.animate.set_opacity(1 if v in [1,6,11,16] else .15) for v,n in zip(range(-5,25),numbers)],run_time=.6)
  self.show(eq(r'1\equiv6\equiv11\equiv16\pmod5',-3.9,48,GOLD));self.to(32)
class Shot03(ModularScene):
 shot=2
 def s03(self):
  self.show(eq(r'a\equiv b\pmod n\quad\Longleftrightarrow\quad n\mid(a-b)',4.4,44),txt('나머지가 같으면 합동',3.2,32,GREEN))
  row=VGroup(*[node(str(v),x,1.8,GOLD,1,.9,40) for x,v in zip([-2.8,-1.4,0,1.4,2.8],[1,6,11,16,21])]);self.show(row);self.to(37)
  target=node('[1]',0,-.6,GOLD,1.7,1.3,67);self.play(TransformFromCopy(row,target),run_time=1)
  self.show(eq(r'[1]=\{\ldots,-4,1,6,11,16,\ldots\}',-2.4,45),txt('동치류  /  Equivalence Class',-3.9,28,GOLD));self.to(41)
class Shot04(ModularScene):
 shot=3
 def s04(self):
  self.show(eq('[2]+[3]',2.2,85,BLUE),txt('집단 사이에서도 연산할 수 있을까?',-.1,34));self.to(46)
  self.clear();self.show(eq('17+28',4.3,85));self.to(51)
  left=node('45',-1.9,2,GREEN,2.7,1.2,69);right=node('2+3',1.9,2,BLUE,2.7,1.2,64)
  self.show(Line([0,3.4,0],[-1.9,2.65,0],color=MUTED),Line([0,3.4,0],[1.9,2.65,0],color=MUTED),left,right,txt('먼저 더하기',3,26,MUTED,x=-1.9,width=3),txt('먼저 나머지',3,26,MUTED,x=1.9,width=3),run_time=.6)
  self.show(eq(r'\bmod5',.6,35,MUTED,x=-1.9),eq('5',.6,64,BLUE,x=1.9),run_time=.5)
  self.show(eq('0',-1.2,88,GREEN,x=-1.9),eq(r'5\bmod5=0',-1.2,53,BLUE,x=1.9),run_time=.7)
  self.show(eq('0=0',-3.2,70,GREEN),txt('같은 나머지',-4.3,29,GREEN),run_time=.6);self.to(59)
class Shot05(ModularScene):
 shot=4
 def s05(self):
  self.show(txt('정수 연산',4.6,29,MUTED,x=-1.9),txt('나머지 연산',4.6,29,BLUE,x=1.9))
  self.show(eq(r'17-28=-11',3.3,45,x=-1.9,width=3.6),eq(r'2-3=-1',3.3,45,BLUE,x=1.9,width=3.6),eq(r'4\equiv4\pmod5',1.8,62,GREEN));self.to(62)
  self.show(eq(r'17\times28=476',.2,43,x=-1.9,width=3.6),eq(r'2\times3=6',.2,43,BLUE,x=1.9,width=3.6),eq(r'1\equiv1\pmod5',-1.3,62,GREEN),txt('덧셈 · 뺄셈 · 곱셈에서 유지',-3.5,34,GOLD));self.to(68)
class Shot06(ModularScene):
 shot=5
 def s06(self):
  question=txt('나눗셈도 같은 관계를 보존할까?',2.2,39,GOLD);self.show(question);self.to(73)
  self.clear();self.show(eq(r'8\equiv2\pmod6',4.5,72,GREEN),dots(8,-1.9,2.8,GRAY),dots(2,1.9,2.8,BLUE));self.to(76)
  self.show(eq(r'\div2',1.1,49,GOLD,x=-1.9),eq(r'\div2',1.1,49,GOLD,x=1.9))
  self.show(dots(4,-1.9,-.2,PURPLE),dots(1,1.9,-.2,GOLD));self.show(eq(r'4\not\equiv1\pmod6',-2,75,RED));self.to(82)
  self.show(txt('같은 나머지였지만 나눈 뒤에는 달라진다',-3.4,29,RED),eq(r'\text{correct cancellation: }4\equiv1\pmod3',-4.35,30,MUTED));self.to(88)
class Shot07(ModularScene):
 shot=6
 def s07(self):
  self.show(txt('나눗셈을 대신할 연산은?',2.4,41,PURPLE));self.to(91)
  self.clear();self.show(eq(r'2a\equiv1\pmod5',4.5,71))
  row=VGroup(*[node(str((2*k)%5),x,1.8,GREEN if k==3 else MUTED,1.05,1.0,46).add(txt('×'+str(k),3.2,26,GOLD,x=x,width=1)) for x,k in zip([-2.8,-1.4,0,1.4,2.8],range(5))]);self.show(row)
  self.show(eq(r'2\times3=6\equiv1\pmod5',-.7,63,GREEN));self.to(96)
  self.clear();self.show(eq(r'2^{-1}\equiv3\pmod5',4.4,72,PURPLE))
  for x,v in [(-2.6,'2'),(0,'4'),(2.6,'2')]:self.show(node(v,x,2,GOLD if x==0 else BLUE,1.25,1.2,67),run_time=.15)
  self.show(Arrow([-1.9,2,0],[-.7,2,0],buff=0,color=GOLD),Arrow([.7,2,0],[1.9,2,0],buff=0,color=PURPLE),eq(r'\times2',3.1,36,GOLD,x=-1.3),eq(r'\times3',3.1,36,PURPLE,x=1.3),eq(r'(a\times2)\times3\equiv a\pmod5',-.2,56),eq(r'\div2\quad\longleftrightarrow\quad\times3',-2,61,PURPLE));self.to(101)
  self.show(txt('곱셈의 역원',-3.8,39,PURPLE),run_time=.4);self.to(103)
class Shot08(ModularScene):
 shot=7
 def s08(self):
  self.show(node(r'\gcd(2,5)=1',-1.9,3.7,GREEN,3.3,1.2,39),node(r'\gcd(2,6)=2',1.9,3.7,RED,3.3,1.2,39),run_time=.4)
  self.show(eq('0,2,4,1,3',1.8,41,GREEN,x=-1.9,width=3.5),eq('0,2,4,0,2,4',1.8,36,RED,x=1.9,width=3.5),txt('역원 존재',.5,31,GREEN,x=-1.9),txt('역원 없음',.5,31,RED,x=1.9),run_time=.4)
  self.show(eq(r'a^{-1}\;\text{exists}\quad\Longleftrightarrow\quad\gcd(a,n)=1',-1.6,47,PURPLE),txt('나누려는 수와 기준수가 서로소일 때',-3.5,32),run_time=.4);self.to(108)
class Shot09(ModularScene):
 shot=8
 def s09(self):
  self.show(eq(r'7^{16}\bmod10\;=?',3.5,88,GOLD),txt('큰 거듭제곱의 나머지를 계산하려면?',1.2,34));self.to(111)
  self.clear();self.show(txt('정수 전체 계산',4.8,27,MUTED,x=-1.4),txt('매번 mod 10',4.8,27,BLUE,x=2.6,width=2.4))
  rows=VGroup()
  for i,k in enumerate([1,2,4,8,16]):
   y=3.6-i*.95;rows.add(VGroup(eq('7^{'+str(k)+'}',y,33,GOLD,x=-3.3,width=1),eq(f'{7**k:,}',y,37,x=-.5,width=4.1),eq(str(pow(7,k,10)),y,47,BLUE,x=2.6,width=1)))
  self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.18),run_time=1.8)
  self.show(eq(r'7^{16}\equiv1\pmod{10}',-2.4,59,GREEN),txt('중간 계산의 수 크기를 작게 유지',-3.9,29));self.to(120)
  self.clear();self.show(txt('RSA의 핵심 연산',4.6,30,BLUE),eq(r'c\equiv m^e\pmod n',3.1,71),node('m',-2.7,.8,BLUE,1.5,1.4,75),node(r'\mathrm{modular\ power}',0,.8,PURPLE,3.2,1.4,34),node('c',2.7,.8,GREEN,1.5,1.4,75),txt('메시지',-.5,28,BLUE,x=-2.7),txt('암호문',-.5,28,GREEN,x=2.7),txt('모듈러 거듭제곱',-2.6,37,PURPLE),run_time=.5);self.to(124)
class Shot10(ModularScene):
 shot=9
 def s10(self):
  self.show(txt('계산의 효율을 넘어, 정수 해의 존재로',2.5,37,PURPLE));self.to(129)
  self.clear();self.show(eq(r'x^2+y^2=2023',4.8,68))
  a=Axes(x_range=[-50,50,10],y_range=[-50,50,10],x_length=5.6,y_length=5.6,tips=False,axis_config=dict(color=MUTED,stroke_width=1.1)).move_to([0,.7,0]);grid=VGroup(*[Dot(a.c2p(x,y),radius=.018,color=MUTED,fill_opacity=.45) for x in range(-50,51,10) for y in range(-50,51,10)])
  circle=Circle(radius=math.sqrt(2023)*.056,color=BLUE).move_to(a.c2p(0,0));self.show(a,grid,circle,txt('이 원 위에 정수 좌표인 점이 있을까?',-2.8,32,GOLD),txt('격자는 일부만 표시 · 존재 여부는 합동으로 증명',-4.1,23,MUTED),run_time=.6);self.to(135)
class Shot11(ModularScene):
 shot=10
 def s11(self):
  self.show(eq(r'x\bmod4\in\{0,1,2,3\}',4.5,49),run_time=.35)
  top=VGroup(*[node(str(k),x,2.8,BLUE,1.2,1,52) for x,k in zip([-2.7,-.9,.9,2.7],range(4))]);self.show(top,run_time=.4)
  self.show(*[eq(str(k*k),.9,53,x=x) for x,k in zip([-2.7,-.9,.9,2.7],range(4))],txt('제곱',1.9,23,MUTED),run_time=.4)
  self.show(*[node(str((k*k)%4),x,-1,GOLD,1.2,1,52) for x,k in zip([-2.7,-.9,.9,2.7],range(4))],txt('mod 4',-.1,24,MUTED),txt('가능한 제곱의 나머지: 0 또는 1',-3,35,GREEN),run_time=.5);self.to(139)
class Shot12(ModularScene):
 shot=11
 def s12(self):
  self.show(eq(r'x^2+y^2\pmod4',4.6,57))
  sums=VGroup(*[node(s,x,y,GREEN,2.7,1,46) for s,x,y in [('0+0=0',-1.7,2.9),('0+1=1',1.7,2.9),('1+0=1',-1.7,1.3),('1+1=2',1.7,1.3)]]);self.show(sums,eq(r'\{0,1,2\}',-.6,74,GREEN));self.to(143)
  self.show(eq(r'2023=4\times505+3\equiv3\pmod4',-2.4,49,RED),txt('우변의 나머지 3은 이 집합에 없다',-4,31,RED));self.to(147)
class Shot13(ModularScene):
 shot=12
 def s13(self):
  self.show(eq(r'x^2+y^2=2023',4.5,71))
  self.show(txt('좌변 mod 4',2.9,30,GREEN,x=-1.8),txt('우변 mod 4',2.9,30,RED,x=2.1),eq(r'\{0,1,2\}',1.4,73,GREEN,x=-1.8,width=3.6),eq('3',1.4,92,RED,x=2.1))
  self.show(eq(r'\{0,1,2\}\not\ni3',-.5,65,RED),txt('정수 해가 존재하지 않는다',-2.3,44,RED),eq(r'\nexists\,(x,y)\in\mathbb Z^2:\ x^2+y^2=2023',-4,43));self.to(154)
class Shot14(ModularScene):
 shot=13
 def s14(self):
  self.show(txt('디오판토스 방정식',4.7,34,BLUE),eq(r'x^2+y^2=2023',3.3,58),txt('방정식의 정수 해를 연구',1.9,32))
  self.show(eq(r'x^n+y^n=z^n',.2,72,PURPLE),eq(r'n>2,\quad x,y,z\in\mathbb Z_{>0}',-1.5,45,PURPLE),txt('페르마의 마지막 정리',-2.8,34,PURPLE));self.to(161)
  self.show(txt('전체 증명에는 더 깊은 수학적 이론이 필요',-4.2,25,MUTED));self.to(165)
class Shot15(ModularScene):
 shot=14
 def s15(self):
  row=VGroup(*[eq(str(n),size=32,color=COLORS[n%5]) for n in range(-2,11)]).arrange(RIGHT,buff=.18).scale_to_fit_width(7.2).move_to([0,3.5,0]);self.show(eq(r'\mathbb Z',4.8,72),row)
  classes=VGroup(*[residue(r,(r-2)*1.4,1.1) for r in range(5)]);self.play(TransformFromCopy(row,classes),run_time=1)
  self.show(eq(r'\mathbb Z/5\mathbb Z',-.5,75,BLUE));self.to(170)
  self.show(txt('복잡한 계산을 단순하게',-2.2,34,BLUE),txt('수학적 성질과 정수 해를 연구',-3.8,34,GREEN));self.to(178)
