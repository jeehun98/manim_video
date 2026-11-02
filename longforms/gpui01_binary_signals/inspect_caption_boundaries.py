"""Review real encoded frames before/at/after every supplied caption boundary."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 fps=15 if a.preview else 30;suffix='preview' if a.preview else 'final'
 rows=json.loads((R/'timing.json').read_text(encoding='utf-8'))
 assert rows[0]['start']==0 and rows[-1]['end']==113
 assert all(x['end']==y['start'] for x,y in zip(rows,rows[1:]))
 boundaries=[0]+[x['end'] for x in rows[:-1]]
 frames=sorted(set(max(0,int(t*fps)+d) for t in boundaries for d in [-1,0,1]))
 expr='+'.join(f'eq(n,{n})' for n in frames)
 qa=R/'qa'/f'caption_{suffix}';qa.mkdir(parents=True,exist_ok=True)
 for layout in ['longform','shorts']:
  video=W/'exports'/f'gpui01_binary_113s_{layout}_{suffix}.mp4'
  # Relative crops use the dedicated bottom subtitle region, excluding notes.
  crop='crop=iw:ih*0.1556:0:ih*0.7778' if layout=='longform' else 'crop=iw:ih*0.1406:0:ih*0.7883'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-vf',f"select='{expr}',{crop}",'-fps_mode','vfr',str(qa/f'{layout}_%03d.png')],check=True)
  paths={n:qa/f'{layout}_{i+1:03}.png' for i,n in enumerate(frames)}
  tw=600 if layout=='longform' else 360
  th=Image.open(paths[0]).height*tw//Image.open(paths[0]).width
  for page in range((len(boundaries)+8)//9):
   subset=boundaries[page*9:(page+1)*9]
   sheet=Image.new('RGB',(tw*3,(th+25)*len(subset)),(18,25,37));draw=ImageDraw.Draw(sheet)
   for row,t in enumerate(subset):
    for col,d in enumerate([-1,0,1]):
     n=max(0,int(t*fps)+d);im=Image.open(paths[n]).convert('RGB').resize((tw,th))
     x=col*tw;y=row*(th+25);sheet.paste(im,(x,y));draw.text((x+8,y+th+5),f'{t}s  frame {n}  ({n/fps:.3f}s)',fill='white')
   out=qa/f'{layout}_boundaries_{page+1}.jpg';sheet.save(out,quality=92);print(out)
 (qa/'audit.json').write_text(json.dumps(dict(sentence_count=len(rows),duration_seconds=113,boundary_count=len(boundaries),frames=frames,policy='One initialized Text object, replaced at half-open sentence boundaries; no caption fades.'),indent=2),encoding='utf-8')
if __name__=='__main__':main()
