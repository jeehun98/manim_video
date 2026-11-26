"""104-second, native 4K landscape prologue. One replaceable shot per claim."""
import os,sys,json,math
from bisect import bisect_right
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]))
from quantum_series.shared.theme import text,FONT
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
PREVIEW=os.getenv('QCS_PREVIEW')=='1'
config.frame_width,config.frame_height=16,9
config.pixel_width,config.pixel_height=(960,540) if PREVIEW else (3840,2160)
config.frame_rate=30
config.background_color='#0B1019'
INK,MUTED,GOLD,BLUE,VIOLET,GREEN='#E8EDF4','#94A3B8','#F4D58D','#60A5FA','#A78BFA','#4ADE80'

def t(s,x=0,y=0,size=28,color=INK,width=14.5):return text(s,x,y,size,color,width)
def e(s,x=0,y=0,size=45,color=INK,width=14.5):
 m=MathTex(s,font_size=size,color=color,substrings_to_isolate=[r'\pi'])
 m.set_color_by_tex(r'\pi',GOLD)
 if m.width>width:m.scale_to_fit_width(width)
 return m.move_to([x,y,0])
def box(title,formula,x,y,color=BLUE,w=3.8,h=1.1):
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.1,color=color,stroke_width=1.3,fill_color=color,fill_opacity=.055),t(title,y=.24,size=21,color=color,width=w-.25),e(formula,y=-.18,size=30,width=w-.25)).move_to([x,y,0])
def pi_center(size=108):return VGroup(Circle(radius=.75,color=GOLD,stroke_width=1.4,fill_color=GOLD,fill_opacity=.025),e(r'\pi',size=size)).move_to([0,.25,0])
def geometry(x=0,y=0,r=.75):
 return VGroup(Circle(radius=r,color=BLUE),Line([-r,0,0],[r,0,0],color=GOLD)).move_to([x,y,0])
def complex_icon(x=0,y=0,r=.6):
 circle=Circle(radius=r,color=VIOLET,stroke_width=1.5)
 return VGroup(circle,Line([0,0,0],[r*math.cos(2.2),r*math.sin(2.2),0],color=GOLD),Dot(circle.point_at_angle(2.2),radius=.045,color=GOLD)).move_to([x,y,0])
def waves(x=0,y=0):
 return VGroup(*[FunctionGraph(lambda u,k=k:.18*math.sin(k*u),x_range=[-1,1,.03],color=VIOLET,stroke_width=1.5).shift(DOWN*i*.28) for i,k in enumerate([2,5,8])]).move_to([x,y,0])
def gaussian(x=0,y=0):
 return FunctionGraph(lambda u:.75*math.exp(-u*u*2),x_range=[-1.3,1.3,.02],color=GREEN,stroke_width=1.8).move_to([x,y,0])
def network(six=False,structured=False):
 center=pi_center()
 positions=[(-5,1.7),(5,1.7),(-5,-1.55),(5,-1.55)]
 names=['기하학','복소지수함수','푸리에 해석','확률론']
 colors=[BLUE,VIOLET,VIOLET,GREEN]
 icons=[geometry(r=.48),complex_icon(r=.48),waves().scale(.7),gaussian().scale(.65)]
 if six:
  positions=[(-5,1.75),(0,2.0),(5,1.75),(-5,-1.65),(0,-1.7),(5,-1.65)]
  names=['기하학','해석학','복소지수함수','대수적 성질','계산과 분포','확률론']
  colors=[BLUE,BLUE,VIOLET,VIOLET,BLUE,GREEN]
  icons=[geometry(r=.42),e(r'\int\ \sum',size=45,color=BLUE),complex_icon(r=.42),e(r'P(\pi)\ne0',size=33),e(r'3.141592\ldots',size=28),gaussian().scale(.6)]
 links=VGroup(*[Line(center.get_center(),[x,y,0],color=c,stroke_opacity=.42,stroke_width=1.1) for (x,y),c in zip(positions,colors)])
 nodes=VGroup()
 for (x,y),name,c,icon in zip(positions,names,colors,icons):
  icon.move_to([x,y+.1,0]);nodes.add(VGroup(icon,t(name,x,y-.7,20,c,width=3.5)))
 if structured:
  links.add(DashedLine([-4.5,1.7,0],[4.5,1.7,0],path_arc=-.4,color=MUTED,stroke_opacity=.3),DashedLine([-4.5,-1.55,0],[4.5,-1.55,0],path_arc=.4,color=MUTED,stroke_opacity=.3))
 return VGroup(links,center,nodes)

