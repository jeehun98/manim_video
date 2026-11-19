"""DFT symmetry to radix-2 butterflies; 177-second portrait short."""
import sys,json
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
sys.path.insert(0,str(HERE))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene
from episodes.detperm01_permutation_sign.scene import txt,eq,BLUE,GREEN,GOLD,PURPLE,RED,INK,MUTED
from model import signal,SAMPLES,dft,fft_stages,pairs,ORDER
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
OUTPUT=dft(SAMPLES)

def box(tex,x,y,color=BLUE,width=2.4,height=.95,size=34):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.12,color=color,fill_color=color,fill_opacity=.09),eq(tex,size=size,color=color,width=width-.25)).move_to([x,y,0])
def sample_cards(indices,y=0,x=0,scale=1):
 return VGroup(*[box('x_'+str(i),0,0,BLUE if i%2==0 else GOLD,.72,.75,27) for i in indices]).arrange(RIGHT,buff=.12).scale(scale).move_to([x,y,0])
def spectrum(x=0,y=0,width=3,height=1.1):
 g=VGroup(Line([x-width/2,y,0],[x+width/2,y,0],color=MUTED,stroke_width=1))
 for k,v in enumerate(abs(OUTPUT)):
  h=max(float(v)/4*height,.015);g.add(Rectangle(width=width/11,height=h,fill_color=GREEN,fill_opacity=.9,stroke_width=0).move_to([x-width/2+(k+.5)*width/8,y+h/2,0]))
 return g

class DFTNetwork(VGroup):
 def __init__(self,x=0,y=0,width=5.4,height=4.9,labels=True):
  super().__init__();self.left=[];self.right=[];self.edges=[]
  for i in range(8):
   self.left.append(np.array([x-width/2,y+height/2-i*height/7,0]));self.right.append(np.array([x+width/2,y+height/2-i*height/7,0]))
  for k in range(8):
   row=VGroup(*[Line(a,self.right[k],color=MUTED,stroke_width=1,stroke_opacity=.16) for a in self.left]);self.edges.append(row);self.add(row)
  self.add(*[Dot(p,radius=.065,color=BLUE) for p in self.left],*[Dot(p,radius=.065,color=GREEN) for p in self.right])
  if labels:
   self.add(*[eq('x_'+str(i),p[1],23,BLUE,x=p[0]-.45,width=.65) for i,p in enumerate(self.left)],*[eq('X_'+str(i),p[1],23,GREEN,x=p[0]+.45,width=.65) for i,p in enumerate(self.right)])

class FFTNetwork(VGroup):
 def __init__(self,x=0,y=.25,width=5.7,height=4.8,labels=True):
  super().__init__();self.positions=[[np.array([x-width/2+c*width/3,y+height/2-r*height/7,0]) for r in range(8)] for c in range(4)];self.wires=[];self.columns=[]
  for stage in range(3):
   wires=VGroup()
   for i,j,w in pairs(8,stage):
    for a,b in [(i,i),(i,j),(j,i),(j,j)]:wires.add(Line(self.positions[stage][a],self.positions[stage+1][b],color=PURPLE,stroke_width=1.6,stroke_opacity=.5))
   self.wires.append(wires);self.add(wires)
  for c in range(4):
   col=VGroup(*[Dot(p,radius=.055,color=GREEN if c==3 else BLUE) for p in self.positions[c]]);self.columns.append(col);self.add(col)
  if labels:
   self.add(*[eq('x_'+str(ORDER[r]),p[1],21,BLUE if ORDER[r]%2==0 else GOLD,x=p[0]-.43,width=.6) for r,p in enumerate(self.positions[0])],*[eq('X_'+str(r),p[1],21,GREEN,x=p[0]+.43,width=.6) for r,p in enumerate(self.positions[3])])

class RootCircle(VGroup):
 def __init__(self,n=8,x=0,y=.3,radius=1.8):
  super().__init__();self.origin=np.array([x,y,0.]);self.root_points=[];self.dots=VGroup();self.names=VGroup()
  self.add(Circle(radius=radius,color=MUTED,stroke_opacity=.5).move_to(self.origin),Line(self.origin+[-radius,0,0],self.origin+[radius,0,0],color=MUTED,stroke_opacity=.3),Line(self.origin+[0,-radius,0],self.origin+[0,radius,0],color=MUTED,stroke_opacity=.3))
  for k in range(n):
   z=np.exp(-2j*np.pi*k/n);p=self.origin+radius*np.array([z.real,z.imag,0]);self.root_points.append(p);self.dots.add(Dot(p,radius=.075,color=PURPLE))
   name=eq(f'W_{{{n}}}^{{{k}}}',size=24 if radius>1.5 else 20,color=PURPLE,width=.9).move_to(self.origin+(radius+.43)*np.array([z.real,z.imag,0]));self.names.add(name)
  self.add(self.dots,self.names)

