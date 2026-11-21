"""Exact quantum oscillator plus reused classical pendulum. hbar=m=omega=1."""
from pathlib import Path
import importlib.util,numpy as np,json
s=importlib.util.spec_from_file_location('shared_classical_packet',Path(__file__).resolve().parents[1]/'chapter_05/mechanics.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
MODEL,I,A,EC,H,field,contour,packet,INITIAL=m.MODEL,m.I,m.A,m.EC,m.H,m.field,m.contour,m.packet,m.INITIAL
X=np.linspace(-5,5,401)
def phi0(x):return np.pi**(-.25)*np.exp(-np.asarray(x)**2/2)
def psi(x,t=0):return (phi0(x)*np.exp(-.5j*t)+np.sqrt(2)*np.asarray(x)*phi0(x)*np.exp(-1.5j*t))/np.sqrt(2)
def rho(x,t=0):return abs(psi(x,t))**2
def cdf_sample(density,seed,count):
 rng=np.random.default_rng(seed);cdf=np.cumsum(density);cdf=cdf/cdf[-1];return np.interp(rng.random(count),cdf,X)
SAMPLES=cdf_sample(rho(X,0),20261121,240)
INTERFERENCE=np.exp(-X*X/5)*np.cos(3*X)**2
HITS=cdf_sample(INTERFERENCE,20261122,200)
JITTER=np.random.default_rng(6).uniform(-.18,.18,200)
OP_A=np.array([[0.,1.],[1.,0.]])
OP_B=np.diag([1.,2.]);INPUT=np.ones(2)/np.sqrt(2)
if __name__=='__main__':
 x=np.linspace(-9,9,18001);dx=x[1]-x[0];normerr=0;residual=0;expecterr=0
 for t in np.linspace(0,6,19):
  z=psi(x,t);normerr=max(normerr,abs(np.trapezoid(abs(z)**2,x)-1))
  dz=(psi(x,t+1e-5)-psi(x,t-1e-5))/(2e-5)
  hz=-.5*np.gradient(np.gradient(z,dx),dx)+.5*x*x*z
  residual=max(residual,float(np.max(abs(1j*dz[20:-20]-hz[20:-20]))))
  expecterr=max(expecterr,abs(np.trapezoid(x*abs(z)**2,x)-np.cos(t)/np.sqrt(2)))
 assert normerr<1e-10 and residual<3e-6 and expecterr<1e-10,(normerr,residual,expecterr)
 assert np.allclose(OP_A@OP_B@INPUT,[2/np.sqrt(2),1/np.sqrt(2)])
 assert np.allclose(OP_B@OP_A@INPUT,[1/np.sqrt(2),2/np.sqrt(2)])
 assert not np.allclose(OP_A@OP_B,OP_B@OP_A)
 # Ehrenfest for x: d<x>/dt=<p>=-sin(t)/sqrt(2), energy expectation 1.
 report=dict(model='harmonic oscillator, hbar=m=omega=1; (|0>+|1>)/sqrt(2)',norm_error=float(normerr),schrodinger_residual=float(residual),position_expectation_error=float(expecterr),energy_expectation=1,commutator_order_verified=True,commutator_sign='d<A>/dt=<[A,H]>/(i*hbar), explicit time independent A',sampling='independently prepared identical state, Born density',double_slit='conceptual far-field interference envelope, not tracked electron paths')
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