class PiScene(Scene):
 replace=Scene.replace
 shot=0
 def setup(self):
  self.info=DATA['scenes'][self.shot];self.offset=self.info['start'];self.caption_index=-1;self.records=[];self.bounds=[]
  self.header=VGroup(t('CHAPTER 00  /  THE STRUCTURE OF π',-4.7,4.05,17,MUTED,width=6),t('원주율은 왜 중요한 수인가',5,4.05,17,MUTED,width=5),Line([-7.2,3.7,0],[7.2,3.7,0],color=MUTED,stroke_width=1,stroke_opacity=.3))
  self.title=t(self.info['title'],y=3.23,size=29)
  self.panel=Rectangle(width=15.3,height=1.32,fill_color=config.background_color,fill_opacity=1,stroke_width=0).move_to([0,-3.65,0]).set_z_index(39)
  self.caption=VGroup().set_z_index(40);self.add(self.header,self.title,self.panel,self.caption);self.update_caption(self.caption);self.caption.add_updater(self.update_caption)
 def update_caption(self,mob,dt=0):
  now=self.offset+self.time;index=bisect_right([r['start'] for r in DATA['sentences']],now+1e-7)-1
  if index==self.caption_index:return
  self.caption_index=index;lines=[];line=''
  for word in DATA['sentences'][index]['text'].split():
   if line and len(line)+len(word)+1>72:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  lines.append(line);cap=Text('\n'.join(lines),font=FONT,font_size=25,color=INK,line_spacing=1.05)
  if cap.width>14.4:cap.scale_to_fit_width(14.4)
  if cap.height>1.1:cap.scale_to_fit_height(1.1)
  cap.move_to([0,-3.65,0]);mob.become(cap).set_z_index(40)
  self.records.append(dict(sentence=index+1,at=round(now,6),lines=len(lines),left=cap.get_left()[0],right=cap.get_right()[0],bottom=cap.get_bottom()[1],top=cap.get_top()[1]))
 def to(self,target):
  assert target<=self.info['end']+1e-6
  endpoints=[r['start'] for r in DATA['sentences'] if self.offset+self.time+1e-6<r['start']<target]+[target]
  for end in endpoints:
   frames=round((end-self.offset-self.time)*30)
   if frames<0:raise RuntimeError(f'{self.info["id"]}: overrun {self.offset+self.time}>{end}')
   if frames:self.wait(frames/30,frozen_frame=True)
   self.update_caption(self.caption)
 def show(self,*mobs,run_time=.6):self.play(*[FadeIn(m) for m in mobs],run_time=run_time)
 def clear_board(self):
  keep=[self.header,self.title,self.caption,self.panel];m=[o for o in self.mobjects if o not in keep]
  if m:self.play(*[FadeOut(o) for o in m],run_time=.35)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.clear_updaters()
  for m in self.mobjects:
   if m in [self.caption,self.panel] or not m.width or not m.height:continue
   assert m.get_left()[0]>=-7.8 and m.get_right()[0]<=7.8,(self.info['id'],m)
   assert m.get_bottom()[1]>=-2.8 and m.get_top()[1]<=4.35,(self.info['id'],m)
  audit=Path(os.environ['QCS_AUDIT_DIR']);audit.mkdir(parents=True,exist_ok=True);(audit/(self.info['id']+'.json')).write_text(json.dumps(self.records),encoding='utf-8')

class Shot01(PiScene):
 shot=0
 def s01(self):
  line=NumberLine(x_range=[-2,8,1],length=13,include_numbers=True,font_size=22,color=MUTED).move_to([0,-.6,0]);self.play(Create(line),run_time=.6)
  for value,s,y in [(0,'0',.4),(1,'1',.9),(2,'2',1.4),(math.e,'e',2),(PI,r'\pi',.5)]:
   point=line.n2p(value);self.show(Dot(point,color=GOLD,radius=.045),DashedLine(point,point+UP*y,color=GOLD,stroke_opacity=.3),e(s,x=point[0],y=point[1]+y+.25,size=40,color=GOLD),run_time=.25)
  self.show(t('수많은 수 중에서 특별히 주목받는 수',y=-2,size=25));self.to(4)

