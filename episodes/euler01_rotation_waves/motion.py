"""One time/angle source for circle coordinates and recorded wave samples."""
import numpy as np
PERIOD=10.
def phase(t):return 2*np.pi*np.asarray(t)/PERIOD
def coordinates(t):
    a=phase(t)
    return np.cos(a),np.sin(a)
def validate():
    t=np.linspace(0,139,8341);x,y=coordinates(t)
    np.testing.assert_allclose(x*x+y*y,1,atol=1e-14)
    np.testing.assert_allclose(x+1j*y,np.exp(1j*phase(t)),atol=1e-14)
    a,b=coordinates(10)
    np.testing.assert_allclose([a,b],[1,0],atol=1e-14)
    xx,yy=coordinates(t+PERIOD)
    np.testing.assert_allclose(xx,x,atol=3e-14);np.testing.assert_allclose(yy,y,atol=3e-14)
    return dict(period=PERIOD,samples=len(t),checks='unit norm, Euler equality, sine/cosine initial values, shared phase, period')
