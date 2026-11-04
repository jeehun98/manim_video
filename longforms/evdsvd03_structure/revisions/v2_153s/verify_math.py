"""Audit all internal geometry; numeric data stay offscreen."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
def R(d):
    t=np.deg2rad(d);return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
P=np.array([[1.,1.],[0.,-1.]]);AE=np.array([[2.,1.],[0.,1.]]);D=np.diag([2.,1.])
V=R(25);U=R(30);sigma=np.diag([2.,1.]);A=U@sigma@V.T
assert np.allclose(P@D@np.linalg.inv(P),AE)
assert np.allclose(AE@P,P@D)
assert not np.isclose(P[:,0]@P[:,1],0)
assert np.allclose(V.T@V,np.eye(2)) and np.allclose(U.T@U,np.eye(2))
assert np.allclose(A@V,U@sigma)
assert np.isclose(np.linalg.det(A),2)
angles=np.linspace(0,2*np.pi,1000)
circle=np.array([np.cos(angles),np.sin(angles)])
ellipse=A@circle;local=U.T@ellipse
assert np.allclose(local[0]**2/4+local[1]**2,1)
for t in [0,.25,.5,.75,1]:
    assert np.allclose(((1-t)*np.eye(2)+t*A)@circle,(1-t)*circle+t*ellipse)
c=np.array([1.15,-.75]);x=V@c
assert np.allclose(V.T@x,c) and c[1]<0
assert np.allclose(c[0]*V[:,0]+c[1]*V[:,1],x)
assert np.allclose(U@(sigma@c),A@x)
assert np.allclose((U@V.T)@(V@sigma@c),A@x)
y=AE@np.array([2.,-1.]);feet=sum(P[:,i]*(y@P[:,i])/(P[:,i]@P[:,i]) for i in range(2))
assert not np.allclose(feet,y)
cues=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'));manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
assert cues[0]['start']==0 and cues[-1]['end']==153
assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
assert len(manifest)==18 and sum(m['duration_seconds'] for m in manifest)==153
report=dict(A=A.tolist(),V=V.tolist(),U=U.tolist(),singular_values=[2,1],input_angles=[25,115],output_angles=[30,120],signed_coordinates=c.tolist(),input=x.tolist(),output=(A@x).tolist(),duration=153,sentences=len(cues),scenes=18,status='passed')
(ROOT/'math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Verified rotated bases, 1000 ellipse points, interpolation, signed projections, and all clocks.')
