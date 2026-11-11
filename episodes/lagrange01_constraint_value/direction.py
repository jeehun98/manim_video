"""One rectangle problem: shape, contours, normal vectors, value sensitivity."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,label,text,p,L

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#101724'
INK,BLUE,ORANGE,GOLD,PURPLE,MUTED,RED='#F3F5FA','#67B7E8','#E9A15B','#F1CE78','#B99AF4','#8D9BB3','#ED7A83'

def eq(s,x=0,y=0,size=39,color=INK,width=7.5):
    o=MathTex(s,font_size=size*1.35,color=color)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to(p(x,y))
def cartesian():
    a=Axes(x_range=[0,11,1],y_range=[0,11,1],x_length=6.6,y_length=6.6,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to(p(0,.55))
    labels=VGroup(label('가로 x',x=2.65,y=-3.2,size=22,color=MUTED),label('세로 y',x=-2.8,y=4.2,size=22,color=MUTED))
    for k in [2,5,10]:
        labels.add(label(str(k),size=17,color=MUTED).move_to(a.c2p(k,0)+DOWN*.18),label(str(k),size=17,color=MUTED).move_to(a.c2p(0,k)+LEFT*.19))
    return a,labels
def level(a,c,color=BLUE):
    xs=np.unique(np.r_[np.linspace(max(c/11,.05),11,161),5.])
    xs=xs[(xs>=c/11)&(xs<=11)]
    return VMobject(color=color,stroke_width=2.6).set_points_as_corners([a.c2p(x,c/x) for x in xs])
def constraint(a,P=20):return Line(a.c2p(0,P/2),a.c2p(P/2,0),color=ORANGE,stroke_width=3)
def rectangle(x,y,center=(0,.7),color=BLUE):
    return Rectangle(width=.5*x,height=.5*y,color=color,fill_color=BLUE,fill_opacity=.12,stroke_width=3).move_to(p(*center))
def value_plot(y=.4):
    a=Axes(x_range=[16,24,2],y_range=[16,36,5],x_length=6.6,y_length=3.5,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to(p(0,y))
    c=a.plot(lambda P:P*P/16,x_range=[16,24,.05],color=BLUE,stroke_width=3)
    labs=VGroup(label('둘레 P',x=2.6,y=y-2.15,size=23,color=ORANGE),label('최대 넓이',x=-2.4,y=y+2.12,size=23,color=BLUE))
    return a,c,labs

class LagrangeScene(QCSScene):
    data=DATA
    def replace(self,old,new):return Scene.replace(self,old,new)
    def setup(self):
        super().setup();self.remove(self.mobjects[0]);self.add(text('수학적 구조  /  라그랑주 승수법',y=L.brand_y,size=18,color=MUTED))
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
    def s01(self):
        a,c,labs=value_plot(.6);dot=Dot(a.c2p(20,25),radius=.09,color=GOLD)
        self.show(a,c,labs,dot,label('최적값',x=-.8,y=1.7,size=27,color=GOLD))
        self.to(3);new=Dot(a.c2p(21,21**2/16),radius=.09,color=GOLD)
        self.play(TransformFromCopy(dot,new),run_time=1)
        self.play(Create(DashedLine(dot.get_center(),new.get_center(),color=PURPLE)),run_time=.8)
        self.to(7);self.show(eq(r'\lambda\;=?',y=-2.8,size=61,color=PURPLE));self.note('제약조건의 변화 → 최적값의 변화')
    def s02(self):
        x=ValueTracker(2);r=rectangle(2,8)
        r.add_updater(lambda m:m.become(rectangle(x.get_value(),10-x.get_value())))
        xl=label('가로 x',size=26,color=BLUE);yl=label('세로 y',size=26,color=BLUE)
        xl.add_updater(lambda m:m.next_to(r,DOWN,buff=.2));yl.add_updater(lambda m:m.next_to(r,LEFT,buff=.2))
        self.show(r,xl,yl,eq('P=20',y=3.6,color=ORANGE))
        self.to(17);self.play(x.animate.set_value(4),run_time=2)
        self.play(x.animate.set_value(3),run_time=1.4)
        self.to(22);self.show(eq('A=xy',y=-2.7,size=48,color=BLUE))
        r.clear_updaters();xl.clear_updaters();yl.clear_updaters();self.note('둘레는 같아도 넓이는 달라진다')
    def s03(self):
        x=ValueTracker(4);y=ValueTracker(6);r=rectangle(4,6,color=ORANGE)
        r.add_updater(lambda m:m.become(rectangle(x.get_value(),y.get_value(),color=ORANGE if abs(2*x.get_value()+2*y.get_value()-20)<1e-6 else RED)))
        per=DecimalNumber(20,num_decimal_places=1,font_size=43,color=ORANGE).move_to(p(1,-2))
        per.add_updater(lambda m:m.set_value(2*x.get_value()+2*y.get_value()))
        self.show(r,eq('2x+2y=',x=-1.6,y=-2,size=36,color=ORANGE),per,eq('f(x,y)=xy',y=3.6,size=38,color=BLUE))
        self.to(31);self.play(x.animate.set_value(6),run_time=1.2)
        warning=label('둘레 20을 벗어남',y=-3.1,size=28,color=RED);self.show(warning,run_time=.4)
        self.play(y.animate.set_value(4),run_time=1.2)
        self.play(Transform(warning,label('조건 안에서만 움직인다',y=-3.1,size=28,color=ORANGE)),run_time=.6)
        r.clear_updaters();per.clear_updaters()
    def s04(self):
        a,labs=cartesian();self.show(a,labs)
        marker=Dot(a.c2p(6,4),radius=.075,color=GOLD);self.show(marker)
        self.to(40);self.play(marker.animate.move_to(a.c2p(2,8)),run_time=.5)
        path=a.plot(lambda x:16/x,x_range=[2,4,.02],color=BLUE)
        self.play(Create(path),MoveAlongPath(marker,path),run_time=1.5)
        badge=eq('xy=16',y=4.4,size=31,color=BLUE);self.show(badge,run_time=.4)
        self.to(44)
        curves=VGroup(*[level(a,v).set_stroke(opacity=.5 if v!=16 else 1) for v in [9,16,25,36]])
        self.play(FadeOut(path),FadeOut(marker),FadeOut(badge),LaggedStart(*[Create(c) for c in curves],lag_ratio=.18),run_time=1.5)
        tags=VGroup(*[eq(str(v),size=24,color=BLUE).move_to(a.c2p(9.3,v/9.3)+RIGHT*.22) for v in [9,16,25,36]])
        self.show(tags)
        self.to(50);line=constraint(a);self.play(Create(line),run_time=1)
        self.show(eq('2x+2y=20',y=4.4,size=32,color=ORANGE))
        self.to(54);d=Dot(a.c2p(2,8),radius=.085,color=GOLD);self.show(d)
        self.play(d.animate.move_to(a.c2p(8,2)),run_time=1.6);self.note('x>0, y>0 · 가로와 세로는 이 직선 위에서 선택')
    def s05(self):
        a,labs=cartesian();line=constraint(a);x=ValueTracker(2)
        c=level(a,16);d=Dot(a.c2p(2,8),radius=.09,color=GOLD)
        c.add_updater(lambda m:m.become(level(a,x.get_value()*(10-x.get_value()))))
        d.add_updater(lambda m:m.move_to(a.c2p(x.get_value(),10-x.get_value())))
        val=DecimalNumber(16,num_decimal_places=1,font_size=35,color=GOLD).move_to(p(1.5,4.4))
        val.add_updater(lambda m:m.set_value(x.get_value()*(10-x.get_value())))
        self.show(a,labs,line,c,d,eq('A=',x=.1,y=4.4,size=31,color=GOLD),val)
        self.play(x.animate.set_value(5),run_time=2)
        self.play(x.animate.set_value(7),run_time=.8)
        self.play(x.animate.set_value(5),run_time=.8)
        self.to(65);self.play(Circumscribe(d,color=GOLD),run_time=.7)
        c.clear_updaters();d.clear_updaters();val.clear_updaters()
        self.note('xy=25와 2x+2y=20은 (5,5)에서 접한다',GOLD)
    def s06(self):
        a,labs=cartesian();o=a.c2p(5,5)
        self.show(a,labs,level(a,25),constraint(a),Dot(o,radius=.085,color=GOLD))
        self.to(71)
        tangent=DashedLine(a.c2p(3.5,6.5),a.c2p(6.5,3.5),color=INK,stroke_width=2)
        gf=Arrow(o,a.c2p(10,10),buff=0,color=BLUE,stroke_width=6)
        gg=Arrow(o,a.c2p(7,7),buff=0,color=ORANGE,stroke_width=4)
        self.play(Create(tangent),GrowArrow(gf),GrowArrow(gg),run_time=1)
        self.show(eq(r'\nabla f',x=2.65,y=3.6,size=30,color=BLUE),eq(r'\nabla g',x=1.8,y=1.3,size=30,color=ORANGE))
        self.to(75);self.note('기울기는 등고선에 수직 · 값이 가장 빨리 증가하는 방향',BLUE)
        self.to(79)
        self.show(eq(r'\nabla f\cdot(1,-1)=0',y=4.5,size=30,color=GOLD))
        self.note('접선 방향 (1,−1)으로는 1차 증가가 없다')
        self.to(86);self.note('매끄러운 내부 최적점 · ∇g ≠ 0',GOLD)
    def s07(self):
        a,labs=cartesian();o=a.c2p(5,5)
        self.show(a,labs,level(a,25).set_stroke(opacity=.4),constraint(a).set_stroke(opacity=.4),Dot(o,color=GOLD))
        self.show(eq(r'\nabla f=\lambda\nabla g',y=4.5,size=37,color=INK))
        self.to(92);self.note('고정된 ∇g에 스칼라 λ를 곱한다',PURPLE)
        self.to(96);self.show(eq('(5,5)',x=-1.2,y=-.2,size=28,color=GOLD))
        self.to(101)
        gf=Arrow(o,a.c2p(10,10),buff=0,color=BLUE,stroke_width=9,stroke_opacity=.4)
        gg=Arrow(o,a.c2p(7,7),buff=0,color=ORANGE,stroke_width=9,stroke_opacity=.5)
        self.show(gf,gg,eq(r'\nabla f=(5,5)',x=1.9,y=3.8,size=26,color=BLUE),eq(r'\nabla g=(2,2)',x=2.3,y=1.0,size=26,color=ORANGE))
        self.to(106);lam=ValueTracker(1)
        scaled=Arrow(o,a.c2p(7,7),buff=0,color=PURPLE,stroke_width=3)
        scaled.add_updater(lambda m:m.become(Arrow(o,a.c2p(5+2*lam.get_value(),5+2*lam.get_value()),buff=0,color=PURPLE,stroke_width=3)))
        self.add(scaled);self.play(lam.animate.set_value(2.5),run_time=2.4);scaled.clear_updaters()
        self.to(110);self.show(eq(r'\lambda=2.5',y=-2,size=50,color=PURPLE));self.note('같은 시작점 · 같은 좌표배율 · 끝점 일치',PURPLE)
    def s08(self):
        per=ValueTracker(20);r=rectangle(5,5,center=(-1.7,.7))
        r.add_updater(lambda m:m.become(rectangle(per.get_value()/4,per.get_value()/4,center=(-1.7,.7))))
        old=DashedVMobject(rectangle(5,5,center=(-1.7,.7),color=MUTED),num_dashes=36)
        self.show(eq(r'\lambda(P=20)=2.5',y=3.8,size=36,color=PURPLE),r)
        self.to(116);self.show(label('둘레 P',x=1.8,y=2.5,size=26,color=ORANGE),label('최대 넓이',x=1.8,y=.5,size=26,color=BLUE))
        pn=DecimalNumber(20,num_decimal_places=1,font_size=40,color=ORANGE).move_to(p(1.8,1.7))
        an=DecimalNumber(25,num_decimal_places=6,font_size=30,color=BLUE).move_to(p(1.8,-.3))
        pn.add_updater(lambda m:m.set_value(per.get_value()));an.add_updater(lambda m:m.set_value(per.get_value()**2/16))
        self.show(pn,an)
        self.to(121);self.show(old,run_time=.3);self.play(per.animate.set_value(20.1),run_time=2.2)
        self.to(124);r.clear_updaters();self.play(r.animate.set_stroke(PURPLE,width=5),run_time=.5)
        self.show(eq(r'A_{\max}\approx25.25',y=-1.6,size=35,color=BLUE))
        self.to(127);self.show(eq(r'\Delta P=0.1,\quad\Delta A=0.250625',y=-2.7,size=30,color=PURPLE))
        r.clear_updaters();pn.clear_updaters();an.clear_updaters();self.note('정사각형 치수는 실제 비율 · 테두리만 강조')
    def s09(self):
        self.show(eq(r'\frac{\Delta A_{\max}}{\Delta P}=2.50625\approx2.5',y=3.8,size=35,color=BLUE))
        self.to(134);self.show(eq(r'\left.\frac{dA_{\max}}{dP}\right|_{P=20}=\lambda=2.5',y=2.1,size=34,color=PURPLE))
        a,c,labs=value_plot(-.75);self.show(a,c,labs)
        o=a.c2p(20,25);self.show(Dot(o,color=GOLD,radius=.08))
        tangent=Line(a.c2p(18,20),a.c2p(24,35),color=PURPLE,stroke_width=3)
        self.to(137);self.play(Create(tangent),run_time=.7)
        self.to(138);self.note('순간 변화율 = λ · 매끄러운 최적해 아래',PURPLE)
    def s10(self):
        self.show(eq(r'A_{\max}(P)=\frac{P^2}{16}',y=4.1,size=40,color=BLUE),eq(r'\lambda(P)=\frac{P}{8}',y=2.8,size=40,color=PURPLE))
        a,c,labs=value_plot(-.4);per=ValueTracker(20)
        d=Dot(a.c2p(20,25),radius=.085,color=GOLD);d.add_updater(lambda m:m.move_to(a.c2p(per.get_value(),per.get_value()**2/16)))
        self.show(a,c,labs,d);self.play(per.animate.set_value(24),run_time=2)
        d.clear_updaters();self.note('P=20 → λ=2.5     P=24 → λ=3',PURPLE)
        self.to(151);self.clear_body()
        self.show(eq(r'\nabla f=\lambda\nabla g',y=2.2,size=48,color=INK),eq(r'\frac{dA_{\max}}{dP}=\lambda',y=.1,size=48,color=PURPLE))
        self.show(label('최적점을 찾고\n제약의 민감도를 읽는다',y=-2.2,size=37,color=GOLD))
        self.note('이 예제: g=2x+2y=P · 매끄러운 최적해')
        self.to(158.5)
