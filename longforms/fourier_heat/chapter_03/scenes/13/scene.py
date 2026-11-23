import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import PropertiesScene
from manim import Line
class Shot13(PropertiesScene):
 index=13
 def geometry(self,t):
  g=super().geometry(t)
  # At the narrow initial peak, put A outside the formula's bounding box.
  g[2].move_to([-3.5,1.1,0])
  g.add(Line([-3.2,1.1,0],g[1][1].get_center(),stroke_color='#4A9EFF',stroke_opacity=.35,stroke_width=1.5))
  return g
