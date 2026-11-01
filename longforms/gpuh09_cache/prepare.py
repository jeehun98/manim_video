import json,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
shutil.copytree(P.parent/'_template',P,dirs_exist_ok=True)
shutil.copy2(P.parent/'gpuh08_global_memory'/'shared_style.py',P/'shared_style.py')
s=(P.parent/'gpuh08_global_memory'/'build.py').read_text(encoding='utf-8').replace('gpuh08_global_memory_165s','gpuh09_cache_169s').replace('gpuh08','gpuh09').replace('165','169');(P/'build.py').write_text(s,encoding='utf-8')
raw='''지금까지 GPU의 레지스터, 공유 메모리, 전역 메모리를 살펴봤습니다.|4
그런데 여기에 엘원 캐시와 엘투 캐시까지 등장한다면, 이들은 어느 메모리에 속하는 것일까요?|9
이 질문에 답하려면 먼저 두 가지 개념을 구분해야 합니다.|13
하나는 프로그램이 데이터를 저장하고 접근하는 메모리 공간이고, 다른 하나는 데이터 접근을 효율적으로 처리하는 하드웨어 캐시입니다.|21
레지스터는 개별 스레드의 계산값을 보관하고, 공유 메모리는 같은 블록의 스레드들이 데이터를 공유하는 공간입니다.|28
전역 메모리는 GPU의 여러 에스엠과 블록에서 접근할 수 있는 대용량 메모리 공간입니다.|34
그렇다면 엘원과 엘투 캐시는 무엇일까요?|37
이들은 전역 메모리에 포함되는 별도의 주소 공간이 아니라, 메모리 접근 과정에서 데이터를 임시로 보관하고 재사용하는 하드웨어 캐시입니다.|45
먼저 GPU의 전체 구조를 살펴보겠습니다.|48
일반적인 엔비디아 GPU에서는 각 에스엠에 가까운 위치에 엘원 캐시가 존재합니다.|53
반면 엘투 캐시는 여러 에스엠이 함께 사용하는 공유 캐시입니다.|57
실제 쿠다 코드를 살펴보겠습니다.|60
스레드가 전역 메모리의 배열 A에서 하나의 값을 읽는다고 생각해 보겠습니다.|64
이 데이터가 엘원 캐시에 존재한다면, 더 먼 메모리까지 접근하지 않고 값을 가져올 수 있습니다.|70
이를 캐시 히트라고 합니다.|72
반대로 데이터가 없다면 캐시 미스가 발생하고, 요청은 다음 메모리 계층으로 전달될 수 있습니다.|78
엘투 캐시에 데이터가 있다면 그곳에서 가져오고, 엘투에도 없다면 디바이스 디램에 접근해야 할 수 있습니다.|84
다만 모든 전역 메모리 요청이 반드시 엘원 캐시를 거치는 것은 아닙니다.|89
실제 접근 경로는 명령과 캐시 정책에 따라 달라질 수 있습니다.|94
그렇다면 공유 메모리와 엘원 캐시는 어떤 관계일까요?|97
여기서 흥미로운 하드웨어 구조가 등장합니다.|100
일부 엔비디아 GPU에서는 공유 메모리와 엘원 캐시가 같은 온칩 메모리 자원을 나누어 사용합니다.|106
하지만 물리적 자원을 공유한다고 해서 같은 메모리 공간인 것은 아닙니다.|111
공유 메모리는 쿠다 코드에서 데이터를 명시적으로 저장하고 관리하며, 같은 블록의 스레드들이 함께 사용합니다.|118
반면 엘원 캐시는 일반적으로 하드웨어가 데이터의 보관과 교체를 관리합니다.|123
즉, 공유 메모리와 엘원 캐시는 물리적으로 가까이 있거나 자원을 공유할 수 있지만, 데이터에 접근하고 관리하는 방식은 서로 다릅니다.|132
엘투 캐시도 마찬가지로 공유 메모리나 전역 메모리의 일부 주소 공간이 아닙니다.|137
여러 에스엠에서 발생하는 메모리 요청을 처리하고, 데이터를 재사용하도록 지원하는 별도의 하드웨어 계층입니다.|144
결국 레지스터, 공유 메모리, 전역 메모리는 데이터가 어떤 공간에 저장되고 누가 접근할 수 있는지를 설명합니다.|151
반면 엘원과 엘투 캐시는 메모리의 데이터를 실제로 어디에서 가져오고 재사용할 수 있는지를 설명합니다.|158
GPU의 메모리 계층을 이해하려면 단순히 저장 공간을 크기순으로 나열하는 것이 아니라, 논리적인 메모리 공간과 실제 하드웨어의 데이터 접근 경로를 함께 살펴봐야 합니다.|169'''
cues=[];start=0
for row in raw.splitlines():
 t,e=row.rsplit('|',1);e=int(e);cap=t
 for a,b in [('엘원','L1'),('엘투','L2'),('에스엠','SM'),('쿠다','CUDA'),('디바이스 디램','Device DRAM')]:cap=cap.replace(a,b)
 cues.append(dict(start=start,end=e,caption=cap,tts=t));start=e
