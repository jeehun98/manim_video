from pathlib import Path
import json,sys
from manim import *
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import IntroScene,txt,math,GOLD,TEAL,PURPLE,MUTED,WHITE_INK
BLUE='#7DA8F9';GRAY='#E1E7F0'

class CircleRatioVisual(VGroup):
    def __init__(self,radius=1,center=ORIGIN,**kwargs):
        super().__init__(**kwargs)
        self.circle=Circle(radius=radius,color=GOLD,stroke_width=4).move_to(center)
        self.diameter=Line(np.array(center)+LEFT*radius,np.array(center)+RIGHT*radius,color=GRAY,stroke_width=2)
        self.add(self.circle,self.diameter)

class RadianCircleVisual(VGroup):
    def __init__(self,angle=PI/3,center=(-2.7,.3,0),radius=1.65,**kwargs):
        super().__init__(**kwargs);self.theta=ValueTracker(angle);self.center=np.array(center);self.radius=radius
        self.circle=Circle(radius=radius,color=GOLD,stroke_width=2).move_to(center)
        self.base=Line(self.center,self.center+RIGHT*radius,color=MUTED,stroke_width=2)
        self.arc=always_redraw(lambda:Arc(radius=radius,start_angle=0,angle=max(self.theta.get_value(),1e-6),arc_center=self.center,color=TEAL,stroke_width=6))
        self.ray=always_redraw(lambda:Line(self.center,self.point(),color=GRAY,stroke_width=3))
        self.dot=always_redraw(lambda:Dot(self.point(),color=WHITE_INK,radius=.065))
        self.angle_arc=always_redraw(lambda:Arc(radius=.38,start_angle=0,angle=max(self.theta.get_value(),1e-6),arc_center=self.center,color=GOLD,stroke_width=2))
        self.add(self.circle,self.base,self.arc,self.angle_arc,self.ray,self.dot)
    def point(self):
        t=self.theta.get_value();return self.center+self.radius*np.array([np.cos(t),np.sin(t),0])
    def length_labels(self):
        r=math('r',31,GRAY).move_to(self.center+RIGHT*self.radius*.52+DOWN*.25)
        s=always_redraw(lambda:math('s',31,TEAL).move_to(self.center+(self.radius+.28)*np.array([np.cos(self.theta.get_value()/2),np.sin(self.theta.get_value()/2),0])))
        return VGroup(r,s)

class UnitCircleVisual(VGroup):
    def __init__(self,angle=0,components=False,**kwargs):
        super().__init__(**kwargs);self.theta=ValueTracker(angle)
        self.axes=Axes(x_range=[-1.5,1.5,.5],y_range=[-1.5,1.5,.5],x_length=4.8,y_length=4.8,axis_config={'color':'#738197','include_tip':False,'include_ticks':False}).move_to([-2.7,.3,0])
        self.origin=self.axes.c2p(0,0)
        self.circle=Circle(radius=1.6,color=GOLD,stroke_width=3).move_to(self.origin)
        self.ray=always_redraw(lambda:Arrow(self.origin,self.point(),buff=0,color=GRAY,stroke_width=4))
        self.dot=always_redraw(lambda:Dot(self.point(),color=GOLD,radius=.07))
        self.angle_arc=always_redraw(lambda:Arc(radius=.35,angle=max(self.theta.get_value()%TAU,1e-6),arc_center=self.origin,color=GOLD,stroke_width=2))
        self.add(self.axes,self.circle,self.angle_arc,self.ray,self.dot)
        self.components=VGroup(
            always_redraw(lambda:Line(self.origin,self.axes.c2p(np.cos(self.theta.get_value())+1e-8,0),color=BLUE,stroke_width=6)),
            always_redraw(lambda:Line(self.axes.c2p(np.cos(self.theta.get_value()),0),self.point()+UP*1e-8,color=PURPLE,stroke_width=5)),
            always_redraw(lambda:DashedLine(self.axes.c2p(0,np.sin(self.theta.get_value())),self.point()+RIGHT*1e-8,color=BLUE,stroke_width=1.5,dash_length=.08)))
        if components:self.add(self.components)
    def point(self):
        t=self.theta.get_value();return self.axes.c2p(np.cos(t),np.sin(t))

