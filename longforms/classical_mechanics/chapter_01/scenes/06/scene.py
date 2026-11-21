import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene
class Shot06(ChapterScene):
 index=6
 def geometry(self,t):
  g=super().geometry(t)
  # The free-fall reference floor is unnecessary and intersects the common-law formula.
  if 120<=t<127:g.remove(g[5])
  return g
