import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene
class Shot07(ChapterScene):
 index=7
 def prepare(self):
  super().prepare()
  self.pristine_history=self.history_ax.copy()
  self.pristine_mini=self.mini.copy()
 def geometry(self,t):
  # Keep coordinate conversion axes independent of updater family alignment.
  self.history_ax=self.pristine_history.copy()
  self.mini=self.pristine_mini.copy()
  return super().geometry(t)
