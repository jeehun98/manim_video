"""Build review clips from the verified final renders, then join with the preview clock."""
import json,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent
manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
def down(m):
 p=R/m['directory']
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'visual_1080p30.mp4'),'-vf','scale=854:480,fps=15','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(p/'visual_preview.mp4')],check=True)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(down,manifest))
subprocess.run([sys.executable,str(R/'build.py'),'--preview','--concat-only'],check=True)
