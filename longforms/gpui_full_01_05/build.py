"""Join the five explicitly requested voiced exports without re-encoding video."""
import json,subprocess
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[1]
TITLES=['컴퓨터는 왜 0과 1을 사용할까?','트랜지스터는 어떻게 전기 신호를 제어할까?','스위치의 연결이 어떻게 논리 연산이 될까?','논리 게이트는 어떻게 숫자를 더할까?','하나의 회로로 여러 연산을 수행하는 방법']
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def stamp(t):
 t=int(float(t)+.5);return f'{t//60:02}:{t%60:02}'
def main():
 files=[W/'exports'/f'gpui_{i}_long.mp4' for i in range(1,6)];items=[];start=Fraction(0)
 for i,p in enumerate(files):
  d=probe(p);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
  assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1920,1080,'30/1','h264')
  duration=int(v['duration_ts'])*Fraction(v['time_base'])
  items.append(dict(file=str(p),title=TITLES[i],start_seconds=float(start),duration_seconds=float(duration),video_frames=int(v['nb_frames']),audio_duration_seconds=float(a['duration'])))
  start+=duration
 (R/'manifest.json').write_text(json.dumps(dict(duration_seconds=float(start),episodes=items),ensure_ascii=False,indent=2),encoding='utf-8')
 concat=R/'concat.txt';concat.write_text('\n'.join("file '"+p.as_posix()+"'" for p in files)+'\n',encoding='utf-8')
 metadata=[';FFMETADATA1','title=GPU 개론 — 전기 신호에서 ALU까지']
 for m in items:
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(m["start_seconds"]*1000)}',f'END={round((m["start_seconds"]+m["duration_seconds"])*1000)}','title='+m['title']])
 meta=R/'chapters.ffmetadata';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
 description='''전기 신호가 어떻게 정보가 되고, 논리 연산과 숫자 계산을 거쳐 하나의 연산 장치로 이어질까요?

GPU 개론 1~5편을 모아, 전압과 이진 표현에서 트랜지스터·논리 게이트·가산기·ALU까지 연결해 살펴봅니다. 각 구조의 동작 원리와 함께, 왜 그런 구조가 필요한지 따라갑니다.

📌 챕터
'''+ '\n'.join(stamp(m['start_seconds'])+' '+m['title'] for m in items)+'''

1. 전압과 잡음: 구분하기 쉬운 두 상태를 조합해 정보를 표현하는 이유
2. 트랜지스터: 전기 신호로 전류 경로를 제어하고 인버터를 만드는 원리
3. 논리 게이트: 스위치의 연결이 AND·OR·NAND 같은 규칙이 되는 과정
4. 덧셈 회로: 반가산기·전가산기와 올림수 의존성, 캐리 룩어헤드
5. ALU: 2의 보수로 가산기를 재사용하고 MUX로 필요한 결과를 선택하는 구조

이 영상은 GPU 아키텍처를 이해하기 위한 컴퓨터 구조 기초를 다룹니다.

#GPU개론 #컴퓨터구조 #논리회로 #트랜지스터 #ALU
'''
 (R/'youtube_description.txt').write_text(description,encoding='utf-8')
 out=W/'exports'/'gpui_1_5_long.mp4'
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat)]
 for p in files:args+=['-i',str(p)]
 args+=['-f','ffmetadata','-i',str(meta)]
 filters=[]
 for i,m in enumerate(items,1):filters.append(f'[{i}:a:0]apad,atrim=duration={m["duration_seconds"]:.9f},asetpts=PTS-STARTPTS[a{i}]')
 filters.append(''.join(f'[a{i}]' for i in range(1,6))+'concat=n=5:v=0:a=1[audio]')
 args+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[audio]','-map_metadata','6','-map_chapters','6','-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{float(start):.9f}','-movflags','+faststart',str(out)]
 subprocess.run(args,check=True)
 final=probe(out);v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
 assert int(v['nb_frames'])==sum(m['video_frames'] for m in items)
 assert abs(float(v['duration'])-float(start))<.002
 assert abs(float(a['duration'])-float(start))<.05
 chapters=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(out)]))['chapters'];assert len(chapters)==5
 (R/'verification.json').write_text(json.dumps(dict(output=str(out),video_frames=v['nb_frames'],video_duration=v['duration'],audio_duration=a['duration'],resolution=[v['width'],v['height']],fps=v['r_frame_rate'],chapters=chapters,video_encoding='stream copy',audio='AAC; per-episode silence padding preserves video boundaries'),ensure_ascii=False,indent=2),encoding='utf-8')
 print(out);print(R/'youtube_description.txt')
if __name__=='__main__':main()
