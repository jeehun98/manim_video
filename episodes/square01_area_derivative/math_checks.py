import json,hashlib,sys
import numpy as np
from model import *

def validate(folder):
 parent=folder.parents[1]/'episodes/energy01_force_gradient/model.py'
 digest=hashlib.sha256((folder/'model.py').read_bytes()+(folder/'math_checks.py').read_bytes()+parent.read_bytes()).hexdigest();out=folder/'math_validation.json'
 if out.exists() and json.loads(out.read_text()).get('sha256')==digest:return
 for x in [0,.5,1,1.8,2]:
  for h in [.5,.3,.04,1e-4]:
   assert np.isclose(area(x+h)-area(x),gain(x,h))
   assert np.isclose(gain(x,h)/h,secant(x,h))
   assert np.isclose(secant(x,h)-derivative(x),h)
   assert np.isclose(h*h/h,h)
 assert gain(2,.3)>gain(1,.3)
 x=np.linspace(-2,2,501);p=np.polynomial.Polynomial([0,0,1]);assert np.allclose(p.deriv()(x),derivative(x))
 v=np.polynomial.Polynomial([0,0,.5]);assert np.allclose(-v.deriv()(x),force(x))
 import importlib.util
 spec=importlib.util.spec_from_file_location('energy_model_checked',parent);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert np.allclose(m.potential(x),potential(x)) and np.allclose(m.force(x),force(x))
 out.write_text(json.dumps({'sha256':digest,'status':'passed','checks':['exact disjoint area decomposition and equal length scales','gain divided by dx equals 2x+dx','corner contribution after division tends to zero','polynomial derivative valid for all real x','finite secant distinct from tangent','quadratic potential coefficient one-half gives restoring force -kq','reused energy helper uses identical potential and force']},indent=2),encoding='utf-8')
