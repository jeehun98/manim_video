"""Horizontal series closing: distinct geometric structures, common orthogonality."""
import json,textwrap,itertools
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
config.frame_width=16;config.frame_height=9;config.background_color='#0B1120'
INK='#EEF4FF';MUTED='#91A4BF';TEAL='#60DFD0';ORANGE='#FFB15A';GOLD='#F8D26A';BLUE='#55AEFF';PURPLE='#BB97FF'
A3=np.array([[2.,1,1],[0,2,1],[0,0,2]])
C=A3[:2,:2];A0=np.array([[3.,1],[1,3]])
vals,vecs=np.linalg.eigh(C.T@C);SIG=np.sqrt(vals[::-1]);v=vecs[:,::-1][:,0];v*=1 if v[0]>=0 else -1;V=np.column_stack([v,[-v[1],v[0]]]);U=C@V@np.diag(1/SIG)
ROWS=json.loads((P/'iterations.json').read_text(encoding='utf-8'));ANGLES=[r['angle'] for r in ROWS]
def rot(t):return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
def label(s,size=27,color=INK,width=7.5):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class ClosingBase(Scene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX];self.start=self.m['start'];self.end=self.m['end']
        self.az=-55*DEGREES;self.el=28*DEGREES;self.center=np.array([-5.5,-.4,0]);self.scale3=.9
        self.add(label('QR 분해의 기하학 · 마무리',20,MUTED).move_to([0,3.95,0]),label(self.m['title'],34,INK,14).move_to([0,3.1,0]),Line([-7,2.55,0],[7,2.55,0],color=MUTED,stroke_opacity=.22))
        self.cues=json.loads((P/'timing.json').read_text(encoding='utf-8'));self.capindex=-1;cap=VGroup()
        def update(m,dt=0):
            now=self.start+self.time;j=next((j for j,c in enumerate(self.cues) if c['start']<=now<c['end']),len(self.cues)-1)
            if j!=self.capindex:
                s='\n'.join(textwrap.wrap(self.cues[j]['caption'],width=56,break_long_words=True));m.become(VGroup(label(s,24,INK,14).move_to([0,-3.5,0])));self.capindex=j
        update(cap);cap.add_updater(update);self.add(cap)
        self.add(label('방향 · 높이 · 특이방향 · 고유방향을 잇는 직교성',18,MUTED,14).move_to([0,-4.1,0]))
        self.shot();self.to(self.end)
    def put(self,*m):self.add(*m)
    def animate(self,*a,d=1):self.play(*a,run_time=d)
    def to(self,t):
        left=t-self.start-self.time
        if left<-.04:raise RuntimeError(f'Overflow {self.INDEX+1}: {self.time} > {t-self.start}')
        if left>.001:self.wait(left)
    def proj(self,v):
        x,y,z=np.array(v);a=self.az;e=self.el
        return self.center+self.scale3*np.array([-np.sin(a)*x+np.cos(a)*y,-np.sin(e)*(np.cos(a)*x+np.sin(a)*y)+np.cos(e)*z,0])
    def axes3(self):
        return VGroup(*(Line(self.proj(-.6*v),self.proj(2.8*v),color=MUTED,stroke_width=1,stroke_opacity=.3) for v in [RIGHT,UP,OUT]))
    def vec3(self,v,col=INK,name='',origin=ORIGIN):
        end=self.proj(v+origin);g=VGroup(Arrow(self.proj(origin),end,color=col,buff=0,stroke_width=4,max_tip_length_to_length_ratio=.15))
        if name:g.add(label(name,22,col,2).move_to(end+[.15,.22,0]))
        return g
    def plane(self):return Polygon(*[self.proj(v) for v in [(-.6,-.6,0),(3,-.6,0),(3,3,0),(-.6,3,0)]],color=TEAL,fill_color=TEAL,fill_opacity=.065,stroke_opacity=.35,stroke_width=1)
    def box(self,M=A3,level=3,col=BLUE):
        if level==1:return self.vec3(M[:,0],col)
        if level==2:return Polygon(*[self.proj(v) for v in [ORIGIN,M[:,0],M[:,0]+M[:,1],M[:,1]]],color=col,fill_color=col,fill_opacity=.12,stroke_width=2)
        vertices={k:M@np.array(k,dtype=float) for k in itertools.product([0,1],repeat=3)};faces=[]
        for axis in range(3):
            others=[j for j in range(3) if j!=axis]
            for side in [0,1]:
                face=[]
                for x,y in [(0,0),(1,0),(1,1),(0,1)]:
                    k=[0,0,0];k[axis]=side;k[others[0]]=x;k[others[1]]=y;face.append(vertices[tuple(k)])
                faces.append(face)
        return VGroup(*(Polygon(*[self.proj(v) for v in f],color=col,fill_color=col,fill_opacity=.075,stroke_width=1.2,stroke_opacity=.6) for f in faces))
    def info(self,s,note='',col=INK,dual=False,low=False):
        c=[0,-2.2,0] if dual else [3.8,-1.7 if low else .35,0]
        g=VGroup(label(s,31,col,13 if dual else 6.7).move_to(c))
        if note:g.add(label(note,21,MUTED,13 if dual else 6.7).next_to(g[0],DOWN,buff=.3))
        self.put(g);return g
    def matrix3(self,symbolic=False,focus=False,center=(3.8,.4,0),name='A'):
        c=np.array(center);g=VGroup(label(name,27).move_to(c+[0,1.3,0]));cells={}
        for i in range(3):
            for j in range(3):
                s=('r'+['₁','₂','₃'][i]+['₁','₂','₃'][j]) if symbolic and i<=j else str(int(A3[i,j]))
                col=GOLD if i==j else ORANGE if i<j else MUTED
                cell=label(s,31,col,1).move_to(c+[(j-1)*1.05,(1-i)*.65,0])
                if focus and i!=j:cell.set_opacity(.28)
                cells[i,j]=cell;g.add(cell)
        for x in [-1.65,1.65]:g.add(Line(c+[x,-.95,0],c+[x,.95,0],color=MUTED,stroke_width=2))
        self.put(g);return cells
    def heights(self):
        self.put(self.vec3(2*RIGHT,GOLD))
        for a,b,n,offset in [(np.array([1.,0,0]),np.array([1.,2,0]),'|r₂₂|',[-.4,.15,0]),(np.array([1.,1,0]),np.array([1.,1,2]),'|r₃₃|',[.5,0,0])]:
            self.put(Line(self.proj(a),self.proj(b),color=GOLD,stroke_width=4),label(n,23,GOLD).move_to(self.proj((a+b)/2)+offset))
        self.put(label('|r₁₁|',23,GOLD).move_to(self.proj(RIGHT)+[0,-.35,0]))
    def point2(self,v,center=(-3.8,0,0),scale=1):return np.array(center)+scale*np.array([v[0],v[1],0.])
    def arrow2(self,v,col,name='',center=(-3.8,0,0),scale=1):
        end=self.point2(v,center,scale);g=VGroup(Arrow(center,end,buff=0,color=col,stroke_width=4,max_tip_length_to_length_ratio=.15))
        if name:g.add(label(name,22,col,2).move_to(end+[.12,.2,0]))
        return g
    def curve(self,M,center,scale=1,col=BLUE):
        return VMobject(color=col,stroke_width=3).set_points_as_corners([self.point2(M@np.array([np.cos(t),np.sin(t)]),center,scale) for t in np.linspace(0,TAU,121)])
    def svd(self,bases=True,show_output=True):
        left=np.array([-3.6,-.1,0]);right=np.array([3.6,-.1,0]);scale=.8
        self.put(self.curve(np.eye(2),left,scale,MUTED),label('입력 xy평면 · V',24,INK).move_to([-3.6,2.15,0]),label('출력 xy평면 · U',24,BLUE).move_to([3.6,2.15,0]))
        if show_output:self.put(self.curve(C,right,scale,BLUE))
        if bases:
            for j,col in enumerate([BLUE,PURPLE]):self.put(self.arrow2(V[:,j],col,['v₁','v₂'][j],left,scale),self.arrow2(C@V[:,j],col,['σ₁u₁','σ₂u₂'][j],right,scale))
    def basis2(self,theta,eigen=True,center=(-3.8,0,0),scale=1.05):
        g=VGroup()
        for v in [np.array([1.,0]),np.array([0.,1])]:g.add(Line(self.point2(-1.7*v,center,scale),self.point2(1.7*v,center,scale),color=MUTED,stroke_opacity=.3))
        if eigen:
            for v in [np.array([1.,1])/np.sqrt(2),np.array([-1.,1])/np.sqrt(2)]:g.add(DashedLine(self.point2(-1.8*v,center,scale),self.point2(1.8*v,center,scale),color=PURPLE,stroke_width=2,dash_length=.1))
        for j in range(2):g.add(self.arrow2(rot(theta)[:,j],TEAL,['p₁','p₂'][j],center,scale))
        return g
    def iterate(self,k,limit=False):
        theta=PI/4 if limit else np.interp(k,np.arange(len(ROWS)),[r['angle'] for r in ROWS]);basis=rot(theta);a=np.diag([4.,2]) if limit else basis.T@A0@basis
        g=self.basis2(theta);c=np.array([3.8,.5,0]);g.add(label('QR 반복 예시 A₀ = [[3,1],[1,3]]',22,MUTED,6.8).move_to([3.8,1.9,0]))
        for i in range(2):
            for j in range(2):g.add(label(str(int(a[i,j])) if limit else f'{a[i,j]:.3f}',32,INK if i==j else ORANGE,1.4).move_to(c+[(j-.5)*1.6,(.5-i)*.85,0]))
        for x in [-1.65,1.65]:g.add(Line(c+[x,-.85,0],c+[x,.85,0],color=MUTED))
        if limit:g.add(label('k → ∞ · 극한',21,PURPLE).move_to(c+[0,-1.2,0]))
        return g
    def orthogonal_panels(self):
        angles=[0,np.arctan2(V[1,0],V[0,0]),np.arctan2(U[1,0],U[0,0]),PI/4]
        for x,t,n in zip([-5.4,-1.8,1.8,5.4],angles,['QR 기저','입력 특이기저 V','출력 특이기저 U','대칭행렬 고유기저']):
            center=np.array([x,.2,0]);basis=rot(t)
            self.put(label(n,22,INK,3.3).move_to([x,1.9,0]))
            for j in range(2):self.put(self.arrow2(basis[:,j],TEAL if j==0 else PURPLE,center=center,scale=.95))
            a=.2*basis[:,0];b=.2*basis[:,1]
            self.put(VMobject(color=GOLD,stroke_width=2).set_points_as_corners([self.point2(a,center),self.point2(a+b,center),self.point2(b,center)]))
    def shot(self):
        i=self.INDEX
        if i==0:
            self.matrix3(center=(0,.4,0));self.info('하나의 행렬, 그 숫자 뒤에는?',dual=True)
        elif i==1:
            self.put(self.axes3(),self.box())
            for j in range(3):self.animate(Create(self.vec3(A3[:,j],INK,['a₁','a₂','a₃'][j])),d=.55)
            self.matrix3();self.info('A = [a₁ a₂ a₃]','숫자의 열이 공간 속 벡터가 됩니다',low=True)
        elif i in [2,3]:
            self.put(self.axes3(),self.vec3(A3[:,0],INK,'a₁'))
            self.animate(Create(Line(self.proj(-2*RIGHT),self.proj(3*RIGHT),color=TEAL,stroke_width=2)),d=.8)
            self.info('span(a₁)','하나의 독립 방향이 만드는 직선',TEAL)
        elif i==4:
            self.put(self.axes3(),self.vec3(A3[:,0],INK,'a₁'),Line(self.proj(-2*RIGHT),self.proj(3*RIGHT),color=TEAL))
            self.animate(Create(self.vec3(A3[:,1],INK,'a₂')),FadeIn(self.plane()),d=1)
            self.info('span(a₁, a₂)','기존 직선을 포함하는 평면',TEAL)
        elif i==5:
            self.el=65*DEGREES;self.put(self.axes3(),self.plane(),self.vec3(A3[:,1],INK,'a₂'),self.vec3(RIGHT,ORANGE,''),self.vec3(2*UP,TEAL,'u₂',origin=RIGHT))
            self.info('a₂ = (q₁ᵀa₂)q₁ + u₂','기존 방향의 성분과 수직 잔여 성분',ORANGE)
        elif i==6:
            self.el=65*DEGREES;self.put(self.axes3(),self.plane(),self.vec3(RIGHT,TEAL,'q₁'))
            length=ValueTracker(2);self.put(always_redraw(lambda:self.vec3(UP*length.get_value(),TEAL,'q₂')));self.animate(length.animate.set_value(1),d=1.2)
            self.info('q₁ᵀq₂ = 0','서로 수직인 단위 기준 방향',TEAL)
        elif i in [7,8]:
            self.put(self.axes3(),self.box(),self.vec3(A3[:,2],INK,'a₃'));cells=self.matrix3(True,i==8,name='R')
            for key in ([(1,0),(2,0),(2,1)] if i==7 else [(0,0),(1,1),(2,2)]):self.animate(Indicate(cells[key],color=GOLD if i==8 else ORANGE),d=.3)
            self.info('공간의 확장 순서 → 위삼각 계수','앞 벡터에는 뒤 직교 방향의 성분이 없습니다',low=True)
        elif i in [9,10]:
            self.put(self.axes3(),self.box(col=GOLD));self.heights();self.matrix3(True,True,name='R')
            self.info('대각 성분 = 새롭게 추가되는 수직 높이' if i==9 else '길이 → 넓이 → 부피','|r₁₁| = 2 · |r₂₂| = 2 · |r₃₃| = 2',GOLD,low=True)
        elif i==11:
            self.put(self.axes3(),self.box(col=GOLD));self.heights();self.info('|det A| = |r₁₁r₂₂r₃₃|','2 × 2 × 2 = 8',GOLD)
        elif i==12:
            t=ValueTracker(0);self.put(self.axes3(),always_redraw(lambda:self.box((1-t.get_value())*np.eye(3)+t.get_value()*A3,col=GOLD)));self.animate(t.animate.set_value(1),d=1.7)
            self.info('단위 부피 1  →  부피 8','모든 꼭짓점에 같은 A를 적용',GOLD)
        elif i==13:
            center=np.array([-3.6,-.1,0]);self.put(self.arrow2(np.array([1.,0]),TEAL,'q₁',center),self.arrow2(np.array([0.,1]),TEAL,'q₂',center),self.curve(np.eye(2),[3.6,-.1,0],.9,MUTED))
            self.info('A = QR   /   C = UΣVᵀ','여기부터 xy평면에 제한한 C = [[2,1],[0,2]]',dual=True)
        elif i==14:
            self.svd(False,False);t=ValueTracker(0);self.put(always_redraw(lambda:self.curve((1-t.get_value())*np.eye(2)+t.get_value()*C,[3.6,-.1,0],.8,BLUE)));self.animate(t.animate.set_value(1),d=1.8)
            for j,col in enumerate([BLUE,PURPLE]):self.put(self.arrow2(V[:,j],col,['v₁','v₂'][j],[-3.6,-.1,0],.8),self.arrow2(C@V[:,j],col,['σ₁u₁','σ₂u₂'][j],[3.6,-.1,0],.8))
            self.info('입력 특이방향 vᵢ → 출력 축 uᵢ','같은 C가 단위원 전체를 타원으로 변환',dual=True,col=BLUE)
        elif i==15:
            self.svd();self.info('Cvᵢ = σᵢuᵢ   ·   Σ = diag(σ₁,σ₂)','특이값은 타원의 두 반축 길이',dual=True,col=BLUE)
        elif i==16:
            left=np.array([-3.6,-.1,0]);right=np.array([3.6,-.1,0]);self.put(label('QR · 원래 열벡터의 순서',24,TEAL).move_to([-3.6,2.1,0]),label('SVD · 변환의 특이방향',24,BLUE).move_to([3.6,2.1,0]))
            for j in range(2):self.put(self.arrow2(C[:,j],INK,['c₁','c₂'][j],left,.8),self.arrow2(np.eye(2)[:,j],TEAL,['q₁','q₂'][j],left,.8))
            self.put(self.curve(C,right,.8,BLUE))
            for j,col in enumerate([BLUE,PURPLE]):self.put(self.arrow2(C@V[:,j],col,['σ₁u₁','σ₂u₂'][j],right,.8))
            self.info('같은 C · 다른 기준이 드러내는 구조','입력 V와 출력 U는 각각 선택됩니다',dual=True)
        elif i in [17,18,19]:
            t=ValueTracker(0 if i==17 else 2 if i==18 else 5);lim=ValueTracker(0)
            self.put(always_redraw(lambda:self.iterate(t.get_value(),lim.get_value()>.5)))
            self.animate(t.animate.set_value(2 if i==17 else 5 if i==18 else 9),d=2.1 if i!=17 else 2.6)
            if i==19:self.to(66.5);lim.set_value(1)
            self.info('Aₖ = PₖᵀA₀Pₖ','누적 직교 기준 Pₖ · 실대칭 양의 정부호 예시',TEAL,low=True)
        elif i==20:
            self.put(self.axes3(),self.box(col=GOLD));self.heights();self.info('공간을 구성하는 방향 / 부피를 결정하는 높이','직선 · 평면 · 공간을 잇는 직교 성분',GOLD)
        elif i==21:
            self.put(self.curve(C,[-3.6,-.1,0],.8,BLUE),self.basis2(PI/4,True,[3.6,-.1,0]),label('특이방향 · C의 출력 공간',24,BLUE).move_to([-3.6,2.15,0]),label('고유방향 · 대칭행렬 A₀',24,PURPLE).move_to([3.6,2.15,0]))
            for j,col in enumerate([BLUE,PURPLE]):self.put(self.arrow2(C@V[:,j],col,['σ₁u₁','σ₂u₂'][j],[-3.6,-.1,0],.8))
            self.info('특이방향 / 고유방향','서로 다른 구조를 드러내는 직교 기준',dual=True,col=PURPLE)
        elif i==22:
            self.orthogonal_panels();self.info('직교성   ·   qᵢᵀqⱼ = 0  (i ≠ j)','각 목적의 기준은 서로 다르지만, 수직이라는 성질은 공통',dual=True,col=GOLD)
        elif i==23:
            self.put(self.axes3(),self.vec3(RIGHT,TEAL,'q₁'),self.vec3(UP,TEAL,'q₂'),self.vec3(OUT,TEAL,'q₃'));self.matrix3(True,name='R')
            self.info('A = QR','Q: 직교 방향들 · R: 그 방향의 조합 계수',TEAL,low=True)
        else:
            self.put(self.axes3(),self.vec3(RIGHT,TEAL,'q₁'),self.vec3(UP,TEAL,'q₂'),self.vec3(OUT,TEAL,'q₃'));self.matrix3()
            self.info('행렬을 분해한다는 것은\n그 안의 구조를 발견하는 일이다.','A = QR',TEAL,low=True)
