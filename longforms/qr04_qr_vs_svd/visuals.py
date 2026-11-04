"""One actual 2×2 map, ordered output QR basis, and input/output SVD bases."""
import json,os,textwrap
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('BATTLE_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#0B1120'
INK='#EEF4FF';MUTED='#91A4BF';BLUE='#55AEFF';GREEN='#59DFAC';ORANGE='#FFB15A';PURPLE='#BB97FF';TEAL='#60DFD0'
def rot(t):return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
Q=rot(PI/6);R=np.array([[2.,1],[0,1]]);A=Q@R
S=np.sqrt(np.array([3+np.sqrt(5),3-np.sqrt(5)]))
v1=np.array([1.,(S[0]**2-4)/2]);v1/=np.linalg.norm(v1);V=np.column_stack([v1,[-v1[1],v1[0]]]);U=A@V@np.diag(1/S)
VA=np.arctan2(V[1,0],V[0,0]);UA=np.arctan2(U[1,0],U[0,0])
def label(s,size=27,color=INK,width=7.5):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class ComparisonBase(Scene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.m['start'];self.end=self.m['end']
        self.center=np.array([-1.,.5,0]) if SHORT else np.array([-3.8,-.2,0]);self.scale2=1.7 if SHORT else 1.1
        self.add(label('QR 기하학 / 04     QR과 SVD',20,MUTED).move_to([0,7.35 if SHORT else 3.95,0]),label(self.m['title'],34,INK,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.1,0]))
        self.add(Line([-3.9,5.7,0],[3.9,5.7,0],color=MUTED,stroke_opacity=.22) if SHORT else Line([-7,2.55,0],[7,2.55,0],color=MUTED,stroke_opacity=.22))
        self.cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));self.capindex=-1
        cap=VGroup()
        def update_caption(m,dt=0):
            now=self.start+self.time
            idx=next((j for j,c in enumerate(self.cues) if c['start']<=now<c['end']),len(self.cues)-1)
            if idx!=self.capindex:
                s='\n'.join(textwrap.wrap(self.cues[idx]['caption'],width=29 if SHORT else 56,break_long_words=True))
                m.become(VGroup(label(s,25 if SHORT else 24,INK,8 if SHORT else 14).move_to([0,-6.4 if SHORT else -3.5,0])));self.capindex=idx
        update_caption(cap);cap.add_updater(update_caption);self.add(cap)
        self.add(label('같은 A · 입력 특이방향 v · 출력 특이방향 u',18,MUTED,8 if SHORT else 14).move_to([0,-7.4 if SHORT else -4.1,0]))
        self.shot();self.to(self.end)
    def pos(self,v,center=None,scale=None):return (self.center if center is None else np.array(center))+(self.scale2 if scale is None else scale)*np.array([v[0],v[1],0.])
    def put(self,*ms):self.add(*ms)
    def animate(self,*a,d=1):self.play(*a,run_time=d)
    def to(self,t):
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError(f'Overflow {self.INDEX+1}: {self.time} > {t-self.start}')
        if left>.001:self.wait(left)
    def axes(self,center=None,scale=None,size=2.3):
        return VGroup(*(Line(self.pos(-size*v,center,scale),self.pos(size*v,center,scale),color=MUTED,stroke_width=1,stroke_opacity=.22) for v in [np.array([1,0]),np.array([0,1])]))
    def vec(self,v,col,name='',origin=np.zeros(2),center=None,scale=None,offset=(.15,.2)):
        p=self.pos(origin,center,scale);end=self.pos(origin+v,center,scale)
        g=VGroup(Arrow(p,end,buff=0,color=col,stroke_width=4,max_tip_length_to_length_ratio=.16))
        if name:g.add(label(name,23,col,2.5).move_to(end+[offset[0],offset[1],0]))
        return g
    def curve(self,M,center=None,scale=None,color=TEAL):
        ts=np.linspace(0,TAU,121);g=VMobject(color=color,stroke_width=3)
        return g.set_points_as_corners([self.pos(M@np.array([np.cos(t),np.sin(t)]),center,scale) for t in ts])
    def info(self,s,note='',color=INK,dual=False,low=False):
        pos=[0,-4.4 if low else -3.55,0] if SHORT else [0,-2.3,0] if dual else [3.7,-1.45 if low else .3,0]
        eq=label(s,31,color,8 if SHORT else 13 if dual else 6.5).move_to(pos);self.put(eq)
        if note:self.put(label(note,22,MUTED,8 if SHORT else 13 if dual else 6.5).next_to(eq,DOWN,buff=.32))
        return eq
    def matrix(self,svd=False,center=None):
        c=np.array(center) if center is not None else np.array([0.,-2.25,0]) if SHORT else np.array([3.7,.6,0])
        vals=[['σ₁','0'],['0','σ₂']] if svd else [['r₁₁','r₁₂'],['0','r₂₂']]
        cells={};g=VGroup(label('Σ =' if svd else 'R =',29,TEAL if svd else PURPLE).move_to(c+[-1.9,0,0]))
        for i in range(2):
            for j in range(2):
                col=BLUE if svd and i==j==0 else ORANGE if svd and i==j==1 else PURPLE if not svd and i==0 and j==1 else INK if i==j else MUTED
                cells[i,j]=label(vals[i][j],30,col,1).move_to(c+[(j-.5)*1.3,(.5-i)*.85,0]);g.add(cells[i,j])
        for x in [-1.25,1.25]:g.add(Line(c+[x,-.85,0],c+[x,.85,0],color=MUTED,stroke_width=2))
        self.put(g);return cells
    def qr(self,first=True,second=True,basis=True):
        self.put(self.axes())
        if first:self.put(self.vec(A[:,0],INK,'a₁',offset=(.15,.3)))
        if second:self.put(self.vec(A[:,1],INK,'a₂',offset=(-.3,.25)))
        if basis:
            self.put(self.vec(Q[:,0],BLUE,'q₁',offset=(.15,-.3)),self.vec(Q[:,1],GREEN,'q₂',offset=(-.3,.1)))
    def input_output(self,bases=True,stretched=True):
        centers=[np.array([-2.1,1.1,0]),np.array([2.1,1.1,0])] if SHORT else [np.array([-3.8,-.1,0]),np.array([3.8,-.1,0])]
        scale=.8 if SHORT else .95
        self.put(self.axes(centers[0],scale,1.3),self.axes(centers[1],scale,2.5),self.curve(np.eye(2),centers[0],scale,MUTED),self.curve(A,centers[1],scale,TEAL))
        y=3.75 if SHORT else 2.15
        self.put(label('입력 공간 · V',24,INK,3.5).move_to([centers[0][0],y,0]),label('출력 공간 · U',24,TEAL,3.5).move_to([centers[1][0],y,0]))
        if bases:
            for j,col in enumerate([BLUE,ORANGE]):
                self.put(self.vec(V[:,j],col,['v₁','v₂'][j],center=centers[0],scale=scale),self.vec((S[j] if stretched else 1)*U[:,j],col,['σ₁u₁','σ₂u₂'][j] if stretched else ['u₁','u₂'][j],center=centers[1],scale=scale))
        return centers,scale
    def ellipse(self,axes=True):
        self.center=np.array([0.,1.,0]) if SHORT else np.array([-3.7,-.1,0]);self.scale2=1.5 if SHORT else 1.05
        if SHORT and self.INDEX==22:self.center=np.array([0.,1.4,0]);self.scale2=1.25
        self.put(self.axes(),self.curve(A))
        if axes:
            for j,col in enumerate([BLUE,ORANGE]):
                self.put(Line(self.pos(-S[j]*U[:,j]),self.pos(S[j]*U[:,j]),color=col,stroke_width=3))
    def comparison(self,detail=False,footer=True):
        xs=[-2.1,2.1] if SHORT else [-3.8,3.8]
        for x,title,eq,col in zip(xs,['QR','SVD'],['A = QR','A = UΣVᵀ'],[PURPLE,TEAL]):
            self.put(label(title,35,col).move_to([x,3.3 if SHORT else 1.65,0]),label(eq,31,col,3.8 if SHORT else 6).move_to([x,2.3 if SHORT else .75,0]))
        if detail:
            self.matrix(False,[xs[0]+.3,.0 if SHORT else -.7,0]);self.matrix(True,[xs[1]+.3,.0 if SHORT else -.7,0])
        if footer:self.info('열벡터의 순서와 조합  /  특이방향과 확대율',dual=True,color=INK)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.comparison(True,footer=False);self.info('위삼각 구조와 대각 구조, 왜 다를까?',dual=True,low=True)
        elif i==1:self.comparison();self.put(label('열벡터의 순서  ↔  변환의 확대 방향',27,INK,8 if SHORT else 13).move_to([0,.5 if SHORT else -.7,0]))
        elif i==2:
            self.qr(basis=False);self.put(Polygon(*[self.pos(v) for v in [np.zeros(2),A[:,0],A[:,0]+A[:,1],A[:,1]]],color=PURPLE,fill_opacity=.08,stroke_width=1));self.info('A = [ a₁  a₂ ]','동일한 선형독립 행렬을 두 방식으로 분해')
        elif i==3:
            self.qr(second=False,basis=False);t=ValueTracker(2)
            self.put(always_redraw(lambda:self.vec(Q[:,0]*t.get_value(),BLUE,'q₁',offset=(.15,-.3))))
            self.animate(t.animate.set_value(1),d=1.5);self.info('q₁ = a₁ / ‖a₁‖','첫 번째 열의 방향 유지 · 길이만 1로')
        elif i==4:
            self.qr();proj=self.vec(Q[:,0],PURPLE,'',offset=(.2,-.2));self.put(proj)
            t=ValueTracker(1);res=always_redraw(lambda:self.vec(Q[:,1],GREEN,'',origin=Q[:,0]*t.get_value()));self.put(res)
            self.animate(FadeOut(proj),t.animate.set_value(0),d=2)
            self.info('u₂ = a₂ − (q₁ᵀa₂)q₁','수직 잔여 방향을 정규화 → q₂',GREEN)
        elif i==5:
            self.qr();self.animate(Create(Line(self.pos(-1.2*Q[:,0]),self.pos(2.2*Q[:,0]),color=BLUE)),d=.8)
            self.put(Polygon(*[self.pos(v) for v in [-Q[:,0]-Q[:,1],2*Q[:,0]-Q[:,1],2*Q[:,0]+Q[:,1],-Q[:,0]+Q[:,1]]],color=GREEN,fill_opacity=.04,stroke_opacity=.25))
            self.info('span(a₁) = span(q₁)','첫 직선을 유지하며 두 번째 독립 방향 추가')
        elif i in [6,7,21]:
            self.qr();self.put(self.vec(Q[:,0],PURPLE,''),label('r₁₂q₁',23,PURPLE).move_to(self.pos(.55*Q[:,0])+[.2,-.65,0]),self.vec(Q[:,1],GREEN,'',origin=Q[:,0]))
            if i==6:self.info('a₂ = r₁₂q₁ + r₂₂q₂','첫 방향의 성분은 원래 벡터에 남습니다',PURPLE)
            else:
                cells=self.matrix();ar=Arrow(self.pos(Q[:,0]),cells[0,1].get_center(),buff=.1,color=PURPLE,stroke_width=2);self.animate(GrowArrow(ar),d=.6);self.animate(Indicate(cells[0,1],color=PURPLE),d=.6);self.remove(ar)
                self.info('r₁₂ = q₁ᵀa₂ = 1 ≠ 0','이 예시의 R = [[2,1],[0,1]]',PURPLE,low=True)
        elif i==8:self.qr();self.info('A를 공간 전체의 변환으로 바라보면?',color=TEAL)
        elif i==9:
            self.center=np.array([0.,1.,0]) if SHORT else np.array([-3.7,-.1,0]);self.scale2=1.5 if SHORT else 1.05
            self.put(self.axes(),self.curve(np.eye(2),color=MUTED))
            for t in np.linspace(0,TAU,13)[:-1]:self.put(Dot(self.pos([np.cos(t),np.sin(t)]),color=TEAL,radius=.035))
            self.info('모든 단위 방향 x에 같은 A를 적용')
        elif i==10:
            self.center=np.array([0.,1.,0]) if SHORT else np.array([-3.7,-.1,0]);self.scale2=1.5 if SHORT else 1.05
            t=ValueTracker(0);self.put(self.axes(),self.curve(np.eye(2),color=MUTED).set_stroke(opacity=.2),always_redraw(lambda:self.curve((1-t.get_value())*np.eye(2)+t.get_value()*A)))
            self.animate(t.animate.set_value(1),d=2.5);self.info('‖x‖ = 1   →   Ax','단위원 → 같은 A가 만드는 타원')
        elif i==11:self.ellipse();self.info('최대 확대 / 최소 확대','타원의 두 축은 서로 수직',TEAL)
        elif i in [12,14,15,16,19]:
            self.input_output(bases=True,stretched=i not in [15,16])
            if i==12:self.info('Avᵢ = σᵢuᵢ','vᵢ: 입력 방향 · uᵢ: 출력 방향',dual=True)
            elif i==14:self.info('σ₁ ≈ 2.288   ·   σ₂ ≈ 0.874','입력 길이 1 → 출력 길이 σᵢ',dual=True,color=TEAL)
            elif i==15:self.info('U = [u₁ u₂]   ·   V = [v₁ v₂]','출력 기준과 입력 기준은 각각 단위 직교 방향',dual=True)
            elif i==16:self.info('UᵀAV = Σ','입력과 출력의 기준을 모두 선택',dual=True,color=TEAL)
            else:self.info('SVD: 변환이 가장 크게 늘리는 입력 방향','입력 v₁과 출력 u₁을 구별합니다',dual=True,color=TEAL)
        elif i==13:
            centers,scale=self.input_output(bases=False);t=ValueTracker(VA-PI/2)
            self.put(always_redraw(lambda:self.vec(np.array([np.cos(t.get_value()),np.sin(t.get_value())]),BLUE,'x',center=centers[0],scale=scale)),always_redraw(lambda:self.vec(A@np.array([np.cos(t.get_value()),np.sin(t.get_value())]),BLUE,'Ax',center=centers[1],scale=scale)))
            self.animate(t.animate.set_value(VA),d=3)
            self.put(self.vec(V[:,1],ORANGE,'v₂',center=centers[0],scale=scale))
            self.info('σ₁ = max ‖Ax‖  (‖x‖ = 1)','최대 방향 v₁을 찾고, 수직인 v₂ 선택',dual=True,color=TEAL)
        elif i==17:
            self.center=np.array([0.,1.,0]) if SHORT else np.array([-3.7,-.1,0]);self.scale2=1.5 if SHORT else 1.05
            if SHORT:self.center=np.array([0.,1.4,0]);self.scale2=1.25
            self.matrix(True)
            t=ValueTracker(0);circle=always_redraw(lambda:self.curve(rot(-VA*t.get_value()),color=MUTED));self.put(self.axes(),circle)
            self.animate(t.animate.set_value(1),d=.55)
            self.remove(circle)
            stage=ValueTracker(0);g=always_redraw(lambda:self.curve(((1-stage.get_value())*np.eye(2)+stage.get_value()*np.diag(S))@V.T));self.put(g);self.animate(stage.animate.set_value(1),d=.6)
            self.remove(g);ang=ValueTracker(0);self.put(always_redraw(lambda:self.curve(rot(UA*ang.get_value())@np.diag(S)@V.T)))
            self.animate(ang.animate.set_value(1),d=.6)
            self.info('Vᵀ  →  Σ  →  U','입력 기준 → 방향별 확대·축소 → 출력 좌표',color=TEAL,low=True)
        elif i in [18,24]:
            self.qr();self.put(Line(self.pos(-1.2*Q[:,0]),self.pos(2.2*Q[:,0]),color=BLUE,stroke_opacity=.65))
            self.info('QR: 원래 열벡터의 순서','첫 방향 고정 → 새로운 직교 방향 추가',color=PURPLE)
        elif i in [20,23]:self.comparison(True)
        elif i==22:
            self.ellipse();self.matrix(True);self.info('Σ = diag(σ₁, σ₂)','두 특이방향 사이의 혼합 없이 확대율만',TEAL,low=True)
        elif i==25:
            self.input_output();self.info('SVD: 공간이 변형되는 방식','입력 특이방향과 방향별 확대율',dual=True,color=TEAL)
        else:self.comparison(footer=False);self.info('A = QR = UΣVᵀ','같은 행렬 · 서로 다른 기하학적 구조',dual=True,low=True)
