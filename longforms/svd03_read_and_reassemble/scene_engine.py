"""Follow one fixed input through reading, scaling and output reassembly."""
import json,math,textwrap
from pathlib import Path
import numpy as np
from manim import *
config.background_color='#09121F';config.frame_width=128/9;config.frame_height=8
FONT='Malgun Gothic';INK='#EDF4FC';MUTED='#8EA3BA';GOLD='#FFD077';PURPLE='#BC9AFF';ORANGE='#FFAB70';TEAL='#51D9C5';BLUE_IN='#64AEFF'
ROOT=Path(__file__).resolve().parent
SENTENCES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['sentences']
def text(s,n=23,c=INK):return Text(s,font=FONT,font_size=n,color=c,line_spacing=1.1)
def rotation(d):
 a=math.radians(d);return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
V=rotation(30);U=rotation(60);SIGMA=np.diag([2.,.5]);MATRIX=U@SIGMA@V.T
V1,V2=V[:,0],V[:,1];U1,U2=U[:,0],U[:,1];MAIN_X=V1+V2;MAIN_Y=MATRIX@MAIN_X

def progress(t,a,b):return float(np.clip((t-a)/(b-a),0,1))
def counter_coefficients(t):
 if t<125 or t>=138:return np.array([0.,1.])
 if t<129:d=120-90*smooth(progress(t,125,129))
 elif t<133:d=30+90*smooth(progress(t,129,133))
 else:d=120-45*smooth(progress(t,133,138))
 a=math.radians(d);c=V.T@np.array([math.cos(a),math.sin(a)]);c[np.abs(c)<1e-12]=0;return c

def coefficients(t):return counter_coefficients(t) if t>=110 else np.array([1.,1.])
def weighted(t):return np.diag(SIGMA)*coefficients(t)
def scalar_scale(t,i):
 if i==0:return 1+smooth(progress(t,50,55))
 return 1-.5*smooth(progress(t,55,58))

