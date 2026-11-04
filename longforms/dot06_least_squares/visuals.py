"""3D world geometry with an orthographic camera and a separate readable HUD."""
import os,json
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F';PURPLE='#BB97FF';YELLOW='#FFD388'
O=np.zeros(3);E1=np.array([1.,0,0]);E2=np.array([0.,1,0]);Z=np.array([0.,0,1.]);B=np.array([2.,3,4.]);FOOT=np.array([2.,3.,0.])
def txt(s,size=30,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class MatrixWidget(VGroup):
    def __init__(self,values,center,name='',colors=None,width=6,size=29):
        super().__init__();rows=len(values);cols=len(values[0]);self.cells={};colors=colors or [INK]*cols
        for i,row in enumerate(values):
            for j,value in enumerate(row):
                cell=txt(value,size,colors[j],width=1.2).move_to([(j-(cols-1)/2)*1.05,((rows-1)/2-i)*.65,0]);self.cells[i,j]=cell;self.add(cell)
        halfx=cols*.525+.12;halfy=rows*.325+.12
        for sign in [-1,1]:
            x=sign*halfx;self.add(Line([x,-halfy,0],[x,halfy,0],color=GRAY,stroke_width=2),Line([x,halfy,0],[x-sign*.17,halfy,0],color=GRAY,stroke_width=2),Line([x,-halfy,0],[x-sign*.17,-halfy,0],color=GRAY,stroke_width=2))
        if name:self.add(txt(name,25,INK,width=3.5).move_to([0,halfy+.4,0]))
        if self.width>width:self.scale(width/self.width,about_point=ORIGIN)
        self.shift(np.array(center));self.columns=[VGroup(*(self.cells[i,j] for i in range(rows))) for j in range(cols)]
class LeastSquaresBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.mini=7<=self.INDEX<=9
        self.center=np.array([-.45,1.7,0]) if SHORT and self.mini else np.array([-.5,1.15,0]) if SHORT else np.array([-4.,-.85,0])
        self.scale3=(.74 if self.mini else .9) if SHORT else (.72 if self.mini else .78)
        self.pitch=ValueTracker((16 if self.INDEX==4 else 25)*DEGREES);self.yaw=20*DEGREES
        self.s=ValueTracker(0);self.t=ValueTracker(0);self.error_alpha=ValueTracker(1);self.plane_alpha=ValueTracker(0 if self.INDEX==1 else .18)
        self.panel=np.array([0,-2.55,0]) if SHORT else np.array([3.65,.45,0])
        self.add(txt('DOT PRO   /   LEVEL 06',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],31,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        self.add(Line([-3.9,5.65,0],[3.9,5.65,0],color=GRAY,stroke_opacity=.25) if SHORT else Line([-7,2.65,0],[7,2.65,0],color=GRAY,stroke_opacity=.25))
        for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],['b 목표','a₁,a₂ 기준','Ax 후보','r 잔차'],[BLUE,GREEN,ORANGE,PURPLE]):self.add(txt(s,17,c,width=2.4).move_to([x,5.15 if SHORT else -3.03,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def project(self,v):
        x,y,z=np.array(v);p=self.pitch.get_value();b=self.yaw
        screen=np.array([np.cos(b)*x-np.sin(b)*y,-np.sin(p)*(np.sin(b)*x+np.cos(b)*y)+np.cos(p)*z,0.])
        return self.center+self.scale3*screen
    def arrow3(self,a,b,color,width=5,opacity=1):
        p,q=self.project(a),self.project(b)
        if np.linalg.norm(q-p)<1e-6:return Dot(q,radius=.03,color=color).set_opacity(opacity)
        return Arrow(p,q,buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.13).set_opacity(opacity)
    def label3(self,s,world,color=INK,offset=(.2,.15),size=21,width=3):
        obj=txt(s,size,color,width).set_z_index(10)
        def update(m):m.move_to(self.project(world() if callable(world) else world)+[offset[0],offset[1],0])
        obj.add_updater(update);obj.update(0);self.add(obj);return obj
    def graph(self):
        def plane():
            alpha=self.plane_alpha.get_value();g=VGroup(Polygon(*(self.project(v) for v in [[-1,-1,0],[4,-1,0],[4,4,0],[-1,4,0]]),fill_color='#285977',fill_opacity=alpha,stroke_color=GRAY,stroke_width=1,stroke_opacity=alpha*2))
            for i in range(-1,5):g.add(Line(self.project([i,-1,0]),self.project([i,4,0]),color=GRAY,stroke_width=1,stroke_opacity=alpha),Line(self.project([-1,i,0]),self.project([4,i,0]),color=GRAY,stroke_width=1,stroke_opacity=alpha))
            return g.set_z_index(-5)
        self.surface=always_redraw(plane);self.add(self.surface)
        axes=always_redraw(lambda:VGroup(Line(self.project([-1,0,0]),self.project([4.35,0,0]),color=GRAY,stroke_width=1.5,stroke_opacity=.65),Line(self.project([0,-1,0]),self.project([0,4.35,0]),color=GRAY,stroke_width=1.5,stroke_opacity=.65),Line(self.project([0,0,0]),self.project([0,0,4.0]),color=GRAY,stroke_width=1.5,stroke_opacity=.65)).set_z_index(-3))
        self.add(axes);self.label3('x',[4.35,0,0],GRAY,(.16,0),18,1);self.label3('y',[0,4.35,0],GRAY,(-.18,-.05),18,1);self.label3('z',[0,0,4.0],GRAY,(.1,.17),18,1);self.label3('0',O,GRAY,(-.17,-.13),16,1)
    def basis(self,names=('a₁','a₂')):
        self.a1=always_redraw(lambda:self.arrow3(O,E1,GREEN,6).set_z_index(7));self.a2=always_redraw(lambda:self.arrow3(O,E2,GREEN,6).set_z_index(7));self.add(self.a1,self.a2)
        self.label3(names[0],E1,GREEN,(.27,-.2),19,1.2);self.label3(names[1],E2,GREEN,(-.28,-.22),19,1.2)
    def target(self,coords=False):
        self.b=always_redraw(lambda:self.arrow3(O,B,BLUE,6).set_z_index(3));self.bdot=always_redraw(lambda:Dot(self.project(B),radius=.055,color=BLUE).set_z_index(8));self.add(self.b,self.bdot)
        self.bname=self.label3('b = (2, 3, 4)' if coords else 'b',B,BLUE,(1.0,.2) if coords else (.22,.2),22,3.3)
    def candidate_world(self):return np.array([self.s.get_value(),self.t.get_value(),0.])
    def candidate(self,xy,residual=True,vector=True):
        self.s.set_value(xy[0]);self.t.set_value(xy[1])
        if vector:
            self.cvec=always_redraw(lambda:self.arrow3(O,self.candidate_world(),ORANGE,5,.9).set_z_index(4));self.add(self.cvec)
        self.cdot=always_redraw(lambda:Dot(self.project(self.candidate_world()),radius=.065,color=ORANGE).set_z_index(9));self.add(self.cdot)
        if residual:
            self.error=always_redraw(lambda:self.arrow3(self.candidate_world(),B,PURPLE,5,self.error_alpha.get_value()).set_z_index(5));self.add(self.error)
    def move(self,xy,d):self.play(self.s.animate.set_value(xy[0]),self.t.animate.set_value(xy[1]),run_time=d,rate_func=smooth)
    def distance(self):return float(np.linalg.norm(B-self.candidate_world()))
    def meter(self,squared=False,offset=0,size=38):
        def make():
            value=self.distance()**(2 if squared else 1)
            return txt(('‖r‖²' if squared else '‖r‖')+f' = {value:.2f}',size,PURPLE,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0])
        m=always_redraw(make);self.add(m);return m
    def markers(self):
        def square():
            g=VGroup()
            if np.linalg.norm(self.candidate_world()-FOOT)>1e-5:return g
            for direction in [E1,E2]:
                points=[FOOT+.35*direction,FOOT+.35*direction+.35*Z,FOOT+.35*Z]
                line=VMobject(color=GRAY,stroke_width=2).set_points_as_corners([self.project(v) for v in points]);g.add(line)
            return g.set_z_index(8)
        mark=always_redraw(square);self.add(mark)
        label=self.label3('90°',FOOT+[.4,-.2,.45],GRAY,(.17,0),18,1.2)
        label.add_updater(lambda m:m.set_opacity(1 if np.linalg.norm(self.candidate_world()-FOOT)<1e-5 else 0));label.update(0)
    def optimum(self,coords=False):
        self.basis();self.target(coords);self.candidate([2,3]);self.markers()
        if coords:
            self.label3('p = (2, 3, 0)',FOOT,ORANGE,(1.0,-.25),21,3)
    def info(self,s,note='',color=INK,size=31):
        g=VGroup(txt(s,size,color,width=8 if SHORT else 6.7).move_to(self.panel))
        if note:g.add(txt(note,22,GRAY,width=7.8 if SHORT else 6.6).next_to(g[0],DOWN,buff=.4))
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=g;self.add(g);return g
    def to(self,t):
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError(f'Scene {self.INDEX+1}: {self.time} > {t-self.start}')
        if left>.001:self.wait(left)
    def small_note(self,s,offset=-1.55,color=GRAY):
        return txt(s,21,color,width=7.8 if SHORT else 6.7).move_to(self.panel+[0,offset,0])
    def shot(self):
        i=self.INDEX
        if i==0:
            self.target();self.candidate([-.2,.6]);self.info('정확히 만들 수 없다면?', '얼마나 가까이 갈 수 있을까?',BLUE);self.to(4)
            self.move([1.2,1.5],2);self.info('내적 + 정사영', '주어진 공간 안에서 가까운 답 찾기',ORANGE)
        elif i==1:
            self.info('3차원 공간의 두 방향', 'x축 방향 · y축 방향',GREEN);self.to(10)
            self.basis();self.info('a₁ = (1, 0, 0)', 'a₂ = (0, 1, 0)',GREEN);self.to(16)
            self.candidate([0,0],False);self.info('c₁a₁ + c₂a₂ = (c₁, c₂, 0)', '계수는 바뀌어도 세 번째 성분은 0',ORANGE)
            self.move([3,.5],2);self.move([.6,3.4],2);self.to(20)
            self.info('z = 0', 'z 방향으로는 움직일 수 없다',ORANGE);self.move([2.7,2],2);self.to(23)
            self.play(self.plane_alpha.animate.set_value(.18),run_time=1.3)
            self.info('span{a₁, a₂} = {(s, t, 0)}', '두 방향이 만드는 xy평면 전체',GREEN)
        elif i==2:
            self.basis();self.target(True);self.candidate([-.2,.2],False)
            self.info('목표 b = (2, 3, 4)', '평면 밖에 놓인 목표',BLUE);self.to(31)
            self.info('후보는 언제나 (c₁, c₂, 0)', '두 벡터의 조합으로는 높이를 바꿀 수 없다',ORANGE)
            self.move([3.6,1],2);self.move([1,3.6],2);self.to(35)
            self.info('후보 z = 0   /   목표 z = 4', '정확하게 같아질 수 없다',BLUE);self.to(38)
            self.info('평면 위에서 가장 가까운 벡터는?', '정확한 일치 → 오차를 최소화하는 결과',ORANGE)
        elif i==3:
            self.basis();self.target();self.candidate([-.4,.5],False,False);self.info('평면 위에서 후보를 선택한다', '후보는 (s, t, 0)',ORANGE);self.to(45)
            self.error=always_redraw(lambda:self.arrow3(self.candidate_world(),B,PURPLE,5).set_z_index(5));self.add(self.error);self.remove(self.inf)
            self.meter();note=self.small_note('후보에서 목표까지의 실제 3차원 거리',-.95);self.add(note);self.to(48)
            self.move([3.7,.8],2);self.move([.7,4],2);self.to(52)
            self.move([2,3],5);self.to(57)
            self.markers();self.play(self.pitch.animate.set_value(16*DEGREES),run_time=1)
            self.remove(note);self.add(self.small_note('최단거리 4  /  오차는 평면에 수직',-.95))
        elif i==4:
            self.basis();self.target();self.candidate([2,3],True,False);self.info('왜 수직이어야 할까?', '최적 위치에서 조금 벗어나 보자',PURPLE)
            self.move([-.1,3.6],1);self.to(62)
            horizontal=always_redraw(lambda:self.arrow3(self.candidate_world(),FOOT,YELLOW,5).set_z_index(6))
            vertical=always_redraw(lambda:self.arrow3(FOOT,B,PURPLE,6).set_z_index(6));self.add(horizontal,vertical);self.error_alpha.set_value(.35);self.error.update(0)
            self.info('평면 방향의 오차가 남아 있다면', '그 성분을 따라 움직여 더 가까워질 수 있다',YELLOW);self.to(69)
            self.move([2,3],4);self.markers();self.to(73)
            self.info('직교 정사영', '평면 방향의 오차가 남지 않는 위치',ORANGE)
        elif i==5:
            self.optimum(True);self.info('p = (2, 3, 0)', '목표를 평면에 정사영한 벡터',ORANGE);self.to(79)
            self.info('r = b − p = (0, 0, 4)', '후보 끝점에서 목표까지의 잔차',PURPLE)
            self.label3('r',lambda:(B+FOOT)/2,PURPLE,(.25,0),24,1);self.to(84)
            self.info('(1, 0, 0) · (0, 0, 4) = 0', 'a₁ · r = 0',GREEN);self.to(87)
            self.info('(0, 1, 0) · (0, 0, 4) = 0', 'a₂ · r = 0',GREEN);self.to(91)
            self.info('a₁ · r = 0    a₂ · r = 0', '오차는 평면의 모든 방향과 직교한다',PURPLE)
        elif i==6:
            self.optimum();self.info('최소제곱법', 'Least Squares',ORANGE,size=40);self.meter(True,-1.5,31)
            self.move([3.6,1.6],2);self.move([2,3],2)
        elif i==7:
            self.optimum();a=MatrixWidget([['1','0'],['0','1'],['0','0']],[0,-3.0,0] if SHORT else [3.6,.15,0],name='A',colors=[GREEN,GREEN],width=5)
            self.add(a)
            for vector,col in zip([self.a1,self.a2],a.columns):
                temporary=col.copy();self.play(TransformFromCopy(vector,temporary),run_time=1);self.remove(temporary)
            self.to(105);self.remove(a)
            ca=[-1.4,-2.9,0] if SHORT else [2.2,.15,0];cx=[1.6,-2.9,0] if SHORT else [5.35,.15,0]
            a=MatrixWidget([['1','0'],['0','1'],['0','0']],ca,'A',[GREEN,GREEN],width=2.8)
            x=MatrixWidget([['c₁'],['c₂']],cx,'x',[ORANGE],width=2.2)
            sign=txt('×',29,INK).move_to([.35,-2.9,0] if SHORT else [3.9,.15,0]);self.add(a,x,sign)
            note=self.small_note('Ax = c₁a₁ + c₂a₂ = (c₁, c₂, 0)',-2.0,ORANGE);self.add(note);self.to(110)
            self.remove(a,x,sign,note);self.info('r = b − Ax', '목표와 만들 수 있는 결과의 차이',PURPLE);self.move([1.1,2],2);self.to(116)
            self.info('minₓ ‖Ax − b‖²', '오차 벡터 길이의 제곱을 최소화',ORANGE,size=37)
            self.add(self.small_note('A: 3×2    x: 2×1    b: 3×1'))
        elif i==8:
            self.optimum();self.info('a₁ᵀr = 0    a₂ᵀr = 0', '최적 잔차는 A의 모든 열과 직교',PURPLE);self.to(124)
            self.info('Aᵀ(b − Ax) = (0, 0)ᵀ', 'Aᵀ의 각 행이 한 방향과의 내적을 계산',PURPLE);self.to(129)
            self.info('Aᵀb − AᵀAx = 0', '직교 조건을 전개하면');self.to(131)
            self.info('AᵀAx = Aᵀb', '정규방정식 · Normal Equations',ORANGE,size=38)
        elif i==9:
            self.basis(('q₁','q₂'));self.target();self.candidate([2,3]);self.markers()
            self.info('A = QR', '축약 QR: Q는 3×2, R은 2×2',ORANGE,size=42);self.to(140)
            self.remove(self.inf)
            q=MatrixWidget([['1','0'],['0','1'],['0','0']],[-1.6,-2.9,0] if SHORT else [2.0,.15,0],'Q = A',[GREEN,GREEN],width=3)
            r=MatrixWidget([['1','0'],['0','1']],[1.65,-2.9,0] if SHORT else [5.35,.15,0],'R = I₂',[ORANGE,ORANGE],width=3)
            self.add(q,r);note=self.small_note('이미 직교정규인 두 열  /  QᵀQ = I₂',-2.05,GREEN);self.add(note);self.to(144)
            self.remove(q,r,note);self.info('Qᵀb = (2, 3)ᵀ', 'q₁ᵀb = 2    q₂ᵀb = 3',ORANGE)
            first=self.arrow3(O,[2,0,0],ORANGE,6).set_z_index(6);second=self.arrow3([2,0,0],FOOT,ORANGE,6).set_z_index(6)
            self.play(GrowArrow(first),run_time=2);self.play(GrowArrow(second),run_time=2);self.to(151)
            self.info('Rx = Qᵀb  →  x = (2, 3)ᵀ', 'R = I₂ 이므로 최적 계수는 2와 3',ORANGE)
            self.add(self.small_note('Ax = (2, 3, 0) = p',-1.65,ORANGE))
        else:
            self.optimum();self.info('주어진 공간 안에서 가장 가까운 결과', '평면 안에서 움직여도 최적보다 가까워지지 않는다',ORANGE)
            meter=self.meter(False,-1.5,31);self.move([2.7,2.5],2);self.move([1.4,3.7],2);self.move([2,3],3);self.to(165)
            self.remove(meter);self.info('Aᵀ(b − Ax) = 0', '가장 가까운 결과에서 오차는 모든 허용 방향과 직교',PURPLE,size=36)
