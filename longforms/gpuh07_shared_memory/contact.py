from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
for layout in ['shorts','longform']:
 source=P.parents[1]/'exports'/f'gpuh07_shared_memory_160s_{layout}_final.mp4'
 if not source.exists():continue
 thumbs=[]
 for i,shot in enumerate(m):
  out=P/f'qa_{layout}_{i:02}.png';t=shot['start']+shot['duration_seconds']*.65
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=270:-1' if layout=='shorts' else 'scale=480:-1',str(out)],check=True)
  im=Image.open(out).convert('RGB');canvas=Image.new('RGB',(im.width,im.height+24),'#172238');canvas.paste(im,(0,24));ImageDraw.Draw(canvas).text((6,6),f'{i+1:02} | {t:.1f}s',fill='white');thumbs.append(canvas)
 cols=5 if layout=='shorts' else 3;w,h=thumbs[0].size;sheet=Image.new('RGB',(cols*w,((len(thumbs)+cols-1)//cols)*h),'#0B1220')
 for i,im in enumerate(thumbs):sheet.paste(im,((i%cols)*w,(i//cols)*h))
 sheet.save(P/f'contact_{layout}.jpg')
