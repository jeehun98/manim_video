"""Geometrically consistent cube maps, rotations, and fixed-height shears."""
from base import *
from base import QRBase as SharedBase
import itertools
TEAL='#5DE0D1'
A=np.array([[1.,0,1],[1,2,2],[0,0,2]])
Q=np.array([[1.,-1,0],[1,1,0],[0,0,np.sqrt(2)]])/np.sqrt(2)
R=np.array([[np.sqrt(2),np.sqrt(2),3/np.sqrt(2)],[0,np.sqrt(2),1/np.sqrt(2)],[0,0,2.]])
def rot(t):return np.array([[np.cos(t),-np.sin(t),0],[np.sin(t),np.cos(t),0],[0,0,1.]])

class VolumeBase(SharedBase):
    def axes(self):
        g=VGroup()
        for v,n in [(RIGHT,'x'),(UP,'y'),(OUT,'z')]:
            g.add(Line(self.proj(ORIGIN),self.proj(2.3*v),color=MUTED,stroke_opacity=.25,stroke_width=1))
            g.add(label(n,17,MUTED).move_to(self.proj(2.5*v)))
        return g
    def box(self,M,color=BLUE,level=3,opacity=.12):
        cols=[M[:,j] for j in range(level)]
        if level==1:return self.vec(cols[0],color)
        if level==2:
            return VGroup(Polygon(*[self.proj(v) for v in [ORIGIN,cols[0],cols[0]+cols[1],cols[1]]],color=color,fill_color=color,fill_opacity=opacity,stroke_width=2))
        vertices={k:M@np.array(k,dtype=float) for k in itertools.product([0,1],repeat=3)}
        faces=[]
        for axis in range(3):
            other=[j for j in range(3) if j!=axis]
            for side in [0,1]:
                face=[]
                for x,y in [(0,0),(1,0),(1,1),(0,1)]:
                    k=[0,0,0];k[axis]=side;k[other[0]]=x;k[other[1]]=y;face.append(vertices[tuple(k)])
                faces.append(face)
        a=self.az.get_value();e=self.el.get_value();depth=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
        faces.sort(key=lambda f:float(np.mean(f,axis=0)@depth))
        g=VGroup(*(Polygon(*[self.proj(v) for v in f],color=color,fill_color=color,fill_opacity=opacity,stroke_width=1.3,stroke_opacity=.65) for f in faces))
        return g
    def columns(self,M,names=True):
        for j,col in enumerate([BLUE,GREEN,ORANGE]):self.put(self.vec(M[:,j],col,['c₁','c₂','c₃'][j] if names else ''))
    def display(self,M,color=BLUE,level=3):self.put(self.box(M,color,level));return M
    def info(self,s,note='',color=INK):
        pos=[0,-3.55 if self.INDEX<11 else -4.5,0] if SHORT else [3.55,.3 if self.INDEX<11 else -1.9,0]
        if not SHORT and self.INDEX in [10,24]:pos=[0,-2.3,0]
        eq=label(s,31,color,8 if SHORT else 6.8).move_to(pos);self.put(eq)
        if note:self.put(label(note,22,MUTED,8 if SHORT else 6.7).next_to(eq,DOWN,buff=.3))
        return eq
    def panel(self,focus=()):
        center=np.array([0.,-2.45,0]) if SHORT else np.array([3.55,.45,0])
        cells={};g=VGroup(label('R =',27).move_to(center+[-2.7,0,0]))
        for i in range(3):
            for j in range(3):
                s=f'r{["₁","₂","₃"][i]}{["₁","₂","₃"][j]}' if i<=j else '0'
                col=[BLUE,GREEN,ORANGE][i] if i==j else PURPLE if i<j else MUTED
                cell=label(s,27,col,1).move_to(center+[(j-1)*1.2,(1-i)*.65,0])
                if focus and (i,j) not in focus:cell.set_opacity(.25)
                cells[i,j]=cell;g.add(cell)
        for x in [-1.9,1.9]:g.add(Line(center+[x,-1,0],center+[x,1,0],color=MUTED,stroke_width=2))
        self.put(g);return cells
    def connect(self,cells,key,point):
        ar=Arrow(self.proj(point),cells[key].get_center(),buff=.14,color=[BLUE,GREEN,ORANGE][key[0]],stroke_width=2,max_tip_length_to_length_ratio=.06)
        self.animate(GrowArrow(ar),d=.4);self.animate(Indicate(cells[key]),d=.4);self.remove(ar)
    def height2(self,M=R):
        p=M[:,1];foot=np.array([p[0],0.,0])
        self.put(Line(self.proj(foot),self.proj(p),color=GREEN,stroke_width=5),label('|r₂₂|',24,GREEN).move_to(self.proj((p+foot)/2)+[.35,.13,0]),self.rightmark(foot,LEFT,UP))
    def height3(self,M=R):
        p=M[:,2];foot=np.array([p[0],p[1],0.])
        self.put(Line(self.proj(foot),self.proj(p),color=ORANGE,stroke_width=5),label('|r₃₃|',24,ORANGE).move_to(self.proj((p+foot)/2)+[.45,0,0]),self.rightmark(foot,LEFT,OUT))
    def pair(self,left=A,right=R):
        oldcenter=self.center.copy();oldscale=self.scale3
        centers=[np.array([-3.8,.8,0]),np.array([.4,.8,0])] if SHORT else [np.array([-6.4,-.6,0]),np.array([.7,-.6,0])]
        self.scale3=.65 if SHORT else .8
        for center,M,col,n in zip(centers,[left,right],[BLUE,PURPLE],['A · 부피 4','R · 부피 4']):
            self.center=center;self.put(self.box(M,col));self.put(label(n,24,col,3.8).move_to(center+[1.5,2.65,0]))
        self.center=oldcenter;self.scale3=oldscale
    def shot(self):
        i=self.INDEX
        self.center=np.array([-3.,1.1,0]) if SHORT else np.array([-6.,-.65,0]);self.scale3=1.22 if SHORT else .85
        if 11<=i<=17:self.el.set_value(65*DEGREES)
        if i in [0,1]:
            self.center=np.array([-1.6,.6,0]) if SHORT else np.array([-4.8,-.3,0]);self.scale3=2.1 if SHORT else 1.6
        if i in [0,1]:
            self.display(np.eye(3),MUTED)
            for j,v in enumerate([RIGHT,UP,OUT]):self.put(self.vec(v,INK,['e₁','e₂','e₃'][j] if i==0 else '1'))
            self.info('det A = ?' if i==0 else 'V₀ = 1 × 1 × 1 = 1','변환 전 기준 부피')
        elif i==2:
            t=ValueTracker(0)
            self.put(always_redraw(lambda:self.box((1-t.get_value())*np.eye(3)+t.get_value()*A,BLUE)))
            for j,col in enumerate([BLUE,GREEN,ORANGE]):self.put(always_redraw(lambda j=j,col=col:self.vec(((1-t.get_value())*np.eye(3)+t.get_value()*A)[:,j],col,['a₁','a₂','a₃'][j])))
            self.animate(t.animate.set_value(1),d=3)
            self.info('Aeᵢ = aᵢ','모든 꼭짓점에 같은 선형변환 A를 적용')
        elif i==3:
            self.put(always_redraw(lambda:self.box(A,BLUE)),self.box(np.eye(3),MUTED,opacity=.035))
            self.animate(self.az.animate.set_value(-43*DEGREES),d=2)
            self.info('단위 정육면체 → 평행육면체')
        elif i==4:
            self.display(A,BLUE);self.info('V = |det A| × V₀','V₀ = 1   →   V = 4',BLUE)
        elif i==5:
            self.display(A,BLUE);self.columns(A,False)
            self.info('길이 · 기울어짐 · 수직 높이','부피를 결정하는 성분만 분리할 수 있을까?')
        elif i==6:
            self.display(A,BLUE);self.info('A = QR','직교변환 Q × 위삼각변환 R',TEAL)
        elif i==7:
            t=ValueTracker(0);self.put(always_redraw(lambda:self.box((1-t.get_value())*np.eye(3)+t.get_value()*R,PURPLE)))
            self.animate(t.animate.set_value(1),d=1.1)
            self.info('x  →  Rx  →  QRx','먼저 R, 그다음 Q')
        elif i in [8,9]:
            angle=ValueTracker(0 if i==8 else PI/4)
            self.put(always_redraw(lambda:self.box(rot(angle.get_value())@R,TEAL)))
            self.animate(angle.animate.set_value(PI/4 if i==8 else 0),d=2)
            self.info('Q: 회전 · 반사' if i==8 else '|det Q| = 1','이번 Q는 45° 회전 · 부피 4 → 4' if i==8 else '길이 · 각도 · 부피가 그대로',TEAL)
        elif i==10:
            self.pair();self.info('|det A| = |det R|','방향이 달라도 부피 배율은 4')
        elif i==11:
            self.put(self.vec(R[:,0],BLUE,'Re₁'));self.panel([(0,0)]);self.info('Re₁ = (r₁₁, 0, 0)')
        elif i==12:
            self.put(self.vec(R[:,0],BLUE,'|r₁₁|'));c=self.panel([(0,0)])
            self.connect(c,(0,0),.5*R[:,0]);self.info('밑변 길이 = |r₁₁|','이 예시에서는 √2',BLUE)
        elif i==13:
            self.display(R,BLUE,2);self.put(self.vec(R[:,0],BLUE,''));self.animate(Create(self.vec(R[:,1],GREEN,'Re₂')),d=1)
            self.panel([(0,0),(1,1)]);self.info('두 열벡터가 만드는 평행사변형')
        elif i==14:
            t=ValueTracker(R[0,1])
            def shear():
                M=R.copy();M[0,1]=t.get_value();return self.box(M,GREEN,2)
            self.put(always_redraw(shear))
            for v in [.2,2.,R[0,1]]:self.animate(t.animate.set_value(v),d=.85)
            self.panel([(0,1)]);self.info('r₁₂ 변화   ·   넓이 S = 2 유지','밑변과 수직 높이는 고정',PURPLE)
        elif i in [15,16,17]:
            self.display(R,GREEN,2);self.put(self.vec(R[:,0],BLUE,''));self.height2()
            c=self.panel([(0,0),(1,1)])
            if i==15:self.info('넓이 = 밑변 × 수직 높이')
            elif i==16:
                self.connect(c,(1,1),np.array([R[0,1],R[1,1]/2,0.]));self.info('수직 높이 = |r₂₂|','두 번째 벡터 자체의 길이와 구별',GREEN)
            else:self.info('S = |r₁₁| × |r₂₂|','√2 × √2 = 2',GREEN)
        elif i==18:
            self.display(R,GREEN,2);self.animate(Create(self.vec(R[:,2],ORANGE,'Re₃')),d=.9)
            self.panel([(2,2)]);self.info('밑면 밖으로 뻗는 세 번째 열')
        elif i in [19,20,21]:
            self.display(R,BLUE);self.put(self.box(R,GREEN,2));self.height3()
            c=self.panel([(0,0),(1,1),(2,2)])
            if i==19:self.info('V = S × h','밑면 넓이 × 평면에서 벗어나는 수직 높이')
            elif i==20:
                self.connect(c,(2,2),np.array([R[0,2],R[1,2],1.]));self.info('h = |r₃₃|','세 번째 벡터 자체의 길이와 구별',ORANGE)
            else:
                self.height2();self.put(self.vec(R[:,0],BLUE,''));self.info('V = |r₁₁r₂₂r₃₃|','√2 × √2 × 2 = 4',ORANGE)
        elif i==22:
            t=ValueTracker(0)
            def shear3():
                M=R.copy();M[0,2]=R[0,2]+.6*np.sin(t.get_value());M[1,2]=R[1,2]+.5*np.sin(t.get_value());return self.box(M,BLUE)
            self.put(always_redraw(shear3));self.animate(t.animate.set_value(TAU),d=2.7)
            self.panel([(0,2),(1,2)]);self.info('r₁₃ · r₂₃ 변화   ·   부피 4 유지','윗면을 밑면과 평행하게 이동',PURPLE)
        elif i==23:
            self.display(R,BLUE);self.height2();self.height3();self.put(self.vec(R[:,0],BLUE,'|r₁₁|'));self.panel([(0,0),(1,1),(2,2)])
            self.info('밑변 · 평면 안 높이 · 평면 밖 높이','세 길이를 고정하면 부피도 고정')
        elif i==24:
            self.pair();self.info('|det A| = |r₁₁r₂₂r₃₃|','두 도형의 부피는 모두 4',ORANGE)
        elif i==25:
            self.display(R,BLUE);self.put(self.box(np.eye(3),MUTED,opacity=.025));self.height2();self.height3();self.put(self.vec(R[:,0],BLUE,'|r₁₁|'))
            c=self.panel([(0,0),(1,1),(2,2)])
            for k,p in [((0,0),.5*R[:,0]),((1,1),np.array([R[0,1],R[1,1]/2,0.])),((2,2),np.array([R[0,2],R[1,2],1.]))]:self.connect(c,k,p)
            self.info('독립 방향마다 쌓이는 부피','직교 길이 세 개의 곱',ORANGE)
        else:
            self.display(R,BLUE);self.height2();self.height3();self.panel([(0,0),(1,1),(2,2)])
            self.info('A = QR','행렬식: 전체 부피 · QR: 부피의 기하학적 구성',ORANGE)
