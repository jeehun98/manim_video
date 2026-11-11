"""Exact tangent geometry and a shared tracker for primal/dual point recording."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,label,text,p,L

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#101622'
INK,BLUE,ORANGE,GOLD,PURPLE,MUTED='#F0F3FA','#69BCEB','#E9A35D','#F0CB73','#B79CF0','#8C9BB4'

def eq(s,x=0,y=0,size=37,color=INK,width=7.4):
    o=MathTex(s,font_size=size*1.35,color=color)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to(p(x,y))
def full_axes():
    a=Axes(x_range=[-3,3,1],y_range=[-4.2,4.2,1],x_length=5.4,y_length=7.56,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to(p(0,.3))
    labs=VGroup(label('X',x=3,y=.05,size=22,color=MUTED),label('Y',x=-.3,y=3.95,size=22,color=MUTED))
    for k in [-2,-1,1,2]:labs.add(label(str(k),size=16,color=MUTED).move_to(a.c2p(k,0)+DOWN*.18))
    return a,labs
def pair_axes(y):
    return Axes(x_range=[-4.5,4.5,1],y_range=[-4.5,4.5,1],x_length=6.6,y_length=3.2,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to(p(0,y))
def parabola(a,dual=False,color=None):
    return a.plot((lambda z:z*z/4) if dual else (lambda z:z*z),x_range=[-4 if dual else -2,4 if dual else 2,.025],color=color or (PURPLE if dual else BLUE),stroke_width=3)
def tangent(a,z,dual=False):
    m=z/2 if dual else 2*z;b=-z*z/4 if dual else -z*z
    xmin,xmax=a.x_range[:2];ymin,ymax=a.y_range[:2]
    if abs(m)<1e-10:lo,hi=xmin,xmax
    else:
        low,high=sorted([(ymin-b)/m,(ymax-b)/m]);lo,hi=max(xmin,low),min(xmax,high)
    return Line(a.c2p(lo,m*lo+b),a.c2p(hi,m*hi+b),color=ORANGE,stroke_width=2.5)
def map_values(z,reverse=False):return (z/2,z*z/4) if reverse else (2*z,z*z)

class LegendreScene(QCSScene):
    data=DATA
    def replace(self,old,new):return Scene.replace(self,old,new)
    def setup(self):
        super().setup();self.remove(self.mobjects[0]);self.add(text('수학적 구조  /  르장드르 변환',y=L.brand_y,size=18,color=MUTED))
    def update_mobjects(self,dt):
        super().update_mobjects(dt)
        for o in self.mobjects:
            if o is getattr(self,'caption',None) or o is getattr(self,'caption_panel',None):continue
            if o.width<.001 or o.height<.001:continue
            assert o.get_left()[0]>=-4.38 and o.get_right()[0]<=4.38,('horizontal',self.shot,self.time)
            assert o.get_bottom()[1]>=-4.9 and o.get_top()[1]<=7.9,('vertical',self.shot,self.time)
    def clear_body(self):
        keep=[self.title,self.caption,self.caption_panel]
        obs=[o for o in self.mobjects if all(o is not k for k in keep) and o.get_center()[1]<4.9]
        if obs:self.play(*[FadeOut(o) for o in obs],run_time=.4)
    def moving(self,a,z,reverse=False):
        factor=.25 if reverse else 1
        dot=Dot(a.c2p(z.get_value(),factor*z.get_value()**2),radius=.075,color=GOLD)
        line=tangent(a,z.get_value(),reverse)
        dot.add_updater(lambda m:m.move_to(a.c2p(z.get_value(),factor*z.get_value()**2)))
        line.add_updater(lambda m:m.become(tangent(a,z.get_value(),reverse)))
        return dot,line
    def mapping(self,reverse=False,complete=False):
        upper,lower=pair_axes(2),pair_axes(-1.5);z=ValueTracker(2 if reverse else 1)
        uc=parabola(upper,dual=reverse);lc=parabola(lower,dual=not reverse)
        dot,line=self.moving(upper,z,reverse)
        bd=Dot(upper.c2p(0,-z.get_value()**2*(.25 if reverse else 1)),radius=.065,color=ORANGE)
        bd.add_updater(lambda m:m.move_to(upper.c2p(0,-z.get_value()**2*(.25 if reverse else 1))))
        target=Dot(lower.c2p(*map_values(z.get_value(),reverse)),radius=.075,color=BLUE if reverse else PURPLE)
        target.add_updater(lambda m:m.move_to(lower.c2p(*map_values(z.get_value(),reverse))))
        h1=eq(r'f^*(p)=p^2/4' if reverse else 'f(x)=x^2',x=2.15,y=3.95,size=25,color=PURPLE if reverse else BLUE,width=3.8)
        h2=eq(r'f^{**}(x)' if reverse else '(p,-b)',x=2.15,y=.4,size=25,color=BLUE if reverse else PURPLE,width=3.8)
        labs=VGroup(h1,h2,label('p' if reverse else 'x',x=3.65,y=1.75,size=23,color=MUTED),label('x' if reverse else 'p',x=3.65,y=-1.75,size=23,color=MUTED),label('Y',x=-.3,y=3.4,size=19,color=MUTED),label('−절편',x=-.6,y=-.1,size=18,color=MUTED))
        for axis,y in [(upper,2),(lower,-1.5)]:
            for k in [-4,-2,2,4]:labs.add(label(str(k),size=14,color=MUTED).move_to(axis.c2p(k,0)+DOWN*.16))
        flow=Arrow(p(-3.7,1),p(-3.7,-.5),buff=0,color=MUTED,stroke_width=2)
        objects=[upper,lower,uc,labs,flow,dot,line,bd,target]
        if complete:objects.append(lc)
        self.show(*objects)
        return dict(upper=upper,lower=lower,z=z,dot=dot,line=line,bd=bd,target=target,curve=lc,h2=h2,reverse=reverse)
    def stop_map(self,m):
        for k in ['dot','line','bd','target']:m[k].clear_updaters()

    def s01(self):
        a,labs=full_axes();z=ValueTracker(1);curve=parabola(a)
        d=Dot(a.c2p(1,1),color=GOLD,radius=.08);d.add_updater(lambda m:m.move_to(a.c2p(z.get_value(),z.get_value()**2)))
        guides=VGroup(DashedLine(a.c2p(1,0),a.c2p(1,1),color=GOLD),DashedLine(a.c2p(0,1),a.c2p(1,1),color=GOLD))
        self.show(a,labs,curve,d,guides,eq('f(x)=x^2',y=4.6,size=40,color=BLUE))
        # Changing dash counts during FadeIn changes its animation family; update after entry.
        guides.add_updater(lambda m:m.become(VGroup(DashedLine(a.c2p(z.get_value(),0),a.c2p(z.get_value(),z.get_value()**2),color=GOLD),DashedLine(a.c2p(0,z.get_value()**2),a.c2p(z.get_value(),z.get_value()**2),color=GOLD))))
        self.to(3);self.play(z.animate.set_value(1.6),run_time=3)
        d.clear_updaters();guides.clear_updaters();self.note('입력 x → 그 위치의 높이 f(x)')
    def s02(self):
        a,labs=full_axes();c=parabola(a);t=tangent(a,1);self.show(a,labs,c,Dot(a.c2p(1,1),color=GOLD),t)
        self.note('점의 정보 대신, 접하는 직선의 정보로?')
        self.to(14);self.play(FadeOut(t),run_time=.4);self.show(eq('f(x)=x^2',y=4.6,size=43,color=BLUE))
        self.to(18);self.play(Flash(a.c2p(0,0),color=GOLD),run_time=.7)
        self.to(22);self.show(Dot(a.c2p(1.5,2.25),color=GOLD,radius=.08));self.note('원점이 최솟값 · 양쪽으로 갈수록 높아진다')
    def s03(self):
        a,labs=full_axes();z=ValueTracker(1);d,t=self.moving(a,z)
        self.show(a,labs,parabola(a))
        self.to(29);self.note('접선의 기울기 p',ORANGE)
        self.to(31);self.show(d,t)
        num=DecimalNumber(2,num_decimal_places=1,font_size=40,color=ORANGE).move_to(p(.7,4.6))
        num.add_updater(lambda m:m.set_value(2*z.get_value()));self.show(eq('p=',x=-.7,y=4.6,size=39,color=ORANGE),num)
        self.to(35);self.play(z.animate.set_value(1.6),run_time=2.6)
        self.to(39);self.play(z.animate.set_value(-1.5),run_time=3)
        for o in [d,t,num]:o.clear_updaters()
    def s04(self):
        a,labs=full_axes();z=ValueTracker(1);d,t=self.moving(a,z)
        self.show(a,labs,parabola(a),d,t)
        f=eq("p=f'(x)=2x",y=4.6,size=39,color=ORANGE);self.show(f)
        self.to(45);self.play(z.animate.set_value(2),run_time=2);self.note('p=4이면 접점은 x=2',GOLD)
        self.to(49);self.play(TransformMatchingTex(f,eq('x=p/2',y=4.6,size=43,color=GOLD)),run_time=.8)
        d.clear_updaters();t.clear_updaters();self.note('이 포물선에서는 기울기와 접점이 일대일 대응')
    def s05(self):
        a,labs=full_axes();z=ValueTracker(1);d,t=self.moving(a,z)
        bd=Dot(a.c2p(0,-1),color=ORANGE,radius=.075);bd.add_updater(lambda m:m.move_to(a.c2p(0,-z.get_value()**2)))
        btag=eq('b',size=30,color=ORANGE);btag.add_updater(lambda m:m.next_to(bd,LEFT,buff=.17))
        tri=VMobject(color=ORANGE,stroke_width=2)
        def triangle(m):
            v=z.get_value();m.set_points_as_corners([a.c2p(v,v*v),a.c2p(v+.5,v*v),a.c2p(v+.5,v*v+v)])
        triangle(tri);tri.add_updater(triangle)
        self.show(a,labs,parabola(a),d,t,eq('Y=pX+b',y=4.6,size=43,color=ORANGE))
        self.to(56);self.show(bd,btag,tri);self.note('기울기 p=2x · 절편 b=−x²',ORANGE)
        self.to(60);self.play(z.animate.set_value(1.5),run_time=2);self.note('기울기를 정하면 절편도 결정된다',ORANGE)
        for o in [d,t,bd,btag,tri]:o.clear_updaters()
    def s06(self):
        m=self.mapping();z=m['z']
        snapshot=Dot(m['lower'].c2p(2,1),color=PURPLE,radius=.075)
        self.play(TransformFromCopy(m['bd'],snapshot),run_time=.5)
        for v in [-2,-1,0,1,2]:
            self.play(z.animate.set_value(v),run_time=.45)
            self.add(Dot(m['lower'].c2p(2*v,v*v),radius=.055,color=PURPLE))
        self.note('기울기 p → 가로좌표 · 절편의 음수 −b → 세로좌표')
        self.to(69);self.play(Transform(m['h2'],eq(r'f^*(p)=-b',x=2.15,y=.4,size=27,color=PURPLE,width=3.8)),run_time=.6)
        self.play(Create(m['curve']),run_time=1.2);self.stop_map(m)
    def s07(self):
        m=self.mapping(complete=True)
        formula=eq(r'Y=pX+[f(x)-px]',y=4.65,size=33,color=ORANGE);self.show(formula)
        self.to(76);new=eq(r'f^*(p)=-b=px-f(x)',y=4.65,size=35,color=PURPLE)
        self.play(TransformMatchingTex(formula,new),run_time=.8)
        self.note('여기서는 p=f′(x)인 접점에서 계산한다',GOLD)
        self.to(80);self.note('일반 정의: f*(p)=supₓ{px−f(x)} · 접점에서 최댓값')
        self.stop_map(m)
    def s08(self):
        m=self.mapping(complete=True)
        f=eq('p=2x',y=4.65,size=40,color=ORANGE);self.show(f)
        self.to(85);new=eq('x=p/2',y=4.65,size=40,color=GOLD);self.play(TransformMatchingTex(f,new),run_time=.7)
        self.to(89);result=eq(r'f^*(p)=\frac{p^2}{2}-\frac{p^2}{4}=\frac{p^2}{4}',y=4.65,size=33,color=PURPLE)
        self.play(TransformMatchingTex(new,result),run_time=.9)
        self.to(93);self.play(m['z'].animate.set_value(2),run_time=2);self.play(m['z'].animate.set_value(-1),run_time=2)
        self.note('윗 가로축: 위치 x · 아랫 가로축: 접선의 기울기 p');self.stop_map(m)
    def s09(self):
        m=self.mapping(reverse=True);z=m['z']
        self.to(104)
        for v in [-4,-2,0,2,4]:
            self.play(z.animate.set_value(v),run_time=.4)
            self.add(Dot(m['lower'].c2p(v/2,v*v/4),radius=.055,color=BLUE))
        self.to(108);f=eq(r'x=\frac{df^*}{dp}=\frac p2',y=4.65,size=34,color=GOLD);self.show(f)
        self.to(111)
        self.play(TransformMatchingTex(f,eq(r'f^{**}(x)=xp-\frac{p^2}{4}=x^2',y=4.65,size=33,color=BLUE)),Create(m['curve']),run_time=1.2)
        self.note('보라 접선의 기울기 x=p/2 · 절편의 음수 x²를 기록');self.stop_map(m)
    def s10(self):
        m=self.mapping(complete=True)
        self.show(eq(r'f\;\longrightarrow\;f^*\;\longrightarrow\;f^{**}=f',y=4.65,size=34,color=GOLD))
        self.play(m['z'].animate.set_value(-1.4),run_time=2);self.play(m['z'].animate.set_value(1.2),run_time=2)
        self.to(124);self.note('예제: 매끄럽고 엄격히 볼록한 x²\n일반 복원: 적정(proper)·닫힌 볼록함수',GOLD);self.stop_map(m)
    def s11(self):
        m=self.mapping(complete=True);self.show(eq(r'f(x)\;\longleftrightarrow\;f^*(p)',y=4.65,size=38,color=INK))
        self.note('위치·높이의 정보 ↔ 기울기·절편의 정보',GOLD)
        self.to(137);self.stop_map(m);self.clear_body()
        self.show(label('고전역학 · 속도 → 운동량',y=3.5,size=29,color=BLUE),eq('H(q,p)=pv-L(q,v)',y=2.3,size=36,color=BLUE))
        self.show(label('열역학 · 엔트로피 → 온도',y=.6,size=29,color=ORANGE),eq('F(T,V)=U(S,V)-TS',y=-.6,size=36,color=ORANGE))
        self.show(label('p=∂L/∂v · T=∂U/∂S',y=-2.2,size=25,color=MUTED));self.note('정칙 조건 필요 · 열역학 F는 U의 S-볼록 켤레와 부호가 반대')
    def s12(self):
        axs=[];dots=[];z=ValueTracker(1)
        for i,cx in enumerate([-2,2]):
            a=Axes(x_range=[-4.5,4.5,1],y_range=[0,4.5,1],x_length=3.4,y_length=3,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to(p(cx,1.5))
            self.show(a,parabola(a,dual=bool(i)),eq(r'f(x)=x^2' if i==0 else r'f^*(p)=p^2/4',x=cx,y=3.7,size=29,color=BLUE if i==0 else PURPLE,width=3.5))
            d=Dot(a.c2p(1 if i==0 else 2,1),color=GOLD,radius=.07)
            d.add_updater(lambda mob,a=a,i=i:mob.move_to(a.c2p(z.get_value()*(1 if i==0 else 2),z.get_value()**2)))
            self.add(d);dots.append(d);axs.append(a)
        self.show(DoubleArrow(p(-.35,1.4),p(.35,1.4),buff=0,color=GOLD),label('x',x=-.4,y=-.3,size=23,color=MUTED),label('p',x=3.7,y=-.3,size=23,color=MUTED))
        self.play(z.animate.set_value(-1),run_time=2)
        self.to(151);self.show(label('같은 수학적 구조\n다른 정보의 기준',y=-1.9,size=39,color=GOLD));self.note('점의 정보 (x,f(x)) ↔ 접선의 정보 (p,−b)')
        for d in dots:d.clear_updaters()
        self.to(155.5)
