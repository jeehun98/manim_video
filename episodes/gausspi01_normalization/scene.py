"""Why the Gaussian normalizer contains pi: product, circles, and rings."""
import json
import math
from pathlib import Path

import numpy as np
from manim import *

config.frame_width = 9
config.frame_height = 16
config.background_color = "#0B1020"

DATA = json.loads((Path(__file__).parent / "script.json").read_text(encoding="utf-8"))
BG = "#0B1020"
PANEL = "#17243B"
EDGE = "#31445F"
WHITE = "#EFF5FB"
MUTED = "#A7BAD0"
GX = "#47D7C4"
GY = "#729DFF"
PI = "#FFB454"
FONT = "Malgun Gothic"
PHASE_ENDS = (15, 40, 50, 94, 122, 155, 177)


def text(s, size=27, color=WHITE):
    return Text(s, font=FONT, font_size=size, color=color)


def tex(*s, size=44):
    return MathTex(*s, font_size=size, color=WHITE)


def wrap(s, limit=23):
    lines = []
    line = ""
    for word in s.split():
        candidate = (line + " " + word).strip()
        if len(candidate) > limit and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def g(x):
    return math.exp(-.5*x*x)


def path(points, color=GX, width=4):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly(points)
    return m


def bell(mu=0, sigma=1, normalized=False, center=(0,-1.0), width=1.0, height=3.1):
    factor = 1/(sigma*math.sqrt(2*math.pi)) if normalized else 1
    pts = [np.array([center[0]+width*x,
                     center[1]+height*factor*g((x-mu)/sigma),0])
           for x in np.linspace(-3.4,3.4,120)]
    return path(pts)


def bell_area(center=(0,-1.0), width=1.0, height=3.1, factor=1):
    pts = [np.array([center[0]+width*x,center[1]+height*factor*g(x),0])
           for x in np.linspace(-3.4,3.4,100)]
    base = center[1]
    return Polygon(np.array([center[0]-3.4*width,base,0]),
                   *pts, np.array([center[0]+3.4*width,base,0]),
                   stroke_width=0, fill_color=GX, fill_opacity=.25)


def graph_axes(center=(0,-1.0), span=3.6):
    x,y=center
    return VGroup(Line([x-span,y,0],[x+span,y,0],color=EDGE,stroke_width=2),
                  Line([x,y-.12,0],[x,y+3.5,0],color=EDGE,stroke_width=2),
                  text("x",21,MUTED).move_to([x+span+.18,y-.15,0]))


def project(x,y,z,top=False):
    if top:
        return np.array([.94*x, .65+.94*y, 0])
    return np.array([.87*x+.40*y, -.15+2.65*z-.36*y-.11*x,0])


def space_axes():
    axes=VGroup(Line(project(-3.4,0,0),project(3.4,0,0),color=GX,stroke_width=2.5),
                Line(project(0,-3.4,0),project(0,3.4,0),color=GY,stroke_width=2.5),
                Line(project(0,0,0),project(0,0,1.15),color=PI,stroke_width=2.5))
    labels=VGroup(text("x",21,GX).move_to(project(3.65,0,0)),
                  text("y",21,GY).move_to(project(0,3.65,0)),
                  text("z",21,PI).move_to(project(0,0,1.28)))
    return VGroup(axes,labels)


def surface_mesh(top=False):
    mesh=VGroup()
    for fixed in np.linspace(-2.8,2.8,13):
        xline=[project(x,fixed,g(x)*g(fixed),top) for x in np.linspace(-3,3,65)]
        yline=[project(fixed,y,g(fixed)*g(y),top) for y in np.linspace(-3,3,65)]
        mesh.add(path(xline,GX,2),path(yline,GY,2))
    return mesh


