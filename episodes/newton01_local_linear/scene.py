"""Newton method: exact geometric updates, independent narration-timed portrait scenes."""
import importlib.util
import json
from pathlib import Path
import numpy as np
from manim import *

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('newton_shared_ui',HERE.parent/'lhopital01_relative_change/scene.py')
ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(ui)
text=ui.text;fit=ui.fit
BG=ui.BG;INK=ui.INK;MUTED=ui.MUTED;F=ui.F;G=ui.G;SEC=ui.SEC;TAN=ui.TAN;LIMIT=ui.LIMIT
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
f=lambda x:x**3-x-1
df=lambda x:3*x*x-1
ROOT=float(next(r.real for r in np.roots([1,0,-1,-1]) if abs(r.imag)<1e-10))
XS=[1.5]
for _ in range(5):XS.append(XS[-1]-f(XS[-1])/df(XS[-1]))


def fm(s,size=36):
    # Whole semantic tokens are isolated, so prime signs remain on their functions.
    colors={r'f(x)':F,r'f(x_n)':F,r'f^{\prime}(x_n)':SEC,r'\Delta x':LIMIT,
            r'x_{n+1}':LIMIT,r'J_F':SEC,r'F(\mathbf{x}_n)':F,
            r'h^{\prime}(x_n)':F,r'h^{\prime\prime}(x_n)':SEC}
    return MathTex(s,font_size=size,color=INK,substrings_to_isolate=list(colors),tex_to_color_map=colors)


class World:
    """Isotropic viewport: real coordinates persist during local pan/zoom."""
    def __init__(self,scene,fn=f,cx=1,cy=0,span=2,size=6.4,center=(0,2.15)):
        self.scene=scene;self.fn=fn;self.size=size;self.center=np.array([*center,0.])
        self.cx=ValueTracker(cx);self.cy=ValueTracker(cy);self.span=ValueTracker(span)
        self.opacity=1
        self.frame=Rectangle(width=size,height=size,stroke_color=MUTED,stroke_opacity=.35,stroke_width=1).move_to(self.center)
        grid=VGroup(*[Line(self.center+np.array([q*size/2,-size/2,0]),self.center+np.array([q*size/2,size/2,0]),stroke_color=MUTED,stroke_opacity=.12,stroke_width=1) for q in (-.5,0,.5)],
                    *[Line(self.center+np.array([-size/2,q*size/2,0]),self.center+np.array([size/2,q*size/2,0]),stroke_color=MUTED,stroke_opacity=.12,stroke_width=1) for q in (-.5,0,.5)])
        def axes():
            a=VGroup();x,y,s=self.values()
            if abs(y)<=s:a.add(Line(self.p(x-s,0),self.p(x+s,0),color=MUTED,stroke_width=2))
            if abs(x)<=s:a.add(Line(self.p(0,y-s),self.p(0,y+s),color=MUTED,stroke_width=2))
            return a
        self.axes=always_redraw(axes)
        self.ticks=VGroup()
        for d in (0,1):
            for q in (-.65,.65):
                m=DecimalNumber(0,num_decimal_places=3,font_size=17,color=MUTED)
                pos=self.center+np.array([q*size/2,-size/2-.22,0]) if d==0 else self.center+np.array([-size/2-.35,q*size/2,0])
                def update(m,d=d,q=q,pos=pos):
                    s=self.span.get_value();m.num_decimal_places=3 if s>.01 else (6 if s>1e-5 else 8)
                    m.set_value((self.cx if d==0 else self.cy).get_value()+q*s).move_to(pos)
                m.add_updater(update);update(m);self.ticks.add(m)
        self.names=VGroup(MathTex('x',font_size=23,color=MUTED).move_to(self.center+[size/2+.2,-size/2,0]),MathTex('y',font_size=23,color=MUTED).move_to(self.center+[-size/2,size/2+.2,0]))
        scene.add(self.frame,grid,self.axes,self.ticks,self.names)
        if fn is not None:
            self.graph=always_redraw(lambda:self.graph_fn(fn,F,opacity=self.opacity))
            scene.add(self.graph)
    def values(self):return self.cx.get_value(),self.cy.get_value(),self.span.get_value()
    def p(self,x,y):
        cx,cy,s=self.values();return self.center+self.size/2/s*np.array([x-cx,y-cy,0.])
    def graph_fn(self,fn,color=F,width=4,opacity=1):
        cx,cy,s=self.values();xs=np.linspace(cx-s,cx+s,251);groups=[];pts=[]
        for x in xs:
            y=fn(float(x))
            if np.isfinite(y) and cy-s<=y<=cy+s:pts.append(self.p(x,y))
            else:
                if len(pts)>1:groups.append(VMobject(fill_opacity=0).set_points_as_corners(pts))
                pts=[]
        if len(pts)>1:groups.append(VMobject(fill_opacity=0).set_points_as_corners(pts))
        return VGroup(*groups).set_stroke(color,width,opacity=opacity)
    def line(self,m,b,color=SEC,width=3,opacity=1):
        cx,cy,s=self.values();lo=cx-s;hi=cx+s
        if abs(m)>1e-14:
            a,bound=sorted(((cy-s-b)/m,(cy+s-b)/m));lo=max(lo,a);hi=min(hi,bound)
        elif not cy-s<=b<=cy+s:hi=lo
        if hi-lo<1e-12:return VMobject()
        return Line(self.p(lo,m*lo+b),self.p(hi,m*hi+b),stroke_color=color,stroke_width=width,stroke_opacity=opacity)
    def zoom(self,cx=None,cy=None,span=None,t=1):
        anim=[]
        for tracker,val in ((self.cx,cx),(self.cy,cy),(self.span,span)):
            if val is not None:anim.append(tracker.animate.set_value(val))
        self.scene.play(*anim,run_time=t)


