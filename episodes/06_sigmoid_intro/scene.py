"""Sigmoid 01: position-dependent compression. 70 seconds, silent portrait master."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT = '#EDF3F7', '#94A7B7', '#61E4CF'
PINK, GOLD, BLUE = '#FF8C9D', '#F3CF75', '#68D9F0'

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def label(s, size=30, color=INK):
    m = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.1)
    if m.width > 7.6:
        m.scale_to_fit_width(7.6)
    return m

class SigmoidIntroduction(Scene):
    def until(self, t):
        if self.time > t + .05:
            raise ValueError(f'Timing overrun: {self.time} > {t}')
        if t > self.time:
            self.wait(t-self.time)

    def caption(self, s):
        new = label(s, 30).move_to(DOWN*5.65)
        self.play(Transform(self.sub, new), run_time=.35)

    def construct(self):
        series = label('ACTIVATION FUNCTION SERIES', 19, MUTED).move_to(UP*6.85)
        title = label('Sigmoid', 66).move_to(UP*5.65)
        episode = label('01  /  위치에 따라 달라지는 압축', 24, MINT).move_to(UP*4.65)
        formula = label('σ(x) = 1 / (1 + e⁻ˣ)', 32, MINT).move_to(UP*3.65)
        self.sub = label('Sigmoid는 어떤 입력이 들어와도\n출력을 0과 1 사이로 바꿉니다.',30).move_to(DOWN*5.65)
        ax = Axes(x_range=[-6,6,2], y_range=[0,1.1,.5], x_length=7, y_length=4.6,
                  axis_config={'color':MUTED,'stroke_width':1.5,'tip_width':.12,'tip_height':.12},
                  y_axis_config={'include_ticks':False}).move_to(UP*.45)
        p = ax.c2p
        ticks = VGroup(*[label(str(x).replace('-', '−'),20,MUTED).next_to(p(x,0),DOWN,buff=.16) for x in [-6,-4,-2,0,2,4,6]])
        yticks = VGroup(*[label(str(y),20,MUTED).next_to(p(-6,y),LEFT,buff=.14) for y in [0,.5,1]])
        bounds = VGroup(*[DashedLine(p(-6,y),p(6,y),color=MUTED,stroke_width=1.2).set_opacity(.45) for y in [.5,1]])
        names = VGroup(label('입력 x',21,MUTED).next_to(ax,DOWN,buff=.6),label('출력 σ(x)',21,MUTED).move_to(LEFT*2.6+UP*3))
        curve = ax.plot(sigmoid,x_range=[-6,6,.04],color=MINT,stroke_width=5)
        self.play(FadeIn(series),FadeIn(title),FadeIn(episode),FadeIn(formula),FadeIn(self.sub),run_time=.8)
        self.play(Create(ax),FadeIn(ticks),FadeIn(yticks),FadeIn(bounds),FadeIn(names),Create(curve),run_time=1.5)
        badge = label('0 < σ(x) < 1',30,MINT).move_to(DOWN*3.45)
        self.play(FadeIn(badge),run_time=.5)
        self.until(6)
        x = ValueTracker(0)
        dot = always_redraw(lambda: Dot(p(x.get_value(),sigmoid(x.get_value())),radius=.10,color=GOLD).set_z_index(5))
        guide = always_redraw(lambda: DashedLine(p(x.get_value(),0),p(x.get_value(),sigmoid(x.get_value())),color=GOLD,stroke_width=2))
        self.add(guide,dot)
        self.caption('입력이 작아질수록\n출력은 0에 가까워지고,')
        self.play(x.animate.set_value(-5),run_time=3.5)
        self.until(12)
        self.caption('입력이 커질수록\n출력은 1에 가까워집니다.')
        self.play(x.animate.set_value(5),run_time=4)
        self.until(18)
        self.caption('가운데, 입력이 0일 때는\n출력이 정확히 0.5입니다.')
        self.play(x.animate.set_value(0),Transform(badge,label('σ(0) = 0.5',34,GOLD).move_to(badge)),run_time=1.5)
        self.play(Indicate(dot),run_time=.8)
        self.until(24)
        self.caption('그래프만 보면 실수 전체를\n0과 1 사이로 눌러 넣는 함수처럼 보입니다.')
        self.play(Transform(badge,label('모든 실수 → (0, 1)',30,MINT).move_to(badge)),run_time=.6)
        self.until(30)
        self.caption('하지만 모든 구간을\n똑같이 줄이는 것은 아닙니다.')
        dot.clear_updaters(); guide.clear_updaters()
        self.play(FadeOut(dot),FadeOut(guide),Transform(badge,label('같은 Δx, 다른 Δ출력',30,GOLD).move_to(badge)),run_time=.6)
        self.until(35)

        def interval(a,b,color):
            ya,yb = sigmoid(a),sigmoid(b)
            return VGroup(
                ax.plot(sigmoid,x_range=[a,b,.02],color=color,stroke_width=9),
                Dot(p(a,ya),radius=.085,color=color),Dot(p(b,yb),radius=.085,color=color),
                Line(p(a,-.09),p(b,-.09),color=color,stroke_width=6),
                DashedLine(p(a,0),p(a,ya),color=color,stroke_width=1.5),
                DashedLine(p(b,0),p(b,yb),color=color,stroke_width=1.5),
                Line(p(b+.25,ya),p(b+.25,yb),color=color,stroke_width=6))

        center = interval(-.5,.5,GOLD)
        left, right = interval(-4.5,-3.5,PINK), interval(3.5,4.5,BLUE)
        self.caption('0 근처에서는 입력이 조금만 변해도\n출력이 비교적 크게 변합니다.')
        self.play(FadeIn(center),Transform(badge,label('Δx = 1    →    Δ출력 ≈ 0.245',29,GOLD).move_to(badge)),run_time=.8)
        self.play(Indicate(center[-1],scale_factor=1.2),run_time=1)
        self.until(42)
        self.caption('반대로 양끝으로 갈수록\n입력이 더 변해도 출력은 거의 움직이지 않습니다.')
        self.play(FadeIn(left),FadeIn(right),Transform(badge,label('Δx = 1    →    Δ출력 ≈ 0.018',29,BLUE).move_to(badge)),run_time=.8)
        self.play(Indicate(left[0]),Indicate(right[0]),run_time=1)
        self.until(50)
        self.caption('같은 크기의 입력 변화라도,\n어디에서 일어났는지에 따라')
        self.play(FadeOut(badge),run_time=.3)
        # Bars share a single scale: their lengths are proportional to Δoutput.
        bars = VGroup()
        for i,(a,b,c,name) in enumerate([(-4.5,-3.5,PINK,'왼쪽'),(-.5,.5,GOLD,'중앙'),(3.5,4.5,BLUE,'오른쪽')]):
            delta = sigmoid(b)-sigmoid(a)
            y = -3.1-i*.57
            bars.add(label(name,22,c).move_to([-2.8,y,0]),
                     Rectangle(width=delta*14,height=.20,fill_color=c,fill_opacity=1,stroke_width=0).move_to([-1.7+delta*7,y,0]),
                     label(f'{delta:.3f}',21,c).move_to([2.75,y,0]))
        self.play(FadeIn(bars),run_time=.8)
        self.until(55)
        self.caption('출력에서 보이는\n변화의 크기는 달라집니다.')
        self.until(59)
        self.caption('Sigmoid는 단순히 값을\n0과 1 사이로 줄이는 것이 아니라,')
        self.until(64)
        self.caption('입력 공간을 위치에 따라\n서로 다른 비율로 압축합니다.')
        self.play(Transform(episode,label('중앙은 덜 압축 · 양끝은 더 압축',25,MINT).move_to(episode)),run_time=.7)
        self.until(70)
