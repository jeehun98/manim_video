from pathlib import Path
import sys,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from visuals import *
from mechanics import validate
out=R.parents[2]/'media/heat_laplacian_short/qa';out.mkdir(parents=True,exist_ok=True)
times=[8,22,39,63,85,109,137,148,166];images=[];violations=[]
with tempconfig(dict(pixel_width=360,pixel_height=640,frame_rate=15,verbosity='ERROR')):
 for i,t in enumerate(times,1):
  s=HeatScene();s.index=i;s.prepare();s.camera.reset();g=s.geometry(t);labels=s.labels(t)
  for m in labels:
   if m.get_left()[0]<-4.2 or m.get_right()[0]>4.2 or m.get_bottom()[1]<-5.65 or m.get_top()[1]>6.4:violations.append((i,t,'label',m.get_center().tolist()))
  s.add(g,labels,tx('삼각함수 · 열방정식 · 라플라스',0,7.25,26),RoundedRectangle(width=8.3,height=1.85,corner_radius=.13,stroke_width=0,fill_color='#142135',fill_opacity=1).move_to([0,-6.85,0]))
  line=next(l for l in json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'] if l['start']<=t<l['end'])
  s.add(VGroup(*[tx(p,size=26,w=7.7) for p in textwrap.wrap(line['text'],width=30,break_long_words=False,break_on_hyphens=False)]).arrange(DOWN,buff=.1).move_to([0,-6.85,0]))
  s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array);im.save(out/f'{i:02}.png');images.append(im)
 sheet=Image.new('RGB',(360*3,640*3))
 for j,im in enumerate(images):sheet.paste(im,(j%3*360,j//3*640))
 sheet.save(out/'contact.png')
 for i,(a,b) in enumerate(zip([0,12,27,43,71,98,114,139,155],[12,27,43,71,98,114,139,155,169]),1):
  s=HeatScene();s.index=i;s.prepare()
  for t in np.arange(a,b,.5):
   g=s.geometry(float(t));assert g.get_left()[0]>=-4.25 and g.get_right()[0]<=4.25 and g.get_bottom()[1]>-5.65 and g.get_top()[1]<6.4,(i,t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
assert not violations,violations
(R/'validation.json').write_text(json.dumps(dict(physics=validate(),geometry_sweep_seconds=.5,representative_times=times),indent=2),encoding='utf-8')
print('QA PASSED',out/'contact.png')
