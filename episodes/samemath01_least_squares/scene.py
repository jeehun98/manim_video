"""One script, two native layouts. Source timings are in script.json."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import *

# Manim creates its camera before Scene.setup(), so set logical dimensions here.
config.frame_width = 16 if "SameMathLong" in sys.argv else 9
config.frame_height = 9 if "SameMathLong" in sys.argv else 16
config.background_color = "#101B2E"

DATA = json.loads((Path(__file__).parent / "script.json").read_text(encoding="utf-8"))
BG = "#101B2E"
PANEL = "#17263D"
EDGE = "#344761"
WHITE = "#ECF3F6"
MUTED = "#A8B8C7"
TEAL = "#5DE0CE"
ORANGE = "#FF9F62"
PURPLE = "#B79CFA"
YELLOW = "#F9DE79"
FONT = "Malgun Gothic"


def label(s, size=28, color=WHITE):
    return Text(s, font=FONT, font_size=size, color=color)


def formula(s, size=44, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def wrapped(s, limit):
    lines, line = [], ""
    for word in s.split():
        proposal = (line + " " + word).strip()
        if len(proposal) > limit and line:
            lines.append(line)
            line = word
        else:
            line = proposal
    if line:
        lines.append(line)
    return "\n".join(lines)


class SameMathBase(Scene):
    wide = False

    def setup(self):
        config.frame_width = 16 if self.wide else 9
        config.frame_height = 9 if self.wide else 16
        config.background_color = BG
        self.fw = 16 if self.wide else 9
        self.fh = 9 if self.wide else 16
        self.top = 3.55 if self.wide else 6.8
        self.caption_y = -3.75 if self.wide else -6.6
        self.mid = 0.35 if self.wide else 0.7

    def header(self, title, kicker):
        a = label(kicker, 21 if self.wide else 23, YELLOW).move_to([0, self.top, 0])
        b = label(title, 32 if self.wide else 29).next_to(a, DOWN, buff=.20)
        b.scale_to_fit_width(min(b.width, self.fw - 1))
        return VGroup(a, b)

    def regression(self, origin=None, scale=1, slope=.5, intercept=5/3):
        if origin is None:
            origin = np.array([0, self.mid-.2, 0])
        ax = Axes(x_range=[-1.5, 1.5, .5], y_range=[.5, 2.5, .5],
                  x_length=5.4 if self.wide else 5.8, y_length=2.9 if self.wide else 4.0,
                  axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False}).scale(scale).move_to(origin)
        xx = [-1, 0, 1]
        yy = [1, 2, 2]
        line = Line(ax.c2p(-1.3, intercept-1.3*slope), ax.c2p(1.3, intercept+1.3*slope), color=TEAL, stroke_width=5)
        dots = VGroup(*[Dot(ax.c2p(x,y), color=WHITE, radius=.085) for x,y in zip(xx,yy)])
        residuals = VGroup(*[DashedLine(ax.c2p(x,intercept+x*slope), ax.c2p(x,y), color=ORANGE, dash_length=.07) for x,y in zip(xx,yy)])
        return VGroup(ax,line,residuals,dots)

    def density(self, laplace=False, x0=0, width=None, obs_x=1.25):
        width = width or (5.8 if not self.wide else 6.8)
        axes = Axes(x_range=[-3,3,1], y_range=[0,1.1,.25], x_length=width,
                    y_length=2.7 if self.wide else 3.7,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False})
        curve = axes.plot((lambda x: math.exp(-abs(x))) if laplace else (lambda x: math.exp(-x*x/2)),
                          x_range=[-3,3], color=PURPLE, stroke_width=5)
        dot = Dot(axes.c2p(obs_x, math.exp(-abs(obs_x) if laplace else -obs_x**2/2)), color=WHITE, radius=.09)
        stem = DashedLine(axes.c2p(obs_x,0), dot.get_center(), color=ORANGE)
        center = Dot(axes.c2p(0,0), color=TEAL, radius=.07)
        return VGroup(axes,curve,stem,dot,center).move_to([x0,self.mid+.2,0])

    def scene_for(self, phase):
        # Each phase states one claim and can be replaced without changing sentence timing.
        if phase == 0:
            h = self.header("가장 가까운 점과 가장 그럴듯한 답", "두 질문")
            a = label("거리 최소", 31, TEAL)
            b = label("우도 최대", 31, PURPLE)
            if self.wide:
                a.move_to([-3.1,.7,0]); b.move_to([3.1,.7,0])
                bar = Line([-1.4,.7,0],[1.4,.7,0], color=YELLOW)
            else:
                a.move_to([0,2.0,0]); b.move_to([0,-1.9,0])
                bar = Line([0,.9,0],[0,-.8,0], color=YELLOW)
            q = label("왜 같은 계산일까?", 30, YELLOW).move_to([0,-2.2 if self.wide else -3.7,0])
            return VGroup(h,a,b,bar,q)
        if phase == 1:
            h=self.header("데이터에 가장 잘 맞는 직선", "기하학 ①")
            graph=self.regression(slope=-.2)
            eq=formula(r"\min_w\sum_i(y_i-\hat y_i)^2", 40, ORANGE).move_to([0,-2.8 if self.wide else -3.6,0])
            return VGroup(h,graph,eq)
        if phase == 2:
            h=self.header("예측 벡터는 열공간 안에", "기하학 ②")
            # Isometric sketch of a plane in the 3D observation space.
            center=np.array([0,self.mid,0]); sw=1.25 if self.wide else 1
            plane=Polygon(center+sw*np.array([-2.8,-.6,0]),center+sw*np.array([1.2,-1.6,0]),
                          center+sw*np.array([2.9,.4,0]),center+sw*np.array([-1.1,1.4,0]),
                          color=TEAL, fill_color=TEAL, fill_opacity=.12, stroke_width=2)
            pred=Dot(center+np.array([.15,-.1,0]),color=TEAL,radius=.09)
            obs=Dot(center+np.array([.15,1.65,0]),color=WHITE,radius=.09)
            residual=Arrow(pred.get_center(),obs.get_center(),buff=0,color=ORANGE,stroke_width=6)
            ylbl=label("y",25).next_to(obs,RIGHT)
            plbl=label("Xw",25,TEAL).next_to(pred,DOWN)
            space=label("col(X)",23,TEAL).move_to(center+np.array([-1.35,-.6,0]))
            eq=formula(r"\|y-Xw\|^2=\sum_i(y_i-\hat y_i)^2",35,ORANGE)
            eq.move_to([0,-2.7 if self.wide else -3.35,0])
            eq.scale_to_fit_width(min(eq.width,self.fw-1))
            return VGroup(h,plane,pred,obs,residual,ylbl,plbl,space,eq)
        if phase == 3:
            h=self.header("가장 가까운 점: 잔차가 수직", "직교투영")
            a=formula(r"X^T(y-Xw)=0",48,TEAL).move_to([0,1.1 if self.wide else 1.5,0])
            b=formula(r"X^TXw=X^Ty",53,YELLOW).move_to([0,-.65 if self.wide else -.5,0])
            c=label("정규방정식",25,MUTED).next_to(b,DOWN,buff=.3)
            return VGroup(h,a,b,c)
        if phase == 4:
            h=self.header("예측값에 무작위 오차가 더해진다면", "확률론 ①")
            d=self.density()
            eq=formula(r"y_i=\hat y_i+\epsilon_i",44,TEAL).move_to([0,-1.65 if self.wide else -3.1,0])
            e=formula(r"\epsilon_i\sim\mathcal N(0,\sigma^2)",40,PURPLE).next_to(eq,DOWN,buff=.22)
            return VGroup(h,d,eq,e)
        if phase == 5:
            h=self.header("가우시안 지수에 숨은 제곱오차", "확률론 ②")
            d=self.density(obs_x=.25)
            eq=formula(r"p(y_i\mid w)\propto e^{-(y_i-\hat y_i)^2/(2\sigma^2)}",38)
            eq.move_to([0,-2.55 if self.wide else -3.35,0]); eq.scale_to_fit_width(min(eq.width,self.fw-1))
            eq.set_opacity(0)
            return VGroup(h,d,eq)
        if phase == 6:
            h=self.header("곱에 로그를 취하면 합이 된다", "확률론 ③")
            p=formula(r"\mathcal L(w)=p_1p_2p_3",47,PURPLE).move_to([0,1.4 if self.wide else 2.0,0])
            arrow=Arrow([0,.75 if self.wide else 1.2,0],[0,.15 if self.wide else .45,0],buff=0,color=YELLOW)
            q=formula(r"\log\mathcal L=\log p_1+\log p_2+\log p_3",39,YELLOW).move_to([0,-.4 if self.wide else -.3,0])
            q.scale_to_fit_width(min(q.width,self.fw-1)); q.set_opacity(0)
            r=formula(r"=-\frac{1}{2\sigma^2}\sum_i(y_i-\hat y_i)^2+C",40,ORANGE)
            r.move_to([0,-2.0 if self.wide else -2.65,0]); r.scale_to_fit_width(min(r.width,self.fw-1)); r.set_opacity(0)
            return VGroup(h,p,arrow,q,r)
        if phase == 7:
            h=self.header("두 관점이 선택하는 같은 해", "같은 목적함수")
            a=label("기하학",25,TEAL).move_to([0,1.85 if self.wide else 2.4,0])
            e1=formula(r"\min_w\sum_i(y_i-\hat y_i)^2",42,TEAL).next_to(a,DOWN,buff=.25)
            b=label("확률론",25,PURPLE).move_to([0,-.3 if self.wide else -.2,0])
            e2=formula(r"\max_w[-c\sum_i(y_i-\hat y_i)^2+C]",39,PURPLE).next_to(b,DOWN,buff=.25)
            e2.scale_to_fit_width(min(e2.width,self.fw-1)); e2.set_opacity(0); b.set_opacity(0)
            ans=formula(r"\boxed{\min_w\sum_i(y_i-\hat y_i)^2}",43,YELLOW)
            ans.move_to([0,-2.5 if self.wide else -3.2,0]); ans.scale_to_fit_width(min(ans.width,self.fw-1)); ans.set_opacity(0)
            return VGroup(h,a,e1,b,e2,ans)
        if phase == 8:
            h=self.header("오차분포가 바뀌면 목적함수도", "가정의 역할")
            if self.wide:
                left=VGroup(label("정규분포",25,PURPLE),formula(r"e^{-c\epsilon^2}",38),formula(r"\min\sum_i\epsilon_i^2",38,ORANGE)).arrange(DOWN,buff=.5).move_to([-3.5,0,0])
                right=VGroup(label("라플라스분포",25,PURPLE),formula(r"e^{-c|\epsilon|}",38),formula(r"\min\sum_i|\epsilon_i|",38,ORANGE)).arrange(DOWN,buff=.5).move_to([3.5,0,0])
            else:
                left=VGroup(label("정규분포",25,PURPLE),formula(r"e^{-c\epsilon^2}\ \Rightarrow\ \min\sum_i\epsilon_i^2",35,ORANGE)).arrange(DOWN,buff=.3).move_to([0,1.5,0])
                right=VGroup(label("라플라스분포",25,PURPLE),formula(r"e^{-c|\epsilon|}\ \Rightarrow\ \min\sum_i|\epsilon_i|",35,ORANGE)).arrange(DOWN,buff=.3).move_to([0,-1.4,0])
                left[1].scale_to_fit_width(min(left[1].width,self.fw-1)); right[1].scale_to_fit_width(min(right[1].width,self.fw-1))
            return VGroup(h,left,right)
        h=self.header("같아지는 조건을 찾아라", "결론")
        a=label("가까운 점",29,TEAL)
        b=label("그럴듯한 답",29,PURPLE)
        eq=formula(r"\min_w\sum_i(y_i-\hat y_i)^2",46,YELLOW)
        if self.wide:
            a.move_to([-3.1,.75,0]); b.move_to([3.1,.75,0]); eq.move_to([0,-1.3,0])
        else:
            a.move_to([0,2,0]); b.move_to([0,.3,0]); eq.move_to([0,-2.1,0])
        return VGroup(h,a,b,eq)

    def phase(self,t):
        for index, end in enumerate((10,22,41,48,60,79,111,136,153,160)):
            if t < end: return index
        return 9

    def construct(self):
        footer=Rectangle(width=self.fw,height=1.43 if self.wide else 2.1,
                         fill_color=PANEL,fill_opacity=1,stroke_width=0)
        footer.move_to([0,-3.78 if self.wide else -6.9,0]).set_z_index(-5)
        rule=Line([-self.fw/2+.55,self.top-.9,0],[self.fw/2-.55,self.top-.9,0],
                  color=EDGE,stroke_width=1).set_z_index(-5)
        self.add(footer,rule)
        self.visual=None
        self.subtitle=None
        previous=0
        last_phase=-1
        for end,sentence in DATA["sentences"]:
            phase=self.phase(previous)
            animations=[]
            if phase!=last_phase:
                new=self.scene_for(phase)
                if self.visual is not None: animations.append(FadeOut(self.visual))
                animations.append(FadeIn(new))
                self.visual=new
                last_phase=phase
            caption=VGroup(*[label(line,25 if self.wide else 28) for line in wrapped(sentence,42 if self.wide else 23).split("\n")])
            caption.arrange(DOWN,buff=.11)
            if caption.width > self.fw-1.0:
                caption.scale_to_fit_width(self.fw-1.0)
            caption.move_to([0,self.caption_y,0])
            if self.subtitle is not None: animations.append(FadeOut(self.subtitle))
            animations.append(FadeIn(caption))
            self.subtitle=caption
            duration=end-previous
            transition=min(.35,duration*.25)
            self.play(*animations,run_time=transition)
            extra=0
            if phase==1 and previous==14:
                extra=1.8
                self.play(Transform(self.visual[1],self.regression()),run_time=extra)
            elif phase==5 and previous==69:
                extra=1.4
                self.play(Transform(self.visual[1],self.density(obs_x=1.25)),self.visual[2].animate.set_opacity(1),run_time=extra)
            elif phase==6 and previous==94:
                extra=.7
                self.play(self.visual[3].animate.set_opacity(1),run_time=extra)
            elif phase==6 and previous==99:
                extra=.7
                self.play(self.visual[4].animate.set_opacity(1),run_time=extra)
            elif phase==7 and previous==117:
                extra=.7
                self.play(self.visual[3].animate.set_opacity(1),self.visual[4].animate.set_opacity(1),run_time=extra)
            elif phase==7 and previous==120:
                extra=.7
                self.play(self.visual[5].animate.set_opacity(1),run_time=extra)
            if extra:
                # Manim lifts an animated child out of a scene-level VGroup.
                # Re-add the group so its other elements remain visible.
                self.add(self.visual)
            self.wait(duration-transition-extra)
            previous=end


class SameMathShort(SameMathBase):
    pass


class SameMathLong(SameMathBase):
    wide=True
