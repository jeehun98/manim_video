import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ChapterScene
class Shot04(ChapterScene):
 index=4
 def prepare(self):
  super().prepare()
  def replace_group(target):
   # Updater replacement avoids accumulating faded alignment clones after mesh→plot cuts.
   self.dynamic.submobjects=target.submobjects
   return self.dynamic
  self.dynamic.become=replace_group
 def get_moving_mobjects(self,*animations):
  # Re-evaluate families from live roots; do not retain children replaced by the updater.
  return list(self.mobjects)
 def get_moving_and_static_mobjects(self,animations):
  # Cairo must traverse live roots each frame, not retain a snapshot of their children.
  return list(self.mobjects),[]
 def labels(self,t):
  g=super().labels(t)
  if t>=126:
   g[0].set_y(2.9)
   g[2].scale(22/30).set_y(2.5)
  return g
