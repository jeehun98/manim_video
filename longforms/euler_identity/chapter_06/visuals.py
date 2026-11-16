from pathlib import Path
import sys,json
from manim import *
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import txt,math,identity,identity_title,SYMS,COLORS,GOLD,TEAL,PURPLE,MUTED,WHITE_INK
from longforms.euler_identity.chapter_05.visuals import ChapterScene as PreviousScene,OrbitVisual,formula_end,euler_eq,fit,BLUE,GRAY

def equation(s,size=70,y=2.8):
    m=MathTex(s,substrings_to_isolate=['e','i',r'\pi',r'\theta',r'\cos',r'\sin'],font_size=size)
    for t,c in [('e',TEAL),('i',PURPLE),(r'\pi',GOLD),(r'\theta',GOLD),(r'\cos',BLUE),(r'\sin',PURPLE)]:m.set_color_by_tex(t,c,substring=False)
    return fit(m,12.5).move_to([0,y,0])
def pi_equation():return equation(r'e^{i\pi}=\cos\pi+i\sin\pi')
def half_orbit(angle=0):
    u=OrbitVisual(angle,center=(-2.7,.1,0),unit=1.7)
    # Keep the original coordinate transform, but shorten the visible axes so
    # the vertical axis and its label cannot touch the formula above the plot.
    u.axes.set_stroke(opacity=0)
    short=VGroup(Line(u.axes.c2p(-1.25,0),u.axes.c2p(1.25,0),color=GRAY),Line(u.axes.c2p(0,-1.25),u.axes.c2p(0,1.25),color=GRAY))
    u.add_to_back(short)
    return u
def endpoints(u):
    return VGroup(math('1',32).move_to(u.axes.c2p(1,0)+DOWN*.35),math('-1',32).move_to(u.axes.c2p(-1,0)+DOWN*.35),txt('Re',22,BLUE).move_to(u.o+RIGHT*2.5),txt('Im',22,PURPLE).move_to(u.o+UP*1.95+LEFT*.35))
def half_state():
    u=half_orbit(PI);u.arc.set_color(GOLD)
    return u,pi_equation(),endpoints(u)
def bare_result():return equation(r'e^{i\pi}=-1',100,.65)
def constants():return VGroup(*[math(s,68,c).move_to([-4.8+2.4*k,1.9,0]) for k,(s,c) in enumerate(zip(SYMS,COLORS))])

class MiniGrowth(VGroup):
    def __init__(self,center=(4.8,-.5,0),width=1.9,height=1.4,x=.7,**kwargs):
        super().__init__(**kwargs);self.x=ValueTracker(x)
        self.axes=Axes(x_range=[-1,1,1],y_range=[0,3,1],x_length=width,y_length=height,axis_config={'color':GRAY,'include_ticks':False,'include_tip':False}).move_to(center)
        self.curve=self.axes.plot(lambda t:np.exp(t),x_range=[-1,1],color=TEAL,stroke_width=3)
        self.dot=always_redraw(lambda:Dot(self.axes.c2p(self.x.get_value(),np.exp(self.x.get_value())),radius=.045,color=GOLD))
        def tangent():
            t=self.x.get_value();v=np.exp(t);d=.18
            return Line(self.axes.c2p(t-d,v-v*d),self.axes.c2p(t+d,v+v*d),color=GOLD,stroke_width=3)
        self.tangent=always_redraw(tangent);self.add(self.axes,self.curve,self.tangent,self.dot)

def meaning_state():
    syms=constants();labels=VGroup(*[txt(s,25,c).move_to([-4.8+2.4*k,.85,0]) for k,(s,c) in enumerate(zip(['덧셈','곱셈','기하학','회전','변화'],COLORS))])
    p=OrbitVisual(PI,center=(0,-.65,0),unit=.62);q=OrbitVisual(PI/2,center=(2.4,-.65,0),unit=.62)
    icons=VGroup(fit(math('a+0=a',35),2.1).move_to([-4.8,-.5,0]),fit(math(r'a\times1=a',35),2.1).move_to([-2.4,-.5,0]),VGroup(p,math(r'\pi\ \mathrm{rad}',25,GOLD).move_to([0,-1.95,0])),VGroup(q,math(r'\times i',25,PURPLE).move_to([2.4,-1.95,0])),VGroup(MiniGrowth(),math(r'(e^x)\prime=e^x',24,TEAL).move_to([4.8,-1.95,0])))
    return syms,labels,icons
