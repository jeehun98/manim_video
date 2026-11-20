from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular03_180s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==180
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))
B=np.array([[1.,2.],[0.,1.]])
M=B.T@B
assert np.array_equal(M,np.array([[1.,2.],[2.,5.]]))
assert np.array_equal(M,M.T)
lambdas=np.array([3+2*np.sqrt(2),3-2*np.sqrt(2)])
v1=np.array([np.cos(np.radians(67.5)),np.sin(np.radians(67.5))]);v2=np.array([-v1[1],v1[0]])
assert np.allclose(M@v1,lambdas[0]*v1) and np.allclose(M@v2,lambdas[1]*v2)
assert np.isclose(v1@v2,0)
for angle in np.linspace(0,2*np.pi,721):
 c1,c2=np.cos(angle),np.sin(angle);inputv=c1*v1+c2*v2
 output=B@inputv;weighted=lambdas[0]*c1*c1+lambdas[1]*c2*c2
 assert np.isclose(output@output,weighted)
 assert lambdas[1]-1e-10<=weighted<=lambdas[0]+1e-10
 assert np.isclose(np.linalg.norm(inputv),1)
assert np.isclose((B@v1)@(B@v2),0)
assert np.allclose(np.sqrt(lambdas),np.array([1+np.sqrt(2),np.sqrt(2)-1]))
assert np.isclose(np.linalg.norm(B@(.8*v1+.6*v2))**2,.64*lambdas[0]+.36*lambdas[1])
points=[4.5,7.5,13.5,17.5,23.5,28.5,33.5,37.5,42.5,47.5,56.5,59.5,65.5,70.5,77.5,81.5,87.5,91.5,96.5,101.5,106.5,111.5,117.5,122.5,131.5,135.5,140.5,144.5,152.5,157.5,166.7,174.5,179.7]
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
 assert n+1==5400
 assert abs(float(stream.duration*stream.time_base)-180)<1e-6
assert len(caption_hashes)==33 and len(set(caption_hashes))==33, 'A sentence caption failed to update'
sheet=Image.new('RGB',(1920,11*392),'#141a24');d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(shots):
 x=(i%3)*640;y=(i//3)*392;sheet.paste(im,(x,y+25));d.text((x+12,y+5),f'{t:.1f}s',fill='white')
sheet.save(qa/'contact.jpg')
for part in range(3):
 top=part*4*392;bottom=min((part+1)*4*392,sheet.height)
 if bottom>top:sheet.crop((0,top,1920,bottom)).save(qa/f'contact_{part+1}.jpg')
import hashlib
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.suffix in ['.py','.json','.md'] and 'qa' not in p.parts}
report=dict(source_hashes=source_hashes,video=str(video),seconds=180,frames=5400,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),eigenvalues=lambdas.tolist(),singular_values=np.sqrt(lambdas).tolist(),weighted_average_samples=721,keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
