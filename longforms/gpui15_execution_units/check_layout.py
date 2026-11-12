import sys,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import *
from check_logic import validate
validate()
assert len(TIMING)==26 and TIMING[0]['start']==0 and TIMING[-1]['end']==141
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
assert sum(m['duration_seconds'] for m in MANIFEST)==141
for r in TIMING:
 c=txt('\n'.join(textwrap.wrap(r['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4)
s=MemoryScene()
for o in [circuit(s),circuit(s,4,2,True,True),s.centered(pair_cards(),7.6 if VERT else 13.5)]:
 assert o.get_left()[0]>-config.frame_width/2+.15
 assert o.get_right()[0]<config.frame_width/2-.15
 assert o.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert o.get_top()[1]<(5.8 if VERT else 2.9)
p=circuit(s,4,2,True,True);p.compute();p.capture();p.write_edge();assert p.state[3]==8 and p.state[6]==7
print('PASS','shorts' if VERT else 'longform','timing, caption/diagram bounds, port limits, ALU math and destinations')
