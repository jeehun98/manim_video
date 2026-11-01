"""Join the user-selected narrated exports without re-encoding picture."""
from pathlib import Path
import subprocess,json,sys
sys.stdout.reconfigure(encoding="utf-8")
R=Path(__file__).resolve().parent;W=R.parents[1];E=W/'exports';M=W/'media/minimal_full_01_08';M.mkdir(parents=True,exist_ok=True)
def run(cmd):subprocess.run(cmd,check=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(p)]))
titles=['최소 표현 — 무엇을 남겨야 할까?','최소 유전체 — 생명에 필요한 유전자는?','그래프 희소화 — 연결을 줄여도 남는 성질','충분통계량 — 데이터 대신 무엇을 기억할까?','최소 실현 — 같은 동작, 더 적은 상태','재규격화와 보편성 — 다른 구조, 같은 법칙','복권 가설 — 큰 신경망 속 작은 신경망','통합 마무리 — 최소 구조를 찾는 세 가지 질문']
descriptions=['원본을 복원하는 압축과 특정 기능만 유지하는 요약은 어떻게 다를까요? 보존할 조건에 따라 필요한 표현이 달라집니다.','유전자의 필수성은 다른 유전자와 환경에 따라 달라집니다. 473개 유전자의 세포를 만들었다는 사실과 절대적인 최소를 증명하는 일은 구별됩니다.','연결성과 최단거리 보존을 구분하고, 간선을 줄이면서 그래프의 에너지 구조를 근사적으로 보존하는 스펙트럴 희소화를 살펴봅니다.','독립·동일 정규분포와 알려진 분산이라는 조건에서, 표본평균이 모집단 평균의 추론 정보를 보존하는 이유를 살펴봅니다.','내부 상태를 결합해 더 적은 상태로 같은 입출력 동작을 나타냅니다. 제어 가능성과 관측 가능성을 통해 최소 실현을 이해합니다.','임계점 근처에서 서로 다른 미시적 구조가 같은 보편성 부류의 거시적 스케일링 법칙을 공유할 수 있는 이유를 살펴봅니다.','특정 조건에서는 연결 구조와 원래 초기값을 선택한 작은 부분 신경망이 큰 모델에 필적하는 성능으로 학습할 수 있습니다.','서로 다른 보존 대상, 축소 가능성과 최소성, 정확한 보존과 근사 보존을 구분하고 서로 다른 파라미터의 함수 동등성을 질문합니다.']
parts=[];total=0
for i in range(1,9):
 p=E/f'minimal_{i}_long.mp4';d=probe(p);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio');n=int(v['nb_frames']);assert v['r_frame_rate']=='30/1';assert (v['width'],v['height'])==(1920,1080);assert a['sample_rate']=='44100'
 parts.append(dict(index=i,path=str(p),start_frame=total,frames=n,start_seconds=total/30,duration_seconds=n/30,title=titles[i-1],audio_seconds=float(a['duration'])));total+=n
concat=M/'video_concat.txt';concat.write_text('\n'.join("file '"+Path(p['path']).as_posix()+"'" for p in parts)+'\n',encoding='utf-8')
video=M/'joined_video.mp4';run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-c:v','copy','-an',str(video)])
meta=R/'chapters.ffmeta';content=';FFMETADATA1\ntitle=모든 것이 필요할까? — 최소 구조를 찾아서\n'
for j,p in enumerate(parts):
 end=parts[j+1]['start_frame'] if j+1<len(parts) else total
 content+=f'\n[CHAPTER]\nTIMEBASE=1/30\nSTART={p["start_frame"]}\nEND={end}\ntitle={p["title"]}\n'
meta.write_text(content,encoding='utf-8')
cmd=['ffmpeg','-v','error','-y','-i',str(video)]
for p in parts:cmd+=['-i',p['path']]
cmd+=['-f','ffmetadata','-i',str(meta)]
filters=[]
for i,p in enumerate(parts,1):filters.append(f'[{i}:a:0]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,apad,atrim=end_sample={p["frames"]*1470},asetpts=PTS-STARTPTS[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(1,9))+'concat=n=8:v=0:a=1[aout]')
out=E/'minimal_1-8_long_full.mp4'
cmd+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[aout]','-map_metadata','9','-map_chapters','9','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)];run(cmd)
d=probe(out);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio');assert int(v['nb_frames'])==total;assert abs(float(v['duration'])-total/30)<.001;assert abs(float(a['duration'])-total/30)<.03;assert len(d['chapters'])==8
report=dict(output=str(out),total_frames=total,duration_seconds=total/30,video=v,audio=a,parts=parts,chapters=d['chapters'])
(R/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(sec):
 sec=int(sec);return f'{sec//3600}:{sec//60%60:02}:{sec%60:02}' if sec>=3600 else f'{sec//60:02}:{sec%60:02}'
intro='''모든 것이 정말 필요할까요?

복잡한 시스템에서 무엇을 줄이고, 무엇을 남겨야 할까요?
생명과 수학, 물리학, 인공지능의 사례를 따라가며 ‘최소 구조’를 찾는 조건을 살펴봅니다.

핵심은 무조건 작게 만드는 것이 아닙니다. 무엇을 보존할지 먼저 정하고, 그 조건 아래에서 어디까지 줄일 수 있는지 묻는 것입니다.

📌 타임라인
'''
text=intro+'\n'.join(f'{stamp(p["start_seconds"])} {p["title"]}' for p in parts)+'\n\n📖 구간별 내용\n\n'+'\n\n'.join(f'{p["title"]}\n{desc}' for p,desc in zip(parts,descriptions))+'\n\n더 작은 구조를 발견하는 것과, 그것이 가능한 가장 작은 구조임을 증명하는 것은 다릅니다.\n\n#최소구조 #수학 #과학 #인공지능 #신경망\n'
(E/'minimal_1-8_youtube_description.txt').write_text(text,encoding='utf-8');(R/'youtube_description.md').write_text(text,encoding='utf-8')
(R/'README.md').write_text('# 모든 것이 필요할까? 1–8 통합 롱폼\n\n입력: 사용자가 지정한 exports/minimal_1_long.mp4 ~ minimal_8_long.mp4. 영상·음성을 모두 유지하며, 각 입력의 영상 끝까지 오디오 무음을 보충한 뒤 결합. 영상 재인코딩 없음. 기존 파일 변경 없음.\n\n실행: `python longforms/minimal_full_01_08/build.py`\n\n출력: exports/minimal_1-8_long_full.mp4, exports/minimal_1-8_youtube_description.txt. MP4 내부에 8개 챕터 포함. 정확한 시작 시각·검증은 verification.json 참조. 유튜브 타임스탬프는 초 단위 내림 표시.\n',encoding='utf-8')
print(json.dumps(dict(path=str(out),seconds=total/30,frames=total,chapters=[dict(time=stamp(p['start_seconds']),title=p['title']) for p in parts]),ensure_ascii=False))
