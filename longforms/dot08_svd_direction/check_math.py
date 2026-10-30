"""Validate displayed matrices, coefficients, geometry and generalization."""
import json
import numpy as np
from visuals import A,U,SIGMA,V,X,Y,P
assert np.allclose(A,U@SIGMA@V.T)
assert np.allclose(U.T@U,np.eye(2)) and np.allclose(V.T@V,np.eye(2))
assert np.all(np.diag(SIGMA)>=0) and SIGMA[0,0]>=SIGMA[1,1]
c=V.T@X;scaled=SIGMA@c;pieces=[scaled[i]*U[:,i] for i in range(2)]
assert np.allclose(c,[2,1]) and np.allclose(scaled,[6,1]) and np.allclose(Y,[-1,6])
assert np.allclose(sum(pieces),Y) and np.allclose(A@V,U@SIGMA)
errors=[]
for angle in np.linspace(0,2*np.pi,361):
    x=np.array([np.cos(angle),np.sin(angle)]);direct=A@x;split=sum(SIGMA[i,i]*U[:,i]*np.dot(V[:,i],x) for i in range(2));errors.append(float(np.max(np.abs(direct-split))))
angle=np.deg2rad(30);vp=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]);ap=U@SIGMA@vp.T
assert not np.allclose(vp,np.eye(2));assert np.allclose(ap@X,U@SIGMA@(vp.T@X))
assert np.allclose(np.linalg.svd(A,compute_uv=False),[3,1])
# Rectangular and rank-deficient maps also obey the spoken general formula.
general=[]
for matrix in [np.array([[1.,2.],[0.,3.],[2.,-1.]]),np.array([[1.,2.,0.],[-2.,-4.,0.]])]:
    u,s,vt=np.linalg.svd(matrix,full_matrices=False);x=np.arange(1,matrix.shape[1]+1,dtype=float);z=sum(s[i]*u[:,i]*np.dot(vt[i],x) for i in range(len(s)));err=float(np.max(np.abs(matrix@x-z)));assert err<1e-12;general.append(dict(shape=list(matrix.shape),error=err))
report=dict(A=A.tolist(),U=U.tolist(),Sigma=SIGMA.tolist(),V=V.tolist(),input=X.tolist(),coefficients=c.tolist(),scaled=scaled.tolist(),output_components=[p.tolist() for p in pieces],output=Y.tolist(),sampled_directions=361,max_reconstruction_error=max(errors),rotated_example_A=ap.tolist(),rotated_example_coefficients=(vp.T@X).tolist(),rotated_example_output=(ap@X).tolist(),general_cases=general)
(P/'qa_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
