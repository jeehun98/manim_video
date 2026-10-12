"""Spacetime strain -> optical phase shift -> gravitational-wave signal."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,OBS,MASS,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery
from episodes.science11_icecube_neutrino.scene import earth,starfield,ICE

LASER='#FF5C68';WAVE='#9B8CFF';GRID='#35506F';SIGNAL='#71E5A5';GOLD='#FFD17A'

def grid(center=(0,1,0),sx=1,sy=1,width=7.2,height=6.2):
    c=np.array(center,dtype=float);g=VGroup()
    for x in np.linspace(-width/2,width/2,13):g.add(Line(c+[x*sx,-height/2*sy,0],c+[x*sx,height/2*sy,0],color=GRID,stroke_opacity=.35,stroke_width=1))
    for y in np.linspace(-height/2,height/2,11):g.add(Line(c+[-width/2*sx,y*sy,0],c+[width/2*sx,y*sy,0],color=GRID,stroke_opacity=.35,stroke_width=1))
    return g

def black_holes(separation=2.5,angle=0,center=(0,1,0),scale=1):
    c=np.array(center,dtype=float);v=np.array([np.cos(angle),np.sin(angle),0])*separation/2
    group=VGroup()
    for p in (c-v,c+v):
        glow=VGroup(*[Circle(radius=scale*r,stroke_width=0,fill_color=WAVE,fill_opacity=.018).move_to(p) for r in np.linspace(.9,.25,6)])
        disk=Ellipse(width=1.25*scale,height=.25*scale,color=GOLD,stroke_opacity=.75).move_to(p).rotate(angle)
        hole=Circle(radius=.28*scale,fill_color='#010208',fill_opacity=1,color=LIGHT,stroke_opacity=.5).move_to(p)
        group.add(glow,disk,hole)
    return group

def ripples(center=(0,1,0),count=5):
    return VGroup(*[Circle(radius=.8+i*.65,color=WAVE,stroke_opacity=.55-.07*i,stroke_width=2).move_to(center) for i in range(count)])

def mirror(pos,vertical=False):
    m=Rectangle(width=.16 if vertical else .7,height=.7 if vertical else .16,color=LIGHT,fill_color=LIGHT,fill_opacity=.65,stroke_width=1).move_to(pos)
    return m

def ligo_layout(x_scale=1,y_scale=1,center=(-1.4,-.5,0),arm=4.2):
    c=np.array(center,dtype=float);right=c+RIGHT*arm*x_scale;top=c+UP*arm*y_scale
    arms=VGroup(Line(c,right,color=GAS,stroke_width=10,stroke_opacity=.32),Line(c,top,color=GAS,stroke_width=10,stroke_opacity=.32))
    tubes=VGroup(Line(c,right,color=LIGHT,stroke_width=2,stroke_opacity=.7),Line(c,top,color=LIGHT,stroke_width=2,stroke_opacity=.7))
    splitter=Square(side_length=.38,color=GOLD,fill_color=GOLD,fill_opacity=.25).rotate(PI/4).move_to(c)
    laser=VGroup(Rectangle(width=.75,height=.42,color=LASER,fill_color=LASER,fill_opacity=.15),txt('LASER',0,17,LASER,.7)).move_to(c+LEFT*1.35)
    detector=VGroup(Rectangle(width=.8,height=.52,color=SIGNAL,fill_color=SIGNAL,fill_opacity=.05),txt('DET',0,17,SIGNAL,.7)).move_to(c+DOWN*1.25)
    return VGroup(arms,tubes,mirror(right,True),mirror(top),splitter,laser,detector),c,right,top

def sine_graph(y,phase=0,color=OBS,amp=.48,x0=-3.4,x1=3.4,cycles=5):
    return ParametricFunction(lambda t:np.array([t,y+amp*np.sin(cycles*TAU*(t-x0)/(x1-x0)+phase),0]),t_range=[x0,x1],color=color,stroke_width=3)

def chirp_graph(center=(0,.4,0),width=7,height=3.2):
    c=np.array(center,dtype=float);pts=[]
    for u in np.linspace(0,1,700):
        phase=TAU*(1.4*u+5.7*u**3);amp=.08+.72*u**2
        pts.append(c+np.array([(u-.5)*width,amp*np.sin(phase)*height/2,0]))
    return VMobject(color=OBS,stroke_width=3).set_points_as_corners(pts)

def telescope(center=(-2,1,0),color=GOLD):
    c=np.array(center,dtype=float)
    return VGroup(Arc(radius=.72,start_angle=-PI/3,angle=2*PI/3,color=color,stroke_width=5).move_to(c),
                  Line(c+[.35,-.6,0],c+[.95,-1.45,0],color=color,stroke_width=5),
                  Line(c+[.62,-1.15,0],c+[.2,-1.65,0],color=color),Line(c+[.62,-1.15,0],c+[1.12,-1.65,0],color=color))

def medal(center=(0,1,0)):
    return VGroup(Circle(radius=.9,color=GOLD,fill_color='#6B4E1E',fill_opacity=.75,stroke_width=4),txt('NOBEL',.18,25,GOLD),txt('2017',-.35,36,GOLD)).move_to(center)

class LIGOInterferometerDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
    def construct(self):
        self.brand=txt('과학의 한 장면  /  Nobel 03',7.1,22,'#9BA9C3');self.add(self.brand)

        self.cue('블랙홀의 공전이, 시공간을 흔든다','가까워질수록 더 빠르게 돌고\n흔들림은 빛의 속도로 퍼져나갑니다.')
        p=ValueTracker(0)
        holes=always_redraw(lambda:black_holes(2.8-1.45*p.get_value(),1.2+6*p.get_value(),(0,1.25,0),1-.15*p.get_value()))
        rings=always_redraw(lambda:ripples((0,1.25,0),5).set_opacity(.12+.65*p.get_value()))
        self.add(grid((0,1.25,0)),rings,holes);self.beat(.68,p.animate.set_value(1),rate_func=rush_into)
        self.add(txt('GRAVITATIONAL WAVES',-3.05,34,WAVE),txt('시공간의 흔들림',-4,26,LIGHT));self.finish()

        self.cue('지구에 도착하면, 거의 사라질 만큼 작다','우주를 건너온 흔들림은 극도로 작습니다.\n이 길이 변화를 어떻게 잴까요?')
        stars=starfield(31,55);self.add(stars);src=black_holes(.8,0,[-2.8,2.5,0],.55);globe=earth([2.8,-1.8,0],.58);self.add(src,globe)
        wave=VGroup(*[Arc(radius=r,start_angle=-1.2,angle=1.6,arc_center=[-2.8,2.5,0],color=WAVE,stroke_opacity=.7-r*.06) for r in np.linspace(.7,5.8,9)])
        self.beat(.45,Create(wave));self.beat(.12,Flash(globe,color=WAVE,flash_radius=.8))
        self.add(txt('1.3 billion light-years',-.2,25,'#9BA9C3'),txt('거의 0처럼 작은 strain',-3.45,31,LIGHT));self.finish()

        self.cue('두 개의 4 km 팔, 하나의 레이저','직교한 두 통로로 레이저를 나눠\n서로 다른 방향으로 보냅니다.')
        layout,c,r,t=ligo_layout();self.add(layout)
        bx=Line(c,r,color=LASER,stroke_width=4);by=Line(c,t,color=LASER,stroke_width=4)
        self.beat(.18,Create(Line(c+LEFT*.95,c,color=LASER,stroke_width=4)));self.beat(.28,Create(bx),Create(by))
        self.add(txt('4 km',-.9,24,GOLD).shift(RIGHT*2.2),txt('4 km',2.1,24,GOLD).shift(LEFT*2.25),txt('beam splitter',-2.2,22,GOLD));self.finish()

        self.cue('거울까지 갔다가, 다시 중앙으로','두 빛은 각 팔의 끝에서 반사되어\n같은 빔 스플리터로 돌아옵니다.')
        layout,c,r,t=ligo_layout();self.add(layout)
        px=Dot(c,radius=.07,color=LASER);py=px.copy();self.add(px,py)
        self.beat(.28,px.animate.move_to(r),py.animate.move_to(t),rate_func=linear)
        self.beat(.28,px.animate.move_to(c),py.animate.move_to(c),rate_func=linear)
        self.add(txt('out  →  mirror  →  back',-3.15,30,LIGHT),txt('평소에는 두 왕복 경로가 거의 같습니다.',-4,23,'#9BA9C3'));self.finish()

        self.cue('같은 빛을, 반대 위상으로 겹친다','경로가 맞으면 두 빛이 거의 상쇄되어\n출력 포트는 어둡게 유지됩니다.')
        a=sine_graph(2.15,0,OBS);b=sine_graph(.65,PI,MASS);self.add(a,b)
        self.add(txt('E₁',2.95,26,OBS),txt('E₂',1.45,26,MASS))
        self.beat(.22,a.animate.shift(DOWN*.75),b.animate.shift(UP*.75))
        zero=Line([-3.4,-.7,0],[3.4,-.7,0],color=SIGNAL,stroke_width=4);self.beat(.2,Create(zero))
        self.add(txt('E₁ + E₂ ≈ 0',-1.55,40,LIGHT),VGroup(Circle(radius=.22,color=SIGNAL,fill_color=SIGNAL,fill_opacity=.04),txt('dark',0,17,SIGNAL)).move_to([0,-3,0]));self.finish()

        self.cue('중력파는 한쪽을 늘리고, 다른 쪽을 줄인다','가로가 늘어날 때 세로는 줄고,\n잠시 뒤에는 그 반대가 됩니다.')
        s=ValueTracker(0);g=always_redraw(lambda:grid((0,1,0),1+.12*s.get_value(),1-.12*s.get_value()))
        ring=always_redraw(lambda:Ellipse(width=3*(1+.16*s.get_value()),height=3*(1-.16*s.get_value()),color=WAVE).move_to([0,1,0]))
        self.add(g,ring);self.beat(.3,s.animate.set_value(1),rate_func=smooth);self.beat(.3,s.animate.set_value(-1),rate_func=smooth)
        self.add(txt('Lₓ ↑    Lᵧ ↓',-2.7,36,OBS),txt('⇄',-3.3,34,LIGHT),txt('Lₓ ↓    Lᵧ ↑',-3.9,36,MASS),txt('변형은 실제보다 크게 과장',-4.65,21,'#9BA9C3'));self.finish()

        self.cue('팔 길이 차이가, 위상 차이가 된다','두 빛의 왕복 거리가 달라지면\n돌아온 파동의 위치도 어긋납니다.')
        layout,c,r,t=ligo_layout(1.08,.93);self.add(layout)
        self.add(Line(c,r,color=LASER,stroke_width=4),Line(c,t,color=LASER,stroke_width=4))
        self.beat(.18,FadeIn(txt('longer',-.85,24,OBS).shift(RIGHT*2.3)),FadeIn(txt('shorter',2.15,24,MASS).shift(LEFT*2.15)))
        self.add(sine_graph(-2.25,0,OBS,amp=.3,x0=-3.3,x1=3.3),sine_graph(-3.05,PI+.55,MASS,amp=.3,x0=-3.3,x1=3.3))
        self.add(txt('ΔL  →  Δφ',-4.1,42,LIGHT));self.finish()

        self.cue('완전한 상쇄가 깨지면, 빛이 나타난다','미세한 위상차가 출력 포트의\n측정 가능한 빛 변화로 바뀝니다.')
        a=sine_graph(2.05,0,OBS);b=sine_graph(.65,PI+.55,MASS);self.add(a,b)
        self.beat(.2,a.animate.shift(DOWN*.7),b.animate.shift(UP*.7))
        residual=sine_graph(-.85,.2,SIGNAL,amp=.18,cycles=5);self.beat(.22,Create(residual))
        glow=VGroup(*[Circle(radius=r,stroke_width=0,fill_color=SIGNAL,fill_opacity=.025).move_to([0,-2.6,0]) for r in (.9,.65,.4)],Dot([0,-2.6,0],radius=.13,color=SIGNAL))
        self.beat(.18,FadeIn(glow),Flash([0,-2.6,0],color=SIGNAL,flash_radius=.7))
        self.add(txt('ΔL  →  Δφ  →  LIGHT SIGNAL',-3.85,31,LIGHT));self.finish()

        self.cue('4 km에서, 양성자보다 작은 변화','strain은 길이 변화의 비율입니다.\n대표 신호는 10⁻²¹ 수준이었습니다.')
        bar=Line([-3.3,2.4,0],[3.3,2.4,0],color=OBS,stroke_width=8);self.beat(.2,Create(bar))
        self.add(txt('L = 4 km',3.15,31,OBS),txt('h = ΔL / L',1.1,44,LIGHT),txt('h  ~  10⁻²¹',-.25,51,WAVE))
        proton=Circle(radius=.65,color=GOLD,fill_color=GOLD,fill_opacity=.08).move_to([-1.6,-2.25,0]);tiny=Line([1.15,-2.25,0],[1.18,-2.25,0],color=SIGNAL,stroke_width=8)
        self.add(proton,txt('proton',-3.15,22,GOLD).shift(LEFT*1.6),tiny,txt('ΔL',-3.15,22,SIGNAL).shift(RIGHT*1.2),txt('화면 비교도 실제 비율이 아닌 개념도',-4.25,21,'#9BA9C3'));self.finish()

        self.cue('2015년, 실제 chirp가 도착했다','느리던 진동이 점점 빠르고 강해진 뒤\n합병 순간을 지나 빠르게 잦아듭니다.')
        axes=Axes(x_range=[0,1,.2],y_range=[-1,1,.5],x_length=7,y_length=3.6,axis_config={'include_ticks':False,'color':'#71809B'}).move_to([0,.8,0]);self.add(axes)
        curve=chirp_graph((0,.8,0),7,3.5);self.beat(.63,Create(curve),rate_func=linear)
        self.add(txt('GW150914',3.45,31,LIGHT),txt('time  →',-1.7,24),txt('14 SEP 2015',-3.25,27,WAVE));self.finish()

        self.cue('파형은, 블랙홀의 운동을 기록한다','공전이 빨라질수록 주파수가 높아지고\n합병에서 가장 강한 신호가 납니다.')
        p=ValueTracker(0);holes=always_redraw(lambda:black_holes(3-2.1*p.get_value(),1+7*p.get_value(),[0,2.65,0],.7));self.add(holes)
        curve=chirp_graph((0,-.75,0),7,2.2);self.beat(.6,Create(curve),p.animate.set_value(1),rate_func=linear)
        merged=VGroup(*[Circle(radius=r,stroke_width=0,fill_color=WAVE,fill_opacity=.03).move_to([0,2.65,0]) for r in (.9,.65,.4)],Circle(radius=.35,fill_color='#010208',fill_opacity=1,color=LIGHT)).set_opacity(0)
        self.add(merged);self.beat(.12,holes.animate.set_opacity(0),merged.animate.set_opacity(1))
        self.add(txt('orbit faster  →  higher frequency',-3.05,29,LIGHT));self.finish()

        self.cue('우리가 본 것은, 빛이 아니다','LIGO는 전자기파가 아니라\n시공간의 흔들림 자체를 측정했습니다.')
        scope=telescope([-2.25,1.25,0],GOLD);layout,c,r,t=ligo_layout(.42,.42,[1.65,.25,0],2.9);layout.scale(.78,about_point=[1.65,.25,0]);self.add(scope,layout)
        star=Star(n=5,outer_radius=.25,inner_radius=.11,color=GOLD,fill_color=GOLD,fill_opacity=1).move_to([-2.25,3.25,0]);self.add(star)
        self.beat(.2,Create(Line(star.get_center(),[-2.25,1.8,0],color=GOLD,stroke_width=3)))
        waves=VGroup(*[Arc(radius=.35+i*.28,start_angle=-.45,angle=.9,arc_center=[1.65,3.2,0],color=WAVE) for i in range(5)]);self.beat(.2,Create(waves))
        self.add(txt('LIGHT',-2,31,GOLD).shift(LEFT*2.2),txt('SPACETIME',-2,31,WAVE).shift(RIGHT*2),txt('서로 다른 messenger',-3.35,29,LIGHT));self.finish()

        self.cue('전자기파 밖에, 새로운 관측 채널','빛의 파장만 바꾼 망원경이 아니라\n완전히 다른 정보를 받기 시작했습니다.')
        colors=[GOLD,OBS,MASS];labels=['OPTICAL','RADIO','X-RAY'];icons=VGroup()
        for x,color,label in zip((-2.5,0,2.5),colors,labels):icons.add(VGroup(telescope([x,2,0],color).scale(.55),txt(label,.5,20,color).shift(RIGHT*x)))
        self.beat(.22,FadeIn(icons));self.add(Brace(icons,DOWN,color=LIGHT),txt('ELECTROMAGNETIC WAVES',-.8,25,LIGHT))
        wave=VGroup(messenger_icon if False else Circle(radius=.6,color=WAVE),ParametricFunction(lambda t:np.array([t,-2.6+.2*np.sin(9*t),0]),t_range=[-.42,.42],color=WAVE)).shift(LEFT*2.2)
        self.beat(.18,FadeIn(wave),FadeIn(txt('GRAVITATIONAL WAVES',-2.6,30,WAVE).shift(RIGHT*.65)))
        self.add(txt('새로운 감각',-3.8,36,SIGNAL));self.finish()

        self.cue('예측에서, 중력파 천문학으로','100년 전의 예측을 직접 신호로 바꾸며\n우주를 보는 새로운 방법이 현실이 됐습니다.')
        self.add(grid((0,1.8,0),1,1,width=7,height=3.5))
        steps=[(-2.8,'1916','prediction',LIGHT),(0,'2015','direct detection',OBS),(2.8,'2017','Nobel Prize',GOLD)]
        for i,(x,year,label,color) in enumerate(steps):
            self.beat(.1,FadeIn(Dot([x,1.8,0],radius=.09,color=color)),FadeIn(txt(year,2.55,29,color).shift(RIGHT*x)),FadeIn(txt(label,1.05,22,color,2.2).shift(RIGHT*x)))
            if i<2:self.add(Arrow([x+.45,1.8,0],[x+2.25,1.8,0],buff=0,color='#71809B',stroke_width=2))
        self.beat(.13,FadeIn(medal([0,-.45,0])))
        self.add(txt('GRAVITATIONAL-WAVE ASTRONOMY',-2.05,35,WAVE),txt('우주를 보는 새로운 감각',-3.25,31,LIGHT),txt('2017 NOBEL PRIZE IN PHYSICS',-4.15,24,GOLD));self.finish()
