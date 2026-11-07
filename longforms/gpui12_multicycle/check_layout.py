import os,json,sys,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from scene_engine import *
report={}
# Caption intervals are half-open, single-object updates: no overlapping tracks.
assert len(TIMING)==33 and TIMING[0]['start']==0 and TIMING[-1]['end']==153
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
for row in TIMING:
 c=txt('\n'.join(textwrap.wrap(row['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4), (row,c.height)
scene=MemoryScene();c=board(scene)
for k in c.nodes:
 c.val(k,'LOAD R1, [100]',GREEN)
 assert c.nodes[k][1].width<c.nodes[k][0].width
 assert c.nodes[k][1].height<c.nodes[k][0].height
for obj in [c,controller(scene),scene.centered(state_rows(),7.5 if VERT else 13.4)]:
 assert obj.get_left()[0]>=-config.frame_width/2+.2
 assert obj.get_right()[0]<=config.frame_width/2-.2
 assert obj.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert obj.get_top()[1]<(5.8 if VERT else 2.9)
# LOAD control example: response stalls and destination stays in IR.
state=0;ir=None;addr=None;data=None;reg=0
for ready in [False,False,False,False,True,True]:
 if state==0:ir=('LOAD',1,100);state=1
 elif state==1:addr=ir[2];state=2
 elif state==2:
  if ready:data=5;state=3
  else:assert reg==0 and ir[1]==1
 elif state==3:reg=data;state=0
assert reg==5 and addr==100
print('PASS', 'shorts' if VERT else 'longform', 'caption geometry, circuit bounds, LOAD control')
