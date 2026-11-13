"""One discriminant drives a parabola, its roots, and its vertex; 175 s portrait."""
import importlib.util
import json
import cmath
from pathlib import Path
import numpy as np
from manim import *

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('discriminant_shared',HERE.parent/'newton01_local_linear/scene.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
World=shared.World;text=shared.text;fit=shared.fit
BG=shared.BG;INK=shared.INK;MUTED=shared.MUTED
F=shared.F;BLUE=shared.G;ORANGE=shared.SEC;PURPLE=shared.TAN;YELLOW=shared.LIMIT
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))


def quadratic(x,D,a=1):return a*(x-1)**2-D/(4*a)

def roots(D,a=1):
    offset=cmath.sqrt(complex(D))/(2*abs(a))
    return 1+offset,1-offset


def math(s):
    colors={'D':YELLOW,r'\mathrm{i}':PURPLE,r'x_1':BLUE,r'x_2':ORANGE,r'z_1':BLUE,r'z_2':ORANGE}
    return MathTex(s,font_size=36,color=INK,substrings_to_isolate=list(colors),tex_to_color_map=colors)


class GeometryLesson(shared.NewtonLesson):
    EQ_Y=-2.95;NOTE_Y=-4.35
    def eq(self,s,duration=.35,colors=None):
        if isinstance(s,(tuple,list)):
            m=MathTex(*s,font_size=36,color=INK)
            for piece,color in zip(m,colors or [INK]*len(s)):piece.set_color(color)
        else:m=math(s)
        m=fit(m,7.9).move_to([0,self.EQ_Y,0]).set_z_index(30)
        if hasattr(self,'equation'):
            old=self.equation;self.play(TransformMatchingTex(old,m),run_time=duration);self.remove(old)
        else:self.play(Write(m),run_time=duration)
        self.equation=m;self.add(m);return m
    def run_lines(self,actions):
        rows=[(end,line) for end,line in DATA['sentences'] if self.START<end<=self.END]
        assert len(rows)==len(actions),(type(self).__name__,len(rows),len(actions))
        for (end,line),action in zip(rows,actions):
            self.caption(line);action();target=end-self.START
            if self.time>target+.02:raise RuntimeError(f'{type(self).__name__}: {self.time} > {target}')
            self.wait(target-self.time)
    def setup_model(self,D=4,a=1,complex_plane=False,span=2,symmetry=False):
        self.D=ValueTracker(D);self.a=a;self.complex_plane=complex_plane
        self.show_symmetry=symmetry;self.show_vertex=False;self.show_height=False
        self.w=World(self,fn=lambda x:quadratic(x,self.D.get_value(),self.a),span=span)
        self.rename_axes(animate=False)
        self.symmetry=always_redraw(lambda:DashedLine(self.w.p(1,-self.w.span.get_value()),self.w.p(1,self.w.span.get_value()),color=PURPLE,stroke_width=2,dash_length=.1) if self.show_symmetry else VGroup())
        self.vertex=always_redraw(lambda:Dot(self.w.p(1,-self.D.get_value()/(4*self.a)),color=INK,radius=.075).set_z_index(12) if self.show_vertex and not self.complex_plane else VGroup())
        def height():
            h=-self.D.get_value()/(4*self.a)
            if self.show_height and not self.complex_plane and abs(h)>1e-8:
                return Line(self.w.p(1,0),self.w.p(1,h),color=INK,stroke_width=4)
            return VGroup()
        self.height_line=always_redraw(height)
        self.root_mobs=always_redraw(self.draw_roots)
        self.add(self.symmetry,self.height_line,self.vertex,self.root_mobs)
        if complex_plane:self.remove(self.w.graph)
        self.make_hud()
    def rename_axes(self,animate=True):
        labels=(r'\operatorname{Re}(z)',r'\operatorname{Im}(z)') if self.complex_plane else ('x','f(x)')
        m=VGroup(*[MathTex(label,font_size=23,color=PURPLE if self.complex_plane and i==1 else MUTED).move_to(self.w.names[i]) for i,label in enumerate(labels)])
        if animate:self.play(Transform(self.w.names,m),run_time=.55)
        else:self.w.names.become(m)
    def draw_roots(self):
        D=self.D.get_value()
        if D<0 and not self.complex_plane:return VGroup()
        if abs(D)<1e-8:return VGroup(Dot(self.w.p(1,0),color=INK,radius=.085).set_z_index(20))
        return VGroup(*[Dot(self.w.p(z.real,z.imag),color=color,radius=.075).set_z_index(20) for z,color in zip(roots(D,self.a),(BLUE,ORANGE))])
    def state(self):
        D=self.D.get_value()
        return 1 if D>1e-8 else (-1 if D<-1e-8 else 0)
    def make_hud(self,height=False):
        if hasattr(self,'data_hud'):
            self.data_hud.clear_updaters(recursive=True);self.remove(self.data_hud)
        label=MathTex('D=',font_size=29,color=YELLOW)
        num=DecimalNumber(self.D.get_value(),num_decimal_places=2,font_size=29,color=YELLOW,edge_to_fix=LEFT)
        cell=VGroup(label,num).arrange(RIGHT,buff=.12).move_to([-2.25,-1.8,0])
        num.add_updater(lambda m:m.set_value(self.D.get_value()))
        if height:
            hlabel=MathTex(r'h=-D/(4a)=',font_size=25,color=INK)
            hn=DecimalNumber(-self.D.get_value()/(4*self.a),num_decimal_places=2,font_size=25,color=INK,edge_to_fix=LEFT)
            other=VGroup(hlabel,hn).arrange(RIGHT,buff=.1).move_to([1.35,-1.8,0])
            hn.add_updater(lambda m:m.set_value(-self.D.get_value()/(4*self.a)))
        else:
            strings={1:'서로 다른 두 실근',0:'중근 · 중복도 2',-1:('서로 켤레인 복소근' if self.complex_plane else '실근 없음')}
            cached={k:text(s,21,INK) for k,s in strings.items()}
            other=always_redraw(lambda:cached[self.state()].copy().move_to([1.55,-1.8,0]))
        self.data_hud=VGroup(cell,other).set_z_index(30);self.add(self.data_hud)
    def change(self,D,t=1.5):self.play(self.D.animate.set_value(D),run_time=t,rate_func=smooth)
    def center_mark(self):
        self.show_symmetry=True
        self.center_dot=always_redraw(lambda:Dot(self.w.p(1,0),color=PURPLE,radius=.045).set_z_index(10));self.add(self.center_dot)
    def distances(self,full=False):
        def draw():
            D=self.D.get_value()
            if D<=1e-8:return VGroup()
            d=np.sqrt(D)/(2*abs(self.a));y=-.23
            if full:
                return VGroup(Line(self.w.p(1-d,y),self.w.p(1+d,y),color=YELLOW,stroke_width=4),*[Line(self.w.p(x,y-.07),self.w.p(x,y+.07),color=YELLOW) for x in (1-d,1+d)])
            return VGroup(*[Arrow(self.w.p(1,y),self.w.p(1+sign*d,y),buff=0,color=YELLOW,stroke_width=3,max_tip_length_to_length_ratio=.2) for sign in (-1,1)])
        m=always_redraw(draw);self.add(m);return m
    def projections(self):
        def draw():
            if self.D.get_value()>=-1e-8:return VGroup()
            rs=roots(self.D.get_value(),self.a)
            return VGroup(*[DashedLine(self.w.p(0,z.imag),self.w.p(z.real,z.imag),color=c,dash_length=.1,stroke_opacity=.5) for z,c in zip(rs,(BLUE,ORANGE))])
        m=always_redraw(draw);self.add(m);return m
    def to_complex(self):
        self.play(FadeOut(self.w.graph),run_time=.45)
        self.complex_plane=True;self.rename_axes();self.make_hud()
    def to_function(self):
        self.complex_plane=False;self.rename_axes();self.make_hud()
        self.w.graph.resume_updating();self.w.graph.update(0)
        self.play(FadeIn(self.w.graph),run_time=.45)
    def switch_orientation(self,a):
        # No interpolation through a=0: both explicitly displayed models are quadratic.
        self.play(FadeOut(self.w.graph),FadeOut(self.vertex),FadeOut(self.height_line),FadeOut(self.equation),FadeOut(self.note_mob),run_time=.3)
        del self.equation
        self.a=a
        self.make_hud(height=True)
        for mob in (self.w.graph,self.vertex,self.height_line):
            mob.resume_updating();mob.update(0)
        self.play(FadeIn(self.w.graph),FadeIn(self.vertex),FadeIn(self.height_line),run_time=.3)


