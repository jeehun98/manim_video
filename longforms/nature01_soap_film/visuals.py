"""True 3-D surfaces, fixed-boundary comparisons, and computed area variation."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('SOAP_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#091421'
TEAL='#35C9D0';SILVER='#D8E1E8';BLUE='#579BE8';GOLD='#E3A447';GREEN='#3BC58B';RED='#ED7681';MUTED='#8EA9BB';WHITE='#F2F6FA'
R=float(np.cosh(.8));H=1.6
MACRO_SCALE=1.65 if SHORT else 1.35
MACRO_OFFSET=np.array([0.,0.,0. if SHORT else .42])
DATA=json.loads((P/'geometry.json').read_text(encoding='utf-8'))
def txt(s,size=28,color=WHITE,width=8):
    t=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if t.width>width:t.scale_to_fit_width(width)
    return t
def pos(z,t,blend=1,eps=0):
    r=R+blend*(np.cosh(z)-R)+eps*np.cos(np.pi*z/H)**2
    return np.array([r*np.cos(t),r*np.sin(t),z])
def surface(blend=1,eps=0,opacity=.52,color=TEAL,zrange=(-.8,.8),trange=(0,TAU),res=(14,32)):
    return Surface(lambda z,t:pos(z,t,blend,eps),u_range=zrange,v_range=trange,resolution=res,fill_opacity=opacity,checkerboard_colors=[color,color],stroke_color=color,stroke_width=.35,stroke_opacity=.25)
def ring(z):
    return ParametricFunction(lambda t:np.array([R*np.cos(t),R*np.sin(t),z]),t_range=[0,TAU],color=SILVER,stroke_width=6)
def mesh(blend=1,eps=0,color=TEAL,alpha=.55):
    g=VGroup()
    for z in np.linspace(-.8,.8,9):g.add(ParametricFunction(lambda t,z=z:pos(z,t,blend,eps),t_range=[0,TAU],color=color,stroke_width=.75,stroke_opacity=alpha))
    for t in np.linspace(0,TAU,17)[:-1]:g.add(ParametricFunction(lambda z,t=t:pos(z,t,blend,eps),t_range=[-.8,.8],color=color,stroke_width=.75,stroke_opacity=alpha))
    return g
def molecule(p,color=BLUE,r=.13):
    return Sphere(center=p,radius=r,resolution=(6,10),checkerboard_colors=[color,color],fill_color=color,fill_opacity=1,stroke_width=0)
def spatial_arrow(start,end,color=BLUE,height=.12,base_radius=.045,**kwargs):
    """Spatial line and a deliberately low-poly cone; Arrow3D's tip ignores its resolution."""
    a=np.array(start,dtype=float);b=np.array(end,dtype=float);v=b-a
    line=Line(a,b,color=color,stroke_width=3)
    tip=Cone(direction=v,height=height,base_radius=base_radius,resolution=(3,8),fill_color=color,fill_opacity=1,stroke_width=0).shift(b)
    return VGroup(line,tip)

