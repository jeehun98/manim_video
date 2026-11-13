"""3D geometry of Lp regularization, timed to the supplied 176 s narration."""
import json
import math
import os
from pathlib import Path

import numpy as np
from manim import *
from scipy.optimize import brentq

ROOT = Path(__file__).parent
SCRIPT = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
PORTRAIT = os.environ.get("VIDEO_LAYOUT") == "portrait"
config.frame_width = 9 if PORTRAIT else 14.2222
config.frame_height = 16 if PORTRAIT else 8
config.background_color = "#0B1020"
config.pixel_width = int(os.environ.get("VIDEO_WIDTH", "1920"))
config.pixel_height = int(os.environ.get("VIDEO_HEIGHT", "1080"))
config.frame_rate = int(os.environ.get("VIDEO_FPS", "30"))

BG = "#0B1020"
INK = "#F1F5FB"
MUTED = "#9BAEC6"
CYAN = "#45D9C9"
ORANGE = "#FFAD55"
VIOLET = "#B69CFF"
GRID = "#41536E"
FONT = "Malgun Gothic"
A = np.array([2.0, .8, .35])
Q = np.array([1.0, 1.2, 1.6])


def loss(w):
    d = np.asarray(w) - A
    return float(np.dot(Q * d, d))


def optimum(p):
    if p == 1:
        return np.array([1., 0., 0.])
    if math.isinf(p):
        return np.clip(A, -1, 1)
    if p < 1:
        raise ValueError("The convex optimizer requires p >= 1")
    def weights(multiplier):
        return np.array([brentq(lambda x: 2*q*(x-a)+multiplier*p*x**(p-1),
                               0., float(a), xtol=1e-13) for a,q in zip(A,Q)])
    upper=1.
    while np.sum(weights(upper)**p)>1:
        upper*=2
    multiplier=brentq(lambda m: np.sum(weights(m)**p)-1,0.,upper,xtol=1e-12)
    result=weights(multiplier)
    if abs(np.sum(result**p)-1)>1e-8:
        raise RuntimeError(f"L{p} KKT root failed")
    return result


def caption_lines(s, limit=44):
    lines, line = [], ""
    for word in s.split():
        test = (line + " " + word).strip()
        if len(test) > limit and line:
            lines.append(line)
            line = word
        else:
            line = test
    lines.append(line)
    return "\n".join(lines)


