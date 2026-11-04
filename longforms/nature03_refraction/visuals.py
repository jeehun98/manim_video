"""Shared ray/phase data; propagate first, select the observation point later."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from physics import A,B,V1,V2,N1,N2,STAR,STRAIGHT,TMIN,DIR1,DIR2,SLOW1,SLOW2,OMEGA,time,times,metrics,front_segments,phasors,ray_exit
P=Path(__file__).resolve().parent;SHORT=os.environ.get('LIGHT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#091421'
TEAL='#35C9D0';BLUE='#579BE8';GOLD='#E3A447';GREEN='#3BC58B';MUTED='#8EA9BB';WHITE='#F2F6FA';RED='#ED7681'
SCALE=1.12 if SHORT else 1.05;CENTER=np.array([0,0,1.05 if SHORT else .65])
def txt(s,size=27,color=WHITE,width=8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def point(p,scale=SCALE,center=CENTER,depth=0):return np.array([p[0],depth,p[1]])*scale+np.array(center)
def ball(p,col=GOLD,r=.065):return Sphere(center=p,radius=r,resolution=(4,8),checkerboard_colors=[col,col],fill_opacity=1,stroke_width=0)
def path(x=STAR,color=GOLD,scale=SCALE,center=CENTER,width=5,end=B):
    return VGroup(Line(point(A,scale,center),point([x,0],scale,center),color=color,stroke_width=width),Line(point([x,0],scale,center),point(end,scale,center),color=color,stroke_width=width))
def direction_arrow(p,v,color=GOLD,length=.75):
    p=np.asarray(p);v=np.asarray(v);v=v/np.linalg.norm(v);q=p+length*v
    return VGroup(Line(p,q,color=color,stroke_width=4),Cone(direction=v,height=.13,base_radius=.05,resolution=(3,8),checkerboard_colors=[color,color],fill_opacity=1,stroke_width=0).shift(q))
def wavefronts(tau=0,scale=SCALE,center=CENTER,three_d=True,levels=None):
    if levels is None:levels=tau+np.arange(-5,5)*(12*TAU/OMEGA)
    g=VGroup()
    for level in levels:
        for j,p,q in front_segments(level):
            col=BLUE if j==0 else TEAL
            if three_d:
                verts=[point(p,scale,center,-.55),point(q,scale,center,-.55),point(q,scale,center,.55),point(p,scale,center,.55)]
                g.add(Polygon(*verts,color=col,stroke_width=.6,fill_color=col,fill_opacity=.16),Line(point(p,scale,center),point(q,scale,center),color=col,stroke_width=2.6))
            else:g.add(Line(point(p,scale,center),point(q,scale,center),color=col,stroke_width=2.7))
    return g
def mini_catenoid(center,scale=.7):
    c=np.array(center)
    return VGroup(Surface(lambda z,t:np.array([np.cosh(z)*np.cos(t),np.cosh(z)*np.sin(t),z])*scale+c,u_range=[-.8,.8],v_range=[0,TAU],resolution=(10,24),checkerboard_colors=[TEAL,TEAL],fill_opacity=.5,stroke_width=.25,stroke_color=TEAL),*[ParametricFunction(lambda t,z=z:np.array([np.cosh(.8)*np.cos(t),np.cosh(.8)*np.sin(t),z])*scale+c,t_range=[0,TAU],color=WHITE,stroke_width=3) for z in [-.8,.8]])

class LightBase(ThreeDScene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.target_seconds=self.m['duration_seconds']
        self.set_camera_orientation(phi=74*DEGREES,theta=-76*DEGREES)
        self.fixed(txt('자연의 최적화  03   /   REFRACTION',18,MUTED,8 if SHORT else 14).move_to([0,7.25 if SHORT else 3.97,0]),txt(self.m['title'],30,WHITE,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.28,0]))
        self.fixed(Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7,2.82,0],[7,2.82,0],color=MUTED,stroke_opacity=.25))
        self.shot()
        for m in self.mobjects:m.clear_updaters(recursive=True)
        left=self.target_seconds-self.time
        if left<-.025:raise RuntimeError(f'{self.INDEX+1}: {self.time} > {self.target_seconds}')
        if left>.001:self.wait(left)
    def fixed(self,*m):self.add_fixed_in_frame_mobjects(*m)
    def billboard(self,s,p,size=21,color=WHITE):
        m=txt(s,size,color).move_to(p);self.add_fixed_orientation_mobjects(m);return m
    def marker(self,p,name,scale=SCALE,center=CENTER,color=WHITE):
        q=point(p,scale,center);return VGroup(ball(q,color),self.billboard(name,q+OUT*.22+LEFT*.12,22,color))
    def info(self,s,note='',color=TEAL):
        g=VGroup(txt(s,31,color,8 if SHORT else 14).move_to([0,-3.15 if SHORT else -1.95,0]))
        if note:g.add(txt(note,19,MUTED,8 if SHORT else 14).move_to([0,-4.05 if SHORT else -2.5,0]))
        self.fixed(g);return g
    def note(self,s):self.fixed(txt(s,16,MUTED,8 if SHORT else 14).move_to([0,-4.85 if SHORT else -2.95,0]))
    def go(self,*m,t=1):self.play(*m,run_time=t)
    def front_camera(self):self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES)
    def base(self,b=True,scale=SCALE,center=CENTER,tank=False,source=True,labels=True):
        g=VGroup()
        if tank:
            box=Prism(dimensions=[6.4,1.4,1.7],fill_color=TEAL,fill_opacity=.045,stroke_color=TEAL,stroke_opacity=.25,stroke_width=.8).scale(scale).move_to(point([0,-.85],scale,center));g.add(box)
            g.add(Polygon(*[point([x,0],scale,center,d) for x,d in [(-3.2,-.7),(3.2,-.7),(3.2,.7),(-3.2,.7)]],fill_color=TEAL,fill_opacity=.1,stroke_width=.8,stroke_color=TEAL))
        else:g.add(Polygon(*[point(p,scale,center) for p in [[-3.2,0],[3.2,0],[3.2,-1.7],[-3.2,-1.7]]],fill_color=TEAL,fill_opacity=.075,stroke_width=0))
        g.add(Line(point([-3.2,0],scale,center),point([3.2,0],scale,center),color=TEAL,stroke_width=2))
        if labels:
            g.add(self.billboard('공기',point([-2.95,.6],scale,center),18,MUTED),self.billboard('물',point([-2.95,-.6],scale,center),18,TEAL))
        if source:g.add(self.marker(A,'A',scale,center) if b else ball(point(A,scale,center),WHITE,.085))
        if b:g.add(self.marker(B,'B',scale,center))
        self.add(g);return g
    def fan(self,scale=SCALE,center=CENTER):
        xs=np.r_[np.linspace(-1.8,1.6,8),STAR];g=VGroup()
        for x in xs:
            ray=path(float(x),GOLD if abs(x-STAR)<1e-7 else BLUE,scale,center,3 if abs(x-STAR)<1e-7 else 1.7,end=ray_exit(x))
            if abs(x-STAR)>1e-7:ray.set_stroke(opacity=.4)
            g.add(ray)
        return g
    def angles(self,scale=SCALE,center=CENTER):
        t1=float(np.arctan2(DIR1[0],-DIR1[1]));t2=float(np.arctan2(DIR2[0],-DIR2[1]));g=VGroup(DashedLine(point([STAR,1.2],scale,center),point([STAR,-1.25],scale,center),color=MUTED,dash_length=.1))
        for th,start,col in [(t1,PI/2,BLUE),(t2,-PI/2,TEAL)]:g.add(ParametricFunction(lambda u,start=start:point([STAR+.52*np.cos(start+u),.52*np.sin(start+u)],scale,center),t_range=[0,th],color=col,stroke_width=3))
        g.add(self.billboard('θ₁',point([STAR-.46,.76],scale,center),23,BLUE),self.billboard('θ₂',point([STAR+.43,-.72],scale,center),23,TEAL));self.add(g);return g
    def math_geometry(self):
        self.front_camera();scale=1. if SHORT else .78;center=np.array([0,0,2.55]) if SHORT else np.array([-3.45,0,.55]);self.base(True,scale,center);return scale,center
    def time_graph(self):
        c=[0,-.72,0] if SHORT else [3.4,.45,0]
        ax=Axes(x_range=[-1.4,2.8,1],y_range=[6,7.3,.5],x_length=5.6 if SHORT else 4.9,y_length=1.7 if SHORT else 2.,axis_config={'include_tip':False,'color':MUTED,'stroke_width':1}).move_to(c)
        curve=ax.plot(lambda x:float(time(x)),x_range=[-1.4,2.8],color=TEAL,stroke_width=3)
        self.fixed(ax,curve,txt('경계 통과 위치 x',17,MUTED).next_to(ax,DOWN,buff=.1),txt('총 이동 시간 T(x)',18,MUTED).next_to(ax,UP,buff=.1))
        return ax
    def time_readout(self,x,position=None):
        a,b=times(x);pos=position if position is not None else [0,-1.7 if SHORT else -1.25,0]
        return txt(f'T = {a:.4f} + {b:.4f} = {a+b:.4f}',25,GOLD,8 if SHORT else 13).move_to(pos)
    def phase_panel(self,center):
        xs,z=phasors(center);g=VGroup()
        for j,v in enumerate(z):
            col=j%3;row=j//3;c=np.array([(col-1)*.96,(.76-row*.8),0]) if SHORT else np.array([3.4+(col-1)*.96,1.6-row*.8,0])
            q=c+.29*np.array([v.real,v.imag,0]);g.add(Circle(radius=.32,color=MUTED,stroke_width=.8,stroke_opacity=.45).move_to(c),Arrow(c,q,buff=0,color=BLUE,stroke_width=2.3,max_tip_length_to_length_ratio=.3))
        c=np.array([0,-1.8,0]) if SHORT else np.array([3.4,-1.0,0]);total=z.mean();radius=.4 if SHORT else .3
        g.add(Circle(radius=radius,color=MUTED,stroke_width=1).move_to(c),Line(c,c+radius*np.array([total.real,total.imag,0]),color=GOLD,stroke_width=5),txt(f'|Σ 기여| / N = {abs(total):.3f}',21,GOLD,6).move_to([c[0],-2.5 if SHORT else -1.5,0]))
        return g
    def shot(self):
        i=self.INDEX
        if i==0:
            self.base(False,tank=True);fan=self.fan();self.go(LaggedStart(*[Create(r) for r in fan],lag_ratio=.08),t=2.8);self.info('빛이 먼저 전파된다','아직 선택된 도착점은 없다')
        elif i==1:
            self.base(False,tank=True);self.add(path(STAR,end=ray_exit(STAR)));self.angles();self.info('REFRACTION · 굴절','각도는 물 표면의 법선을 기준으로 잰다');self.move_camera(theta=-90*DEGREES,run_time=1.4)
        elif i==2:
            self.base(False,tank=True);fan=self.fan();self.add(fan);self.info('전파 → 관찰점 선택','B는 빛이 미리 정한 목적지가 아니다');self.wait(4)
            b=self.marker(B,'B',color=WHITE);a=self.marker(A,'A');self.go(FadeIn(b),FadeIn(a),t=.7)
        elif i==3:
            self.front_camera();self.base();self.add(path());straight=DashedLine(point(A),point(B),color=MUTED,dash_length=.12);self.go(Create(straight),t=.7)
            self.fixed(txt(f'직선 거리  {metrics(STRAIGHT)["distance"]:.4f}',23,MUTED).move_to([-1.95,-1.45 if SHORT else -1.1,0]),txt(f'굴절 거리  {metrics(STAR)["distance"]:.4f}',23,GOLD).move_to([1.95,-1.45 if SHORT else -1.1,0]))
            self.info('직선은 짧지만, 빛의 경로와 다르다','회색 점선은 비교를 위한 가상의 경로')
        elif i==4:
            self.front_camera();self.base(False,source=False);t=ValueTracker(0)
            g=always_redraw(lambda:VGroup(Line(point([-2.2,.9]),point([-2.2+t.get_value(),.9]),color=BLUE,stroke_width=7),Line(point([-2.2,-.8]),point([-2.2+.75*t.get_value(),-.8]),color=TEAL,stroke_width=7),ball(point([-2.2+t.get_value(),.9]),BLUE),ball(point([-2.2+.75*t.get_value(),-.8]),TEAL)))
            self.add(g);self.info('상대 속력  공기 : 물 = 1 : 0.75','같은 시간 동안 물속에서 진행하는 거리가 짧다');self.note('등방성·비분산 매질의 상대 위상속력 모형');self.go(t.animate.set_value(4.3),t=3.5)
        elif i==5:
            self.front_camera();self.base();self.add(path(),DashedLine(point(A),point(B),color=MUTED,dash_length=.12))
            s=metrics(STRAIGHT);r=metrics(STAR)
            y=-1.35 if SHORT else -1.0;gap=.6 if SHORT else .45
            self.fixed(txt(f'직선: {s["t_air"]:.4f} + {s["t_water"]:.4f} = {s["time"]:.4f}',23,MUTED).move_to([0,y,0]),txt(f'굴절: {r["t_air"]:.4f} + {r["t_water"]:.4f} = {r["time"]:.4f}',23,GOLD).move_to([0,y-gap,0]))
            self.info('T = d_air/v_air + d_water/v_water','같은 A와 B · 같은 속력으로 계산한 상대 시간');self.note('더 긴 거리여도 물속 구간이 짧으면 총시간이 줄어든다')
        elif i==6:
            self.front_camera();self.base();self.add(path());candidates=VGroup(*[path(x,MUTED,width=1.1) for x in np.linspace(-1.3,2.6,15)])
            self.go(LaggedStart(*[Create(r) for r in candidates],lag_ratio=.025),t=2.5);self.info('가정: 모든 후보를 계산한다면?', '사고실험 · 실제 빛의 작동 방식이 아님',GOLD);self.go(FadeOut(candidates),t=.7)
        elif i==7:
            self.base(False,tank=True);fan=self.fan();self.info('빛의 전파가 먼저다','전파된 빛 가운데 한 지점을 나중에 고른다');self.go(LaggedStart(*[Create(r) for r in fan],lag_ratio=.08),t=3);self.wait(1)
            self.go(FadeIn(self.marker(B,'B')),t=.7)
        elif i==8:
            self.front_camera();self.base(False,source=False);ray=path();self.add(ray);waves=wavefronts(0,three_d=False);self.go(FadeOut(ray),FadeIn(waves),t=1.4);self.info('파면 = 같은 위상을 가진 점들의 면','광선의 진행 방향은 파면에 수직이다')
        elif i in [9,10,11,12]:
            self.base(False,tank=True,source=False)
            tau=ValueTracker(-2.0 if i==9 else -.5)
            waves=always_redraw(lambda:wavefronts(tau.get_value(),three_d=i!=12));self.add(waves)
            if i==9:
                self.add(direction_arrow(point([-.5,.9]),[DIR1[0],0,DIR1[1]]));self.info('비스듬히 도착하는 3D 파면','같은 주파수 · 경계에 평행한 파수 성분은 연속');self.note('국소 평면파 모형 · 같은 위상면을 일정 간격으로 발췌')
                self.go(tau.animate.set_value(1.3),t=4.7)
            elif i==10:
                self.info('같은 시간: 공기에서 더 멀리, 물에서 더 짧게','파면은 임의 변형이 아니라 매질별 위상장으로 계산');self.note('v₂ < v₁ · 주파수는 같고 물속 파장은 더 짧다');self.go(tau.animate.set_value(2.0),t=4.8)
            elif i==11:
                self.info('국소적인 전파 속력 차이 → 굴절','각 매질에서 파면의 법선과 진행 방향이 일치한다');self.add(path());self.go(tau.animate.set_value(.8),t=1.5);self.move_camera(phi=90*DEGREES,theta=-90*DEGREES,run_time=1)
            else:
                self.front_camera();self.info('목적지 없이, 매질에 따라 전파된다','B는 전파를 관찰한 뒤 선택하는 지점');self.go(tau.animate.set_value(1.3),t=2.8);waves.clear_updaters();self.go(FadeOut(waves),FadeIn(path()),t=.6);self.go(FadeIn(self.marker(B,'B')),t=.5)
        elif i==13:
            self.front_camera();self.base();self.add(path());self.info('물리적 전파 → 수학적 경로 분석','이제 고정된 A와 B 사이의 경로를 비교한다');self.note('후보 형태를 바꾸는 비교는 실제 시간 전파와 다르다')
        elif i in [14,15]:
            scale,center=self.math_geometry();x=ValueTracker(-.8 if i==14 else STAR-.75)
            ray=always_redraw(lambda:path(x.get_value(),GOLD,scale,center));dot=always_redraw(lambda:ball(point([x.get_value(),0],scale,center),GOLD));self.add(ray,dot)
            cname=self.billboard('C',point([x.get_value(),0],scale,center)+OUT*.25+RIGHT*.12,21,GOLD)
            cname.add_updater(lambda m:m.move_to(point([x.get_value(),0],scale,center)+OUT*.25+RIGHT*.12))
            ax=self.time_graph();cursor=always_redraw(lambda:Dot(ax.c2p(x.get_value(),float(time(x.get_value()))),radius=.055,color=GOLD));self.fixed(cursor)
            readout=always_redraw(lambda:self.time_readout(x.get_value(),[0,-2.25 if SHORT else -1.2,0]));self.fixed(readout)
            if i==14:
                self.info('A와 B는 고정 · 통과 위치 C만 변경','경로와 시간 그래프를 같은 x 값으로 갱신한다');self.go(x.animate.set_value(2.5),t=4);self.go(x.animate.set_value(STAR),t=1.6)
            else:
                self.info('페르마의 원리: δT = 0','이 평면 경계 예시에서는 최소시간이 된다');self.note('일반적인 페르마 원리는 전역 최소가 아니라 정지 조건')
                self.go(x.animate.set_value(STAR),t=3.1)
                tangent=Line(ax.c2p(STAR-.55,TMIN),ax.c2p(STAR+.55,TMIN),color=GOLD,stroke_width=4);self.fixed(tangent,txt('dT/dx = 0',23,GOLD).move_to(ax.c2p(STAR,TMIN)+[0,.5,0]))
        elif i==16:
            self.front_camera();self.base();self.add(path());self.angles();self.info('n₁ sin θ₁ = n₂ sin θ₂','페르마의 정지시간 조건이 스넬 법칙으로 이어진다');self.note('법선 기준의 각도 · n = c/v')
            self.fixed(txt('sin θ₁ / v₁ = sin θ₂ / v₂',24,BLUE).move_to([0,-1.25 if SHORT else -1.15,0]))
        elif i in [17,18]:
            self.front_camera();scale=.76 if SHORT else .78;center=np.array([0,0,3.05]) if SHORT else np.array([-3.45,0,.55]);self.base(True,scale,center)
            tracker=ValueTracker(-.5)
            def candidates():
                xs,_=phasors(tracker.get_value());return VGroup(*[path(float(x),MUTED,scale,center,1).set_stroke(opacity=.45) for x in xs])
            rays=always_redraw(candidates);self.add(rays);panel=always_redraw(lambda:self.phase_panel(tracker.get_value()));self.fixed(panel)
            self.info('위상 φⱼ = ωTⱼ' if i==17 else '정지시간 근처의 위상 기여가 두드러진다','동일 진폭의 수학적 위상합 모형 · 광선의 경쟁 과정이 아님');self.note('짧은 파장 근사 · 다른 기여가 정확히 0이 되는 것은 아님')
            if i==17:self.wait(2)
            else:
                self.wait(1);self.go(tracker.animate.set_value(STAR),t=4);self.wait(1.5);rays.clear_updaters();self.go(FadeOut(rays),FadeIn(path(STAR,GOLD,scale,center)),t=1)
        elif i in [19,20]:
            self.front_camera();sep=2.05 if SHORT else 3.4;sc=.55 if SHORT else .75;z=2.05 if SHORT else .85;lc=np.array([-sep,0,z]);rc=np.array([sep,0,z])
            left=self.base(False,sc,lc,source=False,labels=False);right=self.base(True,sc,rc,labels=False);lray=path(STAR,GOLD,sc,lc);rray=path(STAR,GOLD,sc,rc);self.add(lray,rray)
            self.fixed(txt('물리적 전파',23,BLUE,3.6).move_to([-sep,4.05 if SHORT else 2.55,0]),txt('수학적 해석',23,TEAL,3.6).move_to([sep,4.05 if SHORT else 2.55,0]))
            ax=Axes(x_range=[-1.4,2.8,2],y_range=[6,7.3,1],x_length=2.4,y_length=.65,axis_config={'include_tip':False,'color':MUTED,'stroke_width':1}).move_to([sep,.1 if SHORT else -.95,0])
            mini_graph=VGroup(ax,ax.plot(lambda x:float(time(x)),x_range=[-1.4,2.8],color=TEAL,stroke_width=2),Dot(ax.c2p(STAR,TMIN),color=GOLD,radius=.045),txt('δT = 0',21,GOLD).move_to([sep,-.75 if SHORT else -1.45,0]));self.fixed(mini_graph)
            if i==19:
                tau=ValueTracker(-.7);waves=always_redraw(lambda:wavefronts(tau.get_value(),sc,lc,False));self.add(waves);self.info('매질에 따른 파동 전파  /  이동 시간의 정지','서로 다른 관점으로 같은 굴절을 기술한다');self.go(tau.animate.set_value(.7),t=3.5)
            else:
                waves=wavefronts(0,sc,lc,False);self.add(waves)
                self.go(FadeOut(left),FadeOut(right),FadeOut(waves),FadeOut(mini_graph),lray.animate.shift(RIGHT*sep),rray.animate.shift(LEFT*sep),t=2.2);self.info('δT = 0','국소적 전파와 전역적 정지 조건');self.note('빛이 후보를 계산하는 최적화 알고리즘을 실행하는 것은 아님')
        else:
            self.set_camera_orientation(phi=78*DEGREES,theta=-80*DEGREES)
            sep=2.65 if SHORT else 4.5;z=1.5 if SHORT else .65
            self.add(mini_catenoid((-sep,0,z),.56 if SHORT else .65))
            chain_scale=1. if SHORT else 1.3
            self.add(ParametricFunction(lambda x:np.array([x*chain_scale,0,(np.cosh(x)-1.17)*chain_scale+z]),t_range=[-.8,.8],color=TEAL,stroke_width=5))
            scale=.34 if SHORT else .45;center=np.array([sep,0,z]);self.base(False,scale,center,source=False,labels=False);self.add(path(STAR,GOLD,scale,center,3))
            self.fixed(txt('표면에너지',19,TEAL,2.5).move_to([-sep,-.05 if SHORT else -.6,0]),txt('위치에너지',19,TEAL,2.5).move_to([0,-.05 if SHORT else -.6,0]),txt('이동 시간',19,GOLD,2.5).move_to([sep,-.05 if SHORT else -.6,0]))
            self.fixed(txt('자연의 최적화',38,GREEN).move_to([0,-1.55 if SHORT else -1.25,0]));self.info('국소적인 물리법칙 → 전체적인 수학적 조건','최적의 결과를 미리 계산하거나 목적지를 아는 것이 아니다');self.note('서로 다른 물리적 기작을 같은 정지 조건의 언어로 기술할 수 있다')
