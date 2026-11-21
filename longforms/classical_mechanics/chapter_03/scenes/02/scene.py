import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene, PERIOD
class Shot02(ChapterScene):
 index=2
 def phase_view(self,ax,u,canonical=True,reveal=1,others=False):
  # Trace ends exactly at the displayed state while the first cycle is being drawn.
  return super().phase_view(ax,u,canonical,min(max(u/PERIOD,0),1),others)
