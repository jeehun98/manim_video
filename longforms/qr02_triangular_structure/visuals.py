"""Space → inner product → matrix entry, using a common 3D model."""
from base import *
from base import QRBase as SharedBase
RED='#FF777E'
VALUES=[['r₁₁','r₁₂','r₁₃'],['0','r₂₂','r₂₃'],['0','0','r₃₃']]
class QRBase(SharedBase):
    def original(self,indices=(0,1,2),opacity=1):
        for j in indices:self.put(self.vec([A1,A2,A3][j],INK,['a₁','a₂','a₃'][j],opacity=opacity))
    def matrix(self,known=(),focus=None,all_known=False,numeric=False):
        c=np.array([0.,-2.55,0]) if SHORT else np.array([3.65,.15,0])
        dx=1.32;dy=.7
        cells={};g=VGroup()
        vals=[['√2','√2','3/√2'],['0','√2','1/√2'],['0','0','2']] if numeric else VALUES
        for row in range(3):
            for col in range(3):
                s=vals[row][col] if all_known or (row,col) in known else '?'
                color=RED if row>col and s=='0' else INK
                cell=label(s,29,color,1.05).move_to(c+[(col-1)*dx,(1-row)*dy,0])
                if focus is not None and col!=focus:cell.set_opacity(.35)
                cells[row,col]=cell;g.add(cell)
        for x in [-2.05,2.05]:
            g.add(Line(c+[x,-1.12,0],c+[x,1.12,0],color=MUTED,stroke_width=2))
            inward=.16 if x<0 else -.16
            g.add(Line(c+[x,-1.12,0],c+[x+inward,-1.12,0],color=MUTED),Line(c+[x,1.12,0],c+[x+inward,1.12,0],color=MUTED))
        g.add(label('R =',28).move_to(c+[-2.65,1.45,0]))
        for j in range(3):g.add(label(['a₁','a₂','a₃'][j],20,MUTED).move_to(c+[(j-1)*dx,1.45,0]))
        for j,col in enumerate([BLUE,GREEN,ORANGE]):g.add(label(['q₁','q₂','q₃'][j],20,col).move_to(c+[-2.45,(1-j)*dy,0]))
        self.put(g);return g,cells
    def formula(self,s,note='',color=INK):
        pos=[0,-4.45,0] if SHORT else [3.65,-1.75,0]
        eq=label(s,29,color,8 if SHORT else 6.5).move_to(pos);self.put(eq)
        if note:self.put(label(note,21,MUTED,8 if SHORT else 6.5).next_to(eq,DOWN,buff=.28))
        return eq
    def link(self,cell,source=ORIGIN):
        arc=Arrow(self.proj(source),cell.get_center(),buff=.17,color=PURPLE,stroke_width=2,max_tip_length_to_length_ratio=.07)
        self.animate(GrowArrow(arc),d=.45);self.animate(Indicate(cell,color=RED,scale_factor=1.3),d=.45)
        self.remove(arc)
    def zeros(self,cells,which):
        for k in which:
            old=cells[k];new=label('0',29,RED).move_to(old)
            self.animate(Transform(old,new),d=.35);self.link(old)
            self.animate(old.animate.set_color(MUTED),d=.2)
    def mark(self,u,v):self.put(self.rightmark(ORIGIN,u,v))
    def grid3(self):
        g=VGroup()
        for z in [-.8,.8,1.8]:
            for t in [-1,0,1,2]:
                g.add(Line(self.proj((t,-1,z)),self.proj((t,2,z)),color=PURPLE,stroke_opacity=.17,stroke_width=1),Line(self.proj((-1,t,z)),self.proj((2,t,z)),color=PURPLE,stroke_opacity=.17,stroke_width=1))
        for x,y in [(-1,-1),(-1,2),(2,-1),(2,2)]:g.add(Line(self.proj((x,y,-.8)),self.proj((x,y,1.8)),color=PURPLE,stroke_opacity=.25,stroke_width=1))
        return g
    def shot(self):
        i=self.INDEX
        first=[(0,0),(1,0),(2,0)];second=first+[(0,1),(1,1),(2,1)]
        if i==0:
            self.formula('A = QR','대각선 아래의 세 칸은 왜 0일까?')
            g,c=self.matrix(all_known=True)
            for k in [(1,0),(2,0),(2,1)]:self.animate(Indicate(c[k],color=RED,scale_factor=1.35),d=.55)
        elif i in [1,2,3]:
            self.original(opacity=.3 if i==3 else 1)
            if i==1:
                g,c=self.matrix(all_known=True)
                for j,v in enumerate([A1,A2,A3]):self.link(c[0,j],v)
                self.formula('숫자의 구조 ↔ 공간의 구조')
            elif i==2:
                self.matrix();self.formula('A = [ a₁  a₂  a₃ ]','세 벡터는 선형독립입니다')
            else:
                for q,col,n in [(Q1,BLUE,'q₁'),(Q2,GREEN,'q₂'),(Q3,ORANGE,'q₃')]:self.animate(FadeIn(self.vec(q,col,n)),d=.6)
                for u,v in [(Q1,Q2),(Q1,Q3),(Q2,Q3)]:self.mark(u,v)
                self.matrix();self.formula('Q = [ q₁  q₂  q₃ ]   ·   QᵀQ = I')
        elif i==4:
            self.el.set_value(65*DEGREES)
            self.original((0,));self.put(self.vec(Q1,BLUE,'q₁'))
            t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(t.get_value()*Q1,BLUE,'')))
            self.animate(t.animate.set_value(np.sqrt(2)),d=1.4)
            self.matrix(known=[(0,0)],focus=0);self.formula('a₁ = r₁₁q₁','r₁₁ = √2',BLUE)
        elif i in [5,6,7,8]:
            self.original((0,));self.bases(True)
            g,c=self.matrix(known=[(0,0)],focus=0)
            if i==5:self.formula('a₁ = r₁₁q₁ + ? q₂ + ? q₃')
            elif i==6:
                self.mark(A1,Q2);self.mark(A1,Q3)
                self.formula('a₁ ⟂ q₂    ·    a₁ ⟂ q₃','두 방향 모두 첫 벡터에 수직')
            elif i==7:
                self.el.set_value(65*DEGREES)
                self.put(Dot(self.proj(ORIGIN),color=RED,radius=.07))
                self.mark(A1,Q2)
                eq=self.formula('rᵢⱼ = qᵢᵀaⱼ','q₂와 q₃ 방향의 투영 벡터는 모두 0',PURPLE)
                for q in [Q2,Q3]:
                    probe=Line(self.proj(-.7*q),self.proj(1.5*q),color=PURPLE,stroke_opacity=.5)
                    self.animate(Create(probe),d=.55);self.animate(Indicate(c[1 if q is Q2 else 2,0],color=PURPLE),d=.55);self.remove(probe)
            else:
                self.mark(A1,Q2);self.mark(A1,Q3)
                self.formula('q₂ᵀa₁ = 0   ·   q₃ᵀa₁ = 0','수직인 두 벡터의 내적은 0')
                self.zeros(c,[(1,0),(2,0)])
        elif i in [9,10,11]:
            if i==10:self.el.set_value(65*DEGREES)
            self.original((1,));self.bases(True)
            g,c=self.matrix(known=first+([(0,1),(1,1)] if i>=10 else []),focus=1)
            if i==9:self.formula('두 번째 열 = a₂의 조합 계수')
            elif i==10:
                self.animate(Create(self.vec(A1,BLUE,'')),d=.55)
                self.put(label('r₁₂q₁',22,BLUE).move_to(self.proj(.5*A1)+[.2,-.7,0]))
                self.animate(Create(self.vec(np.sqrt(2)*Q2,GREEN,'',origin=A1)),d=.55)
                self.put(label('r₂₂q₂',22,GREEN).move_to(self.proj(A1+.5*np.sqrt(2)*Q2)+[.45,.15,0]))
                self.formula('a₂ = r₁₂q₁ + r₂₂q₂')
                self.link(c[0,1],A1);self.link(c[1,1],A2)
            else:
                self.put(self.plane(),Dot(self.proj(ORIGIN),color=RED,radius=.07));self.mark(A2,Q3)
                self.formula('r₃₂ = q₃ᵀa₂ = 0','q₃는 처음 두 벡터가 만드는 평면에 수직',ORANGE)
                self.zeros(c,[(2,1)])
        elif i==12:
            self.original((2,),opacity=.6);self.bases(True)
            self.matrix(known=second,focus=2)
            v1=1.5*A1;v2=.5*np.array([-1.,1,0]);v3=2*OUT
            for v,col,n,o,offset in [(v1,BLUE,'r₁₃q₁',ORIGIN,[.7,-.25,0]),(v2,GREEN,'r₂₃q₂',v1,[0,.4,0]),(v3,ORANGE,'r₃₃q₃',v1+v2,[.45,0,0])]:
                self.animate(Create(self.vec(v,col,'',origin=o)),d=.6)
                self.put(label(n,22,col).move_to(self.proj(o+.5*v)+offset))
            self.formula('a₃ = r₁₃q₁ + r₂₃q₂ + r₃₃q₃')
        elif i==13:
            self.original(opacity=.4);self.bases(True)
            g,c=self.matrix()
            for j in range(3):
                for row in range(3):
                    color=MUTED if row>j else INK
                    self.animate(Transform(c[row,j],label(VALUES[row][j],29,color,1.05).move_to(c[row,j])),d=.1)
                self.link(c[0,j],[A1,A2,A3][j])
            self.formula('열 j = aⱼ를 표현하는 계수들')
        elif i==14:
            self.bases(True);g,c=self.matrix(all_known=True)
            self.formula('i > j   ⇒   rᵢⱼ = 0','대각선 아래쪽이 0인 위삼각행렬')
            for k in [(1,0),(2,0),(2,1)]:self.animate(Circumscribe(c[k],color=RED,buff=.12),d=.5)
        elif i==15:
            self.original();self.matrix(all_known=True)
            self.formula('무엇이 그대로 유지될까?',color=PURPLE)
        elif i==16:
            self.el.set_value(65*DEGREES);self.original((0,));self.put(self.vec(Q1,BLUE,'q₁'))
            self.animate(Create(Line(self.proj(-1.5*A1),self.proj(2*A1),color=BLUE,stroke_width=3)),d=1.3)
            self.equation('span(a₁) = span(q₁)','길이는 달라도 같은 직선')
        elif i==17:
            self.put(self.plane());originals=VGroup(self.vec(A1,INK,'a₁'),self.vec(A2,INK,'a₂'));self.put(originals)
            self.animate(originals.animate.set_opacity(.25),FadeIn(self.vec(Q1,BLUE,'q₁')),FadeIn(self.vec(Q2,GREEN,'q₂')),d=1.7)
            self.equation('span(a₁, a₂)\n= span(q₁, q₂)','기준 벡터가 바뀌어도 평면은 그대로')
        elif i==18:
            self.put(self.grid3(),self.plane());self.original(opacity=.35);self.bases(True)
            self.equation('span(a₁, a₂, a₃)\n= span(q₁, q₂, q₃)','같은 3차원 공간을 만드는 두 기저')
        elif i==19:
            self.bases(True)
            self.animate(Create(Line(self.proj(-1.4*Q1),self.proj(2.5*Q1),color=BLUE)),d=.6)
            self.animate(FadeIn(self.plane()),d=.6);self.animate(FadeIn(self.grid3()),d=.6)
            self.equation('V₁ ⊂ V₂ ⊂ V₃','직선 → 평면 → 공간',PURPLE)
        elif i==20:
            self.put(self.grid3(),self.plane());self.original(opacity=.25);self.bases(True)
            self.equation('원래 기준 {a₁, a₂, a₃}\n↓\n직교 기준 {q₁, q₂, q₃}','각 단계의 부분공간은 유지됩니다')
        elif i in [21,22,23]:
            self.original((0,1),opacity=.6);self.bases(True);self.put(self.plane())
            g,c=self.matrix(all_known=True)
            if i==21:
                self.formula('r₂₁ = 0   ·   r₃₁ = 0   ·   r₃₂ = 0')
                for k in [(1,0),(2,0),(2,1)]:self.link(c[k])
            elif i==22:
                self.mark(A1,Q2);self.mark(A1,Q3);self.mark(A2,Q3)
                self.formula('q₃ ⟂ span(a₁,a₂)\nq₂ ⟂ span(a₁)','뒤에 만든 방향은 앞부분 공간에 수직')
            else:
                self.formula('qᵢᵀaⱼ = 0   (i > j)','공간의 수직 관계 → 행렬의 0',PURPLE)
                for k in [(1,0),(2,0),(2,1)]:self.animate(Indicate(c[k],color=RED),d=.35)
        else:
            self.bases(True);self.matrix(all_known=True)
            self.formula('A = QR','위삼각 구조는 공간의 직교 관계를 기록합니다',ORANGE)
