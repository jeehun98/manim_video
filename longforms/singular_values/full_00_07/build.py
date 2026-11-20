"""Pair the user's numbered video/audio files, then join the eight voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['고윳값만으로는 알 수 없는 것','방향이 아닌 길이의 변화','단위 원에서 발견하는 특잇값','새로운 행렬의 등장','정보의 보존과 소실','행렬식과 공간의 부피','작은 오차가 커지는 이유 — 조건수','하나의 행렬에서 발견할 수 있는 다양한 정보']
FPS=30

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    durations=[63,100,121,180,137,151,156,90]
    video=EXPORT/f'singular{i:02}_{durations[i]}s_1080p30.mp4';audio=EXPORT/f'sig_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'singular_ch{i:02}_voiced.mp4'
    # Distinct names preserve all user-owned originals, and all silent source videos.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p30-crf18-veryfast-aac192k48k-hold-last-v2').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'singular_ch{i:02}_voiced.building.mp4'
        run(['-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
             '-vf',f'fps={FPS},tpad=stop_mode=clone:stop_duration={duration-vd+1:.8f}',
             '-af',f'aresample=48000,apad,atrim=duration={duration:.8f},asetpts=PTS-STARTPTS',
             '-t',f'{duration:.8f}','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4',
             '-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','60000','-x264-params','keyint=30:min-keyint=30:scenecut=0',
             '-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-movflags','+faststart',str(temp)],HERE/f'pair_{i:02}.log')
        temp.replace(out);stamp.write_text(signature)
    data=probe(out);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==frames,(i,v['nb_frames'],frames)
    assert abs(float(v['duration'])-duration)<.002
    assert abs(float(a['duration'])-duration)<.025
    assert duration>=ad and duration>=vd
    print(f'PAIRED {i}/7: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(8)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\nduration "+format(c['duration'],'.12f')+"\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=특잇값은 왜 중요할까? — 길이 변화에서 랭크와 조건수까지'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f"END={offset+c['frames']}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'singular_full_00_07_longform.mp4';temp=EXPORT/'singular_full_00_07_longform.building.mp4'
    # Copy the normalized picture; re-encode the joined audio once to handle AAC
    # packet padding at chapter boundaries with a continuous output timeline.
    run(['-y','-f','concat','-safe','0','-i',str(concat),'-i',str(metadata),
         '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','copy','-c:a','aac','-b:a','192k','-af','aresample=async=1:first_pts=0',
         '-t',f'{offset/FPS:.8f}','-movflags','+faststart',str(temp)],HERE/'concat.log')
    temp.replace(final)
    data=probe(final);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert int(v['nb_frames'])==offset
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert abs(float(v['duration'])-offset/FPS)<.002
    assert abs(float(a['duration'])-offset/FPS)<.05
    # A full decode verifies both streams and all eight splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p30; concat all eight')
    (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    write_delivery(chapters,final,offset/FPS)
    print(f'COMPLETE {final}\nDURATION {offset/FPS:.3f}s; {offset} frames; audio/video decode passed',flush=True)

def timecode(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def seconds(s):
    h,m,sec=s.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(sec)
def write_delivery(chapters,final,total):
    import shutil
    cues=[]
    for c in chapters:
        source=HERE.parent/f"chapter_{c['number']:02}"/'captions.srt'
        blocks=source.read_text(encoding='utf-8').strip().split('\n\n')
        for k,block in enumerate(blocks):
            rows=block.splitlines();start,end=rows[1].split(' --> ')
            a,b=seconds(start),seconds(end)
            if k==len(blocks)-1:b=c['duration']
            cues.append((c['start_seconds']+a,c['start_seconds']+b,'\n'.join(rows[2:])))
    assert all(a<b for a,b,_ in cues)
    assert all(abs(a[1]-b[0])<.001 for a,b in zip(cues,cues[1:]))
    assert abs(cues[-1][1]-total)<.001
    captions=final.with_name(final.stem+'_captions.srt')
    captions.write_text('\n\n'.join(f'{k}\n{timecode(a)} --> {timecode(b)}\n{s}' for k,(a,b,s) in enumerate(cues,1))+'\n',encoding='utf-8')
    def yt(t):
        n=int(t);return f'{n//60:02}:{n%60:02}'
    description='두 행렬의 고윳값이 같아도, 공간을 변화시키는 방식은 다를 수 있습니다. 그렇다면 모든 방향에서 벡터의 길이가 얼마나 늘어나고 줄어드는지는 어떻게 알 수 있을까요?\n\n단위 원이 타원으로 변하는 모습에서 출발해 특잇값의 기하학적 의미와 계산 원리를 살펴봅니다. 이어서 같은 특잇값들을 관찰하고, 세고, 곱하고, 나누며 랭크·행렬식·조건수가 어떻게 연결되는지 알아봅니다.\n\n챕터\n' + '\n'.join(yt(c['start_seconds'])+' '+str(c['number'])+'장 · '+c['title'] for c in chapters) + '\n\n이 영상에서 다루는 내용\n• 단위 원과 타원의 반축으로 이해하는 특잇값\n• AᵀA의 고윳값과 특잇값의 관계\n• 양의 특잇값 개수로 보는 랭크와 정보 소실\n• 특잇값의 곱과 정사각행렬의 부피 변화 배율 |det A|\n• 최대·최소 특잇값의 비율로 보는 조건수와 상대 오차 민감도\n\n조건수는 실제 오차가 항상 커지는 배율이 아니라, 고정된 가역행렬에서 상대 오차가 얼마나 증폭될 수 있는지를 분석하는 지표입니다.\n\n#특잇값 #선형대수 #행렬 #고윳값 #랭크 #행렬식 #조건수\n'
    desc=HERE/'youtube_description.txt';desc.write_text(description,encoding='utf-8')
    shutil.copyfile(desc,EXPORT/'singular_youtube_description.txt')
    print('CAPTIONS',captions,'cues',len(cues),flush=True)
    print('DESCRIPTION',EXPORT/'singular_youtube_description.txt',flush=True)

if __name__=='__main__':main()
