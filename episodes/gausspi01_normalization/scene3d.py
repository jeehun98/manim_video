"""A camera-led 3D proof of the Gaussian normalization constant."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene import BG, EDGE, FONT, GX, GY, MUTED, PANEL, PI, WHITE, bell, bell_area, g, graph_axes, tex, text, wrap

DATA = json.loads((Path(__file__).parent / "script.json").read_text(encoding="utf-8"))


def title(kicker, main):
    a = text(kicker, 21, PI).move_to([0, 6.82, 0])
    b = text(main, 30, WHITE)
    if b.width > 8:
        b.scale_to_fit_width(8)
    b.next_to(a, DOWN, buff=.18)
    return VGroup(a, b).set_z_index(110)


def fit(m, width=8):
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def gaussian_surface(axes):
    surface = Surface(
        lambda x, y: axes.c2p(x, y, g(x)*g(y)),
        u_range=[-3, 3], v_range=[-3, 3], resolution=(22, 22),
        checkerboard_colors=[ManimColor("#194354"), ManimColor("#245A70")],
        fill_opacity=.68, stroke_color=ManimColor("#92DCE4"),
        stroke_width=.25, stroke_opacity=.34,
    )
    return surface


def Gaussian_curve(axes, along="x"):
    if along == "x":
        fn = lambda t: axes.c2p(t, 0, g(t))
        color = GX
    else:
        fn = lambda t: axes.c2p(0, t, g(t))
        color = GY
    return ParametricFunction(fn, t_range=[-3, 3], color=color, stroke_width=6)


def surface_mesh(axes):
    mesh = VGroup()
    for q in np.linspace(-2.75, 2.75, 10):
        mesh.add(ParametricFunction(
            lambda t, q=q: axes.c2p(t, q, g(t)*g(q)+.008),
            t_range=[-3, 3], color=GX, stroke_width=1.4, stroke_opacity=.65))
        mesh.add(ParametricFunction(
            lambda t, q=q: axes.c2p(q, t, g(q)*g(t)+.008),
            t_range=[-3, 3], color=GY, stroke_width=1.4, stroke_opacity=.65))
    return mesh


def contour(axes, radius, color=PI, width=4):
    height = g(radius)
    return ParametricFunction(
        lambda t: axes.c2p(radius*math.cos(t), radius*math.sin(t), height+.012),
        t_range=[0, TAU], color=color, stroke_width=width)


def ring_volume(axes, radius, half_width=.095):
    """A thin annular volume, with its top on z=g(x)g(y)."""
    lo, hi = radius-half_width, radius+half_width
    top = Surface(
        lambda angle, r: axes.c2p(r*math.cos(angle), r*math.sin(angle), g(r)),
        u_range=[0, TAU], v_range=[lo, hi], resolution=(36, 3),
        checkerboard_colors=[ManimColor("#D69A4E"), ManimColor("#E6AD65")],
        fill_opacity=.9, stroke_width=0)
    outer = Surface(
        lambda angle, z: axes.c2p(hi*math.cos(angle), hi*math.sin(angle), z),
        u_range=[0, TAU], v_range=[0, g(hi)], resolution=(36, 5),
        checkerboard_colors=[ManimColor("#A56733"), ManimColor("#BB7941")],
        fill_opacity=.36, stroke_width=0)
    inner = Surface(
        lambda angle, z: axes.c2p(lo*math.cos(angle), lo*math.sin(angle), z),
        u_range=[0, TAU], v_range=[0, g(lo)], resolution=(36, 5),
        checkerboard_colors=[ManimColor("#A56733"), ManimColor("#BB7941")],
        fill_opacity=.26, stroke_width=0)
    rim = contour(axes, radius, PI, 5)
    return VGroup(outer, inner, top, rim)


def sample_columns(axes):
    first, rest = VGroup(), VGroup()
    for ix in range(-2, 3):
        for iy in range(-2, 3):
            x, y = ix*.92, iy*.92
            height = g(x)*g(y)
            prism = Prism(dimensions=[.75, .75, max(.045, height*2.34)],
                          fill_color=GX if (ix+iy)%2 else GY,
                          fill_opacity=.30 if abs(ix)<=1 and abs(iy)<=1 else .16,
                          stroke_color=WHITE,
                          stroke_width=.35, stroke_opacity=.28)
            prism.move_to(axes.c2p(x, y, height/2))
            (first if abs(ix)<=1 and abs(iy)<=1 else rest).add(prism)
    return first, rest


class GaussianPi3DShort(ThreeDScene):
    def overlay(self, m):
        m.set_z_index(110)
        self.add_fixed_in_frame_mobjects(m)
        return m

    def replace_overlay(self, old, new, duration=.5):
        new.move_to(old).set_z_index(110)
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=duration)
        self.remove_fixed_in_frame_mobjects(old)
        return new

    def make_world(self):
        axes = ThreeDAxes(
            x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], z_range=[0, 1.2, .2],
            x_length=6.4, y_length=6.4, z_length=2.8, tips=False,
            axis_config={"color": MUTED, "stroke_width": 1.4})
        labels = VGroup(
            MathTex("x", color=GX, font_size=30).move_to(axes.c2p(3.45, 0, 0)),
            MathTex("y", color=GY, font_size=30).move_to(axes.c2p(0, 3.45, 0)),
            MathTex("z", color=PI, font_size=30).move_to(axes.c2p(0, 0, 1.3)),
        )
        self.add_fixed_orientation_mobjects(*labels)
        return {"axes": axes, "labels": labels, "gx": Gaussian_curve(axes),
                "gy": Gaussian_curve(axes, "y"), "surface": gaussian_surface(axes),
                "mesh": surface_mesh(axes),
                "contours": VGroup(*[contour(axes, r) for r in (.75, 1.35, 2.0, 2.6)]),
                "columns": sample_columns(axes)}

    def flat_intro(self):
        h = title("정규분포", "종 모양 곡선 속의 π")
        axes = graph_axes((0, -1.25))
        curve = bell(normalized=True, center=(0, -1.25))
        eq = fit(tex(r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}", size=43)).move_to([0, 3.45, 0])
        eq.set_color_by_tex(r"\pi", PI)
        eq.set_opacity(0)
        circle = Circle(radius=.55, color=PI, stroke_width=3, fill_opacity=0).move_to([0, -3.45, 0])
        circle.set_stroke(opacity=0)
        return VGroup(h, axes, curve, eq, circle)

    def flat_prelude(self):
        h = title("평균과 표준편차", "먼저 정규화 계수를 떼어낸다")
        axes = graph_axes((0, -1.4))
        area = bell_area((0, -1.4)); area.set_fill(opacity=0)
        curve = bell(normalized=True, center=(0, -1.4))
        eq = fit(tex(r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}", size=41)).move_to([0, 3.6, 0])
        eq.set_color_by_tex(r"\mu", GX); eq.set_color_by_tex(r"\sigma", GY)
        legend = VGroup(text("μ  중심 위치", 22, GX), text("σ  퍼진 정도", 22, GY)).arrange(RIGHT, buff=.6).move_to([0, 2.8, 0])
        unknown = text("A = ?", 30, PI).move_to([0, -3.45, 0]); unknown.set_opacity(0)
        return VGroup(h, axes, area, curve, eq, legend, unknown)

    def flat_final(self):
        h = title("처음의 넓이로 돌아가기", "원 속에 숨어 있던 정규화 계수")
        axes = graph_axes((0, -.85), 3.3)
        area = bell_area((0, -.85), .93, 2.5)
        curve = bell(center=(0, -.85), width=.93, height=2.5)
        eq = tex("A^2", "=", r"2\pi", size=65).move_to([0, 3.7, 0]); eq[2].set_color(PI)
        full = tex(r"f(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}", size=48).move_to([0, -3.6, 0])
        full.set_color_by_tex(r"\pi", PI); full.set_opacity(0)
        circles = VGroup(*[Circle(radius=r, color=PI, stroke_width=2, stroke_opacity=0,
                                  fill_opacity=0).move_to([0, -.85, 0]) for r in (.65, 1.25, 1.85)])
        return VGroup(h, axes, area, curve, eq, full, circles)

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1)
        self.renderer.camera.light_source.move_to([-7, -9, 11])
        footer = Rectangle(width=9, height=2.2, fill_color=PANEL, fill_opacity=1,
                           stroke_width=0).move_to([0, -6.9, 0]).set_z_index(90)
        divider = Line([-4, 5.85, 0], [4, 5.85, 0], color=EDGE, stroke_width=1).set_z_index(90)
        self.add_fixed_in_frame_mobjects(footer, divider)

        flat = None
        world = None
        heading = None
        equation = None
        note = None
        columns_visible = False
        ring = None
        caption = None

        for end, sentence in DATA["sentences"]:
            start = self.time
            duration = end - start
            if duration <= 0:
                raise RuntimeError(f"Timing overrun before {end}s: {start:.3f}s")
            new_caption = VGroup(*[text(line, 28) for line in wrap(sentence)]).arrange(DOWN, buff=.1)
            fit(new_caption, 8)
            new_caption.move_to([0, -6.58, 0]).set_z_index(120)
            self.add_fixed_in_frame_mobjects(new_caption)
            anims = [FadeIn(new_caption)]
            if caption is not None:
                anims.append(FadeOut(caption))
            caption = new_caption

            tick = int(round(start))
            if tick == 0:
                flat = self.overlay(self.flat_intro())
                anims.append(FadeIn(flat))
            elif tick == 15:
                new_flat = self.overlay(self.flat_prelude())
                anims.extend([FadeOut(flat), FadeIn(new_flat)]); flat = new_flat
            elif tick == 40:
                anims.append(FadeOut(flat)); flat = None
                self.set_camera_orientation(phi=88*DEGREES, theta=-90*DEGREES, zoom=.94)
                world = self.make_world()
                self.add(world["axes"], world["gx"])
                anims.extend([FadeIn(world["axes"]), Create(world["gx"])])
                heading = self.overlay(title("차원을 올리기", "곡선은 xz 평면에 남는다"))
                equation = self.overlay(tex(r"z=g(x)=e^{-x^2/2}", size=49).move_to([0, -3.75, 0]))
                equation.set_color_by_tex(r"g(x)", GX)
                anims.extend([FadeIn(heading), FadeIn(equation)])
            elif tick == 50:
                self.add(world["gy"])
                anims.append(Create(world["gy"]))
                heading = self.replace_overlay(heading, title("두 방향의 곱", "곡선 두 개가 곡면을 만든다"), .35)
                equation = self.replace_overlay(equation, tex(r"z=g(x)g(y)", size=50).move_to([0,-3.75,0]), .35)
            elif tick == 94:
                heading = self.replace_overlay(heading, title("넓이의 제곱", "두 방향의 작은 넓이를 곱한다"), .35)
                volume_eq = tex("V", "=", "A", r"\times", "A", "=", "A^2", size=53).move_to([0,-3.75,0])
                volume_eq[2].set_color(GX); volume_eq[4].set_color(GY)
                equation = self.replace_overlay(equation, volume_eq, .35)
            elif tick == 122:
                heading = self.replace_overlay(heading, title("원형 고리의 합", "곡면 아래의 얇은 고리"), .35)
                equation = self.replace_overlay(equation, fit(tex(r"dV=2\pi r\,e^{-r^2/2}\,dr", size=45)).move_to([0,-3.75,0]), .35)
            elif tick == 155:
                if ring is not None: anims.append(FadeOut(ring))
                anims.extend([FadeOut(world["axes"]), FadeOut(world["gx"]), FadeOut(world["gy"]),
                              FadeOut(world["surface"]), FadeOut(world["mesh"]), FadeOut(world["contours"]),
                              FadeOut(world["labels"]), FadeOut(heading), FadeOut(equation)])

            intro = min(.3, duration*.2)
            self.play(*anims, run_time=intro)

            if tick == 155:
                self.set_camera_orientation(phi=0, theta=-90*DEGREES, zoom=1)
                flat = self.overlay(self.flat_final())
                self.play(FadeIn(flat), run_time=.3)

            if tick == 9:
                self.play(flat[3].animate.set_opacity(1), flat[4].animate.set_stroke(opacity=1), run_time=.8)
            elif tick == 18:
                self.play(Transform(flat[3], bell(mu=.65, normalized=True, center=(0,-1.4))), run_time=1.5)
                self.play(Transform(flat[3], bell(sigma=1.5, normalized=True, center=(0,-1.4))), run_time=1.5)
            elif tick == 23:
                self.play(Transform(flat[3], bell(center=(0,-1.4))),
                          Transform(flat[4], tex(r"g(x)=e^{-x^2/2}",size=49).move_to(flat[4])), run_time=1.3)
            elif tick == 32:
                self.play(flat[2].animate.set_fill(opacity=.25), flat[6].animate.set_opacity(1), run_time=.8)
            elif tick == 44:
                self.move_camera(phi=62*DEGREES, theta=-55*DEGREES, zoom=.90, run_time=2.5)
            elif tick == 56:
                samples = VGroup()
                a = world["axes"]
                for x,y in [(-1.5,-1.2),(-1.5,1.2),(0,0),(1.5,-1.2),(1.5,1.2),(-.8,.6),(.8,-.6)]:
                    samples.add(Line3D(a.c2p(x,y,0), a.c2p(x,y,g(x)*g(y)), color=PI, thickness=.015))
                self.add(samples)
                self.play(FadeIn(samples), run_time=.65)
                self.add(world["surface"], world["mesh"])
                self.play(FadeIn(world["surface"]), FadeIn(world["mesh"]), run_time=1.25)
                self.play(FadeOut(samples), run_time=.35)
            elif tick == 66:
                self.move_camera(theta=-40*DEGREES, zoom=.98, run_time=1.3)
            elif tick == 68:
                self.move_camera(phi=6*DEGREES, theta=-90*DEGREES, zoom=.88, run_time=2.2)
            elif tick == 72:
                self.add(world["contours"])
                self.play(Create(world["contours"]), run_time=1.2)
            elif tick in (74, 79, 83):
                expr = {74:r"g(x)g(y)=e^{-(x^2+y^2)/2}", 79:r"x^2+y^2=r^2", 83:r"z=e^{-r^2/2}"}[tick]
                equation = self.replace_overlay(equation, fit(tex(expr,size=47)).move_to([0,-3.75,0]), .7)
            elif tick == 97:
                self.move_camera(phi=55*DEGREES, theta=-55*DEGREES, zoom=.92, run_time=2.1)
            elif tick == 103:
                self.play(world["surface"].animate.set_fill(opacity=.26),
                          world["mesh"].animate.set_stroke(opacity=.23), run_time=.7)
                self.add(world["columns"][0])
                self.play(FadeIn(world["columns"][0]), run_time=1.1)
                columns_visible = True
            elif tick == 109:
                self.add(world["columns"][1])
                self.play(FadeIn(world["columns"][1]), run_time=1.2)
                equation = self.replace_overlay(equation,
                    fit(tex(r"(g(x)\,\Delta x)(g(y)\,\Delta y)\to V=A^2",size=38)).move_to([0,-3.75,0]), .6)
            elif tick == 117:
                self.move_camera(theta=-68*DEGREES, zoom=.98, run_time=1.0)
            elif tick == 122:
                if columns_visible:
                    self.play(FadeOut(world["columns"][0]), FadeOut(world["columns"][1]),
                              world["surface"].animate.set_fill(opacity=.58),
                              world["mesh"].animate.set_stroke(opacity=.38), run_time=.7)
                self.move_camera(phi=17*DEGREES, theta=-80*DEGREES, zoom=.9, run_time=1.5)
                ring = ring_volume(world["axes"], .72)
                self.add(ring)
                self.play(FadeIn(ring), run_time=.6)
            elif tick == 126:
                self.move_camera(phi=58*DEGREES, theta=-58*DEGREES, zoom=1.04, run_time=1.7)
                self.play(Transform(ring, ring_volume(world["axes"], 1.18)), run_time=1.0)
            elif tick in (134, 138):
                self.play(Transform(ring, ring_volume(world["axes"], 1.7 if tick==134 else 2.25)),run_time=1.1)
            elif tick == 141:
                equation = self.replace_overlay(equation,
                    fit(tex(r"V=2\pi\int_0^\infty r e^{-r^2/2}\,dr",size=42)).move_to([0,-3.75,0]), .7)
            elif tick == 146:
                equation = self.replace_overlay(equation,
                    fit(tex(r"u=r^2/2,\quad\int_0^\infty e^{-u}\,du=1",size=37)).move_to([0,-3.75,0]), .7)
            elif tick == 152:
                equation = self.replace_overlay(equation,tex(r"\boxed{V=2\pi}",size=62).move_to([0,-3.75,0]), .7)
            elif tick == 155:
                new = tex(r"A=\sqrt{2\pi}",size=65).move_to(flat[4]); new.set_color_by_tex(r"\pi",PI)
                self.add_fixed_in_frame_mobjects(new)
                self.play(FadeOut(flat[4]), FadeIn(new), run_time=.65)
            elif tick == 161:
                self.play(flat[5].animate.set_opacity(1),
                          Transform(flat[3],bell(normalized=True,center=(0,-.85),width=.93,height=2.5)),
                          flat[2].animate.set_fill(opacity=.1),run_time=1.3)
            elif tick == 168:
                self.play(flat[6].animate.set_stroke(opacity=.35),run_time=.8)

            remaining = end-self.time
            if remaining < -.04:
                raise RuntimeError(f"Timing overrun at {end}s: {self.time:.3f}s")
            if remaining > 0:
                self.wait(remaining, frozen_frame=True)
        if self.time < 177 - 1/60:
            self.wait(177-self.time)