class NewtonLesson(ui.Lesson):
    EQ_Y=-2.65
    NOTE_Y=-4.15

    def note(self,s,color=MUTED):
        if hasattr(self,"note_mob"):
            self.remove(self.note_mob)
        self.note_mob=fit(text(s,23,color),8).move_to([0,self.NOTE_Y,0]).set_z_index(30)
        self.add(self.note_mob)

    def eq(self,s,duration=.35):
        m=fit(fm(s),7.9).move_to([0,self.EQ_Y,0]).set_z_index(30)
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
    def main(self,x=1.5,**kw):
        self.w=World(self,**kw);self.wx=ValueTracker(x);self.wy=ValueTracker(f(x));self.tangents=[]
        self.point=always_redraw(lambda:Dot(self.w.p(self.wx.get_value(),self.wy.get_value()),color=INK,radius=.075).set_z_index(8))
        def guide():
            cx,cy,span=self.w.values()
            y0=float(np.clip(0,cy-span,cy+span));yv=float(np.clip(self.wy.get_value(),cy-span,cy+span))
            a=self.w.p(self.wx.get_value(),y0);b=self.w.p(self.wx.get_value(),yv)
            return DashedLine(a,b,color=INK,stroke_opacity=.5,dash_length=.09) if np.linalg.norm(a-b)>.01 else VGroup()
        self.guide=always_redraw(guide);self.add(self.guide,self.point)
    def tangent(self,x,animate=True):
        for _,_,style in self.tangents:style.update(color=MUTED,opacity=.25)
        style={'color':SEC,'opacity':1}
        m=always_redraw(lambda:self.w.line(df(x),f(x)-df(x)*x,**style))
        if animate:self.play(Create(m),run_time=.7)
        else:self.add(m)
        self.tangents.append((x,m,style));return m
    def root(self):
        m=always_redraw(lambda:Dot(self.w.p(ROOT,0),color=TAN,radius=.06).set_z_index(9));self.add(m);return m
    def step(self,x,t=1.5):
        nxt=x-f(x)/df(x)
        target=always_redraw(lambda:Dot(self.w.p(nxt,0),color=LIMIT,radius=.065).set_z_index(9));self.add(target)
        self.play(self.wx.animate.set_value(nxt),self.wy.animate.set_value(0),run_time=t*.62,rate_func=linear)
        self.play(self.wy.animate.set_value(f(nxt)),run_time=t*.38,rate_func=linear)
        self.remove(target)
    def value_note(self,n):
        self.note(f'곡선 위의 새 점 · x{n} = {XS[n]:.9f} · 오차 {abs(XS[n]-ROOT):.2e}',LIMIT)


