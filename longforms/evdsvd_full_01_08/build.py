"""Join the user's named narrated files, preserving video and exact frame-based chapter offsets."""
import json,subprocess
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;WORK=ROOT.parents[1];EXPORT=WORK/'exports'
TITLES=['이름','분해 조건','분해 구조','고윳값과 특이값','미래 예측','복원 정확도','역변환','최종 선택']
OUT=EXPORT/'evdsvd_long_1-8_full.mp4'
def run(args):subprocess.run(args,check=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def clock(sec):
    sec=int(sec);return f'{sec//60:02}:{sec%60:02}'
def main():
    ROOT.mkdir(exist_ok=True);(ROOT/'qa').mkdir(exist_ok=True)
    paths=[EXPORT/f'evdsvd_long_{i}.mp4' for i in range(1,9)];chapters=[];frames=0
    for i,p in enumerate(paths):
        info=probe(p);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],v['pix_fmt'],v['time_base'])==(1920,1080,'30/1','h264','yuv420p','1/15360')
        n=int(v['nb_frames']);duration=Fraction(n,30)
        chapters.append(dict(episode=i+1,title=TITLES[i],source=str(p),start_frame=frames,end_frame=frames+n,start_seconds=frames/30,duration_seconds=float(duration),source_video_frames=n,source_audio_seconds=float(a['duration'])))
        frames+=n
    duration=Fraction(frames,30)
    (ROOT/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf-8')
    # Explicit video durations prevent shorter audio tracks moving the following episode's boundary.
    playlist=ROOT/'concat.txt'
    playlist.write_text(''.join(f"file '{p.as_posix()}'\nduration {m['duration_seconds']:.9f}\n" for p,m in zip(paths,chapters)),encoding='utf-8')
    video=ROOT/'video_only.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(playlist),'-map','0:v:0','-c:v','copy','-an',str(video)])
    metadata=ROOT/'chapters.ffmetadata'
    # TIMEBASE 1/30 preserves each exact frame offset in the MP4 chapter table.
    metadata.write_text(';FFMETADATA1\ntitle=행렬 분해 이상형 월드컵 — EVD vs SVD 전체 1~8편\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/30\nSTART={m["start_frame"]}\nEND={m["end_frame"]}\ntitle={m["episode"]:02} · {m["title"]}\n' for m in chapters),encoding='utf-8')
    filters=[]
    for i,m in enumerate(chapters):
        samples=m['source_video_frames']*1600
        filters.append(f'[{i+1}:a:0]aresample=48000,apad=whole_len={samples},atrim=end_sample={samples},asetpts=PTS-STARTPTS[a{i}]')
    filters.append(''.join(f'[a{i}]' for i in range(8))+'concat=n=8:v=0:a=1[audio]')
    filter_file=ROOT/'audio_filter.txt';filter_file.write_text(';\n'.join(filters),encoding='utf-8')
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video)]
    for p in paths:args+=['-i',str(p)]
    args+=['-f','ffmetadata','-i',str(metadata),'-filter_complex',filter_file.read_text(encoding='utf-8'),'-map','0:v:0','-map','[audio]','-map_metadata','9','-map_chapters','9','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(OUT)]
    run(args)
    chapter_text='\n'.join(f'{clock(m["start_seconds"])} {m["episode"]:02}. {m["title"]}' for m in chapters)
    description='''EVD와 SVD, 어떤 행렬 분해를 선택해야 할까요?

「행렬 분해 이상형 월드컵」 1~8편을 한 영상으로 모았습니다.
고유값 분해(EVD)와 특이값 분해(SVD)를 이름, 분해 조건, 구조, 숫자의 의미, 미래 예측, 복원 정확도, 역변환이라는 기준으로 비교합니다.

같은 행렬도 어떤 질문을 던지느냐에 따라 다른 정보가 드러납니다.
고유방향과 반복 변환을 알고 싶다면 EVD를, 입력·출력 방향과 길이 변화, 저랭크 근사와 의사역행렬을 살펴보고 싶다면 SVD를 떠올려 보세요.

⏱️ 챕터
'''+chapter_text+'''

📌 수학적 조건
• 영상에서 EVD는 A = PDP⁻¹ 형태의 대각화를 뜻하며, 선택한 수 체계에서 고유기저가 존재해야 합니다.
• SVD의 특이값은 항상 0 이상이며, 회전과 방향 반전은 좌·우 특이벡터의 관계로 표현합니다.
• 절단 SVD의 최적 저랭크 근사는 같은 랭크 이하에서 Frobenius 노름 또는 스펙트럴 노름 기준으로 성립합니다.
• 의사역행렬은 사라진 정보를 되살리는 대신, 최소제곱 해 중 최소 노름 해를 선택합니다.

월드컵의 승패는 선정한 비교 기준에 따른 결과입니다. 어떤 분해가 필요한지는 우리가 알고 싶은 행렬의 성질에 달려 있습니다.

#선형대수 #행렬분해 #EVD #SVD #고유값분해 #특이값분해 #수학시각화
'''
    desc=EXPORT/'evdsvd_long_1-8_youtube_description.txt';desc.write_text(description,encoding='utf-8')
    (EXPORT/'evdsvd_long_1-8_chapters.txt').write_text(chapter_text+'\n',encoding='utf-8')
    # Validate both streams over the complete output, not only the container metadata.
    final=probe(OUT);v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
    assert int(v['nb_frames'])==frames and abs(float(v['duration'])-float(duration))<1/30
    assert abs(float(a['duration'])-float(duration))<.05
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(OUT),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    cc=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(OUT)]))['chapters'];assert len(cc)==8
    for m,c in zip(chapters,cc):assert abs(float(c['start_time'])-m['start_seconds'])<.002
    # Inspect the beginning of every episode, including all seven joins.
    for m in chapters:
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(m['start_seconds']+.5),'-i',str(OUT),'-vf','scale=640:360','-frames:v','1',str(ROOT/'qa'/f'episode_{m["episode"]:02}.png')])
    report=dict(output=str(OUT),duration_seconds=float(duration),frames=frames,resolution=[1920,1080],fps=30,audio='AAC 48kHz mono; source narration retained, tails padded with silence',chapters=8,full_decode='passed',video_reencoded=False,description=str(desc))
    (ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True);print(chapter_text,flush=True)
if __name__=='__main__':main()