ends=[21,34,45,57,64,72,84,94,106,118,132,144,158,169]
titles=['메모리 공간과 캐시는 다른 관점','데이터는 누가 접근할까?','캐시는 별도의 주소 공간일까?','SM별 L1 · GPU 공용 L2','같은 Global Load의 시작','L1에 데이터가 있다면','L1에 없다면 어디로 갈까?','모든 요청이 L1을 거칠까?','Shared와 L1의 물리적 관계','같은 자원 · 다른 사용 방식','Shared는 코드로 · L1은 하드웨어가','여러 SM이 재사용하는 L2','저장·접근 범위와 데이터 공급 경로','두 관점으로 보는 GPU 메모리']
events=[[(0,'Register Shared Global강조'),(4,'L1 L2질문카드'),(9,'두관점열분리'),(13,'메모리공간과캐시분류')],[(21,'Register Thread/Shared Block'),(28,'Global SM공통주소공간')],[(34,'L1 L2카드'),(37,'Global A5의캐시복사본')],[(45,'전체GPU'),(48,'SM별L1'),(53,'공용L2연결')],[(57,'readArray.cu'),(60,'A5=6읽기요청')],[(64,'L1 Hit가정값6반환'),(70,'Hit표시')],[(72,'L1 Miss가정'),(78,'L2 Hit'),(81,'별도L2 Miss/DRAM사례')],[(84,'L1미사용요청'),(89,'정책과명령에따른차이')],[(94,'Shared/L1동일SM'),(100,'통합온칩자원비례모형만변경')],[(106,'동일자원≠동일공간'),(111,'명시적Shared쓰기')],[(118,'L1하드웨어적재교체'),(123,'관리방식비교')],[(132,'공유L2'),(137,'SM0가읽은데이터가남아SM1에공급')],[(144,'Register Shared Global범위'),(151,'L1 L2데이터공급')],[(158,'동일시스템에서두관점을연결'),(164,'크기순정렬대신범위와경로결론')]]
accuracy='Global은 논리 주소 공간이며 데이터가 캐시에 복사될 수 있다. L1/L2는 별도 CUDA 주소 공간이 아니다. Register는 스레드별 계산 자원, Shared는 Block별 명시적 공유 공간이다. 일부 GPU의 Unified L1/Shared는 물리 자원 공유이며 주소 공간의 통합이나 자동 Shared↔L1 복사가 아니다. 25/75·50/50·75/25는 개념 비율이며 실제 지원 구성이 아니다. 캐시 상태와 경로는 독립적으로 가정한 설명용 사례, 측정된 Hit/Miss·레이턴시·프로파일러 결과가 아니다. 일반 C++ Load가 항상 L1을 사용한다고 보장하지 않는다. L1 bypass는 별도 __ldcg 정책 예제이며 원래 코드가 바뀌지 않고 정책을 지정한 것처럼 보이지 않게 구분한다. L2 SM간 재사용은 입력에 쓰기가 없는 상태와 데이터 잔류를 가정하며 SM간 동기화나 직접 L1 공유를 뜻하지 않는다.'
manifest=[];paras=[];start=0
for i,(end,title) in enumerate(zip(ends,titles)):
 d=P/f'scenes/{i+1:02}_scene';d.mkdir(parents=True,exist_ok=True);script='\n'.join(c['tts'] for c in cues if start<=c['start'] and c['end']<=end);paras.append(script)
 (d/'script.txt').write_text(script+'\n',encoding='utf-8');manifest.append(dict(id=f'{i+1:02}',directory=d.relative_to(P).as_posix(),title=title,start=start,end=end,duration_seconds=end-start,**{'class':f'Cache{i+1:02}'}))
 timeline='\n'.join(f'- {t}초: {s}' for t,s in events[i]);(d/'spec.md').write_text(f'# {title}\n\n## 핵심 주장\n{title}\n\n## 확정 대본과 길이\n{start}–{end}초. 사용자 문장 종료 시각 기준, 음원 미제공.\n\n{script}\n\n## 화면 타임라인\n{timeline}\n\n## 지속 요소와 시작/종료\nSM0의Warp·Register·Shared·L1과 GPU공용L2, DeviceDRAM의 식별을 유지한다. 상단 요청·값 이동이 하단 캐시 상태와 동기화된다. Memory Spaces와 Cache Hierarchy를 별도 축에 둔다. 줄번호 없는 코드 패널과 별도 자막 영역을 유지한다. 다음 영상 예고 없음.\n\n## 정확성\n{accuracy}\n',encoding='utf-8')
 (d/'scene.py').write_text(f'import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom cache_visuals import CacheBase\nclass Cache{i+1:02}(CacheBase):\n    INDEX={i}\n',encoding='utf-8');start=end
