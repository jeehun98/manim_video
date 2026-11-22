import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import *
class Shot09(HeatScene):
 index=9
 def geometry(self,t):
  g=super().geometry(t)
  for j,n in enumerate([1,3,5]):
   # Reveal complete exact modal shapes; do not interpolate into a false heat solution.
   g[3+j*3].set_stroke(opacity=float(np.clip((t-155-j*.8)/.7,0,1)))
   if 160<=t<164:g.add(eq(r'\times(-'+str(n*n)+r'\pi^2)',2.55,1.55-j*1.35,24,c=GREEN,w=1.8))
  return g
 def labels(self,t):
  return super().labels(t).add(tx('예시: L=1',-2.6,4.3,20,c=MUTED,w=2))

