from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular04_137s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==137
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))

for t in [1,.6,.1,.01,1e-12,0]:
 A=np.diag([2.,t]);singular=np.linalg.svd(A,compute_uv=False)
 assert np.allclose(singular,[2,t])
 assert sum(singular>0)==(2 if t>0 else 1)
A0=np.diag([2.,0.])
for y in np.linspace(-2,2,17):
 assert np.array_equal(A0@np.array([0,y]),[0,0])
 assert np.array_equal(A0@np.array([1,y]),[2,0])
for diag,rank in [([2,1,.65],3),([2,1,0],2),([2,0,0],1)]:
 assert np.linalg.matrix_rank(np.diag(diag))==rank
original=np.diag([2.,.1]);approx=np.diag([2.,0.]);error=original-approx
assert np.linalg.matrix_rank(original)==2 and np.linalg.matrix_rank(approx)==1
assert np.isclose(np.linalg.norm(error,ord=2),.1)
for a in np.linspace(0,2*np.pi,721):
 v=np.array([np.cos(a),np.sin(a)])
 assert np.linalg.norm(error@v)<=.1+1e-12
spectrum=np.array([2,1.55,1.2,.65,.08,.04,.02]);truncated=spectrum.copy();truncated[4:]=0
assert sum(spectrum>0)==7 and sum(truncated>0)==4
assert np.isclose(np.linalg.norm(np.diag(spectrum-truncated),ord=2),.08)
points=[3.5,8.5,11.5,16.5,20.5,26.5,31.5,35.5,39.5,44.5,50.5,54.5,60.5,65.5,70.5,77.5,81.5,90.5,94.5,100.5,106.5,115.5,120.5,131.5,136.7]
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
 assert n+1==4110
 assert abs(float(stream.duration*stream.time_base)-137)<1e-6
assert len(caption_hashes)==25 and len(set(caption_hashes))==25, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,9*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
for part in range(3):
 top=part*4*392;bottom=min((part+1)*4*392,sheet.height)
 if bottom>top:sheet.crop((0,top,1920,bottom)).save(qa/f'contact_{part+1}.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=137,frames=4110,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),exact_zero_rank_checks=True,low_rank_unit_error=.1,spectrum_truncation_error=.08,keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
