import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent;shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True);shutil.copy2(P.parent/'gpuh10_dram'/'shared_style.py',P/'shared_style.py')
s=(P.parent/'gpuh10_dram'/'build.py').read_text(encoding='utf-8').replace('gpuh10_dram_164s','gpuh11_integrated_191s').replace('gpuh10','gpuh11').replace('164','191').replace("default='both'","default='longform'");(P/'build.py').write_text(s,encoding='utf-8')
raw='''지금까지 GPU를 구성하는 여러 실행 단위와 메모리 구조를 살펴봤습니다.|4
스레드부터 워프, 블록, 그리드, 그리고 에스엠까지.|8
여기에 레지스터, 공유 메모리, 전역 메모리와 캐시, 디램까지 등장했습니다.|13
그렇다면 이 모든 구조는 실제 하나의 쿠다 프로그램에서 어떻게 연결될까요?|18
간단한 벡터 덧셈 코드를 살펴보겠습니다.|21
두 배열 A와 B의 같은 위치에 있는 값을 더해, 결과를 C에 저장하는 프로그램입니다.|26
먼저 커널을 실행할 때 그리드와 블록의 크기를 지정합니다.|29
그리드는 하나의 커널 실행에 속한 블록들의 집합이고, 각 블록은 여러 스레드로 구성됩니다.|35
예를 들어 하나의 블록에 128개의 스레드를 배치한다면, 일반적인 엔비디아 GPU에서는 32개씩 네 개의 워프로 구성됩니다.|43
각 스레드는 자신의 스레드 인덱스와 블록 인덱스를 이용해 담당할 배열의 위치를 계산합니다.|50
여기까지는 쿠다 프로그램에서 정의한 논리적인 실행 구조입니다.|53
그렇다면 실제 계산은 어디에서 일어날까요?|56
GPU에는 여러 개의 에스엠이 존재합니다.|59
커널이 실행되면 블록들이 사용 가능한 에스엠에 배치되고, 각 에스엠의 워프 스케줄러는 실행 가능한 워프의 명령을 선택합니다.|67
워프에 속한 스레드들은 에스엠의 연산 자원을 이용해 명령을 수행합니다.|72
이 과정에서 스레드마다 필요한 계산값은 레지스터에 보관될 수 있습니다.|76
같은 블록의 스레드들이 데이터를 함께 사용해야 한다면 공유 메모리를 활용할 수도 있습니다.|81
하지만 모든 데이터가 에스엠 내부에 있는 것은 아닙니다.|85
벡터 덧셈에 필요한 배열 A와 B는 전역 메모리에 존재합니다.|89
각 스레드가 자신의 원소를 읽으려고 하면 GPU의 메모리 시스템에 읽기 요청이 발생합니다.|95
필요한 데이터가 캐시에 존재한다면 엘원이나 엘투 캐시에서 공급받을 수 있습니다.|100
반대로 캐시에 데이터가 없다면 메모리 컨트롤러를 거쳐 디램에 접근해야 할 수 있습니다.|105
읽어온 값이 준비되면 스레드는 두 값을 더하고, 계산 결과를 배열 C에 저장합니다.|111
결과를 저장하는 과정에서도 캐시와 메모리 시스템이 관여할 수 있습니다.|115
여기서 중요한 사실이 하나 있습니다.|117
우리가 작성한 코드는 하나의 덧셈이지만, GPU는 수많은 스레드가 서로 다른 데이터에 대해 같은 계산을 수행하도록 구성합니다.|125
그리고 이 스레드들은 워프로 묶이고, 블록 단위로 에스엠에 배치되며, 하드웨어 자원과 메모리 계층을 활용해 실행됩니다.|133
그렇다면 GPU의 성능은 단순히 스레드가 많을수록 높아질까요?|137
반드시 그렇지는 않습니다.|139
에스엠에 배치할 수 있는 블록의 수는 레지스터와 공유 메모리 같은 자원의 사용량에 영향을 받습니다.|145
또한 스레드들이 데이터를 읽고 쓰는 방식에 따라 필요한 메모리 요청과 데이터 이동량이 달라집니다.|151
결국 GPU에서의 계산은 단순히 수많은 연산을 동시에 수행하는 문제가 아닙니다.|156
어떤 스레드가 계산을 담당하고, 어느 하드웨어에서 실행되며, 필요한 데이터가 어디에서 공급되는지가 함께 결정되어야 합니다.|163
지금까지 살펴본 스레드, 워프, 블록, 그리드는 계산을 구성하는 논리적인 실행 구조입니다.|169
에스엠은 이러한 계산을 실제로 수행하는 하드웨어이고, 레지스터와 공유 메모리, 캐시와 디램은 필요한 데이터를 저장하고 공급하는 메모리 구조입니다.|178
이것이 하나의 쿠다 프로그램을 실행하기 위해 서로 연결되는 GPU의 계층 구조입니다.|183
그리고 GPU 최적화는 바로 이 구조 위에서, 계산과 데이터 이동을 어떻게 더 효율적으로 배치할 것인가라는 질문으로 이어집니다.|191'''
cues=[];start=0
for row in raw.splitlines():
 t,e=row.rsplit('|',1);e=int(e);cap=t
 for a,b in [('쿠다','CUDA'),('에스엠','SM'),('엘원','L1'),('엘투','L2'),('디램','DRAM')]:cap=cap.replace(a,b)
 cues.append(dict(start=start,end=e,caption=cap,tts=t));start=e
