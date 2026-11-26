"""User-timed 169-second BBP short, native portrait, 23 replaceable shots."""
import sys,json,math
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.padic01_local_global.scene import PadicScene,txt,eq
import longforms.qcs01_speed.direction as shared
shared.FPS=30
config.frame_rate=30
config.background_color='#10141C'
INK,MUTED,BLUE,GOLD,GREEN,RED='#E5E7EB','#94A3B8','#60A5FA','#FACC15','#4ADE80','#F87171'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))

def e(s,y=0,size=48,color=INK,x=0,width=7.3):return eq(s,y,size,color,x,width)
def t(s,y=0,size=30,color=INK,x=0,width=7.3):return txt(s,y,size,color,x,width)
def card(s,x,y,color=BLUE,width=2.6,height=1,size=45):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.12,color=color,stroke_width=1.5,fill_color=color,fill_opacity=.06),e(s,size=size,color=color,width=width-.2)).move_to([x,y,0])
def bbp(y=2.8):
 a=e(r'\pi=\sum_{k=0}^{\infty}\frac{1}{16^k}',y+1.1,62)
 b=e(r'\left(\frac4{8k+1}-\frac2{8k+4}\right.',y-.4,58)
 c=e(r'\left.{}-\frac1{8k+5}-\frac1{8k+6}\right)',y-1.9,58)
 a.set_color_by_tex('16',BLUE,substring=True)
 return VGroup(a,b,c)
def compact(y=3.8):
 return VGroup(e(r'\pi=\sum_{k=0}^{\infty}\frac{B_k}{16^k}',y,62),e(r'B_k=\frac4{8k+1}-\frac2{8k+4}',y-1.5,43,MUTED),e(r'{}-\frac1{8k+5}-\frac1{8k+6}',y-2.6,43,MUTED))
def digitrow(s,y=0,highlight=None,size=51):
 g=VGroup(*[e(c,size=size,color=GOLD if i==highlight else INK) for i,c in enumerate(s)]).arrange(RIGHT,buff=.105)
 if g.width>7.2:g.scale_to_fit_width(7.2)
 return g.move_to([0,y,0])
def hexrow(y=3.3,shifted=False):return digitrow('3243.F6A888…' if shifted else '3.243F6A88…',y,5,51)
def split_formula(y=3.8):
 return VGroup(e(r'16^n\pi=',y,52,BLUE),e(r'\underbrace{\sum_{k=0}^{n}16^{n-k}B_k}_{A}',y-1.6,55,BLUE),e(r'{}+\underbrace{\sum_{k=n+1}^{\infty}16^{n-k}B_k}_{T}',y-3.5,55,GREEN))
def two_sums():
 return VGroup(e(r'16^n\pi=A+T',4.3,62),e(r'A=\sum_{k=0}^{n}16^{n-k}B_k',2.8,43,BLUE,x=-1.9,width=3.6),e(r'T=\sum_{r=1}^{\infty}\frac{B_{n+r}}{16^r}',2.8,43,GREEN,x=1.9,width=3.6),Line([-3.6,1.9,0],[3.6,1.9,0],color=MUTED,stroke_opacity=.3))
def network(extra=False):
 center=VGroup(Circle(radius=.75,color=BLUE,stroke_width=1.5),e(r'\pi',size=85, color=BLUE)).move_to([0,.5,0])
 labels=[('기하학',0,4.1),('무한급수',-2.6,2.2),('확률론',2.6,2.2),('적분 표현',-2.6,-1.8),('물리학',2.6,-1.8)]
 if extra:labels[-1]=('BBP 알고리즘',2.4,-1.8)
 links=VGroup(*[DashedLine([0,.5,0],[x,y-.3,0],color=GREEN if extra and 'BBP' in s else MUTED,stroke_width=1.1,dash_length=.1) for s,x,y in labels])
 names=VGroup(*[t(s,y,27,GREEN if 'BBP' in s else INK,x=x,width=2.8) for s,x,y in labels])
 return VGroup(links,center,names)

