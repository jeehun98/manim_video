"""Decode both exports, audit clocks, and capture representative final frames."""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
WORK=next(p for p in ROOT.parents if (p/'scripts/render.py').exists())

def verify(layout):
    video=WORK/'exports'/f'evdsvd02_conditions_132s_{layout}_final.mp4'
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(video)]))['streams']
    s=streams[0]
    assert len(streams)==1 and s['codec_type']=='video'
    assert int(s['nb_read_frames'])==3960 and float(s['duration'])==132
    assert s['r_frame_rate']=='30/1'
    expected=(1080,1920) if layout=='shorts' else (1920,1080)
    assert (s['width'],s['height'])==expected
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(video),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    for t,name in ([(92.6,'diagonal'),(95.6,'offdiagonal'),(131.5,'score')] if layout=='shorts' else [(105.5,'symmetry'),(109.6,'orthogonal'),(131.5,'score')]):
        target=ROOT/'qa'/f'{name}_{layout}_final.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-vf','scale=360:640' if layout=='shorts' else 'scale=960:540','-frames:v','1',str(target)],check=True)
    return dict(layout=layout,file=str(video),duration=132,frames=3960,fps=30,width=s['width'],height=s['height'],decode_check='passed',audio=False)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:report=list(pool.map(verify,['shorts','longform']))
    (ROOT/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Both 132-second final exports verified: correct dimensions, 3960 frames, full decode.')
