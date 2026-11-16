"""Review new scenes and compare the bridge to chapter 01's last rendered scene."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[2]
video=W/'exports/euler_identity_ch02_142s_longform_final.mp4'
out=W/'media/euler_identity_ch02/review';out.mkdir(parents=True,exist_ok=True)
def frame(src,t,path,size=None):
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(src)]
    if size:args+=['-vf',f'scale={size}']
    subprocess.run(args+['-frames:v','1',str(path)],check=True)
times=[0,14,23.5,30.5,35,48,60.5,73.5,81.5,94,104,117,132,140.5]
sheet=Image.new('RGB',(1920,5*390),'#10151F');draw=ImageDraw.Draw(sheet)
for k,t in enumerate(times):
    path=out/f'{k+1:02}_{t:05.1f}.png'
    if not path.exists() or path.stat().st_mtime<video.stat().st_mtime:frame(video,t,path,'640:360')
    x=k%3*640;y=k//3*390;sheet.paste(Image.open(path),(x,y));draw.text((x+15,y+365),f'{t:.1f} s',fill='#B8C2D1')
sheet.save(out/'contact_sheet.jpg')
previous=W/'exports/euler_identity_ch01_83s_longform_final.mp4';pt=82.966667
if not previous.exists():previous=W/'media/euler_identity_ch01/final/12.mp4';pt=4.966667
frame(previous,pt,out/'previous_end.png');frame(video,0,out/'current_start.png')
a=np.asarray(Image.open(out/'previous_end.png').convert('RGB'))[:875].astype(float)
b=np.asarray(Image.open(out/'current_start.png').convert('RGB'))[:875].astype(float)
error=float(np.mean(np.abs(a-b)));assert error<2,error
p=R/'verification_final.json';report=json.loads(p.read_text(encoding='utf-8'))
report['chapter_01_bridge']={'reference':str(previous),'mean_absolute_pixel_difference_excluding_caption':error,'passed':True}
p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(out/'contact_sheet.jpg');print('Bridge difference:',error)
