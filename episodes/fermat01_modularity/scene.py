"""174-second portrait: Fermat -> Frey -> Ribet and Wiles -> contradiction."""
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
BLUE,GOLD,PURPLE,GREEN,RED,INK,MUTED='#42B8E8','#E8B45D','#A18CF3','#65D6AC','#EF7185','#E8EDF5','#8B9CB7'
FERMAT=r'a^n+b^n=c^n'
FREY=r'E:\ y^2=x(x-a^p)(x+b^p)'
def txt(s,y=0,size=35,color=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=color,width=width)
def eq(s,y=0,size=45,color=INK,width=7.4,x=0):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def elliptic(y=0):
 ax=Axes(x_range=[-1.6,2.5,1],y_range=[-4,4,2],x_length=6,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.3}).move_to(UP*y)
 x0=float(np.roots([1,0,-1,1])[0].real)
 # Real endpoint is selected explicitly instead of assuming root ordering.
 x0=next(float(r.real) for r in np.roots([1,0,-1,1]) if abs(r.imag)<1e-10)
 branches=VGroup(*[ax.plot(lambda x,sg=sg:sg*np.sqrt(max(0,x**3-x+1)),x_range=[x0,2.3,.012],color=GOLD,stroke_width=3) for sg in [1,-1]])
 return VGroup(ax,branches)
def cube(name,x,size=1):
 a=np.array([-.6,-.5,0])*size;b=np.array([.4,-.5,0])*size;c=np.array([.4,.5,0])*size;d=np.array([-.6,.5,0])*size;v=np.array([.35,.3,0])*size
 g=VGroup(Polygon(a,b,c,d,fill_color=BLUE,fill_opacity=.12,stroke_color=BLUE),Polygon(d,c,c+v,d+v,fill_color=BLUE,fill_opacity=.3,stroke_color=BLUE),Polygon(b,b+v,c+v,c,fill_color=BLUE,fill_opacity=.2,stroke_color=BLUE))
 g.move_to([x,.5,0]);return VGroup(g,eq(name,-1,36,BLUE,x=x))
class FermatScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.6)
  self.add(txt('MATHEMATICS  /  FERMAT’S LAST THEOREM',7,17,MUTED))
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]
  obs=[m for m in self.mobjects if m not in keep and m.get_center()[1]<6.5]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
class Shot01(FermatScene):
 shot=0
 def s01(self):
  self.show(txt('아주 단순한 질문',2.1,45),txt('Fermat’s Last Theorem',.6,27,MUTED));self.to(3)
  self.clear_body();a=eq(r'a^3+b^3=c^3\ ?',3.4,61,BLUE);self.show(a,cube('a',-2,1.3),cube('b',1.6,1),eq('+',.5,52,x=-.1),txt('양의 정수 길이 · 부피의 합이라는 질문',-2.8,26,MUTED));self.to(8)
  self.clear_body();self.show(eq(r'a^3+b^3\ne c^3',2.3,63,RED),eq(r'a,b,c\in\mathbb Z_{>0}',.5,43,BLUE),txt('양의 정수 해 없음',-1.5,42,RED));self.to(11)
  self.clear_body();a=eq(r'a^3+b^3=c^3',2.1,57,BLUE);self.show(a,txt('양의 정수 해 없음',-1,39,RED))
  for n in [4,5]:self.play(TransformMatchingTex(a,b:=eq(fr'a^{n}+b^{n}=c^{n}',2.1,57,BLUE)),run_time=1);a=b
  self.to(17);self.clear_body();self.show(eq(FERMAT,2.7,65,BLUE),eq(r'n\in\mathbb Z,\ n\geq3',.9,43),eq(r'a,b,c\in\mathbb Z_{>0}',-.4,44,BLUE),txt('조건을 만족하는 해는 존재하지 않는다',-2.4,34,RED));self.to(26)
  self.show(txt('페르마의 마지막 정리',-3.8,36,GREEN));self.to(28)