class BBPScene(PadicScene):
 data=DATA
 def setup(self):
  super().setup();self.remove(self.header)
  self.header=VGroup(t('THE STRUCTURE OF π  /  BBP FORMULA',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
 def change(self,a,b,seconds=.8):self.play(ReplacementTransform(a,b),run_time=seconds);return b

class Shot01(BBPScene):
 shot=0
 def s01(self):
  c=Circle(radius=1.1,color=BLUE).move_to([0,2.5,0]);d=Line([-1.1,2.5,0],[1.1,2.5,0],color=GOLD)
  self.play(Create(c),Create(d),run_time=.6);self.show(e('C',3.5,34,BLUE,x=1.4),e('d',2.1,32,GOLD),run_time=.3)
  length=2*PI*1.1
  arc=c.copy();self.add(arc)
  def unwrap(m,a):
   angle=max(TAU*(1-a),.001);r=length/angle;base=1.4*(1-a)-.6*a
   curve=ParametricFunction(lambda u:np.array([r*np.sin(angle*u),base+r*(np.cos(angle*u)-np.cos(angle/2)),0]),t_range=[-.5,.5,.005],color=BLUE)
   m.become(curve)
  self.play(UpdateFromAlphaFunc(arc,unwrap),run_time=1.4,rate_func=smooth)
  marks=VGroup(*[Line([-length/2+2.2*i,-.77,0],[-length/2+2.2*i,-.43,0],color=GOLD) for i in range(4)])
  self.show(marks,e(r'\frac Cd=\pi\approx3.141592\ldots',-2.5,59),run_time=.6);self.to(4)

class Shot02(BBPScene):
 shot=1
 def s02(self):
  g=network();self.play(LaggedStart(FadeIn(g[1]),Create(g[0]),FadeIn(g[2]),lag_ratio=.25),run_time=1.8)
  self.show(t('하나의 상수, 서로 다른 수학적 구조',-3.8,29,MUTED));self.to(11)

class Shot03(BBPScene):
 shot=2
 def s03(self):
  a=e(r'1+\frac14+\frac19+\cdots=\frac{\pi^2}{6}',2.4,65);self.show(t('해석학 · 바젤 급수',4.7,29,BLUE),a)
  bars=VGroup(*[Rectangle(width=.48,height=2/(k*k),fill_opacity=.8,color=BLUE).move_to([-1.8+(k-1)*.6,-1+1/(k*k),0]) for k in range(1,8)]);self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.08),run_time=.7);self.to(14.5)
  self.clear();axes=Axes(x_range=[-3.5,3.5,1],y_range=[0,.5,.1],x_length=6.3,y_length=2.7,tips=False,axis_config=dict(stroke_opacity=.3));axes.move_to([0,1.4,0]);curve=axes.plot(lambda x:math.exp(-x*x/2)/math.sqrt(2*PI),color=BLUE)
  self.show(t('확률론 · 표준정규분포',4.7,29,BLUE),axes,curve,e(r'f(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}',-1.5,66));self.to(18)
  self.clear();orbit=Ellipse(width=5,height=2.5,color=BLUE).move_to([0,2,0]);sun=Dot([-1,2,0],radius=.14,color=GOLD);planet=Dot(orbit.point_from_proportion(.1),color=BLUE)
  self.show(t('물리학 · 두 물체의 궤도',4.7,29,BLUE),orbit,sun,planet,e(r'T^2=\frac{4\pi^2}{G(M+m)}a^3',-.9,60),t('뉴턴 중력 · 타원 궤도',-3.2,27,MUTED));self.play(MoveAlongPath(planet,orbit),run_time=1.4);self.to(22)

class Shot04(BBPScene):
 shot=3
 def s04(self):
  center=e(r'\pi',.7,115,BLUE);self.show(center)
  forms=[e(r'\frac Cd',4.1,58),e(r'4\left(1-\frac13+\frac15-\cdots\right)',.7,43,x=-2.5,width=3.2),e(r'4\int_0^1\frac{dx}{1+x^2}',.7,48,x=2.5,width=3.2),e(r'3.14159265358979\ldots',-2.9,51)]
  for f in forms:self.show(DashedLine(center.get_center(),f.get_center(),color=MUTED,stroke_opacity=.4),f,run_time=.7)
  self.show(t('수는 같아도, 표현은 다양하다',-4.2,28,MUTED));self.to(32)

class Shot05(BBPScene):
 shot=4
 def s05(self):
  self.show(e('1995',4.6,57,GOLD),t('Bailey · Borwein · Plouffe',3.4,27,MUTED),bbp(.8),run_time=.7);self.to(37)
  self.show(t('BBP Formula',-3.8,43,BLUE),run_time=.4);self.to(38)

