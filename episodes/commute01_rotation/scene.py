"""Actual 3D vertices projected by a fixed orthographic camera into a portrait layout."""
import json
import os
import sys
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from longforms.qcs01_speed.direction import QCSScene,label
from quantum_series.shared.theme import FONT
from episodes.commute01_rotation import model

DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
BG,INK,MUTED='#101923','#EDF3FC','#8B9CB7'
XCOL,YCOL,ZCOL,GOLD,GREEN,RED='#FF827C','#61AEFF','#52E2A8','#FFD275','#52E2A8','#FF747F'
config.background_color=BG

def txt(s,y=0,size=34,c=INK,x=0,width=7.5):return label(s,x=x,y=y,size=size,color=c,width=width)
def math(s,y=0,size=46,c=INK,width=7.3):
    m=MathTex(s,font_size=size,color=c)
    if m.width>width:m.scale_to_fit_width(width)
    return m.move_to(UP*y)
def panel(s,y,c=GREEN,size=29):
    return VGroup(RoundedRectangle(width=7.1,height=.95,corner_radius=.14,stroke_color=c,fill_color=c,fill_opacity=.05),txt(s,size=size,c=c,width=6.8)).move_to(UP*y)

class Book(VGroup):
    """Immutable local vertices; orientation is the only rotational state."""
    def __init__(self,y=1.4,scale=1.25):
        super().__init__();self.origin=np.array([0.,y,0.]);self.display_scale=scale;self.orientation=np.eye(3)
        x,y,z=.8,1.15,.16
        self.vertices=np.array([[-x,-y,-z],[x,-y,-z],[x,y,-z],[-x,y,-z],[-x,-y,z],[x,-y,z],[x,y,z],[-x,y,z]])
        self.faces=[([0,3,2,1],'#245765'),([0,1,5,4],'#DED9CC'),([1,2,6,5],'#D9D5C8'),
                    ([2,3,7,6],'#D9D5C8'),([3,0,4,7],'#843F4A'),([4,5,6,7],GOLD)]
        self.polygons=[Polygon(*[ORIGIN,RIGHT,UP],fill_color=c,fill_opacity=1,stroke_color=c,stroke_width=1.3) for _,c in self.faces]
        front=Text('FRONT',font=FONT,font_size=21,color='#30261A').scale(.8)
        front.move_to([0,0,.17])
        top=Text('TOP ↑',font=FONT,font_size=13,color='#30261A').move_to([0,.82,.17])
        self.decals=[front,top]
        self.decal_points=[[m.points.copy() for m in d.family_members_with_points()] for d in self.decals]
        self.surface=VGroup(*self.polygons,*self.decals)
        self.normal=Arrow(ORIGIN,UP,buff=0,color=GOLD,stroke_width=5,max_tip_length_to_length_ratio=.2)
        self.add(self.surface,self.normal);self.refresh()
    def refresh(self):
        vertices=self.vertices@self.orientation.T
        points=model.project(vertices,self.origin,self.display_scale)
        order=[]
        for polygon,(indices,_) in zip(self.polygons,self.faces):
            polygon.set_points_as_corners([*points[indices],points[indices[0]]])
            order.append((float(np.mean(vertices[indices],axis=0)@model.EYE),polygon))
        for decal,originals in zip(self.decals,self.decal_points):
            for part,original in zip(decal.family_members_with_points(),originals):
                part.set_points(model.project(original@self.orientation.T,self.origin,self.display_scale))
            order.append((float((self.orientation@np.array([0,0,.18]))@model.EYE),decal))
        self.surface.submobjects=[m for _,m in sorted(order,key=lambda pair:pair[0])]
        normal=model.project(np.array([[0,0,.22],[0,0,1.45]])@self.orientation.T,self.origin,self.display_scale)
        self.normal.put_start_and_end_on(*normal)
        return self
    def pose(self,origin=None,scale=None):
        if origin is not None:self.origin=np.array(origin,dtype=float)
        if scale is not None:self.display_scale=scale
        return self.refresh()

def world_axes(book):
    axes=VGroup()
    for vector,name,c in [(RIGHT,'X',XCOL),(UP,'Y',YCOL),(OUT,'Z',ZCOL)]:
        a,b=model.project(np.array([-1.75*vector,1.95*vector]),book.origin,book.display_scale)
        axis=Arrow(a,b,buff=0,color=c,stroke_width=2,max_tip_length_to_length_ratio=.055)
        axes.add(axis,txt(name,size=20,c=c,width=.4).move_to(b+(b-a)/np.linalg.norm(b-a)*.2))
    return axes

