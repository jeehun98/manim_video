"""Join the five explicitly requested voiced exports without re-encoding video."""
import json,subprocess
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[1]
TITLES=['논리 게이트는 어떻게 값을 기억할까?','회로는 언제 값을 갱신할까?','저장된 값은 어떻게 다시 계산에 사용될까?','명령어는 어떻게 회로를 제어할까?','컴퓨터는 어떻게 프로그램을 실행할까?']
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def stamp(t):
 t=int(float(t)+.5);return f'{t//60:02}:{t%60:02}'
def main():
 files=[W/'exports'/f'gpui_{i}_long.mp4' for i in range(6,11)];items=[];start=Fraction(0)
 for i,p in enumerate(files):
  d=probe(p);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
  assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1920,1080,'30/1','h264')
  duration=int(v['duration_ts'])*Fraction(v['time_base'])
  items.append(dict(file=str(p),title=TITLES[i],start_seconds=float(start),duration_seconds=float(duration),video_frames=int(v['nb_frames']),audio_duration_seconds=float(a['duration'])))
  start+=duration
 (R/'manifest.json').write_text(json.dumps(dict(duration_seconds=float(start),episodes=items),ensure_ascii=False,indent=2),encoding='utf-8')
 concat=R/'concat.txt';concat.write_text('\n'.join("file '"+p.as_posix()+"'" for p in files)+'\n',encoding='utf-8')
 metadata=[';FFMETADATA1','title=GPU 개론 2부 — 기억하는 회로에서 프로그램 실행까지']
 for m in items:
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(m["start_seconds"]*1000)}',f'END={round((m["start_seconds"]+m["duration_seconds"])*1000)}','title='+m['title']])
 meta=R/'chapters.ffmetadata';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
 description='GPU 개론 6~10편을 모아, 값을 기억하는 회로에서 프로그램을 실행하는 기본 프로세서 구조까지 살펴봅니다.\n\nSR 래치와 클럭, 레지스터와 데이터 경로, 명령어 해독, 프로그램 카운터와 분기를 차례로 연결합니다.\n\n챕터\n'+'\n'.join(stamp(m['start_seconds'])+' '+m['title'] for m in items)+'\n'
 (R/'youtube_description.txt').write_text(description,encoding='utf-8')
 out=W/'exports'/'gpui_6_10_long.mp4'
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
