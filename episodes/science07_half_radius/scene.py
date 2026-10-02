"""Why half the turnaround radius: conserved energy plus virial equilibrium."""
import json
import re
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import GravitationalLensingDiscovery, txt, LIGHT, OBS, MASS, EXPECT
from episodes.science04_virial_theorem.scene import MovingCluster


def formula(s, y=0, size=42, color=OBS, width=7.5):
    """Cambria text with explicit, portable ta/vir subscripts."""
    items = []
    for part in re.split(r'([A-Za-z]_(?:ta|vir))', s):
        if not part:
            continue
        if re.fullmatch(r'[A-Za-z]_(?:ta|vir)', part):
            base, sub = part.split('_')
            letter = Text(base, font='Cambria', font_size=size, color=color)
            suffix = Text(sub, font='Cambria', font_size=size*.56, color=color)
            suffix.next_to(letter, RIGHT, buff=.025).shift(DOWN*size/190)
            items.append(VGroup(letter, suffix))
        else:
            items.append(Text(part, font='Cambria', font_size=size, color=color))
    group = VGroup(*items).arrange(RIGHT, buff=.035, aligned_edge=UP)
    if group.width > width:
        group.scale_to_fit_width(width)
    return group.move_to([0, y, 0])


rng = np.random.default_rng(71)
cloud_points = rng.normal(size=(24, 3))
cloud_points /= np.linalg.norm(cloud_points, axis=1)[:, None]
cloud_points *= rng.uniform(.02, .95, (24, 1))**(1/3)


def cloud(radius=2, center=(0, 1.25, 0), speed=0):
    c = np.asarray(center, dtype=float)
    g = VGroup(Circle(radius=radius, color=LIGHT, stroke_opacity=.6).move_to(c))
    for i, point in enumerate(cloud_points):
        p = c + radius*np.array([point[0], point[1], 0])
        g.add(Dot(p, radius=.035, color=LIGHT))
        if speed > .01 and i % 6 == 0:
            inward = -np.array([point[0], point[1], 0])
            inward /= np.linalg.norm(inward)
            g.add(Arrow(p, p + inward*speed*.4, buff=0, color=OBS, stroke_width=2))
    return g


def signed_bar(value, y, color, unit=1.35):
    zero = .2
    if abs(value) < .001:
        return Dot([zero, y, 0], radius=.04, color=color)
    return Rectangle(width=abs(value)*unit, height=.25, stroke_width=0,
                     fill_color=color, fill_opacity=.85).move_to([zero+value*unit/2, y, 0])


def energies(r):
    """Normalized ledger: initial U=-1, E=-1, no energy or mass lost."""
    u = -1/r
    return -1-u, u, -1.


def energy_board(r):
    k, u, e = energies(r)
    rows = [(k, 1.25, 'K', OBS), (u, 0., 'U', MASS), (e, -1.25, 'E', LIGHT)]
    board = VGroup(DashedLine([.2, -1.75, 0], [.2, 1.85, 0], color='#66758C', stroke_width=1))
    board.add(formula('0', 2.12, 25, '#A9B8CB').shift(RIGHT*.2))
    for value, y, name, color in rows:
        board.add(formula(name, y, 34, color).shift(LEFT*3.4), signed_bar(value, y, color))
        value_text = '0.0' if abs(value) < .001 else f'{value:+.1f}'.replace('-', '−')
        board.add(formula(value_text, y, 29, color).shift(RIGHT*3.2))
    return board


