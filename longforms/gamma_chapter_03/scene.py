"""Gaussian integral, from a one-dimensional area to concentric rings."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import (
    Annulus, Arrow, Circle, Create, DashedLine, Dot, FadeOut, Indicate, Line,
    MarkupText, Rectangle, Transform, TransformFromCopy, VGroup, VMobject,
    ValueTracker, always_redraw, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from longforms.gamma_chapter_01.scene import (
    BLUE, GOLD, GREEN, MUTED, PURPLE, RED, ChapterShot, eq, panel, text,
)
from longforms.gamma_chapter_02.scene import axes_at, axis_labels, decimal, half_factorial_frame, plot

DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
WHOLE = "∫<sub>−∞</sub><sup>∞</sup>"
POSITIVE = "∫<sub>0</sub><sup>∞</sup>"


def integral(body, x=0, y=0, size=51, color=GREEN):
    mob = MarkupText(body, font="Cambria Math", font_size=size, color=color)
    if mob.width > 13.7:
        mob.scale_to_fit_width(13.7)
    return mob.move_to([x,y,0])


def bell(u):
    return math.exp(-u*u)


def bell_graph(x, y, width=8.7, height=3, normalized=False):
    axes=axes_at(x,y,[-3.2,3.2,1],[0,1.08,.25],width,height)
    fn=(lambda u:bell(u)/math.sqrt(math.pi)) if normalized else bell
    graph=plot(axes,fn,-3.1,3.1,GREEN)
    return axes,graph


def wire_mesh(x=0, y=-.9, scale=1.25, tilt=.49):
    """Project a sampled Gaussian surface with an orthographic camera tilt."""
    theta=np.linspace(0,2*np.pi,65)
    radius=np.linspace(0,2.3,49)
    ct,st=np.cos(tilt),np.sin(tilt)

    def line(px,py,pz,opacity):
        xy=np.column_stack((x+scale*px,y+scale*(ct*py+2.45*st*pz),np.zeros_like(px)))
        return VMobject(stroke_color=GREEN,stroke_opacity=opacity,stroke_width=1.5).set_points_as_corners(xy)

    rings=VGroup(*(line(r*np.cos(theta),r*np.sin(theta),
                        np.full(theta.shape,np.exp(-r*r)),.68)
                   for r in np.linspace(.08,2.3,29)))
    spokes=VGroup(*(line(radius*np.cos(a),radius*np.sin(a),np.exp(-radius*radius),.24)
                    for a in np.linspace(0,2*np.pi,20,endpoint=False)))
    return VGroup(rings,spokes)


def radial_field(x=0,y=.1,scale=1):
    disks=VGroup()
    for r in np.linspace(2.2,.12,38):
        strength=.03+.13*bell(r)
        disks.add(Circle(radius=r*scale,stroke_width=0,fill_color=GREEN,fill_opacity=strength)
                  .move_to([x,y,0]))
    lines=VGroup(*(Circle(radius=r*scale,color=GREEN,stroke_opacity=.46,stroke_width=1.2)
                   .move_to([x,y,0]) for r in np.linspace(.42,2.2,6)))
    return VGroup(disks,lines)


def disk_grid(x,y):
    return VGroup(*(Line([x+i,y-2,0],[x+i,y+2,0],color=MUTED,stroke_opacity=.44,stroke_width=1)
                    for i in np.linspace(-2,2,11)),
                  *(Line([x-2,y+i,0],[x+2,y+i,0],color=MUTED,stroke_opacity=.44,stroke_width=1)
                    for i in np.linspace(-2,2,11)))


class GammaChapterThree(ChapterShot):
    data=DATA

    def setup(self):
        super().setup()
        self.header[0].become(text("GAMMA FUNCTION  /  CHAPTER 03",-5.2,3.83,18,MUTED))


class Shot01(GammaChapterThree):
    shot=0

    def s01(self):
        opening=half_factorial_frame()
        self.add(opening)
        self.play(Transform(opening[1],eq("(½)! = Γ(3/2)",-3.15,.65,65)),run_time=.7)
        self.to(5)
        self.play(Transform(opening[1],eq("(½)! = Γ(3/2) = ½ Γ(½)",-3.15,.65,55,
                                           colors={"½ Γ(½)":GOLD})),run_time=.8)
        self.to(11)
        self.play(FadeOut(opening),run_time=.4)
        self.show(eq("Γ(½)",y=1.11,size=80,color=GREEN))
        self.to(15)
        self.show(integral(f"Γ(½) = {POSITIVE} t<sup>−1/2</sup> e<sup>−t</sup> dt",y=-.13,size=65),
                  eq("½ − 1 = −½",y=-1.49,size=41,color=PURPLE))
        self.to(19)
        self.show(text("제곱근이 있는 적분을 어떻게 계산할까?",y=-2.14,size=25,color=MUTED))
        self.to(23)


class Shot02(GammaChapterThree):
    shot=1

    def s02(self):
        self.show(integral(f"Γ(½) = {POSITIVE} (1/√t)e<sup>−t</sup> dt",y=1.38,size=58))
        self.show(eq("t = u²    (u ≥ 0)",y=-.17,size=58,color=PURPLE))
        self.to(26)
        self.show(eq("1/√t = 1/u    (u > 0)",y=-1.61,size=49,color=BLUE))
        self.to(31)
        self.clear_body()
        left=-4.65
        def px(u):
            return left+4.4*u
        def tx(t):
            return left+2.2*t
        map_marks=VGroup(Line([left,.98,0],[4.65,.98,0],color=PURPLE),
                         Line([left,-.65,0],[4.65,-.65,0],color=BLUE),
                         eq("u",left-.65,.98,36,PURPLE),eq("t",left-.65,-.65,36,BLUE))
        for u in (0,.5,1,1.5,2):
            a,b=[px(u),.98,0],[tx(u*u),-.65,0]
            map_marks.add(DashedLine(a,b,color=MUTED,stroke_opacity=.55),
                          Dot(a,radius=.06,color=PURPLE),Dot(b,radius=.06,color=BLUE),
                          eq(f"{u:g}",a[0],1.37,27,PURPLE),eq(f"{u*u:g}",b[0],-1.05,27,BLUE))
        self.show(map_marks)
        self.show(Line([px(1),.98,0],[px(1.5),.98,0],color=PURPLE,stroke_width=9,stroke_opacity=.55),
                  Line([tx(1),-.65,0],[tx(2.25),-.65,0],color=BLUE,stroke_width=9,stroke_opacity=.55),
                  eq("dt/du = 2u    →    dt = 2u du",y=-1.93,size=43,color=GOLD))
        self.to(35)
        self.clear_body()
        top=integral(f"Γ(½) = {POSITIVE} e<sup>−t</sup>/√t dt",y=1.63,size=51)
        a=eq("u",-.59,.38,49,PURPLE)
        b=eq("u",2.17,.38,49,PURPLE)
        row=VGroup(integral(f"= {POSITIVE}  (1/",-2.17,.38,51),a,
                   integral(") e<sup>−u²</sup> · 2",.81,.38,51),b,eq("du",2.91,.38,45))
        row.arrange([1,0,0],buff=.07).move_to([0,.38,0])
        self.show(top,row)
        self.play(*(Create(Line(m.get_corner([-1,-1,0]),m.get_corner([1,1,0]),color=GOLD))
                    for m in (a,b)),run_time=.7)
        self.show(integral(f"= 2 {POSITIVE} e<sup>−u²</sup> du",y=-1.31,size=57))
        self.to(41)
        self.play(Indicate(row[2],color=PURPLE),run_time=.7)
        self.to(46)


class Shot03(GammaChapterThree):
    shot=2

    def s03(self):
        axes,graph=bell_graph(-1.15,.29,9.4,3.56)
        self.show(axes,axis_labels(axes,range(-3,4),(.25,.5,.75,1),left=-3.2),
                  text("최댓값 1",-.26,2.1,25,GOLD),
                  integral("e<sup>−u²</sup>",5.25,1.35,62))
        self.play(Create(graph),run_time=1.2)
        move=ValueTracker(.03)
        trace=always_redraw(lambda:VGroup(
            Dot(axes.c2p(move.get_value(),bell(move.get_value())),color=GOLD),
            Dot(axes.c2p(-move.get_value(),bell(move.get_value())),color=GOLD)))
        self.add(trace)
        self.play(move.animate.set_value(2.5),run_time=3,rate_func=linear)
        self.remove(trace)
        self.to(53)
        first=axes.get_area(graph,x_range=(0,3.1),color=GREEN,opacity=.32)
        second=axes.get_area(graph,x_range=(-3.1,0),color=GREEN,opacity=.32)
        self.show(first,eq("A",-.04,-.83,36))
        self.play(TransformFromCopy(first,second),run_time=.9)
        self.show(eq("A",-2.22,-.83,36),
                  integral(f"2 {POSITIVE} e<sup>−u²</sup> du = {WHOLE} e<sup>−u²</sup> du",
                           0,-2.1,43))
        self.to(61)
        self.show(text("가우스 적분",5.17,.16,29,GREEN))
        self.to(63)
        self.show(text("이 넓이를 어떻게 계산할까?",5.1,-.89,25,MUTED))
        self.to(68)


class Shot04(GammaChapterThree):
    shot=3

    def s04(self):
        self.show(integral(f"I = {WHOLE} e<sup>−u²</sup> du",y=.73,size=67))
        self.to(71)
        self.show(eq("I² = I × I",y=-.81,size=62,color=GOLD))
        self.to(75)
        self.clear_body()
        self.show(integral(f"{WHOLE} e<sup>−x²</sup> dx", -3.53,.63,57),
                  eq("×",0,.63,50,GOLD),
                  integral(f"{WHOLE} e<sup>−y²</sup> dy",3.5,.63,57))
        self.to(81)
        self.show(integral("I² = ∬<sub>ℝ²</sub> e<sup>−(x²+y²)</sup> dx dy",y=-1.15,size=61))
        self.to(86)
        self.clear_body()
        mesh=wire_mesh(-2.44,-.13,1.36,1.05)
        self.show(mesh,integral("z = e<sup>−(x²+y²)</sup>",4.26,1.05,52),
                  text("곡면 아래의 전체 부피",4.31,.01,30),
                  eq("V = I²",4.28,-.96,58,GOLD))
        self.to(92)


class Shot05(GammaChapterThree):
    shot=4

    def s05(self):
        tilt=ValueTracker(1.05)
        surface=always_redraw(lambda:wire_mesh(
            -2.44,-.13,1+(.36/1.05)*tilt.get_value(),tilt.get_value()))
        self.add(surface,integral("z = e<sup>−(x²+y²)</sup>",4.26,1.05,52),
                 text("곡면 아래의 전체 부피",4.31,.01,30),eq("V = I²",4.28,-.96,58,GOLD))
        self.play(tilt.animate.set_value(0),run_time=1.6,rate_func=linear)
        surface.clear_updaters()
        self.to(94)
        self.clear_body()
        cx,cy=-3.27,.03
        field=radial_field(cx,cy,.99)
        self.show(field,Line([cx-2.4,cy,0],[cx+2.4,cy,0],color=BLUE,stroke_opacity=.55),
                  Line([cx,cy-2.36,0],[cx,cy+2.36,0],color=RED,stroke_opacity=.55))
        angle=ValueTracker(.4)
        def target():
            return [cx+1.22*math.cos(angle.get_value()),cy+1.22*math.sin(angle.get_value()),0]
        scope=always_redraw(lambda:VGroup(Line([cx,cy,0],target(),color=PURPLE),
                                          Dot(target(),color=GOLD)))
        x_value=decimal(angle,math.cos,4.86,1.22,3,BLUE)
        y_value=decimal(angle,math.sin,4.86,.54,3,RED)
        self.add(scope,x_value,y_value,eq("x =",3.62,1.22,40,BLUE),eq("y =",3.62,.54,40,RED),
                 text("높이",2.9,-.55,28,GREEN),eq("e⁻¹ ≈ 0.3679",4.72,-.55,40,GREEN),
                 Circle(radius=1.22,color=GOLD,stroke_opacity=.6).move_to([cx,cy,0]))
        self.play(angle.animate.set_value(2*math.pi+.4),run_time=3.4,rate_func=linear)
        for mob in (scope,x_value,y_value):
            mob.clear_updaters()
        self.to(99)
        relation=eq("x² + y² = 1",4.09,-1.51,42,PURPLE)
        self.show(relation)
        self.to(105)
        self.play(Transform(relation,eq("x² + y² = r²",4.09,-1.51,45,PURPLE)),run_time=.7)
        self.to(110)
        self.show(text("같은 반지름 · 같은 높이",4.09,-2.18,26,GOLD))
        self.to(114)


class Shot06(GammaChapterThree):
    shot=5

    def s06(self):
        cy=.26
        cx=-3.68
        radial=3.66
        grid=disk_grid(cx,cy)
        self.show(radial_field(cx,cy,.89),grid,
                  Rectangle(width=.4,height=.4,stroke_width=0,fill_color=GOLD,fill_opacity=.9)
                  .move_to([cx+1,cy+.6,0]),
                  text("직교 격자",cx,2.47,26),eq("dA = dx dy",cx,-2.15,38))
        self.to(121)
        ring=Annulus(inner_radius=1.09,outer_radius=1.27,stroke_width=0,fill_color=GOLD,fill_opacity=.88)
        ring.move_to([radial,cy,0])
        self.show(radial_field(radial,cy,.89),ring,
                  text("반지름으로 나눈 원형 고리",radial,2.47,26),
                  Arrow([-1,.3,0],[1,.3,0],buff=.1,color=MUTED),
                  eq("dA = 2πr dr",radial,-2.15,38,GOLD))
        self.to(124)
        self.show(eq("r",radial+.43,.64,33,PURPLE),
                  Line([radial,cy,0],[radial+.76,cy+.78,0],color=PURPLE))
        self.to(127)
        self.play(grid.animate.set_opacity(.23),run_time=.7)
        self.show(text("고리 위 부피 ≈ 넓이 × e⁻ʳ²",0,2.02,25,GREEN))
        self.to(134)


class Shot07(GammaChapterThree):
    shot=6

    def s07(self):
        c=[-3.73,.16,0]
        ring=Annulus(inner_radius=1.41,outer_radius=1.59,stroke_width=0,fill_color=GOLD,fill_opacity=.85)
        self.show(ring.move_to(c),Dot(c,color=GOLD),Line(c,[-2.46,.77,0],color=PURPLE),
                  eq("r",-3.11,.73,34,PURPLE),text("둘레",1.97,1.47,33,GOLD),
                  eq("2πr",3.97,1.47,57,GOLD))
        self.to(136)
        self.show(panel(3.18,.19,6.03,.72),text("길이 2πr",3.18,.19,30),
                  text("두께 Δr",6.49,-.49,25,PURPLE),
                  text("넓이",1.7,-1.43,30,GOLD),eq("≈ 2πr Δr",3.97,-1.43,45,GOLD))
        self.to(141)
        self.play(Indicate(ring,color=GOLD),run_time=.8)
        self.show(text("원주율은 고리의 둘레에서 나온다",y=-2.17,size=25,color=GOLD))
        self.to(144)


class Shot08(GammaChapterThree):
    shot=7

    def s08(self):
        self.show(radial_field(-4.2,.04,.92))
        rings=VGroup(*(Circle(radius=r,color=GOLD,stroke_opacity=.53,stroke_width=2)
                       .move_to([-4.2,.04,0]) for r in np.linspace(.18,1.99,11)))
        for ring in rings:
            self.show(ring,run_time=.2)
        self.show(integral("dV = e<sup>−r²</sup> · 2πr dr",2.22,1.1,51))
        self.show(integral(f"I² = {POSITIVE} e<sup>−r²</sup> · 2πr dr",2.22,-.42,54))
        self.to(150)
        self.clear_body()
        self.show(integral(f"I² = π {POSITIVE} e<sup>−r²</sup> (2r dr)",y=1.27,size=62),
                  eq("s = r²    →    ds = 2r dr",y=.02,size=46,color=PURPLE))
        self.to(154)
        self.show(integral(f"= π {POSITIVE} e<sup>−s</sup> ds = π",y=-1.37,size=63,color=GOLD))
        self.to(159)


class Shot09(GammaChapterThree):
    shot=8

    def s09(self):
        axes,graph=bell_graph(4.01,.39,5.25,2.67)
        self.show(wire_mesh(-4.01,-.31,1.02,1.05),eq("I² = π",-4.0,-1.73,53,GOLD),
                  text("곡면 아래 부피",-4.03,2.31,24,MUTED))
        self.to(163)
        self.show(Arrow([-1,.15,0],[1,.15,0],buff=.1,color=MUTED),
                  axes,axes.get_area(graph,x_range=(-3.1,3.1),color=GREEN,opacity=.32),graph,
                  text("곡선 아래 넓이",4.03,2.31,24,MUTED),eq("I = √π",4.03,-1.73,54,GOLD))
        self.to(168)
        self.clear_body()
        self.show(eq("Γ(½) = I = √π",y=1.01,size=65,color=GREEN))
        self.to(172)
        result=eq("(½)! = ½ Γ(½) = √π / 2",y=-.77,size=68,colors={"√π / 2":GOLD})
        self.show(result)
        self.play(Indicate(result,color=GOLD),run_time=.7)
        self.to(178)


class Shot10(GammaChapterThree):
    shot=9

    def s10(self):
        self.show(eq("1 × 2 × ⋯ × n", -3.52,.54,63,GOLD),
                  Arrow([-.76,.53,0],[.76,.53,0],buff=.1,color=MUTED),
                  eq("F(x) = Γ(x+1)",3.48,.54,61,GREEN),
                  text("정수의 곱셈에서 연속적인 함수로",y=-1.13,size=29))
        self.to(183)
        self.clear_body()
        xs=(-5.38,-1.8,1.8,5.38)
        for i,(x,title,color) in enumerate(zip(xs,("곱셈","적분","공간","원형 대칭"),(GOLD,GREEN,BLUE,PURPLE))):
            self.show(panel(x,.19,3.1,3.95),text(title,x,1.77,26,color),run_time=.4)
            if i:
                self.show(eq("›",(xs[i-1]+x)/2,.26,40,MUTED),run_time=.2)
        mini_axes,mini_bell=bell_graph(xs[1],.24,2.35,1.51)
        ring=Annulus(inner_radius=.58,outer_radius=.79,stroke_width=0,fill_color=GOLD,fill_opacity=.9)
        self.show(eq("n!",xs[0],.4,65,GOLD),eq("1×2×⋯×n",xs[0],-.98,28),
                  mini_axes,mini_bell,mini_axes.get_area(mini_bell,x_range=(-3.1,3.1),color=GREEN,opacity=.26),
                  wire_mesh(xs[2],.04,.51,1.05),
                  ring.move_to([xs[3],.39,0]),eq("π",xs[3],-.99,40,GOLD))
        self.to(191)
        self.clear_body()
        for x,value,color,description in ((-4.38,"n!",GOLD,"이산적인 계산"),
                (0,"∫",GREEN,"공통된 표현"),(4.38,"π",PURPLE,"기하학적 구조")):
            self.show(Circle(radius=1.22,color=color).move_to([x,.35,0]),
                      eq(value,x,.35,83,color),text(description,x,-1.34,27,color))
        self.show(Line([-3.16,.35,0],[-1.22,.35,0],color=MUTED),
                  Line([1.22,.35,0],[3.16,.35,0],color=MUTED))
        self.to(197)


class Shot11(GammaChapterThree):
    shot=10

    def s11(self):
        left,graph=bell_graph(-4.05,.34,5.45,2.85)
        right,density=bell_graph(4.05,.34,5.45,2.85,normalized=True)
        self.show(left,graph,left.get_area(graph,x_range=(-3.1,3.1),color=GREEN,opacity=.32),
                  integral("e<sup>−x²</sup>",-4.05,2.1,49),
                  text("전체 넓이",-5.13,-1.62,27,GREEN),eq("= √π",-3.14,-1.62,39,GREEN))
        self.to(202)
        self.show(Arrow([-1.13,.39,0],[1.13,.39,0],buff=.06,color=MUTED),
                  eq("÷ √π",0,.89,37,GOLD),right,density,
                  right.get_area(density,x_range=(-3.1,3.1),color=GREEN,opacity=.32),
                  integral("e<sup>−x²</sup>/√π",4.05,2.1,49),
                  text("전체 넓이",3.13,-1.62,27,GOLD),eq("= 1",4.96,-1.62,39,GOLD))
        self.to(207)
        self.show(text("적분으로 전체 넓이를 구하고 1로 맞춘다",y=-2.18,size=27,color=GREEN))
        self.to(212)
