"""Thirty independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT20_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT20_PREVIEW')=='1' else 1080
config.background_color='#0B1020'
WARN='#FB923C'
INK='#F8FAFC';BASE='#38BDF8';EXP='#FACC15';REL='#C084FC';RESULT='#4ADE80';MUTED='#94A3B8'
def tx(s,x=0,y=0,size=28,color=INK,width=14):return text(s,x,y,size,color,width)
def eq(s,x=0,y=.4,size=64,color=INK,width=13):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def card(s,x,y,color=REL,width=4.5):
 return VGroup(RoundedRectangle(width=width,height=1.1,corner_radius=.15,stroke_color=color,stroke_width=1.4,fill_color=color,fill_opacity=.06).move_to([x,y,0]),eq(s,x,y,40,color,width-.4))
class IntersectionShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.20',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('지수함수와 로그함수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
  self.add(Line([-7.15,3.55,0],[7.15,3.55,0],color=MUTED,stroke_opacity=.25,stroke_width=1))
  self.add(tx(self.info['title'],y=2.95,size=32))
  self.status()
  self.caption=VGroup().set_z_index(50);self.add(self.caption)
  self.caption.add_updater(self.update_caption);self.update_caption(self.caption)
  self.bound_checks=0
 def update_caption(self,m,dt=0):
  now=self.offset+self.time;i=bisect_right([s['start'] for s in DATA['sentences']],now+1e-6)-1
  if i==self.caption_index:return
  self.caption_index=i
  lines=textwrap.wrap(DATA['sentences'][i]['caption'],width=53,break_long_words=False,break_on_hyphens=False)
  new=tx('\n'.join(lines),y=-3.5,size=28,width=14.1)
  if new.height>1.1:new.scale_to_fit_height(1.1)
  assert new.get_top()[1]<-2.8 and new.get_bottom()[1]>-4.2
  m.become(new).set_z_index(50)
 def update_mobjects(self,dt):
  super().update_mobjects(dt)
  for m in self.mobjects:
   if m is self.caption or m.width<.001:continue
   assert m.get_left()[0]>=-7.8 and m.get_right()[0]<=7.8,(self.shot,self.time,'x')
   assert m.get_bottom()[1]>-2.65 and m.get_top()[1]<4.4,(self.shot,self.time,'y',m.get_bottom())
  self.bound_checks+=1
 def to(self,t):
  frames=round((t-self.offset-self.time)*30)
  if frames<0:raise RuntimeError(f'Overrun {self.offset+self.time} > {t}')
  if frames:self.wait(frames/30-1e-8)
 def show(self,*ms,rt=.6):self.play(*[FadeIn(m,shift=UP*.08) for m in ms],run_time=rt)
 def morph(self,a,b,rt=.7):self.play(ReplacementTransform(a,b),run_time=rt);return b
 def note(self,s,color=MUTED):
  new=tx('\n'.join(textwrap.wrap(s,width=27,break_long_words=False)),x=-3.7,y=-1.9,size=24,color=color,width=6.1) if hasattr(self,'ax') else tx(s,y=-1.95,size=26,color=color)
  if new.height>.8:new.scale_to_fit_height(.8)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')











 def status(self):
  t=self.offset
  vals=[r'p=3' if t>=131 else r'p=?',r'q=3^{1/4}' if t>=168 else r'q=?',r'r=-\frac43 3^{1/4}' if t>=249 else r'r=?']
  for x,s in zip([-4.6,0,4.6],vals):
   self.add(RoundedRectangle(width=4.25,height=.6,corner_radius=.12,stroke_color=MUTED,stroke_opacity=.35,stroke_width=1).move_to([x,2.25,0]),eq(s,x,2.25,28,RESULT if '?' not in s else MUTED,width=3.9))
 def plane(self,ray=False):
  beta=3**.25;alpha=beta/3;b=beta**(1/alpha)
  ax=Axes(x_range=[0,2.1,1],y_range=[-1.5,3.8,1],x_length=6.1,y_length=3.15,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.45,-.25,0]);self.ax=ax
  c1=ax.plot(lambda x:b**x,x_range=[0,2,.015],color=BASE,stroke_width=2.5,use_smoothing=False).set_fill(opacity=0)
  c2=ax.plot(lambda x:-np.log(x)/np.log(b),x_range=[b**(-3.65),2,.015],color=REL,stroke_width=2.5,use_smoothing=False).set_fill(opacity=0)
  self.add(ax,c1,c2,tx('지수함수: 청록 · 로그함수: 보라',3.45,1.65,21,MUTED,width=6.2))
  for v in [0,1,2]:self.add(eq(str(v),*(ax.c2p(v,0)+DOWN*.23)[:2],size=20,color=MUTED))
  for v in [1,3]:self.add(eq(str(v),*(ax.c2p(0,v)+LEFT*.2)[:2],size=20,color=MUTED))
  self.add(Dot(ax.c2p(alpha,beta),radius=.07,color=EXP),eq(r'P(\alpha,\beta)',*(ax.c2p(alpha,beta)+RIGHT*1.1+UP*.27)[:2],size=29,color=EXP))
  self.add(DashedLine(ax.c2p(alpha,0),ax.c2p(alpha,beta),color=EXP,stroke_width=1),DashedLine(ax.c2p(0,beta),ax.c2p(alpha,beta),color=EXP,stroke_width=1))
  if ray:self.add(Line(ax.c2p(0,0),ax.c2p(1.15,3.45),color=RESULT,stroke_width=2.5))
 def lesson(self):
  plan=PLANS[self.shot]
  if plan.get('graph'):self.plane(plan.get('ray',False))
  x=-3.65 if plan.get('graph') else 0;width=6.1 if plan.get('graph') else 13.5
  if plan.get('known'):self.add(eq(plan['known'],x,1.15,31,MUTED,width))
  events=plan['events'];m=None
  for t,formula in events:
   self.to(t)
   n=eq(formula,x,-.15 if plan.get('known') else .25,49 if plan.get('graph') else 66,plan.get('color',INK),width)
   if m is None:self.show(n)
   else:self.play(TransformMatchingTex(m,n),run_time=.7)
   m=n
  if plan.get('note'):self.note(plan['note'],plan.get('note_color',MUTED))

PLANS=[
 dict(graph=True,ray=True,events=[(0,r'f(x)=b^x,\quad b>1'),(3,r'g(x)=-\log_bx'),(7,r'P(\alpha,\beta),\ O(0,0)')],note='원점과 교점을 연결한 직선의 기울기'),
 dict(events=[(10,r'p=m,\quad q=\beta,\quad r=g(m)')],known=r'\alpha\beta^3=1',note='세 빈칸을 채우고 (pqr)²을 계산한다'),
 dict(graph=True,events=[(16,r'\beta=b^\alpha=-\log_b\alpha')],note='같은 점을 지난다는 조건에 집중'),
 dict(graph=True,events=[(23,r'f(x)=b^x,\quad g(x)=-\log_bx'),(30,r'b>1'),(32,r'f\nearrow,\quad g\searrow')],note='b>1: 지수함수는 증가, 음의 로그함수는 감소'),
 dict(graph=True,events=[(38,r'P=(\alpha,\beta)'),(41,r'\alpha>0,\quad\beta>0')],note='제1사분면의 교점'),
 dict(graph=True,known=r'P=(\alpha,\beta)',events=[(44,r'f(\alpha)=g(\alpha)=\beta'),(49,r'\beta=b^\alpha=-\log_b\alpha')],note='두 함수에 같은 x좌표를 대입한다'),
 dict(known=r'\beta=b^\alpha',events=[(54,r'\beta=b^\alpha'),(57,r'\log_b\beta=\alpha')],note='지수식과 로그식은 같은 관계를 표현한다'),
 dict(known=r'\log_b\beta=\alpha',events=[(62,r'\beta=-\log_b\alpha'),(65,r'\log_b\alpha=-\beta')],note='두 좌표를 모두 로그로 표현했다'),
 dict(known=r'\log_b\alpha=-\beta,\qquad\log_b\beta=\alpha',events=[(71,r'\alpha\beta^3=1')],note='곱으로 연결된 조건에 로그를 취한다'),
 dict(events=[(77,r'\log_b(\alpha\beta^3)=\log_b1'),(80,r'\log_b(\alpha\beta^3)=0')],note='α>0, β>0이므로 로그를 취할 수 있다'),
 dict(events=[(83,r'\log_b(\alpha\beta^3)=0'),(86,r'\log_b\alpha+\log_b\beta^3=0')],note='곱의 로그는 로그의 합'),
 dict(events=[(90,r'\log_b\alpha+\log_b\beta^3=0'),(94,r'\log_b\alpha+3\log_b\beta=0')],note='거듭제곱의 지수 3을 계수로'),
 dict(known=r'\log_b\alpha=-\beta,\qquad\log_b\beta=\alpha',events=[(99,r'\log_b\alpha+3\log_b\beta=0'),(105,r'-\beta+3\alpha=0')],note='이미 얻은 관계를 대입한다'),
 dict(graph=True,ray=True,events=[(108,r'-\beta+3\alpha=0'),(111,r'\beta=3\alpha')],note='교점의 세로좌표는 가로좌표의 3배',color=RESULT),
 dict(graph=True,ray=True,known=r'\beta=3\alpha',events=[(117,r'm=\frac{\beta}{\alpha}')],note='기울기 = 세로 변화량 ÷ 가로 변화량'),
 dict(graph=True,ray=True,known=r'\beta=3\alpha',events=[(125,r'm=\frac{\beta}{\alpha}=3'),(128,r'p=3')],color=RESULT,note='첫 번째 빈칸'),
 dict(known=r'm=\frac{\beta}{\alpha}',events=[(131,r'\beta=m\alpha')],note='기울기와 좌표의 관계를 다시 사용한다'),
 dict(known=r'\beta=m\alpha',events=[(140,r'\beta\cdot\beta^3=m\alpha\cdot\beta^3'),(143,r'\beta^4=m(\alpha\beta^3)')],note='주어진 곱 αβ³을 만들어 준다'),
 dict(known=r'\alpha\beta^3=1',events=[(146,r'\beta^4=m(\alpha\beta^3)'),(151,r'\beta^4=m')],note='주어진 조건으로 곱을 1로 바꾼다'),
 dict(known=r'm=3,\quad\beta>0',events=[(154,r'\beta^4=3'),(161,r'\beta=3^{1/4}')],note='β가 양수이므로 양의 네제곱근을 선택'),
 dict(events=[(164,r'q=\beta=3^{1/4}')],note='두 번째 빈칸',color=RESULT),
 dict(known=r'g(x)=-\log_bx',events=[(168,r'g(m)=\ ?'),(173,r'g(m)=-\log_bm')],note='구하려는 것은 밑 b가 아니라 함수값'),
 dict(known=r'\log_b\alpha=-\beta',events=[(178,r'g(m)=-\log_bm')],note='밑변환으로 이미 알고 있는 로그를 만든다'),
 dict(known=r'm=3>1,\quad 0<\alpha<1',events=[(186,r'\log_bm=\frac{\log_b\alpha}{\log_m\alpha}'),(191,r'g(m)=\frac{-\log_b\alpha}{\log_m\alpha}')],note='분자: logᵦ α  /  분모: logₘ α',note_color=WARN),
 dict(known=r'-\log_b\alpha=\beta',events=[(197,r'g(m)=\frac{-\log_b\alpha}{\log_m\alpha}'),(200,r'g(m)=\frac{\beta}{\log_m\alpha}')],note='분자에 교점 조건을 대입한다'),
 dict(known=r'\alpha=\frac{\beta}{m}',events=[(203,r'g(m)=\frac{\beta}{\log_m\alpha}'),(209,r'g(m)=\frac{\beta}{\log_m(\beta/m)}')],note='분모도 β와 m만으로 표현한다'),
 dict(known=r'\log_m m=1',events=[(214,r'g(m)=\frac{\beta}{\log_m\beta-\log_m m}'),(219,r'g(m)=\frac{\beta}{\log_m\beta-1}')],note='비의 로그는 로그의 차'),
 dict(known=r'm=3,\quad\beta=3^{1/4}',events=[(225,r'g(m)=\frac{\beta}{\log_m\beta-1}')],note='밑 b 없이 필요한 값만 대입'),
 dict(known=r'\log_3\beta=\log_3 3^{1/4}=\frac14',events=[(231,r'\log_3\beta-1=\frac14-1'),(234,r'\log_3\beta-1=-\frac34')],note='분모는 음수'),
 dict(events=[(238,r'g(m)=\frac{3^{1/4}}{-3/4}'),(243,r'g(m)=-\frac43 3^{1/4}'),(247,r'r=-\frac43 3^{1/4}')],note='세 번째 빈칸',color=RESULT),
 dict(events=[(249,r'p=3,\quad q=3^{1/4},\quad r=-\frac43 3^{1/4}')],note='이제 세 값을 곱한 뒤 제곱한다'),
 dict(known=r'p=3,\quad q=3^{1/4},\quad r=-\frac43 3^{1/4}',events=[(259,r'(pqr)^2=\left(3\cdot3^{1/4}\cdot\left(-\frac43 3^{1/4}\right)\right)^2')]),
 dict(events=[(263,r'pqr=3\cdot\left(-\frac43\right)\cdot3^{1/4}\cdot3^{1/4}'),(266,r'pqr=-4\cdot3^{1/4}\cdot3^{1/4}')],note='계수 3과 분모 3을 약분'),
 dict(events=[(268,r'pqr=-4\cdot3^{1/4+1/4}'),(271,r'pqr=-4\cdot3^{1/2}')],note='같은 밑의 거듭제곱을 곱하면 지수를 더한다'),
 dict(events=[(274,r'pqr=-4\sqrt3'),(277,r'(pqr)^2=(-4\sqrt3)^2'),(280,r'(pqr)^2=48')],note='정답 48',color=RESULT),
 dict(graph=True,ray=True,events=[(282,r'b,\quad\alpha,\quad\beta'),(291,r'\frac{\beta}{\alpha}=3')],note='각각의 값보다 좌표 사이의 관계'),
 dict(known=r'\log_b\alpha=-\beta,\qquad\log_b\beta=\alpha',events=[(294,r'\alpha\beta^3=1'),(300,r'-\beta+3\alpha=0'),(305,r'\beta=3\alpha')],note='곱의 조건을 로그로 바꾸면 비율이 드러난다'),
 dict(graph=True,ray=True,events=[(309,r'\beta=3\alpha\ \Longrightarrow\ m=3')],note='좌표의 비율은 원점과 교점을 잇는 기울기'),
 dict(events=[(313,r'm=3\ \Longrightarrow\ \beta^4=3'),(317,r'\beta=3^{1/4},\quad g(m)=-\frac43 3^{1/4}')],note='기울기와 좌표 관계, 밑변환으로 필요한 값을 완성'),
 dict(events=[(321,r'\beta=b^\alpha\ \Longleftrightarrow\ \log_b\beta=\alpha')],known=r'\log_b\alpha=-\beta',note='서로 다른 표현을 같은 형태로 바꾸어 연결한다'),
 dict(events=[(329,r'b,\ \alpha,\ \beta\quad\longrightarrow\quad m,\ \beta,\ g(m)')],note='문제에서 실제로 요구하는 값을 먼저 확인'),
 dict(events=[(335,r'\frac{\beta}{\alpha}=3\quad\Longrightarrow\quad(pqr)^2=48')],note='필요한 관계를 직접 이용하면 계산을 줄일 수 있다',color=RESULT),
 dict(events=[(342,r'\text{Relation}\ \longrightarrow\ \text{Transformation}\ \longrightarrow\ 48')],note='필요한 관계를 찾고, 계산하기 쉬운 형태로 바꾼다',color=RESULT),
]
assert len(PLANS)==len(DATA['scenes'])==43
for i in range(43):
 setattr(IntersectionShot,f's{i+1:02d}',IntersectionShot.lesson)
 globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(IntersectionShot,),{'shot':i})
