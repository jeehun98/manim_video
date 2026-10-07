"""High-harmonic generation -> phase locking -> attosecond electron dynamics."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,OBS,MASS,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

IR='#FF6678'; UV='#A48BFF'; ELECTRON='#63E6FF'; SIGNAL='#78F0A6'; GOLD='#FFD17A'; DIM='#50647E'

def atom(center=ORIGIN,scale=1,stretch=1):
    c=np.array(center,dtype=float)
    cloud=VGroup(*[Ellipse(width=2.4*r*stretch,height=1.7*r,stroke_width=0,fill_color=UV,fill_opacity=.022)
                   for r in np.linspace(1,.25,10)]).scale(scale).move_to(c)
    return VGroup(cloud,Dot(c,radius=.16*scale,color=GOLD),txt('e⁻',c[1]+.58*scale,20,ELECTRON).shift(RIGHT*c[0]))

def wave(y=0,color=IR,cycles=4,amp=.55,x0=-3.5,x1=3.5,phase=0):
    return ParametricFunction(lambda x:np.array([x,y+amp*np.sin(cycles*TAU*(x-x0)/(x1-x0)+phase),0]),
                              t_range=[x0,x1],color=color,stroke_width=3)

def pulse(center=ORIGIN,width=.24,height=2.4,color=UV):
    c=np.array(center,dtype=float)
    return ParametricFunction(lambda x:c+np.array([x,height*np.exp(-(x/width)**2),0]),
                              t_range=[-1.15,1.15],color=color,stroke_width=5)

def timeline(y=-2.6):
    return Arrow([-3.4,y,0],[3.45,y,0],buff=0,color=GAS,stroke_width=2)

class AttosecondPulseDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
    def construct(self):
        self.brand=txt('과학의 한 장면  /  Nobel 04',7.1,22,'#9BA9C3');self.add(self.brand)

        self.cue('빠른 움직임에는, 더 빠른 셔터가 필요하다','노출이 길면 여러 순간이 겹치고\n짧으면 한 순간이 분리됩니다.')
        path=Line([-3,1,0],[3,1,0],color=OBS,stroke_width=16,stroke_opacity=.22);ball=Dot([-3,1,0],radius=.26,color=GOLD)
        self.add(path,ball);self.beat(.35,ball.animate.move_to([3,1,0]),rate_func=linear)
        sharp=VGroup(Dot([0,-1.5,0],radius=.28,color=GOLD),Circle(radius=.52,color=SIGNAL).move_to([0,-1.5,0]))
        self.beat(.18,FadeIn(sharp));self.add(txt('LONG EXPOSURE',2.05,25,OBS),txt('SHORT EXPOSURE',-.55,25,SIGNAL));self.finish()

        self.cue('원자 안에서는, 변화가 이미 끝나 있다','전자 이동과 에너지 변화는\n상상하기 어려울 만큼 빠릅니다.')
        a=atom([0,.7,0],1.25);e=Dot([1.2,.7,0],radius=.1,color=ELECTRON);self.add(a,e)
        trail=TracedPath(e.get_center,stroke_color=ELECTRON,stroke_opacity=.65,stroke_width=3);self.add(trail)
        self.beat(.55,Rotate(e,angle=3*TAU,about_point=[0,.7,0]),rate_func=linear)
        shutter=Rectangle(width=6.8,height=.25,fill_color=LIGHT,fill_opacity=.8,stroke_width=0).move_to([0,-1.35,0]);self.beat(.15,shutter.animate.shift(UP*3.8))
        self.add(txt('camera: too slow',-3.45,29,MASS));self.finish()

        self.cue('10⁻¹⁸초, 아토초의 세계','펨토초보다 천 배 더 짧은\n전자 동역학의 시간척도입니다.')
        units=['1 s','10⁻³','10⁻⁶','10⁻⁹','10⁻¹²','10⁻¹⁵','10⁻¹⁸ s'];dots=VGroup()
        for i,u in enumerate(units):
            y=3.2-i*.83;dots.add(VGroup(Dot([-2.7,y,0],radius=.07,color=UV if i==6 else GAS),txt(u,y,28,UV if i==6 else LIGHT).shift(LEFT*.4)))
        self.beat(.5,LaggedStart(*[FadeIn(x,shift=DOWN*.1) for x in dots],lag_ratio=.08))
        self.add(txt('1 attosecond = 10⁻¹⁸ s',-3.25,40,GOLD));self.finish()

        self.cue('더 큰 현미경이 아니라, 더 짧은 빛','전자 변화보다 짧은 펄스가\n시간을 가르는 초고속 셔터가 됩니다.')
        a=atom([0,-.15,0],.9);long=wave(2.45,IR,4,.45);short=pulse([-1.6,-2.2,0],.22,1.25,UV)
        self.add(a);self.beat(.28,Create(long));self.add(txt('여러 순간이 겹친다',1.25,25,IR));self.beat(.25,Create(short))
        self.add(txt('한 순간만 묻는다',-3.7,27,UV),txt('ULTRAFAST SHUTTER',-4.55,32,GOLD));self.finish()

        self.cue('한 파동을, 어디까지 짧게 자를 수 있을까?','한두 번의 진동보다 짧은 곳에\n에너지를 모으는 것이 문제였습니다.')
        w=wave(.8,IR,5,.75);self.beat(.42,Create(w));box=Rectangle(width=2.0,height=2.2,color=GOLD).move_to([0,.8,0])
        self.beat(.18,box.animate.scale(.32).move_to([0,.8,0]));self.add(txt('few-cycle limit',-1.2,34,LIGHT),txt('더 짧게?',-3.2,31,GOLD));self.finish()

        self.cue('강한 레이저가, 전자를 원자 밖으로 끌어낸다','희가스 원자의 퍼텐셜이 기울며\n전자가 터널 이온화됩니다.')
        a=atom([1.3,.4,0],1);laser=wave(.4,IR,3,.5,x0=-3.6,x1=.2);self.add(a);self.beat(.28,Create(laser))
        stretched=atom([1.3,.4,0],1,1.65);self.beat(.2,Transform(a,stretched));e=Dot([1.9,.4,0],radius=.11,color=ELECTRON);self.add(e)
        self.beat(.28,e.animate.move_to([3.1,.4,0]),rate_func=rush_into);self.add(txt('tunnel ionization',-2.35,29,ELECTRON));self.finish()

        self.cue('전기장이 뒤집히면, 전자가 돌아온다','밖으로 나온 전자는 장의 반전과 함께\n원자핵 쪽으로 다시 가속됩니다.')
        a=atom([-1.8,.4,0],.85);e=Dot([2.7,.4,0],radius=.11,color=ELECTRON);self.add(a,e,wave(2.4,IR,2.5,.5))
        outbound=Arrow([-1.1,.4,0],[2.1,.4,0],buff=0,color=DIM);returning=Arrow([2.2,-.2,0],[-1.15,-.2,0],buff=0,color=ELECTRON)
        self.add(outbound);self.beat(.18,Transform(outbound,returning));self.beat(.38,e.animate.move_to([-1.55,.4,0]),rate_func=rush_into)
        self.add(txt('FIELD REVERSAL',-2.2,29,IR),txt('RETURN',-3.2,31,ELECTRON));self.finish()

        self.cue('재결합 에너지가, 높은 주파수의 빛이 된다','되돌아온 전자가 에너지를 방출하며\n고차 고조파를 만듭니다.')
        a=atom([-2.4,.9,0],.72);e=Dot([1.7,.9,0],radius=.1,color=ELECTRON);self.add(a,e);self.beat(.3,e.animate.move_to([-2.15,.9,0]),rate_func=rush_into)
        self.beat(.13,Flash([-2.15,.9,0],color=UV,flash_radius=.8))
        harms=VGroup(*[wave(2-i*.78,[IR,GOLD,OBS,UV][i],2*i+1,.23,x0=-.5,x1=3.5) for i in range(4)]);self.beat(.28,LaggedStart(*[Create(h) for h in harms],lag_ratio=.08))
        self.add(txt('ω     3ω     5ω     7ω  ···',-2.45,32,LIGHT),txt('HIGH HARMONICS',-3.45,31,UV));self.finish()

        self.cue('여러 주파수가, 한 순간에만 합쳐진다','위상이 맞으면 대부분은 상쇄되고\n좁은 시간 구간에서만 강화됩니다.')
        waves=VGroup(*[wave(2.65-i*.65,[IR,GOLD,OBS,UV][i],2*i+1,.18) for i in range(4)]);self.add(waves)
        self.beat(.22,waves.animate.set_opacity(.28));spike=pulse([0,-1.1,0],.16,2.2,SIGNAL);self.beat(.35,Create(spike))
        self.add(txt('many frequencies',-.35,27,MASS),Arrow([-1.3,-2.25,0],[1.25,-2.25,0],color=GAS),txt('VERY SHORT PULSE',-3.35,31,SIGNAL));self.finish()

        self.cue('250 as, 연속된 펄스 열','Agostini 연구팀은 펄스의 연속열을\n만들고 그 길이를 측정했습니다.')
        axis=timeline(-1.2);self.add(axis);train=VGroup(*[pulse([x,-1.2,0],.11,2.25,UV) for x in (-2.7,-1.35,0,1.35,2.7)])
        self.beat(.48,LaggedStart(*[Create(p) for p in train],lag_ratio=.08));self.add(txt('2001  ·  PIERRE AGOSTINI',2.65,27,LIGHT),txt('250 as',-3.8,48,GOLD));self.finish()

        self.cue('650 as, 하나의 펄스를 분리하다','Krausz 연구팀은 펄스 열에서\n단일 펄스 하나를 떼어냈습니다.')
        train=VGroup(*[pulse([x,1.6,0],.12,1.6,DIM) for x in (-2.7,-1.35,0,1.35,2.7)]);chosen=train[2].copy().set_color(SIGNAL);self.add(train,chosen)
        self.beat(.35,chosen.animate.move_to([0,-1.2,0]).scale(1.35),train.animate.set_opacity(.12));self.add(Arrow([0,.3,0],[0,-.5,0],color=GOLD),txt('650 as',-3.25,48,GOLD),txt('2001  ·  FERENC KRAUSZ',2.8,27,LIGHT));self.finish()

        self.cue('결과 하나가, 시간 순서로 펼쳐진다','아토초 펄스를 지연시키며\n전자 과정의 각 단계를 측정합니다.')
        states=VGroup()
        for i,x in enumerate((-2.5,0,2.5)):
            a=atom([x,.65,0],.48,1+i*.25);e=Dot([x+.35+i*.28,.65,0],radius=.07,color=ELECTRON);states.add(VGroup(a,e,txt(f't{i+1}',-1.05,27,UV).shift(RIGHT*x)))
        self.beat(.5,LaggedStart(*[FadeIn(s) for s in states],lag_ratio=.18));self.add(timeline(-2.1),txt('전자 분포 변화  →  이온화  →  방출',-3.25,29,LIGHT));self.finish()

        self.cue('사진이 아니라, 시간 해상도다','전자 궤도의 스냅사진이 아니라\n변화의 앞뒤를 구분하는 측정입니다.')
        fake=VGroup(atom([-2.1,1.2,0],.75),Circle(radius=1.1,color=GAS).move_to([-2.1,1.2,0]),Cross(stroke_color=IR,stroke_width=8).scale(.8).move_to([-2.1,1.2,0]));self.add(fake)
        sequence=VGroup(*[VGroup(atom([1.5,2.2-i*1.3,0],.32,1+i*.18),txt(f't{i+1}',2.2-i*1.3,24,UV).shift(RIGHT*2.6)) for i in range(3)])
        self.beat(.32,LaggedStart(*[FadeIn(s) for s in sequence],lag_ratio=.15));self.add(txt('NOT A CAMERA PHOTO',-2.3,25,IR),txt('TIME-RESOLVED MEASUREMENT',-3.5,29,SIGNAL));self.finish()

        self.cue('안 보이던 이유마다, 다른 관측 도구','안 부딪힘, 너무 작음, 너무 빠름을\n각기 다른 장치로 넘어섰습니다.')
        rows=[('IceCube','너무 안 부딪힌다','NEUTRINO DETECTOR',OBS),('LIGO','변화가 너무 작다','INTERFEROMETER',UV),('Attosecond','변화가 너무 빠르다','LIGHT PULSE',GOLD)]
        cards=VGroup()
        for i,(name,limit,tool,color) in enumerate(rows):
            y=2.7-i*2.05;box=RoundedRectangle(width=7.2,height=1.55,corner_radius=.18,color=color,fill_color=color,fill_opacity=.035).move_to([0,y,0]);cards.add(VGroup(box,txt(name,y+.35,28,color).shift(LEFT*2.35),txt(limit,y+.35,24,LIGHT).shift(RIGHT*.85),txt('→  '+tool,y-.38,23,color)))
        self.beat(.5,LaggedStart(*[FadeIn(c,shift=UP*.1) for c in cards],lag_ratio=.12));self.add(txt('보이지 않던 것을, 측정 가능하게',-4.15,31,SIGNAL));self.finish()

        self.cue('아토초 세계가, 관측 가능해졌다','새 입자보다 새로운 시간 해상도,\n전자 동역학을 보는 창을 열었습니다.')
        a=atom([0,1.75,0],.9);p=pulse([-3.0,1.1,0],.14,1.7,UV);self.add(a,p);self.beat(.38,p.animate.shift(RIGHT*6))
        self.add(txt('THE ATTOSECOND WORLD',-.25,38,UV),txt('BECOMES OBSERVABLE',-1.05,38,SIGNAL),txt('AGOSTINI  ·  KRAUSZ  ·  L’HUILLIER',-2.05,23,LIGHT),txt('2023 NOBEL PRIZE IN PHYSICS',-3.05,27,GOLD))
        medal=VGroup(Circle(radius=.75,color=GOLD,fill_color='#6B4E1E',fill_opacity=.7),txt('NOBEL',.22,22,GOLD),txt('2023',-.28,31,GOLD)).move_to([0,-4.25,0]);self.beat(.14,FadeIn(medal));self.finish()