for filename,data in [('manifest.json',manifest),('timing.json',cues)]: (P/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def ts(n):return f'{n//3600:02}:{n//60%60:02}:{n%60:02},000'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["caption"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
(P/'tts_script.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8');(P/'narration.md').write_text('# L1 & L2 Cache — 확정169초\n\n'+'\n\n'.join(f'{c["start"]}–{c["end"]}초\n\n{c["caption"]}' for c in cues),encoding='utf-8');shutil.copy2(P/'narration.md',P/'master_script.md')
(P/'scenes.yaml').write_text('title: GPU LEVEL 09 L1 & L2 Cache\nduration_seconds: 169\ntiming_source: user_sentence_end_times\nscenes:\n'+''.join(f'  - id: "{m["id"]}"\n    directory: {m["directory"]}\n    duration_seconds: {m["duration_seconds"]}\n    class: {m["class"]}\n' for m in manifest),encoding='utf-8')
shutil.copy2(Path(r'C:\Users\as042\.codex\attachments\c40de86d-587a-428e-aa17-64b74a91beca\붙여넣은 텍스트.txt'),P/'storyboard.md')
(P/'brief.md').write_text('# 제작 기준\n\n169초 · 가로1920×1080/세로1080×1920 · 30fps · 무음·전체 자막. 사용자 대본과 문장 종료시각 확정. 명시 제공된 도입 유지, 추가 복습과 예고 없음.\n\n'+accuracy+'\n\n실제 CUDA readArray와sharedRead및__ldcg예제의값만GPU검증한다. 캐시애니메이션은명시적상태모형이며 실제GPU상태추적이아니다. A[i]=i+1,선택A5=6,B5=12. L1 Hit는L2/DRAM미접근, L2 Hit는DRAM미접근, bypass는L1미접근. 요청은주황/값은초록, Shared청록/Register보라/Global황금/L1파랑/L2진한파랑.\n',encoding='utf-8')
(P/'README.md').write_text('# GPU LEVEL 09 — L1 & L2 Cache\n\n169초 · 독립 씬14개 · 가로/세로30fps · 무음·전체 자막.\n\n```powershell\npython longforms/gpuh09_cache/build.py --preview\npython longforms/gpuh09_cache/build.py --jobs 4\npython longforms/gpuh09_cache/verify.py\n```\n\n메모리 공간과캐시계층을별도축에배치. 캐시상태/비율은설명용모형이며실측결과가아니다. 실제CUDA계산결과는cuda_trace.json에기록한다.\n\n기술출처: [NVIDIA Programming Model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html), [Writing SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html).\n',encoding='utf-8')
print(len(cues),'cues',len(manifest),'shots')
