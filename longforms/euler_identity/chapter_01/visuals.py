from pathlib import Path
import json, sys
from manim import *
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parents[2]))
from longforms.euler_identity.chapter_00.visuals import IntroScene, txt, math, identity, ZERO, ONE, GOLD, MUTED, WHITE_INK
BLUE='#8AA9FF'

def formula(s,size=64):
    m=MathTex(s,font_size=size,substrings_to_isolate=['0','1',r'\vec{0}','I_2'])
    for token,c in [('0',ZERO),('1',ONE),(r'\vec{0}',ZERO),('I_2',ONE)]:m.set_color_by_tex(token,c)
    return m
def opening_state():
    eq=identity().scale(.55).move_to([0,2.7,0])
    for s in ['e','i',r'\pi']:eq.get_part_by_tex(s).set_opacity(.25)
    pair=VGroup(math('0',130,ZERO),math('1',130,ONE)).arrange(RIGHT,buff=2).move_to([0,.3,0])
    title=txt('연산의 기준',25,MUTED).move_to([0,-1.4,0])
    return eq,pair,title
def numberline(maximum=10):
    step=2 if maximum==10 else 40
    line=NumberLine(x_range=[0,maximum,step],length=9,include_numbers=False,color=MUTED,include_tip=True).move_to([0,-.7,0])
    labels=VGroup(*[math(str(n),25,MUTED).next_to(line.n2p(n),DOWN,buff=.22) for n in ([0,5,10] if maximum==10 else [0,100,200])])
    return VGroup(line,labels)
def add_state():
    eq=formula('a+0=a',80).move_to([0,1.5,0])
    label=txt('덧셈의 항등원',30,BLUE).move_to([0,-.15,0])
    note=txt('연산 후에도 원래 값을 유지하는 요소',24,MUTED).move_to([0,-1.1,0])
    underline=Line([-1.6,.75,0],[1.6,.75,0],color=BLUE,stroke_width=3)
    return VGroup(eq,label,note,underline)
def summary():
    left=VGroup(formula('a+0=a',64),txt('덧셈의 항등원',26,BLUE)).arrange(DOWN,buff=.55).move_to([-3,1,0])
    right=VGroup(formula(r'a\times1=a',64),txt('곱셈의 항등원',26,GOLD)).arrange(DOWN,buff=.55).move_to([3,1,0])
    return VGroup(left,right)
def comparison():
    divider=Line([0,2.3,0],[0,-1.7,0],color='#2C3647')
    eq0=formula(r'5\times0=0',64).move_to([-3.2,1.6,0]);eq1=formula(r'5\times1=5',64).move_to([3.2,1.6,0])
    origins=[np.array([-5,-.2,0]),np.array([1.4,-.2,0])]
    bars=VGroup(*[Arrow(p,p+RIGHT*3.5,buff=0,color=c,stroke_width=8) for p,c in zip(origins,[BLUE,GOLD])])
    dots=VGroup(*[Dot(p,color=c,radius=.06) for p,c in zip(origins,[BLUE,GOLD])])
    baseline=VGroup(*[Line(p+DOWN*.12,p+RIGHT*3.5+DOWN*.12,color=MUTED,stroke_opacity=.3) for p in origins])
    return VGroup(divider,eq0,eq1,bars,dots,baseline)
def branches():
    s=summary().scale(.7).move_to([0,2.2,0])
    root=txt('숫자',30).move_to([0,.9,0])
    v=txt('벡터',30,BLUE).move_to([-3,-.65,0]);m=txt('행렬',30,GOLD).move_to([3,-.65,0])
    lines=VGroup(Line([0,.5,0],[-3,-.2,0],color=BLUE),Line([0,.5,0],[3,-.2,0],color=GOLD))
    return VGroup(s,root,v,m,lines)
