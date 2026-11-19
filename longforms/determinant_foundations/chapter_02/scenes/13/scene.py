import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import GeometryScene
class Shot13(GeometryScene):
    index=13
    def show(self,*objects,d=.5):
        # This shot's label sits above the diagram, clear of its orientation arrows.
        for obj in objects:
            if '순열' in getattr(obj,'text',''):
                obj.move_to([3,2.15,0])
        return super().show(*objects,d=d)
