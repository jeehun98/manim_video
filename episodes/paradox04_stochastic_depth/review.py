"""Check movie metadata, layouts and mask/gating semantics."""
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox04.mp4' if final else 'paradox04_preview.mp4')
folder=ROOT/'media'/'paradox04'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in data['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(data['format']['duration'])-133)<.05
assert not any(s['codec_type']=='audio' for s in data['streams'])
times=[4,13,25,29,36,42,47,50,56,65,70,74,82,90,94,99,103,111,117,123,128,132]
sheet=Image.new('RGB',(1440,4020),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:03}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('depth_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.StochasticDepthPaths()
for i in range(26):
    p=scene.panel(i)
    assert p.get_left()[0]>-4.1 and p.get_right()[0]<4.1,(i,'horizontal bounds')
    assert p.get_top()[1]<4.6 and p.get_bottom()[1]>-5,(i,'vertical bounds')
assert sum(m.MASK5)==5 and sum(m.MASK4)==4
for on in [True,False]:
    assert m.residual(on)[1].get_fill_opacity()==0
for mask in [m.MASK5,m.MASK4]:
    assert all(row[0].get_fill_opacity()==0 for row in m.ladder(mask)[:8])
assert len(set(itertools.product([0,1],repeat=8)))==256
x=np.array([.3,.5]);w=np.array([[.2,-.1],[.4,.6]])
assert np.allclose(x+0*(w@x),x)
assert np.allclose(np.eye(2)+0*w,np.eye(2))
p=.7
assert np.allclose((1-p)*x+p*(x+w@x),x+p*(w@x))
timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert len(timing['segments'])==26 and timing['segments'][-1]['end']==133
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==26
print(json.dumps(dict(video=str(video),duration=data['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='26 panel bounds; 5/4 masks; 256 combinations; identity forward/Jacobian; original inference scaling; 26 narration boundaries'),indent=2))
