"""Verify the storyboard's exact decompositions, coordinates, and geometry."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
AE=np.array([[2.,1.],[0.,1.]])
P=np.array([[1.,1.],[0.,-1.]])
D=np.diag([2.,1.]);xe=np.array([2.,-1.])
AS=np.array([[0.,-1.],[3.,0.]])
U=np.array([[0.,-1.],[1.,0.]]);V=np.eye(2);sigma=np.diag([3.,1.])
assert np.allclose(P@D@np.linalg.inv(P),AE)
assert np.allclose(AE@P,P@D)
assert np.allclose(np.linalg.solve(P,xe),[1,1])
assert np.allclose(P.T@xe,[2,3])
assert not np.allclose(P.T,np.linalg.inv(P))
assert np.allclose(AE@xe,[3,-1])
assert np.allclose(U@sigma@V.T,AS)
assert np.allclose(U.T@U,np.eye(2)) and np.allclose(V.T@V,np.eye(2))
for i in range(2):assert np.allclose(AS@V[:,i],sigma[i,i]*U[:,i])
angles=np.linspace(0,2*np.pi,1000)
points=np.array([np.cos(angles),np.sin(angles)])
image=AS@points
assert np.allclose(image[0]**2+image[1]**2/9,1)
assert np.allclose(np.linalg.norm(image,axis=0)**2,np.sin(angles)**2+9*np.cos(angles)**2)
xs=np.array([2.,1.]);assert np.allclose(sigma@V.T@xs,[6,1]);assert np.allclose(AS@xs,[-1,6])
cues=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
assert cues[0]['start']==0 and cues[-1]['end']==149
assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
assert len(manifest)==24 and sum(m['duration_seconds'] for m in manifest)==149
report=dict(evd=dict(A=AE.tolist(),P=P.tolist(),D=D.tolist(),basis_coordinates=[1,1],direct_inner_products=[2,3],output=[3,-1]),svd=dict(A=AS.tolist(),U=U.tolist(),Sigma=sigma.tolist(),V=V.tolist(),input=[2,1],scaled_coordinates=[6,1],output=[-1,6],ellipse_semiaxes=dict(horizontal=1,vertical=3)),duration=149,sentences=len(cues),scenes=24,status='passed')
(ROOT/'math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Verified EVD, dual coordinates, SVD, 1000 circle points, and all narration boundaries.')
