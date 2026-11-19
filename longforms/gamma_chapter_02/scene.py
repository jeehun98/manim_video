"""Gamma chapter two, aligned to the 214-second narration."""
import json
import math
import sys
from pathlib import Path

from manim import (
    Arrow, Axes, Circle, Create, DashedLine, DecimalNumber, Dot, FadeOut, Indicate,
    Line, SurroundingRectangle, Text, Transform, ValueTracker, VGroup,
    always_redraw, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from longforms.gamma_chapter_01.scene import (
    BLUE, GOLD, GREEN, MUTED, PURPLE, RED, ChapterShot, eq, panel, text,
    transition_rules,
)

DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
TERMS = {"tⁿ⁻¹": BLUE, "tⁿ": BLUE, "t²": BLUE, "e⁻ᵗ": RED, "n ·": GOLD}


def axes_at(x, y, xr, yr, width=8, height=3):
    axes = Axes(x_range=xr, y_range=yr, x_length=width, y_length=height,
                tips=False, axis_config={"color": MUTED, "stroke_width": 1.6})
    axes.move_to([x,y,0])
    return axes


def plot(axes, fn, xmin, xmax, color):
    return axes.plot(fn,x_range=[xmin,xmax,(xmax-xmin)/100],color=color,stroke_width=3.5)


def axis_labels(axes, xs, ys, *, bottom=0, left=0):
    return VGroup(
        *(eq(f"{x:g}",axes.c2p(x,bottom)[0],axes.c2p(x,bottom)[1]-.23,20,MUTED) for x in xs),
        *(eq(f"{y:g}",axes.c2p(left,y)[0]-.25,axes.c2p(left,y)[1],20,MUTED) for y in ys),
    )


def area(axes, graph, end, color=GREEN):
    return axes.get_area(graph,x_range=(0,end),color=color,opacity=.28)


def decimal(tracker, fn, x, y, places, color):
    mob = DecimalNumber(fn(tracker.get_value()),num_decimal_places=places,
                        mob_class=Text,font_size=35,color=color)
    mob.add_updater(lambda number: number.set_value(fn(tracker.get_value())).move_to([x,y,0]))
    return mob.move_to([x,y,0])


def product(t, n=2):
    return t**n*math.exp(-t)


def gamma_variant(x,a):
    return math.gamma(x)*(1+a*math.sin(2*math.pi*x))


class GammaChapterTwo(ChapterShot):
    data = DATA

    def setup(self):
        super().setup()
        self.header[0].become(text("GAMMA FUNCTION  /  CHAPTER 02",-5.2,3.83,18,MUTED))


class Shot01(GammaChapterTwo):
    shot = 0

    def s01(self):
        factorial, divider, derivative, question=transition_rules()
        self.add(factorial,divider,derivative,question)
        self.to(1)
        self.play(Indicate(factorial[1],color=GOLD),run_time=.8)
        self.to(6)
        moving=eq("n",1.9,-.59,38,BLUE)
        self.add(moving)
        self.play(Transform(moving,eq("n",.52,-.85,58,GOLD)),run_time=.7)
        self.play(FadeOut(moving),Indicate(derivative[1],color=BLUE),run_time=.6)
        self.to(12)
        self.play(Transform(question[1],text("현재 수를 곱하고 한 단계 낮춘다",y=-2.05,size=26)),
                  run_time=.6)
        self.to(19)


class Shot02(GammaChapterTwo):
    shot = 1

    def s02(self):
        self.show(eq("tⁿ   →   ∫₀∞ tⁿ dt",y=.7,size=68,colors=TERMS))
        self.to(22)
        self.show(eq("n > 0",y=-.72,size=39,color=PURPLE))
        self.to(25)
        self.show(eq("d/dt  tⁿ = n · tⁿ⁻¹",y=-1.74,size=49,colors=TERMS))
        self.to(31)
        self.clear_body()
        axes=axes_at(-2.65,.23,[0,5.1,1],[0,27,5],8.2,3.6)
        graph=plot(axes,lambda t:t*t,0,5,BLUE)
        upper=ValueTracker(.25)
        fill=always_redraw(lambda:area(axes,graph,upper.get_value(),BLUE))
        guide=always_redraw(lambda:DashedLine(axes.c2p(upper.get_value(),0),
            axes.c2p(upper.get_value(),upper.get_value()**2),color=GOLD))
        value=decimal(upper,lambda t:t**3/3,5.34,-.43,3,BLUE)
        limit=decimal(upper,lambda t:t,4.75,.52,1,GOLD)
        self.add(axes,axis_labels(axes,range(6),(5,10,15,20,25)),fill,graph,guide,
                 eq("t²", -5.4,1.77,42,BLUE),eq("T =",3.75,.52,42,GOLD),limit,
                 eq("T³/3 =",3.36,-.43,43),value)
        self.play(upper.animate.set_value(5),run_time=5.5,rate_func=linear)
        for mob in (fill,guide,value,limit):
            mob.clear_updaters()
        self.to(38)
        self.show(text("증가를 억제할 함수가 필요하다",4.01,-1.55,25,RED))
        self.to(42)


class Shot03(GammaChapterTwo):
    shot = 2

    def s03(self):
        axes=axes_at(-2.6,.25,[0,12.3,2],[0,.65,.2],8.5,3.8)
        decay_axes=axes_at(-2.6,.25,[0,6.2,2],[0,1.1,.25],8.5,3.8)
        self.show(decay_axes,axis_labels(decay_axes,(0,2,4,6),(.5,1)),
                  eq("g(t) = e⁻ᵗ",4.38,.82,58,RED))
        self.play(Create(plot(decay_axes,lambda t:math.exp(-t),0,6,RED)),run_time=1)
        self.to(46)
        self.show(text("t가 커질수록 빠르게 0에 접근",4.38,-.54,26,MUTED))
        self.to(49)
        self.clear_body()
        graph=plot(axes,product,0,12,GREEN)
        tracker=ValueTracker(.3)
        glider=always_redraw(lambda:VGroup(
            DashedLine(axes.c2p(tracker.get_value(),0),axes.c2p(tracker.get_value(),product(tracker.get_value())),color=MUTED),
            Dot(axes.c2p(tracker.get_value(),product(tracker.get_value())),color=GOLD)))
        vals=VGroup(decimal(tracker,lambda t:t,5.66,1.84,1,GOLD),
                    decimal(tracker,lambda t:t*t,5.66,.9,2,BLUE),
                    decimal(tracker,lambda t:math.exp(-t),5.66,-.02,5,RED),
                    decimal(tracker,product,5.66,-.98,5,GREEN))
        self.add(axes,axis_labels(axes,range(0,13,2),(.2,.4,.6)),
                 area(axes,graph,12),graph,glider,*vals,
                 eq("t =",3.75,1.84,38,GOLD),eq("t² =",3.75,.9,38,BLUE),
                 eq("e⁻ᵗ =",3.75,-.02,38,RED),eq("t²e⁻ᵗ =",3.75,-.98,38,GREEN))
        self.play(tracker.animate.set_value(2),run_time=3,rate_func=linear)
        self.play(tracker.animate.set_value(11),run_time=4,rate_func=linear)
        for mob in (glider,*vals):
            mob.clear_updaters()
        self.to(59)
        self.play(FadeOut(glider),run_time=.4)
        self.show(eq("∫₀∞ t²e⁻ᵗ dt = 2",4.05,-1.91,39,GREEN))
        self.to(63)


class Shot04(GammaChapterTwo):
    shot = 3

    def s04(self):
        axes=axes_at(-2.55,.25,[0,6.2,2],[-1.1,1.1,1],8.2,3.6)
        self.show(axes,axis_labels(axes,(0,2,4,6),(-1,1)),
                  plot(axes,lambda t:math.exp(-t),0,6,RED),
                  eq("e⁻ᵗ",-5.1,1.71,43,RED))
        self.to(66)
        self.play(Create(plot(axes,lambda t:-math.exp(-t),0,6,RED)),run_time=.9)
        self.show(eq("−e⁻ᵗ",-5.06,-1.38,38,RED),
                  eq("∫ e⁻ᵗ dt = −e⁻ᵗ + C",4.19,.55,42,colors=TERMS),
                  text("그래프는 C = 0",4.19,-.45,25,MUTED))
        self.to(71)
        self.clear_body()
        self.show(eq("Iₙ = ∫₀∞ tⁿe⁻ᵗ dt",y=.52,size=76, color=GREEN,colors=TERMS),
                  text("곱을 적분해 얻는 전체 넓이",y=-1.05,size=31))
        self.to(77)


class Shot05(GammaChapterTwo):
    shot = 4

    def s05(self):
        self.show(eq("Iₙ = ∫₀∞ tⁿe⁻ᵗ dt",y=1.77,size=57,colors=TERMS))
        self.to(79)
        self.show(eq("∫ u dv = uv − ∫ v du",y=.35,size=59),
                  text("한쪽은 미분하고, 다른 쪽은 적분한다",y=-1.04,color=MUTED))
        self.to(86)
        self.clear_body()
        left=VGroup(panel(-3.66,.31,6.16,3.65),text("거듭제곱을 미분",-3.66,1.52,28,BLUE),
                    eq("u = tⁿ",-3.66,.62,58,BLUE))
        right=VGroup(panel(3.66,.31,6.16,3.65),text("지수함수를 적분",3.66,1.52,28,RED),
                     eq("dv = e⁻ᵗ dt",3.66,.62,58,RED))
        self.show(left,right)
        self.to(90)
        self.show(eq("du = n · tⁿ⁻¹ dt",-3.66,-.64,53,BLUE,TERMS))
        self.to(96)
        self.show(eq("v = −e⁻ᵗ",3.66,-.64,53,RED))
        self.to(99)


class Shot06(GammaChapterTwo):
    shot = 5

    def s06(self):
        axes=axes_at(-2.55,.24,[0,13.2,2],[0,.65,.2],8.4,3.45)
        graph=plot(axes,product,0,13,GREEN)
        self.show(axes,axis_labels(axes,(0,2,4,6,8,10,12),(.2,.4,.6)),graph,
                  eq("[−tⁿe⁻ᵗ]₀∞",4.05,1.38,52,colors=TERMS),
                  eq("n > 0",4.05,.72,31,MUTED))
        for t,y,value in ((0,.03,"t → 0⁺"),(13,-.81,"t → ∞")):
            point=axes.c2p(t,0)
            self.show(Arrow(point+[.42 if t==0 else -.55,.94,0],point,buff=.06,color=GOLD),
                      eq(value,4.05,y,40,GOLD))
        self.to(105)
        self.clear_body()
        boundary=eq("[−tⁿe⁻ᵗ]₀∞",.8,1.41,52,MUTED,TERMS)
        lead=eq("Iₙ =", -2.42,1.41,53)
        integral=eq("+ ∫₀∞ n tⁿ⁻¹e⁻ᵗ dt",y=-.11,size=61,colors=TERMS)
        self.show(lead,boundary,integral)
        self.play(Transform(boundary,eq("0   (n > 0)",.8,1.41,41,MUTED)),run_time=.7)
        self.play(FadeOut(boundary),FadeOut(lead),
                  Transform(integral,eq("Iₙ = ∫₀∞ n tⁿ⁻¹e⁻ᵗ dt",y=.08,size=61,colors=TERMS)),
                  run_time=.7)
        self.to(110)
        self.play(Transform(integral,eq("Iₙ = n · ∫₀∞ tⁿ⁻¹e⁻ᵗ dt",y=.08,size=61,colors=TERMS)),
                  run_time=.7)
        self.to(116)
        recurrence=eq("Iₙ = n · Iₙ₋₁",y=-1.47,size=61,color=GREEN,colors=TERMS)
        self.show(recurrence)
        self.to(120)
        self.show(eq("n! = n · (n−1)!",y=1.52,size=57,color=GOLD))
        self.play(Indicate(recurrence,color=GOLD),run_time=.9)
        self.to(124)


class Shot07(GammaChapterTwo):
    shot = 6

    def s07(self):
        axes=axes_at(-2.7,.16,[0,13.3,2],[0,5,1],8.1,3.8)
        current=plot(axes,lambda t:product(t,0),0,13,GREEN)
        fill=area(axes,current,13)
        result=eq("I₀ = 1",4.41,.65,63,GREEN)
        name=eq("e⁻ᵗ",-5.76,1.62,36,RED)
        self.show(axes,axis_labels(axes,(0,2,4,6,8,10,12),(1,2,3,4,5)),fill,current)
        self.to(126)
        self.show(result,name,text("전체 넓이",4.35,1.62,27,MUTED))
        self.to(130)
        exps=("","¹","²","³","⁴")
        subs=("₀","₁","₂","₃","₄")
        for n, end in ((1,133),(2,136),(3,137),(4,138)):
            new=plot(axes,lambda t:product(t,n),0,13,GREEN)
            expression=f"I{subs[n]} = {n} × {math.factorial(n-1)} = {math.factorial(n)}"
            self.play(Transform(current,new),Transform(fill,area(axes,new,13)),
                      Transform(result,eq(expression,4.2,.65,46,GREEN)),
                      Transform(name,eq(f"t{exps[n]}e⁻ᵗ",-5.76,1.62,33,colors=TERMS)),
                      run_time=.6)
            self.to(end)
        self.show(eq("1 → 1 → 2 → 6 → 24",4.15,-.88,41,GOLD),
                  text("색칠은 화면에 보이는 구간",4.15,-1.74,22,MUTED))
        self.to(141)


class Shot08(GammaChapterTwo):
    shot = 7

    def s08(self):
        self.show(eq("Iₙ = ∫₀∞ tⁿe⁻ᵗ dt",y=.74,size=66,colors=TERMS),
                  eq("F(x) = ∫₀∞ tˣe⁻ᵗ dt",y=-.63,size=66,colors={"ˣ":PURPLE,"e⁻ᵗ":RED}))
        self.to(146)
        self.clear_body()
        left=axes_at(-3.92,.48,[0,8.25,2],[0,.65,.2],5.85,2.75)
        right=axes_at(3.95,.48,[1,2.05,.25],[.9,2.12,.25],5.85,2.75)
        tracker=ValueTracker(1)
        shape=always_redraw(lambda:plot(left,lambda t:product(t,tracker.get_value()),0,8,GREEN))
        fill=always_redraw(lambda:area(left,shape,8))
        dot=always_redraw(lambda:Dot(right.c2p(tracker.get_value(),math.gamma(tracker.get_value()+1)),
                                     color=PURPLE,radius=.09).set_z_index(4))
        value=decimal(tracker,lambda x:math.gamma(x+1),-2.33,-1.49,4,GREEN)
        parameter=decimal(tracker,lambda x:x,4.45,-1.49,2,PURPLE)
        self.add(left,right,axis_labels(left,(0,2,4,6,8),(.2,.4,.6)),
                 axis_labels(right,(1,1.5,2),(1,1.5,2),bottom=.9,left=1),
                 plot(right,lambda x:math.gamma(x+1),1,2,GREEN),fill,shape,dot,value,parameter,
                 text("전체 넓이",-4.65,-1.49,27,GREEN),eq("x =",3.2,-1.49,36,PURPLE),
                 text("적분 안의 함수",-3.92,2.26,25,MUTED),
                 eq("F(x) = Γ(x+1)",3.95,2.26,34,GREEN),
                 text("색칠은 화면에 보이는 구간",-3.92,-2.11,21,MUTED),
                 Arrow([-.57,.45,0],[.58,.45,0],buff=.1,color=MUTED))
        self.play(tracker.animate.set_value(2),run_time=7.3,rate_func=linear)
        for mob in (shape,fill,dot,value,parameter):
            mob.clear_updaters()
        self.to(154)
        self.show(eq("F(x+1) = (x+1) F(x)",3.95,-2.07,32,GOLD))
        self.to(160)


class Shot09(GammaChapterTwo):
    shot = 8

    def s09(self):
        gamma=eq("Γ(x)",y=1.48,size=79,color=GREEN)
        self.show(gamma,text("감마함수",y=.24,size=37))
        self.to(163)
        self.show(eq("Γ(x) = ∫₀∞ tˣ⁻¹e⁻ᵗ dt",y=-.73,size=59,
                     colors={"ˣ⁻¹":PURPLE,"e⁻ᵗ":RED}),eq("x > 0",y=-1.7,size=34,color=MUTED))
        self.to(169)
        self.clear_body()
        self.show(eq("Γ(n+1) = ∫₀∞ tⁿe⁻ᵗ dt",y=.93,size=62,colors=TERMS),
                  eq("n! = Γ(n+1)",y=-.62,size=77,color=GOLD))
        self.to(174)


class Shot10(GammaChapterTwo):
    shot = 9

    def s10(self):
        axes=axes_at(-2.57,.27,[1,5.15,1],[0,30,5],8.45,3.56)
        self.show(axes,axis_labels(axes,(1,2,3,4,5),(5,10,15,20,25),left=1))
        self.play(*(Create(plot(axes,lambda x:gamma_variant(x,0),1,5,GREEN)),
                    Create(plot(axes,lambda x:gamma_variant(x,.25),1,5,PURPLE)),
                    Create(plot(axes,lambda x:gamma_variant(x,-.25),1,5,RED))),run_time=1.1)
        self.show(*(Dot(axes.c2p(x,math.gamma(x)),color=GOLD).set_z_index(4) for x in range(1,6)),
                  eq("Γ(x)[1 + a sin(2πx)]",4.2,1.22,39),
                  text("정수값과 재귀를 모두 유지",4.22,.27,26),
                  eq("−1 < a < 1",4.2,-.61,36,PURPLE))
        self.to(181)
        self.clear_body()
        axes=axes_at(-2.7,.1,[1,3.2,.5],[-.24,.93,.25],8.2,3.4)
        a,b=1.25,2.85
        x=(a+b)/2
        low,high=math.lgamma(a),math.lgamma(b)
        self.show(axes,axis_labels(axes,(1,1.5,2,2.5,3),(.25,.5,.75),bottom=-.24,left=1),
                  plot(axes,math.lgamma,1,3.15,GREEN),
                  Line(axes.c2p(a,low),axes.c2p(b,high),color=GOLD),
                  Dot(axes.c2p(x,math.lgamma(x)),color=GREEN),
                  DashedLine(axes.c2p(x,math.lgamma(x)),axes.c2p(x,(low+high)/2),color=MUTED),
                  eq("log Γ(x)",4.13,1.27,54,GREEN),
                  text("곡선 위 두 점을 이은 선분은",4.11,.29,25),
                  text("그 사이의 곡선보다 위에 있다",4.11,-.38,25,GOLD))
        self.to(187)
        self.clear_body()
        items=(( "로그 볼록성", "log f", GREEN),
               ( "재귀 관계", "f(x+1) = x f(x)", GOLD),
               ( "초기값", "f(1) = 1", PURPLE))
        for i,(title,value,color) in enumerate(items):
            x=(i-1)*4.7
            self.show(panel(x,.57,4.15,1.86),text(title,x,1.12,26,color),
                      eq(value,x,.33,39,color))
        self.show(text("양의 실수에서 정의된 양의 함수  f",y=2.13,size=26,color=MUTED),
                  eq("f(x) = Γ(x)",y=-.89,size=62,color=GREEN))
        self.to(194)
        self.show(text("보어–몰레루프 정리",y=-1.97,size=31))
        self.to(197)


def half_factorial_frame():
    """Shared body layout for the next chapter's opening."""
    circle=Circle(radius=1.42,color=MUTED,stroke_opacity=.64).move_to([4.21,.28,0])
    return VGroup(
        text("계산하고 싶은 값",-3.15,1.65,28,MUTED),
        eq("(½)! = ½ Γ(½)",-3.15,.65,65),
        eq("Γ(½) = ∫₀∞ (1/√t)e⁻ᵗ dt",-3.15,-.68,49,GREEN),
        Line([1.47,-1.34,0],[1.47,1.86,0],color=MUTED,stroke_opacity=.4),
        circle,eq("π",4.21,.28,102,PURPLE),
        Line([4.21,.28,0],[5.63,.28,0],color=PURPLE),
        panel(0,-2.02,9.1,.6),text("왜 팩토리얼을 계산하는 데 원주율이 등장할까?",y=-2.02,size=27),
    )


class Shot11(GammaChapterTwo):
    shot = 10

    def s11(self):
        self.show(eq("n! = ∫₀∞ tⁿe⁻ᵗ dt",y=.56,size=68,colors=TERMS))
        self.to(203)
        self.show(eq("(½)! = ?",y=-.94,size=65,color=PURPLE))
        self.to(208)
        self.clear_body()
        scene=half_factorial_frame()
        self.show(*scene[:4])
        self.play(Create(scene[4]),run_time=.9)
        self.show(*scene[5:],run_time=.6)
        self.to(214)
