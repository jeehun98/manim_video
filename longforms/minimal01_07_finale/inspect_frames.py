from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
r=Path('longforms/minimal01_07_finale');folder=Path('media/minimal01_07_review');folder.mkdir(parents=True,exist_ok=True)
ts=[2,6,14,18,29,38,46,53,61,69,76,84,94,102,113,119,125,136,142,159]
for part in range(2):
 sheet=Image.new('RGB',(1600,4*247),'#152338');draw=ImageDraw.Draw(sheet)
 for j,t in enumerate(ts[part*10:(part+1)*10]):
  p=folder/f'{t}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i','exports/minimal01_07_finale_163s_longform_preview.mp4','-frames:v','1',str(p)],check=True)
  im=Image.open(p).convert('RGB').resize((400,225));x=j%4*400;y=j//4*247;sheet.paste(im,(x,y+22));draw.text((x+8,y+4),f'{t}s',fill='white')
 sheet.save(folder/f'contact{part}.jpg')
