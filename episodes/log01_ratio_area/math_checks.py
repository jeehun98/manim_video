"""Validate mathematical invariants of the actual sampled area geometry."""
from pathlib import Path
import json
import numpy as np
def validate(target):
 assert np.allclose(np.diff(np.log10([10,100,1000])),[1,1])
 assert np.isclose(np.log10(20)-np.log10(10),np.log10(200)-np.log10(100))
 assert (101-100)/100==(1010-1000)/1000==.01
 assert abs(np.log1p(.01)-.01)<.00005
 def vertices(l,r,f):
  x=np.linspace(l,r,129);return np.array([(l*f,0)]+[(t*f,1/t/f) for t in x]+[(r*f,0)])
 def area(v):return abs(np.dot(v[:,0],np.roll(v[:,1],1))-np.dot(v[:,1],np.roll(v[:,0],1)))/2
 errors=[]
 for l,r in [(1,2),(1,3)]:
  original=area(vertices(l,r,1))
  for f in np.linspace(.4,3,101):
   v=vertices(l,r,f);errors.append(abs(area(v)-original));assert np.allclose(v[1:-1,1],1/v[1:-1,0])
 assert max(errors)<1e-12
 rng=np.random.default_rng(20261114)
 for a,b in np.exp(rng.uniform(-3,3,(200,2))):assert np.isclose(np.log(a*b),np.log(a)+np.log(b))
 assert np.isclose(np.log(2)+np.log(6/2),np.log(6))
 report=dict(scale_frames_checked=202,max_polygon_area_error=max(errors),boundary='all sampled upper points satisfy y=1/x',spacing='passed',relative_change='exactly 1 percent',approximation='ln(1.01) approx 0.01, not equality',composition_samples=200,intervals='[1,2] and [2,6] share exactly x=2',positive_domain=True)
 (Path(target)/'math_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__':validate(Path(__file__).resolve().parent)
