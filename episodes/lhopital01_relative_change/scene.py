"""Narration-timed portrait animations for L'Hopital's rule; independent scenes."""
import json
import math
import os
from pathlib import Path

import numpy as np
from manim import *

HERE=Path(__file__).parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.frame_width=9
config.frame_height=16
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1080'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1920'))
config.frame_rate=int(os.environ.get('VIDEO_FPS','30'))
config.background_color='#0B1020'
BG='#0B1020'; INK='#EFF5FB'; MUTED='#8190A5'
F='#47D7C4'; G='#729DFF'; SEC='#FFB454'; TAN='#C5A3FF'; LIMIT='#F8DC79'
FONT='Malgun Gothic'
FUNCTION_COLORS={r'\sin x':F,r'\cos x':F,'f(x)':F,'g(x)':G,
                 'f(t)':F,'g(t)':G,"f'(x)":F,"g'(x)":G,"f'(c)":F,"g'(c)":G}
FUNCTION_COLORS.update({rf'f^{{\prime}}({a})':F for a in ('x','0','c')})
FUNCTION_COLORS.update({rf'g^{{\prime}}({a})':G for a in ('x','0','c')})


def text(s,size=27,color=INK):
    return Text(s,font=FONT,font_size=size,color=color)


def formula(s,size=36):
    return MathTex(s,font_size=size,color=INK,
                   substrings_to_isolate=list(FUNCTION_COLORS),tex_to_color_map=FUNCTION_COLORS)


def fit(m,width=8):
    if m.width>width:
        m.scale_to_fit_width(width)
    return m


def wrap(s,limit=25):
    lines=[]; line=''
    for word in s.split():
        candidate=(line+' '+word).strip()
        if len(candidate)>limit and line:
            lines.append(line);line=word
        else:
            line=candidate
    return '\n'.join(lines+[line])


def curve(ax,fn,color=F,lo=-2,hi=2,scale=1,width=4):
    pts=[ax.c2p(u,fn(scale*u)/scale) for u in np.linspace(lo,hi,101)]
    return VMobject(stroke_color=color,stroke_width=width,fill_opacity=0).set_points_smoothly(pts)


