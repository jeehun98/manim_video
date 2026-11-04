"""Extract representative actual video frames for visual review."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
TIMES=[3,8,12,16,20,25,30,35,39,42,45,49,54,60,64,69,74,78,82,84,87,90,93,96,101,105,109,112,116,119,123,129,134,139,143,147,151,155,158,162,164]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['longform','shorts','both'],default='both');a=p.parse_args()
 suffix='preview' if a.preview else 'final';qa=R/'qa'/suffix;qa.mkdir(parents=True,exist_ok=True)
 for layout in (['longform','shorts'] if a.layout=='both' else [a.layout]):
  video=W/'exports'/f'gpui10_program_165s_{layout}_{suffix}.mp4'
  tw,th=(400,225) if layout=='longform' else (225,400);cols=4 if layout=='longform' else 5
  rows=(len(TIMES)+cols-1)//cols;sheet=Image.new('RGB',(cols*tw,rows*(th+25)),(16,22,32));draw=ImageDraw.Draw(sheet)
  for i,t in enumerate(TIMES):
   path=qa/f'{layout}_{t:03}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True)
   img=Image.open(path).convert('RGB');img.thumbnail((tw,th))
   x=i%cols*tw;y=i//cols*(th+25);sheet.paste(img,(x,y));draw.text((x+8,y+th+5),f'{t:03}s',fill='white')
  out=qa/f'{layout}_contact.png';sheet.save(out);print(out)
if __name__=='__main__':main()