class DG01Intro(GeometryLesson):
    START=0;END=11
    def construct(self):
        self.title('판별식에 숨겨진 기하학');self.setup_model(4)
        def a():self.eq(r'D=b^2-4ac',.5);self.note('ax² + bx + c = 0  ·  실수 계수  ·  a ≠ 0')
        def b():
            self.note('같은 포물선이 움직이며 교점의 개수가 달라진다')
            self.change(0,1.5);self.wait(.6);self.change(-4,1.5)
        def c():self.eq(r'D>0\quad D=0\quad D<0');self.note('왜 이 숫자 하나로 구분할 수 있을까?',YELLOW)
        self.run_lines([a,b,c])


class DG02Parabola(GeometryLesson):
    START=11;END=32
    def construct(self):
        self.title('방정식의 실근은 x축과의 교점');self.setup_model(-4)
        def a():self.eq(r'f_{D}(x)=(x-1)^2-\frac{D}{4}');self.change(4,1.8);self.note('a=1, b=−2, c=1−D/4  →  실제 판별식은 D')
        def b():
            self.eq(r'f_{D}(x_1)=f_{D}(x_2)=0');self.note('주황: x₂=0  /  파랑: x₁=2')
            for x,color in ((0,ORANGE),(2,BLUE)):
                self.play(Indicate(Dot(self.w.p(x,0),radius=.1,color=color),color=color),run_time=.6)
        def c():self.change(0,1.7);self.wait(.65);self.change(-4,1.7);self.wait(.6);self.change(4,1.7)
        def d():self.eq(r'D=b^2-4ac');self.note('교점의 위치와 판별식은 어떻게 연결될까?',YELLOW)
        self.run_lines([a,b,c,d])


