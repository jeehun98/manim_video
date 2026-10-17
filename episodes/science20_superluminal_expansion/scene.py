"""Local measured speed and FLRW proper-distance rate are different quantities."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,galaxy,LIGHT,OBS,MASS,EXPECT
from episodes.science04_virial_theorem.scene import equation
from episodes.science08_density_growth.scene import DensityGrowthDiscovery

DIM='#526781'

def label(s,x,y,size=28,color=LIGHT,width=7.5):return txt(s,y,size,color,width).move_to([x,y,0])

def ruler(n,spacing,y=1,left=-3,color=OBS):
    ticks=VGroup(*[Line([left+i*spacing,y-.13,0],[left+i*spacing,y+.13,0],color=color,stroke_width=2) for i in range(n+1)])
    return VGroup(Line([left,y,0],[left+n*spacing,y,0],color=DIM,stroke_width=2),ticks)

def expanding_grid(s):
    lines=VGroup(*[Line([x*s,-1.8*s+1,0],[x*s,1.8*s+1,0],color=DIM,stroke_opacity=.6,stroke_width=1) for x in np.arange(-3,3.1,.6)],
                 *[Line([-3*s,y*s+1,0],[3*s,y*s+1,0],color=DIM,stroke_opacity=.6,stroke_width=1) for y in np.arange(-1.8,1.9,.6)])
    return VGroup(lines,galaxy([-2.4*s,1,0],.45,LIGHT),galaxy([2.4*s,1,0],.45,MASS),
                  DoubleArrow([-2.4*s,.35,0],[2.4*s,.35,0],buff=.05,color=OBS,stroke_width=2))

def car(x,y):
    return VGroup(RoundedRectangle(width=.65,height=.28,corner_radius=.08,color=LIGHT,fill_opacity=.25).move_to([x,y,0]),
                  Dot([x-.2,y-.18,0],radius=.065,color=LIGHT),Dot([x+.2,y-.18,0],radius=.065,color=LIGHT))

class SuperluminalExpansionDiscovery(DensityGrowthDiscovery):
    TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
    DURATION=TIMING['duration']

    def construct(self):
        self.brand=txt('과학의 한 장면  /  20',7.1,23,'#9BA9C3');self.add(self.brand)
        self.cue('빛보다 빠른 게 존재한다?', '빛보다 빠르게 늘어나는 은하 사이의 거리.\n상대성이론과 모순되는 걸까요?')
        path=Line([-3.1,2.6,0],[3.1,2.6,0],color=OBS,stroke_opacity=.35)
        photon=Dot(path.get_start(),radius=.075,color=OBS);self.add(path,photon,label('빛 · c',0,3.35,32,OBS))
        self.beat(.15,MoveAlongPath(photon,path),rate_func=linear)
        s=ValueTracker(.55);g=always_redraw(lambda:expanding_grid(s.get_value()).shift(DOWN*.8));self.add(g)
        self.beat(.32,s.animate.set_value(1),rate_func=linear)
        self.add(equation('Ḋ > c',-2.4,MASS,49),txt('거리 증가율',-3.45,29,MASS));self.finish()

        self.cue('바로 옆을 지나가는 속도', '가까운 관측자 옆을 지나는 운동에는\n빛의 속도 제한이 적용됩니다.')
        track=Line([-3.2,1,0],[3.2,1,0],color=DIM);self.add(track)
        observer=VGroup(Circle(radius=.18,color=OBS),Line([0,.8,0],[0,0,0],color=OBS)).move_to([0,.25,0]);self.add(observer)
        moving=galaxy([-2.8,1.5,0],.6,LIGHT);self.add(moving,label('가까운 관측자',0,-.9,26,OBS))
        self.beat(.43,moving.animate.shift(RIGHT*5.6),rate_func=linear)
        self.add(equation('v_local < c',-2.6,OBS,42),txt('질량이 있는 물체의 국소 속도',-3.8,26));self.finish()

        self.cue('눈금을 건너지 않아도 멀어진다', '은하는 격자의 같은 눈금에 머물지만,\n눈금 사이 거리는 늘어날 수 있습니다.')
        s=ValueTracker(.55);g=always_redraw(lambda:expanding_grid(s.get_value()));self.add(g)
        self.beat(.6,s.animate.set_value(1.08),rate_func=linear)
        self.add(txt('늘어나는 것은 눈금 사이의 거리',-2.7,31,OBS),txt('우주 팽창을 따라가는 두 지점 · 개념도',-3.8,23,DIM));self.finish()

        self.cue('팽창하는 가상의 눈금', '각 구간이 같은 시간 동안 같은 비율로 증가.\n실제 고체 자가 늘어난다는 뜻은 아닙니다.')
        s=ValueTracker(.65)
        marks=always_redraw(lambda:ruler(5,s.get_value(),1.3,-2.5*s.get_value()));self.add(marks)
        self.beat(.55,s.animate.set_value(1.05),rate_func=linear)
        self.add(txt('같은 시간 · 같은 비율',-.3,33,OBS),txt('공간에 붙인 가상의 표지',-2.4,29,MASS));self.finish()

        self.cue('한 칸에서는, 작은 길이 변화', '한 칸이 늘어난 만큼\n가까운 두 점 사이 거리도 증가합니다.')
        length=ValueTracker(1.9);marks=always_redraw(lambda:ruler(1,length.get_value(),1.5,-1.2));self.add(marks)
        ghost=ruler(1,1.9,1.5,-1.2,DIM).set_opacity(.35);self.add(ghost)
        self.beat(.48,length.animate.set_value(2.35),rate_func=linear)
        delta=Line([.7,.6,0],[1.15,.6,0],color=MASS,stroke_width=9)
        self.beat(.16,Create(delta));self.add(equation('ΔD = Δℓ',-1.2,MASS,44),txt('한 칸의 증가량',-2.8,29));self.finish()

        self.cue('열 칸의 변화가 함께 누적된다', '각 칸이 동시에 늘어납니다.\n합치는 것은 길이 변화량입니다.')
        step=ValueTracker(.48);marks=always_redraw(lambda:ruler(10,step.get_value(),2,-2.8));self.add(marks)
        self.beat(.3,step.animate.set_value(.56),rate_func=linear)
        pieces=VGroup(*[Line([-2.8+i*.56+.48,1.4,0],[-2.8+(i+1)*.56,1.4,0],color=MASS,stroke_width=8) for i in range(10)])
        self.beat(.14,Create(pieces))
        targets=VGroup(*[Line([-.4+i*.08,-.2,0],[-.4+(i+1)*.08,-.2,0],color=MASS,stroke_width=8) for i in range(10)])
        self.beat(.25,Transform(pieces,targets))
        self.add(equation('ΔD = 10 Δℓ',-1.6,MASS,43),txt('길이 변화의 합 ≠ 상대속도의 합',-3.2,29,OBS));self.finish()

        self.cue('더 먼 곳은, 더 빠르게 멀어진다', '같은 팽창률에서 거리가 1 : 2 : 5라면,\n거리 증가율도 1 : 2 : 5입니다.')
        scale=ValueTracker(1)
        def rows():
            out=VGroup()
            for i,n in enumerate([1,2,5]):
                y=2.9-i*1.45;end=-2.6+n*.72*scale.get_value()
                out.add(Line([-2.6,y,0],[end,y,0],color=DIM),galaxy([-2.6,y,0],.25,OBS),galaxy([end,y,0],.3,LIGHT),
                        label(f'{n}D  →  {n}v',1.8,y-.5,26,MASS,width=3.2))
            return out
        self.add(always_redraw(rows));self.beat(.62,scale.animate.set_value(1.4),rate_func=linear)
        self.add(txt('모두 같은 시간 동안의 변화',-3.4,27,OBS));self.finish()

        self.cue('허블 관계: Ḋ = HD', '표준적인 팽창 우주에서 팽창을 따라가는 지점.\nD는 같은 우주 시간에 정의한 거리입니다.')
        self.add(equation('D = a(t) χ',3.1,OBS,40),txt('같은 공변 눈금 χ',2.25,25,OBS))
        self.beat(.16,FadeIn(equation('Ḋ = H(t) D',.9,LIGHT,48)))
        d=ValueTracker(1)
        def bars():
            return VGroup(Line([-2.6,-.4,0],[-2.6+d.get_value(),-.4,0],color=OBS,stroke_width=9),
                          Line([-2.6,-1.5,0],[-2.6+d.get_value(),-1.5,0],color=MASS,stroke_width=9),
                          label('D',-3.2,-.4,30,OBS),label('Ḋ',-3.2,-1.5,30,MASS))
        self.add(always_redraw(bars));self.beat(.42,d.animate.set_value(5),rate_func=linear)
        self.add(txt('H : 그때의 팽창률 · 여기서는 고정',-3.2,26),txt('거리 증가율 v_rec = Ḋ',-4.1,25,MASS));self.finish()

        self.cue('충분히 멀면, c를 넘는다', '국소 운동의 속도가 아니라,\n먼 두 지점 사이 거리의 증가율입니다.')
        axes=Axes(x_range=[0,2.5,.5],y_range=[0,2.3,.5],x_length=5.8,y_length=4.1,
                  axis_config={'include_ticks':False,'color':DIM}).move_to([0,.8,0]);self.add(axes)
        threshold=DashedLine(axes.c2p(0,1),axes.c2p(2.5,1),color=OBS)
        shaded=Polygon(axes.c2p(1,1),axes.c2p(2.25,1),axes.c2p(2.25,2.25),fill_color=MASS,fill_opacity=.12,stroke_width=0)
        line=axes.plot(lambda x:x,x_range=[0,2.25],color=LIGHT)
        self.add(threshold,label('c',0,0,29,OBS).move_to(axes.c2p(0,1)+LEFT*.4),label('Ḋ',-3.25,3.4,29,MASS),label('거리 D',2.8,-1.75,27,OBS,width=2))
        self.beat(.48,Create(line));self.beat(.15,FadeIn(shaded),FadeIn(Dot(axes.c2p(1,1),color=OBS,radius=.06)))
        self.add(equation('D > c/H  →  Ḋ > c',-3.1,MASS,37),txt('같은 순간의 H로 비교',-4.1,24));self.finish()

        self.cue('국소적으로 측정하면, 언제나 c', '각 은하 근처의 작은 영역에서 직접 측정.\n진공에서 측정한 빛의 속도는 c입니다.')
        photons=VGroup();paths=[]
        for i in range(3):
            y=2.8-i*1.7
            self.add(RoundedRectangle(width=5.5,height=1.15,corner_radius=.12,color=DIM).move_to([0,y,0]),
                     label(f'관측자 {i+1}',-1.9,y+.2,22,OBS,width=1.4),label('c',2,y,35,OBS))
            path=Line([-1,y-.15,0],[1.25,y-.15,0]);paths.append(path)
            dot=Dot(path.get_start(),radius=.07,color=OBS);photons.add(dot)
        self.add(photons);self.beat(.43,*[MoveAlongPath(dot,path) for dot,path in zip(photons,paths)],rate_func=linear)
        self.add(txt('같은 국소 측정 · 같은 빛의 속도',-3.4,29,OBS));self.finish()

        self.cue('단위는 같아도, 측정 대상이 다르다', '바로 옆을 지나가는 운동과\n멀리 떨어진 두 위치 사이 거리의 변화.')
        for x in [-2,2]:self.add(RoundedRectangle(width=3.5,height=4.2,corner_radius=.15,color=DIM).move_to([x,1,0]))
        self.add(label('국소 운동',-2,2.5,31,OBS,width=3),label('원거리 거리 변화',2,2.5,29,MASS,width=3))
        vehicle=car(-3,1);self.add(vehicle,Line([-3.4,.6,0],[-.6,.6,0],color=DIM))
        a=galaxy([1.4,1,0],.35);b=galaxy([2.6,1,0],.35,MASS);self.add(a,b)
        self.beat(.44,vehicle.animate.shift(RIGHT*2),a.animate.shift(LEFT*.6),b.animate.shift(RIGHT*.6),rate_func=linear)
        self.add(label('옆에서 재는 속도',-2,-.3,24,OBS,width=3),label('두 지점의 거리 증가율',2,-.3,24,MASS,width=3),
                 equation('≠',-2.1,LIGHT,55),txt('같은 단위 ≠ 같은 측정',-3.5,31));self.finish()

        self.cue('같은 1%, 다른 길이 증가량', '두 띠 모두 1% 늘어납니다.\n긴 띠에서는 늘어난 길이가 더 큽니다.')
        s=ValueTracker(1)
        def strips():
            out=VGroup()
            for length,y in [(1,2.6),(5,.8)]:
                out.add(Line([-2.5,y,0],[-2.5+length*s.get_value(),y,0],color=OBS,stroke_width=10),
                        label('+1%',3,y,28,MASS,width=1.5))
            return out
        self.add(always_redraw(strips));self.beat(.3,s.animate.set_value(1.01),rate_func=linear)
        self.add(txt('늘어난 부분만 확대 ×40',-.6,26))
        self.beat(.23,Create(Line([-1.5,-1.5,0],[-1.1,-1.5,0],color=MASS,stroke_width=10)),
                   Create(Line([-1.5,-2.5,0],[.5,-2.5,0],color=MASS,stroke_width=10)))
        self.add(txt('길이 5배 → 증가량도 5배 · 비율은 둘 다 1%',-4,24,OBS));self.finish()

        self.cue('작은 방향 변화도 누적된다', '짧은 구간마다 방향은 조금씩 바뀌어도,\n긴 경로에서는 큰 변화가 됩니다.')
        turn=ValueTracker(0)
        def curve():
            angles=np.arange(24)*turn.get_value()
            vertices=np.r_[np.zeros((1,2)),np.cumsum(np.c_[np.cos(angles),np.sin(angles)]*.23,axis=0)]
            out=VGroup(*[Line(np.r_[a,0],np.r_[b,0],color=OBS if i%2 else LIGHT,stroke_width=4) for i,(a,b) in enumerate(zip(vertices,vertices[1:]))])
            return out.move_to([0,1.2,0])
        self.add(always_redraw(curve));self.beat(.6,turn.animate.set_value(PI/25),rate_func=linear)
        self.add(txt('작은 방향 변화 → 큰 전체 방향 변화',-2.7,29,OBS),txt('경로의 방향 변화에 대한 비유',-3.8,24,DIM));self.finish()

        self.cue('두 문장은 동시에 참이다', '국소 운동의 제한은 유지됩니다.\n먼 두 지점의 거리 증가율은 c를 넘을 수 있습니다.')
        for x in [-2,2]:self.add(RoundedRectangle(width=3.5,height=3.4,corner_radius=.15,color=DIM).move_to([x,1.4,0]))
        self.add(label('작은 관측 영역',-2,2.5,27,OBS,width=3),label('먼 두 지점',2,2.5,27,MASS,width=3),
                 equation('c',1,OBS,54).shift(LEFT*2),equation('Ḋ > c',1,MASS,43).shift(RIGHT*2))
        self.beat(.25,FadeIn(txt('서로 다른 측정',-1.4,36,LIGHT)))
        self.add(txt('국소적인 빛의 속도와 우주론적 거리 증가율',-3,26));self.finish()

        self.cue('빛보다 빠른 물체를 발견한 것은 아니다', '빛보다 빠른 거리 증가율은 가능합니다.\n같은 단위로 서로 다른 것을 재고 있습니다.')
        s=ValueTracker(.68);self.add(always_redraw(lambda:expanding_grid(s.get_value())))
        self.beat(.48,s.animate.set_value(1.08),rate_func=linear)
        self.add(equation('Ḋ > c',-2.5,MASS,48));self.beat(.14,FadeIn(txt('국소 운동 ≠ 원거리 거리 변화',-3.65,32,LIGHT)))
        self.finish()
