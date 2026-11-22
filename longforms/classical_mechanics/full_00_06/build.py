"""Pair the user's numbered video/audio files, then join the seven voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['고전역학의 발전을 따라가는 지도','예측이 가능해진 물체의 운동','하나의 원리로 설명되는 운동','새로운 공간에 기록된 운동','에너지 함수로 펼쳐지는 운동','변화 속에서도 보존되는 구조','고전역학을 넘어 이어지는 수학']
FPS=30

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    durations=[91,156,180,299,366,317,265]
    video=EXPORT/f'classical_ch{i:02}_{durations[i]}s_longform_final.mp4';audio=EXPORT/f'물리_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'classical_ch{i:02}_voiced.mp4'
    # Distinct names preserve all user-owned originals, and all silent source videos.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p30-crf18-veryfast-aac192k48k-hold-last-v2').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'classical_ch{i:02}_voiced.building.mp4'
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
    print(f'PAIRED {i}/6: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(7)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\nduration "+format(c['duration'],'.12f')+"\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=고전역학은 어떻게 발전해 왔는가? — 뉴턴에서 해밀토니안까지'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f"END={offset+c['frames']}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'classical_full_00_06_longform.mp4';temp=EXPORT/'classical_full_00_06_longform.building.mp4'
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
    # A full decode verifies both streams and all seven splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p30; concat all seven')
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
    description='고전역학은 어떻게 발전해 왔는가? — 뉴턴에서 해밀토니안까지\n\n뉴턴은 이미 물체의 운동을 예측할 수 있는 법칙을 제시했습니다. 그런데 왜 이후에도 라그랑주 역학과 해밀턴 역학이 등장했을까요?\n\n하나의 진자에서 출발해 힘과 초기조건, 에너지와 작용, 위치와 운동량으로 이루어진 위상 공간을 차례로 살펴봅니다. 같은 운동을 새로운 수학적 언어로 표현할 때, 이전에는 쉽게 드러나지 않던 기하학적 구조와 대칭성, 보존량의 관계가 어떻게 나타나는지 알아봅니다.\n\n마지막에는 양자역학에서 상태의 표현 방식이 달라져도 해밀토니안이 시간 진화를 결정하는 역할로 이어진다는 점을 살펴봅니다.\n\n챕터\n' + '\n'.join(yt(c['start_seconds'])+' '+str(c['number'])+'장 · '+c['title'] for c in chapters) + '\n\n이 영상에서 다루는 내용\n• 뉴턴 역학: 힘과 초기조건으로 운동을 예측하는 방법\n• 라그랑주 역학: 라그랑지안과 작용의 정지 조건\n• 르장드르 변환과 위상 공간: 각도와 정준운동량으로 표현한 상태\n• 해밀턴 역학: 해밀토니안이 만드는 시간 진화와 진자의 다양한 운동\n• 심플렉틱 구조: 해밀턴 흐름에서 유지되는 기하학적 관계\n• 대칭성과 보존량: 뇌터 정리와 푸아송 괄호\n• 양자역학과의 연결: 상태, 해밀토니안 연산자, 교환자\n\n고전역학의 세 접근은 같은 운동을 서로 다른 방식으로 기술합니다. 양자역학은 새로운 상태와 측정의 원리를 가진 물리 이론이며, 고전역학의 단순한 좌표 변환을 뜻하지 않습니다.\n\n#고전역학 #뉴턴역학 #라그랑주역학 #해밀턴역학 #해밀토니안 #위상공간 #뇌터정리 #물리학\n'
    desc=HERE/'youtube_description.txt';desc.write_text(description,encoding='utf-8')
    shutil.copyfile(desc,EXPORT/'classical_youtube_description.txt')
    print('CAPTIONS',captions,'cues',len(cues),flush=True)
    print('DESCRIPTION',EXPORT/'classical_youtube_description.txt',flush=True)

if __name__=='__main__':main()
