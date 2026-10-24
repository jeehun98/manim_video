import json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
layout=sys.argv[1] if len(sys.argv)>1 else 'shorts'
ms=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
qa=ROOT/'qa';qa.mkdir(exist_ok=True)
w,h=(180,320) if layout=='shorts' else (320,180)
sheet=Image.new('RGB',(w*5,(h+20)*4),'#111111');draw=ImageDraw.Draw(sheet)
for i,m in enumerate(ms):
    source=ROOT/m['directory']/f'visual_{layout}_preview.mp4'
    if not source.exists():continue
    target=qa/f'{m["id"]}_{layout}_preview.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(m['duration_seconds']-.6),'-i',str(source),'-frames:v','1',str(target)],check=True)
    im=Image.open(target);im.thumbnail((w,h))
    x=(i%5)*w;y=(i//5)*(h+20);sheet.paste(im,(x,y));draw.text((x+5,y+h),m['id'],fill='white')
sheet.save(qa/f'contact_{layout}.png')