class Lesson(Scene):
    START=0; END=0

    def play(self,*animations,**kwargs):
        if 'run_time' in kwargs:
            kwargs['run_time']=max(1,round(kwargs['run_time']*config.frame_rate))/config.frame_rate
        return super().play(*animations,**kwargs)

    def wait(self,duration=1,**kwargs):
        frames=round(duration*config.frame_rate)
        if frames>0:
            return super().wait(frames/config.frame_rate,**kwargs)

    def title(self,s):
        if hasattr(self,'heading'):
            self.remove(self.heading)
        self.heading=fit(text(s,30),8.1).move_to([0,7.05,0]).set_z_index(30)
        self.add(self.heading)

    def eq(self,s,duration=.4):
        m=fit(formula(s),8).move_to([0,5.6,0]).set_z_index(30)
        if hasattr(self,'equation'):
            old=self.equation
            self.play(TransformMatchingTex(old,m),run_time=duration)
            self.remove(old)
        else:
            self.play(Write(m),run_time=duration)
        self.equation=m
        self.add(m)
        return m

    def note(self,s,color=MUTED):
        if hasattr(self,'note_mob'):
            self.remove(self.note_mob)
        self.note_mob=fit(text(s,23,color),8).move_to([0,4.35,0]).set_z_index(30)
        self.add(self.note_mob)

    def caption(self,s):
        if hasattr(self,'caption_mob'):
            self.remove(self.caption_mob)
        m=fit(text(wrap(s),27),7.9).move_to([0,-6.55,0])
        bg=RoundedRectangle(width=8.45,height=m.height+.25,corner_radius=.12,
                            fill_color=BG,fill_opacity=.96,stroke_width=0).move_to(m)
        self.caption_mob=VGroup(bg,m).set_z_index(50)
        self.add(self.caption_mob)

    def hud(self,items,rows=1):
        if hasattr(self,'hud_mob'):
            self.hud_mob.clear_updaters(recursive=True)
            self.remove(self.hud_mob)
        cells=VGroup()
        for label,color,fn in items:
            lhs=MathTex(label,font_size=29,color=color)
            value=DecimalNumber(float(fn()),num_decimal_places=3,font_size=29,color=color)
            cell=VGroup(lhs,value).arrange(RIGHT,buff=.1)
            value.add_updater(lambda mob,fn=fn:mob.set_value(float(fn())))
            cells.add(cell)
        cells.arrange_in_grid(rows=rows,buff=(.45,.25))
        fit(cells,7.9).move_to([0,-4.75,0]).set_z_index(30)
        self.hud_mob=cells
        self.add(cells)

    def hide_hud(self):
        if hasattr(self,'hud_mob'):
            self.hud_mob.clear_updaters(recursive=True)
            self.remove(self.hud_mob)

    def run_lines(self,actions):
        rows=[(end,line) for end,line in DATA['sentences'] if self.START<end<=self.END]
        if len(rows)!=len(actions):
            raise RuntimeError(f'{type(self).__name__}: sentence count mismatch')
        for (end,line),action in zip(rows,actions):
            self.caption(line)
            action()
            target=end-self.START
            if self.time>target+.02:
                raise RuntimeError(f'{type(self).__name__}: {self.time} exceeds {target}')
            self.wait(target-self.time)

    def axes(self,mode='symmetric',center=(0,.1),length=6.8):
        if mode=='positive':
            xr=[0,1.1,.25];yr=[0,1.1,.25];xl=length;yl=length
        elif mode=='mean':
            xr=[0,2.1,.5];yr=[0,4.3,1];xl=6.5;yl=6.3
        else:
            xr=[-2,2,1];yr=[-2,2,1];xl=length;yl=length
        ax=Axes(x_range=xr,y_range=yr,x_length=xl,y_length=yl,tips=False,
                axis_config={'color':MUTED,'stroke_width':1.7,'include_ticks':True,
                             'tick_size':.04})
        ax.move_to([center[0],center[1],0])
        return ax

    def axis_names(self,ax,x='x',y='y'):
        labels=VGroup(MathTex(x,font_size=25,color=MUTED).next_to(ax.x_axis.get_end(),RIGHT,buff=.13),
                      MathTex(y,font_size=25,color=MUTED).next_to(ax.y_axis.get_end(),UP,buff=.13))
        self.add(labels)
        return labels

    def ticks(self,ax,scale=None):
        labels=VGroup()
        for direction in (0,1):
            for q in (-1,1):
                value=DecimalNumber(q,num_decimal_places=2,font_size=18,color=MUTED)
                pos=ax.c2p(q,0)+DOWN*.23 if direction==0 else ax.c2p(0,q)+LEFT*.35
                value.move_to(pos)
                if scale is not None:
                    value.add_updater(lambda m,q=q:m.set_value(q*scale.get_value()))
                labels.add(value)
        self.add(labels)
        return labels

    def pair(self,ax,t,f,g,scale=None):
        def draw():
            s=scale.get_value() if scale is not None else 1
            u=t.get_value();base=ax.c2p(u/s,0)
            pf=ax.c2p(u/s,f(u)/s);pg=ax.c2p(u/s,g(u)/s)
            return VGroup(Line(base,pg,color=G,stroke_width=5),
                          Line(base,pf,color=F,stroke_width=2.6),
                          Dot(pg,color=G,radius=.085),Dot(pf,color=F,radius=.055))
        m=always_redraw(draw)
        self.add(m)
        return m

    def sine_plot(self,draw=False):
        self.ax=self.axes()
        self.add(self.ax)
        self.names=self.axis_names(self.ax)
        self.ticks(self.ax)
        self.sin_graph=curve(self.ax,math.sin,F)
        self.x_graph=DashedVMobject(curve(self.ax,lambda x:x,G,width=5),num_dashes=38,dashed_ratio=.65)
        if draw:
            self.play(Create(self.x_graph),Create(self.sin_graph),run_time=1.5)
        else:
            self.add(self.x_graph,self.sin_graph)

    def power_plot(self,draw=False):
        self.ax=self.axes('positive',center=(0,.1),length=6.2)
        self.add(self.ax);self.names=self.axis_names(self.ax)
        self.f_graph=curve(self.ax,lambda x:x**3,F,0,1.02)
        self.g_graph=curve(self.ax,lambda x:x*x,G,0,1.02)
        if draw:
            self.play(Create(self.g_graph),Create(self.f_graph),run_time=1.4)
        else:
            self.add(self.g_graph,self.f_graph)