class HalfRadiusDiscovery(GravitationalLensingDiscovery):
    TIMING = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION = TIMING['duration']

    def to(self, frame):
        remaining = frame-round(self.time*30)
        if remaining < 0:
            raise RuntimeError(f'Cue overrun at {self.time}: target {frame/30}')
        if remaining:
            self.wait(remaining/30-1e-6)

    def cue(self, *args, **kwargs):
        if kwargs.get('clear', True):
            for mob in self.mobjects:
                mob.clear_updaters()
        super().cue(*args, **kwargs)

    def construct(self):
        self.brand = txt('과학의 한 장면  /  07', 7.1, 23, '#9BA9C3')
        self.add(self.brand)

        self.cue('안정된 크기는 왜 절반쯤일까?', 'Turnaround에서는 가장 크게 부풀어 있고,\n이 영역의 팽창 속도는 거의 0입니다.')
        sphere = cloud(2.05)
        radius = Line([0, 1.25, 0], [2.05, 1.25, 0], color=LIGHT, stroke_width=3)
        self.beat(.18, FadeIn(sphere), Create(radius))
        self.beat(.15, FadeIn(formula('R = R_ta', -1.8, 43, LIGHT)), FadeIn(txt('최대 팽창 크기', -2.65, 27, LIGHT)))
        self.beat(.16, FadeIn(txt('이 크기의 절반이 되는 이유는?', -3.9, 31, MASS)))
        self.finish()

        self.cue('처음의 에너지는 거의 전부 U', '내부 무작위 운동을 무시한 단순 모형에서는,\n전체 에너지가 거의 전부 중력 에너지입니다.')
        self.add(cloud(1.25, (0, 2.6, 0)))
        self.beat(.18, FadeIn(formula('K_ta ≈ 0', .6, 39, OBS)))
        self.beat(.18, FadeIn(formula('E_ta ≈ U_ta', -.9, 47, MASS)))
        self.add(formula('U < 0', -2.35, 36, MASS), txt('무작위 운동이 없는 균일한 구를 가정', -3.95, 22, '#A9B8CB'))
        self.finish()

        self.cue('수축하면서, 운동에너지가 생긴다', '중력 에너지 일부가 운동에너지로 바뀌며,\n영역은 줄어들고 입자들은 빨라집니다.')
        r = ValueTracker(1)
        sphere = always_redraw(lambda: cloud(2.1*r.get_value(), speed=energies(r.get_value())[0]))
        self.add(sphere)
        self.beat(.55, r.animate.set_value(.58), rate_func=linear)
        self.add(txt('수축 → 속도 증가', -2.1, 33, OBS), formula('U ↓    K ↑', -3.25, 38, MASS),
                 txt('U는 더 음수가 되고, K는 증가합니다.', -4.3, 22, '#A9B8CB'))
        self.finish()

        self.cue('부호를 포함해 더하면, E는 그대로', '질량과 에너지가 빠져나가지 않는다면,\nK는 늘고 U는 더 음수가 되어도 E는 같습니다.')
        r = ValueTracker(1)
        self.add(always_redraw(lambda: energy_board(r.get_value())))
        self.add(txt('음수 ←                 → 양수', 3.05, 25, '#A9B8CB'))
        self.beat(.56, r.animate.set_value(.5), rate_func=linear)
        self.beat(.12, FadeIn(formula('E = K + U = constant', -2.65, 36, LIGHT)))
        self.add(txt('K: 0 → 1    U: −1 → −2    E: −1 그대로', -3.65, 23, LIGHT),
                 txt('단위는 최대 팽창 에너지의 절댓값으로 정규화', -4.35, 21, '#A9B8CB'))
        self.finish()

        self.cue('안정된 뒤에는, 비리얼 관계', '운동에너지의 두 배와 중력 에너지의 합은 0.\nK는 U의 절댓값의 절반입니다.')
        bound = MovingCluster(center=(0, 2.35, 0), radius=1.25, speed=1.1, arrows=True)
        self.add(bound)
        relation = formula('2K + U = 0', .05, 46)
        self.beat(.17, FadeIn(relation))
        self.beat(.18, Transform(relation, formula('K = −U / 2', .05, 46)))
        self.add(Rectangle(width=1.35, height=.25, fill_color=OBS, fill_opacity=.85, stroke_width=0).move_to([-1.5, -1.55, 0]),
                 Rectangle(width=2.7, height=.25, fill_color=MASS, fill_opacity=.85, stroke_width=0).move_to([1.45, -1.55, 0]),
                 formula('K', -2.15, 29, OBS).shift(LEFT*1.5), formula('|U|', -2.15, 29, MASS).shift(RIGHT*1.45),
                 txt('K와 U는 안정된 상태의 시간 평균', -3.45, 24, '#A9B8CB'))
        self.finish()

        self.cue('최종 전체 에너지는 U의 절반', '비리얼 관계를 전체 에너지에 넣으면,\n최종 E는 최종 U의 절반입니다.')
        self.beat(.12, FadeIn(formula('E = K + U', 2.55, 44)))
        self.beat(.17, FadeIn(formula('E = −U / 2 + U', 1.15, 44)))
        self.beat(.17, FadeIn(formula('E = U / 2', -.25, 51, LIGHT)))
        self.add(formula('+1 + (−2) = −1', -2.15, 35, LIGHT), txt('예: K = 1, U = −2일 때', -3.3, 26, '#A9B8CB'))
        self.finish()

        self.cue('같은 E를, 두 상태에서 비교하면', '처음에는 U 전부, 나중에는 U의 절반.\n최종 U는 처음보다 두 배 더 음수여야 합니다.')
        self.add(txt('최대 팽창', 3.0, 27, LIGHT).shift(LEFT*2), txt('안정 뒤', 3.0, 27, MASS).shift(RIGHT*2))
        self.beat(.14, FadeIn(formula('E_ta = U_ta', 1.95, 35, LIGHT, 3.5).shift(LEFT*2)),
                  FadeIn(formula('E_vir = ½ U_vir', 1.95, 35, MASS, 3.5).shift(RIGHT*2)))
        self.beat(.17, FadeIn(formula('E_ta = E_vir', .25, 40, LIGHT)))
        self.beat(.18, FadeIn(formula('U_ta = ½ U_vir', -1.4, 47, MASS)))
        self.beat(.12, FadeIn(formula('U_vir = 2 U_ta', -2.8, 43, MASS)))
        self.add(txt('−1 = ½ × (−2)', -4, 28, LIGHT))
        self.finish()

        self.cue('반지름이 작아지면 |U|는 커진다', '같은 질량과 비슷한 밀도 분포라면,\n반지름 절반 → 중력 에너지 절댓값 두 배.')
        r = ValueTracker(1)
        self.add(always_redraw(lambda: cloud(1.75*r.get_value(), (0, 2.0, 0))))
        self.add(formula('|U| ∝ 1 / R', -.25, 46, MASS))
        bar = always_redraw(lambda: Rectangle(width=1.25/r.get_value(), height=.3, stroke_width=0,
                           fill_color=MASS, fill_opacity=.85).move_to([-1.25+.625/r.get_value(), -1.6, 0]))
        self.add(bar, formula('|U|', -1.6, 31, MASS).shift(LEFT*2.35))
        self.beat(.52, r.animate.set_value(.5), rate_func=linear)
        self.add(txt('반지름 ½    |U| 2배', -2.75, 31, LIGHT), formula('U = −C GM² / R', -3.7, 32, MASS),
                 txt('M과 구조 계수 C를 같게 두는 모형', -4.5, 21, '#A9B8CB'))
        self.finish()

        self.cue('두 조건을 합치면, 반지름 절반', '중력 에너지의 절댓값이 두 배가 되려면,\n반지름은 절반이어야 합니다.')
        self.beat(.14, FadeIn(formula('U_vir = 2 U_ta', 2.7, 44, MASS)))
        self.beat(.14, FadeIn(formula('U ∝ −1 / R', 1.3, 43, MASS)))
        self.beat(.18, FadeIn(formula('1 / R_vir = 2 / R_ta', -.2, 42)))
        self.beat(.16, FadeIn(Arrow([0, -1, 0], [0, -1.75, 0], buff=0, color=LIGHT)),
                  FadeIn(formula('R_vir ≈ ½ R_ta', -2.65, 51, LIGHT)))
        self.add(txt('질량·에너지 보존 + 같은 구조 계수', -4, 24, '#A9B8CB'))
        self.finish()

        self.cue('같은 눈금으로 보면, 2 : 1', '절반은 면적이나 부피가 아니라,\n최대 팽창 크기와 비교한 반지름입니다.')
        left_center = np.array([-2, 1.75, 0]); right_center = np.array([2, 1.75, 0])
        self.add(cloud(1.6, left_center))
        bound = MovingCluster(center=right_center, radius=.8, speed=1.1)
        self.add(bound)
        for center, radius in [(left_center, 1.6), (right_center, .8)]:
            self.add(Line(center, center+RIGHT*radius, color=LIGHT, stroke_width=3), Dot(center, color=LIGHT, radius=.04))
        self.add(txt('최대 팽창', -.55, 25, LIGHT).shift(LEFT*2), txt('안정 뒤', -.55, 25, MASS).shift(RIGHT*2))
        a = Line([-1.25, -1.75, 0], [1.55, -1.75, 0], color=LIGHT, stroke_width=5)
        b = Line([-1.25, -2.85, 0], [.15, -2.85, 0], color=MASS, stroke_width=5)
        self.beat(.17, Create(a), FadeIn(formula('R_ta', -1.75, 32, LIGHT).shift(LEFT*2.65)))
        self.beat(.17, Create(b), FadeIn(formula('R_vir', -2.85, 32, MASS).shift(LEFT*2.65)))
        self.beat(.13, FadeIn(formula('2 : 1', -3.95, 43, LIGHT)))
        self.finish()

        self.cue('절반을 만드는 두 조건', '에너지 보존과 Virial theorem이 함께 만든 결과.\n실제 크기는 질량 손실과 밀도 분포에 따라 달라집니다.')
        self.add(txt('에너지 보존', 3.1, 31, LIGHT), txt('비리얼 정리', 2.2, 31, OBS))
        self.beat(.15, FadeIn(formula('E_ta = E_vir', .9, 38, LIGHT)), FadeIn(formula('2K + U = 0', -.15, 38, OBS)))
        self.beat(.18, FadeIn(formula('R_vir ≈ ½ R_ta', -1.9, 53, LIGHT)))
        self.beat(.13, FadeIn(txt('Spherical Collapse', -3.15, 34, MASS)))
        self.add(txt('질량 손실·에너지 유출 없음 · 같은 구조 계수', -4.2, 21, '#A9B8CB'))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        for mob in self.mobjects:
            mob.clear_updaters()
        self.beat(.08, *[FadeOut(mob) for mob in list(self.mobjects)])
        self.finish()
