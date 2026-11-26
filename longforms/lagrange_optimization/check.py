"""Fast algebra, normal/tangent and exact timeline checks; no remote claims."""
from pathlib import Path
import json
import numpy as np
from visuals import F,grad,level,f,df
R=Path(__file__).resolve().parent
rng=np.random.default_rng(426)
for x,y in rng.uniform(-5,8,(100,2)):
 assert np.isclose(F(x,y),19-(x-y-1)**2-2*(y-3)**2)
 assert np.isclose(f(x),F(x,3))
 eps=1e-5
 assert np.allclose(grad(x,y),[(F(x+eps,y)-F(x-eps,y))/(2*eps),(F(x,y+eps)-F(x,y-eps))/(2*eps)])
for c in [13,15,16,17,18]:
 for t in np.linspace(0,2*np.pi,30):
  x,y=level(c,t);assert np.isclose(F(x,y),c)
  tangent=(level(c,t+1e-5)-level(c,t-1e-5))/2e-5
  assert abs(grad(x,y)@tangent)<1e-7
assert F(2,2)==16 and F(4,3)==19 and np.all(grad(2,2)==[2,2])
assert np.isclose(F(2.4,2.2)-F(2,2),1.08)
assert np.isclose(grad(2,2)@[.4,.2],1.2)
for x in np.linspace(0,4,100):
 y=4-x;assert np.isclose(np.array([y,x])@[1,-1],4-2*x);assert x*y<=4+1e-10
assert 2*2==4 and 0*4==4*0==0
timing=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
assert timing[0]['start']==0 and timing[-1]['end']==426
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
print('PASS: algebra, finite differences, level curves, orthogonality, rectangle boundaries, sentence continuity')
