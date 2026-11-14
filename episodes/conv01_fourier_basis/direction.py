"""Numerically consistent convolution, phase rotation, and Fourier diagonalization."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from episodes.log01_ratio_area.scene import LogRatioGeometry,eq,text
from episodes.conv01_fourier_basis.model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BLUE,ORANGE,TEAL,PURPLE,GOLD,MUTED='#80A8FF','#F1B66D','#43D3C4','#BD9BFA','#FFD477','#77849C'
class FourierConvolution(LogRatioGeometry):
 data=DATA
 def setup(self):
  super().setup();self.offset=self.info['start']
  for m in list(self.mobjects):
   if isinstance(m,Text) and '수학의연결' in m.text.replace(' ',''):self.remove(m)
  self.add(text('수학의 연결  /  합성곱과 푸리에 변환',y=7.15,size=18,color=MUTED))
 def plot_axes(self,y=2.0,h=3,w=7,x=0,yr=1.8):
  a=Axes(x_range=[0,1,.25],y_range=[-yr,yr,1],x_length=w,y_length=h,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([x,y,0])
  return a
 def path(self,a,ys,color=BLUE,xs=None,stroke=3):
  if xs is None:xs=np.linspace(0,1,len(ys))
  return VMobject(color=color,stroke_width=stroke).set_points_as_corners([a.c2p(float(x),float(y)) for x,y in zip(xs,ys)])
 def wave(self,a,fn,color=BLUE):
  ts=np.linspace(0,1,241);return self.path(a,fn(ts),color,ts)
 def raw_plot(self,y=2.0,h=3):
  a=self.plot_axes(y,h);xs=np.linspace(0,1,len(RAW));v=self.path(a,RAW)
  dots=VGroup(*[Dot(a.c2p(x,v),radius=.045,color=BLUE) for x,v in zip(xs,RAW)])
  return a,v,dots
 def spectrum(self,y=-1.0,output=False,phase=False):
  g=VGroup();xs=[-2.3,0,2.3];heights=AMP*np.abs([response(2*np.pi*f) for f in FREQ]) if output else AMP
  for x,f,h in zip(xs,FREQ,heights):
   g.add(Rectangle(width=.42,height=max(.01,h*2.2),fill_color=TEAL if output else BLUE,fill_opacity=.85,stroke_width=0).move_to([x,y+h*1.1,0]),text(f'{f} Hz',x=x,y=y-.35,size=22,color=MUTED),text(f'{h:.3f}',x=x,y=y+h*2.2+.23,size=21,color=TEAL if output else BLUE))
  return g
 def rotation_panel(self,delay=0):
  self.tt=ValueTracker(.1);self.lag=ValueTracker(delay)
  self.ca=Axes(x_range=[-1.3,1.3,1],y_range=[-1.3,1.3,1],x_length=3.3,y_length=3.3,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,2.35,0])
  unit=np.linalg.norm(self.ca.c2p(1,0)-self.ca.c2p(0,0));self.circle=Circle(radius=unit,color=MUTED,stroke_width=1.2).move_to(self.ca.c2p(0,0))
  self.wa=self.plot_axes(-.65,1.6,yr=1.2)
  self.reference=self.wave(self.wa,lambda t:np.cos(OMEGA*t),BLUE).set_stroke(opacity=.35)
  self.shifted=always_redraw(lambda:self.wave(self.wa,lambda t:np.cos(OMEGA*(t-self.lag.get_value())),ORANGE))
  def arrow(delay,color):
   z=np.exp(1j*OMEGA*(self.tt.get_value()-delay));return Arrow(self.ca.c2p(0,0),self.ca.c2p(z.real,z.imag),buff=0,color=color,stroke_width=4,max_tip_length_to_length_ratio=.15)
  self.ref_arrow=always_redraw(lambda:arrow(0,BLUE).set_opacity(.5));self.del_arrow=always_redraw(lambda:arrow(self.lag.get_value(),PURPLE))
  self.wdot=always_redraw(lambda:Dot(self.wa.c2p(self.tt.get_value()%1,np.cos(OMEGA*(self.tt.get_value()-self.lag.get_value()))),radius=.06,color=PURPLE))
  self.add(self.ca,self.circle,self.wa,self.reference,self.shifted,self.ref_arrow,self.del_arrow,self.wdot,text('Re',x=1.85,y=2.13,size=20,color=MUTED),text('Im',x=.24,y=4.08,size=20,color=MUTED))
 def s01(self):
  image=np.full((24,24),.15);image[7:20,5:19]=.85;image[4:8,8:16]=.85;image[12:20,10:14]=.3
  padded=np.pad(image,1,mode='edge');blur=sum(padded[i:i+24,j:j+24] for i in range(3) for j in range(3))/9
  rgb=lambda im:np.repeat(np.uint8(im*255)[...,None],3,axis=2)
  im=ImageMobject(rgb(image)).set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest']).scale_to_fit_width(2.6).move_to([-1.85,2.25,0])
  blurred=ImageMobject(rgb(blur)).set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest']).scale_to_fit_width(2.6).move_to(im)
  a=self.plot_axes(2.25,2.4,3.2,1.85);ts=np.linspace(0,1,121);v=self.path(a,.65*np.sin(2*np.pi*ts)+.3*np.sin(24*np.pi*ts),BLUE,ts);filtered=sum(c*(.65*np.sin(2*np.pi*(ts-k*TAU))+.3*np.sin(24*np.pi*(ts-k*TAU))) for k,c in enumerate(C));smooth=self.path(a,filtered,TEAL,ts)
  self.add(im,a,v,text('이미지의 주변 픽셀',x=-1.85,y=.55,size=22,color=ORANGE),text('신호의 주변 값',x=1.85,y=.55,size=22,color=BLUE));self.play(Transform(im,blurred),Create(smooth),run_time=2)
  self.to(5);self.formulas(r'\text{Convolution}',colors=[TEAL]);self.note_at('합성곱',color=TEAL,size=36)
  self.to(6);box=Square(side_length=.85,color=ORANGE).move_to([-1.85,2.25,0]);window=Rectangle(width=.55,height=2.4,color=ORANGE).move_to([1.85,2.25,0]);self.show(box,window)
  self.formulas(r'\text{one output}\;\longleftarrow\;\text{neighboring values}')
 def s02(self):
  a,v,dots=self.raw_plot();self.add(a,v,dots);self.formulas(r'f[n]')
  self.to(16);xs=np.linspace(0,1,len(RAW));idx=5
  window=Rectangle(width=7*2/(len(RAW)-1)+.16,height=3.1,color=ORANGE,stroke_width=2).move_to([a.c2p(xs[idx],0)[0],2,0]);self.show(window,run_time=.35)
  avg=np.convolve(RAW,np.ones(3)/3,mode='valid');target=Dot(a.c2p(xs[idx],avg[idx-1]),color=TEAL,radius=.07)
  arrows=VGroup(*[Arrow(a.c2p(xs[j],RAW[j]),target.get_center(),buff=.05,color=ORANGE,stroke_width=2,max_tip_length_to_length_ratio=.13) for j in [idx-1,idx,idx+1]])
  self.show(arrows,target);self.formulas(r'y[n]=\frac{f[n-1]+f[n]+f[n+1]}3',colors=[TEAL]);self.note_at('가장자리 두 점은 계산에서 제외',size=22)
  self.to(21);self.drop(arrows);self.drop(target);out=VGroup()
  for j in range(1,len(RAW)-1):
   self.play(window.animate.move_to([a.c2p(xs[j],0)[0],2,0]),run_time=.15)
   d=Dot(a.c2p(xs[j],avg[j-1]),radius=.045,color=TEAL);self.add(d);out.add(d)
  self.play(Create(self.path(a,avg,TEAL,xs[1:-1],4)),run_time=.7)
 def s03(self):
  a,v,_=self.raw_plot();self.add(a,v);self.formulas(r'[\tfrac13,\tfrac13,\tfrac13]\longrightarrow[c_0,c_1,c_2]')
  self.note_at('가중치 ¼,½,¼ · 표시 범위 밖의 값은 0',color=ORANGE,size=23)
  self.to(31);self.formulas(r'y[n]=\sum_k g[k]f[n-k]',colors=[TEAL])
  self.to(37);self.drop(a);self.drop(v);rows=VGroup();n=len(RAW)
  parts=[]
  for k,c in enumerate(C):
   vals=np.concatenate([np.zeros(k),RAW])[:n]*c;parts.append(vals);ax=self.plot_axes(3.25-k*1.25,.9,6.2,yr=.85);rows.add(ax,self.path(ax,vals,[BLUE,ORANGE,PURPLE][k]),text(f'c{k} f[n−{k}]',x=-2.65,y=3.8-k*1.25,size=20,color=[BLUE,ORANGE,PURPLE][k]))
  self.show(rows);self.formulas(r'y=c_0f+c_1T_1f+c_2T_2f',colors=[TEAL]);self.note_at('이동 → 가중치 곱하기 → 더하기',color=TEAL,size=25)
  self.to(40);self.drop(rows);out_axes=self.plot_axes();self.add(out_axes,self.path(out_axes,RAW,BLUE).set_stroke(opacity=.25));self.play(Create(self.path(out_axes,np.sum(parts,axis=0),TEAL)),run_time=1)
 def s04(self):
  a=self.plot_axes(2.7,2.0);self.add(a,self.wave(a,mixture,BLUE));spec=self.spectrum(-1.25);self.show(spec);self.note_at('주파수 예시 · 아래는 양의 주파수 진폭 요약',size=22)
  self.formulas(r'f*g\xrightarrow{\mathcal F}F\cdot G',colors=[TEAL])
  self.to(47);self.play(Transform(spec,self.spectrum(-1.25,True)),run_time=2)
  self.to(53);self.note_at('왜 성분별 곱셈이 될까?',color=TEAL,size=30)
 def s05(self):
  a=self.plot_axes(2.0,3,yr=1.3);base=self.wave(a,lambda t:np.cos(OMEGA*t),BLUE);self.add(a,base);self.formulas(r'f(t)=\cos(\omega t),\quad\omega=6\pi')
  self.to(58);lag=ValueTracker(0);moving=always_redraw(lambda:self.wave(a,lambda t:np.cos(OMEGA*(t-lag.get_value())),ORANGE));self.add(moving);base.set_stroke(opacity=.3);self.play(lag.animate.set_value(TAU),run_time=2)
  self.to(61);self.formulas(r'f(t-\tau)=\cos(\omega(t-\tau))',r'T=\frac{2\pi}{\omega}\quad\text{unchanged}',colors=[ORANGE,WHITE])
  self.to(65);self.drop(a);self.drop(base);self.drop(moving);self.rotation_panel(TAU);self.note_at('실수부는 파동 · 복소수는 회전',size=26,color=PURPLE)
 def s06(self):
  self.rotation_panel(0);self.formulas(r'P(t)=e^{i\omega t}',r'\operatorname{Re}P(t)=\cos(\omega t)',colors=[PURPLE,BLUE]);self.note_at('같은 속도로 원을 도는 점',size=26,color=PURPLE)
  self.play(self.tt.animate.set_value(.1+1/3),run_time=3,rate_func=linear)
  self.to(73);self.note_at('시간 지연 τ → 시계 방향 −ωτ',color=ORANGE,size=26);self.play(self.lag.animate.set_value(TAU),run_time=3)
  self.to(79);self.formulas(r'e^{-i\omega\tau}=e^{-i\pi/4}',r'\omega\tau=45^\circ',colors=[GOLD,ORANGE])
 def s07(self):
  self.rotation_panel(TAU);self.tt.set_value(.1+1/3);self.formulas(r'e^{i\omega(t-\tau)}',colors=[PURPLE]);self.note_at('시간 이동을 곱셈으로 표현',size=27,color=GOLD)
  self.to(85);self.formulas(r'\boxed{e^{i\omega(t-\tau)}=e^{i\omega t}e^{-i\omega\tau}}',r'\text{wave}\quad\times\quad\text{constant rotation}',colors=[GOLD,WHITE])
  self.play(Indicate(self.del_arrow,color=GOLD),run_time=.8)
 def s08(self):
  self.note_at('그림은 복소 신호의 실수부 · 가중치 ¼,½,¼',size=21,color=ORANGE)
  curves=VGroup()
  for k,c in enumerate(C):
   a=self.plot_axes(3.1-k*1.3,1.0,6.5,yr=1);curves.add(a,self.wave(a,lambda t,k=k,c=c:c*np.cos(OMEGA*(t-k*TAU)),[BLUE,ORANGE,PURPLE][k]),text(f'c{k} f(t−{k}τ)',x=-2.55,y=3.7-k*1.3,size=20,color=[BLUE,ORANGE,PURPLE][k]))
  self.add(curves);self.formulas(r'f(t)=e^{i\omega t}')
  self.to(90);self.formulas(r'y(t)=\sum_{k=0}^2c_k f(t-k\tau)',colors=[TEAL])
  self.to(95);self.formulas(r'y(t)=\sum_{k=0}^2c_ke^{i\omega(t-k\tau)}',r'=e^{i\omega t}\sum_{k=0}^2c_ke^{-i\omega k\tau}',colors=[WHITE,GOLD])
 def s09(self):
  a=Axes(x_range=[-.2,1.2,.5],y_range=[-1,.4,.5],x_length=4.5,y_length=4.5,tips=False,axis_config={'color':MUTED,'include_ticks':False,'stroke_width':1.2}).move_to([0,2.0,0]);self.add(a)
  terms=C*np.exp(-1j*OMEGA*TAU*np.arange(3));z=0j
  for v,c in zip(terms,[BLUE,ORANGE,PURPLE]):
   arrow=Arrow(a.c2p(z.real,z.imag),a.c2p((z+v).real,(z+v).imag),buff=0,color=c,stroke_width=4,max_tip_length_to_length_ratio=.18);self.play(GrowArrow(arrow),run_time=.45);z+=v
  result=Arrow(a.c2p(0,0),a.c2p(z.real,z.imag),buff=0,color=GOLD,stroke_width=5,max_tip_length_to_length_ratio=.15);self.show(result,run_time=.45)
  self.formulas(r'G(\omega)=\sum_{k=0}^2c_ke^{-i\omega k\tau}',r'y(t)=G(\omega)e^{i\omega t}',colors=[GOLD,TEAL]);self.note_at('복소수 벡터의 합이 하나의 계수로',size=25,color=GOLD)
 def s10(self):
  a=self.plot_axes(2,3,yr=1.3);H=response(OMEGA);self.add(a,self.wave(a,lambda t:np.cos(OMEGA*t),BLUE),self.wave(a,lambda t:np.real(H*np.exp(1j*OMEGA*t)),TEAL))
  self.note_at(f'진폭 ×{abs(H):.3f}   ·   위상 {np.angle(H)*180/np.pi:.0f}°   ·   같은 주파수',size=24,color=TEAL)
  self.formulas(r'G(\omega)=|G(\omega)|e^{i\phi(\omega)}',r'y(t)=|G(\omega)|e^{i(\omega t+\phi(\omega))}',colors=[GOLD,TEAL]);self.show(text('파형은 실수부 · G(ω)=0이면 해당 성분은 소멸',y=-4.2,size=19,color=MUTED))
 def s11(self):
  a=self.plot_axes(2.95,1.6);self.add(a,self.wave(a,mixture,BLUE));pieces=VGroup()
  for j,(f,c) in enumerate(zip(FREQ,AMP)):
   b=self.plot_axes(.95-j*1.12,.85,6.4,yr=1.1);pieces.add(b,self.wave(b,lambda t,f=f,c=c:c*np.sin(2*np.pi*f*t),[BLUE,ORANGE,PURPLE][j]),text(f'{f} Hz',x=-3.6,y=.95-j*1.12,size=18,color=[BLUE,ORANGE,PURPLE][j]))
  self.show(pieces);self.formulas(r'f(t)=\sin(2\pi t)+\tfrac12\sin(6\pi t)+\tfrac14\sin(12\pi t)',colors=[BLUE])
  self.to(117);self.drop(pieces);self.show(self.spectrum(-1.3));self.note_at('양의 주파수 진폭 요약 · 음의 주파수는 생략',size=21)
 def s12(self):
  self.note_at('막대: 진폭  ·  화살표: 위상  ·  양의 주파수 요약',size=21)
  for x,f,c in zip([-2.3,0,2.3],FREQ,AMP):
   H=response(2*np.pi*f);base=-.65
   before=Rectangle(width=.35,height=2.6*c,fill_color=BLUE,fill_opacity=.85,stroke_width=0).move_to([x-.25,base+1.3*c,0]);after=before.copy().set_fill(TEAL).shift(RIGHT*.5)
   self.add(before,after,text(f'{f} Hz',x=x,y=base-.3,size=23,color=MUTED),text(f'|G|={abs(H):.3f}',x=x,y=2.9,size=21,color=GOLD))
   target=Rectangle(width=.35,height=2.6*c*abs(H),fill_color=TEAL,fill_opacity=.85,stroke_width=0).move_to([x+.25,base+1.3*c*abs(H),0])
   center=np.array([x,-1.8,0]);ring=Circle(radius=.36,color=MUTED,stroke_width=1).move_to(center);phase_in=-PI/2;phase_out=phase_in+np.angle(H)
   p=Arrow(center,center+.34*np.array([np.cos(phase_in),np.sin(phase_in),0]),buff=0,color=BLUE,stroke_width=2,max_tip_length_to_length_ratio=.25);q=p.copy().set_color(TEAL)
   self.add(ring,p,q);self.play(Transform(after,target),Rotate(q,np.angle(H),about_point=center),run_time=1.1)
  self.form=VGroup(eq(r'Y(\omega_j)=F(\omega_j)G(\omega_j)',y=-3.0,color=TEAL));self.show(self.form);self.show(text('예시 입력 위상 −90°  ·  출력 위상에 arg G 추가',y=-3.9,size=20,color=MUTED,width=7.65))
 def s13(self):
  t,f,g,y,z=numerical_example();a=self.plot_axes(2.6,2);self.add(a,self.path(a,f,BLUE,t),self.path(a,y.real,TEAL,t));self.show(self.spectrum(-1.25,True));self.note_at('시간 영역의 합성곱 ↔ 주파수 성분별 곱셈',size=24,color=TEAL)
  self.formulas(r'(f*g)(t)=\int_{-\infty}^{\infty}f(t-\tau)g(\tau)\,d\tau',r'Y(\omega)=F(\omega)G(\omega)',colors=[WHITE,TEAL])
  self.show(text('그림: 주기 신호의 이산 예시',y=-4.2,size=18,color=MUTED))
  self.to(136);self.formulas(r'\boxed{\mathcal F(f*g)=\mathcal F(f)\mathcal F(g)}',colors=[TEAL]);self.note_at('Convolution Theorem · 합성곱 정리',size=25,color=TEAL)
 def s14(self):
  t,f,g,direct,via=numerical_example();a=self.plot_axes(2,3);self.add(a,self.path(a,direct.real,TEAL,t,4));overlay=DashedVMobject(self.path(a,via.real,GOLD,t,3),num_dashes=35);self.play(Create(overlay),run_time=1.5)
  self.note_at('순환 합성곱 · 한 주기 · DFT N=24',size=24,color=GOLD)
  self.formulas(r'f\xrightarrow{\mathcal F}F\xrightarrow{\times G}Y\xrightarrow{\mathcal F^{-1}}y')
  self.to(142);self.formulas(r'f*g=\mathcal F^{-1}(FG)',r'\text{direct result}=\text{FFT/IFFT result}',colors=[TEAL,GOLD]);self.show(text('청록: 직접 계산   ·   금색 점선: 변환을 경유한 계산',y=4.0,size=22,color=MUTED,width=7.65))
 def heat(self,matrix,x,color):
  g=VGroup();n=len(matrix);size=.44
  for i in range(n):
   for j in range(n):
    v=abs(matrix[i,j]);cell=Square(side_length=size,stroke_color=MUTED,stroke_width=.6,fill_color=color,fill_opacity=min(.95,.03+.9*v)).move_to([x+(j-(n-1)/2)*size,1.8+((n-1)/2-i)*size,0]);g.add(cell)
  return g
 def s15(self):
  Cmat,W,D=matrices();left=self.heat(Cmat,-1.9,ORANGE);right=self.heat(Cmat,1.9,PURPLE);self.add(left,right,text('C',x=-1.9,y=3.5,size=28,color=ORANGE),text('W C W⁻¹',x=1.9,y=3.5,size=26,color=PURPLE))
  self.note_at('순환 합성곱 N=6 예시 · 밝기는 절댓값',size=23)
  self.formulas(r'C=W^{-1}DW',r'D=\operatorname{diag}(G_0,\ldots,G_5)',colors=[WHITE,PURPLE]);self.play(Transform(right,self.heat(D,1.9,PURPLE)),run_time=2)
  self.show(text('원래 기준: 이웃 값이 섞임',x=-1.9,y=-.1,size=21,color=ORANGE,width=3.3),text('푸리에 기준: 성분별 계산',x=1.9,y=-.1,size=21,color=PURPLE,width=3.3))
 def s16(self):
  cards=VGroup(text('이동된 신호의 가중합',y=3.3,size=30,color=BLUE),text('파동의 이동 = 복소수 곱셈',y=1.8,size=30,color=GOLD),text('주파수마다 독립적인 계산',y=.3,size=30,color=TEAL));self.show(cards)
  self.formulas(r'\mathcal F(f*g)=FG',colors=[TEAL]);self.to(158);self.play(FadeOut(cards),run_time=.5);self.note_at('복잡한 연산도, 적절한 기준에서는 단순해진다',y=1.7,size=32,color=TEAL);self.show(text('Fourier Transform · Convolution · Eigenfunctions',y=-.1,size=19,color=MUTED,width=7.65));self.play(self.form.animate.move_to([0,3.3,0]),run_time=.6)
 def construct(self):
  getattr(self,f's{self.shot+1:02}')();self.to(self.info['end']);self.caption.remove_updater(self.update_caption)
  q=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'review')));q.mkdir(parents=True,exist_ok=True)
  (q/(self.info['id']+'.json')).write_text(json.dumps(self.caption_records),encoding='utf-8')
