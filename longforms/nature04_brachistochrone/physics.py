import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad, cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
X,Y,G=4.,3.,1.
THETA=brentq(lambda t:(t-np.sin(t))/(1-np.cos(t))-X/Y,.01,np.pi)
A=Y/(1-np.cos(THETA)); TC=np.sqrt(A/G)*THETA; TS=np.hypot(X,Y)*np.sqrt(2/(G*Y))
def cycle(theta):return np.array([A*(theta-np.sin(theta)),A*(1-np.cos(theta))])
def deep(x):return Y*x/X+5.5*np.sin(np.pi*x/X)
def slope(x):return Y/X+5.5*np.pi/X*np.cos(np.pi*x/X)
def integrand(u):
    if u<1e-10:return np.sqrt(2*X/G)*np.hypot(1,slope(0))/np.sqrt(slope(0))
    x=X*u*u;return 2*X*u*np.hypot(1,slope(x))/np.sqrt(2*G*deep(x))
TD=quad(integrand,0,1,epsabs=1e-11)[0]
US=np.linspace(0,1,16385);TIMES=cumulative_trapezoid([integrand(u) for u in US],US,initial=0);TIMES*=TD/TIMES[-1]
INVERSE=PchipInterpolator(TIMES,US)
def pos(kind,t):
    if kind=='cycle':return cycle(min(t,TC)*np.sqrt(G/A))
    if kind=='straight':return np.array([X,Y])*min(t/TS,1)**2
    u=float(INVERSE(np.clip(t,0,TD)));x=X*u*u;return np.array([x,deep(x)])
def geometry(kind,u):
    if kind=='cycle':return cycle(THETA*u)
    if kind=='straight':return np.array([X,Y])*u
    return np.array([X*u,deep(X*u)])
def light(y):return np.array([quad(lambda z:np.sqrt(z/(2*A-z)),0,y,epsabs=1e-10)[0],y])
def layers(n):
    ys=np.linspace(0,Y,n+1);v=np.sqrt(2*G*(ys[:-1]+ys[1:])/2);dy=Y/n
    p=brentq(lambda p:np.sum(dy*p*v/np.sqrt(1-(p*v)**2))-X,0,(1-1e-12)/max(v))
    return np.c_[np.r_[0,np.cumsum(dy*p*v/np.sqrt(1-(p*v)**2))],ys],p,v
def metrics():
    return dict(X=X,Y=Y,g=G,a=A,theta=THETA,cycle_time=TC,straight_time=TS,deep_time=TD,deep_length=quad(lambda x:np.hypot(1,slope(x)),0,X)[0],cycle_length=4*A*(1-np.cos(THETA/2)),straight_length=5.)
