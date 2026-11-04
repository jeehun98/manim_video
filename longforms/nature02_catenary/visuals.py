"""22 independent shots: constrained chains, tangent forces, and a swept catenoid."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from physics import B,R,L,height,slope,coefficient,integrals
P=Path(__file__).resolve().parent
SHORT=os.environ.get('CHAIN_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#091421'
SILVER='#D8E1E8';TEAL='#35C9D0';BLUE='#579BE8';GOLD='#E3A447';GREEN='#3BC58B';RED='#ED7681';MUTED='#8EA9BB';WHITE='#F2F6FA'
MID=(1+R)/2;SCALE=3.6 if SHORT else 3.2;CZ=1.05 if SHORT else .65
DATA=json.loads((P/'geometry.json').read_text(encoding='utf-8'));SIM=np.load(P/'dynamics.npz')
def text(s,size=28,color=WHITE,width=8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def world(q,scale=SCALE,center=(0,0,CZ)):
    q=np.asarray(q,dtype=float).copy();q[...,2]-=MID;return q*scale+np.array(center)
def ball(q,color=GOLD,r=.105):return Sphere(center=q,radius=r,resolution=(4,8),checkerboard_colors=[color,color],fill_opacity=1,stroke_width=0)
def arrow(a,b,color=BLUE):
    a=np.array(a,dtype=float);b=np.array(b,dtype=float)
    return VGroup(Line(a,b,color=color,stroke_width=4),Cone(direction=b-a,height=.13,base_radius=.05,resolution=(3,8),checkerboard_colors=[color,color],fill_opacity=1,stroke_width=0).shift(b))
def centerline(alpha=0,color=TEAL,scale=SCALE,center=(0,0,CZ),width=4):
    beta=coefficient(float(alpha))
    return ParametricFunction(lambda x:world([x,0,height(x,alpha,beta)],scale,center),t_range=[-B,B],color=color,stroke_width=width)
def chain(alpha=0,scale=SCALE,center=(0,0,CZ),color=SILVER):
    beta=coefficient(float(alpha))
    def point(x,t):
        m=slope(x,alpha,beta);normal=np.array([-m,0,1])/np.sqrt(1+m*m)
        return world([x,0,height(x,alpha,beta)],scale,center)+.055*(np.cos(t)*normal+np.sin(t)*UP)
    return Surface(point,u_range=[-B,B],v_range=[0,TAU],resolution=(40,6),checkerboard_colors=[color,color],fill_opacity=1,stroke_width=0)
def pins(scale=SCALE,center=(0,0,CZ)):
    g=VGroup()
    for x in [-B,B]:
        p=world([x,0,R],scale,center);g.add(ball(p),Line(p+OUT*.05,p+OUT*.48,color=GOLD,stroke_width=3),Line(p+OUT*.48+LEFT*.22,p+OUT*.48+RIGHT*.22,color=MUTED,stroke_width=3))
    return g
def sim_positions(t):
    k=np.clip(float(t)*60,0,len(SIM['positions'])-1);j=int(k);f=k-j
    return SIM['positions'][j]*(1-f)+SIM['positions'][min(j+1,len(SIM['positions'])-1)]*f
def discrete_chain(t,color=SILVER,scale=SCALE,center=(0,0,CZ),colored=False):
    pts=world(sim_positions(t),scale,center);g=VGroup()
    if colored:
        for a,b in zip(pts,pts[1:]):
            ratio=float(np.clip(((a[2]+b[2])/2-(CZ-.7))/1.4,0,1));g.add(Line(a,b,color=interpolate_color(ManimColor(TEAL),ManimColor(GOLD),ratio),stroke_width=8))
    else:
        g.add(VMobject(color=color,stroke_width=9).set_points_as_corners(pts),VMobject(color=WHITE,stroke_width=1.6,stroke_opacity=.5).set_points_as_corners(pts))
    return g
def local_links(shift=0):
    g=VGroup()
    for i in range(5):
        x=(i-2)*.75;z=.16*(i-2)**2 + (shift if i==2 else 0)
        # Adjacent elliptical metal links alternate their planes.
        def f(u,v,i=i,x=x,z=z):
            p=np.array([.48*np.cos(u),.23*np.sin(u),0.]);n=np.array([np.cos(u),np.sin(u),0.])
            q=p+.045*(np.cos(v)*n+np.sin(v)*OUT)
            if i%2:q=np.array([q[0],q[2],q[1]])
            return q+np.array([x,0,z])
        g.add(Surface(f,u_range=[0,TAU],v_range=[0,TAU],resolution=(20,6),checkerboard_colors=[GOLD if i==2 else SILVER]*2,fill_opacity=1,stroke_width=0))
    return g
def force_patch(x=0,size=.13,scale=SCALE,center=(0,0,CZ)):
    # Forces on [x-d,x+d]: H=λga=1, V=λga sinh(x/a), weight=λg ds.
    l=x-size;r=x+size;p=world([x,0,np.cosh(x)],scale,center)
    vL=np.array([-1,0,-np.sinh(l)]);vR=np.array([1,0,np.sinh(r)]);vG=np.array([0,0,-(np.sinh(r)-np.sinh(l))])
    factor=.8
    return VGroup(arrow(p,p+vL*factor,BLUE),arrow(p,p+vR*factor,BLUE),arrow(p,p+vG*factor,GOLD))
def cat_surface(theta=TAU,scale=1.5,offset=(0,0,0),vertical=False):
    def f(x,t):
        q=np.array([x,np.cosh(x)*np.sin(t),np.cosh(x)*np.cos(t)])
        if vertical:q=np.array([q[2],q[1],-q[0]])
        return q*scale+np.array(offset)
    return Surface(f,u_range=[-B,B],v_range=[0,max(theta,.001)],resolution=(14,28),checkerboard_colors=[TEAL,TEAL],fill_opacity=.48,stroke_color=TEAL,stroke_opacity=.25,stroke_width=.35)
def cat_rings(scale=1.5,offset=(0,0,0),vertical=False):
    g=VGroup()
    for x in [-B,B]:
        def f(t,x=x):
            q=np.array([x,R*np.sin(t),R*np.cos(t)])
            if vertical:q=np.array([q[2],q[1],-q[0]])
            return q*scale+np.array(offset)
        g.add(ParametricFunction(f,t_range=[0,TAU],color=SILVER,stroke_width=5))
    return g

class ChainBase(ThreeDScene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.target_seconds=self.m['duration_seconds']
        self.set_camera_orientation(phi=78*DEGREES,theta=-78*DEGREES)
        self.fixed(text('자연의 최적화  02   /   CATENARY',18,MUTED,8 if SHORT else 14).move_to([0,7.25 if SHORT else 3.97,0]),text(self.m['title'],31,WHITE,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.28,0]))
        self.fixed(Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.25) if SHORT else Line([-7,2.82,0],[7,2.82,0],color=MUTED,stroke_opacity=.25))
        self.shot()
        for m in self.mobjects:m.clear_updaters(recursive=True)
        left=self.target_seconds-self.time
        if left<-.025:raise RuntimeError(f'scene {self.INDEX+1}: {self.time} > {self.target_seconds}')
        if left>.001:self.wait(left)
    def fixed(self,*m):self.add_fixed_in_frame_mobjects(*m)
    def info(self,s,note='',color=TEAL):
        g=VGroup(text(s,31,color,8 if SHORT else 14).move_to([0,-3.15 if SHORT else -1.95,0]))
        if note:g.add(text(note,19,MUTED,8 if SHORT else 14).move_to([0,-4.05 if SHORT else -2.5,0]))
        self.fixed(g);return g
    def note(self,s):self.fixed(text(s,17,MUTED,8 if SHORT else 14).move_to([0,-4.85 if SHORT else -2.95,0]))
    def go(self,*m,t=1):self.play(*m,run_time=t)
    def whole(self,alpha=0,color=SILVER):
        g=VGroup(chain(alpha,color=color),pins());self.add(g);return g
    def sim(self,t0,t1,seconds,colored=False):
        tracker=ValueTracker(t0);g=always_redraw(lambda:discrete_chain(tracker.get_value(),colored=colored));self.add(g,pins());self.go(tracker.animate.set_value(t1),t=seconds);g.clear_updaters();return g
    def energy_bars(self,candidates=(0,.07,-.1),minimum=True):
        # Values are continuous integrals with the same reference plane and mass.
        rows=[integrals(float(a)) for a in candidates];umin=integrals(0)['energy'];g=VGroup()
        for j,row in enumerate(rows):
            y=(-.45-j*.7) if SHORT else (-.25-j*.45)
            col=GREEN if abs(row['alpha'])<1e-10 else GOLD
            w=15*(row['energy']-1.95)
            g.add(text('현수선' if row['alpha']==0 else f'후보 {j}',20,col,2.1).move_to([-2.55,y,0]),Rectangle(width=w,height=.17,fill_color=col,fill_opacity=.8,stroke_width=0).move_to([-1.2+w/2,y,0]),text(f'U = {row["energy"]:.5f}',19,col,2.7).move_to([2.4,y,0]))
        g.add(text('막대: 공통 기준 U = 1.95부터 표시',15,MUTED,7).move_to([0,-2.4 if SHORT else -1.55,0]))
        self.fixed(g);return g
    def shot(self):
        i=self.INDEX
        if i==0:
            self.add(pins());self.sim(0,.7,2.4);self.info('중력 위치에너지 최소화','고정된 양 끝 · 늘어나지 않는 균일한 사슬');self.note('거리 제약과 감쇠를 둔 질점 사슬 모형')
        elif i==1:
            self.whole();s=np.linspace(-np.sinh(B),np.sinh(B),17);dots=VGroup(*[ball(world([np.arcsinh(v),0,np.sqrt(1+v*v)]),TEAL,.055) for v in s]);self.go(FadeIn(dots),t=.8)
            self.info('같은 호길이마다 같은 질량','점들은 수평 간격이 아니라 사슬을 따른 간격이 같다');self.move_camera(theta=-90*DEGREES,run_time=1.3)
        elif i==2:
            self.add(pins(),centerline(0,GREEN))
            for a,col in [(.07,GOLD),(-.1,BLUE)]:self.add(centerline(a,col,width=3).set_stroke(opacity=.65))
            self.energy_bars();self.info('서로 다른 모양 · 같은 길이','전체 위치에너지는 실제 곡선 적분으로 비교한다');self.note(f'모든 후보: L = {L:.6f} · 기준 높이와 총질량 동일')
        elif i==3:
            self.whole();trace=centerline(0,GOLD,width=7);self.go(Create(trace),t=2.2)
            self.fixed(text(f'L = 2a sinh(b/a) = {L:.6f}',25,GOLD).move_to([0,-.65 if SHORT else -.8,0]));self.info('목표: 전체 위치에너지 최소','조건: 양 끝 고정 · 전체 길이 일정')
        elif i==4:
            self.whole();dot=ball(world([0,0,1]),GOLD,.13);self.add(dot);self.info('사슬의 작은 부분으로','전체 후보를 계산하는 탐색 과정이 아니다');self.go(dot.animate.scale(1.6),t=1.2)
        elif i in [5,6,7]:
            self.set_camera_orientation(phi=75*DEGREES,theta=-85*DEGREES)
            links=local_links(.15 if i==6 else 0).shift(OUT*(1 if SHORT else .5));self.add(links)
            p=np.array([0,-.16,1 if SHORT else .5]);up=.5 if i==6 else .65;down=1.7 if i==6 else 1.3
            forces=VGroup(arrow(p,p+[-1.35,0,up]),arrow(p,p+[1.35,0,up]),arrow(p,p+[0,0,-down],GOLD));self.add(forces)
            self.fixed(text('T_L',24,BLUE).move_to([-1.9,2.3 if SHORT else 1.6,0]),text('T_R',24,BLUE).move_to([1.9,2.3 if SHORT else 1.6,0]),text('重力 mg'.replace('重力','중력'),23,GOLD).move_to([0,-1.0 if SHORT else -.9,0]))
            if i==5:self.info('중력 + 양옆의 접선 방향 장력','화살표는 유연한 사슬의 이상적인 힘 모형')
            elif i==6:
                net=arrow(p,p+[0,0,-.7],RED);self.add(net);self.go(links.animate.shift(IN*.22),t=1.5);self.go(FadeOut(net),t=.5);self.info('ΣF = ma','힘이 맞지 않으면, 연결된 부분이 함께 반응한다')
            else:
                self.go(LaggedStart(*[Indicate(link,color=TEAL,scale_factor=1.03) for link in links],lag_ratio=.15),t=2)
                self.info('연결되어 있으므로 함께 변한다','금속 고리 확대 모형 · 거시적 움직임은 거리 제약 질점 계산')
            self.note('실제 강체 고리의 접촉·회전을 계산한 모형은 아님')
        elif i==8:
            self.sim(.15,1.45,4.5);self.info(f'고정된 총길이  L = {L:.6f}','한 부분이 내려가면 다른 부분의 위치도 달라진다');self.note('고정점 불변 · 각 질점 사이 거리 제약 적용')
        elif i==9:
            tracker=ValueTracker(0);g=always_redraw(lambda:VGroup(chain(tracker.get_value()),pins()));self.add(g)
            left=ball(world([-.4,0,height(-.4)]),BLUE,.1);right=ball(world([.4,0,height(.4)]),GOLD,.1);self.add(left,right)
            target=.1
            self.go(tracker.animate.set_value(target),left.animate.move_to(world([-.4,0,height(-.4,target)])),right.animate.move_to(world([.4,0,height(.4,target)])),t=2.5)
            self.fixed(text('일부 ↓    다른 부분 ↑',26,GOLD).move_to([0,-.7 if SHORT else -.9,0]));self.info('U = ∫ gy dm = Σ mᵢgyᵢ','한 부분의 감소가 전체의 감소를 뜻하지는 않는다');self.note('후보 형태 비교 · 실제 시간에 따른 운동과 구별')
        elif i==10:
            ax=Axes(x_range=[0,14,7],y_range=[0,1,.5],x_length=5.7,y_length=1.5,axis_config={'include_tip':False,'color':MUTED,'stroke_width':1}).move_to([0,-1.35 if SHORT else -.85,0]);self.fixed(ax)
            u=SIM['U'];k=SIM['K'];t=SIM['times'];baseline=float(u[-1]);den=float(np.max(u+k)-baseline)
            for arr,col in [(u,TEAL),(k+baseline,BLUE),(u+k,GOLD)]:
                curve=VMobject(color=col,stroke_width=2).set_points_as_corners([ax.c2p(float(t[j]),float((arr[j]-baseline)/den)) for j in range(0,len(t),4)]);self.fixed(curve)
            lost=(u[0]+k[0])-(u+k)
            loss=VMobject(color=MUTED,stroke_width=2).set_points_as_corners([ax.c2p(float(t[j]),float(lost[j]/den)) for j in range(0,len(t),4)])
            self.fixed(DashedVMobject(loss,num_dashes=30),text('시간',17,MUTED).next_to(ax,RIGHT,buff=.13))
            self.info('U는 오르내려도, U + K는 감소','청록 U · 파랑 K · 금색 U+K · 회색 소산분');self.note('공통 기준의 상대량 · 소산분은 감쇠와 수치 소산의 합')
            self.sim(0,7,4.2,colored=True)
        elif i==11:
            self.whole(color=TEAL);forces=VGroup(*[force_patch(x,size=.1) for x in [-.4,0,.4]]);self.go(FadeIn(forces),t=.8);self.info('평형에서는 각 부분의 ΣF = 0','중력은 사라지지 않고, 장력과 균형을 이룬다')
        elif i==12:
            self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES)
            self.whole();tracker=ValueTracker(0)
            def vectors():
                x=tracker.get_value();p=world([x,0,np.cosh(x)]);h=np.array([1.,0,0]);v=np.array([0,0,np.sinh(x)])
                return VGroup(ball(p,TEAL,.09),arrow(p,p+h,BLUE),Line(p+h,p+h+v,color=GOLD,stroke_width=4),arrow(p,p+h+v,TEAL))
            g=always_redraw(vectors);self.add(g)
            self.fixed(text('Tₓ = λga = 일정',24,BLUE).move_to([-1.9,-.8 if SHORT else -.9,0]),text('Tᵧ = λga sinh(x/a)',24,GOLD,3.9).move_to([1.9,-.8 if SHORT else -.9,0]))
            self.info('중심에서 멀수록 더 가파른 접선','오른쪽의 수직 성분 증가 · 왼쪽에서는 부호 반대')
            self.go(tracker.animate.set_value(.72),t=5.4)
        elif i==13:
            self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES);self.add(pins());curve=centerline(0,TEAL,width=5);self.go(Create(curve),t=2.7)
            self.fixed(text('dy/dx = Tᵧ/Tₓ = sinh(x/a)',27,BLUE).move_to([0,-.8 if SHORT else -.85,0]));self.info('y = a cosh(x/a) + C','장력의 방향과 곡선의 접선이 일치한다')
        elif i==14:
            self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES);self.whole(color=TEAL)
            parabola=DashedVMobject(ParametricFunction(lambda x:world([x,0,1+x*x/2]),t_range=[-B,B],color=BLUE,stroke_width=4),num_dashes=35);self.go(Create(parabola),t=.7)
            diff=np.cosh(B)-1-B*B/2
            self.info('CATENARY · 현수선','청록 cosh(x) / 파랑 1 + x²/2 : 같은 꼭짓점·중심 곡률');self.note(f'x=0.8에서 높이 차이 Δy = {diff:.6f} · 길이 제약 후보 비교와는 별개')
            # A magnified difference graph makes the true small difference visible without distorting the chain.
            ax=Axes(x_range=[0,.8,.4],y_range=[0,.02,.01],x_length=4,y_length=1.15,axis_config={'include_tip':False,'color':MUTED,'stroke_width':1}).move_to([0,-1.4 if SHORT else -.85,0]);self.fixed(ax,ax.plot(lambda x:np.cosh(x)-1-x*x/2,x_range=[0,.8],color=GOLD));self.fixed(text('差 Δy'.replace('差 ','실제 차이 '),18,GOLD).next_to(ax,RIGHT,buff=.12))
        elif i in [15,16,17]:
            self.set_camera_orientation(phi=82*DEGREES,theta=-90*DEGREES)
            sep=2.0 if SHORT else 3.5;sc=1.9 if SHORT else 2.6;cz=2.0 if SHORT else .85
            left=VGroup(chain(0,sc,(-sep,0,cz),TEAL),pins(sc,(-sep,0,cz)));self.add(left)
            if i==15:
                tracker=ValueTracker(.12)
                right=always_redraw(lambda:VGroup(chain(tracker.get_value(),sc,(sep,0,cz),GOLD),pins(sc,(sep,0,cz))));self.add(right)
                self.go(tracker.animate.set_value(-.1),t=2.4);self.go(tracker.animate.set_value(.07),t=2.0)
                self.energy_bars((0,.07,-.1));self.info('왼쪽: 힘의 평형 / 오른쪽: 후보 비교','후보들도 같은 양 끝과 같은 총길이를 지킨다')
            else:
                right=VGroup(chain(0,sc,(sep,0,cz),GREEN),pins(sc,(sep,0,cz)));self.add(right)
                self.fixed(text('국소적인 힘의 평형',20,TEAL,3.5).move_to([-sep,-.25 if SHORT else -.4,0]),text('전체 위치에너지 최소',20,GREEN,3.5).move_to([sep,-.25 if SHORT else -.4,0]))
                if i==16:self.go(right.animate.shift(LEFT*2*sep),t=1.6);self.info('동일한 현수선','같은 고정점과 길이에서 두 접근이 만난다')
                else:
                    self.go(left.animate.shift(RIGHT*sep),right.animate.shift(LEFT*sep),t=2.2);self.info('같은 평형 형태','국소적 힘의 조건과 전체 에너지의 조건이 연결된다')
        elif i==18:
            self.whole(color=TEAL)
            for x in [-.4,0,.4]:
                f=force_patch(x,.1);self.go(FadeIn(f),t=.5)
            self.fixed(text('각 부분: 중력 + 주변 장력',27,BLUE).move_to([0,-.7 if SHORT else -.85,0]));self.info('부분의 물리적 반응 → 전체의 최소 에너지','전체 에너지를 미리 계산하는 과정이 아니다');self.note('균일한 사슬 · 고정점과 총길이 제약 아래의 평형')
        elif i in [19,20]:
            self.set_camera_orientation(phi=68*DEGREES,theta=-64*DEGREES)
            scale=1.5 if SHORT else 1.23;offset=np.array([0.,0.,.4 if SHORT else .55]);tracker=ValueTracker(0 if i==19 else PI/2)
            def draw():
                th=tracker.get_value();g=VGroup(cat_surface(th,scale,offset))
                g.add(ParametricFunction(lambda x:np.array([x,np.cosh(x)*np.sin(th),np.cosh(x)*np.cos(th)])*scale+offset,t_range=[-B,B],color=GOLD,stroke_width=4))
                return g
            g=always_redraw(draw);self.add(g)
            axis=DashedLine(np.array([-1.6,0,0])*scale+offset,np.array([1.6,0,0])*scale+offset,color=MUTED,dash_length=.1);self.add(axis)
            if i==19:
                self.info('회전 반지름  r(x) = a cosh(x/a)','회전축은 최저점보다 a 아래 · 최소 반지름 a > 0');self.go(tracker.animate.set_value(PI/2),t=4.5)
            else:
                self.info('CATENARY → CATENOID','a = 1 · h = 1.6 · R = cosh(0.8)');self.go(tracker.animate.set_value(TAU),t=2.8);self.go(FadeIn(cat_rings(scale,offset)),t=.5)
        else:
            # Both objects are newly defined: this comparison also works as an independent ending.
            self.set_camera_orientation(phi=76*DEGREES,theta=-82*DEGREES)
            sep=2.05 if SHORT else 3.4;sc=1.8 if SHORT else 2.4;cz=1.6 if SHORT else .8
            cat_scale=.9 if SHORT else .8
            self.add(chain(0,sc,(-sep,0,cz),TEAL),pins(sc,(-sep,0,cz)),cat_surface(TAU,cat_scale,(sep,0,cz),True),cat_rings(cat_scale,(sep,0,cz),True))
            self.fixed(text('사슬',24,TEAL).move_to([-sep,3.7 if SHORT else 2.2,0]),text('비눗막',24,TEAL).move_to([sep,3.7 if SHORT else 2.2,0]),text('중력 위치에너지 최소',20,GOLD,3.8).move_to([-sep,-.35 if SHORT else -.65,0]),text('표면에너지 최소',20,GOLD,3.8).move_to([sep,-.35 if SHORT else -.65,0]))
            self.move_camera(theta=-66*DEGREES,run_time=2);self.wait(2)
            common=text('같은 함수  cosh',33,GREEN).move_to([0,-1.6 if SHORT else -1.25,0]);self.fixed(common);self.go(FadeIn(common),t=.6);self.wait(3.4)
            self.info('국소적 물리법칙 → 전체적인 최적화 구조','줄이는 에너지는 다르지만, 같은 수학적 함수가 나타난다');self.note('회전은 두 형상을 잇는 기하학적 관계 · 두 물리적 기작이 같다는 뜻은 아님')
