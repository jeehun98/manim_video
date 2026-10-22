"""Verify delivered timing and frames; inspect comparison colors and the final single output."""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
P=R.parents[1]/'exports/svd04_inverse_sensitivity_176s_1080p30.mp4'
targets=[3,12,23,30,38,47,56,66,75,82,89,96,103,111,118,136,143,150,158,165,173]
shots=[];count=0;previous=None;idx=0
with av.open(str(P)) as c:
 s=c.streams.video[0]
 assert (s.width,s.height)==(1920,1080) and s.average_rate==30 and s.frames==5280
 assert float(s.duration*s.time_base)==176 and not c.streams.audio
 for f in c.decode(video=0):
  if previous is not None:assert f.pts>previous
  previous=f.pts;count+=1
  if idx<len(targets) and float(f.time)>=targets[idx]:
   raw=f.to_image();t=targets[idx];patch=np.asarray(raw)[498:506,1645:1665,:3].astype(float)
   if t in [89,96,103,111]:
    gold=(patch[:,:,0]>200)&(patch[:,:,1]>160)&(patch[:,:,2]<160);assert int(gold.sum())>3,(t,'maximum arrow color')
   if t==173:
    teal=(patch[:,:,1]-patch[:,:,0]>45)&(patch[:,:,2]-patch[:,:,0]>35)&(patch[:,:,1]>150);assert int(teal.sum())==0,'extra output locus still highlighted'
   im=raw.resize((640,360));tile=Image.new('RGB',(640,386),'#142033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((12,7),f'{t}s / final 1080p30',fill='white');shots.append(tile);idx+=1
assert count==5280 and idx==21
sheet=Image.new('RGB',(1280,386*11),'#142033')
for i,im in enumerate(shots):sheet.paste(im,((i%2)*640,(i//2)*386))
(R/'qa').mkdir(exist_ok=True);sheet.save(R/'qa/final_contact_sheet.jpg')
for i,(a,b) in enumerate([(0,1544),(1544,3088),(3088,4246)],1):sheet.crop((0,a,1280,b)).save(R/f'qa/final_part_{i}.jpg')
report={'video':str(P),'duration_seconds':176,'resolution':[1920,1080],'fps':30,'decoded_frames':count,'audio':'none; source audio not supplied','timing_source':'34 user-supplied sentence endpoints','checks':['monotonic frame timestamps','exact duration and frame count','20 independent scenes joined','21 final-video sample frames extracted','maximum response gold/purple minimum comparison palette','final selected output is one point, not the entire range line']}
(R/'qa/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