class LH01Intro(Lesson):
    START=0;END=16
    def construct(self):
        self.title('로피탈: 왜 따로 미분할까?')
        self.run_lines([self.intro,self.forms,self.differentiate])

    def intro(self):
        self.eq(r'\lim_{x\to a}\frac{f(x)}{g(x)}',1.6)
        self.name=text("L’Hôpital’s Rule",28,MUTED).move_to([0,2.8,0])
        self.play(FadeIn(self.name),run_time=.8)

    def forms(self):
        self.forms_mob=VGroup(formula(r'\frac00\;?'),formula(r'\frac{\infty}{\infty}\;?'))
        self.forms_mob.arrange(RIGHT,buff=1.7).move_to([0,.4,0])
        self.play(LaggedStart(*[Write(m) for m in self.forms_mob],lag_ratio=.6),run_time=2.8)
        self.note('부정형: 대입만으로 비율을 정할 수 없음',LIMIT)

    def differentiate(self):
        self.eq(r'\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f^{\prime}(x)}{g^{\prime}(x)}',1.8)
        self.note('근방에서 미분 가능 · g′ ≠ 0\n도함수 비율의 극한 존재 등 적용 조건 필요',MUTED)
        self.play(FadeOut(self.forms_mob),FadeOut(self.name),run_time=.5)
        chain=VGroup(formula(r'f(x)\longrightarrow f^{\prime}(x)').set_color(F),
                     formula(r'g(x)\longrightarrow g^{\prime}(x)').set_color(G)).arrange(DOWN,buff=.8)
        chain.move_to([0,.4,0]);self.play(LaggedStart(*[Write(m) for m in chain],lag_ratio=.6),run_time=2)


class LH02Sine(Lesson):
    START=16;END=31
    def construct(self):
        self.title('첫 예시: sin x / x')
        self.t=ValueTracker(1.5)
        self.run_lines([self.graphs,self.approach,self.result])

    def graphs(self):
        self.eq(r'\lim_{x\to0}\frac{\sin x}{x}')
        self.note('청록: f(x) = sin x   /   파랑: g(x) = x',MUTED)
        self.sine_plot(draw=True)
        self.pair(self.ax,self.t,math.sin,lambda x:x)

    def approach(self):
        self.hud([('t=',INK,lambda:self.t.get_value()),
                  ('f(t)=',F,lambda:math.sin(self.t.get_value())),
                  ('g(t)=',G,lambda:self.t.get_value()),
                  ('f/g=',LIMIT,lambda:math.sin(self.t.get_value())/self.t.get_value())],rows=2)
        self.play(self.t.animate.set_value(.12),run_time=3.5,rate_func=linear)

    def result(self):
        self.eq(r'\lim_{x\to0}\frac{\sin x}{x}=\lim_{x\to0}\frac{\cos x}{1}',1.8)
        self.note('분자 sin x → cos x    /    분모 x → 1',MUTED)
        self.play(self.t.animate.set_value(.025),run_time=1.8)
        self.eq(r'\lim_{x\to0}\frac{\sin x}{x}=1',1)


