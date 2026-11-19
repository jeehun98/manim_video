import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import SummaryScene
class Shot11(SummaryScene):
    index=11

    def s11(self):
        from visuals import basis, eq, tx, np, UP, RED, GREEN
        self.add(basis.cards((0,0,1),0,4.6,.65),eq(r'(\mathbf e_1,\mathbf e_1,\mathbf e_2)',3.3,42,RED))
        M=np.array([[1,1,0],[0,0,1],[0,0,0]])
        flat=basis.cube(M,[0,1.0,0],1.6).shift(UP*1.1)
        self.add(flat,tx('같은 방향이 반복되면',-.2,31,RED),eq('V=0',-1.2,57,RED))
        self.show(eq(r'\det(\mathbf e_1,\mathbf e_2,\mathbf e_3)=1',-2.8,39,GREEN),d=.5)
        self.to(83)
