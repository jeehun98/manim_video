import subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1];q=R/'qa';q.mkdir(exist_ok=True)
for layout in ['longform','shorts']:
 images=[]
 for t in [55,70,100,110,141]:
  out=q/f'{layout}_{t}.png'
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(W/'exports'/f'gpui12_multicycle_153s_{layout}_final.mp4'),'-frames:v','1',str(out)],check=True)
  im=Image.open(out);im.thumbnail((640,640));images.append(im.copy())
 cw=640 if layout=='longform' else 360;ch=360 if layout=='longform' else 640
 sheet=Image.new('RGB',(cw*3,ch*2),'#0B1020');d=ImageDraw.Draw(sheet)
 for i,(im,t) in enumerate(zip(images,[55,70,100,110,141])):
  x=i%3*cw;y=i//3*ch;sheet.paste(im,(x,y));d.text((x+4,y+4),f'{t}s',fill='yellow')
 sheet.save(q/f'{layout}_keyframes.jpg')
