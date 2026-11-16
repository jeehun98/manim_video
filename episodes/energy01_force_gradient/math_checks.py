import hashlib,json
import numpy as np
from model import *

def validate(folder):
 digest=hashlib.sha256((folder/'model.py').read_bytes()+(folder/'math_checks.py').read_bytes()).hexdigest();out=folder/'math_validation.json'
 if out.exists() and json.loads(out.read_text()).get('sha256')==digest:return
 assert gravity_potential(1)==10 and gravity_potential(2)==20
 for dh in [1,2,.1,.001]:assert np.isclose((gravity_potential(.7+dh)-gravity_potential(.7))/dh,10)
 assert gravity_force(1)==-10
 x=np.linspace(-2,2,501);p=np.polynomial.Polynomial([0,0,.5]);assert np.allclose(-p.deriv()(x),force(x))
 for c in [-5,0,2,100]:
  pc=p+c;assert np.allclose(-pc.deriv()(x),force(x))
  for a in [-1.5,0,1.5]:assert np.isclose(tangent(a,a,c),potential(a,c))
 assert force(1.5)<0 and force(-1.5)>0 and force(0)==0 and p.deriv(2)(0)>0
 for a,b in [(0,2),(2,0),(.2,1.8)]:
  dv=gravity_potential(b)-gravity_potential(a);wext=WEIGHT*(b-a);wg=-WEIGHT*(b-a)
  assert np.isclose(wext,dv) and np.isclose(wg,-dv) and np.isclose(wext+wg,0)
 out.write_text(json.dumps({'sha256':digest,'status':'passed','checks':['10 J per meter equals 10 N; gravity sign negative','external versus gravitational work signs for quasistatic lifting','finite differences and derivative limit','potential derivative, tangent contact, and force directions','constant energy offset leaves derivative and force unchanged','strict local minimum; stationarity alone not used as stability proof']},indent=2),encoding='utf-8')
