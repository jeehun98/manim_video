"""Orthographic projections of 3D vortex geometry, with explicit toy models."""
from pathlib import Path
import json
from manim import *

ROOT=Path(__file__).resolve().parent
config.background_color='#081622'
config.frame_width=14.222222222
config.frame_height=8
INK,MUTED,CYAN,GREEN,GOLD,PINK='#EAF5FB','#8FAABD','#51D8EE','#8BE0B1','#F4C978','#F28A9F'
FONT='Malgun Gothic'

def txt(s,size=27,color=INK,width=12):
    t=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.15)
    if t.width>width:t.scale_to_fit_width(width)
    return t

def project(p,tilt=1.12):
    x,y,z=p
    q=np.array([x,np.cos(tilt)*y+np.sin(tilt)*z,0.])
    a=-.12
    return np.array([np.cos(a)*q[0]-np.sin(a)*q[1],np.sin(a)*q[0]+np.cos(a)*q[1],0.])

def tube(stretch=1,phase=0,center=(-2,.1,0),tilt=1.12,color=CYAN,radius=.85,length=1.7,opacity=.7):
    r=radius/np.sqrt(stretch);l=length*stretch;c=np.array(center)
    rings=VGroup()
    # All points live on an actual 3D cylinder before orthographic projection.
    for z in np.linspace(-l/2,l/2,9):
        ring=VMobject(stroke_color=color,stroke_width=1.8,stroke_opacity=opacity,fill_opacity=0)
        ring.set_points_as_corners([c+project([r*np.cos(t),r*np.sin(t),z],tilt) for t in np.linspace(0,TAU,49)])
        rings.add(ring)
    walls=VGroup()
    for t in np.linspace(0,TAU,9)[:-1]:
        walls.add(Line(c+project([r*np.cos(t),r*np.sin(t),-l/2],tilt),c+project([r*np.cos(t),r*np.sin(t),l/2],tilt),color=color,stroke_width=1,stroke_opacity=.24))
    cap=Polygon(*[c+project([r*np.cos(t),r*np.sin(t),l/2],tilt) for t in np.linspace(0,TAU,49)],stroke_width=0,fill_color=color,fill_opacity=.1)
    dots=VGroup()
    for z in [-l*.32,0,l*.32]:
        for t in np.arange(4)*TAU/4:
            angle=t+phase
            dots.add(Dot(c+project([r*np.cos(angle),r*np.sin(angle),z],tilt),radius=.045,color=GOLD))
    tangents=VGroup()
    for z in [-l*.32,l*.32]:
        t=phase
        p=c+project([r*np.cos(t),r*np.sin(t),z],tilt)
        q=c+project([r*np.cos(t+.35),r*np.sin(t+.35),z],tilt)
        tangents.add(Arrow(p,q,buff=0,color=GOLD,stroke_width=2,max_tip_length_to_length_ratio=.32))
    return VGroup(cap,walls,rings,dots,tangents)

def plane(center=(0,.1,0),shear=0,scale=1):
    c=np.array(center);g=VGroup()
    for k in np.linspace(-2,2,9):
        g.add(Line(c+[-2*scale,k*scale,0],c+[2*scale,k*scale,0],color='#254554',stroke_width=1))
        g.add(Line(c+[k*scale,-2*scale,0],c+[k*scale,2*scale,0],color='#254554',stroke_width=1))
    patch=Polygon(*[c+scale*np.array([np.cos(t)+shear*np.sin(t),np.sin(t),0]) for t in np.linspace(0,TAU,80)],stroke_color=CYAN,stroke_width=3,fill_color=CYAN,fill_opacity=.12)
    rings=VGroup()
    for r in [.45,.75,1.]:
        rings.add(ParametricFunction(lambda t: c+scale*np.array([r*np.cos(t)+shear*r*np.sin(t),r*np.sin(t),0]),t_range=[0,TAU,.07],stroke_color=CYAN,stroke_width=1.5,fill_opacity=0))
    arrows=VGroup()
    for t in np.arange(8)*TAU/8:
        p=c+scale*np.array([.85*np.cos(t)+shear*.85*np.sin(t),.85*np.sin(t),0])
        tangent=scale*np.array([-.28*np.sin(t)+shear*.28*np.cos(t),.28*np.cos(t),0])
        arrows.add(Arrow(p,p+tangent,buff=0,color=CYAN,stroke_width=2,max_tip_length_to_length_ratio=.3))
    return VGroup(g,patch,rings,arrows)

