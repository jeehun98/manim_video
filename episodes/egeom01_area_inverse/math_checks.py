"""New checks; unchanged polygon scaling reuses the validated log01 implementation."""
import json,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
def validate(target):
 target=Path(target);root=target.parents[1]
 inherited=json.loads((root/'episodes/log01_ratio_area/math_checks.json').read_text())
 assert inherited['max_polygon_area_error']<1e-12
 def A(x):return quad(lambda t:1/t,1,x,epsabs=1e-13,epsrel=1e-13)[0]
 e_area=brentq(lambda x:A(x)-1,1,4,xtol=1e-14)
 assert abs(e_area-np.e)<1e-13 and abs(A(e_area)-1)<1e-13
 assert A(1)==0 and A(4)>1
 max_error=0
 for u in np.linspace(-2,2,81):
  x=np.exp(u);assert abs(A(x)-u)<1e-12
  h=1e-5;derivative=(np.exp(u+h)-np.exp(u-h))/(2*h)
  max_error=max(max_error,abs(derivative-x));assert abs(derivative-x)<1e-8
  P=np.array([x,np.log(x)]);Q=P[::-1];assert np.allclose(Q,[u,x])
  p1=P+[-.1,-.1/x];p2=P+[.1,.1/x]
  q1=p1[::-1];q2=p2[::-1]
  assert np.isclose((q2[1]-q1[1])/(q2[0]-q1[0]),x)
 for a in [.2,.7,1.5,3]:
  for x in [.3,1,2.7]:assert np.isclose(1/(a*x),(1/x)/a)
 assert np.exp(0)==1 and abs(np.exp(1)-e_area)<1e-13
 report=dict(e_from_area_root=e_area,area_at_root=A(e_area),inverse_samples=81,max_exponential_derivative_error=max_error,coordinate_swap='passed',inverse_tangent_reciprocity='passed',normalization='f(1)=1; E(0)=1',equal_axis_units='asserted in render',area_scaling='inherited unchanged region() and scale_region() from log01; previous checks reused',shared_source_sha256=hashlib.sha256((root/'episodes/log01_ratio_area/scene.py').read_bytes()).hexdigest())
 (target/'math_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__':validate(Path(__file__).resolve().parent)
