from pathlib import Path
import sys,json,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from longforms.complex_geometry_04.direction import mobius,inverse,derivative,distance,circle_parameters,pattern_centers
rng=np.random.default_rng(27);z=.98*np.sqrt(rng.random(4000))*np.exp(2j*np.pi*rng.random(4000));a=.9*np.sqrt(rng.random(4000))*np.exp(2j*np.pi*rng.random(4000))
q=mobius(z,a)
assert np.max(abs(q))<1
inverse_error=float(np.max(abs(inverse(q,a)-z)));assert inverse_error<1e-12
identity_error=float(np.max(abs((1-abs(q)**2)-(1-abs(a)**2)*(1-abs(z)**2)/abs(1+np.conj(a)*z)**2)));assert identity_error<1e-12
metric_error=float(np.max(abs(abs(derivative(z,a))*(1-abs(z)**2)/(1-abs(q)**2)-1)));assert metric_error<1e-10
assert np.max(abs(derivative(0,a)-(1-abs(a)**2)))<1e-12
boundary=np.exp(1j*np.linspace(0,2*np.pi,300));assert np.max(abs(abs(mobius(boundary,.65))-1))<1e-12
# The boundary is invariant as a set, but e.g. i is not fixed by the chosen map.
assert abs(mobius(1j,.65)-1j)>.1
rho=.16;R=2*np.arctanh(rho);circle_error=0
for a in [.3,.65,.95,.6+.2j]:
 c,r=circle_parameters(a,rho);zs=mobius(rho*boundary,a)
 circle_error=max(circle_error,float(np.max(abs(abs(zs-c)-r))))
 assert np.max(abs(distance(zs,a)-R))<1e-11
assert circle_error<1e-12
steps=np.tanh(np.arange(0,18)*.25);assert np.max(abs(distance(steps[:-1],steps[1:])-.5))<1e-11
rn=1-2.**(-np.arange(0,20));increments=distance(rn[:-1],rn[1:]);exact=np.log((2.**(np.arange(19)+2)-1)/(2.**(np.arange(19)+1)-1))
assert np.max(abs(increments-exact))<1e-10 and np.min(increments)>np.log(2)
centers=pattern_centers();assert np.max(abs(centers))<1
for observer in [0,.25,.65]:
 c,r=circle_parameters(inverse(centers,observer),rho)
 assert np.max(abs(c)+r)<1
 assert np.min(r)>0
report=dict(status='passed',source=dict(url='https://people.math.harvard.edu/~ctm/home/text/class/harvard/213a/17/html/home/course/course.pdf',author='Curtis T. McMullen',sections='2.4: disk automorphisms, hyperbolic metric and isometries'),normalization='ds=2|dz|/(1-|z|²), curvature -1. Relative correction examples use center scale as baseline.',inverse_error=inverse_error,metric_invariance_relative_error=metric_error,circle_boundary_error=circle_error,finite_circles='Exact Euclidean center and radius of Ta(|z|=rho), distinct from hyperbolic center a',ruler='r_n=tanh(n*0.5/2); adjacent hyperbolic distances verified =0.5',halving='r_n=1-2^-n; delta d_n=log((2^(n+2)-1)/(2^(n+1)-1))>log(2), tends to log(2), sum diverges',pattern=dict(circles=len(centers),description='Equal hyperbolic radius circles, generated in enough world rings to reveal circles under observer recentering. Not a tessellation.',observer='Actual inverse disk automorphism on hyperbolic centers; exact finite-circle geometry recalculated each animation frame'),atlas='CLI unavailable: existing knowledge_atlas/data/sources.json missing; unrelated knowledge data unchanged')
(Path(__file__).parent/'math_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Math checks passed;',len(centers),'pattern circles; metric error',metric_error)