def vector_state():
    axes=Axes(x_range=[-1,4,1],y_range=[-1,3,1],x_length=4.7,y_length=3.4,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([-2.8,.3,0])
    origin=axes.c2p(0,0);tip=axes.c2p(3,2)
    v=Arrow(origin,tip,buff=0,color=BLUE,stroke_width=6)
    vl=formula(r'\vec{v}',35).next_to(v.get_center(),UP,buff=.2)
    eq=formula(r'\vec{v}+\vec{0}=\vec{v}',55).move_to([3,1.1,0])
    label=txt('영벡터 · 길이 0',25,BLUE).move_to([3,-.1,0])
    zero=Dot(tip,radius=.075,color=ZERO)
    return VGroup(axes,v,vl,eq,label,zero)
def matrix_state():
    axes=Axes(x_range=[-1,3,1],y_range=[-1,3,1],x_length=4,y_length=3.4,axis_config={'color':MUTED,'include_tip':False,'include_ticks':False}).move_to([-3,.3,0])
    points=[axes.c2p(x,y) for x,y in [(0,0),(1.8,.3),(2.2,1.7),(.4,1.4)]]
    shape=Polygon(*points,stroke_color=GOLD,fill_color=GOLD,fill_opacity=.1,stroke_width=4)
    dots=VGroup(*[Dot(p,radius=.055,color=GOLD) for p in points])
    mat=formula(r'I_2=\begin{pmatrix}1&0\\0&1\end{pmatrix}',49).move_to([2.7,1.6,0])
    apply=formula('I_2x=x',44).move_to([2.7,.2,0])
    eq=formula('AI_2=A',51).move_to([2.7,-1,0])
    return VGroup(axes,shape,dots,mat,apply,eq)
def roles_state():
    header=txt('항등원',39).move_to([0,2.6,0])
    left=VGroup(formula('a+0=a',53),formula(r'\vec{v}+\vec{0}=\vec{v}',53),txt('덧셈에서 값 유지',26,BLUE)).arrange(DOWN,buff=.6).move_to([-3.1,.2,0])
    right=VGroup(formula(r'a\times1=a',53),formula('AI_2=A',53),txt('곱셈에서 값 유지',26,GOLD)).arrange(DOWN,buff=.6).move_to([3.1,.2,0])
    rule=Line([0,1.6,0],[0,-1.5,0],color='#2C3647')
    return VGroup(header,left,right,rule)

class ChapterScene(IntroScene):
    index=1
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
        eq,pair,title=opening_state();self.add(eq,pair,title)
        self.play_for(1,FadeOut(eq),FadeOut(title));self.to(2)
        # An empty outline and a single dot express quantity without implying two zeros.
        empty=Circle(radius=.3,color=MUTED,stroke_width=1.5).move_to(pair[0].get_center()+DOWN*1.4)
        full=Circle(radius=.3,color=MUTED,stroke_width=1.5).move_to(pair[1].get_center()+DOWN*1.4)
        dot=Dot(full.get_center(),color=ONE,radius=.08)
        self.play_for(.8,FadeIn(empty),FadeIn(full),FadeIn(dot));self.to(5.8)
        self.play_for(.8,FadeOut(empty),FadeOut(full),FadeOut(dot));self.to(7)
    def add_zero(self):
        _,pair,_=opening_state();self.add(pair)
        nl=numberline(10);eq=formula('5+0=5',76).move_to([0,1.4,0])
        self.play_for(1,FadeOut(pair[1]),pair[0].animate.scale(.55).move_to([-5.6,2.4,0]),FadeIn(nl))
        self.to(2)
        dot=Dot(nl[0].n2p(5),color=BLUE,radius=.09);plus=formula('+0',40).next_to(dot,UP,buff=.3)
        self.play_for(.6,FadeIn(dot),FadeIn(plus),FadeIn(eq));self.to(5)
        nl2=numberline(200);eq2=formula('100+0=100',76).move_to(eq)
        self.play_for(.7,Transform(nl,nl2),TransformMatchingTex(eq,eq2))
        self.to(8.5);self.play_for(.5,FadeOut(pair[0]),FadeOut(plus))
    def subtract(self):
        nl=numberline(200);dot=Dot(nl[0].n2p(100),color=BLUE,radius=.09);eq=formula('100+0=100',76).move_to([0,1.4,0]);self.add(nl,dot,eq)
        new=numberline(10);neweq=formula('5-5=0',76).move_to(eq)
        self.play_for(.6,Transform(nl,new),TransformMatchingTex(eq,neweq))
        minus=math('-5',38,BLUE).next_to(dot,UP,buff=.3);self.add(minus)
        self.play_for(1.8,dot.animate.move_to(new[0].n2p(0)),minus.animate.move_to(new[0].n2p(0)+UP*.55))
        self.play_for(.5,Indicate(dot,color=BLUE),FadeOut(minus));self.to(4)
    def add_identity(self):
        nl=numberline(10);dot=Dot(nl[0].n2p(0),color=BLUE,radius=.09);old=formula('5-5=0',76).move_to([0,1.4,0]);self.add(nl,dot,old)
        example=formula('5+0=5',76).move_to(old)
        self.play_for(.7,FadeOut(nl),FadeOut(dot),TransformMatchingTex(old,example))
        state=add_state();self.play_for(1.3,TransformMatchingTex(example,state[0]),Create(state[3]))
        self.to(5)
        self.play_for(.8,FadeIn(state[1]),FadeIn(txt('Identity Element',21,MUTED).move_to([0,-.65,0])),FadeIn(state[2]))
        self.to(10)
    def multiply(self):
        state=add_state();english=txt('Identity Element',21,MUTED).move_to([0,-.65,0]);self.add(state,english)
        c=comparison();self.play_for(1,FadeOut(state),FadeOut(english),FadeIn(c))
        self.to(3)
        origin=c[4][0].get_center();target=Line(origin,origin+RIGHT*.001,color=BLUE,stroke_width=8)
        self.play_for(1.4,Transform(c[3][0],target))
        left=txt('값이 0으로 변함',26,BLUE).move_to([-3.2,-1.2,0]);self.play_for(.5,FadeIn(left));self.to(6)
        right=txt('원래 값을 유지',26,GOLD).move_to([3.2,-1.2,0]);self.play_for(.7,Indicate(c[3][1],color=GOLD,scale_factor=1),FadeIn(right));self.to(10)
    def mul_identity(self):
        eq=formula(r'5\times1=5',82).move_to([0,1,0]);self.add(eq)
        self.to(1.8)
        new=formula(r'100\times1=100',82).move_to(eq);self.play_for(.7,TransformMatchingTex(eq,new));self.to(4)
        s=summary();self.play_for(1,TransformMatchingTex(new,s[1][0]),FadeIn(s[0]),FadeIn(s[1][1]));self.to(6)
    def extend(self):
        s=summary();self.add(s);b=branches()
        self.play_for(1,Transform(s,b[0]),FadeIn(b[1]));self.to(2)
        self.play_for(1.1,Create(b[4]),FadeIn(b[2]),FadeIn(b[3]))
        self.play_for(1,FadeIn(txt('대상이 달라도, 값을 보존하는 역할',25,MUTED).move_to([0,-1.8,0])));self.to(8)
    def vector(self):
        b=branches();self.add(b)
        v=vector_state();self.play_for(.6,FadeOut(b),FadeIn(v))
        ring=Circle(radius=.15,color=BLUE).move_to(v[5]);self.play_for(.7,Create(ring))
        unchanged=v[1].copy().set_color(WHITE_INK).set_stroke(width=2)
        self.play_for(.7,FadeIn(unchanged),Indicate(v[5],color=BLUE,scale_factor=1.2))
        self.to(3.3);self.play_for(.7,FadeOut(ring),FadeOut(unchanged));self.to(4)
    def matrix(self):
        v=vector_state();self.add(v)
        m=matrix_state();self.play_for(.5,FadeOut(v),FadeIn(m))
        overlay=m[1].copy().set_fill(opacity=0).set_stroke(WHITE_INK,width=2)
        self.play_for(.8,FadeIn(overlay),Indicate(m[3],color=GOLD,scale_factor=1.03))
        self.to(2.4);self.play_for(.6,FadeOut(overlay));self.to(3)
    def roles(self):
        m=matrix_state();self.add(m);s=roles_state()
        self.play_for(1,FadeOut(m),FadeIn(s))
        self.to(3)
        boxes=VGroup(SurroundingRectangle(s[1],color=BLUE,buff=.25,stroke_width=2),SurroundingRectangle(s[2],color=GOLD,buff=.25,stroke_width=2))
        self.play_for(.8,Create(boxes));self.to(5.8);self.play_for(.6,FadeOut(boxes));self.to(7)
    def geometry(self):
        s=roles_state();self.add(s)
        self.play_for(1.2,FadeOut(s[1]),FadeOut(s[2]),FadeOut(s[3]))
        self.to(4.2);self.play_for(.8,FadeOut(s[0]));self.to(5)
        center=Dot(ORIGIN,color=GOLD,radius=.05);circle=Circle(radius=1.5,color=GOLD,stroke_width=4)
        self.play_for(.5,FadeIn(center));self.play_for(2.5,Create(circle));self.to(10)
    def pi(self):
        circle=Circle(radius=1.5,color=GOLD,stroke_width=4);center=Dot(ORIGIN,color=GOLD,radius=.05);self.add(circle,center)
        diameter=Line(LEFT*1.5,RIGHT*1.5,color=WHITE_INK,stroke_width=2)
        g=VGroup(circle,diameter,center)
        eq=math(r'\frac{C}{d}=\pi',63,GOLD).move_to([3.4,.3,0])
        self.play_for(.6,g.animate.shift(LEFT*1.5),FadeIn(eq))
        self.play_for(1.1,g.animate.scale(.65));self.play_for(1.1,g.animate.scale(1/.65))
        self.to(4)
        pi=math(r'\pi',110,GOLD).move_to([2.7,.3,0])
        self.play_for(.6,TransformMatchingTex(eq,pi),FadeOut(diameter),FadeOut(center))
        self.to(5)

