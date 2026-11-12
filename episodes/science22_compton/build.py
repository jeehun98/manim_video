"""Render independently replaceable shorts chapters and verify exact user timing."""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))

def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def support():
    sentences=[]; start=0
    for end,s in DATA['sentences']:
        sentences.append({'start':start,'end':end,'text':s}); start=end
    assert start==136 and all(s['end']>s['start'] for s in sentences)
    (HERE/'timing.json').write_text(json.dumps({'duration':136,'fps':30,'source':'user-provided sentence ending times','audio':'not supplied','sentences':sentences,'scenes':DATA['scenes']},ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
    (HERE/'narration.md').write_text('# 콤프턴 효과 · 확정 대본\n\n사용자 제공 대본과 문장 종료 시각, 총 136초.\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
    groups=[]
    for _,a,b,_ in DATA['scenes']:
        groups.append(' '.join(s['text'] for s in sentences if a<=s['start']<b).replace('1923년','천구백이십삼 년').replace('X선','엑스선'))
    (HERE/'tts_script.txt').write_text('\n\n'.join(groups)+'\n',encoding='utf-8')

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True,encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--scene',nargs='+');args=ap.parse_args()
    support()
    quality='preview' if args.preview else 'final'
    media=ROOT/'media'/'science22'/quality;media.mkdir(parents=True,exist_ok=True)
    classes=['Compton'+s[0].title() for s in DATA['scenes']]
    clips=[]; reports=[]
    # Reuse only when every relevant source and render setting matches.
    sources=[HERE/'scene.py',HERE/'script.json',Path(__file__),ROOT/'quantum_series/shared/theme.py',ROOT/'quantum_series/shared/components.py']
    fingerprint=hashlib.sha256(b''.join(p.read_bytes() for p in sources)+quality.encode()).hexdigest()
    for (sid,a,b,title),cls in zip(DATA['scenes'],classes):
        if args.scene and sid not in args.scene:continue
        clip=media/(sid+'.mp4'); cache=media/(sid+'.sha256')
        if not(clip.exists() and cache.exists() and cache.read_text()==fingerprint):
            env=os.environ.copy();env.update(PYTHONUTF8='1',QUANTUM_LAYOUT='shorts',QUANTUM_PREVIEW=str(int(args.preview)))
            print('Rendering '+quality+' / '+sid,flush=True)
            with (media/(sid+'.log')).open('w',encoding='utf-8') as log:
                result=subprocess.run([sys.executable,'-m','manim','render',str(HERE/'scene.py'),cls,'--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:raise RuntimeError((media/(sid+'.log')).read_text(encoding='utf-8',errors='replace')[-5000:])
            rendered=max((media/'videos').rglob(cls+'.mp4'),key=lambda p:p.stat().st_mtime)
            import shutil
            shutil.copy2(rendered,clip);cache.write_text(fingerprint)
        info=probe(clip);v=next(s for s in info['streams'] if s['codec_type']=='video')
        assert int(v['nb_frames'])==(b-a)*30,(sid,v['nb_frames'])
        clips.append(clip); reports.append({'scene':sid,'frames':int(v['nb_frames']),'duration':b-a})
    if args.scene:return
    manifest=media/'concat.txt';manifest.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in clips),encoding='utf-8')
    output=ROOT/'exports'/('science22_compton'+('_preview' if args.preview else '')+'.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy','-movflags','+faststart',str(output)],check=True)
    info=probe(output);v=next(s for s in info['streams'] if s['codec_type']=='video')
    assert int(v['nb_frames'])==4080 and v['r_frame_rate']=='30/1'
    assert (v['width'],v['height'])==((360,640) if args.preview else (1080,1920))
    assert abs(float(info['format']['duration'])-136)<.001
    assert not any(s['codec_type']=='audio' for s in info['streams'])
    (HERE/('render_report_'+quality+'.json')).write_text(json.dumps({'output':str(output),'duration':136,'frames':4080,'width':v['width'],'height':v['height'],'audio':'not supplied; silent','text_bounds':'checked at animation endpoints','scenes':reports},ensure_ascii=False,indent=2),encoding='utf-8')
    print(output,flush=True)

if __name__=='__main__':main()
