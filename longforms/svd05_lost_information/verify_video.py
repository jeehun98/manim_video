"""Decode every delivered frame; independently check numerical invariants and timings."""
from pathlib import Path
import json
import av,numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;P=R.parents[1]/'exports/svd05_lost_information_251s_1080p30.mp4'
d=np.load(R/'assets/svd_data.npz');photo=d['photo'];u,s,v=np.linalg.svd(photo,full_matrices=False)
for k in [1,2,5,10]:assert np.isclose(np.linalg.norm(photo-(u[:,:k]*s[:k])@v[:k])**2,np.sum(s[k:]**2))
assert np.linalg.matrix_rank(d['matrix_rank3'])==3
assert np.isclose(np.linalg.norm(d['matrix']-d['matrix_rank3'])**2,1.29)
assert np.linalg.matrix_rank(d['marker'])==2 and np.linalg.matrix_rank(d['marker_rank1'])==1
assert np.allclose(d['marker_rank1'],.5) and np.isclose(np.linalg.norm(d['marker']-d['marker_rank1'])**2,.09)
A=np.diag([1.,0]);pinv=np.linalg.pinv(A)
for t in [-20,-1,0,3,40]:assert np.allclose(A@np.array([1,t]),[1,0])
assert np.allclose(pinv@np.array([1,.3]),[1,0])
assert np.isclose(np.linalg.norm(A@pinv@np.array([1,.3])-[1,.3]),.3)
B=np.diag([8.,4,2]);B2=np.diag([8.,4,0]);C2=np.diag([8.,0,2])
assert np.linalg.matrix_rank(B2)==np.linalg.matrix_rank(C2)==2
assert np.isclose(np.linalg.norm(B-B2)**2,4) and np.isclose(np.linalg.norm(B-C2)**2,16)
sent=json.loads((R/'timing.json').read_text(encoding='utf-8'))['sentences'];manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
assert len(sent)==52 and len(manifest)==28 and sum(m['duration_seconds'] for m in manifest)==251
assert sent[0]['start']==0 and sent[-1]['end']==251
assert all(a['end']==b['start'] for a,b in zip(sent,sent[1:]))
targets=[4,20,32,47,56,61,66,71,73,75,77,82,90,106,114,120,128,138,150,157,167,170,171,173,181,189,198,213,221,228,235,250]
shots=[];count=0;previous=None;idx=0
with av.open(str(P)) as c:
 st=c.streams.video[0];assert (st.width,st.height)==(1920,1080) and st.average_rate==30 and st.frames==7530
 assert float(st.duration*st.time_base)==251 and not c.streams.audio
 for f in c.decode(video=0):
  if previous is not None:assert f.pts>previous
  previous=f.pts;count+=1
  if idx<len(targets) and float(f.time)>=targets[idx]:
   t=targets[idx];im=f.to_image();(R/'qa').mkdir(exist_ok=True);im.save(R/f'qa/final_{t}.jpg')
   im=im.resize((640,360));tile=Image.new('RGB',(640,386),'#142033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((12,7),f'{t}s / final 1080p30',fill='white');shots.append(tile);idx+=1
assert count==7530 and idx==len(targets)
for start in range(0,len(shots),8):
 subset=shots[start:start+8];sheet=Image.new('RGB',(1280,386*((len(subset)+1)//2)),'#142033')
 for i,im in enumerate(subset):sheet.paste(im,((i%2)*640,(i//2)*386))
 sheet.save(R/f'qa/final_part_{start//8+1}.jpg')
report={'video':str(P),'duration_seconds':251,'resolution':[1920,1080],'fps':30,'decoded_frames':count,'audio':'none; act 5 audio not supplied','sentence_endpoints':52,'independent_scenes':28,'sampled_frames':len(targets),'checks':['all frame timestamps strictly increase','exact frame count and duration','continuous approved sentence intervals','null space versus affine solution set','minimum norm least squares outside range','actual SVD image error equals discarded squared singular values','same rank 2 error comparison: 4 vs 16','orthogonal local marker is absent from actual rank 1 approximation']}
(R/'qa/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
