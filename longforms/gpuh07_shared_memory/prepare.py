"""One-time project setup using the user's approved 160-second narration."""
import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
shutil.copy2(P.parent/'gpuh06_register'/'shared_style.py',P/'shared_style.py')
s=(P.parent/'gpuh06_register'/'build.py').read_text(encoding='utf-8').replace('gpuh06_register_175s_motion_v3','gpuh07_shared_memory_160s').replace('gpuh06','gpuh07').replace('175','160')
(P/'build.py').write_text(s,encoding='utf-8')
raw='''GPU의 스레드는 계산에 필요한 값과 중간 결과를 레지스터에 저장할 수 있습니다.|5
그런데 서로 다른 스레드가 같은 데이터를 사용해야 한다면 어떻게 해야 할까요?|10
여기서 등장하는 것이 공유 메모리, Shared Memory입니다.|14
공유 메모리는 같은 블록의 스레드들이 함께 접근할 수 있는 빠른 온칩 메모리입니다.|19
레지스터가 개별 스레드의 계산값을 보관한다면, 공유 메모리는 스레드 사이에서 데이터를 공유하고 재사용하도록 합니다.|27
실제 쿠다 코드를 살펴보겠습니다.|29
128개의 스레드로 구성된 블록에서, 셰어드 키워드로 공유 메모리 배열을 선언합니다.|35
이제 각 스레드는 전역 메모리에서 자신의 데이터를 읽어 공유 메모리에 저장합니다.|40
예를 들어 스레드 5는 5번 위치에, 스레드 6은 6번 위치에 값을 저장합니다.|45
이때 스레드 5가 스레드 6이 저장한 값을 읽을 수도 있습니다.|49
같은 블록의 스레드들이 동일한 공유 메모리 배열에 접근하기 때문입니다.|54
하지만 스레드 6이 아직 값을 저장하지 않았다면 어떻게 될까요?|57
올바른 결과를 보장할 수 없습니다.|59
이때 필요한 것이 싱크스레드입니다.|62
이 명령은 블록의 스레드들이 모두 해당 지점에 도달할 때까지 기다리고, 이전의 공유 메모리 쓰기가 다른 스레드에서도 올바르게 관찰되도록 합니다.|70
따라서 모든 스레드가 데이터를 저장한 뒤 서로의 값을 읽을 수 있습니다.|75
그렇다면 공유 메모리는 단순히 데이터를 전달하기 위한 공간일까요?|79
그렇지는 않습니다. GPU 최적화에서 중요한 역할 중 하나는 데이터 재사용입니다.|84
행렬곱을 생각해 보겠습니다.|86
서로 다른 출력값을 계산하는 스레드들이 동일한 입력 데이터를 반복해서 사용하는 경우가 많습니다.|92
이때 각 스레드가 데이터를 매번 전역 메모리에서 읽는 대신, 블록의 스레드들이 입력 행렬의 일부를 공유 메모리에 가져올 수 있습니다.|99
그리고 여러 스레드가 이 데이터를 반복해서 사용합니다.|103
이처럼 데이터를 작은 타일 단위로 가져와 재사용하는 방식을 타일링, Tiling이라고 합니다.|109
이를 통해 전역 메모리에서 같은 데이터를 반복해서 읽는 횟수를 줄일 수 있습니다.|113
하지만 공유 메모리에도 제약이 있습니다.|116
공유 메모리는 에스엠의 제한된 자원이므로, 블록당 사용량이 많으면 동시에 상주할 수 있는 블록이 줄어들 수 있습니다.|123
또한 공유 메모리는 여러 메모리 뱅크로 나뉩니다.|126
같은 워프의 스레드들이 서로 다른 주소에 접근하더라도, 같은 뱅크에 접근이 집중되면 처리가 분할될 수 있습니다.|133
이를 뱅크 컨플릭트라고 합니다.|135
결국 공유 메모리를 사용한다고 모든 계산이 빨라지는 것은 아닙니다.|139
데이터 재사용의 이점과 동기화 비용, 메모리 접근 패턴을 함께 고려해야 합니다.|144
레지스터가 개별 스레드의 계산값을 유지한다면, 공유 메모리는 같은 블록의 스레드들이 데이터를 공유하고 재사용하는 공간입니다.|152
GPU의 높은 성능은 많은 스레드를 실행하는 것뿐 아니라, 필요한 데이터를 얼마나 효율적으로 이동하고 재사용하는지에도 달려 있습니다.|160'''
def caption(s):
    for a,b in [('쿠다','CUDA'),('에스엠','SM'),('셰어드 키워드','__shared__ 키워드'),('싱크스레드','__syncthreads()'),('뱅크 컨플릭트','Bank Conflict')]:s=s.replace(a,b)
    return s