class NW01Intro(NewtonLesson):
    START=0;END=22
    def construct(self):
        self.title('비선형 문제를 선형 문제로');self.w=World(self)
        linear=self.w.line(1,-1,SEC)
        def a():self.eq(r'f(x)=0\quad\longrightarrow\quad ax+b=0');self.play(Create(linear),run_time=1.5);self.note('청록: 곡선  /  주황: 풀기 쉬운 직선')
        def b():self.play(FadeOut(linear),run_time=.5);self.eq(r'f(x)=x^3-x-1')
        def c():
            m=always_redraw(lambda:Dot(self.w.p(ROOT,0),color=TAN,radius=.09));self.play(FadeIn(m),run_time=.5);self.note('곡선과 x축의 교점: f(x) = 0',TAN)
        def d():self.eq(r'x^3-x-1=0\qquad x=?');self.w.zoom(cx=1.4,span=1.1,t=1.3)
        def e():self.w.zoom(cx=1,span=2,t=1);self.play(Create(self.w.line(df(1.5),f(1.5)-df(1.5)*1.5)),run_time=1);self.note('한 점 근처에서는 접선으로 근사',SEC)
        self.run_lines([a,b,c,d,e])


class NW02First(NewtonLesson):
    START=22;END=35
    def construct(self):
        self.title('접선의 교점을 다음 추정값으로');self.main()
        def a():self.eq(r'x_0=1.5,\qquad f(x_0)=0.875');self.note('흰 점: 현재 곡선 위의 점')
        def b():self.tangent(XS[0]);self.eq(r'T_0(x)=0.875+5.75(x-1.5)')
        def c():
            self.w.zoom(cx=1.4,cy=.4,span=.65,t=.9);self.eq(r'T_0(x)=0\quad\Rightarrow\quad x_1=1.347826\ldots');self.note('노란 점: 접선과 x축의 교점',LIMIT)
            self.target=Dot(self.w.p(XS[1],0),color=LIMIT,radius=.085);self.play(FadeIn(self.target),run_time=.5)
        def d():self.remove(self.target);self.step(XS[0],2.5);self.note('접선을 따라 이동 → 같은 x에서 곡선으로 복귀');self.value_note(1)
        self.run_lines([a,b,c,d])


class NW03Iteration(NewtonLesson):
    START=35;END=50
    def construct(self):
        self.title('이동한 곳에서 다시 선형화');self.main(XS[1],cx=1.4,cy=.4,span=.65);self.tangent(XS[0],False)
        def a():self.w.zoom(cx=1.35,cy=0,span=.25,t=1.2);self.tangent(XS[1]);self.eq(r'T_1(x)=f(x_1)+f^{\prime}(x_1)(x-x_1)')
        def b():self.eq(r'T_1(x_2)=0');self.step(XS[1],2);self.value_note(2)
        def c():self.w.zoom(cx=ROOT,span=.012,t=1.2);self.eq(r'T_2(x_3)=0');self.tangent(XS[2]);self.step(XS[2],1.8);self.root();self.value_note(3)
        def d():self.title('뉴턴법 · Newton’s method')
        self.run_lines([a,b,c,d])


class NW04View(NewtonLesson):
    START=50;END=62
    def construct(self):
        self.title('실제로 푼 문제는 일차방정식');self.main();self.w.opacity=.45
        def a():self.eq(r'f(x)=0\quad\longrightarrow\quad T_n(x)=0');self.tangent(XS[0]);self.note('원래 곡선을 한 번에 풀지 않는다')
        def b():
            self.eq(r'T_n(x)=a_nx+b_n=0');self.note('각 단계: 접선의 기울기와 절편으로 교점 계산',SEC)
            for n in range(3):
                self.tangent(XS[n]);dot=Dot(self.w.p(XS[n+1],0),color=LIMIT);self.play(FadeIn(dot),run_time=.35)
            self.eq(r'x_{n+1}=-\frac{b_n}{a_n}')
        def c():self.note('왜 국소적인 직선으로 다음 위치를 정할 수 있을까?',LIMIT)
        self.run_lines([a,b,c])


