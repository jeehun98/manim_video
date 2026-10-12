"""Detector plus observation -> a new window for high-energy astronomy."""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt, LIGHT, OBS, MASS, GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery
from episodes.science11_icecube_neutrino.scene import detector_array, earth, starfield, ICE, BLUE

GAMMA = '#FFD17A'
CRAY = '#FF8E86'
GREEN = '#71E5A5'


def accelerator(center=(-2.8, 1.2, 0), scale=1):
    c = np.array(center, dtype=float)
    glow = VGroup(*[Circle(radius=scale*r, stroke_width=0, fill_color=MASS,
                           fill_opacity=.02+.012*i).move_to(c)
                    for i, r in enumerate(np.linspace(1.5,.35,8))])
    disk = VGroup(*[Ellipse(width=scale*w, height=scale*w*.22, color=GAMMA,
                            stroke_opacity=.25+.12*i, stroke_width=2).move_to(c)
                    for i,w in enumerate([3.2,2.6,2.0,1.45])])
    core = Circle(radius=.28*scale, fill_color='#02040A', fill_opacity=1,
                  color=LIGHT, stroke_opacity=.5).move_to(c)
    jets = VGroup(Line(c+UP*.25*scale,c+UP*1.65*scale,color=OBS,stroke_width=5),
                  Line(c+DOWN*.25*scale,c+DOWN*1.65*scale,color=OBS,stroke_width=5))
    return VGroup(glow,disk,jets,core)


def medal(center=(0,1.5,0), scale=1):
    return VGroup(Circle(radius=1.0*scale,color=LIGHT,fill_color='#6B4E1E',fill_opacity=.78,stroke_width=4),
                  txt('NOBEL',.2,27*scale,LIGHT),txt('2026',-.38,39*scale,LIGHT)).move_to(center)


def card(label, sub, x, color):
    box=RoundedRectangle(width=3.65,height=2.45,corner_radius=.22,color=color,
                         fill_color=color,fill_opacity=.055)
    return VGroup(box,txt(label,.35,30,color,3.2),txt(sub,-.48,22,LIGHT,3.15)).move_to([x,.8,0])


def messenger_icon(kind, center, color):
    c=np.array(center,dtype=float)
    ring=Circle(radius=.75,color=color,fill_color=color,fill_opacity=.05).move_to(c)
    if kind=='light':
        symbol=VGroup(*[Line(c+np.array([-0.48,y,0]),c+np.array([.48,y,0]),color=color,stroke_width=2)
                        for y in (-.18,0,.18)])
    elif kind=='wave':
        symbol=ParametricFunction(lambda t:c+np.array([t,.2*np.sin(9*t),0]),t_range=[-.5,.5],color=color)
    else:
        symbol=VGroup(Line(c+LEFT*.46,c+RIGHT*.46,color=color,stroke_width=3),Dot(c,radius=.075,color=color))
    return VGroup(ring,symbol)


class NeutrinoTelescopeDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def construct(self):
        self.brand=txt('과학의 한 장면  /  Nobel 02',7.1,22,'#9BA9C3');self.add(self.brand)

        self.cue('검출기를 만든 것이, 왜 노벨상일까?', '뉴트리노는 이미 알려진 입자였습니다.\n그런데 왜 IceCube가 노벨상일까요?')
        cube=detector_array((-1.45,.9,0),.48); prize=medal((2,1.15,0),.72)
        self.beat(.2,FadeIn(cube),FadeIn(prize))
        neq=Text('≠',font='Cambria',font_size=58,color=CRAY).move_to([.4,1,0]);self.beat(.13,FadeIn(neq))
        self.add(txt('새 입자의 발견?',-1.65,34,CRAY),txt('질문은 “무엇을 새로 볼 수 있게 됐나?”',-3.15,29,LIGHT))
        self.finish()

        self.cue('공식 수상 사유에는, 두 축이 있다', '검출기를 현실로 만든 기여와\n고에너지 천체 뉴트리노의 발견입니다.')
        left=card('IceCube','결정적 기여',-2.05,ICE);right=card('DISCOVERY','천체 기원의\n고에너지 ν',2.05,OBS)
        self.beat(.18,FadeIn(left));self.beat(.18,FadeIn(right))
        bridge=DoubleArrow([-.65,.8,0],[.65,.8,0],buff=0,color=LIGHT,stroke_width=2)
        self.beat(.13,Create(bridge))
        self.add(txt('instrument  +  observation',-1.45,31,LIGHT),
                 txt('둘 중 하나만의 상이 아닙니다.',-3.15,25,'#9BA9C3'))
        self.finish()

        self.cue('빛과 우주선에는, 서로 다른 한계', '빛은 가려진 곳에서 흡수될 수 있고\n하전 우주선은 자기장에 휘어집니다.')
        src=accelerator((-2.75,1.25,0),.75);target=earth((3.1,1.2,0),.58);self.add(src,target)
        photon=Line([-2.2,1.65,0],[.35,1.65,0],color=GAMMA,stroke_width=4)
        cloud=VGroup(*[Circle(radius=r,stroke_width=0,fill_color=GAS,fill_opacity=.035).move_to([.55,1.65,0]) for r in (.8,.6,.4)])
        cosmic=CubicBezier([-2.2,.65,0],[-.4,.2,0],[.8,2.6,0],[2.65,.65,0]).set_color(CRAY).set_stroke(width=4)
        self.beat(.18,Create(photon),FadeIn(cloud));self.beat(.22,Create(cosmic))
        self.add(txt('γ  absorbed / reprocessed',-1.55,23,GAMMA),txt('charged cosmic ray  ·  direction changed',-2.55,22,CRAY),
                 txt('출발점을 거꾸로 찾기 어렵습니다.',-3.65,27,LIGHT))
        self.finish()

        self.cue('뉴트리노는, 출발 방향을 지킨다', '전하가 없고 거의 반응하지 않아\n먼 거리에서도 정보를 비교적 잘 보존합니다.')
        src=accelerator((-2.9,1.2,0),.72);target=earth((3.1,1.2,0),.58);self.add(src,target)
        path=Line([-2.25,1.2,0],[2.55,1.2,0],color=OBS,stroke_width=4)
        particle=Dot(path.get_start(),radius=.08,color=OBS);self.add(particle)
        self.beat(.52,MoveAlongPath(particle,path),Create(path),rate_func=linear)
        self.add(txt('ν  ·  no electric charge',-.55,28,OBS),
                 txt('source direction',-2,25,LIGHT).shift(LEFT*2.2),txt('arrival direction',-2,25,LIGHT).shift(RIGHT*2.2),
                 txt('우주의 극한 환경이 보낸 messenger',-3.45,29,OBS))
        self.finish()

        self.cue('장점이 그대로, 검출의 약점이 된다', '우주를 쉽게 통과한다는 것은\n검출기도 쉽게 통과한다는 뜻입니다.')
        top=Arrow([-3.3,2.65,0],[3.25,2.65,0],buff=0,color=OBS,stroke_width=4)
        bottom=Arrow([-3.3,.8,0],[3.25,.8,0],buff=0,color=CRAY,stroke_width=4)
        self.add(txt('through the universe',3.45,25,OBS),txt('through the detector',1.6,25,CRAY))
        self.beat(.2,GrowArrow(top));self.beat(.2,GrowArrow(bottom))
        cube=detector_array((0,-1.5,0),.43);self.beat(.18,FadeIn(cube))
        self.add(txt('rare × enormous volume',-3.15,31,LIGHT),txt('Antarctic ice  ·  1 km³',-4.05,25,ICE))
        self.finish()

        self.cue('우주 뉴트리노 자체가, 처음은 아니다', '태양과 초신성은 이미 관측됐습니다.\nIceCube는 훨씬 높은 에너지 영역을 열었습니다.')
        line=Line([-3.5,1,0],[3.5,1,0],color='#71809B',stroke_width=3);self.add(line)
        items=[(-2.8,'1956','ν 검출',LIGHT),(-.9,'1987','SN 1987A',GAMMA),(.9,'2002','Nobel',MASS),(2.8,'2013','high-energy\ncosmic ν',OBS)]
        for i,(x,year,label,color) in enumerate(items):
            self.beat(.085,FadeIn(Dot([x,1,0],radius=.09,color=color)),FadeIn(txt(year,1.65,27,color).shift(RIGHT*x)),
                      FadeIn(txt(label,.15,22,color,1.5).shift(RIGHT*x)))
        self.add(txt('태양·초신성 ν',-1.4,25,LIGHT).shift(LEFT*1.65),
                 Arrow([-.3,-1.4,0],[1.8,-1.4,0],buff=0,color=OBS,stroke_width=3),
                 txt('더 높은 에너지의 우주',-1.4,25,OBS).shift(RIGHT*2.6),
                 txt('“뉴트리노 발견”이 아니라 관측 가능한 에너지 창의 확장',-3.55,23,'#9BA9C3'))
        self.finish()

        self.cue('검출기와 관측이, 새 천문학을 연다', 'LIGO가 중력파 천문학을 열었듯\nIceCube는 고에너지 뉴트리노 천문학을 열었습니다.')
        self.add(txt('LIGO',3.3,31,LIGHT).shift(LEFT*2),txt('IceCube',3.3,31,ICE).shift(RIGHT*2))
        left=VGroup(messenger_icon('wave',[-2,1.6,0],MASS),txt('gravitational waves',.25,22,MASS).shift(LEFT*2))
        right=VGroup(messenger_icon('nu',[2,1.6,0],OBS),txt('high-energy neutrinos',.25,22,OBS).shift(RIGHT*2))
        self.beat(.18,FadeIn(left),FadeIn(right))
        for x,color in [(-2,MASS),(2,OBS)]:
            self.beat(.12,GrowArrow(Arrow([x,-.45,0],[x,-1.35,0],buff=0,color=color)))
        self.add(txt('detector + signal',-2.05,23,LIGHT,2.8).shift(LEFT*2),
                 txt('detector + signal',-2.05,23,LIGHT,2.8).shift(RIGHT*2),
                 txt('NEW ASTRONOMY',-3.45,40,GREEN))
        self.finish()

        self.cue('검출기는 목적이 아니라, 새로운 창', '빛만으로 볼 수 없던 극한의 우주를\n뉴트리노로 보게 만든 것이 핵심입니다.')
        stars=starfield(22,50);self.add(stars)
        source=accelerator((0,2.25,0),.62);self.beat(.15,FadeIn(source))
        icons=VGroup(messenger_icon('light',[-2.1,-.15,0],GAMMA),messenger_icon('wave',[0,-.15,0],MASS),
                     messenger_icon('nu',[2.1,-.15,0],OBS));self.beat(.16,FadeIn(icons))
        self.add(txt('빛',-1.2,23,GAMMA).shift(LEFT*2.1),txt('중력파',-1.2,23,MASS),txt('뉴트리노',-1.2,23,OBS).shift(RIGHT*2.1))
        self.beat(.14,FadeIn(txt('검출기의 발명  ≠  목적',-2.35,31,CRAY)))
        self.beat(.14,FadeIn(txt('보이지 않던 우주를 보는 것  =  목적',-3.35,32,LIGHT)))
        self.add(txt('2026 NOBEL PRIZE IN PHYSICS',-4.35,25,ICE))
        self.finish()
