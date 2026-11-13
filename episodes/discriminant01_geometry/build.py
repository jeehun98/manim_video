"""Prepare assets, render independent scenes, then assemble the 175 s short."""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))


def prepare():
    timing=[];captions=[];narration=[f"# {DATA['title']}",'','사용자 제공 문장 종료 시각 · 175초','']
    previous=0
    def stamp(t):
        return f'{t//3600:02}:{t//60%60:02}:{t%60:02},000'
    for i,(end,line) in enumerate(DATA['sentences'],1):
        assert end>previous
        timing.append({'start':previous,'end':end,'text':line})
        captions.append(f'{i}\n{stamp(previous)} --> {stamp(end)}\n{line}\n')
        narration.append(f'- {previous:03}–{end:03}초: {line}')
        previous=end
    assert previous==DATA['duration']==175
    assert DATA['scenes'][0][2]==0 and DATA['scenes'][-1][3]==175
    assert all(a[3]==b[2] for a,b in zip(DATA['scenes'],DATA['scenes'][1:]))
    groups=[' '.join(line for end,line in DATA['sentences'] if start<end<=stop)
            for _,_,start,stop,_ in DATA['scenes']]
    (HERE/'timing.json').write_text(json.dumps({'duration':175,'timing_source':DATA['timing_source'],
                                               'sentences':timing,'scenes':DATA['scenes']},
                                              ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (HERE/'captions.srt').write_text('\n'.join(captions),encoding='utf-8-sig')
    (HERE/'narration.md').write_text('\n'.join(narration)+'\n',encoding='utf-8')
    (HERE/'tts_script.txt').write_text('\n\n'.join(groups)+'\n',encoding='utf-8')


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=width,height,nb_frames,avg_frame_rate','-show_entries',
        'format=duration','-of','json',str(path)],text=True))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--only',help='Comma-separated scene IDs, e.g. 05,07')
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    prepare()
    if args.prepare_only:
        return
    width,height,fps=(360,640,15) if args.preview else (1080,1920,30)
    media=ROOT/'media'/'discriminant01'/('preview' if args.preview else 'final')
    media.mkdir(parents=True,exist_ok=True)
    manifest_path=media/'manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    source=(HERE/'scene.py').read_text(encoding='utf-8')
    lines=source.splitlines(keepends=True)
    nodes=[n for n in ast.parse(source).body if isinstance(n,ast.ClassDef)]
    classes={n.name:''.join(lines[n.lineno-1:n.end_lineno]) for n in nodes}
    shared=source[:source.index('class DG01Intro')]
    ui=(ROOT/'episodes/lhopital01_relative_change/scene.py').read_text(encoding='utf-8')
    shared+=ui[:ui.index('class LH01Intro')]
    world=(ROOT/'episodes/newton01_local_linear/scene.py').read_text(encoding='utf-8')
    shared+=world[:world.index('class NW01Intro')]
    selection=set(args.only.split(',')) if args.only else {s[0] for s in DATA['scenes']}
    unknown=selection-{s[0] for s in DATA['scenes']}
    if unknown:
        raise ValueError(f'Unknown scenes: {sorted(unknown)}')
    pending=[];hashes={};paths={}
    for sid,name,start,end,claim in DATA['scenes']:
        output=media/'videos'/'scene'/f'{height}p{fps}'/f'{name}.mp4'
        paths[sid]=output
        rows=[r for r in DATA['sentences'] if start<r[0]<=end]
        payload=shared+classes[name]+json.dumps([rows,start,end,width,height,fps])
        digest=hashlib.sha256(payload.encode()).hexdigest()
        hashes[sid]=digest
        if sid in selection and (manifest.get(sid)!=digest or not output.exists()):
            pending.append(name)
    if pending:
        env=os.environ.copy()
        env.update(VIDEO_WIDTH=str(width),VIDEO_HEIGHT=str(height),VIDEO_FPS=str(fps))
        command=[sys.executable,'-m','manim','render',str(HERE/'scene.py'),*pending,
                 '--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none']
        subprocess.run(command,cwd=ROOT,env=env,check=True)
    for sid,name,start,end,claim in DATA['scenes']:
        if sid not in selection:
            continue
        info=probe(paths[sid]);stream=info['streams'][0]
        expected=round((end-start)*fps)
        if int(stream.get('nb_frames',-1))!=expected:
            raise RuntimeError(f'{name}: expected {expected} frames, got {stream}')
        if (stream['width'],stream['height'])!=(width,height):
            raise RuntimeError(f'{name}: wrong resolution')
        manifest[sid]=hashes[sid]
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    if args.only:
        print('Verified independent scenes:',','.join(sorted(selection)))
        return
    concat=media/'concat.txt'
    concat.write_text(''.join("file '"+p.as_posix()+"'\n" for p in paths.values()),encoding='utf-8')
    exports=ROOT/'exports';exports.mkdir(exist_ok=True)
    output=exports/f"discriminant01_short{'_preview' if args.preview else ''}.mp4"
    temp=output.with_name(output.stem+'_cfr.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0',
                    '-i',str(concat),'-vf',f'setpts=N/({fps}*TB)','-r',str(fps),'-fps_mode','cfr',
                    '-frames:v',str(175*fps),'-c:v','libx264','-preset','fast','-crf','18',
                    '-pix_fmt','yuv420p','-an','-movflags','+faststart',str(temp)],check=True)
    info=probe(temp);stream=info['streams'][0]
    assert int(stream['nb_frames'])==175*fps
    assert abs(float(info['format']['duration'])-175)<1e-6
    temp.replace(output)
    print(output)


if __name__=='__main__':
    main()
