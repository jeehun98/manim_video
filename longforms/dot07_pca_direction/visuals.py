"""PCA geometry: fixed data, rotating unit direction, exact energy accounting."""
import os,json
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9
config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';GREEN='#55DFA3';ORANGE='#FFB45F';PURPLE='#BB97FF'
S=np.array([-2.7,-2.4,-2.1,-1.7,-1.3,-.9,-.5,-.2,.3,.7,1.0,1.4,1.8,2.2,2.5,2.8]);S-=S.mean()
N=np.array([.4,-.6,.5,-.3,.7,-.5,.2,-.6,.6,-.4,.5,-.7,.3,-.4,.6,-.2]);N-=N.mean();N-=S*np.dot(S,N)/np.dot(S,S);N*=.75
ROT=np.array([[np.cos(35*DEGREES),-np.sin(35*DEGREES)],[np.sin(35*DEGREES),np.cos(35*DEGREES)]])
DATA=np.column_stack([S,N])@ROT.T;MEAN=np.array([.55,.3]);COV=DATA.T@DATA/len(DATA)
EVAL,EVEC=np.linalg.eigh(COV);OPT=float(np.arctan2(EVEC[1,-1],EVEC[0,-1])%PI);TOTAL=float(np.sum(DATA**2));K=14
def txt(s,size=29,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class PCABase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.center=np.array([0,1.4,0]) if SHORT else np.array([-4,0,0]);self.unit=.95 if SHORT else .78
        self.panel=np.array([0,-2.65,0]) if SHORT else np.array([3.6,.3,0])
        self.theta=ValueTracker(10*DEGREES);self.translation=ValueTracker(1 if self.INDEX<3 else 0)
        self.proj_alpha=ValueTracker(0);self.res_alpha=ValueTracker(0);self.cloud_alpha=ValueTracker(1)
        self.add(txt('DOT PRO   /   LEVEL 07',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],31,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        y=5.65 if SHORT else 2.65;self.add(Line([-3.9 if SHORT else -7,y,0],[3.9 if SHORT else 7,y,0],color=GRAY,stroke_opacity=.25))
        for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],['x 데이터','u 방향','p 정사영','r 잔차'],[BLUE,GREEN,ORANGE,PURPLE]):self.add(txt(s,17,c,width=2.4).move_to([x,5.15 if SHORT else -3.03,0]))
        self.graph();self.shot();self.to(self.meta['end'])
    def to(self,t):
        # Cairo may freeze a wait; materialize tracker changes before that wait.
        self.update_mobjects(0)
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError((self.INDEX,self.time,t-self.start))
        if left>.001:self.wait(left)
    def u(self):return np.array([np.cos(self.theta.get_value()),np.sin(self.theta.get_value())])
    def shift(self):return self.translation.get_value()*MEAN
    def xy(self,v):return self.center+self.unit*np.r_[v,0]
    def foot(self,x):return np.dot(x,self.u())*self.u()
    def energy(self):
        v=float(np.sum((DATA@self.u())**2));return TOTAL-v,v
    def graph(self):
        self.add(Line(self.xy([-3.8,0]),self.xy([3.8,0]),color=GRAY,stroke_width=1,stroke_opacity=.4),Line(self.xy([0,-3.1]),self.xy([0,3.1]),color=GRAY,stroke_width=1,stroke_opacity=.4),txt('0',16,GRAY).move_to(self.xy([-.16,-.2])))
        self.line=always_redraw(lambda:Line(self.xy(self.shift()-3.15*self.u()),self.xy(self.shift()+3.15*self.u()),color=GREEN,stroke_width=2,stroke_opacity=.65))
        self.add(self.line)
        self.dots=always_redraw(lambda:VGroup(*(Dot(self.xy(x+self.shift()),radius=.067,color=BLUE).set_opacity(self.cloud_alpha.get_value()) for x in DATA)).set_z_index(5))
        self.projections=always_redraw(lambda:VGroup(*(Dot(self.xy(self.foot(x)+self.shift()),radius=.05,color=ORANGE) for x in DATA)).set_opacity(self.proj_alpha.get_value()).set_z_index(4))
        self.residuals=always_redraw(lambda:VGroup(*(DashedLine(self.xy(self.foot(x)+self.shift()),self.xy(x+self.shift()),color=PURPLE,stroke_width=2,dash_length=.07) for x in DATA)).set_opacity(self.res_alpha.get_value()).set_z_index(2))
        self.add(self.residuals,self.projections,self.dots)
    def show_projection(self,res=True):self.proj_alpha.set_value(1);self.res_alpha.set_value(.65 if res else 0)
    def direction(self):
        self.add(always_redraw(lambda:Arrow(self.xy(self.shift()),self.xy(self.shift()+self.u()),buff=0,color=GREEN,stroke_width=6,max_tip_length_to_length_ratio=.18).set_z_index(8)))
        self.add(always_redraw(lambda:txt('u',22,GREEN,width=1).move_to(self.xy(self.shift()+self.u())+[.1,.28,0])))
    def turn(self,angle,d=2):self.play(self.theta.animate.set_value(angle),run_time=d,rate_func=smooth)
    def info(self,s,note='',color=INK,size=31):
        if hasattr(self,'inf'):self.remove(self.inf)
        self.inf=VGroup(txt(s,size,color,width=8 if SHORT else 6.7).move_to(self.panel))
        if note:self.inf.add(txt(note,22,GRAY,width=7.8 if SHORT else 6.6).next_to(self.inf[0],DOWN,buff=.4))
        self.add(self.inf)
    def triangle(self):
        self.cloud_alpha.set_value(.25);x=DATA[K]
        self.add(Dot(self.xy(x),radius=.085,color=BLUE),Arrow(self.xy([0,0]),self.xy(x),buff=0,color=BLUE,stroke_width=5,max_tip_length_to_length_ratio=.1))
        self.add(always_redraw(lambda:Arrow(self.xy([0,0]),self.xy(self.foot(x)),buff=0,color=ORANGE,stroke_width=5,max_tip_length_to_length_ratio=.12)))
        self.add(always_redraw(lambda:Arrow(self.xy(self.foot(x)),self.xy(x),buff=0,color=PURPLE,stroke_width=5,max_tip_length_to_length_ratio=.15)))
        def corner():
            f=self.foot(x);v=x-f;v=v/np.linalg.norm(v);u=self.u();p=[f-.18*u,f-.18*u+.18*v,f+.18*v]
            return VMobject(color=INK,stroke_width=2).set_points_as_corners([self.xy(z) for z in p])
        self.add(always_redraw(corner))
        self.add(txt('xᵢ',23,BLUE).move_to(self.xy(x)+[.28,.2,0]))
        self.add(always_redraw(lambda:txt('pᵢ',23,ORANGE).move_to(self.xy(self.foot(x)/2)+[0,-.3,0])))
        self.add(always_redraw(lambda:txt('rᵢ',23,PURPLE).move_to(self.xy((x+self.foot(x))/2)+[.32,0,0])))
    def meter(self):
        base=self.panel+[0,-.3,0];w=7.1 if SHORT else 6.0
        def draw():
            e,v=self.energy();g=VGroup();left=base[0]-w/2
            for start,length,color in [(left,w*v/TOTAL,ORANGE),(left+w*v/TOTAL,w*e/TOTAL,PURPLE)]:
                if length>.00001:g.add(Rectangle(width=length,height=.3,stroke_width=0,fill_color=color,fill_opacity=1).move_to([start+length/2,base[1],0]))
            g.add(txt(f'보존 V = {v:.2f}',22,ORANGE,width=3.3).move_to(base+[-w/4,.6,0]),txt(f'잔차 E = {e:.2f}',22,PURPLE,width=3.3).move_to(base+[w/4,.6,0]),txt(f'T = E + V = {TOTAL:.2f}  ·  일정',22,GRAY,width=6.5).move_to(base+[0,-.65,0]))
            return g
        self.add(always_redraw(draw))
    def below(self,s,color=INK,offset=-1.65):self.add(txt(s,25,color,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0]))
    def shot(self):
        i=self.INDEX
        if i==0:
            self.info('여러 점 → 하나의 숫자씩', '어떤 방향을 선택해야 할까?',BLUE);self.to(5);self.show_projection();self.turn(55*DEGREES,2);self.info('내적 + 정사영', '원래 데이터를 잘 보존하는 방향',ORANGE)
        elif i==1:
            self.info('같은 데이터 · 다른 표현', '파란 점은 그대로 유지',BLUE);self.to(12);self.show_projection();self.info('직선 위 위치 = 숫자 하나','선 밖 성분은 사라진다',ORANGE);self.to(18);self.turn(65*DEGREES,2);self.info('방향에 따라 달라지는 잔차', '보라색 선: 제거된 성분',PURPLE);self.to(22)
            self.turn(0,2);self.info('수평 투영 → 세로 성분 제거',color=ORANGE);self.to(25);self.turn(90*DEGREES,2);self.info('수직 투영 → 가로 성분 제거',color=ORANGE)
        elif i==2:
            self.theta.set_value(90*DEGREES);self.show_projection();self.info('가장 잘 보존하는 방향은?', '먼저 데이터의 중심을 맞춘다');self.to(33)
            self.proj_alpha.set_value(0);self.res_alpha.set_value(0)
            self.add(always_redraw(lambda:Dot(self.xy(self.shift()),radius=.09,color=ORANGE)),always_redraw(lambda:txt('평균',21,ORANGE).move_to(self.xy(self.shift())+[.4,-.3,0])))
            self.info('xᵢ ← xᵢ − 평균', '모든 점을 같은 거리·방향으로 이동',BLUE);self.play(self.translation.animate.set_value(0),run_time=4);self.info('중심화 완료', '데이터 평균 = (0, 0)',BLUE)
        elif i==3:
            self.direction();self.info('‖u‖ = 1','기준은 길이가 1인 방향벡터',GREEN);self.to(41);self.triangle();self.info('cᵢ = xᵢ · u','내적: 방향 성분을 숫자로 측정',GREEN);self.to(46);self.info('pᵢ = cᵢu = (xᵢ · u)u','숫자 × 단위방향 = 정사영 벡터',ORANGE);self.to(50);self.info('rᵢ = xᵢ − pᵢ','제거된 성분: 정사영에서 원래 점까지',PURPLE)
        elif i==4:
            self.direction();self.show_projection();self.info('E(u) = Σᵢ ‖rᵢ‖²','모든 잔차의 길이를 제곱해 더한다',PURPLE);self.turn(65*DEGREES,2);self.to(60);self.info('어떤 방향에서 E가 최소일까?', '직교하는 두 성분의 관계를 보자',PURPLE)
        elif i==5:
            self.direction();self.triangle();self.info('xᵢ = pᵢ + rᵢ','pᵢ ⟂ rᵢ',BLUE);self.to(67);self.info('‖xᵢ‖² = ‖pᵢ‖² + ‖rᵢ‖²','직각삼각형의 피타고라스 정리');self.to(73);self.info('‖rᵢ‖² = ‖xᵢ‖² − ‖pᵢ‖²','원래 길이 제곱 − 보존한 길이 제곱',PURPLE)
        elif i==6:
            self.direction();self.show_projection();self.meter();self.below('E = T − V',offset=-1.65);self.to(82);self.turn(75*DEGREES,2);self.to(85);self.turn(OPT,4);self.below('잔차 최소 ↔ 보존 성분 최대',GREEN,offset=-2.25)
        elif i==7:
            self.direction();self.show_projection();self.theta.set_value(OPT)
            self.info('‖pᵢ‖ = |xᵢ · u|','음수 성분도 제곱하면 보존량에 포함',ORANGE)
            for k in [1,14]:
                c=float(DATA[k]@self.u());self.add(txt(f'c = {c:+.2f}',20,ORANGE,width=2).move_to(self.xy(self.foot(DATA[k]))+[0,-.37 if k==1 else .35,0]))
            self.to(96);self.info('평균(cᵢ) = 0','평균(xᵢ) = 0  →  평균(xᵢ · u) = 0',GREEN);self.to(99);self.info('Var(c) = (1/n) Σᵢ cᵢ² = V/n','중심화된 내적값의 분산',ORANGE);self.below(f'n = 16  ·  최적 분산 = {EVAL[-1]:.3f}',GRAY)
        elif i==8:
            self.direction();self.show_projection();self.theta.set_value(75*DEGREES);self.meter();self.below('오차 최소 = 투영 분산 최대',GREEN);self.turn(OPT,4);self.to(111);self.below('PCA · 주성분 분석',INK,-2.25)
        elif i==9:
            self.direction();self.show_projection();self.theta.set_value(OPT);self.info('최적 방향은 어떻게 구할까?', '데이터의 퍼짐을 행렬에 담는다',GREEN);self.to(117)
            self.info('Σ = (1/n) Σᵢ xᵢxᵢᵀ','Var(x · u) = uᵀΣu',BLUE)
            mat=f'Σ = [ {COV[0,0]:.3f}    {COV[0,1]:.3f} ]\n       [ {COV[1,0]:.3f}    {COV[1,1]:.3f} ]';self.below(mat,GRAY,-1.8);self.to(123)
            self.remove(self.inf);self.info('Σu₁ = λ₁u₁','‖u₁‖ = 1  ·  λ₁ = 가장 큰 고윳값',GREEN);self.below(f'λ₁ = {EVAL[-1]:.3f}  >  λ₂ = {EVAL[0]:.3f}',GREEN,-2.6)
        elif i==10:
            self.direction();self.show_projection();self.theta.set_value(OPT);self.info('u₁ · 첫 번째 주성분',f'데이터가 가장 넓게 퍼지는 방향 · {OPT/DEGREES:.0f}°',GREEN);self.to(131)
            self.info('최소제곱법: 공간을 고정','주어진 공간 안에서 가까운 결과 찾기',ORANGE)
            # A fixed plane, a target above it, and its perpendicular foot.
            anchor=self.panel+[0,-1.9,0]
            g=VGroup(Polygon(anchor+[-1.8,-.25,0],anchor+[.8,-.25,0],anchor+[1.6,.3,0],anchor+[-1,.3,0],fill_color=GREEN,fill_opacity=.15,stroke_color=GREEN,stroke_width=1),Dot(anchor,radius=.06,color=ORANGE),Dot(anchor+[0,.9,0],radius=.06,color=BLUE),Line(anchor,anchor+[0,.9,0],color=PURPLE,stroke_width=3),txt('고정 평면 · 목표까지 수직 잔차',18,GRAY,width=5).move_to(anchor+[0,-.65,0]));self.add(g);self.to(137)
            self.remove(g);self.info('PCA: 공간의 방향을 선택','여러 데이터를 함께 가장 잘 표현하는 직선',GREEN);self.turn(65*DEGREES,1);self.turn(OPT,2)
        elif i==11:
            self.direction();self.show_projection();self.theta.set_value(OPT);self.meter();self.below('측정 cᵢ = xᵢ · u₁',GREEN,-1.65);self.below('복원 pᵢ = cᵢu₁',ORANGE,-2.25)
