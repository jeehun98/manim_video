from pathlib import Path
import av,json,numpy as np,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
video=WORKSPACE/'exports/singular05_151s_1080p30.mp4'
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
assert timing[0]['start']==0 and timing[-1]['end']==151
assert all(a['end']==b['start'] for a,b in zip(timing,timing[1:]))

matrices=[np.eye(2),np.array([[1.,2.],[0.,1.]]),np.diag([2.,3.]),np.diag([2.,.75]),np.diag([-2.,1.]),np.diag([100.,.01]),np.diag([2.,0.]),np.diag([2.,1.,.75]),np.array([[1.,2.,0.],[0.,-1.,1.],[1.,0.,2.]])]
for A in matrices:
 sigma=np.linalg.svd(A,compute_uv=False);det=np.linalg.det(A);M=A.T@A
 assert np.isclose(abs(det),np.prod(sigma),atol=1e-10)
 assert np.isclose(np.linalg.det(M),det*det,atol=1e-10)
 assert np.allclose(sigma*sigma,np.linalg.eigvalsh(M)[::-1],atol=1e-10)
for p in np.linspace(0,1,301):
 s=100**p;M=np.diag([s,1/s])
 assert np.isclose(np.linalg.det(M),1)
 corners=np.array([[-s/2,-.5/s],[s/2,-.5/s],[s/2,.5/s],[-s/2,.5/s]])*.1
 area=.5*abs(np.dot(corners[:,0],np.roll(corners[:,1],1))-np.dot(corners[:,1],np.roll(corners[:,0],1)))
 assert np.isclose(area,.01)
assert 0<1080/8*.1/100<1
assert np.isclose(np.prod(np.linalg.svd(np.diag([2,1,.75]),compute_uv=False)),1.5)
for d in [[1,1],[2,.5],[4,.25]]:assert np.isclose(np.pi*np.prod(d)*.38**2,np.pi*.38**2)
P=np.array([[.5,.35],[-.45,.2],[-.35,-.4]])
def signed_area(points):return np.cross(points[1]-points[0],points[2]-points[0])/2
left=(np.diag([2,1])@P.T).T;right=(np.diag([-2,1])@P.T).T
assert np.isclose(signed_area(left),-signed_area(right))
assert np.allclose(np.linalg.svd(np.diag([2,1]),compute_uv=False),np.linalg.svd(np.diag([-2,1]),compute_uv=False))
points=[3.5,8.5,12.5,19.5,24.5,27.5,30.5,37.5,42.5,48.5,51.5,58.5,64.5,65.5,70.5,75.5,78.5,84.5,87.5,93.5,100.5,105.5,111.5,115.5,124.5,132.5,139.5,144.5,150.5]
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
 assert n+1==4530
 assert abs(float(stream.duration*stream.time_base)-151)<1e-6
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
report=dict(source_hashes=source_hashes,video=str(video),seconds=151,frames=4530,fps=30,resolution=[1920,1080],audio=False,full_decode='passed',monotonic_pts=True,contiguous_captions=True,distinct_sentence_caption_frames=len(set(caption_hashes)),determinant_product_matrices=9,area_preservation_samples=301,orientation_sign_check=True,extreme_thickness_pixels=.135,keyframes=points)
(qa/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
