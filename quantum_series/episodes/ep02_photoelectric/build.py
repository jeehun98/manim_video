"""Render responsive chapters, validate frame counts, and assemble exact 101-second outputs."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))

def probe(path):
    result=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                          check=True,capture_output=True,text=True,encoding='utf-8')
    return json.loads(result.stdout)

def timestamp(seconds):
    milliseconds=round(seconds*1000)
    return f'{milliseconds//3600000:02}:{milliseconds//60000%60:02}:{milliseconds//1000%60:02},{milliseconds%1000:03}'

def supporting_files():
    sentences=DATA['sentences']
    assert [s['end'] for s in sentences]==[3,5,9,14,16,19,26,31,34,39,43,48,54,57,62,66,73,79,86,91,97,101]
    assert all(s['start']==(sentences[i-1]['end'] if i else 0) for i,s in enumerate(sentences))
    (HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{timestamp(s['start'])} --> {timestamp(s['end'])}\n{s['text']}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
    (HERE/'timing.json').write_text(json.dumps({'duration':101,'fps':30,'source':DATA['timing_source'],'sentences':sentences},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--layout',choices=['shorts','longform','both'],default='both')
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--ending',choices=['standalone','join','auto'],default='auto')
    parser.add_argument('--scene',choices=[s['id'] for s in DATA['scenes']],help='Rerender one scene, then assemble existing scene clips.')
    args=parser.parse_args()
    supporting_files()
    layouts=['shorts','longform'] if args.layout=='both' else [args.layout]
    report=[]
    for layout in layouts:
        ending=('standalone' if layout=='shorts' else 'join') if args.ending=='auto' else args.ending
        quality='preview' if args.preview else 'final'
        media=ROOT/'media'/'quantum02'/layout/ending/quality
        media.mkdir(parents=True,exist_ok=True)
        clips=[]
        for scene in DATA['scenes']:
            if not args.scene or args.scene==scene['id']:
                env=os.environ.copy()
                env.update(QUANTUM_LAYOUT=layout,QUANTUM_PREVIEW=str(int(args.preview)),QUANTUM_ENDING=ending)
                command=[sys.executable,'-m','manim','render',str(HERE/'scenes'/scene['id']/'scene.py'),scene['class'],
                         '--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching']
                print(f"Rendering {layout} / {scene['id']} / {quality}",flush=True)
                with (media/f"{scene['id']}.log").open('w',encoding='utf-8') as log:
                    process=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
                if process.returncode:
                    print((media/f"{scene['id']}.log").read_text(encoding='utf-8')[-7000:])
                    raise SystemExit(process.returncode)
            candidates=list((media/'videos').rglob(scene['class']+'.mp4'))
            if not candidates:raise RuntimeError(f"Missing {scene['id']}: render all scenes first")
            clip=max(candidates,key=lambda path:path.stat().st_mtime)
            stream=next(s for s in probe(clip)['streams'] if s['codec_type']=='video')
            expected=round((scene['end']-scene['start'])*30)
            if int(stream['nb_frames'])!=expected:
                raise RuntimeError(f"{scene['id']}: expected {expected} frames, got {stream['nb_frames']}")
            clips.append(clip)
        manifest=media/'concat.txt'
        manifest.write_text('\n'.join("file '"+str(path.resolve()).replace('\\','/')+"'" for path in clips)+'\n',encoding='utf-8')
        suffix='_preview' if args.preview else ''
        # Default deliverables have simple filenames; optional modes are explicit.
        if args.ending!='auto':suffix+='_'+ending
        output=ROOT/'exports'/f'quantum02_{layout}{suffix}.mp4'
        output.parent.mkdir(exist_ok=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),
                        '-vf','setpts=N/(30*TB)','-r','30','-fps_mode','cfr','-frames:v','3030',
                        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an',
                        '-movflags','+faststart',str(output)],check=True)
        result=probe(output)
        video=next(s for s in result['streams'] if s['codec_type']=='video')
        width,height=((360,640) if layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        assert (video['width'],video['height'])==(width,height)
        assert int(video['nb_frames'])==3030 and video['r_frame_rate']=='30/1'
        assert abs(float(result['format']['duration'])-101)<.001
        report.append({'layout':layout,'ending':ending,'output':str(output),'duration':101,'frames':3030,
                       'width':width,'height':height,'fps':30,'audio':'not supplied; silent video',
                       'clips':[str(path) for path in clips]})
        print(f'Export: {output}',flush=True)
    (HERE/('render_report_preview.json' if args.preview else 'render_report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
