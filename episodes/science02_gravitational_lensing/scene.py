"""Light distortion -> projected total mass -> unseen mass."""
import json
import os
from pathlib import Path
import numpy as np
from manim import *

config.pixel_width = int(os.environ.get('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.environ.get('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#080E1B'
LIGHT, EXPECT, OBS, MASS, GAS = '#F9DE9C', '#FF978D', '#62DCEC', '#8F9CFF', '#A9B8CB'

def txt(s, y=0, size=30, color=WHITE, width=7.8):
    m = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.25)
    if m.width > width: m.scale_to_fit_width(width)
    return m.move_to([0,y,0])

def galaxy(pos, scale=.35, color=LIGHT):
    g = VGroup(*[Ellipse(width=1.2*r,height=.55*r,stroke_width=0,
                         fill_color=color,fill_opacity=.07) for r in (1.5,1.2,.9,.6)])
    g.add(Ellipse(width=.6,height=.17,fill_color=color,fill_opacity=.8,stroke_width=0),Dot(radius=.05,color=color))
    return g.scale(scale).move_to(pos)

def cluster(pos=ORIGIN, scale=1):
    offsets = [(-.55,.4),(.45,.6),(-.7,-.45),(.55,-.35),(0,0)]
    gas = VGroup(*[Ellipse(width=2*r,height=1.6*r,stroke_width=0,fill_color=GAS,fill_opacity=.025) for r in (1,.8,.6)])
    stars = VGroup(*[galaxy([x,y,0],.32).rotate(i*.6) for i,(x,y) in enumerate(offsets)])
    return VGroup(gas,stars).scale(scale).move_to(pos)

def haze(pos=ORIGIN, scale=1):
    return VGroup(*[Ellipse(width=5*r,height=4.1*r,stroke_width=0,
                            fill_color=MASS,fill_opacity=.025) for r in np.linspace(1,.1,18)]).scale(scale).move_to(pos)

def ray(sign=1, amount=1.35, y=.6, color=OBS):
    return ParametricFunction(lambda t: np.array([-3.35+6.7*t,y+sign*amount*np.sin(PI*t),0]),
                              t_range=[0,1],color=color,stroke_width=3)

def image_arcs(center=np.array([0,.6,0])):
    return VGroup(*[Arc(radius=r,start_angle=a,angle=b,arc_center=center,color=OBS,stroke_width=w)
                    for r,a,b,w in [(2.0,.25,1.15,9),(1.7,3.45,.8,7),(2.45,5.05,.55,5)]])

class GravitationalLensingDiscovery(Scene):
    TIMING = json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION = TIMING['duration']

    def beat(self, fraction, *animations, **kwargs):
        frames = max(1,round(self.span_frames*fraction))
        self.play(*animations,run_time=frames/30,**kwargs)

    def to(self, frame):
        remaining = frame-round(self.time*30)
        if remaining < 0: raise RuntimeError(f'Cue overrun at {self.time}: target {frame/30}')
        if remaining: self.wait(remaining/30)

    def cue(self, title, caption, clear=True):
        self.index = getattr(self,'index',-1)+1
        self.current = self.TIMING['cues'][self.index]
        self.span_frames = self.current['end_frame']-self.current['start_frame']
        self.to(self.current['start_frame'])
        new = VGroup(txt(title,5.65,36),txt(caption,-5.8,27))
        animations = [FadeIn(new)]
        if hasattr(self,'words'): animations.append(FadeOut(self.words))
        if clear:
            animations += [FadeOut(m) for m in list(self.mobjects) if m is not self.brand and m is not getattr(self,'words',None)]
        self.beat(.07,*animations)
        self.words = new

    def finish(self): self.to(self.current['end_frame'])

    def construct(self):
        self.brand = txt('과학의 한 장면  /  02',7.1,23,'#9BA9C3')
        self.add(self.brand)
        self.cue('보이지 않는 질량은\n어떻게 찾을까?', '멀리 있는 은하에서, 우리에게 오는 빛.')
        source = galaxy([-3.35,.6,0],.6,OBS)
        eye = VGroup(Ellipse(width=.6,height=.35,color=WHITE),Dot(radius=.07)).move_to([3.35,.6,0])
        labels = VGroup(txt('배경 은하',-1.15,22,OBS).shift(LEFT*3),txt('관측자',-1.15,22).shift(RIGHT*3))
        straight = Line(source.get_center(),eye.get_center(),color=OBS)
        self.beat(.15,FadeIn(source),FadeIn(eye),FadeIn(labels))
        self.beat(.25,Create(straight))
        photon = Dot(source.get_center(),radius=.06,color=WHITE)
        self.add(photon)
        self.beat(.3,MoveAlongPath(photon,straight),rate_func=linear)
        self.remove(photon)
        self.finish()

        self.cue('질량이 있으면, 빛의 길도', '질량이 휘게 만든 시공간을 따라\n빛의 경로가 부드럽게 휘어집니다.',clear=False)
        lens = cluster([0,.6,0],.85)
        upper,lower = ray(),ray(-1)
        self.beat(.15,FadeIn(lens),FadeOut(straight))
        self.beat(.25,Create(upper),Create(lower))
        grid = VGroup(*[ParametricFunction(lambda t,y=y: np.array([t,.6+y*(1-.25*np.exp(-t*t)),0]),t_range=[-2.4,2.4],color=MASS,stroke_opacity=.15) for y in np.linspace(-2,2,9)])
        self.beat(.12,Create(grid))
        photons = VGroup(Dot(upper.get_start(),radius=.06),Dot(lower.get_start(),radius=.06))
        self.add(photons)
        self.beat(.25,MoveAlongPath(photons[0],upper),MoveAlongPath(photons[1],lower),rate_func=linear)
        self.add(txt('옆에서 본 경로 · 개념도',-3.6,22,GAS))
        self.finish()

        self.cue('하나의 은하, 여러 모습', '뒤에 있는 은하가 호처럼 늘어나거나,\n여러 개의 상으로 보이기도 합니다.')
        lens = cluster([0,.6,0],.85)
        original = galaxy([0,2.7,0],.6,OBS)
        arcs = image_arcs()
        self.beat(.15,FadeIn(lens),FadeIn(original))
        self.beat(.35,ReplacementTransform(original,arcs))
        self.beat(.1,FadeIn(txt('Gravitational Lensing',-3.25,29,OBS)))
        self.add(txt('관측자 시점 · 중력렌즈',-4,23,GAS))
        self.finish()

        self.cue('별과 가스만으로 충분할까?', '보통 물질의 질량을 모두 합쳐도,\n관측된 왜곡을 설명하기엔 부족합니다.')
        lens = cluster([0,.6,0],.85)
        weak = VGroup(ray(1,.45,color=EXPECT),ray(-1,.45,color=EXPECT))
        strong = VGroup(ray(1,1.6),ray(-1,1.6))
        self.add(lens,galaxy([-3.35,.6,0],.45,OBS),Dot([3.35,.6,0],color=WHITE))
        self.beat(.2,Create(weak),FadeIn(txt('별 + 가스의 질량으로 예상',-2.45,25,EXPECT)))
        self.beat(.3,Create(strong),FadeIn(txt('관측된 왜곡에 필요한 휘어짐',-3.2,25,OBS)))
        self.beat(.12,Indicate(strong))
        self.add(txt('경로 비교는 설명용 개념도',-4,21,GAS))
        self.finish()

        self.cue('빛의 왜곡에서 질량을 거꾸로', '여러 배경 은하의 왜곡 패턴을 모아,\n필요한 질량 분포를 거꾸로 추론합니다.')
        rng = np.random.default_rng(22)
        galaxies,marks = VGroup(),VGroup()
        for i,a in enumerate(np.linspace(0,TAU,24,endpoint=False)):
            r = 2.1 + .7*rng.random()
            pos = np.array([r*np.cos(a),.75+r*np.sin(a),0])
            tangent = a+PI/2
            galaxies.add(galaxy(pos,.27,OBS).rotate(tangent))
            marks.add(Line(pos-.19*np.array([np.cos(tangent),np.sin(tangent),0]),pos+.19*np.array([np.cos(tangent),np.sin(tangent),0]),color=OBS,stroke_width=4))
        self.beat(.15,LaggedStart(*[FadeIn(g) for g in galaxies],lag_ratio=.025))
        self.beat(.18,ReplacementTransform(galaxies,marks))
        self.add(txt('여러 은하의 평균 왜곡 패턴',-3.1,23,OBS))
        self.beat(.1,Indicate(marks))
        cells = VGroup()
        for x in np.linspace(-1.9,1.9,13):
            for y in np.linspace(-1.65,1.65,11):
                strength=np.exp(-((x/.95)**2+(y/1.2)**2)/2)
                cells.add(Square(side_length=.3,stroke_width=0,fill_color=MASS,fill_opacity=.65*strength).move_to([x,y+.75,0]))
        self.beat(.25,LaggedStart(*[FadeIn(c) for c in cells],lag_ratio=.003),marks.animate.set_opacity(.45))
        self.beat(.1,FadeIn(txt('왜곡 패턴  →  총질량 지도',-4,28,MASS)))
        self.add(txt('하늘에 투영된 분포 · 복원 과정의 개념도',4,21,GAS))
        self.finish()

        self.cue('지도에 드러난 추가 질량', '별과 가스의 질량을 합친 것보다\n더 많은 질량이 필요합니다.')
        ordinary = cluster([0,1.2,0],1)
        mass = haze([0,1.2,0])
        self.beat(.18,FadeIn(ordinary))
        self.beat(.25,FadeIn(mass,scale=.4))
        self.bring_to_front(ordinary)
        bars = VGroup(Rectangle(width=1.1,height=.25,fill_color=LIGHT,fill_opacity=.8,stroke_width=0).move_to([-1.5,-2.4,0]),Rectangle(width=4,height=.25,fill_color=MASS,fill_opacity=.8,stroke_width=0).move_to([-.05,-3.4,0]))
        self.beat(.15,FadeIn(bars),FadeIn(txt('별 + 가스',-1.95,23,LIGHT)),FadeIn(txt('렌즈로 추론한 총질량',-2.95,23,MASS)))
        self.add(txt('막대 길이와 지도 색은 설명용 · 실제 수치 아님',-4.15,20,GAS))
        self.finish()

        self.cue('같은 은하단, 두 가지 단서', '보이지 않아도 질량이 있다면,\n뒤에서 오는 빛에 흔적을 남깁니다.')
        left,right=np.array([-2.05,.6,0]),np.array([2.05,.6,0])
        a,b=cluster(left,.65),cluster(right,.65)
        h=haze(right,.7)
        self.beat(.2,FadeIn(a),FadeIn(b))
        self.beat(.25,FadeIn(h),FadeIn(image_arcs(right).scale(.65,about_point=right)))
        self.bring_to_front(b)
        self.add(txt('빛으로 본 모습',-2,25,LIGHT).shift(LEFT*2.05),txt('렌즈로 추론한 질량',-2,25,MASS).shift(RIGHT*2.05))
        self.beat(.12,FadeIn(txt('별의 운동  →  질량\n빛의 왜곡  →  질량',-3.8,28,OBS)))
        self.finish()

        self.cue('빛이 지나간 길에 남은 흔적', '암흑물질은 빛을 내지 않지만,\n빛의 왜곡에 질량의 흔적을 남깁니다.')
        arc = Arc(radius=2.1,start_angle=.2,angle=1.55,arc_center=np.array([0,.6,0]),color=OBS,stroke_width=10)
        h=haze([0,.6,0])
        self.beat(.15,Create(arc))
        self.beat(.23,FadeIn(h))
        self.beat(.12,FadeIn(txt('Dark Matter',-2.8,39,MASS)),FadeIn(txt('빛의 왜곡이 남긴 단서',-3.65,29,OBS)))
        self.to(self.current['end_frame']-round(self.span_frames*.08))
        self.beat(.08,*[FadeOut(m) for m in list(self.mobjects)])
        self.finish()