def axis_marker(x=0,y=.1):
    return VGroup(Circle(radius=.14,color=GOLD,stroke_width=2),Dot(radius=.04,color=GOLD)).move_to([x,y,0])

def axial_flow(center=(-2,.1,0),stretch=1):
    c=np.array(center);l=1.7*stretch
    return VGroup(*[Arrow(c+project([0,0,sign*l/2]),c+project([0,0,sign*(l/2+.55)]),buff=0,color=PINK,stroke_width=3) for sign in [-1,1]])

def badge(s,x,y,color=CYAN,w=3.4):
    b=RoundedRectangle(width=w,height=.7,corner_radius=.1,stroke_color=color,stroke_width=1,fill_color=color,fill_opacity=.06)
    return VGroup(b,txt(s,23,color,w-.2)).move_to([x,y,0])

def heatpatch(x=0,spread=1,color=CYAN,scale=1):
    # Fixed-length vorticity support; spread is not material tube expansion.
    g=VGroup()
    for r in np.linspace(1.4,.08,20):
        alpha=.14/spread**2*np.exp(-r*r/(2*spread**2))
        g.add(Circle(radius=r*spread*scale,stroke_width=0,fill_color=color,fill_opacity=alpha).move_to([x,.1,0]))
    return g

class VortexScene(Scene):
    index=1
    def construct(self):
        m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
        self.timing=json.loads((ROOT/m['directory']/'timing.json').read_text(encoding='utf-8'))
        titles=['평면에서는 축을 늘릴 수 없다','회전의 방향과 강도 — 보티시티','평면을 벗어나면, 관이 보인다','길어지고, 가늘어지고, 강해진다','보티시티를 바꾸는 새로운 항','늘어남과 확산은 함께 작용한다','두 차원을 가르는 하나의 항']
        self.add(txt('NAVIER–STOKES × NEURAL NETWORKS',15,MUTED).move_to([-3.7,3.65,0]),txt(f'02막   /   {self.index:02} — {titles[self.index-1]}',29).move_to([0,3.15,0]))
        self.add(Line([-6.2,-2.85,0],[6.2,-2.85,0],color='#294958',stroke_width=1))
        self.caption=VGroup()
        self.progress=Line([-6.2,-3.8,0],[-6.19,-3.8,0],color=CYAN,stroke_width=3);self.add(self.progress)
        getattr(self,f'scene{self.index}')()
        duration=self.timing['duration']
        frames=round(duration*config.frame_rate)-round(self.time*config.frame_rate)
        if frames<0:raise ValueError(f'Scene overrun: {self.time}/{duration}')
        if frames:self.wait(frames/config.frame_rate)

    def cue(self,n,*animations,seconds=3):
        self.remove(self.caption);line=self.timing['lines'][n-1]
        if len(line)>46:
            spaces=[i for i,c in enumerate(line) if c==' ']
            if spaces:
                at=min(spaces,key=lambda i:abs(i-len(line)/2));line=line[:at]+'\n'+line[at+1:]
        self.caption=txt(line,23,width=12.1).move_to([0,-3.32,0]);self.add(self.caption)
        end=round(self.timing['ends'][n-1]*config.frame_rate)/config.frame_rate
        available=end-self.time
        if available<-.01:raise ValueError(f'Cue overrun: {n}')
        if animations:self.play(*animations,run_time=round(min(seconds,available)*config.frame_rate)/config.frame_rate)
        frames=round(end*config.frame_rate)-round(self.time*config.frame_rate)
        if frames>0:self.wait(frames/config.frame_rate)
        self.progress.put_start_and_end_on([-6.2,-3.8,0],[-6.2+12.4*end/self.timing['duration'],-3.8,0])

    def replace_label(self,label,string,color=INK,y=2.35):
        # Crossfade text so Korean glyphs never morph into illegible outlines.
        replacement=txt(string,27,color).move_to([0,y,0])
        return FadeTransform(label,replacement),replacement

    def scene1(self):
        p=plane(center=(-1.8,.1,0));mark=axis_marker(-1.8)
        self.add(p,mark)
        b=badge('2D：흐름은 평면 안에만',3,1.4,CYAN);self.add(b)
        self.cue(1)
        self.cue(2,Transform(p,plane(center=(-1.5,.1,0),shear=.85)),mark.animate.shift(RIGHT*.3),seconds=5)
        axis=Arrow([3,.1,0],[3,1,0],buff=0,color=GOLD)
        self.cue(3,FadeIn(badge('ω：평면에 수직인 회전축',3,-.2,GOLD)),Indicate(mark,color=GOLD),seconds=3)
        self.cue(4,FadeIn(badge('축 방향 속도 = 0',3,-1.35,PINK)),FadeIn(txt('(ω·∇)u = 0',31,GOLD).move_to([0,-2.35,0])),seconds=3)

    def scene2(self):
        disk=Circle(radius=1.15,stroke_color=CYAN,fill_color=CYAN,fill_opacity=.08).move_to([-2,.1,0])
        cross=VGroup(Line([-3.15,.1,0],[-.85,.1,0],color=GOLD),Line([-2,-1.05,0],[-2,1.25,0],color=GOLD))
        arrows=VGroup()
        for t in np.arange(8)*TAU/8:
            pos=np.array([-2+1.5*np.cos(t),.1+1.5*np.sin(t),0])
            arrows.add(Arrow(pos,pos+[-.5*np.sin(t),.5*np.cos(t),0],buff=0,color=CYAN,stroke_width=3))
        self.add(disk,cross)
        eq=Text('ω = ∇ × u',font=FONT,font_size=36,color=CYAN,t2w={'ω':BOLD,'u':BOLD}).move_to([2.7,1.5,0])
        self.cue(1,FadeIn(txt('와도 · 보티시티  /  Vorticity',25,CYAN,width=5.6).move_to([2.7,2.25,0])),seconds=2)
        self.cue(2,FadeIn(arrows),seconds=3)
        self.cue(3,Rotate(cross,angle=TAU,about_point=[-2,.1,0]),seconds=4)
        self.cue(4,FadeIn(eq),FadeIn(axis_marker(-2)),seconds=3)
        self.cue(5,FadeIn(txt('강체 회전 예시：ω = 2Ω',26,GOLD).move_to([2.7,.4,0])),Rotate(cross,angle=TAU,about_point=[-2,.1,0]),seconds=3)
        heat=VGroup(heatpatch(2,spread=.8),heatpatch(4.3,spread=.8,color=PINK))
        self.cue(6,FadeIn(heat),FadeIn(txt('ω > 0             ω < 0',21).move_to([3.2,-1.6,0])),seconds=3)

    def scene3(self):
        tilt=ValueTracker(0);length=ValueTracker(.08);phase=ValueTracker(0)
        body=always_redraw(lambda:tube(center=(0,.1,0),radius=1.1,tilt=tilt.get_value(),length=length.get_value(),phase=phase.get_value()))
        self.add(body)
        self.cue(1,tilt.animate.set_value(1.12),seconds=4)
        self.cue(2,length.animate.set_value(2.7),phase.animate.set_value(PI),seconds=5)
        axial=Arrow(project([0,0,-1])+[0,.1,0],project([0,0,1])+[0,.1,0],buff=0,color=GOLD)
        self.cue(3,FadeIn(axial),FadeIn(txt('회전은 둘레를 따라  /  보티시티는 축을 따라',25,GOLD).move_to([0,-2.3,0])),phase.animate.set_value(3*PI),seconds=4)
        pull=axial_flow(center=(0,.1,0),stretch=2.7/1.7)
        self.cue(4,FadeIn(pull),seconds=3)
        self.cue(5,Indicate(pull,color=PINK),FadeIn(txt('축 방향의 속도 차이',27,PINK).move_to([0,2.4,0])),phase.animate.set_value(5*PI),seconds=4)
        body.clear_updaters()

    def scene4(self):
        stretch=ValueTracker(1);phase=ValueTracker(0)
        body=always_redraw(lambda:tube(stretch.get_value(),phase.get_value(),center=(-2.3,.1,0)))
        pull=always_redraw(lambda:axial_flow(center=(-2.3,.1,0),stretch=stretch.get_value()))
        omega=always_redraw(lambda:Arrow(np.array([-2.3,.1,0])+project([0,0,-.48*stretch.get_value()]),np.array([-2.3,.1,0])+project([0,0,.48*stretch.get_value()]),buff=0,color=GOLD,stroke_width=4))
        self.add(body,omega)
        values=VGroup(badge('L = L₀',3,1.7),badge('A = A₀',3,.75),badge('r = r₀',3,-.2),badge('ω = ω₀',3,-1.15,GOLD))
        self.add(values)
        self.cue(1,phase.animate.set_value(PI),seconds=3)
        self.cue(2,FadeIn(pull),stretch.animate.set_value(1.25),phase.animate.set_value(2*PI),seconds=4)
        self.cue(3,stretch.animate.set_value(2),phase.animate.set_value(4*PI),FadeTransform(values[0],badge('L = 2L₀',3,1.7)),FadeTransform(values[1],badge('A = A₀ / 2',3,.75)),seconds=5)
        self.cue(4,FadeTransform(values[2],badge('r = r₀ / √2',3,-.2)),FadeIn(txt('V = A L = 일정',26,GREEN).move_to([0,-2.35,0])),phase.animate.set_value(6*PI),seconds=4)
        self.cue(5,FadeTransform(values[3],badge('ω = 2ω₀',3,-1.15,GOLD)),phase.animate.set_value(10*PI),seconds=5)
        self.cue(6,FadeIn(txt('Vortex Stretching',26,GOLD).move_to([0,2.55,0])),phase.animate.set_value(12*PI),seconds=4)
        self.cue(7)
        body.clear_updaters();pull.clear_updaters();omega.clear_updaters()

    def scene5(self):
        terms=VGroup(*[Text(s,font=FONT,font_size=29,color=c,t2w={'ω':BOLD,'u':BOLD}) for s,c in [('Dω/Dt',INK),('=',INK),('(ω·∇)u',GOLD),('+',INK),('ν∇²ω',GREEN)]]).arrange(RIGHT,buff=.22).move_to([0,2.25,0])
        self.add(txt('ν 일정 · ∇·u = 0 · ∇×f = 0',18,MUTED).move_to([0,2.7,0]))
        body=tube(center=(-3,.05,0),stretch=1.3);self.add(body)
        axis=Arrow([-3,-.6,0],[-3,.8,0],buff=0,color=GOLD);self.add(axis)
        self.cue(1,FadeIn(terms),seconds=3)
        braces=VGroup(Brace(terms[2],DOWN,color=GOLD),Brace(terms[4],DOWN,color=GREEN))
        labels=VGroup(txt('Vortex\nStretching',15,GOLD,width=2.2).next_to(braces[0],DOWN,buff=.07),txt('Viscous\nDiffusion',15,GREEN,width=2.2).next_to(braces[1],DOWN,buff=.07)).shift(DOWN*.05)
        self.cue(2,Indicate(terms[2],color=GOLD),FadeIn(braces),FadeIn(labels),seconds=3)
        alignment=VGroup(badge('늘어나는 방향에 정렬',2.7,.25,GOLD,w=4.2),txt('Dω/Dt = aω   (a > 0)',27,GOLD).move_to([2.7,-.65,0]))
        self.cue(3,FadeIn(alignment),Transform(axis,Arrow([-3,-.9,0],[-3,1.15,0],buff=0,color=GOLD)),seconds=4)
        self.cue(4,FadeTransform(alignment,VGroup(badge('압축 방향이면 약화 가능',2.7,.25,PINK,w=4.2),txt('방향과 정렬이 중요합니다',24,PINK).move_to([2.7,-.65,0]))),seconds=4)
        loop=VGroup(*[badge(s,x,-2.1,c,w=2.9) for s,x,c in [('보티시티 ω',-4.2,GOLD),('속도장 u',0,CYAN),('변형 ∇u',4.2,PINK)]])
        connections=VGroup(Arrow([-2.65,-2.1,0],[-1.55,-2.1,0],buff=0,color=MUTED),Arrow([1.55,-2.1,0],[2.65,-2.1,0],buff=0,color=MUTED),Line([4.2,-2.45,0],[4.2,-2.65,0],color=MUTED),Arrow([4.2,-2.65,0],[-4.2,-2.65,0],buff=0,color=MUTED,stroke_width=1.5),Line([-4.2,-2.65,0],[-4.2,-2.45,0],color=MUTED))
        self.cue(5,FadeIn(loop),FadeIn(connections),seconds=4)
        self.cue(6,FadeIn(txt('조건부 증폭 ≠ 끝없는 폭주',25,PINK).move_to([2.7,-1.25,0])),seconds=3)

    def scene6(self):
        a=tube(center=(-3,.1,0),radius=.62,length=1.7);b=tube(center=(3,.1,0),radius=.62,length=1.7,color=GREEN)
        self.add(a,b,txt('늘어남',26,GOLD).move_to([-3,2.4,0]),txt('점성 확산',26,GREEN).move_to([3,2.4,0]))
        self.cue(1)
        self.cue(2,Transform(a,tube(stretch=2,phase=PI,center=(-3,.1,0),radius=.62)),seconds=4)
        # Diffusion is a widening distribution, not an expanding material tube.
        clouds=VGroup(*[heatpatch(3,spread=1.4,color=GREEN,scale=.6).shift([0,y,0]) for y in [-.7,0,.7]])
        self.cue(3,FadeOut(b),FadeIn(clouds),FadeIn(txt('최고값 ↓  /  분포 폭 ↑',22,GREEN).move_to([3,-1.7,0])),seconds=4)
        combined=tube(center=(0,.1,0),stretch=1.4,color=CYAN)
        join=VGroup(Arrow([-3,1.9,0],[-.85,.85,0],buff=.1,color=GOLD),Arrow([3,1.9,0],[.85,.85,0],buff=.1,color=GREEN))
        self.cue(4,FadeOut(a),FadeOut(clouds),FadeIn(combined),FadeIn(join),seconds=4)
        self.cue(5,FadeIn(txt('늘어남의 크기뿐 아니라, 완화와의 경쟁',26).move_to([0,-2.35,0])),seconds=3)
        self.cue(6,FadeIn(badge('증폭률',-3.8,.1,GOLD,w=2.7)),FadeIn(badge('확산률 ∼ ν / ℓ²',3.8,.1,GREEN,w=3.2)),seconds=4)

    def scene7(self):
        left=VGroup(txt('2D',30,CYAN).move_to([-3,2.45,0]),txt('Dω/Dt = ν∇²ω',26,GREEN).move_to([-3,1.8,0]),plane(center=(-3,-.2,0),scale=.63))
        right=VGroup(txt('3D',30,GOLD).move_to([3,2.45,0]),txt('Dω/Dt = (ω·∇)u + ν∇²ω',24,GOLD,width=5.6).move_to([3,1.8,0]),tube(center=(3,-.2,0),length=1.45,radius=.65))
        divider=Line([0,-2.1,0],[0,2.5,0],color='#294958',stroke_width=1)
        self.add(left,right,divider)
        self.cue(1)
        self.cue(2,FadeIn(txt('stretching = 0',23,CYAN).move_to([-3,-1.85,0])),seconds=3)
        self.cue(3,FadeIn(txt('ν > 0 · 적절한 매끄러운 자료',19,MUTED).move_to([-3,-2.35,0])),seconds=3)
        self.cue(4,Transform(right[2],tube(center=(3,-.2,0),stretch=1.6,length=1.45,radius=.65,phase=PI)),seconds=4)
        self.cue(5,FadeIn(txt('방향에 따라 증폭·재배향',22,GOLD).move_to([3,-1.85,0])),seconds=3)
        self.cue(6,FadeIn(txt('보티시티 증가 ≠ 특이점의 증명',21,PINK,width=5.8).move_to([3,-2.35,0])),seconds=3)
        self.cue(7,FadeOut(left),FadeOut(right),FadeOut(divider),seconds=2)
        self.cue(8,FadeIn(txt('전체 에너지는 유한해도,\n아주 작은 영역의 강도는 끝없이 커질 수 있을까?',31,GOLD).move_to([0,.35,0])),seconds=1)
