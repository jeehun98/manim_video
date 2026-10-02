"""One background expansion, with a sufficiently overdense region turning around."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import GravitationalLensingDiscovery,txt,LIGHT,OBS,MASS,EXPECT
from episodes.science04_virial_theorem.scene import equation,MovingCluster

THETA=np.linspace(.55,5.35,1001)
TIME=THETA-np.sin(THETA)
TMAX=TIME[-1]

def theta(t):return np.interp(t,TIME,THETA)
def local_radius(t):return (1-np.cos(theta(t)))/2
def background(t):return 6**(2/3)/4*np.asarray(t)**(2/3)
def local_speed(t):
    angle=theta(t);return np.sin(angle)/(2*(1-np.cos(angle)))

def grid(spacing=.9,opacity=.2):
    """A cropped patch of a grid, never the edge of the Universe."""
    g=VGroup()
    xs=[x*spacing for x in range(-7,8) if abs(x*spacing)<3.75]
    ys=[.65+y*spacing for y in range(-7,8) if -2.1<.65+y*spacing<3.8]
    for x in xs:g.add(Line([x,-2.1,0],[x,3.8,0],color=OBS,stroke_opacity=opacity,stroke_width=1))
    for y in ys:g.add(Line([-3.75,y,0],[3.75,y,0],color=OBS,stroke_opacity=opacity,stroke_width=1))
    for x in xs:
        for y in ys:g.add(Dot([x,y,0],radius=.025,color=OBS).set_opacity(opacity*2))
    return g

RNG=np.random.default_rng(19)
POINTS=RNG.normal(size=(26,2));POINTS/=np.linalg.norm(POINTS,axis=1)[:,None]
POINTS*=RNG.uniform(.1,.88,(26,1))**.5

def region(radius,center=(0,.65,0),motion=0,gravity=False):
    c=np.array(center,dtype=float);g=VGroup(Circle(radius=max(.03,radius),color=LIGHT,stroke_opacity=.65))
    g[0].move_to(c)
    for point in POINTS:g.add(Dot(c+np.array([point[0],point[1],0])*radius,radius=.03,color=LIGHT))
    for a in (0,PI/2,PI,3*PI/2):
        radial=np.array([np.cos(a),np.sin(a),0]);edge=c+radial*radius
        if abs(motion)>.02:
            length=np.clip(abs(motion)*.45,.07,.65)
            g.add(Arrow(edge,edge+radial*np.sign(motion)*length,buff=0,color=OBS if motion>0 else EXPECT,stroke_width=2))
        if gravity:
            g.add(Arrow(edge-radial*.05,edge-radial*.32,buff=0,color=MASS,stroke_width=2))
    return g

class TurnaroundDiscovery(GravitationalLensingDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def to(self,frame):
        remaining=frame-round(self.time*30)
        if remaining<0:raise RuntimeError(f'Cue overrun at {self.time}: target {frame/30}')
        # Keep np.arange's floating-point endpoint from adding a dynamic wait frame.
        if remaining:self.wait(remaining/30-1e-6)

    def cue(self,*args,**kwargs):
        if kwargs.get('clear',True):
            for m in self.mobjects:m.clear_updaters()
        super().cue(*args,**kwargs)

    def graphs(self,clock):
        axes=Axes(x_range=[0,TMAX,1],y_range=[0,3,1],x_length=6.65,y_length=3.7,
                  axis_config={'include_ticks':False,'color':'#A9B8CB'}).move_to([0,.3,0])
        def path(func):
            end=max(TIME[0]+.001,clock.get_value())
            return VMobject(color=OBS if func is background else LIGHT,stroke_width=3).set_points_as_corners([axes.c2p(t,func(t)) for t in np.linspace(TIME[0],end,180)])
        mean=always_redraw(lambda:path(background));local=always_redraw(lambda:path(local_radius))
        points=always_redraw(lambda:VGroup(Dot(axes.c2p(clock.get_value(),background(clock.get_value())),color=OBS,radius=.055),Dot(axes.c2p(clock.get_value(),local_radius(clock.get_value())),color=LIGHT,radius=.055)))
        self.add(axes,mean,local,points)
        self.add(txt('평균 팽창  a(t)',3.4,27,OBS),txt('과밀 영역의 반지름  R(t)',2.75,26,LIGHT),txt('시간',-2.3,24),txt('동일 시간축 · 크기를 정규화한 모형',-3.3,22,'#A9B8CB'))
        return axes,mean,local,points

    def construct(self):
        self.brand=txt('과학의 한 장면  /  06',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('우주가 팽창한다면?', '중심에서 바깥으로 퍼지는 폭발처럼\n생각하기 쉽습니다.')
        burst=VGroup(Dot(radius=.09,color=OBS),Circle(radius=.2,color=OBS))
        self.add(burst);self.beat(.3,burst.animate.scale(11))
        x=VGroup(Line([-1.6,-.9,0],[1.6,2.3,0],color=EXPECT,stroke_width=5),Line([-1.6,2.3,0],[1.6,-.9,0],color=EXPECT,stroke_width=5))
        self.beat(.15,Create(x),FadeIn(txt('우주 전체가 이런 폭발인 것은 아닙니다.',-3.1,27,EXPECT)));self.finish()

        self.cue('경계가 아니라, 거리의 스케일', '평균적으로는 같은 팽창을 따라,\n멀리 떨어진 위치 사이의 거리가 늘어납니다.')
        spacing=ValueTracker(.72);patch=always_redraw(lambda:grid(spacing.get_value(),.35));self.add(patch)
        distance=always_redraw(lambda:DoubleArrow([-spacing.get_value(),.65,0],[spacing.get_value(),.65,0],buff=.04,color=LIGHT))
        self.add(distance);self.beat(.5,spacing.animate.set_value(1.23),rate_func=linear)
        self.add(txt('특별한 중심 없음 · 거리의 스케일 증가',-2.95,28,OBS),txt('격자는 우주의 일부를 잘라낸 표현입니다.',-3.9,22,'#A9B8CB'));self.finish()

        self.cue('처음에는 아주 작은 밀도 차이', '어떤 영역은 주변보다\n조금 더 많은 물질을 가지고 있었습니다.')
        spacing=ValueTracker(.85);clock=ValueTracker(.18)
        patch=always_redraw(lambda:grid(spacing.get_value(),.17));self.add(patch)
        local=always_redraw(lambda:region(.8+.5*(clock.get_value()-.18),motion=.4))
        self.add(local)
        self.beat(.45,spacing.animate.set_value(1.1),clock.animate.set_value(.8),rate_func=linear)
        self.add(txt('평균적인 배경 + 조금 더 조밀한 영역',-2.95,28,LIGHT),txt('밀도 차이는 이해를 돕기 위해 과장했습니다.',-3.95,21,'#A9B8CB'));self.finish()

        self.cue('둘 다, 처음에는 팽창한다', '조금 더 조밀한 영역도 처음에는\n우주와 함께 커집니다.')
        clock=ValueTracker(.35)
        mean=always_redraw(lambda:region(background(clock.get_value())*.72,(-2.05,.8,0),motion=.3))
        local=always_redraw(lambda:region(local_radius(clock.get_value())*.72,(2.05,.8,0),motion=local_speed(clock.get_value())))
        self.add(mean,local,txt('평균 팽창',-1.7,25,OBS).shift(LEFT*2.05),txt('과밀 영역',-1.7,25,LIGHT).shift(RIGHT*2.05))
        self.beat(.55,clock.animate.set_value(2),rate_func=linear)
        self.add(equation('a(t) ↑',-2.9,OBS,34).shift(LEFT*2.05),equation('R(t) ↑',-2.9,LIGHT,34).shift(RIGHT*2.05));self.finish()

        self.cue('중력은 처음부터, 바깥 운동을 감속', '더 많은 질량의 중력이,\n이 영역의 팽창을 계속 늦춥니다.')
        clock=ValueTracker(1.5)
        local=always_redraw(lambda:region(local_radius(clock.get_value())*2.1,motion=local_speed(clock.get_value()),gravity=True))
        self.add(local)
        self.beat(.55,clock.animate.set_value(PI-.12),rate_func=linear)
        self.add(txt('보라: 중력은 계속 안쪽으로',-2.7,27,MASS),txt('청록: 바깥 운동은 점점 느려진다',-3.55,27,OBS));self.finish()

        self.cue('한 시간축, 두 가지 크기 변화', '우주는 계속 팽창하는 동안에도,\n한 지역은 평균 팽창에서 벗어날 수 있습니다.')
        clock=ValueTracker(TIME[0]);axes,_,_,_=self.graphs(clock)
        self.beat(.62,clock.animate.set_value(TMAX),rate_func=linear)
        ta=Dot(axes.c2p(PI,1),radius=.08,color=MASS)
        self.beat(.1,FadeIn(ta),FadeIn(txt('계속 팽창하는 배경 · 돌아서는 지역',-4.25,27,MASS)));self.finish()

        self.cue('최대 크기, Turnaround', '이 영역의 팽창 속도가 0이 되는 순간,\n최대 크기에 도달합니다.')
        clock=ValueTracker(PI-.8)
        local=always_redraw(lambda:region(local_radius(clock.get_value())*2.15,motion=local_speed(clock.get_value()),gravity=True));self.add(local)
        self.beat(.4,clock.animate.set_value(PI),rate_func=linear)
        self.beat(.12,FadeIn(txt('Turnaround',-2.35,36,MASS)),FadeIn(equation('dR/dt = 0',-3.25)))
        self.add(txt('지역의 반지름이 최대 · 중력은 계속 작용',-4.2,24,LIGHT));self.finish()

        self.cue('최고점에서의 공과 비슷하다', '바깥으로 가던 속도만 0일 뿐,\n중력은 계속 안쪽을 향합니다.')
        phase=ValueTracker(0)
        ball=always_redraw(lambda:Dot([-2.2,-.5+3.2*(1-(phase.get_value()-1)**2),0],radius=.12,color=OBS))
        gravity=always_redraw(lambda:Arrow(ball.get_center()+RIGHT*.35,ball.get_center()+RIGHT*.35+DOWN*.65,buff=0,color=MASS))
        patch=always_redraw(lambda:region(.75+.55*(1-(phase.get_value()-1)**2),(1.7,1.2,0),motion=(1-phase.get_value())*.4,gravity=True))
        self.add(ball,gravity,patch)
        self.beat(.22,phase.animate.set_value(1),rate_func=linear)
        self.beat(.12,FadeIn(equation('dR/dt = 0',-2.55)),FadeIn(equation('d²R/dt² < 0',-3.5,MASS,36)))
        self.beat(.22,phase.animate.set_value(2),rate_func=linear)
        self.add(txt('운동 방향이 바뀌는 순간을 비교한 비유',-4.35,21,'#A9B8CB'));self.finish()

        self.cue('주변은 팽창, 이 영역은 수축', '주변 우주는 계속 넓어지지만,\n이 영역은 반대로 작아지기 시작합니다.')
        clock=ValueTracker(PI);spacing=ValueTracker(.9)
        self.add(always_redraw(lambda:grid(spacing.get_value(),.16)),always_redraw(lambda:region(local_radius(clock.get_value())*2,motion=local_speed(clock.get_value()))))
        self.beat(.6,clock.animate.set_value(5.9),spacing.animate.set_value(1.6),rate_func=linear)
        self.add(txt('평균 우주: 팽창',-2.8,29,OBS),txt('과밀 영역: 수축',-3.65,29,LIGHT));self.finish()

        self.cue('국소 붕괴가, 구조의 시작', '수축 뒤에는 궤도 혼합을 거쳐,\n속박된 중력 구조가 만들어질 수 있습니다.')
        spacing=ValueTracker(1.15);self.add(always_redraw(lambda:grid(spacing.get_value(),.13)))
        contracting=region(.8);self.add(contracting)
        self.beat(.2,contracting.animate.scale(.65))
        bound=MovingCluster(radius=1.15,speed=1.1,arrows=True)
        self.beat(.15,FadeOut(contracting));self.add(bound)
        self.beat(.32,spacing.animate.set_value(1.6),rate_func=linear)
        self.add(txt('국소 붕괴 → 궤도 혼합 → 속박된 구조',-2.7,28,MASS),txt('충분히 조밀한 영역의 예 · 모든 과밀 영역이 붕괴하지는 않습니다.',-4,21,'#A9B8CB'));self.finish()

        self.cue('우주 전체가 멈춘 순간이 아니다', '팽창하던 한 지역이, 중력 때문에\n수축으로 방향을 바꾸는 순간입니다.')
        clock=ValueTracker(TMAX);axes,_,_,_=self.graphs(clock)
        self.beat(.12,FadeIn(Dot(axes.c2p(PI,1),radius=.075,color=MASS)))
        self.beat(.15,FadeIn(txt('Turnaround · 팽창에서 붕괴로',-4.25,31,MASS)))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        for m in self.mobjects:m.clear_updaters()
        self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)]);self.finish()