class RegularizationGeometry(ThreeDScene):
    def fixed(self, obj):
        obj.set_z_index(100)
        self.add_fixed_in_frame_mobjects(obj)
        return obj

    def label(self, s, size=28, color=INK):
        return Text(s, font=FONT, font_size=size, color=color)

    def set_header(self, s):
        new = self.label(s, 29 if PORTRAIT else 28, INK)
        new.move_to([0, 7.1, 0] if PORTRAIT else [-3.0, 3.45, 0])
        width = 8.2 if PORTRAIT else 7.8
        if new.width > width:
            new.scale_to_fit_width(width)
        self.fixed(new)
        if hasattr(self, "header"):
            self.remove_fixed_in_frame_mobjects(self.header)
            self.remove(self.header)
        self.header = new
        self.add(new)

    def set_formula(self, tex, color=INK):
        new = MathTex(tex, font_size=34, color=color)
        new.move_to([0, 5.75, 0] if PORTRAIT else [3.6, 2.75, 0])
        width = 8.15 if PORTRAIT else 6.2
        if new.width > width:
            new.scale_to_fit_width(width)
        self.fixed(new)
        if hasattr(self, "formula"):
            self.remove_fixed_in_frame_mobjects(self.formula)
            self.remove(self.formula)
        self.formula = new
        self.add(new)

    def set_caption(self, s):
        new = self.label(caption_lines(s, 25 if PORTRAIT else 44), 29 if PORTRAIT else 26, INK)
        width = 7.9 if PORTRAIT else 12.5
        if new.width > width:
            new.scale_to_fit_width(width)
        new.move_to([0, -6.5 if PORTRAIT else -3.25, 0])
        back = RoundedRectangle(corner_radius=.15, width=8.35 if PORTRAIT else 13.2,
                                height=max(.68, new.height+.22),
                                fill_color=BG, fill_opacity=.88,
                                stroke_width=0).move_to(new)
        group = VGroup(back, new)
        self.fixed(group)
        if hasattr(self, "caption"):
            self.remove_fixed_in_frame_mobjects(self.caption)
            self.remove(self.caption)
        self.caption = group
        self.add(group)

    def lp_surface(self, p):
        if math.isinf(p):
            unit = np.linalg.norm(self.axes.c2p(1,0,0)-self.axes.c2p(0,0,0))
            return Cube(side_length=2*unit, fill_color=CYAN, fill_opacity=.35,
                        stroke_color=CYAN, stroke_width=1.3).move_to(self.axes.c2p(0,0,0))
        if p < 1:
            patches = VGroup()
            grid = np.linspace(0, PI/2, 9)
            for sx in (-1,1):
                for sy in (-1,1):
                    for sz in (-1,1):
                        def octant(u, v):
                            d = np.array([sx*math.sin(v)*math.cos(u),
                                          sy*math.sin(v)*math.sin(u), sz*math.cos(v)])
                            norm = np.sum(np.abs(d)**p)**(1/p)
                            return self.axes.c2p(*(d/norm))
                        for i in range(len(grid)-1):
                            for j in range(len(grid)-1):
                                u0,u1 = grid[i:i+2]
                                v0,v1 = grid[j:j+2]
                                patches.add(Polygon(octant(u0,v0), octant(u1,v0),
                                                    octant(u1,v1), octant(u0,v1),
                                                    fill_color=CYAN, fill_opacity=.37,
                                                    stroke_color=CYAN, stroke_width=.35,
                                                    stroke_opacity=.44))
            return patches
        def point(u, v):
            d = np.array([math.sin(v)*math.cos(u),
                          math.sin(v)*math.sin(u), math.cos(v)])
            norm = np.max(np.abs(d)) if math.isinf(p) else np.sum(np.abs(d)**p)**(1/p)
            return self.axes.c2p(*(d / max(norm, 1e-9)))
        return Surface(point, u_range=[0, TAU], v_range=[.001, PI-.001],
                       resolution=(16, 10),
                       checkerboard_colors=[ManimColor("#166B70"), ManimColor("#277F82")],
                       fill_opacity=.35, stroke_color=CYAN,
                       stroke_width=.45, stroke_opacity=.45)

    def octahedron(self):
        vertices = [np.eye(3)[i]*sign for i in range(3) for sign in (1,-1)]
        faces = VGroup()
        for sx in (1,-1):
            for sy in (1,-1):
                for sz in (1,-1):
                    points = [self.axes.c2p(sx,0,0), self.axes.c2p(0,sy,0),
                              self.axes.c2p(0,0,sz)]
                    faces.add(Polygon(*points, fill_color=CYAN, fill_opacity=.38,
                                      stroke_color=CYAN, stroke_width=1.4))
        return faces

    def ellipsoid(self, c):
        r = np.sqrt(c/Q)
        return Surface(lambda u,v: self.axes.c2p(*(A+r*np.array([
            math.sin(v)*math.cos(u), math.sin(v)*math.sin(u), math.cos(v)]))),
            u_range=[0, TAU], v_range=[.001, PI-.001], resolution=(16, 10),
            checkerboard_colors=[ManimColor("#A15C29"), ManimColor("#CF7C3E")],
            fill_opacity=.15, stroke_color=ORANGE,
            stroke_width=.35, stroke_opacity=.32)

    def contact(self, p):
        w = optimum(p)
        return Dot3D(self.axes.c2p(*w), radius=.085, color=INK), w

    def replace_shape(self, p, run_time=1.5):
        new = self.octahedron() if p == 1 else self.lp_surface(p)
        if hasattr(self, "shape"):
            self.play(FadeOut(self.shape), FadeIn(new), run_time=run_time)
        else:
            self.play(FadeIn(new), run_time=run_time)
        self.shape = new

    def replace_solution(self, p, run_time=1.2):
        new, w = self.contact(p)
        shell = self.ellipsoid(loss(w))
        if hasattr(self, "solution"):
            self.play(ReplacementTransform(self.solution, new),
                      FadeOut(self.loss_shell), FadeIn(shell), run_time=run_time)
        else:
            self.play(FadeIn(new), FadeIn(shell), run_time=run_time)
        self.solution, self.loss_shell = new, shell
        return w

    def construct(self):
        self.set_camera_orientation(phi=67*DEGREES, theta=-57*DEGREES,
                                    zoom=1.25 if PORTRAIT else 1.12)
        self.axes = ThreeDAxes(x_range=[-2.5,2.5,1], y_range=[-2.5,2.5,1],
                               z_range=[-2.5,2.5,1], x_length=5.8 if PORTRAIT else 6.3,
                               y_length=5.8 if PORTRAIT else 6.3,
                               z_length=5.8 if PORTRAIT else 6.3, tips=False,
                               axis_config={"color": GRID, "stroke_width": 1.5})
        self.axes.shift(LEFT*(.95 if PORTRAIT else .7)+DOWN*.1)
        origin = Dot3D(self.axes.c2p(0,0,0), radius=.045, color=MUTED)
        minimum = Dot3D(self.axes.c2p(*A), radius=.095, color=ORANGE)
        self.origin, self.minimum = origin, minimum
        self.add(self.axes, origin, minimum)
        self.set_header("손실의 최소점과 규제")
        self.set_formula(r"\mathcal L_{\mathrm{data}}(\mathbf w)")
        self.initial_shells = VGroup(self.ellipsoid(.42))
        self.play(FadeIn(self.initial_shells), run_time=1.5)
        actions = {
            1: self.action_penalty,
            4: self.action_lambda,
            6: self.action_coordinates,
            8: self.action_loss_shells,
            11: self.action_constraint,
            13: self.action_l2,
            19: self.action_l2_contact,
            20: self.action_l1_intro,
            22: self.action_l1,
            25: self.action_zero,
            27: self.action_l1_contact,
            29: self.action_p,
            31: self.action_p1_to_p2,
            32: self.action_p4,
            33: self.action_pinf,
            34: self.action_p07,
            36: self.action_final,
        }
        previous = 0
        for i, (end, sentence) in enumerate(SCRIPT["sentences"]):
            self.set_caption(sentence)
            before = self.time
            if i in actions:
                actions[i]()
            remaining = end - self.time
            if remaining < -1e-3:
                raise RuntimeError(f"Sentence {i+1} overran {end}s by {-remaining:.2f}s")
            if remaining > 0:
                self.wait(remaining)
            previous = end

    def action_penalty(self):
        self.set_formula(r"\mathcal L_{\rm data}(\mathbf w)+\lambda R(\mathbf w)")
        self.play(Indicate(self.minimum, color=ORANGE, scale_factor=1.5), run_time=1)

    def action_lambda(self):
        self.set_header("규제 강도 λ가 커지면")
        self.set_formula(r"\min_{\mathbf w}\;\mathcal L_{\rm data}+\lambda R")
        start = self.axes.c2p(*A)
        end = self.axes.c2p(*optimum(2))
        moving = Dot3D(start, radius=.08, color=INK)
        self.add(moving)
        self.play(moving.animate.move_to(end), run_time=2.2)
        self.play(FadeOut(moving), run_time=.3)

    def action_coordinates(self):
        self.set_header("세 가중치 = 3D 공간의 한 점")
        self.set_formula(r"\mathbf w=(w_1,w_2,w_3)")
        self.move_camera(phi=72*DEGREES, theta=-42*DEGREES, run_time=1.6)

    def action_loss_shells(self):
        self.set_header("손실이 같은 점들의 표면")
        self.set_formula(r"\mathcal L=(\mathbf w-\mathbf a)^TQ(\mathbf w-\mathbf a)")
        layers = VGroup(self.ellipsoid(.9), self.ellipsoid(1.6))
        self.initial_shells.add(*layers)
        self.play(FadeIn(layers), run_time=1.3)

    def action_constraint(self):
        self.set_header("벌점 문제 ↔ 제약 문제")
        self.set_formula(r"\min\mathcal L(\mathbf w)\quad\mathrm{s.t.}\;\|\mathbf w\|_p\leq1")
        self.play(Indicate(self.origin, color=CYAN), run_time=.9)

    def action_l2(self):
        self.set_header("L2: 제곱합의 경계는 구")
        self.set_formula(r"w_1^2+w_2^2+w_3^2\leq1")
        self.replace_shape(2, 1.6)
        self.move_camera(phi=62*DEGREES, theta=-61*DEGREES, run_time=1.2)

    def action_l2_contact(self):
        self.set_header("등손실면이 처음 닿는 곳")
        self.play(FadeOut(self.initial_shells), run_time=.5)
        self.replace_solution(2, 1.5)

    def action_l1_intro(self):
        self.set_header("L1: 절댓값의 합")
        self.set_formula(r"|w_1|+|w_2|+|w_3|\leq1")

    def action_l1(self):
        self.set_header("8개 삼각형 면 · 6개 꼭짓점")
        self.replace_shape(1, 1.7)
        self.move_camera(phi=68*DEGREES, theta=-30*DEGREES, run_time=1.5)

    def action_zero(self):
        self.set_header("모서리에는 0이 되는 좌표")
        self.set_formula(r"(w_1,0,0)\quad\mathrm{or}\quad(w_1,w_2,0)", VIOLET)
        vertex = Dot3D(self.axes.c2p(1,0,0), radius=.11, color=VIOLET)
        self.zero_vertex = vertex
        self.play(FadeIn(vertex), run_time=.5)
        self.play(Indicate(vertex, color=VIOLET), run_time=.8)

    def action_l1_contact(self):
        self.set_header("L1 해: (1, 0, 0)")
        self.set_formula(r"\mathbf w^*_1=(1,0,0)", VIOLET)
        self.replace_solution(1, 1.4)

    def action_p(self):
        self.set_header("하나의 지수 p를 바꾼다")
        self.set_formula(r"\|\mathbf w\|_p=(|w_1|^p+|w_2|^p+|w_3|^p)^{1/p}")

    def action_p1_to_p2(self):
        self.set_header("p = 1: 정팔면체")
        self.wait(.35)
        self.set_header("p = 2: 구")
        self.play(FadeOut(self.zero_vertex), run_time=.2)
        self.replace_shape(2, .8)
        self.replace_solution(2, .65)

    def action_p4(self):
        self.set_header("p = 4: 부푼 경계")
        self.replace_shape(4, 1.0)
        self.replace_solution(4, .7)

    def action_pinf(self):
        self.set_header("p → ∞: 가장 큰 좌표가 결정")
        self.set_formula(r"\|\mathbf w\|_\infty=\max_i|w_i|")
        self.replace_shape(math.inf, 1.0)
        self.replace_solution(math.inf, .7)

    def action_p07(self):
        self.set_header("p < 1: 안쪽으로 오목한 경계")
        self.set_formula(r"|w_1|^{0.7}+|w_2|^{0.7}+|w_3|^{0.7}\leq1")
        self.replace_shape(.7, 1.0)
        self.play(FadeOut(self.solution), FadeOut(self.loss_shell), run_time=.4)
        del self.solution, self.loss_shell

    def action_final(self):
        self.set_header("정의가 바뀌면 해의 성질도 달라진다")
        self.set_formula(r"\min_{\mathbf w}\left[\mathcal L_{\rm data}(\mathbf w)+\lambda R(\mathbf w)\right]")
        self.move_camera(phi=62*DEGREES, theta=-57*DEGREES, run_time=1.5)
