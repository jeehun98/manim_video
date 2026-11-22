"""Vector algebra, metric geometry, and completeness: independent vertical scenes."""
from pathlib import Path
import json,textwrap,math
import numpy as np
from manim import *
from mechanics import U,V,angle,norm,taylor,l2_error,error_bound,projection
R=Path(__file__).resolve().parent
BG='#10131C';INK='#EAF0F7';MUTED='#8294AB';BLUE='#65B9EF';GOLD='#EDBC73';GREEN='#62D7B9';PURPLE='#A596EF';RED='#F1848B'
config.frame_width=9;config.frame_height=16;config.background_color=BG
TC={}
def tx(s,x=0,y=0,size=28,c=INK,w=7.2):
 key=(s,size,c,w)
 if key not in TC:
  o=Text(s,font='Malgun Gothic',font_size=size,color=c)
  if o.width>w:o.scale_to_fit_width(w)
  TC[key]=o
 return TC[key].copy().move_to([x,y,0])
def eq(s,x=0,y=0,size=36,c=INK,w=7.2):return tx(s,x,y,size,c,w)
def clip(q):return float(np.clip(q,0,1))
def pt(x,y):return np.array([float(x),float(y),0.])
def arr(o,v,c=BLUE,s=1.):return Arrow(pt(*o),pt(*o)+s*np.array([v[0],v[1],0.]),buff=0,color=c,stroke_width=4,max_tip_length_to_length_ratio=.12)
def angle_arc(o,a=1.,r=.55,c=GREEN):
 phi=float(np.arctan2(1,a));return Arc(radius=r,start_angle=-phi,angle=2*phi,arc_center=pt(*o),color=c,stroke_width=2.5)
def grid(a=1.,o=(-.7,.3),s=1.3):
 g=VGroup()
 for j in [-1,0,1]:g.add(Line(pt(o[0]+s*a*j,o[1]-2.2),pt(o[0]+s*a*j,o[1]+2.2),color=MUTED,stroke_width=1,stroke_opacity=.35))
 for j in [-1,0,1]:g.add(Line(pt(o[0]-s*a,o[1]+s*j),pt(o[0]+s*a,o[1]+s*j),color=MUTED,stroke_width=1,stroke_opacity=.35))
 return g
def function_plot(x,values,y=1.3,h=3.,w=7.,xr=(0,1),yr=(0,3),c=BLUE,width=3):
 xx=(np.asarray(x)-(xr[0]+xr[1])/2)*w/(xr[1]-xr[0]);yy=y-h/2+(np.asarray(values)-yr[0])*h/(yr[1]-yr[0])
 return VMobject(stroke_color=c,stroke_width=width).set_points_as_corners(np.column_stack((xx,yy,np.zeros(len(xx)))))
def function_axes(y=1.3,h=3.,w=7.,xr=(0,1),yr=(0,3)):
 g=VGroup(Line(pt(-w/2,y-h/2),pt(w/2,y-h/2),color=MUTED,stroke_width=1.2),Line(pt(-w/2,y-h/2),pt(-w/2,y+h/2),color=MUTED,stroke_width=1.2))
 if yr[0]<0<yr[1]:
  z=y-h/2+(0-yr[0])*h/(yr[1]-yr[0]);g.add(Line(pt(-w/2,z),pt(w/2,z),color=MUTED,stroke_width=1,stroke_opacity=.5))
 return g
