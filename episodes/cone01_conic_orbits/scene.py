"""A 9:16 silent Manim short: conic sections and inverse-square orbits."""
import json
import math
from pathlib import Path

import numpy as np
from manim import *

config.frame_width=9
config.frame_height=16
config.background_color='#0B1020'

DATA=json.loads((Path(__file__).parent/'script.json').read_text(encoding='utf-8'))
BG='#0B1020';PANEL='#17243B';EDGE='#31445F';WHITE='#EFF5FB';MUTED='#A7BAD0'
CIRCLE='#48D6C6';ELLIPSE='#69BDF8';PARABOLA='#F6CE71';HYPERBOLA='#C49BFF'
SUN='#FFB454';PLANE='#648FCE';FONT='Malgun Gothic'
COLORS=(CIRCLE,ELLIPSE,PARABOLA,HYPERBOLA)
NAMES=('원','타원','포물선','쌍곡선')
ENDS=(9,32,45,59,80,100,125,147,158,177)


def txt(s,size=27,color=WHITE):
    return Text(s,font=FONT,font_size=size,color=color)


def tex(s,size=43,color=WHITE):
    return MathTex(s,font_size=size,color=color)


def wrap(s,limit=23):
    out=[];line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if len(test)>limit and line:out.append(line);line=word
        else:line=test
    if line:out.append(line)
    return out


def curve_from_points(points,color,width=4):
    if len(points)<3:return VGroup()
    path=VMobject(stroke_color=color,stroke_width=width)
    path.set_points_smoothly(points)
    return path


