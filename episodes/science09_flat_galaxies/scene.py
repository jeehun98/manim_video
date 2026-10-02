"""Gravity contracts, angular momentum survives, gas cooling reduces thickness."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT, OBS, MASS, EXPECT
from episodes.science04_virial_theorem.scene import equation
from episodes.science08_density_growth.scene import DensityGrowthDiscovery, matter_sphere


def project(point, inclination, center=np.array([0., 1., 0.])):
    x, y, z = point
    return center+np.array([x, y*np.cos(inclination)+z*np.sin(inclination), 0.])


class RotatingCloud(VGroup):
    """Homologous illustrative gas: R²ω fixed, independent vertical amplitude."""
    def __init__(self, radius, height, inclination=PI/3, arrows='tangent'):
        super().__init__()
        self.radius_tracker = radius;self.height_tracker = height;self.inclination = inclination
        self.elapsed = 0.;self.phase = 0.;self.arrow_mode = arrows
        rng = np.random.default_rng(91)
        self.q = rng.uniform(.08, .95, 42)**.5
        self.a = np.sqrt(1-self.q**2)*rng.uniform(.35, 1, 42)
        self.phases = rng.uniform(0, TAU, 42);self.zphases = rng.uniform(0, TAU, 42)
        self.dots = VGroup(*[Dot(radius=.043, color=OBS) for _ in self.q])
        self.boundary = Ellipse(width=4, height=4, color=OBS, stroke_opacity=.28)
        self.vectors = VGroup(*[Arrow(ORIGIN, RIGHT*.1, buff=0, color=EXPECT if arrows=='vertical' else MASS,
                                     stroke_width=2) for _ in range(7)])
        self.add(self.boundary, self.dots)
        if arrows:self.add(self.vectors)
        self.motion(0);self.add_updater(lambda m, dt: m.motion(dt))

    def motion(self, dt):
        r = self.radius_tracker.get_value();h = self.height_tracker.get_value();omega = .8/r**2
        self.elapsed += dt;self.phase += dt*omega
        extent = np.sqrt((r*np.cos(self.inclination))**2+(h*np.sin(self.inclination))**2)
        self.boundary.stretch_to_fit_width(2*r).stretch_to_fit_height(max(.05, 2*extent)).move_to([0, 1, 0])
        for i, dot in enumerate(self.dots):
            p = self.phases[i]+self.phase;zphase = self.zphases[i]+self.elapsed*1.2
            xyz = np.array([r*self.q[i]*np.cos(p), r*self.q[i]*np.sin(p), h*self.a[i]*np.sin(zphase)])
            pos = project(xyz, self.inclination);dot.move_to(pos)
            if self.arrow_mode and i<7:
                if self.arrow_mode=='vertical':
                    velocity = np.array([0., 0., .65*h*self.a[i]*np.cos(zphase)])
                else:
                    velocity = r*self.q[i]*omega*np.array([-np.sin(p), np.cos(p), 0.])
                vec = project(velocity, self.inclination, np.zeros(3))*.85
                if np.linalg.norm(vec)<.02:vec=RIGHT*.02
                self.vectors[i].put_start_and_end_on(pos, pos+vec)
        return self


class GalaxyView(VGroup):
    """One unchanging thick bulge plus thin 3D disk; only viewing angle changes."""
    def __init__(self, view):
        super().__init__();self.view=view;self.phase=0.
        rng=np.random.default_rng(92)
        self.radii=rng.uniform(.1,1,120)**.6*2.25
        self.angles=1.7*np.log(self.radii+.15)+rng.integers(0,3,120)*TAU/3+rng.normal(0,.2,120)
        self.z=np.clip(rng.normal(0,.06,120),-.14,.14)
        self.stars=VGroup(*[Dot(radius=rng.uniform(.025,.045),color=LIGHT) for _ in self.radii])
        bulge=rng.normal(size=(36,3));bulge/=np.linalg.norm(bulge,axis=1)[:,None]
        self.bulge_xyz=bulge*rng.uniform(.05,.38,(36,1))
        self.bulge=VGroup(*[Dot(radius=.035,color=LIGHT) for _ in self.bulge_xyz])
        self.arms=VGroup(*[VMobject(color=OBS,stroke_width=2,stroke_opacity=.5) for _ in range(3)])
        self.glow=VGroup(*[Circle(radius=r,stroke_width=0,fill_color=LIGHT,fill_opacity=.05).move_to([0,1,0]) for r in [.4,.3,.2,.1]])
        self.glow.add(Circle(radius=.4,color=LIGHT,stroke_opacity=.28,stroke_width=1.5,
                             fill_color=LIGHT,fill_opacity=.04).move_to([0,1,0]))
        self.add(self.arms,self.stars,self.glow,self.bulge)
        self.motion(0);self.add_updater(lambda m,dt:m.motion(dt))

    def motion(self,dt):
        self.phase+=dt*.1;inc=self.view.get_value()
        for dot,r,a,z in zip(self.stars,self.radii,self.angles,self.z):
            dot.move_to(project([r*np.cos(a+self.phase),r*np.sin(a+self.phase),z],inc))
        for dot,p in zip(self.bulge,self.bulge_xyz):dot.move_to(project(p,inc))
        for i,arm in enumerate(self.arms):
            rs=np.linspace(.18,2.3,65)
            arm.set_points_as_corners([project([r*np.cos(1.7*np.log(r+.15)+i*TAU/3+self.phase),
                                               r*np.sin(1.7*np.log(r+.15)+i*TAU/3+self.phase),0],inc) for r in rs])
        return self


def passing_orbit():
    """A bound Kepler ellipse with the mass at a focus, rather than its center."""
    a=2.;e=.65;center=np.array([0.,1.,0.])
    return ParametricFunction(lambda q:center+np.array([a*(np.cos(q)-e),a*np.sqrt(1-e*e)*np.sin(q),0]),
                              t_range=[PI,PI+TAU],color=OBS,stroke_width=2)


class FlatGalaxyDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def construct(self):
        self.brand=txt('과학의 한 장면  /  09',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('중력은 당기는데, 은하는 왜 납작할까?', '중력은 모든 방향에서 중심으로 당깁니다.\n그런데 왜 많은 은하는 납작한 원반일까요?')
        sphere=matter_sphere(2,(0,1,0),36,OBS);self.add(sphere)
        arrows=VGroup(*[Arrow([2*np.cos(a),1+2*np.sin(a),0],[1.45*np.cos(a),1+1.45*np.sin(a),0],
                             buff=0,color=MASS,stroke_width=2) for a in np.linspace(0,TAU,9)[:-1]])
        self.beat(.25,Create(arrows));self.add(txt('모든 방향의 중력 → 납작한 은하?',-2.4,30,MASS));self.finish()

        self.cue('회전 없는 이상적인 초기 붕괴', '회전과 압력을 무시하면,\n물질은 중심을 향해 거의 곧장 떨어집니다.')
        sphere=matter_sphere(2.1,(0,1,0),36,OBS);self.add(sphere)
        self.beat(.55,sphere.animate.scale(.22),rate_func=linear)
        self.add(txt('처음의 붕괴 방향: 거의 방사형',-1.4,30,OBS),txt('회전·압력을 무시한 초기 운동의 예',-3.2,23,'#A9B8CB'));self.finish()

        self.cue('실제로는 작은 회전이 있다', '작은 회전과 비대칭이 있는 물질은\n각운동량을 가지고 있습니다.')
        r=ValueTracker(2.1);h=ValueTracker(2.1);cloud=RotatingCloud(r,h);self.add(cloud)
        self.beat(.2,FadeIn(txt('Angular Momentum',-2.1,34,MASS)))
        self.add(txt('처음의 느린 회전',-3.3,28,OBS));self.finish()

        self.cue('수축할수록 회전은 빨라진다', '큰 외부 토크가 없다면 각운동량은 보존됩니다.\n반지름이 줄어들면 회전 속도는 커집니다.')
        r=ValueTracker(2.1);h=ValueTracker(2.1);cloud=RotatingCloud(r,h);self.add(cloud)
        self.add(equation('L ≈ m r vφ',-2.0,MASS,40))
        self.beat(.54,r.animate.set_value(1.05),h.animate.set_value(1.05),rate_func=linear)
        self.add(txt('r ½ → vφ 2배 → 회전은 더 빠르게',-3.1,29,OBS),txt('L 유지 · r은 회전축까지의 거리',-4.15,22,'#A9B8CB'));self.finish()

        self.cue('옆방향 속도가 있으면, 중심을 비껴간다', '중심으로 곧장 떨어지는 대신,\n중심을 비껴 도는 궤도로 움직일 수 있습니다.')
        path=passing_orbit();dot=Dot(path.get_start(),radius=.07,color=OBS)
        self.add(Dot([0,1,0],radius=.11,color=MASS),dot,txt('중력 중심',-1.1,25,MASS))
        self.beat(.54,Create(path),MoveAlongPath(dot,path),rate_func=linear)
        self.add(txt('회전은 중심으로의 직행을 어렵게 한다',-2.9,28,OBS),txt('비껴가는 궤도의 예 · 냉각 전에는 원 궤도가 아닐 수도 있음',-4.1,21,'#A9B8CB'));self.finish()

        self.cue('회전만으로 얇아지지는 않는다', '위아래 운동과 열적 지지가 있으면,\n회전하는 구조도 여전히 두껍습니다.')
        r=ValueTracker(2.1);h=ValueTracker(1.6);cloud=RotatingCloud(r,h,PI/2,'vertical');self.add(cloud)
        self.add(txt('옆에서 본 회전 구름',-1.1,25,OBS))
        self.beat(.17,FadeIn(DoubleArrow([2.6,-.6,0],[2.6,2.6,0],buff=0,color=EXPECT)))
        self.add(txt('아직 큰 두께',-2.4,31,EXPECT),txt('회전과 수직 무작위 운동은 서로 다릅니다.',-3.8,23,'#A9B8CB'));self.finish()

        self.cue('충돌 → 열 → 빛으로 냉각', '가스 충돌은 운동을 열로 바꾸고,\n그 열을 빛으로 방출하면 가스가 식습니다.')
        top=Circle(radius=.32,color=OBS,fill_color=OBS,fill_opacity=.4).move_to([0,2.8,0])
        bottom=top.copy().move_to([0,-.8,0]);self.add(top,bottom)
        self.beat(.2,top.animate.move_to([0,1.32,0]),bottom.animate.move_to([0,.68,0]),rate_func=linear)
        heat=VGroup(*[Circle(radius=r,color=EXPECT,stroke_opacity=.2,fill_color=EXPECT,fill_opacity=.05).move_to([0,1,0]) for r in [.5,.7,.9]])
        self.beat(.12,FadeIn(heat),top.animate.set_color(EXPECT),bottom.animate.set_color(EXPECT))
        phase=txt('운동 → 열',-1.0,30,EXPECT);self.add(phase)
        photons=VGroup(*[Dot([0,1,0],radius=.045,color=LIGHT) for _ in range(8)]);self.add(photons)
        self.beat(.22,*[p.animate.shift(np.array([np.cos(a),np.sin(a),0])*2.2) for p,a in zip(photons,np.linspace(0,TAU,9)[:-1])],
                  FadeOut(heat),top.animate.set_color(OBS),bottom.animate.set_color(OBS))
        self.beat(.12,Transform(phase,txt('열 → 빛 방출 → 냉각',-1.5,30,OBS)))
        self.add(txt('무작위 운동·열적 지지 감소',-2.7,29,OBS),equation('vz ↓',-3.85,OBS,39));self.finish()

        self.cue('에너지는 빠져나가도, 회전은 남는다', '전체적인 회전의 각운동량은 대체로 남습니다.\n냉각은 회전까지 지우는 과정이 아닙니다.')
        r=ValueTracker(2.1);h=ValueTracker(1.2);cloud=RotatingCloud(r,h,PI/3);self.add(cloud)
        self.beat(.52,h.animate.set_value(.4),rate_func=linear)
        self.add(txt('무작위 운동 ↓',-1.7,30,OBS),txt('순각운동량은 대체로 유지',-2.85,30,MASS),
                 txt('외부 토크·강한 유출을 무시한 설명',-4.1,22,'#A9B8CB'));self.finish()

        self.cue('같은 평면 가까이, 얇은 원반으로', '위아래 운동은 줄고, 회전은 남으면서\n가스가 한 평면 가까이에 모입니다.')
        r=ValueTracker(2.1);h=ValueTracker(1.5);cloud=RotatingCloud(r,h,PI/2);self.add(cloud)
        self.beat(.59,h.animate.set_value(.16),rate_func=linear)
        self.add(txt('옆면: 두께 감소 · 회전은 계속',-1.35,29,OBS),txt('가스의 냉각이 얇게 만든다',-2.75,33,MASS),
                 txt('원반은 유한한 두께를 가집니다.',-4.05,23,'#A9B8CB'));self.finish()

        self.cue('세 가지 역할은 다릅니다', '중력은 수축, 각운동량은 중심 직행을 방해,\n가스의 충돌과 냉각은 두께를 줄입니다.')
        rows=[('중력','구름을 수축',2.6,MASS),('각운동량','중심으로 곧장 떨어지기 어렵게',.5,LIGHT),('충돌과 냉각','가스의 두께 감소',-1.6,OBS)]
        for name,meaning,y,color in rows:
            self.beat(.16,FadeIn(txt(name,y,32,color)),FadeIn(txt('→ '+meaning,y-.75,27,color)))
        self.add(txt('가스 원반에서 별이 태어나면 별 원반으로 이어집니다.',-4.05,22,'#A9B8CB'));self.finish()

        self.cue('정면과 옆면, 같은 3차원 은하', '중심은 두껍고, 바깥은 얇은 별 원반.\n같은 은하를 다른 방향에서 본 모습입니다.')
        view=ValueTracker(0);galaxy=GalaxyView(view);self.add(galaxy)
        label=txt('정면',-1.8,29,OBS);self.add(label)
        self.beat(.13,FadeIn(txt('동일한 3D 은하 · 시점만 90° 회전',-3.0,24,'#A9B8CB')))
        self.beat(.4,view.animate.set_value(PI/2),rate_func=smooth)
        self.beat(.1,Transform(label,txt('옆면: 얇은 원반 + 두꺼운 중심부',-1.8,28,OBS)))
        self.add(txt('Gravity + Angular Momentum + Cooling',-4.1,25,MASS))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        for m in self.mobjects:m.clear_updaters()
        self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)]);self.finish()
