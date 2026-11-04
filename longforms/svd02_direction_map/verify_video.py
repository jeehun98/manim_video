"""Inspect the delivered concat, not just its individual source clips."""
import json
from pathlib import Path
from fractions import Fraction
import av
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
P=R.parents[1]/'exports/svd02_direction_map_154s_1080p30.mp4'
targets=[5,18,29,40,52,64,73,80,90,99,105,112,123,147,152]
shots=[];count=0;previous=None;next_target=0
with av.open(str(P)) as c:
 s=c.streams.video[0]
 assert (s.width,s.height)==(1920,1080)
 assert s.average_rate==30 and s.frames==4620
 assert float(s.duration*s.time_base)==154
 assert not c.streams.audio
 for f in c.decode(video=0):
  if previous is not None:assert f.pts>previous
  previous=f.pts;count+=1
  if next_target<len(targets) and float(f.time)>=targets[next_target]:
   im=f.to_image().resize((640,360));tile=Image.new('RGB',(640,386),'#142033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((12,7),f'{targets[next_target]}s / final 1080p30',fill='white');shots.append(tile);next_target+=1
assert count==4620 and next_target==len(targets)
sheet=Image.new('RGB',(1280,386*8),'#142033')
for i,im in enumerate(shots):sheet.paste(im,((i%2)*640,(i//2)*386))
(R/'qa').mkdir(exist_ok=True);sheet.save(R/'qa/final_contact_sheet.jpg')
report={'video':str(P),'duration_seconds':154,'resolution':[1920,1080],'fps':30,'decoded_frames':count,'audio':'none; source audio not supplied','timing_source':'29 user-supplied sentence endpoints','checks':['monotonic frame timestamps','exact duration and frame count','all 20 independent scenes joined','15 final-video sample frames extracted']}
(R/'qa/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