def top_contours():
    result=VGroup()
    for r in (.65,1.2,1.8,2.45,3.0):
        c=Circle(radius=.94*r,stroke_color=PI,stroke_width=3,
                 stroke_opacity=.95 if r==1.8 else .55).move_to([0,.65,0])
        result.add(c)
    result.add(Dot([0,.65,0],color=PI,radius=.1))
    return result


def ring(r):
    return Annulus(inner_radius=max(.01,.94*r-.09),outer_radius=.94*r+.09,
                   fill_color=PI,fill_opacity=.72,stroke_width=0).move_to([0,.65,0])


class GaussianPiShort(Scene):
    def fit(self,m,w=8):
        if m.width>w:
            m.scale_to_fit_width(w)
        return m

    def title(self,kicker,main):
        a=text(kicker,21,PI).move_to([0,6.82,0])
        b=self.fit(text(main,30),8).next_to(a,DOWN,buff=.18)
        return VGroup(a,b)

    def phase(self,t):
        for i,end in enumerate(PHASE_ENDS):
            if t<end:
                return i
        return len(PHASE_ENDS)-1

    def scene_for(self,i):
        if i==0:
            h=self.title("정규분포", "종 모양 곡선 속의 π")
            axes=graph_axes((0,-1.25))
            curve=bell(normalized=True,center=(0,-1.25))
            eq=self.fit(tex(r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}",size=43)).move_to([0,3.45,0])
            eq.set_color_by_tex(r"\pi",PI)
            eq.set_opacity(0)
            circle=Circle(radius=.55,color=PI,stroke_width=3).move_to([0,-3.45,0])
            circle.set_stroke(opacity=0)
            return VGroup(h,axes,curve,eq,circle)
        if i==1:
            h=self.title("평균과 표준편차", "먼저 정규화 계수를 떼어낸다")
            axes=graph_axes((0,-1.4))
            area=bell_area((0,-1.4));area.set_fill(opacity=0)
            curve=bell(normalized=True,center=(0,-1.4))
            eq=self.fit(tex(r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}",size=41)).move_to([0,3.6,0])
            eq.set_color_by_tex(r"\mu",GX);eq.set_color_by_tex(r"\sigma",GY)
            legend=VGroup(text("μ  중심 위치",22,GX),text("σ  퍼진 정도",22,GY)).arrange(RIGHT,buff=.6).move_to([0,2.8,0])
            answer=text("A = ?",30,PI).move_to([0,-3.45,0]);answer.set_opacity(0)
            return VGroup(h,axes,area,curve,eq,legend,answer)
        if i==2:
            h=self.title("차원을 올리기", "높이를 z축으로 옮긴다")
            axes=space_axes()
            gx=path([project(x,0,g(x)) for x in np.linspace(-3,3,100)],GX,5)
            eq=tex(r"z=g(x)=e^{-x^2/2}",size=49).move_to([0,-3.65,0])
            eq.set_color_by_tex(r"g(x)",GX)
            return VGroup(h,axes,gx,eq)
        if i==3:
            h=self.title("두 방향의 곱", "곡면에서 원형 대칭으로")
            axes=space_axes()
            gx=path([project(x,0,g(x)) for x in np.linspace(-3,3,100)],GX,5)
            gy=path([project(0,y,g(y)) for y in np.linspace(-3,3,100)],GY,5)
            gy.set_stroke(opacity=0)
            samples=VGroup()
            for x,y in [(-1.5,-1.2),(-1.5,1.2),(0,0),(1.5,-1.2),(1.5,1.2),(-.8,.6),(.8,-.6)]:
                samples.add(Line(project(x,y,0),project(x,y,g(x)*g(y)),color=PI,stroke_width=3))
            samples.set_stroke(opacity=0)
            mesh=surface_mesh();mesh.set_stroke(opacity=0)
            space=VGroup(axes,gx,gy,samples,mesh)
            eq=tex(r"z=g(x)g(y)",size=50).move_to([0,-3.75,0])
            eq.set_color_by_tex(r"g(x)",GX);eq.set_color_by_tex(r"g(y)",GY)
            note=text("가운데서 멀어질수록 낮아진다",23,MUTED).move_to([0,-4.55,0])
            return VGroup(h,space,eq,note)
        if i==4:
            h=self.title("넓이의 제곱", "두 방향의 작은 넓이를 곱한다")
            heat=VGroup()
            for ix in range(-5,6):
                for iy in range(-5,6):
                    x,y=ix*.48,iy*.48
                    op=.08+.74*g(x)*g(y)
                    sq=Square(side_length=.46,stroke_width=.4,stroke_color=EDGE,
                              fill_color=GX,fill_opacity=op).move_to([x,y+.65,0])
                    heat.add(sq)
            xlab=text("g(x) 방향의 넓이 A",22,GX).move_to([0,3.75,0])
            ylab=text("g(y) 방향의 넓이 A",22,GY).move_to([0,-2.55,0])
            eq=tex("V","=","A",r"\times","A","=","A^2",size=55).move_to([0,-3.75,0])
            for k in (2,4):eq[k].set_color(GX if k==2 else GY)
            return VGroup(h,heat,xlab,ylab,eq)
        if i==5:
            h=self.title("원형 고리의 합", "둘레에서 π가 등장한다")
            contours=top_contours()
            active=ring(.65)
            radial=Line([0,.65,0],[1.9,.65,0],color=PI,stroke_width=3)
            rlab=tex("r",size=34).move_to([1.15,.92,0]);rlab.set_color(PI)
            eq=self.fit(tex(r"dV=2\pi r\,e^{-r^2/2}\,dr",size=47)).move_to([0,-3.35,0])
            eq.set_color_by_tex(r"2\pi r",PI)
            note=text("고리 넓이 × 높이 = 작은 부피",23,MUTED).move_to([0,-4.15,0])
            return VGroup(h,contours,active,radial,rlab,eq,note)
        h=self.title("처음의 넓이로 돌아가기", "원 속에 숨어 있던 정규화 계수")
        axes=graph_axes((0,-.85),3.3)
        area=bell_area((0,-.85),.93,2.5)
        curve=bell(center=(0,-.85),width=.93,height=2.5)
        eq=tex("A^2","=",r"2\pi",size=65).move_to([0,3.7,0])
        eq[2].set_color(PI)
        full=tex(r"f(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}",size=48).move_to([0,-3.6,0])
        full.set_color_by_tex(r"\pi",PI)
        full.set_opacity(0)
        circles=VGroup(*[Circle(radius=r,color=PI,stroke_width=2,stroke_opacity=.25,
                                fill_opacity=0).move_to([0,-.85,0]) for r in (.65,1.25,1.85)])
        circles.set_stroke(opacity=0)
        return VGroup(h,axes,area,curve,eq,full,circles)

    def construct(self):
        footer=Rectangle(width=9,height=2.2,fill_color=PANEL,fill_opacity=1,stroke_width=0).move_to([0,-6.9,0])
        rule=Line([-4,5.85,0],[4,5.85,0],color=EDGE,stroke_width=1)
        self.add(footer,rule)
        visual=None;caption=None;last=-1;start=0
        for end,sentence in DATA["sentences"]:
            phase=self.phase(start);animations=[]
            if phase!=last:
                new=self.scene_for(phase)
                if visual is not None:animations.append(FadeOut(visual))
                animations.append(FadeIn(new));visual=new;last=phase
            new_caption=VGroup(*[text(line,28) for line in wrap(sentence)]).arrange(DOWN,buff=.1)
            self.fit(new_caption,8)
            new_caption.move_to([0,-6.58,0])
            if caption is not None:animations.append(FadeOut(caption))
            animations.append(FadeIn(new_caption));caption=new_caption
            duration=end-start;intro=min(.3,duration*.22)
            self.play(*animations,run_time=intro)
            extra=0
            if phase==0 and start==9:
                extra=1.0
                self.play(visual[3].animate.set_opacity(1),visual[4].animate.set_stroke(opacity=1),run_time=extra)
            elif phase==1 and start==18:
                extra=3.2
                shifted=bell(mu=.65,normalized=True,center=(0,-1.4))
                wide=bell(sigma=1.5,normalized=True,center=(0,-1.4))
                self.play(Transform(visual[3],shifted),run_time=1.5)
                self.play(Transform(visual[3],wide),run_time=1.7)
            elif phase==1 and start==23:
                extra=1.4
                next_curve=bell(center=(0,-1.4))
                next_eq=tex(r"g(x)=e^{-x^2/2}",size=49).move_to(visual[4])
                self.play(Transform(visual[3],next_curve),Transform(visual[4],next_eq),run_time=extra)
            elif phase==1 and start==32:
                extra=.9
                self.play(visual[2].animate.set_fill(opacity=.25),visual[6].animate.set_opacity(1),run_time=extra)
            elif phase==3 and start==50:
                extra=1.0
                self.play(visual[1][2].animate.set_stroke(opacity=1),run_time=extra)
            elif phase==3 and start==56:
                extra=1.8
                self.play(visual[1][3].animate.set_stroke(opacity=.9),run_time=.7)
                self.play(visual[1][4].animate.set_stroke(opacity=.75),run_time=1.1)
            elif phase==3 and start==68:
                extra=1.7
                top=VGroup(top_contours(),surface_mesh(top=True).set_stroke(opacity=.28))
                self.play(Transform(visual[1],top),run_time=extra)
            elif phase==3 and start in (74,79,83):
                extra=.7
                expr={74:r"g(x)g(y)=e^{-(x^2+y^2)/2}",
                      79:r"x^2+y^2=r^2",
                      83:r"z=e^{-r^2/2}"}[start]
                new=tex(expr,size=47).move_to(visual[2])
                if start==79:new.set_color_by_tex("r",PI)
                self.play(Transform(visual[2],new),run_time=extra)
            elif phase==5 and start in (126,134,138):
                extra=1.0
                r={126:1.2,134:1.8,138:2.45}[start]
                self.play(Transform(visual[2],ring(r)),run_time=extra)
            elif phase==5 and start==141:
                extra=.8
                new=self.fit(tex(r"V=2\pi\int_0^\infty r e^{-r^2/2}\,dr",size=42)).move_to(visual[5])
                new.set_color_by_tex(r"2\pi",PI)
                self.play(Transform(visual[5],new),run_time=extra)
            elif phase==5 and start==146:
                extra=.8
                new=self.fit(tex(r"u=r^2/2,\quad\int_0^\infty e^{-u}\,du=1",size=37)).move_to(visual[5])
                self.play(Transform(visual[5],new),run_time=extra)
            elif phase==5 and start==152:
                extra=.8
                new=tex(r"\boxed{V=2\pi}",size=61).move_to(visual[5])
                new.set_color_by_tex(r"\pi",PI)
                self.play(Transform(visual[5],new),run_time=extra)
            elif phase==6 and start==155:
                extra=.9
                new=tex(r"A=\sqrt{2\pi}",size=65).move_to(visual[4]);new.set_color_by_tex(r"\pi",PI)
                self.play(Transform(visual[4],new),run_time=extra)
            elif phase==6 and start==161:
                extra=1.3
                self.play(visual[5].animate.set_opacity(1),
                          Transform(visual[3],bell(normalized=True,center=(0,-.85),width=.93,height=2.5)),
                          visual[2].animate.set_fill(opacity=.1),run_time=extra)
            elif phase==6 and start==168:
                extra=.8
                self.play(visual[6].animate.set_stroke(opacity=.35),run_time=extra)
            self.wait(duration-intro-extra)
            start=end
        # Manim rounds the accumulated waits one frame short on this timeline.
        self.wait(1/30)
