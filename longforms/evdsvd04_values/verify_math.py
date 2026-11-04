"""Audit the one shear matrix, singular directions, and confirmed narration clock."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
A=np.array([[1.,2.],[0.,1.]])
s=np.array([1+np.sqrt(2),np.sqrt(2)-1])
v=np.column_stack(([np.cos(np.deg2rad(67.5)),np.sin(np.deg2rad(67.5))],[np.cos(np.deg2rad(-22.5)),np.sin(np.deg2rad(-22.5))]))
u=np.column_stack(([np.cos(np.deg2rad(22.5)),np.sin(np.deg2rad(22.5))],[np.cos(np.deg2rad(-67.5)),np.sin(np.deg2rad(-67.5))]))
assert np.allclose(np.linalg.eigvals(A),[1,1])
assert np.linalg.matrix_rank(A-np.eye(2))==1
assert np.allclose(A@np.array([1,0]),[1,0]) and np.allclose(A@np.array([0,1]),[2,1])
assert np.allclose(np.linalg.svd(A)[1],s)
assert np.allclose(A@v,u@np.diag(s))
assert np.allclose(v.T@v,np.eye(2)) and np.allclose(u.T@u,np.eye(2))
assert np.allclose(u@np.diag(s)@v.T,A)
t=np.linspace(0,2*np.pi,1000);circle=np.array([np.cos(t),np.sin(t)]);ellipse=A@circle
local=u.T@ellipse;assert np.allclose((local[0]/s[0])**2+(local[1]/s[1])**2,1)
for alpha in [0,.25,.5,.75,1]:
    assert np.allclose(np.array([[1,2*alpha],[0,1]])@circle,(1-alpha)*circle+alpha*ellipse)
project=json.loads((ROOT/'project.json').read_text(encoding='utf-8'));cues=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert project['ending_confirmed'] and project['duration']==103
assert cues[-2]['end']==101 and cues[-1]['end']==103
assert all(a['end']==b['start'] for a,b in zip(cues,cues[1:]))
(ROOT/'math_verification.json').write_text(json.dumps(dict(matrix=A.tolist(),eigenvalues=[1,1],eigenspace_dimension=1,singular_values=s.tolist(),V=v.tolist(),U=u.tolist(),duration=103,sentences=len(cues),status='passed'),indent=2),encoding='utf-8')
print('Verified same shear, one eigenline, both exact singular directions, ellipse, and confirmed 103s clock.')
