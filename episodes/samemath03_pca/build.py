"""Render Same Math 03 in native short and long layouts."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--preview',action='store_true')
    p.add_argument('--aspect',choices=('short','long','both'),default='both')
    a=p.parse_args()
    dims={'short':(360,640) if a.preview else (1080,1920),
          'long':(640,360) if a.preview else (1920,1080)}
    targets=dims if a.aspect=='both' else {a.aspect:dims[a.aspect]}
    media=ROOT/'media'/'samemath03'
    exports=ROOT/'exports';exports.mkdir(exist_ok=True)
    for aspect,(width,height) in targets.items():
        scene='SameMath03Short' if aspect=='short' else 'SameMath03Long'
        name=f"samemath03_{aspect}{'_preview' if a.preview else ''}.mp4"
        subprocess.run([sys.executable,'-m','manim','render',str(HERE/'scene.py'),scene,
                        '-r',f'{width},{height}','--fps','30','--disable_caching',
                        '--media_dir',str(media),'-o',name],cwd=ROOT,check=True)
        source=next(media.rglob(name))
        shutil.copy2(source,exports/name)
        print(exports/name)

if __name__=='__main__':main()
