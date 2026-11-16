"""Inspect representative new scenes and compare the chapter 03 bridge."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[2]
video=W/'exports/euler_identity_ch04_202s_longform_final.mp4';out=W/'media/euler_identity_ch04/review';out.mkdir(parents=True,exist_ok=True)
def frame(src,t,path,size=None):
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(src)]
    if size:args+=['-vf',f'scale={size}']
    subprocess.run(args+['-frames:v','1',str(path)],check=True)
times=[0,20,33,45,56,71,85,100,116,130,144.5,156.8,160,165.5,170,184,192.5,201]
for part,subset in enumerate([times[:9],times[9:]],1):
    sheet=Image.new('RGB',(1920,3*390),'#10151F');draw=ImageDraw.Draw(sheet)
    for k,t in enumerate(subset):
        path=out/f'{t:05.1f}.png'
        if not path.exists() or path.stat().st_mtime<video.stat().st_mtime:frame(video,t,path,'640:360')
        x=k%3*640;y=k//3*390;sheet.paste(Image.open(path),(x,y));draw.text((x+15,y+365),f'{t:.1f} s',fill='#B8C2D1')
    sheet.save(out/f'contact_sheet_{part}.jpg')
previous=W/'exports/euler_identity_ch03_171s_longform_final.mp4';pt=170.966667
if not previous.exists():previous=W/'media/euler_identity_ch03/final/14.mp4';pt=5.966667
frame(previous,pt,out/'previous_end.png');frame(video,0,out/'current_start.png')
a=np.asarray(Image.open(out/'previous_end.png').convert('RGB'))[:875].astype(float);b=np.asarray(Image.open(out/'current_start.png').convert('RGB'))[:875].astype(float)
error=float(np.mean(np.abs(a-b)));assert error<2,error
p=R/'verification_final.json';report=json.loads(p.read_text(encoding='utf-8'));report['chapter_03_bridge']={'reference':str(previous),'mean_absolute_pixel_difference_excluding_caption':error,'passed':True};p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(out/'contact_sheet_1.jpg');print(out/'contact_sheet_2.jpg');print('Bridge difference:',error)
