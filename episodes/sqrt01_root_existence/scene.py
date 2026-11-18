"""Manim short synchronized to the supplied sentence boundaries."""

import json
import os
from pathlib import Path
import sys

from manim import *

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from visual_library.manim.theme import FONT, INK, MUTED, configure_vertical

configure_vertical()
config.background_color = "#090E19"
config.progress_bar = "none"
config.disable_caching = True
DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
CYAN, VIOLET, GREEN, ORANGE, GOLD = "#56CEF7", "#B9A4FF", "#67E2BC", "#FF9975", "#FFD07A"
PANEL = "#152033"
POLY = r"x^2-2"
ROOTS = r"x=\pm\sqrt{2}"
ROOT = 2**0.5


def pos(x, y):
    return x * RIGHT + y * UP


def label(text, y=0, size=38, color=INK, x=0, width=7.8):
    obj = Text(text, font=FONT, font_size=size, color=color, line_spacing=0.9)
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj.move_to(pos(x, y))


def eq(tex, y=0, size=64, color=INK, x=0, width=7.8):
    obj = MathTex(tex, font_size=size, color=color)
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj.move_to(pos(x, y))


def panel(x, y, w, h, color=MUTED):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.22, stroke_width=1.4,
        stroke_color=color, fill_color=PANEL, fill_opacity=1,
    ).move_to(pos(x, y))


