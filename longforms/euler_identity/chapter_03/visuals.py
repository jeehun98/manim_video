from pathlib import Path
import json,sys,re
from manim import *
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import IntroScene,txt,math,GOLD,TEAL,PURPLE,MUTED,WHITE_INK,exponential
from longforms.euler_identity.chapter_02.visuals import UnitCircleVisual
BLUE='#7DA8F9';GRAY='#DCE3EE'
def cmath(s,size=58):
    # Isolate the symbol i without splitting TeX commands such as \times or \rightarrow.
    marked=re.sub(r'\\[A-Za-z]+|i',lambda m:'{{i}}' if m.group()=='i' else m.group(),s)
    m=MathTex(marked,font_size=size);m.set_color_by_tex('i',PURPLE);return m
def wide_axes(labels=True):
    a=Axes(x_range=[-4,4,1],y_range=[-4,4,1],x_length=5.2,y_length=5.2,axis_config={'include_tip':False,'include_ticks':False}).move_to([-2.7,.3,0])
    a.x_axis.set_color(GRAY);a.y_axis.set_color(PURPLE)
    if labels:a.add(txt('Re',21,GRAY).next_to(a.x_axis,RIGHT,buff=.1),txt('Im',21,PURPLE).next_to(a.y_axis,UP,buff=.08))
    return a
class ComplexRotationVisual(UnitCircleVisual):
    def __init__(self,angle=0,**kwargs):
        super().__init__(angle,**kwargs)
        self.axes.x_axis.set_color(GRAY);self.axes.y_axis.set_color(PURPLE)
        self.remove(self.ray,self.dot,self.angle_arc)
        self.ray=always_redraw(lambda:Arrow(self.origin,self.point(),buff=0,color=BLUE,stroke_width=5))
        self.trail=always_redraw(lambda:Arc(radius=1.6,start_angle=0,angle=max(self.theta.get_value(),1e-6),arc_center=self.origin,color=TEAL,stroke_width=3))
        self.add(self.trail,self.ray,self.dot)
        self.labels=VGroup(txt('Re',21,GRAY).next_to(self.axes.x_axis,RIGHT,buff=.08),txt('Im',21,PURPLE).next_to(self.axes.y_axis,UP,buff=.08))
        for text,pos,c in [('1',[1.85,-.25,0],GRAY),('i',[.25,1.85,0],PURPLE),('-1',[-1.95,-.25,0],GRAY),('-i',[.3,-1.85,0],PURPLE)]:self.labels.add(math(text,29,c).move_to(self.origin+pos))
        self.add(self.labels)
class GeneralVisual(VGroup):
    def __init__(self,angle=0,result=False,**kwargs):
        super().__init__(**kwargs);self.theta=ValueTracker(angle);self.axes=wide_axes();self.origin=self.axes.c2p(0,0)
        self.original=np.array([2.,3.]);self.start=self.axes.c2p(*self.original)
        self.original_ray=Arrow(self.origin,self.start,buff=0,color=BLUE,stroke_width=5)
        self.projections=VGroup(Line(self.origin,self.axes.c2p(2,0),color=BLUE,stroke_width=3),DashedLine(self.axes.c2p(2,0),self.start,color=PURPLE,stroke_width=3))
        self.ab=VGroup(math('a',28,BLUE).move_to(self.axes.c2p(1,0)+DOWN*.25),math('b',28,PURPLE).move_to(self.axes.c2p(2,1.5)+RIGHT*.2),math('(a,b)',29,BLUE).next_to(self.start,UP,buff=.15))
        self.target=self.axes.c2p(-3,2)
        self.target_ray=Arrow(self.origin,self.target,buff=0,color=GOLD,stroke_width=3)
        self.target_label=math('(-b,a)',29,GOLD).next_to(self.target,UP,buff=.15)
        self.moving=always_redraw(lambda:Arrow(self.origin,self.point(),buff=0,color=GOLD,stroke_width=5))
        initial=np.arctan2(3,2);radius=np.linalg.norm(self.start-self.origin)
        self.arc=always_redraw(lambda:Arc(radius=radius,start_angle=initial,angle=max(self.theta.get_value(),1e-6),arc_center=self.origin,color=TEAL,stroke_width=3))
        self.add(self.axes,self.projections,self.original_ray,self.ab)
        if result:self.add(self.target_ray,self.target_label)
    def point(self):
        t=self.theta.get_value();a,b=self.original
        return self.axes.c2p(a*np.cos(t)-b*np.sin(t),a*np.sin(t)+b*np.cos(t))
