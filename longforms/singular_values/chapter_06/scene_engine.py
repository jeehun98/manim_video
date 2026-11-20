from visual_common import *
config.background_color='#10141e'
STARTS=[0,22,40,68,81,113,140];ENDS=[22,40,68,81,113,140,156]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class SensitivityScene(Scene):
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
 def eq(self,s,p=[0,.3,0],size=43,color=WHITE,width=12):
  m=MathTex(s,font_size=size,color=color)
  if m.width>width:m.scale_to_fit_width(width)
  m.move_to(p);self.add(m);return m
 def replace_eq(self,m,s,p=None,size=43,color=WHITE,duration=.8):
  n=MathTex(s,font_size=size,color=color)
  if n.width>12:n.scale_to_fit_width(12)
  n.move_to(m.get_center() if p is None else p);self.play(TransformMatchingTex(m,n),run_time=duration);return n
 def disk(self,c,d=[1,1],scale=1,color=BLUEC,fill=.15):
  d=np.array(d);c=np.array(c)
  return ParametricFunction(lambda t:c+np.r_[d*vec(t),0]*scale,t_range=[0,TAU,.03],color=color,stroke_width=3,fill_color=color,fill_opacity=fill)
 def arr(self,c,v,color,scale=1):
  if np.linalg.norm(v)==0:return Dot(c,color=color,radius=.055)
  return arrow(c,v,color,scale)
 def planes(self,left='입력',right='출력',middle='B'):
  l=np.array([-3.45,.25,0]);r=np.array([3.45,.25,0]);self.add(grid(l),grid(r),label(left,[-3.45,2.35,0],26,BLUEC),label(right,[3.45,2.35,0],26,ORANGE),Arrow([-.6,.25,0],[.6,.25,0]),label(middle,[0,.8,0],28));return l,r
 def error_pair(self,c,exact,noisy,scale=1.2):
  c=np.array(c);p=c+np.r_[exact,0]*scale;q=c+np.r_[noisy,0]*scale
  return VGroup(self.arr(c,exact,'#2dd4bf',scale),self.arr(c,noisy,'#fb7185',scale),Dot(p,color='#2dd4bf',radius=.035),Dot(q,color='#fb7185',radius=.035),Line(p,q,color='#fb7185',stroke_width=4))
 def construct(self):
  self.caption_setup();i=self.index;CYAN='#2dd4bf';RED='#fb7185';YEL='#facc15';LIGHT='#e9d5ff'
  if i==0:
   self.reset('벡터를 변환하고 원래대로 복원하기');centers=[np.array([x,.3,0]) for x in [-4.5,0,4.5]];x=np.array([.7,.7]);T=np.diag([1,.35])
   for c,name in zip(centers,['원래 벡터','변환된 벡터','복원된 벡터']):self.add(grid(c,scale=.6).scale(.65,about_point=c),label(name,c+UP*1.9,25))
   self.add(self.disk(centers[0],scale=.9),self.arr(centers[0],x,BLUEC,1.2));out=VGroup(self.disk(centers[1],scale=.9,color=ORANGE),self.arr(centers[1],x,ORANGE,1.2));self.add(out,Arrow([-3,.3,0],[-1.5,.3,0]),label('T',[-2.25,.8,0],25));self.play(Transform(out,VGroup(self.disk(centers[1],[1,.35],.9,ORANGE),self.arr(centers[1],T@x,ORANGE,1.2))),run_time=2)
   restored=VGroup(self.disk(centers[2],[1,.35],.9,CYAN),self.arr(centers[2],T@x,CYAN,1.2));self.add(restored,Arrow([1.5,.3,0],[3,.3,0]));self.play(Transform(restored,VGroup(self.disk(centers[2],scale=.9,color=CYAN),self.arr(centers[2],x,CYAN,1.2))),run_time=3)
   self.reset('오차가 없다면 정확한 복원이 가능하다');f=self.eq(r'A^{-1}(Ax)=(A^{-1}A)x',[0,.9,0],58);self.to(8);f=self.replace_eq(f,r'A^{-1}(Ax)=Ix=x',size=62,color=GREEN);self.to(10)
   self.reset('측정과 유한 정밀도에서 생기는 오차');curve=ParametricFunction(lambda t:np.array([-5.7+t*2.1,.6*np.sin(t*1.8)+.45,0]),t_range=[0,2.6,.03],color=BLUEC);self.add(curve,label('측정 오차',[-3,2.1,0],29));
   for j,t in enumerate(np.linspace(0,2.6,18)):
    p=np.array([-5.7+t*2.1,.6*np.sin(t*1.8)+.45+.13*np.sin(j*2.1),0]);self.add(Dot(p,color=RED,radius=.04))
   self.eq(r'1.23456789\ldots',[3.1,1.1,0],43,BLUEC,width=5);self.add(Arrow([3.1,.6,0],[3.1,-.1,0]));self.eq(r'1.2346',[3.1,-.65,0],49,ORANGE);self.add(label('제한된 자릿수로 표현',[3.1,-1.6,0],26,MUTED));self.eq(r'\Delta y',[0,-2.1,0],43,RED);self.to(18)
   self.reset('오차까지 함께 역변환하면?');c=np.array([-3,.1,0]);self.add(grid(c),self.arr(c,np.array([1,.4]),ORANGE,1.4),self.arr(c,np.array([1,.65]),RED,1.4),Arrow([-.3,.1,0],[1.7,.1,0]),label('A⁻¹',[.7,.65,0],29),label('?',[3.3,.1,0],75,RED));self.eq(r'\widetilde y=y+\Delta y',[0,-2,0],43);self.to(22)
  elif i==1:
   self.reset('가역적이지만 서로 다른 두 행렬');self.eq(r'A=I=\begin{pmatrix}1&0\\0&1\end{pmatrix}',[-3.45,.65,0],47);self.eq(r'B=\begin{pmatrix}1&0\\0&0.01\end{pmatrix}',[3.45,.65,0],47,PURPLE);self.to(24)
   self.reset('항등행렬 A: 모든 방향의 길이 유지');l,r=self.planes(middle='A');self.add(self.disk(l,scale=1.1),self.disk(r,scale=1.1,color=ORANGE));self.eq(r'\sigma_1=\sigma_2=1',[0,-2.05,0],45,GREEN);self.to(29)
   self.reset('B: 세로 방향만 백분의 일로 수축');l,r=self.planes(middle='B');self.add(self.disk(l,scale=1.1));p=ValueTracker(0);out=always_redraw(lambda:self.disk(r,[1,10**(-2*p.get_value())],1.1,ORANGE));self.add(out);self.to(31);self.play(p.animate.set_value(1),run_time=3,rate_func=linear);self.eq(r'\sigma=(1,0.01)',[0,-2.05,0],45,PURPLE);self.to(35)
   self.reset('두 행렬 모두 양의 특잇값과 역행렬을 갖는다');self.eq(r'A^{-1}=I',[-3.45,1,0],52,GREEN);self.eq(r'B^{-1}=\begin{pmatrix}1&0\\0&100\end{pmatrix}',[3.45,1,0],46,CYAN);self.eq(r'\operatorname{rank}(A)=\operatorname{rank}(B)=2',[0,-1.5,0],43);self.to(40)
  elif i==2:
   self.reset('B를 입력 벡터에 적용');l,r=self.planes('입력 x = (1, 1)','출력 y = Bx','B');x=np.array([1.,1.]);y=np.array([1.,.01]);self.add(self.arr(l,x,BLUEC,1.2));out=self.arr(r,x,ORANGE,1.2);self.add(out);self.to(43);self.play(Transform(out,self.arr(r,y,ORANGE,1.2)),run_time=4);self.eq(r'Bx=(1,0.01)^T',[0,-2.05,0],44,ORANGE);self.to(48)
   self.reset('정방향 변환 이후에 발생한 출력 오차');c=np.array([-3.5,0,0]);self.add(grid(c),self.error_pair(c,np.array([1,.01]),np.array([1,.012]),1.2));self.add(RoundedRectangle(width=4,height=2.8,color=MUTED,stroke_width=1).move_to([3.1,.6,0]),label('끝점 세로 차이 ×200',[3.1,2.35,0],25,MUTED),Dot([3.1,.1,0],color=ORANGE),Dot([3.1,.58,0],color=RED),Arrow([3.1,.1,0],[3.1,.58,0],buff=0,color=RED),label('0.010',[2,.1,0],24,ORANGE),label('0.012',[4.2,.58,0],24,RED));self.eq(r'\Delta y=(0,0.002)^T',[0,-2.1,0],44,RED);self.to(53)
   self.reset('줄어들었던 세로 성분을 다시 백 배로');l,r=self.planes('정확한 출력과 오차 출력','동일한 역변환을 받는 두 벡터','B⁻¹');p=ValueTracker(0);y=np.array([1.,.01]);noisy=np.array([1.,.012]);self.add(self.error_pair(l,y,noisy));
   def cur(v):return np.diag([1.,100**p.get_value()])@v
   restored=always_redraw(lambda:self.error_pair(r,cur(y),cur(noisy)));self.add(restored);self.eq(r'B^{-1}=\operatorname{diag}(1,100)',[0,-1.7,0],38,CYAN);self.to(58);self.play(p.animate.set_value(1),run_time=4,rate_func=linear);self.eq(r'\Delta x=B^{-1}\Delta y:\quad0.002\longrightarrow0.2',[0,-2.35,0],36,RED);self.to(64)
   self.reset('항등행렬과 B의 절대 오차 비교');self.add(label('항등행렬 A',[-3.45,1.65,0],31),label('수축행렬 B',[3.45,1.65,0],31));self.eq(r'0.002\ \to\ 0.002',[-3.45,.25,0],40,GREEN);self.eq(r'0.002\ \to\ 0.2',[3.45,.25,0],40,RED);self.add(label('절대 증폭 1배',[-3.45,-1,0],31,GREEN),label('절대 증폭 100배',[3.45,-1,0],31,RED));self.to(68)
  elif i==3:
   self.reset('수축 방향은 역변환에서 역수만큼 팽창');self.eq(r'Av_i=\sigma_i u_i',[0,1.6,0],57,ORANGE);self.eq(r'A^{-1}u_i=\frac1{\sigma_i}v_i',[0,-.1,0],57,CYAN);self.eq(r'\sigma_i>0',[0,-1.9,0],38,MUTED);self.to(75)
   self.reset('최소 특잇값 → 최대 절대 오차 증폭률')
   for cx,vals,names,color in [(-3.5,[1,.5,.2],['σ₁','σ₂','σ₃'],PURPLE),(3.5,[1,2,5],['1/σ₁','1/σ₂','1/σ₃'],CYAN)]:
    for j,(v,name) in enumerate(zip(vals,names)):
     x=cx+(j-1)*1.3;h=v*.4;self.add(Rectangle(width=.65,height=h,color=color,fill_color=color,fill_opacity=.8).move_to([x,-.5+h/2,0]),label(f'{v:g}',[x,-.5+h+.28,0],25,color),label(name,[x,-.9,0],23,MUTED))
   self.eq(r'\|A^{-1}\|_2=\frac1{\sigma_{\min}(A)}',[0,-1.7,0],41);self.eq(r'\|\Delta x\|_2\leq\frac1{\sigma_{\min}}\|\Delta y\|_2',[0,-2.3,0],34,MUTED);self.to(81)
  elif i==4:
   self.reset('같은 절대 오차, 다른 상대 오차')
   for y,data in [(1.25,5),(-.45,25)]:
    w=data*.3;self.add(Line([-4.8,y,0],[-4.8+w,y,0],stroke_width=20,color=BLUEC),Line([-4.8+w,y,0],[-4.5+w,y,0],stroke_width=20,color=RED),label(f'데이터 {data}  /  오차 1',[-2,y+.55,0],28),label(f'상대 오차 = {100/data:g}%',[-1,y-.65,0],30))
   self.to(87);self.eq(r'\text{Relative error}=\frac{\|\Delta y\|_2}{\|y\|_2}',[0,-2.2,0],39);self.to(89)
   self.reset('새 행렬 C: 모든 방향을 균일하게 수축');l,r=self.planes(middle='C');self.add(self.disk(l,scale=1.1));s=ValueTracker(1);small=always_redraw(lambda:self.disk(r,[s.get_value(),s.get_value()],1.1,ORANGE));self.add(small);self.play(s.animate.set_value(.01),run_time=3);self.add(self.disk([5.7,1.1,0],scale=.55,color=ORANGE),label('균일 확대 ×50',[5.7,1.95,0],18,MUTED),DashedLine(r,[5.15,1.1,0],color=MUTED,stroke_width=1));self.eq(r'C=0.01I,\quad\sigma=(0.01,0.01)',[0,-2.05,0],39,PURPLE);self.to(94)
   self.reset('C도 역변환에서 절대 오차를 백 배 증폭');self.eq(r'C^{-1}=100I',[0,1.5,0],58,CYAN);self.eq(r'(0,0.002)^T\longmapsto(0,0.2)^T',[0,-.1,0],48,RED);self.add(label('절대 오차 증폭률 = 100배',[0,-1.8,0],34,RED));self.to(98)
   self.reset('데이터와 오차가 같은 비율로 복원된다');self.add(label('새 비교 실험: x = (1, 0), Δy = (0, 0.002)',[0,2.4,0],25,MUTED));l=np.array([-3.45,.65,0]);r=np.array([3.45,.65,0]);self.add(grid(l),grid(r),self.error_pair(l,np.array([.01,0]),np.array([.01,.002]),1.2),Arrow([-.6,.65,0],[.6,.65,0]));p=ValueTracker(0)
   restored=always_redraw(lambda:self.error_pair(r,np.array([.01,0])*100**p.get_value(),np.array([.01,.002])*100**p.get_value(),1.2));self.add(restored);self.eq(r'0.002/0.01=20\%',[-3.45,-1.1,0],34,RED);self.eq(r'0.2/1=20\%',[3.45,-1.1,0],34,RED)
   for x in [-3.45,3.45]:self.add(Line([x-1.3,-1.85,0],[x+1.3,-1.85,0],color=BLUEC,stroke_width=14),Line([x+1.3,-1.85,0],[x+1.82,-1.85,0],color=RED,stroke_width=14))
   self.to(100);self.play(p.animate.set_value(1),run_time=3,rate_func=linear);self.add(label('상대 오차 증폭률 = 1배',[0,-2.4,0],28,GREEN));self.to(105)
   self.reset('같은 최소 특잇값, 서로 다른 상대 오차 증폭');self.add(label('동일한 x = (1, 0), 동일한 Δy = (0, 0.002)',[0,2.4,0],24,MUTED))
   for x,name,sigma,before,after,ampli in [(-3.45,'B',(1,.01),.2,20,100),(3.45,'C',(.01,.01),20,20,1)]:
    self.add(RoundedRectangle(width=6.1,height=3.75,color='#354458',stroke_width=1).move_to([x,.05,0]),label(f'{name}: σ = {sigma}',[x,1.25,0],30,PURPLE),label(f'복원 전 {before:g}% → 복원 후 {after:g}%',[x,-.1,0],28,RED),label(f'상대 증폭 {ampli}배',[x,-1.15,0],32,YELLOW if ampli==100 else GREEN))
   self.to(113)
  elif i==5:
   self.reset('최대와 최소 특잇값의 비율');c=np.array([-3,.3,0]);self.add(self.disk(c,[1,.25],1.65,ORANGE),self.arr(c,np.array([1,0]),PURPLE,1.65),self.arr(c,np.array([0,.25]),LIGHT,1.65));self.eq(r'\frac{\sigma_{\max}}{\sigma_{\min}}',[2.8,.4,0],75,PURPLE);self.to(118)
   self.reset('조건수 · Condition Number');self.eq(r'\boxed{\kappa_2(A)=\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}}',[0,1,0],59,YEL);self.eq(r'\kappa_2(A)=\|A\|_2\|A^{-1}\|_2',[0,-.8,0],46);self.add(label('가역 정사각행렬 · 이차 노름 기준',[0,-2,0],27,MUTED));self.to(122)
   self.reset('균일한 길이 배율이면 조건수는 1');
   for x,rad in [(-4.4,.35),(0,.7),(4.4,1.05)]:self.add(self.disk([x,.7,0],scale=rad,color=CYAN));self.eq(r'\kappa_2=1',[x,-.9,0],39,GREEN)
   self.eq(r'\kappa_2(sI)=\frac{|s|}{|s|}=1\quad(s\neq0)',[0,-2.2,0],39);self.to(125)
   self.reset('산술적 차이가 아닌 배율의 비율');log=ValueTracker(0);c=np.array([-3,.35,0]);body=always_redraw(lambda:self.disk(c,[1,10**(-log.get_value())],1.55,ORANGE));self.add(body,label('σmax = 1 고정',[-3,-1.65,0],28,PURPLE));number=DecimalNumber(1,mob_class=Text,num_decimal_places=0,font_size=47,color=YEL).move_to([3.5,.55,0]);number.add_updater(lambda m:m.set_value(10**log.get_value()));self.add(number,label('κ₂ =',[1.9,.55,0],35,YEL));minimum=DecimalNumber(1,mob_class=Text,num_decimal_places=6,font_size=31,color=LIGHT).move_to([3.1,-.7,0]);minimum.add_updater(lambda m:m.set_value(10**(-log.get_value())));self.add(minimum,label('σmin > 0',[3.1,-1.6,0],28,LIGHT));self.to(127);self.play(log.animate.set_value(4),run_time=3,rate_func=linear);self.to(131)
   self.reset('조건수는 상대 오차 증폭의 최악 상한');self.add(label('A는 고정 · 우변 b에만 오차 · x ≠ 0, b ≠ 0',[0,2.4,0],24,MUTED));self.eq(r'Ax=b,\qquad A(x+\Delta x)=b+\Delta b',[0,1.5,0],39);self.add(label('우변의 상대 오차',[-3.7,.3,0],28),label('해의 상대 오차 상한',[3.4,.3,0],28),label('0.2%',[-3.7,-.55,0],48,RED),Arrow([-1.7,-.55,0],[1.5,-.55,0],color=YEL));q=ValueTracker(0);upper=DecimalNumber(.2,mob_class=Text,num_decimal_places=1,font_size=48,color=RED).move_to([3.4,-.55,0]);upper.add_updater(lambda m:m.set_value(.2*10**q.get_value()));condition=DecimalNumber(1,mob_class=Text,num_decimal_places=0,font_size=31,color=YEL).move_to([.25,.1,0]);condition.add_updater(lambda m:m.set_value(10**q.get_value()));self.add(label('%',[5.2,-.55,0],48,RED),upper,condition,label('κ₂ =',[-.9,.1,0],26,YEL));self.to(134);self.play(q.animate.set_value(3),run_time=3,rate_func=linear);self.eq(r'\frac{\|\Delta x\|_2}{\|x\|_2}\leq\kappa_2(A)\frac{\|\Delta b\|_2}{\|b\|_2}',[0,-1.7,0],44);self.add(label('실제 증폭률은 데이터와 오차의 방향에 따라 달라진다',[0,-2.45,0],24,MUTED));self.to(140)
  else:
   self.reset('작은 양수와 정확한 0은 다르다');c=np.array([-2.6,.35,0]);s=ValueTracker(.01)
   def body():
    if s.get_value()==0:return Line(c+LEFT*1.7,c+RIGHT*1.7,color=RED,stroke_width=4)
    return self.disk(c,[1,s.get_value()],1.7,ORANGE)
   self.add(always_redraw(body));status=always_redraw(lambda:VGroup(label('σmin = '+f'{s.get_value():.6f}',[2.5,1.2,0],30,LIGHT),label('κ₂ = '+('∞' if s.get_value()==0 else f'{1/s.get_value():,.0f}'),[2.5,0,0],40,YEL)));self.add(status);self.play(s.animate.set_value(.0001),run_time=2,rate_func=linear);self.play(s.animate.set_value(0),run_time=1,rate_func=linear);s.set_value(0);self.add(label('역행렬 없음',[0,-1.8,0],37,RED));self.to(144)
   self.reset('복원 가능성과 오차 민감도는 다르다')
   for x,t,kappa,color,desc in [(-4.4,1,'1',GREEN,'역행렬 존재'),(0,.01,'100',YEL,'역행렬 존재'),(4.4,0,'∞',RED,'역행렬 없음')]:
    self.add(self.disk([x,.75,0],[1,t],.95,color) if t>0 else Line([x-.95,.75,0],[x+.95,.75,0],color=RED,stroke_width=3),label(desc,[x,-.6,0],27,color),label('κ₂ = '+kappa,[x,-1.5,0],34,color))
   self.to(150);self.reset('역행렬의 존재와 안정적인 복원은 다르다');self.add(label('복원할 수 있다는 것과',[0,.9,0],42),label('오차에 민감하지 않게 복원할 수 있다는 것은 다르다',[0,-.6,0],31,YEL));self.to(152)
   self.reset('특잇값으로 분석하는 복원 문제의 민감도');c=np.array([-3.8,.35,0]);self.add(self.disk(c,[1,.25],1.5,ORANGE),self.arr(c,np.array([1,0]),PURPLE,1.5),self.arr(c,np.array([0,.25]),LIGHT,1.5));self.eq(r'\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}',[2.2,.35,0],55,YEL,width=7.5);self.add(label('조건수는 문제의 민감도를 측정한다',[0,-2.15,0],29,MUTED));self.to(156)