class Shot02(FermatScene):
 shot=1
 def s02(self):
  self.show(txt('정수론 · Number Theory',3.8,40,BLUE))
  line=NumberLine(x_range=[-3,5,1],length=7,include_numbers=True,font_size=24).move_to(UP*1.6);self.show(line);self.to(34)
  self.clear_body();self.show(eq(r'2,3,5,7,11,\ldots',3.1,43,BLUE),txt('소수의 분포',2.2,28),eq(r'17=5\cdot3+2',.7,44,GOLD),txt('나눗셈과 나머지',-.2,28),eq(FERMAT,-1.6,44,BLUE),txt('정수 해의 존재',-2.6,28));self.to(41)
  self.clear_body();self.show(eq(r'x^2=2',3.3,58),txt('실수 범위',1.7,31,BLUE,x=-1.9),txt('정수 범위',1.7,31,GOLD,x=1.9),eq(r'x=\pm\sqrt2',.4,43,BLUE,width=3.3,x=-1.9),eq(r'x\in\mathbb Z',.4,43,GOLD,width=3.3,x=1.9),txt('해가 있다',-1.1,31,GREEN,x=-1.9),txt('해가 없다',-1.1,31,RED,x=1.9),txt('어떤 수의 범위에서 해를 찾는가?',-3.3,31));self.to(47)
class Shot03(FermatScene):
 shot=2
 def s03(self):
  self.show(txt('1637년경 · Pierre de Fermat',4.2,31,GOLD))
  page=Rectangle(width=6.8,height=4.6,fill_color='#D2BD92',fill_opacity=.12,stroke_color=GOLD).move_to(UP*.6)
  divider=Line([1.5,-1.7,0],[1.5,2.9,0],color=GOLD,stroke_opacity=.5)
  self.show(page,divider,eq(FERMAT,.9,44,BLUE,width=4.5,x=-.7),txt('증명을\n발견했다',.7,25,GOLD,x=2.4,width=1.5),txt('기록 내용의 요약 · 원문 인용 아님',-2.8,23,MUTED));self.to(55)
  self.clear_body();years=Integer(1637,font_size=76,color=GOLD).move_to(UP*1.5);self.show(years,txt('350년을 넘긴 난제',-1,42));self.play(ChangeDecimalToValue(years,1995),run_time=3,rate_func=linear);self.show(txt('1995 · 완성된 증명 출판',-2.8,27,GREEN));self.to(61)
  self.clear_body();self.show(eq(r'(1,2,3),\ (2,3,4),\ (3,4,5),\ldots',2.6,38,BLUE),txt('모든 정수를 하나씩 확인할 수는 없다',.3,35),txt('문제를 다른 수학적 구조로 옮긴다',-1.8,32,GREEN));self.to(66)
class Shot04(FermatScene):
 shot=3
 def s04(self):
  self.show(txt('가정 · 양의 정수 반례가 있다면?',4.2,31,RED),eq(FERMAT,2.5,57,BLUE),eq(r'(a,b,c)=(?,\ ?,\ ?)',.8,43,BLUE),txt('실제 반례의 값이 아닌 가정',-1.3,28,MUTED));self.to(72)
  self.clear_body();self.show(eq(r'a^p+b^p=c^p',4.3,45,BLUE),txt('p ≥ 5 소수 · 서로소인 반례로 환원',3.35,24,MUTED),eq(r'\Downarrow',2.1,49,GREEN),eq(FREY,.5,43,GOLD),txt('가상의 해로부터 새로운 곡선을 정의',-1.3,30,GOLD),txt('지수 3, 4는 고전적으로 해결된 경우',-3.4,24,MUTED));self.to(78)
  self.clear_body();self.show(eq(FREY,4.25,36,GOLD),txt('타원곡선의 일반적인 예시',3.3,28,MUTED));g=elliptic(.7);self.show(g,eq(r'y^2=x^3-x+1',-1.8,43,GOLD),eq(r'y^2=x^3+Ax+B,\quad4A^3+27B^2\ne0',-3,31),txt('위 그래프는 가상 반례의 프라이 곡선이 아님',-4.2,23,MUTED));self.to(86)
  self.clear_body();self.show(eq(FREY,3,45,GOLD),txt('이 곡선은 어떤 성질을 가질까?',.5,39),txt('가정한 반례에서 만들어진 같은 곡선 E',-1.6,27,MUTED));self.to(89)
