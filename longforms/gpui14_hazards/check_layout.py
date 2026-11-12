import sys,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import *
from check_logic import validate
validate()
assert len(TIMING)==33 and TIMING[0]['start']==0 and TIMING[-1]['end']==147
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
assert sum(m['duration_seconds'] for m in MANIFEST)==147
for r in TIMING:
 c=txt('\n'.join(textwrap.wrap(r['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4)
s=MemoryScene()
for o in [five(s),unit(s,True,True),unit(s,True,True,True)]:
 assert o.get_left()[0]>-config.frame_width/2+.15
 assert o.get_right()[0]<config.frame_width/2-.15
 assert o.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert o.get_top()[1]<(5.8 if VERT else 2.9)
print('PASS','shorts' if VERT else 'longform','timing, caption bounds, diagram bounds, hazard control/forwarding logic')
