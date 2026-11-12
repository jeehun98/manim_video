"""Shared curve geometry; physically distinct wave and heat time laws."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,label,text,p,L

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#10141C'
INK,BLUE,GREEN,PURPLE,HEAT,GOLD,MUTED='#F5F5F5','#4EA8DE','#45C7A4','#B38AF5','#F1A65B','#F3D06B','#8995AA'
COLORS=[BLUE,GREEN,PURPLE]
ALPHA=.18
COEFF=np.array([1.,.15,-.2])
XS=np.linspace(0,np.pi,145)

def modes(x,t=0):
    x=np.asarray(x)
    return np.array([a*np.exp(-ALPHA*n*n*t)*np.sin(n*x) for n,a in enumerate(COEFF,1)])
def heat(x,t=0):return np.sum(modes(x,t),axis=0)
def eq(s,x=0,y=0,size=38,color=INK,width=7.3):
    o=MathTex(s,font_size=size*1.35,color=color)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to(p(x,y))
def card(s,x=0,y=0,w=6,h=1,color=BLUE,size=28):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.14,stroke_color=color,fill_color=color,fill_opacity=.06),label(s,size=size,color=color,width=w-.3)).move_to(p(x,y))
def setcurve(m,values,y=0,amp=1,width=6.7,x=0):
    coords=np.column_stack((x+(XS/np.pi-.5)*width,y+amp*np.asarray(values),np.zeros(len(XS))))
    m.set_points_as_corners(coords)
    return m
def curve(values,y=0,amp=1,color=INK,width=6.7,x=0):
    return setcurve(VMobject(stroke_color=color,stroke_width=3),values,y,amp,width,x)
def baseline(y,width=6.7,x=0):return Line(p(x-width/2,y),p(x+width/2,y),color=MUTED,stroke_width=1,stroke_opacity=.55)
def endpoints(y):return VGroup(*[Dot(p(x,y),radius=.07,color=MUTED) for x in [-3.35,3.35]])
def rod(y=-1.8):
    cells=VGroup(*[Rectangle(width=6.7/56+.006,height=.45,stroke_width=0,fill_opacity=1).move_to(p(-3.35+(i+.5)*6.7/56,y)) for i in range(56)])
    return paintrod(cells,0)
def paintrod(cells,t):
    vals=heat((np.arange(56)+.5)/56*np.pi,t)
    for cell,v in zip(cells,vals):cell.set_fill(interpolate_color(ManimColor('#183146'),ManimColor('#F1A65B'),np.clip(v/1.25,0,1)))
    return cells

class FourierScene(QCSScene):
    data=DATA
    def replace(self,old,new):return Scene.replace(self,old,new)
    def setup(self):
        super().setup();self.remove(self.mobjects[0])
        self.add(text('수학의 기본 요소  /  후보 01',y=L.brand_y,size=18,color=MUTED))
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
        c=curve(heat(XS),y=1.3,amp=1.3);self.play(Create(c),run_time=1)
        self.show(label('복잡한 형태',y=3.2,size=30))
        self.to(4)
        parts=VGroup(*[curve(np.sin(n*XS),y=-.7-i*1.0,amp=.34,color=COLORS[i]) for i,n in enumerate([1,2,3])])
        self.play(LaggedStart(*[TransformFromCopy(c,o) for o in parts],lag_ratio=.2),run_time=1.5)
        self.note('Sine & Cosine  /  사인과 코사인',GOLD)
    def s02(self):
        clock=ValueTracker(0)
        base=baseline(.9);c=curve(np.sin(XS),y=.9,amp=1.25,color=BLUE)
        self.show(label('18세기 · 다니엘 베르누이',y=3.7,size=26,color=MUTED),base,endpoints(.9),c)
        c.add_updater(lambda m:setcurve(m,np.sin(XS)*np.cos(clock.get_value()),y=.9,amp=1.25))
        self.play(clock.animate.set_value(2*PI),run_time=3,rate_func=linear)
        self.to(12);c.clear_updaters()
        c.add_updater(lambda m:setcurve(m,sum(a*np.sin(n*XS)*np.cos(n*clock.get_value()) for n,a in enumerate(COEFF,1)),y=.9,amp=1.25))
        self.play(clock.animate.set_value(4*PI),run_time=3.5,rate_func=linear)
        self.to(16)
        self.show(eq(r'y(x,t)=\sum_n A_n\sin(k_nx)\cos(\omega_nt)',y=-1.7,size=31),label('기본 진동들의 합',y=-2.8,size=29,color=GOLD))
        self.play(clock.animate.set_value(6*PI),run_time=4.5,rate_func=linear);c.clear_updaters()
        self.note('양 끝이 고정된 줄 · 동일한 시간으로 진동')
    def s03(self):
        a=ValueTracker(0);b=ValueTracker(0)
        total=curve(np.sin(XS),y=2,amp=1.0,color=INK)
        total.add_updater(lambda m:setcurve(m,np.sin(XS)+a.get_value()*np.sin(2*XS)+b.get_value()*np.sin(3*XS),y=2,amp=1.0))
        self.show(baseline(2),total)
        parts=VGroup(*[curve(v,y=.3-i*1.05,amp=.6,color=COLORS[i]) for i,v in enumerate(modes(XS))])
        self.show(parts[0]);self.show(parts[1]);self.play(a.animate.set_value(COEFF[1]),run_time=.7)
        self.show(parts[2]);self.play(b.animate.set_value(COEFF[2]),run_time=.7)
        self.to(26)
        x0=np.pi*.35;px=(x0/np.pi-.5)*6.7
        cursor=DashedLine(p(px,-2.3),p(px,3.4),color=GOLD,stroke_width=1)
        self.show(cursor)
        vals=modes(x0)
        self.show(VGroup(*[Dot(p(px,.3-i*1.05+.6*v),radius=.065,color=COLORS[i]) for i,v in enumerate(vals)]),Dot(p(px,2+sum(vals)),radius=.085,color=GOLD))
        self.note('같은 위치 x에서 높이를 더한다',GOLD)
        self.to(31);total.clear_updaters()
        self.play(FadeOut(cursor),run_time=.4)
        self.note('실제 진동 여부보다, 함수들의 합이라는 표현',GOLD)
    def s04(self):
        self.show(label('19세기 초 · 조제프 푸리에',y=3.5,size=28,color=MUTED))
        r=rod(y=.3);self.show(r)
        self.to(42);self.show(label('물체 내부의 열전달',y=2,size=37,color=HEAT))
        self.to(45)
        t=ValueTracker(0);r.add_updater(lambda m:paintrod(m,t.get_value()))
        graph=curve(heat(XS),y=-2,amp=1.4,color=HEAT);graph.add_updater(lambda m:setcurve(m,heat(XS,t.get_value()),y=-2,amp=1.4))
        self.show(baseline(-2),graph,label('위치마다 다른 온도',y=-3.2,size=28,color=HEAT))
        self.play(t.animate.set_value(2),run_time=4.5,rate_func=linear)
        graph.clear_updaters();r.clear_updaters();self.note('양 끝 온도는 기준 온도로 고정')
    def s05(self):
        c=curve(heat(XS),y=.2,amp=1.45,color=BLUE)
        axis=VGroup(baseline(.2),Arrow(p(-3.35,-.6),p(-3.35,2.5),buff=0,color=MUTED,stroke_width=1.3))
        ylabel=label('줄의 변위',y=3.1,size=31,color=BLUE)
        self.show(c,axis,ylabel,label('위치 x',x=2.65,y=-.4,size=24,color=MUTED))
        self.to(55)
        self.play(Transform(ylabel,label('온도 편차',y=3.1,size=31,color=HEAT)),c.animate.set_color(HEAT),run_time=1.2)
        self.show(eq(r'u=T-T_{\rm ref}=f(x)',y=-1.3,size=36,color=HEAT))
        self.to(60)
        parts=VGroup(*[curve(v,y=-2.1-i*.65,amp=.42,color=COLORS[i],width=5.9) for i,v in enumerate(modes(XS))])
        self.play(LaggedStart(*[TransformFromCopy(c,m) for m in parts],lag_ratio=.2),run_time=1.5)
        self.to(66);self.note('공간의 사인파 ≠ 시간에 따른 진동',GOLD)
        self.to(69)
        self.play(Circumscribe(ylabel,color=GOLD),run_time=.8)
        self.note('예시: 양끝 온도 편차 0 · 사인 모드로 전개')
    def s06(self):
        self.show(label('가운데가 뜨겁고, 양끝은 차갑다면',y=3.6,size=29,color=HEAT))
        t=ValueTracker(0);r=rod(y=-.9);c=curve(heat(XS),y=.3,amp=1.4,color=HEAT)
        self.show(baseline(.3),c,r)
        self.to(78)
        r.add_updater(lambda m:paintrod(m,t.get_value()));c.add_updater(lambda m:setcurve(m,heat(XS,t.get_value()),y=.3,amp=1.4))
        self.show(Arrow(p(-.2,-1.8),p(-2.3,-1.8),color=HEAT),Arrow(p(.2,-1.8),p(2.3,-1.8),color=HEAT))
        self.play(t.animate.set_value(2.6),run_time=3.5,rate_func=linear)
        c.clear_updaters();r.clear_updaters();self.note('열이 주변으로 퍼지며 온도 차이가 줄어든다',HEAT)
    def s07(self):
        for x,sign,c,word in [(-1.85,-1,HEAT,'봉우리 → 감소'),(1.85,1,BLUE,'골짜기 → 증가')]:
            v=(XS/np.pi-.5)**2
            shape=curve(sign*v,y=2.4,amp=2.5,width=2.8,x=x,color=c)
            # A peak is -x², a valley is +x².
            self.show(shape,label(word,x=x,y=1.2,size=25,color=c,width=3.4))
            self.show(Arrow(p(x,2.4),p(x,2.4+sign*.6),color=c,buff=.05))
        equation=eq(r'\frac{\partial u}{\partial t}=\alpha\frac{\partial^2u}{\partial x^2}',y=-.35,size=47,color=GOLD)
        self.show(equation,label('시간 변화  ←  공간적인 휘어짐',y=-1.7,size=28,color=HEAT))
        self.note('u = T − Tref · α는 열확산계수')
        self.to(90)
        self.play(equation.animate.scale(.7).move_to(p(0,-2.7)),run_time=.8)
        self.show(label('두 번 미분해도\n단순하게 남는 함수는?',y=-.1,size=34,color=GOLD))
    def s08(self):
        c=curve(np.sin(XS),y=.2,amp=1.15,color=BLUE)
        f=eq(r'\sin x',y=2.6,size=54,color=BLUE)
        self.show(baseline(.2),c,f)
        self.to(99)
        cosine=eq(r'\cos x',y=2.6,size=54,color=GREEN)
        self.play(Transform(c,curve(np.cos(XS),y=.2,amp=1.15,color=GREEN)),TransformMatchingTex(f,cosine),run_time=.9)
        self.play(Transform(c,curve(-np.sin(XS),y=.2,amp=1.15,color=PURPLE)),TransformMatchingTex(cosine,eq(r'-\sin x',y=2.6,size=54,color=PURPLE)),run_time=.9)
        self.show(eq(r'\frac{d^2}{dx^2}\sin(kx)=-k^2\sin(kx)',y=-2,size=36,color=GOLD))
        self.show(label('k=1 → −1     k=2 → −4     k=3 → −9',y=-3.1,size=27,color=GOLD))
        self.note('같은 주파수 유지 · 코사인에도 동일한 성질')
    def s09(self):
        self.show(eq(r'u(x,t)=A(t)\sin x',y=3.5,size=42,color=HEAT))
        self.show(label('초기 모양',x=-2.3,y=2.4,size=23,color=MUTED))
        initial=DashedVMobject(curve(np.sin(XS),y=.6,amp=1.5,color=MUTED),num_dashes=45)
        c=curve(np.sin(XS),y=.6,amp=1.5,color=HEAT);t=ValueTracker(0)
        self.show(baseline(.6),initial,c,endpoints(.6))
        c.add_updater(lambda m:setcurve(m,np.exp(-ALPHA*t.get_value())*np.sin(XS),y=.6,amp=1.5))
        number=DecimalNumber(100,num_decimal_places=0,unit=r'\%',font_size=42,color=HEAT).move_to(p(0,-1.8))
        number.add_updater(lambda m:m.set_value(100*np.exp(-ALPHA*t.get_value())))
        self.show(label('진폭',y=-.9,size=27,color=HEAT),number)
        self.play(t.animate.set_value(2.4),run_time=4.4,rate_func=linear)
        self.to(111);self.show(eq(r'A(t)=A(0)e^{-\alpha t}',y=-3,size=34,color=GOLD))
        self.play(t.animate.set_value(5.5),run_time=4,rate_func=linear)
        c.clear_updaters();number.clear_updaters();self.note('L=π · 양 끝 온도 편차 0 · 내부 열원 없음')
    def s10(self):
        t=ValueTracker(0)
        baselines=[3.3,1.9,.5]
        graphs=[];numbers=[]
        for i,y in enumerate(baselines):
            n=i+1
            self.add(baseline(y,width=5.3,x=-.5))
            g=curve(modes(XS)[i]/abs(COEFF[i]),y=y,amp=.52,color=COLORS[i],width=5.3,x=-.5)
            g.add_updater(lambda m,i=i,y=y:setcurve(m,modes(XS,t.get_value())[i]/abs(COEFF[i]),y=y,amp=.52,width=5.3,x=-.5))
            self.show(g,label(f'n={n}',x=-3.45,y=y,size=21,color=COLORS[i],width=.8))
            number=DecimalNumber(100,num_decimal_places=0,font_size=26,color=COLORS[i]).move_to(p(3.05,y))
            number.add_updater(lambda m,n=n:m.set_value(100*np.exp(-ALPHA*n*n*t.get_value())))
            self.add(number);graphs.append(g);numbers.append(number)
        combined=curve(heat(XS),y=-2,amp=.9,color=INK)
        combined.add_updater(lambda m:setcurve(m,heat(XS,t.get_value()),y=-2,amp=.9))
        self.show(label('실제 계수로 합성',x=-1.8,y=-.7,size=24),baseline(-2),combined)
        self.note('위: 초기 진폭=1로 정규화 · 숫자: 남은 비율(%)')
        self.to(122)
        self.play(t.animate.set_value(1.6),run_time=5,rate_func=linear)
        self.to(128)
        self.play(t.animate.set_value(4.2),run_time=5,rate_func=linear)
        for g in graphs+[combined]+numbers:g.clear_updaters()
        self.note('감쇠율 αn²: 1차보다 2차는 4배, 3차는 9배',GOLD)
    def s11(self):
        self.show(eq(r'u(x,t)=\sum_{n=1}^{3}A_n(t)\sin(nx)',y=3,size=37,color=INK))
        self.show(curve(heat(XS),y=1,amp=.9,color=HEAT))
        self.to(138)
        boxes=VGroup(*[card(s,x=x,y=-.5,w=2.2,h=1.15,color=c,size=23) for x,s,c in [(-2.5,'복잡한 함수',HEAT),(0,'성분별 진폭',GREEN),(2.5,'쉬운 계산',GOLD)]])
        self.show(boxes);self.show(eq(r'A_n(t)=A_n(0)e^{-\alpha n^2t}',y=-2.3,size=38,color=GOLD))
        self.note('그림은 3성분 예시 · 일반 급수는 무한합')
    def s12(self):
        boxes=VGroup(*[card(s,x=x,y=y,w=3.1,h=1.1,color=c,size=27) for s,x,y,c in [('소리 · 빛',-1.8,2.6,BLUE),('전기 신호',1.8,2.6,GREEN),('이미지',-1.8,.9,PURPLE),('주파수 분석',1.8,.9,HEAT)]])
        self.show(boxes)
        self.to(150);self.clear_body()
        x=card('좌표 x',y=3.4,w=3,color=BLUE)
        feat=card('sin(b₁x), cos(b₁x), …',y=1.2,w=6.5,color=GREEN,size=30)
        mlp=card('작은 신경망 · MLP',y=-1.1,w=5.2,color=PURPLE,size=29)
        self.show(x,feat,mlp)
        self.play(GrowArrow(Arrow(x.get_bottom(),feat.get_top(),buff=.2,color=GREEN)),GrowArrow(Arrow(feat.get_bottom(),mlp.get_top(),buff=.2,color=PURPLE)),run_time=1)
        self.show(label('Fourier Features',y=-2.5,size=31,color=GOLD));self.note('일부 좌표 기반 신경망의 입력 표현')
    def s13(self):
        self.show(label('자연현상의 최소 단위?',y=3.2,size=39,color=GOLD),curve(heat(XS),y=.8,amp=1.1))
        self.to(161)
        self.show(label('물리적 최소 단위가 아니라',y=-.6,size=29,color=MUTED),card('함수를 구성하는 수학적 기저',y=-2,w=7.1,h=1.2,color=GOLD,size=30))
        self.note('기저는 유일하지 않다 · 함수공간과 경계조건에 따라 선택')
        self.to(169);self.clear_body()
        for i,n in enumerate([1,2,3]):self.show(curve(np.sin(n*XS),y=2.6-i*1.2,amp=.35,color=COLORS[i]),run_time=.35)
        self.show(label('서로 다른 현상\n같은 수학적 기본 성분',y=-1.6,size=37,color=GOLD))
        self.note('기저는 유일하지 않다 · 함수공간과 경계조건에 따라 선택')
        self.to(173.5)
