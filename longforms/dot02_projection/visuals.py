"""One fixed Euclidean diagram, scalar measurement, and vector reconstruction."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F'
X=np.array([4.,2.]);U=np.ones(2)/np.sqrt(2);PROJ=np.array([3.,3.])
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def colored(parts,size=32,width=7.8):
    g=VGroup(*(txt(s,size,c,width) for s,c in parts)).arrange(RIGHT,buff=.12)
    if g.width>width:g.scale_to_fit_width(width)
    return g
class ProjectionBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.meta['start'];self.origin=np.array([-1.5,.4,0]) if SHORT else np.array([-5.75,-1.65,0]);self.unit=1.05
        self.panel=np.array([0,-2.25,0]) if SHORT else np.array([3.55,.55,0])
        self.add(txt('DOT PRO   /   LEVEL 02',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        if SHORT:
            self.add(txt('x  원래 벡터',18,BLUE,width=2.8).move_to([-2.5,5.15,0]),txt('u  기준',18,GREEN,width=2).move_to([0,5.15,0]),txt('p  추출 성분',18,ORANGE,width=2.8).move_to([2.45,5.15,0]))
        else:
            self.add(txt('x  원래 벡터',18,BLUE,width=2.8).move_to([-5.6,-2.9,0]),txt('u  기준',18,GREEN,width=2).move_to([-2.7,-2.9,0]),txt('p  추출 성분',18,ORANGE,width=2.8).move_to([.3,-2.9,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def pt(self,v):return self.origin+self.unit*np.array([v[0],v[1],0.])
    def graph(self):
        grid=VGroup()
        for i in range(5):
            grid.add(Line(self.pt([i,-.7]),self.pt([i,4.1]),color=GRAY,stroke_opacity=.11,stroke_width=1),Line(self.pt([-.7,i]),self.pt([4.8,i]),color=GRAY,stroke_opacity=.11,stroke_width=1))
        grid.add(Line(self.pt([-.7,0]),self.pt([4.8,0]),color=GRAY,stroke_opacity=.6,stroke_width=1.5),Line(self.pt([0,-.7]),self.pt([0,4.1]),color=GRAY,stroke_opacity=.6,stroke_width=1.5))
        self.add(grid,txt('0',17,GRAY).move_to(self.pt([-.2,-.26])))
        self.x=self.arr(X,BLUE,5);self.add(self.x)
        self.add(txt('x = (4, 2)',22,BLUE,width=2.6).move_to(self.pt([4.,1.55])))
    def arr(self,v,col=GREEN,width=6):return Arrow(self.pt([0,0]),self.pt(v),buff=0,color=col,stroke_width=width,max_tip_length_to_length_ratio=.13)
    def basis(self,unit=True,angle=False):
        self.baseline=Line(self.pt([-.65,-.65]),self.pt([3.9,3.9]),color=GREEN,stroke_opacity=.45,stroke_width=2)
        self.add(self.baseline)
        if unit:
            self.u=self.arr(U,GREEN,7).set_z_index(8);self.add(self.u)
        if angle:
            arc=Arc(radius=.65*self.unit,start_angle=0,angle=PI/4,arc_center=self.origin,color=GRAY,stroke_width=2)
            self.add(arc,txt('45°',19,GREEN,width=1.3).move_to(self.pt([1.15,.32])))
    def projection(self,label=True):
        self.p=self.arr(PROJ,ORANGE,6).set_z_index(4);self.add(self.p)
        if hasattr(self,'u'):self.add(self.u)
        if label:self.add(txt('p = (3, 3)',22,ORANGE,width=2.8).move_to(self.pt([2.25,3.55])))
        return self.p
    def foot(self):
        return Dot(self.pt(PROJ),radius=.065,color=ORANGE)
    def perpendicular(self,animate=False):
        line=DashedLine(self.pt(X),self.pt(PROJ),color=GRAY,stroke_width=3)
        if animate:self.play(Create(line),run_time=2)
        else:self.add(line)
        right=RightAngle(Line(self.pt(PROJ),self.pt(PROJ+[1,1])),Line(self.pt(PROJ),self.pt(X)),length=.23,color=GRAY,stroke_width=2)
        self.add(right,self.foot())
        return VGroup(line,right)
    def coordinate_guides(self,v,color=GRAY):
        return VGroup(DashedLine(self.pt([v[0],0]),self.pt(v),color=color,stroke_opacity=.5),DashedLine(self.pt([0,v[1]]),self.pt(v),color=color,stroke_opacity=.5),txt(str(int(v[0])),22,color).move_to(self.pt([v[0],-.3])),txt(str(int(v[1])),22,color).move_to(self.pt([-.3,v[1]])))
    def info(self,s,note='',color=INK,size=32):
        line=txt(s,size,color,width=8 if SHORT else 6.7) if isinstance(s,str) else colored(s,size,width=8 if SHORT else 6.7)
        line.move_to(self.panel)
        group=VGroup(line)
        if note:group.add(txt(note,23,GRAY,width=7.8 if SHORT else 6.6).next_to(line,DOWN,buff=.42))
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=group;self.add(group);return group
    def to(self,t):
        remain=t-self.start-self.time
        if remain<-.04:raise RuntimeError(f'Scene {self.INDEX+1}: clock {self.time} exceeds {t-self.start}')
        if remain>.001:self.wait(remain)
    def scalar_line(self):
        return Line(self.pt([0,0]),self.pt(PROJ),color=ORANGE,stroke_width=5)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.basis();self.info([('x',BLUE),('·',INK),('u',GREEN),('= 숫자 하나',ORANGE)],'특정 방향에서 읽은 값')
            self.play(Indicate(self.u,color=GREEN),run_time=.7);self.to(5)
            self.info('숫자 → 벡터 ?', '원하는 방향의 성분만 꺼낼 수 있을까?',ORANGE)
            question=self.arr([1.7,1.7],GRAY).set_opacity(.4);self.play(GrowArrow(question),run_time=1)
            self.add(txt('?',27,GRAY).move_to(self.pt([1.25,2.])))
        elif i==1:
            guides=self.coordinate_guides(X,BLUE);self.play(Create(guides),run_time=1);self.info('x = (4, 2)','가로 4 · 세로 2',BLUE);self.to(14)
            self.basis(False,True);self.play(Indicate(self.baseline,color=GREEN),run_time=1)
            self.info('45° 방향의 성분', '원래 벡터 x는 고정',GREEN)
        elif i==2:
            self.basis(False);self.u=self.arr(U,GREEN,7).set_z_index(8);self.play(GrowArrow(self.u),run_time=1)
            self.info('길이 1인 기준벡터', '45° 방향',GREEN);self.to(22)
            tri=VGroup(DashedLine(self.pt([0,0]),self.pt([U[0],0]),color=GREEN),DashedLine(self.pt([U[0],0]),self.pt(U),color=GREEN))
            self.add(tri,txt('1',20,GREEN).move_to(self.pt([.25,.7])))
            self.info('u = (1/√2, 1/√2)', '‖u‖ = √(1/2 + 1/2) = 1',GREEN)
            self.play(Indicate(self.u,color=GREEN),run_time=.8)
        elif i==3:
            self.basis();self.info([('(4, 2)',BLUE),('·',INK),('(1/√2, 1/√2)',GREEN)],'원래 벡터와 기준 단위벡터');self.to(30)
            self.info([('4',BLUE),('× 1/√2',GREEN),('+',INK),('2',BLUE),('× 1/√2',GREEN)],'= 6/√2')
            self.play(Indicate(self.inf[0][0],color=BLUE),Indicate(self.inf[0][1],color=GREEN),run_time=1.1)
            self.play(Indicate(self.inf[0][3],color=BLUE),Indicate(self.inf[0][4],color=GREEN),run_time=1.1);self.to(35)
            self.info('x · u = 3√2', '≈ 4.24    /    숫자 하나',ORANGE,size=42);self.play(Indicate(self.inf[0],color=ORANGE),run_time=.8)
        elif i==4:
            self.basis();measurement=self.scalar_line();self.play(Create(measurement),run_time=1.4);self.add(self.u)
            self.info('3√2 ≈ 4.24', '45° 방향에서 측정한 부호 있는 길이',ORANGE,size=42);self.to(43)
            self.info('숫자 3√2  →  벡터 (?, ?)', '스칼라 하나에 방향을 결합하려면?',ORANGE)
            self.add(txt('화살촉 없는 선분 = 측정 구간',19,GRAY,width=6).move_to(self.panel+[0,-1.5,0]));self.to(48)
            self.play(Indicate(self.u,color=GREEN),run_time=.6)
        elif i==5:
            self.basis();self.info('u = (1/√2, 1/√2)', '방향 45° · 길이 1',GREEN)
            self.play(Indicate(self.u,color=GREEN),run_time=1);self.to(54)
            self.info([('3√2',ORANGE),('×',INK),('(1/√2, 1/√2)',GREEN)],'길이 1 → 3√2 ≈ 4.24')
            growth=self.arr(U,GREEN,6).set_z_index(4);self.add(growth)
            self.play(Transform(growth,self.arr(PROJ,ORANGE,6).set_z_index(4)),run_time=4,rate_func=smooth)
            self.info('(3√2 / √2, 3√2 / √2)', '= (3, 3)',ORANGE)
            self.add(self.coordinate_guides(PROJ,ORANGE),self.foot(),txt('p = (3, 3)',22,ORANGE,width=2.8).move_to(self.pt([2.25,3.55])))
            self.play(Indicate(self.inf[1],color=ORANGE),run_time=.9)
        elif i==6:
            self.basis();self.projection();self.info([('x = (4, 2)',BLUE),('→',INK),('p = (3, 3)',ORANGE)],'45° 방향의 성분만 추출');self.to(66)
            self.info('정사영', 'Orthogonal Projection',ORANGE,size=44);self.to(71)
            perpendicular=self.perpendicular(True)
            self.play(Indicate(perpendicular[1],color=ORANGE,scale_factor=1.7),run_time=1)
            self.info('(4, 2) → (3, 3)', '기준선에 수직으로 내린 수선의 발',ORANGE)
            self.add(txt('(x − p) · u = (1 − 1)/√2 = 0',22,GRAY,width=7 if SHORT else 6.5).move_to(self.panel+[0,-1.7,0]))
        elif i==7:
            self.basis();self.projection();self.info('측정 → 방향 결합', '하나의 과정으로 묶어 보면');self.to(80)
            self.info('STEP 01   x · u = 3√2', '내적 → 숫자 하나',ORANGE);self.play(Indicate(self.inf[0],color=ORANGE),run_time=.7);self.to(84)
            self.info('STEP 02   (x · u)u = (3, 3)', '측정값 × 기준 단위벡터 → 정사영',ORANGE)
            self.remove(self.p);self.p=self.arr(U,ORANGE,6).set_z_index(4);self.add(self.p)
            self.play(Transform(self.p,self.arr(PROJ,ORANGE,6).set_z_index(4)),run_time=2.2)
        else:
            self.basis();self.projection();self.perpendicular()
            self.info('내적:  x · u  →  숫자', '정사영:  (x · u)u  →  벡터',ORANGE)
            self.add(txt('기준 단위벡터의 길이 ‖u‖ = 1',21,GREEN,width=7).move_to(self.panel+[0,-1.7,0]));self.to(96)
            self.info('projᵤ(x) = (x · u)u', '내적으로 측정하고, 같은 방향으로 추출한다.',ORANGE)
            self.play(Indicate(self.p,color=ORANGE),run_time=1)