class Shot02(PiScene):
 shot=1
 def s02(self):
  left=Ellipse(width=7,height=3.5,color=BLUE,fill_color=BLUE,fill_opacity=.05).move_to([-2,0,0]);right=Ellipse(width=7,height=3.5,color=VIOLET,fill_color=VIOLET,fill_opacity=.05).move_to([2,0,0]);self.show(left,right,t('짝수',-4,1.4,28,BLUE),t('소수',4,1.4,28,VIOLET))
  evens=VGroup(*[e(str(n),x=x,y=y,size=41,color=MUTED) for n,x,y in [(4,-4,.5),(6,-2.8,.6),(8,-4,-.6),(10,-2.5,-.7),(12,-2,.1)]]);primes=VGroup(*[e(str(n),x=x,y=y,size=41,color=MUTED) for n,x,y in [(3,2.5,.6),(5,4,.5),(7,2.8,-.6),(11,4.2,-.7)]])
  self.show(evens,primes);two=e('2',size=103,color=GOLD);self.show(two);self.play(Circumscribe(two,color=GOLD),run_time=.7);self.show(e(r'\mathbb P\cap2\mathbb N=\{2\}',y=-2.35,size=44),t('가장 작은 소수 · 유일한 짝수 소수',y=2.4,size=28,color=GOLD));self.to(11)

class Shot03(PiScene):
 shot=2
 def s03(self):
  center=VGroup(Circle(radius=.7,color=GOLD),e('2',size=95,color=GOLD));self.add(center)
  cards=VGroup(box('가장 작은 소수',r'\min\mathbb P=2',-4.7,1.3,BLUE),box('유일한 짝수 소수',r'\mathbb P\cap2\mathbb N=\{2\}',4.7,1.3,VIOLET),box('짝수의 기준',r'n\equiv0\pmod2',-4.7,-1.4,BLUE),box('홀수의 기준',r'n\equiv1\pmod2',4.7,-1.4,VIOLET))
  for c in cards:self.play(Create(Line(ORIGIN,c.get_center(),color=MUTED,stroke_width=1)),FadeIn(c),run_time=.55)
  self.to(17)

class Shot04(PiScene):
 shot=3
 def s04(self):
  old=e('2',x=-2,size=110,color=MUTED);self.add(old);new=e(r'\pi',x=2,size=135);self.play(TransformFromCopy(old,new),old.animate.set_opacity(.2),run_time=.9);self.to(19)

class Shot05(PiScene):
 shot=4
 def s05(self):
  p=pi_center();self.add(p)
  formulas=[e(r'C=2\pi r',-4.8,1.3,55),e(r'A=\pi r^2',4.8,1.3,55),e(r'V=\frac43\pi r^3',-4.8,-1.25,55),e(r'S=4\pi r^2',4.8,-1.25,55)]
  self.play(LaggedStart(*[FadeIn(m) for m in formulas],lag_ratio=.2),run_time=1.5);self.show(e(r'3.14159265358979323846\ldots',y=-2.35,size=37,color=MUTED));self.to(24)

class Shot06(PiScene):
 shot=5
 def s06(self):
  self.show(e(r'\pi',y=.6,size=143),t('원주율은 왜 중요한 수인가?',y=-1.5,size=37));self.to(29)

class Shot07(PiScene):
 shot=6
 def s07(self):
  c=geometry(-4,.6,1);self.show(c,e('d',-4,.3,35,color=BLUE));L=TAU
  arc=Circle(radius=1,color=GOLD).move_to([-4,.6,0]);self.add(arc)
  def unroll(m,a):
   angle=max(TAU*(1-a),.001);r=L/angle;cx=-4*(1-a)+2*a;base=-.4
   m.become(ParametricFunction(lambda u:np.array([cx+r*np.sin(angle*u),base+r*(np.cos(angle*u)-np.cos(angle/2)),0]),t_range=[-.5,.5,.005],color=GOLD))
  self.play(UpdateFromAlphaFunc(arc,unroll),run_time=1.4)
  self.show(e(r'\pi=\frac Cd',y=-1.65,size=68),t('지름 약 3.14159배의 둘레',2,.15,25,GOLD));self.to(33)

class Shot08(PiScene):
 shot=7
 def s08(self):
  g=geometry(-4,0,1.2);self.add(g);target=complex_icon(4,0,1.2)
  axes=Axes(x_range=[-1.5,1.5,1],y_range=[-1.5,1.5,1],x_length=3.6,y_length=3.6,tips=False,axis_config=dict(stroke_opacity=.4)).move_to([4,0,0]);self.show(axes)
  self.play(TransformFromCopy(g,target),GrowArrow(Arrow([-1.5,0,0],[1.5,0,0],color=MUTED)),run_time=1.2);self.show(t('기하학적 대상',-4,-2,25,BLUE),t('복소지수함수',4,-2,25,VIOLET));self.to(37)

