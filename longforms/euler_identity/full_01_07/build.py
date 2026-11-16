"""Pair the user's numbered video/audio files, then join the seven voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['도입','0과 1 — 수학의 기준점','π — 원과 각도','i — 허수와 회전','e — 연속적인 변화','지수함수가 회전이 되는 순간','다섯 숫자가 하나로 연결되는 순간']
FPS=60

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    video=EXPORT/f'euler_identity_{i}.mp4';audio=EXPORT/f'euler_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'euler_identity_{i}_voiced.mp4'
    # Distinct names preserve all user-owned originals, including euler_1.mp4.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p60-crf18-veryfast-aac192k48k-hold-last-v1').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'euler_identity_{i}_voiced.building.mp4'
        run(['-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
             '-vf',f'fps={FPS},tpad=stop_mode=clone:stop_duration={duration-vd+1:.8f}',
             '-af',f'aresample=48000,apad,atrim=duration={duration:.8f},asetpts=PTS-STARTPTS',
             '-t',f'{duration:.8f}','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4',
             '-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','60000',
             '-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-movflags','+faststart',str(temp)],HERE/f'pair_{i:02}.log')
        temp.replace(out);stamp.write_text(signature)
    data=probe(out);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'60/1')
    assert int(v['nb_frames'])==frames,(i,v['nb_frames'],frames)
    assert abs(float(v['duration'])-duration)<.002
    assert abs(float(a['duration'])-duration)<.025
    assert duration>=ad and duration>=vd
    print(f'PAIRED {i}/7: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i-1],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(1,8)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=오일러 항등식 — 전체 롱폼'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/60000',f'START={offset*1000}',f"END={(offset+c['frames'])*1000}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'euler_identity_full_01_07_longform.mp4';temp=EXPORT/'euler_identity_full_01_07_longform.building.mp4'
    # Copy the normalized picture; re-encode the joined audio once to handle AAC
    # packet padding at chapter boundaries with a continuous output timeline.
    run(['-y','-f','concat','-safe','0','-i',str(concat),'-i',str(metadata),
         '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','copy','-c:a','aac','-b:a','192k','-af','aresample=async=1:first_pts=0',
         '-t',f'{offset/FPS:.8f}','-movflags','+faststart',str(temp)],HERE/'concat.log')
    temp.replace(final)
    data=probe(final);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert int(v['nb_frames'])==offset
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'60/1')
    assert abs(float(v['duration'])-offset/FPS)<.002
    assert abs(float(a['duration'])-offset/FPS)<.05
    # A full decode verifies both streams and all seven splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p60; concat all seven')
    (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'COMPLETE {final}\nDURATION {offset/FPS:.3f}s; {offset} frames; audio/video decode passed',flush=True)

if __name__=='__main__':main()