class RotationScene(QCSScene):
    data=DATA
    def setup(self):
        super().setup();self.remove(self.mobjects[0]);self.title.move_to(UP*5.35)
        self.add(txt('회전과 행렬  /  NONCOMMUTATIVITY',7,18,MUTED));self.rotation_records=[]
    def turn(self,book,axis,duration=1.3):
        before=book.orientation.copy();at=self.offset+self.time
        self.play(UpdateFromAlphaFunc(book,lambda b,a:self.set_rotation(b,axis,a,before)),run_time=duration)
        book.orientation=(model.RX if axis=='X' else model.RY)@before;book.refresh()
        assert np.allclose(book.orientation.T@book.orientation,np.eye(3))
        self.rotation_records.append(dict(at=round(at,6),end=round(self.offset+self.time,6),axis=axis,
            before=before.tolist(),after=book.orientation.tolist(),normal=(book.orientation@model.NORMAL).tolist()))
    @staticmethod
    def set_rotation(book,axis,a,before):
        book.orientation=model.rotation(axis,a*PI/2)@before;book.refresh()
    def construct(self):
        super().construct()
        audit=Path(os.environ.get('QCS_AUDIT_DIR',str(HERE/'audit')))
        (audit/(self.info['id']+'_rotations.json')).write_text(json.dumps(self.rotation_records),encoding='utf-8')

def plane(y=.6):
    axes=Axes(x_range=[-2.5,2.5,1],y_range=[-2.5,2.5,1],x_length=6,y_length=6,
              tips=False,axis_config={'color':MUTED,'stroke_width':2}).move_to(UP*y)
    return axes
def vector(axes,point,c):return Arrow(axes.c2p(0,0),axes.c2p(*point),buff=0,color=c,stroke_width=5)

class Shot01(RotationScene):
    shot=0
    def s01(self):
        self.show(txt('교환법칙?',2.8,61,GOLD))
        self.to(2)
        a,b=txt('2',.7,62,YCOL,x=-1.55),txt('3',.7,62,YCOL,x=1.55)
        sign=txt('+',.7,53);self.show(a,b,sign)
        self.to(4);self.play(Swap(a,b),run_time=1)
        self.to(7)
        self.show(math('2+3=3+2=5',-1.3,45,GREEN))
        self.to(9)
        self.play(Transform(sign,txt('×',.7,53)))
        self.show(math(r'2\times3=3\times2=6',-2.7,45,GREEN))
        self.to(13)
        self.play(FadeOut(VGroup(a,b,sign)),run_time=.5)
        self.show(txt('A → B',1,40,XCOL),txt('B → A',-.1,40,YCOL))
        self.show(txt('행동의 순서도 같을까?',-4.1,34,GOLD))

class Shot02(RotationScene):
    shot=1
    def s02(self):
        book=Book();axes=world_axes(book);self.show(axes,book)
        self.show(txt('공간에 고정된 X·Y·Z축',4.5,24,MUTED))
        command=txt('앞표지: +Z',-1.7,32,GOLD);self.show(command)
        self.to(23)
        self.play(Transform(command,txt('X축 +90°',-1.7,32,XCOL)),run_time=.3)
        self.turn(book,'X',1.7);self.wait(.4)
        self.to(27)
        self.play(Transform(command,txt('다음 Y축 +90°',-1.7,32,YCOL)),run_time=.3)
        self.turn(book,'Y',1.7);self.wait(.4)
        self.to(31)
        self.play(FadeOut(axes),FadeOut(command),run_time=.3)
        book.pose([-2,1.3,0],.8)
        first_axes=world_axes(book);self.add(first_axes)
        second=Book();second.pose([2,1.3,0],.8);second_axes=world_axes(second)
        self.show(second,second_axes,run_time=.35)
        self.turn(second,'Y',1);self.wait(.3);self.turn(second,'X',1)
        self.to(35)
        self.show(txt('X → Y',-.7,31,XCOL,x=-2,width=3),txt('Y → X',-.7,31,YCOL,x=2,width=3))
        self.show(txt('앞표지 −Y',-1.7,27,GOLD,x=-2,width=3.4),txt('앞표지 +X',-1.7,27,GOLD,x=2,width=3.4))
        self.show(panel('같은 회전 · 다른 순서 → 다른 자세',-3.2,GREEN,size=27))
        self.to(40)
        self.show(txt('이 차이를 좌표와 행렬로 표현한다면?',-4.4,25,MUTED))

