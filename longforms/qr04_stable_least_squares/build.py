"""Render validated clocks; never estimate the unconfirmed ending."""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
WORK=next(p for p in ROOT.parents if (p/'scripts/render.py').exists())

def run(args,env=None):subprocess.run(args,env=env,cwd=WORK,check=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['shorts','longform','both'],default='both');p.add_argument('--scene');p.add_argument('--jobs',type=int,default=2);p.add_argument('--concat-only',action='store_true');p.add_argument('--render-only',action='store_true');p.add_argument('--resume',action='store_true');a=p.parse_args()
    project=json.loads((ROOT/'project.json').read_text(encoding='utf-8'));duration=project['duration']
    if not project['ending_confirmed'] and not (a.preview or a.render_only or a.scene):
        raise SystemExit('Actual end times of the last two sentences are required before final concatenation.')
    fps=15 if a.preview else 30
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    report=[]
    for layout in (['shorts','longform'] if a.layout=='both' else [a.layout]):
        suffix=layout+('_preview' if a.preview else '_final')
        res=('360,640' if layout=='shorts' else '640,360') if a.preview else ('1080,1920' if layout=='shorts' else '1920,1080')
        env=os.environ.copy();env['BATTLE_LAYOUT']=layout
        files=[ROOT/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
        def render(pair):
            m,target=pair
            if a.concat_only or (a.scene and a.scene!=m['id']):return
            if a.resume and target.exists():
                try:
                    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(target)]))['streams'][0]
                    if int(info['nb_frames'])==m['duration_seconds']*fps and info['r_frame_rate']==f'{fps}/1':
                        print('REUSE',suffix,m['id'],flush=True);return
                except (subprocess.CalledProcessError,KeyError,ValueError):pass
            media=WORK/'media'/f'qr04_stable_least_squares_{suffix}'/m['id']
            run([sys.executable,'-m','manim','--resolution',res,'--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--media_dir',str(media),str(ROOT/m['directory']/'scene.py'),m['class']],env)
            source=next(media.rglob(m['class']+'.mp4'))
            raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(source)]))['streams'][0]
            assert abs(int(raw['nb_frames'])-m['duration_seconds']*fps)<=1,(m,raw)
            # Correct at most one frame of floating-point wait rounding.
            run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-an','-vf',f'tpad=stop_mode=clone:stop_duration={1/fps},fps={fps}','-frames:v',str(m['duration_seconds']*fps),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(target)])
            print('RENDERED',suffix,m['id'],flush=True)
        with ThreadPoolExecutor(max_workers=max(1,a.jobs)) as pool:
            list(pool.map(render,zip(manifest,files)))
        if a.scene or a.render_only:continue
        concat=ROOT/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+f.as_posix()+"'" for f in files),encoding='utf-8')
        edition=f'{duration}s' if project['ending_confirmed'] else f'0_{duration}s_working'
        out=WORK/'exports'/f'qr04_stable_least_squares_{edition}_{suffix}.mp4';out.parent.mkdir(exist_ok=True)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)])
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,duration,nb_read_frames,r_frame_rate','-of','json',str(out)]))['streams'][0]
        assert int(info['nb_read_frames'])==duration*fps,info
        assert abs(float(info['duration'])-duration)<.001,info
        shutil.copy2(ROOT/'captions.srt',out.with_suffix('.srt'))
        report.append(dict(layout=layout,output=str(out),**info));print('COMPLETE',out,info,flush=True)
    (ROOT/(('preview' if a.preview else 'render')+'_report_'+a.layout+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
