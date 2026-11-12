"""Reusable dual-layout scene renderer, exact-frame assembly and compact QA."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys



def probe(path):
    result=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                          check=True,capture_output=True,text=True,encoding='utf-8')
    return json.loads(result.stdout)

def timestamp(seconds):
    milliseconds=round(seconds*1000)
    return f'{milliseconds//3600000:02}:{milliseconds//60000%60:02}:{milliseconds//1000%60:02},{milliseconds%1000:03}'

def supporting_files():
    sentences=DATA['sentences']
    assert sentences[-1]['end']==DATA['duration']
    assert all(s['start']==(sentences[i-1]['end'] if i else 0) for i,s in enumerate(sentences))
    (HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{timestamp(s['start'])} --> {timestamp(s['end'])}\n{s['text']}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
    (HERE/'timing.json').write_text(json.dumps({'duration':DATA['duration'],'fps':30,'source':DATA['timing_source'],'sentences':sentences},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main(here):
    global HERE,ROOT,DATA
    HERE=Path(here).resolve();ROOT=HERE.parents[2]
    DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
    parser=argparse.ArgumentParser()
    parser.add_argument('--layout',choices=['shorts','longform','both'],default='both')
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--stills',action='store_true',help='Save representative final frame of each independent scene; no video assembly.')
    parser.add_argument('--inspect',action='store_true',help='Decode outputs and create a compact review sheet.')
    parser.add_argument('--ending',choices=['standalone','join','auto'],default='auto')
    parser.add_argument('--scene',choices=[s['id'] for s in DATA['scenes']],help='Rerender one scene, then assemble existing scene clips.')
    args=parser.parse_args()
    supporting_files()
    layouts=['shorts','longform'] if args.layout=='both' else [args.layout]
    report=[]
    for layout in layouts:
        ending=('standalone' if layout=='shorts' else 'join') if args.ending=='auto' else args.ending
        quality='stills' if args.stills else ('preview' if args.preview else 'final')
        media=ROOT/'media'/DATA['id']/layout/ending/quality
        media.mkdir(parents=True,exist_ok=True)
        clips=[]
        for scene in DATA['scenes']:
            if not args.scene or args.scene==scene['id']:
                env=os.environ.copy()
                env.update(PYTHONIOENCODING='utf-8',QUANTUM_LAYOUT=layout,QUANTUM_PREVIEW=str(int(args.preview)),QUANTUM_ENDING=ending)
                command=[sys.executable,'-m','manim','render',str(HERE/'scenes'/scene['id']/'scene.py'),scene['class'],
                         '--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching']
                if args.stills:command.append('-s')
                print(f"Rendering {layout} / {scene['id']} / {quality}",flush=True)
                with (media/f"{scene['id']}.log").open('w',encoding='utf-8') as log:
                    process=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
                if process.returncode:
                    print((media/f"{scene['id']}.log").read_text(encoding='utf-8',errors='replace')[-7000:])
                    raise SystemExit(process.returncode)
            if args.stills:continue
            candidates=list((media/'videos').rglob(scene['class']+'.mp4'))
            if not candidates:raise RuntimeError(f"Missing {scene['id']}: render all scenes first")
            clip=max(candidates,key=lambda path:path.stat().st_mtime)
            stream=next(s for s in probe(clip)['streams'] if s['codec_type']=='video')
            expected=round((scene['end']-scene['start'])*30)
            if int(stream['nb_frames'])!=expected:
                raise RuntimeError(f"{scene['id']}: expected {expected} frames, got {stream['nb_frames']}")
            clips.append(clip)
        if args.stills:continue
        manifest=media/'concat.txt'
        manifest.write_text('\n'.join("file '"+str(path.resolve()).replace('\\','/')+"'" for path in clips)+'\n',encoding='utf-8')
        suffix='_preview' if args.preview else ''
        # Default deliverables have simple filenames; optional modes are explicit.
        if args.ending!='auto':suffix+='_'+ending
        output=ROOT/'exports'/f"{DATA['id']}_{layout}{suffix}.mp4"
        output.parent.mkdir(exist_ok=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),
                        '-vf','setpts=N/(30*TB)','-r','30','-fps_mode','cfr','-frames:v',str(round(DATA['duration']*30)),
                        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an',
                        '-movflags','+faststart',str(output)],check=True)
        result=probe(output)
        video=next(s for s in result['streams'] if s['codec_type']=='video')
        width,height=((360,640) if layout=='shorts' else (640,360)) if args.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        assert (video['width'],video['height'])==(width,height)
        assert int(video['nb_frames'])==round(DATA['duration']*30) and video['r_frame_rate']=='30/1'
        assert abs(float(result['format']['duration'])-DATA['duration'])<.001
        report.append({'layout':layout,'ending':ending,'output':str(output),'duration':DATA['duration'],'frames':round(DATA['duration']*30),
                       'width':width,'height':height,'fps':30,'audio':'not supplied; silent video',
                       'clips':[str(path) for path in clips]})
        if not args.preview:
            still=output.with_name(output.stem+'_ending.png')
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-sseof','-0.05','-i',str(output),'-frames:v','1',str(still)],check=True)
        print(f'Export: {output}',flush=True)
    if args.stills:
        still_sheet(HERE,ROOT,DATA,layouts);return
    if args.inspect:inspect_outputs(HERE,ROOT,DATA,report,args.preview)
    (HERE/('render_report_preview.json' if args.preview else 'render_report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')




def contact_sheet(paths,output,thumb=(240,240),cols=6):
    from PIL import Image,ImageDraw
    tiles=[]
    for path,label in paths:
        im=Image.open(path).convert('RGB');im.thumbnail(thumb)
        tile=Image.new('RGB',(thumb[0],thumb[1]+22),'#111827');tile.paste(im,((thumb[0]-im.width)//2,22+(thumb[1]-im.height)//2));ImageDraw.Draw(tile).text((5,4),label,fill='white');tiles.append(tile)
    if not tiles:raise RuntimeError('No review frames')
    w,h=tiles[0].size;sheet=Image.new('RGB',(cols*w,((len(tiles)+cols-1)//cols)*h),'#212735')
    for i,tile in enumerate(tiles):sheet.paste(tile,((i%cols)*w,(i//cols)*h))
    output.parent.mkdir(parents=True,exist_ok=True);sheet.save(output)

def still_sheet(here,root,data,layouts):
    frames=[]
    for layout in layouts:
        ending='standalone' if layout=='shorts' else 'join'
        media=root/'media'/data['id']/layout/ending/'stills'
        for scene in data['scenes']:
            candidates=list((media/'images').rglob(scene['class']+'*.png'))
            if not candidates:raise RuntimeError(f"Missing still {scene['id']}")
            frames.append((max(candidates,key=lambda p:p.stat().st_mtime),f"{layout} {scene['id']}"))
    output=root/'media'/data['id']/'qa'/'representatives.png'
    contact_sheet(frames,output,thumb=(300,360),cols=6)
    print(f'Representative sheet: {output}',flush=True)

def inspect_outputs(here,root,data,reports,preview):
    qa=root/'media'/data['id']/'qa'/('preview' if preview else 'final');qa.mkdir(parents=True,exist_ok=True)
    frames=[]
    for report in reports:
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',report['output'],'-f','null','-'],check=True)
        report['full_decode']='passed'
        for t in data.get('qa_times',[]):
            frame=qa/f"{report['layout']}_{t:03}.png"
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',report['output'],'-frames:v','1',str(frame)],check=True)
            frames.append((frame,f"{report['layout']} {t}s"))
    contact_sheet(frames,qa/'contact.png',thumb=(240,280),cols=8)
    (qa/'verification.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Decoded all outputs; review sheet: {qa/'contact.png'}",flush=True)
