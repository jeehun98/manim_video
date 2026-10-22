"""28 replaceable scenes driven by the same absolute clock and numerical models."""
import json,math,textwrap
from pathlib import Path
import numpy as np
from manim import *
config.background_color='#09121F';config.frame_width=128/9;config.frame_height=8
ROOT=Path(__file__).resolve().parent;FONT='Malgun Gothic'
INK='#EDF4FC';MUTED='#8EA3BA';BLUE_IN='#64AEFF';TEAL='#51D9C5';ORANGE='#FFAB70';GOLD='#FFD077';PURPLE='#BC9AFF';BG='#09121F'
SENTENCES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['sentences']
CHECK=json.loads((ROOT/'assets/numerical_checks.json').read_text(encoding='utf-8'))
def txt(s,n=24,c=INK):return Text(s,font=FONT,font_size=n,color=c,line_spacing=1.1)
def clamp(x):return max(0,min(1,x))
def mix(a,b,t):return a+(b-a)*clamp(t)

class Overlay:
 def setup_overlay(self,clock,fixed=False):
  self.clock=clock;self.fixed=fixed
  self.put(txt('사라진 정보는 복원할 수 있을까?',32).move_to([0,3.43,0]))
  self.put(txt('관측 실험  /  05     소실 · 선택 · 근사',15,MUTED).move_to([0,3.87,0]))
  self.put(Line([-6.65,2.98,0],[6.65,2.98,0],color='#25364B',stroke_width=1))
  self.put(Rectangle(width=128/9,height=.87,fill_color='#060D16',fill_opacity=1,stroke_width=0).move_to([0,-3.55,0]))
  for s in SENTENCES:
   if self.over(s['start'],s['end']):
    m=txt('\n'.join(textwrap.wrap(s['text'],49)),21)
    if m.width>13.1:m.scale_to_fit_width(13.1)
    if m.height>.73:m.scale_to_fit_height(.73)
    self.show(m.move_to([0,-3.52,0]),s['start'],s['end'])
 def over(self,lo,hi):return hi>self.start_time and lo<self.end_time
 def put(self,m):
  if self.fixed:self.add_fixed_in_frame_mobjects(m)
  else:self.add(m)
  return m
 def show(self,m,lo=0,hi=251):
  if not self.over(lo,hi):return m
  styles=[(child,child.get_fill_opacity(),child.get_stroke_opacity()) for child in m.family_members_with_points() if isinstance(child,VMobject)]
  def visibility(mob):
   on=lo<=self.clock.get_value()<hi
   if styles:
    for child,fill,stroke in styles:child.set_fill(opacity=fill if on else 0);child.set_stroke(opacity=stroke if on else 0)
   else:mob.set_opacity(1 if on else 0)
  m.add_updater(visibility);self.put(m);return m
 def label(self,s,x,y,n=24,c=INK,lo=0,hi=251):
  if self.over(lo,hi):
   m=txt(s,n,c).move_to([x,y,0])
   if abs(abs(x)-3.65)<.01 and .6<y<2.1:m.add_background_rectangle(color='#101E2D',opacity=.95,buff=.04)
   return self.show(m,lo,hi)
 def note(self,s,lo,hi,c=MUTED):self.label(s,0,-2.83,19,c,lo,hi)