class ConeOrbitShort(Scene):
    def setup(self):
        self.scene_center=np.array([0,1.35,0])
        self.orbit_center=np.array([0,1.15,0])

    def fit(self,obj,width=8):
        if obj.width>width:obj.scale_to_fit_width(width)
        return obj

    def title(self,main,kicker):
        a=txt(kicker,22,PARABOLA).move_to([0,6.8,0])
        b=txt(main,30).next_to(a,DOWN,buff=.17)
        self.fit(b,8)
        return VGroup(a,b)

    def project3(self,x,y,z):
        return self.scene_center+np.array([.86*x+.38*y,.9*z-.29*y,0])

    def cut_curve(self,slope):
        # Double cone x²+y²=z² intersected with the actual plane z=slope*x+0.9.
        sections=[]
        color=COLORS[0 if slope<.12 else 1 if slope<.88 else 2 if slope<1.12 else 3]
        for sign in (1,-1):
            run=[]
            for theta in np.linspace(-math.pi,math.pi,300):
                denom=sign-slope*math.cos(theta)
                r=.9/denom if abs(denom)>1e-5 else -1
                valid=.05<r<2.35
                if valid:
                    pt=self.project3(r*math.cos(theta),r*math.sin(theta),sign*r)
                    if run and np.linalg.norm(pt-run[-1])>.24:
                        if len(run)>3:sections.append(curve_from_points(run,color,5))
                        run=[]
                    run.append(pt)
                elif len(run)>3:
                    sections.append(curve_from_points(run,color,5));run=[]
            if len(run)>3:sections.append(curve_from_points(run,color,5))
        return VGroup(*sections)

    def cone(self,slope=0):
        apex=self.project3(0,0,0)
        wires=VGroup()
        for sign in (1,-1):
            rim=[self.project3(2.35*math.cos(t),2.35*math.sin(t),sign*2.35)
                 for t in np.linspace(0,2*math.pi,73)]
            wires.add(curve_from_points(rim,EDGE,2))
            for t in np.linspace(0,2*math.pi,13)[:-1]:
                edge=self.project3(2.35*math.cos(t),2.35*math.sin(t),sign*2.35)
                wires.add(Line(apex,edge,color=EDGE,stroke_width=1.5,stroke_opacity=.75))
        corners=[self.project3(x,y,slope*x+.9) for x,y in
                 [(-2.0,-1.8),(2.0,-1.8),(2.0,1.8),(-2.0,1.8)]]
        plane=Polygon(*corners,stroke_color=PLANE,stroke_width=2,
                      fill_color=PLANE,fill_opacity=.16)
        intersection=self.cut_curve(slope)
        return VGroup(wires,plane,intersection)

    def orbit_points(self,e,center=None,scale=1.12):
        center=self.orbit_center if center is None else np.array(center)
        # Periapsis is fixed at r=1. Tangential launch speed gives e=v²-1
        # for μ=r0=1; the same focus remains at the Sun for every orbit.
        runs=[];run=[]
        for theta in np.linspace(-math.pi,math.pi,420):
            denominator=1+e*math.cos(theta)
            r=(1+e)/denominator if denominator>.025 else -1
            valid=.02<r<3.15
            if valid:
                pt=center+np.array([scale*r*math.cos(theta),scale*r*math.sin(theta),0])
                if run and np.linalg.norm(pt-run[-1])>.2:
                    if len(run)>3:runs.append(run)
                    run=[]
                run.append(pt)
            elif len(run)>3:runs.append(run);run=[]
        if len(run)>3:runs.append(run)
        color=COLORS[0 if e<.08 else 1 if e<.95 else 2 if e<1.1 else 3]
        return VGroup(*[curve_from_points(points,color,4) for points in runs])

    def orbit(self,e,theta=.5,arrows=False,straight=False):
        center=self.orbit_center
        color=COLORS[0 if e<.08 else 1 if e<.95 else 2 if e<1.1 else 3]
        curve=self.orbit_points(e)
        sun=VGroup(Circle(radius=.25,stroke_color=SUN,stroke_width=2,
                          fill_color=SUN,fill_opacity=.22).move_to(center),
                   Dot(center,color=SUN,radius=.115))
        denom=1+e*math.cos(theta)
        r=(1+e)/denom if denom>.08 else 3
        planet_at=center+np.array([1.12*r*math.cos(theta),1.12*r*math.sin(theta),0])
        planet=Dot(planet_at,color=WHITE,radius=.085)
        items=[curve,sun,planet]
        if straight:
            start=center+np.array([1.12,0,0])
            items.append(DashedLine(start,start+UP*3.3,color=MUTED,dash_length=.12))
        if arrows:
            gravity=Arrow(planet_at,planet_at+.68*(center-planet_at)/np.linalg.norm(center-planet_at),
                          buff=0,color=SUN,stroke_width=4,tip_length=.17)
            tangent=np.array([-math.sin(theta),e+math.cos(theta),0])
            tangent=tangent/np.linalg.norm(tangent)
            velocity=Arrow(planet_at,planet_at+.72*tangent,buff=0,color=ELLIPSE,
                           stroke_width=4,tip_length=.17)
            items.extend([gravity,velocity])
        return VGroup(*items)

    def focus_geometry(self,phi,second=True,distances=False,gravity=False):
        e=.65;a=1/(1-e);b=a*math.sqrt(1-e*e)
        c=a*e;scale=.85
        origin=self.orbit_center
        center=origin+LEFT*c*scale
        ellipse=Ellipse(width=2*a*scale,height=2*b*scale,color=ELLIPSE,stroke_width=4).move_to(center)
        first=origin;other=origin+LEFT*2*c*scale
        planet_at=center+np.array([a*scale*math.cos(phi),b*scale*math.sin(phi),0])
        sun=Dot(first,color=SUN,radius=.12)
        planet=Dot(planet_at,color=WHITE,radius=.09)
        items=[ellipse,sun,planet]
        if second:items.append(Dot(other,color=HYPERBOLA,radius=.09))
        if distances and second:
            items.extend([Line(planet_at,first,color=SUN,stroke_width=2),
                          Line(planet_at,other,color=HYPERBOLA,stroke_width=2)])
        if gravity:
            vector=(first-planet_at)/np.linalg.norm(first-planet_at)
            items.append(Arrow(planet_at,planet_at+.72*vector,buff=0,
                               color=SUN,stroke_width=4,tip_length=.16))
        return VGroup(*items)

    def mini_curve(self,e,color,label):
        center=np.array([0,0,0]);points=[];runs=[];run=[]
        for t in np.linspace(-math.pi,math.pi,240):
            den=1+e*math.cos(t)
            r=(1+e)/den if den>.03 else -1
            if .02<r<2.9:
                pt=np.array([r*math.cos(t)*.55,r*math.sin(t)*.55,0])
                if run and np.linalg.norm(pt-run[-1])>.18:
                    if len(run)>2:runs.append(run)
                    run=[]
                run.append(pt)
            elif len(run)>2:runs.append(run);run=[]
        if len(run)>2:runs.append(run)
        shape=VGroup(*[curve_from_points(p,color,3) for p in runs])
        shape.scale_to_fit_width(min(shape.width,2.55)) if shape.width>2.55 else None
        title=txt(label,22,color)
        return VGroup(shape,title).arrange(DOWN,buff=.12)

    def gallery(self):
        cards=[self.mini_curve(e,c,n) for e,c,n in zip((0,.47,1,1.5),COLORS,NAMES)]
        rows=VGroup(VGroup(*cards[:2]).arrange(RIGHT,buff=.6),
                    VGroup(*cards[2:]).arrange(RIGHT,buff=.6)).arrange(DOWN,buff=.5)
        rows.move_to([0,1.25,0]);self.fit(rows,7.6)
        return rows

    def scene_for(self,i):
        if i==0:
            h=self.title('우주의 궤도에서 원뿔로','하나의 도형')
            visual=self.orbit(.47)
            note=txt('원 · 타원 · 열린 궤도',26,ELLIPSE).move_to([0,-3.3,0])
            return VGroup(h,visual,note)
        if i==1:
            h=self.title('평면의 기울기가 곡선을 바꾼다','원뿔의 절단')
            self.cut_angle=ValueTracker(0)
            diagram=always_redraw(lambda:self.cone(self.cut_angle.get_value()))
            label=always_redraw(lambda:txt(NAMES[0 if self.cut_angle.get_value()<.12 else
                                               1 if self.cut_angle.get_value()<.88 else
                                               2 if self.cut_angle.get_value()<1.12 else 3],
                                          31,COLORS[0 if self.cut_angle.get_value()<.12 else
                                                    1 if self.cut_angle.get_value()<.88 else
                                                    2 if self.cut_angle.get_value()<1.12 else 3]).move_to([0,-3.75,0]))
            note=txt('이중 원뿔  +  절단 평면',23,MUTED).move_to([0,-4.5,0])
            return VGroup(h,diagram,label,note)
        if i==2:
            h=self.title('원뿔곡선은 궤도에서도 나타난다','같은 네 곡선')
            gallery=self.gallery()
            note=txt('원뿔의 절단   ↔   중력 아래의 궤도',24,PARABOLA).move_to([0,-3.85,0])
            self.fit(note)
            return VGroup(h,gallery,note)
        if i==3:
            h=self.title('중력은 운동 방향을 휘게 한다','하나의 중력 중심')
            self.orbit_theta=ValueTracker(-.55)
            visual=always_redraw(lambda:self.orbit(.47,self.orbit_theta.get_value(),arrows=True,straight=True))
            legend=VGroup(txt('파랑  순간 속도',22,ELLIPSE),txt('주황  태양을 향한 중력',22,SUN)).arrange(DOWN,buff=.2).move_to([0,-3.8,0])
            return VGroup(h,visual,legend)
        if i==4:
            h=self.title('출발 속도로 달라지는 궤도','같은 출발 위치')
            self.ecc=ValueTracker(0)
            visual=always_redraw(lambda:self.orbit(self.ecc.get_value(),theta=.6))
            label=always_redraw(lambda:txt(f'e = {self.ecc.get_value():.2f}  ·  '+
                    NAMES[0 if self.ecc.get_value()<.08 else 1 if self.ecc.get_value()<.95 else 2 if self.ecc.get_value()<1.1 else 3],
                    26,COLORS[0 if self.ecc.get_value()<.08 else 1 if self.ecc.get_value()<.95 else 2 if self.ecc.get_value()<1.1 else 3]).move_to([0,-3.6,0]))
            speed=always_redraw(lambda:txt(f'같은 시작점  ·  출발 속도 {math.sqrt(1+self.ecc.get_value()):.2f} × 원궤도 속도',
                                         21,MUTED).move_to([0,-4.4,0]))
            self.fit(speed)
            return VGroup(h,visual,label,speed)
        if i==5:
            h=self.title('타원의 두 초점','기하학적 질문')
            self.phi=ValueTracker(.5)
            geometry=always_redraw(lambda:self.focus_geometry(self.phi.get_value(),second=True,distances=True))
            f=tex(r'PF_1+PF_2=2a',38,ELLIPSE).move_to([0,-3.4,0])
            note=txt('태양 F₁   ·   다른 초점 F₂ ?',24,HYPERBOLA).move_to([0,-4.2,0])
            return VGroup(h,geometry,f,note)
        if i==6:
            h=self.title('두 번째 초점은 힘의 원인이 아니다','원인과 결과')
            self.reveal=ValueTracker(0)
            geometry=always_redraw(lambda:self.focus_geometry(.95,second=self.reveal.get_value()>.5,gravity=True))
            first=txt('태양의 중력 → 궤도 형성',24,SUN).move_to([0,-3.55,0])
            second=txt('형성된 타원 → 두 번째 초점',24,HYPERBOLA).move_to([0,-4.25,0])
            second.set_opacity(0)
            return VGroup(h,geometry,first,second)
        if i==7:
            h=self.title('왜 원뿔곡선이 나타날까?','역제곱 중력')
            sun=Dot([-2.7,1.35,0],color=SUN,radius=.17)
            dots=VGroup(*[Dot([-2.7+d,1.35,0],color=WHITE,radius=.07) for d in (1,2,3)])
            rays=VGroup(*[Line(sun.get_center(),d.get_center(),color=EDGE,stroke_width=2) for d in dots])
            labels=VGroup(txt('r → F',22,ELLIPSE),txt('2r → F/4',22,PARABOLA),txt('3r → F/9',22,HYPERBOLA)).arrange(DOWN,buff=.25).move_to([0,-.35,0])
            gravity_eq=tex(r'F=\frac{GMm}{r^2}',43,SUN).move_to([0,-2.0,0])
            bridge=txt('운동방정식 + 각운동량 보존',21,MUTED).move_to([0,-2.95,0])
            orbit_eq=tex(r'r=\frac{p}{1+e\cos\theta}',40,CIRCLE).move_to([0,-3.95,0])
            gravity_eq.set_opacity(0);bridge.set_opacity(0);orbit_eq.set_opacity(0)
            return VGroup(h,sun,dots,rays,labels,gravity_eq,bridge,orbit_eq)
        if i==8:
            h=self.title('이심률 하나로 네 가지 궤도','e의 역할')
            eq=tex(r'r=\frac{p}{1+e\cos\theta}',42,CIRCLE).move_to([0,4.5,0])
            gallery=self.gallery().move_to([0,.4,0])
            conditions=VGroup(*[txt(s,22,c) for s,c in
                                [('e = 0  원',CIRCLE),('0 < e < 1  타원',ELLIPSE),
                                 ('e = 1  포물선',PARABOLA),('e > 1  쌍곡선',HYPERBOLA)]]).arrange(DOWN,buff=.12).move_to([0,-3.75,0])
            return VGroup(h,eq,gallery,conditions)
        h=self.title('다른 출발점, 같은 곡선','기하학 × 중력')
        cone=self.cone(.55).scale(.54).move_to([0,2.8,0])
        orbit=self.orbit(.47).scale(.53).move_to([0,-.45,0])
        left=txt('원뿔을 자르는 평면',23,ELLIPSE).move_to([0,.85,0])
        right=txt('태양의 중력과 초기 속도',23,SUN).move_to([0,-2.65,0])
        conclusion=txt('서로 다른 과정, 동일한 원뿔곡선',25,PARABOLA).move_to([0,-4.1,0]);self.fit(conclusion)
        return VGroup(h,cone,orbit,left,right,conclusion)

    def phase(self,t):
        for i,end in enumerate(ENDS):
            if t<end:return i
        return len(ENDS)-1

    def construct(self):
        footer=Rectangle(width=9,height=2.12,fill_color=PANEL,fill_opacity=1,stroke_width=0).move_to([0,-6.9,0]).set_z_index(-5)
        rule=Line([-3.95,5.85,0],[3.95,5.85,0],color=EDGE,stroke_width=1).set_z_index(-5)
        self.add(footer,rule)
        visual=None;caption=None;last=-1;start=0
        for end,sentence in DATA['sentences']:
            phase=self.phase(start);animations=[]
            if phase!=last:
                new=self.scene_for(phase)
                if visual is not None:animations.append(FadeOut(visual))
                animations.append(FadeIn(new));visual=new;last=phase
            new_caption=VGroup(*[txt(line,28) for line in wrap(sentence)]).arrange(DOWN,buff=.11)
            self.fit(new_caption,8)
            new_caption.move_to([0,-6.6,0])
            if caption is not None:animations.append(FadeOut(caption))
            animations.append(FadeIn(new_caption));caption=new_caption
            duration=end-start;intro=min(.35,duration*.23)
            self.play(*animations,run_time=intro)
            extra=0
            if phase==0 and start==8:
                extra=.6
                self.play(Transform(visual[1],self.cone(0)),run_time=extra)
            elif phase==1 and start in (14,20,25):
                extra=min(2.1,duration-intro-.1)
                target={14:.5,20:1.0,25:1.8}[start]
                self.play(self.cut_angle.animate.set_value(target),run_time=extra)
            elif phase==3 and start in (48,55):
                extra=min(2,duration-intro-.1)
                self.play(self.orbit_theta.animate.set_value(.25 if start==48 else .95),run_time=extra)
            elif phase==4 and start in (65,70):
                if start==65:
                    extra=1.8;self.play(self.ecc.animate.set_value(.47),run_time=extra)
                else:
                    extra=3.1
                    self.play(self.ecc.animate.set_value(1),run_time=1.5)
                    self.play(self.ecc.animate.set_value(1.5),run_time=1.6)
            elif phase==5 and start in (85,90):
                extra=min(2.2,duration-intro-.1)
                self.play(self.phi.animate.set_value(1.6 if start==85 else 2.6),run_time=extra)
            elif phase==6 and start==107:
                extra=1.2
                self.play(self.reveal.animate.set_value(1),visual[3].animate.set_opacity(1),run_time=extra)
            elif phase==7 and start==133:
                extra=.7;self.play(visual[5].animate.set_opacity(1),run_time=extra)
            elif phase==7 and start==140:
                extra=1.3;self.play(visual[6].animate.set_opacity(1),visual[7].animate.set_opacity(1),run_time=extra)
            self.wait(duration-intro-extra)
            start=end
