from pathlib import Path
import sys,json,textwrap
from manim import *
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import IntroScene,txt,math,GOLD,TEAL,PURPLE,MUTED,WHITE_INK
from longforms.euler_identity.chapter_04.visuals import ExponentialGraph,limit_eq
BLUE='#7DA8F9';GRAY='#738197'
def fit(m,width=12.7):
    if m.width>width:m.scale_to_fit_width(width)
    return m
def panel(s,size=50,y=1,color=WHITE_INK):return fit(math(s,size,color),6.15).move_to([2.8,y,0])
def cexp(size=110):
    m=MathTex(r'e^{i\theta}',substrings_to_isolate=['e','i',r'\theta'],font_size=size)
    for t,c in [('e',TEAL),('i',PURPLE),(r'\theta',GOLD)]:m.set_color_by_tex(t,c)
    return m
def euler_eq():
    m=MathTex(r'e^{i\theta}=\cos\theta+i\sin\theta',substrings_to_isolate=['e','i',r'\theta',r'\cos',r'\sin'],font_size=85)
    for t,c in [('e',TEAL),('i',PURPLE),(r'\theta',GOLD),(r'\cos',BLUE),(r'\sin',PURPLE)]:m.set_color_by_tex(t,c)
    return fit(m,12.6).move_to([0,2,0])
def complex_exp_steps(theta,n):return (1+1j*theta/n)**np.arange(n+1)
def make_axes(center=(-2.7,.3,0),unit=1.6,extent=1.5):
    return Axes(x_range=[-extent,extent,1],y_range=[-extent,extent,1],x_length=2*extent*unit,y_length=2*extent*unit,axis_config={'color':GRAY,'include_ticks':False,'include_tip':False}).move_to(center)

class FiniteVisual(VGroup):
    def __init__(self,theta=1,n=4,k=0,wide=False,**kwargs):
        super().__init__(**kwargs);self.theta=theta;self.n=n;self.k=k
        self.axes=make_axes(unit=5.2/6,extent=3) if wide else make_axes()
        self.o=self.axes.c2p(0,0);self.values=complex_exp_steps(theta,n)
        self.reference=Circle(radius=np.linalg.norm(self.axes.c2p(1,0)-self.o),color=GRAY,stroke_width=2,stroke_opacity=.5).move_to(self.o)
        self.ray=Arrow(self.o,self.point(self.values[k]),buff=0,color=BLUE,stroke_width=5)
        self.dot=Dot(self.point(self.values[k]),color=GOLD,radius=.065)
        self.path=self.path_to(k);self.add(self.axes,self.ray,self.dot,self.path)
    def point(self,z):return self.axes.c2p(z.real,z.imag)
    def path_to(self,k):
        points=[self.point(z) for z in self.values[:k+1]]
        if len(points)==1:points.append(points[0]+RIGHT*1e-8)
        return VMobject(color=TEAL,stroke_width=3).set_points_as_corners(points)
    def delta(self,k):return Arrow(self.point(self.values[k]),self.point(self.values[k+1]),buff=0,color=PURPLE,stroke_width=4,max_tip_length_to_length_ratio=.35)

