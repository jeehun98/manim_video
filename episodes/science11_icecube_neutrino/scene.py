"""Rare interaction -> Cherenkov timing -> reconstructed cosmic direction."""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT, OBS, MASS, GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

ICE = '#8FE7FF'
BLUE = '#31B7FF'
EARTH = '#56A7C7'
EARLY = '#FFE08A'
LATE = '#8F9CFF'


def earth(center=(0, 1, 0), radius=2.15):
    center = np.array(center, dtype=float)
    globe = Circle(radius=radius, color=EARTH, fill_color='#102E4D', fill_opacity=.88).move_to(center)
    land = VGroup(
        Polygon(*(center + radius*np.array([[-.75,.25,0],[-.45,.62,0],[-.08,.5,0],[.12,.15,0],[-.18,-.05,0],[-.42,.05,0]])),
                stroke_width=0, fill_color='#4B8F73', fill_opacity=.8),
        Polygon(*(center + radius*np.array([[.18,.58,0],[.68,.38,0],[.78,.02,0],[.5,-.08,0],[.25,.15,0]])),
                stroke_width=0, fill_color='#4B8F73', fill_opacity=.8),
        Polygon(*(center + radius*np.array([[.05,-.16,0],[.35,-.28,0],[.22,-.72,0],[-.02,-.55,0]])),
                stroke_width=0, fill_color='#4B8F73', fill_opacity=.8),
    )
    atmosphere = Circle(radius=radius*1.07, color=ICE, stroke_opacity=.22, stroke_width=8).move_to(center)
    return VGroup(atmosphere, globe, land)


def detector_array(center=(0, .8, 0), scale=1):
    c = np.array(center, dtype=float)
    front = Polygon(*(c+scale*np.array([[-2.8,2.7,0],[2.8,2.7,0],[2.8,-2.9,0],[-2.8,-2.9,0]])),
                    color=ICE, stroke_opacity=.55, fill_color='#0C4160', fill_opacity=.32)
    back_shift = scale*np.array([.72,.52,0])
    back = front.copy().shift(back_shift).set_fill(opacity=.1)
    joins = VGroup(*[Line(front.get_vertices()[i], back.get_vertices()[i], color=ICE, stroke_opacity=.45)
                     for i in range(4)])
    strings = VGroup(); sensors = VGroup()
    for x in np.linspace(-2.25, 2.25, 7):
        top = c+scale*np.array([x,2.25,0]) + back_shift*(x+2.25)/4.5
        bottom = top+scale*DOWN*4.65
        strings.add(Line(top, bottom, color=ICE, stroke_opacity=.3, stroke_width=1.4))
        for f in np.linspace(.08,.92,7):
            sensors.add(Dot(interpolate(top,bottom,f), radius=.035*scale, color=ICE))
    return VGroup(back, front, joins, strings, sensors)


def cherenkov(track_start=(-2.7,-1.8,0), track_end=(2.6,2.7,0)):
    a, b = np.array(track_start, dtype=float), np.array(track_end, dtype=float)
    direction = b-a; direction /= np.linalg.norm(direction)
    normal = np.array([-direction[1], direction[0], 0])
    vertex = a+.35*(b-a)
    rays = VGroup()
    for f in np.linspace(.12,1,8):
        p = vertex+f*3.2*direction
        width = f*1.45
        rays.add(Line(p, p+normal*width, color=BLUE, stroke_opacity=.2+.55*f, stroke_width=2),
                 Line(p, p-normal*width, color=BLUE, stroke_opacity=.2+.55*f, stroke_width=2))
    cone = Polygon(vertex, b+normal*1.45, b-normal*1.45, color=BLUE,
                   fill_color=BLUE, fill_opacity=.06, stroke_opacity=.25)
    return VGroup(cone, rays)


def starfield(seed=11, count=44):
    rng = np.random.default_rng(seed)
    return VGroup(*[Dot([rng.uniform(-4.1,4.1),rng.uniform(-3.5,4.7),0],
                        radius=rng.uniform(.012,.038), color=LIGHT).set_opacity(rng.uniform(.35,.9))
                    for _ in range(count)])


