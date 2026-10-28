import os,json
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F'
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class DotBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.meta['start'];self.origin=np.array([-.8,0.,0]) if SHORT else np.array([-4.2,-1.8,0]);self.unit=1.05 if SHORT else .88
        self.panel=np.array([0,-2.4,0]) if SHORT else np.array([3.5,.45,0])
        self.add(txt('INNER PRODUCT   /   LEVEL 01',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],34,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        self.add(txt('x  원래 벡터',19,BLUE,width=3).move_to([-2.1,5.15 if SHORT else -2.9,0]),txt('u  측정 기준',19,GREEN,width=3).move_to([1.7,5.15 if SHORT else -2.9,0]))
        self.add(txt('내적의 결과는 숫자 하나',18,GRAY).move_to([0,-7.45 if SHORT else -4.1,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def pt(self,x):return self.origin+self.unit*np.array([x[0],x[1],0.])
    def graph(self):
        self.grid=VGroup()
        for i in range(-2,5):
            self.grid.add(Line(self.pt([i,-1]),self.pt([i,4.5]),color=GRAY,stroke_opacity=.11,stroke_width=1),Line(self.pt([-2,i]),self.pt([4,i]),color=GRAY,stroke_opacity=.11,stroke_width=1)) if i<=4 and i>=-1 else None
        self.grid.add(Line(self.pt([-2,0]),self.pt([4.3,0]),color=GRAY,stroke_opacity=.6,stroke_width=1.5),Line(self.pt([0,-1]),self.pt([0,4.6]),color=GRAY,stroke_opacity=.6,stroke_width=1.5))
        self.add(self.grid,txt('0',17,GRAY).move_to(self.pt([-.25,-.27])))
        self.x=Arrow(self.pt([0,0]),self.pt([3,4]),buff=0,color=BLUE,stroke_width=6,max_tip_length_to_length_ratio=.07)
        self.xname=txt('x = (3, 4)',23,BLUE,width=3).move_to(self.pt([2.3,4.55]));self.add(self.x,self.xname)
    def arr(self,v,color=GREEN):return Arrow(self.pt([0,0]),self.pt(v),buff=0,color=color,stroke_width=7,max_tip_length_to_length_ratio=.2)
    def info(self,s,note='',color=INK):
        g=VGroup(txt(s,34,color,width=8 if SHORT else 6.8).move_to(self.panel))
        if note:g.add(txt(note,23,GRAY,width=8 if SHORT else 6.5).next_to(g[0],DOWN,buff=.4))
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=g;self.add(g);return g
    def to(self,t):
        remain=t-self.start-self.time
        if remain<-.04:raise RuntimeError((self.INDEX,t,self.time))
        if remain>.001:self.wait(remain)
    def triangle(self):
        return VGroup(DashedLine(self.pt([0,0]),self.pt([3,0]),color=GRAY),DashedLine(self.pt([3,0]),self.pt([3,4]),color=GRAY),txt('3',25,ORANGE).move_to(self.pt([1.5,-.35])),txt('4',25,ORANGE).move_to(self.pt([3.35,2])),txt('5',30,BLUE).move_to(self.pt([1.1,2.2])))
    def meter(self,angle,value=True):
        self.angle=ValueTracker(angle)
        def direction():return np.array([np.cos(self.angle.get_value()),np.sin(self.angle.get_value())])
        def scalar():
            n=float(np.dot([3,4],direction()));return 0. if abs(n)<1e-7 else n
        self.u=always_redraw(lambda:self.arr(direction()))
        def guide_end():
            u=direction();limit=min(5.1,3.3/abs(u[0])) if u[0]<-1e-6 else 5.1
            return limit*u
        self.guide=always_redraw(lambda:Line(self.pt(-1.3*direction()),self.pt(guide_end()),color=GREEN,stroke_width=1.5,stroke_opacity=.35))
        self.component=always_redraw(lambda:Line(self.pt([0,0]),self.pt(scalar()*direction()+np.array([1e-8,0])),color=ORANGE,stroke_width=5,stroke_opacity=.9))
        self.drop=always_redraw(lambda:DashedLine(self.pt([3,4]),self.pt(scalar()*direction()+np.array([1e-8,0])),color=GRAY,stroke_width=2))
        self.add(self.guide,self.drop,self.component,self.u)
        if value:
            number=always_redraw(lambda:txt(f'{scalar():.2f}',62,ORANGE).move_to(self.panel+[0,.25,0]))
            self.add(number,txt('x · u   /   測定'.replace('測定','측정값'),23,GRAY).move_to(self.panel+[0,1.1,0]))
    def turn(self,angle,d):self.play(self.angle.animate.set_value(angle),run_time=d,rate_func=smooth)
    def shot(self):
        i=self.INDEX;theta=np.arctan2(4,3)
        if i==0:
            u=self.arr([1,0]);self.add(u);self.info('x  ·  u  =  ?', '두 벡터를 곱하면?',ORANGE);self.to(2)
            self.info('내적', 'Dot Product');self.play(Indicate(u,color=GREEN),run_time=.7);self.to(6)
            self.info('a · b', 'Dot = 점    Product = 곱');self.to(9)
            self.info('(a₁, a₂) · (b₁, b₂)', 'a₁ × b₁ + a₂ × b₂');self.play(Indicate(self.inf),run_time=1)
        elif i==1:
            self.add(self.arr([1,0]));self.info('(3, 4) · (1, 0)', '대응하는 원소끼리 곱한다');self.to(18)
            self.info('3 × 1 + 4 × 0', '3 + 0');self.to(20)
            self.info('3', '내적의 결과',ORANGE);self.play(Indicate(self.inf[0]),run_time=.6);self.to(21)
            self.info('3', '이 숫자는 무엇을 의미할까?',ORANGE)
        elif i==2:
            tri=self.triangle();self.play(Create(tri),run_time=1.1);self.info('방향 + 길이', 'x = (3, 4)');self.to(26)
            self.info('‖x‖ = √(3² + 4²)', '= 5',BLUE);self.play(Indicate(self.x,color=BLUE),run_time=1.2)
        elif i==3:
            self.add(self.triangle());u=self.arr([3,4]);self.add(u);self.info('방향은 그대로', '길이 5 → 1',GREEN)
            self.play(Transform(u,self.arr([.6,.8])),run_time=2);self.to(36)
            self.info('u = (3/5, 4/5)', '= (0.6, 0.8)',GREEN);self.to(40)
            self.info('단위벡터 · Unit Vector','√(0.6² + 0.8²) = 1',GREEN);self.play(Indicate(u,color=GREEN),run_time=1)
        elif i==4:
            self.add(self.arr([.6,.8]));self.info('(3, 4) · (0.6, 0.8)', '같은 방향 · 길이 1');self.to(49)
            self.info('3 × 0.6 = 1.8', '첫 번째 원소의 곱');self.to(51)
            self.info('4 × 0.8 = 3.2', '두 번째 원소의 곱');self.to(53)
            self.info('1.8 + 3.2 = 5', '내적으로 읽은 값',ORANGE);self.play(Indicate(self.inf[0],color=ORANGE),run_time=.7);self.to(55)
            length=txt('5',35,ORANGE).move_to(self.pt([1.1,2.3]));self.add(length);self.play(TransformFromCopy(self.inf[0],length),run_time=.8);self.to(57)
            self.play(Create(Line(self.pt([0,0]),self.pt([3,4]),color=ORANGE,stroke_width=5)),run_time=.8)
            self.add(self.arr([.6,.8]));self.info('같은 방향에서 측정하면 5', '원래 벡터의 전체 길이',ORANGE)
        elif i==5:
            self.meter(theta,False);self.info('기준 방향을 바꾸면?', '원래 벡터 x는 고정');self.turn(0,2);self.to(65)
            self.info('x · (1, 0) = 3', '가로 방향의 성분',ORANGE);self.to(69)
            self.turn(PI/2,1.2);self.info('x · (0, 1) = 4', '세로 방향의 성분',ORANGE)
        elif i==6:
            self.meter(PI/2);self.turn(0,2);self.turn(theta,3);self.to(80)
            self.play(Indicate(self.x,color=ORANGE),run_time=.8);self.turn(PI/2,2.2);self.to(86)
            self.turn(theta+PI/2,2);self.add(txt('u = (−0.8, 0.6)',23,GREEN,width=6).move_to(self.panel+[0,-.65,0]),txt('−2.4 + 2.4 = 0',23,GRAY).move_to(self.panel+[0,-1.2,0]))
        else:
            self.meter(theta+PI/2,False)
            self.info('같은 방향 5  /  가로 3', 'x와 수직인 방향 0',ORANGE);self.to(96)
            for m in [self.u,self.guide,self.drop,self.component]:m.clear_updaters();self.remove(m)
            self.add(self.arr([.6,.8]));self.info('x · u = ‖x‖ cos θ', '‖u‖ = 1\n특정 방향에서 측정한 부호 있는 성분',ORANGE)
