"""One fixed projectile, admissible histories, signed action and two solvers."""
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.linalg import solve_banded
from scipy.interpolate import CubicSpline
M=G=VX=1.;Y0=.5;VY=2.;DURATION=4.
COEFF=M*np.pi**2/(4*DURATION)
def eta(t):return np.sin(np.pi*np.asarray(t)/DURATION)
def deta(t):return np.pi/DURATION*np.cos(np.pi*np.asarray(t)/DURATION)
def y(t,eps=0):return Y0+VY*np.asarray(t)-G*np.asarray(t)**2/2+eps*eta(t)
def vy(t,eps=0):return VY-G*np.asarray(t)+eps*deta(t)
def q(t,eps=0):return np.array([VX*np.asarray(t),y(t,eps)])
def energy(t,eps=0,vertical=False):
    return .5*M*(vy(t,eps)**2+(0 if vertical else VX**2)),M*G*y(t,eps)
def lagrangian(t,eps=0,vertical=False):
    k,v=energy(t,eps,vertical);return k-v
def action(eps=0,vertical=False):return quad(lambda t:float(lagrangian(t,eps,vertical)),0,DURATION,epsabs=1e-11)[0]
S0=action();SY0=action(vertical=True)
def exact_action(eps=0,vertical=False):return (SY0 if vertical else S0)+COEFF*eps**2
def accumulated(t,eps=0):return quad(lambda s:float(lagrangian(s,eps)),0,t,epsabs=1e-10)[0]
def candidate(t,kind):
    if kind=='straight':return np.array([VX*t,Y0])
    if kind=='low':return np.array([VX*t,Y0-.25*eta(t)])
    return q(t,0 if kind=='actual' else .8)
def retimed_q(t):return q(DURATION*(np.asarray(t)/DURATION)**2)
# Newton's initial-value propagation, independently integrated.
_IVP=solve_ivp(lambda t,z:[z[2],z[3],0,-G],[0,DURATION],[0,Y0,VX,VY],rtol=1e-12,atol=1e-13,dense_output=True)
def newton(t):return _IVP.sol(t)[:2]
# Discrete stationary action, linear potential, fixed endpoint positions/times.
# Derivative of midpoint discrete action: y[i-1]-2y[i]+y[i+1]=-g*dt**2.
GRID=np.linspace(0,DURATION,201);DT=GRID[1]-GRID[0]
AB=np.zeros((3,len(GRID)-2));AB[0,1:]=1;AB[1]=-2;AB[2,:-1]=1
RHS=np.full(len(GRID)-2,-G*DT**2);RHS[0]-=Y0;RHS[-1]-=float(y(DURATION))
Y_EL=np.r_[Y0,solve_banded((1,1),AB,RHS),float(y(DURATION))]
EL=CubicSpline(GRID,Y_EL)
def variational(t):return np.array([VX*np.asarray(t),EL(t)])
def first_variation(eps):
    return quad(lambda t:M*vy(t,eps)*deta(t)-M*G*eta(t),0,DURATION,epsabs=1e-11)[0]
def metrics():return dict(m=M,g=G,T=DURATION,x0=0,y0=Y0,v0x=VX,v0y=VY,full_action=S0,vertical_action=SY0,epsilon_squared_coefficient=COEFF,lagrangian_roots=[2-np.sqrt(2),2+np.sqrt(2)],energy=float(sum(energy(0))))
