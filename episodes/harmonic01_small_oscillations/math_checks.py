import hashlib,json
import numpy as np
from model import *

def validate(folder):
 digest=hashlib.sha256((folder/'model.py').read_bytes()+(folder/'math_checks.py').read_bytes()).hexdigest();out=folder/'math_validation.json'
 if out.exists() and json.loads(out.read_text()).get('sha256')==digest:return
 p=np.polynomial.Polynomial([0,0,.5,.12,.08]);x=np.linspace(-1.8,1.8,1001)
 assert np.allclose(-p.deriv()(x),force(x))
 assert p.deriv()(0)==0 and p.deriv(2)(0)==1
 assert np.all(x*force(x)<=1e-14)
 for e in [1.,.5,.2]:
  assert np.allclose(scaled(x,e),.5*x*x+.12*e*x**3+.08*e*e*x**4)
 assert np.max(abs(scaled(x,.2)-quadratic(x)))<np.max(abs(scaled(x,1)-quadratic(x)))
 t=np.linspace(0,4*np.pi,1001)
 assert np.allclose(M*acceleration(t),-K*displacement(t))
 assert np.allclose(.5*M*velocity(t)**2+.5*K*displacement(t)**2,.5)
 ec,el=lc_energies(t);assert np.allclose(ec+el,1)
 theta=.2;assert abs(np.sin(theta)-theta)/theta<.007
 mu=2*3/(2+3);assert np.isclose(mu,1.2)
 out.write_text(json.dumps({'sha256':digest,'status':'passed','checks':['exact potential derivative and restoring force signs','nondegenerate minimum Vprime(0)=0 Vsecond(0)=1','normalized small-displacement quadratic limit','analytic motion solves m qddot=-k q and conserves energy','LC electric plus magnetic energy constant','small-angle condition; reduced mass relation']},indent=2),encoding='utf-8')
