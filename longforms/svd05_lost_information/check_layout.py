from pathlib import Path
import sys
from PIL import Image,ImageDraw
from manim import tempconfig
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from scene_engine import LossScene,RankScene
targets=[4,20,32,47,56,66,73,77,82,90,106,114,120,128,138,150,157,167,171,173,181,189,198,213,221,228,235,250]
shots=[]
for t in targets:
 base=RankScene if 58<=t<85 else LossScene
 class Snap(base):start_time=t;end_time=t+.04
 with tempconfig({'pixel_width':1280,'pixel_height':720,'frame_rate':25,'dry_run':True,'skip_animations':True,'progress_bar':'none','verbosity':'ERROR'}):
  s=Snap();s.render();s.renderer.update_frame(s);im=Image.fromarray(s.renderer.get_frame()).convert('RGB')
 (R/'qa').mkdir(exist_ok=True);im.save(R/f'qa/layout_{t}.png');im=im.resize((640,360));tile=Image.new('RGB',(640,386),'#142033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((12,7),f'{t}s',fill='white');shots.append(tile)
 print('SNAP',t,flush=True)
for start in range(0,len(shots),8):
 subset=shots[start:start+8];sheet=Image.new('RGB',(1280,386*((len(subset)+1)//2)),'#142033')
 for i,im in enumerate(subset):sheet.paste(im,((i%2)*640,(i//2)*386))
 sheet.save(R/f'qa/layout_part_{start//8+1}.jpg')