class OrbitVisual(VGroup):
    def __init__(self,angle=0,center=(-2.7,.3,0),unit=1.6,velocity=False,**kwargs):
        super().__init__(**kwargs);self.theta=ValueTracker(angle);self.unit=unit;self.axes=make_axes(center,unit,1.5);self.o=self.axes.c2p(0,0)
        self.circle=Circle(radius=unit,color=GRAY,stroke_width=2).move_to(self.o)
        self.ray=always_redraw(lambda:Arrow(self.o,self.point(),buff=0,color=BLUE,stroke_width=5))
        self.dot=always_redraw(lambda:Dot(self.point(),color=GOLD,radius=.065))
        self.arc=always_redraw(lambda:Arc(radius=unit,start_angle=0,angle=max(self.theta.get_value(),1e-6),arc_center=self.o,color=TEAL,stroke_width=3))
        self.angle=always_redraw(lambda:Arc(radius=.3,start_angle=0,angle=max(self.theta.get_value(),1e-6),arc_center=self.o,color=GOLD,stroke_width=2))
        self.velocity=always_redraw(lambda:Arrow(self.point(),self.velocity_end(),buff=0,color=PURPLE,stroke_width=4))
        self.right_angle=always_redraw(lambda:RightAngle(Line(self.point(),self.o),Line(self.point(),self.velocity_end()),length=.18,color=GOLD))
        self.components=VGroup(always_redraw(lambda:Line(self.o,self.axes.c2p(np.cos(self.theta.get_value())+1e-8,0),color=BLUE,stroke_width=5)),always_redraw(lambda:Line(self.axes.c2p(np.cos(self.theta.get_value()),0),self.point()+UP*1e-8,color=PURPLE,stroke_width=4)))
        self.add(self.axes,self.circle,self.arc,self.angle,self.ray,self.dot)
        if velocity:self.add(self.velocity,self.right_angle)
    def point(self):return self.axes.c2p(np.cos(self.theta.get_value()),np.sin(self.theta.get_value()))
    def velocity_end(self):
        t=self.theta.get_value();return self.point()+self.unit*np.array([-np.sin(t),np.cos(t),0])