class ButterflyUnit(VGroup):
 def __init__(self):
  super().__init__();e=np.array([-3,1.6,0]);o=np.array([-3,-1.2,0]);t=np.array([-1.3,-1.2,0]);p=np.array([2,1.6,0]);m=np.array([2,-1.2,0])
  self.wire=VGroup(Line(e,p,color=BLUE),Line(e,m,color=BLUE),Line(o,t,color=GOLD),Line(t,p,color=GOLD),Line(t,m,color=GOLD))
  self.add(self.wire,Dot(e,color=BLUE),Dot(o,color=GOLD),box('W_N^k',-1.8,-1.2,PURPLE,1.1,.7,25),Circle(radius=.3,color=GREEN).move_to(p),Circle(radius=.3,color=GREEN).move_to(m),eq('+',1.6,37,GREEN,x=2,width=.5),eq('-',-1.2,37,GREEN,x=2,width=.5),Line(p+[.3,0,0],[3.1,1.6,0],color=GREEN),Line(m+[.3,0,0],[3.1,-1.2,0],color=GREEN),eq('E_k',2.3,35,BLUE,x=-3,width=1),eq('O_k',-1.9,35,GOLD,x=-3,width=1),eq('X_k',2.3,33,GREEN,x=2.8,width=1.2),eq('X_{k+N/2}',-1.9,30,GREEN,x=2.5,width=2.4))

class FFTScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel]
  self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*6.1)
  self.header=VGroup(txt('SIGNAL PROCESSING  /  RADIX-2 FFT',7.2,16,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.25),txt('같은 입력 · 같은 DFT · 적은 계산',5.05,28,BLUE));self.add(self.header)
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.header];obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def comparison(self):
  a=DFTNetwork(-2,1,width=2,height=3.4,labels=False);b=FFTNetwork(2,1,width=2.7,height=3.4,labels=False)
  self.show(a,b,txt('Direct DFT',3.5,30,GOLD,x=-2,width=3.5),txt('FFT',3.5,30,BLUE,x=2,width=3.5),eq('O(N^2)',-1.5,35,GOLD,x=-2,width=3.5),eq(r'O(N\log N)',-1.5,35,GREEN,x=2,width=3.5))
  return a,b

class Shot01(FFTScene):
 shot=0
 def s01(self):
  curve=VMobject(color=BLUE).set_points_smoothly([[-3.4+6.8*t/8,3.2+.4*float(signal(t)),0] for t in np.linspace(0,8,100)])
  self.show(curve,box('DFT',-2,1,GOLD),box('FFT',2,1,BLUE),spectrum(-2,-1.6),spectrum(2,-1.6),eq('=',-1,45,GREEN),txt('비정규화 스펙트럼 |X[k]| · k=0…7',-3.5,24,MUTED));self.to(3)
  self.show(txt('Same mathematical result',-.25,31,GREEN),run_time=.4);self.to(7)
  self.clear_body();self.comparison();self.show(txt('변환의 정의는 같고 계산 경로가 다르다',-3.5,32));self.to(12)

class Shot02(FFTScene):
 shot=1
 def s02(self):
  axes=Line([-3.3,1.6,0],[3.3,1.6,0],color=MUTED,stroke_opacity=.5)
  curve=VMobject(color=MUTED).set_points_smoothly([[-3.15+.9*t,1.6+.8*float(signal(t)),0] for t in np.linspace(0,7,120)])
  dots=VGroup(*[VGroup(Line([-3.15+.9*i,1.6,0],[-3.15+.9*i,1.6+.8*v,0],color=BLUE,stroke_width=2),Dot([-3.15+.9*i,1.6+.8*v,0],color=BLUE),eq('x_'+str(i),.1,23,BLUE,x=-3.15+.9*i,width=.7)) for i,v in enumerate(SAMPLES)])
  self.show(axes,curve);self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.1),run_time=1.2);self.to(16)
  self.show(eq(r'X_k=\sum_{n=0}^{7}x_n e^{-2\pi i kn/8}',-1.5,40),txt('입력 × 회전 인자를 모두 더한다',-3.6,30,PURPLE));self.to(23)
  self.clear_body();g=DFTNetwork(y=.6,height=4.7);self.show(g,run_time=.4)
  for k in range(4):self.play(Indicate(g.edges[k],color=BLUE,scale_factor=1),run_time=.8)
  self.show(txt('각 출력에 8개 입력 · 출력도 8개',-3.4,31));self.to(30)
  self.clear_body();cells=VGroup(*[Square(side_length=.49,fill_color=BLUE,fill_opacity=.12+.06*((i+j)%4),stroke_color=BLUE,stroke_opacity=.4).move_to([(j-3.5)*.59,2.9-i*.59,0]) for i in range(8) for j in range(8)])
  self.show(cells,txt('8개 입력 × 8개 주파수 bin',4,28),eq(r'8\times8=64',-2.5,43,GOLD),eq('O(N^2)',-3.55,46,GOLD),txt('64는 곱 항의 수 · 전체 연산 수 아님',-4.45,22,MUTED),run_time=.4);self.to(36)

