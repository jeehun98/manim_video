"""Gamma chapter four, from area normalization to waiting-time densities."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import (
    Arrow, Circle, Create, DashedLine, Dot, FadeOut, Indicate, Line, Rectangle,
    Transform, ValueTracker, VGroup, always_redraw, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from longforms.gamma_chapter_01.scene import (
    BLUE, GOLD, GREEN, MUTED, PURPLE, RED, ChapterShot, eq, panel, text,
)
from longforms.gamma_chapter_02.scene import axes_at, axis_labels, decimal, plot
from longforms.gamma_chapter_03.scene import POSITIVE, WHOLE, bell, bell_graph, integral

DATA=json.loads((HERE/"timing.json").read_text(encoding="utf-8"))
PALETTE=(BLUE,PURPLE,GREEN,GOLD)
POWERS=("","t","t²","t³")


def kernel(t,alpha):
    return t**(alpha-1)*math.exp(-t)


def density(t,alpha):
    return kernel(t,alpha)/math.gamma(alpha)


def shade(axes,graph,a,b,color=GREEN):
    return axes.get_area(graph,x_range=(a,b),color=color,opacity=.31)


def time_axes(x=-2.6,y=.2,width=8.3,height=3.6,maximum=10,top=1.08):
    tick=2 if maximum>=8 else 1
    return axes_at(x,y,[0,maximum,tick],[0,top,.25 if top<1.2 else .5],width,height)


def timeline(y,events,start=-4.93,end=5.96,active=0):
    axis=Line([start,y,0],[end,y,0],color=MUTED,stroke_width=1.8)
    points=VGroup(*(Dot([start+(end-start)*fraction,y,0],
                        radius=.082,color=GOLD if i==active else GREEN)
                    for i,fraction in enumerate(events)))
    return VGroup(axis,points)


def person(x,y,color):
    return VGroup(Circle(radius=.19,color=color).move_to([x,y+.48,0]),
                  Line([x,y+.29,0],[x,y-.27,0],color=color),
                  Line([x-.25,y+.02,0],[x,y+.2,0],color=color),
                  Line([x,y+.2,0],[x+.25,y+.02,0],color=color),
                  Line([x-.23,y-.56,0],[x,y-.27,0],color=color),
                  Line([x,y-.27,0],[x+.23,y-.56,0],color=color))


def gaussian_opening():
    left,graph=bell_graph(-4.05,.34,5.45,2.85)
    right,normalized=bell_graph(4.05,.34,5.45,2.85,normalized=True)
    return VGroup(
        left,graph,left.get_area(graph,x_range=(-3.1,3.1),color=GREEN,opacity=.32),
        integral("e<sup>−x²</sup>",-4.05,2.1,49),
        text("전체 넓이",-5.13,-1.62,27,GREEN),eq("= √π",-3.14,-1.62,39,GREEN),
        Arrow([-1.13,.39,0],[1.13,.39,0],buff=.06,color=MUTED),eq("÷ √π",0,.89,37,GOLD),
        right,normalized,right.get_area(normalized,x_range=(-3.1,3.1),color=GREEN,opacity=.32),
        integral("e<sup>−x²</sup>/√π",4.05,2.1,49),
        text("전체 넓이",3.13,-1.62,27,GOLD),eq("= 1",4.96,-1.62,39,GOLD),
        text("적분으로 전체 넓이를 구하고 1로 맞춘다",y=-2.18,size=27,color=GREEN),
    )


class GammaChapterFour(ChapterShot):
    data=DATA

    def setup(self):
        super().setup()
        self.header[0].become(text("GAMMA FUNCTION  /  CHAPTER 04",-5.2,3.83,18,MUTED))


class Shot01(GammaChapterFour):
    shot=0

    def s01(self):
        self.add(gaussian_opening())
        self.to(5)
        self.clear_body()
        self.show(text("곡선 아래의 넓이를 확률로 읽으려면?",y=.43,size=46))
        self.to(10)
        self.clear_body()
        axes=axes_at(-2.43,.26,[-3.2,3.2,1],[0,.63,.2],8.3,3.5)
        graph=plot(axes,lambda x:bell(x)/math.sqrt(math.pi),-3.1,3.1,BLUE)
        bound=ValueTracker(.5)
        fill=always_redraw(lambda:shade(axes,graph,-bound.get_value(),bound.get_value(),BLUE))
        guides=always_redraw(lambda:VGroup(*(DashedLine(
            axes.c2p(side*bound.get_value(),0),
            axes.c2p(side*bound.get_value(),bell(bound.get_value())/math.sqrt(math.pi)),color=GOLD)
            for side in (-1,1))))
        value=decimal(bound,lambda t:100*math.erf(t),4.12,-.15,1,BLUE)
        self.add(axes,axis_labels(axes,range(-3,4),(.2,.4,.6),left=-3.2),graph,fill,guides,value,
                 eq("%",5.1,-.15,36,BLUE),
                 text("색칠한 구간의 확률",4.27,.88,29))
        self.play(bound.animate.set_value(1),run_time=3,rate_func=linear)
        self.show(eq("−1 ≤ X ≤ 1",4.25,-1.11,39,GOLD))
        for mob in (fill,guides,value):
            mob.clear_updaters()
        self.to(17)
        self.play(FadeOut(fill),FadeOut(guides),FadeOut(value),
                  run_time=.4)
        self.clear_body()
        self.show(integral(f"{WHOLE} p(x) dx = 1",y=.42,size=76),
                  text("가능한 모든 값의 확률을 더하면 1",y=-1.24,size=31))
        self.to(21)


class Shot02(GammaChapterFour):
    shot=1

    def s02(self):
        axes,original=bell_graph(-2.51,.23,8.5,3.54)
        self.show(axes,original,shade(axes,original,-3.1,3.1),
                  integral("e<sup>−x²</sup>",4.11,1.13,58),
                  text("전체 넓이",3.05,-.26,28,GREEN),eq("√π",4.89,-.26,50,GOLD))
        self.to(25)
        self.show(text("모든 높이를 √π로 나눈다",4.11,-1.42,28,BLUE))
        self.to(30)
        self.clear_body()
        multiplier=ValueTracker(1)
        baseline=plot(axes,bell,-3.1,3.1,MUTED).set_stroke(opacity=.45)
        graph=always_redraw(lambda:plot(axes,lambda x:multiplier.get_value()*bell(x),-3.1,3.1,BLUE))
        fill=always_redraw(lambda:shade(axes,graph,-3.1,3.1,BLUE))
        value=decimal(multiplier,lambda k:k*math.sqrt(math.pi),4.23,-.32,4,BLUE)
        self.add(axes,baseline,fill,graph,value,text("전체 적분값",4.23,.69,29))
        self.play(multiplier.animate.set_value(1/math.sqrt(math.pi)),run_time=4.2,rate_func=linear)
        for mob in (graph,fill,value):
            mob.clear_updaters()
        self.to(35)
        self.show(text("정규화",4.23,-1.37,36,GOLD))
        self.to(40)
        self.clear_body()
        note=text("원래의 전체 넓이  √π가 정규화 상수가 된다",y=-1.9,size=27,color=GOLD)
        self.show(integral(f"{WHOLE} e<sup>−x²</sup> dx = √π",y=1.14,size=61),
                  integral("p(x) = e<sup>−x²</sup> / √π",y=-.42,size=66,color=BLUE),
                  note)
        self.to(47)
        self.play(Transform(note,text("감마 적분에서도 전체 넓이로 나눌 수 있을까?",
                  y=-1.9,size=27,color=GOLD)),run_time=.6)
        self.to(51)


class Shot03(GammaChapterFour):
    shot=2

    def s03(self):
        self.show(timeline(-1.58,(.09,.23,.46,.54,.84)),
                  text("도착 시각",-5.4,-2.02,24,MUTED))
        self.to(56)
        self.show(panel(-4.26,.56,3.2,2.7),
                  text("상점",-4.26,1.5,32),
                  Rectangle(width=.78,height=1.19,color=MUTED,stroke_width=1.4)
                  .move_to([-3.69,.35,0]),
                  person(-.79,.53,GOLD),person(1.39,.53,MUTED),person(3.57,.53,MUTED),
                  Arrow([-1.24,.53,0],[-2.62,.53,0],buff=.1,color=GOLD))
        self.to(59)
        self.clear_body()
        trials=((.08,.22,.32,.59,.82),(.17,.21,.47,.7,.93),(.035,.36,.46,.56,.84))
        for i,(y,times) in enumerate(zip((1.46,.38,-.72),trials),1):
            row=timeline(y,times)
            self.show(row,text(f"시행 {i}",-5.98,y,23,MUTED),
                      Line([-4.93,y-.24,0],row[1][0].get_center()+[0,-.24,0],
                           color=GOLD,stroke_width=3))
        self.show(text("같은 조건에서도 대기 시간은 매번 달라진다",y=-1.77,size=27))
        self.to(67)
        self.show(text("포아송 과정 · 발생률 λ = 1",y=-2.25,size=24,color=GOLD))
        self.to(73)


class Shot04(GammaChapterFour):
    shot=3

    def s04(self):
        axes=time_axes(maximum=6)
        graph=plot(axes,lambda t:math.exp(-t),0,5.99,BLUE)
        rng=np.random.default_rng(414)
        bins=np.linspace(0,6,25)
        samples=rng.exponential(size=5000)
        counts,_=np.histogram(samples,bins)
        hist=VGroup()
        for k,count in enumerate(counts):
            lo,hi=bins[k:k+2]
            h=count/(len(samples)*(hi-lo))
            if h>0:
                bottom=axes.c2p(lo,0)
                top=axes.c2p(hi,h)
                hist.add(Rectangle(width=top[0]-bottom[0],height=top[1]-bottom[1],
                                   stroke_width=.5,stroke_color=GREEN,fill_color=GREEN,fill_opacity=.35)
                         .move_to((bottom+top)/2))
        self.show(axes,axis_labels(axes,range(7),(.25,.5,.75,1)),hist)
        self.play(Create(graph),run_time=1.2)
        self.show(eq("p₁(t) = e⁻ᵗ",4.18,1.19,53,BLUE),
                  text("모의실험 5,000회",4.18,.22,24,GREEN))
        self.to(79)
        self.show(text("짧은 대기 시간에서 밀도가 높다",4.16,-1.22,25))
        self.to(84)


class Shot05(GammaChapterFour):
    shot=4

    def s05(self):
        self.show(timeline(1.16,(.32,)),text("첫 번째 손님까지",0,1.73,29,BLUE))
        self.to(89)
        self.show(timeline(-.39,(.32,.66),active=1),
                  text("두 번째 손님까지",0,.18,29,PURPLE),
                  eq("T₂ = X₁ + X₂",y=-1.56,size=48,color=GOLD))
        self.to(93)
        self.clear_body()
        axes=time_axes(maximum=8)
        a=plot(axes,lambda t:density(t,1),0,8,BLUE)
        b=plot(axes,lambda t:density(t,2),0,8,PURPLE)
        self.show(axes,axis_labels(axes,(0,2,4,6,8),(.25,.5,.75,1)),a,b,
                  shade(axes,a,0,.64,BLUE),shade(axes,b,0,.64,PURPLE),
                  eq("p₁(t) = e⁻ᵗ",4.58,.88,48,BLUE),
                  eq("p₂(t) = te⁻ᵗ",4.58,-.34,48,PURPLE))
        self.to(99)
        self.clear_body()
        left,right=-5.8,.93
        for i,fraction in enumerate((.13,.31,.52,.68,.87)):
            y=1.84-i*.61
            s=left+(right-left)*fraction
            self.show(Line([left,y,0],[s,y,0],color=BLUE,stroke_width=4),
                      Line([s,y,0],[right,y,0],color=PURPLE,stroke_width=4),
                      Dot([s,y,0],color=GREEN),Dot([right,y,0],color=GOLD),run_time=.2)
        self.show(eq("0",left,-1.02,29,MUTED),eq("t",right,-1.02,33,GOLD),
                  text("첫 도착 시각 s는 달라진다",4.53,.92,25,GREEN),
                  text("두 번째 도착 시각은 t로 고정",4.53,.11,25,GOLD),
                  integral("p₂(t) = ∫<sub>0</sub><sup>t</sup> e<sup>−s</sup>e<sup>−(t−s)</sup> ds = te<sup>−t</sup>",
                           0,-1.97,43))
        self.to(105)


class Shot06(GammaChapterFour):
    shot=5

    def s06(self):
        for k,y in enumerate((1.75,.68,-.39,-1.46),1):
            self.show(text(f"{k}번째 손님",-5.82,y,25),
                      timeline(y,(.17,.36,.55,.78)[:k],start=-4.3,end=.5,active=k-1),
                      eq(("e⁻ᵗ","te⁻ᵗ","t²e⁻ᵗ / 2!","t³e⁻ᵗ / 3!")[k-1],4.06,y,43,PALETTE[k-1]),
                      run_time=.5)
        self.to(113)
        self.clear_body()
        self.show(integral(f"Γ(n) = {POSITIVE} t<sup>n−1</sup>e<sup>−t</sup> dt",y=1.07,size=65),
                  integral("p<sub>n</sub>(t) = t<sup>n−1</sup>e<sup>−t</sup> / (n−1)!",y=-.75,size=65,color=BLUE))
        self.to(119)


class Shot07(GammaChapterFour):
    shot=6

    def s07(self):
        axes=time_axes(maximum=14,top=1.5)
        graph=plot(axes,lambda t:kernel(t,1),0,14,GREEN)
        area=shade(axes,graph,0,14)
        value=eq("1",4.24,-.24,56,GOLD)
        form=eq("e⁻ᵗ",4.24,1.03,49,GREEN)
        self.show(axes,axis_labels(axes,range(0,15,2),(.5,1,1.5)),area,graph,form,value)
        for alpha in (2,3,4):
            next_graph=plot(axes,lambda t:kernel(t,alpha),0,14,GREEN)
            self.play(Transform(graph,next_graph),Transform(area,shade(axes,next_graph,0,14)),
                      Transform(value,eq(str(math.factorial(alpha-1)),4.24,-.24,56,GOLD)),
                      Transform(form,eq(POWERS[alpha-1]+"e⁻ᵗ",4.24,1.03,49,GREEN)),
                      run_time=.7)
        self.show(text("전체 넓이",4.24,.41,25,MUTED))
        self.to(124)
        normal=plot(axes,lambda t:density(t,4),0,14,BLUE)
        self.play(Transform(graph,normal),Transform(area,shade(axes,normal,0,14,BLUE)),
                  Transform(form,eq("t³e⁻ᵗ / 6",4.24,1.03,49,BLUE)),
                  Transform(value,eq("1",4.24,-.24,56,BLUE)),run_time=1.3)
        self.to(131)
        self.show(eq("Γ(4) = 6",4.24,-1.37,47,GOLD))
        self.to(134)
        self.play(Indicate(value,color=GOLD),run_time=.6)
        self.to(136)
        self.clear_body()
        self.show(integral("p<sub>n</sub>(t) = t<sup>n−1</sup>e<sup>−t</sup> / Γ(n)",y=1.29,size=66,color=BLUE),
                  integral(f"{POSITIVE} p<sub>n</sub>(t) dt = Γ(n) / Γ(n) = 1",y=-.42,size=62),
                  eq("t ≥ 0",y=-1.56,size=34,color=MUTED))
        self.to(144)
        self.show(text("감마분포 · 발생률 1",y=-2.18,size=28,color=GOLD))
        self.to(147)


class Shot08(GammaChapterFour):
    shot=7

    def s08(self):
        self.show(integral("p(t; α) = t<sup>α−1</sup>e<sup>−t</sup> / Γ(α)",y=.74,size=70,color=PURPLE),
                  eq("α > 0   ·   t > 0",y=-.62,size=44,color=MUTED))
        self.to(151)
        self.clear_body()
        axes=time_axes(maximum=14)
        shape=ValueTracker(1)
        curve=always_redraw(lambda:plot(axes,lambda t:density(t,shape.get_value()),0,14,PURPLE))
        fill=always_redraw(lambda:shade(axes,curve,0,14,PURPLE))
        alpha=decimal(shape,lambda k:k,5.04,1.51,2,PURPLE)
        exponent=decimal(shape,lambda k:k-1,5.04,.53,2,BLUE)
        constant=decimal(shape,math.gamma,5.04,-.44,4,GOLD)
        context=VGroup(*(plot(axes,lambda t:density(t,k),0,14,MUTED).set_stroke(opacity=.29)
                         for k in (1,2,3,4)))
        self.add(axes,axis_labels(axes,range(0,15,2),(.25,.5,.75,1)),context,fill,curve,alpha,exponent,
                 constant,eq("α =",3.58,1.51,42,PURPLE),eq("α − 1 =",3.44,.53,37,BLUE),
                 eq("Γ(α) =",3.44,-.44,37,GOLD),text("전체 넓이  1",4.26,-1.49,28,GREEN))
        self.play(shape.animate.set_value(2.5),run_time=5,rate_func=linear)
        self.to(157)
        self.play(shape.animate.set_value(3.8),run_time=3.4,rate_func=linear)
        for mob in (curve,fill,alpha,exponent,constant):
            mob.clear_updaters()
        self.to(161)
        self.show(text("정수 사이의 형태도 표현",4.27,-2.11,23,PURPLE))
        self.to(168)
        self.clear_body()
        left=time_axes(-4.0,.41,5.6,2.82,12,1.35)
        right=time_axes(4.0,.41,5.6,2.82,12,1.35)
        raw=plot(left,lambda t:kernel(t,3.5),0,12,GREEN)
        scaled=plot(right,lambda t:density(t,3.5),0,12,BLUE)
        self.show(left,right,axis_labels(left,(0,4,8,12),(.5,1)),
                  axis_labels(right,(0,4,8,12),(.5,1)),
                  raw,scaled,shade(left,raw,0,12),shade(right,scaled,0,12,BLUE),
                  text("정규화 전",-4,2.25,26),text("정규화 후",4,2.25,26),
                  text("전체 넓이  3.323…",-4,-1.5,28,GOLD),text("전체 넓이  1",4,-1.5,28,BLUE),
                  eq("α = 3.5",y=-2.13,size=33,color=PURPLE))
        self.to(176)


class Shot09(GammaChapterFour):
    shot=8

    def s09(self):
        for support,x,color,title in ((False,-4.02,GOLD,"사건의 발생 횟수"),
                                      (True,4.02,PURPLE,"분포의 형태 매개변수")):
            line=Line([x-2.7,.18,0],[x+2.7,.18,0],color=color if support else MUTED)
            self.show(line,text(title,x,1.32,30,color))
            for i in range(4):
                p=x+(i-1.5)*1.32
                self.show(Dot([p,.18,0],color=MUTED if support else color),
                          eq(str(i+1),p,-.32,29,MUTED),run_time=.2)
        self.to(181)
        self.show(Dot([4.02,.18,0],radius=.12,color=PURPLE),eq("2.5",4.02,.73,42,PURPLE),
                  eq("α > 0",4.02,-1.35,43,PURPLE),eq("n = 1, 2, …",-4.02,-1.35,42,GOLD))
        self.to(186)


def small_curve(fn,low,high,x,y,width,height,color=GREEN):
    sample=np.linspace(low,high,101)
    top=max(fn(t) for t in sample)
    axes=axes_at(x,y,[low,high,(high-low)/2],[0,top*1.05,top],width,height)
    return VGroup(Line(axes.c2p(low,0),axes.c2p(high,0),color=MUTED,stroke_width=1.3),
                  plot(axes,fn,low,high,color))


class Shot10(GammaChapterFour):
    shot=9

    def s10(self):
        for x,title,shape in ((-4.65,"대기 시간",1.6),(0,"장비의 수명",3.3),(4.65,"양의 연속 데이터",2.15)):
            self.show(panel(x,.14,4.01,3.64),text(title,x,1.45,29),
                      small_curve(lambda t:density(t,shape),0,10,x,-.39,3.16,1.36))
        self.to(194)
        self.clear_body()
        self.show(Circle(radius=.77,color=GOLD).move_to([0,.14,0]),eq("Γ",0,.14,62,GOLD))
        items=((-4.4,1.16,"감마분포",lambda t:density(t,2.5),0,9),
               (4.4,1.16,"베타분포",lambda t:12*t*(1-t)**2,0,1),
               (-4.4,-1.14,"카이제곱분포",lambda t:density(t/2,2)/2,0,14),
               (4.4,-1.14,"스튜던트 t분포",lambda t: (2/(math.pi*math.sqrt(3)))*(1+t*t/3)**-2,-4,4))
        for x,y,title,fn,lo,hi in items:
            self.show(Line([.68 if x>0 else -.68,.14,0],[x/2,y,0],color=MUTED),
                      panel(x,y,4.34,1.8),text(title,x,y+.58,24),
                      small_curve(fn,lo,hi,x,y-.18,3.11,.77),run_time=.5)
        self.to(203)


def probability_transition():
    frame=VGroup()
    for x,title,color in ((-4.73,"정수의 곱셈",GOLD),(0,"연속적인 적분",GREEN),(4.73,"불확실성의 표현",BLUE)):
        frame.add(panel(x,.34,4.19,3.49),text(title,x,1.65,28,color))
    frame.add(eq("n!",-4.73,.47,79,GOLD),text("이산적인 계산",-4.73,-.89,24,MUTED),
              eq("Γ(x)",0,.92,49,GREEN),
              small_curve(lambda t:kernel(t,2.4),0,9,0,-.25,3.32,1.32),
              text("정규화 상수",0,-1.08,24,MUTED),
              Arrow([-2.6,.35,0],[-2.12,.35,0],buff=.04,color=MUTED),
              Arrow([2.12,.35,0],[2.6,.35,0],buff=.04,color=MUTED))
    axes=time_axes(4.73,.22,3.2,1.44,9,1.08)
    frame.add(Line(axes.c2p(0,0),axes.c2p(9,0),color=MUTED,stroke_width=1.3))
    for k,color in enumerate(PALETTE[:3],1):
        frame.add(plot(axes,lambda t:density(t,k),0,9,color))
    frame.add(text("확률과 통계",4.73,-1.08,24,MUTED),
              text("계산 규칙은 유지되고, 그 규칙이 쓰이는 곳은 넓어진다",y=-2.13,size=27))
    return frame


class Shot11(GammaChapterFour):
    shot=10

    def s11(self):
        left=axes_at(-4.04,.29,[0,4.1,1],[0,26,6],5.65,2.94)
        right=time_axes(4.04,.29,5.65,2.94,12)
        fact=plot(left,lambda x:math.gamma(x+1),0,4,GREEN)
        self.show(left,fact,*(Dot(left.c2p(n,math.factorial(n)),color=GOLD) for n in range(5)),
                  right,*(plot(right,lambda t:density(t,k),0,12,color) for k,color in enumerate(PALETTE,1)),
                  text("팩토리얼의 확장",-4.04,2.19,26),text("확률분포의 구성",4.04,2.19,26),
                  eq("Γ(x+1)",-4.04,-1.67,44,GREEN),eq("p(t; α)",4.04,-1.67,44,BLUE))
        self.to(209)
        self.show(Arrow([-.9,.32,0],[.9,.32,0],buff=.1,color=GOLD))
        self.show(text("전체 넓이를 계산하고 확률의 기준 1로 맞춘다",y=-2.16,size=27,color=GOLD))
        self.to(218)
        self.clear_body()
        self.show(probability_transition(),run_time=1)
        self.to(225)
