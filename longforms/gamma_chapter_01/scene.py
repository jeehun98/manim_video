"""Seven independently rendered shots for Gamma chapter one."""
import itertools
import json
import math
import sys
from pathlib import Path

from manim import (
    Arrow, Axes, Circle, Create, DashedLine, Dot, FadeOut, Indicate, LaggedStart,
    Line, RoundedRectangle, Scene, Square, Transform, Triangle, ValueTracker,
    VGroup, always_redraw, config, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from episodes.gamma01_factorial_extension.scene import (
    BLUE, GOLD, GREEN, INK, MUTED, PURPLE, RED, formula as math_text, shared,
)
from longforms.qcs01_speed.direction import QCSScene, label

DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))


def text(value, x=0, y=0, size=30, color=INK, width=14):
    return label(value, x, y / shared.L.y(1), size, color, width)


def eq(value, x=0, y=0, size=54, color=INK, colors=None):
    return math_text(value, y=y, x=x, size=size, color=color, colors=colors)


def panel(x, y, width, height):
    return RoundedRectangle(width=width, height=height, corner_radius=.15,
                            stroke_color="#3A4960", stroke_width=1.5,
                            fill_color="#151E2E", fill_opacity=1).move_to([x, y, 0])


def shapes(indices, x, y, size=.47, gap=.72):
    result = VGroup()
    for k, index in enumerate(indices):
        shape = (Circle(), Square(), Triangle())[index]
        shape.scale_to_fit_height(size).set_stroke(width=0).set_fill((GOLD, BLUE, PURPLE)[index], 1)
        shape.move_to([x + (k-(len(indices)-1)/2)*gap, y, 0])
        result.add(shape)
    return result


def graph():
    axes = Axes(x_range=[0, 4.3, 1], y_range=[0, 28, 5], x_length=8.7, y_length=3.7,
                tips=False, axis_config={"color": MUTED, "stroke_width": 1.6})
    axes.move_to([-.75, .13, 0])
    grid = VGroup(*(Line(axes.c2p(0,y), axes.c2p(4.3,y), color=MUTED,
                         stroke_width=1, stroke_opacity=.22) for y in range(5, 26, 5)),
                  *(Line(axes.c2p(x,0), axes.c2p(x,28), color=MUTED,
                         stroke_width=1, stroke_opacity=.22) for x in range(1, 5)))
    labels = VGroup(*(eq(str(x), *[axes.c2p(x,0)[0], axes.c2p(x,0)[1]-.26], size=23)
                      for x in range(5)),
                    *(eq(str(y), *[axes.c2p(0,y)[0]-.35, axes.c2p(0,y)[1]], size=21, color=MUTED)
                      for y in range(5, 26, 5)),
                    text("입력 x", 3.1, -2.35, 21, MUTED))
    dots = VGroup(*(Dot(axes.c2p(x, math.factorial(x)), radius=.073, color=GOLD)
                    .set_z_index(4) for x in range(5)))
    return axes, VGroup(grid, axes, labels), dots


def interpolated(x, a, frequency):
    return math.gamma(x+1)*(1+a*math.sin(frequency*math.pi*x))


def plot(axes, a, color, frequency=1):
    return axes.plot(lambda x: interpolated(x,a,frequency), x_range=[0, 4, .025],
                     color=color, stroke_width=3)


def transition_rules():
    """Comparison objects for a subsequent chapter to place at identical coordinates."""
    return (
        VGroup(text("팩토리얼의 재귀 관계", y=1.81, size=25, color=MUTED),
               eq("n! = n · (n−1)!", y=1.12, size=65, colors={"n ·": GOLD})),
        Line([-5.5,.34,0],[5.5,.34,0], color=MUTED, stroke_opacity=.4, stroke_width=1.4),
        VGroup(text("거듭제곱의 미분", y=-.13, size=25, color=MUTED),
               eq("d/dt  tⁿ = n · tⁿ⁻¹", y=-.85, size=63,
                  colors={"tⁿ⁻¹": BLUE, "tⁿ": BLUE, "n ·": GOLD})),
        VGroup(panel(0,-2.05,7.5,.57),
               text("이 두 규칙을 연결할 수 있을까?", y=-2.05, size=25)),
    )


