"""Kakeya: zero volume does not mean smaller dimension.

Finite fans, tubes and translated triangles are explanatory diagrams,
not constructions of the limiting zero-measure Kakeya set.
"""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

BLUE = '#62CFFF'
GOLD = '#FFD166'
RED = '#FF7B72'
GREEN = '#78E6A6'
DIM = '#526781'


def lab(s, x=0, y=0, size=30, color=LIGHT, width=7.4):
    return txt(s, y, size, color, width=width).move_to([x, y, 0])


def needle(angle=0, center=(0, 1, 0), length=4, color=BLUE):
    c = np.array(center)
    v = length/2*np.array([np.cos(angle), np.sin(angle), 0])
    return Line(c-v, c+v, color=color, stroke_width=5)


def fan(n=32, radius=2.6, y=1):
    return VGroup(*[needle(a, (0, y, 0), radius*2,
                          BLUE if j % 2 else GREEN).set_stroke(width=1.5, opacity=.7)
                    for j, a in enumerate(np.linspace(0, PI, n, endpoint=False))])


def triangles(packed=False, n=11, offset=1):
    out = VGroup()
    for j, a in enumerate(np.linspace(0, PI, n, endpoint=False)):
        d = np.array([np.cos(a), np.sin(a), 0])
        normal = np.array([-np.sin(a), np.cos(a), 0])
        shift = offset*np.array([.45*np.cos(3*a), .35*np.sin(2*a), 0]) if packed else 1.9*d
        c = np.array([0, 1, 0])+shift
        out.add(Polygon(c-1.1*d-.13*normal, c+1.1*d,
                        c-1.1*d+.13*normal, color=BLUE if j % 2 else GREEN,
                        fill_opacity=.24, stroke_width=1))
    return out


def project(p):
    x, y, z = p
    return np.array([.85*x-.5*y, .35*x+.45*y+z, 0])


def cube(side=2.7, y=1, color=DIM):
    edges = VGroup()
    for axis in range(3):
        others = [a for a in range(3) if a != axis]
        for b in (-.5, .5):
            for c in (-.5, .5):
                p = np.zeros(3); p[others[0]] = b; p[others[1]] = c
                q = p.copy(); p[axis] = -.5; q[axis] = .5
                edges.add(Line(side*project(p)+UP*y, side*project(q)+UP*y,
                               color=color, stroke_width=1.4))
    return edges


def tubes(spread=0, angle=0, n=38):
    # Fibonacci sphere directions: straight spatial tubes, shown in projection.
    out = VGroup()
    for j in range(n):
        z = 1-2*(j+.5)/n; az = j*PI*(3-np.sqrt(5))+angle
        d = np.array([np.sqrt(1-z*z)*np.cos(az), np.sqrt(1-z*z)*np.sin(az), z])
        c = spread*np.array([np.sin(j*2.1), np.cos(j*1.3), np.sin(j*.9)])
        a = 2.6*project(c-d)+UP; b = 2.6*project(c+d)+UP
        color = BLUE if j % 3 else GREEN
        out.add(VGroup(Line(a, b, color=color, stroke_width=9, stroke_opacity=.12),
                       Line(a, b, color=color, stroke_width=1.4, stroke_opacity=.8)))
    return out


def cover(n=4, dim=2, y=1):
    if dim == 1:
        return VGroup(*[Square(side_length=4/n, color=BLUE, fill_opacity=.1,
                              stroke_width=1.2).move_to([-2+(j+.5)*4/n, y, 0]) for j in range(n)])
    return VGroup(*[Square(side_length=4/n, color=GREEN, fill_opacity=.06,
                          stroke_width=1).move_to([-2+(j+.5)*4/n, y-2+(k+.5)*4/n, 0])
                    for j in range(n) for k in range(n)])


def bundle(width=.25, angle=0, x=0, y=1, n=10, color=BLUE):
    return VGroup(*[needle(angle+(j-n/2)*width/10,
                          (x+(j-n/2)*width/5, y, 0), 4, color).set_stroke(width=3, opacity=.7)
                    for j in range(n)])


