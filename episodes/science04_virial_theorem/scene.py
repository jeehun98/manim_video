"""Size and velocity dispersion as a scale for an equilibrium gravitational system."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import GravitationalLensingDiscovery, txt, LIGHT, EXPECT, OBS, MASS

def equation(s,y=-2.8,color=OBS,size=42):
    obj=Text(s,font='Cambria',font_size=size,color=color)
    if obj.width>7.5:obj.scale_to_fit_width(7.5)
    return obj.move_to([0,y,0])

class MovingCluster(VGroup):
    """Bounded illustrative tracer motions; not an N-body simulation."""
    def __init__(self,center=(0,.7,0),radius=1.5,speed=1,arrows=False):
        super().__init__()
        self.center=np.array(center,dtype=float);self.radius=radius;self.speed=speed;self.elapsed=0
        rng=np.random.default_rng(44)
        self.phases=rng.uniform(0,TAU,24);self.radii=radius*rng.uniform(.2,.74,24)
        self.frequencies=rng.uniform(.65,1.3,24);self.signs=rng.choice([-1,1],24)
        self.boundary=Circle(radius=radius,color=MASS,stroke_opacity=.35).move_to(center)
        self.dots=VGroup(*[Dot(radius=.038,color=LIGHT) for _ in range(24)])
        self.vectors=VGroup()
        self.add(self.boundary,self.dots)
        self.show_arrows=arrows
        if arrows:
            self.vectors=VGroup(*[Arrow(ORIGIN,RIGHT*.2,buff=0,color=OBS,stroke_width=2,max_tip_length_to_length_ratio=.25) for _ in range(8)])
            self.add(self.vectors)
        self.update_motion(0)
        self.add_updater(lambda m,dt:m.update_motion(dt))

    def update_motion(self,dt):
        self.elapsed+=dt
        for i,dot in enumerate(self.dots):
            a=self.phases[i]+self.elapsed*self.frequencies[i]*self.signs[i]*self.speed
            r=self.radii[i]
            p=self.center+np.array([r*np.cos(a),.8*r*np.sin(a*1.13),0])
            dot.move_to(p)
            if self.show_arrows and i<8:
                v=np.array([-np.sin(a),.904*np.cos(a*1.13),0])*self.speed*.23
                if np.linalg.norm(v)<.03:v=RIGHT*.03
                self.vectors[i].put_start_and_end_on(p,p+v)
        return self

def mass_bar(x,y,width,label):
    bar=Rectangle(width=width,height=.24,stroke_width=0,fill_color=MASS,fill_opacity=.85).move_to([x-1+width/2,y,0])
    return VGroup(bar,txt(label,y-.45,23,MASS).shift(RIGHT*x))

def trajectory(mu):
    position=np.array([.85,0.,0]);velocity=np.array([0.,1.7,0]);points=[];dt=.005
    for _ in range(400):
        points.append(position.copy());acc=-mu*position/np.linalg.norm(position)**3
        next_pos=position+velocity*dt+.5*acc*dt*dt
        next_acc=-mu*next_pos/np.linalg.norm(next_pos)**3
        velocity+=.5*(acc+next_acc)*dt;position=next_pos
    return points

class VirialMassDiscovery(GravitationalLensingDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def cue(self,*args,**kwargs):
        # Retire illustrative motion updaters before a stage is removed.
        if kwargs.get('clear',True):
            for m in self.mobjects:
                if isinstance(m,MovingCluster):m.clear_updaters()
        super().cue(*args,**kwargs)

    def construct(self):
        self.brand=txt('과학의 한 장면  /  04',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('저울에 올릴 수 없는 은하단', '너무 크고 먼 천체의 질량은\n어떻게 잴 수 있을까요?')
        cluster=MovingCluster(radius=2.45,speed=.45);self.add(cluster)
        scale=VGroup(Line([-1,-2.65,0],[1,-2.65,0]),Line([0,-3.35,0],[0,-2.35,0]),Line([-.55,-3.35,0],[.55,-3.35,0]),
                     Arc(radius=.3,start_angle=PI,angle=PI).move_to([-.8,-3.05,0]),Arc(radius=.3,start_angle=PI,angle=PI).move_to([.8,-3.05,0]))
        self.beat(.22,Create(scale));self.beat(.18,FadeOut(scale));self.finish()

        self.cue('우리가 측정할 수 있는 움직임', '은하들이 얼마나 빠르게 움직이는지\n그 빛의 스펙트럼으로 측정합니다.')
        cluster=MovingCluster(radius=2.35,speed=1,arrows=True);self.add(cluster)
        spectrum=VGroup(Line([-2.5,-2.55,0],[2.5,-2.55,0],color=OBS),*[Line([x,-2.8,0],[x,-2.3,0],color=LIGHT) for x in (-1.9,-.6,.8,1.6)])
        self.beat(.17,FadeIn(spectrum),FadeIn(txt('스펙트럼의 이동 → 시선 방향 속도',-3.3,25,OBS)))
        self.beat(.18,spectrum[1:].animate.shift(RIGHT*.4));self.beat(.1,FadeIn(txt('움직임 → 질량?',-4.15,31,MASS)));self.finish()

        self.cue('빠른 은하들을 붙잡으려면', '같은 속도라도 중력이 약하면 벗어나고,\n충분히 강하면 묶여 있을 수 있습니다.')
        centers=[np.array([-2.1,.4,0]),np.array([2.1,.4,0])]
        paths=[];dots=[]
        for c,mu in zip(centers,(.5,2.8)):
            self.add(Circle(radius=1.25,color=MASS,stroke_opacity=.35).move_to(c),Dot(c,color=MASS,radius=.1))
            path=VMobject(color=OBS,stroke_width=2).set_points_as_corners([p+c for p in trajectory(mu)])
            paths.append(path);dots.append(Dot(path.get_start(),color=LIGHT,radius=.065))
        self.add(*dots,txt('작은 질량',-1.4,25,EXPECT).shift(LEFT*2.1),txt('큰 질량',-1.4,25,MASS).shift(RIGHT*2.1))
        self.beat(.38,MoveAlongPath(dots[0],paths[0]),MoveAlongPath(dots[1],paths[1]),Create(paths[0]),Create(paths[1]),rate_func=linear)
        self.beat(.15,FadeIn(txt('같은 크기 · 같은 출발 속도',-2.65,25)),FadeIn(txt('빠른 은하들이 계속 묶여 있다면?',-3.5,28,OBS)))
        self.add(txt('탈출과 속박을 비교한 단순 중력 모형',-4.25,21,'#A9B8CB'));self.finish()

        self.cue('같은 크기라면, 빠를수록 무겁다', '대표 속도가 2배라면,\n필요한 질량은 약 4배가 됩니다.')
        a=MovingCluster((-2.1,.8,0),1.25,.6,True);b=MovingCluster((2.1,.8,0),1.25,.6,True);self.add(a,b)
        self.add(txt('속도 1×',-1.25,25,OBS).shift(LEFT*2.1))
        label=txt('속도 1×',-1.25,25,OBS).shift(RIGHT*2.1);self.add(label)
        self.beat(.2,Transform(label,txt('속도 2×',-1.25,25,OBS).shift(RIGHT*2.1)))
        b.speed=1.2
        self.beat(.18,FadeIn(mass_bar(-2.1,-2.1,.65,'질량 1×')),FadeIn(mass_bar(2.1,-2.1,2.6,'질량 4×')))
        self.beat(.12,FadeIn(equation('M ∝ v²',-3.6)))
        self.add(txt('크기와 구조가 비슷한 안정된 계끼리 비교',-4.45,21,'#A9B8CB'));self.finish()

        self.cue('같은 속도라면, 클수록 무겁다', '더 넓게 퍼진 은하들을 같은 속도로 묶으려면,\n더 많은 질량이 필요합니다.')
        a=MovingCluster((-2.15,.85,0),.82,.8,True);b=MovingCluster((2.05,.85,0),1.64,.8,True)
        # Equal physical speeds: larger tracers take longer to cross their system.
        b.frequencies*=.5
        self.add(a,b,Line([-2.15,.85,0],[-1.33,.85,0],color=LIGHT),Line([2.05,.85,0],[3.69,.85,0],color=LIGHT))
        self.add(txt('크기 1×',-1.25,25,LIGHT).shift(LEFT*2.15),txt('크기 2×',-1.25,25,LIGHT).shift(RIGHT*2.05))
        self.beat(.18,FadeIn(mass_bar(-2.15,-2.1,1.1,'질량 1×')),FadeIn(mass_bar(2.05,-2.1,2.2,'질량 2×')))
        self.beat(.14,FadeIn(equation('M ∝ R',-3.65)))
        self.add(txt('같은 대표 속도 · 비슷한 구조',-4.45,23,'#A9B8CB'));self.finish()

        self.cue('수식 하나로 묶으면', '질량은 크기에 비례하고,\n대표 속도의 제곱에 비례합니다.')
        self.beat(.18,FadeIn(equation('M ∼ R v² / G',1.6,size=50)))
        items=VGroup(txt('R   크기 2배 → 질량 약 2배',-.1,30,LIGHT),txt('v²  속도 2배 → 질량 약 4배',-1.3,30,OBS),txt('G   중력 상수: 고정값',-2.5,29,MASS))
        for item in items:self.beat(.12,FadeIn(item))
        self.add(txt('∼ : 구조에 따른 계수를 생략한 크기 관계',-4.1,23,'#A9B8CB'));self.finish()

        self.cue('비리얼 정리의 바탕', '평균 크기가 안정된 중력계에서,\n운동에너지와 중력 에너지가 균형을 이룹니다.')
        cluster=MovingCluster(radius=1.85,speed=1.1,arrows=True);self.add(cluster)
        self.beat(.14,FadeIn(equation('2K + U = 0',-2.0,size=42)))
        kbar=Rectangle(width=2.4,height=.25,stroke_width=0,fill_color=OBS,fill_opacity=.85).move_to([-1.35,-3.15,0])
        ubar=Rectangle(width=2.4,height=.25,stroke_width=0,fill_color=MASS,fill_opacity=.85).move_to([1.35,-3.15,0])
        self.beat(.15,FadeIn(kbar),FadeIn(ubar),FadeIn(txt('2K',-3.65,26,OBS).shift(LEFT*1.35)),FadeIn(txt('−U',-3.65,26,MASS).shift(RIGHT*1.35)))
        self.add(txt('K와 U는 오랜 시간의 평균값 · U < 0',-4.3,22,'#A9B8CB'))
        self.finish()

        self.cue('한 개의 속도보다, 속도의 퍼짐', '평균 운동을 뺀 은하들의 시선 방향 속도에서\n속도 분산을 측정합니다.')
        values=np.array([-1.9,-1.6,-1.2,-.9,-.7,-.5,-.3,-.15,0,.1,.25,.45,.6,.8,1.1,1.3,1.6,2.0])
        values-=values.mean()
        source=VGroup(*[Arrow([-2.5,.3+i*.11,0],[-2.5+v*.5,.3+i*.11,0],buff=0,color=OBS) for i,v in enumerate(values) if v])
        self.beat(.16,FadeIn(source))
        axis=Line([-3.3,-.2,0],[3.3,-.2,0],color=WHITE)
        dots=VGroup(*[Dot([v*1.4,.2+(i%3)*.19,0],radius=.055,color=OBS) for i,v in enumerate(values)])
        self.beat(.22,FadeOut(source),Create(axis),FadeIn(dots))
        self.add(txt('평균을 뺀 시선 방향 속도',-1.2,24),txt('0',-.6,22))
        sigma=np.std(values)*1.4
        width=DoubleArrow([0,1.45,0],[sigma,1.45,0],buff=0,color=LIGHT)
        self.beat(.12,GrowArrow(width),FadeIn(equation('σᵥ',2.15,LIGHT,38).shift(RIGHT*sigma/2)))
        self.beat(.12,FadeIn(equation('M ∼ C · R σᵥ² / G',-2.65,size=42)))
        self.add(txt('C: 구조와 관측 방향을 반영하는 계수',-3.65,23,'#A9B8CB'));self.finish()

        self.cue('크기와 움직임이 저울이 된다', '크기와 속도 분산으로 전체 질량을 추정합니다.\n충돌 중인 계에는 그대로 적용하기 어렵습니다.')
        cluster=MovingCluster(radius=2.1,speed=.9,arrows=True);self.add(cluster)
        radius=Arrow([0,.7,0],[2.1,.7,0],color=LIGHT,buff=0)
        self.beat(.15,GrowArrow(radius),FadeIn(equation('R',1.05,LIGHT,32).shift(RIGHT*1.1)))
        pair=VGroup(equation('R',-2.25,LIGHT),equation('σᵥ',-2.25,OBS).shift(RIGHT*2))
        pair[0].shift(LEFT*2)
        self.beat(.17,FadeIn(pair))
        self.beat(.17,ReplacementTransform(pair,txt('M  전체 질량',-2.25,38,MASS)))
        self.add(txt('질량 추정의 조건: 평균 크기가 안정된 계',-3.45,26,MASS),txt('앞 편의 충돌 은하단에는 평형 가정부터 확인',-4.25,22,'#A9B8CB'));self.finish()

        self.cue('움직임으로 질량을 잰다', '같은 크기라면 빠를수록 더 무겁고,\n같은 속도라면 클수록 더 무겁습니다.')
        cluster=MovingCluster(radius=1.65,speed=.8,arrows=True);self.add(cluster)
        self.beat(.12,FadeIn(txt('Virial Theorem',-1.65,37,MASS)))
        self.beat(.16,FadeIn(txt('같은 크기: 빠를수록 무겁다\n같은 속도: 클수록 무겁다',-3.15,31,OBS)))
        self.to(self.current['end_frame']-round(self.span_frames*.08));cluster.clear_updaters()
        self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)]);self.finish()
