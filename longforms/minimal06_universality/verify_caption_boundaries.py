"""Compare every sentence boundary frame with a clean, single-track reference."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from caption_pass import ROOT,W,create_ass
p=argparse.ArgumentParser();p.add_argument('--layout',choices=['shorts','longform'],required=True);a=p.parse_args()
rows=json.loads((ROOT/'narration_timing.json').read_text(encoding='utf-8'))
frames=sorted({f for r in rows for f in [int(r['start']*30)-1,int(r['start']*30),int(r['start']*30)+1] if 0<=f<4800}|{4799})
short=a.layout=='shorts';width,height=(1080,1920) if short else (1920,1080)
y,h=(1430,330) if short else (820,185)
folder=W/'media/minimal06_caption_verify'/a.layout;folder.mkdir(parents=True,exist_ok=True)
select="select='"+'+'.join(f'between(n,{max(0,int(r["start"]*30)-1)},{int(r["start"]*30)+1})' for r in rows)+"+eq(n,4799)'"
fixed=W/'exports'/f'minimal06_160s_{a.layout}_final.mp4'
ass=create_ass(a.layout)
for reference in [False,True]:
 args=['ffmpeg','-hide_banner','-loglevel','error','-y']
 args+=['-f','lavfi','-i',f'color=c=0x0B1423:s={width}x{height}:r=30:d=160'] if reference else ['-i',str(fixed)]
 vf=select+(f',ass={ass.name}' if reference else '')+f',crop={width}:{h}:0:{y}'
 args+=['-vf',vf,'-fps_mode','vfr',str(folder/('ref_%03d.png' if reference else 'actual_%03d.png'))]
 subprocess.run(args,cwd=ROOT,check=True)
scores=[]
for i,f in enumerate(frames,1):
 actual=np.asarray(Image.open(folder/f'actual_{i:03}.png').convert('RGB'))
 ref=np.asarray(Image.open(folder/f'ref_{i:03}.png').convert('RGB'))
 am=actual.mean(axis=2)>120;rm=ref.mean(axis=2)>120
 union=(am|rm).sum();score=float((am&rm).sum()/max(1,union))
 scores.append(dict(frame=f,time=f/30,iou=score))
assert min(s['iou'] for s in scores)>.90,sorted(scores,key=lambda s:s['iou'])[:5]
report=dict(layout=a.layout,checked_frames=len(frames),sentence_boundaries=len(rows),minimum_text_mask_iou=min(s['iou'] for s in scores),results=scores)
(ROOT/f'caption_boundary_verification_{a.layout}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
# Review the term introduction and the central experiment boundaries.
picked=[i for i,f in enumerate(frames,1) if f in [1679,1680,1681,1919,1920,1921,2429,2430,2431,3149,3150,3151]]
tw=540;th=round(h*tw/width)
sheet=Image.new('RGB',(tw*3,(th+24)*4),'#152338');draw=ImageDraw.Draw(sheet)
for j,i in enumerate(picked):
 x=j%3*tw;yy=j//3*(th+24)
 sheet.paste(Image.open(folder/f'actual_{i:03}.png').resize((tw,th)),(x,yy+24));draw.text((x+5,yy+4),f'{frames[i-1]/30:.3f}s',fill='white')
sheet.save(folder/'boundary_contact.png')
print(json.dumps({k:v for k,v in report.items() if k!='results'}))
