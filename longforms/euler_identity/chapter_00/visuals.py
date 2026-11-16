from pathlib import Path
import json, textwrap
from manim import *

R=Path(__file__).resolve().parent
config.background_color='#10151F'
config.frame_width=128/9
config.frame_height=8
FONT='Malgun Gothic'
WHITE_INK='#F5F7FB'; MUTED='#8190A5'; ZERO='#B8C2D1'; ONE='#FFFFFF'; GOLD='#F3BA61'; PURPLE='#B69CF8'; TEAL='#66CFC1'
COLORS=[ZERO,ONE,GOLD,PURPLE,TEAL]
SYMS=['0','1',r'\pi','i','e']

def txt(s,size=25,color=WHITE_INK):
    return Text(s,font=FONT,font_size=size,color=color)
def math(s,size=60,color=WHITE_INK):
    return MathTex(s,font_size=size,color=color)
def bank():
    return VGroup(*[math(s,38,c).move_to([-4+2*k,2.9,0]) for k,(s,c) in enumerate(zip(SYMS,COLORS))])
def circle_diagram(scale=1):
    c=Circle(radius=1.2,color=GOLD,stroke_width=4)
    diameter=Line(LEFT*1.2,RIGHT*1.2,color=WHITE_INK,stroke_width=2)
    return VGroup(c,diameter).scale(scale)
def complex_diagram(scale=1):
    axes=VGroup(Line(LEFT*1.65,RIGHT*1.65,color=MUTED,stroke_width=2),Line(DOWN*1.4,UP*1.4,color=PURPLE,stroke_width=2))
    labels=VGroup(math('1',23).move_to([1.3,-.3,0]),math('-1',23).move_to([-1.3,-.3,0]),math('i',25,PURPLE).move_to([.25,1.2,0]))
    return VGroup(axes,labels).scale(scale)
def exponential(scale=1):
    axes=Axes(x_range=[-1.5,1.6,1],y_range=[0,5,1],x_length=3.4,y_length=2.6,axis_config={'color':MUTED,'include_ticks':False,'include_tip':False})
    curve=axes.plot(lambda x:np.exp(x),x_range=[-1.5,1.5],color=TEAL,stroke_width=4)
    return VGroup(axes,curve).scale(scale)
def cards():
    # Four concept groups; constants remain individual objects for their later flight.
    symbols=VGroup(math('0',58,ZERO).move_to([-4.9,1.45,0]),math('1',58,ONE).move_to([-3.9,1.45,0]),math(r'\pi',62,GOLD).move_to([-1.45,1.45,0]),math('i',62,PURPLE).move_to([1.45,1.45,0]),math('e',62,TEAL).move_to([4.4,1.45,0]))
    backs=VGroup(*[RoundedRectangle(width=2.65,height=3.7,corner_radius=.18,stroke_color='#2C3647',fill_color='#182131',fill_opacity=.7).move_to([x,.35,0]) for x in [-4.4,-1.45,1.45,4.4]])
    icons=VGroup(VGroup(math('a+0=a',27),math(r'a\cdot1=a',27)).arrange(DOWN,buff=.22).move_to([-4.4,0,0]),circle_diagram(.48).move_to([-1.45,0,0]),complex_diagram(.45).move_to([1.45,0,0]),exponential(.46).move_to([4.4,0,0]))
    labels=VGroup(*[txt(s,22,c).move_to([x,-1.05,0]) for s,c,x in zip(['기본 연산','원과 기하학','복소수','지수함수 · 미적분'],[ONE,GOLD,PURPLE,TEAL],[-4.4,-1.45,1.45,4.4])])
    return symbols,VGroup(backs,icons,labels)
def identity():
    # TeX lays out the superscript; semantic tokens retain the introduction colors.
    eq=MathTex(r'e^{i\pi}+1=0',substrings_to_isolate=SYMS,font_size=112)
    for s,c in zip(SYMS,COLORS):eq.set_color_by_tex(s,c,substring=False)
    return eq.move_to([0,.65,0])
def identity_title():return txt("Euler’s Identity  ·  오일러 항등식",25,MUTED).move_to([0,-1,0])