ends=[18,26,43,53,72,81,95,105,115,133,145,151,163,178,183,191]
titles=['하나의 CUDA 프로그램으로 연결되는 GPU','끝까지 추적할 계산 · 벡터 덧셈','Grid의 4개 Block · Block당 128 Thread','Block 1의 Thread 5 → 배열 위치 133','논리적 작업을 실제 SM에 배치','Register와 선택적인 Shared Memory','같은 Thread가 요청하는 A[133]와 B[133]','캐시와 DRAM · 같은 Load의 다른 공급 경로','4 + 7 = 11 · 계산과 Global Store','하나의 코드가 512개의 계산으로','상주 규모를 제한하는 하드웨어 자원','주소 패턴이 바꾸는 데이터 이동','누가 · 어디서 · 데이터를 어디에서','실행 조직과 하드웨어·메모리의 연결','하나의 Kernel에서 GPU 실행까지','GPU HIERARCHY — COMPLETE']
events=[[(0,'통합관계도'),(4,'논리Grid Block Warp Thread강조'),(8,'메모리노드강조'),(13,'같은CUDA코드로수렴')],[(18,'A B C첫4원소'),(21,'1+5=6등계산')],[(26,'N512 Grid4 Block128'),(29,'4Block'),(35,'Block0 4Warp각32Thread')],[(43,'Block1 Thread5 i133'),(50,'논리조직과물리SM분리')],[(53,'논리Block/물리SM분리'),(59,'Block1→SM1배치예시'),(63,'Warp0 스케줄'),(67,'SM ALU실행')],[(72,'Register Thread별할당'),(76,'Shared는선택적협력,이커널은미사용')],[(81,'Global논리주소와물리경로'),(85,'A133=4 B133=7'),(89,'각입력요청')],[(95,'A L1Hit/B L2Hit가정'),(100,'같은B Load의대안DRAM사례,제3Load아님')],[(105,'4+7=11'),(111,'C133 GlobalStore요청,DRAM반영시점구별')],[(115,'선택Thread에서전체로'),(117,'Block별128개결과순차채움'),(125,'Warp시간별선택과메모리흐름')],[(133,'상주자원제약'),(139,'Register/Shared제약분리,이커널Shared0')],[(145,'별도stride패턴4→32Sector,원본커널변경아님')],[(151,'동일코드'),(156,'Who Where FromWhere')],[(163,'논리조직'),(169,'물리SM와메모리'),(175,'Controller DRAM연결')],[(178,'KernelLaunch→논리→실행→데이터공급통합')],[(183,'계산배치와데이터이동질문'),(188,'완결문구와관계도유지')]]
accuracy='N=512,Grid4,Block128,4Warp/Block,32Thread/Warp. Block1 Thread5→i133→Warp0 Lane5,선택값A133=4 B133=7 C133=11. 첫4원소A1,2,3,4/B5,6,7,8/C6,8,10,12. Block1→SM1은가정한배치이며실제SM번호·동시성·배치순서는보장되지않음. Warp는32Thread하드웨어실행묶음이며CUDA Launch에서별도크기를지정하는계층이아니다. Shared는원본커널에없고실제데이터이동경로에포함하지않음. 모든변수=고정Register슬롯이아님. CacheHit/Miss/DRAM경로는가정모형. A의L1/B의L2Hit뒤에보이는DRAM은같은B Load의다른상황이며세번째입력이아님. Global Store요청은DRAM기록완료와다름. 512결과채움은동시실행/실제타이밍추적이아님. 자원예산과Coalescing은별도구조설명예시,원본vectorAdd성능실측아님. 논리주소/캐시/DRAM물리공간을동일포함계층에중첩하지않음. 사용자최종요청대로가로형만제작,191초길이유지.'
manifest=[];paras=[];start=0
for i,(end,title) in enumerate(zip(ends,titles)):
 d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True);script='\n'.join(c['tts'] for c in cues if start<=c['start'] and c['end']<=end);paras.append(script);(d/'script.txt').write_text(script+'\n',encoding='utf-8')
 manifest.append(dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Integrated{i+1:02}'}));timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i]);(d/'spec.md').write_text(f'# {title}\n\n## 확정 대본/길이\n{start}–{end}초,사용자문장종료시각.음원미제공.\n\n{script}\n\n## 화면타임라인\n{timeline}\n\n## 지속요소\n상단의Grid·선택Block1 Thread5·SM1·Cache·Controller·DRAM위치를유지한다. 논리조직은왼쪽,물리하드웨어는오른쪽으로분리한다. 하단확대도와코드는상단의요청·값이동에맞춘다.\n\n## 정확성\n{accuracy}\n',encoding='utf-8');(d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom integrated_visuals import IntegratedBase\nclass Integrated{i+1:02}(IntegratedBase):\n    INDEX={i}\n',encoding='utf-8');start=end
for name,data in [('manifest.json',manifest),('timing.json',cues)]: (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8');(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8');(P/'narration.md').write_text('# GPU 통합편 — 확정191초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU LEVEL 11 Integrated\nduration_seconds: 191\nlayout: longform\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8');shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\0384fcec-0d89-4cda-a54e-77277991e340\붙여넣은 텍스트.txt'),P/'storyboard.md');(P/'brief.md').write_text('# 제작 기준\n\n191초 · 가로1920×1080 · 30fps · 무음·전체자막. 사용자대본과시간확정. 명시제공된회상/최종정리는유지하며임의예고없음.\n\n'+accuracy.replace('선택값','선택값')+'\n',encoding='utf-8');(P/'README.md').write_text('# GPU LEVEL 11 — 최종 통합편\n\n191초 · 독립씬16개 · 가로형만 · 30fps · 무음·전체자막.\n\n```powershell\npython longforms/gpuh11_integrated/build.py --preview\npython longforms/gpuh11_integrated/build.py --jobs 4\npython longforms/gpuh11_integrated/verify.py\n```\n\nN512/Block128/Grid4의실행가능한vectorAdd하나를끝까지추적한다. Block1 Thread5 i133에서4+7=11. 캐시·SM배치와자원비교는가정모형이며실제GPU실행추적이아니다. 원본커널의Shared사용은0.\n\n출처: [NVIDIA Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html), [Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).\n',encoding='utf-8');print(len(cues),'cues',len(manifest),'shots')
