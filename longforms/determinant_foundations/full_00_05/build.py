"""Pair the user's numbered video/audio files, then join the six voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['행렬식은 왜 등장했을까?','방정식에서 발견한 특별한 숫자','행렬식의 기하학적 의미','계산 규칙 — 순열과 방향','효율적 계산 — 불변성과 가우스 소거법','행렬식이 담고 있는 정보']
FPS=30

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    durations=[71,126,164,168,171,143]
    video=EXPORT/f'determinant_ch{i:02}_{durations[i]}s_longform_final.mp4';audio=EXPORT/f'행렬식_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'determinant_ch{i:02}_voiced.mp4'
    # Distinct names preserve all user-owned originals, and all silent source videos.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p30-crf18-veryfast-aac192k48k-hold-last-v1').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'determinant_ch{i:02}_voiced.building.mp4'
        run(['-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
             '-vf',f'fps={FPS},tpad=stop_mode=clone:stop_duration={duration-vd+1:.8f}',
             '-af',f'aresample=48000,apad,atrim=duration={duration:.8f},asetpts=PTS-STARTPTS',
             '-t',f'{duration:.8f}','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4',
             '-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','60000',
             '-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-movflags','+faststart',str(temp)],HERE/f'pair_{i:02}.log')
        temp.replace(out);stamp.write_text(signature)
    data=probe(out);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==frames,(i,v['nb_frames'],frames)
    assert abs(float(v['duration'])-duration)<.002
    assert abs(float(a['duration'])-duration)<.025
    assert duration>=ad and duration>=vd
    print(f'PAIRED {i}/5: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(6)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=행렬식의 탄생부터 계산 원리까지'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f"END={offset+c['frames']}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'determinant_full_00_05_longform.mp4';temp=EXPORT/'determinant_full_00_05_longform.building.mp4'
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
    # A full decode verifies both streams and all six splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p30; concat all six')
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
    description='행렬식은 왜 등장했고, 어떻게 공간의 부피와 방향을 나타내는 값이 되었을까요?\n\n연립방정식에서 발견한 ad−bc를 출발점으로, 기하학적 의미와 순열을 이용한 계산 공식, 불변성과 가우스 소거법까지 연결합니다. 마지막에는 행렬식이 담는 정보와 그 한계를 살펴봅니다.\n\n챕터\n' + '\n'.join(yt(c['start_seconds'])+' '+str(c['number'])+'장 · '+c['title'] for c in chapters) + '\n\n행렬식의 절댓값은 공간의 부피 배율을, 부호는 방향을 나타냅니다. 순열 항의 개수 n!과 단순 직접 전개의 연산량 O(n·n!)을 구별하며, 가우스 소거법으로 O(n³) 연산에 계산하는 원리를 설명합니다.\n\n역사 참고: MacTutor — Matrices and determinants\nhttps://mathshistory.st-andrews.ac.uk/HistTopics/Matrices_and_determinants/\n\n#행렬식 #선형대수 #가우스소거법 #순열 #수학\n'
    desc=HERE/'youtube_description.txt';desc.write_text(description,encoding='utf-8')
    shutil.copyfile(desc,EXPORT/'determinant_youtube_description.txt')
    print('CAPTIONS',captions,'cues',len(cues),flush=True)
    print('DESCRIPTION',EXPORT/'determinant_youtube_description.txt',flush=True)

if __name__=='__main__':main()