class ReadingScene(Scene):
 start_time=0;end_time=152
 def construct(self):
  clock=ValueTracker(self.start_time);now=lambda:clock.get_value();self.add(clock)
  self.add(text('행렬은 하나의 입력을 어떻게 읽어낼까?',33).move_to([0,3.43,0]),text('관측 실험  /  03     하나의 입력을 읽고 조립하다',15,MUTED).move_to([0,3.87,0]),Line([-6.65,2.98,0],[6.65,2.98,0],color='#25364B',stroke_width=1))
  L=np.array([-4.65,.28,0]);R=np.array([4.65,.28,0]);unit=.84
  def world(o,v):return o+unit*np.array([*v,0])
  for center in [-4.65,0,4.65]:
   self.add(RoundedRectangle(width=4.14,height=3.86,corner_radius=.15,stroke_color='#2A3D54',stroke_width=1.1,fill_color='#101E2D',fill_opacity=1).move_to([center,.56,0]))
  self.add(text('주 실험 입력 x',21,ORANGE).move_to([-4.65,2.7,0]))
  for lo,hi,label in [(0,110,'방향별 스칼라 계수'),(110,138,'별도 반례 z · A는 고정'),(138,152,'출력에서 거꾸로 읽기')]:
   m=text(label,20,INK).move_to([0,2.7,0]);m.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(m)
  for lo,hi,label in [(0,110,'출력 공간 · 성분별 기여'),(110,138,'별도 반례의 출력 Az'),(138,152,'관측 가능한 출력만')]:
   m=text(label,20,TEAL).move_to([4.65,2.7,0]);m.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(m)
  for o in [L,R]:
   self.add(Arrow(o+[-1.65,0,0],o+[1.65,0,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.03),Arrow(o+[0,-.85,0],o+[0,1.8,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.03),Dot(o,color=MUTED,radius=.035))
  # Fixed unit input basis, with names positioned independently of the orange input.
  for v,col,label,off in [(V1,GOLD,'v₁  30°',[.15,-.15,0]),(V2,PURPLE,'v₂  120°',[-.23,.18,0])]:
   self.add(Arrow(L,world(L,v),buff=0,color=col,stroke_width=1.5,tip_length=.1),text(label,14,col).move_to(world(L,v)+off))
  q1=world(L,.14*V1);q2=world(L,.14*V2);q=world(L,.14*(V1+V2));self.add(VMobject().set_points_as_corners([q1,q,q2]).set_stroke(MUTED,width=1))
  # This orange input NEVER rotates or changes length. Counterexamples use a different symbol z.
  main_arrow=Arrow(L,world(L,MAIN_X),buff=0,color=ORANGE,stroke_width=3,tip_length=.14)
  main_dot=Dot(world(L,MAIN_X),radius=.045,color=ORANGE)
  main_label=text('x',23,ORANGE).move_to(world(L,MAIN_X)+[.21,.13,0])
  for m in [main_arrow,main_dot,main_label]:m.add_updater(lambda m:m.set_opacity(1 if 13<=now()<138 else 0));self.add(m)
  input_read=text('x ≈ (0.3660, 1.3660)',15,ORANGE).move_to([-4.65,-1.14,0]);input_read.add_updater(lambda m:m.set_opacity(1 if 13<=now()<138 else 0));self.add(input_read)
  fixed_tag=text('주 입력 x는 그대로',15,ORANGE).move_to([-4.65,2.24,0]);fixed_tag.add_updater(lambda m:m.set_opacity(1 if 110<=now()<138 else 0));self.add(fixed_tag)
  # Projection lines are static and have nonzero length; scalar coefficients are shown separately.
  for i,(v,col) in enumerate([(V1,GOLD),(V2,PURPLE)]):
   projection=DashedLine(world(L,MAIN_X),world(L,v),color=col,stroke_width=1.5,dash_length=.065)
   projection.add_updater(lambda m,i=i:m.set_opacity(.8 if 22<=now()<138 and (i==0 or now()>=22) else 0));self.add(projection)
  comp1=Arrow(L,world(L,V1),buff=0,color=GOLD,stroke_width=3,tip_length=.11)
  comp1.add_updater(lambda m:m.set_opacity(.9 if 22<=now()<138 else 0));self.add(comp1)
  comp2=Arrow(L,world(L,V2),buff=0,color=PURPLE,stroke_width=3,tip_length=.11)
  def input_add(m):
   shift=smooth(progress(now(),36,40))*V1
   m.put_start_and_end_on(world(L,shift),world(L,shift+V2));m.set_opacity(.9 if 22<=now()<138 else 0)
  comp2.add_updater(input_add);self.add(comp2)
  # Output contribution arrows use actual coefficient-weighted vectors, not just directions.
  def output_parts(t):
   c=coefficients(t);return 2*c[0]*U1,.5*c[1]*U2
  def show_part(t,i):
   return (7<=t<13) or ((67<=t<110 and (i==0 or t>=72))) or 110<=t<152
  for i,col in [(0,GOLD),(1,PURPLE)]:
   arrow=Arrow(R,world(R,2*U1 if i==0 else .5*U2),buff=0,color=col,stroke_width=3,tip_length=.12)
   def update_output(m,i=i):
    t=now();a,b=output_parts(t);d=a if i==0 else b
    shift=(smooth(progress(t,77,80))*a if i==1 and 77<=t<110 else np.zeros(2))
    start=world(R,shift);end=world(R,shift+d)
    visible=show_part(t,i) and np.linalg.norm(d)>=.001
    if np.linalg.norm(end-start)<.001:end=start+np.array([.001,0,0])
    m.put_start_and_end_on(start,end);m.set_opacity(.95 if visible else 0)
   arrow.add_updater(update_output);self.add(arrow)
  # Output unit directions remain guides, not mislabeled scaled vectors.
  for u,col,label,off in [(U1,GOLD,'u₁  60°',[-.32,.1,0]),(U2,PURPLE,'u₂  150°',[-.25,.14,0])]:
   guide=DashedLine(R,world(R,1.25*u),color=col,stroke_width=1,dash_length=.06)
   lab=text(label,13,col).move_to(world(R,u)+off)
   for m in [guide,lab]:m.add_updater(lambda m:m.set_opacity(.6 if 7<=now()<13 or now()>=67 else 0));self.add(m)
  result=Arrow(R,world(R,MAIN_Y),buff=0,color=TEAL,stroke_width=3,tip_length=.14)
  result.add_updater(lambda m:m.set_opacity(1 if 80<=now()<110 else 0));self.add(result)
  result_dot=Dot(world(R,MAIN_Y),color=TEAL,radius=.045);result_dot.add_updater(lambda m:m.set_opacity(1 if 80<=now()<110 else 0));self.add(result_dot)
  result_label=text('Ax',22,TEAL).move_to(world(R,MAIN_Y)+[.25,.13,0]);result_label.add_updater(lambda m:m.set_opacity(1 if 80<=now()<110 else 0));self.add(result_label)
  direct=DashedLine(R,world(R,MATRIX@MAIN_X),color=INK,stroke_width=2,dash_length=.09)
  direct.add_updater(lambda m:m.set_opacity(.85 if 82<=now()<85 else 0));self.add(direct)
  exact=text('직접 Ax = 성분별 합',17,TEAL).move_to([4.65,-.76,0]);exact.add_updater(lambda m:m.set_opacity(1 if 82<=now()<110 else 0));self.add(exact)
  data=text('Ax ≈ (0.5670, 1.9821)',15,TEAL).move_to([4.65,-1.14,0]);data.add_updater(lambda m:m.set_opacity(1 if 80<=now()<110 else 0));self.add(data)
  waiting=text('아직 출력 방향을\n부여하지 않았다',18,MUTED).move_to([4.65,.85,0]);waiting.add_updater(lambda m:m.set_opacity(1 if 46<=now()<67 else 0));self.add(waiting)
  # Scalar lane cache: values are exact for the fixed input; rounded comparison values use ≈.
  cache={}
  def cached(label,n,c):
   key=(label,n,c)
   if key not in cache:cache[key]=text(label,n,c)
   return cache[key].copy()
  for i,(y,col) in enumerate([(1.1,GOLD),(-.35,PURPLE)]):
   heading=VGroup(text(' ',18));value=VGroup(text(' ',25));bar=Line([-1.15,y-.43,0],[-.55,y-.43,0],color=col,stroke_width=5)
   def heading_update(m,i=i,y=y,col=col):
    t=now();label=('관측된 출력 성분' if i==0 else '원래 입력 성분') if t>=138 else f'c{"₁" if i==0 else "₂"} = v{"₁" if i==0 else "₂"}ᵀ'+('z' if t>=110 else 'x')
    if (50<=t<110 and i==0) or (55<=t<110 and i==1):label='σ₁c₁ = 2c₁' if i==0 else 'σ₂c₂ = 0.5c₂'
    if 110<=t<138:label='기여 계수 σ₁(v₁ᵀz)' if i==0 else '기여 계수 σ₂(v₂ᵀz)'
    m.become(cached(label,18,col).move_to([0,y+.35,0]));m.set_opacity(1 if t>=26 and (i==0 or t>=33) else 0)
   def value_update(m,i=i,y=y,col=col):
    t=now();tq=math.floor(t*5)/5
    if t>=138:label=('0.50' if t<146 else '0.51 = 0.50 + 0.01') if i==0 else '?'
    elif t>=110:
     c=counter_coefficients(tq)[i];weighted_c=np.diag(SIGMA)[i]*c;label=f'{np.diag(SIGMA)[i]:g} × {c:.2f} ≈ {weighted_c:.2f}'
    elif t<50:label='1  (스칼라)'
    elif t<55 and i==1:label='1  (스칼라)'
    elif t<62:label='1 × 2 = 2' if i==0 else '1 × 0.5 = 0.5'
    else:label='2' if i==0 else '0.5'
    m.become(cached(label,23 if t<110 else 21,col).move_to([0,y-.05,0]));m.set_opacity(1 if t>=26 and (i==0 or t>=33) else 0)
   def bar_update(m,i=i,y=y):
    t=now();length=(weighted(t)[i] if t>=110 else scalar_scale(t,i))*.65
    m.put_start_and_end_on([-1.15,y-.43,0],[-1.15+max(abs(length),.001),y-.43,0]);m.set_opacity(.85 if 26<=t<138 and (i==0 or t>=33) and abs(length)>=.001 else 0)
   heading.add_updater(heading_update);value.add_updater(value_update);bar.add_updater(bar_update);self.add(heading,value,bar)
  early=text('한 입력에\n두 방향의 성분',26,INK).move_to([0,.65,0]);early.add_updater(lambda m:m.set_opacity(1 if 13<=now()<26 else 0));self.add(early)
  initial=text('두 직교 방향\n서로 다른 배율',25,INK).move_to([0,.65,0]);initial.add_updater(lambda m:m.set_opacity(1 if now()<13 else 0));self.add(initial)
  # Distinct comparison input z in its own small coordinate inset. The orange main input stays fixed.
  Z=np.array([0,1.95,0]);zunit=.3
  mini=Circle(radius=zunit,color=MUTED,fill_opacity=0,stroke_width=1).move_to(Z);mini.add_updater(lambda m:m.set_stroke(opacity=.5 if 110<=now()<138 else 0));self.add(mini)
  zarrow=Arrow(Z,Z+[0,zunit,0],color=BLUE_IN,buff=0,stroke_width=2,tip_length=.07)
  def update_z(m):
   z=V@counter_coefficients(now());m.put_start_and_end_on(Z,Z+zunit*np.array([*z,0]));m.set_opacity(1 if 110<=now()<138 else 0)
  zarrow.add_updater(update_z);self.add(zarrow)
  zname=text('별도 입력 z',13,BLUE_IN).move_to([.82,1.95,0]);zname.add_updater(lambda m:m.set_opacity(1 if 110<=now()<138 else 0));self.add(zname)
  # Actual output sum for the separate counterexample, computed from current coefficients.
  cy=Arrow(R,world(R,.5*U2),buff=0,color=TEAL,stroke_width=2,tip_length=.1)
  def update_cy(m):
   a,b=output_parts(now());y=a+b
   if now()>=146:y=y+.01*U2
   m.put_start_and_end_on(R,world(R,y));m.set_opacity(.9 if now()>=125 else 0)
  cy.add_updater(update_cy);self.add(cy)
  # Fixed reverse-observation phase: no camera enlargement or fake geometric error size.
  error_line=Line(world(R,.5*U2),world(R,.51*U2),color=ORANGE,stroke_width=4)
  error_line.add_updater(lambda m:m.set_opacity(1 if now()>=146 else 0));self.add(error_line)
  for lo,hi,label in [(110,125,'z = v₂    /    c₁ = 0, c₂ = 1'),(125,138,'A와 특잇값 고정 · z만 변화'),(138,146,'관측 성분 0.50 · u₂ 방향'),(146,152,'오차 +0.01 · 관측 성분 0.51')]:
   m=text(label,15,TEAL if hi<=146 else ORANGE).move_to([4.65,-1.14,0]);m.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(m)
  mask=RoundedRectangle(width=4.05,height=3.75,corner_radius=.12,fill_color='#0C1625',fill_opacity=1,stroke_width=0).move_to([-4.65,.56,0])
  hidden=VGroup(text('?',52,MUTED),text('출력만으로 복원할 수 있을까?',16,MUTED)).arrange(DOWN,buff=.25).move_to([-4.65,.6,0])
  for m in [mask,hidden]:m.add_updater(lambda m:m.set_opacity(1 if now()>=138 else 0));self.add(m)
  # Reading, scaling and assembly summary cards. Operators appear only once named at 99s.
  for i,(x,title,col,description,symbol) in enumerate([(-4.45,'읽기',GOLD,'방향별 좌표 (1, 1)','Vᵀ'),(0,'배율',PURPLE,'성분별 크기 (2, 0.5)','Σ'),(4.45,'조립',TEAL,'출력 방향으로 합성','U')]):
   box=RoundedRectangle(width=4.12,height=1.02,corner_radius=.1,fill_color='#12263A',fill_opacity=1,stroke_width=1,stroke_color='#304A62').move_to([x,-2.03,0]);box.add_updater(lambda m,i=i:m.set_opacity(1 if now()>=(26 if i==0 else 50 if i==1 else 67) else 0));self.add(box)
   titlemob=text(title,21,col).move_to([x,-1.78,0]);desc=text(description,15,MUTED).move_to([x,-2.16,0]);sym=text(symbol,22,col).move_to([x+1.5,-1.79,0])
   def card_visible(t,i):return t>=26 if i==0 else t>=50 if i==1 else t>=67
   titlemob.add_updater(lambda m,i=i:m.set_opacity(1 if card_visible(now(),i) else 0));self.add(titlemob)
   def update_desc(m,i=i,x=x,description=description):
    t=now();label=description if t<110 else ['반례 z의 좌표','배율 2 · 0.5는 그대로','입력 z에 따른 출력 Az'][i] if t<138 else ['입력의 성분은 ?','배율은 고정','오차가 섞인 관측 출력' if t>=146 else '알고 있는 것은 출력뿐'][i]
    m.become(cached(label,15,MUTED).move_to([x,-2.16,0]));m.set_opacity(1 if card_visible(t,i) else 0)
   desc.add_updater(update_desc);self.add(desc)
   sym.add_updater(lambda m:m.set_opacity(1 if now()>=99 else 0));self.add(sym)
  for px,threshold in [(-2.225,50),(2.225,67)]:
   forward=text('→',22,TEAL).move_to([px,-2.03,0]);back=text('←',22,ORANGE).move_to([px,-2.03,0])
   forward.add_updater(lambda m,threshold=threshold:m.set_opacity(1 if threshold<=now()<138 else 0));back.add_updater(lambda m:m.set_opacity(1 if now()>=138 else 0));self.add(forward,back)
  # Context formula in its own band, entirely above the narration subtitle.
  captions=[(0,7,'입력 v₁: 30°    /    입력 v₂: 120°',INK),(7,13,'A v₁ = 2 u₁    /    A v₂ = 0.5 u₂',INK),(13,26,'주 실험: x = v₁ + v₂ · 입력 벡터는 고정',ORANGE),(26,33,'스칼라 c₁ = 1    /    투영 벡터는 c₁v₁',GOLD),(33,36,'스칼라 c₂ = 1    /    투영 벡터는 c₂v₂',PURPLE),(36,42,'x = c₁v₁ + c₂v₂ = v₁ + v₂',ORANGE),(42,46,'같은 x · 표준 좌표 (0.3660, 1.3660) ↔ 기준 좌표 (1, 1)',ORANGE),(46,50,'읽어낸 계수 두 개를 별도 경로로 처리한다',INK),(50,58,'첫 번째 ×2    /    두 번째 ×0.5',INK),(58,62,'같은 계수 1 · 서로 다른 배율',INK),(62,67,'(2, 0.5)는 스칼라 좌표 · 아직 출력 벡터가 아니다',MUTED),(67,77,'2 → 2u₁    /    0.5 → 0.5u₂',INK),(77,80,'방향과 길이는 유지 · 두 번째 벡터를 평행이동',INK),(80,87,'A x = (2c₁)u₁ + (0.5c₂)u₂ = 2u₁ + 0.5u₂',TEAL),(87,99,'하나의 계산을 읽기 → 배율 → 조립으로 나눠 보았다',INK),(99,103,'x → Vᵀx → ΣVᵀx → UΣVᵀx',INK),(103,108,'A = U Σ Vᵀ',TEAL),(108,110,'특잇값 분해 · Singular Value Decomposition',TEAL),(110,113,'주 실험 x는 고정 · 별도 반례 z를 비교한다',BLUE_IN),(113,119,'큰 배율 2 × 입력 성분 0 = 출력 기여 0',GOLD),(119,125,'작은 배율 0.5 × 입력 성분 1 = 출력 기여 0.5',PURPLE),(125,138,'행렬의 반응 능력과 특정 입력의 실제 기여는 다르다',INK),(138,146,'출력의 성분을 거꾸로 읽으면, 원래 값을 알아낼 수 있을까?',INK),(146,152,'작게 전달한 성분을 다시 확대하면, 오차는 어떻게 될까?',ORANGE)]
  for lo,hi,label,col in captions:
   m=text(label,20,col).move_to([0,-2.84,0]);m.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0));self.add(m)
  self.add(Rectangle(width=14.23,height=.87,fill_color='#070D16',fill_opacity=1,stroke_width=0).move_to([0,-3.55,0]))
  for rec in SENTENCES:
   if rec['end']<=self.start_time or rec['start']>=self.end_time:continue
   m=text('\n'.join(textwrap.wrap(rec['text'],49)),21).move_to([0,-3.52,0])
   if m.width>13.1:m.scale_to_fit_width(13.1)
   if m.height>.73:m.scale_to_fit_height(.73)
   m.add_updater(lambda m,r=rec:m.set_opacity(1 if r['start']<=now()<r['end'] else 0));self.add(m)
  self.update_mobjects(0)
  self.play(clock.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)
