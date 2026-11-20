from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular02_121s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==121
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
B=np.array([[1.,2.],[0.,1.]]);u=np.array([1.,2.])/np.sqrt(5);v=np.array([-2.,1.])/np.sqrt(5)
assert np.allclose(B@u,np.array([5,2])/np.sqrt(5))
assert np.allclose(B@v,np.array([0,1])/np.sqrt(5))
assert np.allclose(np.linalg.eigvals(B),[1,1])
assert np.linalg.matrix_rank(B-np.eye(2))==1
for angle,wanted in [(60,2.394170170971),(150,.517638090205)]:
 t=np.radians(angle);assert abs(np.linalg.norm(B@np.array([np.cos(t),np.sin(t)]))-wanted)<1e-9
for c in [.5,1,2,-2]:assert np.allclose(np.linalg.norm(B@(c*u))/np.linalg.norm(c*u),np.linalg.norm(B@u))
v1=np.array([np.cos(np.radians(67.5)),np.sin(np.radians(67.5))]);v2=np.array([-v1[1],v1[0]])
w1=B@v1;w2=B@v2
assert abs(v1@v2)<1e-12 and abs(w1@w2)<1e-12
assert np.isclose(np.linalg.norm(w1),1+np.sqrt(2))
assert np.isclose(np.linalg.norm(w2),np.sqrt(2)-1)
assert np.allclose(np.degrees(np.arctan2([w1[1],w2[1]],[w1[0],w2[0]])),[22.5,112.5])
assert np.allclose(np.linalg.svd(np.diag([2,1,.5]),compute_uv=False),[2,1,.5])
angles=np.linspace(0,2*np.pi,7201)
inputs=np.stack([np.cos(angles),np.sin(angles)])
lengths=np.linalg.norm(B@inputs,axis=0)
assert abs(lengths.max()-(1+np.sqrt(2)))<1e-6
assert abs(lengths.min()-(np.sqrt(2)-1))<1e-6
for phi in np.linspace(0,np.pi,17):
 for theta in np.linspace(0,2*np.pi,25):
  point=np.array([np.sin(phi)*np.cos(theta),np.sin(phi)*np.sin(theta),np.cos(phi)])
  transformed=np.diag([2,1,.5])@point
  assert np.isclose(np.sum((transformed/np.array([2,1,.5]))**2),1)

points=[5.5,7.5,11.5,17.5,22.5,26.5,34.5,43.5,47.5,50.5,53.5,59.5,64.5,70.5,77.5,81.5,86.5,92.5,96.5,105.5,109.5,115.5,120.7]
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
 assert n+1==3630
 assert abs(float(stream.duration*stream.time_base)-121)<1e-6
assert len(caption_hashes)==23 and len(set(caption_hashes))==23, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,8*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=121,frames=3630,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),length_ratios=[float(np.linalg.norm(B@u)),float(np.linalg.norm(B@v))],keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
