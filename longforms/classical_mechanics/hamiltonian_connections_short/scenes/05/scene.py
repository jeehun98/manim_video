import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ConnectionScene,VGroup
class Shot05(ConnectionScene):
 index=5
 def geometry(self,t):
  # Hold the prepared state before 94s; start its exact evolution continuously at 94s.
  v,_=self.phase((t-77)*.5,y=3.1,h=2.5,w=5.5)
  g=VGroup(v)
  if t>=81:g.add(self.wave(max(t-94,0)*.35,y=-1.55,h=2.1))
  return g
