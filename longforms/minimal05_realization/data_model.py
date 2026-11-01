"""Independent state integrations and exact linear-system checks for the video."""
from pathlib import Path
import json
import numpy as np
A=-np.eye(2);B=np.ones((2,1));C=np.ones((1,2));T=np.array([[1.,1.],[1.,-1.]])
TIME=np.linspace(0,8,1601)
def input_value(t):
 return 0. if t<1 else 1.4 if t<3 else -.4 if t<5 else 1. if t<6 else .35

def integrate_original(x0=(1.5,.5)):
 x=np.zeros((len(TIME),2));x[0]=x0
 for k in range(len(TIME)-1):
  h=TIME[k+1]-TIME[k];u=input_value((TIME[k]+TIME[k+1])/2)
  def f(v):return A@v+B[:,0]*u
  v=x[k];k1=f(v);k2=f(v+h*k1/2);k3=f(v+h*k2/2);k4=f(v+h*k3);x[k+1]=v+h*(k1+2*k2+2*k3+k4)/6
 return x

def integrate_reduced(z0=2.):
 z=np.zeros(len(TIME));z[0]=z0
 for k in range(len(TIME)-1):
  h=TIME[k+1]-TIME[k];u=input_value((TIME[k]+TIME[k+1])/2)
  def f(v):return -v+2*u
  v=z[k];k1=f(v);k2=f(v+h*k1/2);k3=f(v+h*k2/2);k4=f(v+h*k3);z[k+1]=v+h*(k1+2*k2+2*k3+k4)/6
 return z
X=integrate_original();Z=integrate_reduced();Y_ORIGINAL=(C@X.T)[0];Y_REDUCED=Z
X_ALT=integrate_original((1.2,.8))
def state(t):return np.array([np.interp(t,TIME,X[:,i]) for i in range(2)])
def reduced(t):return float(np.interp(t,TIME,Z))
def verify():
 errors=[float(abs((C@integrate_original(x0).T)[0]-integrate_reduced(sum(x0))).max()) for x0 in [(1.5,.5),(0.,0.),(-2.,3.),(4.,-1.)]]
 assert max(errors)<1e-11
 d_error=float(abs((X[:,0]-X[:,1])-np.exp(-TIME)).max());assert d_error<1e-10
 assert np.allclose(T@A@np.linalg.inv(T),-np.eye(2)) and np.allclose(T@B,[[2],[0]]) and np.allclose(C@np.linalg.inv(T),[[1,0]])
 co=np.column_stack((B,A@B));ob=np.vstack((C,C@A));assert np.linalg.matrix_rank(co)==np.linalg.matrix_rank(ob)==1
 tf_errors=[]
 for s in [0,1,2,1j,2j,1+3j]:tf_errors.append(float(abs((C@np.linalg.solve(s*np.eye(2)-A,B))[0,0]-2/(s+1))))
 assert max(tf_errors)<1e-12
 assert np.dot([1,1],[1,-1])==0
 report=dict(original_A=A.tolist(),original_B=B.tolist(),original_C=C.tolist(),transformed_B=(T@B).tolist(),transformed_C=(C@np.linalg.inv(T)).tolist(),initial_state=[1.5,.5],reduced_initial_state=2,independent_integration_max_output_error=max(errors),difference_free_decay_max_error=d_error,original_controllability_rank=1,original_observability_rank=1,reduced_controllability_rank=1,reduced_observability_rank=1,transfer_function='2/(s+1)',transfer_function_max_error=max(tf_errors),minimal_dimension=1,minimality_reason='Controllable and observable scalar LTI realization; nonconstant transfer function excludes dimension zero.',general_equivalence='Zero-initial-state input-output relation',example_stronger_equivalence='Any x(0), with z(0)=x1(0)+x2(0), gives identical outputs for all inputs by z_dot=-z+2u.',difference_dynamics='d_dot=-d; autonomous decay, no u term; absent from y')
 (Path(__file__).resolve().parent/'math_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