class KakeyaDimensionDiscovery(DensityGrowthDiscovery):
    TIMING = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION = TIMING['duration']

    def construct(self):
        self.brand = lab('과학의 한 장면  /  Fields 2026', y=7.1, size=21, color='#9BA9C3')
        self.add(self.brand)
        cues = [
            ('바늘을 돌리면, 원판이 생긴다', '모든 방향으로 돌린 바늘이\n지나가는 영역을 생각해봅니다.'),
            ('꼭, 가운데에서 돌려야 할까?', '중심을 고정하지 않고\n회전과 이동을 함께 할 수 있습니다.'),
            ('움직임은 잊고, 방향만 남겨보자', '이제는 연속 회전이 아니라\n각 방향의 단위 선분을 포함하는 문제입니다.'),
            ('공간은 겹쳐도, 방향은 사라지지 않는다', '각 선분의 길이와 방향은 그대로.\n평행 이동과 겹침의 개념도입니다.'),
            ('면적 0인데, 모든 방향이 들어 있다', '그런 Kakeya 집합이 존재합니다.\n유한 선분 그림은 방향의 개념도입니다.'),
            ('같은 면적 0인데, 정말 같은 걸까?', '선에는 한 방향.\nKakeya 집합에는 모든 방향.'),
            ('얼마나 채웠나 ≠ 어떤 구조인가', '면적만으로는 차이를 알 수 없습니다.\n다른 방식으로 살펴보겠습니다.'),
            ('선을, 두 배 더 자세히 보면?', '칸 크기를 절반으로 줄여봅니다.\n선을 덮는 칸: 4 → 8 → 16.'),
            ('면을, 두 배 더 자세히 보면?', '가로 두 배 × 세로 두 배.\n면을 덮는 칸: 4 → 16 → 64.'),
            ('입체는, 앞뒤까지 두 배', '규칙적인 입체: 2 × 2 × 2 = 8배.\n칸 수의 성장률이 차원을 알려줍니다.'),
            ('넓이는 없어도, 선처럼 단순하지 않다', '평면 Kakeya 집합: 면적 0 · 차원 2.\n매 단계 정확히 4배라는 뜻은 아닙니다.'),
            ('면적 0과, 낮은 차원은 다른 말', '얼마나 채웠나와\n해상도를 높이면 어떻게 늘어나는가는 다릅니다.'),
            ('앞뒤와 위아래, 모든 방향까지', '같은 질문을\n3차원 공간에서 해봅니다.'),
            ('선 → 작은 해상도 → 얇은 튜브', '선 주변에 작은 두께를 주는 분석 도구.\n실제 선 자체를 굵게 만든 것은 아닙니다.'),
            ('부피를 없애면, 차원도 줄어들까?', '3차원 Kakeya 집합도 부피는 0일 수 있습니다.\n차원도 3보다 작아질 수 있을까요?'),
            ('뭉치기 쉬운 방향, 벌어지는 방향', '비슷한 방향은 잘 겹치지만\n다른 방향은 서로 벌어집니다.'),
            ('하지만, 겹침은 아주 영리할 수 있다', '어떤 곳에서는 겹치고, 다른 곳에서는 갈라집니다.\n선 자체는 언제나 곧습니다.'),
            ('멀리서 한 묶음, 가까이서 여러 선', 'Hong Wang · Joshua Zahl\n확대 수준을 바꿔 겹침을 추적합니다.'),
            ('계속 뭉치거나, 결국 흩어지거나', '구조의 제약과 퍼짐을 함께 이용합니다.\n완전한 증명이 아닌 전략의 개념도입니다.'),
            ('부피는 0. 그래도 차원은 3.', '모든 R³ Kakeya 집합의\nHausdorff·Minkowski 차원은 3입니다.'),
            ('바늘의 겹침은, 파동의 문제와 닮았다', '다른 방향의 파동이\n얼마나 한곳에 모일 수 있을까요?'),
            ('부피는 없애도, 차원은 피할 수 없다', '모든 방향의 단위 선분을 담는다는 조건이\n3차원의 차원을 끝까지 남깁니다.'),
            ('모든 방향을 담으면, 차원 3은 남는다', '2025 Wang–Zahl 공동 증명.\nHong Wang의 폭넓은 업적 → 2026 필즈상.')]
        for i, (title, caption) in enumerate(cues):
            self.cue(title, caption)
            self.visual(i)
            self.finish()

    def visual(self, i):
        if i == 0:
            a = needle(); disk = Circle(radius=2, color=BLUE, fill_opacity=.14).move_to(UP)
            self.add(a, Dot(UP, color=GOLD))
            self.beat(.58, Rotate(a, PI, about_point=UP), Create(disk), rate_func=linear)
            self.beat(.12, FadeIn(lab('모든 방향 → 원판', y=-2.4, color=GOLD)))
        elif i == 1:
            a = needle(); self.add(a)
            for j in range(5):
                b = needle(j*PI/5, (.7*np.sin(j), 1+.6*np.cos(j), 0))
                self.beat(.12, Transform(a, b), FadeIn(b.copy().set_stroke(opacity=.2, width=2)))
            self.add(lab('회전 + 이동', y=-2.5, color=GOLD))
        elif i == 2:
            a = triangles(False); self.beat(.18, FadeIn(a))
            self.beat(.38, Transform(a, triangles(True)))
            self.add(lab('방향 유지 · 위치만 이동', y=-2.6, color=GOLD),
                     lab('배치의 개념도', y=-3.6, size=22, color=DIM))
        elif i == 3:
            a = triangles(True); self.add(a)
            self.beat(.4, Transform(a, triangles(True, offset=.15)))
            self.add(lab('같은 공간을 함께 쓴다', y=-1.7, color=BLUE))
            self.beat(.16, FadeIn(lab('방향은 모두 유지', y=-2.8, size=37, color=GOLD)))
            self.add(lab('실제 극한 구성은 더 정교합니다', y=-3.9, size=22, color=DIM))
        elif i == 4:
            a = fan(); self.beat(.15, Create(a))
            current = needle(0, length=5.2, color=GOLD); self.add(current)
            for angle in (PI/2, PI/4, 2*PI/3):
                self.beat(.1, Transform(current, needle(angle, length=5.2, color=GOLD)))
            self.beat(.15, FadeIn(lab('면적 = 0', y=-2.25, size=43, color=GOLD)))
            self.add(lab('그런데, 모든 방향이 있다', y=-3.4, size=32, color=BLUE))
        elif i == 5:
            self.add(needle(center=(-2, 1, 0), length=2.6),
                     fan(radius=1.35).move_to([2, 1, 0]))
            self.add(lab('선', -2, 3, 30, BLUE, 3), lab('Kakeya', 2, 3, 30, GREEN, 3))
            self.beat(.16, FadeIn(lab('면적 0', -2, -1, 31, BLUE, 3)),
                      FadeIn(lab('면적 0', 2, -1, 31, GREEN, 3)))
            self.add(lab('한 방향', -2, -2.1, 26, BLUE, 3), lab('모든 방향', 2, -2.1, 26, GREEN, 3))
            self.beat(.16, FadeIn(lab('같은 0인데, 같은 구조일까?', y=-3.7, size=33, color=GOLD)))
        elif i == 6:
            a = VGroup(lab('얼마나 채웠나?', y=2.9, size=38, color=BLUE),
                       Rectangle(width=3.8, height=1.3, color=BLUE, fill_opacity=.16).move_to([0, 1.4, 0]),
                       lab('면적', y=1.4, color=BLUE))
            self.beat(.2, FadeIn(a))
            self.beat(.18, FadeIn(lab('이 숫자 하나로는 부족하다', y=-.2, size=33)))
            self.beat(.2, FadeIn(lab('더 자세히 보면, 어떻게 늘어날까?', y=-2.3, size=35, color=GOLD)))
        elif i == 7:
            a = cover(4, dim=1); count = lab('4칸', y=-1.4, size=43, color=GOLD)
            self.add(needle(length=4), a, count)
            for n in (8, 16):
                self.beat(.24, Transform(a, cover(n, dim=1)),
                          Transform(count, lab(f'{n}칸', y=-1.4, size=43, color=GOLD)))
            self.add(lab('두 배 더 자세히 → 칸도 두 배', y=-3.2, size=30, color=BLUE))
        elif i == 8:
            a = cover(2); count = lab('4칸', y=-2, size=40, color=GOLD)
            self.add(a, count)
            for n in (4, 8):
                self.beat(.24, Transform(a, cover(n)),
                          Transform(count, lab(f'{n*n}칸', y=-2, size=40, color=GOLD)))
            self.add(lab('가로 2배 × 세로 2배 = 4배', y=-3.5, size=30, color=GREEN))
        elif i == 9:
            shape = cube(3.3)
            dividers = VGroup()
            for face_axis in range(3):
                for face in (-.5, .5):
                    for varying in (k for k in range(3) if k != face_axis):
                        p = np.zeros(3); q = np.zeros(3)
                        p[face_axis] = q[face_axis] = face
                        p[varying] = -.5; q[varying] = .5
                        dividers.add(Line(3.3*project(p)+UP, 3.3*project(q)+UP,
                                          color=BLUE, stroke_width=1.2))
            self.add(shape)
            self.beat(.3, Create(dividers))
            self.beat(.18, FadeIn(lab('2 × 2 × 2 = 8', y=-2.1, size=43, color=GOLD)))
            self.add(lab('1차원 2배 / 2차원 4배 / 3차원 8배', y=-3.4, size=27))
        elif i == 10:
            self.add(fan(radius=2.05))
            self.beat(.16, FadeIn(lab('면적 = 0', y=-1.9, size=38, color=BLUE)))
            self.beat(.2, FadeIn(lab('차원 = 2', y=-3.1, size=49, color=GOLD)))
            self.add(lab('집합 전체를 덮는 칸 수의 성장률', y=3.8, size=23, color=GREEN))
        elif i == 11:
            for x, s, value, col in ((-2, '면적', '0', BLUE), (2, '차원', '2', GOLD)):
                self.add(RoundedRectangle(width=3.2, height=3, corner_radius=.2, color=col).move_to([x, 1.3, 0]),
                         lab(s, x, 2.2, 32, col, 3), lab(value, x, .9, 65, col, 3))
            self.beat(.25, FadeIn(lab('면적 0 ≠ 낮은 차원', y=-2.3, size=40, color=GOLD)))
        elif i == 12:
            a = fan(radius=2); self.add(a)
            self.beat(.4, Transform(a, tubes()), Create(cube(4)))
            self.add(lab('좌우 · 앞뒤 · 위아래', y=-3.3, size=33, color=GOLD))
        elif i == 13:
            line = needle(length=5)
            tube = RoundedRectangle(width=5.4, height=.7, corner_radius=.3,
                                    color=BLUE, fill_opacity=.13, stroke_width=2).move_to(UP)
            tube.set_z_index(-1)
            self.add(line, lab('곧은 선', y=2.7, color=BLUE))
            self.beat(.22, FadeIn(tube))
            self.beat(.22, FadeIn(lab('해상도 r만큼의 주변', y=-.5, size=32, color=GOLD)))
            self.beat(.2, tube.animate.stretch_to_fit_height(.24))
            self.add(lab('더 자세히 볼수록, 더 얇게', y=-2.6, size=30))
        elif i == 14:
            self.add(VGroup(cube(3.4), tubes().scale(.85, about_point=UP)).shift(UP*.35))
            self.beat(.15, FadeIn(lab('부피 = 0 가능', y=-2.3, size=39, color=BLUE)))
            self.beat(.18, FadeIn(lab('차원도 3보다 작게?', y=-3.5, size=39, color=GOLD)))
        elif i == 15:
            a = bundle(); self.beat(.2, Create(a))
            self.add(lab('비슷한 방향은 뭉치기 쉽다', y=-2.4, size=30, color=BLUE))
            self.beat(.35, Transform(a, fan()))
            self.beat(.13, FadeIn(lab('다른 방향은 벌어진다', y=-3.6, size=31, color=GOLD)))
        elif i == 16:
            a = VGroup(*[needle(t, (0, 1, 0), 5).set_stroke(width=12, opacity=.2)
                         for t in (-.25, -.13, 0, .13, .25)])
            self.beat(.25, Create(a))
            self.add(Circle(radius=.5, color=GOLD).move_to(UP))
            self.beat(.2, FadeIn(lab('여기서는 겹치고', y=-.3, color=GOLD)),
                      FadeIn(lab('다른 곳에서는 갈라진다', y=-2, size=32, color=BLUE)))
            self.add(lab('선은 휘지 않습니다', y=-3.4, size=24, color=DIM))
        elif i == 17:
            # Same collection, successively revealed rather than new bent branches.
            lines = bundle(.3)
            coarse = RoundedRectangle(width=4.7, height=1.2, corner_radius=.2, color=GREEN, fill_opacity=.3).move_to(UP)
            mid = VGroup(*[Rectangle(width=4.1, height=.22, color=GREEN, fill_opacity=.2).move_to([0, 1+j*.25, 0]) for j in (-1, 0, 1)])
            self.add(coarse)
            self.beat(.22, ReplacementTransform(coarse, mid))
            self.beat(.26, FadeOut(mid), Create(lines))
            self.add(lab('멀리서: 한 묶음', y=3.1, size=30, color=GREEN),
                     lab('가까이서: 개별 선들의 겹침', y=-2.1, size=30, color=BLUE))
            self.beat(.13, FadeIn(lab('확대 수준을 바꿔 추적한다', y=-3.5, size=31, color=GOLD)))
        elif i == 18:
            self.add(bundle(.15).scale(.45).move_to([-1.8, 2, 0]), fan(radius=1).move_to([1.8, 2, 0]))
            self.beat(.16, FadeIn(lab('계속 뭉치면', -1.8, .6, 26, BLUE, 3)),
                      FadeIn(lab('흩어지면', 1.8, .6, 26, GREEN, 3)))
            self.add(lab('구조를 이용', -1.8, -.25, 24, BLUE, 3), lab('퍼짐을 이용', 1.8, -.25, 24, GREEN, 3))
            self.beat(.16, Create(Arrow([-1.8, -.8, 0], [-.3, -2, 0], color=BLUE)),
                      Create(Arrow([1.8, -.8, 0], [.3, -2, 0], color=GREEN)))
            self.beat(.16, FadeIn(lab('어느 쪽도, 차원 < 3 불가능', y=-3, size=34, color=GOLD)))
        elif i == 19:
            self.add(tubes().scale(.65).move_to([0, 2.2, 0]))
            self.beat(.18, FadeIn(lab('부피 = 0', y=-.5, size=42, color=BLUE)))
            self.beat(.22, FadeIn(lab('차원 = 3', y=-2, size=56, color=GOLD)))
            self.add(lab('Hausdorff = Minkowski = 3', y=-3.6, size=27, color=GREEN))
        elif i == 20:
            # Wave packets are schematic; geometry alone does not settle every PDE conjecture.
            packets = VGroup()
            for angle in (-.65, 0, .65):
                points = [np.array([u, .12*np.sin(10*u)*np.exp(-u*u/4), 0]) for u in np.linspace(-2.8, 2.8, 150)]
                wave = VMobject(color=GOLD, stroke_width=2).set_points_as_corners(points).rotate(angle).shift(UP)
                outline = needle(angle, length=5.6, color=BLUE).set_stroke(width=20, opacity=.13)
                packets.add(VGroup(outline, wave))
            self.beat(.4, LaggedStart(*[Create(p) for p in packets], lag_ratio=.25))
            self.add(lab('다른 방향의 파동이, 한곳에 모인다', y=-2.2, size=31, color=GOLD))
            self.beat(.15, FadeIn(lab('기하학 ↔ 푸리에 해석 ↔ 파동', y=-3.6, size=28, color=GREEN)))
        elif i == 21:
            a = needle(); self.add(a)
            self.beat(.3, Transform(a, fan(radius=2)))
            self.beat(.2, FadeIn(lab('부피는 없애도', y=-1.8, size=37, color=BLUE)))
            self.beat(.16, FadeIn(lab('차원은 피할 수 없다', y=-3, size=43, color=GOLD)))
        else:
            self.add(tubes().scale(.6).move_to([0, 2.2, 0]))
            self.beat(.15, FadeIn(lab('부피 0이어도, 차원은 3', y=-.2, size=40, color=GOLD)))
            self.beat(.15, FadeIn(lab('Hong Wang · Joshua Zahl', y=-1.45, size=31)))
            self.add(lab('2025  /  3차원 Kakeya 공동 증명', y=-2.35, size=24, color=GREEN))
            self.beat(.15, FadeIn(lab('Hong Wang', y=-3.45, size=35, color=BLUE)))
            self.add(lab('2026 Fields Medal', y=-4.2, size=26, color=GOLD))
