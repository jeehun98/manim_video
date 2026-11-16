"""Verify finite growth, limits, derivative values and the perpendicular preview."""
from pathlib import Path
import json,numpy as np
from visuals import discrete_growth
R=Path(__file__).resolve().parent
ns=[2,5,10,20,50,100,200,1000]
ends=[float(discrete_growth(1,n)[-1]) for n in ns]
assert all(a<b<np.e for a,b in zip(ends,ends[1:]))
assert np.allclose([1,1.1,1.21,1.331],1.1**np.arange(4))
for n in ns:
    y=discrete_growth(1,n);t=np.arange(n+1)/n
    assert t[0]==0 and t[-1]==1
    assert np.allclose(y[1:]-y[:-1],y[:-1]/n)
tests=[]
for x in [-2,-.5,0,.5,1,2]:
    values=[float(discrete_growth(x,n)[-1]) for n in [10,100,1000,10000]]
    errors=[abs(v-np.exp(x)) for v in values]
    assert all(a>=b for a,b in zip(errors,errors[1:])),(x,errors)
    tests.append(dict(x=x,finite_values=values,limit=float(np.exp(x))))
for x in [-.4,0,np.log(2),1.1]:
    h=1e-5;slope=(np.exp(x+h)-np.exp(x-h))/(2*h)
    assert np.isclose(slope,np.exp(x),rtol=1e-8)
assert np.isclose(np.exp(np.log(2)),2)
for x in np.linspace(.01,2,100):assert 2**x<np.exp(x)<3**x
h=.18;z=1+0j;preview=[z]
for _ in range(3):
    delta=h*1j*z;assert abs((np.conj(z)*delta).real)<1e-12
    z=z+delta;preview.append(z)
assert abs(z)>1 and np.isclose(abs(z),(1+h*h)**1.5)
report=dict(passed=True,finite_growth=dict(zip(map(str,ns),ends)),fixed_interval=[0,1],real_limit_tests=tests,current_value_equals_derivative=True,positive_x_base_ordering=True,finite_perpendicular_preview=[[z.real,z.imag] for z in preview],preview_norm=float(abs(z)),preview_is_not_normalized_to_a_circle=True)
(R/'math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Finite growth, fixed time interval, real limits, derivative equality, base ordering and perpendicular finite steps verified.')