class SoapBase(ThreeDScene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.target_duration=self.m['duration_seconds'];self.title=self.m['title']
        self.set_camera_orientation(phi=66*DEGREES,theta=-64*DEGREES,zoom=1)
        self.hud=[]
        self.fixed(txt('자연의 최적화  01   /   SOAP FILM',18,MUTED,8 if SHORT else 14).move_to([0,7.25 if SHORT else 3.97,0]))
        self.fixed(txt(self.title,32,WHITE,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.28,0]))
        self.fixed(Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7,2.82,0],[7,2.82,0],color=MUTED,stroke_opacity=.25))
        self.shot();self.finish()
    def fixed(self,*objs):
        self.add_fixed_in_frame_mobjects(*objs);self.hud.extend(objs)
    def info(self,s,note='',color=TEAL):
        g=VGroup(txt(s,34,color,8 if SHORT else 14).move_to([0,-3.25 if SHORT else -1.95,0]))
        if note:g.add(txt(note,19,MUTED,8 if SHORT else 14).move_to([0,-4.15 if SHORT else -2.55,0]))
        self.fixed(g);return g
    def note(self,s):self.fixed(txt(s,17,MUTED,8 if SHORT else 14).move_to([0,-4.9 if SHORT else -2.95,0]))
    def go(self,*a,t=1):self.play(*a,run_time=t)
    def finish(self):
        # No tracker changes after the last animation: freeze redraws during the narration hold.
        for m in self.mobjects:m.clear_updaters(recursive=True)
        left=self.target_duration-self.time
        if left<-.025:raise RuntimeError(f'{self.INDEX}: overflow {self.time}/{self.target_duration}')
        if left>.001:self.wait(left)
    def film(self,blend=1,eps=0,scale=None,opacity=.5):
        g=VGroup(surface(blend,eps,opacity),ring(-.8),ring(.8));g.scale(MACRO_SCALE if scale is None else scale).shift(MACRO_OFFSET);self.add(g);return g
    def molecule_grid(self,surface_only=False):
        g=VGroup();coords=[]
        for z in [-.6,0,.6]:
            for x in [-1.2,-.6,0,.6,1.2]:
                for y in [-.6,0,.6]:
                    if surface_only and z<.6:continue
                    q=np.array([x,y,z]);coords.append(q);g.add(molecule(q))
        self.add(g);return g,coords
    def graph(self,kind='lj'):
        # Fixed-in-frame explanatory overlay, separate from the spatial model.
        center=np.array([0.,-2.1 if SHORT else -1.25,0.]) if kind=='lj' or SHORT else np.array([3.5,.35,0.])
        ax=Axes(x_range=[.85,2.5,.5] if kind=='lj' else [-.23,.23,.1],y_range=[-1.2,2.5,1] if kind=='lj' else [13.1,14.2,.5],x_length=5.4,y_length=2.0,axis_config={'color':MUTED,'stroke_width':1.5,'include_tip':False}).move_to(center)
        self.fixed(ax)
        if kind=='lj':
            f=lambda x:4*(x**-12-x**-6);curve=ax.plot(f,x_range=[.93,2.5],color=GOLD);self.fixed(curve)
            self.fixed(txt('거리 r',18,MUTED).next_to(ax,RIGHT,buff=.15),txt('위치에너지 U(r)',18,MUTED).next_to(ax,UP,buff=.12))
            return ax,f
        pts=DATA['variation'];base=DATA['areas']['1'];ys=[p['area'] for p in pts]
        # Actual computed area, mapped relative to A(0); use a compact readable axis.
        self.remove(ax);self.camera.remove_fixed_in_frame_mobjects(ax)
        ax=Axes(x_range=[-.23,.23,.1],y_range=[0,max(ys)-base+.015,.05],x_length=5.4,y_length=1.75,axis_config={'color':MUTED,'stroke_width':1.5,'include_tip':False}).move_to(center)
        self.fixed(ax)
        line=VMobject(color=TEAL,stroke_width=3).set_points_as_corners([ax.c2p(p['eps'],p['area']-base) for p in pts]);self.fixed(line)
        self.fixed(txt('면적 차이 A(ε) − A(0)',17,MUTED).next_to(ax,UP,buff=.1),txt('ε',20,GOLD).next_to(ax,RIGHT,buff=.1))
        tangent=Line(ax.c2p(-.13,0),ax.c2p(.13,0),color=GOLD,stroke_width=4);self.fixed(tangent,Dot(ax.c2p(0,0),color=GOLD,radius=.06))
        return ax,None
    def patch(self,eps=0,scale=3.0):
        zr=(-.38,.38);tr=(-PI/2-.42,-PI/2+.42)
        g=VGroup(surface(1,eps,.75,GOLD,zr,tr,res=(10,12)))
        for z in zr:g.add(ParametricFunction(lambda t,z=z:pos(z,t,1,eps),t_range=list(tr),color=GOLD,stroke_width=3))
        for t in tr:g.add(ParametricFunction(lambda z,t=t:pos(z,t,1,eps),t_range=list(zr),color=GOLD,stroke_width=3))
        # Tangential outward co-normals, not arrows towards the surface centre.
        for z,sign in [(zr[0],-1),(zr[1],1)]:
            for t in np.linspace(tr[0]+.07,tr[1]-.07,4):
                rp=np.sinh(z)-eps*PI/H*np.sin(2*PI*z/H)
                tangent=np.array([rp*np.cos(t),rp*np.sin(t),1.]);tangent/=np.linalg.norm(tangent)
                p=pos(z,t,1,eps);g.add(spatial_arrow(p,p+sign*.22*tangent,color=BLUE,height=.09,base_radius=.035))
        for t,sign in [(tr[0],-1),(tr[1],1)]:
            for z in np.linspace(-.3,.3,4):
                p=pos(z,t,1,eps);tangent=sign*np.array([-np.sin(t),np.cos(t),0.]);g.add(spatial_arrow(p,p+.22*tangent,color=BLUE,height=.09,base_radius=.035))
        g.move_to(ORIGIN);g.scale(scale);return g
    def shot(self):
        i=self.INDEX
        if i==0:
            hoop=ring(0).scale(1.8);disk=Surface(lambda r,t:np.array([r*np.cos(t),r*np.sin(t),0]),u_range=[0,R],v_range=[0,TAU],resolution=(8,32),checkerboard_colors=[TEAL,TEAL],fill_opacity=.5,stroke_width=0).scale(1.8)
            bath=Surface(lambda x,y:np.array([x,y,-.9]),u_range=[-2.8,2.8],v_range=[-2.0,2.0],resolution=(2,2),checkerboard_colors=[BLUE,BLUE],fill_opacity=.18,stroke_width=0)
            self.add(bath,hoop.shift(IN*.9));self.go(hoop.animate.shift(OUT*.9),FadeIn(disk),t=1.6);self.go(FadeOut(bath),t=.6);self.info('경계가 있으면, 막이 생긴다','철사 고리 + 두 계면을 가진 얇은 액체막')
        elif i==1:
            tracker=ValueTracker(.24)
            def draw():
                h=tracker.get_value();a=1.3
                for _ in range(10):a-= (a*np.cosh(h/(2*a))-R)/(np.cosh(h/(2*a))-h/(2*a)*np.sinh(h/(2*a)))
                f=Surface(lambda z,t:np.array([a*np.cosh(z/a)*np.cos(t),a*np.cosh(z/a)*np.sin(t),z]),u_range=[-h/2,h/2],v_range=[0,TAU],resolution=(12,28),checkerboard_colors=[TEAL,TEAL],fill_opacity=.5,stroke_width=.25)
                return VGroup(f,ring(-h/2),ring(h/2)).scale(1.7 if SHORT else 1.4).shift(MACRO_OFFSET)
            live=always_redraw(draw);self.add(live);self.go(tracker.animate.set_value(1.6),t=4);self.info('고리 간격을 천천히 늘리면','고리 반지름은 일정 · 안정한 카테노이드 가지')
        elif i==2:
            tracker=ValueTracker(0)
            live=always_redraw(lambda:VGroup(surface(tracker.get_value()),ring(-.8),ring(.8)).scale(MACRO_SCALE).shift(MACRO_OFFSET));self.add(live)
            guide=VGroup()
            for t in np.linspace(0,TAU,9)[:-1]:guide.add(DashedLine(pos(-.8,t,0),pos(.8,t,0),dash_length=.1,color=MUTED,stroke_opacity=.5))
            guide.scale(MACRO_SCALE).shift(MACRO_OFFSET);self.add(guide);self.info('원기둥과는 다른 모양','점선: 비교용 원기둥 / 청록: 고정 경계의 곡면');self.note('기하학적 비교 · 실제 유체 운동의 시간 재현 아님')
            self.go(tracker.animate.set_value(1),t=3.7);self.move_camera(theta=-40*DEGREES,run_time=1.2)
        elif i==3:
            f=self.film();section=ParametricFunction(lambda z:pos(z,-PI/2),t_range=[-.8,.8],color=GOLD,stroke_width=6).scale(MACRO_SCALE).shift(MACRO_OFFSET)
            self.go(Create(section),t=.8);self.info('CATENOID','r(z) = a cosh(z/a) · 현수선을 회전한 곡면');self.move_camera(theta=-42*DEGREES,run_time=2.0)
        elif i==4:
            f=self.film(opacity=.32);p=surface(color=GOLD,zrange=(-.3,.3),trange=(-1.95,-1.2),res=(6,8)).scale(MACRO_SCALE).shift(MACRO_OFFSET);self.add(p)
            self.go(FadeOut(f),FadeOut(p),t=1.5);g,coords=self.molecule_grid();g.scale(1.55 if SHORT else 1.3).shift(MACRO_OFFSET)
            self.info('연속적인 막 → 분자들의 상호작용','분자 배열과 운동은 이해를 위한 개념 모형')
            self.go(g.animate.shift(RIGHT*.09+OUT*.06),t=1.5);self.go(g.animate.shift(LEFT*.09+IN*.06),t=1.5)
        elif i==5:
            self.set_camera_orientation(phi=0,theta=-90*DEGREES)
            left=molecule([-1.4,1.7,0],r=.29);right=molecule([1.4,1.7,0],r=.29);self.add(left,right)
            self.fixed(txt('분자 사이의 상호작용',24,BLUE).move_to([0,3.9 if SHORT else 2.45,0]))
            ax,fun=self.graph('lj');tracker=ValueTracker(1.65)
            dot=always_redraw(lambda:Dot(ax.c2p(tracker.get_value(),fun(tracker.get_value())),color=WHITE,radius=.07));self.fixed(dot)
            attraction=VGroup(Arrow([-1.05,1.7,0],[-.3,1.7,0],color=GOLD),Arrow([1.05,1.7,0],[.3,1.7,0],color=GOLD));self.add(attraction)
            self.go(left.animate.move_to([-.4,1.7,0]),right.animate.move_to([.4,1.7,0]),tracker.animate.set_value(.96),t=2)
            self.remove(attraction);repel=VGroup(Arrow([-.4,1.7,0],[-1.3,1.7,0],color=RED),Arrow([.4,1.7,0],[1.3,1.7,0],color=RED));self.add(repel)
            self.go(left.animate.move_to([-.75,1.7,0]),right.animate.move_to([.75,1.7,0]),tracker.animate.set_value(2**(1/6)),t=2.4)
            self.remove(repel);self.fixed(txt('인력과 반발력 사이의 낮은 에너지',23,GREEN).move_to([0,3.1 if SHORT else .95,0]));self.note('Lennard–Jones 형태의 개념 모형 · 실제 비눗물 전체의 퍼텐셜 아님')
        elif i in [6,7]:
            self.set_camera_orientation(phi=78*DEGREES,theta=-70*DEGREES)
            g,coords=self.molecule_grid();g.scale(1.45)
            plane=Surface(lambda x,y:np.array([x,y,.92]),u_range=[-2.05,2.05],v_range=[-1.2,1.2],resolution=(2,2),checkerboard_colors=[TEAL,TEAL],fill_opacity=.18,stroke_width=0);self.add(plane)
            focus=molecule([.15,-.1,-.2],GOLD,.22);self.add(focus)
            links=VGroup(*[Line(focus.get_center(),q*1.45,color=GOLD,stroke_opacity=.45,stroke_width=2) for q in coords if np.linalg.norm(q)<.9]);self.add(links)
            if i==6:
                self.go(focus.animate.move_to([.15,-.1,1.06]),FadeOut(links),t=3.5)
                remaining=VGroup(*[Line(focus.get_center(),q*1.45,color=GOLD,stroke_opacity=.6,stroke_width=2) for q in coords if q[2]>.3 and np.linalg.norm(q[:2])<.9])
                self.go(FadeIn(remaining),t=.7)
            else:
                focus.move_to([.15,-.1,1.06]);self.remove(links)
                links=VGroup(*[Line(focus.get_center(),q*1.45,color=GOLD,stroke_opacity=.5) for q in coords if q[2]>.3 and np.linalg.norm(q[:2])<.9]);self.add(links)
            self.info('내부 → 표면' if i==6 else '바깥쪽에는 액체 이웃이 적다','상호작용 일부를 잃는다는 분자 수준의 직관')
            self.note('자유에너지는 열운동과 배열도 포함한다')
        elif i in [8,9,10,11]:
            self.set_camera_orientation(phi=56*DEGREES,theta=-66*DEGREES)
            tracker=ValueTracker(1)
            surf=always_redraw(lambda:Surface(lambda x,y:np.array([x*tracker.get_value(),y,0]),u_range=[-1.3,1.3],v_range=[-1,1],resolution=(3,4),checkerboard_colors=[TEAL,TEAL],fill_opacity=.55,stroke_color=TEAL,stroke_width=.6).scale(1.35 if SHORT else 1.05).shift(np.array([0.,0.,0. if SHORT else 1.1])))
            self.add(surf)
            def meters():
                a=tracker.get_value();g=VGroup()
                for j,(label,col) in enumerate([('면적 A',TEAL),('자유에너지 E',GOLD)]):
                    x=-2.5+j*3.25;y=-2.1 if SHORT else -.95
                    g.add(txt(label,21,col,3).move_to([x+.6,y-.45,0]),Rectangle(width=1.2,height=.22,stroke_width=0,fill_color=col,fill_opacity=.22).move_to([x+.6,y,0]),Rectangle(width=1.2*a/2,height=.22,stroke_width=0,fill_color=col,fill_opacity=1).move_to([x+.3*a,y,0]),txt(f'{a:.2f} ×',19,col,2).move_to([x+.6,y+.4,0]))
                return g
            bars=always_redraw(meters);self.fixed(bars)
            self.info('E_film = 2γA','앞뒤 두 계면 · γ는 한 계면의 표면장력 · 온도·조성 일정')
            if i in [8,9]:self.go(tracker.animate.set_value(2),t=2.5)
            elif i==10:self.go(tracker.animate.set_value(1.8),t=1.5);self.go(tracker.animate.set_value(1),t=1.5)
            else:
                tracker.set_value(1.9);self.go(tracker.animate.set_value(1),t=2.7)
                self.fixed(txt('표면적 ↓  →  자유에너지 ↓',25,GREEN).move_to([0,2.5 if SHORT else 1.8,0]))
        elif i==12:
            self.film();self.info('표면적을 줄인다','하지만 경계까지 사라질 수 있을까?')
            arrows=VGroup(*[spatial_arrow(np.array([x,y,0])*2.1,np.array([x,y,0])*1.5,color=GOLD,height=.15,base_radius=.07) for x,y in [(1,0),(-1,0),(0,1),(0,-1)]])
            self.go(FadeIn(arrows),t=.8);self.go(FadeOut(arrows),t=1.5)
            borders=VGroup(ring(-.8),ring(.8)).scale(MACRO_SCALE).shift(MACRO_OFFSET).set_color(GOLD);self.go(Create(borders),t=1.2)
        elif i in [13,14]:
            tracker=ValueTracker(0 if i==13 else .5)
            live=always_redraw(lambda:VGroup(surface(tracker.get_value()),ring(-.8),ring(.8)).scale(MACRO_SCALE).shift(MACRO_OFFSET));self.add(live)
            def area_label():
                b=tracker.get_value();z=np.linspace(-.8,.8,1201);r=R+b*(np.cosh(z)-R);dr=b*np.sinh(z);A=2*PI*np.trapezoid(r*np.sqrt(1+dr*dr),z)
                return txt(f'고정 경계     A = {A:.3f}',30,GOLD,8).move_to([0,-3.3 if SHORT else -1.95,0])
            label=always_redraw(area_label);self.fixed(label)
            self.fixed(txt('R = 1.3374  ·  h = 1.6000',21,MUTED).move_to([0,-4.15 if SHORT else -2.55,0]));self.note('면적적분값 · 임의 단위² / 형태 보간은 기하학적 비교')
            self.go(tracker.animate.set_value(.5 if i==13 else 1),t=2.3)
            if i==13:self.go(tracker.animate.set_value(1),t=2.3)
        elif i==15:
            self.film();grid=mesh().scale(MACRO_SCALE).shift(MACRO_OFFSET);self.go(Create(grid),t=1);self.info('MINIMAL SURFACE    H = 0','압력차·중력을 무시한 막의 매끄러운 내부');self.note('안정한 국소 최소 · 모든 가능한 형태의 절대 최소를 뜻하지 않음');self.move_camera(theta=-42*DEGREES,run_time=3)
        elif i==16:
            tracker=ValueTracker(0);live=always_redraw(lambda:VGroup(surface(1,float(tracker.get_value())),ring(-.8),ring(.8)).scale(MACRO_SCALE).shift(MACRO_OFFSET));self.add(live)
            self.info('가정: 모든 후보를 계산해서 고른다면?','사고실험 · 실제 자연의 동작을 재현한 것이 아님',GOLD)
            for value in [.17,-.14,.08,-.06,.19,-.1,.03]:self.go(tracker.animate.set_value(value),t=.42)
        elif i==17:
            self.film();self.info('전체 면적을 계산하는 탐색은 없다','각 부분에 작용하는 힘으로 시선을 옮긴다')
            gold=surface(color=GOLD,zrange=(-.38,.38),trange=(-1.99,-1.15),res=(8,8)).scale(MACRO_SCALE).shift(MACRO_OFFSET);self.go(FadeIn(gold),t=1.0);self.move_camera(zoom=1.25,run_time=1.8)
        elif i==18:
            self.film(opacity=.13);patch=surface(color=GOLD,zrange=(-.38,.38),trange=(-1.99,-1.15),res=(8,8)).scale(MACRO_SCALE).shift(MACRO_OFFSET);self.add(patch);self.info('한 조각만 확대','주변 막과 맞닿은 경계를 따라 힘이 작용한다')
        elif i in [19,20]:
            self.set_camera_orientation(phi=66*DEGREES,theta=-80*DEGREES)
            patch=self.patch(.12 if i==19 else .05,2.6);self.add(patch)
            self.info('장력은 표면의 접평면 안에서 작용','각 화살표는 남는다 · 합력이 균형을 이룬다')
            self.note('압력차 무시 · 축소한 패치의 국소 모형')
            # Boundary co-normal integral points in +y for this outward bump.
            # verify.py independently evaluates all four edges (equilibrium residual < 1e-6).
            normal=spatial_arrow([0,0,0],[0,1,0],color=GOLD,height=.13,base_radius=.06);self.add(normal)
            self.go(Transform(patch,self.patch(0,2.6)),normal.animate.scale(.015,about_point=ORIGIN),t=3.5)
            self.go(FadeOut(normal),t=.6)
            self.fixed(txt('합력의 법선 성분 → 0' if i==19 else '평균곡률  H = 0',28,GREEN).move_to([0,3.5 if SHORT else 2.15,0]))
            if i==20:self.go(patch.animate.scale(.82),t=1.2)
        elif i==21:
            # Geometry above the graph, no camera-time metaphor: epsilon is a candidate parameter.
            self.set_camera_orientation(phi=66*DEGREES,theta=-64*DEGREES)
            tracker=ValueTracker(0)
            offset=np.array([0,0,1.9]) if SHORT else -3.4*np.array([np.cos(26*DEGREES),np.sin(26*DEGREES),0.])
            live=always_redraw(lambda:VGroup(surface(1,tracker.get_value(),.4),ring(-.8),ring(.8)).scale(1.05).shift(offset));self.add(live)
            self.graph('variation');self.fixed(txt('ε: 후보 형태의 변화 · 실제 시간 아님',20,GOLD,8 if SHORT else 14).move_to([0,-4.1 if SHORT else -2.6,0]))
            self.fixed(txt('dA/dε | ε=0 = 0    ⇔    δA = 0',30,GREEN,8 if SHORT else 14).move_to([0,-4.9 if SHORT else -3.05,0]))
            self.go(tracker.animate.set_value(.2),t=1.4);self.go(tracker.animate.set_value(-.2),t=2.0);self.go(tracker.animate.set_value(0),t=1.4)
        elif i==22:
            self.film();grid=mesh(color=GREEN,alpha=.7).scale(MACRO_SCALE).shift(MACRO_OFFSET);self.add(grid)
            patches=VGroup(*[surface(color=GREEN,zrange=(z,z+.3),trange=(t,t+.5),res=(3,4)).scale(MACRO_SCALE).shift(MACRO_OFFSET) for z,t in [(-.6,-1.8),(-.2,-1.5),(.2,-1.2)]])
            self.go(LaggedStart(*[FadeIn(p) for p in patches],lag_ratio=.35),t=2)
            self.info('국소적인 힘의 평형  →  δA = 0','허용된 작은 변형에 대한 면적의 일차 변화가 0');self.note('전역 최소를 보장하는 조건은 아님');self.go(FadeOut(patches),FadeOut(grid),t=1.8)
        else:
            self.film();self.info('국소적인 물리법칙에서','전체적인 최적화의 구조를 발견한다',GREEN)
            self.fixed(txt('경계 고정   ·   힘의 평형   ·   δA = 0',26,TEAL,8 if SHORT else 14).move_to([0,3.9 if SHORT else 2.5,0]))
            self.move_camera(theta=-48*DEGREES,run_time=3.2)





