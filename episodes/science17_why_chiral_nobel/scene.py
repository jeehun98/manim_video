"""Why nonlinear chiral amplification deserved the 2026 Nobel Prize in Chemistry."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery
from episodes.science16_chiral_amplification.scene import molecule,axes_graph,R,S,GOOD,GOLD,DIM,PURPLE

def panel(title,x,color,width=3.15,height=4.5):
 box=RoundedRectangle(width=width,height=height,corner_radius=.22,color=color,fill_color=color,fill_opacity=.035).move_to([x,.15,0])
 return VGroup(box,txt(title,2.75,22,color).move_to([x,2.75,0]))

def receptor(center,color=GOLD,mirror=False):
 x,y,_=center;sgn=-1 if mirror else 1
 return VMobject(color=color,stroke_width=10).set_points_as_corners([[x-1.1*sgn,y+.9,0],[x-.35*sgn,y+.9,0],[x-.35*sgn,y+.2,0],[x+.35*sgn,y+.2,0],[x+.35*sgn,y+.9,0],[x+1.1*sgn,y+.9,0]])

class WhyChiralNobel(DensityGrowthDiscovery):
 TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
 def construct(self):
  self.brand=txt('과학의 한 장면  /  Nobel Chemistry 02',7.1,21,'#9BA9C3');self.add(self.brand)

  self.cue('왜 이 비대칭이, 노벨상일까?','작은 분자 차이의 증폭이\n왜 근본적인 발견이었을까요?')
  left=molecule([-1.65,.55,0],False,.75);right=molecule([1.65,.55,0],True,.75);axis=DashedLine([0,-1.2,0],[0,2.4,0],color=GAS)
  self.beat(.28,FadeIn(left),FadeIn(right),Create(axis));self.add(txt('R',-1.55,37,R).shift(LEFT*1.65),txt('S',-1.55,37,S).shift(RIGHT*1.65),txt('WHY A NOBEL PRIZE?',-3.25,37,GOLD));self.finish()

  self.cue('문제는, 분자 하나의 모양이 아니다','생명체의 화학 전체가\n강하게 한쪽 손성으로 정렬됩니다.')
  chain=VGroup(*[molecule([-3+i,1.2,0],False,.3) for i in range(7)]);protein=VGroup(*[Dot([2*np.cos(i*.65),-1.2+.55*np.sin(i*1.1),0],radius=.12,color=R) for i in range(10)])
  self.beat(.4,LaggedStart(*[FadeIn(m) for m in chain],lag_ratio=.06));self.beat(.2,Create(VMobject(color=R,stroke_width=4).set_points_as_corners([d.get_center() for d in protein])),FadeIn(protein));self.add(txt('L · L · L · L · L · L · L',-.25,30,R),txt('LIFE IS HOMOCHIRAL',-3.5,34,GOLD));self.finish()

  self.cue('하지만 화학 법칙은, 어느 편도 들지 않는다','같은 조건에서 R과 S는\n거의 동등한 가능성을 가집니다.')
  self.add(molecule([-2,1,0],False,.55),molecule([2,1,0],True,.55),DashedLine([0,-1.3,0],[0,2.6,0],color=GAS),txt('same energy',-1.25,26,LIGHT).shift(LEFT*2),txt('same energy',-1.25,26,LIGHT).shift(RIGHT*2),txt('P(R)  =  P(S)',-3.1,46,GOLD));self.finish()

  self.cue('대칭적인 화학에서, 왜 생명은 한쪽일까?','화학의 대칭과 생명의 선택 사이에\n오래된 간극이 남아 있었습니다.')
  self.add(panel('CHEMISTRY',-1.85,S),panel('LIFE',1.85,R),txt('R  :  S',1.1,35,LIGHT).shift(LEFT*1.85),txt('50 : 50',.25,42,S).shift(LEFT*1.85),txt('L · L · L · L',.7,34,R).shift(RIGHT*1.85),txt('?',-1.2,70,GOLD));self.finish()

  self.cue('한쪽만 만드는 기술은, 이미 가능했다','다만 선택을 시작하려면 보통\n키랄한 촉매나 원천이 필요했습니다.')
  catalyst=Square(side_length=.9,color=R,fill_color=R,fill_opacity=.18).rotate(PI/4).move_to([-2,1,0]);self.add(catalyst,txt('R catalyst',1,24,R).shift(LEFT*2),Arrow([-1.1,.8,0],[.8,.8,0],color=GAS),molecule([2,.8,0],False,.58),txt('SELECTIVE SYNTHESIS',-2.7,31,GOLD),txt('a chiral source is already supplied',-3.55,23,LIGHT));self.finish()

  self.cue('그러면 질문은, 한 단계 뒤로 밀릴 뿐이다','생성물의 손성을 설명해도\n촉매의 손성은 다시 설명해야 합니다.')
  product=txt('R product',1.75,35,R).move_to([2,1.75,0]);catalyst=txt('R catalyst',.35,35,R).move_to([0,.35,0]);question=txt('?',.35,72,GOLD).move_to([-2.6,.35,0])
  self.add(product,Arrow([1.15,1.45,0],[.45,.7,0],color=GAS),catalyst,Arrow([-.8,.35,0],[-1.75,.35,0],color=GAS),question,txt('WHERE DID ITS HANDEDNESS COME FROM?',-3.1,25,LIGHT));self.finish()

  self.cue('Kagan은, 작은 원인이 큰 결과가 될 수 있음을 보였다','비대칭은 그대로 전달되는 것이 아니라\n반응 안에서 비선형적으로 증폭됩니다.')
  axes,line=axes_graph(False);_,curve=axes_graph(True);self.add(axes,line.set_opacity(.22));self.beat(.45,Create(curve));self.add(txt('small input',-2.45,23,S),txt('LARGE OUTPUT',1.95,28,R),txt('NONLINEAR AMPLIFICATION',-3.5,29,GOLD));self.finish()

  self.cue('Soai는, 결과를 다시 원인으로 연결했다','생성물이 같은 손성의 생성을 돕는\n화학적 피드백을 만들었습니다.')
  nodes=VGroup(txt('product',1.55,34,R),txt('catalyst',-.25,34,GOLD),txt('more product',-2.05,34,R));self.add(nodes);arrows=VGroup(Arrow([1.5,1.1,0],[1.5,.35,0],color=R),Arrow([1.5,-.65,0],[1.5,-1.35,0],color=R),CurvedArrow([-1.8,-1.75,0],[-1.8,1.75,0],angle=-PI/1.45,color=R));self.beat(.42,LaggedStart(*[Create(a) for a in arrows],lag_ratio=.12));self.add(txt('RESULT  →  CAUSE',-3.55,31,LIGHT));self.finish()

  self.cue('거대한 비대칭을, 처음부터 넣을 필요가 없어졌다','작은 차이가 사라지는 대신\n스스로 커질 수 있기 때문입니다.')
  self.add(panel('WITHOUT FEEDBACK',-1.85,S),panel('WITH FEEDBACK',1.85,R));left=VGroup(*[Dot([-3.05+i*.3,.5+(.2 if i%2 else -.2),0],radius=.08,color=R if i<4 else S) for i in range(9)]);right=VGroup(*[Dot([.65+i*.3,.5+(.2 if i%2 else -.2),0],radius=.08,color=R if i<8 else S) for i in range(9)]);self.beat(.3,FadeIn(left),FadeIn(right));self.add(txt('difference fades',-1.5,23,S).shift(LEFT*1.85),txt('difference grows',-1.5,23,R).shift(RIGHT*1.85));self.finish()

  self.cue('질문 자체가, 더 근본적으로 바뀌었다','누가 선택했는가가 아니라\n대칭이 어떻게 스스로 깨지는가입니다.')
  old=txt('WHO CHOSE R?',1.25,36,LIGHT);new=txt('HOW CAN SYMMETRY BREAK ITSELF?',-1.1,31,GOLD);self.add(old,txt('?',-.15,58,R));self.beat(.42,old.animate.set_opacity(.2).shift(UP*.4),FadeIn(new,shift=UP*.25));self.add(Arrow([0,.55,0],[0,-.55,0],color=GAS),txt('A NEW QUESTION',-3.35,28,R));self.finish()

  self.cue('그래서 생명의 기원과, 연결된다','작은 초기 편향이 생명의 강한 손성으로\n커지는 가능한 경로가 생겼습니다.')
  rng=np.random.default_rng(17);start=VGroup(*[Dot([rng.uniform(-3,3),rng.uniform(.1,2.4),0],radius=.075,color=R if i%2 else S) for i in range(30)]);chain=VGroup(*[Dot([-2.7+i*.6,-1.25+.16*np.sin(i),0],radius=.11,color=R) for i in range(10)]);self.add(start);self.beat(.4,Transform(start,chain));self.add(txt('EARLY CHEMISTRY',2.85,23,S),Arrow([0,.1,0],[0,-.65,0],color=GAS),txt('HOMOCHIRAL LIFE',-2.35,28,R));self.finish()

  self.cue('하지만 생명이 선택한 방향까지, 밝혀낸 것은 아니다','증폭 경로에는 체크할 수 있지만\n최초 편향의 기원은 남아 있습니다.')
  self.add(txt("ORIGIN OF LIFE'S HANDEDNESS",1.7,27,LIGHT),txt('?',.5,82,GOLD),txt('possible amplification mechanism',-1.25,25,GOOD),txt('✓',-2.65,44,GOOD).shift(LEFT*3),txt('origin of the first bias',-2.65,25,R),txt('?',-3.55,43,R).shift(LEFT*3));self.finish()

  self.cue('그래도 한 가지는, 완전히 달라졌다','미세한 비대칭이 거대한 손성으로\n자라날 수 있음을 화학으로 보였습니다.')
  assumption=txt('tiny asymmetry should remain tiny',1.55,27,LIGHT);self.add(assumption,Line([-3,1.4,0],[3,1.4,0],color=R,stroke_width=7).rotate(-.08));self.beat(.3,FadeIn(txt('tiny asymmetry',.1,29,S)),GrowArrow(Arrow([0,-.4,0],[0,-1.25,0],color=GOLD)),FadeIn(txt('MACROSCOPIC HANDEDNESS',-2.1,35,R)));self.finish()

  self.cue('이 의미는, 합성화학에도 이어진다','키랄한 생체 안에서는 거울상 분자가\n약물과 반응에서 다르게 작용합니다.')
  self.add(molecule([-2.25,1,0],False,.48),molecule([2.25,1,0],True,.48),receptor([-2.25,-.35,0],GOOD),receptor([2.25,-.35,0],DIM,True),txt('FIT',-2.15,29,GOOD).shift(LEFT*2.25),txt('DIFFERENT FIT',-2.15,26,S).shift(RIGHT*2.25),txt('SELECTIVE SYNTHESIS MATTERS',-3.45,29,GOLD));self.finish()

  self.cue('두 발견은, 비대칭이 비대칭을 낳는 길을 열었다','Kagan의 비선형 증폭과\nSoai의 비대칭 자기촉매입니다.')
  self.add(panel('HENRI B. KAGAN',-1.85,R),panel('KENSO SOAI',1.85,S),txt('nonlinear',.8,30,R).shift(LEFT*1.85),txt('amplification',.05,27,LIGHT).shift(LEFT*1.85),txt('asymmetric',.8,28,S).shift(RIGHT*1.85),txt('autocatalysis',.05,27,LIGHT).shift(RIGHT*1.85));self.beat(.3,GrowArrow(Arrow([-1.2,-1.2,0],[-.15,-1.9,0],color=R)),GrowArrow(Arrow([1.2,-1.2,0],[.15,-1.9,0],color=S)));self.add(txt('ASYMMETRY CREATES MORE ASYMMETRY',-2.85,27,GOLD));self.finish()

  self.cue('노벨상의 핵심은, 오래된 질문을 실험 가능한 화학으로 바꾼 것','좌우가 동등한 화학에서\n한쪽 세계는 어떻게 나타날까요?')
  dots=VGroup(*[Dot([-3+(i%10)*.67,2-(i//10)*.55,0],radius=.1,color=R if i%2 else S) for i in range(50)]);target=VGroup(*[Dot(d.get_center(),radius=.1,color=R if i<47 else S) for i,d in enumerate(dots)]);self.add(dots);self.beat(.5,Transform(dots,target));self.add(txt('대칭적인 화학에서',-1.7,35,LIGHT),txt('비대칭은 어떻게 스스로 나타나는가',-2.65,34,GOLD),txt('2026 NOBEL PRIZE IN CHEMISTRY',-3.65,26,R));self.finish()
