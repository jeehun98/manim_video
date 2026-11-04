"""Two fixed coordinate spaces, coefficient scaling, and SVD reconstruction."""
import json,os
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('DOT_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#0B1220'
INK='#EDF4FF';GRAY='#8B9CB6';BLUE='#55ACFF';CYAN='#53D7D0';ORANGE='#FFB45F';YELLOW='#FFD388';GREEN='#55DFA3';PURPLE='#BB97FF';OUT='#8FD8FF'
A=np.array([[0.,-1.],[3.,0.]]);U=np.array([[0.,-1.],[1.,0.]]);SIGMA=np.diag([3.,1.]);V=np.eye(2);X=np.array([2.,1.]);Y=A@X
def txt(s,size=29,color=INK,width=7.8):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
    if m.width>width:m.scale_to_fit_width(width)
    return m
class MatrixWidget(VGroup):
    def __init__(self,values,center,name='',colors=None,size=30):
        super().__init__();rows=len(values);cols=len(values[0]);self.cells={};colors=colors or [INK]*cols
        for i,row in enumerate(values):
            for j,value in enumerate(row):
                cell=txt(str(value),size,colors[j],width=.9).move_to([(j-(cols-1)/2)*1.0,((rows-1)/2-i)*.64,0]);self.cells[i,j]=cell;self.add(cell)
        hx=cols*.5+.13;hy=rows*.32+.08
        for sign in [-1,1]:
            x=sign*hx;self.add(Line([x,-hy,0],[x,hy,0],color=GRAY,stroke_width=2),Line([x,hy,0],[x-sign*.15,hy,0],color=GRAY,stroke_width=2),Line([x,-hy,0],[x-sign*.15,-hy,0],color=GRAY,stroke_width=2))
        if name:self.add(txt(name,25,width=3).move_to([0,hy+.45,0]))
        self.shift(center)
class SVDBase(Scene):
    INDEX=0
    def construct(self):
        self.meta=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.meta['start']
        self.left=np.array([-2.2,2.,0]) if SHORT else np.array([-6.,-.6,0]);self.right=np.array([2.05,.4,0]) if SHORT else np.array([-2.8,-1.65,0]);self.unit=.6 if SHORT else .5
        self.panel=np.array([0,-2.5,0]) if SHORT else np.array([3.65,.3,0]);self.content=VGroup()
        self.xval=ValueTracker(2);self.yval=ValueTracker(1);self.amount=ValueTracker(1);self.tx=ValueTracker(0)
        self.add(txt('DOT PRO   /   LEVEL 08',19,GRAY).move_to([0,7.2 if SHORT else 3.95,0]),txt(self.meta['title'],31,width=8 if SHORT else 14).move_to([0,6.25 if SHORT else 3.15,0]))
        yy=5.65 if SHORT else 2.65;self.add(Line([-3.9 if SHORT else -7,yy,0],[3.9 if SHORT else 7,yy,0],color=GRAY,stroke_opacity=.25))
        labels=['x 입력','v 입력방향','σ 특이값','u 출력방향'];colors=[BLUE,CYAN,YELLOW,GREEN]
        for x,s,c in zip([-3,-1,1,3] if SHORT else [-5.8,-2.9,0,2.9],labels,colors):self.add(txt(s,16,c,width=2.4).move_to([x,5.15 if SHORT else -3.03,0]))
        self.spaces();self.shot();self.to(self.meta['end'])
    def to(self,t):
        self.update_mobjects(0);left=t-self.start-self.time
        if left<-.04:raise RuntimeError((self.INDEX,self.time,t-self.start))
        if left>.001:self.wait(left)
    def pos(self,v,output=False):return (self.right if output else self.left)+self.unit*np.r_[v,0]
    def vec(self,a,b,color=BLUE,output=False,width=5):
        p,q=self.pos(a,output),self.pos(b,output)
        if np.linalg.norm(q-p)<1e-5:return Dot(q,radius=.015,color=color)
        return Arrow(p,q,buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.16)
    def input(self):return np.array([self.xval.get_value(),self.yval.get_value()])
    def spaces(self):
        self.space_group=VGroup()
        for output,center in [(False,self.left),(True,self.right)]:
            xr=(-2.2,1.15) if output else (-.5,3.1);yr=(-.5,6.8) if output else (-.5,3.1)
            self.space_group.add(Line(self.pos([xr[0],0],output),self.pos([xr[1],0],output),color=GRAY,stroke_width=1.5,stroke_opacity=.5),Line(self.pos([0,yr[0]],output),self.pos([0,yr[1]],output),color=GRAY,stroke_width=1.5,stroke_opacity=.5),txt('0',14,GRAY).move_to(center+[-.13,-.16,0]))
            for k in ([1,3,6] if output else [1,2]):
                p=self.pos([0,k],output);self.space_group.add(Line(p+[-.055,0,0],p+[.055,0,0],color=GRAY,stroke_width=1),txt(str(k),13,GRAY,width=.4).move_to(p+[-.18,0,0]))
            x=center[0];self.space_group.add(txt('출력 공간' if output else '입력 공간',21,GRAY,width=3).move_to([x,4.7 if SHORT else 2.22,0]))
        self.add(self.space_group)
    def live_vectors(self,output=True):
        self.iv=always_redraw(lambda:self.vec([0,0],self.input(),BLUE).set_z_index(5));self.add(self.iv)
        if output:self.ov=always_redraw(lambda:self.vec([0,0],A@self.input(),OUT,True).set_z_index(5));self.add(self.ov)
    def basis(self,output=False):
        if output:
            a=self.vec([0,0],[0,1],GREEN,True,6);b=self.vec([0,0],[-1,0],PURPLE,True,6)
            labels=[('u₁',[0,1],GREEN,(.32,.05)),('u₂',[-1,0],PURPLE,(-.2,-.25))]
        else:
            a=self.vec([0,0],[1,0],CYAN,width=6);b=self.vec([0,0],[0,1],CYAN,width=6)
            labels=[('v₁',[1,0],CYAN,(0,-.3)),('v₂',[0,1],CYAN,(-.55,.18))]
        g=VGroup(a,b)
        for s,v,c,off in labels:g.add(txt(s,22,c,width=1).move_to(self.pos(v,output)+[off[0],off[1],0]))
        self.add(g);return g
    def info(self,s,note='',color=INK,size=30):
        self.remove(self.content);self.content=VGroup(txt(s,size,color,width=7.9 if SHORT else 6.7).move_to(self.panel))
        if note:self.content.add(txt(note,22,GRAY,width=7.8 if SHORT else 6.6).next_to(self.content[0],DOWN,buff=.4))
        self.add(self.content)
    def below(self,s,color=INK,offset=-1.6,size=24):
        m=txt(s,size,color,width=7.8 if SHORT else 6.6).move_to(self.panel+[0,offset,0]);self.add(m);return m
    def matrix(self,values,name,offset=0,colors=None):
        m=MatrixWidget(values,self.panel+[0,offset,0],name,colors);self.add(m);return m
    def move_input(self,x,d=1.6):self.play(self.xval.animate.set_value(x[0]),self.yval.animate.set_value(x[1]),run_time=d)
    def flow(self,active=None,offset=-1.6):
        g=VGroup()
        for j,(s,n,c) in enumerate([('Vᵀ','측정',CYAN),('Σ','배율',YELLOW),('U','결합',GREEN)]):
            x=(j-1)*(2.5 if SHORT else 2.0);center=self.panel+[x,offset,0]
            g.add(txt(s,31,c if active is None or active==j else GRAY,width=1.6).move_to(center),txt(n,19,c if active is None or active==j else GRAY,width=1.8).move_to(center+[0,-.5,0]))
            if j<2:g.add(txt('→',24,GRAY,width=.5).move_to(center+[1.25 if SHORT else 1.,0,0]))
        self.add(g);return g
    def final_output(self):
        self.add(self.vec([0,0],[0,6],GREEN,True),self.vec([0,6],[-1,6],PURPLE,True))
        self.add(self.vec([0,0],Y,OUT,True,width=5).set_z_index(6),Dot(self.pos(Y,True),radius=.06,color=OUT))
        self.add(txt('Ax = (−1, 6)',20,OUT,width=2.7).move_to(self.pos(Y,True)+[-.4,.3,0]))
    def hide_spaces(self):self.remove(self.space_group)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.xval.set_value(1);self.yval.set_value(0);self.live_vectors()
            ghosts=VGroup()
            for angle in [30,60,90]:
                x=np.array([np.cos(angle*DEGREES),np.sin(angle*DEGREES)])
                ghosts.add(self.vec([0,0],x,BLUE,width=3).set_opacity(.25),self.vec([0,0],A@x,OUT,True,width=3).set_opacity(.25))
            self.add(ghosts);self.info('행렬은 방향마다 어떻게 반응할까?',color=BLUE);self.to(3)
            self.move_input([.6,.8],2);self.move_input([0,1],2);self.to(8);self.remove(ghosts);self.move_input([1.2,.8],1);self.info('x → A → Ax','길이도 방향도 바뀔 수 있다',OUT);self.to(12);self.move_input([1,0],1.5);self.basis();self.info('특별한 입력 방향을 기준으로 읽자','방향 성분 측정 · 배율 · 출력 방향')
        elif i==1:
            self.live_vectors();self.info('SVD · 특이값 분해','Singular Value Decomposition',BLUE);self.to(21);self.info('A = UΣVᵀ','벡터에 작용하는 순서는 오른쪽부터');f=self.flow();self.to(26);self.remove(f);self.flow(active=0);self.below('입력 → Vᵀ → Σ → U → 출력',GRAY,-2.65,21)
        elif i==2:
            matrix=self.matrix([['?','?'],['?','?']],'A');self.to(31);self.remove(matrix);matrix=self.matrix([[0,'−1'],['','']],'A');self.to(33);self.remove(matrix);matrix=self.matrix([[0,'−1'],[3,0]],'A');self.to(35);self.remove(matrix)
            self.xval.set_value(1);self.yval.set_value(0);self.live_vectors();self.info('A(1, 0) = (0, 3)','오른쪽 단위벡터 → 위쪽 길이 3',GREEN);self.to(41);self.move_input([0,1],1.5);self.info('A(0, 1) = (−1, 0)','위쪽 단위벡터 → 왼쪽 길이 1',PURPLE);self.to(46);self.basis();self.basis(True);self.info('가로 입력 → 위쪽 3배','세로 입력 → 왼쪽 1배',OUT)
        elif i==3:
            self.basis();self.info('v₁ = (1, 0)   v₂ = (0, 1)','서로 직교하고 길이가 1인 입력 방향',CYAN);self.to(54);self.remove(self.content);self.matrix([[1,0],[0,1]],'V = [v₁  v₂]',colors=[CYAN,CYAN]);self.below('이번 예제에서는 V = I₂',GRAY)
        elif i==4:
            self.basis();self.live_vectors(False);self.info('x = (2, 1)','입력 벡터는 그대로 두고 성분을 측정',BLUE);self.to(61)
            p1=self.vec([0,0],[2,0],ORANGE);self.play(Create(p1),run_time=.7);self.info('c₁ = v₁ᵀx = (1, 0) · (2, 1) = 2',color=ORANGE);self.to(64.5)
            p2=self.vec([0,0],[0,1],ORANGE);self.play(Create(p2),run_time=.7);self.info('c₂ = v₂ᵀx = (0, 1) · (2, 1) = 1',color=ORANGE);self.to(68);self.info('Vᵀx = (v₁ᵀx, v₂ᵀx)ᵀ = (2, 1)','숫자가 같은 이유: 이 예제의 V = I₂',CYAN)
        elif i==5:
            self.basis();self.live_vectors(False);self.info('Vᵀx = (2, 1)','아직 출력 방향에 배치하지 않은 성분',ORANGE);self.to(75);self.remove(self.content);m=self.matrix([[3,0],[0,1]],'Σ',colors=[YELLOW,YELLOW]);self.to(78);self.below('σ₁ = 3   ·   σ₂ = 1  (둘 다 0 이상)',YELLOW,-1.6,23);self.to(84);self.remove(m)
            # Scalar bars, deliberately outside the output coordinate space.
            self.amount.set_value(2)
            def bars():
                g=VGroup();base=self.panel+[0,.2,0]
                for j,(v,c,label) in enumerate([(self.amount.get_value(),YELLOW,'첫 성분'),(1,ORANGE,'둘째 성분')]):
                    y=base[1]+.5-j*.9;left=base[0]-2.8;w=v*.7
                    g.add(Rectangle(width=w,height=.28,fill_color=c,fill_opacity=.9,stroke_width=0).move_to([left+w/2,y,0]),txt(f'{label}: {v:.0f}',23,c,width=2.3).move_to([base[0]+2.3,y,0]))
                return g
            self.add(always_redraw(bars));self.play(self.amount.animate.set_value(6),run_time=2);self.below('2 × 3 = 6    /    1 × 1 = 1',YELLOW,-.95,27)
        elif i==6:
            self.basis();self.live_vectors(False);m=self.matrix([[0,'−1'],[1,0]],'U',colors=[GREEN,PURPLE]);self.to(91);self.basis(True);self.to(94);self.remove(m);self.info('u₁ = (0, 1)   u₂ = (−1, 0)','위쪽과 왼쪽: 서로 다른 두 출력 방향',GREEN);self.to(99)
            vertical=self.vec([0,0],[0,6],GREEN,True);self.play(GrowArrow(vertical),run_time=2);self.info('6u₁ = (0, 6)','첫 번째 성분 6을 위쪽으로 배치',GREEN);self.to(102)
            horizontal=self.vec([0,6],[-1,6],PURPLE,True);self.play(GrowArrow(horizontal),run_time=1.3);self.info('6u₁ + u₂ = (0, 6) + (−1, 0)',color=PURPLE);self.to(104)
            result=self.vec([0,0],Y,OUT,True).set_z_index(6);self.play(GrowArrow(result),run_time=1);self.add(txt('Ax = (−1, 6)',20,OUT,width=2.7).move_to(self.pos(Y,True)+[-.4,.3,0]));self.info('Ax = (−1, 6)','왼쪽 출력은 u₂의 방향에서 나온다',OUT)
        elif i==7:
            self.basis();self.live_vectors(False);self.final_output();self.info('Ax = (0×2 − 1×1, 3×2 + 0×1)','직접 계산하면 (−1, 6)',OUT);self.to(113);self.info('Ax = UΣVᵀx = (−1, 6)','같은 결과 · 방향별 작용을 분리해서 해석',OUT);self.flow(offset=-1.65);self.below('(2, 1) → (6, 1) → (−1, 6)',GRAY,-2.75,23)
        elif i==8:
            # A separate valid SVD with a nontrivial rotated input basis.
            a=30*DEGREES;vp=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);ap=U@SIGMA@vp.T
            self.add(self.vec([0,0],X,BLUE),self.vec([0,0],ap@X,OUT,True));self.info('다른 예제 A′ = UΣV′ᵀ','V′: 입력 방향이 30° 회전한 직교기저',CYAN)
            self.add(txt('별도 예제 A′  ·  V′ ≠ I₂',20,GRAY,width=6).move_to([0 if SHORT else -4.3,-.85 if SHORT else -2.45,0]))
            for k in range(2):self.add(self.vec([0,0],vp[:,k],CYAN),txt('v′₁' if k==0 else 'v′₂',19,CYAN,width=1).move_to(self.pos(vp[:,k])+[.12 if k==0 else -.25,.24,0]))
            self.to(123);self.info('Ax = Σᵢ σᵢuᵢ(vᵢᵀx)','일반식: 모든 입력 특이방향의 반응을 더한다');f=self.flow(active=0);self.to(125);self.remove(f);f=self.flow(active=1);self.to(127);self.remove(f);self.flow(active=2)
        elif i==9:
            self.hide_spaces();self.remove(self.content)
            # A centered data distribution, explicitly distinct from a linear map.
            s=np.linspace(-2.4,2.4,16);noise=np.array([.3,-.4,.5,-.2,.3,-.4,.2,-.3,.4,-.3,.2,-.5,.3,-.2,.4,-.3]);noise-=noise.mean();noise-=s*(s@noise)/(s@s);a=35*DEGREES;r=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]);data=np.column_stack([s,noise])@r.T
            center=np.array([0,2,0]) if SHORT else np.array([-4.2,.2,0]);scale=1 if SHORT else .9
            cloud=VGroup(*(Dot(center+scale*np.r_[p,0],radius=.06,color=BLUE) for p in data),Line(center-2.9*scale*np.r_[r[:,0],0],center+2.9*scale*np.r_[r[:,0],0],color=GREEN,stroke_width=3));self.add(cloud);self.info('PCA · 데이터의 분포','투영 분산이 가장 큰 방향',GREEN);self.to(134);self.remove(cloud);self.add(self.space_group);self.xval.set_value(1);self.yval.set_value(0);self.live_vectors();self.info('SVD · 행렬의 방향별 작용','입력 방향 → 배율 → 출력 방향',OUT)
            self.move_input([0,1],1.4);self.move_input([1,0],1.4);self.below('행이 샘플인 중심화 데이터 X의',GRAY,-1.6,20);self.below('오른쪽 특이벡터 = PCA 주성분 방향',GRAY,-2.15,20)
        elif i==10:
            self.basis();self.live_vectors(False);self.info('Vᵀx = (2, 1)','내적으로 방향별 성분 측정',CYAN);f=self.flow(active=0);self.to(142);self.remove(f);self.info('ΣVᵀx = (6, 1)','각 성분에 특이값을 적용',YELLOW);f=self.flow(active=1);self.to(144);self.remove(f);self.final_output();self.info('UΣVᵀx = Ax = (−1, 6)','조절한 성분을 출력 방향으로 결합',OUT);self.flow(active=2)
