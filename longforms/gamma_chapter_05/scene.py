"""Final chapter of the Gamma function longform."""
import json
import math
import sys
from pathlib import Path

from manim import (
    Annulus, Arrow, Circle, DashedLine, Dot, FadeOut, Line,
    SurroundingRectangle, Transform, VGroup,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))

from longforms.gamma_chapter_01.scene import (
    BLUE, GOLD, GREEN, MUTED, PURPLE, RED, ChapterShot, eq, graph, panel, text,
)
from longforms.gamma_chapter_02.scene import axes_at, plot
from longforms.gamma_chapter_03.scene import POSITIVE, integral, wire_mesh
from longforms.gamma_chapter_04.scene import density, kernel, probability_transition, shade

DATA = json.loads((HERE/"timing.json").read_text(encoding="utf-8"))
RULE_COLORS = {"n ·":GOLD,"tⁿ⁻¹":BLUE,"tⁿ":BLUE,"e⁻ᵗ":RED}


def arrow(x1,y1,x2,y2,color=MUTED):
    return Arrow([x1,y1,0],[x2,y2,0],buff=.06,color=color,stroke_width=2.4)


def node(x,y,width,height,heading,color):
    return VGroup(panel(x,y,width,height).set_stroke(color=color,opacity=.67),
                  text(heading,x,y+height/2-.34,25,color))


def distribution_curves(x,y,width,height):
    axes=axes_at(x,y,[0,11,2],[0,1.09,.25],width,height)
    return VGroup(Line(axes.c2p(0,0),axes.c2p(11,0),color=MUTED,stroke_width=1.4),
                  *(plot(axes,lambda t:density(t,k),0,11,color)
                    for k,color in ((1,BLUE),(2,PURPLE),(3,GREEN),(4,GOLD))))


def ring_symbol(x,y,scale=1):
    return VGroup(*(Circle(radius=r*scale,color=PURPLE,stroke_opacity=.56,stroke_width=1.6)
                    .move_to([x,y,0]) for r in (.36,.58,.81)),
                  Annulus(inner_radius=.59*scale,outer_radius=.7*scale,stroke_width=0,
                          fill_color=GOLD,fill_opacity=.82).move_to([x,y,0]),
                  eq("π",x,y,39*scale,GOLD))


def structure_cards():
    positions=(-4.62,0,4.62)
    cards=VGroup()
    for x,title,sub,color in zip(positions,("구조의 발견","표현의 변화","새로운 가능성"),
                                ("유지할 관계","더 넓은 표현","발견되는 연결"),(GOLD,GREEN,PURPLE)):
        cards.add(VGroup(node(x,.23,4.04,3.52,title,color),text(sub,x,-1.01,26)))
    for x in (-5.54,-4.62,-3.7):
        cards[0].add(Dot([x,.20,0],radius=.18,color=GOLD))
    cards[0].insert(2,Line([-5.54,.20,0],[-3.7,.20,0],color=GOLD))
    axes=axes_at(0,.08,[0,8,2],[0,.6,.2],2.85,1)
    cards[1].add(plot(axes,lambda t:kernel(t,3),0,8,GREEN),
                 eq("Γ",0,.68,49,GREEN))
    center=[4.62,.29,0]
    for angle in range(0,360,60):
        rad=math.radians(angle)
        target=[center[0]+.68*math.cos(rad),center[1]+.68*math.sin(rad),0]
        cards[2].add(Line(center,target,color=PURPLE),Dot(target,radius=.083,color=PURPLE))
    cards[2].add(Dot(center,radius=.19,color=PURPLE))
    return cards


class GammaChapterFive(ChapterShot):
    data=DATA

    def setup(self):
        super().setup()
        self.header[0].become(text("GAMMA FUNCTION  /  CHAPTER 05",-5.2,3.83,18,MUTED))


class Shot01(GammaChapterFive):
    shot=0

    def s01(self):
        previous=probability_transition()
        self.add(previous)
        self.wait(.4)
        self.play(*(m.animate.set_opacity(.13) for i,m in enumerate(previous) if i not in (0,1,6,7)),
                  run_time=.7)
        self.play(FadeOut(previous),run_time=.4)
        axes,frame,points=graph()
        q=axes.c2p(2.5,0)
        self.show(frame,points,
                  DashedLine(q,axes.c2p(2.5,16),color=PURPLE),
                  eq("?",q[0],.82,52,PURPLE),
                  eq("2.5",q[0],-1.995,24,PURPLE),
                  text("정수가 아닌 팩토리얼도\n정의할 수 있을까?",5.44,.67,28,PURPLE,width=4.2))
        self.to(5)