def real_state():
    line=NumberLine(x_range=[-3,3,1],length=10.5,include_numbers=True,font_size=25,color=GRAY).move_to([0,-.5,0])
    title=txt('실수 · Real Numbers',30,GRAY).move_to([0,1.6,0]);return VGroup(line,title)
def graph_state():
    axes=Axes(x_range=[-2.5,2.5,1],y_range=[-1.5,4.5,1],x_length=4.5,y_length=3.6,axis_config={'include_tip':False,'include_ticks':False,'color':MUTED}).move_to([-2.7,.2,0])
    curve=axes.plot(lambda x:x*x,x_range=[-2,2],color=BLUE,stroke_width=4)
    negative=Line(axes.c2p(-2.5,-1),axes.c2p(2.5,-1),color=GOLD,stroke_width=3)
    example=VGroup(math('2^2=4',40).move_to([-2.4,3,0]),math('(-2)^2=4',40).move_to([2.4,3,0]))
    bound=math(r'x^2\geq0\quad(x\in\mathbb R)',43,BLUE).move_to([2.7,1.7,0])
    eq=math('x^2=-1',68).move_to([2.7,.3,0]);no=txt('실수해 없음',29,GOLD).move_to([2.7,-1,0])
    lab=math('y=-1',27,GOLD).next_to(negative,DOWN,buff=.12)
    return VGroup(axes,curve,negative,example,bound,eq,no,lab)
def imaginary_state():
    plane=wide_axes(False);eq=cmath('i^2=-1',88).move_to([2.7,1.4,0]);name=txt('허수 단위 · Imaginary Unit',25,MUTED).move_to([2.7,.1,0]);return plane,eq,name
def definition_state():
    plane=wide_axes(False)
    points=VGroup(Dot(plane.c2p(1,1),color=BLUE,radius=.06),Dot(plane.c2p(2,3),color=GOLD,radius=.06))
    examples=VGroup(cmath('1+i',52).move_to([2.7,2.1,0]),cmath('2+3i',52).move_to([2.7,1.1,0]))
    eq=cmath('z=a+bi',61).move_to([2.7,-.1,0])
    name=txt('복소수 · Complex Number',24,MUTED).move_to([2.7,-1,0])
    parts=txt('실수부 a · 허수부 b',23,MUTED).move_to([2.7,-1.6,0])
    return VGroup(plane,points,examples,eq,name,parts)
def point_state():
    plane=wide_axes();origin=plane.c2p(0,0);p=plane.c2p(2,3)
    grid=VGroup(*[Line(plane.c2p(x,-4),plane.c2p(x,4),color='#465469',stroke_width=1,stroke_opacity=.3) for x in [-3,-2,-1,1,2,3]],*[Line(plane.c2p(-4,y),plane.c2p(4,y),color='#465469',stroke_width=1,stroke_opacity=.3) for y in [-3,-2,-1,1,2,3]])
    path=VGroup(Line(origin,plane.c2p(2,0),color=BLUE,stroke_opacity=.4),Line(plane.c2p(2,0),p,color=PURPLE,stroke_opacity=.4))
    ray=Arrow(origin,p,buff=0,color=BLUE,stroke_width=5);dot=Dot(p,color=GOLD,radius=.065)
    label=cmath('2+3i',32).next_to(p,RIGHT,buff=.15)
    mapping=cmath(r'2+3i\longleftrightarrow(2,3)',47).move_to([2.8,.8,0])
    title=txt('복소평면 · Complex Plane',27).move_to([0,3.4,0])
    return VGroup(grid,plane,path,ray,dot,label,mapping,title)