class LH03Question(Lesson):
    START=31;END=38
    def construct(self):
        self.title('그런데 왜 같은 답이 나올까?')
        self.sine_plot()
        self.run_lines([self.ask,self.shift])

    def ask(self):
        self.eq(r'\frac{\sin x}{x}\;\xrightarrow{\;?\;}\;\frac{\cos x}{1}',1.8)
        self.note('값의 비율과 변화율의 비율은 어떻게 연결될까?',LIMIT)

    def shift(self):
        self.play(self.sin_graph.animate.set_stroke(opacity=.25),self.x_graph.animate.set_stroke(opacity=.25),run_time=1)
        self.note('먼저 0/0이 무엇을 알려 주는지 살펴보자',MUTED)


class LH04Rates(Lesson):
    START=38;END=58
    def construct(self):
        self.title('같은 0/0, 다른 접근 속도')
        self.t=ValueTracker(1.)
        self.run_lines([self.cases,self.move,self.difference,self.replay])

    def cases(self):
        self.eq(r'\frac{x}{x}=1\qquad\frac{x^2}{x}=x')
        self.note('같이 0으로 가도 비율은 다를 수 있다',LIMIT)
        self.panels=VGroup()
        for center,power,tag in [(1.9,1,'A: f(x)=x, g(x)=x'),(-2.05,2,'B: f(x)=x², g(x)=x')]:
            ax=Axes(x_range=[0,1.1,.5],y_range=[0,1.1,.5],x_length=5.8,y_length=2.65,
                    tips=False,axis_config={'color':MUTED,'stroke_width':1.4})
            ax.move_to([0,center,0])
            label=text(tag,22).move_to([0,center+1.65,0])
            blue=DashedVMobject(curve(ax,lambda x:x,G,0,1,width=5),num_dashes=25)
            green=curve(ax,lambda x,p=power:x**p,F,0,1,width=3)
            self.add(ax,label);self.play(Create(blue),Create(green),run_time=.7)
            self.pair(ax,self.t,lambda x,p=power:x**p,lambda x:x)
            self.panels.add(ax,label,blue,green)

    def move(self):
        self.hud([('t=',INK,lambda:self.t.get_value()),('A=',LIMIT,lambda:1),
                  ('B=',LIMIT,lambda:self.t.get_value())])
        self.play(self.t.animate.set_value(.1),run_time=4.2,rate_func=linear)

    def difference(self):
        self.eq(r'\frac{x}{x}\to1\qquad\frac{x^2}{x}\to0')
        self.play(self.t.animate.set_value(.035),run_time=2.6,rate_func=linear)

    def replay(self):
        self.note('A: 높이가 같음   /   B: x²의 높이가 더 빨리 감소',MUTED)
        self.play(self.t.animate.set_value(.8),run_time=1.2)
        self.play(self.t.animate.set_value(.04),run_time=3.9,rate_func=linear)