class Shot02(GammaChapterFive):
    shot=1

    def s02(self):
        for n,x in enumerate((-5.56,-2.78,0,2.78,5.56)):
            self.show(panel(x,.52,1.89,1.35),eq(str(math.factorial(n)),x,.52,52),
                      eq(f"{n}!",x,-.52,28,MUTED),run_time=.2)
        for n,x in enumerate((-4.17,-1.39,1.39,4.17),1):
            self.show(arrow(x-.41,.52,x+.41,.52,GOLD),eq(f"×{n}",x,1.34,31,GOLD),run_time=8/30)
        rule=eq("n! = n · (n−1)!",y=-1.7,size=54,color=GOLD)
        self.show(rule,SurroundingRectangle(rule,buff=.17,color=GOLD,stroke_width=1.2))
        self.to(11)


class Shot03(GammaChapterFive):
    shot=2

    def s03(self):
        self.show(text("팩토리얼의 재귀 관계",-3.8,2.13,26,MUTED),
                  text("거듭제곱의 미분",3.8,2.13,26,MUTED),
                  eq("n! = n · (n−1)!",-3.8,1.33,54,colors=RULE_COLORS),
                  eq("d/dt  tⁿ = n · tⁿ⁻¹",3.8,1.33,51,colors=RULE_COLORS),
                  Line([-6.5,.62,0],[6.5,.62,0],color=MUTED,stroke_opacity=.38))
        self.to(13)
        self.show(eq("tⁿ × e⁻ᵗ", -3.36,-.19,51,colors=RULE_COLORS),
                  arrow(-1.72,-.19,.4,-.19),
                  integral(f"{POSITIVE} t<sup>n</sup>e<sup>−t</sup> dt",3,-.19,49))
        gamma=integral(f"Γ(x) = {POSITIVE} t<sup>x−1</sup>e<sup>−t</sup> dt    (x &gt; 0)",
                       y=-1.72,size=49)
        self.show(gamma,SurroundingRectangle(gamma,buff=.15,color=GREEN,stroke_width=1.2))
        self.to(18)


class Shot04(GammaChapterFive):
    shot=3

    def s04(self):
        axes=axes_at(3.89,.43,[0,14,4],[0,5.2,2],5.31,2.53)
        curve=plot(axes,lambda t:kernel(t,5),0,14,GREEN)
        self.show(text("이산적인 곱셈",-3.83,2.16,28,GOLD),
                  eq("4! = 24",-3.83,1.04,67,GOLD),
                  eq("1 × 2 × 3 × 4",-3.83,-.12,45))
        self.show(text("연속적인 적분",3.89,2.16,28,GREEN),
                  arrow(-1,.44,1,.44),axes,shade(axes,curve,0,14),curve,
                  eq("t⁴e⁻ᵗ",5.18,1.27,38,GREEN))
        self.show(integral(f"4! = {POSITIVE} t<sup>4</sup>e<sup>−t</sup> dt = 24",
                           y=-1.79,size=56,color=GOLD))
        self.to(24)


class Shot05(GammaChapterFive):
    shot=4

    def s05(self):
        center=VGroup(node(0,.26,4.25,3.57,"연속적인 적분",GREEN),
                      eq("Γ(x)",0,.54,80,GREEN),
                      integral(f"{POSITIVE} t<sup>x−1</sup>e<sup>−t</sup> dt",0,-.69,41))
        self.show(center)
        self.to(26)
        for x,caption,color in ((-4.94,"새로운 관계",PURPLE),(4.94,"새로운 활용",BLUE)):
            side=1 if x>0 else -1
            self.show(node(x,.26,3.6,2.26,caption,color),
                      eq("?",x,.03,57,color),arrow(side*2.14,.26,side*3.12,.26))
        self.to(29)


