"""Representative stills and content/subtitle safety checks."""
import json,textwrap
from pathlib import Path
from PIL import Image
from visuals import *
D=R.parents[2]/'media/classical_ch06/qa';D.mkdir(parents=True,exist_ok=True)
TIMES=[(1,8),(1,28),(2,48),(3,81),(3,92),(4,115),(5,150),(5,165),(6,199),(6,211),(7,228),(7,240),(7,250),(7,263)]
lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));images=[]
with tempconfig({'pixel_width':854,'pixel_height':480,'frame_rate':15,'verbosity':'ERROR'}):
 for i,t in TIMES:
  s=ChapterScene();s.index=i;s.prepare();g=s.geometry(t);labels=s.labels(t)
  s.add(g,labels,tx('EPILOGUE / QUANTUM',-4.9,3.6,18,MUTED,w=4.2),tx('고전역학을 넘어 이어지는 수학',3.4,3.6,22,w=6))
  line=next(x for x in lines if x['start']<=t<x['end'])
  s.add(RoundedRectangle(width=13,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-3.3,0]))
  s.add(VGroup(*[tx(p,size=25,w=12.2) for p in textwrap.wrap(line['text'],width=52,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-3.3,0]))
  s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array);im.save(D/f'{i:02}_{t}.png');images.append(im.resize((640,360)))
 for i,m in enumerate(manifest,1):
  s=ChapterScene();s.index=i;s.prepare()
  for t in sorted(set(range(m['start'],m['start']+m['duration_seconds'],2))|{x['start'] for x in lines if m['start']<=x['start']<m['start']+m['duration_seconds']}):
   for v in s.labels(t):assert v.get_left()[0]>-6.8 and v.get_right()[0]<6.8 and v.get_bottom()[1]>-2.75 and v.get_top()[1]<3.15,('label',i,t,v.get_center(),v.width,v.height)
   g=s.geometry(t)
   if len(g):assert g.get_left()[0]>=-6.9 and g.get_right()[0]<=6.9 and g.get_bottom()[1]>-2.78 and g.get_top()[1]<3.15,('geometry',i,t,g.get_bottom(),g.get_top())
 canvas=Image.new('RGB',(1280,360*7))
 for k,im in enumerate(images):canvas.paste(im,(k%2*640,k//2*360))
 canvas.save(D/'contact.png')
(R/'geometry_validation.json').write_text(json.dumps({'sampled_every_seconds':2,'safe_scenes':list(range(1,8)),'representative_frames':len(TIMES)}),encoding='utf-8')
assert len(lines)==46 and len(manifest)==7 and sum(m['duration_seconds'] for m in manifest)==265
assert (R/'tts_script.txt').read_text(encoding='utf-8').replace('\n\n','\n').strip()=='\n'.join(x['text'] for x in lines)
print('PASS: geometry, labels, exact TTS script; contact sheet',D/'contact.png')
