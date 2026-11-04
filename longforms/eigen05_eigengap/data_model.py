"""Deterministic80-point PCA examples. Four identical point edits give identical E."""
import numpy as np
N=80;CONTROL_A=2.;INDICES=np.arange(76,80);E=np.array([[0.,.01],[.01,0.]])
C_SMALL=np.diag([1.01,1.]);C_LARGE=np.diag([2.,1.]);C_ROUND=np.diag([1.12,1.]);C_ISO=np.eye(2)
phi=np.deg2rad(25);rot=np.array([[np.cos(phi),-np.sin(phi)],[np.sin(phi),np.cos(phi)]])
C_ELLIPSE=rot@np.diag([3.,.5])@rot.T
rng=np.random.default_rng(20261023);angles=rng.uniform(0,2*np.pi,38);radii=2*np.sqrt(rng.uniform(.05,1,38));z=np.c_[radii*np.cos(angles),radii*np.sin(angles)];z=np.r_[z,-z]
def root(c):
 vals,vecs=np.linalg.eigh(c);assert vals.min()>0
 return (vecs*np.sqrt(vals))@vecs.T
white=z@np.linalg.inv(root(z.T@z/(N-1)))
controls=np.array([[2.,0.],[-2.,0.],[0.,2.],[0.,-2.]])
alpha=2*CONTROL_A**2/(N-1)
def data_for_cov(c):
 residual=c-alpha*np.eye(2);return np.r_[white@root(residual),controls]
def perturb(points,t=1.):
 # Rotate both control pairs toward each other; preserve each diagonal variance.
 theta=.5*np.arcsin(E[0,1]/alpha)*float(t);a=CONTROL_A
 u=np.array([a*np.cos(theta),a*np.sin(theta)]);v=np.array([a*np.sin(theta),a*np.cos(theta)])
 result=points.copy();result[INDICES]=np.array([u,-u,v,-v]);return result
ELLIPSE=data_for_cov(C_ELLIPSE);SMALL=data_for_cov(C_SMALL);LARGE=data_for_cov(C_LARGE);ISO=data_for_cov(C_ISO)
def isotropic_choice(axis,t=1.,eps=.01):
 result=ISO.copy();new=np.sqrt(CONTROL_A**2+(N-1)*eps/2*float(t));j=0 if axis==0 else 2;direction=np.eye(2)[axis];result[76+j]=new*direction;result[76+j+1]=-new*direction;return result
PLUS=isotropic_choice(0);MINUS=isotropic_choice(1)
def pca(points):
 mean=points.mean(axis=0);centered=points-mean;c=centered.T@centered/(len(points)-1);values,vectors=np.linalg.eigh(c);order=np.argsort(values)[::-1];values=values[order];vectors=vectors[:,order];gap=float(values[0]-values[1]);angle=.5*np.arctan2(2*c[0,1],c[0,0]-c[1,1]) if gap>1e-10 else None
 return dict(mean=mean,cov=c,values=values,vectors=vectors,gap=gap,angle=angle)
def line_angle(a,b):
 assert a is not None and b is not None
 return abs((b-a+np.pi/2)%np.pi-np.pi/2)
def rotation(points,t=1.):return np.rad2deg(line_angle(pca(points)['angle'],pca(perturb(points,t))['angle']))
def displacement(a,b):
 lengths=np.linalg.norm(b-a,axis=1);return dict(changed_points=int(np.count_nonzero(lengths>1e-10)),max_point_displacement=float(lengths.max()),rms_point_displacement=float(np.sqrt(np.mean(lengths**2))))
def verify():
 report={}
 for name,x,c in [('ellipse',ELLIPSE,C_ELLIPSE),('large',LARGE,C_LARGE),('small',SMALL,C_SMALL),('isotropic',ISO,C_ISO)]:
  assert x.shape==(80,2);assert np.allclose(pca(x)['cov'],c,atol=1e-12)
  report[name]={'covariance':pca(x)['cov'].tolist(),'eigenvalues':pca(x)['values'].tolist(),'gap':pca(x)['gap']}
 for name,x in [('large',LARGE),('small',SMALL)]:
  after=perturb(x);delta=pca(after)['cov']-pca(x)['cov'];assert np.allclose(delta,E,atol=1e-12);assert displacement(x,after)['changed_points']==4
  report[name].update(displacement(x,after));report[name].update(covariance_delta=delta.tolist(),covariance_delta_spectral_norm=float(np.linalg.norm(delta,2)),axis_rotation_degrees=float(rotation(x)))
 assert abs(rotation(SMALL)-31.717474411)<1e-6;assert abs(rotation(LARGE)-.572881419)<1e-6
 assert np.allclose(perturb(SMALL)-SMALL,perturb(LARGE)-LARGE)
 assert pca(ISO)['angle'] is None
 for theta in np.linspace(0,np.pi,101):
  d=np.array([np.cos(theta),np.sin(theta)]);assert abs(float(d@pca(ISO)['cov']@d)-1)<1e-12
 assert np.allclose(pca(PLUS)['cov'],np.diag([1.01,1.]));assert np.allclose(pca(MINUS)['cov'],np.diag([1.,1.01]));assert abs(np.rad2deg(line_angle(pca(PLUS)['angle'],pca(MINUS)['angle']))-90)<1e-8
 report['isotropic_choices']={'plus_covariance':pca(PLUS)['cov'].tolist(),'minus_covariance':pca(MINUS)['cov'].tolist(),'angle_difference_degrees':90,'plus_displacement':displacement(ISO,PLUS),'minus_displacement':displacement(ISO,MINUS),'all_projection_variances':1}
 return report
if __name__=='__main__':
 import json
 from pathlib import Path
 result=verify();Path(__file__).with_name('data_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
