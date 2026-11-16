"""Benford digit frequencies as lengths of a shared logarithmic ruler."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text
from episodes.energy01_force_gradient import tex_compat
from episodes.benford01_log_intervals.model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
TEAL,ORANGE,PURPLE,BLUE,MUTED='#20D6B0','#FFAC55','#A78BFA','#80A8FF','#8396B8'
TOY=['1532','8.41','729','0.0046','92.7','18300','21.5','306','47.8','5800','6.02','0.071','85','910','12.6','0.23','34400','4.2','597','6100','76.5','8320','0.0094','145','29.8','360','482','5.01','65','701','8900','0.012','930','246','37.1','4200','56.7','688','72','10900','0.008','19.6','9500','312','41.9']
def dc(d):return TEAL if d==1 else ORANGE if d==9 else BLUE
class BenfordGeometry(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup();self.offset=self.info['start']
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  벤포드 법칙',y=7.15,size=18,color=MUTED))
 def numbers(self,small=False):
  g=VGroup()
  for i,s in enumerate(TOY):
   m=Text(s,font='Malgun Gothic',font_size=19,color=WHITE,disable_ligatures=True)
   if m.width>1.16:m.scale_to_fit_width(1.16)
   idx=next(j for j,c in enumerate(s) if c in '123456789');m[idx].set_color(dc(int(s[idx])));m.move_to([-2.9+1.45*(i%5),3.8-.5*(i//5),0]);g.add(m)
  return g
 def histogram(self,values=P,y=.2,height=3.15,maximum=.35,labels=True):
  g=VGroup(Line([-3.4,y,0],[3.4,y,0],color=MUTED,stroke_width=1))
  for d,p in enumerate(values,1):
   x=-3+.75*(d-1);h=float(p)/maximum*height
   g.add(Rectangle(width=.45,height=max(.006,h),fill_color=dc(d),fill_opacity=.8,stroke_width=0).move_to([x,y+h/2,0]),text(str(d),x=x,y=y-.35,size=23,color=dc(d)))
   if labels:g.add(text(f'{p*100:.1f}%',x=x,y=y+h+.2,size=17,color=dc(d),width=.72))
  for v in ([0,.1,.2,.3] if maximum==.35 else [0,.5,1]):g.add(text(f'{v*100:.0f}%',x=-3.8,y=y+height*v/maximum,size=17,color=MUTED,width=.55))
  return g
 def ruler(self,y=2.6,log=True,scale=1,high=None):
  g=VGroup();positions=np.log10(np.arange(1,11)) if log else np.arange(10)/9
  for d in range(1,10):
   left,right=-3.5+7*positions[d-1],-3.5+7*positions[d];c=dc(d) if d in [1,9] else (PURPLE if log else BLUE);alpha=.65 if high is None or d in high else .13
   g.add(Rectangle(width=right-left,height=.42,stroke_width=1,stroke_color='#0B1020',fill_color=c,fill_opacity=alpha).move_to([(left+right)/2,y,0]))
  for i,pos in enumerate(positions):
   x=-3.5+7*pos;ly=y-.52-(.43 if (i+1)%2==0 else 0)
   g.add(Line([x,y-.23,0],[x,y-.34,0],color=MUTED,stroke_width=1),text(str((i+1)*scale),x=x,y=ly,size=20,color=dc(i+1) if i<9 else WHITE,width=.75))
  return g
 def marker(self,u,y=2.6,color=WHITE):return Triangle(fill_color=color,fill_opacity=1,stroke_width=0).scale(.09).rotate(PI).move_to([-3.5+7*(u%1),y+.48,0])
 def compare_row(self,start,end,t,y,color):
  duration=travel(start,end);u=min(t,duration);value=growth(u,start);fraction=(value-start)/(end-start)
  return VGroup(Line([-3,y,0],[3,y,0],color=MUTED,stroke_width=1.3),Dot([-3+6*fraction,y,0],radius=.07,color=color),Rectangle(width=max(.006,4.5*u/TWO_TIME),height=.14,stroke_width=0,fill_color=color,fill_opacity=.6).move_to([-3+2.25*u/TWO_TIME,y-.72,0]))
 def time_rows(self,a=1,b=9):
  self.ta=ValueTracker(0);self.tb=ValueTracker(0)
  for start,end,tracker,y,c in [(a,2*a,self.ta,3,TEAL),(b,b*10/9,self.tb,.65,ORANGE)]:
   self.add(always_redraw(lambda start=start,end=end,tr=tracker,y=y,c=c:self.compare_row(start,end,tr.get_value(),y,c)),text(f'{start:g} → {end:g}',x=-2.1,y=y+.48,size=30,color=c))
   n=DecimalNumber(0,num_decimal_places=2,font_size=30,color=c).move_to([2.35,y-.7,0]);n.add_updater(lambda m,tr=tracker:m.set_value(tr.get_value()));self.add(n,text('일',x=3.1,y=y-.7,size=22,color=c))
 def growth_axes(self):return Axes(x_range=[0,25,5],y_range=[0,12,5],x_length=6.7,y_length=2.1,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,.3,0])
 def path(self,a,fn,xs,color=BLUE):return VMobject(stroke_color=color,stroke_width=3).set_points_as_corners([a.c2p(float(x),float(y)) for x,y in zip(xs,fn(xs))])
 def dots_on_fraction(self,cluster=False,y=2.55):
  u=mantissa(sample(90,cluster));g=VGroup()
  for i,v in enumerate(u):g.add(Dot([-3.5+7*v,y+.13*((i%3)-1),0],radius=.032,color=PURPLE))
  return g
 def s01(self):
  self.show(self.numbers());self.note_at('여러 종류의 수치 데이터 · 설명용 예시',size=24);self.formulas(r'1,2,3,\ldots,9\quad\text{equally likely?}')
  self.to(3);self.show(text('0.0046의 첫 유효숫자는 4',y=-3.6,size=25,color=MUTED))
 def s02(self):
  self.show(self.histogram());self.note_at('벤포드 이론 분포 · 실제 표본 측정 결과 아님',size=23);self.formulas(r'P(1)\approx30.1\%,\qquad P(9)\approx4.6\%',colors=[WHITE]);self.to(14);self.note_at('벤포드 법칙',size=34,color=TEAL)
 def s03(self):
  self.show(text('1',y=2.65,size=100,color=TEAL));self.note_at('왜 1이 더 자주 나타날까?',y=.5,size=32,color=TEAL)
 def s04(self):
  self.t=ValueTracker(0);n=DecimalNumber(1,num_decimal_places=3,font_size=62,color=WHITE).move_to([0,2.8,0]);n.add_updater(lambda m:m.set_value(growth(self.t.get_value())));self.add(n,text('×1.1 / day',x=2.5,y=3.7,size=23,color=TEAL));a=self.growth_axes();xs=np.linspace(0,25,241);self.add(a,self.path(a,growth,xs),always_redraw(lambda:Dot(a.c2p(self.t.get_value(),growth(self.t.get_value())),radius=.06,color=TEAL)),text('0',x=-3.4,y=-1.2,size=20,color=MUTED),text('25일',x=3.2,y=-1.2,size=20,color=MUTED));self.formulas(r'X(t)=1.1^t',colors=[TEAL])
  self.to(24);self.note_at('처음 값 1 · 하루에 10% 성장',size=26)
  self.to(28)
  for value in [1,2,3]:self.play(self.t.animate.set_value(value),run_time=1.2,rate_func=linear)
 def s05(self):
  self.time_rows();self.note_at('연속시간 성장 모형 · 구간 통과 후 점을 고정',size=23);self.formulas(r'X(t)=a\,1.1^t',colors=[WHITE]);self.play(self.ta.animate.set_value(TWO_TIME),run_time=3.5,rate_func=linear)
  self.to(41);self.note_at('9 → 10은 약 11.1%의 증가',size=27,color=ORANGE);self.to(45);self.play(self.tb.animate.set_value(NINE_TIME),run_time=1.6,rate_func=linear)
  self.to(49);self.formulas(r'1\to2:\ 7.27\;\text{days}',r'9\to10:\ 1.11\;\text{days}',colors=[TEAL,ORANGE])
 def s06(self):
  self.time_rows(10,90);self.ta.set_value(TWO_TIME);self.tb.set_value(NINE_TIME);self.note_at('같은 비율이면, 10배 커져도 같은 시간',size=25);self.formulas(r'\times10\quad\Rightarrow\quad\text{same time}',colors=[WHITE])
 def s07(self):
  self.show(text('구간 통과 시간을 정확히 계산하려면?',y=2.1,size=31));self.to(62);self.formulas(r'\log_{10}(ab)=\log_{10}a+\log_{10}b',colors=[PURPLE]);self.note_at('로그: 곱셈을 덧셈으로',size=30,color=PURPLE)
 def s08(self):
  left=eq(r'X',y=2.7,size=54);right=eq(r'\log_{10}X',y=.6,size=45,color=PURPLE);self.show(left,right);self.formulas(r'\log_{10}(10X)=\log_{10}X+1',colors=[PURPLE]);self.to(72);self.formulas(r'\log_{10}(100X)=\log_{10}X+2',colors=[PURPLE]);self.note_at('×10은 +1 · ×100은 +2',size=29,color=PURPLE)
 def s09(self):
  a=self.growth_axes();xs=np.linspace(0,25,241);curve=self.path(a,growth,xs,BLUE);self.add(a,curve);self.formulas(r'\log_{10}X(t)=t\log_{10}(1.1)',r'\Delta\log_{10}X=\log_{10}(1.1)',colors=[PURPLE,WHITE]);self.note_at('매일 로그값에 같은 수를 더한다',size=27,color=PURPLE)
  b=Axes(x_range=[0,25,5],y_range=[0,1.1,.5],x_length=6.7,y_length=2.1,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,.3,0]);straight=self.path(b,lambda t:t*STEP,xs,PURPLE);self.play(Transform(a,b),Transform(curve,straight),run_time=2);self.add(text('세로축: log₁₀X · 가로축: 시간 t',y=1.9,size=22,color=PURPLE))
 def s10(self):
  r=self.ruler(log=False);self.add(r);self.note_at('같은 값의 차이 → 같은 비율의 차이',size=27);self.to(85);self.play(Transform(r,self.ruler()),run_time=2);self.formulas(r'0=\log_{10}1<\log_{10}2<\cdots<\log_{10}10=1',colors=[PURPLE])
 def s11(self):
  self.add(self.ruler());u=ValueTracker(0);self.add(always_redraw(lambda:self.marker(u.get_value())));self.note_at('로그 눈금 위에서 일정한 속도',size=28,color=PURPLE);self.formulas(r'\log_{10}X(t)=t\log_{10}(1.1)',colors=[PURPLE]);self.play(u.animate.set_value(.9999),run_time=5,rate_func=linear)
 def s12(self):
  self.add(self.ruler(y=3));u=ValueTracker(0);self.add(always_redraw(lambda:self.marker(u.get_value(),y=3)),always_redraw(lambda:self.histogram(occupancy(u.get_value()),y=-1.05,height=1.6,maximum=1,labels=False)));self.note_at('이상적인 연속 관찰 · 완전한 로그 주기를 반복',size=23);self.formulas(r'\frac{\text{time in interval}}{\text{total time}}\longrightarrow\text{interval length}',colors=[PURPLE]);self.play(u.animate.set_value(3),run_time=5,rate_func=linear)
  self.to(104);self.note_at('정속 이동 → 구간의 길이가 체류 비율',size=27,color=PURPLE)
 def s13(self):
  self.add(self.ruler(y=3,high=[1,2]),self.ruler(y=.6,scale=10,high=[1,2]));self.note_at('먼저 1≤S<10 · 첫 유효숫자의 구간',size=25);self.formulas(r'X=10^kS,\quad1\le S<10,\quad k\in\mathbb Z',r'd\le S<d+1',colors=[WHITE,PURPLE]);self.to(114);self.note_at('10배씩 커져도 구간의 비율은 같다',size=26,color=PURPLE)
 def interval_to_bar(self,r,h,d):
  target=h[1+2*(d-1)];target.set_opacity(0);copy=target.copy().set_opacity(.8)
  self.play(TransformFromCopy(r[d-1],copy),run_time=1);self.remove(copy);target.set_opacity(.8)
 def s14(self):
  r=self.ruler(y=3,high=[1]);self.add(r);self.hh=self.histogram(np.array([P[0]]+[0.]*8),y=-.8,height=1.8,labels=False);self.hh[1].set_opacity(0);self.add(self.hh);self.formulas(r'P(1)=\log_{10}2-\log_{10}1\approx30.1\%',colors=[TEAL]);self.note_at('로그 눈금 한 주기의 전체 길이 = 1',size=25);self.interval_to_bar(r,self.hh,1)
  self.to(125);new=self.histogram(np.array([P[0]]+[0.]*7+[P[8]]),y=-.8,height=1.8,labels=False);self.hh[17].become(new[17]);self.hh[17].set_opacity(0);self.play(Transform(r,self.ruler(y=3,high=[9])),run_time=.5);self.formulas(r'P(9)=\log_{10}10-\log_{10}9\approx4.6\%',colors=[ORANGE]);self.interval_to_bar(r,self.hh,9)
 def s15(self):
  self.add(self.ruler(y=3),self.histogram(y=-.8,height=1.8,labels=False));self.formulas(r'P(d)=\log_{10}(d+1)-\log_{10}d',r'=\log_{10}\left(1+\frac1d\right),\quad d=1,\ldots,9',colors=[PURPLE,WHITE]);self.note_at('로그 구간의 길이 → 첫 자리 확률',size=27,color=PURPLE)
 def s16(self):
  self.add(self.ruler(y=3),self.histogram(y=-.8,height=1.8,labels=False));self.formulas(r'\boxed{P(d)=\log_{10}\left(1+\frac1d\right)}',colors=[PURPLE])
 def s17(self):
  cards=VGroup(*[text(s,x=(-2 if i%2==0 else 2),y=3.4-.85*(i//2),size=38,color=dc(int(s[0]))) for i,s in enumerate(['1.5','32','860','12000','450000'])]);self.show(cards);self.note_at('원리 설명용 수치 · 실제 관측 자료 아님',size=24);self.formulas(r'\text{all grow at the same rate?}',colors=[WHITE]);self.to(142);self.note_at('같은 성장 과정이 꼭 필요한 것은 아니다',size=27,color=PURPLE)
 def s18(self):
  self.add(self.ruler(y=2.8),self.dots_on_fraction(y=2.8));self.note_at('설명용 모의자료 · 전체 로그값이 아닌 소수 부분',size=23);self.formulas(r'u=\{\log_{10}X\}\in[0,1)',r'u\ \text{approximately uniform}',colors=[PURPLE,PURPLE]);self.to(153);self.show(text('서로 다른 자릿수 → 같은 [0,1) 눈금으로',y=.7,size=27,color=PURPLE));self.show(text('여러 자릿수라는 조건만으로는 충분하지 않음',y=-4.15,size=23,color=MUTED))
 def s19(self):
  self.add(self.ruler(y=3));dots=self.dots_on_fraction(y=3);h=self.histogram(probabilities(sample()),y=-1,height=1.6,maximum=1,labels=False);self.add(dots,h);self.note_at('모의자료: 로그 소수 부분이 고르면 벤포드에 근접',size=22)
  self.to(164);self.note_at('조건: 로그값의 소수 부분이 비교적 고른 분포',size=23,color=PURPLE)
 def s20(self):
  self.add(self.ruler(),self.dots_on_fraction());self.formulas(r'P(d)=\log_{10}\left(1+\frac1d\right)',colors=[PURPLE]);self.note_at('1이 특별해서가 아니라, 분포의 구조 때문에',size=27,color=TEAL)
  self.to(170);self.show(text('숫자의 빈도 뒤에는 분포의 구조가 있다',y=.25,size=31,color=WHITE));self.show(text('크기와 비율 → 로그 공간 → 첫 자리 확률',y=-.85,size=24,color=PURPLE))
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')

