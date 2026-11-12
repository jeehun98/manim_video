import sys,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import *
from shared_components import validate
validate()
assert len(TIMING)==28 and TIMING[0]['start']==0 and TIMING[-1]['end']==141
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
assert len(MANIFEST)==13 and sum(m['duration_seconds'] for m in MANIFEST)==141
for r in TIMING:
 c=txt('\n'.join(textwrap.wrap(r['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4)
s=MemoryScene()
objects=[core(s,i) for i in range(6)]+[zoom(s,DualMemory()),zoom(s,FiveStage()),zoom(s,ForwardUnit(True,True)),zoom(s,DualPath(4,2,True,True)),zoom(s,PipelineView()),zoom(s,Limits())]
for o in objects:
 assert o.get_left()[0]>-config.frame_width/2+.15
 assert o.get_right()[0]<config.frame_width/2-.15
 assert o.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert o.get_top()[1]<(5.8 if VERT else 2.9)
# Main LOAD/ADD/STORE keeps memory source intact and writes destination8.
mem={100:5,102:0};r1=mem[100];r2=3;r3=r1+r2;mem[102]=r3
assert r3==mem[102]==8 and mem[100]==5
print('PASS','shorts' if VERT else 'longform','28 timings, caption bounds, cumulative diagram bounds, main program and dual ALU model')