class Shot03(FFTScene):
 shot=2
 def s03(self):
  self.show(eq(r'W_N=e^{-2\pi i/N}',2.5,54,PURPLE),eq(r'X_k=\sum_{n=0}^{N-1}x_nW_N^{kn}',.3,43),txt('많은 인자들이 같은 수의 거듭제곱',-2.7,33));self.to(40)
  self.clear_body();r=RootCircle();r.dots.set_opacity(0);r.names.set_opacity(0);self.add(r)
  arrow=Arrow(r.origin,r.root_points[0],buff=0,color=PURPLE);self.show(arrow,eq(r'e^{-i\theta}=\cos\theta-i\sin\theta',3.7,34,PURPLE),txt('음의 지수 → 시계 방향 회전',-3.4,30));self.play(Rotate(arrow,angle=-PI/4,about_point=r.origin),run_time=1.5);self.to(45)
  self.play(FadeOut(arrow),run_time=.2)
  for k in range(8):self.play(r.dots[k].animate.set_opacity(1),r.names[k].animate.set_opacity(1),run_time=.3)
  self.to(49);self.clear_body();a=RootCircle(8,-1.95,.2,1.1);b=RootCircle(4,1.95,.2,1.1)
  for k in range(8):
   a.dots[k].set_color(BLUE if k%2==0 else MUTED).set_opacity(1 if k%2==0 else .2);a.names[k].set_color(BLUE if k%2==0 else MUTED).set_opacity(1 if k%2==0 else .2)
  b.dots.set_color(BLUE);b.names.set_color(BLUE);self.show(a,b,eq(r'W_8^{2k}=W_4^k',3.2,45,BLUE),txt('짝수 지수의 네 점은 같은 위치',-2.8,30),run_time=.4)
  self.play(*[TransformFromCopy(a.dots[2*k],b.dots[k]) for k in range(4)],run_time=1.2);self.to(55)
  self.clear_body();r=RootCircle();self.show(r,eq(r'W_8^{k+4}=-W_8^k',3.7,43,PURPLE),run_time=.4)
  u=Arrow(r.origin,r.root_points[1],buff=0,color=BLUE);v=Arrow(r.origin,r.root_points[5],buff=0,color=GOLD);self.show(u);self.play(Rotate(u.copy(),angle=-PI,about_point=r.origin),run_time=1.3);self.show(v,txt('절댓값 1 · 반 바퀴 차이 · 반대 부호',-3.4,28));self.to(60)
  self.clear_body();self.show(txt('작은 DFT로 분할',3.4,35,BLUE),eq(r'W_N^{2k}=W_{N/2}^k',2,49,BLUE),txt('반대편 출력에서 재사용',-.1,35,PURPLE),eq(r'W_N^{k+N/2}=-W_N^k',-1.6,45,PURPLE),txt('N은 2의 거듭제곱인 예시',-4,24,MUTED),run_time=.4);self.to(64)

class Shot04(FFTScene):
 shot=3
 def s04(self):
  g=sample_cards(range(8),2.9);self.show(g,txt('0부터 시작하는 입력 인덱스',4,28,MUTED),run_time=.4)
  targets={i:np.array([(-1.5+q)*1.0,1 if i%2==0 else -.6,0]) for parity in [0,1] for q,i in enumerate(range(parity,8,2))}
  self.play(*[g[i].animate.move_to(targets[i]) for i in range(8)],run_time=1.4);self.show(txt('Even: 0, 2, 4, 6',2,28,BLUE),txt('Odd: 1, 3, 5, 7',-1.6,28,GOLD),txt('데이터 값이 아닌 인덱스의 홀짝',-3.5,30));self.to(69)
  self.clear_body();self.show(box(r'E_k=\mathrm{DFT}_4(x_0,x_2,x_4,x_6)',0,2.6,BLUE,7,1.1,35),box(r'O_k=\mathrm{DFT}_4(x_1,x_3,x_5,x_7)',0,.6,GOLD,7,1.1,35),eq(r'X_k=E_k+W_8^kO_k',-1.7,47,GREEN),eq(r'0\le k<4',-3.1,29,MUTED),run_time=.4);self.to(76)
  self.show(txt('두 개의 4점 결과로 8개 출력은 어떻게?',-4.3,28,PURPLE),run_time=.3);self.to(80)

