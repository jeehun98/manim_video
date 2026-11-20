"""171-second Catalan derivation; independently replaceable portrait shots."""
import sys,json
from pathlib import Path
from functools import lru_cache
from math import comb
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.genfunc01_dice.scene import GFScene,txt,eq,BLUE,RED,GOLD,GREEN,INK,MUTED
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
@lru_cache(None)
def trees(n):
 if n==0:return (None,)
 return tuple((a,b) for k in range(n) for a in trees(k) for b in trees(n-1-k))
def catalan(n):return comb(2*n,n)//(n+1)
LEAF=(None,None)
SAMPLE=((LEAF,(None,LEAF)),(LEAF,LEAF))
class BinaryTreeMobject(VGroup):
 def __init__(self,shape,width=3.2,level=.8,radius=.12,color=None):
  super().__init__();self.edges=VGroup();self.nodes=VGroup();self.branches=[VGroup(),VGroup()];self.root=None
  if shape is None:
   self.add(eq(r'\varnothing',size=44,color=MUTED));return
  def walk(t,x,y,spread,c,branch=None):
   node=Dot([x,y,0],radius=radius,color=c);self.nodes.add(node)
   if branch is not None:self.branches[branch].add(node)
   if self.root is None:self.root=node
   for j,child in enumerate(t):
    if child is None:continue
    dx=(-1 if j==0 else 1)*spread
    cc=color or (BLUE if j==0 else RED) if branch is None else c
    b=j if branch is None else branch
    edge=Line([x,y,0],[x+dx,y-level,0],color=cc,stroke_width=2.5)
    self.edges.add(edge);self.branches[b].add(edge)
    walk(child,x+dx,y-level,spread*.53,cc,b)
  walk(shape,0,0,width/4,color or GOLD)
  self.add(self.edges,self.nodes);self.move_to(ORIGIN)
def gallery(n):
 g=VGroup(*[BinaryTreeMobject(t,width=1.8,level=.6,radius=.11) for t in trees(n)])
 if n<=2:g.arrange(RIGHT,buff=1.1)
 else:g.arrange_in_grid(cols=3,buff=(.65,.8))
 return g.move_to([0,1.8,0])
def abstract():
 root=Dot([0,4.2,0],radius=.22,color=GOLD)
 sides=VGroup()
 for x,c,label in [(-2,BLUE,'왼쪽 트리'),(2,RED,'오른쪽 트리')]:
  triangle=Polygon([x,2.9,0],[x-1.25,.8,0],[x+1.25,.8,0],color=c,fill_color=c,fill_opacity=.1)
  sides.add(VGroup(Line([0,4.2,0],[x,2.9,0],color=c),triangle,eq('C(x)',1.55,49,c,x=x,width=2.2),txt(label,.2,27,c,x=x,width=3)))
 return VGroup(root,sides)
def seq(y=-2.7):
 return VGroup(*[VGroup(txt(str(n),.6,20,MUTED),RoundedRectangle(width=.78,height=.65,corner_radius=.08,fill_color=GREEN,fill_opacity=.16,stroke_width=0),eq(str(catalan(n)),size=32,color=GREEN)) for n in range(7)]).arrange(RIGHT,buff=.22).move_to([0,y,0])
