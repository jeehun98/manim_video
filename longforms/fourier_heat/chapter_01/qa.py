"""Numerical, timing, safe-area sweep and representative contact sheet."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from visuals import *
out=R.parents[2]/'media/heat_ch01/qa';out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
assert len(lines)==28 and lines[-1]['end']==169
assert all(a['end']==b['start'] for a,b in zip(lines,lines[1:]))
x=np.linspace(0,1,2001);dt=1e-5;dx=x[1]-x[0];u=heat(x,.4)
res=(heat(x,.4+dt)-heat(x,.4-dt))/(2*dt)-.08*(u[2:]-2*u[1:-1]+u[:-2])/dx**2 if False else None
res=(heat(x[1:-1],.4+dt)-heat(x[1:-1],.4-dt))/(2*dt)-.08*(u[2:]-2*u[1:-1]+u[:-2])/dx**2
assert np.max(abs(res))<1e-4
assert abs(np.trapezoid(heat(x,0),x)-np.trapezoid(heat(x,2),x))<1e-10
images=[];audits=[]
with tempconfig(dict(pixel_width=640,pixel_height=360,frame_rate=15,verbosity='ERROR')):
 for m in manifest:
  s=HeatScene();s.index=int(m['id']);s.rec=m;s.start=m['start'];s.end=s.start+m['duration_seconds'];s.audit=[];s.lines=lines
  rng=np.random.default_rng(20261123);s.walks=np.concatenate([np.zeros((110,1,2)),np.cumsum(rng.normal(0,.14,(110,96,2)),axis=1)],axis=1);s.price=np.cumsum(rng.normal(0,.10,(7,120)),axis=1)
  for t in np.arange(s.start,s.end,.5):
   g=s.geometry(float(t))
   if len(g):assert g.get_left()[0]>=-6.85 and g.get_right()[0]<=6.85 and g.get_bottom()[1]>=-2.65 and g.get_top()[1]<=3.8,(m['id'],t,g.get_left(),g.get_right(),g.get_bottom(),g.get_top())
  t=s.start+m['duration_seconds']*.7
  s.caption=VGroup();s.static=VGroup();s.update_text(t)
  s.add(s.geometry(t),RoundedRectangle(width=12.9,height=1.05,corner_radius=.12,stroke_width=0,fill_color='#141E33',fill_opacity=1).move_to([0,-3.27,0]).set_z_index(50))
  s.camera.capture_mobjects(s.mobjects);im=Image.fromarray(s.camera.pixel_array).convert('RGB');im.save(out/f"{m['id']}.png")
  small=im.resize((480,270));ImageDraw.Draw(small).text((8,6),f"{m['id']} / {t:.1f}s",fill='white');images.append(small);audits.extend(s.audit)
 sheet=Image.new('RGB',(480*4,270*6),BG)
 for j,im in enumerate(images):sheet.paste(im,(j%4*480,j//4*270))
 sheet.save(out/'contact.png')
(R/'validation.json').write_text(json.dumps(dict(sentence_count=28,duration=169,scene_count=23,heat_pde_max_residual=float(np.max(abs(res))),heat_energy_conserved=True,geometry_step_seconds=.5,representative_audits=audits),ensure_ascii=False,indent=2),encoding='utf-8')
print('QA PASSED',out/'contact.png')
