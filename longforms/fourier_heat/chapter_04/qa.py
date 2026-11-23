"""Check numerical claims, every caption, safe regions, representative imagery."""
import json,hashlib,importlib.util
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from visuals import *
from mechanics import validate
out=R.parents[2]/'media/heat_ch04/qa';out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
assert len(lines)==69 and lines[0]['start']==0 and lines[-1]['end']==357
assert all(a['end']==b['start'] for a,b in zip(lines,lines[1:]))
assert sum(m['duration_seconds'] for m in manifest)==357
math=validate();images=[];audits=[]
with tempconfig(dict(pixel_width=640,pixel_height=360,frame_rate=15,verbosity='ERROR')):
 for m in manifest:
  spec=importlib.util.spec_from_file_location('qa_shot_'+m['id'],R/m['directory']/'scene.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  s=getattr(module,m['class_name'])();s.init_scene()
  # Geometry is sampled throughout every new shot, captions at all exact starts.
  for t in np.arange(s.start,s.end,.5):
   g=s.geometry(float(t))
   if len(g):assert g.get_left()[0]>=-6.9 and g.get_right()[0]<=6.9 and g.get_bottom()[1]>=-2.65 and g.get_top()[1]<=3.35,(m['id'],t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
  for line in lines:
   if s.start<=line['start']<s.end:s.update_text(line['start'])
  t=s.start+.7*m['duration_seconds'];s.update_text(t);s.add(s.geometry(t),RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#192031',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array).convert('RGB');im.save(out/f"{m['id']}.png")
  thumb=im.resize((480,270));ImageDraw.Draw(thumb).text((8,29),f"{m['id']} / {t:.1f}s",fill='white');images.append(thumb);audits.extend(s.audit)
 sheet=Image.new('RGB',(480*4,270*9),BG)
 for j,im in enumerate(images):sheet.paste(im,(j%4*480,j//4*270))
 sheet.save(out/'contact.png')
digest=hashlib.sha256(b''.join((R/f).read_bytes() for f in ['visuals.py','mechanics.py','timing.json','manifest.json'])+b''.join((R/m['directory']/'scene.py').read_bytes() for m in manifest)).hexdigest()
(R/'validation.json').write_text(json.dumps(dict(input_sha256=digest,sentence_count=69,scene_count=33,duration=357,math=math,geometry_step_seconds=.5,audits=audits),ensure_ascii=False,indent=2),encoding='utf-8')
print('QA PASSED',out/'contact.png')
