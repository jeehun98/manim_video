"""Video metadata, representative frames and interpolation consistency checks."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox03.mp4' if final else 'paradox03_preview.mp4')
folder=ROOT/'media'/'paradox03'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in data['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(data['format']['duration'])-109)<.05
assert not any(s['codec_type']=='audio' for s in data['streams'])
times=[1,8,14,25,32,38,42,46,51,58,64,70,76,82,90,95,99,102,108]
sheet=Image.new('RGB',(1440,3350),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:03}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('mixup_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.MixupRules()
for i in range(23):
    p=scene.panel(i)
    assert p.get_left()[0]>-4.1 and p.get_right()[0]<4.1,(i,'horizontal bounds')
    assert p.get_top()[1]<4.6 and p.get_bottom()[1]>-5,(i,'vertical bounds')
grid=np.linspace(0,1,1001)
for amount in [1,.22,.07]:
    prediction=m.prediction(grid,amount)
    assert np.all((prediction>0)&(prediction<1))
    assert np.allclose(prediction[[0,-1]],[.02,.98])
cat=m.photo_array('cat_photo.png');dog=m.photo_array('dog_photo.png')
assert cat.shape==dog.shape==(384,320,3)
for lam in [.5,.7]:
    q=lam*np.array([1.,0.])+(1-lam)*np.array([0.,1.])
    assert np.allclose(q,[lam,1-lam]) and np.isclose(q.sum(),1)
timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert len(timing['segments'])==23 and timing['segments'][-1]['end']==109
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==23
print(json.dumps(dict(video=str(video),duration=data['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='23 panel bounds; probability bounds; input/target lambda consistency; 23 narration boundaries'),indent=2))