class Shot03(RotationScene):
    shot=2
    def s03(self):
        ax=plane();self.show(ax)
        e1=vector(ax,(1,0),GOLD);self.show(e1,txt('(1, 0)',-3,32,GOLD))
        self.to(46)
        self.show(txt('원점 중심의 회전',4.2,28,MUTED))
        self.to(52)
        self.play(Rotate(e1,PI/2,about_point=ax.c2p(0,0)),run_time=1.8)
        self.show(txt('(1, 0) → (0, 1)',-3.6,32,GOLD))
        self.to(57)
        e2=vector(ax,(0,1),YCOL);self.show(e2,run_time=.3)
        self.play(Rotate(e2,PI/2,about_point=ax.c2p(0,0)),run_time=1.7)
        self.show(txt('(0, 1) → (−1, 0)',-4.4,29,YCOL))

class Shot04(RotationScene):
    shot=3
    def s04(self):
        ax=plane(.6);self.show(ax)
        self.show(txt('P = (2, 1)',4.2,32,GREEN))
        component1=vector(ax,(2,0),GOLD)
        component2=Arrow(ax.c2p(2,0),ax.c2p(2,1),buff=0,color=YCOL,stroke_width=5)
        total=vector(ax,(2,1),GREEN)
        self.show(total)
        self.to(67)
        self.show(component1,component2,math(r'(2,1)=2(1,0)+(0,1)',-3.45,34))
        self.to(72)
        self.play(FadeOut(total),run_time=.3)
        self.play(component2.animate.shift(ax.c2p(0,0)-ax.c2p(2,0)),run_time=.7)
        self.play(Rotate(component1,PI/2,about_point=ax.c2p(0,0)),Rotate(component2,PI/2,about_point=ax.c2p(0,0)),run_time=1.4)
        self.play(component2.animate.shift(ax.c2p(0,2)-ax.c2p(0,0)),run_time=.7)
        self.show(vector(ax,(-1,2),GREEN),txt('새 좌표 (−1, 2)',-4.35,30,GREEN))

class Shot05(RotationScene):
    shot=4
    def s05(self):
        self.show(txt('(1,0) → (0,1)',3.7,32,GOLD),txt('(0,1) → (−1,0)',2.7,32,YCOL))
        matrix=Matrix([[0,-1],[1,0]],element_to_mobject=lambda s:MathTex(s,font_size=48))
        matrix.get_columns()[0].set_color(GOLD);matrix.get_columns()[1].set_color(YCOL);matrix.move_to(UP*.8)
        self.play(TransformFromCopy(self.mobjects[-2],matrix.get_columns()[0]),TransformFromCopy(self.mobjects[-1],matrix.get_columns()[1]),run_time=1)
        self.add(matrix);self.show(txt('각 열 = 기준 방향이 이동한 결과',-.9,27,GREEN))
        self.to(84)
        calculation=math(r'\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2\\1\end{pmatrix}=\begin{pmatrix}-1\\2\end{pmatrix}',-2.7,41)
        self.show(calculation)
        self.to(88)
        self.show(panel('연속된 변환은 행렬 곱으로',-4.15,GREEN))
        self.show(txt('같은 원점 중심의 평면 회전끼리는 가환',4.55,21,MUTED))

class Shot06(RotationScene):
    shot=5
    def s06(self):
        self.show(txt('A = X축 +90°',3.4,35,XCOL),txt('B = Y축 +90°',2.2,35,YCOL))
        self.to(98)
        self.show(math(r'\mathbf v\ \xrightarrow{A}\ A\mathbf v\ \xrightarrow{B}\ B(A\mathbf v)',.3,39))
        self.show(math(r'B(A\mathbf v)=(BA)\mathbf v',-1.5,44,GOLD))
        self.show(panel('열벡터: 오른쪽 행렬이 먼저 작용',-3.35,GREEN,size=27))

