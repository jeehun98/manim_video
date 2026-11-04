import json
from pathlib import Path
import av
from PIL import Image,ImageDraw
R=Path('longforms/svd01_distinguish_inputs');manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
shots=[]
for t in [5,15,27,38,47,61,68,76,87,94,102,112,123,130]:
 m=next(m for m in manifest if m['start']<=t<m['end']);p=R/m['directory']/'visual_1080p30.mp4'
 if not p.exists():p=R/m['directory']/'visual_preview.mp4'
 if not p.exists():continue
 try:
  with av.open(str(p)) as c:
   f=next(f for f in c.decode(video=0) if float(f.time)>=t-m['start'])
   im=f.to_image().resize((640,360));tile=Image.new('RGB',(640,386),'#142033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((12,7),f'{t}s / scene {m["id"]}',fill='white');shots.append(tile)
 except Exception:continue
sheet=Image.new('RGB',(1280,386*((len(shots)+1)//2)),'#142033')
for i,im in enumerate(shots):sheet.paste(im,((i%2)*640,(i//2)*386))
(R/'qa').mkdir(exist_ok=True);sheet.save(R/'qa/contact_sheet.jpg');print(len(shots),'frames inspected in sheet')
