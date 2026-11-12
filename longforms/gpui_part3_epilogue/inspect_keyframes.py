import subprocess,argparse
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1];q=R/'qa';q.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['both','longform','shorts'],default='both');args=parser.parse_args()
for layout in (['longform','shorts'] if args.layout=='both' else [args.layout]):
 cw,ch=(640,360) if layout=='longform' else (360,640);sheet=Image.new('RGB',(cw*3,ch*2),'#0B1020');d=ImageDraw.Draw(sheet)
 for i,t in enumerate([21,62,79,87,121,133]):
  out=q/f'{layout}_{t}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(W/'exports'/f'gpui_part3_epilogue_141s_{layout}_final.mp4'),'-frames:v','1',str(out)],check=True)
  im=Image.open(out);im.thumbnail((cw,ch));x=i%3*cw;y=i//3*ch;sheet.paste(im,(x,y));d.text((x+4,y+4),f'{t}s',fill='yellow')
 sheet.save(q/f'{layout}_keyframes.jpg')
