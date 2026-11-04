"""Exact inverse experiments: absolute error, relative sensitivity, then loss of uniqueness."""
import json,math,textwrap
from pathlib import Path
import numpy as np
from manim import *
config.background_color='#09121F';config.frame_width=128/9;config.frame_height=8
FONT='Malgun Gothic';INK='#EDF4FC';MUTED='#8EA3BA';BLUE_IN='#64AEFF';TEAL='#51D9C5';ORANGE='#FFAB70';GOLD='#FFD077';PURPLE='#BC9AFF'
ROOT=Path(__file__).resolve().parent
SENTENCES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['sentences']
A=np.diag([1.,.001]);A_UNIFORM=.001*np.eye(2);A_ZERO=np.diag([1.,0.])
def rotation(d):
 a=math.radians(d);return np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
OLD_A=rotation(60)@np.diag([2.,.5])@rotation(-30)
OLD_X=rotation(30)@np.ones(2)
def absolute_case():
 x=np.array([0.,1.]);y=A@x;dy=np.array([0.,.0001]);observed=y+dy;restored=np.linalg.solve(A,observed)
 return x,y,dy,observed,restored

def relative_case(horizontal=False):
 x=np.array([1.,0.]);y=A@x;dy=np.array([.001,0.]) if horizontal else np.array([0.,.001]);observed=y+dy;restored=np.linalg.solve(A,observed)
 return x,y,dy,observed,restored

def relative_metrics(horizontal=False):
 x,y,dy,_,restored=relative_case(horizontal)
 ey=np.linalg.norm(dy)/np.linalg.norm(y);ex=np.linalg.norm(restored-x)/np.linalg.norm(x)
 return ey,ex,ex/ey

def text(s,n=23,c=INK):return Text(s,font=FONT,font_size=n,color=c,line_spacing=1.1)

