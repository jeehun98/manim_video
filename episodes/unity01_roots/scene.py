"""Exact-time portrait scenes for the roots of unity short."""
import json
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    Arc, Arrow, Circle, ComplexPlane, Create, DashedLine, DashedVMobject, Dot,
    FadeIn, FadeOut, Line, MathTex, Polygon, Rotate,
    TAU, Transform, ValueTracker, VGroup, VMobject, always_redraw, config, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene, label

shared.FPS = config.frame_rate = 15 if os.getenv("QCS_PREVIEW") == "1" else 60
config.background_color = "#0C1018"
DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
WHITE, MUTED, GRID = "#E5E7EB", "#A7B6CD", "#51637B"
BLUE, GOLD, VIOLET, GREEN, RED = "#60A5FA", "#FBBF24", "#A78BFA", "#34D399", "#F87171"
COLORS = (BLUE, GOLD, VIOLET, GREEN, RED)
RECTANGULAR = (r"1", r"\frac{-1+i\sqrt3}{2}", r"\frac{-1-i\sqrt3}{2}")


def pt(x, y):
    return np.array([x, y, 0.0])


def unit(theta):
    return pt(np.cos(theta), np.sin(theta))


def roots(n):
    return [unit(TAU * k / n) for k in range(n)]


def txt(s, y, size=30, color=WHITE, x=0, width=7.5):
    return label(s, x=x, y=y, size=size, color=color, width=width)


def eq(s, y, size=49, color=WHITE, x=0, width=7.5):
    m = MathTex(s, color=color, font_size=size)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to(pt(x, y))


def axis(y, radius, x=0, *, grid=True):
    extent = 2.5 * radius
    return ComplexPlane(x_range=[-1.25, 1.25, 0.25], y_range=[-1.25, 1.25, 0.25],
                        x_length=extent, y_length=extent,
                        axis_config={"stroke_color": MUTED, "stroke_width": 1.45},
                        background_line_style={"stroke_color": GRID, "stroke_width": 1,
                                               "stroke_opacity": 0.49 if grid else 0},
                        ).move_to(pt(x, y))


def ring(center, radius, color=GRID, dashed=True):
    circle = Circle(radius=radius, color=color, stroke_width=2).move_to(center)
    return DashedVMobject(circle, num_dashes=44, dashed_ratio=0.52) if dashed else circle


def outline(points, color=BLUE):
    return Polygon(*points, stroke_color=color, stroke_width=3.4,
                   fill_color=color, fill_opacity=0.09)


def diagram(n, y, radius, x=0, grid=True):
    center = pt(x, y)
    points = [center + radius * v for v in roots(n)]
    return VGroup(axis(y, radius, x, grid=grid), ring(center, radius),
                  outline(points), VGroup(*(Dot(p, radius=min(0.095, radius / 18),
                                               color=GOLD) for p in points)))


def pointer(start, end, color=BLUE):
    return Arrow(start, end, buff=0, color=color, stroke_width=3.5,
                 max_tip_length_to_length_ratio=0.20)


def angle_arc(center, radius, start, sweep, color=VIOLET):
    return Arc(radius=radius, start_angle=start, angle=sweep, arc_center=center,
               color=color, stroke_width=3.0)


