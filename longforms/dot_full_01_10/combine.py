"""Join the user's voiced dot_long1..10 exports and derive exact chapters."""
import json,subprocess,sys
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
OUT=ROOT/'exports/dot_full_01_10_longform.mp4'
TITLES=['내적과 방향 성분의 측정','정사영: 원하는 방향의 성분 추출','직교와 잔차: 방향 성분 제거','직교정규기저와 좌표 표현','그람–슈미트 직교화와 QR 분해','최소제곱법: 가장 가까운 해','PCA: 정보를 보존하는 방향','SVD: 행렬의 방향별 작용','Attention: 정보의 비교와 결합','기울기와 경사하강법 · 시리즈 마무리']
def probe(f):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(f)]))
def stamp(t):
    seconds=int(t);return f'{seconds//60:02}:{seconds%60:02}'
def main():
    inputs=[ROOT/'exports'/f'dot_long{i}.mp4' for i in range(1,11)];data=[probe(f) for f in inputs]
    signatures=[[tuple(s.get(k) for k in ['codec_type','codec_name','width','height','pix_fmt','r_frame_rate','time_base','sample_rate','channels']) for s in p['streams']] for p in data]
    assert all(x==signatures[0] for x in signatures),'Stream formats differ'
    assert [s['codec_type'] for s in data[0]['streams']]==['video','audio']
    chapters=[];frames=0;meta=[';FFMETADATA1','title=내적 하나로 어디까지 이해할 수 있을까? — LEVEL 01–10']
    concat=[]
    for index,(f,p,title) in enumerate(zip(inputs,data,TITLES),1):
        v=next(s for s in p['streams'] if s['codec_type']=='video');n=int(v['nb_frames']);assert v['r_frame_rate']=='30/1'
        assert (v['width'],v['height'])==(1920,1080)
        start=Fraction(frames,30);end=Fraction(frames+n,30);duration=Fraction(n,30)
        assert abs(float(p['format']['duration'])-float(duration))<.001
        concat.append("file '"+f.as_posix()+"'\nduration "+f'{float(duration):.9f}')
        chapter_title=f'{index:02} {title}'
        meta+=['[CHAPTER]','TIMEBASE=1/30000',f'START={frames*1000}',f'END={(frames+n)*1000}',f'title={chapter_title}']
        chapters.append(dict(episode=index,source=str(f.relative_to(ROOT)),title=title,start_seconds=float(start),duration_seconds=float(duration),start_frame=frames,frames=n,youtube_time=stamp(start)))
        frames+=n
    (P/'concat.txt').write_text('\n'.join(concat)+'\n',encoding='utf-8');(P/'chapters.ffmetadata').write_text('\n'.join(meta)+'\n',encoding='utf-8')
    lines=[f'{c["youtube_time"]} {c["episode"]:02} {c["title"]}' for c in chapters]
    text='내적 하나로 어디까지 이해할 수 있을까?\n방향 성분의 측정에서 정사영, 직교기저, 최소제곱, PCA, SVD, Attention, 경사하강법까지 연결하는 LEVEL 01–10 통합 영상입니다.\n\n타임라인\n'+'\n'.join(lines)+'\n'
    (P/'youtube_description.txt').write_text(text,encoding='utf-8');(ROOT/'exports/dot_full_01_10_youtube_description.txt').write_text(text,encoding='utf-8')
    if '--verify-only' not in sys.argv:
        with (P/'concat.log').open('w',encoding='utf-8') as log:
            subprocess.run(['ffmpeg','-hide_banner','-n','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-i',str(P/'chapters.ffmetadata'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(OUT)],stdout=log,stderr=log,check=True)
    final=probe(OUT);v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
    assert int(v['nb_frames'])==frames and len(final['chapters'])==10
    assert abs(float(v['duration'])-float(Fraction(frames,30)))<.04
    assert abs(float(final['format']['duration'])-float(Fraction(frames,30)))<.1
    assert a['codec_name']=='aac'
    for expected,actual in zip(chapters,final['chapters']):assert abs(expected['start_seconds']-float(actual['start_time']))<.04
    with (P/'decode.log').open('w',encoding='utf-8') as log:
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(OUT),'-f','null','-'],stdout=log,stderr=log,check=True)
    report=dict(output=str(OUT),method='video and audio stream copy; source tails preserved',width=v['width'],height=v['height'],fps=v['r_frame_rate'],frames=frames,video_duration_seconds=float(v['duration']),container_duration_seconds=float(final['format']['duration']),audio_codec=a['codec_name'],audio_duration_seconds=float(a['duration']),full_decode='passed',chapters=chapters,youtube_chapter_rounding='floor to preceding whole second',bytes=OUT.stat().st_size)
    (P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
