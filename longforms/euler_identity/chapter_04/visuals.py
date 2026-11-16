from pathlib import Path
import sys,json
from manim import *
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import IntroScene,txt,math,GOLD,TEAL,PURPLE,MUTED,WHITE_INK,exponential
from longforms.euler_identity.chapter_03.visuals import ComplexRotationVisual,cmath
BLUE='#7DA8F9'

def discrete_growth(x,n):
    return np.exp(np.arange(n+1)*np.log1p(x/n))

class ExponentialGraph(VGroup):
    def __init__(self,mode='comparison',**kwargs):
        super().__init__(**kwargs)
        if mode=='integers':xr,yr,xl,yl,pos=[0,4,1],[0,18,4],6.5,3.9,[-1.9,.1,0]
        elif mode=='derivative':xr,yr,xl,yl,pos=[-.5,1.5,.5],[0,5,1],4.8,3.8,[-2.8,.1,0]
        else:xr,yr,xl,yl,pos=[-.5,2,.5],[0,10,2],6.5,3.9,[-1.9,.1,0]
        self.axes=Axes(x_range=xr,y_range=yr,x_length=xl,y_length=yl,axis_config={'color':MUTED,'include_tip':False,'include_numbers':True,'font_size':19}).move_to(pos)
        self.domain=[xr[0],xr[1]];self.add(self.axes)
        self.names=VGroup(math('x',24,MUTED).next_to(self.axes.x_axis,RIGHT,buff=.13),math('y',24,MUTED).next_to(self.axes.y_axis,UP,buff=.1));self.add(self.names)
    def curve(self,base=np.e,color=TEAL):return self.axes.plot(lambda x:base**x,x_range=self.domain,color=color,stroke_width=4)

class TangentVisual(VGroup):
    def __init__(self,x=0,**kwargs):
        super().__init__(**kwargs);self.x=ValueTracker(x);self.graph=ExponentialGraph('derivative');self.curve=self.graph.curve()
        self.dot=always_redraw(lambda:Dot(self.graph.axes.c2p(self.x.get_value(),np.exp(self.x.get_value())),color=GOLD,radius=.065))
        def tangent():
            x=self.x.get_value();y=np.exp(x);dx=.23
            return Line(self.graph.axes.c2p(x-dx,y-y*dx),self.graph.axes.c2p(x+dx,y+y*dx),color=GOLD,stroke_width=4)
        self.tangent=always_redraw(tangent);self.add(self.graph,self.curve,self.tangent,self.dot)

