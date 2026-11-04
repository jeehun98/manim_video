"""Extract representative actual video frames for visual review."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
TIMES=[3,8,13,18,22,25,29,34,38,41,45,49,51,54,58,62,66,70,73,78,80,81,83,86,89,91,92,94,98,101,104,107,109,111,113,117,121,124,128,133,138]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 suffix='preview' if a.preview else 'final';qa=R/'qa'/suffix;qa.mkdir(parents=True,exist_ok=True)
 for layout in ['longform','shorts']:
  video=W/'exports'/f'gpui06_memory_140s_{layout}_{suffix}.mp4'
  tw,th=(400,225) if layout=='longform' else (225,400);cols=4 if layout=='longform' else 5
  rows=(len(TIMES)+cols-1)//cols;sheet=Image.new('RGB',(cols*tw,rows*(th+25)),(16,22,32));draw=ImageDraw.Draw(sheet)
  for i,t in enumerate(TIMES):
   path=qa/f'{layout}_{t:03}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True)
   img=Image.open(path).convert('RGB');img.thumbnail((tw,th))
   x=i%cols*tw;y=i//cols*(th+25);sheet.paste(img,(x,y));draw.text((x+8,y+th+5),f'{t:03}s',fill='white')
  out=qa/f'{layout}_contact.png';sheet.save(out);print(out)
if __name__=='__main__':main()
