"""Inspect key frames and probe the produced movie."""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
final = '--final' in sys.argv
video = ROOT/'exports'/('paradox01.mp4' if final else 'paradox01_preview.mp4')
folder = ROOT/'media'/'paradox01'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True, exist_ok=True)
result = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
stream = next(s for s in result['streams'] if s['codec_type']=='video')
assert (stream['width'],stream['height']) == ((1080,1920) if final else (360,640))
assert stream['r_frame_rate']=='30/1'
assert abs(float(result['format']['duration'])-98)<.05
assert not any(s['codec_type']=='audio' for s in result['streams'])
sheet = Image.new('RGB',(360*4,670*3),'#091119')
draw = ImageDraw.Draw(sheet)
for i,sec in enumerate([3,9,17,28,39,50,56,64,70,77,86,95]):
    path = folder/f'{sec:02}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB'); im.thumbnail((360,640))
    x,y = i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+12,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
print(json.dumps(dict(video=str(video),duration=result['format']['duration'],width=stream['width'],height=stream['height'],fps=stream['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg')),indent=2))
