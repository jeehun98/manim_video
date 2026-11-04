"""27 independent shots, one projectile and mathematically computed action."""
import os,json
from pathlib import Path
import numpy as np
from manim import *
from physics import M,G,VX,VY,Y0,DURATION,COEFF,S0,SY0,y,vy,q,eta,deta,energy,lagrangian,action,exact_action,accumulated,candidate,retimed_q,newton,variational
P=Path(__file__).resolve().parent;SHORT=os.environ.get('ACTION_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#091421'
GOLD='#E3A447';TEAL='#35C9D0';BLUE='#579BE8';RED='#ED7681';PURPLE='#BB97FF';MUTED='#8EA9BB';WHITE='#F2F6FA'
def txt(s,size=26,col=WHITE,width=None):
    m=Text(s,font='Malgun Gothic',font_size=size,color=col,line_spacing=.8)
    if m.width>(width or (8 if SHORT else 14)):m.scale_to_fit_width(width or (8 if SHORT else 14))
    return m
def ball(p,col=GOLD,r=.085):return Sphere(center=p,radius=r,resolution=(5,10),checkerboard_colors=[col,col],stroke_width=0)
def vec(p,v,col=RED,scale=1):
    p=np.asarray(p);v=np.asarray(v)*scale;length=np.linalg.norm(v)
    if length<1e-6:return VGroup()
    tip=p+v
    return VGroup(Line(p,tip,color=col,stroke_width=3),Cone(direction=v/length,height=.12,base_radius=.045,resolution=(3,8),checkerboard_colors=[col,col],stroke_width=0).shift(tip))
class ActionBase(ThreeDScene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.target_seconds=self.m['duration_seconds']
        self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES)
        self.scale=1.4 if SHORT else 1.5;self.stage=1.5 if SHORT else .45
        self.fixed(txt('자연의 최적화  05   /   STATIONARY ACTION',18,MUTED).move_to([0,7.25 if SHORT else 3.97,0]),txt(self.m['title'],30).move_to([0,6.35 if SHORT else 3.28,0]))
        self.fixed(Line([-3.8 if SHORT else -7,5.8 if SHORT else 2.82,0],[3.8 if SHORT else 7,5.8 if SHORT else 2.82,0],color=MUTED,stroke_opacity=.25))
        self.shot()
        for m in self.mobjects:m.clear_updaters(recursive=True)
        left=self.target_seconds-self.time
        if left<-.025:raise ValueError((self.INDEX+1,self.time,self.target_seconds))
        if left>.001:self.wait(left)
    def fixed(self,*m):self.add_fixed_in_frame_mobjects(*m)
    def flat(self):self.set_camera_orientation(phi=0,theta=-90*DEGREES)
    def info(self,s,note='',col=TEAL):
        group=VGroup(txt(s,30,col).move_to([0,-3.15 if SHORT else -1.85,0]))
        if note:group.add(txt(note,18,MUTED).move_to([0,-4.05 if SHORT else -2.45,0]))
        self.fixed(group);return group
    def foot(self,s):self.fixed(txt(s,15,MUTED).move_to([0,-4.85 if SHORT else -2.95,0]))
    def p(self,a):return np.array([(a[0]-2)*self.scale,0,(a[1]-1.4)*self.scale+self.stage])
    def label(self,s,p,size=20,col=WHITE):
        m=txt(s,size,col).move_to(p);self.add_fixed_orientation_mobjects(m);return m
    def trajectory(self,eps=0,col=GOLD,fun=q):return ParametricFunction(lambda t:self.p(fun(t,eps)) if fun is q else self.p(fun(t)),t_range=[0,4,.025],color=col,stroke_width=4)
    def physical(self,curve=True,ground=True):
        if curve:self.add(self.trajectory())
        if ground:self.add(Line(self.p([-.3,0]),self.p([4.3,0]),color=MUTED,stroke_width=1,stroke_opacity=.4))
    def moving(self,seconds=4,force=False,trace=False):
        tracker=ValueTracker(0);b=ball(self.p(q(0)));b.add_updater(lambda m:m.move_to(self.p(q(tracker.get_value()))));self.add(b)
        if trace:self.add(TracedPath(b.get_center,stroke_color=GOLD,stroke_width=4))
        if force:self.add(always_redraw(lambda:vec(self.p(q(tracker.get_value())),[0,0,-.8],RED)))
        self.play(tracker.animate.set_value(4),run_time=seconds,rate_func=linear)
        return tracker,b
    def axes(self,xrange,yrange,center,xlen,ylen,xlabel,ylabel):
        self.flat();ax=Axes(x_range=xrange,y_range=yrange,x_length=xlen,y_length=ylen,axis_config={'include_tip':False,'color':MUTED,'stroke_width':1.2}).move_to(center)
        self.add(ax)
        self.add(txt(xlabel,17,MUTED).next_to(ax,DOWN,buff=.12),txt(ylabel,20,MUTED).next_to(ax,UP,buff=.18))
        return ax
    def one_axes(self,kind='history'):
        if kind=='history':return self.axes([0,4,1],[0,3.5,1],[0,1.35 if SHORT else .45,0],6.2 if SHORT else 8.2,3.8 if SHORT else 2.8,'시간 t','높이 y(t)')
        return self.axes([0,4,1],[-3,3,1],[0,1.35 if SHORT else .45,0],6.2 if SHORT else 8.2,3.8 if SHORT else 2.8,'시간 t','라그랑지안 L(t) = K(t) − V(t)')
    def two_axes(self,second='lagrangian',first_label='높이 y(t)',second_label=None,first_xlabel='시간 t'):
        c1=[0,3.25,0] if SHORT else [-3.65,.5,0];c2=[0,-.35,0] if SHORT else [3.65,.5,0]
        xl=5.9 if SHORT else 5.45;yl=2.05 if SHORT else 2.5
        a=self.axes([0,4,1],[0,3.5,1],c1,xl,yl,first_xlabel,first_label)
        b=self.axes(([-1,1,.5] if second=='action' else [0,4,1]),([0,.8,.2] if second=='action' else ([-4,4,2] if second=='lagrangian' else [0,3.5,1])),c2,xl,yl,'변형 ε' if second=='action' else '시간 t',second_label or ('작용 차이 ΔS = S(ε) − S(0)' if second=='action' else '라그랑지안 L(t)'))
        return a,b
    def plot(self,ax,fn,col=GOLD,domain=(0,4),width=3.5):
        return ax.plot(lambda t:float(fn(t)),x_range=[*domain,.025],color=col,stroke_width=width,use_smoothing=False)
    def lock(self,ax):
        for t in [0,4]:
            point=ax.c2p(t,Y0);self.add(Dot(point,color=GOLD,radius=.065),RoundedRectangle(width=.18,height=.15,corner_radius=.025,color=WHITE,stroke_width=1.2).move_to(point+UP*.28),Arc(radius=.06,start_angle=0,angle=PI,color=WHITE,stroke_width=1.2).move_to(point+UP*.39))
        self.add(txt('t₁ = 0',16,MUTED).next_to(ax.c2p(0,0),DOWN,buff=.12),txt('t₂ = 4',16,MUTED).next_to(ax.c2p(4,0),DOWN,buff=.12))
    def histories(self,ax,all=True):
        group=VGroup()
        for k,c in ([('straight',MUTED),('high',TEAL),('low',BLUE),('actual',GOLD)] if all else [('actual',GOLD)]):
            curve=self.plot(ax,lambda t,k=k:candidate(t,k)[1],c,width=3.5 if k=='actual' else 1.7);group.add(curve)
        self.add(group);self.lock(ax);return group
    def energybars(self,tracker,vertical=False):
        def one(x,value,col):
            h=max(.012,float(value)/3*1.7);m=Rectangle(width=.26,height=h,color=col,fill_opacity=.65).rotate(PI/2,axis=RIGHT).move_to([x,0,-.6+h/2]);return m
        for index,(x,c,name) in enumerate([(-3.5,BLUE,'K'),(3.5,TEAL,'V')]):
            self.add(always_redraw(lambda index=index,x=x,c=c:one(x,energy(tracker.get_value(),vertical=vertical)[index],c)))
            self.label(name,[x,0,1.4],20,c)
    def eps_panels(self):
        a,b=self.two_axes('action');eps=ValueTracker(0)
        self.add(self.plot(a,y,GOLD,width=2))
        history=always_redraw(lambda:self.plot(a,lambda t:y(t,eps.get_value()),TEAL,width=3));self.add(history);self.lock(a)
        parabola=self.plot(b,lambda e:exact_action(e)-S0,PURPLE,domain=(-1,1));self.add(parabola)
        dot=Dot(b.c2p(0,0),color=PURPLE);dot.add_updater(lambda m:m.move_to(b.c2p(eps.get_value(),exact_action(eps.get_value())-S0)));self.add(dot)
        return a,b,eps
    def stationary_surfaces(self,three=False):
        self.set_camera_orientation(phi=64*DEGREES,theta=-73*DEGREES)
        centers=([-2.5,0,2.5] if SHORT else [-4.3,0,4.3]) if three else ([-2,2] if SHORT else [-3.3,3.3])
        kinds=['min','max','saddle'] if three else ['min','saddle']
        for x,k in zip(centers,kinds):
            scale=.7 if SHORT and three else .95
            def f(u,v,k=k):return u*u+v*v if k=='min' else (-u*u-v*v if k=='max' else u*u-v*v)
            col=TEAL if k=='min' else (BLUE if k=='max' else PURPLE)
            center=np.array([x,0,1.8 if SHORT else .6])
            mesh=Surface(lambda u,v,f=f,center=center:np.array([u*scale,v*scale,.4*f(u,v)])+center,u_range=[-1,1],v_range=[-1,1],resolution=(12,12),checkerboard_colors=[col,col],fill_opacity=.35,stroke_width=.5,stroke_color=col)
            self.add(mesh,ball(center,WHITE,.055))
            self.add(ParametricFunction(lambda u,f=f,center=center:center+np.array([u*scale,0,.4*f(u,0)]),t_range=[-1,1],color=GOLD,stroke_width=2.5),ParametricFunction(lambda v,f=f,center=center:center+np.array([0,v*scale,.4*f(0,v)]),t_range=[-1,1],color=BLUE,stroke_width=2.5))
            self.fixed(txt({'min':'최솟값','max':'극댓값','saddle':'안장점'}[k],22,col).move_to([x,-.85 if SHORT else -.95,0]),txt('∇f = 0',19,MUTED).move_to([x,-1.45 if SHORT else -1.4,0]))
    def mini(self,kind,center,size=1):
        c=np.array(center);g=VGroup()
        if kind=='soap':
            for sign in [-1,1]:g.add(ParametricFunction(lambda t,sign=sign:c+size*np.array([sign*.55*np.cosh(t),t,0]),t_range=[-.65,.65],color=TEAL,stroke_width=2.5))
            for yy in [-.65,.65]:g.add(Ellipse(width=1.34*size,height=.25*size,color=MUTED,stroke_width=1.5).move_to(c+UP*yy*size))
        elif kind=='chain':g.add(ParametricFunction(lambda t:c+size*np.array([t,.65*(np.cosh(t)-1)-.3,0]),t_range=[-1.1,1.1],color=GOLD,stroke_width=3))
        elif kind=='light':
            g.add(Line(c+size*np.array([-1,.3,0]),c+size*np.array([1,.3,0]),color=MUTED,stroke_width=1),Line(c+size*np.array([-.9,1,0]),c+size*np.array([.1,.3,0]),color=GOLD,stroke_width=3),Line(c+size*np.array([.1,.3,0]),c+size*np.array([.5,-.9,0]),color=GOLD,stroke_width=3))
        else:g.add(ParametricFunction(lambda t:c+size*np.array([.55*(t-np.sin(t))-.85,.75-.55*(1-np.cos(t)),0]),t_range=[0,PI],color=TEAL,stroke_width=3))
        return g
    def shot(self):
        i=self.INDEX
        if i==0:
            self.set_camera_orientation(phi=76*DEGREES,theta=-76*DEGREES);self.physical(False);self.info('공의 운동을 두 관점으로 설명한다','한순간의 힘 · 시간 전체의 운동 이력');self.moving(3.2,trace=True)
        elif i==1:
            self.physical();self.info('m a = F','중력은 매 순간 아래 방향으로 작용한다',RED);self.moving(5.5,force=True)
        elif i==2:
            self.physical()
            for t in np.linspace(0,4,5):
                p=self.p(q(t));self.add(ball(p,GOLD,.05),vec(p,[0,0,-.65],RED),vec(p,[VX,0,vy(t)],TEAL,.32))
            self.info('aₓ = 0   ·   aᵧ = −g','금색: 등시간 위치 · 청록: 속도 · 빨강: 같은 중력')
            self.foot('공기 저항 없음 · 수평 속도 일정 · 정점에서도 중력은 작용')
        elif i==3:
            self.physical();self.info('매 순간의 힘 → 전체 운동 이력','공간 경로에 시간 정보를 더한다');self.fixed(txt('시간 t  →',25,PURPLE).move_to([0,4.8 if SHORT else 2.35,0]))
        elif i==4:
            a=self.one_axes();self.histories(a,False);self.info('시작과 끝의 위치 · 시간을 고정','비교 대상은 y(t), 수평 운동 x(t)=t는 공통');self.foot('상대 단위 · t=0..4 · y(0)=y(4)=0.5')
        elif i==5:
            a=self.one_axes();self.histories(a);t=ValueTracker(.5)
            for k,c in [('straight',MUTED),('high',TEAL),('low',BLUE),('actual',GOLD)]:
                dot=Dot(a.c2p(t.get_value(),candidate(t.get_value(),k)[1]),color=c);dot.add_updater(lambda m,k=k:m.move_to(a.c2p(t.get_value(),candidate(t.get_value(),k)[1])));self.add(dot)
            line=always_redraw(lambda:DashedLine(a.c2p(t.get_value(),0),a.c2p(t.get_value(),3.5),color=MUTED,dash_length=.1));self.add(line)
            self.info('같은 시각에 서로 다른 위치','금색은 실제 운동 · 나머지는 비교하는 가상 이력');self.play(t.animate.set_value(2),run_time=3);self.wait(2)
        elif i==6:
            a,b=self.two_axes('history',first_label='공간 경로 · x–y',second_label='시간 이력 · t–y',first_xlabel='수평 위치 x')
            self.add(self.plot(a,y,GOLD),self.plot(b,y,GOLD),self.plot(b,lambda t:retimed_q(t)[1],TEAL));t=ValueTracker(0)
            for fn,c in [(q,GOLD),(retimed_q,TEAL)]:
                d1=Dot(color=c);d2=Dot(color=c)
                d1.add_updater(lambda m,fn=fn:m.move_to(a.c2p(*fn(t.get_value()))));d2.add_updater(lambda m,fn=fn:m.move_to(b.c2p(t.get_value(),fn(t.get_value())[1])));self.add(d1,d2)
            self.info('같은 공간 경로여도 시간 이력은 다르다','금색 q(t) · 청록 q(t²/4), 0≤t≤4');self.play(t.animate.set_value(3.2),run_time=3.5,rate_func=linear)
        elif i==7:
            a=self.one_axes();self.histories(a);self.info('실제 운동은 어떤 조건을 만족할까?','곡선의 모양을 넘어 시간에 따른 운동을 비교')
            self.play(Indicate(self.plot(a,y,GOLD)),run_time=1.5)
        elif i==8:
            self.physical();t=ValueTracker(0);b=ball(self.p(q(0)));b.add_updater(lambda m:m.move_to(self.p(q(t.get_value()))));self.add(b);self.energybars(t)
            title=self.info('K + V = 일정','K = ½mv²  ·  V = mgy');self.play(t.animate.set_value(4),run_time=5,rate_func=linear)
            self.play(FadeOut(title),run_time=.3);self.info('이번에는 두 에너지의 차이 · K − V','합과 차이는 서로 다른 물리량이다',PURPLE)
        elif i==9:
            self.physical();t=ValueTracker(0);b=ball(self.p(q(0)));b.add_updater(lambda m:m.move_to(self.p(q(t.get_value()))));self.add(b);self.energybars(t)
            self.info('L = K − V','라그랑지안 · Lagrangian',PURPLE);self.foot('보존되는 에너지 K+V와 구별한다');self.play(t.animate.set_value(4),run_time=3.2,rate_func=linear)
        elif i==10:
            a=self.one_axes('lagrangian');self.add(self.plot(a,lagrangian,PURPLE));t=ValueTracker(0)
            roots=[2-np.sqrt(2),2+np.sqrt(2)]
            def area():
                groups=VGroup();stop=t.get_value()
                for lo,hi,col in [(0,roots[0],GOLD),(roots[0],roots[1],PURPLE),(roots[1],4,GOLD)]:
                    upper=min(stop,hi)
                    if upper<=lo+.0001:continue
                    xx=np.linspace(lo,upper,60);points=[a.c2p(lo,0)]+[a.c2p(x,lagrangian(x)) for x in xx]+[a.c2p(upper,0)]
                    groups.add(Polygon(*points,fill_color=col,fill_opacity=.3,stroke_width=0))
                return groups
            self.add(always_redraw(area));dot=Dot(color=WHITE);dot.add_updater(lambda m:m.move_to(a.c2p(t.get_value(),lagrangian(t.get_value()))));self.add(dot)
            readout=always_redraw(lambda:txt(f'누적 S = {accumulated(t.get_value()):+.3f}',23,PURPLE).move_to([0,-1.95,0] if SHORT else [4.65,-1.25,0]));self.fixed(readout)
            self.info('S = ∫ L dt   ·   작용 Action','양수는 더하고 음수는 뺀다 · 부호 있는 시간 적분',PURPLE);self.play(t.animate.set_value(4),run_time=5.5,rate_func=linear)
        elif i==11:
            a,b=self.two_axes();eps=ValueTracker(0)
            self.add(self.plot(a,y,GOLD,width=1.8),self.plot(b,lagrangian,GOLD,width=1.8))
            self.add(always_redraw(lambda:self.plot(a,lambda t:y(t,eps.get_value()),TEAL)),always_redraw(lambda:self.plot(b,lambda t:lagrangian(t,eps.get_value()),PURPLE)))
            self.lock(a);self.info('운동 이력 전체 → 하나의 작용값','위치뿐 아니라 속도도 함께 다시 계산한다',PURPLE)
            readout=always_redraw(lambda:txt(f'ε = {eps.get_value():+.2f}    S = {exact_action(eps.get_value()):+.3f}',23,PURPLE).move_to([0,-1.95 if SHORT else -1.15,0]));self.fixed(readout)
            self.play(eps.animate.set_value(.75),run_time=2);self.play(eps.animate.set_value(-.6),run_time=2)
        elif i==12:
            a=self.one_axes();self.histories(a,False);self.info('실제 운동 y*(t)','끝점 위치·시간 고정 · ε=0',GOLD)
        elif i==13:
            a,b,eps=self.eps_panels();self.info('yε(t) = y*(t) + εη(t)','η(t) = sin(πt/4)  ·  η(0)=η(4)=0',PURPLE)
            self.play(eps.animate.set_value(-.8),run_time=1.5);self.play(eps.animate.set_value(.8),run_time=2);self.play(eps.animate.set_value(0),run_time=1.5)
            self.foot('ΔS = mπ²ε²/(4T) · T=4 · 유한 변형에서는 ΔS>0')
        elif i==14:
            a,b,eps=self.eps_panels();self.add(Line(b.c2p(-.55,0),b.c2p(.55,0),color=WHITE,stroke_width=3));self.info('dS/dε |ε=0 = 0    →    δS = 0','일차 변화량 0 · 유한 변화량이 항상 0인 것은 아니다',PURPLE)
        elif i==15:
            self.stationary_surfaces();self.info('정지 조건이 항상 최솟값을 뜻하지는 않는다','두 정지점 모두 일차 변화가 0',PURPLE);self.foot('별도의 일반 수학 예시 · 지금의 공은 작용의 최솟값을 갖는다')
            self.fixed(txt('f=u²+v²',21,TEAL).move_to([-2 if SHORT else -3.3,3.8 if SHORT else 2.3,0]),txt('f=u²−v²',21,PURPLE).move_to([2 if SHORT else 3.3,3.8 if SHORT else 2.3,0]))
        elif i==16:
            self.physical();self.info('δS = 0    ?    m a = F','전체 운동의 조건과 순간적인 힘은 어떻게 연결될까?',PURPLE)
        elif i==17:
            self.physical();t=ValueTracker(0);b=ball(self.p(q(0)));b.add_updater(lambda m:m.move_to(self.p(q(t.get_value()))));self.add(b);self.energybars(t,True)
            self.info('Lᵧ = ½m(dy/dt)² − mgy','Sᵧ = ∫ Lᵧ dt · 수직 성분에 집중한다',PURPLE);self.foot('고정한 수평 운동의 작용은 모든 후보에 공통인 상수');self.play(t.animate.set_value(4),run_time=5.5,rate_func=linear)
        elif i==18:
            a=self.one_axes();eps=ValueTracker(0);self.add(self.plot(a,y,GOLD,width=2),always_redraw(lambda:self.plot(a,lambda t:y(t,eps.get_value()),TEAL)));self.lock(a)
            self.info('위치 y + εη   ·   속도 dy/dt + εdη/dt','δSᵧ = δ∫[½m(dy/dt)² − mgy]dt = 0',PURPLE);self.foot('변분은 후보 운동의 비교 · 실제 시간의 진행과 구별한다')
            self.play(eps.animate.set_value(.55),run_time=1.6);self.play(eps.animate.set_value(0),run_time=1.6)
        elif i==19:
            self.flat();positions=[4.3,2.85,1.3,-.3] if SHORT else [2.1,1.15,.2,-.75]
            lines=[('δS = ∫[m(dy/dt)(dη/dt) − mgη]dt',WHITE),('부분적분 · η(0)=η(T)=0',MUTED),('δS = −∫[m(d²y/dt²) + mg]η dt = 0',PURPLE),('임의의 η(t)  →  m(d²y/dt²) = −mg',GOLD)]
            for j,((s,c),yy) in enumerate(zip(lines,positions)):
                obj=txt(s,25 if SHORT else 30,c).move_to([0,yy,0]);self.play(FadeIn(obj,shift=UP*.15),run_time=.75)
                if j<3:self.wait(.45)
            self.info('속도의 변분 → 가속도에 관한 조건','임의의 끝점 고정 변형에서 성립해야 한다')
        elif i==20:
            self.flat();self.add(txt('m(d²y/dt²) = −mg',35,GOLD).move_to([0,2.1 if SHORT else .9,0]),txt('m(d²x/dt²) = 0',27,MUTED).move_to([0,.7 if SHORT else 0,0]));self.info('m a = F','가속도 × 질량 = 힘',RED)
        elif i==21:
            self.flat();sep=2.1 if SHORT else 3.5;scale=.6 if SHORT else .8;stage=1.6 if SHORT else .65
            def pt(v,offset=0):return np.array([(v[0]-2)*scale+offset,(v[1]-1.3)*scale+stage,0])
            l=ParametricFunction(lambda t:pt(newton(t),-sep),t_range=[0,4,.025],color=GOLD,stroke_width=3.5);r=ParametricFunction(lambda t:pt(variational(t),sep),t_range=[0,4,.025],color=TEAL,stroke_width=3.5);self.add(l,r)
            self.add(txt('뉴턴 · 힘에서 출발',20,GOLD,width=3.8 if SHORT else 6).move_to([-sep,3.8 if SHORT else 2.1,0]),txt('작용 · 정지 조건에서 출발',20,TEAL,width=3.8 if SHORT else 6).move_to([sep,3.8 if SHORT else 2.1,0]))
            t=ValueTracker(0);b1=Dot(color=GOLD,radius=.07);b2=Dot(color=TEAL,radius=.065);b1.add_updater(lambda m:m.move_to(pt(newton(t.get_value()),-sep)));b2.add_updater(lambda m:m.move_to(pt(variational(t.get_value()),sep)));self.add(b1,b2)
            self.info('두 관점 · 같은 운동방정식','같은 초기 위치·속도에서 동일한 운동을 얻는다');self.play(t.animate.set_value(4),run_time=4.5,rate_func=linear)
            b1.clear_updaters();b2.clear_updaters();self.play(l.animate.shift(RIGHT*sep),r.animate.shift(LEFT*sep),b1.animate.shift(RIGHT*sep),b2.animate.shift(LEFT*sep),run_time=1.6)
            self.foot('뉴턴 초기값 적분 / 작용 정지식의 독립 경계값 계산 · 해가 일치')
        elif i==22:
            self.physical(False);self.info('현재의 힘 → 현재의 가속도','물체 안에서 전체 후보 경로를 계산하는 과정이 아니다',RED);self.moving(6.5,force=True,trace=True)
        elif i==23:
            self.physical();self.info('δS = 0','국소적인 운동법칙 ↔ 전체 운동의 정지 조건',PURPLE);self.moving(2.8)
        elif i==24:
            self.flat();centers=[[-2,3.25,0],[2,3.25,0],[-2,.3,0],[2,.3,0]] if SHORT else [[-5.4,.65,0],[-1.8,.65,0],[1.8,.65,0],[5.4,.65,0]]
            for k,c,name,expr in zip(['soap','chain','light','cycloid'],centers,['비눗막','사슬','빛','최속강하선'],['표면에너지','위치에너지','이동 시간','이동 시간']):
                group=VGroup(self.mini(k,c,.8),txt(name,21,WHITE).move_to(np.array(c)+DOWN*1.15),txt(expr,17,MUTED).move_to(np.array(c)+DOWN*1.65));self.play(FadeIn(group),run_time=.65)
            self.wait(2.4);self.info('최소화만이 전부는 아니다','자연의 운동에는 더 일반적인 정지 조건이 나타난다',PURPLE)
        elif i==25:
            self.stationary_surfaces(True);self.info('δJ = 0','최소·최대·안장점의 공통점: 일차 변화량 0',PURPLE);self.foot('일반 수학 예시 · 최댓값 도식은 이 공의 작용을 나타내지 않음')
        else:
            self.flat();labels=[]
            for x,s,c in [(-2.7,'표면에너지',TEAL),(-.9,'위치에너지',GOLD),(.9,'이동 시간',BLUE),(2.7,'작용',PURPLE)]:
                obj=txt(s,20,c,width=1.7).move_to([x,3.7 if SHORT else 1.8,0]);labels.append(obj);self.add(obj)
            self.add(txt('δJ = 0',55,PURPLE).move_to([0,1.6 if SHORT else .4,0]));self.info('서로 다른 물리법칙 · 공통된 변분의 수학','각 문제의 경계조건과 제약조건 안에서 성립한다');self.foot('자연의 최적화  /  NATURE & VARIATION')
            self.wait(2.8);self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.8)