class LH05Zoom(Lesson):
    START=58;END=85
    def construct(self):
        self.title('원점 근처를 확대하면')
        self.scale=ValueTracker(1.)
        self.t=ValueTracker(.2)
        self.run_lines([self.draw,self.zoom,self.approximate,self.cancel,self.slope])

    def draw(self):
        self.eq(r'f(x)=\sin x,\qquad g(x)=x')
        self.note('같은 배율로 x와 y를 확대한다',MUTED)
        self.ax=self.axes();self.add(self.ax);self.axis_names(self.ax)
        self.ticks(self.ax,self.scale)
        self.fg=always_redraw(lambda:curve(self.ax,math.sin,F,scale=self.scale.get_value()))
        self.gg=always_redraw(lambda:DashedVMobject(curve(self.ax,lambda x:x,G,scale=self.scale.get_value(),width=5),num_dashes=36))
        self.play(FadeIn(self.gg),FadeIn(self.fg),run_time=1.2)

    def zoom(self):
        self.hud([('s=',MUTED,lambda:self.scale.get_value())])
        self.play(self.scale.animate.set_value(.14),run_time=4.3,rate_func=smooth)
        self.note('축의 숫자는 작아지고 곡선은 접선에 가까워진다',MUTED)

    def approximate(self):
        self.note('f(0)=g(0)=0,  g′(0)=1 ≠ 0인 예시',MUTED)
        self.tangent=DashedLine(self.ax.c2p(-1.9,-1.9),self.ax.c2p(1.9,1.9),
                                color=TAN,stroke_width=2.5,dash_length=.12)
        self.play(Create(self.tangent),run_time=1)
        self.pair(self.ax,self.t,math.sin,lambda x:x,self.scale)
        self.eq(r'f(t)\approx f^{\prime}(0)t,\quad g(t)\approx g^{\prime}(0)t',1.3)
        self.hud([('t=',INK,lambda:self.t.get_value()),('f/g=',LIMIT,
                  lambda:math.sin(self.t.get_value())/self.t.get_value())])
        self.play(self.t.animate.set_value(.055),run_time=4.8,rate_func=linear)

    def cancel(self):
        self.eq(r'\frac{f(t)}{g(t)}\approx\frac{f^{\prime}(0)t}{g^{\prime}(0)t}=\frac{f^{\prime}(0)}{g^{\prime}(0)}',1.8)
        self.note('같은 t가 약분되고 기울기의 비율이 남는다',TAN)
        self.play(self.t.animate.set_value(.025),run_time=1.3)

    def slope(self):
        self.eq(r'\frac{f(t)}{g(t)}\longrightarrow\frac{f^{\prime}(0)}{g^{\prime}(0)}=1',1)
        self.note('이 일차 근사는 g′(0) ≠ 0일 때의 직관',TAN)
        self.play(self.t.animate.set_value(.008),run_time=2.8)


class LH06Mean(Lesson):
    START=85;END=99
    def construct(self):
        self.title('평균값 정리: 할선과 평행한 접선')
        self.c=ValueTracker(.22)
        self.run_lines([self.setup_graph,self.match])

    def setup_graph(self):
        self.eq(r'h(x)=x^2')
        self.note('두 끝점의 평균 변화율과 내부의 순간 변화율',MUTED)
        self.ax=self.axes('mean');self.add(self.ax);self.axis_names(self.ax)
        self.graph=curve(self.ax,lambda x:x*x,F,0,2)
        self.play(Create(self.graph),run_time=1.6)
        self.add(Dot(self.ax.c2p(0,0),color=INK),Dot(self.ax.c2p(2,4),color=INK))
        self.secant=Line(self.ax.c2p(0,0),self.ax.c2p(2,4),color=SEC,stroke_width=4)
        self.play(Create(self.secant),run_time=1.2)

    def match(self):
        self.eq(r'\frac{h(2)-h(0)}{2-0}=2=h^{\prime}(1)',1.1)
        def tangent():
            c=self.c.get_value();lo=max(0,c-.38);hi=min(2,c+.38)
            return VGroup(Line(self.ax.c2p(lo,c*c+2*c*(lo-c)),self.ax.c2p(hi,c*c+2*c*(hi-c)),
                               color=TAN,stroke_width=5),Dot(self.ax.c2p(c,c*c),color=TAN,radius=.08))
        self.tan=always_redraw(tangent);self.add(self.tan)
        self.hud([('c=',INK,lambda:self.c.get_value()),('m_{sec}=',SEC,lambda:2),
                  (r'h^{\prime}(c)=',TAN,lambda:2*self.c.get_value())],rows=2)
        self.play(self.c.animate.set_value(1),run_time=4.8,rate_func=linear)
        self.note('c = 1에서 할선과 접선이 평행하다',TAN)