def numeric_panel(u):
    g=VGroup()
    for func,name,c,y in [(np.cos,r'\cos\theta',BLUE,1.6),(np.sin,r'\sin\theta',PURPLE,-.6)]:
        label=math(name,38,c).move_to([2.25,y+.55,0])
        number=DecimalNumber(0,num_decimal_places=2,include_sign=True,font_size=36,color=c).move_to([4.65,y+.55,0])
        number.add_updater(lambda m,f=func:m.set_value(0 if abs(f(u.theta.get_value()))<.0001 else f(u.theta.get_value())))
        origin=np.array([3.4,y,0])
        line=Line(origin+LEFT*1.4,origin+RIGHT*1.4,color=MUTED,stroke_width=2)
        bar=always_redraw(lambda f=func,p=origin,col=c:Line(p,p+RIGHT*(1.4*f(u.theta.get_value())+1e-8),color=col,stroke_width=7))
        labels=VGroup(*[math(s,20,MUTED).move_to(origin+[x,-.35,0]) for s,x in [('-1',-1.4),('0',0),('1',1.4)]])
        g.add(label,number,line,bar,labels)
    return g
def coordinate_panel():
    eq=MathTex(r'P(\theta)=({{\cos\theta}},{{\sin\theta}})',font_size=44).move_to([2.8,1.6,0])
    eq.set_color_by_tex(r'\cos\theta',BLUE);eq.set_color_by_tex(r'\sin\theta',PURPLE)
    x=math(r'\cos\theta=\frac{x}{1}=x',42,BLUE).move_to([2.8,.1,0])
    y=math(r'\sin\theta=\frac{y}{1}=y',42,PURPLE).move_to([2.8,-1.25,0])
    return VGroup(eq,x,y)
def two_circles():
    result=VGroup()
    for radius,x,label in [(.85,-3.2,'r'),(1.7,3,'2r')]:
        c=Circle(radius=radius,color=GOLD,stroke_width=4).move_to([x,.4,0])
        line=Line(c.get_center(),c.get_center()+RIGHT*radius,color=GRAY,stroke_width=2)
        t=math(label,30,GRAY).move_to(c.get_center()+RIGHT*radius*.5+DOWN*.28)
        result.add(VGroup(c,line,t))
    return result
def ratio_end():
    circles=two_circles()
    for g in circles:
        g.remove(g[1],g[2]);g.scale(.65)
    pi=math(r'\pi',105,GOLD).move_to([0,.4,0])
    return circles,pi
def relation_state():
    c=CircleRatioVisual(1.35,[-2.5,.2,0])
    eq=math(r'C=\pi d=2\pi r',59,GOLD).move_to([2.5,.3,0])
    return c,eq
def degrees_end():
    v=RadianCircleVisual(1.2);labels=v.length_labels()
    eq=math(r'\frac{s}{r}',70,TEAL).move_to([2.7,.8,0])
    name=txt('라디안 · radian',26,MUTED).move_to([2.7,-1.2,0])
    return v,labels,eq,name
def turns_end():
    v=RadianCircleVisual(PI)
    eq=math(r'\frac{\pi}{2}\quad\pi\quad2\pi',59,GOLD).move_to([2.7,.5,0])
    name=txt('회전의 크기를 나타내는 수',24,MUTED).move_to([2.7,-.8,0])
    return v,eq,name
def unit_end():
    u=UnitCircleVisual(0)
    one=math('1',30,GRAY).move_to(u.origin+[.8,-.25,0])
    point=math('(1,0)',28).next_to(u.point(),DOWN,buff=.22)
    title=txt('단위원 · Unit Circle',28,GOLD).move_to([2.7,1,0])
    radius=math('r=1',50).move_to([2.7,-.2,0])
    return u,VGroup(one,point,title,radius)
def question_end():
    u=UnitCircleVisual(PI)
    q=math(r'\times\,?',100).move_to([2.7,.3,0])
    return u,q

