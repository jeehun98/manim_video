"""Revision 2: point → line → plane → space → columns of R."""
from helpers import *

class QRBase(Helpers):
    def axes(self):
        if self.INDEX in [0,1,22]:return VGroup()
        return super().axes()
    def space(self,level=1,original=True,basis=True):
        self.put(Line(self.proj(-1.5*A1),self.proj(2*A1),color=BLUE,stroke_width=2,stroke_opacity=.65))
        if level>=2:self.put(always_redraw(self.plane))
        if level>=3:self.put(self.grid3())
        if original:self.original(tuple(range(level)),opacity=.65)
        if basis:
            self.put(self.vec(Q1,BLUE,'q₁'))
            if level>=2:self.put(self.vec(Q2,GREEN,'q₂'))
            if level>=3:self.put(self.vec(Q3,ORANGE,'q₃'))
    def caption_formula(self,s,note='',color=INK):
        if self.INDEX<14 or self.INDEX==22:
            pos=[0,-3.65,0] if SHORT else [0,-2.3,0]
            eq=label(s,31,color,8 if SHORT else 13).move_to(pos);self.put(eq)
            if note:self.put(label(note,22,MUTED,8 if SHORT else 13).next_to(eq,DOWN,buff=.3))
            return eq
        return self.formula(s,note,color)
    def fill(self,cells,column):
        for row in range(3):
            v=VALUES[row][column];col=MUTED if v=='0' else INK
            self.animate(Transform(cells[row,column],label(v,29,col,1.05).move_to(cells[row,column])),d=.2)
    def shot(self):
        i=self.INDEX
        if i<14:
            self.center=np.array([-.7,1.1,0]) if SHORT else np.array([-1,-.7,0]);self.scale3=1.65 if SHORT else 1.15
        if i in range(5,10):self.el.set_value(68*DEGREES)
        first=[(0,0),(1,0),(2,0)];second=first+[(0,1),(1,1),(2,1)]
        if i==0:
            g,c=self.matrix(all_known=True)
            for k,v in c.items():
                if k[0]<=k[1]:v.set_opacity(.35)
            if SHORT:g.shift(UP*3.4).scale(1.2)
            else:g.move_to([0,.2,0]).scale(1.1)
            for k in [(1,0),(2,0),(2,1)]:self.animate(Indicate(c[k],color=RED,scale_factor=1.25),d=.5)
            self.caption_formula('왜 아래쪽만 0일까?',color=ORANGE)
        elif i==1:
            self.put(Dot(self.proj(ORIGIN),color=INK,radius=.075),label('O',25).move_to(self.proj(ORIGIN)+[.25,-.3,0]))
            self.caption_formula('0차원 · 원점','아직 독립 방향이 없습니다')
        elif i==2:
            self.put(Dot(self.proj(ORIGIN),radius=.055))
            self.animate(Create(self.vec(A1,INK,'a₁')),d=1.1)
        elif i==3:
            self.original((0,));self.animate(Create(Line(self.proj(-1.5*A1),self.proj(2*A1),color=BLUE)),d=1.4)
            self.caption_formula('V₁ = span(a₁)','앞뒤로 움직일 수 있는 하나의 직선')
        elif i==4:
            self.space(1,basis=False)
            t=ValueTracker(np.sqrt(2));self.put(always_redraw(lambda:self.vec(Q1*t.get_value(),BLUE,'q₁')))
            self.animate(t.animate.set_value(1),d=1.5)
            self.caption_formula('a₁ = r₁₁q₁','기준 방향 1개 · q₁의 길이는 1',BLUE)
        elif i==5:
            self.space(1);self.animate(Create(self.vec(A2,INK,'a₂')),d=1.2)
            self.caption_formula('첫 번째 직선에서 벗어난 벡터')
        elif i==6:
            self.space(1);self.original((1,))
            poly=Polygon(*[self.proj(v) for v in [ORIGIN,A1,A1+A2,A2]],color=PURPLE,fill_opacity=.12)
            self.animate(Create(poly),d=1)
            self.animate(FadeOut(poly),FadeIn(self.plane()),d=1.2)
            self.caption_formula('V₂ = span(a₁, a₂)','기존 직선을 포함하는 평면')
        elif i==7:
            self.space(2,basis=False)
            point=Dot(self.proj(ORIGIN),color=ORANGE,radius=.07);self.put(point)
            for v in [.8*A1,-.6*A1,np.array([-.7,1.4,0]),np.array([1.6,-.4,0]),A2]:self.animate(point.animate.move_to(self.proj(v)),d=.65)
            self.caption_formula('독립 방향 1개 → 독립 방향 2개','직선 밖으로도 움직일 수 있습니다')
        elif i==8:
            self.space(2,basis=False);self.put(self.vec(Q1,BLUE,'q₁'))
            proj=self.vec(A1,PURPLE,'',dashed=True);self.put(proj)
            t=ValueTracker(1);residual=always_redraw(lambda:self.vec(np.array([-1.,1,0]),GREEN,'',origin=A1*t.get_value()));self.put(residual)
            self.animate(FadeOut(proj),t.animate.set_value(0),d=1.2)
            self.remove(residual);self.stage.remove(residual)
            length=ValueTracker(np.sqrt(2));self.put(always_redraw(lambda:self.vec(Q2*length.get_value(),GREEN,'q₂')))
            self.animate(length.animate.set_value(1),d=.8);self.mark(Q1,Q2)
            self.caption_formula('기존 방향 성분 제거 → 수직 잔여 방향','남은 벡터를 정규화해서 q₂를 만듭니다',GREEN)
        elif i==9:
            self.space(2,original=False);self.mark(Q1,Q2)
            dot=Dot(self.proj(ORIGIN),color=ORANGE,radius=.06);self.put(dot)
            for v in [1.5*Q1,1.5*Q1+Q2,-Q1+Q2]:self.animate(dot.animate.move_to(self.proj(v)),d=.6)
            self.caption_formula('V₂ = span(q₁, q₂)','서로 직교하는 두 단위 방향')
        elif i==10:
            self.space(2);self.animate(Create(self.vec(A3,INK,'a₃')),d=.9)
        elif i==11:
            self.space(2);self.original((2,))
            p=np.array([1.,2,0]);self.animate(Create(DashedLine(self.proj(p),self.proj(A3),color=ORANGE)),d=1)
            self.caption_formula('기존 평면 밖의 성분 ≠ 0','세 번째 독립 방향이 추가됩니다',ORANGE)
        elif i==12:
            self.space(2);self.original((2,))
            dot=Dot(self.proj([.3,.7,0]),color=ORANGE,radius=.07);self.put(dot)
            self.animate(dot.animate.move_to(self.proj([.3,.7,1.3])),FadeIn(self.grid3()),d=1.4)
            self.caption_formula('1차원 → 2차원 → 3차원','세 벡터의 조합이 만드는 3차원 공간')
        elif i==13:
            self.space(2);self.original((2,),opacity=.3)
            p=np.array([1.,2,0]);proj=self.vec(p,PURPLE,'',dashed=True);self.put(proj)
            t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(2*OUT,ORANGE,'',origin=t.get_value()*p)))
            self.animate(FadeOut(proj),t.animate.set_value(0),d=1.2)
            # Preserve direction while shortening the residual to unit length.
            self.remove(self.stage[-1]);self.stage.remove(self.stage[-1])
            length=ValueTracker(2);self.put(always_redraw(lambda:self.vec(length.get_value()*OUT,ORANGE,'q₃')))
            self.animate(length.animate.set_value(1),d=.9)
            self.mark(Q1,Q3);self.mark(Q2,Q3)
            self.caption_formula('Q = [ q₁  q₂  q₃ ]','기존 평면에 수직인 단위 방향 q₃',ORANGE)
        elif i==14:
            self.space(3);self.matrix();self.formula('원래 벡터의 조합 계수를 찾으면?')
        elif i==15:
            self.space(1);g,c=self.matrix(focus=0)
            t=ValueTracker(1);self.put(always_redraw(lambda:self.vec(Q1*t.get_value(),BLUE,'')))
            self.animate(t.animate.set_value(np.sqrt(2)),d=1.1)
            self.fill(c,0);self.link(c[0,0],A1)
            self.formula('a₁ = r₁₁q₁','다른 두 방향의 성분은 0',BLUE)
        elif i==16:
            if SHORT:self.center=np.array([-.6,1.6,0]);self.scale3=1.15
            self.el.set_value(65*DEGREES);self.space(2);g,c=self.matrix(known=first,focus=1)
            self.animate(Create(self.vec(A1,BLUE,'')),d=.5)
            self.animate(Create(self.vec(np.sqrt(2)*Q2,GREEN,'',origin=A1)),d=.5)
            self.fill(c,1);self.link(c[1,1],A2)
            self.formula('a₂ = r₁₂q₁ + r₂₂q₂','평면에 수직인 q₃ 성분은 0')
        elif i==17:
            self.space(3,original=False);self.original((2,),opacity=.4);g,c=self.matrix(known=second,focus=2)
            v1=1.5*A1;v2=.5*np.array([-1.,1,0])
            for v,col,o in [(v1,BLUE,ORIGIN),(v2,GREEN,v1),(2*OUT,ORANGE,v1+v2)]:self.animate(Create(self.vec(v,col,'',origin=o)),d=.35)
            self.fill(c,2);self.formula('a₃ = r₁₃q₁ + r₂₃q₂ + r₃₃q₃')
        elif i==18:
            self.space(3,original=False);self.original(opacity=.35);g,c=self.matrix(all_known=True)
            for j,v in enumerate([A1,A2,A3]):self.link(c[0,j],v)
            self.formula('벡터 aⱼ의 조합 계수 → R의 j번째 열')
        elif i==19:
            self.space(3,original=False);g,c=self.matrix(all_known=True)
            for j in range(3):
                rect=SurroundingRectangle(VGroup(*(c[r,j] for r in range(3))),color=[BLUE,GREEN,ORANGE][j],buff=.15)
                self.animate(Create(rect),d=.4);self.animate(Indicate(VGroup(*(c[r,j] for r in range(j+1))),color=[BLUE,GREEN,ORANGE][j]),d=.6);self.remove(rect)
            self.formula('직선: 1개   ·   평면: 최대 2개\n공간: 최대 3개','0이 아닌 계수가 들어갈 수 있는 위치')
        elif i==20:
            self.space(2);self.put(self.vec(Q3,ORANGE,'q₃'));g,c=self.matrix(all_known=True)
            self.mark(A1,Q2);self.mark(A1,Q3);self.mark(A2,Q3)
            for k in [(1,0),(2,0),(2,1)]:self.link(c[k])
            self.formula('q₂ᵀa₁ = q₃ᵀa₁ = q₃ᵀa₂ = 0','앞 벡터는 뒤 직교 방향에 성분이 없습니다')
        elif i==21:
            self.bases(True);g,c=self.matrix(all_known=True)
            for k in [(1,0),(2,0),(2,1)]:self.animate(Circumscribe(c[k],color=RED),d=.45)
            self.formula('위삼각행렬 R','공간의 구조가 계수의 구조로')
        elif i==22:
            # Identical projected subspaces on both sides; only vector sets differ.
            oldcenter=self.center.copy();oldscale=self.scale3
            left=np.array([-2.2,1.1,0]) if SHORT else np.array([-4.2,-.8,0])
            right=np.array([2.0,1.1,0]) if SHORT else np.array([3.5,-.8,0])
            self.scale3=.85 if SHORT else 1.15
            self.put(label('원래 벡터 A',24,INK,3.5).move_to(left+[0,2.7,0]),label('직교 기저 Q',24,BLUE,3.5).move_to(right+[0,2.7,0]))
            for level in [1,2,3]:
                groups=[]
                for center,basis in [(left,False),(right,True)]:
                    self.center=center
                    g=VGroup(Line(self.proj(-1.1*A1),self.proj(1.6*A1),color=BLUE,stroke_width=2))
                    if level>=2:g.add(self.plane())
                    if level>=3:g.add(self.grid3())
                    for j in range(level):g.add(self.vec([Q1,Q2,Q3][j] if basis else [A1,A2,A3][j],[BLUE,GREEN,ORANGE][j] if basis else INK,['q₁','q₂','q₃'][j] if basis else ['a₁','a₂','a₃'][j]))
                    groups.append(g)
                if level>1:self.animate(FadeOut(previous),d=.25)
                previous=VGroup(*groups);self.animate(FadeIn(previous),d=.65)
                self.wait(1.1)
            self.center=oldcenter;self.scale3=oldscale
            self.caption_formula('span(a₁, …, aₖ) = span(q₁, …, qₖ)','각 단계의 직선 · 평면 · 공간이 같습니다')
        else:
            self.put(Dot(self.proj(ORIGIN),color=INK,radius=.06));self.bases(True)
            self.animate(Create(Line(self.proj(-1.4*Q1),self.proj(2.5*Q1),color=BLUE)),d=.5)
            self.animate(FadeIn(self.plane()),d=.5);self.animate(FadeIn(self.grid3()),d=.5)
            g,c=self.matrix(all_known=True)
            for j in range(3):self.link(c[0,j],[Q1,Q2,Q3][j])
            self.formula('A = QR','R의 위삼각 구조는 공간의 확장 순서를 기록합니다',ORANGE)
