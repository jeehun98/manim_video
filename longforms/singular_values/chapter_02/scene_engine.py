from visual_common import *
config.background_color='#10141e'
STARTS=[0,23,51,78,97,106];ENDS=[23,51,78,97,106,121]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class GeometryScene(ThreeDScene):
 index=0
 def to(self,t):
  d=(round((t-STARTS[self.index])*config.frame_rate)-round(self.time*config.frame_rate))/config.frame_rate
  if d>.001:self.wait(d)
  elif d<-.04:raise ValueError((t,self.time))
 def caption_setup(self):
  self.caps={}
  for j,row in enumerate(DATA):
   group=VGroup(*[txt(s,25) for s in textwrap.wrap(row['text'],width=48,break_long_words=False)]).arrange(DOWN,buff=.12)
   if group.width>12.8:group.scale_to_fit_width(12.8)
   group.move_to([0,-3.25,0]);assert group.get_bottom()[1]>-3.98
   self.caps[j]=group
  self.cap=VGroup();self.cap_key=-1
  def update(m,dt):
   t=STARTS[self.index]+self.time
   key=next((j for j,r in enumerate(DATA) if r['start']<=t<r['end']),len(DATA)-1)
   if key!=self.cap_key:
    m.become(self.caps[key]);m.set_z_index(100);self.camera.add_fixed_in_frame_mobjects(m);self.cap_key=key
  self.cap.add_updater(update);self.bar=Rectangle(width=14.22,height=1.3,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-3.35,0]);self.bar.z_index=90;self.cap.z_index=100;self.add(self.bar,self.cap)
 def reset(self,title):
  for m in list(self.mobjects):
   if m not in [self.cap,self.bar]:self.remove(m)
  self.add_fixed_in_frame_mobjects(label(title,[0,3.2,0],32))
 def formula(self,s,y=-2,size=33,color=PURPLE):
  m=label(s,[0,y,0],size,color)
  if m.width>12:m.scale_to_fit_width(12)
  self.add(m);return m
 def pair(self,v=np.array([1.,1.]),scale=.8,y=.4):
  l=np.array([-3.45,y,0]);r=np.array([3.45,y,0]);self.add(grid(l,scale=scale),grid(r,scale=scale),label('입력 벡터 v',l+UP*1.9,25,BLUEC),label('출력 벡터 Av',r+UP*1.9,25,ORANGE),Arrow([-.6,y,0],[.6,y,0]),label('A',[0,y+.5,0],24))
  return l,r
 def bars(self,x,y,length,color):return Line([x,y,0],[x+length,y,0],stroke_width=12,color=color)
 def graph(self,center=[0,-.55,0],width=11.5,height=2.4):
  ax=Axes(x_range=[0,360,90],y_range=[0,3,1],x_length=width,y_length=height,tips=False,axis_config={'stroke_color':MUTED,'stroke_width':1.3}).move_to(center)
  self.add(ax)
  for n in [0,90,180,270,360]:self.add(label(f'{n}°',ax.c2p(n,0)+DOWN*.25,18,MUTED))
  for n in [1,2,3]:self.add(label(str(n),ax.c2p(0,n)+LEFT*.25,18,MUTED))
  self.add(DashedLine(ax.c2p(0,1),ax.c2p(360,1),color=BLUEC,stroke_width=2))
  return ax
 def curve(self,ax,end=360):return ax.plot(lambda x:norm(x*DEGREES),x_range=[0,max(.01,end),1],color=ORANGE,stroke_width=3,use_smoothing=False)
 def ellipse(self,c=np.array([0,.2,0]),scale=1,color=ORANGE):
  return ParametricFunction(lambda t:np.array(c)+np.r_[A@vec(t),0]*scale,t_range=[0,TAU,.025],color=color,stroke_width=3)
 def circle(self,c,scale=1):return Circle(radius=scale,color=BLUEC).move_to(c)
 def spokes(self,c,n=32,M=np.eye(2),scale=1,color=BLUEC):
  return VGroup(*[VGroup(Line(c,np.array(c)+np.r_[M@vec(t),0]*scale,color=color,stroke_width=1.4),Dot(np.array(c)+np.r_[M@vec(t),0]*scale,radius=.025,color=color)) for t in np.linspace(0,TAU,n,endpoint=False)])
 def axes2(self):
  l=np.array([-3.45,.35,0]);r=np.array([3.45,.35,0]);self.add(grid(l),grid(r),label('입력 공간',l+UP*2.05,26,BLUEC),label('출력 공간',r+UP*2.05,26,ORANGE),Arrow([-.6,.35,0],[.6,.35,0]),label('A',[0,.85,0],26));return l,r
 def hud(self,s,p,size=28,color=WHITE):
  m=label(s,p,size,color);self.add_fixed_in_frame_mobjects(m);return m
 def wire(self,d=np.ones(3),color=BLUEC,center=ORIGIN,scale=1.3):
  d=np.array(d);c=np.array(center);g=VGroup()
  for phi in np.linspace(.22,PI-.22,9):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(phi)*np.cos(t),np.sin(phi)*np.sin(t),np.cos(phi)]),t_range=[0,TAU,.12],color=color,stroke_width=1,stroke_opacity=.55))
  for theta in np.linspace(0,TAU,12,endpoint=False):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(t)*np.cos(theta),np.sin(t)*np.sin(theta),np.cos(t)]),t_range=[0,PI,.10],color=color,stroke_width=1,stroke_opacity=.55))
  return g
 def construct(self):
  self.caption_setup();i=self.index
  v1=vec(67.5*DEGREES);v2=vec(157.5*DEGREES);w1=A@v1;w2=A@v2
  if i==0:
   # Same unit circle position and scale as chapter 1's final geometric state.
   self.reset('모든 방향의 단위벡터');c=np.array([0,.2,0]);circle=self.circle(c,1.8);self.add(circle);self.formula('x² + y² = 1',y=-2.15,size=30,color=BLUEC);self.to(2)
   rays=self.spokes(c,8,scale=1.8);self.play(FadeIn(rays),run_time=.6);self.play(Transform(rays,self.spokes(c,32,scale=1.8)),run_time=1.4);self.play(rays.animate.set_opacity(.2),run_time=1);self.to(6)
   self.reset('단위 원');c=np.array([-2.4,.2,0]);self.add(self.circle(c,1.55),arrow(c,np.array([1,0]),BLUEC,1.55),label('1',c+np.array([.8,.3,0]),28,BLUEC),label('단위 원',[2.8,.65,0],43),label('x² + y² = 1',[2.8,-.3,0],32,BLUEC));self.to(8)
   self.reset('모든 방향에 같은 행렬을 적용');l,r=self.axes2();left=self.spokes(l,32,scale=.95);right=self.spokes(r,32,scale=.95);self.add(left,right);self.formula('A(x, y) = (x + 2y, y)',y=-2.2,size=28,color=MUTED);self.play(Transform(right,self.spokes(r,32,A,.95,ORANGE)),run_time=3);self.to(12)
   self.remove(right);self.add(self.spokes(r,32,A,.95,ORANGE).set_opacity(.18));theta=ValueTracker(PI/4);hi=always_redraw(lambda:VGroup(arrow(l,vec(theta.get_value()),BLUEC,.95),arrow(r,A@vec(theta.get_value()),ORANGE,.95)));self.add(hi)
   self.add(label('입력 길이 = 1',l+DOWN*2,27,BLUEC),label('출력 길이 ≈',[2.6,-1.65,0],27,ORANGE));number=DecimalNumber(np.sqrt(5),mob_class=Text,num_decimal_places=3,font_size=30,color=ORANGE).move_to([4.65,-1.65,0]);number.add_updater(lambda m:m.set_value(norm(theta.get_value())));self.add(number);self.play(theta.animate.set_value(TAU+PI/4),run_time=6,rate_func=linear)
   self.reset('끝점을 연결하면 나타나는 타원');l,r=self.axes2();dots1=VGroup(*[Dot(l+np.r_[vec(t),0]*.95,radius=.025,color=BLUEC) for t in np.linspace(0,TAU,64,endpoint=False)]);dots2=VGroup(*[Dot(r+np.r_[A@vec(t),0]*.95,radius=.025,color=ORANGE) for t in np.linspace(0,TAU,64,endpoint=False)]);self.add(dots1,dots2);self.to(20);self.play(Create(self.circle(l,.95)),Create(self.ellipse(r,.95)),run_time=2);self.to(23)
  elif i==1:
   self.reset('타원의 서로 수직인 두 축');c=np.array([0,.3,0]);scale=1.22;ellipse=self.ellipse(c,scale);self.add(grid(c),ellipse)
   major=Line(c-np.r_[w1,0]*scale,c+np.r_[w1,0]*scale,color=PURPLE,stroke_width=4);minor=Line(c-np.r_[w2,0]*scale,c+np.r_[w2,0]*scale,color='#e1c6ff',stroke_width=4)
   self.play(Create(major),run_time=1);self.play(Create(minor),run_time=1);a=w1/np.linalg.norm(w1)*.22;b=w2/np.linalg.norm(w2)*.22;self.add(VMobject(color=WHITE).set_points_as_corners([c+np.r_[a,0],c+np.r_[a+b,0],c+np.r_[b,0]]),label('90°',c+UP*.65,24));self.to(27)
   self.reset('중심에서 가장 멀리, 가장 가까이');self.add(ellipse);theta=ValueTracker(0);radius=always_redraw(lambda:Line(c,c+np.r_[A@vec(theta.get_value()),0]*scale,color=PURPLE,stroke_width=4));point=always_redraw(lambda:Dot(c+np.r_[A@vec(theta.get_value()),0]*scale,color=PURPLE));self.add(radius,point);self.play(theta.animate.set_value(67.5*DEGREES),run_time=3);self.add(major,label('장축',[3.7,1.6,0],30,PURPLE));self.to(31);self.play(theta.animate.set_value(157.5*DEGREES),run_time=2);self.add(minor,label('단축',[-2.2,-1.1,0],30,'#e1c6ff'));self.to(35)
   self.reset('가장 긴 반지름 = 최대 길이 변화 배율');l,r=self.axes2();scale=.95;self.add(self.circle(l,scale),self.ellipse(r,scale));theta=ValueTracker(67.5*DEGREES);ar=always_redraw(lambda:VGroup(arrow(l,vec(theta.get_value()),PURPLE,scale),arrow(r,A@vec(theta.get_value()),PURPLE,scale)));self.add(ar)
   self.add(label('67.5°',l+UP*1.4,25,PURPLE),label('출력 방향 22.5°',r+UP*1.4,25,PURPLE));self.to(38);self.add(label('입력 길이 = 1',l+DOWN*1.8,28,BLUEC),label('출력 길이 ≈ 2.414',r+DOWN*1.8,28,PURPLE));self.to(41);f=self.formula('max ‖Av‖ = 2.414…   (‖v‖ = 1)',y=-2.3,size=29);self.to(44)
   self.reset('가장 짧은 반지름 = 최소 길이 변화 배율');l,r=self.axes2();self.add(self.circle(l,scale),self.ellipse(r,scale));theta=ValueTracker(67.5*DEGREES);ar=always_redraw(lambda:VGroup(arrow(l,vec(theta.get_value()),PURPLE,scale),arrow(r,A@vec(theta.get_value()),PURPLE,scale)));self.add(ar);self.play(theta.animate.set_value(157.5*DEGREES),run_time=1.5);self.add(label('입력 방향 157.5°',l+DOWN*1.85,27,PURPLE),label('출력 길이 ≈ 0.414',r+DOWN*1.85,27,PURPLE));self.formula('min ‖Av‖ = 0.414…   (‖v‖ = 1)',y=-2.35,size=28);self.to(48)
   self.reset('이 두 반축의 길이가 특잇값');c=np.array([0,.8,0]);self.add(self.ellipse(c,1.05),arrow(c,w1,PURPLE,1.05),arrow(c,w2,'#e1c6ff',1.05));self.add(label('σ₁ = 1 + √2 ≈ 2.414',[-3,-1.35,0],31,PURPLE),label('σ₂ = √2 − 1 ≈ 0.414',[3,-2,0],31,'#e1c6ff'));self.to(51)
  elif i==2:
   self.reset('같은 행렬에서 얻는 서로 다른 정보');self.formula('A(x, y) = (x + 2y, y)',y=2.45,size=26,color=MUTED)
   for x,title,value,color in [(-3.4,'고윳값','λ₁ = λ₂ = 1',GREEN),(3.4,'특잇값','σ₁ ≈ 2.414\nσ₂ ≈ 0.414',PURPLE)]:
    self.add(RoundedRectangle(width=5.6,height=3.4,color=color,stroke_width=1).move_to([x,.1,0]),label(title,[x,1.2,0],30,color),label(value,[x,-.05,0],33,color))
   self.to(54);self.reset('고윳값: 원래 놓인 직선 안에서');l,r=self.axes2();self.add(DashedLine(l+LEFT*2.6,l+RIGHT*2.6,color=GREEN),DashedLine(r+LEFT*2.6,r+RIGHT*2.6,color=GREEN),arrow(l,np.array([1,0]),GREEN,1.2),arrow(r,np.array([1,0]),GREEN,1.2));self.formula('Av = λv       λ = 1',color=GREEN);self.to(60)
   self.reset('특잇값: 입력과 출력 방향은 달라도 된다');l,r=self.axes2();self.add(self.circle(l,.95),self.ellipse(r,.95),arrow(l,v1,PURPLE,.95),arrow(r,w1,PURPLE,.95),DashedLine(r,r+np.r_[v1,0]*1.8,color=MUTED),label('입력 방향 67.5°',l+DOWN*1.85,28,PURPLE),label('출력 방향 22.5°',r+DOWN*1.85,28,PURPLE));self.formula('Av₁ = σ₁u₁     (‖v₁‖ = ‖u₁‖ = 1)',y=-2.35,size=27);self.to(65)
   self.reset('방향이 달라도 길이는 비교할 수 있다');c=np.array([-3,.2,0]);self.add(grid(c),arrow(c,v1,BLUEC,1),arrow(c,w1,ORANGE,1));aa=arrow(c,v1,BLUEC,1);bb=arrow(c,w1,ORANGE,1);self.add(aa,bb);self.to(67);self.play(Transform(aa,self.bars(1.6,1,1,BLUEC)),Transform(bb,self.bars(1.6,-.2,np.linalg.norm(w1),ORANGE)),run_time=2);self.add(label('입력 길이 1',[2.7,1.6,0],26,BLUEC),label('출력 길이 ≈ 2.414',[3.3,-.8,0],26,ORANGE));self.formula('‖Av₁‖ = σ₁ ‖v₁‖',y=-2.1);self.to(71)
   self.reset('고윳값과 특잇값이 가질 수 있는 값');self.formula('별도 예시: C = −2I',y=2.45,size=27,color=MUTED);c=np.array([-2,.2,0]);self.add(arrow(c,np.array([1,0]),BLUEC,1));a=arrow(c,np.array([1,0]),GREEN,1);self.add(a);self.play(Transform(a,arrow(c,np.array([-2,0]),GREEN,1)),run_time=1);self.add(label('Cv = −2v',[2,.3,0],35,GREEN));self.to(73)
   self.reset('별도 예시: 90° 회전행렬 R');c=np.array([-2,.2,0]);a=arrow(c,np.array([1,0]),GREEN,1.3);self.add(a);self.play(Rotate(a,PI/2,about_point=c),run_time=1);self.add(label('λ = ±i',[2,.3,0],40,GREEN));self.to(75)
   self.reset('고윳값은 복소수도, 특잇값은 0 이상의 실수');self.add(label('λ ∈ ℂ',[-3.6,1.2,0],44,GREEN),label('음수 · 양수 · 복소수',[-3.6,.2,0],28,GREEN),label('σ ≥ 0',[3.6,1.2,0],44,PURPLE),NumberLine(x_range=[0,3,1],length=4.7,color=PURPLE).move_to([3.5,-.2,0]),label('길이는 음수가 될 수 없다',[3.5,-1.3,0],27,PURPLE));self.to(78)
  elif i==3:
   self.reset('이차원에서 삼차원으로');self.add_fixed_in_frame_mobjects(self.bar,self.cap);self.set_camera_orientation(phi=65*DEGREES,theta=-55*DEGREES)
   self.add(ThreeDAxes(x_range=[-2,2],y_range=[-2,2],z_range=[-2,2],x_length=4,y_length=4,z_length=4,axis_config={'stroke_width':1,'color':MUTED}))
   ring=Circle(radius=1.45,color=BLUEC);self.add(ring);sphere=self.wire(scale=1.45);self.play(Create(sphere),run_time=2);self.to(82)
   unit_label=self.hud('단위구   x² + y² + z² = 1',[0,2.5,0],29,BLUEC)
   points=[]
   for n in range(40):
    z=1-2*(n+.5)/40;r0=np.sqrt(1-z*z);t=n*PI*(3-np.sqrt(5));points.append(np.array([r0*np.cos(t),r0*np.sin(t),z]))
   rays=VGroup(*[Line(ORIGIN,p*1.45,color=BLUEC,stroke_width=1) for p in points]);self.play(Create(rays),run_time=2);self.play(rays.animate.set_opacity(.12),run_time=2);self.to(87)
   self.remove(unit_label);self.hud('새 3차원 행렬   B = diag(2, 1, 0.5)',[0,2.45,0],30,ORANGE);self.remove(ring,rays);self.to(89)
   original=self.wire(scale=1.45,color=BLUEC).set_stroke(opacity=.15);self.add(original);self.play(Transform(sphere,self.wire(d=[2,1,.5],scale=1.45,color=ORANGE)),run_time=3);self.move_camera(theta=-45*DEGREES,run_time=1);self.to(93)
   for j,d in enumerate([2,1,.5]):
    p=np.zeros(3);p[j]=d*1.45;self.add(Line(ORIGIN,p,color=PURPLE,stroke_width=5))
   self.hud('σ₁ = 2     σ₂ = 1     σ₃ = 0.5',[0,-2.15,0],35,PURPLE);self.to(97)
  elif i==4:
   self.reset('최대·최소 사이의 배율도 특잇값');self.add_fixed_in_frame_mobjects(self.bar,self.cap);self.set_camera_orientation(phi=65*DEGREES,theta=-55*DEGREES)
   # Centers lie on the camera's horizontal basis; both share the same scale.
   basis=np.array([np.cos(35*DEGREES),np.sin(35*DEGREES),0]);l=-3.4*basis;r=3.4*basis
   self.add(self.wire(center=l,scale=1.03),self.wire(d=[2,1,.5],center=r,scale=1.03,color=ORANGE))
   for j,d in enumerate([2,1,.5]):
    e=np.eye(3)[j];self.add(Line(l,l+e*1.03,color=PURPLE,stroke_width=4),Line(r,r+e*d*1.03,color=PURPLE,stroke_width=4))
   self.hud('입력: 서로 직교하는 단위벡터',[-3.4,2.3,0],24,BLUEC);self.hud('출력: 대응하는 세 반축',[3.4,2.3,0],24,ORANGE);self.to(100)
   for x,val,name in [(-4.4,2,'최대 배율'),(0,1,'중간 배율'),(4.4,.5,'최소 배율')]:self.hud(f'{name}   {val:g}',[x,-1.8,0],28,PURPLE)
   self.to(103)
   for m in list(self.mobjects):
    if m not in [self.cap,self.bar]:self.remove(m)
   self.hud('고차원 특잇값 분포 · 설명용 예시',[0,3.15,0],31)
   for j,val in enumerate([2.6,2,1.65,1.1,.7,.3,.1]):
    rect=Rectangle(width=.7,height=val,color=PURPLE,fill_color=PURPLE,fill_opacity=.65).move_to([-4.5+j*1.5,-1.1+val/2,0]);self.add_fixed_in_frame_mobjects(rect)
   self.hud('σ₁ ≥ σ₂ ≥ ⋯ ≥ σₙ ≥ 0',[0,-2.1,0],34,PURPLE);self.to(106)
  else:
   self.reset('모든 방향을 하나씩 계산해야 할까?');c=np.array([-3,.3,0]);self.add(self.circle(c,1.55),self.spokes(c,64,scale=1.55).set_opacity(.2));theta=ValueTracker(0);ar=always_redraw(lambda:arrow(c,vec(theta.get_value()),BLUEC,1.55));self.add(ar,label('s(θ₁) = …\ns(θ₂) = …\ns(θ₃) = …',[2.4,.4,0],32,MUTED),label('?',[5,.4,0],70,PURPLE));self.play(theta.animate.set_value(TAU),run_time=4,rate_func=linear)
   self.reset('길이를 수식으로 표현하면');c=np.array([-3,.1,0]);self.add(grid(c),arrow(c,np.array([1.5,1]),BLUEC,1),DashedLine(c,c+RIGHT*1.5,color=MUTED),DashedLine(c+RIGHT*1.5,c+RIGHT*1.5+UP,color=MUTED));f=label('‖v‖² = x² + y²',[2.7,.8,0],37,BLUEC);self.add(f);self.to(112);self.play(Transform(f,label('‖v‖² = vᵀv',[2.7,.8,0],37,BLUEC)),run_time=.6);self.to(114);self.play(Transform(f,label('‖Av‖² = (Av)ᵀ(Av)',[1.8,.8,0],35,PURPLE)),run_time=.6);self.to(116)
   self.reset('길이에서 새로운 행렬로, 다시 고윳값으로')
   cards=VGroup()
   for x,s,color in [(-4.7,'A\n원래의 행렬',BLUEC),(0,'?\n새로운 행렬',GREEN),(4.7,'σ₁, σ₂, …\n특잇값',PURPLE)]:cards.add(VGroup(RoundedRectangle(width=3,height=2.2,color=color,stroke_width=1).move_to([x,.9,0]),label(s,[x,.9,0],30,color)))
   self.add(cards,Arrow([-3.1,.9,0],[-1.6,.9,0]),label('길이 측정',[-2.35,1.45,0],21,MUTED));self.to(118);self.add(Arrow([1.6,.9,0],[3.1,.9,0]),label('고윳값',[2.35,1.45,0],21,GREEN));self.formula('‖Av‖² = (Av)ᵀ(Av)',y=-1.7,size=40);self.to(120)
   self.reset('');self.formula('‖Av‖² = (Av)ᵀ(Av)',y=.25,size=49);self.to(121)
