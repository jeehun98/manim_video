"""178-second p-adic short; local expansion, residues, metric, completion."""
import sys,json,math
from pathlib import Path
from bisect import bisect_right
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from episodes.genfunc01_dice.scene import GFScene,txt,eq,INK,MUTED
BLUE,GOLD,GREEN,PURPLE='#58C4DD','#F0C75E','#83C167','#B39DDB'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.background_color='#0D1117'
def poly(x):return (x-2)*(x-3)**2*(x*x+1)
def shifted(h):return 10*h*h+16*h**3+7*h**4+h**5
def node(s,x,y,c=GREEN,width=1.1,height=.65,size=29):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.1,color=c,fill_color=c,fill_opacity=.08),eq(s,size=size,color=c,width=width-.15)).move_to([x,y,0])
def rings(y=0,scale=1):
 g=VGroup(*[Circle(radius=r,color=GREEN,stroke_opacity=.4).move_to([0,y,0]) for r in [.65,1.2,1.75]],Dot([0,y,0],color=GOLD),Dot([.25,y+.2,0],color=GREEN));return g.scale(scale)
def graph():
 a=Axes(x_range=[-.3,4.3,1],y_range=[-25,80,20],x_length=6.8,y_length=3.7,tips=False,axis_config=dict(color=MUTED,stroke_width=1.3)).move_to([0,.15,0])
 c=a.plot(poly,x_range=[-.1,4.2,.02],color=BLUE)
 labels=VGroup(*[eq(str(x),size=22,color=MUTED).move_to(a.c2p(x,0)+DOWN*.3) for x in range(5)])
 return a,c,labels
class PadicScene(GFScene):
 data=DATA
 def update_caption(self,mob,dt=0):
  now=self.offset+self.time;index=bisect_right([r['start'] for r in self.data['sentences']],now+1e-7)-1
  if index==self.caption_index:return
  self.caption_index=index;words=self.data['sentences'][index]['text'].split();lines=[];line=''
  for word in words:
   if line and len(line)+len(word)+1>26:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  lines.append(line)
  cap=Text('\n'.join(lines),font='Malgun Gothic',font_size=30,color=INK,line_spacing=1.1)
  if cap.width>7.2:cap.scale_to_fit_width(7.2)
  if cap.height>1.9:cap.scale_to_fit_height(1.9)
  cap.move_to([-.2,-5.95,0]);assert cap.get_top()[1]<-4.95 and cap.get_bottom()[1]>-6.95
  self.caption_records.append(dict(sentence=index+1,at=round(now,6),lines=len(lines),width=cap.width,height=cap.height,left=cap.get_left()[0],right=cap.get_right()[0],bottom=cap.get_bottom()[1],top=cap.get_top()[1]))
  mob.become(cap).set_z_index(40)
 def setup(self):
  super().setup();self.caption_panel.stretch_to_fit_height(2.3).move_to([0,-5.95,0]);self.remove(self.header)
  self.header=VGroup(txt('NUMBER THEORY  /  p-ADIC NUMBERS',7.15,17,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.3));self.add(self.header)
 def construct(self):
  super().construct()
  keep=[self.caption,self.caption_panel]
  for m in self.mobjects:
   if m in keep or not m.width or not m.height:continue
   assert m.get_bottom()[1]>=-4.65,(self.shot,m)
class Shot01(PadicScene):
 shot=0
 def s01(self):
  line=NumberLine(x_range=[-3,3,1],length=6.7,include_numbers=True,font_size=23).move_to([0,2.5,0]);self.show(line,eq(r'\mathbb R',4.3,76,BLUE))
  self.show(Dot(line.n2p(-1),color=BLUE),Dot(line.n2p(2),color=BLUE),eq(r'|x-y|',1,53,BLUE));self.to(5)
  self.show(eq(r'\mathbb Q_p',-.8,85,GREEN),rings(-2.8,.7),run_time=.7);self.to(8)
  self.show(txt('왜 새로운 거리와 수 체계가 필요할까?',.1,33,GOLD));self.to(12)
  self.clear();self.show(node(r'\mathrm{Local}',-1.9,2.3,GOLD,3,1.3,50),node(r'\mathrm{Global}',1.9,2.3,PURPLE,3,1.3,50),txt('특정 지점의 주변',.4,30,GOLD,x=-1.9,width=3.4),txt('대상 전체의 성질',.4,30,PURPLE,x=1.9,width=3.4));self.to(17)
