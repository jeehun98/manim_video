"""Probe output metadata and inspect representative frames."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox02.mp4' if final else 'paradox02_preview.mp4')
folder=ROOT/'media'/'paradox02'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in info['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(info['format']['duration'])-96)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[3,11,18,28,33,40,45,49,58,65,69,75,85,91,95]
sheet=Image.new('RGB',(1440,2680),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:02}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('label_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.LabelSmoothingSimplex()
for i in range(19):
    panel=scene.panel(i)
    assert panel.get_left()[0]>-4.1 and panel.get_right()[0]<4.1,(i,'horizontal bounds')
    assert panel.get_top()[1]<4.6 and panel.get_bottom()[1]>-5,(i,'vertical bounds')
q=.85*m.HARD+.15*m.UNIFORM
assert np.allclose(q,m.SMOOTH)
p=np.array([.7,.2,.1]);u=m.UNIFORM
direct=-np.dot(q,np.log(p))
decomp=.85*(-np.log(p[0]))+.15*np.dot(u,np.log(u/p))+.15*np.log(3)
assert np.isclose(direct,decomp)
assert np.allclose(np.exp(np.log(q))/np.exp(np.log(q)).sum(),q)
print(json.dumps(dict(video=str(video),duration=info['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='19 panel bounds; loss decomposition; finite logits for internal target'),indent=2))
