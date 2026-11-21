"""One nonlinear pendulum model shared by physical, force, and prediction views."""
import numpy as np
class PendulumModel:
 def __init__(self,length=2.,g=9.81,theta0=.65,omega0=0.,duration=200.,dt=.002):
  self.length=length;self.g=g;self.dt=dt
  self.times=np.arange(0,duration+dt,dt);self.states=np.empty((len(self.times),2));self.states[0]=[theta0,omega0]
  def f(y):return np.array([y[1],-g/length*np.sin(y[0])])
  for i in range(1,len(self.times)):
   y=self.states[i-1];a=f(y);b=f(y+dt*a/2);c=f(y+dt*b/2);d=f(y+dt*c)
   self.states[i]=y+dt*(a+2*b+2*c+d)/6
 def state_at(self,t):
  t=np.clip(t,0,self.times[-1]);return tuple(np.interp(t,self.times,self.states[:,i]) for i in range(2))
 def energy(self):return .5*self.length**2*self.states[:,1]**2+self.g*self.length*(1-np.cos(self.states[:,0]))
