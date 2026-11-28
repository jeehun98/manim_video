"""Pair numbered originals, preserve complete voice tracks, then assemble one longform."""
from pathlib import Path
import concurrent.futures,hashlib,json,math,subprocess,shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
EXPORT=ROOT/'exports'
FPS=30
RATE=48000
TITLES=['복소수의 곱셈과 복소미분','코시 적분 공식과 조화함수','리만 곡면과 균일화 정리','쌍곡 거리와 푸앵카레 원판']
TITLE='복소평면에 숨겨진 기하학 — 수의 연산에서 공간의 발견까지'

def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(p)]))

def run(args,log):
 with log.open('w',encoding='utf-8') as f:
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin',*args],check=True,stdout=f,stderr=f)

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def pair(i):
 video=EXPORT/f'complex_geometry_{i:02}.mp4';audio=EXPORT/f'복소_{i}.mp3'
 assert video.is_file() and audio.is_file(),(video,audio)
 vp=probe(video);ap=probe(audio);v=next(s for s in vp['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
 original_frames=int(v['nb_frames']);nominal=original_frames/FPS;ad=float(ap['format']['duration'])
 frames=math.ceil(max(nominal,ad)*FPS-1e-8);duration=frames/FPS
 out=EXPORT/f'complex_geometry_{i:02}_voiced.mp4'
 hashes=dict(video=digest(video),audio=digest(audio))
 signature=hashlib.sha256(json.dumps([hashes,frames,'hold-last-crf18-veryfast-48k-mono-aac192-v1'],sort_keys=True).encode()).hexdigest()
 stamp=HERE/f'{i:02}.sha256'
 if not out.exists() or not stamp.exists() or stamp.read_text()!=signature:
  temp=out.with_name(out.stem+'.building.mp4')
  # Use the actual frame count, including the source with a slightly rounded container timestamp.
  run(['-y','-i',str(video),'-i',str(audio),'-map','0:v:0','-map','1:a:0',
       '-vf',f'fps={FPS},tpad=stop_mode=clone:stop_duration={duration-nominal+1:.9f}',
       '-frames:v',str(frames),'-af',f'aresample={RATE},apad,atrim=end_sample={frames*1600},asetpts=PTS-STARTPTS',
       '-t',f'{duration:.9f}','-c:v','libx264','-crf','18','-preset','veryfast','-threads','4',
       '-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','60000',
       '-x264-params','keyint=30:min-keyint=30:scenecut=0',
       '-c:a','aac','-b:a','192k','-ar',str(RATE),'-ac','1','-movflags','+faststart',str(temp)],HERE/f'pair_{i:02}.log')
  temp.replace(out);stamp.write_text(signature)
 result=probe(out);vo=next(s for s in result['streams'] if s['codec_type']=='video');ao=next(s for s in result['streams'] if s['codec_type']=='audio')
 assert (vo['width'],vo['height'],vo['r_frame_rate'],int(vo['nb_frames']))==(1920,1080,'30/1',frames)
 assert abs(float(vo['duration'])-duration)<.002
 assert abs(float(ao['duration'])-duration)<.025,(i,ao['duration'],duration)
 assert duration>=ad and duration>=nominal
 print(f'PAIRED {i}/4: {duration:.3f}s; last-frame hold {duration-nominal:.3f}s',flush=True)
 return dict(number=i,title=TITLES[i-1],video=str(video),audio=str(audio),output=str(out),source_hashes=hashes,source_video_duration=float(v['duration']),source_video_frames=original_frames,source_audio_duration=ad,frames=frames,duration=duration,hold_seconds=duration-nominal)

def timecode(t):
 ms=round(t*1000)
 return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def yt(t):
 n=int(t);return f'{n//60:02}:{n%60:02}'

def write_delivery(chapters,final,total):
 cues=[]
 for c in chapters:
  data=json.loads((ROOT/f'longforms/complex_geometry_{c["number"]:02}/script.json').read_text(encoding='utf-8'))
  for j,s in enumerate(data['sentences']):
   end=c['duration'] if j==len(data['sentences'])-1 else s['end']
   cues.append((c['start_seconds']+s['start'],c['start_seconds']+end,s['text']))
 assert all(a<b for a,b,_ in cues)
 assert all(abs(a[1]-b[0])<.00001 for a,b in zip(cues,cues[1:]))
 assert abs(cues[-1][1]-total)<.00001
 captions=final.with_name(final.stem+'_captions.srt')
 captions.write_text('\n\n'.join(f'{i}\n{timecode(a)} --> {timecode(b)}\n{s}' for i,(a,b,s) in enumerate(cues,1))+'\n',encoding='utf-8')
 description=TITLE+'\n\n복소수의 계산은 어떻게 공간의 기하학으로 이어질까요?\n\n복소수의 곱셈을 회전과 확대·축소로 바라보는 데서 출발해, 복소미분이 각 점 주변의 변화를 어떻게 제한하는지 살펴봅니다. 코시 적분 공식이 경계와 내부의 정보를 연결하는 과정, 조화함수와 온도 분포의 관계, 함수를 표현하기 위해 공간을 확장하는 리만 곡면을 차례로 따라갑니다.\n\n마지막에는 원판을 자기 자신으로 옮기는 정칙 변환의 미분값을 이용해 새로운 길이 측정법을 유도합니다. 같은 원판이 어떻게 무한히 넓은 쌍곡평면을 표현하는 푸앵카레 원판이 되는지 함께 확인해 보세요.\n\n챕터\n'+ '\n'.join(yt(c['start_seconds'])+' '+c['title'] for c in chapters)+'\n\n이 영상에서 다루는 내용\n• 복소수의 곱셈과 복소미분의 기하학적 의미\n• 코시–리만 방정식과 정칙함수\n• 코시 적분 정리·적분 공식, 테일러 급수\n• 조화함수와 등각 변환을 이용한 온도 문제\n• 제곱근의 두 겹 공간, 리만 곡면과 보편피복\n• 균일화 정리: 리만 구면·복소평면·단위원판\n• 원판 자기동형과 쌍곡 길이 요소의 유도\n• 유한한 원판 안에서 경계까지의 거리가 무한한 이유\n\n우리는 수를 연구하기 시작했지만, 어느 순간 공간을 연구하고 있었습니다.\n\n#복소수 #복소해석학 #리만곡면 #쌍곡기하학 #푸앵카레원판 #수학\n'
 (HERE/'youtube_description.txt').write_text(description,encoding='utf-8')
 shutil.copyfile(HERE/'youtube_description.txt',EXPORT/'complex_geometry_youtube_description.txt')
 return len(cues)

def main():
 HERE.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:chapters=list(pool.map(pair,range(1,5)))
 manifest=HERE/'concat.txt'
 manifest.write_text(''.join("file '"+Path(c['output']).as_posix()+"'\nduration "+format(c['duration'],'.12f')+'\n' for c in chapters),encoding='utf-8')
 meta=[';FFMETADATA1','title='+TITLE];offset=0
 for c in chapters:
  c['start_seconds']=offset/FPS
  meta+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f'END={offset+c["frames"]}',f'title={c["title"]}']
  offset+=c['frames']
 metadata=HERE/'chapters.ffmetadata';metadata.write_text('\n'.join(meta)+'\n',encoding='utf-8')
 final=EXPORT/'complex_geometry_full_01_04_longform.mp4';temp=final.with_name(final.stem+'.building.mp4')
 inputs=['-y','-f','concat','-safe','0','-i',str(manifest),'-i',str(metadata)]
 for c in chapters:inputs+=['-i',c['audio']]
 filters=[]
 for j,c in enumerate(chapters):
  filters.append(f'[{j+2}:a:0]aresample={RATE},aformat=sample_fmts=fltp:channel_layouts=mono,apad,atrim=end_sample={c["frames"]*1600},asetpts=PTS-STARTPTS[a{j}]')
 filters.append(''.join(f'[a{j}]' for j in range(4))+'concat=n=4:v=0:a=1[voice]')
 # Picture is joined from the four voiced chapter files. Encode the original
 # voices once for the final soundtrack to avoid AAC splice padding and extra loss.
 run(inputs+['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[voice]',
             '-map_metadata','1','-map_chapters','1','-c:v','copy','-c:a','aac','-b:a','192k','-ar',str(RATE),'-ac','1',
             '-t',f'{offset/FPS:.9f}','-movflags','+faststart',str(temp)],HERE/'concat.log')
 temp.replace(final)
 result=probe(final);v=next(s for s in result['streams'] if s['codec_type']=='video');a=next(s for s in result['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',offset)
 assert abs(float(v['duration'])-offset/FPS)<.002
 assert abs(float(a['duration'])-offset/FPS)<.025
 assert len(result['chapters'])==4
 for actual,c in zip(result['chapters'],chapters):assert abs(float(actual['start_time'])-c['start_seconds'])<.001
 run(['-v','error','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'],HERE/'decode_check.log')
 assert not (HERE/'decode_check.log').read_text().strip()
 count=write_delivery(chapters,final,offset/FPS)
 report=dict(output=str(final),chapters=chapters,duration_seconds=offset/FPS,video_frames=offset,video=v,audio=a,caption_cues=count,full_decode='passed',method='Pair each numbered source without speed changes or voice cuts; hold last picture to preserve complete voice; join normalized voiced pictures and one-pass original soundtrack with exact 48k sample boundaries.')
 (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'COMPLETE {final}\nDURATION {offset/FPS:.3f}s; {offset} frames; {count} captions; full audio/video decode passed',flush=True)

if __name__=='__main__':main()
