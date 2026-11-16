"""Thirty-three independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT13_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT13_PREVIEW')=='1' else 1080
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
class AreaShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.13',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('넓이와 미분',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
 def left(self,s,y=.5,size=52,color=INK):return eq(s,-3.7,y,size,color,width=6.1)
 @staticmethod
 def h(x):return (x-1)**2+1
 def area(self,ax,a,b,color=EXP,between=False):
  xs=np.linspace(a,b,90)
  lo=(lambda x:.2*x+.5) if between else (lambda x:0)
  hi=(lambda x:.2*x+.5+self.h(x)) if between else self.h
  return Polygon(*([ax.c2p(x,lo(x)) for x in xs]+[ax.c2p(x,hi(x)) for x in xs[::-1]]),stroke_width=0,fill_color=color,fill_opacity=.3).set_z_index(-1)
 def curves(self,end=2):
  ax=Axes(x_range=[0,3.2,1],y_range=[0,7,1],x_length=6.1,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.4,.05,0]);self.ax=ax
  g=lambda x:.2*x+.5;f=lambda x:g(x)+self.h(x);self.g=g;self.f=f
  upper=ax.plot(f,x_range=[0,3.15],color=BASE,stroke_width=2.7);lower=ax.plot(g,x_range=[0,3.15],color=REL,stroke_width=2.7)
  self.add(ax,upper,lower,tx('관계 설명용 예시 곡선',3.4,2.15,20,MUTED,width=6.5),eq('f',*(ax.c2p(3.05,f(3.05))+LEFT*.25+UP*.2)[:2],size=30,color=BASE),eq('g',*(ax.c2p(3.05,g(3.05))+UP*.25)[:2],size=30,color=REL))
  self.boundary=ValueTracker(end);self.add(always_redraw(lambda:self.area(ax,0,self.boundary.get_value(),between=True)))
  self.add(always_redraw(lambda:Line(ax.c2p(self.boundary.get_value(),g(self.boundary.get_value())),ax.c2p(self.boundary.get_value(),f(self.boundary.get_value())),color=EXP,stroke_width=3)))
  self.add(eq('0',*(ax.c2p(0,0)+DOWN*.25)[:2],size=23,color=MUTED),always_redraw(lambda:eq('t',*(ax.c2p(self.boundary.get_value(),0)+DOWN*.25)[:2],size=28,color=EXP)))
  return ax
 def strip(self,width=.45):
  ax=self.ax;self.delta=ValueTracker(width);t=2
  strip=always_redraw(lambda:self.area(ax,t,t+self.delta.get_value(),EXP,between=True).set_fill(opacity=.7).set_z_index(1));self.add(strip)
  line=always_redraw(lambda:Line(ax.c2p(t+self.delta.get_value(),self.g(t+self.delta.get_value())),ax.c2p(t+self.delta.get_value(),self.f(t+self.delta.get_value())),color=EXP,stroke_width=2));self.add(line);return strip
 def parabola(self,areas=None):
  ax=Axes(x_range=[-2.4,4.4,1],y_range=[0,11,2],x_length=6.5,y_length=3.65,tips=False,axis_config={'color':MUTED,'stroke_width':1.1}).move_to([3.35,.05,0]);self.ax=ax
  curve=ax.plot(self.h,x_range=[-2,4,.02],color=INK,stroke_width=2.3,use_smoothing=False)
  axis=DashedLine(ax.c2p(1,0),ax.c2p(1,11),color=WARN,stroke_width=1.4,dash_length=.08);self.symmetry_axis=axis
  labs=VGroup(*[eq(str(v),*(ax.c2p(v,0)+DOWN*.28)[:2],size=21,color=MUTED) for v in [-2,0,1,2,4]],eq('10',*(ax.c2p(0,10)+LEFT*.3)[:2],size=21,color=MUTED),eq('x=1',*(ax.c2p(1,11)+UP*.25)[:2],size=27,color=WARN))
  self.add(ax,curve,axis,labs)
  if areas:
   for a,b,c in areas:self.add(self.area(ax,a,b,c))
  return ax
 def s01(self):
  n=tx('13',size=85,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.85,0]),run_time=2)
  self.show(eq('f(x)>g(x)',-3.5,1.5,52,BASE,width=6),eq('f(1)-g(1)=1',3.5,1.5,52,REL,width=6));self.to(5)
  self.show(eq("S'(t)=t^2-2t+a",y=.1,size=69,color=EXP));self.to(8)
  self.show(tx('ㄱ. a = 1',-4.6,-1.55,26,width=4),tx('ㄴ. S(3) = 6',0,-1.55,26,width=4),tx('ㄷ. 두 구간의 넓이',4.6,-1.55,26,width=4))
 def s02(self):
  m=eq('S(t)',size=110,color=EXP);self.add(m);self.change(m,"S'(t)",13,size=110,color=EXP);self.note('넓이의 순간적인 변화율')
 def s03(self):
  ax=self.curves();self.add(self.left('f(x)>g(x)',y=1.3,size=65,color=BASE));self.to(20)
  self.play(Indicate(Line(ax.c2p(2,self.g(2)),ax.c2p(2,self.f(2)),color=EXP)),run_time=1);self.to(23)
  self.show(self.left('f(x)-g(x)',y=-.4,size=63,color=EXP))
 def s04(self):
  self.curves(.2);self.add(self.left(r'S(t)=\int_0^t[f(x)-g(x)]\,dx',y=.9,size=43,color=EXP));self.to(28)
  self.play(self.boundary.animate.set_value(2),run_time=2,rate_func=linear);self.note('0 ≤ x ≤ t · 세로 높이 차이를 누적')
 def s05(self):
  self.curves(2);self.add(self.left(r't\ \longrightarrow\ t+\Delta t',y=1.3,size=52,color=EXP));self.to(35)
  ax=self.ax;self.strip(.03);self.play(self.delta.animate.set_value(.45),run_time=2,rate_func=linear);self.to(37)
  self.show(self.left(r'\Delta S\approx[f(t)-g(t)]\Delta t',y=-.1,size=42,color=EXP));self.to(39)
  rect=Polygon(ax.c2p(2,self.g(2)),ax.c2p(2.45,self.g(2)),ax.c2p(2.45,self.f(2)),ax.c2p(2,self.f(2)),color=RESULT,fill_opacity=.08,stroke_width=1.6);self.play(Create(rect),run_time=.8);self.note('정확한 띠 넓이 ≈ 높이 차이 × 작은 가로 폭')
 def s06(self):
  self.curves(2);self.strip(.45);m=self.left(r'\frac{\Delta S}{\Delta t}\approx f(t)-g(t)',y=.7,size=48,color=EXP);self.add(m)
  self.play(self.delta.animate.set_value(.025),run_time=3,rate_func=linear);self.to(46)
  m=self.change(m,r'\lim_{\Delta t\to0}\frac{\Delta S}{\Delta t}=f(t)-g(t)',x=-3.7,y=.7,width=6.1,size=47,color=EXP);self.to(50)
  self.change(m,r"S'(t)=f(t)-g(t)",x=-3.7,y=.7,width=6.1,size=59,color=RESULT);self.note('넓이를 미분하면 경계에서의 높이 차이가 남는다',RESULT)
 def s07(self):
  self.add(eq("S'(t)=f(t)-g(t)",y=1.65,size=59,color=EXP));m=eq("S'(t)=t^2-2t+a",y=-.1,size=70);self.add(m);self.to(58)
  self.change(m,'f(t)-g(t)=t^2-2t+a',y=-.1,size=72,color=REL)
 def s08(self):
  self.add(eq('f(t)-g(t)=t^2-2t+a',y=1.8,size=47,color=REL));self.to(63);self.show(eq(r'a=1\ ?',y=-.1,size=99,color=EXP));self.note('ㄱ 보기의 주장')
 def s09(self):
  m=eq('f(1)=g(1)+1',size=86,color=BASE);self.add(m);self.change(m,'f(1)-g(1)=1',70,size=87,color=BASE)
 def s10(self):
  m=eq('f(1)-g(1)=1^2-2(1)+a',size=71);self.add(m);m=self.change(m,'1=1-2+a',74,size=89);m=self.change(m,'1=a-1',76,size=93);self.change(m,'a=2',78,size=106,color=RESULT)
 def s11(self):
  self.add(eq('a=2',y=1.65,size=67,color=RESULT));m=eq('a=1',y=-.1,size=91,color=WARN);self.add(m,Cross(m,stroke_color=WARN,stroke_width=3));self.note('ㄱ 거짓',WARN)
 def s12(self):
  self.add(tx('ㄱ 거짓  /  ㄴ 확인',y=1.95,size=26,color=MUTED));self.to(85);self.show(eq(r'S(3)=6\ ?',y=.9,size=77,color=EXP));self.to(87)
  m=eq("S'(t)=t^2-2t+a",y=-.8,size=67);self.add(m);self.change(m,"S'(t)=t^2-2t+2",89,y=-.8,size=67,color=REL)
 def s13(self):
  m=eq(r"S(3)=\int_0^3 S'(t)\,dt",size=78,color=EXP);self.add(m);self.change(m,r'S(3)=\int_0^3(t^2-2t+2)\,dt',96,size=73,color=EXP);self.note('넓이의 정의에서 S(0) = 0')
 def s14(self):
  self.add(eq(r'\int_0^3(t^2-2t+2)\,dt',y=1.65,size=58,color=EXP));self.show(eq(r't^2\to\frac{t^3}{3}',-4.5,-.2,51,BASE,width=4));self.to(101)
  self.show(eq(r'-2t\to-t^2',0,-.2,51,REL,width=4));self.to(104);self.show(eq(r'2\to2t',4.5,-.2,51,RESULT,width=4));self.show(eq(r'\left[\frac{t^3}{3}-t^2+2t\right]_0^3',y=-1.75,size=50,color=EXP))
 def s15(self):
  m=eq(r'S(3)=\frac{27}{3}-9+6',size=84,color=EXP);self.add(m);m=self.change(m,'S(3)=9-9+6',108,size=85);self.change(m,'S(3)=6',110,size=99,color=RESULT);self.note('ㄱ 거짓  /  ㄴ 참',RESULT)
 def intervals(self):
  line=NumberLine(x_range=[-3,5,1],length=12,include_numbers=False,color=MUTED).move_to([0,.6,0]);self.add(line)
  self.add(*[eq(str(v),*(line.n2p(v)+DOWN*.3)[:2],size=26,color=MUTED) for v in [-2,0,1,2,4]])
  return line
 def s16(self):
  line=self.intervals();self.to(115)
  self.show(Line(line.n2p(-2)+UP*.6,line.n2p(2)+UP*.6,color=BASE,stroke_width=7),eq('[-2,2]',-1.5,1.95,43,BASE));self.to(118)
  self.show(Line(line.n2p(0)+DOWN*.8,line.n2p(4)+DOWN*.8,color=REL,stroke_width=7),eq('[0,4]',1.5,-1.05,43,REL))
 def s17(self):
  self.add(eq('2-(-2)=4',-3.5,1.25,69,BASE,width=6),eq('4-0=4',3.5,1.25,69,REL,width=6));self.to(124)
  self.show(tx('구간의 길이만으로 넓이는 결정되지 않는다',y=-.3,size=34,color=WARN));self.note('넓이는 각 위치의 높이까지 누적한 결과')
 def s18(self):
  m=eq('h(x)=f(x)-g(x)',y=.7,size=81,color=EXP);self.add(m);self.to(132)
  self.change(m,'h(x)=x^2-2x+2',size=85,color=REL);self.note('h는 두 함수의 차이 · 개별 f, g의 식이 아님')
 def s19(self):
  m=eq('x^2-2x+2',size=99,color=REL);self.add(m);m=self.change(m,'(x-1)^2-1+2',137.3,size=93);self.change(m,'(x-1)^2+1',139,size=100,color=RESULT)
 def s20(self):
  ax=self.parabola();self.add(self.left('h(x)=(x-1)^2+1',y=1.2,size=47,color=REL));self.add(Dot(ax.c2p(1,1),radius=.06,color=EXP));self.to(145)
  self.play(Indicate(self.symmetry_axis,color=WARN),run_time=1);self.to(148);self.show(self.left('h(2-x)=h(x)',y=-.4,size=53,color=EXP))
 def s21(self):
  ax=self.parabola();self.add(self.left(r'x\longmapsto2-x',y=1.2,size=63,color=EXP));seg=Line(ax.c2p(-2,0),ax.c2p(2,0),color=BASE,stroke_width=6);self.add(seg);self.to(153)
  target=Line(ax.c2p(0,0),ax.c2p(4,0),color=REL,stroke_width=6);self.add(target.copy().set_opacity(.25));self.to(155)
  reflected=seg.copy().flip(axis=UP,about_point=ax.c2p(1,0)).set_color(REL);self.play(Transform(seg,reflected),run_time=1.5);self.note('[−2,2]을 x = 1에 대해 반사하면 [0,4]')
 def s22(self):
  self.parabola();self.add(self.left(r'-2\longleftrightarrow4',y=1.2,size=66,color=BASE));self.to(159)
  self.show(self.left(r'2\longleftrightarrow0',y=-.4,size=66,color=REL));self.note('모든 대응점의 중점은 x = 1')
 def s23(self):
  ax=self.parabola();self.add(self.left('h(2-x)=h(x)',y=1.4,size=54,color=EXP));self.add(Dot(ax.c2p(-2,10),radius=.065,color=BASE),Dot(ax.c2p(4,10),radius=.065,color=BASE));self.to(163)
  self.play(Create(DashedLine(ax.c2p(-2,10),ax.c2p(4,10),color=BASE)),run_time=.7);self.show(self.left('h(-2)=h(4)=10',y=0,size=44,color=BASE),self.left('h(0)=h(2)=2',y=-1.3,size=44,color=REL))
 def s24(self):
  ax=self.parabola();a=self.area(ax,-2,2,BASE);target=self.area(ax,0,4,REL);self.add(a,target.copy().set_fill(opacity=.12))
  self.add(self.left(r'\int_{-2}^2 h(x)\,dx',y=1.3,size=56,color=BASE),self.left(r'=\int_0^4 h(x)\,dx',y=-.3,size=56,color=REL))
  reflected=a.copy().flip(axis=UP,about_point=ax.c2p(1,0)).set_fill(REL,opacity=.35);self.play(Transform(a,reflected),run_time=2);self.to(168)
  self.play(a.animate.set_fill(RESULT,opacity=.4),run_time=.8);self.note('반사는 넓이를 보존한다');self.to(170);self.note('ㄷ 참',RESULT)
 def s25(self):
  self.add(eq(r'H(x)=\frac{x^3}{3}-x^2+2x',y=1.8,size=46,color=MUTED));self.to(174)
  m=eq(r'\int_{-2}^2 h(x)\,dx=[H(x)]_{-2}^2',size=72,color=BASE);self.show(m);m=self.change(m,r'\frac83-\left(-\frac{32}{3}\right)',178,size=86,color=BASE);self.change(m,r'\frac{40}{3}',180,size=100,color=RESULT)
 def s26(self):
  m=eq(r'\int_0^4h(x)\,dx=\frac{64}{3}-16+8',size=73,color=REL);self.add(m);self.change(m,r'\int_0^4h(x)\,dx=\frac{40}{3}',183,size=83,color=RESULT);self.to(185)
  self.note('두 구간의 넓이는 모두 40/3',RESULT)
 def s27(self):
  self.add(tx('ㄱ. a = 1',-4.5,1.2,31,width=4.2),tx('ㄴ. S(3) = 6',0,1.2,31,width=4.2),tx('ㄷ. 두 넓이가 같다',4.5,1.2,31,width=4.2));self.to(191)
  self.show(tx('거짓  ×',-4.5,-.1,34,WARN,width=4.2),tx('참  ✓',0,-.1,34,RESULT,width=4.2),tx('참  ✓',4.5,-.1,34,RESULT,width=4.2));self.to(194)
  self.show(tx('정답 ⑤ · ㄴ, ㄷ',y=-1.7,size=43,color=RESULT))
 def s28(self):
  self.curves(2);self.add(self.left(r'S(t)=\int_0^t(f-g)\,dx',y=1.2,size=47,color=EXP));self.to(199)
  self.strip(.03);self.play(self.delta.animate.set_value(.45),run_time=1.5,rate_func=linear);self.to(202)
  self.play(self.delta.animate.set_value(.015),run_time=1.5,rate_func=linear);self.show(self.left("S'(t)=f(t)-g(t)",y=-.5,size=56,color=RESULT))
 def s29(self):
  ax=self.parabola();m=self.left("S'(t)=f(t)-g(t)",y=1.25,size=53,color=EXP);self.add(m);self.to(207)
  self.change(m,r'S(v)-S(u)=\int_u^v h(x)\,dx',x=-3.7,y=1.25,width=6.1,size=43,color=REL);self.add(self.area(ax,0,3,EXP));self.note('구간 끝점 u, v ≥ 0 · 높이를 적분해 넓이 계산')
 def s30(self):
  self.add(eq(r'\int_{-2}^2h(x)\,dx,\quad\int_0^4h(x)\,dx',-3.5,.8,53,MUTED,width=6),tx('직접 적분',-3.5,1.95,29,MUTED,width=6));self.to(214)
  self.show(eq('h(2-x)=h(x)',3.5,.8,55,EXP,width=6),tx('대칭성 확인',3.5,1.95,29,EXP,width=6));self.note('함수와 구간이 함께 대칭이면 계산을 줄일 수 있다')
 def s31(self):
  self.parabola();m=self.left('x^2-2x+2',y=1.1,size=62,color=REL);self.add(m);self.change(m,'(x-1)^2+1',219,x=-3.7,y=1.1,width=6.1,size=64,color=RESULT);self.to(221)
  self.play(Indicate(self.symmetry_axis,color=WARN),run_time=.8);self.note('완전제곱식에서 대칭축 x = 1이 드러난다')
 def s32(self):
  self.show(tx('① 높이 차이',-4.7,1.7,29,EXP,width=4.4),eq('f(x)-g(x)',-4.7,.3,48,EXP,width=4.4));self.to(227)
  self.show(tx('② 미분과 적분',0,1.7,29,BASE,width=4.4),eq("S'(t)=f(t)-g(t)",0,.3,41,BASE,width=4.4));self.to(230)
  self.show(tx('③ 넓이 비교',4.7,1.7,29,REL,width=4.4),eq(r'\int h(x)\,dx',4.7,.3,53,REL,width=4.4));self.note('높이 차이의 식을 중심으로 미분과 적분을 연결')
 def s33(self):
  ax=self.parabola(areas=[(-2,2,BASE),(0,4,REL)]);self.add(self.left("S'(t)=f(t)-g(t)",y=1.25,size=53,color=EXP),self.left('h(2-x)=h(x)',y=-.2,size=52,color=REL));self.to(237)
  self.show(tx('정답 ⑤ · ㄴ, ㄷ',-3.7,-1.65,36,RESULT,width=6));self.to(240)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=2)
for i in range(33):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(AreaShot,),{'shot':i,'__module__':__name__})
