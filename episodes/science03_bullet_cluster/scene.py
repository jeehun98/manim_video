"""Collision separates the X-ray gas peaks from the lensing mass peaks."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import GravitationalLensingDiscovery, txt, LIGHT, OBS, MASS

GAS = '#FF8EAE'
Y = .65

def galaxies(x, small=False):
    rng=np.random.default_rng(74 if small else 18)
    return VGroup(*[Dot([x+dx,Y+dy,0],radius=.036+(.012 if i%4==0 else 0),color=LIGHT)
                   for i,(dx,dy) in enumerate(rng.normal(0,[.4,.53],size=(16 if small else 23,2)))])

def cloud(x, small=False):
    size=.8 if small else 1
    g=VGroup(*[Ellipse(width=2.25*r*size,height=2.8*r*size,stroke_width=0,
                       fill_color=GAS,fill_opacity=.038) for r in np.linspace(1,.12,15)])
    return g.move_to([x,Y,0])

def mass(x, small=False):
    size=.8 if small else 1
    g=VGroup(*[Ellipse(width=3.05*r*size,height=3.55*r*size,stroke_width=0,
                       fill_color=MASS,fill_opacity=.023) for r in np.linspace(1,.1,15)])
    g.add(Ellipse(width=3.05*size,height=3.55*size,color=MASS,stroke_opacity=.55,stroke_width=1.5))
    return g.move_to([x,Y,0])

def cross(x,color):
    p=np.array([x,Y,0])
    return VGroup(Line(p+[-.13,0,0],p+[.13,0,0],color=color),Line(p+[0,-.13,0],p+[0,.13,0],color=color))

class BulletClusterDiscovery(GravitationalLensingDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def after(self, show_mass=False):
        stars=VGroup(galaxies(2.55),galaxies(-2.55,True))
        gas=VGroup(cloud(-.65),cloud(.6,True))
        halos=VGroup(mass(2.55),mass(-2.55,True))
        self.add(gas)
        if show_mass:self.add(halos)
        self.add(stars)
        return stars,gas,halos

    def construct(self):
        self.brand=txt('과학의 한 장면  /  03',7.1,23,'#9BA9C3')
        self.add(self.brand)
        self.cue('가스와 질량은\n왜 서로 다른 곳에 있을까?', '두 은하단이 충돌했습니다.\n그런데 가스와 질량의 중심이 서로 다릅니다.')
        a,b=galaxies(-2.7),galaxies(2.7,True)
        ga,gb=cloud(-2.7),cloud(2.7,True)
        ma,mb=mass(-2.7),mass(2.7,True)
        self.beat(.15,FadeIn(VGroup(ma,mb,ga,gb,a,b)))
        legends=VGroup(txt('은하',-2.45,23,LIGHT).shift(LEFT*2.4),txt('뜨거운 가스',-2.45,23,GAS),txt('질량 모형',-2.45,23,MASS).shift(RIGHT*2.5))
        collision_note=txt('Bullet Cluster · 충돌 과정의 개념도',-3.65,23,'#A9B8CB')
        self.add(legends,collision_note)
        self.finish()

        self.cue('보통 물질의 질량은 가스에 더 많다', '은하단의 보통 물질에서는, 별보다\n뜨거운 가스가 훨씬 많은 질량을 차지합니다.',clear=False)
        self.beat(.08,FadeOut(legends),FadeOut(collision_note))
        ordinary_label=txt('보통 물질의 질량 비교',-1.9,25)
        star_bar=Rectangle(width=.9,height=.22,stroke_width=0,fill_color=LIGHT,fill_opacity=.9).move_to([-2.55,-2.8,0])
        gas_bar=Rectangle(width=3.6,height=.22,stroke_width=0,fill_color=GAS,fill_opacity=.85).move_to([-1.2,-3.65,0])
        comparison=VGroup(ordinary_label,star_bar,gas_bar,txt('별',-2.4,23,LIGHT),txt('뜨거운 가스',-3.25,23,GAS),txt('막대는 질량의 상대적 크기만 표현한 개념도',-4.35,20,'#A9B8CB'))
        self.beat(.2,FadeIn(comparison))
        self.beat(.12,Indicate(gas_bar,color=GAS))
        self.to(self.current['start_frame']+round(self.span_frames*.67))
        self.beat(.08,FadeOut(comparison))
        self.add(collision_note)
        self.beat(.18,*[m.animate.shift(RIGHT*1.6) for m in (a,ga,ma)],*[m.animate.shift(LEFT*1.6) for m in (b,gb,mb)],rate_func=linear)
        self.finish()

        self.cue('은하는 지나가고, 가스는 늦어진다', '은하들은 대부분 서로 비껴 지나가지만,\n가스는 충돌하며 압축되고 느려집니다.',clear=False)
        self.beat(.4,a.animate.shift(RIGHT*3.65),ma.animate.shift(RIGHT*3.65),b.animate.shift(LEFT*3.65),mb.animate.shift(LEFT*3.65),
                  ga.animate.move_to([-.65,Y,0]).stretch(.7,0),gb.animate.move_to([.6,Y,0]).stretch(.7,0),rate_func=linear)
        compression=VGroup(Arrow([-1.65,-1.4,0],[-.2,-1.4,0],color=GAS,buff=.1),Arrow([1.65,-1.4,0],[.2,-1.4,0],color=GAS,buff=.1))
        self.beat(.15,GrowArrow(compression[0]),GrowArrow(compression[1]))
        self.beat(.1,FadeOut(VGroup(ma,mb)),FadeOut(compression))
        self.finish()

        self.cue('보통 물질의 큰 부분은 가스', '질량이 보통 물질뿐이라면,\n질량도 가스 쪽에 많이 모여 있어야 합니다.')
        stars,gas,_=self.after()
        self.beat(.2,Indicate(gas,color=GAS,scale_factor=1.06))
        self.beat(.15,FadeIn(txt('X-ray gas',-2.4,30,GAS)),FadeIn(txt('분홍색: X선으로 관측한 뜨거운 가스',-3.25,23,GAS)))
        self.add(txt('보통 물질만 있다면: 질량도 가스 쪽에',-4.2,24,GAS))
        self.finish()

        self.cue('그런데 질량의 중심은?', '배경 은하의 왜곡으로 질량을 복원하면,\n주된 질량 피크는 가스에서 어긋나 있습니다.')
        stars,gas,halos=self.after()
        marks=VGroup()
        for x in (-2.55,2.55):
            for angle in np.linspace(0,TAU,12,endpoint=False):
                pos=np.array([x+1.3*np.cos(angle),Y+1.9*np.sin(angle),0])
                tangent=np.array([-np.sin(angle),np.cos(angle),0])
                marks.add(Line(pos-.13*tangent,pos+.13*tangent,color=OBS,stroke_width=3))
        self.beat(.17,LaggedStart(*[Create(m) for m in marks],lag_ratio=.02))
        self.beat(.3,FadeIn(halos),marks.animate.set_opacity(.35))
        self.beat(.12,FadeIn(cross(-2.55,MASS)),FadeIn(cross(2.55,MASS)),FadeIn(txt('중력렌즈로 추론한 총질량',-3.2,27,MASS)))
        self.add(txt('배경 은하의 왜곡 → 하늘에 투영된 질량 지도',-4.15,22,OBS))
        self.finish()

        self.cue('두 지도의 중심이 어긋난다', '보통 물질의 대부분을 차지하는 가스와,\n중력으로 추론한 질량의 중심이 다릅니다.')
        stars,gas,halos=self.after()
        self.beat(.18,FadeIn(txt('X선 가스 지도',-2.4,26,GAS)))
        self.beat(.25,FadeIn(halos),FadeIn(txt('중력렌즈 질량 지도',-3.1,26,MASS)))
        gas_peaks=VGroup(cross(-.65,GAS),cross(.6,GAS))
        mass_peaks=VGroup(cross(-2.55,MASS),cross(2.55,MASS))
        offsets=VGroup(DashedLine([-2.55,Y,0],[-.65,Y,0],color=WHITE),DashedLine([.6,Y,0],[2.55,Y,0],color=WHITE))
        self.beat(.15,FadeIn(gas_peaks),FadeIn(mass_peaks),Create(offsets))
        self.beat(.12,FadeIn(txt('가스의 중심  ≠  질량의 중심',-4.15,31)))
        self.finish()

        self.cue('무엇이 가스를 따라오지 않았을까?', '질량의 큰 부분은 가스처럼 충돌해 늦어지지 않고,\n은하들과 함께 지나간 것으로 보입니다.')
        stars,gas,halos=self.after(True)
        self.beat(.16,stars[0].animate.shift(LEFT*5.25),halos[0].animate.shift(LEFT*5.25),stars[1].animate.shift(RIGHT*5.25),halos[1].animate.shift(RIGHT*5.25),
                  gas[0].animate.move_to([-2.7,Y,0]),gas[1].animate.move_to([2.7,Y,0]))
        replay_label=txt('충돌 전으로 되돌려 보면',-2.8,25,'#A9B8CB')
        self.add(replay_label)
        self.beat(.48,FadeOut(replay_label),stars[0].animate.shift(RIGHT*5.25),halos[0].animate.shift(RIGHT*5.25),stars[1].animate.shift(LEFT*5.25),halos[1].animate.shift(LEFT*5.25),
                  gas[0].animate.move_to([-.65,Y,0]).stretch(.7,0),gas[1].animate.move_to([.6,Y,0]).stretch(.7,0),rate_func=linear)
        self.add(txt('같은 충돌을 다시 따라가면',-2.8,25,'#A9B8CB'))
        self.beat(.1,FadeIn(txt('가스는 뒤처지고  ·  질량은 은하와 함께',-3.65,27,MASS)))
        self.finish()

        self.cue('가스와 분리된 질량 성분', '은하 쪽의 별 질량만으로는 부족합니다.\n그곳에 보이지 않는 큰 질량이 함께 있습니다.')
        stars,gas,halos=self.after(True)
        self.beat(.25,Indicate(halos[0],color=MASS,scale_factor=1.06),Indicate(halos[1],color=MASS,scale_factor=1.06))
        star_mass=Rectangle(width=.8,height=.22,stroke_width=0,fill_color=LIGHT,fill_opacity=.85).move_to([-2.6,-2.05,0])
        lens_mass=Rectangle(width=3.5,height=.22,stroke_width=0,fill_color=MASS,fill_opacity=.85).move_to([-1.25,-3.05,0])
        self.beat(.15,FadeIn(star_mass),FadeIn(lens_mass),FadeIn(txt('은하 쪽의 별 질량',-1.65,23,LIGHT)),FadeIn(txt('그곳의 렌즈 질량',-2.65,23,MASS)))
        self.add(txt('막대 길이는 설명용 · 실제 수치 아님',-3.65,20,'#A9B8CB'))
        self.beat(.12,FadeIn(txt('Dark Matter',-4.35,35,MASS)))
        self.finish()

        self.cue('단서는 양뿐 아니라, 위치', '가스의 중심과 질량의 중심이 어긋나 있습니다.\n충돌이 드러낸 암흑물질의 단서입니다.')
        stars,gas,halos=self.after(True)
        self.add(txt('질량 / 은하',-1.75,23,MASS).shift(LEFT*2.65),txt('뜨거운 가스',-1.75,23,GAS),txt('질량 / 은하',-1.75,23,MASS).shift(RIGHT*2.65))
        self.beat(.15,FadeIn(txt('Bullet Cluster',-2.9,32,OBS)))
        self.beat(.18,FadeIn(txt('가스의 중심  ≠  질량의 중심',-3.9,33)))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)])
        self.finish()