class GrowthIteration(VGroup):
    def __init__(self,value=1,**kwargs):
        super().__init__(**kwargs);self.value=ValueTracker(value)
        def bar():
            w=3*self.value.get_value()
            return Rectangle(width=w,height=.55,stroke_color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([-4.8+w/2,0,0])
        self.bar=always_redraw(bar)
        self.number=DecimalNumber(value,num_decimal_places=3,font_size=72,color=TEAL).move_to([2.8,.5,0]);self.number.add_updater(lambda m:m.set_value(self.value.get_value()))
        self.eq=math(r'y_{k+1}=y_k(1+0.1)',65,TEAL).move_to([0,2,0]);self.add(self.bar,self.number,self.eq)

class ExponentialLimit(VGroup):
    def __init__(self,n=10,center=(-2.5,.1,0),**kwargs):
        super().__init__(**kwargs)
        self.axes=Axes(x_range=[0,1,.25],y_range=[0,3.1,1],x_length=5.8,y_length=3.6,axis_config={'color':MUTED,'include_tip':False,'include_numbers':True,'font_size':18}).move_to(center)
        self.exact=self.axes.plot(lambda t:np.exp(t),x_range=[0,1],color=MUTED,stroke_width=3)
        self.steps=self.path(n);self.add(self.axes,self.exact,self.steps)
    def path(self,n):
        values=discrete_growth(1,n);points=[self.axes.c2p(0,1)]
        for k in range(n):points.extend([self.axes.c2p((k+1)/n,values[k]),self.axes.c2p((k+1)/n,values[k+1])])
        return VMobject(color=TEAL,stroke_width=3).set_points_as_corners(points)

class ComplexDirectionPreview(VGroup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.axes=Axes(x_range=[-1.5,1.5,.5],y_range=[-1.5,1.5,.5],x_length=3.8,y_length=3.8,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([3,.1,0])
        o=self.axes.c2p(0,0);z=self.axes.c2p(1,.4);iz=self.axes.c2p(-.4,1)
        self.z=Arrow(o,z,buff=0,color=BLUE,stroke_width=5);self.iz=Arrow(o,iz,buff=0,color=PURPLE,stroke_width=5)
        self.labels=VGroup(math('z',33,BLUE).next_to(z,RIGHT,buff=.1),math('iz',33,PURPLE).next_to(iz,UP,buff=.1))
        self.right_angle=RightAngle(Line(o,z),Line(o,iz),length=.22,color=GOLD)
        self.add(self.axes,self.z,self.iz,self.labels,self.right_angle)

def powers_state():
    return VGroup(*[VGroup(math(f'2^{k}',65,BLUE),math(str(2**k),35,MUTED)).arrange(DOWN,buff=.45).move_to([x,.6,0]) for k,x in zip(range(1,5),[-4.5,-1.5,1.5,4.5])])
def comparison_state():
    g=ExponentialGraph();curves=VGroup(g.curve(2,BLUE),g.curve(np.e,TEAL),g.curve(3,GOLD))
    labels=VGroup(math('2^x',45,BLUE).move_to([4.2,1.8,0]),math('e^x',45,TEAL).move_to([4.2,.5,0]),math('3^x',45,GOLD).move_to([4.2,-.8,0]))
    return g,curves,labels
def derivative_eq():return math(r'\frac{d}{dx}e^x=e^x',57,TEAL).move_to([2.8,1.6,0])
def rate_panel(v):
    g=VGroup()
    for name,y,c in [('현재 값',.5,WHITE_INK),('순간 변화율',-1.2,GOLD)]:
        label=txt(name,25,c).move_to([1.9,y,0]);number=DecimalNumber(1,num_decimal_places=2,font_size=48,color=c).move_to([4.4,y,0]);number.add_updater(lambda m:m.set_value(np.exp(v.x.get_value())))
        g.add(label,number)
    return g
def small_growth_pair():
    graphs=VGroup()
    for center in [[-3.2,.1,0],[3.2,.1,0]]:
        a=Axes(x_range=[0,1,.5],y_range=[0,3,1],x_length=4.5,y_length=3.3,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to(center);graphs.add(a)
    curve=graphs[0].plot(lambda t:np.exp(t),x_range=[0,1],color=TEAL,stroke_width=4)
    values=discrete_growth(1,5);points=[graphs[1].c2p(0,1)]
    for k in range(5):points.extend([graphs[1].c2p((k+1)/5,values[k]),graphs[1].c2p((k+1)/5,values[k+1])])
    steps=VMobject(color=GOLD,stroke_width=3).set_points_as_corners(points)
    labels=VGroup(txt('연속적인 성장',26,TEAL).move_to([-3.2,2.5,0]),txt('작은 변화 × 반복',26,GOLD).move_to([3.2,2.5,0]))
    return VGroup(graphs,curve,steps,labels)
def step_panel(n):
    return VGroup(math(r'(1+1/n)^n',53,TEAL).move_to([3,1.7,0]),math(f'n={n}',43).move_to([3,.6,0]),math(f'{discrete_growth(1,n)[-1]:.5f}',55,TEAL).move_to([3,-.4,0]),txt(f'한 단계 비율 {100/n:g}%',23,MUTED).move_to([3,-1.4,0]))
def limit_eq():return math(r'e^x=\lim_{n\to\infty}\left(1+\frac{x}{n}\right)^n',75,TEAL).move_to([0,1,0])
def convergence_end():
    g=ExponentialLimit(200);g.remove(g.steps);g.exact.set_color(TEAL).set_stroke(width=4)
    formula=limit_eq().scale(.58).move_to([0,2.9,0])
    panel=VGroup(math('e^t',65,TEAL).move_to([3,1.5,0]),math(r'e\approx2.71828',46,TEAL).move_to([3,.1,0]),txt('연속적인 성장',25,MUTED).move_to([3,-1.2,0]))
    return g,formula,panel
def proportional_state():
    left=VGroup(txt('일정한 양을 더함',28,MUTED),math('y_{k+1}=y_k+c',50),math(r'1\to2\to3\to4',43),math(r'+1\quad+1\quad+1',33,GOLD)).arrange(DOWN,buff=.55).move_to([-3.2,.5,0])
    right=VGroup(txt('현재 값에 비례하는 변화',27,TEAL),math('y_{k+1}=y_k(1+h)',48,TEAL),math(r'1\to1.1\to1.21',43),math(r'+0.1\quad+0.11',33,GOLD)).arrange(DOWN,buff=.55).move_to([3.2,.5,0])
    return VGroup(left,right)
def direction_end():
    a=Axes(x_range=[0,1.2,.4],y_range=[0,4,1],x_length=3.8,y_length=3.1,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([-3.3,.1,0])
    curve=a.plot(lambda x:np.exp(x),x_range=[0,1.2],color=TEAL,stroke_width=4)
    arrow=Arrow(a.c2p(1,np.exp(1)),a.c2p(1,np.exp(1)+.7),buff=0,color=GOLD,stroke_width=4)
    left=VGroup(a,curve,arrow,math("y'=y",52,TEAL).move_to([-3.3,2.5,0]))
    right=ComplexDirectionPreview();header=txt('변화의 방향',32).move_to([0,3.2,0])
    return left,right,header

class ChapterScene(IntroScene):
    index=1
    def play_for(self,t,*animations,**kwargs):self.play(*animations,run_time=t,**kwargs)
    def construct(self):
        record=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption=VGroup();self.caption_index=-1;self.caption_audit=[]
        self.caption_driver=VMobject().add_updater(lambda m,dt:self.update_caption());self.add(self.caption_driver);self.update_caption()
        getattr(self,record['method'])();self.to(self.total_duration);self.caption_driver.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def opening(self):
        e=math('e',140,TEAL).move_to([0,.3,0]);curve=exponential(.9)[1].move_to([2.2,.3,0]).set_stroke(opacity=.2);self.add(e,curve)
        u=ComplexRotationVisual(0);label=cmath(r'\times i',65).move_to([2.7,.5,0]);self.play_for(1,FadeOut(e),FadeOut(curve),FadeIn(u),FadeIn(label))
        self.play_for(2.5,u.theta.animate.set_value(PI/2),rate_func=linear);self.to(5)
        q=math(r'\times\,?',80).move_to(label);self.play_for(.6,TransformMatchingTex(label,q),u.theta.animate.set_value(0))
        self.play_for(1.5,u.theta.animate.set_value(5*DEGREES),rate_func=linear);self.play_for(1.5,u.theta.animate.set_value(DEGREES),rate_func=linear);self.to(11)
        power=math('2^3',110,BLUE).move_to([0,.5,0]);self.play_for(1.5,FadeOut(u),FadeOut(q),FadeIn(power));self.to(15)
    def integer_powers(self):
        old=math('2^3',110,BLUE).move_to([0,.5,0]);self.add(old);eq=math(r'2^3=2\times2\times2=8',75,BLUE).move_to([0,.5,0]);self.play_for(1.3,TransformMatchingTex(old,eq));self.to(3)
        new=math(r'2^4=2\times2\times2\times2=16',72,BLUE).move_to(eq);self.play_for(1.5,TransformMatchingTex(eq,new));self.to(7)
        p=powers_state();self.play_for(1,FadeOut(new),FadeIn(p));self.to(11)
    def fraction_question(self):
        p=powers_state();self.add(p);self.play_for(1,FadeOut(p));self.to(3)
        row=VGroup(math('2^0',65,BLUE),math('2^{1/2}',80,TEAL),math('2^1',65,BLUE)).arrange(RIGHT,buff=2).move_to([0,.7,0])
        self.play_for(.8,FadeIn(row));question=txt('2를 반 번 곱한다?',30,MUTED).move_to([0,-.8,0]);self.play_for(.7,FadeIn(question));self.to(9)
        rule=math('2^a2^b=2^{a+b}',82,TEAL).move_to([0,.5,0]);self.play_for(1,FadeOut(row),FadeOut(question),FadeIn(rule));self.to(12)
    def square_root(self):
        old=math('2^a2^b=2^{a+b}',82,TEAL).move_to([0,.5,0]);self.add(old)
        eq=math(r'2^{1/2}\cdot2^{1/2}=2^{1/2+1/2}=2',70,TEAL).move_to([0,.8,0]);self.play_for(2,TransformMatchingTex(old,eq));self.to(5)
        root=math(r'2^{1/2}=\sqrt2',85,TEAL).move_to([0,1,0]);line=NumberLine(x_range=[1,2,.25],length=7,include_numbers=True,font_size=23,color=MUTED).move_to([0,-1,0]);dot=Dot(line.n2p(np.sqrt(2)),color=TEAL,radius=.08)
        self.play_for(1,TransformMatchingTex(eq,root),FadeIn(line),FadeIn(dot));self.to(9);self.play_for(.7,FadeOut(line),FadeOut(dot));self.to(10)
    def real_exponents(self):
        root=math(r'2^{1/2}=\sqrt2',85,TEAL).move_to([0,1,0]);self.add(root);g=ExponentialGraph('integers');self.play_for(.8,FadeOut(root),FadeIn(g))
        integer=VGroup(*[Dot(g.axes.c2p(x,2**x),color=BLUE,radius=.055) for x in range(5)]);self.play_for(.8,FadeIn(integer))
        fractions=VGroup(*[Dot(g.axes.c2p(x,2**x),color=TEAL,radius=.035) for x in np.arange(.125,4,.125) if x%1]);self.play_for(2,FadeIn(fractions));self.to(5)
        curve=g.curve(2,BLUE);label=math('y=2^x',67,BLUE).move_to([4.2,1.2,0]);self.play_for(2,Create(curve),FadeOut(integer),FadeOut(fractions),FadeIn(label));self.to(11)
    def bases(self):
        old=ExponentialGraph('integers');oldcurve=old.curve(2,BLUE);oldlabel=math('y=2^x',67,BLUE).move_to([4.2,1.2,0]);self.add(old,oldcurve,oldlabel)
        g,curves,labels=comparison_state();self.play_for(1.2,FadeOut(old),FadeOut(oldcurve),FadeOut(oldlabel),FadeIn(g),FadeIn(curves[0]),FadeIn(labels[0]))
        self.play_for(1.5,Create(curves[2]),FadeIn(labels[2]));self.to(5)
        self.play_for(1.5,Create(curves[1]),FadeIn(labels[1]));self.to(10)
        x=1.5;line=DashedLine(g.axes.c2p(x,0),g.axes.c2p(x,3**x),color=MUTED)
        dots=VGroup(*[Dot(g.axes.c2p(x,b**x),color=c,radius=.06) for b,c in [(2,BLUE),(np.e,TEAL),(3,GOLD)]])
        self.play_for(.8,Create(line),FadeIn(dots));self.to(14);self.play_for(.7,FadeOut(line),FadeOut(dots));self.to(15)
    def derivative(self):
        g,curves,labels=comparison_state();self.add(g,curves,labels);v=TangentVisual(.1);self.play_for(1,FadeOut(g),FadeOut(curves),FadeOut(labels),FadeIn(v));self.play_for(2,v.x.animate.set_value(.5))
        eq=math(r'\frac{d}{dx}a^x=(\ln a)a^x',49).move_to([2.8,1.3,0]);note=math('a>0',28,MUTED).move_to([2.8,-.1,0]);self.play_for(.8,FadeIn(eq),FadeIn(note));self.to(8)
        one=math(r'\ln e=1',57,GOLD).move_to([2.8,-.1,0]);self.play_for(1,FadeOut(note),FadeIn(one));self.to(12)
        self.play_for(1,TransformMatchingTex(eq,derivative_eq()),FadeOut(one));self.to(14)
    def equal_rate(self):
        v=TangentVisual(.5);eq=derivative_eq();self.add(v,eq);panel=rate_panel(v)
        self.play_for(1.5,v.x.animate.set_value(0),FadeIn(panel));self.to(7)
        self.play_for(4,v.x.animate.set_value(np.log(2)),rate_func=linear);self.to(14)
        self.play_for(3,v.x.animate.set_value(1.1),rate_func=linear)
    def discrete_question(self):
        v=TangentVisual(1.1);eq=derivative_eq();panel=rate_panel(v);self.add(v,eq,panel);self.to(4)
        pair=small_growth_pair();self.play_for(1,FadeOut(v),FadeOut(eq),FadeOut(panel),FadeIn(pair[0]),FadeIn(pair[1]),FadeIn(pair[3]));self.to(8)
        self.play_for(4,Create(pair[2]),rate_func=linear);self.to(13)
    def ten_percent(self):
        old=small_growth_pair();self.add(old);g=GrowthIteration();self.play_for(1,FadeOut(old),FadeIn(g));self.to(4)
        plus=txt('+10%',35,GOLD).move_to([2.8,-.8,0]);self.play_for(1.2,g.value.animate.set_value(1.1),FadeIn(plus));self.to(9)
        self.play_for(1.2,g.value.animate.set_value(1.21));self.to(14)
        sequence=math(r'1\to1.1\to1.21\to1.331',52).move_to([0,-1.6,0]);self.play_for(1.2,g.value.animate.set_value(1.331),FadeIn(sequence));self.to(19)
    def refinement(self):
        old=GrowthIteration(1.331);plus=txt('+10%',35,GOLD).move_to([2.8,-.8,0]);sequence=math(r'1\to1.1\to1.21\to1.331',52).move_to([0,-1.6,0]);self.add(old,plus,sequence)
        g=ExponentialLimit(10);panel=step_panel(10);header=txt('고정 구간 0 ≤ t ≤ 1 · x = 1',27).move_to([0,2.9,0]);self.play_for(1,FadeOut(old),FadeOut(plus),FadeOut(sequence),FadeIn(g),FadeIn(panel),FadeIn(header));self.to(3)
        for n,target in [(20,6),(100,9)]:
            new=step_panel(n);self.play_for(1,Transform(g.steps,g.path(n)),Transform(panel,new));self.to(target)
    def limit_formula(self):
        g=ExponentialLimit(100);panel=step_panel(100);header=txt('고정 구간 0 ≤ t ≤ 1 · x = 1',27).move_to([0,2.9,0]);self.add(g,panel,header)
        expression=math(r'\left(1+\frac{x}{n}\right)^n',110,TEAL).move_to([0,1.2,0]);note=txt('x 고정 · 한 단계 비율 x/n · 반복 횟수 n',28,MUTED).move_to([0,-.6,0])
        self.play_for(1.2,FadeOut(g),FadeOut(panel),FadeOut(header),FadeIn(expression),FadeIn(note));self.to(5)
        counts=math(r'n=10\quad100\quad1000\quad\cdots',54,GOLD).move_to([0,-1.6,0]);self.play_for(.8,FadeIn(counts));self.to(9)
        eq=limit_eq();self.play_for(1.2,TransformMatchingTex(expression,eq),FadeOut(counts),note.animate.move_to([0,-1.1,0]));self.to(12)
    def convergence(self):
        eq=limit_eq();note=txt('x 고정 · 한 단계 비율 x/n · 반복 횟수 n',28,MUTED).move_to([0,-1.1,0]);self.add(eq,note)
        g=ExponentialLimit(5);panel=step_panel(5);self.play_for(1,eq.animate.scale(.58).move_to([0,2.9,0]),FadeOut(note),FadeIn(g),FadeIn(panel));self.to(4)
        for n in [10,50,200]:self.play_for(.6,Transform(g.steps,g.path(n)),Transform(panel,step_panel(n)))
        _,_,endpanel=convergence_end();self.play_for(1,FadeOut(g.steps),g.exact.animate.set_color(TEAL).set_stroke(width=4),Transform(panel,endpanel));self.to(8)
    def proportional(self):
        g,eq,panel=convergence_end();self.add(g,eq,panel);p=proportional_state();self.play_for(1,FadeOut(g),FadeOut(eq),FadeOut(panel),FadeIn(p));self.to(4)
        self.play_for(.8,Indicate(p[1][3],color=GOLD,scale_factor=1.1));self.to(6)
    def direction(self):
        old=proportional_state();self.add(old);left,right,header=direction_end()
        self.play_for(1,FadeOut(old),FadeIn(left),FadeIn(right.axes),FadeIn(right.z),FadeIn(right.labels[0]));self.to(4)
        self.play_for(2,Create(right.iz),FadeIn(right.labels[1]),Create(right.right_angle));self.to(9)
        self.play_for(.8,FadeIn(header));self.to(15)
    def complex_question(self):
        left,right,header=direction_end();self.add(left,right,header)
        axes=Axes(x_range=[-.5,1.5,.5],y_range=[-.5,1.5,.5],x_length=4.2,y_length=4.2,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([-2.75,.05,0]);o=axes.c2p(0,0)
        z=1+0j;point=lambda v:axes.c2p(v.real,v.imag)
        ray=Arrow(o,point(z),buff=0,color=BLUE,stroke_width=5);dot=Dot(point(z),color=GOLD,radius=.065)
        eq=math(r'z_{\mathrm{new}}=z+h\,iz',52,PURPLE).move_to([2.8,1.7,0]);finite=txt('유한 단계 예시 · h = 0.18',24,MUTED).move_to([2.8,.3,0])
        self.play_for(1.2,FadeOut(left),FadeOut(right),FadeOut(header),FadeIn(axes),FadeIn(ray),FadeIn(dot),FadeIn(eq),FadeIn(finite))
        paths=VGroup()
        for _ in range(3):
            next_z=z+.18j*z;delta=Arrow(point(z),point(next_z),buff=0,color=PURPLE,stroke_width=4,max_tip_length_to_length_ratio=.3);segment=Line(point(z),point(next_z),color=TEAL,stroke_width=3)
            self.play_for(.3,Create(delta));self.play_for(.9,Transform(ray,Arrow(o,point(next_z),buff=0,color=BLUE,stroke_width=5)),dot.animate.move_to(point(next_z)),Create(segment),rate_func=linear);self.play_for(.2,FadeOut(delta));paths.add(segment);z=next_z
        self.to(7)
        growth=txt('성장?',38,TEAL).move_to([2.8,-.7,0]);turn=txt('회전?',38,GOLD).move_to([2.8,-1.7,0]);self.play_for(.7,FadeIn(growth));self.to(9);self.play_for(.7,FadeIn(turn));self.to(11)
        final=MathTex(r'e^{i\theta}',substrings_to_isolate=['e','i',r'\theta'],font_size=125).move_to([0,.8,0]);final.set_color_by_tex('e',TEAL);final.set_color_by_tex('i',PURPLE);final.set_color_by_tex(r'\theta',GOLD)
        self.play_for(1.2,FadeOut(eq),FadeOut(finite),FadeOut(growth),FadeOut(turn),FadeIn(final),axes.animate.set_stroke(opacity=.25),ray.animate.set_opacity(.25),dot.animate.set_opacity(.25),paths.animate.set_stroke(opacity=.25));self.to(15)
