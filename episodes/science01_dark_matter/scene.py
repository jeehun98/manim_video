"""A question, a rotation curve, and the unseen mass inferred from motion."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.environ.get('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.environ.get('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#080E1B'
LIGHT, EXPECT, OBS, HALO = '#F9DE9C', '#FF978D', '#62DCEC', '#8F9CFF'

def text(s, y=0, size=30, color=WHITE):
    m = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.25)
    if m.width > 7.8: m.scale_to_fit_width(7.8)
    return m.move_to([0, y, 0])

def galaxy(center=ORIGIN, scale=1):
    rng = np.random.default_rng(41)
    g = VGroup()
    for radius in np.linspace(1.55, .15, 12):
        g.add(Circle(radius=radius, stroke_width=0, fill_color=LIGHT,
                     fill_opacity=.018).stretch(.62, 1))
    for i in range(120):
        r = 1.6 * np.sqrt(rng.random())
        a = i * TAU / 3 + r * 2.8 + rng.normal(0, .22)
        g.add(Dot([r*np.cos(a), .62*r*np.sin(a), 0], radius=.016 + .015*(1-r/1.7),
                  color=LIGHT).set_opacity(.85-.4*r/1.7))
    g.add(Dot(radius=.13, color=LIGHT))
    return g.scale(scale).move_to(center)

class DarkMatterDiscovery(Scene):
    DURATION = 104

    def to(self, target):
        if self.time > target + 1/30: raise RuntimeError(f'Cue overrun: {self.time} > {target}')
        n = round((target-self.time)*30)
        if n > 0: self.wait(n/30)

    def cue(self, title, caption):
        new = VGroup(text(title, 5.65, 36), text(caption, -5.8, 27))
        if hasattr(self, 'words'): self.play(FadeOut(self.words), FadeIn(new), run_time=.5)
        else: self.play(FadeIn(new), run_time=.5)
        self.words = new

    def clear_stage(self):
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.brand and m is not self.words], run_time=.6)

    def orbit(self, center, radius, duration, color=OBS, angle=0, sweep=TAU):
        path = Arc(radius=radius, start_angle=angle, angle=sweep, arc_center=center)
        star = Dot(path.get_start(), radius=.09, color=color)
        track = Circle(radius=radius, color=color, stroke_opacity=.25).move_to(center)
        self.add(track, star)
        self.play(MoveAlongPath(star, path, rate_func=linear), run_time=duration)
        return star, track

    def construct(self):
        self.brand = text('과학의 한 장면  /  01', 7.1, 23, '#9BA9C3')
        self.add(self.brand)
        self.cue('은하 바깥의 별은\n왜 이렇게 빠를까?', '바깥으로 갈수록 보이는 물질은 희박해지는데,\n별은 여전히 빠르게 돕니다.')
        g = galaxy([0, .6, 0], 1.35)
        self.play(FadeIn(g), run_time=1.5)
        ray = Line([0,.6,0], [2.9,.6,0], color=OBS)
        self.play(Create(ray), run_time=1)
        star, track = self.orbit(np.array([0,.6,0]), 2.9, 5, sweep=PI)
        self.to(12)

        self.cue('먼 곳에서는 느려질까?', '질량이 대부분 은하 안쪽에 모여 있다면,\n멀리 있는 별일수록 속도는 낮아져야 합니다.')
        self.clear_stage()
        sun = Dot([0,.5,0], radius=.18, color=LIGHT)
        self.add(sun, text('질량이 중심에 집중된 경우', -3.3, 25, LIGHT))
        phase = ValueTracker(0)
        inner = always_redraw(lambda: Dot([1.15*np.cos(phase.get_value()), .5+1.15*np.sin(phase.get_value()),0], color=LIGHT))
        outer = always_redraw(lambda: Dot([2.7*np.cos(phase.get_value()*(1.15/2.7)**1.5), .5+2.7*np.sin(phase.get_value()*(1.15/2.7)**1.5),0], color=EXPECT))
        rings = VGroup(*[Circle(radius=r, stroke_opacity=.3).move_to(sun) for r in (1.15,2.7)])
        self.add(rings, inner, outer)
        self.play(phase.animate.set_value(TAU*2), run_time=9, rate_func=linear)
        inner.clear_updaters(); outer.clear_updaters()
        self.to(24)

        self.cue('예상을 곡선으로 그리면', '은하의 위치마다 예상 속도를 기록합니다.\n안쪽에서 올라가고, 바깥에서 내려갑니다.')
        self.clear_stage()
        g = galaxy([0,2.1,0], 1)
        axes = Axes(x_range=[0,5,1], y_range=[0,1.4,.5], x_length=6.6, y_length=3.1,
                    axis_config={'include_ticks':False,'color':'#8190AA'}).move_to([0,-1.7,0])
        labels = VGroup(text('회전 속도', .2, 23), text('중심에서의 거리', -3.75, 23), text('개념도 · 실제 측정 데이터 아님', -4.35, 19, '#9BA9C3'))
        def expected(r): return r if r <= 1 else 1/np.sqrt(r)
        def observed(r): return r if r <= 1 else 1
        radius = ValueTracker(.1)
        probe = always_redraw(lambda: Dot([radius.get_value()*.62,2.1,0], color=EXPECT, radius=.07))
        line = always_redraw(lambda: Line([0,2.1,0],probe.get_center(),color=EXPECT))
        point = always_redraw(lambda: Dot(axes.c2p(radius.get_value(),expected(radius.get_value())),color=EXPECT))
        trace = always_redraw(lambda: axes.plot(expected,x_range=[.01,max(.02,radius.get_value())],color=EXPECT))
        self.play(FadeIn(g),Create(axes),FadeIn(labels),run_time=1)
        self.add(probe,line,point,trace)
        self.play(radius.animate.set_value(4.7),run_time=9,rate_func=linear)
        for m in (probe,line,point,trace): m.clear_updaters()
        # Korean labels, with the gas contribution included in the physical model.
        expected_label = text('별·가스만으로 예상', -2.85, 23, EXPECT).shift(RIGHT*1.25)
        self.play(FadeIn(expected_label),run_time=.5)
        self.to(38)

        self.cue('그런데 관측은 다릅니다', '많은 나선은하에서는 바깥으로 가도\n회전 속도가 거의 줄어들지 않습니다.')
        obs_points = VGroup(*[Dot(axes.c2p(r,observed(r)),radius=.065,color=OBS) for r in np.linspace(.35,4.7,14)])
        obs_curve = axes.plot(observed,x_range=[.01,4.7],color=OBS)
        self.play(LaggedStart(*[FadeIn(p,scale=2) for p in obs_points],lag_ratio=.18),run_time=4)
        self.play(Create(obs_curve),run_time=2)
        obs_label = text('관측: 속도가 유지된다', -.65, 25, OBS)
        self.play(FadeIn(obs_label),Indicate(obs_points[-4:]),run_time=1)
        self.to(51)

        self.cue('이 궤도를 유지하려면?', '이 빠른 별들이 같은 궤도를 유지하려면,\n더 강한 중력이 필요합니다.')
        self.clear_stage()
        g = galaxy([0,.5,0],1)
        star = Dot([2.8,.5,0],radius=.11,color=OBS)
        orbit = DashedVMobject(Circle(radius=2.8).move_to([0,.5,0]),num_dashes=48).set_opacity(.35)
        velocity = Arrow(star.get_center(),[2.8,2.3,0],buff=.12,color=OBS)
        weak = Arrow([2.8,.5,0],[2.05,.5,0],buff=.1,color=EXPECT)
        needed = Arrow([2.8,.15,0],[.65,.15,0],buff=.1,color=HALO)
        self.play(FadeIn(g),FadeIn(star),Create(orbit),GrowArrow(velocity),run_time=1.5)
        self.play(GrowArrow(weak),FadeIn(text('별·가스로 계산한 중력',-2.85,25,EXPECT)),run_time=1)
        self.play(GrowArrow(needed),FadeIn(text('관측된 원운동에 필요한 중력',-3.6,25,HALO)),run_time=1.5)
        self.play(Indicate(needed),run_time=1)
        self.to(65)

        self.cue('별의 운동에서 질량을 거꾸로', '바깥에서도 속도가 유지되려면,\n더 큰 반지름 안의 총질량이 계속 증가해야 합니다.')
        self.clear_stage()
        g = galaxy([0,.7,0],.9)
        self.play(FadeIn(g),run_time=1)
        shell_groups = VGroup()
        for i,r in enumerate((1.4,2.1,2.8,3.5)):
            ring = Circle(radius=r,color=HALO,stroke_opacity=.65).move_to([0,.7,0])
            dots = VGroup(*[Dot([r*.93*np.cos(a),.7+r*.93*np.sin(a),0],radius=.028,color=HALO) for a in np.linspace(0,TAU,18,endpoint=False)])
            shell_groups.add(VGroup(ring,dots))
            self.play(Create(ring),LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.03),run_time=1.8)
        self.add(text('점과 원: 운동으로 추론한 질량의 표현',-3.7,22,HALO))
        self.to(79)

        self.cue('보이지 않는 넓은 분포', '표준 중력 이론에서는 이 추가 질량을\n암흑물질 헤일로로 설명합니다.')
        halo = VGroup(*[Circle(radius=r,stroke_width=0,fill_color=HALO,fill_opacity=.013).move_to([0,.7,0]) for r in np.linspace(3.65,.2,22)])
        self.play(FadeOut(shell_groups),FadeIn(halo,scale=.3),run_time=3)
        self.bring_to_front(g)
        self.play(FadeIn(text('Dark Matter Halo',-4.35,30,HALO)),run_time=1)
        self.to(91)

        self.cue('빛보다 넓게, 중력이 말한다', '빛으로 보이는 은하 너머에도\n별의 운동을 설명하는 질량이 있습니다.')
        self.clear_stage()
        left,right = np.array([-2.05,.7,0]),np.array([2.05,.7,0])
        a,b = galaxy(left,.72),galaxy(right,.72)
        h = VGroup(*[Circle(radius=r,stroke_width=0,fill_color=HALO,fill_opacity=.023).move_to(right) for r in np.linspace(1.85,.15,14)])
        self.play(FadeIn(a),FadeIn(h),FadeIn(b),run_time=2)
        self.add(text('빛으로 본 은하',-1.75,24,LIGHT).shift(LEFT*2.05),text('중력으로 추론한 은하',-1.75,24,HALO).shift(RIGHT*2.05))
        self.play(FadeIn(text('암흑물질\n빛이 아니라, 운동이 남긴 단서',-3.5,31,HALO)),run_time=1)
        self.to(102)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=2)
