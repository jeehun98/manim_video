"""Extract only representative new scenes and important transitions for visual QA."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[2]
video=W/'exports/euler_identity_ch00_58s_longform_final.mp4'
out=W/'media/euler_identity_ch00/review';out.mkdir(parents=True,exist_ok=True)
times=[1.9,9,11.5,15.5,18.5,21.4,33,43.5,50,57.7]
sheet=Image.new('RGB',(1920,4*390),'#10151F');draw=ImageDraw.Draw(sheet)
for k,t in enumerate(times):
    path=out/f'{k+1:02}_{t:04.1f}.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-vf','scale=640:360','-frames:v','1',str(path)],check=True)
    x=k%3*640;y=k//3*390
    sheet.paste(Image.open(path),(x,y));draw.text((x+15,y+365),f'{t:.1f} s',fill='#B8C2D1')
sheet.save(out/'contact_sheet.jpg')
print(out/'contact_sheet.jpg')