class DG03Formula(GeometryLesson):
    START=32;END=42
    def construct(self):
        self.title('근의 공식을 두 부분으로');self.setup_model(4)
        def a():self.eq(r'x=\frac{-b\pm\sqrt{D}}{2a}');self.note('이차방정식의 근의 공식  ·  a ≠ 0')
        def b():self.play(Indicate(self.equation,color=YELLOW),run_time=.8);self.eq(r'x=\frac{-b+\sqrt{D}}{2a}\quad\text{or}\quad x=\frac{-b-\sqrt{D}}{2a}')
        def c():self.eq([r'x=',r'\frac{-b}{2a}',r'\pm',r'\frac{\sqrt{D}}{2a}'],colors=[INK,PURPLE,INK,YELLOW]);self.note('보라: 중심  /  노랑: 중심으로부터의 변위')
        self.run_lines([a,b,c])


class DG04Center(GeometryLesson):
    START=42;END=50
    def construct(self):
        self.title('첫 번째 항은 두 근의 중심');self.setup_model(4)
        def a():self.eq([r'm=',r'\frac{-b}{2a}',r'=1'],colors=[PURPLE,PURPLE,INK]);self.note('보라: 대칭축 x=m',PURPLE);self.center_mark()
        def b():self.distances();self.eq(r'\frac{x_1+x_2}{2}=m');self.note('두 근에서 같은 거리만큼 떨어진 중간 위치',PURPLE);self.change(2,1.1);self.change(4,1.1)
        self.run_lines([a,b])


