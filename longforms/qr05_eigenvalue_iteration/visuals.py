"""Actual QR iterates and cumulative basis; fixed physical A0 throughout."""
import os,json,textwrap
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('BATTLE_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16;config.frame_height=16 if SHORT else 9;config.background_color='#0B1120'
INK='#EEF4FF';MUTED='#91A4BF';TEAL='#60DFD0';PURPLE='#BB97FF';ORANGE='#FFB15A';BLUE='#55AEFF'
A0=np.array([[3.,1],[1,3]])
ROWS=json.loads((P/'iterations.json').read_text(encoding='utf-8'))
ANGLES=np.radians([r['angle_degrees'] for r in ROWS])
E1=np.array([1.,1])/np.sqrt(2);E2=np.array([-1.,1])/np.sqrt(2)
def rot(t):return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
def label(s,size=27,color=INK,width=7.5):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class IterationBase(Scene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.m['start'];self.end=self.m['end']
        self.center=np.array([0.,1.8,0]) if SHORT else np.array([-3.8,-.1,0]);self.scale2=1.25 if SHORT else 1.05
        self.add(label('QR 기하학 / 05     QR 반복과 고윳값',20,MUTED).move_to([0,7.35 if SHORT else 3.95,0]),label(self.m['title'],33,INK,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.1,0]))
        self.add(Line([-3.9,5.7,0],[3.9,5.7,0],color=MUTED,stroke_opacity=.22) if SHORT else Line([-7,2.55,0],[7,2.55,0],color=MUTED,stroke_opacity=.22))
        self.cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));self.capindex=-1;cap=VGroup()
        def update(m,dt=0):
            now=self.start+self.time;j=next((j for j,c in enumerate(self.cues) if c['start']<=now<c['end']),len(self.cues)-1)
            if j!=self.capindex:
                s='\n'.join(textwrap.wrap(self.cues[j]['caption'],width=29 if SHORT else 56,break_long_words=True));m.become(VGroup(label(s,25 if SHORT else 24,INK,8 if SHORT else 14).move_to([0,-6.4 if SHORT else -3.5,0])));self.capindex=j
        update(cap);cap.add_updater(update);self.add(cap)
        self.add(label('실대칭 양의 정부호 예시 · 양의 대각 QR',18,MUTED,8 if SHORT else 14).move_to([0,-7.4 if SHORT else -4.1,0]))
        self.shot();self.to(self.end)
    def pos(self,v):return self.center+self.scale2*np.array([v[0],v[1],0.])
    def put(self,*m):self.add(*m)
    def animate(self,*a,d=1):self.play(*a,run_time=d)
    def to(self,t):
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError(f'Overflow cut {self.INDEX+1}: {self.time} > {t-self.start}')
        if left>.001:self.wait(left)
    def arrow(self,v,col,name='',origin=np.zeros(2),offset=(.12,.2)):
        g=VGroup(Arrow(self.pos(origin),self.pos(origin+v),buff=0,color=col,stroke_width=4,max_tip_length_to_length_ratio=.15))
        if name:g.add(label(name,23,col,2).move_to(self.pos(origin+v)+[offset[0],offset[1],0]))
        return g
    def diagram(self,theta=0,eigen=False,names=('p₁','p₂')):
        g=VGroup()
        for v in [np.array([1.,0]),np.array([0.,1])]:g.add(Line(self.pos(-1.9*v),self.pos(1.9*v),color=MUTED,stroke_width=1,stroke_opacity=.4))
        if eigen:
            for v in [E1,E2]:g.add(DashedLine(self.pos(-1.9*v),self.pos(1.9*v),color=PURPLE,stroke_width=2,dash_length=.1))
        basis=rot(theta)
        for j in range(2):
            v=basis[:,j];g.add(Line(self.pos(-1.7*v),self.pos(1.7*v),color=TEAL,stroke_width=2,stroke_opacity=.65),self.arrow(v,TEAL,names[j],offset=(.15,-.25) if j==0 else (-.22,.2)))
        return g
    def matrix_group(self,M,name='A₀',center=None,decimals=3,limit=False):
        c=np.array(center) if center is not None else np.array([0.,-2.5,0]) if SHORT else np.array([3.8,.4,0])
        g=VGroup(label(name,26,INK,5).move_to(c+[0,1.2,0]))
        for i in range(2):
            for j in range(2):
                col=INK if i==j else ORANGE;val=M[i,j]
                s=f'{val:.{decimals}f}' if decimals else str(int(round(val)))
                cell=label(s,34,col,1.45).move_to(c+[(j-.5)*1.65,(.5-i)*.85,0])
                if i!=j:cell.set_opacity(.3+.7*min(1,abs(val)))
                g.add(cell)
        for x in [-1.7,1.7]:g.add(Line(c+[x,-.85,0],c+[x,.85,0],color=MUTED,stroke_width=2))
        if limit:g.add(label('k → ∞ · 극한',20,PURPLE).move_to(c+[0,-1.2,0]))
        return g
    def matrix(self,*a,**kw):g=self.matrix_group(*a,**kw);self.put(g);return g
    def info(self,s,note='',color=INK,dual=False,low=False):
        c=[0,-4.45 if low else -3.55,0] if SHORT else [0,-2.25,0] if dual else [3.8,-1.65 if low else .3,0]
        g=VGroup(label(s,30,color,8 if SHORT else 13 if dual else 6.7).move_to(c))
        if note:g.add(label(note,21,MUTED,8 if SHORT else 13 if dual else 6.7).next_to(g[0],DOWN,buff=.32))
        self.put(g);return g
    def state(self,k):
        theta=float(np.interp(k,np.arange(len(ANGLES)),ANGLES));basis=rot(theta);return theta,basis.T@A0@basis
    def live(self,tracker,eigen=True,limit=None):
        def draw():
            final=limit is not None and limit.get_value()>.5
            theta,M=(PI/4,np.diag([4.,2])) if final else self.state(tracker.get_value())
            g=self.diagram(theta,eigen)
            g.add(self.matrix_group(M,'Aₖ' if not final else 'A∞',decimals=0 if final else 3,limit=final))
            return g
        g=always_redraw(draw);self.put(g);return g
    def pair(self):
        centers=[[-2.1,1.3,0],[2.1,1.3,0]] if SHORT else [[-3.8,.4,0],[3.8,.4,0]]
        for j in [0,1]:
            g=self.matrix_group(np.array(ROWS[j]['A']),['A₀','A₁'][j],center=centers[j],decimals=1);g.scale(.78 if SHORT else 1.0,about_point=np.array(centers[j]));self.put(g)
    def eigenspace(self):
        self.center=np.array([0.,.8,0]) if SHORT else np.array([-3.8,-.1,0]);self.scale2=.85 if SHORT else .55
        g=VGroup()
        for v in [E1,E2]:g.add(DashedLine(self.pos(-4*v),self.pos(4*v),color=PURPLE,stroke_opacity=.5,dash_length=.12))
        self.put(g)
    def shot(self):
        i=self.INDEX
        if i==0:
            self.put(label('A = QR',43,INK).move_to([0,2.6 if SHORT else 2.,0]))
            y=.8 if SHORT else .4
            q=label('Q',52,TEAL).move_to([-1,y,0]);r=label('R',52,ORANGE).move_to([1,y,0]);self.put(q,r)
            self.animate(q.animate.move_to([1,y,0]),r.animate.move_to([-1,y,0]),d=1.3)
            self.info('QR → RQ','실제 행렬곱의 순서를 바꿉니다',dual=True)
        elif i==1:
            self.matrix(A0,center=[0,1.1,0] if SHORT else [0,.4,0],decimals=0);self.info('A₀ = [[3,1],[1,3]]',dual=True)
        elif i==2:
            q=np.array(ROWS[0]['Q']);self.put(self.diagram(np.arctan2(q[1,0],q[0,0]),names=('q₁','q₂')))
            self.info('A₀ = Q₀R₀\nQ₀ = (1/√10) [[3,−1],[1,3]]\nR₀ = (1/√10) [[10,6],[0,8]]','Q₀ᵀQ₀ = I · R₀는 위삼각',TEAL)
        elif i==3:
            q=label('Q₀',42,TEAL).move_to([-1.1,2.8 if SHORT else 1.5,0]);r=label('R₀',42,ORANGE).move_to([1.1,2.8 if SHORT else 1.5,0]);self.put(q,r)
            self.animate(q.animate.shift(RIGHT*2.2),r.animate.shift(LEFT*2.2),d=1.2)
            self.matrix(np.array(ROWS[1]['A']),'A₁ = R₀Q₀',center=[0,0,0] if SHORT else [0,-.2,0],decimals=1)
            self.info('A₁ = [[3.6,0.8],[0.8,2.4]]',dual=True)
        elif i in [4,5]:
            self.pair();self.info('원소는 달라졌습니다' if i==4 else 'λ(A₀) = λ(A₁) = {4, 2}','대각선 원소와 고윳값은 별개' if i==5 else '',PURPLE if i==5 else INK,dual=True)
        elif i==6:self.put(label('왜?',50,PURPLE).move_to([0,1 if SHORT else .4,0]))
        elif i==7:
            self.put(label('A₀ = Q₀R₀',42).move_to([0,2.5 if SHORT else 1.2,0]));self.info('R₀ = Q₀ᵀA₀','직교성: Q₀ᵀQ₀ = I',TEAL,dual=True)
        elif i==8:
            self.put(label('A₁ = R₀Q₀',40).move_to([0,2.5 if SHORT else 1.2,0]));self.info('A₁ = Q₀ᵀA₀Q₀','R₀를 Q₀ᵀA₀로 치환',TEAL,dual=True)
        elif i==9:self.info('직교 유사변환\nA′ = QᵀAQ',color=TEAL,dual=True)
        elif i==10:
            t=ValueTracker(0);self.live(t,eigen=False);self.animate(t.animate.set_value(1),d=2.7)
            self.info('고정된 A₀를 새 직교 기준으로 표현','λ(A₀) = λ(A₁) = {4,2}',PURPLE,low=True)
        elif i==11:self.info('A₀ → A₁ → A₂ → …','QR → RQ를 계속 반복',dual=True,color=TEAL)
        elif i==12:
            self.matrix(np.array(ROWS[2]['A']),'A₂',center=[0,.6,0] if SHORT else [0,.5,0]);self.info('A₁ = Q₁R₁  →  A₂ = R₁Q₁',dual=True)
        elif i==13:
            t=ValueTracker(0);self.live(t,eigen=False)
            for k in [1,2,3]:self.animate(t.animate.set_value(k),d=.85)
            self.info('Pₖ = Q₀Q₁…Qₖ₋₁','Aₖ = PₖᵀA₀Pₖ · 실제 누적 기준',TEAL,low=True)
        elif i==14:
            self.matrix(np.array(ROWS[3]['A']),'A₃',center=[0,1.1,0] if SHORT else [0,.4,0]);self.info('비대각: 1 → 0.800 → 0.471 → 0.246',dual=True,color=ORANGE)
        elif i==15:
            self.matrix(A0,center=[0,1.1,0] if SHORT else [0,.4,0],decimals=0);self.info('실대칭 · 서로 다른 양의 고윳값 4, 2','이 예시의 수렴을 살펴봅니다',dual=True)
        elif i==16:
            self.eigenspace();t=ValueTracker(0)
            self.put(always_redraw(lambda:self.arrow(E1*(1+3*t.get_value()),PURPLE,'4v₁')),always_redraw(lambda:self.arrow(E2*(1+t.get_value()),PURPLE,'2v₂',offset=(-.35,.2))))
            self.animate(t.animate.set_value(1),d=2.2);self.info('A₀v₁ = 4v₁  ·  A₀v₂ = 2v₂','두 고유방향은 변하지 않고 길이만 변합니다',PURPLE)
        elif i==17:
            self.put(self.diagram(0,eigen=True));self.info('원래 가로·세로 축 ≠ 고유방향','고유방향은 45°와 135°의 두 직선',PURPLE)
        elif i==18:
            self.put(self.diagram(0,eigen=True));k=ValueTracker(0)
            def power():
                ratio=2.**(-k.get_value());y=(E1-ratio*E2);y/=np.linalg.norm(y)
                return self.arrow(1.4*y,INK,'정규화된 A₀ᵏx')
            self.put(always_redraw(power));self.animate(k.animate.set_value(6),d=3.5)
            self.info('상대 비율: (2/4)ᵏ → 0','참고: 고정된 A₀의 거듭제곱 후 길이 정규화',ORANGE)
        elif i==19:
            t=ValueTracker(0);self.put(always_redraw(lambda:self.diagram(self.state(t.get_value())[0],eigen=True)));self.animate(t.animate.set_value(3),d=1.6)
            self.info('하나의 벡터 → 직교하는 여러 기준','QR 반복에서는 직교화가 함께 이루어집니다',TEAL)
        elif i==20:
            t=ValueTracker(0);self.live(t,eigen=True)
            for k,d in [(1,.8),(2,.8),(3,.8),(5,1.1),(8,1.2)]:self.animate(t.animate.set_value(k),d=d)
            self.info('누적 기준: 0° → 18.4° → 31.0° → …','Pₖ의 첫 기준이 45° 고유방향으로 접근',TEAL,low=True)
        elif i==21:
            self.center=np.array([0.,1.6,0]) if SHORT else np.array([-3.8,-.1,0]);self.scale2=.7 if SHORT else .5
            t=ValueTracker(0)
            def action():
                theta,_=self.state(t.get_value());p=rot(theta);u=p[:,0];a=A0@u;diag=(u@a)*u;off=a-diag
                return VGroup(self.diagram(theta,True),self.arrow(diag,TEAL),self.arrow(off,ORANGE,origin=diag),self.arrow(a,INK,'A₀p₁'))
            self.put(always_redraw(action));self.animate(t.animate.set_value(7),d=3)
            self.info('자기 축 성분 + 다른 축의 혼합 성분','다른 축 방향의 주황 성분이 작아집니다',ORANGE)
        elif i==22:
            t=ValueTracker(0);self.live(t,True)
            for k in [1,2,3]:self.animate(t.animate.set_value(k),d=.8)
            self.info('비대각 성분이 점점 작아집니다','표시 숫자는 실제 QR 반복값의 반올림',ORANGE,low=True)
        elif i==23:
            t=ValueTracker(3);self.live(t,True);self.animate(t.animate.set_value(9),d=1.1)
            self.info('Aₖ → diag(4, 2)','유한 반복에서 정확히 0이 된다는 뜻은 아닙니다',ORANGE,low=True)
        elif i==24:
            self.put(self.diagram(PI/4,True));self.matrix(np.diag([4.,2]),'A∞',decimals=0,limit=True)
            self.info('대각선의 4와 2 = 원래 고윳값','A₀의 대각선 3,3은 고윳값이 아니었습니다',PURPLE,low=True)
        elif i==25:
            self.matrix(A0,center=[0,1.1,0] if SHORT else [0,.4,0],decimals=0);self.info('출발점: 주어진 행렬의 원소','반복의 입력에 고윳값은 필요하지 않습니다',dual=True)
        elif i==26:
            t=ValueTracker(0);self.live(t,False);self.animate(t.animate.set_value(5),d=2.2)
            self.info('Aₖ = QₖRₖ → Aₖ₊₁ = RₖQₖ','분해 → 순서 변경 → 반복',TEAL,low=True)
        elif i==27:
            self.put(self.diagram(PI/4,True));self.matrix(np.diag([4.,2]),'극한',decimals=0,limit=True)
            self.info('λ₁ = 4  ·  λ₂ = 2','동일한 변환의 고유구조가 드러납니다',PURPLE,low=True)
        elif i==28:
            q=np.array(ROWS[0]['Q']);self.put(self.diagram(np.arctan2(q[1,0],q[0,0]),names=('q₁','q₂')));self.info('A = QR','직교 기준을 구성하는 분해',TEAL)
        else:
            t=ValueTracker(0);limit=ValueTracker(0);self.live(t,True,limit);self.animate(t.animate.set_value(8),d=3.5)
            self.to(122);limit.set_value(1)
            self.info('고윳값은 변하지 않는다.\n달라지는 것은 바라보는 기준이다.','Aₖ₊₁ = QₖᵀAₖQₖ',TEAL,low=True)
