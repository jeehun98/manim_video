"""One quadratic loss: true surfaces, level sets, derivatives and finite steps."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';ORANGE='#FFB45F';GREEN='#55DFA3';PURPLE='#BB97FF';CYAN='#53D7D0';OUT='#8FD8FF'
THETA=np.array([2.,1.]);GRAD=np.array([4.,8.]);NORM=float(np.linalg.norm(GRAD));GA=float(np.arctan2(8,4));DESCENT_ANGLE=GA+PI
def loss(v):return float(v[0]**2+4*v[1]**2)
def txt(s,size=29,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class GradientBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.main=np.array([0,1.7,0]) if SHORT else np.array([-4,0,0]);self.panel=np.array([0,-2.55,0]) if SHORT else np.array([3.6,.35,0]);self.unit=.78 if SHORT else .64
        self.angle=ValueTracker(0);self.eta=ValueTracker(0);self.surface_alpha=ValueTracker(1);self.content=VGroup()
        self.add(txt('DOT PRO   /   LEVEL 10',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],30,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        y=5.65 if SHORT else 2.65;self.add(Line([-3.9 if SHORT else -7,y,0],[3.9 if SHORT else 7,y,0],color=GRAY,stroke_opacity=.25))
        for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],['θ 현재점','∇L 기울기','u 이동방향','ΔL 손실변화'],[BLUE,ORANGE,GREEN,PURPLE]):self.add(txt(s,16,c,width=2.5).move_to([x,5.15 if SHORT else -3.03,0]))
        self.header=list(self.mobjects);self.shot();self.to(self.meta['end'])
    def to(self,t):
        self.update_mobjects(0);left=t-self.start-self.time
        if left<-.04:raise RuntimeError((self.INDEX,self.time,t-self.start))
        if left>.001:self.wait(left)
    def clear_body(self):
        for m in list(self.mobjects):
            if m not in self.header:self.remove(m)
        self.content=VGroup()
    def info(self,s,note='',color=INK,size=30):
        self.remove(self.content);self.content=VGroup(txt(s,size,color,width=7.9 if SHORT else 6.7).move_to(self.panel))
        if note:self.content.add(txt(note,22,GRAY,width=7.8 if SHORT else 6.6).next_to(self.content[0],DOWN,buff=.4))
        self.add(self.content)
    def below(self,s,color=INK,offset=-1.65,size=22):
        m=txt(s,size,color,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0]);self.add(m);return m
    def pos(self,v):return self.main+self.unit*np.r_[v,0]
    def arrow(self,a,b,color,width=5):
        p,q=self.pos(a),self.pos(b)
        if np.linalg.norm(p-q)<1e-6:return Dot(q,radius=.01,color=color)
        return Arrow(p,q,buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.14)
    def contours(self,point=True):
        self.add(Line(self.pos([-5.1,0]),self.pos([5.1,0]),color=GRAY,stroke_width=1,stroke_opacity=.5),Line(self.pos([0,-2.8]),self.pos([0,2.8]),color=GRAY,stroke_width=1,stroke_opacity=.5))
        for c in [1,2.72,4,8,12,19.52,24]:
            color=interpolate_color(ManimColor(CYAN),ManimColor(ORANGE),c/24)
            self.add(Ellipse(width=2*np.sqrt(c)*self.unit,height=np.sqrt(c)*self.unit,color=color,stroke_width=1.2,stroke_opacity=.5).move_to(self.main))
            if c in [2.72,8,19.52]:
                at=np.array([-.866*np.sqrt(c),.25*np.sqrt(c)]);self.add(txt(f'L={c:g}',16,GRAY,width=1.5).move_to(self.pos(at)))
        self.add(txt('θ₁',20,GRAY,width=1).move_to(self.pos([5.1,0])+[.16,-.18,0]),txt('θ₂',20,GRAY,width=1).move_to(self.pos([0,2.8])+[.15,.15,0]),txt('0',15,GRAY,width=.5).move_to(self.main+[-.14,-.18,0]))
        if point:self.current_point()
    def current_point(self):
        self.add(Dot(self.pos(THETA),radius=.07,color=BLUE).set_z_index(9),txt('θ = (2, 1)',20,BLUE,width=2.3).move_to(self.pos(THETA)+[.5,-.28,0]).set_z_index(10))
    def gradient(self):
        self.add(self.arrow(THETA,THETA+.18*GRAD,ORANGE,6).set_z_index(7),txt('∇L = (4, 8)',21,ORANGE,width=2.5).move_to(self.pos(THETA+.18*GRAD)+[.25,.25,0]).set_z_index(10))
        self.add(txt('주황 기울기 화살표: 0.18배 표시',16,GRAY,width=6).move_to(self.main+[0,-2.3 if SHORT else -2.15,0]))
    def u(self):return np.array([np.cos(self.angle.get_value()),np.sin(self.angle.get_value())])
    def derivative(self):return float(GRAD@self.u())
    def direction(self,circle=False):
        if circle:self.add(Circle(radius=self.unit,color=GRAY,stroke_width=1,stroke_opacity=.5).move_to(self.pos(THETA)))
        self.add(always_redraw(lambda:self.arrow(THETA,THETA+self.u(),GREEN,6).set_z_index(8)))
        self.add(always_redraw(lambda:txt('u',22,GREEN,width=.6).move_to(self.pos(THETA+self.u())+[.12,-.21,0]).set_z_index(10)))
    def turn(self,angle,d=2):self.play(self.angle.animate.set_value(angle),run_time=d,rate_func=linear)
    def meter(self,cosine=False,offset=0):
        def make():
            value=self.derivative();color=ORANGE if value>1e-5 else GREEN if value< -1e-5 else INK
            return txt((f'cos φ = {value/NORM:+.3f}' if cosine else f'DᵤL = ∇L · u = {value:+.2f}'),32,color,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0])
        self.add(always_redraw(make))
    def angle_arc(self):
        def make():
            delta=(self.angle.get_value()-GA+PI)%(2*PI)-PI
            if abs(delta)<.001:return VGroup()
            return Arc(radius=.46*self.unit,start_angle=GA,angle=delta,color=INK,stroke_width=2).shift(self.pos(THETA)).set_z_index(10)
        self.add(always_redraw(make))
    def project3(self,v):
        x,y,z=v;a=25*DEGREES;b=-25*DEGREES
        sx=np.cos(b)*x-np.sin(b)*y;sy=-np.sin(a)*(np.sin(b)*x+np.cos(b)*y)+np.cos(a)*(.15*z)
        center=np.array([0,.9,0]) if SHORT else np.array([-4,-.8,0]);scale=.92 if SHORT else .74
        return center+scale*np.array([sx,sy,0])
    def surface(self,current=False):
        g=VGroup();patches=[];xs=np.linspace(-3,3,21);ys=np.linspace(-1.6,1.6,17)
        for x0,x1 in zip(xs,xs[1:]):
            for y0,y1 in zip(ys,ys[1:]):
                vertices=[[x0,y0,loss([x0,y0])],[x1,y0,loss([x1,y0])],[x1,y1,loss([x1,y1])],[x0,y1,loss([x0,y1])]]
                level=np.mean([v[2] for v in vertices]);color=interpolate_color(ManimColor(CYAN),ManimColor(ORANGE),min(level/19.3,1))
                poly=Polygon(*(self.project3(v) for v in vertices),fill_color=color,fill_opacity=.72,stroke_color=color,stroke_width=.55,stroke_opacity=.7)
                depth=-.423*(x0+x1)/2+.906*(y0+y1)/2;patches.append((depth,poly))
        for _,poly in sorted(patches,key=lambda p:-p[0]):g.add(poly)
        for end,name in [([3.6,0,0],'θ₁'),([0,2.05,0],'θ₂'),([0,0,22],'L')]:
            g.add(Line(self.project3([0,0,0]),self.project3(end),color=GRAY,stroke_width=1.4,stroke_opacity=.7),txt(name,21,GRAY,width=1).move_to(self.project3(end)+[.15,.1,0]))
        g.add(txt('z = θ₁² + 4θ₂²  ·  높이축 0.15배 표시',18,GRAY,width=7.5).move_to(self.main+[0,-2 if SHORT else -2.3,0]));self.add(g)
        if current:
            at=self.project3([2,1,8]);g.add(Dot(at,radius=.08,color=BLUE).set_z_index(500),txt('(2, 1),  L = 8',21,BLUE,width=3).move_to(at+[.3,.35,0]).set_z_index(501))
        return g
    def tangent(self):
        points=[]
        for x,y in [[1.3,.3],[2.7,.3],[2.7,1.7],[1.3,1.7]]:points.append(self.project3([x,y,8+4*(x-2)+8*(y-1)]))
        self.add(Polygon(*points,fill_color=BLUE,fill_opacity=.16,stroke_color=BLUE,stroke_width=1.5).set_z_index(501))
        # Lift a parameter displacement to the tangent plane by dL=G·dθ.
        delta=-.06*GRAD;a=self.project3([2,1,8]);b=self.project3([*(THETA+delta),8+GRAD@delta])
        self.add(Arrow(a,b,buff=0,color=GREEN,stroke_width=6,max_tip_length_to_length_ratio=.2).set_z_index(503))
    def recap_pos(self,v):
        return (np.array([-1.8,.25,0]) if SHORT else np.array([-5.7,-1.25,0]))+(.75 if SHORT else .65)*np.r_[v,0]
    def recap_arrow(self,a,b,c):return Arrow(self.recap_pos(a),self.recap_pos(b),buff=0,color=c,stroke_width=5,max_tip_length_to_length_ratio=.13)
    def recap_axes(self):
        self.add(Line(self.recap_pos([-.4,0]),self.recap_pos([5.2,0]),color=GRAY,stroke_width=1),Line(self.recap_pos([0,-1.5]),self.recap_pos([0,5]),color=GRAY,stroke_width=1))
    def tag(self,s):self.add(txt(s,23,GRAY,width=7).move_to(self.main+[0,2.65 if SHORT else 2.12,0]))
    def mini_least_squares(self):
        center=np.array([0,.3,0]) if SHORT else np.array([-4,-1.15,0]);scale=.75 if SHORT else .6
        def pos(v):x,y,z=v;return center+scale*np.array([.8*x-.2*y,.3*x+.3*y+.65*z,0])
        self.add(Polygon(*(pos(v) for v in [[0,0,0],[4,0,0],[4,4,0],[0,4,0]]),fill_color=GREEN,fill_opacity=.13,stroke_color=GREEN,stroke_width=1.5))
        for a,b,c in [([0,0,0],[2,3,4],BLUE),([0,0,0],[2,3,0],ORANGE),([2,3,0],[2,3,4],PURPLE)]:self.add(Arrow(pos(a),pos(b),buff=0,color=c,stroke_width=5,max_tip_length_to_length_ratio=.1))
        self.tag('LEVEL 06  ·  최소제곱');self.info('주어진 공간에서 가장 가까운 결과','잔차는 그 공간과 직교',ORANGE)
    def mini_pca(self):
        angle=35*DEGREES;r=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]);s=np.linspace(-2.8,2.8,16);n=np.array([.3,-.4,.5,-.2,.3,-.4,.2,-.3,.4,-.3,.2,-.5,.3,-.2,.4,-.3]);n-=n.mean();n-=s*(s@n)/(s@s);data=np.column_stack([s,n])@r.T
        self.add(VGroup(*(Dot(self.main+.85*np.r_[p,0],radius=.055,color=BLUE) for p in data)))
        angle_tracker=ValueTracker(0)
        self.add(always_redraw(lambda:Line(self.main-2.7*np.array([np.cos(angle_tracker.get_value()),np.sin(angle_tracker.get_value()),0]),self.main+2.7*np.array([np.cos(angle_tracker.get_value()),np.sin(angle_tracker.get_value()),0]),color=GREEN,stroke_width=3)))
        self.tag('LEVEL 07  ·  PCA');self.info('데이터를 잘 보존하는 방향','재구성 오차 최소 = 투영 분산 최대',GREEN);self.play(angle_tracker.animate.set_value(angle),run_time=1)
    def mini_svd(self):
        left=np.array([-2.4,.3,0]) if SHORT else np.array([-6.1,-1.2,0]);right=np.array([1.8,.3,0]) if SHORT else np.array([-2.7,-1.2,0]);unit=.45
        for origin,v,color in [(left,[2,1],BLUE),(right,[0,6],GREEN),(right,[-1,6],OUT)]:self.add(Arrow(origin,origin+unit*np.r_[v,0],buff=0,color=color,stroke_width=5,max_tip_length_to_length_ratio=.12))
        self.add(Arrow(right+unit*np.array([0,6,0]),right+unit*np.array([-1,6,0]),buff=0,color=PURPLE,stroke_width=4));self.tag('LEVEL 08  ·  SVD');self.info('Vᵀx → ΣVᵀx → UΣVᵀx','(2, 1) → (6, 1) → (−1, 6)',OUT)
    def mini_attention(self):
        nodes=[(0,1.3,'Query',BLUE),(-1.9,0,'Key 1',GREEN),(1.9,0,'Key 2',PURPLE),(0,-1.5,'Value 가중합',OUT)]
        centers={name:self.main+[x,y*(1 if SHORT else .8),0] for x,y,name,c in nodes}
        for a,b in [('Query','Key 1'),('Query','Key 2'),('Key 1','Value 가중합'),('Key 2','Value 가중합')]:self.add(Line(centers[a],centers[b],color=GRAY,stroke_width=2))
        for x,y,name,c in nodes:self.add(RoundedRectangle(width=2,height=.65,corner_radius=.1,color=c,fill_color='#0B1220',fill_opacity=1).move_to(centers[name]),txt(name,22,c,width=1.8).move_to(centers[name]))
        self.tag('LEVEL 09  ·  Attention');self.info('점수 → Softmax → 별도의 Value 결합','(3, 2) → (0.67, 0.33) → (2.68, 0.66)',OUT)
    def concept_ring(self):
        g=VGroup();radius=2.35 if SHORT else 1.7
        for j,(name,color) in enumerate([('정사영',GREEN),('직교기저',CYAN),('최소제곱',ORANGE),('PCA',GREEN),('SVD',BLUE),('Attention',PURPLE),('경사하강',GREEN)]):
            a=TAU*j/7+PI/2;center=self.main+radius*np.array([np.cos(a),np.sin(a),0]);g.add(Line(self.main,center,color=GRAY,stroke_width=1,stroke_opacity=.5),Circle(radius=.4,color=color,stroke_width=1.5).move_to(center),txt(name,17,color,width=1.4).move_to(center+[0,-.62,0]))
            # Small geometric icons rather than a list of titles.
            if j in [0,1]:g.add(Line(center+[-.2,-.15,0],center+[.2,-.15,0],color=color),Line(center+[-.2,-.15,0],center+[.05,.22,0],color=BLUE),DashedLine(center+[.05,.22,0],center+[.05,-.15,0],color=color,dash_length=.035))
            elif j in [2,3]:
                for x,y in [(-.2,-.15),(-.1,.02),(.08,.05),(.2,.17)]:g.add(Dot(center+[x,y,0],radius=.027,color=BLUE))
                g.add(Line(center+[-.23,-.2,0],center+[.23,.2,0],color=color,stroke_width=2))
            elif j==4:g.add(Arrow(center+[-.24,0,0],center+[.24,.12,0],buff=0,color=color,stroke_width=3,max_tip_length_to_length_ratio=.3))
            elif j==5:
                for p in [[0,.2,0],[-.2,-.15,0],[.2,-.15,0]]:g.add(Dot(center+p,radius=.04,color=color))
                g.add(Line(center+[0,.2,0],center+[-.2,-.15,0],color=color),Line(center+[0,.2,0],center+[.2,-.15,0],color=color))
            else:g.add(Ellipse(width=.55,height=.35,color=ORANGE,stroke_width=1).move_to(center),Arrow(center+[.23,.1,0],center,buff=0,color=GREEN,stroke_width=3,max_tip_length_to_length_ratio=.4))
        g.add(Circle(radius=.58,color=INK,fill_color='#0B1220',fill_opacity=1).move_to(self.main),txt('내적',29,INK,width=1.1).move_to(self.main));self.add(g)
    def shot(self):
        i=self.INDEX
        if i==0:
            nodes=[]
            for x,count in [(-2.4,3),(0,4),(2.4,2)]:
                for y in np.linspace(-1.2,1.2,count):nodes.append((x,self.main+np.array([x,y,0])))
            network=VGroup()
            for xa,a in nodes:
                for xb,b in nodes:
                    if abs(xb-xa-2.4)<.01:network.add(Line(a,b,color=GRAY,stroke_width=1,stroke_opacity=.4))
            for _,p in nodes:network.add(Dot(p,radius=.1,color=BLUE))
            network.add(txt('θ₁, θ₂, …, θₙ',25,BLUE,width=6).move_to(self.main+[0,2.1,0]));self.add(network);self.info('파라미터를 어느 방향으로 움직일까?','손실을 줄이는 이동 방향을 찾자',BLUE);self.to(4);self.remove(network);self.contours();self.angle.set_value(25*DEGREES);self.direction();self.info('내적 · Dot Product','이동 방향과 손실 변화의 관계',GREEN)
        elif i==1:
            self.contours(False);self.info('두 개의 파라미터 θ₁, θ₂',color=BLUE);self.to(12);self.info('L(θ₁,θ₂) = θ₁² + 4θ₂²','θ₁ 방향보다 θ₂ 방향의 곡률이 크다',CYAN);self.to(18);self.clear_body();surf=self.surface();self.info('z = L(θ₁,θ₂)','높이가 낮아질수록 손실도 작아진다',CYAN)
        elif i==2:
            surf=self.surface(True);self.info('현재 위치 θ = (2, 1)','L(2,1) = 8',BLUE);self.to(28);self.info('∂L/∂θ₁ = 2θ₁','∂L/∂θ₂ = 8θ₂',ORANGE);self.to(32);self.info('∇L = (2θ₁, 8θ₂)','각 파라미터 방향의 순간 변화율을 모은 벡터',ORANGE);self.to(37);self.info('∇L(2,1) = (4, 8)',color=ORANGE);self.to(40);self.clear_body();self.contours();self.gradient();self.info('왜 기울기가 학습 방향을 결정할까?',color=ORANGE)
        elif i==3:
            self.contours();self.gradient();self.info('∇L · Δθ',color=ORANGE,size=38);self.to(45);self.direction();self.info('Δθ = εu  ·  ‖u‖ = 1','실제 이동은 충분히 작은 ε만큼',GREEN);self.to(49);self.info('ΔL ≈ ∇L · Δθ = ε(∇L · u)','작은 이동에 대한 일차 근사',PURPLE);self.to(54);self.remove(self.content);self.meter();self.below('순간 변화율 · 실제 1단위 이동의 손실차가 아님',GRAY,-1.1,20);self.turn(210*DEGREES,4)
        elif i==4:
            self.contours();self.gradient();self.direction();self.meter();self.below('u = (1, 0)  ·  순간 손실 증가 방향',ORANGE,-1.1);self.to(64);self.clear_body();self.contours();self.gradient();self.direction();self.meter();self.turn(PI,1.5);self.below('u = (−1, 0)  ·  순간 손실 감소 방향',GREEN,-1.1)
        elif i==5:
            self.contours();self.gradient();self.angle.set_value(GA);self.direction(True);self.angle_arc()
            ghosts=VGroup(*(self.arrow(THETA,THETA+np.array([np.cos(a),np.sin(a)]),GREEN,2).set_opacity(.23) for a in np.linspace(0,TAU,12,endpoint=False)));self.add(ghosts);self.info('같은 길이의 방향들 중 최솟값은?',color=GREEN);self.to(74);self.info('∇L · Δθ = ‖∇L‖ ‖Δθ‖ cosφ',color=ORANGE);self.to(78);self.info('기울기 고정  ·  ‖Δθ‖ = ε 고정','단위방향 u만 회전시킨다');self.to(83);self.remove(self.content);self.meter(cosine=True);self.below('DᵤL = ‖∇L‖ cosφ  ·  ‖∇L‖ = √80',GRAY,-1.0,23);self.turn(GA+TAU,4);self.to(87);self.turn(GA+3*PI,2.5);self.to(91);self.remove(ghosts);self.below('u_min = −∇L / ‖∇L‖',GREEN,-1.7,27)
        elif i==6:
            self.surface(True);self.tangent();self.info('음의 기울기 = 가장 빠른 국소 감소','같은 유클리드 이동 길이 · 순간 변화 기준',GREEN);self.to(99);self.info('Gradient Descent · 경사하강법','국소적 성질: 임의의 큰 이동까지 보장하지 않는다',GREEN)
        elif i==7:
            self.contours();self.gradient();self.info('θ_new = θ − η∇L','θ=(2,1)  ·  ∇L=(4,8)',GREEN);self.to(107)
            self.add(Dot(self.pos(THETA),radius=.08,color=BLUE).set_opacity(.4))
            moving=always_redraw(lambda:Dot(self.pos(THETA-self.eta.get_value()*GRAD),radius=.09,color=BLUE).set_z_index(20));path=always_redraw(lambda:self.arrow(THETA,THETA-self.eta.get_value()*GRAD,GREEN).set_z_index(12));self.add(path,moving)
            gauge=always_redraw(lambda:txt(f'L(θ) = {loss(THETA-self.eta.get_value()*GRAD):.2f}',29,PURPLE,width=6).move_to(self.panel+[0,-1.6,0]));self.add(gauge);self.info('η = 0.1','(2,1) − 0.1(4,8) = (1.6,0.2)',GREEN);self.play(self.eta.animate.set_value(.1),run_time=4);self.to(113);self.info('손실 8.00 → 2.72','실제 새 위치에서 손실함수를 다시 계산',PURPLE)
        elif i==8:
            self.contours();self.gradient();small=THETA-.1*GRAD;large=THETA-.4*GRAD
            self.add(self.arrow(THETA,small,GREEN),Dot(self.pos(small),radius=.08,color=GREEN));self.info('음의 기울기는 국소적인 최급강하 방향','η=0.1  →  (1.6,0.2),  L=2.72',GREEN);self.to(123)
            self.play(GrowArrow(self.arrow(THETA,large,PURPLE)),run_time=1);self.add(Dot(self.pos(large),radius=.08,color=PURPLE),txt('(0.4, −2.2)',20,PURPLE,width=2.8).move_to(self.pos(large)+[.6,-.2,0]));self.info('η = 0.4  →  L = 19.52','같은 시작점 · 같은 방향 · 너무 큰 이동',PURPLE);self.below('2.72 < 8  < 19.52',PURPLE,-1.6,28)
        elif i==9:
            self.recap_axes();self.add(self.recap_arrow([0,0],[3,4],BLUE),self.recap_arrow([0,0],[1,0],GREEN));self.info('다시, 하나의 내적에서',color=INK);self.to(129);self.tag('LEVEL 01  ·  방향의 성분 측정');self.add(self.recap_arrow([0,0],[3,0],ORANGE),DashedLine(self.recap_pos([3,4]),self.recap_pos([3,0]),color=GRAY,stroke_width=2));self.info('(3,4) · (1,0) = 3','단위방향을 기준으로 성분을 측정',ORANGE)
        elif i==10:
            self.recap_axes();self.tag('LEVEL 02  ·  정사영');self.add(self.recap_arrow([0,0],[4,2],BLUE),self.recap_arrow([0,0],[3,3],ORANGE),DashedLine(self.recap_pos([3,3]),self.recap_pos([4,2]),color=PURPLE));self.info('측정한 성분을 벡터로 추출',color=ORANGE);self.to(134)
            self.clear_body();self.recap_axes();self.tag('LEVEL 03  ·  잔차');self.add(self.recap_arrow([0,0],[4,2],BLUE),self.recap_arrow([0,0],[3,3],ORANGE),self.recap_arrow([0,0],[1,-1],PURPLE));self.info('(4,2) − (3,3) = (1,−1)','원하는 방향의 성분 제거',PURPLE);self.to(135)
            self.clear_body();self.recap_axes();self.tag('LEVEL 04  ·  직교정규기저');self.add(self.recap_arrow([0,0],[.707,.707],GREEN),self.recap_arrow([0,0],[-.707,.707],PURPLE),self.recap_arrow([0,0],[5,1],BLUE));self.info('같은 벡터 · 다른 기저의 좌표',color=GREEN);self.to(136)
            self.clear_body();self.recap_axes();self.tag('LEVEL 05  ·  Gram–Schmidt');self.add(self.recap_arrow([0,0],[1,1],GREEN),self.recap_arrow([0,0],[2,0],BLUE),self.recap_arrow([0,0],[1,-1],PURPLE));self.info('정사영 제거 → 직교기저 구성',color=PURPLE);self.to(137)
            self.clear_body();self.mini_least_squares();self.to(139.5);self.clear_body();self.mini_pca()
        elif i==11:
            self.mini_svd();self.to(145);self.clear_body();self.mini_attention();self.to(148);self.clear_body();self.contours();self.gradient();self.angle.set_value(DESCENT_ANGLE);self.direction();self.info('∇L · Δθ','LEVEL 10  ·  손실을 줄이는 학습 방향',GREEN)
        elif i==12:
            self.concept_ring();self.info('서로 다른 문제를 잇는 공통 원리',color=INK);self.to(158);self.clear_body();self.recap_axes();self.add(self.recap_arrow([0,0],[3,2],BLUE),self.recap_arrow([0,0],[2,0],GREEN));self.info('a · b = ‖a‖ ‖b‖ cosθ','한 벡터가 다른 방향에 얼마나 반응하는가',INK);self.to(162);self.clear_body()
            self.add(txt('DOT PRODUCT SERIES · LEVEL 01–10',21,GRAY,width=7.8 if SHORT else 6.7).move_to(self.main+[0,1.5,0]),txt('내적 하나로\n어디까지 이해할 수 있을까?',35,INK,width=7.8 if SHORT else 6.7).move_to(self.main+[0,.2,0]),txt('방향 → 공간 → 데이터 → 신경망',23,CYAN,width=7.8 if SHORT else 6.7).move_to(self.main+[0,-1.4,0]));self.info('공간의 구조 · 데이터의 표현','신경망의 계산과 최적화까지',OUT)