class DG05Distance(GeometryLesson):
    START=50;END=67
    def construct(self):
        self.title('두 번째 항은 중심에서의 거리');self.setup_model(4,symmetry=True);self.center_mark()
        def a():self.eq([r'\frac{\sqrt{D}}{2a}',r'\qquad(D>0)'],colors=[YELLOW,INK]);self.distances();self.note('중심에서 양쪽 근을 향하는 같은 길이의 화살표',YELLOW)
        def b():self.eq([r'd=',r'\frac{\sqrt{D}}{2|a|}'],colors=[YELLOW,YELLOW]);self.w.zoom(span=1.4,t=1.2);self.note('거리에는 |a| 사용: a<0이어도 길이는 양수',YELLOW)
        def c():
            self.eq(r'x_1=m+d,\qquad x_2=m-d');self.change(1,1);self.change(4,1);self.w.zoom(span=2,t=.8)
            self.distances(full=True);self.eq(r'|x_1-x_2|=\frac{\sqrt{D}}{|a|}');self.note('두 근의 중심 m  +  중심으로부터의 거리 d')
        self.run_lines([a,b,c])


class DG06Merge(GeometryLesson):
    START=67;END=83
    def construct(self):
        self.title('D가 작아지면 두 근이 가까워진다');self.setup_model(4,symmetry=True);self.center_mark();self.distances()
        def a():self.eq(r'd=\frac{\sqrt{D}}{2|a|}\qquad(D\ge0)');self.note('a를 고정하고 판별식 D를 줄인다',YELLOW)
        def b():self.change(2,2.5);self.w.zoom(span=1.5,t=.7)
        def c():self.change(0,3.5);self.note('D=0: 두 근과 꼭짓점이 같은 위치에서 만난다',INK);self.wait(.7)
        def d():self.change(-.16,1.5);self.w.zoom(span=1.1,t=.8);self.eq(r'D<0:\quad \sqrt{D}\notin\mathbb{R}');self.note('포물선은 x축 위에 있고, 실수 교점은 없다')
        self.run_lines([a,b,c,d])


class DG07Complex(GeometryLesson):
    START=83;END=97
    def construct(self):
        self.title('실근이 없어져도 근이 사라진 것은 아니다');self.setup_model(-.16,span=1.1,symmetry=True)
        def a():
            self.eq(r'\sqrt{D}=\mathrm{i}\sqrt{-D}\quad(D\le0)');self.note('함수값 f(x)와 복소수의 허수부는 다른 좌표',PURPLE)
            self.change(0,.8);self.to_complex()
        def b():self.eq(r'D=0:\quad z_1=z_2=1');self.note('중근에서 출발해, 복소평면에서 두 근을 추적',INK);self.w.zoom(span=2,t=1)
        def c():self.eq(r'z_{1,2}=1\pm\mathrm{i}\frac{\sqrt{-D}}2');self.change(-4,3.5);self.projections();self.note('실수부 1 고정  /  허수부만 +와 −로 갈라진다',PURPLE)
        self.run_lines([a,b,c])


class DG08Continuity(GeometryLesson):
    START=97;END=120
    def construct(self):
        self.title('실수축에서 만나, 허수 방향으로');self.setup_model(-4,complex_plane=True,symmetry=True);self.projections()
        def a():
            self.eq(r'z_{1,2}=1\pm\frac{\sqrt{D}}2');self.note('파랑: +가지  /  주황: −가지  ·  같은 두 근을 추적')
            self.change(4,1.3);self.change(0,2);self.wait(.4);self.change(-4,2)
        def b():self.eq(r'D>0\ \longleftrightarrow\ D=0\ \longleftrightarrow\ D<0');self.change(0,2);self.wait(.6);self.change(4,2);self.note('D>0: 실근 2개  /  D=0: 중근  /  D<0: 켤레근',YELLOW)
        def c():
            paths=VGroup(*[TracedPath(lambda i=i:self.w.p(roots(self.D.get_value(),self.a)[i].real,roots(self.D.get_value(),self.a)[i].imag),stroke_color=color,stroke_width=2,stroke_opacity=.35) for i,color in enumerate((BLUE,ORANGE))]);self.add(paths)
            self.change(0,1.3);self.wait(.4);self.change(-4,1.8);self.note('중근도 중복도를 포함하면 두 근이 겹친 상태',INK)
        self.run_lines([a,b,c])


