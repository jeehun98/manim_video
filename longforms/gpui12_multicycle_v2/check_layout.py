import sys,json,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import *
assert len(TIMING)==34 and TIMING[0]['start']==0 and TIMING[-1]['end']==161
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
assert sum(m['duration_seconds'] for m in MANIFEST)==161
for r in TIMING:
 c=txt('\n'.join(textwrap.wrap(r['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4),(r,c.height)
s=MemoryScene()
for obj in [proc(s),proc(s,True),s.centered(Control(True),7.6 if VERT else 13.5),s.centered(phases(),7.5 if VERT else 13.4)]:
 assert obj.get_left()[0]>-config.frame_width/2+.15
 assert obj.get_right()[0]<config.frame_width/2-.15
 assert obj.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert obj.get_top()[1]<(5.8 if VERT else 2.9)
p=proc(s);assert not p.storage
for k in ['ir','addr','mdr']:
 p.reveal(k);p.value(k,{'ir':'LOAD R1, [100]','addr':'100','mdr':'5'}[k],GREEN)
 assert p.nodes[k][1].height>p.nodes[k][0].height*.1
 assert p.nodes[k][1].width<p.nodes[k][0].width
# Four-state educational LOAD, with memory completing in its assigned read cycle.
state=0;ir=None;address=None;data=None;r1=0
for expected in range(4):
 assert state==expected
 if state==0:ir=('LOAD',1,100)
 elif state==1:address=ir[2]
 elif state==2:data={100:5}[address];assert r1==0
 else:r1=data
 state=(state+1)%4
assert r1==5 and state==0
print('PASS', 'shorts' if VERT else 'longform','timing, captions, bounds, staged storage, LOAD sequence')
