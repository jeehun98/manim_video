"""Pair the user's numbered video/audio files, then join the five voiced chapters."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXPORT=ROOT/'exports'
TITLES=['열의 이동에서 푸리에 해석으로','복잡한 함수와 푸리에 해석','매끄러움·최댓값 원리·하르나크 부등식','브라운 운동·파인만–카츠·블랙–숄즈','열핵·지표정리·리치 흐름']
FPS=30

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def pair(i):
    durations={1:169,2:324,3:255,4:357,5:284}
    video=EXPORT/('heat_ch01_169s_longform_guided.mp4' if i==1 else f'heat_ch{i:02}_{durations[i]}s_longform_final.mp4');audio=EXPORT/f'열방정식_{i}.mp3'
    assert video.is_file() and audio.is_file(),(video,audio)
    vp=probe(video);ap=probe(audio)
    vs=next(s for s in vp['streams'] if s['codec_type']=='video')
    vd=float(vs['duration']);ad=float(ap['format']['duration'])
    frames=math.ceil(max(vd,ad)*FPS-1e-8);duration=frames/FPS
    out=EXPORT/f'heat_ch{i:02}_voiced.mp4'
    # Distinct names preserve all user-owned originals, and all silent source videos.
    signature=hashlib.sha256(video.read_bytes()+audio.read_bytes()+b'1080p30-crf18-veryfast-aac192k48k-hold-last-v2').hexdigest()
    stamp=HERE/f'{i:02}.sha256'
    if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
        temp=EXPORT/f'heat_ch{i:02}_voiced.building.mp4'
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
    print(f'PAIRED {i}/5: {duration:.3f}s, final-frame hold {duration-vd:.3f}s',flush=True)
    return dict(number=i,title=TITLES[i-1],video=str(video),audio=str(audio),output=str(out),source_video_duration=vd,source_audio_duration=ad,duration=duration,frames=frames,hold_seconds=duration-vd)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        chapters=list(pool.map(pair,range(1,6)))
    concat=HERE/'concat.txt';concat.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\nduration "+format(c['duration'],'.12f')+"\n" for c in chapters),encoding='utf-8')
    meta=[';FFMETADATA1','title=열방정식 — 열의 이동에서 수학의 거대한 연결고리로'];offset=0
    for c in chapters:
        c['start_seconds']=offset/FPS
        meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f"END={offset+c['frames']}",f"title={c['number']:02} · {c['title']}"]
        offset+=c['frames']
    metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
    final=EXPORT/'heat_full_01_05_longform.mp4';temp=EXPORT/'heat_full_01_05_longform.building.mp4'
    # Copy the normalized picture; re-encode the joined audio once to handle AAC
    # packet padding at chapter boundaries with a continuous output timeline.
    run(['-y','-f','concat','-safe','0','-i',str(concat),'-i',str(metadata),
         '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1',
         # The concat demuxer exposes one 1024-sample AAC priming block before
         # the first chapter. Remove that block, then keep a continuous clock.
         '-c:v','copy','-c:a','aac','-b:a','192k','-af','aresample=async=1:first_pts=0,atrim=start_sample=1024,asetpts=PTS-STARTPTS,apad',
         '-t',f'{offset/FPS:.8f}','-movflags','+faststart',str(temp)],HERE/'concat.log')
    temp.replace(final)
    data=probe(final);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert int(v['nb_frames'])==offset
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert abs(float(v['duration'])-offset/FPS)<.002
    assert abs(float(a['duration'])-offset/FPS)<.05
    # A full decode verifies both streams and all five splice points.
    run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
    assert not (HERE/'decode_check.log').read_text().strip()
    report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,decode_check_passed=True,method='pair numbered originals; clone last frame for full voice; 1080p30; concat all five')
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
    description='열방정식 — 열의 이동에서 수학의 거대한 연결고리로\n\n뜨거운 물체가 식어가는 현상을 설명하는 열방정식은 어떻게 푸리에 해석, 확률론, 금융수학, 기하학과 위상수학으로 이어졌을까요?\n\n열의 보존과 푸리에의 열전도 법칙에서 출발해, 복잡한 온도 분포를 진동 성분으로 분해하는 방법을 살펴봅니다. 이어 열방정식의 해가 따르는 규칙, 브라운 운동과 기댓값을 이용한 해의 표현, 휘어진 공간의 열핵과 리치 흐름까지 하나씩 연결합니다.\n\n구간 안내\n' + '\n'.join(yt(c['start_seconds'])+' '+str(c['number'])+'장 · '+c['title'] for c in chapters) + '\n\n이 영상에서 다루는 내용\n• 에너지 보존과 푸리에의 열전도 법칙\n• 푸리에 급수: 직교성·고유함수·선형성\n• 열방정식의 매끄러움, 최댓값 원리, 하르나크 부등식\n• 브라운 운동, 파인만–카츠 공식, 블랙–숄즈 방정식\n• 라플라스–벨트라미 작용소와 열핵\n• 아티야–싱어 지표정리의 열 작용소 접근\n• 리치 흐름과 푸앵카레 추측\n\n서로 다른 현상이 모두 하나의 열방정식으로 설명되는 것은 아닙니다. 영상에서는 고정된 공간 위의 온도 확산과 공간의 계량 자체가 변하는 리치 흐름을 구별하며, 여러 문제에서 공통된 수학적 구조가 어떻게 나타나는지 살펴봅니다.\n\n#열방정식 #푸리에해석 #푸리에급수 #브라운운동 #파인만카츠 #블랙숄즈 #열핵 #리치흐름 #수학\n'
    desc=HERE/'youtube_description.txt';desc.write_text(description,encoding='utf-8')
    shutil.copyfile(desc,EXPORT/'heat_youtube_description.txt')
    print('CAPTIONS',captions,'cues',len(cues),flush=True)
    print('DESCRIPTION',EXPORT/'heat_youtube_description.txt',flush=True)

if __name__=='__main__':main()
