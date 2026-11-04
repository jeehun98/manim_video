"""Extract representative actual video frames for visual review."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
TIMES=[2,7,11,15,18,24,31,38,42,48,57,61,67,73,77,85,91,94,103,110,116,122,127,132,137,143,150,155,162]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 suffix='preview' if a.preview else 'final';qa=R/'qa'/suffix;qa.mkdir(parents=True,exist_ok=True)
 for layout in ['longform','shorts']:
  video=W/'exports'/f'gpui03_logic_164s_{layout}_{suffix}.mp4'
  tw,th=(400,225) if layout=='longform' else (225,400);cols=4 if layout=='longform' else 5
  rows=(len(TIMES)+cols-1)//cols;sheet=Image.new('RGB',(cols*tw,rows*(th+25)),(16,22,32));draw=ImageDraw.Draw(sheet)
  for i,t in enumerate(TIMES):
   path=qa/f'{layout}_{t:03}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True)
   img=Image.open(path).convert('RGB');img.thumbnail((tw,th))
   x=i%cols*tw;y=i//cols*(th+25);sheet.paste(img,(x,y));draw.text((x+8,y+th+5),f'{t:03}s',fill='white')
  out=qa/f'{layout}_contact.png';sheet.save(out);print(out)
if __name__=='__main__':main()
