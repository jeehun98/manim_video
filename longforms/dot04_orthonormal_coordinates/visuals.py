"""Passive coordinate changes: x never moves, orthonormal axes rotate."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';PURPLE='#BB97FF';ORANGE='#FFB45F'
X=np.array([5.,1.]);Q1=np.array([1.,1.])/np.sqrt(2);Q2=np.array([-1.,1.])/np.sqrt(2)
P1=np.array([3.,3.]);P2=np.array([2.,-2.])
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def colored(parts,size=32,width=7.8):
    g=VGroup(*(txt(s,size,c,width) for s,c in parts)).arrange(RIGHT,buff=.12)
    if g.width>width:g.scale_to_fit_width(width)
    return g
class BasisBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.meta['start'];self.origin=np.array([-1.75,1.,0]) if SHORT else np.array([-5.55,-.45,0]);self.unit=.9 if SHORT else .85
        self.panel=np.array([0,-2.45,0]) if SHORT else np.array([3.65,.55,0])
        self.add(txt('DOT PRO   /   LEVEL 04',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        for x,s,c in zip([-2.6,0,2.6] if SHORT else [-5.4,-2.5,.4],['x 고정 벡터','q₁ 첫 기준','q₂ 둘째 기준'],[BLUE,GREEN,PURPLE]):
            self.add(txt(s,18,c,width=2.5).move_to([x,5.15 if SHORT else -3.03,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def pt(self,v):return self.origin+self.unit*np.array([v[0],v[1],0.])
    def arr(self,v,col,origin=None,width=6):
        origin=np.zeros(2) if origin is None else np.array(origin)
        return Arrow(self.pt(origin),self.pt(origin+v),buff=0,color=col,stroke_width=width,max_tip_length_to_length_ratio=.14)
    def graph(self):
        grid=VGroup()
        for k in range(-2,6):
            grid.add(Line(self.pt([k,-2.4]),self.pt([k,3.5]),color=GRAY,stroke_width=1,stroke_opacity=.075))
        for k in range(-2,4):
            grid.add(Line(self.pt([-2.3,k]),self.pt([5.65,k]),color=GRAY,stroke_width=1,stroke_opacity=.075))
        grid.add(Line(self.pt([-2.3,0]),self.pt([5.65,0]),color=GRAY,stroke_width=1.5,stroke_opacity=.3),Line(self.pt([0,-2.4]),self.pt([0,3.5]),color=GRAY,stroke_width=1.5,stroke_opacity=.3))
        self.add(grid,txt('0',16,GRAY).move_to(self.pt([-.22,-.28])))
        self.x=self.arr(X,BLUE,width=6).set_z_index(8)
        self.xname=txt('x',27,BLUE,width=1).move_to(self.pt([5.35,1.35]));self.add(self.x,self.xname)
    def info(self,s,note='',color=INK,size=32):
        line=txt(s,size,color,width=8 if SHORT else 6.65) if isinstance(s,str) else colored(s,size,width=8 if SHORT else 6.65)
        line.move_to(self.panel);group=VGroup(line)
        if note:group.add(txt(note,23,GRAY,width=7.8 if SHORT else 6.5).next_to(line,DOWN,buff=.4))
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=group;self.add(group);return group
    def to(self,t):
        remain=t-self.start-self.time
        if remain<-.04:raise RuntimeError(f'Scene {self.INDEX+1}: clock {self.time} exceeds {t-self.start}')
        if remain>.001:self.wait(remain)
    def emphasize(self,m,color):self.play(Indicate(m,color=color,scale_factor=1),run_time=.8)
    def directions(self):
        t=self.angle.get_value();return np.array([np.cos(t),np.sin(t)]),np.array([-np.sin(t),np.cos(t)])
    def ray_end(self,d):
        limits=[]
        for v,lo,hi in zip(d,[-2.3,-2.4],[5.65,3.5]):
            if abs(v)>1e-8:limits.append((hi if v>0 else lo)/v)
        return min(limits)*d
    def basis(self,theta=PI/4,names=('q₁','q₂')):
        self.angle=ValueTracker(theta)
        self.axis1=always_redraw(lambda:Line(self.pt(self.ray_end(-self.directions()[0])),self.pt(self.ray_end(self.directions()[0])),color=GREEN,stroke_width=2,stroke_opacity=.48))
        self.axis2=always_redraw(lambda:Line(self.pt(self.ray_end(-self.directions()[1])),self.pt(self.ray_end(self.directions()[1])),color=PURPLE,stroke_width=2,stroke_opacity=.48))
        self.q1=always_redraw(lambda:self.arr(self.directions()[0],GREEN,width=7).set_z_index(11))
        self.q2=always_redraw(lambda:self.arr(self.directions()[1],PURPLE,width=7).set_z_index(11))
        a=txt(names[0],22,GREEN,width=1);b=txt(names[1],22,PURPLE,width=1)
        a.add_updater(lambda m:m.move_to(self.pt(1.35*self.directions()[0]+.65*self.directions()[1])))
        b.add_updater(lambda m:m.move_to(self.pt(1.35*self.directions()[1]-.3*self.directions()[0])))
        # Position labels before the first potentially frozen Scene.wait.
        a.update(0);b.update(0)
        self.basis_objects=VGroup(self.axis1,self.axis2,self.q1,self.q2,a,b);self.add(self.basis_objects)
    def turn(self,theta,seconds):self.play(self.angle.animate.set_value(theta),run_time=seconds,rate_func=smooth)
    def square(self):
        return RightAngle(Line(self.pt([0,0]),self.pt(Q1)),Line(self.pt([0,0]),self.pt(Q2)),length=.25,color=GRAY,stroke_width=2)
    def component(self,n,arrow=True,label=False):
        v,col=(P1,ORANGE) if n==1 else (P2,PURPLE)
        obj=self.arr(v,col).set_z_index(6) if arrow else Line(self.pt([0,0]),self.pt(v),color=col,stroke_width=5).set_z_index(5)
        self.add(obj)
        if label:
            at=[2.2,3.35] if n==1 else [3.,-1.65]
            self.add(txt('(3, 3)' if n==1 else '(2, −2)',22,col,width=2.7).move_to(self.pt(at)))
        return obj
    def drop(self,n):
        v=P1 if n==1 else P2
        obj=DashedLine(self.pt(X),self.pt(v),color=GRAY,stroke_width=2)
        self.add(obj,Dot(self.pt(v),radius=.05,color=ORANGE if n==1 else PURPLE));return obj
    def standard_guides(self):
        return VGroup(DashedLine(self.pt([5,0]),self.pt(X),color=GRAY),DashedLine(self.pt([0,1]),self.pt(X),color=GRAY),txt('5',23,BLUE).move_to(self.pt([5,-.35])),txt('1',23,BLUE).move_to(self.pt([-.3,1])))
    def pair_display(self):
        def text_pair():
            q1,q2=self.directions();t=self.angle.get_value()
            if abs(t)<1e-6:s='(5, 1)'
            elif abs(t-PI/4)<1e-6:s='(3√2, −2√2)'
            else:
                a,b=np.dot(X,q1),np.dot(X,q2);s=f'({a:.2f}, {b:.2f})'.replace('-', '−')
            return txt(s,41,ORANGE,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,-.2,0])
        self.live=always_redraw(text_pair);self.add(self.live)
        self.live_note=txt('현재 기저에서 읽은 좌표',22,GRAY,width=7).move_to(self.panel+[0,-1.15,0]);self.add(self.live_note)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.basis(0);self.info('(5, 1) → (?, ?)', '좌표는 변하는데, 벡터는 그대로?',ORANGE)
            self.turn(PI/8,3.5);self.to(4)
            self.turn(PI/4,2.3)
        elif i==1:
            self.basis(0,('e₁','e₂'));guides=self.standard_guides();self.add(guides)
            self.info('x = (5, 1)', '가로 5 · 세로 1',BLUE);self.to(12)
            self.info('e₁ = (1, 0)    e₂ = (0, 1)', '표준 기저의 두 단위벡터');self.to(16)
            self.remove(guides);self.info([('x',BLUE),('= 5e₁',GREEN),('+ 1e₂',PURPLE)],'좌표 5와 1은 기저에 곱하는 계수')
            first=self.arr([1,0],ORANGE).set_z_index(6);self.add(first)
            self.play(Transform(first,self.arr([5,0],ORANGE).set_z_index(6)),run_time=2)
            second=self.arr([0,1],PURPLE,origin=[5,0]).set_z_index(6);self.play(GrowArrow(second),run_time=1)
            self.add(Dot(self.pt(X),radius=.055,color=BLUE))
        elif i==2:
            self.basis(0);self.info('좌표축만 45° 회전', '벡터 x의 위치·방향·길이는 고정',GREEN)
            self.turn(PI/4,4);self.to(26)
            self.info('기준만 바뀌었다', '같은 벡터를 다른 기준에서 측정');self.to(30)
            self.info('q₁ = (1/√2, 1/√2)', '오른쪽 위 · 45°',GREEN);self.to(34)
            self.info('q₂ = (−1/√2, 1/√2)', '왼쪽 위 · 135°',PURPLE);self.to(37)
            self.add(self.square());self.info('‖q₁‖ = ‖q₂‖ = 1', 'q₁ · q₂ = 0    /    서로 수직');self.to(40)
            self.info('직교정규기저', 'Orthonormal Basis',GREEN,size=42)
        elif i==3:
            self.basis();self.info('[x]q = (?, ?)', '새로운 좌표는 얼마일까?',ORANGE);self.to(50)
            self.info('c₁ = x · q₁', '첫 번째 방향에서 측정',GREEN);self.to(52)
            self.info('q₁ = (1/√2, 1/√2)', '길이 1인 첫 번째 기준',GREEN);self.to(56)
            self.info('c₁ = (5 + 1)/√2', '= 3√2',ORANGE)
            self.play(Create(Line(self.pt([0,0]),self.pt(P1),color=ORANGE,stroke_width=5)),run_time=1.3);self.drop(1)
            self.add(txt('c₁ = 3√2',22,ORANGE,width=2.7).move_to(self.pt([1.8,3.25])))
        elif i==4:
            self.basis();self.component(1,False);self.drop(1)
            self.info('c₂ = x · q₂', '두 번째 방향에서 측정',PURPLE);self.to(65)
            self.info('q₂ = (−1/√2, 1/√2)', '왼쪽 위를 향하는 단위벡터',PURPLE);self.to(70)
            self.info('c₂ = (−5 + 1)/√2', '= −2√2',PURPLE)
            second=self.arr(P2,PURPLE).set_z_index(6);self.play(GrowArrow(second),run_time=1.8);self.drop(2)
            self.add(txt('음수 → q₂ 반대 방향',21,PURPLE,width=3.8).move_to(self.pt([4.3,-1.8])))
            self.to(75);self.info('[x]q = (3√2, −2√2)', '새 직교정규기저에서 읽은 좌표',ORANGE)
        elif i==5:
            self.basis();self.info('[x]ₑ = (5, 1)', '[x]q = (3√2, −2√2)',ORANGE);self.to(84)
            self.info('정말 같은 벡터일까?', '좌표 숫자를 잠시 가려 보면',BLUE);self.to(86)
            self.info('좌표 × 해당 기저', '두 성분을 더해 직접 확인한다',ORANGE)
        elif i==6:
            self.basis();self.info('3√2 q₁ = (3, 3)', '첫 번째 좌표 × 첫 번째 기저',ORANGE)
            first=self.arr(Q1,ORANGE).set_z_index(6);self.add(first)
            self.play(Transform(first,self.arr(P1,ORANGE).set_z_index(6)),run_time=2.4)
            self.add(txt('(3, 3)',22,ORANGE,width=2.7).move_to(self.pt([2.2,3.35])));self.to(94)
            self.info('−2√2 q₂ = (2, −2)', '음수이므로 q₂의 반대 방향',PURPLE)
            second=self.arr(Q2,PURPLE).set_z_index(6);self.add(second)
            self.play(Rotate(second,PI,about_point=self.origin),run_time=1)
            self.play(Transform(second,self.arr(P2,PURPLE).set_z_index(6)),run_time=1.6)
            p2label=txt('(2, −2)',22,PURPLE,width=2.7).move_to(self.pt([3.,-1.65]));self.add(p2label);self.to(100)
            self.play(Transform(second,self.arr(P2,PURPLE,origin=P1).set_z_index(6)),p2label.animate.move_to(self.pt([4.6,2.1])),run_time=2)
            self.info('(3, 3) + (2, −2) = (5, 1)', '원래 벡터가 그대로 복원된다',BLUE)
            self.add(Dot(self.pt(X),radius=.065,color=BLUE));self.play(Flash(self.pt(X),color=BLUE,flash_radius=.22),run_time=.8)
        elif i==7:
            self.basis();first=self.component(1,True);second=self.component(2,True)
            self.info('3√2 q₁ − 2√2 q₂ = x', '좌표와 기저를 함께 결합하면 같은 벡터',BLUE)
            self.play(Transform(second,self.arr(P2,PURPLE,origin=P1).set_z_index(6)),run_time=3)
            self.add(Dot(self.pt(X),radius=.06,color=BLUE));self.to(112)
            self.info('직교정규기저에서의 좌표', '각 기저 방향과의 내적');self.to(114)
            self.info([('c₁ = x · q₁',GREEN),(' / ',INK),('c₂ = x · q₂',PURPLE)],'내적 → 각 방향의 좌표')
            self.to(120)
            self.info('x = (x · q₁)q₁ + (x · q₂)q₂', '두 기저는 2차원 공간 전체를 이룬다',ORANGE)
        else:
            self.basis(0);self.add(txt('같은 벡터 · 기준만 다시 회전',24,BLUE,width=7.8 if SHORT else 6.5).move_to(self.panel+[0,.85,0]))
            self.pair_display();self.turn(PI/4,6);self.to(131)
            self.remove(self.live,self.live_note)
            self.info('x = Σᵢ (x · qᵢ)qᵢ', '공간 전체를 이루는 직교정규기저 {qᵢ}',ORANGE,size=35)
            self.add(txt('[x]ₑ = (5, 1)  /  [x]q = (3√2, −2√2)',22,GRAY,width=7.9 if SHORT else 6.5).move_to(self.panel+[0,-1.7,0]))
