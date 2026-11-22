"""Mathematical and frame-independent layout verification for the new short."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from mechanics import *
R=Path(__file__).resolve().parent
xx=np.linspace(-5,5,501);times=[.002,.01,.1,.25,.45,.9,1.9]
ranges=[]
for t in times:
 v=solution(xx,t);assert v.min()>=20-1e-10 and v.max()<=95+1e-10
 ranges.append(dict(t=t,minimum=float(v.min()),maximum=float(v.max())))
# Independent numerical quadrature of the Gaussian average.
errors=[]
for x in [-2.5,-1.2,0,1.3,3.2]:
 for t in [.05,.45,1.2]:
  v=20+sum(h*quad(lambda z:float(kernel(x-z,t)),a,b,epsabs=1e-10)[0] for a,b,h in INTERVALS)
  errors.append(abs(v-float(solution(x,t))))
assert max(errors)<1e-8
# PDE and tangent derivative finite differences, away from t=0.
pde=[];deriv=[]
for t in [.1,.45,.9]:
 dx=1e-3;dt=1e-5
 ut=(solution(xx,t+dt)-solution(xx,t-dt))/(2*dt)
 uxx=(solution(xx+dx,t)-2*solution(xx,t)+solution(xx-dx,t))/dx**2
 pde.append(float(np.max(abs(ut-K*uxx))))
 deriv.append(float(np.max(abs((solution(xx+dx,t)-solution(xx-dx,t))/(2*dx)-slope(xx,t)))))
assert max(pde)<.001 and max(deriv)<.001
slacks=[]
for t1,t2 in [(.1,.3),(.25,.9),(.45,1.2)]:
 for x in np.linspace(-4,4,17):
  for y in np.linspace(-4,4,17):slacks.append(float(solution(y,t2))-lower(x,y,t1,t2))
assert min(slacks)>0
mc_rng=np.random.default_rng(20);samples=initial(np.sqrt(2*K*T)*mc_rng.normal(size=200000))
mc=float(samples.mean());expected=float(solution(0,T));se=float(samples.std()/np.sqrt(len(samples)));assert abs(mc-expected)<5*se
# Check all label states plus dynamic geometry at 4 Hz; rendering additionally checks every frame.
from visuals import HeatScene
labels=0;geometry=0
for i,m in enumerate(json.loads((R/'manifest.json').read_text(encoding='utf-8')),1):
 scene=HeatScene();scene.index=i
 for t in np.arange(m['start'],m['start']+m['duration_seconds'],.25):
  g=scene.geometry(float(t));ls=scene.labels(float(t));labels+=len(ls);geometry+=1
  for name,obj in [('geometry',g),('labels',ls)]:
   if len(obj):assert obj.get_left()[0]>=-4.05 and obj.get_right()[0]<=4.05 and obj.get_bottom()[1]>=-4.7 and obj.get_top()[1]<=6.4,(i,t,name,obj.get_bottom(),obj.get_top())
report=dict(domain='R, bounded strictly positive step data, kappa=0.65',range=ranges,convolution_max_error=max(errors),pde_max_error=max(pde),tangent_max_error=max(deriv),harnack_min_slack=min(slacks),monte_carlo=dict(n=len(samples),average=mc,exact=expected,standard_error=se),layout_samples=geometry,label_objects=labels,sources=['https://www.math.ias.edu/files/Lecture-No1.pdf','https://math.stanford.edu/~ryzhik/STANFORD/STANF227-12/notes227-09.pdf'])
(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
