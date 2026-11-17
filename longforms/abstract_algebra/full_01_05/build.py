"""Pair the user's numbered video/audio files, then join the five voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['숫자에서 연산 구조로','군 — 대칭과 하나의 연산','환 — 두 연산과 분배법칙','체 — 곱셈 역원과 유한체','군·환·체의 관계와 추상대수학']
FPS=60

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    durations=[81,155,118,128,75]
    video=EXPORT/f'abstract_algebra_ch{i:02}_{durations[i-1]}s_longform_final.mp4';audio=EXPORT/f'군체환_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'abstract_algebra_ch{i:02}_voiced.mp4'
    # Distinct names preserve all user-owned originals, and all silent source videos.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p60-crf18-veryfast-aac192k48k-hold-last-v1').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'abstract_algebra_ch{i:02}_voiced.building.mp4'
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
    print(f'PAIRED {i}/5: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i-1],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(1,6)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=추상대수학 입문 — 군·환·체'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/60000',f'START={offset*1000}',f"END={(offset+c['frames'])*1000}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'abstract_algebra_full_01_05_longform.mp4';temp=EXPORT/'abstract_algebra_full_01_05_longform.building.mp4'
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
    # A full decode verifies both streams and all five splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p60; concat all five')
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
    description='''군, 환, 체는 무엇이고, 왜 숫자뿐 아니라 도형의 대칭과 다항식에서도 등장할까요?

이 영상은 세부 공리를 모두 외우기보다, 각 개념의 대표적인 예시와 핵심 차이를 떠올릴 수 있도록 구성한 추상대수학 입문입니다.

정사각형의 회전에서 군의 규칙을 발견하고, 정수와 다항식에서 환을, 유리수와 다섯 원소의 나머지 계산에서 체를 살펴봅니다. 마지막에는 같은 집합도 어떤 연산을 선택하느냐에 따라 서로 다른 구조로 연구할 수 있다는 관점으로 연결합니다.

챕터
'''+ '\n'.join(yt(c['start_seconds'])+' '+c['title'] for c in chapters)+'''

영상에서 다루는 내용
• 군(Group): 하나의 연산에서 닫힘·항등원·역원·결합법칙이 성립하는 구조
• 환(Ring): 덧셈의 아벨 군과 결합적인 곱셈이 분배법칙으로 연결된 구조
• 체(Field): 0이 아닌 모든 원소에 곱셈 역원이 있는 가환환
• 유한체 F₅: 덧셈과 곱셈의 결과를 5로 나눈 나머지로 계산하는 다섯 원소의 세계
• 정사각형의 네 회전과 mod 4 덧셈에서 발견하는 연산 구조의 일치

모든 체는 환이지만 모든 환이 체인 것은 아닙니다. 환의 덧셈은 아벨 군을 이룹니다.

서로 다른 대상, 공통된 수학적 구조.
집합과 연산의 규칙을 바라보는 추상대수학의 관점을 함께 살펴봅니다.

#추상대수학 #군환체 #수학 #군론 #유한체
'''
    desc=HERE/'youtube_description.txt';desc.write_text(description,encoding='utf-8')
    shutil.copyfile(desc,EXPORT/'abstract_algebra_youtube_description.txt')
    print('CAPTIONS',captions,'cues',len(cues),flush=True)
    print('DESCRIPTION',EXPORT/'abstract_algebra_youtube_description.txt',flush=True)

if __name__=='__main__':main()