class IntroScene(Scene):
    index=1
    def construct(self):
        self.manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
        record=self.manifest[self.index-1]
        self.start=record['start'];self.total_duration=record['duration_seconds']
        self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
        self.caption=VGroup();self.caption_index=-1
        self.caption_audit=[]
        self.caption_driver=VMobject().add_updater(lambda m,dt:self.update_caption())
        self.add(self.caption_driver)
        getattr(self,['world','zero','one','pi','imaginary','exponential','domains','identity','question','transition'][self.index-1])()
        self.to(self.total_duration)
        self.caption_driver.clear_updaters()
        (R/record['directory']/'layout_audit.json').write_text(json.dumps(self.caption_audit,ensure_ascii=False,indent=2),encoding='utf-8')
    def update_caption(self):
        t=self.start+self.time
        i=next((k for k,x in enumerate(self.lines) if x['start']<=t<x['end']),len(self.lines)-1)
        if i==self.caption_index:return
        self.caption_index=i;self.remove(self.caption)
        s=self.lines[i]['text']
        wrapped=textwrap.fill(s,width=49,break_long_words=False,break_on_hyphens=False)
        caption=txt(wrapped,25)
        if caption.width>12.5:caption.scale_to_fit_width(12.5)
        caption.move_to([0,-3.35,0])
        bg=RoundedRectangle(width=13,height=max(.7,caption.height+.25),corner_radius=.1,stroke_width=0,fill_color='#10151F',fill_opacity=.97).move_to(caption)
        self.caption=VGroup(bg,caption).set_z_index(100)
        self.add(self.caption)
        assert caption.get_bottom()[1]>-3.95 and caption.get_top()[1]<-2.75
        self.caption_audit.append(dict(line=i+1,left=float(caption.get_left()[0]),right=float(caption.get_right()[0]),top=float(caption.get_top()[1]),bottom=float(caption.get_bottom()[1])))
    def to(self,t):
        frames=round(t*config.frame_rate)-round(self.time*config.frame_rate)
        if frames<0:raise ValueError(f'Scene {self.index} overrun {self.time}>{t}')
        if frames:self.wait(frames/config.frame_rate)
    def play_for(self,t,*anims):self.play(*anims,run_time=t)
    def world(self):
        formulas=['1','2','3','x','y',r'a^2+b^2=c^2',r"f'(x)",r'\int f(x)\,dx',r'\sum_{k=1}^n k',r'\sqrt{2}',r'\frac{a}{b}',r'\sin x',r'x+y',r'\Delta x',r'\infty',r'\log x',r'x^2',r'\frac{dy}{dx}',r'\alpha+\beta',r'a_n']
        cloud=VGroup()
        for k,s in enumerate(formulas):
            x=-5.65+(k%5)*2.8;y=2.4-(k//5)*1.35
            cloud.add(math(s,27+(k%3)*8,MUTED).move_to([x,y,0]).set_opacity(.35+.12*(k%4)))
        self.play_for(2.7,LaggedStart(*[FadeIn(x,shift=UP*.12) for x in cloud],lag_ratio=.06))
        self.to(3)
        b=bank()
        self.play_for(2,FadeOut(cloud),LaggedStart(*[FadeIn(x,shift=DOWN*.3) for x in b],lag_ratio=.15))
        self.to(8)
    def zero(self):
        b=bank();self.add(b)
        eq=math('5+0=5',92);eq.set_color_by_tex('0',ZERO)
        self.play_for(.45,b[0].animate.scale(1.4),FadeIn(eq,shift=UP*.1))
        self.to(1.6)
        self.play_for(.4,b[0].animate.scale(1/1.4))
    def one(self):
        b=bank();old=math('5+0=5',92);self.add(b,old)
        new=math(r'5\times1=5',92)
        self.play_for(.65,TransformMatchingTex(old,new),b[1].animate.scale(1.4))
        self.to(2.5);self.play_for(.5,FadeOut(new),b[1].animate.scale(1/1.4))
    def pi(self):
        b=bank();self.add(b);g=circle_diagram().shift(LEFT*1.9);eq=math(r'\pi=\frac{C}{d}',76,GOLD).shift(RIGHT*2)
        self.play_for(.8,Create(g[0]),Create(g[1]),FadeIn(eq))
        dot=Dot(g[0].point_from_proportion(0),color=GOLD,radius=.07);self.add(dot)
        self.play_for(2.4,MoveAlongPath(dot,g[0],rate_func=linear))
        self.play_for(.8,FadeOut(g),FadeOut(eq),FadeOut(dot))
    def imaginary(self):
        b=bank();g=complex_diagram().shift(LEFT*1.8);eq=math('i^2=-1',76,PURPLE).shift(RIGHT*2.1)
        origin=LEFT*1.8;v=Arrow(origin,origin+RIGHT*1.2,buff=0,color=PURPLE,stroke_width=6)
        self.add(b,g,eq,v)
        self.play_for(.7,Rotate(v,PI/2,about_point=origin))
        self.play_for(.7,Rotate(v,PI/2,about_point=origin))
        self.to(1.7);self.play_for(.3,FadeOut(g),FadeOut(v),FadeOut(eq))
    def exponential(self):
        b=bank();self.add(b);g=exponential().shift(RIGHT*.9);eq=math('e^x',86,TEAL).shift(LEFT*3)
        self.play_for(.6,FadeIn(g[0]),FadeIn(eq))
        self.play_for(1.6,Create(g[1],rate_func=linear))
        dot=Dot(g[1].get_start(),color=TEAL,radius=.07);self.add(dot)
        self.play_for(1.2,MoveAlongPath(dot,g[1],rate_func=linear))
        self.play_for(.6,FadeOut(g),FadeOut(eq),FadeOut(dot),FadeOut(b))
    def domains(self):
        sy,other=cards();self.play_for(1,FadeIn(other[0]),FadeIn(sy))
        self.to(3)
        for j,end in enumerate([5,7,8,12]):
            self.play_for(.4,FadeIn(other[1][j]),FadeIn(other[2][j]),other[0][j].animate.set_stroke([ONE,GOLD,PURPLE,TEAL][j],width=2))
            self.to(end)
    def identity(self):
        sy,other=cards()
        for j,c in enumerate([ONE,GOLD,PURPLE,TEAL]):other[0][j].set_stroke(c,width=2)
        self.add(other,sy)
        self.play_for(2,FadeOut(other),*[s.animate.move_to([x,.65,0]) for s,x in zip(sy,[-4,-2,0,2,4])])
        self.to(4)
        eq=identity();used=[];anims=[]
        for obj,s in zip(sy,SYMS):
            target=eq.get_part_by_tex(s)
            used.append(target);anims.append(ReplacementTransform(obj,target))
        ops=eq.copy()
        for s in SYMS:ops.get_part_by_tex(s).set_opacity(0)
        self.play_for(2.4,*anims,FadeIn(ops))
        self.remove(sy,*used,ops);self.add(eq)
        self.to(7)
        self.play_for(.7,FadeIn(identity_title()))
        self.to(10)
    def question(self):
        eq=identity();title=identity_title();self.add(eq,title)
        circle=circle_diagram(.65).move_to([-4,1.8,0]).set_opacity(.25)
        curve=exponential(.55).move_to([3.9,1.65,0]).set_opacity(.25)
        arc=Arc(radius=.8,start_angle=0,angle=PI*.8,color=PURPLE,stroke_opacity=.35).add_tip(tip_length=.15).move_to([0,-1.8,0])
        self.play_for(1,FadeIn(circle),Indicate(eq.get_part_by_tex(r'\pi',substring=False),color=GOLD,scale_factor=1.12))
        self.to(2.5)
        self.play_for(1,FadeIn(curve),Indicate(eq.get_part_by_tex('e',substring=False),color=TEAL,scale_factor=1.12))
        self.to(4.5)
        self.play_for(1,FadeIn(arc),Indicate(eq.get_part_by_tex('i',substring=False),color=PURPLE,scale_factor=1.12))
        self.to(7.4);self.play_for(.6,FadeOut(circle),FadeOut(curve),FadeOut(arc))
    def transition(self):
        eq=identity();title=identity_title();self.add(eq,title)
        self.play_for(1.2,eq.animate.scale(.55).move_to([0,2.7,0]),FadeOut(title))
        for s in ['e','i',r'\pi']:eq.get_part_by_tex(s,substring=False).set_opacity(.25)
        pair=VGroup(math('0',130,ZERO),math('1',130,ONE)).arrange(RIGHT,buff=2).move_to([0,.3,0])
        self.play_for(1.6,TransformFromCopy(eq.get_part_by_tex('0',substring=False),pair[0]),TransformFromCopy(eq.get_part_by_tex('1',substring=False),pair[1]))
        self.to(4)
        self.play_for(.5,FadeIn(txt('연산의 기준',25,MUTED).move_to([0,-1.4,0])))
        self.to(5)

