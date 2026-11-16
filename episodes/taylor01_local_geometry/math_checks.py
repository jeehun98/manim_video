import hashlib,json,math
import numpy as np
from model import coefficients,polynomial,derivative

def validate(folder):
 digest=hashlib.sha256((folder/'model.py').read_bytes()+(folder/'math_checks.py').read_bytes()).hexdigest()
 out=folder/'math_validation.json'
 if out.exists() and json.loads(out.read_text()).get('sha256')==digest:return
 for a in [0.,1.]:
  for n in range(8):
   q=np.polynomial.Polynomial(coefficients(a,n))
   for k in range(n+1):assert np.isclose(q.deriv(k)(0),derivative(a,k),atol=1e-12)
 x=np.linspace(-3,3,601)
 assert np.allclose(polynomial(x,0,5),x-x**3/6+x**5/120)
 assert np.isclose(derivative(1,2),-np.sin(1))
 assert math.factorial(3)==6
 for radius in [.1,.5,1.,2.]:
  xs=np.linspace(-radius,radius,501)
  for n in [1,3,5,7]:
   err=np.abs(np.sin(xs)-polynomial(xs,0,n))
   assert np.max(err)<=radius**(n+2)/math.factorial(n+2)+1e-12
 assert abs(np.sin(.2)-polynomial(.2,0,1))<abs(np.sin(1)-polynomial(1,0,1))
 out.write_text(json.dumps({'sha256':digest,'status':'passed','checks':['Taylor derivative matching at a=0 and a=1 through order 7','factorial coefficient recovery','sin P1/P3/P5/P7 and remainder bounds','second derivative is slope rate; no curvature identity asserted','finite approximation distinguished from infinite-series reconstruction']},indent=2),encoding='utf-8')