class LH07Cauchy(Lesson):
    START=99;END=118
    def construct(self):
        self.title('코시: 같은 내부 지점 c를 찾는다')
        self.t=ValueTracker(2.)
        self.ax=self.axes('mean');self.add(self.ax)
        self.labels=self.axis_names(self.ax)
        self.add(curve(self.ax,lambda x:x*x,F,0,2))
        self.run_lines([self.relabel,self.shrink,self.ground])

    def relabel(self):
        self.eq(r'P(u)=(g(u),f(u))=(u,u^2)',.7)
        self.note('가로축 g(u), 세로축 f(u)에서 보는 하나의 곡선',MUTED)
        new=VGroup(MathTex('g(u)',font_size=24,color=G).move_to(self.labels[0]),
                   MathTex('f(u)',font_size=24,color=F).move_to(self.labels[1]))
        fit(new[0],1.05)
        self.play(TransformMatchingTex(self.labels[0],new[0]),
                  TransformMatchingTex(self.labels[1],new[1]),run_time=1)
        def lines():
            t=self.t.get_value();c=t/2
            sec=Line(self.ax.c2p(0,0),self.ax.c2p(t,t*t),color=SEC,stroke_width=4)
            span=min(.32,t*.4)
            tan=Line(self.ax.c2p(c-span,c*c+2*c*(-span)),self.ax.c2p(c+span,c*c+2*c*span),
                     color=TAN,stroke_width=4)
            return VGroup(sec,tan,Dot(self.ax.c2p(t,t*t),color=INK,radius=.08),
                          Dot(self.ax.c2p(c,c*c),color=TAN,radius=.07))
        self.lines=always_redraw(lines);self.add(self.lines)
        self.hud([('t=',INK,lambda:self.t.get_value()),('c=',TAN,lambda:self.t.get_value()/2),
                  (r'\Delta f/\Delta g=',SEC,lambda:self.t.get_value()),
                  (r'f^{\prime}(c)/g^{\prime}(c)=',TAN,lambda:self.t.get_value())],rows=2)
        self.eq(r'\frac{f(t)-f(0)}{g(t)-g(0)}=\frac{f^{\prime}(c)}{g^{\prime}(c)}',1.2)

    def shrink(self):
        self.note('이 예시에서는 c=t/2, 항상 0<c<t',TAN)
        self.play(self.t.animate.set_value(.25),run_time=5.3,rate_func=linear)

    def ground(self):
        self.eq(r'\frac{f(t)}{g(t)}=\frac{f^{\prime}(c)}{g^{\prime}(c)},\quad 0<c<t',1.1)
        self.note('두 도함수는 같은 c에서 평가한다\n0/0, t→0⁺를 설명하는 예시',TAN)
        self.play(self.t.animate.set_value(.045),run_time=3.3,rate_func=linear)


class LH08Flat(Lesson):
    START=118;END=131
    def construct(self):
        self.title('두 접선이 모두 수평이라면?')
        self.run_lines([self.question,self.draw,self.flat,self.restore])

    def question(self):
        self.eq(r'f^{\prime}(0)=g^{\prime}(0)=0')
        self.note('같은 접선이 같은 접근 속도를 뜻할까?',LIMIT)

    def draw(self):
        self.power_plot(draw=True)
        self.eq(r'f(x)=x^3,\qquad g(x)=x^2',.8)

    def flat(self):
        self.tangent=Line(self.ax.c2p(0,0),self.ax.c2p(1.02,0),color=TAN,stroke_width=5)
        self.play(Create(self.tangent),self.f_graph.animate.set_stroke(opacity=.25),
                  self.g_graph.animate.set_stroke(opacity=.25),run_time=1.6)
        self.note('두 함수의 원점 접선은 모두 y=0',TAN)

    def restore(self):
        self.play(self.f_graph.animate.set_stroke(opacity=1),self.g_graph.animate.set_stroke(opacity=1),run_time=1)
        self.note('하지만 곡선의 높이는 다르게 줄어든다',LIMIT)