def one_panel():return cmath(r'1=1+0i\longleftrightarrow(1,0)',43).move_to([2.8,.8,0])
def cycle_panel():return VGroup(cmath(r'1\to i\to-1\to-i\to1',43).move_to([2.8,1.4,0]),cmath(r'\times i\ \longrightarrow\ +90^\circ',53).move_to([2.8,-.3,0]))
def algebra_panel():
    top=cmath('i(a+bi)=ai+bi^2',44).move_to([2.8,1.8,0])
    middle=cmath('=ai-b=-b+ai',44).move_to([2.8,.6,0])
    mapping=math(r'(a,b)\longmapsto(-b,a)',49,GOLD).move_to([2.8,-1,0])
    return VGroup(top,middle,mapping)
def rotation_end():
    g=GeneralVisual(PI/2,result=True);g.add(g.arc,g.moving)
    panel=VGroup(math(r'(a,b)\longmapsto(-b,a)',49,GOLD).move_to([2.8,-1,0]),math(r'90^\circ',80,GOLD).move_to([2.8,1,0]))
    return g,panel
def half_end():
    u=ComplexRotationVisual(PI)
    eq=cmath('i^2=-1',85).move_to([2.7,.8,0]);note=txt('두 번의 회전 = 부호 반전',25,MUTED).move_to([2.7,-.9,0])
    return u,eq,note
def continuous_end():
    u=ComplexRotationVisual(PI/3);q=math(r'\times\,?',95).move_to([2.7,.5,0]);note=txt('임의의 각도 θ만큼 회전',25,MUTED).move_to([2.7,-1,0]);return u,q,note

