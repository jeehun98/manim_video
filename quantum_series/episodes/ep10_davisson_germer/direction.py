import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.episodes.ep10_davisson_germer.layouts import DiffractionLayout
from quantum_series.shared.diffraction import normalized_amplitude
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=DiffractionLayout(configure().portrait)
BLUE='#48A9E6';GREEN='#42C1AA';ORANGE='#F18A54'
def wrap(s,n):
 lines=[];line=''
 for word in s.split():
  if line and len(line+' '+word)>n:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 return '\n'.join(lines+[line])
class EpisodeScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None;self.body=Group()
  self.add(text('양자역학의 발견   /   1927 · 데이비슨–거머',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
 def to(self,t):
  remain=t-self.offset-self.time
  if remain<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time} > {t}')
  frames=round(remain*30)
  if frames:self.wait((frames+1e-5)/30)
 def cue(self,i):
  s=D['sentences'][i];self.to(s['start'])
  if self.caption:self.remove(self.caption)
  self.caption=text(wrap(s['text'],26 if L.portrait else 62),y=L.caption_y,size=24 if L.portrait else 25,width=7.6 if L.portrait else 14.1);self.add(self.caption)
  h=text(s['heading'],y=L.heading_y,size=32,width=L.body_width)
  if self.heading:self.play(Transform(self.heading,h),run_time=.25)
  else:self.heading=h;self.play(FadeIn(h),run_time=.3)
 def put(self,*objects):self.body.add(*objects);self.add(*objects)
 def clear(self):
  if len(self.body):self.play(FadeOut(self.body),run_time=.35)
  self.body=Group()
 def note(self,s,color=MUTED):
  if self.foot:self.remove(self.foot)
  self.foot=text(s,y=-3.95 if L.portrait else -2.85,size=18,color=color,width=L.body_width);self.add(self.foot)
 def title(self,s,y=0,size=32,color=INK):return text(s,y=y,size=size,color=color,width=L.body_width)
 def centers(self):return L.panels
 def device(self,c):
  g=VGroup();target=Rectangle(width=2.7,height=.4,color=BLUE,fill_opacity=.3).move_to(c+p(0,-.8));gun=RoundedRectangle(width=.65,height=.65,corner_radius=.08,color=MUTED).move_to(c+p(0,1.6))
  g.add(target,gun,Arrow(c+p(0,1.2),c+p(0,-.55),buff=0,color=BLUE),text('전자총',*(c+p(-1,1.6))[:2],size=21),text('Ni',*(c+p(0,-1.25))[:2],size=23))
  origin=c+p(0,-.55);direction=p(np.sin(50*DEGREES),np.cos(50*DEGREES));det=Rectangle(width=.6,height=.4,color=GOLD).move_to(origin+2.1*direction)
  g.add(DashedLine(origin,origin+p(0,1.4),color=MUTED),Arrow(origin,origin+1.85*direction,buff=0,color=GOLD),det,text('검출기',*(origin+2.1*direction+p(.25,.5))[:2],size=19),Arc(radius=.8,start_angle=40*DEGREES,angle=50*DEGREES,color=GOLD).shift(origin),text('φ',*(origin+p(.35,.95))[:2],size=22,color=GOLD))
  return g,det,origin
 def scan_detector(self,g,det,o,degrees):
  self.remove(g[9],g[10]);g.remove(g[9],g[10])
  destination=o+rotate_vector(det.get_center()-o,-degrees*DEGREES)
  arrow=Arrow(o,destination,buff=.25,color=GOLD)
  self.play(det.animate.move_to(destination),Transform(g[6],arrow),run_time=.6)
 def lattice(self,c,grains=False):
  g=VGroup()
  if grains:
   for col in range(3):
    for row in range(2):
     cell=VGroup(*[Dot(p((x-1)*.22,(y-1)*.22),radius=.045,color=BLUE) for x in range(3) for y in range(3)])
     cell.rotate((col+row*2)*.27).move_to(c+p((col-1)*1.05,(row-.5)*1.05));g.add(cell,Square(side_length=.97,color=MUTED,stroke_width=1).move_to(cell))
  else:
   for x in range(8):
    for y in range(4):g.add(Dot(c+p((x-3.5)*.4,(y-1.5)*.4),radius=.065,color=BLUE))
  return g
 def graph(self,c,peak=True):
  ax=Axes(x_range=[0,90,30],y_range=[0,1.2,.5],x_length=5.7,y_length=1.75,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(c)
  curve=ax.plot(lambda x:.15+.78*np.exp(-((x-50)/8)**2) if peak else .2+.12*np.sin(x*DEGREES),x_range=[0,90],color=GOLD)
  labels=VGroup(text('0°',*(ax.c2p(0,0)+p(0,-.28))[:2],size=18),text('50°',*(ax.c2p(50,0)+p(0,-.28))[:2],size=18,color=GOLD),text('90°',*(ax.c2p(90,0)+p(0,-.28))[:2],size=18),text('상대 산란 전류',*(c+p(0,1.2))[:2],size=21),text('검출각 φ',*(c+p(0,-1.35))[:2],size=20))
  return VGroup(ax,curve,labels)
 def wave(self,c,phase=0,color=BLUE,amp=.35):return ParametricFunction(lambda t:c+p(t,amp*np.sin(2*PI*t/1.5+phase)),t_range=[-2.7,2.7],color=color)
 def label(self,s,c,color=INK,size=29):return text(s,*c[:2],size=size,color=color,width=6.4)
 def construct(self):
  scene=next(s for s in D['scenes'] if s['id']==self.section);a,b=self.centers()
  indices=[i for i,s in enumerate(D['sentences']) if scene['start']<=s['start']<scene['end']]
  for i in indices:
   self.cue(i)
   if i!=indices[0]:self.clear()
   if self.section=='question':
    self.put(self.label('1927 · 전자 회절',a+p(0,1),GOLD),Dot(a,radius=.13,color=BLUE),self.wave(b),self.label('입자로 검출 · 파동으로 예측',b+p(0,-1),BLUE))
    if i>=2:self.put(self.label('λ = h / p',a+p(0,-1),GOLD,size=40))
    self.note('파동 그래픽은 전자의 이동 궤적이 아닌 물질파의 개념 표현')
   elif self.section=='apparatus':
    g,det,o=self.device(a);self.put(g,self.graph(b,False));self.note('장치 단면 개념도 · 전자총과 표적 고정 · 방향별 전류 측정')
    dot=Dot(a+p(0,1.2),radius=.065,color=BLUE);self.put(dot);self.play(dot.animate.move_to(o),run_time=.65);self.play(dot.animate.move_to(det.get_center()),run_time=.65)
    if i==5:self.scan_detector(g,det,o,20)
   elif self.section=='accident':
    self.put(self.label('1925',a+p(0,1.75),GOLD,size=40))
    if i<9:
     tube=RoundedRectangle(width=3.5,height=1.65,corner_radius=.3,color=MUTED).move_to(a);self.put(tube,self.label('공기 유입' if i==7 else '산화 → 가열',b,ORANGE))
     for x in [-1,0,1]:self.put(Arrow(a+p(x,2),a+p(x,.4),color=ORANGE))
    else:
     old=self.lattice(a,True);new=self.lattice(b);self.put(old,new,self.label('여러 작은 결정립',a+p(0,-1.3),MUTED,size=25),self.label('성장한 결정 영역',b+p(0,-1.3),GOLD,size=25));self.play(LaggedStart(*[FadeIn(m) for m in new],lag_ratio=.015),run_time=.7)
    self.note('가열 전에도 결정립 내부는 규칙적 · 실제 구조의 2D 개념도')
   elif self.section in ['peak','scan']:
    g,det,o=self.device(a);chart=self.graph(b);self.put(g,chart)
    self.put(self.label('54 V' if i>=21 else 'U 조절',a+p(-1.6,.65),GOLD,size=24));self.play(Create(chart[1]),run_time=.7)
    self.note('각도별 신호는 정성적 재구성 · φ: 바깥 법선에서 잰 검출각')
    if i in [12,20]:self.scan_detector(g,det,o,15)
   elif self.section=='interference':
    if i<16:
     phase=PI if i==15 else 0
     w1=self.wave(a);w2=self.wave(a,phase,GOLD);total=self.wave(b,0,GREEN,amp=.7 if phase==0 else .001);self.put(w1,w2,total,self.label('같은 위상 → 보강' if phase==0 else '반대 위상 → 상쇄',b+p(0,-1),GREEN));self.play(Create(total),run_time=.7)
    else:
     atoms=self.lattice(a);self.put(atoms)
     phi=50 if i!=17 else 25;lam=.165;spacing=.215;delta=spacing*np.sin(phi*DEGREES);factor=normalized_amplitude(phi,lam,spacing)
     direction=p(np.sin(phi*DEGREES),np.cos(phi*DEGREES))
     for x in range(8):
      origin=a+p((x-3.5)*.4,.6);self.put(Line(origin,origin+direction*1.2,color=GREEN if factor>.8 else ORANGE,stroke_opacity=.7))
     self.put(self.graph(b) if i>=18 else self.wave(b,amp=max(.04,.7*factor),color=GREEN if factor>.8 else ORANGE),self.label('Δ경로 = D sin φ',a+p(0,-1.25),GOLD,size=24),self.label(f'φ = {phi}° · 상대 합성 진폭 {factor:.2f}',a+p(0,-1.8),size=21))
    if i==16:
     wavelets=VGroup(*[Arc(radius=.5,start_angle=0,angle=PI,color=BLUE,stroke_opacity=.4).shift(a+p((x-3.5)*.4,.6)) for x in range(8)]);self.put(wavelets);self.play(Create(wavelets),run_time=.6)
    self.note('표면 원자열의 1차원 간섭 모형 · 위상합으로 보강·상쇄 계산')
   elif self.section=='wavelength':
    self.put(self.label('운동량으로 예측',a+p(0,.8),BLUE),self.label('λ = h / √(2mₑeU)',a,BLUE,size=33),self.label('U = 54 V',a+p(0,-.7),size=25))
    if i>=24:self.put(self.label('0.167 nm',a+p(0,-1.35),BLUE,size=42))
    self.put(self.label('결정 회절에서 추정',b+p(0,.8),GOLD),self.label('λ ≈ D sin φ',b,GOLD,size=33))
    if i>=25:self.put(self.label('0.165 nm',b+p(0,-1.35),GOLD,size=42),self.label('D ≈ 0.215 nm · φ ≈ 50°',b+p(0,-.7),size=22))
    if i>=26:self.play(Indicate(self.body,color=GOLD,scale_factor=1.02),run_time=.7)
    self.note('표면 원자열 간섭의 근사 해석 · 두 독립적 파장 추정의 일치')
   elif self.section=='thomson':
    self.put(self.label('G. P. Thomson · 1927',a+p(0,1),GOLD,size=29),self.label('얇은 금속박을 투과한 전자',a+p(0,.45),size=23))
    foil=Rectangle(width=.07,height=1.1,color=MUTED,fill_opacity=.8).move_to(a+p(-1.7,-.8));self.put(foil,Arrow(a+p(-3,-.8),a+p(-1.85,-.8),buff=0,color=BLUE),Arrow(a+p(-1.6,-.8),a+p(-1.05,-.8),buff=0,color=BLUE),self.label('금속박',a+p(-2,-1.65),MUTED,size=17))
    for r in [.35,.65,.95]:self.put(Circle(radius=r,color=BLUE,stroke_opacity=.8).move_to(a+p(0,-.8)))
    self.put(self.label('J. J. Thomson · 1897',b+p(0,1),BLUE,size=29),self.label('음극선의 전기·자기적 편향',b+p(0,.4),size=23))
    path=ParametricFunction(lambda t:b+p(t,-.7+.12*t*t),t_range=[-2,2],color=BLUE);self.put(path);self.play(Create(path),run_time=.7)
    self.note('서로 다른 실험 · 니켈 표면 산란과 금속박 투과 회절을 구분')
   else:
    if i==32:
     self.put(self.wave(a),self.label('간섭과 회절',a+p(0,-.9),BLUE))
     screen=Rectangle(width=5.5,height=1.6,color=MUTED).move_to(b);self.put(screen)
     rng=np.random.default_rng(1927)
     dots=VGroup(*[Dot(b+p(rng.normal(0,.7),rng.uniform(-.6,.6)),radius=.035,color=GOLD) for _ in range(65)]);self.put(dots);self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.005),run_time=.7)
    else:
     packet=ParametricFunction(lambda x:a+p(x,.7*np.exp(-x*x/.6)*np.cos(10*x)),t_range=[-2.7,2.7],color=BLUE)
     spread=ParametricFunction(lambda x:b+p(x,.8*np.exp(-x*x/3)),t_range=[-2.7,2.7],color=GOLD);self.put(packet,spread,self.label('위치 공간의 파동묶음',a+p(0,-1),BLUE),self.label('운동량 성분의 분포',b+p(0,-1),GOLD));self.note('가우스 파동묶음의 개념도 · 위치와 운동량을 묻는 새 질문')
   self.to(D['sentences'][i]['end'])
