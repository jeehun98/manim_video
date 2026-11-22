"""Camera continuity, fixed UI projection, representative world tour stills."""
import json,numpy as np
from PIL import Image
from visuals import *
D=R.parents[2]/'media/classical_ch00/qa';D.mkdir(parents=True,exist_ok=True)
TIMES=[0,16,24,30,40,50,62,70,79,82,86,90]
lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];images=[]
with tempconfig({'pixel_width':854,'pixel_height':480,'verbosity':'ERROR'}):
 s=IntroScene();s.prepare();s.lines=lines
 for t in TIMES:
  s.clear();s.set_camera(t);s.add(s.geometry(t),s.anchor_ui(s.screen_ui(t),t));s.camera.reset();s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array);im.save(D/f'{t:02}.png');images.append(im.resize((640,360)))
 for t in np.arange(0,91,.5):
  cap=s.caption(float(t));assert cap.get_left()[0]>=-6.3 and cap.get_right()[0]<=6.3 and cap.get_bottom()[1]>-3.77 and cap.get_top()[1]<-2.82,('caption',t,cap.height)
  x,w=camera_at(t);anchored=s.anchor_ui(cap.copy(),t);restored=anchored.shift([-x,0,0]).scale(FW/w,about_point=ORIGIN);assert np.max(abs(restored.get_center()-cap.get_center()))<1e-10
 for b in [24,35,54,74]:assert np.max(abs(np.array(camera_at(b-1e-5))-camera_at(b+1e-5)))<.001
 for i in range(6):
  for t in [0,16,30,50,62,70,82,90]:
   g=s.region(i,t);assert g.get_bottom()[1]>-2.8 and g.get_top()[1]<3.2,(i,t,g.get_bottom(),g.get_top())
 canvas=Image.new('RGB',(640*3,360*4))
 for k,im in enumerate(images):canvas.paste(im,(k%3*640,k//3*360))
 canvas.save(D/'contact.png')
assert len(lines)==15 and lines[-1]['end']==91
assert (R/'tts_script.txt').read_text(encoding='utf-8').replace('\n\n','\n').strip()=='\n'.join(x['text'] for x in lines)
report=dict(continuous_camera_at_segment_boundaries=True,camera_fixed_captions_verified_every_seconds=.5,caption_intervals=15,representative_frames=len(TIMES),world_regions=6,physics='reuse unchanged validated chapter05 and chapter06 models')
(R/'geometry_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('PASS camera continuity, anchored UI, exact script, regional bounds')