class LH09Order(Lesson):
    START=131;END=148
    def construct(self):
        self.title('x³은 x²보다 더 빠르게 0으로')
        self.power_plot()
        self.t=ValueTracker(.85)
        self.run_lines([self.compare,self.horizontal,self.orders])

    def compare(self):
        self.eq(r'\frac{f(t)}{g(t)}=\frac{t^3}{t^2}=t\to0',.7)
        self.note('청록 분자 x³   /   파랑 분모 x²',MUTED)
        self.moving=self.pair(self.ax,self.t,lambda x:x**3,lambda x:x*x)
        self.hud([('t^3=',F,lambda:self.t.get_value()**3),('t^2=',G,lambda:self.t.get_value()**2),
                  ('f/g=',LIMIT,lambda:self.t.get_value())])
        self.play(self.t.animate.set_value(.08),run_time=4.8,rate_func=linear)

    def horizontal(self):
        self.tangent=Line(self.ax.c2p(0,0),self.ax.c2p(1.02,0),color=TAN,stroke_width=5)
        self.play(Create(self.tangent),run_time=.8)
        self.note('1차 변화율 0만으로는 구별할 수 없다',TAN)

    def orders(self):
        self.hide_hud();self.moving.clear_updaters();self.remove(self.moving)
        self.play(FadeOut(self.ax),FadeOut(self.names),FadeOut(self.f_graph),
                  FadeOut(self.g_graph),FadeOut(self.tangent),run_time=.5)
        self.title('처음으로 0이 아닌 도함수는?')
        self.eq(r'\begin{gathered}x^2\to2x\to2\\x^3\to3x^2\to6x\to6\end{gathered}',.8)
        self.note('아래 값은 모두 x=0에서 평가한다',MUTED)
        headings=VGroup(*[text(s,24,MUTED) for s in ['차수','0차','1차','2차','3차']])
        headings.arrange(RIGHT,buff=.53).move_to([0,2.5,0]);self.add(headings)
        rows=VGroup()
        for y,label,color,values in [(1.1,'g=x²',G,[0,0,2,0]),(-.4,'f=x³',F,[0,0,0,6])]:
            tag=text(label,25,color).move_to([headings[0].get_x(),y,0]);self.add(tag)
            nums=VGroup(*[MathTex(str(v),font_size=40,color=color).move_to([headings[j+1].get_x(),y,0])
                          for j,v in enumerate(values)])
            rows.add(nums)
        self.play(LaggedStart(*[Write(VGroup(rows[0][j],rows[1][j])) for j in range(4)],lag_ratio=.8),run_time=3)
        boxes=VGroup(SurroundingRectangle(rows[0][2],color=LIMIT,buff=.17),
                     SurroundingRectangle(rows[1][3],color=LIMIT,buff=.17))
        self.play(Create(boxes),run_time=.7)
        note=text('x²: 2차에서 2     x³: 3차에서 6',26,LIMIT).move_to([0,-2.2,0])
        self.play(FadeIn(note),run_time=.4)


class LH10Taylor(Lesson):
    START=148;END=158
    def construct(self):
        self.title('테일러: 낮은 차수의 항이 남는다')
        self.s=ValueTracker(1.)
        self.run_lines([self.setup_graph,self.dominant])

    def setup_graph(self):
        self.eq(r'\sin x=x-\frac{x^3}{6}+\frac{x^5}{120}-\cdots',.7)
        self.note('sin x와 실제 테일러 다항식의 비교',MUTED)
        self.ax=self.axes();self.add(self.ax);self.axis_names(self.ax);self.ticks(self.ax,self.s)
        self.actual=always_redraw(lambda:curve(self.ax,math.sin,F,scale=self.s.get_value(),width=5))
        self.first=always_redraw(lambda:DashedVMobject(curve(self.ax,lambda x:x,G,scale=self.s.get_value()),num_dashes=32))
        self.add(self.actual);self.play(Create(self.first),run_time=1.1)

    def dominant(self):
        self.third=always_redraw(lambda:curve(self.ax,lambda x:x-x**3/6,SEC,scale=self.s.get_value(),width=2.5))
        self.fifth=always_redraw(lambda:curve(self.ax,lambda x:x-x**3/6+x**5/120,TAN,scale=self.s.get_value(),width=2))
        self.play(FadeIn(self.third),run_time=.55);self.play(FadeIn(self.fifth),run_time=.55)
        self.note('파랑 T₁ · 주황 T₃ · 보라 T₅\n원점 근처에서 고차 항의 상대적 영향 감소',MUTED)
        self.eq(r'\frac{\sin x}{x}=1-\frac{x^2}{6}+\frac{x^4}{120}-\cdots',.7)
        self.hud([('x=',INK,lambda:self.s.get_value()),
                  (r'\sin(x)/x=',LIMIT,lambda:math.sin(self.s.get_value())/self.s.get_value()),
                  ('-x^2/6=',SEC,lambda:-self.s.get_value()**2/6),
                  ('x^4/120=',TAN,lambda:self.s.get_value()**4/120)],rows=2)
        self.pair(self.ax,self.s,math.sin,lambda x:x,self.s)
        self.play(self.s.animate.set_value(.12),run_time=4.4,rate_func=linear)


