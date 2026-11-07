import sys,textwrap
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import *
assert len(TIMING)==29 and TIMING[-1]['end']==148 and TIMING[0]['start']==0
assert all(a['end']==b['start'] for a,b in zip(TIMING,TIMING[1:]))
for r in TIMING:
 c=txt('\n'.join(textwrap.wrap(r['text'],width=26 if VERT else 52)),30 if VERT else 29,INK,7.55 if VERT else 14.2)
 if VERT and c.height>1.95:c.scale_to_fit_height(1.95)
 assert c.height<=(2.25 if VERT else 1.4)
s=MemoryScene()
for o in [hw(s),dual(s,True),pipe(s,True,True),s.centered(Schedule(),7.7 if VERT else 13)]:
 assert o.get_left()[0]>-config.frame_width/2+.15
 assert o.get_right()[0]<config.frame_width/2-.15
 assert o.get_bottom()[1]>(-4.5 if VERT else -2.5)
 assert o.get_top()[1]<(5.8 if VERT else 2.9)
# Registers sampled at an edge use the previous stage's packet, never the new one.
fd=dm=mw=None;regs={1:0,2:0};memory={100:5,101:3};program=[dict(owner='A',address=100,dest=1,read=True,write=True),dict(owner='B',address=101,dest=2,read=True,write=True)];completed=[]
for cycle in range(1,6):
 if mw:
  assert mw['write'];regs[mw['dest']]=mw['data'];completed.append((mw['owner'],cycle))
 newmw=dict(dm,data=memory[dm['address']]) if dm else None
 newdm=dict(fd) if fd else None
 newfd=dict(program[cycle-1]) if cycle<=2 else None
 fd,dm,mw=newfd,newdm,newmw
 if cycle==3:
  assert mw['owner']=='A' and mw['data']==5 and mw['dest']==1
  assert dm['owner']=='B' and dm['address']==101 and dm['dest']==2
assert regs=={1:5,2:3} and completed==[('A',4),('B',5)]
assert memory=={100:5,101:3}
p=pipe(s,True,True)
for n in range(1,6):p.cycle(n)
print('PASS', 'shorts' if VERT else 'longform', 'caption bounds, pipeline ownership, edge snapshots, A4/B5 completion')