class LossScene(Overlay,Scene):
 start_time=0;end_time=251
 def construct(self):
  c=ValueTracker(self.start_time);self.add(c);self.setup_overlay(c);now=lambda:c.get_value()
  def stage(lo,hi):return self.over(lo,hi)
  def panel(cx,w=5.8):self.put(RoundedRectangle(width=w,height=4.36,corner_radius=.16,fill_color='#101E2D',fill_opacity=1,stroke_color='#2A3D54',stroke_width=1).move_to([cx,.52,0]))
  # Content panels are below titles and above the statement/caption bands.
  if self.start_time<131 or 205<=self.start_time<231:
   for x in [-3.65,3.65]:panel(x)
  def plane(cx,lo,hi):
   if not stage(lo,hi):return
   o=np.array([cx,.15,0]);u=.9
   for p,q in [([-2.25,0],[2.25,0]),([0,-1.55],[0,2.05])]:
    self.show(Arrow(o+[*np.array(p)*u,0],o+[*np.array(q)*u,0],buff=0,color=MUTED,stroke_width=1,max_tip_length_to_length_ratio=.025),lo,hi)
   self.show(Dot(o,radius=.025,color=MUTED),lo,hi)
  def point(cx,v):return np.array([cx,.15,0])+.9*np.array([v[0],v[1],0])
  def dynamic_dot(cx,fn,col,lo,hi,r=.065):
   if not stage(lo,hi):return
   m=Dot(point(cx,fn(now())),radius=r,color=col)
   m.add_updater(lambda m:m.move_to(point(cx,fn(now()))));self.show(m,lo,hi)
  def seg(cx,v,w,col,lo,hi,width=3):
   if stage(lo,hi):self.show(Line(point(cx,v),point(cx,w),color=col,stroke_width=width),lo,hi)
  def image(name,x,y,h,lo,hi):
   if stage(lo,hi):
    m=ImageMobject(str(ROOT/'assets'/f'{name}.png')).set_height(h).move_to([x,y,0]);self.show(m,lo,hi)
    self.show(Rectangle(width=m.width+.04,height=m.height+.04,stroke_color='#58708A',stroke_width=1,fill_opacity=0).move_to(m),lo,hi)
  def chip(s,x,y,col,lo,hi,w=3.6):
   if stage(lo,hi):
    self.show(RoundedRectangle(width=w,height=.68,corner_radius=.1,fill_color='#162638',fill_opacity=1,stroke_color=col,stroke_width=1).move_to([x,y,0]),lo,hi);self.label(s,x,y,21,col,lo,hi)
  if stage(0,58) or stage(85,131):
   lo=0 if self.start_time<58 else 85;hi=58 if lo==0 else 131
   plane(-3.65,lo,hi);plane(3.65,lo,hi)
   self.label('입력 공간',-3.65,2.45,21,BLUE_IN,lo,hi);self.label('관찰 가능한 출력',3.65,2.45,21,TEAL,lo,hi)
   self.label('A = diag(1, 0)',0,-2.12,26,INK,lo,hi)
   self.label('→',0,.6,35,MUTED,lo,hi)
   def tval(t):
    if t<17:return mix(0,1,(t-1)/5)
    if t<37:return 1.5*math.sin((t-17)*.55)
    if t<58:return .9+.45*math.sin((t-39)*.6)
    if t<103:return 1.4*math.sin((t-85)*.5)
    if t<110:return 1.4
    if t<117:return mix(1.4,0,(t-110)/5)
    return 0
   dynamic_dot(-3.65,lambda t:[1,tval(t)],BLUE_IN,lo,hi)
   dynamic_dot(3.65,lambda t:[1,0],TEAL,lo,hi)
   self.label('y = (1, 0)',3.65,-1.25,22,TEAL,lo,min(hi,117))
   self.label('x = (1, t)',-3.65,-1.25,22,BLUE_IN,lo,hi)
   if stage(25,58) or stage(85,131):
    aa=max(lo,25)
    seg(-3.65,[1,-1.5],[1,2.0],BLUE_IN,aa,hi)
    for y in np.linspace(-1.4,1.9,12):dynamic_dot(-3.65,lambda t,y=y:[1,y],BLUE_IN,aa,hi,.026)
    for y,di in [(-1.5,-1),(2.,1)]:self.show(Arrow(point(-3.65,[1,y-di*.3]),point(-3.65,[1,y]),buff=0,color=BLUE_IN,stroke_width=1,tip_length=.09),aa,hi)
   if stage(37,58):
    seg(-3.65,[0,-1.5],[0,2],PURPLE,44,58)
    self.label('ker(A)',-4.5,1.63,22,PURPLE,44,58)
    self.label('원점을 지나는 차이 벡터의 공간',-3.65,-.87,15,PURPLE,44,58)
    self.label('Ax = y',-2.25,1.63,19,BLUE_IN,44,58)
    self.label('Av = 0',3.65,1.7,26,PURPLE,39,58)
    self.label('A(x + v) = Ax + Av = Ax',3.65,1.12,19,INK,44,58)
   self.note('서로 다른 입력 → 같은 출력',0,25,TEAL)
   self.note('해 집합: x₀ + ker(A) = {(1, t) : t ∈ ℝ}',25,37,BLUE_IN)
   self.note('추가한 차이 v = (0, t)만 0으로 보내진다',37,44,PURPLE)
   self.note('Null Space ≠ 해 집합  ·  원점 통과 여부를 구분',44,54,PURPLE)
   self.note('세로 변화는 출력에 흔적을 남기지 않는다',54,58,TEAL)
   # Pseudoinverse selects a candidate; it does not reveal the actual hidden t.
   self.label('실제 입력은 어느 점일까?',-3.65,1.96,20,GOLD,85,96)
   self.label('출력만으로 특정 불가',3.65,1.8,25,ORANGE,85,96)
   self.label('Pseudoinverse  A⁺',3.65,1.83,26,GOLD,96,117)
   self.label('σ > 0  →  1 / σ',3.65,1.16,23,TEAL,103,110)
   self.label('σ = 0  →  0',3.65,.67,23,PURPLE,103,110)
   self.label('해 선택: x̂ = A⁺y',3.65,.68,25,GOLD,110,117)
   self.label('x̂ = (1, 0)',3.65,-.68,24,GOLD,110,117)
   if stage(110,117):
    line=Line(point(-3.65,[0,0]),point(-3.65,[1,1.4]),color=GOLD,stroke_width=3)
    line.add_updater(lambda m:m.put_start_and_end_on(point(-3.65,[0,0]),point(-3.65,[1,tval(now())])));self.show(line,110,117)
   dynamic_dot(-3.65,lambda t:[1,0],GOLD,115,131,.09)
   self.note('원래 입력을 알아내는 것과 해를 선택하는 것은 다르다',85,103,GOLD)
   self.note('A⁺ = VΣ⁺Uᵀ  ·  0의 역수는 계산하지 않는다',103,110,GOLD)
   self.note('정확해 중 최소 노름: ‖(1, t)‖² = 1 + t²  →  t = 0',110,117,GOLD)
   if stage(117,124):
    dynamic_dot(3.65,lambda t:[1,.3],ORANGE,117,124,.065)
    seg(3.65,[-2,0],[2,0],TEAL,117,124,2)
    seg(3.65,[1,0],[1,.3],GOLD,117,124,4)
    self.label('새 관측 y = (1, 0.3)',3.65,1.84,24,ORANGE,117,124)
    self.label('가장 가까운 Ax = (1, 0)',3.65,1.2,20,TEAL,117,124)
    self.label('최소 잔차 = 0.3',3.65,-1.25,22,GOLD,117,124)
    self.label('t가 달라도 잔차는 같다',-3.65,1.95,18,MUTED,117,124)
   self.note('치역 밖의 관측: 먼저 최소제곱, 그 해들 중 최소 노름',117,124,GOLD)
   self.label('x̂ = (1, 0)',3.65,1.7,31,GOLD,124,131)
   self.label('보이지 않는 성분을 0으로 선택',3.65,1.03,19,PURPLE,124,131)
   self.label('실제 세로 성분은 여전히 알 수 없다',3.65,-1.25,17,ORANGE,124,131)
   self.note('최소 노름 선택 ≠ 사라진 정보의 복원',124,131,ORANGE)
  # Deliberate removal: six known singular components, then actual matrices.
  if stage(131,161):
   self.label('행렬이 지운 차이  →  우리가 버릴 성분',0,2.45,26,GOLD,131,141)
   self.label('A = Σᵢ σᵢuᵢvᵢᵀ',0,2.45,30,INK,141,152)
   for i,s in enumerate([8,4,2,1,.5,.2]):
    x=-5.35+i*2.14
    image(f'component{i+1}',x,.9,1.62,131,152)
    self.label(f'σ{i+1} = {s:g}',x,1.99,18,TEAL if i<3 else PURPLE,131,152)
    self.label('rank 1',x,-.18,16,MUTED,141,152)
    if stage(131,152):
     h=s*.17;self.show(Rectangle(width=.65,height=h,fill_color=TEAL if i<3 else PURPLE,fill_opacity=1,stroke_width=0).move_to([x,-1.7+h/2,0]),131,152)
    if i>=3:
     self.show(Line([x-.7,.23,0],[x+.7,1.6,0],color=ORANGE,stroke_width=4),148,152)
   self.note('주어진 A는 유지하고, 일부 성분을 뺀 새 행렬 Aₖ를 만든다',131,141,GOLD)
   self.note('각 항은 랭크 1 행렬  ·  큰 성분 3개를 유지',141,152,TEAL)
   for x,name,title,col in [(-4.45,'matrix_original','원래 행렬 A · rank 6',BLUE_IN),(0,'matrix_rank3','근사 A₃ · rank 3',TEAL),(4.45,'matrix_error','차이 A − A₃',PURPLE)]:
    image(name,x,.45,2.85,152,161);self.label(title,x,2.35,22,col,152,161)
   self.label('A₃ = Σᵢ₌₁³ σᵢuᵢvᵢᵀ',0,-1.55,29,TEAL,152,161)
   self.note('Low-Rank Approximation  ·  제곱 오차 = 1² + 0.5² + 0.2² = 1.29',152,161,TEAL)
  if stage(161,176) or stage(231,239):
   lo,hi=(161,176) if self.start_time<176 else (231,239)
   self.label('같은 원본으로 계산한 절단 SVD',0,2.45,26,TEAL,lo,hi)
   image('photo_original',-3.65,.15,3.35,lo,hi);self.label('원본 · 192 × 160 픽셀',-3.65,2.12,18,BLUE_IN,lo,hi)
   phases=[(161,165,None),(165,169,1),(169,170.5,2),(170.5,172,5),(172,174.5,10),(174.5,176,None)] if lo==161 else [(231,233,10),(233,235,5),(235,237,2),(237,239,1)]
   for a,b,k in phases:
    image('photo_original' if k is None else f'photo_rank{k}',3.65,.15,3.35,a,b)
    self.label('원본' if k is None else f'Rank {k}',3.65,2.12,22,TEAL,a,b)
    if k:self.label(f"상대 Frobenius 오차 {CHECK['photo_errors'][str(k)]['relative_frobenius']*100:.1f}%",3.65,-1.9,18,GOLD,a,b)
   self.note('블러 효과 없이 실제 SVD 성분의 합으로 계산',lo,hi,TEAL)
  if stage(176,191):
   self.label('별도 수치 예: σ = (8, 4, 2)',0,2.45,27,INK,176,191)
   for x,title,keep,drop,err,col in [(-3.65,'큰 성분 두 개','8, 4','2',4,TEAL),(3.65,'큰 성분 하나 + 작은 성분','8, 2','4',16,ORANGE)]:
    self.label(title,x,1.8,23,col,176,187);chip('둘 다 Rank 2',x,1.14,col,176,187)
    self.label(f'유지 {keep}  /  버림 {drop}',x,.43,22,col,176,187)
    self.show(Rectangle(width=err*.19,height=.38,fill_color=col,fill_opacity=1,stroke_width=0).move_to([x-1.55+err*.095,-.43,0]),176,187)
    self.label(f'제곱 오차 = {err}',x,-1.18,29,col,176,187)
   self.note('모든 rank ≤ k 행렬 중 Frobenius 오차 최소  ·  Eckart–Young–Mirsky',178,187,GOLD)
   self.label('‖A − Aₖ‖²',-1.8,1.25,39,GOLD,187,191)
   self.label('F',-.56,.98,20,GOLD,187,191)
   self.label('= ∑ σᵢ²',1.48,1.25,39,GOLD,187,191)
   self.label('i > k',1.38,.76,16,GOLD,187,191)
   self.label('k = 2  →  버린 성분 2  →  오차 2² = 4',0,.2,27,TEAL,187,191)
   self.label('단순합이 아니라 제곱합',0,-1,27,PURPLE,187,191)
   self.note('제곱 오차의 기준: Frobenius norm의 제곱',187,191,MUTED)
  if stage(191,205):
   self.label('별도 검증 실험: 작은 표식이 있는가?',0,2.45,25,GOLD,191,205)
   for x,name,title,score,col in [(-3.65,'marker_original','원본 · rank 2','표식 점수 0.15',BLUE_IN),(3.65,'marker_rank1','최적 rank 1 근사','표식 점수 0',TEAL)]:
    image(name,x-.65,.65,2.25,191,205);image(name+'_zoom',x+1.35,.65,1.1,195,205)
    self.label(title,x,1.99,22,col,191,205)
    self.label('표식 주변 ×4',x+1.35,-.12,13,MUTED,195,205)
    self.label(score,x,-1.03,23,col,195,205)
   self.label('σ₁ = 8   /   σ₂ = 0.3',0,-1.72,24,PURPLE,191,205)
   self.label('제곱 오차 0.09  ·  상대 오차 3.75%  ·  표식 판별은 실패',0,-2.22,20,GOLD,195,205)
   self.note('가장 적게 잃는다는 것은, 무엇을 손실로 측정하느냐에 달려 있다',200,205,GOLD)
  if stage(205,231):
   plane(-3.65,205,231);plane(3.65,205,231)
   self.label('입력 차이 Δx',-3.65,2.45,23,BLUE_IN,205,231);self.label('출력 차이 AΔx',3.65,2.45,23,TEAL,205,231)
   theta=lambda t:(t-205)*.65
   vec=lambda t:np.array([math.cos(theta(t)),math.sin(theta(t))])
   dynamic_dot(-3.65,lambda t:[0,0],BLUE_IN,205,217);dynamic_dot(-3.65,vec,BLUE_IN,205,217)
   dynamic_dot(3.65,lambda t:[0,0],TEAL,205,217);dynamic_dot(3.65,lambda t:vec(t)*[1,.1],TEAL,205,217)
   self.label('‖Δx‖ = 1',-3.65,-1.24,24,BLUE_IN,205,217);self.label('A = diag(1, 0.1)',3.65,-1.24,23,TEAL,205,217)
   self.note('같은 크기의 입력 차이, 방향에 따라 다른 출력 차이',205,217,GOLD)
   if stage(217,224):
    for cx,sc,col in [(-3.65,[1,1],BLUE_IN),(3.65,[1.6,.5],TEAL)]:
     shape=VMobject().set_points_as_corners([point(cx,np.array([math.cos(a),math.sin(a)])*sc) for a in np.linspace(0,TAU,145)]).set_stroke(col,2)
     self.show(shape,217,224)
     for j in [0,1]:
      v=np.zeros(2);v[j]=sc[j];seg(cx,-v,v,GOLD if j==0 else PURPLE,217,224)
    self.label('v₁, v₂  ·  입력의 직교 방향',-3.65,-1.24,21,BLUE_IN,217,224)
    self.label('σ₁u₁, σ₂u₂  ·  출력 반응',3.65,-1.24,21,TEAL,217,224)
    self.note('Avᵢ = σᵢuᵢ  →  A = UΣVᵀ',217,224,GOLD)
   self.label('σ = 0.001 ≠ 0',-3.65,1.7,29,BLUE_IN,224,231)
   self.label('역배율 ×1000',-3.65,.9,28,GOLD,224,231)
   self.label('오차도 함께 증폭',-3.65,-.65,24,ORANGE,224,231)
   self.label('σ = 0',3.65,1.7,29,PURPLE,224,231)
   self.label('서로 다른 입력 → 같은 출력',3.65,.9,22,TEAL,224,231)
   self.label('출력만으로 복원 불가',3.65,-.65,24,ORANGE,224,231)
   self.note('약하게 남은 차이와 완전히 사라진 차이는 다르다',224,231,GOLD)
  if stage(239,251):
   self.label('A = UΣVᵀ',0,1.91,55,INK,239,251)
   for x,s,body,col,at in [(-4.4,'Vᵀ','입력의 방향별\n성분을 읽는다',BLUE_IN,239),(0,'Σ','방향별 차이를\n확대 · 축소 · 소실',GOLD,242),(4.4,'U','출력 공간의\n방향으로 조립한다',TEAL,245)]:
    chip(s,x,.5,col,at,251);self.label(body,x,-.55,23,col,at,251)
   self.label('무엇을 구별하고, 무엇을 복원하거나 포기할 수 있을까?',0,-1.8,23,MUTED,246,251)
   self.note('SVD — 행렬은 어떤 차이를 남기고, 어떤 차이를 잃는가?',249,251,GOLD)
  c.set_value(self.start_time);self.play(c.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)