class HilbertScene(Scene):
 index=1
 def get_moving_and_static_mobjects(self,animations):return list(self.mobjects),[]
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[];self.body_audit=[];self.current=None
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
  self.add(tx('벡터에는 원래 길이도 각도도 없다?',0,7.15,25),Line([-3.7,6.65,0],[3.7,6.65,0],color=MUTED,stroke_opacity=.35))
  self.add(RoundedRectangle(width=7.8,height=2.0,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([-.1,-5.9,0]).set_z_index(50))
  self.caption=VGroup();self.labels_now=VGroup();self.dynamic=VGroup();self.clock=ValueTracker(self.start);self.add(self.clock,self.dynamic)
  def update(m):
   t=self.clock.get_value();g=self.geometry(t)
   if len(g):
    assert g.get_left()[0]>=-4.05 and g.get_right()[0]<=4.05 and g.get_bottom()[1]>=-4.7 and g.get_top()[1]<=6.4,('geometry',self.index,t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
   m.submobjects=g.submobjects
  self.dynamic.add_updater(update)
  events=sorted(set([self.start,self.end]+[z for z in [4,6,9,11,14,16,23,28,32,39,42,48,57,58,62,67,70,81,88,92,98,102,110,117,122,126,131,136,142,155,159,163,166] if self.start<z<self.end]+[x['start'] for x in self.lines if self.start<x['start']<self.end]))
  for a,b in zip(events,events[1:]):
   self.update_text(a);self.play(self.clock.animate.set_value(b),run_time=(round(b*config.frame_rate)-round(a*config.frame_rate))/config.frame_rate,rate_func=linear)
  self.dynamic.clear_updaters()
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(dict(captions=self.audit,labels=self.body_audit,geometry_checked_every_frame=True),indent=2),encoding='utf-8')
 def update_text(self,t):
  line=next(x for x in self.lines if x['start']<=t<x['end'])
  if line!=self.current:
   self.remove(self.caption);self.current=line
   self.caption=VGroup(*[tx(p,size=28,w=7.2) for p in textwrap.wrap(line['text'],width=27,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.12)
   if self.caption.height>1.5:self.caption.scale_to_fit_height(1.5)
   self.caption.move_to([-.1,-5.9,0]).set_z_index(51);self.add(self.caption)
   self.audit.append(dict(start=line['start'],end=line['end'],left=float(self.caption.get_left()[0]),right=float(self.caption.get_right()[0]),bottom=float(self.caption.get_bottom()[1]),top=float(self.caption.get_top()[1]),height=float(self.caption.height)))
  self.remove(self.labels_now);self.labels_now=self.labels(t);self.add(self.labels_now)
  for m in self.labels_now:
   assert m.get_left()[0]>=-4.05 and m.get_right()[0]<=4.05 and m.get_bottom()[1]>=-4.7 and m.get_top()[1]<=6.4,('label',self.index,t,m.get_center())
  self.body_audit.append(dict(time=t,bottom=float(self.labels_now.get_bottom()[1]),top=float(self.labels_now.get_top()[1])))
 def labels(self,t):
  i=self.index;g=VGroup();titles=['벡터 공간에 주어진 것은?','연산을 보존해도 각도는 달라진다','기하학을 정하는 추가 규칙 · 내적','같은 좌표, 서로 다른 기하학','극한도 공간 안에 있어야 한다','화살표에서 함수의 공간으로']
  g.add(tx(titles[i-1],0,5.9,30,c=GOLD))
  if i==1:
   if t<9:
    g.add(tx('익숙한 화살표의 그림',0,4.75,26,c=MUTED))
    if t<6:g.add(eq('‖u‖',.3,3.25,29,c=BLUE).set_opacity(1-clip((t-4)/2)),eq('‖v‖',.3,-1.8,29,c=GOLD).set_opacity(1-clip((t-4)/2)))
   else:
    g.add(eq('u + v     ·     a u',0,4.6,38,c=GREEN))
    if t<16:g.add(tx('덧셈과 스칼라곱',0,-2.8,29,c=GREEN))
    elif t<23:g.add(tx('선형독립 · 기저 · 차원',0,-2.8,29,c=GREEN),eq('dim V = 2',0,-3.8,31,c=MUTED))
    else:g.add(tx('길이 ?    각도 ?',0,-2.8,33,c=MUTED),tx('연산의 규칙에는 포함되지 않는다',0,-3.9,27))
   g.add(tx('실수 벡터 공간',0,-4.55,20,c=MUTED))
  elif i==2:
   g.add(tx('표준 내적은 고정 · 벡터의 좌표를 변환',0,4.8,24,c=MUTED),eq('T(x,y) = (2x,y)' if t>=32 else 'u = (1,1),  v = (1,−1)',0,3.8,33,c=GREEN))
   if t>=42:
    g.add(eq('T(u+v) = T(u)+T(v)',0,-2.8,31,c=GREEN),eq('T(a u) = a T(u)',0,-3.65,31,c=GREEN))
    if t>=48:g.add(tx('기본 연산만으로는 각도를 정할 수 없다',0,-4.5,25,c=GOLD))
    else:g.add(eq('각도 90° → 53.1°',0,-4.5,29,c=GOLD))
   else:g.add(tx('가로 성분을 두 배로',0,-3.7,28,c=GREEN))
  elif i==3:
   g.add(tx('INNER PRODUCT · 실수 벡터 공간',0,4.8,22,c=MUTED))
   if t<62:
    g.add(eq('u',-1.9,3.4,42,c=BLUE,w=1),eq('v',1.9,3.4,42,c=GOLD,w=1),eq('⟨u,v⟩',0,.5,48,c=GREEN),tx('두 벡터 → 하나의 실수',0,-3.2,29,c=GREEN))
    if t>=58:g.add(eq('0 ∈ ℝ',0,-1.7,38))
    else:g.add(eq('?',0,-1.7,44,c=MUTED))
   else:
    g.add(tx('익숙한 규칙',0,3.8,25,c=BLUE),eq('⟨u,v⟩ = u₁v₁ + u₂v₂',0,2.75,35,c=BLUE))
    if t<67:g.add(eq('1×1 + 1×(−1) = 0',0,.6,36,c=GREEN))
    if t>=67:g.add(tx('다른 규칙도 가능하다',0,1.25,26,c=GREEN))
    if t>=70:g.add(eq('⟨u,v⟩ᴳ = 4u₁v₁ + u₂v₂',0,.15,34,c=GREEN),tx('대칭 · 쌍선형 · 양의 정부호',0,-1.65,24,c=MUTED),eq('G = diag(4,1)',0,-2.7,30,c=GREEN))
    g.add(tx('조건을 만족하는 내적을 선택한다',0,-4.15,26,c=MUTED))
  elif i==4:
   if t<92:
    g.add(eq('u=(1,1),  v=(1,−1)  ·  좌표 고정',0,4.75,28,c=MUTED),tx('좌표 그림',-2.6,3.9,23,c=MUTED,w=2))
    g.add(tx('내적 기하학의 표현',-1.85,.2,22,c=GREEN,w=3.4))
    if t<81:
     g.add(eq('⟨u,v⟩ = 1−1 = 0',1.65,2.75,28,c=GREEN,w=3.4),eq('90°',1.65,1.7,33,c=GREEN,w=2))
    else:
     g.add(eq('⟨u,v⟩ᴳ = 4−1 = 3',1.6,2.75,27,c=GREEN,w=3.55),eq('G = diag(4,1)',1.65,1.7,25,c=GREEN,w=3.3))
    g.add(tx('아래 그림'+'는 선택한 내적의 측정 모델',0,-3.1,22,c=MUTED))
    if t>=88:g.add(eq('‖u‖: √2 → √5     θ: 90° → 53.1°',0,-4.2,27,c=GREEN))
    else:g.add(tx('벡터를 옮기는 실험과 구별',0,-4.2,26,c=MUTED))
   else:
    g.add(eq('‖u‖ = √⟨u,u⟩',0,4.6,36,c=GREEN))
    g.add(eq('cos θ = ⟨u,v⟩ / (‖u‖ ‖v‖)',0,-1.45,32,c=GREEN))
    g.add(tx('벡터 공간 + 내적 = 내적 공간',0,-2.85,29,c=GOLD))
    if t>=102:g.add(tx('길이 · 거리 · 각도 · 직교 · 정사영',0,-4.2,25),tx('그림: 표준 내적의 정사영 예시',0,3.55,22,c=MUTED))
    else:g.add(tx('내적으로 길이와 각도를 정의한다',0,-4.2,27))
  elif i==5:
   if t<117:
    g.add(tx('CAUCHY SEQUENCE · 코시 수열',0,4.8,23,c=MUTED),tx('충분히 뒤의 모든 항들이 서로 가까워진다',0,3.65,26,c=BLUE),eq('m,n ≥ N  ⇒  ‖vₘ−vₙ‖ < ε',0,-1.4,31,c=BLUE),tx('극한이 원래 공간의 원소일까?',0,-2.75,30,c=PURPLE),tx('열린 원: 빠진 극한을 나타내는 개념도',0,-4.25,23,c=MUTED))
   else:
    g.add(tx('P = [0,1] 위의 모든 유한차수 다항식',0,4.8,24,c=MUTED),eq('⟨p,q⟩ = ∫₀¹ p(x)q(x) dx',0,3.85,29,c=GREEN))
    if t<126:
     g.add(eq('pₙ(x) = Σₖ₌₀ⁿ xᵏ/k!',0,-1.2,33,c=BLUE),eq('pₙ → eˣ   (L² 노름)',0,-2.45,31,c=PURPLE),tx('균등 수렴 ⇒ L² 코시 수열',0,-3.5,26,c=BLUE),tx('eˣ는 다항식이 아니다',0,-4.35,25,c=PURPLE))
    elif t<136:
     g.add(tx('P 안의 근사들',-1.7,-1.35,24,c=BLUE,w=3),tx('P 밖의 극한',1.85,-1.35,24,c=PURPLE,w=3),eq('p₀, p₁, p₂, …',-1.65,-2.35,27,c=BLUE,w=3),eq('eˣ ∉ P',1.85,-2.35,31,c=PURPLE,w=3),tx('극한은 존재해도 P 안에서는 다룰 수 없다',0,-3.7,26,c=PURPLE),tx('상자는 원소의 소속을 나타내는 개념도',0,-4.5,20,c=MUTED))
    else:
     g.add(tx('완비성 · COMPLETENESS',0,-.65,27,c=PURPLE),tx('모든 코시 수열 → 공간 안에서 수렴',0,-1.25,25,c=PURPLE),eq('L²[0,1]',0,-2.15,32,c=PURPLE))
     if t>=142:g.add(tx('완비된 내적 공간 = 힐베르트 공간',0,-3.65,29,c=GREEN),tx('거의 모든 곳에서 같은 함수는 동일시',0,-4.5,20,c=MUTED))
     else:g.add(tx('한 극한이 아닌, 필요한 모든 극한을 포함',0,-3.7,24,c=MUTED),tx('L² 노름에 대한 P의 완비화',0,-4.5,22,c=MUTED))
  elif i==6:
   if t<155:
    for y,s,c in [(4.1,'벡터 공간',BLUE),(1.35,'내적 공간',GREEN),(-1.4,'힐베르트 공간',PURPLE)]:g.add(tx(s,0,y,33,c=c))
    g.add(tx('덧셈 · 스칼라곱',0,3.35,24,c=MUTED),tx('+ 내적',0,2.5,25,c=GREEN),tx('길이 · 각도 · 직교',0,.6,24,c=MUTED),tx('+ 완비성',0,-.25,25,c=PURPLE),tx('모든 코시 수열의 극한',0,-2.15,24,c=MUTED),tx('집합 포함이 아닌 구조를 추가하는 순서',0,-4.3,22,c=MUTED))
   elif t<166:
    g.add(eq('f(x)=sin x,   g(x)=cos x',0,4.8,31),tx('실수 L²[−π,π]',0,3.9,23,c=MUTED))
    if t>=159:g.add(eq('⟨f,g⟩ = ∫₋π^π f(x)g(x) dx = 0',0,-1.2,29,c=GREEN),tx('서로 직교하는 함수',0,-2.45,31,c=GREEN),tx('그래프가 직각으로 교차한다는 뜻이 아니다',0,-3.5,23,c=MUTED),tx('sin x cos x의 양·음 적분이 상쇄',0,-4.35,23,c=MUTED))
    else:g.add(tx('함수도 벡터처럼 더하고 곱한다',0,-2.7,29,c=GREEN),tx('벡터의 구조를 함수 공간으로 확장',0,-4,26,c=MUTED))
   else:
    g.add(tx('함수도 벡터가 될 수 있다',0,4.7,33,c=GREEN),eq('sin x + 0.4 sin 3x + 0.2 cos 5x',0,3.65,25,c=MUTED),tx('파형 = 함수 벡터들의 선형결합',0,-1.8,28,c=GREEN),tx('힐베르트 공간 · 푸리에 해석학',0,-3.2,27),tx('함수해석학의 출발점',0,-4.25,28,c=PURPLE))
  return g
 def geometry(self,t):
  i=self.index;g=VGroup()
  if i==1:
   o=(-1.1,.7);u=np.array([1.,1.]);v=np.array([1.,-1.]);s=1.55
   if 14<=t<16:u=u*(1+clip((t-14)/2)*.65)
   g.add(arr(o,u,BLUE,s),arr(o,v,GOLD,s),tx('u',o[0]+s*u[0]+.27,o[1]+s*u[1]+.18,26,c=BLUE,w=1),tx('v',o[0]+s*v[0]+.27,o[1]+s*v[1]-.18,26,c=GOLD,w=1))
   if t<9:
    opacity=1-clip((t-6)/3);g.add(angle_arc(o).set_opacity(opacity),tx('90°',.65,.7,30,c=GREEN,w=2).set_opacity(opacity))
   if 11<=t<14:
    q=max(.001,clip((t-11)/2));end=pt(*o)+s*np.r_[u,0];g.add(arr(tuple(end[:2]),v*q,GOLD,s),arr(o,(u+v)*q,GREEN,s))
    g.add(DashedLine(pt(*o)+s*np.r_[v,0],pt(*o)+s*np.r_[u+v,0],color=BLUE,stroke_width=1.5))
    if t>=13:g.add(tx('u+v',2.55,1.3,25,c=GREEN,w=1.9))
  elif i==2:
   a=1+clip((t-32)/7);o=(-.7,.3);s=1.3;g.add(grid(a,o,s),arr(o,(a,1),BLUE,s),arr(o,(a,-1),GOLD,s),angle_arc(o,a))
   g.add(tx(f'({a:.0f},1)' if t<32 or t>=39 else 'T(u)',o[0]+a*s+.45,o[1]+s+.35,25,c=BLUE,w=1.6),tx(f'({a:.0f},−1)' if t<32 or t>=39 else 'T(v)',o[0]+a*s+.45,o[1]-s-.35,25,c=GOLD,w=1.7))
   g.add(tx(f'{np.degrees(2*np.arctan2(1,a)):.1f}°',.65,.3,30,c=GREEN,w=2))
   if t<42:g.add(tx(f'θ = {np.degrees(2*np.arctan2(1,a)):.1f}°',0,-2.9,32,c=GREEN))
  elif i==3 and t<62:
   g.add(Arrow(pt(-1.8,2.9),pt(-.5,1.3),buff=.15,color=BLUE,stroke_width=3),Arrow(pt(1.8,2.9),pt(.5,1.3),buff=.15,color=GOLD,stroke_width=3),Arrow(pt(0,-.2),pt(0,-1.1),buff=.05,color=GREEN,stroke_width=3))
   g.add(RoundedRectangle(width=3.5,height=1.45,corner_radius=.14,color=GREEN,stroke_width=2).move_to([0,.5,0]))
  elif i==4:
   if t<92:
    o=(-2.2,2.45);s=.9;g.add(arr(o,U,BLUE,s),arr(o,V,GOLD,s))
    if t<81:g.add(angle_arc(o,r=.36))
    w=1 if t<81 else 1+3*clip((t-81)/5);a=np.sqrt(w);o2=(-2.2,-1.15);g.add(arr(o2,(a,1),BLUE,.95),arr(o2,(a,-1),GOLD,.95),angle_arc(o2,a,r=.45),tx(f'{angle(w=w):.1f}°',1.7,-1.15,33,c=GREEN,w=2))
    g.add(Line(pt(-3.6,.75),pt(3.6,.75),color=MUTED,stroke_width=1,stroke_opacity=.35))
   else:
    o=(-1.6,.9);s=1.6;u=np.array([1,1]);v=np.array([2,0]);g.add(arr(o,u,BLUE,s),arr(o,v,GOLD,s),angle_arc(o,a=1,r=.45).set_opacity(0))
    g.add(tx('u',.3,2.75,25,c=BLUE,w=1),tx('v',2.05,.9,25,c=GOLD,w=1))
    if t>=102:
     q=projection(u,v);p=pt(*o)+s*np.r_[q,0];tip=pt(*o)+s*np.r_[u,0];g.add(DashedLine(tip,p,color=GREEN,stroke_width=2),arr(o,q,GREEN,s),RightAngle(Line(p,p+RIGHT),Line(p,p+UP),length=.17,color=GREEN),tx('projᵥ u',0,.15,24,c=GREEN,w=2.5))
  elif i==5:
   if t<117:
    g.add(Line(pt(-3.3,.6),pt(3.2,.6),color=MUTED,stroke_width=1.5));limit=2.2
    for j in range(1,11):
     x=limit-5/(j+1);opacity=.4 if j<4 else 1;g.add(Dot(pt(x,.6),radius=.05,color=BLUE).set_opacity(opacity))
    g.add(Circle(radius=.16,color=PURPLE,stroke_width=2).move_to([limit,.6,0]),tx('극한',limit,1.35,25,c=PURPLE,w=2))
    n=2+int(clip((t-110)/7)*6);x=limit-5/(n+1);g.add(Line(pt(x,1.9),pt(limit,1.9),color=BLUE,stroke_width=3),tx('수열의 꼬리',-.3,2.6,25,c=BLUE))
   else:
    x=np.linspace(0,1,201);g.add(function_axes(1.35,2.7),function_plot(x,np.exp(x),1.35,2.7,c=PURPLE,width=2))
    n=min(7,max(0,int((t-117)*.85)))
    if t<126:g.add(function_plot(x,taylor(x,n),1.35,2.7,c=BLUE,width=3.5),tx(f'p{str(n).translate(str.maketrans("0123456789","₀₁₂₃₄₅₆₇₈₉"))}',-2.9,2.6,25,c=BLUE,w=1),tx('eˣ',2.8,2.8,27,c=PURPLE,w=1),tx('0',-3.5,-.2,20,c=MUTED,w=.5),tx('1',3.5,-.2,20,c=MUTED,w=.5))
    else:g.add(function_plot(x,taylor(x,7),1.35,2.7,c=BLUE,width=1.5).set_stroke(opacity=.4))
    if 126<=t<136:g.add(RoundedRectangle(width=3.3,height=1.45,corner_radius=.12,color=BLUE,stroke_width=1.5).move_to([-1.65,-2.35,0]),Arrow(pt(.25,-2.35),pt(.65,-2.35),color=MUTED,buff=0,stroke_width=2))
    if t>=136:
     g.add(RoundedRectangle(width=7.2,height=1.3,corner_radius=.15,color=PURPLE,stroke_width=2).move_to([0,-2.4,0]))
     for j in range(5):g.add(Dot(pt(-2.7+j*1.35,-2.7),radius=.045,color=BLUE if j%2 else PURPLE))
  elif i==6:
   if t<155:
    for y,c in [(3.7,BLUE),(.95,GREEN),(-1.8,PURPLE)]:g.add(RoundedRectangle(width=6.5,height=1.65,corner_radius=.13,color=c,stroke_width=1.5).move_to([0,y,0]))
   else:
    x=np.linspace(-np.pi,np.pi,241);g.add(function_axes(1.25,3.1,xr=(-np.pi,np.pi),yr=(-1.25,1.25)))
    if t<166:
     g.add(function_plot(x,np.sin(x),1.25,3.1,xr=(-np.pi,np.pi),yr=(-1.25,1.25),c=BLUE),function_plot(x,np.cos(x),1.25,3.1,xr=(-np.pi,np.pi),yr=(-1.25,1.25),c=GOLD))
     if t>=159:
      # The shaded product's signed integral cancels by oddness.
      for j in range(4):
       xx=np.linspace(-np.pi+j*np.pi/2,-np.pi+(j+1)*np.pi/2,40);prod=np.sin(xx)*np.cos(xx);z=1.25
       path=function_plot(xx,prod,1.25,3.1,xr=(-np.pi,np.pi),yr=(-1.25,1.25),c=GREEN if np.mean(prod)>=0 else PURPLE,width=1)
       coords=np.column_stack((xx*7/(2*np.pi),z+prod*3.1/2.5,np.zeros(len(xx))));pts=np.vstack((pt(coords[0,0],z),coords,pt(coords[-1,0],z),pt(coords[0,0],z)))
       g.add(VMobject(stroke_width=0,fill_color=GREEN if np.mean(prod)>=0 else PURPLE,fill_opacity=.15).set_points_as_corners(pts))
    else:
     q=clip((t-166)/3);v=np.sin(x)+q*(.4*np.sin(3*x)+.2*np.cos(5*x));g.add(function_plot(x,v,1.25,3.1,xr=(-np.pi,np.pi),yr=(-1.5,1.5),c=GREEN,width=3.5))
  return g
