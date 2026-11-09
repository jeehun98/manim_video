"""Render independent shots, reject stale clips, concatenate, verify exact frame counts."""
import argparse
import ast
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
FPS=60

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True,encoding='utf-8'))

def source_hash(scene,layout,preview,ending):
    h=hashlib.sha256()
    # Hash only this shot and its dependencies so unrelated shot edits do not invalidate clips.
    tree=ast.parse((HERE/'direction.py').read_text(encoding='utf-8'))
    number=int(scene['id'])
    for node in tree.body:
        if isinstance(node,ast.ClassDef):
            node.body=[m for m in node.body if not isinstance(m,ast.FunctionDef)
                or (m.name==f's{number:02}' or not (m.name.startswith('s') and m.name[1:].isdigit()))
]
        h.update(ast.dump(node,include_attributes=False).encode())
    for path in [HERE/'visuals.py',HERE/'probability_model.py',HERE/'script.json',HERE/'scenes'/scene['id']/'scene.py',ROOT/'longforms/qcs01_speed/direction.py',ROOT/'longforms/qcs01_speed/layouts.py',ROOT/'quantum_series/shared/theme.py',ROOT/'quantum_series/shared/components.py']:
        h.update(path.read_bytes())
    h.update(json.dumps([layout,preview,ending,FPS]).encode())
    return h.hexdigest()

def render(args):
    media=ROOT/'media/expression01_v2_168s'/args.layout/args.ending/('preview' if args.preview else 'final')
    media.mkdir(parents=True,exist_ok=True)
    clips=[]; checks=[]
    for s in DATA['scenes']:
        stamp=media/(s['id']+'.json')
        digest=source_hash(s,args.layout,args.preview,args.ending)
        existing=json.loads(stamp.read_text()) if stamp.exists() else {}
        matched=existing.get('sha256')==digest and Path(existing.get('clip','missing')).exists()
        selected=not args.scene or s['id'] in args.scene
        if selected and not matched:
            env=os.environ.copy();env.update(PYTHONIOENCODING='utf-8',QCS_LAYOUT=args.layout,QCS_PREVIEW=str(int(args.preview)),
                                            QCS_ENDING=args.ending,QCS_AUDIT_DIR=str(media/'caption_audit'))
            cmd=[sys.executable,'-m','manim','render',str(HERE/'scenes'/s['id']/'scene.py'),s['class'],
                 '--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching']
            print('Render',args.layout,s['id'],flush=True)
            with (media/(s['id']+'.log')).open('w',encoding='utf-8') as log:
                result=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:
                print((media/(s['id']+'.log')).read_text(encoding='utf-8')[-5000:]);raise SystemExit(result.returncode)
            clip=max((media/'videos').rglob(s['class']+'.mp4'),key=lambda p:p.stat().st_mtime)
            stamp.write_text(json.dumps({'sha256':digest,'clip':str(clip)}),encoding='utf-8')
            matched=True;existing={'clip':str(clip)}
        if not matched:
            if args.scene:continue
            raise RuntimeError('Missing matching clip '+s['id'])
        clip=Path(existing['clip']);v=next(x for x in probe(clip)['streams'] if x['codec_type']=='video')
        expected=round((s['end']-s['start'])*FPS)
        assert int(v['nb_frames'])==expected,(s['id'],v['nb_frames'],expected)
        assert v['r_frame_rate']=='60/1'
        clips.append(clip);checks.append({'scene':s['id'],'frames':expected,'source_sha256':digest})
    if len(clips)!=len(DATA['scenes']):
        print('Selected previews ready; remaining shots are required for assembly.');return
    for s,c in zip(DATA['scenes'],checks):
        assert c['source_sha256']==source_hash(s,args.layout,args.preview,args.ending),'Source changed during build; rerun to refresh affected shots'
    manifest=media/'concat.txt'
    manifest.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in clips)+'\n',encoding='utf-8')
    suffix=('_preview' if args.preview else '')+('_join' if args.ending=='join' else '')
    name='short' if args.layout=='shorts' else 'long'
    output=ROOT/'exports'/f'expression01_{name}{suffix}.mp4'
    output.parent.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),
                    '-c','copy','-an','-movflags','+faststart',str(output)],check=True)
    result=probe(output);v=next(x for x in result['streams'] if x['codec_type']=='video')
    wh=((360,640) if args.layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if args.layout=='shorts' else (1920,1080))
    assert (v['width'],v['height'])==wh
    assert int(v['nb_frames'])==DATA['duration']*FPS and v['r_frame_rate']=='60/1'
    assert abs(float(result['format']['duration'])-DATA['duration'])<.02,result['format']['duration']
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    seen=set()
    for scene in DATA['scenes']:
        records=json.loads((media/'caption_audit'/(scene['id']+'.json')).read_text())
        for record in records:
            sentence=DATA['sentences'][record['sentence']-1]
            expected=max(scene['start'],sentence['start'])
            assert -.00001<=record['at']-expected<=1/FPS+.00001,record
            seen.add(record['sentence'])
    assert seen==set(range(1,len(DATA['sentences'])+1)),seen
    versioned=None
    if not args.preview:
        versioned=output.with_name(f'expression01_{name}_{DATA["revision"]}{suffix}.mp4')
        versioned=None
    report={'output':str(output),'revision':DATA['revision'],'duration':DATA['duration'],'frames':DATA['duration']*FPS,'fps':60,'width':wh[0],'height':wh[1],
            'versioned_output':str(versioned) if versioned else None,
            'audio':'not supplied; silent','subtitles':f"{len(DATA['sentences'])} full narration sentences burned in; exact supplied boundaries",
            'subtitle_audit':f"all {len(DATA['sentences'])} sentences within one frame; safe band assertions passed",
            'ending':args.ending,'shots':checks,'full_decode':'passed'}
    (HERE/('render_report_'+name+('_preview' if args.preview else '')+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Verified:',output,flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--preview',action='store_true')
    ap.add_argument('--layout',choices=['shorts','longform','both'],default='both')
    ap.add_argument('--ending',choices=['standalone','join'],default='standalone')
    ap.add_argument('--scene',nargs='+',help='Render selected scenes and assemble if all matching clips exist')
    args=ap.parse_args()
    layouts=['longform','shorts'] if args.layout=='both' else [args.layout]
    for layout in layouts:
        args.layout=layout;render(args)

if __name__=='__main__':main()
