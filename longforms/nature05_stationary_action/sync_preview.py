"""Refresh reviewed previews from final clips without changing playback speed."""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent
def main():
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    jobs=[(m,layout) for layout in ['shorts','longform'] for m in manifest]
    def one(pair):
        m,layout=pair;d=P/m['directory'];w,h=(360,640) if layout=='shorts' else (640,360)
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(d/f'visual_{layout}_final.mp4'),'-an','-vf',f'scale={w}:{h},fps=15','-frames:v',str(15*m['duration_seconds']),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(d/f'visual_{layout}_preview.mp4')],check=True)
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,jobs))
if __name__=='__main__':main()