class CatalanScene(GFScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.header)
  self.header=VGroup(txt('MATHEMATICS  /  CATALAN NUMBERS',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
class Shot01(CatalanScene):
 shot=0
 def s01(self):
  row=VGroup(*[VGroup(RoundedRectangle(width=.76,height=.8,corner_radius=.1,fill_color=BLUE if i in (5,6) else '#293343',fill_opacity=.8,stroke_width=0),txt(str(n),size=31)) for i,n in enumerate([0,1,1,2,3,5,8,13])]).arrange(RIGHT,buff=.17).move_to([0,3.4,0])
  self.play(LaggedStart(*[FadeIn(r) for r in row],lag_ratio=.1),run_time=1.3)
  self.show(eq(r'5+8=13',1.9,51,GREEN));self.to(4)
  unknown=VGroup(*[txt('?',size=47,color=MUTED) for _ in range(5)],eq(r'\cdots',size=35),eq('F_{100}',size=50,color=GOLD)).arrange(RIGHT,buff=.5).move_to([0,.2,0])
  self.show(unknown,txt('이전 항의 순차 계산 없이?',-1.4,35,GOLD));self.to(11)
  self.show(eq(r'F_n=\frac1{\sqrt5}\left[\left(\frac{1+\sqrt5}{2}\right)^n-\left(\frac{1-\sqrt5}{2}\right)^n\right]',-3.1,39),run_time=.7);self.to(14)
  self.clear();self.show(eq(r'G(x)=\sum_{n\geq0}a_nx^n',2.7,62),txt('구조의 규칙 → 생성함수 → 일반항',.6,33,BLUE),BinaryTreeMobject(SAMPLE,width=3.5).move_to([0,-2,0]));self.to(20)
class Shot02(CatalanScene):
 shot=1
 def s02(self):
  t=BinaryTreeMobject((LEAF,LEAF),width=5,level=1.3,radius=.2).move_to([0,2.5,0]);self.show(t);self.to(23)
  self.show(txt('왼쪽 L',.5,34,BLUE,x=-2),txt('오른쪽 R',.5,34,RED,x=2),txt('자식은 최대 2개 · 좌우를 구별',-1.3,32));self.to(29)
  self.clear();g=gallery(1);count=eq('C_1=1',-1.7,58,GREEN);self.show(g,count,run_time=.4)
  self.to(30.3);self.play(Transform(g,gallery(2)),Transform(count,eq('C_2=2',-1.7,58,GREEN)),run_time=.6)
  self.to(32);self.play(Transform(g,gallery(3)),Transform(count,eq('C_3=5',-1.7,58,GREEN)),run_time=.7);self.to(35)
  self.show(seq(-3.1),txt('카탈란 수열  /  Catalan Numbers',-4.3,26,BLUE));self.to(42)
  self.play(g.animate.set_opacity(.3),FadeOut(count),run_time=.4);self.show(txt('노드가 많아져도 직접 계산할 수 있을까?',-.3,33,GOLD),eq('C_{10}=?',-1.1,56));self.to(48)
class Shot03(CatalanScene):
 shot=2
 def s03(self):
  t=BinaryTreeMobject(SAMPLE,width=6,level=1.15,radius=.16).move_to([0,2.5,0]);self.show(t);self.to(51)
  root=t.root;left,right=t.branches
  self.play(Indicate(root,color=GOLD),left.animate.shift(LEFT*.35+DOWN*.3),right.animate.shift(RIGHT*.35+DOWN*.3),run_time=1.2)
  self.show(txt('루트',4.7,26,GOLD,x=.65),txt('왼쪽도 이진 트리',-.5,28,BLUE,x=-2),txt('오른쪽도 이진 트리',-.5,28,RED,x=2));self.to(57)
  self.play(Circumscribe(left,color=BLUE),Circumscribe(right,color=RED),run_time=1.3);self.show(txt('부분 구조에서도 같은 분해가 가능하다',-2.1,32));self.to(63)
  self.clear();a=abstract();self.show(a,txt('동일한 종류의 구조가 반복된다',-1.5,34));self.to(67)
  self.show(eq(r'\text{Tree}=\varnothing+\text{Root}\times\text{Tree}\times\text{Tree}',-3.2,37));self.to(70)
class Shot04(CatalanScene):
 shot=3
 def s04(self):
  s=seq(3.2);self.show(s,eq(r'C(x)=\sum_{n=0}^{\infty}C_nx^n',.9,59),txt('Cₙ = 노드가 n개인 이진 트리의 개수',-1.2,31,GREEN));self.to(78)
  self.clear();empty=VGroup(RoundedRectangle(width=1.3,height=1.25,corner_radius=.12,color=MUTED,fill_color=MUTED,fill_opacity=.1),eq(r'\varnothing',size=48,color=MUTED)).move_to([-2.9,4,0]);self.show(empty,txt('빈 트리',2.9,24,MUTED,x=-2.9,width=1.6))
  one=eq('1',-1.1,66,x=-3,color=INK);self.play(TransformFromCopy(empty,one),run_time=.8);unit=eq(r'1x^0=1',-3,40,color=MUTED);self.show(unit);self.to(83)
  self.play(FadeOut(unit),run_time=.3);a=abstract();self.show(a[0],run_time=.4);x=eq('x',-1.1,65,GOLD,x=-1.1);self.play(TransformFromCopy(a[0],x),run_time=.6);self.to(86)
  self.show(a[1],run_time=.6)
  left=eq('C(x)',-1.1,54,BLUE,x=.55,width=1.8);right=eq('C(x)',-1.1,54,RED,x=2.7,width=1.8)
  self.play(TransformFromCopy(a[1][0],left),TransformFromCopy(a[1][1],right),run_time=1.1);self.to(93)
  self.show(eq(r'\cdot',-1.1,42,x=-.4),eq(r'\cdot',-1.1,42,x=1.7),run_time=.4)
  example=eq(r'x\cdot x\cdot x^3=x^5',-2.9,47);countnote=txt('루트 1개 + 왼쪽 1개 + 오른쪽 3개 = 5개',-4.1,26,MUTED);self.show(example,countnote);self.to(97)
  self.play(Transform(example,eq(r'xC(x)^2',-2.9,61)),run_time=.8);self.to(102)
  self.play(FadeOut(example),FadeOut(countnote),run_time=.3);self.show(eq('+',-1.1,46,x=-2.1),eq(r'C(x)=1+xC(x)^2',-2.9,62,color=GREEN),run_time=.8);self.to(107)
class Shot05(CatalanScene):
 shot=4
 def s05(self):
  f=eq(r'C(x)=1+xC(x)^2',3.7,56);self.show(f,run_time=.4)
  q=eq(r'xC(x)^2-C(x)+1=0',1.8,55,GOLD);self.play(TransformFromCopy(f,q),run_time=.8)
  self.show(eq('xy^2-y+1=0',-.1,57),txt('미지수 y = C(x)',.8,27,MUTED));self.to(112)
  self.show(eq(r'a=x,\quad b=-1,\quad c=1',-1.5,39,BLUE),run_time=.4)
  self.show(eq(r'C(x)=\frac{1\pm\sqrt{1-4x}}{2x}',-3.3,62),run_time=.8);self.to(116)
class Shot06(CatalanScene):
 shot=5
 def s06(self):
  self.show(eq('C_0=1',4.5,53,GREEN),eq(r'C_\pm(x)=\frac{1\pm\sqrt{1-4x}}{2x}',2.7,57),txt('빈 트리는 크기 0인 1가지 구조',.8,30));self.to(121)
  self.clear()
  axes=Axes(x_range=[0,.25,.05],y_range=[0,10,2],x_length=6.4,y_length=3.2,tips=False,axis_config=dict(color=MUTED,stroke_width=1.3)).move_to([0,1.8,0])
  plus=axes.plot(lambda x:(1+np.sqrt(1-4*x))/(2*x),x_range=[.095,.25,.001],color=RED)
  minus=axes.plot(lambda x:2/(1+np.sqrt(1-4*x)),x_range=[0,.25,.001],color=GREEN)
  self.show(axes,plus,minus,eq(r'C_+(x)\to+\infty',4.4,37,RED),eq(r'C_-(x)\to1',-.3,37,GREEN),run_time=.7)
  value=ValueTracker(.05)
  marker=always_redraw(lambda:DashedLine(axes.c2p(value.get_value(),0),axes.c2p(value.get_value(),10),color=GOLD,stroke_width=1.5))
  self.add(marker);self.play(value.animate.set_value(.005),run_time=2,rate_func=linear)
  rational=eq(r'\frac{1-\sqrt{1-4x}}{2x}=\frac{2}{1+\sqrt{1-4x}}',-1.9,47)
  self.show(rational,eq(r'\lim_{x\to0}\frac2{1+\sqrt{1-4x}}=1',-3.5,43),run_time=.7);self.to(127)
  marker.clear_updaters();self.clear();self.show(eq(r'C(x)=\frac{1-\sqrt{1-4x}}{2x}',1.8,79,GREEN),txt('상수항 1을 갖는 해',-.6,36),eq(r'C(0)=1\quad\text{(continuous extension)}',-2,34,MUTED),run_time=.6);self.to(130)
class Shot07(CatalanScene):
 shot=6
 def s07(self):
  f=eq(r'C(x)=\frac{1-\sqrt{1-4x}}{2x}',2.9,69);self.show(f,txt('거듭제곱의 계수를 꺼내려면?',.7,35));self.to(134)
  self.clear();binomial=eq(r'(1+t)^\alpha=\sum_{k=0}^{\infty}\binom\alpha k t^k',3.7,52);self.show(binomial,eq(r'\alpha=\frac12,\quad t=-4x',2.1,45,BLUE));self.to(139)
  self.clear();sqrt=eq(r'\sqrt{1-4x}=1-2x-2x^2-4x^3-10x^4-\cdots',4,37);fraction=eq(r'C(x)=\frac{2x+2x^2+4x^3+10x^4+\cdots}{2x}',1.8,49)
  self.show(sqrt);self.play(TransformFromCopy(sqrt,fraction),run_time=1);self.to(144)
  series=eq(r'1+x+2x^2+5x^3+14x^4+42x^5+\cdots',-.3,43,GREEN);self.play(TransformFromCopy(fraction,series),run_time=.7);self.show(seq(-2.3),run_time=.5);self.to(148)
  self.clear();summation=eq(r'C(x)=\sum_{k=1}^{\infty}\left[-\frac12\binom{1/2}{k}(-4)^k\right]x^{k-1}',4,43);self.show(summation,eq(r'k-1=n\quad\Rightarrow\quad k=n+1',2.3,43,GOLD),run_time=.4)
  self.show(eq(r'C_n=-\frac12\binom{1/2}{n+1}(-4)^{n+1}',.4,51),run_time=.5);self.to(151.5)
  final=eq(r'C_n=\frac1{n+1}\binom{2n}{n}=\frac{(2n)!}{n!(n+1)!}',-2.3,58,GREEN);self.show(final,run_time=.6);self.play(Circumscribe(final,color=GREEN),run_time=.7);self.to(154)
class Shot08(CatalanScene):
 shot=7
 def s08(self):
  f=eq(r'C_n=\frac{(2n)!}{n!(n+1)!}',3.8,70);self.show(f,txt('이전 항을 순서대로 구하지 않아도',2.3,31))
  result=eq(r'C_{10}=\frac{20!}{10!\,11!}=16{,}796',.5,58,GREEN);self.show(result,run_time=.8);self.to(158)
  self.show(eq(r'C_{20}=6{,}564{,}120{,}420',-1.5,49,GREEN),txt('노드 수로 원하는 항을 직접 계산',-3.1,31));self.to(161)
  self.clear();a=abstract().scale(.64).move_to([0,3,0]);self.show(a,eq(r'C(x)=1+xC(x)^2',.3,57),txt('구조가 만들어지는 규칙',1.2,27,MUTED));self.to(166)
  self.show(eq(r'C_n=\frac{(2n)!}{n!(n+1)!}',-1.8,60,GREEN),run_time=.6);self.to(169)
  self.show(txt('구조를 세는 대신,\n구조가 만들어지는 규칙을 푼다.',-3.8,31),run_time=.5);self.to(171)
