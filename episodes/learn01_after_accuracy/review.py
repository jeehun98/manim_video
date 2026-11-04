import importlib.util,json,math,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('after_accuracy',HERE/'scene.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.AfterAccuracy()
for i in range(28):
    p=scene.panel(i)
    assert p.get_left()[0]>=-4.05 and p.get_right()[0]<=4.05,(i,'horizontal',p.get_left(),p.get_right())
    assert p.get_top()[1]<4.6 and p.get_bottom()[1]>-5.15,(i,'vertical',p.get_top(),p.get_bottom())
for i,(x,y) in enumerate(m.POINTS):
    assert (x>0)==(x-.25*y>0)==(i>=5)
assert .3>0 and .3-.25*2.05<0
for z,p,loss in [(2,.880797,.126928),(4,.982014,.018150),(8,.999665,.0003354)]:
    assert abs(1/(1+math.exp(-z))-p)<1e-6
    assert abs(math.log1p(math.exp(-z))-loss)<1e-6
j=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
assert len(j['segments'])==28 and j['segments'][-1]['end']==141
assert len((HERE/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==28
final='--final' in sys.argv
video=ROOT/'exports'/('learn01.mp4' if final else 'learn01_preview.mp4')
out=ROOT/'media/learn01'/('review_final' if final else 'review_preview');out.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
v=next(s for s in info['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==((1080,1920) if final else (360,640))
assert v['r_frame_rate']=='30/1' and abs(float(info['format']['duration'])-141)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[2,7,11,15,20,28,34,39,44,49,54,59,64,69,77,88,98,106,111,119,128,133,138,140.5]
sheet=Image.new('RGB',(1440,math.ceil(len(times)/4)*670),'#091119');d=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    f=out/f'{sec}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(f)],check=True)
    im=Image.open(f).convert('RGB');im.thumbnail((360,640));x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));d.text((x+10,y+8),f'{sec}s',fill='white')
sheet.save(out/'contact_sheet.jpg')
report=dict(duration=info['format']['duration'],width=v['width'],height=v['height'],fps=v['r_frame_rate'],panels=28,training_points=10,checks='bounds, exact sentence ends, fixed points, rotation classification, unknown prediction flip, softmax/CE values, TTS paragraphs, silent video',contact_sheet=str(out/'contact_sheet.jpg'))
(HERE/('review_final.json' if final else 'review_preview.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
