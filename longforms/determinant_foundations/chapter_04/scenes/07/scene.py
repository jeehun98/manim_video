import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import EliminationScene,eq,GREEN
class Shot07(EliminationScene):
    index=7
    def show(self,*objects,d=.5):
        # Render the product symbol with TeX; the Korean font lacks this glyph.
        objects=[eq(r'\det(U)=\prod_i u_{ii}',3,.45,30,GREEN,w=5.7) if '일반형' in getattr(obj,'text','') else obj for obj in objects]
        return super().show(*objects,d=d)