class Shot05(FermatScene):
 shot=4
 def s05(self):
  self.show(txt('켄 리베 · Ken Ribet',4.1,35,RED),eq(FREY,2.6,40,GOLD),Arrow([0,1.6,0],[0,-.2,0],color=PURPLE),txt('모듈러 형식',-1.1,40,PURPLE))
  self.show(Cross(stroke_color=RED,stroke_width=6).scale(.25).move_to([0,.7,0]),txt('반례에서 얻은 E는 비모듈러',-2.8,34,RED),txt('레벨 내림 정리와 프라이 곡선의 성질의 귀결',-4.2,22,MUTED));self.to(95)
  self.clear_body();self.show(txt('모듈러 형식 · Modular Form',4.2,34,PURPLE))
  ax=ComplexPlane(x_range=[-2,2,1],y_range=[0,2,1],x_length=5.5,y_length=2.5,background_line_style={'stroke_opacity':.2}).move_to(UP*1.8)
  dot=Dot(ax.c2p(-.5,1),color=PURPLE);self.show(ax,dot,eq(r'\operatorname{Im}z>0',.15,30,PURPLE));self.play(dot.animate.move_to(ax.c2p(.5,1)),run_time=1)
  self.show(eq(r'f\!\left(\frac{\alpha z+\beta}{\gamma z+\delta}\right)=(\gamma z+\delta)^k f(z)',-1.5,34,PURPLE),txt('특정 합동부분군의 변환 규칙',-2.8,27),txt('정칙성 등 해석적 조건도 필요',-4,25,MUTED));self.to(102)