class Shot05(FFTScene):
 shot=4
 def s05(self):
  e=box('E_1=3',-1.9,2.8,BLUE,2.8,1.1);t=box('T=W_8O_1=1',1.8,2.8,GOLD,3.2,1.1,31)
  self.show(e,t,eq(r'T=W_8O_1\quad\text{(once)}',.8,37,PURPLE),txt('k=1 · 같은 두 중간값을 보관',-3.5,30));self.to(86)
  plus=eq(r'X_1=E_1+T=4',-.5,47,GREEN);self.play(TransformFromCopy(VGroup(e,t),plus),run_time=.8);self.to(90)
  minus=eq(r'X_5=E_1-T=2',-2,47,GREEN);self.play(TransformFromCopy(VGroup(e,t),minus),run_time=.8);self.to(95)
  self.clear_body();self.show(eq(r'k=1\longrightarrow5=1+8/2',3.9,37,PURPLE),txt('입력 n',3,23,MUTED,x=-2.85,width=1.3),txt('k = 1',3,23,MUTED,x=-.9,width=1.3),txt('k = 5',3,23,MUTED,x=1,width=1.3),txt('변화',3,23,MUTED,x=2.8,width=1.2),run_time=.4)
  rows=[]
  for n in range(8):
   y=2.25-n*.57;c=BLUE if n%2==0 else GOLD
   row=VGroup(eq('x_'+str(n),y,26,c,x=-2.85,width=.7),eq(f'W_8^{{{n}}}',y,26,c,x=-.9,width=1),eq(f'W_8^{{{(5*n)%8}}}',y,26,c,x=1,width=1),txt('유지' if n%2==0 else '반전',y,23,c,x=2.8,width=1.3));rows.append(row)
  for parity in [0,1]:self.play(LaggedStart(*[FadeIn(rows[n]) for n in range(parity,8,2)],lag_ratio=.15),run_time=1.2)
  self.show(eq(r'W_N^{(k+N/2)n}=W_N^{kn}(-1)^n',-3.25,33,PURPLE),txt('지수는 mod 8 · 짝수 항 +1 / 홀수 항 −1',-4.3,25,MUTED));self.to(106)
  self.clear_body();self.show(e.copy(),t.copy(),eq(r'X_1=E_1+T=4',.4,49,GREEN),eq(r'X_5=E_1-T=2',-1.3,49,GREEN),txt('곱셈 T는 한 번 · 덧셈과 뺄셈에서 공유',-3.5,30));self.to(112)
  self.show(txt('대칭성 → 중간 결과의 재사용',-4.4,29,PURPLE),run_time=.4);self.to(117)

class Shot06(FFTScene):
 shot=5
 def s06(self):
  b=ButterflyUnit();self.show(b,run_time=.6)
  self.play(ShowPassingFlash(b.wire.copy().set_color(GREEN),time_width=.5),run_time=1.5)
  self.show(eq(r'X_k=E_k+W_N^kO_k',-3.1,37,GREEN),eq(r'X_{k+N/2}=E_k-W_N^kO_k',-4.05,35,GREEN),txt('0 ≤ k < N/2',3.7,25,MUTED));self.to(122)
  self.show(txt('Butterfly Operation',2.95,35,PURPLE),run_time=.4);self.to(125)

