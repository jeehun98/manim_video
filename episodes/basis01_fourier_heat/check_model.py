"""Numerical checks independent of animation timings and curve sampling."""
import json
from pathlib import Path
import numpy as np

P=Path(__file__).resolve().parent
A=np.array([1.,.15,-.2]);n=np.arange(1,4);alpha=.18
def u(x,t):return sum(a*np.exp(-alpha*k*k*t)*np.sin(k*x) for k,a in zip(n,A))
x=np.linspace(.01,np.pi-.01,181);h=1e-4
residual=[]
for t in [0.1,.7,2,5]:
    ut=(u(x,t+h)-u(x,t-h))/(2*h)
    uxx=(u(x+h,t)-2*u(x,t)+u(x-h,t))/h**2
    residual.append(float(np.max(np.abs(ut-alpha*uxx))))
assert max(residual)<1e-6,residual
for t in np.linspace(0,10,101):
    assert abs(u(0,t))<1e-12 and abs(u(np.pi,t))<1e-12
    assert np.min(u(np.linspace(0,np.pi,1001),t))>-1e-12
energies=[float(np.trapezoid(u(np.linspace(0,np.pi,1001),t)**2,np.linspace(0,np.pi,1001))) for t in [0,.5,1,2,5]]
assert all(a>b for a,b in zip(energies,energies[1:])),energies
ratios=np.exp(-alpha*n*n*2)
assert ratios[0]>ratios[1]>ratios[2]
d=json.loads((P/'script.json').read_text(encoding='utf-8'))
raw=[v.strip() for v in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if v.strip()]
assert len(d['sentences'])==34 and len(raw)==68
for i,s in enumerate(d['sentences']):assert s['text']==raw[2*i] and s['end']==int(raw[2*i+1])
for key in ['sentences','scenes']:
    items=d[key];assert items[0]['start']==0 and items[-1]['end']==175
    assert all(a['end']==b['start'] for a,b in zip(items,items[1:]))
assert len((P/'captions.srt').read_text(encoding='utf-8').strip().split('\n\n'))==34
report=dict(heat_equation_finite_difference_max_residual=max(residual),fixed_endpoint_boundary='passed',nonnegative_temperature_excess='passed',decreasing_energy=energies,modal_remaining_fractions_at_t2=ratios.tolist(),source_text_and_all_34_end_times='exact match',scene_and_caption_continuity='0–175s; passed',model=dict(L='pi',alpha=alpha,coefficients=A.tolist()),sources=['https://math.mit.edu/~gs/cse/websections/cse41.pdf','https://bmild.github.io/fourfeat/'])
(P/'model_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Heat equation, boundary conditions, modal decay, source text and timings: passed')