class Shot02(PadicScene):
 shot=1
 def s02(self):
  a,c,l=graph();self.show(a,c,l);self.to(20)
  f=VGroup(eq(r'f(x)=-18+21x-26x^2',size=43),eq(r'+22x^3-8x^4+x^5',size=43)).arrange(DOWN,buff=.2).move_to([0,4.2,0]);self.show(f);self.to(25)
  dot=Dot(a.c2p(0,-18),color=GOLD);self.show(dot,eq('f(0)=-18',-2.6,43,GOLD),eq(r'f(x)=\sum_{k=0}^5 a_k(x-0)^k',-3.9,44));self.to(30)
class Shot03(PadicScene):
 shot=2
 def s03(self):
  a,c,l=graph();self.show(a,c,l,eq(r'f(x)=-18+21x-26x^2+22x^3-8x^4+x^5',4.5,34))
  center=ValueTracker(0);marker=always_redraw(lambda:DashedLine(a.c2p(center.get_value(),-25),a.c2p(center.get_value(),65),color=GOLD));self.add(marker)
  self.play(center.animate.set_value(3),run_time=1.6);self.to(34)
  self.show(eq('h=x-3',-2.6,60,GOLD),eq(r'f(3+h)=10h^2+16h^3+7h^4+h^5',-3.9,42));self.to(39)
  marker.clear_updaters();self.clear()
  cards=VGroup(*[node(str(v),0,0,MUTED if k<2 else GOLD if k==2 else BLUE,.94,1.1,42).add(eq('h^'+str(k),-.8,28,MUTED)) for k,v in enumerate([0,0,10,16,7,1])]).arrange(RIGHT,buff=.18).move_to([0,2.1,0]);self.show(cards)
  self.play(*[Create(Cross(cards[k],stroke_color=MUTED,stroke_width=2)) for k in [0,1]],run_time=.7);self.show(eq(r'f(3+h)=h^2(10+16h+7h^2+h^3)',-.3,48));self.to(44)
  self.show(txt('상수항과 일차항은 0 · 이차항 계수는 10',-1.8,29,GOLD),eq(r'f(3)=f\prime(3)=0,\quad f\prime\prime(3)=20\ne0',-3.4,40),txt('3은 정확히 이중근',4.7,33,GOLD));self.to(48)
class Shot04(PadicScene):
 shot=3
 def s04(self):
  self.show(eq(r't=\frac{x-3}{r},\qquad y=\frac{f(3+rt)}{10r^2}',4.5,42))
  a=Axes(x_range=[-1,1,.5],y_range=[-.1,3.6,1],x_length=6.7,y_length=3.9,tips=False,axis_config=dict(color=MUTED,stroke_width=1.3)).move_to([0,.2,0]);self.show(a)
  r=ValueTracker(1);curve=always_redraw(lambda:a.plot(lambda t:shifted(r.get_value()*t)/(10*r.get_value()**2),x_range=[-1,1,.02],color=BLUE));q=a.plot(lambda t:t*t,x_range=[-1,1,.02],color=GOLD,stroke_width=2)
  self.add(curve);self.show(DashedVMobject(q,num_dashes=30),eq('r=',3.3,35,GOLD,x=-.5))
  value=DecimalNumber(1,num_decimal_places=2,font_size=35,color=GOLD).move_to([.4,3.3,0]);value.add_updater(lambda m:m.set_value(r.get_value()));self.add(value)
  self.play(r.animate.set_value(.1),run_time=2);self.to(54)
  self.play(r.animate.set_value(.01),run_time=1.5);self.show(eq(r'\frac{f(3+rt)}{10r^2}=t^2+\frac85rt^3+\frac7{10}r^2t^4+\frac1{10}r^3t^5',-2.9,37),txt('같은 범위로 확대할수록 고차항의 상대 영향은 감소',-4.1,25,GOLD));self.to(59);curve.clear_updaters();value.clear_updaters()