class NW05Local(NewtonLesson):
    START=62;END=74
    def construct(self):
        self.title('접점 주변을 확대하면');self.main(cx=1.5,cy=.875,span=1.2);self.tangent(1.5,False)
        delta=ValueTracker(.06);a=1.5
        def tri():
            x=a+delta.get_value();pred=f(a)+df(a)*(x-a)
            return VGroup(Line(self.w.p(a,f(a)),self.w.p(x,f(a)),color=LIMIT,stroke_width=4),Line(self.w.p(x,f(a)),self.w.p(x,pred),color=SEC,stroke_width=4),Dot(self.w.p(x,pred),color=SEC,radius=.06),Dot(self.w.p(x,f(x)),color=F,radius=.055),Line(self.w.p(x,pred),self.w.p(x,f(x)),color=RED,stroke_width=6))
        triangle=always_redraw(tri)
        def b():
            self.add(triangle);self.eq(r'f(x_n+\Delta x)\approx f(x_n)+f^{\prime}(x_n)\Delta x');self.note('노랑: 가로 이동  /  주황: 기울기 × 이동',SEC)
            self.play(delta.animate.set_value(.015),self.w.span.animate.set_value(.15),run_time=3)
            self.note('이동을 줄이면 실제 높이와 예측 높이의 차이도 감소',F)
        self.run_lines([lambda:(self.eq(r'T_n(x)=f(x_n)+f^{\prime}(x_n)(x-x_n)'),self.w.zoom(span=.45,t=2)),b])


class NW06Formula(NewtonLesson):
    START=74;END=86
    def construct(self):
        self.title('선형 근사가 0이 되는 이동량');self.main();self.tangent(1.5,False)
        def a():
            self.eq(r'0=f(x_n)+f^{\prime}(x_n)\Delta x');self.note('예측한 함수값을 0으로 놓는다',LIMIT)
            self.eq(r'\Delta x=-\frac{f(x_n)}{f^{\prime}(x_n)}',.7)
            arrow=Arrow(self.w.p(XS[0],-.25),self.w.p(XS[1],-.25),buff=0,color=LIMIT,max_tip_length_to_length_ratio=.25);self.play(GrowArrow(arrow),run_time=.8)
        def b():
            self.eq(r'\boxed{x_{n+1}=x_n-\frac{f(x_n)}{f^{\prime}(x_n)}}');self.step(1.5,2.5);self.note('함수값: 청록  ·  기울기: 주황  ·  새 추정값: 노랑')
        self.run_lines([a,b])


class NW07Renew(NewtonLesson):
    START=86;END=94
    def construct(self):
        self.title('새로운 위치에서는 새 근사를');self.main();self.tangent(1.5,False)
        q=ValueTracker(1.1)
        gap=always_redraw(lambda:Line(self.w.p(q.get_value(),f(q.get_value())),self.w.p(q.get_value(),f(1.5)+df(1.5)*(q.get_value()-1.5)),color=RED,stroke_width=5))
        def a():self.eq(r'f(x)\ne T_n(x)\ \text{in general}');self.add(gap);self.note('빨간 간격: 실제 곡선과 접선의 차이',RED);self.play(q.animate.set_value(1.47),run_time=1.2)
        def b():
            self.remove(gap);self.wx.set_value(XS[1]);self.wy.set_value(f(XS[1]));self.w.zoom(cx=1.35,span=.25,t=.8);self.tangent(XS[1]);self.eq(r'T_{n+1}(x)=f(x_{n+1})+f^{\prime}(x_{n+1})(x-x_{n+1})');self.step(XS[1],1.5);self.note('이동할 때마다 함수값과 기울기를 다시 계산',SEC)
        self.run_lines([a,b])


