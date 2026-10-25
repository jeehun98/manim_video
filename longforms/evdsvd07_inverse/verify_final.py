"""Audit complete 142-second exports, including the user's confirmed ending."""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent;WORK=ROOT.parents[1]
def verify(layout):
    video=WORK/'exports'/f'evdsvd07_inverse_142s_{layout}_final.mp4'
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(video)]))['streams']
    s=streams[0]
    assert len(streams)==1 and s['codec_type']=='video'
    assert int(s['nb_read_frames'])==4260 and float(s['duration'])==142
    assert s['r_frame_rate']=='30/1'
    assert (s['width'],s['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(video),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    for t,name in [(11.5,'ellipse'),(17.5,'restore'),(55.,'svdinverse'),(66.5,'collapse'),(69.5,'overlap'),(92.,'nullspace'),(101.5,'notmagic'),(109.5,'minnorm'),(114.5,'systems'),(141.5,'score')]:
        target=ROOT/'qa'/f'{name}_{layout}_final.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-vf','scale=360:640' if layout=='shorts' else 'scale=960:540','-frames:v','1',str(target)],check=True)
    return dict(layout=layout,file=str(video),duration=142,frames=4260,fps=30,width=s['width'],height=s['height'],decode_check='passed',audio=False)
if __name__=='__main__':
    assert json.loads((ROOT/'project.json').read_text(encoding='utf-8'))['ending_confirmed']
    with ThreadPoolExecutor(max_workers=2) as pool:report=list(pool.map(verify,['shorts','longform']))
    (ROOT/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Both final exports verified: 142 seconds, 4260 frames, correct dimensions, full decode.')
