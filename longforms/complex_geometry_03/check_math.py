"""Numerical regression checks complementing the exact identities in the specs."""
from pathlib import Path
import sys,json,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from direction import torus_q,lifted_point,sheet_point,clip_segment
t=np.linspace(0,4*np.pi,1001);z=np.exp(1j*t);w=np.exp(.5j*t)
assert np.max(abs(w*w-z))<1e-12
assert abs(w[500]+1)<1e-12 and abs(w[-1]-1)<1e-12
assert np.linalg.norm(lifted_point(2*np.pi)-sheet_point(1,1))<1e-12
assert np.linalg.norm(lifted_point(4*np.pi)-sheet_point(1,0))<1e-12
rng=np.random.default_rng(19);zs=np.sqrt(rng.random(5000))*.999*np.exp(2j*np.pi*rng.random(5000))
F=lambda z:1j*(1+z)/(1-z)
inv=lambda q:(q-1j)/(q+1j)
err=float(np.max(abs(inv(F(zs))-zs)))
assert err<1e-12 and np.min(F(zs).imag)>0
assert np.max(abs(F(zs).imag-(1-abs(zs)**2)/abs(1-zs)**2))<1e-9
for u,v in rng.random((100,2))*2*np.pi:
 assert np.linalg.norm(torus_q(u+2*np.pi,v)-torus_q(u,v))<1e-12
 assert np.linalg.norm(torus_q(u,v+2*np.pi)-torus_q(u,v))<1e-12
for t in np.linspace(0,1,21):
 assert np.min(abs(1j*(1+t)/(1-t*zs)**2))>0
rect=(-6.8,6.8,-1.6,2.15)
for a,b in rng.uniform(-100,100,(10000,2,3)):
 a[2]=b[2]=0;s=clip_segment(a,b,rect)
 if s is not None:
  for q in s:assert rect[0]-1e-9<=q[0]<=rect[1]+1e-9 and rect[2]-1e-9<=q[1]<=rect[3]+1e-9
report=dict(square_root='w(theta)^2=z(theta); 2pi changes sign; 4pi returns',sheets='negative-real-axis cut crossed at pi and 3pi; endpoints at 2pi/4pi match opposite/original sheet',local_coordinate='w globally parametrizes S={(w²,w)}; F(w)=w entire; 3D saddle is a visualization of Re(w²)',torus='doubly periodic torus embedding checked; complex torus is C/(Z+iZ), not its induced Euclidean metric',cayley_inverse_max_error=err,cayley='Im F(z)=(1-|z|²)/|1-z|²>0; inverse (q-i)/(q+i); Fprime(0)=2i',homotopy='Ft derivative i(1+t)/(1-tz)^2 nonzero on disk; pole excluded and actual transformed segments clipped to viewport',uniformization='connected Riemann surface: universal holomorphic cover is biholomorphic to sphere, C or D; punctured disk has disk as universal cover',sources=[dict(url='https://people.math.osu.edu/costin.9/7651-2021/notes2.pdf',sections='26.142–143, 43.18–19; universal covers and three biholomorphic types'),dict(url='https://people.math.harvard.edu/~pspark/uniformization.pdf',subject='Complex tori and holomorphic covering construction')],atlas='Existing sources.json absent; no unrelated knowledge files modified',status='passed')
(Path(__file__).parent/'math_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Math checks passed; Cayley inverse error',err)