class InverseScene(Scene):
 start_time=0;end_time=176
 def construct(self):
  clock=ValueTracker(self.start_time);now=lambda:clock.get_value();self.add(clock)
  def intersects(lo,hi):return hi>self.start_time and lo<self.end_time
  def visible(m,lo,hi,stroke=False):
   if not intersects(lo,hi):return
   if stroke:m.add_updater(lambda m,lo=lo,hi=hi:m.set_stroke(opacity=1 if lo<=now()<hi else 0))
   else:m.add_updater(lambda m,lo=lo,hi=hi:m.set_opacity(1 if lo<=now()<hi else 0))
   self.add(m)
  def label(s,p,n=22,c=INK,lo=0,hi=176):
   if intersects(lo,hi):
    mob=text(s,n,c).move_to(p)
    if abs(abs(p[0])-4.65)<.05 and .65<=p[1]<=2.25:mob.add_background_rectangle(color='#101E2D',opacity=1,buff=.045)
    visible(mob,lo,hi)
  self.add(text('출력에 남은 정보를 되돌리면 왜 오차가 커질까?',31).move_to([0,3.43,0]),text('관측 실험  /  04     절대 오차와 상대 민감도',15,MUTED).move_to([0,3.87,0]),Line([-6.65,2.98,0],[6.65,2.98,0],color='#25364B',stroke_width=1))
  L=np.array([-4.65,.28,0]);R=np.array([4.65,.28,0]);unit=1.0
  def world(o,v):return o+unit*np.array([*v,0])
  for cx in [-4.65,0,4.65]:self.add(RoundedRectangle(width=4.14,height=3.86,corner_radius=.15,stroke_color='#2A3D54',stroke_width=1.1,fill_color='#101E2D',fill_opacity=1).move_to([cx,.56,0]))
  for lo,hi,lh,ch,rh in [(0,85,'입력·복원 공간','행렬과 역연산','출력·관측 공간'),(85,114,'모든 방향 동일 압축','방향별 역배율 비교','특정 방향만 압축'),(114,153,'별도 실험: 입력·복원','상대 오차와 조건수','별도 실험: 출력·관측'),(153,176,'서로 다른 입력','정확히 0이면?','같은 출력')]:
   label(lh,[-4.65,2.7,0],20,BLUE_IN,lo,hi);label(ch,[0,2.7,0],20,INK,lo,hi);label(rh,[4.65,2.7,0],20,TEAL,lo,hi)
  for o in [L,R]:
   self.add(Arrow(o+[-1.62,0,0],o+[1.62,0,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.03),Arrow(o+[0,-.87,0],o+[0,1.8,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.03),Dot(o,radius=.03,color=MUTED))
  def arrow(o,v,col,lo,hi,width=3):
   if not intersects(lo,hi):return
   v=np.asarray(v);end=world(o,v)
   if np.linalg.norm(v)>=.005:mob=Arrow(o,end,buff=0,color=col,stroke_width=width,tip_length=.12,max_tip_length_to_length_ratio=.14)
   else:mob=Line(o,end,color=col,stroke_width=width)
   visible(mob,lo,hi);visible(Dot(end,radius=.035,color=col),lo,hi)
  def connection(start,end,col,lo,hi,width=2):
   if intersects(lo,hi):visible(Line(start,end,color=col,stroke_width=width),lo,hi)
  # Same mathematical scale on both sides; tiny outputs stay tiny here.
  arrow(L,OLD_X,BLUE_IN,0,9);arrow(R,OLD_A@OLD_X,TEAL,0,16)
  x,y,dy,observed,restored=absolute_case()
  arrow(L,x,BLUE_IN,16,85,width=5);arrow(R,y,TEAL,16,85)
  arrow(L,x,TEAL,26,53,width=2);arrow(L,restored,ORANGE,58,85,width=2);arrow(R,observed,ORANGE,44,85,width=2)
  label('실험 공개: 원래 입력 (0, 1)',[-4.65,2.14,0],15,BLUE_IN,16,85)
  label('정확 복원 = 1',[-4.65,-1.13,0],18,TEAL,26,53)
  label('원본 1  /  복원 1.1',[-4.65,-1.13,0],18,ORANGE,58,85)
  label('x₂ = 1',world(L,x)+[-.48,.01,0],16,BLUE_IN,16,85)
  label('1.1',world(L,restored)+[.62,.08,0],17,ORANGE,58,85)
  # The visible error in reconstructed space has its ACTUAL length 0.1.
  p=world(L,x);q=world(L,restored)
  connection(p+[.18,0,0],q+[.18,0,0],GOLD,58,85,3)
  connection(p+[.1,0,0],p+[.26,0,0],GOLD,58,85);connection(q+[.1,0,0],q+[.26,0,0],GOLD,58,85)
  label('절대 복원 오차 0.1',[-4.65,1.84,0],17,GOLD,64,85)
  # Precise numeric output labels; no enlargement of the main coordinate plane.
  label('정확한 출력 성분',[4.65,1.95,0],18,TEAL,20,44);label('0.001',[4.65,1.45,0],32,TEAL,20,44)
  label('가로·세로 축의 척도는 동일',[4.65,-1.13,0],14,MUTED,16,44)
  # Separate magnifier: 0.0001 * 10000 = 1 unit of displayed vertical separation.
  if intersects(44,53):
   magnifier=RoundedRectangle(width=3.26,height=1.86,corner_radius=.12,fill_color='#12303B',fill_opacity=1,stroke_color=TEAL,stroke_width=1.3).move_to([4.65,1.2,0]);visible(magnifier,44,53)
   label('세로 차이 ×10,000 · 별도 척도',[4.65,1.98,0],12,TEAL,44,53)
   for py,val,col in [(.65,'0.001',TEAL),(1.65,'0.0011',ORANGE)]:
    visible(Dot([3.6,py,0],radius=.04,color=col),44,53);label(val,[4.8,py,0],22,col,44,53)
   connection(np.array([3.6,.65,0]),np.array([3.6,1.65,0]),GOLD,44,53)
   label('실제 세로 간격 0.0001',[4.65,-1.13,0],16,GOLD,44,53)
  for px,heading,value,col in [(3.7,'정확 출력','0.001',TEAL),(5.6,'관측 출력','0.0011',ORANGE)]:
   label(heading,[px,1.92,0],16,col,53,85);label(value,[px,1.45,0],24,col,53,85)
  label('실제 출력 차이 = 0.0001',[4.65,-1.13,0],16,GOLD,53,85)
  # Only the INPUT is hidden at the observer setup.
  if intersects(9,16):
   visible(RoundedRectangle(width=4.05,height=3.75,corner_radius=.12,fill_color='#0C1625',fill_opacity=1,stroke_width=0).move_to([-4.65,.56,0]),9,16)
   label('?',[-4.65,.85,0],52,MUTED,9,16);label('입력은 보이지 않는다',[-4.65,.03,0],19,MUTED,9,16)
  # Uniform vs nonuniform case: output bases are drawn at their true 0.001 sizes.
  for o,diag,name,col in [(L,[.001,.001],'A₁ = diag(0.001, 0.001)',TEAL),(R,[1.,.001],'A₂ = diag(1, 0.001)',PURPLE)]:
   label(name,[o[0],1.98,0],17,col,85,114)
   for v in [np.array([1.,0.]),np.array([0.,1.])]:
    if intersects(85,114):visible(DashedLine(o,world(o,v),color=MUTED,stroke_width=1,dash_length=.06),85,114)
    arrow(o,np.array(diag)*v,TEAL if o is L else GOLD if v[0] else PURPLE,85,114,width=3)
   label('출력: 가로 0.001 · 세로 0.001' if o is L else '출력: 가로 1 · 세로 0.001',[o[0],1.43,0],15,col,85,114)
   label('역배율: 가로 ×1000' if o is L else '역배율: 가로 ×1',[o[0],-.66,0],16,col,85,114)
   label('세로 ×1000',[o[0],-1.1,0],16,col,85,114)
  # A genuinely different relative-error experiment; baseline norms are both 1.
  for lo,hi,horizontal in [(114,140,False),(140,147,True),(147,153,False)]:
   xx,yy,ddy,obs,rec=relative_case(horizontal)
   arrow(L,xx,BLUE_IN,lo,hi,width=5);arrow(R,yy,TEAL,lo,hi,width=5);arrow(L,rec,ORANGE,lo,hi,width=2);arrow(R,obs,ORANGE,lo,hi,width=2)
   connection(world(L,xx),world(L,rec),GOLD,lo,hi,3)
   label('기준 x = (1, 0)',[-4.65,2.14,0],16,BLUE_IN,lo,hi)
   label('복원 (1.001, 0)' if horizontal else '복원 (1, 1)',[-4.65,-1.13,0],18,ORANGE,lo,hi)
   label('정확 y = (1, 0)',[4.65,2.14,0],16,TEAL,lo,hi)
   label('관측 (1.001, 0)' if horizontal else '관측 (1, 0.001)',[4.65,-1.13,0],18,ORANGE,lo,hi)
   label('가로 오차 δy = (0.001, 0)' if horizontal else '세로 오차 δy = (0, 0.001)',[4.65,1.55,0],15,ORANGE,lo,hi)
   label('오차를 실제 척도로 표시',[4.65,.99,0],14,MUTED,lo,hi)
   if not horizontal:label('δx = (0, 1)',[-4.03,1.65,0],16,GOLD,lo,hi)
  # At 161s the matrix changes EXACTLY to diag(1,0), not a rounded tiny value.
  if intersects(153,161):
   visible(Circle(radius=unit,fill_opacity=0,color=BLUE_IN,stroke_width=1.5).move_to(L),153,161,stroke=True)
   ellipse=VMobject().set_points_as_corners([world(R,np.array([math.cos(a),.001*math.sin(a)])) for a in np.linspace(0,TAU,721)]).set_stroke(TEAL,width=2)
   visible(ellipse,153,161,stroke=True)
   label('s = 0.001 ≠ 0',[4.65,-1.13,0],19,TEAL,153,161)
   label('세로 단면 ×1000 · 별도 척도',[0,-1.21,0],12,MUTED,153,161)
   connection(np.array([0,-1.1,0]),np.array([0,.9,0]),TEAL,153,161,3)
   for py in [-1.1,.9]:connection(np.array([-.13,py,0]),np.array([.13,py,0]),TEAL,153,161)
  if intersects(161,176):
   visible(Line(world(R,[-1,0]),world(R,[1,0]),color=TEAL,stroke_width=2),161,163)
   for val,col,name,offset in [(0.,BLUE_IN,'x₁ = (1, 0)',[.50,-.28,0]),(1.,ORANGE,'x₂ = (1, 1)',[.50,.18,0])]:
    point=world(L,[1,val]);visible(Dot(point,radius=.045,color=col),161,176);label(name,point+offset,13,col,161,176)
   visible(Dot(world(R,[1,0]),radius=.06,color=TEAL),161,176)
   label('y = (1, 0)',world(R,[1,0])+[-.04,-.3,0],17,TEAL,161,176)
   label('s = 0 · 차이가 완전히 사라짐',[4.65,-1.13,0],17,ORANGE,161,176)
   if intersects(170,176):
    visible(Line(world(L,[1,-.8]),world(L,[1,1.55]),color=MUTED,stroke_width=1.3),170,176)
    for val in [-.8,-.45,-.2,.3,.6,1.3,1.55]:visible(Dot(world(L,[1,val]),radius=.03,color=MUTED),170,176)
  # Central operator/data panel. Only intersecting states are constructed for each scene.
  records=[
   (0,6,[(1.8,'이전 A: 특잇값 2, 0.5',19,INK),(.95,'(1, 1) → (2, 0.5)',24,TEAL),(.1,'읽기 → 배율 → 조립',21,INK),(-.7,'x → Ax',28,TEAL)]),
   (6,9,[(1.7,'순방향에서 역방향으로',21,INK),(.75,'출력에서 입력으로',25,TEAL),(-.2,'x  ←  Ax',30,ORANGE)]),
   (9,16,[(1.7,'알고 있는 것',20,MUTED),(1.13,'행렬 A · 출력 y',27,TEAL),(.12,'찾아야 하는 것',20,MUTED),(-.46,'입력 x',29,BLUE_IN)]),
   (16,26,[(1.8,'새 실험 행렬',20,MUTED),(1.11,'A = diag(1, 0.001)',22,INK),(.22,'1 × 0.001 = 0.001',24,TEAL),(-.75,'세로 방향만 강하게 압축',17,MUTED)]),
   (26,41,[(1.8,'역연산: ÷0.001',23,INK),(.88,'0.001 ÷ 0.001',27,TEAL),(.12,'= 1',34,TEAL),(-.75,'정확한 출력 → 정확한 복원',17,MUTED)]),
   (41,44,[(1.8,'관측이 정확하지 않다면?',21,INK),(1.0,'정확 신호 0.001',27,TEAL),(.15,'측정에 오차가 섞인다면?',20,ORANGE)]),
   (44,50,[(1.8,'오차가 더해진 출력',21,INK),(1.04,'신호 0.001',27,TEAL),(.23,'+ 오차 0.0001',25,ORANGE),(-.7,'두 값 모두 같은 출력에 포함',16,MUTED)]),
   (50,53,[(1.8,'관찰자가 얻은 값',21,INK),(1.05,'0.001 + 0.0001',25,INK),(.23,'= 0.0011',31,ORANGE)]),
   (53,58,[(1.8,'정확값: ÷0.001',18,TEAL),(1.19,'0.001 → 1',27,TEAL),(.29,'관측값: ÷0.001',18,ORANGE),(-.31,'0.0011 → ?',27,ORANGE),(-.99,'서로 구분하지 않는 같은 연산',15,MUTED)]),
   (58,70,[(1.8,'정확값: ÷0.001',18,TEAL),(1.19,'0.001 → 1',27,TEAL),(.29,'관측값: ÷0.001',18,ORANGE),(-.31,'0.0011 → 1.1',27,ORANGE),(-.99,'서로 구분하지 않는 같은 연산',15,MUTED)]),
   (70,85,[(1.8,'신호와 오차에 같은 역연산',19,INK),(1.0,'0.001 + 0.0001',26,INK),(.28,'둘 다 ÷0.001',23,MUTED),(-.42,'1 + 0.1',32,GOLD),(-1.0,'이 예의 상대 오차: 10% → 10%',16,MUTED)]),
   (85,93,[(1.8,'같은 최소 특잇값 0.001',19,INK),(.99,'다른 방향별 격차',25,INK),(.16,'절대 오차는 양쪽 모두',18,MUTED),(-.55,'×1000 확대 가능',26,GOLD)]),
   (93,98,[(1.8,'균일 압축의 역배율',21,INK),(.95,'가로 ×1000',28,TEAL),(.17,'세로 ×1000',28,TEAL),(-.76,'방향별 불균형 없음',18,MUTED)]),
   (98,107,[(1.8,'같은 |δy| = 0.0001',20,INK),(.96,'가로: δx = 0.0001',22,TEAL),(.18,'세로: δx = 0.1',24,GOLD),(-.77,'여전히 절대 오차 비교',17,MUTED)]),
   (107,114,[(1.8,'단위 입력의 출력',21,INK),(1.0,'가로 1 · 세로 0.001',23,INK),(.12,'1 / 0.001 = 1000',26,GOLD),(-.75,'방향별 전달 배율의 격차',17,MUTED)]),
   (114,123,[(1.8,'새 기준: x = y = (1, 0)',19,INK),(1.0,'δy = (0, 0.001)',25,ORANGE),(.25,'δx = (0, 1)',27,GOLD),(-.62,'상대 0.1% → 100%',23,TEAL)]),
   (123,126,[(1.8,'조건수',26,INK),(.94,'Condition Number',23,TEAL),(.1,'상대 오차의 민감도',23,INK),(-.67,'이 사례: 0.1% → 100%',20,GOLD)]),
   (126,140,[(1.83,'가역 정사각행렬 · 2-노름',17,MUTED),(1.0,'κ₂(A) = σmax / σmin',25,INK),(.27,'= 1 / 0.001',26,TEAL),(-.43,'= 1000',33,GOLD),(-1.02,'균일 압축 0.001I는 κ₂ = 1',15,MUTED)]),
   (140,147,[(1.8,'κ₂(A)=1000 · 최악의 경우',18,INK),(.95,'가로 상대 증폭 ×1',24,TEAL),(.12,'세로 상대 증폭 ×1000',22,MUTED),(-.77,'모든 오차가 최악은 아니다',17,MUTED)]),
   (147,153,[(1.8,'κ₂(A)=1000 · 최악의 경우',18,INK),(.95,'가로 상대 증폭 ×1',24,MUTED),(.12,'세로 상대 증폭 ×1000',22,GOLD),(-.77,'오차 방향에 따라 달라진다',17,MUTED)]),
   (153,161,[(1.91,'세로 배율 s',20,INK),(1.31,'0.001 → 0',28,ORANGE)]),
   (161,170,[(1.8,'A₀ = diag(1, 0)',23,INK),(.99,'A₀x₁ = A₀x₂',27,TEAL),(.22,'= (1, 0)',29,TEAL),(-.7,'출력에 구별할 정보가 없다',17,ORANGE)]),
   (170,176,[(1.8,'입력 후보 (1, t)',25,BLUE_IN),(1.0,'t ∈ ℝ',29,INK),(.16,'모든 출력 = (1, 0)',24,TEAL),(-.75,'유일하게 고를 수 있을까?',18,ORANGE)])]
  for lo,hi,rows in records:
   for py,body,size,col in rows:label(body,[0,py,0],size,col,lo,hi)
  # Three measurement cards explicitly change from absolute to relative error units.
  metric_states=[
   (0,16,[('읽기','Vᵀx','이전 계산 구조'),('배율','ΣVᵀx','이전 특잇값 2 · 0.5'),('조립','Ax','이번에는 거꾸로')]),
   (16,26,[('정확 출력','0.001','정확히 0이 아니다'),('변환 배율','×0.001','세로 성분을 압축한다'),('원래 입력 성분','1','실험을 위해 공개한 입력')]),
   (26,41,[('정확 출력','0.001','정확히 0이 아니다'),('역연산','÷0.001','같은 방향을 되돌린다'),('복원 성분','1','정확한 관측을 가정')]),
   (41,44,[('정확 신호','0.001','이 값은 알고 있다'),('관측이 부정확하다면','?','측정 오차를 가정한다'),('복원 결과','?','정확한 결과와 같을까?')]),
   (44,53,[('정확 신호','0.001','출력의 세로 성분'),('측정 오차','+0.0001','작지만 0은 아니다'),('관측값','0.0011','신호와 오차가 함께 있다')]),
   (53,58,[('정확 출력','0.001','역연산 ÷0.001'),('관측 출력','0.0011','같은 역연산 ÷0.001'),('복원 결과','?','동일 연산을 적용한다')]),
   (58,70,[('출력 절대 오차','0.0001','정확 출력과 관측값의 차이'),('복원 절대 오차','0.1','실제 1에서 복원 1.1로'),('절대 증폭','×1000','상대 오차는 10% → 10%')]),
   (70,85,[('출력 절대 오차','0.0001','수학적 차이를 수치로 표시'),('복원 절대 오차','0.1','같은 역연산이 오차에도 적용'),('절대 증폭','×1000','이 예의 상대 오차 10% → 10%')]),
   (85,114,[('균일 압축 역배율','1000 / 1000','가로 · 세로가 같다'),('비균일 압축 역배율','1 / 1000','방향에 따라 달라진다'),('주의','둘 다 절대 증폭 가능','작은 σmin과 방향 격차는 별개')]),
   (114,140,[('출력 상대 오차','0.1%','|δy| / |y| = 0.001 / 1'),('입력 상대 오차','100%','|δx| / |x| = 1 / 1'),('상대 증폭','×1000','별도 사례 · 기준 x = y = (1,0)')]),
   (140,147,[('출력 상대 오차','0.1%','같은 크기 · 가로 오차'),('입력 상대 오차','0.1%','|δx| / |x| = 0.001 / 1'),('실제 상대 증폭','×1','κ₂는 최악의 상한')]),
   (147,153,[('출력 상대 오차','0.1%','같은 크기 · 세로 오차'),('입력 상대 오차','100%','|δx| / |x| = 1 / 1'),('실제 상대 증폭','×1000','이 방향에서 최악에 도달')]),
   (153,161,[('현재 배율','0.001','아직 0이 아니다'),('이제 묻는 것','정확히 0이면?','오차 화살표를 제거한다'),('실험의 전환','불안정 → 정보 소실','숫자가 0이 되는 순간을 구분')]),
   (161,176,[('입력 차이','0이 아님','x₁ ≠ x₂'),('출력 차이','정확히 0','A₀x₁ = A₀x₂'),('문제의 성질','유일한 복원 불가','단순한 오차 증폭과 다르다')])]
  for lo,hi,cards in metric_states:
   if not intersects(lo,hi):continue
   for i,(heading,value,desc) in enumerate(cards):
    px=[-4.45,0,4.45][i];col=[TEAL,ORANGE,GOLD][i]
    visible(RoundedRectangle(width=4.12,height=1.02,corner_radius=.1,fill_color='#12263A',fill_opacity=1,stroke_color='#304A62',stroke_width=1).move_to([px,-2.03,0]),lo,hi)
    label(heading,[px,-1.7,0],16,MUTED,lo,hi);label(value,[px,-2.0,0],23,col,lo,hi);label(desc,[px,-2.34,0],12,MUTED,lo,hi)
  notes=[(0,6,'이전 A의 방향별 계산: 입력 성분 → 특잇값 → 출력',INK),(6,16,'행렬과 출력만 알고, 원래 입력을 알아내야 한다',INK),(16,26,'새 행렬 A = diag(1, 0.001) · 가로는 보존, 세로는 압축',INK),(26,34,'0.001 / 0.001 = 1 · 정확한 출력이면 복원 가능',TEAL),(34,41,'작게 남은 차이 ≠ 완전히 사라진 차이',TEAL),(41,53,'관측값 = 정확한 출력 + 측정 오차',ORANGE),(53,60,'동일한 ÷0.001을 정확값과 관측값에 적용한다',INK),(60,70,'출력 절대 오차 0.0001 → 복원 절대 오차 0.1',GOLD),(70,78,'역변환은 원래 신호와 측정 오차를 구분하지 못한다',INK),(78,85,'(0.001 + 0.0001) / 0.001 = 1 + 0.1',GOLD),(85,98,'균일 압축도 절대 오차는 ×1000 확대할 수 있다',INK),(98,107,'같은 절대 크기의 출력 오차 · 방향에 따라 복원 결과가 다르다',INK),(107,114,'입력 거리 1 → 출력 거리 1 또는 0.001',INK),(114,126,'별도 상대 오차 실험: 기준 신호와 오차의 방향을 구분한다',TEAL),(126,140,'κ₂(A) = σmax / σmin = 1 / 0.001 = 1000',GOLD),(140,153,'조건수는 모든 오차의 실제 배율이 아니라 최악의 상대 민감도',INK),(153,161,'0.001은 아직 0이 아니다 · 정확히 0이 되면 어떨까?',ORANGE),(161,170,'오차 때문이 아니라, 입력의 차이가 출력에서 사라졌다',ORANGE),(170,176,'하나의 출력 (1,0)에 대응하는 입력은 몇 개일까?',INK)]
  for lo,hi,body,col in notes:label(body,[0,-2.87,0],19,col,lo,hi)
  self.add(Rectangle(width=14.23,height=.87,fill_color='#070D16',fill_opacity=1,stroke_width=0).move_to([0,-3.55,0]))
  for rec in SENTENCES:
   if not intersects(rec['start'],rec['end']):continue
   cap=text('\n'.join(textwrap.wrap(rec['text'],49)),21).move_to([0,-3.52,0])
   if cap.width>13.1:cap.scale_to_fit_width(13.1)
   if cap.height>.73:cap.scale_to_fit_height(.73)
   visible(cap,rec['start'],rec['end'])
  self.update_mobjects(0)
  self.play(clock.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)
