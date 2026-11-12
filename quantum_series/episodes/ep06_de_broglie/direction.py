"""Seven independent claims, fixed narration boundaries and responsive wave diagrams."""
import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.matter_waves import *
from quantum_series.episodes.ep06_de_broglie.layouts import MatterLayout
from quantum_series.episodes.ep06_de_broglie.physics_model import phase,is_phase_matched
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=MatterLayout(configure().portrait)
def wrap(s,n):
 lines=[];line=''
 for w in s.split():
  if line and len(line+' '+w)>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
class MatterScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None
  self.add(text('양자역학의 발견   /   1924 · 루이 드브로이',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
 def to(self,t):
  rem=t-self.offset-self.time
  if rem<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time} > {t}')
  frames=round(rem*30)
  if frames:self.wait((frames+1e-5)/30)
 def cue(self,i):
  s=D['sentences'][i];self.to(s['start'])
  if self.caption:self.remove(self.caption)
  self.caption=text(wrap(s['text'],26 if L.portrait else 62),y=L.caption_y,size=24 if L.portrait else 25,width=7.6 if L.portrait else 14.1);self.add(self.caption)
  h=text(s['heading'],y=L.heading_y,size=32,width=L.body_width)
  if self.heading:self.play(Transform(self.heading,h),run_time=.25)
  else:self.heading=h;self.play(FadeIn(h),run_time=.3)
 def note(self,s,color=MUTED):
  if self.foot:self.remove(self.foot)
  self.foot=text(s,y=-3.85 if L.portrait else -2.85,size=18,color=color,width=L.body_width);self.add(self.foot)
 def orbit_motion(self,center,radius=1.8,duration=1.4):
  electron=Dot(center+p(radius,0),radius=.08,color=ELECTRON);self.add(electron)
  self.play(MoveAlongPath(electron,Circle(radius=radius).move_to(center)),run_time=duration,rate_func=linear);return electron
 def radiation(self,origin):
  arcs=VGroup(*[Arc(radius=.2+j*.16,start_angle=-PI/3,angle=2*PI/3,color=MISMATCH,stroke_width=2).shift(origin) for j in range(3)])
  self.play(Create(arcs),run_time=.4);self.play(FadeOut(arcs,scale=1.8),run_time=.5)
 def unwrap(self,pair,to_flat=True,duration=1.5):
  moving=(pair.circular if to_flat else pair.flat).copy();self.add(moving)
  target=pair.flat if to_flat else pair.circular
  self.play(Transform(moving,target.copy()),run_time=duration);self.remove(moving)
 def phase_arrows(self,pair):
  group=VGroup()
  for center,angle in [(pair.L.straight+p(-1.1,-1.0),0),(pair.L.straight+p(1.1,-1.0),TAU*pair.cycles)]:
   group.add(Circle(radius=.22,color=MUTED).move_to(center),Arrow(center,center+p(.22*np.cos(angle),.22*np.sin(angle)),buff=0,color=GOLD,stroke_width=3))
  self.add(group);return group
class QuestionsDirection(MatterScene):
 offset=0
 def construct(self):
  self.cue(0);c=L.center;atom=BohrAtom(c);extra=VGroup(*[Circle(radius=r,color=MUTED,stroke_opacity=.4).move_to(c) for r in [1.05,1.2,1.75,1.95,2.4]])
  self.add(atom,extra);self.play(LaggedStart(*[FadeOut(o) for o in extra],lag_ratio=.15),run_time=1.3);e=self.orbit_motion(c,1.5,1.4);self.note('보어의 원형 궤도 모형 · 서로 다른 허용 상태');self.to(6)
  self.cue(1);questions=text('① 허용 궤도의 조건     ② 원자의 안정성',y=-2.3 if L.portrait else -2.0,size=27,width=7.5 if L.portrait else 12);self.add(questions);self.to(9)
  self.cue(2);candidate=DashedVMobject(Circle(radius=1.15,color=MISMATCH).move_to(c),num_dashes=35);self.play(Create(candidate),run_time=.7);self.play(Indicate(candidate),run_time=.6);self.to(12)
  self.cue(3);self.remove(e,candidate,questions);e=Dot(c+p(1.5,0),radius=.08,color=ELECTRON);self.add(e)
  velocity=Arrow(e.get_center(),e.get_center()+UP*.8,buff=0,color=ELECTRON);accel=Arrow(e.get_center(),c+p(.3,0),buff=0,color=MISMATCH);vectors=VGroup(velocity,accel,text('v',*(e.get_center()[:2]+[.3,.7]),size=24,color=ELECTRON),text('a · 중심 방향',c[0]+.5,c[1]-.45,20,MISMATCH));self.add(vectors);self.wait(.4);self.play(FadeOut(vectors),run_time=.3)
  self.note('고전 전자기학의 예측: 가속하는 전하의 복사',MISMATCH)
  spiral=ParametricFunction(lambda t:c+p((1.5-1.25*t)*np.cos(TAU*2*t),(1.5-1.25*t)*np.sin(TAU*2*t)),t_range=[0,1],color=MISMATCH)
  self.radiation(e.get_center());self.play(MoveAlongPath(e,spiral),Create(spiral),run_time=2.2,rate_func=linear);self.to(18)
class MatterWaveDirection(MatterScene):
 offset=18
 def construct(self):
  self.cue(4);c=L.center;wave=matter_wave(c,3);name=text('1924\nLouis de Broglie',y=3.4 if L.portrait else 1.7,size=36,color=GOLD);self.add(name);self.play(Create(wave),run_time=1.5);self.to(25)
  self.cue(5);self.remove(name);xs=L.comparison_x;yy=L.pair_y
  self.play(Transform(wave,matter_wave(p(xs[0],yy),2,3.0,.3)),run_time=.7)
  photon=VGroup(Circle(radius=.24,color=GOLD,fill_color=GOLD,fill_opacity=.25).move_to(p(xs[1],yy)),text('hν',xs[1],yy,24,GOLD));self.add(photon,text('빛 · 파동',xs[0],yy+1.1,26),text('빛 · 에너지 단위',xs[1],yy+1.1,24,GOLD,width=3.5));self.note('서로 다른 설명 관점 · 파동이 공으로 쪼개지는 과정이 아님');self.to(32)
  self.cue(6);arrow=Arrow(p(xs[0]+.7,yy-.8),p(xs[1]-.7,yy-.8),buff=0,color=GOLD);self.add(arrow);self.play(Rotate(arrow,PI),run_time=.6);self.to(34)
  self.cue(7);self.remove(photon);electron=Dot(p(xs[1],yy),radius=.14,color=ELECTRON);self.add(electron);self.play(electron.animate.shift(RIGHT*.65),run_time=1);electron_wave=matter_wave(p(xs[1],yy),2,3,.3);self.play(FadeOut(electron),Create(electron_wave),run_time=1.2);self.note('파동은 전자에 대응하는 상태의 표현 · 이동 궤적이나 꼬리가 아님');self.to(42)
  self.cue(8);self.clear_diagrams();w=matter_wave(p(0,1.4 if L.portrait else .9),3,6.3);formula=text('λ = h / p',y=-.2 if L.portrait else -.4,size=47,color=GOLD);self.add(w,formula,text('파장 λ    플랑크 상수 h    운동량 p',y=-1.3 if L.portrait else -1.5,size=25,width=L.body_width));self.to(48)
  self.cue(9);self.remove(w);upper=matter_wave(p(0,2.8 if L.portrait else 1.65),2,6.3,.25);lower=matter_wave(p(0,1.45 if L.portrait else .6),4,6.3,.25);self.add(upper,lower,text('작은 p · 긴 λ',-2.1,3.35 if L.portrait else 2.15,21,MATCH),text('큰 p · 짧은 λ',-2.1,.95 if L.portrait else .08,21,WAVE));self.play(Create(lower),run_time=.9);self.to(53)
  self.cue(10);self.play(Indicate(formula),run_time=.6);self.to(56)
 def clear_diagrams(self):
  retained=[self.caption,self.heading,self.foot];objects=[m for m in self.mobjects if m not in retained and not(isinstance(m,Text) and m.get_center()[1]>3.7)]
  self.play(*[FadeOut(m) for m in objects],run_time=.4)
class RingDirection(MatterScene):
 offset=56
 def construct(self):
  self.cue(11);pair=WavePair(L,3);self.add(pair.circle,Dot(L.ring,radius=.09,color=NUCLEUS));e=self.orbit_motion(L.ring,L.radius,1.6);self.note('원형 궤도라는 모형 안에서의 설명');self.to(61)
  self.cue(12);self.play(FadeOut(e),Create(pair.circular),run_time=1.2);self.add(pair.count);self.note('안팎의 굴곡은 파동값의 표현 · 전자의 궤적이 아님');self.to(65)
  self.cue(13);marker=Dot(pair.ringpoint(0),color=GOLD,radius=.085);self.add(marker,text('A',*(L.ring[:2]+[L.radius+.4,.3]),size=24,color=GOLD));self.play(UpdateFromAlphaFunc(marker,lambda m,a:m.move_to(pair.ringpoint(a))),run_time=1.8,rate_func=linear);self.add(pair.line);self.unwrap(pair,True,1.3);self.add(pair.flat,pair.endpoints());self.to(72)
class MismatchDirection(MatterScene):
 offset=72
 def construct(self):
  self.cue(14);pair=WavePair(L,3.5,MISMATCH);self.add(pair,pair.endpoints());self.note('같은 반지름·진폭 · 파장 수만 비교');self.unwrap(pair,True,1.5);self.to(76)
  self.cue(15);ends=pair.endpoints();self.play(Indicate(ends,color=GOLD),run_time=.8);self.add(pair.phase_indicator());gauges=self.phase_arrows(pair);self.to(79)
  self.cue(16);self.unwrap(pair,False,1.4);seam=VGroup(Dot(pair.ringpoint(0),color=GOLD,radius=.085),Dot(pair.ringpoint(1),color=MISMATCH,radius=.085),Line(pair.ringpoint(0),pair.ringpoint(1),color=MISMATCH));self.add(seam,text('A',L.ring[0]+L.radius+.55,L.ring[1]+.3,23,GOLD));self.play(Indicate(seam),run_time=.7);self.to(84)
  self.cue(17);self.play(pair.circular.animate.set_stroke(opacity=.35),pair.flat.animate.set_stroke(opacity=.35),run_time=.7);self.note('Δφ = 7π ≠ 2π의 정수배 · 연결 조건 불만족',MISMATCH);self.to(89)
class MatchDirection(MatterScene):
 offset=89
 def construct(self):
  self.cue(18);pair=WavePair(L,3.5,MISMATCH);self.add(pair);matched=WavePair(L,3,MATCH);self.play(Transform(pair,matched),run_time=1.6);pair=matched;self.remove(*[m for m in self.mobjects if isinstance(m,WavePair)]);self.add(pair,pair.endpoints());self.note('같은 반지름·진폭 · 파장 수만 비교');self.to(93)
  self.cue(19);self.unwrap(pair,False,1.2);phase_label=pair.phase_indicator();self.add(phase_label);gauges=self.phase_arrows(pair);self.to(96)
  self.cue(20);marker=Dot(pair.ringpoint(0),color=GOLD,radius=.085);self.add(marker);self.play(UpdateFromAlphaFunc(marker,lambda m,a:m.move_to(pair.ringpoint(a))),run_time=2,rate_func=linear);self.to(100)
  self.cue(21);self.remove(marker,gauges,phase_label);self.note('2πr = nλ     ·     n = 1, 2, 3, …',MATCH)
  for n in [2,4]:
   new=WavePair(L,n,MATCH);self.play(Transform(pair,new),run_time=.8)
  self.to(105)
class QuantizationDirection(MatterScene):
 offset=105
 def construct(self):
  self.cue(22);c=p(0,2.0) if L.portrait else p(-3.8,.2);r=1.5 if L.portrait else 1.8
  circle=Circle(radius=r,color=MUTED).move_to(c);wave=sampled_curve(lambda u:circular_point(u,3,c,r),MATCH);self.add(circle,wave,Dot(c,color=NUCLEUS,radius=.08),Line(c,c+p(r,0),color=GOLD),text('r',c[0]+r*.5,c[1]+.2,25,GOLD))
  fx=0 if L.portrait else 3.65;fy=-.5 if L.portrait else 1.3
  a=text('2πr = nλ',fx,fy,37,MATCH);b=text('λ = h/p',fx,fy-.9,35,WAVE);self.add(a,b);self.note('원형 경로의 길이와 운동량에 따른 파장을 결합');self.to(110)
  self.cue(23);combined=text('2πr = nh/p',fx,fy-1.8,35,GOLD);self.play(TransformFromCopy(a,combined),run_time=.9);self.note('이 조건은 r과 p의 곱을 제한한다 · 각각의 값에는 추가 법칙이 필요');self.to(116)
  self.cue(24);self.remove(b,combined);result=text('L = rp = nℏ',fx,fy-1.1,40,GOLD);self.play(TransformFromCopy(a,result),run_time=1.1);self.add(text('ℏ = h / 2π',fx,fy-2,25,MUTED));self.note('보어의 원형 궤도 모형에서 각운동량 L = rp');self.to(121)
  self.cue(25);self.play(*[FadeOut(m) for m in [circle,wave,a,result]],run_time=.5)
  self.remove(*[m for m in self.mobjects if m not in [self.heading,self.caption,self.foot] and m.get_center()[1]<3.7])
  xs=L.comparison_x;yy=L.pair_y;bohr=BohrAtom(p(xs[0],yy),(.55,.95,1.4));ring=VGroup(Circle(radius=1.4,color=MUTED).move_to(p(xs[1],yy)),sampled_curve(lambda u:circular_point(u,3,p(xs[1],yy),1.4),MATCH))
  self.add(bohr,ring,text('보어 · 1913',xs[0],yy+2,25),text('드브로이 · 1924',xs[1],yy+2,25),text('허용 궤도를 가정',xs[0],yy-1.95,23,width=3.5),text('파동의 연결 조건',xs[1],yy-1.95,23,MATCH,width=3.5),text('L = nℏ',y=3.7 if L.portrait else -2.2,size=35,color=GOLD));self.note('같은 양자화 규칙에 새로운 파동적 해석');self.play(Indicate(ring),run_time=1);self.to(131)
class LimitsDirection(MatterScene):
 offset=131
 def construct(self):
  self.cue(26);xs=L.comparison_x;yy=L.pair_y
  ringcenter=p(xs[0],yy);other=p(xs[1],yy);ring=VGroup(Circle(radius=1.4,color=MUTED).move_to(ringcenter),sampled_curve(lambda u:circular_point(u,3,ringcenter,1.4),MATCH));atom=BohrAtom(other,(1.4,),MUTED);self.add(ring,atom);self.note('파동의 연결 조건과 고전적 복사는 별개의 문제');self.to(134)
  self.cue(27);self.add(text('위상 연결',xs[0],yy+2,25,MATCH),text('고전적 복사',xs[1],yy+2,25,MISMATCH));e=self.orbit_motion(other,1.4,1.3)
  spiral=ParametricFunction(lambda t:other+p((1.4-1.1*t)*np.cos(TAU*2*t),(1.4-1.1*t)*np.sin(TAU*2*t)),t_range=[0,1],color=MISMATCH);self.radiation(e.get_center());self.play(MoveAlongPath(e,spiral),Create(spiral),run_time=2,rate_func=linear);self.note('주기적 연결 조건 ≠ 원자 안정성의 완전한 설명',MISMATCH);self.to(142)
  self.cue(28);objects=[m for m in self.mobjects if m not in [self.caption,self.heading,self.foot] and m.get_center()[1]<3.7];self.play(*[FadeOut(m) for m in objects],run_time=.6)
  center=L.center;state=abstract_state(center);self.play(Create(state),run_time=1.3);words=text('에너지     위치     시간',y=-1.4 if L.portrait else -1.7,size=29,color=GOLD);self.add(words);self.note('원자 속 파동의 상태와 시간 변화를 정하는 법칙은?');self.to(150)
  self.cue(29);self.play(state.animate.scale(1.13),FadeOut(words),run_time=1.5);self.note('파동적 상태를 암시하는 개념도 · 특정 오비탈의 정확한 형상 아님');self.to(156)
  self.cue(30);year=text('1924 · Louis de Broglie',y=-1.5 if L.portrait else -1.9,size=27,color=GOLD);self.play(FadeIn(year),run_time=.5);self.to(159);self.play(FadeOut(year),run_time=.6);self.to(160);self.to(161)
