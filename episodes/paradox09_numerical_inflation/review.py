import json,sys,subprocess,importlib.util,math
from pathlib import Path
from decimal import Decimal,localcontext
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[2];final='--final' in sys.argv
video=R/'exports'/('paradox09.mp4' if final else 'paradox09_preview.mp4')
out=R/'media/paradox09'/('review_final' if final else 'review_preview');out.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True));v=next(s for s in info['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==((1080,1920) if final else (360,640));assert v['r_frame_rate']=='30/1';assert abs(float(info['format']['duration'])-173)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[4,11,23,26,34,39,50,55,60,69,72,76,82,90,96,104,110,116,123,128,133,143,147,157,161,169,172]
sheet=Image.new('RGB',(1440,math.ceil(len(times)/4)*670),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
 p=out/f'{sec:03}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(p)],check=True)
 im=Image.open(p).convert('RGB');im.thumbnail((360,640));x,y=i%4*360,i//4*670;sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(out/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('nfi_scene',Path(__file__).with_name('scene.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);scene=m.NumericalFeatureInflation()
for i in range(34):
 p=scene.panel(i)
 assert p.get_left()[0]>-4.15 and p.get_right()[0]<4.15,(i,'horizontal',p.get_left(),p.get_right())
 assert p.get_top()[1]<4.6 and p.get_bottom()[1]>-5,(i,'vertical',p.get_top(),p.get_bottom())
z=np.array([2.,1.,.5]);assert np.allclose(m.softmax(z),m.softmax(z+2),atol=1e-15)
g=m.softmax(z)-[1,0,0];assert abs(g.sum())<1e-15
p32=m.softmax([20,0,0],np.float32);g32=p32-np.array([1,0,0],dtype=np.float32)
assert p32[0]==1 and g32[0]==0 and np.all(g32[1:]>0) and g32.sum()>0
with localcontext() as ctx:
 ctx.prec=60;e=Decimal(-20).exp();p0=1/(1+2*e);pe=e/(1+2*e)
 assert p0<1 and abs((p0-1)+2*pe)<Decimal('1e-58')
u=np.ones(3)/np.sqrt(3);vv=np.array([-2,1,1])/np.sqrt(6)
assert abs(u@vv)<1e-15 and abs(g@u)<1e-15 and g32@u>0
# A simplified anti-parallel mean-field loop: growing feature mean drives next weight drift.
w,h=-.2,.2;increments=[]
for i in range(5):
 nw=w-.25*h;nh=h-.25*w;increments.append(abs(nw-w));w,h=nw,nh
assert all(b>a for a,b in zip(increments,increments[1:])) and w*h<0
j=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert j['sentence_end_seconds']==[5,12,16,20,24,27,30,35,40,43,51,56,61,70,73,77,83,85,91,97,100,105,111,117,124,129,134,144,148,151,158,162,170,173]
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==34
print(json.dumps(dict(duration=info['format']['duration'],size=[v['width'],v['height']],fps=v['r_frame_rate'],contact=str(out/'contact_sheet.jpg'),float32_gradient=[float(x) for x in g32],checks='34 panel bounds; exact narration ends; shift invariance; decimal zero-sum vs float32 residual; orthogonal projection; conditional feedback toy; silent'),indent=2))