class Shot06(BBPScene):
 shot=5
 def s06(self):
  rows=VGroup(*[digitrow(s,4-i*.8,size=37) for i,s in enumerate(['3.141592653589','7932384626433','8327950288419','7169399375105','8209749445923'])]);self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.13),run_time=1.4)
  self.show(e(r'\vdots',-.9,65,MUTED),t('소수점 아래 1,000,000,000번째',-2.4,30,GOLD),card('?',0,-3.8,GOLD,1.1,.9,54));self.to(46)

class Shot07(BBPScene):
 shot=6
 def s07(self):
  h=hexrow(.7);self.show(t('10진법',4.5,28,MUTED),e(r'3.141592653589\ldots',3.3,55),t('16진법',1.9,28,BLUE),h)
  row=digitrow('3.???F????…',.7,5);self.to(49);self.play(Transform(h,row),run_time=.8)
  self.show(card(r'\mathrm{BBP}',0,-2.4,GREEN,2.7,1.1,53),Arrow([0,-1.8,0],[0,0,0],color=GREEN),t('앞의 자릿수를 구하지 않고 추출',-4.1,30,GREEN));self.to(54)

class Shot08(BBPScene):
 shot=7
 def s08(self):
  self.show(e(r'16^n\times\pi',2.8,91,BLUE),t('특정 숫자를 어떻게 추출할까?',-.4,40),e(r'\{16^n\pi\}',-2.8,77,GREEN));self.to(57)

class Shot09(BBPScene):
 shot=8
 def s09(self):
  whole=bbp(2.8);self.add(whole);self.to(59)
  simple=compact();self.change(whole,simple,1)
  self.show(e(r'=B_0+\frac{B_1}{16}+\frac{B_2}{16^2}+\cdots',-1.3,57),t('네 분수의 조합을 Bₖ로 묶는다',-3.8,29,MUTED),run_time=.5);self.to(62)

class Shot10(BBPScene):
 shot=9
 def s10(self):
  f=compact();self.add(f);self.to(63)
  self.play(f.animate.scale(.65).move_to([0,3.8,0]),run_time=.6)
  weights=VGroup(*[card(r'\frac1{'+('1' if k==0 else '16' if k==1 else '16^'+str(k))+'}',x,.4,BLUE,1.55,1.5,57) for k,x in enumerate([-2.7,-.9,.9,2.7])]);self.play(LaggedStart(*[FadeIn(w) for w in weights],lag_ratio=.15),run_time=.8)
  self.show(*[e('k='+str(k),-1,30,MUTED,x=x) for k,x in enumerate([-2.7,-.9,.9,2.7])],t('16진법과 연결되는 가중치',-3.4,32,BLUE));self.to(67)

class Shot11(BBPScene):
 shot=10
 def s11(self):
  dec=digitrow('3.14159265…',3.3);self.show(t('10진법: ×10',4.6,30,BLUE),dec)
  for i in range(1,4):
   self.to(67+i);dec=self.change(dec,digitrow(['31.4159265…','314.159265…','3141.59265…'][i-1],3.3),.55)
  self.to(71);hex=hexrow(-.7);self.show(t('16진법: ×16',.6,30,BLUE),hex,run_time=.4)
  for i in range(1,4):
   self.to(71+i);hex=self.change(hex,digitrow(['32.43F6A88…','324.3F6A88…','3243.F6A88…'][i-1],-.7,5),.4)
  self.to(75);self.play(FadeOut(dec),*[FadeOut(m) for m in self.mobjects if isinstance(m,Text) and m not in [self.title,self.caption]],Transform(hex,hexrow(3.3)),run_time=.6);self.to(76)

class Shot12(BBPScene):
 shot=11
 def s12(self):
  original=hexrow(3.3);self.add(original);self.show(t('16진법 · 네 번째 숫자 F',4.6,28,GOLD),run_time=.4)
  self.show(e(r'\times16^3',1.7,60,BLUE),run_time=.4);shifted=hexrow(.1,True)
  self.play(TransformFromCopy(original,shifted),GrowArrow(Arrow([0,1.1,0],[0,.65,0],color=BLUE)),run_time=.8)
  self.show(e(r'\pi=(3.d_1d_2\cdots d_n d_{n+1}\cdots)_{16}',-1.9,43),e(r'\times16^n\quad\Longrightarrow\quad d_{n+1}\text{ first}',-3.5,41,GOLD));self.to(82)

