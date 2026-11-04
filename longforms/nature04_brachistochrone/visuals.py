import os,json
from pathlib import Path
import numpy as np
from manim import *
from physics import X,Y,G,A,THETA,TC,TS,TD,cycle,deep,pos,geometry,light,layers,metrics
P=Path(__file__).resolve().parent;SHORT=os.environ.get('BRACHI_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#091421'
TEAL='#35C9D0';BLUE='#579BE8';GOLD='#E3A447';RED='#ED7681';MUTED='#8EA9BB';WHITE='#F2F6FA'
def txt(s,size=27,col=WHITE,width=None):
    m=Text(s,font='Malgun Gothic',font_size=size,color=col,line_spacing=.8)
    w=width or (8 if SHORT else 14)
    if m.width>w:m.scale_to_fit_width(w)
    return m
def ball(p,col=GOLD):return Sphere(center=p,radius=.09,resolution=(5,10),checkerboard_colors=[col,col],stroke_width=0)
class BrachiBase(ThreeDScene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.target_seconds=self.m['duration_seconds']
        self.set_camera_orientation(phi=90*DEGREES,theta=-90*DEGREES)
        self.s=1.18 if SHORT else 1.;self.cx=2;self.cy=1.5;self.z=1.25 if SHORT else .45
        self.fixed(txt('자연의 최적화  04   /   BRACHISTOCHRONE',18,MUTED).move_to([0,7.25 if SHORT else 3.97,0]),txt(self.m['title'],30).move_to([0,6.35 if SHORT else 3.28,0]))
        self.fixed(Line([-3.8 if SHORT else -7,5.8 if SHORT else 2.82,0],[3.8 if SHORT else 7,5.8 if SHORT else 2.82,0],color=MUTED,stroke_opacity=.25))
        self.shot()
        for m in self.mobjects:m.clear_updaters(recursive=True)
        rest=self.target_seconds-self.time
        if rest<-.025:raise ValueError((self.INDEX,self.time,self.target_seconds))
        if rest>.001:self.wait(rest)
    def fixed(self,*m):self.add_fixed_in_frame_mobjects(*m)
    def p(self,q):return np.array([(q[0]-self.cx)*self.s,0,(self.cy-q[1])*self.s+self.z])
    def label(self,s,q,col=WHITE,size=21):
        m=txt(s,size,col).move_to(q);self.add_fixed_orientation_mobjects(m);return m
    def info(self,s,note='',col=TEAL):
        self.fixed(txt(s,30,col).move_to([0,-3.15 if SHORT else -1.8,0]))
        if note:self.fixed(txt(note,18,MUTED).move_to([0,-4.05 if SHORT else -2.43,0]))
    def foot(self,s):self.fixed(txt(s,15,MUTED).move_to([0,-4.85 if SHORT else -2.95,0]))
    def track(self,kind,col=TEAL,width=5):return ParametricFunction(lambda u:self.p(geometry(kind,u)),t_range=[0,1,.008],color=col,stroke_width=width)
    def base(self,kinds=('straight','cycle')):
        for k in kinds:self.add(self.track(k,{'straight':BLUE,'cycle':TEAL,'deep':RED}[k]))
        for q,name in [([0,0],'A'),([X,Y],'B')]:self.add(ball(self.p(q),WHITE));self.label(name,self.p(q)+OUT*.3+LEFT*.15)
    def runrace(self,kinds=('straight','cycle'),duration=4.5):
        timer=ValueTracker(0);end=max({'straight':TS,'cycle':TC,'deep':TD}[k] for k in kinds)
        for k in kinds:
            b=ball(self.p([0,0]),{'straight':BLUE,'cycle':GOLD,'deep':RED}[k]);b.add_updater(lambda m,k=k:m.move_to(self.p(pos(k,timer.get_value()))));self.add(b)
        self.play(timer.animate.set_value(end),run_time=duration,rate_func=linear)
    def overlay(self):
        self.base(('cycle',));ray=ParametricFunction(lambda u:self.p(light(Y*u)),t_range=[0,1,.008],color=GOLD,stroke_width=2.2)
        self.play(Create(ray),run_time=1.5)
    def layerdraw(self,n,col=GOLD):
        points,p,v=layers(n);g=VGroup()
        for j in range(n):
            y0=Y*j/n;y1=Y*(j+1)/n
            g.add(Polygon(*[self.p(q) for q in [[-.3,y0],[4.3,y0],[4.3,y1],[-.3,y1]]],fill_color=BLUE,fill_opacity=.035+.12*j/n,stroke_width=.25,stroke_color=MUTED))
        ray=VMobject(color=col,stroke_width=4).set_points_as_corners([self.p(q) for q in points]);g.add(ray);return g
    def shot(self):
        i=self.INDEX
        if i==0:
            self.set_camera_orientation(phi=75*DEGREES,theta=-78*DEGREES);self.base(())
            self.add(Line(self.p([-.5,0]),self.p([-.5,2]),color=GOLD));self.label('g ↓',self.p([-.9,1]),GOLD)
            self.info('最短 거리 ≠ 최소 시간'.replace('最短','최단'),'서로 다른 높이의 두 지점')
        elif i==1:
            self.set_camera_orientation(phi=77*DEGREES,theta=-80*DEGREES);self.base(('straight',));self.info('마찰 없음 · 정지 출발','구슬은 미끄러지는 점입자의 위치 표식')
            self.runrace(('straight',),4)
        elif i==2:
            self.base();self.info('직선: 가장 짧은 거리','직선은 파랑 · 사이클로이드는 청록')
            self.runrace(duration=3.4)
        elif i==3:
            self.base();self.info(f'사이클로이드 {TC:.3f}  <  직선 {TS:.3f}','같은 물리 시간으로 비교 · 도착 이후 표식 고정')
            self.foot('상대 단위 · A=(0,0), B=(4,3), g=1')
            self.runrace(duration=7.5)
        elif i==4:
            self.s=.61 if SHORT else .53;self.cy=3.5;self.z=1.3 if SHORT else .35;self.base(('straight','cycle','deep'))
            self.info(f'깊은 경로 {TD:.3f}  >  사이클로이드 {TC:.3f}',f'이동 거리: 직선 5.00 · 사이클로이드 {metrics()["cycle_length"]:.2f} · 깊은 곡선 12.16')
            self.foot('같은 끝점 · 같은 중력 · 상대 단위의 계산값')
            self.runrace(('straight','cycle','deep'),6)
        elif i==5:
            self.base();self.info('어떤 곡선이 시간을 최소화할까?','경로의 길이와 깊이에 따른 속력을 함께 고려')
            self.play(Indicate(self.track('cycle',GOLD)),run_time=1.5)
        elif i==6:
            self.base(('cycle',));self.info('mgy = ½mv²  →  v = √(2gy)','y: 출발점에서 아래로 내려간 높이')
            t=ValueTracker(0);b=ball(self.p([0,0]));b.add_updater(lambda m:m.move_to(self.p(pos('cycle',t.get_value()))));self.add(b)
            def energybar(x,value,col):
                h=max(.015,value/Y*1.5);return Rectangle(width=.22,height=h,color=col,fill_opacity=.7).rotate(PI/2,axis=RIGHT).move_to([x,0,-.6+h/2])
            potential=always_redraw(lambda:energybar(-3.35,Y-pos('cycle',t.get_value())[1],BLUE));kinetic=always_redraw(lambda:energybar(3.35,pos('cycle',t.get_value())[1],GOLD));self.add(potential,kinetic)
            self.label('위치',[-3.35,0,1.3],BLUE,16);self.label('운동',[3.35,0,1.3],GOLD,16)
            self.play(t.animate.set_value(TC*.8),run_time=5,rate_func=linear)
        elif i in [7,8]:
            self.base();ys=1.5;tc=np.sqrt(A)*np.arccos(1-ys/A);ts=TS*np.sqrt(ys/Y)
            self.add(DashedLine(self.p([0,ys]),self.p([4,ys]),color=MUTED))
            for k,t,c in [('straight',ts,BLUE),('cycle',tc,GOLD)]:self.add(ball(self.p(pos(k,t)),c))
            self.info('같은 높이 y → 같은 속력 √(2gy)' if i==7 else f'도달 시간: 청록 {tc:.3f} · 파랑 {ts:.3f}','각 경로가 해당 높이에 도달한 순간을 따로 비교')
        elif i==9:
            self.base(('cycle',));self.info('Δt ≈ Δs / v    ·    dt = ds / v','작은 구간의 근사 → 무한히 작은 구간의 관계')
            for j in range(12):
                c=GOLD if j%2==0 else TEAL;self.add(Line(self.p(cycle(THETA*j/12)),self.p(cycle(THETA*(j+1)/12)),color=c,stroke_width=6))
            self.play(Indicate(self.track('cycle',GOLD)),run_time=2)
        elif i==10:
            self.base();self.info('T = ∫ ds / √(2gy)','출발점 A · 도착점 B 고정, 곡선 전체를 비교')
            for h in [.25,.5,.75]:
                c=ParametricFunction(lambda u,h=h:self.p((1-h)*geometry('straight',u)+h*geometry('cycle',u)),t_range=[0,1],color=MUTED,stroke_width=1.3);self.play(Create(c),run_time=.7)
            self.foot('후보 곡선의 비교는 수학적 설계이며 물체의 형태 탐색이 아님')
        elif i==11:
            self.base(('cycle',));self.info('최속강하선 문제','Brachistochrone problem')
        elif i==12:
            self.base(('straight',));c=self.track('cycle',GOLD);self.play(Create(c),run_time=2);self.info('사이클로이드 · Cycloid','x = a(θ − sinθ),  y = a(1 − cosθ)')
        elif i==13:
            self.s=.78 if SHORT else .72;self.cx=2.2;self.cy=1.5;self.z=1.1 if SHORT else .4
            self.add(Line(self.p([-1.6,0]),self.p([6.2,0]),color=MUTED))
            t=ValueTracker(0)
            circle=always_redraw(lambda:ParametricFunction(lambda u:self.p([A*t.get_value()+A*np.cos(u),A+A*np.sin(u)]),t_range=[0,TAU],color=BLUE,stroke_width=2))
            radius=always_redraw(lambda:Line(self.p([A*t.get_value(),A]),self.p(cycle(t.get_value())),color=GOLD))
            dot=ball(self.p([0,0]));dot.add_updater(lambda m:m.move_to(self.p(cycle(t.get_value()))));trace=TracedPath(dot.get_center,stroke_color=TEAL,stroke_width=5)
            self.add(circle,radius,dot,trace);self.info('원 위의 한 점이 그리는 곡선','미끄럼 없는 회전: 중심 이동 거리 = aθ');self.foot('원의 회전은 곡선 생성법 · 앞의 입자는 회전 관성 없는 점입자')
            self.play(t.animate.set_value(THETA),run_time=3.3,rate_func=linear)
        elif i in [14,15,16]:
            self.s=.57 if SHORT else .7;self.cx=2;self.z=1.3 if SHORT else .5
            separation=2.05 if SHORT else 3.4
            shift=LEFT*separation
            curve=self.track('cycle',TEAL).shift(shift);self.add(curve)
            for q,name in [([0,0],'A'),([X,Y],'B')]:self.add(ball(self.p(q)+shift,WHITE))
            from scipy.optimize import brentq
            crossing=brentq(lambda x:x/np.hypot(x,1.5)/1.-(4-x)/np.hypot(4-x,1.5)/.75,.001,3.999)
            shift=RIGHT*separation
            interface=Line(self.p([-.3,1.5])+shift,self.p([4.3,1.5])+shift,color=MUTED,stroke_width=1)
            ray=VGroup(Line(self.p([0,0])+shift,self.p([crossing,1.5])+shift,color=GOLD,stroke_width=4),Line(self.p([crossing,1.5])+shift,self.p([4,3])+shift,color=GOLD,stroke_width=4));self.add(interface,ray)
            self.label('물체 · 중력',self.p([2,-.6])+LEFT*separation,TEAL,20);self.label('빛 · 매질',self.p([2,-.6])+RIGHT*separation,GOLD,20)
            self.info(['물체: 중력에 따라 속력 변화','물체와 빛: T = ∫ ds / v','물체 v = √(2gy)   ·   빛 v = c/n'][i-14],['빛: 매질에 따라 속력 변화','같은 시간 식 · 서로 다른 속력 함수','같은 수학적 표현, 서로 다른 물리적 원인'][i-14])
            self.foot('공기·물의 속력 차이를 단순화한 광선 / 두 경로의 시간값은 다름')
            if i==14:self.play(Indicate(curve),Indicate(ray),run_time=2)
        elif i in [17,18,19]:
            self.info('가상의 매질 · 깊어질수록 빠르게','빛의 속력 분포를 설계한 수학적 대응')
            self.foot('y=0은 연속 모형의 극한 · 유한층은 중간 깊이 속력을 사용')
            if i==17:
                g=self.layerdraw(6);self.play(Create(g),run_time=3);self.label('느림',self.p([-.8,.3]),BLUE);self.label('빠름',self.p([-.8,2.7]),GOLD)
            elif i==18:
                self.add(self.layerdraw(6));points,p,v=layers(6)
                for q in points[1:-1]:self.add(DashedLine(self.p(q+[0,-.24]),self.p(q+[0,.24]),color=WHITE,dash_length=.05))
                self.fixed(txt('sinθ / v = 일정  (θ: 수직 법선 기준)',21,GOLD).move_to([0,4.8 if SHORT else 2.35,0]))
            else:
                g=self.layerdraw(6);self.add(g)
                count=txt('N = 6',23,GOLD).move_to([0,4.8 if SHORT else 2.35,0]);self.fixed(count)
                for n in [12,24,48]:
                    new=self.layerdraw(n);self.play(Transform(g,new),Transform(count,txt(f'N = {n}',23,GOLD).move_to(count)),run_time=1.1)
                self.play(Create(ParametricFunction(lambda u:self.p(light(Y*u)),t_range=[0,1],color=TEAL,stroke_width=2)),run_time=1.2)
        elif i==20:
            self.overlay();self.info('v빛(y) = √(2gy) = v물체(y)','가상의 속력 분포를 같게 설정하면 시간 식도 같다')
            self.foot('유한층의 근사 경로와 연속 극한은 구별한다')
        elif i==21:
            self.overlay();self.info('같은 속력 함수 → 같은 시간 최소화','청록: 사이클로이드 · 금색: 굴절 법칙으로 별도 계산')
            self.foot('sinθ / v = 일정 → 연속 굴절 → 사이클로이드')
        elif i==22:
            self.overlay();self.info('빛은 전파한다 · 트랙은 우리가 설계한다','물체가 스스로 최적의 미끄럼틀을 만들지는 않는다')
            self.runrace(('cycle',),3.5)
        elif i==23:
            self.base(('cycle',));theta=1.7;q=cycle(theta);p=self.p(q);self.add(ball(p))
            normal=np.array([np.cos(theta/2),0,np.sin(theta/2)])
            self.add(Line(p,p+DOWN*.0-OUT*.9,color=GOLD),Line(p,p+normal*.9,color=TEAL));self.label('mg',p-OUT*1.1,GOLD);self.label('N',p+normal*1.1,TEAL)
            self.info('중력 + 접촉력 → 주어진 트랙 위 운동','최적의 트랙을 고르는 것은 별도의 수학적 문제')
        elif i==24:
            self.set_camera_orientation(phi=77*DEGREES,theta=-79*DEGREES);self.base();self.info(f'설계 결과: {TC:.3f} < {TS:.3f}','이상적인 점입자 모형 · 동일 A와 B · 상대 단위')
            self.runrace(duration=4.7)
        else:
            self.overlay();self.info('δT = 0   ·   변분법','국소적인 물리법칙을 전체 경로의 조건으로 표현한다')
            self.runrace(('cycle',),4.5)
            self.fixed(txt('Calculus of Variations',23,GOLD).move_to([0,4.8 if SHORT else 2.3,0]));self.wait(1)
            for m in self.mobjects:m.clear_updaters(recursive=True)
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.8)