class NW08Convergence(NewtonLesson):
    EQ_Y=-3.05
    START=94;END=108
    def construct(self):
        self.title('해 근처에서는 오차가 빠르게 감소');self.w=World(self,cx=ROOT,span=.4,size=4.2,center=(0,3.4));self.root()
        x=ValueTracker(XS[0]);dot=always_redraw(lambda:Dot(self.w.p(x.get_value(),0),color=LIMIT,radius=.065));self.add(dot)
        err=always_redraw(lambda:Line(self.w.p(ROOT,0),self.w.p(x.get_value(),0),color=LIMIT,stroke_width=5));self.add(err)
        table=VGroup()
        header=fit(text('반복       추정값 xₙ          절대오차',21),7.5).move_to([0,.55,0]);self.add(header)
        for n in range(4):
            row=VGroup(MathTex(str(n),font_size=25,color=MUTED),MathTex(f'{XS[n]:.9f}',font_size=25,color=LIMIT),MathTex(f'{abs(XS[n]-ROOT):.2e}'.replace('e-',r'\times10^{-')+'}' if 'e-' in f'{abs(XS[n]-ROOT):.2e}' else '',font_size=25,color=TAN)).arrange(RIGHT,buff=.6).move_to([0,-.05-n*.57,0]);table.add(row)
        self.add(table[0])
        def a():self.eq(r'e_n=x_n-\alpha');self.note('보라: 실제 해 α  /  노랑: 추정값',TAN)
        def b():
            self.eq(r'|e_{n+1}|\approx C|e_n|^2');self.note('단순근 · 충분히 매끄러움 · 가까운 시작점',SEC)
            for n,span in ((1,.4),(2,.06),(3,.002)):
                self.w.zoom(span=span,t=.45);self.play(x.animate.set_value(XS[n]),FadeIn(table[n]),run_time=.8)
        def c():self.w.zoom(span=1e-6,t=1.2);self.note('3회 갱신: 절대오차 약 0.000000217',LIMIT)
        self.run_lines([a,b,c])


class NW09Failure(NewtonLesson):
    START=108;END=114
    def construct(self):
        self.title('항상 수렴하는 것은 아니다');h=lambda x:x**3-2*x+2;dh=lambda x:3*x*x-2
        self.w=World(self,fn=h,cx=.5,cy=1,span=1.7);x=ValueTracker(0);y=ValueTracker(2)
        self.add(always_redraw(lambda:Dot(self.w.p(x.get_value(),y.get_value()),color=INK,radius=.075)))
        def a():
            self.eq(r'g(x)=x^3-2x+2,\quad 0\to1\to0');self.note('좋지 않은 초기값은 두 점 사이를 순환시킬 수도 있다',LIMIT)
            for at,nxt in ((0,1),(1,0)):
                line=self.w.line(dh(at),h(at)-dh(at)*at);self.play(Create(line),run_time=.45)
                self.play(x.animate.set_value(nxt),y.animate.set_value(0),run_time=.6,rate_func=linear)
                self.play(y.animate.set_value(h(nxt)),run_time=.4,rate_func=linear)
                self.play(line.animate.set_stroke(opacity=.2),run_time=.2)
        self.run_lines([a])


class NW10System(NewtonLesson):
    START=114;END=135
    def construct(self):
        self.title('여러 변수도 선형 문제로 바꾼다');self.w=World(self,fn=None,cx=0,cy=0,span=2)
        circle=Circle(radius=np.sqrt(2)*self.w.size/4,color=F,stroke_width=4).move_to(self.w.p(0,0));line=self.w.line(1,0,G)
        z=np.array([1.5,1.]);tracker=[ValueTracker(float(q)) for q in z]
        dot=always_redraw(lambda:Dot(self.w.p(*[t.get_value() for t in tracker]),color=INK,radius=.075));self.add(dot)
        current=[z.copy()];linear=[None]
        def a():self.eq(r'F_1=x^2+y^2-2=0,\quad F_2=x-y=0');self.play(Create(circle),Create(line),run_time=1.5);self.note('원과 직선의 교점 중 (1,1)을 찾는 예시')
        def b():self.play(FadeIn(Dot(self.w.p(1,1),color=TAN,radius=.065)),run_time=.5);self.note('현재 추정점: (1.5, 1.0)')
        def c():self.eq(r'J_F(x,y)=\begin{pmatrix}2x&2y\\1&-1\end{pmatrix}');self.note('야코비안: 각 함수의 변수별 변화율',SEC)
        def update(t):
            at=current[0];J=np.array([[2*at[0],2*at[1]],[1.,-1.]])
            residual=np.array([at@at-2,at[0]-at[1]])
            nxt=at+np.linalg.solve(J,-residual)
            boundary=self.w.line(-at[0]/at[1],(at@at+2)/(2*at[1]),SEC)
            if linear[0] is not None:self.remove(linear[0])
            linear[0]=boundary;self.play(Create(boundary),run_time=.55)
            target=Dot(self.w.p(*nxt),color=LIMIT,radius=.075);self.play(FadeIn(target),run_time=.25)
            self.play(*[tracker[i].animate.set_value(nxt[i]) for i in range(2)],run_time=t)
            self.remove(target);current[0]=nxt
        def d():self.eq(r'J_F\Delta\mathbf{x}=-F(\mathbf{x}_n)');self.note('주황: 영점 조건의 선형화선 (원 자체의 접선 아님)',SEC);update(1.4)
        def e():self.eq(r'\mathbf{x}_{n+1}=\mathbf{x}_n+\Delta\mathbf{x}');update(.8);update(.8);self.note('선형 연립방정식을 풀고, 새 위치에서 다시 계산',LIMIT)
        self.run_lines([a,b,c,d,e])


