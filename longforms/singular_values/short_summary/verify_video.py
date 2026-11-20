from pathlib import Path
import av,json,numpy as np,hashlib,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;WORKSPACE=ROOT.parents[2];qa=ROOT/'qa';qa.mkdir(exist_ok=True)
video=WORKSPACE/'exports/singular_summary_150s_1080p30.mp4'
rows=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'));assert len(rows)==27
assert rows[0]['start']==0 and rows[-1]['end']==150
assert all(a['end']==b['start'] for a,b in zip(rows,rows[1:]))
A=np.array([[1.,2.],[0.,1.]]);M=A.T@A;u,s,vt=np.linalg.svd(A)
assert np.allclose(np.linalg.eigvals(A),[1,1]);assert np.linalg.matrix_rank(A-np.eye(2))==1
assert np.allclose(M,[[1,2],[2,5]]);assert np.allclose(s,[1+np.sqrt(2),np.sqrt(2)-1])
V=np.column_stack([np.array([np.cos(t),np.sin(t)]) for t in np.deg2rad([67.5,157.5])]);assert np.allclose(V.T@V,np.eye(2));assert np.allclose(M@V,V@np.diag(s*s))
assert np.allclose(A@V/s,np.column_stack([np.array([np.cos(t),np.sin(t)]) for t in np.deg2rad([22.5,112.5])]))
for theta in np.linspace(0,2*np.pi,181):
 v=np.array([np.cos(theta),np.sin(theta)]);assert np.isclose(np.linalg.norm(A@v)**2,v@M@v)
for t in [1,.1,.0001,1e-12,0]:assert np.count_nonzero(np.linalg.svd(np.diag([2,t]),compute_uv=False)>0)==(2 if t>0 else 1)
D=np.diag([1.,.01]);x=np.array([1.,0]);dy=np.array([0,.002]);y=D@x;dx=np.linalg.solve(D,dy)
assert np.allclose(dx,[0,.2]);assert np.isclose(np.linalg.norm(dy)/np.linalg.norm(y),.002);assert np.isclose(np.linalg.norm(dx)/np.linalg.norm(x),.2)
for p in np.linspace(0,1,121):
 T=np.diag([1,100**p]);assert np.allclose(T@(y+dy)-T@y,T@dy)
assert np.isclose(.002*2.4*200,.96)
for matrix in [A,np.diag([2,.75]),D]:assert np.isclose(np.prod(np.linalg.svd(matrix,compute_uv=False)),abs(np.linalg.det(matrix)))
rng=np.random.default_rng(20261120)
for t in [1,.1,.01,.001]:
 Q=np.diag([1,t]);k=1/t;assert np.isclose(np.linalg.cond(Q),k)
 for _ in range(64):
  x=rng.normal(size=2);db=rng.normal(size=2)*.001;b=Q@x;dx=np.linalg.solve(Q,db);assert np.linalg.norm(dx)/np.linalg.norm(x)<=k*np.linalg.norm(db)/np.linalg.norm(b)+1e-10
points=sorted(set([r['end']-.4 for r in rows]+[88.5,90.5,119,122.5,129.5,149.6]));selected={round(t*30):t for t in points};sentence_frames={round((r['end']-.4)*30) for r in rows};shots=[];hashes=[];last=-1
with av.open(str(video)) as c:
 stream=c.streams.video[0];assert (stream.width,stream.height)==(1080,1920);assert stream.average_rate==30;assert len(c.streams.audio)==0
 for n,frame in enumerate(c.decode(video=0)):
  timestamp=float(frame.pts*frame.time_base);assert timestamp>last;last=timestamp
  if n in selected:
   im=frame.to_image()
   if n in sentence_frames:hashes.append(hashlib.sha256(im.crop((80,1510,950,1840)).tobytes()).hexdigest())
   im.thumbnail((360,640));shots.append((selected[n],im.copy()))
 assert n+1==4500;assert abs(float(stream.duration*stream.time_base)-150)<1e-6
assert len(hashes)==27 and len(set(hashes))==27,'Caption did not update'
for part in range(math.ceil(len(shots)/8)):
 group=shots[part*8:(part+1)*8];sheet=Image.new('RGB',(1440,665*math.ceil(len(group)/4)),'#141a24');d=ImageDraw.Draw(sheet)
 for i,(t,im) in enumerate(group):
  x=(i%4)*360;y=(i//4)*665;sheet.paste(im,(x,y+25));d.text((x+10,y+5),f'{t:.1f}s',fill='white')
 sheet.save(qa/f'contact_{part+1}.jpg')
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=150,frames=4500,fps=30,resolution=[1080,1920],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(hashes)),math_checks='passed',relative_error_gain=100,bound_samples=256,keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
