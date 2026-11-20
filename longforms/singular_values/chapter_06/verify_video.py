from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular06_156s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==156
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))

A=np.eye(2);B=np.diag([1.,.01]);C=.01*np.eye(2)
x=np.array([1.,1.]);dy=np.array([0.,.002]);y=B@x
assert np.allclose(y,[1,.01])
assert np.allclose(np.linalg.solve(B,y),x)
assert np.allclose(np.linalg.solve(B,y+dy),[1,1.2])
assert np.allclose(np.linalg.solve(B,dy),[0,.2])
for p in np.linspace(0,1,121):
 T=np.diag([1.,100**p]);exact=T@y;noisy=T@(y+dy)
 assert np.allclose(noisy-exact,T@dy)
 assert np.isclose((noisy-exact)[1],.002*100**p)
x=np.array([1.,0.])
for matrix,before,after,factor in [(B,.002,.2,100),(C,.2,.2,1)]:
 y=matrix@x;dx=np.linalg.solve(matrix,dy)
 measured=np.linalg.norm(dy)/np.linalg.norm(y);recovered=np.linalg.norm(dx)/np.linalg.norm(x)
 assert np.isclose(measured,before) and np.isclose(recovered,after)
 assert np.isclose(recovered/measured,factor)
rng=np.random.default_rng(20261120)
for matrix,kappa in [(A,1),(B,100),(C,1)]:
 sigma=np.linalg.svd(matrix,compute_uv=False);inv=np.linalg.inv(matrix)
 assert np.isclose(sigma.max()/sigma.min(),kappa)
 assert np.isclose(np.linalg.norm(inv,ord=2),1/sigma.min())
 for j in range(128):
  x=rng.normal(size=2);db=rng.normal(size=2)*.002;b=matrix@x;dx=inv@db
  assert np.linalg.norm(dx)<=np.linalg.norm(db)/sigma.min()+1e-12
  assert np.linalg.norm(dx)/np.linalg.norm(x)<=kappa*np.linalg.norm(db)/np.linalg.norm(b)+1e-12
assert np.allclose(np.array([1,10,100,1000])*.2,[.2,2,20,200])
for t in [1,.01,.0001,1e-8,0]:
 if t==0:assert np.linalg.det(np.diag([1,t]))==0
 else:assert np.isclose(np.linalg.cond(np.diag([1,t])),1/t)
points=[4.5,9.5,17.5,21.5,23.5,28.5,34.5,39.5,42.5,47.5,52.5,57.5,63.5,67.5,74.5,80.5,88.5,93.5,97.5,104.5,112.5,117.5,121.5,124.5,130.5,139.5,143.5,151.5,155.5]
selected={int(t*30):t for t in points};shots=[];last=-1;caption_hashes=[]
with av.open(str(video)) as container:
 stream=container.streams.video[0]
 assert (stream.width,stream.height)==(1920,1080)
 assert stream.average_rate==30
 assert len(container.streams.audio)==0
 for n,frame in enumerate(container.decode(video=0)):
  timestamp=float(frame.pts*frame.time_base)
  assert timestamp>last;last=timestamp
  if n in selected:
   im=frame.to_image();caption_hashes.append(hashlib.sha256(im.crop((0,930,1920,1080)).tobytes()).hexdigest());im.thumbnail((640,360));shots.append((selected[n],im.copy()))
 assert n+1==4680
 assert abs(float(stream.duration*stream.time_base)-156)<1e-6
assert len(caption_hashes)==29 and len(set(caption_hashes))==29, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,10*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
for part in range(3):
 top=part*4*392;bottom=min((part+1)*4*392,sheet.height)
 if bottom>top:sheet.crop((0,top,1920,bottom)).save(qa/f'contact_{part+1}.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=156,frames=4680,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),absolute_error_gain=100,relative_gains={"B":100,"C":1},condition_bound_samples=384,singular_limit_check=True,keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
