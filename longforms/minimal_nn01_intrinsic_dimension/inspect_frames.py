"""Create labelled contact sheets from actual rendered frames."""
import subprocess,argparse
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args()
 for layout in ['longform','shorts']:
  suffix=layout+('_final' if a.final else '_preview')
  source=W/'exports'/f'minimal_nn01_intrinsic_129s_{suffix}.mp4'
  if not source.exists():continue
  times=[5,11,24,28,34,41,46,55,68,74,80,85,94,102,111,121,127]
  size=(384,216) if layout=='longform' else (216,384);cols=4 if layout=='longform' else 6
  sheet=Image.new('RGB',(cols*size[0],((len(times)+cols-1)//cols)*(size[1]+24)),(30,35,45));d=ImageDraw.Draw(sheet)
  folder=R/'qa'/suffix;folder.mkdir(parents=True,exist_ok=True)
  for i,t in enumerate(times):
   out=folder/f'{t:03}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1',str(out)],check=True)
   im=Image.open(out);im.thumbnail(size);x=i%cols*size[0];y=i//cols*(size[1]+24)
   sheet.paste(im,(x,y+24));d.text((x+5,y+5),f'{t:03}s',fill='white')
  sheet.save(R/'qa'/f'{suffix}_contact.png')
if __name__=='__main__':main()