class ChapterScene(IntroScene):
    index=1
    def play_for(self,t,*animations,**kwargs):
        self.play(*animations,run_time=t,**kwargs)
    def construct(self):
        record=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
        self.caption=VGroup();self.caption_index=-1;self.caption_audit=[]
        self.caption_driver=VMobject().add_updater(lambda m,dt:self.update_caption())
        self.add(self.caption_driver);self.update_caption()
        getattr(self,record['method'])()
        self.to(self.total_duration);self.caption_driver.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def opening(self):
        c=Circle(radius=1.5,color=GOLD,stroke_width=4).shift(LEFT*1.5)
        pi=math(r'\pi',110,GOLD).move_to([2.7,.3,0]);self.add(c,pi)
        self.to(5);self.play_for(1.5,FadeOut(pi),c.animate.move_to(ORIGIN));self.to(8)
    def two_circles(self):
        old=Circle(radius=1.5,color=GOLD,stroke_width=4);self.add(old)
        g=two_circles();self.play_for(1.5,Transform(old,g[0][0]),FadeIn(g[1][0]))
        self.remove(old);self.add(g[0][0]);self.to(3)
        self.play_for(.7,FadeIn(g[0][1:]),FadeIn(g[1][1:]))
        dots=VGroup(*[Dot(x[0].point_at_angle(0),radius=.06,color=TEAL) for x in g]);self.add(dots)
        self.play_for(2.6,*[MoveAlongPath(d,c[0],rate_func=linear) for d,c in zip(dots,g)])
        self.play_for(.7,FadeOut(dots));self.to(7)
        self.play_for(.8,*[Indicate(c[0],color=GOLD,scale_factor=1.02) for c in g]);self.to(9)
    def ratio(self):
        g=two_circles();self.add(g)
        markings=VGroup();eqs=VGroup()
        for k,c in enumerate(g,1):
            center=c[0].get_center();r=c[0].radius
            markings.add(VGroup(Line(center+LEFT*r,center+RIGHT*r,color=GRAY),math(f'd_{k}',28,GRAY).move_to(center+DOWN*.3),math(f'C_{k}',29,GOLD).next_to(c[0],UP,buff=.15)))
            eqs.add(math(r'\frac{C_'+str(k)+r'}{d_'+str(k)+'}',58).move_to([center[0],-2.05,0]))
        self.play_for(1,FadeOut(g[0][1:]),FadeOut(g[1][1:]),FadeIn(markings),FadeIn(eqs));self.to(4)
        approx=VGroup(*[math(r'\approx3.14159',50,GOLD).move_to(e) for e in eqs])
        self.play_for(1.2,*[TransformMatchingTex(a,b) for a,b in zip(eqs,approx)])
        self.to(8)
        end,pi=ratio_end()
        self.play_for(1.2,Transform(g[0][0],end[0][0]),Transform(g[1][0],end[1][0]),FadeOut(markings),FadeOut(approx),FadeIn(pi));self.to(11)
    def relation(self):
        old,pi=ratio_end();self.add(old,pi)
        decimal=math(r'\pi=3.14159265358979323846\ldots',56,GOLD).move_to([0,.5,0])
        self.play_for(1,FadeOut(old),TransformMatchingTex(pi,decimal));self.to(5)
        c,eq=relation_state();self.play_for(1,FadeOut(decimal),FadeIn(c),FadeIn(eq))
        self.play_for(1.3,c.animate.scale(.7));self.play_for(1.3,c.animate.scale(1/.7));self.to(10)
    def motion(self):
        c,eq=relation_state();self.add(c,eq);v=RadianCircleVisual(0)
        self.play_for(1.2,FadeOut(eq),FadeOut(c),FadeIn(v.circle),FadeIn(v.base));self.to(5)
        self.add(v);self.play_for(2,v.theta.animate.set_value(PI/7),rate_func=linear)
        self.play_for(5,v.theta.animate.set_value(PI/3),rate_func=linear)
        theta=math(r'\theta',80,GOLD).move_to([2.7,.8,0]);self.play_for(.7,FadeIn(theta));self.to(16)
    def degrees(self):
        v=RadianCircleVisual(PI/3);theta=math(r'\theta',80,GOLD).move_to([2.7,.8,0]);self.add(v,theta)
        ninety=math(r'90^\circ',70,GOLD).move_to(theta)
        self.play_for(1.4,v.theta.animate.set_value(PI/2),TransformMatchingTex(theta,ninety))
        half=math(r'180^\circ',70,GOLD).move_to(theta)
        self.play_for(1.4,v.theta.animate.set_value(PI),TransformMatchingTex(ninety,half));self.to(4)
        labels=v.length_labels();fraction=math(r'\frac{s}{r}',70,TEAL).move_to(theta)
        self.play_for(1,TransformMatchingTex(half,fraction),FadeIn(labels))
        self.play_for(3.7,v.theta.animate.set_value(1.2));self.to(9)
        self.play_for(.6,FadeIn(txt('라디안 · radian',26,MUTED).move_to([2.7,-1.2,0])));self.to(10)
    def radian(self):
        v,labels,old,name=degrees_end();self.add(v,labels,old,name)
        eq=math(r'\theta=\frac{s}{r}',70,GOLD).move_to(old)
        self.play_for(.8,TransformMatchingTex(old,eq))
        self.play_for(5.7,v.theta.animate.set_value(1),rate_func=linear);self.to(7)
        result=math(r's=r\quad\Longrightarrow\quad\theta=1\,\mathrm{rad}',42,TEAL).move_to([2.7,-.2,0])
        label=math(r'1\,\mathrm{rad}',28,GOLD).move_to(v.center+[.8,.6,0])
        self.play_for(.8,FadeIn(result),FadeIn(label));self.to(11)
    def turns(self):
        v=RadianCircleVisual(1);labels=v.length_labels();old=math(r'\theta=\frac{s}{r}',70,GOLD).move_to([2.7,.8,0]);self.add(v,labels,old)
        self.play_for(.6,FadeOut(labels),v.theta.animate.set_value(0))
        full=math(r'\frac{2\pi r}{r}=2\pi\,\mathrm{rad}',51,GOLD).move_to(old)
        self.play_for(.7,TransformMatchingTex(old,full))
        self.play_for(3.7,v.theta.animate.set_value(TAU),rate_func=linear);self.to(5)
        v.theta.set_value(0)
        half=math(r'\frac{\pi r}{r}=\pi\,\mathrm{rad}',51,GOLD).move_to(full)
        self.play_for(2,v.theta.animate.set_value(PI),TransformMatchingTex(full,half),rate_func=linear);self.to(8)
        _,eq,name=turns_end();self.play_for(.8,TransformMatchingTex(half,eq),FadeIn(name));self.to(11)
    def unit(self):
        v,eq,name=turns_end();self.add(v,eq,name);self.to(4)
        u,extra=unit_end();self.play_for(1.3,FadeOut(v),FadeOut(eq),FadeOut(name),FadeIn(u),FadeIn(extra[0]),FadeIn(extra[1]))
        self.to(7);self.play_for(.7,FadeIn(extra[2]),FadeIn(extra[3]));self.to(9)
    def coordinates(self):
        u,extra=unit_end();self.add(u,extra)
        self.play_for(.8,FadeOut(extra));self.play_for(2.2,u.theta.animate.set_value(PI/4),rate_func=linear)
        generic=math('P=(x,y)',55).move_to([2.8,1.6,0]);self.play_for(.7,FadeIn(u.components),FadeIn(generic));self.to(6)
        panel=coordinate_panel();self.play_for(1,TransformMatchingTex(generic,panel[0]),FadeIn(panel[1]),FadeIn(panel[2]));self.to(11)
    def functions(self):
        u=UnitCircleVisual(PI/4,components=True);old=coordinate_panel();self.add(u,old)
        panel=numeric_panel(u)
        self.play_for(1,FadeOut(old),FadeIn(panel),u.theta.animate.set_value(0))
        self.play_for(17,u.theta.animate.set_value(TAU),rate_func=linear)
    def multiplication(self):
        u=UnitCircleVisual(TAU,components=True);panel=numeric_panel(u);self.add(u,panel)
        pair=MathTex(r'({{\cos\theta}},{{\sin\theta}})',font_size=55).move_to([2.7,1.3,0]);pair.set_color_by_tex(r'\cos\theta',BLUE);pair.set_color_by_tex(r'\sin\theta',PURPLE)
        self.play_for(.8,FadeOut(panel),FadeIn(pair));self.to(2)
        box=SurroundingRectangle(pair,color=MUTED,buff=.3);q=math(r'\times\,?',75).move_to([2.7,-.3,0])
        self.play_for(.7,Create(box),FadeIn(q))
        self.play_for(3.3,u.theta.animate.set_value(TAU+PI/2),rate_func=linear)
        self.play_for(.6,FadeOut(pair),FadeOut(box),FadeOut(u.components),q.animate.scale(100/75).move_to([2.7,.3,0]))
        self.play_for(3.4,u.theta.animate.set_value(TAU+PI),rate_func=linear)
    def imaginary(self):
        u,q=question_end();self.add(u,q)
        question=math('?',100).move_to(q)
        self.play_for(.8,TransformMatchingTex(q,question))
        self.play_for(1.2,u.theta.animate.set_value(0))
        i=math('i',110,PURPLE).move_to(question);self.play_for(1,TransformMatchingTex(question,i));self.to(4)
        eq=MathTex(r'i^2=-1',substrings_to_isolate=['i'],font_size=90).move_to([2.7,.3,0]);eq.set_color_by_tex('i',PURPLE)
        self.play_for(1,TransformMatchingTex(i,eq),FadeIn(txt('복소수와 회전',25,MUTED).move_to([2.7,-1.2,0])));self.to(8)
