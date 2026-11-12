"""Join the six explicitly requested voiced exports without re-encoding video."""
import json,subprocess
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[1]
TITLES=['레지스터에 없는 데이터는 어떻게 계산할까?','명령어 실행 순서를 제어하는 FSM','명령어의 실행 단계를 겹치는 파이프라인','데이터 의존성 — Stall과 Forwarding','계산 회로를 늘리는 다중 실행 유닛','3부 마무리 — 하나의 명령어에서 병렬 실행까지']
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def stamp(t):
 t=int(float(t)+.5);return f'{t//60:02}:{t%60:02}'
def main():
 files=[W/'exports'/f'gpui_long_{i}.mp4' for i in range(11,17)];items=[];start=Fraction(0)
 for i,p in enumerate(files):
  d=probe(p);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
  assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1920,1080,'30/1','h264')
  duration=int(v['duration_ts'])*Fraction(v['time_base'])
  items.append(dict(file=str(p),title=TITLES[i],start_seconds=float(start),duration_seconds=float(duration),video_frames=int(v['nb_frames']),audio_duration_seconds=float(a['duration'])))
  start+=duration
 (R/'manifest.json').write_text(json.dumps(dict(duration_seconds=float(start),episodes=items),ensure_ascii=False,indent=2),encoding='utf-8')
 concat=R/'concat.txt';concat.write_text('\n'.join("file '"+p.as_posix()+"'\nduration "+f'{m["duration_seconds"]:.9f}' for p,m in zip(files,items))+'\n',encoding='utf-8')
 metadata=[';FFMETADATA1','title=GPU 개론 3부 — 하나의 명령어에서 병렬 실행까지']
 for m in items:
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(m["start_seconds"]*1000)}',f'END={round((m["start_seconds"]+m["duration_seconds"])*1000)}','title='+m['title']])
 meta=R/'chapters.ffmetadata';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
 description='GPU 개론 3부에서는 기본 프로세서에 데이터 메모리, 실행 순서 제어, 파이프라인, 데이터 의존성 제어, 다중 실행 유닛을 차례로 추가합니다.\n\n각 구조가 왜 필요한지 살펴보며, 하나의 명령어를 실행하던 회로가 여러 명령어를 겹쳐 처리하고 독립적인 계산을 동시에 수행하는 과정까지 연결합니다. 마지막에는 의존성과 데이터 공급이 만드는 병렬 실행의 한계를 짚습니다.\n\n챕터\n'+'\n'.join(stamp(m['start_seconds'])+' '+m['title'] for m in items)+'\n'
 (R/'youtube_description.txt').write_text(description,encoding='utf-8')
 out=W/'exports'/'gpui_11_16_long.mp4'
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat)]
 for p in files:args+=['-i',str(p)]
 args+=['-f','ffmetadata','-i',str(meta)]
 filters=[]
 for i,m in enumerate(items,1):filters.append(f'[{i}:a:0]apad,atrim=duration={m["duration_seconds"]:.9f},asetpts=PTS-STARTPTS[a{i}]')
 filters.append(''.join(f'[a{i}]' for i in range(1,7))+'concat=n=6:v=0:a=1[audio]')
 args+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[audio]','-map_metadata','7','-map_chapters','7','-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{float(start):.9f}','-movflags','+faststart',str(out)]
 subprocess.run(args,check=True)
 final=probe(out);v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
 assert int(v['nb_frames'])==sum(m['video_frames'] for m in items)
 assert abs(float(v['duration'])-float(start))<.002
 assert abs(float(a['duration'])-float(start))<.05
 chapters=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(out)]))['chapters'];assert len(chapters)==6
 (R/'verification.json').write_text(json.dumps(dict(output=str(out),video_frames=v['nb_frames'],video_duration=v['duration'],audio_duration=a['duration'],resolution=[v['width'],v['height']],fps=v['r_frame_rate'],chapters=chapters,video_encoding='stream copy',audio='AAC; per-episode silence padding preserves video boundaries'),ensure_ascii=False,indent=2),encoding='utf-8')
 print(out);print(R/'youtube_description.txt')
if __name__=='__main__':main()