class Shot07(FFTScene):
 shot=6
 def s07(self):
  root=box(r'8\mathrm{-DFT}',0,3.7,BLUE,1.8,.8,30);a=box(r'4\mathrm{-DFT}',-1.9,2,BLUE,1.8,.8,30);b=box(r'4\mathrm{-DFT}',1.9,2,GOLD,1.8,.8,30)
  self.show(root,a,b,Line(root.get_bottom(),a.get_top(),color=PURPLE),Line(root.get_bottom(),b.get_top(),color=PURPLE),run_time=.4);self.to(128)
  nodes=[]
  for q,x in enumerate([-2.85,-.95,.95,2.85]):
   node=box(r'2\mathrm{-DFT}',x,.15,BLUE if q<2 else GOLD,1.45,.8,26);nodes.append(node);parent=a if q<2 else b;self.show(node,Line(parent.get_bottom(),node.get_top(),color=PURPLE),run_time=.3)
  for q,i in enumerate(ORDER):
   leaf=box('x_'+str(i),-3.15+.9*q,-1.8,BLUE if i%2==0 else GOLD,.72,.7,25);self.show(leaf,Line(nodes[q//2].get_bottom(),leaf.get_top(),color=PURPLE),run_time=.2)
  self.show(eq(r'8\to4\to2\to1',-3.5,41,PURPLE),txt('인덱스를 반복해서 짝수·홀수로 분할',-4.4,25,MUTED),run_time=.4);self.to(134)
  self.clear_body();g=FFTNetwork();self.add(g)
  for c in g.wires:c.set_opacity(.12)
  for c in g.columns[1:]:c.set_opacity(.2)
  self.show(txt('입력 순서: 0, 4, 2, 6, 1, 5, 3, 7',3.85,25,MUTED),txt('회전 인자와 +/− 생략 · 선은 계산 의존 관계',-3.4,23,MUTED),run_time=.3)
  for stage in range(3):self.play(g.wires[stage].animate.set_opacity(.8),g.columns[stage+1].animate.set_opacity(1),run_time=.7)
  self.show(txt('2점 결과 → 4점 결과 → 8점 결과',-4.35,28,GREEN),run_time=.3);self.to(139)

class Shot08(FFTScene):
 shot=7
 def s08(self):
  self.show(eq(r'8=2^3\quad\Rightarrow\quad\log_2 8=3',3.6,38,PURPLE),txt('8 → 16 → 32 → 64개 입력',1.9,31),txt('3 → 4 → 5 → 6단계',.6,33,PURPLE),eq(r'\log_2 N\ \mathrm{stages}',-1.5,45,PURPLE));self.to(144)
  self.clear_body();self.show(eq(r'N/2\ \mathrm{butterflies\ per\ stage}',3.6,31,BLUE),txt('8점: 매 단계 4개 버터플라이',2.3,30,BLUE),txt('각 버터플라이: 곱 1회 + 덧셈·뺄셈 2회',.8,27),eq(r'O(N)\times O(\log N)',-1,45),eq(r'=O(N\log N)',-2.5,53,GREEN),txt('특수 회전 인자의 곱은 단순화 가능',-4.1,23,MUTED),run_time=.4);self.to(151)
  self.clear_body();axes=Axes(x_range=[0,64,16],y_range=[0,4096,1024],x_length=6.3,y_length=4.3,tips=False,axis_config={'include_numbers':False}).move_to([0,.6,0]);self.show(axes,txt('연산량 증가율 척도 · 실측 시간 아님',3.8,26,MUTED),run_time=.3)
  self.play(Create(axes.plot(lambda n:n*n,x_range=[1,64],color=GOLD)),Create(axes.plot(lambda n:n*np.log2(n),x_range=[1,64],color=GREEN)),run_time=1.7)
  self.show(eq('N^2',2.7,35,GOLD,x=2.65,width=1.5),eq(r'N\log_2 N',-.9,31,GREEN,x=2.2,width=2.5),eq('N',-2,29,MUTED,x=3.4,width=.5),txt('입력 규모가 커질수록 벌어지는 차이',-3.8,30),run_time=.4);self.to(157)

class Shot09(FFTScene):
 shot=8
 def s09(self):
  self.comparison();self.show(spectrum(-2,-3.2,2.7,.9),spectrum(2,-3.2,2.7,.9),eq('=',-2.6,38,GREEN),txt('동일한 |X[k]| · 정규화 없음',-4.3,25,MUTED),run_time=.4);self.to(164)
  self.clear_body();self.show(txt('같은 종류의 복소수 곱셈·덧셈',3.3,34),box(r'\times',-1.8,1,PURPLE,1.6,1.2,55),box('+',1.8,1,BLUE,1.6,1.2,55),txt('Fewer Operations',-1.6,43,GREEN),txt('필요한 연산 자체를 줄인다',-3.7,33));self.to(169)
  self.clear_body();self.show(txt('대칭성과 주기성',3.5,39,PURPLE),txt('↓',2.4,40,MUTED),txt('중간 계산 결과의 재사용',1.15,35,BLUE),txt('↓',-.1,40,MUTED),eq(r'O(N^2)\longrightarrow O(N\log N)',-1.5,41,GREEN),txt('수학적 구조를 이해하면 계산을 줄일 수 있다',-3.9,29));self.to(177)