class Shot13(BBPScene):
 shot=12
 def s13(self):
  row=hexrow(.1,True);self.add(row);self.to(83)
  boxes=VGroup(card('3243',-1.95,2.6,RED,3.3,1.2,66),card(r'\mathrm{F6A}\ldots',1.95,2.6,GREEN,3.3,1.2,60));self.change(row,boxes,.8)
  self.show(t('정수 부분',3.8,29,RED,x=-1.95),t('소수 부분',3.8,29,GREEN,x=1.95))
  self.play(boxes[0].animate.set_opacity(.15),TransformFromCopy(boxes[1],e(r'(0.\mathrm{F6A}\ldots)_{16}',.1,74,GREEN)),run_time=.8)
  self.show(e(r'\{x\}=x-\lfloor x\rfloor',-2,56),e(r'\{16^3\pi\}=(0.\mathrm{F6A}\ldots)_{16}',-3.8,47,GREEN));self.to(89)

class Shot14(BBPScene):
 shot=13
 def s14(self):
  fractional=e(r'\{16^3\pi\}=(0.\mathrm{F6A}\ldots)_{16}',-3.8,47,GREEN);self.add(fractional)
  f=e(r'\pi=\sum_{k=0}^{\infty}\frac{B_k}{16^k}',3.8,62);self.show(f)
  self.to(91);g=e(r'16^n\pi=\sum_{k=0}^{\infty}\frac{16^n}{16^k}B_k',2.6,59,BLUE);self.change(f,g,1)
  self.to(94);h=e(r'16^n\pi=\sum_{k=0}^{\infty}16^{n-k}B_k',3.8,62,BLUE);self.change(g,h,1)
  self.show(e(r'\frac{16^n}{16^k}=16^{n-k}',.6,73,BLUE),t('곱셈과 지수법칙',-1.8,30,MUTED));self.to(97)

class Shot15(BBPScene):
 shot=14
 def s15(self):
  f=e(r'16^n\pi=\sum_{k=0}^{\infty}16^{n-k}B_k',3.8,62,BLUE);self.add(f)
  powers=VGroup(*[e(s,1.5,43,BLUE if i<3 else GREEN,x=x) for i,(s,x) in enumerate(zip(['16^2','16^1','16^0','16^{-1}','16^{-2}'],[-2.8,-1.4,0,1.4,2.8]))]);self.show(powers,DashedLine([.7,2.2,0],[.7,.3,0],color=MUTED),t('k ≤ n',.1,32,BLUE,x=-1.7),t('k > n',.1,32,GREEN,x=2),run_time=.5)
  sums=VGroup(e(r'A=\sum_{k=0}^{n}16^{n-k}B_k',-1.4,48,BLUE),e(r'T=\sum_{k=n+1}^{\infty}16^{n-k}B_k',-3.5,48,GREEN));self.play(TransformFromCopy(f,sums),run_time=.8);self.to(101)
  self.clear();self.add(two_sums());self.to(102)

class Shot16(BBPScene):
 shot=15
 def s16(self):
  self.add(two_sums());sample=e(r'\frac{256}{7}=36+\frac47',.6,70);self.show(sample,run_time=.5)
  self.to(104);rem=e(r'256\bmod7=4',.6,70,GREEN);self.change(sample,rem,.7)
  general=e(r'\left\{\frac{16^{n-k}}{8k+j}\right\}=\frac{16^{n-k}\bmod(8k+j)}{8k+j}',-1.5,48,GREEN);self.show(general,run_time=.6)
  self.show(e(r'j\in\{1,4,5,6\},\quad k\le n',-3,37,MUTED),t('각 분수를 계산한 뒤 계수 4, −2, −1, −1 결합',-4.2,25,MUTED),run_time=.4);self.to(109)

class Shot17(BBPScene):
 shot=16
 def s17(self):
  self.add(two_sums());base=-1.1
  bars=VGroup(*[Rectangle(width=.8,height=max(2.1/16**i,.008),color=GREEN,fill_opacity=.65).move_to([-2.7+i*1.8,base+max(2.1/16**i,.008)/2,0]) for i in range(4)])
  self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.2),run_time=1.2)
  self.show(Line([-3.4,base,0],[3.4,base,0],color=MUTED),*[e(r'16^{-'+str(i+1)+'}',-1.8,34,GREEN,x=-2.7+i*1.8) for i in range(4)],t('막대는 16⁻ʳ 가중치의 감소를 표시',-2.7,25,MUTED),run_time=.5)
  self.to(114);self.show(e(r'T_R=\sum_{r=1}^{R}\frac{B_{n+r}}{16^r}',.9,42,GREEN),e(r'|T-T_R|\le\frac8{15\cdot16^R}',-4,43,GREEN),run_time=.5);self.to(118)