class Shot09(PiScene):
 shot=8
 def s09(self):
  center=np.array([-3.7,.2,0]);circle=Circle(radius=1.6,color=VIOLET).move_to(center);dot=Dot(center+RIGHT*1.6,color=GOLD);radius=always_redraw(lambda:Line(center,dot.get_center(),color=GOLD));self.add(circle,dot,radius)
  self.show(e(r'e^{i\theta}=\cos\theta+i\sin\theta',3,.9,47,width=7),e(r'e^{i\pi}=-1',3,-.8,64));self.play(MoveAlongPath(dot,Arc(radius=1.6,start_angle=0,angle=PI).shift(center)),run_time=2);radius.clear_updaters();self.to(41)

class Shot10(PiScene):
 shot=9
 def s10(self):
  f=lambda x:math.sin(x)+.45*math.sin(3*x)+.25*math.sin(5*x)
  total=FunctionGraph(f,x_range=[-PI,PI,.025],color=GOLD).scale(.65).move_to([0,1.4,0]);self.show(total)
  components=VGroup(*[FunctionGraph(lambda x,n=n,a=a:a*math.sin(n*x),x_range=[-PI,PI,.025],color=co).scale(.48).move_to([x,-.5,0]) for n,a,co,x in [(1,1,BLUE,-5),(3,.45,VIOLET,0),(5,.25,GREEN,5)]])
  self.play(TransformFromCopy(total,components),run_time=1);self.show(e(r'f(\theta)=\sin\theta+0.45\sin3\theta+0.25\sin5\theta',y=-1.6,size=36),e(r'c_n=\frac1{2\pi}\int_0^{2\pi}f(\theta)e^{-in\theta}\,d\theta',y=-2.2,size=29));self.to(45)

class Shot11(PiScene):
 shot=10
 def s11(self):
  ax=Axes(x_range=[-3.5,3.5,1],y_range=[0,.5,.1],x_length=6.3,y_length=3,tips=False,axis_config=dict(stroke_opacity=.4)).move_to([-3.7,.2,0]);curve=ax.plot(lambda x:math.exp(-x*x/2)/math.sqrt(TAU),color=GREEN)
  self.show(ax,curve);area=ax.get_area(curve,x_range=[-3.5,3.5],color=GREEN,opacity=.15);self.play(FadeIn(area),run_time=.6)
  self.show(t('표준정규분포',3.3,1.4,30,GREEN),e(r'f(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2}',3.3,.25,48,width=7),e(r'\int_{-\infty}^{\infty}f(x)\,dx=1',3.3,-1.25,40));self.to(49)

class Shot12(PiScene):
 shot=11
 def s12(self):
  g=network();self.add(g[2]);self.play(Create(g[0]),FadeIn(g[1]),run_time=1.3);self.to(54)

class Shot13(PiScene):
 shot=12
 def s13(self):
  n=e('17',y=1.6,size=100,color=MUTED);self.show(n)
  formulas=VGroup(*[e(s,x=x,y=y,size=39,color=MUTED) for s,x,y in [('17=20-3',-5,.1),('17=10+7',0,.1),('17=34/2',5,.1),('17=16+1',-5,-1.15),(r'17=\sqrt{289}',0,-1.15),('17=51/3',5,-1.15)]]);self.play(LaggedStart(*[FadeIn(m) for m in formulas],lag_ratio=.1),run_time=1.2);self.show(t('수식의 개수만으로 중요성을 설명할 수는 없다',y=-2.45,size=26,color=MUTED));self.to(60)

class Shot14(PiScene):
 shot=13
 def s14(self):
  g=network(structured=True);self.add(g[2]);self.play(Create(g[0]),FadeIn(g[1]),run_time=1.3)
  self.show(t('회전',0,2.45,24,VIOLET),t('주기성 · 직교성',0,-2.3,24,VIOLET),t('연결의 성립 이유를 탐구한다',0,1.6,24,MUTED));self.to(67)

