"""Twenty-three independent shots, exact supplied sentence times, landscape only."""
import os,sys,json,textwrap
from pathlib import Path
from bisect import bisect_right
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import text
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
config.frame_width=16;config.frame_height=9;config.frame_rate=30
config.pixel_width=640 if os.getenv('CSAT09_PREVIEW')=='1' else 1920
config.pixel_height=360 if os.getenv('CSAT09_PREVIEW')=='1' else 1080
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
class MotionShot(Scene):
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1
  self.always_update_mobjects=True
  self.add(tx('수능 수학  /  EP.09',x=-5.6,y=3.95,size=19,color=MUTED,width=4),tx('속도와 위치',x=6.2,y=3.95,size=19,color=BASE,width=2.7))
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
  new=tx(s,y=-1.95,size=26,color=color)
  if hasattr(self,'foot'):self.play(ReplacementTransform(self.foot,new),run_time=.3)
  else:self.show(new,rt=.3)
  self.foot=new
 def relations(self):
  a=card('a+b=4',-3.4,1.7);b=card('ab=1',3.4,1.7);self.add(a,b);return a,b
 def construct(self):
  getattr(self,f's{self.shot+1:02d}')();self.to(self.info['end'])
  out=HERE/'qa';out.mkdir(exist_ok=True)
  (out/f'shot{self.shot+1:02d}_{config.pixel_width}.json').write_text(json.dumps(dict(start=self.offset,end=self.info['end'],frames=round(self.time*30),geometry_checks=self.bound_checks)),encoding='utf-8')
 def p(self,t):return t**3/3-t**2/2
 def q(self,t):return t**2/2
 def left(self,s,y=.8,color=INK,size=51):return eq(s,x=-3.9,y=y,size=size,color=color,width=6)
 def right(self,s,y=.8,color=INK,size=51):return eq(s,x=3.4,y=y,size=size,color=color,width=6.5)
 def motion(self,t=0,only_p=False,zoom=False):
  limits=[-.25,.25,.25] if zoom else [-1,5,1]
  line=NumberLine(x_range=limits,length=6.25,include_tip=True,include_numbers=False,color=MUTED,stroke_width=1.3,tip_width=.08,tip_height=.08).move_to([3.35,.25,0]);self.line=line
  labels=VGroup()
  for value in ([-.25,0,.25] if zoom else [-1,0,1,2,3,4,5]):labels.add(eq(str(value),*(line.n2p(value)+DOWN*.32)[:2],size=20,color=MUTED))
  if zoom:labels.add(tx('원점 부근 확대',3.35,2,21,MUTED,width=6))
  self.time_value=ValueTracker(t)
  pp=Dot(radius=.1,color=BASE,fill_opacity=.6,stroke_width=2.5).set_z_index(3)
  qq=Dot(radius=.055,color=EXP).set_z_index(4)
  pp.add_updater(lambda m:m.move_to(line.n2p(self.p(self.time_value.get_value()))))
  lp=eq('P',size=27,color=BASE);lp.add_updater(lambda m:m.move_to(line.n2p(self.p(self.time_value.get_value()))+UP*.43))
  group=VGroup(line,labels,pp,lp);self.dotp=pp;self.dotq=qq
  if not only_p:
   qq.add_updater(lambda m:m.move_to(line.n2p(self.q(self.time_value.get_value()))))
   lq=eq('Q',size=27,color=EXP);lq.add_updater(lambda m:m.move_to(line.n2p(self.q(self.time_value.get_value()))+DOWN*.83));group.add(qq,lq)
  counter=DecimalNumber(t,num_decimal_places=1,font_size=34,color=INK).move_to([3.7,1.45,0]);counter.add_updater(lambda m:m.set_value(self.time_value.get_value()))
  group.add(eq('t=',2.7,1.45,36),counter);self.motion_group=group;self.add(group);self.update_mobjects(0);return group
 def travel(self,end,rt=3):self.play(self.time_value.animate.set_value(end),run_time=rt,rate_func=linear)
 def relative_graph(self):
  p=lambda t,v:np.array([.6+1.8*t,-.6+.7*v,0])
  axes=VGroup(Arrow(p(0,0),p(3.4,0),buff=0,stroke_width=1.2,tip_length=.08,color=MUTED),Arrow(p(0,-1.45),p(0,3.3),buff=0,stroke_width=1.2,tip_length=.08,color=MUTED))
  f=lambda t:t*t-2*t
  curve=VMobject(color=REL,stroke_width=2.5).set_points_as_corners([p(t,f(t)) for t in np.linspace(0,3,150)])
  areas=VGroup()
  for a,b,c in [(0,2,WARN),(2,3,RESULT)]:
   coords=[p(a,0)]+[p(t,f(t)) for t in np.linspace(a,b,90)]+[p(b,0)];areas.add(Polygon(*coords,fill_color=c,fill_opacity=.2,stroke_width=0))
  labels=VGroup(eq('t',*p(3.45,0)[:2],size=19,color=MUTED),*[eq(str(t),*(p(t,0)+DOWN*.25)[:2],size=20,color=MUTED) for t in [0,2,3]],eq(r'-\frac43',*p(1,-.45)[:2],size=32,color=WARN),eq(r'+\frac43',*p(2.75,1.1)[:2],size=32,color=RESULT))
  self.add(axes,areas,curve,labels)
 def s01(self):
  n=tx('09',size=90,color=BASE);self.add(n);self.play(n.animate.scale(.4).move_to([-6.7,2.8,0]),run_time=1)
  self.motion(0);self.to(4);self.show(self.left(r'v_1(t)=t^2-t',y=1.2,color=BASE,size=49),self.left(r'v_2(t)=t',y=-.1,color=EXP,size=49));self.to(7)
  self.show(tx('다시 같은 위치에 도달하는 양수 k',y=-1.85,size=29,color=REL))
 def s02(self):
  self.show(tx('주어진 정보: 속도',-3.6,1.7,29,BASE,width=6),eq(r'v_1(t),\ v_2(t)',-3.6,.5,56,BASE,width=6));self.to(14)
  self.show(tx('구하려는 조건: 같은 위치',3.6,1.7,29,REL,width=6),eq('p(k)=q(k)',3.6,.5,57,REL,width=6));self.to(17)
  self.play(Circumscribe(eq('p(k)=q(k)',3.6,.5,57,REL,width=6),color=REL),run_time=.8);self.note('속도는 순간적인 변화율, 위치는 누적된 결과')
 def s03(self):
  self.motion(0);self.add(self.left(r'v(t)=\frac{dx}{dt}',y=1.3,color=BASE,size=48));self.to(23)
  self.show(self.left(r'x(t)-x(0)=\int_0^t v(s)\,ds',y=-.05,color=REL,size=41));self.to(25)
  self.show(eq('p(0)=q(0)=0',y=-1.8,size=49,color=EXP))
 def s04(self):
  a=eq(r'\int_0^k v_1(t)\,dt',-3.2,.6,64,BASE,width=6);b=eq(r'\int_0^k v_2(t)\,dt',3.2,.6,64,EXP,width=6);self.add(a);self.to(32)
  self.show(b,eq('=',y=.6,size=64));self.note('p(0) = q(0) = 0이므로 위치 변화량을 비교한다')
 def s05(self):
  m=eq(r'\int_0^k v_1(t)\,dt=\int_0^k v_2(t)\,dt',y=.65,size=62);self.add(m)
  target=eq(r'\int_0^k v_1(t)\,dt-\int_0^k v_2(t)\,dt=0',y=.65,size=60,color=REL);self.play(TransformMatchingTex(m,target),run_time=1);self.to(38)
  self.play(TransformMatchingTex(target,eq(r'\int_0^k[v_1(t)-v_2(t)]\,dt=0',y=.65,size=66,color=REL)),run_time=1);self.note('두 번의 적분 → 속도 차이를 한 번 적분')
 def s06(self):
  a=eq(r'v_1(t)=t^2-t',-3.4,1.4,53,BASE,width=6);b=eq(r'v_2(t)=t',3.4,1.4,53,EXP,width=6);self.add(a,b);self.to(43)
  m=eq(r'(t^2-t)-t',y=-.1,size=72);self.show(m);self.to(45)
  m=self.morph(m,eq(r't^2-2t',y=-.1,size=78,color=REL));self.to(48)
  self.morph(m,eq(r'v_1(t)-v_2(t)=t^2-2t',y=-.1,size=64,color=REL))
 def s07(self):
  self.relative_graph();self.add(self.left(r'p(k)-q(k)',y=1.3,color=REL,size=57));self.to(52)
  self.show(self.left(r'\int_0^k(t^2-2t)\,dt=0',y=-.2,color=REL,size=45));self.note('적분이 0 → 위치 차이가 0  ·  각 점이 원점이라는 뜻은 아님',WARN)
 def s08(self):
  m=eq(r'\int_0^k(t^2-2t)\,dt',y=1.1,size=69,color=REL);self.add(m);self.to(57)
  self.show(eq(r't^2\ \longrightarrow\ \frac{t^3}{3}',-3.5,-.65,53,BASE,width=6));self.to(60)
  self.show(eq(r'-2t\ \longrightarrow\ -t^2',3.5,-.65,53,EXP,width=6));self.to(61.5)
  self.play(*[FadeOut(o) for o in list(self.mobjects) if isinstance(o,MathTex)],FadeIn(eq(r'\left[\frac{t^3}{3}-t^2\right]_0^k',y=.55,size=80,color=REL)),run_time=.7)
 def s09(self):
  m=eq(r'\left[\frac{t^3}{3}-t^2\right]_0^k=0',y=.65,size=74,color=REL);self.add(m)
  self.to(64);m=self.morph(m,eq(r'\left(\frac{k^3}{3}-k^2\right)-(0)=0',y=.65,size=68,color=REL));self.to(68)
  self.morph(m,eq(r'\frac{k^3}{3}-k^2=0',y=.65,size=79,color=REL));self.note('위끝값의 함수값 − 아래끝값의 함수값')
 def s10(self):
  m=eq(r'\frac{k^3}{3}-k^2=0',y=.7,size=80,color=REL);self.add(m);self.play(Indicate(m,color=EXP),run_time=1);self.to(73)
  self.morph(m,eq(r'k^2\left(\frac{k}{3}-1\right)=0',y=.7,size=80,color=REL));self.note('공통인수 k²으로 묶는다')
 def s11(self):
  a=card('k=0',-3.5,.75,WARN,width=4);b=card('k=3',3.5,.75,EXP,width=4);self.add(a,b);self.to(78)
  self.show(tx('출발 시각',-3.5,-.35,28,WARN,width=5),tx('출발 이후',3.5,-.35,28,EXP,width=5));self.to(81)
  self.play(Create(Cross(a,stroke_color=WARN,stroke_width=3)),Indicate(b,color=RESULT),run_time=.8);self.note('문제는 출발 이후의 양수 k를 요구한다',WARN)
 def s12(self):
  self.motion(2.6);self.add(self.left('k=3',y=1.1,color=RESULT,size=85));self.travel(3,1.2);self.to(86)
  self.show(tx('정답 ③',-3.9,-.5,32,RESULT,width=6),eq(r'p(3)=q(3)=\frac92',3.35,-1.5,43,RESULT,width=6),rt=.5)
 def s13(self):
  m=eq(r'v_1(t)=t^2-t',y=1.2,size=63,color=BASE);self.add(m);self.to(90)
  m=self.morph(m,eq(r'p(t)=\int_0^t(s^2-s)\,ds',y=.6,size=63,color=BASE));self.to(94)
  self.morph(m,eq(r'p(t)=\frac{t^3}{3}-\frac{t^2}{2}',y=.6,size=76,color=BASE))
 def s14(self):
  self.add(eq(r'p(t)=\frac{t^3}{3}-\frac{t^2}{2}',-3.7,.65,53,BASE,width=6));m=eq(r'q(t)=\int_0^t s\,ds',3.7,.65,53,EXP,width=6);self.add(m)
  self.morph(m,eq(r'q(t)=\frac{t^2}{2}',3.7,.65,64,EXP,width=6))
 def s15(self):
  self.add(eq('p(k)=q(k)',y=1.8,size=44,color=REL));m=eq(r'\frac{k^3}{3}-\frac{k^2}{2}=\frac{k^2}{2}',y=.2,size=79);self.add(m)
  self.to(103);m=self.morph(m,eq(r'\frac{k^3}{3}-\frac{k^2}{2}-\frac{k^2}{2}=0',y=.2,size=71,color=REL));self.to(105)
  self.morph(m,eq(r'\frac{k^3}{3}-k^2=0',y=.2,size=80,color=REL));self.note('속도 차이 적분과 같은 방정식')
 def s16(self):
  self.show(tx('각각 적분',-3.6,1.6,30,MUTED,width=6),tx('차이를 적분',3.6,1.6,30,REL,width=6),eq(r'\int_0^k v_1\,dt,\ \int_0^k v_2\,dt',-3.6,.35,43,MUTED,width=6),eq(r'\int_0^k(v_1-v_2)\,dt',3.6,.35,51,REL,width=6));self.to(110)
  self.show(tx('두 위치함수 계산',-3.6,-1.1,27,MUTED,width=6),tx('위치 차이를 직접 계산',3.6,-1.1,27,REL,width=6));self.note('이번 문제에서는 한 번의 적분으로 계산 가능',REL)
 def s17(self):
  self.note('위치가 같음 ≠ 속도가 같음',WARN);self.to(114)
  self.show(tx('속도가 같음',-3.5,1.3,30,WARN,width=6),tx('위치가 같음',3.5,1.3,30,REL,width=6));self.to(117)
  self.show(eq(r'v_1(t)=v_2(t)',-3.5,-.1,60,WARN,width=6),eq('p(t)=q(t)',3.5,-.1,60,REL,width=6))
 def s18(self):
  self.motion(2);m=self.left('t^2-t=t',y=1.25,color=WARN,size=58);self.add(m);m=self.morph(m,self.left('t(t-2)=0',y=1.25,color=WARN,size=58));self.to(122)
  m=self.morph(m,self.left(r't=0,\quad t=2',y=1.25,color=WARN,size=55));self.show(self.left(r'p(2)=\frac23,\quad q(2)=2',y=-.15,color=REL,size=44))
  self.show(tx('v₁(2) = v₂(2) = 2',3.35,-1.5,27,WARN,width=6));self.play(Create(DashedLine(self.line.n2p(self.p(2))+UP*.75,self.line.n2p(self.q(2))+UP*.75,color=REL,dash_length=.06)),run_time=.6)
 def s19(self):
  self.motion(2);self.add(self.left(r't:2\longrightarrow3',y=1.3,color=REL,size=55));self.travel(3,3.5);self.to(129)
  self.show(self.left(r'p(3)=q(3)=\frac92',y=-.2,color=RESULT,size=53));self.to(131)
  self.show(tx('t = 2: 속도 같음',-3.9,-1.65,25,WARN,width=6),tx('t = 3: 위치 같음',3.35,-1.65,25,RESULT,width=6))
 def s20(self):
  self.motion(0,only_p=True,zoom=True);self.add(self.left(r'v_1(t)=t(t-1)',y=1.3,color=BASE,size=52));self.to(136)
  self.travel(1,2.5);self.to(139)
  self.show(self.left(r'0<t<1\Rightarrow v_1(t)<0',y=.05,color=WARN,size=43));self.play(Create(Arrow(self.line.n2p(0)+DOWN*1.1,self.line.n2p(-1/6)+DOWN*1.1,color=WARN,buff=0,tip_length=.12)),run_time=.6)
  self.to(142);self.show(self.left(r'\int_0^t v_1(s)\,ds',y=-1.25,color=REL,size=58),tx('위치 변화량은 부호를 유지한다',3.35,-1.75,25,WARN,width=6))
 def s21(self):
  m=eq(r'v_1(t)-v_2(t)=t^2-2t',y=1.1,size=64,color=REL);self.add(m);self.to(149)
  m=self.morph(m,eq(r'\int_0^k(t^2-2t)\,dt',y=.8,size=72,color=REL));self.to(152)
  m=self.morph(m,eq(r'\int_0^k(t^2-2t)\,dt=0',y=.8,size=72,color=REL));self.note('초기 위치가 같고 k > 0이므로 k = 3',RESULT)
 def s22(self):
  self.show(tx('t = 2',-3.6,1.3,38,WARN,width=6),tx('속도가 같아짐',-3.6,.2,29,WARN,width=6),tx('t = 3',3.6,1.3,38,RESULT,width=6),tx('위치가 같아짐',3.6,.2,29,RESULT,width=6));self.to(158)
  self.show(eq('k>0',y=-1.2,size=67,color=RESULT));self.note('문제가 묻는 조건과 출발 시각 포함 여부를 확인')
 def s23(self):
  self.add(eq(r'\int_0^k(v_1-v_2)\,dt=0',y=1.3,size=57,color=REL),eq('k=3',y=-.1,size=91,color=RESULT),tx('정답 ③',y=-1.6,size=32,color=RESULT));self.to(163.5)
  self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.caption],run_time=.5)
for i in range(23):globals()[f'Shot{i+1:02d}']=type(f'Shot{i+1:02d}',(MotionShot,),{'shot':i,'__module__':__name__})
