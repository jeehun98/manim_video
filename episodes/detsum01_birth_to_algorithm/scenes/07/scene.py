import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import SummaryScene
class Shot07(SummaryScene):
    index=7

    def s07(self):
        from visuals import board, eq, tx, basis, geometry, np, VGroup, UpdateFromAlphaFunc, RED, GREEN
        b=board([[3,1],[1,3]])
        self.add(b)
        self.morph(b,[[3,3],[1,1]],2.2)
        self.show(eq(r'\det(A)=0',-2.7,51,RED),d=.4)
        self.to(47)
        self.clear(.25)
        original=np.array([[-1.5,-.2,0],[1.5,-.2,0],[1.5,2.8,0],[-1.5,2.8,0]])
        def figure(alpha):
            points=original.copy();points[:,0]*=1-2*alpha
            color=GREEN if alpha<.5 else RED
            return VGroup(geometry.outline(points,color),basis.arrows(list(points),c=color),*[eq(str(j+1),p[1],27,color,x=p[0]) for j,p in enumerate(points)])
        g=figure(0);self.add(g)
        self.act(1.2,UpdateFromAlphaFunc(g,lambda m,t:m.become(figure(t))))
        self.show(eq(r'\det(B)=-1',-2.5,50,RED),d=.4)
        self.to(50)
