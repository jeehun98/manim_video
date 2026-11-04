"""Extract representative actual video frames for visual review."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
TIMES=[3,8,12,17,21,24,28,32,35,38,40,45,48,50,53,56,60,64,66,68,72,76,81,87,91,96,100,105,109,114,118,123,125,126,128,131,134,138,145,151,155,159,165,169,174]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 suffix='preview' if a.preview else 'final';qa=R/'qa'/suffix;qa.mkdir(parents=True,exist_ok=True)
 for layout in ['longform','shorts']:
  video=W/'exports'/f'gpui05_alu_175s_{layout}_{suffix}.mp4'
  tw,th=(400,225) if layout=='longform' else (225,400);cols=4 if layout=='longform' else 5
  rows=(len(TIMES)+cols-1)//cols;sheet=Image.new('RGB',(cols*tw,rows*(th+25)),(16,22,32));draw=ImageDraw.Draw(sheet)
  for i,t in enumerate(TIMES):
   path=qa/f'{layout}_{t:03}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(path)],check=True)
   img=Image.open(path).convert('RGB');img.thumbnail((tw,th))
   x=i%cols*tw;y=i//cols*(th+25);sheet.paste(img,(x,y));draw.text((x+8,y+th+5),f'{t:03}s',fill='white')
  out=qa/f'{layout}_contact.png';sheet.save(out);print(out)
if __name__=='__main__':main()
