"""Render independent Manim shots and assemble two exact 160-second editions."""
import argparse,json,os,subprocess,sys,shutil,textwrap
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent;WORK=P.parents[1]
def run(cmd,env=None,cwd=WORK):subprocess.run([str(x) for x in cmd],cwd=cwd,env=env,check=True)
def probe(f):return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,r_frame_rate,duration','-of','json',str(f)]))['streams'][0]
def astamp(t):return f'{int(t)//3600}:{int(t)//60%60:02}:{int(t)%60:02}.{round(t%1*100):02}'
def ass(layout):
    short=layout=='shorts';w,h=(360,640) if short else (640,360)
    header=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Malgun Gothic,{15 if short else 14},&H00F8F8F8,&H00FFFFFF,&H00211409,&H00211409,0,0,0,0,100,100,0,0,3,3,0,2,{15 if short else 28},{15 if short else 28},{26 if short else 14},1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
    for cue in cues:
        # Use word-aware wrapping with Korean character width, not font-dependent auto-wrap.
        rows=textwrap.wrap(cue['caption'],width=30 if short else 58,break_long_words=True)
        caption=(r'{\fs13}' if short and len(rows)>3 else '')+r'\N'.join(rows)
        header+=f'Dialogue: 0,{astamp(cue["start"])},{astamp(cue["end"])},Default,,0,0,0,,{caption}\n'
    (P/f'captions_{layout}.ass').write_text(header,encoding='utf-8')
def main():
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['both','shorts','longform'],default='both');p.add_argument('--scene');p.add_argument('--jobs',type=int,default=2);p.add_argument('--resume',action='store_true');p.add_argument('--concat-only',action='store_true');a=p.parse_args()
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 30
    selected=set(a.scene.split(',')) if a.scene else None
    report=[]
    for layout in (['shorts','longform'] if a.layout=='both' else [a.layout]):
        suffix=layout+('_preview' if a.preview else '_final');dims=((360,640) if layout=='shorts' else (640,360)) if a.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
        env=os.environ.copy();env['GPUH_LAYOUT']=layout
        files=[P/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
        def render(pair):
            m,target=pair
            if a.concat_only or (selected and m['id'] not in selected):return
            if a.resume and target.exists():
                info=probe(target)
                if int(info.get('nb_frames',0))==m['duration_seconds']*fps and (int(info['width']),int(info['height']))==dims:
                    print('REUSE',suffix,m['id'],flush=True);return
            media=WORK/'media'/f'gpuh07_{suffix}'/m['id']
            run([sys.executable,'-m','manim','--renderer','cairo','--resolution',f'{dims[0]},{dims[1]}','--fps',fps,'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',media,P/m['directory']/'scene.py',m['class']],env)
            src=next(media.rglob(m['class']+'.mp4'));info=probe(src)
            expected=m['duration_seconds']*fps
            if abs(int(info['nb_frames'])-expected)>1:raise RuntimeError((m,info))
            run(['ffmpeg','-v','error','-y','-i',src,'-an','-vf',f'tpad=stop_mode=clone:stop_duration={1/fps},fps={fps}','-frames:v',expected,'-c:v','libx264','-preset','fast','-crf',18,'-pix_fmt','yuv420p',target])
            print('RENDERED',suffix,m['id'],flush=True)
        with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,files)))
        if a.scene:continue
        concat=P/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+f.as_posix()+"'" for f in files),encoding='utf-8')
        raw=WORK/'media'/f'gpuh07_{suffix}_raw.mp4'
        run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-c','copy',raw])
        ass(layout);out=WORK/'exports'/f'gpuh07_shared_memory_160s_{suffix}.mp4';out.parent.mkdir(exist_ok=True)
        # Reserve a clean subtitle strip in the landscape edition.
        vf=('drawbox=x=0:y=ih*0.86:w=iw:h=ih*0.14:color=0x0B1220:t=fill,' if layout=='longform' else '')+f'ass=captions_{layout}.ass'
        run(['ffmpeg','-v','error','-y','-i',raw,'-an','-vf',vf,'-c:v','libx264','-preset','fast','-crf',18,'-pix_fmt','yuv420p','-movflags','+faststart',out],cwd=P)
        shutil.copy2(P/'captions.srt',out.with_suffix('.srt'))
        info=probe(out);assert int(info['nb_frames'])==160*fps,info;assert abs(float(info['duration'])-160)<.001,info
        report.append(dict(output=str(out),layout=layout,audio='none; no narration audio supplied',**info));print('COMPLETE',out,info,flush=True)
    (P/f'{"preview" if a.preview else "render"}_report_{a.layout}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()





