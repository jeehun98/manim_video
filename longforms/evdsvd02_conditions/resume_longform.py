"""Resume missing/invalid final landscape scenes, then concatenate and verify."""
import json, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))

def complete(m):
    target=ROOT/m['directory']/'visual_longform_final.mp4'
    if target.exists():
        try:
            s=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,r_frame_rate','-of','json',str(target)]))['streams'][0]
            if s['width']==1920 and s['height']==1080 and s['r_frame_rate']=='30/1' and int(s['nb_frames'])==m['duration_seconds']*30:
                print('REUSE',m['id'],flush=True)
                return
        except (ValueError,KeyError,subprocess.CalledProcessError):
            pass
    subprocess.run([sys.executable,str(ROOT/'build.py'),'--layout','longform','--scene',m['id']],check=True)

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(complete,manifest))
    subprocess.run([sys.executable,str(ROOT/'build.py'),'--layout','longform','--concat-only'],check=True)
