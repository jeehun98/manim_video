"""Extract a reproducible visual review sheet; no source video is changed."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;W=ROOT.parents[1]
p=argparse.ArgumentParser();p.add_argument('--layout',choices=['shorts','longform'],default='shorts');p.add_argument('--final',action='store_true');a=p.parse_args()
suffix=a.layout+('_final' if a.final else '_preview')
video=W/'exports'/f'minimal01_154s_{suffix}.mp4'
folder=W/'media/minimal01_review'/suffix;folder.mkdir(parents=True,exist_ok=True)
times=[5,15,28,38,47,56,64,70,80,85,95,99,104,112,121,130,137,141,148,152]
for part in range(2):
 ts=times[part*10:(part+1)*10];thumbw=240 if a.layout=='shorts' else 480;thumbh=427 if a.layout=='shorts' else 270
 sheet=Image.new('RGB',(thumbw*5,(thumbh+26)*2),'#172235');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(ts):
  path=folder/f'{t:03}.png'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True)
  im=Image.open(path).convert('RGB').resize((thumbw,thumbh))
  x=i%5*thumbw;y=i//5*(thumbh+26);sheet.paste(im,(x,y+26));draw.text((x+8,y+5),f'{t:03}s',fill='white')
 sheet.save(folder/f'contact_{part+1}.jpg')
 print(folder/f'contact_{part+1}.jpg')