class Shot05(PadicScene):
 shot=4
 def s05(self):
  self.show(txt('LOCAL  /  x=3 주변',4.8,27,GOLD),eq(r'f(x)=10(x-3)^2+\cdots',3.6,58,GOLD))
  fact=eq(r'f(x)=(x-2)(x-3)^2(x^2+1)',1.8,51,PURPLE);self.show(fact)
  a=Axes(x_range=[-.5,3.6,1],y_range=[-1.3,1.3,1],x_length=6.3,y_length=2.2,tips=False,axis_config=dict(color=MUTED,stroke_width=1.2)).move_to([0,-1.3,0]);self.show(a,txt('GLOBAL  /  모든 근',.5,27,PURPLE))
  for x,y,label in [(2,0,'2'),(3,0,'3'),(0,1,'i'),(0,-1,'-i')]:
   pt=a.c2p(x,y);self.show(Dot(pt,color=PURPLE),eq(label,size=28,color=PURPLE).move_to(pt+[.25,.3,0]),run_time=.2)
  self.show(Circle(radius=.17,color=PURPLE).move_to(a.c2p(3,0)),txt('3은 중근',-3.1,25,PURPLE));self.to(66)
  self.show(txt('한 지점의 주변 ↔ 대상 전체',-4.1,33));self.to(74)
class Shot06(PadicScene):
 shot=5
 def s06(self):
  self.show(eq(r'f(x)=(x-3)^k g(x),\quad g(3)\ne0',3.7,49),txt('함수에서: 특정 인수의 거듭제곱',2.3,30,GOLD));self.to(79)
  self.show(VGroup(node('x-3',-2,0,GOLD,2.7,1.2,61),eq(r'\longrightarrow',size=54),node('p',2,0,GREEN,2.7,1.2,67)),txt('유추  /  Analogy',-1.3,26,MUTED));self.to(85)
  self.show(eq(r'n=p^k m,\quad p\nmid m',-2.5,55,GREEN),eq(r'72=2^3\cdot3^2',-3.8,48),txt('수론에서: 소수의 거듭제곱',4.8,30,GREEN));self.to(93)
class Shot07(PadicScene):
 shot=6
 def s07(self):
  line=NumberLine(x_range=[0,130,25],length=7,include_numbers=True,font_size=22).move_to([0,1.8,0]);self.show(line,eq(r'1\qquad126',4.2,77))
  pts=[Dot(line.n2p(n),color=GOLD if n==1 else GREEN,radius=.1) for n in [1,126]];self.show(*pts);self.to(96)
  self.show(BraceBetweenPoints(line.n2p(1)+UP*.35,line.n2p(126)+UP*.35,direction=UP,color=BLUE),eq('|126-1|=125',-.3,70,BLUE));self.to(100)
  self.show(eq('126-1=125=5^3',-2.6,69,GREEN));self.to(103)
class Shot08(PadicScene):
 shot=7
 def s08(self):
  root=node(r'1,126',0,4.3,GREEN,2.4,.8,39);self.show(root,txt('mod 5：둘 다 나머지 1',3.4,28,GREEN));self.to(107)
  previous=root
  for level,(values,y,mod) in enumerate([([1,6,11,16,21],2.25,25),([1,26,51,76,101],.3,125),([1,126,251,376,501],-1.65,625)]):
   nodes=VGroup(*[node(str(v),x,y,GOLD if level==2 and v==1 else GREEN if (j==0 or level==2 and v==126) else MUTED) for j,(x,v) in enumerate(zip([-2.8,-1.4,0,1.4,2.8],values))])
   lines=VGroup(*[Line(previous.get_bottom(),n.get_top(),color=GREEN if j==0 else MUTED,stroke_width=1.3,stroke_opacity=.6) for j,n in enumerate(nodes)])
   self.show(lines,nodes,txt('mod '+str(mod),y+.65,24,GREEN,x=-3.3,width=1.4),run_time=.7)
   previous=nodes[0]
   if level==0:self.to(110)
   elif level==1:self.show(eq(r'1\equiv126\pmod{125}',-3.5,49,GREEN));self.to(114)
   else:self.show(txt('mod 625에서는 1과 126으로 분리',-2.9,29,GOLD));self.to(118)
  self.clear();self.show(rings(.5,1.05),eq(r'5\;\to\;25\;\to\;125\;\to\;625',4.1,48,GREEN),txt('같은 나머지 집합을 더 세밀하게 나눈다',-2.2,29));self.to(125)
  self.show(txt('더 늦게 구별되는 수일수록 더 가깝다',-3.7,32,GOLD),txt('중첩된 p진 근방의 개념도',3.1,24,MUTED));self.to(132)
