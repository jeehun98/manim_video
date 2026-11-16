"""Forty independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT15_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT15_PREVIEW')=='1' else 1080
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
class CubicShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.15',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('절댓값 적분과 삼차함수',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
  self.add(Line([-7.15,3.55,0],[7.15,3.55,0],color=MUTED,stroke_opacity=.25,stroke_width=1))
  self.add(tx(self.info['title'],y=2.95,size=32))
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






 def change(self,m,s,t=None,y=.5,color=REL,size=72,x=0,width=13):
  if t is not None:self.to(t)
  n=eq(s,x,y,size,color,width);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def left(self,s,y=.6,size=53,color=INK):return eq(s,-3.7,y,size,color,width=6.1)
 @staticmethod
 def f(x,k=.25):return k*x*x*(x-3)
 @staticmethod
 def pieces(k,q):
  roots=np.roots([k,-3*k,0,q]);cuts=[0.,3.]
  for z in roots:
   if abs(z.imag)<1e-6 and 1e-7<z.real<3-1e-7 and not any(abs(z.real-v)<1e-6 for v in cuts):cuts.append(float(z.real))
  return sorted(cuts)
 @staticmethod
 def patch(ax,fun,a,b,color):
  xs=np.linspace(a,b,55);pts=[ax.c2p(a,0)]+[ax.c2p(x,fun(x)) for x in xs]+[ax.c2p(b,0)]
  return Polygon(*pts,stroke_width=0,fill_color=color,fill_opacity=.34).set_z_index(-1)
 def concept(self,mode='mixed'):
  ax=Axes(x_range=[-1.2,1.2,1],y_range=[-1.5,1.5,1],x_length=6.1,y_length=3.4,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  fun=(lambda x:x) if mode=='mixed' else ((lambda x:.4+.5*x*x) if mode=='positive' else (lambda x:-.4-.5*x*x))
  self.add(ax,ax.plot(fun,x_range=[-1,1,.02],color=INK,stroke_width=2.4),tx('개념 예시 · 실제 함수가 아님',3.4,2.15,21,MUTED,width=6.5))
  if mode=='mixed':
   a=self.patch(ax,fun,0,1,BASE);b=self.patch(ax,fun,-1,0,WARN);self.add(a,b,eq('A',*(ax.c2p(.6,.3))[:2],size=38,color=BASE),eq('B',*(ax.c2p(-.6,-.3))[:2],size=38,color=WARN));self.negative_patch=b;self.b_label=self.mobjects[-1]
  else:self.add(self.patch(ax,fun,-1,1,BASE if mode=='positive' else WARN))
  return ax
 def interval(self,start=-1,r=3,symbol=False):
  line=NumberLine(x_range=[-4,7,1],length=6.55,include_numbers=False,color=MUTED,stroke_width=1.3).move_to([3.35,.2,0]);self.ax=line;self.p_value=ValueTracker(start)
  self.add(line,*[eq(str(v),*(line.n2p(v)+DOWN*.33)[:2],size=22,color=MUTED) for v in [-3,0,3,6]])
  self.add(Dot(line.n2p(r),radius=.075,color=REL),eq('r' if symbol else f'x={r}',*(line.n2p(r)+DOWN*.85)[:2],size=32,color=REL))
  self.add(always_redraw(lambda:VGroup(Line(line.n2p(self.p_value.get_value())+UP*.65,line.n2p(self.p_value.get_value()+3)+UP*.65,color=EXP,stroke_width=6),Dot(line.n2p(self.p_value.get_value())+UP*.65,radius=.06,color=EXP),Dot(line.n2p(self.p_value.get_value()+3)+UP*.65,radius=.06,color=EXP))),always_redraw(lambda:eq('p',*(line.n2p(self.p_value.get_value())+UP*1.12)[:2],size=31,color=EXP)),always_redraw(lambda:eq('p+3',*(line.n2p(self.p_value.get_value()+3)+UP*1.12)[:2],size=31,color=EXP)))
  state=VGroup();state.flag=None
  def update_state(m):
   flag=self.p_value.get_value()+1e-7<r<self.p_value.get_value()+3-1e-7
   if flag!=m.flag:
    m.become(tx('내부에 포함 · 두 부호 존재' if flag else '내부에 포함되지 않음',3.35,-1.35,25,RESULT if flag else MUTED,width=6.5));m.flag=flag
  state.add_updater(update_state);self.add(state);update_state(state);return line

 def shift(self,q=0,k=.25,label='조건 (나) · [0,3] · 수직 이동 개념도',minimum=False):
  ax=Axes(x_range=[0,3,1],y_range=[-1.6,1.6,1],x_length=6.25,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax;self.q_value=ValueTracker(q);self.shift_k=k
  self.add(ax,tx(label,3.4,2.15,20,MUTED,width=6.5),*[eq(str(v),*(ax.c2p(v,0)+DOWN*.27)[:2],size=22,color=MUTED) for v in [0,3]])
  self.add(always_redraw(lambda:ax.plot(lambda x:CubicShot.f(x,k)+self.q_value.get_value(),x_range=[0,3,.025],color=REL,stroke_width=2.7,use_smoothing=False)))
  def areas():
   q=self.q_value.get_value();cuts=CubicShot.pieces(k,q);g=VGroup()
   for a,b in zip(cuts,cuts[1:]):
    val=CubicShot.f((a+b)/2,k)+q
    if abs(val)>1e-9:g.add(CubicShot.patch(ax,lambda x:CubicShot.f(x,k)+q,a,b,BASE if val>0 else WARN))
   return g
  self.add(always_redraw(areas))
  self.add(always_redraw(lambda:VGroup(Dot(ax.c2p(0,self.q_value.get_value()),radius=.055,color=BASE),Dot(ax.c2p(3,self.q_value.get_value()),radius=.055,color=BASE))))
  if minimum:self.add(always_redraw(lambda:Dot(ax.c2p(2,-4*k+self.q_value.get_value()),radius=.07,color=EXP)))
  return ax
 def shape(self,sign=1):
  ax=Axes(x_range=[-1,4,1],y_range=[-2,2,1],x_length=6.25,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  self.add(ax,ax.plot(lambda x:CubicShot.f(x,.25*sign),x_range=[-.7,3.55,.02],color=INK,stroke_width=2.6),Dot(ax.c2p(0,0),radius=.07,color=EXP),Dot(ax.c2p(3,0),radius=.07,color=EXP),eq('0',*(ax.c2p(0,0)+DOWN*.3)[:2],size=24,color=MUTED),eq('3',*(ax.c2p(3,0)+DOWN*.3)[:2],size=24,color=MUTED),tx('근의 형태 예시 · k의 크기와 부호는 아직 미정',3.4,2.15,18,MUTED,width=6.5));return ax
 def s01(self):
  n=tx('15',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=1);self.to(2)
  self.show(eq(r'\int_p^{p+3}|f(x)|\,dx\ne\left|\int_p^{p+3}f(x)\,dx\right|',y=1.5,size=51),eq('0<p<3',y=.35,size=45,color=EXP));self.to(5)
  self.show(eq(r'\int_0^3|f(x)+q|\,dx\ne\left|\int_0^3(f(x)+q)\,dx\right|',y=-.9,size=49));self.to(7)
  self.show(eq('0<q<1,\qquad f(6)=?',y=-2.1,size=42,color=EXP))
 def s02(self):
  self.add(eq(r'\int|f(x)|\,dx',y=1.35,size=88));self.to(12)
  self.show(tx('함수의 부호',y=-.1,size=49,color=EXP),tx('양수 영역',-3.3,-1.6,33,BASE,width=6),tx('음수 영역',3.3,-1.6,33,WARN,width=6))
 def s03(self):
  self.add(tx('절댓값을 먼저',-3.5,1.8,31,BASE,width=6),eq(r'\int_u^v|f(x)|\,dx',-3.5,.35,71,BASE,width=6));self.to(19)
  self.show(tx('적분한 뒤 절댓값',3.5,1.8,31,REL,width=6),eq(r'\left|\int_u^v f(x)\,dx\right|',3.5,.35,71,REL,width=6));self.to(26);self.note('언제 두 결과가 달라질까?',EXP)
 def s04(self):
  self.concept('positive');m=self.left(r'f(x)\ge0',y=1.2,size=72,color=BASE);self.add(m,self.left(r'\int|f|=\left|\int f\right|',y=-.2,size=49,color=RESULT));self.to(33)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption and m.get_center()[0]>.1 and m.get_top()[1]<2.5],run_time=.5);self.concept('negative');self.change(m,r'f(x)\le0',x=-3.7,y=1.2,width=6.1,size=72,color=WARN);self.note('한쪽 부호만 존재하면 두 결과는 같다',RESULT)
 def s05(self):
  self.concept();self.add(self.left(r'A>0,\quad B>0',y=1.15,size=66,color=EXP));self.to(39);self.note('A와 B는 모두 양의 넓이값으로 정의')
 def s06(self):
  ax=self.concept();self.add(self.left(r'\int_u^v|f(x)|\,dx=A+B',y=1.2,size=48,color=EXP));self.play(Transform(self.negative_patch,self.negative_patch.copy().flip(axis=RIGHT,about_point=ax.c2p(0,0))),self.b_label.animate.move_to(ax.c2p(-.6,.3)),run_time=2);self.note('아래쪽 영역도 양의 넓이로 더한다')
 def s07(self):
  self.concept();m=self.left(r'\int_u^v f(x)\,dx=A-B',y=1.2,size=49,color=EXP);self.add(m);self.to(49)
  self.change(m,r'\left|\int_u^v f(x)\,dx\right|=|A-B|',x=-3.7,y=1.2,width=6.1,size=47,color=REL)
 def s08(self):
  self.concept();self.add(self.left('A+B>|A-B|',y=1.15,size=61,color=EXP));self.to(55)
  self.show(self.left(r'A>0,\quad B>0',y=-.25,size=54,color=RESULT));self.note('구간 안에 양수 값과 음수 값이 모두 존재',RESULT)
 def s09(self):
  self.add(eq(r'\int_p^{p+3}|f(x)|\,dx\ne\left|\int_p^{p+3}f(x)\,dx\right|',y=1.1,size=64));self.to(60)
  self.show(eq('0<p<3',y=-.4,size=99,color=EXP));self.to(64);self.note('길이 3인 구간의 위치 p를 바꾼다')
 def s10(self):
  self.interval(-2);self.add(self.left('(p+3)-p=3',y=1.1,size=65,color=EXP));self.to(71)
  self.play(self.p_value.animate.set_value(3.5),run_time=3.5,rate_func=linear)
 def s11(self):
  self.interval(-1,r=3,symbol=True);self.add(self.left(r'p<r<p+3',y=1.2,size=68,color=REL));self.to(78)
  self.play(self.p_value.animate.set_value(1.5),run_time=2,rate_func=linear);self.note('부호 변화 지점 r을 구간 내부에 포함한다')
 def s12(self):
  self.interval(1.5,r=3,symbol=True);m=self.left('p<r<p+3',y=1.2,size=65,color=REL);self.add(m);self.to(85)
  self.change(m,'r-3<p<r',88,x=-3.7,y=1.2,width=6.1,size=67,color=EXP)
 def s13(self):
  self.interval(0);self.add(self.left('r-3<p<r',y=1.3,size=58,color=REL),self.left('0<p<3',y=.05,size=66,color=EXP));self.to(94)
  self.play(self.p_value.animate.set_value(1.5),run_time=1);self.to(96)
  self.show(self.left('r=3',y=-1.1,size=70,color=RESULT));self.play(self.p_value.animate.set_value(3),run_time=1.2);self.note('각 부호변화근의 (r−3,r)가 (0,3) 안에 있어야 한다')
 def s14(self):
  self.add(eq('f(x)=Ax^3+Bx^2+Cx',y=1.25,size=75));self.to(105)
  self.show(eq('f(0)=0',y=-.1,size=105,color=EXP));self.to(107);self.note('상수항 0 → x = 0도 함수의 근')
 def s15(self):
  self.interval(-3,r=0);self.add(tx('가정: 0에서 부호 변화?',-3.7,1.2,32,WARN,width=6.1));self.to(115)
  self.play(self.p_value.animate.set_value(-1),run_time=2);self.show(self.left('-3<p<0',y=-.1,size=70,color=WARN));self.to(120)
  self.note('가정: 0에서 부호 변화 → 주어진 p 범위와 모순',WARN)
 def s16(self):
  self.shape();self.add(self.left('f(0)=0',y=1.4,size=70,color=EXP));self.to(129)
  self.show(self.left('x^2',y=-.1,size=107,color=REL));self.to(132);self.note('0은 중근 · 축에 접하고 같은 부호로 돌아온다')
 def s17(self):
  self.shape();self.add(self.left('f(3)=0',y=1.4,size=67,color=EXP));self.to(136)
  self.show(self.left('(x-3)',y=-.15,size=89,color=REL));self.note('3은 단순근 · 부호가 바뀌며 축을 통과')
 def s18(self):
  self.add(eq('x^2',-3.4,1.4,88,REL,width=6),eq('(x-3)',3.4,1.4,88,REL,width=6));self.to(141)
  self.show(eq('f(x)=kx^2(x-3)',y=-.25,size=91,color=RESULT));self.to(145);self.note('k ≠ 0 · 아직 크기와 부호는 미정',MUTED)
 def s19(self):
  self.add(eq(r'\int_0^3|f(x)+q|\,dx\ne\left|\int_0^3(f(x)+q)\,dx\right|',y=1.15,size=63));self.to(150)
  self.show(eq('0<q<1',y=-.3,size=94,color=REL));self.note('구간은 [0,3]으로 고정 · 이번에는 q가 변한다')
 def s20(self):
  self.shift(label='수직 이동 설명용 그래프 · k의 부호는 미정');self.add(self.left('y=f(x)+q',y=1.3,size=70,color=REL));self.to(158)
  self.play(self.q_value.animate.set_value(.5),run_time=1.5);self.to(160)
  self.play(self.q_value.animate.set_value(-.4),run_time=2);self.note('q > 0: 위로  /  q < 0: 아래로')
 def s21(self):
  self.add(eq('0<q<1',y=1.4,size=99,color=REL));self.to(169)
  self.show(tx('양수 부분과 음수 부분이 동시에 존재',y=-.3,size=38,color=EXP));self.note('양수 q를 더한 결과에도 두 부호가 남아야 한다')
 def s22(self):
  self.add(eq('0<x<3',y=1.7,size=74,color=EXP));self.to(178)
  self.show(eq('x^2>0',-3.4,-.1,87,BASE,width=6),eq('x-3<0',3.4,-.1,87,WARN,width=6));self.note('x²(x−3)는 구간 (0,3)에서 음수')
 def s23(self):
  self.shift(k=.25,label='경우 비교: k > 0의 방향 예시');m=self.left(r'k>0\Rightarrow f(x)<0',y=1.15,size=45,color=WARN);self.add(m);self.to(187)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption and m.get_center()[0]>.1 and m.get_top()[1]<2.5],run_time=.4)
  self.shift(q=.2,k=-.25,label='경우 비교: k < 0에 양수 q를 더한 예시');self.change(m,r'k<0\Rightarrow f(x)>0',x=-3.7,y=1.15,width=6.1,size=45,color=BASE);self.note('k < 0이면 f + q는 양수뿐 → 조건 불가능',WARN);self.to(191)
  self.show(self.left('k>0',y=-.5,size=91,color=RESULT))
 def s24(self):
  self.shift();self.add(self.left('f(0)=f(3)=0',y=1.2,size=57,color=EXP));self.to(198)
  self.show(self.left(r'0<x<3:\ f(x)<0',y=-.15,size=46,color=WARN));self.to(202)
  self.play(self.q_value.animate.set_value(.4),run_time=3,rate_func=linear);self.note('양수 q를 더하면 양 끝점은 축 위로 이동')
 def s25(self):
  self.shift(q=.4,minimum=True);self.add(self.left('0<q<1',y=1.25,size=76,color=REL));self.to(209)
  self.show(self.left(r'\min_{[0,3]}(f+q)<0',y=-.2,size=53,color=WARN));self.note('끝은 양수 · 가운데는 음수 → 두 부호 공존')
 def s26(self):
  self.shift(q=.4,minimum=True);self.add(self.left('y=f(x)+q',y=1.25,size=70,color=REL));self.play(self.q_value.animate.set_value(.8),run_time=3,rate_func=linear);self.to(215)
  self.play(self.q_value.animate.set_value(.98),run_time=3,rate_func=linear);self.to(219)
  self.play(self.q_value.animate.set_value(1),run_time=2,rate_func=linear);self.note('음수 영역 소멸 · 두 적분값이 같아진다',RESULT)
 def s27(self):
  self.shift(q=1,minimum=True);m=self.left('q=1',y=1.2,size=83,color=REL);self.add(m);self.to(228)
  self.change(m,r'\min_{[0,3]}f=-1',x=-3.7,y=1.2,width=6.1,size=67,color=RESULT);self.note('경계 q = 1에서 최저점이 x축에 접한다')
 def s28(self):
  m=eq('f(x)=kx^2(x-3)',size=89,color=RESULT);self.add(m);m=self.change(m,'f(x)=kx^3-3kx^2',234,size=87);m=self.change(m,"f'(x)=3kx^2-6kx",238,size=87);self.change(m,"f'(x)=3kx(x-2)",241,size=90,color=REL)
 def s29(self):
  ax=self.shift(minimum=True,label='[0,3]에서 도함수의 부호와 최솟값');self.add(self.left("f'(x)=3kx(x-2)",y=1.45,size=52,color=REL));self.show(self.left("0<x<2:\ f'(x)<0",y=.15,size=42,color=WARN));self.to(246)
  self.show(self.left("2<x<3:\ f'(x)>0",y=-1,size=42,color=BASE));self.to(249)
  self.note('[0,3]에서 x = 2일 때 최솟값',RESULT);self.add(eq('2',*(ax.c2p(2,0)+DOWN*.3)[:2],size=25,color=EXP))
 def s30(self):
  m=eq(r'f(2)=k\cdot2^2(2-3)',size=89);self.add(m);m=self.change(m,'f(2)=-4k',256,size=103);self.change(m,'-4k=-1',259,size=110,color=RESULT)
 def s31(self):
  m=eq('-4k=-1',size=109);self.add(m);self.change(m,r'k=\frac14',262.5,size=117,color=RESULT)
 def s32(self):
  m=eq('f(x)=kx^2(x-3)',size=93,color=RESULT);self.add(m);self.change(m,r'f(x)=\frac14x^2(x-3)',267,size=98,color=RESULT)
 def s33(self):
  m=eq('f(6)=?',size=110,color=EXP);self.add(m);m=self.change(m,r'f(6)=\frac14\cdot6^2(6-3)',275,size=88);self.change(m,r'f(6)=\frac14\cdot36\cdot3',277,size=91,color=RESULT)
 def s34(self):
  self.add(eq(r'f(6)=\boxed{27}',y=.7,size=113,color=RESULT));self.to(281);self.show(tx('정답 ④',y=-1.4,size=39,color=RESULT),rt=.5)
 def s35(self):
  self.concept();self.add(self.left(r'\int|f|\ne\left|\int f\right|',y=1.2,size=54,color=EXP));self.to(285)
  self.show(self.left('A+B>|A-B|',y=-.25,size=61,color=REL));self.to(291);self.note('두 적분값이 다름 ⇔ 구간 안에 양수와 음수 모두 존재',RESULT)
 def s36(self):
  self.interval(0);self.add(self.left('0<p<3',y=1.25,size=84,color=EXP));self.play(self.p_value.animate.set_value(1.5),run_time=3);self.to(302)
  self.show(self.left(r'x=0:\ x^2',y=-.1,size=60,color=REL),self.left(r'x=3:\ (x-3)',y=-1.1,size=57,color=REL));self.note('0에서는 접함 · 3에서는 통과')
 def s37(self):
  self.shift(q=.4,minimum=True);self.add(self.left('0<q<1',y=1.3,size=77,color=REL));self.play(self.q_value.animate.set_value(1),run_time=4,rate_func=linear);self.to(312)
  self.show(self.left(r'\min_{[0,3]}f=-1',y=-.1,size=60,color=RESULT));self.to(315);self.note('−4k = −1 → k = 1/4',RESULT)
 def s38(self):
  self.show(tx('① 부호 분석',-4.7,1.65,30,EXP,width=4.4),eq('A+B>|A-B|',-4.7,.25,45,EXP,width=4.4));self.to(322)
  self.show(tx('② 근의 위치',0,1.65,30,REL,width=4.4),eq('x=0,3',0,.25,61,REL,width=4.4));self.to(325)
  self.show(tx('③ 최솟값',4.7,1.65,30,RESULT,width=4.4),eq(r'\min_{[0,3]}f=-1',4.7,.25,43,RESULT,width=4.4))
 def s39(self):
  self.interval(0);self.add(self.left('[p,p+3]',y=1.25,size=72,color=EXP));self.play(self.p_value.animate.set_value(2.5),run_time=3);self.to(332)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption and m.get_center()[0]>.1 and m.get_top()[1]<2.5],run_time=.3)
  self.shift(q=.2,minimum=True);self.show(self.left('f(x)+q',y=-.1,size=67,color=REL));self.play(self.q_value.animate.set_value(1),run_time=2.5);self.note('조건 (가): 구간 이동 / 조건 (나): 수직 이동')
 def s40(self):
  self.add(eq(r'f(x)=\frac14x^2(x-3)',y=1.45,size=76,color=RESULT),eq(r'f(6)=\boxed{27}',y=-.05,size=105,color=RESULT),tx('정답 ④',y=-1.7,size=36,color=RESULT));self.to(338.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(40):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(CubicShot,),{'shot':i,'__module__':__name__})
