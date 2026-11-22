"""Verify the mathematical examples and sampled vertical bounds."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.integrate import quad
from mechanics import *
R=Path(__file__).resolve().parent
assert inner(U,V)==0 and inner(U,V,4)==3
assert abs(angle()-90)<1e-12 and abs(angle(w=4)-53.13010235415598)<1e-10
assert np.allclose(TRANSFORM@U,[2,1]) and np.allclose(TRANSFORM@V,[2,-1])
assert np.allclose(TRANSFORM.T@TRANSFORM,gram(4))
rng=np.random.default_rng(22)
for _ in range(100):
 u,v=rng.normal(size=(2,2));a=float(rng.normal());assert np.allclose(TRANSFORM@(u+v),TRANSFORM@u+TRANSFORM@v);assert np.allclose(TRANSFORM@(a*u),a*(TRANSFORM@u))
 assert inner(u,u,4)>0 and abs(inner(u,v,4)-inner(v,u,4))<1e-10
u=np.array([1,1]);v=np.array([2,0]);q=projection(u,v);assert np.allclose(q,[1,0]) and inner(u-q,v)==0
errors=[dict(n=n,l2_error=l2_error(n),uniform_error_upper_bound=error_bound(n)) for n in range(8)]
assert all(x['l2_error']<=x['uniform_error_upper_bound'] for x in errors)
assert all(x['l2_error']>y['l2_error'] for x,y in zip(errors,errors[1:]))
x=np.linspace(0,1,201)
for n in range(8):assert np.max(abs(np.exp(x)-taylor(x,n)))<=error_bound(n)
# Tail distances are controlled by ||p_m-p_n||₂ <= ||p_m-e^x||₂+||p_n-e^x||₂.
for n in range(8):
 for m in range(n+1,8):assert np.sqrt(quad(lambda x:(float(taylor(x,m)-taylor(x,n)))**2,0,1)[0])<=error_bound(m)+error_bound(n)
fourier=quad(lambda x:np.sin(x)*np.cos(x),-np.pi,np.pi)[0];assert abs(fourier)<1e-12
from visuals import HilbertScene
samples=0
for i,m in enumerate(json.loads((R/'manifest.json').read_text(encoding='utf-8')),1):
 scene=HilbertScene();scene.index=i
 for t in np.arange(m['start'],m['start']+m['duration_seconds'],.5):
  for name,g in [('labels',scene.labels(float(t))),('geometry',scene.geometry(float(t)))]:
   if len(g):assert g.get_left()[0]>=-4.05 and g.get_right()[0]<=4.05 and g.get_bottom()[1]>=-4.7 and g.get_top()[1]<=6.4,(i,t,name,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
  samples+=1
report=dict(standard_inner_product=inner(U,V),weighted_inner_product=inner(U,V,4),standard_norm=norm(U),weighted_norm=norm(U,4),weighted_angle_degrees=angle(w=4),projection=q.tolist(),taylor_errors=errors,convergence_argument='Uniform Taylor remainder <= e/(n+1)! implies L2 convergence on [0,1] and Cauchy. Every derivative of exp is nonzero, so exp is not any finite-degree polynomial. L2 uniqueness excludes an alternative polynomial limit.',completion='P[0,1] completes to real L2[0,1], functions identified a.e.; all Cauchy limits, not one added function.',sin_cos_integral=fourier,layout_samples=samples,mechanics_sha256=hashlib.sha256((R/'mechanics.py').read_bytes()).hexdigest(),sources=['https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-08-25-slides.html','https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/8fb8d5c170f1613151aca71de21027bc_MIT18_102s21_full_lec.pdf'])
(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
