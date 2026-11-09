"""Render selected shots, reuse only matching inputs, assemble and validate."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True,encoding='utf-8'))

def digest(scene,preview):
    tree=ast.parse((HERE/'scene.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node,ast.ClassDef) and node.name=='TimedShot':
            node.body=[m for m in node.body if not isinstance(m,ast.FunctionDef) or not (m.name.startswith('s') and m.name[1:].isdigit()) or m.name==f's{scene["id"]:02}']
    h=hashlib.sha256(ast.dump(tree).encode())
    for path in [HERE/'timing.json',HERE/'build.py',HERE/'motion.py',*sorted((ROOT/'visual_library/manim').glob('*.py'))]:h.update(path.read_bytes())
    h.update(str(preview).encode());return h.hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--scene',nargs='+',type=int)
    args=parser.parse_args();mode='preview' if args.preview else 'final'
    media=ROOT/'media/euler01'/mode;media.mkdir(parents=True,exist_ok=True)
    wh=(360,640) if args.preview else (1080,1920)
    clips=[];checks=[];seen=set()
    for s in DATA['scenes']:
        if args.scene and s['id'] not in args.scene:continue
        stamp=media/f'{s["id"]:02}.json';hash_value=digest(s,args.preview)
        old=json.loads(stamp.read_text()) if stamp.exists() else {}
        if old.get('sha256')!=hash_value or not Path(old.get('clip','missing')).exists():
            env=os.environ.copy();env.update(VIDEO_WIDTH=str(wh[0]),VIDEO_HEIGHT=str(wh[1]),PYTHONIOENCODING='utf-8',EULER_AUDIT=str(media/'audit'))
            command=[sys.executable,'-m','manim','render',str(HERE/'scene.py'),s['cls'],'--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching']
            print(f'Render {mode} shot {s["id"]:02} ({s["start"]}–{s["end"]}s)',flush=True)
            log_path=media/f'{s["id"]:02}.log'
            with log_path.open('w',encoding='utf-8') as log:result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:print(log_path.read_text(encoding='utf-8')[-5000:]);raise SystemExit(result.returncode)
            clip=max((media/'videos').rglob(s['cls']+'.mp4'),key=lambda p:p.stat().st_mtime)
            video=next(x for x in probe(clip)['streams'] if x['codec_type']=='video')
            expected=(s['end']-s['start'])*60
            if int(video['nb_frames'])!=expected:
                assert abs(int(video['nb_frames'])-expected)<=4,('unexpected frame drift',s['id'],video['nb_frames'])
                corrected=media/f'Shot{s["id"]:02}_cfr.mp4'
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(clip),'-vf','tpad=stop_mode=clone:stop_duration=0.1,setpts=N/(60*TB)',
                    '-frames:v',str(expected),'-r','60','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an',str(corrected)],check=True)
                clip=corrected
            old=dict(sha256=hash_value,clip=str(clip));stamp.write_text(json.dumps(old),encoding='utf-8')
        clip=Path(old['clip']);info=probe(clip);v=next(x for x in info['streams'] if x['codec_type']=='video')
        assert int(v['nb_frames'])==(s['end']-s['start'])*60,(s['id'],v['nb_frames'])
        assert (v['width'],v['height'])==wh and v['r_frame_rate']=='60/1'
        audit=json.loads((media/'audit'/f'{s["id"]:02}.json').read_text())
        for record in audit:
            sentence=DATA['segments'][record['sentence']-1]
            expected=max(s['start'],sentence['start'])
            # The last boundary belongs to the next independently rendered shot.
            if expected>=s['end']:continue
            seen.add(record['sentence'])
            assert abs(record['at']-expected)<=1/60+.0001,(s['id'],record,expected)
        checks.append(dict(scene=s['id'],frames=int(v['nb_frames']),sha256=hash_value));clips.append(clip)
    if args.scene:print('Selected shots verified.');return
    assert seen==set(range(1,len(DATA['segments'])+1)),('missing captions',seen)
    assert all(c['sha256']==digest(s,args.preview) for s,c in zip(DATA['scenes'],checks)), 'Sources changed during rendering'
    manifest=media/'concat.txt';manifest.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in clips)+'\n',encoding='utf-8')
    output=ROOT/'exports'/('euler01_preview.mp4' if args.preview else 'euler01.mp4');output.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-an','-movflags','+faststart',str(output)],check=True)
    info=probe(output);v=next(x for x in info['streams'] if x['codec_type']=='video')
    assert int(v['nb_frames'])==DATA['duration']*60 and abs(float(info['format']['duration'])-DATA['duration'])<.04
    assert (v['width'],v['height'])==wh and v['r_frame_rate']=='60/1'
    assert not any(x['codec_type']=='audio' for x in info['streams'])
    assert all(a['end']==b['start'] for a,b in zip(DATA['segments'],DATA['segments'][1:]))
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    report=dict(output=str(output),duration=DATA['duration'],width=wh[0],height=wh[1],fps=60,frames=DATA['duration']*60,audio='not supplied; silent',sentences=len(DATA['segments']),shots=checks,checks='clip frames, caption boundaries, continuous timing, resolution, FPS, complete video decode')
    (HERE/f'review_{mode}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Export verified: {output}',flush=True)

if __name__=='__main__':main()
