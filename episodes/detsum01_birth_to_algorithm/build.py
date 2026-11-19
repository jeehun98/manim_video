"""Render independent Manim scenes, concatenate, and verify exact timing."""

import argparse, hashlib, json, os, shutil, subprocess, sys

from pathlib import Path

R=Path(__file__).resolve().parent

W=R.parents[1]

def probe(p):

    return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]))

def run(args):subprocess.run(args,cwd=W,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def main():

    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--scene',type=int);a=p.parse_args()

    fps=30;wh=(360,640) if a.preview else (1080,1920)

    kind='preview' if a.preview else 'final';manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))

    media=W/'media'/'detsum01'/kind;media.mkdir(parents=True,exist_ok=True)

    targets=[];reports=[]

    for m in manifest:

        d=R/m['directory'];target=media/f"{m['id']}.mp4";targets.append(target)

        if a.scene and int(m['id'])!=a.scene:continue

        digest=hashlib.sha256(b''.join((R/f).read_bytes() for f in ['visuals.py','scene.py','timing.json','manifest.json','build.py','../../longforms/determinant_foundations/chapter_01/visuals.py','../../longforms/determinant_foundations/chapter_02/visuals.py','../../longforms/determinant_foundations/chapter_03/visuals.py','../../longforms/determinant_foundations/chapter_04/visuals.py'])+(d/'scene.py').read_bytes()+str((fps,wh)).encode()).hexdigest()

        stamp=target.with_suffix('.sha256')

        if not target.exists() or not stamp.exists() or stamp.read_text()!=digest:

            log=media/f"{m['id']}.log"

            with log.open('w',encoding='utf-8') as f:

                result=subprocess.run([sys.executable,'-m','manim','--resolution',f'{wh[0]},{wh[1]}','--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',str(media/m['id']),str(d/'scene.py'),m['class_name']],cwd=W,env={**os.environ,'PYTHONIOENCODING':'utf-8'},stdout=f,stderr=subprocess.STDOUT)

            if result.returncode:raise RuntimeError(log.read_text(encoding='utf-8',errors='replace')[-5000:])

            candidates=list((media/m['id']).rglob(m['class_name']+'.mp4'));assert len(candidates)==1,candidates

            shutil.copyfile(candidates[0],target)

            stamp.write_text(digest)

        info=probe(target)['streams'][0]

        assert int(info['nb_read_frames'])==m['duration_seconds']*fps,(m,info)

        assert (info['width'],info['height'])==wh

        reports.append(dict(scene_id=m['id'],sha256=digest,**info))

        print('VERIFIED',kind,m['id'],flush=True)

    if a.scene:return

    concat=media/'concat.txt';concat.write_text('\n'.join("file '"+t.as_posix()+"'" for t in targets),encoding='utf-8')

    out=W/'exports'/f'detsum01_177s_short_{kind}.mp4';out.parent.mkdir(exist_ok=True)

    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf',f'setpts=N/({fps}*TB)','-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','18','-movflags','+faststart',str(out)])

    data=probe(out);video=data['streams'][0]

    assert len(data['streams'])==1,'Expected silent video'

    assert int(video['nb_read_frames'])==177*fps

    assert abs(float(video['duration'])-177)<.001

    timing=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']

    assert timing[0]['start']==0 and timing[-1]['end']==177

    assert all(x['end']==y['start'] for x,y in zip(timing,timing[1:]))

    assert all(x['start']<x['end'] for x in timing)

    for m in manifest:

        audit=json.loads((R/m['directory']/'layout_audit.json').read_text(encoding='utf-8'))

        assert audit and all(x['left']>=-3.9 and x['right']<=3.9 and x['bottom']>-6.25 and x['top']<-4.45 for x in audit)

    (R/f'verification_{kind}.json').write_text(json.dumps(dict(output=str(out),silent=True,sentence_end_times=[x['end'] for x in timing],video=video,scenes=reports),ensure_ascii=False,indent=2),encoding='utf-8')

    shutil.copyfile(R/'captions.srt',out.with_name(out.stem+'_captions.srt'))

    print('COMPLETE',out,flush=True)

if __name__=='__main__':main()

