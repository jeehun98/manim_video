"""Euler characteristic as a visual count of connections and cycles."""
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
VERT = "#FFB454"
LINE = "#48D6C6"
FACE = "#61A8FF"
CYCLE = "#E58CFF"
FONT = "Malgun Gothic"
PHASE_ENDS = (21, 25, 56, 77, 92, 117, 144, 157, 173)


def label(s, size=27, color=WHITE):
    return Text(s, font=FONT, font_size=size, color=color)


def formula(*parts, size=45):
    m = MathTex(*parts, font_size=size, color=WHITE)
    return m


def wrap(s, limit=23):
    lines = []
    line = ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if len(trial) > limit and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def projected_polyhedron(vertices, faces, center, scale=1):
    pts = []
    for x, y, z in vertices:
        pts.append(np.array([center[0] + scale * (.72*x+.48*y),
                             center[1] + scale * (.82*z-.31*x+.23*y), 0]))
    fills = VGroup()
    edges = set()
    for face in faces:
        fills.add(Polygon(*(pts[i] for i in face), stroke_width=0,
                          fill_color=FACE, fill_opacity=.15))
        for a, b in zip(face, face[1:] + face[:1]):
            edges.add(tuple(sorted((a, b))))
    wires = VGroup(*[Line(pts[a], pts[b], color=LINE, stroke_width=3) for a, b in sorted(edges)])
    dots = VGroup(*[Dot(p, radius=.075, color=VERT) for p in pts])
    return VGroup(fills, wires, dots)