class IceCubeNeutrinoDiscovery(DensityGrowthDiscovery):
    TIMING = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION = TIMING['duration']

    def construct(self):
        self.brand = txt('과학의 한 장면  /  Nobel 01', 7.1, 22, '#9BA9C3')
        self.add(self.brand)

        self.cue('지구에 흔적을 남기는 입자들', '빛은 흡수되고, 전하를 띤 입자는 휘어집니다.\n그런데 뉴트리노는 다릅니다.')
        globe = earth((0,1,0),1.85); self.add(globe)
        photon = Line([-4,2.6,0],[-1.05,1.55,0],color=LIGHT,stroke_width=3)
        charged = CubicBezier([-4,1.2,0],[-2.2,.95,0],[-1.4,-.3,0],[-.4,-.65,0]).set_color('#FF978D')
        neutrino = Line([-4,-1.1,0],[4,2.3,0],color=OBS,stroke_width=3)
        self.beat(.17,Create(photon),Create(charged),Create(neutrino))
        self.add(txt('광자 · 흡수',3.3,23,LIGHT).shift(LEFT*2.7),
                 txt('하전입자 · 굴절',-.9,23,'#FF978D').shift(LEFT*2.4),
                 txt('뉴트리노 · 거의 직진',-2.65,25,OBS))
        self.finish()

        self.cue('대부분, 지구도 그냥 통과한다', '전하가 없고 물질과 거의 반응하지 않아\n대부분 아무 흔적도 남기지 않습니다.')
        globe = earth((0,.85,0),2.35); self.add(globe)
        paths = VGroup(*[Line([-4,y,0],[4,y+1.2,0],color=OBS,stroke_opacity=.22,stroke_width=1.4)
                         for y in np.linspace(-1.5,2.3,8)])
        main = Line([-4,-1.25,0],[4,2.05,0],color=OBS,stroke_width=4)
        dot = Dot(main.get_start(),radius=.075,color=OBS); self.add(paths,dot)
        self.beat(.55,MoveAlongPath(dot,main),rate_func=linear)
        self.add(txt('neutrino',-2.7,32,OBS),txt('“통과하는 입자를 어떻게 볼까?”',-3.85,32,LIGHT))
        self.finish()

        self.cue('검출기를, 1 km³로 만든다면?', '남극 얼음 속 5,160개의 광센서.\n이 거대한 검출기가 IceCube입니다.')
        array = detector_array((0,.8,0),.88)
        self.beat(.22,FadeIn(array[0:3]))
        self.beat(.3,Create(array[3]),FadeIn(array[4]))
        self.add(txt('ANTARCTICA',4.25,24,'#9BA9C3'),txt('1 km³',-2.65,48,LIGHT),
                 txt('86 strings  ·  5,160 light sensors',-3.75,25,ICE))
        self.finish()

        self.cue('아주 드문 충돌 하나', '뉴트리노가 얼음 속 원자핵과 충돌하면\n빠른 2차 하전입자가 만들어집니다.')
        array = detector_array((0,.8,0),.86).set_opacity(.38); self.add(array)
        incoming = Arrow([-3.8,-2.5,0],[-.3,.45,0],buff=0,color=OBS,stroke_width=3,max_tip_length_to_length_ratio=.08)
        nucleus = VGroup(Circle(radius=.24,color=MASS),Dot(radius=.08,color=LIGHT)).move_to([-.25,.5,0])
        secondary = Arrow([-.05,.7,0],[3.1,3.35,0],buff=0,color=LIGHT,stroke_width=5,max_tip_length_to_length_ratio=.08)
        self.beat(.24,GrowArrow(incoming),FadeIn(nucleus))
        self.beat(.22,GrowArrow(secondary),Flash(nucleus,color=BLUE,flash_radius=.6))
        self.add(txt('ν',-1.05,39,OBS).shift(LEFT*1.5),txt('2차 하전입자',3.85,27,LIGHT),
                 txt('센서가 뉴트리노를 직접 보는 것은 아닙니다.',-3.7,22,'#9BA9C3'))
        self.finish()

        self.cue('얼음 속에서 퍼지는 푸른 빛', '2차 입자가 얼음 속 빛보다 빠르면\n체렌코프 빛이 원뿔처럼 퍼집니다.')
        start,end=np.array([-2.8,-2,0]),np.array([2.7,2.7,0])
        track=Line(start,end,color=LIGHT,stroke_width=4); particle=Dot(start,radius=.08,color=LIGHT)
        self.add(track.copy().set_opacity(.18),particle)
        self.beat(.28,MoveAlongPath(particle,track),rate_func=linear)
        cone=cherenkov(start,end); self.beat(.28,FadeIn(cone))
        self.add(txt('Cherenkov light',-3.25,34,BLUE),
                 txt('얼음 속 빛의 속도 기준 · 진공 광속은 넘지 않음',-4.15,21,'#9BA9C3'))
        self.finish()

        self.cue('센서마다, 빛이 오는 시간이 다르다', '가까운 센서부터 차례로 반응하며\n빛의 세기와 도착 시간을 기록합니다.')
        array=detector_array((0,.8,0),.86); array[4].set_opacity(.22); self.add(array)
        hits=[array[4][i] for i in [8,16,23,31,38,46]]
        for i,hit in enumerate(hits):
            color=ManimColor(EARLY).interpolate(ManimColor(LATE),i/(len(hits)-1))
            self.beat(.055,hit.animate.set_color(color).set_opacity(1).scale(2.2),
                      Flash(hit,color=color,flash_radius=.25))
            self.add(txt(f't{i+1}',hit.get_center()[1],18,color).move_to(hit.get_center()+RIGHT*.28))
        self.add(txt('early',-2.9,25,EARLY).shift(LEFT*2),txt('late',-2.9,25,LATE).shift(RIGHT*2),
                 Arrow([-1.15,-2.9,0],[1.15,-2.9,0],buff=0,color='#9BA9C3',stroke_width=2))
        self.finish()

        self.cue('시간차를 거꾸로 맞추면', '빛의 패턴에서 입자 경로를 복원하고\n그 선을 하늘로 연장해 온 방향을 찾습니다.')
        stars=starfield(); self.add(stars)
        hit_points=[[-2.1,-2.5,0],[-1.25,-1.35,0],[-.25,-.2,0],[.8,1,0],[1.8,2.15,0]]
        hits=VGroup(*[Dot(p,radius=.09,color=ManimColor(EARLY).interpolate(ManimColor(LATE),i/4)) for i,p in enumerate(hit_points)])
        self.beat(.18,FadeIn(hits))
        path=Line([-2.75,-3.25,0],[3.35,4.15,0],color=OBS,stroke_width=4)
        self.beat(.28,Create(path))
        source=Star(n=5,outer_radius=.28,inner_radius=.12,color=LIGHT,fill_color=LIGHT,fill_opacity=1).move_to(path.get_end())
        self.beat(.14,FadeIn(source),Flash(source,color=LIGHT,flash_radius=.55))
        self.add(txt('light pattern  →  trajectory  →  source',-3.85,25,LIGHT))
        self.finish()

        self.cue('빛으로 못 보는 우주를, 경로로 본다', '이 아이디어를 현실로 만든 Francis Halzen.\n2026년 노벨 물리학상으로 이어졌습니다.')
        stars=starfield(13,52); self.add(stars)
        line=Line([-3.2,-2.8,0],[2.5,3.45,0],color=OBS,stroke_width=3); self.add(line)
        medal=VGroup(Circle(radius=1.05,color=LIGHT,fill_color='#6B4E1E',fill_opacity=.75,stroke_width=4),
                     txt('NOBEL',.25,27,LIGHT),txt('2026',-.35,39,LIGHT)).move_to([0,1.6,0])
        self.beat(.22,FadeIn(medal),Flash(medal,color=LIGHT,flash_radius=1.3))
        self.add(txt('Francis Halzen',-.15,37,LIGHT),
                 txt('IceCube · astrophysical high-energy neutrinos',-1.05,23,ICE),
                 txt('보이지 않는 입자의 경로가\n새로운 망원경이 되었습니다.',-3.05,34,OBS))
        self.finish()
