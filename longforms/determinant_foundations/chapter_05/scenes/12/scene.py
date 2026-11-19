import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import FinaleScene
class Shot12(FinaleScene):
    index=12

    def shot_12(self):
        from visuals import shared, basis, np, tx, eq, Arrow, MUTED, GOLD, GREEN, INK
        m=shared.symbol_grid(5,-4.5,.6)
        self.add(m,tx('행렬',-4.5,-1.4,28,MUTED,w=3))
        volume=basis.cube(np.array([[2,1,0],[0,1,1],[0,0,1]]),[-.3,.5,0],1)
        volume.scale(.8,about_point=np.array([-.3,.5,0])).shift(np.array([-.5,0,0]))
        self.show(volume,tx('공간의 부피와 방향',0,-1.4,26,GOLD,w=4),Arrow([-2.8,.5,0],[-2,.5,0],color=MUTED,buff=0,tip_length=.12),d=.8)
        self.to(131)
        self.show(Arrow([1.9,.5,0],[2.8,.5,0],color=MUTED,buff=0,tip_length=.12),eq(r'\det(A)',4.2,.5,62,INK,w=4),tx('하나의 숫자',4.2,-1.4,28,GREEN,w=4),d=.8)
        self.to(135)