class RankScene(Overlay,ThreeDScene):
 start_time=58;end_time=85
 def construct(self):
  c=ValueTracker(self.start_time);self.add(c);self.setup_overlay(c,fixed=True)
  self.set_camera_orientation(phi=65*DEGREES,theta=-52*DEGREES,zoom=.85)
  axes=ThreeDAxes(x_range=[-1.5,1.5,1],y_range=[-1.5,1.5,1],z_range=[-1.5,1.5,1],x_length=5,y_length=5,z_length=5,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False})
  self.add(axes)
  def scales(t):
   if t<63:return np.ones(3)
   if t<65:return np.array([1.,mix(1,.7,(t-63)/2),mix(1,.4,(t-63)/2)])
   if t<70:return np.array([1.,.7,.4])
   if t<72:return np.array([1.,.7,mix(.4,0,(t-70)/2)])
   if t<74:return np.array([1.,.7,0.])
   if t<76:return np.array([1.,mix(.7,0,(t-74)/2),0.])
   if t<79:return np.array([1.,0.,0.])
   if t<81:return np.array([1.,.7,0.])
   if t<83:return np.array([1.,.7,.4])
   return np.array([1.,0.,0.])
  # Real world-space 3D geometry. Interior points make the unit ball, not only a shell.
  sphere=Sphere(radius=1,resolution=(8,12),fill_opacity=.16,stroke_width=.45,stroke_opacity=.45,color=TEAL)
  # Direct per-point affine scaling is robust at EXACT zero; never invert a scale.
  base=[(m,m.points.copy()) for m in sphere.family_members_with_points()]
  def update_shape(m):
   s=scales(c.get_value())
   for child,points in base:child.set_points(points*s*1.667)
  sphere.add_updater(update_shape);self.add(sphere)
  grid=np.array([p for p in np.ndindex(5,5,5)],dtype=float)/2-1;grid=grid[np.sum(grid**2,axis=1)<=1.001]
  cloud=VGroup(*[Dot3D(point=p*1.667,radius=.035,resolution=(2,3),color=TEAL) for p in grid])
  for m,p in zip(cloud,grid):m.add_updater(lambda m,p=p:m.move_to(p*scales(c.get_value())*1.667))
  self.add(cloud)
  # A filled disk appears only when the third singular value is exactly zero.
  disk=Circle(radius=1,fill_color=TEAL,fill_opacity=.22,stroke_color=TEAL,stroke_width=2).scale([1.667,1.167,1])
  disk.add_updater(lambda m:m.set_opacity(.6 if np.array_equal(scales(c.get_value()),[1,.7,0]) else 0));self.add(disk)
  line=Line([-1.667,0,0],[1.667,0,0],color=TEAL,stroke_width=5)
  line.add_updater(lambda m:m.set_opacity(1 if np.array_equal(scales(c.get_value()),[1,0,0]) else 0));self.add(line)
  for lo,hi,title,sg,rk in [(58,63,'3차원 단위공과 세 독립 방향','(1, 1, 1)',3),(63,65,'방향별 배율을 적용한다','(1, 1, 1) → (1, 0.7, 0.4)',3),(65,70,'부피가 있는 타원체','(1, 0.7, 0.4)',3),(70,72,'세 번째 특잇값을 0으로','σ₃ : 0.4 → 0',3),(72,74,'한 방향 소실 → 채워진 원판','(1, 0.7, 0)',2),(74,76,'두 번째 특잇값도 0으로','σ₂ : 0.7 → 0',2),(76,79,'두 방향 소실 → 선분','(1, 0, 0)',1),(79,81,'평면에서 움직이는 독립 방향 두 개','(1, 0.7, 0)',2),(81,83,'공간에서 움직이는 독립 방향 세 개','(1, 0.7, 0.4)',3),(83,85,'선 위에서 움직이는 독립 방향 한 개','(1, 0, 0)',1)]:
   self.label(title,0,2.52,24,TEAL,lo,hi);self.label('특잇값 '+sg,0,-1.98,24,INK,lo,hi);self.label(f'Rank {rk}',4.8,1.6,31,GOLD,lo,hi)
  self.note('Rank = 0이 아닌 특잇값의 개수  ·  작은 값과 0은 다르다',58,85,GOLD)
  self.play(c.animate.set_value(self.end_time),run_time=self.end_time-self.start_time,rate_func=linear)