class Shot09(PadicScene):
 shot=8
 def s09(self):
  self.show(eq(r'1\equiv126\pmod{5^3}',4.3,57,GREEN),eq(r'126-1=5^3',2.9,67));self.to(137)
  pair=VGroup(node('3',-1.9,.8,GOLD,2.3,1.3,80),eq(r'\longrightarrow',.8,55),node('5^{-3}',1.9,.8,GREEN,2.3,1.3,66));self.show(pair,txt('차수',-.5,29,GOLD,x=-1.9),txt('5진 거리',-.5,29,GREEN,x=1.9));self.to(141)
  self.show(eq(r'd_5(1,126)=5^{-3}=\frac1{125}',-1.8,59,GREEN));self.to(144)
  self.show(eq(r'd_p(a,b)=p^{-v_p(a-b)}\;(a\ne b),\quad d_p(a,a)=0',-3.5,39),txt('차이에 포함된 소수 p의 차수가 높을수록 가까움',-4.4,23,MUTED));self.to(147)
class Shot10(PadicScene):
 shot=9
 def s10(self):
  self.show(eq(r'\mathbb Q',4.3,99));self.to(149)
  self.show(eq(r'|x-y|',2.4,58,BLUE,x=-2),eq(r'|x-y|_p',2.4,58,GREEN,x=2),Line([0,3.5,0],[-2,3,0],color=BLUE),Line([0,3.5,0],[2,3,0],color=GREEN));self.to(151)
  self.show(txt('완비화',.7,34,MUTED),Arrow([-2,1.6,0],[-2,-.4,0],color=BLUE),eq(r'\mathbb R',-1.5,106,BLUE,x=-2));self.to(154)
  self.show(Arrow([2,1.6,0],[2,-.4,0],color=GREEN),eq(r'\mathbb Q_p',-1.5,99,GREEN,x=2),txt('같은 유리수 · 다른 거리 · 다른 수렴',-3.6,31));self.to(158)
class Shot11(PadicScene):
 shot=10
 def s11(self):
  self.show(eq(r'\mathbb Q',4.3,92))
  groups=VGroup()
  for x,p in zip([-3,-1.5,0,1.5,3],[2,3,5,7,11]):
   groups.add(VGroup(Line([0,3.4,0],[x,2.4,0],color=GREEN,stroke_opacity=.5),node(str(p),x,1.8,GREEN,1,.8,38),Line([x,1.4,0],[x,.5,0],color=GREEN),node(r'\mathbb Q_{'+str(p)+'}',x,-.2,GREEN,1.3,1,43)))
  self.play(LaggedStart(*[FadeIn(g) for g in groups],lag_ratio=.15),run_time=1.5)
  self.show(txt('각각의 소수, 서로 다른 국소적 세계',-2.7,34,GREEN),eq(r'p=2,3,5,7,11,\ldots',-4,39));self.to(163)
class Shot12(PadicScene):
 shot=11
 def s12(self):
  self.show(eq(r'F(x_1,\ldots,x_n)=0',4.4,55),txt('유리수 해의 존재?',3.2,34,PURPLE))
  local=VGroup(*[node(s,x,1,PURPLE if i==0 else GREEN,1.5,1,50) for i,(x,s) in enumerate(zip([-2.8,-.95,.95,2.8],[r'\mathbb R',r'\mathbb Q_2',r'\mathbb Q_3',r'\cdots']))]);self.show(local,run_time=.6)
  self.show(txt('실수체와 모든 p진수체에서 살펴보기',-.3,29,MUTED),Arrow([0,-.8,0],[0,-1.7,0],color=PURPLE),txt('대역적 해의 존재성과 연결',-2.3,33,PURPLE),run_time=.6);self.to(168)
  self.show(txt('특정한 종류의 방정식에서 성립',-3.4,29,GOLD),txt('대표 사례: 하세–민코프스키 정리 (이차형식)',-4.3,23,MUTED),run_time=.5);self.to(171)
class Shot13(PadicScene):
 shot=12
 def s13(self):
  self.show(eq(r'(x-a)^k',4,82,GOLD),txt('함수에서의 국소적 관찰',2.6,32,BLUE),eq(r'\Downarrow\quad\text{Analogy}',1.2,48,MUTED),eq(r'p^k',-.2,87,GREEN),txt('소수를 기준으로 수를 관찰',-1.6,32,GREEN))
  self.show(eq(r'\mathbb Q_p',-3,79,GREEN),txt('Local ↔ Global',-4.3,29,PURPLE));self.to(178)
