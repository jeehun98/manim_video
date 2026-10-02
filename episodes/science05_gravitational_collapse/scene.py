"""Collisionless contraction, central passage, mixing, and a moving remnant."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import GravitationalLensingDiscovery,txt,LIGHT,OBS,MASS,EXPECT
from episodes.science04_virial_theorem.scene import equation

DATA=np.load(Path(__file__).with_name('collapse_data.npz'))
TIMES=DATA['times'];POSITIONS=DATA['positions'];VELOCITIES=DATA['velocities']

def sample(values,t):
    x=np.clip(t/TIMES[-1]*(len(TIMES)-1),0,len(TIMES)-1)
    i=min(int(x),len(TIMES)-2);return values[i]*(1-(x-i))+values[i+1]*(x-i)

class ParticleView(VGroup):
    def __init__(self,clock,center=(0,.6,0),scale=2.8,arrows=False,bound_only=False):
        super().__init__();self.clock=clock;self.origin=np.array(center,dtype=float);self.scale_factor=scale
        self.indices=np.flatnonzero(DATA['bound']) if bound_only else np.arange(POSITIONS.shape[1])
        self.dots=VGroup(*[Dot(radius=.03,color=LIGHT) for _ in self.indices]);self.add(self.dots)
        self.vectors=VGroup()
        if arrows:
            self.vectors=VGroup(*[Arrow(ORIGIN,RIGHT*.1,buff=0,color=OBS,stroke_width=2,max_tip_length_to_length_ratio=.25) for _ in range(8)])
            self.add(self.vectors)
        self.refresh();self.add_updater(lambda m,dt:m.refresh())

    def refresh(self):
        t=self.clock.get_value();p=sample(POSITIONS,t);v=sample(VELOCITIES,t)
        for j,i in enumerate(self.indices):
            point=self.origin+np.array([p[i,0],p[i,1],0])*self.scale_factor
            visible=abs(point[0])<3.8 and -3.5<point[1]<4.2
            self.dots[j].move_to(point if visible else self.origin).set_opacity(1 if visible else 0)
            if j<len(self.vectors):
                velocity=np.array([v[i,0],v[i,1],0])*.32
                length=np.linalg.norm(velocity)
                if length<.03:velocity=RIGHT*.03
                elif length>.6:velocity*=.6/length
                self.vectors[j].put_start_and_end_on(point if visible else self.origin,(point if visible else self.origin)+velocity).set_opacity(.85 if visible else 0)
        return self

def sphere(radius=2.6,center=(0,.6,0)):
    return VGroup(Circle(radius=radius,color=MASS,stroke_opacity=.3),Ellipse(width=radius*2,height=radius*.55,color=MASS,stroke_opacity=.17)).move_to(center)

class CollapseVirialization(GravitationalLensingDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def cue(self,*args,**kwargs):
        if kwargs.get('clear',True):
            for m in self.mobjects:m.clear_updaters()
        super().cue(*args,**kwargs)

    def flow_to(self,clock,target,frame=None):
        end=self.current['end_frame'] if frame is None else frame
        remaining=end-round(self.time*30)
        if remaining<0:raise RuntimeError('Motion cue overrun')
        if remaining:self.play(clock.animate.set_value(target),run_time=remaining/30,rate_func=linear)
        self.to(end)

    def view(self,start,arrows=False,bound=False,scale=2.8):
        clock=ValueTracker(start);view=ParticleView(clock,arrows=arrows,bound_only=bound,scale=scale)
        self.add(view);return clock,view

    def construct(self):
        self.brand=txt('과학의 한 장면  /  05',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('중력은 당기는데,\n왜 한 점에서 멈추지 않을까?', '끌어당기기만 한다면,\n결국 중심 한 점에 모여야 하지 않을까요?')
        clock,view=self.view(0);outline=sphere();self.add(outline)
        forces=VGroup()
        for a in np.linspace(0,TAU,8,endpoint=False):
            radial=np.array([np.cos(a),np.sin(a),0]);c=np.array([0,.6,0])
            forces.add(Arrow(c+radial*2.65,c+radial*1.85,buff=0,color=MASS,stroke_width=2))
        self.beat(.18,LaggedStart(*[GrowArrow(a) for a in forces],lag_ratio=.04))
        self.add(txt('충돌과 에너지 방출이 적은 중력계를 생각해 봅시다.',-3.35,23,OBS))
        self.beat(.3,clock.animate.set_value(.55),rate_func=linear);self.flow_to(clock,.75)

        self.cue('처음에는, 정말 한 점처럼', '자신의 중력으로 수축하면서,\n중앙의 밀도가 높아집니다.')
        clock,view=self.view(.55);radius=ValueTracker(2.3)
        ring=always_redraw(lambda:sphere(radius.get_value()))
        self.add(ring)
        self.beat(.5,clock.animate.set_value(1.2),radius.animate.set_value(.5),rate_func=linear)
        ring.clear_updaters()
        self.beat(.1,FadeIn(txt('수축 → 밀도 증가',-2.85,31,MASS)))
        self.add(txt('작은 비대칭이 있는 입자 모형의 투영',-3.75,21,'#A9B8CB'));self.flow_to(clock,1.25)

        self.cue('하지만 중심은 벽이 아니다', '중심에 도착했다고 멈추지 않습니다.\n이미 얻은 속도로 반대편까지 지나갑니다.')
        center=np.array([0,.8,0]);star=Dot([-3.1,.8,0],color=LIGHT,radius=.09)
        path=Line([-3.1,.8,0],[3.1,.8,0],color=OBS,stroke_opacity=.4)
        marker=Circle(radius=.15,color=MASS).move_to(center)
        self.add(star,path,marker,txt('중심',-.05,24,MASS))
        self.beat(.38,MoveAlongPath(star,path),rate_func=linear)
        self.beat(.13,FadeIn(txt('가속 → 중심 통과 → 반대편',-2.55,31,OBS)))
        self.add(txt('중심을 통과하는 한 궤도를 확대한 개념도',-3.65,22,'#A9B8CB'));self.finish()

        self.cue('떨어질수록, 더 빠르게', '중력 위치에너지가 줄어들면서,\n운동에너지는 늘어납니다.')
        rows=VGroup()
        for y,length,label in [(2.2,.5,'멀리'),(.5,1.1,'안쪽'),(-1.2,2,'중심 부근')]:
            point=np.array([-2.3,y,0])
            rows.add(VGroup(Dot(point,color=LIGHT,radius=.08),Arrow(point,point+RIGHT*length,buff=.1,color=OBS),txt(label,y,25,LIGHT).shift(RIGHT*2.2)))
        self.beat(.25,LaggedStart(*[FadeIn(row) for row in rows],lag_ratio=.3))
        self.beat(.15,FadeIn(txt('위치에너지 감소 → 운동에너지 증가',-2.85,29,OBS)))
        self.add(txt('중력이 사라지거나, 새로운 바깥 힘이 생기지 않습니다.',-4,22,'#A9B8CB'));self.finish()

        self.cue('서로 부딪히지 않고 지나간다', '입자들은 중심 부근에서 서로 지나치고,\n다시 바깥으로 움직입니다.')
        clock,view=self.view(.75,arrows=True)
        self.beat(.58,clock.animate.set_value(2.7),rate_func=linear)
        self.beat(.12,FadeIn(txt('통과하며 궤도가 겹친다',-2.9,29,OBS)))
        self.add(txt('충돌에 의한 튕김을 표현한 장면이 아닙니다.',-3.9,22,'#A9B8CB'));self.flow_to(clock,3.1)

        self.cue('처음과 똑같이 되돌아가지 않는다', '비대칭과 시간에 따라 변하는 중력장이,\n입자들의 궤도와 에너지를 뒤섞습니다.')
        clock,view=self.view(2.7,arrows=True)
        self.beat(.63,clock.animate.set_value(9),rate_func=linear)
        self.add(txt('입자별 에너지 재분배 · 궤도의 위상 혼합',-2.95,25,OBS),txt('마찰로 전체 에너지가 사라지는 과정이 아닙니다.',-4,22,'#A9B8CB'));self.flow_to(clock,10.5)

        self.cue('수축과 팽창, 그리고 혼합', '한 번에 한 점으로 끝나는 대신,\n대표 크기가 요동하다 비교적 안정됩니다.')
        axes=Axes(x_range=[0,24,6],y_range=[0,1,.25],x_length=6.6,y_length=3.1,axis_config={'include_ticks':False,'color':'#A9B8CB'}).move_to([0,.4,0])
        curve=VMobject(color=OBS,stroke_width=3).set_points_as_corners([axes.c2p(t,r) for t,r in zip(TIMES,DATA['radii'])])
        self.beat(.12,Create(axes))
        self.beat(.43,Create(curve),rate_func=linear)
        self.add(txt('대표 크기',2.75,25,LIGHT),txt('시간',-1.75,25),txt('절반의 입자를 포함하는 3D 반지름',-2.65,23,OBS),txt('설명용 입자 모형 · 시간과 길이는 임의 단위',-3.65,21,'#A9B8CB'))
        self.finish()

        self.cue('멈추지 않았는데, 안정된다', '일부는 벗어날 수 있지만, 남은 입자들은\n계속 움직이며 넓은 분포를 유지할 수 있습니다.')
        clock,view=self.view(16,arrows=True,bound=True)
        outline=sphere(2.4);self.add(outline)
        self.beat(.6,clock.animate.set_value(21),rate_func=linear)
        self.add(txt('개별 입자: 움직임은 계속',-2.65,28,OBS),txt('전체 분포: 비교적 일정',-3.55,28,MASS));self.flow_to(clock,24)

        self.cue('움직이는 안정, 비리얼 관계', '오랫동안 안정된 계에서는, 평균 에너지가\n비리얼 정리의 관계에 가까워집니다.')
        clock,view=self.view(18,arrows=True,bound=True,scale=2.3)
        self.beat(.1,FadeIn(equation('2K + U ≈ 0',-2.2)))
        bars=VGroup(Rectangle(width=2.3,height=.22,fill_color=OBS,fill_opacity=.85,stroke_width=0).move_to([-1.3,-3.05,0]),Rectangle(width=2.3,height=.22,fill_color=MASS,fill_opacity=.85,stroke_width=0).move_to([1.3,-3.05,0]))
        self.beat(.12,FadeIn(bars),FadeIn(txt('2K',-3.5,25,OBS).shift(LEFT*1.3)),FadeIn(txt('−U',-3.5,25,MASS).shift(RIGHT*1.3)))
        self.add(txt('K·U: 시간 평균값 · 관계를 나타낸 개념도',-4.25,21,'#A9B8CB'))
        self.beat(.45,clock.animate.set_value(22),rate_func=linear);self.flow_to(clock,24)

        self.cue('한 점 대신, 넓은 중력 구조', '붕괴하며 얻은 운동은 사라지지 않고,\n서로 다른 속박된 궤도에 분포할 수 있습니다.')
        initial=VGroup(*[Dot([p[0]*1.25-2.4,p[1]*1.25+.75,0],radius=.025,color=LIGHT) for p in POSITIONS[0]])
        clock=ValueTracker(19);final=ParticleView(clock,center=(2.25,.75,0),scale=1.9,bound_only=True)
        self.add(initial,final)
        self.beat(.15,FadeIn(sphere(1.25,(-2.4,.75,0))),FadeIn(sphere(1.6,(2.25,.75,0))))
        self.beat(.12,GrowArrow(Arrow([-1,.75,0],[.6,.75,0],color=OBS,buff=.1)))
        self.add(txt('초기 분포',-1.55,25,LIGHT).shift(LEFT*2.4),txt('수축과 혼합 뒤',-1.55,25,MASS).shift(RIGHT*2.25),txt('Halo · 넓게 분포한 속박된 중력계',-3.2,29,MASS))
        self.beat(.4,clock.animate.set_value(23),rate_func=linear)
        self.add(txt('형태 비교 · 초기와 최종의 표시 축척은 다릅니다.',-4.15,22,'#A9B8CB'));self.flow_to(clock,24)

        self.cue('움직이면서 안정된다', '중력이 만든 안정은,\n멈춤이 아니라 계속되는 운동일 수 있습니다.')
        clock,view=self.view(19,arrows=True,bound=True);self.add(sphere(2.4))
        self.beat(.1,FadeIn(txt('Gravitational Collapse',-2.35,31,OBS)),FadeIn(txt('↓',-3.05,31,MASS)),FadeIn(txt('Virialization',-3.75,34,MASS)))
        self.beat(.55,clock.animate.set_value(22),rate_func=linear)
        self.flow_to(clock,24,self.current['end_frame']-round(self.span_frames*.08))
        view.clear_updaters();self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)]);self.finish()