class ChapterScene(IntroScene):
    index=1
    def play_for(self,t,*animations,**kwargs):self.play(*animations,run_time=t,**kwargs)
    def construct(self):
        record=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
        self.caption=VGroup();self.caption_index=-1;self.caption_audit=[]
        self.caption_driver=VMobject().add_updater(lambda m,dt:self.update_caption());self.add(self.caption_driver);self.update_caption()
        getattr(self,record['method'])();self.to(self.total_duration);self.caption_driver.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def opening(self):
        u=UnitCircleVisual(0);eq=cmath('i^2=-1',90).move_to([2.7,.3,0]);name=txt('복소수와 회전',25,MUTED).move_to([2.7,-1.2,0]);self.add(u,eq,name)
        self.play_for(3,u.theta.animate.set_value(PI/3),rate_func=linear);self.to(4)
        q=math(r'\times\,?',100).move_to(eq)
        self.play_for(1,TransformMatchingTex(eq,q),FadeOut(name));self.to(8)
        real=real_state();self.play_for(1.5,FadeOut(u),FadeOut(q),FadeIn(real));self.to(12)
    def real_square(self):
        real=real_state();self.add(real);g=graph_state()
        self.play_for(1,FadeOut(real),FadeIn(g[3]));self.to(4)
        self.play_for(1.3,Create(g[0]),Create(g[1]),FadeIn(g[4]));self.to(8)
        self.play_for(1,Create(g[2]),FadeIn(g[5]),FadeIn(g[6]),FadeIn(g[7]));self.to(13)
    def imaginary_unit(self):
        g=graph_state();self.add(g);old=g[5]
        self.play_for(1.5,*[FadeOut(x) for k,x in enumerate(g) if k!=5],old.animate.move_to([0,.8,0]));self.to(3)
        eq=cmath('i^2=-1',88).move_to(old);name=txt('허수 단위 · Imaginary Unit',25,MUTED).move_to([0,-.5,0])
        self.play_for(1,TransformMatchingTex(old,eq),FadeIn(name));self.to(7)
        real=real_state();real.remove(real[1]);hover=math('i',45,PURPLE).move_to([-2,.1,0])
        self.play_for(.6,eq.animate.move_to([2.7,1.4,0]),name.animate.move_to([2.7,.1,0]),FadeIn(real),FadeIn(hover))
        self.play_for(2,hover.animate.move_to([1,.1,0]));self.to(11)
        plane,_,_=imaginary_state()
        self.play_for(1,FadeOut(real),FadeOut(hover),Create(plane.x_axis))
        self.play_for(2,Create(plane.y_axis));self.to(17)
    def complex_numbers(self):
        plane,eq,name=imaginary_state();self.add(plane,eq,name);d=definition_state()
        self.play_for(1,FadeOut(eq),FadeOut(name),FadeIn(d[1]),FadeIn(d[2]));self.to(7)
        self.play_for(1,FadeIn(d[3]),FadeIn(d[4]),FadeIn(d[5]));self.to(11)
    def complex_plane(self):
        d=definition_state();self.add(d);generic=cmath(r'a+bi\longleftrightarrow(a,b)',47).move_to([2.8,.8,0])
        self.play_for(1,FadeOut(d[1]),FadeOut(d[2]),FadeOut(d[3]),FadeOut(d[4]),FadeOut(d[5]),FadeIn(generic));self.to(3)
        p=point_state();self.play_for(1,FadeIn(p[0]),Transform(d[0],p[1]),TransformMatchingTex(generic,p[6]));self.to(7)
        dot=Dot(p[1].c2p(0,0),color=GOLD,radius=.065);self.add(dot)
        self.play_for(2,dot.animate.move_to(p[1].c2p(2,0)),Create(p[2][0]),rate_func=linear)
        self.play_for(2.3,dot.animate.move_to(p[1].c2p(2,3)),Create(p[2][1]),rate_func=linear)
        self.play_for(.7,FadeIn(p[5]));self.to(12)
        self.play_for(1,Create(p[3]),FadeIn(p[7]));self.to(16)
    def one(self):
        old=point_state();self.add(old);u=ComplexRotationVisual(0);panel=one_panel()
        self.play_for(1.2,FadeOut(old),FadeIn(u),FadeIn(panel));self.to(7)
    def first_turn(self):
        u=ComplexRotationVisual(0);old=one_panel();self.add(u,old)
        eq=cmath(r'1\times i',75).move_to([2.8,.8,0]);self.play_for(.8,TransformMatchingTex(old,eq));self.to(2)
        result=cmath(r'1\times i=i',75).move_to(eq)
        ghost=Arrow(u.origin,u.origin+RIGHT*1.6,buff=0,color=GOLD,stroke_width=3,stroke_opacity=.4);self.add(ghost)
        self.play_for(3,u.theta.animate.set_value(PI/2),TransformMatchingTex(eq,result),rate_func=linear)
        self.to(8.5);self.play_for(.5,FadeOut(ghost));self.to(9)
    def four_turns(self):
        u=ComplexRotationVisual(PI/2);old=cmath(r'1\times i=i',75).move_to([2.8,.8,0]);self.add(u,old)
        eq=cmath(r'i\times i=-1',70).move_to(old);self.play_for(1,TransformMatchingTex(old,eq));self.to(2)
        self.play_for(3,u.theta.animate.set_value(PI),rate_func=linear);self.to(6)
        next_eq=cmath(r'-1\times i=-i',70).move_to(eq)
        self.play_for(1.8,u.theta.animate.set_value(3*PI/2),TransformMatchingTex(eq,next_eq),rate_func=linear)
        last=cmath(r'-i\times i=1',70).move_to(eq)
        self.play_for(1.8,u.theta.animate.set_value(TAU),TransformMatchingTex(next_eq,last),rate_func=linear);self.to(10)
        panel=cycle_panel();self.play_for(1,FadeOut(last),FadeIn(panel));self.to(16)
    def general(self):
        u=ComplexRotationVisual(TAU);panel=cycle_panel();self.add(u,panel);self.to(4)
        g=GeneralVisual();coord=math('(a,b)',62,BLUE).move_to([2.8,.8,0]);self.play_for(1.2,FadeOut(u),FadeOut(panel),FadeIn(g),FadeIn(coord));self.to(8)
        z=cmath('z=a+bi',68).move_to(coord);self.play_for(1,TransformMatchingTex(coord,z));self.to(11)
    def algebra(self):
        g=GeneralVisual();old=cmath('z=a+bi',68).move_to([2.8,.8,0]);self.add(g,old);p=algebra_panel()
        self.play_for(1,TransformMatchingTex(old,p[0]));self.to(4)
        rule=cmath('i^2=-1',45).move_to([2.8,-.8,0]);self.play_for(.7,FadeIn(rule));self.play_for(1,FadeIn(p[1]));self.to(9)
        self.play_for(1,FadeOut(rule),FadeIn(p[2]),FadeIn(g.target_ray),FadeIn(g.target_label));self.to(13)
    def rotation(self):
        g=GeneralVisual(result=True);p=algebra_panel();self.add(g,p)
        degree=math(r'90^\circ',80,GOLD).move_to([2.8,1,0]);self.play_for(.7,FadeOut(p[0]),FadeOut(p[1]),FadeIn(degree))
        self.add(g.arc,g.moving);self.play_for(4,g.theta.animate.set_value(PI/2),rate_func=linear)
        self.play_for(.8,Indicate(g.target_ray,color=GOLD,scale_factor=1));self.to(7)
    def half_turn(self):
        g,p=rotation_end();self.add(g,p);conclusion=cmath(r'\times i\ \longleftrightarrow\ 90^\circ',53).move_to([2.8,.9,0])
        self.play_for(1,TransformMatchingTex(p[1],conclusion));self.to(6)
        u=ComplexRotationVisual(0);count=math(r'90^\circ+90^\circ=180^\circ',46,GOLD).move_to([2.7,1.4,0])
        self.play_for(.8,FadeOut(g),FadeOut(p[0]),FadeOut(conclusion),FadeIn(u),FadeIn(count))
        self.play_for(2,u.theta.animate.set_value(PI/2),rate_func=linear);self.play_for(2,u.theta.animate.set_value(PI),rate_func=linear)
        _,eq,note=half_end();self.play_for(.8,FadeOut(count),FadeIn(eq),FadeIn(note));self.to(15)
    def continuous(self):
        u,old,note=half_end();self.add(u,old,note);self.to(3)
        label=cmath(r'\times i\ \longrightarrow\ 90^\circ',58).move_to([2.7,.7,0])
        integer=txt('정수 거듭제곱 iⁿ: 90° 단위',23,MUTED).move_to([2.7,-1.1,0])
        self.play_for(.6,FadeOut(note),TransformMatchingTex(old,label),FadeIn(integer),u.theta.animate.set_value(0))
        self.play_for(1.6,u.theta.animate.set_value(PI/2),rate_func=linear);self.to(7)
        self.play_for(.4,FadeOut(integer),FadeOut(label))
        current=math(r'30^\circ',75,GOLD).move_to([2.7,.7,0]);self.add(current)
        for k,angle in enumerate([30,15,5,1]):
            new=math(str(angle)+r'^\circ',75,GOLD).move_to(current)
            self.play_for(1.1,u.theta.animate.set_value(angle*DEGREES),TransformMatchingTex(current,new),rate_func=linear);current=new
        self.to(13)
        q=math(r'\times\,?',95).move_to([2.7,.5,0]);newnote=txt('임의의 각도 θ만큼 회전',25,MUTED).move_to([2.7,-1,0])
        self.play_for(.6,FadeOut(current),FadeIn(q),FadeIn(newnote))
        self.play_for(4.4,u.theta.animate.set_value(PI/3),rate_func=linear)
    def e_transition(self):
        u,q,note=continuous_end();self.add(u,q,note)
        e=math('e',110,TEAL).move_to([2.7,.5,0]);self.play_for(1.5,TransformMatchingTex(q,e),FadeOut(note));self.to(3)
        curve=exponential(.9)[1].move_to([2.2,.3,0]).set_stroke(opacity=.2)
        self.play_for(1.5,FadeOut(u),e.animate.scale(140/110).move_to([0,.3,0]),Create(curve));self.to(6)