cues=[];start=0
for line in raw.splitlines():
    s,e=line.rsplit('|',1);e=int(e);cues.append(dict(start=start,end=e,caption=caption(s),tts=s));start=e
ends=[14,27,40,49,54,62,75,84,92,99,109,113,123,135,144,152,160]
titles=['다른 Thread의 값이 필요하다면','Block 안에서 공유하는 저장 공간','선언한 배열이 SM 자원으로','서로 다른 위치에 쓰고 이웃 값 읽기','공유할 수 있는 범위는 같은 Block','아직 기록되지 않은 값을 읽는다면','도착을 기다린 뒤 안전하게 읽기','데이터 공유에서 재사용으로','여러 출력이 같은 입력을 사용','입력 Tile을 Shared에 가져오기','같은 Tile로 여러 출력 계산','Global 요청의 중복을 줄인다','Shared 사용량과 상주 Block','같은 Bank에 모이는 다른 주소','재사용의 이점과 가능한 비용','Register와 Shared의 사용 범위','데이터 이동과 재사용이 만드는 성능']
events=[[(0,'Register의Thread전용값'),(5,'Thread5와6강조,일반지역변수직접공유는차단'),(10,'SharedMemory영역활성화')],[(14,'Block0의Shared할당영역'),(19,'Register전용과Shared협력대비')],[(27,'neighborRead실제코드'),(29,'s128선언,128Thread표시'),(35,'A5→T5→s5, A6→T6→s6')],[(40,'T5에105,T6에106저장'),(45,'동기화완료가정에서T5가s6을읽어106반환')],[(49,'Block0내같은배열범위'),(51,'Block1은별도할당')],[(54,'s6기록미완료를가정한위험,결과?'),(59,'모든Thread가참여하는Barrier강조')],[(62,'도착32'),(64,'도착64'),(66,'도착96'),(69,'도착128'),(70,'배리어통과'),(71,'T5←s6'),(73,'T6←s7')],[(75,'이웃데이터공유에서재사용질문'),(79,'별도GEMM의A B C로전환')],[(84,'별도4×4GEMM중C00,C01선택'),(86,'동일A행데이터가두출력에필요')],[(92,'T=2인As,Bs타일적재'),(95,'Shared에8개입력'),(97,'다른예제와분리된동기화')],[(99,'타일0데이터를서로다른출력에반복사용'),(103,'타일1로바꿔누적'),(107,'C00=90,C01=100,C10=202,C11=228')],[(109,'선택4출력의Global요청원소수32→16,캐시트랜잭션아님')],[(113,'가상Shared용량64KiB'),(116,'블록요구8→16KiB,상주8→4개')],[(123,'32Bank중4개표시'),(126,'4Lane주소0,1,2,3은각기다른Bank'),(129,'주소0,32,64,96은Bank0에집중'),(133,'개념적분할처리')],[(135,'재사용과동기화·용량·Bank제약'),(139,'실제속도보장X')],[(144,'Thread별Register와Block별Shared동시대비'),(148,'T6→s6→T5이동')],[(152,'각Block별Shared영역을여러SM에표시'),(156,'각각의영역내재사용움직임')]]
manifest=[];paras=[];start=0
for i,(end,title) in enumerate(zip(ends,titles)):
    d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True)
    script='\n'.join(c['tts'] for c in cues if start<=c['start'] and c['end']<=end);paras.append(script);(d/'script.txt').write_text(script+'\n',encoding='utf-8')
    m=dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Shared{i+1:02}'})
    manifest.append(m);timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i])
    (d/'spec.md').write_text(f'# {title}\n\n## 목적·핵심 주장\n{title}를지속되는메모리관계도의동작으로설명한다.\n\n## 앞 장면과 연결\nSM0·Block0·Thread5녹색·Thread6주황·Shared청록색식별을유지한다.\n\n## TTS와 확정 길이\n사용자문장종료시각 {start}–{end}초, {end-start}초. 음원미제공.\n\n{script}\n\n## 화면과 타임라인\n{timeline}\n\n## 화면 텍스트\nSharedMemory / Block0 / T5 / T6 / s5 / s6 / __syncthreads(). 코드1–4줄,배경·테두리분리,줄번호없음. 상단도실제값이움직이고상태가변한다.\n\n## 시작·종료 상태\n같은메모리관계도에서값·접근경로·도착상태만갱신한다. 새그림을계속갈아끼우지않고동일객체변형으로이어간다. 다음영상예고없음.\n\n## 정확성\nneighborRead는1Block128Thread·입력A[t]=100+t. T5는s5에쓰고s6에서106을읽는다. 불안전예시는결과를특정하지않으며실제로경쟁커널을실행하지않음. 정상코드는128Thread가모두배리어에참여. GEMM은별도N4,T2·4Thread/Block의예제. 요청원소수32/16은선택4출력에대한소스수준수이며실측DRAM트랜잭션·속도배수가아님. Bank는32개중0–3과활성4Lane만표시,단어주소mod32,같은주소broadcast예외. 용량비교는별도가상SM모델.\n',encoding='utf-8')
    (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom shared_visuals import SharedBase\nclass Shared{i+1:02}(SharedBase):\n    INDEX={i}\n',encoding='utf-8');start=end
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');(P/'timing.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2),encoding='utf-8')
def stamp(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8');(P/'narration.md').write_text('# Shared Memory — 확정160초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU 계층 구조 LEVEL 07 — Shared Memory\nduration_seconds: 160\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\8ff1f064-aa8b-412a-ac49-997653c887dc\붙여넣은 텍스트.txt'),P/'storyboard.md')
(P/'README.md').write_text('# GPU 계층 구조 LEVEL07 — Shared Memory\n\n사용자종료시각160초·17독립씬·가로세로30fps무음전체자막. 상단도기록·이웃읽기·배리어·Tile재사용·Bank접근에동기화해움직인다.\n\n```powershell\npython longforms/gpuh07_shared_memory/build.py --preview\npython longforms/gpuh07_shared_memory/build.py --jobs 4\npython longforms/gpuh07_shared_memory/verify.py\n```\n\nneighborRead1×128,별도GEMM N4/T2,32Bank중4활성Lane검증예제를분리한다.\n',encoding='utf-8')
(P/'brief.md').write_text('# 제작 기준\n\n160초·30fps·세로1080×1920·가로1920×1080. 사용자확정대본및시각유지. 무음·전체자막. 복습문장은이번에명시제공된원문을유지하며추가복습·다음편예고없음.\n\nThread5녹색,Thread6주황,Shared청록,Register보라. Shared는SM물리자원/Block별논리할당을분리. 실제관계도의기록·대기·해제·이웃읽기·Tile재사용·자원점유·Bank경로가변한다. 소스코드와상태변화동기화.\n\n안전한neighborRead만실제CUDA로검증. unsafe화면은미기록값?이며잘못된특정숫자를보장하지않음. 배리어는동시발행이아닌모든참여자의도착과가시성. 다른Block공유배열은분리.\n\n별도GEMM4×4/T2예제의선택C2×2출력은90,100,202,228. Global요청원소수32→16은캐시/DRAM트랜잭션이나실측성능아님. 예제의그리드·Thread수와neighborRead128을섞지않는다. Bank주소는32bitword%32,4활성Lane만확대,동일주소broadcast는예외. 용량64KiB와8/16KiB요구량은가상예시,neighborRead의512B와구분.\n\n출처: NVIDIA CUDA Best Practices Shared Memory/Bank Conflicts 및 CUDA Programming Guide synchronization.\n',encoding='utf-8')
for f in (P/'scenes/01_example').glob('*'):f.unlink()
print('Prepared',len(cues),'cues and',len(manifest),'shots')