class ChapterShot(QCSScene):
    data = DATA
    replace = Scene.replace

    def setup(self):
        super().setup()
        self.remove(*[m for m in self.mobjects if m not in (self.title, self.caption, self.caption_panel)])
        self.title.move_to([-4.8, 3.2, 0], aligned_edge=[-1, 0, 0]).shift([-2.15,0,0])
        self.header = VGroup(text("GAMMA FUNCTION  /  CHAPTER 01", -5.2, 3.83, 18, MUTED),
                             Line([-7,2.8,0],[7,2.8,0], color=MUTED, stroke_opacity=.33, stroke_width=1.4))
        self.add(self.header)

    def clear_body(self):
        keep = (self.title, self.header, self.caption_panel, self.caption)
        self.play(*(FadeOut(m) for m in self.mobjects if m not in keep), run_time=.4)


class Shot01(ChapterShot):
    shot = 0

    def s01(self):
        self.show(shapes((0,1,2),0,.64,1.0,1.65),text("서로 다른 물체를 어떻게 배열할까?",y=-.93))
        self.to(4)
        self.clear_body()
        slots = VGroup(*(panel(x,-.13,2,.9) for x in (-2.5,0,2.5)))
        self.show(slots,shapes((0,1,2),0,1.38,.66,1),
                  text("세 물체를 일렬로 배열",y=-1.43,color=MUTED))
        self.to(8)
        self.clear_body()
        for place, x in enumerate((-4.4,0,4.4)):
            remaining=tuple(range(place,3))
            card=VGroup(panel(x,.14,3.7,4.15),
                        text(f"{place+1}번째 위치",x,1.8,29,MUTED),
                        shapes(remaining,x,.89,.53,.76),
                        shapes((place,),x,-.07,.83),
                        eq(str(len(remaining)),x,-1.04,57,GOLD),
                        text("가지 선택",x,-1.64,22,MUTED))
            self.show(card,run_time=.5)
            if place < 2:
                self.show(eq("×",x+2.2,-1.04,40),run_time=.3)
            self.to((10,12,15)[place])
        self.clear_body()
        for i, order in enumerate(itertools.permutations(range(3))):
            x,y=(-3.65,0,3.65)[i%3],(1.57,.32)[i//3]
            self.show(VGroup(panel(x,y,2.71,.95),shapes(order,x,y,.46,.67)),run_time=.2)
        self.show(eq("3 × 2 × 1 = 6",y=-1.53,size=66,color=GOLD))
        self.to(19)
        self.clear_body()
        self.show(eq("n! = n × (n−1) × ⋯ × 1",y=.6,size=66,colors={"n!":GOLD}),
                  text("자연수의 연속 곱",y=-.94,color=MUTED))
        self.to(23)


class Shot02(ChapterShot):
    shot = 1

    def s02(self):
        objects=shapes((0,1,2),0,.57,.82,1.16)
        count=eq("3! = 6",0,-.69,52,GOLD)
        self.show(objects,count)
        self.play(objects.animate.shift([-4.4,0,0]),count.animate.shift([-4.4,0,0]),run_time=.7)
        machine=VGroup(panel(3.68,.52,2.6,1.23),eq("F(n)",3.68,.52,57,GOLD))
        self.show(text("배열의 개수",-4.4,1.78,color=MUTED),
                  text("하나의 함수",3.68,1.78,color=MUTED),
                  Arrow([-1.9,.52,0],[-.65,.52,0],buff=0,color=MUTED),machine,
                  eq("n →",1.82,.52,43),eq("→ n!",5.67,.52,43),
                  eq("F(n) = n!",3.68,-.69,46))
        self.to(29)
        self.play(FadeOut(objects),FadeOut(count),run_time=.4)
        self.show(eq("F(3) = 6", -3.56,.54,49,GOLD),
                  eq("F(2.5) = ?", -3.56,-.65,49,PURPLE))
        self.to(32)


class Shot03(ChapterShot):
    shot = 2

    def s03(self):
        axes, frame, dots=graph()
        self.show(frame,text("F(n) = n!",5.4,1.42,30,GOLD))
        self.play(LaggedStart(*(Create(dot) for dot in dots),lag_ratio=.3),run_time=1.4)
        self.to(36)
        guide=DashedLine(axes.c2p(2.5,0),axes.c2p(2.5,12),color=PURPLE)
        self.show(guide,eq("2.5",axes.c2p(2.5,0)[0],-1.98,25,PURPLE),
                  eq("F(2.5) = ?",5.4,.22,39,PURPLE),
                  text("정수 사이의 값은 미정",5.38,-.94,25,MUTED))
        self.to(41)


class Shot04(ChapterShot):
    shot = 3

    def s04(self):
        axes, frame, dots=graph()
        self.add(frame,dots)
        baseline=plot(axes,0,BLUE)
        self.play(Create(baseline),run_time=1.55)
        self.to(44)
        tracker=ValueTracker(0)
        moving=always_redraw(lambda:plot(axes,tracker.get_value(),PURPLE))
        self.add(moving)
        self.play(tracker.animate.set_value(.45),run_time=1.5,rate_func=linear)
        moving.clear_updaters()
        alternate=plot(axes,-.38,RED)
        self.play(Create(alternate),run_time=1)
        guide=DashedLine(axes.c2p(2.5,0),axes.c2p(2.5,14),color=MUTED)
        matches=[Dot(axes.c2p(2.5,interpolated(2.5,a,1)),color=c,radius=.068).set_z_index(4)
                 for a,c in ((.45,PURPLE),(0,BLUE),(-.38,RED))]
        self.show(guide,*matches,eq("x = 2.5",5.35,.97,42,PURPLE),
                  text("곡선마다 다른 높이",5.35,.03,27))
        self.to(51)
        self.play(*(curve.animate.set_opacity(.38) for curve in (baseline,moving,alternate)),run_time=.6)
        self.show(text("같은 정수값",5.35,-.91,27,GOLD),
                  text("어떤 연결을 선택할까?",5.35,-1.61,27))
        self.to(56)


class Shot05(ChapterShot):
    shot = 4

    def s05(self):
        self.show(eq("3! = 6", -4.5,.62,58,GOLD),eq("4! = 24",0,.62,58,GOLD),
                  eq("5! = 120",4.5,.62,58,GOLD),
                  text("한 단계씩 어떻게 바뀔까?",y=-1.03))
        self.to(61)
        self.clear_body()
        first=eq("4! = 3! × 4",y=1.13,size=64,colors={"× 4":GOLD,"3!":PURPLE})
        second=eq("5! = 4! × 5",y=-.66,size=64,colors={"× 5":GOLD,"4!":PURPLE})
        self.show(first,second)
        self.play(Indicate(first,color=GOLD),Indicate(second,color=GOLD),run_time=.9)
        self.to(67)
        self.clear_body()
        self.show(eq("n! = n · (n−1)!",y=.75,size=72,colors={"n ·":GOLD,"(n−1)!":PURPLE}),
                  text("현재 숫자",-.36,-.34,26,GOLD),
                  text("이전 단계",2.1,-.34,26,PURPLE))
        self.to(72)
        self.show(text("재귀 관계",y=-1.54,size=41,color=BLUE))
        self.to(75)


class Shot06(ChapterShot):
    shot = 5

    def s06(self):
        self.show(eq("F(n) = n!",-3.62,1.15,58,GOLD),text("정수에서 기존 값 유지",-3.62,.17,29),
                  eq("F(x+1) = (x+1) F(x)",3.32,1.15,53,colors={"(x+1)":GOLD,"F(x)":PURPLE}),
                  text("연속인 F에 같은 재귀 적용",3.32,.17,29),
                  eq("x ≥ 0",3.32,-.55,32,MUTED),
                  eq("F(2.5) = 2.5 F(1.5)",3.32,-1.44,43,PURPLE))
        self.to(83)
        self.clear_body()
        axes,frame,dots=graph()
        self.show(frame,dots)
        self.play(*(Create(plot(axes,a,c,frequency=2)) for a,c in ((-.25,BLUE),(0,GREEN),(.25,PURPLE))),
                  run_time=.9)
        self.show(text("같은 재귀를 만족하는",5.32,.99,26),
                  text("서로 다른 연속함수",5.32,.36,27,PURPLE))
        self.to(86)
        self.show(eq("F(x+1) = (x+1) F(x)",5.22,-.65,34,GOLD),
                  text("함수를 구성하는 단서",5.32,-1.43,25,MUTED))
        self.to(91)


class Shot07(ChapterShot):
    shot = 6

    def s07(self):
        factorial, divider, derivative, question=transition_rules()
        self.show(factorial,divider)
        self.to(93)
        self.show(derivative,run_time=.7)
        self.to(95)
        self.show(question,run_time=.6)
        self.to(97)
