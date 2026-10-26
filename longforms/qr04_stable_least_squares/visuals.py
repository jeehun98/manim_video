"""Least-squares geometry and coefficient conditioning, with fixed column space."""
from base import *
from base import QRBase as SharedBase
TEAL='#60DFD0';YELLOW='#FFCB70'
B=np.array([0.,1,1.2]);P0=np.array([0.,1,0])
def mat(e):return np.array([[1.,1],[0,e],[0,0]])

class LeastSquaresBase(SharedBase):
    def axes(self):
        g=VGroup()
        for v,n in [(RIGHT,'x'),(UP,'y'),(OUT,'z')]:
            g.add(Line(self.proj(-.5*v),self.proj(1.65*v),color=MUTED,stroke_width=1,stroke_opacity=.25))
            g.add(label(n,17,MUTED).move_to(self.proj(1.8*v)))
        return g
    def plane(self):
        g=VGroup(Polygon(*[self.proj(v) for v in [(-.6,-.6,0),(1.4,-.6,0),(1.4,1.4,0),(-.6,1.4,0)]],fill_color=PURPLE,fill_opacity=.09,color=PURPLE,stroke_width=1,stroke_opacity=.35))
        for t in [0,.5,1]:
            g.add(Line(self.proj((t,-.6,0)),self.proj((t,1.4,0)),color=PURPLE,stroke_opacity=.15),Line(self.proj((-.6,t,0)),self.proj((1.4,t,0)),color=PURPLE,stroke_opacity=.15))
        return g
    def vec(self,v,color,name='',origin=ORIGIN,**kwargs):
        g=super().vec(v,color,name,origin,**kwargs)
        if name=='a₁':g[-1].move_to(self.proj(np.array(origin)+v)+[0,-.38,0])
        if name=='a₂':g[-1].move_to(self.proj(np.array(origin)+v)+[.05,.36,0])
        if name=='q₂':g[-1].move_to(self.proj(np.array(origin)+v)+[-.35,.4,0])
        return g
    def geometry(self,e=.8,target=True,projection=True,basis=False):
        self.put(self.plane(),self.vec(RIGHT,BLUE,'' if basis else 'a₁',opacity=.25 if basis else 1),self.vec(np.array([1.,e,0]),GREEN,'a₂',opacity=.35 if basis else 1))
        if target:self.put(self.vec(B,PURPLE,'b'))
        if projection:
            self.put(Dot(self.proj(P0),color=TEAL,radius=.055),label('p',24,TEAL).move_to(self.proj(P0)+([.3,.1,0] if basis else [-.25,.08,0])),Line(self.proj(P0),self.proj(B),color=ORANGE,stroke_width=3))
        if basis:self.put(self.vec(RIGHT,BLUE,'q₁',opacity=.8),self.vec(UP,TEAL,'q₂'))
    def formula(self,s,note='',color=INK):
        pos=[0,-3.5,0] if SHORT else [3.65,.4,0]
        if not SHORT and self.INDEX==14:pos=[3.65,-.8,0]
        eq=label(s,32,color,8 if SHORT else 6.7).move_to(pos);self.put(eq)
        if note:self.put(label(note,22,MUTED,8 if SHORT else 6.5).next_to(eq,DOWN,buff=.4))
        return eq
    def route(self,focus='both',bottom='같은 최소제곱 문제'):
        x1,x2=(-2.1,2.1) if SHORT else (-3.8,3.8)
        y1=2.9 if SHORT else 1.45;y2=.5 if SHORT else -.3
        title=label('min ‖Ax − b‖₂²',35).move_to([0,4.5 if SHORT else 2.25,0])
        self.put(title)
        for x,col,name,eq,mode in [(x1,YELLOW,'정규방정식','AᵀAx = Aᵀb','normal'),(x2,TEAL,'QR 분해','Rx = Qᵀb','qr')]:
            group=VGroup(label(name,28,col,3.8).move_to([x,y1,0]),label(eq,29,col,3.8).move_to([x,y2+.9,0]),RoundedRectangle(width=3.9,height=2,corner_radius=.14,color=col,stroke_width=1.5).move_to([x,y1-.7,0]),Arrow([0,4 if SHORT else 2.15,0],[x,y1+.5,0],buff=.15,color=col,stroke_width=2))
            if focus not in ['both',mode]:
                for child in group:
                    if isinstance(child,RoundedRectangle):child.set_stroke(opacity=.28);child.set_fill(opacity=0)
                    else:child.set_opacity(.28)
            self.put(group)
        self.put(label(bottom,27,INK,8 if SHORT else 13).move_to([0,-2 if SHORT else -2,0]))
    def coefficient_display(self,e_tracker,delta=None):
        pos=[0,-2.9,0] if SHORT else [3.7,.65,0]
        def group():
            e=e_tracker.get_value();dy=0 if delta is None else delta.get_value()
            s=f'ε = {e:.3f}\nx₁ = −{(1+dy)/e:,.1f}\nx₂ = +{(1+dy)/e:,.1f}'
            return label(s,33,INK,7 if SHORT else 6).move_to(pos)
        self.put(always_redraw(group))
    def shot(self):
        i=self.INDEX
        self.center=np.array([-1.1,1.0,0]) if SHORT else np.array([-4.1,-.45,0]);self.scale3=2.3 if SHORT else 1.7
        if i in [0,1,2,13,14,15,16,21,24,25,26,27]:
            # Pure comparison screens do not retain background axes.
            for m in list(self.mobjects):
                if getattr(m,'updaters',[]):self.remove(m)
        if i==0:
            self.put(label('min ‖Ax − b‖₂²',42).move_to([0,2 if SHORT else .8,0]))
            self.put(Line([0,1 if SHORT else .2,0],[-2,-.2,0],color=YELLOW),Line([0,1 if SHORT else .2,0],[2,-.2,0],color=TEAL))
            self.formula('같은 문제 · 두 가지 계산 방법')
        elif i in [1,2]:self.route('both' if i==1 else 'qr','같은 답, 다른 계산의 안정성?')
        elif i==3:
            self.geometry(projection=False);self.formula('p ∈ col(A),   b ∉ col(A)','열벡터의 조합이 만드는 평면')
        elif i==4:
            self.geometry(projection=False)
            point=VectorizedPoint(np.array([.9,.2,0]));dot=always_redraw(lambda:Dot(self.proj(point.get_location()),color=TEAL,radius=.06));line=always_redraw(lambda:Line(self.proj(point.get_location()),self.proj(B),color=ORANGE,stroke_width=3))
            self.put(dot,line)
            for v in [[.8,.8,0],[-.3,1.2,0],P0]:self.animate(point.animate.move_to(v),d=.75)
            self.formula('후보점 Ax → 가장 가까운 점 p')
        elif i in [5,6,7,8]:
            self.geometry();self.put(self.rightmark(P0,RIGHT,OUT))
            if i==5:self.formula('min ‖Ax − b‖₂²','p = A x̂',TEAL)
            elif i==6:self.formula('잔차 = b − A x̂','잔차 ⟂ col(A)',ORANGE)
            elif i==7:
                eq=self.formula('Aᵀ(b − A x̂) = 0','잔차가 모든 열벡터에 수직')
                self.to(27);self.animate(Transform(eq,label('AᵀA x̂ = Aᵀb',32,YELLOW,8 if SHORT else 6.5).move_to(eq)),d=.7)
            else:self.formula('AᵀA x̂ = Aᵀb   ✓','열 전체 계수 · 정확한 산술에서 올바른 해',YELLOW)
        elif i==9:
            self.formula('AᵀA · 부동소수점 계산','컴퓨터는 유한한 자리수로 저장합니다',YELLOW)
            pos=[0,2,0] if SHORT else [-3.8,.8,0]
            number=label('1.0000000047',42,YELLOW).move_to(pos);self.put(number)
            self.animate(Transform(number,label('1.00000000',42,YELLOW).move_to(pos)),d=1.2)
        elif i==10:
            self.put(self.plane(),self.vec(RIGHT,BLUE,'a₁'))
            e=ValueTracker(.8);self.put(always_redraw(lambda:self.vec(np.array([1.,e.get_value(),0]),GREEN,'a₂')))
            self.animate(e.animate.set_value(.05),d=1.8)
            self.formula('a₁ = (1,0,0)   ·   a₂ = (1,ε,0)','ε > 0이면 열공간은 여전히 같은 평면')
        elif i==11:
            e=ValueTracker(.2);self.put(self.plane(),self.vec(RIGHT,BLUE,'a₁'),self.vec(P0,TEAL,'p'))
            self.put(always_redraw(lambda:self.vec(np.array([1.,e.get_value(),0]),GREEN,'a₂')))
            self.coefficient_display(e)
            for v in [.05,.02]:self.animate(e.animate.set_value(v),d=1.5)
            self.put(label('작은 독립 방향 → 큰 계수의 상쇄',23,ORANGE,8 if SHORT else 6.6).move_to([0,-4.7,0] if SHORT else [3.7,-1.45,0]))
            self.put(label('a₂ − a₁ = (0, ε, 0)  ·  p = (0, 1, 0)',21,MUTED,8 if SHORT else 6.6).move_to([0,-5.25,0] if SHORT else [3.7,-2,0]))
        elif i==12:
            self.geometry(e=.02,target=False,projection=False)
            self.formula('κ₂(A) = σmax / σmin','조건수 ↑  →  계수 계산의 민감성 ↑',ORANGE)
        elif i==13:
            self.put(label('AᵀA =\n⎡ 1       1      ⎤\n⎣ 1   1 + ε² ⎦',33,YELLOW,8).move_to([0,2,0] if SHORT else [-3.6,.5,0]))
            self.formula('κ₂(AᵀA) = κ₂(A)²','열 전체 계수 · 2-노름 조건수의 정확한 관계',YELLOW)
        elif i==14:
            self.put(label('κ₂(A) = 1,000',36,INK).move_to([0,3,0] if SHORT else [-3.7,.8,0]))
            n=ValueTracker(1000);pos=[0,.4,0] if SHORT else [3.65,.8,0]
            self.put(always_redraw(lambda:label(f'{n.get_value():,.0f}',52,YELLOW).move_to(pos)))
            self.animate(n.animate.set_value(1000000),d=2)
            self.formula('κ₂(AᵀA) = 1,000,000','조건수의 비교 · 실제 오차의 배율은 아님',YELLOW)
        elif i in [15,16]:self.route('normal' if i==15 else 'qr','문제의 민감성 + 계산 경로의 선택')
        elif i in [17,18]:
            self.geometry(e=.02,target=False,projection=False,basis=True);self.put(self.rightmark(ORIGIN,RIGHT,UP))
            self.formula('A = QR\nR = ⎡1   1⎤\n       ⎣0   ε⎦' if i==17 else 'QᵀQ = I','Q는 정규직교 열을 가진 3×2 축약 기저' if i==17 else '평면은 그대로 · 기준 방향은 서로 직교',TEAL)
        elif i==19:
            self.geometry(e=.02,basis=True);self.put(self.vec(P0,TEAL,''));self.formula('c = Qᵀb = (0, 1)ᵀ','직교 방향에 대한 두 투영 계수',TEAL)
        elif i==20:
            self.geometry(e=.05,basis=True)
            eq=self.formula('Rx = Qᵀb','후진대입: 아래 행 → 위 행',TEAL)
            self.to(75);self.animate(Transform(eq,label('εx₂ = c₂  →  x₂ = c₂/ε',29,TEAL,8 if SHORT else 6.6).move_to(eq)),d=.4)
            self.to(76.3);self.animate(Transform(eq,label('x₁ + x₂ = c₁  →  x₁ = c₁−x₂',29,TEAL,8 if SHORT else 6.6).move_to(eq)),d=.4)
            self.to(77.5);self.animate(Transform(eq,label('x₁ = −20, x₂ = 20  →  p = (0,1,0)',28,TEAL,8 if SHORT else 6.6).move_to(eq)),d=.4)
        elif i==21:
            self.route('both','κ₂(AᵀA) = κ₂(A)²   ·   κ₂(R) = κ₂(A)')
        elif i==22:
            self.geometry(e=.02,target=False,projection=False);self.formula('R = ⎡1   1⎤\n       ⎣0   ε⎦\nκ₂(R) = κ₂(A)','작은 ε가 R에도 남아 있습니다',ORANGE)
        elif i==23:
            e=ValueTracker(.002);delta=ValueTracker(0)
            self.put(self.plane(),self.vec(RIGHT,BLUE,'a₁'),self.vec(np.array([1.,.002,0]),GREEN,'a₂'),self.vec(P0,TEAL,'p'))
            self.coefficient_display(e,delta)
            self.animate(delta.animate.set_value(.001),d=2)
            self.put(label('목표의 y좌표: 1 → 1.001\n계수: ±500 → ±500.5',24,ORANGE,8 if SHORT else 6.6).move_to([0,-4.8,0] if SHORT else [3.7,-1.6,0]))
        elif i==24:
            self.route('both','조건수 제곱  ↔  직교변환 · 후진대입')
            self.put(label('안정적인 Householder QR 기준',22,TEAL,8).move_to([0,-4,0] if SHORT else [0,-2.75,0]))
        elif i==25:self.route('both','열 전체 계수 · 정확한 산술 → 같은 최소제곱 해')
        elif i==26:
            # Qualitative finite-precision illustration; both paths have nonzero error.
            self.put(label('유한 정밀도 계산 · 개념도',27,MUTED).move_to([0,3.5 if SHORT else 1.8,0]))
            center=np.array([0,1,0]);self.put(Dot(center,color=TEAL,radius=.09),label('정확한 해',24,TEAL).next_to(Dot(center),UP,buff=.4))
            self.put(Dot(center+[-.4,-.15,0],color=YELLOW,radius=.07),Dot(center+[.18,-.1,0],color=BLUE,radius=.07))
            self.formula('오차는 문제 · 알고리즘 · 정밀도에 좌우됩니다','QR도 항상 오차가 0인 것은 아닙니다')
        else:
            self.route('qr','같은 수학적 해 · 다른 수치적 안정성')
