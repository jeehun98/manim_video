"""Orthogonal subtraction, translated residual, and exact vector reconstruction."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F';PURPLE='#BB97FF'
X=np.array([4.,2.]);U=np.ones(2)/np.sqrt(2);PROJ=np.array([3.,3.]);RES=X-PROJ
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
def colored(parts,size=32,width=7.8):
    g=VGroup(*(txt(s,size,c,width) for s,c in parts)).arrange(RIGHT,buff=.12)
    if g.width>width:g.scale_to_fit_width(width)
    return g
class ResidualBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.meta['start'];self.origin=np.array([-1.5,.4,0]) if SHORT else np.array([-5.75,-1.65,0]);self.unit=1.05
        self.panel=np.array([0,-2.25,0]) if SHORT else np.array([3.55,.55,0])
        self.add(txt('DOT PRO   /   LEVEL 03',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],33,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        if SHORT:
            for x,s,c in zip([-3,-1,1,3],['x 원래','u 기준','p 정사영','r 잔차'],[BLUE,GREEN,ORANGE,PURPLE]):
                self.add(txt(s,17,c,width=1.8).move_to([x,5.15,0]))
        else:
            for x,s,c in zip([-5.8,-2.9,0,2.9],['x 원래 벡터','u 기준','p 정사영','r 잔차'],[BLUE,GREEN,ORANGE,PURPLE]):
                self.add(txt(s,18,c,width=2.8).move_to([x,-3.03,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def pt(self,v):return self.origin+self.unit*np.array([v[0],v[1],0.])
    def graph(self):
        grid=VGroup()
        for i in range(5):
            grid.add(Line(self.pt([i,-1.1]),self.pt([i,4.1]),color=GRAY,stroke_opacity=.11,stroke_width=1),Line(self.pt([-.7,i]),self.pt([4.8,i]),color=GRAY,stroke_opacity=.11,stroke_width=1))
        grid.add(Line(self.pt([-.7,-1]),self.pt([4.8,-1]),color=GRAY,stroke_opacity=.11,stroke_width=1))
        grid.add(Line(self.pt([-.7,0]),self.pt([4.8,0]),color=GRAY,stroke_opacity=.6,stroke_width=1.5),Line(self.pt([0,-1.1]),self.pt([0,4.1]),color=GRAY,stroke_opacity=.6,stroke_width=1.5))
        self.add(grid,txt('0',17,GRAY).move_to(self.pt([-.2,-.26])))
        self.x=self.arr(X,BLUE,5);self.add(self.x)
        self.xname=txt('x = (4, 2)',22,BLUE,width=2.6).move_to(self.pt([4.,1.55]));self.add(self.xname)
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
        if label:
            self.pname=txt('p = (3, 3)',22,ORANGE,width=2.8).move_to(self.pt([2.25,3.55]));self.add(self.pname)
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
    def residual_arrow(self,at_tip=False):
        base=PROJ if at_tip else np.zeros(2)
        return Arrow(self.pt(base),self.pt(base+RES),buff=0,color=PURPLE,stroke_width=6,max_tip_length_to_length_ratio=.16).set_z_index(5)
    def residual(self,at_tip=False,label=True):
        self.r=self.residual_arrow(at_tip);self.add(self.r)
        if label:
            at=[4.05,3.05] if at_tip else [2.05,-.75]
            self.rname=txt('r = (1, −1)',22,PURPLE,width=2.8).move_to(self.pt(at));self.add(self.rname)
        return self.r
    def orthogonal_marker(self,base=None):
        base=np.zeros(2) if base is None else np.array(base)
        return RightAngle(Line(self.pt(base),self.pt(base+U)),Line(self.pt(base),self.pt(base+RES)),length=.27,color=GRAY,stroke_width=2)
    def dim_original(self,opacity=.17,projection=True):
        self.x.set_opacity(opacity);self.xname.set_opacity(opacity)
        if projection:
            if hasattr(self,'p'):self.p.set_opacity(opacity)
            if hasattr(self,'pname'):self.pname.set_opacity(opacity)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.basis(False,True);self.info('이 방향의 성분만 제거한다면?', 'x = (4, 2)',PURPLE);self.to(4)
            component=self.scalar_line().set_opacity(.65);self.play(Create(component),run_time=.8)
            self.info('정사영으로 찾은 성분', '제거할 방향과 나란한 부분',ORANGE);self.to(7)
            self.play(Create(self.coordinate_guides(X,BLUE)),run_time=.8);self.info('x = (4, 2)', '가로 4 · 세로 2',BLUE);self.to(10)
            self.info('제거할 방향: 45°', '이 방향의 성분만 선택한다',GREEN);self.play(Indicate(self.baseline,color=GREEN),run_time=1)
        elif i==1:
            self.basis(False);self.u=self.arr(U,GREEN,7).set_z_index(8);self.play(GrowArrow(self.u),run_time=.8)
            self.info('제거할 성분을 먼저 구한다', '기준 방향 45°',GREEN);self.to(17)
            self.info('u = (1/√2, 1/√2)', '‖u‖ = 1',GREEN)
            tri=VGroup(DashedLine(self.pt([0,0]),self.pt([U[0],0]),color=GREEN),DashedLine(self.pt([U[0],0]),self.pt(U),color=GREEN))
            self.add(tri);self.to(23)
            self.info('x · u = 4/√2 + 2/√2', '= 3√2',ORANGE);self.play(Indicate(self.inf[1],color=ORANGE),run_time=.7);self.to(26)
            self.remove(tri);self.info('p = (x · u)u', '= 3√2 (1/√2, 1/√2)',ORANGE)
            growth=self.arr(U,GREEN,6).set_z_index(4);self.add(growth)
            self.play(Transform(growth,self.arr(PROJ,ORANGE,6).set_z_index(4)),run_time=3)
            self.add(txt('p = (3, 3)',22,ORANGE,width=2.8).move_to(self.pt([2.25,3.55])))
            self.info('p = (3, 3)', '제거할 방향과 나란한 성분',ORANGE)
        elif i==2:
            self.basis();self.projection();self.info([('r',PURPLE),('=',INK),('x',BLUE),('−',INK),('p',ORANGE)],'(4, 2) − (3, 3)');self.to(36)
            self.info('가로: 4 − 3 = 1', '첫 번째 성분',PURPLE);self.to(38)
            self.info('세로: 2 − 3 = −1', '두 번째 성분',PURPLE);self.to(40)
            self.r=self.residual_arrow(True);self.play(GrowArrow(self.r),run_time=1.5)
            self.add(txt('r = (1, −1)',22,PURPLE,width=2.8).move_to(self.pt([4.05,3.05])))
            self.info('r = (1, −1)', '정사영 끝점 → 원래 벡터 끝점',PURPLE)
        elif i==3:
            self.basis();self.projection();self.residual(True,False);self.dim_original()
            self.info('정말 45° 성분이 사라졌을까?', '남은 벡터로 직접 확인한다',PURPLE)
            self.play(Transform(self.r,self.residual_arrow(False)),run_time=2)
            self.add(txt('r = (1, −1)',22,PURPLE,width=2.8).move_to(self.pt([2.05,-.75])))
            self.to(49);self.info('잔차 · 기준 방향 = ?', '같은 방향에서 다시 내적한다',PURPLE);self.play(Indicate(self.u,color=GREEN,scale_factor=1),run_time=.7);self.to(53)
            self.check=self.arr([1,1],GREEN,5).set_z_index(7);self.play(GrowArrow(self.check),run_time=.7)
            self.add(txt('v = (1, 1)',21,GREEN,width=2.8).move_to(self.pt([.8,1.4])))
            self.info('(1, −1) · (1, 1)', '직교 검사: 길이 1일 필요는 없다',GREEN)
            vnote=txt('v = (1, 1) = √2 u  /  ‖v‖ = √2',21,GRAY,width=7 if SHORT else 6.5).move_to(self.panel+[0,-1.55,0]);self.add(vnote);self.to(58)
            self.remove(vnote)
            self.info('1 × 1 + (−1) × 1', '서로 반대인 두 기여',PURPLE)
            terms=VGroup(txt('+1',36,ORANGE).move_to(self.panel+[-1.5,-1.2,0]),txt('−1',36,PURPLE).move_to(self.panel+[1.5,-1.2,0]))
            self.add(terms);self.play(terms[0].animate.move_to(self.panel+[-.6,-1.2,0]),terms[1].animate.move_to(self.panel+[.6,-1.2,0]),run_time=1.4);self.to(61)
            self.remove(terms);self.info('0', '1 − 1 = 0',PURPLE,size=60)
            self.add(self.orthogonal_marker());self.play(Indicate(self.inf[0],color=PURPLE),run_time=.6)
        elif i==4:
            self.basis();self.residual();self.dim_original(projection=False)
            square=self.orthogonal_marker();self.add(square)
            self.info('r · u = 0', '두 방향은 직교한다 · 90°',PURPLE,size=42)
            self.play(Indicate(square,color=PURPLE,scale_factor=1.5),run_time=1);self.to(65)
            # The foot of the residual on the reference line is exactly the origin.
            drop=DashedLine(self.pt(RES),self.pt([0,0]),color=GRAY,stroke_width=3)
            self.play(Create(drop),run_time=1)
            dot=Dot(self.pt([0,0]),radius=.065,color=ORANGE);self.add(dot)
            self.info('기준 방향의 투영 = 0', '측정 구간은 원점의 점 하나',ORANGE)
            self.play(Indicate(dot,color=ORANGE,scale_factor=1.8),run_time=1);self.to(70)
            self.info('이것은 우연이 아니다', '나란한 성분을 정확히 뺐기 때문',PURPLE)
        elif i==5:
            self.basis();self.projection();self.residual(True,False)
            self.info('p는 기준 방향과 나란하다', '정사영으로 추출한 성분',ORANGE)
            self.play(Indicate(self.p,color=ORANGE,scale_factor=1),run_time=1);self.to(76)
            self.info('나란한 성분을 제거하면', '직교하는 성분만 남는다',PURPLE)
            self.play(self.p.animate.set_opacity(0),self.pname.animate.set_opacity(0),self.x.animate.set_opacity(.15),self.xname.animate.set_opacity(.15),Transform(self.r,self.residual_arrow(False)),run_time=2)
            self.add(self.orthogonal_marker());self.to(80)
            self.info('잔차 · Residual', '선택한 방향으로 설명되지 않는 성분',PURPLE,size=40)
            self.add(txt('r = (1, −1)',22,PURPLE,width=2.8).move_to(self.pt([2.05,-.75])))
        elif i==6:
            self.basis();self.projection();self.residual(False,False);self.x.set_opacity(.25);self.xname.set_opacity(.25)
            rlabel=txt('직교 성분 r',20,PURPLE,width=3).move_to(self.pt([2.05,-.75]))
            self.add(txt('나란한 성분 p',20,ORANGE,width=3).move_to(self.pt([1.6,2.8])),rlabel)
            square=self.orthogonal_marker();self.add(square);self.info([('x',BLUE),('=',INK),('p',ORANGE),('+',INK),('r',PURPLE)],'(4, 2) = (3, 3) + (1, −1)');self.to(89)
            self.play(Transform(self.r,self.residual_arrow(True)),rlabel.animate.move_to(self.pt([4.05,3.05])),Transform(square,self.orthogonal_marker(PROJ)),run_time=1.8)
            self.play(self.x.animate.set_opacity(1),self.xname.animate.set_opacity(1),run_time=.7)
            self.add(Dot(self.pt(X),radius=.065,color=BLUE));self.info('(3, 3) + (1, −1) = (4, 2)', '두 성분을 더하면 원래 벡터',BLUE)
        else:
            self.basis();self.projection();self.residual();self.dim_original(.2,False)
            self.add(self.orthogonal_marker());self.info('측정   x · u', '= 3√2',ORANGE);self.to(95)
            self.info('추출   (x · u)u', '= (3, 3)',ORANGE);self.to(97)
            self.info('제거   r = x − (x · u)u', '= (1, −1)',PURPLE)
            self.add(txt('‖u‖ = 1     /     r · u = 0',22,GREEN,width=7).move_to(self.panel+[0,-1.65,0]));self.to(99)
            self.x.set_opacity(0);self.xname.set_opacity(0);self.p.set_opacity(0);self.pname.set_opacity(0)
            self.play(Indicate(self.r,color=PURPLE,scale_factor=1),run_time=.8)