def relation_state():return identity(),txt('다섯 숫자 · 하나의 관계',29,MUTED).move_to([0,-1.15,0])
def principles_state():
    growth=MiniGrowth(center=(-4.4,-.2,0),width=2.7,height=2.1)
    u=OrbitVisual(PI/2,center=(0,-.2,0),unit=.95);v=OrbitVisual(PI,center=(4.4,-.2,0),unit=.95)
    labels=VGroup(*[txt(s,27,c).move_to([x,2.3,0]) for s,c,x in zip(['지수적 변화','복소수 곱셈','원의 각도'],[TEAL,PURPLE,GOLD],[-4.4,0,4.4])])
    eqs=VGroup(math("y'=y",45,TEAL).move_to([-4.4,-1.95,0]),math(r'\times i',45,PURPLE).move_to([0,-1.95,0]),math(r'\theta=\pi',45,GOLD).move_to([4.4,-1.95,0]))
    return growth,u,v,labels,eqs
def centered_formula(angle=PI/3):return formula_end(angle)

class ChapterScene(PreviousScene):
    def construct(self):
        record=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1];self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.caption_index=-1;self.caption_audit=[]
        self.caption=VGroup().set_z_index(100);self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
        getattr(self,record['method'])();self.to(self.total_duration);self.caption.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def opening(self):
        u,eq,title=formula_end();self.add(u,eq,title)
        self.play_for(6,u.theta.animate.set_value(PI/2),rate_func=linear);self.to(7)
        self.play_for(.7,FadeIn(u.components));self.play_for(3.6,u.theta.animate.set_value(PI/3),rate_func=linear);self.to(12)
        self.play_for(1.5,FadeOut(u.components),u.theta.animate.set_value(0));self.to(14)
    def half_turn_angle(self):
        old,eq,title=formula_end(0);self.add(old,eq,title);u=half_orbit(0);new=equation(r'e^{i\theta}=\cos\theta+i\sin\theta')
        question=txt('반 바퀴 = ?',35,GOLD).move_to([3,.8,0])
        self.play_for(1.1,FadeOut(old),FadeOut(title),TransformMatchingTex(eq,new),FadeIn(u),FadeIn(question));self.to(4)
        full=Arc(radius=1.7,start_angle=0,angle=TAU,arc_center=u.o,color=GOLD,stroke_width=5)
        full_label=math(r'2\pi\ \mathrm{rad}',56,GOLD).move_to([3,.8,0])
        self.play_for(2,Create(full),Transform(question,full_label));self.to(7)
        half=Arc(radius=1.7,start_angle=0,angle=PI,arc_center=u.o,color=GOLD,stroke_width=5)
        self.play_for(1.2,Transform(full,half),Transform(question,math(r'\pi\ \mathrm{rad}',56,GOLD).move_to([3,.8,0])));self.to(10)
        sub=pi_equation();self.play_for(1.4,TransformMatchingTex(new,sub),FadeOut(full),Transform(question,math(r'\theta=\pi',56,GOLD).move_to([3,.8,0])));self.to(13)
    def half_turn(self):
        u=half_orbit(0);eq=pi_equation();label=math(r'\theta=\pi',56,GOLD).move_to([3,.8,0]);self.add(u,eq,label)
        tags=endpoints(u);self.play_for(1,FadeOut(label),FadeIn(tags));self.to(4)
        self.play_for(.8,Indicate(tags[0],color=GOLD));self.to(8)
        # Positive theta follows the upper half-circle, without changing radius.
        self.play_for(5,u.theta.animate.set_value(PI),rate_func=linear)
        answer=equation(r'e^{i\pi}=-1',66,.7).move_to([3,.7,0]);self.play_for(.7,Indicate(tags[1],color=GOLD),FadeIn(answer));self.to(15)
    def evaluate(self):
        u,eq,tags=half_state();answer=equation(r'e^{i\pi}=-1',66,.7).move_to([3,.7,0]);self.add(u,eq,tags,answer)
        cos=math(r'\cos\pi=-1',51,BLUE).move_to([3,1.05,0]);sin=math(r'\sin\pi=0',51,PURPLE).move_to([3,-.25,0])
        self.play_for(1,FadeOut(answer),FadeIn(cos),Indicate(tags[1],color=BLUE));self.to(3)
        zero=math('0',30,PURPLE).move_to(u.axes.c2p(-1,0)+UP*.35)
        self.play_for(1,FadeIn(sin),FadeIn(zero));self.to(6)
        evaluated=equation(r'e^{i\pi}=-1+i\cdot0',77,.8)
        self.play_for(1.2,FadeOut(u),FadeOut(tags),FadeOut(zero),FadeOut(cos),FadeOut(sin),TransformMatchingTex(eq,evaluated))
        self.play_for(1,TransformMatchingTex(evaluated,bare_result()));self.to(10)
    def identity_assembly(self):
        old=bare_result();self.add(old)
        added=equation(r'e^{i\pi}+1=-1+1',88,.65)
        self.play_for(1.5,TransformMatchingTex(old,added));self.to(2)
        result=identity();self.play_for(1.6,TransformMatchingTex(added,result));self.to(4)
        title=identity_title();self.play_for(.8,FadeIn(title));self.to(8)
    def five_meanings(self):
        old=identity();title=identity_title();self.add(old,title)
        syms,labels,icons=meaning_state()
        self.play_for(1.4,FadeOut(title),ReplacementTransform(old,syms));self.to(3)
        # Each card is introduced exactly during its approved narration interval.
        self.play_for(.65,FadeIn(labels[0]),FadeIn(icons[0]),Indicate(syms[0],color=COLORS[0]));self.to(5)
        self.play_for(.65,FadeIn(labels[1]),FadeIn(icons[1]),Indicate(syms[1],color=COLORS[1]));self.to(7)
        icons[2][0].theta.set_value(0)
        self.play_for(.5,FadeIn(labels[2]),FadeIn(icons[2]));self.play_for(1.6,icons[2][0].theta.animate.set_value(PI),rate_func=linear);self.to(10)
        icons[3][0].theta.set_value(0)
        self.play_for(.5,FadeIn(labels[3]),FadeIn(icons[3]));self.play_for(1.6,icons[3][0].theta.animate.set_value(PI/2),rate_func=linear);self.to(13)
        icons[4][0].x.set_value(-.7)
        self.play_for(.5,FadeIn(labels[4]),FadeIn(icons[4]));self.play_for(1.8,icons[4][0].x.animate.set_value(.7),rate_func=linear);self.to(16)
    def one_relation(self):
        syms,labels,icons=meaning_state();self.add(syms,labels,icons)
        self.play_for(1,icons.animate.set_opacity(.25),labels.animate.set_opacity(.5));self.to(4)
        eq=identity();title=txt('다섯 숫자 · 하나의 관계',29,MUTED).move_to([0,-1.15,0])
        self.play_for(2,FadeOut(labels),FadeOut(icons),ReplacementTransform(syms,eq),FadeIn(title));self.to(7)
        self.play_for(.8,Indicate(eq,color=GOLD,scale_factor=1.03));self.to(13)
    def principles(self):
        old,title=relation_state();self.add(old,title)
        g,u,v,labels,eqs=principles_state();g.x.set_value(-.7);u.theta.set_value(0);v.theta.set_value(0)
        self.play_for(1.2,FadeOut(old),FadeOut(title),FadeIn(g),FadeIn(u),FadeIn(v),FadeIn(labels));self.to(3)
        self.play_for(.5,FadeIn(eqs[0]));self.play_for(2.5,g.x.animate.set_value(.7),rate_func=linear);self.to(7)
        self.play_for(.5,FadeIn(eqs[1]));self.play_for(2.5,u.theta.animate.set_value(PI/2),rate_func=linear);self.to(11)
        self.play_for(.5,FadeIn(eqs[2]));self.play_for(2.5,v.theta.animate.set_value(PI),rate_func=linear);self.to(15)
    def special_angle(self):
        g,u,v,labels,eqs=principles_state();self.add(g,u,v,labels,eqs)
        circle,formula,title=centered_formula(0);circle.add(circle.components)
        self.play_for(1.5,FadeOut(g),FadeOut(u),FadeOut(v),FadeOut(labels),FadeOut(eqs),FadeIn(circle),FadeIn(formula),FadeIn(title))
        coord=equation(r'\cos\theta+i\sin\theta',52,-2.05)
        self.play_for(.6,FadeIn(coord));self.play_for(4,circle.theta.animate.set_value(PI/3),rate_func=linear);self.to(7)
        pi_form=equation(r'e^{i\pi}=\cos\pi+i\sin\pi',74,2)
        self.play_for(2,circle.theta.animate.set_value(PI),TransformMatchingTex(formula,pi_form),rate_func=linear)
        self.play_for(1.3,FadeOut(circle),FadeOut(title),FadeOut(coord),TransformMatchingTex(pi_form,identity()),FadeIn(identity_title()));self.to(12)
    def connected_structure(self):
        old=identity();title=identity_title();self.add(old,title);self.play_for(1,Indicate(old,color=GOLD,scale_factor=1.03));self.to(4)
        graph=MiniGrowth(center=(-3.5,-.25,0),width=3.7,height=2.5,x=-.7);u=OrbitVisual(0,center=(3.5,-.25,0),unit=1.15)
        left=math('e^x',65,TEAL).move_to([-3.5,2.3,0]);right=txt('회전과 삼각함수',28,PURPLE).move_to([3.5,2.3,0])
        divider=Line([0,-2.2,0],[0,2.7,0],color=GRAY,stroke_opacity=.4)
        self.play_for(1.2,FadeOut(old),FadeOut(title),FadeIn(graph),FadeIn(u),FadeIn(left),FadeIn(right),Create(divider))
        self.play_for(3.8,graph.x.animate.set_value(.7),u.theta.animate.set_value(PI/3),rate_func=linear);self.to(10)
        extension=txt('복소수로 확장',27,MUTED).move_to([-3.5,1.15,0]);complex_left=equation(r'e^{i\theta}',65,2.3).move_to([-3.5,2.3,0])
        self.play_for(1.1,TransformMatchingTex(left,complex_left),FadeIn(extension),FadeOut(divider))
        expr=equation(r'\cos\theta+i\sin\theta',48,2.3).move_to([3.5,2.3,0]);self.play_for(.8,ReplacementTransform(right,expr));self.to(14)
        final,formula,formula_title=centered_formula(PI/3)
        self.play_for(1.4,FadeOut(graph),FadeOut(u),FadeOut(complex_left),FadeOut(extension),FadeOut(expr),FadeIn(final),FadeIn(formula),FadeIn(formula_title));self.to(18)
    def ending(self):
        u,eq,title=centered_formula(PI/3);self.add(u,eq,title)
        # Return to the origin of the half-turn before the final positive rotation.
        self.play_for(.5,FadeOut(title),u.theta.animate.set_value(0))
        target=equation(r'e^{i\pi}=-1',90,2)
        self.play_for(3,u.theta.animate.set_value(PI),TransformMatchingTex(eq,target),rate_func=linear);self.to(4)
        add=equation(r'e^{i\pi}+1=-1+1',88,.65)
        self.play_for(1,FadeOut(u),TransformMatchingTex(target,add))
        result=identity();self.play_for(1.4,TransformMatchingTex(add,result));self.to(7)
        self.to(9)
