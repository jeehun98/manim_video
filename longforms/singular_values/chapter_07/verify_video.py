from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular07_90s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==90
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))

A=np.array([[1.,2.],[0.,1.]])
u,s,vt=np.linalg.svd(A);eig=np.linalg.eigvalsh(A.T@A)[::-1]
assert np.allclose(s,[1+np.sqrt(2),np.sqrt(2)-1])
assert np.allclose(eig,[3+2*np.sqrt(2),3-2*np.sqrt(2)])
assert np.allclose(np.sqrt(eig),s)
assert np.allclose(np.linalg.eigvals(A),[1,1])
assert np.isclose(np.prod(s),abs(np.linalg.det(A)))
assert np.isclose(s[0]/s[1],3+2*np.sqrt(2))
assert np.allclose(A@vt.T,u@np.diag(s))
for theta in np.linspace(0,2*np.pi,181):
 v=np.array([np.cos(theta),np.sin(theta)])
 assert np.isclose(np.linalg.norm(A@v)**2,v@(A.T@A)@v)
for t in [.7,.01,1e-6,0]:
 assert np.count_nonzero(np.linalg.svd(np.diag([2,t]),compute_uv=False)>0)==(2 if t>0 else 1)
for p in np.linspace(0,1,121):
 T=np.eye(2)+p*(np.linalg.inv(A)-np.eye(2));y=np.array([1.,.2]);dy=np.array([0,.04])
 assert np.allclose(T@(y+dy)-T@y,T@dy)
 assert np.linalg.det(np.array([[1,2*p],[0,1]]))==1
points=[4.5,11.5,18.5,24.5,32.5,38.5,45.5,50.5,59.5,65.5,71.5,81.5,88.5,89.7]
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
 assert n+1==2700
 assert abs(float(stream.duration*stream.time_base)-90)<1e-6
assert len(caption_hashes)==14 and len(set(caption_hashes))>=12, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,5*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
for part in range(3):
 top=part*4*392;bottom=min((part+1)*4*392,sheet.height)
 if bottom>top:sheet.crop((0,top,1920,bottom)).save(qa/f'contact_{part+1}.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=90,frames=2700,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_selected_caption_frames=len(set(caption_hashes)),singular_values=s.tolist() if hasattr(s,'tolist') else [2.41421356,.41421356],matrix_checks='passed',keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
