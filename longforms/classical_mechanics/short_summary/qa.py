"""Vertical representative stills, timing and layout safety."""
import json,textwrap
from PIL import Image
from visuals import *
D=R.parents[2]/'media/classical_short/qa';D.mkdir(parents=True,exist_ok=True)
TIMES=[(1,18),(2,42),(3,58),(4,80),(5,98),(5,121),(6,132),(7,149),(8,160),(9,172)]
lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));images=[]
with tempconfig({'pixel_width':360,'pixel_height':640,'frame_rate':15,'verbosity':'ERROR'}):
 for i,t in TIMES:
  s=SummaryScene();s.index=i;s.prepare();s.add(s.geometry(t),s.labels(t),tx('뉴턴에서 해밀토니안까지',0,7.25,28,w=8))
  line=next(x for x in lines if x['start']<=t<x['end'])
  s.add(RoundedRectangle(width=8.3,height=1.85,corner_radius=.13,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-6.85,0]))
  s.add(VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]))
  s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array);im.save(D/f'{i:02}_{t}.png');images.append(im)
 for i,m in enumerate(manifest,1):
  s=SummaryScene();s.index=i;s.prepare()
  for t in sorted(set(range(m['start'],m['start']+m['duration_seconds']))|{x['start'] for x in lines if m['start']<=x['start']<m['start']+m['duration_seconds']}):
   for v in s.labels(t):assert v.get_left()[0]>-4.2 and v.get_right()[0]<4.2 and v.get_bottom()[1]>-5.65 and v.get_top()[1]<6.4,('label',i,t,v.get_center(),v.width,v.height)
   g=s.geometry(t)
   if len(g):assert g.get_left()[0]>=-4.25 and g.get_right()[0]<=4.25 and g.get_bottom()[1]>-5.65 and g.get_top()[1]<6.4,('geometry',i,t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
 for line in lines:
  cap=VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]);assert cap.get_bottom()[1]>-7.8 and cap.get_top()[1]<-5.9,('caption',line['id'],cap.height)
 canvas=Image.new('RGB',(360*5,640*2))
 for k,im in enumerate(images):canvas.paste(im,(k%5*360,k//5*640))
 canvas.save(D/'contact.png')
assert len(lines)==37 and sum(x['duration_seconds'] for x in manifest)==174
assert (R/'tts_script.txt').read_text(encoding='utf-8').replace('\n\n','\n').strip()=='\n'.join(x['text'] for x in lines)
(R/'geometry_validation.json').write_text(json.dumps({'every_seconds':1,'scenes':9,'caption_intervals':37,'representative_frames':10}),encoding='utf-8');print('PASS vertical geometry, labels and captions')