class NW11Optimization(NewtonLesson):
    START=135;END=145
    def construct(self):
        self.title('최적화: 기울기를 0으로');h=lambda x:x**4/4+x*x/2;hp=lambda x:x**3+x;hpp=lambda x:3*x*x+1
        a=1.2;nxt=a-hp(a)/hpp(a);q=lambda x:h(a)+hp(a)*(x-a)+hpp(a)/2*(x-a)**2
        self.w=World(self,fn=h,cx=.5,cy=.8,span=1.5)
        x=ValueTracker(a);y=ValueTracker(h(a));self.add(always_redraw(lambda:Dot(self.w.p(x.get_value(),y.get_value()),color=INK,radius=.07)))
        def a1():
            self.eq(r'h(x)=\tfrac14x^4+\tfrac12x^2,\quad h^{\prime}(x)=0');self.note('함수값이 아닌, 기울기를 0으로 만든다',F)
            self.play(FadeIn(Dot(self.w.p(0,0),color=TAN,radius=.075)),run_time=.5)
        # Follow q(x) while moving horizontally to its actual minimizer.
        point=self.mobjects[-1];self.remove(point)
        self.moving=always_redraw(lambda:Dot(self.w.p(x.get_value(),y.get_value()),color=INK,radius=.07));self.add(self.moving)
        def move_quadratic():
            y.add_updater(lambda m:m.set_value(q(x.get_value())))
            self.play(x.animate.set_value(nxt),run_time=1.3);y.clear_updaters()
        def b2():
            self.eq(r'h(x_n+\Delta x)\approx h(x_n)+h^{\prime}(x_n)\Delta x+\tfrac12h^{\prime\prime}(x_n)(\Delta x)^2')
            self.play(Create(self.w.graph_fn(q,SEC)),run_time=1)
            self.play(FadeIn(Dot(self.w.p(nxt,q(nxt)),color=LIMIT,radius=.07)),run_time=.3)
            self.note('청록: 원래 함수  /  주황: 국소 이차 근사',SEC)
            self.eq(r'\Delta x=-\frac{h^{\prime}(x_n)}{h^{\prime\prime}(x_n)}');self.add(y);move_quadratic();self.remove(y)
            self.play(y.animate.set_value(h(nxt)),run_time=.6);self.note('양의 곡률: 근사 포물선의 최소점으로 이동',LIMIT)
        self.run_lines([a1,b2])


class NW12Conclusion(NewtonLesson):
    START=145;END=156
    def construct(self):
        self.title('쉬운 문제를 만들고, 다시 푼다');self.main();self.root()
        def a():self.eq(r'f(x)=0\quad\longrightarrow\quad T_n(x)=0');self.tangent(XS[0]);self.step(XS[0],1.6)
        def b():
            self.w.zoom(cx=1.35,span=.25,t=.8);self.tangent(XS[1]);self.step(XS[1],1.4)
            self.w.zoom(cx=ROOT,span=.012,t=.7);self.tangent(XS[2]);self.step(XS[2],1.2)
            self.eq(r'\boxed{x_{n+1}=x_n-\frac{f(x_n)}{f^{\prime}(x_n)}}');self.note('국소 선형화 → 쉬운 해 → 새 위치에서 다시 선형화',LIMIT)
        self.run_lines([a,b])
