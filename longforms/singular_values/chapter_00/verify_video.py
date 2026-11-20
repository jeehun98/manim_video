from pathlib import Path
import av,json,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular00_63s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==63
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
B=np.array([[1.,2.],[0.,1.]]);u=np.array([1.,2.])/np.sqrt(5);v=np.array([-2.,1.])/np.sqrt(5)
assert np.allclose(B@u,np.array([5,2])/np.sqrt(5))
assert np.allclose(B@v,np.array([0,1])/np.sqrt(5))
assert np.allclose(np.linalg.eigvals(B),[1,1])
assert np.linalg.matrix_rank(B-np.eye(2))==1
points=[5.5,9,11.5,16,20,27,32,40,48,52,61.5]
selected={int(t*30):t for t in points};shots=[];last=-1
with av.open(str(video)) as container:
 stream=container.streams.video[0]
 assert (stream.width,stream.height)==(1920,1080)
 assert stream.average_rate==30
 assert len(container.streams.audio)==0
 for n,frame in enumerate(container.decode(video=0)):
  timestamp=float(frame.pts*frame.time_base)
  assert timestamp>last;last=timestamp
  if n in selected:
   im=frame.to_image();im.thumbnail((640,360));shots.append((selected[n],im.copy()))
 assert n+1==1890
 assert abs(float(stream.duration*stream.time_base)-63)<1e-6
sheet=Image.new('RGB',(1920,4*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
report=dict(video=str(video),seconds=63,frames=1890,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,length_ratios=[float(np.linalg.norm(B@u)),float(np.linalg.norm(B@v))],keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
