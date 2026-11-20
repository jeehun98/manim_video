from visual_common import *
config.frame_width=9
config.frame_height=16
config.background_color='#10141e'
STARTS=[0,21,50,76,98,112,132];ENDS=[21,50,76,98,112,132,150]
A=B
CYAN='#2dd4bf';RED='#fb7185';YEL='#facc15';LIGHT='#e9d5ff'

def vec(t):return np.array([np.cos(t),np.sin(t)])
class SummaryScene(Scene):
 index=0
 def to(self,t):
  d=(round((t-STARTS[self.index])*config.frame_rate)-round(self.time*config.frame_rate))/config.frame_rate
  if d>.001:self.wait(d)
  elif d<-.04:raise ValueError((t,self.time))
 def caption_setup(self):
  self.caps={}
  for j,row in enumerate(DATA):
   group=VGroup(*[txt(s,25) for s in textwrap.wrap(row['text'],width=23,break_long_words=False)]).arrange(DOWN,buff=.14)
   if group.width>7.0:group.scale_to_fit_width(7.0)
   group.move_to([-.25,-5.65,0]);assert group.get_bottom()[1]>-7.1
   self.caps[j]=group
  self.cap=VGroup();self.key=-1
  def update(m,dt):
   t=STARTS[self.index]+self.time;k=next((j for j,r in enumerate(DATA) if r['start']<=t<r['end']),len(DATA)-1)
   if k!=self.key:m.become(self.caps[k]);m.set_z_index(100);self.key=k
  self.cap.add_updater(update);self.bar=Rectangle(width=9,height=3.1,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-6.45,0]).set_z_index(90);self.add(self.bar,self.cap)
 def clear(self,title):
  for m in list(self.mobjects):
   if m not in [self.cap,self.bar]:self.remove(m)
  t=label(title,[-.25,6.4,0],34)
  if t.width>7.1:t.scale_to_fit_width(7.1)
  self.add(t)
 def text(self,s,y,size=29,color=WHITE):
  m=label(s,[-.25,y,0],size,color)
  if m.width>7:m.scale_to_fit_width(7)
  self.add(m);return m
 def eq(self,s,y=0,size=45,color=WHITE):
  m=MathTex(s,font_size=size,color=color)
  if m.width>7:m.scale_to_fit_width(7)
  m.move_to([-.25,y,0]);self.add(m);return m
 def replace(self,m,s,size=45,color=WHITE):
  n=MathTex(s,font_size=size,color=color)
  if n.width>7:n.scale_to_fit_width(7)
  n.move_to(m);self.play(TransformMatchingTex(m,n),run_time=.8);return n
 def ellipse(self,c=[-.25,1,0],M=A,scale=1.15,color=ORANGE):
  c=np.array(c);return ParametricFunction(lambda t:c+np.r_[M@vec(t),0]*scale,t_range=[0,TAU,.03],color=color,fill_color=color,fill_opacity=.13,stroke_width=3)
 def axis(self,c,scale=1.15,M=A):
  u,s,v=np.linalg.svd(M);g=VGroup();c=np.array(c)
  for k in range(2):
   w=u[:,k]*s[k]*scale
   if k==0 and w[0]<0:w=-w
   if k==1 and w[1]<0:w=-w
   p=c+np.r_[w,0];g.add(Line(c,p,color=PURPLE,stroke_width=5),label('σ'+str(k+1),p+UP*.28,26,PURPLE))
  return g
 def arr(self,c,v,color=ORANGE,scale=1.15):return arrow(np.array(c),np.array(v),color,scale)
 def square(self,c,M=np.eye(2),scale=.8,color=ORANGE):
  c=np.array(c);return Polygon(*[c+np.r_[M@np.array(p),0]*scale for p in [(-1,-1),(1,-1),(1,1),(-1,1)]],color=color,stroke_width=3,fill_opacity=.15)
 def pair(self,c,exact,noisy,scale=2.4):
  c=np.array(c);p=c+np.r_[exact,0]*scale;q=c+np.r_[noisy,0]*scale
  return VGroup(self.arr(c,exact,CYAN,scale),self.arr(c,noisy,RED,scale),Dot(p,color=CYAN,radius=.045),Dot(q,color=RED,radius=.045),Line(p,q,color=RED,stroke_width=4))
 def num(self,value,p,places=2,color=PURPLE,size=37):return DecimalNumber(value,mob_class=Text,num_decimal_places=places,font_size=size,color=color).move_to(p)
 def construct(self):
  self.caption_setup();i=self.index
  if i==0:
   self.clear('고윳값이 같다면, 같은 변환일까?');top=np.array([-.25,3.7,0]);bottom=np.array([-.25,-1.,0]);s1=self.square(top,color=BLUEC);s2=self.square(bottom,color=BLUEC);self.add(s1,s2);self.eq(r'\lambda_1=\lambda_2=1',1.65,42,GREEN);self.eq(r'\lambda_1=\lambda_2=1',-2.35,42,GREEN);self.to(4)
   self.eq(r'I=\begin{pmatrix}1&0\\0&1\end{pmatrix}',5.3,36,BLUEC);self.eq(r'A=\begin{pmatrix}1&2\\0&1\end{pmatrix}',.5,36,ORANGE);self.play(Transform(s2,self.square(bottom,A,.8)),run_time=2);self.to(8)
   p=ValueTracker(0);self.remove(s2);field=always_redraw(lambda:VGroup(grid(bottom,np.array([[1,2*p.get_value()],[0,1]]),.65),self.square(bottom,np.array([[1,2*p.get_value()],[0,1]]),.8)));self.add(grid(top,scale=.65),field);self.play(p.animate.set_value(1),run_time=4,rate_func=linear);self.text('같은 고윳값, 서로 다른 공간 변화',-3.6,29,ORANGE);self.to(14)
   self.clear('고윳값은 특별한 방향을 관찰한다');c=np.array([-.25,2,0]);self.add(grid(c,scale=1.2),Line(c+LEFT*2.8,c+RIGHT*2.8,color=GREEN,stroke_width=4),self.arr(c,[1,0],GREEN,1.8));self.eq(r'Av=\lambda v\quad(\lambda=1)',-1.2,44,GREEN);self.text('독립적인 고유방향은 가로 방향 하나',-2.4,25,MUTED);self.to(16)
   originals=VGroup(*[self.arr(c,vec(t),BLUEC,1.1) for t in [PI/4,PI/2,3*PI/4]]);outputs=VGroup(*[self.arr(c,vec(t),ORANGE,1.1) for t in [PI/4,PI/2,3*PI/4]]);self.add(originals,outputs);self.play(Transform(outputs,VGroup(*[self.arr(c,A@vec(t),ORANGE,1.1) for t in [PI/4,PI/2,3*PI/4]])),run_time=2);self.text('다른 방향의 길이 변화는?',-3.6,31,PURPLE);self.to(21)
  elif i==1:
   self.clear('방향을 내려놓고 길이를 측정한다');c=np.array([-1.8,2.7,0]);v=vec(PI/4);self.add(self.arr(c,v,BLUEC,1.3),self.arr(c,A@v,ORANGE,1.3));self.to(23);self.play(Create(Line([-2.9,-.1,0],[-1.6,-.1,0],color=BLUEC,stroke_width=12)),Create(Line([-2.9,-1.3,0],[-2.9+np.linalg.norm(A@v)*1.3,-1.3,0],color=ORANGE,stroke_width=12)),run_time=1.5);self.eq(r'\frac{\|Av\|_2}{\|v\|_2}',-3.2,62,PURPLE);self.to(27)
   self.clear('길이가 1인 모든 방향의 벡터');c=np.array([-.25,1.4,0]);self.add(grid(c,scale=1.3));rays=VGroup(*[self.arr(c,vec(t),BLUEC,1.65) for t in np.linspace(0,TAU,24,endpoint=False)]);self.play(LaggedStart(*[GrowArrow(r) for r in rays],lag_ratio=.045),run_time=3);self.eq(r'\|v\|_2=1',-2.3,55,BLUEC);self.to(31)
   circle=self.ellipse(c,np.eye(2),1.65,BLUEC);self.play(Create(circle),rays.animate.set_opacity(.2),run_time=2);self.eq(r'x^2+y^2=1',-3.6,44);self.to(35)
   self.clear('単位円'.replace('単位円','단위 원')+'에 같은 행렬을 적용한다');c=np.array([-.25,1.4,0]);self.add(grid(c,scale=1.15),DashedVMobject(self.ellipse(c,np.eye(2),1.15,BLUEC)));p=ValueTracker(0);ellipse=always_redraw(lambda:self.ellipse(c,np.array([[1,2*p.get_value()],[0,1]]),1.15));self.add(ellipse);self.play(p.animate.set_value(1),run_time=4,rate_func=linear);self.eq(r'A=\begin{pmatrix}1&2\\0&1\end{pmatrix}',-2.3,45);self.to(40)
   self.clear('가장 긴 반축과 가장 짧은 반축');ct=np.array([-.25,3.9,0]);cb=np.array([-.25,-.5,0]);theta=ValueTracker(0);self.add(self.ellipse(ct,np.eye(2),1.15,BLUEC),self.ellipse(cb,A,1.15));moving=always_redraw(lambda:VGroup(self.arr(ct,vec(theta.get_value()),BLUEC,1.15),self.arr(cb,A@vec(theta.get_value()),ORANGE,1.15)));self.add(moving);self.play(theta.animate.set_value(67.5*DEGREES),run_time=2,rate_func=linear);f=self.eq(r'\max\|Av\|_2=1+\sqrt2',-3.1,43,PURPLE);self.to(44);self.play(theta.animate.set_value(157.5*DEGREES),run_time=1.7,rate_func=linear);self.remove(f);self.eq(r'\min\|Av\|_2=\sqrt2-1',-3.1,43,LIGHT);self.add(self.axis(cb));self.to(47)
   self.clear('특잇값 · Singular Values');self.add(self.ellipse([-.25,2,0]),self.axis([-.25,2,0]));self.eq(r'\sigma_1=1+\sqrt2',-1.2,49,PURPLE);self.eq(r'\sigma_2=\sqrt2-1',-2.6,49,LIGHT);self.text('주축 방향의 길이 변화 배율',-3.8,28);self.to(50)
  elif i==2:
   self.clear('이 숫자는 어떻게 계산할까?');self.add(self.ellipse([-.25,2,0]));self.eq(r'\sigma_1=?\qquad\sigma_2=?',-1.5,50,PURPLE);self.to(53)
   self.clear('길이의 제곱을 내적으로 표현한다');c=np.array([-1.7,3,0]);w=np.array([2,1]);self.add(self.arr(c,w,ORANGE,1.3),DashedLine(c+RIGHT*2.6,c+RIGHT*2.6+UP*1.3,color=MUTED),DashedLine(c,c+RIGHT*2.6,color=MUTED));self.eq(r'w=Av',1.1,43,ORANGE);f=self.eq(r'\|w\|_2^2=w_1^2+w_2^2',-.6,46);self.to(55);f=self.replace(f,r'\|w\|_2^2=w^Tw');self.to(56);self.eq(r'\|Av\|_2^2=(Av)^T(Av)',-2.6,42);self.to(58)
   self.clear('길이를 정리하면 새로운 행렬이 보인다');f=self.eq(r'(Av)^T(Av)',3.5,58);self.to(60);f=self.replace(f,r'v^TA^TAv',58);self.eq(r'M=A^TA',.5,62,CYAN);self.to(62);self.eq(r'\|Av\|_2^2=v^TMv',-2.2,49);self.to(64)
   self.clear('새로운 대칭행렬의 직교 고유벡터');self.eq(r'M=A^TA=\begin{pmatrix}1&2\\2&5\end{pmatrix}',4.5,44,CYAN);self.eq(r'M^T=M',2.7,38,CYAN);c=np.array([-.25,-.2,0]);V=np.column_stack([vec(67.5*DEGREES),vec(157.5*DEGREES)]);self.add(self.ellipse(c,np.eye(2),1.5,BLUEC));self.to(66);self.play(GrowArrow(self.arr(c,V[:,0],GREEN,1.5)),GrowArrow(self.arr(c,V[:,1],GREEN,1.5)),run_time=2);self.text('A가 아니라 M의 고유벡터',-2.7,29,GREEN);self.text('서로 직교하는 두 기저 방향',-3.8,26,MUTED);self.to(70)
   self.clear('고윳값의 제곱근이 특잇값이 된다');self.eq(r'Mv_i=\lambda_i v_i',4.3,45,GREEN);f=self.eq(r'\|Av_i\|_2^2=v_i^TMv_i',2.6,44);self.to(72);f=self.replace(f,r'\|Av_i\|_2^2=\lambda_i\underbrace{v_i^Tv_i}_{1}');self.to(74);self.eq(r'\boxed{\sigma_i=\sqrt{\lambda_i(A^TA)}}',-.1,46,PURPLE);self.add(self.ellipse([-.25,-2.3,0],scale=.95),self.axis([-.25,-2.3,0],.95));self.to(76)
  elif i==3:
   self.clear('같은 숫자에서 서로 다른 정보를 읽는다');self.eq(r'\sigma_1,\sigma_2,\ldots,\sigma_n',4.2,54,PURPLE)
   for y,s,col in [(2,'크기 → 길이 변화',PURPLE),(.3,'개수 → 남아 있는 차원',GREEN),(-1.4,'곱 → 공간의 부피',YEL),(-3.1,'비율 → 오차 민감도',RED)]:self.text(s,y,32,col)
   self.to(82);self.clear('한 특잇값을 줄이면 어떻게 될까?');self.eq(r'A_t=\begin{pmatrix}2&0\\0&t\end{pmatrix}',4.5,47);self.text('별도의 대각행렬 예시',5.5,25,MUTED);c=np.array([-.25,1.5,0]);t=ValueTracker(1);geometry=always_redraw(lambda:VGroup(self.ellipse(c,np.diag([2,t.get_value()]),1.2),Line(c,c+RIGHT*2.4,color=PURPLE,stroke_width=5),Line(c,c+UP*t.get_value()*1.2,color=LIGHT,stroke_width=5)));self.add(geometry);number=self.num(1,[-.25,-1.1,0],6);number.add_updater(lambda m:m.set_value(t.get_value()));self.add(number);self.text('σ₁ = 2 고정 · σ₂ = t',-.1,30,PURPLE);status=self.text('t > 0 : rank = 2',-3,33,GREEN);self.to(85);self.play(t.animate.set_value(.1),run_time=2,rate_func=linear);self.play(t.animate.set_value(.0001),run_time=1.5,rate_func=linear);self.to(89);self.play(t.animate.set_value(0),run_time=1,rate_func=linear);geometry.clear_updaters();self.remove(geometry);self.add(Line(c+LEFT*2.4,c+RIGHT*2.4,color=ORANGE,stroke_width=4),Dot(c,color=RED));self.play(Transform(status,label('t = 0 : rank = 1',[-.25,-3,0],33,GREEN)),run_time=.5);self.to(91)
   self.clear('양의 특잇값 개수가 랭크다');self.eq(r'\operatorname{rank}(A)=\#\{i:\sigma_i>0\}',4.2,43,GREEN);self.add(self.ellipse([-.25,2.3,0],np.diag([2,.7]),1.05),Line([-2.35,-1,0],[1.85,-1,0],color=ORANGE,stroke_width=4),Dot([-.25,-1,0],color=RED));self.text('σ = (2, 0.7) → rank = 2',.9,31,GREEN);self.text('σ = (2, 0) → rank = 1',-2.3,31,GREEN);self.text('정확히 0일 때 독립적인 차원이 사라진다',-3.8,26,MUTED);self.to(98)
  elif i==4:
   self.clear('이번에는 특잇값들을 곱한다');D=np.diag([2,.75]);self.add(self.ellipse([-.25,2.3,0],D),self.axis([-.25,2.3,0],M=D));self.eq(r'\sigma_1\times\sigma_2',-1.2,64,YEL);self.text('별도 예시: diag(2, 0.75)',-3.2,27,MUTED);self.to(101)
   self.clear('직교하는 길이 배율의 곱은 넓이 배율');ct=np.array([-.25,3.8,0]);cb=np.array([-.25,-.3,0]);self.add(self.ellipse(ct,np.eye(2),1,BLUEC));self.eq(r'S=\pi',2.2,43,BLUEC);self.to(103);p=ValueTracker(0);area=always_redraw(lambda:VGroup(self.ellipse(cb,np.diag([1+p.get_value(),1-.25*p.get_value()]),1.15),grid(cb,np.diag([1+p.get_value(),1-.25*p.get_value()]),.65)));self.add(area);self.play(p.animate.set_value(1),run_time=2.5,rate_func=linear);self.eq(r'S=1.5\pi',-2.2,43,ORANGE);self.to(106);self.eq(r'\frac{\pi\sigma_1\sigma_2}{\pi}=1.5',-3.7,44,YEL);self.to(108)
   self.clear('정사각행렬의 부피 변화는 |det|');self.add(self.ellipse([-.25,3,0],D),self.axis([-.25,3,0],M=D));self.eq(r'\sigma_1\sigma_2\cdots\sigma_n',.4,52,YEL);self.eq(r'\boxed{|\det A|=\prod_{i=1}^n\sigma_i}',-1.8,48,YEL);self.text('방향성이 아닌 부피 변화 배율',-3.6,28,MUTED);self.to(112)
  elif i==5:
   self.clear('가장 큰 값 ÷ 가장 작은 값');self.add(self.ellipse([-.25,3.3,0],np.diag([1,.2]),2.2),self.axis([-.25,3.3,0],2.2,np.diag([1,.2])));self.eq(r'\frac{\sigma_{\max}}{\sigma_{\min}}',-.6,84,PURPLE);self.to(116)
   self.clear('강한 수축은 역변환에서 큰 팽창이 된다');self.eq(r'D=\begin{pmatrix}1&0\\0&0.01\end{pmatrix}',5.1,40);c=np.array([-1.5,2.3,0]);self.add(self.ellipse([-.25,2.3,0],np.diag([1,.01]),1.7));self.text('정확한 출력 y = (1, 0)',3.8,27,ORANGE);self.to(118);self.add(self.pair(c,[1,0],[1,.002],2.4));self.eq(r'\Delta y=(0,0.002)^T',.8,40,RED);self.text('끝점의 세로 차이 ×200 확대',-.5,25,MUTED);inset=VGroup(RoundedRectangle(width=2.4,height=1.3,color=MUTED,stroke_width=1).move_to([-.25,-1.6,0]),Dot([-.25,-1.9,0],color=ORANGE),Dot([-.25,-.94,0],color=RED),Line([-.25,-1.9,0],[-.25,-.94,0],color=RED));self.add(inset);self.to(120)
   self.clear('동일한 역변환이 데이터와 오차에 적용된다');self.eq(r'D^{-1}=\begin{pmatrix}1&0\\0&100\end{pmatrix}',5,42,CYAN);p=ValueTracker(0);exact=np.array([1.,0]);noise=np.array([0,.002]);top=np.array([-1.6,2.9,0]);bottom=np.array([-1.6,-.6,0]);self.add(self.pair(top,exact,exact+noise,2.5));recovery=always_redraw(lambda:self.pair(bottom,exact,exact+np.diag([1,100**p.get_value()])@noise,2.5));self.add(recovery,Arrow([-.25,1.7,0],[-.25,.8,0],color=CYAN));self.play(p.animate.set_value(1),run_time=2.3,rate_func=linear);self.eq(r'0.002\ \longrightarrow\ 0.2',-2.4,43,RED);self.text('상대 오차 0.2% → 20%  (100배)',-3.8,29,RED);self.to(123)
   self.clear('방향별 배율의 불균형 · 조건수');self.eq(r'\kappa_2(D)=\frac{\sigma_{\max}}{\sigma_{\min}}',4.7,53,YEL);self.eq(r'\frac{1}{0.01}=100',2.9,48,YEL);self.to(126);self.clear('작은 특잇값일수록 조건수가 커진다');self.text('diag(1, t), t > 0',5.3,27,MUTED);q=ValueTracker(0);c=np.array([-.25,2.3,0]);geometry=always_redraw(lambda:self.ellipse(c,np.diag([1,10**(-q.get_value())]),2));self.add(geometry);number=self.num(1,[-.25,-.1,0],0,YEL,55);number.add_updater(lambda m:m.set_value(10**q.get_value()));self.add(number);self.text('κ₂ =',1,33,YEL);self.play(q.animate.set_value(3),run_time=3,rate_func=linear);self.eq(r'\frac{\|\Delta x\|_2}{\|x\|_2}\leq\kappa_2(D)\frac{\|\Delta y\|_2}{\|y\|_2}',-2.2,39);self.text('고정 가역행렬 · 출력에만 오차 · 2-노름',-3.45,23,MUTED);self.text('실제 증폭률이 아닌 최악의 상대 오차 상한',-4.2,24,RED);self.to(132)
  else:
   self.clear('같은 특잇값, 네 가지 관찰');self.eq(r'\sigma_1,\sigma_2,\ldots,\sigma_n',5.1,45,PURPLE);cards=[]
   forms=[r'\sigma_i',r'\#\{i:\sigma_i>0\}',r'\prod_i\sigma_i',r'\sigma_{\max}/\sigma_{\min}'];descs=['크기 · 방향별 길이 변화','개수 · 랭크와 정보 소실','곱 · 행렬식과 부피 변화','비율 · 조건수와 오차 민감도'];colors=[PURPLE,GREEN,YEL,RED]
   for k,(f,desc,color) in enumerate(zip(forms,descs,colors)):
    y=3.1-1.95*k;box=RoundedRectangle(width=6.8,height=1.65,color=color,stroke_width=1.5,fill_color=color,fill_opacity=.05).move_to([-.25,y,0]);formula=MathTex(f,font_size=37,color=color).move_to([-.25,y+.3,0]);desc=label(desc,[-.25,y-.45,0],25,color);card=VGroup(box,formula,desc);cards.append(card);self.play(FadeIn(card),run_time=.6);self.to(134+2*k)
   self.clear('하나의 변환에 담긴 다양한 정보');self.eq(r'A=\begin{pmatrix}1&2\\0&1\end{pmatrix}',5,42);c=np.array([-.25,2.5,0]);p=ValueTracker(0);geometry=always_redraw(lambda:self.ellipse(c,np.array([[1,2*p.get_value()],[0,1]]),1.15));self.add(geometry);self.play(p.animate.set_value(1),run_time=2,rate_func=linear);self.to(143);geometry.clear_updaters();axes=self.axis(c);self.add(axes);self.text('특잇값',-.1,44,PURPLE);self.text('기하학적 구조 · 정보 소실 · 계산 민감도',-1.6,27);self.to(146);self.eq(r'\lambda(A)=(1,1),\quad\sigma\approx(2.414,0.414)',-2.8,34);self.text('rank = 2 · det = 1 · κ₂ ≈ 5.828',-4,27,MUTED);self.to(148);self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in [self.cap,self.bar,geometry,axes]],run_time=1);self.text('특잇값 · Singular Values',-1.4,39,PURPLE);self.to(150)
  self.to(ENDS[i])
