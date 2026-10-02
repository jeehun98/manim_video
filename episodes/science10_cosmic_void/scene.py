"""Conserved illustrative particles: low density -> walls -> cosmic web."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.spatial import Voronoi
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT, OBS, MASS, EXPECT
from episodes.science04_virial_theorem.scene import equation
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

CENTER = np.array([0., 1., 0.])

def geometry():
    rng = np.random.default_rng(101)
    seeds = np.array([[x, y] for x in np.arange(-6, 7, 3) for y in np.arange(-6, 7, 3)], dtype=float)
    seeds += rng.uniform(-.55, .55, seeds.shape)
    seeds[12] = 0
    vor = Voronoi(seeds)
    polygon = vor.vertices[vor.regions[vor.point_region[12]]]
    return vor, polygon

VOR, POLYGON = geometry()

def nearest_edge(p, polygon=POLYGON):
    candidates = []
    for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
        q = a + np.clip(np.dot(p-a, b-a)/np.dot(b-a, b-a), 0, 1)*(b-a)
        candidates.append(q)
    return min(candidates, key=lambda q: np.linalg.norm(q-p))

class VoidPatch(VGroup):
    """Geometric illustration; every matter marker survives the transition."""
    def __init__(self, progress, scale=1.5, center=CENTER):
        super().__init__()
        self.progress = progress; self.scale_factor = scale; self.origin = np.asarray(center)
        rng = np.random.default_rng(102)
        # Points inside a convex Voronoi cell, with a slight central deficit.
        candidates = rng.uniform(POLYGON.min(axis=0), POLYGON.max(axis=0), (400, 2))
        edges = np.roll(POLYGON, -1, axis=0)-POLYGON
        relative = candidates[:, None, :]-POLYGON[None, :, :]
        crosses = edges[None,:,0]*relative[:,:,1]-edges[None,:,1]*relative[:,:,0]
        mask = np.all(crosses>=0,axis=1)|np.all(crosses<=0,axis=1)
        points = candidates[mask][:88]
        points[:4] = np.array([[.15,.23],[-.3,-.2],[.4,-.4],[-.15,.55]])
        for i in range(4, len(points)):
            if np.linalg.norm(points[i]) < .75: points[i] *= 1.13
        self.initial = points
        targets = np.array([nearest_edge(p) for p in points])
        targets[:4] = points[:4] * 1.15
        targets[4:] += rng.normal(0, .035, targets[4:].shape)
        self.targets = targets
        self.dots = VGroup(*[Dot(radius=.032, color=LIGHT) for _ in points])
        self.add(self.dots); self.motion(); self.add_updater(lambda m: m.motion())

    def position(self, p): return self.origin + self.scale_factor*np.array([p[0],p[1],0.])
    def motion(self):
        t = self.progress.get_value()
        for i, dot in enumerate(self.dots):
            dot.move_to(self.position((1-t)*self.initial[i]+t*self.targets[i]))
        return self
    def walls(self):
        return Polygon(*[self.position(p) for p in POLYGON], color=OBS, stroke_width=2.2, stroke_opacity=.6)
    def nodes(self):
        return VGroup(*[VGroup(Circle(radius=.13,fill_color=MASS,fill_opacity=.16,stroke_width=0),
                              Dot(radius=.045,color=LIGHT)).move_to(self.position(p)) for p in POLYGON])

def sample(count, center, color):
    return VGroup(*[Dot(np.array(center)+np.array([((i%4)-1.5)*.5,((i//4)-1)*.5,0]),radius=.06,color=color)
                    for i in range(count)])

def web():
    """A 2D conceptual slice, clipped to the visual stage; no outer cosmic edge."""
    lines = VGroup(); dots = VGroup(); rng = np.random.default_rng(103)
    def clip(a,b):
        t0,t1=0.,1.;d=b-a
        for axis,lo,hi in [(0,-4.7,4.7),(1,-3.6,3.6)]:
            if abs(d[axis]) < 1e-9:
                if not lo <= a[axis] <= hi:return None
            else:
                u,v=sorted([(lo-a[axis])/d[axis],(hi-a[axis])/d[axis]])
                t0=max(t0,u);t1=min(t1,v)
                if t0>t1:return None
        return a+t0*d,a+t1*d
    for edge in VOR.ridge_vertices:
        if -1 in edge:continue
        segment=clip(*VOR.vertices[edge])
        if segment is None:continue
        a,b=segment
        def pos(p):return CENTER+np.array([p[0]*.78,p[1]*.78,0.])
        lines.add(Line(pos(a),pos(b),color=OBS,stroke_width=1.5,stroke_opacity=.4))
        for t in np.linspace(0,1,max(3,int(np.linalg.norm(b-a)*10))):
            q=(1-t)*a+t*b+rng.normal(0,.04,2)
            dots.add(Dot(pos(q),radius=.026,color=LIGHT))
    for p in VOR.vertices:
        if abs(p[0])<4.7 and abs(p[1])<3.6:
            dots.add(Dot(CENTER+np.r_[p*.78,0],radius=.065,color=LIGHT))
    dots.add(Dot([.1,1.15,0],radius=.02,color=MASS),Dot([-1,2,0],radius=.02,color=MASS))
    return VGroup(lines,dots)

class CosmicVoidDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def construct(self):
        self.brand=txt('과학의 한 장면  /  10',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('우주에는 왜 거대한 빈 공간이 생길까?', '거의 균일한 초기 우주에도\n아주 조금 성긴 곳이 있었습니다.')
        p=ValueTracker(0);patch=VoidPatch(p);self.add(patch)
        self.beat(.2,Create(DashedVMobject(Circle(radius=1.05,color=MASS).move_to(CENTER),num_dashes=24)))
        self.add(txt('처음의 작은 밀도 차이',-2.8,31,MASS));self.finish()

        self.cue('처음에는, 한두 개의 차이', '평균보다 조금 적은 물질.\n작지만 중요한 차이입니다.')
        left=sample(12,[-2,1.2,0],OBS);right=sample(11,[2,1.2,0],MASS)
        self.beat(.25,FadeIn(left),FadeIn(right))
        self.add(txt('평균 밀도',-.8,28,OBS,width=3).shift(LEFT*2),txt('조금 낮은 밀도',-.8,28,MASS,width=3).shift(RIGHT*2),
                 equation('δ < 0',-2.5,MASS,48),txt('δ : 평균 대비 밀도 차이',-3.8,24));self.finish()

        self.cue('팽창은 덜 늦추고, 주변은 당긴다', '저밀도 영역은 팽창을 덜 감속시킵니다.\n주변의 조밀한 곳은 물질을 끌어당깁니다.')
        p=ValueTracker(.08);patch=VoidPatch(p);nodes=patch.nodes();self.add(patch,nodes)
        arrows=VGroup()
        for i in [9,19,35,53]:
            point=patch.dots[i].get_center();target=patch.position(min(POLYGON,key=lambda q:np.linalg.norm(q-patch.initial[i])))
            arrows.add(Arrow(point,point+(target-point)*.6,buff=.07,color=MASS,stroke_width=2))
        self.beat(.25,Create(arrows));self.add(txt('조밀한 곳을 향한 중력',-2.9,30,MASS),txt('빈 공간이 밀어내는 힘은 없습니다.',-4,26));self.finish()

        self.cue('물질 일부가 주변으로 이동한다', '우주가 팽창하는 동안, 물질 일부는\n주변의 더 조밀한 곳으로 이동합니다.')
        p=ValueTracker(.08);patch=VoidPatch(p);self.add(patch,patch.nodes())
        self.beat(.65,p.animate.set_value(.85),rate_func=smooth)
        self.add(txt('사라지는 점 없이, 위치가 바뀝니다.',-3.3,27,OBS));self.finish()

        self.cue('조금 비었던 곳이, 더 비어진다', '평균에 비해 더 성겨지면서\n처음의 작은 차이가 커집니다.')
        a=VoidPatch(ValueTracker(0),.65,[-2,1.7,0]);b=VoidPatch(ValueTracker(.98),.65,[2,1.7,0]);self.add(a,b)
        self.add(txt('처음',-.15,28).shift(LEFT*2),txt('나중',-.15,28,MASS).shift(RIGHT*2))
        for fraction,label,y in [(.16,'조금 낮은 밀도',-1.6),(.16,'물질이 주변으로 이동',-2.6),(.16,'더 낮은 상대 밀도',-3.6)]:
            self.beat(fraction,FadeIn(txt(label,y,29,MASS)))
        self.finish()

        self.cue('구조와 빈 공간이 함께 성장한다', '같은 중력이 물질을 모으는 동안,\n빈 공간도 더 선명해집니다.')
        left=sample(20,[-2,1.5,0],OBS);p=ValueTracker(0);right=VoidPatch(p,.65,[2,1.5,0]);self.add(left,right)
        self.add(equation('δ > 0',-.6,OBS,37).shift(LEFT*2),equation('δ < 0',-.6,MASS,37).shift(RIGHT*2))
        self.beat(.6,left.animate.scale(.35),p.animate.set_value(1),rate_func=smooth)
        self.add(txt('더 조밀하게',-2.1,28,OBS,width=3).shift(LEFT*2),txt('더 비어 있게',-2.1,28,MASS,width=3).shift(RIGHT*2),
                 txt('중력은 작은 차이를 키웁니다.',-3.6,31,LIGHT));self.finish()

        self.cue('밀도 차이는 두 방향으로 벌어진다', '많은 곳은 더 조밀해지고,\n적은 곳은 상대적으로 더 비어갑니다.')
        axes=Axes(x_range=[0,1,.2],y_range=[-1,1.5,.5],x_length=6.3,y_length=4.1,
                  axis_config={'include_ticks':False,'color':'#A9B8CB'}).move_to([0,.8,0]);self.add(axes)
        self.add(txt('평균 대비 밀도 차이 δ',3.6,26),txt('시간',-1.9,24),txt('δ = 0 · 평균',.65,23).shift(LEFT*2.3))
        upper=axes.plot(lambda t:.035+.19*(np.exp(2*t)-1),x_range=[0,1],color=OBS)
        lower=axes.plot(lambda t:-1+.965*np.exp(-1.7*t),x_range=[0,1],color=MASS)
        self.beat(.6,Create(upper),Create(lower),rate_func=linear)
        self.add(txt('과밀',3,25,OBS).shift(RIGHT*2.7),txt('저밀',-.5,25,MASS).shift(RIGHT*2.7),
                 txt('δ ≥ −1 · 밀도는 0보다 작아질 수 없습니다.',-3.15,24),txt('성장 방향을 보여주는 개념 그래프',-4.1,21,'#9BA9C3'));self.finish()

        self.cue('물질은 벽과 필라멘트로 이어진다', '물질은 사라지지 않고 경계에 모입니다.\n교차점에서는 더 큰 구조가 자랍니다.')
        p=ValueTracker(.85);patch=VoidPatch(p);self.add(patch)
        self.beat(.33,p.animate.set_value(1),Create(patch.walls()))
        self.beat(.2,FadeIn(patch.nodes()))
        self.add(txt('Void',1.1,36,MASS),txt('Wall / Filament',-2.6,31,OBS),txt('물질 분포의 단면 · 개념도',-3.8,22,'#9BA9C3'));self.finish()

        self.cue('더 멀리서 보면, 우주 거미줄', '은하가 드문 거대한 저밀도 영역,\nCosmic Void. 완전히 비어 있지는 않습니다.')
        p=ValueTracker(1);patch=VoidPatch(p);patch.clear_updaters();central=VGroup(patch,patch.walls(),patch.nodes());self.add(central)
        self.beat(.3,central.animate.scale(.78/1.5,about_point=CENTER))
        network=web();self.beat(.25,FadeOut(central),FadeIn(network))
        self.add(txt('Cosmic Void',1.15,28,MASS),txt('은하가 드문 영역 · 물질은 일부 남습니다.',-3.2,25),
                 txt('우주 거미줄의 단면을 단순화한 그림',-4.1,22,'#9BA9C3'));self.finish()

        self.cue('빈 공간도 함께 성장한다', '조금 덜 조밀했던 차이가 커진 결과.\n물질이 모이는 동안, 빈 공간도 성장합니다.')
        network=web();self.add(network)
        self.beat(.18,FadeIn(txt('Cosmic Void',1.15,34,MASS)))
        self.beat(.18,FadeIn(txt('조금 비었던 곳이 더 비어간다',-3.2,34,LIGHT)))
        self.add(txt('작은 차이 → 구조와 빈 공간',-4.2,27,OBS));self.finish()
