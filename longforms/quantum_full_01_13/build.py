"""Assemble the thirteen user-selected voiced videos with synchronized chapter boundaries."""
from pathlib import Path
from fractions import Fraction
import json,subprocess,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MEDIA=ROOT/'media/quantum_full_01_13';MEDIA.mkdir(parents=True,exist_ok=True)
TITLES=['흑체복사와 플랑크의 에너지 양자','광전효과와 아인슈타인','러더퍼드의 금박 실험과 원자핵','보어 모형과 원자의 스펙트럼','프랑크–헤르츠 실험','드브로이의 물질파','하이젠베르크의 행렬역학','슈뢰딩거의 파동역학','보른의 확률 해석','데이비슨–거머의 전자 회절','하이젠베르크의 불확정성 원리','보어의 상보성 원리','행렬역학과 파동역학의 연결 · 첫 이야기의 완결']
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def duration(v):return int(v['duration_ts'])*Fraction(v['time_base'])
def stamp(seconds):
 t=math.floor(seconds);return f'{t//60:02}:{t%60:02}'
def main():
 files=[ROOT/'exports'/f'quantum_long_{i}.mp4' for i in range(1,14)];items=[];clips=[];start=Fraction(0)
 for i,path in enumerate(files,1):
  data=probe(path);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio');original_duration=duration(v);clip=path
  assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and float(v.get('start_time',0))==0
  assert a['codec_name']=='aac' and a['sample_rate']=='44100' and a['channels']==1 and float(a.get('start_time',0))==0
  if (v['width'],v['height'],v['r_frame_rate'])!=(1920,1080,'30/1'):
   assert i==4 and (v['width'],v['height'],v['r_frame_rate'])==(1280,720,'24/1')
   frames=math.ceil(original_duration*30);clip=MEDIA/'quantum_long_4_1080p30.mp4'
   print('Normalizing EP.04 to 1080p30',flush=True)
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),'-map','0:v:0','-map','0:a:0',
    '-vf','scale=1920:1080:flags=lanczos,setsar=1,fps=30','-frames:v',str(frames),'-c:v','libx264','-preset','fast','-crf','18','-profile:v','high','-level:v','4.0','-pix_fmt','yuv420p','-video_track_timescale','15360','-c:a','copy','-movflags','+faststart',str(clip)],check=True)
   v=next(s for s in probe(clip)['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==frames
  else:frames=int(v['nb_frames'])
  length=Fraction(frames,30);assert duration(v)==length
  item={'episode':i,'title':TITLES[i-1],'source':str(path),'video_input':str(clip),'start_seconds':float(start),'duration_seconds':float(length),'frames':frames,'audio_samples':int(length*44100),'source_video_duration_seconds':float(original_duration),'source_audio_duration_seconds':float(a['duration']),'video_action':'normalized 720p24 to 1080p30' if clip!=path else 'stream copy'}
  items.append(item);clips.append(clip);start+=length
 manifest={'title':'양자역학의 발견 Part I — 1–13편 합본','duration_seconds':float(start),'frames':sum(i['frames'] for i in items),'episodes':items}
 (HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 concat=MEDIA/'concat.txt';concat.write_text('\n'.join("file '"+path.as_posix()+"'\nduration "+f"{item['duration_seconds']:.9f}" for path,item in zip(clips,items))+'\n',encoding='utf-8')
 metadata=[';FFMETADATA1','title=양자역학의 발견 Part I — 13개의 이야기']
 for item in items:metadata+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(item['start_seconds']*1000)}",f"END={round((item['start_seconds']+item['duration_seconds'])*1000)}",'title='+item['title']]
 meta=HERE/'chapters.ffmetadata';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
 description='''양자역학은 어떻게 탄생했을까요?

뜨거운 물체가 내는 빛, 원자의 안정성, 전자의 파동성. 서로 다른 현상을 설명하려던 시도들이 어떻게 하나의 양자역학으로 연결되었는지 따라갑니다.

플랑크의 흑체복사에서 아인슈타인의 광전효과, 원자핵과 보어 모형, 물질파와 전자 회절, 행렬역학과 파동역학까지. 「양자역학의 발견」 1–13편을 하나로 모은 첫 번째 이야기입니다.

챕터
'''+ '\n'.join(stamp(item['start_seconds'])+' '+item['title'] for item in items)+'''

이 영상에서 다루는 내용
• 에너지와 빛의 양자적 성질
• 원자핵, 에너지 준위와 원자의 스펙트럼
• 물질파와 전자 회절의 실험적 증거
• 행렬역학, 파동역학과 보른의 확률 해석
• 불확정성 원리와 상보성 원리
• 서로 다른 수학적 표현이 같은 물리적 예측으로 연결되는 과정

애니메이션과 일부 그래프는 원리를 설명하기 위한 모형입니다. 실제 실험 장치의 축척이나 측정 데이터를 그대로 재현한 것은 아니며, 필요한 가정과 구분은 영상 안에 표시했습니다.

#양자역학 #물리학 #과학다큐 #과학사 #양자역학의발견
'''
 (HERE/'youtube_description.txt').write_text(description,encoding='utf-8');(ROOT/'exports/quantum_long_1_13_youtube_description.txt').write_text(description,encoding='utf-8')
 (HERE/'youtube_title.txt').write_text('양자역학의 발견 Part I | 플랑크에서 행렬역학과 파동역학의 연결까지\n',encoding='utf-8')
 out=MEDIA/'joined_streams.mp4';args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat)]
 for path in files:args+=['-i',str(path)]
 args+=['-f','ffmetadata','-i',str(meta)];filters=[]
 for i,item in enumerate(items,1):filters.append(f'[{i}:a:0]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=mono,apad,atrim=end_sample={item["audio_samples"]},asetpts=N/SR/TB[a{i}]')
 filters.append(''.join(f'[a{i}]' for i in range(1,14))+'concat=n=13:v=0:a=1[audio]')
 args+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[audio]','-map_metadata','14','-map_chapters','14','-c:v','copy','-c:a','aac','-b:a','192k','-ar','44100','-ac','1','-t',f'{float(start):.9f}','-movie_timescale','1000','-video_track_timescale','30000','-avoid_negative_ts','disabled','-use_editlist','1','-movflags','+faststart',str(out)]
 print(f'Assembling 13 episodes: {float(start):.3f}s',flush=True);subprocess.run(args,check=True)
 # Reset copied video PTS after the AAC mux, preserving composition offsets and all encoded packets.
 joined=out;out=ROOT/'exports/quantum_long_1_13_full.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(joined),'-f','ffmetadata','-i',str(meta),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-bsf:v','setts=pts=PTS-STARTPTS:dts=DTS-STARTPTS','-movie_timescale','1000','-video_track_timescale','30000','-avoid_negative_ts','disabled','-use_editlist','1','-movflags','+faststart',str(out)],check=True)
 data=probe(out);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1') and int(v['nb_frames'])==manifest['frames']
 assert abs(float(duration(v))-float(start))<.002 and abs(float(a['duration'])-float(start))<.03
 assert float(v['start_time'])==0 and float(a['start_time'])==0
 assert abs(float(data['format']['duration'])-float(start))<.002
 chapters=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(out)]))['chapters'];assert len(chapters)==13
 for chapter,item in zip(chapters,items):
  assert abs(float(chapter['start_time'])-item['start_seconds'])<.002
  assert abs(float(chapter['end_time'])-(item['start_seconds']+item['duration_seconds']))<.002
 verification={'output':str(out),'duration_seconds':float(start),'frames':v['nb_frames'],'audio_duration':a['duration'],'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'chapters':chapters,'video':'12 source videos stream copied; episode 4 normalized','audio':'per-episode exact sample padding; one AAC encode'}
 (HERE/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(out,flush=True);print(HERE/'youtube_description.txt',flush=True)
if __name__=='__main__':main()