def polyhedra():
    cube_vertices = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    cube_faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4],
                  [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
    tet_vertices = [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
    tet_faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    cube = projected_polyhedron(cube_vertices, cube_faces, (-2.1, 1.7), .85)
    tet = projected_polyhedron(tet_vertices, tet_faces, (2.1, 1.7), .85)
    names = VGroup(label("정육면체", 24).move_to([-2.1, -.55, 0]),
                   label("정사면체", 24).move_to([2.1, -.55, 0]))
    counts = VGroup(label("V 8    E 12    F 6", 22, MUTED).move_to([-2.1, -1.25, 0]),
                    label("V 4    E 6    F 4", 22, MUTED).move_to([2.1, -1.25, 0]))
    results = VGroup(formula("8", "-", "12", "+", "6", "=", "2", size=38).move_to([-2.1, -2.05, 0]),
                     formula("4", "-", "6", "+", "4", "=", "2", size=38).move_to([2.1, -2.05, 0]))
    for f in results:
        f[-1].set_color(VERT)
    return VGroup(cube, tet, names, counts, results)


def triangle_points():
    return [np.array([-2.65, -.75, 0]), np.array([2.65, -.75, 0]), np.array([0, 2.85, 0])]


class EulerHomologyShort(Scene):
    def fit(self, m, width=8):
        if m.width > width:
            m.scale_to_fit_width(width)
        return m

    def heading(self, kicker, title):
        a = label(kicker, 21, CYCLE).move_to([0, 6.82, 0])
        b = self.fit(label(title, 31), 8).next_to(a, DOWN, buff=.2)
        return VGroup(a, b)

    def phase(self, t):
        for i, end in enumerate(PHASE_ENDS):
            if t < end:
                return i
        return len(PHASE_ENDS)-1

    def graph(self, filled=False):
        p = triangle_points()
        heading = self.heading("점 · 선 · 면", "연결과 고리의 탄생")
        face = Polygon(*p, stroke_width=0, fill_color=FACE, fill_opacity=.35)
        edge_objects = VGroup(Line(p[0], p[1], color=LINE, stroke_width=8),
                              Line(p[1], p[2], color=LINE, stroke_width=8),
                              Line(p[2], p[0], color=LINE, stroke_width=8))
        ring = Polygon(*p, stroke_color=CYCLE, stroke_width=9, fill_opacity=0)
        dots = VGroup(*[Dot(v, color=VERT, radius=.16) for v in p])
        if not filled:
            face.set_fill(opacity=0)
            for e in edge_objects:
                e.set_opacity(0)
            ring.set_stroke(opacity=0)
        else:
            face.set_fill(opacity=0)
        counts = label("V = 3       E = 0       F = 0", 27, MUTED).move_to([0, -2.35, 0])
        chi = formula("V", "-", "E", "+", "F", "=", "3", size=43).move_to([0, -3.22, 0])
        chi[0].set_color(VERT); chi[2].set_color(LINE); chi[4].set_color(FACE)
        beta = label("연결된 덩어리 3개", 24, CYCLE).move_to([0, -4.2, 0])
        if filled:
            for e in edge_objects:
                e.set_opacity(1)
            ring.set_stroke(opacity=1)
            counts.become(label("V = 3       E = 3       F = 0", 27, MUTED).move_to(counts))
            chi.become(formula("3", "-", "3", "+", "0", "=", "0", size=43).move_to(chi))
            beta.become(label("면으로 채워지지 않은 고리 1개", 24, CYCLE).move_to(beta))
        group = VGroup(heading, face, edge_objects, ring, dots, counts, chi, beta)
        return group

    def surface_icon(self, kind, center, scale=1):
        x, y = center
        if kind == "sphere":
            shell = Circle(radius=1.05*scale, stroke_color=FACE, stroke_width=4,
                           fill_color=FACE, fill_opacity=.24).move_to([x, y, 0])
            equator = Ellipse(width=2.05*scale, height=.65*scale,
                              color=LINE, stroke_width=2).move_to([x, y, 0])
            meridian = Ellipse(width=.75*scale, height=2.05*scale,
                               color=LINE, stroke_width=2).move_to([x, y, 0])
            return VGroup(shell, equator, meridian)
        if kind == "torus":
            outer = Ellipse(width=3.05*scale, height=1.95*scale,
                            stroke_color=FACE, stroke_width=4,
                            fill_color=FACE, fill_opacity=.6).move_to([x, y, 0])
            inner = Ellipse(width=1.12*scale, height=.65*scale,
                            stroke_color=CYCLE, stroke_width=4,
                            fill_color=BG, fill_opacity=1).move_to([x, y+.12*scale, 0])
            lower = ArcBetweenPoints([x-1.25*scale,y-.42*scale,0],
                                     [x+1.25*scale,y-.42*scale,0], angle=-.65,
                                     color=LINE, stroke_width=2.5)
            return VGroup(outer, lower, inner)
        left = self.surface_icon("torus", (x-.9*scale, y), scale*.72)
        right = self.surface_icon("torus", (x+.9*scale, y), scale*.72)
        bridge = Rectangle(width=1.45*scale, height=.55*scale, stroke_width=0,
                           fill_color=FACE, fill_opacity=.6).move_to([x, y-.36*scale, 0])
        return VGroup(left, right, bridge)

    def scene_for(self, i):
        if i == 0:
            h = self.heading("오일러 공식", "다른 도형, 같은 숫자")
            return VGroup(h, polyhedra())
        if i == 1:
            h = self.heading("왜 더하고 뺄까?", "V − E + F")
            eq = formula("V", "-", "E", "+", "F", "=", "2", size=75).move_to([0, 1.4, 0])
            for k, color in ((0, VERT), (2, LINE), (4, FACE), (6, CYCLE)):
                eq[k].set_color(color)
            desc = VGroup(label("V  꼭짓점", 26, VERT), label("E  모서리", 26, LINE),
                          label("F  면", 26, FACE)).arrange(DOWN, buff=.45).move_to([0, -1.8, 0])
            return VGroup(h, eq, desc)
        if i == 2:
            return self.graph()
        if i == 3:
            return self.graph(filled=True)
        if i == 4:
            h = self.heading("계산의 의미", "연결과 순환의 변화")
            a = label("점", 31, VERT).move_to([-2.8, 2.7, 0])
            b = label("선", 31, LINE).move_to([0, 2.7, 0])
            c = label("면", 31, FACE).move_to([2.8, 2.7, 0])
            d = label("연결의 기준", 22, MUTED).next_to(a, DOWN, buff=.3)
            e = label("연결 또는 순환", 22, MUTED).next_to(b, DOWN, buff=.3)
            f = label("고리를 채움", 22, MUTED).next_to(c, DOWN, buff=.3)
            arrows = VGroup(Arrow([-1.9,2.7,0],[-.85,2.7,0],buff=.05,color=EDGE),
                            Arrow([.8,2.7,0],[1.85,2.7,0],buff=.05,color=EDGE))
            eq = formula(r"\chi", "=", "V", "-", "E", "+", "F", size=65).move_to([0, -.9, 0])
            for k, col in ((2, VERT), (4, LINE), (6, FACE)):
                eq[k].set_color(col)
            note = label("값 2는 모든 도형에 적용되지 않는다", 24, CYCLE).move_to([0,-2.55,0])
            return VGroup(h,a,b,c,d,e,f,arrows,eq,note)
        if i == 5:
            h = self.heading("표면의 구멍", "관통하는 구멍마다 값이 변한다")
            cube = polyhedra()[0].copy().scale(.55).move_to([0,3.2,0])
            icons = VGroup(cube,
                           self.surface_icon("torus", (0,.9), .62),
                           self.surface_icon("double", (0,-1.6), .62))
            names = VGroup(label("정육면체 표면   χ = 2", 22, WHITE).move_to([0,2.15,0]),
                           label("손잡이 1개   χ = 0", 22, WHITE).move_to([0,-.35,0]),
                           label("손잡이 2개   χ = −2", 22, WHITE).move_to([0,-3,0]))
            rule = formula(r"\chi", "=", "2", "-", "2g", size=46).move_to([0,-4.2,0])
            rule[-1].set_color(CYCLE)
            for j in (1,2):
                icons[j].set_opacity(.12)
                names[j].set_opacity(.12)
            return VGroup(h,icons,names,rule)
        if i == 6:
            h = self.heading("호몰로지", "구멍에도 종류가 있다")
            two = VGroup(Dot([-1.0,2.95,0],radius=.3,color=VERT),
                         Dot([1.0,2.95,0],radius=.3,color=VERT))
            torus = self.surface_icon("torus", (0,.25), .75)
            sphere = self.surface_icon("sphere", (0,-2.55), .75)
            markers = VGroup(label("β₀ = 2   연결 성분", 25, VERT).move_to([0,2.05,0]),
                             label("β₁ = 2   독립적인 고리", 25, CYCLE).move_to([0,-1.2,0]),
                             label("β₂ = 1   닫힌 표면", 25, FACE).move_to([0,-4.05,0]))
            return VGroup(h,two,torus,sphere,markers)
        if i == 7:
            h = self.heading("두 계산의 만남", "구성 요소 = 공간의 구조")
            a = formula(r"\chi", "=", "V", "-", "E", "+", "F", size=59).move_to([0,2,0])
            b = formula(r"\chi", "=", r"\beta_0", "-", r"\beta_1", "+", r"\beta_2", size=59).move_to([0,-1.0,0])
            for eq in (a,b):
                eq[2].set_color(VERT); eq[4].set_color(CYCLE if eq is b else LINE); eq[6].set_color(FACE)
            desc = VGroup(label("꼭짓점 · 모서리 · 면", 24, MUTED).move_to([0,1.15,0]),
                          label("연결 성분 · 고리 · 닫힌 표면", 24, MUTED).move_to([0,-1.9,0]))
            arrow = Arrow([0,.72,0],[0,-.48,0],buff=.1,color=LINE,stroke_width=5)
            return VGroup(h,a,b,desc,arrow)
        h = self.heading("오일러 지표", "모양보다 연결 구조")
        shapes = polyhedra()
        shapes.scale(.78).move_to([0,1.3,0])
        eq = formula(r"\boxed{\chi=V-E+F}", size=59).move_to([0,-2.45,0])
        note = label("모양이 달라도, 연결 구조는 남는다", 27, CYCLE).move_to([0,-3.55,0])
        return VGroup(h,shapes,eq,note)

    def replace_text(self, group, idx, content, color=MUTED, size=27):
        old = group[idx]
        new = label(content, size, color).move_to(old)
        self.play(Transform(old, new), run_time=.3)
        return .3

    def construct(self):
        footer = Rectangle(width=9, height=2.2, fill_color=PANEL,
                           fill_opacity=1, stroke_width=0).move_to([0,-6.9,0])
        rule = Line([-4,5.85,0],[4,5.85,0], color=EDGE, stroke_width=1)
        self.add(footer, rule)
        visual = None
        caption = None
        last = -1
        start = 0
        for end, sentence in DATA["sentences"]:
            phase = self.phase(start)
            animations = []
            if phase != last:
                new = self.scene_for(phase)
                if visual is not None:
                    animations.append(FadeOut(visual))
                animations.append(FadeIn(new))
                visual = new
                last = phase
            new_caption = VGroup(*[label(line, 28) for line in wrap(sentence)])
            new_caption.arrange(DOWN, buff=.1)
            self.fit(new_caption, 8)
            new_caption.move_to([0,-6.58,0])
            if caption is not None:
                animations.append(FadeOut(caption))
            animations.append(FadeIn(new_caption))
            caption = new_caption
            duration = end-start
            intro = min(.3, duration*.22)
            self.play(*animations, run_time=intro)
            extra = 0
            if phase == 2 and start in (28,34,37):
                k = {28:0,34:1,37:2}[start]
                extra = .75 if start != 37 else 1.2
                actions = [visual[2][k].animate.set_opacity(1)]
                if k == 2:
                    actions.append(visual[3].animate.set_stroke(opacity=1))
                self.play(*actions, run_time=extra)
                count = ["V = 3       E = 1       F = 0", "V = 3       E = 2       F = 0", "V = 3       E = 3       F = 0"][k]
                result = ["2","1","0"][k]
                component = ["연결된 덩어리 2개","연결된 덩어리 1개","새로운 고리 1개"][k]
                visual[5].become(label(count,27,MUTED).move_to(visual[5]))
                chi = formula("3","-",str(k+1),"+","0","=",result,size=43).move_to(visual[6])
                visual[6].become(chi)
                visual[7].become(label(component,24,CYCLE).move_to(visual[7]))
            elif phase == 3 and start == 59:
                extra = 1.4
                self.play(visual[1].animate.set_fill(opacity=.35),run_time=extra)
                visual[5].become(label("V = 3       E = 3       F = 1",27,MUTED).move_to(visual[5]))
                visual[6].become(formula("3","-","3","+","1","=","1",size=43).move_to(visual[6]))
                visual[7].become(label("고리는 면의 경계로 남는다",24,FACE).move_to(visual[7]))
            elif phase == 5 and start == 96:
                extra = 1.4
                sphere = self.surface_icon("sphere", (0,3.2), .62)
                name = label("구의 표면   χ = 2",22,WHITE).move_to(visual[2][0])
                self.play(Transform(visual[1][0],sphere),
                          Transform(visual[2][0],name),run_time=extra)
            elif phase == 5 and start in (101,105):
                k = 1 if start == 101 else 2
                extra = 1.0
                self.play(visual[1][k].animate.set_opacity(1),
                          visual[2][k].animate.set_opacity(1),run_time=extra)
            self.wait(duration-intro-extra)
            start=end