class Shot18(BBPScene):
 shot=17
 def s18(self):
  self.add(two_sums());a=card(r'\{A\}',-1.8,.5,BLUE,2.8,1.3,70);b=card('T_R',1.8,.5,GREEN,2.8,1.3,70);self.show(a,b,run_time=.5)
  comb=e(r'\{16^n\pi\}\approx\{\{A\}+T_R\}',.4,57,GREEN);self.to(120);self.play(ReplacementTransform(VGroup(a,b),comb),run_time=.7)
  self.show(e(r'd_{n+1}=\left\lfloor16\{16^n\pi\}\right\rfloor',-1.3,51),run_time=.4)
  self.to(122);self.show(e(r'n=3:\quad\lfloor16\times0.963509\ldots\rfloor=15',-2.8,42),e(r'15_{10}=\mathrm F_{16}',-4,56,GOLD),run_time=.5)
  self.play(FadeOut(comb),run_time=.2);self.add(t('오차가 자릿수 경계를 넘지 않도록 계산',.4,28,GREEN));self.to(125)

class Shot19(BBPScene):
 shot=18
 def s19(self):
  self.show(e(r'\pi',4.2,95),t('동일한 실수',3.1,28,MUTED))
  self.show(card(r'3.14159\ldots',-1.9,.9,INK,3.4,1.2,46),card(r'3.243\mathrm F6\ldots',1.9,.9,BLUE,3.4,1.2,46),t('10진법',2.1,29,x=-1.9),t('16진법',2.1,29,BLUE,x=1.9))
  self.show(t('BBP와 같은 효율의\n자릿수 추출: 미발견',-1.5,29,MUTED,x=-1.9,width=3.4),t('BBP 방식으로\n특정 자릿수 추출',-1.5,29,GREEN,x=1.9,width=3.4),t('10진법 추출 자체가 불가능하다는 뜻은 아니다',-4.1,25,MUTED));self.to(136)

class Shot20(BBPScene):
 shot=19
 def s20(self):
  self.show(e(r'\alpha=\sum_{k=0}^{\infty}\frac{p(k)}{b^kq(k)}',4,60),t('BBP 유형의 표현',2.6,29,BLUE))
  constants=VGroup(card(r'\pi',-2.4,.8,BLUE,1.8,1.2,68),card(r'\ln2',0,.8,GREEN,1.8,1.2,56),card(r'\pi^2',2.4,.8,BLUE,1.8,1.2,65));self.show(constants)
  self.show(e(r'\ln2=\sum_{k=1}^{\infty}\frac1{k2^k}',-1.2,59,GREEN),t('자릿수 분포도 새로운 연구 대상',-3,30),t('π의 정상성: 모든 숫자열의 균등한 빈도는 미해결',-4.2,24,MUTED));self.to(145)

class Shot21(BBPScene):
 shot=20
 def s21(self):
  rows=VGroup(*[digitrow(s,4-i*.85,size=39).set_opacity(.17) for i,s in enumerate(['314159265358979','323846264338327','950288419716939','937510582097494','459230781640628'])]);self.show(rows)
  self.to(147);self.play(rows.animate.set_opacity(.05),run_time=.7);self.show(e(r'\pi',1,154,BLUE),t('더 많은 자릿수 ≠ 더 완전한 이해',-2.5,35),run_time=.5);self.to(150)

class Shot22(BBPScene):
 shot=21
 def s22(self):
  g=network(True);self.show(g,run_time=1)
  extra=VGroup(t('자릿수 분포',-3.4,30,GREEN),Line([0,-.25,0],[0,-2.8,0],color=GREEN,stroke_width=1.4));self.show(extra)
  self.show(t('표현 · 성질 · 연결',-4.3,27,MUTED));self.to(161)

class Shot23(BBPScene):
 shot=22
 def s23(self):
  ring=Circle(radius=2.1,color=BLUE,stroke_opacity=.35);inner=DashedVMobject(Circle(radius=1.8,color=BLUE,stroke_opacity=.4),num_dashes=55);g=VGroup(ring,inner,e(r'\pi',size=185)).move_to([0,1.9,0]);self.show(g,run_time=1)
  self.show(e(r'3.14159265358979\ldots',-1.3,53,BLUE),t('오래전부터 알고 있었던 수',-2.9,31),t('여전히 이해하고 있는 수',-4.1,31,BLUE));self.to(169)
