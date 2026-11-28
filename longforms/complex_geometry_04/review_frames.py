import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
mode=sys.argv[1] if len(sys.argv)>1 else 'preview'
media=ROOT/'media/complex_geometry_04_v1_243s/longform/standalone'/mode
review=HERE/'review';review.mkdir(exist_ok=True)
samples=[('02',16),('05',13.5),('05',19),('07',4),('08',10),('10',15.5),('12',14),('14',21)]
if mode=='final':samples+=[('06',15),('09',14.7),('13',14.7)]
frames=[]
for id,t in samples:
 stamp=media/(id+'.json')
 if not stamp.exists():continue
 clip=json.loads(stamp.read_text())['clip'];out=review/f'{mode}_{id}_{t}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',clip,'-frames:v','1','-update','1',str(out)],check=True)
 im=Image.open(out).convert('RGB');im.thumbnail((800,450));tile=Image.new('RGB',(800,478),'#101722');tile.paste(im,(0,28));ImageDraw.Draw(tile).text((12,7),f'{mode} | scene {id} + {t}s',fill='white');frames.append(tile)
sheet=Image.new('RGB',(1600,478*((len(frames)+1)//2)),'#101722')
for i,im in enumerate(frames):sheet.paste(im,((i%2)*800,(i//2)*478))
sheet.save(review/(mode+'_contact.png'));print(review/(mode+'_contact.png'))