class Shot07(RotationScene):
    shot=6
    def s07(self):
        first,second=Book(),Book();first.pose([-2,1.1,0],.8);second.pose([2,1.1,0],.8)
        self.add(world_axes(first),world_axes(second),first,second)
        self.show(txt('A → B',3.65,32,XCOL,x=-2,width=3),txt('B → A',3.65,32,YCOL,x=2,width=3))
        self.show(txt('A = Rx(90°)   B = Ry(90°)',4.55,24,MUTED))
        self.to(106)
        self.turn(first,'X',1.2);self.wait(.3);self.turn(first,'Y',1.2)
        self.to(110)
        self.turn(second,'Y',1.2);self.wait(.3);self.turn(second,'X',1.2)
        self.to(113)
        self.show(math(r'BA\mathbf n_0=-\mathbf e_y',-1.2,30,GOLD,width=3.5).shift(LEFT*2),math(r'AB\mathbf n_0=\mathbf e_x',-1.2,30,GOLD,width=3.5).shift(RIGHT*2))
        self.show(math(r'AB\ne BA',-2.65,53,RED))
        self.to(117)
        self.show(txt('n₀ = (0, 0, 1) : 처음 앞표지 방향',-3.8,26,MUTED))
        self.to(122)
        self.play(Indicate(first.normal,color=GOLD),Indicate(second.normal,color=GOLD))

class Shot08(RotationScene):
    shot=7
    def s08(self):
        self.show(math(r'AB\ne BA',2.5,68,RED))
        self.show(txt('비가환성',.2,60,GOLD),txt('Noncommutativity',-1.2,27,MUTED))
        self.show(panel('순서가 결과에 영향을 준다',-3,GREEN))
        self.to(131)
        self.show(txt('공간의 자세를 계산하는 기본 성질',4.3,26,MUTED))

class Shot09(RotationScene):
    shot=8
    def s09(self):
        # Three original schematic applications, with the same orientation convention.
        robot=VGroup(Line([-2.2,1,0],[-1.2,2.2,0],stroke_width=12,color=YCOL),Line([-1.2,2.2,0],[.2,1.5,0],stroke_width=12,color=XCOL),Dot([-1.2,2.2,0],radius=.15,color=GOLD))
        label=txt('로봇 팔 · 관절 회전의 합성',-.1,32,GREEN)
        self.show(robot,label)
        self.to(137)
        self.play(Rotate(robot[1],PI/3,about_point=[-1.2,2.2,0]),run_time=1)
        self.to(138.5)
        self.play(FadeOut(robot),FadeOut(label),run_time=.4)
        craft=VGroup(Triangle(color=INK,fill_opacity=.2).scale(.8),Rectangle(width=1.8,height=.7,color=YCOL,fill_opacity=.2).shift(LEFT*1.5),Rectangle(width=1.8,height=.7,color=YCOL,fill_opacity=.2).shift(RIGHT*1.5)).move_to(UP*1.4)
        self.show(craft,txt('우주선 · 방향과 자세',-.1,32,GREEN))
        self.play(Rotate(craft,PI/3),run_time=1)
        self.to(142)
        self.play(FadeOut(craft),run_time=.3)
        book=Book(y=2,scale=.8);self.show(book,world_axes(book),txt('컴퓨터 그래픽 · 모델 회전',-1.4,31,GREEN))
        self.turn(book,'X',.75);self.turn(book,'Y',.75)
        self.to(145)
        self.show(panel('회전 명령의 순서까지 계산해야 한다',-3.5,GOLD,size=27))

class Shot10(RotationScene):
    shot=9
    def s10(self):
        self.show(txt('교환법칙은 연산의 성질이다',3.5,37,GOLD))
        self.show(math(r'a+b=b+a',1.9,48,GREEN),math(r'ab=ba',.5,48,GREEN))
        self.to(153)
        self.show(txt('수의 덧셈과 곱셈: 성립',-.9,31,GREEN))
        self.show(math(r'AB\ne BA',-2.5,47,RED),txt('3차원 회전: 항상 성립하지는 않는다',-3.8,28,MUTED))

class Shot11(RotationScene):
    shot=10
    def s11(self):
        self.show(txt('무엇을 계산하는가?',2.5,42,YCOL))
        self.to(162)
        self.show(txt('어떤 규칙을\n만족하는가?',-.2,54,GREEN))
        self.show(txt('연산의 결과에서 연산의 구조로',-3.2,29,GOLD))
        self.to(166)