class RootExistence(Scene):
    def construct(self):
        self.offset = 0
        core_preview = os.getenv("SQRT01_CORE_PREVIEW") == "1"
        if core_preview:
            self.offset = DATA["scene_boundaries"][4]
        else:
            self.opening()
            self.expressions()
            self.assumption()
            self.domains()

        self.endpoints()
        self.crossing()
        if not core_preview:
            self.name_root()
            self.reasoning()
            self.close()

    def to(self, target):
        frame = round(self.time * 30)
        remaining = (target - self.offset) * 30 - frame
        if remaining < 0:
            raise ValueError(f"Missed {target}s by {-remaining} frames")
        if remaining:
            self.wait(remaining / 30)

    def show(self, *objects, seconds=0.6):
        self.play(*(FadeIn(obj, shift=UP * 0.12) for obj in objects), run_time=seconds)

    def clear(self, seconds=0.4):
        if self.mobjects:
            self.play(*(FadeOut(obj) for obj in self.mobjects), run_time=seconds)

    def heading(self, title, color=CYAN):
        return label(title, 5.25, 33, color)

    def comparison(self, y=1.4, height=2.8):
        w = 3.35
        x = 2.12
        left = VGroup(
            panel(-x, y, w, height, CYAN),
            eq(r"x^2=2", y+0.30, 55, CYAN, -x, 2.95),
            label("제곱하면 2가 된다", y-0.72, 25, INK, -x, 2.95),
        )
        right = VGroup(
            panel(x, y, w, height, VIOLET),
            eq(ROOTS, y+0.30, 55, VIOLET, x, 2.95),
            label("제곱근으로 나타낸다", y-0.72, 25, INK, x, 2.95),
        )
        arrow = eq(r"\Longleftrightarrow", y+0.3, 34, GREEN, width=0.76)
        return left, right, arrow

    def opening(self):
        initial = eq(POLY+r"=0", size=105)
        self.play(Write(initial), run_time=0.7)
        self.to(1)
        question = label("이 방정식의 해는?", -0.65, 48, CYAN)
        self.play(initial.animate.move_to(UP*2.7), FadeIn(question), run_time=0.65)
        self.to(4)
        middle = eq(r"x^2=2", 0.25, 80, CYAN)
        answer = eq(ROOTS, -2.05, 88, VIOLET)
        self.play(FadeOut(question), run_time=0.3)
        self.show(eq(r"\Downarrow", 1.48, 40, MUTED), middle)
        self.show(eq(r"\Downarrow", -0.93, 40, MUTED), answer)
        check = eq(r"\checkmark", -2.05, 42, GREEN, 2.8)
        box = SurroundingRectangle(answer, color=VIOLET, buff=0.31, corner_radius=0.15)
        self.show(box, check, seconds=0.45)
        self.play(FadeOut(check), run_time=0.35)
        self.to(8)

    def expressions(self):
        question = label("그런데, 루트 2는 무엇을 뜻할까?", -4.3, 35, GOLD)
        self.show(question)
        self.to(10)
        previous = list(self.mobjects)
        self.definition_root = eq(r"\sqrt{2}", 1.15, 125, VIOLET)
        self.play(*(FadeOut(obj) for obj in previous), FadeIn(self.definition_root), run_time=0.7)
        self.to(13)
        self.show(label("제곱하면 2가 되는 양수", -0.65, 47))
        self.to(16)
        self.clear()
        left, right, arrow = self.comparison()
        self.show(left, right)
        self.play(Indicate(left[1], color=CYAN), run_time=0.65)
        self.play(Indicate(right[1], color=VIOLET), run_time=0.65)
        statement = label("실수에서 같은 해집합", -3.25, 41, GREEN)
        self.show(arrow, statement)
        for x in (-2.12, 2.12):
            pair = VGroup(
                Dot(pos(x-0.57, -0.85), color=VIOLET),
                Dot(pos(x+0.57, -0.85), color=CYAN),
                eq("-", -1.35, 32, VIOLET, x-0.57),
                eq("+", -1.35, 32, CYAN, x+0.57),
            )
            self.show(pair, seconds=0.35)
        marker = Dot(radius=0.065, color=GREEN).move_to(pos(-0.32, 1.22))
        self.play(FadeIn(marker), run_time=0.23)
        self.play(marker.animate.shift(RIGHT * 0.64), run_time=0.43)
        self.play(marker.animate.shift(LEFT * 0.64), run_time=0.43)
        self.play(FadeOut(marker), run_time=0.23)
        self.to(22)

    def assumption(self):
        self.clear()
        self.show(eq(r"x^2=2", 3.65, 57, CYAN), eq(ROOTS, 1.15, 92, VIOLET))
        self.show(label("올바른 풀이", -0.75, 35, GREEN))
        self.to(25)
        self.show(label("그런 수가 정말 존재할까?", -2.25, 49, GOLD))
        self.to(28)
        self.clear()
        self.show(self.heading("존재성 · Existence", GOLD))
        self.show(eq(r"\exists x\in\mathbb{R}:\quad x^2=2\;?", 1.10, 66))
        self.to(32)
        self.show(label("왜 이 수가 당연히 있다고 생각할까?", -1.4, 39, MUTED))
        self.to(35)
        self.clear()
        self.show(self.heading("익숙한 두 연산"))
        self.show(eq(r"x\longmapsto x^2", 1.85, 72, CYAN),
                  eq(r"y\longmapsto\sqrt{y}", -0.4, 72, VIOLET),
                  label("음이 아닌 실수에서", -2.05, 33, MUTED))
        self.to(39)

    def domains(self):
        self.clear()
        formula = eq(r"x^2=2", 3.4, 92)
        self.show(formula, eq(r"\mathbb{Q}\qquad\mathbb{R}", 0.8, 75, CYAN))
        self.to(43)
        self.clear()
        line = NumberLine(x_range=[1,2,1], length=6.5, color=MUTED, include_numbers=True)
        line.move_to(UP * 0.1)
        samples = VGroup()
        for value, tex, y in ((4/3, r"\frac{4}{3}", -1.65), (3/2, r"\frac{3}{2}", 1.25), (7/5, r"\frac{7}{5}", 2.25)):
            p = line.n2p(value)
            samples.add(VGroup(
                DashedLine(p, pos(p[0], y*0.72), color=MUTED, stroke_width=2),
                Dot(p, color=CYAN),
                eq(tex, y, 42, CYAN, p[0]),
            ))
        self.show(self.heading("유리수"), line)
        self.to(46)
        self.show(eq(r"\frac{a}{b},\quad a,b\in\mathbb{Z},\quad b\ne0", 3.55, 54))
        self.play(LaggedStart(*(FadeIn(s) for s in samples), lag_ratio=0.35), run_time=1.3)
        self.show(label("수직선 위의 유리수 예시", -3.3, 34, MUTED))
        self.to(49)
        self.show(eq(r"\nexists x\in\mathbb{Q}:\quad x^2=2", -4.85, 55, ORANGE))
        self.to(53)
        self.clear()
        self.show(self.heading("같은 방정식, 다른 수의 범위"))
        cards = VGroup()
        for x, title, symbol, status, color in (
            (-2, "유리수", r"\mathbb{Q}", "해가 없음", ORANGE),
            (2, "실수", r"\mathbb{R}", "해가 존재함", GREEN),
        ):
            cards.add(VGroup(
                panel(x, 0.7, 3.65, 4.6, color),
                label(title, 2.15, 33, INK, x),
                eq(symbol, 1.12, 48, color, x),
                eq(r"x^2=2", 0.13, 51, INK, x),
                label(status, -0.95, 33, color, x),
            ))
        self.show(cards[0])
        self.show(cards[1])
        self.to(56)
        self.show(label("어느 집합에서 해를 찾는가?", -2.84, 40))
        self.to(61)
        self.play(Indicate(cards[1][0], color=GREEN, scale_factor=1.05), run_time=0.85)
        self.to(63)

    def endpoints(self):
        self.clear()
        self.proof_heading = self.heading("실수에서 해가 존재하는 이유")
        self.show(self.proof_heading)
        problem = eq(POLY+r"=0", 2.9, 78)
        self.show(problem)
        self.to(66)
        self.function = eq("f(x)="+POLY, 3.72, 70)
        self.play(TransformMatchingTex(problem, self.function), run_time=0.8)
        self.axes = Axes(
            x_range=[0.67, 2.29, 0.2], y_range=[-1.52, 2.6, 1],
            x_length=6.55, y_length=5.3, tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False},
        ).move_to(DOWN * 0.32)
        self.show(self.axes)
        x_axis = self.axes.c2p(2.22, 0)
        origin = self.axes.c2p(0.69, 0)
        self.show(eq("x", x_axis[1]-0.36, 32, MUTED, x_axis[0]),
                  eq("0", origin[1]+0.25, 32, MUTED, origin[0]-0.22))
        self.to(70)
        for x, y, color, text, dx, dy in (
            (1,-1,ORANGE,r"f(1)=-1",0.56,-0.54),
            (2,2,GREEN,r"f(2)=2",-0.42,0.49),
        ):
            p = self.axes.c2p(x,y)
            q = self.axes.c2p(x,0)
            guide = DashedLine(q, p, color=color, stroke_width=2)
            marker = Dot(p, radius=0.105, color=color)
            tick = eq(str(x), -3.44, 39, INK, q[0])
            name = eq(text, p[1]+dy, 42, color, p[0]+dx)
            self.show(guide, marker, tick, name)
            self.wait(0.8)
        self.to(75)
        signs = eq(r"f(1)<0<f(2)", -4.6, 59, GOLD)
        self.show(signs)
        self.to(78)
        self.continuity = label("다항함수  →  연속함수", -5.6, 35, CYAN)
        self.show(self.continuity)
        self.to(81)

    def crossing(self):
        ax = self.axes
        p = ax.c2p(ROOT, 0)
        for bottom, top, color in ((-1.23, 0, ORANGE), (0, 2.35, GREEN)):
            lo, hi = ax.c2p(0.75, bottom), ax.c2p(2.20, top)
            band = Rectangle(width=hi[0]-lo[0], height=hi[1]-lo[1],
                             stroke_width=0, fill_color=color, fill_opacity=0.055)
            self.add(band.move_to((lo+hi)/2).set_z_index(-1))
        curve = ax.plot(lambda x: x*x-2, x_range=[1,2,0.02], color=CYAN, stroke_width=5)
        self.play(Create(curve), run_time=1.05)
        x_value = ValueTracker(1)
        dot = Dot(radius=0.14)
        def follow(marker):
            x = x_value.get_value()
            y = x*x-2
            color = ORANGE if y < -1e-8 else GREEN if y > 1e-8 else INK
            marker.move_to(ax.c2p(x, y)).set_color(color)
        dot.add_updater(follow, call_updater=True)
        self.add(dot)
        negative = eq(r"f(x)<0", 0.2, 42, ORANGE, 2.6)
        zero = eq(r"f(x)=0", 0.2, 42, INK, 2.6)
        positive = eq(r"f(x)>0", 0.2, 42, GREEN, 2.6)
        self.add(negative)
        self.play(x_value.animate.set_value(ROOT), rate_func=linear, run_time=3.4)
        self.remove(negative)
        self.add(zero)
        self.wait(0.8)
        self.remove(zero)
        self.add(positive)
        self.play(x_value.animate.set_value(2), rate_func=linear, run_time=1.4)
        self.remove(dot, positive)
        self.to(88)
        guide = DashedLine(p, pos(p[0], -3.2), color=GOLD, stroke_width=2.7)
        self.show(guide, Dot(p, radius=0.14, color=GOLD),
                  eq("c", -3.44, 47, GOLD, p[0]),
                  eq(r"f(c)=0", p[1]+0.46, 47, GOLD, p[0]-0.80))
        self.to(92)
        theorem = self.heading("중간값 정리 · Intermediate Value Theorem", GOLD)
        ivt = eq(r"\exists c\in(1,2):\quad f(c)=0", -5.6, 55, GOLD)
        self.play(FadeOut(self.continuity), FadeOut(self.proof_heading), FadeIn(theorem), FadeIn(ivt), run_time=0.7)
        self.to(94)
        expanded = eq(r"\exists c\in(1,2):\quad c^2-2=0", -5.6, 55, GOLD)
        self.play(TransformMatchingTex(ivt, expanded), run_time=0.8)
        self.to(99)
        self.play(
            TransformMatchingTex(expanded, eq(r"1<c<2,\qquad c^2=2", -5.6, 62, GOLD)),
            run_time=0.8,
        )
        self.show(label("제곱해서 2가 되는 양의 실수가 존재한다", -6.7, 34, GREEN))
        self.to(105)

    def name_root(self):
        self.clear()
        self.show(self.heading("계산 없이 알아낸 것"))
        axis = NumberLine(x_range=[1,2,1], length=6, color=MUTED, include_numbers=True)
        point = axis.n2p(ROOT)
        self.show(axis, Dot(point, color=GOLD), eq("c", 0.62, 52, GOLD, point[0]))
        decimal = eq(r"c=1.\,???\ldots", -2.35, 64, MUTED)
        self.show(decimal)
        self.to(110)
        self.play(FadeOut(decimal), run_time=0.4)
        self.show(eq(r"1<c<2", -1.8, 62, CYAN), eq(r"c^2=2", -3.15, 62, GREEN))
        self.to(114)
        self.clear()
        self.show(eq(r"c^2=2,\qquad c>0", 3.4, 66, GOLD))
        name = eq(r"\sqrt{2}", 1.15, 125, VIOLET)
        identity = eq("c=", 1.15, 104, INK).next_to(name, LEFT, buff=0.22)
        self.show(identity, name)
        self.to(117)

    def reasoning(self):
        self.clear()
        left, right, arrow = self.comparison(2.8)
        self.show(left, right, arrow)
        ax = Axes(x_range=[0.85,2.18,1], y_range=[-1.25,2.4,1],
                  x_length=4.5, y_length=3, tips=False,
                  axis_config={"color": MUTED, "include_ticks": False})
        ax.move_to(DOWN*1.8)
        curve = ax.plot(lambda x:x*x-2, x_range=[1,2,0.03], color=CYAN)
        mini = VGroup(ax, curve, Dot(ax.c2p(ROOT,0), color=GOLD)).set_opacity(0.36)
        self.show(mini)
        self.play(mini.animate.set_opacity(1), run_time=1)
        self.to(124)
        self.clear()
        self.show(eq(r"\sqrt{2}", 3.65, 105, VIOLET))
        for y, title, color in (
            (1.52, "해의 존재", GREEN),
            (-0.40, "연속성 · 중간값 정리", CYAN),
            (-2.32, "실수의 완비성", GOLD),
        ):
            self.show(VGroup(panel(0,y,6.7,1.45,color), label(title,y,44,color)), seconds=0.65)
        self.to(131)
        self.clear()
        left, right, arrow = self.comparison(2.8)
        self.show(left, right, arrow)
        self.show(label("해집합을 표현한다", 0.42, 39, GREEN))
        self.play(Indicate(arrow, color=GREEN), run_time=0.75)
        self.show(eq(r"\exists c\in(1,2):\quad c^2=2", -2.38, 63, GOLD),
                  label("해의 존재를 보장한다", -3.62, 39, GOLD))
        self.to(139)

    def close(self):
        self.clear()
        opening = eq(POLY+r"=0", 4.36, 70)
        answer = eq(ROOTS, 2.12, 81, VIOLET)
        self.show(opening, eq(r"\Downarrow", 3.24, 35, MUTED), answer)
        for y, title, detail, color in (
            (0.14, "연속성", "다항함수는 연속이다", CYAN),
            (-1.69, "중간값 정리", "1과 2 사이에 양의 해가 있다", GREEN),
            (-3.52, "실수의 완비성", "중간값 정리를 뒷받침한다", GOLD),
        ):
            self.show(VGroup(panel(0,y,7.35,1.56,color),
                             label(title,y+0.31,37,color),
                             label(detail,y-0.35,30)), seconds=0.6)
        self.show(label("양수에서 증가 · 제곱의 대칭성으로 두 해", -5.35, 31, MUTED))
        self.to(149)
        self.play(*(FadeOut(m) for m in self.mobjects if m is not answer),
                  answer.animate.move_to(UP*1.05), run_time=1)
        self.show(label("이미 확립된 수학적 사실 위에서 쓰는 기호", -0.95, 35, MUTED))
        self.to(153)
        self.clear()
        final = eq(r"x^2=2\quad\Longleftrightarrow\quad "+ROOTS, 1.4, 74, width=7.65)
        self.show(final, label("기호 하나에도\n수학적 근거가 숨어 있다", -0.7, 51))
        self.to(158)
        root = eq(r"\pm\sqrt{2}", 0.9, 111, VIOLET)
        self.play(*(FadeOut(obj) for obj in self.mobjects), FadeIn(root), run_time=0.65)
        self.play(FadeOut(root), run_time=1.0)
        self.to(160)
