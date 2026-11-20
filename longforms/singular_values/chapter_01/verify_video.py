from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular01_100s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==100
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
B=np.array([[1.,2.],[0.,1.]]);u=np.array([1.,2.])/np.sqrt(5);v=np.array([-2.,1.])/np.sqrt(5)
assert np.allclose(B@u,np.array([5,2])/np.sqrt(5))
assert np.allclose(B@v,np.array([0,1])/np.sqrt(5))
assert np.allclose(np.linalg.eigvals(B),[1,1])
assert np.linalg.matrix_rank(B-np.eye(2))==1
for angle,wanted in [(60,2.394170170971),(150,.517638090205)]:
 t=np.radians(angle);assert abs(np.linalg.norm(B@np.array([np.cos(t),np.sin(t)]))-wanted)<1e-9
for c in [.5,1,2,-2]:assert np.allclose(np.linalg.norm(B@(c*u))/np.linalg.norm(c*u),np.linalg.norm(B@u))
points=[3.5,8,15,19,23,29,35,41,48,53,58,64,69,75,81,86,94,99.8]
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
 assert n+1==3000
 assert abs(float(stream.duration*stream.time_base)-100)<1e-6
assert len(caption_hashes)==18 and len(set(caption_hashes))==18, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,6*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=100,frames=3000,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),length_ratios=[float(np.linalg.norm(B@u)),float(np.linalg.norm(B@v))],keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