def previous_end():
    axes=Axes(x_range=[-.5,1.5,.5],y_range=[-.5,1.5,.5],x_length=4.2,y_length=4.2,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([-2.75,.05,0]);o=axes.c2p(0,0)
    p=lambda z:axes.c2p(z.real,z.imag);z=1+0j;paths=VGroup()
    for _ in range(3):nxt=z+.18j*z;paths.add(Line(p(z),p(nxt),color=TEAL,stroke_width=3));z=nxt
    ray=Arrow(o,p(z),buff=0,color=BLUE,stroke_width=5).set_opacity(.25);dot=Dot(p(z),color=GOLD,radius=.065).set_opacity(.25)
    axes.set_stroke(opacity=.25);paths.set_stroke(opacity=.25)
    return VGroup(axes,ray,dot,paths),cexp(125).move_to([0,.8,0])
def context_end():return make_axes().set_stroke(opacity=.25),cexp(125).move_to([0,.8,0])
def complex_limit_eq():return fit(math(r'e^{i\theta}=\lim_{n\to\infty}\left(1+\frac{i\theta}{n}\right)^n',74,TEAL))
def small_header():return complex_limit_eq().scale(.57).move_to([0,3.1,0])
def factor():return panel(r'1+\frac{i\theta}{n}',68,.4,PURPLE)
def step_panel():
    return VGroup(panel(r'z_{k+1}=z_k+\frac{i\theta}{n}z_k',48,1.5),txt('예시 · θ = 1, n = 4',23,MUTED).move_to([2.8,-.2,0]))
def comparison_panel(n):
    r=abs(complex_exp_steps(PI,n)[-1])
    return VGroup(panel(r'\theta=\pi',57,1.9,GOLD),panel(f'n={n}',57,.6),txt('최종 벡터의 길이',24,MUTED).move_to([2.8,-.6,0]),panel(f'{r:.6f}',54,-1.4,TEAL))
def comparison_state(n):
    v=FiniteVisual(PI,n,n,wide=True);v.add_to_back(v.reference);return v,comparison_panel(n)
def limit_end():
    u=OrbitVisual(PI);p=VGroup(panel(r'|z|=1',76,.9,TEAL),panel(r'n\to\infty',43,-.5,MUTED));return u,p
def derivative_end():
    u=OrbitVisual(.65)
    eq=panel(r'\frac{d}{d\theta}e^{i\theta}=ie^{i\theta}',53,1.2,TEAL)
    note=txt('복소 지수함수로 확장 · 연쇄법칙',23,MUTED).move_to([2.8,-.5,0]);return u,VGroup(eq,note)
def ode_panel():return VGroup(panel(r"z'(\theta)=iz(\theta)",60,1.6,PURPLE),txt('θ에 대한 변화율',24,MUTED).move_to([2.8,.3,0]),txt('현재 위치 z',24,BLUE).move_to([2.8,-.7,0]),txt('순간 변화율 iz',24,PURPLE).move_to([2.8,-1.5,0]))
def speed_end():
    u=OrbitVisual(1,velocity=True)
    p=VGroup(panel(r'|z|=1',60,1.6,TEAL),panel(r"|z'|=1",60,.3,PURPLE),panel('z(0)=1',42,-1,MUTED));return u,p
def radians_end():
    u=OrbitVisual(1.3)
    p=VGroup(panel(r'\theta=\frac{s}{r}=\frac{s}{1}=s',57,1.5,GOLD),txt('회전각 = θ rad',28,TEAL).move_to([2.8,-.3,0]));return u,p
def coord_pair():
    m=MathTex(r'(\cos\theta,\sin\theta)',substrings_to_isolate=[r'\cos\theta',r'\sin\theta'],font_size=57);m.set_color_by_tex(r'\cos\theta',BLUE);m.set_color_by_tex(r'\sin\theta',PURPLE);return fit(m,6.15).move_to([2.8,1.1,0])
def complex_expr():
    m=MathTex(r'\cos\theta+i\sin\theta',substrings_to_isolate=[r'\cos\theta',r'i\sin\theta'],font_size=61);m.set_color_by_tex(r'\cos\theta',BLUE);m.set_color_by_tex(r'i\sin\theta',PURPLE);return fit(m,6.15).move_to([2.8,1.1,0])
def formula_end(angle=PI/3):return OrbitVisual(angle,center=(0,-.65,0),unit=1.05),euler_eq(),txt('Euler’s Formula · 오일러 공식',24,MUTED).move_to([0,1.15,0])

class ChapterScene(IntroScene):
    index=1
    def play_for(self,t,*animations,**kwargs):self.play(*animations,run_time=t,**kwargs)
    def construct(self):
        record=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption_index=-1;self.caption_audit=[]
        self.caption=VGroup().set_z_index(100);self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
        getattr(self,record['method'])();self.to(self.total_duration);self.caption.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def update_caption(self):
        # A persistent updated layer prevents stale captions in Cairo's static background.
        t=self.start+round(self.time*config.frame_rate)/config.frame_rate
        index=next((k for k,x in enumerate(self.lines) if x['start']<=t<x['end']),len(self.lines)-1)
        if index==self.caption_index:return
        self.caption_index=index
        wrapped=textwrap.fill(self.lines[index]['text'],width=49,break_long_words=False,break_on_hyphens=False)
        text=txt(wrapped,25)
        if text.width>12.5:text.scale_to_fit_width(12.5)
        text.move_to([0,-3.35,0])
        band=Rectangle(width=128/9,height=1.3,stroke_width=0,fill_color='#10151F',fill_opacity=1).move_to([0,-3.35,0])
        self.caption.become(VGroup(band,text).set_z_index(100))
        assert text.get_bottom()[1]>-3.95 and text.get_top()[1]<-2.75
        self.caption_audit.append(dict(line=index+1,left=float(text.get_left()[0]),right=float(text.get_right()[0]),top=float(text.get_top()[1]),bottom=float(text.get_bottom()[1])))
    def opening(self):
        old,eq=previous_end();self.add(old,eq);g=ExponentialGraph('derivative');curve=g.curve();u=OrbitVisual(0,center=(3,.3,0),unit=1.3)
        labels=VGroup(math('e^x',52,TEAL).move_to([-2.8,2.8,0]),math(r'\times i',52,PURPLE).move_to([3,2.8,0]))
        self.play_for(1.3,FadeOut(old),FadeOut(eq),FadeIn(g),Create(curve),FadeIn(u),FadeIn(labels));self.to(5)
        dot=Dot(curve.get_start(),color=GOLD,radius=.06);self.add(dot)
        self.play_for(3.5,u.theta.animate.set_value(PI/2),MoveAlongPath(dot,curve),rate_func=linear);self.to(11)
        axes,new=context_end();self.play_for(1.5,FadeOut(g),FadeOut(curve),FadeOut(dot),FadeOut(u),FadeOut(labels),FadeIn(axes),FadeIn(new));self.to(15)
    def complex_limit(self):
        axes,old=context_end();self.add(axes,old);real=limit_eq();self.play_for(1.2,FadeOut(axes),TransformMatchingTex(old,real));self.to(4)
        note=txt('한 단계 비율 x/n · 반복 횟수 n',28,MUTED).move_to([0,-1.1,0]);self.play_for(.7,FadeIn(note));self.to(10)
        expanded=complex_limit_eq().move_to([0,.6,0]);self.play_for(1.2,TransformMatchingTex(real,expanded),FadeOut(note));self.to(13)
        self.play_for(1,expanded.animate.scale(.57).move_to([0,3.1,0]),FadeIn(txt('복소 지수함수로 확장',25,MUTED).move_to([0,-.5,0])));self.to(17)
    def start_one(self):
        header=small_header();note=txt('복소 지수함수로 확장',25,MUTED).move_to([0,-.5,0]);self.add(header,note);v=FiniteVisual()
        self.play_for(1,FadeOut(note),FadeIn(v.axes),FadeIn(v.dot));self.to(4)
        z0=panel('z_0=1',63,2.0,BLUE);self.play_for(.8,Create(v.ray),FadeIn(z0));self.to(6)
        self.play_for(.8,FadeIn(factor()));self.to(10)
    def first_step(self):
        v=FiniteVisual();header=small_header();z0=panel('z_0=1',63,2.0,BLUE);f=factor();self.add(v,header,z0,f)
        eq=panel(r'z_1=z_0(1+i\theta/n)',51,1.6);self.play_for(.8,FadeOut(z0),FadeOut(f),FadeIn(eq));self.to(4)
        expanded=panel(r'z_1=z_0+\frac{i\theta}{n}z_0',54,1.6);delta=v.delta(0)
        angle=RightAngle(Line(v.point(v.values[0]),v.o),Line(v.point(v.values[0]),v.point(v.values[1])),length=.15,color=GOLD)
        self.play_for(1.2,TransformMatchingTex(eq,expanded),Create(delta),Create(angle))
        self.play_for(.8,FadeIn(txt('현재 벡터 + 수직 변화량',24,MUTED).move_to([2.8,-.2,0])));self.to(11)
        next_ray=Arrow(v.o,v.point(v.values[1]),buff=0,color=GOLD,stroke_width=5);segment=v.path_to(1)
        self.play_for(1.5,Create(next_ray),Create(segment),v.dot.animate.move_to(v.point(v.values[1])))
        self.play_for(.7,FadeOut(v.ray),next_ray.animate.set_color(BLUE),FadeOut(delta),FadeOut(angle));self.to(16)
    def repeat_steps(self):
        v=FiniteVisual(k=1);header=small_header();old=panel(r'z_1=z_0+\frac{i\theta}{n}z_0',54,1.6);note=txt('현재 벡터 + 수직 변화량',24,MUTED).move_to([2.8,-.2,0]);self.add(v,header,old,note)
        p=step_panel();self.play_for(.8,FadeOut(old),FadeOut(note),FadeIn(p));self.to(4)
        for k in [1,2]:
            delta=v.delta(k);nxt=Arrow(v.o,v.point(v.values[k+1]),buff=0,color=GOLD,stroke_width=5)
            self.play_for(.5,Create(delta));self.play_for(1.2,Transform(v.ray,nxt),v.dot.animate.move_to(v.point(v.values[k+1])),Transform(v.path,v.path_to(k+1)),rate_func=linear);self.play_for(.5,FadeOut(delta),v.ray.animate.set_color(BLUE))
        self.to(13)
    def finite_growth(self):
        v=FiniteVisual(k=3);header=small_header();p=step_panel();self.add(v,header,p);self.to(3)
        norm=panel(r'|1+ih|=\sqrt{1+h^2}>1',51,1.5,GOLD);h=panel(r'h=\theta/n\ne0',38,.1,MUTED)
        self.play_for(1,FadeOut(p),FadeIn(norm),FadeIn(h))
        triangle=VGroup(Arrow(v.o,v.point(1),buff=0,color=BLUE,stroke_width=4),v.delta(0),Arrow(v.o,v.point(v.values[1]),buff=0,color=GOLD,stroke_width=3))
        self.play_for(1,FadeIn(triangle));self.to(8)
        actual=panel(f'|z_3|={abs(v.values[3]):.6f}',50,-1.1,TEAL);self.play_for(1,Create(v.reference),FadeIn(actual));self.to(14)
    def four_steps(self):
        old=FiniteVisual(k=3);old.add_to_back(old.reference);header=small_header();p=VGroup(panel(r'|1+ih|=\sqrt{1+h^2}>1',51,1.5,GOLD),panel(r'h=\theta/n\ne0',38,.1,MUTED),panel(f'|z_3|={abs(old.values[3]):.6f}',50,-1.1,TEAL));self.add(old,header,p)
        v=FiniteVisual(PI,4,0,wide=True);v.add_to_back(v.reference);info=comparison_panel(4)
        self.play_for(1.2,FadeOut(old),FadeOut(header),FadeOut(p),FadeIn(v),FadeIn(info));self.to(3)
        for k in range(4):
            delta=v.delta(k);self.play_for(.3,Create(delta));self.play_for(.7,Transform(v.ray,Arrow(v.o,v.point(v.values[k+1]),buff=0,color=BLUE,stroke_width=5)),v.dot.animate.move_to(v.point(v.values[k+1])),Transform(v.path,v.path_to(k+1)),rate_func=linear);self.play_for(.2,FadeOut(delta))
        self.to(8);self.play_for(.7,Indicate(v.dot,color=GOLD,scale_factor=1.5));self.to(13)
    def refine_steps(self):
        v,p=comparison_state(4);self.add(v,p)
        for n,start,end in [(10,0,6),(100,6,10),(1000,10,14)]:
            self.to(start);new,info=comparison_state(n)
            self.play_for(.6,FadeOut(v.path),FadeOut(v.ray),FadeOut(v.dot),Transform(p,info));self.play_for(1.4,Create(new.path),FadeIn(new.ray),FadeIn(new.dot));v.path=new.path;v.ray=new.ray;v.dot=new.dot;self.to(end)
    def limit_circle(self):
        v,p=comparison_state(1000);self.add(v,p);new,info=comparison_state(10000)
        self.play_for(2,FadeOut(v.path),FadeOut(v.ray),FadeOut(v.dot),Create(new.path),FadeIn(new.ray),FadeIn(new.dot),Transform(p,info));self.to(6)
        u,limit=limit_end();self.play_for(1.4,FadeOut(v.axes),FadeOut(v.reference),FadeOut(new.path),FadeOut(new.ray),FadeOut(new.dot),FadeOut(p),FadeIn(u),FadeIn(limit));self.to(10)
    def angle_question(self):
        u,p=limit_end();self.add(u,p);q=panel(r'\theta\ =\ ?',90,.8,GOLD);self.play_for(.8,FadeOut(p),FadeIn(q));self.to(3)
        arc=Arc(radius=1.6,start_angle=0,angle=PI,arc_center=u.o,color=GOLD,stroke_width=5);self.play_for(1.5,Create(arc));self.to(7.4);self.play_for(.6,FadeOut(arc));self.to(8)
    def derivative(self):
        u=OrbitVisual(PI);q=panel(r'\theta\ =\ ?',90,.8,GOLD);self.add(u,q)
        self.play_for(1,u.theta.animate.set_value(.65),FadeOut(q));self.to(3)
        real=panel(r'\frac{d}{dx}e^x=e^x',58,1.2,TEAL);self.play_for(.7,FadeIn(real));self.to(7)
        _,p=derivative_end();self.play_for(1.4,TransformMatchingTex(real,p[0]),FadeIn(p[1]));self.to(14)
    def perpendicular(self):
        u,p=derivative_end();self.add(u,p);ode=ode_panel();self.play_for(1,FadeOut(p),FadeIn(ode));self.to(7)
        velocity_at_origin=Arrow(u.o,u.o+u.velocity_end()-u.point(),buff=0,color=PURPLE,stroke_width=4)
        self.play_for(.5,Create(velocity_at_origin));self.play_for(.7,velocity_at_origin.animate.shift(u.point()-u.o))
        self.play_for(.4,FadeOut(velocity_at_origin),FadeIn(u.velocity),Create(u.right_angle));self.to(12)
        self.play_for(4,u.theta.animate.set_value(1),rate_func=linear)
    def unit_speed(self):
        u=OrbitVisual(1,velocity=True);p=ode_panel();self.add(u,p)
        lengths=VGroup(panel(r"|z'|=|z|",66,1.5,PURPLE),panel(r'|z|=\mathrm{constant}',43,0,MUTED));self.play_for(1,FadeOut(p),FadeIn(lengths))
        self.play_for(4,u.theta.animate.set_value(1.35),rate_func=linear);self.to(9)
        _,end=speed_end();self.play_for(1.2,FadeOut(lengths),FadeIn(end),u.theta.animate.set_value(1));self.to(13)
    def radians(self):
        u,p=speed_end();self.add(u,p);self.play_for(.6,FadeOut(p),FadeOut(u.velocity),FadeOut(u.right_angle),u.theta.animate.set_value(0))
        unit=panel(r'|z|=1\quad|z^\prime|=1',49,1.7,TEAL);self.add(unit)
        self.play_for(4.4,u.theta.animate.set_value(1),rate_func=linear)
        eq=panel(r'\theta=\frac{s}{r}',65,.4,GOLD);self.play_for(.8,FadeIn(eq));self.to(9)
        full=panel(r'\theta=\frac{s}{r}=\frac{s}{1}=s',57,1.5,GOLD);self.play_for(1,FadeOut(unit),TransformMatchingTex(eq,full));self.to(13)
        note=txt('회전각 = θ rad',28,TEAL).move_to([2.8,-.3,0]);self.play_for(.6,FadeIn(note));self.play_for(3.4,u.theta.animate.set_value(1.3),rate_func=linear)
    def coordinates(self):
        u,p=radians_end();self.add(u,p);self.play_for(1,FadeOut(p),u.theta.animate.set_value(PI/4));self.to(4)
        pair=coord_pair();self.play_for(1,FadeIn(u.components),FadeIn(pair));self.to(10)
    def complex_coordinates(self):
        u=OrbitVisual(PI/4);u.add(u.components);pair=coord_pair();self.add(u,pair)
        labels=VGroup(txt('Re',22,BLUE).next_to(u.axes.x_axis,RIGHT,buff=.08),txt('Im',22,PURPLE).next_to(u.axes.y_axis,UP,buff=.08))
        parts=VGroup(panel(r'\operatorname{Re}z=\cos\theta',41,0,BLUE),panel(r'\operatorname{Im}z=\sin\theta',41,-1.1,PURPLE));self.play_for(.8,FadeIn(labels),FadeIn(parts));self.to(4)
        expr=complex_expr();self.play_for(1.5,TransformMatchingTex(pair,expr),FadeOut(parts));self.to(7)
        expo=cexp(75).move_to([2.8,-.6,0]);self.play_for(.8,FadeIn(expo));self.to(9)
    def euler_formula(self):
        u=OrbitVisual(PI/4);u.add(u.components);labels=VGroup(txt('Re',22,BLUE).next_to(u.axes.x_axis,RIGHT,buff=.08),txt('Im',22,PURPLE).next_to(u.axes.y_axis,UP,buff=.08));expr=complex_expr();expo=cexp(75).move_to([2.8,-.6,0]);self.add(u,labels,expr,expo)
        final,eq,title=formula_end(PI/4);self.play_for(1.4,FadeOut(u),FadeOut(labels),FadeOut(expr),FadeOut(expo),FadeIn(final),FadeIn(eq));self.play_for(4,final.theta.animate.set_value(PI/3),rate_func=linear);self.to(6)
        self.play_for(.8,FadeIn(title));self.to(8)
    def closing(self):
        u,eq,title=formula_end();self.add(u,eq,title)
        left=VGroup(txt('연속적인 변화',25,TEAL),cexp(60)).arrange(DOWN,buff=.4).move_to([-4.6,-.2,0])
        right=VGroup(txt('삼각함수와 좌표',25,PURPLE),fit(complex_expr(),4.5)).arrange(DOWN,buff=.4).move_to([4.5,-.2,0])
        self.play_for(.7,FadeIn(left),FadeIn(right));self.play_for(3.3,u.theta.animate.set_value(PI/2),rate_func=linear)
        self.play_for(.4,FadeOut(left),FadeOut(right),u.theta.animate.set_value(0));self.play_for(2.6,u.theta.animate.set_value(PI/3),rate_func=linear)