class Shot06(FermatScene):
 shot=5
 def s06(self):
  self.show(txt('타원곡선',4,35,GOLD,x=-1.9),txt('모듈러 형식',4,35,PURPLE,x=1.9))
  g=elliptic().scale(.48).move_to([-1.9,1.4,0]);self.show(g,eq(r'f(z)=\sum_{r=1}^{\infty}a_rq^r',1.6,33,PURPLE,width=3.5,x=1.9),eq(r'q=e^{2\pi iz}',.25,30,PURPLE,width=3.5,x=1.9),txt('소수별 점의 개수',-1.4,25,GOLD,x=-1.9,width=3.5),txt('계수에 담긴 산술 정보',-1.4,25,PURPLE,x=1.9,width=3.5),txt('서로 다른 정의 사이의 모듈러성 추측',-3.3,30));self.to(109)
  self.clear_body();self.show(eq(r'E_0:\ y^2=x^3-x+1',4.1,36,GOLD),txt('일반 곡선 예시 · 좋은 소수 ℓ = 5',3.2,24,MUTED))
  ax=Axes(x_range=[0,5,1],y_range=[0,5,1],x_length=2.8,y_length=2.8,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to([-1.9,.9,0]);self.add(ax)
  pts=[(x,y) for x in range(5) for y in range(5) if (y*y-x**3+x-1)%5==0]
  self.show(*[Dot(ax.c2p(x,y),color=GOLD,radius=.055) for x,y in pts],eq(r'a_5=-2',1.3,45,PURPLE,width=3.3,x=1.9),txt('대응하는 계수',.2,25,PURPLE,x=1.9,width=3.3),txt('유한 점 7개 + 무한원점 1개',-1,23,GOLD,x=-1.9,width=3.5),eq(r'a_\ell=\ell+1-\#E(\mathbb F_\ell)',-2.4,41,GREEN),eq(r'a_5=5+1-8=-2',-3.5,35,GREEN));self.to(115)
  self.clear_body();self.show(txt('앤드루 와일스',2.8,47,GREEN),txt('Andrew Wiles',1.6,30,MUTED),txt('타원곡선의 모듈러성',-.3,39,PURPLE));self.to(118)
class Shot07(FermatScene):
 shot=6
 def s07(self):
  self.show(txt('와일스의 정리',4.2,38,GREEN),txt('유리수 Q 위의 모든 준안정 타원곡선',2.7,32,GOLD),eq(r'\Longrightarrow',1.1,62,GREEN),txt('모듈러이다',-.4,48,PURPLE),txt('1995 · Wiles / Taylor–Wiles',-2.2,25,MUTED));self.to(124)
  self.clear_body();self.show(eq(FREY,4.4,39,GOLD),txt('가정한 반례에서 만든 같은 곡선 E',3.45,24,MUTED),txt('E는 유리수 위의 준안정 타원곡선',2.5,28,GOLD));self.to(129)
  right=VGroup(RoundedRectangle(width=3.4,height=2,corner_radius=.16,color=GREEN),txt('와일스의 정리',.45,28,GREEN),txt('모듈러',-.35,39,GREEN)).move_to([1.95,.4,0])
  self.show(right,Arrow([.8,2,0],[1.95,1.55,0],color=GREEN,buff=.1));self.to(133)
  left=VGroup(RoundedRectangle(width=3.4,height=2,corner_radius=.16,color=RED),txt('리베의 정리 등',.45,28,RED),txt('비모듈러',-.35,39,RED)).move_to([-1.95,.4,0])
  self.show(left,Arrow([-.8,2,0],[-1.95,1.55,0],color=RED,buff=.1));self.to(137)
  self.show(txt('모순',-1.9,60,RED),eq(r'M(E)\land\neg M(E)',-3.25,42,RED));self.to(141)
  self.clear_body();self.show(eq(r'a^p+b^p=c^p',3.5,49,BLUE),txt('양의 정수 반례를 가정',2.4,30,RED),eq(r'\Downarrow',1.3,40),txt('프라이 곡선 E',.2,37,GOLD),eq(r'\Downarrow',-.9,40),txt('모순',-2,44,RED),txt('따라서 처음 가정한 반례는 존재하지 않는다',-3.6,30,GREEN));self.to(146)
class Shot08(FermatScene):
 shot=7
 def s08(self):
  self.show(eq(FERMAT,3,58,BLUE),eq(r'n\in\mathbb Z,\ n\geq3,\quad a,b,c\in\mathbb Z_{>0}',1.4,33),txt('양의 정수 해 없음',-.7,45,GREEN));self.to(149)
  self.show(txt('하나씩 대입하는 계산을 넘어',-2.7,34));self.to(154)
  self.clear_body();self.show(txt('정수 방정식',3.7,42,BLUE),eq(r'\Downarrow',2.4,42),txt('타원곡선',1,42,GOLD),eq(r'\Updownarrow',-.4,49),txt('모듈러 형식',-1.9,42,PURPLE),txt('서로 다른 구조를 연결한다',-3.7,32,GREEN));self.to(161)
class Shot09(FermatScene):
 shot=8
 def s09(self):
  self.show(eq(FREY,3.7,39,GOLD),txt('모듈러',1.7,42,GREEN,x=-1.9),txt('비모듈러',1.7,42,RED,x=1.9),txt('양립할 수 없는 성질 → 모순',-.3,36,RED));self.to(165)
  self.clear_body();self.show(eq(FERMAT,3.9,56,BLUE),txt('정수 방정식에서 출발해',2.4,33),txt('타원곡선  ↔  모듈러 형식',.4,35,GOLD),txt('서로 다른 수학의 깊은 연결',-1.5,37,GREEN),txt('단순한 질문을 해결하는 새로운 관점',-3.4,29));self.to(174)