class Shot06(GammaChapterFive):
    shot=5

    def s06(self):
        self.show(node(-3.59,.23,6.59,4.73,"기하학적 연결",PURPLE),
                  wire_mesh(-4.37,.14,.59,1.05),ring_symbol(-2.32,.53,.84),
                  eq("Γ(½) = √π",-3.59,-1.39,47,PURPLE))
        self.to(34)
        self.show(node(3.59,.23,6.59,4.73,"확률분포의 구성",BLUE),
                  integral("t<sup>α−1</sup>e<sup>−t</sup>    →    t<sup>α−1</sup>e<sup>−t</sup> / Γ(α)",
                           3.59,1.30,35,BLUE),
                  distribution_curves(3.59,.02,4.86,1.64))
        self.show(text("정규화한 밀도의 전체 넓이",3.32,-1.39,24),eq("= 1",6.02,-1.39,36,GOLD))
        self.to(40)


class Shot07(GammaChapterFive):
    shot=6

    def s07(self):
        self.show(node(-5.04,.3,3.75,3.56,"기존의 구조",GOLD),
                  eq("n!",-5.04,.58,67,GOLD),eq("n! = n(n−1)!",-5.04,-.56,35,GOLD))
        self.show(arrow(-3.15,.3,-2.14,.3),
                  node(-.05,.3,4.09,3.56,"새로운 표현",GREEN),
                  eq("Γ(x)",-.05,.62,68,GREEN),eq("Γ(x+1) = x Γ(x)",-.05,-.56,36,GREEN))
        self.to(43)
        self.show(Line([2,.3,0],[2.57,.3,0],color=MUTED),
                  Line([2.57,-.88,0],[2.57,1.37,0],color=MUTED),
                  arrow(2.57,1.37,3.11,1.37),arrow(2.57,-.88,3.11,-.88),
                  node(5.06,1.37,3.9,1.76,"공간의 대칭성",PURPLE),
                  eq("Γ(½) = √π",5.06,1.08,36,PURPLE),
                  node(5.06,-.88,3.9,1.76,"확률분포의 정규화",BLUE),
                  integral(f"{POSITIVE} p(t) dt = 1",5.06,-1.17,36,BLUE))
        self.to(48)


class Shot08(GammaChapterFive):
    shot=7

    def s08(self):
        starts=VGroup(eq("n! = n(n−1)!",-4.62,.35,46,GOLD),
                      integral(f"Γ(x) = {POSITIVE} t<sup>x−1</sup>e<sup>−t</sup> dt",0,.35,41),
                      eq("√π    ·    p(t; α)",4.62,.35,45,PURPLE))
        self.show(starts)
        self.to(51)
        cards=structure_cards()
        self.play(*(Transform(starts[i],cards[i]) for i in range(3)),run_time=1.1)
        self.show(arrow(-2.53,.30,-2.08,.30),arrow(2.08,.30,2.53,.30))
        self.to(57)


class Shot09(GammaChapterFive):
    shot=8

    def s09(self):
        cards=structure_cards()
        arrows=VGroup(arrow(-2.53,.30,-2.08,.30),arrow(2.08,.30,2.53,.30))
        self.add(cards,arrows)
        self.play(cards.animate.arrange(buff=.2).scale(.39).move_to([0,.56,0]),
                  FadeOut(arrows),run_time=1.2)
        self.play(FadeOut(cards),run_time=.4)
        self.to(59)
        self.show(eq("Γ(x)",y=1.18,size=117,color=GREEN),
                  eq("Γ(x+1) = x Γ(x)",y=.05,size=41,color=MUTED),
                  Line([-3.34,-.45,0],[3.34,-.45,0],color=MUTED,stroke_opacity=.5))
        self.to(61)
        axes=axes_at(-5.01,.85,[0,4.3,1],[0,27,9],3.2,1.97)
        dots=VGroup(*(Dot(axes.c2p(n,math.factorial(n)),radius=.063,color=GOLD) for n in range(5)))
        rings=ring_symbol(5.37,1.17,1.1)
        family=distribution_curves(5.28,-1.44,3.15,1.22)
        for support in (axes,dots,rings,family):
            support.set_opacity(.12)
        for curve in (*family[1:], *rings[:3]):
            curve.set_fill(opacity=0)
        self.show(axes,dots,rings,family)
        self.to(63)
        self.show(text("구조는 유지하고, 표현의 가능성은 확장한다.",y=-1.42,size=36,width=9.9))
        self.to(65)
