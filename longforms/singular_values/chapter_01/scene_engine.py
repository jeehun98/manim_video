from visual_common import *
config.background_color='#10141e'
STARTS=[0,16,36,65,87];ENDS=[16,36,65,87,100]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class LengthScene(Scene):
 index=0
 def to(self,t):
  d=t-(STARTS[self.index]+self.time)
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
    m.become(self.caps[key]);m.set_z_index(100);self.cap_key=key
  self.cap.add_updater(update);self.bar=Rectangle(width=14.22,height=1.3,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-3.35,0]);self.bar.z_index=90;self.cap.z_index=100;self.add(self.bar,self.cap)
 def reset(self,title):
  for m in list(self.mobjects):
   if m not in [self.cap,self.bar]:self.remove(m)
  self.add(label(title,[0,3.2,0],32))
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
 def construct(self):
  self.caption_setup();i=self.index
  if i==0:
   self.reset('행렬변환: 크기와 방향');l,r=self.pair();self.formula('A = [[1, 2], [0, 1]]',y=2.65,size=24,color=MUTED)
   self.add(arrow(l,np.array([1,1]),BLUEC,.9));out=arrow(r,np.array([1,1]),BLUEC,.9);self.add(out);self.to(1);self.play(Transform(out,arrow(r,np.array([3,1]),ORANGE,.9)),run_time=2)
   self.to(4);self.reset('고윳값이 관찰하는 특별한 경우');c=np.array([0,.2,0]);self.add(grid(c));ar=VGroup(*[arrow(c,vec(t),GREEN if abs(np.sin(t))<1e-8 else MUTED,1.3) for t in np.arange(0,2*np.pi,np.pi/6)]);self.add(ar)
   self.play(Transform(ar,VGroup(*[arrow(c,A@vec(t),GREEN if abs(np.sin(t))<1e-8 else MUTED,.95) for t in np.arange(0,2*np.pi,np.pi/6)])),run_time=2)
   self.add(DashedLine(c+LEFT*3,c+RIGHT*3,color=GREEN));self.formula('Av = λv       λ = 1',color=GREEN);self.to(10)
   self.reset('방향의 보존 조건에서 벗어나기');c=np.array([-3,.1,0]);v=vec(np.pi/4);self.add(grid(c),arrow(c,v,BLUEC,1.2),arrow(c,A@v,ORANGE,1.2));a=arrow(c,v,BLUEC,1.2);b=arrow(c,A@v,ORANGE,1.2);self.add(a,b);self.to(12)
   self.play(Transform(a,self.bars(1.4,.9,1.2,BLUEC)),Transform(b,self.bars(1.4,-.4,1.2*np.sqrt(5),ORANGE)),run_time=2);self.add(label('입력 길이',[2,1.45,0],25,BLUEC),label('출력 길이',[2,-.95,0],25,ORANGE));self.formula('방향이 아닌 길이의 변화',y=-2.15);self.to(16)
  elif i==1:
   self.reset('하나의 벡터에 행렬을 적용하면');c=np.array([-1.3,-.2,0]);self.add(grid(c,scale=1));self.play(GrowArrow(arrow(c,np.array([1,1]),BLUEC,1)),run_time=1);self.add(label('v = (1, 1)',c+np.array([.6,1.45,0]),25,BLUEC));self.to(20)
   self.formula('A(x, y) = (x + 2y, y)',y=2.5,size=28,color=WHITE);self.to(22);self.play(GrowArrow(arrow(c,np.array([3,1]),ORANGE,1)),run_time=1);self.add(label('Av = (3, 1)',c+np.array([3,1.45,0]),25,ORANGE));self.to(24)
   self.reset('길이의 변화 배율');self.add(label('입력 길이  ‖v‖ = √2',[-2,1.8,0],30,BLUEC),label('출력 길이  ‖Av‖ = √10',[-1.7,.1,0],30,ORANGE),self.bars(-4,1.05,np.sqrt(2)*1.5,BLUEC),self.bars(-4,-.65,np.sqrt(10)*1.5,ORANGE));self.to(26);f=self.formula('√10 / √2 = √5 ≈ 2.236',y=-1.6);self.to(28);self.play(Transform(f,label('s(v) = ‖Av‖ / ‖v‖     (v ≠ 0)',[0,-1.6,0],33,PURPLE)),run_time=.6);self.to(30)
   self.reset('길이 변화 배율의 의미')
   for y,name,s in [(1.6,'팽창  s > 1',np.sqrt(5)),(0,'유지  s = 1',1),(-1.6,'수축  s < 1',1/np.sqrt(5))]:
    g=VGroup(label(name,[-4.3,y,0],28),self.bars(-1.8,y+.22,1.6,BLUEC),self.bars(-1.8,y-.22,1.6*s,ORANGE),label(f'≈ {s:.3f}배',[4.7,y,0],28,PURPLE),DashedLine([-.2,y-.55,0],[-.2,y+.55,0],color=MUTED))
    self.play(FadeIn(g),run_time=.6)
   self.to(36)
  elif i==2:
   self.reset('입력이 두 배가 되면 출력도 두 배');l,r=self.pair(scale=.4);k=ValueTracker(1);v=np.array([1.,1.]);self.add(arrow(l,v,BLUEC,.4).set_opacity(.25),arrow(r,A@v,ORANGE,.4).set_opacity(.25))
   ar=always_redraw(lambda:VGroup(arrow(l,k.get_value()*v,BLUEC,.4),arrow(r,k.get_value()*(A@v),ORANGE,.4)));self.add(ar)
   num=DecimalNumber(1,mob_class=Text,num_decimal_places=1,color=PURPLE,font_size=36).move_to([0,-1.65,0]);num.add_updater(lambda m:m.set_value(k.get_value()));self.add(label('공통 크기 배율',[-2.1,-1.65,0],27),num,label('배',[.8,-1.65,0],27));self.play(k.animate.set_value(2),run_time=4,rate_func=smooth);self.formula('A(cv) = c(Av)',y=-2.3,size=29,color=WHITE);self.to(42)
   self.reset('처음 길이가 달라도 배율은 같다')
   for y,c in [(1.6,.5),(.25,1),(-1.1,2)]:
    self.add(label(f'{c:g}v',[-5.7,y,0],26,MUTED),self.bars(-4.8,y,c*np.sqrt(2)*.7,BLUEC),self.bars(-1.9,y,c*np.sqrt(10)*.7,ORANGE),label('√5',[4.7,y,0],33,PURPLE))
   self.to(45);f=self.formula('s(cv) = |c| ‖Av‖ / (|c| ‖v‖)',y=-2.25,size=29);self.to(47);self.play(Transform(f,label('s(cv) = s(v)     (c ≠ 0)',[0,-2.25,0],31,PURPLE)),run_time=.7);self.to(49)
   self.reset('관찰해야 하는 것은 입력 방향');c=np.array([-2.6,-.2,0]);self.add(grid(c));v=vec(np.pi/4)
   for k0 in [.8,1.4,2]:self.add(arrow(c,k0*v,BLUEC,1))
   self.add(Arc(radius=.7,start_angle=0,angle=np.pi/4,color=PURPLE).shift(c),label('θ',c+np.array([.95,.35,0]),32,PURPLE),label('벡터의 길이 r',[3,1.1,0],32,MUTED),Line([1.3,1.1,0],[4.7,1.1,0],color=MUTED),label('벡터의 방향 θ',[3,-.2,0],36,PURPLE));self.to(54)
   self.reset('길이를 1로 고정하기');c=np.array([0,.1,0]);self.add(grid(c));ar=VGroup(*[arrow(c,k0*v,BLUEC,1.1) for k0 in [.6,1.3,2]]) ;self.add(ar)
   self.play(Transform(ar,VGroup(*[arrow(c,v,BLUEC,1.1) for _ in range(3)])),run_time=2);self.add(DashedVMobject(Circle(radius=1.1,color=BLUEC).move_to(c)));self.formula('v̂ = v / ‖v‖       ‖v̂‖ = 1',y=-2);self.to(59)
   self.reset('출력 길이 자체가 변화 배율');f=self.formula('s(v) = ‖Av‖ / ‖v‖',y=1.3,size=43);self.to(61);self.play(Transform(f,label('s(v) = ‖Av‖ / 1',[0,1.3,0],43,PURPLE)),run_time=.5);self.to(62);self.play(Transform(f,label('s(v) = ‖Av‖',[0,1.3,0],46,PURPLE)),run_time=.5);self.formula('‖v‖ = 1     →     ‖Av‖ = √5',y=-.5,size=34,color=WHITE);self.formula('v = (1, 1) / √2      Av = (3, 1) / √2',y=-1.65,size=27,color=MUTED);self.to(65)
  elif i==3:
   self.reset('같은 행렬, 방향에 따라 달라지는 길이');theta=ValueTracker(0);l=np.array([-3.45,1.25,0]);r=np.array([3.45,1.25,0]);scale=.62
   self.add(grid(l,scale=scale),grid(r,scale=scale),DashedVMobject(Circle(radius=scale,color=BLUEC).move_to(l)),label('입력 v',[-3.45,2.55,0],25,BLUEC),label('출력 Av',[3.45,2.55,0],25,ORANGE),label('A',[0,1.25,0],30))
   arrows=always_redraw(lambda:VGroup(arrow(l,vec(theta.get_value()),BLUEC,scale),arrow(r,A@vec(theta.get_value()),ORANGE,scale)));self.add(arrows)
   self.add(label('입력 길이 = 1',[-3.45,.05,0],24,BLUEC),label('출력 길이 ≈',[2.85,.05,0],24,ORANGE));value=DecimalNumber(1,mob_class=Text,num_decimal_places=3,font_size=28,color=ORANGE).move_to([4.65,.05,0]);value.add_updater(lambda m:m.set_value(norm(theta.get_value())));self.add(value)
   self.play(theta.animate.set_value(90*DEGREES),run_time=5,rate_func=linear)
   ax=self.graph(center=[0,-1.25,0],width=11.5,height=1.8);trace=always_redraw(lambda:self.curve(ax,theta.get_value()/DEGREES));dot=always_redraw(lambda:Dot(ax.c2p(theta.get_value()/DEGREES,norm(theta.get_value())),color=PURPLE,radius=.06));line=always_redraw(lambda:DashedLine(ax.c2p(theta.get_value()/DEGREES,0),ax.c2p(theta.get_value()/DEGREES,3),color=PURPLE,stroke_width=1));self.add(trace,dot,line)
   self.play(theta.animate.set_value(360*DEGREES),run_time=7,rate_func=linear);self.reset('늘어나는 방향과 줄어드는 방향')
   for c,t in [(np.array([-3.45,.25,0]),60),(np.array([3.45,.25,0]),150)]:
    v0=vec(t*DEGREES);self.add(grid(c),DashedVMobject(Circle(radius=.9,color=BLUEC).move_to(c)),arrow(c,v0,BLUEC,.9),arrow(c,A@v0,ORANGE,.9),label(f'입력 방향 {t}°',c+UP*2,27),label(f'≈ {norm(t*DEGREES):.3f}배',c+DOWN*2,34,PURPLE))
   self.to(82);self.reset('하나의 행렬, 방향마다 다른 배율');l,r=self.pair(scale=.85)
   before=VGroup(*[arrow(l,vec(t),BLUEC,.85) for t in np.arange(0,2*np.pi,np.pi/8)]);out=VGroup(*[arrow(r,vec(t),BLUEC,.85) for t in np.arange(0,2*np.pi,np.pi/8)]);self.add(before,out);self.play(Transform(out,VGroup(*[arrow(r,A@vec(t),ORANGE,.85) for t in np.arange(0,2*np.pi,np.pi/8)])),run_time=2);self.formula('입력은 모두 길이 1, 출력 길이는 서로 다르다',y=-2.2,size=28);self.to(87)
  else:
   self.reset('어떤 방향에서 최대와 최소가 나타날까?');ax=self.graph(center=[0,.45,0],width=11.5,height=3.2);self.add(self.curve(ax));t=ValueTracker(0);point=always_redraw(lambda:Dot(ax.c2p(t.get_value(),norm(t.get_value()*DEGREES)),color=PURPLE,radius=.07));self.add(point);self.play(t.animate.set_value(360),run_time=3,rate_func=linear)
   for x in [67.5,247.5]:self.add(Dot(ax.c2p(x,norm(x*DEGREES)),color=GREEN,radius=.09))
   self.formula('max ‖Av‖   (‖v‖ = 1)',y=-1.75,size=29,color=GREEN);self.to(92)
   for x in [157.5,337.5]:self.add(Dot(ax.c2p(x,norm(x*DEGREES)),color=PURPLE,radius=.09))
   self.formula('min ‖Av‖   (‖v‖ = 1)',y=-2.3,size=29,color=PURPLE);self.to(95)
   self.reset('모든 방향의 단위벡터');c=np.array([0,.2,0]);radius=1.8
   def spokes(n):return VGroup(*[VGroup(Line(c,c+np.r_[vec(t)*radius,0],color=BLUEC,stroke_width=1.4),Dot(c+np.r_[vec(t)*radius,0],radius=.035,color=BLUEC)) for t in np.linspace(0,2*np.pi,n,endpoint=False)])
   rays=spokes(8);self.add(rays);self.to(96)
   for n in [16,32,64]:self.play(Transform(rays,spokes(n)),run_time=.65)
   dots=VGroup(*[Dot(c+np.r_[vec(t)*radius,0],radius=.025,color=BLUEC) for t in np.linspace(0,2*np.pi,64,endpoint=False)])
   self.play(FadeOut(rays),FadeIn(dots),run_time=.65);self.to(99);circle=Circle(radius=radius,color=BLUEC).move_to(c);self.play(Create(circle),FadeOut(dots),run_time=.6);self.formula('x² + y² = 1',y=-2.15,size=30,color=BLUEC);self.to(100)