class Shot15(PiScene):
 shot=14
 def s15(self):
  geo=geometry(-5,1,.55);self.add(geo);self.show(e(r'\frac Cd',-5,-.1,43),e(r'3.141592\ldots',-5,-1.1,29,color=GOLD),run_time=.4);self.to(69)
  ax=Axes(x_range=[0,4,1],y_range=[-.8,1.2,.5],x_length=4,y_length=1.9,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([0,.8,0]);limit=ax.plot(math.sin,x_range=[0,4,.02],color=MUTED,stroke_opacity=.4);self.show(ax,limit,run_time=.3)
  partial=lambda count:ax.plot(lambda x:sum((-1)**n*x**(2*n+1)/math.factorial(2*n+1) for n in range(count)),x_range=[0,3.6,.025],color=VIOLET)
  curve=partial(3);self.add(curve)
  for count in [4,5,8]:self.play(Transform(curve,partial(count)),run_time=.35)
  self.show(Dot(ax.c2p(PI,0),color=GOLD,radius=.045),e(r'S(x)=\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n+1}}{(2n+1)!}',0,-.7,27),e(r'\min\{x>0:S(x)=0\}',0,-1.45,27),t('유한합은 근사 · 정의는 무한급수 S',0,-2.25,17,MUTED,width=5),run_time=.3);self.to(72)
  b=Axes(x_range=[0,1,.25],y_range=[0,1.1,.5],x_length=3.7,y_length=1.8,tips=False,axis_config=dict(stroke_opacity=.3)).move_to([5,.8,0]);f=b.plot(lambda x:1/(1+x*x),color=GREEN);rects=b.get_riemann_rectangles(f,x_range=[0,1],dx=.2,color=GREEN,fill_opacity=.25,stroke_width=.5)
  self.show(b,f,rects,run_time=.4);finer=b.get_riemann_rectangles(f,x_range=[0,1],dx=.05,color=GREEN,fill_opacity=.25,stroke_width=.5);self.play(Transform(rects,finer),run_time=.6)
  self.show(e(r'4\int_0^1\frac{dx}{1+x^2}',5,-.6,35),e(r'3.141592\ldots',5,-1.55,29,color=GOLD),run_time=.3);self.to(74.5)
  sources=VGroup(e(r'3.141592\ldots',-5,-1.1,29,color=GOLD),e(r'3.141592\ldots',0,-1.85,29,color=GOLD),e(r'3.141592\ldots',5,-1.55,29,color=GOLD));self.add(sources)
  back=[m for m in self.mobjects if m not in [self.header,self.title,self.caption,self.panel,sources]];self.play(*[FadeOut(m) for m in back],ReplacementTransform(sources,e(r'\pi',y=.5,size=112)),run_time=1);self.to(77)

class Shot16(PiScene):
 shot=15
 def s16(self):
  p=e(r'\pi',size=105);self.add(p)
  pictures=VGroup(geometry(-5,0,1),complex_icon(0,0,1),VGroup(*[box('',s,x,0,GOLD if s=='F' else MUTED,.65,.75) for s,x in zip('243F6A',[3.2,3.95,4.7,5.45,6.2,6.95])]))
  self.play(ReplacementTransform(p,pictures),run_time=.7)
  self.show(e(r'\pi=\frac Cd',-5,1.9,39),e(r'e^{i\pi}=-1',0,1.9,39),e(r'\pi=\sum_{k=0}^{\infty}\frac{B_k}{16^k}',5,1.9,33,width=4.8))
  self.show(t('기하학적 관계',-5,-1.65,24,BLUE),t('복소수의 회전',0,-1.65,24,VIOLET),t('16진수의 특정 자릿수 추출',5,-1.65,23,GOLD,width=4.8),t('Bₖ: BBP 공식의 네 유리수 항 조합',5,-2.45,16,MUTED,width=4.8));self.to(82)

class Shot17(PiScene):
 shot=16
 def s17(self):
  p=pi_center(143).scale(1.3);value=e(r'3.14159265358979\ldots',y=-1.35,size=40,color=MUTED);self.add(p,value);self.to(85)
  target=network(six=True);self.play(ReplacementTransform(p,target[1]),FadeOut(value),run_time=.6)
  for link,node in zip(target[0],target[2]):self.play(Create(link),FadeIn(node),run_time=.42)
  self.to(90)

class Shot18(PiScene):
 shot=17
 def s18(self):
  g=network(six=True);self.add(g)
  for node in [g[2][0],g[2][1],g[2][4],g[2][3]]:self.play(Indicate(node,scale_factor=1.08,color=GOLD),run_time=.65)
  self.show(t('연결선은 탐구할 관계를 나타내며 논리적 함의를 뜻하지 않는다',y=-2.6,size=18,color=MUTED));self.to(98)

class Shot19(PiScene):
 shot=18
 def s19(self):
  g=network(six=True);self.add(g);self.play(g[0].animate.set_stroke(opacity=.22),g[2].animate.set_opacity(.14),g[1].animate.scale(1.3).move_to([0,.9,0]),run_time=1.3);self.to(101)
  self.play(FadeOut(self.title),g[2].animate.scale(.7),run_time=.6);self.to(102)
  self.show(t('원주율은 왜 중요한 수인가',y=-1.1,size=42),run_time=.5);self.to(103)
  self.show(t('하나의 수학적 대상을 이해한다는 것',y=-2.15,size=27,color=MUTED),run_time=.5);self.to(104)
