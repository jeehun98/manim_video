import json,subprocess,sys
from fractions import Fraction
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'exports/gpuh_full_01_11_longform.mp4'
TITLES=['Thread — GPU의 개별 실행 문맥','Warp — 32개 Thread와 SIMT','Block — Thread의 협력과 동기화','SM — Warp 실행과 대기 시간 숨기기','Grid — 전체 작업과 Block 배치','Register — 계산값과 레지스터 자원','Shared Memory — 데이터 공유와 재사용','Global Memory — 주소 패턴과 Coalescing','L1 & L2 Cache — 메모리 공간과 데이터 공급 경로','Memory Controller & DRAM — 실제 저장 장치의 동작','최종 통합 — 하나의 CUDA 커널로 연결되는 GPU']
DETAILS=['인덱스와 실행 상태를 가진 Thread가 각자의 데이터를 계산하는 과정을 살펴봅니다.','32개 Thread의 명령 실행, Lane, SIMT와 Warp Divergence를 설명합니다.','같은 Block의 Thread들이 Shared Memory와 동기화를 이용해 협력하는 과정을 다룹니다.','SM의 실행 자원, Warp Scheduler, Latency Hiding과 Occupancy의 관계를 살펴봅니다.','Grid와 Block의 논리적 구성, 전체 인덱스 계산과 실제 SM 배치를 구분합니다.','SM의 Register File이 Thread에 할당되는 방식과 Register Pressure·Spilling을 설명합니다.','Block 내부의 안전한 데이터 공유, Tiling을 통한 재사용과 Bank Conflict를 살펴봅니다.','같은 128B의 유효 데이터라도 접근 주소에 따라 필요한 32B Sector 수가 달라지는 원리를 설명합니다.','CUDA의 메모리 공간과 하드웨어 캐시를 구분하고 Hit·Miss 및 Shared/L1 자원 공유를 다룹니다.','논리적 Global 주소와 물리적 DRAM을 구분하고 컨트롤러, Bank·Row·Column, GDDR·HBM 구조를 연결합니다.','벡터 덧셈 하나를 따라 Grid·Block·Warp·Thread, SM의 실행, 캐시와 DRAM의 데이터 공급을 통합합니다.']
def probe(f):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(f)]))
def stamp(t):
 n=int(t);return f'{n//60:02}:{n%60:02}'
def main():
 inputs=[ROOT/'exports'/f'gpuh_{i}.mp4' for i in range(1,12)];data=[probe(f) for f in inputs]
 fields=['codec_type','codec_name','profile','width','height','pix_fmt','r_frame_rate','time_base','sample_rate','channels','channel_layout']
 sig=[[tuple(s.get(k) for k in fields) for s in p['streams']] for p in data];assert all(s==sig[0] for s in sig)
 assert [s['codec_type'] for s in data[0]['streams']]==['video','audio']
 frames=0;chapters=[];concat=[];meta=[';FFMETADATA1','title=GPU 내부의 계산 — Thread에서 DRAM까지 | LEVEL 01–11']
 for i,(f,p,title,detail) in enumerate(zip(inputs,data,TITLES,DETAILS),1):
  v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio');n=int(v['nb_frames']);assert v['r_frame_rate']=='30/1' and (v['width'],v['height'])==(1920,1080)
  duration=Fraction(n,30);assert abs(float(p['format']['duration'])-float(duration))<.001
  concat.append("file '"+f.as_posix()+"'\nduration "+f'{float(duration):.9f}')
  meta+=['[CHAPTER]','TIMEBASE=1/30000',f'START={frames*1000}',f'END={(frames+n)*1000}',f'title={i:02} {title}']
  chapters.append(dict(episode=i,source=str(f.relative_to(ROOT)),title=title,description=detail,start_frame=frames,start_seconds=float(Fraction(frames,30)),duration_seconds=float(duration),frames=n,audio_duration_seconds=float(a['duration']),youtube_time=stamp(Fraction(frames,30))));frames+=n
 (P/'concat.txt').write_text('\n'.join(concat)+'\n',encoding='utf-8');(P/'chapters.ffmetadata').write_text('\n'.join(meta)+'\n',encoding='utf-8');(P/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf-8')
 intro='GPU 내부의 계산 — 하나의 Thread에서 GPU 전체와 DRAM까지\n\nGPU의 실행 구조와 메모리 시스템을 하나의 흐름으로 이해하는 LEVEL 01–11 통합 영상입니다.\nThread·Warp·Block·Grid가 계산을 어떻게 구성하고, SM이 어떻게 실행하며, Register·Shared Memory·캐시·DRAM이 데이터를 어떻게 저장하고 공급하는지 CUDA 코드와 애니메이션으로 살펴봅니다. 마지막에는 벡터 덧셈 하나로 전체 구조를 연결합니다.\n'
 timeline='\n타임라인\n'+'\n'.join(f'{c["youtube_time"]} {c["episode"]:02} {c["title"]}' for c in chapters)
 desc='\n\n구간별 내용\n'+'\n\n'.join(f'{c["episode"]:02}. {c["title"]}\n{c["description"]}' for c in chapters)
 text=intro+timeline+desc+'\n\n#GPU #CUDA #병렬컴퓨팅 #GPU구조 #GPU최적화\n'
 for dest in [P/'youtube_description.txt',ROOT/'exports/gpuh_full_01_11_youtube_description.txt']:dest.write_text(text,encoding='utf-8')
 if '--verify-only' not in sys.argv:
  with (P/'concat.log').open('w',encoding='utf-8') as log:subprocess.run(['ffmpeg','-hide_banner','-n','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-i',str(P/'chapters.ffmetadata'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(OUT)],stdout=log,stderr=log,check=True)
 final=probe(OUT);v=next(s for s in final['streams'] if s['codec_type']=='video');a=next(s for s in final['streams'] if s['codec_type']=='audio')
 assert int(v['nb_frames'])==frames and len(final['chapters'])==11
 assert abs(float(v['duration'])-float(Fraction(frames,30)))<.04 and abs(float(final['format']['duration'])-float(Fraction(frames,30)))<.1
 assert a['codec_name']=='aac' and a['sample_rate']=='44100' and a['channels']==1
 for e,actual in zip(chapters,final['chapters']):assert abs(e['start_seconds']-float(actual['start_time']))<.04
 with (P/'decode.log').open('w',encoding='utf-8') as log:subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(OUT),'-f','null','-'],stdout=log,stderr=log,check=True)
 report=dict(output=str(OUT),method='video/audio stream copy; original durations and tails preserved',width=1920,height=1080,fps='30/1',frames=frames,duration_seconds=float(v['duration']),container_duration_seconds=float(final['format']['duration']),audio_duration_seconds=float(a['duration']),audio='AAC mono 44100Hz',full_decode='passed',bytes=OUT.stat().st_size,chapters=chapters,youtube_rounding='floor to preceding whole second')
 (P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='chapters'},ensure_ascii=False));print('\n'.join(f'{c["youtube_time"]} {c["title"]}' for c in chapters))
if __name__=='__main__':main()