class LH11Scope(Lesson):
    START=158;END=167
    def construct(self):
        self.title('연결되지만 조건과 범위는 다르다')
        self.run_lines([self.scope])

    def scope(self):
        self.eq(r'f(x)=a_mx^m+o(x^m)\quad(a_m\ne0)',.7)
        self.note('유한 차수의 국소 전개와 일반 정리를 구분',MUTED)
        top=RoundedRectangle(width=7.6,height=2.5,corner_radius=.2,stroke_color=F,
                             fill_color=BG,fill_opacity=1).move_to([0,1.6,0])
        low=top.copy().set_stroke(G).move_to([0,-1.7,0])
        a=text('테일러: 처음 남는 항',27,F).move_to([0,2.3,0])
        b=fit(formula(r'\sin x=x+O(x^3)'),6.8).move_to([0,1.55,0])
        c=fit(text('매끄러움 ≠ 무한급수와 항상 일치',21,MUTED),7).move_to([0,.8,0])
        d=text('로피탈: 도함수 비율의 극한',27,G).move_to([0,-1,0])
        e=fit(formula(r'\lim\frac{f(x)}{g(x)}=\lim\frac{f^{\prime}(x)}{g^{\prime}(x)}'),6.7).move_to([0,-1.8,0])
        f=fit(text('미분 가능 · g′≠0 · 비율의 극한 존재 등',21,MUTED),7).move_to([0,-2.55,0])
        self.play(Create(top),Write(a),run_time=1)
        self.play(Write(b),FadeIn(c),run_time=1.3)
        self.play(Create(low),Write(d),run_time=1)
        self.play(Write(e),FadeIn(f),run_time=1.5)
        footer=text('일반적인 근거: 코시의 평균값 정리',24,TAN).move_to([0,-4.3,0])
        self.play(FadeIn(footer),run_time=.6)


class LH12Conclusion(Lesson):
    START=167;END=179
    def construct(self):
        self.title('값의 비율을 결정하는 상대적 변화')
        self.t=ValueTracker(.8)
        self.sine_plot()
        self.pair(self.ax,self.t,math.sin,lambda x:x)
        self.run_lines([self.beyond,self.answer])

    def beyond(self):
        self.eq(r'\frac{f(x)}{g(x)}\quad\longleftrightarrow\quad\frac{f^{\prime}(x)}{g^{\prime}(x)}',.8)
        self.note('공식의 조작에서 상대적 변화의 관찰로',MUTED)
        self.hud([('t=',INK,lambda:self.t.get_value()),('f/g=',LIMIT,
                  lambda:math.sin(self.t.get_value())/self.t.get_value())])
        self.play(self.t.animate.set_value(.15),run_time=3.5,rate_func=linear)

    def answer(self):
        self.eq(r'\lim_{x\to0}\frac{\sin x}{x}=1',.8)
        self.note('같은 0이 아니라, 서로에 비해 얼마나 변하는가',LIMIT)
        self.play(self.t.animate.set_value(.012),run_time=4.8,rate_func=linear)