class DG09Square(GeometryLesson):
    START=120;END=136
    def construct(self):
        self.title('판별식은 꼭짓점의 높이이기도 하다');self.setup_model(-4,complex_plane=True,symmetry=True)
        def a():self.eq(r'D=b^2-4ac');self.to_function();self.note('복소평면에서 함수 그래프로: 세로축은 다시 f(x)',F)
        def b():self.eq(r'f(x)=ax^2+bx+c');self.eq(r'f(x)=a\left(x+\frac{b}{2a}\right)^2-\frac{D}{4a}',.6)
        def c():self.center_mark();self.show_vertex=True;self.eq([r'x_{\mathrm{vertex}}=',r'\frac{-b}{2a}'],colors=[INK,PURPLE]);self.note('대칭축과 꼭짓점의 가로 위치 m=1',PURPLE)
        def d():self.show_height=True;self.make_hud(height=True);self.eq(r'h=-\frac{D}{4a}');self.change(4,1.7);self.note('흰 점: 꼭짓점  /  흰 선: x축에서의 높이',INK)
        self.run_lines([a,b,c,d])


class DG10Orientation(GeometryLesson):
    START=136;END=151
    def construct(self):
        self.title('방향이 바뀌어도 교점의 규칙은 같다');self.setup_model(4,symmetry=True);self.show_vertex=True;self.show_height=True;self.make_hud(height=True)
        def a():self.eq(r'a=1,\qquad h=-\frac{D}{4}');self.note('a>0: 위로 열린 포물선',F);self.change(0,2);self.wait(.65);self.change(-4,2)
        def b():self.switch_orientation(-1);self.eq(r'a=-1,\qquad h=\frac{D}{4}');self.note('a<0: 아래로 열리지만, 실근 개수의 규칙은 같다',F);self.change(0,1.5);self.wait(.4);self.change(4,1.5)
        self.run_lines([a,b])


class DG11Conclusion(GeometryLesson):
    START=151;END=175
    def construct(self):
        self.title('하나의 판별식에 담긴 해의 기하학');self.setup_model(4,a=-1,symmetry=True)
        def a():self.eq(r'D=b^2-4ac');self.distances();self.note('하나의 D가 근의 위치와 포물선의 구조를 연결',YELLOW)
        def b():
            self.eq(r'|x_1-x_2|=\frac{\sqrt{D}}{|a|}');self.note('D>0: 중심에서 각각 같은 거리',YELLOW);self.wait(1)
            self.note('복소평면으로 전환: 세로축은 허수부',PURPLE);self.to_complex();self.eq(r'z_{1,2}=1\pm\mathrm{i}\frac{\sqrt{-D}}{2|a|}');self.change(-4,1.8);self.note('D<0: 같은 실수부, 반대 부호의 허수부',PURPLE);self.wait(.6)
            self.note('함수 그래프로 복귀: 세로축은 f(x)',F);self.to_function();self.show_vertex=True;self.show_height=True;self.make_hud(height=True);self.eq(r'h=-\frac{D}{4a}');self.change(4,1.6);self.note('완전제곱: D가 꼭짓점 높이를 결정',INK)
        def c():
            self.eq(r'\boxed{D=b^2-4ac}');self.note('근의 위치 · 복소근의 대칭 · 꼭짓점의 높이',YELLOW)
            self.change(0,1.3);self.wait(.4);self.change(-4,1.3);self.wait(.4);self.change(4,1.3)
        self.run_lines([a,b,c])
