"""A small relative density contrast grows into a halo and a luminous galaxy."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT, OBS, MASS, EXPECT
from episodes.science04_virial_theorem.scene import equation, MovingCluster
from episodes.science06_turnaround.scene import grid, region
from episodes.science07_half_radius.scene import HalfRadiusDiscovery


THETA = np.linspace(.25, 2*np.pi-.001, 1600)
TIMES = (THETA-np.sin(THETA))/(2*np.pi)
DELTA_C = (3/5)*(3*np.pi/2)**(2/3)


def radius(angle):
    return (1-np.cos(angle))/2


def background_radius(angle):
    return 6**(2/3)/4*(angle-np.sin(angle))**(2/3)


def delta_nl(angle):
    return 4.5*(angle-np.sin(angle))**2/(1-np.cos(angle))**3-1


def delta_linear(angle):
    return .6*(.75*(angle-np.sin(angle)))**(2/3)


def matter_sphere(r=1.3, center=(0, 1, 0), count=30, color=LIGHT):
    rng = np.random.default_rng(8)
    points = rng.normal(size=(count, 3))
    points /= np.linalg.norm(points, axis=1)[:, None]
    points *= rng.uniform(.05, .9, (count, 1))**(1/3)
    c = np.asarray(center)
    return VGroup(Circle(radius=r, color=color, stroke_opacity=.5).move_to(c),
                  *[Dot(c+r*np.array([p[0], p[1], 0]), radius=.04, color=color) for p in points])


def initial_patch():
    dots = VGroup()
    for x in np.linspace(-3.4, 3.4, 9):
        for y in np.linspace(-1.8, 3.8, 8):
            p = np.array([x, y, 0])
            if np.linalg.norm(p-np.array([0, 1, 0])) < 1.5:
                p = np.array([0, 1, 0])+.94*(p-np.array([0, 1, 0]))
            dots.add(Dot(p, radius=.035, color=LIGHT))
    return dots


def contrast_definition():
    rho = Text('ρ', font='Cambria', font_size=37, color=OBS)
    bar = Line(rho.get_corner(UL)+UP*.06, rho.get_corner(UR)+UP*.06, color=OBS, stroke_width=1.5)
    mean = VGroup(rho, bar)
    numerator = VGroup(Text('ρ −', font='Cambria', font_size=37, color=OBS), mean.copy()).arrange(RIGHT, buff=.16)
    denominator = mean.copy()
    fraction = VGroup(numerator.move_to([0, .42, 0]), denominator.move_to([0, -.42, 0]),
                      Line([-1, 0, 0], [1, 0, 0], color=OBS, stroke_width=2))
    left = Text('δ =', font='Cambria', font_size=43, color=OBS).next_to(fraction, LEFT, buff=.27)
    return VGroup(left, fraction).move_to([0, -2.4, 0])


def densities(angle):
    """Both absolute densities decrease on the expanding part; their ratio grows."""
    mean = (background_radius(1.5)/background_radius(angle))**3
    local = (1+delta_nl(1.5))*(radius(1.5)/radius(angle))**3
    return mean, local


def density_bars(angle):
    mean, local = densities(angle)
    g = VGroup()
    for density, y, name, color in [(mean, 1.8, '평균 밀도', OBS),
                                  (local, .5, '지역 밀도', LIGHT)]:
        width = 1.8*density
        g.add(Rectangle(width=width, height=.28, stroke_width=0, fill_color=color, fill_opacity=.85).move_to([-1.35+width/2, y, 0]),
              txt(name, y, 25, color, width=1.7).shift(LEFT*2.8))
    return g


def halo(center=(0, .9, 0), r=2.55):
    glow = VGroup(*[Circle(radius=r*f, stroke_width=0, fill_color=MASS, fill_opacity=.018).move_to(center)
                    for f in np.linspace(1, .22, 10)])
    tracers = MovingCluster(center=center, radius=r, speed=.38)
    tracers.dots.set_color(MASS).set_opacity(.5)
    return VGroup(glow, tracers)


def threshold_label(y, size=38):
    symbol = Text('δ', font='Cambria', font_size=size, color=OBS)
    sub = Text('c', font='Cambria', font_size=size*.56, color=OBS).next_to(symbol, RIGHT, buff=.025).shift(DOWN*.15)
    rest = Text('≈ 1.686', font='Cambria', font_size=size, color=OBS)
    return VGroup(VGroup(symbol, sub), rest).arrange(RIGHT, buff=.16, aligned_edge=UP).move_to([0, y, 0])


class CoolingGas(VGroup):
    """Illustrative gas settling, with angular motion and shrinking thickness."""
    def __init__(self, progress, center=(0, .9, 0)):
        super().__init__()
        self.progress = progress
        self.center = np.array(center)
        self.elapsed = 0.
        rng = np.random.default_rng(82)
        self.radii = rng.uniform(.1, 1, 42)**.55
        self.phases = rng.uniform(0, TAU, 42)
        self.dots = VGroup(*[Dot(radius=.045, color=OBS).set_opacity(.75) for _ in self.radii])
        self.outline = Ellipse(width=4.2, height=3.7, color=OBS, stroke_opacity=.2)
        self.add(self.outline, self.dots)
        self.motion(0)
        self.add_updater(lambda m, dt: m.motion(dt))

    def motion(self, dt):
        self.elapsed += dt
        f = self.progress.get_value()
        scale = 2.1-.4*f
        thin = .88-.53*f
        self.outline.stretch_to_fit_width(2*scale).stretch_to_fit_height(2*scale*thin).move_to(self.center)
        for i, dot in enumerate(self.dots):
            angle = self.phases[i]+self.elapsed*(.24+.23*f)
            dot.move_to(self.center+scale*self.radii[i]*np.array([np.cos(angle), thin*np.sin(angle), 0]))
        return self


class SpiralGalaxy(VGroup):
    """Tilted luminous disk inside a distinct, spherical dark-matter halo."""
    def __init__(self, center=(0, .9, 0)):
        super().__init__()
        self.center = np.array(center)
        self.phase = 0.
        rng = np.random.default_rng(83)
        self.radii = rng.uniform(.1, 1, 100)**.65*1.85
        self.angles = 1.7*np.log(self.radii+.15)+rng.integers(0, 3, 100)*TAU/3+rng.normal(0, .2, 100)
        self.stars = VGroup(*[Dot(radius=rng.uniform(.024, .047), color=LIGHT) for _ in self.radii])
        self.arms = VGroup(*[VMobject(color=OBS, stroke_width=2.5, stroke_opacity=.55) for _ in range(3)])
        self.core = VGroup(*[Ellipse(width=w, height=w*.48, stroke_width=0, fill_color=LIGHT,
                                    fill_opacity=.08+.05*i).move_to(center) for i, w in enumerate([1, .7, .45, .23])],
                           Dot(center, radius=.07, color=LIGHT))
        self.add(self.arms, self.stars, self.core)
        self.motion(0)
        self.add_updater(lambda m, dt: m.motion(dt))

    def position(self, r, angle):
        return self.center+r*np.array([np.cos(angle), .38*np.sin(angle), 0])

    def motion(self, dt):
        self.phase += dt*.13
        for dot, r, a in zip(self.stars, self.radii, self.angles):
            dot.move_to(self.position(r, a+self.phase))
        for i, arm in enumerate(self.arms):
            rs = np.linspace(.18, 1.95, 60)
            arm.set_points_as_corners([self.position(r, 1.7*np.log(r+.15)+i*TAU/3+self.phase) for r in rs])
        return self


class DensityGrowthDiscovery(HalfRadiusDiscovery):
    TIMING = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION = TIMING['duration']

    def beat(self, fraction, *animations, **kwargs):
        frames = max(1, round(self.span_frames*fraction))
        duration = frames/30-(1e-6 if frames > 1 else 0)
        self.play(*animations, run_time=duration, **kwargs)

    def to(self, frame):
        remaining = frame-round(self.time*30)
        if remaining < 0:
            raise RuntimeError(f'Cue overrun at {self.time}: target {frame/30}')
        if remaining:
            # Frozen waits truncate epsilon-short durations; dynamic waits use ceil.
            # Use one sampling path for both still and moving illustrations.
            duration = remaining/30-(1e-6 if remaining > 1 else 0)
            self.wait(duration, frozen_frame=False)

    def growth_graph(self, cutoff=5.5):
        axes = Axes(x_range=[0, 1, .25], y_range=[0, cutoff, 1], x_length=6.4, y_length=3.65,
                    axis_config={'include_ticks': False, 'color': '#A9B8CB'}).move_to([0, .45, 0])
        keep = delta_nl(THETA) < cutoff-.3
        actual = VMobject(color=LIGHT, stroke_width=3).set_points_as_corners([
            axes.c2p(t, d) for t, d in zip(TIMES[keep], delta_nl(THETA[keep]))])
        linear = VMobject(color=OBS, stroke_width=2.7).set_points_as_corners([
            axes.c2p(t, d) for t, d in zip(TIMES, delta_linear(THETA))])
        self.add(axes, txt('평균 대비 밀도 차이 δ', 3.3, 27, LIGHT), txt('시간', -2, 24))
        return axes, actual, DashedVMobject(linear, num_dashes=36), keep

    def construct(self):
        self.brand = txt('과학의 한 장면  /  08', 7.1, 23, '#9BA9C3')
        self.add(self.brand)
        self.cue('작은 밀도 차이는 어떻게 은하가 될까?', '초기 우주는 거의 균일했습니다.\n하지만 완전히 똑같지는 않았습니다.')
        patch = initial_patch()
        self.beat(.28, FadeIn(patch))
        self.beat(.2, Create(Circle(radius=1.5, color=MASS, stroke_opacity=.55).move_to([0, 1, 0])))
        self.add(txt('아주 작은 차이 · 그림에서는 과장', -3.5, 24, '#A9B8CB'))
        self.finish()

        self.cue('평균과 비교한, 상대적인 밀도 차이', '어떤 영역은 주변보다\n조금 더 많은 물질을 가지고 있었습니다.')
        self.beat(.18, FadeIn(matter_sphere(1.3, (-2, 1.6, 0), 10, OBS)),
                  FadeIn(matter_sphere(1.3, (2, 1.6, 0), 11)))
        self.add(txt('10개', -.35, 25, OBS).shift(LEFT*2), txt('11개', -.35, 25, LIGHT).shift(RIGHT*2),
                 txt('같은 크기의 영역 · 이해를 위한 비교 예시', -1.2, 22, '#A9B8CB'))
        self.beat(.16, FadeIn(contrast_definition()))
        self.add(txt('Density Contrast', -3.8, 28, MASS))
        self.finish()

        self.cue('작은 질량 차이, 작은 중력 차이', '같은 크기라도 질량이 더 많은 곳은,\n중력도 조금 더 강합니다.')
        for x, color, length, count in [(-2, OBS, .19, 10), (2, LIGHT, .25, 11)]:
            self.add(matter_sphere(1.25, (x, 1.2, 0), count, color))
            for a in np.linspace(0, TAU, 5)[:-1]:
                v = np.array([np.cos(a), np.sin(a), 0]);p = np.array([x, 1.2, 0])+v*1.25
                self.beat(.045, GrowArrow(Arrow(p, p-v*length, buff=0, color=MASS, stroke_width=2)))
        self.add(txt('평균 영역', -.6, 25, OBS).shift(LEFT*2), txt('과밀 영역', -.6, 25, LIGHT).shift(RIGHT*2),
                 txt('처음의 차이는 아주 작습니다.', -2.3, 29, MASS))
        self.finish()

        self.cue('둘 다 커지지만, 같은 속도는 아니다', '조밀한 영역은 주변보다 덜 팽창합니다.\n그 차이가 시간이 지나며 벌어집니다.')
        angle = ValueTracker(1.2)
        mean = always_redraw(lambda: matter_sphere(1.1*background_radius(angle.get_value()), (-2, 1.4, 0), 30, OBS))
        local = always_redraw(lambda: matter_sphere(1.1*radius(angle.get_value()), (2, 1.4, 0)))
        self.add(mean, local, txt('평균 팽창', -.5, 25, OBS).shift(LEFT*2), txt('조금 덜 팽창', -.5, 25, LIGHT).shift(RIGHT*2))
        self.beat(.56, angle.animate.set_value(2.4), rate_func=linear)
        self.add(txt('모두 팽창 중 · 상대적인 차이는 증가', -2.8, 29, MASS))
        self.finish()

        self.cue('밀도 자체보다, 평균과의 차이', '팽창 중 두 밀도가 모두 낮아져도,\n평균에 비한 밀도 차이는 커질 수 있습니다.')
        angle = ValueTracker(1.5)
        self.add(always_redraw(lambda: density_bars(angle.get_value())))
        number = DecimalNumber(delta_nl(1.5), mob_class=Text, num_decimal_places=2, font_size=39, color=MASS).move_to([.8, -1.5, 0])
        number.add_updater(lambda m: m.set_value(delta_nl(angle.get_value())).move_to([.8, -1.5, 0]))
        self.add(number, equation('δ =', -1.5, MASS, 39).shift(LEFT*.8), txt('평균 대비 밀도 차이', -2.55, 28, MASS))
        self.beat(.6, angle.animate.set_value(2.5), rate_func=linear)
        self.add(txt('막대는 절대 밀도 · δ는 상대적인 차이', -3.9, 22, '#A9B8CB'))
        self.finish()

        self.cue('작은 차이가, 스스로 증폭된다', '더 조밀해서 덜 퍼지고, 덜 퍼져서\n평균에 비해 더 조밀해집니다.')
        nodes = [txt('평균 대비\n밀도 ↑', 3.2, 29, LIGHT, 2.5), txt('더 강한\n중력', 1.25, 29, MASS, 2.4).shift(RIGHT*2.3),
                 txt('평균보다\n덜 팽창', -.8, 29, OBS, 2.5), txt('상대적인\n차이 확대', 1.25, 29, LIGHT, 2.5).shift(LEFT*2.3)]
        endpoints = [([.9, 3.05, 0], [1.65, 2.1, 0]), ([2.15, .55, 0], [.9, -.7, 0]),
                     ([-.9, -.7, 0], [-2.15, .55, 0]), ([-1.65, 2.1, 0], [-.9, 3.05, 0])]
        arrows = [CurvedArrow(a, b, angle=-.35, color=MASS, stroke_width=2) for a, b in endpoints]
        for node, arrow in zip(nodes, arrows):
            self.beat(.07, FadeIn(node), Create(arrow))
        tracer = Dot(arrows[0].get_start(), radius=.08, color=LIGHT);self.add(tracer)
        for arrow in arrows:
            tracer.move_to(arrow.get_start());self.beat(.07, MoveAlongPath(tracer, arrow), rate_func=linear)
        self.add(txt('중력이 밀도 차이를 증폭한다', -3.1, 30, MASS))
        self.finish()

        self.cue('이제, 작은 요동의 계산을 벗어난다', '처음에는 선형 이론이 잘 맞지만,\n차이가 커지면 비선형 변화가 중요해집니다.')
        angle = ValueTracker(.25)
        axes = Axes(x_range=[0, .35, .1], y_range=[0, 3, 1], x_length=6.3, y_length=3.5,
                    axis_config={'include_ticks': False, 'color': '#A9B8CB'}).move_to([0, .65, 0])
        curve = always_redraw(lambda: VMobject(color=LIGHT, stroke_width=3).set_points_as_corners([
            axes.c2p((a-np.sin(a))/(2*np.pi), delta_nl(a)) for a in np.linspace(.25, angle.get_value()+.001, 100)]))
        self.add(axes, curve, txt('평균 대비 밀도 차이 δ', 3.4, 25, LIGHT), txt('시간', -1.65, 23))
        small = equation('δ ≪ 1', -2.8, OBS, 43);self.add(small)
        self.beat(.46, angle.animate.set_value(2.5), rate_func=linear)
        self.beat(.13, Transform(small, equation('δ ∼ 1', -2.8, LIGHT, 43)))
        self.add(txt('1에 가까워지면 작은 차이의 근사가 어려워집니다.', -4.1, 22, '#A9B8CB'))
        self.finish()

        self.cue('충분히 성장한 영역은, 붕괴로', '최대 팽창을 지나 수축하는 동안에도,\n주변 우주는 계속 팽창합니다.')
        angle = ValueTracker(2.2);spacing = ValueTracker(1)
        self.add(always_redraw(lambda: grid(spacing.get_value(), .16)),
                 always_redraw(lambda: region(2*radius(angle.get_value()), motion=np.sin(angle.get_value())*.4)))
        self.beat(.6, angle.animate.set_value(4.9), spacing.animate.set_value(1.65), rate_func=linear)
        self.add(txt('Overdensity → Collapse', -2.7, 31, MASS), txt('충분히 성장하여 붕괴하는 한 영역의 예', -3.8, 22, '#A9B8CB'))
        self.finish()

        self.cue('붕괴 시점을, 선형 이론으로 연장하면', '이상화된 붕괴가 끝나는 시점에,\n선형 이론의 연장은 약 1.686에 도달합니다.')
        axes, actual, linear_curve, keep = self.growth_graph()
        self.beat(.36, Create(actual), Create(linear_curve))
        end = actual.get_end()
        self.add(Arrow(end, end+UP*.32, color=LIGHT, buff=0), txt('실제 비선형 변화', 2.6, 22, LIGHT).shift(LEFT*1.9))
        line = DashedLine(axes.c2p(1, 0), axes.c2p(1, 5.5), color=MASS, stroke_width=1.4)
        point = Dot(axes.c2p(1, DELTA_C), radius=.06, color=OBS)
        self.beat(.12, Create(line), FadeIn(point))
        self.add(txt('선형 이론의 연장', -.98, 22, OBS).shift(RIGHT*.6),
                 txt('붕괴 완료 시점', -2.55, 22, MASS).shift(RIGHT*2.35), threshold_label(-3.45),
                 txt('물질 우세 구형 모형 · 최대 팽창 시점과는 다름', -4.4, 21, '#A9B8CB'))
        self.finish()

        self.cue('실제 밀도 배수가 아닙니다', '실제 밀도도, 실제 밀도 차이도 아닙니다.\n선형 이론을 붕괴 시점까지 연장한 기준입니다.')
        wrong = txt('실제 밀도 = 평균 밀도 × 1.686', 2.45, 30)
        self.add(wrong)
        self.beat(.2, Create(Line([-3.45, 2.05, 0], [3.45, 2.85, 0], color=EXPECT, stroke_width=4)),
                  Create(Line([-3.45, 2.85, 0], [3.45, 2.05, 0], color=EXPECT, stroke_width=4)))
        self.beat(.16, FadeIn(threshold_label(.45, 43)), FadeIn(txt('선형 이론으로 연장한 붕괴 기준', -1.3, 29, OBS)))
        self.add(txt('실제 밀도와 실제 비선형 δ는 이 값과 다릅니다.', -3.3, 24, '#A9B8CB'))
        self.finish()

        self.cue('먼저 헤일로, 그 안으로 모이는 가스', '성장한 밀도 차이는 중력 구조를 만들고,\n그 안에 은하의 재료인 가스도 모입니다.')
        diffuse = matter_sphere(2.8, (0, .9, 0), 30, MASS)
        self.add(diffuse)
        self.beat(.28, diffuse.animate.scale(.75))
        self.dark_halo = halo()
        self.beat(.14, FadeOut(diffuse), FadeIn(self.dark_halo))
        progress = ValueTracker(0)
        gas = CoolingGas(progress)
        self.beat(.18, FadeIn(gas))
        self.add(txt('암흑물질 헤일로', -2.5, 28, MASS), txt('가스는 별도의 물질 성분', -3.5, 27, OBS))
        self.finish()

        self.cue('가스가 냉각하고, 원반과 별이 생긴다', '에너지를 빛으로 잃은 가스가 안쪽으로 모이고,\n회전 원반의 조밀한 곳에서 별이 태어납니다.')
        self.add(halo())
        progress = ValueTracker(0);self.gas = CoolingGas(progress);self.add(self.gas)
        waves = VGroup(*[Arc(radius=.18, start_angle=-PI/3, angle=2*PI/3, color=OBS, stroke_width=2).move_to([x, y, 0])
                         for x, y in [(1.55, 1.7), (-1.55, .15), (-.9, 2.3)]])
        self.beat(.1, Create(waves))
        self.beat(.32, progress.animate.set_value(1), waves.animate.scale(1.8).set_opacity(0), rate_func=linear)
        points = [(-.9, .7), (.65, 1.25), (.1, .85), (-.25, 1.1), (1.25, .65), (-1.3, 1.25)]
        self.seed_stars = VGroup(*[Dot([x, y, 0], radius=.055, color=LIGHT) for x, y in points])
        self.beat(.19, LaggedStart(*[FadeIn(dot, scale=.4) for dot in self.seed_stars], lag_ratio=.17))
        self.formation_labels = VGroup(txt('가스 냉각 → 회전 원반 → 별 형성', -2.65, 28, OBS),
                                      txt('원반 은하가 형성되는 한 사례', -3.85, 23, '#A9B8CB'))
        self.add(self.formation_labels)
        self.finish()

        self.cue('작은 차이가, 은하가 자랄 바탕으로', '헤일로 안에 가스와 별의 은하가 자리 잡습니다.\n시작은 거의 보이지 않던 작은 밀도 차이였습니다.', clear=False)
        disk = SpiralGalaxy()
        self.beat(.28, FadeOut(self.gas), FadeOut(self.seed_stars), FadeOut(self.formation_labels), FadeIn(disk))
        self.beat(.14, FadeIn(txt('Density Perturbation → Galaxy', -2.8, 30, MASS)))
        self.add(txt('초기 요동 → 중력 성장 → 헤일로 → 은하', -3.85, 24, LIGHT),
                 txt('작은 차이가 은하의 바탕이 된다', -4.65, 26, LIGHT))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        for mob in self.mobjects:
            mob.clear_updaters()
        self.beat(.08, *[FadeOut(mob) for mob in list(self.mobjects)])
        self.finish()