class UnityScene(QCSScene):
    data = DATA

    def setup(self):
        super().setup()
        self.remove(self.mobjects[0])
        self.add(txt("ROOTS OF UNITY", 7.10, 19, MUTED))

    def clear(self, duration=0.45):
        fixed = (self.title, self.caption, self.caption_panel)
        body = [m for m in self.mobjects if m not in fixed and m.get_top()[1] < 6.55]
        if body:
            self.play(*(FadeOut(m) for m in body), run_time=duration)

    def s01(self):
        expression = eq(r"z^5=1", 3.88, 72)
        names = eq(r"z_0\quad z_1\quad z_2\quad z_3\quad z_4", 2.52, 35, GOLD)
        self.show(expression, names)
        self.to(5)
        chart = diagram(5, -0.18, 2.20)
        self.show(chart[0], chart[1])
        for dot in chart[3]:
            self.show(dot, run_time=.25)
        self.play(Create(chart[2]), run_time=1.0)
        self.show(txt("복소평면 위에 드러난 대칭", -3.65, 32, BLUE))
        self.to(13)

    def s02(self):
        base = eq(r"z^3=1", 3.9, 66)
        self.show(base)
        self.to(16)
        self.play(Transform(base, eq(r"z^3-1=0", 3.9, 60)), run_time=0.6)
        self.show(eq(r"(z-1)(z^2+z+1)=0", 2.55, 53))
        branch = VGroup(Line(pt(0, 1.9), pt(0, 1.45), color=GRID),
                        Line(pt(0, 1.45), pt(-2.24, 0.79), color=GRID),
                        Line(pt(0, 1.45), pt(2.24, 0.79), color=GRID))
        self.play(Create(branch), run_time=0.65)
        self.show(eq(r"z-1=0", 0.18, 36, BLUE, -2.28),
                  eq(r"z^2+z+1=0", 0.18, 36, GOLD, 2.28))
        self.to(22)
        self.show(eq(r"z=1", -1.04, 40, BLUE, -2.28),
                  eq(r"\Delta=1-4=-3", -1.04, 36, RED, 2.28))
        self.to(25)
        self.clear()
        self.show(eq(r"y=x^2+x+1", 3.93, 47, BLUE))
        # Use equal axis units and center the graph on its useful real range.
        scale = 1.22
        origin = pt(0.56, -1.55)
        frame = VGroup(*(Line(pt(-3.15, y), pt(3.15, y), color=GRID, stroke_width=1)
                         for y in (-0.64, 0.28, 1.19, 2.11)),
                       Line(pt(-3.15, origin[1]), pt(3.15, origin[1]), color=MUTED),
                       Line(pt(origin[0], -1.95), pt(origin[0], 2.61), color=MUTED))
        curve = VMobject(color=BLUE, stroke_width=4)
        curve.set_points_smoothly([origin + scale * pt(x, x*x+x+1)
                                   for x in np.linspace(-2.04, 1.04, 95)])
        vertex = origin + scale * pt(-0.5, 0.75)
        self.play(FadeIn(frame), Create(curve), run_time=0.75)
        self.show(Dot(vertex, color=GOLD),
                  DashedLine(vertex, pt(vertex[0], origin[1]), color=GOLD),
                  eq(r"\frac34", vertex[1]+0.36, 30, GOLD, vertex[0]+0.38),
                  txt("실수축과 만나지 않는다", -3.1, 30, RED))
        self.to(31)
        self.clear()
        self.show(eq(r"z=\frac{-1\pm\sqrt{-3}}2=\frac{-1\pm i\sqrt3}2", 3.4, 46))
        for y, k, form in zip((1.25, -0.56, -2.39), range(3), RECTANGULAR):
            self.show(eq(fr"z_{k}={form}", y, 51, GOLD), run_time=0.42)
        self.to(36)

    def s03(self):
        center, radius = pt(0, 0.26), 2.37
        points = [center + radius * v for v in roots(3)]
        self.show(eq(r"z^3=1", 4.0, 55), axis(0.26, radius),
                  txt("Im", 3.37, 22, MUTED, .26), txt("Re", .57, 22, MUTED, 3.34))
        for k, (p, formula) in enumerate(zip(points, RECTANGULAR)):
            pos = (2.70, 0.65) if k == 0 else (-2.39, p[1] + (0.34 if k == 1 else -0.41))
            self.show(Dot(p, radius=.105, color=GOLD), eq(formula, pos[1], 33, GOLD, pos[0]),
                      run_time=.53)
        self.to(40)
        self.play(*(Create(Line(center, p, color=BLUE, stroke_width=3)) for p in points),
                  Create(ring(center, radius)), run_time=1)
        self.show(eq(r"|z_0|=|z_1|=|z_2|=1", -3.46, 42, GREEN))
        self.to(43)
        for k in range(3):
            start = TAU * k / 3
            pos = center + 1.27 * unit(start + TAU / 6)
            self.play(Create(angle_arc(center, .82, start, TAU / 3)),
                      FadeIn(eq(r"120^\circ", pos[1], 27, VIOLET, pos[0])), run_time=.55)
        self.to(47)
        self.play(Create(outline(points)), run_time=.75)
        self.show(txt("정삼각형", -4.19, 29, BLUE))
        self.to(50)

    def s04(self):
        self.show(eq(r"z^3-1=(z-1)(z^2+z+1)", 2.93, 47),
                  eq(r"z^4=1\qquad z^5=1\qquad z^{10}=1", .88, 41, BLUE),
                  txt("해의 위치를 바로 구할 수 있을까?", -1.65, 33, GOLD))
        self.to(56)
        self.clear()
        center, radius, theta = pt(0, .62), 2.34, TAU/9
        endpoint = center + radius * unit(theta)
        foot = pt(endpoint[0], center[1])
        self.show(axis(.62, radius), ring(center, radius), Dot(endpoint, color=GOLD),
                  eq("z", endpoint[1]+.34, 36, GOLD, endpoint[0]+.12))
        self.play(Create(Line(center, foot, color=BLUE, stroke_width=4)),
                  Create(Line(foot, endpoint, color=GOLD, stroke_width=4)), run_time=.7)
        self.show(eq("x", .25, 31, BLUE, .85), eq("y", 1.45, 32, GOLD, 2.1),
                  eq("z=x+iy", -3.09, 48))
        self.play(Create(Line(center, endpoint, color=WHITE, stroke_width=3.7)),
                  Create(angle_arc(center, .62, 0, theta)), run_time=.7)
        self.show(eq("r", 1.80, 34, WHITE, .68), eq(r"\theta", .93, 29, VIOLET, .92))
        self.to(63)
        self.show(eq(r"x=r\cos\theta,\qquad y=r\sin\theta", 4.12, 39, BLUE))
        self.show(eq(r"z=r(\cos\theta+i\sin\theta)", -4.13, 38, GREEN))
        self.to(66)
        self.clear()
        trig = eq(r"e^{i\theta}=\cos\theta+i\sin\theta", 3.15, 49)
        self.show(trig)
        self.show(eq(r"z=r e^{i\theta}", .88, 77, GREEN))
        self.show(txt("크기", -0.55, 30, BLUE, -1.09),
                  txt("각도", -0.55, 30, VIOLET, .82))
        self.to(71)

    def s05(self):
        center, scale = pt(0, .30), 1.55
        self.show(axis(.30, 2.37, grid=False),
                  eq(r"z_1z_2=r_1r_2e^{i(\theta_1+\theta_2)}", 4.0, 47))
        for r, theta, color, s in ((1.2, TAU/12, BLUE, "z_1"), (1.5, TAU/6, VIOLET, "z_2"),
                                   (1.8, TAU/4, GREEN, "z_1z_2")):
            p = center + scale * r * unit(theta)
            self.play(Create(pointer(center, p, color)),
                      Create(angle_arc(center, .45+.38*(r-1.2)/.6, 0, theta, color)),
                      FadeIn(eq(s, p[1]+.24, 29, color, p[0]+.32)), run_time=.67)
        self.show(txt("크기는 곱하고 각도는 더한다", -3.0, 30),
                  eq(r"(1.2e^{i\pi/6})(1.5e^{i\pi/3})=1.8e^{i\pi/2}", -4.11, 36, GREEN))
        self.to(76)
        self.clear()
        self.show(axis(.30, 2.37, grid=False), eq(r"z=1.2e^{i(40^\circ)}", 4.08, 49))
        for power, s in enumerate(("1", "z", "z^2", "z^3")):
            p = center + scale * 1.2**power * unit(power*TAU/9)
            color = GREEN if power == 3 else BLUE
            self.play(Create(pointer(center, p, color)),
                      FadeIn(eq(s, p[1]+.30, 30, color, p[0]+.25)), run_time=.42)
        self.show(eq(r"z^3=r^3e^{3i\theta}", -3.63, 52, GREEN))
        self.to(81)

    def s06(self):
        self.show(eq(r"z^3=r^3e^{3i\theta}=1", 3.89, 54))
        self.show(txt("크기 조건", 1.98, 27, BLUE, -2.12),
                  txt("각도 조건", 1.98, 27, VIOLET, 2.12),
                  eq(r"r^3=1", .79, 48, BLUE, -2.12),
                  eq(r"3\theta=2\pi k", .79, 44, VIOLET, 2.12))
        self.to(85)
        self.clear()
        center = pt(0, .06)
        self.show(axis(.06, 2.23), eq(r"r^3=1\Longrightarrow r=1", 4.06, 50, BLUE))
        self.play(Create(ring(center, 2.23, GREEN, dashed=False)), run_time=.9)
        self.show(Line(center, center + pt(2.23, 0), color=GREEN, stroke_width=3),
                  eq("1", .39, 34, GREEN, 1.28), txt("가능한 위치는 단위원 위", -3.44, 30, GREEN))
        self.to(90)
        self.clear()
        formula = eq(r"1=e^{0i}=e^{2\pi i}=e^{4\pi i}=\cdots", 4.0, 42)
        center = pt(0, -.05)
        t = ValueTracker(0)
        ray = always_redraw(lambda: pointer(center, center + 2.05*unit(t.get_value()), VIOLET))
        self.show(formula, axis(-.05, 2.05), ring(center, 2.05),
                  Dot(center+pt(2.05, 0), color=GREEN))
        self.add(ray)
        self.play(t.animate.set_value(2*TAU), run_time=2.45, rate_func=linear)
        self.show(eq(r"3\theta=2\pi k,\qquad k\in\mathbb Z", -3.47, 43, VIOLET))
        self.to(95)
        self.remove(ray)
        self.clear(.25)
        t.set_value(0)
        r = 1.39
        upper, lower = pt(.70, 2.74), pt(.70, -1.55)
        self.show(axis(2.74, r, .70), axis(-1.55, r, .70), ring(upper,r), ring(lower,r),
                  txt("입력 z", 3.7, 25, BLUE, -2.62),
                  txt("출력 z³", -.66, 25, GOLD, -2.62),
                  txt("각도 × 3", .59, 24, VIOLET, -2.62),
                  pointer(pt(.70, .78), pt(.70, .23), MUTED),
                  Dot(lower+pt(r,0), radius=.10, color=GREEN), run_time=.32)
        input_ray = always_redraw(lambda: pointer(upper, upper + r*unit(t.get_value()), BLUE))
        output_ray = always_redraw(lambda: pointer(lower, lower + r*unit(3*t.get_value()), GOLD))
        self.add(input_ray, output_ray)
        for k in range(3):
            if k:
                self.play(t.animate.set_value(k*TAU/3), run_time=1.28, rate_func=linear)
            self.show(Dot(upper + r*unit(k*TAU/3), color=GREEN, radius=.086),
                      txt((f"{120*k}° → {360*k}°"), -3.86, 25, GREEN, -2.58 + k*2.58),
                      run_time=.26)
        self.to(101)
        self.remove(input_ray, output_ray)
        self.clear()
        self.show(txt("회전과 극형식", 3.68, 27, BLUE, -1.75),
                  txt("인수분해와 근의 공식", 3.68, 27, GOLD, 1.74))
        for k, (y, formula) in enumerate(zip((2.34, .79, -.78), RECTANGULAR)):
            angle = ("0", r"2\pi i/3", r"4\pi i/3")[k]
            self.show(eq(fr"e^{{{angle}}}={formula}", y, 46))
        self.show(txt("두 방법에서 같은 세 해가 나온다", -3.1, 31, GREEN))
        self.to(108)

    def s07(self):
        top = eq(r"z^3=1", 4, 66)
        self.show(top, diagram(3, -.52, 2.13))
        self.play(Transform(top, eq(r"z^n=1", 4, 66)), run_time=.65)
        self.to(110)
        self.clear()
        self.show(eq(r"z^n=r^ne^{in\theta}=1", 3.79, 56))
        self.show(eq(r"r^n=1", 1.97, 44, BLUE, -1.86),
                  eq(r"n\theta=2\pi k", 1.97, 44, VIOLET, 1.73))
        self.show(eq(r"r=1", .55, 46, BLUE, -1.86),
                  eq(r"\theta=\frac{2\pi k}{n}", .55, 46, VIOLET, 1.73))
        self.show(eq(r"z_k=e^{2\pi i k/n}", -1.53, 64, GREEN),
                  eq(r"n\ge1,\quad k=0,1,\ldots,n-1", -3.25, 35, MUTED))
        self.to(119)
        self.clear()
        center = pt(0, .23)
        self.show(diagram(5, .23, 2.30), eq(r"z^5=1", 4.06, 57),
                  angle_arc(center, .74, 0, TAU/5), eq(r"72^\circ", .91, 34, VIOLET, .78))
        self.show(eq(r"\Delta\theta=\frac{360^\circ}{n}", -3.43, 49, VIOLET))
        self.to(125)
        self.clear(.3)
        for index, n in enumerate((3, 4, 5, 6, 12, 60)):
            column, row = index % 3, index // 3
            x, y = (column-1)*2.63, 2.25-row*3.86
            self.show(diagram(n, y, .96, x, grid=False),
                      eq(fr"z^{{{n}}}=1", y+1.50, 30, WHITE, x),
                      eq(fr"{360//n}^\circ", y-1.45, 28, GOLD, x), run_time=.45)
        self.to(131)
        self.clear(.25)
        self.show(txt("단위근", 2.8, 50, GOLD),
                  eq(r"\mu_n=\{z\in\mathbb C:z^n=1\}", .68, 48), run_time=.45)
        self.to(133)

    def s08(self):
        self.show(diagram(5, .69, 2.19), eq(r"z^5=1", 4.02, 55))
        self.to(137)
        self.show(eq(r"z_0+z_1+z_2+z_3+z_4=0", -3.02, 45, GREEN))
        self.to(140)
        self.clear(.3)
        self.show(eq(r"z^5+0z^4-1=0", 3.12, 55),
                  txt("근과 계수의 관계", 1.45, 30, MUTED),
                  eq(r"\sum_{k=0}^4 z_k=-(0)=0", -.63, 57, GREEN))
        self.to(144)
        self.clear(.30)
        vectors = roots(5)
        c, d, r = pt(0, 2.65), pt(-1.0,-3.53), 1.33
        self.show(ring(c, r), axis(2.65, r, grid=False),
                  txt("원점에서 각 해로", 4.66, 25),
                  txt("방향과 길이를 유지해 이어 붙이기", .46, 26), run_time=.4)
        originals = [pointer(c, c+r*v, color) for v, color in zip(vectors, COLORS)]
        self.show(*originals, run_time=.35)
        self.show(Dot(d, color=WHITE, radius=.085), eq("0", d[1]-.06, 28, MUTED, d[0]-.36))
        current = d
        for v, arrow in zip(vectors, originals):
            copy = arrow.copy()
            self.add(copy)
            self.play(copy.animate.shift(current-c), run_time=.59)
            current = current + r*v
        assert np.linalg.norm(current - d) < 1e-9
        self.show(Dot(d, color=GREEN, radius=.10), eq(r"\sum_{k=0}^4z_k=0", -4.30, 38, GREEN),
                  run_time=.42)
        self.to(151)

    def s09(self):
        center, radius = pt(0,.20), 2.28
        positions = [center+radius*v for v in roots(5)]
        plane = diagram(5, .20, radius)
        moving = VGroup(*(VGroup(Line(center, p, color=color, stroke_width=3),
                                  Dot(p, color=color, radius=.115))
                          for p, color in zip(positions, COLORS)))
        self.show(*plane[:3], moving, eq(r"\omega=e^{2\pi i/5}", 4, 54))
        self.show(eq(r"z\longmapsto \omega z", -3.15, 47, VIOLET),
                  angle_arc(center, .72, 0, TAU/5))
        self.play(Rotate(moving, angle=TAU/5, about_point=center), run_time=2.25)
        self.show(txt("72° 회전 · 같은 꼭짓점 집합", -4.03, 28, GREEN))
        self.to(158)
        self.clear(.28)
        self.show(diagram(5, -.13, 1.73),
                  eq(r"\omega^2\cdot\omega^4=\omega^6=\omega", 3.64, 49))
        c = pt(0,-.13)
        self.show(*(Dot(c + 1.73*roots(5)[i], color=col, radius=.12)
                    for i, col in ((2,GOLD),(4,GOLD),(1,GREEN))))
        self.show(txt("곱해도 해의 집합 안에 남는다", -2.98, 29, GREEN),
                  txt("순환군", -4.05, 27, VIOLET))
        self.to(163)

    def s10(self):
        self.show(txt("대수", 4.53, 27, MUTED), eq(r"z^n=1", 3.49, 65),
                  pointer(pt(0,2.84),pt(0,2.40),MUTED))
        self.show(txt("기하", 2.03, 27, MUTED))
        for x,n in zip((-2.57, 0, 2.57), (3,4,5)):
            self.show(diagram(n, .62, .96, x, grid=False), run_time=.36)
        self.to(168)
        self.show(txt("회전 대칭", -1.03, 27, VIOLET))
        shape = outline([pt(0,-2.47)+.87*v for v in roots(5)], VIOLET)
        self.show(ring(pt(0,-2.47),.99,VIOLET,False), shape,
                  eq(r"72^\circ", -2.13, 38, VIOLET, 1.55))
        self.play(Rotate(shape, angle=TAU/5, about_point=pt(0,-2.47)), run_time=1.12)
        self.show(eq(r"z_k=e^{2\pi i k/n}", -4.05, 41, GREEN))
        self.to(173)


class Shot01(UnityScene): shot = 0
class Shot02(UnityScene): shot = 1
class Shot03(UnityScene): shot = 2
class Shot04(UnityScene): shot = 3
class Shot05(UnityScene): shot = 4
class Shot06(UnityScene): shot = 5
class Shot07(UnityScene): shot = 6
class Shot08(UnityScene): shot = 7
class Shot09(UnityScene): shot = 8
class Shot10(UnityScene): shot = 9
